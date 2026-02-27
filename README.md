# Evidence-Based Framework for Economic and Social Behavior (EBF)

## Das 10C CORE Framework für ökonomische Rationalität

> **Version 54** | Januar 20, 2026 | FehrAdvice & Partners AG
>
> **Major Updates:** Evidence Integration Pipeline (EIP), Intervention Design Workflow, UNTCM Model, 10C→10C Migration, Portfolio Archetypes

---

## Schnell Einstieg

**[EBF Introduction](docs/EBF-INTRODUCTION.md)** — Was ist das EBF? Was kannst du damit machen? Warum?

*Komplett neu? Starte hier!* (10 min read)

---

## Forschungs-Fundament

Das EBF basiert auf **50+ Jahren verhaltensökonomischer Forschung** mit vollständiger wissenschaftlicher Dokumentation:

| Quelle | Umfang | Status |
|--------|--------|--------|
| **Paper-Sources Registry** | 1,922 wissenschaftliche Arbeiten | Fully Indexed |
| **BibTeX Bibliography** | 2,584 Einträge | Konsistent & aktualisiert |
| **Zeitraum** | 1972-2026 | Kontinuierlich aktualisiert |
| **Kernautoren** | Kahneman, Thaler, Fehr, Sunstein, Ariely, +50 more | 10C-indiziert |
| **Indexierung** | 10C CORE + Evidence Integration Pipeline | Systematisch klassifiziert |

**Besonderheit:** Alle 1,922 Papers sind systematisch nach den **10C Dimensionen** indiziert, mit vollständiger Evidence Integration Pipeline (EIP) für PRO + CONTRA Evidenz.

---

## Die zentrale Frage

> **Warum handeln Menschen oft anders als erwartet?**

Das EBF beantwortet diese Frage durch **10 fundamentale Fragen** — das **10C CORE Framework**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DIE 10C CORE ARCHITEKTUR                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   META-STRUKTUR: HIERARCHY                                              │
│   ├─ Wie stratifizieren sich Entscheidungen über Ebenen? → L0-L3      │
│   └─ (Unterlage für alle anderen Dimensionen)                          │
│                              ↓                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │  STUFE 1: UTILITY DEFINITION                                    │   │
│   │                                                                 │   │
│   │    WHO    →  Wer hat Utility?           →  L (Ebenen)          │   │
│   │    WHAT   →  Was ist Utility?           →  d (Dimensionen)     │   │
│   │    HOW    →  Wie interagieren sie?      →  γ (Komplementarität)│   │
│   │    WHEN   →  Wann zählt Kontext?        →  Ψ (8 Dimensionen)   │   │
│   │    WHERE  →  Woher die Zahlen?          →  Θ (Parameter)       │   │
│   │                                                                 │   │
│   │    U_pot = f(L, d, γ, Ψ, Θ)                                    │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │  STUFE 2: AWARENESS FILTER                                      │   │
│   │                                                                 │   │
│   │    AWARE  →  Wie bewusst bin ich mir?   →  A(·) (Salienz)      │   │
│   │                                                                 │   │
│   │    U_eff = A(·) × U_pot                                        │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │  STUFE 3: ACTION THRESHOLD                                      │   │
│   │                                                                 │   │
│   │    READY  →  Wie handlungsbereit?       →  WAX, θ (Schwelle)   │   │
│   │                                                                 │   │
│   │    Action ⟺ WAX ≥ θ                                            │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                              ↓                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │  STUFE 4: BEHAVIORAL CHANGE JOURNEY                             │   │
│   │                                                                 │   │
│   │    STAGE  →  Wo in der Veränderung?     →  S(t), dS/dt         │   │
│   │                                                                 │   │
│   │    Journey = f(Awareness, Willingness, Context, Time)          │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Die 9 fundamentalen Fragen (10C CORE Framework)

| # | CORE | Frage | Antwort | Symbol | Appendix |
|---|------|-------|---------|--------|----------|
| 1 | **WHO** | Wer hat Utility? | 9-Ebenen-Hierarchie | $L$ | [AAA](appendices/AAA_aggregation_levels.tex) |
| 2 | **WHAT** | Was ist Utility? | 144 FEPSDE-Komponenten | $d$ | [C](appendices/C_fepsde_matrix.tex) |
| 3 | **HOW** | Wie interagieren? | Komplementarität | $γ$ | [B](appendices/B_complementarity_levels.tex) |
| 4 | **WHEN** | Wann zählt Kontext? | 8 Ψ-Dimensionen | $Ψ$ | [V](appendices/V_psi_dimensions.tex) |
| 5 | **WHERE** | Woher die Zahlen? | Kalibrierung | $Θ$ | [BBB](appendices/BBB_parameter_estimation.tex) |
| 6 | **AWARE** | Wie bewusst bin ich mir? | Salienz-Filter | $A(·)$ | [AU](appendices/AU_bcm_axiom_formalization.tex) |
| 7 | **READY** | Wie handlungsbereit? | Handlungsschwelle | $WAX, θ$ | [AV](appendices/AV_willingness_formalization.tex) |
| 8 | **STAGE** | Wo in der Veränderung? | Behavioral Change Journey | $S(t), φ ∈ \{1,...,5\}$ | [AW](appendices/AW_behavioral_change_journey.tex) |
| 9 | **HIERARCHY** | Wie stratifizieren Entscheidungen? | Mehrebenen-Struktur | $L_0, L_1, L_2, L_3$ | [HI](appendices/HI_hierarchy_levels.tex) |

