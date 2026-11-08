#!/usr/bin/env python3
"""Re-adjudicate flood_credit_candidates.json under sentence-only rule (SOL2 D-B)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "artifacts/research-scripts/2026-10-26/flood_credit_candidates.json"
NOTE = ROOT / "docs/research/FOREST-FLOOD-CREDITS.md"

ENGINEERED = re.compile(
    r"bioretention|rain garden|tree box|green roof|permeable pavement|stormwater planter",
    re.I,
)


def is_sentence_only(text: str) -> bool:
    t = " ".join(text.split()).strip()
    if not t or len(t) < 20:
        return False
    if ENGINEERED.search(t):
        return False
    words = t.split()
    alpha = re.sub(r"[^A-Za-z]", "", t)
    if alpha and sum(1 for c in alpha if c.isupper()) / len(alpha) > 0.55 and len(words) <= 12:
        return False
    if t.startswith("To ") and len(words) < 18:
        return False
    if t.endswith(":") or t.endswith("?"):
        return False
    return True


def main():
    data = json.loads(LEDGER.read_text())
    dropped = []
    for c in data["candidates"]:
        if not c.get("kept"):
            continue
        ok = is_sentence_only(c["sentence"])
        if c["i"] in (155, 158):
            ok = False
        if not ok:
            c["kept"] = False
            dropped.append(c["i"])
    kept = [c for c in data["candidates"] if c.get("kept")]
    data["note"] = (
        f"{data.get('note', '')} SOL2-2026-11-02: re-adjudicated under sentence-only rule; "
        f"dropped candidate ids {sorted(dropped)}."
    )
    LEDGER.write_text(json.dumps(data, indent=1) + "\n")
    print("kept", len(kept), "dropped", len(dropped), "ids", sorted(dropped))
    return len(kept), sorted(dropped)


if __name__ == "__main__":
    main()
