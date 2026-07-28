# Figma Design Integration

Two separate Figma MCP integrations are available. Pick based on the task —
they solve different problems and have different setup costs.

## Before generating a brand-new design

If the task is "create/generate a new design" (not editing an existing
file the human already has open), first complete the
`design-request-intake` skill — Linear context, GitHub/codebase context,
and platform confirmation (never default/guess the target platform
silently). This is the same intake step used by the Stitch flow
(`.claude/rules/stitch-design.md`) — see that skill for the full
procedure. Skip it for pure edits to an already-identified file/frame,
where the platform and context are already fixed by what's open.

## Color tokens — SBSI design system

Follow `.claude/rules/design-system.md` for every color decision (semantic
role tokens, Light+Dark, price-color convention, chart palettes). Before
picking a color by hand from `.claude/design-system/tokens-SBSI-design-system-v1.json`,
try resolving it live first: `search_design_system` /
`get_variable_defs` (official Figma MCP) or `get_styles` (TalkToFigma) can
pull directly from SBSI's actual Figma library/variables if it's connected
in the target file — that resolves aliases correctly, which the static
JSON export can't fully guarantee (see the "Known gap" section in
`.claude/design-system/README.md`). Fall back to the JSON file only when
the live library isn't reachable.

## 1. Official Figma MCP (`mcp__claude_ai_Figma__*`)

Connected account-level integration, already authenticated (verify with
`whoami` if anything seems off). No local process required.

- Use for: generating new designs/files from scratch or from code
  (`use_figma`, `create_new_file`), reading existing files into code
  (`get_design_context`, `get_screenshot`, `get_metadata`), design systems
  (`search_design_system`, `get_variable_defs`), Code Connect.
- **MANDATORY**: call `mcp__claude_ai_Figma__get_figma_skill` and read the
  `/figma-use` skill (or its `skill://figma/figma-use/SKILL.md` fallback)
  before ever calling `use_figma`.
- Default choice when the task is "create/generate a design" and there's no
  need to manipulate a specific file a human already has open. Run the
  intake step above first.

## 2. TalkToFigma (`mcp__TalkToFigma__*`) — live plugin bridge

Node-level read/write access to whatever file is currently open in the
user's Figma desktop app. Requires three things to be running/connected
simultaneously — **this does not work out of the box**, unlike #1.

**One-time setup already done** (2026-07-22): bridge repo cloned to
`~/.claude/tools/cursor-talk-to-figma-mcp` (outside this project repo — it's
a personal dev tool, not project code, so it's not tracked in this repo's
git history).

**Per-session steps to (re)establish the connection:**

1. Ensure the WebSocket bridge is running on port 3055:
   ```bash
   cd ~/.claude/tools/cursor-talk-to-figma-mcp && bun run src/socket.ts
   ```
   Run this in the background (`run_in_background: true`). If a previous
   session's bridge is still alive, this step can be skipped — check first
   with `mcp__TalkToFigma__get_document_info`; a "Not connected to Figma"
   error means either the bridge isn't running or no channel is joined yet.
2. Ask the human to open Figma desktop, run the **"Cursor MCP Plugin"**
   (community plugin, id `1485687494525374295` —
   https://www.figma.com/community/plugin/1485687494525374295/cursor-talk-to-figma-mcp-plugin)
   inside the file they want edited. The plugin UI displays a channel code.
3. Call `mcp__TalkToFigma__join_channel` with that code.
4. Verify with `mcp__TalkToFigma__get_document_info` before making changes.

The channel code is per-plugin-session — it changes every time the human
re-runs the plugin, so step 2-3 repeat each time the bridge/plugin
connection drops (e.g. Figma file closed, plugin stopped, bridge process
killed). The bridge process itself (step 1) does NOT need to restart unless
it was actually killed.

- Use for: editing a specific file the human already has open — bulk text
  replacement, styling existing nodes, instance override propagation,
  annotations, FigJam connectors from prototype reactions.

## Load this rule when

- The user asks to create, generate, edit, or sync anything in Figma.
- A `mcp__claude_ai_Figma__*` or `mcp__TalkToFigma__*` tool call is about to
  be made.

## Skip when

- No Figma-related task is in play.
