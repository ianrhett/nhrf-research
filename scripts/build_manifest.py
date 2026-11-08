"""Build docs/research/sources/MANIFEST.csv: one row per source on the Sources tab.

Usage: python3 build_manifest.py <commitments_dir> <local_pdf_dir> <sources_dir>
local_pdf_dir holds <doc_id>.pdf as downloaded from each source_url (retrieved 2026-10-22).
For each source: title, date, status, URL, kind (pdf or web), SHA-256 and size of the retrieved
PDF, page count, Commitments row count, cover image path (page 1 for PDFs, a browser screenshot for
web pages), and a note. Web pages have no fixed file; their notes say how they were captured.
"""
import csv, hashlib, os, re, subprocess, sys

CDIR, PDFS, SDIR = sys.argv[1:4]
rows = [r for r in csv.reader(open(f'{CDIR}/sources.csv', encoding='utf-8'))][1:]
rows = [r for r in rows if r and r[0] not in ('Total',) and len(r) > 5 and r[5].startswith('http')]
counts = {}
for r in csv.DictReader(open(f'{CDIR}/commitments.csv', encoding='utf-8')):
    counts[r['doc']] = counts.get(r['doc'], 0) + 1

WEB_NOTE = {
    'Metro_Code': 'Municode, read in a browser 2026-10-22; excerpts quoted on Commitments. Municode shows a bot check to automated capture, so no screenshot or archive copy; use Municode print/PDF in a normal browser for a full copy. Code text changes as Council amends it.',
    'Ordinance_': 'Metro Council legislative archive page; screenshot 2026-10-22.',
    'Resolution_': 'Legistar Web API record (JSON); screenshot 2026-10-22.',
    'Mayor_Release': 'nashville.gov news release; screenshot 2026-10-22.',
    'Ecological_Conservation_Strategy': 'engage.nashville.gov project page; screenshot 2026-10-22. Page changes as the project proceeds.',
}
SCANS = {'NEA_1973_Natural_Environmental_Analysis', 'General_Plan_1980_2000'}

out = []
for r in rows:
    doc, title, date, status, pages, url = r[:6]
    pdf = f'{PDFS}/{doc}.pdf'
    cover = f'covers/{doc}.jpg' if os.path.exists(f'{SDIR}/covers/{doc}.jpg') else ''
    if os.path.exists(pdf):
        data = open(pdf, 'rb').read()
        sha, size = hashlib.sha256(data).hexdigest(), len(data)
        info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
        m = re.search(r'Pages:\s+(\d+)', info)
        npages = m.group(1) if m else pages
        kind = 'pdf'
        note = 'Archival scan without a text layer; rows verified against OCR.' if doc in SCANS else ''
    else:
        sha, size, npages, kind = '', '', '', 'web'
        note = next((v for k, v in WEB_NOTE.items() if doc.startswith(k)), 'Web page.')
    out.append([doc, title, date, status, url, kind, sha, size, npages, counts.get(doc, 0), cover, '2026-10-22', note])

with open(f'{SDIR}/MANIFEST.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['doc', 'title', 'date', 'status', 'source_url', 'kind', 'sha256', 'bytes', 'pages', 'commitments_rows', 'cover', 'retrieved', 'notes'])
    w.writerows(out)
print(len(out), 'sources;', sum(1 for o in out if o[5] == 'pdf'), 'pdf;', sum(1 for o in out if o[10]), 'with cover;',
      sum(1 for o in out if o[9] == 0), 'with no Commitments rows')
