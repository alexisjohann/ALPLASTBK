#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige Evidence-Tier-Klassifikation (ersetzt durch add_evidence_tier.py) │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Classify papers by evidence tier based on author, title, and methodology patterns.

Evidence Tier System:
- Tier 1: BE experimental with causal ID (RCT, IV, RDD + incentives + parameters)
- Tier 2: BE observational / BS experimental (structural estimation, psychology RCTs)
- Tier 3: BS correlational (surveys, observational psychology)
- Tier 4: Anecdotal / popular science
- Tier 5: Theoretical / methodological (pure theory, frameworks)
"""

import yaml
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
YAML_PATH = BASE_DIR / "data" / "paper-sources.yaml"

# Author patterns for classification
TIER_1_AUTHORS = {
    # Experimental economists known for causal identification
    'fehr', 'list', 'levitt', 'gneezy', 'rustichini', 'charness',
    'duflo', 'banerjee', 'kremer', 'miguel', 'karlan',
    'chetty', 'friedman', 'saez', 'kleven',
    # Behavioral with strong experimental work
    'camerer', 'loewenstein', 'prelec', 'weber',
}

TIER_1_2_AUTHORS = {
    # Strong experimental but sometimes observational
    'thaler', 'benartzi', 'madrian', 'choi',
    'ariely', 'norton', 'mazar',
    'kahneman', 'tversky',
    'falk', 'gaechter', 'kosfeld', 'rockenbach',
    'malmendier', 'tate', 'shue',
    'dellavigna', 'pope', 'card',
    'imas', 'exley', 'niederle', 'vesterlund',
    # Labor economists with natural experiments
    'autor', 'katz', 'krueger', 'angrist', 'pischke',
    'acemoglu', 'robinson',
}

TIER_2_AUTHORS = {
    # Good empirical but not always causal
    'shiller', 'akerlof', 'blanchard',
    'laibson', 'odonoghue', 'rabin',
    'sunstein', 'jolls',
    'bertrand', 'mullainathan',
}

TIER_3_AUTHORS = {
    # Psychology / correlational
    'dweck', 'duckworth', 'baumeister', 'vohs',
    'mischel', 'bandura',
}

TIER_5_AUTHORS = {
    # Pure theory
    'arrow', 'debreu', 'nash', 'harsanyi', 'selten',
    'myerson', 'maskin', 'tirole', 'laffont',
    'milgrom', 'wilson', 'roth', 'shapley',
    'aumann', 'schelling', 'rubinstein',
    'stiglitz', 'spence', 'rothschild',
    'grossman', 'hart', 'holmstrom',
    'diamond', 'dybvig', 'mortensen', 'pissarides',
    'lucas', 'sargent', 'prescott', 'kydland',
    'becker', 'murphy', 'posner',
    'williamson', 'coase', 'north',
    # Methodological
    'heckman', 'mcfadden', 'newey', 'west',
    # Philosophy/methodology of science
    'polanyi', 'kuhn', 'collins', 'ioannidis', 'nosek',
    # Gigerenzer (mixed - some experimental, some theoretical)
    'gigerenzer', 'todd', 'hertwig', 'hoffrage',
}

# Title keywords for classification
TIER_1_KEYWORDS = [
    r'\bRCT\b', r'\brandomized\b', r'\bfield experiment\b',
    r'\bnatural experiment\b', r'\binstrumental variable\b',
    r'\bregression discontinuity\b', r'\bdifference.in.difference\b',
    r'\bcausal\b.*\bidentification\b', r'\bexogenous\b',
]

TIER_2_KEYWORDS = [
    r'\bexperiment\b', r'\blaboratory\b', r'\blab\b',
    r'\bincentivized\b', r'\btreatment\b', r'\bcontrol group\b',
    r'\bpanel data\b', r'\bstructural estimation\b',
]

TIER_3_KEYWORDS = [
    r'\bsurvey\b', r'\bcorrelation\b', r'\bcross.sectional\b',
    r'\bquestionnaire\b', r'\bself.report\b',
]

TIER_5_KEYWORDS = [
    r'\btheory\b', r'\btheoretical\b', r'\bmodel\b', r'\bframework\b',
    r'\baxiom\b', r'\bequilibrium\b', r'\boptimal\b',
    r'\bwelfare theorem\b', r'\bexistence\b', r'\bproof\b',
    r'\breview\b', r'\bhandbook\b', r'\bsurvey of\b',
]


def get_author_tier(authors):
    """Determine tier based on author names"""
    if not authors:
        return None

    # Normalize author names
    author_set = set()
    for author in authors:
        if isinstance(author, str):
            # Extract last name
            parts = author.lower().replace(',', ' ').split()
            for part in parts:
                if len(part) > 2:
                    author_set.add(part)

    # Check author patterns (priority order)
    for author in author_set:
        if author in TIER_1_AUTHORS:
            return 1

    for author in author_set:
        if author in TIER_5_AUTHORS:
            return 5

    for author in author_set:
        if author in TIER_1_2_AUTHORS:
            return 2

    for author in author_set:
        if author in TIER_2_AUTHORS:
            return 2

    for author in author_set:
        if author in TIER_3_AUTHORS:
            return 3

    return None


def get_title_tier(title):
    """Determine tier based on title keywords"""
    if not title:
        return None

    title_lower = title.lower()

    # Check Tier 1 keywords
    for pattern in TIER_1_KEYWORDS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return 1

    # Check Tier 5 keywords (theory)
    for pattern in TIER_5_KEYWORDS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return 5

    # Check Tier 2 keywords
    for pattern in TIER_2_KEYWORDS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return 2

    # Check Tier 3 keywords
    for pattern in TIER_3_KEYWORDS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return 3

    return None


def classify_paper(paper):
    """Classify a single paper, returning suggested tier and confidence"""
    # Already classified?
    existing_tier = paper.get('evidence_tier')
    if existing_tier is not None:
        return existing_tier, 'existing', 1.0

    authors = paper.get('authors', [])
    title = paper.get('title', '')
    year = paper.get('year')
    relevance = paper.get('relevance', '')

    # Try author-based classification
    author_tier = get_author_tier(authors)

    # Try title-based classification
    title_tier = get_title_tier(title)

    # Determine final tier
    if author_tier and title_tier:
        # Both agree - high confidence
        if author_tier == title_tier:
            return author_tier, 'author+title', 0.9
        # Prefer more specific (lower tier number = more specific evidence)
        tier = min(author_tier, title_tier)
        return tier, 'author+title_mixed', 0.7
    elif author_tier:
        return author_tier, 'author', 0.8
    elif title_tier:
        return title_tier, 'title', 0.6
    else:
        # Default based on relevance field (from CSV)
        if relevance == 'high':
            return 2, 'default_high', 0.4
        else:
            return 3, 'default', 0.3


def classify_all_papers(dry_run=True):
    """Classify all papers and optionally update the YAML"""
    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    classifications = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    sources = {'existing': 0, 'author': 0, 'title': 0, 'author+title': 0,
               'author+title_mixed': 0, 'default_high': 0, 'default': 0}

    updated = 0
    for paper in data.get('sources', []):
        tier, source, confidence = classify_paper(paper)
        classifications[tier] += 1
        sources[source] += 1

        if paper.get('evidence_tier') is None and tier is not None:
            if not dry_run:
                paper['evidence_tier'] = tier
            updated += 1

    print(f"Classification results:")
    print(f"  Tier 1 (BE causal): {classifications[1]}")
    print(f"  Tier 2 (BE obs/BS exp): {classifications[2]}")
    print(f"  Tier 3 (BS corr): {classifications[3]}")
    print(f"  Tier 4 (Anecdotal): {classifications[4]}")
    print(f"  Tier 5 (Theory): {classifications[5]}")
    print(f"\nClassification sources:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src}: {count}")
    print(f"\nWould update: {updated} papers")

    if not dry_run:
        # Update metadata
        data['metadata']['classification_status'] = 'complete'
        data['metadata']['tier_distribution'] = classifications

        with open(YAML_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"\nUpdated {updated} papers in {YAML_PATH}")

    return data, classifications


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Classify papers by evidence tier')
    parser.add_argument('--dry-run', action='store_true', help='Show classifications without saving')
    parser.add_argument('--apply', action='store_true', help='Apply classifications to YAML')
    args = parser.parse_args()

    if args.apply:
        classify_all_papers(dry_run=False)
    else:
        classify_all_papers(dry_run=True)
