# Shakedown pass 2: NashvilleNext Vol. IV actions by section

Source: NashvilleNext Vol. IV Actions (adopted June 22, 2015), Bunny copy, SHA-256 2057d0390ca72ef04e62beed618b671c53e3ba312722a2b57e949d7ccb098423 (matches MANIFEST). Action list from `data/nn_vol4_actions.csv` (377 action rows, all marked verified). Timeframes as defined on Vol. IV PDF p4: "Near term: Begin work within 1 to 3 years", "Mid term: Begin work within 4 to 7 years", "Long term: Begin work within 7 to 10 years." The action tables themselves print "Mid-term (4-6 years)" (for example PDF p72), so the source is internally inconsistent on the mid-term window.
Checked 2026-11-27 by SO nhrf (subagent). Review only; nothing public changes until the operator rules.

## How "forest-relevant" was chosen

An action counts as forest-relevant here if its `commitments_rows` points to a row in `data/recommendation_statements.csv` that carries a recommendation ID (P01 to P19). That is the data's own tagging, not a new judgment. 88 action rows have `commitments_rows`; 10 of those rows (9 distinct actions; action 323 appears under two policies) point to a P-tagged statement. The other 78 point to statements left untagged or marked context (energy, recycling, transit and similar). A short list of untagged NR 1 actions that bear on land and trees is given at the end for context, with a status only where this pass opened a primary source.

Status test (Method section of RECOMMENDATIONS-IMPLEMENTATION.md): Implemented = a binding rule, program or funding that does what was asked, in substance. Partly implemented = part of it, or a weaker form. No implementation reported = no record found either way, or no measure. Evidence is cited to the review file where it was checked.

## Section by section

### Natural Resources and Hazard Adaptation, NR 1.1 (protect the Cumberland and its tributaries)

| Action | Timeframe | Asked | Feeds | Status | Evidence |
|---|---|---|---|---|---|
| 210 (PDF p69) | Near term | "Strengthen hillside development regulations to minimize development on greater than 15% slopes." Implementer Metro Planning. | P01 | Partly implemented | BL2022-1121 (passed 2022-05-17) requires single and two-family subdivisions on 20% or greater slopes to use conservation development (17.28.030.A.2; MPC minutes 2022-04-28 PDF p18). The 15% threshold was not adopted for homes; rural subdivisions protect 15% slopes under the 2016 rules. See P01, P05. |

Section status: Partly implemented.

### Natural Resources and Hazard Adaptation, NR 1.2 (land, funding and staff for parks and natural infrastructure)

| Action | Timeframe | Asked | Feeds | Status | Evidence |
|---|---|---|---|---|---|
| 119 (PDF p71) | Long-term | Research how to identify ecologically valuable lands and recommend an in-lieu fee "where permanent protection cannot be accomplished to fund a land bank." Implementers Metro Parks, Metro Water Services, Land Trust for Tennessee. | P08 | No implementation reported | Legistar Web API titles since 2019: "land bank" 0 matters; "in lieu" 53 matters, none about land, trees or open space (all payments in lieu of taxes and similar). Plan to Play 2026 Update PDF p51 says acquisition is "reactive to specific opportunities." Not searched: Parks or Water Services research memos. See P08. |

Section status: No implementation reported for the tagged action. (Untagged action 221, regular parks master plan updates, is Implemented; see the context list.)

### Natural Resources and Hazard Adaptation, NR 1.3 (farmland and local food)

| Action | Timeframe | Asked | Feeds | Status | Evidence |
|---|---|---|---|---|---|
| 141 (PDF p71) | Mid-term | Assess best practices that preserve prime farmland "and create an agricultural zoning category for existing farms and prime farmland soils." Implementers Metro Planning, Land Trust for Tennessee. | P04 | No implementation reported | Legistar Web API titles since 2019: "agricultur" 24 matters (board appointments, grants, rezonings), "farmland" 0; no agricultural zoning district. Legislative archive 2015 to 2019 not searched. See P04. |

