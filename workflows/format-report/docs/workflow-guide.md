# FehrAdvice Report Formatter - Workflow Guide

## Übersicht

Dieser Workflow konvertiert Markdown-Reports automatisch in voll formatierte FehrAdvice-Dokumente mit Corporate Design.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WORKFLOW: Markdown → Formatiertes Dokument                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INPUT                    PROCESSING                    OUTPUT          │
│  ─────                    ──────────                    ──────          │
│                                                                         │
│  ┌──────────┐     ┌─────────────────────┐     ┌──────────────────┐     │
│  │ Markdown │────►│ format_report.py    │────►│ PDF / HTML /     │     │
│  │ (.md)    │     │                     │     │ PPTX / DOCX      │     │
│  └──────────┘     │ • Schweizer Ortho.  │     └──────────────────┘     │
│                   │ • Unicode-Handling  │                               │
│  ┌──────────┐     │ • Template-Apply    │     ┌──────────────────┐     │
│  │ YAML     │────►│ • Metadata-Extract  │────►│ Corporate Design │     │
│  │ Frontmat.│     │ • Pandoc-Convert    │     │ angewandt        │     │
│  └──────────┘     └─────────────────────┘     └──────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Voraussetzungen

### System-Abhängigkeiten

```bash
# Werden automatisch vom Session-Start Hook installiert
apt-get install pandoc texlive-xetex texlive-fonts-recommended \
  texlive-fonts-extra texlive-latex-extra texlive-lang-german \
  latexmk fonts-roboto fonts-open-sans
```

### Python-Abhängigkeiten

```bash
pip install pyyaml weasyprint
```

### Prüfen

```bash
python scripts/format_report.py --check-deps
```

## Verwendung

### 1. Einzelne Datei konvertieren

```bash
# Standard: Markdown → PDF
python scripts/format_report.py report.md

# PDF mit professioneller Cover-Page (empfohlen für Kundenreports)
python scripts/format_report.py report.md --cover

# Mit explizitem Output-Pfad
python scripts/format_report.py report.md -o /path/to/output.pdf

# HTML-Output (empfohlen für komplexe Dokumente)
python scripts/format_report.py report.md -f html

# PDF via WeasyPrint mit Cover (für Dokumente mit Emojis + Cover)
python scripts/format_report.py report.md --engine weasyprint --cover

# PowerPoint-Output
python scripts/format_report.py report.md -f pptx

# Word-Output
python scripts/format_report.py report.md -f docx
```

### 2. Batch-Konvertierung

```bash
# Alle Markdown-Dateien in einem Verzeichnis
python scripts/format_report.py --batch outputs/sessions/

# Mit spezifischem Format
python scripts/format_report.py --batch outputs/sessions/ -f html
```

### 3. Session-Report formatieren

```bash
/format-report --session EBF-S-2026-01-29-POL-001
```

### 4. Datei analysieren (vor Konvertierung)

```bash
python scripts/format_report.py --analyze report.md
```

## YAML Frontmatter

Das Script extrahiert Metadaten aus dem YAML-Frontmatter:

```yaml
---
title: "Strategisches Dossier"
subtitle: "Fiskalische Disziplin in der Schweiz"
doctype: "Strategisches Dossier"
session-id: "EBF-S-2026-01-29-POL-001"
date: "29. Januar 2026"
author: "FehrAdvice & Partners AG"
client: "Eidgenössische Finanzverwaltung"  # Optional: für Cover-Page
---
```

## Cover-Page (--cover)

Die `--cover` Option fügt eine professionelle FehrAdvice-Deckseite mit TikZ-Design hinzu:

```bash
# PDF mit Cover-Page generieren
python scripts/format_report.py report.md --cover
```

### Cover-Page Elemente

| Element | Quelle | Fallback |
|---------|--------|----------|
| Logo | `assets/fehradvice-logo.png` | Text-Box "FehrAdvice" |
| Dokumenttyp | YAML `doctype` | "Strategisches Dossier" |
| Titel | YAML `title` | Dateiname |
| Untertitel | YAML `subtitle` | (leer) |
| Kunde | YAML `client` | (nicht angezeigt) |
| Session-ID | YAML `session-id` | (nicht angezeigt) |
| Datum | YAML `date` | Aktuelles Datum |

### Cover-Page Design

```
┌─────────────────────────────────────────────────────────────────┐
│  ████████████████████████████████████████  (Dunkelblau Bar)    │
│  [LOGO]                                                         │
│  ════════════════════════════════════════  (Hellblau Akzent)   │
│                                                                 │
│                    DOKUMENTTYP                                  │
│                                                                 │
│                    HAUPTTITEL                                   │
│                                                                 │
│                    Untertitel                                   │
│                                                                 │
│                    ───────────                                  │
│                                                                 │
│                FehrAdvice & Partners AG                         │
│              Evidence-Based Framework (EBF)                     │
│                  Kunde: [Client]                                │
│                Session: [Session-ID]                            │
│                  Datum: [Date]                                  │
│                                                                 │
│  ════════════════════════════════════════  (Hellblau Akzent)   │
│  ████████████████████████████████████████  (Dunkelblau Bar)    │
│            www.fehradvice.com                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Cover-Page Template anpassen

Das Template befindet sich in `templates/fehradvice-cover.latex` und kann für Kundenprojekte angepasst werden.

## Back-Page (--back)

Die `--back` Option fügt eine professionelle FehrAdvice-Rückseite mit Kontaktdaten und Disclaimer hinzu:

```bash
# PDF mit Back-Page generieren
python scripts/format_report.py report.md --back

