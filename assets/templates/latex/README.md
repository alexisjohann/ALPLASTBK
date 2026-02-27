# FehrAdvice LaTeX Templates

> Offizielle LaTeX-Vorlagen basierend auf dem FehrAdvice Corporate Identity Guide

**Quelle:** Corporate-Identity-Guide-FAP-EN-231007 2.pdf

---

## 📁 Dateien

| Datei | Beschreibung |
|-------|--------------|
| `fehradvice-report.cls` | Hauptdokumentklasse für Reports |
| `fehradvice-colors.sty` | Farbdefinitionen (Primär + Sekundär) |
| `fehradvice-fonts.sty` | Schriftarten (Roboto, Open Sans, Playfair Display) |
| `example-report.tex` | Beispieldokument mit allen Features |

---

## 🚀 Verwendung

### Basis-Setup

```latex
\documentclass{fehradvice-report}

\title{Report Title}
\subtitle{Subtitle}
\author{FehrAdvice \& Partners AG}
\date{Januar 2026}

\begin{document}
\maketitle
\tableofcontents

\section{Einleitung}
...

\end{document}
```

### Kompilieren

**Wichtig:** Verwende XeLaTeX oder LuaLaTeX für korrekte Schriftarten:

```bash
xelatex example-report.tex
```

Oder mit latexmk:

```bash
latexmk -xelatex example-report.tex
```

---

## 🎨 Farbpalette

### Verwendung in LaTeX

```latex
\textcolor{fadarkblue}{Dunkelblauer Text}
\textcolor{falightblue}{Hellblauer Text}
\textcolor{fadarkgray}{Dunkelgrauer Text}

% Hintergrund
\colorbox{falightgray}{Grauer Hintergrund}
```

### Verfügbare Farben

| Name | Alias | HEX | Verwendung |
|------|-------|-----|------------|
| `fadarkblue` | `faprimary` | `#024079` | Headlines, Akzente |
| `falightblue` | `fasecondary` | `#549EDE` | Sekundäre Elemente |
| `fadarkgray` | `fatext` | `#25212A` | Fliesstext |
| `falightgray` | `fabackground` | `#F3F5F7` | Hintergründe |
| `falilac` | - | `#A1A0C6` | Diagramme |
| `famint` | - | `#7EBDAC` | Diagramme |
| `faocher` | - | `#DECB3F` | Hervorhebungen |
| `faorange` | - | `#DE9D3E` | Warnungen |

---

## 📝 Typografie

### Schriftarten

| Element | Font | Fallback |
|---------|------|----------|
| Headlines | Roboto Bold | Arial Bold |
| Subheadlines | Roboto Regular | Arial |
| Fliesstext | Open Sans | Arial |
| Akzente | Playfair Display | Georgia |
| Code | Inconsolata | Consolas |

### Akzent-Befehle

```latex
% Playfair Display für Akzente
\faaccent{Akzenttext}

% Schweizer Anführungszeichen
\faquote{Zitat mit « »}
```

---

## 📦 Boxen

### Info-Box (Blau)

```latex
\begin{fainfobox}[Titel]
Inhalt der Info-Box
\end{fainfobox}
```

### Warnung-Box (Orange)

```latex
\begin{fawarningbox}[Achtung]
Wichtiger Hinweis
\end{fawarningbox}
```

### Erfolg-Box (Mintgrün)

```latex
\begin{fasuccessbox}[Ergebnis]
Erfolgreiche Nachricht
\end{fasuccessbox}
```

### Zitat-Box

```latex
\begin{faquotebox}
Zitat in Playfair Display
\end{faquotebox}
```

---

## 📊 Tabellen

### FehrAdvice-Tabellenstil

```latex
\begin{tabular}{lll}
\toprule
\rowcolor{fadarkblue}
\fahead{Spalte 1} & \fahead{Spalte 2} & \fahead{Spalte 3} \\
\midrule
\rowcolor{fawhite}
Zeile 1 & Wert & Wert \\
\rowcolor{falightgray}
Zeile 2 & Wert & Wert \\
\bottomrule
\end{tabular}
```

---

## 🔢 Zahlenformat

Schweizer Format mit Apostroph (1'000.00):

```latex
\num{1250000.00}  % → 1'250'000.00
\num{12500}       % → 12'500
```

---

## 📋 Metadata

```latex
\client{Kundenname AG}
\project{Projektname}
\version{1.0}
\classification{Confidential}
```

---

## ⚠️ Hinweise

### Font-Installation

Die Schriftarten müssen auf dem System installiert sein:

- **Roboto**: [fonts.google.com/specimen/Roboto](https://fonts.google.com/specimen/Roboto)
- **Open Sans**: [fonts.google.com/specimen/Open+Sans](https://fonts.google.com/specimen/Open+Sans)
- **Playfair Display**: [fonts.google.com/specimen/Playfair+Display](https://fonts.google.com/specimen/Playfair+Display)

### pdfLaTeX Fallback

Bei Verwendung von pdfLaTeX (ohne fontspec) wird automatisch Helvetica als Fallback verwendet. Für korrekte Fonts immer XeLaTeX oder LuaLaTeX verwenden.

---

*Referenz: Appendix SG (REF-STYLE) | Version 1.0 | Januar 2026*
