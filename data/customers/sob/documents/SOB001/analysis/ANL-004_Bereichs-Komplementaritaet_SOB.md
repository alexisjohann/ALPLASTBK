# SOB Bereichs-Komplementaritäts-Analyse (γ-Matrix)

**Analyse-ID:** ANL-004
**Projekt:** SOB002 (Vorarbeit Phase 2: BEATRIX-Modellentwicklung)
**Datum:** 2026-02-10
**Basis:** 11-Dokument-EBF-Analyse, ANL-001 (Pyramide), ANL-002 (Stakeholder), ANL-003 (Gap-Analyse)
**Status:** ENTWURF

---

## 1. Executive Summary

Diese Analyse quantifiziert die **Komplementarität (γ)** zwischen den 5 Geschäftsbereichen der SOB und identifiziert die grössten Hebel zur γ-Erhöhung. Die Analyse basiert auf dem EBF-Komplementaritätsframework (Appendix B):

```
U_SOB = Σ gᵢ + Σ γᵢⱼ × gᵢ × gⱼ
```

**Kernbefund:** Die SOB hat **starke additive Leistung** (Σ gᵢ = hoch), aber **schwache Komplementarität** (γ̄ = 0.27). Die grösste Schwachstelle ist die Beziehung P&O ↔ alle GBs (γ ≈ 0.15), gefolgt von Transport ↔ Mobilität (γ = 0.25). Die grösste Chance liegt in der Achse **Transport × Mobilität** (Customer Journey Integration) und **P&O × alle GBs** (Behavioral Change als Querschnittsfunktion).

```
┌─────────────────────────────────────────────────────────────────────────┐
│  KOMPLEMENTARITÄTS-DIAGNOSE                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  γ̄_IST  = 0.27  (gewichteter Durchschnitt aller GB-Paare)             │
│  γ̄_SOLL = 0.52  (EBF-Benchmark für integrierte Organisationen)        │
│  Δγ     = -0.25  (substanziell)                                        │
│                                                                         │
│  INTERPRETATION:                                                        │
│  → 0.00-0.20: Isolierte Bereiche (Silos)                              │
│  → 0.20-0.40: Schwache Komplementarität ← SOB IST HIER (0.27)        │
│  → 0.40-0.60: Moderate Komplementarität ← SOB ZIEL (0.52)            │
│  → 0.60-0.80: Starke Komplementarität                                 │
│  → 0.80-1.00: Vollständige Integration                                │
│                                                                         │
│  NUTZEN-POTENZIAL:                                                     │
│  U(γ=0.52) - U(γ=0.27) ≈ +25% Gesamtleistungsfähigkeit              │
│  → Durch bessere Zusammenarbeit, NICHT durch mehr Einzelleistung       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Methodik

### 2.1 γ-Schätzung: Triangulation aus 3 Quellen

Jeder γ-Wert wird aus 3 unabhängigen Quellen geschätzt:

| Quelle | Gewicht | Methode |
|--------|---------|---------|
| **MA-Umfrage (DOC-004)** | 40% | Quantitative Scores für Zusammenarbeit (F6, I4, H2) |
| **Schwerpunktthemen (DOC-007)** | 30% | Analyse der Cross-GB-Projekte und Abhängigkeiten |
| **SWOT pro GB (DOC-009)** | 30% | Qualitative Bewertung der Schnittstellen-Qualität |

### 2.2 γ-Skala

| γ-Wert | Interpretation | Beispiel |
|--------|---------------|----------|
| 0.00 | Keine Interaktion | Komplett isolierte Einheiten |
| 0.10-0.20 | Minimal | Nur formale Schnittstellen |
| 0.20-0.35 | Schwach | Gelegentliche Koordination |
| 0.35-0.50 | Moderat | Regelmässige Zusammenarbeit |
| 0.50-0.65 | Gut | Aktive Integration |
| 0.65-0.80 | Stark | Strategische Verzahnung |
| 0.80-1.00 | Vollständig | Organische Einheit |
| < 0.00 | Destruktiv | Aktiver Wettbewerb / Blockade |

### 2.3 Leistungsindex gᵢ pro GB

Die additive Leistung jedes GB wird auf einer Skala 0-1 geschätzt:

| GB | gᵢ | Quelle | Begründung |
|----|-----|--------|-----------|
| Transport (V) | 0.75 | DOC-004, DOC-009 | Hohe operative Reife, Pünktlichkeit, aber tiefste Motivation (75) |
| Infrastruktur (I) | 0.80 | DOC-009 | Guter Netzzustand, Innovation (AFAS), breite Kompetenz |
| Mobilität (M) | 0.70 | DOC-009 | Innovativ, aber knappe Ressourcen, Anschlussfähigkeit unvollständig |
| Finanzen & Services (F) | 0.75 | DOC-009 | Solide Prozesse, Compliance, wachsende Immobilienkompetenz |
| P&O | 0.55 | DOC-008, DOC-009 | Keine strategische Rolle, FK-Entwicklung nicht mit BC verknüpft |

---

## 3. γ-Matrix: Vollständige Darstellung

### 3.1 IST-Zustand

```
┌─────────────────────────────────────────────────────────────────────────┐
│  γ-MATRIX IST: KOMPLEMENTARITÄT ZWISCHEN GESCHÄFTSBEREICHEN             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│              Transport  Infrastr.  Mobilität  Fin&Serv   P&O           │
│              (V)        (I)        (M)        (F)        (PO)          │
│  ──────────  ─────────  ─────────  ─────────  ─────────  ─────────    │
│  Transport    1.00       0.35       0.25       0.30       0.15        │
│  Infrastr.    0.35       1.00       0.20       0.30       0.10        │
│  Mobilität    0.25       0.20       1.00       0.25       0.15        │
│  Fin&Serv     0.30       0.30       0.25       1.00       0.20        │
│  P&O          0.15       0.10       0.15       0.20       1.00        │
│                                                                         │
│  Legende:                                                              │
│  ■ 0.00-0.15  Kritisch (rot)    → P&O↔I, P&O↔V                       │
│  ■ 0.15-0.25  Schwach (orange)  → V↔M, I↔M, M↔F, P&O↔M              │
│  ■ 0.25-0.35  Unter Soll (gelb) → V↔I, V↔F, I↔F                     │
│  ■ 0.35-0.50  Akzeptabel (grün) → (keiner erreicht diesen Wert)      │
│                                                                         │
│  γ̄_IST = (0.35+0.25+0.30+0.15+0.20+0.30+0.25+0.10+0.15+0.20)/10    │
│         = 0.225 (ungewichtet)                                          │
│  γ̄_IST = 0.27 (gewichtet nach gᵢ × gⱼ)                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 SOLL-Zustand

