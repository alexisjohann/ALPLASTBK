#!/usr/bin/env python3
"""
generate_style_prompt.py - LLM Prompt Generator from 8D Document Type Profiles

Based on EBF Appendices CCC (METHOD-DOCTYPE) and DDD (REF-DOCTYPE).
Generates system prompts for LLMs to write in specific styles.

Theory Foundation:
- 8D → Structure (Axiom DT-5, DT-6)
- 8D → Style → Vocabulary (Axiom DT-7, DT-8, DT-9)

Usage:
    python generate_style_prompt.py --author "Ernst Fehr"
    python generate_style_prompt.py --profile 0.9,0.85,0.5,0.6,0.5,0.85,0.25,0.95
    python generate_style_prompt.py --list-authors
"""

import argparse
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class DocumentType8D:
    """8-dimensional document type specification (Axiom DT-1)."""
    D1_expertise: float      # Technical expertise level [0,1]
    D2_formality: float      # Formality degree [0,1]
    D3_emotional: float      # Emotional engagement [0,1]
    D4_complexity: float     # Cognitive complexity [0,1]
    D5_temporal: float       # Temporal orientation [0,1]
    D6_evidence: float       # Evidence requirements [0,1]
    D7_narrative: float      # Narrative vs analytical [0,1]
    D8_precision: float      # Precision requirements [0,1]

    def __post_init__(self):
        for i, val in enumerate([self.D1_expertise, self.D2_formality,
                                  self.D3_emotional, self.D4_complexity,
                                  self.D5_temporal, self.D6_evidence,
                                  self.D7_narrative, self.D8_precision], 1):
            if not 0 <= val <= 1:
                raise ValueError(f"D{i} must be in [0,1], got {val}")

    @classmethod
    def from_tuple(cls, values: Tuple[float, ...]) -> 'DocumentType8D':
        if len(values) != 8:
            raise ValueError(f"Expected 8 values, got {len(values)}")
        return cls(*values)


@dataclass
class StyleParameters:
    """Style parameters derived from 8D (Axiom DT-7)."""
    sentence_length_range: Tuple[int, int]
    clause_complexity: str  # "simple", "moderate", "complex"
    tone: str               # "casual", "neutral", "formal", "academic"
    pronoun_style: str      # "first_singular", "first_plural", "third", "impersonal"
    hedging_required: bool
    boosters_allowed: bool
    narrative_elements: bool
    citation_style: str     # "none", "inline", "footnote", "academic"


@dataclass
class VocabularyGuide:
    """Vocabulary constraints derived from style (Axiom DT-9)."""
    hedging_words: List[str]
    booster_words: List[str]
    connectives: List[str]
    forbidden_words: List[str]
    technical_terms_level: str  # "basic", "intermediate", "advanced", "expert"
    example_phrases: List[str]


# =============================================================================
# PREDEFINED AUTHOR PROFILES
# =============================================================================

