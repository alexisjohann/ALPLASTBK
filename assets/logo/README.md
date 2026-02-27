# Logo Assets

> Alle Logo-Varianten von FehrAdvice & Partners AG

**Quelle:** Extrahiert aus `assets/Corporate-Identity-Guide-FAP-EN-231007 2.pdf`

---

## 🎨 Logo-Farben

| Element | Farbe | HEX |
|---------|-------|-----|
| Symbol (Schlussstein) | Dunkelblau | `#024079` |
| Wortmarke | Dunkelblau | `#024079` |
| Tagline | Dunkelblau | `#024079` |

---

## 📁 Ordnerstruktur

```
logo/
├── color/                              # Vollfarbe auf weissem/hellem Hintergrund
│   ├── fehradvice-logo-2lines.png            ✅ EMPFOHLEN (isoliertes Logo, 300 DPI)
│   ├── fehradvice-schlussstein-symbol.svg    ⚠️ Komplette PDF-Seite
│   ├── fehradvice-schlussstein-symbol.png    ⚠️ Komplette PDF-Seite
│   ├── fehradvice-logo-color-tagline.svg     ⚠️ Komplette PDF-Seite
│   ├── fehradvice-logo-color-tagline.png     ⚠️ Komplette PDF-Seite
│   └── [weitere Seiten-Exports]
│
├── monochrome/                         # Einfarbige Varianten
│   ├── fehradvice-logo-white.png             ✅ Generiert
│   ├── fehradvice-logo-variants.svg          ✅ Extrahiert
│   └── fehradvice-logo-variants.png          ✅ Extrahiert (300 DPI)
│
├── favicon/                            # Favicons für Web
│   ├── favicon.ico                           ✅ Generiert (16/32/48)
│   ├── favicon-16x16.png                     ✅ Generiert
│   ├── favicon-32x32.png                     ✅ Generiert
│   ├── favicon-48x48.png                     ✅ Generiert
│   ├── favicon-180x180.png                   ✅ Generiert (Apple Touch)
│   └── favicon-512x512.png                   ✅ Generiert (PWA)
│
├── social/                             # Social Media Profilbilder
│   └── fehradvice-profile-square.png         ✅ Generiert (400x400)
│
└── extracted/                          # Rohdaten (alle 21 Seiten als SVG)
    ├── page-1.svg ... page-21.svg            ✅ Vollständig extrahiert
```

---

## ⚠️ WICHTIG: Empfohlenes Logo für Templates

**Für alle Cover/Back-Templates dieses Logo verwenden:**

```
assets/logo/color/fehradvice-logo-2lines.png
```

**Spezifikation:**
- Variante: "Large, 2 lines" (FEHR / ADVICE ohne Tagline)
- Grösse: 1133 × 272 Pixel
- Auflösung: 300 DPI
- Extrahiert aus: CI-Guide Seite 8

**⚠️ Achtung:** Die anderen PNG/SVG-Dateien sind komplette PDF-Seiten aus dem
CI-Guide, NICHT isolierte Logos! Sie sind >1MB gross und enthalten zusätzlichen
Text und Layout-Elemente.

---

## 📏 Mindestgrössen

| Medium | Mindestbreite |
|--------|---------------|
| Print | 25 mm |
| Digital | 100 px |
| Favicon | 16 × 16 px |

---

## 🚫 Logo Don'ts

- ❌ Nicht strecken oder verzerren
- ❌ Nicht drehen oder kippen
- ❌ Nicht in nicht-definierten Farben darstellen
- ❌ Nicht auf unruhigen Hintergründen platzieren
- ❌ Nicht mit Schatten oder Effekten versehen
- ❌ Mindestabstand (Höhe des «F») immer einhalten

---

## ✅ Extrahierte Dateien (Januar 2026)

### Priorität 1 (Kritisch)
- [x] `color/fehradvice-schlussstein-symbol.svg` - Schlussstein-Symbol
- [x] `color/fehradvice-schlussstein-symbol.png` - Schlussstein (300 DPI)
- [x] `color/fehradvice-logo-color-tagline.svg` - Logo mit Tagline
- [x] `monochrome/fehradvice-logo-white.png` - Weisses Logo
- [x] `favicon/favicon.ico` - Multi-Resolution Favicon

### Priorität 2 (Wichtig)
- [x] `color/fehradvice-logo-color-tagline.png` - Logo mit Tagline (300 DPI)
- [x] `favicon/favicon-180x180.png` - Apple Touch Icon
- [x] `social/fehradvice-profile-square.png` - Social Media (400x400)
- [x] `monochrome/fehradvice-logo-variants.svg` - Alle Varianten (Seite 6)

### Rohdaten
- [x] `extracted/page-*.svg` - Alle 21 Seiten als Vektor

---

## 🔧 Extraktions-Methode

Die Logos wurden mit folgenden Tools aus dem CI Guide PDF extrahiert:

```bash
# PDF → SVG (alle Seiten)
pdf2svg "Corporate-Identity-Guide-FAP-EN-231007 2.pdf" extracted/page-%d.svg all

# SVG → PNG (300 DPI)
inkscape input.svg --export-filename=output.png --export-dpi=300

# Favicons (verschiedene Grössen)
inkscape input.svg --export-filename=output.png --export-width=SIZE --export-height=SIZE

# ICO (Multi-Resolution)
convert favicon-16x16.png favicon-32x32.png favicon-48x48.png favicon.ico
```

---

*Referenz: Appendix SG §5 (Logo) | Extrahiert: Januar 2026*
