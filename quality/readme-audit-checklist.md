# README Detailed Audit Checklist

> **Systematische Checkliste für umfassende README-Prüfungen**

**Version:** 1.0 | **Type:** Quality Assurance | **Last Updated:** 2026-01-20

---

## 🎯 Zweck

Diese Checkliste dient als:
1. **Operatives Werkzeug** - Schritt-für-Schritt Audit durchführen
2. **Trainingsdokument** - Neue Auditor:innen einarbeiten
3. **Beweiswerkzeug** - Nachweisen, dass vollständig geprüft wurde
4. **Lernwerkzeug** - Erkannte Fehler dokumentieren

---

## 📋 PHASE 1: VORBEREITUNG (< 5 min)

### 1.1 Environment Setup

```
☐ Clone neueste Version: git pull origin main
☐ Alle README-Dateien lokal verfügbar
☐ Tools verfügbar:
  ☐ Python 3.8+ (für Validierungsskripte)
  ☐ grep/ripgrep (für Textsuche)
  ☐ Markdown Editor (VSCode oder ähnlich)
  ☐ Git (für Versionshistorie)
```

### 1.2 Dateien identifizieren

```
☐ Haupt-README: README.md
☐ Kapitel-README: chapters/README.md
☐ Appendix-README: appendices/README.md
☐ Docs-README: docs/README.md
☐ Models-README: data/models/README.md
☐ Skills-README: .claude/commands/README.md
☐ Andere (je nach Projekt): ___________
```

### 1.3 Automatisierte Basis-Checks ausführen

```bash
# Schritt 1: Skript ausführen
python scripts/validate_readme_consistency.py

# Prüfen ob erfolgreich
# Erwartet: "Status: PASSED" oder "Status: FAILED"

# Schritt 2: Report inspizieren
cat quality/readme-validation-report.json | jq '.summary'
```

### 1.4 Befunde dokumentieren

```
Audit-Datum: ___________________
Auditor: ________________________
Skript-Ergebnis: PASSED / FAILED / WARNINGS
Fehleranzahl (automatisch detektiert): _____
Warnungsanzahl: _____
```

---

## 📊 PHASE 2: ZAHLENKONSISTENZ (10 min)

### 2.1 Appendix-Zahlen

Suche nach allen Erwähnungen von Appendix-Zahlen:

```bash
grep -n "append" README.md chapters/README.md appendices/README.md | grep -E "[0-9]+"
```

**Checkliste:**

```
☐ README.md - Haupt-Zahl dokumentieren:
   - Zeile: ________  Zahl: ________
   - Zeile: ________  Zahl: ________
   - Zeile: ________  Zahl: ________
   Konsistent? ☐ JA ☐ NEIN ☐ MEHRERE WERTE GEFUNDEN

☐ appendices/README.md - Zahlen prüfen:
   - "165 systematische Ergänzungen" vorhanden? ☐ JA ☐ NEIN
   - "167 Dateien" Erklärung vorhanden? ☐ JA ☐ NEIN

☐ docs/README.md - Zahlen prüfen:
   - Appendix-Referenz korrekt? ☐ JA ☐ NEIN

☐ Alle Zahlen stimmen überein? ☐ JA ☐ NEIN
   Falls NEIN → Fehler #_____ dokumentieren
```

### 2.2 Kapitel-Zahlen

```bash
grep -n "kapitel\|chapter" README.md | grep -i "19\|76"
```

```
☐ Hauptzahl "19 + 4 Extended" oder "76" überall konsistent?
   ☐ README.md Zeile: ___  Zahl: ___
   ☐ chapters/README.md Zeile: ___  Zahl: ___
   ☐ docs/README.md Zeile: ___  Zahl: ___

☐ Alle Zahlen identisch? ☐ JA ☐ NEIN
   Falls NEIN → Fehler #_____ dokumentieren
```

### 2.3 Paper-/Reference-Zahlen

```bash
grep -n "1,922\|2,226\|50+" README.md
```

