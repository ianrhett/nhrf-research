# NHRF P02 — Highland Rim Escarpment: conservation policy versus formal designation

> **OPERATOR IS NOT A COURIER — NO COPY/PASTE HANDOFFS.**
>
> The operator has explicitly directed that prompts, source links, instructions and findings must travel through repository artifacts and existing agent/runner mechanisms. **Do not ask the operator to copy, paste, relay, retype, or ferry this prompt or any response between CSO, XO, Sol, Fable, the Debate Room, or GitHub.** Agents must read the canonical file themselves, fetch cited sources, and publish their outputs to the repository through an issue/branch/PR as appropriate. If a room has read-only rules, its executor must use an existing execution lane; it must not hand the work back to the operator for transport.
>
> **Execution focus:** Decide P02 from the original evidence and return a source-grounded verdict. Do not debate how to organize another debate.

**Protocol ID:** NHRF-P02-ESCARPMENT-001  
**Prepared:** 2026-11-23  
**Scope:** P02 only; research verification and claim adjudication; no changes to the source dataset or published infographic.  
**Primary repository:** https://github.com/ianrhett/nhrf-research  
**Frozen research snapshot:** `4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`  
**Fleet-accessible mirror:** `ianrhett/nhrf` on branch `docs/p02-escarpment-debate-2026-11-23`, at `docs/research/NHRF-P02-ESCARPMENT-DEBATE-PROMPT.md`.

## Proposition requiring an evidence-based ruling

**Did Metro Nashville formally propose designating the Highland Rim Escarpment as a named, geographically bounded conservation area, or did its planning documents recommend preserving the escarpment primarily through general land-use policy and development restrictions?**

Determine (a) what Metro actually recommended, (b) what legal or planning tools already existed or were subsequently adopted, (c) what is unimplemented or unverified, and (d) what NHRF can accurately say in public.

**Do not assume that a policy label containing “Conservation” creates a legally protected conservation area. Do not assume that absence of a dedicated statutory designation means there were no protections.**

## Frozen baseline and materials

Current P02 description in the frozen dataset: **“Preserve the Highland Rim escarpment as a natural landscape.”**

- P02 assigned records: **15**.
- Consolidated source documents: **3**.
- Counted years: **1973–1992** (1992 adoption date provisional).
- Published implementation assessment: **Partly implemented**.
- Existing summary says Rural/Conservation policies and rural subdivision rules cover much of the Rim, but it has not been mapped or protected *by name*; it cites 2025 Council recognition and a not-started master plan. **These claims are to be verified, not adopted as conclusions.**

Canonical frozen files:

