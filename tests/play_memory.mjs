// 回憶篇試玩：遺言之後 → 回憶一（坐下、她調第一杯、門口塞傘）→ CG → 回憶二（黃銅匙、她教他）→ CG → 回憶三（那杯、甜嗎）→ CG → 回到現實 → 終局抉擇。
// 專案複製一份、把開頭改到 card_mem_enter，省掉前面整段解謎。每一步點任務提示（引擎會把沈淮走過去）再按互動鍵。
// WRONG=1 改選另一組選項（都有、最烈的、先看著她、再試一次、轉過身、太甜、不問），看她的反應有沒有接上。截圖存 art/check/mem-<步>.png。
// node tests/play_memory.mjs   （先 python3 src/build.py；HEADED=1 看畫面）
import { serve, open, sleep, assert } from './lib.mjs';
import fs from 'node:fs';
const p = JSON.parse(fs.readFileSync('dist/project.json', 'utf8'));
for (const b of p.boards) for (const n of b.nodes) { delete n.data.start; if (n.id === 'card_mem_enter') n.data.start = true; }
fs.mkdirSync('art/check', { recursive: true });
fs.writeFileSync('dist/test-memory.json', JSON.stringify(p));
const WRONG = !!process.env.WRONG;
const s = await serve('dist/test-memory.json');
const ui = await open(s.base, { width: 1600, height: 900 });
const { page, text } = ui;
const shot = n => page.screenshot({ path: `art/check/mem-${n}.png` });
const visible = async t => { for (const f of page.frames()) if (await f.getByText(t, { exact: false }).first().isVisible().catch(() => false)) return true; return false; };
// 選項：看到就點（對的或錯的那個）
const PICK = WRONG
  ? ['「都有。」', '「來杯最烈的。」', '先看著她', '再試一次', '轉過身', '「有點太甜。」', '什麼都不說']
  : ['「躲雨。」', '「不要太苦就好。」', '喝一口', '「妳教我。」', '握緊她的手', '「剛好。」', '問她怎麼了'];
let seen = '';
const PROMPTS = ['回答她：躲雨，還是喝酒？', '點什麼？', '杯子推到你面前。', '又混了。', '她的手還覆在你手上。', '回答她甜不甜。', '她看起來有點不一樣。'];
async function until(re, ms = 90000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    const t = await text(); seen += t;
    if (re.test(t)) return t;
    const opt = PICK.find(o => t.includes(o));
    if (opt && await visible(opt)) { await ui.clickText(opt); await sleep(600); continue; }
    // 選擇題剛跳出來、選項還沒點得到：不要按 Enter（會選到預設的第一個）
    if (PROMPTS.some(q => t.includes(q))) { await sleep(300); continue; }
    await ui.advance(); await sleep(450);
  }
  throw new Error('等不到 ' + re + '\n畫面：' + (await text()).slice(-600));
}
async function step(note, expect, name) {
  for (let k = 0; k < 4; k++) {
    await ui.clickText(note); await sleep(5000);
    await page.keyboard.press('Space'); await sleep(800);
    try { await until(expect, 40000); await shot(name); return; } catch (e) { if (k === 3) throw e; console.log('  重試', note); }
  }
}
try {
  await ui.clickText('開始遊戲'); await sleep(1500);
  await until(/三年前的那個晚上/); await shot('0-enter');
  await until(/還有一杯的時間/); assert(true, '回憶一開場：他淋濕進門');
  await until(/坐到吧檯前的高腳椅/); await shot('1-map');
  await step('坐到吧檯前的高腳椅', /往門口走/, '1-taste'); assert(true, '坐下、點酒、喝第一杯');
  await step('雨小了，往門口走', /一直下到天亮|教你調酒/, '1-leave'); assert(true, '她追到門口塞傘');
  await until(/一直下到天亮|教你調酒/); await shot('1-cg'); assert(true, '過了 CG 1');
  await until(/拿吧檯角落的黃銅匙/); await shot('2-map');
  await step('拿吧檯角落的黃銅匙', /把匙交給她/, '2-spoon'); assert(true, '拿到黃銅匙');
  await step('把匙交給她', /只借你/, '2-hands'); assert(true, '她握著他的手教，匙只借他');
  await until(/一直放在自己的位置上|試試這杯/); await shot('2-cg'); assert(true, '過了 CG 2');
  await until(/試試這杯/); await until(/喝她推過來的那杯/); await shot('3-map');
  await step('喝她推過來的那杯', /真正的晚霞/, '3-sunset'); assert(true, '她說想看晚霞');
  await until(/第一次說想看晚霞|妳想看的晚霞/); await shot('3-cg'); assert(true, '過了 CG 3');
  await until(/妳想看的晚霞，在這杯裡/); await shot('4-return'); assert(true, '回到現實');
  await until(/一口飲盡/); await shot('5-choice'); assert(true, '接上終局抉擇');
  if (WRONG) { const miss = [/貪心/, /今晚聽我的/, /看我做什麼/, /還是攪成一團/, /近到看得見/, /沒有問/].filter(r => !r.test(seen)); assert(!miss.length, '錯的選項都有反應' + (miss.length ? '，缺：' + miss.join(' ') : '')); }
  else for (const r of [/雨停之前/, /握進掌心/, /怎麼了/, /嚐不出你調的酒/]) assert(r.test(seen), '選項台詞有出現：' + r);
  console.log(ui.errors.length ? ui.errors : '沒有頁面錯誤');
} catch (e) { await shot('fail'); console.error(e.message); process.exitCode = 1; }
finally { await ui.close(); s.kill(); }
