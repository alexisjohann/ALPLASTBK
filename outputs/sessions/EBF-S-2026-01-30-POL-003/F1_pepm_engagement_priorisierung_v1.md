# EBF Session Report: Political Engagement Portfolio Model (PEPM)

**Session-ID:** EBF-S-2026-01-30-POL-003
**Kunde:** economiesuisse
**Projekt:** PRJ-ECOS-003 (Political Engagement Prioritization)
**Modus:** STANDARD
**Datum:** 2026-01-30

---

## Executive Summary

Dieses Dokument beschreibt das **Political Engagement Portfolio Model (PEPM)** - ein Entscheidungsmodell zur Priorisierung politischen Engagements über verschiedene Abstimmungen hinweg. Das Modell berücksichtigt:

1. **Stakeholder-Heterogenität** - Verschiedene Interessen innerhalb von economiesuisse
2. **Interdependenzen** - Spillover-Effekte zwischen Abstimmungen
3. **Risiko-Bewertung** - Verlust bei Nicht-Engagement
4. **Ressourcen-Optimierung** - Optimale Allokation des politischen Budgets

**Ranking für 2026:**
1. EU-Rahmenabkommen II (Π = 0.458)
2. USA-Zollabkommen (Π = 0.449)
3. 10-Millionen-Initiative (Π = 0.382)
4. Biodiversitäts-Initiative (Π = 0.271)
5. Prämienentlastung (Π = 0.249)

---

## 1. Problemstellung

### 1.1 Aufgabe

Economiesuisse steht vor der Herausforderung, begrenzte Ressourcen (Budget, Personal, politisches Kapital) über mehrere parallele Abstimmungen zu verteilen. Die Komplexität entsteht durch:

- **Stakeholder-Heterogenität:** Pharma, Banking, MEM, Chemie etc. haben unterschiedliche Prioritäten
- **Interdependenzen:** Abstimmungsergebnisse beeinflussen sich gegenseitig
- **Unsicherheit:** Kampagnendynamik und Gegner-Verhalten schwer vorhersagbar

### 1.2 Fragestellung

> *Wie kann economiesuisse ihr Engagement bei unterschiedlichen Volksabstimmungen und Referenden priorisieren, unter Berücksichtigung von:*
> - *Impact auf andere Fokusthemen*
> - *Risiko bei Nicht-Engagement*
> - *Internen Stakeholder-Interessen*

---

## 2. Modell: MOD-017 PEPM

### 2.1 Drei-Ebenen-Architektur

```
EBENE 1: VOTE ASSESSMENT
├── Strategic Value (Sᵢ)
├── Risk Score (Rᵢ)
├── Impact Score (Iᵢ)
└── Alignment Score (Aᵢ)
         ↓
EBENE 2: INTERDEPENDENCY MAPPING
├── Spillover Matrix (Γ)
└── Cluster Identification
         ↓
EBENE 3: PORTFOLIO OPTIMIZATION
├── Priority Score (Πᵢ)
└── Optimal Engagement (eᵢ*)
```

### 2.2 Kernformeln

**Strategic Value:**
```
Sᵢ = Σₖ wₖ × Uₖ(vᵢ)
```
Gewichtete Summe der Stakeholder-Utilities für Abstimmung i.

**Risk Score:**
```
Rᵢ = P(Niederlage | e=0) × λ × |Sᵢ|
```
Verlust-gewichtetes Risiko (λ = 2.1 für Schweiz).

**Impact Score:**
```
Iᵢ = ΔP(Erfolg | e=1) - ΔP(Erfolg | e=0)
```
Marginaler Effekt des eigenen Engagements.

**Alignment Score:**
```
Aᵢ = 1 - Var({Uₖ(vᵢ)}) / Var_max
```
Interner Konsens (1 = perfekt, 0 = maximal gespalten).

**Priority Score:**
```
Πᵢ = w₁×|Sᵢ| + w₂×Rᵢ + w₃×Iᵢ + w₄×Aᵢ + w₅×Σⱼγᵢⱼ - w₆×(rᵢ/R)
```

**Gewichte:**
| Parameter | Wert | Beschreibung |
|-----------|------|--------------|
| w₁ | 0.25 | Strategic Value |
| w₂ | 0.25 | Risk |
| w₃ | 0.15 | Impact |
| w₄ | 0.15 | Alignment |
| w₅ | 0.15 | Spillover |
| w₆ | 0.05 | Cost |

