# GPM 3.0: Goalkeeper Performance Model

**Status:** DRAFT | **Version:** 3.0.0 | **Created:** 2026-02-16 | **Updated:** 2026-02-17

## Overview

Multi-dimensional framework for systematic evaluation of goalkeeper techniques and training time allocation. The model decomposes goalkeeper performance into three interdependent levels -- strategic, tactical, operative -- embedded in a team performance system (Leistungsverbund). Includes injury risk dimension (D6), Visibility-Contribution framework, and effective value (V\*_eff) availability model.

**Working Paper:** `outputs/medium/working-papers/WP-001_goalkeeper_performance_framework.tex`

## Core Architecture

### Three-Level Performance Decomposition

```
L(GK) = f(L_S, L_T, L_O) | Team Context Φ
```

| Level | Symbol | Central Question |
|-------|--------|------------------|
| **Strategic** | L_S | Does the GK make the TEAM better? |
| **Tactical** | L_T | Does the GK make the RIGHT decision? |
| **Operative** | L_O | Does the GK EXECUTE cleanly? |

The three levels are **complementary** (not substitutable):

```
∂²L/∂L_i∂L_j > 0  for all i,j ∈ {S,T,O}, i≠j
```

Complementarity parameters:
- γ_ST = 0.45 (Strategic × Tactical)
- γ_SO = 0.30 (Strategic × Operative)
- γ_TO = 0.50 (Tactical × Operative)

### Six-Dimension Technique Evaluation

Each technique is scored across six dimensions:

| Dim | Name | Weight | Symbol |
|-----|------|--------|--------|
| D1 | Game Relevance | 25% | R |
| D2 | Risk Reduction | 22% | ρ |
| D3 | Learning Efficiency | 13% | η |
| D4 | Coach Transmissibility | 8% | τ |
| D5 | Strategic Potential | 17% | Π |
| D6 | Injury Risk | 15% | ι |

D6 is a composite: **D6 = 0.5 × D6a (non-contact) + 0.5 × D6b (contact)**. Inverted scale: 1.0 = safest.

**Score:** S(t) = Σ w_i × D_i(t)

### Key Finding: Catching vs Blocking

| Dimension | Catching | Blocking | Winner |
|-----------|----------|----------|--------|
| Game Relevance (R) | 0.85 | 0.20 | **Catching** |
| Risk Reduction (ρ) | 0.95 | 0.50 | **Catching** |
| Learning Efficiency (η) | 0.55 | 0.35 | **Catching** |
| Coach Transmissibility (τ) | 0.80 | 0.30 | **Catching** |
| Strategic Potential (Π) | 0.90 | 0.10 | **Catching** |
| Injury Risk (ι) | 0.70 | 0.225 | **Catching** |
| **Total Score** | **0.815** | **0.280** | **Catching (6/6)** |

Block is **3.1x more dangerous** than catching (D6: 0.225 vs 0.70).

### Visibility-Contribution Framework

Based on Holmstrom-Milgrom (1991) multi-task theory:

```
Position V-C Spectrum: ST(+0.85) → W(+0.65) → CM(+0.40) → CB(+0.10) → GK(-0.15)
```

The GK has a **negative** Visibility-Contribution correlation: the most valuable actions (prevention, positioning) are invisible, while the most visible (spectacular saves) are least important.

### Effective Value: V\*_eff

```
V*_eff = V* × A × D
```

- **V\*** = true performance value
- **A** = availability (matches_available / total_matches) -- **veto factor** (A=0 → V\*_eff=0)
- **D** = career durability

Key prediction: An available average GK (V\*=0.6, A=0.95) outperforms an injury-prone elite GK (V\*=0.8, A=0.5) in effective value.

## Usage

```bash
# Run all analyses
python models/GPM-1-0-GOALKEEPER-PERFORMANCE/gpm_model.py --all

# Specific analyses
python models/GPM-1-0-GOALKEEPER-PERFORMANCE/gpm_model.py --evaluate
python models/GPM-1-0-GOALKEEPER-PERFORMANCE/gpm_model.py --compare
python models/GPM-1-0-GOALKEEPER-PERFORMANCE/gpm_model.py --allocate
python models/GPM-1-0-GOALKEEPER-PERFORMANCE/gpm_model.py --complementarity
python models/GPM-1-0-GOALKEEPER-PERFORMANCE/gpm_model.py --substitution
python models/GPM-1-0-GOALKEEPER-PERFORMANCE/gpm_model.py --profiles
```

## Files

| File | Purpose |
|------|---------|
| `model-definition.yaml` | SSOT: Complete model specification |
| `gpm_model.py` | Python implementation (v3.0) |
| `test_gpm_model.py` | Unit tests (105 tests, 12 predictions) |
| `__init__.py` | Python package module |
| `conftest.py` | Pytest configuration |
| `README.md` | This documentation |

## EEE Workflow Formalization (10C Mapping)

Designed via EEE Workflow (SCHNELL mode) | Formalized: 2026-02-16

