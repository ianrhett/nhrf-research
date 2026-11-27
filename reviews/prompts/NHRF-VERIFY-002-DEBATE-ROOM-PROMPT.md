# NHRF — Independent Fact-Checking, Adversarial Review & Evidence Adjudication

**Protocol:** NHRF-VERIFY-002  
**Date:** November 20, 2026  
**Project:** Alliance to Conserve Nashville's Highland Rim Forest  
**Research artifact:** *Recommended 216 Times*, v1.7.1  
**Reviewers:** Sol and Fable  
**Objective:** Establish a reproducible, independently verifiable, defensible body of research and an accompanying set of publication-ready claims.

---

## 1. Mission

The Alliance to Conserve Nashville's Highland Rim Forest has published research examining Metro Nashville's conservation recommendations from 1973 through 2026.

The central published claim is that Metro made the same 19 forest-related recommendations 216 times across 53 years, with only one classified as fully implemented.

An initial independent ChatGPT audit reproduced the headline arithmetic but identified potential factual inaccuracies, methodological inconsistencies, questionable classifications, and unsupported or overly broad implementation assessments.

**Your mission is not to validate either the original publication or that audit.**

Your mission is to establish, through independent examination of the data and original primary sources:

1. What Metro Nashville actually recommended.
2. How frequently those recommendations occurred.
3. Whether the research accurately extracted, classified, grouped and counted the statements.
4. What Metro subsequently enacted, funded, implemented and delivered.
5. Which conclusions can be stated as facts, which require qualification, and which remain unresolved.
6. The strongest defensible public claims supported by the evidence.

The published figure of 216 is not a target to preserve. Neither are the existing 19 groups or the current implementation classifications.

**Accuracy takes precedence over the preservation of any existing conclusion.**

Consensus among reviewers is not proof. A finding is established through evidence and reproducible reasoning, not agreement.

---

## 2. Review architecture

The review consists of four phases.

### Phase 1 — Independent blind audits

Sol and Fable independently audit the same frozen research snapshot.

Each reviewer must:

- Operate in a separate context without access to the other reviewer's work.
- Avoid viewing the previous ChatGPT fact-check report.
- Independently inspect the repository and original source documents.
- Independently reproduce the published calculations.
- Independently evaluate the methodology, classifications and implementation claims.
- Seek evidence that contradicts the publication, including evidence omitted from the repository.
- Produce a complete, evidence-linked audit.

Neither reviewer should be told what findings the other reviewer or ChatGPT reached.

The orchestration process must preserve genuine independence. Do not simply ask one reviewer to critique another reviewer's output.

### Phase 2 — Freeze independent findings

Before comparison begins:

- Save Sol's completed independent audit.
- Save Fable's completed independent audit.
- Preserve each reviewer's findings, evidence citations, calculations and limitations.
- Identify the exact repository commit and source versions examined.
- Record any documents that could not be accessed.
- Prevent retrospective changes to Phase 1 results.

**Do not proceed to Phase 3 until both reviews are independently completed and preserved.**

If context isolation is impossible, report that the reviews are not fully blind. Do not claim otherwise.

### Phase 3 — Adversarial comparison and adjudication

Only after Phase 2, reveal:

- Sol's independent audit.
- Fable's independent audit.
- The previous ChatGPT audit.

Compare the three reviews claim by claim.

Identify agreement, disagreement, omissions, contradictory evidence, and methodological differences.

Adjudicate disagreements against original primary sources.

### Phase 4 — Synthesis and publication recommendations

Produce two distinct outputs:

**A. Authoritative research conclusions**

The best-supported factual findings, methodologies, calculations, implementation assessments and unresolved questions.

**B. Defensible publication claims**

Concise, understandable, appropriately qualified statements suitable for public communication.

The second must be traceable to the first.

Publication language may simplify the research but must never change its meaning, omit material limitations, or imply greater certainty than the evidence supports.

---

## 3. Source repository and frozen snapshot

**Repository:**

https://github.com/ianrhett/nhrf-research

**Required baseline commit:**

`4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`

Snapshot:

https://github.com/ianrhett/nhrf-research/tree/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636

