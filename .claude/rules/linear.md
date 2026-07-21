# Linear (Issue Tracker) — MCP-based

<Placeholder — fill in your team key/workspace name once known. This rule
ported the WORKFLOW from the reference project's Linear setup, but that
project used custom `bun scripts/linear/*.ts` hitting the Linear API
directly with a personal API key. This project instead uses the connected
**Linear MCP tools** (no API key file, no scripts) — read
`.claude/skills/linear-workflow/SKILL.md` for the exact tool-call sequence.>

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

## What NOT to invent

- Don't hardcode workflow state names, label taxonomy, or team keys here
  until you've actually called `list_teams` / `get_project` and seen what
  your workspace really has. The reference project's states (Backlog /
  Todo / In Progress / In Review / Blocked / Done) were specific to ITS
  team — yours may differ.
- Don't build a PII-scanning layer or label-enforcement layer speculatively
  — the reference project's version existed because a real incident (PII
  leak into an issue) forced it. Add that kind of guardrail when you have a
  concrete reason, not preemptively.

## Load this rule when

- Linking/unlinking a session to a Linear issue.
- About to comment on, transition, or reference a linked Linear issue.
- A `linear-*` hook nudge fires in the transcript.

## Skip when

- Work has no Linear ref and isn't being tracked.
- Pure code reading/explanation with no tracked task involved.
