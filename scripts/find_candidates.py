"""Find candidate sentences for the Commitments tab in one or more PDFs.

Usage: python3 find_candidates.py <commitments_dir> <out.csv> <doc_id>=<pdf or OCR dir> [...]

Splits each PDF page into sentences and keeps those that touch a Forest-related topic and carry
a promise word, a number, or a stated fact about land. Each candidate gets the triggers that fired
and whether the workbook already holds a row for that doc whose excerpt overlaps it. Sentences that
repeat word for word across the documents in one run (shared boilerplate) are kept once and marked.
This narrows reading; it does not decide anything. A person reviews the output, and every row
written later is still checked word for word against its page.
"""
import csv, os, re, subprocess, sys
from collections import defaultdict

CDIR, OUT, *DOCS = sys.argv[1:]

TOPIC = re.compile(r'forest|wood(ed|land)|tree|canopy|slope|hillside|ridge|escarpment|highland rim|headwater|'
                   r'conservation|conserv|preserv|open space|natural area|green network|greenway|park ?land|'
                   r'sensitive (environmental )?feature|floodplain|floodway|stream|creek|wetland|habitat|wildlife|'
                   r'rural|farmland|agricultur|sewer|easement|acquisi|undisturbed|clearing|grading|steep|soil', re.I)
PROMISE = re.compile(r'\b(should|shall|will|must|encourage[sd]?|recommend\w*|require[sd]?|intend\w*|goal|target|'
                     r'polic(y|ies)|strateg\w*|priorit\w*|protect\w*|preserv\w*|maintain\w*|limit\w*|avoid\w*|'
                     r'discourag\w*|minimiz\w*|apply|applied|commit\w*|action)\b', re.I)
NUMBER = re.compile(r'\b\d[\d,.]*\s*(%|percent|acres?|square miles?|miles?|feet|units?)\b|\b\d{4}\b', re.I)
FACT = re.compile(r'\b(contains?|covers?|comprises?|located|includes?|is|are|has|have)\b', re.I)
# Forest-core topics keep a sentence on their own; the broader TOPIC list needs a promise or a number too.
STRONG = re.compile(r'forest|wood(ed|land)|\btrees?\b|canopy|slope|ridge|escarpment|highland rim|headwater|habitat|wildlife|'
                    r'undisturbed|clearing|sensitive (environmental )?feature', re.I)
NOISE = re.compile(r'^(Figure|Table|Contents)\b|www\.|https?://|ADOPTED [A-Z]+ \d+, \d{4} III|(\b\w{1,2}\b\s+){8,}')

n = lambda s: re.sub(r'\s+', ' ', s.replace('\xa0', ' ')).strip()
Q = str.maketrans({'‘': "'", '’': "'", '“': '"', '”': '"', '–': '-', '—': '-'})

def pages(pdf):
    # A directory instead of a PDF holds Tesseract OCR of a scan, one p<N>.txt per page.
    if os.path.isdir(pdf):
        nums = sorted(int(m.group(1)) for f in os.listdir(pdf) if (m := re.fullmatch(r'p(\d+)\.txt', f)))
        for p in nums:
            t = re.sub(r'(\w)-\n(\w)', r'\1\2', open(f'{pdf}/p{p}.txt', encoding='utf-8').read())
            yield p, n(t.translate(Q))
        return
    count = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    for p in range(1, count + 1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout
        t = re.sub(r'(\w)-\n(\w)', r'\1\2', t)  # line-break hyphenation
        yield p, n(t.translate(Q))

def sentences(text):
    for s in re.split(r'(?<=[.;!?])\s+(?=[A-Z•])|\s•\s', text):
        s = s.strip(' •')
        if 40 <= len(s) <= 700:
            yield s

existing = defaultdict(list)
with open(f'{CDIR}/commitments.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        existing[r['doc']].append(n(r['excerpt'].translate(Q)).lower())

def already(doc, s):
    low = s.lower()
    for ex in existing.get(doc, []):
        if len(ex) >= 25 and (ex in low or low in ex):
            return 'yes'
        a, b = set(re.findall(r'[a-z]{4,}', ex)), set(re.findall(r'[a-z]{4,}', low))
        if a and b and len(a & b) / min(len(a), len(b)) >= 0.8:
            return 'likely'
    return ''

rows, seen = [], defaultdict(list)
for spec in DOCS:
    doc, pdf = spec.split('=', 1)
    for p, text in pages(pdf):
        for s in sentences(text):
            if not TOPIC.search(s) or NOISE.search(s):
                continue
            trig = [name for name, rx in (('promise', PROMISE), ('number', NUMBER), ('fact', FACT)) if rx.search(s)]
            if STRONG.search(s):
                trig.append('forest')
            if not ({'promise', 'number', 'forest'} & set(trig)):
                continue
            key = s.lower()
            seen[key].append(doc)
            rows.append(dict(doc=doc, page=p, triggers='+'.join(trig), topics=','.join(sorted({m.group(0).lower() for m in TOPIC.finditer(s)}))[:120],
                             already=already(doc, s), sentence=s, key=key))

out, kept = [], set()
for r in rows:
    docs = seen[r['key']]
    if len(set(docs)) > 1:
        if r['key'] in kept:
            continue
        kept.add(r['key'])
        r['repeated_in'] = len(set(docs))
    else:
        r['repeated_in'] = 1
    out.append(r)

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['doc', 'page', 'triggers', 'topics', 'already', 'repeated_in', 'sentence'], extrasaction='ignore')
    w.writeheader()
    w.writerows(out)
by_doc = defaultdict(int)
for r in out:
    by_doc[r['doc']] += 1
print(f'{len(out)} candidates', dict(by_doc), 'already in workbook:', sum(1 for r in out if r['already']), 'shared boilerplate kept once:', len(kept))