AUTHOR_PROFILES: Dict[str, Tuple[DocumentType8D, str, str]] = {
    # (8D Profile, Description, Language)

    "Ernst Fehr": (
        DocumentType8D(0.90, 0.85, 0.15, 0.60, 0.50, 0.85, 0.25, 0.95),
        "Academic behavioral economics - precise, evidence-based, collaborative",
        "en"
    ),

    "NYT Opinion": (
        DocumentType8D(0.45, 0.60, 0.55, 0.45, 0.70, 0.50, 0.65, 0.60),
        "New York Times opinion style - accessible, engaging, contemporary",
        "en"
    ),

    "Der Spiegel": (
        DocumentType8D(0.50, 0.65, 0.50, 0.55, 0.75, 0.55, 0.60, 0.65),
        "German investigative journalism - analytical, critical, thorough",
        "de"
    ),

    "BCM Appendix": (
        DocumentType8D(0.95, 0.90, 0.10, 0.80, 0.30, 0.90, 0.15, 0.95),
        "EBF Framework appendix style - formal, mathematical, precise",
        "en"
    ),

    "FehrAdvice Report": (
        DocumentType8D(0.70, 0.75, 0.25, 0.55, 0.60, 0.70, 0.35, 0.80),
        "Consulting report - professional, evidence-based, actionable",
        "de"
    ),

    "Blog Post": (
        DocumentType8D(0.35, 0.40, 0.60, 0.35, 0.80, 0.30, 0.75, 0.45),
        "Casual blog style - personal, engaging, conversational",
        "en"
    ),

    "Scientific Abstract": (
        DocumentType8D(0.95, 0.95, 0.05, 0.70, 0.40, 0.95, 0.10, 0.98),
        "Academic abstract - maximally concise, formal, precise",
        "en"
    ),

    "TED Talk": (
        DocumentType8D(0.55, 0.50, 0.70, 0.45, 0.65, 0.45, 0.80, 0.55),
        "TED presentation style - inspirational, narrative, accessible",
        "en"
    ),

    "Reinhard Sprenger": (
        DocumentType8D(0.60, 0.55, 0.55, 0.50, 0.70, 0.40, 0.65, 0.60),
        "German management provocateur - direct, challenging, anti-bureaucratic",
        "de"
    ),

    "The Economist": (
        DocumentType8D(0.65, 0.70, 0.35, 0.55, 0.80, 0.65, 0.40, 0.70),
        "British weekly - authoritative, witty, globally-minded, opinionated",
        "en"
    ),

    "Yuval Noah Harari": (
        DocumentType8D(0.70, 0.60, 0.50, 0.65, 0.55, 0.60, 0.75, 0.55),
        "Big-history storyteller - sweeping narratives, accessible philosophy",
        "en"
    ),

    "Steven Pinker": (
        DocumentType8D(0.80, 0.65, 0.35, 0.70, 0.60, 0.85, 0.45, 0.80),
        "Cognitive scientist - data-driven optimism, rigorous, clear prose",
        "en"
    ),

    "Nassim Taleb": (
        DocumentType8D(0.75, 0.45, 0.70, 0.70, 0.50, 0.65, 0.55, 0.60),
        "Flaneur-philosopher - combative, aphoristic, anti-fragile thinking",
        "en"
    ),

    "Donald Trump": (
        DocumentType8D(0.15, 0.20, 0.90, 0.15, 0.85, 0.10, 0.70, 0.15),
        "Populist rhetoric - simple, repetitive, superlative, emotional",
        "en"
    ),

    "Daron Acemoglu": (
        DocumentType8D(0.85, 0.80, 0.25, 0.75, 0.55, 0.90, 0.50, 0.85),
        "Institutional economist - rigorous, historical, inclusive/extractive framework",
        "en"
    ),
}


# =============================================================================
# STYLE DERIVATION (Axiom DT-7, DT-8)
# =============================================================================

def derive_style(doc_type: DocumentType8D) -> StyleParameters:
    """
    Derive style parameters from 8D coordinates.
    Implements: σ = s(D) where s: [0,1]^8 → Σ
    """
    # Sentence length: Higher expertise + formality → longer sentences
    base_length = 12 + int(doc_type.D1_expertise * 10) + int(doc_type.D2_formality * 8)
    length_variance = 6 if doc_type.D4_complexity > 0.5 else 4
    sentence_length = (base_length - length_variance, base_length + length_variance)

    # Clause complexity
    complexity_score = (doc_type.D1_expertise + doc_type.D4_complexity) / 2
    if complexity_score > 0.7:
        clause_complexity = "complex"
    elif complexity_score > 0.4:
        clause_complexity = "moderate"
    else:
        clause_complexity = "simple"

    # Tone
    if doc_type.D2_formality > 0.8:
        tone = "academic"
    elif doc_type.D2_formality > 0.6:
        tone = "formal"
    elif doc_type.D2_formality > 0.4:
        tone = "neutral"
    else:
        tone = "casual"

    # Pronoun style
    if doc_type.D2_formality > 0.75 and doc_type.D1_expertise > 0.7:
        pronoun_style = "first_plural"  # Academic "we"
    elif doc_type.D7_narrative > 0.6:
        pronoun_style = "first_singular"  # Personal narrative
    elif doc_type.D2_formality > 0.6:
        pronoun_style = "impersonal"
    else:
        pronoun_style = "third"

    # Hedging & Boosters
    hedging_required = doc_type.D6_evidence > 0.7 and doc_type.D8_precision > 0.7
    boosters_allowed = doc_type.D3_emotional > 0.5 or doc_type.D7_narrative > 0.6

    # Narrative elements
    narrative_elements = doc_type.D7_narrative > 0.5

    # Citation style
    if doc_type.D6_evidence > 0.8 and doc_type.D2_formality > 0.8:
        citation_style = "academic"
    elif doc_type.D6_evidence > 0.6:
        citation_style = "inline"
    elif doc_type.D6_evidence > 0.3:
        citation_style = "footnote"
    else:
        citation_style = "none"

    return StyleParameters(
        sentence_length_range=sentence_length,
        clause_complexity=clause_complexity,
        tone=tone,
        pronoun_style=pronoun_style,
        hedging_required=hedging_required,
        boosters_allowed=boosters_allowed,
        narrative_elements=narrative_elements,
        citation_style=citation_style
    )


