"""Add NashvilleNext Volume I (four parts, 2017) and the Volume II Land Use, Transportation & Infrastructure
element (2015) as sources with Forest-related rows.

Usage: python3 nn_vol1_luti_add.py <pdf_dir> <commitments_dir> [--write]
pdf_dir holds the official PDFs under the FILE names below (downloaded 2026-10-22 from URL).
Candidates came from find_candidates.py and were selected by reading; every excerpt is rechecked
against its PDF page (with and without line-break hyphens joined) and the script exits without
writing on any miss or duplicate. After --write: forest_priorities.py --write, cover_sheet.py.
"""
import csv, re, subprocess, sys
import openpyxl
from copy import copy

PDF_DIR, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
A, E, F, G, L = ('NashvilleNext_Vol1_ABCD_Intro_2017', 'NashvilleNext_Vol1_E_Key_Issues_2017', 'NashvilleNext_Vol1_F_Guiding_Principles_2017',
                 'NashvilleNext_Vol1_GH_Strategy_Implementation_2017', 'NashvilleNext_Vol2_Land_Use_Transportation_Infrastructure')
B = 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/NashvilleNext/2017Update/'
FILE = {A: 'next-volume1-ABCD-IntroWhyPlan_Amended2017.pdf', E: 'next-volume1-E-KeyIssues_Amended2017.pdf',
        F: 'next-volume1-F-Guiding_Principles_Amended2017.pdf', G: 'next-volume1-GH-StrategyImplementation_Amended2017.pdf', L: 'luti.pdf'}
URL = {A: B + 'next-volume1-ABCD-IntroWhyPlan_Amended2017.pdf', E: B + 'next-volume1-E-KeyIssues_Amended2017.pdf',
       F: B + 'next-volume1-F-Guiding%20Principles_Amended2017.pdf', G: B + 'next-volume1-GH-StrategyImplementation_Amended2017.pdf',
       L: 'https://www.nashville.gov/sites/default/files/2025-09/next-volume2-Elements_LUTI.pdf'}
