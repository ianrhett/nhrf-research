# Methodology — blind independent verification

## Independence
Single reviewer (Claude Opus), working alone. Inputs were restricted to: the `data/` CSVs, `sources/MANIFEST.csv` + `sources/BUNNY-URLS.csv`, `scripts/count_funnel.py`, `verification/selected-216-ids.csv`, and the original source documents on the Bunny CDN. No pull requests, no files under `verification/ reviews/ fable/ sol/ one-pager/`, and nothing named `*audit* / *evidence-ledger* / *reconciliation* / *one-pager* / *fact-check* / *216_Times*` were opened. No other reviewer's conclusions were seen at any point.

## Record set
The 216 authoritative `promise_id` records were taken from `selected-216-ids.csv` and joined back to `data/commitments.csv` by (doc, pdf_page, promise_id, metric), disambiguated by item_type where needed. All 216 joined 1:1 (0 unmatched). Each record carries its full corpus fields (category, item_type, value, excerpt, notes, verify, source_url, promise_id).

## Source acquisition and integrity
Each of the 26 files behind the 216 records was downloaded by `curl` and its `sha256sum` compared to `BUNNY-URLS.csv`/`MANIFEST.csv` before any use. Result recorded per file (26/26 MATCH). A file whose hash failed or whose URL 404'd would have been marked `original_checked = no` with the blocker; none occurred.

## Reading the original
Born-digital PDFs were split to per-physical-page text with `pdftotext -layout`. The two scanned plans (NEA 1973, General Plan 1980) were read from the project's hash-verified OCR sidecars, which carry explicit `===== PAGE N =====` markers. The image-only `Concept_2010` PDF (no sidecar) was OCR'd page-by-page by the reviewer with `tesseract` on the hash-verified file.

For every record the cited page's text (and ±3 neighbours, and a whole-document keyword scan) was examined; the quoted sentence was located in context, and the item was judged against the actual surrounding passage, not the CSV excerpt alone. `original_text_quote` in the ledger is text taken from the source page as read.

## Counting boundary (judged as the dataset does, per `scripts/count_funnel.py`)
Counted item types are `recommendation, commitment, target, funding_estimate` ("recommendation-type"). Enacted law/resolutions (`Metro_Code_*`, `Ordinance_*`, `Executive_Order_*`, `Resolution_*`) are implementation evidence, not recommendations, and are excluded. A row is in scope if its category is forest-related (`forest_protection, tree_canopy, highland_rim_named_place, habitat_natural_area, land_acquisition, open_space`) OR it is tagged P01–P19. `context`-tagged rows are excluded. I confirmed the one 216-vs-217 boundary row — `Metro_Code_17.28.030` field `17.28.030.A.2` (P01, "slopes over 25% recorded as open space") — is correctly excluded as enacted code; it appears in `promise_groups.csv` but not in the 216. I did not re-litigate the boundary.

## Disposition rule
- **accept** — excerpt is faithfully present at the cited page of the hash-verified original, and the item_type and P-group are defensible for the passage.
- **reassign** — excerpt is faithful, but the item_type or the P-group should change; the proposed value is given in `proposed_type` / `proposed_group`.
- **reject** — not supported: wrong page/source, material misquote, or the passage is background/context or already-enacted law rather than a recommendation-type statement. (None found.)
- **unresolved** — could not be verified (none).
Confidence (high/med/low) reflects OCR clarity, vocabulary ambiguity, and how clear-cut the type/group call is.

## Duplicate / restatement rule
`duplicate_key` groups records that quote the **same statement within the same document** (a true restatement/double-count). Cross-document repetition of the same recommendation (e.g. the canopy policy recurring across eight plans) is **intentional** under this corpus's "times/docs" counting and is **not** flagged as a duplicate. Two records that share boilerplate wording but describe genuinely different subjects (e.g. two different redevelopment sites) are **not** treated as duplicates.