---

## Das Kernargument

> **Warum versagen LLMs bei Verhaltensvorhersagen?**
>
> Sie wurden auf *Texten über* Experimente trainiert — nicht auf *Verhaltensdaten*.

| Aspekt | LLM / Digital Twin | EBF |
|--------|-------------------|---------|
| **Datenquelle** | Textkorpora | Experimentelle Verhaltensdaten |
| **Wissen** | "Der Endowment-Effekt ist..." | $E(Ψ) = 0.31 + 0.24·Ψ_C$ |
| **Heterogenität** | Weggemittelt | Explizit modelliert |
| **Replikation** | ~50% | >85% (by construction) |
| **Lernen** | Retraining nötig | Δ triggert Revision |

**Details:** [Kapitel 4x](chapters/ch04x_README.md)

---

## Dokumentstruktur

### Hauptdokument: 22 Kapitel (davon 8 Extended: Intervention Design)

| Teil | Kapitel | Thema | CORE |
|------|---------|-------|------|
| **I** | [1-4](chapters/) | Grundlagen | — |
| **II** | [5-9](chapters/) | Kerntheorie | B, V |
| **III** | [10](chapters/ch10_README.md) | Nutzenarchitektur | C, AAA |
| **IV** | [11](chapters/ch11_README.md) | Awareness | **AU** |
| **V** | [12](chapters/ch12_README.md) | Willingness | **AV** |
| **VI** | [13](chapters/) | **BCJ: Stage-Dependent Dynamics** | AW |
| **VII** | [14](chapters/) | **BCJ: Behavioral Change Segments** | AW |
| **VIII** | [15](chapters/) | **WEC-Synthesis** | AW |
| **IX** | [16](chapters/) | **Probability & Effectiveness** | HHH |
| **X** | [17-20](chapters/) | **Intervention Toolkit** | TKT, WAT |
| **XI** | [21-22](chapters/) | Limitations & Conclusion | — |

### Appendices: 165 systematische Ergänzungen (167 Dateien)

| Kategorie | Anzahl | Codes | Beschreibung |
|-----------|--------|-------|--------------|
| **CORE** | 8 | AAA, B, C, V, BBB, AU, AV, AW | Die 8 fundamentalen Fragen |
| **FORMAL** | 10+ | A, D, PBB, UN, FND, ... | Mathematik, Wahrscheinlichkeiten, UNTCM |
| **DOMAIN** | 40+ | AA-AK, W-Z | Feldanwendungen, Portfolio Archetypes |
| **CONTEXT** | 10+ | AH, AI, V, ... | Zeit/Raum/Kontext, NTM |
| **METHOD** | 15+ | AL, AN, E, R, HHH, TKT, ... | Methodik, Intervention Toolkit |
| **PREDICT** | 20+ | AO-AT, S, ... | Testbare Vorhersagen, 10C Delta |
| **LIT** | 40+ | I-Q, U, LIT-R/-M/-O | Literatur-Integration (EIP) |
| **REF** | 15+ | F, G, H, T, WAT | Nachschlagewerke, FEPSDE Matrix |

**Details:** [appendices/README.md](appendices/README.md)

---

## Die 8 Ψ-Dimensionen

Der Kontext modulliert alles:

| Dim | Symbol | Was es misst |
|-----|--------|--------------|
| **Institutional** | Ψ_I | Regeln, Durchsetzung, Eigentumsrechte |
| **Social** | Ψ_S | Vertrauen, Normen, Sozialkapital |
| **Cognitive** | Ψ_C | Informationsverarbeitung, Numeracy |
| **Informational** | Ψ_K | Transparenz, Signalqualität |
| **Economic** | Ψ_E | Entwicklung, Markttiefe |
| **Temporal** | Ψ_T | Zeithorizonte, Stabilität |
| **Market Scope** | Ψ_M | Geografische Reichweite |
| **Factor Flexibility** | Ψ_F | Anpassungskapazität |

---

## Die Lernarchitektur

EBF ist selbstverbessernd:

```
C*(Ψ) generiert Vorhersagen
       ↓
Δ = C - C* misst Abweichung
       ↓
Diagnostik klassifiziert Δ (Appendix AK)
       ↓
Update-Regeln revidieren Modell (Appendix AL)
       ↓
Iteration → besseres C*
```

