# NotebookLM Infographic Prompt — LANDSCAPE (16:9)
# ============================================================================
# SSOT: templates/infographic-design-system.yaml
# Verwendung: Copy-Paste in NotebookLM Style Prompt Feld
# Platzhalter: {{VARIABLE}} — vor Verwendung ersetzen
# ============================================================================

## PLATZHALTER-REFERENZ

| Platzhalter | Beschreibung | Beispiel |
|-------------|--------------|----------|
| `{{TITEL}}` | Action Title (These + Richtung) | "Preise runter, Löhne rauf" |
| `{{UNTERTITEL}}` | Kontext-Zeile | "Wie die SPÖ-Entlastung wirkt" |
| `{{KILLER_ZAHL_PRIMARY}}` | Die EINE Hauptzahl | "-0,7%" |
| `{{KILLER_ZAHL_PRIMARY_LABEL}}` | Beschriftung der Hauptzahl | "Preisrückgang im Monatsvergleich" |
| `{{KILLER_ZAHL_SECONDARY_1}}` | Stützende Zahl 1 | "11% → 2%" |
| `{{KILLER_ZAHL_SECONDARY_1_LABEL}}` | Beschriftung | "Inflation 2023 → 2026" |
| `{{KILLER_ZAHL_SECONDARY_2}}` | Stützende Zahl 2 | "-4,9%" |
| `{{KILLER_ZAHL_SECONDARY_2_LABEL}}` | Beschriftung | "Energiepreise im Jahresvergleich" |
| `{{MASSNAHME_1_TITEL}}` | Massnahme 1 Überschrift | "MwSt-Senkung Lebensmittel" |
| `{{MASSNAHME_1_ZAHL}}` | Massnahme 1 Kernzahl | "1,4 Mrd. € Entlastung" |
| `{{MASSNAHME_1_TEXT}}` | Massnahme 1 Kurzbeschreibung | "Mehrwertsteuer auf Grundnahrungsmittel halbiert" |
| `{{MASSNAHME_2_TITEL}}` | Massnahme 2 Überschrift | "Mietpreisbremse" |
| `{{MASSNAHME_2_ZAHL}}` | Massnahme 2 Kernzahl | "300.000 Haushalte geschützt" |
| `{{MASSNAHME_2_TEXT}}` | Massnahme 2 Kurzbeschreibung | "Mieterhöhungen auf Inflationsniveau gedeckelt" |
| `{{MASSNAHME_3_TITEL}}` | Massnahme 3 Überschrift | "Anti-Shrinkflation-Gesetz" |
| `{{MASSNAHME_3_ZAHL}}` | Massnahme 3 Kernzahl | "Bis zu 15.000 € Strafe" |
| `{{MASSNAHME_3_TEXT}}` | Massnahme 3 Kurzbeschreibung | "Transparenzpflicht für 100 Produkte" |
| `{{EHRLICHKEIT}}` | Behavioral Inoculation Satz | "Gegen die Teuerung gewinnt man nie ganz — aber man kann sie bremsen." |
| `{{VERGLEICH_SPALTE_A}}` | Vergleich links | "SPÖ-Regierungsprogramm" |
| `{{VERGLEICH_SPALTE_B}}` | Vergleich rechts | "Orbán-Modell (Ungarn)" |
| `{{VERGLEICH_ZEILE_1}}` | Zeile 1 Kategorie + Werte | "Inflation: 2,0% vs. 3,7%" |
| `{{VERGLEICH_ZEILE_2}}` | Zeile 2 Kategorie + Werte | "Lebensmittel: MwSt gesenkt vs. Preise gestiegen" |
| `{{VERGLEICH_ZEILE_3}}` | Zeile 3 Kategorie + Werte | "Mieten: Gedeckelt vs. +22% seit 2022" |
| `{{FAZIT}}` | Fazit-Satz | "Ordnung wirkt — bei Preisen, Mieten und Energie." |
| `{{QUELLE}}` | Quellenangabe | "Statistik Austria, Eurostat" |
| `{{DATUM}}` | Stand-Datum | "Jänner 2026" |
| `{{HASHTAG}}` | Closer-Hashtag | "#OrdnenStattSpalten" |
| `{{PRIMAERFARBE_HEX}}` | Kundenfarbe | "#E3000F" |

