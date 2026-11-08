#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

from openpyxl import load_workbook

SHEET = "Promised_vs_Delivered"


def cell_value(text):
    if text == "":
        return None
    if text.startswith("="):
        return text
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: apply_pvd_to_xlsx.py <promised_vs_delivered.csv> <NHRF_Commitments.xlsx>")
    csv_path, xlsx_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    rows = list(csv.reader(csv_path.open(newline="", encoding="utf-8")))
    wb = load_workbook(xlsx_path)
    ws = wb[SHEET]
    header = [c.value for c in ws[1]][: len(rows[0])]
    if header != rows[0]:
        sys.exit(f"header mismatch in {SHEET}: {header}")
    existing = [str(ws.cell(r, 1).value) for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value is not None]
    pairs_in_sheet = [p for p in existing if p.isdigit()]
    pairs_in_csv = [r[0] for r in rows[1:] if r[0].isdigit()]
    if pairs_in_csv[: len(pairs_in_sheet)] != pairs_in_sheet:
        sys.exit(f"sheet pairs {pairs_in_sheet} are not a prefix of csv pairs {pairs_in_csv}")
    old_footer = max(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value is not None)
    footer_merges = []
    for rng in list(ws.merged_cells.ranges):
        if rng.min_row > 1:
            if rng.min_row == rng.max_row == old_footer:
                footer_merges.append((rng.min_col, rng.max_col))
            ws.unmerge_cells(str(rng))
    for r_idx, row in enumerate(rows, start=1):
        for c_idx, text in enumerate(row, start=1):
            ws.cell(r_idx, c_idx).value = cell_value(text)
    for r_idx in range(len(rows) + 1, ws.max_row + 1):
        for c_idx in range(1, len(rows[0]) + 1):
            ws.cell(r_idx, c_idx).value = None
    last = len(rows)
    for min_col, max_col in footer_merges:
        ws.merge_cells(start_row=last, start_column=min_col, end_row=last, end_column=max_col)
    wb.save(xlsx_path)
    print(f"{SHEET}: {len(pairs_in_sheet)} pairs before, {len(pairs_in_csv)} after, saved {xlsx_path}")


if __name__ == "__main__":
    main()
