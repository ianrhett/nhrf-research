# Workbook changelog

Each release is a dated copy in `versions/`. Newest first.

## v1.6.0 (2026-10-24)

Applies the accepted findings of the 2026-10-24 external review of v1.5.1 (Sol; findings and notes in `reviews/2026-10-24-sol/`, triage https://github.com/ianrhett/nhrf/issues/2#issuecomment-6392551464). Built by `artifacts/sol-review-2026-10-24/apply_workbook_v160.py` from the v1.5.1 file.

- SOL-001, SOL-003, SOL-029, SOL-055: pair 2 no longer reads $12.8M against $534M as percent funded. $534,362,411 is labeled estimated market value; pct_delivered removed; assessment Not yet due (horizon 2027). 2.4% appears only as Metro allocations divided by estimated market value; the printed 2.2% is labeled source-reported and unverified. 568.78 acres and $12.8M marked Verify, pending Plan to Play 2026 Appendix pages A-474 to A-478. Pair 1 is Not yet due (deadline 2026).
- SOL-002: notes on Commitments rows 767, 1492, 912 and 921: Metro planning documents have recognized the Rim since at least 1973; the 1980-2000 General Plan was adopted in 1981.
- SOL-004 to SOL-010: NashvilleNext Vol IV timeframes are windows to begin work (Vol IV p4), not completion deadlines. Pairs 21 to 26 show start windows in due; pairs 21 and 25 change from Not met to No status reported; pair 22 is assessed on the tool enacted, not lateness. Forest_Priorities gains start_window_passed for the 23 NashvilleNext timeframe rows; due_passed now covers stated years before 2026 only.
- SOL-011 to SOL-013: Beaman evidence brought forward in pairs 1, 5 and 18 and Commitments notes: about 300 acres announced July 24, 2026; transfer of approximately 298.20 acres requested September 1, 2026; pending closing. 568.78 + 298.20 = 866.98 (not 878). 309 marked as the superseded June estimate. Pair 5 pct_delivered removed (projection, not delivery).
- SOL-014: pair 15 updated with Park Board Policy 3000.45 (approved August 4, 2026): Partly met; designations and management plans still to come.
- SOL-015 to SOL-018, SOL-020: pairs 14, 16, 17 and 27 downgraded to Not verified; pair 26 notes its regional implementers; pair 27 labeled a draft recommendation.
- SOL-019: pair 22 pct_delivered removed; 50% requested and 20% enacted described as separate standards.
- SOL-021 to SOL-023: About splits counted-document totals (647 promises; 296 Forest-related; of the 647, 605 actions, 22 estimates, 20 allocations) from all-extracted totals (850; 393). Counted documents corrected from 45 to 48.
- SOL-024: Commitments 221 to 223 reclassified from target to baseline (modeled potential).
- SOL-027: Commitments 1515 reclassified from commitment to conditional_policy.
- SOL-028: Commitments 706 moved from P10 to context; P10 times 2 to 1. Core 12 now 164 times; all 19 now 217 times.
- SOL-030: Inconsistencies for Commitments 399 and 587 relabeled BASELINE CHANGE.
- SOL-031: Concept 2010 adoption year kept provisional (Sources note).
- SOL-032 to SOL-034: Sources rows added for the 2002 Parks and Greenways Master Plan, its 2008 update and Policy 3000.45, pending extraction and excluded from counts.
- SOL-025, SOL-026: notes on Commitments 239, 452 and 453: transcription to be corrected from source.
- SOL-035 to SOL-054: content not changed; a Sources repo_copy_note says each source needs a copy stored in the repo.
- Also: RS2025-1549 (forest recognition, passed 2025-10-10) and RS2025-1556 (Beaman grant application, about 308 acres, passed 2025-10-21) confirmed as two different resolutions from Legistar matters 19659 and 19714; notes on Commitments 1359 and 1549.

`versions/NHRF_Commitments_v1.6.0_2026-10-24.xlsx`. Documents listed: 57 (48 counted, 6 background, 3 pending extraction), Extracted rows (all kinds): 1557, Promises, counted documents: 647, Forest-related promises, counted documents: 296, Promises, all extracted documents: 850, Forest-related promises, all extracted documents: 393, Stated facts (baseline): 303, Progress claims (status_claim): 227, Definitions: 176, Promises scored on Forest_Priorities: 457, of which score 5: 170, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 72 (2 baseline changes), Highland Rim and named-place rows: 126, Public comments naming the Highland Rim: 30.

## v1.5.1 (2026-10-24)

Wording: RS2025-1549 recognizes the Forest as "Nashville's Highland Rim Forest" (recognition only), not "names" it.

`versions/NHRF_Commitments_v1.5.1_2026-10-24.xlsx`. Documents: 54, Extracted rows (all kinds): 1557, Promises (all topics): 854, Promises in Forest-related categories: 397, Stated facts (baseline): 300, Progress claims (status_claim): 227, Definitions: 176, Promises scored on Forest_Priorities: 461, of which score 5 (protect existing forest): 171, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 72, Highland Rim and named-place rows: 126, Public comments naming the Highland Rim: 30.

## v1.5 (2026-10-24)

Researches all 19 distinct forest recommendations (the 229 Forest action statements, grouped; P13-P19 added) against ordinances, code, Planning Commission and Park Board actions, budgets and Metro reports: 1 implemented, 15 partly, 3 no implementation reported; core 12 none fully implemented. New Recommendations tab and RECOMMENDATIONS-IMPLEMENTATION.md. Canopy evidence corrected (net gain 2010-2021; loss 2016-2021 in the urban district only).

`versions/NHRF_Commitments_v1.5_2026-10-24.xlsx`. Documents: 54, Extracted rows (all kinds): 1557, Promises (all topics): 854, Promises in Forest-related categories: 397, Stated facts (baseline): 300, Progress claims (status_claim): 227, Definitions: 176, Promises scored on Forest_Priorities: 461, of which score 5 (protect existing forest): 171, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 72, Highland Rim and named-place rows: 126, Public comments naming the Highland Rim: 30.

## v1.4 (2026-10-23)

Counts only adopted plans and official final Metro documents (48 of 54; six background documents marked not counted on Sources). Groups the top-tier Forest statements into 12 distinct items (promise_id column): made 165 times in 26 documents since 1973; none fully implemented (4 not met, 5 partly, 3 never reported). Adds three adopted items found in a completeness check against Metro's indexes: RS2025-1549 (Council names Nashville's Highland Rim Forest), BL2021-829 (Code 2.226) and Executive Order 41 (Amended). Brief: 46 full statements in 17 documents since 1973.

