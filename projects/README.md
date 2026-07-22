# Projects

Per-project **knowledge**, one folder per SBSI product the team supports —
not code. Each SBSI product's actual codebase lives in its own dedicated
repo; this repo never hosts it. What lives here instead is the context
Claude Code (and teammates) need to produce good documents, design, scripts,
and demos *for* that product: domain vocabulary, current scope, tech stack,
where its issues are tracked, links to its real repo/design files.

## Current projects

- `research-hub/` — SBSI Research Hub, the crowdsourced investment-research
  platform (see `research-hub/CLAUDE.md`).
- `trading-web-app/` — SBSI's trading web/app product (see
  `trading-web-app/CLAUDE.md`).
- `websites/` — SBSI's marketing/corporate websites (see
  `websites/CLAUDE.md`).

## Conventions

- One folder per project, named for the product, holding at minimum a
  `CLAUDE.md` with that project's domain context.
- Never add application source code here. If a demo in `../demos/` outgrows
  its throwaway purpose and needs to become a real product, it moves out
  into its own repo — not into a folder here.
- Keep each project's `CLAUDE.md` current as you learn more about it (tech
  stack, domain model, where its Linear project lives) — stale placeholders
  are worse than short "not decided yet" notes.
- Root `CLAUDE.md`'s brokerage/trading domain model is generic context for
  reasoning about SBSI's business; it is not any one project's domain
  model. Each project's own domain model (if it has one) lives in its own
  `CLAUDE.md` here.
- Root `.claude/soul.md` is SBSI's default brand voice for any
  brand-representing content (docs, decks, design). If a project's voice
  deviates from that default (e.g. an analyst-toned research product vs. an
  aspirational marketing site), note the deviation in that project's own
  `CLAUDE.md` rather than forking `soul.md`.