```
☐ Papers: "1,922" überall gleich?
   ☐ Vorkommen: _____
   ☐ Konsistent? ☐ JA ☐ NEIN

☐ Bibliography: "2,226" überall gleich?
   ☐ Vorkommen: _____
   ☐ Konsistent? ☐ JA ☐ NEIN

☐ "50+ Jahre" Research überall gleich?
   ☐ Vorkommen: _____
   ☐ Konsistent? ☐ JA ☐ NEIN
```

### 2.4 Skills/Commands-Zahlen

```bash
grep -n "15\|skill\|command" README.md | grep -i "+"
```

```
☐ Skills-Zahl konsistent?
   Erwartung: "15+" oder spezifische Zahl
   ☐ README.md sagt: _____
   ☐ .claude/commands/README.md sagt: _____
   ☐ Übereinstimmend? ☐ JA ☐ NEIN
```

### 2.5 SSOT Quelle dokumentieren

```
Quelle der Wahrheit für Zahlen:
  ☐ scripts/update_readme_stats.py (automatisch)
  ☐ data/counts_registry.yaml (manuell gepflegt)
  ☐ Andere: ________________________

Falls nicht automatisiert:
  → Verbesserungsvorschlag dokumentieren
```

---

## 🏷️ PHASE 3: VERSIONSKONSISTENZ (5 min)

### 3.1 Hauptversion prüfen

```bash
grep -n "Version\|version" README.md | head -5
```

```
☐ Hauptversion in README.md bestimmen:
   Header Version: _______
   Erwartung: v54 (Januar 2026)
   ☐ Stimmt überein? ☐ JA ☐ NEIN
```

### 3.2 Version in allen Dateien prüfen

```bash
grep -r "v5[0-9]" *.md docs/ chapters/ appendices/ | grep -v "changelog"
```

```
☐ v54 überall vorhanden (außer Changelog)?
   ☐ README.md: ☐ JA ☐ NEIN ☐ MEHRERE WERTE
   ☐ docs/README.md: ☐ JA ☐ NEIN ☐ MEHRERE WERTE
   ☐ chapters/README.md: ☐ JA ☐ NEIN ☐ MEHRERE WERTE
   ☐ appendices/README.md: ☐ JA ☐ NEIN ☐ MEHRERE WERTE
   ☐ .claude/commands/README.md: ☐ JA ☐ NEIN ☐ MEHRERE WERTE

☐ Überaltete Versionen gefunden (v47, v53)?
   ☐ NEIN (gut!)
   ☐ JA → Zeilen: _________ → Fehler dokumentieren
```

### 3.3 Datums-Konsistenz

```bash
grep -n "2026-01-2[0-9]\|Januar.*2026" README.md
```

```
☐ Datum überall aktuell (2026-01-20 oder neuer)?
   Vorkommen: _____
   ☐ Alle konsistent? ☐ JA ☐ NEIN

☐ Veraltete Daten gefunden?
   ☐ NEIN (gut!)
   ☐ JA → Welche: _________ → Fix
```

---

## 🔗 PHASE 4: LINK-VALIDITÄT (10 min)

### 4.1 Markdown Links extrahieren

```bash
grep -o "\[.*\](.*)" README.md | sort | uniq
```

```
☐ Externe Links (http/https):
   Anzahl: _____
   ☐ Alle sind HTTPS? ☐ JA ☐ NEIN
   Broken? ☐ NEIN ☐ JA → Welche: _________

☐ Relative Links (lokale Dateien):
   Anzahl: _____
   ☐ Alle vorhanden? ☐ JA ☐ NEIN
   Falls NEIN → Broken Links dokumentieren
```

### 4.2 Spezifische Link-Checks

