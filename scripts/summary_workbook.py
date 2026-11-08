"""Write a read-only, plain-language summary workbook for a non-technical team, built from the CSVs.

Usage: python3 summary_workbook.py <commitments_dir>
Writes <commitments_dir>/versions/NHRF_Promises_Summary_v<VERSION>_<DATE>.xlsx, where VERSION and DATE are the two
fields of <commitments_dir>/VERSION. Refuses to overwrite an existing file. Reads sources.csv, commitments.csv,
promised_vs_delivered.csv, top5_timeline.csv, brief_rec_counts.csv, promise_counts.csv and promise_groups.csv (never the
xlsx). Documents marked counted = 'no' on sources.csv are left out of every number and list, and named in a note on
The Documents. All values are plain text and numbers, no formulas. Tabs: Start Here, The Scorecard, The Recommendations,
Every Time They Said It, Our Brief vs. Their Plans, The Documents.
"""
import csv, os, re, sys
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

CDIR = sys.argv[1]
PROMISE_TYPES = ('recommendation', 'commitment', 'target', 'funding_estimate', 'funding_allocated')
STATUS_ORDER = ['Not met', 'Partly met', 'No status reported', 'Goal restated', 'Not yet due', 'Met']
STATUS_PHRASE = {'Not met': 'not met', 'Partly met': 'partly met', 'No status reported': 'never reported on',
                 'Goal restated': 'restated as new goals', 'Not yet due': 'not yet due', 'Met': 'met'}
STATUS_FILL = {'Not met': 'F4CCCC', 'Partly met': 'FCE5CD', 'No status reported': 'E7E6E6', 'Goal restated': 'E7E6E6',
               'Not yet due': 'DDEBF7', 'Met': 'D9EAD3'}
PROTECTIONS = ['Limit building on steep slopes', 'Keep sewers and dense development out of rural Rim land',
               'Buy or ease large natural lands', 'Protect trees on private land', 'Conservation subdivisions with open space']
RECS = [
    ('Name the Forest a conservation priority area with defined boundaries', 'Partly'),
    ('Metro Water treats the Forest as a priority watershed and funds it in stormwater planning', 'Partly'),
    ('Pursue Tree City USA and Biophilic City designations', 'Partly'),
    ('Enforce against illegal dumping', 'Already said'),
    ('Publish a progress dashboard', 'Already said'),
    ('Re-fund the Conservation Assistance Fund and move it to Metro Water', 'Partly'),
    ('Identify new rules, zoning and tools to protect the Forest', 'Already said'),
    ('Transfer of development rights', 'Already said'),
    ('Move tree canopy and natural land management to Metro Water', 'Partly'),
    ('Set and fund land-buying targets in and around the Forest', 'Already said'),
    ('Fix the code: 50% open space in conservation subdivisions, tree protection', 'Already said'),
    ('Online map tracking priority and protected land', 'Partly'),
    ('Compile and publish storm runoff and landslide history', 'Partly'),
    ('Regional conservation with surrounding counties', 'Already said'),
    ('Highland Rim Forest scenic byway', 'Partly'),
    ('Park-to-Park and Rim-to-River trails', 'Partly'),
    ('Cap sewer expansion into Forest conservation areas', 'Already said'),
    ('Marketing Nashville as a forest city', 'Not found'),
    ('State and federal programs (Forest Legacy, Wildlife Action Plan)', 'Not found'),
]
VERDICT_FILL = {'Already said': 'D9EAD3', 'Partly': 'FCE5CD', 'Not found': 'E7E6E6'}
GREEN, GRAY = '2E5E3E', '808080'
BORDER = Border(*(Side(style='thin', color='D9D9D9'),) * 4)


def read(name):
    return list(csv.DictReader(open(f'{CDIR}/{name}', encoding='utf-8')))


def fill(color):
    return PatternFill('solid', start_color=color, end_color=color)


def num(s):
    return (0, int(s)) if str(s).isdigit() else (1, 0)


def header(ws, titles, widths):
    for i, (t, w) in enumerate(zip(titles, widths), 1):
        c = ws.cell(1, i, t)
        c.font, c.fill = Font(name='Calibri', size=12, bold=True, color='FFFFFF'), fill(GREEN)
        c.alignment = Alignment(wrap_text=True, vertical='center')
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = 'A2'


