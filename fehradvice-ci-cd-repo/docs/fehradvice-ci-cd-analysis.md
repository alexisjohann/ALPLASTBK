# FehrAdvice & Partners AG — CI/CD Reverse Engineering

**Basierend auf:** 6 öffentlichen SlideShare-Präsentationen (2013–2015) + aktuelles Proposal-Dokument (Mai 2025, KPT Genossenschaft)

---

## 1. Logo

- **Platzierung:** Immer oben rechts
- **Aufbau:** Zweizeilig — "FEHR" (oben, grösser) / "ADVICE" (unten, etwas kleiner, gesperrt), beides Uppercase, serifenlos
- **Icon:** Links neben dem Text ein stilisiertes Kartenfächer-Symbol (5 aufgefächerte Karten) in Navy/Dunkelblau
- **Variante Deckblatt (Slide):** Logo auf weissem Kasten über Navy-Hintergrund
- **Variante Deckblatt (Dokument):** Logo oben rechts auf weissem Bereich ÜBER dem Navy-Block
- **Variante Content-Seiten (Dokument):** Nur das Kartenfächer-Icon (ohne Text), oben rechts

---

## 2. Farbpalette

| Rolle | Farbe | Hex (geschätzt) | Verwendung |
|-------|-------|-----------------|------------|
| **Primary** | Dunkel-Navy | `#1B365D` | Deckblatt-Hintergrund, Headlines, Akzentlinien, Header |
| **Secondary** | Petrol/Teal | `#2A7F8E` | Logo-Icon (ältere Version), gelegentliche Akzente |
| **Accent (Slides)** | Orange/Amber | `#E8A33D` | Pfeile (→), Schlussfolgerungen, Prozent-Balken |
| **Accent (Dokumente)** | Navy-Blau | `#1B365D` | "Nutzen"-Boxen, Phasen-Überschriften |
| **Background** | Weiss | `#FFFFFF` | Content-Seiten/-Slides |
| **Text Primary** | Schwarz/Dunkelgrau | `#1A1A1A` | Fliesstext (Dokument) |
| **Text Headings** | Dunkel-Navy | `#1B365D` | Kapitelüberschriften |
| **Text Secondary** | Mittelgrau | `#6B7280` | Fusszeilen, Seitenzahlen |

**Grundregel:** Extrem reduziertes Farbschema. Navy + Weiss dominieren. In Slides punktuell Orange, in Dokumenten fast ausschliesslich Navy + Schwarz + Weiss.

---

## 3. Typografie

### 3.1 Slide-Decks (Präsentationen)

| Element | Font | Grösse (geschätzt) | Stil |
|---------|------|---------------------|------|
| **Slide-Titel** | Sans-serif (Arial/Helvetica) | 20–24 pt | Bold, Dunkel-Navy |
| **Untertitel** | Sans-serif | 14–16 pt | Regular, Dunkel-Navy |
| **Fliesstext** | Sans-serif | 11–13 pt | Regular, Navy |
| **Bullets** | Sans-serif | 11–13 pt | Regular |
| **Fusszeile** | Sans-serif | 8–9 pt | Regular, Grau |
| **Grosse Zahlen** | Sans-serif | 36–48 pt | Bold, Orange oder Navy |
| **Zitate** | Sans-serif | 14–16 pt | Italic, zentriert |

### 3.2 Dokumente / Proposals (2025)

| Element | Font | Grösse (geschätzt) | Stil |
|---------|------|---------------------|------|
| **Deckblatt-Titel** | Sans-serif (wahrsch. Calibri/Helvetica) | 28–32 pt | Bold, Weiss, Uppercase |
| **Deckblatt-Subtitle** | Sans-serif | 14–16 pt | Regular, Weiss |
| **Kapitelüberschrift** | Sans-serif | 22–26 pt | Bold, Uppercase, Navy |
| **Phasen-Überschrift** | Sans-serif | 12–14 pt | Bold, Navy, Blauer Akzent |
| **Fliesstext** | Sans-serif | 10–11 pt | Regular, Schwarz, Blocksatz |
| **Bold-Hervorhebungen** | Sans-serif | 10–11 pt | Bold, Schwarz |
| **Aufzählungspunkte** | Sans-serif | 10–11 pt | Regular |
| **Header** | Sans-serif | 8–9 pt | Regular, Grau/Navy |
| **Inhaltsverzeichnis** | Sans-serif | 11–12 pt | Bold für Einträge, Regular für Seitenzahlen |

