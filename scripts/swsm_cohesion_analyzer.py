#!/usr/bin/env python3
"""
SWSM Cohesion Analyzer (E5)
===========================

Analyzes textual cohesion following Halliday & Hasan (1976).

Cohesion Types:
1. GRAMMATICAL COHESION
   - Reference (anaphoric, cataphoric, exophoric)
   - Substitution (nominal, verbal, clausal)
   - Ellipsis (nominal, verbal, clausal)
   - Conjunction (additive, adversative, causal, temporal)

2. LEXICAL COHESION
   - Repetition (exact, partial, paraphrase)
   - Synonymy (near-synonyms)
   - Hyponymy (superordinate/hyponym)
   - Meronymy (whole/part)
   - Collocation (habitual co-occurrence)

Implements SWSM Axioms:
- SWSM-11: Cohesion Continuity
- SWSM-12: Thematic Progression

References:
- Halliday & Hasan (1976): Cohesion in English
- Martin (1992): English Text
- Tanskanen (2006): Collaborating towards Coherence

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
# ENUMS: COHESION CATEGORIES
# =============================================================================

class ReferenceType(Enum):
    """Types of reference (Halliday & Hasan 1976)."""
    ANAPHORIC = "anaphoric"      # Refers back
    CATAPHORIC = "cataphoric"    # Refers forward
    EXOPHORIC = "exophoric"      # Refers outside text
    COMPARATIVE = "comparative"  # Comparative reference


class ReferenceCategory(Enum):
    """Categories of referring expressions."""
    PERSONAL = "personal"        # he, she, it, they
    DEMONSTRATIVE = "demonstrative"  # this, that, these, those
    COMPARATIVE = "comparative"  # same, similar, other, different
    DEFINITE = "definite"        # the + NP


class ConjunctionType(Enum):
    """Types of conjunction (cohesive connectors)."""
    ADDITIVE = "additive"        # and, also, moreover, furthermore
    ADVERSATIVE = "adversative"  # but, however, yet, nevertheless
    CAUSAL = "causal"            # so, therefore, because, thus
    TEMPORAL = "temporal"        # then, next, finally, meanwhile
    CONTINUATIVE = "continuative"  # well, now, anyway, of course


class LexicalCohesionType(Enum):
    """Types of lexical cohesion."""
    REPETITION = "repetition"        # Same word/lemma
    SYNONYMY = "synonymy"            # Similar meaning
    HYPONYMY = "hyponymy"            # Is-a relation
    MERONYMY = "meronymy"            # Part-of relation
    ANTONYMY = "antonymy"            # Opposite meaning
    COLLOCATION = "collocation"      # Habitual co-occurrence


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ReferenceLink:
    """A reference link between two expressions."""
    source_span: Tuple[int, int]  # (start, end) in text
    source_text: str
    target_span: Optional[Tuple[int, int]]  # None for exophoric
    target_text: Optional[str]
    reference_type: ReferenceType
    reference_category: ReferenceCategory
    sentence_distance: int = 0  # 0 = same sentence
    confidence: float = 1.0


@dataclass
class ReferenceChain:
    """A chain of coreferent mentions."""
    chain_id: str
    mentions: List[Dict[str, Any]]  # List of mentions with positions
    head_mention: str  # The "anchor" of the chain
    chain_length: int = 0
    span_sentences: int = 0  # How many sentences the chain spans


@dataclass
class ConjunctionLink:
    """A conjunction/connective linking text spans."""
    connector: str
    conjunction_type: ConjunctionType
    position: int  # Position in text
    sentence_index: int
    scope: str  # "clause" | "sentence" | "paragraph"


@dataclass
class LexicalLink:
    """A lexical cohesion link between two items."""
    source_word: str
    source_lemma: str
    source_position: int
    target_word: str
    target_lemma: str
    target_position: int
    link_type: LexicalCohesionType
    sentence_distance: int
    confidence: float = 1.0


@dataclass
class CohesionMetrics:
    """Aggregated cohesion metrics for a text."""
    # Reference metrics
    reference_chain_count: int = 0
    avg_chain_length: float = 0.0
    reference_density: float = 0.0  # Referring expressions per sentence

    # Conjunction metrics
    conjunction_count: int = 0
    conjunction_ratio: float = 0.0  # Per 100 words
    conjunction_distribution: Dict[str, int] = field(default_factory=dict)

    # Lexical cohesion metrics
    lexical_link_count: int = 0
    repetition_ratio: float = 0.0
    type_token_ratio: float = 0.0
    lexical_density: float = 0.0  # Content words / total words

    # Overall score
    cohesion_score: float = 0.0
    cohesion_level: str = "moderate"  # poor | moderate | good | excellent


@dataclass
class CohesionAnalysis:
    """Complete cohesion analysis of a text."""
    text: str
    sentence_count: int
    word_count: int

    # Grammatical cohesion
    reference_chains: List[ReferenceChain] = field(default_factory=list)
    reference_links: List[ReferenceLink] = field(default_factory=list)
    conjunctions: List[ConjunctionLink] = field(default_factory=list)

    # Lexical cohesion
    lexical_links: List[LexicalLink] = field(default_factory=list)

    # Metrics
    metrics: CohesionMetrics = field(default_factory=CohesionMetrics)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'text_stats': {
                'sentence_count': self.sentence_count,
                'word_count': self.word_count
            },
            'grammatical_cohesion': {
                'reference_chains': [
                    {
                        'chain_id': c.chain_id,
                        'head': c.head_mention,
                        'mentions': c.mentions,
                        'length': c.chain_length,
                        'span_sentences': c.span_sentences
                    }
                    for c in self.reference_chains
                ],
                'conjunctions': [
                    {
                        'connector': c.connector,
                        'type': c.conjunction_type.value,
                        'sentence': c.sentence_index
                    }
                    for c in self.conjunctions
                ]
            },
            'lexical_cohesion': {
                'links': [
                    {
                        'source': l.source_word,
                        'target': l.target_word,
                        'type': l.link_type.value,
                        'distance': l.sentence_distance
                    }
                    for l in self.lexical_links[:20]  # Limit output
                ]
            },
            'metrics': {
                'reference_chain_count': self.metrics.reference_chain_count,
                'avg_chain_length': round(self.metrics.avg_chain_length, 2),
                'reference_density': round(self.metrics.reference_density, 2),
                'conjunction_ratio': round(self.metrics.conjunction_ratio, 2),
                'conjunction_distribution': self.metrics.conjunction_distribution,
                'type_token_ratio': round(self.metrics.type_token_ratio, 2),
                'lexical_density': round(self.metrics.lexical_density, 2),
                'cohesion_score': round(self.metrics.cohesion_score, 2),
                'cohesion_level': self.metrics.cohesion_level
            }
        }


# =============================================================================
# COHESION ANALYZER
# =============================================================================

class CohesionAnalyzer:
    """
    Analyzes textual cohesion following Halliday & Hasan (1976).

    Supports:
    - Reference chain detection
    - Conjunction/connector analysis
    - Lexical cohesion (repetition, synonymy)
    - Quantitative cohesion metrics
    """

    def __init__(self, language: str = 'en'):
        """
        Initialize the cohesion analyzer.

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
                logger.warning(f"spaCy model {model_name} not found. Using basic analysis.")
        except ImportError:
            logger.warning("spaCy not available. Using basic analysis.")

        # Initialize lexicons
        self._init_lexicons()

    def _init_lexicons(self):
        """Initialize cohesion marker lexicons."""

        # Personal pronouns (for reference)
        self.personal_pronouns = {
            'en': {
                'subject': ['i', 'you', 'he', 'she', 'it', 'we', 'they'],
                'object': ['me', 'you', 'him', 'her', 'it', 'us', 'them'],
                'possessive': ['my', 'your', 'his', 'her', 'its', 'our', 'their',
                              'mine', 'yours', 'hers', 'ours', 'theirs']
            },
            'de': {
                'subject': ['ich', 'du', 'er', 'sie', 'es', 'wir', 'ihr', 'sie'],
                'object': ['mich', 'dich', 'ihn', 'sie', 'es', 'uns', 'euch', 'sie'],
                'possessive': ['mein', 'dein', 'sein', 'ihr', 'unser', 'euer']
            },
            'fr': {
                'subject': ['je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles'],
                'object': ['me', 'te', 'le', 'la', 'nous', 'vous', 'les'],
                'possessive': ['mon', 'ton', 'son', 'notre', 'votre', 'leur']
            }
        }

        # Demonstratives (for reference)
        self.demonstratives = {
            'en': ['this', 'that', 'these', 'those', 'here', 'there', 'such'],
            'de': ['dieser', 'diese', 'dieses', 'jener', 'jene', 'jenes', 'solch'],
            'fr': ['ce', 'cet', 'cette', 'ces', 'ceci', 'cela', 'celui', 'celle']
        }

        # Conjunctions/Connectors by type
        self.connectors = {
            'en': {
                ConjunctionType.ADDITIVE: [
                    'and', 'also', 'moreover', 'furthermore', 'in addition',
                    'besides', 'additionally', 'likewise', 'similarly',
                    'as well', 'too', 'plus'
                ],
                ConjunctionType.ADVERSATIVE: [
                    'but', 'however', 'yet', 'nevertheless', 'nonetheless',
                    'on the other hand', 'in contrast', 'conversely',
                    'although', 'though', 'even though', 'whereas', 'while',
                    'despite', 'in spite of', 'still'
                ],
                ConjunctionType.CAUSAL: [
                    'so', 'therefore', 'thus', 'hence', 'consequently',
                    'as a result', 'because', 'since', 'for', 'due to',
                    'owing to', 'accordingly', 'for this reason'
                ],
                ConjunctionType.TEMPORAL: [
                    'then', 'next', 'after', 'afterwards', 'subsequently',
                    'finally', 'eventually', 'meanwhile', 'in the meantime',
                    'first', 'second', 'third', 'firstly', 'secondly',
                    'before', 'previously', 'earlier', 'later', 'soon',
                    'at first', 'at last', 'in the end'
                ],
                ConjunctionType.CONTINUATIVE: [
                    'well', 'now', 'anyway', 'anyhow', 'of course',
                    'after all', 'indeed', 'actually', 'in fact'
                ]
            },
            'de': {
                ConjunctionType.ADDITIVE: [
                    'und', 'auch', 'ausserdem', 'zudem', 'ferner',
                    'darüber hinaus', 'ebenfalls', 'gleichfalls', 'ebenso'
                ],
                ConjunctionType.ADVERSATIVE: [
                    'aber', 'jedoch', 'doch', 'dennoch', 'trotzdem',
                    'hingegen', 'dagegen', 'obwohl', 'obgleich', 'während'
                ],
                ConjunctionType.CAUSAL: [
                    'also', 'daher', 'deshalb', 'deswegen', 'folglich',
                    'somit', 'weil', 'da', 'denn', 'aufgrund'
                ],
                ConjunctionType.TEMPORAL: [
                    'dann', 'danach', 'anschliessend', 'schliesslich',
                    'zuerst', 'erstens', 'zweitens', 'vorher', 'nachher',
                    'inzwischen', 'währenddessen'
                ],
                ConjunctionType.CONTINUATIVE: [
                    'nun', 'jedenfalls', 'natürlich', 'tatsächlich',
                    'eigentlich', 'übrigens'
                ]
            },
            'fr': {
                ConjunctionType.ADDITIVE: [
                    'et', 'aussi', 'de plus', 'en outre', 'également',
                    'de même', 'par ailleurs'
                ],
                ConjunctionType.ADVERSATIVE: [
                    'mais', 'cependant', 'pourtant', 'néanmoins', 'toutefois',
                    'en revanche', 'par contre', 'bien que', 'quoique'
                ],
                ConjunctionType.CAUSAL: [
                    'donc', 'ainsi', 'par conséquent', 'c\'est pourquoi',
                    'parce que', 'car', 'puisque', 'en raison de'
                ],
                ConjunctionType.TEMPORAL: [
                    'puis', 'ensuite', 'après', 'enfin', 'finalement',
                    'd\'abord', 'premièrement', 'avant', 'pendant'
                ],
                ConjunctionType.CONTINUATIVE: [
                    'eh bien', 'maintenant', 'en fait', 'effectivement',
                    'bien sûr', 'd\'ailleurs'
                ]
            }
        }

        # Content word POS tags
        self.content_pos = {'NOUN', 'VERB', 'ADJ', 'ADV'}

        # Function word POS tags
        self.function_pos = {'DET', 'ADP', 'CONJ', 'CCONJ', 'SCONJ', 'PART', 'PRON', 'AUX'}

    # =========================================================================
    # MAIN ANALYSIS METHOD
    # =========================================================================

    def analyze(self, text: str) -> CohesionAnalysis:
        """
        Perform complete cohesion analysis on a text.

        Args:
            text: Input text

        Returns:
            CohesionAnalysis with all cohesion features
        """
        # Parse text
        if self.nlp:
            doc = self.nlp(text)
            sentences = list(doc.sents)
            words = [token.text for token in doc if not token.is_space]
        else:
            sentences = self._split_sentences(text)
            words = text.split()

        sentence_count = len(sentences)
        word_count = len(words)

        # Create analysis object
        analysis = CohesionAnalysis(
            text=text,
            sentence_count=sentence_count,
            word_count=word_count
        )

        # Analyze grammatical cohesion
        analysis.reference_chains = self._analyze_reference_chains(text, sentences)
        analysis.reference_links = self._extract_reference_links(text, sentences)
        analysis.conjunctions = self._analyze_conjunctions(text, sentences)

        # Analyze lexical cohesion
        analysis.lexical_links = self._analyze_lexical_cohesion(text, sentences)

        # Calculate metrics
        analysis.metrics = self._calculate_metrics(analysis)

        return analysis

    # =========================================================================
    # REFERENCE ANALYSIS
    # =========================================================================

    def _analyze_reference_chains(
        self,
        text: str,
        sentences: List
    ) -> List[ReferenceChain]:
        """Identify reference chains (coreference)."""
        chains = []

        if self.nlp:
            doc = self.nlp(text)

            # Use simple heuristic: group by head noun
            noun_mentions: Dict[str, List[Dict]] = defaultdict(list)

            for sent_idx, sent in enumerate(doc.sents):
                for token in sent:
                    if token.pos_ in ('NOUN', 'PROPN'):
                        lemma = token.lemma_.lower()
                        noun_mentions[lemma].append({
                            'text': token.text,
                            'lemma': lemma,
                            'sentence': sent_idx,
                            'position': token.idx
                        })
                    # Track pronouns
                    elif token.pos_ == 'PRON' and token.text.lower() in self._get_all_pronouns():
                        # Simple: assign to most recent noun
                        if noun_mentions:
                            last_noun = list(noun_mentions.keys())[-1]
                            noun_mentions[last_noun].append({
                                'text': token.text,
                                'lemma': token.lemma_.lower(),
                                'sentence': sent_idx,
                                'position': token.idx,
                                'is_pronoun': True
                            })

            # Create chains from mentions
            chain_id = 0
            for head, mentions in noun_mentions.items():
                if len(mentions) >= 2:  # Only chains with 2+ mentions
                    chain_id += 1
                    sentences_spanned = len(set(m['sentence'] for m in mentions))
                    chains.append(ReferenceChain(
                        chain_id=f"RC-{chain_id:03d}",
                        mentions=mentions,
                        head_mention=head,
                        chain_length=len(mentions),
                        span_sentences=sentences_spanned
                    ))

        return chains

    def _extract_reference_links(
        self,
        text: str,
        sentences: List
    ) -> List[ReferenceLink]:
        """Extract individual reference links."""
        links = []
        lang_pronouns = self.personal_pronouns.get(self.language, self.personal_pronouns['en'])
        lang_demonstratives = self.demonstratives.get(self.language, self.demonstratives['en'])

        all_pronouns = set()
        for category in lang_pronouns.values():
            all_pronouns.update(category)

        if self.nlp:
            doc = self.nlp(text)

            for sent_idx, sent in enumerate(doc.sents):
                for token in sent:
                    token_lower = token.text.lower()

                    # Personal pronouns
                    if token_lower in all_pronouns:
                        links.append(ReferenceLink(
                            source_span=(token.idx, token.idx + len(token.text)),
                            source_text=token.text,
                            target_span=None,  # Would need coreference resolution
                            target_text=None,
                            reference_type=ReferenceType.ANAPHORIC,
                            reference_category=ReferenceCategory.PERSONAL,
                            sentence_distance=0
                        ))

                    # Demonstratives
                    elif token_lower in lang_demonstratives:
                        links.append(ReferenceLink(
                            source_span=(token.idx, token.idx + len(token.text)),
                            source_text=token.text,
                            target_span=None,
                            target_text=None,
                            reference_type=ReferenceType.ANAPHORIC,
                            reference_category=ReferenceCategory.DEMONSTRATIVE,
                            sentence_distance=0
                        ))

                    # Definite article + noun (potential anaphoric reference)
                    elif token.pos_ == 'DET' and token.text.lower() in ('the', 'der', 'die', 'das', 'le', 'la'):
                        # Check if followed by noun
                        if token.head.pos_ == 'NOUN':
                            links.append(ReferenceLink(
                                source_span=(token.idx, token.head.idx + len(token.head.text)),
                                source_text=f"{token.text} {token.head.text}",
                                target_span=None,
                                target_text=None,
                                reference_type=ReferenceType.ANAPHORIC,
                                reference_category=ReferenceCategory.DEFINITE,
                                sentence_distance=0
                            ))

        return links

    def _get_all_pronouns(self) -> Set[str]:
        """Get all pronouns for current language."""
        all_pronouns = set()
        lang_pronouns = self.personal_pronouns.get(self.language, self.personal_pronouns['en'])
        for category in lang_pronouns.values():
            all_pronouns.update(category)
        return all_pronouns

    # =========================================================================
    # CONJUNCTION ANALYSIS
    # =========================================================================

    def _analyze_conjunctions(
        self,
        text: str,
        sentences: List
    ) -> List[ConjunctionLink]:
        """Identify and classify conjunctions/connectors."""
        conjunctions = []
        lang_connectors = self.connectors.get(self.language, self.connectors['en'])

        text_lower = text.lower()

        for sent_idx, sent in enumerate(sentences):
            sent_text = sent.text if hasattr(sent, 'text') else str(sent)
            sent_lower = sent_text.lower()

            for conj_type, markers in lang_connectors.items():
                for marker in markers:
                    # Check if marker appears in sentence
                    if marker in sent_lower:
                        # Find position
                        pos = sent_lower.find(marker)

                        # Determine scope
                        if pos < 5:  # At beginning
                            scope = "sentence"
                        else:
                            scope = "clause"

                        conjunctions.append(ConjunctionLink(
                            connector=marker,
                            conjunction_type=conj_type,
                            position=text_lower.find(sent_lower) + pos,
                            sentence_index=sent_idx,
                            scope=scope
                        ))

        return conjunctions

    # =========================================================================
    # LEXICAL COHESION ANALYSIS
    # =========================================================================

    def _analyze_lexical_cohesion(
        self,
        text: str,
        sentences: List
    ) -> List[LexicalLink]:
        """Analyze lexical cohesion (repetition, synonymy, etc.)."""
        links = []

        if not self.nlp:
            return self._analyze_lexical_basic(text, sentences)

        doc = self.nlp(text)

        # Collect content words by sentence
        sentence_words: List[List[Dict]] = []
        for sent_idx, sent in enumerate(doc.sents):
            words = []
            for token in sent:
                if token.pos_ in self.content_pos and len(token.text) > 2:
                    words.append({
                        'text': token.text,
                        'lemma': token.lemma_.lower(),
                        'pos': token.pos_,
                        'position': token.idx,
                        'sentence': sent_idx
                    })
            sentence_words.append(words)

        # Find lexical links between sentences
        for i in range(len(sentence_words)):
            for j in range(i + 1, min(i + 4, len(sentence_words))):  # Look ahead 3 sentences
                for word_i in sentence_words[i]:
                    for word_j in sentence_words[j]:
                        link_type = self._classify_lexical_link(word_i, word_j)
                        if link_type:
                            links.append(LexicalLink(
                                source_word=word_i['text'],
                                source_lemma=word_i['lemma'],
                                source_position=word_i['position'],
                                target_word=word_j['text'],
                                target_lemma=word_j['lemma'],
                                target_position=word_j['position'],
                                link_type=link_type,
                                sentence_distance=j - i,
                                confidence=0.8 if link_type == LexicalCohesionType.REPETITION else 0.6
                            ))

        return links

    def _analyze_lexical_basic(
        self,
        text: str,
        sentences: List
    ) -> List[LexicalLink]:
        """Basic lexical analysis without spaCy."""
        links = []

        # Simple repetition detection
        words_by_sentence: List[List[str]] = []
        for sent in sentences:
            sent_text = sent.text if hasattr(sent, 'text') else str(sent)
            words = [w.lower() for w in re.findall(r'\b\w{3,}\b', sent_text)]
            words_by_sentence.append(words)

        for i in range(len(words_by_sentence)):
            for j in range(i + 1, min(i + 4, len(words_by_sentence))):
                common = set(words_by_sentence[i]) & set(words_by_sentence[j])
                for word in common:
                    links.append(LexicalLink(
                        source_word=word,
                        source_lemma=word,
                        source_position=0,
                        target_word=word,
                        target_lemma=word,
                        target_position=0,
                        link_type=LexicalCohesionType.REPETITION,
                        sentence_distance=j - i
                    ))

        return links

    def _classify_lexical_link(
        self,
        word1: Dict,
        word2: Dict
    ) -> Optional[LexicalCohesionType]:
        """Classify the type of lexical link between two words."""

        # Exact repetition (same lemma)
        if word1['lemma'] == word2['lemma']:
            return LexicalCohesionType.REPETITION

        # Partial repetition (one contains the other)
        if word1['lemma'] in word2['lemma'] or word2['lemma'] in word1['lemma']:
            return LexicalCohesionType.REPETITION

        # Could add WordNet integration for synonymy/hyponymy here
        # For now, skip other types

        return None

    # =========================================================================
    # METRICS CALCULATION
    # =========================================================================

    def _calculate_metrics(self, analysis: CohesionAnalysis) -> CohesionMetrics:
        """Calculate aggregated cohesion metrics."""
        metrics = CohesionMetrics()

        # Reference metrics
        metrics.reference_chain_count = len(analysis.reference_chains)
        if analysis.reference_chains:
            metrics.avg_chain_length = sum(
                c.chain_length for c in analysis.reference_chains
            ) / len(analysis.reference_chains)

        metrics.reference_density = (
            len(analysis.reference_links) / analysis.sentence_count
            if analysis.sentence_count > 0 else 0
        )

        # Conjunction metrics
        metrics.conjunction_count = len(analysis.conjunctions)
        metrics.conjunction_ratio = (
            (metrics.conjunction_count / analysis.word_count) * 100
            if analysis.word_count > 0 else 0
        )

        # Distribution by type
        for conj in analysis.conjunctions:
            type_name = conj.conjunction_type.value
            metrics.conjunction_distribution[type_name] = (
                metrics.conjunction_distribution.get(type_name, 0) + 1
            )

        # Lexical metrics
        metrics.lexical_link_count = len(analysis.lexical_links)
        repetitions = sum(
            1 for l in analysis.lexical_links
            if l.link_type == LexicalCohesionType.REPETITION
        )
        metrics.repetition_ratio = (
            repetitions / analysis.sentence_count
            if analysis.sentence_count > 0 else 0
        )

        # Type-token ratio and lexical density
        if self.nlp:
            doc = self.nlp(analysis.text)
            tokens = [t for t in doc if not t.is_space and not t.is_punct]
            lemmas = set(t.lemma_.lower() for t in tokens)

            metrics.type_token_ratio = len(lemmas) / len(tokens) if tokens else 0

            content_words = sum(1 for t in tokens if t.pos_ in self.content_pos)
            metrics.lexical_density = content_words / len(tokens) if tokens else 0
        else:
            words = analysis.text.lower().split()
            unique = set(words)
            metrics.type_token_ratio = len(unique) / len(words) if words else 0
            metrics.lexical_density = 0.5  # Default

        # Calculate overall cohesion score
        metrics.cohesion_score = self._calculate_cohesion_score(metrics, analysis)

        # Determine level
        if metrics.cohesion_score >= 0.8:
            metrics.cohesion_level = "excellent"
        elif metrics.cohesion_score >= 0.6:
            metrics.cohesion_level = "good"
        elif metrics.cohesion_score >= 0.4:
            metrics.cohesion_level = "moderate"
        else:
            metrics.cohesion_level = "poor"

        return metrics

    def _calculate_cohesion_score(
        self,
        metrics: CohesionMetrics,
        analysis: CohesionAnalysis
    ) -> float:
        """
        Calculate overall cohesion score (0-1).

        Based on SWSM-Schema cohesion_metrics.aggregated.cohesion_score formula:
        C = w₁ × reference_chain_density
          + w₂ × conjunction_ratio_normalized
          + w₃ × lexical_repetition_index
          + w₄ × given_new_balance
        """
        weights = {
            'reference': 0.30,
            'conjunction': 0.25,
            'lexical': 0.25,
            'given_new': 0.20
        }

        # Normalize metrics to 0-1 scale

        # Reference chain density (optimal: 0.3-0.6 chains per sentence)
        ref_density = metrics.reference_chain_count / max(analysis.sentence_count, 1)
        ref_score = min(ref_density / 0.5, 1.0)  # Cap at 1.0

        # Conjunction ratio (optimal: 2-5 per 100 words)
        conj_normalized = min(metrics.conjunction_ratio / 3.5, 1.0)

        # Lexical repetition (optimal: moderate)
        lexical_score = min(metrics.repetition_ratio / 2.0, 1.0)

        # Given/New balance (approximate via reference density)
        given_new_score = min(metrics.reference_density / 3.0, 1.0)

        score = (
            weights['reference'] * ref_score +
            weights['conjunction'] * conj_normalized +
            weights['lexical'] * lexical_score +
            weights['given_new'] * given_new_score
        )

        return min(max(score, 0.0), 1.0)

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def _split_sentences(self, text: str) -> List[str]:
        """Basic sentence splitting."""
        # Simple split on sentence-ending punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def get_cohesion_report(self, analysis: CohesionAnalysis) -> str:
        """Generate a human-readable cohesion report."""
        m = analysis.metrics

        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║  COHESION ANALYSIS REPORT                                            ║
