# EBF Session Report: economiesuisse Referendum Dynamics Model

**Session-ID:** EBF-S-2026-01-30-POL-001
**Kunde:** economiesuisse
**Projekt:** PRJ-ECOS-001 (10 Millionen Schweiz Initiative)
**Modus:** STANDARD
**Datum:** 2026-01-30

---

## Executive Summary

Dieses Dokument fasst die Model-Building Session für das economiesuisse Referendum Dynamics Model (RDM-X) zusammen. Das Modell wurde auf Basis historischer Volksabstimmungsdaten kalibriert und prognostiziert einen Nein-Anteil von **64% [57-71%]** bei einer Standard-Kampagne.

---

## 1. Kontext

### 1.1 Aufgabenstellung
Entwicklung eines Forecast-Modells für das Referendum «10 Millionen Schweiz» (SVP-Initiative) mit folgenden Zielen:
- Vorhersage des Abstimmungsergebnisses
- Testing verschiedener Kampagnen-Strategien
- Simulation von Interventionswirkungen

### 1.2 Ψ-Dimensionen
| Dimension | Relevanz | Beschreibung |
|-----------|----------|--------------|
| Ψ_I | 0.95 | Institutionell: Direkte Demokratie, Konkordanz |
| Ψ_S | 0.75 | Sozial: Regionale Identität, Peer Effects |
| Ψ_K | 0.70 | Kulturell: Unabhängigkeit, Identitätspolitik |
| Ψ_C | 0.55 | Kognitiv: Komplexität, Status-Quo-Bias |
| Ψ_E | 0.80 | Ökonomisch: Arbeitsplatz, Wohnungsmarkt |
| Ψ_T | 0.65 | Temporal: Kampagnenphasen |
| Ψ_M | 0.70 | Material: Kanäle (TV, Social Media) |
| Ψ_F | 0.60 | Physisch: Briefwahl |

### 1.3 10C-Dimensionen
- **Primär:** WHO (Wähler-Segmente), WHAT (Utility), WHEN (Timing), AWARE (Informiertheit)
- **Sekundär:** HOW (Komplementarität), READY (Mobilisierung), STAGE (Journey)
- **Extended:** WHERE (Parameter-Quellen)

---

## 2. Modell

### 2.1 Modell-Auswahl
**Gewählt:** M4 Custom (RDM-X) basierend auf M3 Hybrid

**Komponenten:**
- Dynamischer Bayesian Forecast (Zeitreihen)
- Segment-basierte Persuasion (4 Segmente)
- 10 Interventionstypen mit Decay-Funktionen
- Historische Kalibrierung (BCM2_07_ABS)

### 2.2 Segmente
| Segment | Anteil | Persuadability | λ | Position |
|---------|--------|----------------|---|----------|
| SEG-WIRTSCHAFT | 25% | 0.10 | 2.20 | Nein (fix) |
| SEG-MITTE | 30% | 0.70 | 2.50 | Unentschieden |
| SEG-BESORGT | 25% | 0.40 | 2.80 | Tendenz Ja |
| SEG-SVP | 20% | 0.05 | 3.00 | Ja (fix) |

### 2.3 Funktionale Form
```
V_t(Nein) = V_{t-1} + Δ_campaign + Δ_media + Δ_events + ε_t

Wobei:
- Δ_campaign = Σᵢ (αᵢ × σ_seg × π_t × exp(-δᵢ × t))
- π_t = Meinungsbildungs-Intensität pro Phase
- δᵢ = Decay-Rate nach Interventions-Horizont
```

---

## 3. Parameter

### 3.1 Baseline (aus BCM2_07_ABS)
| Referenz | Resultat | Ähnlichkeit | Gewicht |
|----------|----------|-------------|---------|
| Begrenzung 2020 | 61.7% Nein | 0.92 | 40% |
| MEI 2014 | 49.7% Nein | 0.85 | 30% |
| Ecopop 2014 | 74.1% Nein | 0.78 | 20% |
| 13. AHV 2024 | 41.8% Nein | 0.55 | 10% |

**V₀ = 58.6% [51%, 66%]**

