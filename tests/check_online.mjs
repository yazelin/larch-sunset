import { chromium } from '/home/ct/larch-preview/node_modules/playwright-core/index.mjs';

const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

const target = 'https://larch.ink/preview/eyJwcm9qZWN0SWQiOiJwcm9qZWN0LThjYjFhYjdlLTg5MWMtNDZiNC1iZDM4LWRmMjkwNjBlNTcxNyIsImtleUlkIjoiM2VlODYxOGYtNzliNS00OGQxLTg0MzMtY2M2YzVjODc2ODI1IiwiZXhwIjoxNzkyMjE2NjA0MDAyfQ.urF3esKUJWAKSFMY_pKO7uPqgXaWYqIatpjk7302VoA';
console.log('Navigating to online preview...');
await page.goto(target, { waitUntil: 'networkidle', timeout: 30000 });
await page.waitForTimeout(2000);

// Find start button
const startBtn = page.getByRole('button', { name: /開始遊戲/ });
console.log('Start button visible?', await startBtn.isVisible());
if (await startBtn.isVisible()) {
  await startBtn.click();
  console.log('Clicked start button');
}

await page.waitForTimeout(2500);
console.log('Clicking dialogue box to advance to RPG map...');
await page.locator('.vn2-box').click();
await page.waitForTimeout(4000);

await page.screenshot({ path: '/tmp/online_rpg_screen.png' });
console.log('Screenshot saved to /tmp/online_rpg_screen.png');

await browser.close();
