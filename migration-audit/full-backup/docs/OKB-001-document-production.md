---
title: "OKB-001: Document Production"
okb_id: "OKB-001"
version: "1.0"
date: "2026-01-28"
author: "FehrAdvice & Partners AG"
last_updated_from: "SPÖ Projekt 2029"
workflow: "/doc"
workflow_file: ".claude/commands/document-production.md"
---

# OKB-001: Document Production

> **Operational Knowledge Base** fur Dokumentenproduktion

| Metrik | Wert |
|:-------|:-----|
| Learnings | 7 (L1-L7) |
| Zeitersparnis | 95+ min/Projekt |
| Workflow | `/doc` |

**Ziel:** Aus jedem Dokumentenprojekt lernen, um die Qualität kontinuierlich zu verbessern.

---

## Session: SPÖ Projekt 2029 (2026-01-28)

### Was ging schief?

| Problem | Ursache | Zeitverlust |
|:--------|:--------|:------------|
| LaTeX kompiliert nicht | `ngerman` statt `german` in babel | 10 min |
| `\rowcolor` undefined | `colortbl` Paket fehlte | 5 min |
| Tabellen zu breit | Spaltenbreiten > 10cm | 15 min |
| Unicode-Fehler in pandoc | λ, ≈, →, «, », ─ Zeichen | 10 min |
| Komplexes LaTeX-Layout | Versuch, Referenz-PDF exakt zu kopieren | 30 min |

**Total Zeitverlust:** ~70 Minuten

### Was haben wir gelernt?

#### 1. FORMAT-WAHL: Markdown > LaTeX (für 90% der Dokumente)

```
WENN Dokument = {Report, Briefing, Analyse, Proposal}
DANN verwende Markdown + YAML Frontmatter
     → Einfacher zu schreiben
     → Weniger Fehlerquellen
     → Schneller zu iterieren

WENN Dokument = {Paper für Journal, Appendix für EBF, komplexe Formeln}
DANN verwende LaTeX
     → Mehr Kontrolle
     → Bessere Typografie
     → Formel-Support
```

#### 2. TEMPLATE-STRUKTUR: Immer YAML Frontmatter

```yaml
---
title: "Titel"
subtitle: "Untertitel"
author: "FehrAdvice & Partners AG"
date: "Monat Jahr"
version: "1.0"
client: "Kunde"
lang: de
toc: true
toc-depth: 2
documentclass: report
papersize: a4
fontsize: 12pt
geometry: margin=2.5cm
---
```

#### 3. UNICODE VERMEIDEN: ASCII-kompatible Alternativen

| Vermeiden | Verwenden | Grund |
|:----------|:----------|:------|
| λ | lambda | LaTeX Unicode-Fehler |
| ≈ | = oder ca. | LaTeX Unicode-Fehler |
| ≠ | != | LaTeX Unicode-Fehler |
| → | -> | LaTeX Unicode-Fehler |
| « » | " " | Kompilierungsprobleme |
| ‹ › | ' ' | Kompilierungsprobleme |
| – | -- | Konsistenz |
| — | --- | Konsistenz |
| ─│┌┐└┘ | ASCII art mit -\|+  | pandoc/LaTeX Fehler |

#### 4. TABELLEN: Einfach halten

**Markdown-Tabellen (bevorzugt):**
```markdown
| Spalte 1 | Spalte 2 | Spalte 3 |
|:---------|:---------|:---------|
| Wert 1   | Wert 2   | Wert 3   |
```

**LaTeX-Tabellen (wenn nötig):**
- Max. Gesamtbreite: 10-11cm für A4 mit 2.5cm Margins
- Keine `\columncolor` in erster Spalte wenn möglich
- `colortbl` Paket IMMER einbinden

#### 5. KONVERTIERUNG: pandoc Workflow

```bash
# Standard-Konvertierung
pandoc input.md -o output.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=2.5cm \
  -V fontsize=12pt \
  -V lang=de

# Mit Inhaltsverzeichnis
pandoc input.md -o output.pdf \
  --pdf-engine=pdflatex \
  --toc \
  -V geometry:margin=2.5cm
```

#### 6. QUALITÄTSPRÜFUNG: Vor Abgabe

- [ ] Alle Tabellen < 10cm breit?
- [ ] Keine Unicode-Sonderzeichen?
- [ ] YAML Frontmatter vollständig?
- [ ] `\newpage` an richtigen Stellen?
- [ ] pandoc kompiliert fehlerfrei?

