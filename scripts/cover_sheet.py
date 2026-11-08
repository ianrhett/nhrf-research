"""Write or rewrite the About tab (cover sheet) as the first sheet of NHRF_Commitments.xlsx.

Usage: python3 cover_sheet.py <NHRF_Commitments.xlsx>
Counts are computed here and written as numbers (previews such as Quick Look and GitHub do not
recalculate formulas), so rerun this script after any change to the other tabs, and after forest_priorities.py.
The About tab is explanatory text and has no CSV twin.
"""
import sys
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

XLSX = sys.argv[1]
GREEN = 'FF2F5D3A'

import datetime, os
PROMISE_TYPES = ('recommendation', 'commitment', 'target', 'funding_estimate', 'funding_allocated')
FOREST_CATS = ('forest_protection', 'tree_canopy', 'highland_rim_named_place', 'habitat_natural_area', 'land_acquisition', 'open_space')

wb = openpyxl.load_workbook(XLSX)
rows = [r for r in wb['Commitments'].iter_rows(min_row=2, values_only=True) if r[0]]
src = [c.value for c in wb['Sources']['A']]
N = {
    'docs': src.index('Total') - 1,
    'rows': len(rows),
    'promises': sum(r[3] in PROMISE_TYPES for r in rows),
    'forest': sum(r[3] in PROMISE_TYPES and r[2] in FOREST_CATS for r in rows),
    'baseline': sum(r[3] == 'baseline' for r in rows),
    'status_claim': sum(r[3] == 'status_claim' for r in rows),
    'definition': sum(r[3] == 'definition' for r in rows),
    'pairs': sum(isinstance(c.value, (int, float)) for c in wb['Promised_vs_Delivered']['A']),
    'incons': sum(1 for c in wb['Inconsistencies']['A'] if c.value) - 1,
    'rim': sum(1 for c in wb['Highland Rim & named places']['A'] if c.value) - 1,
    'ranked': sum(1 for c in wb['Forest_Priorities']['A'] if isinstance(c.value, int)),
    'top': sum(1 for c in wb['Forest_Priorities']['A'] if c.value == 5),
    'vol4': len({c.value for c in wb['NN_Vol4_Actions']['A'] if isinstance(c.value, int)}),
    'comments': sum(1 for c in wb['Public_Comments_Highland_Rim']['E'] if str(c.value).startswith('verified')),
}
srows = [r for r in wb['Sources'].iter_rows(min_row=2, max_row=src.index('Total'), values_only=True) if r[0]]
counted = {r[0] for r in srows if r[7] == 'yes'}
N['counted_docs'] = len(counted)
N['pending'] = sum(1 for r in srows if r[7] != 'yes' and str(r[8] or '').startswith('Pending extraction'))
N['background'] = len(srows) - N['counted_docs'] - N['pending']
crows = [r for r in rows if r[0] in counted]
N['c_promises'] = sum(r[3] in PROMISE_TYPES for r in crows)
N['c_actions'] = sum(r[3] in ('recommendation', 'commitment', 'target') for r in crows)
N['c_estimates'] = sum(r[3] == 'funding_estimate' for r in crows)
N['c_allocated'] = sum(r[3] == 'funding_allocated' for r in crows)
N['c_forest'] = sum(r[3] in PROMISE_TYPES and r[2] in FOREST_CATS for r in crows)
N['baseline_changes'] = sum(1 for c in wb['Inconsistencies']['K'] if str(c.value or '').startswith('BASELINE CHANGE'))
TODAY = os.environ.get('NHRF_ASOF') or datetime.date.today().isoformat()
_vf = os.path.join(os.path.dirname(os.path.abspath(XLSX)), 'VERSION')
VERSION_LINE = open(_vf, encoding='utf-8').read().split() if os.path.exists(_vf) else []
VERSION_TEXT = f'Version {VERSION_LINE[0]}, released {VERSION_LINE[1]}. Shared copies are in versions/ and named by version; NHRF_Commitments.xlsx is the working copy. See CHANGELOG.md.' if VERSION_LINE else 'Unreleased working copy.'

