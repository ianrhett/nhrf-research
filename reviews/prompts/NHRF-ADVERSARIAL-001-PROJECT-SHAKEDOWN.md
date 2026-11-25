# NHRF — Project-Wide Adversarial Shakedown and Final Claims Adjudication

> **OPERATOR IS NOT A COURIER. NO COPY/PASTE HANDOFFS.**
>
> The operator has expressly rejected being asked to relay prompts, source files, results or instructions between models, rooms, repositories and agents. **Do not ask the operator to copy, paste, forward, retype or manually file any output.** Read this prompt and its cited sources directly; deliver findings through existing GitHub and execution workflows. CSO/XO/runner are responsible for any transport and publication of artifacts. If this Debate Room is read-only, it must *adjudicate* the evidence supplied by existing execution lanes—not request manual relay by the operator.
>
> **DO THE RESEARCH, NOT A DEBATE ABOUT THE DEBATE.** This room must identify weaknesses, examine contradictory evidence, require actual corrections and produce a reconciled claim set. Procedural questions are delegated to XO without a room discussion. Work that needs code execution, bulk inspection or files must be dispatched by XO through the existing host job workflow. No workflow redesign.

**Protocol ID:** NHRF-ADVERSARIAL-001  
**Prepared:** 2026-11-23  
**Purpose:** Exhaustive, adversarial, source-grounded examination of the NHRF research and resulting public claims, followed by explicit reconciliation of independent findings.  
**Scope:** Research corpus, counting methodology, source quotations, group assignments, implementation judgments, historical timeline, conservation geography, legal/regulatory/funding claims, infographic, and public-facing claims. This is **not** a website/deployment redesign.  
**Status:** Review-only. No source, code, chart, publication or production edits before approved corrections.

## 1. Mandate and standard of proof

Assume the role of a skeptical external auditor who **does not share the Alliance's objectives**, and whose job is to find material errors that a sophisticated opponent could use to discredit the research.

Your mission is to try to **falsify every material assertion** before accepting it. Look for errors, exaggerations, unsupported generalizations, hidden denominators, selective use of sources, policy/legal category mistakes, outdated evidence, contradictory statements, duplicated passages, unpublished exceptions, and claims that go beyond what the originals say.

The goal is **the most defensible possible final claims**, not saving the current “216” figure, the 19 groups, the claimed 53-year span, or the current implementation ratings.

The standard is not “all models agree.” The standard is:

- Every published **factual** claim has exact, accessible primary-source support and a reproducible derivation where it is numerical.
- Every published **interpretation** states the rule and scope on which it depends.
- Every materially contradictory piece of evidence has been examined.
- Material uncertainty is disclosed or the claim is held back.
- The final claims inventory is internally consistent with the reconciled dataset.
- A skeptical independent reader can follow the cited trail to the underlying source and reach the reported result.

**100% defensible does not mean 100% omniscience.** Claims with evidence gaps must be qualified, replaced, or withheld; the report must never claim that missing evidence was checked.

## 2. Canonical baseline and evidence locations

Freeze the research **as evaluated**, separately from current publication status.

- **Canonical repository:** https://github.com/ianrhett/nhrf-research
- **Frozen baseline commit for v1.7.1 audit:** `4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`
- **Public artifact:** `one-pager/NHRF_Recommended_216_Times_v1.7.1.pdf`
- **Statements:** `data/commitments.csv`
- **Sources and inclusion decisions:** `data/sources.csv`
- **Group-to-record assignments:** `data/promise_groups.csv`
- **Groups, counts and implementation notes:** `data/recommendations.csv` and `data/distinct_promises.csv`
- **Outcome comparisons:** `data/promised_vs_delivered.csv`
- **Workbook:** `data/NHRF_Commitments.xlsx`
- **Version history:** `data/CHANGELOG.md`, `data/VERSION`, `data/versions/`
- **Methodology and calculations:** `methodology/methodology.html`, `scripts/count_funnel.py`, `scripts/funnel.json`
- **Publication generation:** `one-pager/build_one_pager.py` and `one-pager/one-pager.tmpl.html`
- **Primary-source inventory and provenance:** `sources/MANIFEST.csv`, `sources/BUNNY-URLS.csv`, documents in `sources/`, and original URLs from `data/sources.csv`

