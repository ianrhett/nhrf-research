#!/usr/bin/env python3
"""NHRF-P10-RECODE workbook delta (operator ruling 2026-11-02, nhrf#2 comment 6586650388).

Run once on the SOL2 workbook (commit e610c751). Recodes the 2011 Open Space Plan replenish line
from funding_allocated to recommendation, then sets P10 times and documents from count_funnel.py.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
WB_PATH = ROOT / "docs/research/commitments/NHRF_Commitments.xlsx"
COVER = ROOT / "artifacts/research-scripts/cover_sheet.py"
FUNNEL = ROOT / "artifacts/research-scripts/count_funnel.py"
EXCERPT = "Make effort regularly to replenish the Metro Open Space Fund (currently at $5 million)."
NOTE = "2011 baseline: fund balance $5M; recoded per operator ruling 2026-11-02 (sentence is an instruction to replenish)."
STALE = (" No counted statement in this review: the 2011 replenish line (Commitments row 704) is "
         "funding_allocated and the Land Trust line (row 706) is context (SOL-028, SO default 2026-11-02).")


def main():
    wb = openpyxl.load_workbook(WB_PATH)
    com = wb["Commitments"]
    hdr = [c.value for c in com[1]]
    col = {name: hdr.index(name) + 1 for name in ("item_type", "excerpt", "notes", "promise_id")}
    hits = [r for r in range(2, com.max_row + 1) if com.cell(r, col["excerpt"]).value == EXCERPT]
    assert len(hits) == 1, hits
    row = hits[0]
    assert com.cell(row, col["item_type"]).value == "funding_allocated"
    assert com.cell(row, col["promise_id"]).value == "P10"
    com.cell(row, col["item_type"]).value = "recommendation"
    old = com.cell(row, col["notes"]).value or ""
    com.cell(row, col["notes"]).value = f"{old} {NOTE}" if old else NOTE
    wb.save(WB_PATH)

    # P10 times and documents come from the counting script, not from this file.
    out = subprocess.run([sys.executable, str(FUNNEL)], check=True, capture_output=True, text=True).stdout
    p10 = json.loads(out)["per_recommendation"]["P10"]

    wb = openpyxl.load_workbook(WB_PATH)
    rec = wb["Recommendations"]
    rows = [r for r in range(2, rec.max_row + 1) if rec.cell(r, 1).value == "P10"]
    assert len(rows) == 1
    r = rows[0]
    rec.cell(r, 4).value = p10["times"]
    rec.cell(r, 5).value = p10["documents"]
    rec.cell(r, 6).value = 2011
    rec.cell(r, 7).value = 2011
    done = rec.cell(r, 9).value or ""
    assert STALE in done, "P10 what_was_done text changed; review before applying"
    rec.cell(r, 9).value = done.replace(STALE, "")
    wb.save(WB_PATH)

    env = {**os.environ, "NHRF_ASOF": "2026-11-02"}
    subprocess.run([sys.executable, "-I", str(COVER), str(WB_PATH)], check=True, env=env)
    print("P10 recode applied: Commitments row", row, "P10", p10)


if __name__ == "__main__":
    main()
