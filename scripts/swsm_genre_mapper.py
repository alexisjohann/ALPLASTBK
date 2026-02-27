#!/usr/bin/env python3
"""
SWSM 8D → Genre Mapper (E7)
Maps 8D target audience profiles to genre-specific constraints for text generation.

This is the unique feature of SWSM that doesn't exist in any other NLP tool.
It enables audience-adaptive text generation based on:
- D₁: Expertise level
- D₂: Domain proximity
- D₃: Scope (personal → societal)
- D₄: Available time
- D₅: Communication goal
- D₆: Context (internal → public)
- D₇: Emotional tone
- D₈: Persistence/archival

Based on:
- EBF 8D Algorithm (Appendix CCC/DDD)
- SWSM Axioms SWSM-8 (Genre Emergence), SWSM-9 (Style Percolation), SWSM-16 (Quantitative Bounds)

Usage:
    python scripts/swsm_genre_mapper.py --profile "0.8,0.7,0.6,0.7,G1,0.9,0.2,0.9"
    python scripts/swsm_genre_mapper.py --interactive
    python scripts/swsm_genre_mapper.py --profile-file profile.yaml --output constraints.yaml
"""

import argparse
import yaml
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import math


# ═══════════════════════════════════════════════════════════════════════════
# ENUMS: 8D DIMENSIONS AND GENRES
# ═══════════════════════════════════════════════════════════════════════════

class CommunicationGoal(Enum):
    """D₅: Communication Goals (G₁-G₇)"""
    G1_INFORM = "inform"           # Informieren
    G2_PERSUADE = "persuade"       # Überzeugen
    G3_INSTRUCT = "instruct"       # Handeln auslösen
    G4_ENTERTAIN = "entertain"     # Unterhalten
    G5_EXPRESS = "express"         # Ausdrücken
    G6_CONNECT = "connect"         # Verbinden
    G7_DOCUMENT = "document"       # Dokumentieren/Archivieren


class GenreType(Enum):
    """Document Genre Types"""
    # Academic
    SCIENTIFIC_PAPER = "scientific_paper"
    LITERATURE_REVIEW = "literature_review"
    THESIS = "thesis"
    CONFERENCE_PAPER = "conference_paper"

    # Business
    BUSINESS_REPORT = "business_report"
    EXECUTIVE_SUMMARY = "executive_summary"
    PROPOSAL = "proposal"
    MEMO = "memo"

    # Policy
    POLICY_BRIEF = "policy_brief"
    WHITE_PAPER = "white_paper"
    POSITION_PAPER = "position_paper"

    # Communication
    PRESS_RELEASE = "press_release"
    BLOG_POST = "blog_post"
    NEWSLETTER = "newsletter"

    # Technical
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    USER_MANUAL = "user_manual"
    API_DOCUMENTATION = "api_documentation"

    # EBF-specific
    EBF_APPENDIX = "ebf_appendix"
    EBF_CHAPTER = "ebf_chapter"
    CASE_STUDY = "case_study"

    # General
    ESSAY = "essay"
    LETTER = "letter"
    EMAIL = "email"


class Register(Enum):
    """Language Register (Formality)"""
    FROZEN = "frozen"           # Legal, liturgical
    FORMAL = "formal"           # Academic, official
    CONSULTATIVE = "consultative"  # Professional
    CASUAL = "casual"           # Informal
    INTIMATE = "intimate"       # Personal


