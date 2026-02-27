# Chapter ↔ Appendix Mapping

> **EBF Framework - Vollständiges Navigationsverzeichnis**
>
> Letzte Aktualisierung: 2026-01-20

---

## Übersicht

Das EBF Dokument folgt einer dualen Struktur:
- **Hauptkapitel (1-19):** Konzeptuelle Darstellung, narrativer Fluss
- **Appendices (49):** Technische Details, formale Spezifikationen, Beweise

Jedes Appendix ist mit mindestens einem Hauptkapitel verlinkt. Dieses Dokument bietet bidirektionale Navigation.

---

## Die acht 10C CORE-Appendices

Die 10C CORE-Appendices beantworten die acht fundamentalen Fragen des EBF Frameworks:

| CORE | Code | Appendix | Frage | Symbol | Primary Chapter |
|------|------|----------|-------|--------|-----------------|
| **WHO** | AAA | [Aggregation Levels](../appendices/AAA_aggregation_levels.tex) | Wer hat Utility? | $L$ | Ch. 2 |
| **WHAT** | C | [FEPSDE Matrix](../appendices/C_fepsde_matrix.tex) | Was ist Utility? | $d$ | Ch. 3 |
| **HOW** | B | [Complementarity](../appendices/B_complementarity_levels.tex) | Wie interagieren sie? | $\gamma$ | Ch. 4 |
| **WHEN** | V | [Ψ-Dimensions](../appendices/V_psi_dimensions.tex) | Wann zählt Kontext? | $\Psi$ | Ch. 5 |
| **WHERE** | BBB | [Estimation Methodology](../appendices/BBB_estimation_methodology.tex) | Woher kommen die Zahlen? | $\Theta, E(\theta)$ | Ch. 6 |
| **AWARE** | AU | [The Awareness Function](../appendices/AU_bcm_axiom_formalization.tex) | Wie bewusst bin ich mir? | $A(\cdot)$ | Ch. 11 |
| **READY** | AV | [The Willingness Function](../appendices/AV_willingness_formalization.tex) | Wie handlungsbereit bin ich? | $WAX, \theta$ | Ch. 12 |
| **STAGE** | AW | [Behavioral Change Journey](../appendices/AW_behavioral_change_journey.tex) | Wo in der Veränderung? | $S(t), dS/dt$ | Ch. 13 |

### Die integrierte EBF Formel

```
Stage 1: Utility Definition (COREs 1-5)
U^{pot}_{total}(Ψ) = Σ_L α^L(Ψ) · [ Σ_d ω^L_d · U^L_d + Σ_{d<d'} γ^L_{dd'} · U^L_d · U^L_{d'} ]

Stage 2: Awareness Filter (CORE 6: AWARE)
U^{eff}_{total}(t*) = A(t*) × U^{pot}_{total}

Stage 3: Action Threshold (CORE 7: READY)
Action ⟺ WAX(U^{eff}, φ, Ψ) ≥ θ(Ψ)

Stage 4: Behavioral Change Journey (CORE 8)
dS/dt = (1/τ) · [S*(A, WAX, Ψ) - S(t)]

Wobei:
  L        ← CORE-WHO (AAA): Ebenen
  d        ← CORE-WHAT (C): Dimensionen
  γ        ← CORE-HOW (B): Interaktionen
  Ψ, α     ← CORE-WHEN (V): Kontext
  E(θ)     ← CORE-WHERE (BBB): Parameterschätzungen
  A(t*)    ← CORE-AWARE (AU): Salienz-Filter (Transformation U_pot → U_eff)
  WAX, θ   ← CORE-READY (AV): Handlungsschwelle (Brücke Wissen → Handeln)
  S(t), τ  ← CORE-STAGE (AW): Behavioral Change Journey (Veränderungsdynamik)
```

---

## Kapitel → Appendix Mapping

### Kapitel 1: Introduction
| Appendix | Name | Relevanz |
|----------|------|----------|
| I | Nobel Contributions | Historische Einordnung |
| H | Computational History | Entwicklungsgeschichte |
| G | Glossary | Terminologie |

### Kapitel 2: Rationality as Stability
| Appendix | Name | Relevanz |
|----------|------|----------|
| T | Metatheory | Philosophische Grundlagen |
| U | Kahneman-Tversky | Behavioral Foundations |

### Kapitel 3: Limits of Classical Utility
| Appendix | Name | Relevanz |
|----------|------|----------|
| U | Kahneman-Tversky | Prospect Theory |
| AD | Evolutionary Game Theory | Alternative Ansätze |
| AF | Social Choice | Aggregationsprobleme |
| M | Shleifer Papers | Behavioral Finance |

### Kapitel 4: Empirical Foundations
| Appendix | Name | Relevanz |
|----------|------|----------|
| E | Operationalization | Messprotokoll |
| R | Evaluation Protocol | Validierung |
| J | Recent Papers | Aktuelle Evidenz |
| K | Fehr Papers | Experimentelle Evidenz |
| N | Heckman Papers | Kausalidentifikation |
| P | Duflo Papers | RCT-Methodik |

### Kapitel 4x: Calibration not Simulation
| Appendix | Name | Relevanz |
|----------|------|----------|
| **AN** | **LLM Monte Carlo** | **Kernmethodik** |
| BBB | Parameter Estimation | Schätzmethodik |

### Kapitel 5: Complementarity ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **B** | **CORE-HOW** | **Kerntheorie** |
| X | Milgrom-Roberts | Supermodularität |
| AC | Industrial Organization | Firmen-Komplementarität |
| AB | Matching Theory | Marktdesign |
| AE | Mechanism Design | Incentive-Komplementarität |

### Kapitel 6: Reference Structure
| Appendix | Name | Relevanz |
|----------|------|----------|
| C | CORE-WHAT | Referenzpunkte nach Dimension |
| U | Kahneman-Tversky | Prospect Theory Foundations |

