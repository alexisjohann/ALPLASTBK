#!/usr/bin/env python3
"""
Paper Generator from EBF Appendices
====================================

Automatically generates academic papers from EBF appendices using the 8D Document
Type Framework (Axioms DT-1 to DT-9 from Appendix DDD).

The 8D Framework:
- D1: Wissen (Knowledge) - 0=Layperson, 1=Expert
- D2: Nähe (Proximity) - 0=Distant field, 1=Same discipline
- D3: Reichweite (Scope) - 0=Personal, 1=Societal
- D4: Zeit (Time) - 0=Little reading time, 1=Much reading time
- D5: Ziel (Goal) - G1=Inform, G2=Act, G3=Persuade, G4=Entertain, G5=Experience, G6=Connect, G7=Express
- D6: Kontext (Context) - 0=Internal, 1=External
- D7: Emotion - 0=Factual, 1=Emotional
- D8: Persistenz (Persistence) - 0=Ephemeral, 1=Archival

Emergence Chain (per Appendix DDD):
  8D Coordinates → Structure (DT-5, DT-6)
  8D Coordinates → Style (DT-7, DT-8) → Vocabulary (DT-9)

Usage:
    python generate_paper.py <appendix_file> [--style <style_name>] [--output <output_dir>]

Example:
    python generate_paper.py appendices/LIT-META_metascience_integration.tex --style ernst_fehr
"""

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ==============================================================================
# 8D DOCUMENT TYPE FRAMEWORK (from Appendix DDD)
# ==============================================================================

class Goal(Enum):
    """D5 Goal Categories (from Appendix DDD, Table D5 Goals)"""
    G1_INFORM = "G1"      # Informieren - Transfer knowledge
    G2_ACT = "G2"         # Handeln - Trigger specific action
    G3_PERSUADE = "G3"    # Überzeugen - Change beliefs
    G4_ENTERTAIN = "G4"   # Unterhalten - Provide enjoyment
    G5_EXPERIENCE = "G5"  # Erleben - Create aesthetic experience
    G6_CONNECT = "G6"     # Verbinden - Build relationship
    G7_EXPRESS = "G7"     # Ausdrücken - Convey emotion/opinion


class OutputFormat(Enum):
    """Output format types (from Appendix CCC, Section Output Generation)"""
    LATEX = "latex"
    MARKDOWN = "markdown"
    PLAIN = "plain"


@dataclass
class OutputConfig:
    """
    Output configuration derived from 8D coordinates.
    Implements Rules O-1 and O-2 from Appendix CCC.
    """
    format: OutputFormat
    auto_compile: bool
    output_dir: str = "outputs"

    @classmethod
    def from_8d(cls, d1: float, d6: float, d8: float, output_dir: str = "outputs") -> "OutputConfig":
        """
        Derive output configuration from 8D coordinates.

        Rule O-1 (Format Selection):
            Format(D8, D6) = LaTeX     if D8 > 0.6 or (D6 > 0.8 and D1 > 0.7)
                          = Markdown  if 0.3 < D8 ≤ 0.6
                          = Plain     if D8 ≤ 0.3

        Rule O-2 (Auto-Compile):
            AutoCompile = True  if Format = LaTeX and D8 > 0.5
                        = False otherwise
        """
        # Rule O-1: Format Selection
        if d8 > 0.6 or (d6 > 0.8 and d1 > 0.7):
            fmt = OutputFormat.LATEX
        elif d8 > 0.3:
            fmt = OutputFormat.MARKDOWN
        else:
            fmt = OutputFormat.PLAIN

        # Rule O-2: Auto-Compile
        auto_compile = (fmt == OutputFormat.LATEX and d8 > 0.5)

        return cls(
            format=fmt,
            auto_compile=auto_compile,
            output_dir=output_dir
        )

    def should_compile_pdf(self) -> bool:
        """Check if PDF should be auto-compiled based on O-2."""
        return self.auto_compile and self.format == OutputFormat.LATEX