All independent Phase 1 calculations must refer to this frozen snapshot.

Do not silently substitute later revisions from `main`.

### Primary publication

`one-pager/NHRF_Recommended_216_Times_v1.7.1.pdf`

https://github.com/ianrhett/nhrf-research/blob/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636/one-pager/NHRF_Recommended_216_Times_v1.7.1.pdf

Examine every textual and numerical assertion, including the chart, timeline, implementation notes, document counts, footer, and attribution.

### Primary research data

All paths below refer to the frozen snapshot.

| File | Purpose |
|---|---|
| `data/NHRF_Recommendations.xlsx` | Full research workbook |
| `data/recommendation_statements.csv` | Extracted records, quoted passages, source pages, classifications and verification flags |
| `data/sources.csv` | Source metadata, official URLs, inclusion decisions |
| `data/promise_groups.csv` | Mapping of records into recurring recommendation groups |
| `data/distinct_promises.csv` | Group definitions, implementation classifications and supporting evidence |
| `data/recommendations.csv` | Summary of the 19 recommendations, frequencies, documents and implementation assessments |
| `data/promised_vs_delivered.csv` | Comparisons between stated goals and reported outcomes |
| `data/promise_counts.csv` | Supporting frequency counts |
| `data/inconsistencies.csv` | Documented inconsistencies in the research |
| `data/CHANGELOG.md` | Dataset correction and revision history |
| `data/VERSION` | Dataset version identifier |

Do not assume the contents of these files are consistent merely because they are published together.

### Methodology and reproduction

- `methodology/methodology.html`
- `methodology/build.py`
- `scripts/count_funnel.py`
- `scripts/funnel.json`
- `scripts/presentation_data.py`
- `one-pager/build_one_pager.py`
- `one-pager/one-pager.tmpl.html`

Review the actual implemented logic, not just the methodology's prose description.

### Original sources and provenance

- `sources/MANIFEST.csv` — source inventory, official URLs, page counts, file hashes and retrieval metadata.
- `sources/BUNNY-URLS.csv` — archived source locations.
- `sources/` — copies of selected supporting documents.
- URLs in `data/sources.csv` — original Metro documents and government records.

Prefer original government sources when verifying factual claims.

Use archived documents when originals are inaccessible, but record the provenance, retrieval method, applicable hash verification and any remaining uncertainty.

When an original source is inaccessible, mark its claims accordingly. Never imply that an unavailable document was inspected.

Supplement the repository with government records when necessary to evaluate implementation, including ordinances, resolutions, zoning rules, Parks Board actions, budgets, spending plans, recorded land transactions and agency reports.

### Previous ChatGPT review — withheld until Phase 3

**Do not open this during Phase 1.**

https://github.com/ianrhett/nhrf-research/pull/1

Report path:

`reviews/2026-11-20/ONE-PAGER-FACT-CHECK.md`

This report contains the previous audit's evidence, calculations, challenges and recommendations. It must be treated as another reviewer's work, not as authoritative findings.

---

## 4. Phase 1A — Independently reproduce every published statistic

Recalculate all major numbers directly from source records.

At minimum:

1. Total source files and consolidated documents.
2. Included and excluded source documents.
3. Total extracted statements.
4. Recommendation-type statement counts.
5. Forest-related statement counts.
6. Number of statements assigned to the 19 groups.
7. Statements per group.
8. Distinct contributing documents per group.
9. Year-by-year statement counts.
10. Timeline chart positions and dot-size calculations.
11. Implementation classification totals.
12. First and last occurrence dates.

Run the repository's counting scripts where possible.

**Also produce an independent implementation of the calculations.**

Do not simply read `funnel.json` or trust the published output.

If a script cannot run, document the exact dependency, input-path or runtime failure. Do not claim execution success based on source-code inspection.

### Counting-unit analysis

Explicitly distinguish:

- Individual text occurrences.
- Unique source passages.
- Distinct policy recommendations or actions.
- Commitments.
- Quantitative targets.
- Funding estimates.
- Repetitions within the same document.
- Repetitions across separate documents.
- Multiple source files representing one consolidated Metro plan.

