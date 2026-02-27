# /learnings - EBF Learnings Management System

> Maschinelles Lernen aus Fehlern für alle EBF-Domains

## Übersicht

Das EBF Learnings System erfasst, speichert und macht Lessons Learned aus allen Workflows durchsuchbar. Jede Domain hat eine eigene YAML-Datenbank mit strukturierten Einträgen.

## Domains

| Domain | Code | Beschreibung | Datei |
|--------|------|--------------|-------|
| Report Formatter | `RPT` | PDF-Generierung, Templates, WeasyPrint | `data/report-formatter-learnings.yaml` |
| Innosuisse | `INO` | BEATRIX, Förderanträge, Dokument-Adaption | `data/innosuisse-learnings.yaml` |
| Paper Integration | `INT` | Paper-Aufnahme, BibTeX, LIT-Appendices | `data/paper-integration-learnings.yaml` |
| Model Building | `MOD` | 10C-Modelle, Parameter, Interventionen | `data/model-building-learnings.yaml` |
| Evidence Integration | `EIP` | Konzept-Validierung, PRO/CONTRA Evidenz | `data/eip-learnings.yaml` |
| General | `GEN` | Allgemeine Workflows, Git, Tooling | `data/general-learnings.yaml` |

## Verwendung

### Learnings auflisten

```bash
# Alle Learnings einer Domain
python scripts/learnings.py list RPT

# Mit Severity-Filter
python scripts/learnings.py list INO --severity high

# Mit Kategorie-Filter
python scripts/learnings.py list RPT --category TEMPLATE
```

### Neues Learning hinzufügen

```bash
# Interaktiv
python scripts/learnings.py add RPT

# Direkt mit Parametern
python scripts/learnings.py add MOD --title "Parameter-Drift" --problem "..." --solution "..."
```

### Learnings durchsuchen

```bash
# Volltextsuche über alle Domains
python scripts/learnings.py search "template"

# Nur bestimmte Domain
python scripts/learnings.py search "WeasyPrint" --domain RPT
```

### Statistiken anzeigen

```bash
# Übersicht aller Domains
python scripts/learnings.py stats

# Bestimmte Domain
python scripts/learnings.py stats RPT
```

### Kontext-Check (automatisch)

```bash
# Prüft git diff und zeigt relevante Learnings
python scripts/learnings.py check
```

## Learning-Schema

Jedes Learning hat folgende Struktur:

```yaml
- id: "RPT-L-001"
  date: "2026-01-28"
  category: "TEMPLATE"
  severity: "high"  # high, medium, low
  title: "Kurztitel"
  problem: |
    Was ist passiert?
  solution: |
    Wie wurde es gelöst?
  prevention: |
    Wie kann es verhindert werden?
  related_files:
    - scripts/format_report.py
    - templates/fehradvice-cover.latex
  tags:
    - pdf
    - template
```

## Integration in Workflows

### Pre-Commit Hook

Der Pre-Commit Hook zeigt einen Reminder wenn:
- Relevante Dateien geändert wurden
- Aber keine Learnings hinzugefügt wurden

### Session-Start

Bei Session-Start wird automatisch `learnings check` ausgeführt um relevante Learnings für die aktuelle Arbeit zu zeigen.

### Nach Fehlern

Nach jedem Fehler sollte via `/learnings add <DOMAIN>` ein Learning erfasst werden:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🧠 LEARNING ERFASSEN                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Fehler ist aufgetreten                                              │
│  2. Fehler wurde behoben                                                │
│  3. → python scripts/learnings.py add <DOMAIN>                          │
│  4. Learning wird in YAML gespeichert                                   │
│  5. Bei ähnlichen Situationen: Automatische Anzeige                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Kategorien pro Domain

### RPT (Report Formatter)
- `TEMPLATE`: LaTeX/HTML Templates
- `PDF`: PDF-Generierung, Merging
- `CONFIG`: Konfiguration, Pfade
- `WORKFLOW`: Prozess-Ablauf

### INO (Innosuisse)
- `DOC`: Dokument-Adaption
- `CONSISTENCY`: Konsistenz-Fehler
- `CLASSIFICATION`: Inhalts-Klassifikation
- `VERIFICATION`: Vollständigkeits-Prüfung

### INT (Paper Integration)
- `BIBTEX`: BibTeX-Einträge
- `LIT`: LIT-Appendix Zuordnung
- `THEORY`: Theorie-Katalog
- `LEVEL`: Integration Level

### MOD (Model Building)
- `10C`: 10C-Framework
- `PARAMETER`: Parameter-Schätzung
- `GAMMA`: Komplementaritäts-Matrix
- `INTERVENTION`: Interventions-Design

### EIP (Evidence Integration)
- `PRO`: PRO-Evidenz Suche
- `CONTRA`: CONTRA-Evidenz Suche
- `DECISION`: Entscheidungs-Matrix
- `CONCEPT`: Konzept-Definition

### GEN (General)
- `GIT`: Git-Workflows
- `TOOL`: Tooling, Scripts
- `CLAUDE`: Claude Code Features
- `YAML`: YAML-Datenbanken

## Best Practices

1. **Sofort erfassen**: Learning direkt nach dem Fehler dokumentieren
2. **Konkret sein**: Problem und Lösung mit Code-Beispielen
3. **Tags nutzen**: Für bessere Durchsuchbarkeit
4. **Related Files**: Alle betroffenen Dateien verlinken
5. **Prevention**: Immer angeben wie der Fehler verhindert werden kann

## Siehe auch

- `/innosuisse` - Innosuisse/BEATRIX Workflow mit Learnings-Integration
- `/integrate-paper` - Paper Integration mit Level-Klassifikation
- `/design-model` - Model Building Workflow
