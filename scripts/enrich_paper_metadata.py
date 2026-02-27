#!/usr/bin/env python3
"""
Paper Metadata Enrichment via CrossRef API
============================================
Reads the enrichment queue, fetches missing metadata from CrossRef,
and updates BibTeX + YAML files.

Usage:
  python scripts/enrich_paper_metadata.py --priority P2 --batch-size 50
  python scripts/enrich_paper_metadata.py --priority ALL --batch-size 200 --dry-run

Requires: requests, pyyaml
Runs in: GitHub Actions (external API access required)
"""

import re
import os
import sys
import time
import yaml
import argparse
import subprocess
import requests
from pathlib import Path
from datetime import datetime

REPO = Path(os.environ.get("GITHUB_WORKSPACE", "."))
BIB_FILE = REPO / "bibliography" / "bcm_master.bib"
QUEUE_FILE = REPO / "data" / "paper-enrichment-queue.yaml"
YAML_DIR = REPO / "data" / "paper-references"
LOG_FILE = REPO / "data" / "paper-enrichment-log.yaml"

CROSSREF_API = "https://api.crossref.org/works"
HEADERS = {
    "User-Agent": "EBF-Enrichment/2.0 (https://github.com/FehrAdvice-Partners-AG/complementarity-context-framework; mailto:research@fehradvice.com)"
}

# Priority filter mapping
PRIORITY_FILTERS = {
    'P1': lambda q: q['is_cited'] and 'title' in q['missing_fields'],
    'P2': lambda q: q['is_cited'] and 'doi' in q['missing_fields'] and 'title' not in q['missing_fields'],
    'P3': lambda q: q['is_cited'] and 'journal' in q['missing_fields'],
    'P4': lambda q: not q['is_cited'] and 'title' in q['missing_fields'],
    'P5': lambda q: not q['is_cited'] and 'doi' in q['missing_fields'] and 'title' not in q['missing_fields'],
    'ALL': lambda q: True,
}


def load_queue():
    """Load enrichment queue."""
    with open(QUEUE_FILE) as f:
        data = yaml.safe_load(f)
    return data.get('queue', [])