### Kapitel 7: Fit and Non-Concavity ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **NC** | **FORMAL-NC: Non-Concavity, Fit, Coherence** | **Primärer Appendix** - Axiome UNMAPPED_NC-1 bis UNMAPPED_NC-4, K vs Q |
| MIL | LIT-MILGROM: Milgrom-Roberts | Supermodularität, Roberts "The Modern Firm" |
| B | CORE-HOW | γ > 0 → Non-Concavity |
| VII | FORMAL-GTC | General Theory of Complementarity |
| A | FORMAL-DERIVE | Mathematische Grundlagen |

**NC Cross-Reference Netzwerk:**
```
Chapter 7 ←→ NC (Primary)
     ↓
┌────┴────┬─────────┬─────────┬─────────┐
↓         ↓         ↓         ↓         ↓
B       MIL       VII        X        XI
HOW    Roberts    GTC       FND      MDL
     ↓         ↓         ↓
   HIE       EQU       MEQ
HIERARCHY  Equilib.  Multi-Eq
     ↓
    IE
   EIT
```

### Kapitel 8: Mathematical Foundations
| Appendix | Name | Relevanz |
|----------|------|----------|
| A | Formal Derivations | Herleitungen |
| D | Proofs | Beweise |
| AU | CORE-AWARE: The Awareness Function | 6th CORE: $U_{eff} = A \times U_{pot}$ |

### Kapitel 9: Context as Endogenous ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **V** | **CORE-WHEN** | **Kerntheorie** |
| AH | Temporal Context | Zeit-Dimension |
| AI | Spatial Context | Raum-Dimension |
| AAA | CORE-WHO | Level Salience |
| AG | Complexity Economics | Emergente Eigenschaften |
| L | Acemoglu Papers | Institutionen |
| Q | Bloom Papers | Unsicherheit |
| W | Information Economics | Informationsasymmetrien |

### Kapitel 10: Die Nutzenarchitektur (INU/KNU/IDN) ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **C** | **CORE-WHAT** | **Kerntheorie** |
| **AAA** | **CORE-WHO** | **Aggregationsebenen** |
| AU | CORE-AWARE: The Awareness Function | 6th CORE |
| AJ | Social Preferences | INU/KNU/IDN |

#### Unterkapitel 10.1-10.9
| Unterkapitel | Appendix | Relevanz |
|--------------|----------|----------|
| 10.1 Three Utility Categories | AJ | Social Preferences |
| 10.2 FEPSDE Dimensions | C | Vollständige Matrix |
| 10.3 144 Components | C | Komponenten-Struktur |
| 10.6 Inter-Category Compl. | B | Interaktionsstruktur |
| 10.7 Context Modulation | V | Ψ-Modulation |
| 10.8 Aggregate Welfare | AAA | Hierarchie-Aggregation |
| 10.9.1 Labor Transitions | AA | Arbeitsmarkt |
| 10.9.2 Health Prevention | F | Worked Examples |
| 10.9.3 Financial Decisions | Y | Kapitalmärkte |
| 10.9.4 Sustainability | Z | Wachstumstheorie |

### Kapitel 11: Awareness ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| AV | Willingness Formalization | Formale Grundlagen |
| AL | Self-Reinforcement Learning | Lernmechanismen |
| AK | Epistemics of Deviation | Belief-Formation |
| AAA | CORE-WHO | Level-spezifische Awareness |

#### Predictions (Ch. 11 Unterkapitel)
| Prediction | Appendix | Thema |
|------------|----------|-------|
| 11.1 | AO | Trade War Dynamics |
| 11.2 | AP | Cross-Level Spillovers |
| 11.3 | AQ | Asymmetric Response |
| 11.4 | AR | Techlash Dynamics |
| 11.5 | AS | Identity Activation |
| 11.6 | AT | Coherence Trap |

### Kapitel 12: Willingness
| Appendix | Name | Relevanz |
|----------|------|----------|
| **AV** | **Willingness Formalization** | **Kerntheorie** |
| AL | Self-Reinforcement Learning | Dynamik |

### Kapitel 13: Behavioral Change Journey
| Appendix | Name | Relevanz |
|----------|------|----------|
| — | — | Stage-Logik im Haupttext |

### Kapitel 14: Behavioral Change Segments
| Appendix | Name | Relevanz |
|----------|------|----------|
| — | — | Segment-Typologien im Haupttext |

### Kapitel 15: Function of Willingness, Journey & Segment
| Appendix | Name | Relevanz |
|----------|------|----------|
| AU | CORE-AWARE | Awareness-Baustein |
| AV | Willingness Formalization | Schwelle & WAX |

### Kapitel 16: Probability of Behavior Change (P_eff) ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **IE** | **CORE-EIT: Emergent Intervention Theory** | **P_eff ← α_BCJ, β_BCS emergence** |
| AV | CORE-READY | W_eff → P_eff Transformation |
| AW | CORE-STAGE | BCJ Phase → α_BCJ Multiplier |
| HHH | METHOD-TOOLKIT | Operational output format |

### Kapitel 17: Intervention Foundations ⭐ (IE Primary)
| Appendix | Name | Relevanz |
|----------|------|----------|
| **IE** | **CORE-EIT: Emergent Intervention Theory** | **Primärer Appendix** - Axiome EIT-1 bis EIT-5 |
| **HHH** | **METHOD-TOOLKIT** | **Operations** - 20-Field Schema, emergent intervention concept |
| S | Falsifiable Predictions | Testbare Vorhersagen |
| P | Duflo Papers | Policy-Evaluierung |
| F | Worked Examples | Anwendungen |

### Kapitel 18: Journey-Phase Targeting ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **IE** | **CORE-EIT** | **Secondary** - Phase-Type Affinity (α_BCJ) |
| **HHH** | **METHOD-TOOLKIT** | Phase-specific intervention selection |
| AW | CORE-STAGE | BCJ Phase definitions (φ ∈ {1,...,5}) |
| S | Falsifiable Predictions | Phase-specific predictions |
| R | Evaluation Protocol | Phase measurement |

### Kapitel 19: Segment Targeting ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **IE** | **CORE-EIT** | **Secondary** - Segment-Type Multiplier (β_BCS) |
| **HHH** | **METHOD-TOOLKIT** | Segment-specific intervention selection |
| PAP1 | FORMAL-SEGMENT | Segment axioms |
| S | Falsifiable Predictions | Segment-specific predictions |

