#!/usr/bin/env python3
"""Count and classify full-text papers, upgrade content_level where appropriate.

Analyzes papers in data/paper-texts/ against their YAML metadata in
data/paper-references/ and classifies them into:
- L3 candidates: true full texts (>= 4000 words, not abstract-only)
- L2: structured summaries (500-3999 words with sections)
- L1: abstracts only (<500 words or marked as abstract-only)

Usage:
    python scripts/count_fulltext_papers.py --report       # Show report only
    python scripts/count_fulltext_papers.py --upgrade       # Upgrade YAML content_levels
    python scripts/count_fulltext_papers.py --upgrade --dry-run  # Show what would change
"""

import os
import sys
import re
import glob
import argparse
from pathlib import Path
from datetime import date


PAPER_TEXTS_DIR = "data/paper-texts"
PAPER_REFS_DIR = "data/paper-references"

# Markers that indicate abstract-only or failed fetches
ABSTRACT_ONLY_MARKERS = [
    "abstract only",
    "pdf download failed",
    "metadata fallback",
    "note: pdf download failed",
]

# Minimum word count thresholds
L3_MIN_WORDS = 4000  # Based on smallest existing L3 paper (4214w)
L2_MIN_WORDS = 500


def get_word_count(filepath):
    """Count words in a file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    # Strip YAML frontmatter
    text = re.sub(r"^---.*?---", "", text, count=1, flags=re.DOTALL)
    return len(text.split())


def is_abstract_only(filepath):
    """Check if file is marked as abstract-only."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        # Only check first 500 chars (header area)
        header = f.read(500).lower()
    return any(marker in header for marker in ABSTRACT_ONLY_MARKERS)


def has_paper_sections(filepath):
    """Check if file has typical paper sections (Introduction, Methods, etc.)."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    section_patterns = [
        r"(?i)##?\s*(introduction|einleitung)",
        r"(?i)##?\s*(method|methodology|experimental|design)",
        r"(?i)##?\s*(result|finding|evidence)",
        r"(?i)##?\s*(discussion|conclusion|summary)",
        r"(?i)##?\s*(reference|bibliography|literatur)",
    ]
    matches = sum(1 for p in section_patterns if re.search(p, text))
    return matches


def is_mpg_pure(filepath):
    """Check if file was fetched from MPG Pure (typically complete)."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        header = f.read(500).lower()
    return "mpg_pure" in header or "source: mpg" in header