@dataclass
class DocumentType8D:
    """
    8D Document Type representation (Axiom DT-2: Dimensional Sufficiency).

    From Appendix DDD: "Eight dimensions are sufficient to characterize any audience."
    """
    name: str
    d1_knowledge: float    # 0=layperson, 1=expert
    d2_proximity: float    # 0=distant, 1=same field
    d3_scope: float        # 0=personal, 1=societal
    d4_time: float         # 0=little, 1=much
    d5_goal: Goal          # categorical
    d6_context: float      # 0=internal, 1=external
    d7_emotion: float      # 0=factual, 1=emotional
    d8_persistence: float  # 0=ephemeral, 1=archival

    def derive_structure(self) -> Dict[str, bool]:
        """
        Axiom DT-5 & DT-6: Structure Emergence from 8D coordinates.

        From Appendix DDD lines 449-465:
        - D1 > 0.7 → Technical Glossary required
        - D4 > 0.6 → Detailed subsections permitted
        - D4 < 0.3 → Executive Summary required
        - D5 = G1 → Theory/Methods section required
        - D5 = G2 → Call-to-Action required
        - D8 > 0.8 → References + Version Control required
        """
        return {
            "glossary_required": self.d1_knowledge > 0.7,
            "detailed_subsections": self.d4_time > 0.6,
            "executive_summary": self.d4_time < 0.3,
            "theory_section": self.d5_goal == Goal.G1_INFORM,
            "call_to_action": self.d5_goal == Goal.G2_ACT,
            "full_references": self.d8_persistence > 0.8,
            "version_control": self.d8_persistence > 0.8,
        }

    def derive_style(self) -> Dict[str, any]:
        """
        Axiom DT-7 & DT-8: Style Emergence from 8D coordinates.

        From Appendix DDD lines 500-531:
        Vocabulary & Complexity:
        - D1 > 0.7 → Technical vocabulary, Flesch-Kincaid ≥ 14
        - D1 < 0.3 → Simple vocabulary, Flesch-Kincaid ≤ 8
        - D2 > 0.8 → Field-specific jargon permitted

        Sentence Structure:
        - D4 > 0.6 → Complex sentences permitted (avg > 20 words)
        - D4 < 0.3 → Short sentences required (avg < 15 words)

        Tone & Voice:
        - D6 > 0.7 → Formal register, passive voice acceptable
        - D6 < 0.3 → Informal register, active voice preferred
        - D7 > 0.6 → Personal pronouns (I/we), narrative elements
        - D7 < 0.3 → Impersonal style, no narrative

        Epistemic Markers:
        - D8 > 0.8 → Hedging required ("suggests", "may")
        - D5 = G3 → Boosters permitted ("clearly", "certainly")
        """
        return {
            # Vocabulary complexity
            "technical_vocabulary": self.d1_knowledge > 0.7,
            "simple_vocabulary": self.d1_knowledge < 0.3,
            "flesch_kincaid_min": 14 if self.d1_knowledge > 0.7 else (8 if self.d1_knowledge < 0.3 else 11),
            "jargon_permitted": self.d2_proximity > 0.8,

            # Sentence structure
            "complex_sentences": self.d4_time > 0.6,
            "short_sentences": self.d4_time < 0.3,
            "avg_sentence_length": 25 if self.d4_time > 0.6 else (12 if self.d4_time < 0.3 else 18),

            # Tone & Voice
            "formal_register": self.d6_context > 0.7,
            "informal_register": self.d6_context < 0.3,
            "passive_voice_ok": self.d6_context > 0.7,
            "personal_pronouns": self.d7_emotion > 0.6,
            "impersonal_style": self.d7_emotion < 0.3,
            "narrative_elements": self.d7_emotion > 0.6,

            # Epistemic markers
            "hedging_required": self.d8_persistence > 0.8,
            "boosters_permitted": self.d5_goal == Goal.G3_PERSUADE,
        }

    def derive_vocabulary(self) -> Dict[str, List[str]]:
        """
        Axiom DT-9: Vocabulary Emergence from style parameters.

        From Appendix DDD lines 553-591:
        From Hedging Parameter:
        - hedging=True → "suggests", "may", "indicates", "appears"
        - hedging=False → "shows", "proves", "demonstrates", "is"

        From Booster Parameter:
        - boosters=True → "clearly", "certainly", "undoubtedly"
        - boosters=False → ∅

        From Register Parameter:
        - register=Formal → "therefore", "consequently", "however"
        - register=Informal → "so", "but", "anyway"

        From Personal Pronouns Parameter:
        - pronouns=True → "I", "we", "my", "our"
        - pronouns=False → "the study", "the analysis", "results"
        """
        style = self.derive_style()

        vocab = {}

        # Hedging vocabulary
        if style["hedging_required"]:
            vocab["hedging"] = ["suggests", "may", "indicates", "appears", "could", "might"]
            vocab["assertions"] = []  # Avoid direct assertions
        else:
            vocab["hedging"] = []
            vocab["assertions"] = ["shows", "proves", "demonstrates", "is", "confirms"]

        # Booster vocabulary
        if style["boosters_permitted"]:
            vocab["boosters"] = ["clearly", "certainly", "undoubtedly", "obviously", "definitely"]
        else:
            vocab["boosters"] = []

        # Register vocabulary (connectives)
        if style["formal_register"]:
            vocab["connectives"] = ["therefore", "consequently", "however", "furthermore",
                                   "moreover", "nevertheless", "notwithstanding"]
        else:
            vocab["connectives"] = ["so", "but", "anyway", "also", "still", "though"]

        # Subject references
        if style["personal_pronouns"]:
            vocab["subjects"] = ["I", "we", "my", "our", "the author"]
        else:
            vocab["subjects"] = ["the study", "the analysis", "results", "this paper",
                                "the evidence", "the findings"]

        return vocab


