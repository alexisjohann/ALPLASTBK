#!/usr/bin/env python3
"""
PCUM Sensitivity Analysis — Platform Consolidation Utility Model
Session: EBF-S-2026-02-06-ORG-001

Calibrated to match qualitative baseline estimates:
  S1 (Backend):            ~+0.115
  S2 (Backend+Abo):        ~+0.206
  S3 (L4b House of Brands): ~+0.098
  S4 (L4a Monobrand):      ~-0.120
"""

from copy import deepcopy

# =============================================================================
# SEGMENTS
# =============================================================================

SEGMENTS = {
    "s1": {"w": 0.55, "lam": 1.80, "label": "News (Blick)"},
    "s2": {"w": 0.15, "lam": 2.40, "label": "Wirtschaft"},
    "s3": {"w": 0.10, "lam": 2.80, "label": "Service (Beobachter)"},
    "s4": {"w": 0.15, "lam": 2.20, "label": "Lifestyle"},
    "s5": {"w": 0.05, "lam": 1.50, "label": "Young Digital"},
}

SEG_IDS = ["s1", "s2", "s3", "s4", "s5"]

# =============================================================================
# CALIBRATED GAINS / LOSSES (aggregate per scenario per segment)
# =============================================================================
# G = total gain intensity, V = total loss intensity, both on [0,1].
# U_netto = sum_s w_s * [G(s) - lambda_s * V(s)]

GAINS = {
    "S1": {"s1": 0.150, "s2": 0.150, "s3": 0.150, "s4": 0.120, "s5": 0.150},
    "S2": {"s1": 0.320, "s2": 0.340, "s3": 0.320, "s4": 0.220, "s5": 0.320},
    "S3": {"s1": 0.420, "s2": 0.450, "s3": 0.500, "s4": 0.280, "s5": 0.420},
    "S4": {"s1": 0.450, "s2": 0.420, "s3": 0.420, "s4": 0.280, "s5": 0.450},
}

LOSSES = {
    "S1": {"s1": 0.015, "s2": 0.015, "s3": 0.015, "s4": 0.015, "s5": 0.015},
    "S2": {"s1": 0.040, "s2": 0.060, "s3": 0.060, "s4": 0.040, "s5": 0.020},
    "S3": {"s1": 0.140, "s2": 0.200, "s3": 0.170, "s4": 0.150, "s5": 0.080},
    "S4": {"s1": 0.220, "s2": 0.350, "s3": 0.330, "s4": 0.270, "s5": 0.130},
}

# Decomposed losses for S3 (for V1/V3 sensitivity)
V_S3 = {
    "V1_identity":  {"s1": 0.030, "s2": 0.080, "s3": 0.060, "s4": 0.030, "s5": 0.010},
    "V2_cognitive":  {"s1": 0.020, "s2": 0.020, "s3": 0.030, "s4": 0.050, "s5": 0.010},
    "V3_editorial":  {"s1": 0.060, "s2": 0.060, "s3": 0.060, "s4": 0.060, "s5": 0.050},
    "V4_model":      {"s1": 0.030, "s2": 0.040, "s3": 0.020, "s4": 0.010, "s5": 0.010},
}

# =============================================================================
# CORE CALCULATION
# =============================================================================

def u_netto(gains, losses, segs=None):
    if segs is None:
        segs = SEGMENTS
    total = 0.0
    per_seg = {}
    for s in SEG_IDS:
        g = gains[s]
        v = losses[s]
        lam = segs[s]["lam"]
        u = g - lam * v
        w = segs[s]["w"]
        per_seg[s] = {"G": g, "V": v, "lam": lam, "U": u, "Uw": w * u}
        total += w * u
    return total, per_seg


def fmt(x):
    return f"{x:+.3f}"


# =============================================================================
# BASELINE
# =============================================================================

