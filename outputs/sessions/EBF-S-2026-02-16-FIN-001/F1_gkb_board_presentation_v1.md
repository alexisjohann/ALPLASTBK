# GKB Bankrat-Praesentation: Digitale Transformation & Kundenvertiefung

> **Erstellt:** 2026-02-16 | **Session:** EBF-S-2026-02-16-FIN-001
> **Modell:** GKB001-ODE-v1.0 | **Provenance:** Layer 1 (deterministic)
> **Zielgruppe:** GKB Bankrat (D1=0.4, D4=0.2)

---

## SLIDE 1: Ausgangslage

### Die GKB steht vor einer strategischen Transformation

| Staerke | Herausforderung |
|---------|-----------------|
| Staatsgarantie + AA-Rating | Zinsabhaengigkeit 67.5% |
| 45% Hypothekarmarktanteil | Margendruck + Neobanken |
| 156 Jahre Vertrauen | Konservative Kultur bremst |
| 1'000 MA, 45 Filialen | Digitalisierung erst im Aufbau |
| Buendner Identitaet (0.85) | AI/ML-Reife nur 0.35 |

**Kernfrage:** Wie schnell kann sich die GKB transformieren — und welche Massnahmen wirken am staerksten?

---

## SLIDE 2: Unser Ansatz — Evidenz-basierte Simulation

### 350 Kontextfaktoren → Mathematisches Modell → 12-Monats-Prognose

```
8 GKB-Kontextdateien          Verhaltens-Dynamik-Modell          Prognose
─────────────────────    →    ───────────────────────────    →    ──────────
Strategie (67 Faktoren)       6 Zustaende:                       12-Monats-
People (84 Faktoren)          • Adoption (A)                     Trajektorie
Technology (45 Faktoren)      • Widerstand (R)                   + Counterfactual
Use Cases (28 Faktoren)       • Gewohnheit (H)                   + Vergleich
Finanzen (52 Faktoren)        • Momentum (M)                     mit 2 anderen
Kultur (74 Faktoren)          • Entscheidung (D)                 Branchen
                              • Nutzen (U)
```

**Methode:** ODE-Simulation (Euler-Integration), validiert an 10 Literaturquellen, 35 automatisierte Tests bestanden.

---

## SLIDE 3: GKB-Dynamik-Profil

### Die GKB ist ein «Slow Transformation»-Typ

| Parameter | GKB | Benchmark | Bedeutung |
|-----------|-----|-----------|-----------|
| **Adoptionsrate** | **0.30** | 0.40-0.50 | Langsamste Uebernahme neuer Prozesse |
| **Widerstandsabbau** | **0.025** | 0.03-0.04 | Tradition baut sich am langsamsten ab |
| **Crowding-Out Risiko** | **-0.10** | -0.15 bis -0.20 | **Geringestes Risiko** — Stabilitaet als Vorteil |
| **Rueckschlag-Sensitivitaet** | **0.12** | 0.15-0.20 | **Am wenigsten empfindlich** gegenueber Fehlern |
| **Purpose-Zerfall** | **0.02** | 0.02-0.03 | Kantonalbank-Mandat nahezu erosionsresistent |

**Fazit:** Die GKB transformiert sich langsamer, aber die Ergebnisse sind nachhaltiger und stabiler.

---

## SLIDE 4: Simulationsergebnis — 12-Monats-Prognose

### Adoption steigt von 10% auf 27%, Widerstand sinkt nur langsam

| Kennzahl | Start | 12 Monate | Veraenderung |
|----------|-------|-----------|--------------|
| **Adoption** | 10.0% | **26.9%** | +16.9pp |
| **Widerstand** | 60.0% | 58.4% | -1.6pp |
| **Entscheidungsfaehigkeit** | 25.0% | **45.7%** | +20.7pp |
| **Gesamtbereitschaft** | 17.0% | **27.0%** | +10.0pp |

### Phasen-Prognose

| Phase | Schwellenwert | Prognose |
|-------|---------------|----------|
| **Kick-off → Umsetzung** | 25% Readiness | **Monat 10** |
| Umsetzung → Skalierung | 55% Readiness | ~Monat 26 |
| Skalierung → Integration | 80% Readiness | ~Monat 40+ |

