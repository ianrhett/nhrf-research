"""Build the dot-chart data for the presentation and print the headline numbers.

Usage: python3 presentation_data.py <commitments_dir> <out_dir>
Reads promise_groups.csv, promise_counts.csv, commitments.csv, sources.csv and ../sources/MANIFEST.csv. Same filter as the
one-pager (build_one_pager.py; FACTS.md section I): rows grouped P01-P19 in counted documents, enacted-rule documents
excluded, REC item types only; year from the Sources tab date. Writes <out_dir>/recommendation_dots.csv
(one row per recommendation per document, with how many times that document made it) and recommendation_dots.json
(the same, nested by recommendation, for the web chart). Mayor is the Metro mayor in office on the document's date; when
the date names only a year that changed mayors, mayor_note says so and the mayor who served most of that year is used.
"""
import csv, json, re, sys
from collections import Counter, OrderedDict

CDIR, OUT = sys.argv[1], sys.argv[2]
MONTHS = {m: i for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                                       'september', 'october', 'november', 'december'], 1)}
# (first day in office as (year, month), mayor). Metro terms change in late September except Barry to D. Briley (March 2018).
MAYORS = [((1963, 4), 'Beverly Briley'), ((1975, 10), 'Richard Fulton'), ((1987, 10), 'Bill Boner'),
          ((1991, 10), 'Phil Bredesen'), ((1999, 10), 'Bill Purcell'), ((2007, 10), 'Karl Dean'),
          ((2015, 10), 'Megan Barry'), ((2018, 3), 'David Briley'), ((2019, 10), 'John Cooper'),
          ((2023, 10), "Freddie O'Connell")]


def mayor_on(y, m):
    return [n for start, n in MAYORS if start <= (y, m)][-1]


src = {r[0]: r for r in csv.reader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r and r[0]}
year = lambda d: int((re.search(r'(19|20)\d\d', src[d][2]) or re.search(r'(19|20)\d\d', d)).group(0))
counted = {r['doc'] for r in csv.DictReader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r.get('counted') != 'no'}
# Same filter as build_one_pager.py: enacted rules and allocations are not recommendations (FACTS.md section I).
ENACTED = {'Ordinance_BL2021-829', 'Executive_Order_041A_2024', 'Metro_Code_17.28.030', 'Metro_Code_17.28.065', 'Metro_Code_17.40.440', 'Ordinance_BL2017-725', 'Resolution_RS2025-1549', 'Resolution_RS2025-1556'}
REC = {'recommendation', 'commitment', 'target', 'funding_estimate'}
kind = {(r['doc'], r['pdf_page'], r['metric']): r['item_type'] for r in csv.DictReader(open(f'{CDIR}/commitments.csv', encoding='utf-8'))}
manifest = {r['doc']: r for r in csv.DictReader(open(f'{CDIR}/../sources/MANIFEST.csv', encoding='utf-8'))}
recs = OrderedDict((r['promise_id'], r) for r in csv.DictReader(open(f'{CDIR}/promise_counts.csv', encoding='utf-8')))
groups = [g for g in csv.DictReader(open(f'{CDIR}/promise_groups.csv', encoding='utf-8'))
          if re.match(r'^P\d\d$', g['promise_id']) and g['doc'] in counted and g['doc'] not in ENACTED
          and kind.get((g['doc'], g['pdf_page'], g['metric'])) in REC]


def doc_mayor(d):
    y = year(d)
    if d.startswith('Metro_Code_'):
        return mayor_on(y, 12), 'Code text in force when read; not a new plan'
    mo = re.search(r'(' + '|'.join(MONTHS) + r')\b(?: \d{1,2},)? ' + str(y), src[d][2], re.I)
    if mo:
        return mayor_on(y, MONTHS[mo.group(1).lower()]), ''
    start, end = mayor_on(y, 1), mayor_on(y, 12)
    if start == end:
        return start, ''
    return start, f'Year only; {end} took office late in {y}'


hits = Counter((g['promise_id'], g['doc']) for g in groups)
rows = []
for (pid, d), n in sorted(hits.items(), key=lambda k: (k[0][0], year(k[0][1]), k[0][1])):
    m, note = doc_mayor(d)
    rows.append(OrderedDict(promise_id=pid, recommendation=recs[pid]['promise'], priority=recs[pid]['priority'],
                            status=recs[pid]['status'], doc=d, title=src[d][1], date=src[d][2], year=year(d),
                            mayor=m, mayor_note=note, times_in_doc=n, cover=manifest.get(d, {}).get('cover', ''),
                            source_url=src[d][5]))
fields = list(rows[0].keys())
with open(f'{OUT}/recommendation_dots.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
nested = [OrderedDict(promise_id=pid, recommendation=r['promise'], priority=r['priority'], status=r['status'],
                      what_happened=r['what_happened'], times=int(r['times']),
                      documents=[{k: x[k] for k in fields[4:]} for x in rows if x['promise_id'] == pid])
          for pid, r in recs.items()]
json.dump(nested, open(f'{OUT}/recommendation_dots.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# Headline numbers
docs = sorted({x['doc'] for x in rows}, key=year)
T = sum(x['times_in_doc'] for x in rows)
print(f'{len(recs)} recommendations, {T} times, {len(docs)} documents, {year(docs[0])} to {year(docs[-1])} ({year(docs[-1]) - year(docs[0])} years).')
dm = OrderedDict()
for d in docs:
    dm.setdefault(doc_mayor(d)[0], []).append(d)
print(f'Mayors whose administrations produced these documents: {len(dm)}')
for m, ds in dm.items():
    t = sum(x['times_in_doc'] for x in rows if x['doc'] in ds)
    print(f'  {m}: {len(ds)} documents, {t} times')
notes = {x['doc']: x['mayor_note'] for x in rows if x['mayor_note']}
for d, n in notes.items():
    print(f'  note {d}: {n}')
for tier in ('Core', 'Supporting'):
    sub = [x for x in rows if x['priority'] == tier]
    print(f"{tier}: {len({x['promise_id'] for x in sub})} recommendations, {sum(x['times_in_doc'] for x in sub)} times, "
          f"{len({x['doc'] for x in sub})} documents, {len({x['mayor'] for x in sub})} mayors")
print('Per recommendation: span in years, mayors, documents since 2015')
for pid, r in recs.items():
    sub = [x for x in rows if x['promise_id'] == pid]
    print(f"  {pid} {r['priority'][0]} {r['status'][:12]:12} span {int(r['last_year']) - int(r['first_year']):2} yrs, "
          f"{len({x['mayor'] for x in sub})} mayors, {sum(x['year'] >= 2015 for x in sub)} docs since 2015")
for since in (2015, 2023):
    sub = [x for x in rows if x['year'] >= since]
    print(f"Since {since}: {sum(x['times_in_doc'] for x in sub)} times in {len({x['doc'] for x in sub})} documents, "
          f"{len({x['promise_id'] for x in sub})} recommendations")
nn = [x for x in rows if x['doc'].startswith('NashvilleNext')]
print(f"NashvilleNext alone: {sum(x['times_in_doc'] for x in nn)} times, {len({x['promise_id'] for x in nn})} recommendations")
print('Missing covers:', [d for d in docs if not manifest.get(d, {}).get('cover')])