```
┌─────────────────────────────────────────────────────────────────────────┐
│  γ-MATRIX SOLL: ZIELWERTE (24 Monate)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│              Transport  Infrastr.  Mobilität  Fin&Serv   P&O           │
│              (V)        (I)        (M)        (F)        (PO)          │
│  ──────────  ─────────  ─────────  ─────────  ─────────  ─────────    │
│  Transport    1.00       0.55       0.60       0.45       0.45        │
│  Infrastr.    0.55       1.00       0.40       0.50       0.40        │
│  Mobilität    0.60       0.40       1.00       0.45       0.45        │
│  Fin&Serv     0.45       0.50       0.45       1.00       0.40        │
│  P&O          0.45       0.40       0.45       0.40       1.00        │
│                                                                         │
│  γ̄_SOLL = 0.52 (gewichtet nach gᵢ × gⱼ)                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Δγ-Matrix (GAP)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Δγ-MATRIX: GAP (SOLL - IST)                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│              Transport  Infrastr.  Mobilität  Fin&Serv   P&O           │
│              (V)        (I)        (M)        (F)        (PO)          │
│  ──────────  ─────────  ─────────  ─────────  ─────────  ─────────    │
│  Transport    --         +0.20      +0.35 ⚡   +0.15      +0.30 ⚡     │
│  Infrastr.    +0.20      --         +0.20      +0.20      +0.30 ⚡     │
│  Mobilität    +0.35 ⚡   +0.20      --         +0.20      +0.30 ⚡     │
│  Fin&Serv     +0.15      +0.20      +0.20      --         +0.20       │
│  P&O          +0.30 ⚡   +0.30 ⚡   +0.30 ⚡   +0.20      --          │
│                                                                         │
│  ⚡ = Grösste Gaps (≥ +0.30)                                           │
│                                                                         │
│  TOP 5 GAPS:                                                           │
│  1. Transport ↔ Mobilität  Δ = +0.35 (Customer Journey)               │
│  2. P&O ↔ Transport        Δ = +0.30 (FK-Entwicklung Betrieb)         │
│  3. P&O ↔ Infrastruktur    Δ = +0.30 (Fachkräfte-Management)          │
│  4. P&O ↔ Mobilität        Δ = +0.30 (Innovations-Kultur)             │
│  5. Transport ↔ P&O        Δ = +0.30 (Kulturwandel Transport)         │
│                                                                         │
│  → P&O ist an 4 von 5 grössten Gaps beteiligt!                        │
│  → Transport ↔ Mobilität ist der grösste Business-Gap                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Detailanalyse pro GB-Paar

### 4.1 Transport ↔ Mobilität (γ = 0.25, Δ = +0.35)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TRANSPORT × MOBILITÄT: GRÖSSTER BUSINESS-GAP                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  IST-ZUSTAND (γ = 0.25):                                              │
│  → Transport liefert den Betrieb, Mobilität das Kundenerlebnis         │
│  → Schnittstelle = informell, nicht formalisiert                       │
│  → DOC-009: «Operative Anschlussfähigkeit an Transport unvollständig» │
│  → Customer Journey bricht an der GB-Grenze                            │
│                                                                         │
│  EVIDENZ:                                                              │
│  • DOC-004: Abt.-übergreifende Prozesse = 56 (tiefster Score)         │
│  • DOC-007: Keine gemeinsamen Schwerpunktthemen V↔M                   │
│  • DOC-009: Mobilität-Schwäche: «Anschlussfähigkeit unvollständig»    │
│                                                                         │
│  WERTSCHÖPFUNGSPOTENZIAL:                                              │
│  → Customer Journey nahtlos (Ticketing → Reise → Service)              │
│  → Datenintegration (Mobilität-Insights → Transport-Planung)          │
│  → Gemeinsame Produktentwicklung (z.B. IFIZ-Integration)              │
│                                                                         │
│  HEBEL:                                                                │
│  → Cross-GB-Team «Customer Experience»                                 │
│  → Gemeinsamer KPI: Customer Satisfaction Score                       │
│  → Pilotprojekt: VAE-Customer-Journey End-to-End                      │
│                                                                         │
│  SOLL (γ = 0.60):                                                      │
│  → Nahtlose Customer Journey als gemeinsame Verantwortung              │
│  → Gemeinsame Produktentwicklung und Datennutzung                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Transport ↔ Infrastruktur (γ = 0.35, Δ = +0.20)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TRANSPORT × INFRASTRUKTUR: OPERATIVE SCHNITTSTELLE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  IST-ZUSTAND (γ = 0.35):                                              │
│  → Höchster IST-γ aller Paare (= natürlich stärkste Abhängigkeit)     │
│  → Transport nutzt Infrastruktur täglich (Netz, Sicherheit, Trassen)  │
│  → Integrierte Struktur (EVU + ISB) als institutioneller Vorteil      │
│  → Aber: Getrennte Finanzierungsplanung (DOC-007: ERTMS «pro GB»)    │
│                                                                         │
│  EVIDENZ:                                                              │
│  • DOC-009: «Integrierte Struktur» als Stärke Infrastruktur           │
│  • DOC-007: ERTMS-Roadmap erfordert GB-übergreifende Koordination     │
│  • DOC-005: Separate Spartenergebnisse (RPV, Infrastruktur)           │
│                                                                         │
│  HEBEL:                                                                │
│  → Gemeinsame Betriebsplanung (Sperrpausen, Ausbauschritt 2030/35)   │
│  → Integriertes Asset Management (Fahrzeug × Infrastruktur)           │
│  → ERTMS als Cross-GB-Programm (nicht «jeder plant separat»)          │
│                                                                         │
│  SOLL (γ = 0.55):                                                      │
│  → Vollintegrierte Betriebsplanung als Wettbewerbsvorteil             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 P&O ↔ alle GBs (γ̄ = 0.15, Δ = +0.30)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  P&O × ALLE GBs: SYSTEMISCHE SCHWACHSTELLE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  IST-ZUSTAND (γ̄ = 0.15):                                              │
│  → P&O hat die niedrigste Komplementarität mit ALLEN anderen GBs      │
│  → P&O hat KEINE strategische Rolle (DOC-008: 4-Rollen ohne P&O)     │
│  → FK-Entwicklung NICHT mit Behavioral Change verknüpft (DOC-009)     │
│  → HR-Analytics begrenzt (DOC-009: Schwäche P&O)                      │
│                                                                         │
│  EINZELWERTE:                                                          │
│  P&O ↔ Transport:     γ = 0.15 (nur Personaladministration)           │
│  P&O ↔ Infrastruktur: γ = 0.10 (minimaler Kontakt)                   │
│  P&O ↔ Mobilität:     γ = 0.15 (gelegentliche Innovationsprojekte)   │
│  P&O ↔ Finanzen:      γ = 0.20 (Gehaltsadministration, Controlling)  │
│                                                                         │
│  WARUM SO NIEDRIG?                                                     │
│  1. Keine strategische Verankerung → wird als «Verwaltung» gesehen   │
│  2. Kein BC-Framework → P&O kann nicht «transformieren»               │
│  3. Keine HR-Analytics → Kann GBs nicht evidenzbasiert beraten        │
│  4. Ressourcenknappheit → Rein operativ ausgelastet                   │
│                                                                         │
│  PARADOX:                                                              │
│  P&O ist der GB, der γ ZWISCHEN allen anderen GBs erhöhen sollte      │
│  (via Kultur, FK-Entwicklung, OE), aber selbst die niedrigste         │
│  Komplementarität hat. Der «Integrator» ist nicht integriert.         │
│                                                                         │
│  HEBEL (höchste Priorität!):                                           │
│  → 5. Strategische Rolle: «Arbeitgeberin & Lernende Organisation»    │
│  → BEATRIX als P&O-Werkzeug für evidenzbasierte Transformation       │
│  → BC-Kompetenz in P&O aufbauen (FA-Training)                         │
│  → Kulturwandel als P&O-Kernaufgabe definieren (nicht Nebenaufgabe)  │
│                                                                         │
│  SOLL (γ̄ = 0.43):                                                     │
│  → P&O als strategischer Partner aller GBs                            │
│  → Behavioral Change als Querschnittskompetenz                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.4 Infrastruktur ↔ Mobilität (γ = 0.20, Δ = +0.20)

| Dimension | Beschreibung |
|-----------|-------------|
| **IST** | Minimale Interaktion. Infrastruktur baut/unterhält, Mobilität vermarktet. Kein gemeinsames Produkt-Denken. |
| **Potenzial** | Verkehrsdrehscheiben als gemeinsames Produkt (Bahnhof = Infrastruktur + Kundenerlebnis). Herisau-Projekt als Pilotchance. |
| **Hebel** | Gemeinsame Planung Verkehrsdrehscheiben, Integration Bahnhofserlebnis |
| **SOLL** | γ = 0.40 (moderate Integration über Knotenpunkte) |

### 4.5 Finanzen & Services ↔ andere GBs (γ̄ = 0.26)

| GB-Paar | IST-γ | Charakter | Hebel |
|---------|-------|-----------|-------|
| F ↔ Transport | 0.30 | Controlling + Spartenergebnis | Integriertes Performance Management |
| F ↔ Infrastruktur | 0.30 | Finanzierung + BAV-Reporting | Gemeinsame Investitionsplanung |
| F ↔ Mobilität | 0.25 | Budget + Immobilien | Business Case Modelle für Innovation |
| F ↔ P&O | 0.20 | Gehaltsadmin + Compliance | HR-Analytics + People Controlling |

---

## 5. Schwerpunktthemen-Analyse: Cross-GB-Vernetzung

### 5.1 IST: GB-Isolation in Schwerpunktthemen (DOC-007)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHWERPUNKTTHEMEN: CROSS-GB VERNETZUNG                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TOTAL THEMEN: 24                                                      │
│  GL-übergreifend: 5 (21%)                                              │
│  GB-spezifisch: 19 (79%)                                               │
│                                                                         │
│  CROSS-GB-VERKNÜPFUNGEN:                                               │
│                                                                         │
│  Thema                      GB1    GB2    Typ                           │
│  ─────────────────────────  ─────  ─────  ──────────────────           │
│  ERTMS-Roadmap              I      V      Technisch (formalisiert)     │
│  Logistik-Professionalis.   F&S    V      Operativ (Projekt DIL)       │
│  Herisau-Entwicklung        F&S    I      Investition (räumlich)       │
│                                                                         │
│  EXPLIZIT CROSS-GB: 3 von 24 = 12.5%                                  │
│  IMPLIZIT CROSS-GB: ~5 von 24 = 20.8%                                 │
│  REIN GB-ISOLIERT: ~16 von 24 = 66.7%                                 │
│                                                                         │
│  FEHLENDE CROSS-GB-THEMEN:                                             │
│  ❌ Customer Journey (V × M)                                           │
│  ❌ Verkehrsdrehscheiben (I × M)                                       │
│  ❌ Kulturwandel Cross-GB (P&O × alle)                                 │
│  ❌ Integriertes Performance Mgmt (F × alle)                           │
│  ❌ Gemeinsame Digitalstrategie (M × I × V)                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Cross-GB-Potenzial-Matrix

| Thema (DOC-007) | Primär-GB | Potenzielle Partner-GBs | γ-Potenzial |
|-----------------|-----------|------------------------|-------------|
| Customer Journey | M | **V** (Betrieb), **I** (Bahnhof) | +0.15 auf V↔M |
| Digitale Transformation | M | **I** (Daten), **V** (Disposition) | +0.10 auf M↔I, M↔V |
| Strategische Personalentwicklung | P&O | **V** (Transport-Kultur), **alle** | +0.15 auf P&O↔alle |
| Nachhaltigkeit | V | **I** (Energie), **F** (Reporting) | +0.05 auf V↔I |
| ERTMS | I | **V** (Rollmaterial), **F** (Finanzierung) | +0.05 auf I↔V |
| Arbeitssicherheit | V | **I** (Infrastruktur-Sicherheit) | +0.05 auf V↔I |
| Compliance Office | F | **P&O** (Governance), **alle** | +0.05 auf F↔P&O |

---

## 6. Komplementaritäts-Treiber und -Blocker

### 6.1 Treiber (γ-erhöhend)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  γ-TREIBER (erhöhen Komplementarität)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  T1: GEMEINSAME WERTE (DOC-011)                                        │
│      5 gemeinsame Werte → geteilte Identität                          │
│      ABER: Nicht operationalisiert → Potenzial nicht genutzt           │
│      Effekt: +0.05 (IST) → +0.15 (nach Operationalisierung)          │
│                                                                         │
│  T2: CEO ALS INTEGRATOR (DOC-001)                                      │
│      CEO Readiness 0.90, sieht Silo-Problem klar                      │
│      Legitimation für Cross-GB-Initiativen                             │
│      Effekt: +0.10 (zeitlich begrenzt auf «Honeymoon-Phase»)          │
│                                                                         │
│  T3: INTEGRIERTE STRUKTUR EVU+ISB (DOC-009)                            │
│      Infrastruktur und Transport unter einem Dach                      │
│      Organisatorischer Vorteil gegenüber getrennten Unternehmen        │
│      Effekt: +0.10 auf V↔I                                            │
│                                                                         │
│  T4: SOBkulturzug (DOC-007)                                            │
│      Bestehendes Gefäss für Kulturentwicklung                          │
│      Potenzial als γ-Plattform                                        │
│      Effekt: +0.05 (IST, ungenutzt) → +0.10 (nach Aktivierung)       │
│                                                                         │
│  T5: HOHE MA-MOTIVATION (DOC-004)                                      │
│      Motivation 77, Zugehörigkeit 81, Vertrauen 78                    │
│      Bereitschaft für Zusammenarbeit vorhanden                         │
│      Effekt: +0.05 (latent, nicht aktiviert)                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Blocker (γ-senkend)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  γ-BLOCKER (senken Komplementarität)                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  B1: GB-IDENTITÄT > SOB-IDENTITÄT (Endowment Effect)                  │
│      BL identifizieren sich mit «ihrem» GB, nicht mit SOB              │
│      Effekt: -0.15 (stärkster Blocker)                                │
│      Evidenz: DOC-004 (Team intern 81-85, Cross 56-70)                │
│                                                                         │
│  B2: ANREIZSYSTEM GB-ISOLIERT (Spartenergebnis als einziger KPI)      │
│      Was gemessen wird, wird optimiert → GB-Optimierung                │
│      Effekt: -0.12                                                     │
│      Evidenz: DOC-005 (nur Spartenergebnisse auf VR-Stufe)            │
│                                                                         │
│  B3: KEINE CROSS-GB-KPIs (DOC-005)                                    │
│      0 KPIs für Prozesse & Organisation                               │
│      Zusammenarbeit ist im Steuerungssystem unsichtbar                 │
│      Effekt: -0.10                                                     │
│      Evidenz: DOC-005 (Perspektive «Prozesse» = 0 KPIs)              │
│                                                                         │
│  B4: RESSOURCENKNAPPHEIT (DOC-009: alle GBs)                           │
│      «An der Grenze der Belastbarkeit» → kein Raum für Neues          │
│      Cross-GB-Projekte = «Extra-Arbeit»                               │
│      Effekt: -0.08                                                     │
│                                                                         │
│  B5: FEHLENDE PLATTFORMEN (keine institutionellen Cross-GB-Gefässe)   │
│      Kein regelmässiges Cross-GB-Meeting (ausser GL)                  │
│      Kein Cross-GB-Budget                                              │
│      Effekt: -0.07                                                     │
│                                                                         │
│  B6: ENTSCHEIDUNGSWEGE (DOC-004: Score 59)                             │
│      Langsame Entscheidungen → Cross-GB-Projekte stocken              │
│      Effekt: -0.05                                                     │
│                                                                         │
│  TOTAL BLOCKER-EFFEKT: -0.57                                           │
│  TOTAL TREIBER-EFFEKT: +0.35 (IST) → +0.55 (nach Aktivierung)        │
│  NETTO IST: -0.22 → erklärt γ̄ = 0.27 (niedrig)                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Interventions-Design: γ-Erhöhungsstrategie

### 7.1 Interventions-Architektur

```
┌─────────────────────────────────────────────────────────────────────────┐
│  γ-ERHÖHUNGSSTRATEGIE: 3 EBENEN                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EBENE 1: BLOCKER ENTFERNEN (Quick Wins, Monat 1-3)                   │
│  ──────────────────────────────────────────────────                    │
│  → B3: Cross-GB-KPIs einführen (3 Leading Indicators)                 │
│  → B5: Cross-GB-Plattformen schaffen (BL-Peer-Meetings)              │
│  → B2: Anreizsystem ergänzen (nicht nur Spartenergebnis)             │
│  Erwarteter Effekt: γ̄ +0.08 → 0.35                                  │
│                                                                         │
│  EBENE 2: TREIBER AKTIVIEREN (Mittelfristig, Monat 3-9)              │
│  ──────────────────────────────────────────────────────                │
│  → T1: Werte operationalisieren (Verhaltensanker)                    │
│  → T4: SOBkulturzug als γ-Plattform nutzen                           │
│  → T3: Integrierte Struktur als Vorteil ausspielen                   │
│  Erwarteter Effekt: γ̄ +0.10 → 0.45                                  │
│                                                                         │
│  EBENE 3: IDENTITÄT TRANSFORMIEREN (Langfristig, Monat 9-24)         │
│  ──────────────────────────────────────────────────────────            │
│  → B1: GB-Identität → SOB-Identität (Identity Economics)             │
│  → BL-Transformation (Readiness 0.45 → 0.75)                         │
│  → P&O als strategischer Partner aufbauen                             │
│  Erwarteter Effekt: γ̄ +0.07 → 0.52                                  │
│                                                                         │
│  GESAMT-TRAJECTORY:                                                    │
│  Monat 0:  γ̄ = 0.27                                                  │
│  Monat 3:  γ̄ = 0.35 (Blocker reduziert)                              │
│  Monat 9:  γ̄ = 0.45 (Treiber aktiviert)                              │
│  Monat 24: γ̄ = 0.52 (Identität transformiert)                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Interventionen pro GB-Paar (Top 5 Gaps)

