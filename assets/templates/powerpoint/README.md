# FehrAdvice PowerPoint Templates

Programmatisch generierte PowerPoint-Präsentationsvorlagen gemäss dem offiziellen Corporate Identity Guide.

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `FehrAdvice_Template.pptx` | Fertige Präsentationsvorlage (14 Folien) |
| `generate_fehradvice_pptx.py` | Python-Script zur Generierung |

## Enthaltene Folientypen

1. **Titelfolie** - Dunkelblaue Startfolie mit Titel und Untertitel
2. **Agenda** - Übersicht mit nummerierten Punkten
3. **Kapiteltrennseite** - Blaue Sektion-Divider mit Nummer
4. **Inhaltsfolie** - Standard-Layout mit Aufzählungspunkten
5. **Zwei-Spalten** - Vergleichs-Layout
6. **Datenvisualisierung** - Chart-Platzhalter mit Notizbereich
7. **Key Insight** - Hervorhebung einer Kernaussage
8. **Zitat** - Hellblauer Hintergrund mit «Guillemets»
9. **Kontakt** - Abschlussfolie mit Kontaktdaten

## Verwendung

### Template direkt verwenden

Die Datei `FehrAdvice_Template.pptx` kann direkt in PowerPoint geöffnet und bearbeitet werden.

### Neues Template generieren

```bash
python generate_fehradvice_pptx.py [output_path.pptx]
```

### Anpassung

Das Script kann angepasst werden für:
- Andere Inhalte
- Zusätzliche Folientypen
- Projektspezifische Präsentationen

## Corporate Identity

### Farben

| Farbe | Hex | RGB | Verwendung |
|-------|-----|-----|------------|
| Dark Blue | #024079 | 2, 64, 121 | Hintergründe, Header |
| Light Blue | #549EDE | 84, 158, 222 | Akzente, Highlights |
| Dark Gray | #25212A | 37, 33, 42 | Fliesstext |
| Light Gray | #F3F5F7 | 243, 245, 247 | Hintergründe (hell) |
| Lilac | #A1A0C6 | 161, 160, 198 | Sekundär |
| Mint | #7EBDAC | 126, 189, 172 | Sekundär |
| Ocher | #DECB3F | 222, 203, 63 | Sekundär |
| Orange | #DE9D3E | 222, 157, 62 | Sekundär |

### Schriften

| Typ | Schriftart | Verwendung |
|-----|------------|------------|
| Headlines | Roboto | Titel, Überschriften |
| Body | Open Sans | Fliesstext, Aufzählungen |
| Accent | Playfair Display | Zitate, spezielle Hervorhebungen |

### Format

- **Seitenverhältnis:** 16:9
- **Sprache:** Deutsch (Schweizer Rechtschreibung)
- **Zahlenformat:** 1'000.00 (Schweizer Hochkomma)
- **Anführungszeichen:** «Guillemets»

## Dependencies

```bash
pip install python-pptx pillow lxml
```

## Hinweis

Das Logo muss manuell eingefügt werden. Platzhalter sind mit `[LOGO]` markiert.

Logo-Dateien befinden sich in: `../../logo/color/`
