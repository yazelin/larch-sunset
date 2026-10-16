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
  await page.waitForTimeout(500);

  // From (10, 7): Move Left 2 times to (8, 7)
  await page.keyboard.press('KeyA');
  await page.waitForTimeout(300);
  await page.keyboard.press('KeyA');
  await page.waitForTimeout(300);

  // Face UP towards (8, 6)
  await page.keyboard.press('KeyW');
  await page.waitForTimeout(300);

  // Press Enter to interact with note
  console.log('Interacting with note...');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1000);

  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_note_dialogue1.png' });
  console.log('Saved preview_note_dialogue1.png');

  // Advance dialogue to see choice options
  for (let i = 0; i < 4; i++) {
    await page.keyboard.press('Space');
    await page.waitForTimeout(1000);
  }

  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_note_choice_active.png' });
  console.log('Saved preview_note_choice_active.png');

} catch (e) {
  console.error('Test error:', e);
} finally {
  await browser.close();
}
