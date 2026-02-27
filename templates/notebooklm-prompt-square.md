# NotebookLM Infographic Prompt — SQUARE (1:1)
# ============================================================================
# SSOT: templates/infographic-design-system.yaml
# Verwendung: Copy-Paste in NotebookLM Style Prompt Feld
# Platzhalter: {{VARIABLE}} — vor Verwendung ersetzen
# ============================================================================

## PLATZHALTER-REFERENZ

| Platzhalter | Beschreibung | Beispiel |
|-------------|--------------|----------|
| `{{TITEL}}` | Action Title (These + Richtung) | "Preise runter, Löhne rauf" |
| `{{KILLER_ZAHL_PRIMARY}}` | Die EINE Hauptzahl | "-0,7%" |
| `{{KILLER_ZAHL_PRIMARY_LABEL}}` | Beschriftung der Hauptzahl | "Preisrückgang im Monatsvergleich" |
| `{{KILLER_ZAHL_SECONDARY}}` | Stützende Zahl | "11% → 2%" |
| `{{KILLER_ZAHL_SECONDARY_LABEL}}` | Beschriftung | "Inflation 2023 → 2026" |
| `{{CHECK_1}}` | Checkmark-Item 1 | "MwSt-Senkung: 1,4 Mrd. € Entlastung" |
| `{{CHECK_2}}` | Checkmark-Item 2 | "Mietpreisbremse: 300.000 Haushalte" |
| `{{CHECK_3}}` | Checkmark-Item 3 | "Anti-Shrinkflation: 15.000 € Strafe" |
| `{{VERGLEICH_LABEL_A}}` | Vergleich links | "Österreich (SPÖ)" |
| `{{VERGLEICH_LABEL_B}}` | Vergleich rechts | "Ungarn (Orbán)" |
| `{{VERGLEICH_WERT_A_1}}` | Wert A Zeile 1 | "2,0%" |
| `{{VERGLEICH_WERT_B_1}}` | Wert B Zeile 1 | "3,7%" |
| `{{VERGLEICH_KATEGORIE_1}}` | Kategorie Zeile 1 | "Inflation" |
| `{{VERGLEICH_WERT_A_2}}` | Wert A Zeile 2 | "Gedeckelt" |
| `{{VERGLEICH_WERT_B_2}}` | Wert B Zeile 2 | "+22%" |
| `{{VERGLEICH_KATEGORIE_2}}` | Kategorie Zeile 2 | "Mieten" |
| `{{MASSNAHME_1_ICON_DESC}}` | Icon-Beschreibung 1 | "Einkaufswagen" |
| `{{MASSNAHME_1_TITEL}}` | Massnahme 1 | "MwSt-Senkung" |
| `{{MASSNAHME_1_ZAHL}}` | Massnahme 1 Zahl | "1,4 Mrd. €" |
| `{{MASSNAHME_2_ICON_DESC}}` | Icon-Beschreibung 2 | "Haus" |
| `{{MASSNAHME_2_TITEL}}` | Massnahme 2 | "Mietpreisbremse" |
| `{{MASSNAHME_2_ZAHL}}` | Massnahme 2 Zahl | "300.000" |
| `{{MASSNAHME_3_ICON_DESC}}` | Icon-Beschreibung 3 | "Waage" |
| `{{MASSNAHME_3_TITEL}}` | Massnahme 3 | "Shrinkflation-Gesetz" |
| `{{MASSNAHME_3_ZAHL}}` | Massnahme 3 Zahl | "15.000 €" |
| `{{FAZIT}}` | Fazit-Satz | "Ordnung wirkt." |
| `{{QUELLE}}` | Quellenangabe | "Statistik Austria, Eurostat" |
| `{{DATUM}}` | Stand-Datum | "Jänner 2026" |
| `{{HASHTAG}}` | Closer-Hashtag | "#OrdnenStattSpalten" |
| `{{PRIMAERFARBE_HEX}}` | Kundenfarbe | "#E3000F" |

---

