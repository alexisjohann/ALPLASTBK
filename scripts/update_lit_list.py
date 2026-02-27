#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige LIT-LIST-Aktualisierung (AB)                                │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Update LIT-LIST appendix (AB) with all 50 John List papers
"""

import yaml
from pathlib import Path

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Find all List papers
list_papers = [p for p in data['sources'] if p.get('lit_appendix') == 'AB']
list_papers.sort(key=lambda p: (p['year'], p['id']))

print(f"Found {len(list_papers)} List papers")

# Generate LaTeX
latex = r"""\section{LIT-AB: John List Research: Field Experiments and Market Behavior}
\label{app:litab}

This appendix integrates papers by John List on field experiments, market behavior, and allocation
mechanisms. List's research program demonstrates that laboratory behavioral anomalies often vanish
in field settings with real stakes and experienced participants, fundamentally challenging behavioral
economics claims about market efficiency.

\subsection{Research Program Overview}

John List's research addresses core behavioral economics and field experimental themes:

\begin{itemize}
  \item \textbf{Field Experiments}: Testing economic behavior in naturally occurring settings
  \item \textbf{Market Efficiency}: When and why markets eliminate behavioral anomalies
  \item \textbf{Experience Effects}: How experience and stakes affect decision-making
  \item \textbf{Auction Design}: How auction mechanisms affect bidding and efficiency
  \item \textbf{Environmental Valuation}: Field methods for non-market good valuation
  \item \textbf{Charitable Behavior}: Mechanisms to increase giving and pro-social behavior
  \item \textbf{Mechanism Design}: Using field experiments to test institutional design
  \item \textbf{Policy Applications}: Using field evidence for evidence-based policy
\end{itemize}

\subsection{Papers Integrated: """ + str(len(list_papers)) + r""" works}

"""

for i, paper in enumerate(list_papers, 1):
    authors = ', '.join(paper['authors'][:2])
    if len(paper['authors']) > 2:
        authors += ", et al."

    title_short = paper['title'][:50]
    latex += f"""
\\subsubsection{{{paper['year']}: {title_short}...}}

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

latex += r"""
\subsection{Summary}

This appendix integrates """ + str(len(list_papers)) + r""" papers by John List spanning research on
field experiments, market efficiency, environmental valuation, auction design, and policy applications.
List's research demonstrates the power of field experiments to test economic theories in real-world settings
and design effective policies.

Key findings from List's research:
\begin{enumerate}
  \item Behavioral anomalies observed in labs often disappear in field settings
  \item Market experience and real stakes eliminate many behavioral effects
  \item Field experiments provide powerful evidence for policy design
  \item Mechanism design works better when tested in the field
  \item Environmental valuation methods show large disparities
  \item Simple interventions (asking, matching) can significantly increase pro-social behavior
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
filename = "appendices/AB_LIT-AB_list_research.tex"
with open(filename, 'w') as f:
    f.write(latex)

print(f"✅ Updated LIT-LIST appendix")
print(f"   File: {filename}")
print("")
print("=" * 80)
print("✅ UPDATED LIT-LIST APPENDIX")
print("=" * 80)
print(f"✅ AB: LIT-LIST ({len(list_papers)} papers)")
print(f"   Field Experiments, Market Behavior, Policy Applications")
print("")
print("Next: Commit and push to remote")
