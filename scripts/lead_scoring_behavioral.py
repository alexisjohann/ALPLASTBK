#!/usr/bin/env python3
"""
Behavioral Lead Scoring — Helvetia Baloise
===========================================

Verhaltensbasiertes Lead-Scoring-Modell basierend auf dem EBF R-Score.

Formel:
    Lead Score = σ(Σ wᵢ·dᵢ + Σ γⱼₖ·dⱼ·dₖ)

    σ(x) = 1 / (1 + exp(-x))   → Output ∈ [0, 1]

    dᵢ: 5 Verhaltensdimensionen (je 0–1)
    wᵢ: Gewichte (aus Literatur, kalibrierbar)
    γⱼₖ: Wechselwirkungen (Komplementarität)

Dimensionen:
    d1: Dringlichkeit      — Hat der Lead gerade einen Anlass?
    d2: Default-Situation   — Was passiert wenn der Lead NICHTS tut?
    d3: Aufmerksamkeit      — Wie präsent ist unser Angebot?
    d4: Verlust-Sensibilität — Wie stark reagiert der Lead auf Verluste?
    d5: Soziale Bestätigung — Was machen andere?

Kategorien:
    Kalt:     0.0–0.3   → Automatisches Nurturing (14 Tage)
    Warm:     0.3–0.6   → Persönlicher Kontakt (7 Tage)
    Heiss:    0.6–0.8   → Sofortige Beratung (3 Tage)
    Siedend:  0.8–1.0   → Alles stehen lassen (24h)

Wissenschaftliche Basis:
    d1: Laibson (1997) — Hyperbolic Discounting, β ≈ 0.70
    d2: Madrian & Shea (2001) — Default Effect +35pp
    d3: Herhausen et al. (2019) — Firestorm Interaction, Effekt 1.43
    d4: Kahneman & Tversky (1979) — Loss Aversion λ ≈ 2.25
    d5: Cialdini (2001) — Social Proof

EBF Parameter-IDs:
    d1 → PAR-BEH-003 (β)
    d2 → PAR-INT-001 (E_default)
    d3 → PAR-DIG-001 (A_max)
    d4 → PAR-BEH-001 (λ)
    d5 → PAR-INT-002 (E_social_norm)
    γ  → PAR-COMP-001 bis PAR-COMP-008

Usage:
    python lead_scoring_behavioral.py --demo
    python lead_scoring_behavioral.py --lead '{"d1":0.8,"d2":0.7,"d3":0.4,"d4":0.9,"d5":0.3}'
    python lead_scoring_behavioral.py --batch leads.csv --output scored.csv
    python lead_scoring_behavioral.py --sensitivity
    python lead_scoring_behavioral.py --marco-sandra

Author: FehrAdvice & Partners AG / EBF Framework
Date: 2026-02-12
"""

import numpy as np
import json
import csv
import argparse
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from pathlib import Path


# =============================================================================
# PARAMETER (Literatur-basierte Defaults, kalibrierbar im Kickoff)
# =============================================================================

# Gewichte (wᵢ) — Literatur-Priors, werden im Projekt kalibriert
# Skaliert so, dass Marco ≈ 0.72 (Heiss) und Sandra ≈ 0.41 (Warm)
DEFAULT_WEIGHTS = {
    "d1_dringlichkeit":       0.60,  # Laibson (1997): β ≈ 0.70, starker Effekt
    "d2_default":             0.50,  # Madrian & Shea (2001): +35pp
    "d3_aufmerksamkeit":      0.40,  # Herhausen et al. (2019): Effekt 1.43
    "d4_verlust":             0.55,  # Kahneman & Tversky (1979): λ ≈ 2.25
    "d5_sozial":              0.35,  # Cialdini (2001): moderater Effekt
}

# Wechselwirkungen (γⱼₖ) — aus PAR-COMP-xxx, kalibrierbar
# Positiv = verstärkt sich, Negativ = schwächt sich ab
DEFAULT_INTERACTIONS = {
    ("d4_verlust", "d2_default"):        0.175,  # Verlust × kein Schutz → Handlungsdruck
    ("d1_dringlichkeit", "d3_aufmerksamkeit"): 0.125,  # Anlass × persönlicher Kontakt
    ("d5_sozial", "d4_verlust"):         0.10,   # Peers + Verlustangst
    ("d1_dringlichkeit", "d4_verlust"):  0.075,  # Zeitdruck × Verlustangst
}

