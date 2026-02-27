#!/usr/bin/env python3
"""
Paper Compose Helper — Registry Data Extraction for Paper Writing
=================================================================

Extracts structured data from EBF registries for the /generate-paper COMPOSE mode.
Provides Claude with a consolidated data bundle for section-by-section paper composition.

Usage:
    python paper_compose_helper.py --model MOD-PSF-2.0
    python paper_compose_helper.py --session EBF-S-2026-02-14-POL-001
    python paper_compose_helper.py --model MOD-PSF-2.0 --section results
    python paper_compose_helper.py --model MOD-PSF-2.0 --format json

Output:
    Structured YAML/JSON with all registry data needed for paper composition.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Warning: PyYAML not installed. Using basic YAML parsing.")
    yaml = None


def load_yaml(filepath):
    """Load a YAML file, with fallback for missing PyYAML or parse errors."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        if yaml:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"Warning: YAML parse error in {filepath}: {e}", file=sys.stderr)
                # Fallback: try loading raw content for manual extraction
                f.seek(0)
                return {'_raw': f.read(), '_parse_error': str(e)}
        else:
            return {'_raw': f.read(), '_note': 'PyYAML not available, raw content loaded'}


def find_model_in_registry(registry_data, model_id):
    """Find a model entry in model-registry.yaml by ID."""
    if not registry_data or 'models' not in registry_data:
        return None
    for model in registry_data['models']:
        if model.get('id') == model_id:
            return model
    return None


def find_session_in_registry(session_data, session_id=None, model_id=None):
    """Find a session entry by session_id or by model_id link."""
    if not session_data:
        return None

    # Normal parsed YAML path
    if 'sessions' in session_data:
        for session in session_data['sessions']:
            if session_id and session.get('session_id') == session_id:
                return session
            if model_id and session.get('model_id') == model_id:
                return session
        return None

    # Fallback for YAML parse errors: search raw content
    if '_raw' in session_data:
        raw = session_data['_raw']
        search_term = session_id or model_id
        if search_term and search_term in raw:
            # Extract basic info around the match
            idx = raw.find(search_term)
            # Get surrounding context (2000 chars)
            start = max(0, raw.rfind('\n- ', 0, idx))
            end = raw.find('\n- ', idx + len(search_term))
            if end == -1:
                end = min(len(raw), idx + 2000)
            snippet = raw[start:end]
            return {
                '_raw_match': True,
                '_snippet': snippet,
                'session_id': session_id,
                'model_id': model_id
            }
    return None


def find_parameters_for_model(param_data, model_id):
    """Find all parameters linked to a model."""
    if not param_data:
        return []
    params = []
    # Search ALL sections ending in _parameters (dynamic discovery)
    for section_key, section in param_data.items():
        if not section_key.endswith('_parameters'):
            continue
        if not isinstance(section, list):
            continue
        for param in section:
            if not isinstance(param, dict):
                continue
            if param.get('source_model') == model_id:
                params.append(param)
    return params


def find_output_for_model(output_data, model_id=None, session_id=None):
    """Find output entries linked to a model or session."""
    if not output_data:
        return []

    # Normal parsed YAML path
    if 'outputs' in output_data:
        results = []
        for output in output_data['outputs']:
            if model_id and output.get('model_id') == model_id:
                results.append(output)
            elif session_id and output.get('session_id') == session_id:
                results.append(output)
        return results

    # Fallback for YAML parse errors
    if '_raw' in output_data:
        raw = output_data['_raw']
        search_term = model_id or session_id
        if search_term and search_term in raw:
            return [{'_raw_match': True, 'model_id': model_id, 'session_id': session_id}]
    return []


def find_bibliography_entries(bib_path, model_id=None, session_ref=None, theory_support=None):
    """Find BibTeX entries related to a model via session_ref or theory_support."""
    if not os.path.exists(bib_path):
        return []

    entries = []
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into entries
    entry_pattern = re.compile(r'@\w+\{([^,]+),([^@]*?)(?=\n@|\Z)', re.DOTALL)
    for match in entry_pattern.finditer(content):
        key = match.group(1).strip()
        body = match.group(2)

        # Check if entry references our model/session
        relevant = False
        if session_ref and session_ref in body:
            relevant = True
        if model_id and model_id in body:
            relevant = True
        # Also check short model name (e.g., PSF-2.0 from MOD-PSF-2.0)
        if model_id and model_id.startswith('MOD-'):
            short_name = model_id[4:]  # Remove MOD- prefix
            if short_name in body:
                relevant = True
        if theory_support:
            for ts in theory_support:
                if ts in body:
                    relevant = True
                    break

        if relevant:
            # Extract key fields
            entry = {'key': key}
            for field in ['title', 'author', 'year', 'journal', 'use_for',
                         'theory_support', 'evidence_tier', 'session_ref',
                         'model_support', 'keywords']:
                field_match = re.search(rf'{field}\s*=\s*\{{([^}}]*)\}}', body)
                if field_match:
                    entry[field] = field_match.group(1).strip()
            entries.append(entry)

    return entries