| Rang | GB-Paar | IST→SOLL | Intervention | Typ | Timeline |
|------|---------|----------|-------------|-----|----------|
| 1 | **V ↔ M** | 0.25→0.60 | Cross-GB-Team «Customer Experience», gemeinsamer Satisfaction-KPI | Strukturell + KPI | M3-M12 |
| 2 | **P&O ↔ V** | 0.15→0.45 | BC-basierte FK-Entwicklung für Transport-Kader, Kulturwandel-Programm | Training + Nudge | M3-M18 |
| 3 | **P&O ↔ I** | 0.10→0.40 | Fachkräfte-Strategie als gemeinsames Programm, Employer Branding | Programm | M6-M18 |
| 4 | **P&O ↔ M** | 0.15→0.45 | Innovations-Kultur gemeinsam entwickeln, «SOBkulturzug» nutzen | Kultur + Plattform | M3-M12 |
| 5 | **BL ↔ BL** | 0.15→0.45 | BL-Peer-Plattform (monatlich), gemeinsame Zielvereinbarungen | Struktur + Commitment | M1-M6 |

### 7.3 Verhaltensökonomische Hebel pro Intervention

| Intervention | EBF-Mechanismus | Erwarteter γ-Effekt |
|-------------|----------------|---------------------|
| Cross-GB-KPIs | «What gets measured, gets managed» + Attention Allocation | +0.05 pro betroffenes GB-Paar |
| BL-Peer-Plattform | Social Identity (In-Group-Erweiterung), Peer Effects | +0.08 auf BL↔BL |
| Gemeinsame Zielvereinbarungen | Commitment Devices, Goal Setting Theory | +0.06 pro GB-Paar |
| SOBkulturzug als γ-Plattform | Social Proof, Narrative Transportation | +0.04 auf alle GB-Paare |
| Werte-Operationalisierung | Construal Level (abstrakt→konkret), Implementation Intentions | +0.03 auf alle GB-Paare |
| BL-Identitätserweiterung | Identity Economics, Endowment Reframing | +0.10 auf BL↔BL (langfristig) |
| Customer Experience Team | Superordinate Goals (Sherif), Contact Hypothesis | +0.12 auf V↔M |

