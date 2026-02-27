# Lead-Eingabe Workflow

> Standardisierter Prozess für die Erfassung neuer Leads mit automatischem Projekt-Phasen-Vorschlag

---

## Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEAD-EINGABE WORKFLOW (5 Schritte)                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: Basis-Identifikation                                        │
│      ↓                                                                  │
│  SCHRITT 2: Klassifikation                                              │
│      ↓                                                                  │
│  SCHRITT 3: Pipeline-Status                                             │
│      ↓                                                                  │
│  SCHRITT 4: Projekt-Phase (AUTO-SUGGEST)  ← Algorithmus schlägt vor     │
│      ↓                                                                  │
│  SCHRITT 5: Zusatzinformationen (optional)                              │
│      ↓                                                                  │
│  ✓ LEAD ERSTELLT                                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Schritt 1: Basis-Identifikation (PFLICHT)

**Fragen an den Benutzer:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 1: BASIS-IDENTIFIKATION                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1.1 Unternehmensname (vollständig)?                                    │
│      → z.B. "Schweizerische Post AG"                                    │
│                                                                         │
│  1.2 Kurzname (für Anzeige)?                                            │
│      → z.B. "Post"                                                      │
│                                                                         │
│  1.3 Website (optional)?                                                │
│      → z.B. "https://www.post.ch"                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Ausgabe:**
```yaml
company:
  name: "Schweizerische Post AG"
  short_name: "Post"
  website: "https://www.post.ch"
```

---

## Schritt 2: Klassifikation (PFLICHT)

**Fragen an den Benutzer:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 2: KLASSIFIKATION                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  2.1 Branche?                                                           │
│      [ ] finance          [ ] packaging        [ ] construction         │
│      [ ] fmcg             [ ] pharma_health    [ ] energy               │
│      [ ] technology       [ ] public_sector    [ ] manufacturing        │
│      [ ] retail           [ ] professional_services                     │
│                                                                         │
│  2.2 Land/Hauptsitz?                                                    │
│      [ ] CH (Schweiz)     [ ] AT (Österreich)  [ ] DE (Deutschland)     │
│      [ ] Andere: _______                                                │
│                                                                         │
│  2.3 Segment (Unternehmensgrösse)?                                      │
│      [ ] enterprise (>5000 MA)                                          │
│      [ ] mid_market (500-5000 MA)                                       │
│      [ ] smb (<500 MA)                                                  │
│      [ ] government                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Ausgabe:**
```yaml
industry: professional_services
headquarters:
  country: CH
  city: "Bern"
segment: enterprise
```

---

## Schritt 3: Pipeline-Status (PFLICHT)

**Fragen an den Benutzer:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 3: PIPELINE-STATUS                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  3.1 Aktueller Status?                                                  │
│                                                                         │
│      AKQUISE:                                                           │
│      [ ] SUSPECT      - Identifiziert, noch kein Kontakt                │
│      [ ] PROSPECT     - Erster Kontakt hergestellt                      │
│      [ ] QUALIFIED    - Bedarf und Budget qualifiziert                  │
│      [ ] PROPOSAL     - Angebot erstellt/präsentiert                    │
│      [ ] NEGOTIATION  - Vertragsverhandlung                             │
│                                                                         │
│  3.2 Owner (wer ist verantwortlich)?                                    │
│      [ ] EB           [ ] MR           [ ] Andere: _______              │
│                                                                         │
│  3.3 Wie kam der Kontakt zustande?                                      │
│      [ ] REFERRAL     - Empfehlung (Client, Partner, Fehr-Network)      │
│      [ ] INBOUND      - Website, Content, Event                         │
│      [ ] OUTBOUND     - Cold Outreach, LinkedIn, Conference             │
│      [ ] RESEARCH     - Akademische Kollaboration, Grant                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Ausgabe:**
```yaml
stage: PROSPECT
relationship:
  owner: "EB"
source:
  channel: OUTBOUND
  subchannel: conference
  first_touch_date: "2026-01-27"
```

---

## Schritt 4: Projekt-Phase (AUTO-SUGGEST)

