# /innosuisse - Innosuisse Projekt-Workflow (BEATRIX)

Verwende diesen Skill für ALLE Aufgaben im Innosuisse-Projekt (BEATRIX Innovation Cheque).

## Verwendung

```
/innosuisse                    # Workflow starten (interaktiv)
/innosuisse check              # Lerndatenbank konsultieren
/innosuisse query --error-type CONSISTENCY  # Nach Fehlertyp filtern
/innosuisse query --tag latex  # Nach Tag filtern
/innosuisse add                # Neues Learning hinzufügen
/innosuisse stats              # Statistiken anzeigen
```

---

## AUTOMATISCHE TRIGGER

**Dieser Skill wird AUTOMATISCH aktiviert wenn:**

| Trigger | Bedingung |
|---------|-----------|
| **T1** | Datei in `docs/funding/` wird bearbeitet |
| **T2** | Begriff "Innosuisse" erscheint |
| **T3** | Begriff "BEATRIX" erscheint |
| **T4** | Begriff "Innovation Cheque" erscheint |
| **T5** | Dokument-Version-Update (V4.x → V4.y) |
| **T6** | Meeting-Transkript mit "Fehr" oder "Luger" |

**Bei Trigger-Erkennung MUSS Claude:**
1. `/innosuisse check` automatisch ausführen
2. Relevante Learnings identifizieren
3. A-Priori Fehlerprävention anwenden
4. Nach Abschluss: Neue Learnings dokumentieren

---

## FEHLERTYP-PRÄVENTION

### Die 8 Fehlertypen

| Code | Name | Prävention |
|------|------|------------|
| **CONSISTENCY** | Konsistenzfehler | Checkliste mit allen betroffenen Stellen |
| **CLASSIFICATION** | Klassifikationsfehler | Inhalte vor Verarbeitung kategorisieren |
| **VERIFICATION** | Verifikationsfehler | Mit grep/Zeilennummern beweisen |
| **OUTPUT_FORMAT** | Ausgabeformat-Fehler | Format-Anforderung klären |
| **DOMAIN_KNOWLEDGE** | Domänenwissen-Fehler | Interne Dokumentation konsultieren |
| **TOOL_SEQUENCE** | Werkzeug-Reihenfolge | Workflow dokumentieren und befolgen |
| **CHECKLIST** | Checklisten-Fehler | Systematische Prüfung durchführen |
| **ASSUMPTION** | Annahme-Fehler | Rückfrage stellen statt annehmen |

### Vor jeder BEATRIX-Aufgabe prüfen

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FEHLERPRÄVENTION CHECKLIST (vor Beginn)                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ☐ CONSISTENCY: Welche Stellen müssen synchron aktualisiert werden?    │
│  ☐ CLASSIFICATION: Sind alle Inhalte nach Typ kategorisiert?           │
│  ☐ VERIFICATION: Wie werde ich Vollständigkeit BEWEISEN?               │
│  ☐ OUTPUT_FORMAT: Welches Format wird erwartet?                        │
│  ☐ DOMAIN_KNOWLEDGE: Welches Domänenwissen ist kritisch?               │
│  ☐ TOOL_SEQUENCE: In welcher Reihenfolge arbeite ich?                  │
│  ☐ CHECKLIST: Welche systematischen Prüfungen mache ich?               │
│  ☐ ASSUMPTION: Welche Annahmen mache ich? Stimmen sie?                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## BEATRIX-SPEZIFISCHE CHECKLISTEN

### 7-Stellen Checkliste für Kernaussagen

Bei Änderungen an BEATRIX-Kernaussagen (z.B. "Wechselwirkungen in der Realität"):

```
☐ 1. Abstract
☐ 2. Säulen-Titel (subsubsection)
☐ 3. Säulen-Haupttext
☐ 4. "Warum ist das neu?"-Abschnitt
☐ 5. Summary-Box (fbox)
☐ 6. Gesamtzusammenfassung-Tabelle
☐ 7. Glossar-Eintrag
```

**Verifizierung:**
```bash
grep -n "Wechselwirkungen" docs/funding/BEATRIX-*.tex
```

### 3-Stellen Checkliste für Versionsnummern

Bei Version-Updates (z.B. V4.1 → V4.2):

```
☐ 1. Header/Kommentar-Block (Zeile 1-6)
☐ 2. Titelseite (\large Version X.X)
☐ 3. Footer (\small Version: X.X)
```

**Verifizierung:**
```bash
grep -n "Version" docs/funding/BEATRIX-*.tex
```

---

## ERNST FEHR BEATRIX-KORREKTUR

**KRITISCH: Diese Beschreibung ist die EINZIG KORREKTE:**

```
FALSCH: "BEATRIX analysiert Wechselwirkungen zwischen Massnahmen"
RICHTIG: "BEATRIX erfasst Wechselwirkungen, die in der Realität
         stattfinden (psychologisch, finanziell, kulturell) und
         schlägt darauf basierend Massnahmen vor"
```

**Drei Elemente der Kernbeschreibung:**
1. Erfasst Wechselwirkungen IN DER REALITÄT (nicht zwischen Massnahmen)
2. Drei Ebenen: psychologisch, finanziell, kulturell
3. Schlägt Massnahmen VOR (nicht nur analysiert)

---

## MEETING-TRANSKRIPT ANALYSE

