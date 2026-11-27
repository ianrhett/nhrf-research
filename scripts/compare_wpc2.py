#!/usr/bin/env python3
"""WP-C, second pass: mechanical join of the two full WP-B evidence ledgers.

NHRF-CO-VERIFY002-002 asks WP-C to join two independent original-source
ledgers by stable record ID. The first WP-C (PR #10) could join only one full
ledger (Fable, PR #9), because Sol (PR #8) was sandbox-blocked at 0/216. The
second full ledger (independent Claude/Opus review, PR #11) arrived after PR #10
and was never joined in a committed file. This script does that join.

No model judgment. Every output field is computed from the input files.

Inputs (snapshots, sha256 pinned in verification/wp-c2/inputs/MANIFEST.sha256):
  verification/wp-c2/inputs/selected-216-ids.csv      PR #7  @ addf1c0
  verification/wp-c2/inputs/fable-evidence-ledger.csv PR #9  @ f48b0a7
  verification/wp-c2/inputs/claude2-evidence-ledger.csv PR #11 @ 7bbed27
  verification/wp-c2/inputs/wpc1-model-comparison.csv PR #10 @ 2bbeb43 (ChatGPT tags)
  data/recommendation_statements.csv  (byte-identical to data/commitments.csv
                                       at frozen corpus 4b67bb8)

Run from repo root:  python3 scripts/compare_wpc2.py
Outputs: verification/wp-c2/model-comparison.csv, reconciliation-queue.csv,
         stats.json. coverage-summary.md and reconciliation-summary.md are
         written from stats.json and cite its numbers.
Exit 1 if any baseline ID is missing from either ledger, or any row's doc/page
disagrees with the corpus row it names.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IN = ROOT / "verification" / "wp-c2" / "inputs"
OUT = ROOT / "verification" / "wp-c2"
CORPUS = ROOT / "data" / "recommendation_statements.csv"
FROZEN_CORPUS_SHA256 = "88730a0ceeb6338a29db65624e950f6d7dcc3101a3b63ec51ce683f8703b3b4c"

# Quote check: share of the shorter text's word 3-grams that occur in the longer.
QUOTE_SHOWS = 0.50   # at or above: the ledger quote shows the corpus excerpt
QUOTE_PARTIAL = 0.20  # below: the ledger quote does not show the excerpt


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def words(s):
    return re.findall(r"[a-z0-9]+", (s or "").lower())


def shingles(ws, n=3):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)} if len(ws) >= n else {tuple(ws)} if ws else set()


def quote_overlap(quote, excerpt):
    a, b = shingles(words(quote)), shingles(words(excerpt))
    if not a or not b:
        return 0.0
    small, big = (a, b) if len(a) <= len(b) else (b, a)
    return round(len(small & big) / len(small), 3)


def quote_band(x):
    return "shows" if x >= QUOTE_SHOWS else ("partial" if x >= QUOTE_PARTIAL else "absent")


def dup_clusters(rows):
    """record_id -> frozenset of record_ids sharing its non-empty duplicate_key."""
    by_key = defaultdict(set)
    for r in rows:
        k = (r.get("duplicate_key") or "").strip()
        if k:
            by_key[k].add(r["record_id"])
    out = {}
    for k, ids in by_key.items():
        for i in ids:
            out[i] = (k, frozenset(ids))
    return out


def main():
    corpus_sha = sha256(CORPUS)
    if corpus_sha != FROZEN_CORPUS_SHA256:
        sys.exit(f"corpus sha256 {corpus_sha} != frozen {FROZEN_CORPUS_SHA256}")

    ids = read(IN / "selected-216-ids.csv")
    fable = {r["record_id"]: r for r in read(IN / "fable-evidence-ledger.csv")}
    claude2 = {r["record_id"]: r for r in read(IN / "claude2-evidence-ledger.csv")}
    wpc1 = {r["record_id"]: r for r in read(IN / "wpc1-model-comparison.csv")}
    corpus = read(CORPUS)

    base_ids = [r["row_ordinal"] for r in ids]
    problems = []
    if len(base_ids) != 216 or len(set(base_ids)) != 216:
        problems.append(f"baseline has {len(base_ids)} rows, {len(set(base_ids))} distinct")
    for name, led in (("fable", fable), ("claude2", claude2)):
        missing = sorted(set(base_ids) - set(led), key=int)
        extra = sorted(set(led) - set(base_ids), key=int)
        if missing or extra:
            problems.append(f"{name}: missing {missing} extra {extra}")

    fdup, cdup = dup_clusters(fable.values()), dup_clusters(claude2.values())

    rows = []
    for b in ids:
        rid = b["row_ordinal"]
        c = corpus[int(rid)]
        # Identity check: the baseline row must point at the corpus row it names.
        ident_ok = (c["doc"] == b["doc"] and str(c["pdf_page"]) == str(b["pdf_page"])
                    and c["item_type"] == b["item_type"] and c["promise_id"] == b["promise_id"])
        if not ident_ok:
            problems.append(f"record {rid}: baseline does not match corpus row")
        f, k = fable.get(rid, {}), claude2.get(rid, {})
        for name, led in (("fable", f), ("claude2", k)):
            if led and (led["source_doc"] != c["doc"] or str(led["pdf_page"]) != str(c["pdf_page"])):
                problems.append(f"record {rid}: {name} doc/page differs from corpus")

        fq, kq = quote_overlap(f.get("original_text_quote"), c["excerpt"]), quote_overlap(k.get("original_text_quote"), c["excerpt"])
        fd, kd = fdup.get(rid), cdup.get(rid)
        f_set = fd[1] if fd else frozenset()
        k_set = kd[1] if kd else frozenset()
        if not fd and not kd:
            dup_cmp = ""
        elif fd and kd and f_set == k_set:
            dup_cmp = "same-cluster"
        elif fd and kd:
            dup_cmp = "overlapping-cluster"
        else:
            dup_cmp = "fable-only" if fd else "claude2-only"

        disputed = []
        if f.get("disposition") != k.get("disposition"):
            disputed.append("disposition")
        if f.get("proposed_type") != k.get("proposed_type"):
            disputed.append("proposed_type")
        if f.get("proposed_group") != k.get("proposed_group"):
            disputed.append("proposed_group")
        if dup_cmp in ("fable-only", "claude2-only", "overlapping-cluster"):
            # Fable RST-/PHASE-/TPL- keys mark related-but-distinct records, not
            # double counts; only DUP- is a within-document double count.
            disputed.append("duplicate_cluster")
        f_band, k_band = quote_band(fq), quote_band(kq)
        if f_band == "absent" or k_band == "absent":
            disputed.append("ledger_quote")

        dispositions = {f.get("disposition"), k.get("disposition")}
        if "reject" in dispositions and "disposition" in disputed:
            sev = "1-high"      # one reviewer would take the record out of the 216
        elif f_band == "absent" and k_band == "absent":
            sev = "1-high"      # neither ledger quote shows the corpus excerpt
        elif "disposition" in disputed or "proposed_type" in disputed or "proposed_group" in disputed:
            sev = "2-med"
        elif "duplicate_cluster" in disputed or "ledger_quote" in disputed:
            sev = "2-med"
        elif "med" in (f.get("confidence"), k.get("confidence")) or "low" in (f.get("confidence"), k.get("confidence")):
            sev = "3-low"
        else:
            sev = ""

        w = wpc1.get(rid, {})
        rows.append({
            "record_id": rid,
            "source_doc": c["doc"],
            "pdf_page": c["pdf_page"],
            "corpus_group": c["promise_id"],
            "corpus_type": c["item_type"],
            "fable_disposition": f.get("disposition", ""),
            "claude2_disposition": k.get("disposition", ""),
            "fable_proposed_type": f.get("proposed_type", ""),
            "claude2_proposed_type": k.get("proposed_type", ""),
            "fable_proposed_group": f.get("proposed_group", ""),
            "claude2_proposed_group": k.get("proposed_group", ""),
            "fable_confidence": f.get("confidence", ""),
            "claude2_confidence": k.get("confidence", ""),
            "fable_original_checked": f.get("original_checked", ""),
            "claude2_original_checked": k.get("original_checked", ""),
            "fable_duplicate_key": f.get("duplicate_key", ""),
            "claude2_duplicate_key": k.get("duplicate_key", ""),
            "duplicate_comparison": dup_cmp,
            "fable_quote_overlap": fq,
            "fable_quote_band": f_band,
            "claude2_quote_overlap": kq,
            "claude2_quote_band": k_band,
            "chatgpt_record_citation": w.get("chatgpt_record_citation", ""),
            "chatgpt_group_finding": w.get("chatgpt_group_finding", ""),
            "disputed_fields": ";".join(disputed),
            "severity": sev,
        })

    fields = list(rows[0].keys())
    with open(OUT / "model-comparison.csv", "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=fields)
        wr.writeheader()
        wr.writerows(rows)

    queue = sorted((r for r in rows if r["severity"]), key=lambda r: (r["severity"], r["source_doc"], int(r["pdf_page"]), int(r["record_id"])))
    with open(OUT / "reconciliation-queue.csv", "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=["severity"] + [x for x in fields if x != "severity"])
        wr.writeheader()
        wr.writerows(queue)

    def tally(key):
        return dict(sorted(Counter(r[key] for r in rows).items()))

    stats = {
        "corpus_sha256": corpus_sha,
        "baseline_ids": len(base_ids),
        "joined_rows": len(rows),
        "integrity_problems": problems,
        "fable_disposition": tally("fable_disposition"),
        "claude2_disposition": tally("claude2_disposition"),
        "fable_original_checked": tally("fable_original_checked"),
        "claude2_original_checked": tally("claude2_original_checked"),
        "fable_confidence": tally("fable_confidence"),
        "claude2_confidence": tally("claude2_confidence"),
        "disposition_agree": sum(r["fable_disposition"] == r["claude2_disposition"] for r in rows),
        "both_accept": sum(r["fable_disposition"] == r["claude2_disposition"] == "accept" for r in rows),
        "type_agree": sum(r["fable_proposed_type"] == r["claude2_proposed_type"] for r in rows),
        "group_agree": sum(r["fable_proposed_group"] == r["claude2_proposed_group"] for r in rows),
        "non_accept_fable": sorted((r["record_id"] for r in rows if r["fable_disposition"] != "accept"), key=int),
        "non_accept_claude2": sorted((r["record_id"] for r in rows if r["claude2_disposition"] != "accept"), key=int),
        "duplicate_comparison": tally("duplicate_comparison"),
        "fable_quote_band": tally("fable_quote_band"),
        "claude2_quote_band": tally("claude2_quote_band"),
        "both_quotes_absent": sorted((r["record_id"] for r in rows if r["fable_quote_band"] == r["claude2_quote_band"] == "absent"), key=int),
        "severity": tally("severity"),
        "queue_rows": len(queue),
    }
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2))
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