V1 = 'Adopted June 22, 2015; amended August 24, 2017'
SOURCES = [
    [A, 'NashvilleNext Volume I: Vision, Trends & Strategy, parts A-D (introduction, role of the plan, community engagement)', V1, 'Adopted', 55, URL[A]],
    [E, 'NashvilleNext Volume I: Vision, Trends & Strategy, part E (key issues and trends)', V1, 'Adopted', 66, URL[E]],
    [F, 'NashvilleNext Volume I: Vision, Trends & Strategy, part F (guiding principles)', V1, 'Adopted', 16, URL[F]],
    [G, 'NashvilleNext Volume I: Vision, Trends & Strategy, parts G-H (strategy and implementation)', V1, 'Adopted', 68, URL[G]],
    [L, 'NashvilleNext Volume II Elements: Land Use, Transportation & Infrastructure', 'Adopted June 22, 2015', 'Adopted', 66, URL[L]],
]
FLOOD = 'Compare FOREST-FLOOD-CHECK.md: the 2026 hazard and 2024 climate plans do not act on existing forest.'
SEWER = 'Sewer limits for rural land also in NashvilleNext #323 (pair 24), Guiding Principles p10 and Land Use p58 and p60. Whether sewer lines were kept out of T2 areas is not reported in any document here; Metro Water Services records would settle it.'

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (A, 22, 'open_space', 'commitment', 'Plans to protect natural resources, farmland and outdoor spaces', None, None, None, None,
     'As demand for our open spaces and natural resources grows, it is more important than ever that we have plans in place to protect the air we breathe, the water we drink, the farmlands that sustain us, and the outdoor spaces our families enjoy.', None),
    (A, 24, 'forest_protection', 'commitment', "NashvilleNext approach: protect the county's remaining natural and rural areas", None, None, None, None,
     "Protect Davidson County's remaining natural and rural areas", 'First item in "The NashvilleNext Approach".'),
    (A, 25, 'forest_protection', 'commitment', 'Infill first, to preserve remaining natural and rural areas', None, None, None, None,
     "Giving priority to infill development allows us to preserve more of Nashville's remaining natural and rural areas.", None),
    (A, 25, 'forest_protection', 'commitment', 'Reduce development on steep slopes and floodplains', None, None, None, None,
     'Reducing development on sensitive features like steep slopes and floodplains minimizes hazards to life and property.',
     'The zoning code still starts residential slope limits at 20% and exempts lots of an acre or more (pair 21).'),
    (E, 43, 'land_acquisition', 'status_claim', 'Greenway goal exceeded; parkland progress "steady"', '14000', 'acres (2015)', '2021', 'Metro Parks',
     'Metro has exceeded the goal for greenways and is making steady progress on the goal for parkland.',
     'Chart on the page: 11,000 acres (2011), 14,000 (2015), 21,000 target (2021); greenways 45 miles (2011), 80 (2015), 70 target. The 21,000 target differs from the Open Space Plan 22,000 by 2035 (Inconsistencies tab).'),
    (E, 66, 'forest_protection', 'baseline', 'Climate change: oaks likely replaced by hickories', None, None, None, None,
     'Oaks and other commercially important species will likely be replaced by hickories and other less valuable trees.', None),
    (F, 10, 'policy_mechanism', 'commitment', 'Direct sewer to suburban and urban areas to keep rural areas rural', None, None, None, None,
     'Direct sewer service to suburban and urban communities to maintain rural areas as a viable lifestyle choice.', SEWER),
    (F, 14, 'land_acquisition', 'commitment', 'Increase funding for buying and preserving land', None, None, None, None,
     'Increase funding and expand the purchase and preservation of land for public recreation and open space.', None),
    (F, 14, 'forest_protection', 'commitment', 'More complete regulations to protect sensitive environmental resources', None, None, None, None,
     "Expand programs and institute more complete regulations to protect Nashville's sensitive environmental resources.", None),
    (G, 2, 'forest_protection', 'baseline', "Preserving natural areas keeps people out of harm's way in floods and slope failures", None, None, None, None,
     "Preserving these areas keeps us out of harm's way when rivers flood and slopes erode.", FLOOD),
    (G, 17, 'forest_protection', 'definition', 'Green Network includes floodplains and steep slopes with unstable soils', None, None, None, 'Metro Planning',
     'They also include sensitive natural features that can be disturbed or destroyed by development or that pose a health or safety risk when developed (such as floodplains and steep slopes with unstable soils).', None),
    (G, 54, 'forest_protection', 'baseline', '2010 flood: floodplains and tree cover kept damage from being worse', None, None, '2010', None,
     "yet the city's natural features-such as floodplains and tree cover-ensured that the damage and loss of life and property was not worse.", FLOOD),
    (L, 10, 'forest_protection', 'baseline', 'Tree canopy and native vegetation infiltrate stormwater', None, None, None, None,
     'open space, tree canopy, and native vegetation all help to manage stormwater by infiltrating it into the ground.', FLOOD),
    (L, 15, 'tree_canopy', 'baseline', '2010 Tree Inventory: 47% of the county shaded by trees', '47', 'percent', '2010', None,
     'The 2010 Tree Inventory found 47 percent of Davidson County was shaded by trees.',
     'INCONSISTENT: the 2023 Urban Tree Canopy Assessment gives 55% for 2010 (p13, Table 4); the 2016 Urban Forestry plan also cites 47%. Method and boundary differ.'),
    (L, 15, 'tree_canopy', 'baseline', '2010: another 35% of the county could hold trees', '35', 'percent', '2010', None,
     'The Inventory also found that another 35 percent of the county had potential for trees.', None),
    (L, 37, 'highland_rim_named_place', 'baseline', 'Hills of Joelton and the Warner Parks: places vanished from other cities', None, None, None, None,
     'From the bends of the Cumberland to the hills of Joelton and the Warner Parks, Nashville contains the kinds of places that have vanished from most other major cities.', None),
    (L, 37, 'forest_protection', 'commitment', 'Green Network marks what should remain natural or rural', None, None, None, 'Metro Planning',
     "These features frame Nashville's future by identifying what parts of the county should remain natural or rural.",
     'Applied through Conservation policy in community plans (same page); Vol I parts G-H p17 repeats it.'),
    (L, 37, 'forest_protection', 'commitment', 'Prevent or reduce development on or near Green Network features', None, None, None, None,
     "We prevent or reduce development on or near them because it places people and property in harm's way.", 'Features named: parks, rural areas, floodplains and steep slopes.'),
    (L, 43, 'forest_protection', 'baseline', 'Growth in centers reduces clearing at the edge of the city', None, None, None, None,
     'encouraging growth in dense, walkable centers reduces the need for clearing and building on undeveloped land at the edge of the city.', None),
    (L, 58, 'policy_mechanism', 'commitment', 'Limit sewer access in rural areas', None, None, None, 'Metro Water Services',
     'Limiting sewer access in rural areas will help preserve their undeveloped character.', SEWER),
    (L, 59, 'forest_protection', 'baseline', 'Natural areas soak rainwater, reducing flooding', None, None, None, None,
     'Natural areas soak rainwater into the ground, reducing flooding and keeping streams and creeks healthy.', FLOOD),
    (L, 60, 'policy_mechanism', 'commitment', 'LUTI 9.4: limit sewer extensions into T2 Rural areas', None, None, None, 'Metro Water Services; Metro Planning',
     'LUTI Policy 9.4 Limit sewer extensions and expansions into areas identified as T2 Rural Agriculture, Countryside, or Maintenance on Community Character Policy maps.', SEWER),
    (L, 65, 'habitat_natural_area', 'status_claim', 'Regional linking of green spaces still needed', None, None, None, None,
     'Progress has been made in preserving natural features across the region, but more steps-including linking green spaces across the region-are needed.',
     'Bears on NashvilleNext #148 (pair 26).'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‐': '-', '­': ''})
cache = {}
def variants(doc, p):
    if (doc, p) not in cache:
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), f'{PDF_DIR}/{FILE[doc]}', '-'], capture_output=True, text=True).stdout.translate(Q)
        cache[(doc, p)] = [n(t), n(re.sub(r'(\w)-\n(\w)', r'\1\2', t)), n(re.sub(r'-\n', '-', t))]
    return cache[(doc, p)]

wb = openpyxl.load_workbook(XLSX)
have_src = {x[0] for x in wb['Sources'].iter_rows(min_row=2, values_only=True)}
bad = [(r[0][13:30], r[1], r[4][:40]) for r in ROWS if not any(n(r[9].translate(Q)) in v for v in variants(r[0], r[1]))]
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
append(wb['Commitments'], full, 13)
append(wb['Highland Rim & named places'], [r for r in full if r[2] == 'highland_rim_named_place'], 12)
append(wb['Inconsistencies'], [r for r in full if 'INCONSISTENT' in (r[10] or '')], 12)

ws = wb['Sources']
total_r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'Total')
tail = [[(c.value, c._style) for c in ws[r]] for r in range(total_r, ws.max_row + 1)]
style = [c._style for c in ws[total_r - 1]]
for i, s in enumerate(SOURCES):
    for col, v in enumerate(s + [f'=COUNTIF(Commitments!$A:$A,A{total_r + i})'], 1):
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
