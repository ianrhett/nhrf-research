"""Add Planning Commission minutes on the Whites Creek rural policies (2015-2016) as sources with rows.

Usage: python3 wc_minutes_add.py <pdf_dir> <commitments_dir> [--write]
pdf_dir holds 150622m.pdf, 160428m.pdf and 160526m.pdf, byte-identical to the URLs below (checked
2026-10-22). Found by a research pass over 2015-2016 MPC minutes and videos (WHITES-CREEK-HEARINGS.md).
Every excerpt is rechecked against its page; the script exits without writing on any miss or duplicate.
After --write: apply_pvd_to_xlsx.py, forest_priorities.py --write, cover_sheet.py.
"""
import csv, re, subprocess, sys
import openpyxl
from copy import copy

PDF_DIR, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
M15, M16A, M16B = 'MPC_Minutes_2015-06-22', 'MPC_Minutes_2016-04-28', 'MPC_Minutes_2016-05-26'
FILE = {M15: '150622m.pdf', M16A: '160428m.pdf', M16B: '160526m.pdf'}
URL = {k: 'https://www.nashville.gov/sites/default/files/2021-09/' + v for k, v in FILE.items()}
SOURCES = [
    [M15, 'Metropolitan Planning Commission Minutes, June 22, 2015 (NashvilleNext adoption; Whites Creek and Scottsboro/Bells Bend amendments)', 'June 22, 2015', 'Final minutes', None, URL[M15]],
    [M16A, 'Metropolitan Planning Commission Minutes, April 28, 2016 (Rural Character Subdivision Regulations, 2015S-001R-001)', 'April 28, 2016', 'Final minutes', None, URL[M16A]],
    [M16B, 'Metropolitan Planning Commission Minutes, May 26, 2016 (Whites Creek deferred areas, 2015CP-000-002)', 'May 26, 2016', 'Final minutes', None, URL[M16B]],
]

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (M15, 26, 'highland_rim_named_place', 'status_claim', 'Commissioner: rural is the appropriate policy for Whites Creek, a community compromise', None, None, '2015', 'Metro Planning Commission',
     "Ms. LeQuire noted that rural is the appropriate policy designation for Whites Creek and that the policy, as presented in the Static Draft, represents a compromise reached by the community.", None),
    (M15, 29, 'highland_rim_named_place', 'status_claim', 'Motion to adopt the Whites Creek rural policies as drafted failed', None, None, '2015', 'Metro Planning Commission',
     "A vote was taken on Ms. LeQuire's motion to adopt the plan as presented in the Static Draft. (1-6-2)",
     'The 11 Whites Creek areas were then deferred to August 13, 2015 (5-4, same page). NashvilleNext was adopted that day without them.'),
    (M15, 30, 'highland_rim_named_place', 'definition', 'Conservation subdivisions excluded from Scottsboro/Bells Bend', None, None, '2015', 'Metro Planning Commission',
     'This amendment would preclude the use of Conservation Subdivisions from the Scottsboro/Bells Bend study area.',
     'Approved 9-0. The community feared conservation subdivisions would add density; compare BL2006-1046 and pair 22.'),
    (M16A, 16, 'policy_mechanism', 'status_claim', 'Rural Character Subdivision Regulations adopted (RS2016-104)', None, None, '2016', 'Metro Planning Commission',
     'Resolution No. RS2016-104 "BE IT RESOLVED by The Metropolitan Planning Commission that 2015S-001R-001 is Approved. (9-0)"',
     'Replaces conservation subdivisions in the Subdivision Regulations with Rural Character Subdivisions for T2 Rural Neighborhood policy areas. Bears on pair 24 (#323).'),
    (M16A, 12, 'forest_protection', 'definition', 'Subdivisions in T2 Rural Neighborhood areas must be Rural Character Subdivisions', None, None, None, 'Metro Planning Commission',
     'All requests for the subdivision of land within areas so designated as T2 Rural Neighborhood policies shall be reviewed and developed as a Rural Character Subdivision in accordance with the provisions of this Chapter.',
     'Proposed text as printed in the minutes, approved 9-0 on p16. "Shall": regulatory, unlike the character policies. Includes tree canopy preservation (p14).'),
    (M16B, 10, 'highland_rim_named_place', 'status_claim', 'Whites Creek deferred areas adopted, including Areas 7 and 8 as drafted (RS2016-142)', None, None, '2016', 'Metro Planning Commission',
     'Councilmember Allen moved and Ms. Farr seconded the motion to approve policies as recommended for nine areas. Approve NashvilleNext Static draft recommendations for Area 7 and Area 8. (6-2-2)',
     'Staff had asked to defer Areas 7 and 8 (Fontanel case); the commission adopted the Static Draft for them instead. Staff moved four areas inside the Urban Services District to T3 (pp5-9). Two commissioners recused. Bears on pair 24.'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‐': '-', '­': ''})
cache = {}
def variants(doc, p):
    if (doc, p) not in cache:
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), f'{PDF_DIR}/{FILE[doc]}', '-'], capture_output=True, text=True).stdout.translate(Q)
        cache[(doc, p)] = [n(t), n(re.sub(r'(\w)-\n(\w)', r'\1\2', t)), n(re.sub(r'-\n', '-', t))]
    return cache[(doc, p)]

