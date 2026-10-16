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

  // Find the quest note or player frame
  const playerFrame = page.frame({ url: /play\/market/ });
  let rpgFrame = null;
  if (playerFrame) {
    for (const cf of playerFrame.childFrames()) {
      if (cf.url().includes('rpg') || cf.url().includes('plugin')) {
        rpgFrame = cf;
      }
    }
  }

  const targetFrame = rpgFrame || playerFrame || frame;
  console.log('Target frame found:', !!targetFrame);

  // Click on the quest guidance banner
  const questEl = targetFrame.locator('text=閱讀吧檯上的便條紙與空高腳杯');
  console.log('Quest note visible?', await questEl.isVisible().catch(() => false));
  if (await questEl.isVisible()) {
    await questEl.click();
    console.log('Clicked quest note!');
  } else {
    // If not found in frame directly, try clicking at coordinate (110, 200) where the banner is
    console.log('Clicking quest banner coordinates...');
    await page.mouse.click(110, 200);
  }

  // Wait for hero to walk to the note (about 2-3 seconds)
  await page.waitForTimeout(3500);

  // Press Enter / Space / Talk button to interact with note
  console.log('Pressing Space / clicking Talk...');
  await page.keyboard.press('Space');
  await page.waitForTimeout(1500);

  // Take screenshot of dialogue
  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_rpg_dialogue.png' });
  console.log('Saved preview_rpg_dialogue.png');

  // Advance dialogue to reach choices
  for (let i = 0; i < 4; i++) {
    await page.keyboard.press('Space');
    await page.waitForTimeout(800);
  }

  // Take screenshot of choices
  await page.screenshot({ path: '/home/ct/.gemini/antigravity-cli/brain/6ac18277-6f59-4166-bad3-11257b816c39/preview_rpg_choice.png' });
  console.log('Saved preview_rpg_choice.png');

} catch (e) {
  console.error('Test error:', e);
} finally {
  await browser.close();
}
