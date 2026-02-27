#!/usr/bin/env python3
"""
Paper L1→L2 Auto-Upgrade via Abstract-Parsing

Parses existing abstracts for structural characteristics S1-S6:
- S1 (Research Question): true if abstract exists
- S2 (Methodology): detected via methodology keywords in abstract
- S3 (Sample/Data): detected via sample/data keywords in abstract
- S4 (Findings): detected via findings keywords in abstract
- S5 (Validity): only from explicit mentions
- S6 (Reproducibility): only from explicit mentions

If S1+S2+S3+S4 all detected → upgrade to L2
"""

import os
import re
import yaml
import sys
from pathlib import Path
from datetime import date

PAPER_DIR = Path("data/paper-references")
PAPER_TEXT_DIR = Path("data/paper-texts")
TODAY = date.today().isoformat()

# === KEYWORD PATTERNS ===

METHODOLOGY_KEYWORDS = [
    # Experimental
    r'\bexperiment\w*\b', r'\brandomiz\w+\b', r'\bRCT\b', r'\bfield experiment\b',
    r'\blab(?:oratory)? experiment\b', r'\btreatment\s+(?:group|arm|condition)\b',
    r'\bcontrol\s+group\b', r'\brandomly\s+assign\w*\b',
    # Empirical
    r'\bempirical\w*\b', r'\bregression\b', r'\bestimation\b', r'\bestimate\w*\b',
    r'\bpanel\s+data\b', r'\bcross[- ]section\w*\b', r'\btime[- ]series\b',
    r'\binstrumental\s+variable\b', r'\bdifference[- ]in[- ]difference\w*\b',
    r'\bDiD\b', r'\bdiscontinuity\s+design\b', r'\bpropensity\s+score\b',
    r'\bfixed\s+effect\b', r'\bOLS\b', r'\bIV\b', r'\b2SLS\b', r'\bGMM\b',
    # Theoretical/Model
    r'\bmodel\b', r'\bframework\b', r'\btheor\w+\b', r'\bequilibrium\b',
    r'\boptimiz\w+\b', r'\bsimulat\w+\b', r'\bcalibrat\w+\b',
    # Survey/Qualitative
    r'\bsurvey\b', r'\bquestionnaire\b', r'\binterview\w*\b',
    # Meta
    r'\bmeta[- ]analysis\b', r'\bsystematic\s+review\b', r'\bliterature\s+review\b',
    # Natural experiment
    r'\bnatural\s+experiment\b', r'\bquasi[- ]experiment\w*\b',
    r'\bevent\s+study\b', r'\bexogenous\b',
]

SAMPLE_DATA_KEYWORDS = [
    # Sample size patterns (handles "6,000 households", "about 500 firms")
    r'(?:about|approximately|over|nearly|more than|around)?\s*\d[\d,.\s]*\s*(?:participants|subjects|households|individuals|firms|'
    r'countries|observations|respondents|students|workers|consumers|patients|'
    r'children|adults|people|employees|managers|agents|voters|banks|companies|'
    r'families|municipalities|cities|districts|schools|hospitals|stores|products)',
    # N= pattern
    r'\b[Nn]\s*=\s*[\d,]+', r'\bsample\s+(?:of|size|includes?)\b',
    # Data mentions
    r'\bdata\s+(?:from|set|on|include|consist|contain)\b', r'\bdataset\b',
    r'\bpanel\b', r'\bcensus\b', r'\badministrative\s+data\b',
    r'\bsurvey\s+data\b', r'\bbilling\s+data\b', r'\bfield\s+data\b',
    r'\blongitudinal\b', r'\bcross-country\b', r'\bmicro-?data\b',
    # Geography
    r'\bU\.?S\.?A?\.?\b', r'\bUnited\s+States\b', r'\bEurop\w+\b',
    r'\bChina\b', r'\bIndia\b', r'\bIndonesia\b', r'\bGerman\w*\b',
    r'\bSwitz\w+\b', r'\bSwitzerland\b', r'\bAustri\w+\b',
    r'\bBritish\b', r'\bUK\b', r'\bJapan\b', r'\bAfrica\w*\b',
    r'\bdeveloping\s+countr\w+\b', r'\bOECD\b', r'\bBrazil\b',
    r'\bMexico\b', r'\bFrance\b', r'\bItaly\b', r'\bSpain\b',
    r'\bCanada\b', r'\bAustralia\b', r'\bKorea\b', r'\bIsrael\b',
    r'\bDenmark\b', r'\bSweden\b', r'\bNorway\b', r'\bFinland\b',
    r'\bNetherlands\b', r'\bBelgium\b',
    # Time periods
    r'\b\d{4}\s*[-–]\s*\d{4}\b',  # 1955-1985
    r'\byears?\s+\d{4}\b', r'\bperiod\s+\d{4}\b',
    r'\bfrom\s+\d{4}\b', r'\bbetween\s+\d{4}\b',
]

