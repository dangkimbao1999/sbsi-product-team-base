#!/usr/bin/env python3
"""Resolve the SBSI document type + registered template for a request.

Usage:
    python3 resolve_template.py --type "Quy trình" --registry template_registry.json
    python3 resolve_template.py --doc source.docx --registry template_registry.json
    python3 resolve_template.py --type "Quy trình" --doc source.docx --registry template_registry.json

Resolution order (strongest evidence first — see references/TEMPLATE_ROUTING_RULES.md):
  1. Explicit --type (the user's stated intent for THIS request).
  2. Strong body markers in --doc (exact document-type title line, e.g. "QUY TRÌNH").
  3. Weak filename hint in --doc's name (last resort only).

If --type and detected --doc type disagree: DOCUMENT_TYPE_CONFLICT (blocking,
must not guess). If the resolved type has no registered template:
TEMPLATE_NOT_REGISTERED (blocking, never substitute another type's template).

Prints one JSON object to stdout and returns a matching non-zero exit code
for every non-RESOLVED status, so a caller can both parse the result and
fail a CI-style pipeline on a bad `$?` without re-parsing JSON.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

EXIT_BY_STATUS = {
    "RESOLVED": 0,
    "DOCUMENT_TYPE_AMBIGUOUS": 2,
    "DOCUMENT_TYPE_CONFLICT": 3,
    "TEMPLATE_NOT_REGISTERED": 4,
    "TEMPLATE_TYPE_MISMATCH": 5,
}


def load_registry(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def canonicalize(value: str, entries: list) -> dict | None:
    n = norm(value)
    for e in entries:
        candidates = [e["document_type"], e.get("display_name", "")] + e.get("aliases", [])
        if any(n == norm(v) for v in candidates if v):
            return e
    return None


def doc_paragraph_text(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as z:
        root = etree.fromstring(z.read("word/document.xml"))
        out = []
        for p in root.xpath(".//w:p", namespaces=NS):
            t = "".join(p.xpath(".//w:t/text()", namespaces=NS)).strip()
            if t:
                out.append(t)
        return out[:400]


def detect_from_doc(docx_path: Path, entries: list):
    paras = doc_paragraph_text(docx_path)
    joined = "\n".join(paras[:120])
    strong = []
    for e in entries:
        for marker in e.get("required_markers", []):
            if re.search(rf"(^|\n)\s*{re.escape(marker)}\s*($|\n)", joined, re.I):
                strong.append((e, marker))
                break
    uniq = {e[0]["document_type"]: e for e in strong}
    if len(uniq) == 1:
        e, marker = next(iter(uniq.values()))
        return e, "HIGH", f"exact document marker: {marker}"
    if len(uniq) > 1:
        return None, "CONFLICT", "multiple document-type markers found in the same document"
    # weak filename fallback — only short, unambiguous alias tokens
    stem = norm(docx_path.stem).replace("_", " ").replace("-", " ")
    for e in entries:
        for a in e.get("aliases", []):
            if len(norm(a)) <= 3 and re.search(rf"\b{re.escape(norm(a))}\b", stem):
                return e, "LOW", f"filename hint: {a}"
    return None, "NONE", "no reliable document-type evidence"


def verify_template_type(registry_path: Path, entry: dict):
    tp = (registry_path.parent / entry["template_path"]).resolve()
    if not tp.exists():
        return False, tp, "registered template file is missing on disk"
    paras = doc_paragraph_text(tp)
    top = "\n".join(paras[:120])
    markers = entry.get("required_markers", [])
    if markers and not any(re.search(rf"(^|\n)\s*{re.escape(m)}\s*($|\n)", top, re.I) for m in markers):
        return False, tp, "registered template does not contain any of its own required type markers"
    return True, tp, "ok"


def resolved_manifest_path(registry_path: Path, entry: dict):
    mp = entry.get("manifest_path")
    if not mp:
        return None
    p = (registry_path.parent / mp).resolve()
    return str(p) if p.exists() else None


def emit(status: str, **fields) -> int:
    print(json.dumps({"status": status, **fields}, ensure_ascii=False, indent=2))
    return EXIT_BY_STATUS[status]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True, type=Path)
    ap.add_argument("--type")
    ap.add_argument("--doc", type=Path)
    args = ap.parse_args()

    registry = load_registry(args.registry)
    entries = registry["templates"]

    explicit = canonicalize(args.type, entries) if args.type else None
    if args.type and not explicit:
        return emit("DOCUMENT_TYPE_AMBIGUOUS", evidence=f"unknown explicit type: {args.type}")

    detected = confidence = evidence = None
    if args.doc:
        detected, confidence, evidence = detect_from_doc(args.doc, entries)
        if confidence == "CONFLICT":
            return emit("DOCUMENT_TYPE_AMBIGUOUS", evidence=evidence)

    if explicit and detected and explicit["document_type"] != detected["document_type"]:
        return emit(
            "DOCUMENT_TYPE_CONFLICT",
            explicit=explicit["document_type"],
            detected=detected["document_type"],
            evidence=evidence,
        )

    selected = explicit or detected
    if not selected:
        return emit("DOCUMENT_TYPE_AMBIGUOUS", evidence=evidence or "no explicit type or reliable source marker")

    if not selected.get("supported") or not selected.get("template_path"):
        return emit(
            "TEMPLATE_NOT_REGISTERED",
            document_type=selected["document_type"],
            display_name=selected.get("display_name"),
        )

    ok, tp, msg = verify_template_type(args.registry, selected)
    if not ok:
        return emit(
            "TEMPLATE_TYPE_MISMATCH",
            document_type=selected["document_type"],
            template_path=str(tp),
            evidence=msg,
        )

    return emit(
        "RESOLVED",
        document_type=selected["document_type"],
        display_name=selected.get("display_name"),
        template_id=selected.get("template_id"),
        template_path=str(tp),
        manifest_path=resolved_manifest_path(args.registry, selected),
        confidence="EXPLICIT" if explicit else confidence,
        evidence="explicit user type" if explicit else evidence,
    )


if __name__ == "__main__":
    sys.exit(main())
