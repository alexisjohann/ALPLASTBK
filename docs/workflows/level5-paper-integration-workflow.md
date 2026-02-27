# Level 5 Paper Integration Workflow (L5-PIW)

> **SSOT:** Dieser Workflow definiert die systematische Integration eines wissenschaftlichen Papers auf Level 5 (FULL) ins EBF Framework.
>
> **Entwickelt:** 2026-02-04 basierend auf Bénabou/Falk/Tirole (2018) Integration
>
> **Skill:** `/upgrade-paper --level 5` oder `/integrate-paper` mit automatischer Level-5-Klassifikation

---

## Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEVEL 5: FULL INTEGRATION WORKFLOW                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: KLASSIFIKATION                                                │
│     └── /integrate-paper → Level-Bestimmung (1-5)                       │
│                                                                         │
│  PHASE 2: ARCHITEKTUR-ENTSCHEIDUNG                                      │
│     └── 6-Faktoren-Framework für CORE-Erweiterungen                     │
│                                                                         │
│  PHASE 3: KOMPONENTEN-INTEGRATION                                       │
│     └── 11-Komponenten-Checkliste                                       │
│                                                                         │
│  PHASE 4: KAPITEL-RELEVANZ                                              │
│     └── HIGH / MEDIUM / LOW Analyse                                     │
│                                                                         │
│  PHASE 5: VALIDIERUNG                                                   │
│     └── Compliance-Check + Commit                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Klassifikation

Verwende `/integrate-paper` für automatische Level-Bestimmung.

### Level 5 Kriterien (Score ≥ 20)

| Kriterium | Gewicht | Indikator |
|-----------|---------|-----------|
| `new_theory_category` | 5 | "new framework", "unified theory" |
| `extends_existing_theory` | 3 | "extends", "builds on" |
| `new_domain` | 4 | "first study", "emerging" |
| `empirical_parameters` | 2 | "we estimate", "β =", "λ =" |
| `policy_implications` | 2 | "policy", "regulation", "nudge" |
| `field_experiment` | 2 | "RCT", "natural experiment" |
| `case_study_worthy` | 1 | "real-world", "practical" |

**Level 5 Bedingung:**
```
Score ≥ 20 + (new_theory_category ≥ 10 ODER new_domain ≥ 8)
```

---

## Phase 2: Architektur-Entscheidung (6-Faktoren-Framework)

### Das Architektur-Prinzip

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ARCHITEKTUR-PRINZIP (PFLICHT!)                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LIT-Appendix (Primary)                                                 │
│     = VOLLSTÄNDIGE Formalisierung                                       │
│     = Alle Axiome, Definitionen, Beweise                                │
│     = Beispiel: UNMAPPED_RB-7 für Bénabou narratives                            │
│           ↓                                                             │
│  CORE-Appendices                                                        │
│     = NUR STRUKTURELLE Erweiterungen                                    │
│     = Nur wenn 6-Faktoren-Check POSITIV                                 │
│     = Cross-Reference zu LIT für Details                                │
│           ↓                                                             │
│  Chapters                                                               │
│     = NUR Cross-References                                              │
│     = Keine eigenständige Formalisierung                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6-Faktoren-Entscheidungsframework

Für **JEDEN** CORE-Appendix diese 6 Faktoren prüfen:

| Faktor | Frage | JA bedeutet |
|--------|-------|-------------|
| **F1: Structural Novelty** | Führt Paper NEUE Struktur ein (nicht nur Parameter)? | Potenzielle Erweiterung |
| **F2: Axiom Contribution** | Erfordert das Paper ein NEUES Axiom im CORE? | Axiom hinzufügen |
| **F3: Dimensionality Change** | Ändert das Paper die Dimensionalität des CORE? | Struktur erweitern |
| **F4: Parameter vs Structure** | Ist es STRUKTUR (nicht nur neue Parameterwerte)? | CORE ändern |
| **F5: Universality** | Gilt die Erweiterung für ALLE Anwendungen des CORE? | In CORE aufnehmen |
| **F6: New Mechanism** | Beschreibt Paper einen NEUEN Mechanismus? | Mechanismus formalisieren |

### Entscheidungsbaum

```
                    ┌─────────────────┐
                    │ Paper-Beitrag   │
                    │ zu CORE-X?      │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
        ┌─────▼─────┐                 ┌─────▼─────┐
        │ F1: Neue  │                 │ Nur neue  │
        │ Struktur? │                 │ Parameter │
        └─────┬─────┘                 └─────┬─────┘
              │                             │
         JA   │                        NEIN │
              │                             │
        ┌─────▼─────┐                 ┌─────▼─────┐
        │ F4: Nicht │                 │ → WHERE   │
        │ nur Param │                 │   (BBB)   │
        └─────┬─────┘                 └───────────┘
              │
         JA   │
              │
        ┌─────▼─────┐
        │ F5: Gilt  │
        │ universal │
        └─────┬─────┘
              │
         JA   │
              │
        ┌─────▼─────┐
        │ → CORE    │
        │ erweitern │
        └───────────┘
```

### Beispiel: Bénabou/Falk/Tirole (2018)

| CORE | F1 | F2 | F3 | F4 | F5 | F6 | Entscheidung |
|------|----|----|----|----|----|----|--------------|
| **WHAT (C)** | ❌ | ❌ | ❌ | ❌ | - | - | KEINE Erweiterung (μv̂ existiert bereits) |
| **HOW (B)** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | **UNMAPPED_CMP-11** (γ sign reversal) |
| **WHEN (V)** | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | **ρ Parameter** (network structure) |
| **AWARE (AU)** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | **AWX-A5** (moral awareness) |
| **EIT (IE)** | ❌ | ❌ | ❌ | ❌ | - | - | KEINE (narratives = I_AWARE + I_WHAT) |

---

## Phase 3: Komponenten-Integration (11-Komponenten-Checkliste)

### Checkliste

```
☐ 1.  BibTeX Entry (bcm_master.bib)
      ├── use_for (5+ Appendices)
      ├── theory_support (MS-XX-XXX)
      ├── parameter (Symbol = Name)
      ├── evidence_tier (1-3)
      └── identification, external_validity, notes

☐ 2.  Theory Catalog (data/theory-catalog.yaml)
      └── MS-XX-XXX mit ebf_restrictions

☐ 3.  Case Registry (data/case-registry.yaml)
      └── CAS-XXX mit 10C Mapping

☐ 4.  Parameter Registry (data/parameter-registry.yaml)
      └── PAR-XXX-XXX mit values.literature

☐ 5.  LIT Appendix (appendices/*LIT*.tex)
      └── Vollständige Formalisierung, Axiom LIT-X-N

☐ 6.  CORE Appendix Extensions (nur wenn 6-Faktoren positiv!)
      ├── Axiom hinzufügen (z.B. UNMAPPED_CMP-11)
      ├── Symbol-Tabelle erweitern
      └── Cross-Reference zu LIT

☐ 7.  BCM2 Context Factors (data/dr-datareq/sources/context/)
      └── Neue Ψ-Faktoren mit ebf_reference

☐ 8.  Chapter-Appendix Mapping (docs/frameworks/chapter-appendix-mapping.yaml)
      └── LIT-Appendix verlinkt zu Chapters

☐ 9.  Chapter Cross-References
      ├── HIGH: Cross-Ref Box + Appendix Reference
      ├── MEDIUM: Appendix Reference nur
      └── LOW: Keine Aktion

☐ 10. Paper YAML (data/paper-references/PAP-*.yaml)
      ├── structural_characteristics (S1-S6)
      ├── ebf_integration
      ├── ten_c_mapping
      ├── chapter_relevance
      ├── key_equations
      └── parameter_contributions mit measurement_contexts  ← NEU!

☐ 11. Paper Full-Text Archive (data/paper-texts/PAP-*.md)
      └── Volltext als Markdown
```

