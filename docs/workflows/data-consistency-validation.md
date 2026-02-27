# Data Consistency Validation Framework

> Ensuring data integrity, cross-database consistency, and contextual coherence across the EBF ecosystem.

**Version:** 1.0
**Date:** January 2026
**Status:** Active

---

## Overview

The EBF Framework relies on multiple interconnected data sources:

| Database | Purpose | Key Fields |
|----------|---------|------------|
| `model-registry.yaml` | EBF-built models | 10C mapping, theory basis, sessions |
| `theory-catalog.yaml` | 134 scientific theories | EBF restrictions, bib_keys |
| `case-registry.yaml` | Real-world cases | 10C dimensions, formulas |
| `intervention-registry.yaml` | Project tracking | Predictions, results, learnings |
| `parameter-registry.yaml` | Canonical parameters | Ranges, sources, confidence |
| `concept-registry.yaml` | EIP-validated concepts | Evidence, decisions |
| `bcm_master.bib` | 2200+ papers | Citations, theory support |
| `BCM2 context files` | 400+ context factors | Values, APIs, timestamps |

**Challenge:** With so many interconnected sources, ensuring consistency is critical.

---

## The Three Pillars of Data Consistency

### 1. Referential Integrity

**Question:** Do all cross-references point to existing entities?

```
model-registry → theory-catalog     ✓ Theory IDs exist?
model-registry → bcm_master.bib     ✓ Paper keys exist?
model-registry → sessions           ✓ Session IDs exist?
case-registry  → appendices         ✓ Appendix codes exist?
case-registry  → chapters           ✓ Chapter numbers exist?
theory-catalog → bcm_master.bib     ✓ BibTeX keys exist?
```

**Script:** `scripts/validate_referential_integrity.py`

**Usage:**
```bash
# Basic check
python scripts/validate_referential_integrity.py

# Verbose output
python scripts/validate_referential_integrity.py --verbose

# With auto-fix suggestions
python scripts/validate_referential_integrity.py --fix
```

**Threshold:** Score ≥ 85% required for commits

---

### 2. Parameter Consistency

**Question:** Are behavioral economics parameters used consistently?

| Parameter | Symbol | Typical Range | Source |
|-----------|--------|---------------|--------|
| Loss Aversion | λ | 2.0-2.5 | Kahneman & Tversky (1992) |
| Present Bias | β | 0.7-1.0 | Laibson (1997) |
| Time Discount | δ | 0.9-1.0 | Frederick et al. (2002) |
| Complementarity | γ | -0.5 to 0.7 | EBF (Chapter 10) |
| Risk Aversion | α | 0.5-2.0 | Mehra & Prescott (1985) |

**Checks:**
1. **Range Validity:** Parameters within theoretical bounds
2. **Cross-Database Consistency:** Same parameter has consistent values
3. **Theory-Model Alignment:** Model parameters respect theory restrictions
4. **Drift Detection:** >20% deviation triggers review

**Script:** `scripts/validate_parameter_consistency.py`

**Usage:**
```bash
# Basic check
python scripts/validate_parameter_consistency.py

# Generate detailed report
python scripts/validate_parameter_consistency.py --report

# Verbose with all warnings
python scripts/validate_parameter_consistency.py --verbose
```

**Deviation Thresholds:**
- 10%: Warning logged
- 20%: Review recommended
- 50%: Critical (blocks commit)

---

### 3. Context Consistency

**Question:** Are Ψ dimensions used consistently without contradictions?

**The 8 Ψ Dimensions:**

| Dimension | Name | Description |
|-----------|------|-------------|
| Ψ_I | Institutional | Rules, defaults, regulations |
| Ψ_S | Social | Norms, peers, identity |
| Ψ_K | Cultural | Values, traditions |
| Ψ_C | Cognitive | State, attention, fatigue |
| Ψ_E | Economic | Resources, constraints |
| Ψ_T | Temporal | Timing, lifecycle |
| Ψ_M | Material | Technology, tools |
| Ψ_F | Physical | Location, environment |

**Checks:**
1. **Factor Existence:** Referenced context factors exist in BCM2
2. **Hierarchy Completeness:** MACRO → MESO → MICRO respected
3. **Ψ Coverage:** Relevant dimensions considered
4. **Cross-Analysis Consistency:** Same context consistent across analyses
5. **Data Freshness:** External APIs not stale

**Script:** `scripts/validate_context_consistency.py`

**Usage:**
```bash
# Basic check
python scripts/validate_context_consistency.py

# With data freshness check
python scripts/validate_context_consistency.py --check-freshness

# Verbose output
python scripts/validate_context_consistency.py --verbose
```

---

## Context Hierarchy (MACRO → MESO → MICRO)

```
┌─────────────────────────────────────────────────────────────────┐
│  MACRO (Country/Market)                                         │
│  ├── BCM2_04_KON_*.yaml (404 factors)                          │
│  └── National parameters: λ_CH, trust_CH, culture              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  MESO (Industry/Client)                                         │
│  ├── clients/bfe/*.yaml, customers/porr/*.yaml                 │
│  └── Domain modifiers: λ_BFE = λ_CH × 1.2                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  MICRO (Situation/Individual)                                   │
│  ├── context-dimensions.yaml (5 MICRO questions)               │
│  ├── BCM2_05_IND_individual.yaml (48 factors)                  │
│  └── Situational modifiers: × 1.3 (workplace) × 1.4 (stress)   │
└─────────────────────────────────────────────────────────────────┘
```