# Bias-Term (Intercept) — wird im Backtesting kalibriert
DEFAULT_BIAS = -1.0  # Kalibriert für Marco ≈ 0.72, Sandra ≈ 0.41

# Kategorien
CATEGORIES = [
    (0.0, 0.3, "Kalt",    "Automatisches Nurturing",               "14 Tage"),
    (0.3, 0.6, "Warm",    "Persönlicher Kontakt, Bedarfsanalyse",  "7 Tage"),
    (0.6, 0.8, "Heiss",   "Sofortige Beratung, Offerte vorbereiten", "3 Tage"),
    (0.8, 1.0, "Siedend", "Alles stehen lassen, Senior-Berater:in", "24 Stunden"),
]

# Dimension-Labels (für Output)
DIMENSION_LABELS = {
    "d1_dringlichkeit":  "Dringlichkeit",
    "d2_default":        "Default-Situation",
    "d3_aufmerksamkeit": "Aufmerksamkeit",
    "d4_verlust":        "Verlust-Sensibilität",
    "d5_sozial":         "Soziale Bestätigung",
}


# =============================================================================
# CORE MODEL
# =============================================================================

def sigmoid(x: float) -> float:
    """Logistische Funktion: Output ∈ [0, 1]."""
    return 1.0 / (1.0 + np.exp(-x))


@dataclass
class LeadInput:
    """Input-Daten für einen Lead."""
    name: str = ""
    d1_dringlichkeit: float = 0.0    # 0 = kein Anlass, 1 = akut
    d2_default: float = 0.0          # 0 = starker Default dagegen, 1 = kein Default
    d3_aufmerksamkeit: float = 0.0   # 0 = kein Kontakt, 1 = persönliche Empfehlung
    d4_verlust: float = 0.0          # 0 = kein Verlustrisiko, 1 = akuter Verlust
    d5_sozial: float = 0.0           # 0 = keine soziale Bestätigung, 1 = starke Norm

    def to_dict(self) -> Dict[str, float]:
        return {
            "d1_dringlichkeit": self.d1_dringlichkeit,
            "d2_default": self.d2_default,
            "d3_aufmerksamkeit": self.d3_aufmerksamkeit,
            "d4_verlust": self.d4_verlust,
            "d5_sozial": self.d5_sozial,
        }

    def dimensions(self) -> np.ndarray:
        return np.array([
            self.d1_dringlichkeit,
            self.d2_default,
            self.d3_aufmerksamkeit,
            self.d4_verlust,
            self.d5_sozial,
        ])


@dataclass
class LeadScore:
    """Ergebnis des Lead Scorings."""
    score: float
    category: str
    action: str
    sla: str
    drivers: List[Tuple[str, float]]     # Top-Treiber [(name, beitrag)]
    interactions: List[Tuple[str, float]] # Aktive Wechselwirkungen
    raw_logit: float                      # Vor Sigmoid

    def to_dict(self) -> Dict:
        return {
            "score": round(self.score, 3),
            "category": self.category,
            "action": self.action,
            "sla": self.sla,
            "drivers": [{"dimension": d, "contribution": round(c, 3)} for d, c in self.drivers],
            "interactions": [{"pair": p, "contribution": round(c, 3)} for p, c in self.interactions],
            "raw_logit": round(self.raw_logit, 3),
        }


