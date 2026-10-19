// 全劇試玩：序幕 → 吧檯 → 回憶一 → 匙 → 回憶二 → 儲藏間 → 回憶三 → 臥室木盒（輸入 0217）→ 回憶四 → 床 → 調〈晚霞〉→ 遺言 → 抉擇 → 結局。
// END=cold 走〈冷卻的餘溫〉，預設〈共赴晚霞〉。node tests/play_full.mjs（先 python3 src/build.py；HEADED=1 看畫面）。截圖 art/check/full-<n>.png
import { serve, open, sleep, assert } from './lib.mjs';
fs_mk();
function fs_mk() { import('node:fs').then(fs => fs.mkdirSync('art/check', { recursive: true })); }
const COLD = process.env.END === 'cold';
const CHOICES = {
  '他怕苦。』': '貴腐甜白酒', '這一杯要兩匙。』': '番紅花', '像天快亮。』': '粉紅胡椒',
  '回答她：躲雨，還是喝酒？': '「躲雨。」', '點什麼？': '「不要太苦就好。」', '杯子推到你面前。': '喝一口',
  '又混了。': '「妳教我。」', '她的手還覆在你手上。': '握緊她的手',
  '回答她甜不甜。': '「有點太甜。」', '她看起來有點不一樣。': '問她怎麼了',
  '匙要插進哪裡？': '右邊滑軌的縫', '怎麼用力？': '手腕放輕，貼著慢慢轉',
  '先放什麼？': '甜白酒，再兩匙番紅花糖漿', '匙怎麼轉？': '貼著杯壁，慢慢轉，不要用力', '最後是那罐胡椒。': '磨在杯口',
  '她拜託我倒掉。': COLD ? '照她說的倒掉' : '替她嚐',
};
const GUIDE = ['看看吧檯上的空杯和便條', '坐到吧檯前的高腳椅', '雨小了，往門口走', '吧檯角落的黃銅匙', '拿吧檯角落的黃銅匙', '繞進吧檯，把匙交給她',
  '去儲藏間找她熬的番紅花糖漿', '工作台的抽屜', '喝她推過來的那杯', '回吧檯', '上樓，回我們的房間', '她的木盒', '她那一側的床', '下樓，回吧檯', '站到她的位置'];
const END_RE = COLD ? /我留下來，替她記得/ : /最後留下來的，也是/;
const MUST = [/她的頭七這一晚，我才知道/, /記得吃飯/, /那就叫它〈破曉〉/, /以後我調不動了/, /第一次接吻/, /少兩匙/, /還差一點/,
  /這罐有毒/, /在我這裡，杯子不准直接放桌上/, /沈淮，如果/, /連這裡都要/, /瞞了你快三年/, /只剩我一個人/, /目前無治療方式/, /偏頭痛/, /你調的，都好甜/, /跟你一起看，才是這種顏色/, /兩個人換了位置/, /睡吧/, /我就知道你會找到這裡/, /毒在胡椒裡/, COLD ? /沒有人回答/ : /是那天晚上的味道/, ...(COLD ? [] : [/把空杯放回杯墊上/])];
// LIVE=<Larch 預覽網址>：直接在 Larch 本站的播放器上跑（推上去之後驗收用）
const s = process.env.LIVE ? { base: process.env.LIVE, kill() {} } : await serve('dist/project.json');
const ui = await open(s.base, { width: 1600, height: 900 });
const { page } = ui;
// 預覽器的「跳到…」下拉選單有全部卡片標題，讀畫面文字時要拿掉，不然會把卡名當成任務提示
const text = async () => (await Promise.all(page.frames().map(f => f.evaluate(() => {
  const c = document.body.cloneNode(true); c.querySelectorAll('select, option, script, style').forEach(e => e.remove()); return c.textContent;
}).catch(() => '')))).join(' | ').replace(/\s+/g, ' ');
let seen = '', n = 0;
const shot = () => page.screenshot({ path: `art/check/full-${COLD ? 'cold' : 'burn'}-${String(n++).padStart(2, '0')}.png` });
const vis = async (t, f0) => { for (const f of f0 ? [f0] : page.frames()) if (await f.getByText(t, { exact: false }).first().isVisible().catch(() => false)) return true; return false; };
const boxOpen = async () => { for (const f of page.frames()) { const b = f.locator('.vn2-box'); if (await b.count() && await b.first().isVisible().catch(() => false)) return true; } return false; };
async function inputBox() { for (const f of page.frames()) { const i = f.locator('input[type=text], input:not([type])'); if (await i.count() && await i.first().isVisible().catch(() => false)) return i.first(); } return null; }
const guided = new Map();
const clickVisible = async t => { for (const f of page.frames()) { const l = f.getByText(t, { exact: false }).filter({ visible: true }); if (await l.count()) { await l.first().click(); return true; } } return false; };
try {
  await ui.clickText('開始遊戲'); await sleep(1500);
  const end = Date.now() + 25 * 60000;
  while (Date.now() < end) {
   try {
    const t = await text(); seen += t;
    if (END_RE.test(seen)) break;   // 用累積讀到的文字判斷：加速時最後一句可能只在畫面上一閃
    const inp = await inputBox();
    if (inp) { await inp.fill('0217'); await page.keyboard.press('Enter'); await sleep(800); continue; }
    const q = Object.keys(CHOICES).find(k => t.includes(k));
    if (q && await vis(CHOICES[q])) { await shot(); await clickVisible(CHOICES[q]); await sleep(700); continue; }
    if (q) { await sleep(300); continue; }
    // 翻頁前後各讀一次：Larch 本站比較慢，長句打字還沒完就翻過去會漏讀
    if (await boxOpen()) { await sleep(300); seen += await text(); await ui.advance(); await sleep(700); seen += await text(); continue; }
    let g = null; for (const x of GUIDE) if (t.includes(x) && await vis(x)) { g = x; break; }
    if (g) {
      const k = (guided.get(g) || 0) + 1; guided.set(g, k);
      if (k > 6) throw new Error('卡在任務：' + g);
      await shot(); await clickVisible(g); await sleep(5000); await page.keyboard.press('Space'); await sleep(900); continue;
    }
    await ui.advance(); await sleep(400);
   } catch (e) {
    // 換場時畫面框架會整個換掉，剛好讀到就會丟 detached；等一下再讀
    if (!/detached|Target closed|Execution context|has been closed/.test(e.message)) throw e;
    await sleep(800);
   }
  }
  await shot();
  assert(END_RE.test(seen), '走到結局 ' + (COLD ? '〈冷卻的餘溫〉' : '〈共赴晚霞〉'));
  for (const r of MUST) assert(r.test(seen), '有出現 ' + r);
  console.log(ui.errors.length ? ui.errors : '沒有頁面錯誤');
} catch (e) { await shot(); console.error(e.message, '\n畫面：', (await text()).slice(-500)); process.exitCode = 1; }
finally { await ui.close(); s.kill(); }