# ==============================================================================
# PREDEFINED STYLE PROFILES (Named 8D Coordinates)
# ==============================================================================

# From Appendix CCC: Example Document Types with 8D coordinates
STYLE_PROFILES: Dict[str, DocumentType8D] = {
    "ernst_fehr": DocumentType8D(
        name="Ernst Fehr Academic Style",
        d1_knowledge=0.9,    # Expert audience
        d2_proximity=0.9,    # Same field (behavioral economics)
        d3_scope=0.7,        # Field-wide impact
        d4_time=0.8,         # Much reading time
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,      # External (public)
        d7_emotion=0.1,      # Highly factual (Fehr is direct, not hedged)
        d8_persistence=0.95  # Archival
    ),
    "kahneman_tversky": DocumentType8D(
        name="Kahneman-Tversky Style",
        d1_knowledge=0.8,
        d2_proximity=0.7,
        d3_scope=0.65,
        d4_time=0.7,
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,
        d7_emotion=0.2,      # Slightly more accessible
        d8_persistence=0.9
    ),
    "policy_brief": DocumentType8D(
        name="Policy Brief Style",
        d1_knowledge=0.6,
        d2_proximity=0.4,
        d3_scope=0.85,       # Societal impact
        d4_time=0.3,         # Quick read
        d5_goal=Goal.G2_ACT,
        d6_context=1.0,
        d7_emotion=0.25,
        d8_persistence=0.7
    ),
    "academic_standard": DocumentType8D(
        name="Standard Academic Style",
        d1_knowledge=0.85,
        d2_proximity=0.75,
        d3_scope=0.6,
        d4_time=0.7,
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,
        d7_emotion=0.15,
        d8_persistence=0.9
    ),
    "practitioner": DocumentType8D(
        name="Practitioner Style",
        d1_knowledge=0.5,
        d2_proximity=0.3,
        d3_scope=0.5,
        d4_time=0.4,
        d5_goal=Goal.G2_ACT,
        d6_context=0.8,
        d7_emotion=0.3,
        d8_persistence=0.5
    ),
    "ebf_appendix": DocumentType8D(
        name="EBF Appendix Style",
        d1_knowledge=0.85,
        d2_proximity=0.75,
        d3_scope=0.6,
        d4_time=0.70,
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,
        d7_emotion=0.15,
        d8_persistence=0.90
    ),
    # -------------------------------------------------------------------------
    # JOURNALISTIC PROFILES
    # -------------------------------------------------------------------------
    "der_spiegel": DocumentType8D(
        name="Der Spiegel Style",
        d1_knowledge=0.4,        # Educated layperson (Bildungsbürger)
        d2_proximity=0.2,        # Distant from academic field
        d3_scope=0.8,            # Societal relevance
        d4_time=0.4,             # Magazine-length attention
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.5,          # Narrative, engaging
        d8_persistence=0.4       # Weekly magazine lifecycle
    ),
    "nyt_science": DocumentType8D(
        name="New York Times Science Style",
        d1_knowledge=0.5,        # Educated general public
        d2_proximity=0.25,       # Outside academia
        d3_scope=0.75,           # Broad societal interest
        d4_time=0.35,            # Newspaper article length
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.35,         # Accessible but authoritative
        d8_persistence=0.5       # News cycle + archive
    ),
    "economist": DocumentType8D(
        name="The Economist Style",
        d1_knowledge=0.6,        # Business/policy educated
        d2_proximity=0.35,       # Adjacent fields
        d3_scope=0.85,           # Global policy implications
        d4_time=0.45,            # Concise but substantive
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.3,          # Witty but factual
        d8_persistence=0.6       # Weekly + archive
    ),
    "harvard_business_review": DocumentType8D(
        name="Harvard Business Review Style",
        d1_knowledge=0.7,        # Business leaders, MBAs
        d2_proximity=0.5,        # Management/strategy adjacent
        d3_scope=0.65,           # Organizational focus
        d4_time=0.55,            # Substantial reads
        d5_goal=Goal.G2_ACT,     # Action-oriented
        d6_context=1.0,          # Public
        d7_emotion=0.25,         # Professional tone
        d8_persistence=0.7       # Referenced in business
    ),
    "wissenschaft_de": DocumentType8D(
        name="wissenschaft.de Style",
        d1_knowledge=0.45,       # Science-interested public
        d2_proximity=0.3,        # Popular science
        d3_scope=0.6,            # General interest
        d4_time=0.3,             # Online article
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.4,          # Engaging, curious
        d8_persistence=0.35      # Online lifecycle
    ),
    # -------------------------------------------------------------------------
    # HIGH-IMPACT SCIENTIFIC JOURNALS
    # -------------------------------------------------------------------------
    "nature": DocumentType8D(
        name="Nature Style",
        d1_knowledge=0.85,       # Expert but cross-disciplinary
        d2_proximity=0.6,        # Broad scientific audience
        d3_scope=0.9,            # High societal impact
        d4_time=0.5,             # Concise but substantive
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.2,          # Accessible yet rigorous
        d8_persistence=0.95      # Archival
    ),
    "science": DocumentType8D(
        name="Science (AAAS) Style",
        d1_knowledge=0.85,       # Expert but accessible
        d2_proximity=0.6,        # Broad scientific
        d3_scope=0.9,            # High impact
        d4_time=0.5,             # Concise
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.15,         # More formal than Nature
        d8_persistence=0.95      # Archival
    ),
    "pnas": DocumentType8D(
        name="PNAS Style",
        d1_knowledge=0.88,       # Expert
        d2_proximity=0.7,        # Cross-disciplinary science
        d3_scope=0.8,            # High impact
        d4_time=0.65,            # Full research article
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.1,          # Very formal
        d8_persistence=0.95      # Archival
    ),
    "nber_working_paper": DocumentType8D(
        name="NBER Working Paper Style",
        d1_knowledge=0.92,       # Economics experts
        d2_proximity=0.85,       # Same field
        d3_scope=0.75,           # Policy relevant
        d4_time=0.85,            # Long, technical
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.05,         # Very dry, technical
        d8_persistence=0.85      # Working paper lifecycle
    ),
    # -------------------------------------------------------------------------
    # BUSINESS & FINANCE JOURNALISM
    # -------------------------------------------------------------------------
    "financial_times": DocumentType8D(
        name="Financial Times Style",
        d1_knowledge=0.65,       # Business/finance educated
        d2_proximity=0.4,        # Adjacent fields
        d3_scope=0.85,           # Global markets
        d4_time=0.4,             # Daily news depth
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.25,         # Authoritative
        d8_persistence=0.55      # News + archive
    ),
    "wall_street_journal": DocumentType8D(
        name="Wall Street Journal Style",
        d1_knowledge=0.6,        # Business readers
        d2_proximity=0.35,       # General business
        d3_scope=0.8,            # US/global business
        d4_time=0.35,            # Daily newspaper
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.3,          # Engaging business stories
        d8_persistence=0.5       # News cycle
    ),
    "forbes": DocumentType8D(
        name="Forbes Style",
        d1_knowledge=0.55,       # Business-interested
        d2_proximity=0.3,        # Popular business
        d3_scope=0.7,            # Business/wealth
        d4_time=0.35,            # Magazine/online
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.4,          # Success stories, lists
        d8_persistence=0.4       # Magazine lifecycle
    ),
    # -------------------------------------------------------------------------
    # MANAGEMENT & CONSULTING
    # -------------------------------------------------------------------------
    "mckinsey_quarterly": DocumentType8D(
        name="McKinsey Quarterly Style",
        d1_knowledge=0.75,       # C-suite, consultants
        d2_proximity=0.55,       # Strategy/management
        d3_scope=0.7,            # Organizational
        d4_time=0.5,             # Substantive reads
        d5_goal=Goal.G2_ACT,     # Action-oriented
        d6_context=1.0,          # Public
        d7_emotion=0.2,          # Professional, confident
        d8_persistence=0.65      # Referenced in business
    ),
    "mit_sloan_review": DocumentType8D(
        name="MIT Sloan Management Review Style",
        d1_knowledge=0.75,       # Managers, academics
        d2_proximity=0.6,        # Management science
        d3_scope=0.65,           # Organizational
        d4_time=0.55,            # Research-backed articles
        d5_goal=Goal.G2_ACT,     # Practical insights
        d6_context=1.0,          # Public
        d7_emotion=0.2,          # Academic-practitioner bridge
        d8_persistence=0.7       # Referenced
    ),
    # -------------------------------------------------------------------------
    # LONG-FORM & TECH JOURNALISM
    # -------------------------------------------------------------------------
    "the_atlantic": DocumentType8D(
        name="The Atlantic Style",
        d1_knowledge=0.5,        # Educated general public
        d2_proximity=0.25,       # Broad topics
        d3_scope=0.75,           # Culture/society/politics
        d4_time=0.6,             # Long-form
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.5,          # Narrative, essay
        d8_persistence=0.6       # Magazine + archive
    ),
    "wired": DocumentType8D(
        name="Wired Style",
        d1_knowledge=0.55,       # Tech-interested
        d2_proximity=0.35,       # Technology adjacent
        d3_scope=0.7,            # Tech/society
        d4_time=0.45,            # Magazine length
        d5_goal=Goal.G1_INFORM,
        d6_context=1.0,          # Public
        d7_emotion=0.5,          # Enthusiastic, future-oriented
        d8_persistence=0.45      # Magazine lifecycle
    ),
    # -------------------------------------------------------------------------
    # PRESENTATION & SPEAKING
    # -------------------------------------------------------------------------
    "ted_talk": DocumentType8D(
        name="TED Talk Style",
        d1_knowledge=0.4,        # General audience
        d2_proximity=0.2,        # Any topic
        d3_scope=0.8,            # Ideas worth spreading
        d4_time=0.25,            # 18 minutes max
        d5_goal=Goal.G5_EXPERIENCE,  # Inspire, experience
        d6_context=1.0,          # Public
        d7_emotion=0.7,          # High emotional engagement
        d8_persistence=0.7       # Videos archived, viral
    ),
}