**Schriftart:** Wahrscheinlich **Calibri** (Dokumente) bzw. **Arial/Helvetica Neue** (Slides) — durchgehend clean corporate sans-serif.

---

## 4. Slide-Master-Typen

### 4.1 Titelslide (Deckblatt)

```
┌─────────────────────────────────────────────┐
│  [NAVY HINTERGRUND]                  [LOGO] │
│                                              │
│  «Titel der Präsentation»     ┌────────────┐│
│   Untertitel (2. Zeile)       │  BILD /    ││
│                                │  GRAFIK    ││
│   Event-Name / Anlass         │            ││
│   Referent: Name              └────────────┘│
│   Datum                                      │
│                                              │
└─────────────────────────────────────────────┘
```

- **Hintergrund:** Navy dunkelblau, vollflächig
- **Text:** Weiss, linksbündig, untere linke Hälfte
- **Bild/Grafik:** Rechte Hälfte, oft thematisch passend (Buch-Cover, Illustration)
- **Titel:** Guillemets «...» für Haupttitel (Schweizer Anführungszeichen)
- **Logo:** Oben rechts, auf hellem Kasten

### 4.2 Inhaltsslide (Index/Agenda)

```
┌─────────────────────────────────────────────┐
│  Slide-Titel (Bold, Navy)            [LOGO] │
│                                              │
│                                              │
│     1.  Punkt eins                           │
│                                              │
│     2.  Punkt zwei                           │
│                                              │
│     3.  Punkt drei                           │
│                                              │
│                                              │
│  ─────────────────────────────────────────── │
│                  FehrAdvice & Partners AG, [Monat] [JJ]   [#] │
└─────────────────────────────────────────────┘
```

- **Hintergrund:** Weiss
- **Nummerierung:** Einfache Ziffern mit Punkt, Navy
- **Viel Weissraum** zwischen den Punkten

### 4.3 Content-Slide (Standard)

```
┌─────────────────────────────────────────────┐
│  Slide-Titel (Bold, Navy)            [LOGO] │
│                                              │
│  ▪ Bullet-Punkt mit Erklärungstext          │
│  ▪ Zweiter Punkt                             │
│                                              │
│  → Schlussfolgerung in Orange/Fett          │
│                                              │
│                                              │
│  ─────────────────────────────────────────── │
│                  FehrAdvice & Partners AG, [Monat] [JJ]   [#] │
└─────────────────────────────────────────────┘
```

- **Titel:** Oben links, fett, Navy, als vollständiger Satz formuliert (nicht Stichwort)
- **Pfeile:** Orange → für Schlussfolgerungen/Key Takeaways
- **Bullet-Stil:** Quadratische oder runde kleine Aufzählungszeichen

### 4.4 Daten-/Umfrage-Slide

```
┌─────────────────────────────────────────────┐
│  Frage als Slide-Titel?              [LOGO] │
│                                              │
│   Hauptfrage fett hervorgehoben             │
│                                              │
│   1: Option A                          12%  │
│   ████████░░░░░░░░░░░░░░░░░░░░░░░░         │
│   2: Option B                          74%  │
│   ████████████████████████████████████      │
│   3: Option C                           9%  │
│   ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░        │
│                                              │
│  ─────────────────────────────────────────── │
│                  FehrAdvice & Partners AG, [Monat] [JJ]   [#] │
└─────────────────────────────────────────────┘
```

- **Balken:** Horizontal, in Navy-Blau
- **Prozentzahlen:** Rechts neben den Balken
- **Optionslabel:** "1:", "2:", "3:" etc. links