**Botschaft:** Die GKB braucht 10 Monate bis zum Phasenuebergang. Das ist laenger als andere Branchen — aber normal fuer eine 156-jaehrige Kantonalbank.

---

## SLIDE 5: Branchenvergleich — Wo steht die GKB?

### 3-Wege-Vergleich mit Bau (Zindel) und Medien (RMS)

| Metrik | Bau (Zindel) | Medien (RMS) | **Banking (GKB)** |
|--------|-------------|-------------|-------------------|
| Adoption nach 12 Mo. | 32.1% | **47.5%** | 26.9% |
| Widerstand nach 12 Mo. | 56.7% | **52.9%** | 58.4% |
| Gesamtbereitschaft | 28.4% | **37.4%** | 27.0% |
| Momentum (Peak) | 10.7% | **19.3%** | 10.2% |

### Geschwindigkeit vs. Stabilitaet

```
     GESCHWINDIGKEIT
          ↑
          |  RMS (Medien) — schnell, aber fragil
          |
          |  Zindel (Bau) — mittleres Tempo
          |
          |  GKB (Banking) — langsam, aber stabil
     ─────┼─────────────────────→ STABILITAET
```

**Erkenntnis:** Die GKB hat das geringste Crowding-Out-Risiko und die niedrigste Rueckschlag-Empfindlichkeit aller 3 Cases. Langsamkeit ist hier KEIN Nachteil — sondern reflektiert institutionelle Stabilitaet.

---

## SLIDE 6: Interventions-Wirkung — Was wirkt am staerksten?

### Counterfactual-Analyse: 4 geplante Interventionen

| Intervention | Adoption OHNE | Impact | Anteil |
|-------------|---------------|--------|--------|
| INT-GKB-003: **Plattform Cross-Selling** | 20.3% | **-6.7pp** | **96%** |
| INT-GKB-004: Lebensmitte-Check Gen X | 26.7% | -0.3pp | 4% |
| INT-GKB-001: Unternehmer-Kontostruktur | 26.8% | -0.1pp | <1% |
| INT-GKB-002: Zweitwohnungsbesitzer | 27.0% | -0.0pp | <1% |
| **Alle 4 zusammen** | **20.0%** | **-7.0pp** | **100%** |

### Warum dominiert INT-GKB-003?

INT-GKB-003 (Plattform-Kunden Cross-Selling) wirkt direkt auf die **Adoptionsrate** — den primaeren Engpass in der Kick-off-Phase. Die anderen 3 Interventionen wirken auf sekundaere Parameter (Utility-Wachstum, Momentum), die erst in spaeteren Phasen dominant werden.

---

## SLIDE 7: Was passiert OHNE die Interventionen?

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  MIT Interventionen:                                            │
│  Adoption 26.9%  │  Readiness 27.0%  │  Phasenuebergang Mo.10  │
│                                                                 │
│  OHNE Interventionen:                                           │
│  Adoption 20.0%  │  Readiness ~21%   │  Phasenuebergang Mo.16+ │
│                                                                 │
│  DELTA:                                                         │
│  -7.0pp Adoption │  ~-6pp Readiness  │  +6 Monate Verzoegerung │
│                                                                 │
│  → Ohne Massnahmen: 6 Monate laengere Kick-off-Phase           │
│  → Das kostet Zeit, Momentum und Glaubwuerdigkeit               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SLIDE 8: Die Buendner Identitaet als staerkster Hebel

### Kulturelle Elastizitaet = 1.05 (hoechster Wert)

Die Buendner Identitaet ist der staerkste Multiplikator im gesamten Modell. Sie wirkt in **beide Richtungen:**

| Als **Asset** | Als **Barriere** |
|---------------|------------------|
| Stolz auf Institution (0.85) | «Mir hend das scho immer so gmacht» |
| 75% MA aus Graubuenden | Widerstand gegen Externe |
| 156 Jahre Erfolgsgeschichte | Pfadabhaengigkeit |
| Starke Teamkultur (Clan) | Hierarchie bremst Innovation |

### Das Narrativ entscheidet

```
FALSCH:  "Die GKB muss sich modernisieren TROTZ ihrer Tradition."
         → Aktiviert Widerstand (Identitaetsbedrohung)

RICHTIG: "Die GKB modernisiert sich WEIL sie buendnerisch ist."
         → Nutzt Identitaet als Antrieb
         → Praezedenz: Strom-Finanzierung, Tourismus-Aufbau
```

