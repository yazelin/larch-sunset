// 線上預覽免點試玩：SPEED=16 node tests/online_auto.mjs <預覽網址>。只按「開始遊戲」，要自己播到片尾名單；列出失敗的請求
import { open, sleep, assert, SPEED } from './lib.mjs';
const ui = await open(process.argv[2], { width: 1600, height: 900 });
const bad = [], audio = new Set(); ui.page.on('response', r => { const u = r.url(); if (r.status() >= 400) bad.push(r.status() + ' ' + u.slice(0, 100)); if (/\.mp3/.test(u) && r.status() < 400) audio.add(u.split('/').pop()); });
const text = async () => (await Promise.all(ui.page.frames().map(f => f.evaluate(() => document.body.innerText).catch(() => '')))).join(' | ');
let seen = '', done = false;
try {
  await ui.clickText('開始遊戲'); await sleep(2000);
  const end = Date.now() + 80 * 60000 / SPEED + 4 * 60000;
  while (Date.now() < end) { const t = await text(); seen += t; if (/林亞澤/.test(t) && /幕後/.test(t)) { done = true; break; } await new Promise(r => setTimeout(r, 80)); }
  for (const s of ['店裡七張高腳椅坐滿了', '記得吃飯', '甜的', '店我想繼續開', '進來坐，今天有開']) assert(seen.includes(s), '線上播到「' + s + '」');
  assert(done, '線上自己播到片尾名單');
  assert(!bad.length, '沒有失敗的請求 ' + bad.slice(0, 3).join(' / '));
  console.log('載到的音檔', [...audio].sort().join(' '));
  assert(!ui.errors.length, '沒有頁面錯誤 ' + ui.errors.slice(0, 2).join(' / '));
} catch (e) { console.error(e.message, '\n畫面：', (await text()).slice(-200)); process.exitCode = 1; }
finally { await ui.close(); }
