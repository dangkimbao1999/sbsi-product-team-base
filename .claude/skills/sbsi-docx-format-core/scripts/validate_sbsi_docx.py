#!/usr/bin/env python3
"""Validate an SBSI DOCX against sbsi-docx-format-core's structural/typography rules.

Usage:
    python3 validate_sbsi_docx.py --doc <output.docx> [--template <selected_template.docx>] \
        [--manifest <template_manifest.json>]

Checks (see references/FORMAT_CONVENTIONS.md for the full rule text):
  1. Fonts      — ordinary text is Times New Roman exactly 13pt.
  2. Headings   — real heading/outline styles exist and are used; no fake
                  (bold-Normal) headings mimicking structural vocabulary.
  3. Numbering  — structural list numbering (Khoản/Điểm-style) uses real
                  Word numPr, not typed "1." / "a)" prefixes.
  4. TOC        — a real Word TOC field exists when the document has a
                  table-of-contents heading.
  5. Sections   — section/page setup is preserved from the selected template
                  (only checked when --template is given).
  6. Header/footer — header/footer parts are not dropped relative to the
                  selected template (only checked when --template is given).

Any ERROR is blocking — the file must not be delivered. WARNINGs are
non-blocking but must be surfaced, never silently dropped.

This script intentionally contains NO document-specific business content
(no hardcoded article names, chapter numbers, or one org's signature text).
Template-specific structural exceptions belong in a manifest — see
_sbsi_docx_common.py's module docstring and load_manifest().
"""
from __future__ import annotations
import argparse
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree

sys.path.insert(0, str(Path(__file__).parent))
from _sbsi_docx_common import (  # noqa: E402
    NS,
    qn,
    text_of,
    style_meta,
    p_style_id,
    effective_outline,
    is_toc_style,
    is_ordinary_text_exempt,
    load_manifest,
    cover_page_boundary_index,
    heading_patterns,
    appendix_pattern,
    in_appendix_zone,
    numbering_id,
    TARGET_FONT,
    TARGET_SZ,
)


def attr_vals(rpr, tag, attrs):
    if rpr is None:
        return []
    out = []
    for n in rpr.findall(qn(tag)):
        for a in attrs:
            v = n.get(qn(a))
            if v:
                out.append(v)
    return out


def effective_style_rpr(styles_root, smap, sid):
    """Walk a style's basedOn chain (falling back to docDefaults) for font/size."""
    fonts, sizes = [], []
    seen = set()
    while sid and sid not in seen:
        seen.add(sid)
        node = smap.get(sid, {}).get("node")
        if node is not None:
            rpr = node.find(qn("rPr"))
            if not fonts:
                fonts = attr_vals(rpr, "rFonts", ["ascii", "hAnsi", "eastAsia", "cs"])
            if not sizes:
                sizes = attr_vals(rpr, "sz", ["val"]) + attr_vals(rpr, "szCs", ["val"])
        sid = smap.get(sid, {}).get("based")
    if not fonts or not sizes:
        ds = styles_root.xpath("./w:docDefaults/w:rPrDefault/w:rPr", namespaces=NS)
        if ds:
            if not fonts:
                fonts = attr_vals(ds[0], "rFonts", ["ascii", "hAnsi", "eastAsia", "cs"])
            if not sizes:
                sizes = attr_vals(ds[0], "sz", ["val"]) + attr_vals(ds[0], "szCs", ["val"])
    return fonts, sizes


def run_is_tnr13(r, p, styles_root, smap):
    rpr = r.find(qn("rPr"))
    fonts = attr_vals(rpr, "rFonts", ["ascii", "hAnsi", "eastAsia", "cs"])
    sizes = attr_vals(rpr, "sz", ["val"]) + attr_vals(rpr, "szCs", ["val"])
    if not fonts or not sizes:
        sf, ss = effective_style_rpr(styles_root, smap, p_style_id(p))
        fonts = fonts or sf
        sizes = sizes or ss
    if not fonts or not sizes:
        return False
    fonts_ok = all(f.strip().lower() == TARGET_FONT for f in fonts)
    sizes_ok = all(str(s) == TARGET_SZ for s in sizes)
    return fonts_ok and sizes_ok


