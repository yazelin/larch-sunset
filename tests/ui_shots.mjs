// 介面截圖：標題（桌機、手機直放）與一句對話。node tests/ui_shots.mjs → art/check/ui_*.png
import { serve, open, sleep } from './lib.mjs';
import { mkdirSync } from 'node:fs';
mkdirSync('art/check', { recursive: true });
const s = await serve('dist/project.json');
try {
  for (const [name, opt] of [['desk', { width: 1600, height: 900 }], ['phone', { mobile: true }]]) {
    const ui = await open(s.base, opt);
    await sleep(5000); await ui.page.screenshot({ path: `art/check/ui_title_${name}.png` });
    await ui.clickText('開始遊戲'); await sleep(9000); await ui.page.screenshot({ path: `art/check/ui_dialogue_${name}.png` });
    for (let i = 0; i < 4; i++) { await ui.advance(); await sleep(700); }
    await sleep(1500); await ui.page.screenshot({ path: `art/check/ui_dialogue2_${name}.png` });
    console.log(name, ui.errors.length ? ui.errors : 'ok'); await ui.close();
  }
} finally { s.kill(); }
