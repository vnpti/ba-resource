"""Validate identity, traceability and source locations without claiming runtime results."""
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
base = root / 'docs/anki'
req = json.loads((base / 'srs/requirements.json').read_text())
errors = []
warnings = []
metadata = {}
count_links = 0
source_links = 0
expected = ['id', 'title', 'version', 'phase', 'domain', 'tags', 'depends_on', 'related_diagrams', 'author', 'last_updated', 'status']
sets = {name: {x['id'] for x in req[key]} for name, key in [('FR','requirements'),('BR','rules'),('ERR','errors'),('NFR','nfr')]}
for name, key in [('FR','requirements'),('BR','rules'),('ERR','errors'),('NFR','nfr')]:
    if len(sets[name]) != len(req[key]): errors.append('Duplicate ' + name)
for file in base.rglob('*.md'):
    text = file.read_text()
    fm = re.match(r'^---\n([\s\S]+?)\n---\n', text)
    if not fm:
        errors.append(f'Missing frontmatter: {file.relative_to(base)}'); continue
    data = dict(re.findall(r'(?m)^([\w_]+):\s*(.*)$', fm[1]))
    for key in expected:
        if key not in data: errors.append(f'{file.name}: missing {key}')
    docid = data.get('id', '').strip('"\'')
    if docid in metadata: errors.append(f'Duplicate document ID: {docid}')
    metadata[docid] = file
    if data.get('status', '').strip('"\'') != 'draft': errors.append(f'Not draft: {file}')
    if text.count('```') % 2: errors.append(f'Unclosed fence: {file}')
    for prefix in ['FR', 'BR', 'ERR', 'NFR']:
        pattern = {'FR':r'FR-[A-Z]{2,4}-[A-Z]{2,4}-\d{3}', 'BR':r'BR-ANKI-\d{3}', 'ERR':r'ERR-ANKI-\d{3}-\d{2}', 'NFR':r'NFR-ANKI-\d{3}'}[prefix]
        unknown = set(re.findall(pattern, text)) - sets[prefix]
        if unknown: errors.append(f'{file.name}: undefined {prefix} {sorted(unknown)}')
    for label, url in re.findall(r'\[([^\]\n]+)\]\(([^)\n]+)\)', text):
        if url.startswith('https://github.com/ankitects/anki/blob/'):
            m = re.search(r'/blob/([^/]+)/([^#]+)(?:#L(\d+))?', url)
            if m:
                if m[1] != req['commit']: errors.append(f'Unpinned commit: {url}')
                target = root / 'sources/anki' / unquote(m[2])
                if not target.is_file(): errors.append(f'Missing source: {url}')
                elif m[3] and int(m[3]) > len(target.read_text().splitlines()): errors.append(f'Invalid source line: {url}')
                source_links += 1
        elif not re.match(r'https?:|mailto:|#', url):
            target = (file.parent / unquote(url.split('#')[0])).resolve()
            if not target.exists(): errors.append(f'{file.name}: missing link {url}')
            count_links += 1

for docid, file in metadata.items():
    fm = re.match(r'^---\n([\s\S]+?)\n---\n', file.read_text())[1]
    deps = re.search(r'(?m)^depends_on:\s*\[(.*?)\]', fm)
    if deps:
        for dep in re.findall(r'DOC-[A-Z]+-ANKI-\d{3}', deps[1]):
            if dep not in metadata: errors.append(f'{docid}: missing dependency {dep}')

qa_file = base / 'test/qa-catalog.json'
coverage = {}
if qa_file.exists():
    qa = json.loads(qa_file.read_text())
    for key in ['stories','scenarios','tests']:
        ids = [x['id'] for x in qa[key]]
        if len(ids) != len(set(ids)): errors.append('Duplicate QA IDs: ' + key)
    stories = {s['id']:s for s in qa['stories']}
    scenarios = {s['id']:s for s in qa['scenarios']}
    valid_tests = []
    for t in qa['tests']:
        ac = scenarios.get(t['ac_id'])
        if not ac: errors.append(f'{t["id"]}: missing AC'); continue
        if t['story_id'] != ac['story_id']: errors.append(f'{t["id"]}: wrong story owner')
        if t['status'] != 'Not Run': errors.append(f'{t["id"]}: status not Not Run')
        for key, prefix in [('fr_ids','FR'),('br_ids','BR'),('err_ids','ERR')]:
            if set(t.get(key,[])) - sets[prefix]: errors.append(f'{t["id"]}: undefined {prefix}')
            if set(t.get(key,[])) - set(ac.get(key,[])): errors.append(f'{t["id"]}: {prefix} inconsistent with AC')
        if not t.get('blocked') and t.get('design_status','').lower() not in ('blocked','pending') and not ac.get('blocked') and ac.get('design_status','').lower() not in ('blocked','pending'):
            valid_tests.append(t)
    csv_rows = list(csv.DictReader((base / 'test/traceability.csv').open()))
    if len(csv_rows) != len(qa['tests']): errors.append('CSV test count mismatch')
    tests_by_id = {t['id']: t for t in qa['tests']}
    for row in csv_rows:
        t = tests_by_id.get(row['Test Case ID'])
        if not t: errors.append('Unknown CSV test: ' + row['Test Case ID']); continue
        if (row['AC ID'], row['Design'], row['Trạng thái chạy']) != (t['ac_id'], t['design_status'], t['status']):
            errors.append('CSV status/mapping mismatch: ' + t['id'])
    declared = qa.get('coverage', {})
    for a in qa['scenarios']:
        if a.get('design_status') == 'Specified' and a.get('blocker'):
            errors.append(f'{a["id"]}: Specified still has blocker')
    for s in qa['stories']:
        acs = [a for a in qa['scenarios'] if a['story_id'] == s['id']]
        if set(s.get('ac_ids',[])) != {a['id'] for a in acs}: errors.append(f'{s["id"]}: backlink mismatch')
        if len(acs) < 3: errors.append(f'{s["id"]}: fewer than 3 scenarios')
    for prefix, key in [('FR','fr_ids'),('BR','br_ids'),('ERR','err_ids')]:
        found = {v for t in valid_tests for v in t.get(key,[])}
        coverage[prefix] = {'mapped':len(found), 'total':len(sets[prefix]), 'missing':sorted(sets[prefix] - found)}
    covered_ac = {t['ac_id'] for t in valid_tests}
    coverage['AC'] = {'mapped':len(covered_ac), 'total':len(scenarios), 'missing':sorted(set(scenarios) - covered_ac)}
    for key, value in coverage.items():
        if declared.get(key) != {'covered':value['mapped'], 'total':value['total'], 'missing':value['missing']}:
            errors.append('Declared coverage mismatch: ' + key)
    qa_counts = {k:len(qa[k]) for k in ['stories','scenarios','tests']}
else:
    errors.append('QA catalog not yet present'); qa_counts = {}

result = {'documents':len(metadata),'local_links':count_links,'pinned_source_links':source_links,'catalog':{k:len(v) for k,v in sets.items()},'qa':qa_counts,'computed_coverage':coverage,'errors':errors,'warnings':warnings,'runtime_tests_executed':0}
out = root / 'plans/2026-11-03-oracle-ba-refresh/validation.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors: sys.exit(1)
