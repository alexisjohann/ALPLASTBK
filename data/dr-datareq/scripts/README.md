# Scripts

> Automatisierungs-Skripte für Datenverwaltung

## Struktur

```
scripts/
├── fetch/                ← Daten-Download-Skripte
│   ├── fetch_bfs.py     ← BFS (Schweiz)
│   ├── fetch_destatis.py ← Destatis (Deutschland)
│   ├── fetch_oecd.py    ← OECD
│   └── fetch_all.py     ← Alle Quellen
├── transform/            ← Datenaufbereitung
│   ├── harmonize.py     ← DACH-Harmonisierung
│   ├── aggregate.py     ← Aggregation
│   └── impute.py        ← Fehlende Werte
└── validate/             ← Validierungsskripte
    ├── schema.py        ← Schema-Validierung
    ├── consistency.py   ← Konsistenzprüfung
    └── completeness.py  ← Vollständigkeitsprüfung
```

## Verwendung

### Alle Daten aktualisieren

```bash
# Alle Quellen abrufen
python fetch/fetch_all.py

# Nur DACH-Quellen
python fetch/fetch_all.py --region dach

# Mit Validierung
python fetch/fetch_all.py --validate
```

### Einzelne Quelle

```bash
# BFS (Schweiz)
python fetch/fetch_bfs.py --indicator unemployment

# OECD
python fetch/fetch_oecd.py --dataset OECD.SDD.TPS --subject LRHUTTTT
```

### Daten transformieren

```bash
# DACH-Daten harmonisieren
python transform/harmonize.py --input ../sources/dach --output ../sources/harmonized

# Aggregieren
python transform/aggregate.py --level quarterly
```

### Validieren

```bash
# Schema-Validierung
python validate/schema.py --config ../config/schema.yaml

# Vollständigkeit prüfen
python validate/completeness.py --report
```

## Abhängigkeiten

```bash
pip install pandas requests sdmx1 pyyaml
```

## Konfiguration

Skripte nutzen Konfigurationen aus `../config/`:
- `sources.yaml`: Quellendefinitionen
- `schema.yaml`: Datenschema
- `update-calendar.yaml`: Update-Zeitplan
