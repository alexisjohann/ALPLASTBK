# Churn-Dekompositionsmodell: Helvetia Baloise Post-Fusion

> Erstellt: 11.02.2026 | FehrAdvice & Partners AG
> Kontext: Session-Vorbereitung Leitidee-Evaluation
> Teilnehmer: Manuel Fischer-Aerni (FA), Michèle Erhardt (Marktforschung), Yves Thiriet

---

## Juristische Ausgangslage

Kunden können **NICHT** wegen der Fusion kündigen. Bestehende Verträge bleiben gültig (Beobachter.ch, 2025).

Kunden **KÖNNEN** kündigen bei:
- Prämienerhöhung (Sonderkündigungsrecht)
- Regulärem Vertragsablauf
- Schadenfall (je nach Vertrag)

**Konsequenz:** Die Fusion ist kein direkter Churn-Treiber, sondern ein **Multiplikator**, der alle anderen Treiber verstärkt. Sie senkt die Toleranzschwelle, bei der andere Trigger zur Kündigung führen.

---

## Basisgleichung

```
Churn_total = Churn_baseline × ∏ᵢ Amplifier(Triggerᵢ)
```

---

## Die 6 Churn-Treiber

### Übersicht

| # | Treiber | Direkter Anteil | Amplifier durch Fusion | Evidenz-Stärke |
|---|---------|:--------------:|:---------------------:|:--------------:|
| 1 | **Prämienerhöhung** | 40% | ×1.4 | ★★★★ |
| 2 | **Service-Bruch / Berater:innen-Wechsel** | 25% | ×1.6 | ★★★ |
| 3 | **Wettbewerber-Abwerbung** | 15% | ×1.3 | ★★★ |
| 4 | **Identitätsverlust (Ex-Baloise)** | 10% | ×2.0 | ★★ |
| 5 | **Vertrauensverlust (Medien)** | 5% | ×1.5 | ★★ |
| 6 | **Change Fatigue** | 5% | ×1.2 | ★★ |

### Treiber 1: Prämienerhöhung (40%)

**Evidenz-Basis: ★★★★ (stark)**

| Datenpunkt | Wert | Quelle |
|-----------|------|--------|
| Preiselastizität CH Versicherung | **-2.0** | PubMed Meta-Studie (2014) |
| Wechselbereitschaft bei >CHF 30/Mt Erhöhung | **72%** | Moneyland 2026 |
| Prämie als Wechselgrund Nr. 1 | **67%** | Deloitte 2025 |
| Durchschnittliche Prämienerhöhung 2026 | **+4.4%** | Comparis |
| Effektive Erhöhung günstigste Optionen | **~7%** (+CHF 23/Mt) | Comparis |

- Einziger Treiber mit **Sonderkündigungsrecht**
- Martin Jara hat höhere Prämien öffentlich angekündigt (BILANZ)
- Unsicherheit: ±8% (Range: 32-48%)

### Treiber 2: Service-Bruch / Berater:innen-Wechsel (25%)

**Evidenz-Basis: ★★★ (mittel-stark)**

- Bain M&A-Studie: Service-Bruch = primärer Churn-Treiber bei Fusionen
- Herhausen et al. 2019 (PAR-CJ-001): β_JS = 0.58 bei Multi-Touchpoint-Kunden
- Helvetia-spezifisch: 1'400-1'800 CH-Stellen fallen weg
- ABER: «Berater:innen nicht vom Abbau betroffen» (Helvetia-Kommunikation)
- Risiko trotzdem: IT-Integration → Systemausfälle → Service-Bruch
- Unsicherheit: ±7% (Range: 18-32%)

### Treiber 3: Wettbewerber-Abwerbung (15%)

**Evidenz-Basis: ★★★ (mittel-stark)**

- JD Power 2025: 57% der Kunden vergleichen aktiv (vs. 49% in 2024)
- Bain: 3× höhere Switching-Wahrscheinlichkeit nach Fusion
- Mobiliar («persönlichste»), AXA werden gezielt abwerben
- Comparis/Moneyland machen Wechsel einfach (κ_switching↓)
- Unsicherheit: ±5% (Range: 10-20%)

