#!/usr/bin/env python3
"""
Tag papers with missing CORE-READY, CORE-STAGE, CORE-HIERARCHY in bcm_master.bib.

This script adds 10C dimension tags to the use_for field of papers that are
relevant but not yet tagged. Addresses coverage gaps identified in the
literature overview (2026-02-11).

Usage:
    python scripts/tag_10c_coverage_gaps.py [--dry-run]
"""

import re
import sys
import os

BIB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bibliography', 'bcm_master.bib')

# Papers to tag with CORE-READY (currently 6 papers, target ~20+)
READY_PAPERS = [
    'odonoghue2001choice',        # Procrastination - intent vs action gap
    'akerlof1991procrastination',  # Threshold model of behavioral readiness
    'tirole_benabou_2004_willpower', # Willpower and commitment
    'sunstein2014nudge',           # Choice architecture = readiness engineering
    'prochaska1983stages',         # Stages of change (readiness phases)
    'prochaska1992stages',         # Transtheoretical model
    'mertens2022nudging',          # Nudging meta-analysis, d=0.43
    'lally2010habits',             # Habit formation (66 days to automaticity)
    'chetty2009salience',          # Salience effects on action readiness
    'loewenstein2014visceral',     # Visceral factors affecting readiness
    'chater2022iframe',            # i-frame vs s-frame readiness
    'guentuerkuen2025crowdingout', # Opt-out defaults (readiness mechanism)
    'sunstein2015simplifying',     # Simplification as readiness enabler
    'ajzen1991theory',             # Theory of Planned Behavior (intent→action)
    'bryan2010commitment',         # Commitment devices
    'croson2009',                  # Conditional cooperation & readiness
    'aiagentbehavioralscience2025', # AI agent behavioral readiness
    'norcross2011stages',          # Stages of change review
    'marlatt1985relapse',          # Relapse prevention = readiness maintenance
]

# Papers to tag with CORE-STAGE (currently 12 papers, target ~20+)
STAGE_PAPERS = [
    'prochaska1983stages',         # 5-stage behavior change model
    'prochaska1992stages',         # Transtheoretical model stages
    'norcross2011stages',          # Stages of change review
    'marlatt1985relapse',          # Relapse prevention stages
    'puntoni2021consumers',        # 4-Experience Model with AI
    'aridor2024socialmedia',       # 3-stage content lifecycle
    'heckman2026measuring',        # Stochastic learning stages
    'heckman2025dynamic',          # Dynamic complementarity stages
    'attanasio2026first1000days',  # Developmental stages (first 1000 days)
    'schoegel2024cxnavigator',     # CX Navigator journey framework
    'gans2026oring',               # Sequential adoption stages
    'braghieri2022socialmedia',    # Staggered adoption cohorts
    'gans2025babbage',             # Organizational expansion/refinement phases
    'anarkulova2025lifecycle',     # Lifecycle investment stages
    'lally2010habits',             # Habit formation stages (18-254 days)
    'ajzen1991theory',             # Attitude→intention→behavior stages
]

# Papers to tag with CORE-HIERARCHY (currently 14 papers, target ~25+)
HIERARCHY_PAPERS = [
    'camerer2010levels',           # Levels of thinking (foundational)
    'camerer2004cognitive',        # Cognitive hierarchy model
    'camerer2003behavioral',       # Behavioral game theory
    'nagel_1998_experimental',     # Beauty contest experiments
    'kahneman2011thinking',        # System 1/System 2
    'gabaix2019behavioral',        # Behavioral inattention (attention hierarchy)
    'williamson1975markets',       # Markets vs hierarchies
    'michie2013behavior',          # BCT taxonomy (hierarchical)
    'strotz1956myopia',            # Planner-doer hierarchy
    'stahl1994experimental',       # Hierarchical player models
    'stahl1995players',            # Theory of hierarchical players
    'fehr2003when',                # Norms vs competition hierarchy
    'bosch_nagel_2002_cognitive',  # Cognitive hierarchy beauty contest
    'coricelli_nagel_2009_neural', # Neural hierarchy of reasoning
    'costa_gomes_nagel_2009_reasoning', # Two-person reasoning depth
    'nagel_costa_gomes_2002_mouse', # Mouselab depth of thinking
    'nagel_bosch_1997_one',        # Iterated reasoning levels
    'nagel_buhren_2012_chess',     # Cognitive limits in hierarchical search
    'nagel_2016_survey',           # Survey of cognitive hierarchy
    'nagel_hommes_1999_expectations', # Heterogeneous reasoning horizons
    'camerer1999overconfidence',   # Meta-cognitive hierarchy failure
    'camerer2009strategic',        # Limited strategic thinking
    'camererho1999',               # Learning with levels of sophistication
    'barber2001',                  # Overconfidence (meta-cognitive)
    'lee2023scaling',              # Nonhierarchical scaling
    'tirole_benabou_2004_willpower', # Planner-doer self-control hierarchy
]

