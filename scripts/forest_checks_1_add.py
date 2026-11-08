"""Forest promise checks, round 1: evidence sources, rows and Promised_vs_Delivered pairs 23 to 27.

Usage: python3 forest_checks_1_add.py <joelton.pdf> <ecs.html> <commitments_dir> [--write]
  joelton.pdf: https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/CommPlans2017/next-vol3-Joelton_Amended2017.pdf
  ecs.html:    https://engage.nashville.gov/w12375 saved as HTML
Metro Code excerpts were matched against Municode page text in a browser on 2026-10-22
(Municode serves no static HTML), so the script trusts them. Joelton and ECS excerpts are
rechecked here; the script exits without writing on any miss. After --write, run
apply_pvd_to_xlsx.py, then forest_priorities.py --write, then cover_sheet.py.
"""
import csv, html, re, subprocess, sys
import openpyxl
from copy import copy

JOELTON, ECS_HTML, CDIR = sys.argv[1:4]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'

C65, C440, JOE, ECS = 'Metro_Code_17.28.065', 'Metro_Code_17.40.440', 'NashvilleNext_Vol3_Joelton_2017', 'Ecological_Conservation_Strategy_2026'
URL = {
    C65: 'https://library.municode.com/tn/metro_government_of_nashville_and_davidson_county/codes/code_of_ordinances?nodeId=CD_TIT17ZO_CH17.28ENOPPEST',
    C440: 'https://library.municode.com/tn/metro_government_of_nashville_and_davidson_county/codes/code_of_ordinances?nodeId=CD_TIT17ZO_CH17.40ADPR_ARTXTRPRREPR_17.40.470TRREPEPR',
    JOE: 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/CommPlans2017/next-vol3-Joelton_Amended2017.pdf',
    ECS: 'https://engage.nashville.gov/w12375',
}
SOURCES = [
    [C65, 'Metro Code of Laws 17.28.065, Trees (protected and heritage trees, tree preservation, tree density, protection during development)',
     'Read on Municode October 22, 2026; created by BL2022-1122 (2022), amended by BL2024-687 (2025)', 'In force (current codified text)', None, URL[C65]],
    [C440, 'Metro Code of Laws 17.40.440, Tree Protection and Replacement Procedures: General (tree removal permit)',
     'Read on Municode October 22, 2026; last amended by BL2022-1122 (2022)', 'In force (current codified text)', None, URL[C440]],
    [JOE, 'NashvilleNext Volume III Community Plans: Joelton', 'Adopted June 22, 2015; amended August 24, 2017', 'Adopted', 25, URL[JOE]],
    [ECS, 'Davidson County Ecological Conservation Strategy, project page (Metro Planning)', 'Launched March 2026; read October 22, 2026',
     'In progress (expected fall 2027)', None, URL[ECS]],
]

