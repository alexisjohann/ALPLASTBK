# /meeting - Meeting-Report & Follow-up Workflow

Standardisierter Workflow für Meeting-Dokumentation, Person-Profile und Follow-ups.

## 🔒 Single Source of Truth (SSOT)

**KRITISCH:** Die Templates sind fixiert und werden NUR am SSOT-Ort geändert!

| Komponente | SSOT-Pfad | Änderungen |
|------------|-----------|------------|
| **Meeting Registry** | `data/meeting-registry.yaml` | Einzige Quelle für Meeting-Metadaten |
| **Report Template (voll)** | `templates/meeting-report-template.md` | 11 Sektionen, alle Details |
| **Report Template (kurz)** | `templates/meeting-report-kurz-template.md` | 6 Sektionen, Quick-Mode |
| **Begleitschreiben** | `templates/begleitschreiben-template.md` | Follow-up Email |
| **Documents Section** | `templates/customer-documents-section.yaml` | Dokument-Tracking in Profilen |
| **Skill Definition** | `.claude/commands/meeting.md` | Dieser Workflow |

**Governance-Regeln:**
1. ✅ Templates IMMER aus SSOT-Pfad laden (nie hardcoded)
2. ✅ Bei Template-Änderung: NUR am SSOT-Ort ändern
3. ✅ Versionierung in Templates (siehe `*Version X.X*` am Ende)
4. ❌ NIEMALS Templates in Output-Dateien duplizieren
5. ❌ NIEMALS Template-Struktur ad-hoc ändern

**Referenz in CLAUDE.md:** Section "Single Sources of Truth (SSOT Registry)"

## Schnellstart

```bash
/meeting                           # Interaktiver Modus
/meeting new "Saskia Schenker"     # Neues Meeting dokumentieren
/meeting followup MTG-XXX          # Follow-up zu bestehendem Meeting
```

## Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `/meeting` | Interaktiver Modus |
| `/meeting new "Name"` | Neues Meeting dokumentieren |
| `/meeting list` | Alle Meetings anzeigen |
| `/meeting followup MTG-XXX` | Follow-up erstellen |
| `/meeting send MTG-XXX` | Versandpaket vorbereiten |

## Workflow: Neues Meeting dokumentieren

### Schritt 1: Basis-Informationen

```
/meeting new "Saskia Schenker"

┌─────────────────────────────────────────────────────────────────────────┐
│  📝 NEUES MEETING DOKUMENTIEREN                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Gesprächspartner:  Saskia Schenker                                    │
│                                                                         │
│  1. Datum & Zeit?                                                       │
│     [heute] / [gestern] / [Datum eingeben: TT.MM.YYYY]                 │
│                                                                         │
│  2. Uhrzeit (Start - Ende)?                                            │
│     z.B. "12:14 - 14:15"                                               │
│                                                                         │
│  3. Ort?                                                               │
│     [Büro FA] / [Büro Kunde] / [Restaurant] / [Video] / [Telefon]      │
│     oder Name eingeben: z.B. "Jacks Brasserie"                         │
│                                                                         │
│  4. FehrAdvice-Teilnehmer?                                             │
│     [GF] Gerhard Fehr / [EB] Ernst Brucker / [MR] Martin Rieder        │
│     Mehrere mit Komma: "GF, EB"                                        │
│                                                                         │
│  5. Beziehung zum Gesprächspartner?                                    │
│     [Du] / [Sie]                                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 2: Person-Profil (automatisch)

Claude prüft automatisch:
- Existiert Person bereits in `data/person-registry.yaml`?
- Existiert Kunden-Profil in `data/customers/`?

**Falls neu:** Profil-Erstellung anbieten

```
Person "Saskia Schenker" nicht gefunden.

Soll ich ein Profil erstellen? [j/n]