### 3.2 Interventions-Effektivität (α)
| Intervention | α (PP) | CI | Quelle |
|--------------|--------|-----|--------|
| GOTV Mobilisierung | +2.5 | ±1.2 | BCM2_07_ABS |
| Lokale Testimonials | +2.0 | ±1.0 | Cialdini |
| KMU-Botschafter | +1.8 | ±0.7 | BCM2_07_ABS |
| Information Salience | +1.5 | ±0.8 | BCM2_07_ABS |
| Empathie-Messaging | +1.5 | ±0.7 | Fehr |
| Loss/Gain Framing | +1.2 | ±0.5 | Kahneman |
| Social Proof | +1.2 | ±0.6 | Profile |
| TV-Arena | +1.0 | ±0.8 | BCM2_07_ABS |
| Fact-Checking | +0.8 | ±0.5 | Nyhan |
| Paid Social | +0.5 | ±0.4 | Profile |

### 3.3 Dynamische Parameter
| Phase | π | Zeitraum |
|-------|---|----------|
| Early | 0.15 | >6 Wochen |
| Mid | 0.35 | 4-6 Wochen |
| Late | 0.60 | 2-4 Wochen |
| Final | 0.85 | <2 Wochen |

---

## 4. Ergebnisse

### 4.1 Szenarien
| Szenario | V(Nein) | CI | Beschreibung |
|----------|---------|-------|--------------|
| A: Minimal | 58.7% | [52%, 65%] | Nur Basics |
| **B: Standard** | **64.1%** | **[57%, 71%]** | **Empfehlung** |
| C: Intensiv | 62.0% | [54%, 70%] | Sättigung |
| D: Risiko | 60.1% | [52%, 68%] | SVP stark |

### 4.2 Sensitivität
| Parameter | Einfluss | Robustheit |
|-----------|----------|------------|
| V₀ (Baseline) | 45% | Mittel |
| α_gotv | 28% | Hoch |
| E_gegner | 22% | Niedrig |
| σ_seg | 5% | Hoch |

### 4.3 Robustheit
- 95% Runs: V(Nein) > 50% ✓
- 80% Runs: V(Nein) > 55% ✓
- 60% Runs: V(Nein) > 60% ✓

---

## 5. Strategische Empfehlung

### 5.1 Prioritäten
1. **GOTV (α=+2.5):** Mobilisierung ist Schlüssel
2. **Lokale Testimonials (α=+2.0):** KMU-Gesichter, regionale Botschafter
3. **Empathie-Messaging (α=+1.5):** Sorgen ernst nehmen

### 5.2 Vermeiden
- Übersättigung (Szenario C weniger effektiv als B)
- Reine Wirtschaftsargumente bei SEG-BESORGT
- Finanzielle Anreize (Crowding-Out)

### 5.3 Timing
| Phase | Aktion |
|-------|--------|
| >6W | Narrative aufbauen, KMU-Netzwerk aktivieren |
| 4-6W | Testimonial-Kampagne starten |
| 2-4W | Empathie-Messaging intensivieren |
| <2W | GOTV maximieren |

---

## 6. Datenquellen

- **BCM2_07_ABS_volksabstimmungen.yaml:** Historische Kalibrierung
- **economiesuisse_profile.yaml:** STANDARD 400 Faktoren
- **BFS Abstimmungsstatistik:** Offizielle Resultate
- **gfs.bern / Sotomo:** Umfragedaten
- **bcm_master.bib:** Wissenschaftliche Literatur

---

## 7. Modell-Registrierung

**ID:** MOD-015
**Name:** Referendum Dynamics Model Extended (RDM-X)
**Version:** 2.0
**Pfad:** data/model-registry.yaml

---

## Anhang: Session-Verlauf

| Schritt | Status | Output |
|---------|--------|--------|
| 0: Session | ✅ | EBF-S-2026-01-30-POL-001 |
| 1: Kontext | ✅ | 8 Ψ-Dimensionen |
| 2: Modell | ✅ | M4 Custom RDM-X |
| 3: Parameter | ✅ | BCM2_07_ABS + Profile |
| 4: Analyse | ✅ | V(Nein) = 64% [57-71%] |
| 5: Intervention | ✅ | Archiviert (completed) |
| 6: Bericht | ✅ | Dieses Dokument |
| 7: Sichern | ⏳ | Pending |
| 8: Qualität | ⏳ | Pending |
| 9: Output | ⏳ | Pending |

---

*Erstellt: 2026-01-30*
*Framework: EBF Evidence-Based Framework v1.22*
*https://claude.ai/code/session_01BNKy1t1mhnVh3WCXZHFdG8*
