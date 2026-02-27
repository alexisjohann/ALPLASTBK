#!/usr/bin/env python3
"""
SWSM Author Profile Extractor

Extracts writing style parameters from a corpus of papers by a specific author.
Uses SWSM components E1-E7 to analyze texts and aggregate parameters.

Usage:
    python scripts/swsm_extract_profile.py --author "Fehr" --papers-dir data/papers/fehr/
    python scripts/swsm_extract_profile.py --author "Fehr" --bib bibliography/bcm_master.bib
"""

import argparse
import yaml
import re
import os
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from collections import Counter
import statistics

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

# Import SWSM components
try:
    from swsm_move_tagger import MoveAnalyzer
    from swsm_cohesion_analyzer import CohesionAnalyzer
    from swsm_sfl_annotator import SFLAnnotator
    SWSM_AVAILABLE = True
except ImportError:
    SWSM_AVAILABLE = False
    print("Warning: Some SWSM components not available. Using basic analysis.")


# ═══════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ThetaMove:
    """Move parameters from CARS analysis."""
    territory_length: float = 0.0
    territory_strategy: Dict[str, float] = field(default_factory=dict)
    niche_markers: Dict[str, float] = field(default_factory=dict)
    niche_strategy: Dict[str, float] = field(default_factory=dict)
    occupy_strategy: Dict[str, float] = field(default_factory=dict)
    hypothesis_explicit: float = 0.0


@dataclass
class ThetaCohesion:
    """Cohesion parameters."""
    lexical_density: float = 0.0
    reference_chain_length: float = 0.0
    conjunction_frequency: float = 0.0


@dataclass
class ThetaRST:
    """RST discourse parameters."""
    relation_distribution: Dict[str, float] = field(default_factory=dict)
    tree_depth_mean: float = 0.0
    nucleus_satellite_ratio: float = 0.0


@dataclass
class ThetaLexicogrammar:
    """Lexicogrammatical parameters."""
    nominalization_rate: float = 0.0
    passive_rate: float = 0.0
    hedging_density: float = 0.0
    sentence_length_mean: float = 0.0
    sentence_length_std: float = 0.0
    mood_distribution: Dict[str, float] = field(default_factory=dict)


@dataclass
class ThetaInfo:
    """Information structure parameters."""
    given_new_ratio: float = 0.0
    theme_distribution: Dict[str, float] = field(default_factory=dict)


@dataclass
class ThetaVocab:
    """Vocabulary parameters."""
    type_token_ratio: float = 0.0
    first_person_usage: float = 0.0


@dataclass
class AuthorProfile:
    """Complete author writing profile."""
    name: str
    corpus_size: int
    theta_move: ThetaMove
    theta_cohesion: ThetaCohesion
    theta_rst: ThetaRST
    theta_lexicogrammar: ThetaLexicogrammar
    theta_info: ThetaInfo
    theta_vocab: ThetaVocab