---

## 3. Stakeholder-Analyse

### 3.1 Stakeholder-Gruppen

| k | Stakeholder | Gewicht wₖ | Mitglieder |
|---|-------------|------------|------------|
| 1 | Pharma | 0.20 | Novartis, Roche, Lonza |
| 2 | Banking | 0.20 | UBS, ZKB, Raiffeisen |
| 3 | MEM | 0.15 | ABB, Sulzer, Bühler |
| 4 | Chemie | 0.12 | Syngenta, Clariant |
| 5 | Uhren | 0.10 | Swatch, Richemont, Rolex |
| 6 | Versicherungen | 0.08 | Zurich, Swiss Re |
| 7 | Detailhandel | 0.08 | Migros, Coop |
| 8 | Tourismus | 0.07 | Hotellerie Suisse |

### 3.2 Utility-Dimensionen

| Symbol | Dimension | Beschreibung |
|--------|-----------|--------------|
| U_reg | Regulatory Burden | Auswirkung auf Regulierungslast |
| U_cost | Cost Impact | Kosten (Arbeit, Steuern) |
| U_market | Market Access | Marktzugang |
| U_rep | Reputation | Image/Reputation |
| U_labor | Labor Availability | Arbeitskräfteangebot |

---

## 4. Anwendung: economiesuisse 2026

### 4.1 Portfolio-Abstimmungen

| ID | Abstimmung | Timing | Status |
|----|------------|--------|--------|
| V1 | USA-Zollabkommen | Q3-2026 | Wahrscheinlich |
| V2 | 10-Millionen-Initiative | Q4-2026 | Sicher |
| V3 | EU-Rahmenabkommen II | 2027 | Möglich |
| V4 | Prämienentlastungs-Initiative | 2026 | Sicher |
| V5 | Biodiversitäts-Initiative | 2026 | Sicher |

### 4.2 Utility-Matrix Uₖ(vᵢ)

**Skala:** -1 (stark negativ) bis +1 (stark positiv)

| Abstimmung | Pharma | Banking | MEM | Chemie | Uhren | Versich. | Detail | Tourism |
|------------|--------|---------|-----|--------|-------|----------|--------|---------|
| V1 USA-Zoll | +0.3 | +0.2 | +0.9 | +0.7 | +0.8 | +0.1 | +0.4 | +0.2 |
| V2 10-Mio | -0.8 | -0.6 | -0.7 | -0.5 | -0.4 | -0.3 | -0.6 | -0.9 |
| V3 EU-Rahmen | +0.4 | +0.8 | +0.6 | +0.5 | +0.3 | +0.7 | +0.3 | +0.5 |
| V4 Prämien | -0.2 | -0.3 | -0.1 | -0.1 | 0.0 | -0.9 | -0.2 | -0.1 |
| V5 Biodiv | -0.3 | -0.1 | -0.4 | -0.6 | -0.2 | -0.1 | -0.3 | -0.5 |

### 4.3 Score-Berechnung

| Abstimmung | Sᵢ | Rᵢ | Iᵢ | Aᵢ | Σγ | **Πᵢ** |
|------------|------|------|------|------|------|--------|
| V1 USA-Zoll | 0.453 | 0.62 | 0.08 | 0.78 | 0.45 | **0.449** |
| V2 10-Mio | -0.620 | 0.07 | 0.05 | 0.92 | 0.55 | **0.382** |
| V3 EU-Rahmen | 0.535 | 0.45 | 0.06 | 0.92 | 0.60 | **0.458** |
| V4 Prämien | -0.248 | 0.29 | 0.03 | 0.79 | 0.10 | **0.249** |
| V5 Biodiv | -0.295 | 0.28 | 0.04 | 0.93 | 0.10 | **0.271** |

### 4.4 Spillover-Matrix

```
       V1    V2    V3    V4    V5
V1     -    0.15  0.30   0     0
V2    0.15   -    0.25  0.10  0.05
V3    0.30  0.25   -     0    0.05
V4     0    0.10   0     -     0
V5     0    0.05  0.05   0     -
```

**Interpretation:**
- V1 ↔ V3: Stärkste Interdependenz (Wirtschafts-/EU-Thema)
- V2 ↔ V3: Zweistärkste (Migration/EU)
- V4, V5: Relativ isoliert

---

## 5. Ergebnisse und Empfehlungen

