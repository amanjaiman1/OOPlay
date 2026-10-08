// Render the notebook with headless Chromium.
//   node render.js pdf                      -> ../Java-OOP-Notebook.pdf
//   node render.js shot <page> [out.png]    -> screenshot of one notebook page (for proofing)
const path = require('path');
const fs = require('fs');
const PW = process.env.PW_CORE ||
  '/opt/toolchains/.nvm/versions/node/v22.23.3/lib/node_modules/@playwright/mcp/node_modules/playwright-core';
const { chromium } = require(PW);
const EXE = process.env.CHROME || '/opt/playwright/chromium-1232/chrome-linux64/chrome';
const HTML = 'file://' + path.resolve(__dirname, '..', 'Java-OOP-Notebook.html');

(async () => {
  const [mode, arg, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox', '--font-render-hinting=none'] });
  const page = await browser.newPage({ viewport: { width: 1000, height: 1400 }, deviceScaleFactor: mode === 'shot' ? 1 : 1 });
  await page.goto(HTML, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  if (mode === 'pdf') {
    await page.evaluate(() => document.querySelectorAll('details').forEach(d => (d.open = true)));
    await page.emulateMedia({ media: 'print' });
    const file = path.resolve(__dirname, '..', 'Java-OOP-Notebook.pdf');
    await page.pdf({ path: file, format: 'A4', printBackground: true, preferCSSPageSize: true,
      margin: { top: '0', bottom: '0', left: '0', right: '0' } });
    console.log('wrote', file, (fs.statSync(file).size / 1048576).toFixed(1) + ' MB');
  } else if (mode === 'shot') {
    const el = await page.$(`#page-${arg}`);
    const file = out || `/projects/sandbox/.kiro/artifacts/screenshots/page-${arg}.png`;
    fs.mkdirSync(path.dirname(file), { recursive: true });
    await el.screenshot({ path: file });
    console.log('wrote', file);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
