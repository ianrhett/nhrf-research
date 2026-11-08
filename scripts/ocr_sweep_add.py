"""Sweep of the 1973 and 1981 scans: rows the candidate finder surfaced in full OCR and a reader kept.

Usage: python3 ocr_sweep_add.py <ocr_dir> <commitments_dir> [--write]
ocr_dir (docs/research/sources/ocr/) holds <doc_id>/p<N>.txt, Tesseract OCR of every page made with ocr_page.sh (pdftoppm -r 250 -gray, then tesseract;
2026-10-22): 162 pages of the 1973 Natural Environmental Analysis and 355 of the General Plan 1980-2000.
Earlier rows from these scans came from partial OCR. find_candidates.py over the full OCR gave 580
candidates; 129 overlapped existing rows and 451 were read. Housing, streets, schools, bibliography,
map legends and restatements of existing rows were skipped; 44 kept. Every excerpt is rechecked against
the OCR of its page; the script exits without writing on any miss. Stray underscores, a scan artifact,
are dropped before matching. After --write: forest_priorities.py --write, cover_sheet.py.
"""
import csv, re, sys
import openpyxl
from copy import copy

OCR, CDIR = sys.argv[1:3]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'
NEA, GP = 'NEA_1973_Natural_Environmental_Analysis', 'General_Plan_1980_2000'
FLOOD = 'Compare FOREST-FLOOD-CHECK.md: the 2026 hazard and 2024 climate plans do not act on existing forest.'
BRIEF13 = 'Bears on the 2026 policy brief recommendation to compile runoff and landslide data.'

