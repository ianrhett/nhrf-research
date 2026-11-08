"""Rank every promise in the workbook by potential benefit to the Highland Rim forest.

Usage: python3 forest_priorities.py <commitments_dir> [--write]
Scores all promise rows (item_type recommendation, commitment, target, funding_estimate,
funding_allocated), groups restatements of the same promise into families, and writes the
Forest_Priorities tab plus forest_priorities.csv. Without --write, prints the family summary.

Score is a judgment of potential benefit to existing forest if the promise were kept:
  5 protects existing forest at scale with a binding tool or land protection
  4 large measurable land or canopy goals that would hold forest countywide
  3 programs, plans and management that enable protection
  2 planting and buyouts: adds trees or open land, protects little existing forest
  1 peripheral: urban street trees, pocket parks, access, education, staffing
Families are assigned by ordered rules (first match wins) on metric and excerpt, then OVERRIDE.
"""
import csv, re, sys
from collections import defaultdict
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

CDIR = sys.argv[1]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
PROMISE = {'recommendation', 'commitment', 'target', 'funding_estimate', 'funding_allocated'}
FOREST_CATS = {'forest_protection', 'tree_canopy', 'highland_rim_named_place', 'habitat_natural_area', 'land_acquisition', 'open_space'}

# family id, score, label, pattern on metric + excerpt (case-insensitive)
FAMILIES = [
    ('F01', 5, 'Hillside and steep-slope protection', r'slope|hillside|ridgetop|ridgeline|escarpment better|rugged topograph|rugged terrain|unstable soils|geologic formation|front range hill|preserving hills'),
    ('F02', 5, 'Conservation subdivisions and cluster open space', r'conservation subdivision|cluster|grouped homes|of tract in natural|natural area set-aside|1 acre per 4|rural character subdivision'),
    ('F03', 5, 'Tree protection rules for development on private land', r'landscape (code|ordinance)|tree protection|tree ordinance|preservation policy|mature trees on private|stricter tree|codes to increase tree preservation|tree preservation during development|barriers to forest conservation|tied to preserving mature tree'),
    ('F04', 5, 'Keep development and sewers out of rural and Rim land', r'sewer|sprawl|urdl|greenfield|steer development|semirural|low density|economic activities kept out|conservation-nonurban|non low density|rural lands|rural land|existing agricultural land|agricultural overlay|prime farmland|fertile agricultural'),
    ('F05', 5, 'Acquire or ease large natural, rural and Rim lands', r'large natural areas|rural and forested|high conservation value|critical rural parcels|private land conservation|privately conserve|privately conserved|ecologically valuable|land bank|regional land conservation|upstream watershed|acquire natural areas|purchase natural areas|designate and purchase|natural corridor areas|critical cultural and ecologic|tree conservation areas|natchez trace|conservation easement|easements, then acqui|habitat protection \(per 2011'),
    ('F06', 5, 'Highland Rim conservation policy and anchors', r'highland rim worthy|anchor: beaman|anchor: warner|beaman park to bells bend|escarpment: natural features|rim hilltops|woodlands cannot be overemphasized|western conservation areas|careful staff review'),
    ('F07', 4, 'Countywide land conservation acreage goals', r'22,?000|new conserved open space|conserve additional acres|additional park ?land|park land needed|regional park acres|new metro parkland|parkland \(open space plan\)|acres of land preserved|new acres of public park|level-of-service goal: new public land|tier (one|two|three) new land|expand park and greenway land|conservation/parkland acres|most progressive open space plan|open space plan and commit|framework defining county land conservation|accelerate purchase|acquire land and preserve open space|use economic downturn|level of service|southeast (nashville )?anchor'),
    ('F08', 4, 'Hold countywide and rural canopy', r'net tree loss|countywide (tree )?canopy|50x50|t1 natural|t2 rural|undisturbed canopy|larger tracts of forested|forested tracts|forested lands|non-urban lands|preserve canopy where high|canopy and conservation land credited|nr 1\.4 policy|greenbelt|forestry management plan'),
    ('F09', 3, 'Natural areas: designate, manage, connect', r'natural area|wildlife corridor|invasive|rare species|cedar glade|unique areas|landscape resources|preconstruction assessment|sensitive environmental and rural|protect lands and critical|invest in and increase natural|protect and preserve nature|natural resources|preserve vegetation|existing vegetation|native vegetation|minimize vegetation removal|existing contours|topography guide|scenic and natural|scenic corridors|scenic easements|vistas|notable trees|mature vegetation|woodlands, slopes|watershed protection|sensitive features|preserve natural|conservation strategy|scenic arterial|open space network|open space system'),
    ('F10', 3, 'Canopy and forest planning, inventory and assessment', r'assessment|urban forest (program|management)|forest management plan|tree canopy campaign|mnuf|canopy goals|canopy target percentage|density .*goals|inventory|tree bank|urban forestry (program|staff)|forestry staff|pest|emerald ash|re-align hmp|merge canopy'),
    ('F11', 2, 'Tree planting programs', r'plant|trees planted|planting|root nashville|tree enhancement|trees to plant'),
    ('F12', 2, 'Floodplain buyouts converted to open space', r'buyout|repetitive loss|flooded properties|duplication of benefits|hazard areas|near all streams|flood regulatory'),
    ('F13', 1, 'Urban canopy targets and street trees', r'canopy target|street tree|downtown|parking lot|canopy over|t[3-6] |subarea|commercial and industrial|single family residential|school properties|right-of-way|hubnashville|transect'),
    ('F14', 1, 'Parks access, small parks, recreation and outreach', r'.'),
]
FAM = {f[0]: f for f in FAMILIES}