### ATOMIC SYMBOL RULE & Measurement Contexts

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ATOMIC SYMBOL RULE: Parameter-Symbole sind EINEINDEUTIG               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PROBLEM: Verschiedene Papers verwenden dasselbe Symbol für             │
│           verschiedene Konzepte (z.B. α, β, λ in mehreren Papern)      │
│                                                                         │
│  LÖSUNG: EBF verwendet eindeutige Symbole mit Subscripts               │
│                                                                         │
│  BEISPIELE:                                                             │
│  ┌──────────────┬────────────┬───────────────────────────────────────┐ │
│  │ Paper-Symbol │ EBF-Symbol │ Bedeutung                             │ │
│  ├──────────────┼────────────┼───────────────────────────────────────┤ │
│  │ λ            │ λ          │ Loss Aversion (Kahneman/Tversky)      │ │
│  │ λ            │ λ_R        │ Rejection Sensitivity (Bénabou 2022)  │ │
│  │ α            │ α_FS       │ Envy (Fehr-Schmidt 1999)              │ │
│  │ α            │ α_R        │ Rejection Scaling (Bénabou 2022)      │ │
│  │ β            │ β          │ Present Bias (O'Donoghue-Rabin)       │ │
│  │ β            │ β_FS       │ Guilt (Fehr-Schmidt 1999)             │ │
│  └──────────────┴────────────┴───────────────────────────────────────┘ │
│                                                                         │
│  REGEL: Jedes EBF-Symbol ist weltweit einzigartig (keine Kollisionen)  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Measurement Contexts Architecture (SSOT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MEASUREMENT CONTEXTS: Paper-YAML = Single Source of Truth             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ARCHITEKTUR:                                                           │
│                                                                         │
│  Paper-YAML (SSOT)                   Parameter-Registry (Aggregation)   │
│  ──────────────────                  ────────────────────────────────   │
│  PAP-benabou_2022_hurts_ask          PAR-BEH-016 (λ_R)                  │
│  └─ parameter_contributions:         └─ by_domain:                      │
│      └─ λ_R:                             └─ welfare: mean: 2.50         │
│          └─ measurement_contexts:             ← aggregiert aus Papers   │
│              ├─ welfare_takeup                                          │
│              │   ├─ value_estimate                                      │
│              │   ├─ psi_conditions                                      │
│              │   ├─ source_in_paper                                     │
│              │   ├─ study_type                                          │
│              │   └─ countries                                           │
│              ├─ workplace_help                                          │
│              └─ healthcare_seeking                                      │
│                                                                         │
│  VORTEILE:                                                              │
│  ✅ Paper-YAML = Primary Source (Traceability zu Originalquelle)        │
│  ✅ Parameter-Registry = Aggregation (Cross-Paper Vergleich)            │
│  ✅ Jeder Ψ-Kontext dokumentiert wo er herkommt                         │
│  ✅ Bayesian Updating: Paper → Prior → Posterior                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### measurement_contexts Schema

```yaml
parameter_contributions:
  - symbol: "λ_R"                         # EBF-eindeutiges Symbol
    paper_notation: "λ"                   # Symbol im Paper
    ebf_id: "PAR-BEH-016"                 # Parameter-Registry ID
    name: "rejection_sensitivity"
    description: "Loss aversion in self-image from rejection"
    typical_range: "[1.5, 3.0]"
    domain: "help_seeking"
    translation_note: "Paper uses λ, EBF uses λ_R to distinguish"

    measurement_contexts:                 # ← PFLICHT für Level 5
      - context: "welfare_takeup"
        value_estimate: "high (λ_R ≈ 2.5)"
        psi_conditions:                   # ← Ψ-Dimension Kontext
          Ψ_I: "bureaucratic_application"
          Ψ_S: "welfare_stigma"
          Ψ_K: "self_reliance_norm"
        source_in_paper: "Section 6.2"    # ← Traceable
        study_type: "field_data"          # theoretical/lab/field
        countries: ["USA"]

      - context: "workplace_help"
        value_estimate: "moderate (λ_R ≈ 1.8)"
        psi_conditions:
          Ψ_I: "professional_hierarchy"
          Ψ_S: "competence_signaling"
          Ψ_C: "performance_evaluation"
        source_in_paper: "Section 6.1"
        study_type: "lab_experiment"
```

### Ψ-Dimension Referenz

| Dimension | Symbol | Typische Werte in measurement_contexts |
|-----------|--------|----------------------------------------|
| Institutional | Ψ_I | "bureaucratic", "professional_hierarchy", "regulation" |
| Social | Ψ_S | "welfare_stigma", "peer_observation", "anonymity" |
| Cognitive | Ψ_C | "performance_evaluation", "information_avoidance" |
| Cultural | Ψ_K | "self_reliance_norm", "reciprocity_expectation" |
| Physical | Ψ_F | "digital_remote", "face_to_face", "public_space" |

---

## Parameter Context Transformation (PCT)

> **⚠️ CORE THEORY: Dies ist der zentrale theoretische Beitrag des EBF!**

### Das Paradigma: Von Fixed zu Contextual Parameters

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EBF CORE THEORY: CONTEXTUAL PARAMETER TRANSFORMATION                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TRADITIONELLE VERHALTENSÖKONOMIE (Kahneman, Thaler, etc.):            │
│  ──────────────────────────────────────────────────────────            │
│  Parameter = Konstante                                                  │
│  λ = 2.25 (Loss Aversion "ist" 2.25)                                   │
│  β = 0.70 (Present Bias "ist" 0.70)                                    │
│                                                                         │
│  PROBLEM: Warum variieren Replikationen so stark?                       │
│           λ ∈ [1.5, 5.0] je nach Studie!                               │
│                                                                         │
│  ════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  EBF (Evidence-Based Framework):                                        │
│  ─────────────────────────────                                         │
│  Parameter = Funktion von Kontext (Ψ) und Utility-Dimensionen (10C)    │
│                                                                         │
│       θ = f(Ψ, 10C)                                                    │
│                                                                         │
│  Loss Aversion λ(Ψ, 10C):                                               │
│    λ(welfare, high_stigma)     = 2.50                                  │
│    λ(workplace, low_stigma)    = 1.80                                  │
│    λ(healthcare, mixed)        = 2.20                                  │
│                                                                         │
│  DIE VARIATION IST NICHT NOISE - SIE IST DAS SIGNAL!                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Warum ist das eine "neue" Theorie?

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WAS EBF ANDERS MACHT                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. KONTEXT IST NICHT CONFOUND - KONTEXT IST EXPLANANS                 │
│     ─────────────────────────────────────────────────                  │
│     Traditionell: "Wir kontrollieren für Kontext"                      │
│     EBF:          "Wir modellieren durch Kontext"                      │
│                                                                         │
│  2. 10C UTILITY DIMENSIONS MODERIEREN PARAMETER                         │
│     ──────────────────────────────────────────────                     │
│     WHO:   Wessen Utility? → Parameter für Self vs. Other              │
│     WHAT:  Welche Dimension? → Parameter pro FEPSDE                    │
│     HOW:   Komplementarität? → Parameter-Interaktionen (γ)             │
│     WHEN:  Welcher Kontext? → Ψ-abhängige Parameter                    │
│     WHERE: Woher die Zahlen? → Measurement Context                     │
│     ...                                                                 │
│                                                                         │
│  3. TRANSFORMATION STATT INTERPOLATION                                  │
│     ───────────────────────────────────                                │
│     Traditionell: "Mittelwert aus allen Studien"                       │
│     EBF:          "Systematische Transformation zwischen Kontexten"    │
│                                                                         │
│  4. FALSIFIZIERBAR                                                      │
│     ─────────────                                                       │
│     Wenn θ_B = θ_A × ∏ᵢ M(ΔΨᵢ) falsche Vorhersagen macht,             │
│     ist die Theorie falsifiziert (nicht nur ein Parameter falsch).     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Die zentrale Gleichung

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  EBF PARAMETER TRANSFORMATION EQUATION                                  │
│                                                                         │
│                 θ(Ψ_B, 10C_B) = θ(Ψ_A, 10C_A) × T(ΔΨ, Δ10C)            │
│                                                                         │
│  WO:                                                                    │
│    θ       = Verhaltensparameter (λ, β, α, μ, γ, ...)                  │
│    Ψ       = Kontext-Vektor (Ψ_I, Ψ_S, Ψ_C, Ψ_K, Ψ_F, Ψ_T, Ψ_M, Ψ_E)  │
│    10C     = Utility-Dimension-Vektor (WHO, WHAT, HOW, WHEN, ...)      │
│    T(·)   = Transformationsfunktion                                    │
│                                                                         │
│  VEREINFACHT (multiplikativ):                                           │
│                                                                         │
│                 θ_B = θ_A × ∏ᵢ M(ΔΨᵢ) × ∏ⱼ N(Δ10Cⱼ)                   │
│                                                                         │
│  M(ΔΨᵢ)  = Ψ-Multiplikator (aus PCT-Tabelle)                          │
│  N(Δ10Cⱼ) = 10C-Multiplikator (aus Sensitivitäts-Matrix)              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Das Kernprinzip

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PARAMETER CONTEXT TRANSFORMATION (PCT)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PROBLEM:  Parameter θ wurde in Kontext A gemessen.                     │
│            Wie lautet θ in Kontext B?                                   │
│                                                                         │
│  LÖSUNG:   Aus den Ψ-Differenzen ableiten!                              │
│                                                                         │
│  FORMEL:                                                                │
│                                                                         │
│    θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)                                               │
│                                                                         │
│  WO:                                                                    │
│    θ_A     = Parameter-Wert in Kontext A (aus measurement_context)      │
│    ΔΨᵢ    = Ψ_i(B) - Ψ_i(A)  (Kontext-Differenz pro Dimension)        │
│    M(ΔΨᵢ) = Multiplikator für diese Dimension                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Transformation über 10C-Dimensionen

```
┌─────────────────────────────────────────────────────────────────────────┐
│  10C-ABHÄNGIGE PARAMETER-TRANSFORMATION                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Jeder Parameter hat eine 10C-Sensitivitäts-Matrix:                     │
│                                                                         │
│  Parameter λ_R (Rejection Sensitivity):                                 │
│  ┌─────────┬────────────────────────────────────────────────────────┐  │
│  │ 10C     │ Einfluss auf λ_R                                       │  │
│  ├─────────┼────────────────────────────────────────────────────────┤  │
│  │ WHO     │ ↑ wenn Selbstbild wichtiger (higher σ_self)            │  │
│  │ WHAT    │ ↑ wenn Identität stärker betroffen                     │  │
│  │ HOW     │ → Komplementarität mit Offering-Normen                 │  │
│  │ WHEN    │ ↑ bei Zeitdruck (weniger Reflexion)                    │  │
│  │ WHERE   │ ↑ bei public rejection (vs. private)                   │  │
│  │ AWARE   │ ↓ wenn Rejection-Risiko nicht salient                  │  │
│  │ READY   │ ↑ bei hoher Willingness (mehr zu verlieren)            │  │
│  │ STAGE   │ ↑ in frühen BCJ-Phasen (mehr Unsicherheit)             │  │
│  └─────────┴────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Beispiel: λ_R Transformation (Welfare → Workplace)

**Gegeben aus Paper-YAML:**
```yaml
measurement_contexts:
  - context: "welfare_takeup"
    value_estimate: "high (λ_R ≈ 2.5)"
    psi_conditions:
      Ψ_I: "bureaucratic_application"
      Ψ_S: "welfare_stigma"          # HIGH stigma
      Ψ_K: "self_reliance_norm"

  - context: "workplace_help"
    value_estimate: "moderate (λ_R ≈ 1.8)"
    psi_conditions:
      Ψ_I: "professional_hierarchy"
      Ψ_S: "competence_signaling"    # LOWER stigma
      Ψ_C: "performance_evaluation"
```

**Transformation berechnen:**

```
SCHRITT 1: Identifiziere Ψ-Differenzen
─────────────────────────────────────
Ψ_S: welfare_stigma → competence_signaling
     HIGH stigma    → MODERATE stigma
     ΔΨ_S = -0.3 (Stigma sinkt)

Ψ_I: bureaucratic → professional_hierarchy
     EXTERNAL     → INTERNAL (same org)
     ΔΨ_I = -0.1 (weniger formal)

Ψ_C: (neu) performance_evaluation
     Neuer Faktor: ΔΨ_C = +0.2

SCHRITT 2: Multiplikatoren anwenden
───────────────────────────────────
M(ΔΨ_S = -0.3) = 0.85  (weniger Stigma → weniger Sensitivity)
M(ΔΨ_I = -0.1) = 0.95  (weniger formal → leicht weniger)
M(ΔΨ_C = +0.2) = 1.10  (Evaluation → mehr Sensitivity)

SCHRITT 3: Transformieren
─────────────────────────
λ_R(workplace) = λ_R(welfare) × M(ΔΨ_S) × M(ΔΨ_I) × M(ΔΨ_C)
               = 2.5 × 0.85 × 0.95 × 1.10
               = 2.22

Gemessen: λ_R ≈ 1.8
Geschätzt: λ_R ≈ 2.22

→ Abweichung 23% - weitere Faktoren untersuchen
```

### PCT-Multiplikator-Tabelle (Referenz)

| Ψ-Dimension | Richtung | Typischer Multiplikator | Beispiel |
|-------------|----------|-------------------------|----------|
| **Ψ_S** (Social) | Stigma ↓ | 0.80 - 0.90 | welfare → workplace |
| **Ψ_S** (Social) | Stigma ↑ | 1.10 - 1.25 | private → public |
| **Ψ_I** (Institutional) | Formal ↓ | 0.90 - 0.98 | bureaucratic → informal |
| **Ψ_I** (Institutional) | Formal ↑ | 1.02 - 1.15 | informal → regulated |
| **Ψ_C** (Cognitive) | Load ↑ | 1.05 - 1.20 | relaxed → stressed |
| **Ψ_C** (Cognitive) | Load ↓ | 0.85 - 0.95 | stressed → relaxed |
| **Ψ_K** (Cultural) | Norm shift | 0.70 - 1.40 | culture-dependent |
| **Ψ_F** (Physical) | Digital → F2F | 1.10 - 1.30 | more personal |

### PCT in der Praxis: 3-Schritt-Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PCT WORKFLOW                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: ANCHOR CONTEXT (aus Paper-YAML)                             │
│  ───────────────────────────────────────────                            │
│  θ_A = 2.5 (λ_R in welfare context)                                     │
│  Ψ_A = {Ψ_I: bureaucratic, Ψ_S: welfare_stigma, Ψ_K: self_reliance}    │
│                                                                         │
│  SCHRITT 2: TARGET CONTEXT (neues Projekt)                              │
│  ─────────────────────────────────────────                              │
│  Ψ_B = {Ψ_I: healthcare_system, Ψ_S: illness_stigma, Ψ_K: privacy}     │
│                                                                         │
│  SCHRITT 3: TRANSFORM                                                   │
│  ────────────────────                                                   │
│  ΔΨ = Ψ_B - Ψ_A                                                         │
│  θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)                                                 │
│                                                                         │
│  OUTPUT: θ_B = 2.2 (λ_R in healthcare context)                          │
│          + Unsicherheits-Intervall [1.9, 2.5]                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Integration mit EBF-Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EBF MODEL-BUILDING + PCT                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Schritt 3 (Parameter) im EBF-Workflow:                                 │
│                                                                         │
│  1. LLMMC Prior generieren                                              │
│       ↓                                                                 │
│  2. Paper-YAML measurement_contexts laden                               │
│       ↓                                                                 │
│  3. Nächsten passenden Anchor Context finden                            │
│       ↓                                                                 │
│  4. PCT: Anchor → Target transformieren                                 │
│       ↓                                                                 │
│  5. Bayesian Update: Prior × Likelihood → Posterior                     │
│       ↓                                                                 │
│  6. Sensitivitätsanalyse auf Ψ-Differenzen                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## EBF Research Agenda: Parameter Context Functions

> **NEXT LEVEL:** Für jeden Parameter eine Kontextfunktion schätzen

### Das Forschungsprogramm

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PARAMETER CONTEXT FUNCTIONS: θ = Fθ(Ψ, 10C)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ZIEL: Für jeden verhaltensökonomischen Parameter θ eine Funktion Fθ   │
│        schätzen, die erklärt WIE θ von Kontext und 10C abhängt.        │
│                                                                         │
│  BEISPIELE:                                                             │
│  ───────────                                                            │
│  λ  = Fλ(Ψ_S, Ψ_I, Ψ_C, ...)     Loss Aversion                        │
│  β  = Fβ(Ψ_T, Ψ_C, WHO, ...)      Present Bias                         │
│  α  = Fα(Ψ_S, Ψ_K, WHAT, ...)     Inequity Aversion (Envy)             │
│  μ  = Fμ(Ψ_S, Ψ_I, AWARE, ...)    Image Concern                        │
│  γ  = Fγ(Ψ_K, HOW, READY, ...)    Complementarity                      │
│  λ_R = Fλ_R(Ψ_S, Ψ_I, WHO, ...)   Rejection Sensitivity                │
│                                                                         │
│  DIE FUNKTION IST DIE THEORIE!                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Datengrundlage: measurement_contexts

```
┌─────────────────────────────────────────────────────────────────────────┐
│  VON PAPERS ZU FUNKTIONEN                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: Alle measurement_contexts aus Paper-YAMLs sammeln          │
│  ─────────────────────────────────────────────────────────────          │
│  data/paper-references/PAP-*.yaml                                       │
│  → parameter_contributions[].measurement_contexts[]                     │
│                                                                         │
│  SCHRITT 2: (θ, Ψ, 10C) Triplets extrahieren                           │
│  ─────────────────────────────────────────────                          │
│  ┌────────────────────────────────────────────────────────────────────┐│
│  │ θ        │ Ψ_I              │ Ψ_S          │ Ψ_K      │ WHO  │ ... ││
│  ├──────────┼──────────────────┼──────────────┼──────────┼──────┼─────┤│
│  │ λ = 2.5  │ bureaucratic     │ welfare_stig │ self_rel │ self │     ││
│  │ λ = 1.8  │ professional     │ competence   │ team     │ self │     ││
│  │ λ = 2.2  │ medical_gate     │ illness_stig │ privacy  │ self │     ││
│  │ λ = 2.9  │ immigration      │ identity_thr │ national │ grp  │     ││
│  │ ...      │ ...              │ ...          │ ...      │ ...  │     ││
│  └────────────────────────────────────────────────────────────────────┘│
│                                                                         │
│  SCHRITT 3: Funktion Fθ(·) schätzen                                    │
│  ───────────────────────────────────                                    │
│  Methoden:                                                              │
│  ├── Linear Regression: θ = β₀ + β₁Ψ_S + β₂Ψ_I + ...                  │
│  ├── Hierarchical Bayes: Partial Pooling über Studien                  │
│  ├── Random Forest: Nicht-lineare Interaktionen                        │
│  └── Neural Network: Komplexe Patterns                                 │
│                                                                         │
│  SCHRITT 4: Validieren (Out-of-Sample)                                 │
│  ─────────────────────────────────────                                  │
│  Train auf 80% der measurement_contexts                                │
│  Test auf 20% → Prediction Error                                       │
│                                                                         │
│  SCHRITT 5: Fθ veröffentlichen als Theorie                             │
│  ─────────────────────────────────────────                              │
│  "Loss Aversion als Funktion von Kontext: Eine empirische Schätzung"   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Beispiel: Loss Aversion Function Fλ

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LOSS AVERSION CONTEXT FUNCTION                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Geschätzte Funktion (hypothetisch):                                    │
│                                                                         │
│  λ(Ψ, 10C) = λ_base × (1 + β_S · Stigma(Ψ_S))                          │
│                     × (1 + β_I · Formality(Ψ_I))                       │
│                     × (1 + β_C · CogLoad(Ψ_C))                         │
│                     × (1 + β_K · IndivNorm(Ψ_K))                       │
│                     × (1 + β_WHO · Self(WHO))                          │
│                     × (1 + β_AWARE · Salience(AWARE))                  │
│                                                                         │
│  Mit geschätzten Koeffizienten (aus N = 847 measurement_contexts):     │
│                                                                         │
│  ┌────────────┬─────────┬──────────┬───────────────────────────────────┐│
│  │ Koeffizient│ Schätzung│ SE      │ Interpretation                    ││
│  ├────────────┼─────────┼──────────┼───────────────────────────────────┤│
│  │ λ_base     │ 2.00    │ 0.15    │ Baseline Loss Aversion            ││
│  │ β_S        │ 0.25    │ 0.04    │ +25% pro Stigma-Stufe             ││
│  │ β_I        │ 0.10    │ 0.03    │ +10% pro Formalitäts-Stufe        ││
│  │ β_C        │ 0.15    │ 0.05    │ +15% unter Cognitive Load         ││
│  │ β_K        │ 0.20    │ 0.06    │ +20% bei Individualismus-Norm     ││
│  │ β_WHO      │ 0.05    │ 0.02    │ +5% wenn Self (vs. Other)         ││
│  │ β_AWARE    │ 0.12    │ 0.04    │ +12% bei hoher Salienz            ││
│  └────────────┴─────────┴──────────┴───────────────────────────────────┘│
│                                                                         │
│  R² = 0.68 (68% der Variation erklärt!)                                │
│                                                                         │
│  INTERPRETATION:                                                        │
│  ───────────────                                                        │
│  λ(welfare, self, salient) = 2.0 × 1.25 × 1.10 × 1.15 × 1.05 × 1.12   │
│                            = 2.0 × 1.87                                │
│                            = 3.74                                      │
│                                                                         │
│  λ(workplace, self, routine) = 2.0 × 1.00 × 1.05 × 1.00 × 1.05 × 1.00 │
│                              = 2.0 × 1.10                              │
│                              = 2.20                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Forschungsfragen pro Parameter

| Parameter | Symbol | Hauptfrage | Vermutete Treiber |
|-----------|--------|------------|-------------------|
| **Loss Aversion** | λ | Wann ist Verlust besonders schmerzhaft? | Ψ_S (Stigma), Ψ_C (Load), AWARE |
| **Present Bias** | β | Wann ist Ungeduld am grössten? | Ψ_T (Zeitdruck), Ψ_C, READY |
| **Inequity Aversion** | α_FS | Wann ist Neid am stärksten? | Ψ_S (Observability), Ψ_K (Equality) |
| **Image Concern** | μ | Wann kümmert Image am meisten? | Ψ_S (Audience), Ψ_I (Stakes) |
| **Rejection Sensitivity** | λ_R | Wann schmerzt Ablehnung am meisten? | Ψ_S (Relationship), Ψ_I (Formal) |
| **Complementarity** | γ | Wann verstärken sich Dimensionen? | HOW (Structure), Ψ_K (Culture) |
| **Discount Rate** | δ | Wann wird Zukunft stärker diskontiert? | Ψ_T (Horizon), Ψ_C (Uncertainty) |

### Nächste Schritte

```
☐ Script erstellen: extract_measurement_contexts.py
   → Alle (θ, Ψ, 10C) Triplets aus Paper-YAMLs sammeln

☐ Datenbank erstellen: data/parameter-context-data.yaml
   → Strukturierte Sammlung aller Messungen

☐ Erste Schätzung: Fλ für Loss Aversion
   → 50+ measurement_contexts verfügbar

☐ Validierung: Out-of-Sample Prediction
   → 80/20 Train/Test Split

☐ Paper: "Contextual Parameters in Behavioral Economics"
   → EBF Core Theory Publication
```

### Wissenschaftliche Neuheit: Was existiert NICHT

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WISSENSCHAFTLICHE NEUHEIT: Contextual Parameter Functions              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WAS IN DER LITERATUR EXISTIERT:                                        │
│  ─────────────────────────────────                                      │
│  ✓ Meta-Analysen: Berichten Durchschnittswerte über Studien             │
│  ✓ Heterogenitäts-Analysen: Notieren "große Varianz" zwischen Studien   │
│  ✓ Kulturvergleiche: Hofstede-Dimensionen, GLOBE, Inglehart             │
│  ✓ WEIRD-Kritik: Henrich et al. zeigen Nicht-Generalisierbarkeit        │
│  ✓ Situationismus-Debatte: Mischel, Ross & Nisbett                      │
│                                                                         │
│  WAS NICHT EXISTIERT (= EBF BEITRAG):                                   │
│  ──────────────────────────────────────                                 │
│  ✗ Formale Spezifikation: θ = f(Ψ, 10C)                                │
│  ✗ Systematische Triplet-Sammlung: (θ, Ψ, 10C) aus Papers               │
│  ✗ Schätzbare Kontextfunktionen: Fθ mit Koeffizienten βᵢ               │
│  ✗ Paradigma: "Variation ist Signal, nicht Noise"                       │
│  ✗ Integration von Utility-Dimensionen als Moderatoren                  │
│  ✗ Transformationsgleichung: θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)                    │
│                                                                         │
│  WARUM EXISTIERT DAS NICHT?                                             │
│  ─────────────────────────────                                          │
│  1. Methodologischer Fokus auf "Kontrollieren für Kontext"              │
│     → Kontext als Confound, nicht als Explanans                         │
│                                                                         │
│  2. Replikationskrise als "Problem", nicht als Datenquelle              │
│     → "λ variiert von 1.5 bis 5.0" = Problem zu lösen                  │
│     → EBF: = Information über Kontextabhängigkeit!                      │
│                                                                         │
│  3. Fehlende integrierte Datenstruktur                                  │
│     → Papers berichten Kontext nicht systematisch                       │
│     → Keine Sammlung von (θ, Ψ, 10C) Triplets                          │
│     → EBF: measurement_contexts Schema löst das                         │
│                                                                         │
│  4. Disziplinäre Silos                                                  │
│     → Psychologie: Individual-Level Heterogenität                       │
│     → Kulturökonomie: Makro-Level Unterschiede                          │
│     → EBF: Integriert alle Ebenen (MACRO→MICRO→INDIVIDUAL)              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Iteratives Lernen: Einfach anfangen, systematisch verbessern

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ITERATIVE IMPROVEMENT PARADIGM                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PRINZIP: Starte mit einfacher Schätzung, verbessere mit mehr Daten    │
│                                                                         │
│  ITERATION 0: Prior (LLMMC)                                             │
│  ────────────────────────────                                           │
│  Fλ(Ψ) = λ_base = 2.25                                                 │
│  → Nur Baseline, keine Kontextabhängigkeit                              │
│  → N = 0 measurement_contexts                                           │
│                                                                         │
│  ITERATION 1: Erste Daten (10-20 Papers)                                │
│  ─────────────────────────────────────────                              │
│  Fλ(Ψ) = λ_base × (1 + β_S · Stigma)                                   │
│  → Ein dominanter Treiber identifiziert                                 │
│  → N ≈ 30 measurement_contexts                                          │
│  → R² ≈ 0.25                                                           │
│                                                                         │
│  ITERATION 2: Mehr Struktur (50-100 Papers)                             │
│  ──────────────────────────────────────────                             │
│  Fλ(Ψ) = λ_base × (1 + β_S·Stigma) × (1 + β_I·Formal)                 │
│  → Zwei-drei Treiber, Interaktionen sichtbar                            │
│  → N ≈ 150 measurement_contexts                                         │
│  → R² ≈ 0.45                                                           │
│                                                                         │
│  ITERATION 3: Vollständiges Modell (200+ Papers)                        │
│  ───────────────────────────────────────────────                        │
│  Fλ(Ψ, 10C) = λ_base × ∏ᵢ (1 + βᵢ · Ψᵢ) × ∏ⱼ (1 + γⱼ · 10Cⱼ)        │
│  → Alle relevanten Dimensionen, Interaktionen                           │
│  → N ≈ 500+ measurement_contexts                                        │
│  → R² ≈ 0.65-0.75                                                      │
│                                                                         │
│  ITERATION N: Asymptotische Konvergenz                                  │
│  ─────────────────────────────────────                                  │
│  Fθ konvergiert gegen "wahre" Kontextfunktion                          │
│  Neue Papers → Bayesian Update → Präzisere Koeffizienten               │
│                                                                         │
│  ════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  JEDES NEUE PAPER VERBESSERT DIE SCHÄTZUNG!                            │
│                                                                         │
│  Paper P mit measurement_context m:                                     │
│    1. Extrahiere (θ, Ψ, 10C) aus m                                     │
│    2. Füge zu Trainingsdaten hinzu                                     │
│    3. Re-estimiere Fθ                                                  │
│    4. Validiere: Sinkt Prediction Error?                               │
│    5. Update Parameter-Registry mit neuem Posterior                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Warum das funktioniert: Bayesian Learning

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BAYESIAN FOUNDATION                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  FORMAL:                                                                │
│                                                                         │
│  P(β | Data) ∝ P(Data | β) × P(β)                                      │
│                                                                         │
│  Prior P(β):       Informierter Start aus LLMMC + bestehender Lit.     │
│  Likelihood:       Wie gut erklärt Fθ(β) die measurement_contexts?      │
│  Posterior P(β|D): Update nach jedem neuen Paper                        │
│                                                                         │
│  PRAKTISCH:                                                             │
│                                                                         │
│  Tag 1:  N=0, verwende Prior → λ = 2.25 ± 0.75 (große Unsicherheit)   │
│  Tag 30: N=50, erstes Update → λ(Ψ_S=high) = 2.8 ± 0.3                │
│  Tag 90: N=200, viel Evidenz → λ(Ψ_S, Ψ_I) = präzise Funktion        │
│                                                                         │
│  KONVERGENZ-GARANTIE:                                                   │
│  ─────────────────────                                                  │
│  Unter milden Regularitätsbedingungen:                                  │
│  - Posterior kontrahiert auf wahren Wert                               │
│  - Credible Intervals werden enger                                     │
│  - Out-of-sample Error sinkt monoton                                   │
│                                                                         │
│  → Mit genug Daten: Fθ approximiert wahre Kontextfunktion              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Der Compound Interest Effekt

