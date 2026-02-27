#!/usr/bin/env python3
"""
SWSM SFL Auto-Annotator (E1)
Automatically annotates Halliday's three metafunctions:
- Ideational (Transitivity): Process types and participant roles
- Interpersonal (Mood): Mood, modality, speech functions
- Textual (Theme): Theme/Rheme structure, information flow

Based on:
- Halliday (1985/2014): Introduction to Functional Grammar
- SWSM Axioms SWSM-6 (Simultaneity) and SWSM-7 (Rank-Metafunction Mapping)

Usage:
    python scripts/swsm_sfl_annotator.py --text "Your text here"
    python scripts/swsm_sfl_annotator.py --file input.txt --output output.json
"""

import argparse
import json
import re
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════
# ENUMS: SFL CATEGORIES (based on Halliday 1985/2014)
# ═══════════════════════════════════════════════════════════════════════════

class ProcessType(Enum):
    """Halliday's Process Types (Transitivity System)"""
    MATERIAL = "material"       # doing, happening (physical actions)
    MENTAL = "mental"           # sensing (cognition, perception, affection)
    RELATIONAL = "relational"   # being, having (attributive, identifying)
    VERBAL = "verbal"           # saying (communication)
    BEHAVIORAL = "behavioral"   # behaving (physiological/psychological)
    EXISTENTIAL = "existential" # existing (there is/are)

class MentalSubtype(Enum):
    """Subtypes of Mental Processes"""
    COGNITIVE = "cognitive"     # think, know, understand, believe
    PERCEPTIVE = "perceptive"   # see, hear, feel, notice
    AFFECTIVE = "affective"     # like, love, hate, fear, want
    DESIDERATIVE = "desiderative"  # want, wish, hope

class RelationalSubtype(Enum):
    """Subtypes of Relational Processes"""
    ATTRIBUTIVE = "attributive"   # X is A (Carrier + Attribute)
    IDENTIFYING = "identifying"   # X is Y (Token + Value)
    POSSESSIVE = "possessive"     # X has Y

class MoodType(Enum):
    """Mood Types (Interpersonal Metafunction)"""
    DECLARATIVE = "declarative"
    INTERROGATIVE_YN = "interrogative_yn"      # yes/no question
    INTERROGATIVE_WH = "interrogative_wh"      # wh-question
    IMPERATIVE = "imperative"
    EXCLAMATIVE = "exclamative"

class ModalityType(Enum):
    """Modality Types"""
    EPISTEMIC = "epistemic"       # probability, certainty
    DEONTIC = "deontic"           # obligation, permission
    DYNAMIC = "dynamic"           # ability, volition

class ModalityValue(Enum):
    """Modality Values (Degrees)"""
    HIGH = "high"       # must, certainly, always
    MEDIAN = "median"   # will, probably, usually
    LOW = "low"         # may, possibly, sometimes

class ThemeType(Enum):
    """Theme Types (Textual Metafunction)"""
    TOPICAL = "topical"           # ideational (participant/process/circumstance)
    INTERPERSONAL = "interpersonal"  # mood markers, vocatives
    TEXTUAL = "textual"           # conjunctions, continuatives

class InformationStatus(Enum):
    """Information Status (Given/New)"""
    GIVEN = "given"         # already activated in discourse
    NEW = "new"             # newly introduced
    BRIDGING = "bridging"   # inferrable from context

# ═══════════════════════════════════════════════════════════════════════════
# DATA CLASSES: SFL ANNOTATIONS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TransitivityAnnotation:
    """Ideational Metafunction: Transitivity Analysis"""
    process_type: ProcessType
    process_subtype: Optional[str] = None
    process_verb: str = ""
    participants: Dict[str, str] = field(default_factory=dict)
    # Participant roles by process type:
    # MATERIAL: Actor, Goal, Beneficiary, Range, Scope
    # MENTAL: Senser, Phenomenon
    # RELATIONAL: Carrier/Token, Attribute/Value
    # VERBAL: Sayer, Receiver, Verbiage
    # BEHAVIORAL: Behaver, Behavior
    # EXISTENTIAL: Existent
    circumstances: List[Dict[str, str]] = field(default_factory=list)
    # Circumstance types: Location, Manner, Cause, Extent, etc.
    confidence: float = 0.0

@dataclass
class MoodAnnotation:
    """Interpersonal Metafunction: Mood Analysis"""
    mood_type: MoodType
    subject: str = ""
    finite: str = ""
    predicator: str = ""
    residue: str = ""
    modality_type: Optional[ModalityType] = None
    modality_value: Optional[ModalityValue] = None
    modality_marker: str = ""
    polarity: str = "positive"  # positive/negative
    speech_function: str = ""   # statement, question, command, offer
    confidence: float = 0.0

@dataclass
class ThemeAnnotation:
    """Textual Metafunction: Theme-Rheme Analysis"""
    theme: str = ""
    theme_type: ThemeType = ThemeType.TOPICAL
    rheme: str = ""
    marked_theme: bool = False  # True if non-canonical theme position
    textual_themes: List[str] = field(default_factory=list)  # conjunctions
    interpersonal_themes: List[str] = field(default_factory=list)  # mood markers
    topical_theme: str = ""
    information_status: Dict[str, InformationStatus] = field(default_factory=dict)
    confidence: float = 0.0

@dataclass
class ClauseSFLAnnotation:
    """Complete SFL annotation for a single clause (SWSM-6: Simultaneity)"""
    clause_id: str
    clause_text: str
    transitivity: TransitivityAnnotation
    mood: MoodAnnotation
    theme: ThemeAnnotation
    # Metadata
    sentence_id: str = ""
    clause_type: str = "main"  # main, subordinate, embedded
    taxis: str = ""  # parataxis, hypotaxis

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'clause_id': self.clause_id,
            'clause_text': self.clause_text,
            'clause_type': self.clause_type,
            'taxis': self.taxis,
            'ideational': {
                'process_type': self.transitivity.process_type.value,
                'process_subtype': self.transitivity.process_subtype,
                'process_verb': self.transitivity.process_verb,
                'participants': self.transitivity.participants,
                'circumstances': self.transitivity.circumstances,
                'confidence': self.transitivity.confidence
            },
            'interpersonal': {
                'mood_type': self.mood.mood_type.value,
                'subject': self.mood.subject,
                'finite': self.mood.finite,
                'modality': {
                    'type': self.mood.modality_type.value if self.mood.modality_type else None,
                    'value': self.mood.modality_value.value if self.mood.modality_value else None,
                    'marker': self.mood.modality_marker
                },
                'polarity': self.mood.polarity,
                'speech_function': self.mood.speech_function,
                'confidence': self.mood.confidence
            },
            'textual': {
                'theme': self.theme.theme,
                'theme_type': self.theme.theme_type.value,
                'rheme': self.theme.rheme,
                'marked_theme': self.theme.marked_theme,
                'textual_themes': self.theme.textual_themes,
                'interpersonal_themes': self.theme.interpersonal_themes,
                'topical_theme': self.theme.topical_theme,
                'confidence': self.theme.confidence
            }
        }