---

## 8. BEATRIX-Modell: γ-Optimierung als Kernfunktion

### 8.1 BEATRIX-Integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BEATRIX-MODELL FÜR SOB: γ-OPTIMIERUNG                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INPUT:                                                                │
│  → 5×5 γ-Matrix (IST-Werte)                                           │
│  → gᵢ pro GB (Leistungsindex)                                         │
│  → Blocker B1-B6 mit Effektstärken                                    │
│  → Treiber T1-T5 mit Effektstärken                                    │
│                                                                         │
│  MODELL:                                                               │
│  U_SOB(t) = Σ gᵢ(t) + Σ γᵢⱼ(t) × gᵢ(t) × gⱼ(t)                    │
│                                                                         │
│  γᵢⱼ(t) = γᵢⱼ(0) + Σ T_k(t) - Σ B_l(t)                               │
│  wobei:                                                                │
│  T_k(t) = Treiber-Aktivierungsfunktion (S-Kurve)                     │
│  B_l(t) = Blocker-Reduktionsfunktion (exponentieller Abfall)          │
│                                                                         │
│  OUTPUT:                                                               │
│  → γ-Trajectory über 24 Monate                                        │
│  → Optimale Interventions-Sequenz                                      │
│  → Sensitivitätsanalyse: Welcher Blocker hat grössten Effekt?         │
│  → Kosten-Nutzen pro Intervention                                      │
│                                                                         │
│  CALIBRATION (SOB002 Phase 2):                                         │
│  → IST-Werte aus DOC-004 (MA-Umfrage)                                │
│  → Blocker/Treiber aus DOC-001 bis DOC-011                            │
│  → Validierung durch GL-Workshop                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Sensitivitäts-Analyse: Welcher Blocker zählt am meisten?

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SENSITIVITÄTS-ANALYSE: BLOCKER-IMPACT AUF γ̄                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  BLOCKER                          EFFEKT    MACHBARKEIT   PRIORITÄT    │
│  ───────────────────────────────  ────────  ───────────   ──────────   │
│  B1: GB-Identität > SOB-Identität -0.15    Schwer (24M)  HOCH        │
│  B2: Anreizsystem GB-isoliert     -0.12    Mittel (6M)   SEHR HOCH   │
│  B3: Keine Cross-GB-KPIs          -0.10    Leicht (3M)   SEHR HOCH   │
│  B4: Ressourcenknappheit          -0.08    Schwer        MITTEL       │
│  B5: Fehlende Plattformen         -0.07    Leicht (1M)   HOCH        │
│  B6: Entscheidungswege            -0.05    Mittel (6M)   MITTEL       │
│                                                                         │
│  → B3 (Cross-GB-KPIs) hat das BESTE Verhältnis von                    │
│    Effekt (-0.10) zu Machbarkeit (leicht, 3M).                        │
│  → B2 + B3 zusammen = -0.22 → HALBER Gesamt-Blocker-Effekt!          │
│  → Empfehlung: B3 → B5 → B2 (in dieser Reihenfolge)                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Monitoring: γ-Tracking-Framework

