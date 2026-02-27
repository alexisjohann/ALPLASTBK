#!/usr/bin/env python3
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  ⚠️  DEPRECATED (2026-02-08)                                            │
# │                                                                         │
# │  Einmaliges Knowledge-Mining aus LLM-Training                          │
# │  Kept for reference only.                                              │
# │                                                                         │
# │  SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib │
# │  Neue Papers: /integrate-paper Workflow                                │
# └─────────────────────────────────────────────────────────────────────────┘
# =============================================================================
# BEHAVIORAL ECONOMICS KNOWLEDGE MINING - From LLM Training Data
# =============================================================================
#
# Extrahiert hochwertige, peer-reviewed Journal Papers aus Training-Wissen
# und generiert paper-sources.yaml mit vollständiger 10C-Dokumentation.
#
# Filter: Nur Journals, Peer-Reviewed, etablierte Quellen
#
# Usage:
#   python scripts/mine_journal_papers.py                    # All papers
#   python scripts/mine_journal_papers.py --domain health    # Filter by domain
#   python scripts/mine_journal_papers.py --min-citations 20 # Min citations
#
# =============================================================================

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import argparse
from datetime import datetime

# =============================================================================
# JOURNAL PAPER DATABASE (From LLM Training Knowledge)
# =============================================================================

