# WORKFLOW: Strategische Frage → Output

**Version:** 2.1
**Datum:** 3. Februar 2026

---

## Die 3-Ebenen-Hierarchie (PFLICHT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 1: GRUNDLAGEN DER STRATEGISCHEN ENTSCHEIDUNG                     │
│  SSOT: strategie/GRUNDLAGEN_strategische_entscheidung.md               │
│  MODELL: spo_two_path_model.yaml (MOD-SPO-TWOPATH-001)                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  5 Kernprinzipien:                                                      │
│  • Komplementarität statt Konkurrenz                                    │
│  • Two-Path-Modell (Funktion vs. Ausschluss)                           │
│  • γ-Architektur (Marktsegmentierung)                                  │
│  • Babler-Credibility (Traiskirchen)                                   │
│  • Nicht verteidigen – ordnen                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 2: STRATEGIE "ORDNEN STATT SPALTEN"                              │
│  SSOT: spo_strategiebriefing_parteitag_2026.md                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  4 Transformations-Prinzipien:                                          │
│  TP-1: Framing als «Ordnung» statt «Verbot»                            │
│  TP-2: Staatstragende Tonalität                                        │
│  TP-3: Fokus auf Ergebnisse und Verantwortung                          │
│  TP-4: Selbstbewusste Agenda                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 3: STRATEGISCHE FRAGESTELLUNG                                    │
│  SSOT: TEMPLATE_strategische_fragestellung.yaml                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  → Konkrete Anwendung für EMRK, SOG, Spitals-Touristen, etc.           │
│  → 3 Lieferobjekte: Report, Präsentation, Infografik                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Übersicht: Der 7-Schritte-Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  STRATEGISCHE FRAGE                                                     │
│  "Wie positionieren wir uns zu [THEMA]?"                               │
│                                                                         │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  ★ SCHRITT 0: STRATEGISCHE ABLEITUNG (Komplementarität) ★       │   │
│  │  Welches Kernprinzip (Ebene 1)? Welches TP (Ebene 2)?           │   │
│  │  Was ist die Transformation (Alt → Neu)?                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SCHRITT 1: STAKEHOLDER-LANDSCHAFT                              │   │
│  │  Wie stehen die anderen zu dieser Frage?                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SCHRITT 2: SPÖ/BABLER-POSITION                                 │   │
│  │  Wie ist die derzeitige Position? Was hat Babler gesagt?        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SCHRITT 3: ORDNEN STATT SPALTEN  ★ KERNANALYSE ★               │   │
│  │  Level 1: THEMA ordnen   → Zahlen, Fakten, Ergebnisse          │   │
│  │  Level 2: DEBATTE ordnen → Frame, Konsens, Abgrenzung          │   │
│  │  Level 3: LAND ordnen    → Geschichte, Identität, Werte        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SCHRITT 4: TEMPLATE AUSFÜLLEN                                  │   │
│  │  → TEMPLATE_strategische_fragestellung.yaml (inkl. TEIL 0)      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SCHRITT 5: ERGEBNISSICHERUNG                                   │   │
│  │  Ablage, Versionierung, ANFRAGEN_REGISTER.yaml                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│         │                                                               │
│         ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SCHRITT 6: 3 STANDARD-LIEFEROBJEKTE                            │   │
│  │                                                                 │   │
│  │  ┌────────────┐  ┌────────────────┐  ┌────────────┐             │   │
│  │  │  REPORT    │  │  PRÄSENTATION  │  │ INFOGRAFIK │             │   │
│  │  │ (taktisch) │  │  (12 Slides)   │  │ (5 Zonen)  │             │   │
│  │  └────────────┘  └────────────────┘  └────────────┘             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Kernidee:** Ableitung (0) → Input (1-2) → Kernanalyse (3) → Dokumentation (4-5) → Output (6)

---

## ★ Schritt 0: Strategische Ableitung (Komplementarität)

### Die ERSTE Frage bei JEDEM Thema:

> **Wie leitet sich diese Fragestellung aus der Gesamtstrategie ab?**

### 0.1 Grundlagen-Prinzip wählen (Ebene 1)

