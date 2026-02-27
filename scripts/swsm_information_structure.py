#!/usr/bin/env python3
"""
SWSM Information Structure Analyzer (E6)
========================================

Analyzes information structure in text:
1. Given/New - Information status (Halliday 1967)
2. Topic/Comment - Sentence-level aboutness (Prague School)
3. Focus/Background - Prominence and presupposition
4. Information Flow - How information develops across text

Theoretical Foundation:
- Halliday (1967): Notes on Transitivity and Theme
- Prince (1981): Toward a Taxonomy of Given-New Information
- Lambrecht (1994): Information Structure and Sentence Form
- Vallduví (1992): The Informational Component

Implements SWSM Axioms:
- SWSM-12: Thematic Progression
- SWSM-13: Information Flow

Author: SWSM Framework / EBF
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict
import re
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS: INFORMATION STRUCTURE CATEGORIES
# =============================================================================

class GivenNewStatus(Enum):
    """Information status following Prince (1981)."""
    # Given (activated in discourse)
    GIVEN_TEXTUAL = "given_textual"      # Explicitly mentioned before
    GIVEN_SITUATIONAL = "given_situational"  # Present in situation
    GIVEN_INFERRABLE = "given_inferrable"    # Inferrable from context

    # New (not activated)
    NEW_BRAND = "new_brand"              # Completely new
    NEW_UNUSED = "new_unused"            # Known but not mentioned
    NEW_INFERRABLE = "new_inferrable"    # New but inferrable


class TopicType(Enum):
    """Types of topics."""
    SENTENCE_TOPIC = "sentence_topic"    # What the sentence is about
    DISCOURSE_TOPIC = "discourse_topic"  # What the text is about
    CONTRASTIVE_TOPIC = "contrastive_topic"  # Contrasted with alternatives
    FRAME_TOPIC = "frame_topic"          # Sets the frame (temporal, spatial)


class FocusType(Enum):
    """Types of focus."""
    INFORMATION_FOCUS = "information_focus"  # New information
    CONTRASTIVE_FOCUS = "contrastive_focus"  # Contrasted with alternatives
    EXHAUSTIVE_FOCUS = "exhaustive_focus"    # Only this, nothing else
    PRESENTATIONAL_FOCUS = "presentational"  # Introduces new referent


class InformationUnit(Enum):
    """Components of information unit."""
    GIVEN = "given"           # Recoverable information
    NEW = "new"               # Non-recoverable information
    FOCUS = "focus"           # Prominent new information
    TAIL = "tail"             # Post-focal given material


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class EntityMention:
    """A mention of an entity in text."""
    text: str
    lemma: str
    position: int               # Character position
    sentence_index: int
    mention_index: int          # Which mention of this entity (1st, 2nd, etc.)
    is_first_mention: bool
    definiteness: str           # "definite" | "indefinite" | "pronoun" | "proper"
    given_new: GivenNewStatus
    confidence: float = 1.0


@dataclass
class InformationUnitAnalysis:
    """Analysis of a single information unit (typically a clause)."""
    text: str
    sentence_index: int

    # Given/New partition
    given_span: Optional[str] = None
    new_span: Optional[str] = None

    # Topic/Comment partition
    topic: Optional[str] = None
    topic_type: Optional[TopicType] = None
    comment: Optional[str] = None

    # Focus/Background partition
    focus: Optional[str] = None
    focus_type: Optional[FocusType] = None
    background: Optional[str] = None

    # Entities
    entities: List[EntityMention] = field(default_factory=list)


@dataclass
class InformationFlowAnalysis:
    """Analysis of information flow across sentences."""
    progression_type: str       # "constant" | "linear" | "derived" | "split"
    topic_chain: List[str]      # Sequence of topics
    focus_chain: List[str]      # Sequence of foci
    given_ratio: float          # Proportion of given information
    new_introduction_rate: float  # New entities per sentence


@dataclass
class InformationStructureAnalysis:
    """Complete information structure analysis."""
    text: str
    sentence_count: int

    # Per-unit analysis
    units: List[InformationUnitAnalysis] = field(default_factory=list)

    # Entity tracking
    entity_registry: Dict[str, List[EntityMention]] = field(default_factory=dict)

    # Flow analysis
    flow: Optional[InformationFlowAnalysis] = None

    # Metrics
    metrics: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'text_stats': {
                'sentence_count': self.sentence_count,
                'total_entities': len(self.entity_registry),
                'total_mentions': sum(len(m) for m in self.entity_registry.values())
            },
            'units': [
                {
                    'sentence': u.sentence_index,
                    'text': u.text[:100] + '...' if len(u.text) > 100 else u.text,
                    'given_new': {
                        'given': u.given_span,
                        'new': u.new_span
                    },
                    'topic_comment': {
                        'topic': u.topic,
                        'topic_type': u.topic_type.value if u.topic_type else None,
                        'comment': u.comment[:50] + '...' if u.comment and len(u.comment) > 50 else u.comment
                    },
                    'focus': {
                        'focus': u.focus,
                        'focus_type': u.focus_type.value if u.focus_type else None
                    }
                }
                for u in self.units
            ],
            'entity_registry': {
                entity: [
                    {
                        'text': m.text,
                        'sentence': m.sentence_index,
                        'first_mention': m.is_first_mention,
                        'given_new': m.given_new.value,
                        'definiteness': m.definiteness
                    }
                    for m in mentions
                ]
                for entity, mentions in list(self.entity_registry.items())[:10]  # Limit
            },
            'flow': {
                'progression_type': self.flow.progression_type if self.flow else None,
                'topic_chain': self.flow.topic_chain[:10] if self.flow else [],
                'given_ratio': round(self.flow.given_ratio, 2) if self.flow else 0,
                'new_rate': round(self.flow.new_introduction_rate, 2) if self.flow else 0
            },
            'metrics': {k: round(v, 3) for k, v in self.metrics.items()}
        }


# =============================================================================
# INFORMATION STRUCTURE ANALYZER
# =============================================================================

class InformationStructureAnalyzer:
    """
    Analyzes information structure in text.

    Combines:
    - Given/New analysis (Halliday, Prince)
    - Topic/Comment analysis (Prague School)
    - Focus/Background analysis (Lambrecht)
    - Information flow tracking
    """

    def __init__(self, language: str = 'en'):
        """
        Initialize the analyzer.

        Args:
            language: Language code ('en', 'de', 'fr')
        """
        self.language = language
        self.nlp = None

        # Try to load spaCy
        try:
            import spacy
            model_map = {
                'en': 'en_core_web_sm',
                'de': 'de_core_news_sm',
                'fr': 'fr_core_news_sm'
            }
            model_name = model_map.get(language, 'en_core_web_sm')
            try:
                self.nlp = spacy.load(model_name)
            except OSError:
                logger.warning(f"spaCy model {model_name} not found.")
        except ImportError:
            logger.warning("spaCy not available.")

        # Initialize markers
        self._init_markers()

    def _init_markers(self):
        """Initialize linguistic markers."""

        # Definite articles (signal given/accessible)
        self.definite_markers = {
            'en': ['the'],
            'de': ['der', 'die', 'das', 'den', 'dem', 'des'],
            'fr': ['le', 'la', 'les', "l'"]
        }

        # Indefinite articles (signal new)
        self.indefinite_markers = {
            'en': ['a', 'an', 'some'],
            'de': ['ein', 'eine', 'einen', 'einem', 'einer', 'eines'],
            'fr': ['un', 'une', 'des']
        }

        # Demonstratives (signal given/accessible)
        self.demonstratives = {
            'en': ['this', 'that', 'these', 'those'],
            'de': ['dieser', 'diese', 'dieses', 'jener', 'jene'],
            'fr': ['ce', 'cet', 'cette', 'ces']
        }

        # Focus particles (signal focus)
        self.focus_particles = {
            'en': ['only', 'even', 'also', 'just', 'especially', 'particularly'],
            'de': ['nur', 'auch', 'sogar', 'besonders', 'gerade'],
            'fr': ['seulement', 'même', 'aussi', 'surtout', 'particulièrement']
        }

        # Contrastive markers
        self.contrastive_markers = {
            'en': ['but', 'however', 'whereas', 'while', 'instead', 'rather'],
            'de': ['aber', 'jedoch', 'während', 'hingegen', 'stattdessen'],
            'fr': ['mais', 'cependant', 'tandis que', 'par contre']
        }

        # Frame setters (temporal, spatial)
        self.frame_markers = {
            'en': ['in', 'at', 'on', 'during', 'before', 'after', 'when', 'where'],
            'de': ['in', 'an', 'während', 'vor', 'nach', 'wenn', 'wo'],
            'fr': ['dans', 'à', 'pendant', 'avant', 'après', 'quand', 'où']
        }

    # =========================================================================
    # MAIN ANALYSIS METHOD
    # =========================================================================

    def analyze(self, text: str) -> InformationStructureAnalysis:
        """
        Perform complete information structure analysis.

        Args:
            text: Input text

        Returns:
            InformationStructureAnalysis with all components
        """
        # Parse text
        if self.nlp:
            doc = self.nlp(text)
            sentences = list(doc.sents)
        else:
            sentences = self._split_sentences(text)

        analysis = InformationStructureAnalysis(
            text=text,
            sentence_count=len(sentences)
        )

        # Track entities across text
        entity_mentions: Dict[str, List[EntityMention]] = defaultdict(list)
        mentioned_entities: Set[str] = set()

        # Analyze each sentence
        for sent_idx, sent in enumerate(sentences):
            sent_text = sent.text if hasattr(sent, 'text') else str(sent)

            unit = self._analyze_unit(
                sent_text,
                sent_idx,
                sent if self.nlp else None,
                mentioned_entities,
                entity_mentions
            )
            analysis.units.append(unit)

            # Update mentioned entities
            for entity in unit.entities:
                mentioned_entities.add(entity.lemma)

        analysis.entity_registry = dict(entity_mentions)

        # Analyze information flow
        analysis.flow = self._analyze_flow(analysis.units, entity_mentions)

        # Calculate metrics
        analysis.metrics = self._calculate_metrics(analysis)

        return analysis

    # =========================================================================
    # UNIT ANALYSIS
    # =========================================================================

    def _analyze_unit(
        self,
        text: str,
        sentence_index: int,
        parsed_sent,
        mentioned_entities: Set[str],
        entity_mentions: Dict[str, List[EntityMention]]
    ) -> InformationUnitAnalysis:
        """Analyze a single information unit (sentence/clause)."""

        unit = InformationUnitAnalysis(
            text=text,
            sentence_index=sentence_index
        )

        # Extract and analyze entities
        entities = self._extract_entities(
            text, sentence_index, parsed_sent, mentioned_entities, entity_mentions
        )
        unit.entities = entities

        # Analyze Given/New partition
        unit.given_span, unit.new_span = self._analyze_given_new(
            text, parsed_sent, entities
        )

        # Analyze Topic/Comment
        unit.topic, unit.topic_type, unit.comment = self._analyze_topic_comment(
            text, parsed_sent, entities
        )

        # Analyze Focus/Background
        unit.focus, unit.focus_type, unit.background = self._analyze_focus(
            text, parsed_sent, entities
        )

        return unit

    # =========================================================================
    # ENTITY EXTRACTION
    # =========================================================================

    def _extract_entities(
        self,
        text: str,
        sentence_index: int,
        parsed_sent,
        mentioned_entities: Set[str],
        entity_mentions: Dict[str, List[EntityMention]]
    ) -> List[EntityMention]:
        """Extract and classify entities in the sentence."""
        entities = []

        if parsed_sent and self.nlp:
            for token in parsed_sent:
                if token.pos_ in ('NOUN', 'PROPN'):
                    lemma = token.lemma_.lower()
                    is_first = lemma not in mentioned_entities

                    # Determine definiteness
                    definiteness = self._get_definiteness(token)

                    # Determine given/new status
                    given_new = self._classify_given_new(
                        token, is_first, definiteness, mentioned_entities
                    )

                    mention = EntityMention(
                        text=token.text,
                        lemma=lemma,
                        position=token.idx,
                        sentence_index=sentence_index,
                        mention_index=len(entity_mentions[lemma]) + 1,
                        is_first_mention=is_first,
                        definiteness=definiteness,
                        given_new=given_new
                    )

                    entities.append(mention)
                    entity_mentions[lemma].append(mention)

                # Also track pronouns
                elif token.pos_ == 'PRON' and token.text.lower() not in ('it', 'es', 'il'):
                    mention = EntityMention(
                        text=token.text,
                        lemma=token.text.lower(),
                        position=token.idx,
                        sentence_index=sentence_index,
                        mention_index=1,
                        is_first_mention=False,  # Pronouns refer to given
                        definiteness='pronoun',
                        given_new=GivenNewStatus.GIVEN_TEXTUAL
                    )
                    entities.append(mention)

        else:
            # Basic extraction without spaCy
            words = text.split()
            lang_def = self.definite_markers.get(self.language, self.definite_markers['en'])
            lang_indef = self.indefinite_markers.get(self.language, self.indefinite_markers['en'])

            for i, word in enumerate(words):
                word_lower = word.lower().strip('.,;:!?')
                # Simple heuristic: capitalized words or words after articles
                if word[0].isupper() and i > 0:
                    is_first = word_lower not in mentioned_entities
                    definiteness = 'proper'
                    given_new = GivenNewStatus.NEW_BRAND if is_first else GivenNewStatus.GIVEN_TEXTUAL

                    mention = EntityMention(
                        text=word,
                        lemma=word_lower,
                        position=text.find(word),
                        sentence_index=sentence_index,
                        mention_index=len(entity_mentions[word_lower]) + 1,
                        is_first_mention=is_first,
                        definiteness=definiteness,
                        given_new=given_new
                    )
                    entities.append(mention)
                    entity_mentions[word_lower].append(mention)

        return entities

    def _get_definiteness(self, token) -> str:
        """Determine definiteness of a noun phrase."""
        # Check for determiner
        for child in token.children:
            if child.dep_ == 'det':
                det_lower = child.text.lower()
                lang_def = self.definite_markers.get(self.language, self.definite_markers['en'])
                lang_indef = self.indefinite_markers.get(self.language, self.indefinite_markers['en'])
                lang_dem = self.demonstratives.get(self.language, self.demonstratives['en'])

                if det_lower in lang_def:
                    return 'definite'
                elif det_lower in lang_indef:
                    return 'indefinite'
                elif det_lower in lang_dem:
                    return 'demonstrative'

        # Proper nouns are definite
        if token.pos_ == 'PROPN':
            return 'proper'

        # Default: indefinite (bare noun)
        return 'bare'

    def _classify_given_new(
        self,
        token,
        is_first_mention: bool,
        definiteness: str,
        mentioned_entities: Set[str]
    ) -> GivenNewStatus:
        """Classify the given/new status of an entity."""

        # Pronouns and demonstratives -> Given
        if definiteness in ('pronoun', 'demonstrative'):
            return GivenNewStatus.GIVEN_TEXTUAL

        # Definite NP
        if definiteness == 'definite':
            if is_first_mention:
                # First mention but definite -> inferrable or situational
                return GivenNewStatus.GIVEN_INFERRABLE
            else:
                return GivenNewStatus.GIVEN_TEXTUAL

        # Proper noun
        if definiteness == 'proper':
            if is_first_mention:
                return GivenNewStatus.NEW_UNUSED  # Known entity, first mention
            else:
                return GivenNewStatus.GIVEN_TEXTUAL

        # Indefinite NP
        if definiteness == 'indefinite':
            return GivenNewStatus.NEW_BRAND

        # Bare noun
        if is_first_mention:
            return GivenNewStatus.NEW_BRAND
        else:
            return GivenNewStatus.GIVEN_TEXTUAL

    # =========================================================================
    # GIVEN/NEW ANALYSIS
    # =========================================================================

    def _analyze_given_new(
        self,
        text: str,
        parsed_sent,
        entities: List[EntityMention]
    ) -> Tuple[Optional[str], Optional[str]]:
        """Partition sentence into Given and New spans."""

        if not entities:
            return None, text

        # Collect given and new entities
        given_entities = [e for e in entities if 'GIVEN' in e.given_new.name]
        new_entities = [e for e in entities if 'NEW' in e.given_new.name]

        given_texts = [e.text for e in given_entities]
        new_texts = [e.text for e in new_entities]

        given_span = ', '.join(given_texts) if given_texts else None
        new_span = ', '.join(new_texts) if new_texts else None

        return given_span, new_span

    # =========================================================================
    # TOPIC/COMMENT ANALYSIS
    # =========================================================================

    def _analyze_topic_comment(
        self,
        text: str,
        parsed_sent,
        entities: List[EntityMention]
    ) -> Tuple[Optional[str], Optional[TopicType], Optional[str]]:
        """Analyze Topic/Comment structure."""

        topic = None
        topic_type = TopicType.SENTENCE_TOPIC
        comment = None

        if parsed_sent and self.nlp:
            # Topic is typically the subject (what the sentence is about)
            for token in parsed_sent:
                if token.dep_ in ('nsubj', 'nsubjpass'):
                    # Get the full subject phrase
                    topic_tokens = list(token.subtree)
                    topic = ' '.join([t.text for t in topic_tokens])

                    # Check for frame-setting topic (temporal/spatial)
                    if token.head.pos_ == 'ADP':
                        topic_type = TopicType.FRAME_TOPIC

                    break

                # Check for fronted adverbials (frame topics)
                elif token.dep_ == 'advmod' and token.i < 3:
                    topic = token.text
                    topic_type = TopicType.FRAME_TOPIC
                    break

            # Comment is the rest (predicate + complements)
            if topic:
                topic_start = text.lower().find(topic.lower())
                if topic_start >= 0:
                    comment = text[topic_start + len(topic):].strip()
                    # Clean up leading punctuation
                    comment = re.sub(r'^[,\s]+', '', comment)
        else:
            # Simple heuristic: first noun phrase is topic
            words = text.split()
            if words:
                # First capitalized word or first few words
                topic = words[0]
                comment = ' '.join(words[1:]) if len(words) > 1 else None

        # Check for contrastive topic
        lang_contrast = self.contrastive_markers.get(self.language, self.contrastive_markers['en'])
        if any(marker in text.lower() for marker in lang_contrast):
            topic_type = TopicType.CONTRASTIVE_TOPIC

        return topic, topic_type, comment

    # =========================================================================
    # FOCUS/BACKGROUND ANALYSIS
    # =========================================================================

    def _analyze_focus(
        self,
        text: str,
        parsed_sent,
        entities: List[EntityMention]
    ) -> Tuple[Optional[str], Optional[FocusType], Optional[str]]:
        """Analyze Focus/Background structure."""

        focus = None
        focus_type = FocusType.INFORMATION_FOCUS
        background = None

        lang_focus = self.focus_particles.get(self.language, self.focus_particles['en'])
        lang_contrast = self.contrastive_markers.get(self.language, self.contrastive_markers['en'])

        # Check for focus particles
        text_lower = text.lower()
        for particle in lang_focus:
            if particle in text_lower:
                # Word after focus particle is likely the focus
                idx = text_lower.find(particle)
                after_particle = text[idx + len(particle):].strip().split()[0] if idx >= 0 else None
                if after_particle:
                    focus = after_particle.strip('.,;:')

                    if particle in ('only', 'nur', 'seulement'):
                        focus_type = FocusType.EXHAUSTIVE_FOCUS
                    elif particle in ('even', 'sogar', 'même'):
                        focus_type = FocusType.CONTRASTIVE_FOCUS
                    break

        # If no focus particle, focus is typically the new information
        if not focus:
            new_entities = [e for e in entities if 'NEW' in e.given_new.name]
            if new_entities:
                focus = new_entities[-1].text  # Last new entity often carries focus
                focus_type = FocusType.INFORMATION_FOCUS

        # Check for contrastive focus
        if any(marker in text_lower for marker in lang_contrast):
            focus_type = FocusType.CONTRASTIVE_FOCUS

        # Background is given information
        given_entities = [e for e in entities if 'GIVEN' in e.given_new.name]
        if given_entities:
            background = ', '.join([e.text for e in given_entities])

        return focus, focus_type, background

    # =========================================================================
    # INFORMATION FLOW ANALYSIS
    # =========================================================================

    def _analyze_flow(
        self,
        units: List[InformationUnitAnalysis],
        entity_mentions: Dict[str, List[EntityMention]]
    ) -> InformationFlowAnalysis:
        """Analyze information flow across the text."""

        # Extract topic and focus chains
        topic_chain = [u.topic for u in units if u.topic]
        focus_chain = [u.focus for u in units if u.focus]

        # Determine progression type
        progression_type = self._determine_progression(units)

        # Calculate given ratio
        total_entities = sum(len(u.entities) for u in units)
        given_entities = sum(
            len([e for e in u.entities if 'GIVEN' in e.given_new.name])
            for u in units
        )
        given_ratio = given_entities / total_entities if total_entities > 0 else 0

        # Calculate new entity introduction rate
        new_introductions = sum(
            len([e for e in u.entities if e.is_first_mention])
            for u in units
        )
        new_rate = new_introductions / len(units) if units else 0

        return InformationFlowAnalysis(
            progression_type=progression_type,
            topic_chain=topic_chain,
            focus_chain=focus_chain,
            given_ratio=given_ratio,
            new_introduction_rate=new_rate
        )

    def _determine_progression(
        self,
        units: List[InformationUnitAnalysis]
    ) -> str:
        """Determine thematic progression type."""

        if len(units) < 2:
            return "unknown"

        topics = [u.topic.lower() if u.topic else "" for u in units]

        # Check for constant progression (same topic)
        if len(set(topics)) == 1 and topics[0]:
            return "constant"

        # Check for linear progression (rheme -> theme)
        # Simplified: check if focus of one sentence becomes topic of next
        linear_count = 0
        for i in range(len(units) - 1):
            if units[i].focus and units[i + 1].topic:
                if units[i].focus.lower() in units[i + 1].topic.lower():
                    linear_count += 1

        if linear_count >= len(units) // 2:
            return "linear"

        # Check for derived progression (topics related to hypertheme)
        # Simplified: check if topics share common words
        topic_words = set()
        for t in topics:
            topic_words.update(t.split())

        if len(topic_words) < len(topics) * 2:  # Topics share vocabulary
            return "derived"

        return "mixed"

    # =========================================================================
    # METRICS
    # =========================================================================

    def _calculate_metrics(
        self,
        analysis: InformationStructureAnalysis
    ) -> Dict[str, float]:
        """Calculate information structure metrics."""
        metrics = {}

        # Given/New balance
        if analysis.flow:
            metrics['given_ratio'] = analysis.flow.given_ratio
            metrics['new_introduction_rate'] = analysis.flow.new_introduction_rate

        # Topic continuity (how often topic is repeated)
        if analysis.units:
            topics = [u.topic for u in analysis.units if u.topic]
            if topics:
                unique_topics = len(set(t.lower() for t in topics))
                metrics['topic_continuity'] = 1 - (unique_topics / len(topics))

        # Focus diversity
        foci = [u.focus for u in analysis.units if u.focus]
        if foci:
            unique_foci = len(set(f.lower() for f in foci))
            metrics['focus_diversity'] = unique_foci / len(foci)

        # Entity density
        total_entities = sum(len(u.entities) for u in analysis.units)
        metrics['entity_density'] = total_entities / analysis.sentence_count if analysis.sentence_count > 0 else 0

        # Reference chain length (average mentions per entity)
        if analysis.entity_registry:
            chain_lengths = [len(mentions) for mentions in analysis.entity_registry.values()]
            metrics['avg_chain_length'] = sum(chain_lengths) / len(chain_lengths)

        # Information structure score (balanced given/new, clear topics)
        given_score = min(analysis.flow.given_ratio / 0.5, 1.0) if analysis.flow else 0
        topic_score = metrics.get('topic_continuity', 0.5)
        metrics['information_structure_score'] = (given_score + topic_score) / 2

        return metrics

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def _split_sentences(self, text: str) -> List[str]:
        """Basic sentence splitting."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def get_report(self, analysis: InformationStructureAnalysis) -> str:
        """Generate a human-readable report."""
        m = analysis.metrics
        f = analysis.flow

        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║  INFORMATION STRUCTURE ANALYSIS                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Text Statistics                                                     ║