# Category defaults (from Appendix CCC)
CATEGORY_DEFAULTS = {
    "CORE": "academic_standard",
    "FORMAL": "ernst_fehr",
    "DOMAIN": "practitioner",
    "CONTEXT": "academic_standard",
    "METHOD": "ernst_fehr",
    "PREDICT": "academic_standard",
    "LIT": "ernst_fehr",
    "REF": "practitioner",
}


# ==============================================================================
# APPENDIX PARSER
# ==============================================================================

@dataclass
class AppendixContent:
    """Parsed content from an EBF appendix."""
    title: str
    category: str
    abstract: str
    fundamental_question: str
    sections: List[Tuple[str, str]]  # (title, content)
    references: List[str]
    key_concepts: List[str]
    equations: List[str]
    tables: List[str]


def parse_appendix(filepath: str) -> AppendixContent:
    """Parse an EBF appendix LaTeX file and extract structured content."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'\\chapter\{([^}]+)\}', content)
    title = title_match.group(1) if title_match else "Untitled"

    # Extract category from filename or content
    category_match = re.search(r'CATEGORY:\s*(\w+)', content)
    if not category_match:
        # Try to extract from filename
        filename = Path(filepath).stem
        for cat in ["CORE", "FORMAL", "DOMAIN", "CONTEXT", "METHOD", "PREDICT", "LIT", "REF"]:
            if cat in filename.upper():
                category = cat
                break
        else:
            category = "Unknown"
    else:
        category = category_match.group(1)

    # Extract abstract
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', content, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""

    # Extract fundamental question
    fq_match = re.search(r'Fundamental Question.*?\\textbf\{([^}]+)\}', content, re.DOTALL)
    if not fq_match:
        fq_match = re.search(r'Core Question.*?\\textit\{([^}]+)\}', content, re.DOTALL)
    fundamental_question = fq_match.group(1) if fq_match else ""

    # Extract sections
    sections = []
    section_pattern = r'\\section\{([^}]+)\}(.*?)(?=\\section\{|\\chapter\{|\\end\{document\}|$)'
    for match in re.finditer(section_pattern, content, re.DOTALL):
        section_title = match.group(1)
        section_content = match.group(2).strip()
        sections.append((section_title, section_content))

    # Extract subsections if no sections found
    if not sections:
        subsection_pattern = r'\\subsection\{([^}]+)\}(.*?)(?=\\subsection\{|\\section\{|\\end\{document\}|$)'
        for match in re.finditer(subsection_pattern, content, re.DOTALL):
            section_title = match.group(1)
            section_content = match.group(2).strip()
            sections.append((section_title, section_content))

    # Extract references (bibitem entries)
    references = re.findall(r'\\bibitem\[[^\]]*\]\{[^}]+\}\s*([^\n]+)', content)

    # Extract key concepts (from bold text, filtered)
    concepts = re.findall(r'\\textbf\{([^}]+)\}', content)
    valid_concepts = [
        c for c in concepts
        if len(c) < 30
        and len(c) > 2
        and not any(char in c for char in [':', '\\', '{', '}', '$', '—', '–', '=', '+'])
        and c.strip()
        and not c.strip().isdigit()
    ]
    key_concepts = list(set(valid_concepts))[:15]

    # Extract equations
    equations = re.findall(r'\\begin\{equation\}(.*?)\\end\{equation\}', content, re.DOTALL)

    # Extract tables
    tables = re.findall(r'\\begin\{table\}.*?\\end\{table\}', content, re.DOTALL)

    return AppendixContent(
        title=title,
        category=category,
        abstract=abstract,
        fundamental_question=fundamental_question,
        sections=sections,
        references=references,
        key_concepts=key_concepts,
        equations=equations,
        tables=tables
    )


# ==============================================================================
# PAPER GENERATOR
# ==============================================================================

def generate_paper_number() -> str:
    """Generate next WP number based on existing papers."""
    papers_dir = Path(__file__).parent.parent / "papers"
    existing = list(papers_dir.glob("WP_2026_*.tex"))

    numbers = []
    for p in existing:
        match = re.search(r'WP_2026_(\d+)', p.name)
        if match:
            numbers.append(int(match.group(1)))

    next_num = max(numbers) + 1 if numbers else 1
    return f"{next_num:02d}"


def clean_latex_content(content: str) -> str:
    """Clean LaTeX content for inclusion in paper."""
    # Remove tcolorbox environments
    content = re.sub(r'\\begin\{tcolorbox\}[^\]]*\]', '', content)
    content = re.sub(r'\\end\{tcolorbox\}', '', content)

    # Remove tikzpicture environments
    content = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', '', content, flags=re.DOTALL)

    # Remove figure environments
    content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)

    # Remove label commands
    content = re.sub(r'\\label\{[^}]+\}', '', content)

    # Remove cross-references to appendices
    content = re.sub(r'Appendix~[A-Z]+', 'the appendix', content)

    # Remove citep/cite commands
    content = re.sub(r'\\citep?\{[^}]+\}', '', content)

    # Convert paragraph to bold
    content = re.sub(r'\\paragraph\{([^}]+)\}', r'\\textbf{\1} ', content)

    # Convert subsubsection to bold
    content = re.sub(r'\\subsubsection\{([^}]+)\}', r'\\textbf{\1}', content)

    return content.strip()


def generate_paper_latex(
    appendix: AppendixContent,
    doc_type: DocumentType8D,
    paper_number: str
) -> str:
    """
    Generate LaTeX paper from appendix content using 8D Document Type Framework.

    Implements the emergence chain from Appendix DDD:
    8D Coordinates → Structure → Style → Vocabulary
    """

    # Derive structure, style, vocabulary from 8D coordinates
    structure = doc_type.derive_structure()
    style = doc_type.derive_style()
    vocab = doc_type.derive_vocabulary()

    # Determine paper title from appendix
    paper_title = appendix.title.replace("LIT-META:", "").replace(":", "").strip()
    if not paper_title or paper_title == appendix.title:
        paper_title = f"Analysis of {appendix.category} Literature"

    # Generate abstract
    abstract = appendix.abstract if appendix.abstract else f"""