| Prinzip | Wann relevant? | Für dieses Thema? |
|:--------|:---------------|:------------------|
| **Komplementarität** | Wenn FPÖ das Terrain besetzt | [ ] Ja [ ] Nein |
| **Two-Path-Modell** | Wenn es um Sicherheit × Identität geht | [ ] Ja [ ] Nein |
| **γ-Architektur** | Wenn wir eigenes Terrain aufbauen | [ ] Ja [ ] Nein |
| **Babler-Credibility** | Wenn Traiskirchen-Erfahrung hilft | [ ] Ja [ ] Nein |
| **Nicht verteidigen** | Wenn wir angegriffen werden | [ ] Ja [ ] Nein |

**Gewähltes Prinzip:** _________________________________

**Anwendung auf dieses Thema:**
```
[Wie wird das Prinzip hier konkret angewendet?]
```

### 0.2 Transformations-Prinzip wählen (Ebene 2)

| TP | Prinzip | Für dieses Thema? |
|:---|:--------|:------------------|
| **TP-1** | Framing als «Ordnung» statt «Verbot» | [ ] Zentral [ ] Relevant [ ] Nicht |
| **TP-2** | Staatstragende Tonalität | [ ] Zentral [ ] Relevant [ ] Nicht |
| **TP-3** | Fokus auf Ergebnisse und Verantwortung | [ ] Zentral [ ] Relevant [ ] Nicht |
| **TP-4** | Selbstbewusste Agenda | [ ] Zentral [ ] Relevant [ ] Nicht |

**Zentrales Prinzip:** _________________________________

### 0.3 Transformation definieren (Alt → Neu)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TRANSFORMATION für [THEMA]                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ALT (Wie wurde bisher kommuniziert?):                                  │
│  → «____________________________________________________________»       │
│                                                                         │
│  NEU (Wie kommunizieren wir jetzt?):                                    │
│  → «____________________________________________________________»       │
│                                                                         │
│  BEGRÜNDUNG (Warum folgt das aus der Strategie?):                       │
│  → ________________________________________________________________     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 0.4 Modell-basierte Validierung (PFLICHT)

> **SSOT:** `spo_two_path_model.yaml` (MOD-SPO-TWOPATH-001)

**Das Modell liefert quantitative Kriterien für die Bewertung jeder strategischen Fragestellung:**

#### A. Pfad-Check: Stärkt die Kommunikation den RICHTIGEN Pfad?

| Pfad | Definition | Für wen? | Diese Fragestellung? |
|:-----|:-----------|:---------|:---------------------|
| **γ^{Ausschluss}** | E(Grenzen) × X(Herkunft) | FPÖ | [ ] Stärkt ❌ [ ] Neutral [ ] Schwächt ✓ |
| **γ^{Funktion}** | E(Systeme) × X(Beitrag) | SPÖ | [ ] Stärkt ✓ [ ] Neutral [ ] Schwächt ❌ |

**Zielwerte aus Modell:**
- γ^{Funktion} aktuell: 0.15 → Ziel: 0.35
- Jede Kommunikation muss γ^{Funktion} stärken, NICHT γ^{Ausschluss}

#### B. Credibility-Check: Bleibt die Glaubwürdigkeit im richtigen Bereich?

| Dimension | Aktuell | Ziel | Gefährdung durch diese Fragestellung? |
|:----------|:--------|:-----|:--------------------------------------|
| Credibility auf Funktion | 0.45 | 0.65 | [ ] Nein ✓ [ ] Möglich ⚠️ [ ] Ja ❌ |
| Credibility auf Ausschluss | 0.20 | 0.20 | [ ] Stabil ✓ [ ] Steigt ⚠️ |

#### C. Erfolgsbedingungen-Check: Gefährdet die Fragestellung eine Bedingung?

| Bedingung | Beschreibung | Gefährdet? |
|:----------|:-------------|:-----------|
| **EXECUTION** | SPÖ muss ZEIGEN, dass Systeme funktionieren | [ ] Nein ✓ [ ] Ja ❌ |
| **KONSISTENZ** | Keine Rückfälle in alte Frames, keine internen Widersprüche | [ ] Nein ✓ [ ] Ja ❌ |
| **ZEIT** | 18-24 Monate für Frame-Aufbau | [ ] Nein ✓ [ ] Ja ❌ |
| **KEINE KRISE** | Keine Reaktivierung des FPÖ-Frames | [ ] Nein ✓ [ ] Ja ❌ |

#### D. Speech-Elements-Check: Werden die RICHTIGEN Elemente verwendet?