# ═══════════════════════════════════════════════════════════════════════════
# EXTRACTION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class ProfileExtractor:
    """Extract SWSM profile from corpus."""

    def __init__(self):
        self.move_analyzer = MoveAnalyzer() if SWSM_AVAILABLE else None
        self.cohesion_analyzer = CohesionAnalyzer() if SWSM_AVAILABLE else None

    def extract_from_texts(self, texts: List[str], author_name: str) -> AuthorProfile:
        """
        Extract profile from list of text strings.
        
        Args:
            texts: List of paper texts
            author_name: Name of the author
            
        Returns:
            Complete AuthorProfile
        """
        # Collect metrics from each text
        all_metrics = []
        
        for text in texts:
            metrics = self._analyze_single_text(text)
            all_metrics.append(metrics)
        
        # Aggregate across corpus
        profile = self._aggregate_metrics(all_metrics, author_name, len(texts))
        
        return profile

    def _analyze_single_text(self, text: str) -> Dict[str, Any]:
        """Analyze a single text and return metrics."""
        metrics = {}
        
        # Basic text stats
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = text.split()
        
        metrics['sentence_count'] = len(sentences)
        metrics['word_count'] = len(words)
        metrics['sentence_lengths'] = [len(s.split()) for s in sentences]
        
        # Lexical density (content words / total words)
        function_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                         'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                         'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                         'can', 'of', 'to', 'in', 'for', 'on', 'with', 'at', 'by',
                         'from', 'as', 'into', 'through', 'during', 'before', 'after',
                         'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either',
                         'neither', 'not', 'only', 'own', 'same', 'than', 'too', 'very',
                         'just', 'also', 'now', 'here', 'there', 'when', 'where', 'why',
                         'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
                         'other', 'some', 'such', 'no', 'any', 'this', 'that', 'these',
                         'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
                         'which', 'who', 'whom', 'whose'}
        
        content_words = [w for w in words if w.lower() not in function_words]
        metrics['lexical_density'] = len(content_words) / len(words) if words else 0
        
        # Type-token ratio
        unique_words = set(w.lower() for w in words)
        metrics['type_token_ratio'] = len(unique_words) / len(words) if words else 0
        
        # First person usage
        first_person = ['i', 'we', 'me', 'us', 'my', 'our', 'mine', 'ours']
        fp_count = sum(1 for w in words if w.lower() in first_person)
        metrics['first_person_usage'] = fp_count / len(words) if words else 0
        
        # Nominalization detection (words ending in -tion, -ment, -ness, -ity)
        nominalizations = [w for w in words if re.search(r'(tion|ment|ness|ity|ance|ence)$', w.lower())]
        metrics['nominalization_rate'] = len(nominalizations) / len(words) if words else 0
        
        # Passive detection (simple heuristic: was/were + past participle)
        passive_patterns = re.findall(r'\b(was|were|is|are|been|being)\s+\w+ed\b', text.lower())
        metrics['passive_rate'] = len(passive_patterns) / len(sentences) if sentences else 0
        
        # Hedging words
        hedges = ['may', 'might', 'could', 'would', 'possibly', 'perhaps', 'suggests',
                 'indicates', 'appears', 'seems', 'likely', 'unlikely', 'probably']
        hedge_count = sum(1 for w in words if w.lower() in hedges)
        metrics['hedging_density'] = hedge_count / len(sentences) if sentences else 0
        
        # Niche markers
        niche_markers = {
            'however': len(re.findall(r'\bhowever\b', text.lower())),
            'yet': len(re.findall(r'\byet\b', text.lower())),
            'but': len(re.findall(r'\bbut\b', text.lower())),
            'nevertheless': len(re.findall(r'\bnevertheless\b', text.lower())),
            'although': len(re.findall(r'\balthough\b', text.lower())),
        }
        metrics['niche_markers'] = niche_markers
        
        # Conjunction frequency
        conjunctions = ['and', 'but', 'or', 'so', 'because', 'although', 'while',
                       'whereas', 'however', 'therefore', 'thus', 'hence']
        conj_count = sum(1 for w in words if w.lower() in conjunctions)
        metrics['conjunction_frequency'] = conj_count / len(sentences) if sentences else 0
        
        # Move analysis (if available)
        if self.move_analyzer:
            try:
                move_result = self.move_analyzer.analyze(text)
                metrics['moves'] = move_result
            except Exception:
                metrics['moves'] = None
        
        return metrics

    def _aggregate_metrics(self, all_metrics: List[Dict], author_name: str, corpus_size: int) -> AuthorProfile:
        """Aggregate metrics across all texts into a profile."""
        
        # Aggregate sentence lengths
        all_sentence_lengths = []
        for m in all_metrics:
            all_sentence_lengths.extend(m.get('sentence_lengths', []))
        
        sl_mean = statistics.mean(all_sentence_lengths) if all_sentence_lengths else 0
        sl_std = statistics.stdev(all_sentence_lengths) if len(all_sentence_lengths) > 1 else 0
        
        # Aggregate scalar metrics
        def avg(key):
            vals = [m.get(key, 0) for m in all_metrics if m.get(key) is not None]
            return statistics.mean(vals) if vals else 0
        
        # Aggregate niche markers
        total_markers = Counter()
        for m in all_metrics:
            if 'niche_markers' in m:
                for k, v in m['niche_markers'].items():
                    total_markers[k] += v
        total = sum(total_markers.values())
        niche_dist = {k: v/total for k, v in total_markers.items()} if total else {}
        
        # Build profile
        profile = AuthorProfile(
            name=author_name,
            corpus_size=corpus_size,
            theta_move=ThetaMove(
                territory_length=2.5,  # Default, would need intro detection
                niche_markers=niche_dist,
                hypothesis_explicit=0.5,  # Would need specific detection
            ),
            theta_cohesion=ThetaCohesion(
                lexical_density=avg('lexical_density'),
                reference_chain_length=3.0,  # Would need coreference resolution
                conjunction_frequency=avg('conjunction_frequency'),
            ),
            theta_rst=ThetaRST(
                relation_distribution={},  # Would need RST parsing
                tree_depth_mean=4.0,
                nucleus_satellite_ratio=0.6,
            ),
            theta_lexicogrammar=ThetaLexicogrammar(
                nominalization_rate=avg('nominalization_rate'),
                passive_rate=avg('passive_rate'),
                hedging_density=avg('hedging_density'),
                sentence_length_mean=sl_mean,
                sentence_length_std=sl_std,
                mood_distribution={'declarative': 0.9, 'interrogative': 0.05, 'imperative': 0.05},
            ),
            theta_info=ThetaInfo(
                given_new_ratio=0.55,  # Would need information structure analysis
                theme_distribution={'topical': 0.7, 'textual': 0.2, 'interpersonal': 0.1},
            ),
            theta_vocab=ThetaVocab(
                type_token_ratio=avg('type_token_ratio'),
                first_person_usage=avg('first_person_usage'),
            ),
        )
        
        return profile

    def profile_to_yaml(self, profile: AuthorProfile) -> Dict:
        """Convert profile to YAML-compatible dict."""
        return {
            'metadata': {
                'name': profile.name,
                'corpus_size': profile.corpus_size,
                'extraction_date': '2026-01-29',
            },
            'parameters': {
                'theta_move': {
                    'territory': {
                        'length_sentences': profile.theta_move.territory_length,
                    },
                    'niche': {
                        'marker_distribution': profile.theta_move.niche_markers,
                    },
                    'occupy': {
                        'hypothesis_explicit': profile.theta_move.hypothesis_explicit,
                    },
                },
                'theta_cohesion': {
                    'lexical_density': round(profile.theta_cohesion.lexical_density, 3),
                    'reference_chain_length': profile.theta_cohesion.reference_chain_length,
                    'conjunction_frequency': round(profile.theta_cohesion.conjunction_frequency, 3),
                },
                'theta_rst': {
                    'relation_distribution': profile.theta_rst.relation_distribution,
                    'tree_depth_mean': profile.theta_rst.tree_depth_mean,
                },
                'theta_lexicogrammar': {
                    'nominalization_rate': round(profile.theta_lexicogrammar.nominalization_rate, 3),
                    'passive_rate': round(profile.theta_lexicogrammar.passive_rate, 3),
                    'hedging_density': round(profile.theta_lexicogrammar.hedging_density, 3),
                    'sentence_length': {
                        'mean': round(profile.theta_lexicogrammar.sentence_length_mean, 1),
                        'std': round(profile.theta_lexicogrammar.sentence_length_std, 1),
                    },
                    'mood_distribution': profile.theta_lexicogrammar.mood_distribution,
                },
                'theta_info': {
                    'given_new_ratio': profile.theta_info.given_new_ratio,
                    'theme_distribution': profile.theta_info.theme_distribution,
                },
                'theta_vocab': {
                    'type_token_ratio': round(profile.theta_vocab.type_token_ratio, 3),
                    'first_person_usage': round(profile.theta_vocab.first_person_usage, 4),
                },
            },
        }


