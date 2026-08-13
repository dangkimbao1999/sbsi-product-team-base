# SBSI DOCX QA Checklist

## Structural (run `validate_sbsi_docx.py`)

- [ ] Correct template was resolved by `sbsi-template-router` before formatting.
- [ ] Real heading/outline-level paragraphs exist and are used for the
      document's section hierarchy.
- [ ] No manual/non-structural heading text (bold-Normal mimicking
      "Chương I" / "Điều 1." etc. without a real outline level).
- [ ] Structural clause/sub-point numbering uses real `w:numPr`, not typed
      "1." / "a)" prefixes — no blocking manual-numbering sequence detected
      outside an appendix.
- [ ] A real Word TOC field exists if the document has a "Mục lục" heading.
- [ ] Header/footer parts are present if the selected template has them.
- [ ] Section count/signature matches the selected template (or any
      difference is intentional and explained).

## Typography

- [ ] Ordinary text is Times New Roman, exactly 13pt.
- [ ] `Normal` / `Body Text` / `List Paragraph` styles and `docDefaults`
      resolve to TNR 13pt.
- [ ] No Calibri/Aptos/Arial or wrong-size leakage in ordinary-text scope.
- [ ] Cover-page/heading/TOC display typography is untouched (not forced
      to 13pt).

## Visual (run `render_qa.py`, then actually look at every page)

- [ ] Every page was rendered and visually inspected — not just skimmed.
- [ ] No text overflow/clipping.
- [ ] No orphaned headings (a heading alone at the bottom of a page with
      its content pushed to the next).
- [ ] No broken/misaligned tables.
- [ ] No unexpected blank pages (`render_qa.py` flags near-100%-white
      pages automatically, but confirm each flagged page by eye).
- [ ] No lost logos/images.
- [ ] Table widths look correct (not collapsed to near-zero on any column).
- [ ] Landscape appendix sections (if any) actually render landscape.
- [ ] Numbering displays correctly and doesn't visibly drift/restart
      unexpectedly.
- [ ] Header/footer/page-number fields are visible on the expected pages.

## Content preservation (format-only requests)

- [ ] If the user asked for format-only changes: wording, punctuation,
      figures, dates, names, references, tables, appendices, and ordering
      are unchanged except for structural-numbering conversions (manual →
      real Word numbering), which must remain semantically identical
      wording.

## Before delivering

- [ ] `validate_sbsi_docx.py` printed `PASS` (zero `ERROR:` lines).
- [ ] Every `WARNING:` line was read and either judged non-blocking with a
      reason, or fixed.
- [ ] Every rendered page from `render_qa.py` was opened and looked at.
- [ ] The file was written to a new path — the selected template file and
      any scratch copy were never overwritten in place.