Determine whether each published number correctly describes its underlying unit.

If different defensible counting rules produce different totals, report each result and its methodology.

Do not select the counting method solely because it reproduces 216.

### Required output

A reconciliation table containing:

`claim_id | published_value | calculated_value | counting_rule | source_records | difference | verification_status | explanation`

Every numerical finding must be independently reproducible.

---

## 5. Phase 1B — Verify the underlying records

### Statement-level verification

For each of the 216 records in the published 19 groups:

1. Locate the cited source document.
2. Examine the cited page and surrounding context.
3. Confirm the quoted passage accurately reflects the original.
4. Confirm the source's document date, status and adoption history.
5. Evaluate the record type.
6. Evaluate its recommendation-group assignment.
7. Check whether the passage duplicates another counted record.
8. Record whether the source supports the assigned meaning.

Do not limit examination to the existing verification flags.

Those flags describe prior verification work; they do not substitute for this review.

Also investigate the broader 340-record forest-related population and relevant excluded or unassigned records to detect omissions, inconsistent inclusion or incorrect grouping.

Where exhaustive verification is prevented by inaccessible sources, provide an explicit coverage report. For example, distinguish independently authenticated records from records only checked against the existing CSV, records not checked, and records whose source could not be retrieved.

**Do not call a record independently verified unless its original source was actually examined.**

### Classification audit

Evaluate whether the record belongs in its designated group.

Challenge loose thematic connections.

A passage about protecting watersheds, for example, does not automatically constitute a recommendation to prohibit development on steep slopes.

A recommendation to finance sewer extensions does not automatically constitute a recommendation to prevent them.

However, consider surrounding context and the intended methodology before rejecting a classification.

For every disputed assignment, record a reasoned argument both for inclusion and against inclusion.

### Exclusion and completeness audit

Determine whether the original research omitted material documents, recommendations, implementation actions or evidence.

Pay particular attention to:

- Excluded drafts versus adopted documents.
- Changes across NashvilleNext volumes or amendments.
- Historical plan editions.
- Newly adopted policies.
- Source documents containing implementation evidence but excluded from recommendation counts.
- Relevant agency records not present in the repository.

Document the cutoff date for each conclusion.

---

## 6. Phase 1C — Independently evaluate implementation

For each recommendation group P01–P19, investigate four separate dimensions.

**1. Policy adoption**

Was the recommended principle adopted into official planning policy?

**2. Legal or administrative implementation**

Was a binding ordinance, regulation, departmental policy, program or administrative mechanism established?

**3. Funding and execution**

Was the action appropriated, staffed, funded, undertaken or otherwise operationalized?

**4. Measured outcomes**

Was the intended conservation outcome achieved, or is progress documented against a meaningful baseline?

These dimensions must not be conflated.

Examples:

- Inclusion in the Capital Improvements Budget does not necessarily mean funds were appropriated.
- An appropriation does not establish expenditure or completion.
- An enacted ordinance does not establish full enforcement or effectiveness.
- A conservation acquisition announcement does not necessarily establish completed Metro ownership.
- A tree replacement requirement is not necessarily an existing-canopy retention requirement.
- A site-specific management plan may constitute partial progress without fulfilling a countywide recommendation.
- A planning policy is not automatically a binding regulation.

### Assessment standards

For each recommendation, first define the original intended outcome and relevant scope.

Then assess the evidence, avoiding arbitrary percentage-of-completion estimates.

Possible findings:

- Fully implemented.
- Partly implemented.
- Not implemented, supported by adequate evidence.
- No implementation reported or found.
- Not independently verified.
- Not yet due.
- Not meaningfully scorable without a clearer definition.

Distinguish an implementation classification from confidence in that classification.

A partly implemented recommendation may be supported by strong evidence; a fully implemented classification may be weakly supported.

### Negative evidence

Apply a particularly high standard to categorical negative statements.

Examples include:

- No program exists.
- No rule protects existing trees.
- No conservation acquisition mechanism exists.
- No natural-area management plan exists.
- No funding was appropriated.

Identify what records were searched, the relevant time period, and what would falsify the assertion.