**System schlägt automatisch vor:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 4: PROJEKT-PHASE                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  🤖 AUTO-VORSCHLAG                                               │   │
│  │                                                                  │   │
│  │  Basierend auf: Stage = PROSPECT                                 │   │
│  │                                                                  │   │
│  │  → Vorgeschlagene Phase: 0 (Erstgespräch / Kennenlernen)        │   │
│  │                                                                  │   │
│  │  Begründung: "Erster Kontakt / Kennenlernen"                    │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Bestätigen oder ändern?                                                │
│                                                                         │
│  [ ] ✓ Phase 0 bestätigen (Enter)                                       │
│  [ ] Phase ändern auf:                                                  │
│      ( ) 0 - Erstgespräch / Kennenlernen                               │
│      ( ) 1 - Themen- & Rahmenprüfung                                   │
│      ( ) 2 - Erwartungsklärung & Vorgehen                              │
│      ( ) 3 - Angebotsphase                                             │
│      ( ) 4 - Abschluss & Commitment                                    │
│      ( ) 5 - Umsetzung & laufendes Projekt                             │
│                                                                         │
│  Begründung für Phase (optional):                                       │
│  → z.B. "Erstkontakt an Swiss Innovation Forum"                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Auto-Suggest Logik:**

| Stage | Default Phase | Begründung |
|-------|---------------|------------|
| SUSPECT | 0 | Noch kein Kontakt hergestellt |
| PROSPECT | 0 | Erster Kontakt / Kennenlernen |
| QUALIFIED | 1 | Thema & Rahmen geprüft (SQL) |
| QUALIFIED + Scope-Diskussion | 2 | Erwartungsklärung läuft |
| PROPOSAL | 3 | Angebot in Arbeit oder versendet |
| NEGOTIATION | 4 | Vertragsverhandlung / Abschluss |
| WON | 4 | Deal gewonnen, Commitment erfolgt |
| WON + Projekt aktiv | 5 | Projekt bereits gestartet |

**Ausgabe:**
```yaml
relationship:
  project_phase: 0
  project_phase_note: "Erstkontakt an Swiss Innovation Forum"
  project_phase_auto_suggested: true   # Markiert ob Auto-Suggest verwendet
  project_phase_confirmed: true        # Markiert ob User bestätigt hat
```

---

## Schritt 5: Zusatzinformationen (OPTIONAL)

**Fragen an den Benutzer:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 5: ZUSATZINFORMATIONEN (optional)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  5.1 Nächste Aktion?                                                    │
│      Typ:    [ ] meeting  [ ] call  [ ] email  [ ] proposal  [ ] other  │
│      Datum:  ___________                                                │
│      Beschreibung: _______________________                              │
│                                                                         │
│  5.2 Opportunity (falls bekannt)?                                       │
│      Name:        _______________________                               │
│      Wert (EUR):  _______________________                               │
│      Wahrscheinlichkeit (%): ___________                                │
│                                                                         │
│  5.3 Kontaktperson?                                                     │
│      Name:  _______________________                                     │
│      Rolle: _______________________                                     │
│                                                                         │
│  5.4 Notizen?                                                           │
│      _____________________________________________                      │
│                                                                         │
│  5.5 Tags?                                                              │
│      [ ] switzerland  [ ] digital_transformation  [ ] sustainability    │
│      [ ] family_business  [ ] publicly_listed  [ ] Andere: _______     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Zusammenfassung & Bestätigung

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ✓ LEAD-ZUSAMMENFASSUNG                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ID:              LEAD-013 (automatisch generiert)                      │
│                                                                         │
│  UNTERNEHMEN                                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Name:            Schweizerische Post AG                                │
│  Kurzname:        Post                                                  │
│  Branche:         professional_services                                 │
│  Land:            CH (Bern)                                             │
│  Segment:         enterprise                                            │
│                                                                         │
│  STATUS                                                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  Pipeline-Stage:  PROSPECT                                              │
│  Projekt-Phase:   0 (Erstgespräch / Kennenlernen) ← AUTO-SUGGESTED     │
│  Owner:           EB                                                    │
│  Source:          OUTBOUND / conference                                 │
│                                                                         │
│  NÄCHSTE AKTION                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  Typ:             meeting                                               │
│  Datum:           2026-02-15                                            │
│  Beschreibung:    Discovery Call vereinbaren                            │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  [ ] ✓ Lead erstellen (Enter)                                           │
│  [ ] ✗ Abbrechen                                                        │
│  [ ] ← Zurück und bearbeiten                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Generiertes YAML

