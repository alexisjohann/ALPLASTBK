<!--
================================================================================
DESIGN INSTRUCTIONS (für Google NotebookLM / externe Tools)
================================================================================
Diese Sektion wird automatisch ans Ende jedes Deliverables angehängt.
Sie ist nur für KI-Tools sichtbar - nicht für den Endleser gedacht.
================================================================================
-->

---

## 🎨 Design Instructions

> **Hinweis für KI/Designer:** Diese Sektion enthält die Gestaltungsrichtlinien.
> Sie soll NICHT im finalen Dokument erscheinen, sondern nur die Gestaltung steuern.

### Kunde
- **Name:** {CLIENT_NAME}
- **Branche:** {INDUSTRY}

### Farben
| Verwendung | Hex-Code | Beispiel |
|------------|----------|----------|
| Primärfarbe (Headlines, Akzente) | {PRIMARY_HEX} | ████ |
| Text dunkel | {TEXT_DARK_HEX} | ████ |
| Text hell (auf dunklem BG) | #FFFFFF | ████ |
| Hintergrund | #FFFFFF | ████ |
| Hintergrund Akzent-Boxen | {BG_ACCENT_HEX} | ████ |
| Chart-Farbe 1 | {CHART_1_HEX} | ████ |
| Chart-Farbe 2 | {CHART_2_HEX} | ████ |
| Chart-Farbe 3 | {CHART_3_HEX} | ████ |

### Schriften
| Verwendung | Schriftart | Schnitt |
|------------|------------|---------|
| Headlines (H1, H2) | {HEADLINE_FONT} | Bold/Semibold |
| Fliesstext | {BODY_FONT} | Regular |
| Google Fonts Import | `{GOOGLE_FONTS_IMPORT}` | |

### Orthographie (Schweiz)
- **ß:** Nicht verwenden → immer "ss" (Strasse, nicht Straße)
- **Gendering:** Mit Doppelpunkt (Kund:innen, Mitarbeiter:innen)
- **Anführungszeichen:** «Guillemets» (nicht "Gänsefüsschen")
- **Tausender:** Apostroph (1'000, nicht 1.000)

### Stil
- **Tonalität:** {TONE}
- **Ecken:** Leicht abgerundet (4px)
- **Schatten:** Dezent
- **Weissraum:** Grosszügig

### Präsentations-Struktur (falls Slides)
1. **Titelfolie:** Titel + Datum, Primärfarbe als Hintergrund, weisse Schrift
2. **Executive Summary:** Key Points in Bullet-Liste
3. **Inhalt:** Weisser Hintergrund, Headlines in Primärfarbe
4. **Statistiken:** Zahlen gross darstellen, Chart-Farben verwenden
5. **Fazit:** Empfehlungen als nummerierte Liste
6. **Kontakt:** Logo + Kontaktdaten

### Prompt für KI
```
Gestalte dieses Dokument als professionelle Präsentation:
- Verwende die Farben aus der Tabelle oben
- Headlines in {HEADLINE_FONT} Bold
- Text in {BODY_FONT} Regular
- Stil: {TONE}
- Schweizer Orthographie beachten (ss, Gendering mit :)
- Statistiken und Zahlen visuell hervorheben
- Die "Design Instructions" Sektion NICHT im Output zeigen
```
