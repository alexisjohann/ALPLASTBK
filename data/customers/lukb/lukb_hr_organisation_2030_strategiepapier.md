# Strategiepapier: HR-Organisation LUKB 2030

**Vom «People Department» zum «People Intelligence Model»**

---

| | |
|---|---|
| **Kunde** | Luzerner Kantonalbank AG |
| **Empfänger:innen** | Patricia, Chantal |
| **Erstellt von** | FehrAdvice & Partners AG |
| **Datum** | 25. Februar 2026 |
| **Version** | 1.0 |
| **Klassifikation** | Vertraulich |
| **Kontext** | LUKB30-Strategie, Funktionalstrategie HR 2026-2030 |

---

## 0. Über BEATRIX: Wie diese Analyse entstanden ist

### Was ist BEATRIX?

BEATRIX steht für **Behavioral Economics AI Technology for Research and Implementation eXcellence**. Es ist ein Analysesystem, das von FehrAdvice & Partners gemeinsam mit der Universität Zürich (Prof. Ernst Fehr, Prof. Harald Gall, Prof. Luger) entwickelt wird.

**BEATRIX ist kein klassischer Chatbot.** Während herkömmliche KI-Systeme (wie ChatGPT) Texte auf Basis statistischer Wortwahrscheinlichkeiten generieren, **berechnet** BEATRIX menschliches Verhalten auf der Grundlage von über 2'300 wissenschaftlichen Studien und 850+ dokumentierten Praxisfällen.

### Wie funktioniert das konkret?

BEATRIX arbeitet mit einer sogenannten **Drei-Schichten-Architektur**, die sicherstellt, dass Zahlen und Empfehlungen nachvollziehbar und überprüfbar sind:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHICHT 1: FORMALE BERECHNUNG (Python)                                 │
│  ─────────────────────────────────────────────                          │
│  Deterministische Algorithmen berechnen Parameter, Szenarien            │
│  und Prognosen. Keine «Schätzungen» — echte Mathematik.                │
│                                                                         │
│  → Fehlerquote: 0% (deterministisch, reproduzierbar)                   │
├─────────────────────────────────────────────────────────────────────────┤
│  SCHICHT 2: PARAMETER-DATENBANK (YAML-Registry)                        │
│  ─────────────────────────────────────────────                          │
│  Über 400 Kontextfaktoren für die LUKB, jeder mit Quellenangabe,       │
│  Konfidenzintervall und Validierungsstatus.                             │
│                                                                         │
│  → Beispiel: «Digital Skills Index = 0.58» stammt aus PEO-KOM-003      │
│              (LUKB interne Erhebung), nicht aus einer KI-Schätzung.     │
├─────────────────────────────────────────────────────────────────────────┤
│  SCHICHT 3: KI-ÜBERSETZUNG (Claude)                                     │
│  ─────────────────────────────────────────────                          │
│  Die KI übersetzt die formalen Ergebnisse in verständliche Sprache.    │
│  Sie ERFINDET keine Zahlen — sie ERKLÄRT berechnete Ergebnisse.        │
│                                                                         │
│  → Das LLM ist Übersetzer, nicht Denker.                                │
└─────────────────────────────────────────────────────────────────────────┘
```

**Warum ist das wichtig?** Wenn Sie in diesem Report lesen, dass die Change Readiness bei 0.55 liegt oder dass ~13-15 FTE durch Automatisierung freigesetzt werden, dann sind das keine KI-Halluzinationen — es sind nachvollziehbare Werte aus der LUKB-Kontextdatenbank oder formale Berechnungen auf Basis validierter Parameter.

### Wie trifft BEATRIX Annahmen?

Jede Annahme in diesem Report hat eine von vier Evidenzstufen:

| Stufe | Quelle | Unsicherheit | Beispiel in diesem Report |
|-------|--------|--------------|--------------------------|
| **Tier 1** | Wissenschaftliche Meta-Analysen | Niedrig | «Peer-Commitment bindet stärker» (Cialdini 2001) |
| **Tier 2** | LLMMC-Schätzung (kalibriert) | Mittel | «Change Readiness = 0.55» (basierend auf HR-Einschätzung + Literatur) |
| **Tier 3** | Empirische Kalibrierung | Variabel | «870 Exits in 10 Jahren» (LUKB-Altersstruktur) |
| **Tier 4** | Expert:innen-Einschätzung | Höher | «CAS-Programme dauern 12 Monate» (Erfahrungswerte) |

**Was ist LLMMC?** LLM Monte Carlo ist ein von FehrAdvice entwickeltes Verfahren, bei dem die KI nicht einfach eine Zahl «rät», sondern systematisch Ober- und Untergrenzen abwägt — vergleichbar mit einem Expertengremium, das die Bandbreite diskutiert, bevor es eine Punktschätzung abgibt. Jede LLMMC-Schätzung hat einen Konfidenzbereich (z.B. σ_IDN = 0.68, Range [0.55, 0.80]).

### Wie wurde die LUKB-Analyse erstellt?

Konkret flossen drei Datenebenen in dieses Strategiepapier ein:

```
EBENE 1: MACRO-KONTEXT (Schweiz / Banking)
├── Schweizer Bankenmarkt-Dynamik (SNB Guidance, VSKB Outlook)
├── Regulatorisches Umfeld (FINMA, Staatsgarantie)
└── Wirtschaftsraum Zentralschweiz (BIP +1.5-2.0%, Bevölkerung +0.8%)

