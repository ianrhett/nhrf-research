"""Add Metro Code 17.28.030, MPC minutes 2022-04-28 and BL2006-1046 as Sources and Commitments rows.

Usage: python3 enactment_sources_add.py <dl_dir> <commitments_dir> [--write]
  dl_dir holds mpc/p{N}.txt (pdftotext -f N -l N of MPC-220428m.pdf) and bl2006_1046.htm.
Metro Code excerpts are checked against Municode page text in a browser (Municode serves
no static HTML); the script cannot refetch them and trusts CODE_CHECKED.
Exits without writing if any MPC or BL2006-1046 excerpt is not found on its stated page.
"""
import csv, html, re, sys
import openpyxl
from copy import copy

DL, CDIR = sys.argv[1], sys.argv[2]
XLSX = f'{CDIR}/NHRF_Commitments.xlsx'

CODE = 'Metro_Code_17.28.030'
MPC = 'MPC_Minutes_2022-04-28'
BL = 'Ordinance_BL2006-1046'
URL = {
    CODE: 'https://library.municode.com/tn/metro_government_of_nashville_and_davidson_county/codes/code_of_ordinances?nodeId=CD_TIT17ZO_CH17.28ENOPPEST',
    MPC: 'https://www.nashville.gov/sites/default/files/2022-05/MPC-220428m.pdf',
    BL: 'https://legisarchive.nashville.gov/mc/ordinances/term_2003_2007/bl2006_1046.htm',
}
CODE_CHECKED = 'Matched against Municode page text 2026-10-22.'

SOURCES = [
    [CODE, 'Metro Code of Laws 17.28.030, Hillside development standards (Title 17 Zoning, Chapter 17.28)',
     'Read on Municode October 22, 2026; last amended by BL2022-1121 (2022)', 'In force (current codified text)', None, URL[CODE]],
    [MPC, 'Metropolitan Planning Commission Minutes, April 28, 2022 (item 13a: 2022Z-004TX-001, BL2022-1121 Conservation Development)',
     'April 28, 2022', 'Final minutes (PDF created May 10, 2022)', 75, URL[MPC]],
    [BL, 'Ordinance BL2006-1046: conservation subdivision standards for AG, AR2a, R80, RS80, R40 and RS40 districts (proposed Metro Code 17.12.120)',
     'Introduced April 4, 2006', 'Not enacted: deferred indefinitely August 15, 2006; withdrawn August 21, 2007', None, URL[BL]],
]

