# Adversarial fact-check: Recommended 216 Times (v1.7.1)

**Prepared:** 2026-11-20  
**Reviewer:** ChatGPT / independent adversarial review  
**Disposition:** Debate and adjudication requested; not an approved correction or replacement for the publication.  
**Audited snapshot:** [4b67bb8f72a5b39a6b146b85a5d2893aa23fa636](https://github.com/ianrhett/nhrf-research/tree/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636)  
**Artifact:** [NHRF_Recommended_216_Times_v1.7.1.pdf](https://github.com/ianrhett/nhrf-research/blob/4b67bb8f72a5b39a6b146b85a5d2893aa23fa636/one-pager/NHRF_Recommended_216_Times_v1.7.1.pdf)

## 1. Executive summary

The headline arithmetic is reproducible. Independent filtering of the published CSV data reproduces 216 coded records, 19 groups, 13 contributing documents, 340 forest-related recommendation-type records, 15 contributing documents, 32 counted documents, and 1 implemented / 15 partly implemented / 3 no implementation reported classifications.

That is a successful data reconciliation, not a certification of the correctness of the extraction, grouping, or implementation judgments. The most important issues are the distinction between a coded record and an independent recommendation; two singleton groups described as recurring; some questionable group assignments; conflation of source files and documents in the recommendations table; and categorical implementation notes that omit existing mechanisms or exceptions.

**Recommendation:** Do not discard the research. Resolve the findings through evidence-based adjudication before publication. The central conservation implementation gap may remain supported even if some counts or wording change. Do not assume every challenge below is correct: the report deliberately invites rebuttal.

### Evidence levels

- **Reproduced:** independently calculated from repository CSVs; not an independent validation of primary-source extraction.
- **Confirmed wording discrepancy:** a primary source contradicts the literal or unqualified wording; a narrower intended meaning may still be valid.
- **Classification dispute:** excerpt and assignment inspected in the repository; original page/context and inclusion criteria must be adjudicated.
- **Open verification:** insufficient evidence to establish the positive or negative claim. No inference of nonexistence from missing evidence.

## 2. Reconciliation of published figures

| Claim | Recalculation | Result |
|---|---:|---|
| All extracted rows (not shown as headline) | 1,557 | Context |
| Counted extracted rows | 1,272 | Match |
| Counted source files | 49 | Context |
| Counted consolidated documents | 32 | Match |
| Forest-related recommendation-type records | 340 | Match |
| Documents containing those records | 15 | Match |
| Records tagged P01–P19 | 216 | Match |
| Consolidated documents containing P01–P19 | 13 | Match |
| Distinct groups | 19 | Match |
| Implemented | 1 | Classification tally matches |
| Partly implemented | 15 | Classification tally matches |
| No implementation reported | 3 | Classification tally matches |
| Date span | 1973–2026 (53 years elapsed) | Match |

The source table contains 63 rows explicitly marked counted yes/no (49 yes and 14 no). Consolidating NashvilleNext and the 2026 Plan to Play files yields 45 document identifiers across the included/excluded source set; 32 are included. The included set includes legislation, code and other evidence, not exclusively plans. Thus “32 qualifying documents counted” is more accurate than “32 documents reviewed.”

Repository evidence: [commitments.csv](../../data/commitments.csv), [sources.csv](../../data/sources.csv), [promise_groups.csv](../../data/promise_groups.csv), [recommendations.csv](../../data/recommendations.csv), [count_funnel.py](../../scripts/count_funnel.py), [funnel.json](../../scripts/funnel.json).

## 3. Findings ledger

### F01 — Counting unit and duplicated action (high significance; reproduced)

The 216 records are 137 recommendation, 43 commitment, 35 target and 1 funding_estimate rows. The broader 340-record population includes 192 recommendations, 67 commitments, 80 targets and 1 funding estimate. The published methodology intentionally includes all four types, but the headline can be read as 216 separate recommendation events.

Examples (page numbers are the repository's PDF-page identifiers):
- NashvilleNext Vol IV, pp. 49 and 79, action #323: identical language discouraging sewer infrastructure expansion appears under two headings; both occurrences are counted under P03. Counting published occurrences is defensible; counting distinct actions requires deduplication.
- Open Space Plan 2011, p. 11, P09: one sentence contains an initial 3,000-acre target and an additional 3,000-acre target by 2035. Two targets are defensible as records, not two distinct textual recommendation occurrences.
- Plan to Play 2017, p. 234, P09: a regional park land market-value estimate of $210,905,799 is a funding estimate, not independently an imperative.

**Proposed resolution:** define the unit as coded statement/target records, disclose repeated identical action text, explain why estimates count, and publish sensitivity totals for unique actions or unique source passages if those units are relevant. Retain 216 only if the chosen inclusion rule is justified and disputed assignments are resolved. Do not subtract examples mechanically without agreeing on the unit.

### F02 — Two singleton groups (confirmed count; framing dispute)

P10 (Open Space Fund, 2011 p. 31) and P12 (regional upstream conservation, NashvilleNext Vol IV p. 78) each have one counted record. Seventeen groups have more than one record (214 records combined). The phrase “same 19 recommendations” implies recurrence for all 19, although a collection of 19 groups can be described as containing repeated recommendations overall.

**Proposed resolution:** say “216 records grouped into 19 conservation recommendations, 17 of which appear more than once” or use equivalent precise language. Review recurrence at the consolidated-document level separately.

### F03 — Agricultural zoning (confirmed wording discrepancy)

P04: “Rural subdivision rules only; no farm zoning.”

Metro lists AG (5-acre minimum) and AR2a (2-acre minimum) as agricultural zones. The research evidence makes a narrower assertion: NashvilleNext recommended an additional agricultural zoning category intended to protect prime farmland, and the additional mechanism was not created.

Primary source: [Metro Planning zoning classifications](https://www.nashville.gov/departments/planning/land-development/rezone-my-property/zoning-classifications). Repository locators: NashvilleNext Vol IV p. 71 (action #141); recommendations.csv P04.

**Proposed wording:** “Rural subdivision rules; recommended new farmland zoning not enacted.” Verify the latter assertion against action #141 and zoning amendments. Existing AG/AR2a alone does not prove that action was implemented.

### F04 — Tree retention (confirmed wording discrepancy)

P06: “Nothing requires keeping existing trees.” P17: “Replacement meets the rule; retention not required.”

[BL2022-1122](https://nashville.legistar.com/LegislationDetail.aspx?FullText=1&GUID=AD288FCD-84FF-4A53-943F-381420C13F08&ID=5464029) passed May 17, 2022. It provides removal restrictions and findings for designated historic/specimen trees, design expectations for minimizing removals, and permit criteria for retained, protected and heritage trees. Replacement is allowed in specified circumstances, and designated historic/specimen trees are a voluntary designation program. These caveats matter: the ordinance is not a universal retention mandate, but the unqualified negative is too broad.

**Proposed wording:** “Removal restrictions apply; no general canopy-retention mandate.” P17 should distinguish design/minimization requirements from a universal mandate to retain trees. Review current consolidated code and scope/exemptions before final wording. Partly implemented may remain appropriate.

### F05 — Acquisition mechanism (confirmed wording discrepancy)

P08: “No acquisition program; $7M easement line not appropriated.”

Metro's [Conservation Assistance Fund](https://www.nashville.gov/departments/parks/greenways-and-open-space/metro-conservation-assistance-fund) accepts applications for targeted acquisition and protective easement projects through conservation NGO partnerships. This establishes a mechanism, not proof of awarded grants, adequacy, or a systematic dedicated Rim land acquisition program.

The [July 24, 2026 Beaman Park announcement](https://training.nashville.gov/departments/mayor/news/mayor-freddie-oconnell-announces-acquisition-300-acres-beaman-park) describes approximately 300 acres acquired by a conservation partner pending transfer to Metro. The repository cites a September transfer request of approximately 298.20 acres. A prior audit also identified an appropriation and a November purchase-option resolution as leads; these should be traced to exact records before being relied on. A partner acquisition, announced transfer, appropriated funding, and completed Metro ownership are different events.

**Proposed wording:** “Acquisitions occur; no dedicated Rim acquisition program identified.” Define how a dedicated program differs from the existing fund and confirm grant history and deed/closing status. See F09 for capital spending.

### F06 — Invasive species and site management (confirmed existence; scope dispute)

P15: “Stream buffers only; no glade or invasives plan.” P13: “Designation policy 2026; no site plans yet.”

[May 7, 2013 Parks Board minutes](https://www.nashville.gov/sites/default/files/2021-11/PARKS-130507m.pdf), pp. 3 onward, contain a Hill Forest State Natural Area Management Plan presented to the Board. The plan addresses invasive plant identification and resource management (including pp. 8–9). This is a documented site-level plan, not proof of countywide invasive management or an adopted plan under the 2026 designation policy. The minutes also specify management authority and a conservation easement held by the Land Trust of Tennessee (p. 4).

**Proposed wording:** “Stream buffers and site-level habitat planning; broader protections incomplete.” For P13, “2026 designation policy; new site plans not yet verified.” Check whether the older plan was adopted and implemented, and distinguish Metro-wide requirements from individual site plans.

### F07 — Per-group document counts (confirmed inconsistency)

The aggregate method collapses NashvilleNext components and the 2026 Plan to Play update/appendix into consolidated documents. The individual recommendations table does not consistently do so.

| ID | Group | Records | Published CSV documents | Recalculated consolidated documents |
|---|---|---:|---:|---:|
| P01 | Steep slopes | 29 | 13 | 5 |
| P02 | Rim escarpment | 15 | 3 | 3 |
| P03 | Sewer expansion | 15 | 8 | 5 |
| P04 | Rural character | 12 | 7 | 5 |
| P05 | Conservation subdivisions | 15 | 8 | 5 |
| P06 | Tree protection | 9 | 7 | 5 |
| P07 | Tree canopy | 22 | 8 | 6 |
| P08 | Land acquisition | 16 | 7 | 7 |
| P09 | Acreage goals | 19 | 5 | 4 |
| P10 | Open Space Fund | 1 | 1 | 1 |
| P11 | Easements/TDR | 9 | 5 | 3 |
| P12 | Regional conservation | 1 | 1 | 1 |
| P13 | Natural areas | 9 | 3 | 3 |
| P14 | Urban forestry | 9 | 6 | 6 |
| P15 | Rare habitats | 8 | 6 | 6 |
| P16 | Scenic corridors | 5 | 2 | 2 |
| P17 | Site design | 8 | 4 | 2 |
| P18 | Connected areas | 7 | 6 | 4 |
| P19 | Broad goals | 7 | 5 | 3 |

Eleven of 19 differ. P01 even has only 12 unique component-file identifiers in the 216-record subset, rather than 13. Note also that the timeline builder uses each file's date while the funnel assigns the earliest counted component date to a consolidated document. These may be intentional separate time concepts, but the distinction should be documented, especially for amended NashvilleNext components.

**Proposed resolution:** generate the per-group document counts and date fields from one agreed filter, identify component-file counts separately, and validate the dates used for the chart. No displayed row count of 216 changes solely as a result of document consolidation.

### F08 — Group assignment challenges (classification disputes, not established errors)

| Source | PDF page | Group | Challenge |
|---|---:|---|---|
| General Plan adopted 1981 | 89 | P03 | The excerpt advocates partly financing sewer extensions through beneficiaries rather than opposing extensions. |
| Natural Environmental Analysis 1973 | 98 | P03 | Soil-data planning for developments reliant on on-site sewage disposal is not directly a recommendation against public sewer extensions. |
| NashvilleNext Rural CCM | 9 | P01 | Sensitive watershed design is called for, but the excerpt does not directly require avoiding construction on steep slopes. |
| Plan to Play 2017 | 177 | P13 | Park site selection to preserve natural or cultural resources is not necessarily management of existing natural areas. |

All four are relevant conservation-related passages. Their assignment may be defensible under a sufficiently broad thematic rule or fuller page context. Forty-nine tagged records fall outside the six named forest categories and enter the forest subset via their P01–P19 tags; this is intentional in the code, but makes those assignments especially important to document. The count is not independently corrected here.

**Proposed resolution:** reviewers should inspect the exact primary-source pages, record an explicit rationale for inclusion, reassignment or exclusion, and regenerate all outputs only after adjudication.

### F09 — Capital budget vs. appropriation (confirmed distinction; project-specific checks open)

P02: “master plan budgeted 2024, not started.” P08: “$7M easement line not appropriated.”

The repository identifies CIB project 24AD0001 (Highland Rim Forests Conceptual Master Plan, $500,000) and 27DS0031 (Highland Rim Conservation Easement Support, $7 million, adopted FY2027 CIB p. III-91). [Metro Finance](https://www.nashville.gov/departments/finance/management-and-budget/capital-budget-and-planning) explicitly distinguishes CIB inclusion from appropriation. The [FY2027 CIB](../../sources/FY27_CIB_Adopted.pdf) is in this repository. The builder says 27DS0031 was excluded from the FY2027 spending plan adopted November 5, 2026. [RS2026-2305](https://nashville.csv.legistar.com/LegislationDetail.aspx?GUID=05E96801-CF50-4099-A6E6-1E33DD44A763&ID=8256471&Options=&Search=) confirms passage November 5 and mayoral approval November 6. Its final amended exhibits have not been fully reconciled in this audit; the absence of project funding is not independently certified.

**Proposed wording:** “Master plan listed in CIB since 2024; status listed as not started [as of date].” Verify both project entries, status fields and final spending exhibits, and distinguish authorization, appropriation, encumbrance and expenditure.

### F10 — Canopy assessment measurement date (confirmed)

P07: “Rural canopy held; no rule protects forest tracts.”

The [2023 Urban Tree Canopy Assessment](https://www.nashville.gov/sites/default/files/2024-03/UTC_Assessment-Final_Report-2023.pdf) uses imagery through 2021, comparing 2010, 2016 and 2021. See also [Metro's assessment overview](https://www.nashville.gov/departments/water/stormwater/tree-information/urban-tree-canopy). The 2026 tree funding ordinance acknowledges storm-related canopy damage. The earlier audit's finding about rural canopy is historical, not a measurement as of November 2026. Also distinguish Metro Nashville, Davidson County and rural transects when quoting acreage.

**Proposed wording:** “Rural canopy held through 2021; tract protections incomplete.” Confirm the precise rural metric, period, geographic definition and applicable protections.

## 4. All 19 implementation notes

The record counts below are reproduced. This table evaluates wording and indicates outstanding checks; it does not automatically change implementation classifications.

| ID | Count | Published classification | Assessment / next check |
|---|---:|---|---|
| P01 | 29 | Partial | Qualify 15% rural subdivision and 20% residential grading standards; verify exemptions including lot size. |
| P02 | 15 | Partial | Clarify nonregulatory policy, CIB listing and status; check F09. |
| P03 | 15 | Partial | Obtain Metro Water sewer-extension criteria, Council acceptance records and Best Brands documentation; resolve F08. Alliance report is not independent confirmation. |
| P04 | 12 | Partial | Correct implication that agricultural zoning does not exist; F03. |
| P05 | 15 | Partial | Distinguish 50% proposal from enacted 20% standard, qualifying zones, triggers, exemptions and natural-area conditions. Do not score 20/50 as percentage implemented. |
| P06 | 9 | Partial | Acknowledge existing removal restrictions; F04. |
| P07 | 22 | Partial | Date rural canopy finding; F10. Verify tract-protection claim. |
| P08 | 16 | Partial | Acknowledge fund and acquisition activity; distinguish dedicated program, appropriations and completed transfers; F05/F09. |
| P09 | 19 | Partial | 4,541 acres is projected additional parkland need, not specifically forest acreage. Verify year, denominator and final delivery. |
| P10 | 1 | No report | Narrow negative: documented search covered specified available capital spending plans and 2026 appendix, not all financial records since 2011. |
| P11 | 9 | Partial | “Easements once” requires a comprehensive deed/easement inventory and definition of Metro vs third-party holders; check grants and TDR rules. |
| P12 | 1 | No report | Review regional partner implementation; NashvilleNext identifies regional partners. No evidence found is not proof no cooperation occurred. |
| P13 | 9 | Partial | 2026 policy is real progress; distinguish new program plans from existing site-level plans; F06. |
| P14 | 9 | Implemented | Urban forestry and funding mechanism supported; check actual annual funding, staffing and assessment cadence if full implementation requires these. |
| P15 | 8 | Partial | Existing site-level invasive species planning contradicts broad wording; F06. |
| P16 | 5 | Partial | Provisionally supported by repository evidence; check scenic road designations, easements and ridgeline-specific controls. |
| P17 | 8 | Partial | Distinguish design standards and retention exceptions from replacement density; F04. |
| P18 | 7 | Partial | Define intended mapped integrated Rim network as distinct from existing parks/greenways. |
| P19 | 7 | No report | Broad goals lack a common measurable target; consider whether unscorable is more precise than an implementation finding. |

P09 detail: Plan to Play 2017 p. 27 reports 4,541 additional acres; 2026 appendix p. 478 and update p. 12 report 568.78 acres acquired since 2017. The appendix figure has a pending verification annotation in promised_vs_delivered.csv pair 1. The 2026 update restates need as 4,540, the appendix as 4,500+. The 2017 baseline is also restated (pair 4; 15,873 vs 15,088). Do not equate acquisition with closure of the level-of-service gap without reconciling definitions and baselines; do not treat a 2026 target as overdue before its applicable deadline. A pending Beaman transfer cannot be added as completed acreage.

## 5. Additional source checks

- P14: [BL2026-1287](https://nashville.legistar.com/LegislationDetail.aspx?FullText=1&GUID=A7EB196D-EAA2-4B62-99DD-FEA9758279DD&ID=7876369) passed March 17, 2026, with mayoral approval March 20. Review the enacted text for removal of the sunset and the $2.5 million annual ceiling; a funding ceiling is not guaranteed annual expenditure.
- P13: [Metro Parks policy manual, October 2026](https://www.nashville.gov/sites/default/files/2026-10/Metro-Board-of-Parks-Policy-Manual-OCTOBER-2026.pdf?ct=1791477105), policy 3000.45, approved August 4, sets a designation process and protections for qualifying natural areas. Verify actual designation decisions and site management plan status.
- Campaign quotation: the previous audit located the passage on [15 Fixes](https://www.readyforfreddie.com/15-fixes), in the Taking Plans to Reality section, and noted a community safety plan exception. Reopen and archive the campaign source and full surrounding passage for final citation, rather than relying on an ellipsis or this review alone.

## 6. Repository reproducibility and provenance

| Item | Finding / suggested resolution |
|---|---|
| Default execution path | count_funnel.py defaults to a path in the originating repository. Supply the workbook explicitly or correct the default. |
| Divergent exclusions | Chart builder's grouped-record filter and count_funnel.py differ on Subdivision_Regulations_Chapter_4_2024; presently both yield 216, but share a canonical filter to prevent drift. |
| Hard-coded notes | LBL in build_one_pager.py contains abbreviated claims independent of evidence text. Establish reviewed source text or explicit cross-check. |
| Version metadata | data/VERSION remains 1.6.0 dated Oct 24; recommendations include November evidence, and v1.7.1 builder cites Nov 8 updates. Establish exact workbook/CSV/PDF provenance and label releases accordingly. |
| Supporting evidence | FACTS.md and RECOMMENDATIONS-IMPLEMENTATION.md are referenced but absent from the audited public tree. Supply public supporting references or replace with accessible evidence locators. |
| Verification flags | 146 verified, 69 verified_ocr, 1 verified_by_hand among the 216. These are existing research flags, not independent reviewer authentication. |
| Completeness | Excluded sources and post-snapshot evidence may matter to implementation even if they do not enter the recommendation denominator. State inclusion rationale and the search cutoff. |

### Independent CSV reproduction

Run from the repository root, using Python 3 standard library. This reproduces the filtering/counting logic without reading the cached totals; it is not a replacement for the workbook script or semantic review.

```python
import csv
from collections import Counter
from pathlib import Path
import re

def load(name):
    with (Path("data") / (name + ".csv")).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def document(d):
    if d.startswith("NashvilleNext_"):
        return "NashvilleNext"
    if d.startswith("Plan_to_Play_2026"):
        return "Plan_to_Play_2026"
    return d

def tag(r):
    return bool(re.fullmatch(r"P(0[1-9]|1[0-9])", r["promise_id"]))

sources = load("sources")
rows = load("commitments")
yes = {r["doc"] for r in sources if r["counted"] == "yes"}
exclude = {
    "Ordinance_BL2021-829", "Executive_Order_041A_2024",
    "Metro_Code_17.28.030", "Metro_Code_17.28.065",
    "Metro_Code_17.40.440", "Ordinance_BL2017-725",
    "Subdivision_Regulations_Chapter_4_2024",
    "Resolution_RS2025-1549", "Resolution_RS2025-1556"
}
types = {"recommendation", "commitment", "target", "funding_estimate"}
forest = {"forest_protection", "tree_canopy", "highland_rim_named_place",
          "habitat_natural_area", "land_acquisition", "open_space"}
counted = [r for r in rows if r["doc"] in yes]
f = [r for r in counted if r["doc"] not in exclude
     and r["item_type"] in types and (r["category"] in forest or tag(r))]
t = [r for r in f if tag(r)]
print(len(rows), len(counted), len(yes), len({document(d) for d in yes}))
print(len(f), len({document(r["doc"]) for r in f}))
print(len(t), len({document(r["doc"]) for r in t}))
print(Counter(r["item_type"] for r in t))
print(Counter(r["verify"] for r in t))
for p in sorted({r["promise_id"] for r in t}):
    subset = [r for r in t if r["promise_id"] == p]
    print(p, len(subset), len({document(r["doc"]) for r in subset}))
print(Counter(r["status"] for r in load("recommendations")))
```

The original audit used an independent JavaScript CSV parser and cross-checked the separate promise_groups.csv filter; the above is a portable Python equivalent provided for reviewers, not a claim that this exact snippet was executed. The original workbook script can be run as `python3 scripts/count_funnel.py data/NHRF_Commitments.xlsx` with pandas and openpyxl installed.

## 7. Candidate publication language (not adopted)

If adjudication preserves the existing totals and classifications:

**216 statements. 53 years.**

Between 1973 and 2026, Metro Nashville's official documents repeatedly called for conservation measures relevant to the forest that surrounds the city. Our research groups 216 recommendation-related records in 13 documents into 19 conservation recommendations. Only one is classified as fully implemented; 15 are partly implemented and three have no implementation reported in this review.

Of 32 qualifying consolidated documents, 15 contain forest-related recommendations. The 216 records include recommendations, commitments, targets and a funding estimate; repeated appearances within a document count under the research method.

**Bind it. Fund it. Report it.** Adopt enforceable conservation protections, establish funded acreage targets and publish annual progress reports.

The wording remains conditional: a narrower counting unit or changed group assignments may alter the figures. The original headline may be defensible under a disclosed occurrence-based counting method, but the ambiguity should be resolved deliberately.

## 8. Debate-room adjudication protocol

The goal is to establish the strongest defensible claims, not defend either the Alliance's publication or this reviewer by default.

For each F01–F10 and each open P01–P19 implementation item, reviewers should record: finding ID, challenged text, source document/version/page or ordinance section, verbatim supporting passage, counterevidence, applicable geographic and temporal scope, verdict (accept / reject / qualify / unresolved), rationale, specific proposed edit, effect on row counts and status, owner, and verification date.

Key questions:
1. What is the counting unit? Distinct source occurrences, coded commitments/targets, independent policy actions, or documents? Can a repeat within one plan count? Can a cost estimate count?
2. What is the semantic threshold for grouping a record under a specific recommendation, and are singleton groups described accurately?
3. What is the minimum evidence for fully implemented, partly implemented, no implementation reported, and possibly unscorable? Use the same thresholds for positive and negative findings.
4. Do site-level plans, limited tree ordinances, grant mechanisms, existing zones and third-party acquisitions satisfy the original recommendation, or only constitute partial progress? Identify explicit scope rather than treating examples as full implementation.
5. What would falsify every categorical absence claim? Which agencies, records, dates and policies have been checked?
6. Which source/version and dates govern all calculations? Are all "counted" and "reviewed" denominators used consistently?

Acceptance criteria for a corrected release:
- All findings have recorded dispositions with primary-source evidence where needed.
- Exact counted unit and grouping rules are documented; duplicates, targets and estimates are either justified or excluded consistently.
- All published counts regenerate from approved data; file/document/date distinctions are explicit.
- Each status has documented scope and evidence, and nonexistence claims are appropriately qualified.
- Source URLs/page locators and versions are preserved; publication is regenerated from the approved snapshot and independently checked.
- No correction is silently made to the source corpus. Preserve a correction ledger, prior release and approved changes.

## 9. Limits and report status

This is the write-up of the prior adversarial audit, with selected primary-source links rechecked on November 20. It reconciles the CSVs and inspects representative records; it does not individually authenticate all 216 original PDF excerpts, run a comprehensive legal and financial records search, recalculate a final count after semantic adjudication, or independently certify every implementation assessment. Some primary-source leads from the prior audit are explicitly retained as open rather than asserted as verified. The proposed wording and proposed adjudication criteria are reviewer recommendations, not decisions by the Alliance. No workbook, CSV, code, infographic or methodology changes are proposed in this report-only commit.

**Disposition: arithmetic passes; individual document counts need correction; classification and implementation claims require adjudication before publication.**
