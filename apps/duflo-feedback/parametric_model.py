"""
Parametric Duflo Scoring Model

Evaluates experimental designs across 5 Duflo criteria with sub-dimensions.
Each criterion has weighted sub-dimensions that produce a score from 0-5.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Criterion definitions with sub-dimensions and scoring rules
# ---------------------------------------------------------------------------

CRITERIA = {
    "randomization": {
        "name": "Randomisierung und Identifikation",
        "weight": 0.25,
        "sub_dimensions": {
            "design_type": {
                "label": "Experimentelles Design",
                "weight": 0.35,
                "scoring": {
                    "rct": 5,
                    "quasi_experimental": 3.5,
                    "natural_experiment": 3,
                    "observational": 1.5,
                    "case_study": 1,
                },
            },
            "assignment_mechanism": {
                "label": "Zuweisungsmechanismus",
                "weight": 0.25,
                "scoring": {
                    "individual_random": 5,
                    "cluster_random": 4,
                    "stratified_random": 4.5,
                    "as_if_random": 3,
                    "self_selection": 1,
                    "no_control": 0,
                },
            },
            "selection_bias_control": {
                "label": "Selektionsbias-Kontrolle",
                "weight": 0.20,
                "scoring": {
                    "balance_test_planned": 5,
                    "baseline_survey": 4,
                    "matching": 3,
                    "no_plan": 1,
                },
            },
            "confounders_addressed": {
                "label": "Störvariablen adressiert",
                "weight": 0.20,
                "scoring": {
                    "systematic_list": 5,
                    "some_identified": 3,
                    "not_discussed": 1,
                },
            },
        },
    },
    "measurability": {
        "name": "Messbarkeit der Outcomes",
        "weight": 0.20,
        "sub_dimensions": {
            "primary_outcome": {
                "label": "Primärer Outcome",
                "weight": 0.30,
                "scoring": {
                    "quantitative_specific": 5,
                    "quantitative_broad": 3.5,
                    "qualitative_structured": 3,
                    "qualitative_vague": 1.5,
                    "not_defined": 0,
                },
            },
            "operationalization": {
                "label": "Operationalisierung",
                "weight": 0.25,
                "scoring": {
                    "validated_instrument": 5,
                    "clear_proxy": 4,
                    "self_developed": 3,
                    "unclear": 1,
                },
            },
            "data_source": {
                "label": "Datenquelle",
                "weight": 0.20,
                "scoring": {
                    "admin_data": 5,
                    "structured_survey": 4,
                    "behavioral_observation": 4,
                    "self_report": 3,
                    "unstructured": 1.5,
                },
            },
            "measurement_timing": {
                "label": "Messzeitpunkte",
                "weight": 0.15,
                "scoring": {
                    "baseline_endline_followup": 5,
                    "baseline_endline": 4,
                    "endline_only": 2.5,
                    "unclear": 1,
                },
            },
            "power_analysis": {
                "label": "Power-Analyse",
                "weight": 0.10,
                "scoring": {
                    "formal_calculation": 5,
                    "informal_justification": 3,
                    "not_addressed": 1,
                },
            },
        },
    },
    "causality": {
        "name": "Kausalität und Theorie des Wandels",
        "weight": 0.20,
        "sub_dimensions": {
            "theory_of_change": {
                "label": "Theory of Change",
                "weight": 0.30,
                "scoring": {
                    "complete_chain": 5,
                    "partial_chain": 3,
                    "implicit": 2,
                    "missing": 0,
                },
            },
            "causal_mechanism": {
                "label": "Kausaler Mechanismus",
                "weight": 0.30,
                "scoring": {
                    "clearly_specified": 5,
                    "plausible_but_vague": 3,
                    "assumed": 1.5,
                    "not_discussed": 0,
                },
            },
            "behavioral_channel": {
                "label": "Verhaltenskanal",
                "weight": 0.20,
                "scoring": {
                    "specific_channel_identified": 5,
                    "multiple_possible": 3,
                    "not_specified": 1,
                },
            },
            "alternative_explanations": {
                "label": "Alternativerklärungen",
                "weight": 0.20,
                "scoring": {
                    "systematically_addressed": 5,
                    "some_discussed": 3,
                    "not_discussed": 1,
                },
            },
        },
    },
    "scalability": {
        "name": "Skalierbarkeit und externe Validität",
        "weight": 0.15,
        "sub_dimensions": {
            "population_transfer": {
                "label": "Populationstransfer",
                "weight": 0.25,
                "scoring": {
                    "representative_sample": 5,
                    "specific_but_transferable": 3.5,
                    "narrow_sample": 2,
                    "not_discussed": 1,
                },
            },
            "context_transfer": {
                "label": "Kontexttransfer",
                "weight": 0.25,
                "scoring": {
                    "multi_site_planned": 5,
                    "transferability_discussed": 3.5,
                    "context_specific": 2,
                    "not_discussed": 1,
                },
            },
            "time_stability": {
                "label": "Zeitstabilität",
                "weight": 0.20,
                "scoring": {
                    "long_term_followup": 5,
                    "medium_term": 3.5,
                    "short_term_only": 2,
                    "not_discussed": 1,
                },
            },
            "scaling_feasibility": {
                "label": "Skalierungspotenzial",
                "weight": 0.15,
                "scoring": {
                    "cost_effective_scalable": 5,
                    "scalable_with_adaptation": 3.5,
                    "difficult_to_scale": 2,
                    "not_discussed": 1,
                },
            },
            "general_equilibrium": {
                "label": "General-Equilibrium-Effekte",
                "weight": 0.15,
                "scoring": {
                    "discussed_and_addressed": 5,
                    "acknowledged": 3,
                    "not_discussed": 1,
                },
            },
        },
    },
    "ethics": {
        "name": "Ethik und Forschungsverantwortung",
        "weight": 0.20,
        "sub_dimensions": {
            "informed_consent": {
                "label": "Informed Consent",
                "weight": 0.25,
                "scoring": {
                    "full_consent_protocol": 5,
                    "partial_consent": 3,
                    "no_consent_justified": 2.5,
                    "no_consent_unjustified": 0,
                },
            },
            "harm_prevention": {
                "label": "Schadensvermeidung",
                "weight": 0.25,
                "scoring": {
                    "no_harm_documented": 5,
                    "minimal_harm_justified": 3.5,
                    "potential_harm_unaddressed": 1,
                },
            },
            "equipoise": {
                "label": "Equipoise",
                "weight": 0.20,
                "scoring": {
                    "genuine_uncertainty": 5,
                    "reasonable_uncertainty": 3.5,
                    "weak_equipoise": 2,
                    "no_equipoise": 0,
                },
            },
            "data_protection": {
                "label": "Datenschutz",
                "weight": 0.15,
                "scoring": {
                    "anonymization_plan": 5,
                    "basic_protection": 3,
                    "not_addressed": 1,
                },
            },
            "aftercare": {
                "label": "Nachsorge (Kontrollgruppe)",
                "weight": 0.15,
                "scoring": {
                    "waitlist_or_crossover": 5,
                    "plan_described": 3.5,
                    "not_addressed": 1,
                },
            },
        },
    },
}

# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------


@dataclass
class SubDimensionResult:
    label: str
    selected: str
    score: float
    max_score: float
    weight: float


@dataclass
class CriterionResult:
    name: str
    score: float
    max_score: float
    weight: float
    sub_dimensions: list
    feedback: str


@dataclass
class ScorecardResult:
    total_score: float
    max_score: float
    percentage: float
    grade: str
    criteria: list
    summary: str
    top_strength: str
    top_weakness: str


def _grade(pct: float) -> str:
    if pct >= 90:
        return "Exzellent"
    if pct >= 75:
        return "Gut"
    if pct >= 60:
        return "Akzeptabel"
    if pct >= 40:
        return "Schwach"
    return "Ungenügend"


def _criterion_feedback(criterion_key: str, score: float, sub_results: list) -> str:
    """Generate Duflo-style feedback for a criterion."""
    pct = (score / 5.0) * 100

    # Find weakest sub-dimension
    weakest = min(sub_results, key=lambda s: s.score / s.max_score if s.max_score > 0 else 0)

    feedback_templates = {
        "randomization": {
            "high": "Euer Identifikationsdesign ist solide. Esther Duflo wuerde sagen: "
                    "«Gut — ihr wisst, warum Randomisierung wichtig ist, und ihr setzt sie korrekt ein.»",
            "medium": "Die Grundidee stimmt, aber es gibt Luecken in der Identifikationsstrategie. "
                      "Duflo wuerde fragen: «Wie schliesst ihr aus, dass der Effekt nicht von {weak} kommt?»",
            "low": "Hier fehlt eine klare Identifikationsstrategie. Duflo wuerde sagen: "
                   "«Ohne saubere Randomisierung wisst ihr nicht, ob eure Intervention wirkt oder ob "
                   "ihr nur eine Korrelation seht. Geht zurueck ans Reissbrett.»",
        },
        "measurability": {
            "high": "Eure Outcome-Variablen sind klar definiert und messbar. "
                    "Duflo: «Ihr wisst genau, welche Zahl sich aendern soll — das ist die Basis fuer gute Forschung.»",
            "medium": "Die Messung ist im Ansatz da, aber noch nicht praezise genug. "
                      "Duflo: «Was genau ist eure abhaengige Variable? Gebt mir eine Zahl, nicht ein Konzept.»",
            "low": "Die Outcomes sind zu vage oder nicht operationalisiert. "
                   "Duflo: «Ihr wollt ‹Nachhaltigkeit› messen — aber was bedeutet das konkret? "
                   "Kg CO2? Recycling-Quote? Ohne klare Messung gibt es kein Experiment.»",
        },
        "causality": {
            "high": "Eure Theory of Change ist ueberzeugend und der Mechanismus klar benannt. "
                    "Duflo: «Ihr versteht nicht nur, DASS es wirkt, sondern WARUM. Das ist der Unterschied "
                    "zwischen einem guten und einem exzellenten Experiment.»",
            "medium": "Der kausale Mechanismus ist plausibel, aber nicht vollstaendig spezifiziert. "
                      "Duflo: «Ihr habt einen Effekt — aber koenntet ihr erklaeren, warum er funktioniert? "
                      "Ohne Mechanismus wisst ihr nicht, ob es anderswo auch klappt.»",
            "low": "Es fehlt eine Theory of Change. "
                   "Duflo: «Ihr springt von der Intervention zum Ergebnis, ohne den Weg dazwischen zu erklaeren. "
                   "Das ist wie eine Landkarte ohne Strassen.»",
        },
        "scalability": {
            "high": "Ihr habt die externe Validitaet systematisch durchdacht. "
                    "Duflo: «Gut — ihr fragt nicht nur ‹funktioniert es hier?›, "
                    "sondern ‹wird es auch dort funktionieren?› Das ist der Schritt von Forschung zu Politik.»",
            "medium": "Die Skalierbarkeit wird erwaehnt, aber nicht systematisch adressiert. "
                      "Duflo: «Euer Experiment funktioniert bei 50 Studierenden. Was passiert bei 50'000? "
                      "Denkt ueber General-Equilibrium-Effekte nach.»",
            "low": "Externe Validitaet wird nicht diskutiert. "
                   "Duflo: «Ihr habt das Experiment in einem sehr spezifischen Kontext gemacht. "
                   "Ohne Diskussion der Uebertragbarkeit bleibt es eine Anekdote.»",
        },
        "ethics": {
            "high": "Die ethischen Aspekte sind vorbildlich adressiert. "
                    "Duflo: «Ihr nehmt eure Verantwortung gegenueber den Teilnehmenden ernst. "
                    "Das ist nicht nur ethisch richtig, sondern macht auch die Forschung besser.»",
            "medium": "Einige ethische Aspekte sind bedacht, andere fehlen. "
                      "Duflo: «Ihr habt Informed Consent, aber was passiert mit der Kontrollgruppe nach dem Experiment? "
                      "Ethik endet nicht mit der Datenerhebung.»",
            "low": "Die ethische Reflexion ist unzureichend. "
                   "Duflo: «Ihr experimentiert mit Menschen. Das erfordert systematische ethische Pruefung — "
                   "nicht als Pflichtaufgabe, sondern weil wir eine Verantwortung haben.»",
        },
    }

    templates = feedback_templates.get(criterion_key, {})
    if pct >= 75:
        fb = templates.get("high", "Gute Arbeit in diesem Bereich.")
    elif pct >= 50:
        fb = templates.get("medium", "Verbesserungspotenzial vorhanden.")
        fb = fb.replace("{weak}", weakest.label)
    else:
        fb = templates.get("low", "Hier besteht erheblicher Verbesserungsbedarf.")

    return fb


def score_experiment(responses: dict) -> ScorecardResult:
    """
    Score an experimental design.

    Parameters
    ----------
    responses : dict
        Mapping of criterion_key -> sub_dimension_key -> selected option key.
        Example: {"randomization": {"design_type": "rct", "assignment_mechanism": "cluster_random", ...}, ...}

    Returns
    -------
    ScorecardResult
    """
    criteria_results = []

    for crit_key, crit_def in CRITERIA.items():
        crit_responses = responses.get(crit_key, {})
        sub_results = []
        weighted_score = 0.0

        for sub_key, sub_def in crit_def["sub_dimensions"].items():
            selected = crit_responses.get(sub_key, "")
            raw_score = sub_def["scoring"].get(selected, 0)
            sub_results.append(
                SubDimensionResult(
                    label=sub_def["label"],
                    selected=selected,
                    score=raw_score,
                    max_score=5.0,
                    weight=sub_def["weight"],
                )
            )
            weighted_score += raw_score * sub_def["weight"]

        feedback = _criterion_feedback(crit_key, weighted_score, sub_results)

        criteria_results.append(
            CriterionResult(
                name=crit_def["name"],
                score=round(weighted_score, 2),
                max_score=5.0,
                weight=crit_def["weight"],
                sub_dimensions=sub_results,
                feedback=feedback,
            )
        )

    total = sum(c.score * c.weight for c in criteria_results)
    max_total = sum(c.max_score * c.weight for c in criteria_results)
    pct = (total / max_total * 100) if max_total > 0 else 0

    # Find top strength and weakness
    best = max(criteria_results, key=lambda c: c.score / c.max_score)
    worst = min(criteria_results, key=lambda c: c.score / c.max_score)

    summary = (
        f"Gesamtbewertung: {pct:.0f}% ({_grade(pct)}). "
        f"Staerkster Bereich: {best.name} ({best.score:.1f}/5). "
        f"Groesster Verbesserungsbedarf: {worst.name} ({worst.score:.1f}/5)."
    )

    return ScorecardResult(
        total_score=round(total, 2),
        max_score=round(max_total, 2),
        percentage=round(pct, 1),
        grade=_grade(pct),
        criteria=criteria_results,
        summary=summary,
        top_strength=best.name,
        top_weakness=worst.name,
    )


def get_criteria_options() -> dict:
    """Return all criteria with their sub-dimensions and options for the frontend."""
    result = {}
    for crit_key, crit_def in CRITERIA.items():
        subs = {}
        for sub_key, sub_def in crit_def["sub_dimensions"].items():
            subs[sub_key] = {
                "label": sub_def["label"],
                "options": {k: k.replace("_", " ").title() for k in sub_def["scoring"]},
            }
        result[crit_key] = {
            "name": crit_def["name"],
            "sub_dimensions": subs,
        }
    return result
