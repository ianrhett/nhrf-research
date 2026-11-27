# Coverage — WP-B second independent Claude (Opus) 216-record evidence review

Frozen corpus: `ianrhett/nhrf-research` @ `4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`
Audited IDs: `verification/selected-216-ids.csv` (authoritative record_id = `promise_id`).
This was a BLIND, independent review. No other reviewer's output and no prior audit of this corpus was read.

## Totals (sum to 216)

| Bucket | Count |
|---|---|
| Checked against the original (hash-verified source, cited page read) | **216** |
| Blocked (could not open/verify original) | **0** |
| Unresolved | **0** |
| **Total** | **216** |

Every one of the 216 records has `original_checked = yes`.

## Disposition tally

| Disposition | Count |
|---|---|
| accept | 214 |
| reassign | 2 |
| reject | 0 |
| unresolved | 0 |

Confidence: high = 205, med = 10, low = 1.

## Source integrity (all hash-verified before use)

26 source files (24 PDFs + 2 OCR sidecars) back the 216 records across 13 consolidated documents.
All 26 were downloaded from the Bunny CDN and their `sha256` matched `sources/BUNNY-URLS.csv` / `sources/MANIFEST.csv`: **26 MATCH, 0 MISMATCH, 0 missing.**

Page-extraction method per source:
- 23 born-digital PDFs: `pdftotext -layout`, physical page N = cited `pdf_page` (calibration below).
- `NEA_1973_Natural_Environmental_Analysis` and `General_Plan_1980_2000`: scanned; verified against the project's **hash-verified OCR sidecar** text (`===== PAGE N =====` markers).
- `Concept_2010_General_Plan_1992`: image-only PDF with **no OCR sidecar provided**. The PDF itself is hash-verified (MATCH); the 11 cited pages were OCR'd by this reviewer with `tesseract` to read the passages. (Caveat: these 11 records were verified from reviewer-produced OCR of the hash-verified original, not from a corpus-provided OCR text.)

## Page-offset calibration

For every record the excerpt's distinctive keywords were scored against the cited page and all pages of the document. For strong matches (score ≥ 0.5), the best-matching page equalled the cited page (delta 0) in **206 cases**; the handful of non-zero deltas are generic-vocabulary collisions (e.g. repeated "preserve undisturbed canopy / 65%" tables, or identical boilerplate reused on adjacent pages / cross-referenced actions) — in each the cited page still contains the quoted text. **No record was found on a wrong page; offset = 0 across all 13 documents.** Minimum per-record cited-page match score was ≥ 0.4; every excerpt was located on its cited page.

## Records audited per group (P01–P19), summing to 216

P01 29 · P02 15 · P03 15 · P04 12 · P05 15 · P06 9 · P07 22 · P08 16 · P09 19 · P10 1 · P11 9 · P12 1 · P13 9 · P14 9 · P15 8 · P16 5 · P17 8 · P18 7 · P19 7  = **216**