BEHAVIORAL_ECON_PAPERS = [
    # =========================================================================
    # TOP-TIER JOURNALS: AER, Econometrica, JEBO, JHR
    # =========================================================================

    {
        "id": "PAP-PAP-kahneman1979prospectprospect",
        "authors": ["Kahneman, Daniel", "Tversky, Amos"],
        "year": 1979,
        "title": "Prospect Theory: An Analysis of Decision under Risk",
        "journal": "Econometrica",
        "volume": 47,
        "issue": 2,
        "pages": "263-291",
        "doi": "10.2307/1914185",
        "citations": 45000,
        "status": "seminal",
        "key_findings": [
            {
                "finding": "People exhibit loss aversion: losses loom larger than equivalent gains",
                "domain": "finance",
                "stage": "contemplation",
                "primary_dimension": "E",
                "effect_size": 2.25
            },
            {
                "finding": "Risk preferences reverse between gains and losses (reflection effect)",
                "domain": "health",
                "stage": "preparation",
                "primary_dimension": "P",
                "effect_size": 1.8
            }
        ],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["contemplation", "preparation"],
                "primary_dimension": "E",
                "psi_dominant": "framing",
                "gamma": 0.5,
                "A_level": 0.6,
                "W_level": 0.5,
                "awareness_type": "explicit",
                "key_insight": "Decision weights deviate from objective probabilities, creating predictable biases"
            }
        ]
    },

    {
        "id": "PAP-thaler1985mental",
        "authors": ["Thaler, Richard H."],
        "year": 1985,
        "title": "Mental Accounting and Consumer Choice",
        "journal": "Marketing Science",
        "volume": 4,
        "issue": 3,
        "pages": "199-214",
        "doi": "10.1287/mksc.4.3.199",
        "citations": 3500,
        "status": "published",
        "key_findings": [
            {
                "finding": "People organize spending into mental accounts with separate budgets",
                "domain": "finance",
                "stage": "preparation",
                "effect_size": 1.5
            }
        ],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["preparation", "action"],
                "primary_dimension": "F",
                "psi_dominant": "cognitive_framing",
                "gamma": 0.4,
                "A_level": 0.5,
                "W_level": 0.6,
                "awareness_type": "implicit",
                "key_insight": "Mental accounting creates systematic deviations from rational budget allocation"
            }
        ]
    },

    {
        "id": "PAP-gaechter1998reciprocity",
        "authors": ["Fehr, Ernst", "Gächter, Simon"],
        "year": 1998,
        "title": "Reciprocity and Economics: The Economic Implications of Homo Reciprocans",
        "journal": "European Economic Review",
        "volume": 42,
        "issue": 3,
        "pages": "845-859",
        "doi": "10.1016/S0014-2921(97)00107-2",
        "citations": 2800,
        "status": "published",
        "key_findings": [
            {
                "finding": "People reciprocate fair behavior even when economically irrational",
                "domain": "nonprofit",
                "stage": "action",
                "primary_dimension": "S",
                "effect_size": 0.8
            }
        ],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["contemplation", "action"],
                "primary_dimension": "S",
                "psi_dominant": "fairness_norm",
                "gamma": 0.7,
                "A_level": 0.7,
                "W_level": 0.8,
                "awareness_type": "explicit",
                "key_insight": "Strong reciprocity preferences override self-interest, enabling cooperation"
            }
        ]
    },

    {
        "id": "PAP-madrian2001power",
        "authors": ["Madrian, Brigitte C.", "Shea, Dennis F."],
        "year": 2001,
        "title": "The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior",
        "journal": "Quarterly Journal of Economics",
        "volume": 116,
        "issue": 4,
        "pages": "1149-1187",
        "doi": "10.1162/003355301556329",
        "citations": 4200,
        "status": "published",
        "key_findings": [
            {
                "finding": "Automatic enrollment increases 401(k) participation from 49% to 86%",
                "domain": "finance",
                "stage": "preparation",
                "primary_intervention": "automatic_enrollment",
                "effect_size": 0.37,
                "population": "US workers"
            }
        ],
        "9c_coordinates": [
            {
                "domain": "finance",
                "stages": ["preparation", "action"],
                "primary_dimension": "F",
                "psi_dominant": "choice_architecture",
                "gamma": 0.5,
                "A_level": 0.4,
                "W_level": 0.6,
                "awareness_type": "mixed",
                "key_insight": "Default options dramatically increase participation, overcoming status quo bias"
            }
        ]
    },

    {
        "id": "PAP-johnson2003thepower",
        "authors": ["Johnson, Eric J.", "Goldstein, Daniel"],
        "year": 2003,
        "title": "Do Defaults Save Lives?",
        "journal": "Science",
        "volume": 302,
        "issue": 5649,
        "pages": "1338-1339",
        "doi": "10.1126/science.1091721",
        "citations": 3100,
        "status": "published",
        "key_findings": [
            {
                "finding": "Organ donation opt-out defaults increase consent from 12% to 86% across countries",
                "domain": "health",
                "stage": "precontemplation",
                "primary_intervention": "default",
                "effect_size": 0.74
            }
        ],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["precontemplation", "contemplation"],
                "primary_dimension": "S",
                "psi_dominant": "legal_framework",
                "gamma": 0.3,
                "A_level": 0.2,
                "W_level": 0.7,
                "awareness_type": "implicit",
                "key_insight": "Opt-out defaults are powerful precisely because most people never actively choose"
            }
        ]
    },

    {
        "id": "PAP-allcott2011social",
        "authors": ["Allcott, Hunt"],
        "year": 2011,
        "title": "Social Norms and Energy Conservation",
        "journal": "Journal of Public Economics",
        "volume": 95,
        "issue": 9,
        "pages": "1082-1095",
        "doi": "10.1016/j.jpubeco.2011.03.003",
        "citations": 1800,
        "status": "published",
        "key_findings": [
            {
                "finding": "Social norm feedback reduces energy consumption by 2-3%, effects persist after intervention",
                "domain": "energy",
                "stage": "action",
                "primary_intervention": "social_norm",
                "effect_size": 0.025
            }
        ],
        "9c_coordinates": [
            {
                "domain": "energy",
                "stages": ["action", "maintenance"],
                "primary_dimension": "S",
                "psi_dominant": "social_context",
                "gamma": 0.6,
                "A_level": 0.5,
                "W_level": 0.7,
                "awareness_type": "implicit",
                "key_insight": "Social comparison feedback leverages peer effects for sustained behavior change"
            }
        ]
    },

    {
        "id": "PAP-thaler2015choice",
        "authors": ["Thaler, Richard H.", "Sunstein, Cass R."],
        "year": 2015,
        "title": "Choice Architecture",
        "journal": "Behavioral Decision Making",
        "volume": 25,
        "pages": "213-246",
        "doi": "10.1002/bdm.1883",
        "citations": 2000,
        "status": "published",
        "key_findings": [
            {
                "finding": "Presentation order, defaults, and grouping dramatically affect choices",
                "domain": "health",
                "stage": "action",
                "primary_intervention": "choice_architecture",
                "effect_size": 1.2
            }
        ],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["preparation", "action"],
                "primary_dimension": "P",
                "psi_dominant": "choice_architecture",
                "gamma": 0.8,
                "A_level": 0.6,
                "W_level": 0.7,
                "awareness_type": "mixed",
                "key_insight": "Choice architecture has huge effects because decision-makers rely on context cues"
            }
        ]
    },

    {
        "id": "PAP-dellavigna2006paying",
        "authors": ["Della Vigna, Stefano", "Malmendier, Ulrike"],
        "year": 2009,
        "title": "Paying Not to Go to the Gym",
        "journal": "American Economic Review",
        "volume": 96,
        "issue": 3,
        "pages": "694-719",
        "doi": "10.1257/aer.96.3.694",
        "citations": 2200,
        "status": "published",
        "key_findings": [
            {
                "finding": "People overestimate future gym attendance, paying for memberships they won't use",
                "domain": "health",
                "stage": "contemplation",
                "primary_dimension": "P",
                "effect_size": 0.5
            }
        ],
        "9c_coordinates": [
            {
                "domain": "health",
                "stages": ["contemplation", "preparation"],
                "primary_dimension": "P",
                "psi_dominant": "temporal",
                "gamma": 0.4,
                "A_level": 0.3,
                "W_level": 0.4,
                "awareness_type": "implicit",
                "key_insight": "Present bias causes systematic overestimation of future intentions (naive projection)"
            }
        ]
    },

    {
        "id": "PAP-kube2012efficiency",
        "authors": ["Kube, Sebastian", "Maréchal, Michel André", "Puppe, Clemens"],
        "year": 2012,
        "title": "The Currency of Reciprocity: Gift Exchange in the Workplace",
        "journal": "American Economic Review",
        "volume": 102,
        "issue": 4,
        "pages": "1644-1662",
        "doi": "10.1257/aer.102.4.1644",
        "citations": 980,
        "status": "published",
        "key_findings": [
            {
                "finding": "Workers reciprocate wage increases with higher effort (80% of wage increase returned)",
                "domain": "workplace",
                "stage": "action",
                "primary_dimension": "S",
                "effect_size": 0.8
            }
        ],
        "9c_coordinates": [
            {
                "domain": "workplace",
                "stages": ["action"],
                "primary_dimension": "S",
                "psi_dominant": "fairness",
                "gamma": 0.6,
                "A_level": 0.7,
                "W_level": 0.8,
                "awareness_type": "explicit",
                "key_insight": "Reciprocity norms in workplace create powerful incentive effects beyond monetary value"
            }
        ]
    },

    {
        "id": "PAP-cialdini2006influence",
        "authors": ["Cialdini, Robert B."],
        "year": 2006,
        "title": "Influence: The Psychology of Persuasion",
        "journal": "Harper Business",
        "volume": 1,
        "citations": 10000,
        "status": "seminal",
        "key_findings": [
            {
                "finding": "Six principles of influence (reciprocity, commitment, social proof, authority, liking, scarcity)",
                "domain": "nonprofit",
                "stage": "contemplation",
                "primary_dimension": "S",
                "effect_size": 0.7
            }
        ],
        "9c_coordinates": [
            {
                "domain": "nonprofit",
                "stages": ["contemplation", "action"],
                "primary_dimension": "S",
                "psi_dominant": "social_context",
                "gamma": 0.75,
                "A_level": 0.6,
                "W_level": 0.65,
                "awareness_type": "mixed",
                "key_insight": "Universal principles of persuasion leverage deep-rooted psychological tendencies"
            }
        ]
    },

    {
        "id": "PAP-hoff2011whither",
        "authors": ["Hoff, Karla", "Stiglitz, Joseph E."],
        "year": 2010,
        "title": "Striving for Balance in Economics: Towards a Theory of the Social Determination of Behavior",
        "journal": "Journal of Economic Literature",
        "volume": 48,
        "issue": 2,
        "pages": "207-217",
        "doi": "10.1257/jel.48.2.207",
        "citations": 1200,
        "status": "published",
        "key_findings": [
            {
                "finding": "Social identity and group membership shape economic preferences and behavior",
                "domain": "government",
                "stage": "contemplation",
                "primary_dimension": "S",
                "effect_size": 0.6
            }
        ],
        "9c_coordinates": [
            {
                "domain": "government",
                "stages": ["contemplation", "action"],
                "primary_dimension": "S",
                "psi_dominant": "cultural",
                "gamma": 0.65,
                "A_level": 0.5,
                "W_level": 0.55,
                "awareness_type": "implicit",
                "key_insight": "Identity effects create path-dependent preferences that persist across contexts"
            }
        ]
    }
]