Nach Bestätigung wird folgender Eintrag in `lead-database.yaml` erstellt:

```yaml
- id: LEAD-013
  company:
    name: "Schweizerische Post AG"
    short_name: "Post"
    legal_form: "AG"
    website: "https://www.post.ch"
    linkedin: "https://www.linkedin.com/company/swiss-post"

  industry: professional_services
  industry_subcategory: logistics
  segment: enterprise
  employee_count: 48000
  revenue_eur: 7500000000
  headquarters:
    country: CH
    city: "Bern"
    region: "Bern"
  geographic_scope: national

  stage: PROSPECT
  stage_history:
    - stage: SUSPECT
      date: "2025-11-01"
      owner: "EB"
      notes: "Identifiziert via LinkedIn"
    - stage: PROSPECT
      date: "2026-01-15"
      owner: "EB"
      notes: "Erstkontakt an Event"

  fit_score: null    # Wird später berechnet
  engagement_score: 25

  relationship:
    owner: "EB"
    # --- Projekt-Phase (Auto-Suggest) ---
    project_phase: 0
    project_phase_note: "Erstkontakt an Swiss Innovation Forum"
    project_phase_auto_suggested: true
    project_phase_confirmed: true

  contacts:
    - name: "[Innovation Lead]"
      role: "Head of Innovation"
      relationship_strength: weak

  projects: []
  ebf_integration: null

  source:
    channel: OUTBOUND
    subchannel: conference
    campaign: "Swiss Innovation Forum 2026"
    first_touch_date: "2026-01-15"

  next_action:
    type: meeting
    date: "2026-02-15"
    description: "Discovery Call vereinbaren"
    owner: "EB"

  notes: "Grosse Transformation (Digitalisierung, E-Commerce). Potenzial für Behavioral Strategy."
  tags: [logistics, public_enterprise, digital_transformation, switzerland]

  created: "2026-01-27"
  updated: "2026-01-27"
```

---

## Kurzversion (Schnelleingabe)

Für erfahrene Benutzer - minimale Pflichtfelder:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHNELLEINGABE (Pflichtfelder)                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Unternehmen:  _________________ [Post]                                 │
│  Branche:      _________________ [professional_services]                │
│  Land:         _________________ [CH]                                   │
│  Stage:        _________________ [PROSPECT]                             │
│  Owner:        _________________ [EB]                                   │
│  Source:       _________________ [OUTBOUND]                             │
│                                                                         │
│  → Phase: 0 (auto) ✓                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Einzeiler-Format:**
```
Post | professional_services | CH | PROSPECT | EB | OUTBOUND
```

---

## Validierungsregeln

| Feld | Validierung | Fehlermeldung |
|------|-------------|---------------|
| `company.name` | Pflicht, nicht leer | "Unternehmensname ist erforderlich" |
| `company.short_name` | Pflicht, nicht leer | "Kurzname ist erforderlich" |
| `industry` | Muss in Taxonomie sein | "Ungültige Branche" |
| `stage` | Muss in pipeline_stages sein | "Ungültiger Pipeline-Status" |
| `headquarters.country` | CH, AT, DE oder ISO-Code | "Ungültiges Land" |
| `relationship.owner` | Muss definiert sein | "Owner ist erforderlich" |
| `project_phase` | 0-5 oder null | "Ungültige Projekt-Phase" |

---

## Integration mit Claude

**Slash-Command:** `/new-lead`

```bash
/new-lead                          # Interaktiver Modus (alle Schritte)
/new-lead --quick                  # Schnelleingabe (nur Pflichtfelder)
/new-lead --from-note "..."        # Aus Freitext extrahieren
```

**Beispiel mit Freitext:**
```
/new-lead --from-note "Hatte heute ein gutes Gespräch mit Hans Müller von
der Migros am Swiss Innovation Forum. Er ist Head of Sustainability und
interessiert sich für Behavioral Interventions im Bereich Nachhaltigkeit.
Sollten nächste Woche einen Call machen."
```

→ Claude extrahiert automatisch:
- Unternehmen: Migros
- Kontakt: Hans Müller, Head of Sustainability
- Stage: PROSPECT
- Source: OUTBOUND / conference
- Phase: 0 (auto-suggest)
- Next Action: Call nächste Woche

---

*Version 1.0 | 2026-01-27*
