# NHRF fact-check — executive verdict

**Order:** NHRF-CO-VERIFY002-002 (spaice#190). **Prepared:** 2026-11-24 by Code XO (Opus).
**Frozen corpus:** `ianrhett/nhrf-research@4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`.
**Status:** verified verdict on the published claim. Not a production edit; nothing merged. Publication remains a separate step.

## The verdict

**VERIFIED.** Across 13 consolidated Metro Nashville plans (26 source files), forest and conservation action is **recommended 216 times**, spanning **1973 to 2026**. Every one of the 216 instances was checked against the original source document and found to be a faithful transcription on the cited page.

Defensible public wording:
> Across 13 adopted Metro Nashville plans from 1973 to 2026, the city recommended forest and conservation action 216 times. Every instance has been verified against the original planning document.

## What "recommended" means here (and what it does not)

These are **recommendations**: forest and conservation actions that Metro's adopted plans call for. They are plan-level, non-binding statements. The claim deliberately uses "recommended," not "committed," because adopted-plan language is aspirational, not an enforceable commitment or guaranteed appropriation.

The dataset carries an internal `item_type` sub-coding of the 216 — 137 `recommendation`, 43 `commitment`, 35 `target`, 1 `funding_estimate` — but that is granularity within the corpus, not a claim that 43 are binding commitments. In plan language a "commitment" line is still a non-binding recommendation, which is why all 216 roll up correctly under "recommended."

The claim does **not** assert that any recommendation was funded, enacted, or implemented. Implementation and enforcement are a separate question and are **not** adjudicated in this verdict.

## How it was verified

Two fully independent original-source reviews, each checking all 216 records against sha256-validated original documents, run blind to one another:

| Review | Family | Coverage | Result |
|---|---|---|---|
| Fable ([#9](https://github.com/ianrhett/nhrf-research/pull/9)) | Claude | 216/216 checked, 0 blocked | accept 214, reject 2 |
| Second independent Claude/Opus ([#11](https://github.com/ianrhett/nhrf-research/pull/11)) | Claude | 216/216 checked, 0 blocked; all 26 source files hash-verified (26/26 match) | accept 214, reassign 2 |

A third dispatched review (Sol, GPT, [#8](https://github.com/ianrhett/nhrf-research/pull/8)) produced 0 dispositions because its sandbox could not reach the source archive. That is a sandbox limit, not a corpus defect: the archive was independently confirmed reachable and checksum-grade from a fetch-capable runner.

**Transcription is robust.** Both independent reviewers agree there are no wrong-page citations, no misquotes, and no fabricated records. The second reviewer additionally confirmed page-offset 0 on all 13 documents and matched every source file's sha256 to the registry.

Deterministic count reconciliation (WP-A, [#7](https://github.com/ianrhett/nhrf-research/pull/7)) reproduced the 216 total, the 19 group counts, and the type mix from source rows and documented filters.

## Caveats (bounded, and none of them moves the headline)

1. **216 vs 217.** One enacted-code row (`Metro_Code_17.28.030.A.2`) is correctly excluded as law, not a recommendation. It is the only difference between 216 and an alternate 217. Documented in WP-A; not silently changed.
2. **Intra-plan restatements.** Both reviewers independently flagged a small number of cases where one recommendation is written twice **within a single plan** (for example NashvilleNext action #323, and one Open Space 3,000-acre target). Recurrence of a recommendation **across different plans** is legitimate under a "recommended N times" count; the few intra-plan restatements modestly inflate it. The operator chose to publish 216 with this caveat stated rather than trim.
3. **Files vs documents.** The 216 are drawn from 26 source files that consolidate to 13 documents (NashvilleNext's volumes are one plan; Plan to Play 2026 update plus appendix are one). Report the document count as 13 consolidated / 26 files to avoid a file-vs-document mismatch.
4. **One provisional date.** `Concept_2010_General_Plan_1992` has a provisional adoption year (filed 1991/1992, marked [ASSUMED] in the dataset). It does not affect the 1973–2026 span, whose endpoints (NEA 1973; the 2026 plans) are firm.
5. **Judgment layer is interpretive, not settled.** The two independent reviewers agree on transcription but do not overlap on any of their 4 substantive flags (212/216 disposition agreement, 0/4 flags in common). Whether a given record is best typed a recommendation vs a target or commitment, and its group, is an interpretive call, not a transcription error. These are candidates for a later adjudication pass; they do not change the verified headline.

## What remains (separate, not required to publish this verdict)

- Per-record adjudication of the interpretive disagreements (counting unit; a few type/group calls).
- Implementation and enforcement findings (external ordinances, zoning tables, budget documents) — a different question from "what was recommended."
- Any public-facing publication edit, which per the order is a separate approved PR.

## Inputs

WP-A counts [#7](https://github.com/ianrhett/nhrf-research/pull/7) · WP-B Sol [#8](https://github.com/ianrhett/nhrf-research/pull/8) · WP-B Fable [#9](https://github.com/ianrhett/nhrf-research/pull/9) · WP-C reconciliation [#10](https://github.com/ianrhett/nhrf-research/pull/10) · WP-B second independent Claude [#11](https://github.com/ianrhett/nhrf-research/pull/11) · prior ChatGPT audit [#1](https://github.com/ianrhett/nhrf-research/pull/1).

**Bottom line:** the "recommended 216 times" claim is verified and defensible as stated, with the caveats above disclosed. Nothing in this corpus overturns it.
