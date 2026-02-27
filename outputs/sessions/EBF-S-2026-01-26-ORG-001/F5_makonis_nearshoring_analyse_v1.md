# EBF-Analyse: Makonis Nearshoring-Standortwahl

**Session-ID:** EBF-S-2026-01-26-ORG-001
**Datum:** 2026-01-26
**Modus:** SCHNELL
**Kunde:** Makonis (IT/Software/Consulting)
**Modell:** EBF-MOD-NEAR-001 (Weighted Multi-Attribute Utility)

---

## Executive Summary

Makonis sucht einen geeigneten EU-Standort für ein Nearshoring-Team (5-10 Entwickler). Die Analyse basiert auf den Haupttreibern **Kosten**, **Arbeitsmarkt** und **Flexibilität**.

**Empfehlung:** "Poland First, Serbia Watch"
- **🥇 Polen (Krakau/Wrocław):** U = 0.78 - Beste Balance aus Talent, Kosten, EU-Sicherheit
- **🥈 Serbien (Belgrad/Novi Sad):** U = 0.77 - Beste Kosten, höchste Flex, aber nicht EU
- **🥉 Portugal (Lissabon/Porto):** U = 0.76 - Einfachste kulturelle Integration

**Kostenersparnis (5 Senior Devs):**
| Standort | All-in/Jahr | vs. DE |
|----------|-------------|--------|
| Deutschland | ~450k € | - |
| Polen | ~250k € | -44% |
| Serbien | ~180k € | -60% |
| Portugal | ~300k € | -33% |

---

## 1. Kontextanalyse

### Ψ-Dimensionen (relevant für Nearshoring)

| Dimension | Beschreibung | Implikation |
|-----------|--------------|-------------|
| **Ψ_E** (Economic) | Lohnkosten, Steuern, Infrastruktur | Senior Dev Gehälter: 25-60k € je nach Land |
| **Ψ_K** (Kultur) | Arbeitskultur, Kommunikationsstil | DE-Affinität wichtig für Integration |
| **Ψ_I** (Institutional) | EU-Recht, Arbeitsrecht, Vertragsflexibilität | EU-Länder rechtlich einfacher |
| **Ψ_T** (Temporal) | Zeitzone (max ±2h zu DE) | Alle EU-Kandidaten erfüllen dies |
| **Ψ_S** (Social) | Talent Pool, Sprachkenntnisse | Englisch Pflicht, Deutsch Bonus |

### 10C CORE Mapping

| CORE | Anwendung |
|------|-----------|
| **WHAT** | Was maximiert Nutzen? → Kosten, Talent, Flex |
| **WHO** | Wer entscheidet? → Makonis GF + HR |
| **WHERE** | Woher die Zahlen? → Eurostat, Glassdoor, Numbeo |
| **WHEN** | Kontext-Multiplikatoren → EU-Recht, Zeitzone |

---

## 2. Modellspezifikation

### Weighted Multi-Attribute Utility (WMAU)

**Formel:**
```
U(Land) = w₁·Kosten + w₂·Talent + w₃·Flex + w₄·Kultur + w₅·Risiko
```

**Gewichte (aus Treibern abgeleitet):**

| Dimension | Gewicht | Begründung |
|-----------|---------|------------|
| Kosten | 0.30 | "Kostendruck" als Haupttreiber genannt |
| Talent | 0.30 | "Arbeitsmarkt" als Haupttreiber genannt |
| Flex | 0.20 | "Flexibilität" als Haupttreiber genannt |
| Kultur | 0.10 | Implizit (DE-Kompatibilität) |
| Risiko | 0.10 | Implizit (EU-Stabilität) |

---

## 3. Parametrisierung (LLMMC)

### Kandidaten-Bewertung (0-1 Skala, höher = besser)

| Land | Kosten | Talent | Flex | Kultur | Risiko | **U(Land)** |
|------|--------|--------|------|--------|--------|-------------|
| 🇵🇱 **Polen** | 0.75 | 0.85 | 0.70 | 0.75 | 0.85 | **0.78** ★★★ |
| 🇷🇸 **Serbien** | 0.90 | 0.70 | 0.85 | 0.60 | 0.65 | **0.77** ★★★ |
| 🇵🇹 **Portugal** | 0.70 | 0.75 | 0.80 | 0.80 | 0.90 | **0.76** ★★★ |
| 🇷🇴 Rumänien | 0.85 | 0.75 | 0.75 | 0.65 | 0.75 | 0.77 ★★☆ |
| 🇧🇬 Bulgarien | 0.90 | 0.65 | 0.80 | 0.55 | 0.70 | 0.74 ★★☆ |
| 🇭🇷 Kroatien | 0.70 | 0.65 | 0.75 | 0.80 | 0.85 | 0.72 ★★☆ |

### Parameter-Erklärung