Wenn ja:
1. Organisation?
2. Position/Titel?
3. Bekannte Kontaktdaten? (optional)
4. Relevante Hintergründe? (optional)
```

### Schritt 3: Meeting-Inhalt

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📋 MEETING-INHALT                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Gesprächsqualität?                                                 │
│     [1] ⭐⭐⭐ Sehr gut  [2] ⭐⭐ Gut  [3] ⭐ Neutral  [4] Schwierig     │
│                                                                         │
│  2. Besprochene Themen (Stichworte):                                   │
│     z.B. "Medikamentenpreise, Strategie prio.swiss, Zusammenarbeit"    │
│                                                                         │
│  3. Verknüpfte EBF-Analyse? (optional)                                 │
│     z.B. "EBF-S-2026-02-04-POL-001"                                    │
│                                                                         │
│  4. Wichtige Erkenntnisse/Notizen:                                     │
│     (Freitext, kann auch später ergänzt werden)                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 4: Follow-ups definieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📤 FOLLOW-UP AKTIONEN                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Welche Follow-ups wurden vereinbart?                                  │
│                                                                         │
│  [1] 📄 Dokument/Analyse zusenden                                      │
│      → Welches? z.B. "Medikamentenpreis-Analyse"                       │
│      → Bis wann? z.B. "Fr 07.02."                                      │
│                                                                         │
│  [2] 📅 Folgetermin vereinbaren                                        │
│      → Thema?                                                          │
│      → Zeitrahmen? z.B. "KW 7"                                         │
│                                                                         │
│  [3] 📝 Offerte erstellen                                              │
│      → Für welches Thema?                                              │
│      → Bis wann?                                                       │
│                                                                         │
│  [4] 🔍 Recherche/Analyse durchführen                                  │
│      → Welches Thema?                                                  │
│                                                                         │
│  [5] ➕ Andere Aktion                                                  │
│                                                                         │
│  Mehrere mit Komma: "1, 3"                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 5: Lead-Eröffnung (DEFAULT)

**IMMER fragen bei neuem Kontakt - mit 3+1 Choice Architecture:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  💼 LEAD ERÖFFNEN?                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Soll für diesen Kontakt ein Lead erstellt werden?                     │
│                                                                         │
│  [j] Ja → Lead erstellen (3+1 Optionen folgen)                         │
│  [n] Nein → Nur Meeting dokumentieren                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Falls ja → 3+1 Choice Architecture für jeden Parameter:**

#### 5a. Unternehmen/Organisation

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🏢 UNTERNEHMEN                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ AUTO-FILL aus Profil: {ORGANISATION}                               │
│                                                                         │
│  [1] {ORGANISATION} (aus Profil)              ← EMPFOHLEN              │
│  [2] {ORGANISATION_KURZFORM}                                           │
│  [3] {ORGANISATION_LEGAL} (inkl. Rechtsform)                           │
│  [4] Manuell eingeben: _________________                               │
│                                                                         │
│  → Enter = Option 1                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 5b. Branche

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🏭 BRANCHE                                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ AUTO-SUGGEST basierend auf Organisation:                           │
│                                                                         │
│  [1] {BRANCHE_1} (primär)                     ← EMPFOHLEN              │
│  [2] {BRANCHE_2} (alternativ)                                          │
│  [3] {BRANCHE_3} (alternativ)                                          │
│  [4] Andere: finance | packaging | construction | fmcg | pharma_health │
│             | energy | technology | public_sector | manufacturing      │
│             | retail | professional_services                           │
│                                                                         │
│  → Enter = Option 1                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 5c. Kontaktperson & Rolle

```
┌─────────────────────────────────────────────────────────────────────────┐
│  👤 KONTAKTPERSON                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ AUTO-FILL aus Meeting:                                              │
│     Name:     {PERSON_NAME}                                            │
│     Position: {PERSON_POSITION}                                        │
│                                                                         │
│  Ist {PERSON_VORNAME} Entscheider:in?                                  │
│  [1] Ja, alleinige Entscheidungsbefugnis      ← bei C-Level/Direktor   │
│  [2] Ja, Teil des Buying Committee                                     │
│  [3] Nein, aber Champion/Influencer                                    │
│  [4] Nein, Kontakt für Weiterleitung                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 5d. Opportunity