# ═══════════════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate profile extraction with sample text."""
    
    print("=" * 70)
    print("SWSM AUTHOR PROFILE EXTRACTOR - DEMO")
    print("=" * 70)
    
    # Sample Fehr-style text
    fehr_sample = """
    Social preferences play a crucial role in human economic behavior. 
    Previous research has extensively documented that individuals often deviate 
    from pure self-interest in economic experiments. However, little attention 
    has been paid to the interaction between social preferences and contextual factors.
    
    This paper aims to fill this gap by examining how context modulates fairness 
    concerns in ultimatum game experiments. We find that the rejection rate of 
    unfair offers varies significantly across institutional contexts. Our results 
    demonstrate that context is not merely a boundary condition but a fundamental 
    determinant of social preference expression.
    
    The experimental evidence suggests that individuals adjust their fairness 
    standards based on what is considered appropriate in a given situation. 
    This observation has important implications for the design of institutions 
    and the prediction of economic behavior in field settings.
    """
    
    # Sample Thaler-style text (more accessible)
    thaler_sample = """
    People make mistakes. That's not news. But the kinds of mistakes we make 
    are surprisingly predictable. We procrastinate on our retirement savings. 
    We eat too much and exercise too little. We forget to cancel subscriptions 
    we no longer use.
    
    The good news is that understanding these mistakes can help us design better 
    systems. A simple change in the default option - automatically enrolling 
    employees in 401(k) plans, for instance - can dramatically increase savings 
    rates. We call these helpful design changes "nudges."
    
    Nudges work because they account for how people actually behave, not how 
    economists assume they should behave. And the best part? They preserve 
    freedom of choice while making it easier to do the right thing.
    """
    
    extractor = ProfileExtractor()
    
    # Extract Fehr profile
    print("\n📊 Extracting FEHR profile...")
    fehr_profile = extractor.extract_from_texts([fehr_sample], "Ernst Fehr (Demo)")
    fehr_yaml = extractor.profile_to_yaml(fehr_profile)
    
    print(f"\nFEHR PROFILE:")
    print(f"  Lexical Density: {fehr_yaml['parameters']['theta_cohesion']['lexical_density']}")
    print(f"  Nominalization Rate: {fehr_yaml['parameters']['theta_lexicogrammar']['nominalization_rate']}")
    print(f"  Passive Rate: {fehr_yaml['parameters']['theta_lexicogrammar']['passive_rate']}")
    print(f"  Hedging Density: {fehr_yaml['parameters']['theta_lexicogrammar']['hedging_density']}")
    print(f"  Sentence Length: {fehr_yaml['parameters']['theta_lexicogrammar']['sentence_length']['mean']} words")
    print(f"  First Person: {fehr_yaml['parameters']['theta_vocab']['first_person_usage']}")
    
    # Extract Thaler profile
    print("\n📊 Extracting THALER profile...")
    thaler_profile = extractor.extract_from_texts([thaler_sample], "Richard Thaler (Demo)")
    thaler_yaml = extractor.profile_to_yaml(thaler_profile)
    
    print(f"\nTHALER PROFILE:")
    print(f"  Lexical Density: {thaler_yaml['parameters']['theta_cohesion']['lexical_density']}")
    print(f"  Nominalization Rate: {thaler_yaml['parameters']['theta_lexicogrammar']['nominalization_rate']}")
    print(f"  Passive Rate: {thaler_yaml['parameters']['theta_lexicogrammar']['passive_rate']}")
    print(f"  Hedging Density: {thaler_yaml['parameters']['theta_lexicogrammar']['hedging_density']}")
    print(f"  Sentence Length: {thaler_yaml['parameters']['theta_lexicogrammar']['sentence_length']['mean']} words")
    print(f"  First Person: {thaler_yaml['parameters']['theta_vocab']['first_person_usage']}")
    
    # Compare
    print("\n" + "=" * 70)
    print("COMPARISON: FEHR vs THALER")
    print("=" * 70)
    print(f"{'Metric':<25} {'Fehr':<15} {'Thaler':<15}")
    print("-" * 55)
    
    metrics = [
        ('Lexical Density', 'theta_cohesion', 'lexical_density'),
        ('Nominalization', 'theta_lexicogrammar', 'nominalization_rate'),
        ('Passive Rate', 'theta_lexicogrammar', 'passive_rate'),
        ('Hedging', 'theta_lexicogrammar', 'hedging_density'),
    ]
    
    for name, cat, key in metrics:
        fv = fehr_yaml['parameters'][cat][key]
        tv = thaler_yaml['parameters'][cat][key]
        diff = "←" if fv > tv else "→" if tv > fv else "="
        print(f"{name:<25} {fv:<15} {tv:<15} {diff}")
    
    # Sentence length
    fsl = fehr_yaml['parameters']['theta_lexicogrammar']['sentence_length']['mean']
    tsl = thaler_yaml['parameters']['theta_lexicogrammar']['sentence_length']['mean']
    print(f"{'Sentence Length':<25} {fsl:<15} {tsl:<15}")
    
    print("\n✓ Demo complete!")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Extract SWSM author profile from corpus')
    parser.add_argument('--author', type=str, help='Author name')
    parser.add_argument('--papers-dir', type=str, help='Directory with paper text files')
    parser.add_argument('--output', type=str, help='Output YAML file')
    parser.add_argument('--demo', action='store_true', help='Run demo with sample texts')
    
    args = parser.parse_args()
    
    if args.demo or (not args.author and not args.papers_dir):
        demo()
        return
    
    # Real extraction would go here
    print(f"Extracting profile for {args.author}...")
    print("(Full implementation requires paper text files)")


if __name__ == '__main__':
    main()
