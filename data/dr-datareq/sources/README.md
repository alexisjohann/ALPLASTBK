# Sources

> Datenquellen für EBF Framework - 3-Ebenen-Architektur (Makro/Meso/Mikro)

## Architektur-Übersicht

```
sources/
│
├── context/              ← MAKRO: Länder-Kontext
│   ├── ch/              ← Schweiz (384 Faktoren)
│   ├── at/              ← Österreich (später)
│   └── de/              ← Deutschland (später)
│
├── industry/             ← MESO: Branchen-Kontext
│   └── finance-ch/      ← Finanzindustrie CH (130 Faktoren)
│
├── clients/              ← MIKRO: Kunden-spezifisch
│   └── ubs/             ← UBS (161 Faktoren)
│       ├── external/    ← Marktwahrnehmung (75)
│       ├── internal/    ← Operative Führung (50)
│       └── theory/      ← Organisationstheorie (36)
│
├── dach/                 ← Rohdaten DACH-Statistikämter
│   ├── ch/              ← BFS, SNB
│   ├── at/              ← Statistik Austria, OeNB
│   └── de/              ← Destatis, Bundesbank
│
├── international/        ← Internationale Quellen
│   ├── oecd/
│   ├── owid/
│   ├── eurostat/
│   └── ecb/
│
└── academic/             ← Replikationsdaten aus Papers
```

## BEATRIX Complete: 675 Faktoren

| Ebene | Ordner | Faktoren | Anteil |
|-------|--------|----------|--------|
| **MAKRO** | `context/ch/` | 384 | 57% |
| **MESO** | `industry/finance-ch/` | 130 | 19% |
| **MIKRO** | `clients/ubs/` | 161 | 24% |
| **TOTAL** | | **675** | 100% |

## Verknüpfungslogik

```
MAKRO (context/)
    │
    │  Schweizer Rahmen: Demografie, Wirtschaft, Politik, Tech, Soziales
    │
    ▼
MESO (industry/)
    │
    │  Branchenspezifika: Regulierung, Wettbewerb, Digitalisierung
    │
    ▼
MIKRO (clients/)
    │
    │  Kundenspezifika: Marktposition, Strategie, Kultur
    │
    ▼
EBF Parameter (Θ, γ, Ψ)
```

## DACH-Rohdaten

| Land | Quelle | API | Indikatoren |
|------|--------|-----|-------------|
| CH | BFS | SDMX | Demografie, Wirtschaft, Soziales |
| CH | SNB | REST | Zinsen, Inflation, Wechselkurse |
| AT | Statistik Austria | REST | Demografie, Wirtschaft |
| AT | OeNB | REST | Monetäre Indikatoren |
| DE | Destatis | GENESIS | Alle statistischen Bereiche |
| DE | Bundesbank | REST | Finanzmarktdaten |

## Dateiformat

### Kontextvektor-Dateien (YAML)
```
BCM2_{ebene}_{code}_{name}.yaml
```
Beispiele:
- `BCM2_04_KON_socio_cultural.yaml` (Makro)
- `BCM2_MESO_FI_basis.yaml` (Meso)
- `BCM2_MIKRO_UBS_INS.yaml` (Mikro)

### Rohdaten-Dateien (CSV)
```
{quelle}_{indikator}_{frequenz}.csv
```
Beispiel: `bfs_unemployment_monthly.csv`

### Header-Konvention
```csv
date,value,unit,region,source,last_updated
2026-01-01,2.3,percent,CH,BFS,2026-01-15
```

## Aktualisierung

Die Daten werden automatisch aktualisiert via:
- **Cron Jobs** (Server-basiert)
- **GitHub Actions** (Repository-basiert)
- **Manuelle Skripte** (On-Demand)

Siehe `../scripts/fetch/` für Implementierungen.

## Vertraulichkeit

⚠️ **MIKRO-Ebene:** Kundenspezifische Daten können vertraulich sein.
- Sensible Dateien in `.gitignore`
- Anonymisierte Versionen für öffentliche Repos
