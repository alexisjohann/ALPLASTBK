#!/usr/bin/env python3
"""
Match parameters without literature_sources to papers in bcm_master.bib.

Uses keyword matching per parameter group to find relevant papers,
then adds literature_sources to each parameter.

Usage:
  python scripts/match_params_to_papers.py --dry-run       # Show matches
  python scripts/match_params_to_papers.py --batch 1       # Apply 1
  python scripts/match_params_to_papers.py --batch all      # Apply all
"""

import yaml
import re
import argparse
from datetime import datetime
from collections import defaultdict

# Keyword mappings: parameter prefix → search terms for BibTeX
PARAM_KEYWORDS = {
    'SF': {
        'keywords': ['skill formation', 'human capital', 'child development', 'personality',
                      'cognitive development', 'non-cognitive', 'conscientiousness', 'openness',
                      'agreeableness', 'neuroticism', 'extraversion', 'big five', 'dreyfus',
                      'complementarity', 'dynamic complementarity', 'investment'],
        'authors': ['Heckman', 'Cunha', 'Schennach', 'Roberts', 'Almlund'],
        'theory_support': ['MS-SF'],
    },
    'VE': {
        'keywords': ['virtue ethics', 'character', 'habituation', 'eudaimonia', 'golden mean',
                      'self-control', 'trait', 'preference formation', 'habit'],
        'authors': ['Heckman', 'Borghans', 'Duckworth'],
        'theory_support': ['MS-VE'],
    },
    'HLT': {
        'keywords': ['pflege', 'care', 'nursing', 'long-term care', 'pflegegrad',
                      'dementia', 'elderly', 'caregiving', 'health insurance'],
        'authors': [],
        'theory_support': [],
    },
    'CM': {
        'keywords': ['firestorm', 'crisis', 'virality', 'social media', 'empathy',
                      'apology', 'compensation', 'service recovery', 'complaint'],
        'authors': ['Herhausen', 'Sutter'],
        'theory_support': ['MS-CM'],
    },
    'CX': {
        'keywords': ['customer experience', 'interaction', 'touchpoint', 'moment of truth',
                      'kano', 'service quality', 'customer journey'],
        'authors': [],
        'theory_support': [],
    },
    'CJ': {
        'keywords': ['customer journey', 'satisfaction', 'loyalty', 'inspiration',
                      'net promoter', 'customer lifetime', 'retention'],
        'authors': [],
        'theory_support': [],
    },
    'EXE': {
        'keywords': ['executive', 'CEO', 'compensation', 'corporate governance',
                      'narrative', 'status', 'control', 'managerial'],
        'authors': [],
        'theory_support': [],
    },
    'CTX': {
        'keywords': ['context', 'taboo', 'trust', 'institutional trust', 'privacy',
                      'social norm', 'cultural context', 'finance discussion'],
        'authors': ['Fehr'],
        'theory_support': [],
    },
    'INT': {
        'keywords': ['nudge', 'social norm', 'identity', 'warm glow', 'intervention',
                      'default', 'framing', 'prosocial', 'charitable'],
        'authors': ['Thaler', 'Sunstein', 'Andreoni', 'Akerlof'],
        'theory_support': ['MS-SP', 'MS-IB'],
    },
    'POL': {
        'keywords': ['fiscal illusion', 'lobby', 'political economy', 'public choice',
                      'debt brake', 'budget', 'diffuse interest', 'concentrated interest'],
        'authors': ['Buchanan', 'Olson'],
        'theory_support': [],
    },
    'ENT': {
        'keywords': ['entrepreneurship', 'product-market fit', 'startup', 'venture',
                      'innovation', 'approval', 'rejection'],
        'authors': [],
        'theory_support': [],
    },
    'TP': {
        'keywords': ['technology policy', 'productivity', 'bandwagon', 'countervailing',
                      'narrative', 'technological change', 'innovation policy'],
        'authors': [],
        'theory_support': [],
    },
    'SPO': {
        'keywords': ['sport', 'injury', 'athletic', 'contact sport', 'training',
                      'performance', 'exercise'],
        'authors': [],
        'theory_support': [],
    },
    'RE': {
        'keywords': ['real estate', 'housing', 'flexibility', 'property'],
        'authors': [],
        'theory_support': [],
    },
}


def parse_bibtex(path='bibliography/bcm_master.bib'):
    """Parse BibTeX file into list of entries."""
    entries = []
    current = {}

    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Split by @ entries
    raw_entries = re.split(r'\n@', content)

    for raw in raw_entries:
        if not raw.strip():
            continue

        # Extract key
        key_match = re.match(r'\w+\{([^,]+),', raw)
        if not key_match:
            continue

        key = key_match.group(1).strip()
        entry = {'key': key, 'raw': raw}

        # Extract fields
        for field in ['title', 'author', 'year', 'journal', 'abstract',
                      'theory_support', 'use_for', 'keywords', 'notes']:
            pattern = rf'{field}\s*=\s*\{{([^}}]*)\}}'
            match = re.search(pattern, raw, re.IGNORECASE)
            if match:
                entry[field] = match.group(1)

        entries.append(entry)

    return entries


