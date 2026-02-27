# FehrAdvice Report Formatter Workflow

> Automatisierte Konvertierung von Markdown-Reports zu voll formatierten FehrAdvice-Dokumenten.

## Ordnerstruktur

```
workflows/format-report/
├── README.md                    # Diese Dokumentation
├── learnings.yaml              # → Symlink zu data/report-formatter-learnings.yaml
├── outputs/                     # Generierte Reports (PDF, HTML, PPTX, DOCX)
├── templates/                   # → Symlinks zu templates/
│   ├── fehradvice-report.latex  # Haupt-Report-Template
│   ├── fehradvice-report.css    # CSS für HTML-Output
│   ├── fehradvice-cover.latex   # Cover-Page Template mit TikZ
│   └── fehradvice-back.latex    # Back-Page Template (Kontakt, Disclaimer)
└── docs/
    └── workflow-guide.md        # Detaillierte Workflow-Dokumentation
```

## Quick Start

```bash
# 1. Markdown-Report formatieren → PDF
python scripts/format_report.py input.md

# 2. PDF mit FehrAdvice Cover-Page (empfohlen für Kundenreports)
python scripts/format_report.py input.md --cover

# 3. PDF mit Cover + Back-Page (vollständiges Kundendokument)
python scripts/format_report.py input.md --cover --back

# 4. HTML-Output (für komplexe Dokumente mit Emojis/Tabellen)
python scripts/format_report.py input.md -f html

# 5. PDF via WeasyPrint mit Cover + Back (für Emojis + vollständig)
python scripts/format_report.py input.md --engine weasyprint --cover --back

# 6. PowerPoint-Output
python scripts/format_report.py input.md -f pptx

# 7. Abhängigkeiten prüfen
python scripts/format_report.py --check-deps

# 8. Learnings anzeigen
python scripts/format_report.py --learnings
```

## Slash Command

```
/format-report                              # Interaktiv
/format-report <datei.md>                   # Spezifische Datei → PDF
/format-report <datei.md> --format html     # HTML-Output
/format-report --session EBF-S-2026-01-29-POL-001  # Session-Report
```

## Learnings-Datenbank

Die Learnings-Datenbank dokumentiert alle bekannten Probleme und deren Lösungen:

| ID | Kategorie | Problem | Wiederauftretens-Wkt |
|----|-----------|---------|---------------------|
| RPT-L-001 | LATEX | Babel ngerman | 5% |
| RPT-L-002 | LATEX | tightlist undefined | 0% |
| RPT-L-003 | LATEX | longtable errors | 15% |
| RPT-L-004 | UNICODE | Emojis | 2% |
| RPT-L-005 | UNICODE | Minus-Zeichen | 3% |
| RPT-L-006 | UNICODE | Guillemets | 0% |
| RPT-L-007 | FONTS | Open Sans/Roboto | 5% |
| RPT-L-008 | DEPS | Pandoc fehlt | 0% |
| RPT-L-009 | DEPS | texlive Pakete | 0% |
| RPT-L-010 | WORKFLOW | HTML-Alternative | 0% |
| RPT-L-011 | WORKFLOW | Font-Generierung | 10% |

**Details:** `learnings.yaml` oder `data/report-formatter-learnings.yaml`

## Format-Empfehlungen

| Dokumenttyp | Format | Grund |
|-------------|--------|-------|
| Einfacher Text-Report | PDF | Saubere Typografie |
| Report mit Emojis/Icons | HTML | Volle Unicode-Unterstützung |
| Report mit Progress-Bars | HTML | CSS kann Progress-Bars rendern |
| Komplexe Tabellen | HTML | Flexiblere Darstellung |
| Präsentation | PPTX | Direkt editierbar |
| Zur Weiterbearbeitung | DOCX | Word-kompatibel |

## Dateien

| Datei | Pfad | Beschreibung |
|-------|------|--------------|
| **Script** | `scripts/format_report.py` | Haupt-Konvertierungsscript |
| **Learnings** | `data/report-formatter-learnings.yaml` | Learnings-Datenbank |
| **LaTeX Template** | `templates/fehradvice-report.latex` | PDF-Template |
| **CSS Template** | `templates/fehradvice-report.css` | HTML-Stylesheet |
| **GitHub Action** | `.github/workflows/format-reports.yml` | CI/CD Workflow |
| **Slash Command** | `.claude/commands/format-report.md` | Skill-Dokumentation |

## GitHub

- **Branch:** `claude/explain-ebf-capabilities-E5Vlg`
- **Workflow:** Push zu `outputs/sessions/**/*.md` triggert automatische PDF-Generierung

## Verwandte Ressourcen

- **Style Guide:** `appendices/REF-STYLE_SG_corporate_style_guide.tex`
- **Session Outputs:** `outputs/sessions/`
- **OKB Document Production:** `docs/okb/OKB-001-document-production.md`