```
☐ Appendix-Links:
  [ ] [AAA](appendices/AAA_...) - vorhanden? ☐ JA ☐ NEIN
  [ ] [B](appendices/B_...) - vorhanden? ☐ JA ☐ NEIN
  [ ] [C](appendices/C_...) - vorhanden? ☐ JA ☐ NEIN
  [ ] [AU](appendices/AU_...) - vorhanden? ☐ JA ☐ NEIN
  [ ] [AV](appendices/AV_...) - vorhanden? ☐ JA ☐ NEIN
  [ ] [AW](appendices/AW_...) - vorhanden? ☐ JA ☐ NEIN

☐ Chapter-Links:
  [ ] [Chapter 1] - vorhanden? ☐ JA ☐ NEIN
  [ ] [Chapter 10] - vorhanden? ☐ JA ☐ NEIN
  [ ] [Chapter 11] - vorhanden? ☐ JA ☐ NEIN

☐ Docs-Links:
  [ ] [EBF-INTRODUCTION.md] - vorhanden? ☐ JA ☐ NEIN
  [ ] [CLAUDE.md] - vorhanden? ☐ JA ☐ NEIN
  [ ] [frameworks/...] - vorhanden? ☐ JA ☐ NEIN

☐ PDF-Links:
  [ ] [complementarity_context_main_v54.pdf] - vs v47? ☐ KORREKT ☐ OUTDATED
  [ ] [complementarity_context_appendices_v54.pdf] - vs v47? ☐ KORREKT ☐ OUTDATED
```

### 4.3 Link-Fehler-Report

```
Broken Links gefunden:
___________________________________________
___________________________________________

Zu beheben: ☐ JA ☐ NEIN
```

---

## ✍️ PHASE 5: FORMATIERUNGSFEHLER (10 min)

### 5.1 Markdown Syntax

```bash
grep -E "\*{3,}" README.md  # Triple asterisks
```

```
☐ Doppelte/Triple Sternchen gefunden?
   ☐ NEIN (gut!)
   ☐ JA → Zeilen: _______ → Beispiele:
      ___________
      ___________

☐ Ungeschlossene Bold/Italic (* oder **)?
   Prüfe: Jedes ** sollte Paar haben
   ☐ OK ☐ FEHLER → Zeilen: _________

☐ Code-Blöcke korrekt geschlossen (```)?
   Anzahl ```: _____ (sollte GERADE sein)
   ☐ OK ☐ FEHLER
```

### 5.2 Tabellen-Struktur

```
Tabelle 1: 10C CORE Framework
  ☐ Spaltenanzahl konsistent? ☐ JA ☐ NEIN
  ☐ Trennlinie (|---|) vorhanden? ☐ JA ☐ NEIN
  ☐ Daten sinnvoll? ☐ JA ☐ NEIN
  ☐ Keine doppelten Zeilen? ☐ JA ☐ NEIN

Tabelle 2: Dokumentstruktur
  ☐ Spaltenanzahl konsistent? ☐ JA ☐ NEIN
  ☐ Alle Kapitel referenziert? ☐ JA ☐ NEIN

Tabelle 3: Portfolio Archetypes
  ☐ Keine doppelten Sternchen? ☐ JA ☐ NEIN
  ☐ 7 Einträge vorhanden? ☐ JA ☐ NEIN
  ☐ Alle Spalten gefüllt? ☐ JA ☐ NEIN

Alle anderen Tabellen:
  Gesamtzahl: _____
  ☐ Alle strukturell OK? ☐ JA ☐ NEIN
  Falls NEIN → Welche: _________
```

---

## 🔄 PHASE 6: DATENINTEGRITÄT (5 min)

### 6.1 Duplizierungen suchen

```bash
grep -n "STAGE\|CORE\|Appendix" README.md | sort | uniq -d
```

```
☐ Duplizierte Einträge in Tabellen?
   ☐ NEIN (gut!)
   ☐ JA → Welche:
      ___________
      ___________

☐ Spezifisch: Zwei "8 | **STAGE**" Einträge?
   Suche in Zeile 98-99
   ☐ NEIN ☐ JA → Fehler!
```

### 6.2 Konsistenz Kategorienamen

