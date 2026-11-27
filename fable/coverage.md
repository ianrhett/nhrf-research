# Fable (WP-B) coverage

Scope: all 216 records in `verification/selected-216-ids.csv` at frozen SHA
`4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`.

## Headline numbers (of 216)

| Measure | Count |
|---|---|
| Checked against the ORIGINAL document (sha256 validated AND cited page read) | 216 |
| Blocked (could not open / sha256 mismatch) | 0 |
| Unresolved (excerpt not located on cited page) | 0 |

All 216 cited excerpts were located on their cited pages of the sha256-validated
originals. No off-by-one page citation errors were found (0 of 216). This is a
positive finding: the corpus page citations are accurate.

## How each source was validated and read

| Source read method | Records | sha256 validated |
|---|---|---|
| `pdftotext` of sha256-validated PDF (22 text-layer docs) | 147 | yes |
| sha256-validated Bunny OCR text (General_Plan_1980_2000, NEA_1973) | 58 | yes (OCR .txt) |
| self-OCR of sha256-validated PDF (Concept_2010_General_Plan_1992) | 11 | yes (PDF) |

All 25 cited source documents were downloaded from the Bunny CDN mirror and every
sha256 matched `sources/MANIFEST.csv` / `sources/BUNNY-URLS.csv` exactly.

## Match strength

| Match type | Records |
|---|---|
| Verbatim (exact despaced slice found on cited page) | 208 |
| ~100% token overlap (every excerpt word on the page; slice broken by OCR/table layout) | 8 |

## Disposition

| Disposition | Count |
|---|---|
| accept | 214 |
| reassign | 0 |
| reject | 2 |
| unresolved | 0 |

## Confidence

| Confidence | Count |
|---|---|
| high | 158 |
| med | 58 |
| low | 0 |

The 58 med-confidence records are: the 11 Concept_2010 self-OCR records, the 8
token-overlap-only matches, records whose selected excerpt is descriptive context
rather than the operative action sentence (concentrated in the 1973 NEA), the
restatement/duplicate/template clusters, and the 35 `target` plus 1 `funding_estimate`
sub-type records that a strict recommendation-only boundary would flag for type review.

## Blockers

None. Every cited document was obtained and sha256-validated, and every cited page
was read. No record was counted as verified without reading its cited page.
