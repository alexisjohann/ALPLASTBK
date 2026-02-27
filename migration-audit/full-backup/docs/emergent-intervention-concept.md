# Emergent Intervention Concept (EIC)

## Das Problem: Warum T1-T8 falsch ist

### Die alte Denkweise (T1-T8)

```
FALSCH: "Wähle aus einem Katalog von 8 Interventionstypen"

T1 = Information        → Dem Kunden Information geben
T2 = Feedback           → Dem Kunden Feedback geben
T3 = Choice Architecture → Die Entscheidungsarchitektur ändern
T4 = Timing             → Den Zeitpunkt wählen
T5 = Identity           → Die Identität ansprechen
T6 = Social Norms       → Soziale Normen nutzen
T7 = Financial Incentives → Finanzielle Anreize setzen
T8 = Commitment         → Verpflichtungen eingehen lassen
```

**Problem:** Dies behandelt Interventionen als **diskrete Kategorien** aus einem festen Katalog. Aber:

1. **Künstliche Grenzen:** Was ist eine "Commitment"-Intervention mit finanziellen Konsequenzen? T8 oder T7?
2. **Versteckte Annahmen:** Warum genau 8 Typen? Warum nicht 5 oder 12?
3. **Statisch:** Keine neuen Kategorien können entdeckt werden
4. **Kombinatorik-Illusion:** "Wähle 3 aus 8" suggeriert $\binom{8}{3} = 56$ Optionen

---

## Die neue Denkweise: Emergenz aus kontinuierlichem Raum

### Die 10C Dimensionen sind die Primitive

```
DIE 10C CORE FRAGEN (die einzigen Primitive):

WHO (AAA)     → Wer hat Utility? (L1-L4)
WHAT (C)      → Was ist Utility? (FEPSDE)
HOW (B)       → Wie interagieren? (γ-Struktur)
WHEN (V)      → Wann zählt Kontext? (Ψ)
WHERE (BBB)   → Woher die Zahlen? (Θ-Quellen)
AWARE (AU)    → Wie bewusst? (A)
READY (AV)    → Handlungsbereit? (W)
STAGE (AW)    → Wo in der Journey? (φ)
HIERARCHY (HI)→ Welche Entscheidungsebene? (Scope)
```

### Interventionen existieren im kontinuierlichen Raum

**Der Interventionsraum:**

```math
I⃗ ∈ [0,1]^9
```

Jede Intervention ist ein **9-dimensionaler Vektor**:

```math
I⃗ = (I_WHO, I_WHAT, I_HOW, I_WHEN, I_WHERE, I_AWARE, I_READY, I_STAGE, I_HIER)
```

wobei jede Komponente $I_d \in [0,1]$ die **Intensität** auf dieser Dimension angibt.

---

## Die Intuition: Farben als Analogie

### Das Farbspektrum-Modell

```
RGB-FARBRAUM                    INTERVENTIONSRAUM
═══════════════                 ═══════════════════

Primitive:                      Primitive:
  R (Rot)                         10C Dimensionen
  G (Grün)                        (WHO, WHAT, HOW, ...)
  B (Blau)

Raum:                           Raum:
  [0,255]³                        [0,1]⁹

Punkte:                         Punkte:
  (255, 0, 0) = Rot               I⃗ = (0.8, 0.2, ...)
  (0, 255, 0) = Grün
  (0, 0, 255) = Blau

Emergente Cluster:              Emergente Cluster:
  "Orange" ≈ (255, 165, 0)        A1 (Awareness-dominant)
  "Lila" ≈ (128, 0, 128)          A6 (Social-dominant)
  "Türkis" ≈ (0, 255, 255)        A7 (Financial-dominant)

Wichtig:                        Wichtig:
  "Orange" ist KEIN Primitiv!     A1-A8 sind KEINE Primitive!
  Es emergiert aus RGB.           Sie emergieren aus 10C.
```

### Was bedeutet "emergieren"?

