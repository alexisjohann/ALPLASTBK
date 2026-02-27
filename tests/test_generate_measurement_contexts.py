#!/usr/bin/env python3
"""
Tests for generate_measurement_contexts.py
===========================================

Verifies that:
  - extract_param_contexts correctly maps domain_specific + dach + literature
  - extract_all_param_contexts iterates over all *_parameters sections
  - merge_contexts deduplicates on (parameter_id, context) key
  - check_new_labels detects unmapped psi labels
  - DOMAIN_PSI_MAP covers expected domains

Tests cover:
  - extract_param_contexts: Single-parameter extraction (domain, DACH, literature)
  - extract_all_param_contexts: Registry-wide extraction
  - merge_contexts: Deduplication logic
  - check_new_labels: Unmapped label detection
  - DOMAIN_PSI_MAP: Coverage and structure
  - Integration: End-to-end with real data
"""

import sys
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from generate_measurement_contexts import (
    extract_param_contexts,
    extract_all_param_contexts,
    merge_contexts,
    check_new_labels,
    DOMAIN_PSI_MAP,
    PREFIX_DOMAIN_MAP,
    load_yaml,
    PARAM_REGISTRY_PATH,
    PSI_SCALES_PATH,
    EXISTING_CONTEXTS_PATH,
)


# ---------------------------------------------------------------------------
# Test fixtures: minimal parameter entries
# ---------------------------------------------------------------------------

PARAM_WITH_DOMAINS = {
    "id": "PAR-TEST-001",
    "symbol": "lambda_test",
    "name": "Test Parameter",
    "values": {
        "domain_specific": {
            "finance": {
                "mean": 2.4,
                "ci_68": [2.1, 2.7],
            },
            "health": {
                "mean": 1.8,
                "ci_68": [1.5, 2.1],
            },
        },
        "dach_adjusted": {
            "mean": 2.35,
            "ci_68": [2.1, 2.6],
            "note": "DACH-specific",
        },
        "literature": {
            "mean": 2.25,
            "note": "Original estimate",
        },
    },
    "literature_sources": [
        {"key": "kahneman1979prospect"},
    ],
}

PARAM_LITERATURE_ONLY = {
    "id": "PAR-TEST-002",
    "symbol": "beta_test",
    "name": "Literature Only Param",
    "values": {
        "literature": {
            "mean": 0.7,
            "note": "Laibson (1997)",
        },
    },
    "literature_sources": [
        {"key": "laibson1997golden"},
    ],
}

PARAM_EMPTY = {
    "id": "PAR-TEST-003",
    "symbol": "gamma_test",
    "name": "Empty Parameter",
    "values": {},
}

PARAM_UNKNOWN_DOMAIN = {
    "id": "PAR-TEST-004",
    "symbol": "tau_test",
    "name": "Unknown Domain Param",
    "values": {
        "domain_specific": {
            "xyzzy_unknown_domain": {
                "mean": 0.5,
            },
        },
    },
}


# ---------------------------------------------------------------------------
# extract_param_contexts tests
# ---------------------------------------------------------------------------

def test_extract_domain_contexts():
    """Should extract one triplet per domain_specific entry."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    domain_contexts = [c for c in contexts if c["study_type"] == "registry_derived"
                       and c["context"] != "dach_adjusted"]
    assert len(domain_contexts) == 2, \
        f"Expected 2 domain contexts, got {len(domain_contexts)}"


def test_extract_domain_psi_conditions():
    """Domain contexts should have correct psi_conditions from DOMAIN_PSI_MAP."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    finance_ctx = [c for c in contexts if c["context"] == "finance_context"]
    assert len(finance_ctx) == 1, f"Expected 1 finance context, got {len(finance_ctx)}"
    psi = finance_ctx[0]["psi_conditions"]
    assert "psi_I" in psi, f"Expected psi_I in finance psi, got {psi}"
    assert psi["psi_I"] == "market_regulatory_environment"