# =============================================================================
# VOCABULARY DERIVATION (Axiom DT-9)
# =============================================================================

# Word banks
HEDGING_WORDS = [
    "suggests", "may", "might", "could", "appears", "seems",
    "indicates", "possibly", "potentially", "arguably", "presumably",
    "tentatively", "approximately", "roughly", "likely"
]

BOOSTER_WORDS = [
    "clearly", "certainly", "undoubtedly", "obviously", "definitely",
    "absolutely", "truly", "really", "extremely", "very",
    "fundamentally", "essentially", "remarkably"
]

FORMAL_CONNECTIVES = [
    "therefore", "consequently", "however", "moreover", "furthermore",
    "nevertheless", "nonetheless", "thus", "hence", "accordingly",
    "subsequently", "notwithstanding", "whereby"
]

CASUAL_CONNECTIVES = [
    "so", "but", "and", "also", "plus", "anyway",
    "besides", "actually", "basically", "honestly"
]

ACADEMIC_PHRASES = [
    "empirical evidence suggests",
    "consistent with theoretical predictions",
    "we hypothesize that",
    "our findings indicate",
    "the results demonstrate",
    "as shown in Figure X",
    "controlling for confounding factors"
]

NARRATIVE_PHRASES = [
    "imagine this scenario",
    "let me tell you a story",
    "here's what happened",
    "picture yourself",
    "think about it this way",
    "the journey began when"
]

SPRENGER_PHRASES = [
    "Warum eigentlich?",
    "Das Gegenteil ist der Fall.",
    "Hören Sie auf damit.",
    "Das ist keine Führung, das ist Kontrolle.",
    "Vertrauen Sie Ihren Mitarbeitern.",
    "Selbstverantwortung statt Fremdsteuerung."
]

ECONOMIST_PHRASES = [
    "This newspaper believes...",
    "The world ought to...",
    "Governments should...",
    "That is a pity.",
    "Alas, the opposite is true.",
    "The answer, it turns out, is more nuanced."
]

HARARI_PHRASES = [
    "For thousands of years...",
    "Homo sapiens conquered the world because...",
    "The real question is not whether... but whether...",
    "This is one of history's greatest ironies.",
    "We have become gods, but...",
    "The agricultural revolution was history's biggest fraud."
]

PINKER_PHRASES = [
    "The data clearly show that...",
    "Contrary to popular belief...",
    "This represents a X% decline since...",
    "The reason is not hard to find.",
    "Progress is not inevitable, but...",
    "The numbers speak for themselves."
]

TALEB_PHRASES = [
    "The more you know, the less you know you know.",
    "Skin in the game.",
    "This is fragile. That is antifragile.",
    "Intellectuals Yet Idiots (IYI)...",
    "Never trust anyone who doesn't have skin in the game.",
    "Fat tails dominate."
]

