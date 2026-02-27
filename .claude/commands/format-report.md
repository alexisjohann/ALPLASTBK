# /format-report - FehrAdvice Report Formatter

## Beschreibung

Konvertiert Markdown-Reports in voll formatierte FehrAdvice-Dokumente mit Corporate Design.

## SSOT

- **Style Guide:** `appendices/REF-STYLE_SG_corporate_style_guide.tex`
- **YAML-Konfiguration:** `templates/pptx/fa-style.yaml`
- **LaTeX-Template:** `templates/fehradvice-report.latex`
- **CSS-Template:** `templates/fehradvice-report.css`
- **PPTX-Template:** `templates/pptx/FehrAdvice-Master.pptx`

## Verwendung

```
/format-report                              # Interaktiv
/format-report <datei.md>                   # PDF mit Cover + Back (Standard)
/format-report <datei.md> --format html     # HTML-Output
/format-report <datei.md> --format pptx     # PowerPoint-Output
/format-report <datei.md> --format docx     # Word-Output mit Cover + Back
/format-report <datei.md> --no-cover        # PDF ohne Cover-Page
/format-report <datei.md> --no-back         # PDF ohne Back-Page
/format-report --batch <verzeichnis>        # Alle MDs im Verzeichnis
/format-report --session EBF-S-2026-01-29-POL-001  # Session-Report formatieren
```

## Standard-Verhalten (ab v1.4)

**Cover und Back sind standardmässig AKTIVIERT** für alle PDF- und DOCX-Outputs.

Das FehrAdvice Corporate Design wird automatisch angewandt:
- **Cover Page:** Weisser Header mit Logo rechts, dunkelblauer Hauptbereich
- **Back Sheet:** Hellgrauer Hintergrund, dünner blauer Balken oben (1cm), breiter blauer Balken unten (4cm), Kontaktinfos, bilingualer Disclaimer

**Back Sheet Template:** `templates/fehradvice-back.latex` (SSOT)

Um Cover/Back zu deaktivieren: `--no-cover` und/oder `--no-back`

### Metadaten-Handling (WICHTIG)

**Metadaten sind NICHT sichtbar im finalen Dokument!**

- **Markdown:** Metadaten gehören in YAML-Frontmatter (zwischen `---`)
- **LaTeX:** Metadaten gehören in Kommentare im Header (`%% - Lead-ID: ...`)
- **PDF/DOCX:** Keine sichtbaren Metadaten-Boxen am Anfang oder Ende

**VERBOTEN:**
- ❌ Sichtbare Metadaten-Box am Dokumentanfang
- ❌ Sichtbare Metadaten-Box am Dokumentende
- ❌ "Dokument-Metadaten:" als sichtbarer Abschnitt

**KORREKT:**
- ✅ YAML-Frontmatter in Markdown
- ✅ LaTeX-Kommentare im Header
- ✅ PDF-Metadaten (unsichtbar, aber durchsuchbar)

## Output-Formate

| Format | Engine | Beschreibung |
|--------|--------|--------------|
| **pdf** | LaTeX (XeTeX) | Höchste Qualität, perfekte Typografie |
| **pdf** | WeasyPrint | Schneller, CSS-basiert |
| **html** | Pandoc | Standalone HTML mit eingebettetem CSS |
| **pptx** | Pandoc | PowerPoint mit FehrAdvice-Master-Template |
| **docx** | Pandoc | Word mit Reference-Doc-Styling |

## Automatisch angewandte Features

### 1. FehrAdvice Corporate Design

- **Primärfarben:**
  - Dunkelblau `#024079` → Headlines, Links
  - Hellblau `#549EDE` → Sekundärelemente
  - Dunkelgrau `#25212A` → Fliesstext
  - Hellgrau `#F3F5F7` → Hintergründe

- **Typografie:**
  - Roboto Bold → H1, H2
  - Open Sans → Body Text
  - Playfair Display → Akzente, Zitate

### 2. Schweizer Orthographie

Automatisch angewandt:
- `ß` → `ss`
- `"..."` → `«...»`
- `'...'` → `‹...›`
- Zahlen: `1,000` → `1'000`

### 3. Strukturelemente

Automatisch erkannt und formatiert:
- **Executive Summary** Box
- **Highlight** Box
- **Warning** Box
- **Recommendation** Box
- Tabellen mit FehrAdvice-Styling (siehe unten)

