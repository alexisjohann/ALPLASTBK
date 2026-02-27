# 🤖 README Auto-Update System (Hybrid)

> Automatisches Aktualisieren der README-Dateien: Wöchentlich + Trigger-basiert + Ad-hoc

---

## 📋 Übersicht

Das System besteht aus **3 Komponenten**:

| Komponente | Wann? | Was? | Status |
|-----------|-------|------|--------|
| **1️⃣ Wöchentlich** | Jeden Montag 08:00 UTC | GitHub Actions Cron | ✅ |
| **2️⃣ Trigger-basiert** | Bei bestimmten Änderungen | Push zu `appendices/*.tex`, `chapters/*.tex`, `CLAUDE.md` etc. | ✅ |
| **3️⃣ Ad-hoc** | Auf Anfrage | Manuell: `python scripts/update_readme_stats.py` | ✅ |

---

## 🔄 Komponente 1: Wöchentliche Automatisierung

**Datei:** `.github/workflows/update-readme-weekly.yml`

**Auslöser:** Jeden Montag um 08:00 UTC (09:00 CET)

**Was wird aktualisiert:**
- Appendices count
- Chapters count
- Bibliography entries
- Timestamps

**Beispiel:**
```
Montag, 08:00 UTC
  ↓
GitHub Actions startet
  ↓
Python-Script läuft
  ↓
README-Dateien aktualisiert
  ↓
Auto-Commit: "docs(weekly): Auto-update README statistics"
```

**Manuell auslösen:**
```bash
# GitHub UI: Actions → "Weekly README Update" → "Run workflow"
# Oder mit gh CLI:
gh workflow run update-readme-weekly.yml
```

---

## 🎯 Komponente 2: Trigger-basierte Automatisierung

**Datei:** `.github/workflows/update-readme-on-changes.yml`

**Auslöser:** Automatisch bei Push zu bestimmten Dateien

### Trigger-Pfade:

```yaml
appendices/*.tex          # Neue/geänderte Appendices
chapters/*.tex            # Neue/geänderte Chapters
bibliography/bcm_master.bib  # Bibliographie erweitert
CLAUDE.md                 # AI-Kontext aktualisiert
.claude/commands/**       # Skills/Commands hinzugefügt
```

**Beispiel-Workflow:**
```
Du commitest neuen Appendix UN_FORMAL-UNTCM.tex
  ↓
Git-Push zu main oder claude/...
  ↓
GitHub Actions erkennt: "appendices/*.tex" changed
  ↓
Python-Script läuft automatisch
  ↓
README.md aktualisiert: "Appendices: 167"
  ↓
Auto-Commit: "docs(appendix): Update README - new appendix added"
```

---

## 📞 Komponente 3: Ad-hoc Manuell

**Für sofortige Updates ohne zu warten:**

### Option A: Lokal ausführen
```bash
# Im repo root:
python scripts/update_readme_stats.py

# Output:
# 🔄 Updating README statistics...
#   ✓ Appendices: 167 (files: 170)
#   ✓ Chapters: 76 (files: 77)
#   ✓ Bibliography: 2226 entries
# ✅ Updated: README.md
# ✅ Updated: docs/README.md
# ✅ Updated: chapters/README.md
# ✅ Updated: appendices/README.md

# Dann normal committen:
git add README.md docs/README.md chapters/README.md appendices/README.md
git commit -m "docs: Manual README update"
git push
```

### Option B: Mit GitHub Actions
```bash
# GitHub UI: Actions → "Weekly README Update" → "Run workflow"
```

### Option C: Frag Claude
```
"Claude, bitte README aktualisieren"
```

---

## 📊 Was wird aktualisiert?

### README.md (Haupt-README)
```markdown
| Metrik | Wert |
|--------|------|
| **Kapitel** | {{ chapter_count }} + 4 Extended |
| **Appendices** | {{ appendix_count }} (A-QQQ++) |
| **Referenzen** | {{ bib_count }} BibTeX Einträge |
```

### docs/README.md
```markdown
| Ordner | Inhalt |
|--------|--------|
| `/chapters/` | {{ chapter_files }} Kapitel-Quelldateien |
| `/appendices/` | {{ appendix_files }} Appendix-Quelldateien |
| `/bibliography/` | {{ bib_count }} BibTeX Einträge |
```

### chapters/README.md
```markdown
| Metrik | Wert |
|--------|------|
| **Dateien** | {{ chapter_files }} |
```

### appendices/README.md
```markdown
| Metrik | Wert |
|--------|------|
| **Appendices** | {{ appendix_count }} |
| **Dateien** | {{ appendix_files }}+ |
```

Alle mit **Timestamp**: `*Letzte Aktualisierung: YYYY-MM-DD*`

---