CODE_NOTE = ' Matched against Municode page text 2026-10-22.'
# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (C65, '17.28.065.B.1', 'tree_canopy', 'definition', 'Tree preservation intent: minimize tree removal in development', None, None, None, 'Metro Codes; Metro Planning',
     'It is the intent of this section to minimize the removal of trees and to ensure that property owners and developers take reasonable measures to design and locate the proposed improvements so that the number of trees to be removed is minimized.',
     '"Minimize", not a limit. Created by BL2022-1122 (2022).' + CODE_NOTE),
    (C65, '17.28.065.C.3.b.i', 'tree_canopy', 'definition', 'Tree density for new single and two-family subdivisions', '14', 'tree density units per acre', '2022', 'Metro Planning',
     'Property within a single and/or two-family residential subdivision for which the preliminary site plan is filed with the planning commission after the date of enactment of this subsection shall attain a tree density factor of at least fourteen units per acre using retained or replacement trees, or a combination of both, excluding the area of the building lots.',
     'Other property: 22 units per acre (C.3.a). Applies to new subdivisions, excluding building lots; retained or planted trees both count.' + CODE_NOTE),
    (C65, '17.28.065.C.3.b.ii', 'tree_canopy', 'definition', 'Street-frontage trees on new single and two-family lots (AG and AR2a exempt)', '1', 'tree per 30 ft of frontage', None, 'Metro Codes',
     'Individual single and two-family lots, other than those lots zoned AG or AR2a, shall include at least one two-inch caliper tree for each thirty feet of lot frontage (or portion thereof), excluding alley frontage.',
     'Planting rule, checked before a certificate of occupancy. AG and AR2a, the rural zones, are exempt.' + CODE_NOTE),
    (C65, 'history note', 'tree_canopy', 'status_claim', 'Tree section enacted 2022, amended 2025', None, None, '2022', 'Metro Council',
     '(Amdt. 1 to Ord. BL2024-687 § 2, 2025; Ord. BL2024-687 § 2, 2025; Ord. BL2022-1122 § 11, 2022)',
     'Answers NashvilleNext #201 (residential tree ordinance, preservation policy) about four years after its 2018 near-term date. See promised_vs_delivered pair 23.' + CODE_NOTE),
    (C440, '17.40.440', 'tree_canopy', 'definition', 'Permit required to remove a retained, protected or heritage tree, unless exempt', None, None, None, 'Zoning Administrator',
     'Unless exempt from the provisions of this chapter, no person shall remove or in any way damage any retained, protected or heritage tree without first obtaining a permit from the zoning administrator.',
     'Removal criteria (17.40.470.B) include that the site has received development, site plan or subdivision approval. Whether existing single-family lots outside development need a permit was not settled from the code text read; a 2004 amendment (BL2004-371) had exempted residential property.' + CODE_NOTE),
    (JOE, 16, 'highland_rim_named_place', 'status_claim', 'T2 Rural Countryside policy applied to southeast Joelton', None, None, '2017', 'Metro Planning',
     'Application of T2 Rural Countryside (T2-RCS) policy to southeast Joelton encourages maintenance of rural landscapes.',
     'Community plan amended August 24, 2017. Answers NashvilleNext #323 for Joelton; see pair 24.'),
    (JOE, 17, 'highland_rim_named_place', 'status_claim', 'T2 Rural Maintenance policy applied to most of Joelton', None, None, '2017', 'Metro Planning',
     'T2 Rural Maintenance (T2-RM) policy is applied to a large swath of the remainder of the community, which is also intended to preserve the character of rural neighborhoods.',
     'T2-RM intends that sewer service and higher-density zoning not be expanded (CCM T2 rows). Whether sewer lines were actually extended in Joelton since 2017 is not reported.'),
    (ECS, 'web', 'highland_rim_named_place', 'baseline', 'Metro: Highland Rim Forest is the most ecologically significant natural area in the county', None, None, None, 'Metro Planning',
     'the Highland Rim Forest in western Davidson County—the most ecologically significant natural area in the county',
     'One of two ECS pilot studies; the other is the Cumberland River waterfront downtown.'),
    (ECS, 'web', 'habitat_natural_area', 'status_claim', 'Ecological Conservation Strategy expected fall 2027', None, None, '2027', 'Metro Planning',
     'The project is expected to be completed by fall 2027.',
     '18-month effort led by Metro Planning with Biohabitats; launched March 2026. Metro calls it the first countywide ecological planning effort since the 2011 Open Space Plan. Closest match to NashvilleNext #119 (define ecologically valuable lands); see pair 25.'),
]

