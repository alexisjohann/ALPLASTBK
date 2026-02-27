# FehrAdvice Brand Assets

> Single Source of Truth für alle visuellen Assets von FehrAdvice & Partners AG

**Referenz:** Appendix SG (REF-STYLE) - FehrAdvice Corporate Style Guide

---

## 📁 Ordnerstruktur

```
assets/
├── logo/                    # Logo-Dateien (alle Varianten)
│   ├── color/               # Vollfarbe (Dunkelblau #024079)
│   ├── monochrome/          # Einfarbig (Dunkel, Weiss, Schwarz)
│   ├── favicon/             # Favicons (16x16 bis 180x180)
│   └── social/              # Social Media Profilbilder
│
├── templates/               # Dokumentvorlagen
│   ├── powerpoint/          # PPT Master-Templates
│   ├── word/                # Word/DOCX Templates
│   ├── latex/               # LaTeX Templates mit CI/CD
│   ├── email/               # E-Mail-Signaturen
│   └── excel/               # Excel/Sheets Templates
│
├── icons/                   # Icon-Bibliothek
│   ├── general/             # Allgemeine Icons
│   └── behavioral-economics/ # BE-spezifische Icons
│
├── images/                  # Bildmaterial
│   ├── photos/              # Genehmigte Fotos
│   ├── illustrations/       # Illustrationen
│   └── examples/            # Beispiele (Do's/Don'ts)
│
├── social-media/            # Social Media Assets
│   ├── linkedin/            # LinkedIn Banner & Posts
│   ├── twitter/             # Twitter/X Assets
│   └── instagram/           # Instagram Assets
│
├── business-materials/      # Geschäftsausstattung
│   ├── letterhead/          # Briefpapier
│   ├── business-cards/      # Visitenkarten
│   └── envelopes/           # Umschläge
│
├── infographics/            # Infografik-Templates
│   ├── process/             # Prozess-Diagramme
│   ├── comparison/          # Vergleichs-Matrizen
│   ├── timeline/            # Zeitleisten
│   └── hierarchy/           # Organigramme
│
├── graphics/                # Auto-generierte Grafiken (NEU)
│   ├── chart-templates/     # Wiederverwendbare Chart-Vorlagen
│   └── generated/           # Session-spezifische Grafiken
│       └── {session_id}/    # Pro Session ein Ordner
│
├── illustrations/           # Konzept-Illustrationen (NEU)
│   ├── concepts/            # Brain, Network, Complexity
│   ├── icons/               # SVG-Icons für Slides
│   └── backgrounds/         # Hintergrund-Grafiken
│
└── logos/                   # Logos für PPTX (NEU)
    ├── fehradvice_logo.png      # Standard-Logo
    ├── fehradvice_logo_white.png # Logo für dunklen Hintergrund
    └── ebf_logo.png             # EBF Framework Logo
```

---

## 🎨 Farbpalette (Quick Reference)

### Primärfarben

| Farbe | HEX | RGB | Verwendung |
|-------|-----|-----|------------|
| Dunkelblau | `#024079` | RGB(2,64,121) | Headlines, Logo, Akzente |
| Hellblau | `#549EDE` | RGB(84,158,222) | Sekundäre Elemente |
| Dunkelgrau | `#25212A` | RGB(37,33,42) | Fliesstext |
| Hellgrau | `#F3F5F7` | RGB(243,245,247) | Hintergründe |

### Sekundärfarben

| Farbe | HEX | RGB | Verwendung |
|-------|-----|-----|------------|
| Flieder | `#A1A0C6` | RGB(161,160,198) | Akzente, Diagramme |
| Mintgrün | `#7EBDAC` | RGB(126,189,172) | Akzente, Diagramme |
| Ocker | `#DECB3F` | RGB(222,203,63) | Hervorhebungen |
| Orange | `#DE9D3E` | RGB(222,157,62) | Warnungen, CTA |

---

## 📝 Typografie

> **Quelle:** Corporate-Identity-Guide-FAP-EN-231007 2.pdf, Seite 11

