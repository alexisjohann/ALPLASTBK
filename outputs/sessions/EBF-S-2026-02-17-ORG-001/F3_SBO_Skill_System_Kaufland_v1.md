# Kaufland Skill-System: Feingranulare Architektur fuer 170'000 Mitarbeitende

**Modell:** MOD-ORG-SBO-001 v1.1 | **Taxonomie:** STAX-KAUF-001 | **Datum:** 17. Februar 2026

**FehrAdvice & Partners AG** | Prof. Ernst Fehr

---

## Executive Summary

Ein Grosskonzern wie Kaufland mit ~170'000 Mitarbeitenden in 1'500+ Filialen, Zentrallagern und Zentralfunktionen braucht ein feingranulares, datengetriebenes Skill-System. Die hier praesentierte Architektur umfasst:

- **120 einzelne Skills** in 9 Domains und 28 Clustern
- **22 Rollenprofile** ueber 3 Job-Familien (Filiale, Logistik, Zentrale)
- **Matching-Algorithmus** mit Mandatory Gate und gewichtetem Fit-Score
- **Karrierepfad-Matrix** mit Uebergangswahrscheinlichkeiten und Skill-Gap-Analyse
- **Autor-Klassifikation** jedes Skills nach 5 Aufgabentypen (Routine, Manual, Interactive, Abstract, Leadership)

Das System ermoeglicht praezise Person-Job-Zuordnung, evidenzbasierte Personalentwicklung und vorausschauende Nachfolgeplanung.

---

## 1. Warum feingranular? Das Problem der groben Kategorien

### 1.1 Status quo: Stellenbeschreibungen als Sackgasse

Traditionelle Stellenbeschreibungen definieren Jobs ueber:
- Titel (*«Fachverkaeufer:in Frische»*)
- Ausbildung (*«Ausbildung Einzelhandel»*)
- Erfahrung (*«3 Jahre Berufserfahrung»*)

**Das Problem:** Zwei Fachverkaeufer:innen mit identischem Titel koennen voellig unterschiedliche Skillprofile haben:

```
Person A (Fleischtheke):          Person B (Obst/Gemuese):
├── Fleisch-Fachkenntnis: L4      ├── Fleisch-Fachkenntnis: L0
├── Obst/Gemuese: L1              ├── Obst/Gemuese: L4
├── HACCP: L3                     ├── HACCP: L2
├── Thekenpraesentation: L4       ├── Thekenpraesentation: L2
├── Kundenberatung: L3            ├── Kundenberatung: L4
└── Bestellwesen: L3              └── Bestellwesen: L1
```

Beide haben denselben Titel, aber nur Person A passt fuer die Fleischtheke, und nur Person B passt fuer den Obst/Gemuese-Bereich. Ohne feingranulare Skills ist diese Unterscheidung **unsichtbar**.

### 1.2 Die Kosten grober Zuordnung

| Problem | Auswirkung | Geschaetzte Kosten (Kaufland) |
|---------|-----------|-------------------------------|
| Fehlbesetzung Fleischtheke | Qualitaetsverlust, Kundenverlust | €2'000-5'000 pro Fall |
| Fehlbesetzung Filialleitung | Umsatzverlust, Mitarbeiterfluktuation | €50'000-200'000 pro Fall |
| Ungenutzte Skills | Demotivation, Kuendigung | €8'000-15'000 pro MA/Jahr |
| Blinde Nachfolgeplanung | Vakanz-Tage, externe Rekrutierung | €20'000-80'000 pro Stelle |

**Hochrechnung:** Bei 170'000 MA und konservativen 5% Fehlzuordnung: **€85M-170M jaehrlicher Effizienzverlust.**

---

## 2. Die Skill-Taxonomie: 9 Domains × 28 Cluster × 120 Skills

### 2.1 Architektur-Ueberblick

