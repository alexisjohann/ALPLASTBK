#!/usr/bin/env python3
"""
Batch upgrade papers from Integration Level 2 to Level 3.

I3 requires: bibtex + theory_support + case_registry entry.
This script:
1. Finds papers at I2 with rich metadata
2. Generates case entries from existing paper YAML data
3. Appends cases to case-registry.yaml
4. Updates integration_level in paper YAMLs

Usage:
  python scripts/batch_upgrade_i2_to_i3.py --dry-run          # Show what would change
  python scripts/batch_upgrade_i2_to_i3.py --batch 1           # Upgrade 1
  python scripts/batch_upgrade_i2_to_i3.py --batch 20          # Upgrade 20
  python scripts/batch_upgrade_i2_to_i3.py --l3-only           # Only L3 content papers
"""

import yaml
import os
import re
import argparse
import glob
from datetime import datetime


def load_paper_yaml(path):
    """Load a paper YAML file safely."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return None


def normalize_integration_level(val):
    """Normalize integration level to integer (handles '2', 'I2', 2)."""
    if val is None:
        return None
    s = str(val).strip().upper()
    if s.startswith('I'):
        s = s[1:]
    try:
        return int(s)
    except ValueError:
        return None


def get_integration_level(data):
    """Extract integration level from paper data (various formats)."""
    if not data:
        return None
    # Direct field
    if 'integration_level' in data:
        return normalize_integration_level(data['integration_level'])
    # Nested in status
    if isinstance(data.get('status'), dict) and 'integration_level' in data['status']:
        return normalize_integration_level(data['status']['integration_level'])
    # Nested in ebf_integration
    if isinstance(data.get('ebf_integration'), dict) and 'integration_level' in data['ebf_integration']:
        return normalize_integration_level(data['ebf_integration']['integration_level'])
    # Nested in prior_score
    if isinstance(data.get('prior_score'), dict) and 'integration_level' in data['prior_score']:
        return normalize_integration_level(data['prior_score']['integration_level'])
    return None


def get_content_level(data):
    """Extract content level from paper data."""
    if not data:
        return None
    cl = data.get('content_level', '')
    if cl:
        return str(cl)
    # Nested in full_text
    if isinstance(data.get('full_text'), dict):
        cl = data['full_text'].get('content_level', '')
        if cl:
            return str(cl)
    # Nested in prior_score
    if isinstance(data.get('prior_score'), dict):
        cl = data['prior_score'].get('content_level', '')
        if cl:
            return str(cl)
    # Nested in status
    if isinstance(data.get('status'), dict):
        cl = data['status'].get('content_level', '')
        if cl:
            return str(cl)
    return None


def score_paper_richness(data):
    """Score how rich the paper metadata is (higher = easier to upgrade)."""
    score = 0
    if not data:
        return 0

    # Has behavioral_mapping
    if data.get('behavioral_mapping'):
        score += 3
    # Has theory_integration
    if data.get('theory_integration'):
        score += 3
    # Has parameter_contributions
    if data.get('parameter_contributions'):
        score += 2
    # Has key_findings_structured
    if data.get('key_findings_structured'):
        score += 2
    # Has chapter_relevance
    if data.get('chapter_relevance'):
        score += 1
    # Has evidence_tier (direct or nested)
    et = data.get('evidence_tier')
    if not et and isinstance(data.get('ebf_integration'), dict):
        et = data['ebf_integration'].get('evidence_tier')
    if et == 1:
        score += 3
    elif et == 2:
        score += 2
    elif et:
        score += 1
    # Has abstract
    if data.get('abstract'):
        score += 1
    # Has full_text
    ft = data.get('full_text', {})
    if isinstance(ft, dict) and ft.get('available'):
        score += 2
    # Has linked_papers
    if data.get('linked_papers'):
        score += 1
    # Has ebf_integration with theory_support
    ei = data.get('ebf_integration', {})
    if isinstance(ei, dict) and ei.get('theory_support'):
        score += 2
    # Has ebf_integration with use_for
    if isinstance(ei, dict) and ei.get('use_for'):
        score += 1
    # Content level bonus
    cl = get_content_level(data)
    if cl == 'L3':
        score += 3
    elif cl == 'L2':
        score += 1

    return score


def extract_title(data):
    """Extract title from various paper YAML formats."""
    if data.get('title'):
        return data['title']
    if isinstance(data.get('bibliographic'), dict):
        return data['bibliographic'].get('title', '')
    return ''


def extract_authors(data):
    """Extract author string from various formats."""
    if data.get('author'):
        return data['author']
    if isinstance(data.get('bibliographic'), dict):
        authors = data['bibliographic'].get('authors', [])
        if authors and isinstance(authors[0], dict):
            return ', '.join(f"{a.get('family', '')} {a.get('given', '')}" for a in authors[:3])
        elif authors and isinstance(authors[0], str):
            return ', '.join(authors[:3])
    return ''


def extract_year(data):
    """Extract year from various formats."""
    if data.get('year'):
        return str(data['year'])
    if isinstance(data.get('bibliographic'), dict):
        return str(data['bibliographic'].get('year', ''))
    return ''


def extract_paper_id(data, filename):
    """Extract paper ID."""
    if data.get('paper_id'):
        return data['paper_id']
    if data.get('superkey'):
        return data['superkey']
    # Derive from filename
    base = os.path.basename(filename).replace('.yaml', '')
    return base


def extract_domain(data):
    """Guess domain from paper content."""
    title = extract_title(data).lower()
    abstract = str(data.get('abstract', '')).lower()
    text = title + ' ' + abstract

    domain_keywords = {
        'finance': ['finance', 'banking', 'investment', 'stock', 'portfolio', 'monetary'],
        'labor': ['labor', 'wage', 'employment', 'worker', 'hiring', 'attrition', 'manager'],
        'health': ['health', 'medical', 'patient', 'hospital', 'disease', 'care'],
        'education': ['education', 'school', 'student', 'learning', 'skill'],
        'politics': ['politic', 'election', 'voting', 'populis', 'democrat', 'authoritarian'],
        'behavior': ['nudge', 'choice architecture', 'default', 'framing', 'heuristic'],
        'social_preferences': ['cooperation', 'trust', 'fairness', 'reciprocity', 'altruism', 'social preference'],
        'identity': ['identity', 'norm', 'culture', 'religion'],
        'market_design': ['market design', 'auction', 'mechanism', 'matching'],
        'development': ['development', 'poverty', 'inequality'],
        'insurance': ['insurance', 'risk', 'moral hazard'],
    }

    for domain, keywords in domain_keywords.items():
        for kw in keywords:
            if kw in text:
                return domain
    return 'economics'


def build_case_entry(data, paper_id, case_id):
    """Build a case registry entry from paper metadata."""
    title = extract_title(data)
    authors = extract_authors(data)
    year = extract_year(data)
    domain = extract_domain(data)

    # Extract key finding
    findings = data.get('key_findings_structured', {})
    if isinstance(findings, dict):
        s4 = findings.get('S4_findings', findings.get('S4', []))
        if isinstance(s4, list) and s4:
            first_finding = s4[0]
            if isinstance(first_finding, dict):
                key_finding = first_finding.get('finding', first_finding.get('formal_result', ''))
            else:
                key_finding = str(first_finding)
        else:
            key_finding = str(s4)[:200] if s4 else ''
    elif isinstance(findings, list) and findings:
        first = findings[0]
        if isinstance(first, dict):
            key_finding = first.get('finding', first.get('ebf_relevance', ''))
        else:
            key_finding = str(first)[:200]
    else:
        key_finding = ''

    if not key_finding:
        key_finding = f"Key empirical findings from {authors} ({year})"

    # Extract 10C dimensions from behavioral_mapping
    ten_c = {}
    bm = data.get('behavioral_mapping', {})
    if isinstance(bm, dict):
        dims = bm.get('10c_dimensions', bm.get('10C_dimensions', {}))
        if isinstance(dims, dict):
            for dim_name, dim_data in dims.items():
                if isinstance(dim_data, dict):
                    rel = dim_data.get('relevance', 'low')
                    if rel in ('high', 'medium'):
                        detail = dim_data.get('detail', dim_data.get('mapping', ''))
                        ten_c[dim_name] = str(detail)[:100] if detail else rel
                elif isinstance(dim_data, str):
                    ten_c[dim_name] = dim_data[:100]
        # Also check psi_dimensions
        psi = bm.get('psi_dimensions', {})
        if isinstance(psi, dict) and 'WHEN' not in ten_c:
            for psi_name, psi_data in psi.items():
                if isinstance(psi_data, dict) and psi_data.get('relevance') in ('high', 'medium'):
                    ten_c.setdefault('WHEN', psi_data.get('description', '')[:100])

    # Build theory references
    theories = []
    ti = data.get('theory_integration', {})
    if isinstance(ti, dict):
        primary = ti.get('primary_theories', [])
        if isinstance(primary, list):
            for t in primary[:3]:
                if isinstance(t, dict):
                    theories.append(t.get('theory_id', ''))

    # Build the case YAML string
    case_lines = []
    case_lines.append(f"  - id: {case_id}")
    case_lines.append(f"    name: \"{title[:80]}\"")
    case_lines.append(f"    domain: [\"{domain}\"]")
    case_lines.append(f"    source: \"{paper_id}\"")
    case_lines.append(f"    source_type: paper")

    # 10C section
    if ten_c:
        case_lines.append(f"    10C:")
        for dim, val in list(ten_c.items())[:4]:
            safe_val = val.replace('"', "'").replace('\n', ' ')[:80]
            case_lines.append(f"      {dim}: \"{safe_val}\"")

    # Insight
    safe_finding = key_finding.replace('"', "'").replace('\n', ' ')[:150]
    case_lines.append(f"    insight: \"{safe_finding}\"")
    case_lines.append(f"    implication: \"Provides empirical evidence for EBF behavioral modeling\"")

    # References
    case_lines.append(f"    references:")
    case_lines.append(f"      - key: {paper_id.replace('PAP-', '')}")
    case_lines.append(f"        type: primary")
    if theories:
        case_lines.append(f"    theories: [{', '.join(theories[:3])}]")

    case_lines.append(f"    created: \"{datetime.now().strftime('%Y-%m-%d')}\"")
    case_lines.append("")

    return '\n'.join(case_lines)


def update_paper_yaml_level(path, data, new_level=3):
    """Update integration_level in a paper YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace ALL occurrences of integration_level: 2 or I2 (covers direct, status, ebf_integration)
    content = re.sub(
        r'(integration_level:\s*)2\b',
        f'\\g<1>{new_level}',
        content
    )
    content = re.sub(
        r'(integration_level:\s*)I2\b',
        f'\\g<1>{new_level}',
        content
    )

    # Update integration_level_name
    content = content.replace(
        'integration_level_name: STANDARD',
        'integration_level_name: CASE'
    )

    # Update header comment
    content = re.sub(
        r'# Integration Level: 2 \(STANDARD\)',
        f'# Integration Level: {new_level} (CASE)',
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def get_next_case_id(case_registry_path):
    """Get the next available case ID by scanning case-registry.yaml."""
    max_id = 960  # We know CAS-960 was the last one added
    try:
        with open(case_registry_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'CAS-(\d+)', line)
                if match:
                    num = int(match.group(1))
                    if num > max_id:
                        max_id = num
    except:
        pass
    return max_id + 1


def main():
    parser = argparse.ArgumentParser(description='Batch upgrade I2 papers to I3')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be upgraded')
    parser.add_argument('--batch', type=str, default='5', help='Number to upgrade (or "all")')
    parser.add_argument('--l3-only', action='store_true', help='Only upgrade L3 content papers')
    parser.add_argument('--min-score', type=int, default=4, help='Minimum richness score')
    args = parser.parse_args()

    # Find all paper YAMLs
    paper_dir = 'data/paper-references'
    papers = []

    for path in glob.glob(os.path.join(paper_dir, 'PAP-*.yaml')):
        data = load_paper_yaml(path)
        if not data:
            continue

        il = get_integration_level(data)
        if il != 2:
            continue

        cl = get_content_level(data)
        if args.l3_only and cl != 'L3':
            continue

        score = score_paper_richness(data)
        if score < args.min_score:
            continue

        paper_id = extract_paper_id(data, path)
        title = extract_title(data)

        papers.append({
            'path': path,
            'data': data,
            'paper_id': paper_id,
            'title': title[:60],
            'content_level': cl or '?',
            'score': score,
            'evidence_tier': data.get('evidence_tier', '?'),
        })

    # Sort: L3 first, then by score descending
    papers.sort(key=lambda p: (
        0 if p['content_level'] == 'L3' else 1,
        -p['score']
    ))

    print(f"Found {len(papers)} I2 papers eligible for upgrade (min_score={args.min_score})")
    print()

    if args.dry_run:
        for i, p in enumerate(papers):
            print(f"  {i+1:3d}. {p['paper_id'][:40]:40s} C={p['content_level']} ET={p['evidence_tier']} score={p['score']:2d}  {p['title']}")
        return

    # Determine batch size
    if args.batch == 'all':
        to_upgrade = papers
    else:
        to_upgrade = papers[:int(args.batch)]

    if not to_upgrade:
        print("Nothing to upgrade.")
        return

    # Get next case ID
    case_registry_path = 'data/case-registry.yaml'
    next_id = get_next_case_id(case_registry_path)

    # Generate case entries and update paper YAMLs
    case_entries = []
    upgraded = []

    for p in to_upgrade:
        case_id = f"CAS-{next_id}"
        case_yaml = build_case_entry(p['data'], p['paper_id'], case_id)
        case_entries.append(case_yaml)

        # Update the paper YAML
        update_paper_yaml_level(p['path'], p['data'], new_level=3)

        upgraded.append({
            'paper_id': p['paper_id'],
            'case_id': case_id,
            'title': p['title'],
            'score': p['score'],
        })

        next_id += 1

    # Append cases to registry
    if case_entries:
        with open(case_registry_path, 'a', encoding='utf-8') as f:
            f.write('\n# === Batch I2→I3 Upgrade (' + datetime.now().strftime('%Y-%m-%d') + ') ===\n')
            for entry in case_entries:
                f.write(entry + '\n')

    print(f"Upgraded {len(upgraded)} papers from I2 → I3:")
    for u in upgraded:
        print(f"  {u['case_id']:8s} {u['paper_id'][:40]:40s} score={u['score']:2d}  {u['title']}")

    remaining = len(papers) - len(upgraded)
    if remaining > 0:
        print(f"\nRemaining eligible: {remaining}")


if __name__ == '__main__':
    main()
