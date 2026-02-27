# DR-DATAREQ: Data Requirements Repository

> Erweiterbare Datenstruktur für Appendix DR (REF-DATAREQ)

## Ordnerstruktur

```
data/dr-datareq/
├── README.md              ← Diese Datei
├── snapshots/             ← Zeitpunkt-bezogene Datensnapshots
│   └── YYYY-MM/          ← Monatliche Snapshots
├── sources/               ← Rohdaten von externen Quellen
│   ├── dach/             ← DACH-spezifische Daten (CH, AT, DE)
│   ├── international/    ← OECD, OWID, Eurostat
│   └── academic/         ← Replikationsdaten aus Papers
├── scripts/               ← Automatisierungs-Skripte
│   ├── fetch/            ← Daten-Download-Skripte
│   ├── transform/        ← Datenaufbereitung
│   └── validate/         ← Validierungsskripte
├── config/                ← Konfigurationsdateien
│   ├── sources.yaml      ← Quellenregister
│   └── update-calendar.yaml ← Update-Kalender
└── papers/                ← Akademische Quellen (PDFs, BibTeX)
    └── by-psi-dimension/ ← Nach Ψ-Dimension organisiert
```

## Verwendung

### Neuen Snapshot hinzufügen

```bash
# Monatlichen Snapshot erstellen
mkdir -p snapshots/$(date +%Y-%m)
cp sources/dach/*.csv snapshots/$(date +%Y-%m)/
```

### Daten aktualisieren

```bash
# Alle DACH-Quellen aktualisieren
python scripts/fetch/fetch_dach_sources.py

# Spezifische Quelle aktualisieren
python scripts/fetch/fetch_bfs.py --indicator=unemployment
```

### Daten validieren

```bash
# Alle Daten gegen Schema validieren
python scripts/validate/validate_all.py

# Konsistenzprüfung
python scripts/validate/check_consistency.py
```

## Namenskonventionen

### Dateien
- `{source}_{indicator}_{date}.{format}`
- Beispiel: `bfs_unemployment_2026-01.csv`

### Snapshots
- `{YYYY-MM}/` für monatliche Snapshots
- `{YYYY-MM-DD}/` für tägliche Snapshots (falls nötig)

## Datenquellen-Status

| Quelle | Typ | Update-Frequenz | Automatisiert |
|--------|-----|-----------------|---------------|
| BFS (CH) | SDMX API | Monatlich | ✅ |
| Statistik Austria | REST API | Monatlich | ✅ |
| Destatis (DE) | GENESIS API | Monatlich | ✅ |
| OECD | SDMX API | Quartalsweise | ✅ |
| OWID | GitHub | Täglich | ✅ |
| Eurostat | REST API | Monatlich | ⏳ |
| ESS | Download | Alle 2 Jahre | ❌ |

## Verknüpfung mit EBF

Dieser Ordner unterstützt:
- **Appendix DR** (REF-DATAREQ): Data Requirements Reference
- **Appendix CAL** (METHOD-LLMMC): Calibration Pipeline
- **Appendix BBB** (CORE-WHERE): Parameter Repository
- **Appendix PM** (REF-PARAMETH): Parameter Methodology

## Beitragen

1. Neue Datenquelle hinzufügen:
   - Fetch-Skript in `scripts/fetch/` erstellen
   - Eintrag in `config/sources.yaml` hinzufügen
   - Update-Kalender in `config/update-calendar.yaml` aktualisieren

2. Neuen Snapshot erstellen:
   - Daten in `sources/` aktualisieren
   - Snapshot-Ordner erstellen
   - Changelog dokumentieren

---

*Teil des EBF Framework | Appendix DR (REF-DATAREQ)*
