"""Mark which Sources-tab documents the Alliance counts, and why the rest are background only.

Usage: python3 counted_docs.py <commitments_dir> [--write]
The Alliance counts only adopted plans and official final Metro documents. Six documents stay in the workbook as
background but are not counted in any number (NOT_COUNTED below). Dry run prints the counted and not-counted lists and
exits 1 if any of the six is missing from the Sources tab. With --write, adds H 'counted' (yes/no) and I
'not_counted_reason' to every source row (column A set and column F starting with http), then rewrites sources.csv.
Re-running overwrites rather than shifts.
"""
import csv, sys
from copy import copy
import openpyxl

CDIR = sys.argv[1]
WRITE = '--write' in sys.argv[2:]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
NOT_COUNTED = {
    'Livable_Nashville_2017_DRAFT': 'Draft, never adopted',
    'Stormwater_Master_Plan_2025_DRAFT': 'Draft, never adopted',
    'Ordinance_BL2006-1046': 'Bill withdrawn, never enacted',
    'Green_Ribbon_Committee_Report_2009': 'Advisory committee report, not adopted by Metro',
    'SAC_Climate_Mitigation_Action_Plan_2021': 'Advisory committee report, not adopted by Metro',
    'NashvilleNext_Natural_Resources_Background_2013': 'Staff background report, not adopted',
}

wb = openpyxl.load_workbook(XLSX)
ws = wb['Sources']
rows = [r for r in range(2, ws.max_row + 1)
        if ws.cell(r, 1).value and str(ws.cell(r, 6).value or '').startswith('http')]
docs = [ws.cell(r, 1).value for r in rows]
missing = [d for d in NOT_COUNTED if d not in docs]
print('counted', [d for d in docs if d not in NOT_COUNTED])
print('not counted', [d for d in docs if d in NOT_COUNTED])
print('missing', missing)
if missing:
    sys.exit(1)
if not WRITE:
    sys.exit(0)

def style(dst, src):
    dst.font = copy(src.font)
    dst.alignment = copy(src.alignment)
    dst.border = copy(src.border)
    dst.fill = copy(src.fill)
    dst.number_format = src.number_format

ws['H1'], ws['I1'] = 'counted', 'not_counted_reason'
style(ws['H1'], ws['G1'])
style(ws['I1'], ws['G1'])
for r in rows:
    reason = NOT_COUNTED.get(ws.cell(r, 1).value)
    ws.cell(r, 8).value = 'no' if reason else 'yes'
    ws.cell(r, 9).value = reason
    style(ws.cell(r, 8), ws.cell(r, 7))
    style(ws.cell(r, 9), ws.cell(r, 7))
wb.save(XLSX)

out = [['' if v is None else v for v in r] for r in ws.iter_rows(values_only=True)]
out = [r for r in out if any(x != '' for x in r)]
with open(f'{CDIR}/sources.csv', 'w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows(out)
print('written')
