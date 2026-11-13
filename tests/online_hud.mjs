// 線上預覽的常駐 UI 截圖：node tests/online_hud.mjs <預覽網址> → art/check/onhud_<視窗>_<卡>.png。從頭點到暴雨夜（回憶）為止
import { open, sleep } from './lib.mjs';
import { mkdirSync } from 'node:fs';
mkdirSync('art/check', { recursive: true });
const STOP = { return: '人家說頭七妳會回來', rain_1: '先把領帶解開' };   // 各卡第三句
for (const [name, opt] of [['desk', { width: 1600, height: 900 }], ['wide', { width: 2560, height: 1080 }], ['phone', { mobile: true }]]) {
  const ui = await open(process.argv[2], opt);
  await sleep(6000); await ui.clickText('開始遊戲'); await sleep(9000);
  for (const [c, at] of Object.entries(STOP)) {
    for (let k = 0; k < 400 && !(await ui.text()).includes(at); k++) { await ui.advance(); await sleep(450); }
    await sleep(3500); await ui.page.screenshot({ path: `art/check/onhud_${name}_${c}.png` });
    console.log(name, c, (await ui.text()).slice(-60));
  }
  console.log(name, '頁面錯誤', ui.errors.length ? ui.errors.slice(0, 2) : '無'); await ui.close();
}
