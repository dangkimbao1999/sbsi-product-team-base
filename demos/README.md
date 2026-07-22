# Demos

On-demand demo generation for the product team — one folder per demo,
named for what it demonstrates (e.g. `demos/order-flow-mockup/`).

## Conventions

- Each demo lives in its own subfolder; keep demos independent of each
  other (no shared state across `demos/*`).
- Demos are short-lived by nature (built to show something, then often
  discarded or superseded), but the same repo-wide rules still apply while
  they're being built — TDD (`.claude/rules/tdd.md`) and no-fallbacks
  (`.claude/rules/no-fallbacks.md`) are not relaxed for demo code.
- If a demo turns out to need ongoing development as a real product, it
  moves into its own dedicated repo (this repo never hosts product code —
  see root `CLAUDE.md`), not somewhere else inside here. Add or update the
  corresponding `projects/<name>/CLAUDE.md` to point at the new repo.
