"""Adopted Metro tree and forest actions: RS2025-1549, BL2021-829 and Executive Order 41 (Amended).

Usage: python3 adopted_tree_actions_add.py <web_dir> <commitments_dir> [--write]
Three adopted Metro documents saved as plain text in web_dir/<doc>.txt (no pages): the Council's October
2025 resolution recognizing "Nashville's Highland Rim Forest", the 2021 ordinance on tree protection on Metro
department properties (Code Chapter 2.226), and the Mayor's April 2024 amended tree-policy order. Ten rows
kept. Every excerpt is rechecked against the whole normalized text of its file; the script exits without
writing on any miss, duplicate, or existing source. Rows whose notes contain INCONSISTENT also go to the
Inconsistencies tab. After --write: forest_priorities.py --write, cover_sheet.py, promise_counts.py,
brief_counts.py.
"""
import csv, re, sys
import openpyxl
from copy import copy

WEB, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
RS = 'Resolution_RS2025-1549'
BL = 'Ordinance_BL2021-829'
EO = 'Executive_Order_041A_2024'
URL = {
    RS: 'https://webapi.legistar.com/v1/nashville/matters/19659/texts/9302',
    BL: 'https://webapi.legistar.com/v1/nashville/matters/13387/texts/2662',
    EO: 'https://nashville.gov/departments/metro-clerk/legal-resources/executive-orders/mayor-freddie-oconnell/fo041a',
}
SOURCES = [
    [RS, 'Resolution RS2025-1549: recognizing the portion of the Western Highland Rim Forest within Metro as "Nashville\'s Highland Rim Forest"',
     'Passed October 2025 (Legistar passed date 2025-10-10)', 'Adopted', None, URL[RS]],
    [BL, 'Ordinance BL2021-829: tree protection and replacement on certain Metro department properties (Metro Code Chapter 2.226)',
     'Enacted August 17, 2021', 'Enacted', None, URL[BL]],
    [EO, 'Executive Order 41 (Amended), Mayor Freddie O\'Connell: Tree Policy on Metropolitan Government Properties',
     'Issued April 26, 2024', 'Executive order', None, URL[EO]],
]

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (RS, 'Section 1', 'highland_rim_named_place', 'definition',
     'Council recognizes the Western Highland Rim forest in Metro as "Nashville\'s Highland Rim Forest"', None, None, None, 'Metro Council',
     'That the Metropolitan County Council hereby goes on record recognizing the forested area, known as the Highland Rim Forest, in the western portion of the Metropolitan Government of Nashville and Davidson County as "Nashville\'s Highland Rim Forest."',
     'Recognition only: no boundary, map or regulatory effect. Bears on policy brief R01 (name the Forest with defined boundaries).'),
    (RS, 'Recitals', 'highland_rim_named_place', 'status_claim',
     '127,000 acres recognized by USFWS, the State and Metro plans', '127000', 'acres', None, 'Metro Council',
     'the 127,000 acres of forest and connected wildlife habitat in this Western Highland Rim area is recognized by the US Fish and Wildlife Service, the State of Tennessee, and in numerous Metro long range plans as an important ecological feature',
     None),
    (RS, 'Recitals', 'highland_rim_named_place', 'status_claim',
     'Council says the area is protected as a "Conservation Overlay" in NashvilleNext', None, None, None, 'Metro Council',
     'the conservation of this area is recognized and protected in Nashville Next\'s community policies as "Conservation Overlay;"',
     'INCONSISTENT: NashvilleNext applies Conservation (CO) policy, not an overlay, and the Community Character Manual states its policies are not regulatory (CCM Introduction p25; unchanged in the March 2026 amendment).'),
    (RS, 'Recitals', 'forest_protection', 'baseline',
     'Forest provides stormwater, air and water filtering and cooling for residents below it', None, None, None, 'Metro Council',
     'this forested area provides critical stormwater services for the majority of Metro\'s residents who live below the forest, filtering of our air and water, and helps mitigate the urban heat island effect',
     'Compare FOREST-FLOOD-CHECK.md.'),
    (BL, '2.226.010', 'tree_canopy', 'commitment',
     'Metro to lead by example: preserve canopy, pursue retention', None, None, None, 'Metro departments',
     'The Metropolitan Government will lead by example to preserve the tree canopy and pursue retention wherever possible.',
     'Applies to Metro rights-of-way and certain Metro department properties only.'),
    (BL, '2.226.060', 'tree_canopy', 'definition',
     'Tree removal review does not apply to protected natural areas in Metro Parks', None, None, None, 'Metro Parks',
     'This protocol will not apply to areas within Metro Parks that are (1) greenways or trails, (2) managed as grasslands or mixed-grass meadows, (3) areas designated as protected natural areas in the Metro Parks Natural Resource Management Plan, or (4) impacted by infrastructure maintenance or repair.',
     'Parks reports removal counts in exempt areas annually (same section). The forested natural areas most like the Highland Rim Forest are outside the review.'),
    (BL, '2.226.080', 'tree_canopy', 'commitment',
     'Metro projects: 20% higher tree density than private development', '20', 'percent', None, 'Metro Codes',
     'Metro projects having tree density requirements pursuant to Chapter 17.24 of the Metropolitan Code shall have a 20% higher tree density requirement than private development.',
     None),
    (EO, 'Order', 'tree_canopy', 'commitment',
     'Mayor reaffirms the Metro-property tree policy in Code Chapter 2.226', None, None, None, "Mayor's Office",
     'I hereby reaffirm continued support of the Tree Policy on Metropolitan Government Properties as codified in Chapter 2.226 of the Metropolitan Code of Laws.',
     'Applies to Metro properties only.'),
    (EO, 'Recitals', 'tree_canopy', 'status_claim',
     'Mayor says the 2018 tree policy objectives have been realized', None, None, None, "Mayor's Office",
     'the objectives of the Metropolitan Tree Policy, previously initiated under former Mayor Megan Barry through Executive Order No. 40, have effectively been realized by virtue of subsequent provisions enacted under Executive Orders and the Metropolitan Code of Laws.',
     'A progress claim by the Mayor\'s Office; compare the 2023 canopy assessment (net loss 2016-2021).'),
    (EO, 'Recitals', 'tree_canopy', 'commitment',
     'Canopy managed as an asset with flexibility for development', None, None, None, "Mayor's Office",
     'this utility shall be managed as an asset, with tree protection and expansion programs that also provide flexibility to ensure development can continue throughout Metropolitan Nashville and Davidson County',
     None),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‐': '-', '­': '', '_': ''})