wb = openpyxl.load_workbook(XLSX)
have_src = {x[0] for x in wb['Sources'].iter_rows(min_row=2, values_only=True)}
bad = [(r[0][13:30], r[1], r[4][:40]) for r in ROWS if not any(n(r[9].translate(Q)) in v for v in variants(r[0], r[1]))]
bad += [('source exists', s[0]) for s in SOURCES if s[0] in have_src]
print('rows', len(ROWS), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

def append(ws, rows, width):
    last = max(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value is not None)
    for k, r in enumerate(rows, 1):
        for col in range(1, width + 1):
            s, d = ws.cell(last, col), ws.cell(last + k, col)
            d.value = r[col - 1]
            d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format

full = [[*r, 'verified', URL[r[0]]] for r in ROWS]
append(wb['Commitments'], full, 13)
append(wb['Highland Rim & named places'], [r for r in full if r[2] == 'highland_rim_named_place'], 12)
append(wb['Inconsistencies'], [r for r in full if 'INCONSISTENT' in (r[10] or '')], 12)

ws = wb['Sources']
total_r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'Total')
tail = [[(c.value, c._style) for c in ws[r]] for r in range(total_r, ws.max_row + 1)]
style = [c._style for c in ws[total_r - 1]]
for i, s in enumerate(SOURCES):
    for col, v in enumerate(s + [f'=COUNTIF(Commitments!$A:$A,A{total_r + i})'], 1):
        ws.cell(total_r + i, col).value = v
        ws.cell(total_r + i, col)._style = copy(style[col - 1])
for i, cells in enumerate(tail):
    for col, (v, st) in enumerate(cells, 1):
        c = ws.cell(total_r + len(SOURCES) + i, col)
        c.value, c._style = v, copy(st)
ws.cell(total_r + len(SOURCES), 7).value = f'=SUM(G2:G{total_r + len(SOURCES) - 1})'
wb.save(XLSX)

def dump(name, path, skip_blank):
    rows = [['' if v is None else v for v in r] for r in wb[name].iter_rows(values_only=True)]
    if skip_blank:
        rows = [r for r in rows if any(x != '' for x in r)]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
dump('Commitments', f'{CDIR}/commitments.csv', False)
dump('Highland Rim & named places', f'{CDIR}/highland_rim.csv', False)
dump('Inconsistencies', f'{CDIR}/inconsistencies.csv', False)
dump('Sources', f'{CDIR}/sources.csv', True)
print('written')
