# SBSI Product Team Workspace

Shared workspace for **SBSI**'s (a Vietnamese securities company, CTCK —
Công ty Chứng khoán) product team. The team supports several SBSI products at once — currently
the **trading web/app**, **Research Hub**, and SBSI's **websites** — using
Claude Code as a teammate. This repo is where that collaboration lives:
shared Claude Code rules/skills, per-product knowledge, work scripts, and
on-demand demos.

**This repo does not hold any SBSI product's real codebase.** Each product
is built in its own dedicated repo. What's here is knowledge and
tooling — not application source code.

## What's here

- `.claude/` — Claude Code configuration (rules, skills, hooks, agents,
  shared memory) used across the whole team. This is the primary content of
  this repo.
- `projects/` — one folder per SBSI product, holding domain knowledge only
  (never code): what the product is, its domain model, its tech stack, where
  its issues are tracked. See `projects/README.md`.
- `scripts/` — product team work scripts (automation, one-off tooling). See
  `scripts/README.md`.
- `demos/` — throwaway demo generation, one folder per demo, for trying out
  an idea quickly. See `demos/README.md`.

## Who this is for

SBSI's product team, and Claude Code (or any AI coding agent) assisting
them. See `CLAUDE.md` for full project context, tech stack, and working
conventions.

## How to use this repo

### 1. Start a Claude Code session here

Open a terminal in this repo and run Claude Code as usual. It auto-loads
`CLAUDE.md`, everything in `.claude/rules/`, and `.claude/memory/MEMORY.md`
— you don't need to paste context in manually. If you're picking up a task
from a previous session, just describe it; Claude will re-read shared
memory for prior decisions and feedback.

### 2. Point Claude at the right product context

Before asking for anything product-specific (a doc, a script, a demo, an
analysis), mention which product it's about. Claude will read the matching
`projects/<name>/CLAUDE.md` for domain vocabulary and scope:

- `projects/research-hub/` — Research Hub
- `projects/trading-web-app/` — trading web/app
- `projects/websites/` — SBSI websites

If a project's `CLAUDE.md` is still a placeholder (marked with `<...>`),
that's expected — fill it in as the team learns more, or ask Claude to
update it after a working session so the next session starts smarter. Don't
let it go stale: an out-of-date placeholder is worse than an honest "not
decided yet."

Adding a new product the team starts supporting: create
`projects/<name>/CLAUDE.md` following the shape of the existing ones (see
`projects/README.md`), rather than waiting for someone to set it up later.

### 3. Producing documents, design, and presentations

This repo stores the **context and rules that make Claude good at
generating these** — brand voice, product knowledge, design-system
conventions. The **output artifacts themselves** (the actual doc, deck, or
design file) live in their native tools, not committed here:

- **What informs the output, kept in this repo**: `.claude/soul.md` (SBSI's
  brand voice — read before any brand-representing content), the relevant
  `projects/<name>/CLAUDE.md` (which product this is for and its
  scope/vocabulary, including any voice deviation from `soul.md`), and
  `.claude/rules/figma-design.md` (how to drive Figma correctly).
- **Design work (Figma)** — see `.claude/rules/figma-design.md`. Claude can
  generate new designs, read/edit an existing Figma file you have open, or
  turn a Figma file into a spec/screenshot.
- **Docs and slides (Google Drive)** — the Google Drive integration is
  available for reading/writing docs and slides directly.
- **Quick shareable write-ups** — for something that doesn't need Figma or
  Drive (a comparison table, a mini dashboard, a one-off explainer), ask
  Claude to publish it as an Artifact instead of a repo file.

### 4. Writing a script

Ask Claude for the automation you need (e.g. "write a script that pulls
this week's Linear issues into a summary"). Scripts land in `scripts/`,
one file per task, following `scripts/README.md`'s conventions. Even though
scripts are small, the repo's TDD and no-fallbacks rules still apply — see
`.claude/rules/tdd.md` and `.claude/rules/no-fallbacks.md`.

### 5. Building a demo

For "let's see if this idea works" — a quick prototype, a mockup, a proof
of concept — ask Claude to build it under `demos/<demo-name>/`, following
`demos/README.md`'s conventions (each demo is self-contained). If a demo
proves out and needs to become a real, ongoing product, it graduates into
its own dedicated repo — it does not grow in place here.

### 6. Tracking work in Linear (optional)

Linear is connected via MCP — no API keys or scripts needed. Linking a
session to an issue is optional; do it when a piece of work is worth
tracking. See `.claude/rules/linear.md` and the `linear-workflow` skill.

### 7. GitHub vs. Linear — where does domain knowledge, requirements, and design decisions go?

Pick based on the lifespan of the information, not which tool is more
convenient in the moment:

| Goes in... | Use for | Why |
|---|---|---|
| **GitHub** — `projects/<name>/CLAUDE.md` | Durable, "always true" domain knowledge: what a product is, its vocabulary/entity model, its scope, its tech stack | Auto-loads into every Claude Code session and is version-controlled/diffable — Linear issues don't auto-load and get buried once closed |
| **Linear** | Requirements and design decisions tied to one specific piece of work: a feature spec, acceptance criteria, "why we chose X" during that ticket's discussion | That's what issues/comments/status already exist for — it's the work-tracking trail |
| **GitHub** — `.claude/memory/` | A decision made *during* Linear-tracked work that turns out to be durable/repo-wide (affects more than that one ticket) | Bridges the gap: writing it back here means it survives after the ticket closes, instead of only being findable by re-reading old Linear comments |

When in doubt: if it should still be true and worth knowing a year from now
regardless of any single ticket's status, it belongs in GitHub (`projects/`
or `.claude/memory/`). If it's scoped to getting one piece of work done
right now, it belongs in Linear.

### 8. Contributing changes back to this repo

Same git discipline as any codebase, even though most of what's here is
docs/config rather than app code:

- Work in a feature branch/worktree (`feat/`, `fix/`, `chore/`) — never
  commit to `main` directly. Use the `EnterWorktree` tool.
- Open a PR when a task is done; PRs default to **draft** and get promoted
  to ready only with explicit human sign-off.
- See `.claude/rules/git-workflow.md` and the `git-workflow` skill for the
  full procedure.

### 9. Growing the team's shared Claude knowledge

When you (or Claude) learn a convention, correction, or durable fact worth
keeping for next time, it belongs in one of:

- `.claude/rules/` — short always-loaded reminders
- `.claude/skills/` — detailed on-demand procedures
- `.claude/memory/` — durable facts/decisions/feedback (committed, shared
  team-wide; see `.claude/memory/MEMORY.md`)
- `.claude/agents/` — a dispatchable specialist for a bounded, recurring
  kind of task

See `.claude/rules/claude-code-conventions.md` for which one fits.
