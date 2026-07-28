# SBSI Design System — Colors

SBSI has a real design token source now:
`.claude/design-system/tokens-SBSI-design-system-v1.json` (structure and
resolution notes in `.claude/design-system/README.md`). It applies to
**every** SBSI product this repo touches — never invent arbitrary hex/RGB
for a UI element, chart, or piece of brand-facing design when a token
exists for that role.

## Rules

- **Use semantic role tokens, not raw scale steps.** Pick `Text.Primary` /
  `BG.Surface.Secondary` / `Stroke.Danger` etc. over reaching for
  `Gray.900` or `Red.600` directly — same principle as referencing a
  codebase's design-token variables instead of literal hex.
- **Support both Light and Dark.** Every `SBSI color/*` role exists in both
  modes with mode-appropriate values — don't hardcode only one and call it
  done, even if the request only mentions one mode; ask which mode(s) are
  in scope if unclear (see `design-request-intake`).
- **Reuse the price-color convention for any trading-price UI.**
  `Text.Price.*` / `Icon.Price.*` (Up/Down/Fixed/Ceiling/Floor) already
  encode Vietnam's stock-exchange price-band colors — see
  `.claude/design-system/README.md` for the mapping. Don't invent a
  different red/green scheme for price deltas.
- **Charts/dataviz for SBSI products**: use the `Chart` (single swatch per
  family) and `Pie_Chart` (5-step ramp per family) tokens instead of the
  generic `dataviz` skill's placeholder palette — that skill's own
  instructions say to swap its palette for the real brand one; this is it.
- **Don't trust `Basic color/Color Scale`** as brand-authoritative without
  confirming first — see the "Known gap" and hue-mismatch notes in
  `.claude/design-system/README.md`. It's plausibly a legacy palette left
  in the export.
- **Prefer live Figma resolution over hand-resolving the static JSON**
  when a concrete hex must ship in code, a generated Figma file, or a
  Stitch design-system asset — see `.claude/rules/figma-design.md` /
  `.claude/rules/stitch-design.md` for the mechanics per destination.

## Scope limitation (v1)

This token set is **colors only** — no typography, spacing, or
corner-radius tokens exist yet. Don't fabricate those either; use
reasonable defaults and say explicitly that they're not sourced from a
design token, or ask, until a v2 export adds them.

## Load this rule when

- Generating or editing any UI screen/mockup (Figma or Stitch) for an
  SBSI product.
- Writing or reviewing frontend code that sets colors for an SBSI product.
- Building any chart/dataviz for an SBSI product.
- Filling in `.claude/soul.md`'s color palette section.

## Skip when

- Non-visual work with no color decisions involved.
- Typography/spacing/layout decisions unrelated to color (not yet covered
  by this token set — see Scope limitation above).