## PROMPT (Copy-Paste Ready)

```
INFOGRAFIK QUADRAT (1:1 Square)

FARBEN: Nur 3 Farben verwenden:
- {{PRIMAERFARBE_HEX}} (Primärfarbe) für Icons, Killer-Zahlen, Banner
- #1A1A1A (Schwarz) für Text und Rahmen
- #FFFFFF (Weiss) für Hintergrund
- #F5F5F5 (Hellgrau) für Box-Hintergründe
Keine Farbverläufe, keine Schatten, keine weiteren Farben.

ICONS: Flat Line Art, einfarbig in Primärfarbe. Einfach, klar, erkennbar in 0.5 Sekunden.

ARCHITEKTUR — 2x2 Grid mit Header und Closer:

═══════════════════════════════════════
HEADER (oben, volle Breite)
═══════════════════════════════════════
Roter Banner.
Weisser Text: «{{TITEL}}»

═══════════════════════════════════════
GRID — 4 Quadranten
═══════════════════════════════════════

┌─────────────────────┬─────────────────────┐
│                     │                     │
│  OBEN LINKS:        │  OBEN RECHTS:       │
│  KILLER-ZAHL        │  ENTLASTUNG         │
│                     │                     │
│  «{{KILLER_ZAHL_PRIMARY}}»               │
│  in 72pt Primärfarbe│  ✓ {{CHECK_1}}      │
│  Starburst oder     │  ✓ {{CHECK_2}}      │
│  Kreis              │  ✓ {{CHECK_3}}      │
│                     │                     │
│  «{{KILLER_ZAHL_PRIMARY_LABEL}}»         │
│                     │                     │
│  Kleiner:           │                     │
│  «{{KILLER_ZAHL_SECONDARY}}»             │
│  «{{KILLER_ZAHL_SECONDARY_LABEL}}»       │
│                     │                     │
├─────────────────────┼─────────────────────┤
│                     │                     │
│  UNTEN LINKS:       │  UNTEN RECHTS:      │
│  VERGLEICH          │  MASSNAHMEN         │
│                     │                     │
│  Mini-Tabelle:      │  3 Icons mit Text:  │
│  {{VERGLEICH_LABEL_A}} vs                │
│  {{VERGLEICH_LABEL_B}}                   │
│                     │                     │
│  {{VERGLEICH_KATEGORIE_1}}:              │
│  {{VERGLEICH_WERT_A_1}} vs              │
│  {{VERGLEICH_WERT_B_1}}                 │
│                     │  [{{MASSNAHME_1_ICON_DESC}}]│
│  {{VERGLEICH_KATEGORIE_2}}:             │  {{MASSNAHME_1_TITEL}}│
│  {{VERGLEICH_WERT_A_2}} vs              │  {{MASSNAHME_1_ZAHL}} │
│  {{VERGLEICH_WERT_B_2}}                 │                     │
│                     │  [{{MASSNAHME_2_ICON_DESC}}]│
│                     │  {{MASSNAHME_2_TITEL}}│
│                     │  {{MASSNAHME_2_ZAHL}} │
│                     │                     │
│                     │  [{{MASSNAHME_3_ICON_DESC}}]│
│                     │  {{MASSNAHME_3_TITEL}}│
│                     │  {{MASSNAHME_3_ZAHL}} │
│                     │                     │
└─────────────────────┴─────────────────────┘

═══════════════════════════════════════
CLOSER (unten, volle Breite)
═══════════════════════════════════════
Roter Banner oder hellgrauer Streifen.
Links: «{{FAZIT}}»
Mitte: «{{HASHTAG}}»
Rechts klein: «Quelle: {{QUELLE}} | Stand: {{DATUM}}»

═══════════════════════════════════════

STIL: Minimalistisch, datengetrieben, symmetrisches Grid.
Jeder Quadrant hat mindestens EINE konkrete Zahl.
Keine dekorativen Elemente. Keine Stockfotos.
Klare Trennlinien zwischen den 4 Quadranten.
```
