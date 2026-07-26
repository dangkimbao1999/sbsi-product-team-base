# SBSI — Project Root

> **Fill this file in as your project grows.** Everything in angle brackets
> (`<LIKE_THIS>`) is a placeholder — replace it with real facts about your
> project.

## Project Context

This repo is **SBSI's product team workspace**. The team supports multiple
SBSI products at once — currently the **trading web/app**, **SBSI Research
Hub**, and SBSI's **websites** — and each needs its own specific domain
knowledge. This repo's job is to hold that shared knowledge, plus the work
the product team actually produces day to day: documents, design and
presentation work (graphics, slide decks), scripts to automate tasks, and
small demo projects to try out ideas.

**We do not code SBSI's products here.** Each product's real codebase lives
in its own dedicated repo. What lives here instead is: `.claude/` (shared
Claude Code rules/skills used across the team), `projects/` (per-product
domain knowledge — see `projects/README.md`), `scripts/` (automation/
tooling), and `demos/` (small, throwaway idea demos — see
`demos/README.md`). Design and document/slide work typically happens in
Figma / Google Drive via the connected integrations rather than as files
committed here — see `.claude/rules/figma-design.md`.

SBSI itself is a Vietnamese securities company (CTCK — Công ty Chứng khoán);
the trading-domain context in this file exists so rules/skills here can
reason about the business, not because this repo builds that platform.

See `projects/research-hub/CLAUDE.md`, `projects/trading-web-app/CLAUDE.md`,
and `projects/websites/CLAUDE.md` for what's known about each product so
far — several are still placeholders, filled in as the team learns more.

## Onboard

<If you have a setup/bootstrap script, name it here so every session runs it
first, e.g.:>

```bash
bash scripts/onboard.sh
```

<If you don't have one yet, delete this section — don't invent a script that
doesn't exist. Add it back once `scripts/onboard.sh` is real.>

## Tech Stack

<List the real stack. Keep it factual and current — this is the single most
useful section for Claude Code because it prevents guessed answers. Example
shape:>

- **Language**: <TypeScript / Python / Go / ...>
- **Package manager**: bun (always use `bun`/`bunx` — never `npm`/`npx`/`node`; enforced by `.claude/hooks/command-guard.sh`)
- **Runtime**: Bun
- **Server framework**: <...>
- **Database**: <...>
- **Frontend**: <...>
- **Mobile**: <...>
- **Cloud provider**: <AWS / GCP / Azure / none yet>
- **IaC**: <Pulumi / Terraform / CDK / none yet>
- **Issue tracker**: Linear (via connected MCP tools) — see `.claude/rules/linear.md`
- **Feature flags**: <Statsig / LaunchDarkly / none yet>

## Folder Structure

```
/<repo-root>
├── .claude/                 # Claude Code settings, rules, skills, hooks — the shared team config (primary content of this repo)
├── projects/                 # Per-product domain knowledge (NOT code) — see projects/README.md
│   ├── research-hub/        # SBSI Research Hub — see projects/research-hub/CLAUDE.md
│   ├── trading-web-app/     # SBSI trading web/app — see projects/trading-web-app/CLAUDE.md
│   └── websites/            # SBSI websites — see projects/websites/CLAUDE.md
├── scripts/                  # Product team work scripts (automation, one-off tooling) — see scripts/README.md
├── demos/                    # Throwaway demo generation, one folder per demo — see demos/README.md
└── ...
```

`projects/` holds knowledge, never application code — see
`projects/README.md` for the convention and how to add a new product folder.
Each major folder should get its own `CLAUDE.md` once it has enough
domain-specific rules to be worth splitting out. Don't create one
preemptively for an empty folder.

## Domain Model

<This section is reserved for your securities-trading domain (CTCK), the way
the reference project this template was cloned from had an
`insurance-schema.md` rule for its insurance domain. Don't fabricate a
schema — fill this in once you've read your actual database/API schema, and
keep it in sync as the schema evolves.

Once you have a real domain model, either summarize it inline here (short
version) or write `.claude/rules/domain-model.md` (detailed version, see the
placeholder already scaffolded there) and link it from here. Things a
securities-brokerage domain model typically needs to define — replace with
YOUR actual entities/terms, don't assume these names match your schema:

- **Core entity chain** — e.g. Customer/Investor -> Trading Account (cash /
  margin / derivatives) -> Order -> Execution/Trade -> Settlement. Don't skip
  levels the way claims-to-plans shortcuts caused bugs in the reference
  project.
- **Securities master** — how stocks/bonds/derivatives/fund certificates are
  identified (ticker, ISIN, internal security ID) and what attributes live
  where.
- **Order lifecycle & states** — order types (limit/market/stop/...),
  matching/execution states, cancellation/amendment rules.
- **Portfolio & cash balance** — how holdings and available cash/buying
  power are computed (cached vs. runtime-derived — the reference project's
  insurance domain deliberately computed claim balances at runtime rather
  than caching them; decide your own tradeoff and document it here).
- **Corporate actions** — dividends, stock splits, rights issues, and how
  they adjust holdings/cost-basis.
