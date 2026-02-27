#!/usr/bin/env python3
"""
SWSM E2: RST Discourse Parser
=============================

Automatic RST (Rhetorical Structure Theory) tree construction from text.

This component implements:
- EDU (Elementary Discourse Unit) segmentation
- Discourse relation classification
- Hierarchical RST tree building
- Integration with SWSM pipeline

Axioms implemented:
- SWSM-3 (RST Hierarchy): Text organizes into nucleus-satellite structures
- SWSM-4 (Relation Taxonomy): 23 relation types following Mann & Thompson
- SWSM-11 (Discourse Coherence): Valid RST trees ensure textual coherence

References:
- Mann & Thompson (1988): Rhetorical Structure Theory
- Carlson et al. (2001): RST Discourse Treebank
- Ji & Eisenstein (2014): Representation Learning for RST
- Feng & Hirst (2014): Linear-time RST parsing

Author: SWSM Framework
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Tuple, Set, Any
import re
from collections import defaultdict


# =============================================================================
# ENUMERATIONS
# =============================================================================

class RelationType(Enum):
    """
    RST relation types following Mann & Thompson (1988) taxonomy.
    Extended with additional relations from RST-DT corpus.
    """
    # Subject Matter Relations (Presentational)
    ELABORATION = "elaboration"
    CIRCUMSTANCE = "circumstance"
    SOLUTIONHOOD = "solutionhood"
    VOLITIONAL_CAUSE = "volitional-cause"
    VOLITIONAL_RESULT = "volitional-result"
    NON_VOLITIONAL_CAUSE = "non-volitional-cause"
    NON_VOLITIONAL_RESULT = "non-volitional-result"
    PURPOSE = "purpose"
    CONDITION = "condition"
    OTHERWISE = "otherwise"
    INTERPRETATION = "interpretation"
    EVALUATION = "evaluation"
    RESTATEMENT = "restatement"
    SUMMARY = "summary"
    SEQUENCE = "sequence"
    CONTRAST = "contrast"

    # Presentational Relations
    MOTIVATION = "motivation"
    ANTITHESIS = "antithesis"
    BACKGROUND = "background"
    ENABLEMENT = "enablement"
    EVIDENCE = "evidence"
    JUSTIFY = "justify"
    CONCESSION = "concession"

    # Multinuclear Relations
    CONJUNCTION = "conjunction"
    DISJUNCTION = "disjunction"
    LIST = "list"
    JOINT = "joint"

    # Special
    SAME_UNIT = "same-unit"
    TEXTUAL_ORGANIZATION = "textual-organization"
    ATTRIBUTION = "attribution"
    MANNER_MEANS = "manner-means"
    COMPARISON = "comparison"
    TOPIC_COMMENT = "topic-comment"
    PROBLEM_SOLUTION = "problem-solution"
    QUESTION_ANSWER = "question-answer"
    STATEMENT_RESPONSE = "statement-response"
    TOPIC_SHIFT = "topic-shift"
    COMMENT = "comment"


class NuclearityType(Enum):
    """Nuclearity status in RST relations."""
    NUCLEUS = "nucleus"
    SATELLITE = "satellite"
    MULTINUCLEAR = "multinuclear"


class EDUType(Enum):
    """Types of Elementary Discourse Units."""
    CLAUSE = "clause"
    SENTENCE = "sentence"
    FRAGMENT = "fragment"
    EMBEDDED = "embedded"


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class EDU:
    """Elementary Discourse Unit - the minimal unit of discourse."""
    id: str
    text: str
    start_char: int
    end_char: int
    edu_type: EDUType = EDUType.CLAUSE
    sentence_id: Optional[int] = None
    clause_id: Optional[int] = None
    # Linguistic features for relation classification
    has_discourse_marker: bool = False
    discourse_marker: Optional[str] = None
    tense: Optional[str] = None
    mood: Optional[str] = None
    contains_pronoun: bool = False
    is_question: bool = False
    is_imperative: bool = False

    def __repr__(self):
        return f"EDU({self.id}: '{self.text[:30]}...')" if len(self.text) > 30 else f"EDU({self.id}: '{self.text}')"


@dataclass
class RSTRelation:
    """A rhetorical relation between discourse units."""
    relation_type: RelationType
    nucleus_ids: List[str]  # Can be multiple for multinuclear
    satellite_ids: List[str] = field(default_factory=list)
    confidence: float = 1.0
    signals: List[str] = field(default_factory=list)  # Discourse markers, cue phrases

    @property
    def is_multinuclear(self) -> bool:
        return len(self.nucleus_ids) > 1 and len(self.satellite_ids) == 0


@dataclass
class RSTNode:
    """A node in the RST tree."""
    id: str
    nuclearity: NuclearityType
    relation: Optional[RelationType] = None
    edu: Optional[EDU] = None  # Leaf nodes have EDUs
    children: List['RSTNode'] = field(default_factory=list)
    parent: Optional['RSTNode'] = None
    span: Tuple[int, int] = (0, 0)  # EDU span (start_idx, end_idx)

    @property
    def is_leaf(self) -> bool:
        return self.edu is not None

    @property
    def text(self) -> str:
        if self.is_leaf:
            return self.edu.text
        return " ".join(child.text for child in self.children)

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        result = {
            'id': self.id,
            'nuclearity': self.nuclearity.value,
            'span': self.span,
        }
        if self.relation:
            result['relation'] = self.relation.value
        if self.is_leaf:
            result['edu'] = {
                'id': self.edu.id,
                'text': self.edu.text,
                'type': self.edu.edu_type.value
            }
        else:
            result['children'] = [child.to_dict() for child in self.children]
        return result


@dataclass
class RSTTree:
    """Complete RST tree for a text."""
    root: RSTNode
    edus: List[EDU]
    relations: List[RSTRelation]
    metadata: Dict = field(default_factory=dict)

    @property
    def num_edus(self) -> int:
        return len(self.edus)

    @property
    def depth(self) -> int:
        """Calculate tree depth."""
        def _depth(node: RSTNode) -> int:
            if node.is_leaf:
                return 1
            return 1 + max(_depth(child) for child in node.children)
        return _depth(self.root)

    def get_relations_by_type(self, rel_type: RelationType) -> List[RSTRelation]:
        """Get all relations of a specific type."""
        return [r for r in self.relations if r.relation_type == rel_type]

    def to_dict(self) -> Dict:
        """Convert to dictionary representation."""
        return {
            'root': self.root.to_dict(),
            'num_edus': self.num_edus,
            'depth': self.depth,
            'relations': [
                {
                    'type': r.relation_type.value,
                    'nucleus_ids': r.nucleus_ids,
                    'satellite_ids': r.satellite_ids,
                    'confidence': r.confidence,
                    'signals': r.signals
                }
                for r in self.relations
            ],
            'metadata': self.metadata
        }

    def to_bracket_notation(self) -> str:
        """Convert to bracket notation (RST-DT format)."""
        def _to_bracket(node: RSTNode) -> str:
            if node.is_leaf:
                return f"(leaf {node.edu.id})"
            rel = node.relation.value if node.relation else "span"
            nuc = node.nuclearity.value
            children_str = " ".join(_to_bracket(c) for c in node.children)
            return f"({rel} ({nuc} {children_str}))"
        return _to_bracket(self.root)


# =============================================================================
# DISCOURSE MARKERS
# =============================================================================

class DiscourseMarkerLexicon:
    """Lexicon of discourse markers and their associated relations."""

    # Discourse markers mapped to likely relations
    MARKERS = {
        # Causal
        'because': [RelationType.VOLITIONAL_CAUSE, RelationType.NON_VOLITIONAL_CAUSE],
        'since': [RelationType.VOLITIONAL_CAUSE, RelationType.BACKGROUND],
        'as': [RelationType.VOLITIONAL_CAUSE, RelationType.CIRCUMSTANCE],
        'so': [RelationType.VOLITIONAL_RESULT, RelationType.NON_VOLITIONAL_RESULT],
        'therefore': [RelationType.VOLITIONAL_RESULT, RelationType.NON_VOLITIONAL_RESULT],
        'thus': [RelationType.VOLITIONAL_RESULT, RelationType.NON_VOLITIONAL_RESULT],
        'consequently': [RelationType.VOLITIONAL_RESULT],
        'hence': [RelationType.VOLITIONAL_RESULT],
        'as a result': [RelationType.VOLITIONAL_RESULT, RelationType.NON_VOLITIONAL_RESULT],
        'due to': [RelationType.NON_VOLITIONAL_CAUSE],
        'owing to': [RelationType.NON_VOLITIONAL_CAUSE],

        # Contrast/Concession
        'but': [RelationType.CONTRAST, RelationType.CONCESSION],
        'however': [RelationType.CONTRAST, RelationType.CONCESSION],
        'although': [RelationType.CONCESSION],
        'though': [RelationType.CONCESSION],
        'even though': [RelationType.CONCESSION],
        'despite': [RelationType.CONCESSION],
        'in spite of': [RelationType.CONCESSION],
        'nevertheless': [RelationType.CONCESSION],
        'nonetheless': [RelationType.CONCESSION],
        'yet': [RelationType.CONTRAST, RelationType.CONCESSION],
        'while': [RelationType.CONTRAST, RelationType.CIRCUMSTANCE],
        'whereas': [RelationType.CONTRAST],
        'on the other hand': [RelationType.CONTRAST],
        'in contrast': [RelationType.CONTRAST],
        'conversely': [RelationType.CONTRAST],

        # Elaboration/Addition
        'moreover': [RelationType.ELABORATION, RelationType.CONJUNCTION],
        'furthermore': [RelationType.ELABORATION, RelationType.CONJUNCTION],
        'in addition': [RelationType.ELABORATION, RelationType.CONJUNCTION],
        'additionally': [RelationType.ELABORATION, RelationType.CONJUNCTION],
        'also': [RelationType.ELABORATION, RelationType.CONJUNCTION],
        'besides': [RelationType.ELABORATION],
        'for example': [RelationType.ELABORATION, RelationType.EVIDENCE],
        'for instance': [RelationType.ELABORATION, RelationType.EVIDENCE],
        'such as': [RelationType.ELABORATION],
        'specifically': [RelationType.ELABORATION],
        'in particular': [RelationType.ELABORATION],
        'namely': [RelationType.ELABORATION],
        'that is': [RelationType.RESTATEMENT],
        'in other words': [RelationType.RESTATEMENT],
        'i.e.': [RelationType.RESTATEMENT],

        # Temporal/Sequence
        'then': [RelationType.SEQUENCE],
        'next': [RelationType.SEQUENCE],
        'first': [RelationType.SEQUENCE, RelationType.LIST],
        'second': [RelationType.SEQUENCE, RelationType.LIST],
        'third': [RelationType.SEQUENCE, RelationType.LIST],
        'finally': [RelationType.SEQUENCE],
        'subsequently': [RelationType.SEQUENCE],
        'afterwards': [RelationType.SEQUENCE],
        'meanwhile': [RelationType.SEQUENCE, RelationType.CIRCUMSTANCE],
        'before': [RelationType.SEQUENCE, RelationType.CIRCUMSTANCE],
        'after': [RelationType.SEQUENCE, RelationType.CIRCUMSTANCE],
        'when': [RelationType.CIRCUMSTANCE],
        'while': [RelationType.CIRCUMSTANCE],

        # Condition
        'if': [RelationType.CONDITION],
        'unless': [RelationType.CONDITION, RelationType.OTHERWISE],
        'provided that': [RelationType.CONDITION],
        'assuming': [RelationType.CONDITION],
        'in case': [RelationType.CONDITION],
        'otherwise': [RelationType.OTHERWISE],

        # Purpose
        'in order to': [RelationType.PURPOSE],
        'so that': [RelationType.PURPOSE],
        'to': [RelationType.PURPOSE],  # infinitive marker
        'for': [RelationType.PURPOSE],

        # Evidence/Justify
        'indeed': [RelationType.EVIDENCE],
        'in fact': [RelationType.EVIDENCE],
        'actually': [RelationType.EVIDENCE],

        # Summary/Conclusion
        'in conclusion': [RelationType.SUMMARY],
        'in summary': [RelationType.SUMMARY],
        'to summarize': [RelationType.SUMMARY],
        'overall': [RelationType.SUMMARY],
        'in short': [RelationType.SUMMARY],
        'to conclude': [RelationType.SUMMARY],

        # Background
        'as mentioned': [RelationType.BACKGROUND],
        'as noted': [RelationType.BACKGROUND],
        'as stated': [RelationType.BACKGROUND],
    }

    # Markers that typically signal multinuclear relations
    MULTINUCLEAR_MARKERS = {
        'and': RelationType.CONJUNCTION,
        'or': RelationType.DISJUNCTION,
        'first': RelationType.LIST,
        'second': RelationType.LIST,
        'on one hand': RelationType.CONTRAST,
        'on the other hand': RelationType.CONTRAST,
    }

    @classmethod
    def find_markers(cls, text: str) -> List[Tuple[str, List[RelationType]]]:
        """Find all discourse markers in text."""
        text_lower = text.lower()
        found = []

        # Sort by length (longer first) to match multi-word markers
        sorted_markers = sorted(cls.MARKERS.keys(), key=len, reverse=True)

        for marker in sorted_markers:
            if marker in text_lower:
                # Check word boundaries
                pattern = r'\b' + re.escape(marker) + r'\b'
                if re.search(pattern, text_lower):
                    found.append((marker, cls.MARKERS[marker]))

        return found

    @classmethod
    def get_likely_relation(cls, marker: str) -> Optional[RelationType]:
        """Get most likely relation for a marker."""
        if marker.lower() in cls.MARKERS:
            return cls.MARKERS[marker.lower()][0]
        return None


# =============================================================================
# EDU SEGMENTER
# =============================================================================

class EDUSegmenter:
    """
    Segments text into Elementary Discourse Units (EDUs).

    Uses a combination of:
    - Sentence boundary detection
    - Clause boundary detection (coordinating/subordinating conjunctions)
    - Discourse marker positions
    - Punctuation patterns
    """

    # Clause boundary patterns
    CLAUSE_BOUNDARIES = [
        r',\s+(?:and|but|or|so|yet)\s+',  # Coordinating conjunctions with comma
        r'\s+(?:because|since|although|though|while|when|if|unless|after|before)\s+',  # Subordinating
        r';\s+',  # Semicolon
        r'\s+--\s+',  # Em-dash
        r':\s+(?=[A-Z])',  # Colon followed by capital
    ]

    # Patterns that should NOT be split
    NO_SPLIT_PATTERNS = [
        r'\d+,\d+',  # Numbers with commas
        r'[A-Z]\.\s+[A-Z]',  # Initials
        r'(?:Mr|Mrs|Ms|Dr|Prof)\.',  # Titles
        r'e\.g\.',
        r'i\.e\.',
        r'etc\.',
    ]

    def __init__(self, min_edu_length: int = 3):
        """
        Initialize segmenter.

        Args:
            min_edu_length: Minimum number of words for an EDU
        """
        self.min_edu_length = min_edu_length

    def segment(self, text: str) -> List[EDU]:
        """
        Segment text into EDUs.

        Args:
            text: Input text

        Returns:
            List of EDU objects
        """
        edus = []

        # First, split into sentences
        sentences = self._split_sentences(text)

        edu_counter = 0
        char_offset = 0

        for sent_idx, sentence in enumerate(sentences):
            # Find sentence position in original text
            sent_start = text.find(sentence, char_offset)
            if sent_start == -1:
                sent_start = char_offset

            # Segment sentence into clauses
            clauses = self._split_clauses(sentence)

            for clause_idx, clause in enumerate(clauses):
                clause = clause.strip()
                if not clause or len(clause.split()) < self.min_edu_length:
                    continue

                # Find clause position
                clause_start = text.find(clause, sent_start)
                if clause_start == -1:
                    clause_start = sent_start
                clause_end = clause_start + len(clause)

                # Detect discourse markers
                markers = DiscourseMarkerLexicon.find_markers(clause)
                has_marker = len(markers) > 0
                marker_text = markers[0][0] if markers else None

                # Detect linguistic features
                is_question = clause.strip().endswith('?')
                is_imperative = self._is_imperative(clause)
                contains_pronoun = bool(re.search(r'\b(he|she|it|they|this|that|these|those)\b', clause.lower()))

                edu = EDU(
                    id=f"edu_{edu_counter}",
                    text=clause,
                    start_char=clause_start,
                    end_char=clause_end,
                    edu_type=self._classify_edu_type(clause),
                    sentence_id=sent_idx,
                    clause_id=clause_idx,
                    has_discourse_marker=has_marker,
                    discourse_marker=marker_text,
                    contains_pronoun=contains_pronoun,
                    is_question=is_question,
                    is_imperative=is_imperative
                )
                edus.append(edu)
                edu_counter += 1

            char_offset = sent_start + len(sentence)

        return edus

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitter (could use NLTK/spaCy for production)
        # Handle abbreviations
        protected = text
        for pattern in self.NO_SPLIT_PATTERNS:
            protected = re.sub(pattern, lambda m: m.group().replace('.', '<DOT>'), protected)

        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', protected)

        # Restore dots
        sentences = [s.replace('<DOT>', '.') for s in sentences]

        return [s.strip() for s in sentences if s.strip()]

    def _split_clauses(self, sentence: str) -> List[str]:
        """Split sentence into clauses."""
        # Protect patterns that shouldn't be split
        protected = sentence
        for pattern in self.NO_SPLIT_PATTERNS:
            protected = re.sub(pattern, lambda m: m.group().replace(',', '<COMMA>'), protected)

        # Apply clause boundary patterns
        for pattern in self.CLAUSE_BOUNDARIES:
            protected = re.sub(pattern, '<SPLIT>\g<0>', protected, flags=re.IGNORECASE)

        # Split and restore
        clauses = protected.split('<SPLIT>')
        clauses = [c.replace('<COMMA>', ',').strip() for c in clauses]

        return [c for c in clauses if c]

    def _classify_edu_type(self, text: str) -> EDUType:
        """Classify the type of EDU."""
        text = text.strip()

        # Check for fragment (no verb)
        if not re.search(r'\b(is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|could|should|may|might|must|can|shall)\b', text.lower()):
            # Simple heuristic - could use POS tagging
            words = text.split()
            if len(words) < 5:
                return EDUType.FRAGMENT

        # Check for embedded clause
        if text.startswith('(') or text.startswith('['):
            return EDUType.EMBEDDED

        # Check if full sentence
        if text.endswith('.') or text.endswith('!') or text.endswith('?'):
            return EDUType.SENTENCE

        return EDUType.CLAUSE

    def _is_imperative(self, text: str) -> bool:
        """Check if clause is imperative."""
        text = text.strip().lower()
        # Simple heuristic: starts with verb
        imperative_starters = ['please', 'do', 'let', 'make', 'be', 'have', 'go', 'come', 'take', 'give']
        first_word = text.split()[0] if text.split() else ''
        return first_word in imperative_starters or text.endswith('!')


# =============================================================================
# RELATION CLASSIFIER
# =============================================================================

class RelationClassifier:
    """
    Classifies rhetorical relations between EDUs.

    Uses a combination of:
    - Discourse marker signals
    - Lexical patterns
    - Structural patterns
    - Semantic similarity (placeholder for embeddings)
    """

    def __init__(self):
        self.marker_lexicon = DiscourseMarkerLexicon()

    def classify(self, edu1: EDU, edu2: EDU, context: Optional[List[EDU]] = None) -> Tuple[RelationType, float, List[str]]:
        """
        Classify the relation between two EDUs.

        Args:
            edu1: First EDU (potential nucleus)
            edu2: Second EDU (potential satellite)
            context: Surrounding EDUs for context

        Returns:
            Tuple of (relation_type, confidence, signals)
        """
        signals = []
        candidates = []

        # 1. Check for discourse markers
        if edu2.has_discourse_marker and edu2.discourse_marker:
            marker_relations = self.marker_lexicon.MARKERS.get(edu2.discourse_marker.lower(), [])
            if marker_relations:
                for rel in marker_relations:
                    candidates.append((rel, 0.8, [f"marker:{edu2.discourse_marker}"]))

        # 2. Check structural patterns
        structural_rel, structural_conf, structural_signals = self._check_structural_patterns(edu1, edu2)
        if structural_rel:
            candidates.append((structural_rel, structural_conf, structural_signals))

        # 3. Check lexical patterns
        lexical_rel, lexical_conf, lexical_signals = self._check_lexical_patterns(edu1, edu2)
        if lexical_rel:
            candidates.append((lexical_rel, lexical_conf, lexical_signals))

        # 4. Check semantic patterns
        semantic_rel, semantic_conf, semantic_signals = self._check_semantic_patterns(edu1, edu2)
        if semantic_rel:
            candidates.append((semantic_rel, semantic_conf, semantic_signals))

        # Select best candidate
        if candidates:
            # Sort by confidence
            candidates.sort(key=lambda x: x[1], reverse=True)
            best = candidates[0]
            return best[0], best[1], best[2]

        # Default: ELABORATION (most common relation)
        return RelationType.ELABORATION, 0.5, ["default"]

    def _check_structural_patterns(self, edu1: EDU, edu2: EDU) -> Tuple[Optional[RelationType], float, List[str]]:
        """Check structural patterns for relation classification."""
        signals = []

        # Question-Answer pattern
        if edu1.is_question and not edu2.is_question:
            return RelationType.QUESTION_ANSWER, 0.9, ["question-answer-pattern"]

        # Same sentence = likely ELABORATION or CIRCUMSTANCE
        if edu1.sentence_id == edu2.sentence_id:
            if edu2.clause_id > edu1.clause_id:
                if edu2.text.lower().startswith(('which', 'who', 'that', 'where')):
                    return RelationType.ELABORATION, 0.7, ["relative-clause"]

        # Imperative followed by declarative = PURPOSE or MOTIVATION
        if edu1.is_imperative and not edu2.is_imperative:
            return RelationType.PURPOSE, 0.6, ["imperative-declarative"]

        return None, 0.0, []

    def _check_lexical_patterns(self, edu1: EDU, edu2: EDU) -> Tuple[Optional[RelationType], float, List[str]]:
        """Check lexical patterns for relation classification."""
        text1_lower = edu1.text.lower()
        text2_lower = edu2.text.lower()

        # Negation contrast
        if ('not' in text1_lower or "n't" in text1_lower) != ('not' in text2_lower or "n't" in text2_lower):
            return RelationType.CONTRAST, 0.6, ["negation-contrast"]

        # Temporal markers
        temporal_words = ['before', 'after', 'then', 'later', 'earlier', 'previously', 'subsequently']
        for word in temporal_words:
            if word in text2_lower:
                return RelationType.SEQUENCE, 0.7, [f"temporal:{word}"]

        # Causal verbs
        causal_verbs = ['cause', 'lead to', 'result in', 'because of', 'due to']
        for verb in causal_verbs:
            if verb in text2_lower:
                return RelationType.NON_VOLITIONAL_CAUSE, 0.7, [f"causal-verb:{verb}"]

        # Example markers
        example_markers = ['example', 'instance', 'such as', 'like', 'including']
        for marker in example_markers:
            if marker in text2_lower:
                return RelationType.ELABORATION, 0.75, [f"example:{marker}"]

        return None, 0.0, []

    def _check_semantic_patterns(self, edu1: EDU, edu2: EDU) -> Tuple[Optional[RelationType], float, List[str]]:
        """Check semantic patterns (placeholder for embedding-based classification)."""
        # Extract key content words
        words1 = set(re.findall(r'\b[a-z]{4,}\b', edu1.text.lower()))
        words2 = set(re.findall(r'\b[a-z]{4,}\b', edu2.text.lower()))

        # High word overlap = likely ELABORATION or RESTATEMENT
        if words1 and words2:
            overlap = len(words1 & words2) / max(len(words1), len(words2))
            if overlap > 0.5:
                return RelationType.ELABORATION, 0.6, [f"word-overlap:{overlap:.2f}"]
            if overlap > 0.7:
                return RelationType.RESTATEMENT, 0.7, [f"high-overlap:{overlap:.2f}"]

        return None, 0.0, []

    def classify_multinuclear(self, edus: List[EDU]) -> Tuple[RelationType, float, List[str]]:
        """
        Classify multinuclear relations between multiple EDUs.

        Args:
            edus: List of EDUs in potential multinuclear relation

        Returns:
            Tuple of (relation_type, confidence, signals)
        """
        if len(edus) < 2:
            return RelationType.JOINT, 0.5, []

        signals = []

        # Check for list markers
        list_markers = ['first', 'second', 'third', '1)', '2)', '3)', 'a)', 'b)', 'c)']
        has_list_markers = any(
            any(marker in edu.text.lower() for marker in list_markers)
            for edu in edus
        )
        if has_list_markers:
            return RelationType.LIST, 0.85, ["list-markers"]

        # Check for conjunction
        has_and = any('and' in edu.text.lower() for edu in edus[:-1])
        if has_and:
            return RelationType.CONJUNCTION, 0.8, ["conjunction-and"]

        # Check for disjunction
        has_or = any('or' in edu.text.lower() for edu in edus[:-1])
        if has_or:
            return RelationType.DISJUNCTION, 0.8, ["disjunction-or"]

        # Check for contrast markers
        contrast_markers = ['on one hand', 'on the other hand', 'while', 'whereas']
        has_contrast = any(
            any(marker in edu.text.lower() for marker in contrast_markers)
            for edu in edus
        )
        if has_contrast:
            return RelationType.CONTRAST, 0.8, ["contrast-markers"]

        # Default: JOINT
        return RelationType.JOINT, 0.5, ["default-multinuclear"]


# =============================================================================
# RST TREE BUILDER
# =============================================================================

class RSTTreeBuilder:
    """
    Builds RST trees from EDUs and relations using a shift-reduce parser.

    Implements a bottom-up parsing strategy:
    1. Start with EDUs as leaf nodes
    2. Greedily combine adjacent nodes based on relation strength
    3. Continue until a single root node remains
    """

    def __init__(self, relation_classifier: Optional[RelationClassifier] = None):
        """
        Initialize tree builder.

        Args:
            relation_classifier: Classifier for determining relations
        """
        self.classifier = relation_classifier or RelationClassifier()

    def build(self, edus: List[EDU]) -> RSTTree:
        """
        Build RST tree from list of EDUs.

        Args:
            edus: List of Elementary Discourse Units

        Returns:
            Complete RST tree
        """
        if not edus:
            raise ValueError("Cannot build tree from empty EDU list")

        if len(edus) == 1:
            # Single EDU - trivial tree
            root = RSTNode(
                id="node_0",
                nuclearity=NuclearityType.NUCLEUS,
                edu=edus[0],
                span=(0, 0)
            )
            return RSTTree(root=root, edus=edus, relations=[])

        # Create leaf nodes
        nodes = self._create_leaf_nodes(edus)
        relations = []

        # Bottom-up parsing
        node_counter = len(nodes)
        while len(nodes) > 1:
            # Find best pair to combine
            best_idx, best_rel, best_conf, best_signals, is_multinuc = self._find_best_combination(nodes)

            if best_idx is None:
                # Fallback: combine first two
                best_idx = 0
                best_rel = RelationType.JOINT
                best_conf = 0.3
                best_signals = ["fallback"]
                is_multinuc = True

            # Create new node
            if is_multinuc:
                # Multinuclear relation
                new_node = RSTNode(
                    id=f"node_{node_counter}",
                    nuclearity=NuclearityType.MULTINUCLEAR,
                    relation=best_rel,
                    children=[nodes[best_idx], nodes[best_idx + 1]],
                    span=(nodes[best_idx].span[0], nodes[best_idx + 1].span[1])
                )
                relation = RSTRelation(
                    relation_type=best_rel,
                    nucleus_ids=[nodes[best_idx].id, nodes[best_idx + 1].id],
                    confidence=best_conf,
                    signals=best_signals
                )
            else:
                # Nucleus-satellite relation
                # Determine which is nucleus (typically the first one)
                nucleus = nodes[best_idx]
                satellite = nodes[best_idx + 1]

                # Update nuclearity
                nucleus.nuclearity = NuclearityType.NUCLEUS
                satellite.nuclearity = NuclearityType.SATELLITE
                satellite.relation = best_rel

                new_node = RSTNode(
                    id=f"node_{node_counter}",
                    nuclearity=NuclearityType.NUCLEUS,
                    relation=best_rel,
                    children=[nucleus, satellite],
                    span=(nucleus.span[0], satellite.span[1])
                )
                relation = RSTRelation(
                    relation_type=best_rel,
                    nucleus_ids=[nucleus.id],
                    satellite_ids=[satellite.id],
                    confidence=best_conf,
                    signals=best_signals
                )

            # Set parent references
            for child in new_node.children:
                child.parent = new_node

            relations.append(relation)

            # Replace combined nodes with new node
            nodes = nodes[:best_idx] + [new_node] + nodes[best_idx + 2:]
            node_counter += 1

        root = nodes[0]
        return RSTTree(root=root, edus=edus, relations=relations)

    def _create_leaf_nodes(self, edus: List[EDU]) -> List[RSTNode]:
        """Create leaf nodes from EDUs."""
        return [
            RSTNode(
                id=f"node_{i}",
                nuclearity=NuclearityType.NUCLEUS,  # Initial default
                edu=edu,
                span=(i, i)
            )
            for i, edu in enumerate(edus)
        ]

    def _find_best_combination(self, nodes: List[RSTNode]) -> Tuple[Optional[int], RelationType, float, List[str], bool]:
        """
        Find best pair of adjacent nodes to combine.

        Returns:
            Tuple of (index, relation, confidence, signals, is_multinuclear)
        """
        best_idx = None
        best_rel = RelationType.JOINT
        best_conf = 0.0
        best_signals = []
        is_multinuc = True

        for i in range(len(nodes) - 1):
            node1 = nodes[i]
            node2 = nodes[i + 1]

            # Get EDUs for classification
            edu1 = self._get_rightmost_edu(node1)
            edu2 = self._get_leftmost_edu(node2)

            if edu1 and edu2:
                # Classify relation
                rel, conf, signals = self.classifier.classify(edu1, edu2)

                # Adjust confidence based on structural factors
                conf = self._adjust_confidence(conf, node1, node2)

                if conf > best_conf:
                    best_idx = i
                    best_rel = rel
                    best_conf = conf
                    best_signals = signals
                    # Determine if multinuclear
                    is_multinuc = rel in [
                        RelationType.CONJUNCTION,
                        RelationType.DISJUNCTION,
                        RelationType.LIST,
                        RelationType.JOINT,
                        RelationType.CONTRAST,
                        RelationType.SEQUENCE
                    ]

        return best_idx, best_rel, best_conf, best_signals, is_multinuc

    def _get_rightmost_edu(self, node: RSTNode) -> Optional[EDU]:
        """Get rightmost EDU in a subtree."""
        if node.is_leaf:
            return node.edu
        if node.children:
            return self._get_rightmost_edu(node.children[-1])
        return None

    def _get_leftmost_edu(self, node: RSTNode) -> Optional[EDU]:
        """Get leftmost EDU in a subtree."""
        if node.is_leaf:
            return node.edu
        if node.children:
            return self._get_leftmost_edu(node.children[0])
        return None

    def _adjust_confidence(self, conf: float, node1: RSTNode, node2: RSTNode) -> float:
        """Adjust confidence based on structural factors."""
        # Prefer combining smaller subtrees first
        size1 = node1.span[1] - node1.span[0] + 1
        size2 = node2.span[1] - node2.span[0] + 1

        # Slight penalty for very unbalanced combinations
        size_ratio = min(size1, size2) / max(size1, size2)
        conf *= (0.8 + 0.2 * size_ratio)

        # Bonus for same sentence
        edu1 = self._get_rightmost_edu(node1)
        edu2 = self._get_leftmost_edu(node2)
        if edu1 and edu2 and edu1.sentence_id == edu2.sentence_id:
            conf *= 1.1

        return min(conf, 1.0)


# =============================================================================
# MAIN RST PARSER
# =============================================================================

class RSTDiscourseParser:
    """
    Main RST Discourse Parser - E2 component of SWSM.

    Integrates EDU segmentation, relation classification, and tree building
    to produce complete RST analyses of texts.
    """

    def __init__(self, min_edu_length: int = 3):
        """
        Initialize parser.

        Args:
            min_edu_length: Minimum words for an EDU
        """
        self.segmenter = EDUSegmenter(min_edu_length=min_edu_length)
        self.classifier = RelationClassifier()
        self.tree_builder = RSTTreeBuilder(self.classifier)

    def parse(self, text: str) -> RSTTree:
        """
        Parse text into RST tree.

        Args:
            text: Input text

        Returns:
            RST tree structure
        """
        # Step 1: Segment into EDUs
        edus = self.segmenter.segment(text)

        if not edus:
            raise ValueError("No EDUs found in text")

        # Step 2: Build tree
        tree = self.tree_builder.build(edus)

        # Step 3: Add metadata
        tree.metadata = {
            'text_length': len(text),
            'num_sentences': len(set(edu.sentence_id for edu in edus if edu.sentence_id is not None)),
            'num_edus': len(edus),
            'parser_version': '1.0.0'
        }

        return tree

    def parse_to_dict(self, text: str) -> Dict:
        """Parse text and return dictionary representation."""
        tree = self.parse(text)
        return tree.to_dict()

    def segment_only(self, text: str) -> List[Dict]:
        """
        Only perform EDU segmentation (without tree building).

        Useful for analysis or integration with other parsers.
        """
        edus = self.segmenter.segment(text)
        return [
            {
                'id': edu.id,
                'text': edu.text,
                'start': edu.start_char,
                'end': edu.end_char,
                'type': edu.edu_type.value,
                'sentence_id': edu.sentence_id,
                'has_marker': edu.has_discourse_marker,
                'marker': edu.discourse_marker
            }
            for edu in edus
        ]

    def get_relation_distribution(self, tree: RSTTree) -> Dict[str, int]:
        """Get distribution of relation types in a tree."""
        distribution = defaultdict(int)
        for rel in tree.relations:
            distribution[rel.relation_type.value] += 1
        return dict(distribution)

    def extract_nucleus_chain(self, tree: RSTTree) -> List[EDU]:
        """
        Extract the nucleus chain (most important EDUs).

        Follows the nucleus path from root to leaves.
        """
        chain = []

        def _traverse(node: RSTNode):
            if node.is_leaf:
                chain.append(node.edu)
            else:
                # Follow nucleus children
                for child in node.children:
                    if child.nuclearity == NuclearityType.NUCLEUS:
                        _traverse(child)
                    elif child.nuclearity == NuclearityType.MULTINUCLEAR:
                        _traverse(child)

        _traverse(tree.root)
        return chain

    def summarize_by_depth(self, tree: RSTTree, max_depth: int = 2) -> str:
        """
        Generate summary by extracting text up to certain depth.

        Args:
            tree: RST tree
            max_depth: Maximum depth to include

        Returns:
            Summary text
        """
        texts = []

        def _traverse(node: RSTNode, depth: int):
            if depth > max_depth:
                return
            if node.is_leaf:
                texts.append(node.edu.text)
            else:
                for child in node.children:
                    # Prioritize nucleus
                    if child.nuclearity == NuclearityType.NUCLEUS:
                        _traverse(child, depth + 1)
                    elif child.nuclearity == NuclearityType.MULTINUCLEAR:
                        _traverse(child, depth + 1)

        _traverse(tree.root, 1)
        return " ".join(texts)


# =============================================================================
# INTEGRATION WITH SWSM PIPELINE
# =============================================================================

class RSTAnalyzer:
    """
    High-level RST analysis for SWSM pipeline integration.

    Provides structured output compatible with other SWSM components.
    """

    def __init__(self):
        self.parser = RSTDiscourseParser()

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Perform complete RST analysis.

        Args:
            text: Input text

        Returns:
            Analysis dictionary with tree, statistics, and summaries
        """
        tree = self.parser.parse(text)

        return {
            'tree': tree.to_dict(),
            'bracket_notation': tree.to_bracket_notation(),
            'statistics': {
                'num_edus': tree.num_edus,
                'depth': tree.depth,
                'relation_distribution': self.parser.get_relation_distribution(tree)
            },
            'nucleus_chain': [
                {'id': edu.id, 'text': edu.text}
                for edu in self.parser.extract_nucleus_chain(tree)
            ],
            'summary_depth_2': self.parser.summarize_by_depth(tree, max_depth=2),
            'edus': self.parser.segment_only(text)
        }

    def get_relations_for_sfl(self, tree: RSTTree) -> List[Dict]:
        """
        Get relations formatted for RST-SFL Bridge (E4).

        Returns relations with clause mapping information.
        """
        relations = []
        for rel in tree.relations:
            relations.append({
                'relation_type': rel.relation_type.value,
                'nucleus_ids': rel.nucleus_ids,
                'satellite_ids': rel.satellite_ids,
                'confidence': rel.confidence,
                'signals': rel.signals,
                'is_multinuclear': rel.is_multinuclear
            })
        return relations


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface for RST parser."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("SWSM E2: RST Discourse Parser")
        print("=" * 40)
        print("\nUsage: python swsm_rst_parser.py <text_or_file>")
        print("\nOptions:")
        print("  --segment-only    Only perform EDU segmentation")
        print("  --json           Output as JSON")
        print("  --bracket        Output bracket notation")
        print("\nExample:")
        print('  python swsm_rst_parser.py "Although it was raining, we went outside. However, we got wet."')
        return

    # Parse arguments
    segment_only = '--segment-only' in sys.argv
    json_output = '--json' in sys.argv
    bracket_output = '--bracket' in sys.argv

    # Get text
    text_arg = [arg for arg in sys.argv[1:] if not arg.startswith('--')][0]

    # Check if file
    if text_arg.endswith('.txt'):
        with open(text_arg, 'r') as f:
            text = f.read()
    else:
        text = text_arg

    # Parse
    parser = RSTDiscourseParser()

    if segment_only:
        edus = parser.segment_only(text)
        if json_output:
            print(json.dumps(edus, indent=2))
        else:
            print("\nEDU Segmentation:")
            print("-" * 40)
            for edu in edus:
                marker_str = f" [{edu['marker']}]" if edu['marker'] else ""
                print(f"  {edu['id']}: {edu['text']}{marker_str}")
    else:
        tree = parser.parse(text)

        if bracket_output:
            print(tree.to_bracket_notation())
        elif json_output:
            print(json.dumps(tree.to_dict(), indent=2))
        else:
            print("\nRST Analysis:")
            print("=" * 40)
            print(f"EDUs: {tree.num_edus}")
            print(f"Depth: {tree.depth}")
            print(f"\nRelations:")
            for rel in tree.relations:
                nuc = ", ".join(rel.nucleus_ids)
                sat = ", ".join(rel.satellite_ids) if rel.satellite_ids else "none"
                print(f"  {rel.relation_type.value}: N={nuc}, S={sat}")
            print(f"\nBracket notation:")
            print(f"  {tree.to_bracket_notation()}")


if __name__ == "__main__":
    main()
