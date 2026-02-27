#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige LIT-Appendix-Generierung (Y, Z, AA, AB, AC, AD)             │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Generate 6 new LIT-Appendices: Y, Z, AA, AB, AC, AD
For: Cialdini, Haidt, Mullainathan, List, Dolan, Specialists
"""

import yaml
from pathlib import Path

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Map codes to metadata
lit_metadata = {
    'Y': {
        'name': 'LIT-CIALDINI',
        'full_name': 'Robert Cialdini',
        'title': 'Robert Cialdini Research: Influence and Social Proof',
        'description': '''This appendix integrates papers by Robert Cialdini on social influence,
persuasion, and compliance. Cialdini's work reveals six principles of influence that shape
human behavior in systematic and predictable ways: reciprocity, commitment, social proof,
authority, liking, and scarcity.''',
        'research_areas': {
            'Social Proof': 'How others\' behavior influences our decisions',
            'Reciprocity': 'Obligation to return favors and treatment',
            'Authority': 'Compliance through perceived expertise',
            'Consistency': 'Commitment to previous decisions',
            'Liking': 'Preference for attractive, similar people',
            'Scarcity': 'Value increases when availability decreases'
        }
    },
    'Z': {
        'name': 'LIT-HAIDT',
        'full_name': 'Jonathan Haidt',
        'title': 'Jonathan Haidt Research: Moral Psychology and Polarization',
        'description': '''This appendix integrates papers by Jonathan Haidt on moral judgment,
emotional reasoning, and political polarization. Haidt\'s work demonstrates that moral
judgments are primarily emotional and intuitive, with reasoning following to justify
initial reactions.''',
        'research_areas': {
            'Moral Foundations': 'Five universal principles underlying morality',
            'Emotional Judgment': 'Intuition-first moral decision-making',
            'Group Polarization': 'How groups magnify initial tendencies',
            'Political Division': 'Why good people are divided by politics',
            'Cultural Diversity': 'Moral foundations vary across cultures'
        }
    },
    'AA': {
        'name': 'LIT-MULLAINATHAN',
        'full_name': 'Sendhil Mullainathan',
        'title': 'Sendhil Mullainathan Research: Scarcity and Behavioral Policy',
        'description': '''This appendix integrates papers by Sendhil Mullainathan on scarcity,
bandwidth, and behavioral policy design. Mullainathan\'s work shows how resource scarcity
captures cognitive attention, reducing bandwidth for other decisions and creating a
self-perpetuating cycle of poverty.''',
        'research_areas': {
            'Bandwidth Theory': 'How scarcity limits cognitive resources',
            'Poverty Dynamics': 'Behavioral mechanisms of poverty traps',
            'Policy Implementation': 'Behavioral solutions for policy problems',
            'Attention Allocation': 'How scarcity reshapes decision focus',
            'Economic Inequality': 'Behavioral drivers of economic gaps'
        }
    },
    'AB': {
        'name': 'LIT-LIST',
        'full_name': 'John List',
        'title': 'John List Research: Field Experiments and Market Behavior',
        'description': '''This appendix integrates papers by John List on field experiments,
market anomalies, and real-world behavioral testing. List\'s work uses field experiments
to test whether laboratory behavioral anomalies generalize to naturally occurring markets
and populations.''',
        'research_areas': {
            'Field Experiments': 'Testing behavior in real-world settings',
            'Market Efficiency': 'When markets eliminate behavioral anomalies',
            'Auction Theory': 'Behavioral bidding and information revelation',
            'Learning & Experience': 'How experience shapes market behavior',
            'Generalization': 'Lab results and field evidence reconciliation'
        }
    },
    'AC': {
        'name': 'LIT-DOLAN',
        'full_name': 'Paul Dolan',
        'title': 'Paul Dolan Research: Happiness and Wellbeing Economics',
        'description': '''This appendix integrates papers by Paul Dolan on wellbeing economics,
happiness measurement, and design of experiences. Dolan\'s work demonstrates that
wellbeing can be measured, predicted, and improved through behavioral design.''',
        'research_areas': {
            'Wellbeing Measurement': 'Experience vs. remembered utility',
            'Happiness Economics': 'Beyond GDP: alternative welfare metrics',
            'Experience Design': 'How to structure activities for wellbeing',
            'Policy Implications': 'Using wellbeing in cost-benefit analysis',
            'Health & Wellbeing': 'Behavioral drivers of health outcomes'
        }
    },
    'AD': {
        'name': 'LIT-SPECIALISTS',
        'full_name': 'Behavioral Economics Specialists',
        'title': 'Behavioral Economics Specialists: Cross-Cutting Research',
        'description': '''This appendix integrates papers from specialized behavioral economists
across multiple domains: Statman (behavioral finance), Rabin (game theory), Babcock
(labor economics), DellaVigna (field methods), Shafir (bounded rationality), Koeszegi
(reference dependence), Bowles (evolution), Haley (cross-cultural), Hogarth (judgment),
and Fox (ambiguity).''',
        'research_areas': {
            'Behavioral Finance': 'Investor psychology and market behavior',
            'Game Theory': 'Fairness and strategic interaction',
            'Labor Markets': 'Negotiation, gender, overconfidence',
            'Bounded Rationality': 'Cognitive limits and decision-making',
            'Reference Dependence': 'How expectations shape behavior',
            'Cross-Cultural': 'Variation in economic behavior across cultures',
            'Judgment & Intuition': 'Pattern-based and educated decisions',
            'Ambiguity': 'Uncertainty about probabilities'
        }
    }
}

def generate_lit_appendix(code, metadata):
    """Generate LaTeX content for a LIT-Appendix"""

    # Find papers for this code in database
    papers = [p for p in data['sources'] if p.get('lit_appendix') == code]
    papers.sort(key=lambda p: (p['year'], p['id']))

    name = metadata['name']
    full_name = metadata['full_name']
    title = metadata['title']
    description = metadata['description']
    research_areas = metadata['research_areas']

    # Generate LaTeX
    latex = f"""\\section{{{name}: {title}}}
