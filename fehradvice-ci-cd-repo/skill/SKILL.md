---
name: fehradvice-docx
description: Generate professional Word documents (.docx) in FehrAdvice & Partners AG Corporate Design. Use when creating proposals, reports, presentations, or any professional document for FehrAdvice. Triggers on requests mentioning FehrAdvice documents, proposals, reports, CI/CD-compliant documents, or "erstelle ein Dokument/Proposal/Bericht im FehrAdvice-Stil". Includes logos, color palette, typography, standard boilerplate sections (Über FehrAdvice, Kontakt), and the complete document architecture.
---

# FehrAdvice DOCX Generator

Generate professional FehrAdvice & Partners AG documents using `docx` (npm).

## Quick Start

1. Install: `npm install docx`
2. Copy and adapt `scripts/create_fehradvice_docx.js`
3. Logos are in `assets/logo_full.png` and `assets/logo_icon.png`

## Assets

- `assets/logo_full.png` — Full logo (icon + "FEHR ADVICE"), for cover page (right-aligned)
- `assets/logo_icon.png` — Kartenfächer icon only, for document header

## References

- `references/cicd-specs.md` — Complete CI/CD specifications (colors, typography, layout)
- `references/boilerplate-de.md` — Standard German text blocks (Über FehrAdvice, Kontakt, Nutzen-Box format)

## Document Types

| Type | Structure |
|------|-----------|
| **Proposal** | Cover → TOC → Ausgangslage → Phasen (Ziel/Inhalte/Nutzen-Box) → Nächster Schritt → Kontakt → Über FehrAdvice |
| **Report** | Cover → TOC → Executive Summary → Kapitel → Fazit → Über FehrAdvice → Appendix |
| **Brief/Memo** | Cover → Inhalt → Kontakt → Über FehrAdvice |

## Key CI/CD Rules

- Font: Calibri (sans-serif fallback), justified body text
- Colors: Navy #1B365D (headings/header), #1A1A1A (body), white background
- Logo: Top-right on cover (full); icon-only in header on content pages
- Nutzen-Box: #F2F4F7 background, navy top border, 👍 icon, bullet points
- Gendersensible Sprache: Kund:innen, Mitarbeiter:innen
- Bold inline key terms for emphasis
- "Über FehrAdvice" boilerplate: Always as standard closing section
- Kontakt: Always with relevant team members

## Script Structure

`scripts/create_fehradvice_docx.js` contains:
1. **Constants** — Colors, fonts, margins (do not change)
2. **Helpers** — h1(), h2(), para(), makeTable(), nutzenBox(), uberFehrAdvice(), kontakt()
3. **Content** — Adapt per document
4. **Assembly** — Headers, footers, page setup, output
