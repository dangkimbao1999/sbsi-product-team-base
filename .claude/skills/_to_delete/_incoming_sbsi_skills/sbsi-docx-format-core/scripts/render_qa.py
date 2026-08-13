#!/usr/bin/env python3
"""Render a DOCX to PDF + per-page PNGs for visual QA, with a few automated checks.

Usage:
    python3 render_qa.py <doc.docx> <out_dir> [--expect-min-pages N] [--expect-max-pages N]

What it does:
  1. Converts the DOCX to PDF with LibreOffice (headless).
  2. Rasterizes every page to a PNG at 150 DPI in <out_dir>/pages/.
  3. Runs cheap automated heuristics:
       - page count sanity (vs --expect-min-pages/--expect-max-pages, if given)
       - flags pages that are >99.5% blank pixels (possible unexpected blank page)
  4. Prints the PNG paths so an agent/human can actually LOOK at every page —
     structural validation (validate_sbsi_docx.py) is necessary but not
     sufficient; this script does not replace visually inspecting the pages
     for overflow, orphaned headings, broken tables, lost logos, wrong
     orientation, or misaligned indents (see references/QA_CHECKLIST.md).

Known limitation: LibreOffice's rendering is a close but NOT pixel-perfect
proxy for Microsoft Word — in particular, Word/LibreOffice can differ on
how a paragraph-level `numPr numId="0"` override (explicit "remove
numbering") is honored. Treat this as a strong visual-QA proxy, not a
guarantee of Word-identical rendering; a final human check in real Word
before distribution is still recommended for high-stakes documents.
"""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path


def convert_to_pdf(doc: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(doc)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {result.stdout}\n{result.stderr}")
    pdf_path = out_dir / (doc.stem + ".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"Expected PDF not found at {pdf_path}")
    return pdf_path


def rasterize(pdf_path: Path, pages_dir: Path) -> list[Path]:
    pages_dir.mkdir(parents=True, exist_ok=True)
    prefix = pages_dir / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "150", str(pdf_path), str(prefix)],
        check=True,
        capture_output=True,
        timeout=120,
    )
    return sorted(pages_dir.glob("page-*.png"))


def blank_ratio(png_path: Path) -> float:
    try:
        from PIL import Image
    except ImportError:
        return -1.0  # PIL unavailable: skip this heuristic rather than fail
    img = Image.open(png_path).convert("L")
    hist = img.histogram()
    total = sum(hist)
    near_white = sum(hist[250:256])
    return near_white / total if total else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("doc", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--expect-min-pages", type=int)
    ap.add_argument("--expect-max-pages", type=int)
    args = ap.parse_args()

    warnings: list[str] = []
    pdf_path = convert_to_pdf(args.doc, args.out_dir)
    pages = rasterize(pdf_path, args.out_dir / "pages")

    n = len(pages)
    if args.expect_min_pages and n < args.expect_min_pages:
        warnings.append(f"Rendered page count {n} is below expected minimum {args.expect_min_pages}")
    if args.expect_max_pages and n > args.expect_max_pages:
        warnings.append(f"Rendered page count {n} is above expected maximum {args.expect_max_pages}")

    for p in pages:
        ratio = blank_ratio(p)
        if ratio < 0:
            continue
        if ratio > 0.995:
            warnings.append(f"Possible unexpected blank page: {p.name} ({ratio:.4%} near-white pixels)")

    print(f"Rendered {n} page(s) to {args.out_dir / 'pages'}")
    for p in pages:
        print("  page:", p)
    for w in warnings:
        print("WARNING:", w)
    print("NEXT STEP: visually inspect each PNG above against references/QA_CHECKLIST.md's Visual section before delivering.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
