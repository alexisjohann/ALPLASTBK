#!/usr/bin/env python3
"""
SWSM Text Generator (E9)
========================

Generates text from document plans using SFL realizations.

This is the synthesis component that brings together:
- E1: SFL clause features (Transitivity, Mood, Theme)
- E4: RST-SFL Bridge (discourse-clause mapping)
- E5: Cohesion devices (reference chains, conjunctions)
- E6: Information structure (Given/New, Topic/Comment)
- E7: 8D style constraints
- E8: Move sequences and document plans

Architecture:
    DocumentPlan (E8)
         |
         v
    +--------------------+
    | E9 Text Generator  |
    +--------------------+
         |
    [For each Section]
         |
    [For each Move]
         |
         v
    +--------------------+
    | Move Realizer      |  <- Uses E4 RST-SFL mappings
    +--------------------+
         |
         v
    +--------------------+
    | Paragraph Builder  |  <- Uses E5 Cohesion, E6 InfoStructure
    +--------------------+
         |
         v
    +--------------------+
    | Clause Generator   |  <- Uses E1 SFL features
    +--------------------+
         |
         v
    Generated Text

Axioms implemented:
- SWSM-6: Simultaneity (all three metafunctions per clause)
- SWSM-7: Rank-Metafunction Mapping (L5 pivot)
- SWSM-9: Style Percolation (8D constraints propagate down)
- SWSM-10: Bidirectional Isomorphism (generation direction)

Sources:
- Halliday (1985): Introduction to Functional Grammar
- Matthiessen & Bateman (1991): Text Generation and SFL
- Teich (1999): Systemic Functional Grammar in NLG

Author: FehrAdvice & Partners AG
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import random


# =============================================================================
# ENUMS AND TYPE DEFINITIONS
# =============================================================================

class ProcessType(Enum):
    """Halliday's process types for Transitivity system."""
    MATERIAL = "material"      # Actions, events
    MENTAL = "mental"          # Cognition, perception, affect
    RELATIONAL = "relational"  # Being, having
    VERBAL = "verbal"          # Saying
    BEHAVIORAL = "behavioral"  # Physiological/psychological behavior
    EXISTENTIAL = "existential"  # Existence


class MoodType(Enum):
    """Mood choices for Interpersonal metafunction."""
    DECLARATIVE = "declarative"
    INTERROGATIVE_YN = "interrogative_yn"
    INTERROGATIVE_WH = "interrogative_wh"
    IMPERATIVE = "imperative"
    EXCLAMATIVE = "exclamative"


class ThemeType(Enum):
    """Theme types for Textual metafunction."""
    TOPICAL = "topical"
    INTERPERSONAL = "interpersonal"
    TEXTUAL = "textual"


class ModalityLevel(Enum):
    """Modality strength levels."""
    HIGH = "high"
    MEDIAN = "median"
    LOW = "low"


class ConjunctionType(Enum):
    """Conjunction types for clause combining."""
    ADDITIVE = "additive"
    ADVERSATIVE = "adversative"
    CAUSAL = "causal"
    TEMPORAL = "temporal"


class InformationStatus(Enum):
    """Given/New information status."""
    GIVEN = "given"
    NEW = "new"
    BRIDGING = "bridging"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ClauseSpec:
    """Specification for generating a single clause."""
    # Ideational
    process_type: ProcessType = ProcessType.MATERIAL
    participants: Dict[str, str] = field(default_factory=dict)
    circumstances: Dict[str, str] = field(default_factory=dict)

    # Interpersonal
    mood: MoodType = MoodType.DECLARATIVE
    modality_type: Optional[str] = None  # epistemic, deontic, dynamic
    modality_level: ModalityLevel = ModalityLevel.MEDIAN
    polarity: bool = True  # positive

    # Textual
    theme_type: ThemeType = ThemeType.TOPICAL
    marked_theme: bool = False
    theme_element: Optional[str] = None

    # Information structure (E6)
    info_status: InformationStatus = InformationStatus.NEW
    is_topic: bool = False
    is_focus: bool = False

    # Content
    content_template: Optional[str] = None
    lexical_choices: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class ClauseComplexSpec:
    """Specification for a clause complex (L4)."""
    clauses: List[ClauseSpec] = field(default_factory=list)
    taxis: str = "paratactic"  # paratactic or hypotactic
    logico_semantic: str = "expansion"  # expansion or projection
    rst_relation: Optional[str] = None
    conjunction: Optional[str] = None