def extract_compose_data(model_id=None, session_id=None, section=None):
    """Extract all registry data needed for paper composition."""
    repo_root = Path(__file__).parent.parent

    # Load registries
    model_reg = load_yaml(repo_root / 'data' / 'model-registry.yaml')
    session_reg = load_yaml(repo_root / 'data' / 'model-building-session.yaml')
    param_reg = load_yaml(repo_root / 'data' / 'parameter-registry.yaml')
    output_reg = load_yaml(repo_root / 'data' / 'output-registry.yaml')
    bib_path = repo_root / 'bibliography' / 'bcm_master.bib'

    result = {
        'status': 'ok',
        'model_id': model_id,
        'session_id': session_id,
    }

    # 1. Find model
    model = None
    if model_id:
        model = find_model_in_registry(model_reg, model_id)
        if not model:
            result['status'] = 'error'
            result['error'] = f'Model {model_id} not found in model-registry.yaml'
            return result
        result['model'] = model

    # 2. Find session
    session = find_session_in_registry(session_reg, session_id, model_id)
    if session:
        result['session'] = session
        if not session_id:
            session_id = session.get('session_id')
            result['session_id'] = session_id

    # 3. Find parameters
    if model_id:
        params = find_parameters_for_model(param_reg, model_id)
        result['parameters'] = params
        result['parameter_count'] = len(params)

    # 4. Find outputs
    outputs = find_output_for_model(output_reg, model_id, session_id)
    result['outputs'] = outputs

    # 5. Find bibliography entries
    theory_support = []
    if model and 'theoretical_basis' in model:
        theory_support = [t.get('theory_id', '') for t in model['theoretical_basis']
                         if isinstance(t, dict)]
    bib_entries = find_bibliography_entries(
        str(bib_path),
        model_id=model_id,
        session_ref=session_id,
        theory_support=theory_support
    )
    result['bibliography'] = bib_entries
    result['bibliography_count'] = len(bib_entries)

    # 6. Find model directory
    if model_id:
        # Check for model directory in models/
        models_dir = repo_root / 'models'
        if models_dir.exists():
            for d in models_dir.iterdir():
                if d.is_dir() and model_id.replace('MOD-', '').replace('.', '-') in d.name.upper():
                    result['model_directory'] = str(d.relative_to(repo_root))
                    # Check for README
                    readme = d / 'README.md'
                    if readme.exists():
                        result['has_readme'] = True
                    # List files
                    result['model_files'] = [
                        str(f.relative_to(repo_root))
                        for f in sorted(d.iterdir())
                        if f.is_file() and not f.name.startswith('.')
                    ]
                    break

    # 7. Find appendix files
    if model and 'appendix_refs' in model:
        appendix_files = []
        appendices_dir = repo_root / 'appendices'
        for ref in model['appendix_refs']:
            code = ref.get('code', '') if isinstance(ref, dict) else str(ref)
            # Search for appendix file matching code
            for f in appendices_dir.glob(f'{code}_*.tex'):
                appendix_files.append(str(f.relative_to(repo_root)))
            for f in appendices_dir.glob(f'*_{code}_*.tex'):
                appendix_files.append(str(f.relative_to(repo_root)))
        result['appendix_files'] = appendix_files

    # Section-specific filtering
    if section:
        result = filter_for_section(result, section)

    # Summary
    result['summary'] = {
        'model_found': model is not None,
        'session_found': session is not None,
        'parameters': result.get('parameter_count', 0),
        'bibliography_entries': result.get('bibliography_count', 0),
        'outputs': len(outputs),
        'model_files': len(result.get('model_files', [])),
        'appendix_files': len(result.get('appendix_files', [])),
    }

    return result


def filter_for_section(data, section):
    """Filter extracted data for a specific paper section."""
    section = section.lower()

    if section == 'abstract':
        return {
            'section': 'abstract',
            'key_findings': data.get('outputs', [{}])[0].get('content_summary', {}).get('key_findings', []) if data.get('outputs') else [],
            'question': data.get('session', {}).get('question', ''),
            'model_id': data.get('model_id'),
        }
    elif section == 'introduction':
        return {
            'section': 'introduction',
            'question': data.get('session', {}).get('question', ''),
            'domain': data.get('session', {}).get('domain', ''),
            'bibliography': data.get('bibliography', [])[:10],
        }
    elif section == 'model':
        return {
            'section': 'model',
            'model': data.get('model', {}),
            'parameters': data.get('parameters', []),
            'appendix_files': data.get('appendix_files', []),
        }
    elif section == 'results':
        model = data.get('model', {})
        return {
            'section': 'results',
            'calibration': model.get('calibration', {}),
            'validation': data.get('session', {}).get('validation', {}),
            'key_findings': data.get('outputs', [{}])[0].get('content_summary', {}).get('key_findings', []) if data.get('outputs') else [],
        }
    elif section == 'discussion':
        return {
            'section': 'discussion',
            'learnings': data.get('session', {}).get('learnings', []),
            'bibliography': data.get('bibliography', []),
        }
    else:
        return data


def format_output(data, fmt='yaml'):
    """Format output as YAML or JSON."""
    if fmt == 'json':
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)
    elif yaml:
        return yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    else:
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Extract registry data for paper composition'
    )
    parser.add_argument('--model', '-m', help='Model ID (e.g., MOD-PSF-2.0)')
    parser.add_argument('--session', '-s', help='Session ID (e.g., EBF-S-2026-02-14-POL-001)')
    parser.add_argument('--section', help='Filter for specific section (abstract, introduction, model, results, discussion)')
    parser.add_argument('--format', '-f', choices=['yaml', 'json'], default='yaml',
                       help='Output format (default: yaml)')
    parser.add_argument('--summary', action='store_true', help='Show only summary')

    args = parser.parse_args()

    if not args.model and not args.session:
        parser.error('Either --model or --session is required')

    data = extract_compose_data(
        model_id=args.model,
        session_id=args.session,
        section=args.section
    )

    if args.summary:
        data = data.get('summary', data)

    print(format_output(data, args.format))
    return 0


if __name__ == '__main__':
    sys.exit(main())
