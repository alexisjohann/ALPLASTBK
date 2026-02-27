# EBF CORE Framework Erweiterungsanleitung

> Wie man das 9C CORE Framework auf 9C, 10C, etc. erweitert

---

## Übersicht

Das EBF CORE Framework ist durch ein **Single Source of Truth (SSOT)** System erweiterbar. Diese Anleitung beschreibt den Prozess, um ein neues CORE (z.B. 9C) hinzuzufügen.

### Architektur

```
docs/frameworks/core-framework-definition.yaml  ← SINGLE SOURCE OF TRUTH
         │
         ▼
scripts/validate_core_framework.py              ← VALIDIERUNG
         │
         ▼
[Alle anderen Dateien]                          ← MÜSSEN KONSISTENT SEIN
```

---

## Schritt 1: SSOT aktualisieren

Öffne `docs/frameworks/core-framework-definition.yaml` und:

### 1.1 Framework-Version erhöhen

```yaml
framework:
  name: "EBF CORE Framework"
  version: "9C"    # ← von 9C auf 9C ändern
  count: 9         # ← von 8 auf 9 ändern
```

### 1.2 Neuen CORE hinzufügen

Füge am Ende der `cores:` Liste einen neuen Eintrag hinzu:

```yaml
  # --------------------------------------------------------------------------
  # CORE 9: [CODE] - [Beschreibung]
  # --------------------------------------------------------------------------
  - number: 9
    code: "[CODE]"                              # z.B. "SUSTAIN"
    appendix_code: "[AX]"                       # z.B. "AX"
    full_name: "CORE-[CODE]"                    # z.B. "CORE-SUSTAIN"
    title: "[English Title]"                    # z.B. "The Sustainability Function"
    question_de: "[Deutsche Frage]"             # z.B. "Wie nachhaltig?"
    question_en: "[English Question]"           # z.B. "How sustainable?"
    output: "[Output-Beschreibung]"             # z.B. "Sustainability σ"
    primary_symbol: "[Symbol]"                  # z.B. "σ"
    chapter_reference: [N]                      # Kapitel-Nummer
    file: "appendices/[AX]_[name].tex"          # z.B. "appendices/AX_sustainability.tex"
    key_concepts:
      - "Concept 1"
      - "Concept 2"
```

### 1.3 Stage-Gleichung erweitern (falls nötig)

Wenn der neue CORE einen neuen Stage hinzufügt:

```yaml
  equations:
    stage_5:
      name: "New Stage Name"
      formula: "[Neue Formel]"
      depends_on: [NEW_CODE]
```

---

## Schritt 2: Validierung ausführen

```bash
python scripts/validate_core_framework.py --verbose
```

Das Script zeigt alle Dateien, die inkonsistent sind.

---

## Schritt 3: Dateien aktualisieren

Das Validierungsscript zeigt alle Dateien, die aktualisiert werden müssen. Typischerweise:

### Pflicht-Dateien

| Datei | Was ändern |
|-------|------------|
| `README.md` | 9C → 9C, CORE-Tabelle erweitern |
| `CLAUDE.md` | 9C → 9C, 9C CORE Tabelle erweitern |
| `appendices/README.md` | CORE-Sektion erweitern |
| `appendices/00_appendix_index.tex` | Neuen CORE eintragen |
| `docs/frameworks/appendix-category-definitions.md` | CORE-Count und Tabelle |

### Kapitel-READMEs

Alle `chapters/ch*_README.md` Dateien, die "9C" oder die CORE-Tabelle referenzieren.

### Neue Appendix-Datei

1. Kopiere `appendices/00_appendix_template.tex`
2. Benenne um: `appendices/[AX]_[name].tex`
3. Fülle alle PFLICHT-Sektionen aus
4. Mindestens 80 Axiome für einen CORE

---

## Schritt 4: Qualitätsprüfung

```bash
# 1. Template Compliance prüfen
python scripts/check_template_compliance.py appendices/[AX]_[name].tex

# 2. Validierung erneut ausführen
python scripts/validate_core_framework.py

# 3. In quality/checklist.md dokumentieren
```