```
┌─────────────────────────────────────────────────────────────────────────┐
│  COMPOUND INTEREST: Jedes Paper macht ALLE zukünftigen Analysen besser │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TRADITIONELL:                                                          │
│  ─────────────                                                          │
│  Paper A → Parameter für Kontext A                                      │
│  Paper B → Parameter für Kontext B                                      │
│  → Isolierte Datenpunkte, keine Akkumulation                           │
│                                                                         │
│  EBF:                                                                   │
│  ────                                                                   │
│  Paper A → measurement_context → verbessert Fθ                         │
│  Paper B → measurement_context → verbessert Fθ weiter                  │
│  Paper C → measurement_context → verbessert Fθ weiter                  │
│  ...                                                                    │
│  → JEDES Paper erhöht Präzision für ALLE zukünftigen Prognosen         │
│                                                                         │
│  NACH 5 JAHREN:                                                         │
│  ──────────────                                                         │
│  - 500+ measurement_contexts für λ                                     │
│  - 300+ measurement_contexts für β                                     │
│  - 400+ measurement_contexts für α                                     │
│  → Hochpräzise Kontextfunktionen für alle wichtigen Parameter          │
│                                                                         │
│  → EBF wird mit jeder Paper-Integration WERTVOLLER                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Dokumentation in Paper-YAML

Für jeden measurement_context können optionale PCT-Felder hinzugefügt werden:

```yaml
measurement_contexts:
  - context: "welfare_takeup"
    value_estimate: "high (λ_R ≈ 2.5)"
    psi_conditions:
      Ψ_I: "bureaucratic_application"
      Ψ_S: "welfare_stigma"
      Ψ_K: "self_reliance_norm"

    # Optional: PCT-Transformation Hinweise
    pct_notes:
      transferable_to: ["healthcare", "education", "housing"]
      key_driver: "Ψ_S (stigma level)"
      sensitivity: "high to Ψ_K (cultural norms vary)"