# Vollständiges Dokument mit Cover + Back
python scripts/format_report.py report.md --cover --back
```

### Back-Page Elemente

| Element | Inhalt |
|---------|--------|
| Logo | FehrAdvice Logo (mit Fallback) |
| Firmenname | FehrAdvice & Partners AG |
| Tagline | Behavioral Strategy Consulting |
| Motto | Verhalten verstehen, Verhalten verändern |
| Kontakt | Adresse, E-Mail, Telefon, Website |
| Disclaimer | Vertraulichkeitshinweis (DE + EN) |
| Copyright | © [Jahr] FehrAdvice & Partners AG |

### Back-Page Design

```
┌─────────────────────────────────────────────────────────────────┐
│  ████████████████████████████████████████  (Dunkelblau Bar)    │
│  ════════════════════════════════════════  (Hellblau Akzent)   │
│                                                                 │
│                    [LOGO]                                       │
│                                                                 │
│            FehrAdvice & Partners AG                             │
│                                                                 │
│           Behavioral Strategy Consulting                        │
│      Verhalten verstehen, Verhalten verändern                   │
│                                                                 │
│                    Kontakt                                      │
│                Klausstrasse 4                                   │
│                8008 Zürich                                      │
│                   Schweiz                                       │
│                                                                 │
│            info@fehradvice.com                                  │
│             +41 44 256 79 00                                    │
│            www.fehradvice.com                                   │
│                                                                 │
│           ┌─────────────────────────────┐                       │
│           │   Vertraulichkeitshinweis   │                       │
│           │   Confidentiality Notice    │                       │
│           └─────────────────────────────┘                       │
│                                                                 │
│  ════════════════════════════════════════  (Hellblau Akzent)   │
│  ████████████████████████████████████████  (Dunkelblau Bar)    │
│       © 2026 FehrAdvice & Partners AG                           │
└─────────────────────────────────────────────────────────────────┘
```

### Back-Page Template anpassen

Das Template befindet sich in `templates/fehradvice-back.latex` und kann angepasst werden.

## Automatisch angewandte Features

### 1. FehrAdvice Corporate Design

| Element | Wert |
|---------|------|
| Primärfarbe (Headlines) | `#024079` (Dunkelblau) |
| Sekundärfarbe | `#549EDE` (Hellblau) |
| Textfarbe | `#25212A` (Dunkelgrau) |
| Hintergrund | `#F3F5F7` (Hellgrau) |

### 2. Schweizer Orthographie

| Von | Zu |
|-----|-----|
| `ß` | `ss` |
| `"..."` | `«...»` |
| `'...'` | `‹...›` |
| `1,000` | `1'000` |

### 3. Unicode-Handling (nur PDF)

Emojis und Sonderzeichen werden automatisch konvertiert:

| Unicode | Ersetzung |
|---------|-----------|
| ✅ | [OK] |
| ❌ | [X] |
| ⚠️ | [!] |
| − (U+2212) | - |
| « » | " " |

## Fehlerbehebung

### Diagnose-Tools

```bash
# Alle Learnings anzeigen
python scripts/format_report.py --learnings

# Abhängigkeiten prüfen
python scripts/format_report.py --check-deps

# Datei analysieren
python scripts/format_report.py --analyze input.md
```

### Häufige Probleme

| Problem | Lösung |
|---------|--------|
| `Unknown option 'ngerman'` | `apt-get install texlive-lang-german` |
| `Undefined control sequence. \tightlist` | Template bereits behoben |
| `Missing number, treated as zero` | `-f html` verwenden |
| `Unicode character not set up` | Automatisch konvertiert |
| `font cannot be found` | `apt-get install fonts-open-sans fonts-roboto` |

### Wann HTML statt PDF?

Das Script analysiert den Inhalt und empfiehlt automatisch das optimale Format:

- **Emojis/Icons** → HTML
- **Progress-Bars (█▓░)** → HTML
- **Komplexe Tabellen (>5 Spalten)** → HTML
- **Einfacher Text** → PDF

## Learning Loop

### Neues Problem dokumentieren

1. Öffne `data/report-formatter-learnings.yaml`
2. Füge neuen Eintrag hinzu:

```yaml
- id: "RPT-L-XXX"
  category: "KATEGORIE"  # LATEX, UNICODE, FONTS, DEPS, WORKFLOW
  title: "Kurze Beschreibung"
  problem: |
    Fehlermeldung
  root_cause: |
    Warum passiert das?
  solution: |
    Wie löst man es?
  prevention: |
    Wie verhindert man es?
  severity: "HIGH"  # HIGH, MEDIUM, LOW, INFO
  first_encountered: "2026-01-29"
  lesson_learned: |
    Was wurde daraus gelernt?
  resolution: |
    Wie wurde es permanent behoben?
  recurrence_probability: "X%"
```

3. Quick-Reference-Eintrag hinzufügen
4. Commit

## CI/CD Integration

### GitHub Actions

Push zu `outputs/sessions/**/*.md` triggert automatisch:
1. PDF-Generierung
2. Artifact-Upload
3. Commit der generierten PDFs

### Manueller Trigger

```bash
gh workflow run format-reports.yml \
  -f input_file="outputs/sessions/EBF-S-2026-01-29-POL-001/report.md" \
  -f output_format="pdf"
```

## Dateipfade

| Datei | Pfad |
|-------|------|
| Script | `scripts/format_report.py` |
| Learnings | `data/report-formatter-learnings.yaml` |
| LaTeX Template | `templates/fehradvice-report.latex` |
| Cover Template | `templates/fehradvice-cover.latex` |
| Back Template | `templates/fehradvice-back.latex` |
| CSS Template | `templates/fehradvice-report.css` |
| GitHub Action | `.github/workflows/format-reports.yml` |
| Slash Command | `.claude/commands/format-report.md` |
| Workflow Ordner | `workflows/format-report/` |
| Outputs | `workflows/format-report/outputs/` |