def test_extract_domain_value_with_ci():
    """Value estimate should include CI when available."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    finance_ctx = [c for c in contexts if c["context"] == "finance_context"][0]
    assert "2.4" in finance_ctx["value_estimate"]
    assert "CI:" in finance_ctx["value_estimate"]


def test_extract_dach_adjusted():
    """Should extract DACH-adjusted as a separate context."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    dach = [c for c in contexts if c["context"] == "dach_adjusted"]
    assert len(dach) == 1, f"Expected 1 DACH context, got {len(dach)}"
    assert dach[0]["countries"] == ["CH", "AT", "DE"]
    assert "psi_K" in dach[0]["psi_conditions"]


def test_extract_literature_baseline():
    """Should extract literature baseline with empty psi_conditions."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    lit = [c for c in contexts if c["context"] == "literature_baseline"]
    assert len(lit) == 1, f"Expected 1 literature baseline, got {len(lit)}"
    assert lit[0]["psi_conditions"] == {}
    assert lit[0]["study_type"] == "literature_meta"
    assert lit[0]["paper_key"] == "kahneman1979prospect"


def test_extract_literature_uses_first_source():
    """Literature baseline paper_key should come from first literature_source."""
    contexts = extract_param_contexts(PARAM_LITERATURE_ONLY)
    lit = [c for c in contexts if c["context"] == "literature_baseline"]
    assert len(lit) == 1
    assert lit[0]["paper_key"] == "laibson1997golden"


def test_extract_literature_fallback_no_sources():
    """If no literature_sources, paper_key should be 'parameter_registry'."""
    param = {
        "id": "PAR-TEST-005",
        "symbol": "x",
        "name": "No Sources",
        "values": {"literature": {"mean": 1.0}},
    }
    contexts = extract_param_contexts(param)
    lit = [c for c in contexts if c["context"] == "literature_baseline"]
    assert len(lit) == 1
    assert lit[0]["paper_key"] == "parameter_registry"


def test_extract_empty_values():
    """Parameter with empty values should produce 0 contexts."""
    contexts = extract_param_contexts(PARAM_EMPTY)
    assert len(contexts) == 0


def test_extract_unknown_domain_skipped():
    """Unknown domains without PSI mapping should be skipped."""
    contexts = extract_param_contexts(PARAM_UNKNOWN_DOMAIN)
    assert len(contexts) == 0, \
        f"Expected 0 contexts for unknown domain, got {len(contexts)}"


def test_extract_parameter_id_preserved():
    """All contexts should have the correct parameter_id."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    for c in contexts:
        assert c["parameter_id"] == "PAR-TEST-001"