### 4.5 Framework/Prinzipien-Slide

```
┌─────────────────────────────────────────────┐
│  Slide-Titel                         [LOGO] │
│                                              │
│  ┌──┐  Prinzip 1: Name                      │
│  │1 │  Beschreibung und Erklärung            │
│  └──┘                                        │
│  ┌──┐  Prinzip 2: Name                      │
│  │2 │  Beschreibung und Erklärung            │
│  └──┘                                        │
│  ┌──┐  Prinzip 3: Name                      │
│  │3 │  Beschreibung und Erklärung            │
│  └──┘                                        │
│  ─────────────────────────────────────────── │
│                  FehrAdvice & Partners AG, [Monat] [JJ]   [#] │
└─────────────────────────────────────────────┘
```

- **Nummerierung:** Kreise oder Quadrate in Navy mit weisser Zahl
- **Zweispaltig:** Nummer links, Text rechts
- **Fett:** Prinzip-Name fett, Beschreibung regular

### 4.6 Vergleichs-/Matrix-Slide

```
┌─────────────────────────────────────────────┐
│  Slide-Titel                         [LOGO] │
│                                              │
│              TYPE 2                          │
│  ┌──────────────┬──────────────┐            │
│  │              │              │            │
│  │  Quadrant    │  Quadrant    │            │
│  │              │              │            │
│  ├──────────────┼──────────────┤            │
│  │              │              │            │
│  │  Quadrant    │  Quadrant    │            │
│  │              │              │            │
│  └──────────────┴──────────────┘            │
│              TYPE 1                          │
│  ─────────────────────────────────────────── │
│                  FehrAdvice & Partners AG, [Monat] [JJ]   [#] │
└─────────────────────────────────────────────┘
```

- **Achsenbeschriftungen:** Ausserhalb der Matrix, zentriert
- **Quadranten:** Leichter Rahmen, weisser Hintergrund, Bilder + Text

### 4.7 Schluss-Slide

- **Navy Hintergrund** (wie Titelslide)
- **"Vielen Dank für Ihre Aufmerksamkeit!"** in Weiss
- **Illustration/Cartoon** als visueller Aufhänger (oft humorvoll)
- **Logo** oben rechts

---

## 4B. Dokument-Master-Typen (Proposals, 2025)

### 4B.1 Deckblatt (Proposal)

```
┌─────────────────────────────────────────────┐
│                                  ┌─────────┐│
│                                  │ FEHR    ││
│                                  │ ADVICE  ││
│                                  └─────────┘│
│  ┌─────────────────────────────────────────┐│
│  │  [NAVY HINTERGRUND]                     ││
│  │                                          ││
│  │                                          ││
│  │  TITEL IN GROSSBUCHSTABEN               ││
│  │  ZWEITE ZEILE                            ││
│  │                                          ││
│  │  Untertitel in Regular, weiss            ││
│  │  mehrzeilig möglich                      ││
│  │                                          ││
│  │  FehrAdvice & Partners AG                ││
│  │  DD.MM.YYYY                              ││
│  │                                          ││
│  │                                          ││
│  └─────────────────────────────────────────┘│
└─────────────────────────────────────────────┘
```

- **Logo:** Oben rechts auf weissem Bereich ÜBER dem Navy-Block
- **Navy-Block:** Grosser Rechteck-Kasten, ca. 80–85% der Seitenhöhe, linke Kante leicht eingerückt
- **Titel:** Weiss, Bold, Uppercase, gross (28–32pt)
- **Untertitel:** Weiss, Regular, kleinere Schriftgrösse
- **Firmenname + Datum:** Unten im Navy-Block, weiss

### 4B.2 Header (alle Content-Seiten)

```
SEITE X VON Y — PROJEKTTITEL (BOLD) — FEHRADVICE & PARTNERS AG    [Karten-Icon]
──────────────────────────────────────────────────────────────────────────────────
```

