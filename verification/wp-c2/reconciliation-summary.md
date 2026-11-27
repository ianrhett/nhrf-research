# WP-C second pass: reconciliation summary (Fable and second Claude review)

**Order:** NHRF-CO-VERIFY002-002, packet `dispatch/WP-002.md`. **Prepared:** 2026-11-27.
**Status:** mechanical comparison for adjudication. Not an approved correction, not a publication edit.
**Files:** `model-comparison.csv` (216 rows, one per baseline ID), `reconciliation-queue.csv` (128 rows, severity ranked), `coverage-summary.md`, `stats.json`, `inputs/` (sha256-pinned snapshots of the two ledgers, the 216 ID list and the PR #10 ChatGPT tags).

## 1. Where the two full ledgers agree

| Field | Agree | Differ |
|---|---|---|
| Disposition | 212 (all 212 are accept by both) | 4 |
| Proposed item type | 215 | 1 |
| Proposed group | 215 | 1 |
| Wrong page, misquote or fabricated record found | neither reviewer found one | |

This confirms the figures the executive verdict (PR #13) states in prose: 212/216 disposition agreement, and no overlap between the two reviewers' non-accept records.

## 2. The four disposition disagreements

| record_id | Source, page | Corpus group / type | Fable | Second Claude | ChatGPT audit (PR #1) | Severity |
|---|---|---|---|---|---|---|
| 102 | Plan_to_Play_2017_Full_Plan p234 | P09 / funding_estimate | reject (cost estimate, not a recommendation) | accept | F01c names this funding estimate | 1-high |
| 1220 | NashvilleNext_Vol4_Actions p49 | P03 / recommendation | reject (duplicate of 1295, action #323) | accept, but flags the same duplicate pair | F01a names the #323 double count | 1-high |
| 998 | MS4_Annual_Report_FY19 p16 | P15 / recommendation | accept | reassign type to commitment | not cited | 2-med |
| 1526 | Concept_2010_General_Plan_1992 p20 | P08 / recommendation | accept | reassign group to P18 | not cited | 2-med |

Records 102 and 1220 are the only ones where a reviewer would take a record out of the 216. On 1220 the two reviewers agree on the fact (action #323 is counted twice in one document) and differ only on the remedy (reject one occurrence versus keep both and flag). On 102 they differ on whether a funding estimate counts. Both are counting-unit questions for adjudication, and both match a ChatGPT finding.

## 3. Duplicates and restatements

The two reviewers use different duplicate rules. Fable keys: `DUP-` same item twice in one document (a double count), `PHASE-` one sentence covering two phases, `TPL-` shared boilerplate for distinct referents, `RST-` the same promise restated across documents. The second Claude keys only "same statement within the same document".

| Pair or cluster | Fable | Second Claude | Reading |
|---|---|---|---|
| 1220, 1295 (NashvilleNext Vol4 action #323, p49 and p79) | DUP | restatement | both: double count |
| 668, 669 (Open Space Plan 2011 p11, two 3,000-acre targets) | PHASE (distinct, keep both) | restatement | both noticed; differ on whether it is a double count |
| 139, 1334 (Climate Adaptation Plan NE1 p204) | not flagged | restatement | second Claude only |
| 751, 1087 (Plan to Play 2026 Update, 82-acre Tier One, p107 and p112) | not flagged | restatement | second Claude only |
| 798, 799 (NEA 1973 p132, escarpment lakes) | not flagged | restatement | second Claude only |
| 66, 67; 1383, 1384 | TPL (distinct) | not flagged | Fable notes shared excerpt text, not a double count |
| 420, 606, 1009, 1252; 604, 1230 | RST (cross-document) | not flagged | intended under the "times" count; not a double count |

Within-document double-count candidates, across both reviewers: 5 pairs (1220/1295, 668/669, 139/1334, 751/1087, 798/799). Only 1220/1295 is called a double count by both. If every candidate pair were collapsed to one record, the count would fall from 216 to 211. That is the outer bound of the restatement caveat in the executive verdict; which pairs to collapse, if any, is an adjudication call.

## 4. Ledger evidence gap (second Claude review)

In 84 records the second Claude ledger's quote field does not show the corpus excerpt, and in 35 more it shows it only in part (see `coverage-summary.md`). Fable's ledger shows the excerpt for all 216. No record lacks quoted excerpt evidence in both ledgers. These 84 rows are in the queue at 2-med with `ledger_quote` in `disputed_fields`.

## 5. Shared failure modes (agreement is not proof)

- **Same model family.** Both full ledgers are Claude. The order asked for one Sol (GPT) and one Fable review; Sol produced 0/216. The only GPT-family view is the ChatGPT findings-level audit (PR #1), which is not a per-record ledger.
- **Same verification method.** Both locate the corpus excerpt in extracted page text (pdftotext, or OCR for the three scanned plans). This tests transcription and page placement. It does not test meaning, and a correct page match says nothing about whether the record should count.
- **Same record set and boundary.** Both reviewed the 216 selected IDs under the corpus's own counting rule. Neither re-ran the 340 forest-record population for omissions, and neither re-litigated the enacted-code exclusion behind 216 versus 217.
- **Same OCR exposure.** Concept_2010_General_Plan_1992 (11 records) has no OCR text in the corpus; each reviewer ran its own OCR.
- **Group calls largely untested.** Fable kept every corpus group by design and records that as a limitation; the second Claude proposed one group change. Group agreement of 215/216 mostly reflects both reviewers accepting the corpus coding.

## 6. What this establishes, and what it does not

Established: both full reviews account for all 216 baseline IDs with no missing or extra rows; they agree on 212 dispositions; every excerpt is shown verbatim on its cited page in at least one ledger; the four disagreements and five within-document double-count candidates are identified by record ID.

Not established: which counting unit to publish (102, the five restatement pairs, the 216 versus 217 enacted-code row); the second Claude review's underlying page match for the 84 records whose ledger quote misses the excerpt; any implementation finding for P01 to P19 (both ledgers' `implementation.csv` files are reviewer summaries, not adjudicated, and implementation status is now under `dispatch/WP-003.md`).
