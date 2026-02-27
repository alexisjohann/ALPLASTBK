# FehrAdvice CI/CD Repository

> Corporate Identity & Corporate Design Automatisierung fuer FehrAdvice & Partners AG

---

## Zweck

Dieses Repository enthaelt alle Ressourcen fuer die automatisierte Erstellung von FehrAdvice-konformen Dokumenten:

- **Corporate Identity Spezifikationen** (Farben, Fonts, Logos)
- **Boilerplate-Texte** (Deutsch/Englisch)
- **Automatisierungsskripte** (DOCX-Generierung)
- **Vorlagen** (Proposals, Reports, Praesentationen)

## Struktur

```
fehradvice-ci-cd-repo/
├── README.md                              ← Du bist hier
├── CHANGELOG.md                           ← Versionshistorie
├── skill/
│   ├── SKILL.md                           ← Skill-Definition (Claude Code)
│   ├── scripts/create_fehradvice_docx.js  ← DOCX-Generierungsskript
│   ├── references/boilerplate-de.md       ← Boilerplate-Texte (DE)
│   ├── references/cicd-specs.md           ← CI/CD Spezifikationen
│   └── assets/                            ← Logos (PNG)
├── docs/
│   ├── fehradvice-ci-cd-analysis.md       ← CI/CD Analyse (Markdown)
│   └── fehradvice-ci-cd-analysis.docx     ← CI/CD Analyse (Word)
└── examples/
    └── beispiel-proposal-template.docx    ← Beispiel-Vorlage
```

## Schnellstart

```bash
# DOCX generieren
node skill/scripts/create_fehradvice_docx.js --template proposal --output output.docx

# Skill in Claude Code verwenden
# /fehradvice-doc --type proposal --lang de
```

## Farben (Quick Reference)

| Farbe | Hex | Verwendung |
|-------|-----|------------|
| Dunkelblau | `#024079` | Headlines, Links, Akzente |
| Hellblau | `#549EDE` | Sekundaere Elemente |
| Dunkelgrau | `#25212A` | Fliesstext |
| Hellgrau | `#F3F5F7` | Hintergruende, Tabellen |

## Fonts

| Font | Verwendung |
|------|------------|
| Roboto Bold | H1, H2 Headlines |
| Roboto Regular | H3, H4 Subheadlines |
| Open Sans | Fliesstext, Tabellen |
| Playfair Display | Akzente, Zitate |

## Verwandte Ressourcen

- **Corporate Style Guide (SSOT):** `appendices/REF-STYLE_SG_corporate_style_guide.tex`
- **Prio Swiss CI/CD:** `data/customers/prio-swiss/ci-cd/`
- **Document Production Skill:** `.claude/commands/document-production.md`

---

*FehrAdvice & Partners AG | 2026*
