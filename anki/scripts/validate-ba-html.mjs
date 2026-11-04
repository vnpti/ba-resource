import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const root = path.resolve(process.argv[2] || '.');
const runtime = process.env.ANKI_BA_RUNTIME || '/Users/ngochoa/.cache/codex-runtimes/codex-primary-runtime/dependencies';
const require = createRequire(path.join(runtime, 'node/package.json'));
const { chromium } = require('playwright');
const browser = await chromium.launch({headless:true, executablePath:process.env.ANKI_BA_CHROMIUM || chromium.executablePath()});
const results = {};
try {
  for (const [name, viewport] of Object.entries({desktop:{width:1440,height:1100},mobile:{width:390,height:844}})) {
    const page = await browser.newPage({viewport});
    await page.goto(pathToFileURL(path.join(root,'dist/anki-ba-documentation.html')).href);
    results[name] = await page.evaluate(() => ({
      articles:document.querySelectorAll('article').length,
      diagrams:document.querySelectorAll('figure svg').length,
      brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(id=>!document.getElementById(id)),
      machineLinks:document.querySelectorAll('a[href*="/Users/"],a[href^="file:"]').length,
      externalScripts:document.querySelectorAll('script[src]').length,
      horizontalOverflow:document.documentElement.scrollWidth>window.innerWidth,
    }));
    await page.screenshot({path:path.join(root,`plans/2026-11-03-oracle-ba-refresh/html-${name}.png`)});
    await page.close();
  }
} finally {await browser.close();}
await fs.writeFile(path.join(root,'plans/2026-11-03-oracle-ba-refresh/html-validation.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify(results,null,2));
if(Object.values(results).some(r=>r.articles!==24||r.diagrams!==6||r.brokenAnchors.length||r.machineLinks||r.externalScripts||r.horizontalOverflow)) process.exitCode=1;
