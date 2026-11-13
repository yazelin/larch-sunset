// 線上預覽檢查（不預設自動播放）：node tests/online_check.mjs <預覽網址>。標題截圖、按開始後不點要停在第一句、再一路點幾句
import { open, sleep, assert } from './lib.mjs';
const ui = await open(process.argv[2], { width: 1600, height: 900 });
const bad = []; ui.page.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url().slice(0, 100)); });
const text = async () => (await Promise.all(ui.page.frames().map(f => f.evaluate(() => document.body.innerText).catch(() => '')))).join(' | ');
await sleep(6000); await ui.page.screenshot({ path: 'art/check/online_title.png' });
const title = await text(); assert(/戴上耳機/.test(title) && !/自動播放/.test(title), '標題說明沒有提自動播放');
await ui.clickText('開始遊戲'); await sleep(15000);
const a = await text(); assert(/七張高腳椅都有人/.test(a) && !/那瓶白酒幫我拿/.test(a), '按開始後不點，停在第一句不會自己往下');
for (let i = 0; i < 8; i++) { await ui.advance(); await sleep(800); }
await sleep(1500); await ui.page.screenshot({ path: 'art/check/online_2.png' });
assert(/阿忠|小葵|沈淮|安雅/.test(await text()), '點了會往下');
assert(!bad.length && !ui.errors.length, '沒有失敗的請求與頁面錯誤 ' + bad.concat(ui.errors).slice(0, 3).join(' / '));
await ui.close();