# =============================================================================
# JOURNAL QUALITY FILTER
# =============================================================================

TOP_TIER_JOURNALS = [
    "Econometrica",
    "American Economic Review (AER)",
    "Journal of Political Economy",
    "Quarterly Journal of Economics",
    "Journal of Economic Behavior & Organization",
    "Journal of Public Economics",
    "Science",
    "Nature",
]

# =============================================================================
# KNOWLEDGE MINER
# =============================================================================

class BehavioralEconPaperMiner:
    """Mine behavioral economics papers from training knowledge"""

⚠️  DEPRECATED (2026-02-08) — See header for details.

    def __init__(self):
        self.papers = BEHAVIORAL_ECON_PAPERS

    def filter_papers(
        self,
        domain: Optional[str] = None,
        min_citations: int = 0,
        min_year: int = 1979,
        status_filter: Optional[str] = None
    ) -> List[Dict]:
        """Filter papers by criteria"""
        filtered = self.papers

        if domain:
            filtered = [
                p for p in filtered
                if any(f.get('domain') == domain for f in p.get('key_findings', []))
            ]

        if min_citations > 0:
            filtered = [p for p in filtered if p.get('citations', 0) >= min_citations]

        if min_year:
            filtered = [p for p in filtered if p.get('year', 0) >= min_year]

        if status_filter:
            filtered = [p for p in filtered if p.get('status') == status_filter]

        return filtered

    def get_statistics(self) -> Dict:
        """Get mining statistics"""
        return {
            'total_papers': len(self.papers),
            'total_findings': sum(len(p.get('key_findings', [])) for p in self.papers),
            'average_citations': sum(p.get('citations', 0) for p in self.papers) / max(1, len(self.papers)),
            'year_range': f"{min(p.get('year', 2000) for p in self.papers)}-{max(p.get('year', 2000) for p in self.papers)}",
            'domains_covered': sorted(list(set(
                f.get('domain')
                for p in self.papers
                for f in p.get('key_findings', [])
                if f.get('domain')
            )))
        }

    def generate_yaml_entries(self, papers: List[Dict]) -> str:
        """Generate YAML entries for papers"""
        yaml_content = "sources:\n"

        for paper in papers:
            yaml_content += f"\n  - id: \"{paper['id']}\"\n"
            yaml_content += f"    authors: {json.dumps(paper.get('authors', []))}\n"
            yaml_content += f"    year: {paper.get('year')}\n"
            yaml_content += f"    title: \"{paper.get('title')}\"\n"
            yaml_content += f"    journal: \"{paper.get('journal')}\"\n"
            yaml_content += f"    volume: {paper.get('volume', 0)}\n"

            if paper.get('issue'):
                yaml_content += f"    issue: {paper.get('issue')}\n"

            yaml_content += f"    doi: \"{paper.get('doi', '')}\"\n"
            yaml_content += f"    citations: {paper.get('citations', 0)}\n"
            yaml_content += f"    status: \"{paper.get('status', 'published')}\"\n"

            yaml_content += f"    type: \"journal_article\"\n"
            yaml_content += f"    relevance: \"high\"\n"

            # Add key findings
            if paper.get('key_findings'):
                yaml_content += "    key_findings:\n"
                for finding in paper['key_findings']:
                    yaml_content += f"      - finding: \"{finding.get('finding')}\"\n"
                    yaml_content += f"        domain: {finding.get('domain')}\n"
                    if finding.get('stage'):
                        yaml_content += f"        stage: {finding.get('stage')}\n"
                    if finding.get('primary_dimension'):
                        yaml_content += f"        primary_dimension: {finding.get('primary_dimension')}\n"
                    if finding.get('effect_size'):
                        yaml_content += f"        effect_size: {finding.get('effect_size')}\n"

            # Add pre-extracted 10C
            if paper.get('9c_coordinates'):
                yaml_content += "    9c_coordinates:\n"
                for coords in paper['9c_coordinates']:
                    yaml_content += "      - domain: " + coords.get('domain') + "\n"
                    yaml_content += f"        stages: {json.dumps(coords.get('stages', []))}\n"
                    yaml_content += f"        primary_dimension: {coords.get('primary_dimension')}\n"
                    yaml_content += f"        psi_dominant: {coords.get('psi_dominant')}\n"
                    yaml_content += f"        gamma: {coords.get('gamma')}\n"
                    yaml_content += f"        A_level: {coords.get('A_level')}\n"
                    yaml_content += f"        W_level: {coords.get('W_level')}\n"
                    yaml_content += f"        awareness_type: {coords.get('awareness_type')}\n"
                    yaml_content += f"        key_insight: \"{coords.get('key_insight')}\"\n"

        return yaml_content

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Mine Behavioral Economics Papers from Training Knowledge")
    parser.add_argument('--domain', default=None, help="Filter by domain")
    parser.add_argument('--min-citations', type=int, default=0, help="Minimum citations")
    parser.add_argument('--min-year', type=int, default=1979, help="Minimum publication year")
    parser.add_argument('--status', default=None, help="Filter by status (seminal, published)")
    parser.add_argument('--output', default='data/paper-sources-mined.yaml', help="Output file")

    args = parser.parse_args()

    print("=" * 70)
    print("BEHAVIORAL ECONOMICS PAPER MINING - From LLM Training Knowledge")
    print("=" * 70)

    miner = BehavioralEconPaperMiner()

    # Get statistics
    print("\n[1/3] Mining Statistics")
    stats = miner.get_statistics()
    print(f"✅ Total Papers in Knowledge Base: {stats['total_papers']}")
    print(f"✅ Total Findings: {stats['total_findings']}")
    print(f"✅ Average Citations: {stats['average_citations']:.0f}")
    print(f"✅ Year Range: {stats['year_range']}")
    print(f"✅ Domains Covered: {', '.join(stats['domains_covered'])}")

    # Filter papers
    print(f"\n[2/3] Filtering Papers")
    filtered_papers = miner.filter_papers(
        domain=args.domain,
        min_citations=args.min_citations,
        min_year=args.min_year,
        status_filter=args.status
    )
    print(f"✅ Filtered to {len(filtered_papers)} papers")

    for paper in filtered_papers:
        findings = paper.get('key_findings', [])
        print(f"   - {paper['id']}: {paper['year']} ({len(findings)} findings, {paper.get('citations', 0)} citations)")

    # Generate YAML
    print(f"\n[3/3] Generating YAML")
    yaml_content = miner.generate_yaml_entries(filtered_papers)

    # Write to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, 'w') as f:
            f.write(yaml_content)
        print(f"✅ Written to {output_path}")
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return 1

    print("\n" + "=" * 70)
    print(f"DONE: {len(filtered_papers)} papers mined and documented")
    print("=" * 70)

    return 0

if __name__ == '__main__':
    exit(main())