### 5.1 Priority Ranking

| Rang | Abstimmung | Πᵢ | Empfohlenes Budget |
|------|------------|-----|-------------------|
| **1** | EU-Rahmenabkommen II | 0.458 | 30-35% |
| **2** | USA-Zollabkommen | 0.449 | 25-30% |
| **3** | 10-Millionen-Initiative | 0.382 | 20-25% |
| **4** | Biodiversitäts-Initiative | 0.271 | 10-15% |
| **5** | Prämienentlastung | 0.249 | 5-10% |

### 5.2 Strategische Begründung

**EU-Rahmenabkommen (Rang 1):**
- Höchster Strategic Value (alle Stakeholder profitieren)
- Höchste Spillover-Summe (beeinflusst andere Vorlagen)
- Hohe Alignment (wenig interne Konflikte)

**USA-Zollabkommen (Rang 2):**
- Höchster Risk Score (Niederlage hätte grosse Konsequenzen)
- Wichtig für exportorientierte Branchen (MEM, Uhren, Chemie)
- Positiver Spillover zu EU-Thema

**10-Millionen-Initiative (Rang 3):**
- Höchster absoluter Strategic Value (alle dagegen)
- Grundsatz-Abstimmung für Wirtschaftsstandort
- Trotz niedrigem Risiko (hohe Gewinnwahrscheinlichkeit) wichtig wegen Spillover

### 5.3 Warnung: Prämienentlastung

Bei V4 (Prämienentlastung) besteht **interner Konflikt**:
- Versicherungen (wₖ = 0.08): Utility = -0.9 (stark dagegen)
- Andere Stakeholder: Mässig negativ bis neutral

**Empfehlung:** Engagement hier v.a. zur Konflikt-Minimierung, nicht zur Kampagnenführung.

---

## 6. Methodische Transparenz

### 6.1 Datenquellen

| Parameter | Quelle | Konfidenz |
|-----------|--------|-----------|
| Stakeholder-Gewichte | Expert Elicitation | Mittel |
| Utility-Matrix | Inference aus Positionen | Mittel |
| Impact Scores | Historische Kampagnen | Niedrig |
| Spillover-Matrix | Qualitative Analyse | Niedrig |

### 6.2 Limitationen

- Utility-Werte sind Schätzungen, nicht empirisch gemessen
- Spillover-Effekte schwer zu quantifizieren
- Politische Dynamik kann sich während Kampagne ändern
- Gewichte (w₁-w₆) sind normativ festgelegt

### 6.3 Sensitivität

Der grösste Einfluss auf das Ranking hat:
1. **λ (Loss Aversion):** Bei λ > 2.5 würde V1 auf Rang 1 springen
2. **Spillover-Matrix:** Bei stärkerer V2↔V3 Korrelation würde V2 steigen
3. **Stakeholder-Gewichte:** Wenn MEM/Uhren höher gewichtet: V1 steigt

---

## 7. Modell-Registrierung

**ID:** MOD-017
**Name:** Political Engagement Portfolio Model (PEPM)
**Version:** 1.0
**Pfad:** data/model-registry.yaml
**Theorie-Basis:** MS-RD-001 (Prospect Theory), MS-SP-001 (Inequity Aversion)

---

## Anhang: Berechnung Strategic Value

**V1 (USA-Zoll):**
```
S₁ = 0.20×0.3 + 0.20×0.2 + 0.15×0.9 + 0.12×0.7 + 0.10×0.8 + 0.08×0.1 + 0.08×0.4 + 0.07×0.2
   = 0.06 + 0.04 + 0.135 + 0.084 + 0.08 + 0.008 + 0.032 + 0.014
   = 0.453
```

**V2 (10-Mio):**
```
S₂ = 0.20×(-0.8) + 0.20×(-0.6) + 0.15×(-0.7) + 0.12×(-0.5) + 0.10×(-0.4) + 0.08×(-0.3) + 0.08×(-0.6) + 0.07×(-0.9)
   = -0.16 - 0.12 - 0.105 - 0.06 - 0.04 - 0.024 - 0.048 - 0.063
   = -0.620
```

---

*Erstellt: 2026-01-30*
*Framework: EBF Evidence-Based Framework v1.22*
*Modell: MOD-017 Political Engagement Portfolio Model (PEPM) v1.0*
*https://claude.ai/code/session_01BNKy1t1mhnVh3WCXZHFdG8*
