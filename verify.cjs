// Render through GitHub's Markdown API, then inspect with disposable Chromium.
// The preview stays local; no profile, browser session or contribution data is changed.
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { pathToFileURL } = require('node:url');
const { chromium } = require(path.join(process.env.APPDATA, 'npm/node_modules/openclaw/node_modules/playwright-core'));

(async () => {
  const root = __dirname;
  const readme = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
  for (const match of readme.matchAll(/\]\((assets\/[^)]+)\)/g)) {
    if (!fs.existsSync(path.join(root, match[1]))) throw new Error(`Missing README asset: ${match[1]}`);
  }
  for (const filename of fs.readdirSync(path.join(root, 'assets')).filter(name => name.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(root, 'assets', filename), 'utf8');
    if (/<(?:script|foreignObject|use)\b/i.test(svg) || /(?:href|src)=["'](?:https?:|data:)/i.test(svg)) {
      throw new Error(`Unsafe or externally dependent SVG: ${filename}`);
    }
  }
  let html = execFileSync('gh', ['api', 'markdown', '--input', '-'], {
    input: JSON.stringify({ text: readme, mode: 'gfm', context: 'Murathanx12/Murathanx12' }), encoding: 'utf8',
  });
  // Use the unpushed local copies when the GitHub renderer resolves relative assets.
  for (const filename of fs.readdirSync(path.join(root, 'assets'))) {
    const local = pathToFileURL(path.join(root, 'assets', filename)).href;
    html = html.replaceAll(`src="assets/${filename}"`, `src="${local}"`)
      .replaceAll(`src="https://github.com/Murathanx12/Murathanx12/raw/refs/heads/main/assets/${filename}"`, `src="${local}"`)
      .replaceAll(`src="https://github.com/Murathanx12/Murathanx12/raw/main/assets/${filename}"`, `src="${local}"`);
  }
  fs.mkdirSync(path.join(root, 'validation'), { recursive: true });
  const preview = path.join(root, 'validation/profile.html');
  fs.writeFileSync(preview, `<!doctype html><html><head><meta charset="UTF-8"><style>
  *{box-sizing:border-box}body{background:#0d1117;color:#e6edf3;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;padding:32px}
  main{max-width:896px;margin:auto;padding:32px;border:1px solid #30363d;border-radius:6px}h1{font-size:30px;line-height:1.3;border-bottom:1px solid #30363d;padding-bottom:14px}h3{font-size:20px;margin:30px 0 12px}p{margin:0 0 16px}img{max-width:100%;height:auto}a{color:#58a6ff;text-decoration:none}table{width:100%;border-collapse:collapse}td{padding:16px;border:1px solid #30363d}td h3{margin-top:0}sub{font-size:12px}svg{max-width:100%}@media(max-width:600px){body{padding:12px}main{padding:16px}h1{font-size:25px}td{padding:10px}h3{font-size:19px}}
  </style></head><body><main>${html}</main></body></html>`);
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  try {
    for (const [name, width] of [['desktop', 1280], ['mobile', 390]]) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(pathToFileURL(preview).href);
      await page.waitForTimeout(2200);
      const result = await page.evaluate(() => ({
        scrollWidth: document.documentElement.scrollWidth, viewport: innerWidth,
        images: [...document.images].map(image => ({ src: image.getAttribute('src'), complete: image.complete, width: image.naturalWidth })),
        projects: [...document.querySelectorAll('h3')].map(heading => heading.textContent),
      }));
      if (result.scrollWidth > width || errors.length || result.images.some(image => !image.complete || !image.width)) {
        throw new Error(JSON.stringify({ name, errors, ...result }));
      }
      await page.screenshot({ path: path.join(root, `validation/${name}.png`), fullPage: true });
      console.log(JSON.stringify({ name, errors, ...result }));
      await page.close();
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