```
┌─────────────────────────────────────────────────────────────────────────┐
│  💰 OPPORTUNITY                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ AUTO-SUGGEST basierend auf Meeting-Themen:                         │
│                                                                         │
│  [1] {OPPORTUNITY_1} (aus Gesprächsthemen)    ← EMPFOHLEN              │
│  [2] Retainer / Laufende Beratung (30-50k p.a.)                        │
│  [3] Strategieprojekt / Workshop (50-150k)                             │
│  [4] Manuell eingeben: _________________                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 5e. Stage & Phase

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 STAGE & PHASE                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ AUTO-SET (Meeting stattgefunden → PROSPECT, Phase 1):              │
│                                                                         │
│  [1] PROSPECT / Phase 1 (Kontakt)             ← DEFAULT nach Meeting   │
│  [2] QUALIFIED / Phase 2 (Rahmen geklärt)                              │
│  [3] SUSPECT / Phase 0 (nur Identifiziert)                             │
│  [4] Manuell: Stage + Phase angeben                                    │
│                                                                         │
│  → Enter = Option 1                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 5f. Behavioral Profile (EBF-spezifisch, optional)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🧠 BEHAVIORAL PROFILE (optional, aus Meeting ableitbar)                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Decision Style?                                                        │
│  [1] Analytical (datengetrieben)              ← bei Zahlen-Fokus       │
│  [2] Intuitive (erfahrungsbasiert)                                     │
│  [3] Consensus (Abstimmung im Team)                                    │
│  [4] Überspringen                                                       │
│                                                                         │
│  AI-Readiness? (basierend auf Tool-Diskussion)                         │
│  [1] Experimenting (nutzt bereits AI)         ← bei ChatGPT-Erwähnung  │
│  [2] Exploring (interessiert)                                          │
│  [3] None (kein Thema)                                                 │
│  [4] Überspringen                                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Zusammenfassung vor Erstellung:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ✅ LEAD-ZUSAMMENFASSUNG                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Lead-ID:       LEAD-{NNN} (automatisch)                               │
│                                                                         │
│  UNTERNEHMEN                                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Name:          {COMPANY}                                               │
│  Branche:       {INDUSTRY}                                              │
│  Land:          {COUNTRY}                                               │
│                                                                         │
│  KONTAKT                                                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  Name:          {PERSON_NAME}                                          │
│  Position:      {PERSON_POSITION}                                      │
│  Entscheider:   {JA/NEIN}                                              │
│                                                                         │
│  OPPORTUNITY                                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Name:          {OPPORTUNITY_NAME}                                      │
│  Stage:         {STAGE}                                                 │
│  Phase:         {PHASE} ({PHASE_NAME})                                 │
│                                                                         │
│  MEETING-LINK                                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  Meeting-ID:    {MTG-ID}                                               │
│  Datum:         {MEETING_DATE}                                          │
│                                                                         │
│  [Enter] Erstellen  |  [b] Zurück bearbeiten  |  [n] Abbrechen         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**🔴 PFLICHT: Atomare ID-Vergabe via Script**

```bash
# VOR Lead-Erstellung IMMER ausführen:
python scripts/get_next_lead_id.py
# → Gibt z.B. "LEAD-061" zurück + incrementiert automatisch
```

**Automatische Kaskade bei Lead-Eröffnung:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEAD-ERÖFFNUNG LÖST AUTOMATISCH AUS:                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  0️⃣  LEAD-ID HOLEN (PFLICHT - VOR allem anderen!)                       │
│      └── python scripts/get_next_lead_id.py → "LEAD-061"               │
│                                                                         │
│  1️⃣  KUNDE (Organisation)                                               │
│      ├── Pfad: data/customers/{org}/                                   │
│      ├── Erstellt: Falls Ordner nicht existiert                        │
│      └── Enthält: {org}_profile.yaml (Organisation)                    │
│                                                                         │
│  2️⃣  PERSON (Kontakt)                                                   │
│      ├── Pfad: data/customers/{org}/{person}_profile.yaml              │
│      ├── Erstellt: Falls Person nicht existiert                        │
│      └── Verlinkt: Mit Kunde (organisation_ref)                        │
│                                                                         │
│  3️⃣  LEAD (Sales-Eintrag)                                               │
│      ├── Pfad: data/sales/lead-database.yaml                           │
│      ├── ID: LEAD-061 (aus Script, NICHT manuell!)                          │
│      ├── Verlinkt: Mit Kunde (company.ref) + Person (contact_ref)      │
│      └── Enthält: Alle Felder aus Schritt 5a-5f                        │
│                                                                         │
│  REIHENFOLGE: Kunde → Person → Lead (Abhängigkeiten beachten)          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Referenzierung zwischen den Dateien:**

| Von | Nach | Feld | Beispiel |
|-----|------|------|----------|
| Lead | Kunde | `company.ref` | `customers/prio-swiss` |
| Lead | Person | `contacts[0].profile_ref` | `customers/prio-swiss/saskia_schenker_profile.yaml` |
| Person | Kunde | `organisation_ref` | `customers/prio-swiss` |
| Person | Lead | `sales.lead_id` | `LEAD-048` |
| Kunde | Leads | `active_leads[]` | `["LEAD-048"]` |
| Kunde | Personen | `contacts[]` | `["saskia_schenker_profile.yaml"]` |

**Automatische Verknüpfungen (Detail):**

| Datenbank | Feld | Wert |
|-----------|------|------|
| `lead-database.yaml` | Neuer LEAD-NNN Eintrag | Alle Felder aus 5a-5f |
| `lead-database.yaml` | `meetings[]` | Link zu MTG-ID |
| `lead-database.yaml` | `behavioral_profile` | Aus 5f (falls ausgefüllt) |
| `{person}_profile.yaml` | `sales.lead_id` | LEAD-NNN |
| `{person}_profile.yaml` | `sales.rolle.is_decision_maker` | true/false |
| `{org}_profile.yaml` | `active_leads[]` | LEAD-NNN hinzugefügt |
| `{org}_profile.yaml` | `contacts[]` | Person hinzugefügt |
| `meeting-registry.yaml` | `lead_ref` | LEAD-NNN |

### Schritt 6: Automatische Generierung

Claude generiert automatisch (in dieser Reihenfolge):

```
┌─────────────────────────────────────────────────────────────────────────┐
│  GENERIERUNGS-KASKADE                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Kunde-Ordner (falls neu)                                           │
│     └── data/customers/{org}/                                          │
│         └── {org}_profile.yaml                                         │
│                                                                         │
│  2. Person-Profil (falls neu)                                          │
│     └── data/customers/{org}/{person}_profile.yaml                     │
│         └── organisation_ref: → Kunde (1)                              │
│                                                                         │
│  3. Lead-Eintrag (falls Schritt 5 = Ja)                                │
│     └── data/sales/lead-database.yaml                                  │
│         ├── company.ref: → Kunde (1)                                   │
│         └── contacts[0].profile_ref: → Person (2)                      │
│                                                                         │
│  4. Rück-Referenzen aktualisieren                                      │
│     ├── {org}_profile.yaml → active_leads[] += LEAD-NNN                │
│     └── {person}_profile.yaml → sales.lead_id = LEAD-NNN               │
│                                                                         │
│  5. Outputs generieren                                                 │
│     ├── Meeting-Report → outputs/sessions/{SESSION}/...                │
│     └── Begleitschreiben → outputs/sessions/{SESSION}/...              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| # | Dokument | Pfad | Bedingung |
|---|----------|------|-----------|
| 1 | **Kunde-Ordner** | `data/customers/{org}/` | Falls Kunde neu |
| 2 | **Kunde-Profil** | `data/customers/{org}/{org}_profile.yaml` | Falls Kunde neu |
| 3 | **Person-Profil** | `data/customers/{org}/{person}_profile.yaml` | Falls Person neu |
| 4 | **Lead-Eintrag** | `data/sales/lead-database.yaml` | Falls Lead eröffnet (Schritt 5) |
| 5 | **Meeting-Report** | `outputs/sessions/{SESSION_ID}/meeting-report-{name}.md` | Immer |
| 6 | **Begleitschreiben** | `outputs/sessions/{SESSION_ID}/begleitschreiben-{name}.md` | Immer |