| Dimension | Was gemessen? | Top-Performer | Quelle |
|-----------|--------------|---------------|--------|
| **Kosten** | Senior Dev Gehalt relativ zu DE (~75k) | 🇷🇸🇧🇬 (~25-30k) | Glassdoor, Numbeo |
| **Talent** | IT-Absolventen, English Level, Erfahrung | 🇵🇱 (starke Unis) | Stack Overflow Survey |
| **Flex** | Contractor-Freundlichkeit, Remote-Kultur | 🇷🇸 (Flat Tax 10%) | World Bank |
| **Kultur** | DE-Arbeitskultur-Nähe, Kommunikationsstil | 🇵🇹🇭🇷 (westlich) | ESS, WVS |
| **Risiko** | EU-Mitglied, Rechtssicherheit, Währung | 🇵🇹🇵🇱 (€-Zone) | EU, IMF |

---

## 4. Ergebnisse

### Top 3 Empfehlungen

#### 🥇 POLEN (Krakau/Wrocław) - U = 0.78

**Stärken:**
- ✓ Stärkstes Talent-Ökosystem (TU Krakau, AGH, viele Seniors)
- ✓ Gute DE-Erfahrung (viele arbeiten bereits für DACH-Firmen)
- ✓ EU + PLN stabil (€-nah)
- ✓ Schnellste Time-to-Hire (3-6 Wochen)

**Schwächen:**
- ⚠ Lohnkosten steigen schnell (~8%/Jahr)
- ⚠ Krakau wird teurer (Warschau-Effekt)

**Kosten:** Senior Dev: ~35-45k €/Jahr all-in

**Empfehlung:** EoR (Employer of Record) nutzen bis ~15-20 Leute

---

#### 🥈 SERBIEN (Belgrad/Novi Sad) - U = 0.77

**Stärken:**
- ✓ Beste Kosten-Effizienz (noch ~30% unter PL)
- ✓ Sehr Freelancer-freundlich (Flat Tax 10%)
- ✓ Starke Tech-Szene (Novi Sad = "serbisches Silicon Valley")
- ✓ Hohe Motivation, westliche Kunden zu bedienen

**Schwächen:**
- ⚠ Nicht EU (aber EU-Beitrittskandidat 2028-2030)
- ⚠ Vertragsrecht komplexer
- ⚠ Brain Drain Risiko (Abwanderung nach EU)

**Kosten:** Senior Dev: ~25-35k €/Jahr all-in

**Empfehlung:** Als Scale-Option oder Backup beobachten

---

#### 🥉 PORTUGAL (Lissabon/Porto) - U = 0.76

**Stärken:**
- ✓ Westliche Arbeitskultur (einfachste Integration)
- ✓ EU + Euro + volle Rechtssicherheit
- ✓ Englisch exzellent, viele sprechen auch Deutsch
- ✓ Zeitzone identisch mit DE (CET)

**Schwächen:**
- ⚠ Teurer als Osteuropa (~50-60k Senior)
- ⚠ Kleinerer Talent Pool als Polen
- ⚠ Lissabon wird zum Tech-Hub → Gehälter steigen

**Kosten:** Senior Dev: ~45-55k €/Jahr all-in

**Empfehlung:** Wenn kulturelle Integration Priorität hat

---

## 5. Makonis-Spezifische Strategie

### "Poland First, Serbia Watch"

**Phase 1: START MIT POLEN (Krakau)**
- Geringste kulturelle Reibung
- Schnellste Time-to-Hire (3-6 Wochen)
- Bei 5-10 Leuten: EoR nutzen (z.B. Remote.com, Deel, Papaya Global)
- Kein eigenes Entity nötig bis ~15-20 Leute

**Phase 2: SERBIEN ALS BACKUP/SCALE-OPTION**
- Wenn Kosten kritischer werden
- Wenn >20 Leute → eigenes Entity lohnt sich
- EU-Beitritt 2028-2030 erwartet → Risiko sinkt dann

### Finanzielle Projektion (5 Senior Devs, Year 1)

| Option | Kosten/Jahr | Ersparnis vs. DE | Risiko |
|--------|-------------|------------------|--------|
| Deutschland | ~450k € | - | Gering |
| **Polen (empfohlen)** | ~250k € | **-44% (200k €)** | Gering |
| Serbien | ~180k € | -60% (270k €) | Mittel |
| Portugal | ~300k € | -33% (150k €) | Gering |

---

## 6. Nächste Schritte

1. **EoR-Partner evaluieren** (Remote.com, Deel, Oyster)
2. **Job Descriptions** für Krakau/Wrocław vorbereiten
3. **Recruiter in Polen** kontaktieren (z.B. Antal, Hays)
4. **Erste Interviews** in 2-3 Wochen starten
5. **Serbien-Option** für Monat 6 prüfen

---

## Quellen

- Eurostat 2024: Arbeitskosten IT-Sektor
- Stack Overflow Developer Survey 2024
- Numbeo Cost of Living Index
- World Bank Ease of Doing Business
- Glassdoor Salary Data 2024/2025

---

*Generiert mit EBF Framework v1.18 | Session: EBF-S-2026-01-26-ORG-001*