### Kapitel 20: Portfolio Design ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **IE** | **CORE-EIT** | **Secondary** - Crowding-Out (γ_ij), Emergence |
| **HHH** | **METHOD-TOOLKIT** | Portfolio construction, F10 Complementarity |
| PAP | FORMAL-EQUILIBRIA | Intervention equilibria |
| B | CORE-HOW | γ_ij for intervention combinations |
| LET | FORMAL-LET | Level Emergence Theorem |

### Kapitel 21 (geplant): Conclusion
| Appendix | Name | Relevanz |
|----------|------|----------|
| G | Glossary | Terminologie-Referenz |
| T | Metatheory | Abschließende Reflexion |

---

## Appendix → Kapitel Mapping (Vollständig)

### 10 CORE Appendices (10C + EIT)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| **AAA** | **CORE-WHO: Welfare Hierarchy** | **CORE** | **10.8** | 9, 11 |
| **C** | **CORE-WHAT: FEPSDE Dimensions** | **CORE** | **10** | 6 |
| **B** | **CORE-HOW: Complementarity γ** | **CORE** | **5** | 7, 10.6 |
| **V** | **CORE-WHEN: Context Ψ** | **CORE** | **9** | 10.7 |
| **BBB** | **CORE-WHERE: Parameter Θ** | **CORE** | **4x** | 4, 8 |
| **AU** | **CORE-AWARE: Awareness A(·)** | **CORE** | **11** | 10, 12 |
| **AV** | **CORE-READY: Willingness WAX** | **CORE** | **12** | 11 |
| **AW** | **CORE-STAGE: BCJ Phase φ** | **CORE** | **13** | 18 |
| **HI** | **CORE-HIERARCHY: Decision Levels L0-L3** | **CORE** | **15** | 5, 20 |
| **IE** | **CORE-EIT: Emergent Intervention Theory** | **CORE** | **17** | 7, 16, 18, 19, 20 |

### FORMAL Appendices (16)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| A | FORMAL-DERIVE: Derivations | FORMAL | 8 | 5, 10 |
| D | FORMAL-PROOF: Theorem Proofs | FORMAL | 8 | All |
| BA | FORMAL-SEGMENT: Segment Axioms | FORMAL | 14 | 19 |
| BB | FORMAL-EQUILIBRIA: Intervention Equilibria | FORMAL | 20 | 17 |
| BC | FORMAL-PROBABILITY: P1-P10 Axioms | FORMAL | 16 | 15 |
| **NC** | **FORMAL-NC: Non-Concavity, K vs Q** | **FORMAL** | **7** | 5, 8, 15 |
| III | FORMAL-EIH: Efficient Intervention Hypothesis | FORMAL | 17 | 20 |
| IV | FORMAL-LET: Level Emergence Theorem | FORMAL | 15 | 5 |
| V | FORMAL-MEP: Minimum Effective Portfolio | FORMAL | 20 | 17 |
| VI | FORMAL-MEQ: Multiple Equilibria Theorem | FORMAL | 7 | 15 |
| VII | FORMAL-GTC: General Theory Complementarity | FORMAL | 5 | 7, 8 |
| X | FORMAL-FOUND: Math Foundations | FORMAL | 8 | 5 |
| XI | FORMAL-MODELS: Canonical Models A-F | FORMAL | 5 | 8 |
| CJ | FORMAL-BELIEFARCHITECTURE | FORMAL | — | Context |
| CK | FORMAL-BELIEFOPPOSITIONS | FORMAL | — | Context |
| CM | FORMAL-FAIRNESSALIGNMENT | FORMAL | — | Context |
| UN | FORMAL-UNTCM: Unified Natural Trajectory | FORMAL | — | 13 |

### DOMAIN Appendices (17)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| AA | DOMAIN-LABOR: Labor Economics | DOMAIN | 10.9.1 | 4 |
| AB | DOMAIN-MATCH: Matching Theory | DOMAIN | 5 | 10.6 |
| AC | DOMAIN-IO: Industrial Organization | DOMAIN | 5 | 7 |
| AD | DOMAIN-EVO: Evolutionary GT | DOMAIN | 3 | 5 |
| AE | DOMAIN-MECH: Mechanism Design | DOMAIN | 5 | 9 |
| AF | DOMAIN-CHOICE: Social Choice | DOMAIN | 3 | 10.8 |
| AG | DOMAIN-COMPLEX: Complexity Economics | DOMAIN | 9 | 5 |
| AH | DOMAIN-CONSULTING: Behavioral Consulting | DOMAIN | — | All |
| AJ | DOMAIN-SOCIAL: Social Preferences | DOMAIN | 10.1 | 4 |
| AK | DOMAIN-EPISTEMIC: Epistemics | DOMAIN | 11.3 | 9 |
| W | DOMAIN-INFO: Information Economics | DOMAIN | 9 | 5 |
| X | DOMAIN-COMPLEMENT: Milgrom-Roberts | DOMAIN | 5 | 7 |
| Y | DOMAIN-CAPITAL: Capital Markets | DOMAIN | 10.9.3 | 5 |
| Z | DOMAIN-GROWTH: Growth Theory | DOMAIN | 10.8 | 9 |
| BF | DOMAIN-SOCIALDEMOCRACY | DOMAIN | — | Context |
| XII | DOMAIN-FOUND: Domain Foundations | DOMAIN | — | All |
| XIII | DOMAIN-EBF: EBF Application | DOMAIN | — | All |
| XIV | DOMAIN-CATALOG: Universal Domain Map | DOMAIN | — | All |

### CONTEXT Appendices (5)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| AH | CONTEXT-TIME: Temporal Ψ_T | CONTEXT | 9 | 10.7 |
| AI | CONTEXT-SPACE: Spatial Ψ_Sp | CONTEXT | 9 | 10.7 |
| BG | CONTEXT-GENESIS: Austrian Media | CONTEXT | — | — |
| BH | CONTEXT-SPÖ_PARADOX | CONTEXT | — | — |
| DX | CONTEXT-MEDIA: Political Economy | CONTEXT | — | — |

