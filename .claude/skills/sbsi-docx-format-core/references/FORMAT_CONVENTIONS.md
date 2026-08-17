# SBSI DOCX Format Conventions

Document-type-independent rules, applied **after** `sbsi-template-router` has
resolved the correct template. Nothing here should ever hardcode one
document's business content (a specific article name, chapter number, or
one org's signature-block text) — see the genericity contract at the top of
`scripts/_sbsi_docx_common.py`. Template-specific quirks belong in that
template's own `template_manifest.json` (see `sbsi-template-router`'s
"Template registration rules"), not in this file or the scripts.

## 1. Ordinary text typography — exact, blocking, per-template

All **ordinary text** MUST be Times New Roman, exactly 13pt (`w:sz`/`w:szCs`
= `26` half-points) — this is `format_contract.json`'s **global default**,
used by every governance document type (Quy trình, Quy định, Quy chế,
Hướng dẫn). It is not a hardcoded constant the engine can't deviate from:
one shared engine (`_sbsi_docx_common.py` / `validate_sbsi_docx.py` /
`normalize_ordinary_text.py`) runs against every SBSI document type, and a
template with its own long-standing, verified typography convention
declares an explicit override in its own `template_manifest.json`'s
`typography_profile` field (e.g. BRD's TNR 12pt, owned by PTSP — see
`sbsi-template-router/templates/brd/template_manifest.json`). Never guess
or silently apply a different value than what the manifest declares —
missing manifest means the global 13pt default applies.

Ordinary text includes: body/legal prose, preamble prose, numbered-clause
content, lettered sub-point content, explanatory paragraphs, and ordinary
table text — including descriptive text inside appendices.

Set all relevant font slots consistently wherever direct run formatting is
applied: `ascii`, `hAnsi`, `eastAsia`, `cs`. Never let a run silently
inherit Aptos/Calibri/Arial from a theme font or an un-set slot.

### Exclusions (not "ordinary text")

- Cover-page title/type/issuance typography.
- Real headings (any paragraph with a resolved Word outline level 0-8).
- TOC heading and TOC entry styles.
- Header/footer branding and page-number fields (separate XML parts —
  never touched by the format-core scripts at all).
- A direct font-size override more than `display_size_margin_above_ordinary_half_points`
  (default 2 half-points = 1pt) above the *selected template's own*
  resolved ordinary size — relative to that template's typography profile,
  not a fixed absolute pt value, so it correctly exempts e.g. BRD's bold
  14pt pseudo-section-titles (12pt baseline + margin) the same way it
  exempts a governance template's oversized promulgation-page title (13pt
  baseline + margin).
- A template-declared special display element (compact appendix matrix,
  landscape form) — declared via that template's manifest, not guessed.

### How "ordinary text scope" is actually determined (generic, not per-document)

1. **Cover-page boundary**: everything before the first paragraph that
   starts a new page (`w:pageBreakBefore` or an explicit `w:br
   w:type="page"`) is treated as cover-page front matter and excluded. This
   is a structural signal, not a text match — it works for any template
   that puts cover + doc-info table + TOC on page 1 and body from page 2,
   which is the common SBSI convention. A template with no such page break,
   or that wants the whole document checked, sets
   `"cover_page_strategy": "none"` in its manifest.