Section status: No implementation reported.

### Natural Resources and Hazard Adaptation, NR 1.4 (preserve and expand tree canopy, including larger tracts of forested land)

| Action | Timeframe | Asked | Feeds | Status | Evidence |
|---|---|---|---|---|---|
| 182 (PDF p72) | Mid-term | "Enact a conservation subdivision ordinance by right with a minimum of 50% open space requirement." | P05 | Partly implemented | BL2022-1121 conservation development: required (not by right) in R and RS zones on qualifying sites; keeps natural areas up to 20% of the site, or at least 20% where there are more. See P05. |
| 174 (PDF p72) | Mid-term | "Revise the existing cluster lot subdivision regulations to increase the amount of required preserved land to be 33% minimum." | P05 | Partly implemented | The old cluster lot option required 15% open space (MPC minutes 2022-04-28 PDF p12); BL2022-1121 replaced it with the 20% conservation development rule. Raised, but below 33%. See P05. |
| 201 (PDF p72) | Near term | Implement and update the Urban Forestry and Landscape Plan; create a street tree policy, residential tree ordinance, maintenance program and preservation policy; fund a replacement planting program; fund more inspectors. | P06 | Partly implemented | BL2022-1122 (2022) sets tree protection and replacement rules for development, including a frontage tree rule for new single and two-family lots (MPC minutes 2022-04-28 PDF p26); BL2021-972 and BL2026-1287 fund planting, including on private land. No preservation (retention) rule: BL2022-1409 withdrawn 2023. Whether the 2016 Urban Forestry and Landscape Plan was updated, and inspector staffing, were not checked. See P06, P07. |

Section status: Partly implemented.

### Natural Resources and Hazard Adaptation, NR 4.1 (climate threats to infrastructure; upstream land)

| Action | Timeframe | Asked | Feeds | Status | Evidence |
|---|---|---|---|---|---|
| 148 (PDF p78) | Mid-term | Collaborate with upstream counties and agencies on upstream land use, and contribute to joint regional efforts "with land conservation, source water protection, hazard reduction, and floodplain management practices." Implementers Cumberland Region Tomorrow, Nashville Area MPO, Cumberland River Compact and others. | P12 | No implementation reported | Legistar Web API titles since 2019 for "upstream": 0 matters. Metro is not a named implementer. P12 was outside this pass's 14 files; its row on file says the same. |

Section status: No implementation reported.

### Natural Resources and Hazard Adaptation, NR 4.2, and Built Environment, BE 1.1 (rural policy; same action listed twice)

| Action | Timeframe | Asked | Feeds | Status | Evidence |
|---|---|---|---|---|---|
| 323 (PDF p49 and p79) | Near term | "Update areas of Nashville/Davidson County as appropriate to new Rural Conservation, Rural Agriculture, and Rural Countryside Community Character Manual Policies that guide a reduction in development and discourage the expansion of sewer infrastructure." Implementers Metro Planning, Metro Water Services. | P03 | Implemented (as a policy-mapping step) | MPC minutes 2016-05-26: Rural Countryside (T2 RCS) and Rural Maintenance (T2 RM) described as new categories adopted with NashvilleNext (PDF p6 to p7); RS2016-142 approved the deferred Whites Creek area policies, 2015CP-000-002 (PDF p10). The action asks only to apply the policies; it does that. Their effect on sewer extensions is partial (see P03): the policies "are not regulatory" and Metro Water's published guides do not mention them. |

Section status: Implemented for the mapping step; the outcome it aims at is Partly implemented (P03, P04).

### Health, Livability and the Built Environment, BE 2.2 (health quality of air, water and land)

