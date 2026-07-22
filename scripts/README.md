# Scripts

Work scripts for SBSI's product team — automation and one-off tooling used
in day-to-day work (not application source code).

## Conventions

- One script per task; name it for what it does (`sync-linear-labels.sh`,
  `export-weekly-report.py`, ...).
- If a script grows enough logic to need its own docs, add a short comment
  header (what it does, how to run it) rather than a separate `.md` file.
- Same rules apply here as everywhere else in this repo — TDD
  (`.claude/rules/tdd.md`) and no-fallbacks (`.claude/rules/no-fallbacks.md`)
  are not relaxed just because a script is small.