### METHOD Appendices (14)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| E | METHOD-OPS: Operationalization | METHOD | 4 | 10 |
| R | METHOD-EVAL: Evaluation Protocol | METHOD | 4 | 18 |
| AL | METHOD-SRL: Self-Reinforcement | METHOD | 11 | 9 |
| AN | METHOD-LLMMC: LLM Monte Carlo | METHOD | 4x | 4 |
| AZ | METHOD-CONSTRUCT: Model Construction | METHOD | — | All |
| QQQ | METHOD-QA: Quality Assessment | METHOD | — | All |
| CCC | METHOD-DOCTYPE: 8D Document Clustering | METHOD | — | All |
| **EEE** | **METHOD-DESIGN: Model Design Workflow** | **METHOD** | **—** | All |
| **FFF** | **METHOD-REGISTRY: Model Archive** | **METHOD** | **—** | All |
| **GGG** | **METHOD-CONFIG: Model Configurator** | **METHOD** | **—** | All |
| **HHH** | **METHOD-TOOLKIT: Intervention Design** | **METHOD** | **17** | 16, 18, 19, 20 |
| VIII | METHOD-COMP: Complementarity Methodology | METHOD | 5 | 8 |
| IX | METHOD-RESEARCH: Research Agenda | METHOD | — | All |
| XX | METHOD-EVIDENCE: Disciplinary Boundaries | METHOD | — | 4 |

### PREDICT Appendices (7)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| S | PREDICT-MASTER: Falsifiable Predictions | PREDICT | 18 | 4 |
| AO | PREDICT-01: Trade War Dynamics | PREDICT | 11.1 | 9 |
| AP | PREDICT-02: Spillover Effects | PREDICT | 11.2 | 10.8 |
| AQ | PREDICT-03: Asymmetric Response | PREDICT | 11.3 | 10 |
| AR | PREDICT-04: Techlash Dynamics | PREDICT | 11.4 | 9 |
| AS | PREDICT-05: Identity Activation | PREDICT | 11.5 | 10.1 |
| AT | PREDICT-06: Coherence Trap | PREDICT | 11.6 | 10.8 |
| HF | PREDICT-HABIT: Habit Formation | PREDICT | — | 13 |

### LIT Appendices (8+)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| I | LIT-NOBEL: Nobel Laureates | LIT | 1 | All |
| J | LIT-RECENT: Recent Papers 2020-25 | LIT | 4 | All |
| K | LIT-FEHR: Ernst Fehr | LIT | 4 | 10.1 |
| L | LIT-ACEMOGLU: Daron Acemoglu | LIT | 9 | 10.8 |
| M | LIT-SHLEIFER: Andrei Shleifer | LIT | 3 | 5 |
| N | LIT-HECKMAN: James Heckman | LIT | 4 | 10.9 |
| O | LIT-AUTOR: David Autor | LIT | 10.9.1 | 4 |
| P | LIT-DUFLO: Esther Duflo | LIT | 4 | 17 |
| Q | LIT-BLOOM: Nick Bloom | LIT | 9 | 5 |
| U | LIT-KT: Kahneman-Tversky | LIT | 3, 6 | 10 |
| MIL | LIT-MILGROM: Milgrom-Roberts | LIT | 5 | 7 |

### REF Appendices (4)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| F | REF-EXAMPLES: Worked Examples | REF | 10.9 | All |
| G | REF-GLOSSARY: Terminology | REF | All | — |
| H | REF-HISTORY: Computational History | REF | 1 | — |
| T | REF-META: Metatheory | REF | 2 | 18 |

---

## Lesepfade

### Pfad 1: Core Theory (Essential) — 10C CORE
```
1. AAA (CORE-WHO) → Verstehe Ebenen L
2. C (CORE-WHAT) → Verstehe Dimensionen d (FEPSDE)
3. B (CORE-HOW) → Verstehe Interaktionen γ
4. V (CORE-WHEN) → Verstehe Kontext Ψ
5. BBB (CORE-WHERE) → Verstehe Parameterschätzung Θ
6. AU (CORE-AWARE) → Verstehe Salienz-Filter A(·): U_pot → U_eff
7. AV (CORE-READY) → Verstehe Handlungsbereitschaft WAX ≥ θ
8. AW (CORE-STAGE) → Verstehe BCJ-Phase φ ∈ {1,...,5}
9. HI (CORE-HIERARCHY) → Verstehe Decision Levels L0-L3, N_L2 = f(γ)
10. IE (CORE-EIT) → Verstehe Emergent Intervention Theory, $\vec{I} \in [0,1]^9$
```

### Pfad 2: Empirischer Forscher
```
1. CORE-WHO + CORE-WHAT → Basis-Framework
2. E (Operationalization) → Messung
3. AN (LLM Monte Carlo) → Schätzung
4. S (Predictions) → Testbare Hypothesen
```

### Pfad 3: Domain-Spezialist
```
1. CORE Appendices → Grundlagen
2. Relevantes DOMAIN Appendix → Dein Feld
3. LIT Appendices → Schlüsselforscher
```

### Pfad 4: Quick Reference
```
1. G (Glossary) → Terminologie
2. F (Worked Examples) → Anwendungen
3. Spezifisches Appendix nach Bedarf
```

---

## Theoretische Grundlage der Cross-References

