"""Append the staged 2013 UFPP rows from docs/research/UFPP-2013-FLOOD-PLAN.md to the workbook and CSVs.

Usage: python3 ufpp2013_add.py <repo_root> [--write]
Rechecks every excerpt against pdftotext of its stated page in docs/research/sources/UFPP_2013_Final_Report.pdf
and exits without writing on any miss.
"""
import csv, io, re, subprocess, sys
import openpyxl
from copy import copy

ROOT = sys.argv[1]
MD = f'{ROOT}/docs/research/UFPP-2013-FLOOD-PLAN.md'
PDF = f'{ROOT}/docs/research/sources/UFPP_2013_Final_Report.pdf'
CDIR = f'{ROOT}/docs/research/commitments'
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'

blocks = re.findall(r'```csv\n(.*?)```', open(MD, encoding='utf-8').read(), re.S)
commit, hr, src = (list(csv.reader(io.StringIO(b))) for b in blocks)
assert len(commit) == 8 and len(hr) == 1 and len(src) == 1, (len(commit), len(hr), len(src))
assert all(len(r) == 13 for r in commit) and len(hr[0]) == 12 and len(src[0]) == 7

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
QUOTES = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', 'ﬁ': 'fi', 'ﬂ': 'fl'})
page = lambda p: n(subprocess.run(['pdftotext', '-f', p, '-l', p, PDF, '-'], capture_output=True, text=True).stdout.translate(QUOTES))
bad = [(r[1], r[4]) for r in commit + hr if n(r[9].translate(QUOTES)) not in page(r[1])]
print('rows', len(commit), len(hr), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

def num(v):
    return int(v) if re.fullmatch(r'\d+', v or '') else (v if v != '' else None)

wb = openpyxl.load_workbook(XLSX)
assert src[0][0] not in {r[0] for r in wb['Sources'].iter_rows(min_row=2, values_only=True)}, 'source already present'

def append(ws, rows, width):
    last = ws.max_row
    for r in rows:
        ws.append([num(v) for v in r])
        for col in range(1, width + 1):
            s, d = ws.cell(last, col), ws.cell(ws.max_row, col)
            d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format

append(wb['Commitments'], commit, 13)
append(wb['Highland Rim & named places'], hr, 12)

# Sources: insert before Total; the staged COUNTIF row number is recomputed for where Total actually sits
ws = wb['Sources']
total_r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'Total')
tail = [[(c.value, c._style) for c in ws[r]] for r in range(total_r, ws.max_row + 1)]
style = [c._style for c in ws[total_r - 1]]
row = [num(v) for v in src[0][:6]] + [f'=COUNTIF(Commitments!$A:$A,A{total_r})']
for col, v in enumerate(row, 1):
    ws.cell(total_r, col).value = v
    ws.cell(total_r, col)._style = copy(style[col - 1])
for i, cells in enumerate(tail):
    for col, (v, st) in enumerate(cells, 1):
        c = ws.cell(total_r + 1 + i, col)
        c.value, c._style = v, copy(st)
ws.cell(total_r + 1, 7).value = f'=SUM(G2:G{total_r})'
wb.save(XLSX)

def dump(name, path, skip_blank):
    rows = [['' if v is None else v for v in r] for r in wb[name].iter_rows(values_only=True)]
    if skip_blank:
        rows = [r for r in rows if any(x != '' for x in r)]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
dump('Commitments', f'{CDIR}/commitments.csv', False)
dump('Highland Rim & named places', f'{CDIR}/highland_rim.csv', False)
dump('Sources', f'{CDIR}/sources.csv', True)
print('written; Total now =SUM(G2:G%d)' % total_r)