```
☐ 10C Names überall identisch?
   [ ] WHO ☐ JA ☐ NEIN
   [ ] WHAT ☐ JA ☐ NEIN
   [ ] HOW ☐ JA ☐ NEIN
   [ ] WHEN ☐ JA ☐ NEIN
   [ ] WHERE ☐ JA ☐ NEIN
   [ ] AWARE ☐ JA ☐ NEIN
   [ ] READY ☐ JA ☐ NEIN
   [ ] STAGE ☐ JA ☐ NEIN

☐ Appendix-Kategorien (8 Stück)?
   [ ] CORE (8) ☐ JA ☐ NEIN
   [ ] FORMAL (10+) ☐ JA ☐ NEIN
   [ ] DOMAIN (40+) ☐ JA ☐ NEIN
   [ ] CONTEXT (10+) ☐ JA ☐ NEIN
   [ ] METHOD (15+) ☐ JA ☐ NEIN
   [ ] PREDICT (20+) ☐ JA ☐ NEIN
   [ ] LIT (40+) ☐ JA ☐ NEIN
   [ ] REF (15+) ☐ JA ☐ NEIN

☐ Skills überall gleich benannt?
   Überprüfe: /new-customer, /apply-models, /design-model, /design-intervention
   ☐ OK ☐ FEHLER
```

---

## 📝 PHASE 7: CONTENT-GENAUIGKEIT (10 min)

### 7.1 Kapitel-Beschreibungen

```
Überprüfe Schnellstart-Sektion:

Für Theoretiker:
  [ ] Kapitel 1 → Chapter 1 vorhanden? ☐ JA ☐ NEIN
  [ ] Kapitel 5 → Chapter 5 vorhanden? ☐ JA ☐ NEIN
  [ ] Kapitel 9 → Chapter 9 vorhanden? ☐ JA ☐ NEIN

Für Empiriker:
  [ ] Kapitel 4x → Existiert (4x bedeutet > 4)? ☐ JA ☐ NEIN
  [ ] Appendix BBB → Vorhanden? ☐ JA ☐ NEIN
  [ ] Appendix AN → Vorhanden? ☐ JA ☐ NEIN

Für Praktiker:
  [ ] Kapitel 11 (Awareness) korrekt? ☐ JA ☐ NEIN
  [ ] Kapitel 12 (Willingness) korrekt? ☐ JA ☐ NEIN
  [ ] Kapitel 17 beschreibt "Intervention Design"? ☐ JA ☐ NEIN
```

### 7.2 Feature-Beschreibungen

```
✅ Evidence Integration Pipeline:
   ☐ Beschreibung technisch korrekt? ☐ JA ☐ NEIN
   ☐ Link zu EIP Docs vorhanden? ☐ JA ☐ NEIN

✅ Intervention Design Workflow:
   ☐ Beschreibung ist "20-Field Schema"? ☐ JA ☐ NEIN
   ☐ Skill-Beispiel vorhanden? ☐ JA ☐ NEIN

✅ UNTCM Model:
   ☐ Appendix UN referenziert? ☐ JA ☐ NEIN
   ☐ Komponenten aufgelistet? ☐ JA ☐ NEIN

✅ Natural Trajectory Model:
   ☐ NTM Definition klar? ☐ JA ☐ NEIN
   ☐ Appendix NTM vorhanden? ☐ JA ☐ NEIN

✅ Portfolio Archetypes:
   ☐ 7 Designs vorhanden? ☐ JA ☐ NEIN
   ☐ Appendix WAT referenziert? ☐ JA ☐ NEIN
   ☐ Alle mit Zielen/Effektivität? ☐ JA ☐ NEIN
```

---

## 🎯 PHASE 8: QUERVERWEIS-VALIDIERUNG (5 min)

### 8.1 Bidirektionale Links

```
☐ Wenn README.md → Chapter 11 referenziert
   → Prüfe ob chapters/README.md auch in Part V?
   ☐ JA ☐ NEIN

☐ Wenn README.md → Appendix AAA referenziert
   → Prüfe ob appendices/README.md auch AAA hat?
   ☐ JA ☐ NEIN

☐ Wenn README.md → Skills referenziert
   → Prüfe ob .claude/commands/README.md auch dokumentiert?
   ☐ JA ☐ NEIN
```

