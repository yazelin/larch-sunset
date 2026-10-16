import { chromium } from '/home/ct/larch-preview/node_modules/playwright-core/index.mjs';
import { spawn } from 'node:child_process';

const server = spawn('python3', ['/home/ct/larch-preview/serve.py', '/home/ct/larch-sunset/dist/project.json', '--port', '0']);
let base = null;
server.stdout.on('data', d => {
  const m = d.toString().match(/預覽：(http:\/\/127\.0\.0\.1:\d+)/);
  if (m) base = m[1];
});
while (!base) await new Promise(r => setTimeout(r, 100));
console.log('Testing walk on', base);

const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome' });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

try {
  await page.goto(base + '/');
  await page.waitForTimeout(2000);

  const frame = page.frameLocator('#player');
  const startBtn = frame.getByRole('button', { name: /開始遊戲/ });
  if (await startBtn.isVisible()) {
    await startBtn.click();
    console.log('Clicked start button');
  }

  await page.waitForTimeout(2500);
  console.log('Advancing prologue...');
  await frame.locator('.vn2-box').click();
  await page.waitForTimeout(3000);

  // Find the RPG child frame and focus its canvas
  const playerFrame = page.frame({ url: /play\/market/ });
  const rpgFrame = playerFrame.childFrames()[0];
  console.log('RPG frame found?', !!rpgFrame);
  if (rpgFrame) {
    const canvas = rpgFrame.locator('canvas[role="application"]');
    await canvas.focus();
    console.log('Canvas focused');

    // Press 'a' or Enter to interact with note
    console.log('Interacting with note via Enter...');
    await canvas.press('Enter');
    await page.waitForTimeout(1000);

    // Click dialogue to advance
    const dlg = rpgFrame.locator('#dialogue');
    for (let i = 0; i < 5; i++) {
      if (await dlg.isVisible()) {
        await dlg.click();
        await page.waitForTimeout(600);
      }
    }

    // Now test moving right towards spoon
    console.log('Moving right...');
    for (let i = 0; i < 4; i++) {
      await canvas.press('ArrowRight');
      await page.waitForTimeout(150);
    }
    await page.waitForTimeout(1000);
    const status = await rpgFrame.locator('#status').textContent();
    console.log('Status after moving right:', status);
    await page.screenshot({ path: '/tmp/test_moved_right.png' });
  }

} finally {
  await browser.close();
  server.kill();
}
