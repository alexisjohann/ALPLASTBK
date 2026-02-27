# /session - Session Management & Learning Skill

Automatisches Session-Tracking für User-Behavior-Learning.

## Überblick

Dieser Skill verwaltet EBF-Sessions mit automatischem Superkey und Learning-Extraktion.

## Befehle

### `/session start`
Startet eine neue Session mit automatischem Superkey.

```
/session start [--domain DOMAIN] [--user USER_ID]
```

**Parameter:**
- `--domain`: REL, FIN, HLT, ENV, POL, ORG, EDU, INT, OTH (auto-detect wenn nicht angegeben)
- `--user`: User-ID aus team.yaml (z.B. FA-VR-001)

**Output:**
```
┌─────────────────────────────────────────────────────────────────┐
│  🚀 SESSION GESTARTET                                           │
├─────────────────────────────────────────────────────────────────┤
│  Superkey:  EBF-S-2026-01-29-ORG-002                           │
│  User:      Gerhard Fehr (FA-VR-001)                           │
│  Domain:    ORG (Organization)                                  │
│  Start:     2026-01-29T15:30:00+01:00                          │
│                                                                 │
│  Diese Session wird automatisch dokumentiert.                   │
│  Am Ende: /session end                                         │
└─────────────────────────────────────────────────────────────────┘
```

### `/session end`
Beendet die Session und dokumentiert Learnings.

```
/session end [--learnings "..."]
```

**Automatisch dokumentiert:**
- Session-Narrative (was ist passiert?)
- User-Verhalten (welche Patterns?)
- Outputs (welche Dateien erstellt?)
- Learnings (was gelernt?)

### `/session status`
Zeigt aktuelle Session-Info.

### `/session learn`
Zeigt extrahierte Learnings aus allen Sessions.

```
/session learn [--pattern PATTERN_TYPE] [--user USER_ID]
```

**Pattern Types:**
- `context`: Kontext-Präferenzen
- `model`: Modell-Präferenzen
- `workflow`: Workflow-Patterns
- `behavior`: User-Verhalten
- `all`: Alle Patterns

## Automatismen

### Bei Session-Start (automatisch)

1. **Superkey generieren:**
   ```
   EBF-S-{YYYY}-{MM}-{DD}-{DOMAIN}-{SEQ}
   ```

2. **User identifizieren:**
   - Prüfe team.yaml nach bekannten Usern
   - Frage nach User-ID wenn nicht erkannt

3. **Session-Datei erstellen:**
   ```
   .claude/current-session.yaml
   ```

### Während der Session (automatisch)

Claude dokumentiert automatisch:
- Jede User-Frage
- Jede Interpretation
- Jede Korrektur durch User
- Alle erstellten Outputs

### Bei Session-Ende (automatisch oder manuell)

1. **Learnings extrahieren:**
   - User-Behavior-Patterns
   - Preference-Patterns
   - Correction-Patterns

2. **In Datenbank speichern:**
   ```
   data/model-building-session.yaml
   ```

3. **Learning-Patterns aktualisieren:**
   ```yaml
   learning_patterns:
     user_patterns:
       - user_id: FA-VR-001
         pattern: "Korrigiert Web-Recherche-Ergebnisse"
         frequency: 3
         recommendation: "Immer User-Validierung einholen"
   ```

## Session-Typen

| Typ | Beschreibung | Trigger |
|-----|--------------|---------|
| `ANALYSIS` | EBF-Analyse (10C Workflow) | Inhaltliche Frage |
| `OPERATIONAL` | Infrastruktur/Tooling | Datenbank-Erstellung |
| `DEMO` | EBF-Demo/Training | "zeigen", "erklären" |
| `RESEARCH` | Literatur-Recherche | Paper, Theorie |

## Learning-Kategorien

### LP-USR: User-Behavior Patterns
```yaml
- pattern_id: "LP-USR-001"
  user_id: "FA-VR-001"
  pattern: "Startet mit vager Aussage, präzisiert iterativ"
  observed_in: ["EBF-S-2026-01-29-ORG-002"]
  recommendation: "Nachfragen statt Annehmen"
```

### LP-CTX: Context Patterns
```yaml
- pattern_id: "LP-CTX-001"
  pattern: "User wählt 'Alle' bei Kontext-Erweiterungen"
  frequency: 5
  recommendation: "Vollständige Ψ-Dimensionen als Default"
```

### LP-COR: Correction Patterns
```yaml
- pattern_id: "LP-COR-001"
  pattern: "Web-Recherche-Ergebnisse oft veraltet"
  frequency: 3
  recommendation: "Immer User-Validierung vor Finalisierung"
```

## Integration mit Team-Datenbank

Der Skill nutzt `data/fehradvice/team.yaml` für:
- User-Identifikation
- EBF-Proficiency-Tracking
- Training-Session-Dokumentation

## Beispiel-Workflow

```
# 1. Session starten (automatisch bei erster Nachricht)
Claude: "Session gestartet: EBF-S-2026-01-29-ORG-002"

# 2. Während der Session
User: "Ich hatte ein Meeting mit Assura"
Claude: [dokumentiert: "User startet mit vager Aussage"]

User: "Marwin ist FehrAdvice-Mitarbeiter"
Claude: [dokumentiert: "User korrigiert Interpretation"]

# 3. Session beenden
/session end

# 4. Learnings verfügbar
/session learn --user FA-VR-001
```

## Datenstruktur

### current-session.yaml (temporär)
```yaml
session_id: "EBF-S-2026-01-29-ORG-002"
user_id: "FA-VR-001"
domain: "ORG"
started: "2026-01-29T15:30:00+01:00"
type: "OPERATIONAL"

narrative:
  - step: 1
    timestamp: "2026-01-29T15:30:15"
    user_input: "Ich hatte heute ein Meeting mit Assura"
    interpretation: "Kunden-Meeting dokumentieren"

  - step: 2
    timestamp: "2026-01-29T15:31:00"
    user_input: "Marwin ist FehrAdvice-Mitarbeiter"
    correction: true
    learning: "Namen nachfragen, nicht annehmen"

outputs_created:
  - path: "data/fehradvice/team.yaml"
    type: "database"
```

## Automatische Trigger

Claude erkennt Session-Ende automatisch bei:
- "Danke, das war's"
- "Fertig für heute"
- "Das reicht"
- Keine Aktivität > 30 Minuten

Bei Erkennung: `/session end` automatisch ausführen.