- **Settlement & clearing** — T+n cycles, custodian/depository integration
  (e.g. VSD in Vietnam), failed-settlement handling.
- **Compliance / KYC / AML** — customer onboarding, suitability checks,
  position/exposure limits, regulatory reporting obligations specific to
  your market and regulator (e.g. SSC/UBCKNN in Vietnam).
- **Market data** — real-time quote/order-book feed source(s), reference
  data (trading calendar, price/volume limits, index membership).
- **Naming/enum conventions** — e.g. CONSTANT_CASE order sides/statuses,
  currency/quantity precision rules — whatever your actual schema uses.>

This root domain model covers the brokerage's core trading entities only.
Individual products with their own distinct domain (e.g.
`projects/research-hub/` — content/research entities, not trading entities)
document their domain model in their own `CLAUDE.md` instead of here.

## Universal Rules

### Working Style

See `.claude/rules/working-style.md` — bias toward caution over speed,
simplicity first, surgical changes, goal-driven execution (RED/GREEN/REFACTOR).
This rule is generic and should NOT need editing.

### Brainstorm Before Any Deliverable

Before producing any document, demo app, or design/mockup, clarify what
the output specifically should be — unless the user already fully defined
it in their prompt. See `.claude/rules/brainstorm-before-deliverables.md`
and the `brainstorming` skill.

### Testing — Red/Green TDD (Mandatory)

All code changes MUST follow red/green TDD: RED (failing test first) ->
GREEN (minimum code to pass) -> REFACTOR. See `.claude/rules/tdd.md` and the
`tdd` skill.

### No Fallbacks — Fail Fast, Fail Loud

Never implement silent fallback/degraded-mode logic. See
`.claude/rules/no-fallbacks.md` and `.claude/rules/no-silent-fallbacks.md`.

### Backward Compatibility

<Delete this section if you don't yet have external consumers (partner SDKs,
public APIs, other teams' services) whose breakage would matter. Once you do,
un-delete and adapt `.claude/rules/backward-compatibility.md`.>

### Secrets & Environment Variables

`.env` files are local-only, gitignored, and generated — never hand-edited
with real secrets, never committed. See `.claude/rules/env-secrets.md`.
<Fill in where your secrets actually live once you pick a secret store — AWS
SSM, GCP Secret Manager, Doppler, 1Password, whatever it is.>

### Git Workflow

Always work on feature branches (`feat/`, `fix/`, `chore/`) — never commit to
`main` directly. Use the `EnterWorktree` tool to create worktrees. Typecheck
before committing. Create a PR after every task; PRs open as **draft** by
default (enforced by a hook) and are promoted to ready only with explicit
human consent. See `.claude/rules/git-workflow.md` and the `git-workflow`
skill for the full procedure.

### Claude Code Conventions

When persisting project knowledge, choose the right format: a short always-on
reminder goes in `.claude/rules/`, detailed on-demand procedure goes in
`.claude/skills/<name>/SKILL.md`, deterministic enforcement goes in
`.claude/hooks/`. See `.claude/rules/claude-code-conventions.md`.

## Code Review Extended Rules

<As your project grows, list domain-specific rule files here the way the
reference project does — e.g. "check the PR diff against
`.claude/rules/no-fallbacks.md`, `.claude/rules/performance.md`,
`.claude/rules/domain-model.md`, `.claude/rules/<your-other-domain-rule>.md`".
Empty for now — add rules here as you write them.>

## Issue Tracker (Linear)

Linear is connected via MCP (no custom scripts, no API key file — see
`.claude/rules/linear.md` and the `linear-workflow` skill). A Linear ref is
always OPTIONAL. Because hooks cannot call MCP tools directly, the
PR/plan/session lifecycle hooks only NUDGE — the model still has to act on
each nudge by calling the connected Linear MCP tool itself.

## Shared Memory

Before starting any work, read `.claude/memory/MEMORY.md` for shared project
memories — feedback, project context, user preferences, and lessons learned
across sessions. These memories are committed to git and apply to everyone
working in this repo. See `.claude/memory/MEMORY.md` for the current index
and instructions on how entries get added.

## Soul & Voice

This repo's whole job includes producing documents, design, and
presentations — much of it brand-representing or stakeholder-facing. Read
`.claude/soul.md` before generating any such content (marketing copy,
investor-facing decks, UI copy, design work) and keep it filled in with
SBSI's real brand guidelines as they become known — it's still a
placeholder as of this writing. If a specific product's voice deviates from
the SBSI-wide default in `.claude/soul.md` (e.g. Research Hub reads more
analyst-toned than a marketing site), note that deviation in that product's
own `projects/<name>/CLAUDE.md` rather than forking `soul.md`.

**Files Claude Code auto-loads for instructions:**
- `CLAUDE.md` at project root and every subdirectory in the working path
- `~/.claude/CLAUDE.md` for user-level personal preferences
- `.claude/settings.json` and `.claude/settings.local.json` for project/user settings
- `.claude/rules/` for always-on rule reminders
- `.claude/skills/` for on-demand detailed procedures
