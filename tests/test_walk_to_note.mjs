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
  console.log('Focusing game canvas...');
  await page.mouse.click(640, 360);
  await page.waitForTimeout(500);

  // Move left 4 times
  for (let i = 0; i < 4; i++) {
    await page.keyboard.press('KeyA');
    await page.waitForTimeout(250);
  }

  // Move up 1 time
  await page.keyboard.press('KeyW');
  await page.waitForTimeout(350);

  // Interact with note at (8, 6)
  console.log('Interacting with note...');
  await page.keyboard.press('Space');
  await page.waitForTimeout(1000);

  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_at_note.png' });
  console.log('Saved preview_at_note.png');

  // Advance dialogue
  for (let i = 0; i < 3; i++) {
    await page.keyboard.press('Space');
    await page.waitForTimeout(800);
  }

  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_choice_screen.png' });
  console.log('Saved preview_choice_screen.png');

} catch (e) {
  console.error('Test error:', e);
} finally {
  await browser.close();
}
