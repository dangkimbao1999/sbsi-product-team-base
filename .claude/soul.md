# Brand & Voice

<Delete this file (and the "Soul & Voice" section in CLAUDE.md) if this
project has no user-facing product surface — e.g. a backend-only service or
an internal tool with no branded UI.

If it does, fill this in before generating any user-facing content (UI copy,
error messages, marketing copy, colors):>

## Voice

<2-3 sentences: how should the product "sound"? Formal vs casual, terse vs
warm, etc.>

## Do

- <e.g. "Use plain language, avoid jargon in user-facing errors">

## Don't

- <e.g. "Never use exclamation points in error messages">

## Color palette

Sourced from `.claude/design-system/tokens-SBSI-design-system-v1.json` —
see `.claude/rules/design-system.md` for how to apply it and
`.claude/design-system/README.md` for the full token structure. Don't
duplicate hex values here; that file is the source of truth and this file
would drift. Key facts worth keeping in mind for voice/brand work:

- Brand primary is a deep red/maroon (`#ad0a0c`, `Basic color` scale
  `Brand.500`) — inferred from data patterns, not yet Figma-verified, see
  the README's "Known gap" section.
- Every color role ships in both Light and Dark modes — brand-facing
  content (marketing pages, decks) should account for both unless the
  target surface is fixed to one.
- Price colors follow the VN stock-exchange convention (green=up,
  red=down, yellow=reference, purple=ceiling, blue=floor) — see the
  README's "Price color convention" table. Reuse these, don't invent new
  ones for trading-price content.
