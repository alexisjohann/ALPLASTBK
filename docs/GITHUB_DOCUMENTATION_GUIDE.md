# EBF GitHub Documentation Guide

> **Wie das Repository strukturiert und dokumentiert wird**

---

## 📋 Inhaltsverzeichnis

1. [Repository-Architektur](#repository-architektur)
2. [Ordnerstruktur](#ordnerstruktur)
3. [Namenskonventionen](#namenskonventionen)
4. [Dokumentations-Hierarchie](#dokumentations-hierarchie)
5. [README-Struktur pro Ordner](#readme-struktur-pro-ordner)
6. [Versionierung](#versionierung)
7. [Commit-Konventionen](#commit-konventionen)

---

## 🏗️ Repository-Architektur

### Drei-Ebenen-Struktur

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EBENE 1: ROOT                                       │
│                                                                             │
│  README.md              ← Haupteinstiegspunkt                               │
│  00_master_*.tex        ← Meta-Frameworks                                   │
│  *.pdf                  ← Kompilierte Dokumente                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EBENE 2: HAUPTORDNER                                │
│                                                                             │
│  chapters/              ← Kapitel-Quelldateien + README.md                  │
│  appendices/            ← Appendix-Quelldateien + README.md                 │
│  docs/                  ← Dokumentation + README.md                         │
│  ...                                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EBENE 3: UNTERORDNER                                │
│                                                                             │
│  docs/guides/           ← Anleitungen + README.md                           │
│  docs/frameworks/       ← Framework-Dokumentation + README.md               │
│  appendices/legacy/     ← Archivierte Versionen                             │
│  ...                                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Ordnerstruktur

### Vollständige Struktur

```
complementarity-context-framework/
│
├── 📄 README.md                           # Repository-Übersicht
├── 📄 CONTRIBUTING.md                     # Beitragsrichtlinien
├── 📄 CHANGELOG.md                        # Versionshistorie
│
├── 📄 00_master_documentation_framework.tex   # META: Integriertes Framework
├── 📄 00_document_specification_framework.tex # META: 12 Dimensionen
├── 📄 00_scope_structure_framework.tex        # META: Scope & Struktur
│
├── 📄 complementarity_context_v*.pdf      # Kompilierte PDFs
├── 📄 complementarity_context_v*.tex      # Monolithische Quelle (Legacy)
│
├── 📁 chapters/                           # HAUPTDOKUMENT
│   ├── 📄 README.md                       # Kapitel-Übersicht
│   ├── 📄 00_frontmatter.tex
│   ├── 📄 00_chapter_template.tex         # Template
│   ├── 📄 01_introduction.tex
│   ├── 📄 02_*.tex ... 15_*.tex
│   └── 📁 legacy/                         # Archivierte Versionen
│
├── 📁 appendices/                         # APPENDICES
│   ├── 📄 README.md                       # Appendix-Übersicht
│   ├── 📄 00_appendix_template.tex        # Template
│   ├── 📄 00_appendix_index.tex           # Master-Navigation
│   ├── 📄 appendix_A_*.tex                # FORMAL
│   ├── 📄 appendix_B_*.tex                # CORE-HOW
│   ├── 📄 appendix_C_*.tex                # CORE-WHAT
│   └── 📄 ... (49 Appendices)
│
├── 📁 docs/                               # DOKUMENTATION
│   ├── 📄 README.md                       # Dokumentations-Übersicht
│   ├── 📁 frameworks/                     # Framework-Dokumentation
│   │   ├── 📄 README.md
│   │   ├── 📄 master-framework.md
│   │   ├── 📄 12-dimensions.md
│   │   └── 📄 scope-structure.md
│   ├── 📁 guides/                         # Anleitungen
│   │   ├── 📄 README.md
│   │   ├── 📄 writing-chapters.md
│   │   ├── 📄 writing-appendices.md
│   │   └── 📄 github-workflow.md
│   └── 📁 references/                     # Nachschlagewerke
│       ├── 📄 glossary.md
│       └── 📄 symbol-reference.md
│
├── 📁 bibliography/                       # LITERATUR
│   ├── 📄 README.md
│   ├── 📄 references.bib
│   └── 📄 author-mappings.json
│
├── 📁 data/                               # DATEN
│   ├── 📄 README.md
│   └── 📁 validation/
│
├── 📁 scripts/                            # CODE
│   ├── 📄 README.md
│   └── 📁 llm-monte-carlo/
│
├── 📁 quality/                            # QUALITÄTSSICHERUNG
│   ├── 📄 README.md
│   └── 📄 checklist.md
│
├── 📁 templates/                          # VORLAGEN
│   ├── 📄 README.md
│   └── 📄 *.docx, *.tex
│
└── 📁 examples/                           # BEISPIELE
    ├── 📄 README.md
    └── 📁 case-studies/
```

---

## 📛 Namenskonventionen

### Dateien

| Typ | Muster | Beispiel |
|-----|--------|----------|
| Meta-Frameworks | `00_[name]_framework.tex` | `00_master_documentation_framework.tex` |
| Templates | `00_[type]_template.tex` | `00_appendix_template.tex` |
| Kapitel | `[NN]_[name].tex` | `05_complementarity.tex` |
| Subkapitel | `[NN]_[N]_[name].tex` | `10_2_fepsde_dimensions.tex` |
| Appendices | `appendix_[CODE]_[name].tex` | `appendix_B_complementarity.tex` |
| PDFs | `complementarity_context_v[NN].pdf` | `complementarity_context_v51.pdf` |
| Markdown | `[name].md` (kebab-case) | `writing-chapters.md` |

### Appendix-Codes

```
CORE:    AAA (WHO), B (HOW), C (WHAT), V (WHEN), BBB (WHERE), AU (AWARE), AV (READY)
FORMAL:  A, D
DOMAIN:  AA-AK, W-Z
CONTEXT: AH, AI
METHOD:  AL, AN, E, R
PREDICT: AO-AT, S
LIT:     I-Q, U
REF:     F, G, H, T
```

### Ordner

| Typ | Konvention | Beispiel |
|-----|------------|----------|
| Hauptordner | lowercase | `chapters/`, `appendices/` |
| Unterordner | lowercase, kebab-case | `case-studies/`, `llm-monte-carlo/` |
| Legacy/Archiv | `legacy/` Unterordner | `chapters/legacy/` |

---

## 📚 Dokumentations-Hierarchie

### README.md pro Ebene

```
ROOT/README.md
├── Repository-Überblick
├── Schnellstart
├── Ordnerstruktur (Übersicht)
├── Aktuelle Version
├── Links zu wichtigen Dokumenten
└── Kontakt/Lizenz

chapters/README.md
├── Kapitel-Übersicht (Tabelle)
├── Teil-Struktur (I-VI)
├── Wie man ein Kapitel schreibt
├── Template-Verweis
└── Verbindung zu Appendices

appendices/README.md
├── Appendix-Übersicht (nach Kategorie)
├── CORE-Anforderungen
├── Wie man einen Appendix schreibt
├── Template-Verweis
└── Kapitel-Mapping

docs/README.md
├── Dokumentations-Übersicht
├── Framework-Dokumentation
├── Anleitungen
└── Nachschlagewerke
```

---

## 📝 README-Struktur pro Ordner

### Template: Hauptordner-README

```markdown
# [Ordnername]

> [Einzeilige Beschreibung]

## Übersicht

[2-3 Sätze was dieser Ordner enthält]

## Inhalt

| Datei/Ordner | Beschreibung |
|--------------|--------------|
| `file.tex`   | Beschreibung |
| `folder/`    | Beschreibung |

## Struktur

[Relevante Strukturinformation, z.B. Kapitel-Übersicht]

## Verwendung

[Wie man mit diesem Inhalt arbeitet]

## Verwandte Dokumente

- [Link zu verwandtem Dokument](path)
- [Link zu Template](path)

## Status

[Aktueller Bearbeitungsstand, falls relevant]
```

---

## 🔢 Versionierung

### Dokument-Versionen

```
Format: v[MAJOR].[MINOR] oder v[NUMBER]

v51     = Hauptversion 51
v51.1   = Minor Update zu v51
```

### Wann Version erhöhen?

| Änderung | Version |
|----------|---------|
| Neue Kapitel/Appendices | +1 Major |
| Strukturelle Änderungen | +1 Major |
| Inhaltliche Ergänzungen | +0.1 Minor |
| Korrekturen/Typos | Keine Erhöhung |

### CHANGELOG.md Format

```markdown
# Changelog

## [v51] - 2026-01-06

### Added
- Master Documentation Framework
- Document Specification Framework

### Changed
- Appendix Template erweitert um CORE-Anforderungen

### Fixed
- Typos in Chapter 5
```

---

## 💬 Commit-Konventionen

### Format

```
[TYPE] [SCOPE]: [Beschreibung]

[Optionaler Body mit Details]
```

### Types

| Type | Verwendung |
|------|------------|
| `Create` | Neue Datei erstellt |
| `Update` | Bestehende Datei aktualisiert |
| `Add` | Inhalt hinzugefügt |
| `Fix` | Fehler korrigiert |
| `Refactor` | Struktur geändert ohne Inhaltsänderung |
| `Docs` | Nur Dokumentation |
| `Meta` | Repository-Konfiguration |

### Scope

```
chapters/     → Ch. [N]
appendices/   → App. [CODE]
docs/         → Docs
root          → Root
```

### Beispiele

```
Create Ch. 5: Add complementarity chapter

Update App. B: Extend axiom system to 15 axioms

Add comprehensive literature review section with 80+ references

Fix Ch. 10.2: Correct equation numbering

Docs: Add writing guide for appendices

Meta: Update README with new structure
```

### Längere Commits

```
Create EBF Master Documentation Framework

INTEGRATED META-FRAMEWORK: From Idea to Document in 5 Steps

Step 1: SPECIFICATION (12 Dimensions)
Step 2: FORMAT DERIVATION
Step 3: ARCHITECTURE (Main vs Appendix)
Step 4: SCOPE DETERMINATION
Step 5: STRUCTURE

Includes:
- Complete 12-Dimension System
- Format Taxonomy (16 formats)
- Master Specification Card
- Quick Reference Trees
```

---

## 🔗 Verlinkungen

### Interne Links in Markdown

```markdown
Siehe [Master Framework](../00_master_documentation_framework.tex)
Siehe [Kapitel 5](../chapters/05_complementarity.tex)
Siehe [Appendix UNMAPPED_HOW](../appendices/appendix_B_complementarity.tex)
```

### Referenzen in LaTeX

```latex
Siehe Appendix~
ef{app:HOW} (CORE-HOW) für Details.
Die formale Ableitung findet sich in Kapitel~\ref{sec:complementarity}.
```

---

## ✅ Checkliste: Neue Datei hinzufügen

- [ ] Dateiname folgt Konvention
- [ ] In korrektem Ordner platziert
- [ ] README.md des Ordners aktualisiert
- [ ] Commit-Message folgt Konvention
- [ ] Bei Kapitel/Appendix: Template verwendet
- [ ] Bei CORE-Appendix: 7 Anforderungen geprüft
- [ ] Verlinkungen korrekt
- [ ] Version in Dokument aktualisiert (falls relevant)

---

## 📊 Dokumentations-Matrix

| Was | Wo | Format |
|-----|-----|--------|
| Repository-Übersicht | `/README.md` | Markdown |
| Meta-Frameworks | `/00_*.tex` | LaTeX |
| Kapitel-Übersicht | `/chapters/README.md` | Markdown |
| Appendix-Übersicht | `/appendices/README.md` | Markdown |
| Framework-Docs | `/docs/frameworks/` | Markdown |
| Anleitungen | `/docs/guides/` | Markdown |
| Glossar | `/docs/references/glossary.md` | Markdown |
| CHANGELOG | `/CHANGELOG.md` | Markdown |
| Beitragsrichtlinien | `/CONTRIBUTING.md` | Markdown |

---

*Letzte Aktualisierung: Januar 2026*
