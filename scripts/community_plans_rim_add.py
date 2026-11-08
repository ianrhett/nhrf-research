"""Add the four Highland Rim community plans (NashvilleNext Vol III, 2017): sources and rows.

Usage: python3 community_plans_rim_add.py <pdf_dir> <commitments_dir> [--write]
pdf_dir holds joelton.pdf, bellevue.pdf, west_nashville.pdf, bordeaux.pdf, each byte-identical to the
official file at its URL below (checked 2026-10-22). Every excerpt is rechecked against its PDF page,
with and without line-break hyphens joined, and the script exits without writing on any miss or
duplicate. After --write: apply_pvd_to_xlsx.py, forest_priorities.py --write, cover_sheet.py.
"""
import csv, re, subprocess, sys
import openpyxl
from copy import copy

PDF_DIR, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'

JOE, BEL, WN, BX = ('NashvilleNext_Vol3_Joelton_2017', 'NashvilleNext_Vol3_Bellevue_2017',
                    'NashvilleNext_Vol3_West_Nashville_2017', 'NashvilleNext_Vol3_Bordeaux_Whites_Creek_Haynes_Trinity')
FILE = {JOE: 'joelton.pdf', BEL: 'bellevue.pdf', WN: 'west_nashville.pdf', BX: 'bordeaux.pdf'}
URL = {
    JOE: 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/CommPlans2017/next-vol3-Joelton_Amended2017.pdf',
    BEL: 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/CommPlans2017/next-vol3-Bellevue_Amended2017.pdf',
    WN: 'https://filetransfer.nashville.gov/portals/0/sitecontent/Planning/docs/CommPlans2017/next-vol3-West%20Nashville_Amended2017.pdf',
    BX: 'https://www.nashville.gov/sites/default/files/2025-10/Bordeaux-Whites-Creek-Haynes-Trinity_Adopted_and_Updated.pdf',
}
SOURCES = [
    [BEL, 'NashvilleNext Volume III Community Plans: Bellevue', 'Adopted June 22, 2015; amended August 24, 2017', 'Adopted', 33, URL[BEL]],
    [WN, 'NashvilleNext Volume III Community Plans: West Nashville', 'Adopted June 22, 2015; amended August 24, 2017', 'Adopted', 41, URL[WN]],
    [BX, 'NashvilleNext Volume III Community Plans: Bordeaux-Whites Creek-Haynes Trinity (adopted and updated; includes the Haynes Trinity Small Area Plan)',
     'Updated 2017; Haynes Trinity maps dated December 27, 2017; PDF created February 14, 2018',
     'Adopted and updated (inner pages still marked DRAFT)', 64, URL[BX]],
]
FLOOD = 'Same headwaters-and-flooding language appears in the Joelton, Bellevue, West Nashville and Bordeaux-Whites Creek plans. Compare FOREST-FLOOD-CHECK.md: the 2026 hazard and 2024 climate plans do not act on existing forest.'

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (JOE, 7, 'highland_rim_named_place', 'baseline', 'Joelton planning area size', '39.6', 'square miles', None, None,
     'Containing approximately 39.6 acres square miles, Joelton represents seven percent of all land in Metro.',
     '"acres square miles" as printed. Metro GIS gives 25,313 acres (39.55 sq mi) for the Community Planning Area.'),
    (JOE, 9, 'tree_canopy', 'baseline', 'Joelton has the highest canopy of the 14 planning areas', None, None, None, None,
     "With the highest percentage of tree canopy coverage of all of Nashville's 14 community planning areas, Joelton helps clean the region's air and reduce its heat island effect.",
     'Metro 2021 canopy layer clipped to Joelton: 81% canopy (scratch analysis 2026-10-22).'),
    (JOE, 9, 'forest_protection', 'baseline', "Joelton's forest soaks rainwater into the ground for Marrowbone and Whites Creeks", None, None, None, None,
     "Joelton's forested land also helps to soak rainwater into the ground, supporting the health of Marrowbone and Whites Creeks.", FLOOD),
    (JOE, 9, 'highland_rim_named_place', 'baseline', 'Joelton is on the Highland Rim', None, None, None, None,
     'Joelton is located on the Highland Rim and its Appalachian topography and soil characteristics resemble those of the Cumberland Plateau.',
     '99% of Joelton lies in EPA ecoregion 71f, Western Highland Rim (scratch analysis 2026-10-22).'),
    (JOE, 9, 'forest_protection', 'baseline', 'Southern Joelton: heavily forested steep slopes, ridges and valleys', '20', 'percent slope (definition)', None, None,
     'In the southern area of the community, heavily forested steep slopes',
     'Northern Joelton is "level to rolling land" (same page).'),
    (JOE, 12, 'forest_protection', 'definition', 'Most of Joelton is in the Green Network of steep slopes and woodlands', None, None, None, None,
     "Much of Joelton is in the Concept Map's Green Network. This area is contiguous steep slopes, woodlands, floodways and floodplains.", None),
    (JOE, 15, 'highland_rim_named_place', 'definition', 'Most of Joelton is in the T2 Rural transect', None, None, None, 'Metro Planning',
     'T2 Rural: includes most of Joelton.', 'No T1 Natural, T3 Suburban or more intense transect in Joelton.'),
    (JOE, 16, 'forest_protection', 'recommendation', 'Conservation policy on Joelton floodplains, floodways and steep slopes', None, None, None, 'Metro Planning',
     'Application of Conservation (CO) policy to these areas encourages the preservation of all environmentally sensitive features - particularly floodplains, floodways, and steep slopes.',
     '"Encourages", not requires.'),
    (JOE, 16, 'forest_protection', 'baseline', 'Steep-slope headwaters: preservation reduces future flooding (Joelton)', None, None, None, 'Metro Planning',
     'Research has shown that the headwaters of many streams and tributaries to the Cumberland River lie in these steep slopes. Preservation of these features can reduce the impact of future flooding by slowing down and absorbing stormwater runoff during rain events.', FLOOD),
    (JOE, 16, 'highland_rim_named_place', 'commitment', 'Rural Countryside is permanent, not a holding zone for urban development', None, None, None, 'Metro Planning',
     'T2-RCS areas are intended to preserve rural character as a permanent choice and do not serve as a holding or transitional zone',
     'Sentence continues on p17: "for future urban development."'),

    (BEL, 8, 'floodplain_stream', 'baseline', 'Bellevue properties damaged in the May 2010 flood', '2347', 'properties', '2010', None,
     "During the May 2010 flood, the community was one of the county's hardest hit areas with 2,347 properties damaged", None),
    (BEL, 11, 'forest_protection', 'baseline', 'After 2010, Nashville learned the value of preserving woodlands and steep slopes', None, None, None, None,
     'Through the experience of the 2010 flood and other flooding events, Nashville has learned the value of preserving woodlands, steep slopes, floodways, floodplains, and natural wetland areas. Preservation of these areas aids absorption of excess water',
     FLOOD),
    (BEL, 12, 'open_space', 'baseline', 'Bellevue park land and community facilities (2015)', '2817', 'acres', '2015', None,
     'In 2015, the Bellevue community contributed approximately 2,817 acres of park land and community facilities to Davidson County.',
     'Plus 1,777 acres of common open space in residential developments (same page).'),
    (BEL, 16, 'forest_protection', 'baseline', 'Bellevue: tree cover stabilizes steep-slope soils and absorbs runoff', None, None, None, None,
     'Many of the areas with steep slopes in Bellevue also have unstable soils that are stabilized by tree cover. Tree cover also aids in protecting headwater quality, absorbing water runoff, and providing wildlife habitat.', FLOOD),
    (BEL, 16, 'forest_protection', 'baseline', 'Bellevue land with sensitive environmental features (2015)', '63', 'percent of land', '2015', None,
     'All together, the community contained 28,534 acres (out of 45,530 acres), or 63 percent, of land containing sensitive environmental features (as of 2015).', None),
    (BEL, 19, 'policy_mechanism', 'commitment', 'Northwest county to remain rural and sparsely developed (little transit)', None, None, None, 'Metro Planning; MTA',
     'the Concept Map shows little transit provided to the northwest of the county because that area is intended to remain rural and sparsely developed.',
     'Same sentence in the Bordeaux-Whites Creek (p19) and West Nashville (p16) plans; recorded once here.'),
    (BEL, 21, 'forest_protection', 'definition', 'Bellevue T2 Rural: steep terrain and woodlands', None, None, None, 'Metro Planning',
     'T2 Rural: Includes much of the northern, western, and southern portions of the community where steep terrain and woodlands exist.', None),
    (BEL, 21, 'highland_rim_named_place', 'definition', 'Bellevue T1 Natural: Edwin Warner Park and the Natchez Trace', None, None, None, 'Metro Planning',
     'T1 Natural: Includes Edwin Warner Park and the Natchez Trace.', None),
    (BEL, 22, 'forest_protection', 'recommendation', 'Conservation policy on all sensitive features after the 2010 flood (Bellevue)', None, None, None, 'Metro Planning',
     'As a result of the May 2010 flooding, the plan encourages the preservation of all environmentally sensitive features, particularly floodplains and floodways, through the use of Conservation policy.',
     '"Encourages", not requires.'),
    (BEL, 22, 'forest_protection', 'baseline', 'Steep-slope headwaters: preservation reduces future flooding (Bellevue)', None, None, None, 'Metro Planning',
     'Research has shown that the headwaters of many streams and tributaries to the Harpeth and the Cumberland Rivers lie in these steep slopes. Preservation of these areas can reduce the impact of flooding in the future by slowing down and absorbing stormwater runoff during rain events.', FLOOD),

    (WN, 10, 'tree_canopy', 'baseline', 'West Nashville infill raises concern about canopy loss', None, None, None, None,
     'This has also led to concerns about the loss of community character resulting from new development with smaller lot sizes, larger homes, and impacts to the tree canopy and other natural features.', None),
    (WN, 11, 'forest_protection', 'baseline', 'Wooded slopes protect communities from flood damage (West Nashville)', None, None, None, None,
     'Among them are floodplains and wooded slopes that clean the air and water, give the region distinctive beauty. They can also protect communities from flood damage and loss of life, as was learned in the flood of 2010.', FLOOD),
    (WN, 11, 'forest_protection', 'baseline', 'West Nashville: tree cover stabilizes slopes and absorbs runoff', None, None, None, None,
     "Many of these areas are also comprised of unstable soils that are stabilized by tree cover. The community's tree cover also aids in absorbing water runoff and provides crucial wildlife habitat and wildlife corridors.", None),
    (WN, 14, 'open_space', 'baseline', 'Very little of West Nashville remains undisturbed', None, None, None, None,
     'Since the West Nashville Community is predominantly developed, very little of the area remains in an undisturbed natural state.', None),
    (WN, 20, 'forest_protection', 'baseline', 'Steep-slope headwaters: preservation reduces future flooding (West Nashville)', None, None, None, 'Metro Planning',
     'Research has shown that the headwaters of many streams and tributaries to the Cumberland River lie in these steep slopes. Preservation of these areas can reduce the impact of flooding in the future by slowing down and absorbing stormwater runoff during rain events.', FLOOD),
    (WN, 30, 'forest_protection', 'recommendation', 'Hillwood Country Club redevelopment: protected open space for slopes and mature vegetation', None, None, None, 'Metro Planning',
     'subject to the creation of permanently protected open space within the development that prioritizes the protection of steep slopes, mature vegetation, and viewsheds.',
     'Supplemental Policy 07-T3-NM-01; applies only if the club use ends and a zone change is sought.'),
    (WN, 31, 'forest_protection', 'recommendation', 'Knob Hill redevelopment: protected open space for slopes and mature vegetation', None, None, None, 'Metro Planning',
     'subject to the creation of permanently protected open space within the development that prioritizes the protection of steep slopes, mature vegetation, and viewsheds.',
     'Supplemental Policy 07-T3-NM-02 (text continues from p30).'),
    (WN, 33, 'tree_canopy', 'recommendation', 'Retain the mature tree row along Harding Pike', None, None, None, 'Metro Planning',
     'Retain distinctive mature tree row along Harding Pike.', 'Supplemental Policy 07-T3-NM-05, West Meade.'),

    (BX, 6, 'highland_rim_named_place', 'status_claim', 'Scottsboro-Bells Bend rural design plan completed 2008', None, None, '2008', 'Metro Planning',
     'A detailed rural design plan for Scottsboro-Bells Bend was completed in 2008 to guide preservation and rural character.',
     'Not in this workbook; a document to acquire.'),
    (BX, 7, 'highland_rim_named_place', 'baseline', 'Bordeaux-Whites Creek-Haynes Trinity planning area size', '70', 'square miles', None, None,
     'The community contains about 70 square miles, or about 13 percent of the land area in Nashville/Davidson County.', None),
    (BX, 10, 'highland_rim_named_place', 'baseline', 'Natural corridor from Williamson County through Bellevue to Cheatham County and Joelton', None, None, None, None,
     'One important link is the network of natural features and undeveloped land that stretches from Williamson County to the south, through Bellevue, westward to Cheatham County and north to Joelton.',
     'Describes the Highland Rim forest arc without naming it.'),
    (BX, 10, 'forest_protection', 'baseline', 'Whites Creek, Scottsboro and Bells Bend: contiguous slopes, woodlands, habitat', None, None, None, None,
     'Much of Whites Creek, Scottsboro, and Bells Bend are contiguous steep slopes, woodlands, floodways and floodplains, wildlife habitat, and farmland.', None),
    (BX, 10, 'forest_protection', 'baseline', 'Land with sensitive environmental features (2015)', '64', 'percent of land', '2015', None,
     'The community contained 28,727 acres of sensitive environmental features out of 44,978 acres (64 percent) of land (in 2015).', None),
    (BX, 11, 'forest_protection', 'baseline', 'About half the community is steep slopes, mainly in Whites Creek', '50', 'percent of community', None, None,
     'Approximately 50 percent of the community, mainly in Whites Creek, has steeply sloping terrain', 'Steep = 20% or greater.'),
    (BX, 11, 'forest_protection', 'baseline', 'Forest cover stabilizes slopes and slows runoff (Bordeaux-Whites Creek)', None, None, None, None,
     'In addition to stabilizing steep slopes and reducing landslides, forest cover also aids in protecting headwater quality, absorbing and slowing water runoff, and providing wildlife habitat.', FLOOD),
    (BX, 11, 'habitat_natural_area', 'baseline', 'Large connected forest habitats', None, None, None, None,
     'The community also provides large sections of forest habitats, connected through corridors, which provide quality areas for wildlife habitat.',
     'Bald eagles nest in the area; rare plants listed on the same page.'),
    (BX, 13, 'highland_rim_named_place', 'baseline', 'Beaman Park: 2,171 acres along the Western Highland Rim', '2171', 'acres', None, None,
     'Beaman Park is a rugged 2,171-acre tract located along the Western Highland Rim.', 'Before the 2026 addition of about 298 acres (BEAMAN-PARK-2026.md).'),
    (BX, 13, 'open_space', 'baseline', 'Bells Bend Park: 808 acres', '808', 'acres', None, None,
     'Bells Bend Park is an 808-acre pastoral tract', 'Bought after a proposed landfill was defeated; designated a park in 2001.'),
    (BX, 13, 'open_space', 'baseline', 'Park, civic and common open space land (2015)', '4516', 'acres', '2015', None,
     'contributes approximately 4,516 acres of park land, community facilities, institutions, recreational areas, and common open space areas to Davidson County (in 2015).', None),
    (BX, 21, 'highland_rim_named_place', 'definition', 'T1 Natural: Beaman Park and Bells Bend Park', None, None, None, 'Metro Planning',
     'T1 Natural: Includes Beaman Park and Bells Bend Park.', None),
    (BX, 22, 'forest_protection', 'baseline', 'Steep-slope headwaters: preservation reduces future flooding (Bordeaux-Whites Creek)', None, None, None, 'Metro Planning',
     'Preservation of these areas can reduce the impact of flooding in the future by slowing down and absorbing stormwater runoff during rain events.',
     'Preceded by: research shows the headwaters of many streams and tributaries to the Cumberland lie in these steep slopes. ' + FLOOD),
    (BX, 22, 'land_acquisition', 'status_claim', 'Private conservation easements in Whites Creek', None, None, None, 'Private landowners',
     "In addition to public lands, several individual property owners in the area have placed conservation easements on their properties to further protect the community's rural, natural setting for decades to come.",
     'Number and acreage not stated.'),
    (BX, 23, 'highland_rim_named_place', 'status_claim', 'New rural policies applied only in the Whites Creek study area (August 2017)', None, None, '2017', 'Metro Planning',
     'Currently (August 2017), these policies have only been applied within the Whites Creek study area.',
     'Rural Agriculture and Rural Countryside. Joelton also applies Rural Countryside (Joelton plan p16). Bears on pair 24 (#323).'),
    (BX, 23, 'policy_mechanism', 'commitment', 'Rural policies to be applied to more rural areas as plans are updated', None, None, None, 'Metro Planning',
     'It is anticipated, however, that as community plan policy areas are updated in the future, these policies will be applied in additional rural areas across Davidson County.',
     'No date given. Bears on pair 24 (#323).'),
    (BX, 23, 'highland_rim_named_place', 'commitment', 'Rural Countryside preserves rural character as a permanent choice', None, None, None, 'Metro Planning',
     'Rural Countryside areas are intended to preserve rural character as a permanent choice for living within Davidson County.', None),
    (BX, 24, 'highland_rim_named_place', 'definition', 'Briley Parkway marks the rural-suburban line', None, None, None, 'Metro Planning',
     'Generally, Briley Parkway marks the transition between Rural and Suburban policies.',
     'A few areas of Suburban policy lie in southern Whites Creek "due to past zoning and development decisions" (same page).'),
    (BX, 33, 'forest_protection', 'definition', 'Fontanel: at least 75% of the site preserved as undisturbed open space', '75', 'percent of site', None, 'Metro Planning',
     'At least 75 percent of the site is permanently preserved as undisturbed open space', 'Supplemental Policy 03-T2-CO-01, a condition for considering commercial use.'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-'})
cache = {}
def page_variants(doc, p):
    if (doc, p) not in cache:
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), f'{PDF_DIR}/{FILE[doc]}', '-'], capture_output=True, text=True).stdout.translate(Q)
        cache[(doc, p)] = [n(t), n(re.sub(r'(\w)-\n(\w)', r'\1\2', t)), n(re.sub(r'-\n', '-', t))]
    return cache[(doc, p)]

wb = openpyxl.load_workbook(XLSX)
have = {(r[0], str(r[1]), n(str(r[9] or '').translate(Q))) for r in wb['Commitments'].iter_rows(min_row=2, values_only=True)}
bad = []
for r in ROWS:
    e = n(r[9].translate(Q))
    if not any(e in v for v in page_variants(r[0], r[1])):
        bad.append((r[0][16:30], r[1], r[4][:40], 'not on page'))
    if (r[0], str(r[1]), e) in have:
        bad.append((r[0][16:30], r[1], 'duplicate'))
bad += [('source exists', s[0]) for s in SOURCES if s[0] in {x[0] for x in wb['Sources'].iter_rows(min_row=2, values_only=True)}]
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
print('written')