# doc, page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = [
    (NEA, 29, 'highland_rim_named_place', 'baseline', 'Highland Rim 2-3 degrees cooler with more rainfall than the basin', '300-400', 'feet higher than basin floor', None, None,
     'The Highland Rim area, which is 300 to 400 feet higher than the central basin floor, is known to have an average temperature 2° - 3° cooler and a more abundant rainfall.', None),
    (NEA, 84, 'forest_protection', 'baseline', 'Bodine-Cannon soils of the dissected Rim hamper development', None, None, None, None,
     'Development is hampered by the steepness of slopes, the high chert and rock content of the soils, and the natural low fertility that makes the establishment of plants difficult.',
     'Bodine-Cannon Association: steep cherty soils in the dissected Highland Rim and its outliers (same page).'),
    (NEA, 85, 'forest_protection', 'baseline', 'Trees on rock outcrop land cannot be reestablished once removed', None, None, None, None,
     'Once this vegetation is removed, reestablishment of trees and shrubs is nearly impossible due to the lack of soil cover.', 'Talbott soils and limestone outcrop areas.'),
    (NEA, 98, 'policy_mechanism', 'baseline', 'Septic fields on steep slopes run effluent unfiltered to streams', None, None, None, None,
     'If an absorption field is placed on a steep slope where there is a layer of dense clay, rock, or other impervious material near the surface, the effluent will flow above the impervious layer to the surface and run unfiltered down the hillsides to streams and waterways.',
     'The 1973 case for limiting development on Rim slopes without sewers; compare sewer rows.'),
    (NEA, 105, 'tree_canopy', 'baseline', 'Davidson County commercial forest share (1973)', '35.3', 'percent of county', '1973', None,
     'Expressed in terms of commercial forests, commercial being defined as those lands capable of growing trees that are both of commercial quality and available for that purpose, Davidson County is officially credited with 35.3 percent as compared to a statewide average of 50.6 percent.',
     'Commercial forest only. The same page puts all forested area at about 40-45 percent of the county.'),
    (NEA, 110, 'habitat_natural_area', 'baseline', 'Clearing cedar glades would be an ecological disaster', None, None, None, None,
     'The removal of trees and herbaceous cover from these areas would spell ecological disaster because the soil would soon wash away and revegetation in these rocky areas would be virtually futile.', 'Cedar Glades Woods community.'),
    (NEA, 136, 'forest_protection', 'baseline', 'Vertical cuts in Dellrose soils risk slippage', None, None, None, None,
     'Dellrose soil is on the steeper side slopes of the hills, and, if vertical cuts are made in them, there is likelihood of soil slippage above the vertical cut.', BRIEF13),
    (NEA, 136, 'forest_protection', 'baseline', 'Hilltop development can send runoff onto unstable slopes', None, None, None, None,
     'It is possible, however, that intensive development could cause excessive water runoff to the unstable side slope characterized by Dellrose and Mimosa soils.', None),
    (NEA, 136, 'forest_protection', 'baseline', 'Vegetation removal on critical soils hastens danger', None, None, None, None,
     'Removal and earthmoving in critical soil and geological areas will, in addition to hastening potential danger in these areas, also induce many other environmental problems.', 'Under the heading "Vegetation".'),
    (NEA, 137, 'highland_rim_named_place', 'status_claim', 'Preservation of the Escarpment justified on environmental grounds', None, None, '1973', 'Metro Planning Commission',
     'Justification for the preservation of the Highland Rim Escarpment was concluded on the basis of many environmental factors, which when analyzed, warn us of potential problems.',
     'Leads into the p137 conclusion that the Escarpment would better serve left generally in its natural state.'),
    (NEA, 138, 'policy_mechanism', 'recommendation', 'Cluster development must not harm surrounding natural area', None, None, None, None,
     'The cluster development should not adversely affect the surrounding natural area as might result from excessive runoff, erosion, or extensive cuts and fills.', None),
    (NEA, 138, 'forest_protection', 'baseline', 'Rim narrow valleys: walls densely wooded', None, None, None, None,
     'In addition to stream side vegetation, the valley walls are densely wooded and play host to an abundance of wild flowers.', 'Narrow valleys of the Escarpment, walls over 30 percent slope.'),
    (NEA, 141, 'highland_rim_named_place', 'status_claim', 'No other area as hostile to development as the Escarpment', None, None, None, None,
     'It is difficult to single out additional areas within the county that show the same degree of hostility as does the Highland Rim Escarpment.', None),
    (NEA, 143, 'forest_protection', 'baseline', 'Losing vegetated open space to paving could cause severe drainage problems', None, None, None, None,
     'However, as development intensifies increasing ground coverage with structures and paving, the amount of open space with vegetation to absorb the runoff will be reduced which could cause severe drainage problems.', FLOOD),
    (NEA, 148, 'forest_protection', 'baseline', 'Erosion from development up to 1,000 times that of woodland', '1000', 'times woodland erosion', None, None,
     'Soils eroded from high intensity development can be 1,000 times as great as that of a natural woodland area', FLOOD),
    (NEA, 148, 'floodplain_stream', 'recommendation', 'Study how development density affects runoff', None, None, None, None,
     'Additional study is needed to determine more specifically how the varying land development densities affect the runoff rates', BRIEF13),
    (NEA, 149, 'floodplain_stream', 'recommendation', 'Development in natural areas raises flooding; protective measures must be required', None, None, None, None,
     'It is quite obvious that increased development in the natural areas will increase flooding potential and, therefore, known protective and corrective measures must become part of the development pattern.', FLOOD),
    (GP, 54, 'policy_mechanism', 'commitment', 'Growth discouraged in remote rural areas', None, None, None, 'Metro Planning Commission',
     'Growth is permitted in other areas where services will be extended during the planning period but discouraged in more remote rural parts of Davidson County.', 'Compare NashvilleNext LUTI Policy 9.4 and pair 24.'),
    (GP, 89, 'policy_mechanism', 'recommendation', 'Sewer extension to low-density areas paid partly by those served', None, None, None, 'Metro Water and Sewerage Services',
     'It is recommended that sewer extension into such areas be financed in part by those benefitting from the service rather than by the rates derived from those now served.',
     'Low-density areas with lots over one acre. Bears on the 2026 policy brief recommendation to cap sewer expansion and right-size infrastructure costs.'),
    (GP, 193, 'policy_mechanism', 'commitment', 'Rural water in Conservation-Nonurban areas only for existing customers\' service', None, None, None, 'Metro Water and Sewerage Services',
     'In areas recommended for Conservation-Nonurban land use, extension of rural water facilities should be permitted provided adequate service to existing customers is maintained.', None),
    (GP, 197, 'policy_mechanism', 'commitment', 'Public sewers required only where urban development is planned', None, None, None, 'Metro Water and Sewerage Services',
     'Because of the health and environmental problems associated with urban development and on-site subsoil wastewater disposal systems, it is recommended that the present policy of requiring public sanitary sewers in all areas designated for urban development be continued.',
     'Pairs with p263: Conservation-Nonurban areas are not designated for urban development, so no sewer requirement applies.'),
    (GP, 201, 'policy_mechanism', 'status_claim', 'Sewer expansion cannot guide development for decades', None, None, '1981', 'Metro Planning Commission',
     'Although the importance of providing sewers to existing development is recognized, meeting those needs prior to extending sewers into areas of future development will take decades which would preclude the use of public sewer expansion programs as a means of guiding development for that period of time.', None),
    (GP, 204, 'floodplain_stream', 'recommendation', 'Monitor rainfall and runoff on all major streams', None, None, None, 'Metro Public Works',
     'precipitation and stream runoff should be continuously monitored for all of the major streams in Davidson County.', BRIEF13),
    (GP, 205, 'floodplain_stream', 'commitment', 'No increase in pre-development runoff where flooding is likely', None, None, None, 'Metro Public Works',
     'the pre-development runoff discharge rate of any site should not be increased as a result of development whenever there is a reasonable certainty that a change would contribute to a probable flooding problem.', None),
    (GP, 255, 'forest_protection', 'baseline', 'Steep slopes, unstable soils and landslides make development unwise in places', None, None, None, None,
     'In an urban setting, these limits include steep slopes and unstable soils restricting the types of activities and development that can safely or profitably occur and the hazards posed by potential floods and landslides that render development unwise at some locations.', None),
    (GP, 255, 'open_space', 'baseline', 'Natural areas matter more as private open space diminishes', None, None, None, None,
     'Enhancement of the most valued elements of the natural environment as a part of the urban community will take on added significance as growth occurs at increasing densities and privately held open space diminishes.', None),
    (GP, 256, 'forest_protection', 'baseline', 'Improper hillside development can cost lives', None, None, None, None,
     'Severe property damage and loss of life can be the consequence of improper hillside development.', BRIEF13),
    (GP, 256, 'forest_protection', 'baseline', 'Devegetated slopes increase runoff and flooding', None, None, None, None,
     'Devegetated slopes contribute to flood problems by increasing rates of runoff and siltation of stream channels.', FLOOD),
    (GP, 259, 'forest_protection', 'baseline', 'Bodine-Sulfura and Dellrose soils very unstable when wet', None, None, None, None,
     'The saturated soils on the sides of the slopes are Bodine-Sulfura and Dellrose - both very unstable when wet.', 'Figure 7-2. ' + BRIEF13),
    (GP, 260, 'forest_protection', 'baseline', 'Rugged area problems reach valleys and off-site properties', None, None, None, None,
     'These problems may affect properties in the valleys and other off-site areas as well as on the slopes and ridges.', 'Rugged Topographic Areas.'),
    (GP, 263, 'forest_protection', 'commitment', 'Prevent development on unstable soils and hazardous formations', None, None, None, 'Metro Planning Commission',
     'Efforts should be made to prevent development from occurring in areas with unstable soils or hazardous geologic formations.', None),
    (GP, 263, 'highland_rim_named_place', 'commitment', 'Conservation-Nonurban development only with wells or water and on-site disposal', None, None, None, 'Metro Planning Commission',
     'Development in the Conservation-Nonurban area should be limited to areas where wells or water service are available and where acceptable waste disposal methods can be arranged.',
     'Conservation-Nonurban encompasses most of the rugged topographic areas (p279). No sewer is contemplated; compare the 1973 septic limits (p98).'),
    (GP, 264, 'highland_rim_named_place', 'commitment', 'Fringe valleys and ridges of Conservation-Nonurban may be added to urban services', None, None, None, 'Metro Planning Commission',
     'Some valleys and ridges which penetrate the CN area along the fringe of urban areas may be suitable for urban development and could be logically added to the service areas of urban services.',
     'The 1981 opening for urban services at the Rim edge; p264 also gives Joelton-Whites Creek utility connection as an example.'),
    (GP, 264, 'policy_mechanism', 'recommendation', 'Use planned unit development to cluster and preserve the natural environment', None, None, None, 'Metro Planning Commission',
     'Development should be proposed under the planned unit concept in order to take advantage of additional design flexibility, to encourage cluster housing, and to preserve the natural environment.',
     'Precursor of the conservation subdivision promise (pairs 13 and 22).'),
    (GP, 266, 'floodplain_stream', 'recommendation', 'Conserve flood plains as open space', None, None, None, None,
     'Where appropriate, flood plains should be conserved as open space.', None),
    (GP, 268, 'floodplain_stream', 'recommendation', 'Base land use decisions on each watershed\'s flood potential', None, None, None, 'Metro Public Works',
     'The consequences of future urbanization in each watershed on flood potential should form the basis for land use decisions along each of the streams.', None),
    (GP, 275, 'habitat_natural_area', 'recommendation', 'Preserve options to protect natural landscapes less prone to catastrophe', None, None, None, None,
     'Broad options for future use and protection of natural landscapes and ecosystems less prone to catastrophe should be preserved.', None),
    (GP, 275, 'open_space', 'baseline', 'Growth will reduce privately held open space', None, None, '2000', None,
     'Normal growth on the periphery of the existing built-up area and infilling or redevelopment at higher densities in older parts of the city will reduce the amount of privately held open space over the course of the planning period.', None),
    (GP, 275, 'open_space', 'commitment', 'A policy framework needed to preserve the natural landscape', None, None, None, 'Metro Planning Commission',
     'A policy framework to guide public and private action will be necessary to preserve natural elements of the landscape for the use and enjoyment of future generations.', None),
    (GP, 278, 'greenways', 'baseline', 'Natural corridors work as stormwater management', None, None, None, None,
     'Preservation of open space and natural qualities in these corridors can be an effective storm water management technique in addition to its aesthetic contribution.', FLOOD),
    (GP, 279, 'highland_rim_named_place', 'recommendation', 'Accommodate urban use with preservation of scenic qualities', None, None, None, None,
     'As urban pressures reach into these areas, a functional accommodation between urban use and preservation of scenic qualities should be achieved.',
     'Scenic resources and corridors, including the Highland Rim Escarpment.'),
    (GP, 280, 'floodplain_stream', 'recommendation', 'Protect stream bank vegetation from removal', None, None, None, None,
     'Vegetation along the stream banks should be protected from indiscriminate removal in order to enhance the aesthetic value of the corridors as well as to control bank erosion.', None),
    (GP, 281, 'greenways', 'recommendation', 'Scenic arterials designed around vistas and natural areas', None, None, None, 'Metro Planning Commission',
     'Scenic arterials should be designed to take advantage of scenic vistas and natural areas and to control development as illustrated in Figure 7-8.',
     'Precedent for the 2026 policy brief Scenic Byways recommendation; McCrory Lane was classed a scenic arterial by amendment (p17).'),
    (GP, 281, 'tree_canopy', 'recommendation', 'Replace ground cover removed in construction', None, None, None, None,
     'Where feasible, ground cover removed during construction should be replaced with plant material suited to soil and climatic conditions.', None),
]

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '‐': '-', '­': '', '_': ''})
cache = {}
def variants(doc, p):
    if (doc, p) not in cache:
        t = open(f'{OCR}/{doc}/p{p}.txt', encoding='utf-8').read().translate(Q)
        cache[(doc, p)] = [n(t), n(re.sub(r'(\w)-\n(\w)', r'\1\2', t)), n(re.sub(r'-\n', '-', t))]
    return cache[(doc, p)]

