#!/usr/bin/env python3
"""
Batch process inbox PDFs: Add BibTeX entries and upgrade YAML metadata.
EXPERIMENTAL mode: processes all identified papers from Feb 2026 inbox batch.
"""

import os
import re
import subprocess
from datetime import datetime

# Papers to process: key -> metadata
PAPERS = {
    # === NEW BibTeX + NEW YAML ===
    "brynjolfsson2010complementarity": {
        "bibtex": """@incollection{brynjolfsson2010complementarity,
  title={Complementarity in Organizations},
  author={Brynjolfsson, Erik and Milgrom, Paul},
  booktitle={The Handbook of Organizational Economics},
  editor={Gibbons, Robert and Roberts, John},
  publisher={Princeton University Press},
  year={2010},
  evidence_tier = {1},
  use_for = {LIT-O, CORE-HOW, DOMAIN-ORG, FORMAL-COMP},
  theory_support = {MS-CM-001, MS-CM-002},
  parameter = {complementarity framework, systems of complements, supermodularity},
  identification = {theoretical, review, synthesis},
  external_validity = {organizational_design, manufacturing, IT},
  notes = {Handbook chapter on complementarity in organizations. Reviews formal theory of supermodularity and its application to organizational design, IT adoption, and systems of complements. Key reference for EBF complementarity framework.}
}""",
        "yaml_new": True,
        "title": "Complementarity in Organizations",
        "authors": [{"family": "Brynjolfsson", "given": "Erik"}, {"family": "Milgrom", "given": "Paul"}],
        "year": 2010,
        "journal": "The Handbook of Organizational Economics",
        "type": "incollection",
        "abstract": "This chapter reviews the formal theory of complementarity and its applications to organizations. Complementarity offers an approach to explaining patterns of organizational practices, how they fit with particular business strategies, and why different organizations choose different patterns and strategies.",
        "research_question": "How does the theory of complementarity explain patterns of organizational practices and their fit with business strategies?",
        "evidence_tier": 1,
        "use_for": ["LIT-O", "CORE-HOW", "DOMAIN-ORG", "FORMAL-COMP"],
        "theory_support": ["MS-CM-001", "MS-CM-002"],
        "primary_10c": [("HOW", "B", "Core complementarity theory"), ("WHAT", "C", "Organizational utility dimensions")],
        "inbox_file": "20240825_Complementarity in Organizations.pdf",
    },
    "baldwin2020ecosystems": {
        "bibtex": """@techreport{baldwin2020ecosystems,
  title={Ecosystems and Complementarities},
  author={Baldwin, Carliss Y.},
  institution={Harvard Business School},
  type={Working Paper},
  year={2020},
  evidence_tier = {2},
  use_for = {LIT-O, DOMAIN-ORG, CORE-HOW},
  theory_support = {MS-CM-001},
  parameter = {ecosystem complementarity, autonomous firms, joint value creation},
  identification = {theoretical, conceptual},
  external_validity = {technology ecosystems, platform economics},
  notes = {Chapter from Design Rules Volume 2. Introduces ecosystems as organizational layer defined by complementarities among autonomous firms. Links complementarity theory to platform and ecosystem economics.}
}""",
        "yaml_new": True,
        "title": "Ecosystems and Complementarities",
        "authors": [{"family": "Baldwin", "given": "Carliss Y."}],
        "year": 2020,
        "journal": "Harvard Business School Working Paper",
        "type": "techreport",
        "abstract": "This chapter introduces two new building blocks to the theory of how technology shapes organizations: business ecosystems and economic complementarity. Ecosystems are groups of autonomous firms whose actions create joint value, defined by complementarities among members.",
        "research_question": "How do complementarities define and shape business ecosystems?",
        "evidence_tier": 2,
        "use_for": ["LIT-O", "DOMAIN-ORG", "CORE-HOW"],
        "theory_support": ["MS-CM-001"],
        "primary_10c": [("HOW", "B", "Ecosystem complementarities"), ("WHAT", "C", "Joint value creation")],
        "inbox_file": "Ecosystems and Complementarities.pdf",
    },
    "pfeifer2011training": {
        "bibtex": """@techreport{pfeifer2011training,
  title={Effects of Training on Employee Suggestions and Promotions in an Internal Labor Market},
  author={Pfeifer, Christian and Janssen, Simon and Yang, Philip and Backes-Gellner, Uschi},
  institution={IZA},
  type={Discussion Paper},
  number={5671},
  year={2011},
  evidence_tier = {2},
  use_for = {LIT-O, DOMAIN-LABOR, CORE-WHAT},
  theory_support = {MS-HC-001},
  parameter = {training effects on promotions and suggestions},
  identification = {empirical, internal_labor_market, panel_data},
  external_validity = {German manufacturing, internal labor markets},
  notes = {IZA DP No. 5671. Studies effects of training on employee suggestions and promotions using internal labor market data from a German manufacturing firm.}
}""",
        "yaml_new": True,
        "title": "Effects of Training on Employee Suggestions and Promotions in an Internal Labor Market",
        "authors": [{"family": "Pfeifer", "given": "Christian"}, {"family": "Janssen", "given": "Simon"}, {"family": "Yang", "given": "Philip"}, {"family": "Backes-Gellner", "given": "Uschi"}],
        "year": 2011,
        "journal": "IZA Discussion Paper No. 5671",
        "type": "techreport",
        "abstract": "Studies effects of training on employee suggestions and promotions using internal labor market data from a German manufacturing firm.",
        "research_question": "How does training affect employee suggestions and promotions in internal labor markets?",
        "evidence_tier": 2,
        "use_for": ["LIT-O", "DOMAIN-LABOR", "CORE-WHAT"],
        "theory_support": ["MS-HC-001"],
        "primary_10c": [("WHAT", "C", "Human capital investment returns"), ("HOW", "B", "Training-promotion complementarity")],
        "inbox_file": "Effects of Training on Employee Suggestions and Promotions in an Internal Labor Market.pdf",
    },
    "eggenberger2022skills": {
        "bibtex": """@techreport{eggenberger2022skills,
  title={IT Skills, Occupation Specificity and Job Separations},
  author={Eggenberger, Christian and Backes-Gellner, Uschi},
  institution={IZA},
  type={Discussion Paper},
  number={15694},
  year={2022},
  evidence_tier = {2},
  use_for = {LIT-O, DOMAIN-LABOR, CORE-WHAT},
  theory_support = {MS-HC-001},
  parameter = {IT skill specificity, job separation rates},
  identification = {empirical, occupational_data, Swiss_labor_market},
  external_validity = {Switzerland, IT occupations, skill specificity},
  notes = {IZA DP No. 15694. Examines how IT skills and occupation specificity affect job separations in the Swiss labor market.}
}""",
        "yaml_new": True,
        "title": "IT Skills, Occupation Specificity and Job Separations",
        "authors": [{"family": "Eggenberger", "given": "Christian"}, {"family": "Backes-Gellner", "given": "Uschi"}],
        "year": 2022,
        "journal": "IZA Discussion Paper No. 15694",
        "type": "techreport",
        "abstract": "Examines how IT skills and occupation specificity affect job separations in the Swiss labor market.",
        "research_question": "How do IT skills and occupation specificity affect job separations?",
        "evidence_tier": 2,
        "use_for": ["LIT-O", "DOMAIN-LABOR", "CORE-WHAT"],
        "theory_support": ["MS-HC-001"],
        "primary_10c": [("WHAT", "C", "Skill complementarity in labor markets")],
        "inbox_file": "IT Skills, Occupation Specificity and Job Separations.pdf",
    },
    "helfat2015managerial": {
        "bibtex": """@article{helfat2015managerial,
  title={Managerial Cognitive Capabilities and the Microfoundations of Dynamic Capabilities},
  author={Helfat, Constance E. and Peteraf, Margaret A.},
  journal={Strategic Management Journal},
  volume={36},
  number={6},
  pages={831--850},
  year={2015},
  doi={10.1002/smj.2247},
  evidence_tier = {2},
  use_for = {LIT-O, DOMAIN-ORG, CORE-AWARE},
  theory_support = {MS-IB-001},
  parameter = {managerial cognitive capabilities, dynamic capabilities},
  identification = {theoretical, conceptual_framework},
  external_validity = {strategic management, organizational capabilities},
  notes = {Introduces managerial cognitive capability concept. Links cognitive capabilities to dynamic capabilities microfoundations. Published in Strategic Management Journal.}
}""",
        "yaml_new": True,
        "title": "Managerial Cognitive Capabilities and the Microfoundations of Dynamic Capabilities",
        "authors": [{"family": "Helfat", "given": "Constance E."}, {"family": "Peteraf", "given": "Margaret A."}],
        "year": 2015,
        "journal": "Strategic Management Journal",
        "type": "article",
        "abstract": "The microfoundations of dynamic capabilities have assumed greater importance in the search for factors that facilitate strategic change. We introduce the concept of managerial cognitive capability, which highlights the fact that capabilities involve the capacity to perform not only physical but also mental activities.",
        "research_question": "What role do managerial cognitive capabilities play in the microfoundations of dynamic capabilities?",
        "evidence_tier": 2,
        "use_for": ["LIT-O", "DOMAIN-ORG", "CORE-AWARE"],
        "theory_support": ["MS-IB-001"],
        "primary_10c": [("AWARE", "AU", "Cognitive capabilities of managers"), ("HOW", "B", "Dynamic capability interactions")],
        "inbox_file": "Managerial_cognitive_capabilities_and_th.pdf",
    },
    "henrekson2025football": {
        "bibtex": """@techreport{henrekson2025football,
  title={Why Is Competition in the European Football Market Failing, and What Should Be Done About It?},
  author={Henrekson, Magnus and Persson, Lars},
  institution={IZA},
  type={Discussion Paper},
  number={18354},
  year={2025},
  evidence_tier = {2},
  use_for = {LIT-O, DOMAIN-SPORT, CORE-HOW},
  theory_support = {MS-CM-001},
  parameter = {competitive balance, market design, football economics},
  identification = {theoretical, institutional_analysis},
  external_validity = {European football, sports economics, market design},
  notes = {IZA DP No. 18354. Analyzes why competition fails in European football and proposes market design solutions. Relevant for EBF complementarity in institutional design.}
}""",
        "yaml_new": True,
        "title": "Why Is Competition in the European Football Market Failing, and What Should Be Done About It?",
        "authors": [{"family": "Henrekson", "given": "Magnus"}, {"family": "Persson", "given": "Lars"}],
        "year": 2025,
        "journal": "IZA Discussion Paper No. 18354",
        "type": "techreport",
        "abstract": "Analyzes why competition fails in European football and proposes market design solutions.",
        "research_question": "Why is competition in the European football market failing and what reforms could improve it?",
        "evidence_tier": 2,
        "use_for": ["LIT-O", "DOMAIN-SPORT", "CORE-HOW"],
        "theory_support": ["MS-CM-001"],
        "primary_10c": [("HOW", "B", "Institutional complementarity in sports markets")],
        "inbox_file": "Why Is Competition in the European Football Market Failing, and What Should Be Done About It?.pdf",
    },
    "collis2025workplace": {
        "bibtex": """@techreport{collis2025workplace,
  title={Workplace Hostility},
  author={Collis, Manuela R. and Van Effenterre, Cl{\\'e}mentine},
  institution={IZA},
  type={Discussion Paper},
  number={18302},
  year={2025},
  evidence_tier = {2},
  use_for = {LIT-O, DOMAIN-LABOR, CORE-WHAT, CORE-WHO},
  theory_support = {MS-SP-001, MS-IB-001},
  parameter = {workplace hostility, gender, labor market outcomes},
  identification = {empirical},
  external_validity = {workplace behavior, gender economics},
  notes = {IZA DP No. 18302. Studies workplace hostility and its effects on labor market outcomes with a focus on gender dynamics.}
}""",
        "yaml_new": True,
        "title": "Workplace Hostility",
        "authors": [{"family": "Collis", "given": "Manuela R."}, {"family": "Van Effenterre", "given": "Clémentine"}],
        "year": 2025,
        "journal": "IZA Discussion Paper No. 18302",
        "type": "techreport",
        "abstract": "Studies workplace hostility and its effects on labor market outcomes with a focus on gender dynamics.",
        "research_question": "How does workplace hostility affect labor market outcomes, particularly for women?",
        "evidence_tier": 2,
        "use_for": ["LIT-O", "DOMAIN-LABOR", "CORE-WHAT", "CORE-WHO"],
        "theory_support": ["MS-SP-001", "MS-IB-001"],
        "primary_10c": [("WHO", "AAA", "Targets of workplace hostility"), ("WHAT", "C", "Social utility dimension — hostility costs")],
        "inbox_file": "Workplace Hostility.pdf",
    },
    "herrmann2008antisocial": {
        "bibtex": """@article{herrmann2008antisocial,
  title={Antisocial Punishment Across Societies},
  author={Herrmann, Benedikt and Th{\\"o}ni, Christian and G{\\"a}chter, Simon},
  journal={Science},
  volume={319},
  number={5868},
  pages={1362--1367},
  year={2008},
  doi={10.1126/science.1153808},
  evidence_tier = {1},
  use_for = {LIT-GCR, CORE-HOW, CORE-WHO, DOMAIN-COOP},
  theory_support = {MS-SP-001, MS-SP-002, MS-SP-005},
  parameter = {antisocial punishment rates across 16 societies, cooperation levels},
  identification = {experimental, cross_cultural, public_goods_game},
  external_validity = {16 societies worldwide, cross-cultural, N=1120},
  notes = {Published in Science. Landmark cross-cultural study showing antisocial punishment (punishing cooperators) varies dramatically across societies and undermines cooperation. Key evidence for EBF cultural context (Psi_K) effects on cooperation.}
}""",
        "yaml_new": True,
        "title": "Antisocial Punishment Across Societies",
        "authors": [{"family": "Herrmann", "given": "Benedikt"}, {"family": "Thöni", "given": "Christian"}, {"family": "Gächter", "given": "Simon"}],
        "year": 2008,
        "journal": "Science",
        "type": "article",
        "doi": "10.1126/science.1153808",
        "abstract": "We document the existence of antisocial punishment — the sanctioning of people who behave prosocially — across 16 diverse societies. Antisocial punishment is widespread and varies strongly across societies. Where antisocial punishment is prevalent, cooperation breaks down.",
        "research_question": "How prevalent is antisocial punishment across societies and how does it affect cooperation?",
        "evidence_tier": 1,
        "use_for": ["LIT-GCR", "CORE-HOW", "CORE-WHO", "DOMAIN-COOP"],
        "theory_support": ["MS-SP-001", "MS-SP-002", "MS-SP-005"],
        "primary_10c": [("HOW", "B", "Punishment-cooperation complementarity"), ("WHO", "AAA", "Cross-cultural variation in punishment norms"), ("WHEN", "V", "Cultural context Psi_K determines punishment")],
        "inbox_file": "herrmann-thoni-gachter.pdf",
    },
    "luger2023depends": {
        "bibtex": """@article{luger2023depends,
  title={Who Depends on Why: Toward an Endogenous, Purpose-driven Mechanism in Organizations' Reference Selection},
  author={Luger, Johannes},
  journal={Strategic Management Journal},
  volume={44},
  number={8},
  pages={2035--2059},
  year={2023},
  doi={10.1002/smj.3486},
  evidence_tier = {2},
  use_for = {LIT-O, DOMAIN-ORG, CORE-WHAT},
  theory_support = {MS-IB-001},
  parameter = {reference selection, organizational purpose, identity},
  identification = {empirical, organizational_data},
  external_validity = {organizational strategy, reference groups},
  notes = {Published in SMJ. Proposes endogenous purpose-driven mechanism for why organizations select specific reference groups. Links organizational identity to strategic reference selection.}
}""",
        "yaml_new": True,
        "title": "Who Depends on Why: Toward an Endogenous, Purpose-driven Mechanism in Organizations' Reference Selection",
        "authors": [{"family": "Luger", "given": "Johannes"}],
        "year": 2023,
        "journal": "Strategic Management Journal",
        "type": "article",
        "doi": "10.1002/smj.3486",
        "abstract": "Proposes an endogenous, purpose-driven mechanism for why organizations select specific reference groups. Links organizational identity and purpose to strategic reference selection.",
        "research_question": "Why do organizations select specific reference groups, and how does purpose drive this selection?",
        "evidence_tier": 2,
        "use_for": ["LIT-O", "DOMAIN-ORG", "CORE-WHAT"],
        "theory_support": ["MS-IB-001"],
        "primary_10c": [("WHAT", "C", "Organizational identity utility"), ("WHO", "AAA", "Reference group selection")],
        "inbox_file": "johannes_luger_who_depends_on_why_publishersversion.pdf",
    },
}