2. **Headings**: any paragraph whose *resolved* outline level (direct
   `w:outlineLvl`, or inherited via the paragraph's style `basedOn` chain)
   is 0-8 is a real heading and is excluded from the ordinary-text font
   check. Outline level 9 means "Body Text" in OOXML — NOT a heading, even
   though some heading-adjacent styles use it as their style default before
   a paragraph-level override sets the real level.
3. **TOC styles**: any paragraph whose style id starts with `toc`
   (case-insensitive) is excluded.

## 2. Numbering must be native Word numbering

Never fake structural numbering by typing `1.`, `2.`, `a)`, `b)` etc. into
paragraph text. Structural clauses/sub-points must carry real `w:numPr` →
`numbering.xml`.

Use the numbering definitions already defined by the **selected template**
— don't invent a new scheme when the template already has one.

### Manual-numbering detection (validator)

The validator looks for **runs of 2+ consecutive paragraphs** matching
`^\d+[\.\)]\s` or `^[a-zđ]\)\s` (case-insensitive) that lack a real `numPr`
and whose numbers/letters increase sequentially — that pattern is a real
manually-typed list, not a coincidence, and is a **blocking ERROR**. An
isolated single match (e.g. a sentence that happens to start with a digit)
is only a WARNING, to avoid false positives.

### The appendix exception

A run of manually-numbered items inside an appendix/reference-list region
(default marker: a paragraph starting with "Phụ lục" — the generic
Vietnamese word for "Appendix", used across every SBSI document type, not
one document's specific content) is downgraded to a WARNING, never
blocking. This matches a real, observed SBSI convention: the Quy Trình
template's own "Danh mục tài liệu tham chiếu" appendix is a manually
numbered bibliography of legal citations, which is a legitimate document
convention, not a structural Khoản/Điểm clause. A template can override the
appendix marker pattern via its manifest's `appendix_heading_pattern`.

## 3. Headings must be real structural styles

Never build "Chương I", "Điều 1." etc. by bolding/centering a `Normal`
paragraph. They must be real Word paragraph styles with real outline
levels, so the Navigation Pane and TOC field work. This is the default for
every SBSI document type; a template's manifest can set
`"requires_real_headings": false` only when its own top-level sections are
verifiably NOT built on real outline-level styles as a long-standing,
deliberate template convention (e.g. BRD's 13 bold-`Normal` section
titles) — this suppresses the "no real heading found" gate for that
template specifically, it does not disable the fake-heading-vocabulary
check below (which stays on regardless, since typing literal
"Chương"/"Điều" text without real numbering is never acceptable for any
type that uses that vocabulary).

The validator's fake-heading check looks for text matching known
Vietnamese legal-drafting heading vocabulary (`Chương I`, `Điều 1.`, `Mục
1.`, `Phần I`) that has **no** resolved outline level — that combination is
always a blocking ERROR. A template whose hierarchy uses different
vocabulary (e.g. named section titles rather than "Điều N") can extend the
pattern list via its manifest's `structural_heading_patterns`; it is not
required to use exactly `Chương`/`Điều`/`Khoản`/`Điểm` — "at minimum
support the hierarchy the selected template actually uses."

Discover a template's real style IDs/outline mapping from the template
itself (`styles.xml`) — never hard-code assumptions like "Style1 is always
the top level" across different templates.

## 4. TOC must be a real Word field

If the document has a "Mục lục" (or "Table of Contents") heading, a real
TOC field must exist: an `instrText` run containing `TOC` between
`w:fldChar` begin/separate/end markers — not typed text with dot leaders.
`word/settings.xml`'s `w:updateFields` should be `true` so Word offers to
refresh on open; the generated file must always support `Ctrl+A → F9` in
Word regardless.

## 5. Preserve selected-template layout assets

Unless the user explicitly requests a layout change, preserve from the
selected template: page size/orientation, section breaks, margins,
header/footer distances and content, logo/company identity, footer
disclaimer, page-number fields, cover geometry, doc-info table geometry,
table border/fill conventions, appendix section orientation (don't flatten
a landscape appendix to portrait), and type-specific title blocks.

The goal is **reusing the selected template's actual Word structure**, not
visually imitating it — see the "golden-template principle" in
`sbsi-template-router`'s SKILL.md.

## 6. Tables

Ordinary tables: reuse the template's borders/widths/cell margins/
alignment/repeat-header/shading; ordinary cell text follows the selected
template's typography profile (§1 — TNR 13pt by default, or that
template's own manifest override) like any other ordinary text; never
shrink text to force-fit content — fix column widths/orientation/section
layout instead.

Special compact matrices/forms: preserve the template's own typography
there; don't blindly normalize a template-intentional compact style to
13pt.

## 7. Format-only mode

When the user says "chỉ sửa format" / "không sửa nội dung" / "only fix the
format" (or equivalent): preserve wording, punctuation, figures, dates,
names, references, tables, appendices, and ordering exactly. No rewriting,
shortening, correction, terminology changes, or restructuring. The one
allowed transformation: replacing a manually-typed structural prefix with
the equivalent real Word numbering/heading style — the visible wording
must stay semantically identical.

## 8. Word parts most likely to need direct manipulation

`python-docx` is safe for most paragraph/run/table edits. Reach for direct
OOXML manipulation (as the validator/normalizer scripts do, via `lxml`)
when python-docx doesn't expose what you need:

- `word/styles.xml` — style definitions, `docDefaults`, outline levels.
- `word/numbering.xml` — `abstractNum`/`num`, level formats (`lvlText`,
  `numFmt`), hanging indents.
- `word/document.xml` — paragraph/run properties, section properties,
  field codes (`fldChar`/`instrText` for TOC).
- `word/settings.xml` — `updateFields`.
- `word/header*.xml`, `word/footer*.xml` — never touched by the
  normalizer/validator; preserved automatically by only ever repacking
  onto the same zip you loaded the template copy from.
- `word/_rels/*` and `[Content_Types].xml` — relationships/media; don't
  touch these unless you're adding new parts (e.g. a new image).

Always work on a COPY of the selected template — never open/edit the
template path itself.