Die 10C CORE Cross-References folgen der **EBF Processing Pipeline** - einer 6-stufigen Verarbeitungskette von Utility zur Intervention:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STAGE 1: UTILITY DEFINITION (COREs 1-5)                                    │
│  ═══════════════════════════════════════                                    │
│                                                                             │
│     WHO (L)  ×  WHAT (d)  ×  HOW (γ)  ×  WHEN (Ψ)  →  U_pot                │
│       ↓           ↓           ↓           ↓                                 │
│    Levels    Dimensions  Complementarity  Context                           │
│                                                                             │
│     WHERE (Θ) provides calibration for all Stage 1 parameters               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGE 2: AWARENESS FILTER (CORE 6: AU)                                     │
│  ══════════════════════════════════════                                     │
│                                                                             │
│     U_eff = A(·) × U_pot                                                   │
│             ↑                                                               │
│     A depends on: WHAT (which d salient), WHEN (Ψ modulates A)              │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGE 3: ACTION THRESHOLD (CORE 7: AV)                                     │
│  ══════════════════════════════════════                                     │
│                                                                             │
│     Action ⟺ WAX(U_eff, φ, Ψ) ≥ θ(Ψ)                                       │
│                    ↑                                                        │
│     WAX depends on: AU (awareness → willingness), HOW (γ), WHEN (Ψ)         │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGE 4: BEHAVIORAL JOURNEY (CORE 8: AW)                                   │
│  ═════════════════════════════════════════                                  │
│                                                                             │
│     dS/dt = (1/τ) · [S*(A, WAX, Ψ) - S(t)]                                 │
│                        ↑    ↑                                               │
│     Phase depends on: AU (awareness), AV (willingness triggers transition)  │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGE 5: DECISION HIERARCHY (CORE 9: HI)                                   │
│  ═════════════════════════════════════════                                  │
│                                                                             │
│     N_L2 = α · γ_avg × n × (1-m) / log(n)                                  │
│                  ↑                                                          │
│     Hierarchy EMERGES from HOW (γ > 0 creates stratification)               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STAGE 6: INTERVENTION (CORE 10: IE)                                        │
│  ════════════════════════════════════                                       │
│                                                                             │
│     I⃗ ∈ [0,1]^9  with emergence modes E-Full/E-Partial/E-None              │
│     ↑                                                                       │
│     IE INTEGRATES all 10C → intervention vectors emerge (continuous space)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Warum diese Dependency-Struktur?

| Verbindung | Theoretische Begründung |
|------------|------------------------|
| **WHO ↔ WHAT** | Levels definieren welche Dimensionen relevant sind (bidirektional) |
| **WHO ↔ HOW** | Cross-Level Komplementarität γ^L (bidirektional) |
| **HOW ↔ WHEN** | Context Ψ moduliert γ; γ bestimmt Ψ-Sensitivität (bidirektional) |
| **AU → AV** | Awareness ist Input für Willingness (unidirektional) |
| **AV ↔ AW** | Willingness triggert Phase-Transitions; Phase beeinflusst Willingness |
| **HOW → HI** | γ > 0 erzeugt Hierarchy (Theorem T1: N_L2 = f(γ)) |
| **HI ↔ IE** | Hierarchy informiert Intervention; Intervention verändert Hierarchy |
| **IE ← alle 10C** | EIT ist Integration Point - benötigt alle Inputs |

### Die Bidirektionalitäts-Regel

```
Bidirektional (↔) genau dann wenn:
  1. Konzept A definiert Parameter für B  UND
  2. Konzept B liefert Feedback das A verändert

Beispiel: READY ↔ STAGE
  - AV → AW: WAX ≥ θ triggert Phase-Transition (forward)
  - AW → AV: Phase φ verändert θ(φ) Schwelle (feedback)
```

---

## Cross-Reference Matrix (Verifiziert 2026-01-20)

> **Quelle:** Direkte Analyse der LaTeX-Dateien in `/appendices/`

### AAA (CORE-WHO) — WHO_aggregation_levels.tex
**Referenziert:**
- WAT (CORE-WHAT): Dimensionen $d$ auf jeder Ebene $L$
- HOW (CORE-HOW): Cross-Level $\gamma$ Interaktionen
- CTW (CORE-WHEN): Context bestimmt salient level
- EST (CORE-WHERE): Level-spezifische Parameter
- AWA (CORE-AWARE): Level-spezifische Awareness $A^L(\cdot)$
- REA (CORE-READY): Level-spezifische Willingness $WAX^L$
- FRM (LIT-FEHR-METHOD): Exclusion Principle
- GLS (Glossary)

**Dependencies:** None (foundational)

