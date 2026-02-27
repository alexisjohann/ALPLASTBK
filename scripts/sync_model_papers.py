#!/usr/bin/env python3
"""
sync_model_papers.py - Automatische Paper-Synchronisation bei Modell-Speicherung

Wird automatisch ausgeführt wenn ein Modell in model-registry.yaml gespeichert wird.
Stellt sicher, dass alle referenzierten Papers in bcm_master.bib und LIT-Appendices sind.

Workflow:
1. Lese model-registry.yaml
2. Für jedes Modell: Prüfe data_sources.key_papers
3. CHECK: Existiert Paper in bcm_master.bib?
   - JA → Weiter
   - NEIN → Warnung ausgeben (manuell hinzufügen)
4. CHECK: Hat Paper use_for Tag?
   - JA → Weiter
   - NEIN → LIT-Appendix vorschlagen
5. Optional: sync_bib_to_lit.py aufrufen

Usage:
    python scripts/sync_model_papers.py                    # Check all models
    python scripts/sync_model_papers.py --model EBF-MOD-001  # Check specific model
    python scripts/sync_model_papers.py --sync             # Also sync to LIT
    python scripts/sync_model_papers.py --verbose          # Detailed output
"""

import yaml
import re
import os
import sys
import argparse
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
MODEL_REGISTRY = ROOT_DIR / "data" / "model-registry.yaml"
BIB_FILE = ROOT_DIR / "bibliography" / "bcm_master.bib"
SESSION_REGISTRY = ROOT_DIR / "data" / "model-building-session.yaml"