---

## Schritt 5: Dokumentation aktualisieren

### quality/checklist.md

Neuen CORE in die Qualitätstabelle eintragen.

### quality/lessons_learned.md

Erweiterungsprozess dokumentieren:

```markdown
### YYYY-MM-DD: 9C Framework Extension

**Kontext:** Erweiterung von 9C auf 9C mit CORE-[CODE]

| # | Beobachtung | Verbesserungspotential | Status |
|---|-------------|------------------------|--------|
| 1 | ... | ... | DONE |

**Empfehlung:** [Konkrete Änderung]
```

---

## Checkliste für Framework-Erweiterung

```markdown
## [CODE] CORE Addition Checklist

### SSOT Update
- [ ] core-framework-definition.yaml: version/count aktualisiert
- [ ] core-framework-definition.yaml: neuer CORE-Eintrag vollständig
- [ ] core-framework-definition.yaml: equations aktualisiert (falls neuer Stage)

### Validierung
- [ ] validate_core_framework.py ausgeführt
- [ ] Alle Fehler behoben
- [ ] Erneute Validierung: 0 Probleme

### Dateien aktualisiert
- [ ] README.md
- [ ] CLAUDE.md
- [ ] appendices/README.md
- [ ] appendices/00_appendix_index.tex
- [ ] docs/frameworks/appendix-category-definitions.md
- [ ] Kapitel-READMEs (wo relevant)

### Neue Appendix
- [ ] Datei erstellt: appendices/[AX]_[name].tex
- [ ] Template-Compliance: ≥ 85%
- [ ] Mindestens 80 Axiome
- [ ] Cross-References zu allen anderen COREs

### Qualität
- [ ] quality/checklist.md aktualisiert
- [ ] quality/lessons_learned.md dokumentiert
```

---

## Beispiel: 9C → 9C Erweiterung

Angenommen, wir fügen CORE-SUSTAIN (Nachhaltigkeit) hinzu:

### 1. SSOT aktualisieren

```yaml
framework:
  version: "9C"
  count: 9

cores:
  # ... existing 8 COREs ...

  - number: 9
    code: "SUSTAIN"
    appendix_code: "AX"
    full_name: "CORE-SUSTAIN"
    title: "The Sustainability Function"
    question_de: "Wie nachhaltig?"
    question_en: "How sustainable?"
    output: "Sustainability σ(t)"
    primary_symbol: "σ"
    chapter_reference: 14
    file: "appendices/AX_sustainability.tex"
    key_concepts:
      - "Long-term utility"
      - "Intergenerational effects"
      - "Discount rates"
```

### 2. Validierung

```bash
$ python scripts/validate_core_framework.py

❌ 12 Problem(e) gefunden:
   WRONG_NC_COUNT: 10 Problem(e)
   MISSING_FILE: 1 Problem(e)
   ...
```

### 3. Fehler beheben

```bash
# Alle 9C → 9C ersetzen
sed -i 's/9C CORE/9C CORE/g' README.md CLAUDE.md ...

# Neue Appendix erstellen
cp appendices/00_appendix_template.tex appendices/AX_sustainability.tex
```

### 4. Erneute Validierung

```bash
$ python scripts/validate_core_framework.py

✅ Keine Probleme gefunden! Das 9C Framework ist konsistent.
```

---

## Häufige Fehler

| Fehler | Lösung |
|--------|--------|
| `MISSING_FILE` | Appendix-Datei erstellen |
| `WRONG_NC_COUNT` | nC Referenzen aktualisieren |
| `COUNT_MISMATCH` | framework.count mit cores-Anzahl synchronisieren |
| `DUPLICATE_CODE` | Eindeutigen CORE-Code wählen |

---

## Support

Bei Fragen zum Erweiterungsprozess:
1. `docs/frameworks/core-framework-definition.yaml` lesen
2. `scripts/validate_core_framework.py --verbose` ausführen
3. Diese Anleitung konsultieren

---

*Version 1.0 | Januar 2026*