# Papers to tag with CORE-EIT (currently 1 paper, target ~15)
EIT_PAPERS = [
    'thaler2015misbehaving',       # Choice architecture, libertarian paternalism
    'sunstein2012simpler',         # Taxonomy of choice architecture tools
    'michie2013behavior',          # 93 BCTs in 16 hierarchical clusters
    'michie2011behaviour',         # COM-B model with intervention functions
    'halpern2015',                 # EAST framework (Easy, Attractive, Social, Timely)
    'milkman2021megastudies',      # Megastudy of 54 interventions
    'hallsworth2017',              # EAST framework application (BIT)
    'johnson2003defaults',         # Default design as intervention mechanism
    'madrian2001power',            # Power of defaults (401k enrollment)
    'dellavigna2020forecasting',   # Forecasting intervention effects
    'dellavigna2022rcts',          # RCTs in behavioral economics
    'benartzi2007save',            # Save More Tomorrow commitment device design
    'beshears2013simplification',  # Simplification as intervention
    'choi2004better',              # Better choices through design
    'allcott2011social',           # Social norm interventions (OPower)
    'dellavigna2018motivates',     # What motivates effort (intervention design)
    'sunstein2014nudge',           # Nudge as intervention framework
    'mertens2022nudging',          # Nudging meta-analysis d=0.43
]

def read_bib(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_bib(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def add_tag_to_use_for(content, bib_key, tag):
    """Add a tag to the use_for field of a specific BibTeX entry."""
    # Find the entry
    pattern = re.compile(
        r'(@\w+\{' + re.escape(bib_key) + r',.*?(?=\n@|\Z))',
        re.DOTALL
    )
    match = pattern.search(content)
    if not match:
        return content, False, 'NOT_FOUND'

    entry = match.group(0)

    # Check if tag already present
    if tag in entry:
        return content, False, 'ALREADY_TAGGED'

    # Find use_for field
    use_for_pattern = re.compile(r'(use_for\s*=\s*\{)([^}]*?)(\})')
    use_for_match = use_for_pattern.search(entry)

    if not use_for_match:
        return content, False, 'NO_USE_FOR'

    # Add tag
    existing_tags = use_for_match.group(2).strip()
    if existing_tags:
        new_tags = existing_tags + ', ' + tag
    else:
        new_tags = tag

    new_entry = entry[:use_for_match.start()] + \
                use_for_match.group(1) + new_tags + use_for_match.group(3) + \
                entry[use_for_match.end():]

    content = content[:match.start()] + new_entry + content[match.end():]
    return content, True, 'ADDED'


def main():
    dry_run = '--dry-run' in sys.argv

    content = read_bib(BIB_PATH)

    all_tags = [
        (READY_PAPERS, 'CORE-READY'),
        (STAGE_PAPERS, 'CORE-STAGE'),
        (HIERARCHY_PAPERS, 'CORE-HIERARCHY'),
        (EIT_PAPERS, 'CORE-EIT'),
    ]

    stats = {'ADDED': 0, 'ALREADY_TAGGED': 0, 'NOT_FOUND': 0, 'NO_USE_FOR': 0}

    for papers, tag in all_tags:
        print(f"\n{'='*60}")
        print(f"  {tag}: {len(papers)} candidates")
        print(f"{'='*60}")

        for key in papers:
            content, changed, status = add_tag_to_use_for(content, key, tag)
            stats[status] += 1

            icon = {'ADDED': '✅', 'ALREADY_TAGGED': '⏭️', 'NOT_FOUND': '❌', 'NO_USE_FOR': '⚠️'}
            print(f"  {icon[status]} {key}: {status}")

    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Added:          {stats['ADDED']}")
    print(f"  Already tagged: {stats['ALREADY_TAGGED']}")
    print(f"  Not found:      {stats['NOT_FOUND']}")
    print(f"  No use_for:     {stats['NO_USE_FOR']}")
    print(f"  Total processed: {sum(stats.values())}")

    if not dry_run and stats['ADDED'] > 0:
        write_bib(BIB_PATH, content)
        print(f"\n  ✅ Written to {BIB_PATH}")
    elif dry_run:
        print(f"\n  🔍 DRY RUN - no changes written")
    else:
        print(f"\n  ℹ️  No changes needed")


if __name__ == '__main__':
    main()