TRUMP_PHRASES = [
    "Believe me.",
    "Nobody knows more about X than me.",
    "It's going to be huge. Tremendous.",
    "Many people are saying...",
    "The best. The greatest. Ever.",
    "Sad!"
]

ACEMOGLU_PHRASES = [
    "Inclusive institutions...",
    "Extractive institutions...",
    "The historical evidence suggests...",
    "This pattern is consistent with...",
    "Critical junctures in history...",
    "The persistence of institutional differences..."
]

# Author-specific example transformations
AUTHOR_TRANSFORMATIONS = {
    "Reinhard Sprenger": (
        '"People often make irrational financial decisions."',
        '"Hören Sie auf, Menschen als irrational zu bezeichnen. Sie handeln '
        'nach ihrer eigenen Logik. Das Problem ist nicht der Mensch – '
        'das Problem ist Ihre Erwartung, dass er sich wie ein '
        'Ökonomie-Lehrbuch verhält."'
    ),
    "Ernst Fehr": (
        '"People often make irrational financial decisions."',
        '"Empirical evidence suggests that individuals may systematically deviate '
        'from rational choice predictions in financial decision-making contexts, '
        'consistent with behavioral economic theory."'
    ),
    "The Economist": (
        '"People often make irrational financial decisions."',
        '"Homo economicus, that mythical creature beloved of textbooks, '
        'would never fall for a sale sign or splurge on lottery tickets. '
        'Real humans, alas, do both with alarming regularity. '
        'Policymakers ought to take note."'
    ),
    "Yuval Noah Harari": (
        '"People often make irrational financial decisions."',
        '"For 200,000 years, Homo sapiens made decisions that served '
        'survival on the African savanna. Then, about 500 years ago, '
        'we invented financial markets. Our brains never got the update. '
        'This is one of history\'s great ironies: the species that '
        'conquered the world cannot conquer its own impulses."'
    ),
    "Steven Pinker": (
        '"People often make irrational financial decisions."',
        '"The data on financial decision-making reveal a consistent pattern: '
        'humans deviate from optimal choice theory in predictable ways. '
        'Yet contrary to popular belief, these biases have declined '
        'significantly since the 1970s, particularly among educated populations. '
        'The reason is not hard to find: financial literacy programs work."'
    ),
    "Nassim Taleb": (
        '"People often make irrational financial decisions."',
        '"\'Irrational\'—the favorite word of Intellectuals Yet Idiots who '
        'have never traded a single option. These decisions look irrational '
        'only if you ignore fat tails. In the real world, the \"irrational\" '
        'person who keeps cash under the mattress survives. '
        'The \"rational\" one blows up. Skin in the game, or silence."'
    ),
    "Donald Trump": (
        '"People often make irrational financial decisions."',
        '"People are making terrible deals. Terrible. The worst deals. '
        'I\'ve seen it. Believe me. Nobody knows deals like I do. '
        'I wrote The Art of the Deal. Best-selling book. Huge. '
        'These people, they don\'t know what they\'re doing. Sad!"'
    ),
    "Daron Acemoglu": (
        '"People often make irrational financial decisions."',
        '"The historical evidence suggests that individual financial behavior '
        'is shaped by institutional context. In societies with extractive '
        'financial institutions, short-term decision-making is a rational '
        'response to uncertainty. Inclusive institutions, by contrast, '
        'create the conditions for long-term planning. This pattern is '
        'consistent with cross-country evidence on savings rates and '
        'financial development."'
    ),
}