```

### PCT Python Implementation (Layer 1)

The PCT equation is fully implemented as Python code in `scripts/pct.py`. All transformations are deterministic Layer-1 computations.

**Quick Reference:**

```python
# 1. Transform with explicit multipliers
from pct import transform_with_multipliers
result = transform_with_multipliers(theta_A=2.5, multipliers=[0.85, 0.95, 1.10])
print(result.theta_B)  # 2.2206

# 2. Transform with named Psi-deltas (auto-lookup from tables)
from pct import transform_with_deltas
result = transform_with_deltas(
    theta_A=2.5,
    deltas={"psi_S": -0.3, "psi_I": -0.1, "psi_C": 0.2},
    anchor_context="welfare", target_context="workplace",
    parameter_symbol="lambda_R", parameter_id="PAR-BEH-016",
)

# 3. Transform with categorical labels (resolves via pct-psi-scales.yaml)
from pct import transform_from_contexts
result = transform_from_contexts(
    theta_A=2.5,
    anchor_psi={"psi_S": "welfare_stigma", "psi_I": "bureaucratic_application"},
    target_psi={"psi_S": "competence_signaling", "psi_I": "professional_hierarchy"},
    anchor_context="welfare", target_context="workplace",
    parameter_symbol="lambda_R",
)

# 4. Full pipeline: PCT → LLMMC calibration (Tier 2.5)
from pct import transform_from_contexts
from llmmc_calibration import LLMMCCalibrator
cal = LLMMCCalibrator(min_anchors=5)
cal.add_pct_anchors()  # Load from measurement_contexts
cal.fit()
pct_result = transform_from_contexts(2.5, anchor_psi, target_psi)
final = cal.calibrate_with_pct(pct_result, eu_pct=0.10)
print(final.theta_final, final.ci_95, final.pct_provenance)