# page, category, item_type, metric, value, unit, target_year, responsible_party, excerpt, notes
ROWS = {
    CODE: [
        ('17.28.030.A', 'policy_mechanism', 'definition', 'Residential hillside grading and clearing threshold', '20', 'percent natural slope', None, 'Metro Planning Commission',
         'The development of residentially zoned property shall minimize changes in grade, cleared area, and volume of cut or fill on those hillside portions of the property with twenty percent or greater natural slopes.',
         'Standard is "minimize", not a limit. NashvilleNext Vol IV #210 (2015, due 2018) asked to minimize development on greater than 15% slopes; see promised_vs_delivered pair 21.'),
        ('17.28.030.A.1', 'policy_mechanism', 'definition', 'Single and two-family lots of one acre or more exempt', '1', 'acre (lot size)', None, None,
         'The following provisions of this section shall not apply to single or two-family lots equal to or greater than one acre in size.',
         'Exemption applies to the lot provisions of 17.28.030.'),
        ('17.28.030.A.1', 'forest_protection', 'definition', 'Lots under one acre keep slopes of 25% or more outside building envelope', '25', 'percent natural slope', None, 'Metro Planning Commission',
         'For lots of less than one acre, any natural slopes equal to or greater than twenty-five percent shall be platted outside of the building envelope and preserved to the greatest extent possible in a natural state.',
         'The Planning Commission may authorize such lots as critical lots under conditions a to g.'),
        ('17.28.030.A.2', 'policy_mechanism', 'definition', 'Subdivisions on 20%+ slopes must use Conservation Development', '20', 'percent slope', '2022', 'Metro Planning Commission',
         'Single and/or two-family subdivisions in areas characterized by twenty percent or greater slopes shall employ the conservation development provisions of Section 17.12.090.',
         'Added by BL2022-1121 section 5 (MPC minutes 2022-04-28 p18). Replaced the cluster lot option reference.'),
        ('17.28.030.A.2', 'open_space', 'recommendation', 'Large areas of slopes over 25% to be recorded as open space', '25', 'percent natural slope', None, None,
         'Large contiguous areas containing natural slopes in excess of twenty-five percent should be recorded as either common or natural open space and permanently maintained in a natural state.',
         '"Should", not "shall".'),
        ('17.28.030.A.3', 'policy_mechanism', 'definition', 'ISR reduced from 15% slopes for multifamily and nonresidential forms', '15', 'percent natural slope', None, None,
         'manipulation of the natural slopes by grading shall result in an effective impervious surface ratio (ISR) for those portions disturbed as shown in Table 17.28.030A.',
         'Table 17.28.030A: ISR x 0.66 at 15 to under 20% slopes, x 0.33 at 20 to under 25%, x 0 at 25%+. Applies to multifamily or nonresidential development in residential districts (RM40 and denser excepted); Table 17.28.030B applies the same factors in nonresidential districts. Single and two-family development has no 15% rule.'),
        ('history note', 'policy_mechanism', 'status_claim', 'Amendments to 17.28.030 since NashvilleNext adoption (June 2015)', '3', 'ordinances', None, 'Metro Council',
         '(Ord. BL2022-1121 § 5, 2022; Ord. BL2019-111 § 1(Exh. A, §§ 36, 37), 2020; Ord. BL2015-1153 § 16, 2015;',
         'BL2015-1153 added -A district names; BL2019-111 added -NS district names; BL2022-1121 added A.2 Conservation Development. None lowers the residential threshold to 15%. See docs/research/ENACTMENT-CHECKS.md.'),
    ],
    MPC: [
        (12, 'open_space', 'baseline', 'Cluster lot option minimum open space (before 2022)', '15', 'percent of gross acreage', None, None,
         'The current standards require a minimum of 15 percent of the gross acreage of the site be set aside as open space.',
         'Standard replaced by Conservation Development under BL2022-1121.'),
        (12, 'policy_mechanism', 'commitment', 'Separate zoning tool for unconstrained sites', None, None, '2022', 'Metro Planning Department',
         'staff anticipates bringing a proposal to the commission at their July meeting.',
         'July 2022. Delivery of this second tool is not checked in this workbook.'),
        (12, 'policy_mechanism', 'target', 'Proposed Conservation Development effective date', None, None, '2022', 'Metro Planning Department',
         'Staff recommends an effective date of September 14, 2022',
         'Applications filed for the September 14, 2022 deadline and after.'),
        (13, 'policy_mechanism', 'definition', 'Conservation Development trigger: minimum natural area on site', '10', 'percent of site', None, None,
         'The second requirement is that the development site must have at minimum 10 percent natural area.',
         'First requirement: site at least ten times the base district minimum lot size.'),
        (13, 'policy_mechanism', 'definition', 'Conservation Development is required, not by right', None, None, None, None,
         'When the criteria of development size and presence of natural features are met, this style of development would be required.',
         'NashvilleNext Vol IV #182 (2015) asked for a conservation subdivision ordinance by right with 50% open space; see promised_vs_delivered pair 22.'),
        (14, 'open_space', 'definition', 'Conservation Development preservation threshold', '20', 'percent of site', None, None,
         'Another minimum standard established in this amendment is the 20 percent preservation requirement threshold.',
         'If natural areas are 20% of the site or less, all must be preserved; if more, at least 20%. Compare 50% in BL2006-1046 and NashvilleNext #182.'),
        (16, 'forest_protection', 'definition', 'Steep slopes counted as natural area', '20', 'percent slope', None, None,
         'c. Areas of natural slopes of 20% or greater of at least 10,000 square foot contiguous area;',
         'Second substitute BL2022-1121, proposed 17.12.090.B.2.c.'),
        (16, 'open_space', 'definition', 'Minimum natural open space where natural areas exceed 20% of site', '20', 'percent of site', None, None,
         'If more than 20 percent of the site contains natural areas, then a minimum of 20 percent of the site shall be set aside as natural open space.',
         'Proposed 17.12.090.D.1.b.ii.'),
        (17, 'policy_mechanism', 'definition', 'Floor on lot size reduction', '3750', 'square feet', None, None,
         '4. In no case shall the minimum lot size be reduced below 3,750 square feet.',
         'Proposed 17.12.090.D.4.'),
        (21, 'policy_mechanism', 'status_claim', 'Planning Commission vote on BL2022-1121 (RS2022-117)', '6-0', 'vote', '2022', 'Metro Planning Commission',
         'Ms. Johnson moved and Mr. Henley seconded the motion to approve with a second substitute and direct staff to prepare a housekeeping amendment to the Metro Subdivision Regulations. (6-0)',
         'Council third reading May 17, 2022 per NTCC; code history note confirms 2022 enactment.'),
    ],
    BL: [
        (1, 'open_space', 'definition', 'Conservation subdivision defined as 50% or more open space', '50', 'percent of land area', None, 'Metro Council',
         'means a residential development where at least 50 percent or more of the land area is designated as undivided, permanent open space or farmland',
         'Proposed Metro Code 17.04.060.B. Sponsors David Briley, Brenda Gilmore. Not enacted.'),
        (1, 'open_space', 'target', 'Conserve at least 50% of tract in natural condition', '50', 'percent of tract', None, None,
         'In order to provide for the flexibility to conserve at least 50 percent of a tract of land in its natural condition, lots in conservation subdivisions in the AG, AR2a, RS80, R80, RS40 and R40 zoning districts may be arranged',
         'Proposed 17.12.120. Optional ("may"), limited to six low-density districts.'),
        (1, 'policy_mechanism', 'status_claim', 'Planning Commission approval of BL2006-1046', '9-0', 'vote', '2006', 'Metro Planning Commission',
         'Referred to: Planning Commission - Approved 9-0 (March 9, 2006)',
         'Passed second reading May 4, 2006.'),
        (1, 'policy_mechanism', 'status_claim', 'BL2006-1046 deferred indefinitely, then withdrawn', None, None, '2007', 'Metro Council',
         'Deferred Indefinitely : August 15, 2006 Withdrawn: August 21, 2007',
         'The 50% conservation subdivision was not enacted. Open Space Plan 2011 (pair 13) and NashvilleNext #182 (pair 22) asked for it again.'),
    ],
}

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
QUOTES = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"'})
bl_text = n(html.unescape(re.sub(r'<[^>]+>', ' ', open(f'{DL}/bl2006_1046.htm', encoding='latin-1').read())))

