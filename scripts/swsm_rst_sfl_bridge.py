#!/usr/bin/env python3
"""
SWSM RST-SFL Bridge (E4)
========================

Bidirectional bridge between Rhetorical Structure Theory (RST) discourse
relations and Systemic Functional Linguistics (SFL) metafunctions.

Theoretical Foundation:
- RST operates at L3-L4 (MESO-MIKRO) - discourse relations between spans
- SFL operates at L5-L6 (SATZ-KLAUSEL) - clause-level linguistic realizations
- The bridge maps how discourse relations are REALIZED through clause choices

Key Insight (SWSM Axiom 7 - Realizational Stratification):
  "Higher strata are REALIZED BY lower strata"
  RST relations → realized by → SFL clause complexes

References:
- Mann & Thompson (1988): Rhetorical Structure Theory
- Halliday & Matthiessen (2014): Introduction to Functional Grammar
- Martin (1992): English Text - System and Structure
- Taboada & Mann (2006): Rhetorical Structure Theory

Author: SWSM Framework / EBF
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
import json


# =============================================================================
# RST RELATION TAXONOMY
# =============================================================================

class RSTRelationType(Enum):
    """RST relation types following Mann & Thompson (1988) + extensions."""

    # Subject Matter Relations (Ideational)
    CAUSE = "cause"
    RESULT = "result"
    PURPOSE = "purpose"
    CONDITION = "condition"
    OTHERWISE = "otherwise"
    INTERPRETATION = "interpretation"
    EVALUATION = "evaluation"
    CIRCUMSTANCE = "circumstance"
    MEANS = "means"
    SOLUTIONHOOD = "solutionhood"

    # Presentational Relations (Interpersonal)
    MOTIVATION = "motivation"
    ANTITHESIS = "antithesis"
    BACKGROUND = "background"
    ENABLEMENT = "enablement"
    EVIDENCE = "evidence"
    JUSTIFY = "justify"
    CONCESSION = "concession"

    # Multinuclear Relations
    CONTRAST = "contrast"
    SEQUENCE = "sequence"
    JOINT = "joint"
    LIST = "list"
    RESTATEMENT = "restatement"

    # Textual Relations
    ELABORATION = "elaboration"
    SUMMARY = "summary"
    PREPARATION = "preparation"

    # Academic Extensions (Swales/Bhatia)
    MOVE_TERRITORY = "move_territory"      # CARS Move 1
    MOVE_NICHE = "move_niche"              # CARS Move 2
    MOVE_OCCUPY = "move_occupy"            # CARS Move 3


class RSTNuclearity(Enum):
    """Nuclearity status in RST."""
    NUCLEUS = "nucleus"
    SATELLITE = "satellite"
    MULTINUCLEAR = "multinuclear"


@dataclass
class RSTRelation:
    """Represents an RST relation between text spans."""
    relation_type: RSTRelationType
    nucleus_span: Tuple[int, int]  # (start, end) character positions
    satellite_span: Optional[Tuple[int, int]] = None
    nuclearity: RSTNuclearity = RSTNuclearity.NUCLEUS
    confidence: float = 1.0

    def is_multinuclear(self) -> bool:
        return self.nuclearity == RSTNuclearity.MULTINUCLEAR


# =============================================================================
# SFL REALIZATION PATTERNS
# =============================================================================

@dataclass
class IdeationalRealization:
    """How RST relations realize through Ideational metafunction."""

    # Logical (clause complex) patterns
    taxis: str  # "paratactic" | "hypotactic"
    logico_semantic: str  # "expansion" | "projection"
    expansion_type: Optional[str] = None  # "elaboration" | "extension" | "enhancement"
    enhancement_type: Optional[str] = None  # "temporal" | "causal" | "conditional" | "manner"

    # Experiential (transitivity) patterns
    typical_process_types: List[str] = field(default_factory=list)
    participant_roles: List[str] = field(default_factory=list)
    circumstance_types: List[str] = field(default_factory=list)

    # Conjunctions that signal this relation
    conjunctions: Dict[str, List[str]] = field(default_factory=dict)  # lang -> conjunctions


@dataclass
class InterpersonalRealization:
    """How RST relations realize through Interpersonal metafunction."""

    # Mood patterns
    typical_mood: str  # "declarative" | "interrogative" | "imperative"
    modality_type: Optional[str] = None  # "epistemic" | "deontic"
    modality_value: Optional[str] = None  # "high" | "median" | "low"
    polarity_pattern: str = "positive"  # "positive" | "negative" | "both"

    # Speech function
    speech_function: str  # "statement" | "question" | "command" | "offer"

    # Appraisal patterns (Martin & White 2005)
    attitude_type: Optional[str] = None  # "affect" | "judgement" | "appreciation"
    engagement_type: Optional[str] = None  # "monogloss" | "heterogloss"
    graduation: Optional[str] = None  # "force" | "focus"


@dataclass
class TextualRealization:
    """How RST relations realize through Textual metafunction."""

    # Theme-Rheme patterns
    theme_type: str  # "topical" | "textual" | "interpersonal" | "multiple"
    marked_theme: bool = False
    thematic_progression: str = "constant"  # "constant" | "linear" | "derived" | "split"

    # Information structure
    information_unit: str = "unmarked"  # "unmarked" | "marked"
    given_new_pattern: str = "given_new"  # "given_new" | "new_given" | "all_new"

    # Cohesion
    reference_type: Optional[str] = None  # "anaphoric" | "cataphoric" | "exophoric"
    conjunction_type: Optional[str] = None  # "additive" | "adversative" | "causal" | "temporal"
    lexical_cohesion: Optional[str] = None  # "repetition" | "synonym" | "hyponym" | "meronym"


@dataclass
class RSTSFLMapping:
    """Complete mapping from RST relation to SFL realizations."""
    rst_relation: RSTRelationType
    ideational: IdeationalRealization
    interpersonal: InterpersonalRealization
    textual: TextualRealization

    # Constraints for generation
    obligatory_features: List[str] = field(default_factory=list)
    optional_features: List[str] = field(default_factory=list)
    incompatible_features: List[str] = field(default_factory=list)


# =============================================================================
# RST-SFL BRIDGE MAPPINGS
# =============================================================================

RST_SFL_MAPPINGS: Dict[RSTRelationType, RSTSFLMapping] = {

    # =========================================================================
    # CAUSE-EFFECT RELATIONS (Ideational: Enhancement - Causal)
    # =========================================================================

    RSTRelationType.CAUSE: RSTSFLMapping(
        rst_relation=RSTRelationType.CAUSE,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="enhancement",
            enhancement_type="causal",
            typical_process_types=["material", "relational"],
            participant_roles=["Actor", "Goal", "Carrier", "Attribute"],
            circumstance_types=["cause", "reason"],
            conjunctions={
                "en": ["because", "since", "as", "for", "due to", "owing to"],
                "de": ["weil", "da", "denn", "aufgrund", "wegen"],
                "fr": ["parce que", "car", "puisque", "vu que"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="high",
            speech_function="statement",
            engagement_type="monogloss"
        ),
        textual=TextualRealization(
            theme_type="textual",
            thematic_progression="linear",
            conjunction_type="causal",
            reference_type="anaphoric"
        ),
        obligatory_features=["causal_conjunction", "clause_complex"],
        optional_features=["temporal_sequence", "epistemic_modality"]
    ),

    RSTRelationType.RESULT: RSTSFLMapping(
        rst_relation=RSTRelationType.RESULT,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="enhancement",
            enhancement_type="causal",
            typical_process_types=["material", "relational"],
            participant_roles=["Goal", "Carrier", "Attribute"],
            circumstance_types=["result", "consequence"],
            conjunctions={
                "en": ["so", "therefore", "thus", "hence", "consequently", "as a result"],
                "de": ["also", "daher", "deshalb", "folglich", "somit", "infolgedessen"],
                "fr": ["donc", "ainsi", "par conséquent", "c'est pourquoi"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="median",
            speech_function="statement",
            engagement_type="monogloss"
        ),
        textual=TextualRealization(
            theme_type="textual",
            thematic_progression="linear",
            conjunction_type="causal",
            given_new_pattern="given_new"
        ),
        obligatory_features=["result_conjunction"],
        optional_features=["quantification", "temporal_marker"]
    ),

    RSTRelationType.PURPOSE: RSTSFLMapping(
        rst_relation=RSTRelationType.PURPOSE,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="enhancement",
            enhancement_type="causal",
            typical_process_types=["material", "mental"],
            participant_roles=["Actor", "Goal", "Beneficiary"],
            circumstance_types=["purpose", "behalf"],
            conjunctions={
                "en": ["to", "in order to", "so that", "so as to", "for the purpose of"],
                "de": ["um zu", "damit", "zwecks", "zum Zweck"],
                "fr": ["pour", "afin de", "dans le but de", "en vue de"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="deontic",
            modality_value="median",
            speech_function="statement",
            attitude_type="judgement"
        ),
        textual=TextualRealization(
            theme_type="topical",
            thematic_progression="constant",
            reference_type="cataphoric"
        ),
        obligatory_features=["purpose_conjunction", "non_finite_clause"],
        optional_features=["beneficiary", "goal_specification"]
    ),

    # =========================================================================
    # CONDITIONAL RELATIONS (Ideational: Enhancement - Conditional)
    # =========================================================================

    RSTRelationType.CONDITION: RSTSFLMapping(
        rst_relation=RSTRelationType.CONDITION,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="enhancement",
            enhancement_type="conditional",
            typical_process_types=["relational", "material"],
            participant_roles=["Carrier", "Attribute", "Actor"],
            circumstance_types=["condition", "contingency"],
            conjunctions={
                "en": ["if", "unless", "provided that", "in case", "assuming"],
                "de": ["wenn", "falls", "sofern", "vorausgesetzt", "angenommen"],
                "fr": ["si", "à condition que", "pourvu que", "en cas de"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="low",
            polarity_pattern="both",
            speech_function="statement",
            engagement_type="heterogloss"
        ),
        textual=TextualRealization(
            theme_type="textual",
            marked_theme=True,
            thematic_progression="derived",
            conjunction_type="causal"
        ),
        obligatory_features=["conditional_conjunction", "hypothetical_modality"],
        optional_features=["counterfactual", "temporal_contingency"]
    ),

    # =========================================================================
    # ELABORATION RELATIONS (Ideational: Elaboration)
    # =========================================================================

    RSTRelationType.ELABORATION: RSTSFLMapping(
        rst_relation=RSTRelationType.ELABORATION,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="elaboration",
            typical_process_types=["relational", "existential"],
            participant_roles=["Carrier", "Attribute", "Identifier", "Identified"],
            circumstance_types=["manner", "location"],
            conjunctions={
                "en": ["that is", "namely", "specifically", "in particular", "for example"],
                "de": ["das heisst", "nämlich", "insbesondere", "zum Beispiel"],
                "fr": ["c'est-à-dire", "notamment", "en particulier", "par exemple"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="high",
            speech_function="statement",
            engagement_type="monogloss"
        ),
        textual=TextualRealization(
            theme_type="topical",
            thematic_progression="constant",
            reference_type="anaphoric",
            lexical_cohesion="hyponym"
        ),
        obligatory_features=["coreference", "specification"],
        optional_features=["exemplification", "particularization"]
    ),

    # =========================================================================
    # CONTRAST RELATIONS (Ideational: Extension - Adversative)
    # =========================================================================

    RSTRelationType.CONTRAST: RSTSFLMapping(
        rst_relation=RSTRelationType.CONTRAST,
        ideational=IdeationalRealization(
            taxis="paratactic",
            logico_semantic="expansion",
            expansion_type="extension",
            typical_process_types=["relational", "material"],
            participant_roles=["Carrier", "Attribute"],
            circumstance_types=["comparison"],
            conjunctions={
                "en": ["but", "however", "whereas", "while", "in contrast", "on the other hand"],
                "de": ["aber", "jedoch", "während", "hingegen", "im Gegensatz"],
                "fr": ["mais", "cependant", "tandis que", "en revanche", "par contre"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            speech_function="statement",
            engagement_type="heterogloss",
            attitude_type="appreciation"
        ),
        textual=TextualRealization(
            theme_type="textual",
            marked_theme=True,
            thematic_progression="split",
            conjunction_type="adversative",
            given_new_pattern="new_given"
        ),
        obligatory_features=["adversative_conjunction", "parallel_structure"],
        optional_features=["antonymy", "negation"]
    ),

    RSTRelationType.CONCESSION: RSTSFLMapping(
        rst_relation=RSTRelationType.CONCESSION,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="extension",
            typical_process_types=["relational", "mental"],
            participant_roles=["Carrier", "Attribute", "Senser"],
            circumstance_types=["concession"],
            conjunctions={
                "en": ["although", "though", "even though", "despite", "nevertheless"],
                "de": ["obwohl", "obgleich", "trotzdem", "dennoch", "gleichwohl"],
                "fr": ["bien que", "quoique", "malgré", "néanmoins", "toutefois"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="median",
            speech_function="statement",
            engagement_type="heterogloss"
        ),
        textual=TextualRealization(
            theme_type="textual",
            marked_theme=True,
            thematic_progression="linear",
            conjunction_type="adversative"
        ),
        obligatory_features=["concessive_conjunction"],
        optional_features=["counter_expectation", "mitigation"]
    ),

    # =========================================================================
    # EVIDENCE & JUSTIFICATION (Interpersonal Focus)
    # =========================================================================

    RSTRelationType.EVIDENCE: RSTSFLMapping(
        rst_relation=RSTRelationType.EVIDENCE,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="projection",
            typical_process_types=["verbal", "mental", "relational"],
            participant_roles=["Sayer", "Verbiage", "Senser", "Phenomenon"],
            circumstance_types=["source", "manner"],
            conjunctions={
                "en": ["according to", "as shown by", "as demonstrated"],
                "de": ["laut", "gemäss", "wie gezeigt", "wie nachgewiesen"],
                "fr": ["selon", "d'après", "comme le montre", "tel que démontré"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="high",
            speech_function="statement",
            engagement_type="heterogloss",
            attitude_type="judgement"
        ),
        textual=TextualRealization(
            theme_type="interpersonal",
            thematic_progression="linear",
            reference_type="exophoric"
        ),
        obligatory_features=["source_attribution", "evidential_marker"],
        optional_features=["quantification", "citation"]
    ),

    RSTRelationType.JUSTIFY: RSTSFLMapping(
        rst_relation=RSTRelationType.JUSTIFY,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="enhancement",
            enhancement_type="causal",
            typical_process_types=["relational", "mental"],
            participant_roles=["Carrier", "Attribute", "Senser", "Phenomenon"],
            circumstance_types=["reason", "cause"],
            conjunctions={
                "en": ["because", "since", "given that", "considering"],
                "de": ["weil", "da", "angesichts", "in Anbetracht"],
                "fr": ["car", "étant donné que", "compte tenu de"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="deontic",
            modality_value="median",
            speech_function="statement",
            attitude_type="judgement",
            engagement_type="heterogloss"
        ),
        textual=TextualRealization(
            theme_type="textual",
            thematic_progression="linear",
            conjunction_type="causal"
        ),
        obligatory_features=["reasoning_chain"],
        optional_features=["authority_appeal", "logical_connector"]
    ),

    # =========================================================================
    # SEQUENCE & TEMPORAL (Ideational: Enhancement - Temporal)
    # =========================================================================

    RSTRelationType.SEQUENCE: RSTSFLMapping(
        rst_relation=RSTRelationType.SEQUENCE,
        ideational=IdeationalRealization(
            taxis="paratactic",
            logico_semantic="expansion",
            expansion_type="enhancement",
            enhancement_type="temporal",
            typical_process_types=["material"],
            participant_roles=["Actor", "Goal", "Scope"],
            circumstance_types=["temporal", "location"],
            conjunctions={
                "en": ["then", "next", "after", "subsequently", "finally", "first", "second"],
                "de": ["dann", "danach", "anschliessend", "schliesslich", "erstens", "zweitens"],
                "fr": ["puis", "ensuite", "après", "finalement", "premièrement", "deuxièmement"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            speech_function="statement",
            engagement_type="monogloss"
        ),
        textual=TextualRealization(
            theme_type="textual",
            thematic_progression="linear",
            conjunction_type="temporal",
            given_new_pattern="given_new"
        ),
        obligatory_features=["temporal_sequence_marker"],
        optional_features=["enumeration", "procedural_marker"]
    ),

    # =========================================================================
    # BACKGROUND & PREPARATION (Textual Focus)
    # =========================================================================

    RSTRelationType.BACKGROUND: RSTSFLMapping(
        rst_relation=RSTRelationType.BACKGROUND,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="elaboration",
            typical_process_types=["relational", "existential"],
            participant_roles=["Carrier", "Attribute", "Existent"],
            circumstance_types=["location", "temporal"],
            conjunctions={
                "en": ["previously", "historically", "traditionally"],
                "de": ["zuvor", "historisch", "traditionell"],
                "fr": ["auparavant", "historiquement", "traditionnellement"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="high",
            speech_function="statement",
            engagement_type="monogloss"
        ),
        textual=TextualRealization(
            theme_type="topical",
            marked_theme=False,
            thematic_progression="constant",
            information_unit="unmarked",
            given_new_pattern="all_new"
        ),
        obligatory_features=["scene_setting"],
        optional_features=["temporal_frame", "spatial_frame"]
    ),

    RSTRelationType.PREPARATION: RSTSFLMapping(
        rst_relation=RSTRelationType.PREPARATION,
        ideational=IdeationalRealization(
            taxis="paratactic",
            logico_semantic="expansion",
            expansion_type="elaboration",
            typical_process_types=["verbal", "mental"],
            participant_roles=["Sayer", "Target"],
            circumstance_types=["matter"],
            conjunctions={
                "en": ["regarding", "concerning", "as for", "with respect to"],
                "de": ["bezüglich", "hinsichtlich", "was ... betrifft"],
                "fr": ["concernant", "quant à", "en ce qui concerne"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            speech_function="statement",
            engagement_type="monogloss"
        ),
        textual=TextualRealization(
            theme_type="textual",
            marked_theme=True,
            thematic_progression="derived",
            reference_type="cataphoric"
        ),
        obligatory_features=["topic_introduction"],
        optional_features=["scope_limitation", "focus_marker"]
    ),

    # =========================================================================
    # ACADEMIC GENRE MOVES (CARS Model Integration)
    # =========================================================================

    RSTRelationType.MOVE_TERRITORY: RSTSFLMapping(
        rst_relation=RSTRelationType.MOVE_TERRITORY,
        ideational=IdeationalRealization(
            taxis="paratactic",
            logico_semantic="expansion",
            expansion_type="elaboration",
            typical_process_types=["relational", "existential", "material"],
            participant_roles=["Carrier", "Attribute", "Existent"],
            circumstance_types=["location", "extent"],
            conjunctions={
                "en": ["increasingly", "widely", "generally", "traditionally"],
                "de": ["zunehmend", "weitgehend", "allgemein", "traditionell"],
                "fr": ["de plus en plus", "largement", "généralement", "traditionnellement"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="high",
            speech_function="statement",
            engagement_type="heterogloss",
            attitude_type="appreciation"
        ),
        textual=TextualRealization(
            theme_type="topical",
            thematic_progression="constant",
            lexical_cohesion="hyponym"
        ),
        obligatory_features=["field_establishment", "importance_claim"],
        optional_features=["citation_density_high", "generalization"]
    ),

    RSTRelationType.MOVE_NICHE: RSTSFLMapping(
        rst_relation=RSTRelationType.MOVE_NICHE,
        ideational=IdeationalRealization(
            taxis="hypotactic",
            logico_semantic="expansion",
            expansion_type="extension",
            typical_process_types=["relational", "mental", "verbal"],
            participant_roles=["Carrier", "Attribute", "Senser"],
            circumstance_types=["manner", "extent"],
            conjunctions={
                "en": ["however", "yet", "although", "despite", "nevertheless"],
                "de": ["jedoch", "dennoch", "obwohl", "trotz", "gleichwohl"],
                "fr": ["cependant", "néanmoins", "bien que", "malgré"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="epistemic",
            modality_value="median",
            polarity_pattern="negative",
            speech_function="statement",
            engagement_type="heterogloss",
            attitude_type="judgement"
        ),
        textual=TextualRealization(
            theme_type="textual",
            marked_theme=True,
            thematic_progression="linear",
            conjunction_type="adversative"
        ),
        obligatory_features=["gap_indication", "counter_claiming"],
        optional_features=["question_raising", "continuation_need"]
    ),

    RSTRelationType.MOVE_OCCUPY: RSTSFLMapping(
        rst_relation=RSTRelationType.MOVE_OCCUPY,
        ideational=IdeationalRealization(
            taxis="paratactic",
            logico_semantic="projection",
            typical_process_types=["verbal", "material", "mental"],
            participant_roles=["Sayer", "Verbiage", "Actor", "Goal"],
            circumstance_types=["purpose", "manner"],
            conjunctions={
                "en": ["this paper", "we argue", "this study", "the present research"],
                "de": ["dieser Beitrag", "wir argumentieren", "diese Studie"],
                "fr": ["cet article", "nous soutenons", "cette étude"]
            }
        ),
        interpersonal=InterpersonalRealization(
            typical_mood="declarative",
            modality_type="deontic",
            modality_value="high",
            speech_function="statement",
            engagement_type="monogloss",
            attitude_type="judgement"
        ),
        textual=TextualRealization(
            theme_type="topical",
            marked_theme=False,
            thematic_progression="constant",
            reference_type="cataphoric"
        ),
        obligatory_features=["purpose_statement", "contribution_claim"],
        optional_features=["methodology_preview", "structure_outline"]
    ),
}


# =============================================================================
# RST-SFL BRIDGE CLASS
# =============================================================================

class RSTSFLBridge:
    """
    Bidirectional bridge between RST and SFL.

    Supports:
    1. RST → SFL: Given RST relations, generate SFL realization constraints
    2. SFL → RST: Given SFL features, infer probable RST relations

    Implements SWSM Axiom 7 (Realizational Stratification).
    """

    def __init__(self, language: str = 'en'):
        """
        Initialize bridge.

        Args:
            language: Language code ('en', 'de', 'fr')
        """
        self.language = language
        self.mappings = RST_SFL_MAPPINGS

    # =========================================================================
    # RST → SFL (Generation Direction)
    # =========================================================================

    def rst_to_sfl(self, relation: RSTRelation) -> RSTSFLMapping:
        """
        Get SFL realization constraints for an RST relation.

        Args:
            relation: RST relation to realize

        Returns:
            Complete SFL realization mapping
        """
        if relation.relation_type in self.mappings:
            return self.mappings[relation.relation_type]
        else:
            # Return default elaboration mapping for unknown relations
            return self.mappings[RSTRelationType.ELABORATION]

    def get_conjunctions(self, relation_type: RSTRelationType) -> List[str]:
        """
        Get conjunctions for a relation in current language.

        Args:
            relation_type: RST relation type

        Returns:
            List of conjunctions
        """
        if relation_type in self.mappings:
            mapping = self.mappings[relation_type]
            return mapping.ideational.conjunctions.get(self.language, [])
        return []

    def get_clause_complex_pattern(self, relation_type: RSTRelationType) -> Dict[str, Any]:
        """
        Get clause complex construction pattern.

        Args:
            relation_type: RST relation type

        Returns:
            Pattern specification for clause complex
        """
        mapping = self.rst_to_sfl(RSTRelation(relation_type, (0, 0)))

        return {
            'taxis': mapping.ideational.taxis,
            'logico_semantic': mapping.ideational.logico_semantic,
            'expansion_type': mapping.ideational.expansion_type,
            'enhancement_type': mapping.ideational.enhancement_type,
            'conjunctions': mapping.ideational.conjunctions.get(self.language, []),
            'mood': mapping.interpersonal.typical_mood,
            'modality': {
                'type': mapping.interpersonal.modality_type,
                'value': mapping.interpersonal.modality_value
            },
            'theme': {
                'type': mapping.textual.theme_type,
                'marked': mapping.textual.marked_theme,
                'progression': mapping.textual.thematic_progression
            }
        }

    def get_generation_constraints(
        self,
        relation_type: RSTRelationType,
        include_optional: bool = False
    ) -> Dict[str, List[str]]:
        """
        Get constraints for text generation.

        Args:
            relation_type: RST relation to realize
            include_optional: Include optional features

        Returns:
            Dictionary of constraint categories
        """
        mapping = self.mappings.get(relation_type)
        if not mapping:
            return {'obligatory': [], 'optional': [], 'incompatible': []}

        result = {
            'obligatory': mapping.obligatory_features.copy(),
            'incompatible': mapping.incompatible_features.copy()
        }

        if include_optional:
            result['optional'] = mapping.optional_features.copy()

        return result

    # =========================================================================
    # SFL → RST (Analysis Direction)
    # =========================================================================

    def sfl_to_rst(
        self,
        conjunction: Optional[str] = None,
        taxis: Optional[str] = None,
        logico_semantic: Optional[str] = None,
        mood: Optional[str] = None,
        theme_marked: Optional[bool] = None,
        modality_type: Optional[str] = None
    ) -> List[Tuple[RSTRelationType, float]]:
        """
        Infer probable RST relations from SFL features.

        Args:
            conjunction: Observed conjunction
            taxis: Taxis type ('paratactic' | 'hypotactic')
            logico_semantic: Logico-semantic type
            mood: Mood type
            theme_marked: Whether theme is marked
            modality_type: Modality type

        Returns:
            List of (relation_type, probability) tuples, sorted by probability
        """
        scores: Dict[RSTRelationType, float] = {}

        for rel_type, mapping in self.mappings.items():
            score = 0.0
            matches = 0

            # Check conjunction match
            if conjunction:
                conjs = mapping.ideational.conjunctions.get(self.language, [])
                if any(c.lower() in conjunction.lower() for c in conjs):
                    score += 2.0
                    matches += 1

            # Check taxis match
            if taxis and mapping.ideational.taxis == taxis:
                score += 1.0
                matches += 1

            # Check logico-semantic match
            if logico_semantic and mapping.ideational.logico_semantic == logico_semantic:
                score += 1.0
                matches += 1

            # Check mood match
            if mood and mapping.interpersonal.typical_mood == mood:
                score += 0.5
                matches += 1

            # Check marked theme
            if theme_marked is not None and mapping.textual.marked_theme == theme_marked:
                score += 0.5
                matches += 1

            # Check modality
            if modality_type and mapping.interpersonal.modality_type == modality_type:
                score += 0.5
                matches += 1

            if matches > 0:
                scores[rel_type] = score / matches  # Normalize by matches

        # Convert to probabilities (softmax-like)
        if scores:
            total = sum(scores.values())
            probabilities = [(rel, score/total) for rel, score in scores.items()]
            return sorted(probabilities, key=lambda x: x[1], reverse=True)

        return [(RSTRelationType.ELABORATION, 1.0)]  # Default

    def infer_relation_from_conjunction(
        self,
        conjunction: str
    ) -> List[Tuple[RSTRelationType, float]]:
        """
        Infer RST relation from conjunction alone.

        Args:
            conjunction: The conjunction word/phrase

        Returns:
            List of (relation_type, probability) tuples
        """
        return self.sfl_to_rst(conjunction=conjunction)

    # =========================================================================
    # BATCH OPERATIONS
    # =========================================================================

    def analyze_clause_complex(
        self,
        clauses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Analyze a clause complex and infer RST relations.

        Args:
            clauses: List of clause annotations with SFL features

        Returns:
            List of inferred relations between clauses
        """
        relations = []

        for i in range(len(clauses) - 1):
            clause1 = clauses[i]
            clause2 = clauses[i + 1]

            # Extract features for inference
            conjunction = clause2.get('textual', {}).get('conjunction')
            taxis = clause2.get('logical', {}).get('taxis')

            # Infer relation
            inferred = self.sfl_to_rst(
                conjunction=conjunction,
                taxis=taxis,
                mood=clause2.get('interpersonal', {}).get('mood'),
                theme_marked=clause2.get('textual', {}).get('marked_theme')
            )

            if inferred:
                best_relation, confidence = inferred[0]
                relations.append({
                    'from_clause': i,
                    'to_clause': i + 1,
                    'relation': best_relation.value,
                    'confidence': confidence,
                    'alternatives': [(r.value, p) for r, p in inferred[1:3]]
                })

        return relations

    def generate_clause_complex_template(
        self,
        relation_sequence: List[RSTRelationType]
    ) -> List[Dict[str, Any]]:
        """
        Generate a template for a clause complex from RST relations.

        Args:
            relation_sequence: Sequence of RST relations

        Returns:
            List of clause templates with SFL constraints
        """
        templates = []

        # First clause (no incoming relation)
        templates.append({
            'position': 0,
            'constraints': {
                'theme': {'type': 'topical', 'marked': False},
                'mood': 'declarative'
            }
        })

        # Subsequent clauses based on relations
        for i, rel_type in enumerate(relation_sequence):
            pattern = self.get_clause_complex_pattern(rel_type)
            templates.append({
                'position': i + 1,
                'incoming_relation': rel_type.value,
                'constraints': {
                    'taxis': pattern['taxis'],
                    'conjunctions': pattern['conjunctions'],
                    'theme': pattern['theme'],
                    'mood': pattern['mood'],
                    'modality': pattern['modality']
                }
            })

        return templates

    # =========================================================================
    # EXPORT & SERIALIZATION
    # =========================================================================

    def export_mappings_yaml(self) -> str:
        """Export all mappings as YAML."""
        import yaml

        output = {'rst_sfl_mappings': {}}

        for rel_type, mapping in self.mappings.items():
            output['rst_sfl_mappings'][rel_type.value] = {
                'ideational': {
                    'taxis': mapping.ideational.taxis,
                    'logico_semantic': mapping.ideational.logico_semantic,
                    'expansion_type': mapping.ideational.expansion_type,
                    'enhancement_type': mapping.ideational.enhancement_type,
                    'conjunctions': mapping.ideational.conjunctions
                },
                'interpersonal': {
                    'mood': mapping.interpersonal.typical_mood,
                    'modality_type': mapping.interpersonal.modality_type,
                    'modality_value': mapping.interpersonal.modality_value,
                    'speech_function': mapping.interpersonal.speech_function
                },
                'textual': {
                    'theme_type': mapping.textual.theme_type,
                    'marked_theme': mapping.textual.marked_theme,
                    'thematic_progression': mapping.textual.thematic_progression,
                    'conjunction_type': mapping.textual.conjunction_type
                },
                'constraints': {
                    'obligatory': mapping.obligatory_features,
                    'optional': mapping.optional_features,
                    'incompatible': mapping.incompatible_features
                }
            }

        return yaml.dump(output, allow_unicode=True, default_flow_style=False)

    def to_json_ld(self) -> Dict[str, Any]:
        """Export as JSON-LD for interoperability."""
        return {
            "@context": {
                "swsm": "https://ebf.fehradvice.com/swsm/",
                "rst": "https://www.sfu.ca/rst/",
                "sfl": "https://www.isfla.org/",
                "language": "@language"
            },
            "@type": "swsm:RSTSFLBridge",
            "language": self.language,
            "mappings": [
                {
                    "@type": "swsm:RSTSFLMapping",
                    "rstRelation": rel_type.value,
                    "sflRealization": {
                        "ideational": {
                            "taxis": mapping.ideational.taxis,
                            "logicoSemantic": mapping.ideational.logico_semantic
                        },
                        "interpersonal": {
                            "mood": mapping.interpersonal.typical_mood,
                            "modalityType": mapping.interpersonal.modality_type
                        },
                        "textual": {
                            "themeType": mapping.textual.theme_type,
                            "markedTheme": mapping.textual.marked_theme
                        }
                    }
                }
                for rel_type, mapping in self.mappings.items()
            ]
        }


