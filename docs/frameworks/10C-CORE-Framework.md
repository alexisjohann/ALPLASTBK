# Das 10C CORE Framework

> **SSOT:** `docs/frameworks/core-framework-definition.yaml`  
> **Upload-Tags:** canonical, 10c, core, framework, ssot  
> **Priorität:** HÖCHSTE — ersetzt alle bisherigen 10C-Einträge in der Knowledge Base

---

## Was ist das 10C Framework?

Das **10C Framework** ist die Struktur des Evidence-Based Framework (EBF). Es besteht aus genau **10 komplementären Dimensionen** (COREs), die gemeinsam menschliches Verhalten vollständig beschreiben.

**Wichtig:** Es sind genau 10 COREs — nicht 9, nicht 11. Der Name "10C" ist fix.

## Die 10 COREs im Überblick

| # | CORE | Code | Frage | Output | Kapitel |
|---|------|------|-------|--------|---------|
| 1 | **WHO** | AAA | Wer hat Utility? | Levels L (Individual → Society) | Ch. 2 |
| 2 | **WHAT** | C | Was ist Utility? | FEPSDE Dimensionen | Ch. 3 |
| 3 | **HOW** | B | Wie interagieren Dimensionen? | Komplementarität γ | Ch. 4 |
| 4 | **WHEN** | V | Wann zählt Kontext? | 8 Ψ-Dimensionen | Ch. 5 |
| 5 | **WHERE** | BBB | Woher die Zahlen? | Parameter Θ | Ch. 6 |
| 6 | **AWARE** | AU | Wie bewusst? | Awareness A(·) ∈ [0,1] | Ch. 11 |
| 7 | **READY** | AV | Handlungsbereit? | Willingness WAX ≥ θ | Ch. 12 |
| 8 | **STAGE** | AW | Wo in der Journey? | BCJ Phase S(t) | Ch. 13 |
| 9 | **HIERARCHY** | HI | Wie stratifizieren Entscheidungen? | Levels L0-L3 | Ch. 15 |
| 10 | **EIT** | IE | Wie emergieren Interventionen? | Vektor I⃗ ∈ [0,1]⁹ | Ch. 17 |

## Die EBF Processing Pipeline (6 Stages)

Die 10 COREs bilden eine sequenzielle Verarbeitungskette:

```
Stage 1: Potential Utility    (WHO + WHAT + HOW + WHEN)
  U^pot = Σ_L α^L(Ψ) · [Σ_d ω^L_d · U^L_d + Σ γ^L_dd' · U^L_d·U^L_d']

Stage 2: Effective Utility    (AWARE)
  U^eff(t*) = A(t*) × U^pot

Stage 3: Action Decision      (READY)
  Action ⟺ WAX(U^eff, φ, Ψ) ≥ θ(Ψ)

Stage 4: Change Journey       (STAGE)
  dS/dt = (1/τ) · [S*(A, WAX, Ψ) - S(t)]

Stage 5: Decision Hierarchy   (HIERARCHY)
  N_L2 = α · γ_avg × n × (1-m) / log(n)

Stage 6: Intervention         (EIT)
  I⃗ ∈ [0,1]⁹ mit E-modes (E-Full, E-Partial, E-None)
```

## Warum 10C und nicht weniger?

Jeder CORE beantwortet eine **eigene, nicht-reduzierbare Frage**:

| CORE | Irreduzibilität |
|------|-----------------|
| WHO | Definiert die Aggregationsebene — ohne WHO keine Zuordnung von Utility |
| WHAT | Definiert die Utility-Dimensionen — ohne WHAT keine Messung möglich |
| HOW | Definiert die Wechselwirkungen — ohne HOW keine Komplementaritäten |
| WHEN | Definiert den Kontext — ohne WHEN keine Situationsabhängigkeit |
| WHERE | Definiert die Datenquellen — ohne WHERE keine empirische Basis |
| AWARE | Filtert durch Bewusstsein — ohne AWARE keine Wahrnehmungsbarrieren |
| READY | Prüft die Handlungsbereitschaft — ohne READY kein Entscheidungsmoment |
| STAGE | Positioniert in der Journey — ohne STAGE keine Veränderungsdynamik |
| HIERARCHY | Ordnet Entscheidungsebenen — ohne HIERARCHY keine Stratifikation |
| EIT | Designt Interventionen — ohne EIT keine systematische Verhaltensänderung |

## 10C vs 9D Interventionsvektor

| Konzept | Definition | Count | Purpose |
|---------|------------|-------|---------|
| **10C** | Das theoretische Framework | 10 | Vollständige Beschreibung menschlichen Verhaltens |
| **9D** | Der Interventionsvektor I⃗ ∈ [0,1]⁹ | 9 | Targetiert COREs 1-9 |

**Warum 9D?** EIT (CORE 10) ist die *Methodologie* für Interventionen, nicht ein Target selbst.

---

*Letzte Aktualisierung: 2026-02-15*
