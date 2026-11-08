"""Append forest-and-flooding rows from the 2026 Hazard Mitigation Plan and 2024 Climate Adaptation and Resilience Plan.

Usage: python3 forest_flood_add.py <hmp.pdf> <carp.pdf> <commitments_dir> [--write]
PDFs are the files at each doc's source_url in the Sources tab. Rechecks every excerpt against
pdftotext of its stated PDF page and exits without writing on any miss or duplicate.
"""
import csv, re, subprocess, sys
import openpyxl
from copy import copy

HMP_PDF, CARP_PDF, CDIR = sys.argv[1:4]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
HMP = 'Hazard_Mitigation_Plan_2026_Final'
CARP = 'Climate_Adaptation_Resilience_Plan_2024_Final'
PDF = {HMP: HMP_PDF, CARP: CARP_PDF}

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (HMP, 92, 'forest_protection', 'baseline', 'Converting woodlands to pavement causes urban flooding', None, None, None, None,
     'Urban flood events result as land loses its ability to absorb rainfall as it is converted from fields or woodlands to roads, buildings, and parking lots.',
     'Flooding hazard profile. The plan names loss of woodland as a flood cause; no mitigation action protects existing forest (see docs/research/FOREST-FLOOD-CHECK.md).'),
    (HMP, 92, 'floodplain_stream', 'baseline', 'Urbanization multiplies runoff', '2 to 6', 'times undeveloped runoff', None, None,
     'Urbanization increases runoff two to six times over what would occur on undeveloped terrain.',
     'Flooding hazard profile.'),
    (HMP, 223, 'tree_canopy', 'status_claim', 'Tree planting credited with flood mitigation', None, None, None, 'Metro Water Services',
     'thereby increasing tree benefits such as heat island mitigation, pollutant removal, carbon sequestration, and flood mitigation.',
     'Capability assessment, Root Nashville planting by MWS (sentence starts on p222). Credits planted trees, not existing forest; no tree or forest action appears among the recommended mitigation actions.'),
    (CARP, 204, 'forest_protection', 'recommendation', 'NE1 canopy and conservation land credited with watershed and floodplain benefits', None, None, None, None,
     'reforestation efforts, and urban tree planting will all contribute to Nashville’s climate resilience by reducing urban heat island effects, preserving biodiversity, protecting watersheds and better managing floodplains',
     'Strategy NE1 description. Listed as a benefit; no forest acreage target. The near-term action is planting on Metro land and rights-of-way (p132); the Goal III measure is acres of green space from FY2027 (p134).'),
    (CARP, 207, 'floodplain_stream', 'definition', 'NE4 nature-based flood measures are stream, wetland and floodplain restoration', None, None, None, None,
     'such as river, stream and wetland restoration and extended detention wetlands, and incorporate nature-based solutions in local planning, zoning, regulations, and built projects.',
     'Strategy NE4. Upland or hillside forest retention is not among the named approaches.'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
QUOTES = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'})
page = lambda doc, p: n(subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), PDF[doc], '-'], capture_output=True, text=True).stdout.translate(QUOTES))

wb = openpyxl.load_workbook(XLSX)
ws = wb['Commitments']
url = {r[0]: r[5] for r in wb['Sources'].iter_rows(min_row=2, values_only=True) if r[0] in PDF}
have = {(r[0], n(r[9] or '')) for r in ws.iter_rows(min_row=2, values_only=True)}
bad = []
for doc, p, *_, ex, notes in ROWS:
    if n(ex.translate(QUOTES)) not in page(doc, p):
        bad.append((doc, p, 'not on page'))
    if (doc, n(ex)) in have:
        bad.append((doc, p, 'duplicate'))
print('rows', len(ROWS), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

last = ws.max_row
for r in ROWS:
    ws.append(list(r) + ['verified', url[r[0]]])
    for col in range(1, 14):
        s, d = ws.cell(last, col), ws.cell(ws.max_row, col)
        d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format
wb.save(XLSX)

with open(f'{CDIR}/commitments.csv', 'w', encoding='utf-8', newline='') as f:
    csv.writer(f).writerows([['' if v is None else v for v in r] for r in ws.iter_rows(values_only=True)])
print('written')