# ═══════════════════════════════════════════════════════════════════════════
# DATA CLASSES: 8D PROFILE AND CONSTRAINTS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Profile8D:
    """8D Target Audience Profile"""
    D1_expertise: float          # 0-1: Laie → Expert
    D2_proximity: float          # 0-1: Fern → Gleiches Feld
    D3_scope: float              # 0-1: Persönlich → Gesellschaftlich
    D4_time: float               # 0-1: Wenig → Viel Zeit
    D5_goal: CommunicationGoal   # G1-G7
    D6_context: float            # 0-1: Intern → Öffentlich
    D7_emotion: float            # 0-1: Sachlich → Emotional
    D8_persistence: float        # 0-1: Kurzlebig → Archiv

    @classmethod
    def from_string(cls, s: str) -> 'Profile8D':
        """Parse from comma-separated string: '0.8,0.7,0.6,0.7,G1,0.9,0.2,0.9'"""
        parts = s.split(',')
        if len(parts) != 8:
            raise ValueError(f"Expected 8 values, got {len(parts)}")

        goal_map = {
            'G1': CommunicationGoal.G1_INFORM,
            'G2': CommunicationGoal.G2_PERSUADE,
            'G3': CommunicationGoal.G3_INSTRUCT,
            'G4': CommunicationGoal.G4_ENTERTAIN,
            'G5': CommunicationGoal.G5_EXPRESS,
            'G6': CommunicationGoal.G6_CONNECT,
            'G7': CommunicationGoal.G7_DOCUMENT,
        }

        return cls(
            D1_expertise=float(parts[0]),
            D2_proximity=float(parts[1]),
            D3_scope=float(parts[2]),
            D4_time=float(parts[3]),
            D5_goal=goal_map.get(parts[4].upper(), CommunicationGoal.G1_INFORM),
            D6_context=float(parts[5]),
            D7_emotion=float(parts[6]),
            D8_persistence=float(parts[7])
        )

    @classmethod
    def from_yaml(cls, data: dict) -> 'Profile8D':
        """Parse from YAML dictionary"""
        goal_map = {
            'inform': CommunicationGoal.G1_INFORM,
            'persuade': CommunicationGoal.G2_PERSUADE,
            'instruct': CommunicationGoal.G3_INSTRUCT,
            'entertain': CommunicationGoal.G4_ENTERTAIN,
            'express': CommunicationGoal.G5_EXPRESS,
            'connect': CommunicationGoal.G6_CONNECT,
            'document': CommunicationGoal.G7_DOCUMENT,
        }

        goal_str = data.get('D5_goal', 'inform').lower()
        goal = goal_map.get(goal_str, CommunicationGoal.G1_INFORM)

        return cls(
            D1_expertise=float(data.get('D1_expertise', 0.5)),
            D2_proximity=float(data.get('D2_proximity', 0.5)),
            D3_scope=float(data.get('D3_scope', 0.5)),
            D4_time=float(data.get('D4_time', 0.5)),
            D5_goal=goal,
            D6_context=float(data.get('D6_context', 0.5)),
            D7_emotion=float(data.get('D7_emotion', 0.5)),
            D8_persistence=float(data.get('D8_persistence', 0.5))
        )


@dataclass
class StructureConstraints:
    """L1-L2 Constraints: Document Structure"""
    genre: GenreType
    register: Register

    # Section structure (L2)
    required_sections: List[str] = field(default_factory=list)
    optional_sections: List[str] = field(default_factory=list)
    section_order: List[str] = field(default_factory=list)

    # Move structure (Swales)
    moves: List[Dict[str, Any]] = field(default_factory=list)

    # Length constraints
    min_sections: int = 1
    max_sections: int = 20

    # Metadata requirements
    requires_abstract: bool = False
    requires_keywords: bool = False
    requires_references: bool = False


@dataclass
class StyleConstraints:
    """L3-L5 Constraints: Style and Rhetoric"""
    # Paragraph constraints (L3)
    min_paragraphs_per_section: int = 2
    max_paragraphs_per_section: int = 10
    min_sentences_per_paragraph: int = 3
    max_sentences_per_paragraph: int = 10

    # Sentence constraints (L5)
    min_words_per_sentence: int = 10
    max_words_per_sentence: int = 35
    target_flesch_kincaid_min: float = 8.0
    target_flesch_kincaid_max: float = 16.0

    # Clause complexity (L4)
    max_clauses_per_sentence: int = 4
    max_embedding_depth: int = 3

    # Cohesion targets
    min_cohesion_score: float = 0.5
    target_conjunction_ratio: Tuple[float, float] = (2.0, 5.0)

    # Voice and perspective
    passive_voice_max: float = 0.35
    first_person_allowed: bool = True
    hedging_required: bool = False
    hedging_level: str = "moderate"  # none, low, moderate, high


@dataclass
class LexiconConstraints:
    """L6-L10 Constraints: Vocabulary and Expression"""
    # Technical terminology (L8)
    technical_term_ratio_min: float = 0.0
    technical_term_ratio_max: float = 0.30

    # Lexical sophistication
    min_lexical_diversity: float = 0.40
    max_lexical_diversity: float = 0.70

    # Word choice
    avoid_contractions: bool = False
    avoid_colloquialisms: bool = False
    prefer_latinate: bool = False  # Latinate vs. Anglo-Saxon

    # Nominalizations
    nominalization_level: str = "moderate"  # avoid, moderate, expected

    # Domain-specific vocabulary
    domain_vocabulary: List[str] = field(default_factory=list)

    # Forbidden words/phrases
    forbidden_words: List[str] = field(default_factory=list)

    # Formatting (L10)
    formatting_allowed: List[str] = field(default_factory=lambda: ['bold', 'italic'])