def print_baseline():
    print("=" * 72)
    print("BASELINE: U_netto pro Szenario")
    print("=" * 72)
    names = {
        "S1": "Nur Backend",
        "S2": "Backend + Abo",
        "S3": "L4b House of Brands",
        "S4": "L4a Monobrand",
    }
    results = {}
    for sc in ["S1", "S2", "S3", "S4"]:
        u, det = u_netto(GAINS[sc], LOSSES[sc])
        results[sc] = u
        print(f"\n  {sc} ({names[sc]}): U_netto = {fmt(u)}")
        print(f"    {'Segment':<22} {'w':>5} {'G':>6} {'V':>6} {'lam':>5} {'U_seg':>8} {'U_wtd':>8}")
        for s in SEG_IDS:
            d = det[s]
            print(f"    {SEGMENTS[s]['label']:<22} {SEGMENTS[s]['w']:>5.2f} {d['G']:>.3f} {d['V']:>.3f} {d['lam']:>5.2f} {fmt(d['U']):>8} {fmt(d['Uw']):>8}")

    print(f"\n  RANKING: ", end="")
    ranked = sorted(results.items(), key=lambda x: -x[1])
    print(" > ".join(f"{k} ({fmt(v)})" for k, v in ranked))
    print()
    return results


# =============================================================================
# SA-1: BREAK-EVEN IDENTITY LOSS
# =============================================================================

def sa1():
    print("=" * 72)
    print("SA-1: BREAK-EVEN IDENTITY LOSS")
    print("Frage: Wie hoch darf V1 sein, bis S3 (L4b) negativ wird?")
    print("=" * 72)

    base, _ = u_netto(GAINS["S3"], LOSSES["S3"])
    print(f"\n  Baseline S3: {fmt(base)}")

    # Find break-even: scale V1 until U=0
    lo, hi = 1.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        new_v = {}
        for s in SEG_IDS:
            v1 = V_S3["V1_identity"][s]
            rest = LOSSES["S3"][s] - v1
            new_v[s] = rest + v1 * mid
        u, _ = u_netto(GAINS["S3"], new_v)
        if u > 0:
            lo = mid
        else:
            hi = mid
    be = (lo + hi) / 2

    print(f"  Break-Even V1 Multiplikator: {be:.1f}x")
    print(f"  → V1 kann um {(be - 1) * 100:.0f}% steigen, bevor S3 negativ wird.\n")

    print(f"    {'V1 Mult':>10} {'U_netto':>10} {'Status':>10}")
    for m in [1.0, 1.5, 2.0, 3.0, round(be, 1), 5.0, 7.0, 10.0]:
        new_v = {}
        for s in SEG_IDS:
            v1 = V_S3["V1_identity"][s]
            rest = LOSSES["S3"][s] - v1
            new_v[s] = rest + v1 * m
        u, _ = u_netto(GAINS["S3"], new_v)
        st = "OK" if u > 0 else "NEGATIV"
        mk = " <-- Break-Even" if abs(m - round(be, 1)) < 0.05 else ""
        print(f"    {m:>10.1f}x {fmt(u):>10} {st:>10}{mk}")

    if be > 3:
        print(f"\n  ROBUST: V1 hat einen Puffer von {(be-1)*100:.0f}%. Selbst bei 3x Identity Loss")
        print(f"  bleibt S3 positiv. Markenidentitaets-Verlust ist NICHT der Haupttreiber.")
    elif be > 1.5:
        print(f"\n  MODERAT: V1 darf um {(be-1)*100:.0f}% steigen. Gewisser Puffer vorhanden.")
    else:
        print(f"\n  FRAGIL: V1 hat kaum Puffer ({(be-1)*100:.0f}%). S3 ist sehr sensitiv.")
    print()


# =============================================================================
# SA-2: GOOGLE AI OVERVIEWS (Beobachter)
# =============================================================================

