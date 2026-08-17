#!/usr/bin/env python3
"""Shared OOXML helpers for validate_sbsi_docx.py and normalize_ordinary_text.py.

IMPORTANT — genericity contract (see references/FORMAT_CONVENTIONS.md and
references/format_contract.json, the machine-readable mirror of the same
rules): this module must never hardcode business content from any one SBSI
document (specific article names, specific chapter numbers, specific
company/org text such as a signature-block name). Every document-specific
tuning knob belongs in a per-template "manifest" JSON (see load_manifest())
supplied by whoever registers that template in sbsi-template-router, not in
this file. The document-type-AGNOSTIC contract values (target font/size,
default heading/appendix patterns, display-size threshold) are loaded from
references/format_contract.json at import time — that JSON is the single
source of truth; edit it, not the literals here, when the SBSI-wide
contract itself changes.
"""
from __future__ import annotations
import copy
import json
import re
from pathlib import Path
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

# Single source of truth for the document-type-agnostic contract values
# below: references/format_contract.json (sibling to this skill's
# scripts/ dir). The JSON is authoritative for the literal values; this
# module only turns them into the shapes the scripts need (compiled-ready
# regex source strings, etc). Missing/unreadable contract is a hard error
# (no-fallbacks) — these values are load-bearing for every check.
_CONTRACT_PATH = Path(__file__).parent.parent / "references" / "format_contract.json"


def _load_contract() -> dict:
    if not _CONTRACT_PATH.exists():
        raise FileNotFoundError(
            f"Required format contract not found: {_CONTRACT_PATH}"
        )
    return json.loads(_CONTRACT_PATH.read_text(encoding="utf-8"))


_CONTRACT = _load_contract()

# Half-points. 13pt ordinary text == sz/szCs val "26".
TARGET_FONT_DISPLAY = _CONTRACT["ordinary_text_typography"]["font_name"]
TARGET_FONT = TARGET_FONT_DISPLAY.lower()
TARGET_SZ = str(_CONTRACT["ordinary_text_typography"]["size_half_points"])
TARGET_FONT_SLOTS = _CONTRACT["ordinary_text_typography"]["font_slots"]

# Generic, template-independent default patterns for text that LOOKS like a
# structural Vietnamese legal-drafting heading (Chương/Điều/Mục/Phần). These
# are structural-vocabulary defaults, not one document's business content —
# every SBSI governance document type can plausibly use this vocabulary.
# A template can extend/replace this list via its manifest's
# "structural_heading_patterns".
DEFAULT_HEADING_PATTERNS = _CONTRACT["structural_headings"]["default_patterns"]

# Generic default marker for "appendix territory": a section where manual
# reference-list numbering (e.g. a bibliography of legal citations) is a
# known, tolerated SBSI drafting convention. "Phụ lục" is the generic
# Vietnamese structural word for "Appendix" (like "Appendix" in English) —
# used across every SBSI document type by definition, not specific business
# content from one document. A template manifest can override this.
DEFAULT_APPENDIX_PATTERN = _CONTRACT["structural_numbering"]["appendix_exception"]["default_marker_pattern"]


def resolved_typography(manifest: dict) -> tuple[str, str, str]:
    """(font_lower, font_display, size_half_points_str) for ordinary text.

    One shared engine runs against every SBSI document type, but the exact
    typography value is a per-template fact, not a hardcoded global: most
    governance templates use the format_contract.json default (TNR 13pt),
    while a template with its own long-standing, verified convention (e.g.
    BRD's TNR 12pt, owned by PTSP) declares an explicit override via its own
    manifest's "typography_profile" — never guessed, never silently forced
    onto the global default.
    """
    profile = manifest.get("typography_profile")
    if not profile:
        return TARGET_FONT, TARGET_FONT_DISPLAY, TARGET_SZ
    font_display = profile["font_name"]
    return font_display.lower(), font_display, str(profile["size_half_points"])


def requires_real_headings(manifest: dict) -> bool:
    """Whether this template's body must use real Word outline-level headings.

    Default True (the standard SBSI governance-document expectation). A
    template whose own verified, established design has no real heading
    styles for its top-level sections (e.g. BRD's 13 numbered sections are
    large/bold Normal text, a PTSP template decision, not an oversight) sets
    "requires_real_headings": false in its manifest — this is a structural
    exception recorded explicitly per template, the same mechanism as
    cover_page_strategy/appendix_heading_pattern, not a hardcoded carve-out
    for one document type in the engine itself.
    """
    return bool(manifest.get("requires_real_headings", True))


def qn(local: str) -> str:
    return f"{{{W}}}{local}"