cache = {}
def text(doc):
    if doc not in cache:
        cache[doc] = n(open(f'{WEB}/{doc}.txt', encoding='utf-8').read().translate(Q))
    return cache[doc]

wb = openpyxl.load_workbook(XLSX)
have_src = {x[0] for x in wb['Sources'].iter_rows(min_row=2, values_only=True)}
have = {(r[0], str(r[1]), n(str(r[9]))) for r in wb['Commitments'].iter_rows(min_row=2, values_only=True) if r[0]}
bad = [(r[1], r[4][:40]) for r in ROWS if n(r[9].translate(Q)) not in text(r[0])]
bad += [('dup', r[1]) for r in ROWS if (r[0], str(r[1]), n(r[9])) in have]
bad += [('source exists', s[0]) for s in SOURCES if s[0] in have_src]
print('rows', len(ROWS), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

def append(ws, rows, width):
    last = max(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value is not None)
    for k, r in enumerate(rows, 1):
        for col in range(1, width + 1):
            s, d = ws.cell(last, col), ws.cell(last + k, col)
            d.value = r[col - 1]
            d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format

full = [[*r, 'verified', URL[r[0]]] for r in ROWS]
append(wb['Commitments'], full, 13)   # columns N-P (brief_rec, brief_match, promise_id) stay empty
append(wb['Highland Rim & named places'], [r for r in full if r[2] == 'highland_rim_named_place'], 12)
append(wb['Inconsistencies'], [r for r in full if 'INCONSISTENT' in (r[10] or '')], 12)

ws = wb['Sources']
total_r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'Total')
tail = [[(c.value, c._style) for c in ws[r]] for r in range(total_r, ws.max_row + 1)]
style = [c._style for c in ws[total_r - 1]]
for i, s in enumerate(SOURCES):
    vals = s + [f'=COUNTIF(Commitments!$A:$A,A{total_r + i})', 'yes', None]
    for col, v in enumerate(vals, 1):
        ws.cell(total_r + i, col).value = v
        ws.cell(total_r + i, col)._style = copy(style[col - 1])
for i, cells in enumerate(tail):
    for col, (v, st) in enumerate(cells, 1):
        c = ws.cell(total_r + len(SOURCES) + i, col)
        c.value, c._style = v, copy(st)
ws.cell(total_r + len(SOURCES), 7).value = f'=SUM(G2:G{total_r + len(SOURCES) - 1})'
wb.save(XLSX)

def dump(name, path, skip_blank):
    rows = [['' if v is None else v for v in r] for r in wb[name].iter_rows(values_only=True)]
    if skip_blank:
        rows = [r for r in rows if any(x != '' for x in r)]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
dump('Commitments', f'{CDIR}/commitments.csv', False)
dump('Highland Rim & named places', f'{CDIR}/highland_rim.csv', False)
dump('Inconsistencies', f'{CDIR}/inconsistencies.csv', False)
dump('Sources', f'{CDIR}/sources.csv', True)
print('written')
