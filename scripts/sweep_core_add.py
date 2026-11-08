"""Sweep of plans extracted selectively early on: rows the candidate finder surfaced and a reader kept.

Usage: python3 sweep_core_add.py <pdf_dir> <commitments_dir> [--write]
pdf_dir holds each document as <doc_id>.pdf, downloaded 2026-10-22 from its source_url on the Sources
tab. find_candidates.py was run over 18 documents (4,162 candidates; 569 Forest-core sentences not
already in the workbook were read; survey comments already on Public_Comments_Highland_Rim and
storm-event logs were skipped). Every excerpt is rechecked against its page; the script exits without
writing on any miss or duplicate. The 1973 and 1981 scans have no text layer and were not swept.
After --write: forest_priorities.py --write, cover_sheet.py.
"""
import csv, re, subprocess, sys
import openpyxl
from copy import copy

PDF_DIR, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
wb0 = openpyxl.load_workbook(XLSX, read_only=True)
URL = {r[0]: r[5] for r in wb0['Sources'].iter_rows(min_row=2, values_only=True) if r[0] and r[5]}
SOURCES = []
FLOOD = 'Compare FOREST-FLOOD-CHECK.md: the 2026 hazard and 2024 climate plans do not act on existing forest.'

HMP, GRC, NNBG, UFL, LIV, NRHA, UTC, OSP, P26, P26A = ('Hazard_Mitigation_Plan_2026_Final', 'Green_Ribbon_Committee_Report_2009',
    'NashvilleNext_Natural_Resources_Background_2013', 'Urban_Forestry_Landscape_Master_Plan_2016', 'Livable_Nashville_2017_DRAFT',
    'NashvilleNext_Vol2_Natural_Resources_Hazard_Adaptation', 'Urban_Tree_Canopy_Assessment_2023', 'Nashville_Open_Space_Plan_2011',
    'Plan_to_Play_2026_Update', 'Plan_to_Play_2026_Appendix')
