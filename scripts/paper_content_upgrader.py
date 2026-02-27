#!/usr/bin/env python3
"""
Paper Content Upgrader

Automatisiert das Upgrade von Papers von Content Level 0 → 1 oder 2:
- Prüft auf Open Access PDFs (Unpaywall, Semantic Scholar, arXiv, SSRN)
- Extrahiert Text aus PDFs wenn verfügbar
- Holt Abstracts via WebSearch als Fallback
- Füllt Queue automatisch auf wenn < 60 Papers

Usage:
    python scripts/paper_content_upgrader.py --check-oa PAP-xxx    # Check Open Access
    python scripts/paper_content_upgrader.py --upgrade PAP-xxx     # Upgrade single paper
    python scripts/paper_content_upgrader.py --batch N             # Upgrade N papers
    python scripts/paper_content_upgrader.py --refill              # Refill queue to 60
    python scripts/paper_content_upgrader.py --stats               # Show statistics
"""

import os
import sys
import yaml
import json
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent.parent
QUEUE_FILE = ROOT / "data" / "paper-integration-queue.yaml"
BIB_FILE = ROOT / "bibliography" / "bcm_master.bib"
PAPERS_DIR = ROOT / "papers" / "evaluated" / "integrated"

# Target queue size
TARGET_QUEUE_SIZE = 60

# Paper template
PAPER_TEMPLATE = """================================================================================
{title}
================================================================================

Authors: {authors}
Year: {year}
Journal: {journal}
DOI: {doi}

Source: {source}

================================================================================
ABSTRACT
================================================================================

{abstract}

================================================================================
KEY FINDINGS
================================================================================

{key_findings}

================================================================================
METHODOLOGY
================================================================================

{methodology}

================================================================================
EBF INTEGRATION NOTES
================================================================================

{ebf_notes}

================================================================================
"""


def load_queue():
    """Load queue from YAML."""
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE) as f:
            return yaml.safe_load(f) or {}
    return {"pending": [], "completed": [], "stats": {}}