╠══════════════════════════════════════════════════════════════════════╣
║  Text Statistics                                                     ║
║  ├── Sentences: {analysis.sentence_count:<10} Words: {analysis.word_count:<10}               ║
║                                                                      ║
║  GRAMMATICAL COHESION                                                ║
║  ├── Reference Chains: {m.reference_chain_count:<5} (avg length: {m.avg_chain_length:.1f})              ║
║  ├── Reference Density: {m.reference_density:.2f} per sentence                      ║
║  ├── Conjunctions: {m.conjunction_count:<5} (ratio: {m.conjunction_ratio:.2f}/100 words)            ║
║  │   ├── Additive: {m.conjunction_distribution.get('additive', 0):<5}                                     ║
║  │   ├── Adversative: {m.conjunction_distribution.get('adversative', 0):<5}                                  ║
║  │   ├── Causal: {m.conjunction_distribution.get('causal', 0):<5}                                       ║
║  │   └── Temporal: {m.conjunction_distribution.get('temporal', 0):<5}                                     ║
║                                                                      ║
║  LEXICAL COHESION                                                    ║
║  ├── Lexical Links: {m.lexical_link_count:<5}                                        ║
║  ├── Repetition Ratio: {m.repetition_ratio:.2f} per sentence                       ║
║  ├── Type-Token Ratio: {m.type_token_ratio:.2f}                                     ║
║  └── Lexical Density: {m.lexical_density:.2f}                                      ║
║                                                                      ║
║  OVERALL SCORE                                                       ║
║  └── Cohesion Score: {m.cohesion_score:.2f} ({m.cohesion_level.upper()})                          ║
╚══════════════════════════════════════════════════════════════════════╝
"""
        return report


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface for Cohesion Analyzer."""
    import argparse

    parser = argparse.ArgumentParser(
        description='SWSM Cohesion Analyzer (E5) - Textual cohesion analysis'
    )
    parser.add_argument(
        '--text', '-t',
        help='Text to analyze'
    )
    parser.add_argument(
        '--file', '-f',
        help='Input file path'
    )
    parser.add_argument(
        '--language', '-l',
        default='en',
        choices=['en', 'de', 'fr'],
        help='Language (default: en)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file (JSON)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'report'],
        default='report',
        help='Output format'
    )

    args = parser.parse_args()

    # Get input text
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # Demo text
        text = """
        Loss aversion is a cornerstone of behavioral economics. It describes the
        tendency for people to prefer avoiding losses over acquiring equivalent gains.
        This phenomenon was first documented by Kahneman and Tversky in 1979.

        However, recent research suggests that loss aversion may be context-dependent.
        For example, experienced traders show reduced loss aversion compared to novices.
        Therefore, the effect appears to be modulated by expertise and familiarity.

        These findings have important implications for policy design. Policymakers
        should consider individual differences when implementing behavioral interventions.
        """

    # Analyze
    analyzer = CohesionAnalyzer(language=args.language)
    analysis = analyzer.analyze(text)

    # Output
    if args.format == 'json':
        result = analysis.to_dict()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Analysis saved to {args.output}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(analyzer.get_cohesion_report(analysis))


if __name__ == '__main__':
    main()