FINDINGS_KEYWORDS = [
    # Explicit findings verbs
    r'\bfind\s+that\b', r'\bwe\s+(?:find|show|demonstrate|document|provide|establish|report)\b',
    r'\bresults?\s+(?:show|indicate|suggest|demonstrate|confirm|reveal|imply)\b',
    r'\bevidence\s+(?:that|for|of|suggesting)\b',
    r'\bour\s+(?:results|findings|analysis|estimates)\b',
    # Statistical significance
    r'\bsignificant\w*\b', r'\beffect\s+(?:of|on|is)\b',
    r'\bimpact\s+(?:of|on)\b',
    # Quantitative results
    r'\bincreas\w+\b', r'\breduc\w+\b', r'\bdecreas\w+\b',
    r'\bimprov\w+\b', r'\benhance\w+\b', r'\bdiminish\w+\b',
    r'\b\d+\s*(?:percent|%|pp|percentage)\b',
    r'\belasticit\w+\b', r'\bcoefficient\b',
    # Comparative findings
    r'\bhigher\s+than\b', r'\blower\s+than\b', r'\bmore\s+(?:likely|effective|efficient)\b',
    r'\bless\s+(?:likely|effective|efficient)\b',
    r'\boutperform\w*\b', r'\bunderperform\w*\b',
    # Directional findings
    r'\bpositive\w*\s+(?:effect|impact|relationship|correlation)\b',
    r'\bnegative\w*\s+(?:effect|impact|relationship|correlation)\b',
    r'\bcausal\b', r'\brobust\b',
    # Conclusion-style
    r'\bsuggest\w*\s+that\b', r'\bimpl(?:y|ies)\s+that\b',
    r'\bconclude\s+that\b', r'\bcontribut\w+\s+to\b',
    r'\bsupport\w*\s+(?:the|for|this)\b',
]


def detect_keywords(text, patterns):
    """Check if text contains any of the keyword patterns."""
    if not text:
        return False, []
    text_lower = text.lower()
    matches = []
    for pattern in patterns:
        found = re.search(pattern, text_lower, re.IGNORECASE)
        if found:
            matches.append(found.group())
    return len(matches) > 0, matches