**Was funktioniert (Score 8-10):**
```
☐ "Ordnung heisst, dass Dinge funktionieren" (Score 9)
☐ "Wer beiträgt, gehört dazu" (Score 10)
☐ "Das ist nicht in Ordnung" (Score 9)
☐ Konkrete Beispiele (Linz, Wien) (Score 8)
☐ "Schritt für Schritt" (Score 8)
☐ Traiskirchen-Referenz (Score 9)
☐ Wohnen-Integration (Score 8)
```

**Was vermieden werden MUSS:**
```
☐ Keine FPÖ-Abgrenzung über 1-2 Sätze hinaus (aktiviert FPÖ-Frame!)
☐ Keine Ankündigungen ohne Beweise
☐ Keine nicht-messbaren Commitments
☐ Doskozil adressiert oder neutral gehalten
```

### 0.5 Konsistenz-Check

```
☐ Grundlagen-Prinzip gewählt und begründet?
☐ Transformations-Prinzip gewählt?
☐ Transformation (Alt → Neu) formuliert?
☐ Keine Konkurrenz auf FPÖ-Terrain? (Komplementarität!)
☐ Keine Verteidigung? (Ordnung statt Reaktion!)
☐ Keine Abschiebungszahlen als Hauptargument?
☐ ★ MODELL-VALIDIERUNG: Alle Checks in 0.4 bestanden?
```

### 0.6 Zusammenfassung: Strategische Ableitung

```
┌─────────────────────────────────────────────────────────────────────────┐
│  STRATEGISCHE ABLEITUNG für [THEMA]                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EBENE 1 (Grundlagen):                                                  │
│  → Prinzip: [z.B. Two-Path-Modell]                                     │
│  → Anwendung: [z.B. EMRK = Ordnung, nicht Hindernis]                   │
│                                                                         │
│  EBENE 2 (Strategie):                                                   │
│  → Prinzip: [z.B. TP-2 Staatstragende Tonalität]                       │
│  → Anwendung: [z.B. Regierungssprache, nicht Opposition]               │
│                                                                         │
│  EBENE 3 (Transformation):                                              │
│  → Alt: «[z.B. Wir stehen zur EMRK]»                                   │
│  → Neu: «[z.B. Die EMRK IST Ordnung]»                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Schritt 1: Stakeholder-Landschaft

### Die erste Frage bei JEDEM Thema:

> **Wie stehen die anderen zu dieser Frage?**

### 1.1 Politische Parteien

| Partei | Position zu [THEMA] | Konsens mit SPÖ? |
|:-------|:--------------------|:-----------------|
| **ÖVP** | | [ ] Ja [ ] Teilweise [ ] Nein |
| **FPÖ** | | [ ] Ja [ ] Teilweise [ ] Nein |
| **Grüne** | | [ ] Ja [ ] Teilweise [ ] Nein |
| **NEOS** | | [ ] Ja [ ] Teilweise [ ] Nein |

### 1.2 Sozialpartner & Verbände

| Organisation | Position zu [THEMA] | Konsens mit SPÖ? |
|:-------------|:--------------------|:-----------------|
| **ÖGB** (Gewerkschaft) | | [ ] Ja [ ] Teilweise [ ] Nein |
| **AK** (Arbeiterkammer) | | [ ] Ja [ ] Teilweise [ ] Nein |
| **WKO** (Wirtschaftskammer) | | [ ] Ja [ ] Teilweise [ ] Nein |
| **IV** (Industriellenvereinigung) | | [ ] Ja [ ] Teilweise [ ] Nein |

### 1.3 SPÖ-regierte Länder

| Land | Position/Erfahrung zu [THEMA] |
|:-----|:------------------------------|
| **Wien** | |
| **Burgenland** | |
| **Kärnten** | |

### 1.4 Bürger:innen Österreichs

| Frage | Antwort |
|:------|:--------|
| Was wollen ALLE? | |
| Was will NIEMAND? | |
| Gibt es Umfragen? | |

### 1.5 Zusammenfassung: Konsens-Landschaft

```
┌─────────────────────────────────────────────────────────────────────────┐
│  KONSENS-ANALYSE zu [THEMA]                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  BREITER KONSENS (Cross-Party):                                        │
│  → [Was wollen alle/fast alle?]                                        │
│                                                                         │
│  SPÖ-POSITION:                                                         │
│  → [Was ist unsere spezifische Position?]                              │
│                                                                         │
│  WER SPALTET:                                                          │
│  → [Wer weicht vom Konsens ab? Wer polarisiert?]                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Schritt 2: SPÖ/BABLER-POSITION

### Die zweite Frage bei JEDEM Thema:

