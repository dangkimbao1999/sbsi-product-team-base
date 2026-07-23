---
name: stitch-workflow
description: Generate, edit, or vary UI screens with the Stitch MCP server, after gathering Linear + GitHub context. Use when a request is about designing/mocking up/generating a new screen, or a `stitch-design` rule trigger fires.
---

# Stitch Workflow

This project has no bundled Stitch plugin (unlike the community
`stitch-skills`/`stitchkit` repos) — it talks directly to whichever
`stitch` MCP server is configured in `.mcp.json`. Tool names below are the
underlying API's names; the actual callable name is prefixed by the MCP
connector (confirm with `ToolSearch("select:mcp__stitch")` before first
use — don't assume the prefix).

## 0. Gather context first

Before writing any prompt: follow `.claude/rules/stitch-design.md`'s
workflow steps 1–2 (Linear via `get_issue`/`list_comments`, GitHub via
existing screens/components/PRs). Skipping this produces a generic Stitch
prompt with none of the product/design context that made the request
worth tracking in the first place.

## 1. Platform check

If the request doesn't specify **MOBILE**, **DESKTOP**, or **TABLET**,
stop here and ask the user via `AskUserQuestion` before calling any
generation tool. Do not guess based on the app's likely primary platform
— confirm it. Skip the ask only when:

- The request explicitly names the platform ("mobile app screen",
  "desktop dashboard"), or
- You're editing an existing screen — its `deviceType` is already fixed;
  call `get_screen` to confirm rather than re-asking.

## 2. Build the prompt

### New screen template

```
[Overall purpose and user intent of the page]

PLATFORM: [Mobile/Desktop/Tablet], [confirmed in step 1]

PAGE STRUCTURE:
1. Header: [navigation and branding]
2. Primary Content Area: [detailed component breakdown — be specific:
   name components, not vague adjectives]
3. Secondary/Supporting Content: [sidebars, related content, etc.]
4. Footer/Actions: [links, primary/secondary CTAs]
```

Ground each section in what you learned in step 0 — actual product
terminology from the Linear issue, actual component names already used
elsewhere in the target app, not generic placeholders.

### Edit template

Be specific about location, change, and (for edits only — not new-screen
generation) exact values:

```
Change the [element] in the [section] to [new value/behavior].
Add a [new element] next to [existing element] with [content/behavior].
```

## 3. MCP call sequence

1. `list_projects` — find the project for the target app. If none
   exists, `create_project` (name it after the app, e.g. "SBSI Research
   Hub").
2. Platform check (step 1 above) if not already resolved.
3. `generate_screen_from_text` with the enhanced prompt + confirmed
   `deviceType`, using the target project. For edits, call
   `edit_screens` against the existing screen instead.
4. Read the response's `outputComponents` — it carries a text
   description, suggestions, and HTML/screenshot URLs.
5. Download the HTML and screenshot into
   `.stitch/designs/<app>/<screen-slug>/` (create the directory if
   needed; gitignored, so nothing here needs cleanup before committing
   elsewhere).
6. Present the description + suggestions + screenshot back to the user.

## 4. Iterating

- **Single revision**: `edit_screens` with a targeted prompt (see Edit
  template above). No need to re-ask platform — it's fixed to the screen
  being edited.
- **Variants**: call `generate_screen_from_text` (or `edit_screens`)
  multiple times with explicit, named deltas ("dark mode", "high-density
  layout", "warm color variant") — never "give me some options" run blind
  N times with no stated axis of variation. Save each under a sibling
  slug in `.stitch/designs/<app>/`.

## Other available tools (use as needed, not part of the default flow)

- `extract_design_context` — pull font/color/layout "design DNA" from an
  existing screen, useful before generating a new screen that should
  match it.
- `fetch_screen_code` / `fetch_screen_image` — re-download an existing
  screen's HTML/screenshot without regenerating it.
- `list_screens` / `get_screen` / `get_project` — inspect existing state
  before deciding whether to create new vs. edit existing.
