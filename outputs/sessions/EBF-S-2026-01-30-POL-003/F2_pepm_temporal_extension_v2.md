# EBF Session Report: PEPM Temporal Extension (v2.0)

**Session-ID:** EBF-S-2026-01-30-POL-003
**Kunde:** economiesuisse
**Projekt:** PRJ-ECOS-003 (Political Engagement Prioritization)
**Modus:** STANDARD
**Datum:** 2026-01-30

---

## Executive Summary

Erweiterung des **Political Engagement Portfolio Model (PEPM)** um temporale Komponenten:

1. **Vote Probability P(Vote)** - Wahrscheinlichkeit, dass Abstimmung stattfindet
2. **Temporal Discount δ(τ)** - Abzinsung entfernter Abstimmungen
3. **4-Horizont-Planung** - H1 (0-12M), H2 (12-24M), H3 (24-36M), H4 (36-48M)

**Neue Formel:**
```
Π*ᵢ = P(Vote)ᵢ × δ(τᵢ) × Πᵢ
```

---

## 1. Neue Modell-Komponenten (v2.0)

### 1.1 Vote Probability P(Vote)ᵢ

**Definition:** Wahrscheinlichkeit, dass Abstimmung i tatsächlich stattfindet

| Status | P(Vote) | Beispiel |
|--------|---------|----------|
| **Sicher** | 1.00 | Datum fixiert, Vorlagen bekannt |
| **Sehr wahrscheinlich** | 0.85-0.95 | Referendum wird ergriffen |
| **Wahrscheinlich** | 0.60-0.85 | Gesetz in Beratung |
| **Möglich** | 0.30-0.60 | Vorstoss hängig |
| **Unwahrscheinlich** | 0.10-0.30 | Frühe Planungsphase |
| **Spekulativ** | <0.10 | Gerüchte |

### 1.2 Temporal Discount δ(τ)

**Formel:**
```
δ(τᵢ) = 1 / (1 + r)^(τᵢ/12)
```

**Parameter:**
- τᵢ = Monate bis zur Abstimmung
- r = 0.15 (politischer Diskontfaktor, jährlich)

**Diskontfaktoren:**

| τ (Monate) | δ(τ) |
|------------|------|
| 2 | 0.98 |
| 6 | 0.93 |
| 12 | 0.87 |
| 24 | 0.76 |
| 36 | 0.66 |
| 48 | 0.57 |

### 1.3 Adjusted Priority Π*

**Formel:**
```
Π*ᵢ = P(Vote)ᵢ × δ(τᵢ) × Πᵢ
```

**Interpretation:**
- Sichere, nahe Abstimmungen: hoher Π*
- Unsichere, ferne Abstimmungen: niedriger Π*

---

## 2. 4-Horizont-Struktur

### 2.1 Budget-Allokation

| Horizont | Zeitraum | Budget | Fokus |
|----------|----------|--------|-------|
| **H1** | 0-12 Monate | 50% | Unmittelbare Abstimmungen |
| **H2** | 12-24 Monate | 25% | Mittelfristige Planung |
| **H3** | 24-36 Monate | 15% | Langfristige Positionierung |
| **H4** | 36-48 Monate | 10% | Strategische Reserve |

### 2.2 Charakteristik pro Horizont

**H1 (Kurzfristig):**
- Hohe Sicherheit (P(Vote) > 0.80)
- Konkrete Kampagnenplanung
- Ressourcen-Allokation fixiert

**H2 (Mittelfristig):**
- Mittlere Sicherheit (P(Vote) 0.50-0.80)
- Strategische Positionierung
- Allianzbildung

**H3 (Langfristig):**
- Niedrige Sicherheit (P(Vote) 0.30-0.60)
- Szenario-Planung
- Kapazitätsaufbau

**H4 (Strategisch):**
- Sehr niedrige Sicherheit (P(Vote) < 0.40)
- Reserve für Überraschungen
- Netzwerk-Investitionen

---

## 3. Abstimmungs-Pipeline 2026-2030

### 3.1 Vollständige Pipeline

| ID | Vorlage | τ | H | P(Vote) | Sᵢ | Πᵢ | **Π*** |
|----|---------|---|---|---------|-----|-----|--------|
| V01 | Bargeld-Initiative | 2 | H1 | 1.00 | -0.08 | 0.17 | 0.167 |
| V02 | SRG-Initiative | 2 | H1 | 1.00 | 0.05 | 0.17 | 0.167 |
| V03 | Klimafonds | 2 | H1 | 1.00 | -0.29 | 0.26 | **0.255** |
| V04 | Individualbesteuerung | 2 | H1 | 1.00 | 0.21 | 0.23 | **0.225** |
| V05 | 10-Mio-Initiative | 5 | H1 | 0.98 | -0.62 | 0.38 | **0.350** |
| V06 | USA-Zollabkommen | 8 | H1 | 0.75 | 0.45 | 0.45 | **0.304** |
| V07 | EU-Rahmenabkommen | 18 | H2 | 0.60 | 0.54 | 0.46 | **0.224** |
| V08 | AHV-Reform | 21 | H2 | 0.70 | 0.43 | 0.37 | 0.202 |
| V09 | Energie-Folge | 27 | H3 | 0.50 | -0.21 | 0.24 | 0.088 |
| V10 | Gesundheitskosten | 30 | H3 | 0.55 | -0.27 | 0.25 | 0.098 |

