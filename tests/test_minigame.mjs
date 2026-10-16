import { chromium } from '/home/ct/larch-preview/node_modules/playwright-core/index.mjs';

const base = 'http://127.0.0.1:8798';
console.log('Testing mini-games on', base);

const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

const logs = [];
page.on('console', m => logs.push(`[${m.type()}] ${m.text()}`));
page.on('pageerror', e => logs.push(`[PAGEERROR] ${e.message}`));

try {
  await page.goto(base + '/');
  await page.waitForTimeout(2000);

  const frame = page.frameLocator('#player');
  const startBtn = frame.getByRole('button', { name: /開始遊戲/ });
  if (await startBtn.isVisible()) {
    await startBtn.click();
    console.log('Clicked start button');
  }

  await page.waitForTimeout(2000);
  // Advance through prologue
  console.log('Advancing through prologue...');
  await frame.locator('.vn2-box').click();
  await page.waitForTimeout(3000);

  // Take screenshot of RPG map with hero
  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_rpg_bar_map.png' });
  console.log('Saved RPG map preview to preview_rpg_bar_map.png');

  // Let's find child frames or game canvas
  const playerFrame = page.frame({ url: /play\/market/ });
  let rpgFrame = null;
  if (playerFrame) {
    for (const cf of playerFrame.childFrames()) {
      if (cf.url().includes('rpg') || cf.url().includes('plugin')) {
        rpgFrame = cf;
      }
    }
  }

  // Press 'W' or Up arrow to walk up to the note, or click on the note
  console.log('Pressing Space/Enter/Arrow keys to test interaction...');
  await page.keyboard.press('ArrowUp');
  await page.waitForTimeout(300);
  await page.keyboard.press('ArrowUp');
  await page.waitForTimeout(300);
  await page.keyboard.press('Space');
  await page.waitForTimeout(1000);

  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_rpg_interact.png' });
  console.log('Saved interaction preview');
  console.log('Console logs count:', logs.length);
} catch (e) {
  console.error('Test error:', e);
} finally {
  await browser.close();
  console.log('Test completed.');
}
