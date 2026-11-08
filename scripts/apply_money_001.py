#!/usr/bin/env python3
"""NHRF-MONEY-001 workbook delta (nhrf#4 comment 6587206103; operator approval 2026-11-02 14:04 CT).

Run once on the P10-RECODE workbook (commit 3dac83e8). Rewrites P08, P10 and P11 what_was_done
and evidence on the Recommendations tab, adds four delivery-evidence rows (counted = no) to the
Sources tab, regenerates the About tab, and writes recommendations.csv and sources.csv.
Counts are not touched: count_funnel.py must still report R2 340 and R3 216.
"""
import csv
import os
import subprocess
import sys
from copy import copy
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
CDIR = ROOT / "docs/research/commitments"
WB_PATH = CDIR / "NHRF_Commitments.xlsx"
COVER = ROOT / "artifacts/research-scripts/cover_sheet.py"

CIB = ("listed in the adopted FY2027 capital budget (27DS0031, $7,000,000, requested by At-Large CM "
       "Burkley Allen; adopted CIB p III-91); FY2027 Capital Spending Plan not yet issued as of 2026-11-02")

P08_OLD = "A $7 million Highland Rim easement project in the FY2027 capital budget is unfunded."
P08_NEW = f"A $7 million Highland Rim conservation easement project is {CIB}."
P08_OLD_VERIFY = "Metro reports $12.8 million allocated for park land since 2017 (to be verified), against"
P08_NEW_VERIFY = "Metro reports $12.8 million allocated for park land since 2017, against"
P08_EV_ADD = ("; FY26 Report on Council Requests 26-01-02 (CM Kimbrough, Conservation Assistance Fund; Planning: "
              "recommend not including, p6); FY27 Report on Council Requests 27-39-02 (CM Allen, p369); "
              "FY27 Council CIB Prioritization Report (rank 12 of 187)")

P11_OLD = "the FY2027 Highland Rim easement project is unfunded,"
P11_NEW = f"the FY2027 Highland Rim conservation easement project is {CIB},"
P11_EV_ADD = ("; FY2027 CIB 27DS0031; FY26 Report on Council Requests 26-01-02 (CM Kimbrough, Conservation "
              "Assistance Fund; Planning: recommend not including, p6); FY27 Report on Council Requests 27-39-02 "
              "(CM Allen, p369)")

P10_OLD = "No record names the Open Space Fund or its balance;"
P10_NEW = ("No record found in FY2017 to FY2026 Capital Spending Plans names the Open Space Fund or its balance "
           "(searched 2026-11-02: every Capital Spending Plan file on the Finance capital budget page, FY2018 to "
           "FY2026 exhibits, resolutions, memos and presentation, and the Plan to Play 2026 Appendix; FY2017 has "
           "no spending plan file on that page);")
P10_EV_ADD = "; absence check 2026-11-02 (FY2018 to FY2026 Capital Spending Plan files, Plan to Play 2026 Appendix)"

NEW_SOURCES = [
    ("FY26_Report_on_Council_Requests_2025",
     "Report on Council Requests, FY2026 to FY2031 Capital Improvements Budget (Planning Department)",
     "February 3, 2025", "Planning staff report to Council", 378,
     "https://www.nashville.gov/sites/default/files/2025-02/FY26_CouncilRequests_CIB.pdf",
     "Delivery evidence (NHRF-MONEY-001): request 26-01-02, Conservation Assistance Fund, CM Kimbrough (District 1); "
     "Planning: recommend not including in CIB, per Parks' response (p6). Not a Metro plan; not counted.",
     "Repo copy pending: docs/research/sources/FY26_CouncilRequests_CIB.pdf (SHA-256 of the 2026-11-02 download recorded in MANIFEST.csv; binary push not available from the FO seat)."),
    ("FY27_Report_on_Council_Requests_2026",
     "Report on Council Requests, FY2027 to FY2032 Capital Improvements Budget (Planning Department)",
     "February 6, 2026", "Planning staff report to Council", 369,
     "https://www.nashville.gov/sites/default/files/2026-02/FY27_CIB_CouncilRequests_C.pdf",
     "Delivery evidence (NHRF-MONEY-001): request 27-39-02, HIghland Rim Conservation Easement Support, At-Large CM "
     "Allen, $7,000,000 build/purchase (p369). Not a Metro plan; not counted.",
     "Repo copy pending: docs/research/sources/FY27_CIB_CouncilRequests_C.pdf (SHA-256 of the 2026-11-02 download recorded in MANIFEST.csv; binary push not available from the FO seat)."),
    ("CIB_FY2027_FY2032_Adopted",
     "Capital Improvements Budget FY2027 to FY2032, Adopted (Metropolitan Planning Commission)",
     "Adopted June 9, 2026", "Adopted capital improvements budget (does not appropriate funds)", 400,
     "https://www.nashville.gov/sites/default/files/2026-10/FY27_CIB_Adopted.pdf",
     "Delivery evidence (NHRF-MONEY-001): project 27DS0031, Highland Rim Conservation Easement Support, $7,000,000, "
     "MPC rec priority B, Council priority 12 of 187 (detail p III-92, PDF p137; Council listing p III-91, PDF p38). "
     "Not a Metro plan; not counted.",
     "Repo copy pending: docs/research/sources/FY27_CIB_Adopted.pdf (SHA-256 of the 2026-11-02 download recorded in MANIFEST.csv; binary push not available from the FO seat)."),
    ("Council_CIB_Prioritization_FY2027",
     "FY2027 Metro Council CIB Project Prioritization Report",
     "September 2026 (PDF created September 23, 2026)", "Council prioritization report", 6,
     "https://www.nashville.gov/sites/default/files/2026-10/FY27_Council_PriorityReport.pdf",
     "Delivery evidence (NHRF-MONEY-001): 27DS0031 ranked 12 of 187, 55 points, districts 1, 23, 34, 35, AL-4 (p1). "
     "Not a Metro plan; not counted.",
     "Repo copy pending: docs/research/sources/FY27_Council_PriorityReport.pdf (SHA-256 of the 2026-11-02 download recorded in MANIFEST.csv; binary push not available from the FO seat)."),
]


