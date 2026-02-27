# LEAD-ID System - Dokumentation

> Atomare ID-Vergabe mit Auto-Fix für die Lead-Datenbank

**Version:** 1.0
**Erstellt:** 2026-02-04
**Status:** AKTIV

---

## Übersicht

Das LEAD-ID System verhindert doppelte Lead-IDs durch eine 3-Ebenen-Architektur:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEAD-ID SYSTEM: 3-Ebenen-Architektur                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EBENE 1: ATOMARE ID-VERGABE (Prävention)                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  Script: scripts/get_next_lead_id.py                                   │
│  • Liest next_lead_id aus metadata                                     │
│  • Gibt LEAD-NNN zurück                                                │
│  • Incrementiert automatisch auf N+1                                   │
│  • Atomar: Lesen + Schreiben in einem Schritt                          │
│                                                                         │
│  EBENE 2: WORKFLOW-DOKUMENTATION (Anleitung)                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  Dateien:                                                              │
│  • .claude/commands/lead-add.md                                        │
│  • .claude/commands/meeting.md                                         │
│  Regeln:                                                               │
│  • VERBOTEN: Manuell IDs vergeben                                      │
│  • PFLICHT: python scripts/get_next_lead_id.py                         │
│                                                                         │
│  EBENE 3: AUTO-FIX HOOK (Sicherheitsnetz)                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  Datei: .claude/hooks/pre-commit.sh                                    │
│  • Erkennt Duplikate vor jedem Commit                                  │
│  • Benennt automatisch um (erste behalten, Rest neue IDs)              │
│  • Re-staged die korrigierte Datei                                     │
│  • Korrigiert next_lead_id falls nötig                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Komponenten

### 1. ID-Tracker (SSOT)

**Datei:** `data/sales/lead-database.yaml`

```yaml
metadata:
  next_lead_id: 61  # ← Single Source of Truth
```

- Einzige autoritative Quelle für die nächste freie ID
- Wird NUR durch das Script verändert
- Niemals manuell editieren!

### 2. ID-Vergabe Script

**Datei:** `scripts/get_next_lead_id.py`

```bash
# Standard: ID holen und incrementieren
python scripts/get_next_lead_id.py
# → Ausgabe: LEAD-061
# → next_lead_id wird auf 62 gesetzt

# Nur schauen (ohne Increment)
python scripts/get_next_lead_id.py --peek
# → Ausgabe: LEAD-061
# → next_lead_id bleibt bei 61

# Konsistenz prüfen
python scripts/get_next_lead_id.py --validate
# → Prüft auf Duplikate und next_lead_id > höchste ID
```

### 3. Pre-Commit Hook (Auto-Fix)

**Datei:** `.claude/hooks/pre-commit.sh`

**Was passiert bei einem Commit:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  COMMIT-ABLAUF                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. git commit                                                          │
│       ↓                                                                 │
│  2. Hook prüft lead-database.yaml                                      │
│       ↓                                                                 │
│  3. Duplikate gefunden?                                                │
│       │                                                                 │
│       ├── NEIN → "✅ All LEAD-IDs are unique" → Commit OK              │
│       │                                                                 │
│       └── JA → Auto-Fix:                                               │
│           ├── Erste Occurrence behalten                                │
│           ├── Nachfolgende umbenennen via Script                       │
│           ├── Datei re-stagen                                          │
│           └── Commit läuft durch                                       │
│                                                                         │
│  4. next_lead_id prüfen                                                │
│       │                                                                 │
│       ├── OK → Weiter                                                  │
│       └── Zu niedrig → Automatisch korrigieren                         │
│                                                                         │
│  5. ✅ Commit erfolgreich                                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Workflows

### Neuen Lead erstellen

```bash
# SCHRITT 1: ID holen (PFLICHT!)
python scripts/get_next_lead_id.py
# → Ausgabe: LEAD-061

# SCHRITT 2: Lead mit dieser ID erstellen
# In lead-database.yaml:
- id: LEAD-061
  company:
    name: "Neue Firma AG"
  ...

# SCHRITT 3: Commit
git add data/sales/lead-database.yaml
git commit -m "feat(sales): Add lead LEAD-061"
# → Hook prüft und bestätigt Eindeutigkeit
```

### Meeting mit Lead-Eröffnung

