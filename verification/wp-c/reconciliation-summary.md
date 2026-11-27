# WP-C reconciliation summary (NHRF-CO-VERIFY002-002)

**Prepared:** 2026-11-24 by Code XO (interactive, Opus 4.8).
**Frozen corpus:** `ianrhett/nhrf-research@4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`.
**Selected records:** 216 (`verification/selected-216-ids.csv`, branch `wp-002-nhrf-verify-002-evidence-audit`).
**Status:** evidence-first reconciliation for adjudication. Not an approved correction, not a publication, nothing merged.

## 1. What WP-C is, and why it is not a clean three-way CSV join

The order sequenced WP-C as a mechanical three-way comparison of two independent original-source reviews (Sol, Fable) against the frozen ChatGPT audit. On inspection the three legs are not the same kind of artifact, so a row-for-row CSV join of three disposition ledgers is not possible. The three legs are:

- **Fable (Claude family), PR #9, branch `wp-002b-fable-review`.** A full 216-row, 16-column disposition ledger. Every record `original_checked=yes` against a sha256-validated original (pdftotext or self-OCR of the hash-matched PDF). Dispositions: **accept 214, reject 2.** Confidence: high 158, med 58. This is the only record-level structured ledger of the three.
- **ChatGPT (GPT family), PR #1 (merged), `reviews/2026-11-20/ONE-PAGER-FACT-CHECK.md`.** A findings-level narrative: ten cross-cutting findings (F01 to F10), a per-group document-count table, and an implementation assessment for all nineteen groups, with specific page and record citations. It explicitly reconciles the CSV arithmetic and inspects representative records; it does not individually authenticate all 216 excerpts and is not a per-record ledger.
- **Sol (GPT family), PR #8, branch `sol/nhrf-verify-002-bunny-checkpoint-20261123`.** A 216-row ledger with every record `original_checked=no; disposition=unresolved`. Sol could not reach the Bunny archive from its execution sandbox (`ConnectionError` to both Bunny and raw GitHub; the `web.open`/`container.download` tools refused the URLs). Sol contributes zero dispositions; it contributes a source-access gate and its blocker cohorts.

So WP-C is delivered as: a per-record comparison across whatever each reviewer actually produced (`model-comparison.csv`), and a ranked adjudication queue (`reconciliation-queue.csv`), summarized here.

## 2. The reviewers audit different layers (this is the central result)

Fable's 214 accept / 2 reject is **not** in tension with ChatGPT's ten findings, because the two reviews operate at different layers:

- **Fable audits transcription and placement.** For each record it asks: does the quoted excerpt actually appear on the cited page of the sha256-validated original, and are the corpus `item_type` and `P01-P19` group internally consistent with that text. That is a verification that the dataset faithfully transcribes its sources. It passed for 214 of 216.
- **ChatGPT audits semantics and claims.** It asks: is a counted record an independent recommendation (versus a target, commitment, funding estimate, or duplicate), is the grouping semantically right, and do the implementation statements hold against external primary sources (ordinances, zoning tables, CIB documents). Those are different questions from transcription.

A record can be a faithful transcription (Fable accept) and still be a debatable counting unit or carry a wording-level implementation dispute (ChatGPT finding). The two reviews are largely orthogonal, and the reconciliation value is concentrated where they touch: Fable's two rejects, its duplicate-key flags, and its 58 medium-confidence type flags.

## 3. Where the two disposition-producing reviewers converge (Tier 1)

The striking result: the two reviewers that produced any disposition, from **different model families and run independently**, converge on the same specific records at the exact places ChatGPT's narrative flagged. Ten records are Tier 1 (a Fable substantive flag coincides with a ChatGPT record-level citation):

