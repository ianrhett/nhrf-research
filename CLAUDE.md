# CLAUDE.md - nhrf-research

Public repository. It holds the published commitments research of the Alliance to Conserve Nashville's Highland Rim Forest: the one-pager, the data, the sources manifest, the methodology and the scripts. `README.md` is the map of the folders.

## Everything here is public

- Nothing confidential goes in this repository: no correspondence, no engagement notes, no credentials, no internal strategy. That covers commits, pull requests, issues and the flight log.
- Research content (the one-pager, the data, the sources, the methodology, the scripts) changes only through a pull request the operator approves.
- Do not alter source data to make a count agree. Record the disagreement instead.
- Corrections from the public arrive as issues, as `README.md` describes. The flight log is not the place for them.

## Flight Officer seat

- Flight log: issue 4 of this repository. State changes only.
- Work packets: `dispatch/WP-NNN.md` on `main`. One branch and one pull request per packet. Never merge your own pull request.
- Parent lane: `ianrhett/nhrf`. Strategy and rulings live there, not here.
- Seat charters: `prompts/FO.md` and `prompts/SO.md` in `ianrhett/spaice`.

<!-- fleet-signpost v1 (spaice#190 comments 5800716535, 5232453522). Keep verbatim; checked by spaice scripts/atlas/check_lane_signposts.py. -->
## Fleet signpost

- Fleet Atlas: https://github.com/ianrhett/spaice/blob/main/ATLAS.md
- Infrastructure register: https://github.com/ianrhett/spaice/blob/main/docs/INFRASTRUCTURE.md

Read both before searching for any host, path, credential location or service.
spaice is private; fetch with `gh api repos/ianrhett/spaice/contents/<path> -H 'Accept: application/vnd.github.raw'`.
<!-- /fleet-signpost -->
