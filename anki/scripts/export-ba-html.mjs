import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

const root = path.resolve(process.argv[2] || '.');
const runtime = process.env.ANKI_BA_RUNTIME || '/Users/ngochoa/.cache/codex-runtimes/codex-primary-runtime/dependencies';
const require = createRequire(path.join(runtime, 'node/package.json'));
const { marked } = require('marked');
const { chromium } = require('playwright');
const sharp = require('sharp');
const base = path.join(root, 'docs/anki');
const out = path.join(root, 'dist');
const assets = path.join(base, 'diagrams/rendered');
await fs.mkdir(assets, { recursive: true });
await fs.mkdir(out, { recursive: true });
const ordered = [
  '00-index.md', '06-brd.md', '01-prd.md', '05-urd.md',
  'srs/spec.md', 'srs/code-derived-spec.md', 'srs/erd.md', 'srs/states.md',
  'diagrams/flows.md',
  ...Array.from({ length: 10 }, (_, i) => `usecases/UC-ANKI-${String(i + 1).padStart(3, '0')}.md`),
  'userstories/backlog.md', 'userstories/acceptance-criteria.md', 'test/test-cases.md',
  'governance/evidence-and-scope.md', 'governance/decisions-and-handoff.md',
];
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const slug = (s) => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const docs = [];
for (const rel of ordered) {
  const raw = await fs.readFile(path.join(base, rel), 'utf8');
  const fm = raw.match(/^---\n([\s\S]*?)\n---\n/);
  if (!fm) throw Error(`Missing metadata: ${rel}`);
  const meta = {};
  for (const line of fm[1].split('\n')) {
    const pair = line.match(/^([\w_]+):\s*(.*)$/);
    if (pair) meta[pair[1]] = pair[2].replace(/^["']|["']$/g, '');
  }
  docs.push({ rel, meta, anchor: slug(meta.id), markdown: raw.slice(fm[0].length), diagrams: [] });
}
const byPath = new Map(docs.map(d => [path.resolve(base, d.rel), d]));
const browser = await chromium.launch({ headless: true, executablePath: process.env.ANKI_BA_CHROMIUM || chromium.executablePath() });
let diagramNumber = 0;
try {
  const page = await browser.newPage({ viewport: { width: 1500, height: 1100 }, deviceScaleFactor: 2 });
  await page.setContent('<html><body style="margin:20px;background:white"></body></html>');
  let mermaidReady = false;
  async function initMermaid() {
    if (mermaidReady) return;
  await page.addScriptTag({ path: process.env.ANKI_MERMAID_SCRIPT || '/tmp/anki-ba-render/mermaid.min.js' });
  await page.evaluate(() => mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base', themeVariables: { fontFamily: 'Arial', fontSize: '18px', primaryColor: '#e8f0f5', primaryTextColor: '#152536', primaryBorderColor: '#829bae', lineColor: '#566d7b' }, flowchart: { htmlLabels: false, useMaxWidth: false }, sequence: { useMaxWidth: false }, er: { useMaxWidth: false } }));
    mermaidReady = true;
  }
  for (const doc of docs) {
    const matches = [...doc.markdown.matchAll(/```mermaid\s*\n([\s\S]*?)```/g)];
    for (const match of matches) {
      diagramNumber++;
      const name = `diagram-${String(diagramNumber).padStart(2, '0')}`;
      const source = match[1];
      if (process.env.ANKI_BA_REUSE_DIAGRAMS === '1') {
        const cachedSource = await fs.readFile(path.join(assets, `${name}.mmd`), 'utf8').catch(() => null);
        if (cachedSource === source) {
          const svg = await fs.readFile(path.join(assets, `${name}.svg`), 'utf8');
          await fs.access(path.join(assets, `${name}.png`));
          doc.diagrams.push({ name, source, svg, png: path.join(assets, `${name}.png`) });
          continue;
        }
      }
      await initMermaid();
      const svg = await page.evaluate(async ({ id, source }) => {
        await mermaid.parse(source);
        const result = (await mermaid.render(id, source)).svg;
        // ER labels inherit the same fill for background and text in Mermaid's base theme.
        const labelStyle = `#${id} .edgeLabel rect{fill:#ffffff!important}#${id} .edgeLabel text,#${id} .edgeLabel tspan{fill:#152536!important}`;
        return result.replace('</style>', labelStyle + '</style>');
      }, { id: name, source });
      await fs.writeFile(path.join(assets, `${name}.svg`), svg);
      await fs.writeFile(path.join(assets, `${name}.mmd`), source);
      // Browser rasterization preserves SVG foreignObject labels as well as native SVG text.
      await page.evaluate(svg => { document.body.innerHTML = svg; const el = document.querySelector('svg'); el.style.maxWidth = '1400px'; el.style.height = 'auto'; }, svg);
      const target = page.locator('svg').first();
      const rawPng = await target.screenshot();
      await sharp(rawPng).png().toFile(path.join(assets, `${name}.png`));
      doc.diagrams.push({ name, source, svg, png: path.join(assets, `${name}.png`) });
    }
  }
} finally {
  await browser.close();
}

function resolveLink(doc, href) {
  if (/^https?:|^mailto:/.test(href)) return href;
  const [file, hash] = href.split('#');
  const full = file ? path.resolve(path.dirname(path.join(base, doc.rel)), decodeURI(file)) : path.join(base, doc.rel);
  const hit = byPath.get(full);
  if (hit) return `#${hit.anchor}${hash ? '--' + hash : ''}`;
  const prefix = path.join(root, 'sources/anki') + '/';
  if (full.startsWith(prefix)) {
    return 'https://github.com/ankitects/anki/blob/136bd42bfbd356fc756b6d3e28cc77b02da11ea7/' + full.slice(prefix.length).replace(/:(\d+)$/, '#L$1');
  }
  if (full.startsWith(root + '/')) return path.relative(out, full) + (hash ? '#' + hash : '');
  return href;
}
const fragments = [];
for (const doc of docs) {
  let idx = 0;
  const renderer = new marked.Renderer();
  renderer.heading = function(token) {
    const inner = this.parser.parseInline(token.tokens);
    return `<h${Math.min(token.depth + 1, 6)} id="${doc.anchor}--${slug(token.text)}">${inner}</h${Math.min(token.depth + 1, 6)}>`;
  };
  renderer.link = function(token) {
    return `<a href="${esc(resolveLink(doc, token.href))}">${this.parser.parseInline(token.tokens)}</a>`;
  };
  renderer.code = function(token) {
    if (token.lang === 'mermaid') {
      const diagram = doc.diagrams[idx++];
      return `<figure>${diagram.svg}<figcaption>Sơ đồ ${diagram.name.replace('diagram-', '')}</figcaption></figure><details><summary>Mã Mermaid</summary><pre>${esc(token.text)}</pre></details>`;
    }
    return `<pre><code>${esc(token.text)}</code></pre>`;
  };
  doc.tokens = marked.lexer(doc.markdown);
  doc.html = marked.parse(doc.markdown, { renderer, gfm: true });
  fragments.push(`<article id="${doc.anchor}"><div class="doc-meta">${esc(doc.meta.id)} · ${esc(doc.meta.version)} · DRAFT</div>${doc.html}</article>`);
}
const bundleVersion = docs[0].meta.version;
const bundleDate = docs[0].meta.last_updated.split('-').reverse().join('/');
const nav = docs.map((d, i) => `<a href="#${d.anchor}"><span>${String(i + 1).padStart(2, '0')}</span>${esc(d.meta.title)}</a>`).join('');
let html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bộ tài liệu BA Anki</title><style>
:root{--ink:#162737;--muted:#536774;--line:#d5dee5;--paper:#fff;--accent:#1e526f}*{box-sizing:border-box}body{overflow-wrap:anywhere;margin:0;background:#eef2f5;color:var(--ink);font:16px/1.65 system-ui,-apple-system,Arial,sans-serif}nav{position:fixed;inset:0 auto 0 0;width:285px;padding:26px 18px;background:#122b3c;color:white;overflow:auto}nav strong{font-size:23px;display:block;margin:0 10px 10px}nav small{display:block;color:#b8cbd7;margin:0 10px 22px}nav a{display:flex;gap:12px;color:#e1ebf1;text-decoration:none;padding:9px;border-radius:5px;font-size:13px;line-height:1.4}nav a:hover{background:#234456}nav span{flex-shrink:0;min-width:20px;white-space:nowrap;color:#8aafc3;font-variant-numeric:tabular-nums}main{margin-left:285px;padding:42px;max-width:1500px}.cover{background:white;padding:44px 48px;border-top:5px solid var(--accent);margin-bottom:26px}.eyebrow{color:var(--accent);font-size:12px;letter-spacing:2px;font-weight:700}h1{font-size:42px;line-height:1.15;letter-spacing:-1px;margin:16px 0}h2{font-size:30px;line-height:1.3;margin:12px 0 25px}h3{font-size:22px;margin:35px 0 14px}h4{font-size:18px;margin:25px 0 12px}article{background:white;margin-bottom:26px;padding:38px 44px;scroll-margin-top:20px}.doc-meta{color:var(--muted);font-size:12px;letter-spacing:.5px}p{margin:14px 0}a{color:#17608a;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;font-size:13px;display:block;overflow:auto;margin:20px 0}th,td{padding:10px 12px;border:1px solid var(--line);vertical-align:top;min-width:85px}th{background:#dfeaf1;text-align:left}tr:nth-child(even) td{background:#f7f9fb}code{font:12px/1.5 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f8;padding:18px;font:12px/1.6 ui-monospace,Menlo,monospace}figure{margin:24px 0;text-align:center;overflow:auto}figure svg{max-width:100%;height:auto}figcaption,details{color:var(--muted);font-size:12px}blockquote{margin:20px 0;color:var(--muted)}li{margin:7px 0}hr{border:0;border-top:1px solid var(--line);margin:28px 0}.cover p{max-width:800px}.status{font-size:13px;color:var(--muted)}@media(max-width:900px){nav{position:static;width:auto;max-height:320px}main{margin:0;padding:15px}article,.cover{padding:24px}h1{font-size:32px}}@media print{nav{display:none}main{margin:0;padding:0;max-width:none}article{page-break-before:always;padding:0}body{background:white;font-size:10pt}table{display:table;font-size:8pt}pre{font-size:8pt}.cover{border:0}details{display:none}a{color:inherit}figure{break-inside:avoid}}
</style></head><body><nav><strong>Anki BA</strong><small>As-Is · ${esc(bundleVersion)} · ${esc(bundleDate)}</small>${nav}</nav><main><header class="cover"><div class="eyebrow">BUSINESS ANALYSIS DOSSIER</div><h1>Bộ tài liệu nghiệp vụ Anki</h1><p>Yêu cầu kinh doanh, đặc tả hệ thống, mô hình dữ liệu và thiết kế kiểm thử được truy vết tới cùng một snapshot mã nguồn.</p><p class="status">Draft để thẩm định · Source 136bd42bfbd35 · Test chưa thực thi<br>HTML hoạt động offline; liên kết tới nguồn GitHub cần kết nối mạng.</p></header>${fragments.join('\n')}</main></body></html>`;
// Markdown heading fragments vary by renderer; retain a working document-level target.
const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]));
html = html.replace(/href="#([^"]+)"/g, (whole, id) => ids.has(id) ? whole : (ids.has(id.split('--')[0]) ? `href="#${id.split('--')[0]}"` : whole));
await fs.writeFile(path.join(out, 'anki-ba-documentation.html'), html);
await fs.writeFile(path.join(root, 'plans/2026-11-03-oracle-ba-refresh/export-content.json'), JSON.stringify(docs.map(({ html, ...d }) => d)));
console.log(JSON.stringify({ documents: docs.length, diagrams: diagramNumber, html: path.join(out, 'anki-ba-documentation.html') }));
