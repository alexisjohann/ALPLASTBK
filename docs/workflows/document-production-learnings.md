---
title: "Document Production Learning Loop"
version: "1.0"
date: "2026-01-28"
author: "FehrAdvice & Partners AG"
last_updated_from: "SPÖ Projekt 2029"
---

# Document Production Learning Loop

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

| Datum | Projekt | Learning | Kategorie |
|:------|:--------|:---------|:----------|
| 2026-01-28 | SPÖ 2029 | Markdown > LaTeX für Reports | FORMAT |
| 2026-01-28 | SPÖ 2029 | Unicode vermeiden | ENCODING |
| 2026-01-28 | SPÖ 2029 | Tabellen max 10cm | LAYOUT |
| 2026-01-28 | SPÖ 2029 | colortbl immer einbinden | PACKAGES |
| 2026-01-28 | SPÖ 2029 | babel: german nicht ngerman | PACKAGES |

---

## Metriken

| Metrik | Vor Learning | Nach Learning | Ziel |
|:-------|:-------------|:--------------|:-----|
| Zeit bis erstes PDF | 90 min | 15 min | < 10 min |
| Kompilierungsfehler | 5+ | 0 | 0 |
| Iterationen | 8 | 2 | 1-2 |
| Kundenzufriedenheit | ? | ? | > 90% |

---

*Dokument wird nach jedem Projekt aktualisiert.*
*Nächstes Review: Nach nächstem Kundenprojekt*