#### 7. PDF-FORMATIERUNG: 10 automatische Regeln (beim Schreiben anwenden!)

> **Prinzip:** Diese Regeln werden BEIM SCHREIBEN angewendet, nicht nachträglich geprüft.
> Zeitersparnis: ~20 min/Dokument (kein iteratives PDF-Debugging)

**R1: ÜBERSCHRIFTEN - Nie am Seitenende isoliert**
```
REGEL: Nach jeder ## oder ### Überschrift MUSS mindestens
       3 Zeilen Inhalt folgen bevor \newpage kommt

AUTOMATISCH: Vor ## in der Nähe von \newpage prüfen
```

**R2: WITWEN - Keine Einzelzeilen am Seitenanfang**
```
REGEL: YAML-Header erweitern mit:
       header-includes:
         - \widowpenalty=10000
         - \clubpenalty=10000

AUTOMATISCH: Durch LaTeX-Einstellung verhindert
```

**R3: TABELLEN - Max 8 Zeilen ohne Pagebreak**
```
REGEL: Tabelle > 8 Zeilen → \newpage DAVOR setzen
       ODER Tabelle in 2 Teile aufteilen

BEISPIEL:
\newpage

| Spalte 1 | Spalte 2 |
|:---------|:---------|
| ... (max 8 Zeilen) |
```

**R4: CODE-BLÖCKE - Max 15 Zeilen ohne Pagebreak**
```
REGEL: Code-Block > 15 Zeilen → \newpage DAVOR setzen
       ODER Block in logische Teile aufteilen

BEISPIEL:
**Phase 1:**

\newpage

```
PHASE 1 Code hier...
```
```

**R5: BLOCKQUOTES - Max 6 Zeilen**
```
REGEL: Blockquote > 6 Zeilen → Aufteilen in mehrere Quotes
       ODER als normalen Text formatieren

SCHLECHT:
> Sehr langer Text über 6 Zeilen der
> wahrscheinlich über die Seite umbricht
> und unschön aussieht...

GUT:
> Kurzes Zitat (max 6 Zeilen)

Dann normaler Text für den Rest.
```

**R6: LISTEN - Max 10 Items ohne Unterbrechung**
```
REGEL: Liste > 10 Items → Gruppieren mit Zwischenüberschriften

SCHLECHT:
1. Item 1
2. Item 2
...
15. Item 15

GUT:
**Gruppe A:**
1. Item 1
2. Item 2

**Gruppe B:**
3. Item 3
...
```

**R7: BILDER - Explizite Breite setzen**
```
REGEL: IMMER Breite angeben, nie floating lassen

SCHLECHT:
![Bild](pfad.png)

GUT:
![Bild](pfad.png){width=80%}
```

**R8: TOC - Immer 2x kompilieren**
```
REGEL: Bei toc: true IMMER latexmk verwenden
       ODER manuell 2x pdflatex ausführen

BEFEHL:
latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" dokument.tex
```

**R9: SILBENTRENNUNG - Fachbegriffe definieren**
```
REGEL: Bei deutschen Dokumenten YAML erweitern:

header-includes:
  - \usepackage[ngerman]{babel}
  - \hyphenation{Fach-be-griff Kom-po-si-tum Ver-hal-tens-öko-no-mie}
```

**R10: ZEILENBREITE - Max 65 Zeichen für ASCII-Art**
```
REGEL: ASCII-Boxen und Code max 65 Zeichen breit
       (A4 mit 2.5cm Margin bei 12pt = ~70 Zeichen)

SCHLECHT (70+ Zeichen):
+----------------------------------------------------------------------+
|  Text hier                                                           |
+----------------------------------------------------------------------+

GUT (max 65 Zeichen):
+---------------------------------------------------------------+
|  Text hier                                                    |
+---------------------------------------------------------------+
```

**Kompletter YAML-Header mit allen R-Regeln:**

```yaml
---
title: "Titel"
subtitle: "Untertitel"
author: "FehrAdvice & Partners AG"
date: "Monat Jahr"
lang: de
toc: true
toc-depth: 2
documentclass: report
papersize: a4
fontsize: 12pt
geometry: margin=2.5cm
header-includes:
  - \usepackage[ngerman]{babel}
  - \widowpenalty=10000
  - \clubpenalty=10000
  - \raggedbottom
  - \hyphenation{Spal-tungs-bou-le-vard Ver-hal-tens-öko-no-mie}
---
```

