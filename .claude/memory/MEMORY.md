# Shared Project Memory — Index

This file is an INDEX, not a memory — each entry is one line pointing at a
file in this same directory. Content lives in the linked file, never here.

Read this file at the start of any work session before making assumptions
about user preferences, project context, or past feedback. These memories
are committed to git and shared across everyone working in this repo
(distinct from personal memory in `~/.claude/`, which is per-engineer and
never committed).

## How entries get added

When you (Claude Code) learn something worth remembering — a correction,
a confirmed approach, an ongoing project fact, a pointer to an external
system — write it as its own file here using this frontmatter shape:

```markdown
---
name: short-kebab-case-slug
description: one-line summary, used to judge relevance in future sessions
metadata:
  type: user | feedback | project | reference
---

<content — for feedback/project entries, structure as: the rule/fact, then
a **Why:** line and a **How to apply:** line>
```

Then add a one-line pointer here: `- [Title](file.md) — one-line hook`.

## What NOT to put in memory

- Anything derivable by reading the current code (architecture, file paths,
  conventions) — read the code instead, it's always more current.
- Git history / who-changed-what — `git log`/`git blame` are authoritative.
- Ephemeral in-progress task state — that belongs in a plan or task list for
  the current conversation, not durable memory.

## Entries

- [Project structure decision](project-structure-decision.md) — root stays CTCK-framed, each SBSI product gets a knowledge-only folder under `projects/`
- [Linear project for Research Hub](linear-research-hub-project.md) — team Iambao, project "Stock Research Hub - SBSI", don't create a duplicate
- [Linear workspace hardcoded](linear-workspace-hardcoded.md) — repo always targets the `iambao` workspace (team Iambao, key IAM); verify with `list_teams` before writing, fail loud on mismatch
- [Product team workspace reframe](product-team-workspace-reframe.md) — repo's purpose is shared Claude rules/skills + per-product knowledge + scripts + demos; no product (incl. Research Hub) is coded here; enforcement hooks unaffected
