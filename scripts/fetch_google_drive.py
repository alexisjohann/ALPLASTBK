#!/usr/bin/env python3
"""
Google Drive File Fetcher & Journal Volume Splitter
====================================================
Downloads files from Google Drive and optionally splits journal volumes
into individual papers.

Usage:
    # Download only
    python scripts/fetch_google_drive.py --file-id <ID> --output-dir data/drive-downloads/

    # Split a previously downloaded text file into papers
    python scripts/fetch_google_drive.py --split-papers --input <file> --output-dir <dir>

    # Full pipeline: download + convert + split
    python scripts/fetch_google_drive.py --file-id <ID> --convert --split-papers
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path


def split_journal_volume(input_file: str, output_dir: str) -> list:
    """Split a journal volume text file into individual papers.

    Detects paper boundaries by looking for patterns like:
    - "Journal of Economic Perspectives—Volume X, Number Y—Season YYYY—Pages N–M"
    - Page headers with author names
    - Clear title/author blocks

    Returns list of dicts with paper metadata.
    """
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    os.makedirs(output_dir, exist_ok=True)

    # Pattern for JEP paper boundaries
    # Matches: "Journal of Economic Perspectives—Volume 40, Number 1—Winter 2026—Pages 3–28"
    jep_pattern = re.compile(
        r'Journal of Economic Perspectives[—–-]+Volume\s+(\d+),?\s*Number\s+(\d+)[—–-]+'
        r'(\w+)\s+(\d{4})[—–-]+Pages?\s+(\d+)[—–]+(\d+)',
        re.IGNORECASE
    )

    # Find all paper boundaries
    matches = list(jep_pattern.finditer(text))

    if not matches:
        # Try alternative patterns for other journals
        alt_pattern = re.compile(
            r'(?:Pages?\s+(\d+)[—–-]+(\d+))',
            re.IGNORECASE
        )
        alt_matches = list(alt_pattern.finditer(text))

        if not alt_matches:
            print("⚠️  No paper boundaries found. Saving as single file.")
            output_path = os.path.join(output_dir, 'full_volume.md')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return [{'file': output_path, 'title': 'Full Volume', 'pages': 'all'}]

    papers = []

    for i, match in enumerate(matches):
        volume = match.group(1)
        number = match.group(2)
        season = match.group(3)
        year = match.group(4)
        page_start = match.group(5)
        page_end = match.group(6)

        # Extract text from this match to the next (or end of file)
        start_pos = match.start()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        paper_text = text[start_pos:end_pos].strip()

        # Try to extract title and authors from the first few lines
        lines = paper_text.split('\n')
        # Skip the header line itself
        content_lines = []
        title_lines = []
        author_line = ''

        in_header = True
        for line in lines[1:]:  # Skip the "Journal of..." line
            stripped = line.strip()
            if not stripped:
                if in_header and title_lines:
                    in_header = False
                continue
            if in_header:
                # Title lines are typically bold/large - here they're just text
                # Authors typically follow the title
                title_lines.append(stripped)
            else:
                content_lines.append(stripped)

        # Heuristic: title is first non-empty block, author is line with multiple names
        title = ' '.join(title_lines[:3]) if title_lines else f'Paper pp. {page_start}-{page_end}'

        # Clean title
        title = re.sub(r'\s+', ' ', title).strip()

        # Generate filename
        safe_title = re.sub(r'[^\w\s-]', '', title[:60]).strip().replace(' ', '_').lower()
        filename = f"paper_{page_start}-{page_end}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)

        # Write paper
        header = f"""# {title}

**Source:** Journal of Economic Perspectives, Volume {volume}, Number {number}, {season} {year}, Pages {page_start}–{page_end}

---

"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header + paper_text)

        paper_info = {
            'file': filepath,
            'title': title,
            'volume': int(volume),
            'number': int(number),
            'season': season,
            'year': int(year),
            'page_start': int(page_start),
            'page_end': int(page_end),
        }
        papers.append(paper_info)

        print(f"  📄 Paper {i+1}: pp. {page_start}-{page_end} — {title[:70]}")

    # Write split log
    log_path = os.path.join(output_dir, 'split-log.yaml')
    log = {
        'source': input_file,
        'papers_found': len(papers),
        'papers': papers
    }
    with open(log_path, 'w', encoding='utf-8') as f:
        yaml.dump(log, f, default_flow_style=False, allow_unicode=True)

    print(f"\n✅ Split into {len(papers)} papers")
    print(f"   Log: {log_path}")

    return papers


def main():
    parser = argparse.ArgumentParser(description='Google Drive Fetch & Journal Volume Splitter')
    parser.add_argument('--file-id', help='Google Drive file ID')
    parser.add_argument('--output-dir', default='data/drive-downloads/', help='Output directory')
    parser.add_argument('--output-name', default='', help='Output filename')
    parser.add_argument('--convert', action='store_true', help='Convert PDF to text')
    parser.add_argument('--split-papers', action='store_true', help='Split journal volume into papers')
    parser.add_argument('--input', help='Input file for split-papers (skip download)')

    args = parser.parse_args()

    if args.split_papers and args.input:
        # Split mode only
        print(f"📚 Splitting journal volume: {args.input}")
        papers = split_journal_volume(args.input, args.output_dir)
        return

    if args.file_id:
        # Download mode
        try:
            import gdown
        except ImportError:
            print("Installing gdown...")
            os.system('pip install gdown')
            import gdown

        os.makedirs(args.output_dir, exist_ok=True)
        url = f'https://drive.google.com/uc?id={args.file_id}'

        output_path = os.path.join(args.output_dir, args.output_name) if args.output_name else args.output_dir
        print(f"📥 Downloading: {url}")
        downloaded = gdown.download(url, output_path, quiet=False, fuzzy=True)

        if downloaded:
            print(f"✅ Downloaded: {downloaded}")
        else:
            print("❌ Download failed")
            sys.exit(1)

        if args.convert and downloaded.endswith('.pdf'):
            print("📄 Converting PDF to text...")
            text_file = downloaded.replace('.pdf', '.txt')
            os.system(f'pdftotext -layout "{downloaded}" "{text_file}"')
            print(f"✅ Converted: {text_file}")

            if args.split_papers:
                split_dir = os.path.join(args.output_dir, 'split')
                papers = split_journal_volume(text_file, split_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
