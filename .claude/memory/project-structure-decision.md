---
name: project-structure-decision
description: Root repo stays framed as SBSI (CTCK/brokerage); Research Hub is a monorepo sub-app under apps/, not a domain rewrite
metadata:
  type: project
---

The root `CLAUDE.md` and `.claude/rules/domain-model.md` stay framed around
SBSI's core brokerage/trading domain (CTCK — OMS, core trading engine,
back-office/settlement, customer portal), even though the first concrete
sub-project built is **SBSI Research Hub**, a crowdsourced research/content
platform (articles, quant ratings, portfolios, screeners) — not a trading
system itself. Research Hub lives at `apps/research-hub/` with its own
`CLAUDE.md` covering its content-domain entities (Contributor, Article/Idea,
Ticker, Quant Rating, Portfolio, Screener), decided 2026-07-21.

**Why:** SBSI is a securities brokerage; Research Hub is explicitly a
top-of-funnel acquisition product meant to pull retail users toward SBSI's
trading products, not a separate business. The human confirmed: keep the
CTCK/trading framing at the root, add Research Hub as a sub-project, and
structure the repo as a monorepo (`apps/<name>/`).

**How to apply:** Any future SBSI sub-project (mobile app, back-office tool,
etc.) should follow the same pattern — new folder under `apps/`, its own
`CLAUDE.md` for domain-specific rules, root `CLAUDE.md`/`domain-model.md`
reserved for the brokerage's core trading entities. Don't rewrite the root
domain model to fit a non-trading sub-project's vocabulary. See
[[linear-research-hub-project]] for where Research Hub work is tracked. Tech
stack for both root and Research Hub was explicitly left as an undecided
placeholder as of this decision — don't assume a stack until CLAUDE.md is
updated with real values.
