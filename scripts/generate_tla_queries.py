#!/usr/bin/env python3
"""
TLA Deviation Study — Query Generator (Stufe 3)
================================================

Generates 100 stratified queries for the TLA deviation study.
Uses parameter-registry.yaml and pct-psi-scales.yaml as sources.

Stratification:
  S1: Context-free (25 queries)  — Pure registry lookup
  S2: 1 Psi dimension (30 queries)  — Single-context PCT
  S3: 2-3 Psi dimensions (30 queries) — Multi-context PCT
  S4: Full pipeline (15 queries) — PCT + LLMMC calibration

Output: data/research/tla-query-battery-100.yaml
"""

import itertools
import random
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARAM_REGISTRY = ROOT / "data" / "parameter-registry.yaml"
PSI_SCALES = ROOT / "data" / "pct-psi-scales.yaml"
OUTPUT = ROOT / "data" / "research" / "tla-query-battery-100.yaml"

random.seed(42)  # Reproducible

# ============================================================================
# Load sources
# ============================================================================
def load_params():
    with open(PARAM_REGISTRY) as f:
        data = yaml.safe_load(f)
    params = []
    # Registry uses category-based keys (behavioral_parameters, contextual_parameters, etc.)
    param_sections = [
        "behavioral_parameters", "contextual_parameters",
        "intervention_parameters", "complementarity_parameters",
        "time_allocation_parameters", "german_care_parameters",
        "real_estate_parameters", "advice_parameters",
    ]
    for section_key in param_sections:
        for p in data.get(section_key, []):
            # Extract value from nested structure: values.literature.mean
            values = p.get("values", {})
            lit = values.get("literature", {})
            val = lit.get("mean")
            if val is None:
                continue
            try:
                val = float(val)
            except (ValueError, TypeError):
                continue

            ci_95 = lit.get("ci_95")

            # Extract domain-specific values
            domain_specific = {}
            ds = values.get("domain_specific", {})
            for domain, ds_info in ds.items():
                if isinstance(ds_info, dict) and "mean" in ds_info:
                    domain_specific[domain] = {"value": ds_info["mean"]}
                elif isinstance(ds_info, (int, float)):
                    domain_specific[domain] = {"value": ds_info}

            params.append({
                "id": p["id"],
                "symbol": p.get("symbol", p["id"]),
                "name": p.get("name", ""),
                "value": val,
                "ci_95": ci_95,
                "domain_specific": domain_specific,
            })
    return params


def load_psi_scales():
    with open(PSI_SCALES) as f:
        data = yaml.safe_load(f)
    scales = {}
    for dim, info in data.get("scales", {}).items():
        labels = info.get("values", {})
        if labels:
            scales[dim] = {
                "description": info.get("description", ""),
                "labels": labels,
            }
    return scales


# ============================================================================
# Query templates
# ============================================================================
def make_s1_query(qid, param, domain=None):
    """S1: Context-free registry lookup."""
    val = param["value"]
    domain_val = None
    if domain and param.get("domain_specific") and domain in param["domain_specific"]:
        ds = param["domain_specific"][domain]
        if isinstance(ds, dict):
            domain_val = ds.get("value")
        elif isinstance(ds, (int, float)):
            domain_val = ds

    gt_val = domain_val if domain_val else val
    ci = param.get("ci_95")

    prompt = (
        f"Du bist ein Experte fuer Verhaltensoekonomie.\n"
        f"Schaetze den Parameter {param['name']} ({param['symbol']}).\n"
    )
    if domain:
        prompt += f"Kontext: {domain} Domaene.\n"
    prompt += "Gib eine Punktschaetzung und ein 95% Konfidenzintervall."

    gt = {"value": gt_val, "source": f"parameter-registry ({param['id']})", "tier": 2}
    if ci:
        gt["ci_95"] = ci

    return {
        "id": qid,
        "stratum": "S1",
        "parameter_id": param["id"],
        "symbol": param["symbol"],
        "parameter_name": param["name"],
        "context": None,
        "domain": domain,
        "llm_prompt": prompt,
        "ground_truth": gt,
    }


def make_s2_query(qid, param, psi_dim, anchor_label, target_label, anchor_val, target_val):
    """S2: Single Psi dimension shift."""
    prompt = (
        f"Du bist ein Experte fuer Verhaltensoekonomie.\n"
        f"Schaetze den Parameter {param['name']} ({param['symbol']}) "
        f"wenn sich der Kontext aendert:\n"
        f"  Von: {anchor_label.replace('_', ' ')}\n"
        f"  Nach: {target_label.replace('_', ' ')}\n"
        f"Referenz: {param['symbol']} = {param['value']} im Basis-Kontext.\n"
        f"Gib eine Punktschaetzung und ein 95% Konfidenzintervall."
    )

    return {
        "id": qid,
        "stratum": "S2",
        "parameter_id": param["id"],
        "symbol": param["symbol"],
        "parameter_name": param["name"],
        "context": {
            "target_psi": {psi_dim: target_label},
            "anchor_psi": {psi_dim: anchor_label},
            "description": f"{psi_dim} shift: {anchor_label} -> {target_label}",
        },
        "domain": None,
        "llm_prompt": prompt,
        "ground_truth": {
            "note": f"PCT-computed from anchor with {psi_dim} delta",
            "anchor_value": param["value"],
            "psi_deltas": {psi_dim: {"anchor": anchor_label, "target": target_label}},
            "tier": "2+PCT",
        },
    }


