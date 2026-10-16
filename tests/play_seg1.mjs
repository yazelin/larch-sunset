// 第一段試玩：序幕（頭七）→ 吧檯空杯與便條 → 燒到一半的風味筆記三題 → 回憶一 → 回到吧檯，任務換成拿匙。
// node tests/play_seg1.mjs   （先 python3 src/build.py；HEADED=1 看畫面）截圖存 art/check/s1-<步>.png
import { serve, open, sleep, assert } from './lib.mjs';
import fs from 'node:fs';
fs.mkdirSync('art/check', { recursive: true });
const s = await serve('dist/project.json');
const ui = await open(s.base, { width: 1600, height: 900 });
const { page, text } = ui;
const shot = n => page.screenshot({ path: `art/check/s1-${n}.png` });
const visible = async t => { for (const f of page.frames()) if (await f.getByText(t, { exact: false }).first().isVisible().catch(() => false)) return true; return false; };
const PICK = ['貴腐甜白酒', '番紅花', '粉紅胡椒', '「躲雨。」', '「不要太苦就好。」', '喝一口'];
const PROMPTS = ['他怕苦。』', '他說剛好。』', '像天快亮。』', '回答她：躲雨，還是喝酒？', '點什麼？', '杯子推到你面前。'];
let seen = '';
async function until(re, ms = 90000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    const t = await text(); seen += t;
    if (re.test(t)) return t;
    const opt = PICK.find(o => t.includes(o));
    if (opt && PROMPTS.some(q => t.includes(q)) && await visible(opt)) { await ui.clickText(opt); await sleep(600); continue; }
    if (PROMPTS.some(q => t.includes(q))) { await sleep(300); continue; }
    await ui.advance(); await sleep(450);
  }
  throw new Error('等不到 ' + re + '\n畫面：' + (await text()).slice(-600));
}
async function step(note, expect, name) {
  for (let k = 0; k < 4; k++) {
    await ui.clickText(note); await sleep(5000);
    await page.keyboard.press('Space'); await sleep(800);
    try { await until(expect, 60000); await shot(name); return; } catch (e) { if (k === 3) throw e; console.log('  重試', note); }
  }
}
try {
  await ui.clickText('開始遊戲'); await sleep(1500);
  await until(/最先被帶走的/); await shot('0-prologue'); assert(true, '序幕獨白');
  await until(/看看吧檯上的空杯和便條/); await shot('1-bar');
  await step('看看吧檯上的空杯和便條', /還有營業嗎/, '2-mem1'); assert(true, '便條→筆記三題→進回憶一');
  for (const r of [/記得吃飯/, /從來不署名/, /〈破曉〉。那是她給那杯酒取的名字/]) assert(r.test(seen), '有出現 ' + r);
  await until(/坐到吧檯前的高腳椅/);
  await step('坐到吧檯前的高腳椅', /往門口走/, '3-taste');
  for (const r of [/最黑的時候，喝一杯天亮/, /那就叫它〈破曉〉/, /你也怕苦/]) assert(r.test(seen), '回憶一有 ' + r);
  await step('雨小了，往門口走', /一直下到天亮/, '4-cg'); assert(true, '過了 CG 1');
  await until(/黃銅調酒匙/); await shot('5-back'); assert(true, '回到吧檯，任務換成拿匙');
  console.log(ui.errors.length ? ui.errors : '沒有頁面錯誤');
} catch (e) { await shot('fail'); console.error(e.message); process.exitCode = 1; }
finally { await ui.close(); s.kill(); }