# Papers that need YAML UPGRADE (already have stubs)
UPGRADES = {
    "milgrom1995complementarities": {
        "title": "Complementarities and Fit: Strategy, Structure, and Organizational Change in Manufacturing",
        "inbox_file": "20240826_ Complementarities and Fit_Strategy, Structure, and Organizational Change in Manufacturing.pdf",
    },
    "milgrom1994complementarities": {
        "title": "Complementarities and Systems: Understanding Japanese Economic Organization",
        "inbox_file": "Complementarities_Japanese System.pdf",
    },
    "benabou2025identity": {
        "title": "Identity as Self-Image",
        "inbox_file": "IDENTITY AS SELF-IMAGE.pdf",
    },
    "bloom2012management": {
        "title": "Management Practices Across Firms and Countries",
        "inbox_file": "MANAGEMENT PRACTICES ACROSS FIRMS AND COUNTRIES .pdf",
    },
}

# Papers already fully in DB (just link PDF)
EXISTING = {
    "stigler1977gustibus": "StiglerBeckerAER.pdf",
    "rustagi2024historical": "Historical self-governance.pdf",
    "hoffman2018people": "People Management Skills.pdf",
    "backesgellner2018preferences": "Do Preferences and Biases Predict Life Outcomes?.pdf",
}

