#!/usr/bin/env python3
"""
SWSM Move Planner (E8)
======================

Plans document structure by generating move sequences based on genre.

Connects:
- Genre (from E7 8D mapping) → Move Sequence
- Moves → RST Relations (via E4 bridge)
- Moves → SFL Constraints (style, register)

Theoretical Foundation:
- Swales (1990): Genre Analysis and the CARS Model
- Bhatia (1993): Analysing Genre
- Martin (1992): English Text

Move = A functional unit of text that achieves a communicative purpose
       within a genre (e.g., "Establishing Territory" in an Introduction)

Implements SWSM Axioms:
- SWSM-8: Genre Emergence (8D → Genre → Constraints)
- SWSM-12: Domain Specialization (Genre → Moves)

Author: SWSM Framework / EBF
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS
# =============================================================================

class GenreType(Enum):
    """Document genres with distinct move structures."""
    # Academic
    SCIENTIFIC_PAPER = "scientific_paper"
    RESEARCH_PROPOSAL = "research_proposal"
    LITERATURE_REVIEW = "literature_review"
    THESIS_CHAPTER = "thesis_chapter"

    # Professional
    POLICY_BRIEF = "policy_brief"
    EXECUTIVE_SUMMARY = "executive_summary"
    BUSINESS_REPORT = "business_report"
    CONSULTING_MEMO = "consulting_memo"

    # EBF-specific
    EBF_APPENDIX = "ebf_appendix"
    EBF_CASE_STUDY = "ebf_case_study"
    INTERVENTION_DESIGN = "intervention_design"

    # Communication
    BLOG_POST = "blog_post"
    PRESS_RELEASE = "press_release"
    NEWSLETTER = "newsletter"


class MoveStatus(Enum):
    """Status of a move in the plan."""
    OBLIGATORY = "obligatory"      # Must be included
    OPTIONAL = "optional"          # May be included
    CONDITIONAL = "conditional"    # Include if condition met
    RECURSIVE = "recursive"        # Can repeat


class RSTRelationHint(Enum):
    """Suggested RST relations for move transitions."""
    ELABORATION = "elaboration"
    BACKGROUND = "background"
    EVIDENCE = "evidence"
    CONTRAST = "contrast"
    CAUSE = "cause"
    RESULT = "result"
    PURPOSE = "purpose"
    SEQUENCE = "sequence"
    PREPARATION = "preparation"
    SUMMARY = "summary"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class MoveConstraints:
    """Constraints for a single move."""
    # Length constraints
    min_sentences: int = 1
    max_sentences: int = 10
    min_words: Optional[int] = None
    max_words: Optional[int] = None

    # Structure constraints
    recommended_rst: List[RSTRelationHint] = field(default_factory=list)
    allowed_submoves: List[str] = field(default_factory=list)

    # Style constraints
    register: str = "formal"  # formal | neutral | informal
    hedging_required: bool = False
    citations_expected: bool = False

    # Content constraints
    required_elements: List[str] = field(default_factory=list)
    optional_elements: List[str] = field(default_factory=list)


@dataclass
class Move:
    """A single move in a genre structure."""
    move_id: str
    name: str
    description: str
    purpose: str                    # Communicative purpose
    status: MoveStatus = MoveStatus.OBLIGATORY
    order: int = 0                  # Position in sequence
    parent_section: Optional[str] = None

    # Constraints
    constraints: MoveConstraints = field(default_factory=MoveConstraints)

    # Strategies (alternative realizations)
    strategies: List[str] = field(default_factory=list)

    # Connections
    typical_follows: List[str] = field(default_factory=list)
    typical_precedes: List[str] = field(default_factory=list)
    transition_rst: Optional[RSTRelationHint] = None


@dataclass
class Section:
    """A section containing multiple moves."""
    section_id: str
    name: str
    moves: List[Move] = field(default_factory=list)
    order: int = 0


@dataclass
class DocumentPlan:
    """Complete document plan with sections and moves."""
    genre: GenreType
    title: Optional[str] = None
    sections: List[Section] = field(default_factory=list)

    # Global constraints
    total_min_words: Optional[int] = None
    total_max_words: Optional[int] = None
    style_profile: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    generated_from: str = "genre_template"  # genre_template | 8d_profile

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'genre': self.genre.value,
            'title': self.title,
            'generated_from': self.generated_from,
            'global_constraints': {
                'min_words': self.total_min_words,
                'max_words': self.total_max_words,
                'style': self.style_profile
            },
            'sections': [
                {
                    'section_id': s.section_id,
                    'name': s.name,
                    'order': s.order,
                    'moves': [
                        {
                            'move_id': m.move_id,
                            'name': m.name,
                            'purpose': m.purpose,
                            'status': m.status.value,
                            'order': m.order,
                            'strategies': m.strategies,
                            'constraints': {
                                'sentences': f"{m.constraints.min_sentences}-{m.constraints.max_sentences}",
                                'register': m.constraints.register,
                                'hedging': m.constraints.hedging_required,
                                'citations': m.constraints.citations_expected,
                                'rst_hints': [r.value for r in m.constraints.recommended_rst]
                            }
                        }
                        for m in s.moves
                    ]
                }
                for s in self.sections
            ],
            'move_sequence': self.get_move_sequence()
        }

    def get_move_sequence(self) -> List[str]:
        """Get flat list of move IDs in order."""
        moves = []
        for section in sorted(self.sections, key=lambda s: s.order):
            for move in sorted(section.moves, key=lambda m: m.order):
                moves.append(move.move_id)
        return moves

    def get_total_moves(self) -> int:
        """Count total moves."""
        return sum(len(s.moves) for s in self.sections)


# =============================================================================
# GENRE TEMPLATES
# =============================================================================

GENRE_TEMPLATES: Dict[GenreType, Dict[str, Any]] = {

    # =========================================================================
    # SCIENTIFIC PAPER (Swales CARS + IMRAD)
    # =========================================================================
    GenreType.SCIENTIFIC_PAPER: {
        'name': "Scientific Research Paper",
        'source': "Swales (1990), IMRAD structure",
        'total_words': (4000, 8000),
        'style': {'register': 'formal', 'hedging': True, 'citations': True},
        'sections': [
            {
                'id': 'abstract',
                'name': 'Abstract',
                'moves': [
                    {'id': 'ABS-1', 'name': 'Background', 'purpose': 'Situate the research',
                     'status': 'obligatory', 'sentences': (1, 2)},
                    {'id': 'ABS-2', 'name': 'Purpose', 'purpose': 'State the aim',
                     'status': 'obligatory', 'sentences': (1, 1)},
                    {'id': 'ABS-3', 'name': 'Method', 'purpose': 'Summarize approach',
                     'status': 'obligatory', 'sentences': (1, 2)},
                    {'id': 'ABS-4', 'name': 'Results', 'purpose': 'Key findings',
                     'status': 'obligatory', 'sentences': (1, 2)},
                    {'id': 'ABS-5', 'name': 'Conclusion', 'purpose': 'Implications',
                     'status': 'optional', 'sentences': (1, 1)}
                ]
            },
            {
                'id': 'introduction',
                'name': 'Introduction',
                'moves': [
                    {'id': 'INT-M1', 'name': 'Establishing Territory',
                     'purpose': 'Show importance of research area',
                     'status': 'obligatory', 'sentences': (3, 8),
                     'strategies': ['Claiming centrality', 'Making topic generalizations',
                                  'Reviewing previous research'],
                     'rst': ['background', 'elaboration']},
                    {'id': 'INT-M2', 'name': 'Establishing Niche',
                     'purpose': 'Indicate gap in current research',
                     'status': 'obligatory', 'sentences': (2, 5),
                     'strategies': ['Counter-claiming', 'Indicating gap',
                                  'Question-raising', 'Continuing tradition'],
                     'rst': ['contrast', 'preparation']},
                    {'id': 'INT-M3', 'name': 'Occupying Niche',
                     'purpose': 'Present the current research',
                     'status': 'obligatory', 'sentences': (2, 5),
                     'strategies': ['Announcing research', 'Announcing findings',
                                  'Indicating structure'],
                     'rst': ['purpose', 'preparation']}
                ]
            },
            {
                'id': 'methods',
                'name': 'Methods',
                'moves': [
                    {'id': 'MTH-1', 'name': 'Overview', 'purpose': 'Describe overall approach',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'MTH-2', 'name': 'Participants/Materials',
                     'purpose': 'Describe sample/data',
                     'status': 'conditional', 'sentences': (2, 6)},
                    {'id': 'MTH-3', 'name': 'Procedure', 'purpose': 'Detail steps taken',
                     'status': 'obligatory', 'sentences': (3, 10),
                     'rst': ['sequence']},
                    {'id': 'MTH-4', 'name': 'Analysis', 'purpose': 'Describe analytical approach',
                     'status': 'optional', 'sentences': (2, 5)}
                ]
            },
            {
                'id': 'results',
                'name': 'Results',
                'moves': [
                    {'id': 'RES-1', 'name': 'Preparatory', 'purpose': 'Set up results presentation',
                     'status': 'optional', 'sentences': (1, 2)},
                    {'id': 'RES-2', 'name': 'Report Results', 'purpose': 'Present findings',
                     'status': 'obligatory', 'sentences': (5, 20),
                     'recursive': True,
                     'rst': ['elaboration', 'evidence']},
                    {'id': 'RES-3', 'name': 'Comment on Results', 'purpose': 'Interpret findings',
                     'status': 'optional', 'sentences': (2, 5)}
                ]
            },
            {
                'id': 'discussion',
                'name': 'Discussion',
                'moves': [
                    {'id': 'DIS-1', 'name': 'Consolidation', 'purpose': 'Summarize key findings',
                     'status': 'obligatory', 'sentences': (2, 5),
                     'rst': ['summary']},
                    {'id': 'DIS-2', 'name': 'Comparison', 'purpose': 'Compare with prior work',
                     'status': 'obligatory', 'sentences': (3, 8),
                     'rst': ['contrast', 'elaboration']},
                    {'id': 'DIS-3', 'name': 'Explanation', 'purpose': 'Explain findings',
                     'status': 'optional', 'sentences': (2, 6),
                     'rst': ['cause', 'result']},
                    {'id': 'DIS-4', 'name': 'Implications', 'purpose': 'Discuss significance',
                     'status': 'obligatory', 'sentences': (2, 5)},
                    {'id': 'DIS-5', 'name': 'Limitations', 'purpose': 'Acknowledge constraints',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'DIS-6', 'name': 'Future Research', 'purpose': 'Suggest next steps',
                     'status': 'optional', 'sentences': (1, 3)}
                ]
            },
            {
                'id': 'conclusion',
                'name': 'Conclusion',
                'moves': [
                    {'id': 'CON-1', 'name': 'Summary', 'purpose': 'Recap main points',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'CON-2', 'name': 'Final Statement', 'purpose': 'End with impact',
                     'status': 'optional', 'sentences': (1, 2)}
                ]
            }
        ]
    },

    # =========================================================================
    # POLICY BRIEF
    # =========================================================================
    GenreType.POLICY_BRIEF: {
        'name': "Policy Brief",
        'source': "FehrAdvice Practice",
        'total_words': (1500, 3000),
        'style': {'register': 'formal', 'hedging': False, 'citations': False},
        'sections': [
            {
                'id': 'executive_summary',
                'name': 'Executive Summary',
                'moves': [
                    {'id': 'ES-1', 'name': 'Key Message', 'purpose': 'State main recommendation',
                     'status': 'obligatory', 'sentences': (1, 2)},
                    {'id': 'ES-2', 'name': 'Context', 'purpose': 'Brief background',
                     'status': 'obligatory', 'sentences': (1, 2)},
                    {'id': 'ES-3', 'name': 'Call to Action', 'purpose': 'What should be done',
                     'status': 'obligatory', 'sentences': (1, 1)}
                ]
            },
            {
                'id': 'problem',
                'name': 'Problem Statement',
                'moves': [
                    {'id': 'PRB-1', 'name': 'Issue Definition', 'purpose': 'Define the problem',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'PRB-2', 'name': 'Scope', 'purpose': 'Who is affected, how much',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'PRB-3', 'name': 'Urgency', 'purpose': 'Why act now',
                     'status': 'optional', 'sentences': (1, 2)}
                ]
            },
            {
                'id': 'evidence',
                'name': 'Evidence',
                'moves': [
                    {'id': 'EVD-1', 'name': 'Key Data', 'purpose': 'Present supporting data',
                     'status': 'obligatory', 'sentences': (3, 6),
                     'rst': ['evidence']},
                    {'id': 'EVD-2', 'name': 'Case Example', 'purpose': 'Illustrate with example',
                     'status': 'optional', 'sentences': (2, 4)}
                ]
            },
            {
                'id': 'options',
                'name': 'Policy Options',
                'moves': [
                    {'id': 'OPT-1', 'name': 'Option A', 'purpose': 'First policy option',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'OPT-2', 'name': 'Option B', 'purpose': 'Second policy option',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'OPT-3', 'name': 'Comparison', 'purpose': 'Compare options',
                     'status': 'optional', 'sentences': (2, 4),
                     'rst': ['contrast']}
                ]
            },
            {
                'id': 'recommendation',
                'name': 'Recommendation',
                'moves': [
                    {'id': 'REC-1', 'name': 'Preferred Option', 'purpose': 'State recommendation',
                     'status': 'obligatory', 'sentences': (1, 2)},
                    {'id': 'REC-2', 'name': 'Rationale', 'purpose': 'Justify choice',
                     'status': 'obligatory', 'sentences': (2, 4),
                     'rst': ['cause', 'evidence']},
                    {'id': 'REC-3', 'name': 'Implementation', 'purpose': 'How to implement',
                     'status': 'obligatory', 'sentences': (2, 4),
                     'rst': ['sequence']}
                ]
            }
        ]
    },

    # =========================================================================
    # EBF APPENDIX
    # =========================================================================
    GenreType.EBF_APPENDIX: {
        'name': "EBF Framework Appendix",
        'source': "EBF Template",
        'total_words': (3000, 8000),
        'style': {'register': 'formal', 'hedging': True, 'citations': True},
        'sections': [
            {
                'id': 'header',
                'name': 'Header Block',
                'moves': [
                    {'id': 'HDR-1', 'name': 'Metadata', 'purpose': 'Category, version, deps',
                     'status': 'obligatory', 'sentences': (1, 1)},
                    {'id': 'HDR-2', 'name': 'Cross-Reference Map', 'purpose': 'Link to other appendices',
                     'status': 'obligatory', 'sentences': (1, 1)}
                ]
            },
            {
                'id': 'abstract',
                'name': 'Abstract',
                'moves': [
                    {'id': 'ABS-1', 'name': 'Quick Reference', 'purpose': 'Key concepts at a glance',
                     'status': 'obligatory', 'sentences': (3, 6)},
                    {'id': 'ABS-2', 'name': 'Fundamental Question', 'purpose': 'Core question addressed',
                     'status': 'obligatory', 'sentences': (1, 2)}
                ]
            },
            {
                'id': 'theory',
                'name': 'Theory',
                'moves': [
                    {'id': 'THY-1', 'name': 'Core Theory', 'purpose': 'Main theoretical content',
                     'status': 'obligatory', 'sentences': (10, 30)},
                    {'id': 'THY-2', 'name': 'Axioms', 'purpose': 'Formal axiom statements',
                     'status': 'conditional', 'sentences': (5, 15)},
                    {'id': 'THY-3', 'name': 'Derivations', 'purpose': 'Mathematical derivations',
                     'status': 'optional', 'sentences': (5, 20)}
                ]
            },
            {
                'id': 'results',
                'name': 'Results',
                'moves': [
                    {'id': 'RES-1', 'name': 'Main Results', 'purpose': 'Key findings/propositions',
                     'status': 'obligatory', 'sentences': (5, 15)},
                    {'id': 'RES-2', 'name': 'Worked Examples', 'purpose': 'Illustrative examples',
                     'status': 'conditional', 'sentences': (5, 20)}
                ]
            },
            {
                'id': 'integration',
                'name': 'Integration',
                'moves': [
                    {'id': 'INT-1', 'name': '10C Connection', 'purpose': 'Link to 10C framework',
                     'status': 'obligatory', 'sentences': (3, 8)},
                    {'id': 'INT-2', 'name': 'Cross-Appendix Links', 'purpose': 'Connections to other appendices',
                     'status': 'obligatory', 'sentences': (2, 5)}
                ]
            },
            {
                'id': 'summary',
                'name': 'Summary',
                'moves': [
                    {'id': 'SUM-1', 'name': 'Key Takeaways', 'purpose': 'Main points',
                     'status': 'obligatory', 'sentences': (3, 6)},
                    {'id': 'SUM-2', 'name': 'Open Issues', 'purpose': 'Unresolved questions',
                     'status': 'optional', 'sentences': (2, 4)}
                ]
            }
        ]
    },

    # =========================================================================
    # EXECUTIVE SUMMARY
    # =========================================================================
    GenreType.EXECUTIVE_SUMMARY: {
        'name': "Executive Summary",
        'source': "Business Practice",
        'total_words': (300, 800),
        'style': {'register': 'formal', 'hedging': False, 'citations': False},
        'sections': [
            {
                'id': 'main',
                'name': 'Executive Summary',
                'moves': [
                    {'id': 'EXS-1', 'name': 'Situation', 'purpose': 'Current state/context',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'EXS-2', 'name': 'Complication', 'purpose': 'The problem/challenge',
                     'status': 'obligatory', 'sentences': (2, 3)},
                    {'id': 'EXS-3', 'name': 'Resolution', 'purpose': 'Recommended action',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'EXS-4', 'name': 'Key Benefits', 'purpose': 'Expected outcomes',
                     'status': 'optional', 'sentences': (1, 3)}
                ]
            }
        ]
    },

    # =========================================================================
    # BLOG POST
    # =========================================================================
    GenreType.BLOG_POST: {
        'name': "Blog Post",
        'source': "Content Marketing",
        'total_words': (800, 2000),
        'style': {'register': 'informal', 'hedging': False, 'citations': False},
        'sections': [
            {
                'id': 'main',
                'name': 'Blog Post',
                'moves': [
                    {'id': 'BLG-1', 'name': 'Hook', 'purpose': 'Grab attention',
                     'status': 'obligatory', 'sentences': (1, 3)},
                    {'id': 'BLG-2', 'name': 'Problem/Question', 'purpose': 'Establish relevance',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'BLG-3', 'name': 'Main Content', 'purpose': 'Deliver value',
                     'status': 'obligatory', 'sentences': (10, 30),
                     'recursive': True},
                    {'id': 'BLG-4', 'name': 'Takeaway', 'purpose': 'Key message',
                     'status': 'obligatory', 'sentences': (1, 3)},
                    {'id': 'BLG-5', 'name': 'Call to Action', 'purpose': 'Engage reader',
                     'status': 'optional', 'sentences': (1, 2)}
                ]
            }
        ]
    },

    # =========================================================================
    # CONSULTING MEMO
    # =========================================================================
    GenreType.CONSULTING_MEMO: {
        'name': "Consulting Memo",
        'source': "McKinsey/BCG Style",
        'total_words': (500, 1500),
        'style': {'register': 'formal', 'hedging': False, 'citations': False},
        'sections': [
            {
                'id': 'main',
                'name': 'Memo',
                'moves': [
                    {'id': 'MEM-1', 'name': 'Governing Thought', 'purpose': 'Main message upfront',
                     'status': 'obligatory', 'sentences': (1, 2)},
                    {'id': 'MEM-2', 'name': 'Situation', 'purpose': 'Context',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'MEM-3', 'name': 'Findings', 'purpose': 'Key insights',
                     'status': 'obligatory', 'sentences': (3, 8),
                     'rst': ['evidence', 'elaboration']},
                    {'id': 'MEM-4', 'name': 'Recommendation', 'purpose': 'What to do',
                     'status': 'obligatory', 'sentences': (2, 4)},
                    {'id': 'MEM-5', 'name': 'Next Steps', 'purpose': 'Immediate actions',
                     'status': 'optional', 'sentences': (2, 4),
                     'rst': ['sequence']}
                ]
            }
        ]
    }
}


# =============================================================================
# MOVE PLANNER
# =============================================================================

class MovePlanner:
    """
    Plans document structure by generating move sequences.

    Usage:
        planner = MovePlanner()
        plan = planner.plan_from_genre(GenreType.SCIENTIFIC_PAPER)
        plan = planner.plan_from_8d(profile_8d)
    """

    def __init__(self, language: str = 'en'):
        """Initialize the move planner."""
        self.language = language
        self.templates = GENRE_TEMPLATES

        # Try to load genre mapper for 8D integration
        self.genre_mapper = None
        try:
            from swsm_genre_mapper import GenreMapper
            self.genre_mapper = GenreMapper()
        except ImportError:
            logger.warning("Genre mapper not available. 8D integration disabled.")

    def plan_from_genre(
        self,
        genre: GenreType,
        customizations: Optional[Dict[str, Any]] = None
    ) -> DocumentPlan:
        """
        Generate a document plan from a genre template.

        Args:
            genre: The genre to plan for
            customizations: Optional customizations (e.g., skip sections)

        Returns:
            DocumentPlan with complete move structure
        """
        if genre not in self.templates:
            logger.warning(f"No template for {genre}, using SCIENTIFIC_PAPER")
            genre = GenreType.SCIENTIFIC_PAPER

        template = self.templates[genre]
        customizations = customizations or {}

        # Create plan
        plan = DocumentPlan(
            genre=genre,
            generated_from="genre_template"
        )

        # Set global constraints
        if 'total_words' in template:
            plan.total_min_words, plan.total_max_words = template['total_words']

        plan.style_profile = template.get('style', {})

        # Build sections and moves
        skip_sections = customizations.get('skip_sections', [])
        section_order = 0

        for section_def in template['sections']:
            if section_def['id'] in skip_sections:
                continue

            section = Section(
                section_id=section_def['id'],
                name=section_def['name'],
                order=section_order
            )
            section_order += 1

            move_order = 0
            for move_def in section_def['moves']:
                # Check if move should be skipped
                skip_moves = customizations.get('skip_moves', [])
                if move_def['id'] in skip_moves:
                    continue

                # Create move
                move = self._create_move(move_def, section.section_id, move_order)
                section.moves.append(move)
                move_order += 1

            plan.sections.append(section)

        return plan

    def plan_from_8d(
        self,
        profile: Dict[str, float],
        customizations: Optional[Dict[str, Any]] = None
    ) -> DocumentPlan:
        """
        Generate a document plan from an 8D profile.

        Args:
            profile: 8D profile (D1-D8 values)
            customizations: Optional customizations

        Returns:
            DocumentPlan with genre inferred from profile
        """
        if not self.genre_mapper:
            logger.warning("Genre mapper not available. Using default genre.")
            return self.plan_from_genre(GenreType.SCIENTIFIC_PAPER, customizations)

        # Import Profile8D
        try:
            from swsm_genre_mapper import Profile8D
            profile_8d = Profile8D(
                D1_expertise=profile.get('D1', 0.5),
                D2_proximity=profile.get('D2', 0.5),
                D3_scope=profile.get('D3', 0.5),
                D4_time=profile.get('D4', 0.5),
                D5_goal=profile.get('D5', 'inform'),
                D6_context=profile.get('D6', 0.5),
                D7_emotion=profile.get('D7', 0.3),
                D8_persistence=profile.get('D8', 0.5)
            )
        except ImportError:
            return self.plan_from_genre(GenreType.SCIENTIFIC_PAPER, customizations)

        # Infer genre
        genre_type, confidence = self.genre_mapper.infer_genre(profile_8d)

        # Map to GenreType enum
        genre_map = {
            'scientific_paper': GenreType.SCIENTIFIC_PAPER,
            'policy_brief': GenreType.POLICY_BRIEF,
            'executive_summary': GenreType.EXECUTIVE_SUMMARY,
            'blog_post': GenreType.BLOG_POST,
            'technical_report': GenreType.BUSINESS_REPORT,
            'consulting_memo': GenreType.CONSULTING_MEMO
        }

        genre = genre_map.get(genre_type.value, GenreType.SCIENTIFIC_PAPER)

        # Generate plan
        plan = self.plan_from_genre(genre, customizations)
        plan.generated_from = "8d_profile"

        # Adjust constraints based on 8D
        self._adjust_for_8d(plan, profile_8d)

        return plan

    def _create_move(
        self,
        move_def: Dict[str, Any],
        parent_section: str,
        order: int
    ) -> Move:
        """Create a Move object from a definition."""

        # Parse status
        status_map = {
            'obligatory': MoveStatus.OBLIGATORY,
            'optional': MoveStatus.OPTIONAL,
            'conditional': MoveStatus.CONDITIONAL,
            'recursive': MoveStatus.RECURSIVE
        }
        status = status_map.get(move_def.get('status', 'obligatory'), MoveStatus.OBLIGATORY)

        # Parse RST hints
        rst_hints = []
        for rst_name in move_def.get('rst', []):
            try:
                rst_hints.append(RSTRelationHint(rst_name))
            except ValueError:
                pass

        # Create constraints
        sentences = move_def.get('sentences', (2, 5))
        constraints = MoveConstraints(
            min_sentences=sentences[0],
            max_sentences=sentences[1],
            recommended_rst=rst_hints
        )

        return Move(
            move_id=move_def['id'],
            name=move_def['name'],
            description=move_def.get('description', ''),
            purpose=move_def.get('purpose', ''),
            status=status,
            order=order,
            parent_section=parent_section,
            constraints=constraints,
            strategies=move_def.get('strategies', [])
        )

    def _adjust_for_8d(self, plan: DocumentPlan, profile) -> None:
        """Adjust plan constraints based on 8D profile."""

        # D4 (time) affects length
        if hasattr(profile, 'D4_time'):
            if profile.D4_time < 0.3:
                # Short time: reduce sentence counts
                for section in plan.sections:
                    for move in section.moves:
                        move.constraints.max_sentences = min(
                            move.constraints.max_sentences,
                            5
                        )
            elif profile.D4_time > 0.7:
                # More time: can expand
                for section in plan.sections:
                    for move in section.moves:
                        move.constraints.max_sentences = int(
                            move.constraints.max_sentences * 1.5
                        )

        # D1 (expertise) affects hedging
        if hasattr(profile, 'D1_expertise'):
            hedging = profile.D1_expertise > 0.7
            for section in plan.sections:
                for move in section.moves:
                    move.constraints.hedging_required = hedging

    def get_available_genres(self) -> List[str]:
        """Get list of available genre templates."""
        return [g.value for g in self.templates.keys()]

    def get_genre_info(self, genre: GenreType) -> Dict[str, Any]:
        """Get information about a genre template."""
        if genre not in self.templates:
            return {}

        template = self.templates[genre]
        return {
            'name': template['name'],
            'source': template['source'],
            'word_range': template.get('total_words'),
            'style': template.get('style'),
            'section_count': len(template['sections']),
            'sections': [s['name'] for s in template['sections']],
            'total_moves': sum(len(s['moves']) for s in template['sections'])
        }


# =============================================================================
# CLI
# =============================================================================

def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description='SWSM Move Planner (E8) - Document Structure Planning'
    )
    parser.add_argument(
        '--genre', '-g',
        choices=[g.value for g in GenreType],
        help='Genre to plan for'
    )
    parser.add_argument(
        '--list-genres',
        action='store_true',
        help='List available genres'
    )
    parser.add_argument(
        '--info',
        metavar='GENRE',
        help='Show info about a genre'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file (JSON)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'outline'],
        default='outline',
        help='Output format'
    )

    args = parser.parse_args()
    planner = MovePlanner()

    if args.list_genres:
        print("Available Genres:")
        print("-" * 40)
        for genre in GenreType:
            info = planner.get_genre_info(genre)
            if info:
                print(f"  {genre.value:<25} ({info['total_moves']} moves)")
        return

    if args.info:
        try:
            genre = GenreType(args.info)
            info = planner.get_genre_info(genre)
            print(f"\n{info['name']}")
            print("=" * 50)
            print(f"Source: {info['source']}")
            print(f"Word Range: {info['word_range']}")
            print(f"Style: {info['style']}")
            print(f"\nSections ({info['section_count']}):")
            for section in info['sections']:
                print(f"  • {section}")
            print(f"\nTotal Moves: {info['total_moves']}")
        except ValueError:
            print(f"Unknown genre: {args.info}")
        return

    if args.genre:
        genre = GenreType(args.genre)
        plan = planner.plan_from_genre(genre)

        if args.format == 'json':
            result = plan.to_dict()
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                print(f"Saved to {args.output}")
            else:
                print(json.dumps(result, indent=2))
        else:
            # Outline format
            print(f"\n{'='*60}")
            print(f"DOCUMENT PLAN: {genre.value.upper()}")
            print(f"{'='*60}")
            print(f"Words: {plan.total_min_words}-{plan.total_max_words}")
            print(f"Style: {plan.style_profile}")
            print()

            for section in plan.sections:
                print(f"\n## {section.name.upper()}")
                print("-" * 40)
                for move in section.moves:
                    status_icon = {
                        MoveStatus.OBLIGATORY: "●",
                        MoveStatus.OPTIONAL: "○",
                        MoveStatus.CONDITIONAL: "◐",
                        MoveStatus.RECURSIVE: "↻"
                    }.get(move.status, "●")

                    print(f"  {status_icon} [{move.move_id}] {move.name}")
                    print(f"      Purpose: {move.purpose}")
                    print(f"      Sentences: {move.constraints.min_sentences}-{move.constraints.max_sentences}")
                    if move.strategies:
                        print(f"      Strategies: {', '.join(move.strategies[:2])}")

            print(f"\n{'='*60}")
            print(f"Total: {plan.get_total_moves()} moves")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