Siehe `.claude/commands/meeting.md` - Schritt 5 (Lead-Eröffnung).

Das Script wird automatisch in Schritt 0 aufgerufen, BEVOR die Kaskade startet:

```
0️⃣  LEAD-ID HOLEN → python scripts/get_next_lead_id.py
1️⃣  KUNDE erstellen
2️⃣  PERSON erstellen
3️⃣  LEAD erstellen (mit ID aus Schritt 0)
```

---

## Fehlerbehebung

### Problem: Duplikat wurde trotzdem committed

**Sollte nicht passieren** (Auto-Fix greift), aber falls doch:

```bash
# 1. Validierung ausführen
python scripts/get_next_lead_id.py --validate

# 2. Falls Duplikate angezeigt werden:
#    - Die YAML-Datei öffnen
#    - Den ZWEITEN Eintrag mit der doppelten ID finden
#    - Neue ID via Script holen
#    - Manuell umbenennen
#    - Commit + Push
```

### Problem: next_lead_id ist zu niedrig

```bash
# Der Hook korrigiert das automatisch beim nächsten Commit.
# Oder manuell:
python scripts/get_next_lead_id.py --validate
# Zeigt den korrekten Wert an, dann manuell in metadata setzen.
```

### Problem: Script nicht gefunden

```bash
# Prüfen ob Script existiert:
ls -la scripts/get_next_lead_id.py

# Falls nicht: Aus Git wiederherstellen
git checkout HEAD -- scripts/get_next_lead_id.py
```

---

## Regeln

### VERBOTEN

```
❌ ID manuell aus metadata lesen und verwenden
❌ next_lead_id manuell incrementieren
❌ ID "schätzen" oder annehmen (z.B. "wahrscheinlich LEAD-062")
❌ Zwei Leads mit derselben ID erstellen
```

### PFLICHT

```
✅ IMMER: python scripts/get_next_lead_id.py vor Lead-Erstellung
✅ Script-Output DIREKT verwenden (nicht merken und später nutzen)
✅ Bei Meeting-Workflow: Schritt 0 (ID holen) vor Kaskade
```

### ERLAUBT

```
✅ --peek für Vorschau ohne Increment
✅ --validate für Konsistenzprüfung
✅ Auf Auto-Fix vertrauen (wird automatisch korrigiert)
```

---

## Technische Details

### ID-Format

```
LEAD-{NNN}
```

- `NNN` = Dreistellige Nummer mit führenden Nullen
- Beispiele: LEAD-001, LEAD-042, LEAD-100

### Atomarität

Das Script garantiert Atomarität durch:
1. Datei komplett lesen
2. Regex-basiertes Parsen (keine YAML-Library)
3. Wert extrahieren, incrementieren, zurückschreiben
4. Alles in einer Python-Funktion

### Hook-Logik

```bash
# Duplikat-Erkennung
grep -E "^  - id: LEAD-[0-9]+" "$LEAD_DB" | sort | uniq -d

# Umbenennung via sed (zeilengenau)
sed -i "${LINE_NUM}s/id: $DUP_ID/id: $NEW_ID  # Auto-fixed from $DUP_ID/"
```

---

## Statistiken

| Metrik | Wert |
|--------|------|
| Aktuelle Leads | 60 |
| Höchste ID | LEAD-060 |
| Nächste freie ID | LEAD-061 |
| Duplikate (aktuell) | 0 |

**Stand:** 2026-02-04

---

## Änderungshistorie

| Datum | Version | Änderung |
|-------|---------|----------|
| 2026-02-04 | 1.0 | Initiale Dokumentation |
| 2026-02-04 | 1.0 | Auto-Fix implementiert (Option C) |
| 2026-02-04 | 1.0 | 9 Duplikate behoben (LEAD-045 bis LEAD-057) |

---

## Referenzen

- **Script:** `scripts/get_next_lead_id.py`
- **Datenbank:** `data/sales/lead-database.yaml`
- **Hook:** `.claude/hooks/pre-commit.sh`
- **Workflow Lead-Add:** `.claude/commands/lead-add.md`
- **Workflow Meeting:** `.claude/commands/meeting.md`

---

*Dokumentation erstellt von Claude Code | Session: EBF-S-2026-02-04-POL-001*
