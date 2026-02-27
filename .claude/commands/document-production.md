---
name: document-production
description: Systematischer Workflow für Dokumentenproduktion mit Qualitäts-Gates
trigger: /doc
okb_id: OKB-001
okb_file: docs/okb/OKB-001-document-production.md
---

# Document Production Workflow (DPW)

**Ziel:** Jedes Dokument wird besser, nie schlechter.

> **OKB:** `OKB-001` | [docs/okb/OKB-001-document-production.md](../../docs/okb/OKB-001-document-production.md)

---

## ⚠️ LEARNINGS AUS OKB-001 (IMMER ZUERST LESEN!)

> **Quelle:** `docs/okb/OKB-001-document-production.md`
> **Letztes Update:** SPÖ Projekt 2029 (2026-01-28)

### Die 6 wichtigsten Erkenntnisse:

| # | Learning | Warum wichtig | Zeitersparnis |
|:--|:---------|:--------------|:--------------|
| L1 | **Markdown > LaTeX** für 90% der Dokumente | Weniger Fehler, schneller iterieren | 30+ min |
| L2 | **Unicode vermeiden** (λ→lambda, «→", →→->) | pandoc/LaTeX Kompilierungsfehler | 10+ min |
| L3 | **Tabellen max 10cm breit** | Overfull hbox Fehler | 15+ min |
| L4 | **YAML Frontmatter** immer vollständig | Konsistenz, Metadaten | 5 min |
| L5 | **colortbl Paket** bei LaTeX-Tabellen mit Farbe | \rowcolor undefined Fehler | 5 min |
| L6 | **babel: german** nicht ngerman | Kompilierungsfehler | 10 min |

### Quick-Check vor Start:

```
[ ] Dokumenttyp bestimmt? → Markdown oder LaTeX?
[ ] Wenn Markdown: Template mit YAML Frontmatter?
[ ] Wenn LaTeX: colortbl + babel korrekt?
[ ] Unicode-Zeichen vermeiden bewusst?
```

---

## PHASE 0: INITIALISIERUNG (2 min)

### Schritt 0.1: Dokumenttyp bestimmen

```
Welcher Dokumenttyp?

  1. BRIEFING     - Strategisches Kundenbriefing (wie SPÖ, UBS)
  2. REPORT       - Analysebericht, Studie
  3. PROPOSAL     - Angebot, Projektvorschlag
  4. APPENDIX     - EBF Framework Appendix (LaTeX)
  5. PAPER        - Wissenschaftliches Paper (LaTeX)
  6. MEMO         - Internes Memo, kurz
  7. PRESENTATION - PowerPoint/Slides

-> Eingabe: 1-7
```

### Schritt 0.2: Template laden

| Typ | Template | Format |
|:----|:---------|:-------|
| BRIEFING | `templates/briefing-template.md` | Markdown |
| REPORT | `templates/report-template.md` | Markdown |
| PROPOSAL | `templates/proposal-template.md` | Markdown |
| APPENDIX | `appendices/00_appendix_template.tex` | LaTeX |
| PAPER | `templates/paper-template.tex` | LaTeX |
| MEMO | `templates/memo-template.md` | Markdown |
| PRESENTATION | `templates/presentation-template.md` | Markdown |

### Schritt 0.3: Metadaten erfassen

```yaml
---
title: "[TITEL]"
subtitle: "[UNTERTITEL]"
author: "FehrAdvice & Partners AG"
date: "[MONAT JAHR]"
version: "0.1"
client: "[KUNDE]"
project: "[PROJEKT-ID]"
status: "DRAFT"
lang: de
---
```

**CHECKPOINT 0:** Template geladen, Metadaten ausgefüllt? -> Weiter

---

## PHASE 1: STRUKTUR (10 min)

### Schritt 1.1: Gliederung erstellen

```markdown
## 1. Executive Summary
## 2. [Hauptteil 1]
## 3. [Hauptteil 2]
## 4. [Hauptteil 3]
## 5. Übersichtstabellen
## Appendix
```

### Schritt 1.2: Kernaussagen definieren

Für JEDES Kapitel:
- Was ist die EINE Kernaussage?
- Welche Tabelle/Grafik unterstützt sie?

### Schritt 1.3: Qualitäts-Check Struktur

```
STRUKTUR-CHECKLISTE:
[ ] Max. 7 Hauptkapitel?
[ ] Jedes Kapitel hat klare Kernaussage?
[ ] Executive Summary an Position 1?
[ ] Appendix am Ende?
[ ] Logischer Fluss: Problem -> Analyse -> Lösung?
```

**CHECKPOINT 1:** Struktur-Checkliste 100%? -> Weiter

---

## PHASE 2: INHALT (variabel)

### Schritt 2.1: Kapitel schreiben

**PRO KAPITEL:**
1. Kernaussage als ersten Satz
2. Unterstützende Argumente (max. 3-5)
3. Tabelle oder Zitat als Evidenz
4. Überleitung zum nächsten Kapitel

### Schritt 2.2: Tabellen-Regeln

```markdown
| Spalte 1 | Spalte 2 | Spalte 3 |
|:---------|:---------|:---------|
| Wert     | Wert     | Wert     |
```

**TABELLEN-CHECKLISTE:**
- [ ] Max. 4 Spalten?
- [ ] Keine Zeile > 80 Zeichen?
- [ ] Header klar und kurz?
- [ ] Linksbündig `:---` für Text?

### Schritt 2.3: Zitate und Hervorhebungen

```markdown
> **Kernaussage als Blockquote**

*Kursiv für Betonung*

**Fett für Schlüsselbegriffe**
```

### Schritt 2.4: Qualitäts-Check Inhalt

```
INHALT-CHECKLISTE:
[ ] Jedes Kapitel < 2 Seiten?
[ ] Keine Wiederholungen?
[ ] Alle Behauptungen belegt?
[ ] Fachbegriffe erklärt?
[ ] Aktive Sprache (nicht Passiv)?
```

**CHECKPOINT 2:** Inhalt-Checkliste 100%? -> Weiter

---

## PHASE 3: FORMATIERUNG (5 min)

### Schritt 3.1: Unicode-Bereinigung

**AUTOMATISCH ausführen:**
```bash
# Unicode-Check
grep -P '[^\x00-\x7F]' dokument.md

# Kritische Zeichen ersetzen:
sed -i 's/«/"/g; s/»/"/g; s/–/--/g; s/—/---/g; s/→/->/g; s/←/<-/g; s/≈/=/g; s/λ/lambda/g' dokument.md
```

### Schritt 3.2: Seitenumbrüche

```markdown
\newpage   <- Nach jedem Hauptkapitel
```

### Schritt 3.3: Qualitäts-Check Format

```
FORMAT-CHECKLISTE:
[ ] Keine Unicode-Sonderzeichen?
[ ] \newpage nach jedem Hauptkapitel?
[ ] Konsistente Überschriften-Hierarchie?
[ ] Keine leeren Zeilen > 2?
[ ] Einheitliche Anführungszeichen (")?
```

**CHECKPOINT 3:** Format-Checkliste 100%? -> Weiter

---

## PHASE 4: KOMPILIERUNG (3 min)

### Schritt 4.1: Test-Kompilierung

```bash
# Markdown -> PDF
pandoc dokument.md -o dokument.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=2.5cm \
  -V fontsize=12pt \
  -V lang=de
```

### Schritt 4.2: Fehler-Behandlung

| Fehler | Ursache | Lösung |
|:-------|:--------|:-------|
| Unicode character not set up | Sonderzeichen | Phase 3.1 wiederholen |
| Overfull hbox | Tabelle zu breit | Spalten kürzen |
| Missing $ | Math-Modus | $ um Formeln |

### Schritt 4.3: Qualitäts-Check Kompilierung

```
KOMPILIERUNG-CHECKLISTE:
[ ] PDF erstellt ohne Fehler?
[ ] Keine Warnungen (ausser Overfull)?
[ ] Seitenzahlen korrekt?
[ ] Inhaltsverzeichnis korrekt?
```

**CHECKPOINT 4:** Kompilierung erfolgreich? -> Weiter

---

## PHASE 5: REVIEW (5 min)

### Schritt 5.1: Visueller Check

PDF öffnen und prüfen:
- [ ] Titelseite vollständig?
- [ ] Tabellen nicht abgeschnitten?
- [ ] Seitenumbrüche sinnvoll?
- [ ] Keine verwaisten Überschriften?

### Schritt 5.2: Inhaltlicher Check

- [ ] Executive Summary fasst alles zusammen?
- [ ] Kernaussagen klar erkennbar?
- [ ] Empfehlungen actionable?

### Schritt 5.3: Kundenbrille

**Frage dich:**
- Versteht der Kunde das in 5 Minuten?
- Kann er morgen damit arbeiten?
- Fehlt etwas Wichtiges?

**CHECKPOINT 5:** Review bestanden? -> Weiter

---

## PHASE 6: FINALISIERUNG (2 min)

### Schritt 6.1: Version hochsetzen

```yaml
version: "0.1" -> "1.0"
status: "DRAFT" -> "FINAL"
```

### Schritt 6.2: Dateien speichern

```bash
# Quell-Datei
data/customers/[kunde]/[projekt].md

# PDF in outputs
outputs/[KUNDE]_[Projekt]_v[VERSION].pdf
```

### Schritt 6.3: Git Commit

```bash
git add data/customers/[kunde]/ outputs/
git commit -m "feat([KUNDE]): [Projekt] v[VERSION] - [Beschreibung]"
```

### Schritt 6.4: Learning erfassen (PFLICHT!)

```
Neues Learning entdeckt?

[ ] JA -> docs/okb/OKB-001-document-production.md aktualisieren:

    1. Session-Log ergänzen (was ging schief?)
    2. Lessons Learned Registry erweitern
    3. Metriken aktualisieren

[ ] NEIN -> Weiter
```

**Learning-Eintrag Format:**

```markdown
| Datum | Projekt | Learning | Kategorie |
|:------|:--------|:---------|:----------|
| YYYY-MM-DD | [PROJEKT] | [WAS GELERNT] | FORMAT/ENCODING/LAYOUT/PACKAGES |
```

**CHECKPOINT 6:** Committed, gepusht UND Learnings dokumentiert? -> FERTIG

---

## QUALITÄTS-MATRIX

| Phase | Checkpoint | Blocker? | Rücksprung zu |
|:------|:-----------|:---------|:--------------|
| 0 | Template geladen | Ja | - |
| 1 | Struktur ok | Ja | Phase 1 |
| 2 | Inhalt ok | Ja | Phase 2 |
| 3 | Format ok | Ja | Phase 3 |
| 4 | Kompiliert | Ja | Phase 3 oder 2 |
| 5 | Review ok | Nein | Phase 2 oder 3 |
| 6 | Committed | Nein | - |

---

## ANTI-PATTERNS (Was NIE tun)

| Anti-Pattern | Warum schlecht | Stattdessen | Learning |
|:-------------|:---------------|:------------|:---------|
| Direkt in LaTeX starten | Komplexität, Fehler | Markdown zuerst | L1 |
| Unicode-Zeichen nutzen | Kompilierungsfehler | ASCII-Alternativen | L2 |
| Tabellen > 10cm breit | Overfull hbox | Spalten kürzen | L3 |
| Ohne Template starten | Inkonsistenz | Template laden | L4 |
| LaTeX ohne colortbl | \rowcolor undefined | Paket einbinden | L5 |
| babel mit ngerman | Kompilierungsfehler | german verwenden | L6 |
| Review überspringen | Fehler beim Kunden | Immer Phase 5 | - |
| Version nicht hochsetzen | Versionschaos | Immer hochsetzen | - |
| **Learnings ignorieren** | Gleiche Fehler wiederholen | Sektion oben lesen! | - |

---

## ITERATION: Dokument verbessern

Wenn ein bestehendes Dokument verbessert wird:

### Regel 1: Nie rückwärts

```
Version 1.0 -> 1.1 -> 1.2 (nie zurück zu 1.0)
```

### Regel 2: Änderungen minimal

```
WENN kleine Änderung (Typo, Formatierung)
DANN nur Phase 3-6

WENN inhaltliche Änderung
DANN Phase 2-6

WENN strukturelle Änderung
DANN Phase 1-6
```

### Regel 3: Backup vor Änderung

```bash
cp dokument.md dokument_backup_$(date +%Y%m%d).md
```

### Regel 4: Diff dokumentieren

```bash
git diff dokument.md  # Vor commit prüfen
```

---

## METRIKEN

Nach jedem Projekt aktualisieren:

```yaml
# In docs/okb/OKB-001-document-production.md
- projekt: "[PROJEKT]"
  datum: "[DATUM]"
  zeit_total: "[MINUTEN]"
  fehler_kompilierung: [ANZAHL]
  iterationen: [ANZAHL]
  checkpoint_fails: [LISTE]
  learning: "[WAS GELERNT]"
```

---

## LEARNING LOOP (Kontinuierliche Verbesserung)

```
+------------------+
|  NEUES PROJEKT   |
+--------+---------+
         |
         v
+------------------+
|  LEARNINGS LESEN |<----+
|  (Sektion oben)  |     |
+--------+---------+     |
         |               |
         v               |
+------------------+     |
|  PHASE 0-5       |     |
|  (Workflow)      |     |
+--------+---------+     |
         |               |
         v               |
+------------------+     |
|  PHASE 6.4       |     |
|  Learning        |     |
|  erfassen        |-----+
+--------+---------+
         |
         v
+------------------+
|  document-       |
|  production-     |
|  learnings.md    |
|  aktualisiert    |
+------------------+
```

**Learnings-Datenbank:** `docs/okb/OKB-001-document-production.md`

---

## QUICK REFERENCE

```
/doc -> Workflow starten

ZUERST: Learnings-Sektion lesen! (L1-L6)

Phase 0: Template + Metadaten (2 min)
Phase 1: Struktur + Gliederung (10 min)
Phase 2: Inhalt schreiben (variabel)
Phase 3: Format bereinigen (5 min)
Phase 4: Kompilieren (3 min)
Phase 5: Review (5 min)
Phase 6: Finalisieren + Learning erfassen (5 min)

TOTAL: ~35 min + Schreibzeit
```
