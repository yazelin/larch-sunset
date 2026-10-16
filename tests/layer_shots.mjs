// 分層色塊驗證（遵循《正式地圖開工前：先用色塊確認 RPG 的遮擋層次》與《十一分鐘》規範）
// 在各物件後面／前面／旁邊放站著不動的探針人物（跟主角同一套前後排序），
// 截圖到 art/check/layer-<地圖>-<區>.webp。
// behind＝物件北邊、在圖框裡（應被蓋住）；front＝南邊（應畫在物件上面）；side＝旁邊；in＝通道口。
// 用法：node tests/layer_shots.mjs [bar|storage|bedroom]
import { readFileSync, writeFileSync } from 'node:fs';
import { serve, open, sleep } from './lib.mjs';

const A = process.argv[2] || 'bar', MAP = 'm-' + A;
const TABLE = {
  bar: {
    spots: [
      ['吧檯桌-behind', 8, 2, 'down'],
      ['吧檯桌-front', 7, 4, 'up'],
      ['吧檯左通道-in', 6, 3, 'up'],
      ['吧檯右通道-in', 14, 3, 'up'],
      ['酒櫃展牆-front', 10, 2, 'up'],
      ['左走道-front', 3, 4, 'up'],
      ['右走道-front', 16, 4, 'up'],
    ],
    zones: [['全景', [9, 5]]]
  },
  storage: {
    spots: [
      ['百葉窗暗格-front', 6, 3, 'up'],
      ['西側香料木架-side', 3, 5, 'left'],
      ['東側乾料架-side', 13, 5, 'right'],
      ['南側出口門-front', 8, 10, 'down'],
    ],
    zones: [['全景', [7, 9]]]
  },
  bedroom: {
    spots: [
      ['四柱大床-behind', 2, 2, 'down'],
      ['四柱大床-side', 4, 5, 'left'],
      ['四柱大床-front', 2, 8, 'up'],
      ['梳妝鏡台-front', 12, 5, 'up'],
      ['雙門衣櫃-side', 12, 7, 'right'],
      ['南側出口門-front', 9, 10, 'down'],
    ],
    zones: [['全景', [8, 9]]]
  }
};

const SPOTS = TABLE[A].spots, ZONES = TABLE[A].zones;
const proj = JSON.parse(readFileSync('dist/project.json', 'utf8'));
const node = proj.boards.flatMap(b => b.nodes).find(n => n.id === MAP);
if (!node) {
  console.error(`找不到地圖節點 ${MAP}`);
  process.exit(1);
}

const base = JSON.parse(node.data.pluginValues.map);
const walls = new Set();
base.layers.filter(l => l.collision).forEach(l =>
  l.tiles.forEach((t, i) => t && walls.add(`${i % base.width},${Math.floor(i / base.width)}`))
);
const taken = new Set(base.events.map(e => `${e.x},${e.y}`));

for (const [id, x, y] of SPOTS) {
  if (walls.has(`${x},${y}`)) throw new Error(`${id} 站在牆上 (${x}, ${y})`);
  if (taken.has(`${x},${y}`)) throw new Error(`${id} 那一格已經有事件 (${x}, ${y})`);
}

for (const [zone, [hx, hy]] of ZONES) {
  const m = JSON.parse(JSON.stringify(base));
  const hero = m.events.find(e => e.id === 'hero');
  hero.x = hx; hero.y = hy;
  
  SPOTS.forEach(([id, x, y, dir], i) => {
    if (!(x === hx && y === hy)) {
      m.events.push({
        ...hero,
        id: 'probe-' + i,
        name: id,
        x, y,
        actor: 'npc',
        solid: true,
        trigger: 'action',
        actions: [],
        conditions: [],
        direction: dir
      });
    }
  });

  node.data.pluginValues.map = JSON.stringify(m);
  writeFileSync('dist/test-layer.json', JSON.stringify(proj));
  console.log(`Starting preview for ${MAP} zone ${zone}...`);
  const s = await serve('dist/test-layer.json');
  try {
    await fetch(s.base + '/api/lp/card', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card: MAP, line: 0 })
    });
    const ui = await open(s.base, { width: 1280, height: 800 });
    await sleep(6000);
    const outPath = `art/check/layer-${A}-${zone}.webp`;
    await ui.page.screenshot({ path: outPath });
    console.log(`Zone ${zone} screenshot saved to ${outPath}`);
    await ui.close();
  } finally {
    s.kill();
  }
}
