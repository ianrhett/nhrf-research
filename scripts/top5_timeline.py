"""Write commitments/top5_timeline.csv: one row per promise in the five top-tier Forest families, for the home-page graphic.

Usage: python3 top5_timeline.py <commitments_dir>
Families F01-F05 on forest_priorities.csv (score 5). Year is the document's year from the Sources tab date
(adoption or publication), not the promise's due date. Columns: protection, year, doc, title, pdf_page,
metric, excerpt, target_year, pair, assessment. pair and assessment are filled where the promise was checked
on Promised_vs_Delivered. Documents marked counted = 'no' on sources.csv (drafts, withdrawn bills, advisory and background
reports) are excluded. Gaps between years reflect the corpus (it holds no plans dated 1982-1991 or 1993-2008), not
necessarily silence from Metro.
"""
import csv, re, sys

CDIR = sys.argv[1]
LABEL = {'F01': 'Limit building on steep slopes', 'F02': 'Conservation subdivisions with open space',
         'F03': 'Protect trees on private land', 'F04': 'Keep sewers and dense development out of rural Rim land',
         'F05': 'Buy or ease large natural lands'}
src = {r[0]: r for r in csv.reader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r and r[0]}
year = lambda d: int((re.search(r'(19|20)\d\d', src[d][2]) or re.search(r'(19|20)\d\d', d)).group(0))
not_counted = {r['doc'] for r in csv.DictReader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r.get('counted') == 'no'}
com = list(csv.DictReader(open(f'{CDIR}/commitments.csv', encoding='utf-8')))
pv = {p['pair']: p['assessment'] for p in csv.DictReader(open(f'{CDIR}/promised_vs_delivered.csv', encoding='utf-8')) if p['pair'].isdigit()}

out = []
for r in csv.DictReader(open(f'{CDIR}/forest_priorities.csv', encoding='utf-8')):
    if r['family'] not in LABEL:
        continue
    c = com[int(r['row']) - 2]  # forest_priorities 'row' is the Commitments sheet row (header is row 1)
    assert (c['doc'], c['pdf_page']) == (r['doc'], r['pdf_page']), r['row']
    if c['doc'] in not_counted:
        continue
    pair = r['checked'][5:] if r['checked'].startswith('Pair ') else ''
    out.append([LABEL[r['family']], year(r['doc']), r['doc'], src[r['doc']][1], r['pdf_page'], r['metric'], c['excerpt'],
                r['target_year'], pair, pv.get(pair, '')])
out.sort(key=lambda o: (list(LABEL.values()).index(o[0]), o[1]))
with open(f'{CDIR}/top5_timeline.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['protection', 'year', 'doc', 'title', 'pdf_page', 'metric', 'excerpt', 'target_year', 'pair', 'assessment'])
    w.writerows(out)
print(len(out), 'promises;', len({o[2] for o in out}), 'documents;', sorted({o[1] for o in out}))
