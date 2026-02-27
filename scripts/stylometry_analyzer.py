#!/usr/bin/env python3
"""
Scientific Writing Style Model (SWSM) - Stylometry Analyzer
============================================================

Analyzes scientific papers to extract a 10-dimensional style vector.
Part of the Evidence-Based Framework (EBF) for Economic and Social Behavior.

Session: EBF-S-2026-01-29-SWSM-001
Authors: FehrAdvice & Partners AG / Prof. Ernst Fehr

Usage:
    python stylometry_analyzer.py --text "paper.txt"
    python stylometry_analyzer.py --author "Fehr" --sample 5
    python stylometry_analyzer.py --validate --bootstrap 1000
"""

import re
import json
import argparse
import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from collections import Counter
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


# =============================================================================
# CONFIGURATION: 10 STYLE DIMENSIONS
# =============================================================================

DIMENSIONS = {
    'D1_formality': {
        'name': 'Formalität',
        'description': '0 = zugänglich ←→ 1 = technisch',
        'subdimensions': ['formulas_per_page', 'technical_vocab', 'theorem_density']
    },
    'D2_evidence': {
        'name': 'Evidenz-Stil',
        'description': '0 = konzeptionell ←→ 1 = empirisch',
        'subdimensions': ['tables_count', 'stat_complexity', 'data_transparency']
    },
    'D3_narrativity': {
        'name': 'Narrativität',
        'description': '0 = abstrakt ←→ 1 = narrativ',
        'subdimensions': ['example_density', 'metaphor_ratio', 'first_person_ratio']
    },
    'D4_hedging': {
        'name': 'Hedging',
        'description': '0 = assertiv ←→ 1 = vorsichtig',
        'subdimensions': ['hedge_words', 'caveat_density', 'uncertainty_markers']
    },
    'D5_policy': {
        'name': 'Policy-Orientierung',
        'description': '0 = rein akademisch ←→ 1 = angewandt',
        'subdimensions': ['policy_terms', 'recommendations', 'real_world_examples']
    },
    'D6_syntax': {
        'name': 'Syntaktische Komplexität',
        'description': '0 = einfach ←→ 1 = komplex',
        'subdimensions': ['avg_sentence_length', 'subordination_ratio', 'passive_ratio']
    },
    'D7_collaboration': {
        'name': 'Kollaboration',
        'description': '0 = solo ←→ 1 = Team',
        'subdimensions': ['coauthor_count', 'we_vs_i_ratio', 'acknowledgments_length']
    },
    'D8_humor': {
        'name': 'Humor',
        'description': '0 = ernst ←→ 1 = humorvoll',
        'subdimensions': ['irony_markers', 'wordplay', 'self_reference']
    },
    'D9_interdisciplinary': {
        'name': 'Interdisziplinarität',
        'description': '0 = mono-disziplinär ←→ 1 = breit',
        'subdimensions': ['discipline_terms', 'cross_references', 'methodology_diversity']
    },
    'D10_temporal': {
        'name': 'Zeitperspektive',
        'description': '0 = historisch ←→ 1 = zukunftsorientiert',
        'subdimensions': ['historical_refs', 'future_terms', 'trend_language']
    }
}


# =============================================================================
# WORD LISTS FOR DIMENSION DETECTION
# =============================================================================

