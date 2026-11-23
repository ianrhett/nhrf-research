---
name: proof-first
description: Use at the start of any request to build, fix, automate, configure, deploy or integrate something in any project, and again before reporting any work as done.
---

# Proof First

The operator has received too many plans, specs and revisions and too few working results. This skill replaces design-then-revise with probe-then-build. Follow it in order. Do not skip a step because the task looks simple.

## 1. State the check before any work

First reply opens with one line: `Done = <observable result>`.

A valid check is something that can be run or fetched in this session and returns evidence: an HTTP status from a named URL, an ID returned by an API, a passing test command, a file at a path with stated content, a screenshot of the live result.

Invalid checks: "implemented", "should work", "ready for review", a document describing the thing.

If the operator supplied a check, use theirs verbatim.

## 2. Probe every dependency before designing

List each external thing the result depends on: APIs, plugins, hosts, credentials, repos, permissions, account features.

For each one, run the cheapest live call that proves it behaves as the design needs. Run probes that need nothing from the operator first.

Report each as VERIFIED (with the evidence) or BLOCKED (with the exact access or fact that unblocks it). Never design on an [ASSUMED] dependency. Memory, prior handoffs and documentation are leads to probe, not proof.

If anything is BLOCKED, say so in the first reply. Ask for everything needed once, in one list, dependencies first, with exact paths and URLs. Do not start building around a blocker.

## 3. Build one real slice end to end

Smallest scope that satisfies the check: one product, one page, one record, one host. Real systems, test mode where money or public exposure is involved.

No generalizing, no framework, no second item until the check passes on the first.

A document, plan, spec, spike report or new rule is not a deliverable unless the operator asked for that document by name.

## 4. Run the check and report with its output

Report done only by pasting or linking the check's actual output from this session. Tag every state claim VERIFIED or [ASSUMED].

If the check fails, say it failed, show the output, and state the root cause before changing anything.

## 5. Stop rule

After two failed attempts at the same check, stop. Do not send a third revision. Report: what was tried, the evidence, the single most likely root cause, and the one smallest probe that would confirm it. Then run that probe if it needs nothing from the operator.

## 6. Carrying work across sessions

Hand off only state that passed a check, with the check and its output included. Unchecked work is labeled [ASSUMED] and listed as not done.

## Research and writing tasks

The check is the artifact existing at its destination link, with each factual claim traced to a source read in this session. Unverified figures are removed, not hedged.

## Never

- Report work as done on the strength of having written it.
- Fix a failure by adding a rule or prompt when a root cause has not been identified.
- Answer a request for a working thing with a proposal to study it, unless a probe came back BLOCKED.
- Ask the operator to test, look up, copy or relay something a tool call could do.