PAIRS = [
    ['23', 'Tree protection', 'NashvilleNext_Vol4_Actions', '72',
     'NR 1.4 #201: Create a street tree policy, residential tree ordinance, maintenance program, and preservation policy; implement and regularly update the Urban Forestry and Landscape Plan.',
     '', '', '2018', C65, '17.28.065.B.1; C.3.b',
     'BL2022-1122 (2022) created Metro Code 17.28.065: an intent to minimize tree removal, tree density of 14 units per acre for new single and two-family subdivisions, and street-frontage trees on new lots. Amended by BL2024-687 (2025).',
     '', '', 'Partly met',
     'Near term (1-3 years) from 2015, so due 2018; enacted 2022. The rules apply when land is developed; they set density with retained or planted trees and say "minimize", so they do not stop clearing of existing forest. Rural AG and AR2a lots are exempt from the frontage rule. The Urban Forestry and Landscape Plan (2016) has not been updated in any document here. Street tree policy and maintenance program not assessed.'],
    ['24', 'Rural policy and sewer', 'NashvilleNext_Vol4_Actions', '49; 79',
     'BE 1.1 / NR 4.2 #323: Update areas to new Rural Community Character Manual policies that guide a reduction in development and discourage the expansion of sewer infrastructure.',
     '', '', '2018', JOE, '16; 17',
     'Joelton community plan, amended August 24, 2017, applies T2 Rural Countryside to southeast Joelton and T2 Rural Maintenance to most of the rest.',
     '', '', 'Partly met',
     'Policy mapping done on time for Joelton (2017). Rural Character Subdivision rules were added to the Subdivision Regulations around 2016 [not read here]. No document reports whether sewer extensions into T2 areas were limited, which is the outcome the action names. Other Highland Rim community plans (Bordeaux-Whites Creek, Bellevue, West Nashville) not yet checked.'],
    ['25', 'Ecologically valuable lands', 'NashvilleNext_Vol4_Actions', '71',
     'NR 1.2 #119: Research methods to define and identify ecologically valuable lands, and recommend an in-lieu fee to fund a land bank where permanent protection cannot be accomplished.',
     '', '', '2025', ECS, 'web',
     'Ecological Conservation Strategy launched March 2026, expected fall 2027. No in-lieu fee or land bank for ecologically valuable land found.',
     '', '', 'Not met',
     'Long term (7-10 years) from 2015, so due by 2025. The strategy may define ecologically valuable land about two years late; Metro itself calls it the first countywide ecological plan since 2011. The tree bank (tree replacement fees) and the Conservation Assistance Grant Fund are different tools. Searches found no land bank; a records request would settle it.'],
    ['26', 'Regional watershed conservation', 'NashvilleNext_Vol4_Actions', '78',
     'NR 4.1 #148: Identify risks to upstream landscapes and contribute to joint regional efforts to mitigate them with land conservation, source water protection, hazard reduction and floodplain management.',
     '', '', '2021', '', '',
     'No joint regional land conservation effort for upstream watersheds found in any document here or in web searches.',
     '', '', 'No status reported',
     'Mid term (4-6 years) from 2015, so due by 2021. Named partners: Cumberland Region Tomorrow, Nashville Area MPO, Cumberland River Compact, TDEC, adjacent counties. A negative finding from searches, not proof of absence.'],
    ['27', 'Tree canopy', 'Livable_Nashville_2017_DRAFT', '12',
     'Stop net tree-loss by 2020.', '0', 'net tree loss (acres)', '2020', 'Urban_Tree_Canopy_Assessment_2023', '13; 14',
     'Davidson County lost just over 900 acres of canopy from 2016 to 2021 (-0.3%). The Urban Services District lost 1,841 acres; the rural General Services District gained.',
     '-900', '', 'Not met',
     'Livable Nashville is a draft; the goal was repeated in later plans (Forest_Priorities family F08). pct_delivered left blank because the target is zero. Net loss fell in the urban district while rural canopy grew.'],
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
QUOTES = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '—': '-', '–': '-'})
def joelton(p):
    return n(subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), JOELTON, '-'], capture_output=True, text=True).stdout.translate(QUOTES))
ecs_text = n(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?s)<(script|style).*?</\1>', '', open(ECS_HTML, encoding='utf-8', errors='replace').read()))).translate(QUOTES))

bad = []
for doc, page, *_, ex, note in ROWS:
    e = n(ex.translate(QUOTES))
    if doc == JOE and e not in joelton(page):
        bad.append((doc, page))
    if doc == ECS and e not in ecs_text:
        bad.append((doc, ex[:40]))
wb = openpyxl.load_workbook(XLSX)
have = {r[0] for r in wb['Sources'].iter_rows(min_row=2, values_only=True)}
bad += [('source exists', d) for d in URL if d in have]
pvd = list(csv.reader(open(f'{CDIR}/promised_vs_delivered.csv', encoding='utf-8')))
bad += [('pair exists', p[0]) for p in PAIRS if p[0] in {r[0] for r in pvd}]
print('rows', len(ROWS), 'pairs', len(PAIRS), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

def append(ws, rows, width):
    last = ws.max_row
    for r in rows:
        ws.append(r[:width])
        for col in range(1, width + 1):
            s, d = ws.cell(last, col), ws.cell(ws.max_row, col)
            d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format

full = [[*r, 'verified', URL[r[0]]] for r in ROWS]
append(wb['Commitments'], full, 13)
append(wb['Highland Rim & named places'], [r for r in full if r[2] == 'highland_rim_named_place'], 12)

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
dump('Sources', f'{CDIR}/sources.csv', True)

# Pairs go into the CSV before its trailing note row; apply_pvd_to_xlsx.py then syncs the tab.
note = pvd[-1]
with open(f'{CDIR}/promised_vs_delivered.csv', 'w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows(pvd[:-1] + PAIRS + [note])
print('written')