# 5. Universal parameter lookup (loads from registry + transforms)
from parameter_api import lookup_parameter
result = lookup_parameter(
    "PAR-BEH-001",  # Loss Aversion
    target_context={"psi_S": "competence_signaling"},
    anchor_context="welfare",
)
```

**CLI Tools:**

```bash
# PCT transformation
python scripts/pct.py --demo
python scripts/pct.py --theta 2.5 --deltas psi_S=-0.3,psi_I=-0.1
python scripts/pct.py --theta 2.5 --anchor-psi psi_S=welfare_stigma --target-psi psi_S=competence_signaling

# LLMMC + PCT demo
python scripts/llmmc_calibration.py --pct-demo

# Extract measurement contexts
python scripts/extract_measurement_contexts.py --stats

# Universal parameter lookup
python scripts/parameter_api.py --id PAR-BEH-001
python scripts/parameter_api.py --symbol lambda_R --domain finance
python scripts/parameter_api.py --id PAR-BEH-016 --target-psi psi_S=competence_signaling
```

**Data Files:**

| File | Purpose |
|------|---------|
| `data/pct-multiplier-tables.yaml` | M(ΔΨ) reference ranges per dimension |
| `data/pct-psi-scales.yaml` | Categorical label → numeric [0,1] mapping (101 labels) |
| `data/pct-measurement-contexts.yaml` | Extracted (parameter, context, Ψ) triplets |
| `data/parameter-registry.yaml` | All EBF parameter values (119 parameters) |

### Komponenten-Reihenfolge

```
PHASE 3A: Datenbanken (parallel)
├── BibTeX
├── Theory Catalog
├── Case Registry
├── Parameter Registry
└── Paper YAML (Skeleton)

PHASE 3B: Appendices (sequentiell)
├── 1. LIT Appendix (PRIMARY - zuerst!)
├── 2. CORE Extensions (nur wenn 6-Faktoren positiv)
└── 3. BCM2 Context (parallel zu CORE)

PHASE 3C: Kapitel (zuletzt)
├── Chapter-Appendix Mapping
└── Chapter Cross-References

