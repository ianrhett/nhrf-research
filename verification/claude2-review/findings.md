# Findings — most important discrepancies

Bottom line: the 216-record corpus holds up well. Every record was checked against a hash-verified original (26/26 source files MATCH), every excerpt was located on its cited page at page-offset 0, and no record was found on the wrong page, misquoted, or fabricated. 214 of 216 are **accept**; 2 are **reassign**; 0 reject, 0 unresolved. The issues below are refinements, not failures.

## 1. Source integrity is clean; two documents needed special handling
All 26 files (24 PDFs + 2 OCR sidecars) matched their registry `sha256`. Two scanned plans (NEA 1973, General Plan 1980) were verified from the project's hash-verified OCR sidecars. **`Concept_2010_General_Plan_1992` is an image-only PDF with no OCR sidecar in the corpus** — the PDF is hash-verified, but its 11 cited pages had to be OCR'd by this reviewer (tesseract) to read them. That is a reproducibility gap in the corpus's source kit: a consumer without OCR tooling cannot verify the 11 Concept_2010 records from shipped text. Recommend adding a hash-verified `Concept_2010` OCR sidecar.

## 2. Intra-document restatements that inflate a group's instance count (accept, flagged)
Same statement counted twice **within one document and one group** (not cross-document recurrence, which is intentional):
- **`NashvilleNext_Vol4_Actions` action #323** is cross-listed under BE 1.1 (p49) and NR 4.2 (p79) — identical text, both P03, counted twice (`duplicate_key NNV4-ACT323-P03`). Adds ~1 to P03's instance count.
- **Climate Plan NE1 (p204)** contributes two P07 rows — the NR 1.4 policy sentence and the strategy's benefits/rationale sentence (`CARP-NE1-p204`).
- **Plan to Play 2026 Update Tier One ~82-acre acquisition** appears in the narrative (p107) and the summary table (p112) as two P09 rows (`P2P26-T1LFG4-82ac`).
- **Open Space Plan 2011 (p11)** splits one two-part sentence ("3,000 acres in 10 years, and an additional 3,000 by 2035") into two P09 rows with an identical excerpt (`OSP-privcons-3000-p11`).
- **NEA 1973 (p132)** has two P08 rows for the escarpment-lakes-as-parkland recommendation at different granularity (`NEA-escarplakes-p132`).
Defensible extractions, but each modestly inflates per-group "times" totals via restatement; worth noting wherever those counts are headline figures.

## 3. Two reassignments proposed
- **`MS4_Annual_Report_FY19` p16, P15 ("Warner Parks stream segments identified for mitigation")** — tagged `recommendation`, but the passage reports an activity Metro Parks has already undertaken (partnering to identify 10 segments), which reads as a **commitment/implementation item**, not a prospective recommendation. Proposed `type: recommendation -> commitment`. Still a valid P15 aquatic-habitat item (med confidence).
- **`Concept_2010_General_Plan_1992` p20, P08 ("Preserve floodplain … greenbelt linking open spaces")** — the statement is about a greenbelt **system linking major open spaces**, which fits **P18** (connected system of protected natural areas/open space) at least as well as P08 (acquire/protect natural land). Proposed `group: P08 -> P18` (low confidence; defensible either way).

## 4. Minor wording/transcription notes (left as accept)
- **`Urban_Forestry_Landscape_Master_Plan_2016` p39, P01** — the record faithfully quotes the plan's own ambiguous line "Increase slope provision in Metro ordinance that restricts development from 15% to 20%," which conflicts in direction with NashvilleNext NR 1.1 #210 ("minimize development on >15% slopes," p69). The ambiguity is in the **source**, not the extraction; flagged for downstream readers.
- A few records store a heavily truncated `excerpt` (e.g. Plan to Play p178 P08 excerpt = "rural and forested land within the county.") that under-represents the fuller sentence on the page; the cited page fully supports the record, so these are accept.

## 5. Counting boundary verified
The 216-vs-217 boundary row — `Metro_Code_17.28.030` field `17.28.030.A.2` (P01) — is present in `promise_groups.csv` but correctly **excluded** from the 216 as enacted code (consistent with `scripts/count_funnel.py`). `context`-tagged rows are likewise excluded. The selection faithfully implements the documented counting rule; the one defensible boundary judgement (17.28.030.A.2) is the only difference from a 217 count, exactly as stated.