def derive_vocabulary(style: StyleParameters, doc_type: DocumentType8D) -> VocabularyGuide:
    """
    Derive vocabulary constraints from style parameters.
    Implements: V = v(σ) where v: Σ → V
    """
    guide = VocabularyGuide(
        hedging_words=[],
        booster_words=[],
        connectives=[],
        forbidden_words=[],
        technical_terms_level="basic",
        example_phrases=[]
    )

    # Hedging words
    if style.hedging_required:
        guide.hedging_words = HEDGING_WORDS.copy()

    # Booster words
    if style.boosters_allowed:
        guide.booster_words = BOOSTER_WORDS.copy()
    else:
        guide.forbidden_words.extend(BOOSTER_WORDS[:5])  # Forbid strongest boosters

    # Connectives based on tone
    if style.tone in ["academic", "formal"]:
        guide.connectives = FORMAL_CONNECTIVES.copy()
        guide.forbidden_words.extend(CASUAL_CONNECTIVES)
    else:
        guide.connectives = CASUAL_CONNECTIVES.copy()

    # Technical terms level
    if doc_type.D1_expertise > 0.85:
        guide.technical_terms_level = "expert"
    elif doc_type.D1_expertise > 0.65:
        guide.technical_terms_level = "advanced"
    elif doc_type.D1_expertise > 0.40:
        guide.technical_terms_level = "intermediate"
    else:
        guide.technical_terms_level = "basic"

    # Example phrases
    if style.narrative_elements:
        guide.example_phrases = NARRATIVE_PHRASES.copy()
    elif style.tone == "academic":
        guide.example_phrases = ACADEMIC_PHRASES.copy()

    return guide


# =============================================================================
# PROMPT GENERATION
# =============================================================================