@dataclass
class SWSMConstraintBundle:
    """Complete constraint bundle for SWSM generation"""
    profile: Profile8D
    structure: StructureConstraints
    style: StyleConstraints
    lexicon: LexiconConstraints

    # Metadata
    inferred_genre: GenreType = GenreType.ESSAY
    confidence: float = 0.0

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML/JSON serialization"""
        return {
            'profile': {
                'D1_expertise': self.profile.D1_expertise,
                'D2_proximity': self.profile.D2_proximity,
                'D3_scope': self.profile.D3_scope,
                'D4_time': self.profile.D4_time,
                'D5_goal': self.profile.D5_goal.value,
                'D6_context': self.profile.D6_context,
                'D7_emotion': self.profile.D7_emotion,
                'D8_persistence': self.profile.D8_persistence
            },
            'inferred_genre': self.inferred_genre.value,
            'confidence': self.confidence,
            'structure': asdict(self.structure),
            'style': asdict(self.style),
            'lexicon': asdict(self.lexicon)
        }


# ═══════════════════════════════════════════════════════════════════════════
# GENRE TEMPLATES: Pre-defined constraint bundles per genre
# ═══════════════════════════════════════════════════════════════════════════

GENRE_TEMPLATES = {
    GenreType.SCIENTIFIC_PAPER: {
        'structure': {
            'required_sections': ['Abstract', 'Introduction', 'Methods', 'Results', 'Discussion', 'References'],
            'optional_sections': ['Acknowledgments', 'Appendix'],
            'moves': [
                {'name': 'Establish_Territory', 'obligatory': True},
                {'name': 'Establish_Niche', 'obligatory': True},
                {'name': 'Occupy_Niche', 'obligatory': True}
            ],
            'requires_abstract': True,
            'requires_keywords': True,
            'requires_references': True,
            'min_sections': 5,
            'max_sections': 10
        },
        'style': {
            'min_sentences_per_paragraph': 4,
            'max_sentences_per_paragraph': 8,
            'min_words_per_sentence': 15,
            'max_words_per_sentence': 35,
            'target_flesch_kincaid_min': 12.0,
            'target_flesch_kincaid_max': 18.0,
            'passive_voice_max': 0.30,
            'first_person_allowed': True,  # "We conducted..."
            'hedging_required': True,
            'hedging_level': 'high'
        },
        'lexicon': {
            'technical_term_ratio_min': 0.15,
            'technical_term_ratio_max': 0.35,
            'avoid_contractions': True,
            'avoid_colloquialisms': True,
            'prefer_latinate': True,
            'nominalization_level': 'expected'
        }
    },

    GenreType.EXECUTIVE_SUMMARY: {
        'structure': {
            'required_sections': ['Key Findings', 'Recommendations'],
            'optional_sections': ['Background', 'Next Steps'],
            'requires_abstract': False,
            'min_sections': 2,
            'max_sections': 4
        },
        'style': {
            'min_sentences_per_paragraph': 2,
            'max_sentences_per_paragraph': 5,
            'min_words_per_sentence': 12,
            'max_words_per_sentence': 25,
            'target_flesch_kincaid_min': 10.0,
            'target_flesch_kincaid_max': 14.0,
            'passive_voice_max': 0.20,
            'first_person_allowed': False,
            'hedging_required': False,
            'hedging_level': 'low'
        },
        'lexicon': {
            'technical_term_ratio_min': 0.05,
            'technical_term_ratio_max': 0.15,
            'avoid_contractions': True,
            'avoid_colloquialisms': True,
            'nominalization_level': 'moderate'
        }
    },

    GenreType.POLICY_BRIEF: {
        'structure': {
            'required_sections': ['Problem Statement', 'Evidence', 'Policy Options', 'Recommendation'],
            'optional_sections': ['Background', 'Implementation', 'Costs'],
            'min_sections': 4,
            'max_sections': 7
        },
        'style': {
            'min_sentences_per_paragraph': 3,
            'max_sentences_per_paragraph': 6,
            'min_words_per_sentence': 12,
            'max_words_per_sentence': 28,
            'target_flesch_kincaid_min': 10.0,
            'target_flesch_kincaid_max': 14.0,
            'passive_voice_max': 0.25,
            'first_person_allowed': False,
            'hedging_required': False,
            'hedging_level': 'moderate'
        },
        'lexicon': {
            'technical_term_ratio_min': 0.05,
            'technical_term_ratio_max': 0.20,
            'avoid_contractions': True,
            'avoid_colloquialisms': True,
            'nominalization_level': 'moderate'
        }
    },

    GenreType.BLOG_POST: {
        'structure': {
            'required_sections': ['Introduction', 'Main Content', 'Conclusion'],
            'optional_sections': ['Call to Action'],
            'min_sections': 3,
            'max_sections': 5
        },
        'style': {
            'min_sentences_per_paragraph': 2,
            'max_sentences_per_paragraph': 5,
            'min_words_per_sentence': 8,
            'max_words_per_sentence': 22,
            'target_flesch_kincaid_min': 6.0,
            'target_flesch_kincaid_max': 10.0,
            'passive_voice_max': 0.15,
            'first_person_allowed': True,
            'hedging_required': False,
            'hedging_level': 'none'
        },
        'lexicon': {
            'technical_term_ratio_min': 0.0,
            'technical_term_ratio_max': 0.10,
            'avoid_contractions': False,
            'avoid_colloquialisms': False,
            'nominalization_level': 'avoid'
        }
    },

    GenreType.EBF_APPENDIX: {
        'structure': {
            'required_sections': [
                'Header Block', 'Abstract', 'Fundamental Question',
                'Theory Section', 'Integration', 'Summary',
                'Glossary Link', 'References'
            ],
            'optional_sections': ['Worked Examples', 'Critical Foundations', 'Open Issues'],
            'requires_abstract': True,
            'requires_references': True,
            'min_sections': 8,
            'max_sections': 15
        },
        'style': {
            'min_sentences_per_paragraph': 3,
            'max_sentences_per_paragraph': 8,
            'min_words_per_sentence': 15,
            'max_words_per_sentence': 35,
            'target_flesch_kincaid_min': 12.0,
            'target_flesch_kincaid_max': 16.0,
            'passive_voice_max': 0.25,
            'first_person_allowed': True,
            'hedging_required': True,
            'hedging_level': 'high'
        },
        'lexicon': {
            'technical_term_ratio_min': 0.20,
            'technical_term_ratio_max': 0.40,
            'avoid_contractions': True,
            'avoid_colloquialisms': True,
            'prefer_latinate': True,
            'nominalization_level': 'expected',
            'domain_vocabulary': ['utility', 'complementarity', 'context', 'parameter', 'axiom']
        }
    }
}


# ═══════════════════════════════════════════════════════════════════════════
# GENRE MAPPER CLASS
# ═══════════════════════════════════════════════════════════════════════════

class GenreMapper:
    """
    Maps 8D profiles to genre constraints.
    Implements SWSM-8 (Genre Emergence) and SWSM-16 (Quantitative Bounds).
    """

    def __init__(self):
        """Initialize the Genre Mapper with templates and rules."""
        self.genre_templates = GENRE_TEMPLATES
        self._build_genre_profiles()

    def _build_genre_profiles(self):
        """Build typical 8D profiles for each genre (for classification)."""
        self.genre_profiles = {
            # Genre: (D1, D2, D3, D4, D5, D6, D7, D8)
            GenreType.SCIENTIFIC_PAPER: (0.90, 0.90, 0.70, 0.80, 'G1', 1.00, 0.10, 0.95),
            GenreType.LITERATURE_REVIEW: (0.85, 0.85, 0.65, 0.85, 'G1', 1.00, 0.10, 0.90),
            GenreType.THESIS: (0.80, 0.80, 0.60, 0.90, 'G1', 0.80, 0.15, 0.95),
            GenreType.BUSINESS_REPORT: (0.60, 0.50, 0.50, 0.50, 'G1', 0.70, 0.20, 0.70),
            GenreType.EXECUTIVE_SUMMARY: (0.50, 0.40, 0.60, 0.20, 'G1', 0.80, 0.25, 0.60),
            GenreType.PROPOSAL: (0.60, 0.50, 0.50, 0.40, 'G2', 0.70, 0.30, 0.65),
            GenreType.MEMO: (0.50, 0.70, 0.30, 0.20, 'G1', 0.20, 0.20, 0.30),
            GenreType.POLICY_BRIEF: (0.55, 0.40, 0.85, 0.30, 'G3', 1.00, 0.20, 0.75),
            GenreType.WHITE_PAPER: (0.70, 0.50, 0.75, 0.60, 'G2', 1.00, 0.15, 0.80),
            GenreType.PRESS_RELEASE: (0.30, 0.20, 0.70, 0.20, 'G1', 1.00, 0.35, 0.50),
            GenreType.BLOG_POST: (0.30, 0.20, 0.50, 0.30, 'G1', 1.00, 0.50, 0.30),
            GenreType.NEWSLETTER: (0.40, 0.30, 0.40, 0.25, 'G6', 0.60, 0.40, 0.40),
            GenreType.TECHNICAL_DOCUMENTATION: (0.75, 0.60, 0.40, 0.70, 'G3', 0.90, 0.05, 0.85),
            GenreType.USER_MANUAL: (0.40, 0.30, 0.30, 0.60, 'G3', 0.90, 0.10, 0.80),
            GenreType.EBF_APPENDIX: (0.85, 0.75, 0.60, 0.70, 'G1', 1.00, 0.15, 0.90),
            GenreType.EBF_CHAPTER: (0.75, 0.65, 0.55, 0.65, 'G1', 1.00, 0.20, 0.85),
            GenreType.CASE_STUDY: (0.65, 0.55, 0.55, 0.55, 'G1', 0.90, 0.25, 0.75),
            GenreType.ESSAY: (0.50, 0.40, 0.50, 0.50, 'G1', 0.80, 0.30, 0.60),
            GenreType.LETTER: (0.40, 0.30, 0.20, 0.30, 'G6', 0.30, 0.50, 0.40),
            GenreType.EMAIL: (0.40, 0.50, 0.20, 0.15, 'G1', 0.20, 0.30, 0.20)
        }

    def infer_genre(self, profile: Profile8D) -> Tuple[GenreType, float]:
        """
        Infer the most appropriate genre from an 8D profile.
        Uses Euclidean distance to find closest genre profile.

        Args:
            profile: The 8D profile

        Returns:
            Tuple of (GenreType, confidence)
        """
        min_distance = float('inf')
        best_genre = GenreType.ESSAY

        profile_vec = [
            profile.D1_expertise,
            profile.D2_proximity,
            profile.D3_scope,
            profile.D4_time,
            profile.D6_context,
            profile.D7_emotion,
            profile.D8_persistence
        ]

        for genre, genre_profile in self.genre_profiles.items():
            # Skip D5 (goal) in distance calculation - handled separately
            genre_vec = list(genre_profile[:4]) + list(genre_profile[5:])

            # Euclidean distance
            distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(profile_vec, genre_vec)))

            # Goal matching bonus
            genre_goal = genre_profile[4]
            if genre_goal == f"G{profile.D5_goal.value[-1]}".upper():
                distance *= 0.8  # 20% bonus for matching goal

            if distance < min_distance:
                min_distance = distance
                best_genre = genre

        # Convert distance to confidence (inverse, normalized)
        max_possible_distance = math.sqrt(7)  # 7 dimensions, max diff = 1 each
        confidence = 1 - (min_distance / max_possible_distance)

        return best_genre, confidence

    def compute_structure_constraints(self, profile: Profile8D, genre: GenreType) -> StructureConstraints:
        """
        Compute L1-L2 structure constraints based on 8D profile and genre.
        Implements SWSM-8 (Genre Emergence).
        """
        # Start with genre template
        template = self.genre_templates.get(genre, {}).get('structure', {})

        # Determine register based on D6 (context) and D1 (expertise)
        if profile.D6_context > 0.8 and profile.D1_expertise > 0.7:
            register = Register.FORMAL
        elif profile.D6_context > 0.6:
            register = Register.CONSULTATIVE
        elif profile.D6_context < 0.3:
            register = Register.CASUAL
        else:
            register = Register.CONSULTATIVE

        # Adjust section counts based on D4 (time)
        if profile.D4_time < 0.3:
            max_sections = min(template.get('max_sections', 5), 4)
        elif profile.D4_time > 0.7:
            max_sections = template.get('max_sections', 10)
        else:
            max_sections = template.get('max_sections', 7)

        return StructureConstraints(
            genre=genre,
            register=register,
            required_sections=template.get('required_sections', []),
            optional_sections=template.get('optional_sections', []),
            section_order=template.get('required_sections', []) + template.get('optional_sections', []),
            moves=template.get('moves', []),
            min_sections=template.get('min_sections', 1),
            max_sections=max_sections,
            requires_abstract=template.get('requires_abstract', False),
            requires_keywords=template.get('requires_keywords', False),
            requires_references=template.get('requires_references', False)
        )

    def compute_style_constraints(self, profile: Profile8D, genre: GenreType) -> StyleConstraints:
        """
        Compute L3-L5 style constraints based on 8D profile.
        Implements SWSM-16 (Quantitative Bounds).
        """
        template = self.genre_templates.get(genre, {}).get('style', {})

        # D4 (time) → sentence/paragraph length
        if profile.D4_time < 0.3:
            # Short: brief sentences, short paragraphs
            min_words = 8
            max_words = 20
            min_sent = 2
            max_sent = 5
        elif profile.D4_time > 0.7:
            # Long: complex sentences, detailed paragraphs
            min_words = 15
            max_words = 35
            min_sent = 4
            max_sent = 10
        else:
            # Medium
            min_words = 12
            max_words = 28
            min_sent = 3
            max_sent = 7

        # D1 (expertise) → Flesch-Kincaid target
        if profile.D1_expertise < 0.3:
            fk_min, fk_max = 6.0, 10.0
        elif profile.D1_expertise > 0.7:
            fk_min, fk_max = 12.0, 18.0
        else:
            fk_min, fk_max = 9.0, 14.0

        # D8 (persistence) → hedging
        if profile.D8_persistence > 0.8:
            hedging_required = True
            hedging_level = 'high'
        elif profile.D8_persistence > 0.5:
            hedging_required = True
            hedging_level = 'moderate'
        else:
            hedging_required = False
            hedging_level = 'low'

        # D7 (emotion) → passive voice, first person
        first_person = profile.D7_emotion > 0.3 or profile.D6_context < 0.5
        passive_max = 0.35 if profile.D7_emotion < 0.2 else 0.20

        return StyleConstraints(
            min_paragraphs_per_section=template.get('min_paragraphs_per_section', 2),
            max_paragraphs_per_section=template.get('max_paragraphs_per_section', 10),
            min_sentences_per_paragraph=min_sent,
            max_sentences_per_paragraph=max_sent,
            min_words_per_sentence=min_words,
            max_words_per_sentence=max_words,
            target_flesch_kincaid_min=fk_min,
            target_flesch_kincaid_max=fk_max,
            max_clauses_per_sentence=4 if profile.D1_expertise > 0.5 else 2,
            max_embedding_depth=3 if profile.D1_expertise > 0.7 else 2,
            min_cohesion_score=0.5,
            target_conjunction_ratio=(2.0, 5.0),
            passive_voice_max=passive_max,
            first_person_allowed=first_person,
            hedging_required=hedging_required,
            hedging_level=hedging_level
        )

    def compute_lexicon_constraints(self, profile: Profile8D, genre: GenreType) -> LexiconConstraints:
        """
        Compute L6-L10 lexicon constraints based on 8D profile.
        Implements SWSM-9 (Style Percolation).
        """
        template = self.genre_templates.get(genre, {}).get('lexicon', {})

        # D1 (expertise) → technical terms
        if profile.D1_expertise < 0.3:
            tech_min, tech_max = 0.0, 0.05
        elif profile.D1_expertise > 0.7:
            tech_min, tech_max = 0.15, 0.40
        else:
            tech_min, tech_max = 0.05, 0.20

        # D6 (context) → formality markers
        avoid_contractions = profile.D6_context > 0.5
        avoid_colloquialisms = profile.D6_context > 0.6

        # D1 + D8 → nominalizations
        if profile.D1_expertise > 0.7 and profile.D8_persistence > 0.7:
            nom_level = 'expected'
        elif profile.D1_expertise < 0.4:
            nom_level = 'avoid'
        else:
            nom_level = 'moderate'

        # D1 (expertise) → vocabulary sophistication
        if profile.D1_expertise < 0.3:
            prefer_latinate = False
            min_diversity, max_diversity = 0.35, 0.50
        elif profile.D1_expertise > 0.7:
            prefer_latinate = True
            min_diversity, max_diversity = 0.50, 0.70
        else:
            prefer_latinate = False
            min_diversity, max_diversity = 0.40, 0.60

        return LexiconConstraints(
            technical_term_ratio_min=tech_min,
            technical_term_ratio_max=tech_max,
            min_lexical_diversity=min_diversity,
            max_lexical_diversity=max_diversity,
            avoid_contractions=avoid_contractions,
            avoid_colloquialisms=avoid_colloquialisms,
            prefer_latinate=prefer_latinate,
            nominalization_level=nom_level,
            domain_vocabulary=template.get('domain_vocabulary', []),
            forbidden_words=template.get('forbidden_words', []),
            formatting_allowed=['bold', 'italic'] if profile.D8_persistence > 0.5 else ['bold', 'italic', 'emoji']
        )

    def map_profile_to_constraints(self, profile: Profile8D) -> SWSMConstraintBundle:
        """
        Main method: Map an 8D profile to a complete SWSM constraint bundle.

        Args:
            profile: The 8D target audience profile

        Returns:
            Complete SWSMConstraintBundle ready for generation
        """
        # Step 1: Infer genre (SWSM-8)
        genre, confidence = self.infer_genre(profile)

        # Step 2: Compute structure constraints (L1-L2)
        structure = self.compute_structure_constraints(profile, genre)

        # Step 3: Compute style constraints (L3-L5)
        style = self.compute_style_constraints(profile, genre)

        # Step 4: Compute lexicon constraints (L6-L10)
        lexicon = self.compute_lexicon_constraints(profile, genre)

        return SWSMConstraintBundle(
            profile=profile,
            structure=structure,
            style=style,
            lexicon=lexicon,
            inferred_genre=genre,
            confidence=confidence
        )


# ═══════════════════════════════════════════════════════════════════════════
# 8D PROFILE INFERENCER (Reverse: Text → 8D)
# ═══════════════════════════════════════════════════════════════════════════

class ProfileInferencer:
    """
    Infer 8D profile from existing text.
    Useful for analyzing existing documents.
    """

    def __init__(self, language: str = "en"):
        self.language = language

    def infer_from_text(self, text: str, metadata: Optional[dict] = None) -> Profile8D:
        """
        Infer 8D profile from text content and metadata.

        Args:
            text: The document text
            metadata: Optional metadata (genre, publication venue, etc.)

        Returns:
            Inferred Profile8D
        """
        # This is a simplified implementation
        # A full implementation would use ML models

        words = text.lower().split()
        sentences = text.split('.')

        # D1: Estimate expertise from vocabulary
        technical_indicators = {
            'coefficient', 'parameter', 'hypothesis', 'methodology', 'empirical',
            'significant', 'correlation', 'regression', 'variable', 'analysis'
        }
        tech_count = sum(1 for w in words if w in technical_indicators)
        d1 = min(1.0, tech_count / (len(words) * 0.05 + 1))

        # D4: Estimate time from length
        word_count = len(words)
        if word_count < 500:
            d4 = 0.2
        elif word_count < 2000:
            d4 = 0.4
        elif word_count < 5000:
            d4 = 0.6
        else:
            d4 = 0.8

        # D6: Estimate context from formality
        contraction_count = sum(1 for w in words if "'" in w or "n't" in w)
        d6 = 1.0 - min(1.0, contraction_count / (len(words) * 0.02 + 1))

        # D7: Estimate emotion from adjectives/exclamations
        emotion_indicators = {'!', 'amazing', 'terrible', 'wonderful', 'awful', 'love', 'hate'}
        emotion_count = sum(1 for w in words if w.rstrip('!.,') in emotion_indicators)
        emotion_count += text.count('!')
        d7 = min(1.0, emotion_count / 10)

        # D8: Estimate persistence from hedging
        hedge_words = {'may', 'might', 'could', 'possibly', 'suggests', 'appears', 'seems'}
        hedge_count = sum(1 for w in words if w in hedge_words)
        d8 = min(1.0, hedge_count / (len(sentences) * 0.3 + 1)) + 0.3

        # D5: Default to inform
        d5 = CommunicationGoal.G1_INFORM

        return Profile8D(
            D1_expertise=d1,
            D2_proximity=0.5,  # Hard to infer
            D3_scope=0.5,      # Hard to infer
            D4_time=d4,
            D5_goal=d5,
            D6_context=d6,
            D7_emotion=d7,
            D8_persistence=d8
        )


# ═══════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="SWSM 8D → Genre Mapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From profile string (D1,D2,D3,D4,D5,D6,D7,D8)
  python swsm_genre_mapper.py --profile "0.85,0.75,0.60,0.70,G1,0.90,0.15,0.90"

  # From YAML file
  python swsm_genre_mapper.py --profile-file audience.yaml --output constraints.yaml

  # Interactive mode
  python swsm_genre_mapper.py --interactive

  # Infer profile from existing text
  python swsm_genre_mapper.py --infer-from-text document.txt
        """
    )
    parser.add_argument("--profile", "-p", help="8D profile as comma-separated string")
    parser.add_argument("--profile-file", help="8D profile as YAML file")
    parser.add_argument("--output", "-o", help="Output file (YAML or JSON)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--infer-from-text", help="Infer profile from text file")
    parser.add_argument("--format", choices=["yaml", "json", "text"], default="text")

    args = parser.parse_args()

    mapper = GenreMapper()

    if args.interactive:
        profile = interactive_profile_builder()
    elif args.profile:
        profile = Profile8D.from_string(args.profile)
    elif args.profile_file:
        with open(args.profile_file, 'r') as f:
            data = yaml.safe_load(f)
            profile = Profile8D.from_yaml(data)
    elif args.infer_from_text:
        with open(args.infer_from_text, 'r') as f:
            text = f.read()
        inferencer = ProfileInferencer()
        profile = inferencer.infer_from_text(text)
        print("Inferred 8D Profile:")
        print_profile(profile)
    else:
        # Demo profile
        profile = Profile8D(
            D1_expertise=0.85,
            D2_proximity=0.75,
            D3_scope=0.60,
            D4_time=0.70,
            D5_goal=CommunicationGoal.G1_INFORM,
            D6_context=0.90,
            D7_emotion=0.15,
            D8_persistence=0.90
        )
        print("Using demo profile (scientific paper):")
        print_profile(profile)

    # Map to constraints
    bundle = mapper.map_profile_to_constraints(profile)

    # Output
    if args.output:
        ext = args.output.split('.')[-1]
        with open(args.output, 'w') as f:
            if ext == 'json':
                json.dump(bundle.to_dict(), f, indent=2, default=str)
            else:
                yaml.dump(bundle.to_dict(), f, default_flow_style=False, allow_unicode=True)
        print(f"Constraints saved to {args.output}")
    elif args.format == "json":
        print(json.dumps(bundle.to_dict(), indent=2, default=str))
    elif args.format == "yaml":
        print(yaml.dump(bundle.to_dict(), default_flow_style=False, allow_unicode=True))
    else:
        print_bundle(bundle)


