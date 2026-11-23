# Fable (WP-B) findings

Independent audit of the 216 selected forest/conservation records. Record ids below
are `row_ordinal` values (the `record_id` column in `fable/evidence-ledger.csv`).

## Overall

The corpus is accurate on its primary-source side. All 216 cited excerpts were found
on their cited pages of sha256-validated originals, with zero off-by-one page errors,
and all 25 source documents' sha256 matched the MANIFEST. Disposition: 214 accept,
2 reject, 0 reassign, 0 unresolved. The discrepancies below are narrow and are mostly
about record TYPE, inclusion boundary, duplication and excerpt quality, not about
fabricated pages or wrong citations.

## Top 5 discrepancies

1. Funding estimate included as a forest record (reject).
   record_id 102, Plan_to_Play_2017 p234. The row "Market value to acquire regional
   park acres" = $210,905,799 is a cost calculation on the page "7.6 FUNDING THE FUTURE
   / MARKET RATE FOR LAND ACQUISITION NEEDS" ($66,180/acre x 3,187 acres). The counting
   boundary explicitly excludes funding estimates from the 216. Its corpus item_type is
   already `funding_estimate`, so it is a labeling-vs-inclusion inconsistency.

2. Same action counted twice within one document (duplicate; reject one).
   record_ids 1220 and 1295, NashvilleNext Vol4 Actions. Action #323 ("apply new Rural
   CCM policies; discourage sewer extension") is cross-listed verbatim under BE 1.1
   (p49) and NR 4.2 (p79). The identical excerpt appears for both. This double-counts a
   single action. Rejected the BE 1.1 cross-listing (1220); kept the Natural-Resources
   listing (1295) as the substantive forest placement.

3. Target / estimate sub-types inside a "recommendation" set (type-boundary issue).
   35 records are sub-typed `target` and 1 `funding_estimate` (36 of 216). Many are
   legitimate recommended goals (acquire 3,000 acres; raise transect canopy to 65%;
   level-of-service acreage). They were accepted as in-scope recommendation-family
   records, but under a strict recommendation-only reading of the counting boundary all
   36 would be flagged for type review. This materially affects what "216 recommendations"
   means and is the largest single category question for the adjudicator.

4. Excerpt-selection quality: descriptive, boilerplate or mis-summarized excerpts.
   Some records cite a descriptive sentence rather than the operative recommendation, or
   carry a metric summary that mischaracterizes the quoted text. Clearest cases:
   record_ids 1383 and 1384 (West Nashville p30 Hillwood, p31 Knob Hill) share the
   identical boilerplate excerpt "subject to the creation of permanently protected open
   space within the..." with nothing identifying the two different sites; several 1973
   NEA rows quote scenic description rather than an action statement; and record_id 702
   (the sole P10 record) carries the metric label "Metro Open Space Fund balance (2011)"
   and value $5,000,000 even though its excerpt correctly quotes the replenish
   recommendation. These were accepted but marked med-confidence.

5. 216 is not 216 unique promises; two groups rest on one record.
   The set includes cross-document restatements (the same promise recurring across
   plans), consistent with the corpus `times` design: NR goal 1 (record_ids 604 / 1230)
   and NR policy 1.4 preserve/expand canopy (606 / 1252 / 1009 / 420) recur across
   NashvilleNext Vol2, Vol4, the UFLMP and the MS4 report. Separately, promise groups P10
   (record_id 702) and P12 (record_id 1290, NashvilleNext Vol4 action #148 upstream
   conservation) each rest on a single record, so their status has a one-source evidence
   base.

## Other notes

- Phased targets are distinct, not duplicates: record_ids 668 / 669 (Open Space p11,
  "Privately conserve a minimum of 3,000 acres") use one source sentence for two phases
  (first 10 years, then an additional 3,000 by 2035). Kept both; `duplicate_key`
  PHASE-privcons3k documents the shared sentence. Per-subarea UFLMP canopy transect
  targets were likewise NOT treated as duplicates despite shared wording, because each
  carries a distinct baseline.
- Group boundaries overlap and were not re-derived. A keyword scan flagged 13 weak
  group-fit outliers (e.g., record_id 798 "Rim escarpment lakes as future parkland" sits
  in P08 buy-land but also fits P02 escarpment). None was a clear enough error to
  reassign; this is a limitation of this review, not a clearance of the grouping.
- `duplicate_key` clusters in the ledger: RST-NRgoal1, RST-NRpol1.4 (cross-document
  restatements, accepted), PHASE-privcons3k (distinct phases, accepted), TPL-protOS and
  TPL-P2Ptable27 (shared boilerplate / shared table row, distinct records, accepted),
  DUP-act323 (true intra-document duplicate, one rejected).

## Implementation evidence (see implementation.csv)

This audit verified the recommendation side (that each record reflects real cited text).
It did not independently trace implementation outcomes for most promise groups, because
that requires ordinance, budget and outcome records outside the 216-record page checks.
The one group with implementation evidence inside the audited documents is P14 (funded
urban forestry program and current canopy studies): the 2026 Hazard Mitigation Plan
(p222) states Metro Water Services coordinates urban forestry, manages the tree bank and
performs a canopy assessment every five years, and canopy assessments exist for 2010 and
2023. For all other groups, implementation status is marked not independently verified
with the specific gap stated.