```
KEINE Auswahl aus Katalog:
╔════════════════════════════════════════════════════════════════╗
║  "Welche Farbe soll das Logo haben?"                           ║
║  ❌ FALSCH: "Wähle aus: Rot, Orange, Gelb, Grün, Blau, Lila"   ║
║  ✅ RICHTIG: "Bestimme RGB-Werte basierend auf Kontext"        ║
║             → Farbe EMERGIERT aus den Werten                   ║
╚════════════════════════════════════════════════════════════════╝

KEINE Auswahl aus Katalog:
╔════════════════════════════════════════════════════════════════╗
║  "Welche Intervention soll eingesetzt werden?"                 ║
║  ❌ FALSCH: "Wähle aus: T1, T2, T3, T4, T5, T6, T7, T8"        ║
║  ✅ RICHTIG: "Bestimme 10C-Intensitäten basierend auf Kontext" ║
║             → Intervention EMERGIERT aus den Werten            ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Die formale Struktur

### Axiom EIT-1: Der kontinuierliche Interventionsraum

```math
∀ Intervention I: I ∈ [0,1]^9
```

**Bedeutung:** Jede mögliche Intervention ist ein Punkt im 9-dimensionalen Einheitswürfel.

### Axiom EIT-2: Intervention als 10C-Transformation

```math
I(I⃗): S⃗₀ → S⃗₁ = S⃗₀ + ΔS⃗(I⃗)
```

**Bedeutung:** Eine Intervention transformiert den Status Quo Vektor $S⃗₀$ in einen neuen Zustand $S⃗₁$.

### Axiom EIT-3: Cluster-Emergenz (der Schlüssel!)

```math
A_k = {I⃗ ∈ [0,1]^9 : ∃d ∈ 10C, I_d > τ ∧ ∀d' ≠ d: I_{d'} < τ}
```

**Bedeutung:** Die "Typen" A1-A8 sind **hochdichte Regionen** im Interventionsraum, wo eine Dimension dominiert. Sie sind NICHT ontologische Primitive.

---

## Warum Cluster praktisch nützlich sind

### Die A1-A8 Archetypen (emergente Cluster)

| Cluster | Dominante Dimension | Typische Intensitäten | Praktisches Beispiel |
|---------|---------------------|----------------------|---------------------|
| **A1** | I_AWARE hoch | (0.1, 0.1, 0.1, 0.1, 0.1, **0.9**, 0.2, 0.1, 0.1) | Informationskampagne |
| **A2** | I_AWARE + I_READY | (0.1, 0.1, 0.1, 0.1, 0.1, **0.7**, **0.6**, 0.1, 0.1) | Feedback-System |
| **A3** | I_HOW hoch | (0.1, 0.1, **0.9**, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1) | Choice Architecture |
| **A4** | I_WHEN hoch | (0.1, 0.1, 0.2, **0.9**, 0.1, 0.2, 0.2, 0.1, 0.1) | Timing-Intervention |
| **A5** | I_WHO (self) hoch | (**0.8**, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1) | Identitäts-Priming |
| **A6** | I_WHO (others) hoch | (**0.7**, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1) | Soziale Normen |
| **A7** | I_WHAT hoch | (0.1, **0.9**, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1) | Finanzielle Anreize |
| **A8** | I_HOW + binding | (0.1, 0.1, **0.8**, 0.2, 0.1, 0.2, **0.7**, 0.1, 0.1) | Commitment Device |

**Wichtig:** Diese Cluster sind **Heuristiken** für die Kommunikation, nicht die wahre Ontologie!

---

## Die drei Emergence Modes

### Abhängig von Datenverfügbarkeit

```
Datenverfügbarkeit D_suff bestimmt den Modus:

┌─────────────────────────────────────────────────────────────────┐
│  D_suff > 0.7  →  E-FULL: Volle Optimierung in [0,1]⁹          │
│                   → Keine Cluster, nur kontinuierlicher Vektor  │
│                   → "Berechne optimale Intensitäten"            │
├─────────────────────────────────────────────────────────────────┤
│  0.4 ≤ D_suff ≤ 0.7  →  E-PARTIAL: Prototyp + Anpassung        │
│                   → Starte mit A_k Cluster                      │
│                   → Passe Intensitäten an                       │
│                   → "Starte mit A6, erhöhe I_AWARE auf 0.5"     │
├─────────────────────────────────────────────────────────────────┤
│  D_suff < 0.4  →  E-NONE: Vereinfachte Heuristik               │
│                   → Verwende A_k Cluster als Approximation      │
│                   → "Verwende A6 (Social Norms)"                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Der Paradigmenwechsel

```
TRADITIONELL (T1-T8)              MIT EIT (EMERGENT)
════════════════════              ═══════════════════

"Wähle aus Katalog"               "Verstehe Kontext → Vektor emergiert"

Taxonomie = INPUT                 Taxonomie = OUTPUT (oder Heuristik)

8 diskrete Optionen               Kontinuierlicher Raum [0,1]⁹

Kombinatorik: 2⁸ = 256            Optimierung: argmax

Statisch: Feste Kategorien        Dynamisch: Vektoren emergieren

"T6 + T7"                         I⃗ = (0.3, 0.7, 0.2, 0.1, 0.1, 0.3, 0.3, 0.5, 0.1)

Kompatibilität: Ja/Nein           γ(I⃗_i, I⃗_j) ∈ [-1, 1]
```

