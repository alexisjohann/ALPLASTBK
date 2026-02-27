#!/usr/bin/env python3
"""
SWSM E3: CARS Move Tagger
=========================

Automatic move identification in academic and professional texts following
Swales (1990) CARS model and genre-specific move structures.

SWSM Axioms implemented:
- SWSM-8: Genre Emergence (8D → Genre → Moves)
- SWSM-9: Style Percolation (constraints propagate)
- SWSM-12: Domain Specialization (genres constrain moves)

Sources:
- Swales (1990): Genre Analysis - The CARS Model
- Bhatia (1993): Analysing Genre
- Hyland (2004): Disciplinary Discourses
- Kanoksilapatham (2005): Rhetorical moves in biochemistry research articles

Author: FehrAdvice & Partners AG
Version: 1.0.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any
import re
from collections import defaultdict


# =============================================================================
# ENUMS AND DATA STRUCTURES
# =============================================================================

class GenreType(Enum):
    """Supported genre types for move tagging."""
    SCIENTIFIC_PAPER = "scientific_paper"
    LITERATURE_REVIEW = "literature_review"
    THESIS = "thesis"
    POLICY_BRIEF = "policy_brief"
    EXECUTIVE_SUMMARY = "executive_summary"
    CONSULTING_MEMO = "consulting_memo"
    BUSINESS_REPORT = "business_report"
    BLOG_POST = "blog_post"
    WHITE_PAPER = "white_paper"
    EBF_APPENDIX = "ebf_appendix"
    EBF_CHAPTER = "ebf_chapter"


class MoveStatus(Enum):
    """Move obligation status."""
    OBLIGATORY = "obligatory"
    CONVENTIONAL = "conventional"
    OPTIONAL = "optional"


class SectionType(Enum):
    """Section types in documents."""
    ABSTRACT = "abstract"
    INTRODUCTION = "introduction"
    LITERATURE = "literature"
    METHODS = "methods"
    RESULTS = "results"
    DISCUSSION = "discussion"
    CONCLUSION = "conclusion"
    EXECUTIVE = "executive"
    PROBLEM = "problem"
    EVIDENCE = "evidence"
    RECOMMENDATION = "recommendation"
    UNKNOWN = "unknown"


@dataclass
class Strategy:
    """A strategy within a move."""
    strategy_id: str
    name: str
    description: str
    confidence: float = 0.0
    text_span: Tuple[int, int] = (0, 0)
    indicators: List[str] = field(default_factory=list)


@dataclass
class Move:
    """A rhetorical move in a document."""
    move_id: str
    name: str
    purpose: str
    status: MoveStatus
    section: SectionType
    strategies: List[Strategy] = field(default_factory=list)
    confidence: float = 0.0
    text_span: Tuple[int, int] = (0, 0)
    text: str = ""


@dataclass
class TaggedSection:
    """A section with identified moves."""
    section_id: str
    section_type: SectionType
    title: str
    moves: List[Move] = field(default_factory=list)
    text: str = ""
    position: str = "medial"  # initial, early, medial, late, final


@dataclass
class TaggedDocument:
    """A document with all moves tagged."""
    genre: GenreType
    sections: List[TaggedSection] = field(default_factory=list)
    move_coverage: float = 0.0
    obligatory_moves_found: int = 0
    obligatory_moves_expected: int = 0


# =============================================================================
# MOVE INDICATOR LEXICONS
# =============================================================================

class MoveIndicatorLexicon:
    """
    Lexicon of linguistic indicators for move identification.
    Based on corpus analysis of academic and professional texts.
    """

    # CARS Move 1: Establishing a Territory
    TERRITORY_INDICATORS = {
        'centrality_claiming': [
            r'\b(important|significant|essential|crucial|critical|vital|key|fundamental)\b',
            r'\b(increasing|growing|rising)\s+(interest|attention|concern)',
            r'\b(widely|generally|commonly|frequently)\s+(recognized|acknowledged|accepted)',
            r'\b(has\s+become|is\s+becoming)\s+(increasingly|more)',
            r'\b(plays?\s+a\s+(central|key|important|crucial)\s+role)',
        ],
        'topic_generalization': [
            r'\b(research\s+on|studies\s+(of|on)|work\s+on)\b',
            r'\b(the\s+field\s+of|the\s+area\s+of|the\s+domain\s+of)\b',
            r'\b(it\s+is\s+well\s+known|it\s+is\s+established)\b',
            r'\b(traditionally|historically|conventionally)\b',
            r'\b(in\s+recent\s+years|over\s+the\s+past|in\s+the\s+last)\b',
        ],
        'literature_review': [
            r'\b(previous\s+(research|studies|work)|prior\s+(research|studies))\b',
            r'\b(researchers\s+have|scholars\s+have|scientists\s+have)\b',
            r'\b(according\s+to|as\s+noted\s+by|as\s+shown\s+by)\b',
            r'\b(\w+\s+et\s+al\.|\w+\s+and\s+\w+\s*\(\d{4}\))\b',
            r'\b(reviewed|examined|investigated|explored|analyzed)\b',
        ],
    }

    # CARS Move 2: Establishing a Niche
    NICHE_INDICATORS = {
        'counter_claiming': [
            r'\b(however|yet|but|nevertheless|nonetheless)\b',
            r'\b(contrary\s+to|in\s+contrast\s+(to|with)|unlike)\b',
            r'\b(challenge|question|dispute|contradict)\b',
            r'\b(problematic|questionable|debatable|controversial)\b',
        ],
        'gap_indication': [
            r'\b(little|few|no|limited)\s+(research|attention|work|studies)\b',
            r'\b(gap|lacuna|void|need)\s+(in|for)\b',
            r'\b(remains?\s+(unclear|unknown|unexplored|understudied))\b',
            r'\b(has\s+not\s+been|have\s+not\s+been)\s+(studied|examined|explored)\b',
            r'\b(neglect|overlook|ignore|fail\s+to)\b',
            r'\b(missing|lacking|absent)\b',
        ],
        'question_raising': [
            r'\b(question|issue|problem)\s+(remains?|arises?|emerges?)\b',
            r'\b(it\s+is\s+(not\s+clear|uncertain|unknown))\b',
            r'\b(what|how|why|whether)\s+.+\s+(remain|is)\s+(unclear|unknown)\b',
        ],
        'continuing_tradition': [
            r'\b(follow|extend|build\s+on|expand)\b',
            r'\b(in\s+line\s+with|consistent\s+with|following)\b',
            r'\b(continue|further|advance)\s+(this|the)\b',
        ],
    }

    # CARS Move 3: Occupying the Niche
    OCCUPY_INDICATORS = {
        'purpose_statement': [
            r'\b(this\s+(paper|study|research|article|work))\s+(aims?|seeks?|attempts?|intends?)\b',
            r'\b(the\s+(purpose|aim|goal|objective)\s+of\s+this)\b',
            r'\b(we\s+(aim|seek|attempt|intend)\s+to)\b',
            r'\b(in\s+this\s+(paper|study),?\s+we)\b',
            r'\b(our\s+(aim|goal|objective)\s+is)\b',
        ],
        'findings_preview': [
            r'\b(we\s+(find|show|demonstrate|argue|propose))\b',
            r'\b(our\s+(results|findings|analysis)\s+(show|indicate|suggest|reveal))\b',
            r'\b(the\s+results\s+(indicate|suggest|show))\b',
            r'\b(we\s+present|we\s+report|we\s+provide)\b',
        ],
        'structure_indication': [
            r'\b(this\s+(paper|article)\s+is\s+(organized|structured))\b',
            r'\b(the\s+(remainder|rest)\s+of\s+this)\b',
            r'\b(section\s+\d|in\s+section)\b',
            r'\b(first,?\s+we|second,?\s+we|finally,?\s+we)\b',
            r'\b(we\s+begin\s+by|we\s+start\s+by|we\s+conclude\s+by)\b',
        ],
    }

    # Methods Section Indicators
    METHODS_INDICATORS = {
        'research_design': [
            r'\b(we\s+(use|employ|adopt|apply))\b',
            r'\b(the\s+(method|approach|methodology|design))\b',
            r'\b(experiment|survey|case\s+study|interview)\b',
            r'\b(quantitative|qualitative|mixed\s+method)\b',
        ],
        'data_collection': [
            r'\b(data\s+(was|were)\s+(collected|gathered|obtained))\b',
            r'\b(participants|subjects|respondents|sample)\b',
            r'\b(n\s*=\s*\d+|sample\s+size)\b',
            r'\b(random|stratified|convenience)\s+sampl\b',
        ],
        'analysis_procedure': [
            r'\b(we\s+(analyze|analyse|examine|test))\b',
            r'\b(regression|correlation|anova|t-test)\b',
            r'\b(statistical|analysis|coded|categorized)\b',
        ],
    }

    # Results Section Indicators
    RESULTS_INDICATORS = {
        'present_findings': [
            r'\b(table\s+\d|figure\s+\d|fig\.\s*\d)\b',
            r'\b(results?\s+(show|indicate|reveal|suggest|demonstrate))\b',
            r'\b(we\s+found|we\s+observed|we\s+identified)\b',
            r'\b(significant|insignificant)\s+(effect|difference|relationship)\b',
        ],
        'support_with_data': [
            r'\b(p\s*[<>=]\s*[\d.]+|β\s*=\s*[\d.-]+)\b',
            r'\b(\d+\.?\d*\s*%|\d+\s+percent)\b',
            r'\b(mean|median|standard\s+deviation|sd)\b',
        ],
    }

    # Discussion Section Indicators
    DISCUSSION_INDICATORS = {
        'summarize_results': [
            r'\b(in\s+summary|to\s+summarize|overall)\b',
            r'\b(our\s+(results|findings)\s+(show|suggest|indicate))\b',
            r'\b(the\s+main\s+(finding|result))\b',
        ],
        'interpret_findings': [
            r'\b(this\s+(suggests|indicates|implies|means))\b',
            r'\b(one\s+possible\s+explanation)\b',
            r'\b(we\s+(interpret|understand|explain)\s+this)\b',
        ],
        'compare_literature': [
            r'\b(consistent\s+with|in\s+line\s+with|contrary\s+to)\b',
            r'\b(similar\s+to|different\s+from)\s+(previous|prior|earlier)\b',
            r'\b(supports?|contradicts?|confirms?)\s+(the|previous|prior)\b',
        ],
        'acknowledge_limitations': [
            r'\b(limitation|limitation\s+of\s+this|constrain)\b',
            r'\b(however,?\s+this\s+study|one\s+limitation)\b',
            r'\b(should\s+be\s+interpreted\s+with\s+caution)\b',
            r'\b(future\s+research\s+should|further\s+research)\b',
        ],
        'suggest_implications': [
            r'\b(implication|practical\s+implication|theoretical\s+implication)\b',
            r'\b(these\s+(findings|results)\s+suggest\s+that)\b',
            r'\b(policy\s+makers?|practitioners?|managers?)\s+(should|could|might)\b',
        ],
    }

    # Conclusion Section Indicators
    CONCLUSION_INDICATORS = {
        'restate_purpose': [
            r'\b(in\s+this\s+(paper|study),?\s+we)\b',
            r'\b(we\s+(set\s+out|aimed|sought)\s+to)\b',
            r'\b(the\s+(purpose|aim|goal)\s+of\s+this\s+(study|paper))\b',
        ],
        'summarize_contribution': [
            r'\b(contribution|this\s+(paper|study)\s+contributes?)\b',
            r'\b(we\s+have\s+(shown|demonstrated|established))\b',
            r'\b(in\s+conclusion|to\s+conclude|in\s+closing)\b',
        ],
        'future_research': [
            r'\b(future\s+(research|studies|work)\s+(should|could|might))\b',
            r'\b(further\s+(research|investigation|analysis))\b',
            r'\b(remains?\s+to\s+be\s+(seen|explored|investigated))\b',
        ],
    }

    # Policy Brief Indicators
    POLICY_INDICATORS = {
        'problem_statement': [
            r'\b(problem|challenge|issue|crisis)\b',
            r'\b(urgent|pressing|critical|immediate)\s+(need|action|attention)\b',
            r'\b(affects?\s+\d+|impacts?\s+(millions?|thousands?))\b',
        ],
        'evidence_presentation': [
            r'\b(evidence\s+(shows?|suggests?|indicates?))\b',
            r'\b(research\s+(shows?|demonstrates?|reveals?))\b',
            r'\b(data\s+(from|indicates?|shows?))\b',
        ],
        'policy_options': [
            r'\b(option\s+\d|alternative\s+\d|policy\s+option)\b',
            r'\b(one\s+(approach|option|solution)|another\s+(approach|option))\b',
            r'\b(could|should|might)\s+(consider|adopt|implement)\b',
        ],
        'recommendation': [
            r'\b(we\s+recommend|recommendation|recommended\s+action)\b',
            r'\b(should\s+be\s+(adopted|implemented|considered))\b',
            r'\b(call\s+for|urge|propose)\b',
        ],
        'call_to_action': [
            r'\b(action\s+(is|must\s+be)\s+(taken|required))\b',
            r'\b(decision\s+makers?\s+(should|must|need\s+to))\b',
            r'\b(next\s+steps?|immediate\s+action)\b',
        ],
    }

    # EBF Appendix Indicators
    EBF_INDICATORS = {
        'header_block': [
            r'\b(appendix|category|version|dependencies)\b',
            r'\b(cross[- ]?reference|chapter\s+linkage)\b',
        ],
        'fundamental_question': [
            r'\b(fundamental\s+question|central\s+question|core\s+question)\b',
            r'\b(what|how|why|when|where)\s+.+\?',
            r'\b(10c\s+dimension|10c\s+mapping)\b',
        ],
        'axioms': [
            r'\b(axiom|theorem|lemma|proposition|corollary)\b',
            r'\b(definition\s+\d|def\.\s*\d)\b',
            r'\b(formal(ly)?|mathematically|rigorous(ly)?)\b',
        ],
        'worked_example': [
            r'\b(example|worked\s+example|illustrat)\b',
            r'\b(consider|suppose|let\s+us|imagine)\b',
            r'\b(step\s+\d|first,?\s+we|then,?\s+we)\b',
        ],
        'integration': [
            r'\b(integrat|connect|link|bridge)\b',
            r'\b(cross[- ]?reference|see\s+also|cf\.)\b',
            r'\b(appendix\s+[a-z]|chapter\s+\d)\b',
        ],
        'glossary_link': [
            r'\b(glossary|terminology|definition)\b',
            r'\b(see\s+glossary|appendix\s+g)\b',
        ],
    }


# =============================================================================
# MOVE PATTERN MATCHER
# =============================================================================

class MovePatternMatcher:
    """
    Matches text against move indicator patterns.
    Returns confidence scores and matched indicators.
    """

    def __init__(self):
        self.lexicon = MoveIndicatorLexicon()
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for efficiency."""
        self.compiled_patterns = {}

        # Compile all indicator categories
        for category_name in dir(self.lexicon):
            if category_name.endswith('_INDICATORS'):
                category = getattr(self.lexicon, category_name)
                self.compiled_patterns[category_name] = {}
                for strategy, patterns in category.items():
                    self.compiled_patterns[category_name][strategy] = [
                        re.compile(p, re.IGNORECASE) for p in patterns
                    ]

    def match_indicators(
        self,
        text: str,
        indicator_category: str
    ) -> Dict[str, Tuple[float, List[str]]]:
        """
        Match text against indicators in a category.

        Returns:
            Dict mapping strategy names to (confidence, matched_indicators)
        """
        if indicator_category not in self.compiled_patterns:
            return {}

        results = {}
        patterns_dict = self.compiled_patterns[indicator_category]

        for strategy, patterns in patterns_dict.items():
            matched = []
            for pattern in patterns:
                matches = pattern.findall(text)
                if matches:
                    if isinstance(matches[0], tuple):
                        matched.extend([m[0] for m in matches])
                    else:
                        matched.extend(matches)

            if matched:
                # Confidence based on number of distinct pattern matches
                confidence = min(1.0, len(set(matched)) / len(patterns) + 0.3)
                results[strategy] = (confidence, list(set(matched)))

        return results

    def identify_move_type(
        self,
        text: str,
        section_context: Optional[SectionType] = None
    ) -> List[Tuple[str, str, float, List[str]]]:
        """
        Identify potential moves in text.

        Returns:
            List of (move_category, strategy, confidence, indicators)
        """
        results = []

        # Check all indicator categories
        category_mapping = {
            'TERRITORY_INDICATORS': ('Establish_Territory', SectionType.INTRODUCTION),
            'NICHE_INDICATORS': ('Establish_Niche', SectionType.INTRODUCTION),
            'OCCUPY_INDICATORS': ('Occupy_Niche', SectionType.INTRODUCTION),
            'METHODS_INDICATORS': ('Methods', SectionType.METHODS),
            'RESULTS_INDICATORS': ('Results', SectionType.RESULTS),
            'DISCUSSION_INDICATORS': ('Discussion', SectionType.DISCUSSION),
            'CONCLUSION_INDICATORS': ('Conclusion', SectionType.CONCLUSION),
            'POLICY_INDICATORS': ('Policy', None),
            'EBF_INDICATORS': ('EBF', None),
        }

        for category, (move_name, expected_section) in category_mapping.items():
            # Apply section context boost
            section_boost = 0.0
            if section_context and expected_section == section_context:
                section_boost = 0.15

            matches = self.match_indicators(text, category)
            for strategy, (confidence, indicators) in matches.items():
                adjusted_confidence = min(1.0, confidence + section_boost)
                results.append((move_name, strategy, adjusted_confidence, indicators))

        # Sort by confidence
        results.sort(key=lambda x: x[2], reverse=True)
        return results