**Fleet-accessible repository:** `ianrhett/nhrf` (research equivalents generally under `docs/research/commitments/`; infographic under `docs/research/one-pager/`; source manifest under `docs/research/sources/`). For this prompt, use branch `docs/nhrf-adversarial-shakedown-2026-11-23` at `docs/research/NHRF-ADVERSARIAL-001-PROJECT-SHAKEDOWN.md`.

The public `nhrf-research` repository remains authoritative. **Never substitute the latest `main` for the frozen baseline without stating a separate snapshot**. The fleet mirror is an access bridge, not a new source of truth. Confirm source hashes/versions if there is any discrepancy.

### Related reviews — for comparison, not assumed truth

- Previous ChatGPT audit: https://github.com/ianrhett/nhrf-research/pull/1 — `reviews/2026-11-20/ONE-PAGER-FACT-CHECK.md`.
- Existing independent verification protocol: https://github.com/ianrhett/nhrf-research/pull/2 — NHRF-VERIFY-002.
- Escarpment-specific challenge: https://github.com/ianrhett/nhrf-research/pull/5 — NHRF-P02-ESCARPMENT-001.
- Audit execution order: https://github.com/ianrhett/spaice/issues/190#issuecomment-7112290239.

**Important independence gate:** If Sol/Fable blind reviews are not yet preserved, do not expose these related challenge findings to those reviewers or present this room's conclusions as independent. XO completes and freezes blind audits in existing execution lanes first. This room is the adversarial **comparison, cross-examination and adjudication** stage once independent artifacts exist. It does not replace the source audit.

## 3. Attack surfaces — examine the entire substantive claim set

### A. Provenance and source authority

For each material source, establish its correct title, publisher, document date, adopted/draft status, scope, revision/amendment history, page numbering, retrieval URL, accessible copy and checksum where available.

Distinguish **adopted official plans** from staff background reports, advisory recommendations, drafts, statutory rules, council resolutions, meeting minutes, implementation evidence and third-party publications. Establish whether the denominator is “official Metro documents,” “adopted plans,” or something narrower; do not use these interchangeably.

Audit omissions, exclusions and new evidence that could falsify a conclusion. Verify the significance of reports not included in the counted corpus instead of assuming exclusion means irrelevance.

### B. Every count, denominator and time period

Independently reproduce the complete count funnel, including:

- Total rows and files in inventory.
- Included versus excluded documents and reasons.
- Source files versus consolidated documents (e.g. NashvilleNext volumes, Plan to Play 2026 update and appendix).
- Forest-related records, selected P01–P19 records, and individual per-group document counts.
- Exact classification by type: recommendation, commitment, target, funding estimate, background statement, implementation report, duplicate.
- Within-document repetition, between-document repetition, duplicate quotations, related but nonidentical targets, reused policy actions.
- Year range: year of original recommendation, adoption, amendment, publication, reporting and implementation; identify which is actually being plotted.
- All chart labels, bar/dot/axis logic, status totals and dates.

Produce **sensitivity counts** using at least (i) currently coded statement occurrences, (ii) unique passages/actions under a declared deduplication rule, and (iii) records that survive independent semantic and original-source verification.

The headline unit must be explicit. A coded occurrence does not necessarily mean a unique recommendation; a target or dollar estimate is not automatically a recommendation. Two singleton groups cannot be described as repeated multiple times.

### C. Validate original quotations and assignments

**Every one of the 216 currently selected records is in scope.** Check its original document page and meaningful surrounding context; verify exact language, source date, meaning, category, policy mechanism and group assignment. Identify any omitted records needed for a fair account. Inspect the broader 340-record forest-related population and exclusions for inconsistent selection.

Report separately:

1. Records whose original source pages were independently inspected.
2. Records checked only against existing transcriptions or derived data.
3. Records not checked.
4. Records blocked by inaccessible or missing originals.
5. Records accepted, rejected, reassigned or merged as duplicates.

Do not count a CSV-to-CSV comparison or an OCR verification flag as an independent reading of the original.

For ambiguous passages, cite the text and give the strongest argument **for** and **against** its assigned group. Do not let group titles retroactively enlarge what the source said.

### D. Reassess all P01–P19 group definitions

For every group, check whether a single coherent recommendation exists, whether statements are genuinely comparable across decades, and whether proposed instruments or geographic scopes differ materially. Split or narrow groups when required by evidence; keep changes explicitly traceable.

**P02 is a required stress test:** recognition of the Highland Rim Escarpment, Conservation-Nonurban planning policies, proposed preservation, legal protection and formal named conservation-area designation are different claims. Do not label the historical recommendation as a call for formal designation unless the original language supports that.

