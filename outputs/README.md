# 📤 EBF Outputs

> Alle produzierten Dokumente nach Format organisiert

---

## 📊 Übersicht

| Kategorie | Formate | Seiten | Ordner |
|-----------|---------|--------|--------|
| **SHORT** | 1-Pager, Summary, Memo, Abstract | 1-5 | `short/` |
| **MEDIUM** | Proposal, Report, Working Paper, Case Study | 5-30 | `medium/` |
| **LONG** | White Paper, Technical Report, Journal Article | 30-100 | `long/` |
| **POLICY** | Policy Memos | 2-5 | `policy/` |
| **PRESENTATIONS** | Slides | 10-30 Folien | `presentations/` |

---

## 📁 Ordner-Struktur

```
outputs/
├── README.md                     # Diese Datei
│
├── short/                        # KURZE DOKUMENTE (1-5 Seiten)
│   ├── README.md
│   ├── one-pagers/               # 1-Pager
│   ├── summaries/                # Executive Summaries
│   ├── memos/                    # Memos
│   └── abstracts/                # Abstracts
│
├── medium/                       # MITTLERE DOKUMENTE (5-30 Seiten)
│   ├── README.md
│   ├── proposals/                # Proposals
│   ├── reports/                  # Reports
│   ├── working-papers/           # Working Papers
│   └── case-studies/             # Case Studies
│
├── long/                         # LANGE DOKUMENTE (30-100 Seiten)
│   ├── README.md
│   ├── white-papers/             # White Papers
│   ├── technical-reports/        # Technical Reports
│   └── papers/                   # Journal Articles
│
├── policy/                       # POLICY DOKUMENTE
│   └── README.md
│
└── presentations/                # PRÄSENTATIONEN
    └── README.md
```

---

## 🔢 Nummerierung

| Format | Schema | Beispiel |
|--------|--------|----------|
| Working Paper | WP-NNN | WP-001, WP-002 |
| Case Study | CS-NNN | CS-001, CS-002 |
| Report | RPT-YYYY-NNN | RPT-2026-001 |
| White Paper | WHP-YYYY-NNN | WHP-2026-001 |

---

## 📝 Namenskonventionen

### Ordner

```
[YYYY-MM-DD]_[topic]/              # Datierte Dokumente
[CODE]_[short-title]/              # Nummerierte Dokumente
```

### Dateien

```
[type].tex                         # Hauptdatei
[type].pdf                         # Kompiliert
[type]_v[N].tex                    # Versioniert
metadata.yaml                      # Metadaten
```

---

## 📋 metadata.yaml Template

```yaml
# Pflichtfelder
title: "Dokumententitel"
type: "one-pager|memo|report|..."
date: "2026-01-06"
author: "Name"
status: "draft|review|final"

# Optional
version: "1.0"
abstract: "Kurzbeschreibung"
keywords: ["keyword1", "keyword2"]
related_docs: ["path/to/doc"]

# Format-spezifisch
# (siehe FORMAT_REGISTRY.md)
```

---

## 🔗 Verwandte Dokumente

- [FORMAT_REGISTRY.md](../docs/FORMAT_REGISTRY.md) - Vollständige Format-Spezifikationen
- [GITHUB_DOCUMENTATION_GUIDE.md](../docs/GITHUB_DOCUMENTATION_GUIDE.md) - Konventionen
- [Master Framework](../00_master_documentation_framework.tex) - 12 Dimensionen

---

## ✅ Neues Dokument erstellen

1. **Format bestimmen** → Master Framework, Schritt 2
2. **Korrekten Ordner wählen** → Diese Übersicht
3. **Template kopieren** → `00_template.*` im Ordner
4. **metadata.yaml anlegen**
5. **README.md aktualisieren**

---

*Letzte Aktualisierung: Januar 2026 — 9C CORE Framework*