> **Wie ist die derzeitige Position der SPÖ? Wie hat sich Babler geäussert?**

### 2.1 Aktuelle SPÖ-Position

| Frage | Antwort |
|:------|:--------|
| Offizielle Partei-Position? | |
| Programmatische Grundlage? | |
| Beschlüsse (Parteitag, Vorstand)? | |

### 2.2 Bablers bisherige Äusserungen

| Kontext | Aussage | Datum |
|:--------|:--------|:------|
| Interview | | |
| Rede/Parteitag | | |
| Social Media | | |
| Pressekonferenz | | |

### 2.3 Grundsätze & Programme

| Dokument | Relevante Passage |
|:---------|:------------------|
| Parteiprogramm | |
| Wahlprogramm | |
| Regierungsübereinkommen | |
| Frühere Beschlüsse | |

### 2.4 Zusammenfassung: SPÖ/Babler-Linie

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SPÖ/BABLER-POSITION zu [THEMA]                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  AKTUELLE POSITION:                                                    │
│  → [Zusammenfassung der offiziellen SPÖ-Linie]                         │
│                                                                         │
│  BABLER-ZITATE:                                                         │
│  → «[Wichtigstes Zitat]»                                               │
│  → «[Zweites wichtiges Zitat]»                                         │
│                                                                         │
│  KONSISTENZ-CHECK:                                                      │
│  → Passt zur Stakeholder-Landschaft (Schritt 1)?   [ ] Ja [ ] Anpassen │
│  → Passt zu "Ordnen statt Spalten"?                [ ] Ja [ ] Anpassen │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Schritt 3: "Ordnen statt Spalten" anwenden

### Die zentrale Frage bei JEDEM Thema:

> **Wie ORDNEN wir dieses Thema – statt zu spalten?**

### 3.1 Fundament prüfen

| Frage | Antwort |
|:------|:--------|
| Bablers persönliche Erfahrung? | |
| Traiskirchen-Beweis möglich? | |
| Welche Sprach-DNA passt? | |

### 3.2 Die 3 Ordnungs-Levels ausfüllen

```
LEVEL 1: THEMA ORDNEN (Was sind die Fakten?)
─────────────────────────────────────────────
Zahlen:      [Absolut, nicht Prozent – Ordnung durch Klarheit]
Massnahmen:  [Was tun wir konkret? – Ordnung durch Handeln]
Ergebnis:    [Was funktioniert? – Ordnung durch Ergebnisse]

KERNAUSSAGE: «____________________________________»


LEVEL 2: DEBATTE ORDNEN (Wie rahmen wir die Diskussion?)
────────────────────────────────────────────────────────
Frame:       [VON: ___ → ZU: ___ – Ordnung statt Ablenkung]
Cross-Party: [Was wollen ALLE? – Ordnung durch Konsens]
Gegner:      [Wer SPALTET? – Abgrenzung von Spaltung]

KERNAUSSAGE: «____________________________________»


LEVEL 3: LAND ORDNEN (Was ist der österreichische Weg?)
───────────────────────────────────────────────────────
Geschichte:  [Welche Lehre? – Ordnung durch Erfahrung]
Identität:   [Der österreichische Weg – Ordnung durch Identität]
Geopolitik:  [Wer sind die Spalter? – Ordnung vs. Chaos]

KERNAUSSAGE: «____________________________________»
```

### 3.3 Closer formulieren

```
«[WAS WIR ORDNEN]. [WAS FUNKTIONIERT]. Das ist der österreichische Weg.»
```

---

## Schritt 4: Template ausfüllen

### Die strategische Frage entlang des Templates beantworten

> **Das vollständige Template ausfüllen → Ergebnis: TAKTIK_babler_[thema].md**

Das Template (`TEMPLATE_taktische_ableitung.md`) strukturiert alle Erkenntnisse aus Schritt 1-3:

### 4.1 Template-Abschnitte

| Abschnitt | Quelle | Was eintragen? |
|:----------|:-------|:---------------|
| **0. Fundament-Check** | BABLER_erkenntnisse.md | Passt zu Bablers Erfahrung? |
| **1. Level 1** | Schritt 3 | Zahlen, Massnahmen, Ergebnisse |
| **2. Level 2** | Schritt 1 + 3 | Frame, Cross-Party, Gegner |
| **3. Level 3** | Schritt 3 | Geschichte, Identität, Geopolitik |
| **4. 9-Akt-Integration** | FRAMEWORK_ordnung_der_dinge.md | Akte zuordnen |
| **5. Szenarien** | Schritt 1 | Mögliche Angriffe + Antworten |
| **6. Quick-Reference** | Aus allen Levels | TV, Radio, Social, Presse |
| **7. Do's & Don'ts** | Aus Analyse | Spezifisch für dieses Thema |

