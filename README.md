# SBSI Product Team Workspace

Shared workspace for **SBSI**'s (a Vietnamese securities brokerage, CTCK)
product team — Claude Code rules/skills used across the team, work scripts,
and on-demand demo generation. This repo intentionally stays light on code;
it is not the home for SBSI's production trading-system codebases.

## What's here

- `.claude/` — Claude Code configuration (rules, skills, hooks, agents,
  shared memory) used across the team when working with Claude Code. This
  is the primary content of this repo.
- `scripts/` — product team work scripts. See `scripts/README.md`.
- `demos/` — throwaway demo generation, one folder per demo. See
  `demos/README.md`.
- `apps/research-hub/` — SBSI Research Hub, a crowdsourced investment
  research platform for the Vietnam market, built as a user-acquisition
  funnel into SBSI's trading products. An existing real sub-project that
  predates this workspace framing; see `apps/research-hub/CLAUDE.md`.

## Who this is for

SBSI's product/engineering team, and any AI coding agents (Claude Code)
assisting them. See `CLAUDE.md` for full project context, tech stack, and
working conventions.
