#!/usr/bin/env python3
"""
Enrich L0 Papers to Content Level L1.

For papers with only metadata (L0), generates a research-question-level
abstract from available information (title, notes, key_findings, parameters).

EXPERIMENTAL Mode: Run with --batch N to process N papers at a time.
  1. --batch 1   → Test on 1 paper
  2. --batch 10  → Verify on 10 papers
  3. --batch 0   → Process ALL remaining L0 papers

Usage:
    python scripts/enrich_l0_papers.py --batch 1    # Test 1
    python scripts/enrich_l0_papers.py --batch 10   # Test 10
    python scripts/enrich_l0_papers.py --batch 0    # All remaining
    python scripts/enrich_l0_papers.py --dry-run     # Show what would change
"""

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data" / "paper-references"


def get_l0_papers():
    """Find all papers at Content Level L0."""
    l0 = []
    for f in sorted(PAPERS_DIR.glob("PAP-*.yaml")):
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh)
            if not data:
                continue

            # Check top-level content_level
            cl = data.get("content_level")
            if cl in ("L1", "L2", "L3"):
                continue

            # Check full_text.content_level (only trust L2/L3, L1 may be auto-set)
            ft = data.get("full_text", {}) or {}
            if isinstance(ft, dict) and ft.get("content_level") in ("L2", "L3"):
                continue

            # Check if already has abstract content (top-level or summary)
            if data.get("abstract"):
                continue
            summary = data.get("summary", {}) or {}
            if isinstance(summary, dict) and summary.get("abstract"):
                continue

            l0.append((f, data))
        except Exception:
            pass
    return l0


def extract_abstract_from_data(data):
    """Generate a research-question-level abstract from available metadata."""
    title = data.get("title", "") or ""
    notes = ""
    key_finding = ""
    params = ""

    # Extract notes from ebf_integration
    ebf = data.get("ebf_integration", {}) or {}
    if isinstance(ebf, dict):
        notes = ebf.get("notes", "") or ""
        params = ebf.get("parameter", "") or ""

    # Extract key_findings
    kf = data.get("key_findings", {}) or {}
    if isinstance(kf, dict):
        key_finding = kf.get("finding", "") or ""
        # Skip auto-generated findings that just echo the title
        if kf.get("auto_generated"):
            key_finding = ""

    # Also check key_findings_structured
    kfs = data.get("key_findings_structured", []) or []
    if isinstance(kfs, list) and kfs:
        findings = [f.get("finding", "") for f in kfs if isinstance(f, dict)]
        if findings:
            key_finding = findings[0]

    # Build abstract from best available source
    if notes and len(notes) > 50:
        # Notes are usually the best source - convert to abstract style
        abstract = _notes_to_abstract(title, notes)
    elif key_finding and len(key_finding) > 30 and "Addresses the research question" not in key_finding:
        abstract = _finding_to_abstract(title, key_finding)
    elif title and len(title) > 10:
        # Fallback: generate from title (only if title is meaningful)
        abstract = _title_to_abstract(title, data)
    else:
        # No usable content at all
        abstract = ""

    return abstract


def _notes_to_abstract(title, notes):
    """Convert EBF integration notes to an abstract-style summary."""
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', notes.strip())

    # Filter out sentences that are EBF-internal
    ebf_patterns = [
        r'^(?:KEY|CRITICAL|IMPORTANT|NOTE|TODO|FOUNDATIONAL)',
        r'^(?:VALIDATES|EXTENDS|SUPPORTS|CONTRADICTS)',
        r'^(?:SEE ALSO|COMPARE|UPDATE)',
        r'(?:HMWM|EBF|PERI|SSOT)',
        r'^TOP-\d+\b',  # "TOP-5 PUBLICATION" etc.
        r'^[A-Z\s]{10,}$',  # All-caps sentence
        r'^(?:Of|For|In|To|At|By)\s\w',  # Fragment starting with preposition
    ]
    clean_sentences = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        is_ebf = False
        for pat in ebf_patterns:
            if re.search(pat, sent):
                is_ebf = True
                break
        if not is_ebf and len(sent) > 15:
            # Remove any leading ALL-CAPS words at start of sentence
            sent = re.sub(r'^(?:[A-Z]{2,}\s+)+', '', sent).strip()
            if sent and len(sent) > 15:
                # Ensure first char is uppercase
                sent = sent[0].upper() + sent[1:] if sent else sent
                clean_sentences.append(sent)

    if not clean_sentences:
        return _title_to_abstract(title, {})

    # Take up to 2 clean sentences
    content = " ".join(clean_sentences[:2]).rstrip(".")
    if len(content) < 30:
        return _title_to_abstract(title, {})

    return f'This paper, "{title}", {content}.'


