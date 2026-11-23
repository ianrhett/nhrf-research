# Fable (WP-B) independent methodology

Independent primary-source audit of the 216 selected forest/conservation records
in `verification/selected-216-ids.csv`, frozen at SHA `4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`.
Conducted alone, without reading any other reviewer's output, the research
reconciliation files, or research PR #1.

## 1. Record identity

`record_id` is the `row_ordinal` value from `verification/selected-216-ids.csv`
(the selection's own ordinal). Each selected record maps one-to-one to a line in
`data/commitments.csv` via the `csv_line` field; that mapping was verified for all
216 records (doc, pdf_page, item_type and metric all matched the referenced line).
The full record fields (excerpt, value, unit, target_year, category, source_url,
promise_id) were pulled from the referenced `commitments.csv` line.

## 2. Obtaining the original documents (sha256-validated)

None of the 25 cited source documents are the in-repo `sources/*.pdf` files (those
are budget/CIB documents and the 2013 UFPP, none of which appear in the 216). The
nashville.gov `source_url` values frequently 403 or are hundreds of pages. Every
cited document is mirrored on the public Bunny CDN listed in `sources/BUNNY-URLS.csv`.

Procedure:
- Downloaded all 25 cited PDFs from `https://practicestudio-taste.b-cdn.net/civic/nashville/sources/`.
- Computed sha256 of each download and confirmed it matched the value in
  `sources/MANIFEST.csv`. All 25 matched exactly.
- For the two scanned documents that have no text layer and that also publish a
  sha256-validated OCR text file on Bunny (General_Plan_1980_2000, NEA_1973), the
  Bunny OCR `.txt` was downloaded and its sha256 confirmed against `BUNNY-URLS.csv`.
  Both matched. These files are page-delimited (form feed for GP1980; `===== PAGE n =====`
  markers for NEA1973) and the markers align with the corpus `pdf_page` numbers.
- The third scanned document (Concept_2010_General_Plan_1992) has no Bunny OCR file,
  so each cited page was rendered from the sha256-validated PDF (`pdftoppm` at 300 dpi)
  and OCR'd locally with `tesseract`.

`original_checked=yes` is set only where the source's sha256 matched AND the cited
page was read.

## 3. Page reading and excerpt matching

- Text-layer PDFs (22 docs, 147 records): `pdftotext`, split on form feed; page N is
  chunk N-1 (1-indexed physical page), confirmed against MANIFEST page counts.
- GP1980 / NEA1973 (58 records): sha256-validated Bunny OCR text, page-indexed as above.
- Concept_2010 (11 records): self-OCR of the sha256-validated PDF, per cited page.

Matching of the corpus `excerpt` against the cited page used two signals, both
whitespace- and case-insensitive:
1. Exact despaced 40-character slice probes taken from the excerpt (robust to spacing
   and line-break differences in extraction).
2. Token-overlap ratio: fraction of the excerpt's words (length >= 4) present on the page.

A record was treated as located on its cited page when at least one slice probe hit,
or token overlap was >= 0.60. Each record was also checked against a +/-2 page window
to detect off-by-one citation errors.

## 4. Type, group and disposition judgment

- `proposed_type` defaults to the corpus `item_type`. It was overridden only with
  page-read evidence (two cases). Automated re-typing by keyword was rejected after
  testing showed it churned legitimate `target` records into `recommendation` and
  produced false `background` flags; corpus type labels were respected unless a page
  read showed a clear error.
- `proposed_group` was kept equal to the corpus `promise_id`. The 19 promise groups
  (P01-P19, `data/promise_counts.csv`) overlap heavily (slopes vs escarpment, acquire-land
  vs connected-system vs acreage-goals). A keyword-overlap outlier scan produced 13
  weak candidates, but none rose to a clear, defensible misassignment on review, so no
  group was reassigned. This is recorded as a limitation, not a clean bill.
- `disposition`:
  - `accept`: excerpt located on the cited page and the record functions as an in-scope
    forest/conservation recommendation, commitment or recommended target.
  - `reassign`: belongs in the corpus but the type label or framing should change.
  - `reject`: not a forest/conservation recommendation as written (funding estimate,
    or a redundant duplicate of another record).
  - `unresolved`: could not be verified (none remained).

## 5. Duplicate / restatement rule

Candidate clusters were formed by excerpt-token Jaccard, then resolved by reading the
pages, because token overlap alone conflated distinct per-subarea canopy targets and
phased acreage targets with true duplicates. `duplicate_key` is assigned only after a
page read confirmed the relationship:
- `RST-*`: the same promise restated across different documents (expected; the corpus
  counts restatements in its `times` field). Both records accepted.
- `PHASE-*`: one source sentence covering two distinct phases (e.g., 3,000 acres by
  ~2026 and an additional 3,000 by 2035). Distinct, both accepted.
- `TPL-*`: identical boilerplate or shared table-row excerpt applied to distinct
  referents (two redevelopment sites; two metrics from one LOS table row). Distinct,
  both accepted, flagged as an excerpt-selection quality issue.
- `DUP-*`: the same item counted twice within one document (NashvilleNext Vol4 action
  #323 cross-listed under BE 1.1 and NR 4.2). One occurrence rejected.

Per-subarea canopy targets and the UFLMP transect targets were deliberately NOT marked
as duplicates despite high token overlap, because each carries a distinct baseline.

## 6. Confidence

- `high`: strong verbatim slice match on a text-layer source and a clear in-scope record.
- `med`: located only by token overlap; or read via OCR (Concept self-OCR); or the
  selected excerpt is descriptive context rather than the operative action sentence; or
  a reassign/reject/duplicate judgment call; or a numeric target/estimate sub-type that
  would be flagged under a strict recommendation-only boundary.
- `low`: none (no record was left unverifiable).

## 7. Constraints honored

No files under `data/` or publication files were edited. No page, quote or status was
invented; every assertion traces to a sha256-validated source and a specific page. No
final publication wording was proposed.
