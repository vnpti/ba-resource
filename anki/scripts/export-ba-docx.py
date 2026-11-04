"""Build the reviewable Word edition from the same token stream as the HTML."""
import json
import os
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
DOCS = json.loads((ROOT / 'plans/2026-11-03-oracle-ba-refresh/export-content.json').read_text())
OUT = ROOT / 'dist/anki-ba-documentation.docx'
BUNDLE_VERSION = DOCS[0]['meta']['version']
BUNDLE_DATE = '/'.join(reversed(DOCS[0]['meta']['last_updated'].split('-')))
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)
sec.top_margin, sec.bottom_margin = Inches(.7), Inches(.65)
sec.left_margin, sec.right_margin = Inches(.7), Inches(.7)
WIDTH = 6.87
for name in ['Normal', 'Title', 'Subtitle', 'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4']:
    st = doc.styles[name]
    st.font.name = 'Arial'
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.font.size = Pt({'Title': 28, 'Heading 1': 21, 'Heading 2': 15, 'Heading 3': 12, 'Heading 4': 11}.get(name, 10))
    st.paragraph_format.space_after = Pt(7)
    st.paragraph_format.line_spacing = 1.12
    if name.startswith('Heading'):
        st.paragraph_format.space_before = Pt(12)
        st.paragraph_format.keep_with_next = True
for style in doc.styles:
    if style.type == 1:
        for border in style.element.xpath('./w:pPr/w:pBdr'):
            border.getparent().remove(border)
doc.core_properties.title = 'Bộ tài liệu nghiệp vụ Anki'
doc.core_properties.subject = 'Đặc tả As-Is và thiết kế kiểm thử'
doc.core_properties.author = 'BA Analysis'
doc.core_properties.keywords = 'Anki, BA, SRS, Draft, As-Is'


def field(paragraph, code):
    f = OxmlElement('w:fldSimple')
    f.set(qn('w:instr'), code)
    paragraph._p.append(f)


footer = sec.footer.paragraphs[0]
footer.alignment = 2
footer.add_run(f'Anki BA {BUNDLE_VERSION} · Draft | ').font.size = Pt(8)
field(footer, 'PAGE')


def bookmark(p, name, num):
    a = OxmlElement('w:bookmarkStart'); a.set(qn('w:id'), str(num)); a.set(qn('w:name'), name)
    b = OxmlElement('w:bookmarkEnd'); b.set(qn('w:id'), str(num))
    p._p.insert(0, a); p._p.append(b)


