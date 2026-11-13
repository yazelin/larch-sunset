/* 《晚霞》片尾主題曲 MV（底子照《餘燼》site/mv.js，動效另做）。資料由 site/build_mv.py 注入：
   MV.theme = { dur, audio, shots:[{t0,t1,cg,img,move,blank,tone,rain}], lines:[{t,en,zh,sec,key,w:[[字,秒]],z:[[段,秒]]}], env:[0..1 每 50 毫秒] }
   網址參數：embed=1（嵌進遊戲：不顯示署名與返回連結、右下「繼續」）、rec=1（錄影用：不顯示任何按鈕與進度線）。
   播完或按「繼續」送 {type:'larch:mv:done'} 給父層；載入時送 {type:'larch:mv:ready'}。
   錄影時由外部注入 window.__makeAudio（照虛擬時間走的假音軌），頁面其餘邏輯不變。 */
const Q = new URLSearchParams(location.search);
const KEY = 'theme';
const SONG = MV[KEY];
const EMBED = Q.get('embed') === '1';
const REC = Q.get('rec') === '1';
const reduced = matchMedia('(prefers-reduced-motion:reduce)').matches;
const lowEnd = matchMedia('(pointer:coarse)').matches || (navigator.hardwareConcurrency || 4) <= 4;
const $ = id => document.getElementById(id);
const root = document.documentElement;
if (EMBED) document.body.classList.add('embed');
if (REC) document.body.classList.add('rec');
const tell = type => { if (window.parent !== window) try { parent.postMessage({ type, song: KEY }, '*'); } catch (_) {} };
tell('larch:mv:ready');

const au = window.__makeAudio ? window.__makeAudio(SONG) : new Audio();
if (!window.__makeAudio) { au.preload = 'auto'; au.src = SONG.audio; }
SONG.shots.forEach(s => { const im = new Image(); im.src = s.img; });
const lines = SONG.lines, ENV = SONG.env, LAST = lines[lines.length - 1];

/* ── 畫面：一鏡一張，交叉淡化，推鏡方向照分鏡表；回憶偏暖、頭七偏冷 ── */
const MOVES = {
  in: ['scale(1.02)', 'scale(1.13)'], out: ['scale(1.13)', 'scale(1.02)'],
  left: ['translateX(2.5%) scale(1.09)', 'translateX(-2.5%) scale(1.09)'], right: ['translateX(-2.5%) scale(1.09)', 'translateX(2.5%) scale(1.09)'],
};
let shot = -1, front = 'fA';
function showShot(i) {
  if (i === shot) return; shot = i;
  const s = SONG.shots[i], nxt = front === 'fA' ? 'fB' : 'fA', n = $(nxt), f = $(front);
  n.style.backgroundImage = `url("${s.img}")`;
  n.getAnimations().forEach(a => a.cancel());
  if (!reduced) n.animate([{ transform: MOVES[s.move][0] }, { transform: MOVES[s.move][1] }], { duration: (s.t1 - s.t0 + 3) * 1000, easing: 'linear', fill: 'forwards' });
  else n.style.transform = 'scale(1.04)';
  n.classList.add('on'); f.classList.remove('on'); front = nxt;
  document.body.dataset.shot = s.cg; document.body.dataset.tone = s.tone;
}

