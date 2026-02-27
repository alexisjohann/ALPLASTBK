#!/usr/bin/env python3
"""
Generate the consolidated literature overview from SSOTs.

Reads:
  - bibliography/bcm_master.bib (BibTeX)
  - data/paper-references/PAP-*.yaml (Paper metadata)

Writes:
  - docs/frameworks/literature-overview.md

Usage:
  python scripts/generate_literature_overview.py          # Generate overview
  python scripts/generate_literature_overview.py --stats   # Print stats only
"""

import re
import os
import sys
import glob
import yaml
from collections import Counter, defaultdict
from datetime import datetime


def parse_bibtex(bib_path):
    """Parse bcm_master.bib and extract all relevant fields."""
    with open(bib_path, 'r', encoding='utf-8') as f:
        bib = f.read()

    entries = []
    # Split into individual entries
    raw_entries = re.findall(r'@(\w+)\{([^,]+),([^@]*?)(?=\n@|\Z)', bib, re.DOTALL)

    for entry_type, key, body in raw_entries:
        entry = {
            'type': entry_type.lower(),
            'key': key.strip(),
        }
        # Extract fields
        for field in ['year', 'journal', 'author', 'title', 'evidence_tier',
                       'use_for', 'theory_support', 'parameter', 'isbn']:
            match = re.search(rf'{field}\s*=\s*\{{([^}}]*)\}}', body, re.IGNORECASE)
            if match:
                entry[field] = match.group(1).strip()
        entries.append(entry)

    return entries


def parse_yamls(yaml_dir):
    """Parse paper YAML files for content_level and integration_level."""
    stats = {
        'content_levels': Counter(),
        'integration_levels': Counter(),
        'total': 0,
        'errors': 0,
    }

    for path in sorted(glob.glob(os.path.join(yaml_dir, 'PAP-*.yaml'))):
        stats['total'] += 1
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if not data:
                stats['errors'] += 1
                continue

            # Content level - check multiple locations
            cl = None
            if 'content_level' in data:
                cl = data['content_level']
            elif 'prior_score' in data and isinstance(data['prior_score'], dict):
                cl = data['prior_score'].get('content_level')
            if cl:
                stats['content_levels'][str(cl)] += 1

            # Integration level - check multiple locations
            il = None
            if 'integration_level' in data:
                il = data['integration_level']
            elif 'prior_score' in data and isinstance(data['prior_score'], dict):
                il = data['prior_score'].get('integration_level')
            if il:
                stats['integration_levels'][str(il)] += 1

        except Exception:
            stats['errors'] += 1

    return stats