║  ├── Sentences: {analysis.sentence_count:<10}                                        ║
║  ├── Entities tracked: {len(analysis.entity_registry):<10}                               ║
║  └── Total mentions: {sum(len(v) for v in analysis.entity_registry.values()):<10}                                 ║
║                                                                      ║
║  INFORMATION FLOW                                                    ║
║  ├── Progression Type: {f.progression_type if f else 'N/A':<15}                          ║
║  ├── Given Ratio: {m.get('given_ratio', 0):.2%}                                        ║
║  ├── New Introduction Rate: {m.get('new_introduction_rate', 0):.2f} per sentence            ║
║  └── Topic Continuity: {m.get('topic_continuity', 0):.2%}                               ║
║                                                                      ║
║  TOPIC CHAIN (first 5):                                              ║"""

        if f and f.topic_chain:
            for i, topic in enumerate(f.topic_chain[:5]):
                report += f"\n║  │  {i+1}. {topic[:40]:<45}║"
        else:
            report += "\n║  │  (no topics extracted)                                      ║"

        report += f"""
║                                                                      ║
║  METRICS                                                             ║
║  ├── Entity Density: {m.get('entity_density', 0):.2f} per sentence                      ║
║  ├── Avg Chain Length: {m.get('avg_chain_length', 0):.2f} mentions                        ║
║  └── Info Structure Score: {m.get('information_structure_score', 0):.2f}                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""
        return report


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description='SWSM Information Structure Analyzer (E6)'
    )
    parser.add_argument('--text', '-t', help='Text to analyze')
    parser.add_argument('--file', '-f', help='Input file')
    parser.add_argument('--language', '-l', default='en', choices=['en', 'de', 'fr'])
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--format', choices=['json', 'report'], default='report')

    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # Demo
        text = """
        Loss aversion describes people's tendency to prefer avoiding losses over
        acquiring equivalent gains. This phenomenon was first documented by
        Kahneman and Tversky. They conducted several experiments to demonstrate
        the effect. The results showed that losses loom larger than gains.

        However, recent research has questioned the universality of loss aversion.
        Some studies suggest that experienced traders show reduced sensitivity.
        These findings have important implications for policy design.
        """

    analyzer = InformationStructureAnalyzer(args.language)
    analysis = analyzer.analyze(text)

    if args.format == 'json':
        result = analysis.to_dict()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Saved to {args.output}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(analyzer.get_report(analysis))


if __name__ == '__main__':
    main()