def sect_signature(doc_root):
    sig = []
    for s in doc_root.xpath(".//w:sectPr", namespaces=NS):
        row = []
        for child in ["pgSz", "pgMar", "headerReference", "footerReference", "type"]:
            for e in s.findall(qn(child)):
                row.append((child, tuple(sorted((etree.QName(k).localname, v) for k, v in e.attrib.items()))))
        sig.append(tuple(row))
    return sig


NUM_SEQ_RE = re.compile(r"^(\d+)[\.\)]\s+\S")
LETTER_SEQ_RE = re.compile(r"^([a-zđA-ZĐ])\)\s+\S")


def detect_manual_numbering(paragraphs_text_numid):
    """Return list of (start_index, kind, first_text) for detected FAKE sequences.

    A 'sequence' is >=2 consecutive matching paragraphs (ignoring blanks and
    paragraphs that already carry real numPr) whose numbers/letters increase
    by exactly one. A single isolated match is reported by the caller as a
    WARNING instead, to avoid false-positives on ordinary prose that happens
    to start with a digit.
    """
    findings = []
    i = 0
    n = len(paragraphs_text_numid)
    while i < n:
        text, numid = paragraphs_text_numid[i]
        m = NUM_SEQ_RE.match(text)
        kind = None
        if m and numid is None:
            kind = "decimal"
            start_val = int(m.group(1))
        else:
            m = LETTER_SEQ_RE.match(text)
            if m and numid is None:
                kind = "letter"
                start_val = ord(m.group(1).lower())
            else:
                i += 1
                continue
        # look ahead for a continuing sequence
        run_len = 1
        j = i + 1
        expect = start_val + 1
        while j < n:
            t2, n2 = paragraphs_text_numid[j]
            if kind == "decimal":
                m2 = NUM_SEQ_RE.match(t2)
                if m2 and n2 is None and int(m2.group(1)) == expect:
                    run_len += 1
                    expect += 1
                    j += 1
                    continue
            else:
                m2 = LETTER_SEQ_RE.match(t2)
                if m2 and n2 is None and ord(m2.group(1).lower()) == expect:
                    run_len += 1
                    expect += 1
                    j += 1
                    continue
            break
        findings.append((i, kind, text[:100], run_len))
        i = j if run_len > 1 else i + 1
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True, type=Path)
    ap.add_argument("--template", type=Path)
    ap.add_argument("--manifest", type=Path)
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    manifest = load_manifest(args.manifest)

    with zipfile.ZipFile(args.doc) as z:
        names = z.namelist()
        for part in ["word/document.xml", "word/styles.xml", "word/numbering.xml"]:
            if part not in names:
                errors.append(f"[Sections] Missing required part {part}")
        if errors:
            for e in errors:
                print("ERROR:", e)
            return 1

        doc_root = etree.fromstring(z.read("word/document.xml"))
        styles_root = etree.fromstring(z.read("word/styles.xml"))
        smap = style_meta(styles_root)

        body_ps = doc_root.xpath(".//w:body/w:p", namespaces=NS)
        cover_end = cover_page_boundary_index(body_ps, manifest)
        h_pats = heading_patterns(manifest)
        app_re = appendix_pattern(manifest)

        # --- TOC ---
        toc_instr = " ".join(doc_root.xpath(".//w:instrText/text()", namespaces=NS)).upper()
        has_toc_heading = any(
            text_of(p).strip().lower() in {"mục lục", "muc luc", "table of contents"}
            for p in body_ps
        )
        has_real_toc_field = "TOC" in toc_instr
        if has_toc_heading and not has_real_toc_field:
            errors.append("[TOC] A 'Mục lục' heading exists but no real Word TOC field (instrText 'TOC ...') was found")
        if has_real_toc_field and not has_toc_heading:
            warnings.append("[TOC] A real TOC field exists but no 'Mục lục' heading text was found — verify intentional")

        # --- Headings / Fonts / Numbering over body scope ---
        any_heading_used = False
        numbering_scan = []  # (text, numid) for scope-included, non-heading, non-toc paragraphs
        numbering_scan_is_appendix = []

        for idx, p in enumerate(body_ps):
            if idx < cover_end:
                continue  # cover-page front matter: excluded from ordinary checks
            t = text_of(p).strip()
            if not t:
                continue
            outline = effective_outline(p, smap)
            toc_style = is_toc_style(p)

            if outline is not None:
                any_heading_used = True

            # Fake-heading detection: text mimics structural heading vocabulary
            # but has no real outline level.
            if outline is None and not toc_style:
                for pat in h_pats:
                    if pat.match(t):
                        errors.append(f"[Headings] Manual/non-structural heading text (no outline level): {t[:120]}")
                        break

            if outline is not None or toc_style or is_ordinary_text_exempt(p, smap):
                continue  # headings/TOC/display-typography lines: skip font+numbering checks

            # --- Fonts ---
            for r in p.xpath("./w:r", namespaces=NS):
                if text_of(r).strip() and not run_is_tnr13(r, p, styles_root, smap):
                    errors.append(f"[Fonts] Ordinary text is not Times New Roman 13pt: {t[:120]}")
                    break

            # --- Numbering scan (deferred sequence detection below) ---
            is_appendix = in_appendix_zone(idx, body_ps, app_re)
            numbering_scan.append((t, numbering_id(p)))
            numbering_scan_is_appendix.append(is_appendix)

        if not any_heading_used:
            msg = "[Headings] No real heading/outline-level paragraphs found in document body"
            if args.template:
                errors.append(msg + " (selected template defines heading structure — this is blocking)")
            else:
                warnings.append(msg)

        # --- Numbering: split scan into main-body vs appendix runs, detect sequences ---
        main_scan = [x for x, is_app in zip(numbering_scan, numbering_scan_is_appendix) if not is_app]
        app_scan = [x for x, is_app in zip(numbering_scan, numbering_scan_is_appendix) if is_app]

        for text, kind, snippet, run_len in detect_manual_numbering(main_scan):
            if run_len >= 2:
                errors.append(f"[Numbering] Manually-typed {kind} numbering sequence detected (should be real Word numbering): {snippet}")
            else:
                warnings.append(f"[Numbering] Possible manual {kind} numbering (isolated, not blocking): {snippet}")

        for text, kind, snippet, run_len in detect_manual_numbering(app_scan):
            # Appendix reference-list numbering is a tolerated SBSI convention
            # (see DEFAULT_APPENDIX_PATTERN) — always a warning, never blocking.
            warnings.append(f"[Numbering] Manual {kind} numbering inside an appendix (tolerated, verify intentional): {snippet}")

        # --- Sections / Header-Footer (only when a template is given) ---
        if args.template:
            with zipfile.ZipFile(args.template) as tz:
                tnames = tz.namelist()
                tdoc_root = etree.fromstring(tz.read("word/document.xml"))
                if len(sect_signature(doc_root)) != len(sect_signature(tdoc_root)):
                    warnings.append("[Sections] Section count differs from the selected template — verify intentional")
                for prefix in ["word/header", "word/footer"]:
                    label = "header" if prefix.endswith("header") else "footer"
                    tparts = [n for n in tnames if n.startswith(prefix) and n.endswith(".xml")]
                    dparts = [n for n in names if n.startswith(prefix) and n.endswith(".xml")]
                    if tparts and not dparts:
                        errors.append(f"[Header/footer] Selected template has {label} parts but the document has none")

    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        print(f"FAIL: {len(errors)} blocking error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: SBSI DOCX structural/typography checks ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