@dataclass
class ParagraphSpec:
    """Specification for a paragraph (L3)."""
    clause_complexes: List[ClauseComplexSpec] = field(default_factory=list)
    paragraph_type: str = "topic"  # topic, supporting, transitional, concluding
    nucleus_position: str = "initial"  # initial, medial, final
    cohesion_devices: List[str] = field(default_factory=list)
    thematic_progression: str = "constant"  # constant, linear, derived


@dataclass
class GeneratedClause:
    """A generated clause with its text and metadata."""
    text: str
    spec: ClauseSpec
    tokens: List[str] = field(default_factory=list)


@dataclass
class GeneratedParagraph:
    """A generated paragraph with its clauses."""
    text: str
    clauses: List[GeneratedClause] = field(default_factory=list)
    cohesion_score: float = 0.0


@dataclass
class GeneratedSection:
    """A generated section with its paragraphs."""
    title: str
    paragraphs: List[GeneratedParagraph] = field(default_factory=list)
    move_sequence: List[str] = field(default_factory=list)


@dataclass
class GeneratedDocument:
    """A complete generated document."""
    title: str
    genre: str
    sections: List[GeneratedSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    word_count: int = 0


@dataclass
class StyleConstraints:
    """Style constraints derived from 8D profile."""
    formality: float = 0.5  # 0=casual, 1=formal
    technicality: float = 0.5  # 0=simple, 1=technical
    hedging: float = 0.5  # 0=assertive, 1=hedged
    sentence_length_range: Tuple[int, int] = (15, 25)
    paragraph_length_range: Tuple[int, int] = (3, 7)
    contractions_allowed: bool = True
    personal_pronouns_allowed: bool = True
    passive_preference: float = 0.3


# =============================================================================
# LEXICAL RESOURCES
# =============================================================================

class LexicalResources:
    """Lexical resources for text generation."""

    # Conjunctions by type and language
    CONJUNCTIONS = {
        'en': {
            ConjunctionType.ADDITIVE: ['and', 'also', 'moreover', 'furthermore', 'in addition'],
            ConjunctionType.ADVERSATIVE: ['but', 'however', 'yet', 'nevertheless', 'on the other hand'],
            ConjunctionType.CAUSAL: ['so', 'therefore', 'thus', 'because', 'consequently'],
            ConjunctionType.TEMPORAL: ['then', 'next', 'finally', 'subsequently', 'meanwhile'],
        },
        'de': {
            ConjunctionType.ADDITIVE: ['und', 'auch', 'ausserdem', 'zudem', 'ferner'],
            ConjunctionType.ADVERSATIVE: ['aber', 'jedoch', 'dennoch', 'hingegen'],
            ConjunctionType.CAUSAL: ['also', 'daher', 'deshalb', 'weil', 'folglich'],
            ConjunctionType.TEMPORAL: ['dann', 'danach', 'schliesslich', 'inzwischen'],
        }
    }

    # Hedging expressions
    HEDGES = {
        'en': {
            'high': ['certainly', 'clearly', 'undoubtedly', 'definitely'],
            'median': ['probably', 'likely', 'suggests', 'indicates'],
            'low': ['possibly', 'perhaps', 'might', 'may'],
        },
        'de': {
            'high': ['sicherlich', 'zweifellos', 'eindeutig'],
            'median': ['wahrscheinlich', 'vermutlich', 'deutet darauf hin'],
            'low': ['möglicherweise', 'vielleicht', 'könnte'],
        }
    }

    # Sentence starters by function
    SENTENCE_STARTERS = {
        'en': {
            'establish_territory': [
                'Research on {topic} has shown that',
                '{topic} is widely recognized as',
                'In recent years, {topic} has become',
                'The importance of {topic} is well established',
            ],
            'establish_niche': [
                'However, little attention has been paid to',
                'Despite this progress, {gap} remains unclear',
                'Yet, few studies have examined',
                'Nevertheless, there is a gap in our understanding of',
            ],
            'occupy_niche': [
                'This paper aims to',
                'The present study investigates',
                'We argue that',
                'This research contributes to',
            ],
            'present_findings': [
                'The results indicate that',
                'Analysis reveals that',
                'The data show that',
                'Our findings suggest that',
            ],
            'conclude': [
                'In conclusion,',
                'To summarize,',
                'These findings demonstrate that',
                'Overall, this study shows that',
            ],
        },
        'de': {
            'establish_territory': [
                'Die Forschung zu {topic} hat gezeigt, dass',
                '{topic} wird weithin als wichtig anerkannt',
                'In den letzten Jahren hat {topic}',
            ],
            'establish_niche': [
                'Jedoch wurde {gap} bisher wenig beachtet',
                'Trotz dieser Fortschritte bleibt unklar',
                'Dennoch gibt es eine Lücke in unserem Verständnis',
            ],
            'occupy_niche': [
                'Diese Arbeit zielt darauf ab',
                'Die vorliegende Studie untersucht',
                'Wir argumentieren, dass',
            ],
        }
    }

    # Process-specific verbs
    PROCESS_VERBS = {
        ProcessType.MATERIAL: {
            'en': ['create', 'produce', 'develop', 'implement', 'conduct', 'perform'],
            'de': ['erstellen', 'produzieren', 'entwickeln', 'durchführen'],
        },
        ProcessType.MENTAL: {
            'en': ['believe', 'think', 'understand', 'recognize', 'perceive', 'consider'],
            'de': ['glauben', 'denken', 'verstehen', 'erkennen', 'betrachten'],
        },
        ProcessType.RELATIONAL: {
            'en': ['is', 'are', 'represents', 'constitutes', 'indicates', 'reflects'],
            'de': ['ist', 'sind', 'stellt dar', 'zeigt', 'reflektiert'],
        },
        ProcessType.VERBAL: {
            'en': ['argue', 'state', 'claim', 'suggest', 'propose', 'assert'],
            'de': ['argumentieren', 'behaupten', 'vorschlagen', 'feststellen'],
        },
        ProcessType.EXISTENTIAL: {
            'en': ['exists', 'there is', 'there are', 'occurs', 'arises'],
            'de': ['existiert', 'es gibt', 'tritt auf', 'entsteht'],
        },
    }


# =============================================================================
# CLAUSE GENERATOR (L5)
# =============================================================================

class ClauseGenerator:
    """
    Generates clauses based on SFL specifications.

    Implements SWSM-6: Every clause realizes all three metafunctions.
    """

    def __init__(self, language: str = 'en'):
        self.language = language
        self.resources = LexicalResources()

    def generate(self, spec: ClauseSpec) -> GeneratedClause:
        """Generate a clause from specification."""
        # Build clause components
        components = []

        # 1. Textual: Theme position
        if spec.marked_theme and spec.theme_element:
            components.append(spec.theme_element + ',')

        # 2. Textual: Textual theme (conjunction)
        if spec.theme_type == ThemeType.TEXTUAL and spec.content_template:
            # Conjunction is handled in content
            pass

        # 3. Interpersonal: Mood structure
        clause_text = self._realize_mood(spec)

        # 4. Ideational: Transitivity
        if not clause_text and spec.content_template:
            clause_text = self._realize_transitivity(spec)
        elif not clause_text:
            clause_text = self._generate_default_clause(spec)

        # Apply hedging if needed
        if spec.modality_type == 'epistemic':
            clause_text = self._apply_hedging(clause_text, spec.modality_level)

        # Apply polarity
        if not spec.polarity:
            clause_text = self._apply_negation(clause_text)

        # Combine components
        if components:
            full_text = ' '.join(components) + ' ' + clause_text
        else:
            full_text = clause_text

        return GeneratedClause(
            text=full_text,
            spec=spec,
            tokens=full_text.split()
        )

    def _realize_mood(self, spec: ClauseSpec) -> str:
        """Realize interpersonal meaning through mood choices."""
        if spec.mood == MoodType.INTERROGATIVE_YN:
            # Yes/No question
            if spec.content_template:
                return f"Does {spec.content_template}?"
            return "Is this the case?"

        elif spec.mood == MoodType.INTERROGATIVE_WH:
            # WH-question
            if spec.content_template:
                return f"What {spec.content_template}?"
            return "What is the explanation?"

        elif spec.mood == MoodType.IMPERATIVE:
            if spec.content_template:
                return spec.content_template
            return "Consider the following."

        # Declarative is default, handled by transitivity
        return ""

    def _realize_transitivity(self, spec: ClauseSpec) -> str:
        """Realize ideational meaning through transitivity choices."""
        template = spec.content_template or ""

        # Replace participant placeholders
        for role, value in spec.participants.items():
            template = template.replace(f"{{{role}}}", value)

        # Replace circumstance placeholders
        for circ_type, value in spec.circumstances.items():
            template = template.replace(f"{{{circ_type}}}", value)

        # Fill in any remaining placeholders with defaults
        if '{Actor}' in template:
            template = template.replace('{Actor}', 'the study')
        if '{Goal}' in template:
            template = template.replace('{Goal}', 'this phenomenon')
        if '{topic}' in template:
            template = template.replace('{topic}', 'the topic')
        if '{gap}' in template:
            template = template.replace('{gap}', 'this aspect')

        return template

    def _generate_default_clause(self, spec: ClauseSpec) -> str:
        """Generate a default clause based on process type."""
        verbs = self.resources.PROCESS_VERBS.get(spec.process_type, {})
        verb_list = verbs.get(self.language, ['is'])
        verb = random.choice(verb_list)

        actor = spec.participants.get('Actor', 'This')
        goal = spec.participants.get('Goal', 'the phenomenon')

        if spec.process_type == ProcessType.RELATIONAL:
            return f"{actor} {verb} {goal}"
        elif spec.process_type == ProcessType.EXISTENTIAL:
            return f"There {verb} {goal}"
        else:
            return f"{actor} {verb} {goal}"

    def _apply_hedging(self, text: str, level: ModalityLevel) -> str:
        """Apply hedging expressions based on modality level."""
        hedges = self.resources.HEDGES.get(self.language, {})
        hedge_list = hedges.get(level.value, [])

        if hedge_list:
            hedge = random.choice(hedge_list)
            # Insert hedge after first word or at start
            words = text.split()
            if len(words) > 1:
                words.insert(1, hedge)
                return ' '.join(words)
            return f"{hedge} {text}"
        return text

    def _apply_negation(self, text: str) -> str:
        """Apply negation to clause."""
        # Simple negation - insert 'not' after first auxiliary or verb
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ['is', 'are', 'was', 'were', 'has', 'have', 'do', 'does']:
                words.insert(i + 1, 'not')
                return ' '.join(words)
        # Fallback: add 'do not' at appropriate position
        if len(words) > 1:
            return f"{words[0]} does not {' '.join(words[1:])}"
        return f"not {text}"


# =============================================================================
# CLAUSE COMPLEX BUILDER (L4)
# =============================================================================

class ClauseComplexBuilder:
    """
    Builds clause complexes from multiple clauses.

    Uses RST-SFL mappings from E4 to determine conjunction choices.
    """

    def __init__(self, language: str = 'en'):
        self.language = language
        self.clause_generator = ClauseGenerator(language)
        self.resources = LexicalResources()

    def build(self, spec: ClauseComplexSpec) -> str:
        """Build a clause complex from specification."""
        if not spec.clauses:
            return ""

        # Generate individual clauses
        generated = [self.clause_generator.generate(c) for c in spec.clauses]

        if len(generated) == 1:
            return generated[0].text

        # Combine clauses based on taxis and RST relation
        return self._combine_clauses(generated, spec)

    def _combine_clauses(self, clauses: List[GeneratedClause], spec: ClauseComplexSpec) -> str:
        """Combine clauses with appropriate connectors."""
        texts = [c.text for c in clauses]

        # Get conjunction based on RST relation or default
        conjunction = self._select_conjunction(spec)

        if spec.taxis == "paratactic":
            # Equal status - coordinate
            if conjunction:
                return f"{texts[0]}, {conjunction} {texts[1]}"
            return f"{texts[0]}, and {texts[1]}"
        else:
            # Hypotactic - dependent
            if conjunction:
                return f"{conjunction} {texts[1]}, {texts[0]}"
            return f"{texts[0]} that {texts[1]}"

    def _select_conjunction(self, spec: ClauseComplexSpec) -> Optional[str]:
        """Select appropriate conjunction based on RST relation."""
        if spec.conjunction:
            return spec.conjunction

        # Map RST relation to conjunction type
        rst_to_conj = {
            'cause': ConjunctionType.CAUSAL,
            'result': ConjunctionType.CAUSAL,
            'contrast': ConjunctionType.ADVERSATIVE,
            'concession': ConjunctionType.ADVERSATIVE,
            'sequence': ConjunctionType.TEMPORAL,
            'elaboration': ConjunctionType.ADDITIVE,
        }

        if spec.rst_relation and spec.rst_relation in rst_to_conj:
            conj_type = rst_to_conj[spec.rst_relation]
            conj_list = self.resources.CONJUNCTIONS.get(self.language, {}).get(conj_type, [])
            if conj_list:
                return random.choice(conj_list)

        return None


# =============================================================================
# PARAGRAPH BUILDER (L3)
# =============================================================================

class ParagraphBuilder:
    """
    Builds paragraphs with proper cohesion and information flow.

    Uses E5 (Cohesion) and E6 (Information Structure) principles.
    """

    def __init__(self, language: str = 'en'):
        self.language = language
        self.complex_builder = ClauseComplexBuilder(language)
        self.resources = LexicalResources()

    def build(self, spec: ParagraphSpec) -> GeneratedParagraph:
        """Build a paragraph from specification."""
        sentences = []

        for i, cc_spec in enumerate(spec.clause_complexes):
            # Apply cohesion devices
            if i > 0 and spec.cohesion_devices:
                cc_spec = self._apply_cohesion(cc_spec, spec.cohesion_devices, i)

            sentence = self.complex_builder.build(cc_spec)
            if sentence:
                # Ensure sentence ends with period
                if not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                # Capitalize first letter
                sentence = sentence[0].upper() + sentence[1:]
                sentences.append(sentence)

        text = ' '.join(sentences)

        return GeneratedParagraph(
            text=text,
            clauses=[],  # Could populate with generated clauses
            cohesion_score=self._calculate_cohesion_score(sentences)
        )

    def _apply_cohesion(self, spec: ClauseComplexSpec, devices: List[str], position: int) -> ClauseComplexSpec:
        """Apply cohesion devices to clause complex."""
        if 'conjunction' in devices and spec.clauses:
            # Add textual theme with conjunction
            if position == 1:
                spec.conjunction = 'Furthermore'
            elif position == 2:
                spec.conjunction = 'Moreover'
            else:
                conj_list = self.resources.CONJUNCTIONS.get(self.language, {}).get(
                    ConjunctionType.ADDITIVE, ['Also']
                )
                spec.conjunction = random.choice(conj_list)

        return spec

    def _calculate_cohesion_score(self, sentences: List[str]) -> float:
        """Calculate a simple cohesion score."""
        if len(sentences) < 2:
            return 1.0

        score = 0.0

        # Check for conjunctions
        conjunctions = ['however', 'therefore', 'moreover', 'furthermore', 'thus', 'also']
        for s in sentences[1:]:
            if any(c in s.lower() for c in conjunctions):
                score += 0.2

        # Check for lexical repetition (simple word overlap)
        all_words = set()
        for s in sentences:
            words = set(s.lower().split())
            overlap = len(words & all_words)
            if overlap > 0:
                score += 0.1 * min(overlap, 3)
            all_words.update(words)

        return min(score, 1.0)


# =============================================================================
# MOVE REALIZER (L2)
# =============================================================================

class MoveRealizer:
    """
    Realizes rhetorical moves as text.

    Maps move specifications to paragraph structures using E4 RST-SFL mappings.
    """

    def __init__(self, language: str = 'en'):
        self.language = language
        self.paragraph_builder = ParagraphBuilder(language)
        self.resources = LexicalResources()

    def realize(self, move_name: str, move_purpose: str,
                style: StyleConstraints, context: Dict[str, Any] = None) -> List[GeneratedParagraph]:
        """Realize a move as one or more paragraphs."""
        context = context or {}
        paragraphs = []

        # Get move-specific templates
        templates = self._get_move_templates(move_name)

        # Build paragraph spec based on move type
        para_spec = self._create_paragraph_spec(move_name, templates, style, context)

        # Generate paragraph
        para = self.paragraph_builder.build(para_spec)
        paragraphs.append(para)

        return paragraphs

    def _get_move_templates(self, move_name: str) -> List[str]:
        """Get sentence templates for a move."""
        move_lower = move_name.lower()

        # Map move names to template categories
        if 'territory' in move_lower or 'background' in move_lower:
            return self.resources.SENTENCE_STARTERS.get(self.language, {}).get('establish_territory', [])
        elif 'niche' in move_lower or 'gap' in move_lower:
            return self.resources.SENTENCE_STARTERS.get(self.language, {}).get('establish_niche', [])
        elif 'occupy' in move_lower or 'purpose' in move_lower or 'aim' in move_lower:
            return self.resources.SENTENCE_STARTERS.get(self.language, {}).get('occupy_niche', [])
        elif 'finding' in move_lower or 'result' in move_lower:
            return self.resources.SENTENCE_STARTERS.get(self.language, {}).get('present_findings', [])
        elif 'conclusion' in move_lower or 'summary' in move_lower:
            return self.resources.SENTENCE_STARTERS.get(self.language, {}).get('conclude', [])

        return []

    def _create_paragraph_spec(self, move_name: str, templates: List[str],
                                style: StyleConstraints, context: Dict[str, Any]) -> ParagraphSpec:
        """Create paragraph specification for a move."""
        clause_complexes = []

        # Create 2-4 clause complexes for the paragraph
        num_sentences = random.randint(
            style.paragraph_length_range[0],
            style.paragraph_length_range[1]
        )

        for i in range(num_sentences):
            clauses = []

            # Create main clause
            main_clause = ClauseSpec(
                process_type=self._select_process_type(move_name),
                mood=MoodType.DECLARATIVE,
                modality_level=ModalityLevel.MEDIAN if style.hedging > 0.5 else ModalityLevel.HIGH,
                modality_type='epistemic' if style.hedging > 0.5 else None,
                theme_type=ThemeType.TOPICAL,
                info_status=InformationStatus.NEW if i == 0 else InformationStatus.GIVEN,
            )

            # Set content template
            if templates and i < len(templates):
                main_clause.content_template = templates[i]
            else:
                main_clause.content_template = self._generate_generic_content(move_name, context)

            # Fill context variables
            for key, value in context.items():
                if main_clause.content_template:
                    main_clause.content_template = main_clause.content_template.replace(
                        f"{{{key}}}", str(value)
                    )

            clauses.append(main_clause)

            # Determine RST relation for clause complex
            rst_relation = self._select_rst_relation(move_name, i)

            clause_complexes.append(ClauseComplexSpec(
                clauses=clauses,
                taxis="paratactic",
                rst_relation=rst_relation,
            ))

        return ParagraphSpec(
            clause_complexes=clause_complexes,
            paragraph_type="topic" if 'establish' in move_name.lower() else "supporting",
            cohesion_devices=['conjunction', 'reference'],
            thematic_progression="linear",
        )

    def _select_process_type(self, move_name: str) -> ProcessType:
        """Select appropriate process type for move."""
        move_lower = move_name.lower()

        if 'finding' in move_lower or 'result' in move_lower:
            return ProcessType.RELATIONAL
        elif 'method' in move_lower or 'procedure' in move_lower:
            return ProcessType.MATERIAL
        elif 'argue' in move_lower or 'claim' in move_lower:
            return ProcessType.VERBAL
        elif 'believe' in move_lower or 'understand' in move_lower:
            return ProcessType.MENTAL

        return ProcessType.RELATIONAL

    def _select_rst_relation(self, move_name: str, position: int) -> Optional[str]:
        """Select RST relation based on move and position."""
        move_lower = move_name.lower()

        if position == 0:
            return 'preparation'
        elif 'niche' in move_lower:
            return 'contrast'
        elif 'evidence' in move_lower:
            return 'evidence'
        elif 'result' in move_lower:
            return 'result'

        return 'elaboration'

    def _generate_generic_content(self, move_name: str, context: Dict[str, Any]) -> str:
        """Generate generic content for a move."""
        topic = context.get('topic', 'the phenomenon')

        generic_templates = {
            'establish_territory': f"Research on {topic} has demonstrated significant findings.",
            'establish_niche': f"However, aspects of {topic} remain underexplored.",
            'occupy_niche': f"This study addresses gaps in our understanding of {topic}.",
            'present_findings': f"The analysis reveals important patterns related to {topic}.",
            'conclude': f"These findings contribute to our understanding of {topic}.",
        }

        for key, template in generic_templates.items():
            if key in move_name.lower():
                return template

        return f"This aspect of {topic} warrants further consideration."


# =============================================================================
# SECTION COMPOSER (L2)
# =============================================================================

class SectionComposer:
    """
    Composes sections from moves.

    Follows move sequences from E8 Move Planner.
    """

    def __init__(self, language: str = 'en'):
        self.language = language
        self.move_realizer = MoveRealizer(language)

    def compose(self, section_spec: Dict[str, Any], style: StyleConstraints,
                context: Dict[str, Any] = None) -> GeneratedSection:
        """Compose a section from its move specification."""
        context = context or {}
        paragraphs = []
        move_sequence = []

        section_id = section_spec.get('id', 'section')
        title = section_spec.get('title', 'Section')
        moves = section_spec.get('moves', [])

        for move_spec in moves:
            move_name = move_spec.get('name', '')
            move_purpose = move_spec.get('purpose', '')
            move_status = move_spec.get('status', 'optional')

            # Skip optional moves sometimes
            if move_status == 'optional' and random.random() > 0.5:
                continue

            move_sequence.append(move_name)

            # Realize the move
            move_paragraphs = self.move_realizer.realize(
                move_name, move_purpose, style, context
            )
            paragraphs.extend(move_paragraphs)

        return GeneratedSection(
            title=title,
            paragraphs=paragraphs,
            move_sequence=move_sequence
        )


# =============================================================================
# DOCUMENT COMPOSER (L1)
# =============================================================================

class DocumentComposer:
    """
    Composes complete documents from document plans.

    Integrates all SWSM components (E1-E8) for text generation.
    """

    def __init__(self, language: str = 'en'):
        self.language = language
        self.section_composer = SectionComposer(language)

    def compose(self, document_plan: Dict[str, Any],
                profile_8d: Dict[str, float] = None) -> GeneratedDocument:
        """
        Compose a complete document from a document plan.

        Args:
            document_plan: Document plan from E8 MovePlanner
            profile_8d: 8D audience profile for style constraints

        Returns:
            GeneratedDocument with all sections and text
        """
        # Derive style constraints from 8D profile
        style = self._derive_style_constraints(profile_8d or {})

        # Get document metadata
        genre = document_plan.get('genre', 'generic')
        title = document_plan.get('title', 'Untitled Document')
        sections_spec = document_plan.get('sections', [])
        context = document_plan.get('context', {})

        # Compose each section
        sections = []
        for section_spec in sections_spec:
            section = self.section_composer.compose(section_spec, style, context)
            sections.append(section)

        # Calculate total word count
        word_count = sum(
            len(p.text.split())
            for s in sections
            for p in s.paragraphs
        )

        return GeneratedDocument(
            title=title,
            genre=genre,
            sections=sections,
            metadata={
                'language': self.language,
                'style_constraints': {
                    'formality': style.formality,
                    'technicality': style.technicality,
                    'hedging': style.hedging,
                },
                '8d_profile': profile_8d,
            },
            word_count=word_count
        )

    def _derive_style_constraints(self, profile_8d: Dict[str, float]) -> StyleConstraints:
        """Derive style constraints from 8D profile (SWSM-9)."""
        d1 = profile_8d.get('D1_expertise', 0.5)
        d4 = profile_8d.get('D4_time', 0.5)
        d6 = profile_8d.get('D6_context', 0.5)
        d7 = profile_8d.get('D7_emotion', 0.5)
        d8 = profile_8d.get('D8_persistence', 0.5)

        # Map 8D to style parameters
        formality = (d6 + d8) / 2
        technicality = d1
        hedging = d8

        # Sentence length based on D4 (time) and D1 (expertise)
        if d4 < 0.3:
            sentence_range = (12, 18)
        elif d4 > 0.7:
            sentence_range = (20, 35)
        else:
            sentence_range = (15, 25)

        # Paragraph length based on D4
        if d4 < 0.3:
            para_range = (3, 5)
        else:
            para_range = (4, 7)

        return StyleConstraints(
            formality=formality,
            technicality=technicality,
            hedging=hedging,
            sentence_length_range=sentence_range,
            paragraph_length_range=para_range,
            contractions_allowed=(d6 < 0.5),
            personal_pronouns_allowed=(d6 < 0.7),
            passive_preference=0.3 + (d6 * 0.4),
        )


# =============================================================================
# SWSM TEXT GENERATOR (Main Interface)
# =============================================================================

class SWSMTextGenerator:
    """
    Main interface for SWSM text generation.

    Integrates:
    - E1: SFL Auto-Annotator (for clause features)
    - E4: RST-SFL Bridge (for discourse-clause mapping)
    - E5: Cohesion Analyzer (for cohesion devices)
    - E6: Information Structure (for Given/New flow)
    - E7: 8D → Genre Mapper (for style constraints)
    - E8: Move Planner (for document structure)
    """

    def __init__(self, language: str = 'en'):
        """
        Initialize the text generator.

        Args:
            language: Target language ('en', 'de', 'fr')
        """
        self.language = language
        self.document_composer = DocumentComposer(language)

    def generate_from_plan(self, document_plan: Dict[str, Any],
                           profile_8d: Dict[str, float] = None) -> GeneratedDocument:
        """
        Generate text from a document plan (E8 output).

        Args:
            document_plan: Output from MovePlanner.plan_from_genre() or plan_from_8d()
            profile_8d: Optional 8D profile for style customization

        Returns:
            GeneratedDocument with complete text
        """
        return self.document_composer.compose(document_plan, profile_8d)

    def generate_section(self, section_spec: Dict[str, Any],
                         style: StyleConstraints = None,
                         context: Dict[str, Any] = None) -> GeneratedSection:
        """Generate a single section."""
        style = style or StyleConstraints()
        return self.document_composer.section_composer.compose(
            section_spec, style, context
        )

    def generate_paragraph(self, move_name: str, move_purpose: str = "",
                           style: StyleConstraints = None,
                           context: Dict[str, Any] = None) -> GeneratedParagraph:
        """Generate a single paragraph for a move."""
        style = style or StyleConstraints()
        paragraphs = self.document_composer.section_composer.move_realizer.realize(
            move_name, move_purpose, style, context
        )
        return paragraphs[0] if paragraphs else GeneratedParagraph(text="")

    def render_document(self, doc: GeneratedDocument,
                        format: str = 'text') -> str:
        """
        Render generated document to string.

        Args:
            doc: GeneratedDocument to render
            format: Output format ('text', 'markdown', 'latex')

        Returns:
            Formatted document string
        """
        if format == 'markdown':
            return self._render_markdown(doc)
        elif format == 'latex':
            return self._render_latex(doc)
        else:
            return self._render_text(doc)

    def _render_text(self, doc: GeneratedDocument) -> str:
        """Render as plain text."""
        lines = [doc.title, '=' * len(doc.title), '']

        for section in doc.sections:
            lines.append(section.title)
            lines.append('-' * len(section.title))
            for para in section.paragraphs:
                lines.append(para.text)
                lines.append('')

        return '\n'.join(lines)

    def _render_markdown(self, doc: GeneratedDocument) -> str:
        """Render as Markdown."""
        lines = [f"# {doc.title}", '']

        for section in doc.sections:
            lines.append(f"## {section.title}")
            lines.append('')
            for para in section.paragraphs:
                lines.append(para.text)
                lines.append('')

        return '\n'.join(lines)

    def _render_latex(self, doc: GeneratedDocument) -> str:
        """Render as LaTeX."""
        lines = [
            '\\documentclass{article}',
            '\\begin{document}',
            f'\\title{{{doc.title}}}',
            '\\maketitle',
            ''
        ]

        for section in doc.sections:
            lines.append(f'\\section{{{section.title}}}')
            for para in section.paragraphs:
                lines.append(para.text)
                lines.append('')

        lines.append('\\end{document}')
        return '\n'.join(lines)


# =============================================================================
# DEMO / TEST
# =============================================================================

def demo():
    """Demonstrate text generation capabilities."""
    print("=" * 70)
    print("SWSM Text Generator (E9) Demo")
    print("=" * 70)

    # Create generator
    generator = SWSMTextGenerator(language='en')

    # Example document plan (simplified from E8)
    document_plan = {
        'genre': 'scientific_paper',
        'title': 'Understanding Behavioral Economics in Practice',
        'context': {
            'topic': 'behavioral economics',
            'gap': 'practical applications',
        },
        'sections': [
            {
                'id': 'introduction',
                'title': 'Introduction',
                'moves': [
                    {'name': 'Establish_Territory', 'status': 'obligatory'},
                    {'name': 'Establish_Niche', 'status': 'obligatory'},
                    {'name': 'Occupy_Niche', 'status': 'obligatory'},
                ]
            },
            {
                'id': 'conclusion',
                'title': 'Conclusion',
                'moves': [
                    {'name': 'Summarize_Findings', 'status': 'obligatory'},
                    {'name': 'Conclude', 'status': 'obligatory'},
                ]
            }
        ]
    }

    # Example 8D profile (scientific paper)
    profile_8d = {
        'D1_expertise': 0.8,
        'D2_proximity': 0.7,
        'D3_scope': 0.6,
        'D4_time': 0.7,
        'D5_goal': 'G1_inform',
        'D6_context': 0.9,
        'D7_emotion': 0.2,
        'D8_persistence': 0.9,
    }

    # Generate document
    print("\nGenerating document from plan...")
    doc = generator.generate_from_plan(document_plan, profile_8d)

    # Render as Markdown
    print("\n" + "-" * 70)
    print("Generated Document (Markdown):")
    print("-" * 70)
    print(generator.render_document(doc, format='markdown'))

    # Show metadata
    print("-" * 70)
    print("Document Metadata:")
    print(f"  Genre: {doc.genre}")
    print(f"  Word Count: {doc.word_count}")
    print(f"  Sections: {len(doc.sections)}")
    print(f"  Style: formality={doc.metadata['style_constraints']['formality']:.2f}, "
          f"technicality={doc.metadata['style_constraints']['technicality']:.2f}")
    print("-" * 70)

    # Demo single paragraph generation
    print("\nSingle Paragraph Generation:")
    print("-" * 70)
    para = generator.generate_paragraph(
        move_name='Establish_Territory',
        context={'topic': 'loss aversion'}
    )
    print(para.text)
    print(f"\nCohesion Score: {para.cohesion_score:.2f}")


if __name__ == "__main__":
    demo()
