# Sub-Agents Index

| Agent | Purpose | Tools |
|---|---|---|
| `coder` | Default implementer: read → RED test → GREEN implement → typecheck → run tests → commit → self-review → digest. Never pushes, opens PRs, or touches an issue tracker. | Read, Edit, Write, MultiEdit, Bash, Grep, Glob |
| `reviewer` | Generic code reviewer: reads a diff, checks it against `.claude/rules/*.md`, reports findings. Never edits. | Read, Grep, Glob, Bash |
| `po-requirement-writer` | Maker. Raw Requirement → Draft Requirement (User Story/Business Rules/AC/Assumptions/Open Questions); also runs Revision mode → Final Requirement. Marks unresolved product judgment calls as `OPEN DECISION`, never guesses. Part of `po-requirement-refinement`. | Read, Grep, Glob |
| `po-requirement-reviewer` | Critic. Adversarially reviews a Draft Requirement for ambiguity/edge cases/missing rules, surfaces numbered Decision Points for the human PO. Never answers its own Decision Points. Part of `po-requirement-refinement`. | Read, Grep, Glob |
| `po-backlog-planner` | Planner. Final Requirement (PO-confirmed) → traceable backlog (FE/BE/Integration-Data/QA) + dependencies + delivery order. Never expands scope. Part of `po-requirement-refinement`. | Read, Grep, Glob |

Add new agents here as you create them (see the `new-agent` skill).
