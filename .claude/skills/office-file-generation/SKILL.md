---
name: office-file-generation
description: Generate or populate Word (.docx) and Excel (.xlsx) files programmatically — fill an existing template with data (e.g. a BRD template) or build a new file from scratch. Use when asked to produce, write, generate, or populate a docx/xlsx file, or to create a document "based on" an existing Office template.
---

# Generating & Populating Office Files (docx / xlsx)

For reading/extracting from existing files, see
`.claude/rules/office-file-parsing.md` instead — this skill is write-side
only. Install everything with `bun add <package>` (never npm/npx).

## Decide: template-fill vs from-scratch

- **Template-fill** (preferred whenever a template file already exists — it
  preserves the org's exact branding/styling/layout): `docxtemplater` for
  Word, `exceljs` for Excel.
- **From-scratch** (no template, or the template has no merge points): build
  the document structurally with the `docx` npm package for Word, `exceljs`
  for Excel.

## Word — filling an existing template (`docxtemplater`)

1. Install: `bun add docxtemplater pizzip`
2. Template authoring: open the template in Word/LibreOffice and mark
   variable spots with `{tag_name}` curly braces. Loops: `{#items}...{/items}`.
   Conditionals: `{#has_x}...{/has_x}`.
   - **If the template has no tags yet** (a typical human-authored template
     with generic section headings) — this is a one-time authoring step:
     open the template once, add `{tag}` placeholders where content should
     vary, save it. Don't try to inject placeholders into the XML
     programmatically; do it in the Word UI.
3. Render:
   ```ts
   import PizZip from "pizzip";
   import Docxtemplater from "docxtemplater";
   import fs from "fs";

   const zip = new PizZip(fs.readFileSync("brd-template.docx"));
   const doc = new Docxtemplater(zip, { paragraphLoop: true, linebreaks: true });
   doc.render({
     project_name: "...",
     stakeholders: [...],
     requirements: [{ id: "REQ-1", description: "..." }],
   });
   fs.writeFileSync(
     "brd-output.docx",
     doc.getZip().generate({ type: "nodebuffer" }),
   );
   ```
4. The free core (dual MIT/GPLv3) covers text/loop/condition substitution.
   Rich-text HTML injection and image replacement are separate paid modules
   — avoid needing them for plain-text documents like a BRD; if a task
   genuinely needs them, flag the paid dependency to the user before adding
   it, don't add it silently.

## Word — building from scratch (no template) — `docx` package

Use the `docx` npm package (`Paragraph`/`HeadingLevel`/`Table`/etc. builder
API) when there's no existing template to preserve. Mirror the section
structure you'd otherwise read out of a reference document with `mammoth`
(see `.claude/rules/office-file-parsing.md`).

## Excel — filling a template or building from scratch (`exceljs`)

`exceljs` covers both cases with the same workbook API:

```ts
import ExcelJS from "exceljs";

const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile("template.xlsx"); // template-fill
// or: const workbook = new ExcelJS.Workbook();  // from scratch

const sheet = workbook.getWorksheet("Requirements");
sheet.getCell("B2").value = "...";
// or sheet.addRow([...]) to append new rows

await workbook.xlsx.writeFile("output.xlsx");
```

Inspect the template's actual layout before writing into it — sheet names
(`workbook.worksheets.map(w => w.name)`), header row
(`sheet.getRow(1).values`) — don't assume column order from memory.

**Caveat**: exceljs's own maintainers have flagged the project as not
actively released since Oct 2023 (see the reading rule for the same note).
It's still the most complete open-source option for template-preserving
Excel writes — there isn't a clearly superior actively-maintained
alternative for this job (`xlsx-populate` is more stale, not less). Mention
this maintenance risk to the user if long-term support matters for their
use case; don't silently pick a lesser-known alternative instead.

## Worked example: generating a BRD from a template + requirements

Concrete workflow for "read my BRD template, write a new BRD based on my
requirements":

1. Read the existing template to understand its section structure: convert
   `brd-template.docx` to Markdown/HTML with `mammoth` and inspect the
   headings/sections.
2. Check whether the template already has `docxtemplater`-style `{tags}`.
   - If yes: skip to step 4.
   - If no: tell the user the template needs one-time tagging (step 2 of
     the docxtemplater section above) before this can be automated on
     future runs — or, for a one-off without editing the template file,
     fall back to generating fresh with the `docx` package, matching the
     template's heading/section structure (not its exact visual styling).
3. Gather the actual content for each tag/section from the user's request.
   Never invent BRD content — stakeholders, scope, acceptance criteria —
   that wasn't given or explicitly confirmed by the user.
4. Render with `docxtemplater` (or build with `docx`) and write the output
   to a new filename that can't collide with the template (e.g.
   `<project>-brd.docx`) — never overwrite `brd-template.docx` itself.
5. Spot-check a rendered field or two before handing off, to confirm
   substitution actually worked.

## Load this skill when

- Asked to generate, write, produce, populate, or fill a `.docx` or `.xlsx`
  file.
- Asked to create a document "based on" or "using" an existing Office
  template.

## Skip when

- Only reading/extracting data from an Office file — use
  `.claude/rules/office-file-parsing.md` instead.
- Generating `.pdf`, `.pptx`, or other non-Word/Excel formats — out of
  scope for this skill.