Apply the same rigor to agricultural zoning, tree retention, acquisition programs, easements, stream and habitat management, canopy goals, parks acreage, capital financing and broad aspirational goals.

### E. Reassess implementation rather than repeating existing notes

For each P01–P19 recommendation, clearly separate:

1. What was recommended, by whom, when and for what geography.
2. Policy recognition/adoption.
3. Binding law, zoning, restrictions, permits or administrative mechanism.
4. Funding request, Capital Improvements Budget listing, actual appropriation, encumbrance, expenditure, and completion.
5. Actual action, measurable outcome and remaining gap.
6. Applicable exemptions, exceptions, conditions, time horizons and later superseding policies.

A plan's designation is not automatically a binding conservation area. A funded program is not automatically completed. Conversely, a limited but real program cannot be described as nonexistent.

**No categorical absence claim without a defined search.** For example, “no acquisition mechanism,” “no tree retention rules,” “no invasive-species plan,” and “no conservation areas designated” require review of counterexamples and clear limitation of scope. Treat “not found,” “not implemented,” “not yet due,” “not reported,” “not measurable” and “not verified” separately.

Determine if each existing status (**Implemented**, **Partly implemented**, **No implementation reported**) should be retained, corrected, qualified or replaced with a better-scoped category. Report evidence confidence separately from implementation degree.

### F. Dates, geography and public presentation

Audit the historical start/end dates and whether the claims refer to 1973–2026, 1973–2025, or narrower periods for each claim. Do not treat an amended volume's publication date as the date of every constituent recommendation.

Distinguish Davidson County, Metro Nashville-Davidson County, urban service districts, rural conservation transects, the Highland Rim Escarpment and the broader Highland Rim forest region. Verify acreage, mapping, boundary, conservation-area terminology, and whether any proposed protection applies countywide or only to particular parcels.

Audit the one-pager, public executive summary, research webpage/copy, chart headings, captions, quotation attribution, claims of first/only/largest, “recommended X times,” and implementation status headlines. If a public claim is outside the 216-record corpus, it still needs a source-level review before approval.

### G. Contradictions and adversarial external evidence

Seek government primary-source evidence **outside the research repository** that undermines or complicates the original claims. Examples: older or newer zoning classifications, Parks Board policies, ecological or tree ordinances, adopted maps, easement/land records, acquisition programs, budgets, legislation, agency status reports and climate/parks plans.

The absence of information from the research corpus is not evidence the government did nothing. Search and document the records that could refute claims of nonimplementation.

For each source conflict, identify chronology, jurisdiction, authority, supersession, and exactly which claim it affects. Preserve unresolved contradictions; do not vote them away.

## 4. Independent reviews and debate-room behavior

**Before adjudication:** XO arranges independent reviews by Sol and Fable, preserved with commit/hash, actual commands used, source-coverage counts and evidence ledgers. The existing ChatGPT report is fixed at its recorded commit. Do not silently edit a frozen independent report after another is visible.

**In this room:** compare the original publication, Sol, Fable and ChatGPT positions on **every material claim**, including points they agree on. Agreement may share a common error. All claims must pass an evidence challenge; don't send only disagreements for review.

Structure each substantive turn as:

**CLAIM → PRIMARY EVIDENCE → STRONGEST COUNTEREVIDENCE → RULE/APPLICATION → VERDICT → SPECIFIC CONSEQUENCE.**

Decide an available factual issue by reading the source, not debating an opinion. Debate only a genuinely unresolved interpretation after the original evidence and standard are available. If evidence remains missing or genuinely contradictory, mark **UNRESOLVED** and say what primary record would settle it.

Allowed finding verdicts: **CONFIRMED / CORRECTED / QUALIFIED / REJECTED / UNRESOLVED**.

A verdict must identify the affected source records, counts, implementation status and publication wording, if any. **No final figure may be produced solely by majority vote.**

## 5. Mandatory reconciliation: differences must become decisions

Create a **master claim ledger** and a **row-level source adjudication ledger**. Do not close the review at a list of disagreements or “the models had different interpretations.”

For each difference between Sol, Fable, ChatGPT and the original research:

1. State the exact original assertion or source row.
2. Record all reviewer values/positions.
3. Identify whether the difference is arithmetic, source interpretation, classification, deduplication, date, scope, legal effect, or missing evidence.
4. Reopen the precise primary-source page(s) and relevant law/official record.
5. Apply a written decision rule consistently across all affected cases.
6. Issue a reasoned verdict and calculate all consequences.
7. Run the applicable count reconstruction again.
8. Update the proposed final claim and note any uncertainty.