---

## Praktische Implikationen

### 1. Tabellen zeigen "Affinitäten", nicht "Typen"

```latex
% FALSCH (diskrete Typen als Spalten):
\begin{tabular}{l|cccccccc}
Segment & T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 \\
\end{tabular}

% RICHTIG (Dimension-Affinitäten mit Footnote):
\begin{tabular}{l|cccccccc}
& \multicolumn{8}{c}{\textbf{10C Dimension Emphasis}} \\
Segment & AWARE & READY & WHEN & STAGE & WHO & WHAT$_S$ & WHAT$_F$ & HOW \\
\end{tabular}
\footnotetext{Interventionen emergieren aus [0,1]⁹. Die Spalten zeigen
Affinität zu Interventionen mit hoher Intensität auf dieser Dimension.}
```

### 2. Die Fußnote ist PFLICHT

Bei jeder Tabelle, die 10C-Dimensionen als Spalten verwendet:

```latex
\footnotetext{Note: The 10C dimensions are the primitives. Interventions
\textit{emerge} from the continuous 10C space $[0,1]^9$ based on context
analysis (Axiom EIT-3). The columns represent interventions with high
intensity on that 10C dimension.}
```

### 3. Segment-Multiplier sind gewichtete Kombinationen

```math
σ_s(I⃗) = ∑_d I_d · σ_s(d)
```

Der effektive Multiplier für Segment $s$ bei Interventionsvektor $I⃗$ ist eine gewichtete Summe der Dimension-Affinitäten.

---

## Historische Notation: T1-T8 → A1-A8

### Mapping (nur für Rückwärtskompatibilität)

| Alt (T) | Neu (A) | 10C Dominante Dim. | Name |
|---------|---------|-------------------|------|
| T1 | A1 | AWARE | Awareness/Information |
| T2 | A2 | AWARE + READY | Feedback |
| T3 | A3 | HOW | Choice Architecture |
| T4 | A4 | WHEN | Timing |
| T5 | A5 | WHO (self) | Identity |
| T6 | A6 | WHO (others) | Social Norms |
| T7 | A7 | WHAT | Financial Incentives |
| T8 | A8 | HOW + binding | Commitment |

**WICHTIG:** A1-A8 sind AUCH nur Heuristiken! Die wahre Ontologie ist der kontinuierliche Raum.

---

## Zusammenfassung: Die drei Ebenen

```
EBENE 1: ONTOLOGISCHE PRIMITIVE (die einzige Wahrheit)
═══════════════════════════════════════════════════════
  • 10C Dimensionen: WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, STAGE, HIERARCHY
  • Kontinuierlicher Raum: [0,1]⁹
  • Interventionsvektor: I⃗ = (I_WHO, I_WHAT, ...)

EBENE 2: EMERGENTE CLUSTER (praktische Heuristiken)
═══════════════════════════════════════════════════════
  • A1-A8 Archetypen
  • Hochdichte Regionen im Interventionsraum
  • Nützlich für Kommunikation und E-PARTIAL/E-NONE Modi

EBENE 3: HISTORISCHE NOTATION (deprecated)
═══════════════════════════════════════════════════════
  • T1-T8 Labels
  • Nur noch in historischem Kontext verwenden
  • Kapitel 17 zeigt explizit "was überwunden wird"
```

---

## Implementierungs-Checkliste

### Bei neuen Dokumenten:

- [ ] Verwende 10C-Dimensionen als Primitive
- [ ] Beschreibe Interventionen als Vektoren $I⃗ \in [0,1]^9$
- [ ] Bei Tabellen: "10C Dimension Emphasis" als Header
- [ ] Pflicht-Fußnote bei allen Dimension-Tabellen
- [ ] Erkläre Cluster als "emergent", nicht "kategorisch"
- [ ] Bei niedrigem $D_{suff}$: Erkläre E-PARTIAL oder E-NONE Modus

### Bei bestehenden Dokumenten:

- [ ] T1-T8 → A1-A8 nur wenn historischer Kontext
- [ ] AWA/RDY/WHN/etc. → AWARE/READY/WHEN/etc. (volle Namen)
- [ ] Fußnoten hinzufügen, die Emergenz erklären
- [ ] "Type" → "Dimension Emphasis" oder "Affinity"

---

*Version 1.0 | Januar 2026*
*Basierend auf Appendix IE (CORE-EIT) und Appendix HHH (METHOD-TOOLKIT)*
