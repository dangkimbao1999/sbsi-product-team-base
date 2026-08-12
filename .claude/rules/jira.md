# Jira (Atlassian Rovo MCP) — SAFe / PO's real tracker

The Product Owner runs this repo's PO Requirement Refinement workflow
inside a **SAFe (Scaled Agile)** process, and the real issue tracker is
**Jira** (not Linear — `.claude/rules/linear.md` / `linear-workflow` stay
in the repo but are not necessarily this PO's tracker of record; don't
assume a Final Backlog should sync to Linear just because that
integration existed first).

## Connection — two mechanisms, pick based on where you're running

- **Cowork session (native connector)** — the Atlassian Rovo connector is
  registered in Cowork's connector registry (`mcp-registry`). If its tools
  aren't connected yet, call `mcp__mcp-registry__suggest_connectors` with
  the Atlassian/Jira/Rovo directory entry so the user gets a Connect
  button; this is the native mechanism, prefer it over anything below when
  running in Cowork.
- **Claude Code CLI against this repo** — `.mcp.json` has an
  `"atlassian-rovo"` entry (`type: http`, `url:
  https://mcp.atlassian.com/v1/mcp`), same shape as the existing
  `linear-server` entry. Each developer adds `"atlassian-rovo"` to their
  own `enabledMcpjsonServers` in `.claude/settings.local.json` (personal,
  gitignored) to enable it locally, then authorizes via `/mcp` — same
  pattern documented in `.claude/rules/stitch-design.md` for the `stitch`
  server.

## Auth is OAuth, interactive-only

The Atlassian Rovo MCP server uses OAuth 2.1 — there is no API key file
and no way to complete the authorization flow from a non-interactive
session. If tools under this server aren't callable yet, tell the human to
authorize it themselves (via claude.ai connector settings in Cowork, or
`/mcp` in an interactive Claude Code CLI session) rather than asking them
for a token or callback URL.

## What this rule does NOT know yet (verify before relying on it)

Unlike `.claude/rules/linear.md`, this rule has **not** been verified
against a live connection yet — no site URL, project key, issue type
scheme (Epic/Story/Task/Sub-task or a SAFe-specific scheme), or workflow
state names have been confirmed. **Do not hardcode any of these** the way
`linear.md` hardcodes the `iambao`/`IAM` workspace — call whatever
resource-listing tool the connected session exposes (e.g. something like
`getAccessibleAtlassianResources` / `atlassianUserInfo` — confirm the
actual tool name once connected, don't assume) before the first write
action, and ask the PO to confirm the target site + project if more than
one is accessible.

## Session ↔ issue linking

Same plain-file pattern as Linear, kept separate so a session can be
linked to a Jira issue and a Linear issue independently if that ever
happens: `.claude/.jira-link` (gitignored, contains the issue key, e.g.
`SAFE-123`). Empty/absent = not linked.

## Load this rule when

- The user mentions Jira, Rovo, Confluence, or SAFe backlog/PI-planning
  tracking.
- About to call any `atlassian-rovo` / Rovo MCP tool.
- Deciding whether a finished PO Requirement Refinement backlog should
  sync to a tracker, and it's unclear whether that tracker is Jira or
  Linear — ask, don't guess.

## Skip when

- Work has no Jira ref and isn't being tracked there.
- The task clearly belongs to Linear (explicitly named by the user).