def search_papers(entries, keywords, authors, theory_supports):
    """Search BibTeX entries for matching papers."""
    matches = []

    for entry in entries:
        score = 0
        match_reasons = []

        # Search in title and abstract
        title = entry.get('title', '').lower()
        abstract = entry.get('abstract', '').lower()
        text = title + ' ' + abstract

        for kw in keywords:
            if kw.lower() in text:
                score += 2
                match_reasons.append(f'keyword:{kw}')

        # Author match
        author_field = entry.get('author', '')
        for auth in authors:
            if auth.lower() in author_field.lower():
                score += 3
                match_reasons.append(f'author:{auth}')

        # Theory support match
        ts = entry.get('theory_support', '')
        for t in theory_supports:
            if t in ts:
                score += 5
                match_reasons.append(f'theory:{t}')

        if score >= 2:
            matches.append({
                'key': entry['key'],
                'title': entry.get('title', '')[:80],
                'author': entry.get('author', '')[:50],
                'year': entry.get('year', ''),
                'score': score,
                'reasons': match_reasons,
            })

    # Sort by score descending
    matches.sort(key=lambda x: -x['score'])
    return matches


def get_param_prefix(param_id):
    """Extract prefix from param ID like PAR-SF-001 → SF."""
    parts = param_id.split('-')
    if len(parts) >= 2:
        return parts[1]
    return ''


def build_literature_source(paper, param_name):
    """Create a literature_sources entry from a paper match."""
    return {
        'key': f'PAP-{paper["key"]}' if not paper['key'].startswith('PAP-') else paper['key'],
        'finding': f'Relevant for {param_name} ({", ".join(paper["reasons"][:2])})',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--batch', type=str, default='1')
    parser.add_argument('--min-score', type=int, default=3, help='Minimum match score')
    parser.add_argument('--max-sources', type=int, default=3, help='Max sources per param')
    args = parser.parse_args()

    # Load data
    with open('data/parameter-registry.yaml', 'r') as f:
        data = yaml.safe_load(f)

    entries = parse_bibtex()
    print(f'Loaded {len(entries)} BibTeX entries')

    # Find params needing literature
    params_to_match = []
    for section_key, section_val in data.items():
        if not isinstance(section_val, list):
            continue
        if not section_val or not isinstance(section_val[0], dict) or 'id' not in section_val[0]:
            continue
        for i, param in enumerate(section_val):
            if param.get('parameter_tier') == 1:
                continue
            if param.get('literature_sources'):
                continue
            params_to_match.append({
                'section': section_key,
                'index': i,
                'id': param.get('id', ''),
                'name': param.get('name', param.get('symbol', '')),
                'prefix': get_param_prefix(param.get('id', '')),
            })

    print(f'Parameters needing literature: {len(params_to_match)}')

    # Match each param to papers
    results = []
    for pm in params_to_match:
        prefix = pm['prefix']
        config = PARAM_KEYWORDS.get(prefix, {
            'keywords': [pm['name'].lower()],
            'authors': [],
            'theory_support': [],
        })

        matches = search_papers(
            entries,
            config['keywords'],
            config['authors'],
            config.get('theory_support', []),
        )

        # Filter by min score and take top N
        matches = [m for m in matches if m['score'] >= args.min_score]
        matches = matches[:args.max_sources]

        if matches:
            results.append({
                'param': pm,
                'matches': matches,
            })

    print(f'Parameters with matches: {len(results)} / {len(params_to_match)}')
    print()

    if args.dry_run:
        for r in results:
            pm = r['param']
            print(f'{pm["id"]:20s} ({pm["name"][:40]})')
            for m in r['matches']:
                print(f'  → {m["key"][:30]:30s} score={m["score"]:2d}  {m["reasons"][:3]}')

        no_match = [pm for pm in params_to_match if not any(r['param']['id'] == pm['id'] for r in results)]
        if no_match:
            print(f'\nNo matches found for {len(no_match)} parameters:')
            for pm in no_match:
                print(f'  {pm["id"]:20s} ({pm["name"][:40]})')
        return

    # Apply matches
    if args.batch == 'all':
        to_apply = results
    else:
        to_apply = results[:int(args.batch)]

    applied = 0
    for r in to_apply:
        pm = r['param']
        section = data[pm['section']]
        param = section[pm['index']]

        # Build literature_sources
        lit_sources = []
        for m in r['matches']:
            lit_sources.append(build_literature_source(m, pm['name']))

        param['literature_sources'] = lit_sources
        param['parameter_tier'] = 1
        if 'last_updated' not in param:
            param['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        applied += 1

    # Update metadata
    if 'metadata' in data:
        data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        old_version = str(data['metadata'].get('version', '1.25'))
        parts = old_version.split('.')
        if len(parts) >= 2:
            parts[-1] = str(int(parts[-1]) + 1)
            data['metadata']['version'] = '.'.join(parts)

    with open('data/parameter-registry.yaml', 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)

    print(f'Applied literature to {applied} parameters')
    remaining = len(results) - applied
    if remaining > 0:
        print(f'Remaining with matches: {remaining}')


if __name__ == '__main__':
    main()
