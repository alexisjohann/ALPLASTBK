#!/usr/bin/env python3
"""
UBS Growth Marketing — Live-Rechner fuer Demo-Session
=====================================================
Berechnet Monte-Carlo-Ergebnisse in Echtzeit mit angepassten Parametern.

USAGE (interaktiv):
    python live_rechner.py

USAGE (direkt):
    python live_rechner.py --param monthly_leads=3500
    python live_rechner.py --param monthly_leads=3500 --param delta_AI=0.50
    python live_rechner.py --scenario optimistic
    python live_rechner.py --all  # Alle Outputs auf einmal

Erstellt: 2026-02-25
Session: EBF-S-2026-02-25-FIN-001
"""

import numpy as np
import sys
import argparse

# Seed fuer Reproduzierbarkeit
SEED = 42
N_DRAWS = 10_000

# =============================================================================
# PARAMETER-DEFINITIONEN (Default = MC_monte_carlo_simulation.yaml)
# =============================================================================

PARAMS = {
    # --- Cluster A: AI Trust & Algorithm Aversion ---
    "delta_AI":          {"mean": 0.42,  "sd": 0.075, "lo": 0.10, "hi": 0.80,
                          "label": "AI-Advice Trust Level",            "tier": 2},
    "alpha_aversion":    {"mean": 0.68,  "sd": 0.125, "lo": 0.30, "hi": 1.00,
                          "label": "Algorithm Aversion Base Effect",   "tier": 1},
    "beta_modification": {"mean": 0.41,  "sd": 0.08,  "lo": 0.15, "hi": 0.70,
                          "label": "Modifiability Effect",             "tier": 1},
    "gamma_objectivity": {"mean": 0.15,  "sd": 0.05,  "lo": 0.00, "hi": 0.40,
                          "label": "Objectivity Framing Effect",       "tier": 2},
    "rho_error_penalty": {"mean": 0.40,  "sd": 0.10,  "lo": 0.10, "hi": 0.70,
                          "label": "Post-Error Trust Penalty",         "tier": 2},

    # --- Cluster B: UTAUT2 / TAM ---
    "PE_beta":           {"mean": 0.32,  "sd": 0.05,  "lo": 0.15, "hi": 0.50,
                          "label": "Performance Expectancy Beta",      "tier": 1},
    "Trust_beta":        {"mean": 0.38,  "sd": 0.06,  "lo": 0.20, "hi": 0.55,
                          "label": "Trust Beta",                       "tier": 1},
    "SI_beta":           {"mean": 0.22,  "sd": 0.05,  "lo": 0.05, "hi": 0.40,
                          "label": "Social Influence Beta",            "tier": 1},

    # --- Cluster C: Segment-Parameter ---
    "W_algo_tech_savvy": {"mean": 0.75,  "sd": 0.08,  "lo": 0.50, "hi": 0.95,
                          "label": "W_algo Tech-Savvy",                "tier": 2},
    "W_algo_mainstream": {"mean": 0.55,  "sd": 0.10,  "lo": 0.30, "hi": 0.80,
                          "label": "W_algo Digital Mainstream",        "tier": 2},
    "W_algo_affluent":   {"mean": 0.30,  "sd": 0.08,  "lo": 0.10, "hi": 0.55,
                          "label": "W_algo Affluent Traditional",      "tier": 3},
    "W_algo_skeptics":   {"mean": 0.20,  "sd": 0.07,  "lo": 0.05, "hi": 0.45,
                          "label": "W_algo Skeptics",                  "tier": 3},
    "seg_tech_savvy":    {"mean": 0.30,  "sd": 0.05,  "lo": 0.15, "hi": 0.45,
                          "label": "Segment-Anteil Tech-Savvy",        "tier": 3},
    "seg_mainstream":    {"mean": 0.25,  "sd": 0.05,  "lo": 0.10, "hi": 0.40,
                          "label": "Segment-Anteil Mainstream",        "tier": 3},
    "seg_affluent":      {"mean": 0.20,  "sd": 0.05,  "lo": 0.10, "hi": 0.35,
                          "label": "Segment-Anteil Affluent",          "tier": 3},
    "seg_skeptics":      {"mean": 0.25,  "sd": 0.05,  "lo": 0.10, "hi": 0.40,
                          "label": "Segment-Anteil Skeptics",          "tier": 3},

    # --- Cluster D: Revenue-Kette ---
    "monthly_leads":     {"mean": 2000,  "sd": 500,   "lo": 500,  "hi": 5000,
                          "label": "Monthly Leads (Chatbot Traffic)",  "tier": 3},
    "lead_to_appt":      {"mean": 0.08,  "sd": 0.03,  "lo": 0.02, "hi": 0.20,
                          "label": "Lead-to-Appointment Rate",         "tier": 2},
    "appt_to_close":     {"mean": 0.35,  "sd": 0.08,  "lo": 0.15, "hi": 0.55,
                          "label": "Appointment-to-Close Rate",        "tier": 2},
    "avg_mortgage":      {"mean": 750000,"sd": 100000, "lo": 400000,"hi":1200000,
                          "label": "Durchschn. Hypothek (CHF)",        "tier": 2},

    # --- Cluster E: eSIM ---
    "psi_transformation":{"mean": 2.46,  "sd": 0.46,  "lo": 1.00, "hi": 4.00,
                          "label": "Psi-Transformation (Pilot->Final)","tier": 3},
    "esim_addressable":  {"mean": 63000, "sd": 20000,  "lo": 20000,"hi":150000,
                          "label": "Adressierbare eSIM-Nutzer/Jahr",   "tier": 3},
    "esim_rev_per_trip": {"mean": 15.0,  "sd": 5.0,   "lo": 5.0,  "hi": 40.0,
                          "label": "Revenue pro eSIM-Trip (CHF)",      "tier": 2},

    # --- Cluster F: Korrekturfaktoren ---
    "tau_brand_CS":      {"mean": 0.55,  "sd": 0.10,  "lo": 0.30, "hi": 0.80,
                          "label": "Brand Trust CS-Migrierte (rel.)",  "tier": 3},
    "kappa_SR_gap":      {"mean": 0.75,  "sd": 0.08,  "lo": 0.50, "hi": 0.95,
                          "label": "Stated-Revealed Gap",              "tier": 2},
    "BFS_esim":          {"mean": 0.405, "sd": 0.08,  "lo": 0.20, "hi": 0.65,
                          "label": "eSIM Brand Fit Score (norm.)",     "tier": 2},
}