### 4.2 Dateiname

```
TAKTIK_babler_[thema]_[datum].md

Beispiel: TAKTIK_babler_emrk_2026-02-02.md
```

### 4.3 Konsistenz-Check vor Abschluss

```
☐ Alle 3 Levels ausgefüllt (aus Schritt 3)?
☐ Stakeholder-Erkenntnisse integriert (aus Schritt 1)?
☐ Babler-Position berücksichtigt (aus Schritt 2)?
☐ Sprach-DNA aus BABLER_erkenntnisse.md verwendet?
☐ Closer formuliert (Statement, keine Frage)?
```

---

## Schritt 5: Ergebnissicherung

### Ablage, Versionierung und Datenbank

> **Jede Anfrage wird dokumentiert – nichts geht verloren**

### 5.1 Anfragen-Datenbank (PFLICHT)

**Jeder Workflow/jede Anfrage wird in der SPÖ-Datenbank erfasst:**

```
data/customers/spo/database/
└── ANFRAGEN_REGISTER.yaml
```

**Eintrag pro Anfrage:**

```yaml
- id: ANF-2026-02-02-001
  datum: 2026-02-02
  thema: "EMRK / Migration"
  typ: "Strategische Positionierung"
  status: "abgeschlossen"
  outputs:
    - taktik: "TAKTIK_babler_emrk_2026-02-02.md"
    - wording: "WORDING_babler_emrk_position.md"
    - briefing: "BRIEFING_babler_emrk_operativ.md"
  stakeholder_analyse: true
  babler_position: true
  drei_levels: true
  erstellt_von: "[Name]"
```

### 5.2 Ablagestruktur

```
data/customers/spo/
├── database/
│   └── ANFRAGEN_REGISTER.yaml              ← Alle Anfragen
├── taktik/
│   └── TAKTIK_babler_[thema]_[datum].md    ← Schritt 4 Ergebnis
├── wordings/
│   ├── WORDING_babler_[thema].md           ← Falls Output gewählt
│   └── BRIEFING_babler_[thema]_operativ.md ← Falls Output gewählt
└── outputs/
    ├── 1PAGER_babler_[thema].md            ← Falls Output gewählt
    └── PPT_babler_[thema].md               ← Falls Output gewählt
```

### 5.3 Konsistenz-Check mit SSOTs

| SSOT | Prüfung | Status |
|:-----|:--------|:-------|
| SSOT-1 (Babler) | Sprach-DNA verwendet? | [ ] ✓ |
| SSOT-2 (3 Levels) | Alle 3 Levels abgedeckt? | [ ] ✓ |
| SSOT-4 (Strategie) | Passt zur Gesamtstrategie? | [ ] ✓ |

### 5.3 Versionierung

| Feld | Eintrag |
|:-----|:--------|
| Version | 1.0 |
| Datum | [YYYY-MM-DD] |
| Erstellt von | [Name] |
| Geprüft | [ ] Noch nicht |

---

## Schritt 6: Output-Format wählen

### Welches Format wird benötigt?

> **Aus der TAKTIK das passende Output-Format ableiten**

| Format | Wann? | Umfang |
|:-------|:------|:-------|
| **1-PAGER** | Schneller Überblick, interner Gebrauch | 1 Seite |
| **PPT** | Präsentation, Gremiensitzung | 5-10 Slides |
| **WORDING** | Vollständige Argumentation | 5-10 Seiten |
| **BRIEFING** | Operative Anleitung für Kommunikationsteam | 10-20 Seiten |
| **REPORT** | Executive Summary des Workflow-Durchlaufs | 2-3 Seiten |

Die Inhalte leiten sich aus der TAKTIK (Schritt 4) ab:

### → 1-PAGER

