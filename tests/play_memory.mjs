// 回憶篇試玩：遺言之後 → 回憶一（毛巾、說話、調酒）→ CG → 回憶二（黃銅匙、教她）→ CG → 回憶三（那杯、甜嗎）→ CG → 回到現實 → 終局抉擇。
// 專案複製一份、把開頭改到 card_mem_enter，省掉前面整段解謎。每一步點任務提示（引擎會把沈淮走過去）再按互動鍵。
// WRONG=1 改選錯的選項（泥煤、苦精、肉桂、在旁邊說），看她的反應有沒有接上。截圖存 art/check/mem-<步>.png。
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
  ? ['泥煤威士忌', '苦精', '肉桂粉', '在旁邊說給她聽', '「有點太甜。」', '什麼都不說']
  : ['貴腐甜白酒', '番紅花糖漿', '粉紅胡椒', '握住她的手示範', '「剛好。」', '問她怎麼了'];
let seen = '';
const PROMPTS = ['基酒用什麼？', '再加一點什麼？', '最後收尾？', '怎麼教她？', '她看起來有點不一樣。'];
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
  await until(/還有一杯的時間/); assert(true, '回憶一開場：她進門');
  await until(/拿沙發上的乾毛巾給她/); await shot('1-map');
  await step('拿沙發上的乾毛巾給她', /把毛巾交給安雅/, '1-towel'); assert(true, '拿到毛巾');
  await step('把毛巾交給安雅', /替她調第一杯/, '1-talk'); assert(true, '跟她說話');
  await step('替她調第一杯', /兩點十七分。我會記得/, '1-taste'); assert(true, '調完第一杯，她說會記得');
  await until(/一直下到天亮|又混掉了/); await shot('1-cg'); assert(true, '過了 CG 1');
  await until(/又混掉了/); await until(/拿吧檯角落的黃銅匙/); await shot('2-map');
  await step('拿吧檯角落的黃銅匙', /教她用黃銅匙/, '2-spoon'); assert(true, '拿到黃銅匙');
  await step('教她用黃銅匙', /以後就是我的了/, '2-hands'); assert(true, '教她，她說匙是她的了');
  await until(/一直放在她的位置上|試試這杯/); await shot('2-cg'); assert(true, '過了 CG 2');
  await until(/試試這杯/); await until(/喝她推過來的那杯/); await shot('3-map');
  await step('喝她推過來的那杯', /真正的晚霞/, '3-sunset'); assert(true, '她說想看晚霞');
  await until(/第一次說想看晚霞|妳想看的晚霞/); await shot('3-cg'); assert(true, '過了 CG 3');
  await until(/妳想看的晚霞，在這杯裡/); await shot('4-return'); assert(true, '回到現實');
  await until(/一口飲盡/); await shot('5-choice'); assert(true, '接上終局抉擇');
  if (WRONG) { const miss = [/燒焦的木頭/, /苦的不要/, /你說的我聽不懂/, /沒有問/, /換了甜白酒/, /改拿番紅花/, /拿起粉紅胡椒/].filter(r => !r.test(seen)); assert(!miss.length, '錯的選項都有反應' + (miss.length ? '，缺：' + miss.join(' ') : '')); }
  else for (const r of [/怎麼了/]) assert(r.test(seen), '選項台詞有出現：' + r);
  console.log(ui.errors.length ? ui.errors : '沒有頁面錯誤');
} catch (e) { await shot('fail'); console.error(e.message); process.exitCode = 1; }
finally { await ui.close(); s.kill(); }
