# NotebookLM Infographic Prompt — PORTRAIT (9:16)
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
| `{{TREND_TEXT}}` | Trend-Beschreibung | "Von 11% (Jän. 2023) auf 2,0% (Jän. 2026)" |
| `{{KONTEXT_ZAHL_1}}` | Kontext-Datenpunkt 1 | "-4,9% Energiepreise" |
| `{{KONTEXT_ZAHL_2}}` | Kontext-Datenpunkt 2 | "Stärkster Rückgang seit Jän. 2019" |
| `{{EHRLICHKEIT}}` | Behavioral Inoculation Satz | "Gegen die Teuerung gewinnt man nie ganz — aber man kann sie bremsen." |
| `{{SCHRITT_1_TITEL}}` | Massnahme 1 | "MwSt-Senkung Lebensmittel" |
| `{{SCHRITT_1_ZAHL}}` | Massnahme 1 Zahl | "1,4 Mrd. € Entlastung" |
| `{{SCHRITT_2_TITEL}}` | Massnahme 2 | "Mietpreisbremse" |
| `{{SCHRITT_2_ZAHL}}` | Massnahme 2 Zahl | "300.000 Haushalte geschützt" |
| `{{SCHRITT_3_TITEL}}` | Massnahme 3 | "Anti-Shrinkflation-Gesetz" |
| `{{SCHRITT_3_ZAHL}}` | Massnahme 3 Zahl | "Bis zu 15.000 € Strafe" |
| `{{VERGLEICH_LABEL_A}}` | Vergleich links | "SPÖ-Programm" |
| `{{VERGLEICH_LABEL_B}}` | Vergleich rechts | "Orbán (Ungarn)" |
| `{{VERGLEICH_PUNKT_1}}` | Vergleichspunkt 1 | "Inflation: 2,0% vs. 3,7%" |
| `{{VERGLEICH_PUNKT_2}}` | Vergleichspunkt 2 | "Mieten: Gedeckelt vs. +22%" |
| `{{VERGLEICH_PUNKT_3}}` | Vergleichspunkt 3 | "Lebensmittel: MwSt gesenkt vs. Preise ↑" |
| `{{FAZIT}}` | Fazit-Satz | "Ordnung wirkt — bei Preisen, Mieten und Energie." |
| `{{QUELLE}}` | Quellenangabe | "Statistik Austria, Eurostat" |
| `{{DATUM}}` | Stand-Datum | "Jänner 2026" |
| `{{HASHTAG}}` | Closer-Hashtag | "#OrdnenStattSpalten" |
| `{{PRIMAERFARBE_HEX}}` | Kundenfarbe | "#E3000F" |

---

## PROMPT (Copy-Paste Ready)

```
INFOGRAFIK HOCHFORMAT (9:16 Portrait)

FARBEN: Nur 3 Farben verwenden:
- {{PRIMAERFARBE_HEX}} (Primärfarbe) für Icons, Killer-Zahlen, Banner
- #1A1A1A (Schwarz) für Text und Rahmen
- #FFFFFF (Weiss) für Hintergrund
- #F5F5F5 (Hellgrau) für Box-Hintergründe
Keine Farbverläufe, keine Schatten, keine weiteren Farben.

ICONS: Flat Line Art, einfarbig in Primärfarbe. Einfach, klar, erkennbar in 0.5 Sekunden.

ARCHITEKTUR — 7 vertikale Sektionen (von oben nach unten):

═══════════════════════════════════════
SEKTION 1 — HEADER
═══════════════════════════════════════
Roter Banner über volle Breite.
Weisser Text:
  Gross: «{{TITEL}}»
  Klein darunter: «{{UNTERTITEL}}»

═══════════════════════════════════════
SEKTION 2 — KILLER-ZAHL
═══════════════════════════════════════
Grosser roter Starburst oder Kreis, zentriert.
Darin: «{{KILLER_ZAHL_PRIMARY}}» in 72pt Primärfarbe.
Darunter: «{{KILLER_ZAHL_PRIMARY_LABEL}}»

═══════════════════════════════════════
SEKTION 3 — TREND + KONTEXT
═══════════════════════════════════════
Hellgrauer Box-Hintergrund.
- Trendlinie oder Pfeil: «{{TREND_TEXT}}»
- «{{KONTEXT_ZAHL_1}}»
- «{{KONTEXT_ZAHL_2}}»
Jeder Punkt mit kleinem roten Icon davor.

═══════════════════════════════════════
SEKTION 4 — EHRLICHKEITS-LINIE
═══════════════════════════════════════
Dünne rote Linie oben und unten als Trenner.
Kursiver Text dazwischen:
«{{EHRLICHKEIT}}»

═══════════════════════════════════════
SEKTION 5 — 3 SCHRITTE / MASSNAHMEN
═══════════════════════════════════════
Überschrift: «Was wir konkret tun:» (oder ähnlich)

✓ «{{SCHRITT_1_TITEL}}»
  «{{SCHRITT_1_ZAHL}}»

✓ «{{SCHRITT_2_TITEL}}»
  «{{SCHRITT_2_ZAHL}}»

✓ «{{SCHRITT_3_TITEL}}»
  «{{SCHRITT_3_ZAHL}}»

Jeder Schritt mit rotem Checkmark-Icon.

═══════════════════════════════════════
SEKTION 6 — VERGLEICH
═══════════════════════════════════════
Side-by-Side Vergleich:

Links: «{{VERGLEICH_LABEL_A}}» | Rechts: «{{VERGLEICH_LABEL_B}}»

{{VERGLEICH_PUNKT_1}}
{{VERGLEICH_PUNKT_2}}
{{VERGLEICH_PUNKT_3}}

═══════════════════════════════════════
SEKTION 7 — CLOSER
═══════════════════════════════════════
Roter Banner oder Box.
Weisser Text: «{{FAZIT}}»
Gross: «{{HASHTAG}}»
Klein: «Quelle: {{QUELLE}} | Stand: {{DATUM}}»

═══════════════════════════════════════

STIL: Minimalistisch, datengetrieben. Vertikaler Lesefluss.
Jede Sektion hat mindestens EINE konkrete Zahl.
Keine dekorativen Elemente. Keine Stockfotos.
```
