# WP-A: deterministic count reconciliation (NHRF-VERIFY-002)

Scope: deterministic arithmetic only. This audit rebuilds the published WP-A counts
from the frozen source rows and the documented filters, and records a status per
metric. No PDFs were read, no source content was judged, and no published or data
files were modified.

## Pinned source

- Repository: `ianrhett/nhrf-research` (public)
- Frozen corpus SHA: `4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`
- Workbook: `data/NHRF_Commitments.xlsx` (sheet `Commitments` has 1557 rows)
- Source CSVs: `data/commitments.csv` (1557 rows), `data/sources.csv`, `data/recommendations.csv`, `data/promise_counts.csv`

## Reproducing command

From the repository root, checked out at the SHA above:

```
python3 scripts/reconcile_wpa.py
```

This writes `verification/reconciliation.csv` and `verification/selected-216-ids.csv`,
and prints a summary. The script rebuilds every metric two independent ways:

1. Authoritative path: it runs the published `scripts/count_funnel.py` against
   `data/NHRF_Commitments.xlsx` and reads its JSON (the published counting code,
   reused unchanged). `count_funnel.py` reproduces `scripts/funnel.json` byte for
   byte at this SHA.
2. Independent path: it rebuilds the same metrics from the source CSV rows
   (`data/commitments.csv` and `data/sources.csv`) by re-applying the documented
   filters, with no dependency on `count_funnel.py`.

A metric is `dataset confirmed` only when the independent CSV rebuild equals the
published figure and the `count_funnel.py` run agrees.

## Numeric reconciliation (headline metrics)

The full machine-readable table, including every per-group row, is
`verification/reconciliation.csv`.

| metric | published/expected | reproduced | status |
|---|---|---|---|
| total extracted rows | 1557 | 1557 | dataset confirmed |
| rows in counted files | 1272 | 1272 | dataset confirmed |
| counted files | 49 | 49 | dataset confirmed |
| consolidated documents | 32 | 32 | dataset confirmed |
| forest-related recommendation-type records | 340 | 340 | dataset confirmed |
| documents holding forest records | 15 | 15 | dataset confirmed |
| selected P01 to P19 records | 216 | 216 | dataset confirmed |
| distinct groups | 19 | 19 | dataset confirmed |
| documents holding selected records | 13 | 13 | dataset confirmed |
| type: recommendation | 137 | 137 | dataset confirmed |
| type: commitment | 43 | 43 | dataset confirmed |
| type: target | 35 | 35 | dataset confirmed |
| type: funding estimate | 1 | 1 | dataset confirmed |

Every WP-A headline metric is `dataset confirmed`. No metric is an arithmetic
discrepancy, and none is source-still-unverified.

## Per-group record counts (the 19)

Record count is the number of selected rows in each group, equal to the
`times` column of `data/recommendations.csv` and to `count_funnel.py`'s
`per_recommendation[...].times`. All 19 are `dataset confirmed`.

| group | record count | group | record count |
|---|---|---|---|
| P01 | 29 | P11 | 9 |
| P02 | 15 | P12 | 1 |
| P03 | 15 | P13 | 9 |
| P04 | 12 | P14 | 9 |
| P05 | 15 | P15 | 8 |
| P06 | 9 | P16 | 5 |
| P07 | 22 | P17 | 8 |
| P08 | 16 | P18 | 7 |
| P09 | 19 | P19 | 7 |
| P10 | 1 | | |

Sum: 216 (with P01 at 29). Note that `data/promise_counts.csv` lists P01 at 30 and
sums to 217; see the P01 section below.

## Per-group document counts: source files vs consolidated documents

Two different document counts exist per group, and they are not the same figure:

- Source-file count: the number of distinct source files, as published in the
  `docs` column of `data/promise_counts.csv` and the `documents` column of
  `data/recommendations.csv`.
- Consolidated-document count: the number of distinct consolidated documents after
  the published crosswalk is applied (`count_funnel.py` `document_of`): all
  `NashvilleNext_*` component files collapse to one document `NashvilleNext`, and
  `Plan_to_Play_2026_Update` plus `Plan_to_Play_2026_Appendix` collapse to one
  document `Plan_to_Play_2026`.

Both figures are reproduced exactly. 11 of the 19 groups show a documented
discrepancy where the source-file count exceeds the consolidated-document count,
and that gap is explained entirely by the two consolidations above.