This paper examines {paper_title.lower()}. Drawing on the Evidence-Based Framework
for Economic and Social Behavior (EBF), we analyze the key findings and their
implications for behavioral science integration.
"""

    # Clean up keywords
    keywords = [k for k in appendix.key_concepts if k and len(k) > 2][:6]
    if not keywords:
        keywords = ["behavioral economics", "integration", "metascience"]

    # Build sections based on structure requirements
    sections_latex = []

    for i, (section_title, section_content) in enumerate(appendix.sections[:10]):
        clean_content = clean_latex_content(section_content)
        if len(clean_content) > 100:
            # Truncate very long sections
            if len(clean_content) > 6000:
                clean_content = clean_content[:6000] + "\n\n[Content continues in full appendix...]"

            sections_latex.append(f"""
%==============================================================================
\\section{{{section_title}}}
\\label{{sec:section{i+1}}}
%==============================================================================

{clean_content}
""")

    # Build style comment for LaTeX
    style_comment = f"""
% Generated using 8D Document Type Framework (Appendix DDD)
% Style Profile: {doc_type.name}
% 8D Coordinates: D1={doc_type.d1_knowledge}, D2={doc_type.d2_proximity}, D3={doc_type.d3_scope},
%                 D4={doc_type.d4_time}, D5={doc_type.d5_goal.value}, D6={doc_type.d6_context},
%                 D7={doc_type.d7_emotion}, D8={doc_type.d8_persistence}
%
% Structure (DT-5/DT-6): glossary={structure['glossary_required']}, theory={structure['theory_section']}
% Style (DT-7/DT-8): formal={style['formal_register']}, hedging={style['hedging_required']}
% Vocabulary (DT-9): {', '.join(vocab['connectives'][:3])}...
"""

    # Generate LaTeX document
    latex = f"""\\documentclass[12pt,a4paper]{{article}}
{style_comment}
% Packages
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{lmodern}}
\\usepackage[margin=2.5cm]{{geometry}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{booktabs}}
\\usepackage{{natbib}}
\\usepackage{{hyperref}}
\\usepackage{{setspace}}
\\usepackage{{enumitem}}
\\usepackage{{float}}