def process_paper(filepath, dry_run=True, verbose=False):
    """Process a single paper YAML for L1→L2 upgrade."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        data = yaml.safe_load(content)
    except Exception as e:
        return {'status': 'error', 'file': str(filepath), 'error': str(e)}

    if not data:
        return {'status': 'skip', 'file': str(filepath), 'reason': 'empty'}

    # Check current level
    current_level = None
    if 'prior_score' in data and isinstance(data['prior_score'], dict):
        current_level = data['prior_score'].get('content_level')

    if current_level and current_level != 'L1':
        return {'status': 'skip', 'file': str(filepath), 'reason': f'already {current_level}'}

    # Get abstract
    abstract = data.get('abstract', '')
    if not abstract or len(str(abstract)) < 50:
        return {'status': 'skip', 'file': str(filepath), 'reason': 'no_abstract'}

    abstract = str(abstract)

    # Also check summary.abstract_extended if available
    extended = ''
    if 'summary' in data and isinstance(data['summary'], dict):
        extended = str(data['summary'].get('abstract_extended', ''))
        key_findings = str(data['summary'].get('key_findings', ''))
    else:
        key_findings = ''

    full_text_for_analysis = abstract + ' ' + extended + ' ' + key_findings

    # Detect structural characteristics
    s1 = True  # If we have an abstract, research question is implied
    s2, s2_matches = detect_keywords(full_text_for_analysis, METHODOLOGY_KEYWORDS)
    s3, s3_matches = detect_keywords(full_text_for_analysis, SAMPLE_DATA_KEYWORDS)
    s4, s4_matches = detect_keywords(full_text_for_analysis, FINDINGS_KEYWORDS)
    s5 = False  # Only from explicit validity discussion
    s6 = False  # Only from explicit reproducibility info

    # S3 INFERENCE: If paper has empirical methodology (S2) AND quantitative
    # findings (S4), data must exist even if not explicitly mentioned in abstract.
    # Theoretical papers won't have S4 with numbers, so this is safe.
    s3_inferred = False
    if s2 and s4 and not s3:
        # Check if methodology is empirical (not purely theoretical)
        empirical_methods = [
            r'\bexperiment\w*\b', r'\brandomiz\w+\b', r'\bRCT\b',
            r'\bempirical\w*\b', r'\bregression\b', r'\bestimation\b',
            r'\bestimate\w*\b', r'\bpanel\s+data\b', r'\bsurvey\b',
            r'\bfield\b', r'\bcross[- ]section\b', r'\bDiD\b',
            r'\binstrumental\b', r'\bdiscontinuity\b', r'\bcalibrat\w+\b',
            r'\bsimulat\w+\b',
        ]
        has_empirical, _ = detect_keywords(full_text_for_analysis, empirical_methods)
        if has_empirical:
            s3 = True
            s3_inferred = True
            s3_matches = ['(inferred from S2+S4)']

    can_upgrade = s1 and s2 and s3 and s4

    result = {
        'status': 'upgrade' if can_upgrade else 'partial',
        'file': str(filepath),
        'paper': data.get('paper', os.path.basename(filepath)),
        'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4,
        's2_matches': s2_matches[:3] if verbose else [],
        's3_matches': s3_matches[:3] if verbose else [],
        's4_matches': s4_matches[:3] if verbose else [],
        'missing': [],
    }

    if not s2:
        result['missing'].append('S2_methodology')
    if not s3:
        result['missing'].append('S3_sample_data')
    if not s4:
        result['missing'].append('S4_findings')

    if s3_inferred:
        result['s3_inferred'] = True

    if can_upgrade and not dry_run:
        _apply_upgrade(filepath, content, data, s1, s2, s3, s4, s5, s6)
        result['status'] = 'upgraded'

    return result


def _apply_upgrade(filepath, original_content, data, s1, s2, s3, s4, s5, s6):
    """Apply the L2 upgrade to a paper YAML file using regex replacements."""
    content = original_content

    # 1. Add structural_characteristics before full_text: block
    sc_block = (
        f"structural_characteristics:\n"
        f"  S1_research_question: {'true' if s1 else 'false'}\n"
        f"  S2_methodology: {'true' if s2 else 'false'}\n"
        f"  S3_sample_data: {'true' if s3 else 'false'}\n"
        f"  S4_findings: {'true' if s4 else 'false'}\n"
        f"  S5_validity: {'true' if s5 else 'false'}\n"
        f"  S6_reproducibility: {'true' if s6 else 'false'}\n"
    )

    # Only add if not already present
    if 'structural_characteristics:' not in content:
        if 'full_text:' in content:
            content = content.replace('full_text:', sc_block + 'full_text:', 1)
        elif 'ebf_integration:' in content:
            content = content.replace('ebf_integration:', sc_block + 'ebf_integration:', 1)

    # 2. Fix garbled content_level in full_text block (L1L0L1 → L2)
    content = re.sub(
        r'(full_text:\n(?:  [^\n]+\n)*?  content_level: )L1L0L1',
        r'\g<1>L2',
        content
    )
    # Also handle clean L1 in full_text block
    content = re.sub(
        r'(full_text:\n(?:  [^\n]+\n)*?  content_level: )L1\b',
        r'\g<1>L2',
        content
    )

    # 3. Update prior_score.content_level: L1 → L2
    content = re.sub(
        r'(prior_score:\n(?:  [^\n]+\n)*?  content_level: )L1\b',
        r'\g<1>L2',
        content
    )

    # 4. Update confidence_multiplier: 0.8 → 0.95
    content = re.sub(
        r'(prior_score:\n(?:  [^\n]+\n)*?  confidence_multiplier: )0\.8\b',
        r'\g<1>0.95',
        content
    )

    # 5. Update quality_score: q_C from 0.333 to 0.667, q_total accordingly
    content = re.sub(
        r'(  quality_score:\n    q_C: )0\.333',
        r'\g<1>0.667',
        content
    )
    # Recalculate q_total = 0.5 * q_C + 0.5 * q_I
    # q_I is typically 0.2 for I1, so q_total = 0.5 * 0.667 + 0.5 * 0.2 = 0.433
    content = re.sub(
        r'(    q_total: )0\.267',
        r'\g<1>0.433',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Paper L1→L2 Auto-Upgrade via Abstract-Parsing')
    parser.add_argument('--batch', type=int, default=0, help='Process N papers (0=all)')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Only analyze, dont modify (default)')
    parser.add_argument('--apply', action='store_true', help='Actually apply upgrades')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show keyword matches')
    parser.add_argument('--tier', type=int, default=0, help='Only process papers of this evidence tier')
    parser.add_argument('--stats', action='store_true', help='Show summary statistics only')
    args = parser.parse_args()

    if args.apply:
        args.dry_run = False

    files = sorted(PAPER_DIR.glob('PAP-*.yaml'))
    print(f"Found {len(files)} paper YAMLs")

    if args.batch > 0:
        files = files[:args.batch]
        print(f"Processing batch of {args.batch}")

    results = {'upgrade': 0, 'partial': 0, 'skip': 0, 'error': 0, 'upgraded': 0}
    missing_counts = {'S2_methodology': 0, 'S3_sample_data': 0, 'S4_findings': 0}
    upgrade_list = []
    partial_list = []

    for f in files:
        r = process_paper(f, dry_run=args.dry_run, verbose=args.verbose)
        status = r['status']
        if status in results:
            results[status] += 1

        if status in ('upgrade', 'upgraded'):
            upgrade_list.append(r)
            if not args.stats and args.verbose:
                print(f"  ✅ {r['paper']}: S2={r['s2_matches']}, S3={r['s3_matches']}")
        elif status == 'partial':
            partial_list.append(r)
            for m in r.get('missing', []):
                missing_counts[m] += 1
            if not args.stats and args.verbose:
                print(f"  ⚠️  {r['paper']}: missing {r['missing']}")
        elif status == 'error':
            print(f"  ❌ {r['file']}: {r.get('error', '?')}")

    # Summary
    total_processed = sum(results.values())
    print(f"\n{'='*60}")
    print(f"RESULTS ({total_processed} papers processed)")
    print(f"{'='*60}")
    if args.dry_run:
        print(f"  ✅ Can upgrade to L2:  {results['upgrade']:>5} ({results['upgrade']/max(total_processed,1)*100:.1f}%)")
    else:
        print(f"  ✅ Upgraded to L2:     {results['upgraded']:>5}")
    print(f"  ⚠️  Partial (missing):  {results['partial']:>5} ({results['partial']/max(total_processed,1)*100:.1f}%)")
    print(f"  ⏭️  Skipped:            {results['skip']:>5}")
    print(f"  ❌ Errors:              {results['error']:>5}")

    if results['partial'] > 0:
        print(f"\n  Missing characteristics breakdown:")
        for k, v in sorted(missing_counts.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v} papers")

    if not args.dry_run and results['upgraded'] > 0:
        print(f"\n  📊 {results['upgraded']} papers upgraded L1→L2")

    return results


if __name__ == '__main__':
    main()
