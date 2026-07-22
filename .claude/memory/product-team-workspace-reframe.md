---
name: product-team-workspace-reframe
description: Repo's primary purpose reframed to a product-team workspace (shared Claude rules/skills, scripts, demos) rather than a trading-system codebase
metadata:
  type: project
---

As of 2026-07-22, this repo's primary purpose is **SBSI's product team
workspace** — shared Claude Code rules/skills, work scripts (`scripts/`),
and on-demand demo generation (`demos/`) — not the home for SBSI's
production trading-system codebases (OMS, core trading engine, back-office/
settlement, customer portal). Those are expected to live in their own repos
if/when built.

**Why:** The human explicitly said this repo won't carry much code going
forward; its job is to be where the product team's shared Claude tooling
lives, plus scripts and the occasional demo.

**How to apply:** Default new work here to `scripts/` or `demos/`, not new
`apps/` sub-projects. `apps/research-hub/` is a real, existing sub-project
that predates this framing and stays as-is, unaffected by this decision —
see [[project-structure-decision]]. Enforcement rules (TDD, no-fallbacks)
were explicitly kept strict for all code in this repo, including scripts
and demos — this pivot did NOT relax `.claude/rules/tdd.md` or
`.claude/rules/no-fallbacks.md`, and no hooks were changed.
