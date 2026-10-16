import { chromium } from '/home/ct/larch-preview/node_modules/playwright-core/index.mjs';

const base = 'http://127.0.0.1:8798';
const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

try {
  await page.goto(base + '/');
  await page.waitForTimeout(2000);

  const frame = page.frameLocator('#player');
  const startBtn = frame.getByRole('button', { name: /開始遊戲/ });
  if (await startBtn.isVisible()) {
    await startBtn.click();
  }

  await page.waitForTimeout(2000);
  await frame.locator('.vn2-box').click();
  await page.waitForTimeout(3000);

  // Focus canvas
  await page.mouse.click(640, 360);
  await page.waitForTimeout(400);

  // Move to (8, 7) facing UP
  await page.keyboard.press('KeyA');
  await page.waitForTimeout(250);
  await page.keyboard.press('KeyA');
  await page.waitForTimeout(250);
  await page.keyboard.press('KeyW');
  await page.waitForTimeout(250);

  // Press Enter to interact with note
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1000);

  // Advance by clicking text=繼續探索 repeatedly
  const playerFrame = page.frame({ url: /play\/market/ });
  let rpgFrame = null;
  if (playerFrame) {
    for (const cf of playerFrame.childFrames()) {
      if (cf.url().includes('rpg') || cf.url().includes('plugin')) {
        rpgFrame = cf;
      }
    }
  }

  const activeFrame = rpgFrame || playerFrame;
  console.log('Active frame found:', !!activeFrame);

  for (let i = 0; i < 5; i++) {
    const nextBtn = activeFrame.locator('text=繼續探索');
    if (await nextBtn.isVisible().catch(() => false)) {
      console.log(`Clicking 繼續探索 step ${i}...`);
      await nextBtn.click();
      await page.waitForTimeout(1200);
    } else {
      console.log(`No 繼續探索 found at step ${i}, pressing Space`);
      await page.keyboard.press('Space');
      await page.waitForTimeout(1000);
    }
  }

  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_choice_active_full.png' });
  console.log('Saved preview_choice_active_full.png');

} catch (e) {
  console.error('Test error:', e);
} finally {
  await browser.close();
}