| Action | Timeframe | Asked | Feeds | Status | Evidence |
|---|---|---|---|---|---|
| 74 (PDF p51) | Ongoing | "Encourage additional conservation land easements by owners of private property." Implementers private sector, Land Trust for Tennessee, other land conservation groups. | P11 | Partly implemented | NashvilleNext 2016 Annual Report PDF p32: The Land Trust for Tennessee "protected 445 acres in the Beaman to Bells Bend Corridor with conservation easements." BL2017-725 created a Conservation Assistance Grant Fund; no award found in Legistar since 2019. The FY2027 Highland Rim easement project (27DS0031) is listed in the CIB but not in the FY2027 Capital Spending Plan. See P11, P08. |

Section status: Partly implemented.

## Which recommendations each section feeds

| Section | P-IDs fed by tagged Vol. IV actions |
|---|---|
| NR 1.1 | P01 |
| NR 1.2 | P08 |
| NR 1.3 | P04 |
| NR 1.4 | P05 (two actions), P06 |
| NR 4.1 | P12 |
| NR 4.2 / BE 1.1 | P03 |
| BE 2.2 | P11 |

No tagged Vol. IV action feeds P02, P07, P09, P10, P13 to P19. Those recommendations draw their NashvilleNext statements from Vols. I to III or from other plans.

## Context: untagged NR 1 actions on land and trees

Listed so the operator can decide whether the tagging should widen. Status is given only where this pass opened a primary source; otherwise "not assessed".

| Action | Asked (short) | Status | Evidence |
|---|---|---|---|
| 199 (NR 1.4, Near term, PDF p72) | Fund and staff a tree planting and maintenance program to meet the canopy goal | Partly implemented | Funded program: BL2021-972, sunset removed by BL2026-1287 (P07). Goal not met: "Nine of the fourteen community planning areas do not meet their canopy goals" (UTC Assessment 2023 PDF p27). |
| 221 (NR 1.2, Near term, PDF p70) | Update the Parks and Greenways Master Plan regularly | Implemented | Plan to Play 2017 and Plan to Play 2026 Update (both in MANIFEST). |
| 224 (NR 1.2 and BE 2.1, Near term, PDF p70 and p51) | Fund the Open Space Acquisition Fund with at least $5 million plus 20% private match | No implementation reported for the named fund | Plan to Play 2026 Update PDF p95: land acquisition allocations $12.8 million FY18 to FY25, $0 in FY24 and FY25; FY2027 Capital Spending Plan (RS2026-2305 Exhibit A) has no land acquisition line. Overlaps P10, which was outside this pass. |
| 228 (NR 1.1, Near term, PDF p69) | Variable stream buffer program on impaired waterways, Mill Creek pilot | No implementation reported | Legistar titles since 2019: no Mill Creek overlay or buffer ordinance (P15). Implementer is the Cumberland River Compact (advocacy). |
| 373 (NR 1.1 and LUTI 3, Near term, PDF p69 and p7) | Process to review old, undeveloped PUDs and SPs that affect sensitive features | Not assessed | One instance seen: BL2021-954 preamble records the Planning Commission found The Cove at Whites Creek SP inactive on June 24, 2021, and Council rezoned it to AR2a (P04). Whether a standing process exists was not checked. |
| 150, 151, 155, 159, 220, 222, 225, 236 | Funding strategies, regional plan, advocacy, watershed coordination, infrastructure and maintenance funding, dumping, buffer repair | Not assessed | Outside the forest tagging and not opened in this pass. |

## Summary for the operator

Of the nine P-tagged Vol. IV actions, one is Implemented as written (323, applying the new rural policies), five are Partly implemented (210, 182, 174, 201, 74) and three have No implementation reported (119, 141, 148). By section: NR 1.1, NR 1.4 and BE 2.2 are Partly implemented; NR 1.2, NR 1.3 and NR 4.1 have No implementation reported for their tagged actions; NR 4.2 / BE 1.1 is Implemented as a mapping step with a partial outcome. Everything rests on the review files P01 to P18 in this folder and the searches named above; Legistar searches cover 2019 onward only.