def print_profile(profile: Profile8D):
    """Pretty-print 8D profile"""
    print(f"""
┌─────────────────────────────────────────────────────────────┐
│  8D PROFILE                                                 │
├─────────────────────────────────────────────────────────────┤
│  D₁ Expertise:    {profile.D1_expertise:.2f}  {'█' * int(profile.D1_expertise * 20):<20}  │
│  D₂ Proximity:    {profile.D2_proximity:.2f}  {'█' * int(profile.D2_proximity * 20):<20}  │
│  D₃ Scope:        {profile.D3_scope:.2f}  {'█' * int(profile.D3_scope * 20):<20}  │
│  D₄ Time:         {profile.D4_time:.2f}  {'█' * int(profile.D4_time * 20):<20}  │
│  D₅ Goal:         {profile.D5_goal.value:<12}                          │
│  D₆ Context:      {profile.D6_context:.2f}  {'█' * int(profile.D6_context * 20):<20}  │
│  D₇ Emotion:      {profile.D7_emotion:.2f}  {'█' * int(profile.D7_emotion * 20):<20}  │
│  D₈ Persistence:  {profile.D8_persistence:.2f}  {'█' * int(profile.D8_persistence * 20):<20}  │
└─────────────────────────────────────────────────────────────┘
""")


def print_bundle(bundle: SWSMConstraintBundle):
    """Pretty-print constraint bundle"""
    print("=" * 70)
    print("SWSM CONSTRAINT BUNDLE")
    print("=" * 70)

    print(f"\n📚 INFERRED GENRE: {bundle.inferred_genre.value.upper()}")
    print(f"   Confidence: {bundle.confidence:.1%}")

    print("\n" + "-" * 70)
    print("📋 STRUCTURE CONSTRAINTS (L1-L2)")
    print("-" * 70)
    s = bundle.structure
    print(f"  Register: {s.register.value}")
    print(f"  Required Sections: {', '.join(s.required_sections[:5])}...")
    print(f"  Section Count: {s.min_sections}-{s.max_sections}")
    print(f"  Requires Abstract: {s.requires_abstract}")
    print(f"  Requires References: {s.requires_references}")

    print("\n" + "-" * 70)
    print("✍️  STYLE CONSTRAINTS (L3-L5)")
    print("-" * 70)
    st = bundle.style
    print(f"  Sentences/Paragraph: {st.min_sentences_per_paragraph}-{st.max_sentences_per_paragraph}")
    print(f"  Words/Sentence: {st.min_words_per_sentence}-{st.max_words_per_sentence}")
    print(f"  Flesch-Kincaid Target: {st.target_flesch_kincaid_min}-{st.target_flesch_kincaid_max}")
    print(f"  Passive Voice Max: {st.passive_voice_max:.0%}")
    print(f"  First Person: {'Allowed' if st.first_person_allowed else 'Avoid'}")
    print(f"  Hedging: {st.hedging_level}")

    print("\n" + "-" * 70)
    print("📖 LEXICON CONSTRAINTS (L6-L10)")
    print("-" * 70)
    l = bundle.lexicon
    print(f"  Technical Terms: {l.technical_term_ratio_min:.0%}-{l.technical_term_ratio_max:.0%}")
    print(f"  Lexical Diversity: {l.min_lexical_diversity:.2f}-{l.max_lexical_diversity:.2f}")
    print(f"  Contractions: {'Avoid' if l.avoid_contractions else 'OK'}")
    print(f"  Colloquialisms: {'Avoid' if l.avoid_colloquialisms else 'OK'}")
    print(f"  Nominalizations: {l.nominalization_level}")

    print("\n" + "=" * 70)