# =============================================================================
# INTEGRATION WITH SFL ANNOTATOR
# =============================================================================

class IntegratedAnalyzer:
    """
    Integrated analyzer combining SFL annotation with RST inference.

    Implements full SWSM analysis pipeline:
    L6 (Clause) → SFL Annotation → RST Inference → L3-L4 (Discourse)
    """

    def __init__(self, language: str = 'en'):
        """Initialize with SFL annotator and RST-SFL bridge."""
        self.language = language
        self.bridge = RSTSFLBridge(language)

        # Import SFL annotator if available
        try:
            from swsm_sfl_annotator import SFLAnnotator
            self.sfl_annotator = SFLAnnotator(language)
            self.sfl_available = True
        except ImportError:
            self.sfl_available = False

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Full SWSM analysis: SFL + RST.

        Args:
            text: Input text

        Returns:
            Complete analysis with both SFL and RST layers
        """
        result = {
            'text': text,
            'language': self.language,
            'analysis_layers': {}
        }

        # L6: SFL Clause Analysis
        if self.sfl_available:
            sfl_analysis = self.sfl_annotator.annotate_text(text)
            result['analysis_layers']['L6_clause_sfl'] = sfl_analysis

            # Extract clause data for RST inference
            clauses = []
            for clause_ann in sfl_analysis.get('clauses', []):
                clauses.append({
                    'textual': {
                        'conjunction': self._extract_conjunction(clause_ann),
                        'marked_theme': clause_ann.get('textual', {}).get('marked_theme', False)
                    },
                    'interpersonal': {
                        'mood': clause_ann.get('interpersonal', {}).get('mood_type')
                    },
                    'logical': {
                        'taxis': self._infer_taxis(clause_ann)
                    }
                })

            # L4: RST Relation Inference
            if len(clauses) > 1:
                rst_relations = self.bridge.analyze_clause_complex(clauses)
                result['analysis_layers']['L4_discourse_rst'] = rst_relations

        return result

    def _extract_conjunction(self, clause_ann: Dict) -> Optional[str]:
        """Extract conjunction from clause annotation."""
        textual = clause_ann.get('textual', {})
        theme_text = textual.get('theme', '')

        # Check for textual theme (conjunction)
        if textual.get('theme_type') == 'textual':
            return theme_text
        return None

    def _infer_taxis(self, clause_ann: Dict) -> str:
        """Infer taxis from clause features."""
        # Hypotactic if subordinate conjunction present
        textual = clause_ann.get('textual', {})
        if textual.get('theme_type') == 'textual':
            return 'hypotactic'
        return 'paratactic'


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """Command-line interface for RST-SFL Bridge."""
    import argparse

    parser = argparse.ArgumentParser(
        description='SWSM RST-SFL Bridge - Discourse-Clause Mapping'
    )
    parser.add_argument(
        '--language', '-l',
        default='en',
        choices=['en', 'de', 'fr'],
        help='Language for conjunctions'
    )
    parser.add_argument(
        '--relation', '-r',
        help='RST relation type to analyze'
    )
    parser.add_argument(
        '--conjunction', '-c',
        help='Conjunction to infer relation from'
    )
    parser.add_argument(
        '--export',
        choices=['yaml', 'json-ld'],
        help='Export all mappings'
    )
    parser.add_argument(
        '--list-relations',
        action='store_true',
        help='List all RST relation types'
    )

    args = parser.parse_args()
    bridge = RSTSFLBridge(args.language)

    if args.list_relations:
        print("RST Relation Types:")
        print("-" * 40)
        for rel_type in RSTRelationType:
            print(f"  {rel_type.value}")
        return

    if args.export == 'yaml':
        print(bridge.export_mappings_yaml())
        return

    if args.export == 'json-ld':
        print(json.dumps(bridge.to_json_ld(), indent=2))
        return

    if args.relation:
        try:
            rel_type = RSTRelationType(args.relation)
            pattern = bridge.get_clause_complex_pattern(rel_type)
            print(f"\nSFL Realization Pattern for '{args.relation}':")
            print("-" * 50)
            print(json.dumps(pattern, indent=2))
        except ValueError:
            print(f"Unknown relation type: {args.relation}")
            return

    if args.conjunction:
        inferred = bridge.infer_relation_from_conjunction(args.conjunction)
        print(f"\nInferred RST relations for '{args.conjunction}':")
        print("-" * 50)
        for rel_type, prob in inferred[:5]:
            print(f"  {rel_type.value}: {prob:.2%}")


if __name__ == '__main__':
    main()
