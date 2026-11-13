// 片尾字卷從開始到回標題要多久（對照主題曲長度）：SPEED=8 node tests/credits_time.mjs
import { serve, open, sleep, SPEED } from './lib.mjs';
const s = await serve('dist/project.json');
try {
  await fetch(s.base + '/api/lp/card', { method: 'POST', headers: { 'Content-Type': 'application/json', Origin: s.base }, body: JSON.stringify({ card: 'credits', line: 0 }) });
  const ui = await open(s.base, { width: 1600, height: 900 }); const t0 = Date.now();
  await ui.waitText(/開始遊戲/, 120000 * 8);
  console.log('片尾字卷約', Math.round((Date.now() - t0) * SPEED / 1000), '秒（含載入）');
  await ui.close();
} finally { s.kill(); }