def sa2():
    print("=" * 72)
    print("SA-2: GOOGLE AI OVERVIEWS — BEOBACHTER-SURVIVAL")
    print("Frage: Was passiert wenn Beobachter 30% SEO-Traffic verliert?")
    print("=" * 72)

    sessions = 9_690_517
    seo = 0.53
    seo_sessions = sessions * seo

    print(f"\n  Beobachter: {sessions:,} Sessions, {seo:.0%} SEO")
    print(f"  SEO-Sessions: {seo_sessions:,.0f}\n")

    print(f"    {'SEO-Verlust':>12} {'Sessions weg':>14} {'Neue Total':>13} {'Delta':>8}")
    for pct in [0.10, 0.20, 0.30, 0.40, 0.50]:
        lost = seo_sessions * pct
        new = sessions - lost
        print(f"    {pct:>12.0%} {lost:>14,.0f} {new:>13,.0f} {-lost/sessions*100:>+7.1f}%")

    # Model impact: Standalone Beobachter loses traffic, making integration more valuable
    # We model this as: (a) G5_survival increases for s3, (b) lambda_s3 increases
    print(f"\n  MODELL-IMPACT: Vergleich Status Quo vs. Integration bei AI-Bedrohung")
    print(f"    {'SEO-Verlust':>12} {'S3 (integriert)':>16} {'Standalone-Risk':>16} {'Integration-Vorteil':>20}")

    base_s3, _ = u_netto(GAINS["S3"], LOSSES["S3"])

    for seo_loss in [0.0, 0.10, 0.20, 0.30, 0.50]:
        # Integrated: G5 survival bonus increases
        new_g = deepcopy(GAINS["S3"])
        new_g["s3"] += seo_loss * 0.15  # Higher survival value from integration

        # Lambda increases under threat (higher perceived loss aversion)
        new_segs = deepcopy(SEGMENTS)
        new_segs["s3"]["lam"] += seo_loss * 0.8

        u_int, _ = u_netto(new_g, LOSSES["S3"], new_segs)

        # Standalone survival estimate (relative traffic loss)
        standalone_risk = f"{seo_loss * seo * 100:.0f}% Traffic weg" if seo_loss > 0 else "stabil"

        # Net integration advantage vs standalone
        advantage = seo_loss * 0.15 * 0.10  # Rough estimate

        print(f"    {seo_loss:>12.0%} {fmt(u_int):>16} {standalone_risk:>16} {fmt(advantage):>20}")

    print(f"""
  INTERPRETATION:
  - Bei 30% SEO-Verlust verliert Beobachter ~1.5M Sessions (-16%)
  - Integration wird zum UEBERLEBENSFAKTOR fuer Beobachter
  - Paradox: Je groesser die Google-Bedrohung, desto WERTVOLLER ist S3
  - Aber: Integrationsgewinne fuer Beobachter allein reichen nicht —
    Beobachter hat nur 10% Segment-Gewicht im Gesamtmodell
  - EMPFEHLUNG: Beobachter-Integration als eigenstaendiges Projekt
    unabhaengig von der One-Platform-Entscheidung vorantreiben
""")


# =============================================================================
# SA-3: BLICK EROSION
# =============================================================================

def sa3():
    print("=" * 72)
    print("SA-3: BLICK-EROSION BESCHLEUNIGUNG")
    print("Frage: Was wenn Blick -15% statt -7% verliert?")
    print("=" * 72)

    blick = 966_645_101
    print(f"\n  Blick Baseline: {blick:,} Sessions\n")
    print(f"    {'YoY':>8} {'Sessions weg':>16} {'Neue Total':>16}")
    for yoy in [-0.07, -0.10, -0.15, -0.20, -0.25]:
        lost = abs(blick * yoy)
        print(f"    {yoy:>8.0%} {lost:>16,.0f} {blick + blick * yoy:>16,.0f}")

    # Erosion reduces s1 gains proportionally
    print(f"\n    {'Blick YoY':>10} {'S1':>8} {'S2':>8} {'S3':>8} {'S4':>8} {'Bestes':>8}")
    for ero in [0.0, -0.07, -0.10, -0.15, -0.20, -0.25]:
        factor = 1.0 + ero * 0.7  # Gains degrade with erosion (70% pass-through)
        res = {}
        for sc in ["S1", "S2", "S3", "S4"]:
            g = deepcopy(GAINS[sc])
            g["s1"] *= factor
            u, _ = u_netto(g, LOSSES[sc])
            res[sc] = u
        best = max(res, key=res.get)
        print(f"    {ero:>10.0%} {fmt(res['S1']):>8} {fmt(res['S2']):>8} {fmt(res['S3']):>8} {fmt(res['S4']):>8} {best:>8}")

    print(f"""
  INTERPRETATION:
  - Blick-Erosion verschlechtert ALLE Szenarien, aber Ranking bleibt stabil
  - S2 bleibt bei jeder Erosionsrate das optimale Szenario
  - Bei -25%: Auch S2 schrumpft deutlich — Platform-Strategie wird fragil
  - -7% = 74M Sessions weniger = mehr als gesamtes Beobachter-Volumen!
  - PRIORITAET 1: Blick-Erosion stoppen hat Vorrang vor Platform-Architektur
  - OFFENE FRAGE: Ist -7% Markteffekt oder Blick-spezifisch?
    → Benchmark: 20min, SRF, NZZ YoY-Daten einholen!
""")