- **Format:** `SEITE X VON Y — **PROJEKTTITEL** — FEHRADVICE & PARTNERS AG`
- **Trennzeichen:** Em-Dashes (—)
- **Projekttitel:** Fett/Bold hervorgehoben
- **Alles Uppercase**
- **Schriftgrösse:** Klein (8–9pt)
- **Icon:** Nur Kartenfächer-Symbol (ohne "FEHR ADVICE" Text), oben rechts
- **Blaue Linie:** Dünne horizontale Linie unter dem Header

### 4B.3 Inhaltsverzeichnis

```
┌─────────────────────────────────────────────┐
│  [HEADER]                          [Icon]   │
│                                              │
│  Inhaltsverzeichnis                          │
│  (Bold, gross, Navy)                         │
│                                              │
│  1    Kapitel eins ....................  3    │
│                                              │
│  2    Kapitel zwei ...................  3    │
│                                              │
│  3    Kapitel drei ...................  4    │
│                                              │
│  4    Kapitel vier ...................  8    │
│                                              │
│  5    Kapitel fünf ...................  8    │
│                                              │
└─────────────────────────────────────────────┘
```

- **Grosszügiger Zeilenabstand** zwischen Einträgen
- **Punktlinie** (Leader Dots) bis zur Seitenzahl
- **Nummerierung:** Arabische Ziffern, linksbündig

### 4B.4 Content-Seite (Standard)

```
┌─────────────────────────────────────────────┐
│  [HEADER]                          [Icon]   │
│                                              │
│  X  KAPITELÜBERSCHRIFT                       │
│     (UPPERCASE, BOLD, NAVY, GROSS)           │
│                                              │
│  Fliesstext in Blocksatz. Wichtige           │
│  Begriffe werden fett hervorgehoben.         │
│  Text ist durchgehend Blocksatz mit          │
│  professionellem Zeilenabstand.              │
│                                              │
│  Unterüberschrift (Bold, Navy)               │
│                                              │
│  Fliesstext weiter...                        │
│                                              │
└─────────────────────────────────────────────┘
```

- **Kapitelüberschriften:** Uppercase, Bold, Navy, gross (22–26pt)
- **Nummerierung:** Arabische Ziffern VOR dem Titel
- **Fliesstext:** Blocksatz (justified), Regular
- **Hervorhebungen:** Wichtige Begriffe inline **fett**
- **Keine Farb-Highlights** im Text (nur Bold)

### 4B.5 Phasen-Beschreibung (Proposal-Spezifisch)

```
┌─────────────────────────────────────────────┐
│  [HEADER]                          [Icon]   │
│                                              │
│  Phase X: Phasenname (Bold, Navy)            │
│                                              │
│  Ziel: Beschreibung... (Ziel: ist fett)      │
│                                              │
│  Inhalte:                                    │
│     1.  Punkt eins (Bold)                    │
│         o  Unterpunkt                        │
│         o  Unterpunkt (fett wo nötig)        │
│     2.  Punkt zwei (Bold)                    │
│         o  Unterpunkt                        │
│                                              │
│  ┌─────────────────────────────────────────┐ │
│  │  👍 Nutzen für die KPT (Bold, Navy)     │ │
│  │                                          │ │
│  │  • Nutzen-Punkt eins mit fetten         │ │
│  │    Hervorhebungen                       │ │
│  │  • Nutzen-Punkt zwei                    │ │
│  │  • Nutzen-Punkt drei                    │ │
│  └─────────────────────────────────────────┘ │
│                                              │
└─────────────────────────────────────────────┘
```

- **Phasen-Überschrift:** `Phase X: Name` — Bold, Navy, mit blauem Akzent
- **Ziel:** Einleitend, "Ziel:" als Label fett
- **Nummerierte Schritte:** 1., 2., 3. etc. — Schrittname fett
- **Unterpunkte:** Mit "o"-Zeichen (hollow circle), eingerückt
- **Sub-Unterpunkte:** Mit ▪ (gefülltes Quadrat), doppelt eingerückt
- **Nutzen-Box:** Hellgrauer Kasten mit:
  - 👍-Icon links oben
  - "Nutzen für die KPT" als Bold-Überschrift in Navy
  - Bullet-Points (•) mit fettem Kern und regulärem Erklärungstext
  - Horizontale Navy-Linie oben als Abgrenzung

