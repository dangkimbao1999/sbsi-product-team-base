# Stitch Design Integration

[Google Stitch](https://stitch.withgoogle.com) generates UI screens from
text prompts. This repo uses two separate pieces — keep them distinct:

- **MCP server** (`.mcp.json` -> `"stitch"`) — the live connection Claude
  Code calls tools through. Runs
  [`@_davideast/stitch-mcp`](https://github.com/davideast/stitch-mcp) via
  `bunx`, which proxies the official Stitch API and layers a few virtual
  tools on top of the upstream ones: `build_site`, `get_screen_code`,
  `get_screen_image`. This is repo-tracked, committed config — every
  developer gets the same server definition.
- **Skill content** —
  [`google-labs-code/stitch-skills`](https://github.com/google-labs-code/stitch-skills),
  a set of `stitch::*`-prefixed Agent Skills (`stitch::generate-design`,
  `stitch::code-to-design`, `stitch::react-components`, ...). This is
  installed as a **global, per-developer Claude Code plugin** (see below)
  — NOT vendored into this repo, the same category as the TalkToFigma
  bridge in `.claude/rules/figma-design.md`. This repo's own
  `design-request-intake` / `stitch-workflow` skills still own the intake
  step (Linear + GitHub context, platform confirmation) before handing off
  to whichever `stitch::*` skill fits the task.

There is no web-automation fallback needed or supported here; always go
through the MCP tools.

## One-time per-developer setup (not scripted — interactive)

### 1. MCP server auth

Auth steps can't be run on your behalf; run them yourself (suggest the
`! <command>` prefix in a Claude Code session):

- **Recommended — guided wizard**:
  `bunx @_davideast/stitch-mcp@latest init` — walks through client
  selection (pick Claude Code), auth mode (API key is simplest, no gcloud
  needed), transport, and writes your MCP client config for you.
- **Manual gcloud** (if you already run gcloud for other tools):
  ```bash
  gcloud auth application-default login
  gcloud config set project <PROJECT_ID>
  gcloud beta services mcp enable stitch.googleapis.com --project=<PROJECT_ID>
  ```
  then set `STITCH_USE_SYSTEM_GCLOUD=1` in the `stitch` entry's `env`
  block via your local `.claude/settings.local.json` override (gitignored)
  so the proxy uses your system gcloud instead of its bundled one.
- Either way, add `"stitch"` to the `enabledMcpjsonServers` array in your
  local `.claude/settings.local.json` (gitignored — mirrors how
  `chrome-devtools`/`TalkToFigma`/`linear-server` are already enabled
  there).
- Verify: `bunx @_davideast/stitch-mcp@latest doctor`, then
  `ToolSearch("select:mcp__stitch")` should return the server's tools.

### 2. Skill plugin (stitch-skills)

```bash
bunx plugins add google-labs-code/stitch-skills --scope project --target claude-code
```

Despite `--scope project`, this third-party `plugins` CLI (unrelated to
`stitch-skills`' own maintainers) records the enablement in your
**user-level** `~/.claude/settings.json` (`enabledPlugins`), not anything
project-scoped or git-tracked — confirmed 2026-07-28. Nothing this command
writes belongs in this repo's git history; each developer runs it once on
their own machine, and it isn't inherited by teammates automatically.

## The workflow

When a request is about design or generating a new screen:

1. **Intake** — follow the `design-request-intake` skill: Linear context,
   GitHub/codebase context, and platform confirmation (never default or
   guess `deviceType` silently) all happen there, shared with the Figma
   flow. Do this before calling any Stitch generation tool.
2. **Build the prompt** — follow the `stitch-workflow` skill's template
   (purpose, platform, page structure). Don't hand Stitch the user's raw
   one-liner unedited.
3. **Project** — find or create the Stitch project for the target app
   (`list_projects` / `create_project`). One Stitch project per app (e.g.
   "SBSI Research Hub").
4. **Generate** — call `generate_screen_from_text` (or `edit_screens` for
   revisions) with the confirmed `deviceType`.
5. **Save output** — download the HTML/screenshot from the response's
   `outputComponents` into `.stitch/designs/<app>/<screen-slug>/`
   (gitignored scratch — nothing here is auto-committed).
6. **Report back** — show the AI's description/suggestions and the
   screenshot to the user. If Linear-linked, nudge to `save_comment` a
   short summary and the local output path — not a raw attachment
   upload.

See `.claude/skills/design-request-intake/SKILL.md` for step 1 and
`.claude/skills/stitch-workflow/SKILL.md` for the exact prompt template
and MCP call sequence (steps 2–5).

## Load this rule when

- The user asks to design, mock up, or generate a new screen/UI.
- The user mentions Stitch or `stitch.withgoogle.com`.
- A `mcp__stitch__*` tool call is about to be made.
- A `stitch::*` skill (from the `stitch-skills` plugin) is available and
  relevant, e.g. `stitch::code-to-design`, `stitch::react-components`.

## Skip when

- No design-generation request is in play.
- The task is implementing/coding an already-designed screen (no new
  design generation needed).
