#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmalige LIT-MALMENDIER-Generierung (AF)                             │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
"""

⚠️  DEPRECATED (2026-02-08) — See header for details.
Generate LIT-MALMENDIER appendix (AF) with 46 Ulrike Malmendier papers
"""

import yaml
from pathlib import Path

# Load paper database
paper_path = Path("data/paper-sources.yaml")
with open(paper_path, 'r') as f:
    data = yaml.safe_load(f)

# Find all Malmendier papers
malmendier_papers = [p for p in data['sources'] if p.get('lit_appendix') == 'AF']
malmendier_papers.sort(key=lambda p: (p['year'], p['id']))

print(f"Found {len(malmendier_papers)} Malmendier papers")

# Generate LaTeX
latex = r"""
\section{LIT-AF: Ulrike Malmendier Research: Behavioral Finance and CEO Overconfidence}
\label{app:litaf}

This appendix integrates papers by Ulrike Malmendier on behavioral finance, CEO overconfidence, investor psychology, and neuroeconomics. Malmendier's research demonstrates that systematic behavioral biases in corporate decision-making and investor behavior have significant economic consequences, fundamentally challenging traditional finance theory's assumption of rational actors.

\subsection{Research Program Overview}

Ulrike Malmendier's research addresses core behavioral finance and behavioral economics themes:

\begin{itemize}
  \item \textbf{CEO Overconfidence}: How executive overconfidence drives acquisitions, investment, and firm performance
  \item \textbf{Behavioral Finance}: Psychological biases in investor behavior and market efficiency
  \item \textbf{Experience Effects}: How macroeconomic shocks in formative years shape lifetime risk attitudes
  \item \textbf{Neuroeconomics}: Neural mechanisms underlying financial decision-making
  \item \textbf{Gender in Finance}: Impact of gender on corporate decision-making and outcomes
  \item \textbf{Corporate Investment}: How behavioral factors drive corporate finance decisions
  \item \textbf{Market Dynamics}: Behavioral patterns in asset pricing and market efficiency
  \item \textbf{Policy Implications}: Using behavioral insights for financial regulation and policy design
\end{itemize}

\subsection{Papers Integrated: """ + str(len(malmendier_papers)) + r""" works}

"""

for i, paper in enumerate(malmendier_papers, 1):
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

This appendix integrates """ + str(len(malmendier_papers)) + r""" papers by Ulrike Malmendier spanning research on behavioral finance, CEO overconfidence, investor psychology, and neuroeconomics. Malmendier's work demonstrates that systematic behavioral biases are not anomalies but fundamental features of financial decision-making by both corporate executives and individual investors.

Key findings from Malmendier's research:

\begin{enumerate}
  \item CEO overconfidence systematically drives acquisitions, investment, and firm underperformance
  \item Macroeconomic shocks in formative years permanently affect lifetime risk attitudes
  \item Behavioral anomalies in investor behavior have persistent economic consequences
  \item Gender and personality traits significantly influence corporate financial decisions
  \item Market institutions and incentive structures amplify behavioral biases
  \item Behavioral factors explain significant variation in asset pricing and market efficiency
  \item Policy design can account for and mitigate systematic behavioral biases in finance
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
filename = "appendices/AF_LIT-AF_malmendier_research.tex"
with open(filename, 'w') as f:
    f.write(latex)

print(f"✅ Generated LIT-MALMENDIER appendix")
print(f"   File: {filename}")
print("")
print("=" * 80)
print("✅ GENERATED LIT-MALMENDIER APPENDIX")
print("=" * 80)
print(f"✅ AF: LIT-MALMENDIER ({len(malmendier_papers)} papers)")
print(f"   Behavioral Finance, CEO Overconfidence, Investor Psychology, Neuroeconomics")
print("")
print("Next: Register LIT-MALMENDIER in appendix index (4 locations)")
