#!/usr/bin/env python3
"""Shared OOXML helpers for validate_sbsi_docx.py and normalize_ordinary_text.py.

IMPORTANT — genericity contract (see references/FORMAT_CONVENTIONS.md):
This module must never hardcode business content from any one SBSI document
(specific article names, specific chapter numbers, specific company/org
text such as a signature-block name). Every document-specific tuning knob
belongs in a per-template "manifest" JSON (see load_manifest()) supplied by
whoever registers that template in sbsi-template-router, not in this file.
Only *structural* Word conventions (outline levels, real numPr numbering,
page breaks, TOC fields, style names) may be hardcoded here, because those
are OOXML-level concepts, not one document's business content.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

# Half-points. 13pt ordinary text == sz/szCs val "26".
TARGET_FONT = "times new roman"
TARGET_SZ = "26"

# Generic, template-independent default patterns for text that LOOKS like a
# structural Vietnamese legal-drafting heading (Chương/Điều/Mục/Phần). These
# are structural-vocabulary defaults, not one document's business content —
# every SBSI governance document type can plausibly use this vocabulary.
# A template can extend/replace this list via its manifest's
# "structural_heading_patterns".
DEFAULT_HEADING_PATTERNS = [
    r"^Chương\s+[IVXLCDM]+\b",  # Chương I, II, ...
    r"^Điều\s+\d+[\.\)]?\s*\S",  # Điều 1. ...
    r"^Mục\s+\d+[\.\)]?\s*\S",  # Mục 1. ...
    r"^Phần\s+[IVXLCDM\d]+\b",  # Phần I / Phần 1
]

# Generic default marker for "appendix territory": a section where manual
# reference-list numbering (e.g. a bibliography of legal citations) is a
# known, tolerated SBSI drafting convention. "Phụ lục" is the generic
# Vietnamese structural word for "Appendix" (like "Appendix" in English) —
# used across every SBSI document type by definition, not specific business
# content from one document. A template manifest can override this.
DEFAULT_APPENDIX_PATTERN = r"^(Phụ\s*lục|PHỤ\s*LỤC|Appendix)\b"


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


def in_appendix_zone(idx: int, body_paragraphs, appendix_re) -> bool:
    """True once any preceding paragraph's text matched the appendix marker."""
    for j in range(idx + 1):
        if appendix_re.match(text_of(body_paragraphs[j]).strip()):
            return True
    return False


# Half-points. A DIRECT (not style-inherited) run/paragraph-mark font-size
# override above this is treated as deliberate display/title typography
# (e.g. a repeated document title on a promulgation page), exempt from the
# ordinary-text TNR-13pt rule — the same category as a cover-page title,
# just not always physically on page 1. This is a structural/magnitude
# signal (nobody accidentally sets ordinary body text to >14pt), not a
# text match, so it generalizes across templates. A genuine ordinary-text
# sizing mistake (e.g. 12pt body text) stays well under this threshold and
# is still caught.
DISPLAY_SIZE_THRESHOLD_HALF_POINTS = 28


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


def has_large_display_override(p) -> bool:
    sizes = []
    ppr_rpr = p.xpath("./w:pPr/w:rPr", namespaces=NS)
    if ppr_rpr:
        sizes += _direct_sizes(ppr_rpr[0])
    for r in p.xpath("./w:r", namespaces=NS):
        sizes += _direct_sizes(r.find(qn("rPr")))
    return bool(sizes) and any(s > DISPLAY_SIZE_THRESHOLD_HALF_POINTS for s in sizes)


def is_ordinary_text_exempt(p, smap) -> bool:
    """True if p is a heading, a TOC entry, or deliberate large-font display
    typography — i.e. NOT in scope for the ordinary-text TNR-13pt rule."""
    return (
        effective_outline(p, smap) is not None
        or is_toc_style(p)
        or has_large_display_override(p)
    )


def numbering_id(p):
    v = p.xpath("./w:pPr/w:numPr/w:numId/@w:val", namespaces=NS)
    if not v:
        return None
    # numId "0" is the explicit "no numbering" sentinel in OOXML.
    return None if v[0] == "0" else v[0]