WORDLISTS = {
    # D1: Formality indicators
    'technical_terms': [
        'equilibrium', 'theorem', 'lemma', 'proof', 'corollary', 'proposition',
        'utility', 'maximization', 'optimization', 'constraint', 'derivative',
        'integral', 'function', 'parameter', 'coefficient', 'variance',
        'asymptotic', 'convergence', 'stochastic', 'endogenous', 'exogenous'
    ],
    'theorem_markers': [
        'theorem', 'lemma', 'proof', 'corollary', 'proposition', 'axiom',
        'q.e.d.', 'qed', '∎', 'by assumption', 'it follows that'
    ],

    # D2: Evidence indicators
    'stat_methods': [
        'regression', 'ols', 'iv', 'instrumental variable', '2sls', 'rdd',
        'difference-in-difference', 'did', 'rct', 'randomized', 'fixed effects',
        'panel data', 'standard error', 'robust', 'clustered', 'bootstrap'
    ],

    # D3: Narrativity indicators
    'example_markers': [
        'for example', 'for instance', 'consider', 'imagine', 'suppose',
        'case study', 'anecdote', 'story', 'illustration', 'scenario'
    ],
    'first_person': ['i', 'we', 'my', 'our', 'me', 'us'],

    # D4: Hedging indicators
    'hedge_words': [
        'may', 'might', 'could', 'would', 'suggest', 'indicate', 'appear',
        'seem', 'likely', 'possibly', 'perhaps', 'potentially', 'arguably',
        'tends to', 'in general', 'on average', 'approximately'
    ],
    'caveat_words': [
        'however', 'although', 'but', 'nevertheless', 'nonetheless',
        'limitation', 'caveat', 'exception', 'under certain conditions'
    ],

    # D5: Policy indicators
    'policy_terms': [
        'policy', 'regulation', 'government', 'intervention', 'welfare',
        'implementation', 'recommendation', 'implication', 'practice',
        'real-world', 'practical', 'applied', 'nudge', 'incentive'
    ],

    # D6: Syntax - passive voice indicators
    'passive_markers': [
        'is shown', 'was found', 'are presented', 'were obtained',
        'has been', 'have been', 'will be', 'can be', 'should be',
        'is expected', 'was observed', 'are reported'
    ],

    # D8: Humor indicators
    'humor_markers': [
        'ironically', 'surprisingly', 'amusingly', 'curiously',
        'so-called', 'air quotes', 'tongue-in-cheek', 'admittedly'
    ],

    # D9: Interdisciplinary indicators
    'psychology_terms': [
        'cognitive', 'psychological', 'behavioral', 'heuristic', 'bias',
        'mental', 'perception', 'attention', 'memory', 'emotion'
    ],
    'neuro_terms': [
        'neural', 'brain', 'fmri', 'neuroimaging', 'cortex', 'dopamine',
        'prefrontal', 'amygdala', 'reward system'
    ],
    'sociology_terms': [
        'social', 'norm', 'institution', 'culture', 'community',
        'network', 'group', 'identity', 'status'
    ],

    # D10: Temporal indicators
    'historical_terms': [
        'historically', 'tradition', 'classical', 'original', 'seminal',
        'early work', 'pioneering', 'foundation', 'origin'
    ],
    'future_terms': [
        'future', 'prospect', 'forecast', 'predict', 'trend', 'emerging',
        'forthcoming', 'next generation', 'innovation', 'evolution'
    ]
}


# =============================================================================
# AUTHOR PRIORS (LLMMC v0.2)
# =============================================================================

