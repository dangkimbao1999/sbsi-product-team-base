# SBSI Document Routing

Document tasks in this workspace use the naming convention:

`<organization> - <document type> - <task>`

e.g. `sbsi - quy định - soạn mới`, `sbsi - quy trình - export docx`,
`sbsi - quy định - chỉnh sửa theo feedback`, `sbsi - quy trình - reformat`.

The three parts: `organization` owns the convention/template,
`document type` names the artifact, `task` is the action requested. This
format is designed to extend to other orgs later (`mb - quy định - ...`,
`company-x - quy trình - ...`) — **do not** treat SBSI's pipeline as the
default for a document type just because it's the first one wired up, and
do not silently apply the SBSI pipeline to a different org's prefix.

## Trigger

Load the `sbsi-template-router` skill (which itself hands off to
`sbsi-docx-format-core` once a template resolves) **before touching any
DOCX** whenever either is true:

1. The task matches `sbsi - <document type> - <task>` for an SBSI
   governance document type: **Quy định, Quy trình, Quy chế, Hướng dẫn**,
   or an equivalent SBSI internal governance/định chế document.
2. No routing prefix is given, but the user clearly asks to create, edit,
   reformat, or export to DOCX an SBSI governance document of one of those
   types.

Don't require the user to name the skill explicitly — recognizing the task
shape above IS the trigger.

## Do NOT use this pipeline for

- BRD — routed through `brd-generation` instead (it resolves its own
  template via the same shared registry but owns its own content workflow
  and typography convention; see that skill's "Relationship to
  sbsi-template-router" section).
- Presentations, spreadsheets, email, or ordinary/non-governance reports.
- Any non-SBSI organization's documents, until that org's own template and
  routing are registered.

## Fail closed

If `sbsi-template-router` does not return `RESOLVED` (e.g. today, `Quy
định` has no registered template yet → `TEMPLATE_NOT_REGISTERED`), stop and
tell the user the specific missing dependency — never generate an
approximate SBSI DOCX from a blank document or a different type's template.
Same rule for every downstream gate in `sbsi-docx-format-core` (structural
validator, typography, render QA): any failure blocks delivery.

## Invocation examples

```text
sbsi - quy định - soạn mới
sbsi - quy định - chỉnh sửa theo feedback
sbsi - quy định - reformat
sbsi - quy trình - chỉnh sửa
sbsi - quy trình - export docx
```

## Load this rule when

- A task's phrasing matches or resembles `<org> - <document type> -
  <task>`.
- The user asks to create, edit, reformat, or export an SBSI governance
  document (Quy định/Quy trình/Quy chế/Hướng dẫn or equivalent) as DOCX,
  with or without the routing prefix.

## Skip when

- The document type is BRD, or is not an SBSI governance document
  (presentation, spreadsheet, email, generic report).
- The organization prefix names an org other than `sbsi` with no
  registered pipeline yet — ask the user rather than guessing which skill
  applies.
