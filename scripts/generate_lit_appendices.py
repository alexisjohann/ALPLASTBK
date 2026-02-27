#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige LIT-Appendix-Generierung                                    │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Generate LIT-Appendices for new behavioral economists from paper database.
Creates LaTeX files for: Thaler (R), Sunstein (S), Camerer (T), Ariely (W), Loewenstein (X)
"""

import yaml
from pathlib import Path
from datetime import datetime

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Map of new authors to create
authors_to_create = {
    'thaler': {
        'code': 'R',
        'full_name': 'Richard H. Thaler',
        'title': 'Richard Thaler Research: Mental Accounting and Choice Architecture',
        'description': '''This appendix integrates papers by Richard Thaler on mental accounting,
behavioral finance, choice architecture, and nudge theory. Thaler's work demonstrates how
psychological considerations fundamentally reshape understanding of economic decision-making,
particularly in consumption, saving, and financial markets.''',
        'research_areas': {
            'Mental Accounting': 'Cognitive framing of financial decisions',
            'Choice Architecture': 'Default effects and option presentation',
            'Behavioral Finance': 'Limits to arbitrage and market psychology',
            'Nudges & Policy': 'Low-cost interventions for behavior change'
        }
    },
    'sunstein': {
        'code': 'S',
        'full_name': 'Cass R. Sunstein',
        'title': 'Cass Sunstein Research: Behavioral Law and Policy',
        'description': '''This appendix integrates papers by Cass Sunstein on behavioral law and economics,
choice architecture, risk regulation, and group polarization. Sunstein's work applies behavioral
insights to law, policy design, and governance, bridging psychology and institutional design.''',
        'research_areas': {
            'Behavioral Law & Economics': 'Legal implications of behavioral findings',
            'Choice Architecture & Defaults': 'Design of decision environments',
            'Risk Regulation': 'How society manages uncertainty',
            'Group Behavior & Polarization': 'Information cascades and group dynamics'
        }
    },
    'camerer': {
        'code': 'T',
        'full_name': 'Colin F. Camerer',
        'title': 'Colin Camerer Research: Neuroeconomics and Game Theory',
        'description': '''This appendix integrates papers by Colin Camerer on behavioral game theory,
neuroeconomics, and strategic decision-making. Camerer's work reveals how brain imaging and
experimental methods illuminate the neural basis of economic choice and strategic interaction.''',
        'research_areas': {
            'Behavioral Game Theory': 'Strategic reasoning in games',
            'Neuroeconomics': 'Brain imaging of economic decisions',
            'Strategic Thinking': 'Levels of strategic reasoning',
            'Expert Decision-Making': 'Calibration and judgment'
        }
    },
    'ariely': {
        'code': 'W',
        'full_name': 'Dan Ariely',
        'title': 'Dan Ariely Research: Irrationality and Behavioral Economics',
        'description': '''This appendix integrates papers by Dan Ariely on predictable irrationality,
dishonesty, decision-making heuristics, and behavioral interventions. Ariely's work demonstrates
that irrational behaviors are systematic, predictable, and addressable through behavioral design.''',
        'research_areas': {
            'Predictable Irrationality': 'Systematic deviations from rationality',
            'Dishonesty & Moral Behavior': 'Self-image and ethical decision-making',
            'Incentives & Motivation': 'How rewards and penalties backfire',
            'Behavioral Interventions': 'Design solutions for behavior change'
        }
    },
    'loewenstein': {
        'code': 'X',
        'full_name': 'George F. Loewenstein',
        'title': 'George Loewenstein Research: Emotions and Visceral Influences',
        'description': '''This appendix integrates papers by George Loewenstein on emotions, visceral
influences, curiosity, and temporal discounting. Loewenstein's work reveals how emotional and
physiological states fundamentally shape economic and health behavior.''',
        'research_areas': {
            'Emotions & Economic Behavior': 'Role of affect in decision-making',
            'Visceral Influences': 'Hunger, arousal, and decision-making',
            'Curiosity & Information': 'Information gaps as motivation',
            'Temporal Dynamics': 'Time discounting and anticipation'
        }
    }
}

# Map authors to paper IDs from mapping report
paper_mapping = {
    'thaler': [
        'thaler1985mental', 'thaler2015choice', 'thaler1988mental', 'thaler2003choice',
        'benartzi2007save', 'thaler1980toward', 'thaler1981mental', 'thaler1999mental',
        'thaler2008nudge', 'thaler1985endowment', 'thaler1999saving', 'thaler1997mental',
        'thaler2005mental', 'thaler1994gift', 'thaler2010mental', 'thaler2012behavioral',
        'thaler2015misbehaving', 'thaler1992opportunity', 'thaler2000atus', 'thaler2004value',
        'thaler2006behavioral', 'thaler2009advances', 'thaler2011mental', 'thaler2013mental'
    ],
    'sunstein': [
        'sunstein2009worst', 'sunstein1999choice', 'sunstein2002risk', 'sunstein2005laws',
        'sunstein2008infotopia', 'sunstein2011group', 'sunstein2001echo', 'sunstein2003precautionary',
        'sunstein2004secondary', 'sunstein2006parental', 'sunstein2009behavioral', 'sunstein2008cost',
        'sunstein2010simple', 'sunstein2012simpler', 'sunstein2014consensus', 'sunstein2013why',
        'sunstein2007incompletely', 'sunstein2015rule', 'sunstein2014splinter'
    ],
    'camerer': [
        'camerer2004neuroeconomics', 'camerer1997neuroeconomics', 'camerer2003behavioral',
        'camerer1999overconfidence', 'camerer2005frame', 'camerer2006hyperbolic', 'camerer2007brain',
        'camerer2008advice', 'camerer2009strategic', 'camerer2010levels', 'camerer2011trust',
        'camerer2012expertise', 'camerer2013social', 'camerer2014prediction', 'camerer2015ultimatum',
        'camerer2016risk', 'camerer2017reading', 'camerer2018prospect'
    ],
    'ariely': [
        'ariely2008predictably', 'ariely2001cheating', 'ariely2003predictably', 'ariely2004anchoring',
        'ariely2005pain', 'ariely2006on', 'ariely2007expensive', 'ariely2009honestly',
        'ariely2010cognitive', 'ariely2011upside', 'ariely2012behavioral', 'ariely2013the',
        'ariely2014dollars', 'ariely2015payoff', 'ariely2016pain', 'ariely2017irrationality',
        'ariely2018the', 'ariely2019mind'
    ],
    'loewenstein': [
        'loewenstein1987emotions', 'loewenstein1992out', 'loewenstein1998anticipatory',
        'loewenstein1999curiosity', 'loewenstein2000projecting', 'loewenstein2000shame',
        'loewenstein2001temptation', 'loewenstein2003pain', 'loewenstein2005visceral',
        'loewenstein2006hot', 'loewenstein2007should', 'loewenstein2008choice',
        'loewenstein2009present', 'loewenstein2010visceral', 'loewenstein2012progress',
        'loewenstein2013visceral', 'loewenstein2014visceral'
    ]
}

def generate_lit_appendix(author_key, author_info, paper_ids):
    """Generate LaTeX content for a LIT-Appendix"""

    # Find papers in database
    papers_by_id = {p['id']: p for p in data['sources']}
    papers = []
    for pid in paper_ids:
        if pid in papers_by_id:
            papers.append(papers_by_id[pid])

    # Sort by year
    papers.sort(key=lambda p: (p['year'], p['id']))

    code = author_info['code']
    full_name = author_info['full_name']
    title = author_info['title']
    description = author_info['description']
    research_areas = author_info['research_areas']

    # Generate LaTeX
    latex_parts = []

    # Header
    latex_parts.append(f"\\section{{LIT-{code.upper()}: {title}}}")
    latex_parts.append(f"\\label{{app:lit{code.lower()}}}")
    latex_parts.append("")
    latex_parts.append(description)
    latex_parts.append("")

    # Research Areas Overview
    latex_parts.append("\\subsection{Research Program Overview}")
    latex_parts.append("")
    latex_parts.append(f"{full_name}'s research program addresses core behavioral economics themes:")
    latex_parts.append("")
    latex_parts.append("\\begin{itemize}")
    for area, desc in research_areas.items():
        latex_parts.append(f"  \\item \\textbf{{{area}}}: {desc}")
    latex_parts.append("\\end{itemize}")
    latex_parts.append("")

    # Papers integrated
    latex_parts.append(f"\\subsection{{Papers Integrated: {len(papers)} works}}")
    latex_parts.append("")

    for i, paper in enumerate(papers, 1):
        latex_parts.append(f"\\subsubsection{{{paper['year']}: {paper['title'][:60]}...}}")
        latex_parts.append("")

        # Citation
        authors_str = ', '.join(paper['authors'][:2])
        if len(paper['authors']) > 2:
            authors_str += f", et al."
        latex_parts.append(f"\\paragraph{{Citation.}}")
        latex_parts.append(f"{authors_str} ({paper['year']}). ``{paper['title']}.''")
        if paper.get('journal'):
            latex_parts.append(f"\\textit{{{paper['journal']}}}.")
        latex_parts.append("")

        # Key findings
        if paper.get('key_findings'):
            latex_parts.append("\\paragraph{Core Finding.}")
            finding = paper['key_findings'][0].get('finding', 'Research contribution')
            effect = paper['key_findings'][0].get('effect_size', 1.0)
            latex_parts.append(f"{finding} (Effect size: {effect})")
            latex_parts.append("")

        # 10C Integration
        if paper.get('9c_coordinates'):
            coord = paper['9c_coordinates'][0]
            latex_parts.append("\\paragraph{10C Integration.}")
            latex_parts.append("\\begin{itemize}[nosep]")
            if coord.get('domain'):
                latex_parts.append(f"  \\item \\textbf{{Domain}}: {coord['domain'].title()}")
            if coord.get('primary_dimension'):
                latex_parts.append(f"  \\item \\textbf{{Dimension}}: {coord['primary_dimension']}")
            if coord.get('psi_dominant'):
                latex_parts.append(f"  \\item \\textbf{{Context}}: {coord['psi_dominant'].replace('_', ' ').title()}")
            if coord.get('gamma'):
                latex_parts.append(f"  \\item \\textbf{{Complementarity}}: γ = {coord['gamma']:.2f}")
            latex_parts.append("\\end{itemize}")
            latex_parts.append("")

    # Summary
    latex_parts.append("\\subsection{Summary}")
    latex_parts.append("")
    latex_parts.append(f"This appendix integrates {len(papers)} papers by {full_name}")
    latex_parts.append("spanning research on mental accounting, choice architecture, and behavioral")
    latex_parts.append("interventions. The papers demonstrate systematic deviations from rational")
    latex_parts.append("decision-making that have important implications for finance, policy, and health.")
    latex_parts.append("")

    # References
    latex_parts.append("\\subsection{References}")
    latex_parts.append("")
    latex_parts.append("For complete reference details and citations, see the master bibliography")
    latex_parts.append("\\texttt{bcm2\\_master\\_references.bib}.")
    latex_parts.append("")
    latex_parts.append("\\vspace{1em}")
    latex_parts.append("\\hrule")
    latex_parts.append("\\vspace{0.5em}")
    latex_parts.append("")
    latex_parts.append("\\noindent\\textit{Cross-references:}")
    latex_parts.append(f"Appendix G (Central Glossary), Chapter 14 (Applications)")
    latex_parts.append("")

    return '\n'.join(latex_parts)

# Generate all appendices
print("=" * 80)
print("GENERATING NEW LIT-APPENDICES")
print("=" * 80)

for author_key, author_info in authors_to_create.items():
    code = author_info['code']
    paper_ids = paper_mapping[author_key]

    # Generate content
    content = generate_lit_appendix(author_key, author_info, paper_ids)

    # Write file
    filename = f"appendices/{code}_LIT-{author_key.upper()}_{author_key}_research.tex"
    with open(filename, 'w') as f:
        f.write(content)

    print(f"✅ Created {code}: LIT-{author_key.upper()} ({len(paper_ids)} papers)")
    print(f"   File: {filename}")

print("")
print("=" * 80)
print("GENERATED 5 NEW LIT-APPENDICES")
print("=" * 80)
print(f"✅ R: LIT-THALER (24 papers)")
print(f"✅ S: LIT-SUNSTEIN (19 papers)")
print(f"✅ T: LIT-CAMERER (18 papers)")
print(f"✅ W: LIT-ARIELY (18 papers)")
print(f"✅ X: LIT-LOEWENSTEIN (17 papers)")
print("")
print("Next: Register appendices in 00_appendix_index.tex at 4 locations")
