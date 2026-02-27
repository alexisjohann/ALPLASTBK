# Document Templates

> Vorlagen für alle FehrAdvice-Dokumente

---

## 📁 Template-Typen

| Ordner | Verwendung | Format |
|--------|------------|--------|
| `powerpoint/` | Präsentationen | .pptx |
| `word/` | Reports, Briefe, Memos | .dotx, .docx |
| `latex/` | Wissenschaftliche Reports | .cls, .sty, .tex |
| `email/` | E-Mail-Signaturen | .html |
| `excel/` | Tabellen, Kalkulationen | .xlsx |

---

## 📊 PowerPoint Templates

```
powerpoint/
├── FehrAdvice-Master.pptx           # Haupt-Template
├── FehrAdvice-Slides-Library.pptx   # Folien-Bibliothek
└── README.md
```

**Enthält:**
- Titelfolie (Dunkelblau Hintergrund, weisse Schrift)
- Inhaltsfolie (1/2/3 Spalten)
- Trennfolie (Hellblau/Hellgrau)
- Diagramm-Folie
- Tabellen-Folie
- Schlussfolie

**Format:** 16:9 (Widescreen)

---

## 📝 Word Templates

```
word/
├── FehrAdvice-Report.dotx           # Report-Template
├── FehrAdvice-Letter.dotx           # Brief-Template
├── FehrAdvice-Memo.dotx             # Memo-Template
├── FehrAdvice-Proposal.dotx         # Angebots-Template
└── README.md
```

---

## 📄 LaTeX Templates

```
latex/
├── fehradvice-report.cls            # Report-Dokumentklasse
├── fehradvice-colors.sty            # Farbdefinitionen
├── fehradvice-fonts.sty             # Font-Setup
├── fehradvice-tables.sty            # Tabellen-Styling
├── example-report.tex               # Beispiel-Dokument
└── README.md
```

**LaTeX-Farbdefinitionen:**
```latex
\definecolor{primarydarkblue}{RGB}{2,64,121}
\definecolor{primarylightblue}{RGB}{84,158,222}
\definecolor{primarydarkgray}{RGB}{37,33,42}
\definecolor{primarylightgray}{RGB}{243,245,247}  % Korrigiert
\definecolor{secondarylilac}{RGB}{161,160,198}
\definecolor{secondarymint}{RGB}{126,189,172}
\definecolor{secondaryocher}{RGB}{222,203,63}
\definecolor{secondaryorange}{RGB}{222,157,62}
```

**Offizielle Fonts (aus CI Guide Oktober 2023):**
| Verwendung | Schriftart | Download |
|------------|------------|----------|
| Headlines | Roboto Bold | fonts.google.com/specimen/Roboto |
| Body | Open Sans | fonts.google.com/specimen/Open+Sans |
| Akzente | Playfair Display | fonts.google.com/specimen/Playfair+Display |

---

## 📧 E-Mail-Signatur

```
email/
├── signature-de.html                # Deutsche Version
├── signature-en.html                # English Version
├── signature-plain.txt              # Plain Text Fallback
└── README.md
```

**Struktur:**
```
Mit freundlichen Grüssen

[Vorname Nachname]
[Funktion]

FehrAdvice & Partners AG
[Strasse], [PLZ Ort]
Tel: +41 XX XXX XX XX
[email]@fehradvice.com
www.fehradvice.com
```

---

## 📈 Excel Templates

```
excel/
├── FehrAdvice-Data-Template.xlsx    # Daten-Template
├── FehrAdvice-Chart-Template.xlsx   # Diagramm-Template
└── README.md
```

**Farben für Excel:**
- Kopfzeilen: RGB(2,64,121)
- Alternating Rows: RGB(245,245,245)
- Akzente: RGB(84,158,222)

---

## ✅ Benötigte Templates

### Priorität 1 (Kritisch)
- [ ] `powerpoint/FehrAdvice-Master.pptx`
- [ ] `latex/fehradvice-report.cls`
- [ ] `email/signature-de.html`

### Priorität 2 (Wichtig)
- [ ] `word/FehrAdvice-Report.dotx`
- [ ] `word/FehrAdvice-Letter.dotx`
- [ ] `excel/FehrAdvice-Data-Template.xlsx`

---

*Referenz: Appendix SG §2-4 (Typografie, Layout, Visuelle Elemente)*