---

## Dokumenttyp-Matrix

| Dokumenttyp | Format | Template | Kompilierung |
|:------------|:-------|:---------|:-------------|
| Strategiebriefing | Markdown | UBS-Template | pandoc |
| Kundenreport | Markdown | UBS-Template | pandoc |
| Projektbriefing | Markdown | UBS-Template | pandoc |
| Präsentation | PowerPoint | FA-PPT-Template | direkt |
| EBF Appendix | LaTeX | appendix_template.tex | pdflatex |
| Journal Paper | LaTeX | journal-specific | pdflatex |
| Technische Doku | Markdown | Standard | pandoc |

---

## Checkliste: Neues Dokument erstellen

### Phase 1: Setup (2 min)
- [ ] Dokumenttyp bestimmen (siehe Matrix)
- [ ] Template kopieren
- [ ] YAML Frontmatter ausfüllen

### Phase 2: Inhalt (variabel)
- [ ] Struktur mit ## Überschriften
- [ ] Tabellen in Markdown
- [ ] Zitate mit > blockquote
- [ ] Listen mit - oder 1.

### Phase 3: Review (5 min)
- [ ] Unicode-Check: `grep -P '[^\x00-\x7F]' datei.md`
- [ ] Tabellen-Check: Keine Zeile > 80 Zeichen
- [ ] Kompilierung testen

### Phase 4: Finalisierung (3 min)
- [ ] PDF generieren
- [ ] Visuelle Prüfung
- [ ] In outputs/ kopieren
- [ ] Git commit

---

## Lessons Learned Registry

| ID | Datum | Projekt | Learning | Kategorie | Zeitersparnis |
|:---|:------|:--------|:---------|:----------|:--------------|
| L1 | 2026-01-28 | SPÖ 2029 | Markdown > LaTeX für Reports | FORMAT | 30 min |
| L2 | 2026-01-28 | SPÖ 2029 | Unicode vermeiden | ENCODING | 10 min |
| L3 | 2026-01-28 | SPÖ 2029 | Tabellen max 10cm | LAYOUT | 15 min |
| L4 | 2026-01-28 | SPÖ 2029 | colortbl immer einbinden | PACKAGES | 5 min |
| L5 | 2026-01-28 | SPÖ 2029 | babel: german nicht ngerman | PACKAGES | 10 min |
| L6 | 2026-01-28 | SPÖ 2029 | Qualitätsprüfung vor Abgabe | PROCESS | 5 min |
| **L7** | **2026-01-28** | **SPÖ 2029** | **10 PDF-Formatierungsregeln (R1-R10)** | **PDF** | **20 min** |

---

## Metriken

| Metrik | Vor L1-L6 | Nach L1-L6 | Nach L7 | Ziel |
|:-------|:----------|:-----------|:--------|:-----|
| Zeit bis erstes PDF | 90 min | 15 min | **10 min** | < 10 min |
| Kompilierungsfehler | 5+ | 1-2 | **0** | 0 |
| PDF-Layout-Iterationen | 8 | 4 | **1-2** | 1-2 |
| Seitenumbruch-Probleme | 10+ | 5 | **0** | 0 |

**Gesamte Zeitersparnis durch L1-L7: 95+ min/Projekt**

---

## Quick Reference: Die 10 R-Regeln

| R# | Regel | Grenzwert | Aktion |
|:---|:------|:----------|:-------|
| R1 | Überschriften | min 3 Zeilen nach ## | Nicht isolieren |
| R2 | Witwen/Waisen | - | YAML: widowpenalty=10000 |
| R3 | Tabellen | max 8 Zeilen | \newpage davor |
| R4 | Code-Blöcke | max 15 Zeilen | \newpage davor |
| R5 | Blockquotes | max 6 Zeilen | Aufteilen |
| R6 | Listen | max 10 Items | Gruppieren |
| R7 | Bilder | - | width=80% setzen |
| R8 | TOC | - | 2x kompilieren |
| R9 | Silbentrennung | - | \hyphenation{} |
| R10 | ASCII-Art | max 65 Zeichen | Breite reduzieren |

---

*Dokument wird nach jedem Projekt aktualisiert.*
*Letztes Update: 2026-01-28 (L7: PDF-Formatierungsregeln)*
*Nächstes Review: Nach nächstem Kundenprojekt*