def test_extract_parameter_symbol_preserved():
    """All contexts should have the correct parameter_symbol."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    for c in contexts:
        assert c["parameter_symbol"] == "lambda_test"


def test_extract_full_param_context_count():
    """PARAM_WITH_DOMAINS: 2 domain + 1 dach + 1 literature = 4 contexts."""
    contexts = extract_param_contexts(PARAM_WITH_DOMAINS)
    assert len(contexts) == 4, \
        f"Expected 4 total contexts, got {len(contexts)}: {[c['context'] for c in contexts]}"


def test_extract_partial_domain_match():
    """Domain names containing a known domain should match via partial match."""
    param = {
        "id": "PAR-TEST-006",
        "symbol": "x",
        "name": "Partial Match",
        "values": {
            "domain_specific": {
                "health_donation": {
                    "mean": 0.55,
                },
            },
        },
    }
    contexts = extract_param_contexts(param)
    # "health_donation" contains "health" which is in DOMAIN_PSI_MAP
    assert len(contexts) >= 1, \
        f"Expected partial domain match for 'health_donation', got {len(contexts)}"


# ---------------------------------------------------------------------------
# extract_all_param_contexts tests
# ---------------------------------------------------------------------------

def test_extract_all_iterates_parameter_sections():
    """Should iterate over all *_parameters sections."""
    registry = {
        "behavioral_parameters": [PARAM_WITH_DOMAINS],
        "contextual_parameters": [PARAM_LITERATURE_ONLY],
        "metadata": {"version": "1.0"},  # should be skipped
    }
    contexts = extract_all_param_contexts(registry)
    param_ids = set(c["parameter_id"] for c in contexts)
    assert "PAR-TEST-001" in param_ids
    assert "PAR-TEST-002" in param_ids


def test_extract_all_skips_non_parameter_keys():
    """Keys not ending in _parameters should be skipped."""
    registry = {
        "metadata": {"version": "1.0"},
        "notes": "some notes",
        "behavioral_parameters": [PARAM_LITERATURE_ONLY],
    }
    contexts = extract_all_param_contexts(registry)
    assert all(c["parameter_id"] == "PAR-TEST-002" for c in contexts)


def test_extract_all_empty_registry():
    """Empty registry should return empty list."""
    contexts = extract_all_param_contexts({})
    assert contexts == []


def test_extract_all_aggregates_counts():
    """Total contexts should equal sum of individual param contexts."""
    registry = {
        "behavioral_parameters": [PARAM_WITH_DOMAINS, PARAM_LITERATURE_ONLY],
    }
    contexts = extract_all_param_contexts(registry)
    expected = len(extract_param_contexts(PARAM_WITH_DOMAINS)) + \
               len(extract_param_contexts(PARAM_LITERATURE_ONLY))
    assert len(contexts) == expected


# ---------------------------------------------------------------------------
# merge_contexts tests
# ---------------------------------------------------------------------------

def test_merge_no_duplicates():
    """Non-overlapping contexts should all be merged."""
    existing = [{"parameter_id": "PAR-A", "context": "ctx1"}]
    new = [{"parameter_id": "PAR-B", "context": "ctx2"}]
    merged, added = merge_contexts(existing, new)
    assert len(merged) == 2
    assert added == 1


def test_merge_dedup_same_key():
    """Same (parameter_id, context) should not be duplicated."""
    existing = [{"parameter_id": "PAR-A", "context": "ctx1", "value": "old"}]
    new = [{"parameter_id": "PAR-A", "context": "ctx1", "value": "new"}]
    merged, added = merge_contexts(existing, new)
    assert len(merged) == 1
    assert added == 0
    # Existing value should be preserved (not overwritten)
    assert merged[0]["value"] == "old"


def test_merge_partial_overlap():
    """Mixed overlap: some new, some duplicate."""
    existing = [
        {"parameter_id": "PAR-A", "context": "ctx1"},
        {"parameter_id": "PAR-B", "context": "ctx2"},
    ]
    new = [
        {"parameter_id": "PAR-A", "context": "ctx1"},  # dup
        {"parameter_id": "PAR-C", "context": "ctx3"},  # new
        {"parameter_id": "PAR-B", "context": "ctx2"},  # dup
        {"parameter_id": "PAR-D", "context": "ctx4"},  # new
    ]
    merged, added = merge_contexts(existing, new)
    assert len(merged) == 4
    assert added == 2


def test_merge_empty_existing():
    """Empty existing list should accept all new."""
    new = [
        {"parameter_id": "PAR-A", "context": "ctx1"},
        {"parameter_id": "PAR-B", "context": "ctx2"},
    ]
    merged, added = merge_contexts([], new)
    assert len(merged) == 2
    assert added == 2


def test_merge_empty_new():
    """Empty new list should not change existing."""
    existing = [{"parameter_id": "PAR-A", "context": "ctx1"}]
    merged, added = merge_contexts(existing, [])
    assert len(merged) == 1
    assert added == 0


def test_merge_same_param_different_contexts():
    """Same parameter_id with different contexts should all be kept."""
    existing = [{"parameter_id": "PAR-A", "context": "finance"}]
    new = [
        {"parameter_id": "PAR-A", "context": "health"},
        {"parameter_id": "PAR-A", "context": "career"},
    ]
    merged, added = merge_contexts(existing, new)
    assert len(merged) == 3
    assert added == 2


# ---------------------------------------------------------------------------
# check_new_labels tests
# ---------------------------------------------------------------------------

def test_check_labels_all_mapped():
    """No unmapped labels when all are in scales."""
    scales = {
        "scales": {
            "psi_I": {"values": {"market_regulatory_environment": {}}},
            "psi_E": {"values": {"moderate_stakes_auction": {}}},
        }
    }
    contexts = [
        {"psi_conditions": {"psi_I": "market_regulatory_environment", "psi_E": "moderate_stakes_auction"}},
    ]
    unmapped = check_new_labels(contexts, scales)
    assert len(unmapped) == 0


def test_check_labels_unmapped_detected():
    """Unmapped labels should be detected."""
    scales = {
        "scales": {
            "psi_I": {"values": {"market_regulatory_environment": {}}},
        }
    }
    contexts = [
        {"psi_conditions": {"psi_I": "brand_new_label_not_in_scales"}},
    ]
    unmapped = check_new_labels(contexts, scales)
    assert "psi_I" in unmapped
    assert "brand_new_label_not_in_scales" in unmapped["psi_I"]


def test_check_labels_unknown_dimension_ignored():
    """Labels in dimensions not defined in scales should be ignored."""
    scales = {
        "scales": {
            "psi_I": {"values": {"x": {}}},
        }
    }
    contexts = [
        {"psi_conditions": {"psi_X": "anything"}},  # psi_X not in scales
    ]
    unmapped = check_new_labels(contexts, scales)
    assert len(unmapped) == 0


def test_check_labels_no_duplicates():
    """Same unmapped label from multiple contexts should appear only once."""
    scales = {
        "scales": {
            "psi_S": {"values": {"existing_label": {}}},
        }
    }
    contexts = [
        {"psi_conditions": {"psi_S": "missing_label"}},
        {"psi_conditions": {"psi_S": "missing_label"}},
        {"psi_conditions": {"psi_S": "missing_label"}},
    ]
    unmapped = check_new_labels(contexts, scales)
    assert unmapped.get("psi_S", []).count("missing_label") == 1


def test_check_labels_empty_psi_ignored():
    """Contexts with empty psi_conditions should be fine."""
    scales = {"scales": {"psi_I": {"values": {"x": {}}}}}
    contexts = [{"psi_conditions": {}}]
    unmapped = check_new_labels(contexts, scales)
    assert len(unmapped) == 0


# ---------------------------------------------------------------------------
# DOMAIN_PSI_MAP tests
# ---------------------------------------------------------------------------

def test_domain_psi_map_has_finance():
    """Finance domain should be in the map."""
    assert "finance" in DOMAIN_PSI_MAP


def test_domain_psi_map_has_health():
    """Health domain should be in the map."""
    assert "health" in DOMAIN_PSI_MAP


def test_domain_psi_map_has_dach():
    """DACH adjusted should be in the map."""
    assert "dach_adjusted" in DOMAIN_PSI_MAP


def test_domain_psi_map_values_are_dicts():
    """All domain mappings should be dicts."""
    for domain, psi in DOMAIN_PSI_MAP.items():
        assert isinstance(psi, dict), f"{domain} mapping is not a dict"


def test_domain_psi_map_labels_are_strings():
    """All psi labels should be non-empty strings."""
    for domain, psi in DOMAIN_PSI_MAP.items():
        for dim, label in psi.items():
            assert isinstance(label, str) and len(label) > 0, \
                f"{domain}.{dim} label is not a valid string: {label!r}"


def test_domain_psi_map_dimensions_valid():
    """All dimension keys should start with 'psi_'."""
    valid_dims = {"psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"}
    for domain, psi in DOMAIN_PSI_MAP.items():
        for dim in psi:
            assert dim in valid_dims, \
                f"{domain} has invalid dimension {dim}, expected one of {valid_dims}"


def test_domain_psi_map_minimum_domains():
    """Should have at least 10 domain mappings."""
    assert len(DOMAIN_PSI_MAP) >= 10, \
        f"Expected >=10 domains, got {len(DOMAIN_PSI_MAP)}"


# ---------------------------------------------------------------------------
# PREFIX_DOMAIN_MAP tests
# ---------------------------------------------------------------------------

def test_prefix_domain_map_has_known_prefixes():
    """Should contain expected parameter prefixes."""
    expected = ["PAR-HLT", "PAR-PP", "PAR-SF", "PAR-COMP"]
    for prefix in expected:
        assert prefix in PREFIX_DOMAIN_MAP, \
            f"Expected {prefix} in PREFIX_DOMAIN_MAP"


def test_prefix_domain_map_values_in_domain_psi_map():
    """All PREFIX_DOMAIN_MAP values must reference valid DOMAIN_PSI_MAP domains."""
    for prefix, domain in PREFIX_DOMAIN_MAP.items():
        assert domain in DOMAIN_PSI_MAP, \
            f"PREFIX_DOMAIN_MAP[{prefix}]={domain!r} not found in DOMAIN_PSI_MAP"


def test_prefix_domain_map_minimum_entries():
    """Should have at least 10 prefix mappings."""
    assert len(PREFIX_DOMAIN_MAP) >= 10, \
        f"Expected >=10 prefix mappings, got {len(PREFIX_DOMAIN_MAP)}"


def test_prefix_domain_map_keys_are_par_prefixes():
    """All keys should look like PAR-XXX (uppercase prefix)."""
    for prefix in PREFIX_DOMAIN_MAP:
        assert prefix.startswith("PAR-"), \
            f"Unexpected prefix format: {prefix!r}, expected PAR-XXX"


# ---------------------------------------------------------------------------
# Path 4 tests: non-standard value key extraction
# ---------------------------------------------------------------------------

PARAM_NONSTANDARD_DIRECT_MATCH = {
    "id": "PAR-TEST-P4A",
    "symbol": "alpha_p4a",
    "name": "Path 4 Direct Match",
    "values": {
        "laboratory": {
            "mean": 0.65,
            "ci_68": [0.55, 0.75],
        },
    },
}

PARAM_NONSTANDARD_PARTIAL_MATCH = {
    "id": "PAR-TEST-P4B",
    "symbol": "alpha_p4b",
    "name": "Path 4 Partial Match",
    "values": {
        "laboratory_experiment": {
            "mean": 0.70,
        },
    },
}

PARAM_NONSTANDARD_PREFIX_FALLBACK = {
    "id": "PAR-HLT-099",
    "symbol": "alpha_p4c",
    "name": "Path 4 Prefix Fallback",
    "values": {
        "individual_MW": {
            "mean": 0.42,
        },
    },
}

PARAM_NONSTANDARD_SCALAR = {
    "id": "PAR-TEST-P4D",
    "symbol": "alpha_p4d",
    "name": "Path 4 Scalar Value",
    "values": {
        "welfare": 3.14,
    },
}

PARAM_NONSTANDARD_SKIPS_STANDARD = {
    "id": "PAR-TEST-P4E",
    "symbol": "alpha_p4e",
    "name": "Path 4 Standard Keys Skipped",
    "values": {
        "note": "some note",
        "unit": "ratio",
        "range": [0, 1],
        "ci_68": [0.4, 0.6],
    },
}


def test_path4_direct_match():
    """Path 4: value key 'laboratory' matches DOMAIN_PSI_MAP directly."""
    contexts = extract_param_contexts(PARAM_NONSTANDARD_DIRECT_MATCH)
    lab_ctx = [c for c in contexts if c["context"] == "laboratory_context"]
    assert len(lab_ctx) == 1, \
        f"Expected 1 laboratory_context, got {[c['context'] for c in contexts]}"
    assert "psi_F" in lab_ctx[0]["psi_conditions"]
    assert lab_ctx[0]["psi_conditions"]["psi_F"] == "laboratory_setting"


def test_path4_direct_match_value():
    """Path 4: value with CI should be formatted correctly."""
    contexts = extract_param_contexts(PARAM_NONSTANDARD_DIRECT_MATCH)
    lab_ctx = [c for c in contexts if c["context"] == "laboratory_context"][0]
    assert "0.65" in lab_ctx["value_estimate"]
    assert "CI:" in lab_ctx["value_estimate"]


def test_path4_partial_match():
    """Path 4: value key 'laboratory_experiment' partially matches 'laboratory'."""
    contexts = extract_param_contexts(PARAM_NONSTANDARD_PARTIAL_MATCH)
    assert len(contexts) >= 1, \
        f"Expected >=1 context for partial match, got {len(contexts)}"
    ctx = contexts[0]
    assert "psi_F" in ctx["psi_conditions"] or "psi_I" in ctx["psi_conditions"]


def test_path4_prefix_fallback():
    """Path 4: unknown key 'individual_MW' falls back to PREFIX_DOMAIN_MAP via PAR-HLT."""
    contexts = extract_param_contexts(PARAM_NONSTANDARD_PREFIX_FALLBACK)
    assert len(contexts) >= 1, \
        f"Expected >=1 context via prefix fallback, got {len(contexts)}"
    ctx = [c for c in contexts if c["context"] == "individual_MW_context"]
    assert len(ctx) == 1
    # PAR-HLT → healthcare_germany → psi_I: medical_gatekeeping
    assert ctx[0]["psi_conditions"].get("psi_I") == "medical_gatekeeping"


def test_path4_scalar_value():
    """Path 4: scalar (non-dict) value should be converted to string."""
    contexts = extract_param_contexts(PARAM_NONSTANDARD_SCALAR)
    welfare_ctx = [c for c in contexts if c["context"] == "welfare_context"]
    assert len(welfare_ctx) == 1
    assert "3.14" in welfare_ctx[0]["value_estimate"]


def test_path4_skips_standard_keys():
    """Path 4: standard keys (note, unit, range, ci_68, ci_95) should be skipped."""
    contexts = extract_param_contexts(PARAM_NONSTANDARD_SKIPS_STANDARD)
    assert len(contexts) == 0, \
        f"Expected 0 contexts for standard-only keys, got {[c['context'] for c in contexts]}"


def test_path4_study_type():
    """Path 4: study_type should be 'registry_derived'."""
    contexts = extract_param_contexts(PARAM_NONSTANDARD_DIRECT_MATCH)
    for c in contexts:
        if c["context"] == "laboratory_context":
            assert c["study_type"] == "registry_derived"


def test_path4_dedup_vs_path1():
    """Path 4: should not duplicate a context already extracted by path 1."""
    param = {
        "id": "PAR-TEST-P4F",
        "symbol": "alpha_p4f",
        "name": "Path 4 Dedup Test",
        "values": {
            "domain_specific": {
                "finance": {"mean": 1.0},
            },
            "finance": {"mean": 1.0},  # same domain as path 1 but as top-level key
        },
    }
    contexts = extract_param_contexts(param)
    finance_contexts = [c for c in contexts if "finance" in c["context"]]
    # Path 1 creates "finance_context" from domain_specific,
    # Path 4 should skip duplicate "finance_context"
    assert len(finance_contexts) == 1, \
        f"Expected exactly 1 finance context (dedup), got {len(finance_contexts)}"


def test_path4_no_match_no_context():
    """Path 4: completely unknown key with no prefix mapping → no context."""
    param = {
        "id": "PAR-TEST-P4G",
        "symbol": "alpha_p4g",
        "name": "Path 4 No Match",
        "values": {
            "xyzzy_unknown_key": {"mean": 0.5},
        },
    }
    contexts = extract_param_contexts(param)
    assert len(contexts) == 0


# ---------------------------------------------------------------------------
# Path 5 tests: prefix-based fallback for empty parameters
# ---------------------------------------------------------------------------

PARAM_PATH5_KNOWN_PREFIX = {
    "id": "PAR-COMP-999",
    "symbol": "gamma_p5a",
    "name": "Path 5 Known Prefix",
    "values": {},
}

PARAM_PATH5_UNKNOWN_PREFIX = {
    "id": "PAR-ZZZZZ-001",
    "symbol": "gamma_p5b",
    "name": "Path 5 Unknown Prefix",
    "values": {},
}


def test_path5_known_prefix_produces_context():
    """Path 5: empty param with known prefix (PAR-COMP) → 1 context."""
    contexts = extract_param_contexts(PARAM_PATH5_KNOWN_PREFIX)
    assert len(contexts) == 1, \
        f"Expected 1 context from prefix fallback, got {len(contexts)}"


def test_path5_study_type_inferred():
    """Path 5: study_type should be 'registry_inferred' (not registry_derived)."""
    contexts = extract_param_contexts(PARAM_PATH5_KNOWN_PREFIX)
    assert len(contexts) == 1
    assert contexts[0]["study_type"] == "registry_inferred"


def test_path5_source_contains_prefix_fallback():
    """Path 5: source_in_paper should mention prefix fallback."""
    contexts = extract_param_contexts(PARAM_PATH5_KNOWN_PREFIX)
    assert "prefix fallback" in contexts[0]["source_in_paper"]


def test_path5_context_name_from_domain():
    """Path 5: context name should be {domain}_context from PREFIX_DOMAIN_MAP."""
    contexts = extract_param_contexts(PARAM_PATH5_KNOWN_PREFIX)
    # PAR-COMP → complementarity → complementarity_context
    assert contexts[0]["context"] == "complementarity_context"


def test_path5_psi_conditions_from_domain():
    """Path 5: psi_conditions from PREFIX_DOMAIN_MAP → DOMAIN_PSI_MAP chain."""
    contexts = extract_param_contexts(PARAM_PATH5_KNOWN_PREFIX)
    # complementarity → psi_I: academic_methodology
    assert contexts[0]["psi_conditions"].get("psi_I") == "academic_methodology"


def test_path5_unknown_prefix_no_context():
    """Path 5: unknown prefix (PAR-ZZZZZ) → 0 contexts."""
    contexts = extract_param_contexts(PARAM_PATH5_UNKNOWN_PREFIX)
    assert len(contexts) == 0


def test_path5_not_triggered_when_paths123_produce():
    """Path 5: should NOT trigger if paths 1-3 already produced contexts."""
    # PARAM_LITERATURE_ONLY produces 1 context from path 3
    # Even if we fake a known prefix, path 5 should not add another
    param = {
        "id": "PAR-COMP-888",
        "symbol": "gamma_p5c",
        "name": "Path 5 Not Triggered",
        "values": {
            "literature": {"mean": 0.9},
        },
    }
    contexts = extract_param_contexts(param)
    # Should have literature_baseline from path 3, but NOT a path 5 fallback
    study_types = [c["study_type"] for c in contexts]
    assert "registry_inferred" not in study_types, \
        f"Path 5 should not trigger when path 3 produced contexts"


# ---------------------------------------------------------------------------
# Integration tests (with real data)
# ---------------------------------------------------------------------------

def test_real_registry_extraction():
    """Extraction from real parameter-registry should produce contexts."""
    registry = load_yaml(PARAM_REGISTRY_PATH)
    if not registry:
        print("  SKIP (parameter-registry.yaml not found)")
        return
    contexts = extract_all_param_contexts(registry)
    assert len(contexts) > 20, \
        f"Expected >20 contexts from real registry, got {len(contexts)}"


def test_real_registry_has_known_parameter():
    """PAR-BEH-001 should produce contexts from real registry."""
    registry = load_yaml(PARAM_REGISTRY_PATH)
    if not registry:
        print("  SKIP (parameter-registry.yaml not found)")
        return
    contexts = extract_all_param_contexts(registry)
    beh001 = [c for c in contexts if c["parameter_id"] == "PAR-BEH-001"]
    assert len(beh001) >= 2, \
        f"Expected >=2 contexts for PAR-BEH-001, got {len(beh001)}"


def test_real_merge_idempotent():
    """Merging extracted contexts with themselves should add 0."""
    registry = load_yaml(PARAM_REGISTRY_PATH)
    if not registry:
        print("  SKIP (parameter-registry.yaml not found)")
        return
    contexts = extract_all_param_contexts(registry)
    merged, added = merge_contexts(contexts, contexts)
    assert added == 0, f"Expected 0 added on self-merge, got {added}"
    assert len(merged) == len(contexts)


def test_real_labels_mapped():
    """All extracted labels should be mapped in psi-scales."""
    registry = load_yaml(PARAM_REGISTRY_PATH)
    scales = load_yaml(PSI_SCALES_PATH)
    if not registry or not scales:
        print("  SKIP (data files not found)")
        return
    contexts = extract_all_param_contexts(registry)
    unmapped = check_new_labels(contexts, scales)
    total_unmapped = sum(len(v) for v in unmapped.values())
    assert total_unmapped == 0, \
        f"Found {total_unmapped} unmapped labels: {unmapped}"


def test_real_existing_contexts_mergeable():
    """Real existing contexts should merge without error."""
    existing_data = load_yaml(EXISTING_CONTEXTS_PATH)
    registry = load_yaml(PARAM_REGISTRY_PATH)
    if not existing_data or not registry:
        print("  SKIP (data files not found)")
        return
    existing = existing_data.get("triplets", [])
    new = extract_all_param_contexts(registry)
    merged, added = merge_contexts(existing, new)
    assert len(merged) >= len(existing), \
        f"Merged ({len(merged)}) should be >= existing ({len(existing)})"


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        # extract_param_contexts
        test_extract_domain_contexts,
        test_extract_domain_psi_conditions,
        test_extract_domain_value_with_ci,
        test_extract_dach_adjusted,
        test_extract_literature_baseline,
        test_extract_literature_uses_first_source,
        test_extract_literature_fallback_no_sources,
        test_extract_empty_values,
        test_extract_unknown_domain_skipped,
        test_extract_parameter_id_preserved,
        test_extract_parameter_symbol_preserved,
        test_extract_full_param_context_count,
        test_extract_partial_domain_match,
        # extract_all_param_contexts
        test_extract_all_iterates_parameter_sections,
        test_extract_all_skips_non_parameter_keys,
        test_extract_all_empty_registry,
        test_extract_all_aggregates_counts,
        # merge_contexts
        test_merge_no_duplicates,
        test_merge_dedup_same_key,
        test_merge_partial_overlap,
        test_merge_empty_existing,
        test_merge_empty_new,
        test_merge_same_param_different_contexts,
        # check_new_labels
        test_check_labels_all_mapped,
        test_check_labels_unmapped_detected,
        test_check_labels_unknown_dimension_ignored,
        test_check_labels_no_duplicates,
        test_check_labels_empty_psi_ignored,
        # DOMAIN_PSI_MAP
        test_domain_psi_map_has_finance,
        test_domain_psi_map_has_health,
        test_domain_psi_map_has_dach,
        test_domain_psi_map_values_are_dicts,
        test_domain_psi_map_labels_are_strings,
        test_domain_psi_map_dimensions_valid,
        test_domain_psi_map_minimum_domains,
        # PREFIX_DOMAIN_MAP
        test_prefix_domain_map_has_known_prefixes,
        test_prefix_domain_map_values_in_domain_psi_map,
        test_prefix_domain_map_minimum_entries,
        test_prefix_domain_map_keys_are_par_prefixes,
        # Path 4: non-standard value keys
        test_path4_direct_match,
        test_path4_direct_match_value,
        test_path4_partial_match,
        test_path4_prefix_fallback,
        test_path4_scalar_value,
        test_path4_skips_standard_keys,
        test_path4_study_type,
        test_path4_dedup_vs_path1,
        test_path4_no_match_no_context,
        # Path 5: prefix fallback for empty params
        test_path5_known_prefix_produces_context,
        test_path5_study_type_inferred,
        test_path5_source_contains_prefix_fallback,
        test_path5_context_name_from_domain,
        test_path5_psi_conditions_from_domain,
        test_path5_unknown_prefix_no_context,
        test_path5_not_triggered_when_paths123_produce,
        # Integration
        test_real_registry_extraction,
        test_real_registry_has_known_parameter,
        test_real_merge_idempotent,
        test_real_labels_mapped,
        test_real_existing_contexts_mergeable,
    ]

    passed = 0
    failed = 0
    errors = []

    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS  {test.__name__}")
        except AssertionError as e:
            failed += 1
            errors.append((test.__name__, str(e)))
            print(f"  FAIL  {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            errors.append((test.__name__, str(e)))
            print(f"  ERROR {test.__name__}: {e}")

    print(f"\n{'=' * 40}")
    print(f"  {passed} passed, {failed} failed, {passed + failed} total")
    if errors:
        print(f"\n  Failures:")
        for name, err in errors:
            print(f"    {name}: {err}")
    print()

    sys.exit(0 if failed == 0 else 1)
