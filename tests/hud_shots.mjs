// 常駐 UI（時間標示、回憶柔邊）截圖：node tests/hud_shots.mjs → art/check/hud_*.png。直接跳到指定卡，不從頭玩
import { serve, open, sleep } from './lib.mjs';
import { mkdirSync } from 'node:fs';
mkdirSync('art/check', { recursive: true });
const s = await serve('dist/project.json');
const CARDS = (process.argv[2] || 'open_1,return,rain_2').split(',');
try {
  for (const [name, opt] of [['desk', { width: 1600, height: 900 }], ['wide', { width: 2560, height: 1080 }], ['phone', { mobile: true }]]) {
    for (const c of CARDS) {
      await fetch(s.base + '/api/lp/card', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: s.base }, body: JSON.stringify({ card: c, line: 0 }) });
      const ui = await open(s.base, opt);
      await sleep(6000);   // 跳卡模式直接進那張卡，沒有標題畫面
      await ui.advance(); await sleep(1200); await ui.advance(); await sleep(3000);
      await ui.page.screenshot({ path: `art/check/hud_${name}_${c}.png` });
      console.log(name, c, ui.errors.length ? ui.errors.slice(0, 2) : 'ok'); await ui.close();
    }
  }
} finally { s.kill(); }