def get_yaml_content_level(yaml_path):
    """Extract first content_level from YAML file."""
    with open(yaml_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            match = re.match(r"\s*content_level:\s*[\"']?(L\d)[\"']?", line)
            if match:
                return match.group(1)
    return None


def update_yaml_content_level(yaml_path, old_level, new_level):
    """Update all content_level occurrences in a YAML file."""
    with open(yaml_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Replace content_level values
    updated = re.sub(
        r"(content_level:\s*)[\"']?" + re.escape(old_level) + r"[\"']?",
        r"\g<1>" + new_level,
        content,
    )

    if updated != content:
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(updated)
        return True
    return False


def classify_paper(md_path):
    """Classify a paper's full-text file.

    Returns dict with classification info.
    """
    key = Path(md_path).stem
    yaml_path = os.path.join(PAPER_REFS_DIR, f"{key}.yaml")

    info = {
        "key": key,
        "md_path": md_path,
        "yaml_path": yaml_path,
        "yaml_exists": os.path.exists(yaml_path),
        "word_count": get_word_count(md_path),
        "abstract_only": is_abstract_only(md_path),
        "mpg_pure": is_mpg_pure(md_path),
        "section_count": has_paper_sections(md_path),
        "current_level": None,
        "recommended_level": None,
        "needs_upgrade": False,
    }

    if info["yaml_exists"]:
        info["current_level"] = get_yaml_content_level(yaml_path)

    # Classification logic
    if info["abstract_only"] or info["word_count"] < L2_MIN_WORDS:
        info["recommended_level"] = "L1"
    elif info["word_count"] >= L3_MIN_WORDS:
        # Strong L3 candidate: enough words, not abstract-only
        info["recommended_level"] = "L3"
    elif info["section_count"] >= 3:
        # Has structure but not enough words for L3
        info["recommended_level"] = "L2"
    else:
        info["recommended_level"] = "L2"

    # Determine if upgrade is needed
    level_order = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
    if info["current_level"] and info["recommended_level"]:
        current_rank = level_order.get(info["current_level"], 0)
        recommended_rank = level_order.get(info["recommended_level"], 0)
        if recommended_rank > current_rank:
            info["needs_upgrade"] = True

    return info


def main():
    parser = argparse.ArgumentParser(description="Count and classify full-text papers")
    parser.add_argument("--report", action="store_true", help="Show classification report")
    parser.add_argument("--upgrade", action="store_true", help="Upgrade YAML content_levels")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    if not args.report and not args.upgrade:
        args.report = True

    # Find all paper text files
    md_files = sorted(glob.glob(os.path.join(PAPER_TEXTS_DIR, "PAP-*.md")))
    print(f"Found {len(md_files)} full-text files in {PAPER_TEXTS_DIR}/")
    print()

    # Classify all papers
    papers = [classify_paper(f) for f in md_files]

    # Papers that have YAML and are not already L3
    candidates = [p for p in papers if p["yaml_exists"] and p["current_level"] != "L3"]
    already_l3 = [p for p in papers if p["yaml_exists"] and p["current_level"] == "L3"]
    no_yaml = [p for p in papers if not p["yaml_exists"]]

    if args.report:
        print("=" * 70)
        print("FULL-TEXT PAPER CLASSIFICATION REPORT")
        print("=" * 70)
        print()

        print(f"Already L3:              {len(already_l3)} papers")
        print(f"Candidates to review:    {len(candidates)} papers")
        print(f"No YAML file:            {len(no_yaml)} papers")
        print()

        # Group candidates by recommended level
        upgrade_to_l3 = [p for p in candidates if p["recommended_level"] == "L3" and p["needs_upgrade"]]
        stay_l2 = [p for p in candidates if p["recommended_level"] == "L2"]
        downgrade_to_l1 = [p for p in candidates if p["recommended_level"] == "L1"]

        print("-" * 70)
        print(f"UPGRADE TO L3: {len(upgrade_to_l3)} papers (>= {L3_MIN_WORDS} words, not abstract-only)")
        print("-" * 70)
        for p in sorted(upgrade_to_l3, key=lambda x: -x["word_count"]):
            src = " [MPG]" if p["mpg_pure"] else ""
            print(f"  {p['current_level']} → L3  {p['key']:<50} {p['word_count']:>6}w  {p['section_count']} sections{src}")

        print()
        print("-" * 70)
        print(f"STAY AT L2: {len(stay_l2)} papers ({L2_MIN_WORDS}-{L3_MIN_WORDS-1} words, structured)")
        print("-" * 70)
        for p in sorted(stay_l2, key=lambda x: -x["word_count"]):
            print(f"  {p['current_level']} = L2  {p['key']:<50} {p['word_count']:>6}w  {p['section_count']} sections")

        print()
        print("-" * 70)
        print(f"ABSTRACT-ONLY (L1): {len(downgrade_to_l1)} papers (<{L2_MIN_WORDS} words or marked abstract-only)")
        print("-" * 70)
        for p in sorted(downgrade_to_l1, key=lambda x: -x["word_count"]):
            marker = " [abstract-only marker]" if p["abstract_only"] else ""
            print(f"  {p['current_level']} → L1  {p['key']:<50} {p['word_count']:>6}w{marker}")

        # Summary
        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        total_l3 = len(already_l3) + len(upgrade_to_l3)
        print(f"  Current L3 papers:     {len(already_l3)}")
        print(f"  + Upgrade to L3:       {len(upgrade_to_l3)}")
        print(f"  = NEW TOTAL L3:        {total_l3}")
        print()
        print(f"  Papers needing upgrade: {len(upgrade_to_l3)}")
        print(f"  Papers staying L2:      {len(stay_l2)}")
        print(f"  Papers that are L1:     {len(downgrade_to_l1)}")

    if args.upgrade:
        upgrade_to_l3 = [p for p in candidates if p["recommended_level"] == "L3" and p["needs_upgrade"]]

        if not upgrade_to_l3:
            print("No papers need upgrading.")
            return

        print()
        print("=" * 70)
        print(f"UPGRADING {len(upgrade_to_l3)} papers to L3")
        print("=" * 70)

        upgraded = 0
        for p in sorted(upgrade_to_l3, key=lambda x: x["key"]):
            old = p["current_level"]
            if args.dry_run:
                print(f"  [DRY-RUN] {old} → L3  {p['key']} ({p['word_count']}w)")
            else:
                success = update_yaml_content_level(p["yaml_path"], old, "L3")
                if success:
                    print(f"  ✅ {old} → L3  {p['key']} ({p['word_count']}w)")
                    upgraded += 1
                else:
                    print(f"  ❌ FAILED  {p['key']} - could not update {p['yaml_path']}")

        if not args.dry_run:
            print(f"\nUpgraded {upgraded}/{len(upgrade_to_l3)} papers to L3.")


if __name__ == "__main__":
    main()
