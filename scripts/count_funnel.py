#!/usr/bin/env python3
import re
import sys
import json
from pathlib import Path
import pandas as pd

WB = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[2] / "docs/research/commitments/NHRF_Commitments.xlsx")

REC_TYPES = {"recommendation", "commitment", "target", "funding_estimate"}
FOREST_CATS = {"forest_protection", "tree_canopy", "highland_rim_named_place",
               "habitat_natural_area", "land_acquisition", "open_space"}
RULES = {"Ordinance_BL2021-829", "Executive_Order_041A_2024", "Metro_Code_17.28.030",
         "Metro_Code_17.28.065", "Metro_Code_17.40.440", "Ordinance_BL2017-725",
         "Subdivision_Regulations_Chapter_4_2024"}
RESOLUTIONS = {"Resolution_RS2025-1549", "Resolution_RS2025-1556"}
ENACTED = RULES | RESOLUTIONS
RULED_ENACTED = ["Ordinance_BL2021-829", "Executive_Order_041A_2024", "Metro_Code_17.28.030"]


def document_of(doc):
    if doc.startswith("NashvilleNext_"):
        return "NashvilleNext"
    if doc.startswith("Plan_to_Play_2026"):
        return "Plan_to_Play_2026"
    return doc


s = pd.read_excel(WB, sheet_name="Sources")
s = s[s["counted"].isin(["yes", "no"])]
counted_files = set(s.loc[s["counted"] == "yes", "doc"])

c = pd.read_excel(WB, sheet_name="Commitments")
c = c[c["doc"].isin(counted_files)].copy()
c["document"] = c["doc"].map(document_of)
c["forest"] = c["category"].isin(FOREST_CATS)
c["enacted"] = c["doc"].isin(ENACTED)

docs = sorted({document_of(d) for d in counted_files})
recs = c[c["item_type"].isin(REC_TYPES) & ~c["enacted"]]
tagged = recs["promise_id"].astype(str).str.match(r"^P(0[1-9]|1[0-9])$")
frecs = recs[recs["forest"] | tagged]
docs_with_frec = sorted(frecs["document"].unique())
recurring19 = frecs[frecs["promise_id"].astype(str).str.match(r"^P(0[1-9]|1[0-9])$")]
core12 = recurring19[recurring19["promise_id"].astype(str).str.match(r"^P(0[1-9]|1[0-2])$")]

alloc = c[c["item_type"] == "funding_allocated"]


def year_of(text):
    m = re.findall(r"(19\d\d|20\d\d)", str(text))
    return int(m[0]) if m else None


doc_year = {}
for _, row in s[s["counted"] == "yes"].iterrows():
    y = year_of(row["date"])
    d = document_of(row["doc"])
    doc_year[d] = min(doc_year.get(d, y), y)


def span(frame):
    ys = sorted(doc_year[d] for d in frame["document"].unique())
    return [ys[0], ys[-1]]


r = pd.read_excel(WB, sheet_name="Recommendations")
r = r[r["promise_id"].astype(str).str.match(r"^P\d\d$")]
r_core = r[r["promise_id"].astype(str).str.match(r"^P(0[1-9]|1[0-2])$")]

per_rec = recurring19.groupby("promise_id").agg(
    times=("doc", "size"),
    documents=("document", "nunique"),
    first_year=("document", lambda x: min(doc_year[d] for d in x)),
)
brief_any = recs[recs["brief_rec"].notna()]
brief_full = brief_any[brief_any["brief_match"].astype(str).str.contains("full")]

p = pd.read_excel(WB, sheet_name="Promised_vs_Delivered")
p = p[pd.to_numeric(p["pair"], errors="coerce").notna()]
p_counted = p[p["promise_doc"].isin(counted_files)]

out = {
    "workbook_rows_all": int(len(pd.read_excel(WB, sheet_name="Commitments"))),
    "workbook_rows_counted": len(c),
    "files_counted": len(counted_files),
    "documents_counted": len(docs),
    "nashvillenext_files": sum(d.startswith("NashvilleNext_") for d in counted_files),
    "documents_with_forest_recommendations": len(docs_with_frec),
    "documents_with_forest_recommendations_list": docs_with_frec,
    "recommendations_all_topics": len(recs),
    "recommendations_by_type": recs["item_type"].value_counts().to_dict(),
    "recommendations_forest": len(frecs),
    "recommendations_forest_by_type": frecs["item_type"].value_counts().to_dict(),
    "recurring19_rows": len(recurring19),
    "recurring19_distinct": recurring19["promise_id"].nunique(),
    "recurring19_documents": recurring19["document"].nunique(),
    "core12_rows": len(core12),
    "core12_distinct": core12["promise_id"].nunique(),
    "core12_documents": core12["document"].nunique(),
    "recurring19_years": span(recurring19),
    "core12_years": span(core12),
    "recurring19_document_list": sorted(recurring19["document"].unique()),
    "status_19": r["status"].value_counts().to_dict(),
    "status_core12": r_core["status"].value_counts().to_dict(),
    "per_recommendation": {k: {kk: int(vv) for kk, vv in v.items()} for k, v in per_rec.to_dict("index").items()},
    "brief_rows_any": len(brief_any),
    "brief_documents_any": brief_any["document"].nunique(),
    "brief_rows_full": len(brief_full),
    "brief_documents_full": brief_full["document"].nunique(),
    "enacted_rule_documents": sorted(RULES & counted_files),
    "resolution_documents": sorted(RESOLUTIONS & counted_files),
    "documents_without_forest_recommendations": len(docs) - len(docs_with_frec),
    "ruled_enacted_present": [d for d in RULED_ENACTED if d in counted_files],
    "funding_allocated_rows": len(alloc),
    "funding_allocated_forest_rows": int(alloc["forest"].sum()),
    "pvd_pairs_all": len(p),
    "pvd_tally_all": p["assessment"].value_counts().to_dict(),
    "pvd_pairs_counted_docs": len(p_counted),
    "pvd_tally_counted_docs": p_counted["assessment"].value_counts().to_dict(),
}
print(json.dumps(out, indent=2))
