#!/usr/bin/env python3
"""
Auto-update README.md statistics from git repository.

Aktualisiert automatisch:
- Appendices count & file count
- Chapters count
- Bibliography entries
- Letzte Aktualisierung timestamp
- Letzte Commits
"""

import os
import subprocess
import re
from datetime import datetime
from pathlib import Path

def run_cmd(cmd):
    """Run shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def count_appendices():
    """Count LaTeX files in appendices directory."""
    appendices_dir = Path("appendices")
    tex_files = list(appendices_dir.glob("*.tex"))
    # Exclude template files
    actual_files = [f for f in tex_files if not f.name.startswith("00_")]
    return len(actual_files), len(tex_files)

def count_chapters():
    """Count LaTeX files in chapters directory."""
    chapters_dir = Path("chapters")
    tex_files = list(chapters_dir.glob("*.tex"))
    # Exclude template files
    actual_files = [f for f in tex_files if not f.name.startswith("00_")]
    return len(actual_files), len(tex_files)

def count_bibliography():
    """Count BibTeX entries in bcm_master.bib."""
    bib_file = Path("bibliography/bcm_master.bib")
    if not bib_file.exists():
        return 0

    content = bib_file.read_text()
    # Count @article, @book, @inproceedings, etc.
    entries = re.findall(r"^@\w+\{", content, re.MULTILINE)
    return len(entries)

def get_last_commit_date():
    """Get date of last commit."""
    cmd = "git log -1 --format='%ai' | cut -d' ' -f1"
    date_str = run_cmd(cmd)
    return date_str.strip("'")

def update_readme_statistics(readme_path="README.md"):
    """Update README.md with current statistics."""

    print("🔄 Updating README statistics...")

    # Get current statistics
    appendix_count, appendix_files = count_appendices()
    chapter_count, chapter_files = count_chapters()
    bib_count = count_bibliography()
    last_commit = get_last_commit_date()

    print(f"  ✓ Appendices: {appendix_count} (files: {appendix_files})")
    print(f"  ✓ Chapters: {chapter_count} (files: {chapter_files})")
    print(f"  ✓ Bibliography: {bib_count} entries")
    print(f"  ✓ Last commit: {last_commit}")

    # Read current README
    with open(readme_path, 'r') as f:
        content = f.read()

    original_content = content

    # Update Appendices statistics table
    # Pattern: | **Appendices** | 167 (A-QQQ++) |
    content = re.sub(
        r"\| \*\*Appendices\*\* \| \d+ \(A-QQQ\+\+\) \|",
        f"| **Appendices** | {appendix_count} (A-QQQ++) |",
        content
    )

    # Update Chapters statistics table
    # Pattern: | **Kapitel** | 19 + 4 Extended |
    content = re.sub(
        r"\| \*\*Kapitel\*\* \| \d+ \+ \d+ Extended \|",
        f"| **Kapitel** | 19 + 4 Extended |",
        content
    )

    # Update Bibliography entry count in statistics table
    # Pattern: | **Referenzen** | 2,226 BibTeX Einträge |
    content = re.sub(
        r"\| \*\*Referenzen\*\* \| [\d,]+ BibTeX Einträge \|",
        f"| **Referenzen** | {bib_count:,} BibTeX Einträge |",
        content
    )

    # Update last update timestamp at the end
    # Pattern: *Letzte Aktualisierung: 2026-01-20*
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r"\*Letzte Aktualisierung: \d{4}-\d{2}-\d{2}\*",
        f"*Letzte Aktualisierung: {today}*",
        content
    )

    # Write back if changed
    if content != original_content:
        with open(readme_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {readme_path}")
        return True
    else:
        print(f"ℹ️  No changes needed for {readme_path}")
        return False

def update_docs_readme(readme_path="docs/README.md"):
    """Update docs/README.md with current statistics."""

    print(f"🔄 Updating {readme_path} statistics...")

    # Get current statistics
    appendix_count, appendix_files = count_appendices()
    chapter_count, chapter_files = count_chapters()
    bib_count = count_bibliography()

    print(f"  ✓ Appendices: {appendix_count} (files: {appendix_files})")
    print(f"  ✓ Chapters: {chapter_count} (files: {chapter_files})")
    print(f"  ✓ Bibliography: {bib_count} entries")

    # Read current file
    with open(readme_path, 'r') as f:
        content = f.read()

    original_content = content

    # Update chapter count
    # Pattern: | `/chapters/` | 76 Kapitel-Quelldateien
    content = re.sub(
        r"\| `/chapters/` \| \d+ Kapitel-Quelldateien",
        f"| `/chapters/` | {chapter_files} Kapitel-Quelldateien",
        content
    )

    # Update appendix count
    # Pattern: | `/appendices/` | 167 Appendix-Quelldateien
    content = re.sub(
        r"\| `/appendices/` \| \d+ Appendix-Quelldateien",
        f"| `/appendices/` | {appendix_files} Appendix-Quelldateien",
        content
    )

    # Update bibliography count
    # Pattern: | `/bibliography/` | 2,226 BibTeX Einträge |
    content = re.sub(
        r"\| `/bibliography/` \| [\d,]+ BibTeX Einträge \|",
        f"| `/bibliography/` | {bib_count:,} BibTeX Einträge |",
        content
    )

    # Update timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r"\*Letzte Aktualisierung: \d{4}-\d{2}-\d{2}",
        f"*Letzte Aktualisierung: {today}",
        content
    )

    if content != original_content:
        with open(readme_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {readme_path}")
        return True
    else:
        print(f"ℹ️  No changes needed for {readme_path}")
        return False

def update_chapters_readme(readme_path="chapters/README.md"):
    """Update chapters/README.md with current statistics."""

    print(f"🔄 Updating {readme_path} statistics...")

    chapter_count, chapter_files = count_chapters()

    print(f"  ✓ Chapters: {chapter_count} (files: {chapter_files})")

    with open(readme_path, 'r') as f:
        content = f.read()

    original_content = content

    # Update file count
    # Pattern: | **Dateien** | 76 |
    content = re.sub(
        r"\| \*\*Dateien\*\* \| \d+ \|",
        f"| **Dateien** | {chapter_files} |",
        content
    )

    # Update timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r"\*Letzte Aktualisierung: \d{4}-\d{2}-\d{2}",
        f"*Letzte Aktualisierung: {today}",
        content
    )

    if content != original_content:
        with open(readme_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {readme_path}")
        return True
    else:
        print(f"ℹ️  No changes needed for {readme_path}")
        return False

def update_appendices_readme(readme_path="appendices/README.md"):
    """Update appendices/README.md with current statistics."""

    print(f"🔄 Updating {readme_path} statistics...")

    appendix_count, appendix_files = count_appendices()

    print(f"  ✓ Appendices: {appendix_count} (files: {appendix_files})")

    with open(readme_path, 'r') as f:
        content = f.read()

    original_content = content

    # Update appendix count
    # Pattern: | **Appendices** | 167 |
    content = re.sub(
        r"\| \*\*Appendices\*\* \| \d+ \|",
        f"| **Appendices** | {appendix_count} |",
        content
    )

    # Update file count
    # Pattern: | **Dateien** | 170+ |
    content = re.sub(
        r"\| \*\*Dateien\*\* \| \d+\+ \|",
        f"| **Dateien** | {appendix_files}+ |",
        content
    )

    # Update timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r"\*Letzte Aktualisierung: \d{4}-\d{2}-\d{2}",
        f"*Letzte Aktualisierung: {today}",
        content
    )

    if content != original_content:
        with open(readme_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {readme_path}")
        return True
    else:
        print(f"ℹ️  No changes needed for {readme_path}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("📊 README Auto-Update Script")
    print("=" * 60)
    print()

    # Change to repo root if needed
    if not Path("README.md").exists():
        print("❌ README.md not found. Are you in the repo root?")
        exit(1)

    # Update all README files
    any_updated = False
    any_updated |= update_readme_statistics("README.md")
    any_updated |= update_docs_readme("docs/README.md")
    any_updated |= update_chapters_readme("chapters/README.md")
    any_updated |= update_appendices_readme("appendices/README.md")

    print()
    if any_updated:
        print("✅ Auto-update complete. Ready to commit.")
    else:
        print("ℹ️  All statistics are already current.")
    print()
