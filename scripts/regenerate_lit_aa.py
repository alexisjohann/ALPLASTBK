#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige LIT-AA-Regenerierung                                        │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Regenerate LIT-AA appendix with expanded Mullainathan papers
"""

import yaml
from pathlib import Path

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Find all Mullainathan papers
mullainathan_papers = [p for p in data['sources'] if p.get('lit_appendix') == 'AA']
mullainathan_papers.sort(key=lambda p: (p['year'], p['id']))

print(f"Found {len(mullainathan_papers)} Mullainathan papers")

# Generate LaTeX
latex = r"""
\section{LIT-AA: Sendhil Mullainathan Research: Scarcity, Behavioral Policy, and Poverty}
\label{app:litaa}

This appendix integrates papers by Sendhil Mullainathan on scarcity, behavioral policy, poverty economics, and decision-making under constraints. Mullainathan's research demonstrates that resource scarcity creates a cognitive tax that reduces bandwidth for other decisions, fundamentally explaining poverty dynamics and enabling behavioral policy solutions.

\subsection{Research Program Overview}

Sendhil Mullainathan's research addresses core behavioral economics and policy themes:

\begin{itemize}
  \item \textbf{Scarcity and Bandwidth}: How resource scarcity captures cognitive attention, reducing capacity for other decisions
  \item \textbf{Poverty Dynamics}: Behavioral mechanisms explaining persistence and transmission of poverty
  \item \textbf{Behavioral Policy Design}: Using behavioral insights to design effective interventions for resource-scarce populations
  \item \textbf{Financial Decision-Making}: How scarcity affects credit, debt, and savings behavior
  \item \textbf{Intertemporal Choice}: Present bias and time inconsistency under scarcity
  \item \textbf{Attention and Salience}: How scarcity reshapes attention allocation and decision focus
  \item \textbf{Health and Education}: Applying scarcity framework to health behavior and educational decisions
  \item \textbf{Policy Evaluation}: Evidence-based behavioral approaches to poverty reduction
\end{itemize}

\subsection{Papers Integrated: """ + str(len(mullainathan_papers)) + r""" works}

"""

for i, paper in enumerate(mullainathan_papers, 1):
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

This appendix integrates """ + str(len(mullainathan_papers)) + r""" papers by Sendhil Mullainathan spanning research on scarcity, poverty, behavioral policy, and decision-making under constraints. Mullainathan's work demonstrates that understanding how scarcity affects cognitive capacity is fundamental to designing effective interventions for poverty reduction and economic policy.

Key findings from Mullainathan's research:

\begin{enumerate}
  \item Scarcity captures cognitive attention, reducing bandwidth for other decisions
  \item Cognitive bandwidth constraints create self-perpetuating poverty cycles
  \item Present bias and time inconsistency are exacerbated under scarcity
  \item Mental accounting and framing effects are amplified when resources are limited
  \item Simple behavioral interventions can overcome scarcity-induced decision barriers
  \item Attention and salience reshape financial decisions in resource-scarce environments
  \item Policy design accounting for bandwidth constraints dramatically improves effectiveness
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
filename = "appendices/AA_LIT-AA_mullainathan_research.tex"
with open(filename, 'w') as f:
    f.write(latex)

print(f"✅ Regenerated LIT-AA appendix")
print(f"   File: {filename}")
print("")
print("=" * 80)
print("✅ REGENERATED LIT-AA APPENDIX")
print("=" * 80)
print(f"✅ AA: LIT-MULLAINATHAN ({len(mullainathan_papers)} papers)")
print(f"   Scarcity, Behavioral Policy, Poverty, Decision-Making Under Constraints")
print("")
print("Next: Generate LIT-AG appendix")
