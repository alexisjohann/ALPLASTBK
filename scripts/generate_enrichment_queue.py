#!/usr/bin/env python3
"""
Generate Paper Enrichment Queue
================================
Analyzes all BibTeX entries, identifies missing metadata,
prioritizes by LaTeX citation status, and exports a queue
for the GitHub Action enrichment workflow.

Output: data/paper-enrichment-queue.yaml
"""

import re
import os
import glob
import yaml
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB_FILE = os.path.join(REPO, "bibliography/bcm_master.bib")
QUEUE_FILE = os.path.join(REPO, "data/paper-enrichment-queue.yaml")


def parse_bibtex():
    """Parse all BibTeX entries with field-level detail."""
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = {}
    for block in re.split(r'\n(?=@)', content):
        m = re.match(r'@(\w+)\{([^,]+),', block)
        if not m:
            continue
        etype, key = m.group(1).lower(), m.group(2)

        def get_field(name):
            p = re.search(rf'^\s*{name}\s*=\s*[\{{"](.*?)[\}}"]\s*,?\s*$', block, re.MULTILINE | re.IGNORECASE)
            return p.group(1).strip() if p else None

        title = get_field('title')
        is_stub = title and 'Title to be added' in title

        entries[key] = {
            'type': etype,
            'title': None if is_stub else title,
            'author': get_field('author'),
            'year': get_field('year'),
            'journal': get_field('journal') or get_field('booktitle'),
            'doi': get_field('doi'),
            'volume': get_field('volume'),
            'pages': get_field('pages'),
            'is_stub': is_stub,
        }

    return entries


def find_latex_citations():
    """Find all BibTeX keys cited in LaTeX files."""
    cited = defaultdict(set)  # key -> set of files
    tex_files = glob.glob(os.path.join(REPO, "appendices/*.tex")) + \
                glob.glob(os.path.join(REPO, "chapters/*.tex"))

    for fpath in tex_files:
        with open(fpath, 'r', errors='replace') as f:
            content = f.read()
        for m in re.finditer(r'\\cite[pt]*\{([^}]+)\}', content):
            for key in m.group(1).split(','):
                k = key.strip()
                if k:
                    cited[k].add(os.path.basename(fpath))

    return cited


def assess_completeness(entry):
    """Return list of missing fields and completeness score."""
    missing = []
    fields = {
        'title': 3,      # weight
        'author': 3,
        'year': 2,
        'journal': 2,
        'doi': 2,
        'volume': 1,
        'pages': 1,
    }

    total_weight = sum(fields.values())
    score = 0

    for field, weight in fields.items():
        if entry.get(field):
            score += weight
        else:
            missing.append(field)

    return missing, round(score / total_weight, 2)


def main():
    print("Parsing BibTeX...")
    entries = parse_bibtex()
    print(f"  {len(entries)} entries found")

    print("Finding LaTeX citations...")
    cited = find_latex_citations()
    print(f"  {len(cited)} unique keys cited")

    # Build queue
    queue = []
    stats = {
        'total': len(entries),
        'complete': 0,
        'needs_enrichment': 0,
        'cited_incomplete': 0,
        'uncited_incomplete': 0,
    }

    for key, entry in entries.items():
        missing, score = assess_completeness(entry)
        is_cited = key in cited

        if not missing:
            stats['complete'] += 1
            continue

        stats['needs_enrichment'] += 1
        if is_cited:
            stats['cited_incomplete'] += 1
        else:
            stats['uncited_incomplete'] += 1

        # Priority: cited + more missing = higher priority
        priority = 0
        if is_cited:
            priority += 100
        if entry['is_stub']:
            priority += 50
        if 'title' in missing:
            priority += 30
        if 'doi' in missing:
            priority += 10
        if 'journal' in missing:
            priority += 10
        priority += len(missing) * 5

        item = {
            'key': key,
            'priority': priority,
            'is_cited': is_cited,
            'cited_in': sorted(cited.get(key, [])) if is_cited else [],
            'missing_fields': missing,
            'completeness': score,
            'current_title': entry.get('title'),
            'current_author': entry.get('author'),
            'current_year': entry.get('year'),
            'current_journal': entry.get('journal'),
            'status': 'pending',
        }
        queue.append(item)

    # Sort by priority (highest first)
    queue.sort(key=lambda x: -x['priority'])

    # Build output
    output = {
        'metadata': {
            'generated': '2026-02-07',
            'total_papers': stats['total'],
            'complete': stats['complete'],
            'needs_enrichment': stats['needs_enrichment'],
            'cited_incomplete': stats['cited_incomplete'],
            'uncited_incomplete': stats['uncited_incomplete'],
            'completeness_rate': round(stats['complete'] / stats['total'] * 100, 1),
        },
        'priority_summary': {
            'P1_cited_no_title': len([q for q in queue if q['is_cited'] and 'title' in q['missing_fields']]),
            'P2_cited_no_doi': len([q for q in queue if q['is_cited'] and 'doi' in q['missing_fields'] and 'title' not in q['missing_fields']]),
            'P3_cited_no_journal': len([q for q in queue if q['is_cited'] and 'journal' in q['missing_fields']]),
            'P4_uncited_stubs': len([q for q in queue if not q['is_cited'] and 'title' in q['missing_fields']]),
            'P5_uncited_no_doi': len([q for q in queue if not q['is_cited'] and 'doi' in q['missing_fields'] and 'title' not in q['missing_fields']]),
        },
        'queue': queue,
    }

    with open(QUEUE_FILE, 'w') as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\n{'='*60}")
    print(f"ENRICHMENT QUEUE GENERATED: {QUEUE_FILE}")
    print(f"{'='*60}")
    print(f"Total papers:        {stats['total']}")
    print(f"Complete:            {stats['complete']} ({stats['complete']/stats['total']*100:.1f}%)")
    print(f"Need enrichment:     {stats['needs_enrichment']}")
    print(f"  Cited + incomplete:{stats['cited_incomplete']} (HIGH PRIORITY)")
    print(f"  Uncited + incomplete:{stats['uncited_incomplete']}")
    print()
    print("Priority breakdown:")
    print(f"  P1 Cited, no title:    {output['priority_summary']['P1_cited_no_title']}")
    print(f"  P2 Cited, no DOI:      {output['priority_summary']['P2_cited_no_doi']}")
    print(f"  P3 Cited, no journal:  {output['priority_summary']['P3_cited_no_journal']}")
    print(f"  P4 Uncited stubs:      {output['priority_summary']['P4_uncited_stubs']}")
    print(f"  P5 Uncited, no DOI:    {output['priority_summary']['P5_uncited_no_doi']}")


if __name__ == "__main__":
    main()