| Verwendung | Schriftart | Fallback | Download |
|------------|------------|----------|----------|
| Headlines | **Roboto Bold** | Arial Bold | [fonts.google.com](https://fonts.google.com/specimen/Roboto) |
| Subheadlines | Roboto Regular | Arial | [fonts.google.com](https://fonts.google.com/specimen/Roboto) |
| Fliesstext | **Open Sans** | Arial | [fonts.google.com](https://fonts.google.com/specimen/Open+Sans) |
| Akzente/Zitate | **Playfair Display** | Georgia | [fonts.google.com](https://fonts.google.com/specimen/Playfair+Display) |
| Code | Consolas | Monaco | - |

---

## ✅ Asset-Checkliste

### Logo (P1 - Kritisch)
- [ ] `logo/color/fehradvice-logo-color.svg`
- [ ] `logo/color/fehradvice-logo-color.png` (300dpi)
- [ ] `logo/color/fehradvice-logo-color-tagline.svg`
- [ ] `logo/monochrome/fehradvice-logo-white.svg`
- [ ] `logo/monochrome/fehradvice-logo-black.svg`
- [ ] `logo/favicon/favicon-16x16.png`
- [ ] `logo/favicon/favicon-32x32.png`
- [ ] `logo/favicon/favicon-180x180.png`
- [ ] `logo/favicon/favicon.ico`
- [ ] `logo/social/fehradvice-profile-square.png` (400x400)

### Templates (P1 - Kritisch)
- [ ] `templates/powerpoint/FehrAdvice-Master.pptx`
- [ ] `templates/latex/fehradvice-report.cls`
- [ ] `templates/word/FehrAdvice-Report.dotx`
- [ ] `templates/email/signature.html`

### Icons (P2)
- [ ] `icons/behavioral-economics/nudge.svg`
- [ ] `icons/behavioral-economics/loss-aversion.svg`
- [ ] `icons/behavioral-economics/social-norms.svg`
- [ ] `icons/behavioral-economics/default-effect.svg`

---

## 📐 Datei-Namenskonvention

```
[marke]-[typ]-[variante]-[größe].[format]

Beispiele:
fehradvice-logo-color.svg
fehradvice-logo-white-tagline.svg
fehradvice-icon-nudge-24x24.svg
fehradvice-template-report.pptx
```

---

## 🔗 Verweise

- **Style Guide:** `appendices/REF-STYLE_SG_corporate_style_guide.tex`
- **Dokumentation:** `docs/frameworks/appendix-category-definitions.md`
- **8D-Algorithmus:** `appendices/CCC_method_doctype.tex`

---

## 📊 Automatische PPTX-Generierung (NEU v1.19)

### Grafik-Generierung

Generiere alle Charts für eine Session:

```bash
python scripts/generate_graphics.py --session EBF-S-2026-01-26-COG-001
```

Erzeugt in `assets/graphics/generated/{session_id}/`:
- `cognitive_hierarchy_bar.png` - Horizontales Balkendiagramm
- `v_n_decay_line.png` - Liniendiagramm V(n)
- `sensitivity_donut.png` - Donut-Chart Sensitivität
- `formula.png` - LaTeX-Formel als PNG

### PPTX-Generierung

Generiere komplette Präsentation:

```bash
# Für Board-Meeting (5-7 Slides, wenig Zeit)
python scripts/generate_pptx.py --session EBF-S-2026-01-26-COG-001 --audience board

# Für Wissenschaft (18-25 Slides, viel Zeit)
python scripts/generate_pptx.py --session EBF-S-2026-01-26-COG-001 --audience science

# Mit automatischer Grafik-Generierung
python scripts/generate_pptx.py --session EBF-S-2026-01-26-COG-001 --audience board --generate-graphics
```

### Verfügbare Zielgruppen (8D-Profile)

| Profil | Slides | Beschreibung |
|--------|--------|--------------|
| `board` | 5-7 | C-Level, strategisch, wenig Zeit |
| `management` | 8-12 | Geschäftsleitung, operativ |
| `team` | 12-18 | Projektteam, technisch |
| `science` | 18-25 | Wissenschaft, Paper-Qualität |
| `client` | 8-12 | Externer Kunde, überzeugend |

### Konfiguration

| Datei | Zweck |
|-------|-------|
| `templates/pptx/fa-style.yaml` | Farben, Fonts, Layouts |
| `templates/pptx/slide-types.yaml` | Slide-Definitionen |
| `templates/pptx/8d-slide-mapping.yaml` | Zielgruppen → Slides |
| `templates/pptx/graphic-mapping.yaml` | Daten → Charts |

---

*FehrAdvice & Partners AG – Stand: Januar 2026*