def load_docx_parts(path: Path) -> dict:
    import zipfile

    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def load_manifest(manifest_path: Path | None) -> dict:
    """Load a template manifest. Returns {} (generic defaults apply) if none given.

    Missing manifest is NOT an error — the engine has safe generic defaults.
    An explicitly-passed but unreadable/invalid manifest IS an error (fail
    loud rather than silently ignoring a broken config), per this repo's
    no-fallbacks rule.
    """
    if manifest_path is None:
        return {}
    if not manifest_path.exists():
        raise FileNotFoundError(f"--manifest given but not found: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def text_of(el) -> str:
    return "".join(el.xpath(".//w:t/text()", namespaces=NS))


def style_meta(styles_root) -> dict:
    """Map styleId -> {based, outline, node} across the stylesheet."""
    out = {}
    for s in styles_root.xpath("./w:style", namespaces=NS):
        sid = s.get(qn("styleId"))
        based = s.xpath("./w:basedOn/@w:val", namespaces=NS)
        outline = s.xpath("./w:pPr/w:outlineLvl/@w:val", namespaces=NS)
        out[sid] = {
            "based": based[0] if based else None,
            "outline": int(outline[0]) if outline else None,
            "node": s,
        }
    return out


def p_style_id(p) -> str:
    v = p.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
    return v[0] if v else "Normal"


def p_direct_outline(p):
    v = p.xpath("./w:pPr/w:outlineLvl/@w:val", namespaces=NS)
    return int(v[0]) if v else None


def resolved_outline(style_id, smap):
    """Outline level for a style, walking basedOn chain. None if not a heading."""
    seen = set()
    sid = style_id
    while sid and sid not in seen:
        seen.add(sid)
        meta = smap.get(sid, {})
        if meta.get("outline") is not None:
            return meta["outline"]
        sid = meta.get("based")
    return None


def effective_outline(p, smap):
    """A real Word heading level (0-8) or None. Level 9 == 'Body Text' (not a heading)."""
    direct = p_direct_outline(p)
    lvl = direct if direct is not None else resolved_outline(p_style_id(p), smap)
    if lvl is not None and lvl <= 8:
        return lvl
    return None


def is_toc_style(p) -> bool:
    sid = p_style_id(p)
    return sid.lower().startswith("toc")


def has_page_break_before(p) -> bool:
    if p.xpath("./w:pPr/w:pageBreakBefore", namespaces=NS):
        return True
    # explicit inline page-break run (<w:br w:type="page"/>) also starts a new page
    if p.xpath(".//w:br[@w:type='page']", namespaces=NS):
        return True
    return False


def cover_page_boundary_index(body_paragraphs, manifest: dict):
    """Index of the first paragraph considered 'body' (not cover-page front matter).

    Generic structural strategy (no document text matching): the cover page
    is everything before the first paragraph that starts a new page via
    pageBreakBefore or an explicit page-break run. This matches the common
    SBSI convention of cover + doc-info table + TOC on page 1, body from
    page 2 (see references/FORMAT_CONVENTIONS.md). A manifest may set
    "cover_page_strategy": "none" to disable this exclusion (validate/
    normalize the whole document) for a template that has no distinct cover.
    """
    strategy = manifest.get("cover_page_strategy", "page_break_before")
    if strategy == "none":
        return 0
    for i, p in enumerate(body_paragraphs):
        if has_page_break_before(p):
            return i
    # No page break found: fail safe by validating/normalizing everything
    # rather than silently skipping the whole document (no-silent-fallback).
    return 0


def heading_patterns(manifest: dict):
    pats = list(DEFAULT_HEADING_PATTERNS)
    pats += manifest.get("structural_heading_patterns", [])
    return [re.compile(p, re.IGNORECASE) for p in pats]


def appendix_pattern(manifest: dict):
    pat = manifest.get("appendix_heading_pattern", DEFAULT_APPENDIX_PATTERN)
    return re.compile(pat, re.IGNORECASE)


DEFAULT_CHAPTER_BOUNDARY_PATTERN = _CONTRACT["structural_numbering"]["appendix_exception"]["zone_bounded_by_chapter_boundary_pattern"]


def chapter_boundary_pattern(manifest: dict):
    pat = manifest.get("chapter_boundary_pattern", DEFAULT_CHAPTER_BOUNDARY_PATTERN)
    return re.compile(pat, re.IGNORECASE)


def appendix_zone_mask(body_paragraphs, appendix_re, chapter_boundary_re) -> list[bool]:
    """Per-paragraph "is this inside a tolerated appendix zone" flags.

    NOT open-ended once triggered: the zone runs from an appendix-marker
    paragraph until the next paragraph matching chapter_boundary_re (a new
    Chương/Phần), or end of document — whichever comes first. A single
    forward pass, computed once per validation run (replaces the old
    per-paragraph O(n) rescan in in_appendix_zone, which was also
    unboundedly sticky: see format_contract.json's appendix_exception.zone_note
    for why an unbounded zone silently hides real numbering violations in
    every chapter that follows a mid-document appendix cross-reference).
    """
    mask = []
    in_zone = False
    for p in body_paragraphs:
        t = text_of(p).strip()
        if in_zone and chapter_boundary_re.match(t):
            in_zone = False
        if appendix_re.match(t):
            in_zone = True
        mask.append(in_zone)
    return mask


# Half-points, added on TOP of the selected template's own resolved ordinary
# target size (see resolved_typography — NOT a fixed absolute pt value: a
# template with a different ordinary baseline, e.g. BRD's 12pt vs the 13pt
# governance default, must have its display-typography margin computed
# relative to ITS OWN baseline, or a legitimate 14pt bold pseudo-heading on a
# 12pt-baseline template would be misclassified as an ordinary-text error).
# A DIRECT (not style-inherited) run/paragraph-mark font-size override more
# than this margin above the template's own ordinary size is treated as
# deliberate display/title typography (e.g. a repeated document title on a
# promulgation page, or a bold non-outline-level section marker), exempt
# from the ordinary-text typography rule — the same category as a
# cover-page title, just not always physically on page 1. This is a
# structural/magnitude signal (nobody accidentally sets ordinary body text
# 1+pt oversized), not a text match, so it generalizes across templates. A
# genuine ordinary-text sizing mistake stays well under this margin and is
# still caught.
DISPLAY_SIZE_MARGIN_HALF_POINTS = _CONTRACT["ordinary_text_typography"]["display_size_margin_above_ordinary_half_points"]


def _direct_sizes(rpr):
    if rpr is None:
        return []
    vals = []
    for tag in ("sz", "szCs"):
        for n in rpr.findall(qn(tag)):
            v = n.get(qn("val"))
            if v and v.isdigit():
                vals.append(int(v))
    return vals


def has_large_display_override(p, target_sz: str) -> bool:
    sizes = []
    ppr_rpr = p.xpath("./w:pPr/w:rPr", namespaces=NS)
    if ppr_rpr:
        sizes += _direct_sizes(ppr_rpr[0])
    for r in p.xpath("./w:r", namespaces=NS):
        sizes += _direct_sizes(r.find(qn("rPr")))
    threshold = int(target_sz) + DISPLAY_SIZE_MARGIN_HALF_POINTS
    return bool(sizes) and any(s > threshold for s in sizes)


def is_ordinary_text_exempt(p, smap, target_sz: str) -> bool:
    """True if p is a heading, a TOC entry, or deliberate large-font display
    typography (relative to the selected template's own ordinary target
    size) — i.e. NOT in scope for the ordinary-text typography rule."""
    return (
        effective_outline(p, smap) is not None
        or is_toc_style(p)
        or has_large_display_override(p, target_sz)
    )


def numbering_id(p):
    v = p.xpath("./w:pPr/w:numPr/w:numId/@w:val", namespaces=NS)
    if not v:
        return None
    # numId "0" is the explicit "no numbering" sentinel in OOXML.
    return None if v[0] == "0" else v[0]


# ---------------------------------------------------------------------------
# Generation helpers — building NEW structural content the correct way.
#
# These exist because of a real, observed failure (2026-08-17,
# QT_Nghien_cuu_va_Phat_trien_SPDV_so_(PC1)_reformatted.docx): new chapter
# headings were built as a single hand-rolled paragraph with the wrong
# style, no direct outlineLvl override, and "Chương I" typed as literal
# text — passing visual inspection but failing every Word-native-features
# guarantee (Navigation Pane, TOC field, auto-renumbering on insert/delete).
# validate_sbsi_docx.py catches this AFTER the fact; these helpers exist so
# there's a correct, low-effort path that never produces it in the first
# place. Always prefer these over hand-rolling numPr/outlineLvl XML.
# ---------------------------------------------------------------------------


def clone_structural_paragraph(ref_para, new_text: str):
    """Deep-clone a reference structural paragraph's formatting (pStyle,
    numPr, direct outlineLvl, run formatting), replacing only its text.

    This is the correct way to add a new Chương/Điều/Khoản/Điểm paragraph:
    find an EXISTING paragraph in the document that already has the real
    Word numbering/outline-level setup you want (see a template's manifest
    — e.g. quy-trinh/template_manifest.json's `chuong_structure` and
    `dieu_numbering` — for which paragraph to use as reference for that
    template), then call this instead of constructing pPr/numPr from
    scratch or, worse, typing the structural prefix as literal text.

    Keeps ref_para's numPr EXACTLY as-is, including the two meaningful
    "no explicit numId" states: a paragraph with no numId at all (inherits
    active numbering from its style — used by e.g. this template's Chương
    number-paragraph) and a paragraph with numId="0" (explicit "no
    numbering here" sentinel — used by e.g. the Chương title-paragraph
    immediately after it). Only the first run's text is replaced; any
    additional runs are dropped, since a structural heading/clause is
    expected to be a single run of plain text.

    Raises ValueError if ref_para has no runs — for a reference paragraph
    that is itself meant to stay textless (e.g. a Chương number-only
    paragraph), use clone_empty_structural_paragraph instead; there is
    nothing to replace new_text into.
    """
    new_p = copy.deepcopy(ref_para)
    runs = new_p.xpath("./w:r", namespaces=NS)
    if not runs:
        raise ValueError(
            "clone_structural_paragraph: reference paragraph has no runs to "
            "clone text-run formatting from — use "
            "clone_empty_structural_paragraph for a textless reference "
            "(e.g. a Chương number-only paragraph)."
        )
    first_run = runs[0]
    for extra in runs[1:]:
        new_p.remove(extra)
    for t in first_run.xpath("./w:t", namespaces=NS):
        first_run.remove(t)
    new_t = etree.SubElement(first_run, qn("t"))
    new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    new_t.text = new_text
    return new_p


def clone_empty_structural_paragraph(ref_para):
    """Deep-clone a reference paragraph that carries no text of its own.

    Used for e.g. the empty "number-only" paragraph half of the Chương
    two-paragraph pattern (see a template's manifest `chuong_structure`,
    e.g. quy-trinh's), whose sole job is to let its style-inherited active
    numbering render (e.g. "Chương I") — nothing about it needs to change
    per new chapter, so this is a plain deep copy rather than a text swap.
    """
    return copy.deepcopy(ref_para)


def build_new_chapter_paragraphs(number_para_ref, title_para_ref, title_text: str):
    """Build the (number_paragraph, title_paragraph) pair for a new Chương.

    number_para_ref / title_para_ref must be the two sibling paragraphs of
    an EXISTING chapter in the same document (see a template's manifest's
    `chuong_structure.verified_example` for which indices/paragraphs those
    are for a given template). Insert the returned pair adjacently, in
    order, at the desired location — never insert only one of them.
    """
    number_p = clone_empty_structural_paragraph(number_para_ref)
    title_p = clone_structural_paragraph(title_para_ref, title_text)
    return number_p, title_p


def build_toc_field_paragraph(
    switches: str = '\\o "1-3" \\h \\z \\u',
    placeholder_text: str = "Nhấn Ctrl+A rồi F9 trong Word để cập nhật Mục lục.",
):
    """Build a real Word TOC field paragraph — fldChar begin -> instrText
    'TOC <switches>' -> fldChar separate -> cached placeholder run ->
    fldChar end. This is the correct replacement for a manually typed
    dot-leader "Mục lục" block (see FORMAT_CONVENTIONS.md §4) — the
    resulting paragraph responds to Ctrl+A -> F9 in Word like any other
    native TOC.

    `switches` should come from the SELECTED template's own manifest
    `toc_field_switches` note when reformatting a document that already had
    a real TOC (reuse the same switches the template's own TOC used —
    don't invent different ones). The returned paragraph has no pStyle set
    — apply the template's own TOC-heading-adjacent paragraph style
    (commonly "TOC1"/"TOC2"/...) by cloning a real TOC-entry paragraph's
    pPr the same way clone_structural_paragraph does, if the template's TOC
    entries need one.

    Caller is responsible for also setting word/settings.xml's
    <w:updateFields w:val="true"/> so Word offers to refresh on open (see
    normalize_ordinary_text.py, which already does this) — this function
    only builds the field paragraph itself.
    """
    p = etree.Element(qn("p"))
    r1 = etree.SubElement(p, qn("r"))
    fld1 = etree.SubElement(r1, qn("fldChar"))
    fld1.set(qn("fldCharType"), "begin")
    r2 = etree.SubElement(p, qn("r"))
    instr = etree.SubElement(r2, qn("instrText"))
    instr.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    instr.text = f" TOC {switches} "
    r3 = etree.SubElement(p, qn("r"))
    fld3 = etree.SubElement(r3, qn("fldChar"))
    fld3.set(qn("fldCharType"), "separate")
    r4 = etree.SubElement(p, qn("r"))
    t4 = etree.SubElement(r4, qn("t"))
    t4.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t4.text = placeholder_text
    r5 = etree.SubElement(p, qn("r"))
    fld5 = etree.SubElement(r5, qn("fldChar"))
    fld5.set(qn("fldCharType"), "end")
    return p