| 10C | CORE | GPM-3.0 Mapping |
|-----|------|-----------------|
| **WHO** | AAA | 3 levels: GK (individual), Coach (organization), Team (system) |
| **WHAT** | C | 6 dimensions: R, ρ, η, τ, Π, ι (domain-specific, not standard FEPSDE) |
| **HOW** | B | Three-level complementarity: γ_ST=0.45, γ_SO=0.30, γ_TO=0.50 |
| **WHEN** | V | Ψ_I (institutional), Ψ_S (social media), Ψ_C (cognitive), Ψ_T (temporal), Ψ_M (tools) |
| **WHERE** | BBB | Hybrid: Tier 1 literature + Tier 3 empirical + Tier 4 expert |
| **AWARE** | AU | 3 biases distort awareness: availability, small sample, isolation |
| **READY** | AV | Coach transmissibility (τ) as readiness proxy |
| **STAGE** | AW | F1 Simulator 3-step adoption: Record → Redesign → Calibrate |
| **HIERARCHY** | HI | L_S (strategic) > L_T (tactical) > L_O (operative) |
| **EIT** | IE | Training allocation vector [T_catch, T_parry, T_block, T_punch, T_foot] |

**Entry Point:** Practice-Driven (correcting bias-driven training misallocation)
**Scope:** Continuous (ongoing training optimization, not one-time decision)
**Functional Forms:** EXC-1 (additive default) for technique scoring; EXC-3 (hybrid) for performance model

## Empirical Case Studies (3 Reference Profiles)

Three real-world goalkeeper profiles validate GPM-3.0 predictions:

| Profile | L_S | L_T | L_O | Type | V\*_eff | Validates |
|---------|-----|-----|-----|------|---------|-----------|
| **Manuel Neuer** | 0.90 | 0.75 | 0.80 | Strategic Specialist | 0.480 | PRED-006, PRED-008 |
| **Alisson Becker** | 0.80 | 0.80 | 0.85 | Balanced Excellence | 0.610 | PRED-004, PRED-002 |
| **Thibaut Courtois** | 0.55 | 0.65 | 0.88 | Operative Specialist | 0.088 | PRED-011, PRED-009 |

### Key Findings

- **PRED-004 validated:** Alisson's balanced profile yields highest complementarity share (50.4%) -- balanced L_S × L_T × L_O maximizes γ-bonus
- **PRED-006 validated:** Neuer's strategic dominance (L_S=0.90) outperforms despite lower L_O -- positioning > spectacle
- **PRED-011 validated:** Courtois' V\*_eff collapses from 0.586 to 0.088 during ACL tear season (A=0.15) -- availability is a veto factor

### Training Allocations

| Technique | Neuer | Alisson | Courtois |
|-----------|-------|---------|----------|
| Catching | 38% | 35% | 30% |
| Parry (safe) | 22% | 24% | 20% |
| Blocking | 5% | 6% | 12% |
| Punching | 15% | 14% | 18% |
| Foot Save | 8% | 6% | 10% |
| Distribution | 12% | 15% | 10% |

All three profiles allocate <12% to blocking, consistent with the catching-first principle.

**Case Registry:** CAS-946 (Neuer), CAS-947 (Alisson), CAS-948 (Courtois)

## Identified Biases in Current Practice

1. **Social Media Availability Bias** -- Spectacular blocks go viral, routine catches don't
2. **Small Sample Illusion** -- 4-5 shots/game means single events become philosophy
3. **Technique Isolation Bias** -- Training techniques without decision context

## The F1 Simulator Principle

Training should mirror match frequency distributions:
- Record actual action distribution across 5 matches
- Design sequences with realistic frequency and decision pressure
- Calibrate allocation via the six-dimension framework

## Parameter Registry

| ID | Symbol | Description |
|----|--------|-------------|
| PAR-SPO-001 | P_action_bias | Action Bias Probability |
| PAR-SPO-002 | Corr_VC | Visibility-Contribution Correlation |
| PAR-SPO-003 | V_prevented | Prevented Goals Fraction |
| PAR-SPO-004 | D6 | Injury Risk Score (composite) |
| PAR-SPO-005 | D6a | Non-Contact Injury Risk |
| PAR-SPO-006 | D6b | Contact Injury Risk |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-16 | Initial: 5 dimensions, 59 tests |
| 3.0 | 2026-02-17 | +D6 injury risk, Visibility framework, V\*_eff, ~85 tests |
| 3.1 | 2026-02-17 | +3 reference profiles (Neuer/Alisson/Courtois), CAS-946-948, WP-001 §10 Fallstudien, 105 tests |

## References

- Gramage Medina et al. (2025). *Coaches' perceptions on the Spread.*
- Holmstrom & Milgrom (1991). *Multitask principal-agent analyses.*
- Otte, Dittmer & West (2022). *Goalkeeping in modern football.*
- Tversky & Kahneman (1973). *Availability: A heuristic for judging frequency and probability.*