% Document settings
\\onehalfspacing
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{0.5em}}

% Title
\\title{{\\textbf{{{paper_title}}}}}
\\author{{Evidence-Based Framework Research Team\\thanks{{FehrAdvice \\& Partners AG. Correspondence: research@fehradvice.com}}\\\\[0.5em]\\small Working Paper WP-2026-{paper_number}}}
\\date{{January 2026}}

\\begin{{document}}

\\maketitle

\\begin{{abstract}}
{abstract.strip()}

\\medskip
\\textbf{{Keywords:}} {', '.join(keywords)}

\\medskip
\\textbf{{JEL Codes:}} A11, A14, D91
\\end{{abstract}}

\\newpage
\\tableofcontents
\\newpage

%==============================================================================
\\section{{Introduction}}
\\label{{sec:intro}}
%==============================================================================

This paper addresses a fundamental question:

\\begin{{quote}}
\\textit{{{appendix.fundamental_question if appendix.fundamental_question else "What are the key insights from this analysis?"}}}
\\end{{quote}}

{''.join(sections_latex)}

%==============================================================================
\\section{{Conclusion}}
\\label{{sec:conclusion}}
%==============================================================================

This analysis has examined {paper_title.lower()}. The evidence supports the
conclusion that integration of behavioral models requires addressing structural
barriers while leveraging new technological capabilities.