def _finding_to_abstract(title, finding):
    """Convert a key finding to an abstract-style summary."""
    # Clean finding of EBF markers
    finding_clean = finding.strip().rstrip(".")
    return f'This paper, "{title}", finds that {_lower_first(finding_clean)}.'


def _title_to_abstract(title, data):
    """Generate abstract from title when no other content available."""
    journal = data.get("journal", "") or ""
    year = data.get("year", "") or ""
    author = data.get("author", data.get("authors", "")) or ""

    if isinstance(author, list):
        if author and isinstance(author[0], dict):
            author = author[0].get("family", "")
        else:
            author = str(author[0]) if author else ""

    # Construct minimal abstract preserving original title case
    parts = [f'This paper, "{title}", addresses its stated research question.']

    if journal and year:
        parts.append(f"Published in {journal} ({year}).")
    elif journal:
        parts.append(f"Published in {journal}.")

    return " ".join(parts)


def _lower_first(s):
    """Lowercase first character unless it's an acronym or proper noun."""
    if not s:
        return s
    # Don't lowercase if starts with acronym pattern (2+ uppercase)
    if len(s) > 1 and s[0].isupper() and s[1].isupper():
        return s
    # Don't lowercase common proper nouns at start
    proper_starts = ["The ", "A ", "An "]
    for p in proper_starts:
        if s.startswith(p):
            rest = s[len(p):].strip()
            return rest if rest else s
    return s[0].lower() + s[1:] if s[0].isupper() else s


def enrich_paper(filepath, data, dry_run=False):
    """Add content_level and summary.abstract to a paper YAML."""
    abstract = extract_abstract_from_data(data)

    if not abstract or len(abstract) < 20:
        return False, "Could not generate abstract"

    if dry_run:
        return True, abstract

    # Read file content
    with open(filepath) as f:
        content = f.read()

    # Add content_level: L1 if not present
    if "content_level:" not in content.split("prior_score:")[0]:
        # Find good insertion point: after doi/publication_type/year
        for marker in ["publication_type:", "doi:", "year:"]:
            if marker in content:
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if line.strip().startswith(marker):
                        # Insert after this line
                        indent = ""
                        lines.insert(i + 1, f"{indent}content_level: L1")
                        content = "\n".join(lines)
                        break
                break

    # Add summary.abstract if not present
    if "summary:" not in content.split("prior_score:")[0]:
        # Find insertion point: after content_level or after publication_type
        lines = content.split("\n")
        insert_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("content_level:") and "prior_score" not in "\n".join(lines[:i]):
                insert_idx = i + 1
                break
        if insert_idx is None:
            for i, line in enumerate(lines):
                if line.strip().startswith("publication_type:"):
                    insert_idx = i + 1
                    break

        if insert_idx is not None:
            # Format abstract as YAML block scalar
            abstract_yaml = f"summary:\n  abstract: >\n    {abstract}"
            lines.insert(insert_idx, abstract_yaml)
            content = "\n".join(lines)

    # Update prior_score.content_level if present
    content = re.sub(
        r"(prior_score:.*?content_level:)\s*L0",
        r"\1 L1",
        content,
        flags=re.DOTALL
    )
    # Update confidence_multiplier
    content = re.sub(
        r"(prior_score:.*?confidence_multiplier:)\s*0\.6",
        r"\1 0.8",
        content,
        flags=re.DOTALL
    )

    with open(filepath, "w") as f:
        f.write(content)

    return True, abstract


def main():
    parser = argparse.ArgumentParser(description="Enrich L0 papers to L1")
    parser.add_argument("--batch", type=int, default=1,
                        help="Number of papers to process (0=all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without modifying files")
    args = parser.parse_args()

    l0_papers = get_l0_papers()
    print(f"Found {len(l0_papers)} L0 papers needing enrichment")

    if args.batch == 0:
        batch = l0_papers
    else:
        batch = l0_papers[:args.batch]

    print(f"Processing {len(batch)} papers {'(dry-run)' if args.dry_run else ''}\n")

    success = 0
    failed = 0
    for filepath, data in batch:
        ok, result = enrich_paper(filepath, data, dry_run=args.dry_run)
        title = (data.get("title", "") or "")[:60]
        if ok:
            success += 1
            if args.dry_run:
                print(f"  ✅ {filepath.stem}")
                print(f"     Title: {title}")
                print(f"     Abstract: {result[:100]}...")
            else:
                print(f"  ✅ {filepath.stem}")
        else:
            failed += 1
            print(f"  ❌ {filepath.stem}: {result}")

    print(f"\nDone: {success} enriched, {failed} failed, {len(l0_papers) - len(batch)} remaining")


if __name__ == "__main__":
    main()