def save_queue(queue):
    """Save queue to YAML."""
    queue["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(QUEUE_FILE, "w") as f:
        yaml.dump(queue, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def parse_bibtex_entry(entry_text):
    """Parse a single BibTeX entry into a dict."""
    result = {}

    # Get entry type and key
    match = re.match(r'@(\w+)\s*\{\s*([^,]+)', entry_text)
    if match:
        result['type'] = match.group(1).lower()
        result['key'] = match.group(2).strip()

    # Parse fields
    field_pattern = r'(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
    for match in re.finditer(field_pattern, entry_text, re.DOTALL):
        field_name = match.group(1).lower()
        field_value = match.group(2).strip()
        result[field_name] = field_value

    return result


def get_all_bibtex_entries():
    """Get all entries from bcm_master.bib."""
    if not BIB_FILE.exists():
        return []

    content = BIB_FILE.read_text(encoding='utf-8', errors='ignore')
    entries = []

    # Split by @ and process each entry
    parts = re.split(r'\n@', content)
    for i, part in enumerate(parts):
        if i == 0 and not part.strip().startswith('@'):
            continue
        if i > 0:
            part = '@' + part

        entry = parse_bibtex_entry(part)
        if entry.get('key'):
            entries.append(entry)

    return entries


def check_unpaywall(doi):
    """Check Unpaywall for Open Access PDF."""
    if not doi:
        return None

    # Unpaywall API (free, just needs email)
    email = "research@fehradvice.com"
    url = f"https://api.unpaywall.org/v2/{quote(doi)}?email={email}"

    try:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            # Check for best OA location
            if data.get('best_oa_location'):
                pdf_url = data['best_oa_location'].get('url_for_pdf')
                if pdf_url:
                    return {
                        'source': 'unpaywall',
                        'pdf_url': pdf_url,
                        'is_oa': data.get('is_oa', False),
                        'oa_status': data.get('oa_status', 'unknown')
                    }
    except Exception as e:
        pass

    return None


def check_semantic_scholar(doi=None, title=None):
    """Check Semantic Scholar for paper info and PDF."""
    try:
        import urllib.request

        if doi:
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{quote(doi)}?fields=title,abstract,openAccessPdf,authors,year"
        elif title:
            url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={quote(title)}&limit=1&fields=title,abstract,openAccessPdf,authors,year"
        else:
            return None

        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            # Handle search results
            if 'data' in data and data['data']:
                data = data['data'][0]

            result = {
                'source': 'semantic_scholar',
                'title': data.get('title'),
                'abstract': data.get('abstract'),
                'year': data.get('year'),
                'authors': [a.get('name') for a in data.get('authors', [])]
            }

            if data.get('openAccessPdf'):
                result['pdf_url'] = data['openAccessPdf'].get('url')

            return result
    except Exception as e:
        pass

    return None


def download_and_extract_pdf(pdf_url, paper_id):
    """Download PDF and extract text."""
    try:
        import urllib.request

        # Download PDF to temp file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                tmp.write(response.read())
            tmp_path = tmp.name

        # Extract text using pdftotext (if available)
        try:
            result = subprocess.run(
                ['pdftotext', '-layout', tmp_path, '-'],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 and result.stdout.strip():
                text = result.stdout
                os.unlink(tmp_path)
                return text
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # Fallback: try pypdf if available
        try:
            from pypdf import PdfReader
            reader = PdfReader(tmp_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            os.unlink(tmp_path)
            return text
        except ImportError:
            pass

        os.unlink(tmp_path)
    except Exception as e:
        pass

    return None


def create_paper_file(paper_id, data, content_level=1):
    """Create paper .txt file with content."""

    # Prepare content
    title = data.get('title', 'Unknown Title')
    authors = data.get('authors', [])
    if isinstance(authors, list):
        authors = ', '.join(authors)
    year = data.get('year', 'Unknown')
    journal = data.get('journal', 'Unknown')
    doi = data.get('doi', '')
    abstract = data.get('abstract', '[Abstract not available]')
    source = data.get('source', 'Unknown source')
    full_text = data.get('full_text', '')

    # Generate key findings from abstract or full text
    key_findings = "- [Key findings to be extracted]\n- [See abstract for main contributions]"

    # Generate methodology placeholder
    methodology = "- Study Design: [To be determined from full text]\n- Sample: [To be determined]\n- Identification: [To be determined]"

    # Generate EBF notes placeholder
    ebf_notes = """CORE Dimensions:
- [To be determined based on paper content]

Theory Support:
- [To be linked to theory-catalog.yaml]

Parameters:
- [To be extracted from paper]

EBF Relevance:
- [To be assessed]"""

    # If we have full text, include it
    if full_text and len(full_text) > 1000:
        content = PAPER_TEMPLATE.format(
            title=title,
            authors=authors,
            year=year,
            journal=journal,
            doi=doi,
            source=f"Full text extracted from PDF ({source})",
            abstract=abstract,
            key_findings=key_findings,
            methodology=methodology,
            ebf_notes=ebf_notes
        )
        # Add full text section
        content += f"""
================================================================================
FULL TEXT
================================================================================

{full_text[:50000]}  # Limit to 50k chars

================================================================================
"""
    else:
        content = PAPER_TEMPLATE.format(
            title=title,
            authors=authors,
            year=year,
            journal=journal,
            doi=doi,
            source=f"Abstract fetched via {source}",
            abstract=abstract,
            key_findings=key_findings,
            methodology=methodology,
            ebf_notes=ebf_notes
        )

    # Write file
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    paper_file = PAPERS_DIR / f"{paper_id}.txt"
    paper_file.write_text(content, encoding='utf-8')

    return paper_file


def normalize_paper_id(paper_id):
    """Normalize paper ID for matching (handle PAP- prefix)."""
    if paper_id.startswith('PAP-'):
        return paper_id, paper_id[4:]  # With and without prefix
    else:
        return f'PAP-{paper_id}', paper_id


def upgrade_paper(paper_id, bib_entry=None):
    """
    Upgrade a paper from Level 0 to Level 1 or 2.

    Returns: (new_level, source_info)
    """
    # Get DOI from BibTeX if not provided
    doi = None
    title = None

    # Normalize paper_id for matching
    paper_id_with_prefix, paper_id_without_prefix = normalize_paper_id(paper_id)

    if bib_entry:
        doi = bib_entry.get('doi', '').strip()
        title = bib_entry.get('title', '').strip()
    else:
        # Try to find in BibTeX (match with or without PAP- prefix)
        entries = get_all_bibtex_entries()
        for entry in entries:
            entry_key = entry.get('key', '')
            if entry_key in (paper_id_with_prefix, paper_id_without_prefix):
                doi = entry.get('doi', '').strip()
                title = entry.get('title', '').strip()
                bib_entry = entry
                break

    print(f"  Upgrading {paper_id}...")
    print(f"    DOI: {doi or 'not found'}")
    print(f"    Title: {title[:50] + '...' if title and len(title) > 50 else title or 'not found'}")

    # Step 1: Check for Open Access PDF
    pdf_url = None
    source = None

    # Try Unpaywall
    if doi:
        print(f"    Checking Unpaywall...")
        oa_info = check_unpaywall(doi)
        if oa_info and oa_info.get('pdf_url'):
            pdf_url = oa_info['pdf_url']
            source = 'Unpaywall'
            print(f"    ✓ Found OA PDF via Unpaywall")

    # Try Semantic Scholar
    if not pdf_url:
        print(f"    Checking Semantic Scholar...")
        ss_info = check_semantic_scholar(doi=doi, title=title)
        if ss_info:
            if ss_info.get('pdf_url'):
                pdf_url = ss_info['pdf_url']
                source = 'Semantic Scholar'
                print(f"    ✓ Found OA PDF via Semantic Scholar")
            elif ss_info.get('abstract'):
                # At least we have abstract
                data = {
                    'title': ss_info.get('title') or title,
                    'authors': ss_info.get('authors', []),
                    'year': ss_info.get('year') or (bib_entry.get('year') if bib_entry else None),
                    'journal': bib_entry.get('journal', '') if bib_entry else '',
                    'doi': doi,
                    'abstract': ss_info['abstract'],
                    'source': 'Semantic Scholar API'
                }
                create_paper_file(paper_id, data, content_level=1)
                print(f"    ✓ Created Level 1 file (abstract from Semantic Scholar)")
                return (1, 'Semantic Scholar abstract')

    # Step 2: If PDF found, download and extract
    if pdf_url:
        print(f"    Downloading PDF from {source}...")
        full_text = download_and_extract_pdf(pdf_url, paper_id)

        if full_text and len(full_text) > 1000:
            # Get abstract from Semantic Scholar if we have it
            abstract = None
            ss_info = check_semantic_scholar(doi=doi, title=title)
            if ss_info:
                abstract = ss_info.get('abstract', '')

            data = {
                'title': title or (bib_entry.get('title') if bib_entry else 'Unknown'),
                'authors': bib_entry.get('author', '').split(' and ') if bib_entry else [],
                'year': bib_entry.get('year') if bib_entry else None,
                'journal': bib_entry.get('journal', '') if bib_entry else '',
                'doi': doi,
                'abstract': abstract or '[See full text below]',
                'full_text': full_text,
                'source': source
            }
            create_paper_file(paper_id, data, content_level=2)
            print(f"    ✓ Created Level 2 file (full text from {source})")
            return (2, f'Full text from {source}')

    # Step 3: Fallback - just abstract (would need WebSearch, which we can't do here)
    print(f"    ✗ No OA content found - needs manual WebSearch")
    return (0, 'No OA content available')


def refill_queue():
    """Refill queue to TARGET_QUEUE_SIZE from bcm_master.bib."""
    queue = load_queue()
    pending = queue.get('pending', [])
    current_size = len(pending)

    if current_size >= TARGET_QUEUE_SIZE:
        print(f"Queue already has {current_size} papers (target: {TARGET_QUEUE_SIZE})")
        return 0

    needed = TARGET_QUEUE_SIZE - current_size
    print(f"Queue has {current_size} papers, need {needed} more")

    # Get all BibTeX entries
    entries = get_all_bibtex_entries()
    print(f"Found {len(entries)} entries in bcm_master.bib")

    # Get existing paper_ids in queue
    existing_ids = {p.get('paper_id') for p in pending}
    existing_ids.update({p.get('paper_id') for p in queue.get('completed', [])})

    # Get papers that already have .txt files
    existing_files = {f.stem for f in PAPERS_DIR.glob('*.txt')} if PAPERS_DIR.exists() else set()

    added = 0
    for entry in entries:
        if added >= needed:
            break

        key = entry.get('key', '')
        paper_id = f"PAP-{key}" if not key.startswith('PAP-') else key

        # Skip if already in queue or has file
        if paper_id in existing_ids:
            continue
        if paper_id in existing_files or key in existing_files:
            continue

        # Add to queue
        pending.append({
            'paper_id': paper_id,
            'added': datetime.now().isoformat(),
            'content_level': 0,
            'integration_level': 1,
            'level': 1,
            'has_full_text': False,
            'track': 'B',
            'missing': ['Content file'],
            'priority': 'normal',
            'attempts': 0
        })
        added += 1

    if added > 0:
        queue['pending'] = pending
        queue['stats']['total_queued'] = queue['stats'].get('total_queued', 0) + added
        save_queue(queue)

    print(f"Added {added} papers to queue")
    return added


def batch_upgrade(count=10):
    """Upgrade N papers from the queue."""
    queue = load_queue()
    pending = queue.get('pending', [])

    # Get Level 0 papers
    level_0 = [p for p in pending if p.get('content_level', 0) == 0]

    if not level_0:
        print("No Level 0 papers in queue")
        return

    print(f"Found {len(level_0)} Level 0 papers, upgrading {min(count, len(level_0))}...")

    upgraded = 0
    for paper in level_0[:count]:
        paper_id = paper.get('paper_id')
        new_level, source = upgrade_paper(paper_id)

        if new_level > 0:
            # Update queue entry
            paper['content_level'] = new_level
            paper['has_full_text'] = new_level >= 1
            paper['track'] = 'A' if new_level >= 1 else 'B'
            if new_level >= 1:
                paper['priority'] = 'high'
            upgraded += 1

    if upgraded > 0:
        save_queue(queue)

    print(f"\nUpgraded {upgraded} papers")


def print_stats():
    """Print statistics about paper content levels."""
    queue = load_queue()
    pending = queue.get('pending', [])

    # Count by content_level
    levels = {0: 0, 1: 0, 2: 0}
    for p in pending:
        lvl = p.get('content_level', 0)
        levels[lvl] = levels.get(lvl, 0) + 1

    # Count BibTeX entries
    entries = get_all_bibtex_entries()
    bib_count = len(entries)

    # Count existing files
    file_count = len(list(PAPERS_DIR.glob('*.txt'))) if PAPERS_DIR.exists() else 0

    print("\n" + "="*60)
    print("  PAPER CONTENT STATISTICS")
    print("="*60)
    print(f"\n  📚 BibTeX Einträge:     {bib_count:,}")
    print(f"  📄 Content-Dateien:      {file_count}")
    print(f"  📋 In Queue:             {len(pending)}")
    print(f"\n  Queue Content Levels:")
    print(f"     📋 Level 0 (Metadata): {levels[0]}")
    print(f"     📄 Level 1 (Abstract): {levels[1]}")
    print(f"     📚 Level 2 (Full):     {levels[2]}")
    print(f"\n  Coverage:")
    print(f"     {file_count / bib_count * 100:.1f}% have content files")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Paper Content Upgrader")
    parser.add_argument("--check-oa", metavar="PAPER_ID", help="Check Open Access availability")
    parser.add_argument("--upgrade", metavar="PAPER_ID", help="Upgrade single paper")
    parser.add_argument("--batch", type=int, metavar="N", help="Upgrade N papers")
    parser.add_argument("--refill", action="store_true", help="Refill queue to 60 papers")
    parser.add_argument("--stats", action="store_true", help="Show statistics")

    args = parser.parse_args()

    if args.check_oa:
        paper_id = args.check_oa
        print(f"Checking Open Access for {paper_id}...")

        # Normalize paper_id for matching
        paper_id_with_prefix, paper_id_without_prefix = normalize_paper_id(paper_id)

        # Get DOI from BibTeX
        entries = get_all_bibtex_entries()
        bib_entry = None
        for entry in entries:
            entry_key = entry.get('key', '')
            if entry_key in (paper_id_with_prefix, paper_id_without_prefix):
                bib_entry = entry
                break

        if bib_entry:
            doi = bib_entry.get('doi', '')
            title = bib_entry.get('title', '')

            print(f"  DOI: {doi}")
            print(f"  Title: {title[:60]}...")

            # Check Unpaywall
            oa = check_unpaywall(doi)
            if oa:
                print(f"\n  Unpaywall: {'✓ OA' if oa.get('is_oa') else '✗ Not OA'}")
                print(f"    Status: {oa.get('oa_status')}")
                if oa.get('pdf_url'):
                    print(f"    PDF: {oa['pdf_url'][:80]}...")

            # Check Semantic Scholar
            ss = check_semantic_scholar(doi=doi, title=title)
            if ss:
                print(f"\n  Semantic Scholar:")
                print(f"    Abstract: {'✓' if ss.get('abstract') else '✗'}")
                print(f"    PDF: {'✓ ' + ss['pdf_url'][:60] + '...' if ss.get('pdf_url') else '✗'}")
        else:
            print(f"  Paper not found in BibTeX")

    elif args.upgrade:
        upgrade_paper(args.upgrade)

    elif args.batch:
        batch_upgrade(args.batch)

    elif args.refill:
        refill_queue()

    elif args.stats:
        print_stats()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