%==============================================================================
% References
%==============================================================================
\\bibliographystyle{{apalike}}

\\begin{{thebibliography}}{{99}}

\\bibitem[EBF, 2026]{{ebf2026}}
Evidence-Based Framework Research Team. (2026). \\textit{{Evidence-Based Framework for Economic and Social Behavior}}. FehrAdvice \\& Partners AG.

\\end{{thebibliography}}

%==============================================================================
% Appendix: 8D Document Type Specification
%==============================================================================
\\appendix
\\section{{8D Document Type Specification}}
\\label{{app:8d}}

This paper was generated using the 8D Document Type Framework (Appendix DDD/CCC).

\\textbf{{Style Profile:}} {doc_type.name}

\\textbf{{8D Coordinates:}}
\\begin{{itemize}}[nosep]
\\item $D_1$ (Knowledge): {doc_type.d1_knowledge}
\\item $D_2$ (Proximity): {doc_type.d2_proximity}
\\item $D_3$ (Scope): {doc_type.d3_scope}
\\item $D_4$ (Time): {doc_type.d4_time}
\\item $D_5$ (Goal): {doc_type.d5_goal.value}
\\item $D_6$ (Context): {doc_type.d6_context}
\\item $D_7$ (Emotion): {doc_type.d7_emotion}
\\item $D_8$ (Persistence): {doc_type.d8_persistence}
\\end{{itemize}}