# ═══════════════════════════════════════════════════════════════════════════
# LEXICONS: Process Type Indicators
# ═══════════════════════════════════════════════════════════════════════════

# English Process Type Lexicon (based on Halliday 1985)
PROCESS_LEXICON_EN = {
    ProcessType.MATERIAL: {
        'core': {'do', 'make', 'create', 'build', 'write', 'run', 'walk', 'go',
                 'come', 'move', 'take', 'give', 'send', 'put', 'get', 'break',
                 'open', 'close', 'start', 'stop', 'finish', 'begin', 'end',
                 'produce', 'develop', 'grow', 'increase', 'decrease', 'change',
                 'conduct', 'perform', 'execute', 'implement', 'establish'},
        'ergativity': {'break', 'open', 'close', 'move', 'change', 'grow'}
    },
    ProcessType.MENTAL: {
        'cognitive': {'think', 'know', 'understand', 'believe', 'consider',
                      'remember', 'forget', 'realize', 'recognize', 'assume',
                      'suppose', 'imagine', 'expect', 'doubt', 'conclude'},
        'perceptive': {'see', 'hear', 'feel', 'notice', 'observe', 'perceive',
                       'watch', 'smell', 'taste', 'sense', 'detect'},
        'affective': {'like', 'love', 'hate', 'fear', 'enjoy', 'prefer',
                      'dislike', 'worry', 'hope', 'regret', 'appreciate'},
        'desiderative': {'want', 'wish', 'desire', 'need', 'intend', 'plan'}
    },
    ProcessType.RELATIONAL: {
        'attributive': {'be', 'become', 'seem', 'appear', 'look', 'sound',
                        'feel', 'taste', 'smell', 'remain', 'stay', 'get',
                        'turn', 'grow'},
        'identifying': {'be', 'represent', 'constitute', 'mean', 'indicate',
                        'signify', 'equal', 'define', 'comprise'},
        'possessive': {'have', 'own', 'possess', 'contain', 'include', 'lack'}
    },
    ProcessType.VERBAL: {
        'core': {'say', 'tell', 'ask', 'answer', 'reply', 'explain', 'describe',
                 'report', 'announce', 'state', 'claim', 'argue', 'suggest',
                 'propose', 'recommend', 'warn', 'promise', 'threaten',
                 'question', 'inform', 'mention', 'note', 'indicate'}
    },
    ProcessType.BEHAVIORAL: {
        'core': {'laugh', 'cry', 'smile', 'frown', 'sigh', 'breathe', 'cough',
                 'sneeze', 'yawn', 'sleep', 'dream', 'wake', 'stare', 'gaze',
                 'listen', 'watch', 'taste', 'smell'}
    },
    ProcessType.EXISTENTIAL: {
        'core': {'exist', 'be', 'arise', 'occur', 'happen', 'emerge', 'remain'}
    }
}

# German Process Type Lexicon
PROCESS_LEXICON_DE = {
    ProcessType.MATERIAL: {
        'core': {'machen', 'tun', 'erstellen', 'bauen', 'schreiben', 'laufen',
                 'gehen', 'kommen', 'bewegen', 'nehmen', 'geben', 'senden',
                 'legen', 'bekommen', 'brechen', 'öffnen', 'schliessen',
                 'anfangen', 'aufhören', 'beenden', 'beginnen', 'enden',
                 'produzieren', 'entwickeln', 'wachsen', 'durchführen'}
    },
    ProcessType.MENTAL: {
        'cognitive': {'denken', 'wissen', 'verstehen', 'glauben', 'meinen',
                      'erinnern', 'vergessen', 'erkennen', 'annehmen'},
        'perceptive': {'sehen', 'hören', 'fühlen', 'bemerken', 'beobachten',
                       'wahrnehmen', 'riechen', 'schmecken'},
        'affective': {'mögen', 'lieben', 'hassen', 'fürchten', 'geniessen',
                      'bevorzugen', 'hoffen', 'bedauern'},
        'desiderative': {'wollen', 'wünschen', 'brauchen', 'beabsichtigen'}
    },
    ProcessType.RELATIONAL: {
        'attributive': {'sein', 'werden', 'scheinen', 'erscheinen', 'aussehen',
                        'klingen', 'bleiben'},
        'identifying': {'sein', 'darstellen', 'bedeuten', 'entsprechen'},
        'possessive': {'haben', 'besitzen', 'enthalten', 'beinhalten'}
    },
    ProcessType.VERBAL: {
        'core': {'sagen', 'erzählen', 'fragen', 'antworten', 'erklären',
                 'beschreiben', 'berichten', 'behaupten', 'argumentieren',
                 'vorschlagen', 'empfehlen', 'warnen', 'versprechen'}
    },
    ProcessType.BEHAVIORAL: {
        'core': {'lachen', 'weinen', 'lächeln', 'seufzen', 'atmen', 'husten',
                 'niesen', 'gähnen', 'schlafen', 'träumen', 'starren'}
    },
    ProcessType.EXISTENTIAL: {
        'core': {'existieren', 'sein', 'entstehen', 'vorkommen', 'geschehen'}
    }
}

# Modality Markers
MODALITY_MARKERS_EN = {
    ModalityType.EPISTEMIC: {
        ModalityValue.HIGH: {'must', 'certainly', 'definitely', 'clearly',
                             'obviously', 'undoubtedly', 'always'},
        ModalityValue.MEDIAN: {'will', 'would', 'should', 'probably',
                               'likely', 'usually', 'often'},
        ModalityValue.LOW: {'may', 'might', 'could', 'possibly', 'perhaps',
                            'maybe', 'sometimes', 'occasionally'}
    },
    ModalityType.DEONTIC: {
        ModalityValue.HIGH: {'must', 'have to', 'need to', 'required'},
        ModalityValue.MEDIAN: {'should', 'ought to', 'supposed to'},
        ModalityValue.LOW: {'may', 'can', 'could', 'allowed to'}
    }
}

MODALITY_MARKERS_DE = {
    ModalityType.EPISTEMIC: {
        ModalityValue.HIGH: {'müssen', 'sicher', 'bestimmt', 'eindeutig', 'immer'},
        ModalityValue.MEDIAN: {'werden', 'würden', 'sollten', 'wahrscheinlich', 'oft'},
        ModalityValue.LOW: {'können', 'könnten', 'möglicherweise', 'vielleicht', 'manchmal'}
    },
    ModalityType.DEONTIC: {
        ModalityValue.HIGH: {'müssen', 'sollen'},
        ModalityValue.MEDIAN: {'sollten', 'sollte'},
        ModalityValue.LOW: {'dürfen', 'können'}
    }
}

