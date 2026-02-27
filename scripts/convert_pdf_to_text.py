#!/usr/bin/env python3
"""
Convert PDFs from intake directory to text files.

Usage:
    # Single file (Iteration 1)
    python scripts/convert_pdf_to_text.py --file "papers/evaluated/integrated/file.pdf"

    # Batch mode (Iteration 2+)
    python scripts/convert_pdf_to_text.py --batch N          # first N pending PDFs
    python scripts/convert_pdf_to_text.py --all              # all pending PDFs

    # Dry run (show what would be converted)
    python scripts/convert_pdf_to_text.py --all --dry-run

    # Status
    python scripts/convert_pdf_to_text.py --status
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install PyMuPDF")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
INTAKE_DIR = ROOT / "papers" / "evaluated" / "integrated"
MANIFEST = INTAKE_DIR / "fulltext-intake.yaml"
OUTPUT_DIR = INTAKE_DIR  # text output next to PDFs for review


def extract_text_from_pdf(pdf_path: Path) -> dict:
    """Extract text from a PDF using PyMuPDF. Returns dict with text and metadata."""
    doc = fitz.open(str(pdf_path))
    pages = []
    total_chars = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        pages.append(text)
        total_chars += len(text)

    doc.close()

    return {
        "text": "\n\n---\n\n".join(pages),
        "page_count": len(pages),
        "total_chars": total_chars,
        "empty_pages": sum(1 for p in pages if len(p.strip()) < 10),
    }


def assess_quality(result: dict) -> dict:
    """Assess extraction quality."""
    quality = {
        "chars_per_page": result["total_chars"] / max(result["page_count"], 1),
        "empty_page_ratio": result["empty_pages"] / max(result["page_count"], 1),
    }

    # Quality rating
    if quality["chars_per_page"] < 100:
        quality["rating"] = "POOR"
        quality["issue"] = "Very little text extracted - may be scanned/image PDF"
    elif quality["empty_page_ratio"] > 0.3:
        quality["rating"] = "PARTIAL"
        quality["issue"] = f"{result['empty_pages']}/{result['page_count']} pages empty"
    elif quality["chars_per_page"] < 500:
        quality["rating"] = "LOW"
        quality["issue"] = "Below average text density"
    else:
        quality["rating"] = "GOOD"
        quality["issue"] = None

    return quality


def convert_single(pdf_path: Path, output_path: Path = None) -> dict:
    """Convert a single PDF and return results."""
    if not pdf_path.exists():
        return {"success": False, "error": f"File not found: {pdf_path}"}

    try:
        result = extract_text_from_pdf(pdf_path)
        quality = assess_quality(result)

        # Default output path: same name but .txt
        if output_path is None:
            output_path = pdf_path.with_suffix(".txt")

        # Write output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        return {
            "success": True,
            "input": str(pdf_path.name),
            "output": str(output_path.name),
            "pages": result["page_count"],
            "chars": result["total_chars"],
            "quality": quality["rating"],
            "issue": quality["issue"],
            "output_size_kb": round(output_path.stat().st_size / 1024, 1),
        }

    except Exception as e:
        return {"success": False, "input": str(pdf_path.name), "error": str(e)}


def load_manifest():
    """Load the intake manifest."""
    if not MANIFEST.exists():
        print(f"ERROR: Manifest not found: {MANIFEST}")
        sys.exit(1)

    with open(MANIFEST, "r") as f:
        data = yaml.safe_load(f)

    return data.get("entries", [])


def get_pending_pdfs(entries):
    """Get pending PDF entries from manifest."""
    return [
        e for e in entries
        if e.get("status") == "pending"
        and e.get("format") in ("pdf",)
    ]


def print_status(entries):
    """Print manifest status."""
    pdfs = [e for e in entries if e.get("format") == "pdf"]
    pending = [e for e in pdfs if e.get("status") == "pending"]
    done = [e for e in pdfs if e.get("status") == "done"]
    skipped = [e for e in pdfs if e.get("status") == "skipped"]

    print(f"\n  INTAKE STATUS")
    print(f"  {'─' * 45}")
    print(f"  Total PDFs:    {len(pdfs)}")
    print(f"  Pending:       {len(pending)}")
    print(f"  Done:          {len(done)}")
    print(f"  Skipped:       {len(skipped)}")
    print()

    if pending:
        print(f"  PENDING (sorted by size):")
        for e in sorted(pending, key=lambda x: x.get("size_kb", 0)):
            print(f"    {e.get('size_kb', '?'):>6} KB  {e['filename']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Convert PDFs to text")
    parser.add_argument("--file", help="Single PDF file to convert")
    parser.add_argument("--batch", type=int, help="Convert first N pending PDFs")
    parser.add_argument("--all", action="store_true", help="Convert all pending PDFs")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--status", action="store_true", help="Show manifest status")
    args = parser.parse_args()

    if args.status:
        entries = load_manifest()
        print_status(entries)
        return

    if args.file:
        # Single file mode
        pdf_path = Path(args.file)
        if not pdf_path.is_absolute():
            pdf_path = ROOT / pdf_path

        print(f"\n  Converting: {pdf_path.name}")
        print(f"  {'─' * 50}")

        result = convert_single(pdf_path)

        if result["success"]:
            print(f"  Pages:    {result['pages']}")
            print(f"  Chars:    {result['chars']:,}")
            print(f"  Quality:  {result['quality']}")
            if result["issue"]:
                print(f"  Issue:    {result['issue']}")
            print(f"  Output:   {result['output']} ({result['output_size_kb']} KB)")
            print(f"  Status:   OK ✓")
        else:
            print(f"  ERROR:    {result['error']}")
            sys.exit(1)
        return

    # Batch/All mode - use manifest
    entries = load_manifest()
    pending = get_pending_pdfs(entries)

    if not pending:
        print("  No pending PDFs in manifest.")
        return

    if args.batch:
        # Sort by size (smallest first) for incremental testing
        pending = sorted(pending, key=lambda x: x.get("size_kb", 0))[:args.batch]
    elif not args.all:
        parser.print_help()
        return

    if args.dry_run:
        print(f"\n  DRY RUN: Would convert {len(pending)} PDFs:")
        for e in pending:
            print(f"    {e.get('size_kb', '?'):>6} KB  {e['filename']}")
        return

    print(f"\n  BATCH CONVERSION: {len(pending)} PDFs")
    print(f"  {'─' * 60}")

    results = []
    for entry in sorted(pending, key=lambda x: x.get("size_kb", 0)):
        pdf_path = INTAKE_DIR / entry["filename"]
        result = convert_single(pdf_path)
        results.append(result)

        status = "OK ✓" if result["success"] else f"FAIL: {result.get('error', '?')}"
        quality = result.get("quality", "?")
        chars = result.get("chars", 0)
        print(f"  {entry['filename'][:45]:<45} {chars:>8,} chars  {quality:<8} {status}")

    # Summary
    ok = sum(1 for r in results if r["success"])
    good = sum(1 for r in results if r.get("quality") == "GOOD")
    poor = sum(1 for r in results if r.get("quality") in ("POOR", "LOW"))

    print(f"\n  {'─' * 60}")
    print(f"  SUMMARY: {ok}/{len(results)} converted, {good} GOOD, {poor} POOR/LOW")
    print()


if __name__ == "__main__":
    main()
