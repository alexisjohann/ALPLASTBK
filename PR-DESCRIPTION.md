# Pull Request: Hybrid README Auto-Update System

## 📋 PR Title
```
feat: Implement hybrid README auto-update system (weekly + trigger + ad-hoc)
```

---

## 📝 PR Description

### Summary

Implementiert ein produktives **Hybrid-Auto-Update-System** für README-Dateien mit 3 unabhängigen Komponenten:

### 🔄 Komponente 1: Wöchentliche Automatisierung
- **Auslöser:** Jeden Montag 08:00 UTC
- **Workflow:** `.github/workflows/update-readme-weekly.yml`
- **Aktion:** Python-Script aktualisiert README-Statistiken
- **Commit:** Automatisch wenn Änderungen gefunden

### 🎯 Komponente 2: Trigger-basierte Automatisierung
- **Auslöser:** Push zu kritischen Dateien
  - `appendices/*.tex` → neue Appendices
  - `chapters/*.tex` → neue Chapters
  - `bibliography/bcm_master.bib` → Bibliographie
  - `CLAUDE.md` → AI-Kontext
  - `.claude/commands/**` → Skills
- **Workflow:** `.github/workflows/update-readme-on-changes.yml`
- **Commits:** Auto-detects change type für aussagekräftige Messages

### 📞 Komponente 3: Ad-hoc Manuell
- **Script:** `scripts/update_readme_stats.py`
- **Benutzung:** `python scripts/update_readme_stats.py`
- **Für:** Lokale Tests, sofortige Updates

---

## 📊 Aktualisierte Dateien

Automatisch gepflegt:
- **README.md** - Appendices, Chapters, Bibliography, Timestamps
- **docs/README.md** - Dokumentations-Überblick
- **chapters/README.md** - Kapitel-Statistiken
- **appendices/README.md** - Appendix-Statistiken

---

## 🔧 Python-Script Details

**Funktionen:**
- Zählt *.tex Dateien (ohne 00_* Templates)
- Grep nach @entry in BibTeX
- Regex-Matching für sichere Updates
- Smart-Detection: nur kommitten wenn Änderungen nötig

**Ablauf:**
```
count_appendices()
  ↓ count_chapters()
  ↓ count_bibliography()
  ↓ regex-replace in 4 README.md Dateien
  ↓ Output: "✅ Updated: README.md"
```

---

## 📖 Dokumentation

Komplette Anleitung in: **`docs/README-AUTO-UPDATE.md`**
- Setup & Konfiguration
- Troubleshooting
- Monitoring Guide
- Cron-Syntax Hilfe

---

## ✅ Test Plan

Nach Merge zu main:

1. **GitHub Actions Auto-erkennung**
   - Workflows sollten automatisch geladen werden

2. **Nächster Montag 08:00 UTC**
   - Erste automatische Ausführung
   - README-Dateien sollten aktualisiert sein

3. **Manuell testen (optional)**
   ```bash
   gh workflow run update-readme-weekly.yml
   gh run list --workflow=update-readme-weekly.yml --limit 1
   ```

---

## 🎯 Benefits

✅ README immer aktuell
✅ Keine manuellen Updates
✅ Automatische Commits
✅ Flexible Konfiguration
✅ Ad-hoc Fallback
✅ Production-ready

---

## 📝 Commits in dieser PR

- `fc51118` - docs: Update README files with v54 changes
- `090988c` - feat: Implement hybrid README auto-update system
- `235c040` - docs: Update README with actual file counts

---

## 🚀 Status

**Branch:** `claude/update-readme-docs-paDas`
**Base Branch:** `main`
**Status:** Ready for review & merge