def hyperlink(p, text, href=None, anchor=None):
    h = OxmlElement('w:hyperlink')
    if anchor:
        h.set(qn('w:anchor'), anchor)
    else:
        rel = p.part.relate_to(href, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
        h.set(qn('r:id'), rel)
    r = OxmlElement('w:r'); pr = OxmlElement('w:rPr')
    color = OxmlElement('w:color'); color.set(qn('w:val'), '245B79'); pr.append(color)
    r.append(pr); t = OxmlElement('w:t'); t.text = text; r.append(t); h.append(r); p._p.append(h)


paths = {str((ROOT / 'docs/anki' / d['rel']).resolve()): f'doc_{i}' for i, d in enumerate(DOCS)}
current = None


def plain(tokens):
    return ''.join(plain(t.get('tokens', [])) if t.get('tokens') else t.get('text', t.get('raw', '')) for t in tokens)


def inline(p, tokens, bold=False, italic=False):
    for t in tokens:
        kind = t['type']
        if kind == 'link':
            href = t['href']; label = plain(t.get('tokens', [])) or t.get('text', '')
            if not re.match(r'https?:|mailto:', href):
                path = str(((ROOT / 'docs/anki' / current['rel']).parent / href.split('#')[0]).resolve())
                if path in paths:
                    hyperlink(p, label, anchor=paths[path]); continue
                if path.startswith(str(ROOT) + '/'):
                    href = os.path.relpath(path, ROOT / 'dist')
            hyperlink(p, label, href=href)
        elif kind in ('strong', 'em'):
            inline(p, t['tokens'], bold or kind == 'strong', italic or kind == 'em')
        elif t.get('tokens'):
            inline(p, t['tokens'], bold, italic)
        else:
            text = t.get('text', '') if kind != 'br' else '\n'
            if kind == 'html':
                text = re.sub('<[^>]+>', '', text).replace('&lt;', '<').replace('&gt;', '>')
            run = p.add_run(text); run.bold = bold; run.italic = italic
            if kind == 'codespan':
                run.font.name = 'Arial'; run.font.size = Pt(9)


def paragraph(tokens, style=None):
    p = doc.add_paragraph(style=style)
    inline(p, tokens)
    if tokens and all(t['type'] == 'strong' for t in tokens):
        p.paragraph_format.keep_with_next = True
    return p


def table(t):
    headers = [plain(c.get('tokens', [])) for c in t['header']]
    rows = t['rows']; count = len(headers)
    long_table = count > 5 or any(sum(len(plain(c.get('tokens', []))) for c in row) > 900 for row in rows)
    if long_table:
        # Wide requirement/test matrices become labeled records in print, preserving every cell.
        for row in rows:
            p = doc.add_paragraph(); inline(p, row[0].get('tokens', []), bold=True)
            p.paragraph_format.keep_with_next = True
            for cell_index, (h, cell) in enumerate(zip(headers[1:], row[1:])):
                p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.keep_with_next = cell_index < len(row) - 2
                p.add_run(h + ': ').bold = True; inline(p, cell.get('tokens', []))
        return
    tab = doc.add_table(rows=1, cols=count)
    tab.alignment = WD_TABLE_ALIGNMENT.CENTER; tab.autofit = False
    weights = [max(10, min(45, len(headers[i]) + sum(min(len(plain(row[i].get('tokens', []))), 100) for row in rows) / max(len(rows), 1) / 3)) for i in range(count)]
    widths = [WIDTH * x / sum(weights) for x in weights]
    for i, w in enumerate(widths):
        tab.columns[i].width = Inches(w)
    for index, row in enumerate([t['header']] + rows):
        cells = tab.rows[0].cells if index == 0 else tab.add_row().cells
        for i, (c, token) in enumerate(zip(cells, row)):
            c.width = Inches(widths[i]); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr = c._tc.get_or_add_tcPr()
            shade = OxmlElement('w:shd'); shade.set(qn('w:fill'), 'DDE9F0' if index == 0 else ('F5F8FA' if index % 2 == 0 else 'FFFFFF')); tcpr.append(shade)
            borders = OxmlElement('w:tcBorders')
            for edge in ['top', 'left', 'bottom', 'right']:
                el = OxmlElement('w:' + edge); el.set(qn('w:val'), 'single'); el.set(qn('w:sz'), '4'); el.set(qn('w:color'), 'D9D9D9'); borders.append(el)
            tcpr.append(borders)
            margins = OxmlElement('w:tcMar')
            for edge in ['top', 'left', 'bottom', 'right']:
                el = OxmlElement('w:' + edge); el.set(qn('w:w'), '85'); el.set(qn('w:type'), 'dxa'); margins.append(el)
            tcpr.append(margins)
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(3); p.paragraph_format.space_before = Pt(3)
            inline(p, token.get('tokens', []), bold=index == 0)
            for run in p.runs:
                run.font.size = Pt(9)
        tab.rows[index]._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        if index == 0:
            prop = tab.rows[0]._tr.get_or_add_trPr(); prop.append(OxmlElement('w:tblHeader'))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def blocks(tokens, diagram_iter):
    for t in tokens:
        kind = t['type']
        if kind == 'heading':
            if t['depth'] == 1:
                continue
            p = doc.add_paragraph(style=f'Heading {min(t["depth"], 4)}'); inline(p, t['tokens'])
        elif kind in ('paragraph', 'text'):
            paragraph(t.get('tokens', [{'type': 'text', 'text': t.get('text', '')}]))
        elif kind == 'list':
            for i, item in enumerate(t['items']):
                p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(.15)
                p.add_run(f'{i + 1}. ' if t.get('ordered') else '• ')
                for subt in item['tokens']:
                    if subt['type'] in ('text', 'paragraph'):
                        inline(p, subt.get('tokens', [{'type': 'text', 'text': subt.get('text', '')}]))
                    elif subt['type'] == 'list':
                        blocks([subt], diagram_iter)
        elif kind == 'table':
            table(t)
        elif kind == 'code' and t.get('lang') == 'mermaid':
            d = next(diagram_iter); img = Image.open(d['png']); width, height = img.size
            w = min(WIDTH, 8.1 * width / height)
            p = doc.add_paragraph(); p.alignment = 1
            run = p.add_run(); run.add_picture(d['png'], width=Inches(w))
            for prop in run._r.xpath('.//wp:docPr'):
                prop.set('descr', 'Sơ đồ nghiệp vụ ' + d['name'])
            p = doc.add_paragraph('Sơ đồ ' + d['name'].replace('diagram-', '')); p.alignment = 1
        elif kind == 'code':
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(.15)
            r = p.add_run(t['text']); r.font.name = 'Arial'; r.font.size = Pt(9)
        elif kind == 'blockquote':
            blocks(t['tokens'], diagram_iter)


doc.add_paragraph('Bộ tài liệu nghiệp vụ Anki', 'Title')
doc.add_paragraph('Đặc tả hệ thống hiện có và thiết kế kiểm thử', 'Subtitle')
doc.add_paragraph(f'Phiên bản bộ {BUNDLE_VERSION} · Ngày {BUNDLE_DATE} · Draft để thẩm định')
doc.add_paragraph('Bộ tài liệu nối mục tiêu nghiệp vụ với đặc tả, mô hình dữ liệu, hành trình người dùng và các kịch bản kiểm thử. Nội dung tái lập từ cùng một snapshot Anki Desktop; các mục chưa xác nhận có owner và phương pháp thẩm định. Test case chưa thực thi giữ trạng thái Not Run.')
doc.add_paragraph('Source commit 136bd42bfbd356fc756b6d3e28cc77b02da11ea7')
doc.add_paragraph('Tài liệu phục vụ Product Owner, BA, đội phát triển và QA. Các ma trận nhiều cột được trình bày thành bản ghi có nhãn trong bản Word/PDF để giữ đầy đủ nội dung và khả năng đọc.')
doc.add_page_break()
doc.add_paragraph('Mục lục', 'Heading 1')
doc.add_paragraph('Mục lục được tạo tự động từ danh mục tài liệu. Chọn tên tài liệu để chuyển tới nội dung.')
for i, d in enumerate(DOCS):
    p = doc.add_paragraph(); p.add_run(f'{i + 1:02}. '); hyperlink(p, d['meta']['title'], anchor=f'doc_{i}')
for i, current in enumerate(DOCS):
    p = doc.add_paragraph(current['meta']['title'], 'Heading 1'); p.paragraph_format.page_break_before = True
    bookmark(p, f'doc_{i}', i + 1)
    p = doc.add_paragraph(f"{current['meta']['id']} · {current['meta']['version']} · Draft")
    p.paragraph_format.space_after = Pt(10)
    blocks(current['tokens'], iter(current['diagrams']))
doc.save(OUT)
print(OUT)
