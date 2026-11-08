"""Write every NashvilleNext Vol IV action to an NN_Vol4_Actions tab, and add Forest-relevant actions
missing from Commitments.

Usage: python nn_vol4_add.py <next-volume4-Actions.pdf> <actions.csv from nn_vol4_parse.py> <commitments_dir> [--write]
(needs pypdf). Each new Commitments excerpt is rechecked against pypdf text of its page with the
"ti"/"tt" ligature glyphs mapped back, or against pdftotext text where pypdf drops a passage. After --write: forest_priorities.py --write, cover_sheet.py.
"""
import csv, re, subprocess, sys
import openpyxl, pypdf
from copy import copy
from openpyxl.styles import Alignment, Font, PatternFill

PDF, ACTIONS, CDIR = sys.argv[1:4]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
DOC = 'NashvilleNext_Vol4_Actions'
URL = 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/NashvilleNext/PlanVolumes/next-volume4-Actions.pdf'

# number, category, metric, note
ADD = [
    (72, 'policy_mechanism', 'LUTI 10 #72 regional assessment of water, sewer and energy infrastructure',
     'Sewer extension drives development of rural Rim land; compare #323 (discourage sewer expansion) and the T2 Rural policies.'),
    (364, 'policy_mechanism', 'LUTI 9.2 #364 update Infrastructure Deficiency Area policy to match character policies',
     'The Infrastructure Deficiency Area policy limits development where roads and utilities are inadequate, which bears on rural and Rim areas.'),
    (375, 'policy_mechanism', 'LUTI 9.2 #375 decision tool weighing environment and climate in infrastructure proposals', None),
    (104, 'green_infrastructure', 'BE 5.2 #104 reduce construction impacts with stormwater best practices', None),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‐': '-', '‑': '-', '’': "'", '‘': "'", '“': '"', '”': '"', '–': '-', '—': '-', 'Ɵ': 'ti', 'Ʃ': 'tt'})
reader = pypdf.PdfReader(PDF)
ptext = {}
def page(p):
    # pypdf text (ligatures mapped) plus pdftotext text: pypdf drops some passages on a few pages.
    if p not in ptext:
        plain = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), PDF, '-'], capture_output=True, text=True).stdout
        ptext[p] = n(reader.pages[p - 1].extract_text().translate(Q)) + ' || ' + n(plain.translate(Q))
    return ptext[p]

actions = list(csv.DictReader(open(ACTIONS, encoding='utf-8')))
for a in actions:
    a['verify'] = 'verified' if n(a['action']) in page(int(a['pdf_page'])) else 'parsed_layout'

wb = openpyxl.load_workbook(XLSX)
cm = wb['Commitments']
in_c = {}
for i, r in enumerate(cm.iter_rows(min_row=2, values_only=True), start=2):
    if r[0] == DOC:
        for m in re.findall(r'#(\d+)', str(r[4])):
            in_c.setdefault(int(m), []).append(i)

new_rows, bad = [], []
by_num = {}
for a in actions:
    by_num.setdefault(int(a['number']), a)
for num, cat, metric, note in ADD:
    a = by_num[num]
    if num in in_c:
        bad.append((num, 'already in Commitments'))
    if a['verify'] != 'verified':
        bad.append((num, 'not verified'))
    new_rows.append([DOC, int(a['pdf_page']), cat, 'recommendation', metric, None, None, a['timeframe'] + {'Near term': ' (1-3 years)', 'Mid-term': ' (4-6 years)', 'Long-term': ' (7-10 years)', 'Ongoing': ''}[a['timeframe']],
                     a['implementers'] or None, a['action'], note, 'verified', URL])
print('actions', len(actions), 'distinct', len(by_num), 'verified', sum(a['verify'] == 'verified' for a in actions), 'new rows', len(new_rows), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

last = max(r for r in range(1, cm.max_row + 1) if cm.cell(r, 1).value is not None)
for k, row in enumerate(new_rows, 1):
    for col in range(1, 14):
        s, d = cm.cell(last, col), cm.cell(last + k, col)
        d.value = row[col - 1]
        d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format
    in_c.setdefault(int(re.search(r'#(\d+)', row[4]).group(1)), []).append(last + k)

COLS = ['number', 'element', 'code', 'policy', 'timeframe', 'implementers', 'action', 'pdf_page', 'verify', 'commitments_rows']
if 'NN_Vol4_Actions' in wb.sheetnames:
    del wb['NN_Vol4_Actions']
ws = wb.create_sheet('NN_Vol4_Actions', wb.sheetnames.index('Commitments') + 1)
ws.append(COLS)
out = []
for a in sorted(actions, key=lambda a: (int(a['number']), a['code'])):
    rows = ', '.join(str(x) for x in in_c.get(int(a['number']), []))
    vals = [int(a['number']), a['element'], a['code'], a['policy'], a['timeframe'], a['implementers'], a['action'], int(a['pdf_page']), a['verify'], rows]
    ws.append(vals)
    out.append(vals)
head = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
for c in ws[1]:
    c.font, c.fill = head, PatternFill('solid', fgColor='FF2F5D3A')
for row in ws.iter_rows(min_row=2):
    for c in row:
        c.font = Font(name='Arial', size=10)
for col, w in zip('ABCDEFGHIJ', (8, 28, 9, 50, 11, 30, 80, 8, 12, 14)):
    ws.column_dimensions[col].width = w
for c in list(ws['D']) + list(ws['G']):
    c.alignment = Alignment(wrap_text=True, vertical='top')
ws.freeze_panes = 'A2'
ws.auto_filter.ref = ws.dimensions
wb.save(XLSX)

with open(f'{CDIR}/nn_vol4_actions.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(COLS)
    w.writerows([['' if v is None else v for v in r] for r in out])
with open(f'{CDIR}/commitments.csv', 'w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows([['' if v is None else v for v in r] for r in cm.iter_rows(values_only=True)])
print('written')
