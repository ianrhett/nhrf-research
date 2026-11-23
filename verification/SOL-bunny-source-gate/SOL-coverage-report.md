# SOL independent audit — source-access checkpoint (NOT a completed audit)

**Auditor indicator:** SOL. **Date:** 2026-11-23.
**Frozen data:** `ianrhett/nhrf-research@4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`. **Selected record IDs:** `wp-002-nhrf-verify-002-evidence-audit:verification/selected-216-ids.csv`.

## Result and evidentiary gate

**This is an access-blocked source-integrity checkpoint, not record-by-record verification and not evidence that the 216 recommendations are valid.** The user requires a downloaded Bunny archive file whose SHA-256 matches `sources/BUNNY-URLS.csv`, plus inspection of the cited original PDF page, before `original_checked=yes`.

- Selected records: **216**, exact selection order retained.
- Source-document identifiers represented: **26**, across **13 consolidated documents** as defined in the frozen project's counting methodology.
- **26/26** source-document identifiers have `BUNNY-URLS.csv.sha256 == MANIFEST.csv.sha256`. This is only a comparison of **two recorded hash strings**, NOT independent verification of downloaded bytes.
- Downloaded, SHA-256-matched and original-page-inspected records under corrected rule: **0/216**.
- Pending under corrected rule: **216/216**; all set to `original_checked=no; disposition=unresolved; confidence=low`.
- Previously blocked, Bunny recheck attempted at domain level: **20** (32, 45, 66, 67, 68, 70, 83, 85, 86, 91, 92, 93, 97, 102, 112, 123, 127, 139, 142, 147).
- Previously page-reviewed against non-hash-validated Metro sources, now requiring archive integrity revalidation: **22** (420, 440, 443, 444, 452, 453, 457, 458, 459, 460, 464, 466, 467, 472, 476, 480, 483, 485, 492, 507, 508, 516).
- Not-yet-audited selected records: **174**, beginning at **record_id=571**.
- Records with a confirmed downloaded archive SHA-256 mismatch: **0** — because **no archive was downloaded**. Do not interpret this as successful verification.
- No independent implementation statuses were established in this corrected pass; the 19-row implementation file is a deliberately unverified queue.

## Exact environment blocker

1. `web.open` on the Bunny CDN PDF endpoint returned **"URL ... not accessible via this tool"**; a Bunny directory URL returned **`DisabledError`**.
2. Direct `requests.get` from the execution container to both the Bunny host and raw GitHub failed with **`ConnectionError`**. This is a runtime network-access restriction, not evidence that the Bunny object returns 403 or is absent.
3. `container.download` rejected the Bunny PDF URL as **"url not viewed in conversation before"** despite attempts to open it. It did not yield document bytes.
4. The GitHub connector successfully fetched CSV **metadata** (frozen `BUNNY-URLS.csv`, `MANIFEST.csv`, `commitments.csv`, `sources.csv`, `recommendations.csv`, and branch-selected IDs), but it does not retrieve the external Bunny PDF bytes.
5. The same source accessibility limitation prevents checks of the two requested OCR text archives. Their **expected** SHA-256 values are recorded in `SOL-source-gate.csv` but **not** validated.

**No source PDF page was checked under the corrected rules**, so the earlier 22 affirmative checks cannot carry forward as verified. Their prior provisional decisions have not been erased from the previous partial checkpoint, but none were promoted.

## Ledger rules

`SOL-evidence-ledger.csv` follows all **16 requested columns** and includes exactly **216** selected IDs with original type/group and original source URL from frozen files. The original type/group are **dataset claims only**. `original_text_quote`, proposed type/group, duplicate key and evidence locator are blank because no archive was inspected. The `blocker` and `justification` fields distinguish previous blocked records, legacy non-hash-validated reviews, and new unprocessed records.

No record is accepted, rejected, regrouped, or assigned a duplicate key without page evidence. The alternative enacted-code 217th entry remains out of scope. The classification rule remains: distinguish recommendation, commitment, quantitative target, estimate, background and enacted law, and only assign semantic duplicate keys after reading surrounding source context.

## Required resumption

On a runner with permitted access to `https://practicestudio-taste.b-cdn.net/civic/nashville/sources/`, download each source at the exact `SOL-source-gate.csv.bunny_url`; compute SHA-256 of **downloaded bytes** and require equality to `expected_sha256`. Also download/verify both OCR archives. For each selected record, inspect the original PDF page and adjacent context (OCR supplementary only for scans); then classify and cite precise page evidence. Start by rechecking the previous **20 blocked** records, then revalidating the **22 legacy** rows under the stricter rule, then proceed from **571** through selection end. Update the ledger only after each original-page inspection.

Implementation status must be verified separately from contemporary primary instruments; descriptions in the frozen recommendation or promise-count tables are not implementation proof. No repo merge or production change was made.

## Files in this SOL checkpoint

- `SOL-evidence-ledger.csv` — 216-row 16-column evidence-gated ledger, **all unresolved**.
- `SOL-source-gate.csv` — 26-document hash **metadata** cross-check and archival location/expected OCR hashes.
- `SOL-implementation.csv` — 19 groups, **implementation unverified**.
- `SOL-coverage-report.md` — this audit checkpoint and blocker.