Bei Meeting-Transkripten mit Ernst Fehr / Johannes Luger:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TRANSKRIPT-ANALYSE WORKFLOW                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Teilnehmer-Liste erstellen                                          │
│                                                                         │
│  2. Pro Teilnehmer kategorisieren:                                      │
│     - INHALTLICH: Textänderungen, Korrekturen, neue Inhalte            │
│     - ORGANISATORISCH: "Mhm", Bestätigungen, Termine                   │
│                                                                         │
│  3. Nur INHALTLICHE Inputs in Dokument einarbeiten                     │
│                                                                         │
│  4. Bei Rückfrage klar kommunizieren:                                  │
│     "X hatte keine inhaltlichen Inputs"                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## LERNDATENBANK ABFRAGEN

### Nach Fehlertyp

```bash
python scripts/query_learnings.py --error-type CONSISTENCY
python scripts/query_learnings.py --error-type VERIFICATION
```

### Nach Kategorie

```bash
python scripts/query_learnings.py --category DOC   # Dokument-Erstellung
python scripts/query_learnings.py --category MEET  # Meeting-Verarbeitung
python scripts/query_learnings.py --category COMM  # Kommunikation
```

### Nach Tag

```bash
python scripts/query_learnings.py --tag latex
python scripts/query_learnings.py --tag kernaussage
python scripts/query_learnings.py --tag ernst-fehr
```

### Statistiken

```bash
python scripts/query_learnings.py --stats
```

---

## NEUES LEARNING HINZUFÜGEN

Nach Abschluss einer Aufgabe mit neuem Learning:

### 1. ID generieren

Format: `INO-L-{YYYY-MM-DD}-{CAT}-{NNN}`

Kategorien:
- DOC: Dokument-Erstellung und -Adaption
- PROC: Prozess und Workflow
- TECH: Technische Aspekte
- COMM: Kommunikation und Feedback
- QA: Qualitätssicherung
- MEET: Meeting-Verarbeitung

### 2. Template ausfüllen

```yaml
- id: "INO-L-YYYY-MM-DD-CAT-NNN"
  date: "YYYY-MM-DD"
  session: "Beschreibende Session-ID"
  category: "DOC|PROC|TECH|COMM|QA|MEET"
  error_type: "CONSISTENCY|CLASSIFICATION|VERIFICATION|OUTPUT_FORMAT|DOMAIN_KNOWLEDGE|TOOL_SEQUENCE|CHECKLIST|ASSUMPTION"
  title: "Kurzer, prägnanter Titel"
  problem: |
    Was war das Problem?
  concrete_example: |
    Konkretes Beispiel aus dem Projekt: Was genau ist passiert?
    Mit Dateinamen, Zeilennummern, Personennamen etc.
  learning: |
    Was wurde gelernt?
  checklist:
    - "Punkt 1"
    - "Punkt 2"
  prevention: |
    Wie kann das Problem in Zukunft vermieden werden?
  severity: "low|medium|high|critical"
  tags: ["tag1", "tag2"]
```

### 3. In Lerndatenbank eintragen

Datei: `data/innosuisse-learning-database.yaml`

### 4. Commit

```bash
git add data/innosuisse-learning-database.yaml
git commit -m "feat(learning): Add learning INO-L-YYYY-MM-DD-CAT-NNN"
```

---

## WORKFLOW: Vollständige Innosuisse-Aufgabe

```
┌─────────────────────────────────────────────────────────────────────────┐
│  INNOSUISSE AUFGABE WORKFLOW                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: VOR BEGINN                                                    │
│  ────────────────────                                                   │
│  1. /innosuisse check ausführen                                         │
│  2. Relevante Learnings identifizieren                                  │
│  3. Fehlerprävention-Checkliste durchgehen                             │
│  4. Bei Kernaussagen: 7-Stellen Liste vorbereiten                      │
│  5. Bei Versionen: 3-Stellen Liste vorbereiten                         │
│                                                                         │
│  PHASE 2: DURCHFÜHRUNG                                                  │
│  ─────────────────────                                                  │
│  6. Aufgabe durchführen                                                │
│  7. Bei jeder Änderung: Konsistenz prüfen                              │
│  8. Verifizierung mit grep -n dokumentieren                            │
│                                                                         │
│  PHASE 3: ABSCHLUSS                                                     │
│  ────────────────────                                                   │
│  9. Vollständigkeit BEWEISEN (nicht behaupten)                         │
│  10. Neue Learnings identifizieren                                      │
│  11. Bei neuem Learning: /innosuisse add                               │
│  12. Commit mit aussagekräftiger Message                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## REFERENZ-DATEIEN

| Datei | Zweck |
|-------|-------|
| `data/innosuisse-learning-database.yaml` | Lerndatenbank (SSOT) |
| `scripts/query_learnings.py` | Abfrage-Script |
| `docs/funding/BEATRIX-INNOSUISSE-ANTRAGSTEXT-V4.2.tex` | Aktuelles BEATRIX-Dokument |
| `appendices/BN_REF-SUPERKEY_database_superkey_specification.tex` | Superkey-Spezifikation |

---

## VERWANDTE SKILLS

| Skill | Verwendung |
|-------|------------|
| `/design-model` | Falls Verhaltensmodell für BEATRIX benötigt |
| `/compile` | LaTeX → PDF kompilieren |
| `/check-compliance` | Dokumentenstruktur prüfen |

---

Version 1.0 | Januar 27, 2026 | Claude Code
