"""Count tagged promises per policy-brief recommendation (R01-R19): write brief_rec_counts.csv and print a summary table.

Usage: python3 brief_counts.py <commitments_dir>
Reads commitments.csv (brief_rec, brief_match columns, added by brief_tags_apply.py --write) and sources.csv. Writes only
brief_rec_counts.csv. A 'full' row is a row with any full match; 'full+partial' counts every tagged row once.
Rows from documents marked counted = 'no' on sources.csv are skipped.
Year is the document's year from the Sources tab date (same rule as top5_timeline.py).
"""
import csv, re, sys

CDIR = sys.argv[1]
RECS = [f'R{i:02d}' for i in range(1, 20)]
src = {r[0]: r for r in csv.reader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r and r[0]}
year = lambda d: int((re.search(r'(19|20)\d\d', src[d][2]) or re.search(r'(19|20)\d\d', d)).group(0))
com = list(csv.DictReader(open(f'{CDIR}/commitments.csv', encoding='utf-8')))
not_counted = {r['doc'] for r in csv.DictReader(open(f'{CDIR}/sources.csv', encoding='utf-8')) if r.get('counted') == 'no'}
tagged = [c for c in com if c['brief_rec'] and c['doc'] not in not_counted]


def stats(pairs):
    """pairs: list of (doc, match). Returns counts and year range for full and full+partial."""
    full = [d for d, m in pairs if m == 'full']
    alld = [d for d, _ in pairs]
    fy = [year(d) for d in full]
    ay = [year(d) for d in alld]
    return {'full_rows': len(full), 'partial_rows': len(pairs) - len(full),
            'full_docs': len(set(full)), 'all_docs': len(set(alld)),
            'full_first': min(fy, default=''), 'full_last': max(fy, default=''),
            'all_first': min(ay, default=''), 'all_last': max(ay, default='')}


rows = []
for rec in RECS:
    pairs = []
    for c in tagged:
        for r, m in zip(c['brief_rec'].split(';'), c['brief_match'].split(';')):
            if r == rec:
                pairs.append((c['doc'], m))
    rows.append({'rec': rec, **stats(pairs)})

total_pairs = []
for c in tagged:
    ms = c['brief_match'].split(';')
    total_pairs.append((c['doc'], 'full' if 'full' in ms else 'partial'))
tot = stats(total_pairs)
tot['partial_rows'] = len(total_pairs) - tot['full_rows']
rows.append({'rec': 'Total (each row once)', **tot})

cols = ['rec', 'full_rows', 'partial_rows', 'full_docs', 'all_docs', 'full_first', 'full_last', 'all_first', 'all_last']
with open(f'{CDIR}/brief_rec_counts.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(cols)
    for r in rows:
        w.writerow([r[c] for c in cols])


def span(a, b):
    if a == '':
        return ''
    return str(a) if a == b else f'{a}-{b}'


print('| Rec | Full | Partial | Docs (full) | Docs (all) | Years (full) | Years (all) |')
print('|---|---|---|---|---|---|---|')
for r in rows[:-1]:
    print(f"| {r['rec']} | {r['full_rows']} | {r['partial_rows']} | {r['full_docs']} | {r['all_docs']} | "
          f"{span(r['full_first'], r['full_last'])} | {span(r['all_first'], r['all_last'])} |")
print(f"Full matches: {tot['full_rows']} statements in {tot['full_docs']} Metro documents since {tot['full_first']}.")
print(f"Full and partial: {len(total_pairs)} statements in {tot['all_docs']} Metro documents since {tot['all_first']}.")
