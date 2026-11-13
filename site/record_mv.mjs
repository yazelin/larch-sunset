// 把 docs/theme.html（片尾主題曲 MV）逐格錄成影片：node site/record_mv.mjs [輸出.mp4] [只錄前幾秒]
// 做法：頁面的時間全部換成假的（performance.now、requestAnimationFrame、音軌、所有 CSS 轉場與動畫），
// 每一格往前推 1/30 秒、截一張圖餵給 ffmpeg，最後配上原音檔。這樣不會掉格，畫面和聲音對得準。
// 錄的是 ?rec=1 的版面：沒有按鈕、返回連結、進度線。
import { chromium } from '/home/ct/larch-preview/node_modules/playwright-core/index.mjs';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const OUT = path.resolve(process.argv[2] || path.join(ROOT, 'site/out/theme_mv.mp4'));
const LIMIT = process.argv[3] ? +process.argv[3] : 0;
const FPS = 30, W = 1920, H = 1080, TAIL = 6;   // 歌結束後多留幾秒給結尾那句話
mkdirSync(path.dirname(OUT), { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROME || '/usr/bin/google-chrome', args: ['--no-sandbox', '--disable-gpu', '--force-device-scale-factor=1', '--hide-scrollbars'] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.log('頁面錯誤', e.message));
await page.addInitScript(() => {
  let now = 0, id = 0; const rafs = [], seen = new WeakMap();
  performance.now = () => now;
  window.requestAnimationFrame = cb => { rafs.push([++id, cb]); return id; };
  window.cancelAnimationFrame = i => { const k = rafs.findIndex(r => r[0] === i); if (k >= 0) rafs.splice(k, 1); };
  window.__makeAudio = song => {
    const a = { paused: true, currentTime: 0, ended: false, onended: null, _t0: 0,
      play() { this.paused = false; this.ended = false; this._t0 = now - this.currentTime * 1000; return Promise.resolve(); }, pause() { this.paused = true; } };
    window.__au = a; window.__dur = song.dur; return a;
  };
  const sync = () => {   // 所有轉場與動畫都停住，位置照假時間算
    void document.body.offsetWidth;
    for (const an of document.getAnimations()) {
      if (!seen.has(an)) { seen.set(an, now); try { an.pause(); } catch (_) {} }
      try { an.currentTime = now - seen.get(an); } catch (_) {}
    }
  };
  window.__step = ms => {
    now += ms; const a = window.__au;
    if (a && !a.paused) { a.currentTime = (now - a._t0) / 1000; if (a.currentTime >= window.__dur) { a.currentTime = window.__dur; a.paused = true; a.ended = true; a.onended && a.onended(); } }
    sync();                                   // 先把上一格留下的動畫推到現在
    const q = rafs.splice(0); for (const [, cb] of q) cb(now);
    sync();                                   // 這一格新開始的轉場從 0 起算
  };
});
await page.goto('file://' + path.join(ROOT, 'docs/theme.html') + '?rec=1');
// 圖和字型都先載完，免得錄到一半才換字型
await page.evaluate(async () => {
  await Promise.all(MV.theme.shots.map(s => new Promise(r => { const im = new Image(); im.onload = im.onerror = r; im.src = s.img; })));
  const zh = MV.theme.lines.map(l => l.zh).join('') + '記得吃飯。晚霞片尾主題曲', en = MV.theme.lines.map(l => l.en).join(' ') + ' ENDING THEME';
  await Promise.all([document.fonts.load('400 40px "LXGW WenKai TC"', zh), document.fonts.load('500 40px "Cormorant Garamond"', en), document.fonts.load('900 40px "Noto Serif TC"', zh), document.fonts.load('500 20px "Noto Serif TC"', zh), document.fonts.load('700 14px "Noto Sans TC"', en)]);
  await document.fonts.ready;
});
const dur = await page.evaluate(() => MV.theme.dur);
const total = Math.round((LIMIT || dur + TAIL) * FPS);
const audio = path.join(ROOT, 'assets/bgm/theme.mp3');
const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-i', audio,
  '-filter_complex', '[1:a]apad[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', String(FPS),
  '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
const closed = new Promise(r => ff.on('close', r));
await page.evaluate(() => { __step(0); document.getElementById('go').click(); });
const t0 = Date.now();
for (let f = 0; f < total; f++) {
  await page.evaluate(ms => __step(ms), 1000 / FPS);
  const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 300 === 0) console.log(`第 ${f}/${total} 格（影片 ${(f / FPS).toFixed(0)} 秒），已花 ${((Date.now() - t0) / 1000).toFixed(0)} 秒`);
}
ff.stdin.end(); await closed; await browser.close();
console.log('完成', OUT);