| record_id | doc / page | group | Fable | ChatGPT finding | agreement |
|---|---|---|---|---|---|
| 102 | Plan_to_Play_2017 p234 | P09 | **reject** (cost estimate, not a recommendation) | F01c (funding estimate $210,905,799) | both exclude |
| 1220 | NashvilleNext_Vol4 p49 | P03 | **reject** + dup `DUP-act323` | F01a (action #323 double-counted pp.49 and 79) | both exclude the duplicate |
| 1295 | NashvilleNext_Vol4 p79 | P03 | dup `DUP-act323` | F01a (same pair) | both identify the pair |
| 668, 669 | Nashville_Open_Space_Plan_2011 p11 | P09 | dup `PHASE-privcons3k` + med | F01b (two 3,000-acre targets) | both identify the doubled target |
| 666, 667, 670, 671 | Nashville_Open_Space_Plan_2011 p11 | P09 | med (target sub-type) | F01b (same page target cluster) | both flag for type/unit review |
| 781 | NEA_1973 p98 | P03 | med (descriptive context, not an action sentence) | F08b (soil-data planning not a sewer recommendation) | both doubt the record is a recommendation |

Both of Fable's independent rejects (102, 1220) fall exactly on ChatGPT F01 examples. This is the strongest evidence in the audit: where one reviewer made a substantive exclusion, a different-family reviewer independently raised the same issue.

## 4. The counting-unit theme is independently confirmed

Fable accepted every record but attached **58 medium-confidence flags**, 50 of them the same note: the record is a `target` sub-type, and "under a strict recommendation-only boundary this would be flagged for type review." That is precisely ChatGPT's F01/F02 challenge: the 216 headline mixes recommendations (137), commitments (43), targets (35) and one funding estimate, so it is a count of coded statement records, not of distinct recommendation events. Two independent reviewers reached the same soft spot from opposite directions. The adjudication question is not whether the transcription is faithful (it is) but whether the chosen counting unit is the one to publish, and whether targets/commitments/estimates are disclosed as such.

## 5. Finding-by-finding mapping (ChatGPT F01 to F10 against Fable record-level evidence)

- **F01 (counting unit, duplicated action):** confirmed at record level. Fable reject 102 (= F01c), reject+dup 1220/1295 (= F01a), dup+med 668/669 and med 666/667/670/671 (= F01b). Adjudicate the counting unit and disclose duplicates/estimates.
- **F02 (two singleton groups P10, P12):** group-level. Fable accepted the P10 record (702) but noted its metric label "Open Space Fund balance (2011) / $5,000,000" mischaracterizes the record; P12 record accepted clean. Framing dispute stands; transcription is sound.
- **F03 (agricultural zoning wording, P04):** group-level wording about implementation, not transcription. Fable accepted the P04 records at Vol4 p71 (1251 P04; 1247 at the same page is P08). No record-level transcription problem; the implementation wording is for adjudication against zoning tables.
- **F04 (tree retention wording, P06/P17):** group-level implementation wording. No Fable record-level objection; adjudicate wording against BL2022-1122.
- **F05 (acquisition mechanism, P08):** group-level implementation wording. No Fable record-level objection.
- **F06 (invasives/site plans, P13/P15):** group-level implementation wording. No Fable record-level objection.
- **F07 (per-group document counts):** presentation-layer, source-file versus consolidated-document counting. Does not change the 216 record count (WP-A reproduced all 19 per-group record counts and the 11 document-count gaps, which are the NashvilleNext/Plan-to-Play consolidation). Adjudicate the displayed document counts and dates from one agreed filter.
- **F08 (four group-assignment challenges):** record level. All four cited records exist and transcribe faithfully (1499 GP1981 p89 P03; 781 NEA p98 P03, which Fable independently flagged med; 1182/1183 CCM Rural p9, P03/P01; 85 P2P2017 p177 P13). Reassignment is a semantic judgment for adjudication; Fable found no transcription error.
- **F09 (capital budget versus appropriation, P02/P08):** external-document implementation claim, outside the record-transcription layer.
- **F10 (canopy measurement date, P07):** external-document implementation claim. Note Fable attached many med flags to P07 Urban Forestry records (420, 466, 467, 480, 483, 485, 492, 507, 508, 516) on the target-sub-type ground, overlapping ChatGPT's attention to P07 wording.

## 6. The one arithmetic item still open (from WP-A)

WP-A reproduced every headline count and isolated the only arithmetic dispute: one row, `Metro_Code_17.28.030` field `17.28.030.A.2`, drives both P01 = 29 versus 30 and total 216 versus 217. `count_funnel.py` excludes it as enacted code; `promise_counts.csv` counts it. WP-A documented the rule and did not resolve it. ChatGPT F07 concerns per-group *document* counts, a separate presentation question, and does not touch this record-count item. The 216-versus-217 decision remains the single count-level adjudication item.

## 7. What this establishes, and what it does not

Established: the dataset faithfully transcribes its sources (Fable 216/216 against sha256-validated originals); the two disposition-producing reviewers converge on the same specific exclusions; the counting-unit mix is the main substantive issue and is confirmed from two directions; the Bunny archive is reachable and checksum-grade (see `coverage-summary.md`).

Not established: a final corrected count; the correctness of ChatGPT's implementation-wording challenges (F03 to F06, F09, F10), which require adjudication against external ordinances and budget documents; a second full-access record-level ledger to stand beside Fable (Sol could not provide one; the second independent record-level review remains the gap in the "two independent reviews" design).

## 8. Files

- `verification/wp-c/model-comparison.csv` — 216 records, per-reviewer status and all ChatGPT finding tags.
- `verification/wp-c/reconciliation-queue.csv` — 140 records needing adjudication, ranked by priority tier.
- `verification/wp-c/coverage-summary.md` — exact coverage numbers, the Bunny reachability result, disposition tallies.
- `verification/wp-c/fable-evidence-ledger.csv` — snapshot of the Fable ledger (PR #9) used as the WP-C input, for reproducibility.