# Rows (1-based on Commitments, header = row 1) whose rule match is wrong, by inspection.
OVERRIDE = {
    1308: 'F01',   # Code 17.28.030.A.2: slopes over 25% recorded as open space
    1322: 'F02',   # BL2006-1046 50% of tract
    164: 'F14',    # Bells Bend grassland conversion candidate: not forest protection
    92: 'F14',     # Brookmeade to Bells Bend bridge or ferry
    407: 'F14',    # Beaman to Bells Bend corridor trail
    94: 'F05',     # Highland Rim long-distance trails via acquisition and easements
    800: 'F06', 801: 'F06',  # Rim escarpment lakes as parkland
    163: 'F14', 194: 'F14', 543: 'F14', 567: 'F14',  # turf or highway to grassland
    1101: 'F14',   # surplus civic sites review
    459: 'F01',    # UFLMP slope provision 15% to 20%
    1015: 'F14', 201: 'F14', 1342: 'F14', 522: 'F14',  # greenway and stormwater items caught by loose words
    478: 'F08',    # Bordeaux-Whites Creek undisturbed canopy, same as Joelton (474)
    1123: 'F03',   # tree preservation on constrained sites
    278: 'F14', 216: 'F14', 1012: 'F14', 355: 'F14', 839: 'F14',  # urban green space, sewer-area GI
    1072: 'F13', 457: 'F13', 642: 'F13',  # combined sewer area trees
    61: 'F12', 825: 'F12',  # floodplain regulation
    932: 'F09', 854: 'F09', 1163: 'F09', 208: 'F09', 215: 'F09', 1088: 'F09', 129: 'F09',
    699: 'F09', 700: 'F09', 1026: 'F09', 1000: 'F09', 603: 'F09',  # buffers, wetlands, aquatic habitat
    68: 'F07', 669: 'F07',  # parkland acreage goals
    262: 'F05', 840: 'F05',  # parcels adjoining Warner Park; regulation and purchase of Rim hills
    144: 'F08', 268: 'F08',  # countywide canopy outcome and vision
    137: 'F11', 100: 'F11', 1069: 'F11',  # planting
    189: 'F13', 366: 'F13', 367: 'F13', 869: 'F13',  # street trees and downtown
    1230: 'F14', 145: 'F14', 923: 'F14',  # park activities, education, riverfront
    672: 'F05',    # Open Space Plan: 10,000 acres of floodplain and sensitive natural areas
    283: 'F05', 704: 'F05', 706: 'F05', 709: 'F05',  # conservation fund, open space fund, land trust fund, TDR
    702: 'F07',    # No Net Loss of Open Space policy for Metro Park lands
    695: 'F07',    # designated department for strategic acquisitions
    1532: 'F01',   # Concept 2010: conserve hills and unique landscape features
    1540: 'F05',   # Concept 2010: identify and secure open space for public use
    1546: 'F03',   # Concept 2010: protect mature vegetation during construction
    1548: 'F04',   # Concept 2010: protect rural areas from untimely development
    1553: 'F13', 1555: 'F13', 1556: 'F13', 1558: 'F13',  # Metro-property tree policy (Code 2.226, EO 41A): public trees, not private-land rules
}

wb = openpyxl.load_workbook(XLSX)
ws = wb['Commitments']

# Commitments row -> Promised_vs_Delivered pair that checks it (pairs 4, 5, 11 and 16 check
# baselines or trail miles, not rows ranked here). #174 is discussed in pair 22's notes only.
PAIR_ROW = {68: 1, 104: 2, 69: 3, 668: 6, 687: 7, 670: 8, 672: 9, 674: 10, 702: 12, 703: 13,
            695: 14, 72: 15, 100: 17, 94: 18, 704: 19, 283: 20, 1238: 21, 1257: 22,
            1255: 23, 1222: 24, 1297: 24, 1249: 25, 1292: 26, 523: 27}