def interactive_profile_builder() -> Profile8D:
    """Interactive 8D profile builder"""
    print("\n" + "=" * 70)
    print("INTERACTIVE 8D PROFILE BUILDER")
    print("=" * 70)
    print("\nAnswer each question on a scale of 0.0 to 1.0")
    print("(or press Enter for default 0.5)\n")

    def ask(prompt: str, default: float = 0.5) -> float:
        response = input(f"{prompt} [{default}]: ").strip()
        if not response:
            return default
        try:
            val = float(response)
            return max(0.0, min(1.0, val))
        except ValueError:
            return default

    d1 = ask("D₁ Expertise (0=Laie, 1=Expert)")
    d2 = ask("D₂ Proximity (0=Fachfremd, 1=Gleiches Feld)")
    d3 = ask("D₃ Scope (0=Persönlich, 1=Gesellschaftlich)")
    d4 = ask("D₄ Time (0=Wenig Zeit, 1=Viel Zeit)")

    print("\nD₅ Goal:")
    print("  1. Inform (G1)")
    print("  2. Persuade (G2)")
    print("  3. Instruct (G3)")
    print("  4. Entertain (G4)")
    print("  5. Express (G5)")
    print("  6. Connect (G6)")
    print("  7. Document (G7)")
    goal_choice = input("Choose 1-7 [1]: ").strip() or "1"
    goal_map = {
        "1": CommunicationGoal.G1_INFORM,
        "2": CommunicationGoal.G2_PERSUADE,
        "3": CommunicationGoal.G3_INSTRUCT,
        "4": CommunicationGoal.G4_ENTERTAIN,
        "5": CommunicationGoal.G5_EXPRESS,
        "6": CommunicationGoal.G6_CONNECT,
        "7": CommunicationGoal.G7_DOCUMENT
    }
    d5 = goal_map.get(goal_choice, CommunicationGoal.G1_INFORM)

    d6 = ask("D₆ Context (0=Intern, 1=Öffentlich)")
    d7 = ask("D₇ Emotion (0=Sachlich, 1=Emotional)")
    d8 = ask("D₈ Persistence (0=Kurzlebig, 1=Archiv)")

    return Profile8D(
        D1_expertise=d1,
        D2_proximity=d2,
        D3_scope=d3,
        D4_time=d4,
        D5_goal=d5,
        D6_context=d6,
        D7_emotion=d7,
        D8_persistence=d8
    )


if __name__ == "__main__":
    main()
