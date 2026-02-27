# Chapter 10: Welfare and FEPSDE — CORE-WHAT + CORE-WHO

> Die Nutzenarchitektur: INU/KNU/IDN × FEPSDE

---

## Übersicht

| Metrik | Wert |
|--------|------|
| **Datei** | `10_welfare_fepsde.tex` (Master) |
| **Teil** | III (Welfare/FEPSDE) |
| **Seiten** | ~80 (inkl. Subkapitel) |
| **Primary COREs** | **C (WHAT)**, **AAA (WHO)** |

---

## 🎯 Die fundamentalen Fragen

> **WHAT: Was ist Utility?** → FEPSDE-Dimensionen definieren die 6 Wohlfahrtskategorien
>
> **WHO: Wer hat Utility?** → Level L bestimmt, OB INU, KNU oder IDN aktiviert wird

---

## 10C CORE Integration

```
┌─────────────────────────────────────────────────────────────┐
│  CORE-WHAT + CORE-WHO in der 10C Architektur                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHO   →  Level L bestimmt AGGREGATION (INU/KNU/IDN) ← HIER│
│  WHAT  →  FEPSDE definiert 144 KOMPONENTEN          ← HIER │
│  HOW   →  γ_{ij} verbindet FEPSDE-Dimensionen               │
│  WHEN  →  Ψ moduliert LEVEL-SALIENZ α^L(Ψ)                  │
│  WHERE →  Θ kalibriert DIMENSION-GEWICHTE                   │
│  AWARE →  A(·) filtert BEWUSSTE Dimensionen                 │
│  READY →  WAX integriert alles in HANDLUNGSSCHWELLE         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Der zentrale Durchbruch: Level-indizierte KNU

| Level L | Beschreibung | KNU-Fokus |
|---------|--------------|-----------|
| L=1 | Individuum | Nur INU (kein KNU) |
| L=2 | Dyade | Partner |
| L=3 | Familie | Kinder, Eltern |
| L=4 | Stamm/Freunde | Nahestehende |
| L=5 | Organisation | Kollegen, Team |
| L=6 | Nation | Mitbürger |
| L=∞ | Meta/Menschheit | Alle |

**Formalisierung:**
$$KNU_{total} = \sum_{L=1}^{\infty} \alpha^L(\Psi) \cdot U^{KNU,L}$$

Wobei $\alpha^L(\Psi)$ die **Level-Salienz** bestimmt — gesteuert durch WHEN (Kontext).

---

### Verbindungen zu anderen COREs

| CORE | Wie Ch.10 beiträgt | Subkapitel |
|------|--------------------|------------|
| **WHO** (AAA) | Level L → INU/KNU/IDN Aktivierung | 10.1, 10.8 |
| **WHAT** (C) | FEPSDE-Dimensionen definiert | 10.2, 10.3 |
| **HOW** (B) | Inter-Kategorie Komplementarität | 10.6 |
| **WHEN** (V) | Kontext moduliert Dimensionen | 10.7 |
| **WHERE** (BBB) | Kalibrierung implizit | 10.4 |
| **AWARE** (AU) | Dimensionsbewusstsein | → Ch.11 |
| **READY** (AV) | Handlungsschwelle | → Ch.12 |

---

## Struktur (10 Subkapitel)

| Subkap. | Datei | Thema | CORE |
|---------|-------|-------|------|
| 10.1 | `10_1_three_utility_categories.tex` | INU/KNU/IDN + **Level-Dependency** | C, **AAA** |
| 10.2 | `10_2_fepsde_dimensions.tex` | FEPSDE-Dimensionen | **C** |
| 10.3 | `10_3_144_component_structure.tex` | 144-Komponenten Matrix | C |
| 10.4 | `10_4_uniform_calculation_logic.tex` | Einheitliche Berechnungslogik | — |
| 10.5 | `10_5_reference_points.tex` | Referenzpunkte C* | — |
| 10.6 | `10_6_inter_category_complementarities.tex` | Inter-Kategorie Komplementaritäten | B |
| 10.7 | `10_7_context_modulation.tex` | Kontext-Modulation der FEPSDE | V |
| 10.8 | `10_8_aggregate_welfare_function.tex` | Aggregierte Wohlfahrtsfunktion | **AAA** |
| 10.9 | `10_9_*.tex` (5 Dateien) | Domänen-Anwendungen | DOMAIN |
| 10.10 | `10_10_cross_domain_patterns.tex` | Cross-Domain Muster | — |

---

## Schlüsselkonzepte

### Die drei Nutzenkategorien

| Kategorie | Symbol | Definition | Level-Abhängig? |
|-----------|--------|------------|-----------------|
| **INU** | Individual Needs Utility | Individuelle Bedürfnisse | Nein (L=1) |
| **KNU** | Kin Needs Utility | Nahestehende Bedürfnisse | **Ja (L=2...∞)** |
| **IDN** | Identity Needs | Identitätsbedürfnisse | Ja (Level-Identität) |

### Die sechs FEPSDE-Dimensionen

| Dim | Symbol | Definition |
|-----|--------|------------|
| **F** | Financial | Finanzielle Wohlfahrt |
| **E** | Emotional | Emotionale Wohlfahrt |
| **P** | Physical | Physische Wohlfahrt |
| **S** | Social | Soziale Wohlfahrt |
| **D** | Digital | Digitale Wohlfahrt |
| **Eco** | Ecological | Ökologische Wohlfahrt |

### Die 144-Komponenten Matrix

$$3 \text{ (INU/KNU/IDN)} \times 6 \text{ (FEPSDE)} \times 4 \text{ (Zeit)} \times 2 \text{ (Valenz)} = 144$$

---

## Key Insight

> **WHO × WHEN → WHAT Integration:**
>
> Der Kontext (WHEN) bestimmt über die Level-Salienz α^L(Ψ), WELCHES Level (WHO) psychologisch aktiv ist.
> Das Level wiederum bestimmt, WELCHE KNU-Komponenten relevant sind.
>
> **Beispiel:** Ein Jobangebot wird unterschiedlich bewertet je nachdem, ob gerade das Familien-Level (L=3, KNU für Kinder) oder das Organisations-Level (L=5, Kollegen) salient ist.

---

## Verbindungen

| Zu Kapitel | Thema | CORE |
|------------|-------|------|
| ← Ch. 1b | 10C CORE Architektur | Alle 8 |
| ← Ch. 5 | Komplementarität γ | HOW |
| ← Ch. 9 | Kontext Ψ | WHEN |
| → Ch. 11 | Awareness A(·) | AWARE |
| → Ch. 12 | Willingness WAX | READY |
| → Appendix C | FEPSDE Matrix (Detail) | **WHAT** |
| → Appendix AAA | Aggregationsebenen | **WHO** |

---

*10C CORE Framework — EBF*