### Treiber 4: Identitätsverlust — Ex-Baloise (10%)

**Evidenz-Basis: ★★ (mittel)**

- Akerlof/Kranton 2000 (MS-IB-001): U_IDN → 0 bei Brand-Mismatch
- KEIN Sonderkündigungsrecht → wirkt erst bei nächstem Trigger
- Betrifft primär SEG-04 (~10% des Bestands, LLMMC-Prior)
- Wirkt als stärkster Amplifier (×2.0)
- Unsicherheit: ±5% (Range: 5-15%)

### Treiber 5: Vertrauensverlust durch Medien (5%)

**Evidenz-Basis: ★★ (mittel)**

- Stellenabbau 2'600 → SRF/NZZ/Blick Berichterstattung negativ
- Festinger 1957: Kognitive Dissonanz (Markenbotschaft ≠ Realität)
- Kein direkter Kündigungsgrund, aber erodiert Bleibe-Motivation
- Unsicherheit: ±3%

### Treiber 6: Change Fatigue (5%)

**Evidenz-Basis: ★★ (mittel)**

- φ_fatigue = 0.65 (CVA-SCHNELL)
- 18 Monate Unsicherheit seit Fusionsankündigung (Sept 2024)
- Kein direkter Kündigungsgrund
- Unsicherheit: ±3%

---

## Amplifier-Mechanismus

Die Fusion verschiebt den **Referenzpunkt** (Prospect Theory, Kahneman & Tversky 1979):

```
OHNE FUSION:
Referenz = «Ich bin Helvetia-Kunde, alles stabil»
→ Prämienerhöhung = kleiner Verlust vs. stabiler Status Quo

MIT FUSION:
Referenz = «Alles ist unsicher, Fusion, Stellenabbau»
→ Prämienerhöhung = NOCH EIN Verlust in einer Serie
→ Kumulation: λ_kumuliert > λ_einzeln
→ «Jetzt reicht's» Schwelle wird schneller erreicht
```

**Formalisierung:**

```
λ_eff = λ_base × (1 + Σ offene_verluste)

Ohne Fusion:  λ_eff = 2.25 × (1 + 0)   = 2.25
Mit Fusion:   λ_eff = 2.25 × (1 + 0.3) = 2.93
Ex-Baloise:   λ_eff = 2.25 × (1 + 0.6) = 3.60
```

---

## Szenario-Analyse

**Basis: ~5 Mio. Kunden (CH kombiniert), Baseline Churn: ~7%/Jahr (Deloitte)**

| Szenario | Amplifier | Churn-Rate | Kunden (24 Mt) | Haupttreiber |
|----------|:---------:|:----------:|:--------------:|-------------|
| **A: Best Case** | ×1.1 | ~8% | 400'000 | Prämie moderat (+3%), Service stabil |
| **B: Base Case** | ×1.4 | ~10% | 500'000 | Prämie +4.4%, IT-Probleme moderat |
| **C: Stress Case** | ×1.8 | ~13% | 650'000 | Prämie +7%, IT-Panne sichtbar |
| **D: Worst Case** | ×2.5 | ~18% | 900'000 | Alles gleichzeitig + Cascading |