AUTHOR_PRIORS = {
    'Fehr': {
        'full_name': 'Ernst Fehr',
        'cluster': 'Formal',
        'priors': {
            'D1': (0.90, 0.05), 'D2': (0.85, 0.07), 'D3': (0.15, 0.08),
            'D4': (0.70, 0.10), 'D5': (0.40, 0.12), 'D6': (0.75, 0.08),
            'D7': (0.95, 0.03), 'D8': (0.05, 0.05), 'D9': (0.45, 0.12),
            'D10': (0.50, 0.12)
        }
    },
    'Camerer': {
        'full_name': 'Colin Camerer',
        'cluster': 'Formal',
        'priors': {
            'D1': (0.85, 0.07), 'D2': (0.80, 0.08), 'D3': (0.25, 0.10),
            'D4': (0.65, 0.10), 'D5': (0.35, 0.10), 'D6': (0.80, 0.07),
            'D7': (0.85, 0.07), 'D8': (0.10, 0.08), 'D9': (0.90, 0.05),
            'D10': (0.55, 0.12)
        }
    },
    'List': {
        'full_name': 'John List',
        'cluster': 'Experimental',
        'priors': {
            'D1': (0.70, 0.08), 'D2': (0.95, 0.03), 'D3': (0.30, 0.12),
            'D4': (0.60, 0.10), 'D5': (0.55, 0.12), 'D6': (0.60, 0.10),
            'D7': (0.80, 0.08), 'D8': (0.15, 0.10), 'D9': (0.35, 0.12),
            'D10': (0.60, 0.12)
        }
    },
    'Sutter': {
        'full_name': 'Matthias Sutter',
        'cluster': 'Experimental',
        'priors': {
            'D1': (0.75, 0.08), 'D2': (0.90, 0.05), 'D3': (0.25, 0.10),
            'D4': (0.75, 0.08), 'D5': (0.45, 0.12), 'D6': (0.65, 0.10),
            'D7': (0.85, 0.07), 'D8': (0.10, 0.08), 'D9': (0.40, 0.12),
            'D10': (0.50, 0.12)
        }
    },
    'Gneezy': {
        'full_name': 'Uri Gneezy',
        'cluster': 'Experimental',
        'priors': {
            'D1': (0.60, 0.10), 'D2': (0.90, 0.05), 'D3': (0.45, 0.12),
            'D4': (0.55, 0.12), 'D5': (0.50, 0.12), 'D6': (0.55, 0.10),
            'D7': (0.75, 0.10), 'D8': (0.35, 0.12), 'D9': (0.50, 0.15),
            'D10': (0.55, 0.12)
        }
    },
    'Thaler': {
        'full_name': 'Richard Thaler',
        'cluster': 'Narrative',
        'priors': {
            'D1': (0.35, 0.10), 'D2': (0.60, 0.12), 'D3': (0.85, 0.07),
            'D4': (0.40, 0.12), 'D5': (0.70, 0.10), 'D6': (0.45, 0.10),
            'D7': (0.70, 0.10), 'D8': (0.90, 0.05), 'D9': (0.65, 0.12),
            'D10': (0.60, 0.12)
        }
    },
    'Ariely': {
        'full_name': 'Dan Ariely',
        'cluster': 'Narrative',
        'priors': {
            'D1': (0.25, 0.08), 'D2': (0.70, 0.10), 'D3': (0.95, 0.03),
            'D4': (0.30, 0.10), 'D5': (0.75, 0.10), 'D6': (0.35, 0.08),
            'D7': (0.65, 0.12), 'D8': (0.85, 0.07), 'D9': (0.70, 0.12),
            'D10': (0.55, 0.12)
        }
    },
    'Kahneman': {
        'full_name': 'Daniel Kahneman',
        'cluster': 'Psychological',
        'priors': {
            'D1': (0.50, 0.12), 'D2': (0.65, 0.12), 'D3': (0.75, 0.10),
            'D4': (0.55, 0.12), 'D5': (0.60, 0.12), 'D6': (0.55, 0.10),
            'D7': (0.60, 0.12), 'D8': (0.30, 0.12), 'D9': (0.85, 0.07),
            'D10': (0.45, 0.15)
        }
    },
    'Sunstein': {
        'full_name': 'Cass Sunstein',
        'cluster': 'Policy',
        'priors': {
            'D1': (0.55, 0.10), 'D2': (0.50, 0.15), 'D3': (0.60, 0.12),
            'D4': (0.45, 0.12), 'D5': (0.95, 0.03), 'D6': (0.70, 0.10),
            'D7': (0.75, 0.10), 'D8': (0.25, 0.12), 'D9': (0.80, 0.08),
            'D10': (0.70, 0.10)
        }
    },
    'Mullainathan': {
        'full_name': 'Sendhil Mullainathan',
        'cluster': 'Policy',
        'priors': {
            'D1': (0.55, 0.12), 'D2': (0.85, 0.08), 'D3': (0.65, 0.12),
            'D4': (0.50, 0.12), 'D5': (0.85, 0.07), 'D6': (0.50, 0.12),
            'D7': (0.80, 0.08), 'D8': (0.40, 0.15), 'D9': (0.75, 0.10),
            'D10': (0.65, 0.12)
        }
    },
    'Autor': {
        'full_name': 'David Autor',
        'cluster': 'Causal',
        'priors': {
            'D1': (0.65, 0.10), 'D2': (0.95, 0.03), 'D3': (0.40, 0.12),
            'D4': (0.70, 0.08), 'D5': (0.80, 0.08), 'D6': (0.65, 0.10),
            'D7': (0.70, 0.10), 'D8': (0.10, 0.08), 'D9': (0.55, 0.12),
            'D10': (0.75, 0.08)
        }
    },
    'Shiller': {
        'full_name': 'Robert Shiller',
        'cluster': 'Causal',
        'priors': {
            'D1': (0.45, 0.12), 'D2': (0.55, 0.15), 'D3': (0.90, 0.05),
            'D4': (0.50, 0.12), 'D5': (0.70, 0.12), 'D6': (0.55, 0.12),
            'D7': (0.55, 0.15), 'D8': (0.35, 0.15), 'D9': (0.80, 0.10),
            'D10': (0.85, 0.07)
        }
    }
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class StyleVector:
    """10-dimensional style vector for a paper or author."""
    D1_formality: float = 0.0
    D2_evidence: float = 0.0
    D3_narrativity: float = 0.0
    D4_hedging: float = 0.0
    D5_policy: float = 0.0
    D6_syntax: float = 0.0
    D7_collaboration: float = 0.0
    D8_humor: float = 0.0
    D9_interdisciplinary: float = 0.0
    D10_temporal: float = 0.0

    def to_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([
            self.D1_formality, self.D2_evidence, self.D3_narrativity,
            self.D4_hedging, self.D5_policy, self.D6_syntax,
            self.D7_collaboration, self.D8_humor, self.D9_interdisciplinary,
            self.D10_temporal
        ])

    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'StyleVector':
        """Create from numpy array."""
        return cls(
            D1_formality=arr[0], D2_evidence=arr[1], D3_narrativity=arr[2],
            D4_hedging=arr[3], D5_policy=arr[4], D6_syntax=arr[5],
            D7_collaboration=arr[6], D8_humor=arr[7], D9_interdisciplinary=arr[8],
            D10_temporal=arr[9]
        )

    def distance(self, other: 'StyleVector') -> float:
        """Euclidean distance to another style vector."""
        return np.linalg.norm(self.to_array() - other.to_array())


@dataclass
class StyleProfile:
    """Complete style profile with uncertainty."""
    author: str
    cluster: str
    mean_vector: StyleVector
    std_vector: StyleVector
    n_papers: int = 0
    confidence_intervals: Dict[str, Tuple[float, float]] = field(default_factory=dict)


# =============================================================================
# STYLOMETRY ANALYZER
# =============================================================================

class StylometryAnalyzer:
    """Analyzes text to extract style dimensions."""

    def __init__(self):
        self.wordlists = WORDLISTS
        self.dimensions = DIMENSIONS

    def analyze_text(self, text: str, metadata: Optional[Dict] = None) -> StyleVector:
        """
        Analyze a paper text and return a 10D style vector.

        Args:
            text: Full text of the paper
            metadata: Optional dict with 'n_authors', 'n_pages', 'n_tables'

        Returns:
            StyleVector with all 10 dimensions
        """
        # Preprocessing
        text_lower = text.lower()
        sentences = self._split_sentences(text)
        words = self._tokenize(text_lower)
        n_words = len(words)
        n_sentences = len(sentences)

        if n_words == 0 or n_sentences == 0:
            return StyleVector()

        # Metadata defaults
        meta = metadata or {}
        n_pages = meta.get('n_pages', max(1, n_words // 500))
        n_authors = meta.get('n_authors', 1)
        n_tables = meta.get('n_tables', 0)

        # D1: Formality
        d1 = self._calc_formality(text, text_lower, words, n_pages)

        # D2: Evidence
        d2 = self._calc_evidence(text_lower, words, n_tables)

        # D3: Narrativity
        d3 = self._calc_narrativity(text_lower, words, n_words)

        # D4: Hedging
        d4 = self._calc_hedging(text_lower, words, n_sentences)

        # D5: Policy orientation
        d5 = self._calc_policy(text_lower, words)

        # D6: Syntactic complexity
        d6 = self._calc_syntax(sentences, text_lower, n_words, n_sentences)

        # D7: Collaboration
        d7 = self._calc_collaboration(text_lower, words, n_authors)

        # D8: Humor
        d8 = self._calc_humor(text_lower, words)

        # D9: Interdisciplinarity
        d9 = self._calc_interdisciplinary(text_lower, words)

        # D10: Temporal perspective
        d10 = self._calc_temporal(text_lower, words)

        return StyleVector(
            D1_formality=d1, D2_evidence=d2, D3_narrativity=d3,
            D4_hedging=d4, D5_policy=d5, D6_syntax=d6,
            D7_collaboration=d7, D8_humor=d8, D9_interdisciplinary=d9,
            D10_temporal=d10
        )

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting (could be improved with NLTK)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return re.findall(r'\b[a-z]+\b', text)

    def _count_matches(self, text: str, wordlist: List[str]) -> int:
        """Count occurrences of words from a wordlist."""
        count = 0
        for word in wordlist:
            count += len(re.findall(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE))
        return count

    def _calc_formality(self, text: str, text_lower: str, words: List[str], n_pages: int) -> float:
        """Calculate D1: Formality (0 = accessible, 1 = technical)."""
        # Formula density (LaTeX-style)
        formula_patterns = [r'\$.*?\$', r'\\frac', r'\\sum', r'\\int', r'\\partial']
        formulas = sum(len(re.findall(p, text)) for p in formula_patterns)
        formula_score = min(1.0, formulas / (n_pages * 3))  # ~3 formulas/page = 1.0

        # Technical vocabulary
        tech_count = self._count_matches(text_lower, self.wordlists['technical_terms'])
        tech_score = min(1.0, tech_count / (len(words) * 0.02))  # 2% technical = 1.0

        # Theorem density
        theorem_count = self._count_matches(text_lower, self.wordlists['theorem_markers'])
        theorem_score = min(1.0, theorem_count / (n_pages * 0.5))  # 0.5/page = 1.0

        return np.clip(0.4 * formula_score + 0.4 * tech_score + 0.2 * theorem_score, 0, 1)

    def _calc_evidence(self, text_lower: str, words: List[str], n_tables: int) -> float:
        """Calculate D2: Evidence style (0 = conceptual, 1 = empirical)."""
        # Statistical methods
        stat_count = self._count_matches(text_lower, self.wordlists['stat_methods'])
        stat_score = min(1.0, stat_count / 20)  # 20 stat terms = 1.0

        # Tables (from metadata or estimated)
        table_markers = len(re.findall(r'\btable\s*\d', text_lower))
        table_score = min(1.0, (n_tables + table_markers) / 8)  # 8 tables = 1.0

        # Data mentions
        data_terms = ['data', 'sample', 'observation', 'subject', 'participant', 'respondent']
        data_count = self._count_matches(text_lower, data_terms)
        data_score = min(1.0, data_count / 50)

        return np.clip(0.4 * stat_score + 0.3 * table_score + 0.3 * data_score, 0, 1)

    def _calc_narrativity(self, text_lower: str, words: List[str], n_words: int) -> float:
        """Calculate D3: Narrativity (0 = abstract, 1 = narrative)."""
        # Example density
        example_count = self._count_matches(text_lower, self.wordlists['example_markers'])
        example_score = min(1.0, example_count / 15)

        # First person usage
        first_person_count = sum(1 for w in words if w in self.wordlists['first_person'])
        fp_ratio = first_person_count / n_words
        fp_score = min(1.0, fp_ratio / 0.02)  # 2% first person = 1.0

        # Story markers
        story_terms = ['story', 'imagine', 'consider', 'picture', 'scenario']
        story_count = self._count_matches(text_lower, story_terms)
        story_score = min(1.0, story_count / 10)

        return np.clip(0.4 * example_score + 0.3 * fp_score + 0.3 * story_score, 0, 1)

    def _calc_hedging(self, text_lower: str, words: List[str], n_sentences: int) -> float:
        """Calculate D4: Hedging (0 = assertive, 1 = cautious)."""
        # Hedge words
        hedge_count = self._count_matches(text_lower, self.wordlists['hedge_words'])
        hedge_score = min(1.0, hedge_count / n_sentences)  # 1 hedge/sentence = 1.0

        # Caveats
        caveat_count = self._count_matches(text_lower, self.wordlists['caveat_words'])
        caveat_score = min(1.0, caveat_count / (n_sentences * 0.3))

        # Uncertainty markers
        uncertainty_terms = ['uncertain', 'unclear', 'ambiguous', 'approximately', 'roughly']
        unc_count = self._count_matches(text_lower, uncertainty_terms)
        unc_score = min(1.0, unc_count / 10)

        return np.clip(0.5 * hedge_score + 0.3 * caveat_score + 0.2 * unc_score, 0, 1)

    def _calc_policy(self, text_lower: str, words: List[str]) -> float:
        """Calculate D5: Policy orientation (0 = pure academic, 1 = applied)."""
        # Policy terms
        policy_count = self._count_matches(text_lower, self.wordlists['policy_terms'])
        policy_score = min(1.0, policy_count / 30)

        # Recommendation language
        rec_terms = ['should', 'recommend', 'suggest', 'propose', 'advise', 'implication']
        rec_count = self._count_matches(text_lower, rec_terms)
        rec_score = min(1.0, rec_count / 20)

        # Practical examples
        practical_terms = ['practice', 'practitioner', 'manager', 'firm', 'company', 'organization']
        prac_count = self._count_matches(text_lower, practical_terms)
        prac_score = min(1.0, prac_count / 15)

        return np.clip(0.4 * policy_score + 0.3 * rec_score + 0.3 * prac_score, 0, 1)

    def _calc_syntax(self, sentences: List[str], text_lower: str,
                     n_words: int, n_sentences: int) -> float:
        """Calculate D6: Syntactic complexity (0 = simple, 1 = complex)."""
        # Average sentence length
        avg_sent_len = n_words / max(1, n_sentences)
        sent_score = min(1.0, avg_sent_len / 35)  # 35 words/sentence = 1.0

        # Subordination (commas as proxy)
        comma_count = text_lower.count(',')
        sub_ratio = comma_count / max(1, n_sentences)
        sub_score = min(1.0, sub_ratio / 4)  # 4 commas/sentence = 1.0

        # Passive voice
        passive_count = self._count_matches(text_lower, self.wordlists['passive_markers'])
        passive_score = min(1.0, passive_count / (n_sentences * 0.3))

        return np.clip(0.4 * sent_score + 0.3 * sub_score + 0.3 * passive_score, 0, 1)

    def _calc_collaboration(self, text_lower: str, words: List[str], n_authors: int) -> float:
        """Calculate D7: Collaboration (0 = solo, 1 = team)."""
        # Author count
        author_score = min(1.0, (n_authors - 1) / 4)  # 5 authors = 1.0

        # We vs I ratio
        we_count = sum(1 for w in words if w in ['we', 'our', 'us'])
        i_count = sum(1 for w in words if w in ['i', 'my', 'me'])
        if we_count + i_count > 0:
            we_ratio = we_count / (we_count + i_count)
        else:
            we_ratio = 0.5

        # Acknowledgments (check for section)
        has_ack = 1.0 if 'acknowledgment' in text_lower or 'acknowledge' in text_lower else 0.0

        return np.clip(0.5 * author_score + 0.3 * we_ratio + 0.2 * has_ack, 0, 1)

    def _calc_humor(self, text_lower: str, words: List[str]) -> float:
        """Calculate D8: Humor (0 = serious, 1 = humorous)."""
        # Humor markers
        humor_count = self._count_matches(text_lower, self.wordlists['humor_markers'])
        humor_score = min(1.0, humor_count / 5)

        # Quotation marks (potential irony)
        quotes = len(re.findall(r'"[^"]{1,30}"', text_lower))
        quote_score = min(1.0, quotes / 10)

        # Exclamation marks (rare in academic writing)
        exclaim = text_lower.count('!')
        exclaim_score = min(1.0, exclaim / 3)

        return np.clip(0.5 * humor_score + 0.3 * quote_score + 0.2 * exclaim_score, 0, 1)

    def _calc_interdisciplinary(self, text_lower: str, words: List[str]) -> float:
        """Calculate D9: Interdisciplinarity (0 = mono, 1 = broad)."""
        # Count discipline markers
        psych = self._count_matches(text_lower, self.wordlists['psychology_terms'])
        neuro = self._count_matches(text_lower, self.wordlists['neuro_terms'])
        socio = self._count_matches(text_lower, self.wordlists['sociology_terms'])

        # Number of disciplines with significant presence
        disciplines = sum([psych > 5, neuro > 3, socio > 5])
        disc_score = disciplines / 3

        # Cross-reference terms
        cross_terms = ['interdisciplinary', 'cross-disciplinary', 'multidisciplinary', 'integrat']
        cross_count = self._count_matches(text_lower, cross_terms)
        cross_score = min(1.0, cross_count / 5)

        # Total discipline term density
        total_disc = psych + neuro + socio
        density_score = min(1.0, total_disc / 50)

        return np.clip(0.4 * disc_score + 0.3 * cross_score + 0.3 * density_score, 0, 1)

    def _calc_temporal(self, text_lower: str, words: List[str]) -> float:
        """Calculate D10: Temporal perspective (0 = historical, 1 = future)."""
        # Historical references
        hist_count = self._count_matches(text_lower, self.wordlists['historical_terms'])

        # Future references
        future_count = self._count_matches(text_lower, self.wordlists['future_terms'])

        # Calculate ratio (shifted to 0-1 scale)
        total = hist_count + future_count
        if total > 0:
            future_ratio = future_count / total
        else:
            future_ratio = 0.5  # Neutral if no temporal markers

        return np.clip(future_ratio, 0, 1)


# =============================================================================
# BOOTSTRAP CONFIDENCE INTERVALS
# =============================================================================

def bootstrap_ci(values: List[np.ndarray], n_bootstrap: int = 1000,
                 ci_level: float = 0.95) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate bootstrap confidence intervals for style vectors.

    Args:
        values: List of style vectors (as numpy arrays)
        n_bootstrap: Number of bootstrap samples
        ci_level: Confidence level (default 0.95)

    Returns:
        Tuple of (mean, ci_lower, ci_upper) arrays
    """
    if len(values) < 2:
        arr = values[0] if values else np.zeros(10)
        return arr, arr, arr

    values = np.array(values)
    n_samples = len(values)

    # Bootstrap sampling
    bootstrap_means = []
    for _ in range(n_bootstrap):
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        bootstrap_sample = values[indices]
        bootstrap_means.append(np.mean(bootstrap_sample, axis=0))

    bootstrap_means = np.array(bootstrap_means)

    # Calculate percentiles
    alpha = (1 - ci_level) / 2
    ci_lower = np.percentile(bootstrap_means, alpha * 100, axis=0)
    ci_upper = np.percentile(bootstrap_means, (1 - alpha) * 100, axis=0)
    mean = np.mean(values, axis=0)

    return mean, ci_lower, ci_upper


# =============================================================================
# DISTANCE CALCULATIONS
# =============================================================================

def euclidean_distance(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calculate Euclidean distance between two style vectors."""
    return np.linalg.norm(v1 - v2)


def calculate_distance_matrix(profiles: Dict[str, StyleProfile]) -> np.ndarray:
    """Calculate pairwise distance matrix between all author profiles."""
    authors = list(profiles.keys())
    n = len(authors)
    matrix = np.zeros((n, n))

    for i, a1 in enumerate(authors):
        for j, a2 in enumerate(authors):
            if i < j:
                d = profiles[a1].mean_vector.distance(profiles[a2].mean_vector)
                matrix[i, j] = d
                matrix[j, i] = d

    return matrix, authors


# =============================================================================
# MAIN CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='SWSM Stylometry Analyzer - Analyze scientific writing styles'
    )
    parser.add_argument('--text', type=str, help='Path to text file to analyze')
    parser.add_argument('--author', type=str, help='Author name to show priors')
    parser.add_argument('--all-authors', action='store_true', help='Show all author profiles')
    parser.add_argument('--distance', action='store_true', help='Show distance matrix')
    parser.add_argument('--validate', action='store_true', help='Run validation')
    parser.add_argument('--bootstrap', type=int, default=1000, help='Bootstrap iterations')
    parser.add_argument('--output', type=str, help='Output file (JSON)')

    args = parser.parse_args()

    analyzer = StylometryAnalyzer()

    # Analyze a text file
    if args.text:
        with open(args.text, 'r', encoding='utf-8') as f:
            text = f.read()

        vector = analyzer.analyze_text(text)
        print("\n=== STYLE VECTOR ===")
        print(f"D1 Formality:        {vector.D1_formality:.2f}")
        print(f"D2 Evidence:         {vector.D2_evidence:.2f}")
        print(f"D3 Narrativity:      {vector.D3_narrativity:.2f}")
        print(f"D4 Hedging:          {vector.D4_hedging:.2f}")
        print(f"D5 Policy:           {vector.D5_policy:.2f}")
        print(f"D6 Syntax:           {vector.D6_syntax:.2f}")
        print(f"D7 Collaboration:    {vector.D7_collaboration:.2f}")
        print(f"D8 Humor:            {vector.D8_humor:.2f}")
        print(f"D9 Interdisciplinary:{vector.D9_interdisciplinary:.2f}")
        print(f"D10 Temporal:        {vector.D10_temporal:.2f}")

    # Show author priors
    if args.author:
        if args.author in AUTHOR_PRIORS:
            p = AUTHOR_PRIORS[args.author]
            print(f"\n=== {p['full_name']} ({p['cluster']}) ===")
            for dim, (mean, std) in p['priors'].items():
                name = DIMENSIONS.get(f'{dim}_formality', {}).get('name', dim)
                print(f"{dim}: {mean:.2f} ± {std:.2f}")
        else:
            print(f"Unknown author: {args.author}")
            print(f"Available: {', '.join(AUTHOR_PRIORS.keys())}")

    # Show all authors
    if args.all_authors:
        print("\n=== ALL AUTHOR PROFILES ===")
        print(f"{'Author':<15} {'Cluster':<12} {'D1':>5} {'D2':>5} {'D3':>5} {'D4':>5} {'D5':>5} {'D6':>5} {'D7':>5} {'D8':>5} {'D9':>5} {'D10':>5}")
        print("-" * 90)
        for name, p in AUTHOR_PRIORS.items():
            priors = p['priors']
            print(f"{name:<15} {p['cluster']:<12} "
                  f"{priors['D1'][0]:>5.2f} {priors['D2'][0]:>5.2f} {priors['D3'][0]:>5.2f} "
                  f"{priors['D4'][0]:>5.2f} {priors['D5'][0]:>5.2f} {priors['D6'][0]:>5.2f} "
                  f"{priors['D7'][0]:>5.2f} {priors['D8'][0]:>5.2f} {priors['D9'][0]:>5.2f} "
                  f"{priors['D10'][0]:>5.2f}")

    # Show distance matrix
    if args.distance:
        print("\n=== DISTANCE MATRIX (Euclidean) ===")
        # Create profiles from priors
        profiles = {}
        for name, p in AUTHOR_PRIORS.items():
            means = [p['priors'][f'D{i}'][0] for i in range(1, 11)]
            profiles[name] = StyleProfile(
                author=name,
                cluster=p['cluster'],
                mean_vector=StyleVector.from_array(np.array(means)),
                std_vector=StyleVector(),
                n_papers=0
            )

        matrix, authors = calculate_distance_matrix(profiles)

        # Print header
        print(f"{'':>12}", end='')
        for a in authors:
            print(f"{a[:6]:>7}", end='')
        print()

        # Print matrix
        for i, a1 in enumerate(authors):
            print(f"{a1:<12}", end='')
            for j, a2 in enumerate(authors):
                if i == j:
                    print(f"{'—':>7}", end='')
                else:
                    print(f"{matrix[i,j]:>7.2f}", end='')
            print()

    # Output to JSON
    if args.output:
        output_data = {
            'dimensions': DIMENSIONS,
            'author_priors': AUTHOR_PRIORS,
            'session': 'EBF-S-2026-01-29-SWSM-001'
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nOutput saved to {args.output}")


if __name__ == '__main__':
    main()