def crossref_search_by_title(title, author=None, year=None):
    """Search CrossRef by title, return full metadata."""
    query = title
    if author:
        first_author = author.split(' and ')[0].split(',')[0].strip()
        query = f"{first_author} {title}"

    params = {
        'query.bibliographic': query,
        'rows': 5,
    }

    try:
        resp = requests.get(CROSSREF_API, params=params, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        items = resp.json().get('message', {}).get('items', [])

        for item in items:
            item_title = ' '.join(item.get('title', ['']))
            # Title similarity check
            if not item_title:
                continue
            t1 = re.sub(r'[^a-z0-9]', '', title.lower())[:60]
            t2 = re.sub(r'[^a-z0-9]', '', item_title.lower())[:60]
            if t1[:30] not in t2 and t2[:30] not in t1:
                continue
            # Year check
            if year:
                item_year = None
                for date_field in ['published-print', 'published-online', 'created']:
                    dp = item.get(date_field, {}).get('date-parts', [[None]])
                    if dp and dp[0] and dp[0][0]:
                        item_year = str(dp[0][0])
                        break
                if item_year and abs(int(item_year) - int(year)) > 1:
                    continue

            return extract_metadata(item)

        return None
    except Exception as e:
        print(f"  CrossRef error: {e}")
        return None


def crossref_lookup_by_doi(doi):
    """Lookup CrossRef by DOI, return full metadata."""
    try:
        resp = requests.get(f"{CROSSREF_API}/{doi}", headers=HEADERS, timeout=30)
        resp.raise_for_status()
        item = resp.json().get('message', {})
        return extract_metadata(item)
    except Exception as e:
        print(f"  CrossRef DOI error: {e}")
        return None


def extract_metadata(item):
    """Extract standardized metadata from CrossRef response."""
    authors = []
    for a in item.get('author', []):
        given = a.get('given', '')
        family = a.get('family', '')
        if family:
            authors.append(f"{family}, {given}" if given else family)

    # Journal
    journal = None
    for field in ['container-title', 'short-container-title']:
        titles = item.get(field, [])
        if titles:
            journal = titles[0]
            break

    # Year
    year = None
    for date_field in ['published-print', 'published-online', 'created']:
        dp = item.get(date_field, {}).get('date-parts', [[None]])
        if dp and dp[0] and dp[0][0]:
            year = str(dp[0][0])
            break

    # Abstract
    abstract = item.get('abstract', '')
    if abstract:
        abstract = re.sub(r'<[^>]+>', '', abstract).strip()

    return {
        'doi': item.get('DOI'),
        'title': ' '.join(item.get('title', [])),
        'author': ' and '.join(authors),
        'year': year,
        'journal': journal,
        'volume': item.get('volume'),
        'pages': item.get('page'),
        'abstract': abstract[:500] if abstract else None,
        'type': item.get('type', 'journal-article'),
    }


def update_bibtex(key, metadata):
    """Update BibTeX entry with new metadata."""
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = rf'(@\w+\{{{re.escape(key)},)(.*?)(\n\}})'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return False

    entry_body = match.group(2)
    changes = []

    field_map = {
        'title': 'title',
        'author': 'author',
        'journal': 'journal',
        'doi': 'doi',
        'volume': 'volume',
        'pages': 'pages',
    }

    for meta_key, bib_key in field_map.items():
        value = metadata.get(meta_key)
        if not value:
            continue

        # Check if field already exists with real content
        existing = re.search(rf'^\s*{bib_key}\s*=\s*[\{{"](.*?)[\}}"]\s*,?\s*$', entry_body, re.MULTILINE | re.IGNORECASE)

        if existing:
            old_val = existing.group(1)
            if 'Title to be added' in old_val or not old_val.strip():
                # Replace stub
                entry_body = entry_body[:existing.start()] + f'  {bib_key} = {{{value}}},' + entry_body[existing.end():]
                changes.append(f"{bib_key}: '{old_val[:30]}' -> '{str(value)[:30]}'")
        else:
            # Add new field
            entry_body += f'\n  {bib_key} = {{{value}}},'
            changes.append(f"+{bib_key}: '{str(value)[:30]}'")

    if changes:
        new_entry = match.group(1) + entry_body + match.group(3)
        content = content[:match.start()] + new_entry + content[match.end():]
        with open(BIB_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes


def update_yaml(key, metadata):
    """Update paper YAML with enriched metadata."""
    yaml_path = YAML_DIR / f"PAP-{key}.yaml"
    if not yaml_path.exists():
        return False

    with open(yaml_path) as f:
        data = yaml.safe_load(f) or {}

    changes = []

    if metadata.get('title') and (not data.get('title') or data.get('title') == 'Title to be added'):
        data['title'] = metadata['title']
        changes.append('title')

    if metadata.get('abstract') and (not data.get('abstract') or 'imaging spectrometry' in str(data.get('abstract', '')).lower()):
        data['abstract'] = metadata['abstract']
        data['abstract_source'] = 'crossref'
        data['abstract_fetched'] = datetime.now().strftime('%Y-%m-%d')
        changes.append('abstract')

    if metadata.get('doi') and not data.get('doi'):
        data['doi'] = metadata['doi']
        if 'doi_missing_reason' in data:
            del data['doi_missing_reason']
        changes.append('doi')

    if changes:
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return changes


def git_commit(message):
    """Commit and push changes."""
    subprocess.run(['git', 'config', '--local', 'user.email',
                    'github-actions[bot]@users.noreply.github.com'], check=True)
    subprocess.run(['git', 'config', '--local', 'user.name',
                    'github-actions[bot]'], check=True)
    subprocess.run(['git', 'add', '-A'], check=True)

    result = subprocess.run(['git', 'diff', '--staged', '--quiet'])
    if result.returncode != 0:
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push'], check=True)
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description='Paper Metadata Enrichment')
    parser.add_argument('--priority', default='P2', choices=PRIORITY_FILTERS.keys())
    parser.add_argument('--batch-size', type=int, default=50)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    print(f"Priority: {args.priority}")
    print(f"Batch size: {args.batch_size}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Load queue
    queue = load_queue()
    pfilter = PRIORITY_FILTERS[args.priority]
    filtered = [q for q in queue if pfilter(q) and q.get('status') == 'pending']

    print(f"Queue: {len(queue)} total, {len(filtered)} matching {args.priority}")
    batch = filtered[:args.batch_size]
    print(f"Processing: {len(batch)} papers")
    print()

    log = {
        'run_date': datetime.now().isoformat(),
        'priority': args.priority,
        'batch_size': args.batch_size,
        'results': [],
    }
    enriched_count = 0

    for i, item in enumerate(batch):
        key = item['key']
        title = item.get('current_title')
        author = item.get('current_author')
        year = item.get('current_year')

        print(f"[{i+1}/{len(batch)}] {key}", end=" ")

        metadata = None

        # Strategy 1: Search by title if we have one
        if title:
            metadata = crossref_search_by_title(title, author, year)
        # Strategy 2: Search by author + year
        elif author and year:
            query = f"{author.split(',')[0]} {year}"
            metadata = crossref_search_by_title(query, None, year)

        if metadata and metadata.get('title'):
            print(f"-> {metadata['title'][:50]}...")

            if not args.dry_run:
                bib_changes = update_bibtex(key, metadata)
                yaml_changes = update_yaml(key, metadata)
                print(f"   BibTeX: {bib_changes}")
                print(f"   YAML: {yaml_changes}")

            enriched_count += 1
            log['results'].append({
                'key': key,
                'status': 'enriched',
                'doi': metadata.get('doi'),
                'title': metadata.get('title'),
            })
        else:
            print("-> NOT FOUND")
            log['results'].append({
                'key': key,
                'status': 'not_found',
            })

        time.sleep(0.5)  # Rate limit

    # Save log
    log['summary'] = {
        'processed': len(batch),
        'enriched': enriched_count,
        'not_found': len(batch) - enriched_count,
        'success_rate': round(enriched_count / len(batch) * 100, 1) if batch else 0,
    }

    with open(LOG_FILE, 'w') as f:
        yaml.dump(log, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Processed: {len(batch)}")
    print(f"Enriched:  {enriched_count} ({log['summary']['success_rate']}%)")
    print(f"Not found: {len(batch) - enriched_count}")

    # Commit
    if not args.dry_run and enriched_count > 0:
        msg = f"""feat(PAP): Enrich {enriched_count} papers with CrossRef metadata ({args.priority})

Processed {len(batch)} papers, enriched {enriched_count} ({log['summary']['success_rate']}% success).
Priority: {args.priority}, Batch: {args.batch_size}

https://claude.ai/code/session_0178bU8m68SGTVPGZPkEqjDQ"""
        if git_commit(msg):
            print("Committed and pushed.")


if __name__ == "__main__":
    main()