def analyze_entries(entries):
    """Compute all statistics from BibTeX entries."""
    stats = {}

    # Entry types
    stats['types'] = Counter(e['type'] for e in entries)
    stats['total'] = len(entries)

    # Years and decades
    years = []
    for e in entries:
        y = e.get('year', '')
        if y.isdigit():
            years.append(int(y))
    stats['years'] = years
    stats['decades'] = Counter((y // 10) * 10 for y in years)
    stats['median_year'] = sorted(years)[len(years) // 2] if years else 0

    # Journals
    stats['journals'] = Counter(
        e.get('journal', '(none)') for e in entries if e.get('journal')
    )

    # Evidence tiers
    stats['tiers'] = Counter(e.get('evidence_tier', 'none') for e in entries)

    # use_for targets
    appendix_counts = Counter()
    lit_counts = Counter()
    core_counts = Counter()
    domain_counts = Counter()
    method_counts = Counter()
    papers_with_use_for = 0

    for e in entries:
        uf = e.get('use_for', '')
        if uf:
            papers_with_use_for += 1
            parts = [p.strip() for p in uf.split(',') if p.strip()]
            for p in parts:
                appendix_counts[p] += 1
                if p.startswith('LIT-'):
                    lit_counts[p] += 1
                elif p.startswith('CORE-'):
                    core_counts[p] += 1
                elif p.startswith('DOMAIN-'):
                    domain_counts[p] += 1
                elif p.startswith('METHOD-'):
                    method_counts[p] += 1

    stats['use_for'] = appendix_counts
    stats['lit'] = lit_counts
    stats['core'] = core_counts
    stats['domain'] = domain_counts
    stats['method'] = method_counts
    stats['papers_with_use_for'] = papers_with_use_for

    # Theory support
    theory_counts = Counter()
    papers_with_theory = 0
    for e in entries:
        ts = e.get('theory_support', '')
        if ts:
            papers_with_theory += 1
            parts = [p.strip() for p in ts.split(',') if p.strip()]
            for p in parts:
                theory_counts[p] += 1
    stats['theories'] = theory_counts
    stats['papers_with_theory'] = papers_with_theory

    # First authors
    first_authors = Counter()
    for e in entries:
        a = e.get('author', '')
        if a:
            first = a.split(' and ')[0].strip()
            if ',' in first:
                last = first.split(',')[0].strip()
            else:
                parts = first.split()
                last = parts[-1] if parts else first
            first_authors[last] += 1
    stats['first_authors'] = first_authors

    # Parameters
    stats['papers_with_parameter'] = sum(1 for e in entries if e.get('parameter'))
    stats['papers_with_isbn'] = sum(1 for e in entries if e.get('isbn'))

    return stats


def make_bar(count, max_count, width=50):
    """Create a text bar chart element."""
    if max_count == 0:
        return ''
    filled = int(count / max_count * width)
    return '\u2588' * max(filled, 1) if count > 0 else '\u2581'


def fmt(n):
    """Format number with Swiss apostrophe for thousands."""
    if n >= 1000:
        return f"{n:,}".replace(',', "'")
    return str(n)


# --- Author → LIT-Appendix mapping ---
AUTHOR_LIT = {
    'Fehr': 'LIT-FEH/FEHR', 'Kahneman': 'LIT-KT', 'Malmendier': 'LIT-MALMENDIER',
    'List': 'LIT-LIST', 'Falk': 'LIT-FALK', 'Bénabou': 'LIT-BENABOU',
    'Card': 'LIT-CARD', 'Aghion': 'LIT-AGHION', 'Goldin': 'LIT-GOLDIN',
    'Becker': 'LIT-BECKER', 'Schelling': 'LIT-SCHELLING', 'Akerlof': 'LIT-AKERLOF',
    'Shafir': 'LIT-SHAFIR', 'Steen': 'LIT-VANDENSTEEN', 'Autor': 'LIT-AUTOR',
    'Thaler': 'LIT-KT', 'Sunstein': 'LIT-SUT', 'Loewenstein': 'LIT-LOEWENSTEIN',
    'Ambühl': '\u2014', 'Camerer': '\u2014', 'Mullainathan': '\u2014',
    'Acemoglu': '\u2014', 'Smith': '\u2014', 'Ariely': '\u2014', 'Roth': '\u2014',
}

AUTHOR_FOCUS = {
    'Fehr': 'Social Preferences, Fairness, Neuro',
    'Kahneman': 'Prospect Theory, Heuristiken',
    'Malmendier': 'Experience Effects, Corporate Finance',
    'List': 'Field Experiments, Methodology',
    'Falk': 'Reciprocity, Global Preferences',
    'Bénabou': 'Motivated Beliefs, Identity',
    'Card': 'Labor Economics, Immigration',
    'Aghion': 'Innovation, Growth',
    'Goldin': 'Gender, Labor History',
    'Becker': 'Household Economics, Human Capital',
    'Camerer': 'Neuroeconomics, Experimental',
    'Schelling': 'Strategy, Focal Points',
    'Akerlof': 'Identity Economics, Market for Lemons',
    'Shafir': 'Scarcity, Decision Making',
    'Steen': 'Strategy, Competition',
    'Autor': 'Labor, Trade, Technology',
    'Mullainathan': 'Scarcity, Machine Learning',
    'Thaler': 'Nudging, Mental Accounting',
    'Acemoglu': 'Institutions, Political Economy',
    'Smith': 'Experimental Markets',
    'Ariely': 'Irrational Behavior',
    'Sunstein': 'Nudging, Regulation',
    'Roth': 'Market Design, Matching',
    'Loewenstein': 'Emotions, Intertemporal Choice',
    'Ambühl': 'Informed Consent, Experiments',
}

# --- Theory ID → Name mapping (top 10) ---
THEORY_NAMES = {
    'MS-SP-004': 'Social Preferences (General)',
    'MS-SP-001': 'Inequity Aversion (Fehr & Schmidt)',
    'MS-SP-002': 'Reciprocity (Rabin)',
    'MS-IB-001': 'Identity Economics (Akerlof & Kranton)',
    'MS-RD-001': 'Prospect Theory (Kahneman & Tversky)',
    'MS-IN-001': 'Inequality (General)',
    'MS-MO-003': 'Motivated Beliefs (Bénabou & Tirole)',
    'MS-BF-001': 'Bounded Rationality',
    'MS-HTE-001': 'Heterogeneous Treatment Effects',
    'MS-LM-001': 'Labor Market Models',
}

# --- 10C CORE mapping ---
CORE_ORDER = [
    ('CORE-HOW', 'B', 'Wie interagieren?'),
    ('CORE-WHO', 'AAA', 'Wer hat Utility?'),
    ('CORE-AWARE', 'AU', 'Wie bewusst?'),
    ('CORE-WHEN', 'V', 'Wann zählt Kontext?'),
    ('CORE-WHAT', 'C', 'Was ist Utility?'),
    ('CORE-WHERE', 'BBB', 'Woher die Zahlen?'),
    ('CORE-INTELLIGENCE', 'HI', 'Wie stratifizieren?'),
    ('CORE-HIERARCHY', 'HI', 'Entscheidungshierarchie?'),
    ('CORE-STAGE', 'AW', 'Wo in der Journey?'),
    ('CORE-READY', 'AV', 'Handlungsbereit?'),
    ('CORE-EIT', 'IE', 'Wie emergieren Interventionen?'),
]


def generate_markdown(bib_stats, yaml_stats):
    """Generate the complete literature-overview.md content."""
    s = bib_stats
    y = yaml_stats
    today = datetime.now().strftime('%Y-%m-%d')
    total = s['total']

    lines = []
    w = lines.append  # shorthand

    # --- Header ---
    w(f'# EBF Literaturüberblick — State of the Literature\n')
    w(f'> **Version:** auto-generated ({today})')
    w(f'> **Status:** Automatisch generiert aus `bcm_master.bib` + {fmt(y["total"])} Paper-YAMLs')
    w(f'> **SSOT:** `bibliography/bcm_master.bib` (BibTeX) + `data/paper-references/PAP-*.yaml` (Metadaten)')
    w(f'> **Script:** `python scripts/generate_literature_overview.py`')
    w('')
    w('---\n')

    # --- Auf einen Blick ---
    tier1 = s['tiers'].get('1', 0)
    tier2 = s['tiers'].get('2', 0)
    tier3 = s['tiers'].get('3', 0)
    tier_other = total - tier1 - tier2 - tier3

    cl0 = y['content_levels'].get('L0', 0)
    cl1 = y['content_levels'].get('L1', 0)
    cl2 = y['content_levels'].get('L2', 0)
    cl3 = y['content_levels'].get('L3', 0)

    il1 = y['integration_levels'].get('I1', 0)
    il2 = y['integration_levels'].get('I2', 0)
    il3 = y['integration_levels'].get('I3', 0)
    il4 = y['integration_levels'].get('I4', 0)
    il5 = y['integration_levels'].get('I5', 0)
    il_na = y['total'] - (il1 + il2 + il3 + il4 + il5)

    w('## Auf einen Blick\n')
    w('```')
    w('┌─────────────────────────────────────────────────────────────────────────┐')
    w('│  EBF PAPER DATABASE — STATE OF THE LITERATURE                           │')
    w(f'│  Stand: {today}{" " * (62 - len(today))}│')
    w('├─────────────────────────────────────────────────────────────────────────┤')
    w('│                                                                         │')
    w(f'│  📚 {fmt(total)} Papers    {len(s["lit"])} LIT-Appendices    153 Theorien    852 Cases{" " * 6}│')
    w('│                                                                         │')
    w('│  QUALITÄTS-PROFIL:                                                      │')
    w(f'│  ├── Evidence Tier 1 (Gold):   {fmt(tier1):>5s} Papers ({tier1*100//total}%){" " * (24 - len(fmt(tier1)))}│')
    w(f'│  ├── Evidence Tier 2 (Silver): {fmt(tier2):>5s} Papers ({tier2*100//total}%){" " * (24 - len(fmt(tier2)))}│')
    w(f'│  ├── Evidence Tier 3 (Bronze): {fmt(tier3):>5s} Papers ({tier3*100//total}%){" " * (24 - len(fmt(tier3)))}│')
    w(f'│  └── Sonstige:                 {fmt(tier_other):>5s} Papers  ({tier_other*100//total}%){" " * (23 - len(fmt(tier_other)))}│')
    w('│                                                                         │')
    w('│  TIEFE-PROFIL:                                                          │')
    w(f'│  ├── Content L0 (Metadata):   {fmt(cl0):>5s} Papers ({cl0*100//total}%){" " * (24 - len(fmt(cl0)))}│')
    w(f'│  ├── Content L1 (Research Q.): {fmt(cl1):>5s} Papers ({cl1*100//total}%){" " * (23 - len(fmt(cl1)))}│')
    w(f'│  ├── Content L2 (Summary):   {fmt(cl2):>5s} Papers ({cl2*100//total}%){" " * (24 - len(fmt(cl2)))}│')
    w(f'│  └── Content L3 (Full Text):  {fmt(cl3):>5s} Papers  ({cl3*100//total}%){" " * (23 - len(fmt(cl3)))}│')
    w('│                                                                         │')
    w('└─────────────────────────────────────────────────────────────────────────┘')
    w('```\n')
    w('---\n')

    # --- 1. Publikationstypen ---
    w('## 1. Publikationstypen\n')
    w('| Typ | Anzahl | Anteil |')
    w('|-----|--------|--------|')
    type_labels = {
        'article': 'article (Peer-reviewed)', 'book': 'book',
        'techreport': 'techreport (Working Papers)', 'incollection': 'incollection (Buchkapitel)',
        'inproceedings': 'inproceedings (Konferenzen)', 'misc': 'misc', 'unpublished': 'unpublished',
    }
    for t, c in s['types'].most_common():
        label = type_labels.get(t, t)
        w(f'| **{label}** | {fmt(c)} | {c*100/total:.1f}% |')
    w(f'| **Total** | **{fmt(total)}** | **100%** |')
    w('')

    # --- 2. Zeitliche Verteilung ---
    w('## 2. Zeitliche Verteilung\n')
    w('```')
    w('Dekade     Papers   Balken')
    w('─────────────────────────────────────────────────────')
    modern_decades = {d: c for d, c in s['decades'].items() if d >= 1950}
    pre_1950 = sum(c for d, c in s['decades'].items() if d < 1950)
    max_d = max(modern_decades.values()) if modern_decades else 1
    if pre_1950 > 0:
        w(f'vor 1950   {pre_1950:>5d}   {make_bar(pre_1950, max_d, 40)}')
    for d in sorted(modern_decades.keys()):
        c = modern_decades[d]
        w(f'{d}er   {c:>5d}   {make_bar(c, max_d, 40)}')
    w('─────────────────────────────────────────────────────')
    w('```\n')

    w(f'**Median-Jahr:** {s["median_year"]}')
    w(f'**Temporal Decay:** τ(p) = 2^(-age/15) mit Halbwertszeit 15 Jahre.\n')
    w('---\n')

    # --- 3. Top Journals ---
    w('## 3. Top-Journals\n')
    w('| # | Journal | Papers | Tier |')
    w('|---|---------|--------|------|')
    tier1_journals = {
        'American Economic Review', 'Quarterly Journal of Economics',
        'Journal of Political Economy', 'Econometrica', 'Review of Economic Studies',
        'Journal of Economic Literature', 'Journal of Economic Perspectives',
        'Journal of the European Economic Association', 'Management Science',
        'Journal of Finance', 'Science', 'Nature',
    }
    for i, (j, c) in enumerate(s['journals'].most_common(16), 1):
        if j in ('null', 'Working Paper', 'Book'):
            continue
        tier = '1' if j in tier1_journals else '2'
        w(f'| {i} | **{j}** | {c} | {tier} |')
    w('')

    top5 = sum(s['journals'].get(j, 0) for j in [
        'American Economic Review', 'Quarterly Journal of Economics',
        'Journal of Political Economy', 'Econometrica', 'Review of Economic Studies'
    ])
    sci_nat = s['journals'].get('Science', 0) + s['journals'].get('Nature', 0)
    w(f'**Top-5 Ökonomie:** AER + QJE + JPE + Econometrica + RES = **{top5} Papers ({top5*100//total}%)**\n')
    w(f'**Interdisziplinär:** Science + Nature = **{sci_nat} Papers**\n')
    w('---\n')

    # --- 4. Evidence Tiers ---
    w('## 4. Evidence Tiers\n')
    w('```')
    max_tier = max(tier1, tier2, tier3)
    w(f'Tier 1 (Gold)    {make_bar(tier1, max_tier, 50)}  {fmt(tier1)} ({tier1*100//total}%)')
    w(f'Tier 2 (Silver)  {make_bar(tier2, max_tier, 50)}  {fmt(tier2)} ({tier2*100//total}%)')
    w(f'Tier 3 (Bronze)  {make_bar(tier3, max_tier, 50)}  {fmt(tier3)} ({tier3*100//total}%)')
    w('```\n')
    w(f'**{(tier1+tier2)*100//total}% der Literatur ist Tier 1 oder 2** — eine starke empirische Basis.\n')
    w('---\n')

    # --- 5. Content Level ---
    w('## 5. Content Level (Strukturelle Tiefe)\n')
    w('Basierend auf den 6 Strukturellen Charakteristika S1-S6:\n')
    w('| Level | Name | Kriterium | Papers | Anteil |')
    w('|-------|------|-----------|--------|--------|')
    w(f'| **L0** | Metadata Only | Kein S₁-S₆ | {fmt(cl0)} | {cl0*100/total:.1f}% |')
    w(f'| **L1** | Research Question | S₁ vorhanden | {fmt(cl1)} | {cl1*100/total:.1f}% |')
    w(f'| **L2** | Summary/Extract | S₁-S₄ vorhanden | {fmt(cl2)} | {cl2*100/total:.1f}% |')
    w(f'| **L3** | Full Text | S₁-S₆ + R1-R4 | {fmt(cl3)} | {cl3*100/total:.1f}% |')
    w('')
    w('```')
    max_cl = max(cl0, cl1, cl2, cl3)
    w(f'L0  {make_bar(cl0, max_cl, 45)}  {fmt(cl0)}')
    w(f'L1  {make_bar(cl1, max_cl, 45)}  {fmt(cl1)}')
    w(f'L2  {make_bar(cl2, max_cl, 45)}  {fmt(cl2)}')
    w(f'L3  {make_bar(cl3, max_cl, 45)}  {fmt(cl3)}')
    w('```\n')
    w('**L3 erfordert R1-R4:** Alle Originalsektionen (R1), Referenzen (R2), >10k Wörter (R3), keine EBF-Sektionen (R4).\n')
    w('---\n')

    # --- 6. Integration Level ---
    w('## 6. Integration Level (EBF-Verknüpfungstiefe)\n')
    w('| Level | Name | Kriterium | Papers | Anteil |')
    w('|-------|------|-----------|--------|--------|')
    w(f'| **I1** | Classified | `use_for` + `evidence_tier` | {fmt(il1)} | {il1*100/total:.1f}% |')
    w(f'| **I2** | Theorized | + `theory_support` (MS-XX-XXX) | {fmt(il2)} | {il2*100/total:.1f}% |')
    w(f'| **I3** | Exemplified | + Case Registry (CAS-XXX) | {fmt(il3)} | {il3*100/total:.1f}% |')
    w(f'| **I4** | Parameterized | + Parameter Registry (PAR-XXX) | {fmt(il4)} | {il4*100/total:.1f}% |')
    w(f'| **I5** | Canonized | + Appendix + Chapter | {fmt(il5)} | {il5*100/total:.1f}% |')
    if il_na > 0:
        w(f'| — | Nicht zugeordnet | — | {fmt(il_na)} | {il_na*100/total:.1f}% |')
    w('')
    w(f'**{s["papers_with_theory"]} Papers ({s["papers_with_theory"]*100//total}%)** haben `theory_support`.')
    w(f'**{s["papers_with_parameter"]} Papers ({s["papers_with_parameter"]*100//total}%)** haben extrahierte Parameter.\n')
    w('---\n')

    # --- 7. Autoren-Cluster ---
    w('## 7. Autoren-Cluster (Top 25 Erstautoren)\n')
    w('| # | Erstautor | Papers | LIT-Appendix | Schwerpunkt |')
    w('|---|-----------|--------|-------------|-------------|')
    for i, (a, c) in enumerate(s['first_authors'].most_common(25), 1):
        lit = AUTHOR_LIT.get(a, '\u2014')
        focus = AUTHOR_FOCUS.get(a, '')
        w(f'| {i} | **{a}** | {c} | {lit} | {focus} |')
    w('')
    w(f'**{len(s["lit"])} LIT-Appendices** decken die Autorenzuordnungen ab. '
      f'Die grösste Kategorie ist **LIT-O** ({fmt(s["lit"].get("LIT-O", 0))} Papers).\n')
    w('---\n')

    # --- 8. Theory Support ---
    w('## 8. Theoretische Verankerung (Theory Support)\n')
    w('Die 10 am häufigsten gestützten Theorien:\n')
    w('| # | Theory ID | Theorie | Papers |')
    w('|---|-----------|---------|--------|')
    for i, (t, c) in enumerate(s['theories'].most_common(10), 1):
        name = THEORY_NAMES.get(t, t)
        w(f'| {i} | **{t}** | {name} | {c} |')
    w('')
    w(f'**{s["papers_with_theory"]} Papers ({s["papers_with_theory"]*100//total}%)** sind explizit mit Theorien verknüpft.\n')
    w('---\n')

    # --- 9. 10C Coverage ---
    w('## 9. 10C-Dimension Coverage\n')
    w('| CORE | Code | Frage | Papers | Abdeckung |')
    w('|------|------|-------|--------|-----------|')
    max_core = max((s['core'].get(k, 0) for k, _, _ in CORE_ORDER), default=1)
    for key, code, question in CORE_ORDER:
        count = s['core'].get(key, 0)
        bar = make_bar(count, max_core, 14)
        if count >= 50:
            label = 'Stark'
        elif count >= 20:
            label = 'Gut'
        elif count >= 10:
            label = 'Dünn'
        else:
            label = 'Sehr dünn'
        w(f'| **{key.replace("CORE-", "")}** | {code} | {question} | {count} | {bar} {label} |')
    w('')
    gaps = [key.replace("CORE-", "") for key, _, _ in CORE_ORDER if s['core'].get(key, 0) < 20]
    if gaps:
        w(f'**Coverage-Gaps:** {", ".join(gaps)} sind unterrepräsentiert.\n')
    else:
        w('**Alle 10C-Dimensionen haben gute Abdeckung (≥20 Papers).**\n')
    w('---\n')

    # --- 10. Domänen ---
    w('## 10. Domänen-Verteilung\n')
    w('| Domäne | Papers | Schwerpunkt |')
    w('|--------|--------|-------------|')
    domain_labels = {
        'DOMAIN-MIGRATION': 'Immigration, Integration, Asyl',
        'DOMAIN-LABOR': 'Arbeitsmarkt, Löhne, Beschäftigung',
        'DOMAIN-POLITICAL': 'Wahlen, Politische Ökonomie',
        'DOMAIN-POLICY': 'Regulierung, Nudging, Public Policy',
        'DOMAIN-HEALTH': 'Gesundheitsverhalten, Prävention',
        'DOMAIN-MONETARY': 'Geldpolitik, Zentralbanken',
        'DOMAIN-FINANCE': 'Finanzmärkte, Behavioral Finance',
        'DOMAIN-EDUCATION': 'Bildung, Skill Formation',
        'DOMAIN-PUBLIC': 'Öffentliche Güter, Kooperation',
        'DOMAIN-INTEGRATION': 'Soziale Integration',
        'DOMAIN-ORG': 'Organisationsverhalten',
        'DOMAIN-DEVELOPMENT': 'Entwicklungsökonomie',
        'DOMAIN-PLATFORM': 'Digitale Plattformen',
        'DOMAIN-ENV': 'Umwelt, Energie',
    }
    for d, c in s['domain'].most_common(14):
        label = domain_labels.get(d, '')
        w(f'| **{d}** | {c} | {label} |')
    w('')
    w('---\n')

    # --- 11. Parameter ---
    w('## 11. Parameter-Extraktion\n')
    w('| Metrik | Wert |')
    w('|--------|------|')
    w(f'| Papers mit `parameter`-Feld | {fmt(s["papers_with_parameter"])} ({s["papers_with_parameter"]*100//total}%) |')
    w(f'| Papers mit `theory_support` | {fmt(s["papers_with_theory"])} ({s["papers_with_theory"]*100//total}%) |')
    w(f'| Papers mit ISBN | {s["papers_with_isbn"]} ({s["papers_with_isbn"]*100//total}%) |')
    w(f'| Papers mit `use_for` | {fmt(s["papers_with_use_for"])} ({s["papers_with_use_for"]*100//total}%) |')
    w('')
    w('---\n')

    # --- 12. Verwandte Dokumente ---
    w('## 12. Verwandte Dokumente\n')
    w('| Priorität | Dokument | Inhalt |')
    w('|-----------|----------|--------|')
    w('| **SSOT** | `appendices/BM_METHOD-PAPERINT_*.tex` | Formale Definitionen (Axiome, Beweise) |')
    w('| **Prozess** | `docs/workflows/paper-workflow-overview.md` | Paper-Lifecycle, Skills, Architektur |')
    w('| **Qualität** | `docs/frameworks/paper-database-quality-dimensions.md` | 2D-System (C × I), S1-S6, R1-R4 |')
    w('| **Schemas** | `docs/frameworks/database-schemas-overview.md` | 5-Datenbank-Architektur |')
    w('| **Dieser** | `docs/frameworks/literature-overview.md` | Konsolidierter Gesamtüberblick |')
    w('')
    w('---\n')

    # --- 13. Aktualisierung ---
    w('## 13. Aktualisierung\n')
    w('Dieses Dokument wird automatisch generiert:\n')
    w('```bash')
    w('python scripts/generate_literature_overview.py')
    w('```\n')
    w(f'*Generiert: {today} | Datenstand: bcm_master.bib v{total} + {fmt(y["total"])} Paper-YAMLs*')

    return '\n'.join(lines)


def print_stats(bib_stats, yaml_stats):
    """Print stats to stdout without generating file."""
    s = bib_stats
    y = yaml_stats
    total = s['total']

    print(f"\n{'='*60}")
    print(f"  EBF LITERATURE STATISTICS")
    print(f"{'='*60}")
    print(f"  Total papers (BibTeX): {fmt(total)}")
    print(f"  Total papers (YAML):   {fmt(y['total'])}")
    print(f"  YAML parse errors:     {y['errors']}")
    print(f"\n  Content Levels:")
    for lv in ['L0', 'L1', 'L2', 'L3']:
        print(f"    {lv}: {y['content_levels'].get(lv, 0)}")
    print(f"\n  Integration Levels:")
    for lv in ['I1', 'I2', 'I3', 'I4', 'I5']:
        print(f"    {lv}: {y['integration_levels'].get(lv, 0)}")
    print(f"\n  Evidence Tiers:")
    for t in ['1', '2', '3']:
        print(f"    Tier {t}: {s['tiers'].get(t, 0)}")
    print(f"\n  Median year: {s['median_year']}")
    print(f"  With theory_support: {s['papers_with_theory']}")
    print(f"  With parameter: {s['papers_with_parameter']}")
    print(f"  With use_for: {s['papers_with_use_for']}")
    print(f"  With ISBN: {s['papers_with_isbn']}")
    print(f"{'='*60}\n")


def main():
    bib_path = 'bibliography/bcm_master.bib'
    yaml_dir = 'data/paper-references'
    output_path = 'docs/frameworks/literature-overview.md'

    if not os.path.exists(bib_path):
        print(f"ERROR: {bib_path} not found. Run from repo root.")
        sys.exit(1)

    print("Parsing BibTeX...", end=' ', flush=True)
    entries = parse_bibtex(bib_path)
    print(f"{len(entries)} entries")

    print("Analyzing BibTeX...", end=' ', flush=True)
    bib_stats = analyze_entries(entries)
    print("done")

    print("Parsing Paper YAMLs...", end=' ', flush=True)
    yaml_stats = parse_yamls(yaml_dir)
    print(f"{yaml_stats['total']} files ({yaml_stats['errors']} errors)")

    if '--stats' in sys.argv:
        print_stats(bib_stats, yaml_stats)
        return

    print(f"Generating {output_path}...", end=' ', flush=True)
    md = generate_markdown(bib_stats, yaml_stats)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print("done")

    print(f"\n✅ Literature overview written to {output_path}")
    print_stats(bib_stats, yaml_stats)


if __name__ == '__main__':
    main()
