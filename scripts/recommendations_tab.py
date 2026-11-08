"""Write the Recommendations tab of NHRF_Commitments.xlsx and its CSV twin, recommendations.csv.

Usage: python3 recommendations_tab.py <commitments_dir>
One row per recommendation in promise_counts.csv (P01-P19), joined to distinct_promises.csv for the evidence column
(what_was_done is the what_happened text). The sheet is replaced if it exists and placed right after Forest_Priorities
(else at the end). The header copies the style of the Commitments header row (A1). Rerun after promise_counts.py.
"""
import csv, sys
from copy import copy
import openpyxl
from openpyxl.styles import Alignment

CDIR = sys.argv[1]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
OUT = f'{CDIR}/recommendations.csv'
HEAD = ['promise_id', 'recommendation', 'priority', 'times', 'documents', 'first_year', 'last_year', 'status', 'what_was_done', 'evidence']
WIDTHS = [10, 50, 11, 8, 10, 10, 10, 22, 70, 40]

dp = {p['promise_id']: p for p in csv.DictReader(open(f'{CDIR}/distinct_promises.csv', encoding='utf-8'))}
rows = []
for r in csv.DictReader(open(f'{CDIR}/promise_counts.csv', encoding='utf-8')):
    p = dp[r['promise_id']]
    num = lambda v: int(v) if v else ''
    rows.append([r['promise_id'], r['promise'], r['priority'], int(r['times']), int(r['docs']), num(r['first_year']),
                 num(r['last_year']), r['status'], r['what_happened'], p['evidence']])

wb = openpyxl.load_workbook(XLSX)
hdr = wb['Commitments']['A1']
if 'Recommendations' in wb.sheetnames:
    del wb['Recommendations']
idx = wb.sheetnames.index('Forest_Priorities') + 1 if 'Forest_Priorities' in wb.sheetnames else len(wb.sheetnames)
ws = wb.create_sheet('Recommendations', idx)
wrap = Alignment(wrap_text=True, vertical='top')
for c, h in enumerate(HEAD, 1):
    cell = ws.cell(1, c, h)
    cell.font, cell.fill, cell.border = copy(hdr.font), copy(hdr.fill), copy(hdr.border)
    cell.alignment = Alignment(wrap_text=True, vertical=hdr.alignment.vertical, horizontal=hdr.alignment.horizontal)
for r, row in enumerate(rows, 2):
    for c, v in enumerate(row, 1):
        ws.cell(r, c, v).alignment = wrap
for c, w in enumerate(WIDTHS):
    ws.column_dimensions[openpyxl.utils.get_column_letter(c + 1)].width = w
ws.freeze_panes = 'A2'
wb.save(XLSX)

out = [['' if v is None else v for v in r] for r in ws.iter_rows(values_only=True)]
with open(OUT, 'w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows(out)
print(f'Recommendations tab written, {ws.max_row - 1} rows; recommendations.csv {len(out) - 1} rows')