| group | consolidated documents | source files | discrepancy |
|---|---|---|---|
| P01 | 5 | 13 | yes |
| P02 | 3 | 3 | no |
| P03 | 5 | 8 | yes |
| P04 | 5 | 7 | yes |
| P05 | 5 | 8 | yes |
| P06 | 5 | 7 | yes |
| P07 | 6 | 8 | yes |
| P08 | 7 | 7 | no |
| P09 | 4 | 5 | yes |
| P10 | 1 | 1 | no |
| P11 | 3 | 5 | yes |
| P12 | 1 | 1 | no |
| P13 | 3 | 3 | no |
| P14 | 6 | 6 | no |
| P15 | 6 | 6 | no |
| P16 | 2 | 2 | no |
| P17 | 2 | 4 | yes |
| P18 | 4 | 6 | yes |
| P19 | 3 | 5 | yes |

Discrepancy count: 11 (P01, P03, P04, P05, P06, P07, P09, P11, P17, P18, P19). This
matches the expected 11 per-group document-count discrepancies. These are not
errors. They are the expected effect of counting consolidated documents rather than
source files. The headline "13 documents" figure for the full set of 216 records is
the consolidated-document count, consistent with this column.

## The P01 discrepancy: 29 vs 30 (both reproduced, not resolved)

Both figures are independently reproduced from the frozen rows:

- `data/promise_counts.csv` lists P01 at 30 and its `times` column sums to 217.
- `data/recommendations.csv` and `scripts/count_funnel.py` give P01 at 29 and an
  overall total of 216.

The single row that accounts for the entire difference is in the counted file
`Metro_Code_17.28.030`:

- Source CSV row ordinal (0-based in `data/commitments.csv`): 1306
- CSV line number (header is line 1): 1308
- doc: `Metro_Code_17.28.030`
- pdf_page field: `17.28.030.A.2`
- item_type: `recommendation`
- promise_id: `P01`
- metric: "Large areas of slopes over 25% to be recorded as open space"

`promise_counts.csv` counts this row under P01 (giving 30 and a 217 total).
`count_funnel.py` excludes it as an enacted code rule (giving 29 and a 216 total).
This one row is the only P01-to-P19 rec-type row whose document is in the enacted
set, so it is the sole source of both the 29 vs 30 and the 216 vs 217 gap.

### The exact exclusion rule in the code

`Metro_Code_17.28.030` is named as an enacted rule in `scripts/count_funnel.py`
(lines 13 to 17):

```python
RULES = {"Ordinance_BL2021-829", "Executive_Order_041A_2024", "Metro_Code_17.28.030",
         "Metro_Code_17.28.065", "Metro_Code_17.40.440", "Ordinance_BL2017-725",
         "Subdivision_Regulations_Chapter_4_2024"}
RESOLUTIONS = {"Resolution_RS2025-1549", "Resolution_RS2025-1556"}
ENACTED = RULES | RESOLUTIONS
```

Each counted row is flagged (line 37):

```python
c["enacted"] = c["doc"].isin(ENACTED)
```

and the exclusion is applied when the recommendation set is built (line 40):

```python
recs = c[c["item_type"].isin(REC_TYPES) & ~c["enacted"]]
```

The `& ~c["enacted"]` clause drops every row whose document is in `ENACTED`.
Because `Metro_Code_17.28.030` is in `RULES` (and therefore in `ENACTED`), its one
P01 rec-type row is removed before grouping, so P01 counts 29 and the overall total
is 216. The methodology states the rationale in plain language: the enacted rules
are used as delivery evidence, and "Plans that restate a recommendation do not count
as action" (`methodology/methodology.tmpl.html`).

Per this packet's instruction, both outputs are documented and neither is declared
correct here. The 30 / 217 figures carry the enacted code-rule row; the 29 / 216
figures exclude it under the rule above.

## Row-level inclusion and exclusion record

- Inclusion: all 216 selected records are listed with stable IDs in
  `verification/selected-216-ids.csv`. Columns: `row_ordinal` (0-based index into
  `data/commitments.csv`), `csv_line` (1-based line, header is line 1),
  `promise_id`, `doc` (source file), `document` (consolidated document),
  `pdf_page`, `item_type`, `metric`.
- Exclusion: exactly one rec-type row tagged P01 to P19 is excluded by the enacted
  rule: the `Metro_Code_17.28.030` row detailed in the P01 section above
  (row ordinal 1306, csv line 1308).

## Blockers

None. Every WP-A metric was reproduced deterministically from the frozen source
rows. No metric is source-still-unverified.