/* ── 歌詞：一次一句。英文照唱到的字一個一個浮出來，中文跟著分段出現 ── */
let lyr = -2, lfront = 'lA', curWords = [];
function span(cls, text, t) { const e = document.createElement('span'); e.className = cls; e.textContent = text; e._t = t; return e; }
function showLine(k) {
  const nxt = lfront === 'lA' ? 'lB' : 'lA';
  $(lfront).classList.remove('on'); curWords = [];
  if (k < 0) return;
  const ln = lines[k], p = $(nxt); p.textContent = ''; p.className = (ln.key ? 'key ' : '') + ln.sec;
  const e = document.createElement('span'); e.className = 'en'; e.lang = 'en';
  ln.w.forEach((w, i) => { const s = span('w', w[0], w[1]); e.append(s); if (i < ln.w.length - 1) e.append(' '); curWords.push(s); });
  const z = document.createElement('span'); z.className = 'zh';
  ln.z.forEach(g => { const s = span('z', g[0], g[1]); z.append(s); curWords.push(s); });
  p.append(e, z); p.classList.add('on'); lfront = nxt;
}
let pour = 0, amp = 0;
function frame(dt) {
  const t = au.currentTime;
  let i = 0; while (i + 1 < SONG.shots.length && SONG.shots[i + 1].t0 <= t) i++;
  showShot(i);
  let k = -1; while (k + 1 < lines.length && lines[k + 1].t <= t) k++;
  if (k === lines.length - 1 && t > SONG.fade) k = -1;          // 最後一句唱完，字跟著畫面一起暗下去
  const key = SONG.shots[i].blank ? -1 : k;
  if (key !== lyr) { lyr = key; showLine(key); }
  for (const s of curWords) if (!s._on && t >= s._t) { s._on = true; s.classList.add('lit'); }
  document.body.dataset.line = key;
  document.body.classList.toggle('intro-on', t > 1.4 && t < SONG.shots[1].t0 - 2.2);
  /* 副歌：畫面底部像倒酒，紅、金、粉紅一層一層疊上來；副歌結束慢慢退掉 */
  const chorus = key >= 0 && lines[key].sec === 'chorus';
  const target = chorus ? Math.min(1, (t - lines[key - lines[key].nth].t) / 7 + .12) : 0;
  pour += (target - pour) * Math.min(1, dt * (target > pour ? 1.6 : .7));
  root.style.setProperty('--pour', pour.toFixed(3));
  const e = ENV[Math.min(ENV.length - 1, Math.max(0, Math.floor(t * SONG.hz)))] || 0;
  amp += (e - amp) * Math.min(1, dt * 6);
  root.style.setProperty('--amp', amp.toFixed(3));
  $('prog').style.width = (Math.min(1, t / SONG.dur) * 100).toFixed(2) + '%';
  if (t >= SONG.fade && !au.paused) { $('black').classList.add('on'); document.body.classList.add('end-on'); }
}