# =============================================================================
# SECTION CLASSIFIER
# =============================================================================

class SectionClassifier:
    """Classifies sections based on titles and content."""

    SECTION_PATTERNS = {
        SectionType.ABSTRACT: [
            r'\babstract\b', r'\bsummary\b', r'\bsynopsis\b'
        ],
        SectionType.INTRODUCTION: [
            r'\bintroduction\b', r'\bbackground\b', r'\boverview\b'
        ],
        SectionType.LITERATURE: [
            r'\bliterature\s+review\b', r'\brelated\s+work\b',
            r'\btheoretical\s+(framework|background)\b', r'\bprior\s+research\b'
        ],
        SectionType.METHODS: [
            r'\bmethod(s|ology)?\b', r'\bdata\b', r'\bprocedure\b',
            r'\bresearch\s+design\b', r'\bmaterial(s)?\s+and\s+method(s)?\b'
        ],
        SectionType.RESULTS: [
            r'\bresult(s)?\b', r'\bfinding(s)?\b', r'\banalysis\b',
            r'\bempirical\s+results\b'
        ],
        SectionType.DISCUSSION: [
            r'\bdiscussion\b', r'\binterpretation\b', r'\bimplication(s)?\b'
        ],
        SectionType.CONCLUSION: [
            r'\bconclusion(s)?\b', r'\bsummary\b', r'\bfinal\s+remarks\b',
            r'\bconcluding\s+remarks\b'
        ],
        SectionType.EXECUTIVE: [
            r'\bexecutive\s+summary\b', r'\bkey\s+points\b', r'\bhighlights\b'
        ],
        SectionType.PROBLEM: [
            r'\bproblem\s+statement\b', r'\bissue\b', r'\bchallenge\b'
        ],
        SectionType.EVIDENCE: [
            r'\bevidence\b', r'\bsupporting\s+data\b'
        ],
        SectionType.RECOMMENDATION: [
            r'\brecommendation(s)?\b', r'\bproposal\b', r'\bsuggestion(s)?\b',
            r'\bcall\s+to\s+action\b'
        ],
    }

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile section patterns."""
        self.compiled = {
            section: [re.compile(p, re.IGNORECASE) for p in patterns]
            for section, patterns in self.SECTION_PATTERNS.items()
        }

    def classify(self, title: str, content: str = "") -> SectionType:
        """Classify section based on title and optionally content."""
        # First check title
        for section, patterns in self.compiled.items():
            for pattern in patterns:
                if pattern.search(title):
                    return section

        # If no match, check content beginning
        if content:
            content_start = content[:500].lower()
            for section, patterns in self.compiled.items():
                for pattern in patterns:
                    if pattern.search(content_start):
                        return section

        return SectionType.UNKNOWN


# =============================================================================
# GENRE-SPECIFIC MOVE TEMPLATES
# =============================================================================

class GenreMoveTemplates:
    """
    Genre-specific move templates based on SWSM schema.
    Maps genres to expected move sequences.
    """

    TEMPLATES = {
        GenreType.SCIENTIFIC_PAPER: {
            'sections': [
                {
                    'id': 'abstract',
                    'position': 'initial',
                    'moves': [
                        ('SP-01', 'Background', MoveStatus.OBLIGATORY),
                        ('SP-02', 'Purpose', MoveStatus.OBLIGATORY),
                        ('SP-03', 'Method', MoveStatus.OBLIGATORY),
                        ('SP-04', 'Results', MoveStatus.OBLIGATORY),
                        ('SP-05', 'Conclusion', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'introduction',
                    'position': 'early',
                    'moves': [
                        ('SP-10', 'Establish_Territory', MoveStatus.OBLIGATORY),
                        ('SP-11', 'Establish_Niche', MoveStatus.OBLIGATORY),
                        ('SP-12', 'Occupy_Niche', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'literature',
                    'position': 'early',
                    'moves': [
                        ('SP-20', 'Organize_Literature', MoveStatus.OBLIGATORY),
                        ('SP-21', 'Synthesize_Findings', MoveStatus.OBLIGATORY),
                        ('SP-22', 'Identify_Gap', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'methods',
                    'position': 'medial',
                    'moves': [
                        ('SP-30', 'Research_Design', MoveStatus.OBLIGATORY),
                        ('SP-31', 'Data_Collection', MoveStatus.OBLIGATORY),
                        ('SP-32', 'Analysis_Procedure', MoveStatus.OBLIGATORY),
                        ('SP-33', 'Validity_Discussion', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'results',
                    'position': 'medial',
                    'moves': [
                        ('SP-40', 'Present_Findings', MoveStatus.OBLIGATORY),
                        ('SP-41', 'Support_with_Data', MoveStatus.OBLIGATORY),
                        ('SP-42', 'Reference_Visuals', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'discussion',
                    'position': 'late',
                    'moves': [
                        ('SP-50', 'Summarize_Results', MoveStatus.OBLIGATORY),
                        ('SP-51', 'Interpret_Findings', MoveStatus.OBLIGATORY),
                        ('SP-52', 'Compare_Literature', MoveStatus.OBLIGATORY),
                        ('SP-53', 'Acknowledge_Limitations', MoveStatus.CONVENTIONAL),
                        ('SP-54', 'Suggest_Implications', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'conclusion',
                    'position': 'final',
                    'moves': [
                        ('SP-60', 'Restate_Purpose', MoveStatus.OBLIGATORY),
                        ('SP-61', 'Summarize_Contribution', MoveStatus.OBLIGATORY),
                        ('SP-62', 'Future_Research', MoveStatus.OPTIONAL),
                    ]
                },
            ]
        },

        GenreType.POLICY_BRIEF: {
            'sections': [
                {
                    'id': 'executive',
                    'position': 'initial',
                    'moves': [
                        ('PB-01', 'Key_Message', MoveStatus.OBLIGATORY),
                        ('PB-02', 'Core_Recommendation', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'problem',
                    'position': 'early',
                    'moves': [
                        ('PB-10', 'Define_Problem', MoveStatus.OBLIGATORY),
                        ('PB-11', 'Quantify_Impact', MoveStatus.OBLIGATORY),
                        ('PB-12', 'Urgency_Claim', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'evidence',
                    'position': 'medial',
                    'moves': [
                        ('PB-20', 'Present_Evidence', MoveStatus.OBLIGATORY),
                        ('PB-21', 'Cite_Research', MoveStatus.OBLIGATORY),
                        ('PB-22', 'Case_Examples', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'options',
                    'position': 'medial',
                    'moves': [
                        ('PB-30', 'Option_A', MoveStatus.OBLIGATORY),
                        ('PB-31', 'Option_B', MoveStatus.OBLIGATORY),
                        ('PB-32', 'Option_C', MoveStatus.OPTIONAL),
                        ('PB-33', 'Compare_Options', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'recommendation',
                    'position': 'late',
                    'moves': [
                        ('PB-40', 'Recommend_Option', MoveStatus.OBLIGATORY),
                        ('PB-41', 'Justify_Choice', MoveStatus.OBLIGATORY),
                        ('PB-42', 'Implementation_Steps', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'action',
                    'position': 'final',
                    'moves': [
                        ('PB-50', 'Specify_Actions', MoveStatus.OBLIGATORY),
                        ('PB-51', 'Timeline', MoveStatus.CONVENTIONAL),
                        ('PB-52', 'Stakeholder_Assignment', MoveStatus.OPTIONAL),
                    ]
                },
            ]
        },

        GenreType.EBF_APPENDIX: {
            'sections': [
                {
                    'id': 'header',
                    'position': 'initial',
                    'moves': [
                        ('EA-01', 'Category_Declaration', MoveStatus.OBLIGATORY),
                        ('EA-02', 'Version_Info', MoveStatus.OBLIGATORY),
                        ('EA-03', 'Dependencies', MoveStatus.OBLIGATORY),
                        ('EA-04', 'Cross_Reference_Map', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'abstract',
                    'position': 'initial',
                    'moves': [
                        ('EA-10', 'Quick_Reference', MoveStatus.OBLIGATORY),
                        ('EA-11', 'Purpose_Statement', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'fundamental',
                    'position': 'early',
                    'moves': [
                        ('EA-20', 'State_Question', MoveStatus.OBLIGATORY),
                        ('EA-21', '10C_Mapping', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'theory',
                    'position': 'early',
                    'moves': [
                        ('EA-30', 'Axioms', MoveStatus.CONVENTIONAL),
                        ('EA-31', 'Core_Concepts', MoveStatus.OBLIGATORY),
                        ('EA-32', 'Formal_Definitions', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'examples',
                    'position': 'medial',
                    'moves': [
                        ('EA-40', 'Example_Setup', MoveStatus.CONVENTIONAL),
                        ('EA-41', 'Step_by_Step', MoveStatus.CONVENTIONAL),
                        ('EA-42', 'Interpretation', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'integration',
                    'position': 'late',
                    'moves': [
                        ('EA-50', '10C_Integration', MoveStatus.OBLIGATORY),
                        ('EA-51', 'Cross_References', MoveStatus.OBLIGATORY),
                        ('EA-52', 'Implications', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'summary',
                    'position': 'final',
                    'moves': [
                        ('EA-60', 'Key_Takeaways', MoveStatus.OBLIGATORY),
                        ('EA-61', 'Critical_Foundations', MoveStatus.OBLIGATORY),
                        ('EA-62', 'Open_Issues', MoveStatus.CONVENTIONAL),
                    ]
                },
                {
                    'id': 'references',
                    'position': 'final',
                    'moves': [
                        ('EA-70', 'Glossary_Link', MoveStatus.OBLIGATORY),
                        ('EA-71', 'Master_Bib_Link', MoveStatus.OBLIGATORY),
                        ('EA-72', 'Section_References', MoveStatus.CONVENTIONAL),
                    ]
                },
            ]
        },

        GenreType.EXECUTIVE_SUMMARY: {
            'sections': [
                {
                    'id': 'headline',
                    'position': 'initial',
                    'moves': [
                        ('ES-01', 'One_Sentence_Summary', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'situation',
                    'position': 'early',
                    'moves': [
                        ('ES-10', 'Context', MoveStatus.OBLIGATORY),
                        ('ES-11', 'Challenge', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'findings',
                    'position': 'medial',
                    'moves': [
                        ('ES-20', 'Finding_1', MoveStatus.OBLIGATORY),
                        ('ES-21', 'Finding_2', MoveStatus.OBLIGATORY),
                        ('ES-22', 'Finding_3', MoveStatus.OPTIONAL),
                    ]
                },
                {
                    'id': 'action',
                    'position': 'final',
                    'moves': [
                        ('ES-30', 'Primary_Action', MoveStatus.OBLIGATORY),
                        ('ES-31', 'Next_Steps', MoveStatus.CONVENTIONAL),
                    ]
                },
            ]
        },

        GenreType.BLOG_POST: {
            'sections': [
                {
                    'id': 'hook',
                    'position': 'initial',
                    'moves': [
                        ('BP-01', 'Attention_Grabber', MoveStatus.OBLIGATORY),
                        ('BP-02', 'Promise_Value', MoveStatus.OBLIGATORY),
                    ]
                },
                {
                    'id': 'body',
                    'position': 'medial',
                    'moves': [
                        ('BP-10', 'Main_Point_1', MoveStatus.OBLIGATORY),
                        ('BP-11', 'Support_1', MoveStatus.OBLIGATORY),
                        ('BP-12', 'Main_Point_2', MoveStatus.CONVENTIONAL),
                        ('BP-13', 'Support_2', MoveStatus.CONVENTIONAL),
                        ('BP-14', 'Main_Point_3', MoveStatus.OPTIONAL),
                    ]
                },
                {
                    'id': 'conclusion',
                    'position': 'final',
                    'moves': [
                        ('BP-20', 'Summary', MoveStatus.OBLIGATORY),
                        ('BP-21', 'Call_to_Action', MoveStatus.CONVENTIONAL),
                        ('BP-22', 'Engagement_Prompt', MoveStatus.OPTIONAL),
                    ]
                },
            ]
        },
    }

    @classmethod
    def get_template(cls, genre: GenreType) -> Optional[Dict]:
        """Get move template for a genre."""
        return cls.TEMPLATES.get(genre)

    @classmethod
    def get_obligatory_moves(cls, genre: GenreType) -> List[Tuple[str, str]]:
        """Get list of obligatory moves for a genre."""
        template = cls.get_template(genre)
        if not template:
            return []

        obligatory = []
        for section in template['sections']:
            for move_id, move_name, status in section['moves']:
                if status == MoveStatus.OBLIGATORY:
                    obligatory.append((move_id, move_name))
        return obligatory


# =============================================================================
# CARS MOVE TAGGER
# =============================================================================

class CARSMoveTagger:
    """
    Main class for CARS-based move tagging.
    Implements SWSM E3 functionality.
    """

    def __init__(self, genre: GenreType = GenreType.SCIENTIFIC_PAPER):
        self.genre = genre
        self.pattern_matcher = MovePatternMatcher()
        self.section_classifier = SectionClassifier()
        self.templates = GenreMoveTemplates()

    def tag_text(self, text: str, section_hint: Optional[str] = None) -> List[Move]:
        """
        Tag moves in a text passage.

        Args:
            text: The text to analyze
            section_hint: Optional hint about which section this is

        Returns:
            List of identified moves
        """
        # Determine section context
        section_type = SectionType.UNKNOWN
        if section_hint:
            section_type = self.section_classifier.classify(section_hint)

        # Get move patterns
        move_matches = self.pattern_matcher.identify_move_type(text, section_type)

        # Convert to Move objects
        moves = []
        seen_moves = set()

        for move_category, strategy, confidence, indicators in move_matches:
            if confidence < 0.3:
                continue

            # Avoid duplicate move categories
            if move_category in seen_moves:
                continue
            seen_moves.add(move_category)

            # Create strategy object
            strategy_obj = Strategy(
                strategy_id=f"{move_category}-{strategy}",
                name=strategy,
                description=f"Strategy: {strategy}",
                confidence=confidence,
                indicators=indicators
            )

            # Find matching move from template
            template = self.templates.get_template(self.genre)
            move_id = f"AUTO-{move_category}"
            status = MoveStatus.CONVENTIONAL

            if template:
                for section in template['sections']:
                    for m_id, m_name, m_status in section['moves']:
                        if strategy.lower() in m_name.lower():
                            move_id = m_id
                            status = m_status
                            break

            move = Move(
                move_id=move_id,
                name=move_category,
                purpose=f"Identified via {strategy}",
                status=status,
                section=section_type,
                strategies=[strategy_obj],
                confidence=confidence,
                text=text[:200] + "..." if len(text) > 200 else text
            )
            moves.append(move)

        return moves

    def tag_document(
        self,
        sections: List[Dict[str, str]]
    ) -> TaggedDocument:
        """
        Tag moves in an entire document.

        Args:
            sections: List of dicts with 'title' and 'content' keys

        Returns:
            TaggedDocument with all moves identified
        """
        tagged_sections = []
        all_moves_found = set()

        for i, section_data in enumerate(sections):
            title = section_data.get('title', f'Section {i+1}')
            content = section_data.get('content', '')

            # Classify section
            section_type = self.section_classifier.classify(title, content)

            # Determine position
            if i == 0:
                position = 'initial'
            elif i == len(sections) - 1:
                position = 'final'
            elif i < len(sections) / 3:
                position = 'early'
            elif i > 2 * len(sections) / 3:
                position = 'late'
            else:
                position = 'medial'

            # Tag moves in content
            moves = self.tag_text(content, title)

            for move in moves:
                all_moves_found.add(move.move_id)

            tagged_section = TaggedSection(
                section_id=f"sec-{i+1}",
                section_type=section_type,
                title=title,
                moves=moves,
                text=content,
                position=position
            )
            tagged_sections.append(tagged_section)

        # Calculate move coverage
        obligatory_moves = self.templates.get_obligatory_moves(self.genre)
        obligatory_found = sum(
            1 for move_id, _ in obligatory_moves
            if move_id in all_moves_found
        )

        coverage = obligatory_found / len(obligatory_moves) if obligatory_moves else 1.0

        return TaggedDocument(
            genre=self.genre,
            sections=tagged_sections,
            move_coverage=coverage,
            obligatory_moves_found=obligatory_found,
            obligatory_moves_expected=len(obligatory_moves)
        )

    def get_missing_moves(self, tagged_doc: TaggedDocument) -> List[Tuple[str, str]]:
        """Get list of obligatory moves not found in document."""
        template = self.templates.get_template(self.genre)
        if not template:
            return []

        found_moves = set()
        for section in tagged_doc.sections:
            for move in section.moves:
                found_moves.add(move.move_id)

        missing = []
        for section in template['sections']:
            for move_id, move_name, status in section['moves']:
                if status == MoveStatus.OBLIGATORY and move_id not in found_moves:
                    missing.append((move_id, move_name))

        return missing


# =============================================================================
# SWSM INTEGRATION: MOVE ANALYZER
# =============================================================================

class MoveAnalyzer:
    """
    SWSM Pipeline integration for E3 Move Tagger.
    Provides interface compatible with other SWSM components.
    """

    def __init__(self):
        self.taggers = {
            genre: CARSMoveTagger(genre)
            for genre in GenreType
        }
        self.default_genre = GenreType.SCIENTIFIC_PAPER

    def analyze(
        self,
        text: str,
        genre: Optional[GenreType] = None,
        section_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze text for moves.

        Args:
            text: Text to analyze
            genre: Genre type (defaults to scientific paper)
            section_hint: Optional section context

        Returns:
            Analysis results dict
        """
        # Handle string or enum input
        if isinstance(genre, str):
            try:
                genre = GenreType(genre)
            except ValueError:
                genre = self.default_genre
        genre = genre or self.default_genre
        tagger = self.taggers.get(genre, self.taggers[self.default_genre])

        moves = tagger.tag_text(text, section_hint)

        return {
            'genre': genre.value,
            'section_hint': section_hint,
            'moves': [
                {
                    'move_id': m.move_id,
                    'name': m.name,
                    'confidence': m.confidence,
                    'status': m.status.value,
                    'strategies': [
                        {
                            'name': s.name,
                            'confidence': s.confidence,
                            'indicators': s.indicators
                        }
                        for s in m.strategies
                    ]
                }
                for m in moves
            ],
            'move_count': len(moves),
            'high_confidence_moves': len([m for m in moves if m.confidence > 0.7])
        }

    def analyze_document(
        self,
        sections: List[Dict[str, str]],
        genre: Optional[GenreType] = None
    ) -> Dict[str, Any]:
        """
        Analyze entire document for moves.

        Args:
            sections: List of section dicts with 'title' and 'content'
            genre: Genre type

        Returns:
            Document analysis results
        """
        genre = genre or self.default_genre
        tagger = self.taggers.get(genre, self.taggers[self.default_genre])

        tagged_doc = tagger.tag_document(sections)
        missing_moves = tagger.get_missing_moves(tagged_doc)

        return {
            'genre': genre.value,
            'move_coverage': tagged_doc.move_coverage,
            'obligatory_found': tagged_doc.obligatory_moves_found,
            'obligatory_expected': tagged_doc.obligatory_moves_expected,
            'missing_obligatory_moves': [
                {'move_id': m_id, 'name': m_name}
                for m_id, m_name in missing_moves
            ],
            'sections': [
                {
                    'section_id': s.section_id,
                    'section_type': s.section_type.value,
                    'title': s.title,
                    'position': s.position,
                    'moves': [
                        {
                            'move_id': m.move_id,
                            'name': m.name,
                            'confidence': m.confidence
                        }
                        for m in s.moves
                    ]
                }
                for s in tagged_doc.sections
            ]
        }

    def get_genre_template(self, genre: GenreType) -> Dict[str, Any]:
        """Get the move template for a genre."""
        template = GenreMoveTemplates.get_template(genre)
        if not template:
            return {'error': f'No template for genre: {genre.value}'}

        return {
            'genre': genre.value,
            'sections': [
                {
                    'section_id': s['id'],
                    'position': s['position'],
                    'moves': [
                        {
                            'move_id': m_id,
                            'name': m_name,
                            'status': status.value
                        }
                        for m_id, m_name, status in s['moves']
                    ]
                }
                for s in template['sections']
            ]
        }