```
┌─────────────────────────────────────────────────────────────────────────┐
│  1-PAGER: [THEMA]                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WIE WIR [THEMA] ORDNEN                                                │
│  ──────────────────────                                                 │
│  [Level-1-Kernaussage]                                                  │
│                                                                         │
│  WARUM DAS FUNKTIONIERT                                                │
│  ──────────────────────                                                 │
│  • [Zahl + Ergebnis]                                                    │
│  • [Cross-Party-Konsens]                                                │
│  • [Österreichischer Weg]                                               │
│                                                                         │
│  WER SPALTET                                                            │
│  ──────────                                                             │
│  [Level-2: Abgrenzung von Spaltern]                                     │
│                                                                         │
│  CLOSER                                                                 │
│  ──────                                                                 │
│  [Ordnung. Ergebnis. Österreichischer Weg.]                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### → PPT (5-10 Slides)

| Slide | Inhalt | Quelle |
|:------|:-------|:-------|
| 1 | Titel: "Ordnen statt Spalten: [THEMA]" | - |
| 2 | Wie wir das Thema ordnen | Level 1: Kernaussage |
| 3 | Die Zahlen | Level 1: Zahlen |
| 4 | Was wir konkret tun | Level 1: Massnahmen |
| 5 | Das funktioniert | Level 1: Ergebnis |
| 6 | Wie wir die Debatte ordnen | Level 2: Frame |
| 7 | Was ALLE wollen | Level 2: Cross-Party |
| 8 | Wer spaltet | Level 2: Gegner |
| 9 | Der österreichische Weg | Level 3: Identität |
| 10 | Closer | "Ordnung. Ergebnis. Das funktioniert." |

### → WORDING (Vollständig)

```
WORDING_babler_[thema].md

├── Wie wir [THEMA] ordnen (Level 1)
├── Wie wir die Debatte ordnen (Level 2)
├── Der österreichische Weg (Level 3)
├── Szenarien: Angriffe der Spalter → Unsere Ordnung
└── Closer
```

### → BRIEFING (Operativ)

```
BRIEFING_babler_[thema]_operativ.md

├── Executive Summary: Ordnen statt Spalten bei [THEMA]
├── Die 3 Ordnungs-Levels (Thema → Debatte → Land)
├── Operative Umsetzung (9 Akte)
├── Quick-Reference Cards (TV, Radio, Social, Presse)
├── Interview-Simulation
└── Do's & Don'ts
```

### → REPORT (Executive Summary)

```
REPORT_[thema]_strategie_[datum].md