NOTED = {1258: 'Noted in pair 22'}

def checked(row):
    return f'Pair {PAIR_ROW[row]}' if row in PAIR_ROW else NOTED.get(row, '')

def due_passed(ty):
    """'Yes' when a stated deadline year is over (before 2026: a 2026 deadline has not ended as of the v1.6.0 release, 2026-10-24)."""
    ty = str(ty or '')
    m = re.search(r'(19|20)\d\d', ty)
    return 'Yes' if m and int(m.group()) < 2026 else ''

def start_window_passed(ty):
    """NashvilleNext Vol IV timeframes (near, mid, long term) are windows to BEGIN work (Vol IV p4), not completion
    deadlines. 'Yes' means the window to begin has passed; it says nothing about whether work began or finished."""
    ty = str(ty or '')
    if re.search(r'(19|20)\d\d', ty):
        return ''
    return 'Yes' if re.search(r'term', ty, re.I) else ''  # all Vol IV start windows closed by 2025

out = []
for i, r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
    if not r[0] or r[3] not in PROMISE:
        continue
    text = f'{r[4]} {r[9]}'
    fam = OVERRIDE.get(i) or next(f[0] for f in FAMILIES if re.search(f[3], text, re.I))
    fid, score, label, _ = FAM[fam]
    out.append(dict(score=score, family=fid, family_label=label, row=i, doc=r[0], pdf_page=r[1],
                    category=r[2], item_type=r[3], metric=r[4], value=r[5], unit=r[6], target_year=r[7],
                    due_passed=due_passed(r[7]), start_window_passed=start_window_passed(r[7]), checked=checked(i),
                    in_forest_353='Yes' if r[2] in FOREST_CATS else 'No (added)'))

# Promises outside the six Forest categories are kept only if they score 4 or 5.
out = [o for o in out if o['in_forest_353'] == 'Yes' or o['score'] >= 4]
def _legacy_due(ty):
    m = re.search(r'(19|20)\d\d', str(ty or ''))
    return bool(m and int(m.group()) <= 2026) or (not m and bool(re.search(r'term', str(ty or ''), re.I)))

out.sort(key=lambda o: (-o['score'], o['family'], not _legacy_due(o['target_year']), o['doc'], o['row']))

fam_rows = defaultdict(list)
for o in out:
    fam_rows[o['family']].append(o)
print(f"{len(out)} promises ranked ({sum(o['in_forest_353'] == 'Yes' for o in out)} from the 353, {sum(o['in_forest_353'] != 'Yes' for o in out)} added)")
for fid, score, label, _ in FAMILIES:
    rs = fam_rows.get(fid, [])
    docs = sorted({o['doc'] for o in rs})
    print(f"{fid} s{score} {label}: {len(rs)} rows, {len(docs)} docs, due-passed {sum(o['due_passed'] == 'Yes' for o in rs)}, start-window-passed {sum(o['start_window_passed'] == 'Yes' for o in rs)}, checked {sum(o['checked'].startswith('Pair') for o in rs)}")
if '--write' not in sys.argv:
    for o in out:
        print(o['score'], o['family'], o['row'], o['doc'][:24], '|', o['metric'][:80], '|', o['in_forest_353'])
    sys.exit(0)

COLS = ['score', 'family', 'family_label', 'row', 'doc', 'pdf_page', 'category', 'item_type', 'metric', 'value', 'unit',
        'target_year', 'due_passed', 'start_window_passed', 'checked', 'in_forest_353']
if 'Forest_Priorities' in wb.sheetnames:
    del wb['Forest_Priorities']
ft = wb.create_sheet('Forest_Priorities', wb.sheetnames.index('Promised_vs_Delivered') + 1)
ft.append(COLS)
for o in out:
    ft.append([o[c] for c in COLS])
head = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
for c in ft[1]:
    c.font, c.fill = head, PatternFill('solid', fgColor='FF2F5D3A')
for row in ft.iter_rows(min_row=2):
    for c in row:
        c.font = Font(name='Arial', size=10)
for col, w in zip('ABCDEFGHIJKLMNOP', (7, 7, 40, 7, 30, 9, 18, 14, 60, 10, 14, 18, 10, 12, 9, 13)):
    ft.column_dimensions[col].width = w
for c in ft['I']:
    c.alignment = Alignment(wrap_text=True, vertical='top')
ft.freeze_panes = 'A2'
ft.auto_filter.ref = ft.dimensions
wb.save(XLSX)
with open(f'{CDIR}/forest_priorities.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(COLS)
    w.writerows([[o[c] if o[c] is not None else '' for c in COLS] for o in out])
print('written')
