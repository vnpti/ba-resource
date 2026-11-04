"""Package portable BA sources, exports, and provenance with verified hashes."""
import hashlib
import json
import re
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
paths = [root / 'README.md']
for name in ['docs/anki', 'evidence']:
    paths.extend(p for p in (root / name).rglob('*') if p.is_file())
paths.append(root / 'docs/anki-business-analysis.md')
paths.extend((root / 'plans/reports').glob('*.md'))
paths.extend((root / 'scripts').glob('*.py'))
paths.extend((root / 'scripts').glob('*.mjs'))
paths.append(root / 'plans/2026-11-02-anki-business-analysis/plan.md')
for name in ['plan.md', 'validation.json', 'html-validation.json', 'export-validation.json', 'changed-documents.json']:
    paths.append(root / 'plans/2026-11-03-oracle-ba-refresh' / name)
for suffix in ['html', 'docx', 'pdf']:
    paths.append(root / f'dist/anki-ba-documentation.{suffix}')
paths = sorted(set(paths))
for p in paths:
    if not p.is_file():
        raise FileNotFoundError(p)
qa = json.loads((root / 'docs/anki/test/qa-catalog.json').read_text())
manifest = {
    'package': 'Anki BA documentation', 'version': qa['version'], 'status': 'Draft',
    'date': '2026-11-03', 'source_commit': '136bd42bfbd356fc756b6d3e28cc77b02da11ea7',
    'test_execution': '0/86; all Not Run',
    'design_coverage': qa['coverage'],
    'resolved_oracles': ['AC-ANKI-035', 'AC-ANKI-067', 'AC-ANKI-072', 'AC-ANKI-077'],
    'design_blocked': [a['id'] for a in qa['scenarios'] if a['design_status'] == 'Blocked'],
    'files': [{'path':str(p.relative_to(root)), 'bytes':p.stat().st_size,
               'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
}
(root / 'dist/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
archive = root / 'dist/documentation-bundle.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in paths:
        z.write(p, 'anki-ba-documentation/' + str(p.relative_to(root)))
    z.write(root / 'dist/manifest.json', 'anki-ba-documentation/manifest.json')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for item in manifest['files']:
        assert hashlib.sha256(z.read('anki-ba-documentation/' + item['path'])).hexdigest() == item['sha256']
print(json.dumps({'zip':str(archive),'files':len(paths)+1,'bytes':archive.stat().st_size,'hashes':'all verified'},indent=2))