def draw_truncated_normal(mean, sd, lo, hi, n=N_DRAWS, rng=None):
    """Zieht n Samples aus einer abgeschnittenen Normalverteilung."""
    if rng is None:
        rng = np.random.default_rng(SEED)
    samples = rng.normal(mean, sd, n * 3)
    samples = samples[(samples >= lo) & (samples <= hi)]
    while len(samples) < n:
        extra = rng.normal(mean, sd, n)
        extra = extra[(extra >= lo) & (extra <= hi)]
        samples = np.concatenate([samples, extra])
    return samples[:n]


def run_mc(overrides=None, n_draws=N_DRAWS, seed=SEED):
    """
    Fuehrt die Monte-Carlo-Simulation mit optionalen Parameter-Overrides durch.

    overrides: dict mit {param_name: neuer_mean_wert}
    Gibt dict mit allen Output-Metriken und Statistiken zurueck.
    """
    rng = np.random.default_rng(seed)

    # Parameter-Draws generieren
    draws = {}
    params = dict(PARAMS)
    if overrides:
        for k, v in overrides.items():
            if k in params:
                params[k]["mean"] = v

    for name, p in params.items():
        draws[name] = draw_truncated_normal(
            p["mean"], p["sd"], p["lo"], p["hi"], n_draws, rng
        )

    results = {}

    # ─────────────────────────────────────────────────────────────────────
    # OUTPUT 1: Q_M06 — Mortgage GPT Adoption Intent (Grand Mean)
    # ─────────────────────────────────────────────────────────────────────
    seg_shares = np.column_stack([
        draws["seg_tech_savvy"], draws["seg_mainstream"],
        draws["seg_affluent"], draws["seg_skeptics"]
    ])
    # Normalisiere Segment-Anteile auf 1
    seg_sums = seg_shares.sum(axis=1, keepdims=True)
    seg_shares = seg_shares / seg_sums

    W_algos = np.column_stack([
        draws["W_algo_tech_savvy"], draws["W_algo_mainstream"],
        draws["W_algo_affluent"], draws["W_algo_skeptics"]
    ])

    # Segment-spezifische Means
    baseline = 4.0  # Likert-Mittelwert
    seg_means = (
        baseline
        + 3.0 * draws["delta_AI"][:, None]
        + 2.0 * draws["beta_modification"][:, None] * W_algos
        - 1.5 * draws["alpha_aversion"][:, None] * (1 - W_algos)
        + 0.8 * draws["PE_beta"][:, None]
        + 0.6 * draws["Trust_beta"][:, None]
    )
    seg_means = np.clip(seg_means, 1.0, 7.0)

    # Grand Mean (gewichtet)
    q_m06 = (seg_means * seg_shares).sum(axis=1)
    q_m06 = np.clip(q_m06, 1.0, 7.0)

    results["Q_M06"] = {
        "label": "Mortgage GPT Adoption (Grand Mean)",
        "unit": "/ 7",
        "mean": float(np.mean(q_m06)),
        "median": float(np.median(q_m06)),
        "sd": float(np.std(q_m06)),
        "ci_95": [float(np.percentile(q_m06, 2.5)), float(np.percentile(q_m06, 97.5))],
        "P_below_3_5": float(np.mean(q_m06 < 3.5)),
        "P_above_5_0": float(np.mean(q_m06 > 5.0)),
    }

    # Segment-spezifische Ergebnisse
    seg_names = ["Tech-Savvy", "Mainstream", "Affluent", "Skeptics"]
    results["Segmente"] = {}
    for i, name in enumerate(seg_names):
        s = seg_means[:, i]
        results["Segmente"][name] = {
            "mean": float(np.mean(s)),
            "ci_95": [float(np.percentile(s, 2.5)), float(np.percentile(s, 97.5))],
        }

    # ─────────────────────────────────────────────────────────────────────
    # OUTPUT 2: Q_M08 — Trust + Post-Error
    # ─────────────────────────────────────────────────────────────────────
    q_m08 = 4.0 + 4.0 * draws["delta_AI"] + 0.8 * draws["Trust_beta"] + 0.4 * draws["SI_beta"]
    q_m08 = np.clip(q_m08, 1.0, 7.0)

    post_error = q_m08 * (1 - draws["rho_error_penalty"])
    post_error = np.clip(post_error, 1.0, 7.0)

    results["Trust_PreError"] = {
        "label": "Trust Grand Mean (Pre-Error)",
        "unit": "/ 7",
        "mean": float(np.mean(q_m08)),
        "median": float(np.median(q_m08)),
        "ci_95": [float(np.percentile(q_m08, 2.5)), float(np.percentile(q_m08, 97.5))],
    }

    results["Trust_PostError"] = {
        "label": "Trust nach GPT-Fehler",
        "unit": "/ 7",
        "mean": float(np.mean(post_error)),
        "median": float(np.median(post_error)),
        "ci_95": [float(np.percentile(post_error, 2.5)), float(np.percentile(post_error, 97.5))],
        "P_below_3_5": float(np.mean(post_error < 3.5)),
    }

    # CS-Migrierte
    cs_trust = q_m08 * draws["tau_brand_CS"]
    cs_post = cs_trust * (1 - draws["rho_error_penalty"])
    results["CS_Trust"] = {
        "label": "CS-Migrierte Trust",
        "unit": "/ 7",
        "mean": float(np.mean(cs_trust)),
        "ci_95": [float(np.percentile(cs_trust, 2.5)), float(np.percentile(cs_trust, 97.5))],
        "post_error_mean": float(np.mean(cs_post)),
    }

    # ─────────────────────────────────────────────────────────────────────
    # OUTPUT 3: Revenue Mortgage
    # ─────────────────────────────────────────────────────────────────────
    revenue = (draws["monthly_leads"] * 12
               * draws["lead_to_appt"]
               * draws["appt_to_close"]
               * draws["avg_mortgage"])

    results["Revenue_Mortgage"] = {
        "label": "Hypotheken-Neuvolumen/Jahr",
        "unit": "CHF",
        "mean": float(np.mean(revenue)),
        "median": float(np.median(revenue)),
        "sd": float(np.std(revenue)),
        "ci_95": [float(np.percentile(revenue, 2.5)), float(np.percentile(revenue, 97.5))],
        "P_above_1bn": float(np.mean(revenue > 1e9)),
    }

    # ─────────────────────────────────────────────────────────────────────
    # OUTPUT 4: eSIM Adoption (Pilot + Final)
    # ─────────────────────────────────────────────────────────────────────
    esim_pilot = rng.normal(3.8, 0.35, n_draws)
    esim_pilot = np.clip(esim_pilot, 1.0, 7.0)

    esim_final = esim_pilot * draws["psi_transformation"]
    esim_final = np.clip(esim_final, 1.0, 7.0)

    results["eSIM_Pilot"] = {
        "label": "eSIM Adoption (Pilot)",
        "unit": "/ 7",
        "mean": float(np.mean(esim_pilot)),
        "ci_95": [float(np.percentile(esim_pilot, 2.5)), float(np.percentile(esim_pilot, 97.5))],
    }

    results["eSIM_Final"] = {
        "label": "eSIM Adoption (Final, nach Psi)",
        "unit": "/ 7",
        "mean": float(np.mean(esim_final)),
        "median": float(np.median(esim_final)),
        "ci_95": [float(np.percentile(esim_final, 2.5)), float(np.percentile(esim_final, 97.5))],
        "P_above_4_5": float(np.mean(esim_final > 4.5)),
    }

    # ─────────────────────────────────────────────────────────────────────
    # OUTPUT 5: eSIM Revenue
    # ─────────────────────────────────────────────────────────────────────
    trips_per_year = 1.5
    esim_rev = draws["esim_addressable"] * draws["esim_rev_per_trip"] * trips_per_year

    results["Revenue_eSIM"] = {
        "label": "eSIM Revenue/Jahr",
        "unit": "CHF",
        "mean": float(np.mean(esim_rev)),
        "median": float(np.median(esim_rev)),
        "ci_95": [float(np.percentile(esim_rev, 2.5)), float(np.percentile(esim_rev, 97.5))],
    }

    # ─────────────────────────────────────────────────────────────────────
    # OUTPUT 6: Revealed Adoption (SR-Gap)
    # ─────────────────────────────────────────────────────────────────────
    revealed = q_m06 * draws["kappa_SR_gap"]
    results["Revealed_Adoption"] = {
        "label": "Tatsaechliche Adoption (nach SR-Gap)",
        "unit": "/ 7",
        "mean": float(np.mean(revealed)),
        "ci_95": [float(np.percentile(revealed, 2.5)), float(np.percentile(revealed, 97.5))],
        "P_below_3_5": float(np.mean(revealed < 3.5)),
    }

    return results