### 4. Tabellen-Styling (FehrAdvice Corporate Design)

Alle Tabellen werden automatisch mit dem FehrAdvice Corporate Design formatiert:

**Zeilenhöhe:**
- Erhöhte Zeilenhöhe (`\arraystretch{1.4}`) für bessere Lesbarkeit

**Kopfzeile:**
- Dunkelblauer Hintergrund (`#024079`)
- **Weisse, fette Schrift** in ALLEN Spalten

**Datenzeilen:**
- Alternierende Farben (weiss / hellgrau)
- **Erste Spalte** (Label): Schwarz + fett für gute Lesbarkeit
- Übrige Spalten: Normale schwarze Schrift

**Spaltentypen (für LaTeX-Outputs):**
| Typ | Verwendung | Formatierung |
|-----|------------|--------------|
| `H` | Header-Spalte (links) | Weiss + fett |
| `C` | Header-Spalte (zentriert) | Weiss + fett |
| `F` | Erste Spalte (Daten, links) | Schwarz + fett |
| `G` | Erste Spalte (Daten, zentriert) | Schwarz + fett |

**Beispiel LaTeX-Tabelle:**
```latex
\begin{tabularx}{\textwidth}{F l X}
\tableheadercolor
\textbf{\color{white}Name} & \textbf{\color{white}Rolle} & \textbf{\color{white}Verantwortung} \\
\tablerowodd
Andrea Becker & HR Director & Strategische HR-Führung \\
\tableroweven
Max Muster & CTO & Technische Leitung \\
\end{tabularx}
```

### 5. Metadaten-Extraktion (YAML-Frontmatter)

**PFLICHT:** Alle Metadaten im YAML-Frontmatter (nicht sichtbar im Output):
```yaml
---
title: "Strategisches Dossier"
subtitle: "Fiskalische Disziplin in der Schweiz"
doctype: "Strategisches Dossier"
client: "Kundenname"
date: "29. Januar 2026"
version: "1.0"
lead-id: "LEAD-XXX"
customer-registry: "CUS-XXX"
session-id: "EBF-S-2026-01-29-POL-001"
status: "QUALIFIED → PROPOSAL"
---
```

Diese Metadaten werden:
- In PDF-Metadaten eingebettet (durchsuchbar, aber nicht sichtbar)
- Für Cover-Page-Generierung verwendet
- In LaTeX als Kommentare übertragen

### 6. Back Sheet (FehrAdvice Corporate)

**Template:** `templates/fehradvice-back.latex`

**Design-Elemente:**
- Hellgrauer Hintergrund (`#F5F5F5`)
- Oberer blauer Balken: 1cm Höhe
- Unterer blauer Balken: 4cm Höhe
- FehrAdvice Logo (zentriert)
- Firmenname + Tagline
- Kontaktdaten (Adresse, E-Mail, Telefon, Website)
- Bilingualer Disclaimer (DE/EN)
- Copyright-Zeile im unteren Balken

**Automatisch eingefügt bei:**
- PDF-Output (Standard)
- DOCX-Output (Standard)

**Deaktivieren:** `--no-back`

## Workflow-Integration

### Mit EBF-Sessions

Nach Abschluss einer EBF-Session (Schritt 7):
```
1. Session-Report in outputs/sessions/{SESSION_ID}/ gespeichert
2. /format-report --session {SESSION_ID}
3. → PDF/PPTX/DOCX mit vollständigem Corporate Design
```

### Mit GitHub Actions

Push zu `outputs/sessions/**/*.md` triggert automatisch:
1. PDF-Generierung
2. Artifact-Upload
3. Commit der generierten PDFs

### Manueller GitHub Workflow

```
gh workflow run format-reports.yml \
  -f input_file="outputs/sessions/EBF-S-2026-01-29-POL-001/F5_strategisches_dossier_v1.md" \
  -f output_format="pdf"
```

## Beispiel-Output-Struktur

```
outputs/sessions/EBF-S-2026-01-29-POL-001/
├── F5_strategisches_dossier_v1.md      # Original Markdown
├── F5_strategisches_dossier_v1.pdf     # Formatierte PDF ← NEU
├── F5_strategisches_dossier_v1.html    # HTML-Version (optional)
└── F5_strategisches_dossier_v1.pptx    # PowerPoint (optional)
```

