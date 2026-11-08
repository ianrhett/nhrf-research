"""Check promise_groups.csv against the Commitments sheet and, with --write, add the promise_id column (P).

Usage: python3 promise_groups_apply.py <commitments_dir> [--write]
Each row of promise_groups.csv names a Commitments row (1-based, header is row 1) and must match that row's doc and
pdf_page; promise_id must be P01-P19 and present in distinct_promises.csv, or 'context'; no row may appear twice.
Dry run prints 'groups N bad [...]' and exits 1 on any problem. With --write, P1 is set to 'promise_id' and P is set on
every data row (None when ungrouped), so re-running overwrites rather than shifts. Then commitments.csv is rewritten.
"""
import csv, re, sys
from copy import copy
import openpyxl

CDIR = sys.argv[1]
WRITE = '--write' in sys.argv[2:]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
CSV = f'{CDIR}/commitments.csv'

wb = openpyxl.load_workbook(XLSX)
ws = wb['Commitments']
groups = list(csv.DictReader(open(f'{CDIR}/promise_groups.csv', encoding='utf-8')))
known = {p['promise_id'] for p in csv.DictReader(open(f'{CDIR}/distinct_promises.csv', encoding='utf-8'))}

bad, seen = [], set()
for g in groups:
    r = int(g['row'])
    if r in seen:
        bad.append(('duplicate row', r))
    seen.add(r)
    if ws.cell(r, 1).value != g['doc']:
        bad.append(('doc', r, g['doc']))
    if str(ws.cell(r, 2).value) != g['pdf_page']:
        bad.append(('pdf_page', r, g['pdf_page']))
    p = g['promise_id']
    if p != 'context' and not (re.match(r'^P(0[1-9]|1[0-9])$', p) and p in known):
        bad.append(('promise_id', r, p))

print(f'groups {len(groups)} bad {bad}')
if bad:
    sys.exit(1)
if not WRITE:
    sys.exit(0)

def style(dst, src):
    dst.font = copy(src.font)
    dst.alignment = copy(src.alignment)
    dst.border = copy(src.border)
    dst.fill = copy(src.fill)
    dst.number_format = src.number_format

pid = {int(g['row']): g['promise_id'] for g in groups}
ws['P1'] = 'promise_id'
style(ws['P1'], ws['M1'])
for r in range(2, ws.max_row + 1):
    if not ws.cell(r, 1).value:
        continue
    ws.cell(r, 16).value = pid.get(r) or None
    style(ws.cell(r, 16), ws.cell(r, 13))
wb.save(XLSX)

rows = [['' if v is None else v for v in r] for r in ws.iter_rows(values_only=True)]
with open(CSV, 'w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows(rows)
print('written')