# =============================================================================
# DEMO / TEST
# =============================================================================

def demo():
    """Demonstrate E3 Move Tagger functionality."""
    print("=" * 70)
    print("SWSM E3: CARS Move Tagger Demo")
    print("=" * 70)

    # Sample academic introduction
    intro_text = """
    Research on behavioral economics has shown that humans often deviate from
    rational decision-making. In recent years, nudging has become increasingly
    important in policy design. Previous studies have demonstrated that default
    options significantly influence choices (Thaler & Sunstein, 2008).

    However, little attention has been paid to cultural variations in nudge
    effectiveness. Despite extensive research in Western contexts, the question
    of whether nudges work equally well across cultures remains unclear.

    This paper aims to address this gap by examining nudge effectiveness across
    three different cultural contexts. We argue that cultural dimensions
    significantly moderate the impact of choice architecture interventions.
    Our findings suggest that individualism-collectivism dimensions predict
    differential responses to social norm nudges.
    """

    # Create analyzer
    analyzer = MoveAnalyzer()

    # Analyze introduction
    print("\n1. Analyzing Academic Introduction:")
    print("-" * 50)

    results = analyzer.analyze(
        intro_text,
        genre=GenreType.SCIENTIFIC_PAPER,
        section_hint="Introduction"
    )

    print(f"Genre: {results['genre']}")
    print(f"Moves found: {results['move_count']}")
    print(f"High confidence: {results['high_confidence_moves']}")
    print("\nIdentified Moves:")
    for move in results['moves']:
        print(f"  - {move['name']} (confidence: {move['confidence']:.2f})")
        for strat in move['strategies']:
            print(f"    Strategy: {strat['name']}")
            print(f"    Indicators: {strat['indicators'][:3]}...")

    # Sample policy brief sections
    print("\n" + "=" * 70)
    print("2. Analyzing Policy Brief Document:")
    print("-" * 50)

    policy_sections = [
        {
            'title': 'Executive Summary',
            'content': 'The retirement savings crisis affects millions of workers. We recommend mandatory auto-enrollment with opt-out provisions.'
        },
        {
            'title': 'Problem Statement',
            'content': 'The problem of inadequate retirement savings is urgent. Over 40% of workers have less than $10,000 saved. This crisis demands immediate policy action.'
        },
        {
            'title': 'Evidence',
            'content': 'Research shows that auto-enrollment increases participation rates by 50 percentage points. According to Madrian and Shea (2001), default effects are powerful.'
        },
        {
            'title': 'Recommendation',
            'content': 'We recommend Option B: mandatory auto-enrollment at 6% with annual escalation. This should be implemented within 12 months.'
        },
    ]

    doc_results = analyzer.analyze_document(
        policy_sections,
        genre=GenreType.POLICY_BRIEF
    )

    print(f"Move Coverage: {doc_results['move_coverage']:.1%}")
    print(f"Obligatory Moves: {doc_results['obligatory_found']}/{doc_results['obligatory_expected']}")

    if doc_results['missing_obligatory_moves']:
        print("\nMissing Obligatory Moves:")
        for move in doc_results['missing_obligatory_moves']:
            print(f"  - {move['move_id']}: {move['name']}")

    # Show genre template
    print("\n" + "=" * 70)
    print("3. Genre Template (EBF Appendix):")
    print("-" * 50)

    template = analyzer.get_genre_template(GenreType.EBF_APPENDIX)
    for section in template['sections'][:3]:  # Show first 3 sections
        print(f"\nSection: {section['section_id']} ({section['position']})")
        for move in section['moves']:
            status_symbol = "★" if move['status'] == 'obligatory' else "◆" if move['status'] == 'conventional' else "○"
            print(f"  {status_symbol} {move['move_id']}: {move['name']}")


if __name__ == "__main__":
    demo()