### 9.1 Messbare Indikatoren pro γ-Paar

| GB-Paar | Proxy-Indikator | Quelle | Frequenz |
|---------|-----------------|--------|----------|
| V ↔ I | Gemeinsame Betriebsplanungs-Meetings/Monat | Protokoll | Monatlich |
| V ↔ M | Customer Satisfaction Score (end-to-end) | Kundenbefragung | Quartalsweise |
| V ↔ F | Durchlaufzeit Finanz-Reporting | Systemmessung | Monatlich |
| V ↔ P&O | FK-Entwicklungsteilnahme Transport-Kader | HR-System | Quartalsweise |
| I ↔ M | Gemeinsame Projekte Verkehrsdrehscheiben | Projektliste | Quartalsweise |
| I ↔ F | Investitionsplanung Abweichung IST vs. Plan | Controlling | Quartalsweise |
| I ↔ P&O | Fachkräfte-Besetzungsquote Infrastruktur | HR-System | Monatlich |
| M ↔ F | Business Cases für Innovation (Anzahl) | Projektliste | Quartalsweise |
| M ↔ P&O | Innovations-Kultur-Score (MA-Umfrage Subdim.) | MA-Umfrage | Jährlich |
| F ↔ P&O | HR-Analytics Nutzung (Reports/Quartal) | HR-System | Quartalsweise |
| **Gesamt** | **MA-Umfrage: «Zusammenarbeit über Bereiche» (I4)** | **MA-Umfrage** | **Jährlich** |
| **Gesamt** | **Cross-GB-Projekte (Anzahl aktiv)** | **Projektliste** | **Quartalsweise** |

