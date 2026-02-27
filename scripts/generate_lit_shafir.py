#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige LIT-SHAFIR-Generierung (AG)                                 │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Generate LIT-SHAFIR appendix (AG) with 22 Eldar Shafir papers
"""

import yaml
from pathlib import Path

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Find all Shafir papers
shafir_papers = [p for p in data['sources'] if p.get('lit_appendix') == 'AG']
shafir_papers.sort(key=lambda p: (p['year'], p['id']))

print(f"Found {len(shafir_papers)} Shafir papers")

# Generate LaTeX
latex = r"""
\section{LIT-AG: Eldar Shafir Research: Decision-Making and Bounded Rationality}
\label{app:litag}

This appendix integrates papers by Eldar Shafir on decision-making, bounded rationality, memory constraints, and the behavioral foundations of poverty. Shafir's research demonstrates that understanding the cognitive limitations and reasoning strategies that people actually use is essential for explaining economic behavior and designing effective interventions.

\subsection{Research Program Overview}

Eldar Shafir's research addresses core behavioral economics and decision-making themes:

\begin{itemize}
  \item \textbf{Bounded Rationality}: Limits on human reasoning and information processing capacity
  \item \textbf{Contingent Reasoning}: How people reason through scenarios and contingencies
  \item \textbf{Memory Constraints}: Role of memory limitations in economic decisions
  \item \textbf{Choice Architecture}: How decision context shapes behavior and outcomes
  \item \textbf{Scarcity and Poverty}: Cognitive effects of resource constraints on decision-making
  \item \textbf{Financial Behavior}: How psychological mechanisms affect credit and savings decisions
  \item \textbf{Reason-Based Choice}: How people justify and explain their decisions
  \item \textbf{Behavioral Interventions}: Designing policies that account for how people actually decide
\end{itemize}

\subsection{Papers Integrated: """ + str(len(shafir_papers)) + r""" works}

"""

for i, paper in enumerate(shafir_papers, 1):
    authors = ', '.join(paper['authors'][:2])
    if len(paper['authors']) > 2:
        authors += ", et al."

    title_short = paper['title'][:50]
    latex += f"""
\\subsubsection{{{paper['year']}: {title_short}...}}

\\paragraph{{Citation.}}
{authors} ({paper['year']}). ``{paper['title']}''"""
    if paper.get('journal'):
        latex += f""". \\textit{{{paper['journal']}}}.
"""
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

latex += r"""
\subsection{Summary}

This appendix integrates """ + str(len(shafir_papers)) + r""" papers by Eldar Shafir spanning research on bounded rationality, decision-making, memory constraints, and behavioral approaches to poverty. Shafir's work demonstrates that understanding how people actually reason and decide is essential for both economic theory and effective policy design.

Key findings from Shafir's research:

\begin{enumerate}
  \item People reason contingently, considering multiple possibilities rather than computing optimal solutions
  \item Memory constraints fundamentally shape financial and household decisions
  \item Choice architecture and framing can overcome reasoning limitations through better design
  \item Scarcity creates cognitive constraints that impair reasoning in resource-poor populations
  \item Reason-based decision-making explains why people seek justifications for choices
  \item Default options and choice architecture have large effects on outcomes
  \item Behavioral interventions designed around actual reasoning processes are more effective
\end{enumerate}

\subsection{References}

For complete reference details and citations, see the master bibliography
\texttt{bcm2\_master\_references.bib}.

\vspace{1em}
\hrule
\vspace{0.5em}

\noindent\textit{Cross-references:}
Appendix G (Central Glossary), Chapter 14 (Applications)
"""

# Write file
filename = "appendices/AG_LIT-AG_shafir_research.tex"
with open(filename, 'w') as f:
    f.write(latex)

print(f"✅ Generated LIT-SHAFIR appendix")
print(f"   File: {filename}")
print("")
print("=" * 80)
print("✅ GENERATED LIT-SHAFIR APPENDIX")
print("=" * 80)
print(f"✅ AG: LIT-SHAFIR ({len(shafir_papers)} papers)")
print(f"   Decision-Making, Bounded Rationality, Memory, Scarcity, Poverty")
print("")
print("Next: Register LIT-SHAFIR in appendix index (4 locations)")
