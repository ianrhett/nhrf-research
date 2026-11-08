"""Build the one-page summary (all 19 recommendations, dot timeline) from the workbook CSVs.

Usage: python3 build_one_pager.py <commitments_dir> one-pager.tmpl.html one-pager.html
Then print to PDF with headless Chrome (v1.7.1: NHRF_Recommended_216_Times_v1.7.1.pdf): --headless=new --no-pdf-header-footer --print-to-pdf=<out.pdf> file://<one-pager.html>
Counts come from promise_groups.csv (counted documents only; enacted rules and allocations excluded, FACTS.md section I) and statuses from distinct_promises.csv; row labels and short notes are in LBL.
v1.7.0 (NHRF-DOCLIST-001) adds "The documents": the counted documents with forest recommendations (FACTS.md D2), year and title, sorted by year, from sources.csv and commitments.csv; the document names are in NAME.
v1.7.1 (NHRF-MONEY-001 follow-up, 2026-11-08): P08 note no longer says "unfunded"; 27DS0031 is listed in the adopted FY2027 CIB and was left out of the FY2027 Capital Spending Plan adopted Nov 5, 2026 (FACTS.md F10).
"""
import csv, math, re, sys
from collections import Counter
C, TMPL, OUT = sys.argv[1:4]
src = {r['doc']: r for r in csv.DictReader(open(f'{C}/sources.csv', encoding='utf-8')) if r['source_url'].startswith('http')}
year = lambda d: int((re.search(r'(19|20)\d\d', src[d]['date']) or re.search(r'(19|20)\d\d', d)).group(0))
ENACTED = {'Ordinance_BL2021-829', 'Executive_Order_041A_2024', 'Metro_Code_17.28.030', 'Metro_Code_17.28.065', 'Metro_Code_17.40.440', 'Ordinance_BL2017-725', 'Resolution_RS2025-1549', 'Resolution_RS2025-1556'}
REC = {'recommendation', 'commitment', 'target', 'funding_estimate'}
kind = {(r['doc'], r['pdf_page'], r['metric']): r['item_type'] for r in csv.DictReader(open(f'{C}/commitments.csv', encoding='utf-8'))}
groups = [r for r in csv.DictReader(open(f'{C}/promise_groups.csv', encoding='utf-8')) if r['promise_id'].startswith('P') and int(r['promise_id'][1:]) <= 19 and src[r['doc']]['counted'] == 'yes' and r['doc'] not in ENACTED and kind.get((r['doc'], r['pdf_page'], r['metric'])) in REC]
dp = {r['promise_id']: r for r in csv.DictReader(open(f'{C}/distinct_promises.csv', encoding='utf-8'))}
LBL = {'P01': ('Keep building off steep slopes', '15% rule only for rural subdivisions; else 20%'),
       'P02': ('Preserve the Rim escarpment', 'Policy only; master plan budgeted 2024, not started'),
       'P03': ('Keep sewers out of rural Rim land', 'No sewer check against policy; extensions go on*'),
       'P04': ('Keep rural land rural', 'Rural subdivision rules only; no farm zoning'),
       'P05': ('Require conservation subdivisions', '50% recommended; 20% enacted, not on AR2a'),
       'P06': ('Protect trees during development', 'Nothing requires keeping existing trees'),
       'P07': ("Hold the county's tree canopy", 'Rural canopy held; no rule protects forest tracts'),
       'P08': ('Buy natural land on the Rim', 'No acquisition program; $7M easement line not appropriated'),
       'P09': ('Meet the conserved-land goals', '4,541-acre goal due 2026; others unreported'),
       'P10': ('Keep the Open Space Fund funded', 'No record of the fund since 2011'),
       'P11': ('Use easements and development rights', 'Easements once (2009); no TDR for land'),
       'P12': ('Conserve upstream land regionally', 'No agreement or program found'),
       'P13': ("Manage Metro's natural areas", 'Designation policy 2026; no site plans yet'),
       'P14': ('Fund urban forestry and canopy studies', 'Program, tree fund and studies in place'),
       'P15': ('Protect rare habitats and species', 'Stream buffers only; no glade or invasives plan'),
       'P16': ('Protect scenic hills and roadsides', 'Scenic easements on some roads; no ridgeline rule'),
       'P17': ('Site development around trees', 'Replacement meets the rule; retention not required'),
       'P18': ('Connect protected natural areas', 'Piece by piece; no mapped system'),
       'P19': ('Broad goals for the natural environment', 'No measurable target')}
SHORT = {'Implemented': 'Implemented', 'Not implemented': 'Not implemented', 'Partly implemented': 'Partly', 'No implementation reported': 'No report'}
COL = {'Implemented': '#1f4d36', 'Not implemented': '#b3261e', 'Partly implemented': '#a35f00', 'No implementation reported': '#6b6b6b'}
cnt = Counter((g['promise_id'], year(g['doc'])) for g in groups)
tot = Counter(g['promise_id'] for g in groups)
W, X0, X1, ROWH, TOP = 960, 240, 520, 22, 22
x = lambda yr: X0 + (yr - 1973) / (2026 - 1973) * (X1 - X0)
ids = [p for p in sorted(dp) if int(p[1:]) <= 19]
H = TOP + ROWH * len(ids) + 22
s = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">']
for yr in (1973, 1981, 1992, 2009, 2017, 2026):
    s.append(f'<line x1="{x(yr):.1f}" y1="{TOP-6}" x2="{x(yr):.1f}" y2="{H-22}" stroke="#e3e7e4"/>')
    s.append(f'<text x="{x(yr):.1f}" y="{H-7}" font-size="10" fill="#6b6b6b" text-anchor="middle">{yr}</text>')