### 3.2 Ranking nach Π*

| Rang | Vorlage | Horizont | Π* |
|------|---------|----------|-----|
| **1** | 10-Millionen-Initiative | H1 | 0.350 |
| **2** | USA-Zollabkommen | H1 | 0.304 |
| **3** | Klimafonds-Initiative | H1 | 0.255 |
| **4** | Individualbesteuerung | H1 | 0.225 |
| **5** | EU-Rahmenabkommen II | H2 | 0.224 |
| 6 | AHV-Reform | H2 | 0.202 |
| 7 | Bargeld-Initiative | H1 | 0.167 |
| 8 | SRG-Initiative | H1 | 0.167 |
| 9 | Gesundheitskosten | H3 | 0.098 |
| 10 | Energie-Folgevorlagen | H3 | 0.088 |

---

## 4. Empfehlungen pro Horizont

### 4.1 H1: 0-12 Monate (50% Budget)

| Vorlage | Termin | Budget | Begründung |
|---------|--------|--------|------------|
| 10-Mio-Initiative | Jun 2026 | 25-30% | Grundsatz-Abstimmung, Umfragen knapp |
| USA-Zollabkommen | Q3-2026 | 20-25% | Höchster Risk Score |
| Klimafonds | Mär 2026 | 15-20% | Kostenrelevant |
| Individualbesteuerung | Mär 2026 | 10-15% | Positiv für Wirtschaft |
| Bargeld + SRG | Mär 2026 | 10% | Niedriger Impact |

### 4.2 H2: 12-24 Monate (25% Budget)

| Vorlage | Termin | Budget | Begründung |
|---------|--------|--------|------------|
| EU-Rahmenabkommen II | Q1-2027 | 35-40% | Strategisch zentral |
| AHV-Reform | 2027 | 25-30% | Alle Stakeholder betroffen |
| Reserve | - | 30-40% | Neue Vorlagen |

### 4.3 H3: 24-36 Monate (15% Budget)

| Fokus | Budget | Aktivitäten |
|-------|--------|-------------|
| Gesundheitskosten | 30-35% | Monitoring, Allianzpflege |
| Energie/Klima | 25-30% | Positionierung |
| Reserve | 35-45% | Flexibilität |

### 4.4 H4: 36-48 Monate (10% Budget)

| Fokus | Budget | Aktivitäten |
|-------|--------|-------------|
| Szenario-Planung | 40% | Verschiedene Pfade modellieren |
| Kapazitätsaufbau | 40% | Netzwerke, Expertise |
| Reserve | 20% | Überraschungen |

---

## 5. Spillover-Cluster

```
CLUSTER A: WIRTSCHAFT-AUSSENPOLITIK (γ = 0.35)
├── V06 USA-Zollabkommen
└── V07 EU-Rahmenabkommen

CLUSTER B: MIGRATION-BILATERALE (γ = 0.40)
├── V05 10-Mio-Initiative
└── V07 EU-Rahmenabkommen
⚠️ ACHTUNG: Gegenläufige Wirkung möglich!

CLUSTER C: KOSTEN-REGULIERUNG (γ = 0.20)
├── V03 Klimafonds
├── V08 AHV-Reform
└── V10 Gesundheitskosten

CLUSTER D: ISOLIERT (γ < 0.10)
├── V01 Bargeld
└── V02 SRG
```

---

## 6. Quellen

- [Bundeskanzlei: Blanko-Abstimmungstermine](https://www.bk.admin.ch/bk/de/home/politische-rechte/volksabstimmungen/blanko-abstimmungstermine.html)
- [admin.ch: Volksabstimmung 8. März 2026](https://www.admin.ch/gov/en/start/documentation/votes/20260308.html)
- [SRF: 10-Mio-Initiative](https://www.srf.ch/news/schweiz/keine-10-millionen-schweiz-parlament-empfiehlt-svp-zuwanderungsinitiative-zur-ablehnung)
- [swissinfo: Politische Themen 2026](https://www.swissinfo.ch/ger/schweizer-politik/was-die-schweiz-erwartet-die-wichtigsten-politischen-themen-f%C3%BCr-2026/90616780)
- [NZZ: 10-Mio ohne Gegenvorschlag](https://www.nzz.ch/schweiz/10-millionen-schweiz-das-parlament-geht-aufs-ganze-und-lehnt-die-svp-initiative-ohne-gegenvorschlag-ab-ld.1916584)

---

## 7. Modell-Update

**ID:** MOD-017
**Name:** Political Engagement Portfolio Model (PEPM)
**Version:** 2.0
**Neue Komponenten:**
- P(Vote) - Vote Probability
- δ(τ) - Temporal Discount
- Π* - Adjusted Priority
- 4-Horizont-Struktur

---

*Erstellt: 2026-01-30*
*Framework: EBF Evidence-Based Framework v1.22*
*Modell: MOD-017 PEPM v2.0*
*https://claude.ai/code/session_01BNKy1t1mhnVh3WCXZHFdG8*