**Erwartungswert:** ~10% (500'000 Kunden in 24 Monaten)
**Range:** 8-18% (400'000-900'000)

---

## 5 weitere Verhaltenseffekte (jenseits Churn)

| # | Effekt | Mechanismus | Messgrösse | Risiko |
|---|--------|------------|-----------|:------:|
| 1 | **Downgrading** | Kunden kündigen nicht, aber reduzieren Policen (3a→weg, Zusatz→weg). Unsichtbar in Churn-Statistik. | Revenue/Kunde sinkt 10-20% | ●●●●○ |
| 2 | **Cross-Selling-Blockade** | Fusion = Chance für mehr Produkte. Aber: Kunden in Unsicherheit kaufen NICHTS dazu. | Policen/Kunde stagniert | ●●●○○ |
| 3 | **NPS-Erosion** | Kunden bleiben, aber empfehlen nicht mehr. Langfrist-Akquisition bricht ein. | NPS sinkt 10-20 Punkte | ●●●●○ |
| 4 | **Mitarbeiter-Demotivation → Service-Abfall** | 22'000 MA sind Markenbotschafter. Demotivation → Service↓ → Kunden merken es. | eNPS, CSAT korreliert | ●●●●● |
| 5 | **Fairness-Verletzung (Preis-Framing)** | «Die sparen CHF 350 Mio. Synergien und ICH soll mehr bezahlen?» Fehr/Schmidt Inequity Aversion (MS-SP-001), α_i ≈ 0.6 | Zahlungsbereitschaft sinkt | ●●●○○ |

### Fairness-Effekt im Detail

```
KUNDEN-LOGIK (Fehr/Schmidt Inequity Aversion):

  Helvetia + Baloise = CHF 350 Mio. Synergien/Jahr
                    +
  2'600 Stellen werden abgebaut
                    =
  «Die sparen Hunderte Millionen»
                    +
  «Und ICH soll MEHR bezahlen?!»
                    =
  Inequity Aversion → Empörung → Wechselbereitschaft ↑↑↑
```

---

## Implikationen für die Leitidee

Die Leitidee muss deshalb:

1. **Preiserhöhung als FAIR rahmen** — nicht ignorieren, sondern adressieren: «Mehr Schutz» statt «mehr Kosten»
2. **Service-Kontinuität versprechen** — und halten: «Ihr:e Berater:in bleibt»
3. **Identitätsverlust abfedern** — Basilisk sichtbar integrieren
4. **Wettbewerbern das Narrativ wegnehmen** — eigenes Territorium besetzen bevor Mobiliar/AXA angreifen

---

## Was Marktforschung hier NICHT sieht

| Blinder Fleck | Warum unsichtbar | BEATRIX-Beitrag |
|--------------|-----------------|----------------|
| Downgrading (stille Erosion) | Keine Kündigung = kein Signal | Segment-spezifische Revenue-Prognose |
| NPS-Erosion | Wird erst in 6-12 Monaten sichtbar | Predictive NPS aus Verhaltensdaten |
| Fairness-Verletzung | Nicht abgefragt in Standard-Tests | Fehr/Schmidt Modell (α_i Parameter) |
| Amplifier-Effekt | Fusion wird als «gegeben» behandelt | Referenzpunkt-Verschiebung modelliert |
| Segment-Heterogenität | Durchschnitt über alle Kunden | 4 separate Segment-Prognosen |

---

## Datenquellen

| Quelle | Datenpunkt | Jahr |
|--------|-----------|------|
| Deloitte Swiss Health Insurance | Wechselquote 7-12%, 67% wegen Prämie | 2025 |
| Moneyland | 72% bei >CHF 30/Mt, Sparpotenzial | 2026 |
| Comparis | Prämienprognose +4.4% bzw. +7% | 2026 |
| Bain & Company | Post-Merger Attrition 20-30%, 3× Likelihood | 2023 |
| JD Power | 57% vergleichen aktiv, 29% wechselten (US Auto) | 2025 |
| PubMed Systematic Review | Preiselastizität CH: -2.0 | 2014 |
| Beobachter.ch | Kein Sonderkündigungsrecht bei Fusion | 2025 |
| Herhausen et al. | Journey Satisfaction β_JS = 0.58 | 2019 |
| Akerlof & Kranton | Identity Economics, U_IDN | 2000 |
| Fehr & Schmidt | Inequity Aversion, α_i | 1999 |
| BILANZ / Martin Jara | Höhere Prämien angekündigt | 2026 |

---

## Parameter-Transparenz

Alle Gewichtungen (40%, 25%, 15%, 10%, 5%, 5%) und Amplifier (×1.1 bis ×2.5) sind **LLMMC-Priors (Tier 2)**, kalibriert an den oben genannten Datenquellen. Sie sind KEINE exakten Messungen und sollten mit Helvetia-internen Daten (NPS, Segmentierung, Churn-Historie) kalibriert werden.

**Sensitivität:** Die Rangfolge der Treiber (Prämie > Service > Wettbewerber > Identität > Vertrauen > Fatigue) ist robust unter realistischen Parameter-Variationen. Die exakten Prozentsätze können sich verschieben, die Richtung der Empfehlungen bleibt stabil.
