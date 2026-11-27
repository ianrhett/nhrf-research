# NHRF civic-evidence design system

One system for three surfaces: the website (versions/v1-infrastructure.html, the direction chosen 2026-11-27), the methodology page and the one-pager (both in ianrhett/nhrf-research). Tokens live in `assets/tokens.css`; the other two surfaces carry a verbatim copy of its `:root` block and fonts. Change a token here first, then copy.

## The idea

A public record, set well. The page reads like an audited municipal document: paper ground, ink type, hairline rules, figures with their source lines beside them. Credibility comes from showing the work, not from decoration.

## Colour

| Token | Value | Use |
|---|---|---|
| `--paper` | #fbfaf7 | page ground |
| `--paper-deep` | #f1efe8 | zebra rows, photo slots, highlighted table row |
| `--card` | #fffefb | tables, ledgers, form: a sheet on the paper |
| `--rule` | #c9c4b6 | every hairline |
| `--ink` | #14213d | headings, figures, strong text |
| `--ink-soft` | #3d4a66 | body text |
| `--muted` | #5f5a4c | source lines and footnotes |
| `--green` | #1b4332 | verified figures, the primary action |
| `--signal` / `--signal-tint` | #a14a07 / #fbf1e6 | the Alliance's own ask (12,000 by 2040) and nothing else |
| `--done` `--partly` `--miss` | #1b4332 #8a5c0a #b3261e | research status only (implemented, partly, none reported) |
| `--night*` | ink-based | footer |

Rule of meaning: green is the record, signal is the Alliance speaking for itself. A verified figure is never signal; the ask is never green.

## Type

- **Source Serif 4** (variable, self-hosted): headings, body, figures. Lining tabular numerals on every figure.
- **Public Sans** (variable, self-hosted; the US Web Design System face): labels, nav, tables, source lines, buttons, form.
- Labels are sentence case and untracked. No eyebrows or kickers above headings; the heading carries the section.
- Scale: `--step--1` .875rem, `--step-0` 1.0625rem body, `--step-1` 1.25, `--step-2` 1.6, `--step-3` 2.2, `--step-4` 3.6.

## Components

- **Stat band**: figure, label, source line. Bordered sheet, cells split by hairlines. The ask cell sits on `--signal-tint`.
- **Ledger** (table, wins list, services): one bordered sheet split by hairlines, 2px ink rule under the head and above totals. No floating cards, no side bars.
- **Ask box**: full 1px signal border on signal tint. Used once per surface.
- **Pull quote**: large italic serif under a hairline, attribution in Public Sans.
- **Button**: one style, green fill, square corners, steps up 1px on hover, presses on click. Secondary action is an underlined text link.
- **Focus**: 2px signal outline, offset 3px, instant.

## Print (one-pager)

Same tokens. On paper: `--card` becomes the page, rules stay hairline, no fills except the ask tint and the zebra rows.