PHASE 3D: Finalisierung
├── Paper YAML vervollständigen
└── Paper Full-Text Archive
```

---

## Phase 4: Kapitel-Relevanz-Analyse

### Klassifikation

| Relevanz | Kriterien | Aktion |
|----------|-----------|--------|
| **HIGH** | Paper erweitert CORE-Struktur des Kapitels | Cross-Ref Box + Appendix Reference |
| **MEDIUM** | Paper liefert Evidenz für Kapitel-Thema | Appendix Reference nur |
| **LOW** | Keine direkte Verbindung | Keine Aktion |

### Kapiteltyp-Priorisierung

| Kapiteltyp | Beschreibung | Typische Relevanz |
|------------|--------------|-------------------|
| **Type A (CORE)** | Kapitel zu CORE-Fragen (5, 9, 10, 11, 12, 13) | HIGH wenn CORE erweitert |
| **Type B (Foundation)** | Grundlagen-Kapitel (1-4, 6-8) | MEDIUM (Evidenz) |
| **Type C (Application)** | Anwendungs-Kapitel (14-24) | HIGH wenn anwendbar |

### Template für chapter_relevance im Paper YAML

```yaml
chapter_relevance:
  high_relevance:
    - chapter: N
      title: "Chapter Title"
      type: A/B/C
      contribution: "Was das Paper beiträgt"
      action: "Cross-reference to X added"
      status: completed
  medium_relevance:
    - chapter: M
      title: "Chapter Title"
      contribution: "Evidenz für..."
      action: "Cross-reference only"
  low_relevance:
    - chapters: [X, Y, Z]
      reason: "No structural contribution needed"
```

---

## Phase 5: Validierung (PFLICHT-GATES)

### ⚠️ KRITISCH: Validierungs-Script MUSS vor Commit ausgeführt werden!

```bash
# PFLICHT: Level 5 Integration Validator
python scripts/validate_level5_integration.py PAP-<paper_key>
```

**Compliance-Schwelle:** ≥ 80% (keine FAILs erlaubt)

### Validierungs-Output verstehen

```
✅ PASS   = Komponente korrekt integriert
⚠️ WARN   = Teilweise integriert (akzeptabel, aber verbessern)
❌ FAIL   = Komponente fehlt (BLOCKIERT Commit)
⏭️ SKIP   = Nicht anwendbar
```

### Die 13 Validierungs-Checks

| # | Check | Prüft | FAIL bedeutet |
|---|-------|-------|---------------|
| 1 | BibTeX Entry | use_for, theory_support, evidence_tier | Paper nicht in Bibliographie |
| 2 | Paper-YAML | structural_characteristics, ebf_integration | Paper-YAML unvollständig |
| 3 | Case Registry | case_id aus Paper-YAML existiert | Case nicht angelegt |
| 4 | Theory Catalog | theory_id aus Paper-YAML existiert | Theorie nicht angelegt |
| 5 | Parameter Registry | Alle parameter_integration IDs | Parameter fehlen |
| 6 | LIT-Appendix | Paper in primary_appendix referenziert | LIT nicht aktualisiert |
| 7 | BCM2 Context | bcm2_factors existieren in BCM2-Datei | Kontext-Faktoren fehlen |
| 8 | Chapter Mapping | paper_key in chapter-appendix-mapping | Mapping nicht aktualisiert |
| 9 | CORE Extensions | Axiome in CORE-Appendices (wenn status=completed) | CORE nicht erweitert |
| 10 | Full-Text | PAP-*.md in data/paper-texts/ existiert | Volltext nicht archiviert |
| 11 | Cross-References | Bidirektionale Verweise zwischen Komponenten | Referenzen fehlen |
| 12 | Chapter Relevance | Alle high_relevance Chapters haben status: completed | Dokumentierte Chapter-Aktionen nicht ausgeführt |
| 13 | Cross-DB Consistency | theory_id, case_id konsistent über alle Datenbanken | **ID-Mismatch** (ATOMIC ID RULE verletzt) |

### ATOMIC ID RULE (Prävention von ID-Mismatches)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ATOMIC ID RULE: Paper-YAML = Single Source of Truth                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Paper-YAML definiert:                                                  │
│    ├── superkey:       PAP-benabou_2022_hurts_ask                       │
│    ├── theory_id:      MS-IB-018                                        │
│    └── case_id:        UNMAPPED_CAS-902                                          │
│                                                                         │
│  ALLE anderen Registries MÜSSEN ableiten:                               │
│    ├── Case Registry:  theory_id = MS-IB-018 (von Paper-YAML)           │
│    └── Theory Catalog: bib_keys enthält paper_key                        │
│                                                                         │
│  Check 13 validiert diese Konsistenz automatisch.                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Beispiel Validierungs-Output

```
======================================================================
  LEVEL 5 INTEGRATION VALIDATION: PAP-benabou_2022_hurts_ask
======================================================================

  ✅ 1. BibTeX Entry
     BibTeX entry found with EBF fields

  ✅ 2. Paper-YAML
     Paper-YAML complete

  ✅ 3. Case Registry
     Case UNMAPPED_CAS-902 found in registry

  ✅ 4. Theory Catalog
     Theory MS-IB-018 found in catalog

  ✅ 5. Parameter Registry
     All 3 parameters found in registry

  ✅ 6. LIT-Appendix
     Paper referenced in RB_LIT-BENABOU_motivation_beliefs.tex

  ✅ 7. BCM2 Context
     All 2 BCM2 factors found

  ✅ 8. Chapter-Appendix Mapping
     Paper referenced in chapter-appendix-mapping.yaml

  ✅ 9. CORE Extensions
     CORE extensions: 1 completed, 2 cross-refs

  ✅ 10. Full-Text Archive
     Full-text archived (8,515 bytes)

  ✅ 11. Cross-References
     2 bidirectional references verified

  ✅ 12. Chapter Relevance
     All 3 high-relevance chapters completed

  ✅ 13. Cross-DB Consistency
     Cross-DB consistent: theory_id in UNMAPPED_CAS-902, paper in MS-IB-018

──────────────────────────────────────────────────────────────────────
  SUMMARY:
  ├── Passed:  13 / 13
  ├── Warned:   0 / 13
  ├── Failed:   0 / 13
  ├── Skipped:  0 / 13
  └── Compliance: 100.0%
──────────────────────────────────────────────────────────────────────
  ✅ LEVEL 5 INTEGRATION COMPLETE
======================================================================
```

### Zusätzliche Pre-Commit Checks

```bash
# 1. Paper YAML Validierung
python scripts/validate_paper_yaml_schema.py data/paper-references/PAP-*.yaml

# 2. BibTeX Integrity
python scripts/validate_bibtex.py bibliography/bcm_master.bib

# 3. Cross-Reference Integrity
python scripts/validate_referential_integrity.py

# 4. Appendix Compliance
python scripts/check_template_compliance.py appendices/<modified>.tex
```

### Commit-Message-Template

```
feat(paper): Add [Author] [Year] - Level 5 FULL integration

Components added:
- BibTeX: [key]
- Theory: MS-XX-XXX
- Case: CAS-XXX
- Parameters: PAR-XXX-XXX
- LIT Appendix: [CODE]-N (Axiom)
- CORE Extensions: [list axioms]
- BCM2 Factors: [list IDs]
- Chapter Cross-Refs: Ch [N], [M], [K]