def generate_llm_prompt(
    doc_type: DocumentType8D,
    author_name: Optional[str] = None,
    description: Optional[str] = None,
    language: str = "en"
) -> str:
    """
    Generate a complete LLM system prompt from an 8D document type profile.

    This implements the full emergence chain:
    8D → Structure (implicit)
    8D → Style → Vocabulary → LLM Instructions
    """
    style = derive_style(doc_type)
    vocab = derive_vocabulary(style, doc_type)

    # Build the prompt
    lines = []

    # Header
    if author_name:
        lines.append(f"# SYSTEM PROMPT: Write in the style of {author_name}")
    else:
        lines.append(f"# SYSTEM PROMPT: Custom Document Style")

    if description:
        lines.append(f"# Style: {description}")
    lines.append("")

    # 8D Profile Summary
    lines.append("## 8D PROFILE")
    lines.append(f"- D1 Expertise:    {doc_type.D1_expertise:.2f} → {_level_desc(doc_type.D1_expertise, 'expertise')}")
    lines.append(f"- D2 Formality:    {doc_type.D2_formality:.2f} → {_level_desc(doc_type.D2_formality, 'formality')}")
    lines.append(f"- D3 Emotional:    {doc_type.D3_emotional:.2f} → {_level_desc(doc_type.D3_emotional, 'emotional')}")
    lines.append(f"- D4 Complexity:   {doc_type.D4_complexity:.2f} → {_level_desc(doc_type.D4_complexity, 'complexity')}")
    lines.append(f"- D5 Temporal:     {doc_type.D5_temporal:.2f} → {_level_desc(doc_type.D5_temporal, 'temporal')}")
    lines.append(f"- D6 Evidence:     {doc_type.D6_evidence:.2f} → {_level_desc(doc_type.D6_evidence, 'evidence')}")
    lines.append(f"- D7 Narrative:    {doc_type.D7_narrative:.2f} → {_level_desc(doc_type.D7_narrative, 'narrative')}")
    lines.append(f"- D8 Precision:    {doc_type.D8_precision:.2f} → {_level_desc(doc_type.D8_precision, 'precision')}")
    lines.append("")

    # Writing Instructions
    lines.append("## WRITING INSTRUCTIONS")
    lines.append("")

    # Sentence Structure
    lines.append("### Sentence Structure")
    min_len, max_len = style.sentence_length_range
    lines.append(f"- Target sentence length: {min_len}-{max_len} words")
    lines.append(f"- Clause complexity: {style.clause_complexity}")
    lines.append(f"- {'USE' if style.narrative_elements else 'AVOID'} narrative elements and anecdotes")
    lines.append("")

    # Tone & Voice
    lines.append("### Tone & Voice")
    lines.append(f"- Overall tone: {style.tone.upper()}")
    pronoun_map = {
        "first_plural": 'Use "we/our" (academic collaborative voice)',
        "first_singular": 'Use "I/my" (personal voice)',
        "third": 'Use third person ("the author", "one")',
        "impersonal": 'Use impersonal constructions ("it is noted that...")'
    }
    lines.append(f"- {pronoun_map[style.pronoun_style]}")
    lines.append("")

    # Vocabulary
    lines.append("### Vocabulary")
    lines.append(f"- Technical terms: {vocab.technical_terms_level} level")

    if vocab.hedging_words:
        lines.append(f"- USE hedging words: {', '.join(vocab.hedging_words[:7])}...")
    else:
        lines.append("- Hedging: not required (can make direct claims)")

    if vocab.booster_words:
        lines.append(f"- Boosters allowed: {', '.join(vocab.booster_words[:5])}...")
    else:
        lines.append("- AVOID boosters and emphatic language")

    if vocab.connectives:
        lines.append(f"- Preferred connectives: {', '.join(vocab.connectives[:6])}...")

    if vocab.forbidden_words:
        lines.append(f"- FORBIDDEN words: {', '.join(vocab.forbidden_words[:8])}...")
    lines.append("")

    # Evidence & Citations
    lines.append("### Evidence & Citations")
    citation_desc = {
        "academic": "Full academic citations (Author, Year) with bibliography",
        "inline": "Inline references to sources and studies",
        "footnote": "Footnote-style references where appropriate",
        "none": "No formal citations required"
    }
    lines.append(f"- {citation_desc[style.citation_style]}")

    evidence_level = "required" if doc_type.D6_evidence > 0.7 else "encouraged" if doc_type.D6_evidence > 0.4 else "optional"
    lines.append(f"- Empirical evidence: {evidence_level}")
    lines.append("")

    # Example Phrases (author-specific override)
    example_phrases = vocab.example_phrases
    author_phrase_map = {
        "Reinhard Sprenger": SPRENGER_PHRASES,
        "The Economist": ECONOMIST_PHRASES,
        "Yuval Noah Harari": HARARI_PHRASES,
        "Steven Pinker": PINKER_PHRASES,
        "Nassim Taleb": TALEB_PHRASES,
        "Donald Trump": TRUMP_PHRASES,
        "Daron Acemoglu": ACEMOGLU_PHRASES,
    }
    if author_name in author_phrase_map:
        example_phrases = author_phrase_map[author_name]

    if example_phrases:
        lines.append("### Example Phrases to Use")
        for phrase in example_phrases[:6]:
            lines.append(f'- "{phrase}"')
        lines.append("")

    # Transformation Example
    lines.append("## EXAMPLE TRANSFORMATION")
    lines.append("")
    lines.append("Input (neutral):")
    lines.append('> "People often make irrational financial decisions."')
    lines.append("")
    lines.append(f"Output ({author_name or 'this style'}):")

    # Check for author-specific transformation first
    if author_name and author_name in AUTHOR_TRANSFORMATIONS:
        _, transformation = AUTHOR_TRANSFORMATIONS[author_name]
        lines.append(f"> {transformation}")
    # Generate style-appropriate transformation
    elif style.tone == "academic" and style.hedging_required:
        lines.append('> "Empirical evidence suggests that individuals may systematically deviate from rational choice predictions in financial decision-making contexts, consistent with behavioral economic theory."')
    elif style.tone == "academic":
        lines.append('> "Research demonstrates systematic deviations from rational choice predictions in financial decision-making, consistent with behavioral economic frameworks."')
    elif style.narrative_elements:
        lines.append('> "Imagine this: you\'re standing in the checkout line, and suddenly that chocolate bar seems irresistible. That\'s your brain making decisions that economists would call \'irrational.\'"')
    elif style.tone == "formal":
        lines.append('> "Analysis indicates that financial decision-making frequently deviates from rational choice models, suggesting the influence of behavioral factors."')
    else:
        lines.append('> "Turns out, we\'re not as rational with money as we\'d like to think. Our brains have some quirky shortcuts that lead us astray."')

    lines.append("")
    lines.append("---")
    lines.append(f"Generated by EBF 8D Document Type Framework")
    lines.append(f"Based on Appendices CCC (METHOD-DOCTYPE) and DDD (REF-DOCTYPE)")

    return "\n".join(lines)


