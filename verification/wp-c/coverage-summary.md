# WP-C coverage summary (NHRF-CO-VERIFY002-002)

**Prepared:** 2026-11-24 by Code XO (interactive, Opus 4.8).
**Frozen corpus:** `ianrhett/nhrf-research@4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`. **Selected records:** 216.

## 1. Source-access reachability (settled, VERIFIED 2026-11-23)

The reviewers disagreed on whether the Bunny archive is reachable. The XO settled it by downloading files from a Code runner and hashing them against the frozen `sources/MANIFEST.csv`:

| file | bunny path | sha256 | bytes | result |
|---|---|---|---|---|
| Parks_Board_Agenda_2026-09-01.pdf | `/civic/nashville/sources/` | `6f480e63...21281` | 122,727 | exact match |
| NEA_1973 OCR text | `/civic/nashville/sources/ocr/` | `1f84a988...248a38` | 204,898 | exact match |

**Conclusion:** the archive is reachable and checksum-grade verifiable from a fetch-capable runner. The Bunny base is `https://practicestudio-taste.b-cdn.net/civic/nashville/sources/`. Sol's inability to verify is a limitation of Sol's own sandbox (`ConnectionError` to Bunny and raw GitHub), not a corpus or archive defect. Fable's full-access run is therefore reproducible by construction.

## 2. Per-reviewer coverage

| reviewer | family | artifact | records checked at source | blocked | dispositions produced |
|---|---|---|---|---|---|
| Fable | Claude | PR #9 ledger | **216 / 216** (sha256-validated originals; pdftotext or self-OCR) | 0 | accept 214, reject 2 |
| ChatGPT | GPT | PR #1 one-pager | representative records + full CSV arithmetic reconciliation; **not** all 216 individually authenticated | n/a | 10 findings (F01-F10) + 19 implementation assessments, findings-level |
| Sol | GPT | PR #8 ledger | **0 / 216** (environment could not reach Bunny) | 216 | 0 (all `unresolved`) |

Sol cohorts (for a future fetch-capable resume): blocked-recheck 20, legacy-revalidate 22, unprocessed 174. These are carried in `model-comparison.csv` as `sol_cohort` so a resumed Sol run has its worklist.

## 3. Fable disposition detail (the only record-level ledger)

- Checked at source: 216 / 216. Blockers: 0.
- Disposition: accept 214, reject 2 (id 102 funding estimate; id 1220 duplicated action #323).
- Confidence: high 158, med 58. The 58 med flags are predominantly the "target sub-type, flag for type review under a strict recommendation-only boundary" note (the counting-unit concern).
- Reassignments (proposed_type or proposed_group differs from corpus): 0. Fable proposed no regrouping.
- Duplicate keys: 6 distinct keys over 14 records (`TPL-P2Ptable27` 66/67; `RST-NRpol1.4` 420/606/1009/1252; `RST-NRgoal1` 604/1230; `PHASE-privcons3k` 668/669; `DUP-act323` 1220/1295; `TPL-protOS` 1383/1384).

## 4. Reconciliation queue (140 of 216 records)

Records needing adjudication, by priority tier (full detail in `reconciliation-queue.csv`):

| tier | meaning | count |
|---|---|---:|
| 1-converge-record | Fable substantive flag coincides with a ChatGPT record-level citation (or a Fable reject) | 10 |
| 2-cg-record-only | ChatGPT cites the record; Fable accepted clean-high | 6 |
| 3-converge-group | Fable flagged the record and its group is named in a ChatGPT wording finding | 25 |
| 3-fable-dup | Fable duplicate-key flag, no ChatGPT record-level citation | 6 |
| 4-cg-group-only | record's group is named in a ChatGPT wording finding; Fable accepted clean-high | 73 |
| 5-fable-medconf | Fable medium-confidence (type/unit) flag only | 20 |

The remaining 76 of 216 records are clean: Fable accept at high confidence, no ChatGPT record-level or group-wording flag (ChatGPT's universal F07 document-count and per-group implementation notes still apply at the presentation layer, tagged `chatgpt_universal` in `model-comparison.csv`).

## 5. Count integrity

- All 216 record identifiers are common to the Fable ledger and `selected-216-ids.csv` (set-equal; no record-level drift).
- All nine ChatGPT record-level citations resolve to existing records via (document, page) join; no dangling citation.
- The 216-versus-217 arithmetic item (one enacted-code row, `Metro_Code_17.28.030.A.2`) is unchanged and remains for adjudication; see WP-A (`verification/reconciliation.md`) and `reconciliation-summary.md` section 6.

Nothing in this checkpoint modifies the corpus, the counts, or any publication. No PR was merged.