### 9.2 γ-Trajectory: Erwartete Entwicklung

```
γ̄
0.55 │                                                    ●─── SOLL (0.52)
     │                                              ●───●
0.50 │                                         ●───●
     │                                    ●───●
0.45 │                               ●───●
     │                          ●───●
0.40 │                     ●───●
     │                ●───●
0.35 │           ●───●
     │      ●───●
0.30 │ ●───●
     │●
0.25 │
     └──────────────────────────────────────────────────────
     M0    M3    M6    M9    M12   M15   M18   M21   M24

     Phase 1:        Phase 2:          Phase 3:
     Blocker         Treiber           Identität
     entfernen       aktivieren        transformieren
```

---

## 10. Cross-Referenzen

| Referenz | Relevanz für γ-Analyse |
|----------|------------------------|
| **ANL-001** (Pyramide) | Ebene 4: Strategische Rollen ohne P&O |
| **ANL-002** (Stakeholder) | BL-Readiness 0.45 = γ-Bottleneck |
| **ANL-003** (Gap-Analyse) | Cluster B (Organisations-Integration) = γ-Gaps |
| **DOC-004** (MA-Umfrage) | Quantitative Basis für IST-γ-Schätzung |
| **DOC-005** (KPIs) | 0 Prozess-KPIs = Blocker B3 |
| **DOC-007** (Schwerpunkte) | 22/24 GB-isoliert = γ-Problem operationalisiert |
| **DOC-009** (Auslegeordnung) | K8: Kohärenz-Aussage = γ-Hypothese bestätigt |
| **SYNTHESE** | U_SOB-Gleichung als analytischer Rahmen |
| **EBF Appendix B** | Komplementaritäts-Framework (theoretische Basis) |

---

*Analyse erstellt im Rahmen des SOB-Strategieprojekts SOB001/SOB002 | FehrAdvice & Partners AG*
