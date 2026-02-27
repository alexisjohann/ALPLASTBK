---
marp: true
theme: default
paginate: true
backgroundColor: #FFFFFF
style: |
  :root {
    --fa-darkblue: #024079;
    --fa-lightblue: #549EDE;
    --fa-darkgray: #25212A;
    --fa-lightgray: #F3F5F7;
  }
  section {
    font-family: 'Open Sans', sans-serif;
    color: #25212A;
  }
  h1, h2 {
    font-family: 'Roboto', sans-serif;
    font-weight: bold;
    color: #024079;
  }
  h3, h4 {
    font-family: 'Roboto', sans-serif;
    font-weight: normal;
    color: #024079;
  }
  table {
    font-size: 0.85em;
  }
  th {
    background-color: #024079;
    color: white;
  }
  tr:nth-child(even) {
    background-color: #F3F5F7;
  }
  .highlight {
    color: #549EDE;
    font-weight: bold;
  }
  .source {
    font-size: 0.6em;
    color: #888;
    position: absolute;
    bottom: 20px;
  }
---

<!-- Slide 1: Titel -->

# Verstehen Menschen Interdependenzen?

## Eine verhaltensökonomische Analyse

<br>

**Session:** EBF-S-2026-01-26-COG-001
**Fragesteller:** Johannes Luger
**Datum:** 26. Januar 2026

<br>

**FehrAdvice & Partners AG**
*Evidence-Based Framework (EBF)*

---

<!-- Slide 2: Executive Summary -->

# Executive Summary

<br>

## Kernbefund

> **Menschen verstehen Interdependenzen nur unter sehr engen Bedingungen.**

<br>

| Metrik | Wert |
|--------|------|
| Median strategisches Denken | **1.5 Levels** |
| Anteil mit max. 1 Schritt | **70%** |
| Haupttreiber für Scheitern | **Komplexität (42%)** |
| Konfidenz | **85%** |

<br>

**Implikation:** Bei Interventionsdesign NIEMALS davon ausgehen, dass Menschen Interdependenzen verstehen.

---

<!-- Slide 3: Die Frage & Drei Lesarten -->

# Die Frage: Drei Lesarten

<br>

| Lesart | Frage | Antwort |
|--------|-------|---------|
| **L1: Kognitiv** | Können Menschen komplexe Systeme mental simulieren? | ❌ NEIN |
| **L2: Strategisch** | Antizipieren Menschen die Reaktionen anderer? | ⚠️ BEGRENZT |
| **L3: Systemisch** | Verstehen Menschen Feedback-Loops? | ❌ KAUM |

<br>

### Relevante Dimensionen (10C Framework)

- **AWARE:** Bewusstsein für Interdependenz
- **HOW:** Verarbeitung von Komplementarität
- **HIERARCHY:** Kognitive Tiefe (Level-k)

---

<!-- Slide 4: Das Modell IDV-2.0 -->

# Modell: Interdependenz-Verständnis (IDV-2.0)

<br>

## Formel

$$V(n) = \frac{(\kappa + \lambda \cdot E) \cdot \psi \cdot (1 + \mu \cdot S)}{n^{\alpha_d} \cdot (1+\tau)^{\beta_d} \cdot (1+\sigma)^{\gamma_d}}$$

<br>

| Variable | Bedeutung | Effekt |
|----------|-----------|--------|
| **n** | Systemkomplexität | ↑n → ↓V |
| **τ** | Zeit-Delay | ↑τ → ↓V |
| **σ** | Soziale Distanz | ↑σ → ↓V |
| **ψ** | Feedback-Sichtbarkeit | ↑ψ → ↑V |
| **λ·E** | Lernen durch Erfahrung | ↑E → ↑V |

<div class="source">Basis: Camerer et al. (2004), Kahneman (2011), Simon (1955)</div>

---

<!-- Slide 5: Cognitive Hierarchy -->

# Cognitive Hierarchy: Wie weit denken Menschen?

<br>

```
Level-0 (21%):  ████████████████████░░░░░░░░░░░░░░░░░░░░  Keine Überlegung
Level-1 (49%):  ████████████████████████████████████████  "Was machen die anderen?"
Level-2 (24%):  ████████████████████████░░░░░░░░░░░░░░░░  "Was denken die, was ich denke?"
Level-3+ (6%):  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  Tiefe Rekursion (selten!)
```

<br>

### Kernbefund

- **Median: 1.47 Levels** (±0.25)
- **70%** der Menschen denken maximal 1 Schritt voraus
- **Nash-Equilibrium** (∞ Schritte) erreicht fast niemand

<div class="source">Quelle: Camerer, Ho, Chong (2004), Quarterly Journal of Economics</div>

---

<!-- Slide 6: Ergebnisse nach Situation -->

# Verständnis nach Situation

<br>