### Schritt 7: Bestätigung & Commit

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ✅ MEETING DOKUMENTIERT                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Meeting-ID:     MTG-2026-02-04-001                                    │
│  Session-ID:     EBF-S-2026-02-04-POL-001                              │
│                                                                         │
│  ERSTELLT:                                                              │
│  ├── outputs/sessions/.../meeting-report-saskia-schenker.md            │
│  ├── outputs/sessions/.../begleitschreiben-saskia-schenker.md          │
│  └── data/customers/prio-swiss/saskia_schenker_profile.yaml            │
│                                                                         │
│  FOLLOW-UPS:                                                            │
│  🔴 1. Analyse zusenden          → Fr 07.02.2026                       │
│  ⏳ 2. Offerte erstellen         → KW 7-8                              │
│                                                                         │
│  Git commit erstellt: "docs(meeting): ..."                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Meeting-Report Struktur (Standard)

```markdown
# Meeting-Report: [Name] ([Organisation])

**Datum:** YYYY-MM-DD | HH:MM - HH:MM
**Ort:** [Ort]
**Teilnehmer:** [FA-Teilnehmer], [Gesprächspartner]
**Session-ID:** EBF-S-YYYY-MM-DD-XXX-NNN
**Status:** ✅ MEETING DURCHGEFÜHRT

---

## 1. Gesprächspartner
[Profil-Kurzfassung]

## 2. Kontext
[Warum dieses Meeting? Vorgeschichte]

## 3. Besprochene Themen
[Bullet-Liste der Themen]

## 4. Kernerkenntnisse
[Wichtigste Takeaways]

## 5. Verknüpfte EBF-Analysen
[Links zu relevanten Analysen]

## 6. Follow-up Aktionen
[Tabelle mit Aktionen, Deadlines, Status]

## 7. Meeting-Notizen
[Detaillierte Notizen, Zitate, Beobachtungen]

---
*Erstellt: [Datum] | Meeting-ID: MTG-YYYY-MM-DD-NNN*
```