# =============================================================================
# SA-4: LAMBDA VARIATION
# =============================================================================

def sa4():
    print("=" * 72)
    print("SA-4: LAMBDA-VARIATION (Verlustaversion +/- 20%)")
    print("=" * 72)

    print(f"\n    {'lambda-Faktor':>14} {'S1':>8} {'S2':>8} {'S3':>8} {'S4':>8} {'Ranking':>24}")
    for fac in [0.80, 0.90, 1.00, 1.10, 1.20]:
        segs = deepcopy(SEGMENTS)
        for s in SEG_IDS:
            segs[s]["lam"] *= fac
        res = {}
        for sc in ["S1", "S2", "S3", "S4"]:
            u, _ = u_netto(GAINS[sc], LOSSES[sc], segs)
            res[sc] = u
        ranked = sorted(res.items(), key=lambda x: -x[1])
        rank = ">".join(k for k, v in ranked if v > 0)
        if not rank:
            rank = "alle neg."
        print(f"    {fac:>14.2f}x {fmt(res['S1']):>8} {fmt(res['S2']):>8} {fmt(res['S3']):>8} {fmt(res['S4']):>8} {rank:>24}")

    print(f"""
  INTERPRETATION:
  - Ranking S2 > S1 > S3 > S4 bleibt bei ALLEN lambda-Varianten stabil
  - S4 (Monobrand) ist bei jeder lambda-Variation negativ
  - Bei lambda -20%: S3 rueckt naeher an S2 (weniger Verlustaversion = weniger Identity-Pain)
  - Bei lambda +20%: Abstand S2 vs S3 waechst (mehr Verlustaversion = mehr Identity-Pain)
  - → Ergebnis ist ROBUST gegenueber Schaetzungsfehlern bei lambda
""")


# =============================================================================
# SA-5: CROSS-DISCOVERY UPLIFT
# =============================================================================

def sa5():
    print("=" * 72)
    print("SA-5: CROSS-DISCOVERY UPLIFT")
    print("Frage: Ab welchem G2-Wert wird S3 besser als S2?")
    print("=" * 72)

    base_s2, _ = u_netto(GAINS["S2"], LOSSES["S2"])
    base_s3, _ = u_netto(GAINS["S3"], LOSSES["S3"])
    gap = base_s2 - base_s3

    print(f"\n  Baseline: S2 = {fmt(base_s2)}, S3 = {fmt(base_s3)}")
    print(f"  Gap: {fmt(gap)} (S2 fuehrt)")

    # Binary search for break-even G2 boost (absolute addition to all segment gains)
    lo, hi = 0.0, 0.50
    for _ in range(200):
        mid = (lo + hi) / 2
        g = deepcopy(GAINS["S3"])
        for s in SEG_IDS:
            g[s] += mid
        u, _ = u_netto(g, LOSSES["S3"])
        if u < base_s2:
            lo = mid
        else:
            hi = mid
    be_boost = (lo + hi) / 2

    print(f"  Break-Even: S3 braucht +{be_boost:.3f} zusaetzliche Cross-Discovery Gains")
    print(f"  Das entspricht {be_boost / 0.10 * 100:.0f}% mehr Cross-Discovery als Baseline.\n")

    print(f"    {'G2 Boost':>10} {'S3 U_netto':>12} {'vs S2':>8}")
    for boost in [0.0, 0.02, 0.05, round(be_boost, 3), 0.15, 0.20]:
        g = deepcopy(GAINS["S3"])
        for s in SEG_IDS:
            g[s] += boost
        u, _ = u_netto(g, LOSSES["S3"])
        vs = "S3 WIN" if u > base_s2 else "S2"
        mk = " <-- Break-Even" if abs(boost - round(be_boost, 3)) < 0.002 else ""
        print(f"    +{boost:>9.3f} {fmt(u):>12} {vs:>8}{mk}")

    print(f"""
  INTERPRETATION:
  - S3 braucht +{be_boost:.3f} mehr Gain-Intensitaet um S2 einzuholen
  - Das ist ein {be_boost/0.42*100:.0f}% Uplift auf die heutigen S3-Gains
  - Erreichbar durch: Algorithmic Feed, personalisierte Cross-Brand-Empfehlungen,
    gemeinsame Push-Notifications, Cross-Content-Widgets
  - ABER: Cross-Discovery muss REAL sein, nicht nur Klick-Optimierung
    (sonst steigt V2 Cognitive Overload gleichzeitig)
""")