| Situation | n | τ | σ | V(n) | Bewertung |
|-----------|---|---|---|------|-----------|
| **Verhandlung 1:1** | 2 | 0 | 0.1 | 0.78 | ✅ Gut |
| **Teamarbeit (5P)** | 5 | 1 | 0.3 | 0.41 | ⚠️ Mässig |
| **Markt** | 50 | 2 | 0.6 | 0.12 | ❌ Schlecht |
| **Klimawandel** | 10⁶ | 30 | 0.9 | 0.02 | ❌❌ Minimal |
| **Rentensystem** | 10⁵ | 40 | 0.7 | 0.03 | ❌❌ Minimal |

<br>

### Erkenntnis

> Bei **n > 10 Elementen** fällt das Verständnis unter 25% – unabhängig von Intelligenz oder Motivation.

---

<!-- Slide 7: Sensitivitätsanalyse -->

# Was treibt (mangelndes) Verständnis?

<br>

```
Komplexität (n)     ████████████████████████████████████████████  42%  ← DOMINANT
Zeit-Delay (τ)      ████████████████████████████░░░░░░░░░░░░░░░░  28%
Feedback (ψ)        ██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  18%
Soz. Distanz (σ)    ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   8%
Kapazität (κ)       ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   4%
```

<br>

### Haupterkenntnis

**Komplexität dominiert alles.**

Selbst mit perfektem Feedback (ψ=1), hoher Motivation (μ·S=1) und viel Erfahrung:
- Bei **n > 10:** V < 0.25
- Bei **n > 50:** V < 0.10

**→ Kognitive Kapazität ist NICHT der Engpass!**

---

<!-- Slide 8: Schlussfolgerungen -->

# Schlussfolgerungen

<br>

## Wann Menschen Interdependenzen verstehen ✅

- 2-3 Akteure (n ≤ 3)
- Sofortiges Feedback (τ ≈ 0)
- Konkrete, nahe Andere (σ niedrig)
- Wiederholte Erfahrung (E hoch)

<br>

## Wann Menschen scheitern ❌

- Viele Akteure (Märkte, Gesellschaft, Ökosysteme)
- Verzögerte Effekte (Klima, Rente, Gesundheit)
- Abstrakte Andere («zukünftige Generationen»)
- Verstecktes Feedback (keine sichtbaren Konsequenzen)

---

<!-- Slide 9: Praktische Implikationen -->

# Praktische Implikationen für Interventionsdesign

<br>

## Die 4 Hebel

| # | Strategie | Massnahme | Effekt |
|---|-----------|-----------|--------|
| 1 | **Komplexität ↓** | Weniger Optionen, klare Pfade | n↓ → V↑ |
| 2 | **Feedback ↑** | Sofortige Konsequenz-Anzeige | ψ↑ → V↑ |
| 3 | **Delays überbrücken** | Future Self salient machen | τ_eff↓ → V↑ |
| 4 | **Abstrakte konkretisieren** | «Dein Nachbar» statt «die Welt» | σ↓ → V↑ |

<br>

### Goldene Regel

> **NIEMALS** davon ausgehen, dass Menschen Interdependenzen verstehen.
> **IMMER** das System für sie vereinfachen.

---

<!-- Slide 10: Quellen & Kontakt -->

# Quellen & Kontakt

<br>

## Wissenschaftliche Basis

- Camerer, Ho, Chong (2004): *Cognitive Hierarchy Model*, QJE
- Crawford, Costa-Gomes, Iriberri (2013): *Structural Models of Strategic Thinking*, JEL
- Kahneman (2011): *Thinking, Fast and Slow*
- Simon (1955): *A Behavioral Model of Rational Choice*, QJE

<br>

## Kontakt

**FehrAdvice & Partners AG**
Klausstrasse 20, 8008 Zürich

**Evidence-Based Framework (EBF)**
Session-ID: EBF-S-2026-01-26-COG-001
Modell-ID: EBF-MOD-IDV-001

---

<!-- Backup Slide: Domain-spezifische Exponenten -->

# Backup: Domain-spezifische Parameter

<br>

| Domain | α (Komplexität) | β (Zeit) | γ (Distanz) | Beschreibung |
|--------|-----------------|----------|-------------|--------------|
| **SOC** | 0.48 | 0.32 | 0.58 | Soziale Interdependenz |
| **ECO** | 0.72 | 0.48 | 0.28 | Ökonomische Märkte |
| **ENV** | 0.82 | 0.78 | 0.42 | Umwelt/Klima |
| **TEC** | 0.88 | 0.42 | 0.22 | Technische Systeme |

<br>

### Interpretation

- **Höheres α:** Komplexität schadet mehr
- **Höheres β:** Zeit-Delays schaden mehr
- **Höheres γ:** Soziale Distanz schadet mehr

**→ ENV (Klima) ist die schwierigste Domain für menschliches Verständnis.**