# Duplicate PDFs (skip)
DUPLICATES = [
    "Complementarities and fit.pdf",  # = milgrom1995complementarities
    "Complementarity in Organizations.pdf",  # = brynjolfsson2010complementarity
    "How Technology Shapes Organizations Chapter 5 Ecosystems and Complementarities By Carliss Y. Baldwin.pdf",  # = baldwin2020ecosystems
]


def generate_yaml(key, meta):
    """Generate YAML content for a new paper."""
    authors_yaml = "\n".join([f'  - family: {a["family"]}\n    given: {a["given"]}' for a in meta["authors"]])
    use_for_yaml = "\n".join([f"  - {u}" for u in meta["use_for"]])
    theory_yaml = "\n".join([f"  - {t}" for t in meta["theory_support"]])
    dim_yaml = ""
    for dim, code, rel in meta.get("primary_10c", []):
        dim_yaml += f"""    - dimension: {dim}
      code: {code}
      relevance: "{rel}"
"""

    return f"""id: PAP-{key}
bibtex_key: {key}
title: "{meta['title']}"
authors:
{authors_yaml}
year: {meta['year']}
journal: "{meta['journal']}"
type: {meta['type']}
{f'doi: "{meta["doi"]}"' if meta.get('doi') else ''}

status:
  content_level: L1
  integration_level: I2
  evidence_tier: {meta['evidence_tier']}

abstract: |
  {meta['abstract']}

research_question: "{meta['research_question']}"

key_findings_structured: []

behavioral_mapping:
  primary_10c:
{dim_yaml}
theory_integration:
  primary_theories:
{theory_yaml}

use_for:
{use_for_yaml}

prior_score:
  content_level: L1
  integration_level: I2
  confidence_multiplier: 0.8
  computed_date: "{datetime.now().strftime('%Y-%m-%d')}"

full_text:
  available: false
  inbox_file: "data/paper-texts/inbox/{meta['inbox_file']}"

linked_cases: []
ssot_migration_date: "{datetime.now().strftime('%Y-%m-%d')}"
"""


