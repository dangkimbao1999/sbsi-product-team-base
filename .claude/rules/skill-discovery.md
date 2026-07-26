# Skill Discovery — Check This Repo's Own Skills First

The skills list injected into the system prompt at session start only
reflects **global/plugin** skills. It does NOT include this repo's own
`.claude/skills/` — those are only discoverable by actually looking in the
folder. Don't assume the injected list is complete.

**Before starting any non-trivial task** — especially generating a document
or deliverable, or following a procedure that plausibly already has a
convention — run a quick check for a project-specific skill first:

```
Glob(".claude/skills/**", path: "<repo root>")
```

If a matching `SKILL.md` exists, read and follow it instead of drafting
from general knowledge. A project-specific skill (e.g. `brd-generation`
with SBSI's actual BRD template) always takes precedence over a generic
global skill (e.g. the generic `docx` skill) or your own default structure
for that document type.

## Load this rule when

- Starting a task that could plausibly have a project-specific skill:
  document/deliverable generation, a named artifact type (BRD, SRS, design
  doc), or a repeated internal workflow.
- About to invoke a global skill (docx, pptx, xlsx, pdf) for a deliverable
  — check for a more specific local one first.

## Skip when

- Purely conversational tasks with no deliverable.
- You've already confirmed this session that no relevant local skill
  exists for this task type.