\\textbf{{Derived Structure (DT-5/DT-6):}}
\\begin{{itemize}}[nosep]
\\item Glossary required: {structure['glossary_required']}
\\item Theory section: {structure['theory_section']}
\\item Full references: {structure['full_references']}
\\end{{itemize}}

\\textbf{{Derived Style (DT-7/DT-8):}}
\\begin{{itemize}}[nosep]
\\item Formal register: {style['formal_register']}
\\item Hedging required: {style['hedging_required']}
\\item Technical vocabulary: {style['technical_vocabulary']}
\\end{{itemize}}

\\section{{Relationship to EBF}}
\\label{{app:ebf}}

This working paper was automatically generated from the EBF documentation
(Category: {appendix.category}). For the complete analysis with all axioms and
formal proofs, see the full appendix in the EBF documentation.

\\end{{document}}
"""

    return latex


def compile_latex(tex_file: str, output_dir: str) -> bool:
    """Compile LaTeX to PDF."""
    try:
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file],
                capture_output=True,
                text=True,
                cwd=output_dir
            )

        pdf_file = Path(tex_file).with_suffix('.pdf')
        return pdf_file.exists()

    except FileNotFoundError:
        print("Warning: pdflatex not found. LaTeX file created but not compiled.")
        return False


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate academic paper from EBF appendix using 8D Document Type Framework"
    )
    parser.add_argument(
        "appendix",
        help="Path to appendix LaTeX file"
    )
    parser.add_argument(
        "--style", "-s",
        choices=list(STYLE_PROFILES.keys()),
        default=None,
        help="Style profile (8D coordinates). If not specified, uses category default."
    )
    parser.add_argument(
        "--output", "-o",
        default="papers",
        help="Output directory for generated paper"
    )
    parser.add_argument(
        "--number", "-n",
        help="Paper number (auto-generated if not specified)"
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Don't compile to PDF"
    )

    args = parser.parse_args()

    # Resolve paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    appendix_path = Path(args.appendix)
    if not appendix_path.is_absolute():
        appendix_path = repo_root / appendix_path

    output_dir = Path(args.output)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    # Check appendix exists
    if not appendix_path.exists():
        print(f"Error: Appendix file not found: {appendix_path}")
        sys.exit(1)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse appendix
    print(f"Parsing appendix: {appendix_path}")
    appendix = parse_appendix(str(appendix_path))
    print(f"  Title: {appendix.title}")
    print(f"  Category: {appendix.category}")
    print(f"  Sections: {len(appendix.sections)}")

    # Determine style profile
    if args.style:
        style_name = args.style
    else:
        # Use category default
        style_name = CATEGORY_DEFAULTS.get(appendix.category, "academic_standard")
        print(f"  Using category default style: {style_name}")

    doc_type = STYLE_PROFILES[style_name]
    print(f"\nUsing 8D profile: {doc_type.name}")
    print(f"  D1={doc_type.d1_knowledge}, D2={doc_type.d2_proximity}, D5={doc_type.d5_goal.value}")

    # Generate paper number
    paper_number = args.number or generate_paper_number()

    # Generate LaTeX
    print(f"\nGenerating paper WP-2026-{paper_number}...")
    latex = generate_paper_latex(appendix, doc_type, paper_number)

    # Determine output filename
    appendix_name = appendix_path.stem.split('_')[0]
    output_filename = f"WP_2026_{paper_number}_{appendix_name}_Generated.tex"
    output_path = output_dir / output_filename

    # Write LaTeX file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex)
    print(f"Written: {output_path}")

    # Compile to PDF
    if not args.no_compile:
        print("Compiling to PDF...")
        success = compile_latex(str(output_path), str(output_dir))
        if success:
            pdf_path = output_path.with_suffix('.pdf')
            print(f"PDF created: {pdf_path}")
        else:
            print("PDF compilation failed or pdflatex not available")

    # Clean up auxiliary files
    for ext in ['.aux', '.log', '.out', '.toc']:
        aux_file = output_path.with_suffix(ext)
        if aux_file.exists():
            aux_file.unlink()

    print("\nDone!")
    print(f"\n8D Emergence Chain Applied:")
    print(f"  8D Coordinates → Structure (DT-5/DT-6)")
    print(f"  8D Coordinates → Style (DT-7/DT-8) → Vocabulary (DT-9)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
