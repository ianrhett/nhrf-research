"""Check brief_tags.csv against the Commitments sheet and, with --write, add the brief_rec and brief_match columns (N, O).

Usage: python3 brief_tags_apply.py <commitments_dir> [--write]
Each tag names a Commitments row (1-based, header is row 1) and must match that row's doc and pdf_page; item_type must
be a promise-type value; brief_rec (R01-R19, semicolon-separated) and brief_match (full or partial) must pair up.
Dry run prints 'tags N bad [...]' and exits 1 on any problem. With --write, N1/O1 are set to the headers and N/O are
set on every data row (None when untagged), so re-running overwrites rather than shifts. Then commitments.csv is rewritten.
"""
import csv, re, sys
from copy import copy
import openpyxl

CDIR = sys.argv[1]
WRITE = '--write' in sys.argv[2:]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
CSV = f'{CDIR}/commitments.csv'
TYPES = {'recommendation', 'commitment', 'target', 'funding_estimate', 'funding_allocated'}

wb = openpyxl.load_workbook(XLSX)
ws = wb['Commitments']
tags = list(csv.DictReader(open(f'{CDIR}/brief_tags.csv', encoding='utf-8')))

bad, seen = [], set()
for t in tags:
    r = int(t['row'])
    if r in seen:
        bad.append(('duplicate row', r))
    seen.add(r)
    if ws.cell(r, 1).value != t['doc']:
        bad.append(('doc', r, t['doc']))
    if str(ws.cell(r, 2).value) != t['pdf_page']:
        bad.append(('pdf_page', r, t['pdf_page']))
    if ws.cell(r, 4).value not in TYPES:
        bad.append(('item_type', r, ws.cell(r, 4).value))
    recs, matches = t['brief_rec'].split(';'), t['brief_match'].split(';')
    if len(recs) != len(matches):
        bad.append(('length', r, t['brief_rec'], t['brief_match']))
    bad += [('rec', r, x) for x in recs if not re.match(r'^R(0[1-9]|1[0-9])$', x)]
    bad += [('match', r, x) for x in matches if x not in ('full', 'partial')]

print(f'tags {len(tags)} bad {bad}')
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

tag = {int(t['row']): (t['brief_rec'], t['brief_match']) for t in tags}
ws['N1'], ws['O1'] = 'brief_rec', 'brief_match'
style(ws['N1'], ws['M1'])
style(ws['O1'], ws['M1'])
for r in range(2, ws.max_row + 1):
    if not ws.cell(r, 1).value:
        continue
    rec, match = tag.get(r, (None, None))
    ws.cell(r, 14).value = rec or None
    ws.cell(r, 15).value = match or None
    style(ws.cell(r, 14), ws.cell(r, 13))
    style(ws.cell(r, 15), ws.cell(r, 13))
wb.save(XLSX)

rows = [['' if v is None else v for v in r] for r in ws.iter_rows(values_only=True)]
with open(CSV, 'w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows(rows)
print('written')