## Begleitschreiben Struktur (Standard)

```markdown
# Follow-up: [Thema]

**An:** [Name]
**Von:** [FA-Teilnehmer]
**Datum:** [Datum]
**Betreff:** [Thema] - wie besprochen

---

[Anrede basierend auf Du/Sie]

[Dank für Gespräch]

[Zusammenfassung der Kernpunkte]

[Angekündigte Beilagen]

[Nächste Schritte]

[Grussformel]

---
**Beilage:** [Liste der Dokumente]
```

## Datenstruktur

### Meeting-Registry (neu)

```yaml
# data/meeting-registry.yaml

metadata:
  version: "1.0"
  total_meetings: 15

meetings:
  - id: MTG-2026-02-04-001
    date: "2026-02-04"
    time: "12:14-14:15"
    location: "Jacks Brasserie"

    participants:
      internal:
        - id: FA-VR-001
          name: Gerhard Fehr
      external:
        - id: PER-EXT-022
          name: Saskia Schenker
          organization: prio.swiss

    relationship: "Du"
    quality: "sehr_gut"

    topics:
      - "Medikamentenpreise Trump MFN"
      - "Strategie prio.swiss"
      - "Mögliche Zusammenarbeit"

    linked_sessions:
      - EBF-S-2026-02-04-POL-001

    follow_ups:
      - action: "Analyse zusenden"
        deadline: "2026-02-07"
        status: "pending"
        owner: GF
      - action: "Offerte erstellen"
        deadline: "2026-02-14"
        status: "pending"
        owner: FA

    outputs:
      meeting_report: "outputs/sessions/EBF-S-2026-02-04-POL-001/meeting-report-saskia-schenker.md"
      cover_letter: "outputs/sessions/EBF-S-2026-02-04-POL-001/begleitschreiben-saskia-schenker.md"
```

## Integration mit anderen Skills

| Skill | Integration |
|-------|-------------|
| `/session` | Meeting wird als Session-Typ dokumentiert |
| `/followup` | Follow-ups erscheinen in täglicher Übersicht |
| `/lead-update` | Bei Neukunden: Lead-Status aktualisieren |
| `/pipeline-summary` | Meetings erscheinen in Pipeline-Aktivitäten |

## Automatische Trigger

Claude erkennt Meeting-Dokumentations-Bedarf bei:
- "Ich hatte ein Meeting mit..."
- "Heute Mittag habe ich ... getroffen"
- "Gerade aus dem Gespräch mit ... zurück"
- "Meeting-Notes zu ..."

Bei Erkennung:
```
Ich erkenne ein Meeting. Soll ich den /meeting Workflow starten?
[j] Ja, vollständig dokumentieren
[k] Kurz - nur Notizen
[n] Nein, weiter ohne Dokumentation
```

## Beispiel-Session

```
User: Ich hatte heute ein Meeting mit Saskia Schenker

Claude:
Ich erkenne ein Meeting. Soll ich den /meeting Workflow starten?
[j] Ja, vollständig dokumentieren
[k] Kurz - nur Notizen
[n] Nein

User: j

Claude:
📝 MEETING DOKUMENTIEREN

Gesprächspartner: Saskia Schenker
✓ Gefunden: PER-EXT-022, Direktorin prio.swiss

1. Datum & Zeit?
   [heute] = 04.02.2026

User: heute, 12:14 - 14:15

Claude:
2. Ort?

User: Jacks Brasserie

Claude:
3. FehrAdvice-Teilnehmer?

User: GF

Claude:
4. Beziehung?

User: Du

Claude:
5. Gesprächsqualität?

User: Sehr gut

Claude:
6. Besprochene Themen?

User: Medikamentenpreis-Case USA/Trump, Strategie prio.swiss, mögliche Zusammenarbeit

Claude:
7. Verknüpfte EBF-Analyse?

User: EBF-S-2026-02-04-POL-001

Claude:
8. Follow-ups?

User: 1 - Analyse zusenden bis Fr, 3 - Offerte KW 7-8

Claude:
✅ MEETING DOKUMENTIERT

Meeting-ID: MTG-2026-02-04-001
[... Zusammenfassung ...]

Soll ich das Begleitschreiben für den Versand vorbereiten? [j/n]
```

## Shortcuts

| Shortcut | Entspricht |
|----------|------------|
| `/mtg` | `/meeting` |
| `/mtg new` | `/meeting new` |
| `/mtg fu` | `/meeting followup` |