\\label{{app:lit{code.lower()}}}

{description}

\\subsection{{Research Program Overview}}

{full_name}'s research program addresses core behavioral economics themes:

\\begin{{itemize}}
"""

    for area, desc in research_areas.items():
        latex += f"  \\item \\textbf{{{area}}}: {desc}\n"

    latex += f"""\\end{{itemize}}

\\subsection{{Papers Integrated: {len(papers)} works}}

"""

    for i, paper in enumerate(papers, 1):
        authors = ', '.join(paper['authors'][:2])
        if len(paper['authors']) > 2:
            authors += ", et al."

        title_short = paper['title'][:50]
        latex += f"""\\subsubsection{{{paper['year']}: {title_short}...}}

\\paragraph{{Citation.}}
{authors} ({paper['year']}). ``{paper['title']}.''
"""
        if paper.get('journal'):
            latex += f"\\textit{{{paper['journal']}}}.\n"
        latex += "\n"

        if paper.get('key_findings'):
            finding = paper['key_findings'][0].get('finding', 'Research contribution')
            latex += f"""\\paragraph{{Core Finding.}}
{finding}

"""

        if paper.get('9c_coordinates'):
            coord = paper['9c_coordinates'][0]
            latex += f"""\\paragraph{{10C Integration.}}
\\begin{{itemize}}[nosep]
"""
            if coord.get('domain'):
                latex += f"  \\item \\textbf{{Domain}}: {coord['domain'].replace('_', ' ').title()}\n"
            if coord.get('primary_dimension'):
                latex += f"  \\item \\textbf{{Dimension}}: {coord['primary_dimension']}\n"
            if coord.get('psi_dominant'):
                latex += f"  \\item \\textbf{{Context}}: {coord['psi_dominant'].replace('_', ' ').title()}\n"
            if coord.get('gamma'):
                latex += f"  \\item \\textbf{{Complementarity}}: γ = {coord['gamma']:.2f}\n"
            latex += "\\end{itemize}\n\n"

    latex += f"""\\subsection{{Summary}}

This appendix integrates {len(papers)} papers by {full_name}
spanning research on {', '.join(list(research_areas.keys())[:3]).lower()}.
The papers demonstrate systematic patterns in human behavior that have important
implications for policy, organization, and individual decision-making.

\\subsection{{References}}

For complete reference details and citations, see the master bibliography
\\texttt{{bcm2\\_master\\_references.bib}}.

\\vspace{{1em}}
\\hrule
\\vspace{{0.5em}}

\\noindent\\textit{{Cross-references:}}
Appendix G (Central Glossary), Chapter 14 (Applications)
"""

    return latex

# Generate all 6 appendices
print("=" * 80)
print("GENERATING 6 NEW LIT-APPENDICES")
print("=" * 80)

for code in ['Y', 'Z', 'AA', 'AB', 'AC', 'AD']:
    metadata = lit_metadata[code]
    content = generate_lit_appendix(code, metadata)

    # Write file
    filename = f"appendices/{code}_LIT-{code}_{metadata['name'].split('-')[1].lower()}_research.tex"
    with open(filename, 'w') as f:
        f.write(content)

    paper_count = len([p for p in data['sources'] if p.get('lit_appendix') == code])
    print(f"✅ {code}: {metadata['name']} ({paper_count} papers)")
    print(f"   File: {filename}")

print("")
print("=" * 80)
print("✅ GENERATED 6 NEW LIT-APPENDICES")
print("=" * 80)
print(f"✅ Y: LIT-CIALDINI (8 papers - Influence, Social Proof)")
print(f"✅ Z: LIT-HAIDT (4 papers - Moral Psychology)")
print(f"✅ AA: LIT-MULLAINATHAN (3 papers - Scarcity, Policy)")
print(f"✅ AB: LIT-LIST (5 papers - Field Experiments)")
print(f"✅ AC: LIT-DOLAN (5 papers - Wellbeing Economics)")
print(f"✅ AD: LIT-SPECIALISTS (20 papers - Cross-Cutting)")
print("")
print("Next: Register in appendix index (4 locations)")
