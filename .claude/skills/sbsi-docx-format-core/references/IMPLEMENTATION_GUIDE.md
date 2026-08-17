# SBSI DOCX Format Core — Implementation Guide

How to actually build/reformat a document once `sbsi-template-router` has
handed you a `RESOLVED` template. This is the "how" companion to
`FORMAT_CONVENTIONS.md`'s "what".

## A. New document from a resolved template

1. Get `{document_type, template_path}` from `sbsi-template-router`
   (`status: RESOLVED` — never proceed on anything else).
2. **Copy** the template file to a scratch working path. Never open/edit
   the template path itself.
   ```bash
   cp "<template_path>" /tmp/work/output.docx
   ```
3. Edit the copy's `word/document.xml` directly with `lxml` (or
   `python-docx` for simple paragraph/table edits) — this is the
   "clone/copy the template → replace content" golden-template workflow,
   not "build blank and imitate visually." See `office-file-generation`
   skill's "Word — filling an existing template without pre-tagging
   (direct XML DOM edit)" section for the general technique (this skill
   assumes you've read that one for the mechanics of DOM edits,
   row/paragraph cloning, and the header-row off-by-one gotcha).
4. For any NEW structural heading/clause you add (not already present in
   the template), **use the generation helpers in `_sbsi_docx_common.py`
   — `clone_structural_paragraph()`, `clone_empty_structural_paragraph()`,
   `build_new_chapter_paragraphs()`, `build_toc_field_paragraph()` — never
   hand-roll `numPr`/`outlineLvl` XML or type the structural prefix
   ("Chương I", "Điều 5.", a dot-leader TOC line) as literal text.** This
   is not a style preference: a real reformatted document
   (`QT_Nghien_cuu_va_Phat_trien_SPDV_so`, found 2026-08-17) got this wrong
   by hand — new chapters used the wrong paragraph style, dropped the
   direct `outlineLvl` override real chapters carry, and typed "Chương I"
   as text — and it passed casual visual inspection while failing every
   Word-native guarantee (Navigation Pane, TOC field, auto-renumbering).
   The helpers exist specifically so that mistake requires effort to
   repeat, not the default path. Pick your reference paragraph(s) from the
   selected template's own manifest (e.g. quy-trinh's `chuong_structure`
   and `dieu_numbering` fields document exactly which existing paragraphs
   to clone and why) — never assume a style name implies an outline level
   or active numbering without checking the manifest or the real XML.
5. Repack onto the **same** `PizZip`/zip instance you loaded from the
   template copy, so headers/footers/styles/numbering/relationships/media
   pass through untouched — only `word/document.xml` (and, if you ran the
   normalizer, `word/styles.xml`/`word/settings.xml`) should actually
   change.
6. Run the validator (`validate_sbsi_docx.py`) — see below.
7. Run the render QA (`render_qa.py`) — see below.
8. Deliver only after both pass.

## B. Reformatting an existing/source document

1. Get the resolved template + document type from `sbsi-template-router`.
2. Inventory the source content (headings, tables, appendices) before
   editing anything.
3. Copy the **selected template** to a new output file (not a copy of the
   source document) — the template is the structural source of truth.
4. Transfer the source's content into the template's structure. In
   format-only mode (see `FORMAT_CONVENTIONS.md` §7), content transfer must
   be wording-for-wording identical.
5. Convert any fake headings/manual numbering found in the source into the
   template's real styles/numbering as you transfer each block, using the
   same generation helpers as §A.4. If the source has a manually-typed
   "Mục lục" (dot-leader lines, no real field), replace it with
   `build_toc_field_paragraph()` using the selected template's own
   `toc_field_switches` manifest note — never keep the typed version even
   if it currently displays correct page numbers, since it will silently
   go stale on the next edit.
6. Run `normalize_ordinary_text.py` on the result to catch any remaining
   direct-run font/size overrides.
7. Run the validator, then render QA.
8. Deliver only after both pass.

## Running the scripts

