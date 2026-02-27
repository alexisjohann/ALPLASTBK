# Pre-Commitment: Nudge Energiesparen CH

**Status: 🔒 LOCKED – Do not modify after commit**
**Locked at:** 2026-02-12T08:24:53.831940Z
**Author:** gerhard.fehr@fehradvice.com

## 1. Fragestellung
Führt die Änderung der Default-Heiztemperatur von 21°C auf 20°C in Schweizer Haushalten zu einer messbaren Reduktion des Energieverbrauchs ohne signifikante Einbußen bei der Zufriedenheit?

## 2. Kontext-Hypothese (BCM/Ψ)
**BCM-Erwartung:** Default-Effekt reduziert Energieverbrauch um 8-15% bei hoher Akzeptanz (>70%)

**Beteiligte Ψ-Dimensionen:**
- **Status Quo Bias (Ψ₁):** Haushalte bleiben bei 20°C Default
- **Effort Aversion (Ψ₂):** Manuelle Anpassung wird vermieden
- **Loss Aversion (Ψ₃):** Komfortverlust wird übergewichtet → potenzielle Reaktanz
- **Social Proof (Ψ₄):** "20°C ist normal" wird kommuniziert

**Hypothese:** Default-Änderung reduziert Heizenergieverbrauch um mindestens 10% bei <30% Override-Rate.

## 3. Methode
**Design:** Randomized Controlled Trial (RCT)
- **Treatment:** Default 20°C (n=500 Haushalte)
- **Control:** Default 21°C (n=500 Haushalte)
- **Dauer:** 6 Monate (Oktober 2026 - März 2027)
- **Randomisierung:** Stratifiziert nach Wohnfläche und Gebäudealter
- **Messungen:** Smart Meter Daten (täglich) + 3 Surveys (Pre/Mid/Post)

## 4. Vorab definierte Erfolgskriterien
**Primärer Endpunkt:**
- Energieeinsparung ≥10% vs. Kontrollgruppe (adjustiert für Außentemperatur)

**Sekundäre Endpunkte:**
- Override-Rate <30% in Treatment-Gruppe
- Zufriedenheit-Score ≥4.0/5.0 (vs. ≥4.2 in Kontrollgruppe)
- Kosten-Nutzen-Verhältnis: €/tCO₂ <100 CHF

**Effektstärke:** Cohen's d ≥0.4 für Energieverbrauch-Differenz

## 5. Planned Checks
**Robustness Checks:**
- Analyse mit/ohne Außentemperatur-Adjustierung
- Subgruppen-Analyse: Mieter vs. Eigentümer
- Sensitivitätsanalyse für Ausreißer (>3 SD)
- Intent-to-Treat vs. Per-Protocol-Analyse

**Alternative Erklärungen:**
- Hawthorne-Effekt: Vergleich erste vs. letzte 2 Monate
- Selection Bias: Baseline-Charakteristika-Vergleich
- Spillover-Effekte: Geografische Cluster-Analyse

## 6. Datenquellen
- **Smart Meter:** Stündlicher Gasverbrauch (Primärdaten)
- **Wetterdaten:** MeteoSchweiz API (Heizgradtage)
- **Surveys:** Qualtrics (Zufriedenheit, Komfort, Override-Verhalten)
- **Gebäudedaten:** GWR-Register (Wohnfläche, Baujahr, Isolation)

## 7. Timeline
- **Feb 2026:** Rekrutierung und Randomisierung
- **Mär 2026:** Baseline-Survey und Smart Meter Installation
- **Apr-Sep 2026:** Vorlaufphase (beide Gruppen 21°C)
- **Okt 2026:** Treatment-Start (Default-Änderung)
- **Jan 2027:** Mid-Survey
- **Mär 2027:** Projekt-Ende, Post-Survey
- **Apr 2027:** Datenanalyse und BFE-Report

## 8. Potential Concerns
**Methodische Risiken:**
- Drop-out Rate >20% gefährdet Power (n=400 pro Gruppe minimum)
- Reaktanz bei Default-Änderung könnte zu Überheizen führen
- Smart Meter Ausfälle reduzieren Datenqualität

**Externe Validität:**
- Sample-Bias: Freiwillige Teilnahme (vermutlich umweltbewusster)
- Generalisierbarkeit auf Gesamtschweiz fraglich (nur 3 Kantone)
- Einmaliger Winter: Wetterextreme könnten Effekte überlagern

**Ethische Überlegungen:**
- Informed Consent ohne Details über Default-Manipulation
- Möglicher Komfortverlust bei vulnerablen Haushalten (Senioren)