def body(ws, r, values, fills=None):
    for i, v in enumerate(values, 1):
        c = ws.cell(r, i, v)
        c.font, c.border = Font(name='Calibri', size=12), BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if fills and i in fills:
            c.fill = fill(fills[i])


def finish(ws, color, autofilter=True):
    if autofilter:
        ws.auto_filter.ref = f'A1:{ws.cell(1, ws.max_column).column_letter}{ws.max_row}'
    ws.sheet_properties.tabColor = color
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr = openpyxl.worksheet.properties.PageSetupProperties(fitToPage=True)


VERSION, DATE = open(f'{CDIR}/VERSION', encoding='utf-8').read().split()[:2]
OUT = f'{CDIR}/versions/NHRF_Promises_Summary_v{VERSION}_{DATE}.xlsx'
if os.path.exists(OUT):
    sys.exit(f'refusing to overwrite {OUT}')

allsrc = {r['doc']: r for r in read('sources.csv') if r['doc'] and r['source_url'].startswith('http')}
src = {d: r for d, r in allsrc.items() if r.get('counted') != 'no'}  # counted documents only
background = [r for r in allsrc.values() if r.get('counted') == 'no']
year = lambda d: int((re.search(r'(19|20)\d\d', allsrc[d]['date']) or re.search(r'(19|20)\d\d', d)).group(0))
promises = {}
for r in read('commitments.csv'):
    if r['item_type'] in PROMISE_TYPES:
        promises[r['doc']] = promises.get(r['doc'], 0) + 1
pairs = [p for p in read('promised_vs_delivered.csv') if p['pair'].isdigit() and p['promise_doc'] in src]
top5 = read('top5_timeline.csv')
recs = {r['rec']: r for r in read('brief_rec_counts.csv')}
total = next(r for r in recs.values() if r['rec'].startswith('Total'))
pc = sorted(read('promise_counts.csv'), key=lambda r: (r['priority'] != 'Core', r['promise_id']))  # Core first, then by id
pc_by_id = {r['promise_id']: r for r in pc}
PC_TIMES = sum(int(r['times']) for r in pc)
PC_DOCS = len({g['doc'] for g in read('promise_groups.csv') if g['promise_id'] in pc_by_id and g['doc'] in src})
PC_FIRST, PC_LAST = min(int(r['first_year']) for r in pc if r['first_year']), max(int(r['last_year']) for r in pc if r['last_year'])
pcs = lambda st: sum(r['status'] == st for r in pc)
core = [r for r in pc if r['priority'] == 'Core']
C_TIMES = sum(int(r['times']) for r in core)
ccs = lambda st: sum(r['status'] == st for r in core)
done = [r['promise'] for r in pc if r['status'] == 'Implemented']
if not done:
    DONE_LINE = f"• None of the {len(pc)} has been fully implemented."
else:
    DONE_LINE = f"• Of all {len(pc)}, {len(done)} {'has' if len(done) == 1 else 'have'} been fully implemented: {'; '.join(done)}."
if ccs('Implemented') or ccs('Not implemented'):
    CORE_LINE = (f"• The {len(core)} that would protect the forest most were recommended {C_TIMES} times: {ccs('Not implemented')} not implemented, "
                 f"{ccs('Partly implemented')} partly implemented, {ccs('No implementation reported')} with no implementation ever reported, {ccs('Implemented')} fully implemented.")
else:
    CORE_LINE = (f"• The {len(core)} that would protect the forest most were recommended {C_TIMES} times. None has been fully implemented: "
                 f"{ccs('Partly implemented')} partly implemented, {ccs('No implementation reported')} with no implementation ever reported.")

wb = openpyxl.Workbook()