**Failure to find evidence is not, by itself, proof of nonexistence.**

---

## 7. Phase 1D — Verify every public-facing claim

Review the one-pager independently, line by line.

For each assertion, classify it:

- **VERIFIED:** Directly supported by adequate evidence.
- **VERIFIED WITH QUALIFICATION:** Substantially supported but requires additional scope, dates or limitations.
- **INCORRECT:** Contradicted by sufficient evidence.
- **UNVERIFIED:** Evidence insufficient or unavailable.
- **INTERPRETIVE:** Depends on an explicit policy, methodological or evaluative judgment.

A claim may have both a factual component and an interpretive component. Separate them.

Verify the mayoral quotation against its original context, including attribution, omitted language and date.

For every proposed correction, supply replacement wording that does not exceed the evidence.

---

## 8. Phase 2 — Preserve the blind audits

The orchestrator must preserve the completed Phase 1 work from both reviewers before allowing cross-review.

Use separate report-only branches originating from the frozen baseline commit, where GitHub write access is available.

Suggested branch names:

- `review/sol-independent-2026-11-20`
- `review/fable-independent-2026-11-20`

Suggested report destinations:

- `reviews/independent-2026-11-20/sol/`
- `reviews/independent-2026-11-20/fable/`

Each reviewer should produce:

- `audit.md` — complete independent audit.
- `findings.csv` — machine-readable finding ledger.
- `counts.csv` — independently calculated counts.
- `implementation.csv` — P01–P19 assessments.
- `coverage.md` — source verification coverage, inaccessible documents and limitations.
- `methodology.md` — actual procedures, scripts, assumptions and deviations.

If these cannot be committed, export equivalent immutable artifacts with timestamps and identifiable content hashes.

Keep each reviewer’s files separate. Never allow one reviewer to overwrite or revise the other's results.

Use a PR for each review branch. Do not merge at this stage.

---

## 9. Phase 3 — Adversarial comparison

After both blind reviews are preserved, release the previous ChatGPT audit and both independent reports.

Construct a three-reviewer comparison covering:

- Every independently discovered finding.
- Every numerical disagreement.
- Every challenged group assignment.
- Every disputed implementation status.
- Every claimed omission.
- Every factual correction.
- Every important difference in methodology.

Do not restrict this phase to findings identified by ChatGPT.

### Evidence-based debate rules

For each disputed finding:

1. State the original claim.
2. Present Sol's findings and supporting evidence.
3. Present Fable's findings and supporting evidence.
4. Present ChatGPT's findings and supporting evidence.
5. Identify precisely what the reviewers agree or disagree about.
6. Retrieve and inspect the decisive original evidence.
7. Explain the applicable counting, interpretation or implementation standard.
8. Present the strongest reasonable counterargument.
9. Assign a final adjudication status.
10. Specify resulting changes, if any.

Allowed adjudication outcomes:

**ACCEPT — REJECT — QUALIFY — UNRESOLVED**

These are verdicts on the challenged finding, not automatic implementation statuses.

A majority vote does not constitute adjudication.

Agreement without independently inspected evidence is not sufficient.

When original evidence cannot resolve the dispute, preserve the disagreement and identify what would resolve it.

### Adjudication ledger

Produce a machine-readable ledger containing at least:

`finding_id | original_claim | Sol_position | Fable_position | ChatGPT_position | decisive_evidence | primary_source_url | document_page | verdict | rationale | confidence | required_change | effect_on_counts | effect_on_status | remaining_uncertainty`

Treat the prior ChatGPT review itself adversarially. Correct its mistakes and reject findings that fail scrutiny.

---

## 10. Phase 4 — Synthesize the authoritative research

Generate the strongest evidence-supported research conclusions.

### Deliverable A — Research conclusions

Produce a consolidated report with:

1. Final recommended counting methodology.
2. Recalculated totals and recommendation frequencies.
3. Independently authenticated source-record coverage.
4. Final implementation assessments.
5. Primary-source evidence for each material conclusion.
6. Methodological judgments and justifications.
7. Remaining disagreements and uncertainties.
8. Version and provenance information.
9. The changes required to make the research fully reproducible.