def make_s3_query(qid, param, psi_shifts):
    """S3: Multi-Psi (2-3 dimensions)."""
    n_dims = len(psi_shifts)
    shifts_desc = ", ".join(
        f"{dim}: {s['anchor']} -> {s['target']}"
        for dim, s in psi_shifts.items()
    )

    lines = [f"  {dim}: von {s['anchor'].replace('_',' ')} nach {s['target'].replace('_',' ')}"
             for dim, s in psi_shifts.items()]

    prompt = (
        f"Du bist ein Experte fuer Verhaltensoekonomie.\n"
        f"Schaetze den Parameter {param['name']} ({param['symbol']}) "
        f"wenn sich {n_dims} Kontext-Dimensionen gleichzeitig aendern:\n"
        + "\n".join(lines) + "\n"
        f"Referenz: {param['symbol']} = {param['value']} im Basis-Kontext.\n"
        f"Wie interagieren diese Kontext-Aenderungen?\n"
        f"Gib eine Punktschaetzung und ein 95% Konfidenzintervall."
    )

    return {
        "id": qid,
        "stratum": "S3",
        "parameter_id": param["id"],
        "symbol": param["symbol"],
        "parameter_name": param["name"],
        "context": {
            "target_psi": {dim: s["target"] for dim, s in psi_shifts.items()},
            "anchor_psi": {dim: s["anchor"] for dim, s in psi_shifts.items()},
            "description": f"{n_dims}D shift: {shifts_desc}",
        },
        "domain": None,
        "llm_prompt": prompt,
        "ground_truth": {
            "note": f"PCT-computed: {n_dims}D psi shift",
            "anchor_value": param["value"],
            "psi_deltas": {dim: {"anchor": s["anchor"], "target": s["target"]}
                          for dim, s in psi_shifts.items()},
            "tier": "2+PCT",
        },
    }


def make_s4_query(qid, param, psi_shifts, domain=None):
    """S4: Full pipeline (PCT + LLMMC)."""
    q = make_s3_query(qid, param, psi_shifts)
    q["stratum"] = "S4"
    q["calibrate"] = True
    q["domain"] = domain
    q["ground_truth"]["tier"] = "2+PCT+LLMMC"
    q["ground_truth"]["note"] = f"Full pipeline: Layer 2 + PCT ({len(psi_shifts)}D) + LLMMC calibration"
    return q