### 8.2 Kreuzreferenzen

```
Haupttext sagt "8 CORE Fragen":
  ☐ Alle 8 in der Tabelle? ☐ JA ☐ NEIN
  ☐ Alle in Appendices referenziert? ☐ JA ☐ NEIN
  ☐ Alle in Kapiteln zugeordnet? ☐ JA ☐ NEIN

Skills erwähnt (15+):
  ☐ Alle in .claude/commands/README.md? ☐ JA ☐ NEIN
  ☐ Mit Beschreibungen? ☐ JA ☐ NEIN
  ☐ Mit Zeit-Angaben? ☐ JA ☐ NEIN
```

---

## 📊 PHASE 9: ZUSAMMENFASSUNG & REPORTING (5 min)

### 9.1 Fehler-Tallying

```
Gefundene Fehler:

KRITISCHE (🔴):
1. _________________________ (Zeile: ___)
2. _________________________ (Zeile: ___)
3. _________________________ (Zeile: ___)

MITTLERE (🟡):
1. _________________________ (Zeile: ___)
2. _________________________ (Zeile: ___)
3. _________________________ (Zeile: ___)

GERING (🟢):
1. _________________________ (Zeile: ___)
2. _________________________ (Zeile: ___)

Gesamt:
  🔴 KRITISCH: ___ (Muss behoben werden)
  🟡 MITTEL: ___ (Sollte behoben werden)
  🟢 GERING: ___ (Kann verbessert werden)
```

### 9.2 Audit-Resultat

```
Audit durchgeführt am: ___________________
Auditor: __________________________________
Zeit benötigt: ___________ Minuten

Gesamt-Fehler: _____
Höchste Severity: 🔴 KRITISCH / 🟡 MITTEL / 🟢 GERING / ✅ KEINE

Status: ☐ PASSED ☐ PASSED WITH WARNINGS ☐ FAILED

Automatisierung verbessert?
  Bisher: _____ Fehler automatisch detektiert
  Neu: _____ Fehler (neue Automation nötig)
  Empfehlung: _____________________________
```

### 9.3 Lessons Learned

```
Fehler, die nicht automatisch gefunden wurden:
1. _________________________ (Automation: _________)
2. _________________________ (Automation: _________)

Neue Best Practices erkannt:
1. _____________________________
2. _____________________________

Für nächste Audit zu verbessern:
1. _____________________________
2. _____________________________
```

---

## 📝 AUSGABE & DOKUMENTATION

### Checklist-Resultat exportieren

```bash
# Kopiere diese Checklist
cp quality/readme-audit-checklist.md \
   quality/audits/audit-2026-01-20.md

# Fülle aus
# Komm während Audit aus

# Commit
git add quality/audits/audit-2026-01-20.md
git commit -m "docs(audit): Complete README audit 2026-01-20"
```

### JSON-Report erstellen

```python
# Erstelle strukturiertes JSON-Report
python scripts/validate_readme_consistency.py
# Output: quality/readme-validation-report.json
```

---

## ⏱️ ZEITBUDGET

| Phase | Zeit | Kumulativ |
|-------|------|-----------|
| 1: Vorbereitung | 5 min | 5 min |
| 2: Zahlenkonsistenz | 10 min | 15 min |
| 3: Versionskonsistenz | 5 min | 20 min |
| 4: Link-Validität | 10 min | 30 min |
| 5: Formatierung | 10 min | 40 min |
| 6: Datenintegrität | 5 min | 45 min |
| 7: Content-Genauigkeit | 10 min | 55 min |
| 8: Querverweise | 5 min | 60 min |
| 9: Zusammenfassung | 5 min | 65 min |

**Gesamt: ~60-75 Minuten pro vollständiger Audit**

---

*Letzte Aktualisierung: 2026-01-20*
*Version: 1.0 — Full Checklist with Automation Integration*