## Implementierung

Wenn der User `/format-report` aufruft:

1. **Interaktiv (ohne Parameter):**
   ```
   Welche Datei formatieren?

   Letzte Session-Reports:
   1. EBF-S-2026-01-29-POL-001/F5_strategisches_dossier_v1.md
   2. [andere Sessions...]

   → Eingabe: 1 oder Dateipfad

   Welches Format?
   📄 PDF (LaTeX)  ← [DEFAULT]
   🌐 HTML
   📊 PPTX
   📝 DOCX

   → Enter = PDF
   ```

2. **Mit Parameter:**
   ```bash
   python scripts/format_report.py <datei> -f <format>
   ```

3. **Ergebnis zeigen:**
   ```
   ✅ Report formatiert!

   📄 Output: outputs/sessions/EBF-S-2026-01-29-POL-001/F5_strategisches_dossier_v1.pdf

   Features angewandt:
   - FehrAdvice Corporate Design ✓
   - Schweizer Orthographie ✓
   - Titelseite mit Logo ✓
   - Inhaltsverzeichnis ✓
   - Methodik-Abschnitt ✓
   - Kontakt-Footer ✓
   ```

## Fehlerbehebung

### Schnelle Diagnose

```bash
# Alle Learnings anzeigen
python scripts/format_report.py --learnings

# Abhängigkeiten prüfen
python scripts/format_report.py --check-deps

# Datei vor Konvertierung analysieren
python scripts/format_report.py --analyze input.md
```

### Learnings-Datenbank

Alle bekannten Probleme und Lösungen sind dokumentiert in:
```
data/report-formatter-learnings.yaml
```

Das Script konsultiert diese Datenbank automatisch bei Fehlern und zeigt:
- Bekanntes Problem (ID)
- Schnelle Lösung
- Verweis auf detaillierte Dokumentation

### Häufige Fehler (Quick Reference)

| Fehler | Lösung | Learning-ID |
|--------|--------|-------------|
| `Unknown option 'ngerman'` | `apt-get install texlive-lang-german` | RPT-L-001 |
| `Undefined control sequence. \tightlist` | Template bereits behoben | RPT-L-002 |
| `Missing number, treated as zero` | HTML-Output verwenden: `-f html` | RPT-L-003 |
| `Unicode character (emoji) not set up` | Automatisch konvertiert | RPT-L-004 |
| `Unicode character − (U+2212)` | Automatisch konvertiert | RPT-L-005 |
| `font cannot be found` | `apt-get install fonts-open-sans fonts-roboto` | RPT-L-007 |
| `Pandoc nicht installiert` | `apt-get install pandoc` | RPT-L-008 |

### Format-Empfehlungen

Das Script analysiert den Inhalt und empfiehlt das optimale Format:

| Dokumenttyp | Empfohlenes Format | Grund |
|-------------|-------------------|-------|
| Einfacher Text-Report | PDF | Saubere Typografie |
| Report mit Emojis/Icons | HTML | Volle Unicode-Unterstützung |
| Report mit Progress-Bars | HTML | CSS kann Progress-Bars rendern |
| Komplexe Tabellen | HTML | Flexiblere Darstellung |
| Präsentation | PPTX | Direkt editierbar |
| Zur Weiterbearbeitung | DOCX | Word-kompatibel |

### Neues Learning hinzufügen

Wenn ein neuer Fehler auftritt:

1. Öffne `data/report-formatter-learnings.yaml`
2. Füge einen neuen Eintrag unter `learnings:` hinzu:
```yaml
- id: "RPT-L-XXX"
  category: "KATEGORIE"
  title: "Kurze Beschreibung"
  problem: |
    Fehlermeldung
  root_cause: |
    Warum passiert das?
  solution: |
    Wie löst man es?
  prevention: |
    Wie verhindert man es?
  severity: "HIGH/MEDIUM/LOW/INFO"
  first_encountered: "YYYY-MM-DD"
```
3. Füge einen Quick-Reference-Eintrag hinzu
4. Committe die Änderung

## Verwandte Skills

- `/compile` - LaTeX-Kompilierung
- `/convert` - Format-Konvertierung
- `/board-presentation` - Board-ready Präsentationen
- `/doc` - Document Production Workflow
