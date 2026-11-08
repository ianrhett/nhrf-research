# Nashville Highland Rim Forest: the commitments research

Published by the Alliance to Conserve Nashville's Highland Rim Forest so that anyone can check or repeat the work.

Since 1973, Metro Nashville has made the same 19 forest recommendations 216 times, in 13 documents. Of the 19, one is classified implemented, 15 partly implemented, and 3 with no implementation reported in this review.

## What is here

| Folder | Contents |
|---|---|
| `one-pager/` | `NHRF_Recommended_216_Times_v1.7.1.pdf`, the one-page summary of record (November 2026), with the script and template that build it |
| `data/` | `NHRF_Commitments.xlsx`, the full workbook; one CSV per tab (`commitments.csv` is every quoted statement with page number; `recommendations.csv` is the 19 with status and evidence; `sources.csv` is every document with its URL and whether it is counted); dated releases in `versions/` |
| `sources/` | `MANIFEST.csv`: every source document with its official URL, SHA-256 fingerprint, page count and retrieval date. `BUNNY-URLS.csv`: archived copies of each file. Copies of sources that are small enough to keep in git. |
| `methodology/` | `methodology.html`, the method in plain language: how 1,272 statements became 19 recommendations made 216 times, and how delivery was checked |
| `scripts/` | Every script used to extract, group, count and check. `count_funnel.py` produces every published number; its output is `funnel.json`. |

## How to verify a number

1. Open `data/sources.csv` and pick a document. Its `source_url` is the official Metro copy; `sources/MANIFEST.csv` has the fingerprint of the file we read.
2. Open `data/commitments.csv`, filter by that document, and read each quoted statement against the stated page.
3. Open `data/recommendations.csv` to see which statements were grouped into which of the 19, and the evidence for each status.
4. Run `python3 scripts/count_funnel.py` against `data/NHRF_Commitments.xlsx` to reproduce `scripts/funnel.json`.

## Rules we followed

- Only adopted plans and official final Metro documents are counted. Drafts, advisory reports and unenacted bills were read but excluded, and are listed as such.
- A document is counted once however many files it spans (NashvilleNext is one document, 17 files).
- Metro documents make recommendations. We do not call them promises.
- Every statement carries its page number and a verification flag (`verified`, `verified_ocr`, `verified_by_hand`).

Corrections: open an issue on this repository with the document, page and quoted text.
