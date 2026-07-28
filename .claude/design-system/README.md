# SBSI Design System — Tokens

Canonical source of SBSI's brand/UI color tokens, exported from Figma
Variables. Applies to **all** SBSI products this repo supports (trading
web/app, Research Hub, websites) — this is shared cross-product design
knowledge, not per-product.

Consumed by `.claude/rules/design-system.md`, `.claude/rules/figma-design.md`,
and `.claude/rules/stitch-design.md`. Read those rules for *how* to apply
this file when generating a design — this README only documents *what's in
the file*.

## Current file

- `tokens-SBSI-design-system-v1.json` — v1, colors only. No typography,
  spacing, or corner-radius tokens yet.

**Never overwrite this file in place when a new export arrives.** Add it as
`tokens-SBSI-design-system-v2.json` (etc.) so the diff between versions
stays reviewable, then update the "Current file" pointer here and in
`.claude/rules/design-system.md`.

## Structure

The file has 5 top-level collections (Figma Variables collection+mode,
flattened to `"<Collection>/<Mode>"` keys):

1. **`SBSI color/Light`**, **`SBSI color/Dark`** — the semantic tokens
   designers/screens actually consume. Six role groups, each present in
   both modes:
   - `Text` — `Primary` / `Secondary` / `Tertiary` / `Inverse` / `White`,
     `Semantics.{Disabled,Brand,Danger,Info,Warning,Success}`,
     `Accent.{Green,Red,Yellow,Purple,Blue}`, and `Price.{Up,Down,Fixed,
     Ceiling,Floor}` (see "Price color convention" below).
   - `BG` — `Page.{Default,Inverse}`, `Surface.{Primary,Secondary,
     Disabled}.{Default,Pressed}` (note: source also has a `Dissabled`
     key — typo, kept as-is, see Quirks), `Surface.Opacity.*`,
     `Surface.Semantic.*`, `Surface.Blanket.Overlay`,
     `Semantics.Danger.{Default,Pressed,Secondary}`,
     `Brand.{Bold,Subtle}.{Default,Pressed}`.
   - `Stroke` — `Default`, `Brand.{Bold,Subtle}`, `Danger`, `Inverse`,
     `White`, `Warning`, `Infor` (typo for Info, kept as-is), `Purple`,
     `Grey`, `Medium`, `Green`.
   - `Icon` — mirrors `Text`'s shape (Primary/Secondary/Tertiary/Inverse/
     White/Semantics/Price/Accent).
   - `Chart` — one swatch per family: `Green`, `Red`, `Blue`, `Gray`,
     `Purple`, `Yellow`.
   - `Pie_Chart` — 5-step ramp (`1`-`5`, light→bold) per family: `Green`,
     `Red`, `Yellow`, `Blue`, `Purple`.

2. **`Basic color/Light`**, **`Basic color/Dark`** — the base 50-900 scale
   (`Brand`, `Green`, `Blue`, `Yellow`, `Red`, `Purple`, `Gray`,
   `Black-alpha`) that the semantic tokens above alias into via
   `{Family.Step}` references (e.g. `{Green.600}`).

3. **`Basic color/Color Scale`** — a third scale. See "Known gap" below —
   **do not treat this as authoritative** without confirming with the
   design team first.

## Verified facts (checked by diffing the raw JSON, not assumed)

- `Basic color/Light` and `Basic color/Dark` are **byte-identical** across
  all 74 shared scalar values — the base palette does not change between
  light/dark mode. Only the semantic layer (`SBSI color/*`) picks
  different scale-steps per mode for the same role (e.g. `Text.Price.Up`
  is `{Green.600}` in Light but `{Green.500}` in Dark). This is the
  intended design-system pattern (cf. Material 3 / Radix Colors) — treat
  `Basic color/Light` (== `Basic color/Dark`) as **the current base
  palette**.
- `Basic color/Color Scale` uses **different hues** for every chromatic
  family than `Basic color/Light|Dark` (e.g. `Brand.500` is `#e45f35`,
  orange, in Color Scale vs. `#ad0a0c`, deep red, in Light/Dark). Given
  `SBSI color/*`'s semantic tokens alias into the Light/Dark base palette
  (by construction — see above), the deep-red `#ad0a0c` is inferred to be
  **the current brand primary**; `Color Scale` reads as a legacy/earlier
  palette left in the file. This is an inference from data patterns, not
  a Figma-verified fact — confirm with the design team or a connected
  Figma file before treating `#ad0a0c` as gospel for anything
  brand-critical (logo colors, marketing collateral).

## Known gap — unresolved dark-mode surface aliases

`SBSI color/Dark`'s `BG.Surface.Primary.Default` (`{Gray.890}`) and
`.Pressed`/`Secondary.Default` (`{Gray.850}`) reference Gray steps that
**do not exist** in `Basic color/Dark`'s Gray family (which only has
10/50/100…900 + White/OffWhite). Those two steps only exist in
`Basic color/Color Scale`'s Gray family (`850` = `#212025`, `890` =
`#1a191e`) — which otherwise exactly matches `Basic color/Light|Dark`'s
Gray family for every shared step, so it's safe to use for this one gap.
Everywhere else, don't reach into `Color Scale`.

## Quirks preserved from the source export (don't "fix" — may be intentional Figma naming)

- `BG.Surface.Dissabled` (extra "s") exists **alongside** a separate
  `BG.Surface.Disabled` key in both modes — same value, kept both as
  exported.
- `Stroke.Infor` is a typo for "Info" — kept as exported since it's the
  actual variable name a Figma-side lookup would need to match.

## Price color convention (VN stock exchange)

`Text.Price.*` / `Icon.Price.*` encode Vietnam's standard stock-exchange
price-band colors — reuse these roles for any trading-price UI rather
than inventing red/green ad hoc:

| Role | Meaning | Light | Dark |
|---|---|---|---|
| `Up` | Price increased | Green | Green |
| `Down` | Price decreased | Red | Red |
| `Fixed` | Reference price (no change) | Yellow | Yellow |
| `Ceiling` | Price ceiling (trần) | Purple | Purple |
| `Floor` | Price floor (sàn) | Blue | Blue |

## How to get a concrete hex value

For planning/discussion, resolving `{Family.Step}` against
`Basic color/Light`/`Dark` (documented above) is reliable. For anything
that ships (code, a generated Figma file, a Stitch design-system asset),
prefer resolving through the **live** source instead of hand-resolving
this static export:

- If a Figma library is connected, use the official Figma MCP's
  `get_variable_defs` / `search_design_system` — Figma resolves aliases
  correctly using real collection/mode bindings, which this flattened
  JSON export cannot fully reconstruct (see "Known gap" above).
- Otherwise, resolve manually against `Basic color/Light|Dark` in this
  file, and flag anything relying on `Color Scale` or the two ungapped
  Gray steps as unverified.