def edit_recommendations(wb):
    rec = wb["Recommendations"]
    hdr = [c.value for c in rec[1]]
    done_col = hdr.index("what_was_done") + 1
    ev_col = hdr.index("evidence") + 1
    rows = {rec.cell(r, 1).value: r for r in range(2, rec.max_row + 1)}
    # P09 cites the same F6a figure; the "to be verified" tag goes with the F6a ruling.
    r9 = rows["P09"]
    t9 = rec.cell(r9, done_col).value
    assert "(568.78 acres reported, to be verified;" in t9
    rec.cell(r9, done_col).value = t9.replace("(568.78 acres reported, to be verified;", "(568.78 acres reported;")
    for pid, old, new, ev_add in (
        ("P08", P08_OLD, P08_NEW, P08_EV_ADD),
        ("P11", P11_OLD, P11_NEW, P11_EV_ADD),
        ("P10", P10_OLD, P10_NEW, P10_EV_ADD),
    ):
        r = rows[pid]
        text = rec.cell(r, done_col).value
        assert old in text, (pid, text)
        text = text.replace(old, new)
        if pid == "P08":
            assert P08_OLD_VERIFY in text
            text = text.replace(P08_OLD_VERIFY, P08_NEW_VERIFY)
        rec.cell(r, done_col).value = text
        rec.cell(r, ev_col).value = rec.cell(r, ev_col).value + ev_add


def add_sources(wb):
    ws = wb["Sources"]
    col_a = [ws.cell(r, 1).value for r in range(1, ws.max_row + 1)]
    total = col_a.index("Total") + 1
    assert ws.cell(total, 1).value == "Total"
    n = len(NEW_SOURCES)
    ws.insert_rows(total, amount=n)
    template = total - 1  # last data row, keeps its style
    for i, (doc, title, date, status, pages, url, reason, note) in enumerate(NEW_SOURCES):
        r = total + i
        vals = [doc, title, date, status, pages, url, f"=COUNTIF(Commitments!$A:$A,A{r})", "no", reason, note]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v)
            src = ws.cell(template, c)
            cell.font = copy(src.font)
            cell.alignment = copy(src.alignment)
            cell.number_format = src.number_format
    new_total = total + n
    assert ws.cell(new_total, 1).value == "Total"
    ws.cell(new_total, 7).value = f"=SUM(G2:G{new_total - 1})"


def dump(wb, sheet, path):
    ws = wb[sheet]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for row in ws.iter_rows(values_only=True):
            vals = ["" if v is None else v for v in row]
            if all(v == "" for v in vals):
                continue
            w.writerow(vals)


def main():
    wb = openpyxl.load_workbook(WB_PATH)
    edit_recommendations(wb)
    add_sources(wb)
    wb.save(WB_PATH)
    env = {**os.environ, "NHRF_ASOF": "2026-11-02"}
    subprocess.run([sys.executable, "-I", str(COVER), str(WB_PATH)], check=True, env=env)
    wb = openpyxl.load_workbook(WB_PATH)
    dump(wb, "Recommendations", CDIR / "recommendations.csv")
    dump(wb, "Sources", CDIR / "sources.csv")
    print("MONEY-001 applied: P08, P10, P11 reworded; 4 Sources rows added (counted = no)")


if __name__ == "__main__":
    main()