```bash
# 1. Normalize ordinary text to Times New Roman 13pt (safe: skips cover
#    page, headings, and TOC entries by structure, not by guessing text).
python3 scripts/normalize_ordinary_text.py draft.docx normalized.docx \
  [--manifest <path/to/template_manifest.json>]

# 2. Validate. --template enables the section/header-footer preservation
#    checks; --manifest supplies template-specific structural exceptions
#    (cover-page detection strategy, appendix marker, extra heading
#    patterns) if the template has any beyond the generic defaults.
python3 scripts/validate_sbsi_docx.py --doc normalized.docx \
  --template "<selected_template.docx>" \
  --manifest "<selected_template_dir>/template_manifest.json"

# 3. Render + visual QA. Look at every PNG it produces — the script only
#    catches blank-page/page-count anomalies automatically; overflow,
#    orphaned headings, broken tables, lost logos, and misaligned indents
#    need an actual look.
python3 scripts/render_qa.py normalized.docx /tmp/work/render_qa_out \
  --expect-min-pages 2
```

`--manifest` is optional. If the selected template's directory has a
`template_manifest.json` sibling to the `.docx`, pass it explicitly — the
scripts do not auto-discover it (explicit is safer than a guessed sibling
path silently picking up the wrong file).

Any `ERROR:` line from the validator is blocking — do not hand the file to
the user. `WARNING:` lines are not blocking but must be reported to the
user, never silently dropped (per this repo's no-silent-fallbacks rule).

## Validation is necessary but not sufficient

`validate_sbsi_docx.py` checks structure/typography; it cannot see whether
a table overflowed a page or a heading got orphaned at a page break. Always
run `render_qa.py` and actually look at the rendered pages before telling
the user the document is ready — see `references/QA_CHECKLIST.md`'s
"Visual" section for what to look for.

## Common pitfalls

- **Table column collapse**: only relevant if you build a table from
  scratch with the `docx` package rather than cloning an existing template
  table row — see `office-file-generation` skill's "Decide" section.
- **Header-row off-by-one** when cloning table rows: always
  `rows[1:]` (skip the header/label row) before mapping data onto rows.
- **numId="0" is a real OOXML sentinel** meaning "remove inherited
  numbering for this paragraph", not "paragraph 0". Don't treat it as
  "no override was set."
- **A style name does not guarantee its outline level** — a style's OWN
  `<w:style>` block can carry a different (or no) `outlineLvl` than what
  every real paragraph using that style actually shows, because the real
  outline level often comes from a DIRECT per-paragraph `<w:outlineLvl>`
  override layered on top. Verified example: the Quy trình template's
  `Style2` has `outlineLvl=9` (OOXML's "Body Text", not a heading) at the
  style level, but every real Điều paragraph overrides it to `1` directly.
  Always clone a real sibling paragraph (via the helpers above) rather than
  constructing `pStyle` + assumed `outlineLvl` from scratch.
- **A "Chương"-level heading is commonly TWO paragraphs**, not one: an
  empty paragraph carrying the style's own active numbering (renders
  "Chương I" via the numbering definition, no typed text, no paragraph-level
  numId override) immediately followed by a title paragraph with numId
  explicitly set to `0` (so it doesn't also render a number). Use
  `build_new_chapter_paragraphs()` for this pair — inserting only one of
  the two, or merging them into one paragraph, breaks the pattern.
- **LibreOffice vs Word rendering differences**: LibreOffice does not
  always honor a paragraph-level `numId="0"` override identically to Word
  (a known interop gap). Treat `render_qa.py`'s output as a strong proxy,
  not a Word-identical guarantee — see that script's docstring.
- **Windows path/tooling gotchas** (this repo runs on Windows for the
  team): see the "Environment gotchas specific to this repo" section of
  the `office-file-generation` skill (Bash command-guard false positives,
  the primary-worktree edit guard's `.claude/` exemption not matching
  backslash paths, heredoc apostrophe issues).