def load_yaml(filepath):
    """Load YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_bib_keys(bib_path):
    """Extract all BibTeX keys from .bib file."""
    keys = set()
    if not bib_path.exists():
        print(f"Warning: BibTeX file not found: {bib_path}")
        return keys

    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Match @type{key,
    pattern = r'@\w+\{([^,]+),'
    matches = re.findall(pattern, content)
    keys = set(m.strip() for m in matches)

    return keys


def get_paper_use_for(bib_path, key):
    """Get use_for field for a specific BibTeX entry."""
    if not bib_path.exists():
        return None

    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find the entry
    pattern = rf'@\w+\{{{key},(.*?)(?=@\w+\{{|\Z)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return None

    entry_content = match.group(1)

    # Find use_for field
    use_for_pattern = r'use_for\s*=\s*\{([^}]+)\}'
    use_for_match = re.search(use_for_pattern, entry_content)

    if use_for_match:
        return use_for_match.group(1).strip()

    return None


def suggest_lit_appendix(paper_key, model_domain="OTH"):
    """Suggest appropriate LIT-Appendix based on paper and model domain."""
    # Domain to LIT mapping
    domain_lit_map = {
        "REL": "LIT-O",      # Religion → Other (no specific LIT)
        "FIN": "LIT-THALER", # Finance → Thaler
        "HLT": "LIT-O",      # Health → Other
        "ENV": "LIT-O",      # Environment → Other
        "POL": "LIT-SUNSTEIN", # Policy → Sunstein
        "ORG": "LIT-FEHR",   # Organization → Fehr
        "EDU": "LIT-O",      # Education → Other
        "OTH": "LIT-O",      # Other → Other
    }

    # Check if paper key contains known author names
    author_lit_map = {
        "kahneman": "LIT-KT",
        "tversky": "LIT-KT",
        "thaler": "LIT-THALER",
        "fehr": "LIT-FEHR",
        "schmidt": "LIT-FEHR",
        "sunstein": "LIT-SUNSTEIN",
        "ariely": "LIT-ARIELY",
        "loewenstein": "LIT-LOEWENSTEIN",
        "camerer": "LIT-CAMERER",
        "rabin": "LIT-RABIN",
    }

    paper_lower = paper_key.lower()
    for author, lit in author_lit_map.items():
        if author in paper_lower:
            return lit

    # Fall back to domain-based suggestion
    return domain_lit_map.get(model_domain, "LIT-O")


def check_model_papers(model, bib_keys, verbose=False):
    """Check papers for a single model."""
    model_id = model.get('id', 'UNKNOWN')
    model_name = model.get('name', 'UNKNOWN')

    results = {
        'model_id': model_id,
        'model_name': model_name,
        'papers_found': [],
        'papers_missing': [],
        'papers_no_lit': [],
        'suggestions': []
    }

    # Get domain from session reference
    session_id = model.get('created_in_session', '')
    domain = "OTH"
    if session_id:
        # Extract domain from session ID: EBF-S-2026-01-25-REL-001 → REL
        parts = session_id.split('-')
        if len(parts) >= 5:
            domain = parts[4]

    # Check data_sources
    data_sources = model.get('data_sources', [])

    for source in data_sources:
        if source.get('type') == 'literature':
            key_papers = source.get('key_papers', [])

            for paper_key in key_papers:
                if paper_key in bib_keys:
                    results['papers_found'].append(paper_key)

                    # Check use_for
                    use_for = get_paper_use_for(BIB_FILE, paper_key)
                    if not use_for:
                        suggested_lit = suggest_lit_appendix(paper_key, domain)
                        results['papers_no_lit'].append(paper_key)
                        results['suggestions'].append({
                            'paper': paper_key,
                            'suggested_lit': suggested_lit,
                            'action': f'Add use_for = {{{suggested_lit}}} to BibTeX entry'
                        })
                else:
                    results['papers_missing'].append(paper_key)
                    results['suggestions'].append({
                        'paper': paper_key,
                        'action': 'Add BibTeX entry to bcm_master.bib'
                    })

    return results


def print_results(results, verbose=False):
    """Print check results."""
    print(f"\n{'='*60}")
    print(f"Model: {results['model_id']} ({results['model_name']})")
    print(f"{'='*60}")

    # Summary
    total = len(results['papers_found']) + len(results['papers_missing'])
    found = len(results['papers_found'])
    missing = len(results['papers_missing'])
    no_lit = len(results['papers_no_lit'])

    print(f"\nPapers: {found}/{total} found in bcm_master.bib")

    if results['papers_found'] and verbose:
        print(f"\n✓ Found ({found}):")
        for p in results['papers_found']:
            print(f"  - {p}")

    if results['papers_missing']:
        print(f"\n✗ Missing ({missing}):")
        for p in results['papers_missing']:
            print(f"  - {p}")

    if results['papers_no_lit']:
        print(f"\n⚠ No LIT-Appendix assigned ({no_lit}):")
        for p in results['papers_no_lit']:
            print(f"  - {p}")

    if results['suggestions']:
        print(f"\n📋 Suggested Actions:")
        for i, s in enumerate(results['suggestions'], 1):
            print(f"  {i}. {s['paper']}: {s['action']}")


def main():
    parser = argparse.ArgumentParser(description='Sync model papers to bcm_master.bib and LIT')
    parser.add_argument('--model', help='Check specific model ID')
    parser.add_argument('--sync', action='store_true', help='Also run sync_bib_to_lit.py')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    # Load data
    if not MODEL_REGISTRY.exists():
        print(f"Error: Model registry not found: {MODEL_REGISTRY}")
        sys.exit(1)

    registry = load_yaml(MODEL_REGISTRY)
    bib_keys = load_bib_keys(BIB_FILE)

    print(f"Loaded {len(bib_keys)} BibTeX keys from bcm_master.bib")

    # Check models
    models = registry.get('models', [])
    all_results = []

    for model in models:
        model_id = model.get('id', '')

        # Filter by model ID if specified
        if args.model and model_id != args.model:
            continue

        results = check_model_papers(model, bib_keys, args.verbose)
        all_results.append(results)
        print_results(results, args.verbose)

    # Summary
    total_missing = sum(len(r['papers_missing']) for r in all_results)
    total_no_lit = sum(len(r['papers_no_lit']) for r in all_results)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Models checked: {len(all_results)}")
    print(f"Papers missing from bcm_master.bib: {total_missing}")
    print(f"Papers without LIT-Appendix: {total_no_lit}")

    if total_missing > 0 or total_no_lit > 0:
        print(f"\n⚠ Action required: Please fix the issues above.")
        if args.sync:
            print("\nSkipping sync due to missing papers.")
        return 1
    else:
        print(f"\n✓ All papers are properly integrated.")

        if args.sync:
            print("\nRunning sync_bib_to_lit.py...")
            sync_script = SCRIPT_DIR / "sync_bib_to_lit.py"
            if sync_script.exists():
                os.system(f"python {sync_script} --update")
            else:
                print(f"Warning: sync_bib_to_lit.py not found")

        return 0


if __name__ == '__main__':
    sys.exit(main())
