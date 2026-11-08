"""Concept 2010, the general plan between the 1981 plan and NashvilleNext: source row and checked rows.

Usage: python3 concept2010_add.py <ocr_dir> <commitments_dir> [--write]
The Alliance's copy is a 70-page scan without a text layer (Concept2010.pdf; the same file is filed as
"Concept 2010--A General Plan for Nashville-Davidson County (October 1991)"). It is the umbrella General
Plan volume; the functional and subarea plans it describes are separate documents not in hand. Printed
pages 32-33, 41 and 51 are missing from the scan. OCR with ocr_page.sh into ocr_dir/<doc>/p<N>.txt
(2026-10-22); find_candidates.py gave 90 candidates, all read; 22 kept. The surviving pages never name
the Highland Rim. Every excerpt is rechecked against the OCR of its page; the script exits without
writing on any miss, duplicate, or existing source. OCR misreadings are kept as printed by the OCR and
noted. After --write: forest_priorities.py --write, cover_sheet.py, top5_timeline.py.
"""
import csv, re, sys
import openpyxl
from copy import copy

OCR, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
C10 = 'Concept_2010_General_Plan_1992'
URL = 'https://www.nashvillehighlandrimforest.org/archive/Concept2010.pdf'
SOURCES = [
    [C10, 'Concept 2010: A General Plan for Nashville-Davidson County (Metropolitan Planning Commission)',
     'Adopted 1992 (per later Metro Planning records [ASSUMED]; Alliance copy filed as October 1991)',
     'Adopted (scan; OCR; general plan volume only; printed pp. 32-33, 41, 51 missing)', 70, URL],
]
FLOOD = 'Compare FOREST-FLOOD-CHECK.md: the 2026 hazard and 2024 climate plans do not act on existing forest.'

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (C10, 9, 'policy_mechanism', 'baseline', 'Natural environment framed as a limit on growth', None, None, None, 'Metro Planning Commission',
     'To focus solely on the preservation of the natural environment would be to severely restrict or even stop residential and commercial development.', None),
    (C10, 20, 'greenways', 'recommendation', 'Preserve floodplain and other land for a greenbelt linking open spaces', None, None, None, 'Metro Parks',
     'Preserve floodplain and other areas necessary to a greenbelt system linking major open spaces.', None),
    (C10, 22, 'open_space', 'recommendation', 'Identify and reserve land for conservation', None, None, None, 'Metro Planning Commission',
     'The identification and reservation of areas appropriate for conservation and recreation should be undertaken.', None),
    (C10, 22, 'floodplain_stream', 'recommendation', 'Preserve floodplains as open space', None, None, None, None,
     'The preservation of floodplain areas as open space is a particularly attractive concept, from both environmental and recreational/scenic standpoints.', None),
    (C10, 29, 'policy_mechanism', 'commitment', 'Sewers drive density; extend them with care', None, None, None, 'Metro Water and Sewerage Services',
     'Public sewerage service allows the density required for large scale urban development. Providing public sewers, then generally leads to increased demand for schools, parks, roads, fire and police protections and other urban services. Thus sewer provision should be carefully considered in light of the potential availability of those services.',
     'Same page continues the 1981 policy of requiring public sewers only in areas recommended for urban development.'),
    (C10, 39, 'forest_protection', 'recommendation', 'Conserve hills and other unique landscape features', None, None, None, 'Metro Planning Commission',
     'Particular care to conserve the landscape features which are in many ways unique in a large urban area. This should involve creative management of the natural open space/scenic potential of floodplains, hills, and other sensitive natural features.',
     'The Natural Environment chapter opens with "many tree-covered hills" (same page) but never names the Highland Rim.'),
    (C10, 39, 'forest_protection', 'status_claim', 'Room to protect natural resources is shrinking (1992)', None, None, '1992', 'Metro Planning Commission',
     'The planning process should reflect an overall awareness that latitude to protect these resources is diminishing with increasing urbanization.', None),
    (C10, 40, 'forest_protection', 'baseline', 'Slopes contribute to flooding by increasing runoff', None, None, None, None,
     'slopes contribute to flood problems by increasing rates of run-off and siltation of stream channels.',
     'The sentence begins on printed p32 or 33, missing from the scan; the 1981 plan p256 has "Devegetated slopes contribute to flood problems". ' + FLOOD),
    (C10, 40, 'forest_protection', 'commitment', 'Rugged terrain: low intensity or open space', None, None, None, 'Metro Planning Commission',
     'As long as there is enough developable land without these hazardous features, rugged terrain should be limited to low intensity development or conserved as open space.', None),
    (C10, 40, 'forest_protection', 'commitment', 'Strictly control development on rugged terrain (Goal 1)', None, None, None, 'Metro Planning Commission',
     'Development on rugged terrain should be strictly controlled. Only compatible development should take place in environmentally fragile areas.', 'Compare NashvilleNext #210 (pair 21).'),
    (C10, 40, 'policy_mechanism', 'recommendation', 'Use clustering or transfer of development rights on rugged terrain', None, None, None, 'Metro Planning Commission',
     'Facilitate creative development approaches such as clustering or transfer of development rights which will conserve',
     'Continues on the next printed page (PDF p42): "notable landscape features and ensure structural soundness." TDR recommended again in 2011 and 2017; never adopted.'),
    (C10, 41, 'policy_mechanism', 'recommendation', 'Restrict septic tanks to suitable land and soils', None, None, None, None,
     'Protect groundwater by restricting the use of septic tanks to appropriate land formations and soil types.', None),
    (C10, 42, 'forest_protection', 'commitment', 'Conserve rugged terrain as open space where development would degrade it (Goal 2)', None, None, None, 'Metro Planning Commission',
     'Rugged terrain should be conserved as open space if development would cause soil and/or water degradation or, where the terrain possesses special scenic or recreational value.', None),
    (C10, 42, 'land_acquisition', 'recommendation', 'Identify land for open space conservation and secure it for public use', None, None, None, 'Metro Planning Commission',
     'Identify areas suitable for conservation as open space based on their development potential and aesthetic qualitics, and work toward securing or preserving them for public use.',
     '"qualitics" is the OCR reading of "qualities".'),
    (C10, 42, 'floodplain_stream', 'recommendation', 'Stormwater by "soft" means: retain vegetation', None, None, None, None,
     'Non point sources should be addressed through proper stormwater management, concentrating on "soft" approaches such as proper site selection, minimizing impervious surfaces and retaining vegetation and other natural drainage systems',
     'Sentence continues: rather than "hard" engineering solutions, which the plan calls less effective and more costly. ' + FLOOD),
    (C10, 45, 'habitat_natural_area', 'recommendation', 'Protect the Cedar Glades from development', None, None, None, None,
     'The Glades constitute a rare and precious resource which should be protected from the impacts of development.', 'Cedar Glades around J. Percy Priest Reservoir.'),
    (C10, 45, 'tree_canopy', 'status_claim', 'Existing vegetation not protected vigorously enough (1992)', None, None, '1992', 'Metro Planning Commission',
     'While most newer developments plan for landscaping, existing vegetation is not protected vigorously enough.', 'Compare pair 23: tree rules enacted 2022.'),
    (C10, 45, 'tree_canopy', 'baseline', 'Replanting does not replace original growth for many years', None, None, None, None,
     'Even if a site is fully replanted, it takes many years, if ever, for the new vegetation to evolve and provide the same benefits as the original growth.', None),
    (C10, 45, 'forest_protection', 'baseline', 'Sensitive undeveloped land needs vegetative cover', None, None, None, None,
     'Environmentally sensitive areas are especially in need of vegetative cover to protect against erosion and water quality degradation.', None),
    (C10, 45, 'tree_canopy', 'commitment', 'Protect mature vegetation; require replanting when removed (Goal 1)', None, None, None, 'Metro Planning Commission',
     'Protect mature vegetation and require replanting in cases where existing vegetation is removed during construction.', 'Compare pair 23.'),
    (C10, 45, 'forest_protection', 'recommendation', 'Use trees along waterways as flood control', None, None, None, None,
     'Use trees along waterways as flood control devices.', FLOOD),
    (C10, 47, 'policy_mechanism', 'commitment', 'Protect rural areas from untimely development', '20', 'years', '2010', 'Metro Planning Commission',
     'Rural parts of the county that are not expected to develop in the next twenty years require protection from untimely development.', 'Compare NashvilleNext #323 and pair 24.'),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‐': '-', '­': '', '_': ''})
cache = {}
def variants(doc, p):
    if (doc, p) not in cache:
        t = open(f'{OCR}/{doc}/p{p}.txt', encoding='utf-8').read().translate(Q)
        # OCR can leave a blank line inside a hyphenated word, so allow whitespace around the break.
        cache[(doc, p)] = [n(t), n(re.sub(r'(\w)-[ \t]*\n\s*(\w)', r'\1\2', t)), n(re.sub(r'-\n', '-', t))]
    return cache[(doc, p)]

wb = openpyxl.load_workbook(XLSX)
have_src = {x[0] for x in wb['Sources'].iter_rows(min_row=2, values_only=True)}
have = {(r[0], str(r[1]), n(str(r[9]))) for r in wb['Commitments'].iter_rows(min_row=2, values_only=True) if r[0]}
bad = [(r[1], r[4][:40]) for r in ROWS if not any(n(r[9].translate(Q)) in v for v in variants(r[0], r[1]))]
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

# Scan rows carry 'PDF p<N>' in source_url, as the 1973 and 1981 rows do.
full = [[*r, 'verified_ocr', f'PDF p{r[1]}'] for r in ROWS]
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
