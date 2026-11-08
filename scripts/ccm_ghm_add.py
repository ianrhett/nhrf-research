"""Add NashvilleNext Volume III Character Manual parts (Introduction and General Principles, T1 Natural,
T3 Suburban; amended 2017) and the Green Hills-Midtown community plan (2017) as sources with rows.

Usage: python3 ccm_ghm_add.py <pdf_dir> <commitments_dir> [--write]
pdf_dir holds the official PDFs under the FILE names below (downloaded 2026-10-22 from URL; the
operator's local Intro and T3 copies are byte-identical). Candidates came from find_candidates.py and
were selected by reading; every excerpt is rechecked against its page and the script exits without
writing on any miss or duplicate. After --write: forest_priorities.py --write, cover_sheet.py.
"""
import csv, re, subprocess, sys
import openpyxl
from copy import copy

PDF_DIR, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
I, T1, T3, GH = ('NashvilleNext_Vol3_CCM_Intro_2017', 'NashvilleNext_Vol3_CCM_T1_Natural_2017',
                 'NashvilleNext_Vol3_CCM_T3_Suburban_2017', 'NashvilleNext_Vol3_Green_Hills_Midtown_2017')
B = 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/CCM/2017Adopted/'
FILE = {I: 'next_vol3_CCM-Intro_Amended2017.pdf', T1: 'next_vol3_CCM-T1_Amended2017.pdf', T3: 'next_vol3_CCM-T3_Amended2017.pdf', GH: 'ghm.pdf'}
URL = {I: B + FILE[I], T1: B + FILE[T1], T3: B + FILE[T3],
       GH: 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/CommPlans2017/next-vol3-Green%20Hills-Midtown_Amended2017.pdf'}
V = 'Adopted June 22, 2015; amended August 24, 2017'
SOURCES = [
    [I, 'NashvilleNext Volume III Community Character Manual: Introduction and General Principles', V, 'Adopted', 62, URL[I]],
    [T1, 'NashvilleNext Volume III Community Character Manual: T1 Natural Transect policy', V, 'Adopted', 8, URL[T1]],
    [T3, 'NashvilleNext Volume III Community Character Manual: T3 Suburban Transect policies', V, 'Adopted', 44, URL[T3]],
    [GH, 'NashvilleNext Volume III Community Plans: Green Hills-Midtown', V, 'Adopted', 35, URL[GH]],
]
FLOOD = 'Same headwaters-and-flooding language as the Joelton, Bellevue, West Nashville and Bordeaux-Whites Creek plans (COMMUNITY-PLANS-RIM.md).'

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (I, 25, 'policy_mechanism', 'definition', 'Character policies are not regulatory', None, None, None, 'Metro Planning',
     'Given that the Community Character Policies are not regulatory',
     'Sentence continues: the policies "do not use verbs such as \"shall\"". Policies guide discretionary decisions (rezonings, plan amendments); they do not bind uses already allowed by zoning. This is why T2 and Conservation policy cannot by themselves stop development or a sewer extension on land already zoned for it.'),
    (I, 41, 'forest_protection', 'baseline', 'Developed habitats and land forms cannot be returned to nature', None, None, None, None,
     'Habitats, waterways, and land forms-once developed-are difficult, if not impossible, to return to the natural form.', None),
    (I, 50, 'forest_protection', 'baseline', 'Steep slopes, floodplains and unstable soils can be harmed by development', None, None, None, None,
     'Many of these environmentally sensitive features-steep slopes, floodways, floodplains, and unstable and problem soils -can be harmed by development.', None),
    (I, 50, 'policy_mechanism', 'definition', 'Conservation Policy is the tool for preserving natural resources', None, None, None, 'Metro Planning',
     'is achieved, in the CCM, through the use of Conservation Policy.', 'Subject: "The conservation, preservation, and in some cases remediation of natural resources".'),
    (I, 54, 'forest_protection', 'recommendation', 'Sustainable sites avoid steep slopes and large stands of mature trees', None, None, None, None,
     'Avoids sensitive environmental features or populations, such as endangered or imperiled species, ecological communities, wetlands or bodies of water, floodplain, steep slopes, prime farmland, large stands of mature trees,or unstable soils.',
     'General Principles, sustainable site location.'),
    (I, 55, 'land_acquisition', 'recommendation', 'Protect sensitive features permanently with easements or development rights transfer', None, None, None, None,
     'permanently protecting sensitive features by using conservation easements, transfer of development rights, or other tools.', None),
    (T1, 5, 'forest_protection', 'commitment', 'T1 Natural intent: keep undisturbed open space undeveloped', None, None, None, 'Metro Planning',
     'Preserve existing undisturbed open space in natural areas to remain undeveloped.', 'Policy intent of T1 Natural.'),
    (T1, 1, 'land_acquisition', 'definition', 'T1 Natural can include private land under conservation easement', None, None, None, None,
     'T1 Natural may also include privately owned land that is permanently protected by conservation easements or other tools and remains in a natural, undeveloped state.', None),
    (T1, 6, 'forest_protection', 'definition', 'T1 buildings kept off ridgelines, below the tree canopy', None, None, None, None,
     'Buildings are not generally located on ridgelines or hilltops; but if this provides the optimum site, their rooflines are below the height of the existing tree canopy.', None),
    (T3, 1, 'tree_canopy', 'recommendation', 'Suburban development keeps existing vegetation and land forms', None, None, None, None,
     'The form of development should emulate the classic suburban model, preserving the natural environment by incorporating existing vegetation and land forms into the site design.', None),
    (T3, 3, 'forest_protection', 'definition', 'New buildings in undisturbed Conservation areas within T3 are inappropriate', None, None, None, 'Metro Planning',
     'Construction of new buildings in undisturbed CO areas within T3 is inappropriate unless the site in question cannot be developed at all without some disturbance',
     'Most Rim-edge development is T3 Suburban. "Inappropriate" is policy language, not a prohibition (see Intro p25).'),
    (T3, 18, 'tree_canopy', 'recommendation', 'Retain clusters of mature trees in suburban neighborhoods', None, None, None, None,
     'Existing vegetation should be retained to preserve the randomly spaced clusters of mature trees like those found in classic suburbs and to provide air and water quality protection.', None),
    (T3, 19, 'forest_protection', 'definition', 'Lower density on environmentally constrained parts of a site', None, None, None, 'Metro Planning',
     'In the event that new construction is supported, the density or intensity of development for the environmentally constrained portions of a site is lower than for the more developable portion of a site', None),
    (T3, 20, 'policy_mechanism', 'definition', 'Feasibility of extending roads and sewers considered near Conservation policy', None, None, None, 'Metro Planning',
     'The adequacy of the infrastructure (including, but not limited to, roads and sewers) and the feasibility of extending infrastructure are also considered with development of property with or adjacent to CO policy.', None),
    (GH, 8, 'forest_protection', 'baseline', 'Southern third of Green Hills-Midtown: steep slopes and woods', None, None, None, None,
     'steep slopes, wooded areas, streams and creeks - that exist throughout the southern third of Green Hills- Midtown and add to its natural, semi-rural beauty.', None),
    (GH, 13, 'forest_protection', 'baseline', 'Forest cover stabilizes slopes and absorbs runoff (Green Hills-Midtown)', None, None, None, None,
     'In addition to stabilizing steep slopes, forest cover also aids in absorbing water run-off and provides crucial wildlife habitat and wildlife corridors.', 'Same page: steep-slope soils "are stabilized by tree cover".'),
    (GH, 16, 'highland_rim_named_place', 'baseline', 'Large steep areas in Forest Hills and Oak Hill', None, None, None, None,
     'Large areas of steeply sloping terrain are found in Forest Hills and Oak Hill.', 'Satellite cities with their own zoning.'),
    (GH, 21, 'highland_rim_named_place', 'definition', 'T1 Natural: Percy Warner Park and Radnor Lake', None, None, None, 'Metro Planning',
     'T1 Natural: Includes Percy Warner Park and Radnor Lake State Natural Area.', 'The Open Space Plan southwest anchor (Commitments row 667).'),
    (GH, 22, 'forest_protection', 'baseline', 'Steep-slope headwaters (Green Hills-Midtown)', None, None, None, 'Metro Planning',
     'Research has shown that the headwaters of many streams and tributaries to the Cumberland River lie in these steep slopes.',
     'Next page: "Preservation of these areas can reduce the impact of flooding in the future". ' + FLOOD),
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
