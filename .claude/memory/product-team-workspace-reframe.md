---
name: product-team-workspace-reframe
description: Repo's primary purpose reframed to a product-team workspace (shared Claude rules/skills, per-product knowledge, scripts, demos) rather than a trading-system codebase; product code lives in separate repos for ALL products, including Research Hub
metadata:
  type: project
---

As of 2026-07-22, this repo's primary purpose is **SBSI's product team
workspace** — the team supports multiple SBSI products at once (trading
web/app, Research Hub, websites, and future ones), each needing its own
domain knowledge. This repo holds: shared Claude Code rules/skills
(`.claude/`), per-product domain knowledge (`projects/<name>/CLAUDE.md` —
NOT code), work scripts (`scripts/`), and on-demand demo generation
(`demos/`). It is not, and never becomes, the home for any SBSI product's
real codebase (OMS, core trading engine, back-office/settlement, customer
portal, Research Hub, trading web/app, websites) — those live in their own
repos.

**Why:** The human explicitly said this repo won't carry product code going
forward; its job is to be where the product team's shared Claude tooling and
per-product context live, plus scripts and the occasional demo. Clarified
2026-07-22 (same day, follow-up): this "no code here" rule applies to EVERY
SBSI product uniformly, including Research Hub — it does not get an
exception. Research Hub's folder moved from `apps/research-hub/` to
`projects/research-hub/` to make that explicit (it only ever held a
`CLAUDE.md`, no actual code, so nothing was lost).

**How to apply:** Default new work here to `scripts/`, `demos/`, or a
`projects/<name>/CLAUDE.md` update — never a new coded sub-app. See
[[project-structure-decision]] for the per-product folder pattern. Design
and document/slide deliverables typically happen via the Figma / Google
Drive integrations rather than as files committed to this repo. Enforcement
rules (TDD, no-fallbacks) stay strict for all code in this repo, including
scripts and demos — this pivot did NOT relax `.claude/rules/tdd.md` or
`.claude/rules/no-fallbacks.md`, and no hooks were changed.
