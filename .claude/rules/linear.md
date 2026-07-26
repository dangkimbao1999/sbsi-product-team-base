# Linear (Issue Tracker) — MCP-based

This project uses the connected **Linear MCP tools** (no API key file, no
scripts) — read `.claude/skills/linear-workflow/SKILL.md` for the exact
tool-call sequence.

## Workspace — hardcoded to a single team, not a placeholder

This repo's Linear workflow always targets **one** workspace: **iambao**
(https://linear.app/iambao), single team **Iambao** (key `IAM`, id
`411d7932-6ab6-429f-8ffa-7a852cb87137`). Verified via `list_teams` /
`list_projects` on 2026-07-22 — see
`.claude/memory/linear-workspace-hardcoded.md`.

**Why hardcoded:** the connected `linear-server` MCP entry in `.mcp.json`
(`https://mcp.linear.app/mcp`) is Linear's generic remote server — it is
NOT workspace-specific by itself. Which workspace it actually talks to
depends entirely on which Linear account the individual user authenticated
with during their own OAuth connection. If a teammate's Claude Code is
connected to a *different* Linear account/workspace (a personal one, or a
different team's), every "shared" Linear action in this repo (issue
comments, state transitions, PR-linked nudges) would silently go somewhere
the rest of the team can't see it.

**MANDATORY verification before the first Linear MCP write action
(`save_issue`, `save_comment`, `save_project`, etc.) of a session:** call
`list_teams`. If the result is not exactly team **Iambao** (key `IAM`),
**stop** — do not create, comment on, or transition anything — and tell the
human their Linear MCP connection is pointed at the wrong workspace, so
they can reconnect it to `iambao` before continuing. Do not silently write
to whichever workspace happens to be connected; see
`.claude/rules/no-fallbacks.md`. Read-only lookups (`get_issue`,
`list_comments` for a session already linked via `.claude/.linear-link`)
don't need re-verification every time, but any write action does if the
workspace hasn't been checked yet this session.

## Key architectural fact: hooks cannot call MCP tools

MCP tools (`get_issue`, `list_issues`, `list_comments`, `save_comment`,
`save_issue`, `list_projects`, `get_project`, `list_teams`, `list_users` —
or whatever the connected Linear MCP server exposes) are only callable by
the model, mid-conversation. A `.claude/hooks/*.sh` script runs as a plain
shell process outside the agent loop and **cannot invoke them**.

Consequence: every "automatic" Linear update in this setup is actually a
**hook that nudges** (prints a reminder to stderr/stdout) at the right
moment, followed by the model actually calling the MCP tool in response.
This is reliable but not code-enforced the way the reference project's
script-based hooks were — if the model ignores a nudge, nothing fires.
Don't assume Linear stays in sync without the model acting on the nudges.

## Linear ref is OPTIONAL

Same principle as the reference project: not every PR/task needs a linked
Linear issue. Only use the flow below when you (the human) decide a piece
of work is worth tracking.

## Session ↔ issue linking

No custom script — just a plain file, gitignored:

- `.claude/.linear-link` — contains the issue identifier (e.g. `ENG-123`)
  the current session is working on. Empty/absent = not linked.
- To link: write the identifier into that file (ask the model to do it, or
  do it yourself).
- To unlink: delete the file.

## MANDATORY: read full issue context before acting

Before taking any non-trivial action on a linked issue — commenting,
transitioning state, referencing it in a PR — call `get_issue` AND
`list_comments` for that issue first. The issue's description alone is not
the full picture; comments carry decisions made after creation.

## Lifecycle checkpoints (nudge-only — see hooks below)

| Moment | Hook | What the model should do when it fires |
|---|---|---|
| `SessionStart` | `linear-session-start.sh` | If linked, call `get_issue` + `list_comments` to catch up before starting work |
| `PostToolUse ExitPlanMode` | `linear-plan-nudge.sh` | If linked, call `save_comment` with the approved plan's content |
| `gh pr create` | `linear-pr-nudge.sh` | If linked, call `save_comment` noting the PR URL; consider `save_issue` to move state to your team's "in review" equivalent |
| `gh pr ready <pr>` | `linear-pr-nudge.sh` | If linked, same as above |
| `gh pr merge <pr>` | `linear-pr-nudge.sh` | If linked, call `save_issue` to move state to your team's "done" equivalent |

## Task wrap-up — no hook, model must recognize the phrase

Unlike the checkpoints above, there's no hook for "sync this finished task
to Linear" — no shell script can deterministically detect an arbitrary
natural-language request. See the `linear-workflow` skill's "Wrapping up a
task" section for the two branches (create a new issue vs. comment on one
the user already wrote). Both branches only fire on an explicit instruction
("lưu vào Linear", "chốt lên Linear", ...) — never on a bare "xong
rồi"/"done", to keep the Linear ref genuinely optional.

## What NOT to invent

- Workspace/team is now known and hardcoded above (`iambao` / `Iambao` /
  `IAM`) — don't invent a different one. Workflow state names and label
  taxonomy are still NOT verified — don't hardcode those until you've
  actually called `list_issue_statuses` / `list_issue_labels` and seen what
  team Iambao really has.
- Don't build a PII-scanning layer or label-enforcement layer speculatively
  — the reference project's version existed because a real incident (PII
  leak into an issue) forced it. Add that kind of guardrail when you have a
  concrete reason, not preemptively.

## Load this rule when

- Before the first Linear MCP write action of a session (workspace
  verification).
- Linking/unlinking a session to a Linear issue.
- About to comment on, transition, or reference a linked Linear issue.
- A `linear-*` hook nudge fires in the transcript.
- The user explicitly asks to sync/save a finished task's results to Linear.

## Skip when

- Work has no Linear ref and isn't being tracked.
- Pure code reading/explanation with no tracked task involved.