Separate established facts from interpretation.

The research conclusions should enable an independent skeptical reviewer to reproduce the calculations and evaluate the same evidence.

### Deliverable B — Publication claims

Produce a separate public-facing claims inventory.

For each candidate claim, provide:

- Proposed publication wording.
- Exact underlying factual finding.
- Evidence references.
- Appropriate qualification or scope.
- Confidence level.
- Any material risk of misleading readers.
- Publication disposition: APPROVE, REVISE, HOLD or REJECT.

Develop the strongest concise headline justified by the adjudicated findings.

Consider alternatives to “Recommended 216 times” if a different measurement or framing better represents the evidence.

The publication should communicate the significance of decades of conservation planning without exaggerating what is known.

Do not dilute well-supported findings merely to avoid strong conclusions.

Do not strengthen uncertain findings merely for rhetorical effect.

### Deliverable C — Correction and verification plan

Produce a deterministic correction plan identifying:

- Exactly which source records require changes.
- Exactly which calculations need regeneration.
- Exactly which implementation classifications need revision.
- Which scripts or templates must change.
- Which source documents or records remain to be obtained.
- Which corrections affect published figures.
- Which changes are wording-only.
- The tests required to verify the corrected publication.

Prefer minimal, auditable changes. Avoid opportunistic refactoring or unrelated repository work.

Do not modify the original research or publication during adjudication.

---

## 11. Repository and execution discipline

All work is review-only until adjudication is complete.

- No direct edits to `main` or production artifacts.
- One review scope per branch.
- No commits from dirty worktrees.
- Pull requests required for all proposed changes.
- Preserve the frozen baseline and previous published release.
- Do not alter existing source data to make counts agree.
- Do not rewrite prior reviewers' findings.
- Keep raw evidence, interpretations and decisions distinct.
- Do not merge a review PR without explicit approval.

The final adjudication may recommend a subsequent, separately scoped correction branch and PR.

No publication, dataset or methodology changes are automatically authorized by this prompt.

If necessary source access or code execution is unavailable, disclose the limitation immediately, preserve completed work and produce a precise blocker report.

Do not fabricate execution results, primary-source citations or verification coverage.

---

## 12. Final acceptance criteria

The review is complete only when:

1. Both independent Phase 1 audits are preserved.
2. The original and independent calculations are reconciled or their differences explained.
3. Every material disputed classification has an adjudicated result or documented unresolved status.
4. Every published numerical figure traces to an explicit counting method and identifiable records.
5. Every retained implementation assessment has adequate supporting evidence and a clear scope.
6. Every categorical claim is supported or appropriately qualified.
7. All material counterevidence has been evaluated.
8. All source limitations and verification gaps are disclosed.
9. The final claims inventory is traceable to the research conclusions.
10. The correction plan is reproducible and can be applied without altering the historical evidentiary record.

**Do not claim 100% verification if any material evidence remains unavailable.**

Where evidence is incomplete, state precisely what is known, what is inferred and what remains unverified.

The goal is the highest achievable factual defensibility, not artificial certainty.

---

## 13. Required final handoff

The orchestrator must deliver:

**Independent reports**
- Sol's preserved blind audit.
- Fable's preserved blind audit.

**Adjudication**
- Three-reviewer comparison.
- Consolidated evidence and adjudication ledger.
- Final recommendation classifications.

**Synthesis**
- Authoritative research conclusions.
- Approved, qualified or rejected public claims.
- Proposed corrected figures and headline.
- Remaining uncertainty register.
- Minimal-change correction plan.

Include GitHub commit references and PR links for every preserved artifact.

Identify unresolved findings prominently. Do not silently exclude them from the final summary.

## Governing principle

**An independently reproducible fact is stronger than a consensus opinion.**

The purpose of this work is to establish a durable evidentiary record of Metro Nashville's conservation recommendations, the actions taken in response, and the extent to which those recommendations were fulfilled.

The record should remain credible even under examination by reviewers who disagree with the Alliance's policy objectives.

**Begin Phase 1. Keep Sol and Fable isolated until both independent reviews are preserved.**