---

## PROMPT (Copy-Paste Ready)

```
INFOGRAFIK QUERFORMAT (16:9 Landscape)

FARBEN: Nur 3 Farben verwenden:
- {{PRIMAERFARBE_HEX}} (Primärfarbe) für Icons, Killer-Zahlen, Banner
- #1A1A1A (Schwarz) für Text und Rahmen
- #FFFFFF (Weiss) für Hintergrund
- #F5F5F5 (Hellgrau) für Box-Hintergründe
Keine Farbverläufe, keine Schatten, keine weiteren Farben.

ICONS: Flat Line Art, einfarbig in Primärfarbe. Einfach, klar, erkennbar in 0.5 Sekunden.

ARCHITEKTUR — 3 Bänder:

═══════════════════════════════════════════════════════════════
BAND 1 — HEADER (oben, 20% der Höhe)
═══════════════════════════════════════════════════════════════
Roter Banner über volle Breite.
Weisser Text:
  Gross: «{{TITEL}}»
  Klein darunter: «{{UNTERTITEL}}»

═══════════════════════════════════════════════════════════════
BAND 2 — CONTENT (Mitte, 55% der Höhe, 2 Spalten)
═══════════════════════════════════════════════════════════════

LINKE SPALTE — TREND / AUSGANGSLAGE:
- Grosser Starburst oder Kreis mit «{{KILLER_ZAHL_PRIMARY}}» in 72pt Primärfarbe
  Darunter: «{{KILLER_ZAHL_PRIMARY_LABEL}}»
- Trendlinie oder Pfeil: «{{KILLER_ZAHL_SECONDARY_1}}»
  Label: «{{KILLER_ZAHL_SECONDARY_1_LABEL}}»
- Zusätzlicher Datenpunkt: «{{KILLER_ZAHL_SECONDARY_2}}»
  Label: «{{KILLER_ZAHL_SECONDARY_2_LABEL}}»

RECHTE SPALTE — MASSNAHMEN:
3 Cards vertikal gestapelt, jede mit:

Card 1: [Icon] «{{MASSNAHME_1_TITEL}}»
  Zahl: «{{MASSNAHME_1_ZAHL}}»
  Text: «{{MASSNAHME_1_TEXT}}»

Card 2: [Icon] «{{MASSNAHME_2_TITEL}}»
  Zahl: «{{MASSNAHME_2_ZAHL}}»
  Text: «{{MASSNAHME_2_TEXT}}»

Card 3: [Icon] «{{MASSNAHME_3_TITEL}}»
  Zahl: «{{MASSNAHME_3_ZAHL}}»
  Text: «{{MASSNAHME_3_TEXT}}»

═══════════════════════════════════════════════════════════════
BAND 3 — SUMMARY (unten, 25% der Höhe)
═══════════════════════════════════════════════════════════════

Hellgrauer Hintergrund.

Ehrlichkeits-Linie (kursiv): «{{EHRLICHKEIT}}»

Vergleichstabelle mit 2 Spalten:
| Kategorie | {{VERGLEICH_SPALTE_A}} | {{VERGLEICH_SPALTE_B}} |
{{VERGLEICH_ZEILE_1}}
{{VERGLEICH_ZEILE_2}}
{{VERGLEICH_ZEILE_3}}

Fazit (fett): «{{FAZIT}}»

Rechts unten klein: «Quelle: {{QUELLE}} | Stand: {{DATUM}}»
Links unten: «{{HASHTAG}}»

═══════════════════════════════════════════════════════════════

STIL: Minimalistisch, datengetrieben, klar strukturiert.
Jeder Abschnitt hat mindestens EINE konkrete Zahl.
Keine dekorativen Elemente. Keine Stockfotos.
```