def _level_desc(value: float, dimension: str) -> str:
    """Generate human-readable description for dimension value."""
    descriptions = {
        "expertise": {0.2: "layperson", 0.4: "informed", 0.6: "advanced", 0.8: "expert", 1.0: "specialist"},
        "formality": {0.2: "casual", 0.4: "conversational", 0.6: "professional", 0.8: "formal", 1.0: "academic"},
        "emotional": {0.2: "detached", 0.4: "neutral", 0.6: "engaged", 0.8: "expressive", 1.0: "passionate"},
        "complexity": {0.2: "simple", 0.4: "straightforward", 0.6: "moderate", 0.8: "complex", 1.0: "highly complex"},
        "temporal": {0.2: "timeless", 0.4: "background", 0.6: "contextual", 0.8: "contemporary", 1.0: "breaking"},
        "evidence": {0.2: "opinion-based", 0.4: "anecdotal", 0.6: "referenced", 0.8: "evidence-based", 1.0: "rigorous"},
        "narrative": {0.2: "analytical", 0.4: "expository", 0.6: "mixed", 0.8: "narrative", 1.0: "storytelling"},
        "precision": {0.2: "approximate", 0.4: "general", 0.6: "specific", 0.8: "precise", 1.0: "exacting"}
    }

    for threshold, desc in sorted(descriptions.get(dimension, {}).items()):
        if value <= threshold:
            return desc
    return "maximum"


# =============================================================================
# CLI INTERFACE
# =============================================================================

def list_authors():
    """Print all available predefined author profiles."""
    print("\n=== Available Author Profiles ===\n")
    for name, (profile, desc, lang) in AUTHOR_PROFILES.items():
        print(f"  {name}")
        print(f"    Description: {desc}")
        print(f"    Language: {lang}")
        print(f"    8D: ({profile.D1_expertise:.2f}, {profile.D2_formality:.2f}, "
              f"{profile.D3_emotional:.2f}, {profile.D4_complexity:.2f}, "
              f"{profile.D5_temporal:.2f}, {profile.D6_evidence:.2f}, "
              f"{profile.D7_narrative:.2f}, {profile.D8_precision:.2f})")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate LLM system prompts from 8D document type profiles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_style_prompt.py --author "Ernst Fehr"
  python generate_style_prompt.py --author "NYT Opinion"
  python generate_style_prompt.py --profile 0.9,0.85,0.15,0.6,0.5,0.85,0.25,0.95
  python generate_style_prompt.py --list-authors
        """
    )

    parser.add_argument(
        "--author", "-a",
        help="Use a predefined author profile"
    )

    parser.add_argument(
        "--profile", "-p",
        help="Custom 8D profile as comma-separated values (D1,D2,...,D8)"
    )

    parser.add_argument(
        "--description", "-d",
        help="Description for custom profile"
    )

    parser.add_argument(
        "--language", "-l",
        default="en",
        help="Language code (default: en)"
    )

    parser.add_argument(
        "--list-authors",
        action="store_true",
        help="List all available predefined author profiles"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    if args.list_authors:
        list_authors()
        return

    if args.author:
        if args.author not in AUTHOR_PROFILES:
            print(f"Error: Unknown author '{args.author}'")
            print("Use --list-authors to see available profiles")
            return 1

        profile, desc, lang = AUTHOR_PROFILES[args.author]
        prompt = generate_llm_prompt(profile, args.author, desc, lang)

    elif args.profile:
        try:
            values = tuple(float(v.strip()) for v in args.profile.split(","))
            profile = DocumentType8D.from_tuple(values)
            prompt = generate_llm_prompt(
                profile,
                description=args.description or "Custom 8D profile",
                language=args.language
            )
        except (ValueError, TypeError) as e:
            print(f"Error parsing profile: {e}")
            return 1
    else:
        parser.print_help()
        return 1

    if args.output:
        with open(args.output, "w") as f:
            f.write(prompt)
        print(f"Prompt written to {args.output}")
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    exit(main() or 0)