# (kind, col A, col B, col C); kind: title, h (section heading), th (table header), row, note
ROWS = [
    ('title', 'NHRF Commitments Workbook', None, None),
    ('note', VERSION_TEXT, None, None),
    ('note', 'What Metro Nashville recommended about forests, trees, open space, floodplains and the Highland Rim, quoted from its own plans, and whether it delivered. Every row quotes the source verbatim with a page number.', None, None),
    ('note', 'Maintained in https://github.com/ianrhett/nhrf under docs/research/commitments/. Each data tab has a CSV twin there; edit the workbook, then regenerate the CSVs.', None, None),
    (None, None, None, None),

    ('h', f'At a glance (as of {TODAY})', None, None),
    ('th', 'Measure', 'Count', 'How counted'),
    ('row', 'Documents listed', N['docs'], 'Rows on Sources above Total'),
    ('row', 'of which counted', N['counted_docs'], 'counted = yes on Sources: adopted plans and official final Metro documents, including codes, ordinances, resolutions, minutes, reports and a news release'),
    ('row', 'of which background, not counted', N['background'], 'Two drafts, a withdrawn bill, two advisory committee reports, a staff background report, the 2008 MPC minutes, and four delivery-evidence records (FY26 and FY27 Council CIB requests, the adopted FY2027 CIB and the FY2027 Council prioritization report; NHRF-MONEY-001)'),
    ('row', 'of which pending extraction, not counted', N['pending'], 'Listed in v1.6.0 after external review; no rows extracted yet'),
    ('row', 'Extracted rows (all kinds)', N['rows'], 'Rows on Commitments, all listed documents'),
    ('row', 'Recommendations, counted documents (all topics)', N['c_promises'], 'item_type is recommendation, commitment, target, funding_estimate or funding_allocated, in counted documents only. This is the figure to publish.'),
    ('row', 'of which actions (recommendation, commitment, target)', N['c_actions'], 'Things a document says Metro should or will do'),
    ('row', 'of which cost estimates (funding_estimate)', N['c_estimates'], 'An estimate is not a spending commitment'),
    ('row', 'of which money already allocated (funding_allocated)', N['c_allocated'], 'An appropriation is an implementation step, not an open recommendation'),
    ('row', 'Recommendations in Forest-related categories, counted documents', N['c_forest'], 'Counted-document recommendations whose category is forest_protection, tree_canopy, highland_rim_named_place, habitat_natural_area, land_acquisition or open_space. This is the figure to publish.'),
    ('row', 'Recommendations, all extracted documents (all topics)', N['promises'], 'Includes drafts, advisory reports and a withdrawn bill, which are not adopted Metro recommendations. Publish only with this label.'),
    ('row', 'Recommendations in Forest-related categories, all extracted documents', N['forest'], 'Same rule as above, all extracted documents. Publish only with this label.'),
    ('row', 'Stated facts (baseline)', N['baseline'], ''),
    ('row', 'Progress claims (status_claim)', N['status_claim'], ''),
    ('row', 'Definitions', N['definition'], ''),
    ('row', 'Recommendations scored on Forest_Priorities', N['ranked'], 'The Forest-related recommendations plus high-impact ones filed under funding or policy'),
    ('row', 'of which score 5 (protect existing forest)', N['top'], ''),
    ('row', 'Recommendations checked against delivery', N['pairs'], 'Pairs on Promised_vs_Delivered'),
    ('row', 'NashvilleNext Vol IV actions captured', N['vol4'], 'Distinct action numbers on NN_Vol4_Actions (all of them)'),
    ('row', 'Inconsistencies flagged', N['incons'], ''),
    ('row', 'of which baseline changes (not contradictions)', N['baseline_changes'], 'Figures that changed between dates; to reconcile'),
    ('row', 'Highland Rim and named-place rows', N['rim'], ''),
    ('row', 'Public comments naming the Highland Rim', N['comments'], ''),
    (None, None, None, None),

    ('h', 'Tabs', None, None),
    ('th', 'Tab', 'What it holds', 'Notes'),
    ('row', 'About', 'This cover sheet.', 'No CSV twin.'),
    ('row', 'Sources', 'One row per document read: title, date, status (adopted, draft, enacted), page count, official URL, and how many rows came from it. The counted column marks the 48 documents that count toward every number; six background documents (two drafts, a withdrawn bill, two advisory committee reports and a staff background report) and three documents pending extraction (added in v1.6.0) are not counted. repo_copy_note marks sources an external review could not open (HTTP 403); a copy needs to be stored in the repo.', 'The Total row and the two method notes under it are part of the tab.'),
    ('row', 'Promised_vs_Delivered', 'One row per recommendation checked against what Metro later reported or enacted, with an assessment.', 'Each recommendation and each delivery figure is also a row on Commitments (doc + page). The last row is a note.'),
    ('row', 'Forest_Priorities', 'Every Forest-related recommendation, plus high-impact recommendations filed under funding or policy, scored 1 to 5 for potential benefit to existing forest and grouped into families of the same recommendation restated across plans. Shows whether a stated deadline year has passed (due_passed), whether a NashvilleNext Vol IV window to begin work has passed (start_window_passed; these timeframes are begin-work windows, not completion deadlines), and whether it has been checked.', 'Written by forest_priorities.py; see Forest priority scores below. CSV: forest_priorities.csv.'),
    ('row', 'Recommendations', "The 19 distinct forest recommendations that Metro's plans repeat (P01-P19; P01-P12 are the core twelve), how often each was made, its implementation status and what was done, with evidence pointers to RECOMMENDATIONS-IMPLEMENTATION.md.", 'Built by recommendations_tab.py from promise_counts.csv and distinct_promises.csv. CSV: recommendations.csv.'),
    ('row', 'NN_Vol4_Actions', 'Every action in NashvilleNext Volume IV (2015): number, element, policy, timeframe, implementers, full text and page; 340 numbered actions, some listed under more than one policy.', 'Reference list; commitments_rows links actions that also have a Commitments row. Written by nn_vol4_parse.py and nn_vol4_add.py. CSV: nn_vol4_actions.csv.'),
    ('row', 'Commitments', 'Everything extracted from the documents. Despite the name, not every row is a recommendation: item_type says what kind of statement it is.', 'See item_type below.'),
    ('row', 'Inconsistencies', 'Rows where a figure conflicts with the same figure elsewhere. Same columns as Commitments.', 'See Inconsistencies below.'),
    ('row', 'Highland Rim & named places', 'A filtered copy of Commitments: every row whose category is highland_rim_named_place (the Highland Rim itself, or places on it such as Beaman Park, Bells Bend, Whites Creek, the Warner Parks, Joelton).', 'Not new data; the Forest-specific slice.'),
    ('row', 'Public_Comments_Highland_Rim', 'Resident comments naming the Highland Rim from the 2025 Plan to Play survey, as printed in Metro\'s adopted Appendix.', 'Public input, not Metro commitments.'),
    (None, None, None, None),

    ('h', 'Commitments columns', None, None),
    ('th', 'Column', 'Meaning', None),
    ('row', 'doc', 'Document ID; matches Sources.', None),
    ('row', 'pdf_page', 'Page index in the PDF (not the printed page number). For web pages or code, a section reference.', None),
    ('row', 'category', 'Topic (see Categories).', None),
    ('row', 'item_type', 'Kind of statement (see item_type).', None),
    ('row', 'metric', 'Short plain-language label.', None),
    ('row', 'value, unit', 'The number stated, if any, and its unit.', None),
    ('row', 'target_year', 'Deadline as stated: a year, or a timeframe such as "Near term (1-3 years)".', None),
    ('row', 'responsible_party', 'Who the document says is responsible.', None),
    ('row', 'excerpt', 'The source text, verbatim.', None),
    ('row', 'notes', 'Context, cross-references, and INCONSISTENT flags.', None),
    ('row', 'verify', 'How the excerpt was checked (see Verification).', None),
    ('row', 'source_url', 'Official URL of the document.', None),
    ('row', 'brief_rec', "Which of the Alliance policy brief's 19 recommendations (R01 to R19, brief order) this recommendation states, in whole or in part; semicolons separate several. Blank when none. See POLICY-BRIEF-VS-PLANS.md.", None),
    ('row', 'brief_match', 'full or partial for each brief_rec value, in the same order.', None),
    ('row', 'promise_id', 'For Forest action statements: which of the 19 distinct recommendations (P01 to P19; P01 to P12 are the core twelve; see the Recommendations tab) this statement repeats; context marks related rows that are not recommendations. Blank otherwise.', None),
    (None, None, None, None),

    ('h', 'item_type', None, None),
    ('th', 'Value', 'Meaning', 'Is it a recommendation?'),
    ('row', 'recommendation', 'Something the document says Metro should do.', 'Yes'),
    ('row', 'commitment', 'Something Metro says it will do.', 'Yes'),
    ('row', 'target', 'A measurable goal, often with a number and a year.', 'Yes'),
    ('row', 'funding_estimate', 'Estimated cost of an action. Not a spending commitment.', 'Yes, reported separately'),
    ('row', 'funding_allocated', 'Money actually appropriated or budgeted: an implementation step.', 'Yes, reported separately'),
    ('row', 'baseline', 'A stated fact or measurement at the time, such as acres of canopy or acres plantable, including modeled potential (such as maximum planting sites). What later claims get measured against.', 'No'),
    ('row', 'status_claim', 'Metro\'s own claim about progress, such as "940 acres added".', 'No'),
    ('row', 'definition', 'How a term, rule or threshold is defined.', 'No'),
    ('row', 'conditional_policy', 'A condition under which a plan permits something, such as development or extending urban services. Not a recommendation to act.', 'No'),
    (None, None, None, None),

    ('h', 'Categories', None, None),
    ('th', 'Value', 'Meaning', 'Counted as Forest-related above'),
    ('row', 'forest_protection', 'Protecting existing forest, hillsides and steep slopes.', 'Yes'),
    ('row', 'tree_canopy', 'Canopy cover, tree planting and tree rules (urban and countywide).', 'Yes'),
    ('row', 'highland_rim_named_place', 'The Highland Rim or a named place on it.', 'Yes'),
    ('row', 'habitat_natural_area', 'Habitat and natural areas.', 'Yes'),
    ('row', 'land_acquisition', 'Buying land or easements.', 'Yes'),
    ('row', 'open_space', 'Parks and conserved open space.', 'Yes'),
    ('row', 'floodplain_stream', 'Floodplains, streams and flooding.', 'No'),
    ('row', 'green_infrastructure', 'Rain gardens, green roofs, low-impact development.', 'No'),
    ('row', 'greenways', 'Greenway trails and corridors.', 'No'),
    ('row', 'funding', 'Funds and budgets.', 'No'),
    ('row', 'policy_mechanism', 'Ordinances, programs, procedures and other tools.', 'No'),
    (None, None, None, None),

    ('h', 'Forest priority scores', None, None),
    ('th', 'Score', 'Meaning', None),
    ('row', '5', 'Protects existing forest at scale with a binding rule or land protection: steep-slope and hillside rules, conservation subdivisions, tree protection on private land, keeping sewers and dense development out of rural and Rim land, buying or easing large natural lands, Highland Rim policy.', None),
    ('row', '4', 'Large measurable goals that would hold forest countywide: land conservation acreage goals, no net tree loss, countywide and rural canopy targets.', None),
    ('row', '3', 'Programs and plans that enable protection: natural area designation and management, wildlife corridors, invasives, canopy assessments, forest management plans.', None),
    ('row', '2', 'Adds trees or open land but protects little existing forest: planting programs, flood buyouts.', None),
    ('row', '1', 'Peripheral to the Forest: urban street trees and canopy targets, pocket parks, access, education, staffing.', None),
    ('note', 'Scores are a judgment of potential benefit if the recommendation were implemented, not of whether it was. Families are assigned by keyword rules on each row, with hand corrections listed in the script.', None, None),
    (None, None, None, None),

    ('h', 'Verification', None, None),
    ('th', 'verify value', 'Meaning', None),
    ('row', 'verified', 'A script found the excerpt, word for word, on the stated page of the official file.', None),
    ('row', 'verified_by_hand', 'Checked by a person, because the text is a table, chart label or broken by a graphic.', None),
    ('row', 'verified_ocr', 'Matched against OCR of an archival scan (1973 Natural Environmental Analysis, 1981 General Plan).', None),
    (None, None, None, None),

    ('h', 'Promised_vs_Delivered assessments', None, None),
    ('th', 'Value', 'Meaning', None),
    ('row', 'Met', 'Delivered as recommended.', None),
    ('row', 'Partly met', 'Some delivered, or delivered late or smaller.', None),
    ('row', 'Not met', 'Not delivered by a stated completion date, or a different and weaker tool was enacted. A NashvilleNext begin-work window is not a completion date.', None),
    ('row', 'Not yet due', 'Deadline has not passed.', None),
    ('row', 'Goal restated', 'A later document changes the baseline or the goal instead of reporting against it.', None),
    ('row', 'No status reported', 'No later document reports against the recommendation.', None),
    ('row', 'Not verified', 'The delivery evidence does not answer the recommendation or compares different measures; a further check is needed.', None),
    ('row', 'pct_delivered', 'A formula: delivered_value / promised_value, where both are numbers.', None),
    (None, None, None, None),

    ('h', 'Inconsistencies', None, None),
    ('note', 'Two kinds, not yet separated by a column. Within one document: the same figure given differently in two places, mostly minor (rounding, typos). Across documents: a figure that changes from one plan to the next, such as the 2017 parks baseline restated 785 acres lower in 2026. The notes column names the conflicting page or document. Notes that begin BASELINE CHANGE mark figures that changed between dates (growth or a change in scope): baselines to reconcile, not proven contradictions.', None, None),
    (None, None, None, None),

    ('h', 'Method', None, None),
    ('note', 'Documents were downloaded from their official URLs and read page by page. Rows were extracted selectively: recommendations, targets, stated facts, progress claims and definitions on the topics above, not every sentence. Each excerpt is then checked against the stated page before it is written. Build and add scripts are in artifacts/research-scripts/ in the repo.', None, None),
    ('note', 'Version 1.6.0 applies the accepted findings of the 2026-10-24 external review of version 1.5.1; its findings and notes are in docs/research/commitments/reviews/2026-10-24-sol/.', None, None),
    ('note', 'Coverage, exclusions, unverified points and open records requests are set out in docs/research/GAPS-AND-LIMITS.md. Every source, with its URL, retrieval date, SHA-256 fingerprint and cover image, is listed in docs/research/sources/MANIFEST.csv.', None, None),
    ('note', 'Write-ups that explain individual findings live next to the workbook in docs/research/: ENACTMENT-CHECKS.md, UFPP-2013-FLOOD-PLAN.md, FOREST-FLOOD-CHECK.md, STORMWATER-MASTER-PLAN-2025-DRAFT.md, FOREST-PROMISE-CHECKS.md, BEAMAN-PARK-2026.md, COMMUNITY-PLANS-RIM.md, NASHVILLENEXT-VOL1-LUTI.md, WHITES-CREEK-HEARINGS.md.', None, None),
]