---

## SLIDE 9: 4 Empfehlungen fuer den Bankrat

### Basierend auf der Simulation und dem 3-Wege-Vergleich

| # | Empfehlung | Timing | Begruendung aus Modell |
|---|------------|--------|------------------------|
| **1** | **INT-GKB-003 priorisieren** (Plattform Cross-Selling) | **Q2 2026** | 96% des Adoptions-Impacts, wirkt auf Engpass beta_adoption |
| **2** | **3-5 Lighthouse-Filialen** als Digital-Vorbilder | Q2-Q3 2026 | Soziale Elastizitaet (0.85) → Clan-Kultur uebertraegt Erfolge |
| **3** | **Buendner Narrativ** aktiv kommunizieren | Ab sofort | Kulturelle Elastizitaet (1.05) ist staerkster Multiplikator |
| **4** | **18-36 Monate Zeithorizont** akzeptieren | Strategisch | GKB ist «Slow Transformation» — aber nachhaltiger als schnelle Branchen |

### Sequenzierung

```
Q2 2026:  INT-GKB-003 starten + Lighthouse-Filialen designen
Q3 2026:  INT-GKB-004 (Lebensmitte-Check) nachlegen
Q3-Q4:    INT-GKB-001 + INT-GKB-002 parallel
Q4 2026:  Erste Ergebnisse Lighthouse → kommunizieren
2027:     Skalierung auf alle 45 Filialen beginnen
```

---

## SLIDE 10: Zusammenfassung — Die GKB-Transformation

### 5 Kernbotschaften fuer den Bankrat

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. LANGSAM IST NICHT SCHLECHT                                  │
│     Die GKB transformiert sich langsamer als Medien oder Bau,   │
│     aber die Ergebnisse sind stabiler und nachhaltiger.         │
│                                                                 │
│  2. PLATTFORM CROSS-SELLING IST DER SCHLUESSEL                 │
│     INT-GKB-003 treibt 96% des Adoptions-Impacts.              │
│     Mit Q2-Start gewinnen wir 6 Monate gegenueber Abwarten.    │
│                                                                 │
│  3. BUENDNER IDENTITAET NUTZEN, NICHT BEKAEMPFEN               │
│     psi_K = 1.05 ist der staerkste Multiplikator im Modell.    │
│     Das Narrativ «Modernisierung WEIL buendnerisch» ist         │
│     entscheidend.                                               │
│                                                                 │
│  4. STAATSGARANTIE ALS TRANSFORMATIONS-PUFFER                   │
│     Geringstes Crowding-Out-Risiko aller 3 Cases.              │
│     Wir koennen Spar- und Transformationsmassnahmen             │
│     PARALLELER durchfuehren.                                    │
│                                                                 │
│  5. 18-36 MONATE BIS SUBSTANTIELLE ERGEBNISSE                  │
│     Phasenuebergang bei Monat 10, Skalierung ab Monat 26.      │
│     Das entspricht dem Rhythmus einer 156-jaehrigen             │
│     Institution.                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technischer Anhang

| Aspekt | Detail |
|--------|--------|
| **Modell** | GKB001-ODE-v1.0: 6-Zustands ODE mit Euler-Integration |
| **Kontextfaktoren** | 350 (aus 8 CVA-Dateien der GKB) |
| **Literaturquellen** | 10 (Kahneman, Cialdini, Deci & Ryan, Bass, Rogers, etc.) |
| **Parameter-SSOT** | `data/customers/gkb/kontextvektoren/GKB001_ODE_parameters.yaml` |
| **Simulation** | `python scripts/ode_simulator.py --customer gkb --project GKB001 --months 12` |
| **Counterfactual** | `python scripts/ode_simulator.py --customer gkb --project GKB001 --months 12 --counterfactual INT-GKB-001 INT-GKB-002 INT-GKB-003 INT-GKB-004` |
| **Tests** | 35/35 bestanden |
| **Provenance** | Layer 1 (susceptibility = 0.0) — deterministische Berechnung |
| **Vergleichscases** | Zindel United (Bau, ZIN003), Ringier Medien (MED, RMS001) |

---

> **FehrAdvice & Partners AG** | Prof. Ernst Fehr
> Evidence-Based Framework (EBF) | Session EBF-S-2026-02-16-FIN-001