├── Executive Summary (1 Absatz)
├── Strategische Ausgangslage
│   ├── Die Frage
│   ├── Das Dilemma
│   └── Die Lösung
├── Workflow-Ergebnisse
│   ├── Schritt 1: Stakeholder-Landschaft (Tabelle)
│   ├── Schritt 2: SPÖ/Babler-Position
│   └── Schritt 3: Die 3 Levels (Grafik)
├── Closer
├── Generierte Dokumente (Übersicht)
├── Quick Reference (TV, Radio, Social)
├── Nächste Schritte
└── Quellen
```

**Zweck:** Der REPORT dokumentiert den gesamten Workflow-Durchlauf und dient als **Nachweis und Nachschlagewerk** für die strategische Frage.

**Ablage:** `reports/REPORT_[thema]_strategie_[datum].md`

---

## Quick-Reference: Ableitung → Output

| Von Taktik | → 1-Pager | → PPT | → Wording | → Briefing | → Report |
|:-----------|:----------|:------|:----------|:-----------|:---------|
| Level 1 Kernaussage | "Wie wir ordnen" | Slide 2 | Teil 1 | Teil 1 | Teil 2 |
| Level 1 Zahlen | Punkt 1 | Slide 3 | Argumentation | Teil 2 | Teil 2 |
| Level 1 Massnahmen | - | Slide 4 | Argumentation | Teil 2 | Teil 2 |
| Level 1 Ergebnis | Punkt 2 | Slide 5 | Argumentation | Teil 2 | Teil 2 |
| Level 2 Frame | - | Slide 6 | Framing | Teil 2 | Teil 2 |
| Level 2 Cross-Party | Punkt 3 | Slide 7 | Argumentation | Teil 2 | Teil 2 |
| Level 2 Gegner | "Wer spaltet" | Slide 8 | Szenarien | Teil 5 | Teil 2 |
| Level 3 Identität | - | Slide 9 | Werte | Teil 2 | Teil 2 |
| Closer | Closer | Slide 10 | Closer | Teil 3 | Teil 3 |
| Workflow-Doku | - | - | - | - | Anhang |

---

## Beispiel: EMRK-Thema

### Schritt 1: Stakeholder-Landschaft (EMRK)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  STAKEHOLDER-ANALYSE: EMRK / Migration / Abschiebungen                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  POLITISCHE PARTEIEN:                                                   │
│  ├── ÖVP:   Will EMRK-Reform → hat Brief unterschrieben                │
│  ├── FPÖ:   Will EMRK verlassen → extreme Position                     │
│  ├── Grüne: Gegen EMRK-Änderung → Konsens mit SPÖ                      │
│  └── NEOS:  Pragmatisch → offen für Diskussion                         │
│                                                                         │
│  SOZIALPARTNER:                                                         │
│  ├── ÖGB:   Gegen Aufweichung von Grundrechten                         │
│  ├── AK:    Schützt Menschenrechte → Konsens mit SPÖ                   │
│  ├── WKO:   Wenig Position → nicht ihr Kernthema                       │
│  └── IV:    Wenig Position → nicht ihr Kernthema                       │
│                                                                         │
│  SPÖ-LÄNDER:                                                            │
│  ├── Wien:      Erfahrung mit Integration, pragmatischer Ansatz        │
│  ├── Burgenland: Grenzland, Sicherheit wichtig                         │
│  └── Kärnten:   Flüchtlingsroute, praktische Erfahrung                 │
│                                                                         │
│  BÜRGER:INNEN:                                                          │
│  ├── Was wollen ALLE?     → Sicherheit, Ordnung                        │
│  ├── Was will NIEMAND?    → Folter, Menschenrechtsverletzungen         │
│  └── Umfragen:            → Mehrheit für harte Linie bei Straftätern   │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  KONSENS-ANALYSE:                                                       │
│                                                                         │
│  BREITER KONSENS:                                                       │
│  → Straffällige abschieben – will jeder (von links bis rechts)         │
│  → Keine Folter – will niemand (unabhängig von der Partei)             │
│                                                                         │
│  SPÖ-POSITION:                                                          │
│  → System funktioniert – nutzen statt reformieren                      │
│                                                                         │
│  WER SPALTET:                                                           │
│  → FPÖ (EMRK verlassen) – extreme Position                             │
│  → Kickl – Freunde sind Putin, Trump, Orbán                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 2: SPÖ/BABLER-POSITION (EMRK)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SPÖ/BABLER-POSITION: EMRK / Migration / Abschiebungen                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  AKTUELLE SPÖ-POSITION:                                                │
│  → Bestehendes System nutzen, nicht aufweichen                         │
│  → EMRK nicht verlassen – aber konsequent anwenden                     │
│  → Fokus auf Rücknahmeabkommen und praktische Lösungen                 │
│                                                                         │
│  BABLERS ÄUSSERUNGEN:                                                   │
│  → «7.000 Abschiebungen. Höchststand. Das funktioniert.»               │
│  → «Null Toleranz bei Straftätern.»                                    │
│  → «Wer Grundrechts-Debatten führt statt zu handeln, lenkt ab.»        │
│  → Traiskirchen-Erfahrung: Praktische Lösungen statt Symbolpolitik     │
│                                                                         │
│  GRUNDSÄTZE:                                                            │
│  → Regierungsübereinkommen: Konsequente Migrationspolitik              │
│  → SPÖ-Tradition: Menschenrechte schützen UND Sicherheit gewährleisten │
│                                                                         │
│  KONSISTENZ-CHECK:                                                      │
│  → Passt zur Stakeholder-Landschaft?  [✓] Ja – Konsens bei Abschiebung │
│  → Passt zu "Ordnen statt Spalten"?   [✓] Ja – System nutzen = Ordnung │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 3: "Ordnen statt Spalten" angewandt (EMRK)

```
THEMA: EMRK / Migration / Abschiebungen

FRAGE: Wie ORDNEN wir dieses Thema – statt zu spalten?


LEVEL 1: THEMA ORDNEN
─────────────────────
Zahlen:      7.000 Abschiebungen. 50% Straftäter. Syrien-Abschiebungen.
Massnahmen:  Null Toleranz. Rücknahmeabkommen. Haft in Herkunftsländern.
Ergebnis:    Das funktioniert.

KERNAUSSAGE: «7.000 Abschiebungen. Höchststand. Das funktioniert.»


LEVEL 2: DEBATTE ORDNEN (aus Stakeholder-Analyse)
─────────────────────────────────────────────────
Frame:       VON: "EMRK reformieren?" → ZU: "System nutzen, das funktioniert"
Cross-Party: Extrem wenige wollen Folter – unabhängig von der Partei
             (→ AK, Grüne, ÖGB = Konsens)