# Tab 1: Start Here
ws = wb.active
ws.title = 'Start Here'
ws.column_dimensions['A'].width = 100
syears = [year(d) for d in src]
t_years = [int(r['year']) for r in top5]
counts = {s: sum(p['assessment'] == s for p in pairs) for s in STATUS_ORDER}
count_text = ', '.join(f'{counts[s]} {STATUS_PHRASE[s]}' for s in STATUS_ORDER if counts[s])
all_rows = int(total['full_rows']) + int(total['partial_rows'])
P = len(pairs)
LINES = {
    1: ("What Metro's plans recommended for Nashville's Highland Rim Forest, and what was done", 18, 'b'),
    3: (f"Our policy brief's recommendations appear {total['full_rows']} times in {total['full_docs']} Metro documents since {total['full_first']}.", 14, 'b'),
    4: (f"Each count is a separate quoted statement in a Metro plan. Counting partial matches too: {all_rows} statements in {total['all_docs']} documents.", 11, 'i'),
    6: ('The numbers that matter', 14, 'b'),
    7: (f"• Metro's own plans made {len(pc)} forest recommendations {PC_TIMES} times in {PC_DOCS} documents, {PC_FIRST} to {PC_LAST}.", 12, ''),
    8: (CORE_LINE, 12, ''),
    9: (DONE_LINE, 12, ''),
    10: ('• Money for land: Plan to Play (2017) said Metro needed $534 million to buy the parkland it recommended. Metro set aside $12.8 million by 2026, about 2.4 percent.', 12, ''),
    11: ('• The 2011 Open Space Plan set a goal of 22,000 acres of new conserved land by 2035. No later Metro plan mentions that goal.', 12, ''),
    12: (f'• This summary draws on {len(src)} Metro documents from {min(syears)} to {max(syears)}.', 12, ''),
    14: ("What's in this workbook", 14, 'b'),
    15: (f'The Scorecard: {P} specific targets and deadlines Metro set, and what happened to each.', 12, ''),
    16: ('The Recommendations: each one, how often Metro\'s plans made it, and whether it was implemented.', 12, ''),
    17: ('Every Time They Said It: the exact quote each time, by recommendation.', 12, ''),
    18: ("Our Brief vs. Their Plans: the Alliance's 19 recommendations, and how often Metro already said the same thing.", 12, ''),
    19: ('The Documents: every plan we read, with a link to read it yourself.', 12, ''),
    21: (f"Every quote is word for word from the Metro document and page shown. The full research workbook (NHRF_Commitments, version {VERSION}) has every detail, check and source note. Prepared by the Alliance to Conserve Nashville's Highland Rim Forest, {DATE}.", 11, 'g'),
}
for row, (text, size, style) in LINES.items():
    c = ws.cell(row, 1, text)
    c.font = Font(name='Calibri', size=size, bold=style == 'b', italic=style in ('i', 'g'), color='595959' if style == 'g' else '000000')
    c.alignment = Alignment(wrap_text=True, vertical='top')
finish(ws, GREEN, autofilter=False)
ws.sheet_properties.tabColor = GREEN
counts_out = {'Start Here': len(LINES)}

# Tab 2: The Scorecard
ws = wb.create_sheet('The Scorecard')
header(ws, ['Target or deadline Metro set', 'In which plan', 'Year set', 'Deadline', 'What happened', 'Status'], [50, 34, 10, 11, 60, 18])
pairs.sort(key=lambda p: (STATUS_ORDER.index(p['assessment']), year(p['promise_doc'])))
for r, p in enumerate(pairs, 2):
    body(ws, r, [re.sub(r'^(?:[A-Z]{2,4} \d+(?:\.\d+)?(?: / [A-Z]{2,4} \d+(?:\.\d+)?)* )?#\d+: ', '', p['promise']), src[p['promise_doc']]['title'], year(p['promise_doc']), p['due'] or '', p['reported_2026'], p['assessment']],
         {6: STATUS_FILL[p['assessment']]})
finish(ws, GRAY)
counts_out['The Scorecard'] = len(pairs)

# Tab 3: The Promises
ws = wb.create_sheet('The Recommendations')
header(ws, ["Metro's plans recommended:", 'Priority', 'Times', 'In how many documents', 'First recommended', 'Status', 'What happened'], [46, 11, 8, 12, 10, 16, 60])
PROMISE_FILL = {'Not implemented': 'F4CCCC', 'Partly implemented': 'FCE5CD', 'No implementation reported': 'E7E6E6', 'Implemented': 'D9EAD3'}
for r, p in enumerate(pc, 2):
    body(ws, r, [p['promise'], p['priority'], int(p['times']), int(p['docs']), int(p['first_year']) if p['first_year'] else '', p['status'], p['what_happened']],
         {6: PROMISE_FILL[p['status']]})
finish(ws, GRAY)
counts_out['The Recommendations'] = len(pc)

