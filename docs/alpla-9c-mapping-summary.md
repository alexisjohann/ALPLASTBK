# ALPLA Plant Categorization → EBF 10C CORE Mapping

> **Version:** 1.0 | **Date:** 2026-01-19 | **Status:** Complete Integration

## Executive Summary

Das ALPLA Plant Categorization Framework (APCF) mit seinen **9 Dimensionen** und **47 Variablen** wurde vollständig in das EBF 10C CORE Framework integriert. Diese Integration ermöglicht:

1. **Systematische Verhaltensmodellierung** von Employee Churn
2. **Theoretisch fundierte Intervention Selection** via AISA
3. **EBF-konforme Messung und Evaluation** im Feldexperiment

---

## Mapping-Übersicht: ALPLA → 10C CORE

| ALPLA Dimension | Code | 10C CORE | Appendix | Mapping |
|-----------------|------|---------|----------|---------|
| **Job Profiles (BC1-BC5)** | - | **WHO** | AAA | Welfare Levels L1-L4 |
| **FEPSDE Utility** | - | **WHAT** | C | 6 Utility-Dimensionen |
| **I (Intervention Fit)** | I1-I5 | **HOW** | B | γ-Complementarity Matrix |
| **S/L/O (Context)** | S1-O5 | **WHEN** | V | Ψ-Context Dimensions |
| **P (Performance)** | P1-P4 | **WHERE** | BBB | Parameter Θ |
| **M/K (Culture)** | M1-K5 | **AWARE** | AU | Awareness A(·) |
| **R (Readiness)** | R1-R5 | **READY** | AV | WAX, θ |
| **T (Temporal)** | T1-T5 | **STAGE** | AW | BCJ Phases S(t) |
| **Decision Levels** | - | **HIERARCHY** | HI | L0-L3, N_L2 |

---

## Detailliertes 10C Mapping

### 1. WHO (AAA): Wer hat Utility?

```
┌──────────────────────────────────────────────────────────────┐
│  WHO: ALPLA Welfare Hierarchy                                │
├──────────────────────────────────────────────────────────────┤
│  L1 (Individual)  │ BC1-BC5 Mitarbeiter                     │
│  L2 (Dyadic)      │ MA ↔ Supervisor (M4_leadership)         │
│  L3 (Team)        │ Schicht/Team (K1_cohesion)              │
│  L4 (Organization)│ Werk (P1_churn, P4_productivity)        │
├──────────────────────────────────────────────────────────────┤
│  α^L(Ψ):                                                     │
│  - Standalone:  α^L1=0.50, α^L3=0.35, α^L4=0.15            │
│  - In-House:    α^L1=0.30, α^L3=0.30, α^L4=0.40            │
│  - Regional HQ: α^L1=0.35, α^L3=0.40, α^L4=0.25            │
└──────────────────────────────────────────────────────────────┘
```

### 2. WHAT (C): Was ist Utility?

```
┌──────────────────────────────────────────────────────────────┐
│  WHAT: FEPSDE für Blue Collar Churn                         │
├──────────────────────────────────────────────────────────────┤
│  F (Financial)    │ L4_wage, INT3_skill_pay          │ ω=0.25│
│  E (Emotional)    │ K5_satisfaction, INT6_recognition│ ω=0.15│
│  P (Physical)     │ Workload, INT4_management        │ ω=0.10│
│  S (Social)       │ K1_cohesion, INT8_team           │ ω=0.15│
│  D (Development)  │ INT2_career, INT1_rotation       │ ω=0.25│
│  E (Existential)  │ Job Security (T5)                │ ω=0.10│
├──────────────────────────────────────────────────────────────┤
│  Wichtigste Churn-Treiber: Development + Financial          │
└──────────────────────────────────────────────────────────────┘
```

### 3. HOW (B): Wie interagieren Interventionen?