### 4B.6 Kontakt-Seite

```
┌─────────────────────────────────────────────┐
│  [HEADER]                          [Icon]   │
│                                              │
│  X  KONTAKT                                  │
│     (UPPERCASE, BOLD, NAVY)                  │
│                                              │
│  ┌──────────┐                ┌──────────┐   │
│  │  FOTO    │  Name          │  FOTO    │   │
│  │  Person  │  Titel/        │  Person  │   │
│  │          │  Funktion      │          │   │
│  └──────────┘                └──────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

- **Fotos:** Professionelle Portraits, quadratisch/leicht gerundet
- **Name:** Bold
- **Funktion:** Regular, mehrzeilig
- **Seite an Seite** für mehrere Kontaktpersonen

---

## 5. Header & Footer

### Slide-Decks (Fusszeile)
```
──────────────────────────────────────────────────────────
                    FehrAdvice & Partners AG, [Monat] [JJ]    [Seitenzahl]
```
- **Position:** Unten rechts, über dünner Navy-Linie
- **Format:** "FehrAdvice & Partners AG, Januar 15" (Monat ausgeschrieben, Jahr zweistellig)

### Dokumente (Kopfzeile)
```
SEITE X VON Y — PROJEKTTITEL — FEHRADVICE & PARTNERS AG    [Karten-Icon]
─────────────────────────────────────────────────────────────────────────
```
- **Position:** Oben, volle Breite
- **Format:** Uppercase, mit Em-Dashes als Separator
- **Projekttitel:** Bold hervorgehoben
- **Icon:** Kartenfächer oben rechts (nur Icon, kein Text)
- **Blaue Trennlinie:** Unter dem Header

---

## 6. Gestaltungsprinzipien

| Prinzip | Umsetzung Slides | Umsetzung Dokumente |
|---------|------------------|---------------------|
| **Extreme Reduktion** | Max. 3 Farben (Navy, Weiss, Orange) | Max. 2 Farben (Navy, Schwarz auf Weiss) |
| **Daten statt Meinung** | Experimentdaten, Voting-Ergebnisse | Empirische Kennzahlen ("Nur 26%", "16%") |
| **Interaktionselemente** | Voting-Fragen (1:, 2:, 3:...) | — |
| **Akademische Referenzen** | Im Fliesstext (Ariely 2009 etc.) | Implizit (verhaltensökonomische Prinzipien) |
| **Satzhafte Titel** | Vollständige Aussagen als Slide-Titel | Kapitelüberschriften als Handlungsimperative |
| **Guillemets** | «...» für Zitate und Titel | Nicht im Proposal-Format verwendet |
| **Viel Weissraum** | Grosszügige Abstände | Sehr grosszügige Ränder und Zeilenabstände |
| **Nutzen-Boxen** | — | Grauer Kasten mit 👍-Icon und Bullets |
| **Bold-Hervorhebungen** | Sparsam | Extensiv — Schlüsselbegriffe inline fett |
| **Phasen-Struktur** | — | Nummerierte Phasen mit Ziel → Inhalte → Nutzen |
| **Blocksatz** | Nein (linksbündig) | Ja (justified) |

---

## 7. Sprachliche Muster

### Über beide Formate konsistent:
- **Deutsch mit Anglizismen:** "Choice Architecture", "Nudging", "Framing", "Touchpoints", "Playbook"
- **Schweizerdeutsch-Konventionen:** "ss" statt "ß" ("Massnahmen"), "grösser"
- **Gendersensible Sprache (2025):** "Kund:innen", "Freund:innen", "Mitarbeitende"
- **Wissenschaftliche Autorität:** Verhaltensökonomische Terminologie durchgehend
- **Aktionssprache:** "aktivieren", "erlebbar machen", "spürbar werden", "emotional aufladen"

### Slide-spezifisch:
- Fragenbasiert ("Haben wir stabile Präferenzen?")
- Passiv-Konstruktionen, akademischer Stil
- Dreier-Regel (3–5 Punkte pro Slide)

### Dokument-spezifisch:
- Lange, elaborierte Sätze (Consulting-Prosa)
- Gedankenstriche (–) als Stilmittel für Einschübe und Kontraste
- Häufige Doppelpunkte nach fetten Einleitungen ("**Ziel:** ...", "**Inhalte:** ...")
- Aufzählungen mit Einleitungssatz + Doppelpunkt
- "Erlebbar machen" als Leitmetapher (wiederkehrendes Motiv)

---

## 8. Zusammenfassung für Template-Bau

### A) Slide Deck Template
```
FEHRADVICE SLIDE DECK TEMPLATE
================================
Aspect Ratio:    16:9
Primary:         #1B365D (Navy)
Secondary:       #2A7F8E (Teal/Petrol)
Accent:          #E8A33D (Orange/Amber)
Background:      #FFFFFF (Content), #1B365D (Title/End)
Text:            #1B365D (Navy), #6B7280 (Grau für Fussnoten)
Font:            Arial oder Helvetica Neue
Logo:            Oben rechts, immer sichtbar (Vollversion)
Footer:          "FehrAdvice & Partners AG, [Monat] [JJ]  [#]"
Bullet Style:    ▪ oder § (klein, Navy)
Arrow Style:     → in Orange für Conclusions
Title Style:     Vollständige Sätze, Bold, 20-24pt
```

### B) Dokument / Proposal Template
```
FEHRADVICE DOCUMENT TEMPLATE
================================
Page Size:       A4, Portrait
Primary:         #1B365D (Navy)
Background:      #FFFFFF
Text Body:       #1A1A1A (Schwarz/Dunkelgrau)
Text Headings:   #1B365D (Navy), Uppercase, Bold
Font:            Calibri (oder Helvetica Neue)
Logo (Cover):    Oben rechts, Vollversion auf weissem Bereich
Logo (Content):  Oben rechts, nur Kartenfächer-Icon
Header:          "SEITE X VON Y — PROJEKTTITEL — FEHRADVICE & PARTNERS AG"
Header-Linie:    Dünne Navy-Linie unter Header
Body Alignment:  Blocksatz (justified)
Bold Usage:      Extensiv — Schlüsselbegriffe inline fett
Nutzen-Box:      Hellgrauer Kasten, Navy-Linie oben, 👍-Icon, Bullets
Phase-Format:    "Phase X: Name" → Ziel → Inhalte (nummeriert) → Nutzen-Box
Margins:         Grosszügig (~2.5cm links/rechts)
Cover:           Navy-Block (80-85% Höhe), Titel weiss/uppercase
```

---

## 9. Evolution des CI/CD (2013 → 2025)

| Element | 2013–2015 (Slides) | 2025 (Dokument) |
|---------|-------------------|-----------------|
| **Logo-Icon** | Kopf/Gehirn-Symbol | Kartenfächer (5 Karten) |
| **Akzentfarbe** | Orange/Amber prominent | Fast kein Orange, reines Navy |
| **Sprache** | Akademisch-neutral | Gendersensibel (Kund:innen) |
| **Struktur** | Frei, thematisch | Stark formalisiert (Phase → Ziel → Inhalte → Nutzen) |
| **Interaktivität** | Voting Devices, Polling | — |
| **Fazit-Stil** | → Pfeil in Orange | Bold-Hervorhebungen inline |
| **Titel-Stil** | Vollständige Sätze | Handlungsimperative ("Genossenschaft neu erlebbar machen") |
| **Nutzen-Kommunikation** | Implizit | Explizite "Nutzen"-Boxen pro Phase |
| **Format-Konsistenz** | Hoch innerhalb Deck | Sehr hoch — jede Phase identische Struktur |