out, bad = [], []
for doc, rows in ROWS.items():
    for page, cat, it, metric, value, unit, ty, rp, ex, notes in rows:
        if doc == MPC:
            ok = n(ex.translate(QUOTES)) in n(open(f'{DL}/mpc/p{page}.txt', encoding='utf-8').read().translate(QUOTES))
            note = notes
        elif doc == BL:
            ok = n(ex) in bl_text
            note = notes
        else:
            ok = True
            note = f'{notes} {CODE_CHECKED}'
        if not ok:
            bad.append((doc, page, metric))
        if '—' in metric + note:
            bad.append((doc, page, 'emdash'))
        out.append([doc, page, cat, it, metric, value, unit, ty, rp, ex, note, 'verified', URL[doc]])

print('rows', len(out), 'bad', bad)
if bad or '--write' not in sys.argv:
    sys.exit(1 if bad else 0)

wb = openpyxl.load_workbook(XLSX)
have = {r[0] for r in wb['Sources'].iter_rows(min_row=2, values_only=True)}
assert not have & set(URL), 'sources already present'

# Commitments: append below the last row, copying the previous row's styles
ws = wb['Commitments']
last = ws.max_row
for row in out:
    ws.append(row)
    for col in range(1, 14):
        src, dst = ws.cell(last, col), ws.cell(ws.max_row, col)
        dst.font, dst.alignment, dst.border, dst.fill, dst.number_format = copy(src.font), copy(src.alignment), copy(src.border), copy(src.fill), src.number_format

# Sources: insert before Total, move Total and the notes block down
ws = wb['Sources']
total_r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'Total')
tail = [[(c.value, c._style) for c in ws[r]] for r in range(total_r, ws.max_row + 1)]
style = [c._style for c in ws[total_r - 1]]
k = len(SOURCES)
for i, s in enumerate(SOURCES):
    r = total_r + i
    for col, v in enumerate(s + [f'=COUNTIF(Commitments!$A:$A,A{r})'], 1):
        ws.cell(r, col).value = v
        ws.cell(r, col)._style = copy(style[col - 1])
for i, cells in enumerate(tail):
    for col, (v, st) in enumerate(cells, 1):
        c = ws.cell(total_r + k + i, col)
        c.value, c._style = v, copy(st)
ws.cell(total_r + k, 7).value = f'=SUM(G2:G{total_r + k - 1})'
wb.save(XLSX)

# CSVs mirror the sheets (Sources csv drops blank rows, as before)
def dump(name, path, skip_blank):
    rows = [['' if v is None else v for v in r] for r in wb[name].iter_rows(values_only=True)]
    if skip_blank:
        rows = [r for r in rows if any(x != '' for x in r)]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
dump('Commitments', f'{CDIR}/commitments.csv', False)
dump('Sources', f'{CDIR}/sources.csv', True)
print('written')