EBENE 2: MESO-KONTEXT (LUKB Organisation)
├── LUKB Geschäftsbericht 2024 (1'181 FTE, Konzerngewinn 286.6M CHF)
├── LUKB30-Strategie (5 Säulen: DEFEND, EXPAND, DATA, DIVERSIFY, EFFICIENT)
├── Funktionalstrategie HR 2026-2030 (4 Hauptfelder)
├── Führungsverständnis L-U-K-B
└── 400+ organisatorische Kontextfaktoren (CVA STANDARD)

EBENE 3: MICRO-KONTEXT (HR-Organisation)
├── HR-Organisationsstruktur (50 FTE, 4-Säulen-Modell)
├── PEO-Daten: Kompetenzen, Führung, Fluktuation, Demografie
├── Behavioral Parameters (Identity, Social, Commitment, Efficacy)
└── Reskilling-Machbarkeitsschätzungen (LLMMC)
```

Alle 400+ Kontextfaktoren sind in der LUKB-Kundendatenbank hinterlegt, mit Quellenangabe und Aktualisierungsdatum. Die vollständige Annahmen-Datenbank ist unter `lukb_assumptions.yaml` dokumentiert und kann jederzeit eingesehen, hinterfragt und aktualisiert werden.

### Was unterscheidet BEATRIX von einem klassischen KI-Report?

| Aspekt | Klassische KI (z.B. ChatGPT) | BEATRIX |
|--------|------------------------------|---------|
| **Datenquelle** | Trainings-Daten (Internet) | 400+ LUKB-spezifische Kontextfaktoren |
| **Berechnung** | Statistische Wortwahrscheinlichkeit | Deterministische Formeln + verhaltensökon. Modelle |
| **Nachvollziehbarkeit** | «Black Box» — Ergebnis nicht prüfbar | Jede Zahl hat eine Quelle und einen Berechnungsweg |
| **Annahmen** | Implizit, nicht dokumentiert | Explizit mit Konfidenz-Ranges (z.B. 0.55 [0.40, 0.70]) |
| **Wissenschaftliche Basis** | Allgemeinwissen | 2'300+ kuratierte Studien (Fehr, Kahneman, Thaler et al.) |
| **Praxisbezug** | Generische «Best Practices» | 850+ dokumentierte Fälle aus DACH-Projekten |
| **Kontext** | Ignoriert oder halluziniert | 8 Ψ-Dimensionen systematisch analysiert |
| **Aktualisierbar** | Nein (eingefroren) | Ja — Kontextdaten werden laufend aktualisiert |

**Die zentrale Botschaft:** Wenn in diesem Report steht, dass der Admin-Anteil von 42% auf 12% sinken soll, dann basiert das nicht auf einer KI-Vermutung, sondern auf:
1. Der aktuellen LUKB-HR-Struktur (50 FTE, Verteilung nach Funktionsbereichen)
2. Benchmarks vergleichbarer Transformationen (Literatur + FehrAdvice-Projekte)
3. Konkreten Automatisierungspotentialen (Prozessautomatisierung heute 55%, Ziel 75%)
4. Validierter Reskilling-Machbarkeit (LLMMC mit Ranges, nicht Einzelwerte)

### Wie können Sie die Ergebnisse hinterfragen?

Jede Zahl in diesem Report kann auf Wunsch bis zur Originalquelle zurückverfolgt werden. Fragen Sie zum Beispiel:

- **«Woher kommt die Zahl 870 Exits?»** → Demografische Analyse der LUKB-Altersstruktur (Durchschnittsalter 42.5, PEO-DEM-003)
- **«Warum 37 FTE statt 40?»** → Formale Berechnung aus Automatisierungspotential + Nicht-Nachbesetzungsquote
- **«Ist 65% Machbarkeit für Reskilling realistisch?»** → LLMMC-Schätzung basierend auf Kompetenz-Distanz + Literatur zu Reskilling-Programmen

Diese Transparenz ist kein Zufall — sie ist das Designprinzip von BEATRIX.

---

## Executive Summary

Die LUKB hat mit ihrem heutigen HR-Modell — HRBP, Expert Team, Operations, Payroll — eine solide Grundlage geschaffen. Die Organisation funktioniert, die Prozesse laufen, das Team hat sich bewährt. Dieses Fundament ist wertvoll.

Gleichzeitig stellt die Strategie LUKB30 neue Anforderungen an HR: Die demografische Entwicklung (870 altersbedingte Abgänge in 10 Jahren), die nationale Expansion und die zunehmende Bedeutung von Daten und KI erfordern Fähigkeiten, die im heutigen Modell noch nicht im Fokus stehen — etwa Workforce Analytics, strategische Personalplanung oder HR-Technologie.

**Unsere Überlegung:** Aufbauend auf den bestehenden Stärken schlagen wir eine schrittweise Weiterentwicklung in Richtung eines **«People Intelligence Model»** vor — mit drei spezialisierten Einheiten, die gezielt auf die LUKB30-Anforderungen ausgerichtet sind. Administrative Tätigkeiten werden durch Automatisierung reduziert, die frei werdende Kapazität fliesst in Beratung, Analytics und Technologie.

**Wichtig:** Dieser Vorschlag ist als Diskussionsgrundlage gedacht, nicht als fertiger Beschluss. Die konkreten Schritte, das Tempo und die Prioritäten sollten gemeinsam mit dem HR-Team und der GL entwickelt werden. Der Umbau kann über natürliche Fluktuation (~3-4 Abgänge/Jahr im HR) und gezieltes Reskilling erfolgen — ohne Stellenabbau.

| Kennzahl | Heute (2024) | Mögliches Ziel (2030) | Entwicklungsrichtung |
|----------|-------------|----------------------|---------------------|
| HR FTE | ~50 | ~37 | Schrittweise über natürliche Fluktuation |
| HR Ratio | 1:24 | 1:32 | Effizienzgewinn durch Automatisierung |
| Admin-Anteil | 42% | ~12% | Kapazität wird für Beratung & Analytics frei |
| Analytics-Anteil | 8% | ~22% | Neue Kernkompetenz für datenbasierte Steuerung |
| Rollen in Entwicklung | — | ~18 Rollen | Bestehende MA wachsen in neue Profile |
| Neue Profile | — | 8 Rollen | Grösstenteils intern besetzbar |
| Externe Hires | — | 2-3 | Nur für hochspezialisierte Schlüsselrollen |

---

## 1. Ausgangslage: Wo die LUKB heute steht

### 1.1 Was heute gut funktioniert

Bevor wir über Veränderung sprechen, lohnt sich ein Blick auf die Stärken der heutigen HR-Organisation:

- **Solide Grundstruktur:** Das Ulrich-Modell mit HRBP, Expert Team, Operations und Payroll ist etabliert und liefert zuverlässig.
- **Hohe Reputation:** HR hat unter Silvanas Leitung in 2.5 Jahren deutlich an Standing gewonnen.
- **GL-Alignment:** Die Geschäftsleitung steht hinter der HR-Strategie (Confidence: 0.80).
- **Tiefe Organisationskenntnis:** Mit durchschnittlich 11.5 Jahren Betriebszugehörigkeit kennt das HR-Team die LUKB wie kaum jemand sonst.

Dieses Fundament ist ein echtes Asset — und der Ausgangspunkt für die Weiterentwicklung.

### 1.2 Fünf strategische Entwicklungsfelder

Mit LUKB30 entstehen neue Anforderungen, die über das heutige Aufgabenspektrum hinausgehen. Nicht weil das heutige Modell schlecht ist — sondern weil sich die Anforderungen verändern:

**Entwicklungsfeld 1: Demografischer Wandel vorausschauend begleiten**
Mit einem Durchschnittsalter von 42.5 Jahren werden in den nächsten 10 Jahren rund 870 Positionen durch Pensionierungen frei. Das ist eine grosse Chance — wenn die Nachfolge rechtzeitig geplant wird. Strategische Personalplanung kann hier einen entscheidenden Beitrag leisten.

**Entwicklungsfeld 2: Skill-Shift bei der KI-Transformation begleiten**
Die LUKB30-Säule S3-DATA wird viele Rollenprofile verändern. HR kann hier eine Schlüsselrolle spielen — nicht nur beim Recruiting, sondern vor allem beim systematischen Reskilling bestehender Mitarbeitender. Dafür wäre der Aufbau von People Analytics und strukturierter Kompetenzentwicklung hilfreich.

**Entwicklungsfeld 3: Nationale Expansion kulturell unterstützen**
Der Schritt vom Luzerner Heimatmarkt auf die nationale Bühne (Private Banking schweizweit) bringt neue Fragen: Wie entwickeln sich Karrierepfade? Wie wirkt die Employer Brand über die Region hinaus? HR kann diesen Kulturwandel aktiv mitgestalten.

**Entwicklungsfeld 4: LUKB30-Strategieumsetzung unterstützen**
Fünf Säulen gleichzeitig umsetzen (DEFEND, EXPAND, DATA, DIVERSIFY, EFFICIENT) ist anspruchsvoll. Die 40 Kader als Multiplikatoren könnten von einer stärker strategisch ausgerichteten HR-Begleitung profitieren.

**Entwicklungsfeld 5: HR-Daten als Entscheidungsgrundlage nutzen**
Die Funktionalstrategie HR 2026-2030 definiert «HR Data Analytics» als eigenes Feld (4B). Hier liegt Potential: Datenbasierte Einblicke können HR-Entscheide fundieren und den Wertbeitrag von HR sichtbarer machen. Der aktuelle Digital Skills Index von 0.58 zeigt, dass hier Entwicklungspotential besteht.

### 1.3 Wo könnten neue Fähigkeiten helfen?

| Anforderung LUKB30 | Heutige Stärke | Entwicklungspotential |
|---------------------|---------------|----------------------|
| 870 Exits vorausschauend steuern | Gute Organisationskenntnis | + Systematisches Workforce Planning |
| Skill-Shift bei KI-Transformation | Engagiertes L&D-Team | + People Analytics & strukturiertes Reskilling |
| Datenbasierte Steuerung | Zuverlässiges Reporting | + Dashboards & Predictive Analytics |
| Change-Begleitung Kader | Vertrauensvolle HRBP-Beziehungen | + Strategische Transformationsbegleitung |
| Employee Experience | Hohe Mitarbeiterzufriedenheit | + Systematisches EX-Design |
| HR-Technologie | Stabile Systeme | + Automatisierung & AI-Tools |
| Talent am Markt finden | Funktionierendes Recruiting | + Talent Intelligence & Active Sourcing |

---

## 2. Zielmodell: Das «People Intelligence Model» 2030

### 2.1 Architektur: 3 Einheiten + Leitung

Wir schlagen eine Neuorganisation in drei spezialisierte Einheiten vor, die direkt auf die LUKB30-Strategie ausgerichtet sind:

```
                    ┌─────────────────────────────────────┐
                    │   PEOPLE LEADERSHIP                 │
                    │   Silvana + Stab (~3-4 FTE)         │
                    │                                     │
                    │   Strategie · GL-Interface           │
                    │   Budget · Governance                │
                    └────────────┬────────────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│ PEOPLE PARTNERS   │  │ PEOPLE STRATEGY   │  │ PEOPLE EXPERIENCE │
│ (~8-10 FTE)       │  │ & INTELLIGENCE    │  │ & TECHNOLOGY      │
│                   │  │ (~14-16 FTE)      │  │ (~10-12 FTE)      │
│ Strategische      │  │                   │  │                   │
│ Beratung der      │  │ Workforce         │  │ HR Tech & AI      │
│ Geschäfts-        │  │ Analytics         │  │                   │
│ bereiche          │  │                   │  │ Employee           │
│                   │  │ Workforce         │  │ Experience         │
│ Change &          │  │ Planning          │  │                   │
│ Transformation    │  │                   │  │ HR Operations      │
│                   │  │ Talent &          │  │ (Lean)             │
│ OD-Beratung       │  │ Succession        │  │                   │
│                   │  │                   │  │ Payroll            │
│ Coaching          │  │ Change & OD       │  │ (automatisiert)    │
│                   │  │                   │  │                   │
│                   │  │ Total Rewards     │  │                   │
│                   │  │ Strategy          │  │                   │
└───────────────────┘  └───────────────────┘  └───────────────────┘

  LUKB30-Säulen:       LUKB30-Säulen:         LUKB30-Säulen:
  S1, S2 (nah am       S2, S3, S4             S3, S5
  Geschäft)            (strategisch)          (Effizienz)
```

### 2.2 Einheit 1: People Partners (~8-10 FTE)

**Mission:** Strategische Beratung der Geschäftsbereiche bei organisatorischen und personellen Fragen — nicht mehr operatives Trouble-Shooting.

| Aspekt | Heute (HRBP) | 2030 (People Partner) |
|--------|-------------|----------------------|
| Fokus | Operativ, reaktiv | Strategisch, proaktiv |
| Zeitaufteilung | 70% Admin, 30% Beratung | 20% Admin, 80% Beratung |
| Skills | Arbeitsrecht, Konflikte | Change, OD, Dateninterpretation |
| Zuordnung | 1 HRBP pro Bereich | 1 Partner pro GL-Mitglied |
| Wertbeitrag | Probleme lösen | Transformation ermöglichen |

**Kernaufgaben:**
- Strategische Beratung der Bereichsleitungen (1:1 mit GL-Mitgliedern)
- Change-Begleitung bei LUKB30-Initiativen
- OD-Interventionen (Teamdesign, Reorganisationen, Kulturentwicklung)
- Übersetzung von People Analytics in Geschäftsentscheide
- Coaching von Führungskräften

### 2.3 Einheit 2: People Strategy & Intelligence (~14-16 FTE)

**Mission:** Das «Gehirn» der HR-Organisation. Daten, Planung und Fachexpertise für evidenzbasierte People-Entscheide.

**5 Unterteams:**

| Team | FTE | Kernaufgaben | LUKB30-Bezug |
|------|-----|-------------|-------------|
| **Workforce Analytics** | 3-4 | Dashboards, Predictive Modelling, HR-KPIs, Datenqualität | S3-DATA |
| **Workforce Planning** | 2-3 | 870-Exit-Steuerung, Szenarioplanung, FTE-Simulation, Rollencluster | S2-EXPAND |
| **Talent & Succession** | 3-4 | Assessment, Potenzialdiagnostik, Skills Taxonomie, Nachfolgeplanung | S1-DEFEND |
| **Change & OD** | 3-4 | Kulturdiagnostik, Organisationsdesign, Workshop-Facilitation | Alle Säulen |
| **Total Rewards Strategy** | 2-3 | Marktanalyse, Vergütungsmodellierung, Benefits, Exec Comp | S5-EFFICIENT |

### 2.4 Einheit 3: People Experience & Technology (~10-12 FTE)

**Mission:** Exzellente Mitarbeitererfahrung durch Technologie und schlanke Prozesse.

| Funktion | FTE | Kernaufgaben | Veränderung vs. heute |
|----------|-----|-------------|----------------------|
| **HR Tech & AI** | 3-4 | HRIS, RPA, AI-Tools, Workflow-Automation | Neu (aus Ops reskilled) |
| **Employee Experience** | 2-3 | Journey Mapping, Touchpoints, Onboarding 2.0 | Neu (aus Ops/Recruiting) |
| **HR Operations (Lean)** | 3-4 | Kernprozesse, Quality, Compliance | Stark reduziert (von ~12) |
| **Payroll (automatisiert)** | 2-3 | System-Monitoring, Exceptions, SV-Expertise | Stark reduziert (von ~9) |

### 2.5 FTE-Verschiebung im Detail

```
HEUTE (50 FTE)                              2030 (37 FTE)
─────────────────────────                   ─────────────────────────

HR-Leitung + Stab     7 ─────────────────► People Leadership     4  (-3)
HRBP                  10 ─────────────────► People Partners      10  ( 0)
                          ┌───────────────► Workforce Analytics    4
Expert Team (CoE)     12 ─┤               ► Workforce Planning    3
                          ├───────────────► Talent & Succession   4
                          ├───────────────► Change & OD           3  (-2)
                          └───────────────► Total Rewards         3
                          ┌───────────────► HR Tech & AI          4
Operations            12 ─┤               ► Employee Experience   3
                          └───────────────► HR Ops (Lean)         4  (-1)
Payroll                9 ─────────────────► Payroll (auto)        3  (-6)
                                           ── Nicht-Nachbesetzung ── (-1)
                     ────                                        ────
                      50                                          37
```

---

## 3. Skills-Transformation: Vom IST zum SOLL

### 3.1 Skills-Verteilung: Der fundamentale Shift

```
                         HEUTE (2024)                    ZIEL (2030)

Administrativ/        ████████████████████  42%          ████         12%
Transaktional

Beratung/             ██████████            22%          ████████████████  35%
Strategisch

Analytics/            ████                   8%          ██████████   22%
Data

Tech/                 —                      0%          ████████     18%
Digital

OD/                   ████████              18%          ██████       13%
Fachexpertise
+ Strategie/Projekt   ████                  10%
```

**Kernaussage:** Der Anteil administrativ-transaktionaler Arbeit sinkt um 30 Prozentpunkte. Diese Kapazität wird zu strategischer Beratung (35%), Analytics (22%) und Technologie (18%) umgebaut.

### 3.2 Neue Skills: Was aufgebaut werden muss

#### Priorität 1 — Kritisch (sofort starten, 2026)

| Skill-Cluster | Warum kritisch | Heutige Abdeckung | Ziel-FTE |
|--------------|---------------|-------------------|---------|
| **People Analytics** | 870 Exits managen, datenbasierte HR-Entscheide | ~0% | 3-4 |
| **AI / HR Tech** | Automatisierung 55%→75%, LUKB30-Säule S3-DATA | ~5% | 3-4 |
| **Workforce Planning** | 870-Exit-Steuerung, nationale Expansion planen | ~5% | 2-3 |
| **Change & OD** | LUKB30-Transformation, Change Leadership 0.55→0.75 | ~15% | 3-4 |

**People Analytics** umfasst: Python/R, Statistik, Dashboard-Design (Power BI/Tableau), Predictive Modelling, HR-Datenmodellierung

**AI / HR Tech** umfasst: HRIS-Architektur, RPA-Automatisierung, AI-Prompt-Engineering, Workflow-Design, Vendor Management

**Workforce Planning** umfasst: Szenarioplanung, FTE-Simulationen, Rollencluster-Design, Arbeitsmarktanalyse, Finanzmodellierung

**Change & OD** umfasst: Organisationsdesign, Kulturdiagnostik, Workshop-Facilitation, Verhaltensökonomie, Kommunikationsdesign

#### Priorität 2 — Wichtig (bis 2028)

| Skill-Cluster | Warum wichtig | Heutige Abdeckung | Ziel-FTE |
|--------------|-------------|-------------------|---------|
| **Employee Experience Design** | Differenzierung im Arbeitsmarkt | ~10% | 2-3 |
| **Data Storytelling** | HR als strategischer Partner auf GL-Ebene | ~5% | — |
| **Learning Architecture** | Wissenstransfer bei 870 Exits | ~10% | 1-2 |
| **Agile Methoden** | Agile Teams 15%→35% | ~5% | — |

#### Priorität 3 — Differenzierung (bis 2030)

| Skill-Cluster | Beschreibung |
|--------------|-------------|
| Predictive HR Modelling | Turnover Prediction, Performance Forecasting |
| Behavioral Nudging im HR | Verhaltensökonomische Kommunikation |
| HR Venture Building | Neue HR-Services als interne Produkte |

### 3.3 Obsolete Skills: Was nicht mehr gebraucht wird

| Skill | Grund für Obsoleszenz | Zeithorizont | Freigesetzte FTE |
|-------|---------------------|-------------|-----------------|
| Manuelle Lohnabrechnung | HRIS-Automatisierung + AI-Prüfung | 2026-2028 | ~5 |
| Physische Dossierführung | Digitale Personalakte + DMS | 2026-2027 | ~3 |
| Manuelle Zeugniserstellung | AI-generierte Zeugnisse mit Freigabe | 2027-2028 | ~2 |
| Standard Excel-Reporting | Automatisierte Dashboards | 2026-2027 | ~2 |
| Manuelle Vertragserstellung | Template Engine + digitale Signatur | 2026-2027 | ~2 |
| Administrative CV-Sichtung | AI-Prescreening mit Human-Freigabe | 2027-2028 | ~2 |
| Stelleninserate texten & schalten | AI-generiert, programmatische Ausspielung | 2027-2028 | ~1 |
| Operatives HRBP-Troubleshooting | Self-Service + strategische Beratung | 2027-2029 | ~3 |
| **Total** | | | **~13-15 FTE** |

---

## 4. Profile: Entwicklung und Neuausrichtung

### 4.1 Profile, die sich weiterentwickeln

Durch Automatisierung und veränderte Anforderungen werden sich einige heutige Rollenprofile verändern. Das bedeutet nicht, dass die Mitarbeitenden in diesen Rollen überflüssig werden — im Gegenteil: Ihre Organisationskenntnis und Erfahrung sind die Grundlage für den nächsten Entwicklungsschritt.

| Heutiges Profil | Heutige FTE | Mögliche FTE 2030 | Entwicklungsrichtung |
|----------------|------------|------------------|---------------------|
| Payroll-Sachbearbeiter:in | ~6 | ~2 | HRIS übernimmt Routine → MA entwickeln sich zu Payroll Experts oder Data Analysts |
| HR-Sachbearbeiter:in / HR-Admin | ~8 | ~3 | Self-Service + Automation → MA wachsen in EX-Design oder HR Ops (Lean) |
| Junior HRBP (operativ) | ~4 | — | Profil verschmilzt mit People Partner oder People Experience |
| HR Reporting Analyst | ~2 | — | Wird zu People Data Analyst (breiteres Spektrum, gleiche Grundkompetenz) |
| Klassische:r Recruiter:in | ~3 | — | Wird zu Talent Intelligence Specialist (Active Sourcing, AI-Tools) |
| **Gesamt in Entwicklung** | **~23** | **~5 verbleibend** | **~18 MA entwickeln sich in neue Profile** |

### 4.2 Neue Job-Profile

| Neues Profil | FTE | Woher (Reskilling) | Kern-Skills |
|-------------|-----|--------------------|-------------|
| **People Analytics Lead** | 1 | Extern | Python/R, HR-Datenmodell, Stakeholder-Kommunikation |
| **People Data Analyst** | 2-3 | HR Reporting, Payroll | SQL, Power BI, ETL, Dashboard-Design |
| **Strategic Workforce Planner** | 2-3 | HR-Stab, HRBP | Szenariomodellierung, FTE-Simulation |
| **HR Tech / AI Specialist** | 2-3 | HR Ops | HRIS-Architektur, RPA, AI-Integration |
| **Employee Experience Designer** | 2-3 | HR Ops, Recruiting | Service Design, Journey Mapping, Feedback-Systeme |
| **Transformation Partner** | 2-3 | HRBP | OD, Change Management, Workshop-Facilitation |
| **Learning Architect** | 1-2 | L&D | Skills Taxonomie, Adaptive Learning, LMS |
| **Talent Intelligence Specialist** | 1-2 | Recruiting | Active Sourcing, Arbeitsmarkt-Intelligence, AI-Tools |

---

## 5. Reskilling: Wer wird was?

### 5.1 Reskilling-Matrix

Die zentrale Frage: Welche heutigen Mitarbeitenden können in welche Zukunftsrollen entwickelt werden?

| Heutige Rolle | Zukunftsrolle | Aufwand | Machbarkeit |
|--------------|--------------|---------|-------------|
| **Payroll-Sachbearbeiter:in** | → People Data Analyst | 12 Monate | 65% |
| | → HR Tech Support | 9 Monate | 75% |
| | → Payroll Expert (verbleibt) | 3 Monate | 95% |
| **HR-Sachbearbeiter:in** | → Employee Experience Designer | 9 Monate | 70% |
| | → HR Ops (Lean) | 6 Monate | 80% |
| | → People Data Analyst | 12 Monate | 55% |
| **Junior HRBP** | → Transformation Partner | 9 Monate | 70% |
| | → People Partner | 6 Monate | 80% |
| | → Employee Experience Designer | 9 Monate | 65% |
| **Senior HRBP** | → People Partner | 6 Monate | 85% |
| | → Strategic Workforce Planner | 9 Monate | 60% |
| **Recruiter:in** | → Talent Intelligence Specialist | 9 Monate | 75% |
| | → Employer Brand Manager | 6 Monate | 80% |
| **L&D-Verantwortliche:r** | → Learning Architect | 9 Monate | 70% |
| | → Change Partner | 12 Monate | 55% |
| **C&B Specialist** | → Total Rewards Strategist | 6 Monate | 85% |
| | → Strategic Workforce Planner | 9 Monate | 65% |
| **HR Reporting** | → People Data Analyst | 9 Monate | 75% |

**Lesehinweis:** Machbarkeit >70% = realistisch, 50-70% = möglich mit Investition, <50% = kritisch.

### 5.2 Kritische Erfolgsfaktoren Reskilling

1. **Individuelle Entwicklungspläne** statt Giesskanne — jede:r HR-Mitarbeitende braucht einen persönlichen Pfad
2. **Learning by Doing** — CAS-Programme kombiniert mit LUKB30-Praxisprojekten
3. **Psychologische Sicherheit** — Angst vor Veränderung ernst nehmen; Change Readiness im HR selbst bei 0.55
4. **Freiwilligkeitsprinzip** — Wer in der heutigen Rolle verbleiben möchte (Payroll Expert, HR Ops Lean), kann das
5. **Zeitfenster nutzen** — Natürliche Fluktuation (~3-4/Jahr) ermöglicht schrittweisen Umbau ohne Druck

---

## 6. Umsetzungsroadmap: 3 Phasen

### Phase 1: Foundation (2026-2027)

**Ziel:** Grundlagen schaffen, Quick Wins realisieren, erste Automatisierungen.

| Massnahme | Zielgruppe | Format | Dauer |
|-----------|-----------|--------|-------|
| Data Literacy Bootcamp | Alle 50 HR-MA | Blended (2 Tage Präsenz + E-Learning) | 3 Monate |
| Power BI / Dashboard Training | 8-10 aus Reporting + Payroll | Praxis-Workshop + Projekt | 6 Monate |
| HRIS Deep Dive | 6-8 aus Ops + Payroll | Zertifizierung + IT-Shadowing | 4 Monate |
| Strategic HRBP Upgrade | 6-8 HRBPs | Coaching + Case-based Learning | 6 Monate |
| Self-Service-Portal (Pilot) | HR Ops | Implementierung + Change | 6 Monate |

**Organisatorisch:**
- People Leadership Team formieren (Silvana + 3 Stab)
- Workforce Analytics als erste neue Funktion aufbauen (1-2 FTE)
- HRIS-Modernisierungsprojekt starten
- **Externe Rekrutierung:** People Analytics Lead

**Quick Wins:**
- Automatisierte Dashboards ersetzen Excel-Reports (Q2 2026)
- Digitale Personalakte einführen (Q3 2026)
- AI-gestütztes Zeugnis-Tool pilotieren (Q4 2026)

### Phase 2: Rebuild (2027-2028)

**Ziel:** Neue Einheiten aufbauen, Profilwechsel durchführen, Automatisierung skalieren.

| Massnahme | Zielgruppe | Format | Dauer |
|-----------|-----------|--------|-------|
| People Analytics Programm | 3-4 aus Reporting/Payroll | CAS Data Science (HSLU/ZHAW) + Praxisprojekt | 12 Monate |
| OD & Change Zertifizierung | 3-4 aus HRBP | CAS OD (extern) + LUKB30-Projekte | 12 Monate |
| Service Design für HR | 3-4 aus Ops/Recruiting | Design Thinking + EX-Projekt | 6 Monate |
| HR Tech / AI Academy | 3-4 aus Ops | RPA-Zertifizierung + AI in HR | 9 Monate |

**Organisatorisch:**
- 3-Einheiten-Struktur offiziell einführen (Q1 2028)
- People Strategy & Intelligence als Einheit formieren
- People Experience & Technology als Einheit formieren
- Workforce Planning operativ machen (870-Exit-Steuerung)
- **Externe Rekrutierung:** HR Tech / AI Architect

### Phase 3: Excellence (2029-2030)

**Ziel:** Spezialisierung vertiefen, Predictive Analytics, volle Automatisierung.

| Massnahme | Zielgruppe | Format |
|-----------|-----------|--------|
| Predictive Workforce Modelling | Analytics-Team | Advanced Analytics + ML |
| Behavioral HR Design | Change & EX Team | EBF-Methodik |
| Strategic Workforce Planning Mastery | WFP-Team | Szenario-Workshops + Tools |

**Organisatorisch:**
- Prozessautomatisierung bei 75% (von heute 55%)
- HR Ratio bei 1:32 (von heute 1:24)
- People Analytics liefert Predictive Insights an GL
- Employee Experience Journey vollständig digitalisiert

### Phasenüberblick

```
2026         2027         2028         2029         2030
──┬────────────┬────────────┬────────────┬────────────┬──
  │            │            │            │            │
  │  PHASE 1:  │            │            │            │
  │  FOUNDATION│            │            │            │
  │  ──────────│            │            │            │
  │  Data      │  PHASE 2:  │            │            │
  │  Literacy  │  REBUILD   │            │            │
  │  HRIS      │  ──────────│            │            │
  │  Quick     │  CAS-      │  PHASE 3:  │            │
  │  Wins      │  Programme │  EXCELLENCE│            │
  │            │  Neue      │  ──────────│            │
  │  Hire:     │  Einheiten │  Predictive│  ZIEL-     │
  │  Analytics │            │  Analytics │  ZUSTAND   │
  │  Lead      │  Hire:     │  Behavioral│  ERREICHT  │
  │            │  HR Tech   │  Design    │            │
  │            │  Architect │            │            │
──┴────────────┴────────────┴────────────┴────────────┴──

  ~50 FTE       ~45 FTE      ~40 FTE      ~38 FTE     ~37 FTE
  Ulrich 4P     Hybrid       3 Einheiten  Optimierung  People
                                                      Intelligence
```

---

## 7. Investitionen und ROI

### 7.1 Investitionsübersicht

| Position | Betrag (CHF) | Zeitraum | Bemerkung |
|----------|-------------|----------|-----------|
| Reskilling HR-intern (CAS, Zertifizierungen) | ~450'000 | 2026-2028 | 12-15 Personen |
| Weiterbildungsbudget HR (Erhöhung) | +700'000 | 2026-2028 | Von 2.8M auf 3.5M |
| HRIS-Modernisierung (HR-Anteil) | ~200'000 | 2026-2027 | Anteil IT-Projekt |
| Tool-Lizenzen (Power BI, RPA, AI) | ~80'000/Jahr | 2026-2030 | Laufend |
| Externe Rekrutierung (2-3 Personen) | ~120'000 | 2026-2028 | Headhunter + Onboarding |
| **Total Einmalig** | **~1'470'000** | | |
| **Total Laufend** | **~80'000/Jahr** | | |

### 7.2 Return on Investment

| Einsparung | Betrag (CHF/Jahr) | Ab wann |
|------------|-------------------|---------|
| -13 FTE durch Nicht-Nachbesetzung | ~2'000'000 | 2028 |
| Prozessautomatisierung (Effizienz) | ~300'000 | 2027 |
| Reduzierte externe Beratung (OD/Change intern) | ~200'000 | 2028 |
| Besseres Workforce Planning (vermiedene Fehlbesetzungen) | ~500'000 | 2029 |
| **Total jährliche Einsparung** | **~3'000'000** | **ab 2029** |

**Payback Period:** ~18 Monate (Investition 1.47M, jährliche Einsparung 3.0M ab 2029)

### 7.3 Nicht-monetärer Nutzen

- **HR als strategischer Partner:** Erstmals datenbasierte Entscheidungsgrundlagen für GL
- **870-Exit-Risiko mitigiert:** Proaktive statt reaktive Personalplanung
- **LUKB30-Beschleunigung:** Dedizierte Change- und Transformationskompetenz im HR
- **Employer Brand:** «People Intelligence» als Differenzierungsmerkmal im Arbeitsmarkt
- **Alignment mit Führungsverständnis:** L-U-K-B Werte operativ verankert (kollaborativ, bemerkenswert)

---

## 8. Alignment mit Funktionalstrategie HR 2026-2030

Das People Intelligence Model ist bewusst auf die vier Hauptfelder der bestehenden Funktionalstrategie ausgerichtet:

| Hauptfeld HR-Strategie | Verantwortliche Einheit 2030 | Wie |
|------------------------|-----------------------------|----|
| **1. Führung & Organisation** (Fokus 1A, 1B) | People Partners + Change & OD | Transformation Partners beraten GL, Change & OD gestaltet Strukturen |
| **2. Retention, Talent & Performance** (Fokus 2C) | Talent & Succession + Workforce Planning | Systematische Nachfolgeplanung, Skills-basiertes Performance Mgmt. |
| **3. Employer Branding & Rekrutierung** (Fokus 3A) | Employee Experience + Talent Intelligence | EX als Differenzierung, AI-gestütztes Active Sourcing |
| **4. HR Prozesse & Daten** (4A, 4B) | Workforce Analytics + HR Tech & AI | Dashboards, Automatisierung, Predictive Analytics |

**Kernpunkt:** Das People Intelligence Model löst keine Strategiefelder auf — es gibt ihnen eine organisatorische Heimat mit klarer Verantwortung und den richtigen Skills.

---

## 9. Risiken und Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|-----------|
| **Widerstand im HR-Team** gegen Profilwechsel | Mittel (0.55 Change Readiness) | Hoch | Freiwilligkeitsprinzip, individuelle Entwicklungspläne, psychologische Sicherheit |
| **Analytics-Talent nicht findbar** am Markt | Mittel | Hoch | Frühzeitig starten (Q1 2026), HSLU/ZHAW-Netzwerk nutzen, alternativ intern aus Finance/Risk |
| **HRIS-Modernisierung verzögert** sich | Mittel | Mittel | Automatisierung unabhängig von HRIS starten (RPA-Brücke) |
| **Überlastung in Übergangsphase** | Hoch | Mittel | Phase 1 priorisiert Quick Wins, keine Big-Bang-Umstellung |
| **GL-Commitment schwindet** | Niedrig (0.80 Confidence) | Hoch | Regelmässiges Reporting, Quick Wins sichtbar machen |
| **Natürliche Fluktuation reicht nicht** | Niedrig (6.8% = ~3-4/Jahr) | Mittel | Interne Mobilität (Transfer in andere Bereiche) als Alternative |

---

## 10. Empfehlung und nächste Schritte

### Empfehlung

Dieses Strategiepapier ist als Grundlage für die gemeinsame Diskussion gedacht. Wir empfehlen, die Ideen im HR-Leitungsteam zu besprechen, zu priorisieren und gemeinsam einen Umsetzungsplan zu entwickeln. Der schrittweise Aufbau in drei Phasen erlaubt es, das Tempo an die Realität und die Kapazitäten des Teams anzupassen.

### Mögliche nächste Schritte

| # | Vorgeschlagene Aktion | Wer könnte beteiligt sein | Möglicher Zeitrahmen |
|---|----------------------|--------------------------|---------------------|
| 1 | Strategiepapier im HR-Leitungsteam besprechen und gemeinsam priorisieren | Patricia, Chantal, Silvana | März 2026 |
| 2 | Individuelle Entwicklungsgespräche mit HR-Mitarbeitenden führen | HR-Leitung | April-Mai 2026 |
| 3 | Persönliche Entwicklungspläne gemeinsam erarbeiten | HR-Leitung + Mitarbeitende | Mai-Juni 2026 |
| 4 | Bedarf für Schlüsselrollen klären (z.B. People Analytics Lead) | Silvana + Recruiting | Q2 2026 |
| 5 | Data Literacy Angebot für interessierte HR-Mitarbeitende starten | L&D | Q2-Q3 2026 |
| 6 | HRIS-Modernisierung als gemeinsames Projekt mit IT prüfen | HR + IT | Q2-Q3 2026 |
| 7 | Erste Quick Wins identifizieren und pilotieren | HR Ops | Q3-Q4 2026 |
| 8 | Weiterbildungsprogramme für Phase 2 evaluieren | HR-Leitung | Q4 2026 |

---

## Anhang

### A. Datengrundlage

Dieses Strategiepapier basiert auf folgenden Quellen:

- **LUKB Geschäftsbericht 2024** — Finanzkennzahlen, Organisation
- **Funktionalstrategie HR 2026-2030** — 4 Hauptfelder, Fokusthemen
- **LUKB Führungsverständnis** — L-U-K-B Akronym
- **LUKB30 Unternehmensstrategie** — 5 Säulen (DEFEND, EXPAND, DATA, DIVERSIFY, EFFICIENT)
- **Brand Identity 2026** — «Wir schaffen Raum»
- **FehrAdvice Kontextanalyse** — 400+ Kontextfaktoren (CVA STANDARD)
- **Behavioral Assumptions** — LLMMC-basierte Parameterschätzungen

### B. Kennzahlen-Referenz

| Kennzahl | Quelle | Wert |
|----------|--------|------|
| Total FTE | Geschäftsbericht 2024 | 1'181 |
| HR FTE | CVA-Schätzung | ~50 |
| Durchschnittsalter | PEO-DEM-003 | 42.5 Jahre |
| Fluktuation | PEO-FLU-001 | 6.8% |
| Betriebszugehörigkeit | PEO-DEM-005 | 11.5 Jahre |
| Digital Skills Index | PEO-KOM-003 | 0.58 (Ziel: 0.80) |
| Change Readiness | PEO-KUL-007 | 0.55 |
| Change Leadership | PEO-FUE-012 | 0.55 |
| Prozessautomatisierung | ORG-PRO-002 | 55% (Ziel: 75%) |
| Agile Teams | ORG-STR-013 | 15% (Ziel: 35%) |
| Weiterbildungstage/MA | PEO-KOM-001 | 4.5 Tage |
| Weiterbildungsbudget | PEO-KOM-002 | 2.8M CHF |
| Kaderquote | ORG-STR-008 | 15% (178 Kader) |
| Kader-Verteilung | PEO-FUE-005 | 40 oberes, 80 mittleres, 58 unteres |

### C. Glossar

| Begriff | Definition |
|---------|-----------|
| **People Intelligence Model** | Vorgeschlagenes Zielmodell für die HR-Organisation 2030 mit 3 Einheiten |
| **People Partner** | Weiterentwicklung des HRBP — strategisch statt operativ |
| **Workforce Analytics** | Datenbasierte Analyse von Personalthemen (Turnover, Performance, Engagement) |
| **Workforce Planning** | Strategische Personalplanung inkl. Szenarioanalysen und FTE-Simulation |
| **Employee Experience (EX)** | Gesamtheit der Mitarbeitererfahrung über alle Touchpoints |
| **Reskilling** | Umschulung bestehender Mitarbeitender auf neue Rollenprofile |
| **HRIS** | Human Resources Information System |
| **RPA** | Robotic Process Automation — Automatisierung repetitiver Prozesse |
| **CAS** | Certificate of Advanced Studies — berufsbegleitende Weiterbildung |
| **LUKB30** | Unternehmensstrategie 2026-2030 mit dem Ziel Top-5-Universalbank Schweiz |
| **CVA** | Context Vector Architecture — FehrAdvice-Methodik zur Kontextanalyse |

---

*Erstellt von FehrAdvice & Partners AG | 25. Februar 2026*
*Dieses Dokument ist vertraulich und ausschliesslich für den internen Gebrauch der LUKB bestimmt.*
