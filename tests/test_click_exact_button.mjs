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

  // Click center of "繼續探索 >" button at (1170, 671) repeatedly
  for (let i = 0; i < 4; i++) {
    console.log(`Clicking 繼續探索 button at (1170, 671), step ${i}...`);
    await page.mouse.click(1170, 671);
    await page.waitForTimeout(1200);
  }

  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_choice_buttons_final.png' });
  console.log('Saved preview_choice_buttons_final.png');

} catch (e) {
  console.error('Test error:', e);
} finally {
  await browser.close();
}
