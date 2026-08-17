#!/usr/bin/env python3
"""Normalize ordinary DOCX text to the selected template's typography, safely.

Target font/size come from format_contract.json's global default (Times New
Roman 13pt) unless a --manifest overrides it via "typography_profile" (e.g.
BRD's own verified 12pt convention) — see _sbsi_docx_common.resolved_typography.

Usage:
    python3 normalize_ordinary_text.py <input.docx> <output.docx> [--manifest <template_manifest.json>]

What it touches:
  - word/styles.xml docDefaults + Normal/Body Text/List Paragraph styles
    (safe global defaults ordinary text inherits from).
  - Direct run-level font/size overrides on ORDINARY body paragraphs only.

What it never touches (see references/FORMAT_CONVENTIONS.md):
  - Headings / any paragraph with a real outline level (0-8).
  - TOC-styled paragraphs.
  - Cover-page front matter (everything before the first structural page
    break — see _sbsi_docx_common.cover_page_boundary_index).
  - Headers/footers (separate XML parts; this script only edits
    word/document.xml + word/styles.xml, so they are untouched by
    construction, not by a text-matching guess).

It does NOT blindly apply 13pt to every run in the document — that was a
real bug in an earlier version of this script that also silently no-op'd
on any document lacking one specific document's exact signature-block text.
This version identifies scope purely from Word structure (styles/outline/
page-breaks), so it works on any SBSI document, not just one template.
"""
from __future__ import annotations
import argparse
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
    is_ordinary_text_exempt,
    load_manifest,
    cover_page_boundary_index,
    resolved_typography,
    TARGET_FONT_SLOTS,
)


def set_rpr_target(rpr, font_display: str, sz: str):
    fonts = rpr.findall(qn("rFonts"))
    rf = fonts[0] if fonts else etree.SubElement(rpr, qn("rFonts"))
    for extra in fonts[1:]:
        rpr.remove(extra)
    for a in TARGET_FONT_SLOTS:
        rf.set(qn(a), font_display)
    for a in ["asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"]:
        rf.attrib.pop(qn(a), None)
    for tag in ["sz", "szCs"]:
        nodes = rpr.findall(qn(tag))
        node = nodes[0] if nodes else etree.SubElement(rpr, qn(tag))
        for extra in nodes[1:]:
            rpr.remove(extra)
        node.set(qn("val"), sz)


def set_run(r, font_display: str, sz: str):
    rpr = r.find(qn("rPr"))
    if rpr is None:
        rpr = etree.Element(qn("rPr"))
        r.insert(0, rpr)
    set_rpr_target(rpr, font_display, sz)


def normalize(inp: Path, out: Path, manifest: dict):
    _, font_display, sz = resolved_typography(manifest)

    with zipfile.ZipFile(inp, "r") as zin:
        files = {n: zin.read(n) for n in zin.namelist()}

    styles_root = etree.fromstring(files["word/styles.xml"])
    smap = style_meta(styles_root)

    rprdef = styles_root.xpath("./w:docDefaults/w:rPrDefault/w:rPr", namespaces=NS)
    if rprdef:
        set_rpr_target(rprdef[0], font_display, sz)
    for sid in ["Normal", "BodyText", "ListParagraph"]:
        nodes = styles_root.xpath(f"./w:style[@w:styleId='{sid}']", namespaces=NS)
        if nodes:
            rpr = nodes[0].find(qn("rPr"))
            if rpr is None:
                rpr = etree.SubElement(nodes[0], qn("rPr"))
            set_rpr_target(rpr, font_display, sz)
    files["word/styles.xml"] = etree.tostring(styles_root, xml_declaration=True, encoding="UTF-8", standalone="yes")

    doc_root = etree.fromstring(files["word/document.xml"])
    body_ps = doc_root.xpath(".//w:body/w:p", namespaces=NS)
    cover_end = cover_page_boundary_index(body_ps, manifest)

    normalized_count = 0
    for idx, p in enumerate(body_ps):
        if idx < cover_end:
            continue  # cover-page front matter — never touched
        if is_ordinary_text_exempt(p, smap, sz):
            continue  # heading / TOC entry / deliberate display typography — preserve as-is
        ppr_rpr = p.xpath("./w:pPr/w:rPr", namespaces=NS)
        if ppr_rpr:
            set_rpr_target(ppr_rpr[0], font_display, sz)
        for r in p.xpath("./w:r", namespaces=NS):
            if text_of(r):
                set_run(r, font_display, sz)
                normalized_count += 1

    files["word/document.xml"] = etree.tostring(doc_root, xml_declaration=True, encoding="UTF-8", standalone="yes")

    if "word/settings.xml" in files:
        settings_root = etree.fromstring(files["word/settings.xml"])
        uf = settings_root.find(qn("updateFields"))
        if uf is None:
            uf = etree.SubElement(settings_root, qn("updateFields"))
        uf.set(qn("val"), "true")
        files["word/settings.xml"] = etree.tostring(settings_root, xml_declaration=True, encoding="UTF-8", standalone="yes")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)

    print(f"Normalized {normalized_count} ordinary run(s) to {font_display} {int(sz) // 2}pt (cover-page/headings/TOC preserved): {out}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--manifest", type=Path)
    args = ap.parse_args()
    manifest = load_manifest(args.manifest)
    normalize(args.input, args.output, manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