https://claude.ai/code/session_XXXXX
```

---

## Workflow-Diagramm (Komplett)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  /integrate-paper [DOI/Title]                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: KLASSIFIKATION                                                │
│  ├── 7 Kriterien prüfen                                                 │
│  ├── Score berechnen                                                    │
│  └── Level bestimmen (1-5)                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                          Level 5?  │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: ARCHITEKTUR (6-Faktoren-Framework)                            │
│  ├── Für JEDEN relevanten CORE: F1-F6 prüfen                            │
│  ├── Entscheidung: Erweitern JA/NEIN                                    │
│  └── Architektur-Prinzip: LIT → CORE → Chapter                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: KOMPONENTEN (11-Checkliste)                                   │
│  ├── 3A: Datenbanken (parallel)                                         │
│  ├── 3B: Appendices (LIT zuerst!)                                       │
│  ├── 3C: Kapitel (Cross-References)                                     │
│  └── 3D: Finalisierung (YAML, Full-Text)                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: KAPITEL-RELEVANZ                                              │
│  ├── HIGH/MEDIUM/LOW klassifizieren                                     │
│  ├── Type A/B/C Kapitel priorisieren                                    │
│  └── chapter_relevance im YAML dokumentieren                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: VALIDIERUNG                                                   │
│  ├── Pre-Commit Checks                                                  │
│  ├── Commit mit Template                                                │
│  └── Push                                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEVEL 5 INTEGRATION - QUICK REFERENCE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ARCHITEKTUR:  LIT (Primary) → CORE (Structural) → Chapter (X-Ref)     │
│                                                                         │
│  6-FAKTOREN:   F1 Novelty · F2 Axiom · F3 Dimension · F4 Structure     │
│                F5 Universal · F6 Mechanism                              │
│                                                                         │
│  11 KOMPONENTEN:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ 1. BibTeX    │ 2. Theory   │ 3. Case     │ 4. Parameter        │   │
│  │ 5. LIT App   │ 6. CORE Ext │ 7. BCM2     │ 8. Ch-App Map       │   │
│  │ 9. Ch X-Ref  │ 10. YAML    │ 11. Full-Text                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  KAPITEL:      HIGH (Box+Ref) · MEDIUM (Ref) · LOW (nichts)            │
│                                                                         │
│  SKILL:        /integrate-paper --doi [DOI]                            │
│                /upgrade-paper [PAP-key] --level 5                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Referenz-Implementationen

### Implementation A: Bénabou, Falk & Tirole (2018)

**Paper:** "Narratives, Imperatives, and Moral Reasoning"

**SSOT:** `data/paper-references/PAP-benabou_2018_narratives.yaml`

**Commits:** Siehe Branch `claude/add-nber-paper-R9r8Y`

### Implementation B: Bénabou, Jaroszewicz & Loewenstein (2022)

**Paper:** "It Hurts To Ask" (NBER WP 30486)

**SSOT:** `data/paper-references/PAP-benabou_2022_hurts_ask.yaml`

**Komponenten:**
| Komponente | Status | ID/Pfad |
|------------|--------|---------|
| BibTeX | ✅ | `benabou_2022_hurts_ask` |
| Theory | ✅ | `MS-IB-018` (Fear of Asking) |
| Case | ✅ | `UNMAPPED_CAS-902` (Workplace Help-Seeking) |
| Parameters | ✅ | `PAR-BEH-016` (λ_R), `PAR-BEH-017` (α) |
| LIT Appendix | ✅ | UNMAPPED_RB-9 axiom in LIT-BENABOU |
| CORE Extension | ✅ | UNMAPPED_CMP-12 box in Chapter 5 |
| BCM2 Factors | ✅ | CH-SOC-14, CH-SOC-15 |
| Full-Text | ✅ | `data/paper-texts/PAP-benabou_2022_hurts_ask.md` |

**Validation:**
```bash
python scripts/validate_level5_integration.py PAP-benabou_2022_hurts_ask
# Result: 100.0% compliance, 0 FAILs, 0 WARNs
```

**Lessons Learned:**
1. **Theory-ID Konsistenz:** Sicherstellen, dass theory_id im Paper-YAML mit dem tatsächlichen Eintrag in theory-catalog.yaml übereinstimmt
2. **Parameter-Nummern prüfen:** PAR-BEH-016/017, nicht PAR-BEH-018/019 - Nummern aus Registry verifizieren
3. **BCM2-Faktoren:** context_integration in Paper-YAML muss die tatsächlich angelegten Faktoren referenzieren
4. **CORE Extensions:** Wenn Axiom in Chapter statt Appendix, in Paper-YAML mit `chapter:` und `status: completed` markieren

---

## Anhang A: Vertiefende CORE-Analyse (Referenz-Paper)

### A.1 CORE-Appendix Analyse-Matrix

Für jeden CORE-Appendix wurde folgende vertiefende Analyse durchgeführt:

#### CORE-WHAT (C) - KEINE Erweiterung

| Faktor | Analyse | Ergebnis |
|--------|---------|----------|
| **F1: Neue Struktur?** | Paper führt μv̂(a) (image utility) ein. ABER: Diese Komponente existiert bereits in CORE-WHAT als Teil der psychologischen Dimension (P in FEPSDE). | ❌ NEIN |
| **F2: Neues Axiom?** | Kein neues Axiom erforderlich - image concerns sind bereits durch U_P abgedeckt. | ❌ NEIN |
| **F3: Dimensionalität?** | FEPSDE bleibt 6-dimensional. Moral identity passt in P und S. | ❌ NEIN |
| **F4: Struktur vs. Parameter?** | μ (image weight) ist ein Parameter, keine neue Struktur. | ❌ Parameter |
| **Entscheidung** | **KEINE Erweiterung** - μ geht in WHERE (BBB) als literatur-validierter Parameter | ❌ |

**Begründung:** Das Paper formalisiert image concerns (μv̂), aber diese sind bereits Teil der psychologischen Utility-Dimension in CORE-WHAT. Die Stärke μ ist ein Parameter, keine strukturelle Erweiterung.

---

#### CORE-HOW (B) - ERWEITERUNG: UNMAPPED_CMP-11

| Faktor | Analyse | Ergebnis |
|--------|---------|----------|
| **F1: Neue Struktur?** | γ(N) - Complementarity als Funktion der Narrative. Das ist NEU: γ war bisher als Funktion von Ψ (Kontext), nicht von N (Narrativ). | ✅ JA |
| **F2: Neues Axiom?** | Ja: "Narratives can reverse the sign of γ" ist eine neue, axiomatisierbare Aussage. | ✅ JA |
| **F3: Dimensionalität?** | Nein - γ bleibt γ, nur die Abhängigkeit erweitert sich. | ❌ NEIN |
| **F4: Struktur vs. Parameter?** | STRUKTUR: γ(N) mit sgn-Reversal ist strukturell anders als γ(Ψ). | ✅ Struktur |
| **F5: Universalität?** | Ja - Narrative Modulation gilt für ALLE γ, nicht nur spezifische. | ✅ JA |
| **F6: Neuer Mechanismus?** | Ja - Exkulpatorische vs. responsiblisierende Narrative als Mechanismus für γ-Flip. | ✅ JA |
| **Entscheidung** | **UNMAPPED_CMP-11 hinzufügen** mit Cross-Ref zu UNMAPPED_RB-7 | ✅ |

**Begründung:** Das Paper zeigt, dass Narrative nicht nur die Magnitude von γ beeinflussen (das wäre UNMAPPED_CMP-4), sondern das VORZEICHEN umkehren können. Das ist eine fundamentale strukturelle Erweiterung: Aktivitäten, die normalerweise Komplemente sind (γ > 0), werden durch exkulpatorische Narrative zu Substituten (γ < 0).

**Formale Ergänzung:**
```latex
\gamma_{ij}(N) = \gamma_{ij}^{\text{base}} + \Delta\gamma(N)
\quad \text{where } \text{sgn}(\gamma_{ij}(N)) \text{ can differ from } \text{sgn}(\gamma_{ij}^{\text{base}})
```

---

#### CORE-WHEN (V) - ERWEITERUNG: ρ Parameter in Ψ_S

| Faktor | Analyse | Ergebnis |
|--------|---------|----------|
| **F1: Neue Struktur?** | ρ (network persistence/segregation) als neuer Kontext-Parameter in Ψ_S. | ✅ JA |
| **F2: Neues Axiom?** | Nicht zwingend - ρ erweitert bestehende Struktur. | ❌ NEIN |
| **F3: Dimensionalität?** | Nein - Ψ_S bleibt eine Dimension, ρ ist ein Parameter darin. | ❌ NEIN |
| **F4: Struktur vs. Parameter?** | STRUKTUR: ρ definiert die Netzwerk-Topologie, nicht nur einen Wert. | ✅ Struktur |
| **F5: Universalität?** | Ja - Netzwerk-Segregation ist universell relevant (nicht nur für Moral). | ✅ JA |
| **F6: Neuer Mechanismus?** | Ja - Narrative Transmission über Netzwerke. | ✅ JA |
| **Entscheidung** | **ρ in Ψ_S aufnehmen** mit Cross-Ref zu RB | ✅ |

**Begründung:** Das Paper formalisiert ρ ∈ [0,1] als Mass für Netzwerk-Segregation. Bei ρ → 1 (homophile Netzwerke) verstärkt sich Polarisierung; bei ρ → 0 (gemischte Netzwerke) konvergieren Narrative. Dies ist eine strukturelle Erweiterung des sozialen Kontexts Ψ_S.

**Formale Ergänzung:**
```latex
N^{-}_{A} = \frac{\pi(1-x)}{1 - \rho(1-x)}
```
ρ bestimmt den "social multiplier" für Narrative-Transmission.

---

#### CORE-AWARE (AU) - ERWEITERUNG: AWX-A5

| Faktor | Analyse | Ergebnis |
|--------|---------|----------|
| **F1: Neue Struktur?** | A_moral als Komponente von A(·) - moralische Awareness. | ✅ JA |
| **F2: Neues Axiom?** | Ja: Narrative beeinflussen A_moral systematisch. | ✅ JA |
| **F3: Dimensionalität?** | Ja - A(·) erhält eine neue Subkomponente. | ✅ JA |
| **F4: Struktur vs. Parameter?** | STRUKTUR: Narrative Transmission ist ein Mechanismus, kein Parameter. | ✅ Struktur |
| **F5: Universalität?** | Ja - Moralische Awareness gilt für alle Entscheidungen mit ethischer Komponente. | ✅ JA |
| **F6: Neuer Mechanismus?** | Ja - Search for reasons (xH, xL) als Awareness-Mechanismus. | ✅ JA |
| **Entscheidung** | **AWX-A5 hinzufügen** - Moral Narratives and Awareness | ✅ |

**Begründung:** Das Paper zeigt, dass Menschen aktiv nach "reasons" suchen, um Verhalten zu rechtfertigen. Diese Search-Intensität (xH, xL) modifiziert A_moral. Exkulpatorische Narrative reduzieren A_moral, responsiblisierende erhöhen sie.

**Formale Ergänzung:**
```latex
A_{\text{moral}}(N, x) = A_{\text{base}} + \Delta A(N) \cdot f(x)
```
wobei x die Search-Intensität und N die dominante Narrative ist.

---

#### CORE-EIT (IE) - KEINE Erweiterung

| Faktor | Analyse | Ergebnis |
|--------|---------|----------|
| **F1: Neue Struktur?** | Narratives als Interventionstyp? PRÜFUNG: Narrative Interventionen existieren bereits als Kombination von I_AWARE (Framing) + I_WHAT (Identity). | ❌ NEIN |
| **F2: Neues Axiom?** | Kein neues Axiom - Narrative-Interventionen sind spezielle Parametrisierungen des 9D-Vektors. | ❌ NEIN |
| **F3: Dimensionalität?** | 9D-Vektor bleibt 9D. | ❌ NEIN |
| **F4: Struktur vs. Parameter?** | Parameter: Wie stark I_AWARE vs I_WHAT gewichtet wird. | ❌ Parameter |
| **Entscheidung** | **KEINE Erweiterung** - Narrative Interventionen = I_AWARE + I_WHAT,S | ❌ |

**Begründung:** Narrative Interventionen sind keine neue Interventionsdimension, sondern eine Kombination bestehender Dimensionen. "Responsibilizing narrative" aktiviert I_AWARE (Salienz moralischer Implikationen) und I_WHAT,S (soziale Identität). Die Stärke ist eine Parametrisierungsfrage.

---

### A.2 Kapitel-Analyse-Matrix

Für alle 24 Kapitel wurde folgende Relevanz-Analyse durchgeführt:

#### HIGH RELEVANCE (3 Kapitel)

| Kapitel | Typ | Analyse | Aktion |
|---------|-----|---------|--------|
| **Ch 5: Complementarity** | A (CORE) | Paper erweitert γ durch UNMAPPED_CMP-11 (sign reversal). Das ist DIREKTE Erweiterung des Kernformalismus. | Cross-Ref Box + Appendix UNMAPPED_RB Reference |
| **Ch 22: Policy Applications** | C (App) | Narrative design ist zentral für Policy-Interventionen. I_AWARE + Framing-Strategien basieren auf Paper. | Appendix UNMAPPED_RB Reference für narrative-aware policy |
| **Ch 23: Multi-Level Implementation** | C (App) | ρ (Netzwerk-Struktur) ist kritisch für Implementation. Homophile vs. gemischte Netzwerke determinieren Narrative-Spread. | Appendix UNMAPPED_V + RB Reference, CH-SOC-13 Note |

**Detaillierte Begründung Ch 5:**
```
Das Kapitel "Complementarity as Structural Principle" definiert γ als Kern des EBF.
Das Paper zeigt, dass γ(N) das Vorzeichen wechseln kann basierend auf Narrativen.
→ DIREKTE strukturelle Erweiterung → HIGH + Cross-Ref Box
```

**Detaillierte Begründung Ch 22:**
```
Policy-Kapitel diskutiert Interventionsdesign.
Paper zeigt: Narrative Framing kann Backfire verursachen (exkulpatorisch)
           oder Wirkung verstärken (responsibilisierend).
