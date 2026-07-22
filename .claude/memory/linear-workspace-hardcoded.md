---
name: linear-workspace-hardcoded
description: This repo's Linear workflow is hardcoded to a single workspace (iambao / team Iambao / key IAM) — verify before writing, don't trust whatever workspace happens to be OAuth-connected
metadata:
  type: project
---

This repo's Linear integration always targets **one** workspace:
**iambao** (https://linear.app/iambao), single team **Iambao** (key `IAM`,
id `411d7932-6ab6-429f-8ffa-7a852cb87137`). Confirmed via `list_teams` (only
team returned) and `list_projects` (project URLs under `linear.app/iambao/`)
on 2026-07-22. Full policy in `.claude/rules/linear.md`.

**Why:** The human owns this Linear workspace and wants it to be the
team's single shared workspace — every teammate using this repo's Linear
workflow should land in the same place. The `linear-server` MCP entry in
`.mcp.json` points at Linear's generic remote server
(`https://mcp.linear.app/mcp`), which is NOT workspace-specific — it
authenticates per-user via OAuth, so which workspace it actually reaches
depends on which Linear account each teammate connects with. A repo config
file cannot force that connection to a specific workspace; the only
reliable way to catch a mismatch is to verify at write-time and fail loud
if the wrong workspace is connected — see `.claude/rules/no-fallbacks.md`.

**How to apply:** Before any Linear MCP write action in a session that
hasn't verified yet, call `list_teams` and confirm the result is exactly
team Iambao (key IAM). If a teammate's connection resolves to a different
team/workspace, stop and tell them to reconnect — don't write to whatever
workspace happens to be connected. See
[[linear-research-hub-project]] for the one existing tracked project in
this workspace.