`versions/NHRF_Commitments_v1.4_2026-10-23.xlsx`. Documents: 54, Extracted rows (all kinds): 1557, Promises (all topics): 854, Promises in Forest-related categories: 397, Stated facts (baseline): 300, Progress claims (status_claim): 227, Definitions: 176, Promises scored on Forest_Priorities: 461, of which score 5 (protect existing forest): 171, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 72, Highland Rim and named-place rows: 126, Public comments naming the Highland Rim: 30.

## v1.3 (2026-10-23)

Adds brief_rec and brief_match columns on Commitments: every promise row tagged against the 2026 policy brief's 19 recommendations. The brief's recommendations appear as 62 separate statements in 22 Metro documents since 1973 (full matches); 185 in 27 counting partial matches. See POLICY-BRIEF-VS-PLANS.md.

`versions/NHRF_Commitments_v1.3_2026-10-23.xlsx`. Documents: 51, Extracted rows (all kinds): 1547, Promises (all topics): 850, Promises in Forest-related categories: 393, Stated facts (baseline): 299, Progress claims (status_claim): 224, Definitions: 174, Promises scored on Forest_Priorities: 457, of which score 5 (protect existing forest): 171, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 71, Highland Rim and named-place rows: 123, Public comments naming the Highland Rim: 30.

## v1.2 (2026-10-22)

Adds Concept 2010, the 1992 general plan (70-page scan, OCRed and swept; 22 rows), filling the gap between the 1981 plan and NashvilleNext. Forest_Priorities steep-slope rule now matches 'rugged terrain'.

`versions/NHRF_Commitments_v1.2_2026-10-22.xlsx`. Documents: 51, Extracted rows (all kinds): 1547, Promises (all topics): 850, Promises in Forest-related categories: 393, Stated facts (baseline): 299, Progress claims (status_claim): 224, Definitions: 174, Promises scored on Forest_Priorities: 457, of which score 5 (protect existing forest): 171, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 71, Highland Rim and named-place rows: 123, Public comments naming the Highland Rim: 30.

## v1.1 (2026-10-22)

Full OCR of the 1973 and 1981 scans (517 pages) swept with the candidate finder; 451 candidates read, 44 rows added.

`versions/NHRF_Commitments_v1.1_2026-10-22.xlsx`. Documents: 50, Extracted rows (all kinds): 1525, Promises (all topics): 834, Promises in Forest-related categories: 384, Stated facts (baseline): 295, Progress claims (status_claim): 222, Definitions: 174, Promises scored on Forest_Priorities: 444, of which score 5 (protect existing forest): 162, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 71, Highland Rim and named-place rows: 123, Public comments naming the Highland Rim: 30.

## v1.0 (2026-10-22)

First complete release. Adds the Character Manual Introduction, T1 and T3 and the Green Hills-Midtown plan; a finder sweep of 18 earlier plans; the 2015-2016 Whites Creek Planning Commission minutes (Rural Character Subdivision Regulations RS2016-104, Whites Creek policies RS2016-142); the sources manifest with fingerprints and cover images; and GAPS-AND-LIMITS.md.

`versions/NHRF_Commitments_v1.0_2026-10-22.xlsx`. Documents: 50, Extracted rows (all kinds): 1481, Promises (all topics): 813, Promises in Forest-related categories: 377, Stated facts (baseline): 275, Progress claims (status_claim): 219, Definitions: 174, Promises scored on Forest_Priorities: 432, of which score 5 (protect existing forest): 154, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 71, Highland Rim and named-place rows: 117, Public comments naming the Highland Rim: 30.

## v0.9 (2026-10-22)

Baseline release of the workbook as merged through PR #25: Highland Rim community plans, all NashvilleNext Vol IV actions, NashvilleNext Vol I and the Land Use element, Forest_Priorities, promise checks through pair 27.

`versions/NHRF_Commitments_v0.9_2026-10-22.xlsx`. Documents: 43, Extracted rows (all kinds): 1432, Promises (all topics): 802, Promises in Forest-related categories: 368, Stated facts (baseline): 258, Progress claims (status_claim): 209, Definitions: 163, Promises scored on Forest_Priorities: 422, of which score 5 (protect existing forest): 149, Promises checked against delivery: 27, NashvilleNext Vol IV actions captured: 340, Inconsistencies flagged: 71, Highland Rim and named-place rows: 110, Public comments naming the Highland Rim: 30.
