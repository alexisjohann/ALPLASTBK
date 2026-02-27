# BCM2 Kontextdatenbank: 459 Faktoren fuer die Schweiz

> **SSOT:** `data/dr-datareq/sources/context/ch/BCM2_04_KON_master_overview.yaml`
> **Upload-Tags:** canonical, bcm2, context, kontext, schweiz, ebf, ssot
> **Prioritaet:** HOCH — erklaert woher die Kontextdaten kommen

---

## Was ist BCM2?

**BCM2** ist die **Kontextdatenbank** des EBF. Sie enthaelt **459 quantitative Faktoren** fuer die Schweiz (und wird fuer Oesterreich und Deutschland erweitert).

**ACHTUNG:** BCM2 ist NICHT «BCM Version 2»! Es ist die Kontextfaktoren-Datenbank.

---

## Die 5 Hauptachsen

| Achse | Code | Faktoren | Inhalt |
|-------|------|----------|--------|
| **Demografie** | DEM | 60 | Bevoelkerung, Alter, Migration, Wohneigentum |
| **Wirtschaft** | ECO | 54 | BIP, Arbeitsmarkt, Preise, Handel |
| **Politik/Institutionen** | POL | 59 | Vertrauen, Regulierung, Abstimmungen |
| **Technologie/Oekologie** | TEC | 65 | Digitalisierung, Energie, Klima |
| **Sozio-Kultur** | SOC | 166 | Werte, Normen, Religion, Gesundheit |

**Gesamt:** 384 Basis-Faktoren + 75 erweiterte = 459

---

## Das Faktor-ID Format

```
CH-[ACHSE]-[NR]
```

Beispiele:
- **CH-DEM-01** = Bevoelkerungswachstum
- **CH-ECO-05** = Arbeitslosenquote
- **CH-SOC-12** = Generalisiertes Vertrauen
- **CH-TEC-03** = Internetnutzung

---

## Jeder Faktor hat

| Feld | Erklaerung |
|------|------------|
| `id` | Eindeutige Kennung (z.B. CH-DEM-01) |
| `name` | Klarer Name |
| `definition` | Was genau gemessen wird |
| `trend` | steigend / fallend / stabil |
| `uncertainty` | gering / mittel / hoch |

---

## Datenquellen (12 primaere)

Die Faktoren stammen aus offiziellen Quellen:

| Quelle | Faktoren | Bereich |
|--------|----------|---------|
| **BFS** (Bundesamt fuer Statistik) | 180 | Demografie, Wirtschaft, Gesellschaft |
| **SECO** (Staatssekretariat fuer Wirtschaft) | 45 | Arbeitsmarkt, Konjunktur |
| **SNB** (Nationalbank) | 25 | Finanzen, Zinsen, Wechselkurse |
| **BSV** (Sozialversicherungen) | 20 | AHV, IV, Pensionen |
| **BFE** (Energie) | 15 | Energie, Klima |
| **BAFU** (Umwelt) | 12 | Umwelt, CO2 |
| **OECD** | 30 | International vergleichend |
| **ESS** (European Social Survey) | 40 | Werte, Vertrauen |
| **WVS** (World Values Survey) | 20 | Kulturelle Werte |

Alle Quellen haben API-Zugang fuer automatische Aktualisierung.

---

## Verbindung zu Ψ-Dimensionen

BCM2-Faktoren werden den 8 Ψ-Dimensionen zugeordnet:

```
CH-DEM-* → Ψ_T (Zeit, Lebensphase)
CH-ECO-* → Ψ_E (Ressourcen, Budget)
CH-POL-* → Ψ_I (Regeln, Institutionen)
CH-TEC-* → Ψ_M (Tools, Technologie)
CH-SOC-* → Ψ_S (Sozial), Ψ_K (Kultur), Ψ_C (Kognitiv)
```

---

## Laender-Abdeckung

| Land | Status | Faktoren | Pfad |
|------|--------|----------|------|
| **Schweiz** | Vollstaendig | 459 | `context/ch/` |
| **Oesterreich** | In Arbeit | ~300 | `context/at/` |
| **Deutschland** | In Arbeit | ~300 | `context/de/` |

---

## Wie BCM2 in der Analyse verwendet wird

```
Schritt 1: Land waehlen (z.B. Schweiz)
     ↓
Schritt 2: Relevante Faktoren laden (z.B. CH-SOC-12 Vertrauen)
     ↓
Schritt 3: Ψ-Dimensionen parametrisieren
     ↓
Schritt 4: Parameter Context Transformation (PCT) anwenden
     ↓
Ergebnis: Kontextspezifische Verhaltensparameter
```

---

## Warum BCM2 wichtig ist

1. **Ohne Kontext ist jede Antwort falsch** — BCM2 liefert die Zahlen
2. **Empirisch fundiert** — Alle Werte aus offiziellen Quellen
3. **Zeitreihen 2020-2040** — Trends und Prognosen verfuegbar
4. **API-basiert** — Automatisch aktualisierbar

---

*Quelle: data/dr-datareq/sources/context/ch/BCM2_04_KON_master_overview.yaml (v1.1, 2026-01-23)*
