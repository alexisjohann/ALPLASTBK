# /pipeline-report - Pipeline-Übersicht generieren

Generiert einen Überblick über die Sales-Pipeline.

## Syntax

```bash
/pipeline-report                    # Vollständiger Report
/pipeline-report --stage ACTIVE     # Nur bestimmter Stage
/pipeline-report --owner EB         # Nur bestimmter Owner
/pipeline-report --industry finance # Nur bestimmte Branche
/pipeline-report --forecast         # Mit Revenue-Forecast
```

## Standard-Report

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 PIPELINE REPORT - FehrAdvice & Partners AG                          │
│  Stand: 2026-01-27                                                      │
└─────────────────────────────────────────────────────────────────────────┘

PIPELINE-ÜBERSICHT
══════════════════════════════════════════════════════════════════════════

AKQUISE-PHASE (3 Leads)
───────────────────────────────────────────────────────────────────────────
Stage         Count   Leads                              Value (EUR)
───────────────────────────────────────────────────────────────────────────
SUSPECT         1     Migros                             -
PROSPECT        1     Post                               -
QUALIFIED       1     Swisscom                           150'000
PROPOSAL        0     -                                  -
NEGOTIATION     0     -                                  -
───────────────────────────────────────────────────────────────────────────
                3                                        150'000

KUNDEN-PHASE (7 Leads)
───────────────────────────────────────────────────────────────────────────
Stage         Count   Leads
───────────────────────────────────────────────────────────────────────────
ACTIVE          6     ALPLA, PORR, LUKB, Lindt, BFE, Innosuisse
DORMANT         1     UBS
───────────────────────────────────────────────────────────────────────────
                7

EHEMALIGE (2 Leads)
───────────────────────────────────────────────────────────────────────────
Stage         Count   Learnings
───────────────────────────────────────────────────────────────────────────
CHURNED         1     Budget-Kürzungen nach Restrukturierung
LOST            1     McKinsey - Brand preference
───────────────────────────────────────────────────────────────────────────
                2

══════════════════════════════════════════════════════════════════════════

ZUSAMMENFASSUNG
───────────────────────────────────────────────────────────────────────────
Total Leads:          12
Aktive Kunden:         6   (50%)
In Akquise:            3   (25%)
Dormant:               1   (8%)
Ehemalige:             2   (17%)
───────────────────────────────────────────────────────────────────────────

PIPELINE-WERT
───────────────────────────────────────────────────────────────────────────
Offene Opportunities:  1
Gesamt-Wert:           150'000 EUR
Gewichteter Wert:      60'000 EUR (40% Wahrscheinlichkeit)
───────────────────────────────────────────────────────────────────────────

NACH BRANCHE
───────────────────────────────────────────────────────────────────────────
finance           ███████████████  3 (25%)
public_sector     ██████████       2 (17%)
packaging         █████            1 (8%)
construction      █████            1 (8%)
fmcg              █████            1 (8%)
technology        █████            1 (8%)
retail            █████            1 (8%)
manufacturing     █████            1 (8%)
───────────────────────────────────────────────────────────────────────────

NACH LAND
───────────────────────────────────────────────────────────────────────────
CH                ██████████████████████████████████████  9 (75%)
AT                ██████████                              2 (17%)
───────────────────────────────────────────────────────────────────────────

NÄCHSTE AKTIONEN
───────────────────────────────────────────────────────────────────────────
Lead          Stage       Aktion                           Datum     Owner
───────────────────────────────────────────────────────────────────────────
Post          PROSPECT    Discovery Call vereinbaren       2026-02-15  EB
Swisscom      QUALIFIED   Workshop-Angebot erstellen       2026-02-01  MR
Migros        SUSPECT     Kontaktperson identifizieren     -           EB
───────────────────────────────────────────────────────────────────────────
```

## Mit --forecast

```bash
/pipeline-report --forecast
```

Zusätzliche Sektion:

```
REVENUE-FORECAST (nächste 12 Monate)
══════════════════════════════════════════════════════════════════════════

Quartal     Opportunities              Gewichtet (EUR)   Kumuliert
───────────────────────────────────────────────────────────────────────────
Q1 2026     -                          -                 -
Q2 2026     Swisscom (150k @ 40%)      60'000            60'000
Q3 2026     -                          -                 60'000
Q4 2026     Post (est. 100k @ 20%)     20'000            80'000
───────────────────────────────────────────────────────────────────────────
                                       Total: 80'000 EUR

Wahrscheinlichkeitsgewichtete Pipeline:

  0%  ─────────────────────────────────────────────────────  100%
  ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  60k (Swisscom)                                      150k Total

Legende: ▓ = Gewichtet   ░ = Ungewichtet
```

## Filter-Optionen

### Nach Stage

```bash
/pipeline-report --stage ACTIVE
```

```
ACTIVE CUSTOMERS (6)
───────────────────────────────────────────────────────────────────────────
Lead          Company           Industry      Country   Since       Health
───────────────────────────────────────────────────────────────────────────
LEAD-001      ALPLA             packaging     AT        2024-09-15  95
LEAD-002      PORR              construction  AT        2024-10-01  85
LEAD-003      LUKB              finance       CH        2024-06-01  92
LEAD-004      Lindt             fmcg          CH        2024-07-01  80
LEAD-006      BFE               public_sector CH        2023-06-01  88
LEAD-007      Innosuisse        public_sector CH        2026-01-01  95
───────────────────────────────────────────────────────────────────────────
```

### Nach Owner

```bash
/pipeline-report --owner EB
```

### Nach Branche

```bash
/pipeline-report --industry finance
```

## Export-Optionen

```bash
/pipeline-report --format markdown > pipeline-2026-01.md
/pipeline-report --format csv > pipeline-2026-01.csv
/pipeline-report --format json > pipeline-2026-01.json
```

## Metriken

Der Report berechnet automatisch:

| Metrik | Beschreibung |
|--------|--------------|
| **Conversion Rate** | QUALIFIED → WON Prozentsatz |
| **Average Deal Size** | Durchschnittlicher Opportunity-Wert |
| **Sales Cycle** | Durchschnittliche Zeit PROSPECT → WON |
| **Win Rate** | WON / (WON + LOST) |
| **Churn Rate** | CHURNED / (ACTIVE + CHURNED) |
| **Pipeline Coverage** | Pipeline-Wert / Ziel |
