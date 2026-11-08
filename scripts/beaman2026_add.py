"""Add the 2026 Beaman Park forest acquisition: three sources, Commitments rows, one Inconsistencies row.

Usage: python3 beaman2026_add.py <mayor.html> <parks_agenda.pdf> <rs2025_1556.json> <commitments_dir> [--write]
  mayor.html:       https://www.nashville.gov/departments/mayor/news/mayor-freddie-oconnell-announces-acquisition-300-acres-beaman-park
  parks_agenda.pdf: https://www.nashville.gov/sites/default/files/2026-08/Parks-Agenda-2026-09-01.pdf
  rs2025_1556.json: https://webapi.legistar.com/v1/nashville/matters/19714
Rechecks every excerpt against its saved source and exits without writing on any miss.
After --write, run cover_sheet.py.
"""
import csv, html, json, re, subprocess, sys
import openpyxl
from copy import copy

MAYOR_HTML, PARKS_PDF, RS_JSON, CDIR = sys.argv[1:5]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'

MAYOR, PARKS, RS = 'Mayor_Release_Beaman_Park_2026-07-24', 'Parks_Board_Agenda_2026-09-01', 'Resolution_RS2025-1556'
URL = {
    MAYOR: 'https://www.nashville.gov/departments/mayor/news/mayor-freddie-oconnell-announces-acquisition-300-acres-beaman-park',
    PARKS: 'https://www.nashville.gov/sites/default/files/2026-08/Parks-Agenda-2026-09-01.pdf',
    RS: 'https://webapi.legistar.com/v1/nashville/matters/19714',
}
SOURCES = [
    [MAYOR, "Mayor Freddie O'Connell announces acquisition of 300 acres for Beaman Park (Mayor's Office media release)", 'July 24, 2026', 'Media release', None, URL[MAYOR]],
    [PARKS, 'Metropolitan Board of Parks and Recreation, meeting agenda, September 1, 2026 (item 08-26-08)', 'September 1, 2026', 'Agenda (Board decision not found)', 5, URL[PARKS]],
    [RS, 'Resolution RS2025-1556: approving an application for a Beaman Park Protection grant from the Tennessee Heritage Conservation Trust Fund',
     'Adopted October 21, 2025; approved by the Mayor October 23, 2025', 'Adopted', None, URL[RS]],
]

BEARS = 'Bears on: acquire large natural and forested land (Plan to Play 2017, Commitments row 88), land next to parks for habitat (row 93), the Open Space Plan northwest anchor from Beaman Park to Bells Bend (row 666), and the parkland acreage goals in pairs 1, 6 and 7. See docs/research/BEAMAN-PARK-2026.md.'
# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (MAYOR, 'web', 'highland_rim_named_place', 'status_claim', 'Metro acquiring 300 acres of forest to expand Beaman Park', '300', 'acres', '2026', "Mayor's Office; Metro Parks; The Conservation Fund",
     "the city is acquiring 300 acres of forestland that will expand Alvin G. Beaman Park and permanently protect one of Nashville's most significant natural landscapes",
     'The Conservation Fund bought the land and holds it until transfer to Metro Parks. ' + BEARS),
    (MAYOR, 'web', 'highland_rim_named_place', 'baseline', 'Highland Rim Forest: one of the largest intact forest ecosystems in the Southeast', None, None, None, "Mayor's Office",
     "The addition expands the park's footprint within the city's Highland Rim Forest, one of the largest intact forest ecosystems in the Southeast.",
     'Metro\'s own description. The Ecological Conservation Strategy page calls the Highland Rim Forest "the most ecologically significant natural area in the county".'),
    (MAYOR, 'web', 'forest_protection', 'status_claim', 'Mayor: a forest is infrastructure that slows floodwater', None, None, None, "Mayor Freddie O'Connell",
     'A forest is not scenery. A forest is infrastructure. It cools our summers. It slows our floodwater.',
     'Contrast docs/research/FOREST-FLOOD-CHECK.md: the 2026 hazard plan and 2024 climate plan say forest helps with flooding but neither acts on existing forest.'),
    (MAYOR, 'web', 'funding', 'funding_allocated', 'Metro and state contributions to the Beaman Park expansion', '1000000', 'USD (Metro)', '2026', 'Metro Nashville; Tennessee Heritage Conservation Trust Fund',
     'Metro Nashville committed $1 million toward the project, and the Tennessee Heritage Conservation Trust Fund awarded an additional $1.08 million.',
     'The Conservation Fund used $3.2 million from its revolving fund; the Beaman family gave a $1 million lead gift. Metro\'s share is about 31% of $3.2 million.'),
    (PARKS, 1, 'land_acquisition', 'status_claim', 'Parks Board item: transfer of about 298.20 acres next to Beaman Park', '298.2', 'acres', '2026', 'Metro Parks',
     'Staff requests approval of the transfer of land from The Conservation Fund, of approximately 298.20 acres adjacent to Beaman Park for park expansion and conservation purposes.',
     'Item 08-26-08, Bull Run Road, southern boundary of the park, Council District 1. INCONSISTENT: the Mayor\'s release says 300 acres; RS2025-1556 says approximately 308 acres. The Board\'s decision and Council acceptance of the land were not found as of 2026-10-22.'),
    (PARKS, 1, 'funding', 'funding_allocated', "Metro's $1,000,000 came from the FY2026 Capital Spending Plan", '1000000', 'USD', '2026', 'Metro Parks',
     "Metro's contribution toward this acquisition was $1,000,000, which was appropriated to Metro Parks through FY2026 CSP for this purpose.",
     'Matches the Mayor\'s release.'),
    (RS, 'title', 'highland_rim_named_place', 'status_claim', 'Council approved state grant application to buy about 308 acres next to Beaman Park', '308', 'acres', '2025', 'Metro Council; Metro Parks; The Conservation Fund',
     'to acquire approximately 308 acres adjoining Alvin G. Beaman Park in Davidson County to add a unique urban wilderness within the City of Nashville.',
     'Adopted October 21, 2025; approved by the Mayor October 23, 2025. The grant became the $1.08 million award named in the Mayor\'s release.'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
QUOTES = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'})
text = {
    MAYOR: n(html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?s)<(script|style).*?</\1>', '', open(MAYOR_HTML, encoding='utf-8', errors='replace').read()))).translate(QUOTES)),
    PARKS: n(subprocess.run(['pdftotext', '-f', '1', '-l', '1', PARKS_PDF, '-'], capture_output=True, text=True).stdout.translate(QUOTES)),
    RS: n(json.load(open(RS_JSON, encoding='utf-8'))['MatterTitle'].translate(QUOTES)),
}
wb = openpyxl.load_workbook(XLSX)
bad = [(r[0], r[4]) for r in ROWS if n(r[9].translate(QUOTES)) not in text[r[0]]]
bad += [('source exists', d) for d in URL if d in {r[0] for r in wb['Sources'].iter_rows(min_row=2, values_only=True)}]
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
append(wb['Inconsistencies'], [r for r in full if 'INCONSISTENT' in r[10]], 12)

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