```
┌──────────────────────────────────────────────────────────────────────┐
│                     STAX-KAUF-001: SKILL-TAXONOMIE                   │
│                     120 Skills × 5 Proficiency Levels                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📦 DOM-WM  Warenmanagement          3 Cluster, 17 Skills            │
│  🤝 DOM-KI  Kundeninteraktion        2 Cluster, 12 Skills            │
│  🧫 DOM-HS  Hygiene & Sicherheit     2 Cluster,  9 Skills            │
│  💻 DOM-TS  Technik & Systeme        3 Cluster, 14 Skills            │
│  👥 DOM-FM  Fuehrung & Management    3 Cluster, 17 Skills            │
│  🚛 DOM-LO  Logistik & Operations    2 Cluster, 10 Skills            │
│  🛡️ DOM-CS  Compliance & Sicherheit  2 Cluster, 10 Skills            │
│  📊 DOM-AB  Analytik & BI            2 Cluster, 11 Skills            │
│  💬 DOM-KZ  Kommunikation            3 Cluster, 12 Skills            │
│                                                                      │
│  GESAMT: 9 Domains | 28 Cluster | 120 Skills | 600 Proficiency-Zellen│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.2 Autor-Aufgabentypen Verteilung

Jeder Skill ist einem der 5 Autor-Aufgabentypen zugeordnet:

| Typ | Anzahl | Anteil | Beschreibung | Automatisierungsrisiko |
|-----|--------|--------|-------------|------------------------|
| **R** Routine | 38 | 31.7% | Standardisierte, regelbasierte Taetigkeiten | Hoch (50-80%) |
| **M** Manual | 14 | 11.7% | Physische, nicht-routinemaessige Taetigkeiten | Mittel (20-40%) |
| **I** Interactive | 30 | 25.0% | Zwischenmenschliche Interaktion | Niedrig (<10%) |
| **A** Abstract | 26 | 21.7% | Analytische, problemloesende Taetigkeiten | Mittel-hoch (30-60% KI-gestuetzt) |
| **L** Leadership | 12 | 10.0% | Fuehrung, Entwicklung, Strategie | Sehr niedrig (<5%) |

**Strategische Implikation:** 31.7% der Skills sind hochgradig automatisierungsgefaehrdet. Das SBO-System muss Mitarbeitende systematisch von R-Skills zu I/A/L-Skills entwickeln.

### 2.3 Die 5 Proficiency Levels (Dreyfus-Modell)

| Level | Name | Verhaltensmarker | Typische Dauer | Supervision |
|-------|------|-----------------|----------------|-------------|
| 1 | **Novize** | Folgt Regeln, fragt bei Abweichungen | 1-4 Wochen | Direkte Anleitung |
| 2 | **Fortgeschritten** | Erkennt Muster, Routine selbstaendig | 1-3 Monate | Gelegentliche Ruecksprache |
| 3 | **Kompetent** | Priorisiert, loest Probleme, leitet an | 6-12 Monate | Ergebnisorientiert |
| 4 | **Gewandt** | Intuition, mentort andere, optimiert | 1-3 Jahre | Strategische Abstimmung |
| 5 | **Expert:in** | Setzt Standards, innoviert, strategisch | 3-10 Jahre | Selbstgesteuert |

---

## 3. Die 22 Rollenprofile: Vom Regal bis zur Geschaeftsfuehrung

### 3.1 Job-Familien Ueberblick

```
┌──────────────────────────────────────────────────────────────────────┐
│  JOB-FAMILIEN: 22 ROLLEN IN 3 FAMILIEN                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  JF-STORE: Filiale (88% ≈ 150'000 MA)                               │
│  ├── JOB-KAS    Kassierer:in                      45'000 MA         │
│  ├── JOB-REG    Regalservice                       35'000 MA         │
│  ├── JOB-FVO    Fachverk. Obst/Gemuese             10'000 MA         │
│  ├── JOB-FVF    Fachverk. Fleisch/Wurst             12'000 MA         │
│  ├── JOB-FVK    Fachverk. Kaese/Feinkost             6'000 MA         │
│  ├── JOB-WAE    Warenannahme/Lager                   8'000 MA         │
│  ├── JOB-SBK    SB-Kassen Betreuung                 5'000 MA         │
│  ├── JOB-SER    Servicepoint                         4'000 MA         │
│  ├── JOB-TLK    Teamleitung Kasse                    3'000 MA         │
│  ├── JOB-ALF    Abteilungsleitung Frische            3'000 MA         │
│  ├── JOB-ALT    Abteilungsleitung Trocken            2'000 MA         │
│  ├── JOB-SFL    Stellv. Filialleitung                1'500 MA         │
│  ├── JOB-FL     Filialleitung                        1'500 MA         │
│  └── JOB-BZL    Bezirksleitung                         200 MA         │
│                                                                      │
│  JF-LOGISTICS: Logistik/Zentrallager (5% ≈ 8'500 MA)                │
│  ├── JOB-LOG-KOM  Kommissionierer:in                 4'000 MA         │
│  ├── JOB-LOG-LTR  LKW-Fahrer:in                     2'000 MA         │
│  └── JOB-LOG-DIS  Disponent:in                        500 MA         │
│                                                                      │
│  JF-CORPORATE: Zentrale (7% ≈ 12'000 MA)                            │
│  ├── JOB-ZEN-HR   HR Business Partner                  300 MA         │
│  ├── JOB-ZEN-CM   Category Manager:in                  200 MA         │
│  ├── JOB-ZEN-MK   Marketing Manager:in                 150 MA         │
│  ├── JOB-ZEN-IT   IT Spezialist:in                     500 MA         │
│  └── JOB-ZEN-VL   Vertriebsleitung                      30 MA         │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 Skill-Anforderungs-Stufen pro Rolle

Jede Rolle hat drei Skill-Stufen:

| Stufe | Bedeutung | Konsequenz |
|-------|-----------|------------|
| **Mandatory** | Gate-Skills — ohne diese: Match-Score = 0 | Muss VOR Stellenantritt erfuellt sein |
| **Core** | Kern-Skills — gewichtet im Fit-Score | Sollte innerhalb 6 Monaten erreicht werden |
| **Development** | Entwicklungs-Skills — fuer naechsten Karriereschritt | Ziel fuer 12-24 Monate |

### 3.3 Beispiel: Skillprofil Filialleitung (JOB-FL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  JOB-FL: FILIALLEITUNG — Skill-Anforderungsprofil                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  MANDATORY (Gate — MUSS erfuellt sein):                              │
│  ├── SKL-FM-001  Mitarbeiterfuehrung          Level 4  ████████░░   │
│  ├── SKL-FM-010  P&L-Verantwortung            Level 4  ████████░░   │
│  ├── SKL-FM-011  KPI-Steuerung                Level 4  ████████░░   │
│  └── SKL-CS-014  Betriebsverfassungsrecht      Level 3  ██████░░░░   │
│                                                                      │
│  CORE (Gewichtet — bestimmt Fit-Score):                              │
│  ├── SKL-FM-013  Strategische Entwicklung      Level 4  ████████░░   │
│  ├── SKL-FM-012  Budgetplanung                 Level 4  ████████░░   │
│  ├── SKL-FM-003  Feedback & Entwicklung        Level 4  ████████░░   │
│  ├── SKL-FM-004  Konfliktmanagement            Level 4  ████████░░   │
│  ├── SKL-FM-020  Change Communication          Level 3  ██████░░░░   │
│  ├── SKL-FM-021  Stakeholder Management        Level 3  ██████░░░░   │
│  ├── SKL-AB-001  Umsatzanalyse                 Level 4  ████████░░   │
│  ├── SKL-AB-011  Personalbedarfsplanung        Level 4  ████████░░   │
│  ├── SKL-AB-003  Marktanalyse                  Level 3  ██████░░░░   │
│  ├── SKL-CS-010  Arbeitsrecht                  Level 3  ██████░░░░   │
│  ├── SKL-KZ-003  Reporting nach oben           Level 4  ████████░░   │
│  └── SKL-FM-006  Diversity & Inklusion         Level 3  ██████░░░░   │
│                                                                      │
│  DEVELOPMENT (Naechster Schritt: Bezirksleitung):                    │
│  ├── SKL-TS-021  Datenanalyse & Reporting      Level 3  ██████░░░░   │
│  └── SKL-FM-022  Projektmanagement             Level 3  ██████░░░░   │
│                                                                      │
│  AUTOR-PROFIL: L=40%, A=35%, I=15%, R=5%, M=5%                      │
│  GESAMTSKILLS: 4 Mandatory + 12 Core + 2 Development = 18 Skills    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.4 Autor-Typ-Shift entlang der Karriere

```
              R     M     I     A     L
Kassierer:in  ████  ░░    ██    ░░    ░░    R=50% I=25% M=10%
Fachverk.     ███   ██    ███   █░    ░░    R=30% I=30% M=20%
Teamleitung   ██    ░░    ███   ██    ███   L=30% I=25% A=20%
Abt.leitung   █░    ░░    ██    ████  ███   A=35% L=25% I=20%
Filialleitung ░░    ░░    ██    ████  ████  L=40% A=35% I=15%
Bezirksltg.   ░░    ░░    █░    ████  █████ L=50% A=35% I=10%

Der Aufstieg verlangt systematischen Skill-Typ-Wechsel:
  Basis:     R/M → Routine & Manual (Ausfuehrung)
  Fach:      I/R → Interactive & Routine (Beratung + Fach)
  Fuehrung:  L/A → Leadership & Abstract (Strategie + Steuerung)
```

---

## 4. Der Matching-Algorithmus

### 4.1 Formel

```
F(p,j) = Gate(p,j) × [ 0.60 × S_core(p,j) + 0.25 × S_dev(p,j) + 0.15 × S_pot(p,j) ]
```

**Wo:**

| Komponente | Formel | Erklaerung |
|-----------|--------|------------|
| **Gate(p,j)** | = 1 wenn ALLE mandatory Skills >= min_level, sonst 0 | Hartes Ausschlusskriterium |
| **S_core(p,j)** | = 1 - sqrt( Σ wᵢ × max(0, req_i - actual_i)² / Σ wᵢ ) | Gewichtete Lueckenanalyse |
| **S_dev(p,j)** | = Anteil development_skills mit actual >= 1 | Entwicklungspotenzial |
| **S_pot(p,j)** | = Lerngeschwindigkeit × Motivationsfaktor | Wachstumsprognose |

### 4.2 Interpretation

| Fit-Score | Kategorie | Bedeutung | Aktion |
|-----------|-----------|-----------|--------|
| F >= 0.85 | **Excellent Fit** | Sofort einsetzbar | Besetzung empfohlen |
| F >= 0.70 | **Good Fit** | Kurzes Onboarding (<4 Wochen) | Besetzung mit Einarbeitung |
| F >= 0.55 | **Development Fit** | Entwicklungsplan noetig (3-6 Monate) | Besetzung mit Foerderprogramm |
| F >= 0.40 | **Stretch Fit** | Ambitioniert (6-12 Monate) | Nur bei hohem Potenzial |
| F < 0.40 | **Gap too large** | Andere Rolle empfehlen | Keine Besetzung |

### 4.3 Rechenbeispiel: Anna wechselt von Kasse zu Teamleitung

**Anna's aktuelles Profil (JOB-KAS, 3 Jahre Erfahrung):**

```
SKL-FM-001  Mitarbeiterfuehrung:    Level 1 (benoetigt: 2)  → Gap: -1
SKL-KI-010  Kassen-Handling:        Level 4 (benoetigt: 4)  → Gap:  0
SKL-FM-002  Dienstplanung:          Level 0 (benoetigt: 2)  → Gap: -2
SKL-FM-005  Onboarding:             Level 1 (benoetigt: 3)  → Gap: -2
SKL-FM-003  Feedback:               Level 0 (benoetigt: 2)  → Gap: -2
SKL-FM-004  Konfliktmanagement:     Level 1 (benoetigt: 2)  → Gap: -1
SKL-KI-004  Beschwerdemanagement:   Level 3 (benoetigt: 4)  → Gap: -1
SKL-AB-002  KPI-Interpretation:     Level 0 (benoetigt: 2)  → Gap: -2
SKL-CS-010  Arbeitsrecht:           Level 0 (benoetigt: 2)  → Gap: -2
```

**Gate-Check:** SKL-FM-001 Level 1 < min_level 2 → **Gate = 0 → F = 0**

**Ergebnis:** Anna ist NOCH NICHT bereit fuer JOB-TLK. Aber mit einem gezielten 16-Wochen-Programm:

```
Woche 1-4:   SKL-FM-001 (Fuehrung) Level 1 → Level 2      ✓ Gate geoeffnet
Woche 5-8:   SKL-FM-002 (Dienstplan) Level 0 → Level 2     ✓
Woche 9-12:  SKL-FM-003 (Feedback) Level 0 → Level 2       ✓
Woche 13-16: SKL-FM-004 (Konflikt) Level 1 → Level 2       ✓

→ Neuer Fit-Score: F = 1 × [0.60 × 0.72 + 0.25 × 0.50 + 0.15 × 0.80] = 0.68
→ Kategorie: Good Fit — Besetzung mit Einarbeitung empfohlen
```

---

## 5. Karrierepfad-Matrix

### 5.1 Typische Aufstiegspfade

```
                                    ┌─────────┐
                                    │ JOB-BZL │  Bezirksleitung
                                    │  200 MA │
                                    └────┬────┘
                                         │ 3%/Jahr
                                    ┌────┴────┐
                     ┌──────────────│ JOB-FL  │  Filialleitung
                     │              │ 1'500 MA│
                     │              └────┬────┘
                     │                   │ 15%/Jahr
                     │              ┌────┴────┐
                     │         ┌────│ JOB-SFL │  Stellv. FL
                     │         │    │ 1'500 MA│
                     │         │    └────┬────┘
                     │         │         │
            ┌────────┴───┐  ┌──┴──────┐  │
            │ JOB-ZEN-HR │  │ JOB-ALF │──┘ Abteilungsltg.     ┌──────────┐
            │ JOB-ZEN-CM │  │ JOB-ALT │    Frische/Trocken    │ JOB-ZEN-VL│
            │     etc.   │  │ 5'000 MA│                        │    30 MA  │
            └────────────┘  └────┬────┘                        └──────────┘
             Zentrale            │ 6%/Jahr
                            ┌────┴────┐
                    ┌───────│ JOB-TLK │  Teamleitung Kasse
                    │       │ 3'000 MA│
                    │       └────┬────┘
                    │            │ 8%/Jahr
               ┌────┴────┐ ┌────┴────┐ ┌─────────┐ ┌─────────┐
               │ JOB-FVF │ │ JOB-KAS │ │ JOB-SBK │ │ JOB-SER │
               │ JOB-FVK │ │ 45'000  │ │ 5'000   │ │ 4'000   │
               │ JOB-FVO │ └────┬────┘ └─────────┘ └─────────┘
               │ 28'000  │      │ 12%/Jahr
               └─────────┘ ┌────┴────┐ ┌─────────┐
                Fachkraefte │ JOB-REG │ │ JOB-WAE │
                            │ 35'000  │ │ 8'000   │
                            └─────────┘ └─────────┘
                             Einstiegsrollen
```

### 5.2 Kritische Skill-Gaps bei Uebergaengen

| Uebergang | Autor-Shift | Groesste Luecken | Entwicklungszeit |
|-----------|------------|-----------------|------------------|
| Fachkraft → Teamleitung | R/M/I → **L** | Fuehrung (-2), Dienstplan (-2), Feedback (-2) | 16 Wochen |
| Teamleitung → Filialleitung | L+I → L+**A** | P&L (-2), Strategie (-3), Marktanalyse (-2) | 26 Wochen |
| Filiale → Zentrale | L+I → **A**+L | Datenanalyse (-2), Projektmanagement (-2), Agile (-3) | 12 Wochen |

**Kerninsight:** Der kritischste Uebergang ist nicht Kasse → Teamleitung (dort wird investiert), sondern **Teamleitung → Filialleitung**. Hier fehlen systematisch Abstract-Skills (P&L, Strategie, Marktanalyse) — und genau hier scheitern viele interne Befoerderungen.

---

## 6. Skill-Decay und Auffrischung

### 6.1 Decay-Raten nach Domain

Jeder Skill hat eine monatliche Decay-Rate (delta_monthly). Ohne Nutzung verliert eine Person pro Monat:

| Domain | Durchschnittliche Decay-Rate | Beispiel |
|--------|-------------------------------|---------|
| DOM-HS Hygiene | 0.012/Monat | HACCP-Wissen: nach 12 Monaten ohne Praxis: -14% |
| DOM-TS Technik | 0.015/Monat | SAP-Kenntnisse: nach 6 Monaten Pause: -9% |
| DOM-WM Warenkunde | 0.015/Monat | Frische-Expertise: nach 12 Monaten: -18% |
| DOM-KI Kundeninteraktion | 0.012/Monat | Beratungsskills: relativ stabil |
| DOM-FM Fuehrung | 0.008/Monat | Fuehrungskompetenz: sehr stabil |
| DOM-KZ Soft Skills | 0.005/Monat | Teamarbeit: quasi-permanent |

**Implikation fuer Kaufland:**
- **Pflichtschulungen** (HACCP, Arbeitssicherheit): Jaehrlich auffrischen
- **Fachskills** (Warenkunde): Bei Abteilungswechsel innerhalb 4 Wochen auffrischen
- **Fuehrungs-Skills**: Investition «haelt» — hoher ROI

### 6.2 Transferierbarkeit (Portabilitaet)

| Transferierbarkeit | Bedeutung | Beispiele |
|--------------------|-----------|----------|
| >= 0.90 | Universell einsetzbar | Teamarbeit, Stressresistenz, Erste Hilfe |
| 0.70 - 0.89 | Branchenuebergreifend | Kundenansprache, Regalbestueckung, Datenanalyse |
| 0.50 - 0.69 | Branchenspezifisch | Fleisch-Fachkenntnis, SAP Retail, Thekenpraesentation |
| < 0.50 | Unternehmensspezifisch | Kaufland-internes Bestellsystem, spezifische Prozesse |

---

## 7. Implementierung: Das digitale Skill-Cockpit

### 7.1 System-Architektur

```
┌──────────────────────────────────────────────────────────────────────┐
│                     SKILL COCKPIT ARCHITEKTUR                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  SKILL TAXONOMY   │  │  JOB PROFILES     │  │  EMPLOYEE        │   │
│  │  STAX-KAUF-001   │  │  JPRF-KAUF-001   │  │  PROFILES        │   │
│  │  120 Skills      │  │  22 Rollen       │  │  170'000 MA      │   │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘   │
│           │                     │                      │             │
│           └─────────────────────┼──────────────────────┘             │
│                                 │                                    │
│                        ┌────────┴────────┐                           │
│                        │  MATCHING ENGINE │                           │
│                        │  F(p,j) Score   │                           │
│                        └────────┬────────┘                           │
│                                 │                                    │
│              ┌──────────────────┼──────────────────┐                 │
│              │                  │                   │                 │
│     ┌────────┴────────┐ ┌──────┴───────┐ ┌────────┴────────┐       │
│     │  BESETZUNGS-     │ │  ENTWICKLUNGS-│ │  NACHFOLGE-     │       │
│     │  EMPFEHLUNG      │ │  PLANUNG      │ │  PLANUNG        │       │
│     │                  │ │               │ │                  │       │
│     │  "Wer passt auf  │ │ "Was braucht  │ │ "Wer kann FL    │       │
│     │   diese Stelle?" │ │  Anna noch?"  │ │  Meier ersetzen?"│      │
│     └──────────────────┘ └───────────────┘ └──────────────────┘      │
│                                                                      │
│  DASHBOARDS:                                                         │
│  ├── Filialleitung: Team-Skill-Heatmap, Gaps, Entwicklung           │
│  ├── HR: Konzernweite Skill-Verteilung, Engpaesse, Trends           │
│  ├── Mitarbeitende: Eigenes Profil, Karrierepfade, Empfehlungen     │
│  └── Geschaeftsfuehrung: Strategische Skill-KPIs, Risikoanalyse     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 7.2 Assessment-Methoden (Multi-Source)

| Methode | Fuer welche Skills | Frequenz | Aufwand |
|---------|-------------------|----------|---------|
| **Selbsteinschaetzung** | Soft Skills, Meta-Kompetenzen | Quartalsweise | 15 Min |
| **Fuehrungskraft-Rating** | Core Skills, Leistung | Halbjaehrlich | 30 Min/MA |
| **Peer-Feedback** | Teamarbeit, Kommunikation | Jaehrlich | 10 Min |
| **Praxis-Assessment** | Fach-Skills (Theke, Kasse, etc.) | Bei Bedarf | 30-60 Min |
| **Wissenstest** | HACCP, Recht, Warenkunde | Jaehrlich | 20 Min |
| **Mystery Shopping** | Kundeninteraktion | Quartalsweise | Extern |
| **KPI-basiert** | P&L, Schwund, Produktivitaet | Laufend | Automatisch |
| **Zertifikate** | Stapler, Erste Hilfe, IHK | Bei Erwerb | Dokumentation |

### 7.3 Rollout-Plan

| Phase | Zeitraum | Scope | Ziel |
|-------|----------|-------|------|
| **Pilot** | M1-M6 | 10 Filialen, 1 Region | Taxonomie validieren, Assessment testen |
| **Rollout 1** | M7-M12 | 200 Filialen | Alle Filialmitarbeitenden erfasst |
| **Rollout 2** | M13-M18 | 1'000 Filialen + Logistik | Matching-Engine live |
| **Vollbetrieb** | M19-M24 | Alle 1'500+ Filialen + Zentrale | Volle Funktionalitaet |

---

## 8. ROI des feingranularen Skill-Systems

### 8.1 Nutzen-Treiber

| Treiber | Mechanismus | Geschaetzter Wert (p.a.) |
|---------|-------------|--------------------------|
| Reduzierte Fehlbesetzung | Fit-Score statt Bauchgefuehl | €15-25M |
| Schnelleres Onboarding | Gezieltes Skill-Gap-Training | €8-12M |
| Reduzierte Fluktuation | Sichtbare Karrierepfade | €20-35M |
| Interne Besetzungsquote erhoehen | Pool-Transparenz | €5-10M |
| Bessere Nachfolgeplanung | Proaktives Gap-Closing | €10-15M |
| **Gesamt** | | **€58-97M/Jahr** |

### 8.2 Investition

| Posten | Einmalig | Laufend (p.a.) |
|--------|----------|----------------|
| Software/Plattform | €2-4M | €0.5-1M |
| Taxonomie-Entwicklung & Validierung | €0.5-1M | €0.2M |
| Assessment-Design & Schulung | €1-2M | €0.5M |
| Change Management & Kommunikation | €1-1.5M | €0.3M |
| **Gesamt** | **€4.5-8.5M** | **€1.5-2M/Jahr** |

### 8.3 ROI

```
ROI (Jahr 1): (€58M - €8.5M - €2M) / (€8.5M + €2M) = 453%
ROI (Jahr 2+): (€58M - €2M) / €2M = 2'800%

Break-Even: Monat 3-5 (bereits durch reduzierte Fehlbesetzungen)
```

---

## 9. Zusammenfassung: Warum dieses System funktioniert

```
┌──────────────────────────────────────────────────────────────────────┐
│  KAUFLAND SKILL-SYSTEM: 5 DESIGN-PRINZIPIEN                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. FEINGRANULAR: 120 Skills statt 20 Stellenbeschreibungen         │
│     → Sichtbarkeit, was Menschen WIRKLICH koennen                   │
│                                                                      │
│  2. EVIDENZBASIERT: Dreyfus-Levels + Autor-Typen + Decay-Raten     │
│     → Wissenschaftlich fundierte Bewertung                          │
│                                                                      │
│  3. ALGORITHMISCH: Fit-Score F(p,j) mit Mandatory Gate             │
│     → Objektive, nachvollziehbare Besetzungsentscheidungen          │
│                                                                      │
│  4. ENTWICKLUNGSORIENTIERT: Karrierepfade mit Skill-Gap-Analyse    │
│     → Jede:r MA sieht den Weg zur naechsten Stufe                  │
│                                                                      │
│  5. ZUKUNFTSSICHER: Automatisierungsrisiko pro Skill quantifiziert  │
│     → Gezielte Umschulung von R-Skills zu I/A/L-Skills              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Anhang: Datenmodell-Referenz

| Datei | Inhalt |
|-------|--------|
| `data/sbo/skill-taxonomy-kaufland.yaml` | 120 Skills, 9 Domains, 28 Cluster |
| `data/sbo/job-profiles-kaufland.yaml` | 22 Rollen, Matching-Algorithmus, Karrierepfade |
| `outputs/sessions/EBF-S-2026-02-17-ORG-001/F1_SBO_Model_Report_v1.md` | Technischer Report (5-Layer Pipeline) |
| `outputs/sessions/EBF-S-2026-02-17-ORG-001/F2_SBO_Executive_Report_Kaufland_v1.md` | Executive Report |

---

*FehrAdvice & Partners AG | Evidence-Based Framework (EBF) | MOD-ORG-SBO-001 v1.1*
