# WP-C second pass: coverage summary (Fable and second Claude review)

**Order:** NHRF-CO-VERIFY002-002, packet `dispatch/WP-002.md`. **Prepared:** 2026-11-27.
**Frozen corpus:** `ianrhett/nhrf-research@4b67bb8f72a5b39a6b146b85a5d2893aa23fa636`.
**Reproduce:** `python3 scripts/compare_wpc2.py` from repo root. Every number below is in `verification/wp-c2/stats.json`.

## Why this pass exists

WP-C asks for a mechanical join of two independent full ledgers by stable record ID. The first WP-C (PR #10) had only one full ledger to join (Fable, PR #9), because Sol (PR #8) was sandbox-blocked at 0/216. The second full ledger (independent Claude/Opus review, PR #11) arrived after PR #10. The executive verdict (PR #13) cites "212/216 disposition agreement, 0/4 flags in common", but no committed file held that join. This pass is that file.

## Join integrity

| Check | Result |
|---|---|
| Baseline IDs (`selected-216-ids.csv`, PR #7) | 216, all distinct |
| Joined rows in `model-comparison.csv` | 216 |
| Baseline IDs missing from either ledger | 0 |
| Rows whose ledger doc/page differs from the corpus row | 0 |
| Corpus file sha256 equals frozen `data/commitments.csv` | yes |

## Coverage against 216, per reviewer

| | Fable (PR #9) | Second Claude (PR #11) | Sol (PR #8) |
|---|---|---|---|
| original_checked = yes | 216 | 216 | 0 |
| Blocked | 0 | 0 | 216 (sandbox could not reach the source archive) |
| accept | 214 | 214 | 0 |
| reassign | 0 | 2 | 0 |
| reject | 2 | 0 | 0 |
| unresolved | 0 | 0 | 216 |
| Confidence high / med / low | 158 / 58 / 0 | 205 / 10 / 1 | n/a |

## Quote evidence in each ledger

Each ledger carries an `original_text_quote` per record: text the reviewer says it read on the cited page. This pass measures, mechanically, whether that quote shows the corpus excerpt (share of the shorter text's word 3-grams found in the longer; 0.50 or more = shows, 0.20 to 0.49 = partial, under 0.20 = absent). It checks the evidence written in the ledger, not the reviewer's underlying page match, and downloads no sources.

| Quote band | Fable | Second Claude |
|---|---|---|
| shows the excerpt | 216 | 97 |
| partial | 0 | 35 |
| absent | 0 | 84 |
| absent in both ledgers | 0 | 0 |

The second Claude ledger's quote field is a fixed-length window that, in 84 records, holds other text from the page (often the text right after the excerpt) rather than the excerpt itself. Its justification column still states a page match score for every record (for example "match score 1.0, page offset 0"). So for those 84 records the second review's verdict rests on its stated match score, not on quoted text in the ledger. Every one of the 216 excerpts is shown verbatim in at least one ledger (Fable's). Re-extracting the 84 cited pages from the hash-verified sources would settle whether the second review's underlying matches are right; that needs a source download and is not done here.

## Blockers

None for this pass. Sol's leg remains at 0/216 for the reason recorded in PR #8.