/* ── 顆粒：一張雜訊圖鋪滿，位置跳動 ── */
{ const c = document.createElement('canvas'); c.width = c.height = 160; const x = c.getContext('2d'), d = x.createImageData(160, 160);
  for (let i = 0; i < d.data.length; i += 4) { const v = 90 + Math.random() * 165; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
  x.putImageData(d, 0, 0); $('grain').style.backgroundImage = `url(${c.toDataURL()})`; }

/* ── 雨絲與氣泡：雨夜那幾鏡下雨，其他時候是氣泡酒的氣泡，跟著音量多一點、亮一點 ── */
const fx = $('fx'), g = fx.getContext('2d');
let W = 0, H = 0;
function resize() { const d = Math.min(devicePixelRatio || 1, 1.5); W = innerWidth; H = innerHeight; fx.width = Math.round(W * d); fx.height = Math.round(H * d); g.setTransform(d, 0, 0, d, 0, 0); }
addEventListener('resize', resize); resize();
const spr = document.createElement('canvas'); spr.width = spr.height = 32;
{ const c = spr.getContext('2d'), gr = c.createRadialGradient(16, 16, 0, 16, 16, 16); gr.addColorStop(0, 'rgba(255,244,222,.95)'); gr.addColorStop(.35, 'rgba(242,196,109,.45)'); gr.addColorStop(1, 'rgba(234,169,182,0)'); c.fillStyle = gr; c.fillRect(0, 0, 32, 32); }
const bits = [], drops = [], MAXB = lowEnd ? 14 : 34, MAXD = lowEnd ? 40 : 110;
let prev = performance.now(), rainLv = 0;
function tick(now) {
  const dt = Math.min((now - prev) / 1000, .05); prev = now;
  if (!au.paused) frame(dt);
  if (!reduced) {
    g.clearRect(0, 0, W, H);
    const sp = au.paused ? .3 : 1, s0 = SONG.shots[Math.max(0, shot)];
    rainLv += ((s0 && s0.rain ? 1 : 0) - rainLv) * Math.min(1, dt * .8);
    /* 雨 */
    if (rainLv > .02) {
      while (drops.length < MAXD * rainLv) drops.push({ x: Math.random() * (W + 200) - 100, y: Math.random() * H, l: 14 + Math.random() * 26, v: 900 + Math.random() * 700, a: .05 + Math.random() * .13 });
      g.lineWidth = 1; g.lineCap = 'round';
      for (let i = drops.length - 1; i >= 0; i--) {
        const d = drops[i]; d.y += d.v * dt * sp; d.x -= d.v * .16 * dt * sp;
        if (d.y > H + 30) { if (drops.length > MAXD * rainLv) { drops.splice(i, 1); continue; } d.y = -30; d.x = Math.random() * (W + 200) - 60; }
        g.strokeStyle = `rgba(200,215,240,${(d.a * rainLv).toFixed(3)})`; g.beginPath(); g.moveTo(d.x, d.y); g.lineTo(d.x + d.l * .16, d.y - d.l); g.stroke();
      }
    } else drops.length = 0;
    /* 氣泡 */
    const lv = (1 - rainLv) * (.45 + amp * 1.1);
    if (bits.length < MAXB && Math.random() < dt * 3.4 * sp * lv) bits.push({ x: Math.random() * W, y: H + 10, vy: -(22 + Math.random() * 38), s: 1.6 + Math.random() * 4.2, ph: Math.random() * 6.3, life: 8 + Math.random() * 6, age: 0 });
    g.globalCompositeOperation = 'lighter';
    for (let i = bits.length - 1; i >= 0; i--) {
      const p = bits[i]; p.age += dt * sp; p.ph += dt * sp;
      if (p.age > p.life || p.y < -20) { bits.splice(i, 1); continue; }
      p.y += p.vy * dt * sp; p.x += Math.sin(p.ph) * 9 * dt * sp;
      g.globalAlpha = (.3 + amp * .35) * Math.min(1, p.age / .8) * Math.min(1, (p.life - p.age) / 1.5) * (1 - rainLv * .8);
      const s = p.s * 2.4; g.drawImage(spr, p.x - s / 2, p.y - s / 2, s, s);
    }
    g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
showShot(0);

/* ── 播放、繼續、結束 ── */
let done = false;
function finish() { if (done) return; done = true; tell('larch:mv:done'); if (!EMBED && !REC) $('again').hidden = false; }
$('go').onclick = () => {
  au.play().then(() => { $('start').classList.add('gone'); if (EMBED) $('next').hidden = false; }).catch(() => { $('sub').textContent = '音樂載入不了，請再按一次'; });
};
$('next').onclick = () => { au.pause(); finish(); };
$('again').onclick = () => { done = false; $('again').hidden = true; $('black').classList.remove('on'); document.body.classList.remove('end-on'); au.currentTime = 0; shot = -1; lyr = -2; pour = 0; au.play(); };
au.onended = () => { $('black').classList.add('on'); document.body.classList.add('end-on'); finish(); };
addEventListener('keydown', e => {
  if (e.code === 'Space' || e.key === 'Enter') { e.preventDefault(); if ($('start').classList.contains('gone')) { au.paused ? au.play() : au.pause(); } else $('go').click(); }
  else if (['Backspace', 'BrowserBack'].includes(e.key) || (e.altKey && e.key.startsWith('Arrow'))) e.preventDefault();   // 按鍵不能把畫面帶離這頁
});