- [Statement-level data](https://github.com/ianrhett/nhrf-research/blob/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636/data/commitments.csv) — filter `promise_id == P02`.
- [Group descriptions and statuses](https://github.com/ianrhett/nhrf-research/blob/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636/data/recommendations.csv).
- [Grouping records](https://github.com/ianrhett/nhrf-research/blob/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636/data/promise_groups.csv).
- [Original-source inventory](https://github.com/ianrhett/nhrf-research/blob/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636/data/sources.csv).
- [Distinct policy group definitions](https://github.com/ianrhett/nhrf-research/blob/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636/data/distinct_promises.csv).

Fleet-accessible source-path equivalents under `ianrhett/nhrf` (on the P02 prompt branch):

| Canonical `nhrf-research` | Fleet `nhrf` |
|---|---|
| `data/commitments.csv` | `docs/research/commitments/commitments.csv` |
| `data/recommendations.csv` | `docs/research/commitments/recommendations.csv` |
| `data/promise_groups.csv` | `docs/research/commitments/promise_groups.csv` |
| `data/sources.csv` | `docs/research/commitments/sources.csv` |
| `data/distinct_promises.csv` | `docs/research/commitments/distinct_promises.csv` |
| `data/NHRF_Commitments.xlsx` | `docs/research/commitments/NHRF_Commitments.xlsx` |

The core files were previously verified byte-identical between the public frozen snapshot and the fleet baseline. Agents must check their current checkout/commit, not assume the two repositories always remain synchronized.

### 1. Natural Environmental Analysis (1973)

Original archive: https://www.nashvillehighlandrimforest.org/archive/PlanningCommissionNaturalEnvironmentalAnalysis1973.pdf

P02 dataset pages: **22, 106, 137, 139 (2 records), 140, 141, 144, 149, 151** (10 records).

Key passages to inspect against the original source:

- **PDF p. 22:** The Highland Rim region is described as worthy of consideration for strong conservation and preservation policies.
- **PDF p. 137:** Extensive urban development of the Highland Rim Escarpment is characterized as environmentally unsound/economically unfeasible; the area should remain generally natural.
- **PDF p. 149:** Significant hill sections should be identified and preservation mechanisms explored.
- **PDF p. 151:** Land regulations and equitable means of preserving hills are recommended.
- **PDF p. 139:** Low-density hillside/ridgetop development is discussed. Decide whether that supports P02 or another group, and distinguish a development-design recommendation from designation.

**Questions:** Does the report explicitly recommend creating a *named and mapped conservation designation*? Or does it argue for preservation policies and restrictions? Are some of these ten passages merely scientific description, general hill-conservation discussion, or repeated components of a single recommendation?

### 2. General Plan 1980–2000 (adopted 1981)

Original archive: https://www.nashvillehighlandrimforest.org/archive/GP1980-2000.pdf

P02 dataset pages: **260, 276, 279** (3 records).

- **PDF p. 260:** Most Rugged Topographic Areas were assigned the *Conservation-Nonurban (CN)* land-use policy; proposed uses were low intensity.
- **PDF p. 276:** Calls for careful review of development inconsistent with low-density or nonurban uses on the Rim.
- **PDF p. 279:** Explicit heading *Highland Rim Escarpment* and recommendation to preserve natural features through Conservation-Nonurban policies and restrictions on unsuitable development.

**Central issue:** Was CN a map-level conservation-oriented land-use policy already implemented in the plan, a legally protected conservation area, or both? Identify its exact legal effect, map boundary, enforceability, adoption status and exemptions. If it counts as a designation in any sense, say **what kind of designation**.

### 3. Concept 2010 General Plan (approximately 1992)

Original archive: https://www.nashvillehighlandrimforest.org/archive/Concept2010.pdf

P02 dataset page: **39** (1 record).

- Calls for conserving floodplains, hills and sensitive features through landscape/open-space management.
- Repository notes say the passage does **not** name the Highland Rim.
- Dataset adoption year is provisional. The copy is dated October 1991; later records suggest 1992. Verify if necessary and distinguish source-document date from adoption date.

**Question:** Does this general recommendation belong in a Rim-specific P02 count or in a wider conservation-policy group?

### 4. Subsequent implementation to verify

Retrieve the controlling original records and current historical status, including:

- NashvilleNext rural, Conservation and Natural policy maps.
- The rural subdivision standards adopted in 2016 and subsequent amendments.
- [RS2025-1549](https://nashville.legistar.com/) recognizing “Nashville’s Highland Rim Forest” (find the exact legislative record/text and avoid assuming this link is a direct bill page).
- Highland Rim Forests Conceptual Master Plan **24AD0001** in Metro CIB and any enacted appropriations, contracts, work orders or deliverables.
- Any legally established natural-area or conservation-area boundaries overlapping the escarpment; conservation easements; zoning or regulatory overlays; adopted greenways/parks; and any newer conservation strategy.
- Distinguish adoption, regulation, funding, implementation and measured ecological outcomes, with dates.

Do not conflate geographic recognition, CN planning policy, natural-area designation, conservation easement and legally enforceable development limitations.

## Questions to decide

### A — Historical recommendation

Did the 1973, 1981 or 1991/1992 documents **explicitly call for formal designation** of the Highland Rim Escarpment as a named conservation area?

Give the exact source wording, page and instrument called for. If none does, state the narrower recommendation they actually support.

### B — Correct P02 counting unit

For **all 15 existing P02 records**, distinguish:

1. Explicitly Rim-specific conservation recommendation.
2. General hill/forest or scenic-landscape conservation recommendation.
3. Development-density/design guidance.
4. Background description or implementation statement.
5. Duplicate or restatement of another substantive action.

Report **15 existing assigned records**, **N defensibly qualifying P02 records**, **N unique substantive actions** (if measurable), and **3 existing consolidated documents** or revised document count if assignments change. List rejected/reassigned records rather than silently deleting them.

### C — Implementation

Did Metro perform the action originally recommended? Separate:

1. Conservation-oriented planning designation.
2. Enforceable regulation or land-use restriction.
3. Formal named and mapped conservation-area designation.
4. Funding, execution, protection of actual acres, and measured outcomes.

If something was implemented only partly, identify what remains unfulfilled. If the original action does not specify formal designation, do **not** grade Metro as failing to implement a designation it never recommended.

### D — Publication wording

Assess the evidence for each proposed formulation:

A. “Metro repeatedly called for designating the Highland Rim Escarpment as a conservation area.”

B. “Metro repeatedly recommended protecting the Highland Rim Escarpment from intensive development.”

C. “Metro repeatedly recognized the conservation value of the Highland Rim and recommended its preservation through land-use policy.”

D. A more accurate alternative, with precise dates and qualifications.

Select only the wording defensible from original documents. Avoid rhetorical enhancement unsupported by the texts.

## Required outputs: answer the questions, not the workflow

Deliver a report with:

1. **Finding first:** a direct answer in one paragraph to whether *formal conservation-area designation* was actually recommended.
2. **15-row evidence ledger:** `record identifier | document | PDF page | original passage | relevance to Rim | policy mechanism | P02 count? | rationale`.
3. **Implementation matrix:** `original requirement | enacted/planned instrument | legal effect | dates | evidence | status | gap`.
4. **Adjudicated P02 counts:** original 15, accepted N, unique actions N or “not determinable”, distinct documents N.
5. **One publication-ready headline and two supporting sentences**, with exact source references and limitations.
6. **Unresolved list** identifying missing evidence and exactly what could settle it.

**Evidence standard:** inspect original pages, not only CSV excerpts. The existing dataset is the audit target, not independent proof. Distinguish direct quotations from interpretation. Use explicit “not verified” labels where original sources cannot be accessed.

**Debate scope:** challenge the substantive interpretation of the documents and the meaning of conservation designation. Do not spend turns debating orchestration, model seats, blind-review protocol, read-only limitations or cost policy. Factual source questions should be resolved by reading sources; unresolved interpretation can be debated.

**Repository behavior:** preserve original source data and the publication; prepare a report-only branch and PR for findings. If the room cannot write, the existing XO execution pathway must handle report publication directly. **Never make the operator the messenger.**

**Exit criterion:** a specific defensible P02 statement, supported by an itemized source-level record and an implementation finding. If the record does not support formal designation, say so explicitly.

**Begin with the 1973 PDF p. 137 and the 1981 General Plan PDF pp. 260 and 279.**