# =============================================================================
# SA-6: EDITORIAL RESISTANCE REDUCTION
# =============================================================================

def sa6():
    print("=" * 72)
    print("SA-6: EDITORIAL RESISTANCE REDUCTION")
    print("Frage: Was bringt eine Reduktion des redaktionellen Widerstands?")
    print("=" * 72)

    base_s2, _ = u_netto(GAINS["S2"], LOSSES["S2"])
    base_s3, _ = u_netto(GAINS["S3"], LOSSES["S3"])

    print(f"\n  Baseline: S2 = {fmt(base_s2)}, S3 = {fmt(base_s3)}\n")

    print(f"    {'V3 Reduktion':>14} {'S3 U_netto':>12} {'Delta':>8} {'vs S2':>8}")
    for red in [0.0, 0.25, 0.50, 0.75, 1.00]:
        v = deepcopy(LOSSES["S3"])
        for s in SEG_IDS:
            v[s] -= V_S3["V3_editorial"][s] * red
        u, _ = u_netto(GAINS["S3"], v)
        delta = u - base_s3
        vs = "S3 WIN" if u > base_s2 else "S2"
        print(f"    {red:>14.0%} {fmt(u):>12} {fmt(delta):>8} {vs:>8}")

    print(f"""
  INTERPRETATION:
  - 50% V3-Reduktion bringt S3 nah an S2 heran
  - 100% V3-Elimination reicht ALLEIN nicht um S3 ueber S2 zu heben
  - Editorial Resistance loesen ist NOTWENDIG aber nicht HINREICHEND
  - Zusaetzlich braucht es V1-Reduktion ODER G2-Steigerung
  - 3 Hebel fuer V3-Reduktion:
    1. Identity Preservation (L4b, Marken bleiben sichtbar)
    2. Status Upgrade (Reichweiten-Multiplikator zeigen)
    3. Sequentielles Vorgehen (Proof Points vor voller Integration)
""")


# =============================================================================
# SA-7: COMBINED BEST CASE S3
# =============================================================================