```
┌──────────────────────────────────────────────────────────────┐
│  HOW: Intervention Complementarity (γ-Matrix)               │
├──────────────────────────────────────────────────────────────┤
│  SYNERGIEN (γ > 0):                                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ INT1 (Rotation) ←→ INT2 (Career)     │ γ = +0.35       ││
│  │ INT2 (Career)   ←→ INT3 (Skill Pay)  │ γ = +0.40       ││
│  │ INT5 (Autonomy) ←→ INT6 (Recognition)│ γ = +0.25       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  KONFLIKTE (γ < 0):                                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ INT3 (Skill Pay) ←→ INT8 (Restructure) │ γ = -0.45     ││
│  │ INT5 (Autonomy)  ←→ INT8 (Restructure) │ γ = -0.30     ││
│  └─────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

### 4. WHEN (V): Kontextdimensionen

```
┌──────────────────────────────────────────────────────────────┐
│  WHEN: Ψ Context Mapping                                    │
├──────────────────────────────────────────────────────────────┤
│  Ψ₁ Economic     │ L1-L5 (Labor Market)                     │
│  Ψ₂ Social       │ K1-K5 (Culture)                          │
│  Ψ₃ Temporal     │ T1-T5 (Temporal)                         │
│  Ψ₄ Spatial      │ S1, L3 (Structure + Urbanization)        │
│  Ψ₅ Institutional│ O3, O5 (Certifications, Union)           │
│  Ψ₆ Cultural     │ K3, K4, M4 (Change History, Leadership)  │
│  Ψ₇ Technological│ S5, O4, R2 (Tech Level, Automation, IT)  │
│  Ψ₈ Environmental│ Physical conditions                      │
├──────────────────────────────────────────────────────────────┤
│  Alle 47 ALPLA-Variablen → 8 Ψ-Dimensionen                  │
└──────────────────────────────────────────────────────────────┘
```

### 5. WHERE (BBB): Parameter-Quellen

```
┌──────────────────────────────────────────────────────────────┐
│  WHERE: Θ Parameter Sources                                 │
├──────────────────────────────────────────────────────────────┤
│  Source          │ Variables        │ Confidence            │
│  ────────────────┼──────────────────┼──────────────────────│
│  L1 (Existing)   │ S1-S6, L1-L5     │ High (LLMMC/Public)  │
│  L2 (Request)    │ O1-O5, P1-P4     │ High (after receipt) │
│  L3 (Collect)    │ K1-K5, M4-M5     │ Medium (Survey)      │
│  L4 (Derive)     │ I1-I5            │ Medium (Calculated)  │
├──────────────────────────────────────────────────────────────┤
│  Total: 47 Variables → E(θ) with 95% CI                     │
└──────────────────────────────────────────────────────────────┘
```

### 6. AWARE (AU): Awareness Levels

```
┌──────────────────────────────────────────────────────────────┐
│  AWARE: A(·) in ALPLA Context                               │
├──────────────────────────────────────────────────────────────┤
│  A_employee      │ Self-awareness (K5, K4)                  │
│  A_management    │ Problem awareness (M5, M1)               │
│  A_organization  │ System awareness (R1, R2)                │
├──────────────────────────────────────────────────────────────┤
│  U^eff = A(t*) × U^pot                                      │
│                                                              │
│  Recognition Intervention:                                   │
│  - Pre:  A ≈ 0.3 → U^eff = 0.3 × U^pot                     │
│  - Post: A ≈ 0.8 → U^eff = 0.8 × U^pot (160% Steigerung)   │
└──────────────────────────────────────────────────────────────┘
```

### 7. READY (AV): Implementation Readiness

```
┌──────────────────────────────────────────────────────────────┐
│  READY: WAX ≥ θ for Intervention                            │
├──────────────────────────────────────────────────────────────┤
│  WAX Components:                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ M5_buyin ≥ 4.0      │ High willingness                  ││
│  │ K4_readiness ≥ 3.5  │ Change acceptance                 ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  θ Threshold:                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ R3_budget ≥ 3       │ Lower threshold                   ││
│  │ T3 = none           │ No confounders → lower threshold  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  Action ⟺ WAX(U^eff, φ, Ψ) ≥ θ(Ψ)                          │
└──────────────────────────────────────────────────────────────┘
```

### 8. STAGE (AW): Behavioral Change Journey

```
┌──────────────────────────────────────────────────────────────┐
│  STAGE: BCJ Phases für Churn Intervention                   │
├──────────────────────────────────────────────────────────────┤
│  S(t)          │ Phase            │ ALPLA Indicators        │
│  ─────────────────────────────────────────────────────────│
│  [0.0, 0.2)    │ Awareness        │ Problem erkannt         │
│  [0.2, 0.4)    │ Trigger          │ Buy-In, Budget          │
│  [0.4, 0.6)    │ Action           │ INT Roll-out            │
│  [0.6, 0.8)    │ Maintenance      │ Churn sinkt             │
│  [0.8, 1.0]    │ Stabilization    │ Nachhaltiger Erfolg     │
├──────────────────────────────────────────────────────────────┤
│  dS/dt = (1/τ) × [S* - S(t)]                                │
│                                                              │
│  Time Constants (τ):                                         │
│  - Recognition: τ ≈ 4 weeks                                 │
│  - Rotation:    τ ≈ 8 weeks                                 │
│  - Career:      τ ≈ 16 weeks                                │
│  - Skill Pay:   τ ≈ 24 weeks                                │
│  - Culture:     τ ≈ 52 weeks                                │
└──────────────────────────────────────────────────────────────┘
```

### 9. HIERARCHY (HI): Decision Levels

```
┌──────────────────────────────────────────────────────────────┐
│  HIERARCHY: Decision Stratification                         │
├──────────────────────────────────────────────────────────────┤
│  L0 (Operative)  │ Supervisor: Schichteinteilung, Tasks    │
│  L1 (Strategic)  │ PM + HR: Experiment, Budget, INT-Mix    │
│  L2 (Derived)    │ PM + Sup: Timing, Pilots, Adjustments   │
│  L3 (Emergent)   │ System: Kulturwandel, Vertrauensbildung │
├──────────────────────────────────────────────────────────────┤
│  N_L2 Formula für ALPLA:                                    │
│  N_L2 = α·γ_avg × n × (1-m) / log(n)                       │
│       = 0.8 × 0.25 × 3 × (1-0.4) / log(3)                  │
│       ≈ 5 koordinierte Entscheidungen pro Werk              │
└──────────────────────────────────────────────────────────────┘
```

---

## EBF Output-Gleichungen für ALPLA

### Stage 1: Potential Utility
```
U^pot_i = Σ_L α^L(Ψ) · [Σ_d ω_d · U_d + Σ γ_dd' · U_d·U_d']
```

### Stage 2: Effective Utility
```
U^eff_i(t*) = A_i(t*) × U^pot_i
```

### Stage 3: Stay/Leave Decision
```
Stay  ⟺ WAX(U^eff, φ, Ψ) ≥ θ(Ψ)
Leave ⟺ WAX(U^eff, φ, Ψ) < θ(Ψ)
```

### Stage 4: Churn Dynamics
```
dChurn/dt = (1/τ) × [Churn*(INT, Ψ) - Churn(t)]
```

---

## HHH 20-Field Integration

Jede der 8 ALPLA-Interventionen wurde auf das HHH 20-Field Schema gemappt:

| INT | Name | F2 Type | F5 FEPSDE | F6 Phase | F12 Scope |
|-----|------|---------|-----------|----------|-----------|
| INT1 | Job Rotation | Contextual | D + P | Action | Tactical |
| INT2 | Career Pathway | Identity | D + F | Action | Strategic |
| INT3 | Skill-Based Pay | Financial | F + D | Action | Strategic |
| INT4 | Workload Mgmt | Contextual | P + E | Action | Tactical |
| INT5 | Autonomy | Identity | E + D | Action | Tactical |
| INT6 | Recognition | Feedback | E + S | All | Operative |
| INT7 | Onboarding | Identity | E + S + D | Trigger | Tactical |
| INT8 | Team Restructure | Social | S + E | Action | Tactical |

---

## Field Experiment Design

### Treatment vs. Control
```
┌─────────────────────────────────────────────────────────────┐
│  MATCHED PAIRS DESIGN                                       │
├─────────────────────────────────────────────────────────────┤
│  Treatment (n=6):  Full Bundle (Primary + Secondary + INT6) │
│  Control (n=6):    Baseline only (INT6 Recognition)         │
├─────────────────────────────────────────────────────────────┤
│  Matching: IFI Cluster, Size (±20%), Churn (±5pp)          │
│  Duration: 12 months                                        │
│  Primary Outcome: Δ Churn Rate (DiD)                        │
└─────────────────────────────────────────────────────────────┘
```

### Expected Results
```
┌─────────────────────────────────────────────────────────────┐
│  EXPECTED CHURN REDUCTION BY CLUSTER                        │
├─────────────────────────────────────────────────────────────┤
│  Cluster A (Rotation):   6-10% reduction                    │
│  Cluster B (Career):     5-8% reduction                     │
│  Cluster C (Technical):  5-9% reduction                     │
│  Cluster D (Autonomy):   5-8% reduction                     │
│  Cluster E (Constrained):2-4% reduction                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Dateien und Referenzen

| Datei | Inhalt |
|-------|--------|
| `data/alpla-ebf-integration.yaml` | Vollständige Integration (diese Dokumentation) |
| `data/alpla-measurement-framework.yaml` | 47 Variablen, 9 Dimensionen |
| `data/alpla-intervention-selection.yaml` | AISA Algorithmus |
| `data/alpla-intervention-fit-index.yaml` | IFI Scores für 17 Werke |
| `data/alpla-job-profiles.yaml` | BC1-BC5 Profile |
| `data/alpla-plant-activities.yaml` | 251 Aktivitäten |
| `scripts/calculate_plant_deltas.py` | Delta-Berechnung |

---

## Next Steps

1. **Appendix UNMAPPED_COR (DOMAIN-ALPLA)** formal als LaTeX erstellen
2. **Model in FFF Registry** registrieren
3. **LLMMC-Parameter** mit ALPLA Ist-Daten validieren
4. **Feldexperiment** durchführen (12 Monate)
5. **BBB-Update** mit empirischen Parametern

---

*Erstellt: 2026-01-19 | EBF Version: 10C | Appendix Code: BI (DOMAIN-ALPLA)*