if 'About' in wb.sheetnames:
    del wb['About']
ws = wb.create_sheet('About', 0)
wb.active = 0

base = Font(name='Arial', size=10)
bold = Font(name='Arial', size=10, bold=True)
white = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
fill = PatternFill('solid', fgColor=GREEN)
wrap = Alignment(wrap_text=True, vertical='top')

r = 0
for kind, a, b, c in ROWS:
    r += 1
    if kind is None:
        continue
    if kind == 'title':
        ws.cell(r, 1, a).font = Font(name='Arial', size=16, bold=True, color=GREEN)
    elif kind == 'h':
        ws.cell(r, 1, a).font = Font(name='Arial', size=12, bold=True, color=GREEN)
    elif kind == 'note':
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        cell = ws.cell(r, 1, a)
        cell.font, cell.alignment = base, wrap
        ws.row_dimensions[r].height = 15 * max(1, len(a) // 120 + 1)
    else:
        for col, v in enumerate((a, b, c), 1):
            if v is None:
                continue
            cell = ws.cell(r, col, v)
            cell.alignment = wrap
            if kind == 'th':
                cell.font, cell.fill = white, fill
            else:
                cell.font = bold if col == 1 else base
        if kind == 'row':
            longest = max(len(str(v or '')) for v in (b, c))
            ws.row_dimensions[r].height = 15 * max(1, longest // 70 + 1)

ws.column_dimensions['A'].width = 34
ws.column_dimensions['B'].width = 70
ws.column_dimensions['C'].width = 70
ws.sheet_view.showGridLines = False
ws.freeze_panes = None
wb.save(XLSX)
print('About tab written,', r, 'rows')