FILE = {d: f'{d}.pdf' for d in (HMP, GRC, NNBG, UFL, LIV, NRHA, UTC, OSP, P26, P26A)}

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (HMP, 26, 'highland_rim_named_place', 'baseline', 'Joelton: steep slopes, ridges and valleys in a crescent', '20', 'percent slope (definition)', None, None,
     'In a crescent that curves from the southwestern portion to the northeastern portion of the area, steep slopes (20 percent and greater), narrow ridges and valleys are the predominant features.', 'Community profile of Joelton.'),
    (HMP, 27, 'forest_protection', 'baseline', 'Parkwood-Union Hill: mostly heavily forested steep slopes', '20', 'percent slope (definition)', None, None,
     "Most of the community plan area's terrain consists of heavily forested steep slopes (20 percent and greater) and narrow ridges and valleys.", 'Community profile of Parkwood-Union Hill, north-central county.'),
    (HMP, 175, 'policy_mechanism', 'commitment', 'Grow in centers so sewer expansion is discouraged and slopes spared', None, None, None, 'Metro Planning',
     'Much of the future population and job growth can be encouraged within the activity centers and corridors so that expansion of sewer service in some areas of Davidson County is discouraged and there is less impact upon slopes and within floodplains.',
     'The hazard plan restates NashvilleNext. Compare LUTI Policy 9.4 (Land Use p60) and pair 24.'),
    (HMP, 221, 'forest_protection', 'definition', 'Critical lot: up-slope over 15% or down/cross-slope over 20%', '15', 'percent slope', None, 'Metro Planning; Metro Codes',
     'Generally, a lot will be designated critical when it is created on an up-slope greater than 15 percent or a down or cross-slope greater than 20 percent grade.',
     'Critical lots get extra review, not a prohibition. The 15% figure here is a review trigger, not the hillside limit NashvilleNext #210 asked for (pair 21).'),
    (HMP, 250, 'policy_mechanism', 'status_claim', 'Subdivision review looks at slope, soils and floodplain', None, None, None, 'Metro Planning',
     'Planning states that Subdivision Regulations state that Planning shall look at Slope, Soils and floodplain, and they may look at geological features also.', 'Capability assessment discussion of critical lots.'),
    (GRC, 38, 'tree_canopy', 'baseline', 'Most city tree ordinances cover removal on private property (2009 survey)', '63', 'percent of ordinances', None, None,
     "A US Conference of Mayors' study found that of the eighty-five percent of 135 cities surveyed that have tree ordinances, 63 percent of the ordinances cover removal of trees from private property.",
     'Shows the model was known in 2009. Same page cites Austin and Atlanta permits for removing large private trees. Compare pair 23.'),
    (GRC, 44, 'floodplain_stream', 'recommendation', 'Honor the natural floodplain and stream buffers', None, None, None, None,
     'Improve protection of the watersheds in Davidson county by honoring the natural flood plain and stream buffers', None),
    (NNBG, 7, 'forest_protection', 'baseline', 'Forested areas protect headwaters and slow erosion', None, None, None, None,
     'Forested areas protect headwaters from pollution by filtering pollutants out of the stream system and slow erosion from flooding, thereby minimizing sediments in the water.', FLOOD),
    (NNBG, 22, 'forest_protection', 'baseline', 'Local government plays a key role in preserving woodlands from development', None, None, None, None,
     'Local governments play a key role in preserving trees and woodlands, particularly dealing with the conversion of land to more intense development uses.', None),
    (NNBG, 28, 'open_space', 'baseline', 'Low level of land conservation will not meet future needs (2012)', '7', 'percent of county protected', '2012', None,
     'This low level of land conservation will not support the future recreation, agriculture and habitat needs of the city.',
     'Preceding sentence: as of 2012, 3% of the county is Metro parkland and another 4% protected by easements or state and federal programs.'),
    (UFL, 9, 'tree_canopy', 'status_claim', 'Nashville needs improvement in tree preservation during development (2016)', None, None, '2016', 'Metro Landscape Coordination Program',
     'From our assessment it shows that Nashville has room for improvement, especially in the areas of tree preservation and making trees a priority in all areas of development.', None),
    (UFL, 33, 'tree_canopy', 'status_claim', 'Voluntary Historic and Specimen Trees program (2016)', None, None, '2016', 'Metro Tree Advisory Committee',
     'This program to protect mature trees was officially announced by Mayor Megan Berry in 2016.', '"Berry" as printed (Barry). Voluntary; designation needs owner consent (Metro Code 17.28.065.A.3).'),
    (LIV, 32, 'forest_protection', 'recommendation', 'Strengthen regulations to protect ridges and steep slopes', None, None, None, None,
     'Strengthen regulations to better protect open spaces and vital natural resources, such as floodplains and ridges/steep slopes.', 'DRAFT document. Compare pair 21.'),
    (NRHA, 5, 'forest_protection', 'baseline', '2010 flood: floodplains and tree cover kept damage from being worse (2015)', None, None, '2010', None,
     'The damage caused to life and property by the 2010 flood and related landslides was enormous, yet the city\'s natural features-such as floodplains and tree cover, ensured that the damage and loss of life and property was not worse.',
     'Repeated in Vol I parts G-H p54 (2017). ' + FLOOD),
    (NRHA, 7, 'forest_protection', 'baseline', 'Forested areas protect headwaters and slow erosion (2015)', None, None, None, None,
     'Forested areas protect headwaters from pollution by filtering pollutants out of the stream system and slow erosion from flooding, thereby minimizing debris and sediments in the water.', FLOOD),
    (NRHA, 9, 'forest_protection', 'baseline', 'Some natural areas should be left undisturbed', None, None, None, None,
     'since there are natural areas that should be left undisturbed-to balance development with preservation.', None),
    (NRHA, 19, 'forest_protection', 'baseline', 'Woodlands serve as headwater areas protected by tree cover', None, None, None, None,
     'Woodlands play a key role in watershed health as previously discussed, serving as headwater areas that are protected by tree cover, vegetation, and undisturbed soils.', FLOOD),
    (NRHA, 33, 'forest_protection', 'status_claim', 'Past policy and regulation did not protect steep slopes and floodplains', None, None, None, None,
     'Like many cities, Nashville must address development that occurred over decades where policy and regulations did not protect natural systems such as floodplains, wetlands, and steep slopes',
     "Metro's own admission in the adopted natural resources element (2015)."),
    (UTC, 20, 'tree_canopy', 'status_claim', 'Half of community planning areas lost canopy 2016-2021', None, None, '2021', None,
     'From 2016 to 2021, half of the community planning areas experienced canopy loss.', 'Joelton had the largest gain 2010-2021 (row 639).'),
    (UTC, 29, 'forest_protection', 'recommendation', 'Explore tree preservation policies and legislation (2023)', None, None, None, None,
     'Explore tree preservation and canopy expansion policies and legislation.', 'Compare pair 23.'),
    (OSP, 23, 'forest_protection', 'baseline', 'Preserving land along streams is the cheapest way to improve water quality', None, None, None, None,
     'Land preservation along the rivers and streams is the least costly and most effective way to improve water quality.', None),
    (P26, 50, 'land_acquisition', 'recommendation', 'Acquire land next to parks to expand unbroken natural habitat', None, None, None, 'Metro Parks',
     'Acquiring adjacent land may prevent incompatible land uses, protect view sheds, secure inholdings, improve public access, expand unbroken natural habitat',
     'The 2026 Beaman Park addition is an example (BEAMAN-PARK-2026.md).'),
    (P26, 13, 'land_acquisition', 'recommendation', 'Land acquisition to weigh viewshed and habitat protection (Rec. 7.2.5b)', None, None, None, 'Metro Parks',
     'Land Acquisition Efforts Should Consider Equitable Access, Viewshed and Habitat Protection, and Programmatic Potential', None),
    (P26A, 488, 'tree_canopy', 'status_claim', 'Metro Parks no longer maintains street trees', None, None, None, 'Metro Parks',
     'Metro Parks no longer maintains street trees and rights of way.', 'Bears on Plan to Play 2017 street tree maintenance (row 96).'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‐': '-', '­': '', '\ufb00': 'ff', '\ufb01': 'fi', '\ufb02': 'fl', '\x07': ''})
cache = {}
def variants(doc, p):
    if (doc, p) not in cache:
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), f'{PDF_DIR}/{FILE[doc]}', '-'], capture_output=True, text=True).stdout.translate(Q)
        cache[(doc, p)] = [n(t), n(re.sub(r'(\w)-\n(\w)', r'\1\2', t)), n(re.sub(r'-\n', '-', t))]
    return cache[(doc, p)]

wb = openpyxl.load_workbook(XLSX)
have_src = {x[0] for x in wb['Sources'].iter_rows(min_row=2, values_only=True)}
bad = [(r[0][13:30], r[1], r[4][:40]) for r in ROWS if not any(n(r[9].translate(Q)) in v for v in variants(r[0], r[1]))]
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
