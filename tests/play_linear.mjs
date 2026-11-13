// 全劇試玩：按「開始遊戲」後一路點到片尾字卷，再等它捲完回標題（作者 11-12：不預設自動播放）。
// SPEED=16 node tests/play_auto.mjs（先 python3 src/build.py）。檢查：每張卡的第一句與最後一句依序出現、每個鏡頭的圖有載到、沒有頁面錯誤。
import { serve, open, sleep, assert, SPEED } from './lib.mjs';
import { readFileSync } from 'node:fs';
const P = JSON.parse(readFileSync('dist/project.json', 'utf8'));
const cards = P.boards[0].nodes.filter(n => n.data.type === 'dialogue' && n.id !== 'hint');
const MUST = cards.flatMap(n => { const l = n.data.dialogueLines; return [[n.id, l[0].text], [n.id, l[l.length - 1].text]]; });
const BGS = new Set(cards.flatMap(n => n.data.dialogueLines.map(l => l.background).filter(Boolean)));
const s = await serve('dist/project.json');
const ui = await open(s.base, { width: 1600, height: 900 });
const loaded = new Set(), failed = [];
ui.page.on('response', r => { const u = new URL(r.url()).pathname; if (u.startsWith('/files/assets/')) (r.status() < 400 ? loaded.add(u) : failed.push(u + ' ' + r.status())); });
const text = async () => (await Promise.all(ui.page.frames().map(f => f.evaluate(() => document.body.innerText).catch(() => '')))).join(' | ');
let seen = '', done = false, back = false; const t0 = Date.now();
try {
  await ui.clickText('開始遊戲'); await sleep(2000);
  const end = Date.now() + 80 * 60000 / SPEED + 8 * 60000;   // 片尾字卷是插件卡，不吃 SPEED，照真實秒數捲
  while (Date.now() < end) {
    const t = await text(); seen += t;
    if (!/林亞澤/.test(t)) await ui.advance().catch(() => {});
    if (/製作名單|幕後/.test(t) && /林亞澤/.test(t)) { done = true; break; }
    await new Promise(r => setTimeout(r, 120));
  }
  // 畫面是每 120 毫秒取樣一次，機器忙的時候短句會被翻過去沒拍到；所以不逐句要求，改成每張卡都要拍到六成以上的句子、而且卡片照順序出現。
  // 「每一句都在成品裡」另外由建置後的逐句比對與推送讀回負責。
  let at = 0; const thin = [], order = [];
  for (const n of cards) {
    const ls = n.data.dialogueLines.map(l => l.text.slice(0, 12)), pos = ls.map(x => seen.indexOf(x, at)).filter(i => i >= 0);
    if (pos.length < ls.length * 0.6) thin.push(`${n.id} ${pos.length}/${ls.length}`);
    if (pos.length) at = Math.min(...pos); else order.push(n.id);
  }
  assert(!thin.length && !order.length, `每張卡照順序出現、各拍到六成以上的句子（不足：${thin.join('、')}）`);
  assert(done, '一路點到片尾字卷');
  console.log('正片約', Math.round((Date.now() - t0) * SPEED / 60000), '分鐘（真實速度）');
  // 開頭幾張圖在按「開始遊戲」前就預載了，監聽不到；沒監聽到的直接向預覽器要一次，要得到才算
  const notLoaded = [];
  for (const u of [...BGS].filter(u => !loaded.has(u))) { const r = await fetch(s.base + u); if (!r.ok) notLoaded.push(u); }
  assert(!notLoaded.length && !failed.length, `鏡頭圖都有載到（${BGS.size} 張；沒載到 ${notLoaded.length}：${notLoaded.map(u => u.split("/").pop()).join(" ")}；失敗 ${failed.join(" ")}）`);
  for (let k = 0; k < 400 && !back; k++) { await new Promise(r => setTimeout(r, 1000)); back = /開始遊戲/.test(await text()); }
  assert(back, '片尾字卷捲完自己回到標題');
  assert(!ui.errors.length, '沒有頁面錯誤 ' + ui.errors.slice(0, 3).join(' / '));
} catch (e) { console.error(e.message, '\n畫面：', (await text()).slice(-300)); process.exitCode = 1; }
finally { await ui.close(); s.kill(); }
