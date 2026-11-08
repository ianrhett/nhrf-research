"""Count how often Metro's plans made each of the 19 distinct forest recommendations: write promise_counts.csv and print a summary.

Usage: python3 promise_counts.py <commitments_dir>
Reads promise_groups.csv, distinct_promises.csv and sources.csv. Uses only rows grouped P01-P19 (not 'context') whose
document is counted (sources.csv 'counted' is not 'no'). Year is the document's year from the Sources tab date (same
rule as top5_timeline.py). Writes only promise_counts.csv, with a 'priority' column (Core for P01-P12, Supporting for P13-P19). After the
all-items summary it prints two more lines computed over the core P01-P12 only.
"""
import csv, re, sys

CDIR = sys.argv[1]
src = {r[0]: r for r in csv.reader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r and r[0]}
year = lambda d: int((re.search(r'(19|20)\d\d', src[d][2]) or re.search(r'(19|20)\d\d', d)).group(0))
counted = {r['doc'] for r in csv.DictReader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r.get('counted') != 'no'}
promises = list(csv.DictReader(open(f'{CDIR}/distinct_promises.csv', encoding='utf-8')))
groups = [g for g in csv.DictReader(open(f'{CDIR}/promise_groups.csv', encoding='utf-8'))
          if re.match(r'^P\d\d$', g['promise_id']) and g['doc'] in counted]

rows = []
for p in promises:
    docs = [g['doc'] for g in groups if g['promise_id'] == p['promise_id']]
    ys = [year(d) for d in docs]
    rows.append([p['promise_id'], p['promise'], 'Core' if int(p['promise_id'][1:]) <= 12 else 'Supporting', len(docs), len(set(docs)), min(ys, default=''), max(ys, default=''),
                 p['status'], p['what_happened']])
with open(f'{CDIR}/promise_counts.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['promise_id', 'promise', 'priority', 'times', 'docs', 'first_year', 'last_year', 'status', 'what_happened'])
    w.writerows(rows)

print('| ID | Recommendation | Priority | Times | Docs | First | Last | Status |')
print('|---|---|---|---|---|---|---|---|')
for r in rows:
    print(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} |')
T = sum(r[3] for r in rows)
D = len({g['doc'] for g in groups})
first, last = min(r[5] for r in rows if r[5] != ''), max(r[6] for r in rows if r[6] != '')
st = lambda s: sum(r[7] == s for r in rows)
print(f'{len(rows)} distinct recommendations, made {T} times in {D} Metro documents, {first} to {last}.')
print(f"Status: {st('Not implemented')} not implemented, {st('Partly implemented')} partly implemented, {st('No implementation reported')} no implementation reported, {st('Implemented')} fully implemented.")
core = [r for r in rows if r[2] == 'Core']
core_ids = {r[0] for r in core}
cT = sum(r[3] for r in core)
cD = len({g['doc'] for g in groups if g['promise_id'] in core_ids})
cfirst, clast = min(r[5] for r in core if r[5] != ''), max(r[6] for r in core if r[6] != '')
cst = lambda s: sum(r[7] == s for r in core)
print(f'Core (P01-P12): {len(core)} recommendations, made {cT} times in {cD} Metro documents, {cfirst} to {clast}.')
print(f"Core status: {cst('Not implemented')} not implemented, {cst('Partly implemented')} partly implemented, {cst('No implementation reported')} no implementation reported, {cst('Implemented')} fully implemented.")