# Textual Theme Markers (Conjunctions)
TEXTUAL_THEME_MARKERS_EN = {
    'additive': {'and', 'also', 'moreover', 'furthermore', 'in addition'},
    'adversative': {'but', 'however', 'nevertheless', 'yet', 'although', 'though'},
    'causal': {'because', 'since', 'therefore', 'thus', 'consequently', 'so'},
    'temporal': {'then', 'when', 'after', 'before', 'while', 'finally', 'first'}
}

TEXTUAL_THEME_MARKERS_DE = {
    'additive': {'und', 'auch', 'ausserdem', 'zudem', 'ferner'},
    'adversative': {'aber', 'jedoch', 'dennoch', 'allerdings', 'obwohl'},
    'causal': {'weil', 'da', 'daher', 'deshalb', 'folglich', 'also'},
    'temporal': {'dann', 'wenn', 'nachdem', 'bevor', 'während', 'schliesslich'}
}

# ═══════════════════════════════════════════════════════════════════════════
# SFL ANNOTATOR CLASS
# ═══════════════════════════════════════════════════════════════════════════

class SFLAnnotator:
    """
    SFL Auto-Annotator for SWSM
    Annotates clauses with Halliday's three metafunctions.
    """

    def __init__(self, language: str = "en"):
        """
        Initialize the SFL Annotator.

        Args:
            language: Language code ("en", "de", "fr")
        """
        self.language = language
        self._load_lexicons()
        self._load_nlp()

    def _load_lexicons(self):
        """Load language-specific lexicons"""
        if self.language == "de":
            self.process_lexicon = PROCESS_LEXICON_DE
            self.modality_markers = MODALITY_MARKERS_DE
            self.textual_markers = TEXTUAL_THEME_MARKERS_DE
        else:  # default to English
            self.process_lexicon = PROCESS_LEXICON_EN
            self.modality_markers = MODALITY_MARKERS_EN
            self.textual_markers = TEXTUAL_THEME_MARKERS_EN

    def _load_nlp(self):
        """Load spaCy model for preprocessing"""
        try:
            import spacy
            model_map = {
                'en': 'en_core_web_sm',
                'de': 'de_core_news_sm',
                'fr': 'fr_core_news_sm'
            }
            model_name = model_map.get(self.language, 'en_core_web_sm')
            try:
                self.nlp = spacy.load(model_name)
            except OSError:
                logger.warning(f"Model {model_name} not found, using blank model")
                self.nlp = spacy.blank(self.language)
        except ImportError:
            logger.warning("spaCy not installed, using basic tokenization")
            self.nlp = None

    # ═══════════════════════════════════════════════════════════════════════
    # TRANSITIVITY ANALYSIS (Ideational Metafunction)
    # ═══════════════════════════════════════════════════════════════════════

    def analyze_transitivity(self, clause: str, parsed=None) -> TransitivityAnnotation:
        """
        Analyze the Transitivity system of a clause.
        Identifies: Process type, Participants, Circumstances

        Args:
            clause: The clause text
            parsed: Optional pre-parsed spaCy doc

        Returns:
            TransitivityAnnotation with process analysis
        """
        if parsed is None and self.nlp:
            parsed = self.nlp(clause)

        # Find the main verb (process)
        process_verb = ""
        process_type = ProcessType.MATERIAL  # default
        process_subtype = None
        confidence = 0.5

        if parsed:
            # Find root verb
            for token in parsed:
                if token.dep_ == "ROOT" or token.pos_ == "VERB":
                    process_verb = token.lemma_.lower()
                    break
        else:
            # Fallback: simple regex
            words = clause.lower().split()
            process_verb = words[1] if len(words) > 1 else ""

        # Classify process type based on lexicon
        for ptype, categories in self.process_lexicon.items():
            for category, verbs in categories.items():
                if process_verb in verbs:
                    process_type = ptype
                    if category != 'core':
                        process_subtype = category
                    confidence = 0.85
                    break

        # Special case: Existential "there is/are"
        if clause.lower().startswith("there ") and ("is" in clause.lower() or "are" in clause.lower()):
            process_type = ProcessType.EXISTENTIAL
            confidence = 0.95

        # Extract participants based on process type
        participants = self._extract_participants(clause, parsed, process_type)

        # Extract circumstances
        circumstances = self._extract_circumstances(clause, parsed)

        return TransitivityAnnotation(
            process_type=process_type,
            process_subtype=process_subtype,
            process_verb=process_verb,
            participants=participants,
            circumstances=circumstances,
            confidence=confidence
        )

    def _extract_participants(self, clause: str, parsed, process_type: ProcessType) -> Dict[str, str]:
        """Extract participant roles based on process type"""
        participants = {}

        if not parsed:
            return participants

        # Map syntactic roles to semantic roles based on process type
        role_mapping = {
            ProcessType.MATERIAL: {'nsubj': 'Actor', 'dobj': 'Goal', 'iobj': 'Beneficiary'},
            ProcessType.MENTAL: {'nsubj': 'Senser', 'dobj': 'Phenomenon'},
            ProcessType.RELATIONAL: {'nsubj': 'Carrier', 'attr': 'Attribute', 'dobj': 'Value'},
            ProcessType.VERBAL: {'nsubj': 'Sayer', 'dobj': 'Verbiage', 'iobj': 'Receiver'},
            ProcessType.BEHAVIORAL: {'nsubj': 'Behaver'},
            ProcessType.EXISTENTIAL: {'nsubj': 'Existent', 'expl': 'Existential_there'}
        }

        mapping = role_mapping.get(process_type, role_mapping[ProcessType.MATERIAL])

        for token in parsed:
            if token.dep_ in mapping:
                role = mapping[token.dep_]
                # Get the full phrase, not just the head
                phrase = ' '.join([t.text for t in token.subtree])
                participants[role] = phrase

        return participants

    def _extract_circumstances(self, clause: str, parsed) -> List[Dict[str, str]]:
        """Extract circumstantial elements (Adjuncts)"""
        circumstances = []

        if not parsed:
            return circumstances

        # Circumstance type indicators
        circ_patterns = {
            'Location': {'in', 'at', 'on', 'to', 'from', 'into', 'onto', 'through'},
            'Temporal': {'when', 'before', 'after', 'during', 'while', 'since', 'until'},
            'Manner': {'by', 'with', 'like', 'as'},
            'Cause': {'because', 'due to', 'since', 'as'},
            'Purpose': {'to', 'in order to', 'for'},
            'Extent': {'for', 'throughout'}
        }

        for token in parsed:
            if token.dep_ in ('prep', 'advmod', 'npadvmod'):
                prep = token.text.lower()
                phrase = ' '.join([t.text for t in token.subtree])

                # Determine circumstance type
                circ_type = 'Other'
                for ctype, preps in circ_patterns.items():
                    if prep in preps:
                        circ_type = ctype
                        break

                circumstances.append({
                    'type': circ_type,
                    'text': phrase,
                    'marker': prep
                })

        return circumstances

    # ═══════════════════════════════════════════════════════════════════════
    # MOOD ANALYSIS (Interpersonal Metafunction)
    # ═══════════════════════════════════════════════════════════════════════

    def analyze_mood(self, clause: str, parsed=None) -> MoodAnnotation:
        """
        Analyze the Mood system of a clause.
        Identifies: Mood type, Subject, Finite, Modality

        Args:
            clause: The clause text
            parsed: Optional pre-parsed spaCy doc

        Returns:
            MoodAnnotation with mood analysis
        """
        if parsed is None and self.nlp:
            parsed = self.nlp(clause)

        # Determine mood type
        mood_type = self._determine_mood_type(clause, parsed)

        # Extract Subject and Finite
        subject = ""
        finite = ""
        predicator = ""

        if parsed:
            for token in parsed:
                if token.dep_ == 'nsubj':
                    subject = ' '.join([t.text for t in token.subtree])
                if token.pos_ == 'AUX' or (token.pos_ == 'VERB' and token.dep_ == 'ROOT'):
                    if not finite:
                        finite = token.text
                    else:
                        predicator = token.text

        # Analyze modality
        modality_type, modality_value, modality_marker = self._analyze_modality(clause)

        # Determine polarity
        polarity = 'negative' if self._has_negation(clause, parsed) else 'positive'

        # Determine speech function
        speech_function = self._determine_speech_function(mood_type, modality_type)

        return MoodAnnotation(
            mood_type=mood_type,
            subject=subject,
            finite=finite,
            predicator=predicator,
            residue=self._extract_residue(clause, subject, finite),
            modality_type=modality_type,
            modality_value=modality_value,
            modality_marker=modality_marker,
            polarity=polarity,
            speech_function=speech_function,
            confidence=0.8
        )

    def _determine_mood_type(self, clause: str, parsed) -> MoodType:
        """Determine the mood type of a clause"""
        clause_lower = clause.lower().strip()

        # Check for interrogative (question mark or question words)
        if clause.strip().endswith('?'):
            wh_words = {'who', 'what', 'where', 'when', 'why', 'how', 'which', 'whose',
                        'wer', 'was', 'wo', 'wann', 'warum', 'wie', 'welche'}
            first_word = clause_lower.split()[0] if clause_lower else ""
            if first_word in wh_words:
                return MoodType.INTERROGATIVE_WH
            return MoodType.INTERROGATIVE_YN

        # Check for imperative (verb-initial, no subject, or command verbs)
        if parsed:
            tokens = list(parsed)
            if tokens and tokens[0].pos_ == 'VERB' and not any(t.dep_ == 'nsubj' for t in tokens):
                return MoodType.IMPERATIVE

        # Check for exclamative
        if clause.strip().endswith('!'):
            excl_markers = {'what', 'how', 'such', 'so', 'was für', 'wie'}
            if any(clause_lower.startswith(m) for m in excl_markers):
                return MoodType.EXCLAMATIVE

        # Default to declarative
        return MoodType.DECLARATIVE

    def _analyze_modality(self, clause: str) -> Tuple[Optional[ModalityType], Optional[ModalityValue], str]:
        """Analyze modality in a clause"""
        clause_lower = clause.lower()

        for mod_type, values in self.modality_markers.items():
            for mod_value, markers in values.items():
                for marker in markers:
                    if marker in clause_lower:
                        return mod_type, mod_value, marker

        return None, None, ""

    def _has_negation(self, clause: str, parsed) -> bool:
        """Check if clause contains negation"""
        neg_markers = {'not', "n't", 'never', 'no', 'none', 'neither', 'nor',
                       'nicht', 'kein', 'keine', 'nie', 'niemals'}
        clause_lower = clause.lower()

        for marker in neg_markers:
            if marker in clause_lower:
                return True

        if parsed:
            for token in parsed:
                if token.dep_ == 'neg':
                    return True

        return False

    def _determine_speech_function(self, mood: MoodType, modality: Optional[ModalityType]) -> str:
        """Determine the speech function based on mood and modality"""
        mapping = {
            MoodType.DECLARATIVE: 'statement',
            MoodType.INTERROGATIVE_YN: 'question',
            MoodType.INTERROGATIVE_WH: 'question',
            MoodType.IMPERATIVE: 'command',
            MoodType.EXCLAMATIVE: 'exclamation'
        }

        base = mapping.get(mood, 'statement')

        # Refine based on modality
        if modality == ModalityType.DEONTIC and mood == MoodType.DECLARATIVE:
            return 'command (indirect)'

        return base

    def _extract_residue(self, clause: str, subject: str, finite: str) -> str:
        """Extract the Residue (complement + adjuncts)"""
        # Simple approach: remove subject and finite from clause
        residue = clause
        if subject:
            residue = residue.replace(subject, '', 1)
        if finite:
            residue = residue.replace(finite, '', 1)
        return residue.strip()

    # ═══════════════════════════════════════════════════════════════════════
    # THEME ANALYSIS (Textual Metafunction)
    # ═══════════════════════════════════════════════════════════════════════

    def analyze_theme(self, clause: str, parsed=None, context: Optional[List[str]] = None) -> ThemeAnnotation:
        """
        Analyze the Theme-Rheme structure of a clause.
        Identifies: Theme (starting point), Rheme (new information)

        Args:
            clause: The clause text
            parsed: Optional pre-parsed spaCy doc
            context: Previous clauses for Given/New analysis

        Returns:
            ThemeAnnotation with theme analysis
        """
        if parsed is None and self.nlp:
            parsed = self.nlp(clause)

        # Identify Textual Themes (conjunctions, continuatives)
        textual_themes = self._extract_textual_themes(clause)

        # Identify Interpersonal Themes (mood markers, vocatives)
        interpersonal_themes = self._extract_interpersonal_themes(clause, parsed)

        # Identify Topical Theme (first ideational element)
        topical_theme, theme_boundary = self._extract_topical_theme(clause, parsed, textual_themes, interpersonal_themes)

        # Determine if Theme is marked (non-canonical position)
        marked_theme = self._is_marked_theme(topical_theme, clause, parsed)

        # Construct full Theme and Rheme
        theme_parts = textual_themes + interpersonal_themes + [topical_theme] if topical_theme else textual_themes + interpersonal_themes
        theme = ' '.join(filter(None, theme_parts))
        rheme = clause[theme_boundary:].strip() if theme_boundary < len(clause) else ""

        # Determine Theme type (based on first element)
        if textual_themes:
            theme_type = ThemeType.TEXTUAL
        elif interpersonal_themes:
            theme_type = ThemeType.INTERPERSONAL
        else:
            theme_type = ThemeType.TOPICAL

        # Analyze Given/New structure
        info_status = self._analyze_information_status(clause, parsed, context)

        return ThemeAnnotation(
            theme=theme,
            theme_type=theme_type,
            rheme=rheme,
            marked_theme=marked_theme,
            textual_themes=textual_themes,
            interpersonal_themes=interpersonal_themes,
            topical_theme=topical_theme,
            information_status=info_status,
            confidence=0.75
        )

    def _extract_textual_themes(self, clause: str) -> List[str]:
        """Extract textual themes (conjunctions, continuatives)"""
        textual_themes = []
        clause_lower = clause.lower()

        all_markers = set()
        for markers in self.textual_markers.values():
            all_markers.update(markers)

        # Check if clause starts with textual marker
        words = clause.split()
        for i, word in enumerate(words[:3]):  # Check first 3 words
            if word.lower().rstrip(',') in all_markers:
                textual_themes.append(word.rstrip(','))

        return textual_themes

    def _extract_interpersonal_themes(self, clause: str, parsed) -> List[str]:
        """Extract interpersonal themes (vocatives, modal adjuncts)"""
        interpersonal_themes = []

        # Modal adjuncts that can be thematic
        modal_adjuncts = {'frankly', 'honestly', 'fortunately', 'unfortunately',
                         'probably', 'certainly', 'perhaps', 'maybe',
                         'leider', 'glücklicherweise', 'wahrscheinlich', 'vielleicht'}

        words = clause.split()
        if words and words[0].lower().rstrip(',') in modal_adjuncts:
            interpersonal_themes.append(words[0].rstrip(','))

        return interpersonal_themes

    def _extract_topical_theme(self, clause: str, parsed, textual: List[str], interpersonal: List[str]) -> Tuple[str, int]:
        """Extract the topical theme (first ideational element)"""
        # Skip textual and interpersonal themes
        skip_count = len(textual) + len(interpersonal)

        if parsed:
            # Find first participant or circumstance
            for token in parsed:
                if token.i < skip_count:
                    continue
                if token.dep_ in ('nsubj', 'nsubjpass', 'expl', 'advmod', 'prep'):
                    # Get the phrase
                    phrase_tokens = list(token.subtree)
                    phrase = ' '.join([t.text for t in phrase_tokens])
                    end_pos = phrase_tokens[-1].idx + len(phrase_tokens[-1].text) if phrase_tokens else 0
                    return phrase, end_pos

        # Fallback: first noun phrase or word after textual/interpersonal
        words = clause.split()
        if len(words) > skip_count:
            theme_word = words[skip_count]
            pos = clause.find(theme_word) + len(theme_word)
            return theme_word, pos

        return "", 0

    def _is_marked_theme(self, topical_theme: str, clause: str, parsed) -> bool:
        """Determine if the theme is marked (non-canonical position)"""
        if not parsed or not topical_theme:
            return False

        # In English/German: Subject-initial is unmarked
        # Marked themes: Adjunct-initial, Complement-initial
        for token in parsed:
            if topical_theme.lower().startswith(token.text.lower()):
                # Marked if theme is not the subject
                if token.dep_ not in ('nsubj', 'nsubjpass', 'expl'):
                    return True
                break

        return False

    def _analyze_information_status(self, clause: str, parsed, context: Optional[List[str]]) -> Dict[str, InformationStatus]:
        """Analyze Given/New status of elements"""
        info_status = {}

        if not context:
            context = []

        # Build set of previously mentioned entities
        previous_entities: Set[str] = set()
        for prev_clause in context:
            words = prev_clause.lower().split()
            previous_entities.update(words)

        if parsed:
            for token in parsed:
                if token.pos_ in ('NOUN', 'PROPN', 'PRON'):
                    word = token.text.lower()
                    if word in previous_entities or token.pos_ == 'PRON':
                        info_status[token.text] = InformationStatus.GIVEN
                    else:
                        info_status[token.text] = InformationStatus.NEW

        return info_status

    # ═══════════════════════════════════════════════════════════════════════
    # MAIN ANNOTATION METHOD
    # ═══════════════════════════════════════════════════════════════════════

    def annotate_clause(self, clause: str, clause_id: str = "c1",
                        sentence_id: str = "s1",
                        context: Optional[List[str]] = None) -> ClauseSFLAnnotation:
        """
        Annotate a clause with all three SFL metafunctions (SWSM-6: Simultaneity)

        Args:
            clause: The clause text
            clause_id: Unique identifier for the clause
            sentence_id: Identifier of the containing sentence
            context: Previous clauses for discourse context

        Returns:
            Complete ClauseSFLAnnotation
        """
        # Parse once, use for all analyses
        parsed = self.nlp(clause) if self.nlp else None

        # Analyze all three metafunctions
        transitivity = self.analyze_transitivity(clause, parsed)
        mood = self.analyze_mood(clause, parsed)
        theme = self.analyze_theme(clause, parsed, context)

        return ClauseSFLAnnotation(
            clause_id=clause_id,
            clause_text=clause,
            transitivity=transitivity,
            mood=mood,
            theme=theme,
            sentence_id=sentence_id
        )

    def annotate_text(self, text: str) -> List[ClauseSFLAnnotation]:
        """
        Annotate all clauses in a text.

        Args:
            text: The full text to annotate

        Returns:
            List of ClauseSFLAnnotation for each clause
        """
        annotations = []
        context = []

        # Split into sentences
        if self.nlp:
            doc = self.nlp(text)
            sentences = list(doc.sents)
        else:
            sentences = text.split('.')

        for s_idx, sent in enumerate(sentences):
            sent_text = sent.text if hasattr(sent, 'text') else sent
            sent_text = sent_text.strip()
            if not sent_text:
                continue

            sentence_id = f"s{s_idx + 1}"

            # For now, treat each sentence as one clause
            # TODO: Implement clause segmentation for complex sentences
            clause_id = f"{sentence_id}_c1"

            annotation = self.annotate_clause(
                sent_text,
                clause_id=clause_id,
                sentence_id=sentence_id,
                context=context
            )
            annotations.append(annotation)
            context.append(sent_text)

        return annotations