wb = openpyxl.load_workbook(XLSX)
have = {(r[0], r[1], n(str(r[9]))) for r in wb['Commitments'].iter_rows(min_row=2, values_only=True) if r[0]}
bad = [(r[0][:3], r[1], r[4][:40]) for r in ROWS if not any(n(r[9].translate(Q)) in v for v in variants(r[0], r[1]))]
dup = [(r[0][:3], r[1]) for r in ROWS if (r[0], r[1], n(r[9])) in have or (r[0], str(r[1]), n(r[9])) in have]
print('rows', len(ROWS), 'bad', bad, 'dup', dup)
if bad or dup or '--write' not in sys.argv:
    sys.exit(1 if bad or dup else 0)

def append(ws, rows, width):
    last = max(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value is not None)
    for k, r in enumerate(rows, 1):
        for col in range(1, width + 1):
            s, d = ws.cell(last, col), ws.cell(last + k, col)
            d.value = r[col - 1]
            d.font, d.alignment, d.border, d.fill, d.number_format = copy(s.font), copy(s.alignment), copy(s.border), copy(s.fill), s.number_format

# Earlier rows from these scans carry 'PDF p<N>' in source_url; follow that.
full = [[*r, 'verified_ocr', f'PDF p{r[1]}'] for r in ROWS]
append(wb['Commitments'], full, 13)
append(wb['Highland Rim & named places'], [r for r in full if r[2] == 'highland_rim_named_place'], 12)

wb.save(XLSX)

def dump(name, path, skip_blank):
    rows = [['' if v is None else v for v in r] for r in wb[name].iter_rows(values_only=True)]
    if skip_blank:
        rows = [r for r in rows if any(x != '' for x in r)]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
dump('Commitments', f'{CDIR}/commitments.csv', False)
dump('Highland Rim & named places', f'{CDIR}/highland_rim.csv', False)
print('written')