Gegner:      Wer Grundrechts-Debatten führt statt zu handeln, SPALTET
             (→ FPÖ/Kickl = Spalter)

KERNAUSSAGE: «Das ist keine Frage von links oder rechts. Das ist Anstand.»


LEVEL 3: LAND ORDNEN
────────────────────
Geschichte:  Nach dem Krieg: Schutz VOR dem Staat
Identität:   Der österreichische Weg: pragmatisch UND menschlich
Geopolitik:  Putin, Trump, Orbán – Spalter. Freunde von Kickl.

KERNAUSSAGE: «Das ist die Lehre aus unserer Geschichte.»


CLOSER: «Sicherheit für alle. Regeln für alle. Das ist der österreichische Weg.»
```

### → 1-Pager (abgeleitet)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  1-PAGER: Ordnen statt Spalten – EMRK-Position                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WIE WIR DIE MIGRATIONSPOLITIK ORDNEN                                  │
│  7.000 Abschiebungen. Höchststand. Das funktioniert.                   │
│                                                                         │
│  WARUM DAS FUNKTIONIERT                                                │
│  • 50% aller Abgeschobenen sind Straftäter – Null Toleranz wirkt       │
│  • Unabhängig von der Partei: Extrem wenige wollen Folter              │
│  • Der österreichische Weg: pragmatisch UND menschlich                 │
│                                                                         │
│  WER SPALTET                                                            │
│  Wer Grundrechts-Debatten führt, statt Abkommen zu verhandeln,         │
│  spaltet. Wir ordnen. Wir handeln.                                     │
│                                                                         │
│  CLOSER                                                                 │
│  Sicherheit für alle. Regeln für alle. Das ist der österreichische Weg.│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Dateien nach Abschluss

```
data/customers/spo/
├── taktik/
│   └── TAKTIK_babler_[thema].md         ← Ordnungs-Strategie
├── outputs/
│   ├── 1PAGER_babler_[thema].md         ← Falls 1-Pager
│   └── PPT_babler_[thema].md            ← Falls PPT-Vorlage
└── wordings/
    ├── WORDING_babler_[thema].md        ← Falls Wording
    └── BRIEFING_babler_[thema].md       ← Falls Briefing
```

---

## Versionierung

| Version | Datum | Änderung |
|:--------|:------|:---------|
| 1.0 | 2026-02-02 | Erstversion |
| 1.1 | 2026-02-02 | Vereinfacht, Output-fokussiert |
| 1.2 | 2026-02-02 | "Ordnen statt Spalten" als Ausgangspunkt |
| 1.3 | 2026-02-02 | Stakeholder-Landschaft als Schritt 1 |
| 1.4 | 2026-02-02 | SPÖ/Babler-Position als Schritt 2 |
| 1.5 | 2026-02-02 | 6-Schritte-Struktur: +Template +Ergebnissicherung +Output-Wahl |
| 1.6 | 2026-02-02 | ANFRAGEN_REGISTER.yaml: Jede Anfrage in Datenbank erfassen |
| 1.7 | 2026-02-02 | REPORT als 5. Output-Format: Executive Summary des Workflow-Durchlaufs |
| **2.0** | **2026-02-03** | **★ SCHRITT 0: STRATEGISCHE ABLEITUNG (Komplementarität)** |
|     |            | + 3-Ebenen-Hierarchie (Grundlagen → Strategie → Fragestellung) |
|     |            | + Verbindung zu GRUNDLAGEN_strategische_entscheidung.md |
|     |            | + 5 Kernprinzipien + 4 Transformations-Prinzipien |
|     |            | + Transformation (Alt → Neu) als PFLICHT |
|     |            | + 3 Standard-Lieferobjekte (Report, Präsentation, Infografik) |
| **2.1** | **2026-02-03** | **★ MODELL-BASIERTE VALIDIERUNG (0.4)** |
|     |            | + Integration von spo_two_path_model.yaml (MOD-SPO-TWOPATH-001) |
|     |            | + Pfad-Check (γ^{Funktion} vs γ^{Ausschluss}) |
|     |            | + Credibility-Check (Glaubwürdigkeits-Zielwerte) |
|     |            | + Erfolgsbedingungen-Check (EXECUTION, KONSISTENZ, ZEIT, KRISE) |
|     |            | + Speech-Elements-Check (Was funktioniert, was vermeiden) |

---

*FehrAdvice & Partners AG*