# ============================================================================
# Generate diverse query combinations
# ============================================================================
def pick_contrasting_labels(labels_dict):
    """Pick an anchor (low end) and target (high end) label pair."""
    sorted_labels = sorted(labels_dict.items(), key=lambda x: x[1])
    # Pick from bottom third and top third
    n = len(sorted_labels)
    low_pool = sorted_labels[:max(n // 3, 1)]
    high_pool = sorted_labels[-(max(n // 3, 1)):]
    anchor = random.choice(low_pool)
    target = random.choice(high_pool)
    return anchor[0], target[0], anchor[1], target[1]


def generate_all_queries():
    params = load_params()
    psi_scales = load_psi_scales()

    # Select core behavioral parameters for the study
    # Focus on well-documented parameters with clear behavioral meaning
    core_param_ids = [
        "PAR-BEH-001",  # λ (loss aversion)
        "PAR-BEH-002",  # φ_crowding (crowding-out)
        "PAR-BEH-003",  # β (present bias)
        "PAR-BEH-004",  # δ_q (quasi-hyperbolic discount)
        "PAR-BEH-009",  # I_s (identity salience)
        "PAR-BEH-010",  # I_o (outgroup identity)
        "PAR-BEH-012",  # α_FS (Fehr-Schmidt alpha)
        "PAR-BEH-013",  # β_FS (Fehr-Schmidt beta)
        "PAR-BEH-014",  # μ (warm glow / moral satisfaction)
        "PAR-BEH-015",  # ρ (reciprocity)
        "PAR-BEH-016",  # λ_R (rejection sensitivity)
        "PAR-BEH-017",  # α_R (rejection aversion)
    ]

    # Also include intervention, domain-specific and other params
    domain_param_ids = [
        "PAR-INT-001",   # E_default (default effect)
        "PAR-INT-002",   # E_social_norm (social norm effect)
        "PAR-INT-003",   # E_identity (identity intervention)
        "PAR-INT-004",   # E_warmglow (warm glow intervention)
        "PAR-POL-001",   # φ_FI (fiscal illusion)
        "PAR-POL-002",   # σ_lobby (lobby effectiveness)
        "PAR-ADV-001",   # α_update (advice update weight)
        "PAR-RE-001",    # κ_cap (capitalization rate)
        "PAR-RE-002",    # π_sea (seasonality premium)
    ]

    all_target_ids = core_param_ids + domain_param_ids
    param_map = {p["id"]: p for p in params}
    usable_params = [param_map[pid] for pid in all_target_ids if pid in param_map]

    psi_dims = list(psi_scales.keys())
    queries = []
    qid_counter = 1

    # ========================================================================
    # S1: Context-free (25 queries)
    # ========================================================================
    # 15 queries: different parameters, no domain
    for p in usable_params[:15]:
        qid = f"Q{qid_counter:03d}"
        queries.append(make_s1_query(qid, p))
        qid_counter += 1

    # 10 queries: key params with domain-specific values
    domains = ["finance", "health", "energy", "education", "labor"]
    for domain in domains:
        for p in [param_map.get("PAR-BEH-001"), param_map.get("PAR-BEH-003")]:
            if p:
                qid = f"Q{qid_counter:03d}"
                queries.append(make_s1_query(qid, p, domain=domain))
                qid_counter += 1

    # ========================================================================
    # S2: Single Psi dimension (30 queries)
    # ========================================================================
    # For each Psi dimension, generate ~4 queries with different params
    s2_combos = []
    for dim in psi_dims:
        labels = psi_scales[dim]["labels"]
        if len(labels) < 2:
            continue
        # 4 queries per dimension
        for _ in range(4):
            p = random.choice(usable_params)
            anchor, target, a_val, t_val = pick_contrasting_labels(labels)
            s2_combos.append((p, dim, anchor, target, a_val, t_val))

    # Take 30
    random.shuffle(s2_combos)
    for combo in s2_combos[:30]:
        p, dim, anchor, target, a_val, t_val = combo
        qid = f"Q{qid_counter:03d}"
        queries.append(make_s2_query(qid, p, dim, anchor, target, a_val, t_val))
        qid_counter += 1

    # ========================================================================
    # S3: Multi-Psi 2-3 dimensions (30 queries)
    # ========================================================================
    for i in range(30):
        p = random.choice(usable_params)
        n_dims = random.choice([2, 2, 3])  # Weighted toward 2D
        dims = random.sample(psi_dims, n_dims)
        shifts = {}
        for dim in dims:
            labels = psi_scales[dim]["labels"]
            anchor, target, _, _ = pick_contrasting_labels(labels)
            shifts[dim] = {"anchor": anchor, "target": target}

        qid = f"Q{qid_counter:03d}"
        queries.append(make_s3_query(qid, p, shifts))
        qid_counter += 1

    # ========================================================================
    # S4: Full pipeline (15 queries)
    # ========================================================================
    s4_domains = ["finance", "health", "energy", None, "labor",
                  "education", None, None, "finance", "health",
                  None, "energy", None, "labor", "education"]

    for i in range(15):
        p = random.choice(usable_params)
        n_dims = random.choice([3, 4, 4])  # Weighted toward 4D
        dims = random.sample(psi_dims, min(n_dims, len(psi_dims)))
        shifts = {}
        for dim in dims:
            labels = psi_scales[dim]["labels"]
            anchor, target, _, _ = pick_contrasting_labels(labels)
            shifts[dim] = {"anchor": anchor, "target": target}

        qid = f"Q{qid_counter:03d}"
        domain = s4_domains[i] if i < len(s4_domains) else None
        queries.append(make_s4_query(qid, p, shifts, domain=domain))
        qid_counter += 1

    return queries


# ============================================================================
# Main
# ============================================================================
def main():
    queries = generate_all_queries()

    # Count by stratum
    strata = {}
    for q in queries:
        s = q["stratum"]
        strata[s] = strata.get(s, 0) + 1

    battery = {
        "metadata": {
            "study_id": "TLA-DEV-2026-001",
            "version": "1.0",
            "n_queries": len(queries),
            "date_created": "2026-02-16",
            "status": "ACTIVE",
            "generator": "scripts/generate_tla_queries.py",
            "seed": 42,
            "stratification": {
                s: {"n": n, "description": desc}
                for s, n, desc in [
                    ("S1", strata.get("S1", 0), "Context-free (SIMPLE query)"),
                    ("S2", strata.get("S2", 0), "1 Psi dimension (CONTEXTUAL)"),
                    ("S3", strata.get("S3", 0), "2-3 Psi dimensions (MULTI-D)"),
                    ("S4", strata.get("S4", 0), "Full pipeline (CALIBRATED)"),
                ]
            },
        },
        "queries": queries,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        yaml.dump(battery, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)

    print(f"Generated {len(queries)} queries:")
    for s, n in sorted(strata.items()):
        print(f"  {s}: {n} queries")
    print(f"\nSaved to: {OUTPUT}")


if __name__ == "__main__":
    main()
