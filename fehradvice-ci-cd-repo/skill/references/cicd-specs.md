# FehrAdvice CI/CD Specifications

## Colors

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | Dunkel-Navy | #1B365D | Headings, header, cover block, table headers |
| Secondary | Petrol/Teal | #2A7F8E | Logo icon, accents |
| Accent (Slides) | Orange/Amber | #E8A33D | Arrows, conclusions (slides only) |
| Accent (Docs) | Navy-Blau | #1B365D | Nutzen-Boxen, phase headers |
| Background | Weiss | #FFFFFF | Content pages |
| Text Primary | Schwarz | #1A1A1A | Body text (documents) |
| Text Headings | Dunkel-Navy | #1B365D | Chapter headings |
| Text Secondary | Mittelgrau | #6B7280 | Footers, page numbers |
| Nutzen-Box BG | Hellgrau | #F2F4F7 | Nutzen-Box background |

## Typography (Documents/Proposals)

| Element | Font | Size | Style |
|---------|------|------|-------|
| Deckblatt-Titel | Calibri | 28–32 pt | Bold, Uppercase, White on Navy |
| Kapitelüberschrift (H1) | Calibri | 22–26 pt | Bold, Uppercase, Navy |
| Phasen-Überschrift (H2) | Calibri | 12–14 pt | Bold, Navy |
| Fliesstext | Calibri | 10–11 pt | Regular, Black, Justified |
| Fussnote/Footer | Calibri | 8–9 pt | Regular, Gray |
| Nutzen-Box Text | Calibri | 10 pt | Regular, bullets |

## Layout Rules

- Page: A4 portrait, margins 2.5cm (top/bottom), 2.5cm (left/right)
- Logo cover: Right-aligned, above navy block
- Logo header: Icon-only, top-right corner, small (28px)
- Header text: "FEHRADVICE & PARTNERS AG" + context, right-aligned, 7pt gray
- Footer: Centered page number "Seite X"
- Body: Justified (Blocksatz)
- Key terms: Bold inline within sentences
- Nutzen-Box: Full-width gray box, navy top border 2pt, 👍 icon, bullet list
- Phase structure: "Phase N: Titel" → "Ziel:" → "Inhalte:" numbered → Nutzen-Box
- Page breaks: Before each major chapter (H1)

## Document Architecture

### Cover Page
- Logo (full) right-aligned, top
- Navy separator lines
- Title (large, bold)
- Subtitle
- Source/client info
- Date
- "FehrAdvice & Partners AG"

### TOC (Inhaltsverzeichnis)
- Manual, not auto-generated
- H1 entries bold with number
- H2 entries indented, regular weight
- Generous whitespace

### Content Pages
- H1 with page break before
- H2 for subsections
- Body text justified
- Tables with navy header row, white text
- Nutzen-Box for benefits

### Standard Closing
1. "Der nächste Schritt" (optional, for proposals)
2. "Kontakt" with team members
3. "Über FehrAdvice & Partners" boilerplate
4. Appendix (if applicable)