### C (CORE-WHAT) — WAT_fepsde_matrix.tex
**Referenziert:**
- WHO (CORE-WHO): Levels $L$ auf denen Dimensionen operieren
- HOW (CORE-HOW): $\gamma_{dd'}$ Dimension-Komplementarität
- CTW (CORE-WHEN): $\Psi$ moduliert Dimension-Gewichte
- EST (CORE-WHERE): Dimension-spezifische Parameter
- FRM (LIT-FEHR-METHOD): Exclusion Principle
- GLS (Glossary)

**Dependencies:** WHO

### B (CORE-HOW) — HOW_complementarity_levels.tex
**Referenziert:**
- WHO (CORE-WHO): Cross-Level Interaktionen
- WAT (CORE-WHAT): Dimension-Interaktionen
- CTW (CORE-WHEN): $\Psi$, 8Ψ Dimensionen, $\gamma(\Psi)$
- EST (CORE-WHERE): Calibration
- **HIE (CORE-HIERARCHY):** $\gamma → N_{L2}$ Emergence
- **NC (FORMAL-NC):** $\gamma > 0 \Rightarrow$ Non-Concave, K vs Q
- FRM (LIT-FEHR-METHOD): Exclusion Principle
- GLS (Glossary)

**Dependencies:** WHO, WAT, CTW

### V (CORE-WHEN) — WEN_psi_dimensions.tex
**Referenziert:**
- WHO (CORE-WHO): Level Salience $\alpha^L(\Psi)$
- HOW (CORE-HOW): $\Lambda$-Matrix, $\delta$-Tensor
- EST (CORE-WHERE): $\delta$-Koeffizienten Calibration
- GLS (Glossary)

**Dependencies:** HOW, WAT, EST

### BBB (CORE-WHERE) — EST_estimation_methodology.tex
**Referenziert:**
- HOW (CORE-HOW): $\Gamma$, $\Lambda$, $\delta$ Parameter
- WAT (CORE-WHAT): Base Weights $w_d$, Reference Points $r_d$
- LLM (METHOD-LLMMC): LLM Monte Carlo Schätzungen
- OPS (METHOD-OPS): Empirische Operationalisierung
- GLS (Glossary)

**Dependencies:** HOW, LLM, OPS

### AU (CORE-AWARE) — AWA_bcm_axiom_formalization.tex
**Referenziert:**
- WAT (CORE-WHAT): Dimension-spezifische Salienz
- CTW (CORE-WHEN): Kontext-modulierte Awareness $A(\Psi)$
- EST (CORE-WHERE): Calibration
- GLS (Glossary)

**Dependencies:** WAT, CTW, EST
**Feeds into:** REA (CORE-READY) ✅ *Fixed 2026-01-20*

### AV (CORE-READY) — REA_willingness_formalization.tex
**Referenziert:**
- AWA (CORE-AWARE): Awareness als Input für WAX
- WAT (CORE-WHAT): Dimension-specific willingness ✅ *Added*
- HOW (CORE-HOW): Complementarity
- CTW (CORE-WHEN): Kontext $\Psi$
- EST (CORE-WHERE): Threshold calibration ✅ *Added*

**Dependencies:** AWA, WAT, HOW, CTW, EST
**Feeds into:** STA (CORE-STAGE) ✅ *Fixed 2026-01-20*

### AW (CORE-STAGE) — STA_behavioral_change_journey.tex
**Referenziert:**
- AWA (CORE-AWARE): Awareness in jeder Phase
- REA (CORE-READY): WAX triggert Phase-Transitions
- CTW (CORE-WHEN): Context
- EST (CORE-WHERE): Parameter
- IE (CORE-EIT): Phase-Type Affinity $\alpha_{BCJ}$ ✅ *Added*
- HHH (METHOD-TOOLKIT): BCJ-specific interventions ✅ *Added*
- FRM (LIT-FEHR-METHOD): Exclusion Principle

**Dependencies:** AWA, REA, CTW

### HI (CORE-HIERARCHY) — HIE_decision_hierarchy.tex
**Referenziert (VOLLSTÄNDIG - alle 10C):**
- AAA (CORE-WHO): Level-Struktur $L_1-L_4$
- WAT (CORE-WHAT): FEPSDE für Strategic Coherence
- HOW (CORE-HOW): $\gamma → N_{L2}$ Emergence (Axiom A1)
- CTW (CORE-WHEN): Modularity Affordance $m$
- EST (CORE-WHERE): Parameter für Hierarchy
- AWA (CORE-AWARE): L2 muss bewusst koordiniert werden
- REA (CORE-READY): Willingness für L2 Decisions
- STA (CORE-STAGE): L2 Complexity by Phase
- FRM (LIT-FEHR-METHOD): $\gamma = 0$ Null Hypothesis

**Dependencies:** HOW, WAT, CTW, WHO, EST

### IE (CORE-EIT) — IE_CORE-EIT.tex
**Referenziert (VOLLSTÄNDIG - alle 10C + Extensions):**
- **Alle 10C COREs:** AAA, C, B, V, BBB, AU, AV, AW, HI
- NC (FORMAL-NC): K vs Q für Emergence
- HHH (METHOD-TOOLKIT): Operational Implementation
- EEE (METHOD-DESIGN): Model Design Workflow

**Dependencies:** Alle 10C COREs

### 10C CORE Interdependenz-Matrix (Verifiziert & Korrigiert 2026-01-20)

```
        AAA   C    B    V   BBB   AU   AV   AW   HI   IE
AAA      -    ↔    ↔    →    ·    →    →    ·    ←    ←
C        ↔    -    ↔    →    ·    ←    ←    ·    ←    ←
B        ↔    ↔    -    ↔    ←    ·    ·    ·    ↔    ←
V        ←    ←    ↔    -    ·    ←    ←    ←    ←    ←
BBB      ·    →    →    ·    -    ·    ←    ·    ←    ←
AU       ←    →    ·    →    →    -    →    ←    ←    ←
AV       ←    ←    →    →    →    ↔    -    →    ←    ←
AW       ·    ·    ·    →    →    →    ↔    -    ←    →
HI       →    →    ↔    →    →    →    →    →    -    ↔
IE       →    →    →    →    →    →    →    ←    ↔    -

Legende:
  ↔ = bidirektional dokumentiert
  → = referenziert (outgoing)
  ← = wird referenziert (incoming)
  · = keine direkte Verbindung
```

**Alle Lücken behoben (2026-01-20):**
- ✅ AU → AV: "Feeds into" Link hinzugefügt
- ✅ AV → STA: "Feeds into" Link hinzugefügt
- ✅ AW → IE: Phase-Type Affinity $\alpha_{BCJ}$ referenziert
- ✅ AV deps: WAT, EST hinzugefügt

---

## Cross-Referenzierungsregeln

Diese Regeln definieren, wann bidirektionale vs. unidirektionale Verlinkung zwischen Dokumenten erforderlich ist.

### Regel 1: Bidirektionale Verlinkung (REQUIRED)

| Verbindung | Beispiel | Begründung |
|------------|----------|------------|
| **CORE ↔ CORE** | AAA ↔ C, B ↔ V | Kernkonzepte sind interdependent |
| **Chapter ↔ Appendix** | Ch.10 ↔ C | Navigation in beide Richtungen |
| **Gleiche Hierarchie** | AH ↔ AI (beide CONTEXT) | Gleichwertige Konzepte |

**Implementation in LaTeX:**
```latex
% In Appendix UNMAPPED_WHO:
\textbf{Cross-References:}
\begin{itemize}
    \item Appendix UNMAPPED_WAT (CORE-WHAT): Dimensionen pro Ebene
    \item Appendix UNMAPPED_HOW (CORE-HOW): Cross-Level Interaktionen
\end{itemize}

% In Appendix UNMAPPED_WAT (entsprechend):
\textbf{Cross-References:}
\begin{itemize}
    \item Appendix UNMAPPED_WHO (CORE-WHO): Level-spezifische Dimensionen
\end{itemize}
```

### Regel 2: Unidirektionale Verlinkung (OK)

| Verbindung | Richtung | Begründung |
|------------|----------|------------|
| **CORE → DOMAIN** | AAA → AJ | Hierarchisch: CORE definiert, DOMAIN wendet an |
| **DOMAIN → CORE** | AJ → C | DOMAIN referenziert Quelle, nicht umgekehrt |
| **ANY → LIT** | C → U | Literatur-Appendices werden nur zitiert |
| **ANY → G (Glossary)** | Alle → G | Glossar ist One-to-Many Referenz |
| **ANY → F (Examples)** | Alle → F | Beispiele werden referenziert, nicht umgekehrt |

**Hierarchie-Prinzip:**
```
CORE (definiert)
  ↓
DOMAIN/METHOD (wendet an)
  ↓
PREDICT/LIT (dokumentiert)
  ↓
REF (unterstützt)
```

### Regel 3: Chapter Linkage Box (REQUIRED in jedem Appendix)

Jedes Appendix MUSS eine Chapter Linkage Box enthalten:

```latex
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!50!black, title=Chapter Linkage]
\textbf{Primary Chapter:} Ch. X (Title)
\begin{itemize}[nosep]
    \item Ch. X.1: Specific section
    \item Ch. X.2: Another section
\end{itemize}
\textbf{Secondary:} Ch. Y, Ch. Z
\end{tcolorbox}
```

### Regel 4: Cross-Reference Map (REQUIRED für CORE/DOMAIN)

CORE und DOMAIN Appendices MÜSSEN eine Cross-Reference Map haben:

```latex
\begin{tcolorbox}[colback=purple!5!white, colframe=purple!50!black, title=Cross-Reference Map]
\textbf{Dieses Appendix referenziert:}
\begin{itemize}[nosep]
    \item Appendix UNMAPPED_FND: Grund
    \item Appendix UNMAPPED_CIA: Grund
\end{itemize}
\textbf{Referenziert von:}
\begin{itemize}[nosep]
    \item Appendix HAI1: Kontext
\end{itemize}
\end{tcolorbox}
```

### Regel 5: Wann NICHT verlinken

- **Keine zirkulären Abhängigkeiten** zwischen mehr als 3 Appendices
- **Keine Trivial-Links** (z.B. jedes Appendix zu Glossary einzeln auflisten)
- **Keine spekulativen Links** zu geplanten aber nicht existierenden Appendices

### Entscheidungsbaum

```
Neuer Link von A → B?
│
├─ Ist B ein CORE Appendix?
│  ├─ Ja: Ist A auch CORE? → Bidirektional
│  └─ Nein: A verlinkt B, B muss nicht zurück
│
├─ Ist B ein LIT/REF Appendix?
│  └─ Unidirektional (A → B nur)
│
├─ Sind A und B gleiche Kategorie?
│  └─ Bidirektional wenn inhaltlich verwandt
│
└─ Hierarchisch unterschiedlich?
   └─ Höhere Ebene wird nicht zurück verlinkt
```

### Checkliste für neue Appendices

- [ ] Chapter Linkage Box vorhanden
- [ ] Primary Chapter korrekt identifiziert
- [ ] Cross-Reference Map (wenn CORE/DOMAIN)
- [ ] Bidirektionale Links zu CORE Appendices geprüft
- [ ] Keine zirkulären Abhängigkeiten >3
- [ ] In `00_appendix_index.tex` eingetragen
- [ ] In dieser Mapping-Datei eingetragen

---

## Cross-Reference Netzwerke für Schlüssel-Appendices

Die folgenden Diagramme zeigen die vollständigen Vernetzungen der wichtigsten Appendices.

### IE (CORE-EIT): Emergent Intervention Theory

```
                            ┌─────────────────────────────────────────┐
                            │  IE (CORE-EIT) - 10C Emergence Theory    │
                            │  v2.6 | Interventionsbaukasten          │
                            └─────────────────────────────────────────┘
                                              │
        ┌──────────────────┬─────────────────┴──────────────────┬─────────────────┐
        │                  │                                    │                 │
   ABHÄNGIGKEITEN    THEORY INPUTS                        OUTPUTS           DEPENDENTS
   (10C COREs)        (Foundations)                    (Emergiert)          (Verwendet IE)
        │                  │                                    │                 │
        ▼                  ▼                                    ▼                 ▼
┌───────────────┐  ┌───────────────┐                   ┌───────────────┐  ┌───────────────┐
│ AAA (WHO)     │  │ NC (FORMAL-NC)│                   │ φ (STAGE)     │  │ HHH (TOOLKIT) │
│  → L, C_k     │  │  → K vs Q     │                   │  Full Emerg.  │  │  Operations   │
│ C (WHAT)      │  │  → γ > 0 →    │                   │ N_L2 (HIER)   │  │ EEE (DESIGN)  │
│  → d, FEPSDE  │  │    peaks      │                   │  Semi-Emerg.  │  │  Workflow     │
│ B (HOW)       │  └───────────────┘                   │ C_k (Segment) │  │ Ch. 17-20     │
│  → γ, Γ       │                                      │  Semi-Emerg.  │  │  Intervention │
│ V (WHEN)      │  ┌───────────────┐                   │ Ψ_perc, Ψ_rel │  │  Design Block │
│  → Ψ_obj      │  │ MIL (Roberts) │                   │  Semi-Emerg.  │  └───────────────┘
│ BBB (WHERE)   │  │  → Org. Fit   │                   └───────────────┘
│  → Θ, D_suff  │  └───────────────┘                          │
│ AU (AWARE)    │                                             │
│  → A_0        │         ┌───────────────────────────────────┘
│ AV (READY)    │         ▼
│  → W_0, WAX   │  ┌───────────────────────────────────────────┐
│ AW (STAGE)    │  │  P_eff = σ(WEC × α_BCJ × β_BCS)          │
│  → BCJ phases │  │  ↑ emergent α_BCJ from φ (STAGE)         │
│ HI (HIER)     │  │  ↑ emergent β_BCS from C_k (Segment)     │
│  → L0-L3      │  │  Connection to Ch.16 Output               │
└───────────────┘  └───────────────────────────────────────────┘

10C Emergence Classification (IE Core):
  Fundamental (4):  L, d, Ψ_obj, Θ
  Semi-Emerg. (6):  A_0, Ψ_perc, Ψ_rel, W_0, γ, N_L2, C_k
  Full Emerg. (1):  φ (STAGE)
```

### B (CORE-HOW): Complementarity Structure

```
                            ┌─────────────────────────────────────────┐
                            │  B (CORE-HOW) - Complementarity γ       │
                            │  v2.1 | 163 Interaction Parameters      │
                            └─────────────────────────────────────────┘
                                              │
        ┌──────────────────┬─────────────────┴──────────────────┬─────────────────┐
        │                  │                                    │                 │
   ABHÄNGIGKEITEN    MATRIX OUTPUTS                      THEORY LINKS        DEPENDENTS
   (COREs)           (Γ, Λ, δ)                          (Formalization)     (Verwendet B)
        │                  │                                    │                 │
        ▼                  ▼                                    ▼                 ▼
┌───────────────┐  ┌───────────────┐                   ┌───────────────┐  ┌───────────────┐
│ AAA (WHO)     │  │ Γ-Matrix      │                   │ NC (FORMAL-NC)│  │ IE (CORE-EIT) │
│  → Level L    │  │  15 params    │                   │  γ > 0 →      │  │  → γ for      │
│  → Cross-lvl  │  │  Utility×Util │                   │  Non-Concave  │  │    emergence  │
│ C (WHAT)      │  │               │                   │  Multiple     │  │ HI (HIER)     │
│  → FEPSDE d   │  │ Λ-Matrix      │                   │  Equilibria   │  │  → N_L2 =     │
│  → γ_dd'      │  │  28 params    │                   │  K vs Q       │  │    f(γ)       │
│ V (WHEN)      │  │  Context×Ctx  │                   │               │  │ HHH (TOOLKIT) │
│  → Ψ, 8Ψ     │  │               │                   │ VII (GTC)     │  │  → F10 γ_ij   │
│  → γ(Ψ)      │  │ δ-Tensor      │                   │  General      │  │ BBB (WHERE)   │
└───────────────┘  │  120 params   │                   │  Theory       │  │  → Calibration│
                   │  Ctx×Util     │                   │               │  │ AN (LLMMC)    │
                   └───────────────┘                   │ X (FND)       │  │  → Estimation │
                          │                            │  Foundations  │  │ AU (Axioms)   │
                          ▼                            │               │  │  → B-axioms   │
                   ┌───────────────┐                   │ XI (MDL)      │  └───────────────┘
                   │ Milgrom-Roberts│                  │  Models       │
                   │  Supermodular │                   └───────────────┘
                   │  Games (MIL)  │                          │
                   └───────────────┘                          ▼
                          │                            ┌───────────────┐
                          └───────────────────────────→│ EQU, MEQ      │
                                                       │  Equilibria   │
                                                       │  Multi-Eq     │
                                                       └───────────────┘

Key Insight (Ch.15): "HIERARCHY emerges from γ"
  N_L2 = α · γ_avg × n × (1-m) / log(n)
```

### HHH (METHOD-TOOLKIT): Intervention Design Operations

```
                            ┌─────────────────────────────────────────┐
                            │  HHH (METHOD-TOOLKIT) - Operations      │
                            │  v2.2 | 20-Field Schema, A1-A8          │
                            └─────────────────────────────────────────┘
                                              │
        ┌──────────────────┬─────────────────┴──────────────────┬─────────────────┐
        │                  │                                    │                 │
   THEORY SOURCE     10C DEPENDENCIES                      TOOLS               DEPENDENTS
   (IE Foundation)   (All COREs)                       (Operational)        (Verwendet HHH)
        │                  │                                    │                 │
        ▼                  ▼                                    ▼                 ▼
┌───────────────┐  ┌───────────────┐                   ┌───────────────┐  ┌───────────────┐
│ IE (CORE-EIT) │  │ AAA → L, HHH-T3│                  │ 20-Field      │  │ THL1 (EVAL)   │
│  Axioms       │  │ C → d, HHH-T4 │                   │  Schema       │  │  Evaluation   │
│  EIT-1 to 5   │  │ B → γ, F10   │                   │  F1-F20       │  │ DSN (DESIGN)  │
│  Emergence    │  │ V → Ψ        │                   │               │  │  Model Design │
│  Modes        │  │ BBB → Θ      │                   │ Intervention  │  │ CAL1 (LLMMC)  │
│  D_suff       │  │ AU → A, HHH-T6│                  │  Vectors      │  │  Calibration  │
└───────────────┘  │ AV → W, HHH-T1│                  │  (Emergent)   │  │               │
        │          │ AW → φ, HHH-T5│                  │               │  │ Ch. 17-20     │
        ▼          │ HI → Scope    │                   │ LLMMC         │  │  Intervention │
┌───────────────┐  │              │                   │  Protocols    │  │  Design Block │
│ FRM (FEHR)    │  └───────────────┘                   │               │  └───────────────┘
│  Exclusion    │         │                            │ Light/Hybrid/ │
│  Principle    │         ▼                            │  Profound     │
│  γ=0 Null     │  ┌───────────────┐                   │  Depths       │
└───────────────┘  │ PAP (Equilib.)│                  └───────────────┘
                   │ PAP1 (Segment)│                          │
                   │ LET (Level)   │                          ▼
                   └───────────────┘                   ┌───────────────┐
                                                       │ 10C Delta      │
                                                       │  Measurement  │
                                                       │  (Ch.20 Sec7.4)│
                                                       └───────────────┘

Separation of Concerns:
  IE (CORE-EIT)  = THEORY (Axioms, Emergence, Data Requirements)
  HHH (TOOLKIT)  = OPERATIONS (20-Field, Clusters, LLMMC)
```

### NC (FORMAL-NC): Non-Concavity and Fit (bereits dokumentiert)

```
Chapter 7 ←→ NC (Primary)
     ↓
┌────┴────┬─────────┬─────────┬─────────┐
↓         ↓         ↓         ↓         ↓
B       MIL       VII        X        XI
HOW    Roberts    GTC       FND      MDL
     ↓         ↓         ↓
   HIE       EQU       MEQ
HIERARCHY  Equilib.  Multi-Eq
     ↓
    IE
   EIT
```

---

*Generiert: 2026-01-20 | Quelle: appendices/00_appendix_index.tex*
