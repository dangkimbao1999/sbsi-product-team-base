# SBSI — Project Root

> **Fill this file in as your project grows.** Everything in angle brackets
> (`<LIKE_THIS>`) is a placeholder — replace it with real facts about your
> project.

## Project Context

This is the monorepo for **SBSI**, a Vietnamese securities brokerage (CTCK).
The core business is trading platform infrastructure — order management /
execution, portfolio & cash account management, market data distribution,
customer trading app (web + mobile), and regulatory/compliance reporting
(systems: OMS, core trading engine, market data feed handler, back-office/
settlement, customer portal — none built out in this repo yet).

The first concrete sub-project in this monorepo is **SBSI Research Hub**
(`apps/research-hub/`) — a crowdsourced financial-research and investment-idea
platform for the Vietnam market, functioning as a top-of-funnel product that
attracts individual investors, analysts, and traders and channels them into
SBSI's trading products. It is not itself a trading system; see
`apps/research-hub/CLAUDE.md` for its full project context and domain model.

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

This repo is a monorepo. `apps/` holds independently deployable sub-projects;
add sibling folders there as new SBSI systems (OMS, core trading engine,
back-office/settlement, customer trading portal, etc.) come online — don't
create them preemptively.

```
/<repo-root>
├── .claude/                # Claude Code settings, rules, skills, hooks (this scaffold)
├── apps/
│   └── research-hub/       # SBSI Research Hub — crowdsourced research & investor-acquisition platform — see apps/research-hub/CLAUDE.md
├── packages/                # Shared packages (once >1 app needs to share code)
├── scripts/                  # Project-wide scripts (onboarding, CI helpers)
└── ...
```

Each major folder should get its own `CLAUDE.md` once it has enough
domain-specific rules to be worth splitting out. Don't create one preemptively
for an empty folder.

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
Sub-projects with their own distinct domain (e.g. `apps/research-hub/` —
content/research entities, not trading entities) document their domain model
in their own `CLAUDE.md` instead of here.

## Universal Rules

### Working Style

See `.claude/rules/working-style.md` — bias toward caution over speed,
simplicity first, surgical changes, goal-driven execution (RED/GREEN/REFACTOR).
This rule is generic and should NOT need editing.

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

<If this project has user-facing product surface (UI copy, branding, colors),
read `.claude/soul.md` before generating any user-facing content and fill it
in with your actual brand guidelines. If this is a backend-only / internal
tool, delete this section and `.claude/soul.md`.>

**Files Claude Code auto-loads for instructions:**
- `CLAUDE.md` at project root and every subdirectory in the working path
- `~/.claude/CLAUDE.md` for user-level personal preferences
- `.claude/settings.json` and `.claude/settings.local.json` for project/user settings
- `.claude/rules/` for always-on rule reminders
- `.claude/skills/` for on-demand detailed procedures