def score_lead(
    lead: LeadInput,
    weights: Dict[str, float] = None,
    interactions: Dict[Tuple[str, str], float] = None,
    bias: float = None,
) -> LeadScore:
    """
    Berechnet den Behavioral Lead Score.

    Lead Score = σ(bias + Σ wᵢ·dᵢ + Σ γⱼₖ·dⱼ·dₖ)
    """
    w = weights or DEFAULT_WEIGHTS
    gamma = interactions or DEFAULT_INTERACTIONS
    b = bias if bias is not None else DEFAULT_BIAS

    dims = lead.to_dict()

    # Lineare Terme: wᵢ · dᵢ
    linear_terms = {}
    logit = b
    for key, weight in w.items():
        value = dims.get(key, 0.0)
        contribution = weight * value
        linear_terms[key] = contribution
        logit += contribution

    # Interaktionsterme: γⱼₖ · dⱼ · dₖ
    interaction_terms = {}
    for (k1, k2), gamma_val in gamma.items():
        v1 = dims.get(k1, 0.0)
        v2 = dims.get(k2, 0.0)
        contribution = gamma_val * v1 * v2
        if abs(contribution) > 0.01:  # Nur relevante anzeigen
            pair_label = f"{DIMENSION_LABELS.get(k1, k1)} × {DIMENSION_LABELS.get(k2, k2)}"
            interaction_terms[pair_label] = contribution
        logit += contribution

    # Sigmoid → Score ∈ [0, 1]
    score = sigmoid(logit)

    # Kategorie bestimmen
    category, action, sla = "Kalt", "Nurturing", "14 Tage"
    for low, high, cat, act, sl in CATEGORIES:
        if low <= score < high or (cat == "Siedend" and score >= high):
            category, action, sla = cat, act, sl
            if score >= low:
                break

    # Top-Treiber sortiert nach Beitrag
    drivers = sorted(
        [(DIMENSION_LABELS.get(k, k), v) for k, v in linear_terms.items()],
        key=lambda x: abs(x[1]),
        reverse=True
    )

    # Interaktionen sortiert
    active_interactions = sorted(
        interaction_terms.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    return LeadScore(
        score=score,
        category=category,
        action=action,
        sla=sla,
        drivers=drivers,
        interactions=active_interactions,
        raw_logit=logit,
    )


# =============================================================================
# MONTE CARLO (Unsicherheitsquantifizierung)
# =============================================================================

def score_lead_mc(
    lead: LeadInput,
    n: int = 10000,
    weight_uncertainty: float = 0.15,
    seed: int = 42,
) -> Dict:
    """
    Monte-Carlo Lead Scoring mit Unsicherheitspropagation.

    Variiert Gewichte und Interaktionen innerhalb ihrer Unsicherheit.
    """
    rng = np.random.default_rng(seed)

    scores = []
    for _ in range(n):
        # Gewichte mit Unsicherheit
        noisy_weights = {
            k: max(0, v + rng.normal(0, weight_uncertainty * v))
            for k, v in DEFAULT_WEIGHTS.items()
        }
        # Interaktionen mit Unsicherheit
        noisy_interactions = {
            k: v + rng.normal(0, weight_uncertainty * abs(v))
            for k, v in DEFAULT_INTERACTIONS.items()
        }
        # Bias mit Unsicherheit
        noisy_bias = DEFAULT_BIAS + rng.normal(0, 0.3)

        result = score_lead(lead, noisy_weights, noisy_interactions, noisy_bias)
        scores.append(result.score)

    scores = np.array(scores)

    return {
        "mean": float(scores.mean()),
        "median": float(np.median(scores)),
        "std": float(scores.std()),
        "ci80": (float(np.percentile(scores, 10)), float(np.percentile(scores, 90))),
        "ci95": (float(np.percentile(scores, 2.5)), float(np.percentile(scores, 97.5))),
        "p_heiss": float((scores >= 0.6).mean()),
        "p_siedend": float((scores >= 0.8).mean()),
    }


# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

def sensitivity_analysis(base_lead: LeadInput = None) -> List[Dict]:
    """
    Sensitivitätsanalyse: Welche Dimension hat den grössten Hebel?

    Variiert jede Dimension von 0→1 bei sonst fixen Werten.
    """
    if base_lead is None:
        # Baseline: alle Dimensionen auf 0.5
        base_lead = LeadInput(
            name="Baseline",
            d1_dringlichkeit=0.5,
            d2_default=0.5,
            d3_aufmerksamkeit=0.5,
            d4_verlust=0.5,
            d5_sozial=0.5,
        )

    base_score = score_lead(base_lead).score
    results = []

    dim_keys = ["d1_dringlichkeit", "d2_default", "d3_aufmerksamkeit",
                "d4_verlust", "d5_sozial"]

    for key in dim_keys:
        # Score bei d=0
        lead_low = LeadInput(**{**base_lead.to_dict(), key: 0.0, "name": ""})
        score_low = score_lead(lead_low).score

        # Score bei d=1
        lead_high = LeadInput(**{**base_lead.to_dict(), key: 1.0, "name": ""})
        score_high = score_lead(lead_high).score

        swing = score_high - score_low

        results.append({
            "dimension": DIMENSION_LABELS.get(key, key),
            "key": key,
            "score_at_0": round(score_low, 3),
            "score_at_1": round(score_high, 3),
            "swing": round(swing, 3),
            "category_at_0": score_lead(lead_low).category,
            "category_at_1": score_lead(lead_high).category,
        })

    # Nach Swing sortieren
    results.sort(key=lambda x: abs(x["swing"]), reverse=True)
    return results


# =============================================================================
# BATCH SCORING
# =============================================================================

def score_batch_csv(input_path: str, output_path: str = None):
    """
    Batch-Scoring aus CSV.

    CSV-Format:
        name,d1_dringlichkeit,d2_default,d3_aufmerksamkeit,d4_verlust,d5_sozial
        Marco,0.85,0.80,0.40,0.90,0.30
        Sandra,0.20,0.15,0.60,0.15,0.25
    """
    leads = []
    with open(input_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lead = LeadInput(
                name=row.get("name", ""),
                d1_dringlichkeit=float(row.get("d1_dringlichkeit", 0)),
                d2_default=float(row.get("d2_default", 0)),
                d3_aufmerksamkeit=float(row.get("d3_aufmerksamkeit", 0)),
                d4_verlust=float(row.get("d4_verlust", 0)),
                d5_sozial=float(row.get("d5_sozial", 0)),
            )
            leads.append(lead)

    results = []
    for lead in leads:
        result = score_lead(lead)
        results.append({
            "name": lead.name,
            "score": round(result.score, 3),
            "category": result.category,
            "action": result.action,
            "sla": result.sla,
            "top_driver": result.drivers[0][0] if result.drivers else "",
            **lead.to_dict(),
        })

    if output_path:
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Ergebnis gespeichert: {output_path}")

    return results


# =============================================================================
# DEMO: Marco vs. Sandra
# =============================================================================

def demo_marco_sandra():
    """Reproduziert das Marco-vs-Sandra-Beispiel aus dem Proposal."""

    print("\n" + "=" * 70)
    print("BEHAVIORAL LEAD SCORING — Marco vs. Sandra")
    print("=" * 70)

    # Marco: 42, Zürich, MFZ-Versicherung
    marco = LeadInput(
        name="Marco (42, ZH, Motorfahrzeug)",
        d1_dringlichkeit=0.85,      # Vertrag läuft in 3 Wochen aus
        d2_default=0.80,            # Keine automatische Verlängerung
        d3_aufmerksamkeit=0.40,     # Nur Website-Besuch, kein persönlicher Kontakt
        d4_verlust=0.90,            # Schadenfall vor 2 Monaten
        d5_sozial=0.30,             # Keine Peer-Empfehlung
    )

    # Sandra: 38, Basel, Hausrat
    sandra = LeadInput(
        name="Sandra (38, BS, Hausrat)",
        d1_dringlichkeit=0.20,      # Kein konkreter Anlass
        d2_default=0.15,            # Bestehende Police bei Konkurrent (starker Default)
        d3_aufmerksamkeit=0.60,     # Messe-Kontakt + Offerte angefordert
        d4_verlust=0.15,            # Kein Schadenfall
        d5_sozial=0.25,             # Keine Peer-Empfehlung
    )

    for lead in [marco, sandra]:
        result = score_lead(lead)
        mc = score_lead_mc(lead)

        print(f"\n{'─' * 70}")
        print(f"  {lead.name}")
        print(f"{'─' * 70}")

        # Dimensionen
        print(f"\n  Dimensionen:")
        for key, label in DIMENSION_LABELS.items():
            val = lead.to_dict()[key]
            bar = "█" * int(val * 20) + "░" * (20 - int(val * 20))
            print(f"    {label:<24} {bar} {val:.2f}")

        # Score
        print(f"\n  SCORE: {result.score:.2f} → {result.category}")
        print(f"  Monte Carlo: {mc['mean']:.2f} [{mc['ci80'][0]:.2f}, {mc['ci80'][1]:.2f}] (80% CI)")
        print(f"  P(Heiss+): {mc['p_heiss']:.0%}  |  P(Siedend): {mc['p_siedend']:.0%}")

        # Top-Treiber
        print(f"\n  Top-Treiber:")
        for dim, contrib in result.drivers[:3]:
            direction = "↑" if contrib > 0 else "↓"
            print(f"    {direction} {dim:<24} {contrib:+.3f}")

        # Wechselwirkungen
        if result.interactions:
            print(f"\n  Wechselwirkungen:")
            for pair, contrib in result.interactions:
                print(f"    ⟷ {pair:<40} {contrib:+.3f}")

        # Empfehlung
        print(f"\n  Empfehlung: {result.action}")
        print(f"  SLA: {result.sla}")

    # Vergleich
    marco_score = score_lead(marco).score
    sandra_score = score_lead(sandra).score

    print(f"\n{'=' * 70}")
    print(f"  VERGLEICH")
    print(f"{'=' * 70}")
    print(f"  Marco:  {marco_score:.2f} → {score_lead(marco).category}")
    print(f"  Sandra: {sandra_score:.2f} → {score_lead(sandra).category}")
    print(f"\n  Klassisch: Sandra (53 Pkt) > Marco (25 Pkt)")
    print(f"  Behavioral: Marco ({marco_score:.2f}) > Sandra ({sandra_score:.2f})")
    print(f"\n  → Priorisierung umgekehrt. Marco zuerst.")
    print(f"{'=' * 70}")


def demo_sensitivity():
    """Sensitivitätsanalyse mit Visualisierung."""

    print("\n" + "=" * 70)
    print("SENSITIVITÄTSANALYSE — Welche Dimension hat den grössten Hebel?")
    print("=" * 70)
    print("\n  Baseline: Alle Dimensionen = 0.5")
    print(f"  Baseline Score: {score_lead(LeadInput(d1_dringlichkeit=0.5, d2_default=0.5, d3_aufmerksamkeit=0.5, d4_verlust=0.5, d5_sozial=0.5)).score:.3f}")

    results = sensitivity_analysis()

    print(f"\n  {'Dimension':<28} {'0→1 Swing':<12} {'bei d=0':<10} {'bei d=1':<10} {'Kat. 0→1'}")
    print(f"  {'─' * 78}")

    for r in results:
        bar = "█" * int(r["swing"] * 40)
        print(f"  {r['dimension']:<28} {bar:<12} {r['score_at_0']:.3f}     {r['score_at_1']:.3f}     {r['category_at_0']}→{r['category_at_1']}")

    print(f"\n  → Stärkster Hebel: {results[0]['dimension']} (Swing: {results[0]['swing']:.3f})")
    print(f"  → Schwächster Hebel: {results[-1]['dimension']} (Swing: {results[-1]['swing']:.3f})")


def demo():
    """Vollständige Demo."""
    demo_marco_sandra()
    print()
    demo_sensitivity()


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Behavioral Lead Scoring — Helvetia Baloise",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python lead_scoring_behavioral.py --demo
  python lead_scoring_behavioral.py --marco-sandra
  python lead_scoring_behavioral.py --sensitivity
  python lead_scoring_behavioral.py --lead '{"d1":0.8,"d2":0.7,"d3":0.4,"d4":0.9,"d5":0.3}'
  python lead_scoring_behavioral.py --batch leads.csv --output scored.csv
        """
    )

    parser.add_argument("--demo", action="store_true", help="Vollständige Demo")
    parser.add_argument("--marco-sandra", action="store_true", help="Marco vs. Sandra Beispiel")
    parser.add_argument("--sensitivity", action="store_true", help="Sensitivitätsanalyse")
    parser.add_argument("--lead", type=str, help="Einzelner Lead als JSON")
    parser.add_argument("--batch", type=str, help="CSV-Datei mit Leads")
    parser.add_argument("--output", type=str, help="Output CSV-Datei")
    parser.add_argument("--json", action="store_true", help="Output als JSON")
    parser.add_argument("--mc", action="store_true", help="Monte Carlo Unsicherheit")
    parser.add_argument("--n-mc", type=int, default=10000, help="Monte Carlo Samples")

    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.marco_sandra:
        demo_marco_sandra()
    elif args.sensitivity:
        demo_sensitivity()
    elif args.lead:
        data = json.loads(args.lead)
        lead = LeadInput(
            name=data.get("name", "Lead"),
            d1_dringlichkeit=data.get("d1", data.get("d1_dringlichkeit", 0)),
            d2_default=data.get("d2", data.get("d2_default", 0)),
            d3_aufmerksamkeit=data.get("d3", data.get("d3_aufmerksamkeit", 0)),
            d4_verlust=data.get("d4", data.get("d4_verlust", 0)),
            d5_sozial=data.get("d5", data.get("d5_sozial", 0)),
        )
        result = score_lead(lead)

        if args.json:
            output = result.to_dict()
            if args.mc:
                output["monte_carlo"] = score_lead_mc(lead, n=args.n_mc)
            print(json.dumps(output, indent=2))
        else:
            print(f"\nScore: {result.score:.3f} → {result.category}")
            print(f"Aktion: {result.action} (SLA: {result.sla})")
            if args.mc:
                mc = score_lead_mc(lead, n=args.n_mc)
                print(f"MC: {mc['mean']:.3f} [{mc['ci80'][0]:.3f}, {mc['ci80'][1]:.3f}]")
    elif args.batch:
        results = score_batch_csv(args.batch, args.output)
        if not args.output:
            for r in results:
                print(f"{r['name']:<30} {r['score']:.3f}  {r['category']:<8}  {r['action']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
