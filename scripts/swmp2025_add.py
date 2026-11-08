"""Add the DRAFT Stormwater Master Plan (MWS, June 2025) as a source with Commitments and Highland Rim rows.

Usage: python3 swmp2025_add.py <DRAFT-SW_MasterPlan-2025.pdf> <commitments_dir> [--write]
The PDF (110 MB, too large for GitHub) is the file at SOURCE[5]; sha256
398dec8a57549ed41e1803dd2e51bc3d4e9cea2685b118a414b046b088693627.
Rechecks every excerpt against whitespace-flattened pdftotext of its stated PDF page
and exits without writing on any miss or duplicate.
"""
import csv, re, subprocess, sys
import openpyxl
from copy import copy

PDF, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
D = 'Stormwater_Master_Plan_2025_DRAFT'
URL = 'https://www.nashville.gov/sites/default/files/2025-09/DRAFT-SW_MasterPlan-2025.pdf'
SOURCE = [D, 'Metropolitan Nashville and Davidson County Stormwater Master Plan, DRAFT (Metro Water Services; Barge Design Solutions)',
          'June 2025 (cover); PDF created June 20, 2023; posted September 2025', 'DRAFT', 198, URL]

# page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes, verify
ROWS = [
    (38, 'forest_protection', 'baseline', 'Model runoff curve number: woods vs open space (soil group B)', '60', 'curve number', None, 'Metro Water Services',
     'Woods (fair condition) B 60',
     'Appendix A Table 1.1 (printed A-2). Open space (fair condition) on B soils is 69; lower means less runoff. Woods is lower on every soil group (A 36 vs 49, C 73 vs 79, D 79 vs 84). The plan states no conclusion from this; it is a model input.', 'verified_by_hand'),
    (39, 'forest_protection', 'baseline', 'Model surface roughness: forest is the highest', '0.4', "Manning's n", None, 'Metro Water Services',
     'Deciduous Forest Evergreen Forest Mixed Forest Shrub/Scrub PERVIOUS 100 0.4',
     "Appendix A Table 1.2 (printed A-3), 2021 NLCD classes. Developed open space, pasture and crops 0.3; developed land 0.25. Higher n slows runoff. Model input only; the only use of the word forest in the plan.", 'verified_by_hand'),
    (27, 'floodplain_stream', 'definition', 'Remedial alternatives considered are all pipe and storage measures', '5', 'alternative types', None, 'Metro Water Services',
     'Increase the capacity of the pipes and associated structures to alleviate the capacity restriction to the outfalls.',
     'First of five: larger pipes, detention storage, reroute to parallel pipes, extend the system, bypass around buildings. No land, forest or upstream conservation alternative.', 'verified'),
    (27, 'policy_mechanism', 'definition', 'Future flooding modeled on NashvilleNext growth map', None, None, None, 'Metro Water Services',
     'Nashville Next concept map was used to estimate future development conditions.',
     'Future impervious cover from the Concept Map is added to the model (also Appendix A p41). Development is an input, not a choice the plan tests.', 'verified'),
    (17, 'floodplain_stream', 'target', 'Level of service for proposed projects', '10', 'year 24-hour storm', None, 'Metro Water Services',
     'meet a level of service corresponding to a 10-year 24-hour design storm event',
     'Printed p14. 100-year flows checked for major systems over 100 cfs (p27). Modeled pipes are 15 inches and larger (p25).', 'verified'),
    (13, 'highland_rim_named_place', 'status_claim', 'Whites Creek sub-basins not yet inventoried or modeled', '5', 'sub-basins', None, 'Metro Water Services',
     'Whites Creek A 5 Whites Creek B 5 Whites Creek C 5 Whites Creek D 5 Whites Creek E 5',
     'Table 3.2 status as of 6/28/2025: no stage marked for these rows. Same for Earthman, Marrowbone, Eatons Creek, Ewing Creek, Bells Bend, Overall Creek, Harpeth and Sevenmile basins (pp13-16). Whites Creek treated as a Highland Rim watershed per the MS4 FY19 row; the plan does not name the Highland Rim.', 'verified_by_hand'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
page = lambda p: n(subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), PDF, '-'], capture_output=True, text=True).stdout)

wb = openpyxl.load_workbook(XLSX)
assert D not in {r[0] for r in wb['Sources'].iter_rows(min_row=2, values_only=True)}, 'source already present'
bad = [(p, m) for p, _, _, m, *_, ex, _, _ in ROWS if n(ex) not in page(p)]
print('rows', len(ROWS), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

def append(ws, rows, width):
    last = ws.max_row
    for r in rows:
        ws.append(r[:width])
        for col in range(1, width + 1):
            s, d = ws.cell(last, col), ws.cell(ws.max_row, col)
            d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format

full = [[D, *r, URL] for r in ROWS]
append(wb['Commitments'], full, 13)
append(wb['Highland Rim & named places'], [r for r in full if r[2] == 'highland_rim_named_place'], 12)

ws = wb['Sources']
total_r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'Total')
tail = [[(c.value, c._style) for c in ws[r]] for r in range(total_r, ws.max_row + 1)]
style = [c._style for c in ws[total_r - 1]]
for col, v in enumerate(SOURCE + [f'=COUNTIF(Commitments!$A:$A,A{total_r})'], 1):
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