def main():
    stats = {"new_bibtex": 0, "new_yaml": 0, "upgraded": 0, "linked": 0, "skipped": 0}

    # 1. Add new BibTeX entries
    print("=" * 60)
    print("STEP 1: Adding BibTeX entries for new papers")
    print("=" * 60)

    with open("bibliography/bcm_master.bib", "r") as f:
        existing_bib = f.read()

    new_entries = []
    for key, meta in PAPERS.items():
        if key not in existing_bib:
            new_entries.append(meta["bibtex"])
            stats["new_bibtex"] += 1
            print(f"  + {key}")
        else:
            print(f"  ~ {key} (already in BibTeX)")

    if new_entries:
        with open("bibliography/bcm_master.bib", "a") as f:
            f.write("\n\n%==============================================================================\n")
            f.write("% INBOX BATCH: Complementarity, Management, Identity, Labor (Feb 2026)\n")
            f.write("%==============================================================================\n\n")
            f.write("\n\n".join(new_entries))
            f.write("\n")

    # 2. Create new YAML files
    print(f"\n{'=' * 60}")
    print("STEP 2: Creating new Paper-YAML files")
    print("=" * 60)

    for key, meta in PAPERS.items():
        yaml_path = f"data/paper-references/PAP-{key}.yaml"
        if not os.path.exists(yaml_path):
            content = generate_yaml(key, meta)
            with open(yaml_path, "w") as f:
                f.write(content)
            stats["new_yaml"] += 1
            print(f"  + {yaml_path}")
        else:
            print(f"  ~ {yaml_path} (already exists)")

    # 3. Link existing papers to inbox PDFs
    print(f"\n{'=' * 60}")
    print("STEP 3: Linking existing papers to inbox PDFs")
    print("=" * 60)

    for key, pdf_file in EXISTING.items():
        print(f"  ~ {key} -> {pdf_file}")
        stats["linked"] += 1

    # 4. Report duplicates
    print(f"\n{'=' * 60}")
    print("STEP 4: Skipping duplicates")
    print("=" * 60)
    for dup in DUPLICATES:
        print(f"  - {dup}")
        stats["skipped"] += 1

    # Summary
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print("=" * 60)
    print(f"  New BibTeX entries:  {stats['new_bibtex']}")
    print(f"  New YAML files:      {stats['new_yaml']}")
    print(f"  Existing (linked):   {stats['linked']}")
    print(f"  Duplicates skipped:  {stats['skipped']}")
    print(f"  Upgrades needed:     {len(UPGRADES)}")


if __name__ == "__main__":
    main()