Reconcile even cases of apparent unanimous agreement against original evidence. When genuine uncertainty remains, **the correct final output is a qualified or withheld claim**, not a forced consensus.

Do not mix three different quantities:

- **Published/baseline count:** what the current research records say.
- **Reproduced count:** what independently executing the published rule yields.
- **Adjudicated count:** what survives the evidence and agreed rule.

These may differ. Explain every difference.

## 6. Required concrete deliverables

### Deliverable 1 — Master numerical reconciliation

A table including:

`metric | original_publication | original_dataset | Sol | Fable | ChatGPT | independently_reproduced | adjudicated | counting_unit | decision_rule | evidence | outstanding_gap`

Required metrics: documents/files included, forest-related count, P01–P19 count, each group's frequency and unique-document count, unique actions, date range, adoption-status denominator, status classifications and any published acreage or dollar claims.

**Give the actual final numbers**, not merely “counts need reconciliation.”

### Deliverable 2 — All-source and all-record ledger

One machine-readable row per originally selected statement, plus separate entries for material omitted records:

`record_id | source_id | source_version | page | quote_location | original_text_checked | statement_type | original_group | adjudicated_group | duplicate_key | include | rationale | reviewer_positions | primary_source_url | verdict | confidence | blocker`

Provide a coverage numerator and denominator for original-source inspection: **N of 216 checked, M unreachable, K unresolved**. Do not silently shrink the denominator.

### Deliverable 3 — Nineteen implementation verdicts

`group | exact_recommendation | applicable_geography | original_status | Sol_status | Fable_status | ChatGPT_status | final_status | enacted_policy | enforceable_rule | funds | actions | measurable_results | contradictory_evidence | primary_sources | missing_evidence`

Use specific, dated evidence; distinguish lack of a countywide program from existence of limited programs.

### Deliverable 4 — Claim approval register

**Every candidate public-facing claim** should have:

`claim_id | proposed_exact_text | historical_derived_facts | original_sources | scope | confidence | material_counterargument | approved/qualify/hold/reject | rationale`

Separate **factual research conclusions** from **approved publication language**. Require 100% traceability for retained claims; no unsupported numbers, invented legal implications or implied proof of absence.

### Deliverable 5 — Final executive verdict and corrections

Start the final report with this answer, in specific numbers:

> “After adjudication, **N** qualifying records representing **M** defensibly grouped policy priorities appear across **D** distinct eligible official documents from **YEAR–YEAR**, under the following counting definition: ____.”

If this exact statement cannot be supported, substitute the **strongest narrower claim that can be supported** and say precisely what prevents the broader claim.

Then provide:
- A corrected 1-paragraph public summary and 2–3 headline alternatives with evidence.
- A concise decision table: **what we accept, revise, drop or cannot yet verify**.
- A change ledger for CSV/workbook/script/one-pager/publication claims (not edits made during review).
- Small, independently testable correction work packages and acceptance tests.
- An unresolved-evidence register with exact source/record needed and responsible next action.

## 7. Stop conditions and ownership

The debate room must **not** end with another proposal to start work, a procedural recap, or a vague “all agreed.” It ends with one of:

1. **ADJUDICATED:** completed claim, numerical and implementation ledgers, tested proposed figures, documented changes; or
2. **EVIDENCE BLOCKED:** a substantive partial reconciliation plus named specific missing primary sources, affected figures and an actionable retrieval task.

Do not report the job as complete with unchecked records or unresolved material claims hidden in footnotes.

**XO owns execution, collection, artifact publication and logistics.** The debate room challenges and adjudicates the evidence; source extraction and computation run in existing host jobs. CSO may participate in interpretation but cannot erase Fable's independent result, and model consensus alone is never the basis for a verdict.

The owner must not be required to operate as messenger, orchestrator, or manual file transporter.

All outputs go into new review-only GitHub artifacts through separate branches and PRs; **no edits to production or the published dataset before an approved correction PR**. Keep one correction scope per branch. Do not spend the debate on repository permissions, process redesign or which seat should paste what. Use the existing systems.

**Begin by testing the central published proposition “216 statements / 19 recommendations / 13 documents / 1973–2026,” and produce a reconciled numeric answer. Then systematically challenge and adjudicate every group and every material public claim.**
