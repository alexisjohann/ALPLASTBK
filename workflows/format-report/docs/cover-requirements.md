# FehrAdvice Cover Sheet - Design Requirements

## SSOT für Cover-Design
**Quelle:** Referenz-Bild vom User (2026-01-29)
**Template:** `templates/fehradvice-cover.latex`

---

## Layout-Struktur

```
┌─────────────────────────────────────────────────────────────┐
│ WEISS (ca. 2.5cm)                            [LOGO rechts] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ DUNKELBLAU (#024079)                                        │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
│   TITEL                     ← Weiss, Bold, 32pt, links      │
│                                                             │
│   Untertitel                ← Weiss, Regular, 16pt, links   │
│                                                             │
│   FehrAdvice & Partners AG  ← Weiss, Regular, 12pt, links   │
│   Monat Jahr                ← Weiss, Regular, 12pt, links   │
│                                                             │
│                                                             │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Farbspezifikation

| Element | Farbe | RGB | Hex |
|---------|-------|-----|-----|
| Header-Bereich | Weiss | 255,255,255 | #FFFFFF |
| Hauptbereich | Dunkelblau | 2,64,121 | #024079 |
| Text (Titel, etc.) | Weiss | 255,255,255 | #FFFFFF |
| Logo-Text (Fallback) | Dunkelblau | 2,64,121 | #024079 |

---

## Typografie

| Element | Font | Grösse | Gewicht | Ausrichtung |
|---------|------|--------|---------|-------------|
| TITEL | Helvetica/Roboto | 32pt | Bold | Links |
| Untertitel | Helvetica/Roboto | 16pt | Regular | Links |
| Firma | Helvetica/Roboto | 12pt | Regular | Links |
| Datum | Helvetica/Roboto | 12pt | Regular | Links |

---

## Positionierung

| Element | X-Position | Y-Position (von oben) |
|---------|------------|----------------------|
| Logo | Rechts, 1.2cm vom Rand | 0.5cm |
| Header-Trennlinie | Gesamte Breite | 2.5cm |
| TITEL | Links, 2cm vom Rand | 11cm |
| Untertitel | Links, 2cm vom Rand | 13cm |
| Firma | Links, 2cm vom Rand | 15cm |
| Datum | Links, 2cm vom Rand | 16cm |

---

## Logo-Spezifikation

- **Position:** Rechts oben im weissen Header-Bereich
- **Höhe:** ca. 1.5cm
- **Format:** PNG mit Transparenz bevorzugt
- **Fallback:** Text "FEHR\nADVICE" in Dunkelblau wenn Datei fehlt

---

## Parameter (variabel)

Diese Werte werden vom Script überschrieben:

```latex
\newcommand{\FATitle}{TITEL}           % Haupttitel
\newcommand{\FASubtitle}{Untertitel}   % Untertitel
\newcommand{\FACompany}{FehrAdvice \& Partners AG}
\newcommand{\FADate}{Monat Jahr}       % z.B. "Januar 2026"
```

---

## Qualitätscheckliste

```
☐ Header weiss (2.5cm)
☐ Logo rechts oben
☐ Hauptbereich dunkelblau (#024079)
☐ Alle Texte weiss
☐ Alle Texte linksbündig
☐ TITEL gross und bold (32pt)
☐ Untertitel kleiner (16pt)
☐ Firma und Datum unten links
☐ Keine Rahmen oder Linien im Hauptbereich
```

---

## Unterschiede zum alten Design

| Aspekt | ALT | NEU (korrekt) |
|--------|-----|---------------|
| Hintergrund | Weiss/Hellgrau mit blauen Balken | Dunkelblau komplett |
| Text | Zentriert, blau | Linksbündig, weiss |
| Logo | Mitte oben | Rechts oben |
| Layout | Symmetrisch | Asymmetrisch (links-lastig) |

---

*Erstellt: 2026-01-29*
*Learning: RPT-L-019 (Cover-Design Requirements)*