def fmt_chf(val):
    """Formatiert CHF-Werte mit Apostroph als Tausendertrennzeichen."""
    if abs(val) >= 1e9:
        return f"CHF {val/1e9:.2f} Mrd"
    elif abs(val) >= 1e6:
        return f"CHF {val/1e6:.2f} Mio"
    elif abs(val) >= 1e3:
        return f"CHF {val/1e3:.0f}K"
    return f"CHF {val:.0f}"


def print_results(results, overrides=None):
    """Druckt die MC-Ergebnisse formatiert aus."""
    print()
    print("=" * 72)
    print("  UBS GROWTH MARKETING — LIVE MONTE CARLO (N=10'000)")
    print("=" * 72)

    if overrides:
        print()
        print("  PARAMETER-OVERRIDES:")
        for k, v in overrides.items():
            default = PARAMS.get(k, {}).get("mean", "?")
            label = PARAMS.get(k, {}).get("label", k)
            if isinstance(default, (int, float)) and default > 1000:
                print(f"  → {label}: {default:,.0f} → {v:,.0f}")
            else:
                print(f"  → {label}: {default} → {v}")
    print()

    # --- Q_M06 ---
    r = results["Q_M06"]
    print("─" * 72)
    print(f"  🟢 MORTGAGE GPT ADOPTION (Grand Mean)")
    print(f"     Mean: {r['mean']:.2f} {r['unit']}  |  95% CI: [{r['ci_95'][0]:.2f}, {r['ci_95'][1]:.2f}]")
    print(f"     P(< 3.5) = {r['P_below_3_5']:.1%}  |  P(> 5.0) = {r['P_above_5_0']:.1%}")
    go = "GO ✓" if r['P_below_3_5'] < 0.05 else "RISIKO ⚠️" if r['P_below_3_5'] < 0.15 else "NO-GO ✗"
    print(f"     Assessment: {go}")

    # Segmente
    print()
    print(f"     Segmente:")
    for name, s in results["Segmente"].items():
        bar_len = int((s['mean'] / 7.0) * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        print(f"     {name:20s} {s['mean']:.1f}  {bar}  [{s['ci_95'][0]:.1f}, {s['ci_95'][1]:.1f}]")

    # --- Trust ---
    print()
    print("─" * 72)
    r = results["Trust_PreError"]
    print(f"  🟢 TRUST (Pre-Error)")
    print(f"     Mean: {r['mean']:.2f} {r['unit']}  |  95% CI: [{r['ci_95'][0]:.2f}, {r['ci_95'][1]:.2f}]")

    r = results["Trust_PostError"]
    print(f"  🔴 TRUST (Post-Error)")
    print(f"     Mean: {r['mean']:.2f} {r['unit']}  |  95% CI: [{r['ci_95'][0]:.2f}, {r['ci_95'][1]:.2f}]")
    print(f"     P(< 3.5) = {r['P_below_3_5']:.1%}")

    r = results["CS_Trust"]
    print(f"  🔴 CS-MIGRIERTE Trust")
    print(f"     Mean: {r['mean']:.2f} {r['unit']}  |  Post-Error: {r['post_error_mean']:.2f}")

    # --- Revenue Mortgage ---
    print()
    print("─" * 72)
    r = results["Revenue_Mortgage"]
    print(f"  🟡 REVENUE MORTGAGE (Neuvolumen/Jahr)")
    print(f"     Median: {fmt_chf(r['median'])}  |  95% CI: [{fmt_chf(r['ci_95'][0])}, {fmt_chf(r['ci_95'][1])}]")
    print(f"     P(> 1 Mrd) = {r['P_above_1bn']:.1%}")

    # --- eSIM ---
    print()
    print("─" * 72)
    r = results["eSIM_Final"]
    print(f"  🔴 eSIM ADOPTION (Final, nach Psi-Transformation)")
    print(f"     Mean: {r['mean']:.2f} {r['unit']}  |  95% CI: [{r['ci_95'][0]:.2f}, {r['ci_95'][1]:.2f}]")
    print(f"     P(> 4.5) = {r['P_above_4_5']:.1%}")

    r = results["Revenue_eSIM"]
    print(f"  🟢 eSIM REVENUE")
    print(f"     Median: {fmt_chf(r['median'])}  |  95% CI: [{fmt_chf(r['ci_95'][0])}, {fmt_chf(r['ci_95'][1])}]")

    # --- Revealed ---
    print()
    print("─" * 72)
    r = results["Revealed_Adoption"]
    print(f"  🟡 REVEALED ADOPTION (nach SR-Gap-Korrektur)")
    print(f"     Mean: {r['mean']:.2f} {r['unit']}  |  95% CI: [{r['ci_95'][0]:.2f}, {r['ci_95'][1]:.2f}]")
    print(f"     P(< 3.5) = {r['P_below_3_5']:.1%}")

    print()
    print("=" * 72)


def compare(baseline, updated, overrides):
    """Zeigt den Vergleich Baseline vs. Updated mit Delta."""
    print()
    print("=" * 72)
    print("  VERGLEICH: BASELINE vs. MIT UBS-DATEN")
    print("=" * 72)

    if overrides:
        print()
        print("  GEAENDERTE PARAMETER:")
        for k, v in overrides.items():
            default = PARAMS.get(k, {}).get("mean", "?")
            label = PARAMS.get(k, {}).get("label", k)
            if isinstance(default, (int, float)) and default > 1000:
                print(f"  → {label}: {default:,.0f} → {v:,.0f}")
            else:
                print(f"  → {label}: {default} → {v}")
    print()

    keys_to_compare = [
        ("Q_M06", "Mortgage Adoption", "/ 7", "mean"),
        ("Trust_PostError", "Trust Post-Error", "/ 7", "mean"),
        ("Revenue_Mortgage", "Revenue Mortgage", "CHF", "median"),
        ("eSIM_Final", "eSIM Adoption", "/ 7", "mean"),
    ]

    print(f"  {'Metrik':<25s}  {'Baseline':>10s}  {'Updated':>10s}  {'Delta':>10s}  {'CI-Aenderung'}")
    print("  " + "─" * 68)

    for key, label, unit, stat in keys_to_compare:
        b = baseline[key]
        u = updated[key]
        bv = b[stat]
        uv = u[stat]
        delta = uv - bv

        b_width = b["ci_95"][1] - b["ci_95"][0]
        u_width = u["ci_95"][1] - u["ci_95"][0]
        ci_change = (u_width - b_width) / b_width * 100

        if unit == "CHF":
            print(f"  {label:<25s}  {fmt_chf(bv):>10s}  {fmt_chf(uv):>10s}  {fmt_chf(delta):>10s}  CI {ci_change:+.0f}%")
        else:
            sign = "+" if delta > 0 else ""
            print(f"  {label:<25s}  {bv:>10.2f}  {uv:>10.2f}  {sign}{delta:>9.2f}  CI {ci_change:+.0f}%")

    print()
    print("=" * 72)


def interactive_mode():
    """Interaktiver Modus fuer die Demo-Session."""
    print()
    print("=" * 72)
    print("  UBS GROWTH MARKETING — LIVE-RECHNER (Interaktiv)")
    print("=" * 72)
    print()
    print("  Verfuegbare Parameter (Default → aendern):")
    print("  " + "─" * 68)

    for name, p in sorted(PARAMS.items()):
        tier_icon = {1: "🟢", 2: "🟡", 3: "🔴", 4: "⚫"}.get(p["tier"], "?")
        if p["mean"] > 1000:
            print(f"  {tier_icon} {name:<22s}  {p['mean']:>10,.0f}  ({p['label']})")
        else:
            print(f"  {tier_icon} {name:<22s}  {p['mean']:>10.3f}  ({p['label']})")

    print()
    print("  Befehle:")
    print("    param_name=wert     Parameter aendern (z.B. monthly_leads=3500)")
    print("    run                 MC mit aktuellen Aenderungen ausfuehren")
    print("    compare             Baseline vs. aktuelle Aenderungen vergleichen")
    print("    reset               Alle Aenderungen zuruecksetzen")
    print("    quit                Beenden")
    print()

    overrides = {}
    baseline = run_mc()

    while True:
        try:
            user_input = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Beendet.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("  Beendet.")
            break

        if user_input.lower() == "reset":
            overrides = {}
            print("  ✓ Alle Aenderungen zurueckgesetzt.")
            continue

        if user_input.lower() == "run":
            results = run_mc(overrides)
            print_results(results, overrides)
            continue

        if user_input.lower() == "compare":
            updated = run_mc(overrides)
            compare(baseline, updated, overrides)
            continue

        # Parameter-Zuweisung
        if "=" in user_input:
            parts = user_input.split("=")
            param_name = parts[0].strip()
            try:
                value = float(parts[1].strip())
            except ValueError:
                print(f"  ✗ Ungültiger Wert: {parts[1].strip()}")
                continue

            if param_name not in PARAMS:
                print(f"  ✗ Unbekannter Parameter: {param_name}")
                # Fuzzy-Match
                matches = [p for p in PARAMS if param_name.lower() in p.lower()]
                if matches:
                    print(f"    Meinten Sie: {', '.join(matches)}?")
                continue

            overrides[param_name] = value
            label = PARAMS[param_name]["label"]
            default = PARAMS[param_name]["mean"]
            if default > 1000:
                print(f"  ✓ {label}: {default:,.0f} → {value:,.0f}")
            else:
                print(f"  ✓ {label}: {default:.3f} → {value:.3f}")
            print(f"    (Aktive Overrides: {len(overrides)}. 'run' zum Berechnen.)")
            continue

        print(f"  ✗ Unbekannter Befehl: {user_input}")
        print(f"    Versuche: param=wert, run, compare, reset, quit")


# Pre-defined Szenarien fuer schnellen Zugriff
SCENARIOS = {
    "optimistic": {
        "monthly_leads": 3000,
        "delta_AI": 0.50,
        "lead_to_appt": 0.10,
        "psi_transformation": 3.00,
    },
    "pessimistic": {
        "monthly_leads": 1200,
        "delta_AI": 0.35,
        "lead_to_appt": 0.05,
        "psi_transformation": 1.80,
    },
    "ubs_data_example": {
        "monthly_leads": 3500,
        "avg_mortgage": 820000,
        "tau_brand_CS": 0.45,
    },
}


def main():
    parser = argparse.ArgumentParser(description="UBS Live-Rechner: MC in Echtzeit")
    parser.add_argument("--param", action="append", help="Parameter override (name=value)")
    parser.add_argument("--scenario", choices=list(SCENARIOS.keys()), help="Vordefiniertes Szenario")
    parser.add_argument("--all", action="store_true", help="Alle Outputs anzeigen")
    parser.add_argument("--compare", action="store_true", help="Baseline vs. Override vergleichen")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interaktiver Modus")
    args = parser.parse_args()

    # Interaktiver Modus
    if args.interactive or (not args.param and not args.scenario and not args.all):
        interactive_mode()
        return

    # Overrides sammeln
    overrides = {}
    if args.scenario:
        overrides.update(SCENARIOS[args.scenario])
        print(f"\n  Szenario: {args.scenario}")

    if args.param:
        for p in args.param:
            name, val = p.split("=")
            overrides[name.strip()] = float(val.strip())

    # Berechnung
    if args.compare:
        baseline = run_mc()
        updated = run_mc(overrides)
        compare(baseline, updated, overrides)
    else:
        results = run_mc(overrides if overrides else None)
        print_results(results, overrides if overrides else None)


if __name__ == "__main__":
    main()