---

## Repository-Struktur

```
complementarity-context-framework/
│
├── README.md                    ← Du bist hier
│
├── chapters/                    ← 19 Kapitel + READMEs
│   ├── README.md                ← Kapitel-Navigation
│   └── *.tex                    ← LaTeX-Quellen
│
├── appendices/                  ← 165 Appendices (167 Dateien)
│   ├── README.md                ← Appendix-Navigation
│   └── *.tex                    ← LaTeX-Quellen
│
├── docs/                        ← Dokumentation
├── quality/                     ← TERAN Quality Framework
├── data/                        ← Empirische Daten
├── scripts/                     ← LLM Monte Carlo
├── bibliography/                ← Literatur
└── latex/                       ← Kompilierung
```

---

## Statistik (Februar 2026)

| Metrik | Wert |
|--------|------|
| **Kapitel** | 19 + 4 Extended |
| **Appendices** | 227 (A-QQQ++) |
| **Axiome** | 250+ (AWX + WAX + EIP) |
| **Seiten** | ~900+ |
| **Referenzen** | 2,453 BibTeX Einträge |
| **Referenzen** | 2,453 BibTeX Einträge |
| **Referenzen** | 2,453 BibTeX Einträge |
| **Referenzen** | 2,453 BibTeX Einträge |
| **Papers (10C-indexed)** | 1,922 |
| **Skills/Commands** | 15+ (incl. EIP, Intervention, Customer Strategy) |

---

## Schnellstart

### Für Theoretiker
1. Start: [Chapter 1](chapters/ch01_README.md) — Einführung
2. Kern: [Chapter 5](chapters/ch05_README.md) — Komplementarität (CORE-HOW)
3. Kontext: [Chapter 9](chapters/ch09_README.md) — Ψ-Dimensionen (CORE-WHEN)

### Für Empiriker
1. Start: [Chapter 4x](chapters/ch04x_README.md) — Kalibrierung (CORE-WHERE)
2. Daten: [Appendix BBB](appendices/BBB_estimation_methodology.tex)
3. Methode: [Appendix AN](appendices/AN_llm_monte_carlo.tex) — LLM Monte Carlo

### Für Praktiker
1. Start: [Chapter 11](chapters/ch11_README.md) — Awareness (CORE-AWARE)
2. Action: [Chapter 12](chapters/ch12_README.md) — Willingness (CORE-READY)
3. Design: [Chapter 17](chapters/ch17_README.md) — Intervention Design (20-Field Schema)

---

## Qualitätssicherung

EBF verwendet das **TERAN-Framework** (adaptiert von Belcher et al. 2016):

| Dimension | Gewicht | Prüft |
|-----------|---------|-------|
| **T**heory | 25% | Literatur, Axiome, Beweise |
| **E**vidence | 30% | Daten, Kalibrierung, Validierung |
| **R**igor | 15% | Notation, Definitionen |
| **A**pplicability | 15% | Beispiele, Skalierbarkeit |
| **N**eutralität | 15% | Epistemic Tags, Limitations |

### Epistemic Status Tags

| Tag | Bedeutung |
|-----|-----------|
| `[EMP]` | Empirisch validiert |
| `[THR]` | Theoretisch abgeleitet |
| `[LLM]` | LLM-Monte-Carlo geschätzt |
| `[ILL]` | Illustrativ |
| `[HYP]` | Hypothetisch |

**Details:** [quality/README.md](quality/README.md)

---

## Quick Links

| Dokument | Link |
|----------|------|
| **Haupttext PDF** | [complementarity_context_main_v54.pdf](complementarity_context_main_v54.pdf) |
| **Appendices PDF** | [complementarity_context_appendices_v54.pdf](complementarity_context_appendices_v54.pdf) |
| **Kapitel-Index** | [chapters/README.md](chapters/README.md) |
| **Appendix-Index** | [appendices/README.md](appendices/README.md) |
| **Chapter-Appendix Mapping** | [docs/chapter_appendix_mapping.md](docs/chapter_appendix_mapping.md) |
| **Customer Strategy Skills** | [.claude/commands/README.md](.claude/commands/README.md) |

---

## Zitation

```bibtex
@article{fehr2026bcm,
  title   = {Complementarity and Context: A Unified Framework
             for Economic Rationality},
  author  = {Fehr, Gerhard},
  journal = {Working Paper},
  year    = {2026},
  note    = {EBF — 10C CORE Framework},
  url     = {https://github.com/FehrAdvice-Partners-AG/
             complementarity-context-framework}
}
```

---

## Lizenz

© 2026 FehrAdvice & Partners AG. Alle Rechte vorbehalten.

---

<div align="center">

**EBF — Das 10C CORE Framework**

*WHO · WHAT · HOW · WHEN · WHERE · AWARE · READY · STAGE*

</div>

---

*Letzte Aktualisierung: 2026-02-08*