# ═══════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="SWSM SFL Auto-Annotator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python swsm_sfl_annotator.py --text "Loss aversion is a cornerstone of behavioral economics."
  python swsm_sfl_annotator.py --file paper.txt --output annotations.json
  python swsm_sfl_annotator.py --text "Sie haben drei Experimente durchgeführt." --language de
        """
    )
    parser.add_argument("--text", "-t", help="Direct text input")
    parser.add_argument("--file", "-f", help="Input file path")
    parser.add_argument("--output", "-o", help="Output file path (JSON)")
    parser.add_argument("--language", "-l", default="en",
                        choices=["en", "de", "fr"],
                        help="Language (default: en)")
    parser.add_argument("--format", choices=["json", "text"], default="text",
                        help="Output format")

    args = parser.parse_args()

    # Get input text
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        parser.error("Either --text or --file required")

    # Initialize annotator
    annotator = SFLAnnotator(language=args.language)

    # Annotate
    annotations = annotator.annotate_text(text)

    # Output
    if args.format == "json" or args.output:
        result = {
            'language': args.language,
            'source_text': text,
            'clause_count': len(annotations),
            'clauses': [a.to_dict() for a in annotations]
        }

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Annotations saved to {args.output}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Pretty print
        print("=" * 70)
        print("SFL ANNOTATION RESULTS")
        print("=" * 70)

        for ann in annotations:
            print(f"\n[{ann.clause_id}] {ann.clause_text}")
            print("-" * 70)

            # Transitivity
            t = ann.transitivity
            print(f"  IDEATIONAL (Transitivity):")
            print(f"    Process: {t.process_type.value.upper()}" +
                  (f" ({t.process_subtype})" if t.process_subtype else "") +
                  f" - '{t.process_verb}'")
            if t.participants:
                print(f"    Participants: {t.participants}")
            if t.circumstances:
                print(f"    Circumstances: {t.circumstances}")

            # Mood
            m = ann.mood
            print(f"  INTERPERSONAL (Mood):")
            print(f"    Mood: {m.mood_type.value.upper()}, Polarity: {m.polarity}")
            print(f"    Subject: '{m.subject}', Finite: '{m.finite}'")
            if m.modality_type:
                print(f"    Modality: {m.modality_type.value} ({m.modality_value.value}) - '{m.modality_marker}'")
            print(f"    Speech Function: {m.speech_function}")

            # Theme
            th = ann.theme
            print(f"  TEXTUAL (Theme-Rheme):")
            print(f"    Theme: '{th.theme}' ({th.theme_type.value})" +
                  (" [MARKED]" if th.marked_theme else ""))
            print(f"    Rheme: '{th.rheme}'")
            if th.textual_themes:
                print(f"    Textual Themes: {th.textual_themes}")

        print("\n" + "=" * 70)


# ═══════════════════════════════════════════════════════════════════════════
# RST-SFL BRIDGE INTEGRATION (E4)
# ═══════════════════════════════════════════════════════════════════════════

class SFLAnnotatorWithRST(SFLAnnotator):
    """
    Extended SFL Annotator with RST-SFL Bridge integration.

    Provides full SWSM analysis: L6 (Clause SFL) + L4 (Discourse RST)
    Implements SWSM Axiom 7 (Realizational Stratification).
    """

    def __init__(self, language: str = 'en'):
        """Initialize with RST-SFL Bridge."""
        super().__init__(language)
        self.bridge = None

        # Try to import bridge
        try:
            from swsm_rst_sfl_bridge import RSTSFLBridge
            self.bridge = RSTSFLBridge(language)
            self.rst_enabled = True
        except ImportError:
            logger.warning("RST-SFL Bridge not available. RST inference disabled.")
            self.rst_enabled = False

    def annotate_text_with_rst(self, text: str) -> Dict:
        """
        Full SWSM analysis with both SFL and RST layers.

        Args:
            text: Input text

        Returns:
            Dictionary with:
            - L6_clause_sfl: SFL clause annotations
            - L4_discourse_rst: Inferred RST relations
            - L3_move_structure: Detected genre moves (if applicable)
        """
        # Get SFL annotations
        sfl_annotations = self.annotate_text(text)

        result = {
            'text': text,
            'language': self.language,
            'L6_clause_sfl': [a.to_dict() for a in sfl_annotations],
            'L4_discourse_rst': [],
            'summary': {
                'total_clauses': len(sfl_annotations),
                'rst_relations_found': 0
            }
        }

        # Infer RST relations if bridge available
        if self.rst_enabled and self.bridge and len(sfl_annotations) > 1:
            rst_relations = self._infer_rst_relations(sfl_annotations)
            result['L4_discourse_rst'] = rst_relations
            result['summary']['rst_relations_found'] = len(rst_relations)

        return result

    def _infer_rst_relations(self, annotations: List[ClauseSFLAnnotation]) -> List[Dict]:
        """
        Infer RST relations between consecutive clauses.

        Uses SFL features (Theme, Mood, Modality) to infer discourse relations.
        """
        relations = []

        for i in range(len(annotations) - 1):
            ann1 = annotations[i]
            ann2 = annotations[i + 1]

            # Extract features from clause 2 for inference
            conjunction = None
            if ann2.theme.textual_themes:
                conjunction = ann2.theme.textual_themes[0]

            taxis = 'hypotactic' if conjunction else 'paratactic'

            # Infer relation using bridge
            inferred = self.bridge.sfl_to_rst(
                conjunction=conjunction,
                taxis=taxis,
                mood=ann2.mood.mood_type.value if ann2.mood else None,
                theme_marked=ann2.theme.marked_theme if ann2.theme else None,
                modality_type=ann2.mood.modality_type.value if ann2.mood and ann2.mood.modality_type else None
            )

            if inferred:
                best_relation, confidence = inferred[0]
                relations.append({
                    'from_clause': ann1.clause_id,
                    'to_clause': ann2.clause_id,
                    'relation': best_relation.value,
                    'confidence': round(confidence, 3),
                    'signal': conjunction or 'implicit',
                    'alternatives': [
                        {'relation': r.value, 'probability': round(p, 3)}
                        for r, p in inferred[1:3]
                    ]
                })

        return relations

    def get_clause_complex_template(self, relation_type: str) -> Dict:
        """
        Get generation template for a specific RST relation.

        Args:
            relation_type: RST relation type (e.g., 'cause', 'contrast')

        Returns:
            Template with SFL constraints for generation
        """
        if not self.rst_enabled or not self.bridge:
            return {'error': 'RST Bridge not available'}

        from swsm_rst_sfl_bridge import RSTRelationType
        try:
            rel_type = RSTRelationType(relation_type)
            return self.bridge.get_clause_complex_pattern(rel_type)
        except ValueError:
            return {'error': f'Unknown relation type: {relation_type}'}


# ═══════════════════════════════════════════════════════════════════════════
# COHESION INTEGRATION (E5)
# ═══════════════════════════════════════════════════════════════════════════

class SWSMFullAnalyzer(SFLAnnotatorWithRST):
    """
    Complete SWSM Analyzer integrating all components:
    - E1: SFL Auto-Annotator (Metafunctions)
    - E4: RST-SFL Bridge (Discourse Relations)
    - E5: Cohesion Analyzer (Reference, Lexical Cohesion)
    - E6: Information Structure (Given/New, Topic/Comment, Focus)

    Provides multi-layer analysis: L6 (SFL) + L4 (RST) + Cohesion + InfoStructure
    """

    def __init__(self, language: str = 'en'):
        """Initialize with all SWSM components."""
        super().__init__(language)
        self.cohesion_analyzer = None
        self.info_structure_analyzer = None

        # Try to import cohesion analyzer (E5)
        try:
            from swsm_cohesion_analyzer import CohesionAnalyzer
            self.cohesion_analyzer = CohesionAnalyzer(language)
            self.cohesion_enabled = True
        except ImportError:
            logger.warning("Cohesion Analyzer not available.")
            self.cohesion_enabled = False

        # Try to import information structure analyzer (E6)
        try:
            from swsm_information_structure import InformationStructureAnalyzer
            self.info_structure_analyzer = InformationStructureAnalyzer(language)
            self.info_structure_enabled = True
        except ImportError:
            logger.warning("Information Structure Analyzer not available.")
            self.info_structure_enabled = False

    def analyze_full(self, text: str) -> Dict:
        """
        Complete SWSM multi-layer analysis.

        Args:
            text: Input text

        Returns:
            Dictionary with all analysis layers:
            - L6_clause_sfl: SFL clause annotations
            - L4_discourse_rst: RST relations
            - cohesion: Cohesion analysis with metrics
            - information_structure: Given/New, Topic/Comment, Focus analysis
            - summary: Aggregated statistics
        """
        # Get SFL + RST analysis
        result = self.annotate_text_with_rst(text)

        # Add cohesion analysis (E5)
        if self.cohesion_enabled and self.cohesion_analyzer:
            cohesion_analysis = self.cohesion_analyzer.analyze(text)
            result['cohesion'] = cohesion_analysis.to_dict()
            result['summary']['cohesion_score'] = cohesion_analysis.metrics.cohesion_score
            result['summary']['cohesion_level'] = cohesion_analysis.metrics.cohesion_level
        else:
            result['cohesion'] = None
            result['summary']['cohesion_score'] = None

        # Add information structure analysis (E6)
        if self.info_structure_enabled and self.info_structure_analyzer:
            info_analysis = self.info_structure_analyzer.analyze(text)
            result['information_structure'] = info_analysis.to_dict()
            result['summary']['given_ratio'] = info_analysis.flow.given_ratio if info_analysis.flow else None
            result['summary']['progression_type'] = info_analysis.flow.progression_type if info_analysis.flow else None
        else:
            result['information_structure'] = None

        return result

    def get_quality_assessment(self, text: str) -> Dict:
        """
        Get a quality assessment of the text based on SWSM criteria.

        Returns quality scores for:
        - Metafunction balance (SFL)
        - Discourse structure (RST)
        - Cohesion (Halliday & Hasan)
        """
        analysis = self.analyze_full(text)

        assessment = {
            'overall_quality': 'moderate',
            'scores': {},
            'recommendations': []
        }

        # Assess cohesion
        if analysis.get('cohesion'):
            cohesion_score = analysis['cohesion']['metrics']['cohesion_score']
            assessment['scores']['cohesion'] = cohesion_score

            if cohesion_score < 0.4:
                assessment['recommendations'].append(
                    "Increase cohesion: Add more connectors and reference chains"
                )
            elif cohesion_score > 0.8:
                assessment['recommendations'].append(
                    "Cohesion is excellent - text flows well"
                )

        # Assess RST structure
        rst_count = analysis['summary'].get('rst_relations_found', 0)
        clause_count = analysis['summary'].get('total_clauses', 1)
        rst_density = rst_count / max(clause_count - 1, 1)
        assessment['scores']['rst_density'] = round(rst_density, 2)

        if rst_density < 0.3:
            assessment['recommendations'].append(
                "Add more explicit discourse markers to clarify relations"
            )

        # Calculate overall
        scores = list(assessment['scores'].values())
        if scores:
            avg_score = sum(scores) / len(scores)
            if avg_score >= 0.7:
                assessment['overall_quality'] = 'good'
            elif avg_score >= 0.5:
                assessment['overall_quality'] = 'moderate'
            else:
                assessment['overall_quality'] = 'needs_improvement'

        return assessment


# ═══════════════════════════════════════════════════════════════════════════
# SWSM COMPLETE PIPELINE (E1-E9 Integration)
# ═══════════════════════════════════════════════════════════════════════════

class SWSMPipeline:
    """
    Complete SWSM Pipeline integrating all components (E1-E9).

    Analysis Direction (Parse):
        Text → E1 (SFL) → E4 (RST) → E5 (Cohesion) → E6 (InfoStructure)

    Generation Direction (Generate):
        8D Profile → E7 (Genre) → E8 (Moves) → E9 (Text) → Document

    Axiom SWSM-10: Bidirectional Isomorphism
        Generate(Parse(T)) ≈ T
    """

    def __init__(self, language: str = 'en'):
        """Initialize all SWSM components."""
        self.language = language

        # Analysis components (E1, E4, E5, E6)
        self.full_analyzer = SWSMFullAnalyzer(language)

        # Generation components (E7, E8, E9)
        self.genre_mapper = None
        self.move_planner = None
        self.text_generator = None

        # Try to import generation components
        try:
            from swsm_8d_genre_mapper import GenreMapper
            self.genre_mapper = GenreMapper()
            self.genre_enabled = True
        except ImportError:
            logger.warning("Genre Mapper (E7) not available.")
            self.genre_enabled = False

        try:
            from swsm_move_planner import MovePlanner
            self.move_planner = MovePlanner(language)
            self.planner_enabled = True
        except ImportError:
            logger.warning("Move Planner (E8) not available.")
            self.planner_enabled = False

        try:
            from swsm_text_generator import SWSMTextGenerator
            self.text_generator = SWSMTextGenerator(language)
            self.generator_enabled = True
        except ImportError:
            logger.warning("Text Generator (E9) not available.")
            self.generator_enabled = False

    # ─────────────────────────────────────────────────────────────────────────
    # ANALYSIS (Parse Direction)
    # ─────────────────────────────────────────────────────────────────────────

    def analyze(self, text: str) -> Dict:
        """
        Complete SWSM analysis of text.

        Integrates E1 (SFL) + E4 (RST) + E5 (Cohesion) + E6 (InfoStructure).

        Args:
            text: Input text to analyze

        Returns:
            Complete multi-layer analysis
        """
        return self.full_analyzer.analyze_full(text)

    def assess_quality(self, text: str) -> Dict:
        """
        Assess text quality using SWSM criteria.

        Returns:
            Quality assessment with scores and recommendations
        """
        return self.full_analyzer.get_quality_assessment(text)

    # ─────────────────────────────────────────────────────────────────────────
    # GENERATION (Generate Direction)
    # ─────────────────────────────────────────────────────────────────────────

    def generate_from_8d(self, profile_8d: Dict[str, float],
                          context: Dict[str, str] = None) -> Dict:
        """
        Generate document from 8D profile.

        Pipeline: 8D → E7 (Genre) → E8 (Moves) → E9 (Text)

        Args:
            profile_8d: 8D audience profile (D1-D8 values)
            context: Optional context (topic, purpose, etc.)

        Returns:
            Generated document with text and metadata
        """
        context = context or {}

        # Check components
        if not self.planner_enabled:
            return {'error': 'Move Planner (E8) not available'}
        if not self.generator_enabled:
            return {'error': 'Text Generator (E9) not available'}

        # E7: 8D → Genre (if available)
        genre_type = None
        if self.genre_enabled and self.genre_mapper:
            genre_result = self.genre_mapper.map_8d_to_genre(profile_8d)
            genre_type = genre_result.get('genre', 'scientific_paper')
        else:
            # Infer genre from 8D heuristically
            genre_type = self._infer_genre_from_8d(profile_8d)

        # E8: Genre → Document Plan
        document_plan = self.move_planner.plan_from_genre(genre_type)
        document_plan['context'] = context
        document_plan['title'] = context.get('title', 'Generated Document')

        # E9: Document Plan → Text
        doc = self.text_generator.generate_from_plan(document_plan, profile_8d)

        return {
            'genre': genre_type,
            'document_plan': document_plan,
            'generated_document': {
                'title': doc.title,
                'sections': [
                    {
                        'title': s.title,
                        'paragraphs': [p.text for p in s.paragraphs],
                        'moves': s.move_sequence
                    }
                    for s in doc.sections
                ],
                'word_count': doc.word_count,
                'metadata': doc.metadata
            },
            'text': self.text_generator.render_document(doc, format='text'),
            'markdown': self.text_generator.render_document(doc, format='markdown'),
        }

    def generate_from_genre(self, genre: str, profile_8d: Dict[str, float] = None,
                             context: Dict[str, str] = None) -> Dict:
        """
        Generate document from explicit genre.

        Pipeline: Genre → E8 (Moves) → E9 (Text)

        Args:
            genre: Genre type (e.g., 'scientific_paper', 'policy_brief')
            profile_8d: Optional 8D profile for style constraints
            context: Optional context

        Returns:
            Generated document
        """
        if not self.planner_enabled or not self.generator_enabled:
            return {'error': 'Generation components not available'}

        context = context or {}
        profile_8d = profile_8d or {}

        # E8: Genre → Document Plan
        document_plan = self.move_planner.plan_from_genre(genre)
        document_plan['context'] = context
        document_plan['title'] = context.get('title', 'Generated Document')

        # E9: Document Plan → Text
        doc = self.text_generator.generate_from_plan(document_plan, profile_8d)

        return {
            'genre': genre,
            'text': self.text_generator.render_document(doc, format='text'),
            'markdown': self.text_generator.render_document(doc, format='markdown'),
            'word_count': doc.word_count
        }

    def _infer_genre_from_8d(self, profile_8d: Dict[str, float]) -> str:
        """Simple genre inference from 8D without E7."""
        d1 = profile_8d.get('D1_expertise', 0.5)
        d4 = profile_8d.get('D4_time', 0.5)
        d6 = profile_8d.get('D6_context', 0.5)
        d8 = profile_8d.get('D8_persistence', 0.5)

        if d1 > 0.8 and d8 > 0.8:
            return 'scientific_paper'
        elif d4 < 0.3 and d6 > 0.7:
            return 'policy_brief'
        elif d4 < 0.2:
            return 'executive_summary'
        elif d6 < 0.5 and d8 < 0.4:
            return 'blog_post'
        else:
            return 'consulting_memo'

    # ─────────────────────────────────────────────────────────────────────────
    # BIDIRECTIONAL (Round-Trip)
    # ─────────────────────────────────────────────────────────────────────────

    def round_trip(self, text: str, profile_8d: Dict[str, float] = None) -> Dict:
        """
        Analyze text and regenerate it (test bidirectional isomorphism).

        Axiom SWSM-10: Generate(Parse(T)) ≈ T

        Args:
            text: Original text
            profile_8d: Optional 8D profile for regeneration

        Returns:
            Analysis, regenerated text, and comparison
        """
        # Parse direction
        analysis = self.analyze(text)

        # Extract context from analysis
        context = {
            'topic': 'the subject matter',  # Could extract from analysis
        }

        # Infer genre from text structure
        genre = self._infer_genre_from_analysis(analysis)

        # Generate direction
        if self.generator_enabled:
            regenerated = self.generate_from_genre(genre, profile_8d, context)
        else:
            regenerated = {'text': '', 'error': 'Generator not available'}

        return {
            'original_text': text,
            'analysis': analysis,
            'inferred_genre': genre,
            'regenerated_text': regenerated.get('text', ''),
            'comparison': {
                'original_words': len(text.split()),
                'regenerated_words': regenerated.get('word_count', 0),
            }
        }

    def _infer_genre_from_analysis(self, analysis: Dict) -> str:
        """Infer genre from text analysis."""
        # Simple heuristic based on RST relations and structure
        rst_relations = analysis.get('L4_discourse_rst', [])

        has_contrast = any(r.get('relation') == 'contrast' for r in rst_relations)
        has_evidence = any(r.get('relation') == 'evidence' for r in rst_relations)

        if has_evidence and has_contrast:
            return 'scientific_paper'
        elif has_contrast:
            return 'policy_brief'
        else:
            return 'consulting_memo'

    # ─────────────────────────────────────────────────────────────────────────
    # UTILITIES
    # ─────────────────────────────────────────────────────────────────────────

    def get_component_status(self) -> Dict:
        """Get status of all SWSM components."""
        return {
            'E1_SFL_Annotator': True,  # Always available (this file)
            'E4_RST_Bridge': self.full_analyzer.rst_enabled,
            'E5_Cohesion': self.full_analyzer.cohesion_enabled,
            'E6_InfoStructure': self.full_analyzer.info_structure_enabled,
            'E7_GenreMapper': self.genre_enabled,
            'E8_MovePlanner': self.planner_enabled,
            'E9_TextGenerator': self.generator_enabled,
        }

    def get_available_genres(self) -> List[str]:
        """Get list of available genres for generation."""
        if self.planner_enabled and self.move_planner:
            from swsm_move_planner import GenreType
            return [g.value for g in GenreType]
        return ['scientific_paper', 'policy_brief', 'executive_summary',
                'blog_post', 'consulting_memo', 'ebf_appendix']


if __name__ == "__main__":
    main()