# Tab 3b: Every Time They Said It
ws = wb.create_sheet('Every Time They Said It')
header(ws, ['Year', 'Plan', 'Page', 'What it says (exact quote)'], [8, 40, 8, 100])
com = read('commitments.csv')
quotes = []
for g in read('promise_groups.csv'):
    if g['promise_id'] in pc_by_id and g['doc'] in src:
        c = com[int(g['row']) - 2]
        assert (c['doc'], c['pdf_page']) == (g['doc'], g['pdf_page']), g['row']
        quotes.append((g['promise_id'], year(g['doc']), g['doc'], g['pdf_page'], c['excerpt']))
r, n = 2, 0
for p in pc:
    rows = sorted((q for q in quotes if q[0] == p['promise_id']), key=lambda q: (q[1], q[2], num(q[3]), q[3]))
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
    c = ws.cell(r, 1, f"{p['promise']}: recommended {p['times']} times in {p['docs']} documents, {p['first_year']} to {p['last_year']}")
    c.font, c.fill = Font(name='Calibri', size=13, bold=True), fill('E2EFDA')
    c.alignment = Alignment(wrap_text=True, vertical='center')
    r += 1
    for q in rows:
        body(ws, r, [q[1], src[q[2]]['title'], q[3], q[4]])
        r, n = r + 1, n + 1
finish(ws, GRAY, autofilter=False)
counts_out['Every Time They Said It'] = n

# Tab 4: Our Brief vs. Their Plans
ws = wb.create_sheet('Our Brief vs. Their Plans')
header(ws, ['When', 'Our recommendation', 'Has Metro already said this?', 'Times Metro said it (in full)', 'Times incl. partial',
            'In how many documents', 'Since'], [11, 55, 18, 14, 14, 14, 10])
for i, (name, verdict) in enumerate(RECS, 1):
    c = recs[f'R{i:02d}']
    when = 'Right away' if i <= 5 else 'Next 1-3 years' if i <= 13 else 'Long term'
    body(ws, i + 1, [when, name, verdict, int(c['full_rows']), int(c['full_rows']) + int(c['partial_rows']), int(c['all_docs']),
                     c['all_first'] or ''], {3: VERDICT_FILL[verdict]})
note = ("'In full' means a Metro document calls for the same action. 'Partial' means the same aim but only part of it, or a weaker form. "
        "Each count is a separate quoted statement. R05: Metro's 2024 climate plan commits to a dashboard (page 119), but that sentence "
        "is not one of the counted statements.").replace('R05', 'The dashboard')
nr = len(RECS) + 3
ws.merge_cells(start_row=nr, start_column=1, end_row=nr, end_column=7)
c = ws.cell(nr, 1, note)
c.font, c.alignment = Font(name='Calibri', size=11, italic=True), Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[nr].height = 50
finish(ws, GRAY, autofilter=False)
ws.auto_filter.ref = f'A1:G{len(RECS) + 1}'
counts_out['Our Brief vs. Their Plans'] = len(RECS)

# Tab 5: The Documents
ws = wb.create_sheet('The Documents')
header(ws, ['Year', 'Document', 'Status', 'Recommendations and targets we pulled from it', 'Read it'], [8, 60, 34, 14, 40])
for r, d in enumerate(sorted(src, key=lambda d: (year(d), src[d]['title'])), 2):
    s = src[d]
    body(ws, r, [year(d), s['title'], s['status'], promises.get(d, 0), s['source_url']])
    link = ws.cell(r, 5)
    link.hyperlink = s['source_url']
    link.font = Font(name='Calibri', size=12, color='0563C1', underline='single')
finish(ws, GRAY)
nr = len(src) + 3
ws.merge_cells(start_row=nr, start_column=1, end_row=nr, end_column=5)
c = ws.cell(nr, 1, 'Also read but not counted: ' + '; '.join(f"{b['title']} ({b['not_counted_reason']})" for b in background))
c.font, c.alignment = Font(name='Calibri', size=11, italic=True), Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[nr].height = 80
ws.auto_filter.ref = f'A1:E{len(src) + 1}'
counts_out['The Documents'] = len(src)

wb.active = 0
wb.save(OUT)
print(OUT)
for k, v in counts_out.items():
    print(f'{k}: {v} rows')