s.append(f'<text x="{X1+26}" y="{TOP-10}" font-size="9" fill="#6b6b6b" letter-spacing="0.6">TIMES · DONE?</text>')
for i, pid in enumerate(ids):
    cy = TOP + ROWH * i + ROWH / 2
    if i:
        s.append(f'<line x1="0" y1="{cy-ROWH/2:.1f}" x2="{W}" y2="{cy-ROWH/2:.1f}" stroke="#eef0ee"/>')
    label, note = LBL[pid]
    st = dp[pid]['status']
    s.append(f'<text x="0" y="{cy+4:.1f}" font-size="13" fill="#1a1a1a">{label}</text>')
    yrs = [y for (p, y) in cnt if p == pid]
    if yrs:  # a recommendation with no counted statement has no baseline or dots
        s.append(f'<line x1="{x(min(yrs)):.1f}" y1="{cy:.1f}" x2="{X1}" y2="{cy:.1f}" stroke="#a9c7b3" stroke-width="1"/>')
    for (p, yr), n in sorted(cnt.items()):
        if p == pid:
            s.append(f'<circle cx="{x(yr):.1f}" cy="{cy:.1f}" r="{2.2 + 1.9 * math.sqrt(n):.1f}" fill="#1f4d36" fill-opacity="0.82"/>')
    s.append(f'<text x="{X1+44}" y="{cy+5:.1f}" font-size="15" font-weight="700" fill="#1f4d36" text-anchor="end">{tot[pid]}</text>')
    s.append(f'<text x="{X1+56}" y="{cy+4:.1f}" font-size="11.5" fill="#555"><tspan font-weight="700" fill="{COL[st]}">{SHORT[st]}</tspan>  {note}</text>')
s.append('</svg>')

# "The documents" (v1.7.0, NHRF-DOCLIST-001): the counted documents with forest recommendations (FACTS.md D2), one line each,
# year then the title as FACTS.md names it, sorted by year. Documents, not files: NashvilleNext and Plan to Play 2026 are one each.
# The set is computed the way count_funnel.py computes D2 (counted, not an enacted rule, recommendation type, Forest category or P01-P19 tag).
FOREST = {'forest_protection', 'tree_canopy', 'highland_rim_named_place', 'habitat_natural_area', 'land_acquisition', 'open_space'}
RULES = ENACTED | {'Subdivision_Regulations_Chapter_4_2024'}
document = lambda d: 'NashvilleNext' if d.startswith('NashvilleNext_') else 'Plan_to_Play_2026' if d.startswith('Plan_to_Play_2026') else d
NAME = {'NEA_1973_Natural_Environmental_Analysis': 'Natural Environmental Analysis',
        'General_Plan_1980_2000': 'General Plan',
        'Concept_2010_General_Plan_1992': 'Concept 2010',
        'Green_Infrastructure_Master_Plan_2009': 'Green Infrastructure Master Plan',
        'Tree_Canopy_Assessment_2010': 'Tree Canopy Assessment',
        'Nashville_Open_Space_Plan_2011': 'Open Space Plan',
        'Home_Buyout_Audit_2014': 'Home Buyout Audit',
        'NashvilleNext': 'NashvilleNext',
        'Urban_Forestry_Landscape_Master_Plan_2016': 'Urban Forestry Landscape Master Plan',
        'Plan_to_Play_2017_Full_Plan': 'Plan to Play',
        'MS4_Annual_Report_FY19': 'MS4 Annual Report FY19',
        'Urban_Tree_Canopy_Assessment_2023': 'Urban Tree Canopy Assessment',
        'Climate_Adaptation_Resilience_Plan_2024_Final': 'Climate Adaptation and Resilience Plan',
        'Hazard_Mitigation_Plan_2026_Final': 'Hazard Mitigation Plan',
        'Plan_to_Play_2026': 'Plan to Play 2026 Update'}
docs = set()
for r in csv.DictReader(open(f'{C}/commitments.csv', encoding='utf-8')):
    d = r['doc']
    if d in src and src[d]['counted'] == 'yes' and d not in RULES and r['item_type'] in REC and (r['category'] in FOREST or re.fullmatch(r'P(0[1-9]|1[0-9])', r['promise_id'] or '')):
        docs.add(document(d))
missing = docs - set(NAME)
assert not missing, f'no FACTS.md name for {sorted(missing)}'
doc_year = {}
for f, r in src.items():
    if r['counted'] == 'yes':
        doc_year[document(f)] = min(doc_year.get(document(f), 9999), year(f))
listed = sorted(docs, key=lambda d: (doc_year[d], NAME[d]))
DOCS_PT, DOCS_LH = 6, 1.1  # this section only: 6pt is the largest size that keeps the PDF to one page (7pt overflows by 19px); nothing else on the page was resized
docs_html = [f'<p id="docs" style="font-size:{DOCS_PT}pt;line-height:{DOCS_LH};margin:2pt 0 0;color:#1a1a1a">'
             f'<b style="color:#1f4d36;letter-spacing:0.09em;text-transform:uppercase">The documents</b>'
             f'<span style="color:#5f6661"> ({len(listed)}, by year)</span> '
             + ' &middot; '.join(f'<b>{doc_year[d]}</b>&nbsp;{NAME[d]}' for d in listed) + '</p>']
open(OUT, 'w', encoding='utf-8').write(open(TMPL, encoding='utf-8').read().replace('{{CHART}}', '\n'.join(s + docs_html)))
print(sum(tot.values()), 'statements;', len(tot), 'recommendations;', Counter(dp[p]['status'] for p in ids))
print(len(listed), 'documents:', '; '.join(f'{doc_year[d]} {NAME[d]}' for d in listed))