## 🔧 Das Python-Script erklärt

**Datei:** `scripts/update_readme_stats.py`

### Funktionen:

```python
count_appendices()        # Zählt *.tex in appendices/ (ohne 00_*)
count_chapters()          # Zählt *.tex in chapters/ (ohne 00_*)
count_bibliography()      # Grep nach @article, @book in bcm_master.bib
get_last_commit_date()    # Holt letztes Commit-Datum
update_readme_statistics()  # Aktualisiert README.md
update_docs_readme()      # Aktualisiert docs/README.md
update_chapters_readme()  # Aktualisiert chapters/README.md
update_appendices_readme() # Aktualisiert appendices/README.md
```

### Pattern-Matching:

```python
# Findet und ersetzt automatisch:
| **Appendices** | 167 |  → | **Appendices** | {{ new_count }} |
| **Kapitel** | 19 + 4 Extended | (bleiben unverändert)
| *Letzte Aktualisierung: 2026-01-20* → | *Letzte Aktualisierung: {{ today }} *|
```

---

## ⚙️ Konfiguration

### Wöchentliches Schedule ändern:

**Datei:** `.github/workflows/update-readme-weekly.yml`

```yaml
on:
  schedule:
    - cron: '0 8 * * 1'  # Montag 08:00 UTC

# Beispiele:
# '0 8 * * 1'    → Montag 08:00 UTC
# '0 0 * * *'    → Täglich Mitternacht UTC
# '0 9 * * 1-5'  → Werktags 09:00 UTC
```

[Cron Syntax Hilfe](https://crontab.guru/)

### Trigger-Pfade ändern:

**Datei:** `.github/workflows/update-readme-on-changes.yml`

```yaml
on:
  push:
    paths:
      - 'appendices/*.tex'          # Diese Pfade überwachen
      - 'chapters/*.tex'
      - 'bibliography/bcm_master.bib'
      - 'CLAUDE.md'
      - '.claude/commands/**'
```

---

## 📈 Monitoring

### GitHub Actions Status prüfen:

```bash
# GitHub UI: Settings → Actions → Workflows
# Oder mit gh CLI:
gh run list --workflow=update-readme-weekly.yml
gh run list --workflow=update-readme-on-changes.yml

# Details einer Run:
gh run view <run-id>
```

### Last successful run:
```bash
gh run list --workflow=update-readme-weekly.yml --limit 1 --status completed
```

---

## 🚨 Troubleshooting

### Problem: Commit schlägt fehl
```
fatal: no changes added to commit
```
**Lösung:** Script hat erkannt, dass keine Änderungen nötig sind. Das ist OK! ✅

### Problem: GitHub Actions läuft nicht
```
No workflows found
```
**Lösung:** Workflows sind im `.github/workflows/` Verzeichnis, müssen gepusht sein:
```bash
git add .github/workflows/
git push
```

### Problem: Falsche Zahlen
```
Appendices: 100 (sollte 167 sein)
```
**Lösung:** Script zählt nur LaTeX-Dateien ohne `00_` Prefix:
```bash
# Prüfen:
ls -la appendices/*.tex | wc -l  # Total
ls -la appendices/[!0]*.tex | wc -l  # Ohne 00_*
```

---

## 🔐 Permissions

Die GitHub Actions brauchen:
- `contents: write` — Um Commits zu machen

```yaml
permissions:
  contents: write
```

Ist bereits konfiguriert in den Workflows. ✅

---

## 📝 Logs & Debugging

### Lokales Testen:
```bash
# Im repo root:
python scripts/update_readme_stats.py --debug

# Zeigt:
# - Gefundene Dateien
# - Neue Zahlen
# - Was geändert wurde
```

### GitHub Actions Logs:
```
GitHub UI → Actions → [Workflow Name] → [Run] → [Logs]
```

---

## 🎯 Best Practices

### 1. Wöchentliche Checks
- ✅ Jeden Montag um 08:00 UTC
- ✅ Automatisch committed wenn Änderungen
- ✅ Oder manuell auslösen wenn nötig

### 2. Trigger-basiert
- ✅ Sofort nach neuen Appendices/Chapters
- ✅ Nach CLAUDE.md Updates
- ✅ Nach Bibliography-Erweiterungen

### 3. Ad-hoc
- ✅ Für schnelle Fixes
- ✅ Für manuelle Tests
- ✅ Wenn GitHub Actions down ist

---

## 📞 Support

**Fragen oder Probleme?**

```bash
# Manuell testen:
python scripts/update_readme_stats.py

# Git Status prüfen:
git status

# Logs anschauen:
gh run list --limit 10
```

---

*Setup implementiert: 20. Januar 2026*
*Hybrid-Automatisierung: Wöchentlich + Trigger + Ad-hoc* ✅
