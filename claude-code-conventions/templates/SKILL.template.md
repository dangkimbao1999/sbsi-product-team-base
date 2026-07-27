---
name: <skill-name-kebab-case>
description: |
  <One paragraph (2-4 sentences): what this skill covers and why it needs to
  exist as its own skill rather than living in CLAUDE.md or a sibling skill.>
  Use when: <comma-separated concrete situations — not "when working in X folder">.
  Triggers on: <file paths, imports, CLI commands, error strings, or keywords
  that signal this skill is needed>.
  Skip when: <only add this line if a close sibling skill could be confused for
  this one, e.g. "backend errors — use debugging instead">.
---

# <Title Case Name>

<1-3 sentences: the problem this solves and the one fact a reader must know
before anything else. If this skill documents an external product (an SDK, a
cloud service, a library), put its canonical doc link here instead of
restating the product's own docs — e.g. "Reference: https://docs.example.com/...".>

<!-- ============================================================
     STEP 1 — Pick ONE shape below, delete the other three blocks
     entirely (including this comment). Every skill in this repo's
     56-skill corpus fits one of these four shapes. If your draft
     needs two, that's a signal to split it into two skills instead.
     ============================================================ -->

<!-- ── SHAPE A — Convention / rule skill ─────────────────────────
     Examples in this repo: tdd, performance, backward-compatibility,
     hasura, extraction-dev, multi-env-dev.
     Teaches a standing rule Claude applies while writing/reviewing code.
     Nothing is "run" — it's read, then followed inline. -->

## Rules
- <banned pattern> → <required replacement>. One falsifiable rule per line —
  a reviewer should be able to point at a diff line and say "this breaks rule N".
- <next rule, most safety-critical first>

## Patterns
```ts
// BAD — <why this fails, ideally cite the incident/reason>
...

// GOOD — <why this is correct>
...
```

## When NOT to apply
- <the one legitimate exception, if any — do not invent one just to fill this>

<!-- ── SHAPE B — Procedure / slash-command skill ─────────────────
     Examples in this repo: sync-main, force-merge-pr, linear-log-bug,
     generate, check-codebuild, release-phoenix-sdk.
     Invoked as /skill-name [args] or by an explicit trigger phrase.
     Reads like a runbook: numbered, deterministic, ends in a checkable
     outcome (exit code, printed status, created artifact). -->

## Usage
`/skill-name [args]`

## Procedure
1. <step — the exact command or tool call, not a paraphrase>
2. <step>
3. <step — how to verify success (a command, an exit code, a URL to check)>

## Failure modes
| Symptom | Cause | Fix |
|---|---|---|
| ... | ... | ... |

<!-- ── SHAPE C — Scaffold / generator skill ──────────────────────
     Examples in this repo: new-agent, new-remote-app, new-sdk,
     implement-engineer-local-env, implement-shared-nonprod-env.
     Produces new files from a template. Keep SKILL.md short and put
     the actual design spec in references/guide.md — this is the one
     shape where a skill should NOT inline everything, because the
     full spec is too long to justify re-loading on every quick
     question this skill answers. -->

Read `references/guide.md` for the full design spec before doing anything.

## Workflow
1. Copy the template from `<source path>`
2. Rename / configure `<placeholders>`
3. Register in `<the place new instances must be wired up>`
4. Verify: typecheck, run, or smoke-test the result

<!-- ── SHAPE D — External SDK / platform reference skill ─────────
     Examples in this repo: statsig-react, statsig-server,
     statsig-feature-gates, agents-dev.
     Documents a third-party API adapted to this repo's conventions.
     Always separate "what the platform does" (survives a vendor doc
     rewrite) from "how we wire it here" (this repo's own choices). -->

Reference: <link to the canonical external doc>

## Purpose
PURPOSE: <one line — what this SDK/tool is FOR>
NOT for: <one line — what it's commonly confused with>

## Core API
<the 3-6 calls/hooks/concepts an engineer actually needs, each with a snippet>

## This repo's conventions
<how the generic SDK gets wired into this codebase specifically — gate/env
names, wrapper functions, required call sites>

<!-- ============================================================
     STEP 2 — sections below apply to any shape. Keep only the ones
     that add information beyond what's already in the frontmatter.
     ============================================================ -->

## When to use / When NOT to use
<Only add this if the frontmatter's Use-when/Skip-when needs more than one
line to disambiguate from a close sibling skill (e.g. autonomous- vs
interactive-frontend-testing, statsig-react vs statsig-server). Otherwise
skip it — restating the frontmatter in prose is dead weight.>

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|

<!-- ============================================================
     Checklist before shipping this skill — delete this block too.
     ============================================================ -->
<!--
[ ] Frontmatter has `name` + `description` only (no extra top-level keys —
    a `metadata:` block is NOT part of the schema even though one skill in
    this repo has it; don't copy that).
[ ] `description` has Use-when + Triggers-on lines Claude can pattern-match.
[ ] Self-contained: no "see the X skill" references — inline the minimum
    needed content instead, or the mention risks auto-loading X unnecessarily.
[ ] If a spec exceeds ~40 lines and isn't needed for every invocation,
    move it to `references/guide.md` and say so in the first line of the body.
[ ] If the skill runs a deterministic multi-step script, colocate it as
    `<skill-name>.sh` next to SKILL.md and call it by exact relative path.
[ ] Matching entry added to `.claude/rules/<name>.md` (see RULE.template.md)
    so the skill has a `Load when:` / `Skip when:` trigger outside its own
    frontmatter — the rule is what's always loaded; the skill is what's
    loaded on demand.
-->
