import { chromium } from '/home/ct/larch-preview/node_modules/playwright-core/index.mjs';
import { spawn } from 'node:child_process';

const server = spawn('python3', ['/home/ct/larch-preview/serve.py', '/home/ct/larch-sunset/dist/project.json', '--port', '0']);
let base = null;
server.stdout.on('data', d => {
  const m = d.toString().match(/預覽：(http:\/\/127\.0\.0\.1:\d+)/);
  if (m) base = m[1];
});
while (!base) await new Promise(r => setTimeout(r, 100));
console.log('Testing on', base);

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
  console.log('Start button visible?', await startBtn.isVisible());
  if (await startBtn.isVisible()) {
    await startBtn.click();
    console.log('Clicked start button');
  }

  await page.waitForTimeout(2500);
  const textEl = frame.locator('.vn2-text');
  console.log('Text content after start:', await textEl.textContent().catch(() => 'no text'));

  // Click text box to advance to m-bar
  console.log('Clicking text box to advance...');
  await frame.locator('.vn2-box').click();
  await page.waitForTimeout(4000);

  // Check inner iframes or canvas inside #player
  const playerFrame = page.frame({ url: /play\/market/ });
  if (playerFrame) {
    console.log('Player frame URL:', playerFrame.url());
    const childFrames = playerFrame.childFrames();
    console.log('Player child frames count:', childFrames.length);
    for (const cf of childFrames) {
      console.log('Child frame URL:', cf.url());
      const statusText = await cf.locator('#status').textContent().catch(e => e.message);
      console.log('Child frame #status:', statusText);
      const loaderTip = await cf.locator('#loader-tip').textContent().catch(e => e.message);
      console.log('Child frame #loader-tip:', loaderTip);
    }
  }

  await page.screenshot({ path: '/tmp/test_sunset.png' });
  console.log('Saved screenshot to /tmp/test_sunset.png');
  console.log('Recent logs:');
  console.log(logs.slice(-30).join('\n'));
} finally {
  await browser.close();
  server.kill();
}
