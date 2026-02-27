#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige LIT-FALK-Generierung (AE)                                   │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Generate LIT-FALK appendix (AE) with 50 Armin Falk papers
"""

import yaml
from pathlib import Path

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Find all Falk papers
falk_papers = [p for p in data['sources'] if p.get('lit_appendix') == 'AE']
falk_papers.sort(key=lambda p: (p['year'], p['id']))

print(f"Found {len(falk_papers)} Falk papers")

# Generate LaTeX
latex = r"""\section{LIT-AE: Armin Falk Research: Cooperation, Reciprocity, and Fairness}
\label{app:litae}

This appendix integrates papers by Armin Falk on reciprocal fairness, cooperation, and social
preferences. Falk's research program demonstrates that reciprocal fairness—not simple altruism—
is the primary driver of human cooperation, explaining both everyday market behavior and the
evolution of human societies.

\subsection{Research Program Overview}

Armin Falk's research addresses core behavioral economics themes:

\begin{itemize}
  \item \textbf{Reciprocal Fairness}: Preference for fairness and willingness to punish unfairness
  \item \textbf{Cooperation Mechanisms}: How reciprocity sustains cooperation across contexts
  \item \textbf{Fairness in Labor Markets}: How wage fairness influences worker effort
  \item \textbf{Trust and Trustworthiness}: Role of reputation in economic exchange
  \item \textbf{Institutional Effects}: How market institutions shape preferences
  \item \textbf{Group Behavior}: In-group favoritism and identity effects on behavior
  \item \textbf{Norm Enforcement}: How punishment supports cooperative norms
  \item \textbf{Evolution of Cooperation}: How reciprocal preferences evolved to enable groups
\end{itemize}

\subsection{Papers Integrated: """ + str(len(falk_papers)) + r""" works}

"""

for i, paper in enumerate(falk_papers, 1):
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

This appendix integrates """ + str(len(falk_papers)) + r""" papers by Armin Falk spanning research on
cooperation, reciprocity, fairness, labor economics, and institutional design. The papers demonstrate
that reciprocal fairness preferences are fundamental to human cooperation, explain behavior in
markets and organizations, and have important policy implications for institutional design.

Falk's research shows that:
\begin{enumerate}
  \item People reciprocate kindness and punish unkindness, even at personal cost
  \item Fair wages induce higher effort through reciprocal motivation
  \item Market institutions can erode moral concerns and reciprocal preferences
  \item Reputation concerns strengthen reciprocal behavior
  \item Reciprocal fairness preferences evolved to enable large-scale group cooperation
\end{enumerate}

The implications are profound: understanding reciprocal fairness is essential for designing
effective institutions, markets, and policies.

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
filename = "appendices/AE_LIT-AE_falk_research.tex"
with open(filename, 'w') as f:
    f.write(latex)

print(f"✅ Generated LIT-FALK appendix")
print(f"   File: {filename}")
print("")
print("=" * 80)
print("✅ GENERATED LIT-FALK APPENDIX")
print("=" * 80)
print(f"✅ AE: LIT-FALK ({len(falk_papers)} papers)")
print(f"   Cooperation, Reciprocity, Fairness, Labor Economics")
print("")
print("Next: Register LIT-FALK in appendix index (4 locations)")
