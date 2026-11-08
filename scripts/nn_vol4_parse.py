"""Parse every action in NashvilleNext Volume IV (Actions, adopted June 22, 2015) into a CSV.

Usage: python nn_vol4_parse.py <next-volume4-Actions.pdf> <out.csv>   (needs pypdf)
Reads pdftotext -layout output page by page. An action starts at a timeframe in the left column
(Near term, Mid-term, Long-term, Ongoing), runs through its text and "Implementers:" line, and ends
at the action number in the right margin. Element and policy codes (e.g. "NR 1.1") carry forward.
The PDF's font drops the "ti" and "tt" ligatures from pdftotext output (they come out as spaces);
each action is re-matched against pypdf's text for the same page, where they appear as U+019F and
U+01A9, and those are mapped back. 377 timeframe markers yield 377 entries; numbers absent from the
document (35 between 1 and 375) are gaps in Metro's numbering.
"""
import csv, re, subprocess, sys
import pypdf

PDF, OUT = sys.argv[1:3]
Q = str.maketrans({'‐': '-', '‑': '-', '’': "'", '‘': "'", '“': '"', '”': '"', '–': '-', '—': '-'})
count = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', PDF], capture_output=True, text=True).stdout).group(1))
TF = re.compile(r'^\s{0,4}(Near term|Mid-term|Mid term|Long-term|Long term|Ongoing)\b')
CODE = re.compile(r'^\s{0,4}([A-Z]{2,5}(?: [A-Z]{1,3})? \d+(?:\.\d+)?)\s*$')
NUM = re.compile(r'\s{3,}(\d{1,3})\s*$')
ELEMENTS = {'LUTI': 'Land Use, Transportation & Infrastructure', 'ACC': 'Arts, Culture & Creativity', 'EWD': 'Economic & Workforce Development',
            'EY': 'Education & Youth', 'HLBE': 'Health, Livability & the Built Environment', 'BE': 'Health, Livability & the Built Environment',
            'H': 'Housing', 'NR': 'Natural Resources & Hazard Adaptation'}

actions, cur, code, policy_text, pending_code = [], None, '', {}, None
for p in range(1, count + 1):
    text = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), PDF, '-'], capture_output=True, text=True).stdout.translate(Q)
    for line in text.split('\n'):
        if 'ACTION PLAN |' in line or not line.strip():
            continue
        m = CODE.match(line)
        if m and cur is None:
            code = m.group(1)
            pending_code = code if not policy_text.get(code) else None  # repeated header on a continuation page
            policy_text.setdefault(code, '')
            continue
        if pending_code and cur is None and not TF.match(line):
            policy_text[pending_code] = (policy_text[pending_code] + ' ' + line.strip()).strip()
            continue
        t = TF.match(line)
        if t and cur is None:
            pending_code = None
            cur = dict(page=p, code=code, timeframe=t.group(1).replace('Mid term', 'Mid-term').replace('Long term', 'Long-term'), parts=[])
            line = line[t.end():]
        if cur is None:
            continue
        nm = NUM.search(line)
        body = line[:nm.start()] if nm else line
        body = re.sub(r'^\s*\(\d-\d+ years\)|^\s*\(\d+\+? years\)', '', body).strip()
        if body:
            cur['parts'].append(body)
        if nm:
            cur['number'] = int(nm.group(1))
            full = ' '.join(cur['parts'])
            imp = ''
            if 'Implementers:' in full:
                full, imp = full.split('Implementers:', 1)
            cur['text'], cur['implementers'] = re.sub(r'\s+', ' ', full).strip(), re.sub(r'\s+', ' ', imp).strip()
            actions.append(cur)
            cur = None

LIG = {'\u019f': 'ti', '\u01a9': 'tt'}
reader = pypdf.PdfReader(PDF)
ptext = {}
def repair(s, page):
    """Re-find s in pypdf text, letting each space stand for a ligature glyph, and return the repaired text."""
    if page not in ptext:
        ptext[page] = reader.pages[page - 1].extract_text().replace('\xa0', ' ')
    toks = s.split(' ')
    pat = r'\s*'.join(re.escape(tok) for tok in toks[:1])
    for tok in toks[1:]:
        pat += r'(?:\s+|[\u019f\u01a9]\s*|\s*[\u019f\u01a9])' + re.escape(tok)
    m = re.search(pat, ptext[page].translate(Q))
    if not m:
        return s, False
    out = m.group(0)
    for k, v in LIG.items():
        out = out.replace(k, v)
    return re.sub(r'\s+', ' ', out).strip(), True

fixed = 0
for a in actions:
    a['text'], ok = repair(a['text'], a['page'])
    fixed += ok
for c, s in list(policy_text.items()):
    for a in actions:
        if a['code'] == c:
            policy_text[c] = repair(s, a['page'])[0] if s else s
            break

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['number', 'element', 'code', 'policy', 'timeframe', 'implementers', 'action', 'pdf_page'])
    for a in actions:
        el = ELEMENTS.get(a['code'].split()[0], '')
        w.writerow([a['number'], el, a['code'], policy_text.get(a['code'], ''), a['timeframe'], a['implementers'], a['text'], a['page']])
nums = [a['number'] for a in actions]
print(fixed, 'of', len(actions), 're-matched in pypdf text;', len(actions), 'action entries;', len(set(nums)), 'distinct numbers; max', max(nums), '; missing in 1..max:', len(set(range(1, max(nums) + 1)) - set(nums)))
