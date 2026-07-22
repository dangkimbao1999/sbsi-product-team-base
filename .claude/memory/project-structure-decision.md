---
name: project-structure-decision
description: Root repo stays framed as SBSI (CTCK, a Vietnamese securities company); each SBSI product gets a knowledge-only folder under projects/, not a coded sub-app
metadata:
  type: project
---

The root `CLAUDE.md` and `.claude/rules/domain-model.md` stay framed around
SBSI's core brokerage/trading domain (CTCK — OMS, core trading engine,
back-office/settlement, customer portal), even though the first concrete
product documented is **SBSI Research Hub**, a crowdsourced research/content
platform (articles, quant ratings, portfolios, screeners) — not a trading
system itself. Research Hub's domain knowledge lives at
`projects/research-hub/CLAUDE.md` covering its content-domain entities
(Contributor, Article/Idea, Ticker, Quant Rating, Portfolio, Screener),
decided 2026-07-21, **superseded 2026-07-22** by
[[product-team-workspace-reframe]]: this repo never hosts product code, so
`research-hub/` moved from `apps/` to `projects/` and is knowledge-only, same
as every other product folder.

**Why:** SBSI is a securities brokerage; Research Hub is explicitly a
top-of-funnel acquisition product meant to pull retail users toward SBSI's
trading products, not a separate business. The human confirmed: keep the
CTCK/trading framing at the root, and document each SBSI product's domain
knowledge here even though the product team doesn't code any of them in
this repo.

**How to apply:** Any SBSI product the team supports (trading web/app,
websites, future ones) gets the same pattern — new folder under
`projects/`, its own `CLAUDE.md` for domain-specific knowledge, root
`CLAUDE.md`/`domain-model.md` reserved for the brokerage's core trading
entities. Don't rewrite the root domain model to fit one product's
vocabulary, and don't put application code under `projects/` — see
[[product-team-workspace-reframe]] for the code-lives-elsewhere rule. See
[[linear-research-hub-project]] for where Research Hub work is tracked. Tech
stack for root and each product was explicitly left as an undecided
placeholder as of this decision — don't assume a stack until the relevant
`CLAUDE.md` is updated with real values.