→ Zentral für Policy-Praxis → HIGH
```

**Detaillierte Begründung Ch 23:**
```
Multi-Level Implementation braucht Verständnis von Diffusion.
Paper formalisiert: ρ bestimmt, ob Narrative polarisieren oder konvergieren.
→ Kritisch für Implementationsstrategie → HIGH
```

---

#### MEDIUM RELEVANCE (3 Kapitel)

| Kapitel | Typ | Analyse | Aktion |
|---------|-----|---------|--------|
| **Ch 2: Rationality & Stability** | B (Found) | Image concerns (μv̂) beziehen sich auf Stabilitätskonzept (consistent self-image). | Cross-reference only |
| **Ch 3: Limits of Utility** | B (Found) | Moralisches Reasoning als Utility-Dimension - Paper liefert Evidenz für non-consequentialist preferences. | Cross-reference only |
| **Ch 4: Empirical Foundations** | B (Found) | Paper diskutiert experimentelle Evidenz zu moral behavior (70+ Referenzen). | Cross-reference to RB |

**Detaillierte Begründung Ch 2:**
```
Kapitel diskutiert Rationalität und stabile Präferenzen.
Paper zeigt: Image concerns (μ) erzeugen "Rationalität" auch bei eigentlich
            irrationalen Handlungen (um Image zu wahren).
→ Relevante Evidenz, aber keine strukturelle Erweiterung → MEDIUM
```

---

#### LOW RELEVANCE (18 Kapitel)

| Kapitel | Begründung |
|---------|------------|
| **Ch 1: Introduction** | Kein struktureller Beitrag - Paper nicht für Intro relevant |
| **Ch 6-8: Reference Structure, Fit, Mathematical** | Technische Kapitel ohne direkte Verbindung zu Moral Narratives |
| **Ch 9-13: CORE Chapters (WHO, WHAT, HOW, WHEN, WHERE, AWARE)** | CORE-Erweiterungen passieren in Appendices, nicht in Kapiteln |
| **Ch 14-20: Domain Applications** | Spezifische Domains - Paper hat keine domain-spezifische Relevanz |
| **Ch 21: Measurement** | Keine Messvorschriften für narrative effects im Paper |
| **Ch 24: Emergent Life Journeys** | Lifecycle-Perspektive nicht im Paper-Fokus |

**Begründung für LOW bei CORE-Kapiteln (9-13):**
```
CORE-Kapitel referenzieren ihre CORE-Appendices.
Die Erweiterungen (UNMAPPED_CMP-11, AWX-A5, ρ) sind in den APPENDICES dokumentiert.
Kapitel brauchen keine zusätzlichen Cross-References - sie verweisen
automatisch auf die erweiterten Appendices.
→ LOW (Erweiterung passiert auf Appendix-Ebene)
```

---

### A.3 BCM2 Kontext-Faktoren Analyse

Drei neue Kontext-Faktoren wurden identifiziert:

| Factor ID | Name | Kategorie | Begründung |
|-----------|------|-----------|------------|
| **CH-SOC-13** | Netzwerk-Segregation (ρ) | SOC | ρ ∈ [0,1] bestimmt Homophilie im Netzwerk. Direkt aus Paper: "mixing reduces polarization" |
| **CH-ETH-13** | Narrative Polarisierung | ETH | Prävalenz exkulpatorischer vs. responsibilisierender Narrative in Population |
| **CH-ETH-14** | Attributionstendenz | ETH | Externe vs. interne Verantwortungszuschreibung. Aus Paper: "downplaying externalities" |

**Warum diese Faktoren?**
```
Das Paper zeigt, dass moralisches Verhalten stark von Kontextfaktoren abhängt:
1. Netzwerk-Struktur (ρ) → SOC-Kategorie
2. Dominante Narrative → ETH-Kategorie
3. Attributionsmuster → ETH-Kategorie

Diese drei Faktoren ermöglichen BCM2-basierte Vorhersagen für
moral behavior in verschiedenen Kontexten.
```

---

## Anhang B: Checkliste der dokumentierten Analysen

```
✅ CORE-Analyse (6-Faktoren für jeden CORE)
   ├── ✅ CORE-WHAT: Keine Erweiterung (μ ist Parameter)
   ├── ✅ CORE-HOW: UNMAPPED_CMP-11 (γ sign reversal)
   ├── ✅ CORE-WHEN: ρ Parameter in Ψ_S
   ├── ✅ CORE-AWARE: AWX-A5 (moral narratives)
   └── ✅ CORE-EIT: Keine Erweiterung (I_AWARE + I_WHAT reicht)

✅ Kapitel-Analyse (HIGH/MEDIUM/LOW für alle 24)
   ├── ✅ HIGH: Ch 5, 22, 23 (Cross-Ref Boxes)
   ├── ✅ MEDIUM: Ch 2, 3, 4 (Cross-Ref only)
   └── ✅ LOW: Ch 1, 6-21, 24 (Keine Aktion)

✅ BCM2-Analyse (neue Kontext-Faktoren)
   ├── ✅ CH-SOC-13: Netzwerk-Segregation
   ├── ✅ CH-ETH-13: Narrative Polarisierung
   └── ✅ CH-ETH-14: Attributionstendenz
```

---

*Version 1.1 | 2026-02-04 | Erweitert um Anhang A+B (Vertiefende Analyse)*