**Rule:** Always define MACRO before MESO before MICRO.

---

## Pre-Commit Automation

The pre-commit hook automatically runs all three validators when registry files are modified:

```
=== EBF PreCommit: Data Consistency Validation ===
Checking referential integrity...
✅ REFERENTIAL INTEGRITY: Score 97.5% (0 critical errors)
Checking parameter consistency...
✅ PARAMETER CONSISTENCY: Score 92.3%
Checking context consistency...
✅ CONTEXT CONSISTENCY: Score 88.7%
```

**Blocking Rules:**
- Referential Integrity < 85% → **BLOCKS COMMIT**
- Parameter Consistency < 85% → Warning only
- Context Consistency < 85% → Warning only

---

## Common Issues & Fixes

### 1. Missing Session Reference

**Error:**
```
Model EBF-MOD-001 references non-existent session: EBF-S-2026-01-25-REL-001
```

**Fix:** Add the session to `model-building-session.yaml` or update the model reference.

### 2. Paper Key Not Found

**Error:**
```
Theory MS-IB-001 references non-existent paper: akerlof2000identity
```

**Fix:** Add the paper to `bcm_master.bib` or correct the key (check spelling, year).

### 3. Parameter Range Violation

**Error:**
```
Parameter lambda=5.2 outside hard bounds [1.0, 5.0]
```

**Fix:** Review the parameter source. If valid, update `PARAMETER_SPECS` with justification.

### 4. Cross-Analysis Conflict

**Error:**
```
Context parameter 'trust_institutions' varies 35.2% across finance analyses
```

**Fix:** Check if different values are context-appropriate or standardize.

### 5. Incomplete Context Hierarchy

**Error:**
```
Model EBF-MOD-REF-001 missing context hierarchy levels: {'MICRO'}
```

**Fix:** Add MICRO-level context sources to the model's `data_sources`.

---

## Manual Validation Commands

Run all validators at once:

```bash
# Quick health check
python scripts/validate_referential_integrity.py && \
python scripts/validate_parameter_consistency.py && \
python scripts/validate_context_consistency.py

# Full report
python scripts/validate_referential_integrity.py --verbose
python scripts/validate_parameter_consistency.py --report
python scripts/validate_context_consistency.py --check-freshness --verbose
```

---

## Integration with EBF Workflow

### During Model Building (Step 7)

When saving results in Step 7, the session tracking ensures:
- Session ID is recorded
- Model references are valid
- Parameters are logged

### During Quality Check (Step 8)

Step 8 explicitly checks:
```
┌─────────────────────────────────────────────────────────────────┐
│  CHECK                              │ STATUS │ AKTION           │
├─────────────────────────────────────┼────────┼──────────────────┤
│  Model in model-registry.yaml?      │ ✅/❌  │ → Hinzufügen     │
│  Papers with 6 EBF fields?          │ ✅/❌  │ → Ergänzen       │
│  Session documented?                │ ✅/❌  │ → Vervollständ.  │
│  Data sources valid?                │ ✅/❌  │ → Korrigieren    │
└─────────────────────────────────────┴────────┴──────────────────┘
```

---

## Architecture Diagram

```
                    ┌─────────────────────┐
                    │   Pre-Commit Hook   │
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ validate_     │    │ validate_     │    │ validate_     │
│ referential_  │    │ parameter_    │    │ context_      │
│ integrity.py  │    │ consistency.py│    │ consistency.py│
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                         DATA LAYER                           │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│ model-      │ theory-     │ case-       │ BCM2 context      │
│ registry    │ catalog     │ registry    │ files (400+)      │
├─────────────┼─────────────┼─────────────┼───────────────────┤
│ intervention│ concept-    │ parameter-  │ bcm_master.bib    │
│ -registry   │ registry    │ registry    │ (2200+ papers)    │
└─────────────┴─────────────┴─────────────┴───────────────────┘
```

---

## Best Practices

1. **Always run validators before major commits**
   ```bash
   python scripts/validate_referential_integrity.py
   ```

2. **Use SSOT pattern** - Single Source of Truth for each data type

3. **Document parameter sources** - Every parameter should trace to literature

4. **Maintain context hierarchy** - MACRO → MESO → MICRO, never skip levels

5. **Check freshness quarterly** - External APIs may become stale

6. **Log deviations** - Parameter drift should be documented in `theory-learning-log.yaml`

---

## Related Documentation

- [Evidence Integration Pipeline](evidence-integration-pipeline.md) - How new concepts are validated
- [EBF Workflow](../EBF-INTRODUCTION.md) - The 10-step analysis workflow
- [Exclusion Principle](../../appendices/FRM_LIT-FEHR-METHOD_integration_vs_falsifiability.tex) - Formula consistency rules (EXC-1 to EXC-6)

---

*Version 1.0 | January 2026*
