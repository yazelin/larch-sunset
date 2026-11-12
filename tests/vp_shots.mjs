// 不同視窗比例下，第一張圖與字卡後第一張圖的截圖：node tests/vp_shots.mjs → art/check/vp_*.png
import { serve, open, sleep } from './lib.mjs';
import { mkdirSync } from 'node:fs';
mkdirSync('art/check', { recursive: true });
const s = await serve('dist/project.json');
try {
  for (const [name, opt] of [['1920x940', { width: 1920, height: 940 }], ['2560x1080', { width: 2560, height: 1080 }], ['1280x900', { width: 1280, height: 900 }], ['844x390', { width: 844, height: 390 }], ['phone', { mobile: true }]]) {
    const ui = await open(s.base, opt);
    await sleep(4000); await ui.clickText('開始遊戲'); await sleep(7000);
    await ui.advance(); await sleep(2500); await ui.page.screenshot({ path: `art/check/vp_${name}.png` });
    const info = await ui.page.evaluate(() => [...document.querySelectorAll('img,div,iframe')].filter(e => { const r = e.getBoundingClientRect(); const bg = getComputedStyle(e).backgroundImage; return r.width > 300 && (e.tagName !== 'DIV' || bg.includes('url')); }).slice(0, 12).map(e => { const r = e.getBoundingClientRect(), c = getComputedStyle(e); return [e.tagName, e.className.toString().slice(0, 40), Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height), c.objectFit, c.backgroundSize, c.objectPosition]; }));
    console.log(name, JSON.stringify(info)); await ui.close();
  }
} finally { s.kill(); }