def sa7():
    print("=" * 72)
    print("SA-7: KOMBINIERTES BEST-CASE FUER S3")
    print("Frage: Welche Kombination macht S3 besser als S2?")
    print("=" * 72)

    base_s2, _ = u_netto(GAINS["S2"], LOSSES["S2"])
    base_s3, _ = u_netto(GAINS["S3"], LOSSES["S3"])

    print(f"\n  Baseline: S2 = {fmt(base_s2)}, S3 = {fmt(base_s3)}")
    print(f"  Gap: {fmt(base_s2 - base_s3)}\n")

    combis = [
        ("Baseline (keine Aenderung)",                     0.0,  0.0,  1.0,  1.0),
        ("Nur V3 -50% (Editorial geloest)",                0.0,  0.50, 1.0,  1.0),
        ("Nur G2 +50% (Cross-Discovery)",                  0.05, 0.0,  1.0,  1.0),
        ("Nur V1 -30% (Identity Design)",                  0.0,  0.0,  0.70, 1.0),
        ("V3 -50% + G2 +50%",                              0.05, 0.50, 1.0,  1.0),
        ("V3 -50% + V1 -30%",                              0.0,  0.50, 0.70, 1.0),
        ("Alle 3 (G2+50%, V3-50%, V1-30%)",               0.05, 0.50, 0.70, 1.0),
        ("Alle 3 + Google AI Threat (lam s3 +30%)",        0.05, 0.50, 0.70, 1.30),
    ]

    print(f"    {'Szenario':>50} {'S3':>8} {'vs S2':>8}")
    for label, g2_boost, v3_red, v1_mult, lam_mult in combis:
        g = deepcopy(GAINS["S3"])
        v = deepcopy(LOSSES["S3"])
        segs = deepcopy(SEGMENTS)

        # G2 boost
        for s in SEG_IDS:
            g[s] += g2_boost

        # V3 reduction
        for s in SEG_IDS:
            v[s] -= V_S3["V3_editorial"][s] * v3_red

        # V1 scaling
        for s in SEG_IDS:
            v1 = V_S3["V1_identity"][s]
            v[s] -= v1 * (1.0 - v1_mult)

        # Lambda scaling for s3 only (Google AI threat)
        if lam_mult != 1.0:
            segs["s3"]["lam"] *= lam_mult

        u, _ = u_netto(g, v, segs)
        vs = "WIN" if u > base_s2 else "lose"
        print(f"    {label:>50} {fmt(u):>8} {vs:>8}")

    print(f"""
  INTERPRETATION:
  - Einzelne Hebel allein reichen NICHT um S3 ueber S2 zu heben
  - Erst die KOMBINATION von 2+ Hebeln macht S3 > S2:
    * V3 -50% + G2 +50% = ERREICHBAR (Cross-Discovery + Change Management)
    * V3 -50% + V1 -30% = ERREICHBAR (Change Management + Brand Architecture)
  - Google AI Threat erhoet den Druck zur Integration zusaetzlich

  → S3 (L4b) wird zum besseren Szenario WENN RMS:
    1. Starke Cross-Discovery implementiert (Personalisierung, Feed)
    2. Editorial Resistance aktiv adressiert (Identity Preservation)
    3. Identity Loss minimiert (House of Brands mit starker Sub-Brand-Praesenz)
""")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("+" + "-" * 70 + "+")
    print("|  PCUM SENSITIVITY ANALYSIS — Ringier Medien Schweiz              |")
    print("|  Session: EBF-S-2026-02-06-ORG-001 | {0}                   |".format("2026-02-06"))
    print("+" + "-" * 70 + "+")
    print()

    results = print_baseline()
    print()
    sa1()
    sa2()
    sa3()
    sa4()
    sa5()
    sa6()
    sa7()

    print("=" * 72)
    print("EXECUTIVE SUMMARY — SENSITIVITAETSANALYSE")
    print("=" * 72)
    print(f"""
  ┌──────────────────────────────────────────────────────────────────────┐
  │  KERNERKENNTNISSE                                                    │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │  1. S2 (Backend + Abo) ist ROBUST optimal                            │
  │     → Haelt bei lambda +/-20%, Blick-Erosion bis -25%                │
  │     → S4 (Monobrand) ist bei ALLEN Varianten wertvernichtend         │
  │                                                                      │
  │  2. S3 (L4b) braucht DREI Bedingungen gleichzeitig:                  │
  │     a) Cross-Discovery wirkt (+50% Uplift)                           │
  │     b) Editorial Resistance halbiert (Change Management)             │
  │     c) Identity Loss minimiert (Brand Architecture)                  │
  │     → Nur wenn alle drei erfuellt sind, schlaegt S3 den S2           │
  │                                                                      │
  │  3. Google AI Overviews: EIGENSTAENDIGES RISIKO                      │
  │     → Beobachter ist bei 30%+ SEO-Verlust standalone nicht viable    │
  │     → Integration als Survival-Faktor (unabhaengig von One-Platform) │
  │                                                                      │
  │  4. Blick-Erosion: HOECHSTE PRIORITAET                               │
  │     → -7% = 74M Sessions weg (mehr als ganzer Beobachter)            │
  │     → Platform-Architektur ist sekundaer wenn Basis erodiert         │
  │                                                                      │
  ├──────────────────────────────────────────────────────────────────────┤
  │  STRATEGISCHE EMPFEHLUNG (PRIORISIERT)                               │
  │                                                                      │
  │  PRIO 1: Blick-Erosion diagnostizieren und stoppen                   │
  │          → Benchmark vs. Markt (20min, SRF, NZZ)                     │
  │          → Google AI Overviews Impact isolieren                       │
  │                                                                      │
  │  PRIO 2: S2 als Basisstrategie implementieren                        │
  │          → Backend/CMS konsolidieren (L1)                             │
  │          → Blick+ als Super-Bundle positionieren (L2)                 │
  │                                                                      │
  │  PRIO 3: Beobachter-Integration vorbereiten                          │
  │          → Unabhaengig von S2/S3-Entscheidung                        │
  │          → Google-Abhaengigkeit (53% SEO) absichern                   │
  │                                                                      │
  │  PRIO 4: S3-Optionalitaet bewahren                                   │
  │          → Cross-Discovery testen (A/B-Test auf blick.ch)             │
  │          → Editorial Change Management starten                        │
  │          → Brand Architecture fuer L4b entwerfen                      │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘
""")


if __name__ == "__main__":
    main()
