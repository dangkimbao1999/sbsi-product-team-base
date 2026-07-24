# Stitch Design Integration

[Google Stitch](https://stitch.withgoogle.com) generates UI screens from
text prompts. Unlike Figma, Stitch has no plugin/bridge model — the only
way in is the `stitch` MCP server (`.mcp.json`), backed by Google Cloud's
`stitch.googleapis.com` API. There is no web-automation fallback needed or
supported here; always go through the MCP tools.

## One-time per-developer setup (not scripted — interactive)

`gcloud auth` steps can't be run on your behalf; run them yourself
(suggest the `! <command>` prefix in a Claude Code session):

1. Create or select a GCP project and enable the Stitch API on it:
   `gcloud config set project <PROJECT_ID>` then
   `gcloud beta services mcp enable stitch.googleapis.com`.
2. `gcloud auth application-default login`.
3. Export `GOOGLE_CLOUD_PROJECT=<PROJECT_ID>` in your shell profile (not
   committed — this is per-developer, like the rest of your gcloud
   config).
4. Add `"stitch"` to the `enabledMcpjsonServers` array in your local
   `.claude/settings.local.json` (gitignored — mirrors how
   `chrome-devtools`/`TalkToFigma`/`linear-server` are already enabled
   there).
5. Verify: `ToolSearch("select:mcp__stitch")` should return the server's
   tools once the above is in place.

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

## Skip when

- No design-generation request is in play.
- The task is implementing/coding an already-designed screen (no new
  design generation needed).
