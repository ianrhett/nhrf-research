#!/usr/bin/env python3
"""NHRF-SOL2-REDO workbook deltas on top of v1.6.0 (2026-11-02).

Run once on the committed v1.6.0 workbook. P10 times follow the SO default of 2026-11-02:
row 704 stays funding_allocated and row 706 is context (SOL-028), so P10 has no counted statement.
"""
import os
import subprocess
import sys
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parents[2]
WB_PATH = ROOT / "docs/research/commitments/NHRF_Commitments.xlsx"
COVER = ROOT / "artifacts/research-scripts/cover_sheet.py"


def main():
    wb = openpyxl.load_workbook(WB_PATH)
    pvd = wb["Promised_vs_Delivered"]
    for row in range(2, pvd.max_row + 1):
        pair = pvd.cell(row, 1).value
        if pair == 22:
            pvd.cell(row, 14).value = "No status reported"
            old = pvd.cell(row, 15).value or ""
            note = "SOL2-2026-11-02: NashvilleNext Vol IV timeframes are start windows, not completion deadlines; no lateness verdict on the conservation-subdivision tool alone."
            pvd.cell(row, 15).value = note if not old else f"{old} {note}"

    rec = wb["Recommendations"]
    for row in range(2, rec.max_row + 1):
        pid = rec.cell(row, 1).value
        if pid == "P01":
            rec.cell(row, 4).value = 29
        elif pid == "P10":
            rec.cell(row, 4).value = 0
            rec.cell(row, 5).value = 0
            old = rec.cell(row, 9).value or ""
            note = ("No counted statement in this review: the 2011 replenish line (Commitments row 704) is "
                    "funding_allocated and the Land Trust line (row 706) is context (SOL-028, SO default 2026-11-02).")
            stale = " Counted once: the second 2011 statement asks The Land Trust for Tennessee to set up its own fund."
            assert stale in old, "P10 note text changed; review before applying"
            rec.cell(row, 9).value = old.replace(stale, " " + note)

    src = wb["Sources"]
    insert_at = None
    for i in range(2, src.max_row + 1):
        if src.cell(i, 1).value == "Total":
            insert_at = i
            break
    assert insert_at, "Sources Total row missing"

    new_rows = [
        (
            "MPC_Minutes_2008-08-14",
            "Metro Planning Commission minutes, August 14, 2008 (RS2008-167, Scottsboro/Bells Bend Detailed Design Plan, 2008CP-07G-03, adopted 10-0)",
            "2008-08-14",
            "Minutes of adoption; uncounted background source",
            12,
            "https://www.nashville.gov/sites/default/files/2021-09/080814m.pdf",
            "no",
            "Uncounted source (SOL2). Wording (SOL-11): about 13,407-acre study area; 77% in conservation-focused land-use policies "
            "(58% Natural Conservation, 19% Rural Parks/Open Space), not proof that 77% is legally conserved. One unit per five acres "
            "is a conditional policy option tied to environmental constraints (existing AR2a zoning was one per two acres), not an "
            "enacted rezoning. Alternative Development Area policies were indefinitely deferred at adoption (minutes pp5, 12).",
        ),
        (
            "Subdivision_Regulations_Chapter_4_2024",
            "Metro Planning Commission Subdivision Regulations, Chapter 4 (Rural Character Subdivisions), amended June 27, 2024",
            "2024-06-27",
            "Adopted enacted rule (Planning Commission)",
            6,
            "https://www.nashville.gov/sites/default/files/2024-08/Subdivision-Regulations-Chapter-4-240627.pdf",
            "yes",
            "Counted enacted rule (SOL2): binding rural subdivision standards outside Metro Code; see RURAL-ZONING-CHECK.md.",
        ),
    ]
    src.insert_rows(insert_at, len(new_rows))
    for offset, row in enumerate(new_rows):
        r = insert_at + offset
        doc, title, date, status, pages, url, counted, reason = row
        vals = (doc, title, date, status, pages, url, f"=COUNTIF(Commitments!$A:$A,A{r})", counted, reason)
        for c, val in enumerate(vals, 1):
            cell = src.cell(r, c, val)
            cell.font = Font(name="Calibri", size=11)

    total_row = insert_at + len(new_rows)
    assert src.cell(total_row, 1).value == "Total"
    src.cell(total_row, 7).value = f"=SUM(G2:G{total_row - 1})"

    if "Plan_lineage" not in wb.sheetnames:
        ws = wb.create_sheet("Plan_lineage")
        headers = [
            "document_key",
            "title",
            "adopted",
            "body",
            "successor_or_amendment",
            "forest_recommendations",
            "notes",
        ]
        ws.append(headers)
        rows = [
            (
                "NEA_1973_Natural_Environmental_Analysis",
                "Natural Environmental Analysis",
                "1973",
                "Metro Planning Commission staff study (not a general plan)",
                "Background to General Plan 1980-2000",
                "yes",
                "Earliest Rim conservation language in corpus (FACTS F1).",
            ),
            (
                "General_Plan_1980_2000",
                "General Plan 1980-2000",
                "1981 (Res. 81-657, per Sources tab)",
                "See Sources tab",
                "Superseded by Concept 2010",
                "yes",
                "General plan (FACTS F5a).",
            ),
            (
                "Concept_2010_General_Plan_1992",
                "Concept 2010: A General Plan for Nashville and Davidson County",
                "1992 [ASSUMED]; adoption resolution not located (SOL-031)",
                "Metro Planning Commission",
                "Superseded by NashvilleNext",
                "yes",
                "General plan (FACTS F5a).",
            ),
            (
                "NashvilleNext",
                "NashvilleNext: A General Plan for Nashville and Davidson County",
                "2015-06 (RS2015-256); amended 2017-08 (RS2017-277)",
                "Metro Planning Commission",
                "Current general plan",
                "yes",
                "17 files = 1 document in counts (FACTS F2).",
            ),
            (
                "Subdivision_Regulations_Chapter_4_2024",
                "Subdivision Regulations Ch. 4",
                "2024-06 (amended)",
                "Metro Planning Commission",
                "none",
                "no",
                "Enacted rule; slope set-asides for T2 rural policy subdivisions.",
            ),
        ]
        for row in rows:
            ws.append(row)
        for c in ws[1]:
            c.font = Font(name="Arial", size=10, bold=True, color="FFFFFFFF")
            c.fill = PatternFill("solid", fgColor="FF2F5D3A")
        ws.freeze_panes = "A2"

    wb.save(WB_PATH)
    env = {**os.environ, "NHRF_ASOF": "2026-11-02"}
    subprocess.run([sys.executable, "-I", str(COVER), str(WB_PATH)], check=True, env=env)
    print("SOL2 workbook applied:", WB_PATH)


if __name__ == "__main__":
    main()
