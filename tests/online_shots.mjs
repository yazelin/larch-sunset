// 線上預覽截圖：node tests/online_shots.mjs <預覽網址> → art/check/online_*.png；列出失敗的請求
import { open, sleep } from './lib.mjs';
import { mkdirSync } from 'node:fs';
mkdirSync('art/check', { recursive: true });
const ui = await open(process.argv[2], { width: 1600, height: 900 });
const bad = []; ui.page.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url().slice(0, 120)); });
await sleep(6000); await ui.page.screenshot({ path: 'art/check/online_title.png' });
await ui.clickText('開始遊戲'); await sleep(9000); await ui.page.screenshot({ path: 'art/check/online_1.png' });
for (let i = 0; i < 6; i++) { await ui.advance(); await sleep(900); }
await sleep(2000); await ui.page.screenshot({ path: 'art/check/online_2.png' });
console.log('頁面錯誤', ui.errors.length ? ui.errors.slice(0, 3) : '無', '；失敗的請求', bad.length ? bad.slice(0, 5) : '無');
await ui.close();
