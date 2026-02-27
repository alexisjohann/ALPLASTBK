# Config

> Konfigurationsdateien für Datenverwaltung

## Dateien

### sources.yaml
Zentrales Register aller Datenquellen:

```yaml
sources:
  bfs:
    name: "Bundesamt für Statistik (CH)"
    type: sdmx
    base_url: "https://sdmx.bfs.admin.ch/public/ws/..."
    update_frequency: monthly
    indicators:
      - unemployment
      - gdp
      - population

  oecd:
    name: "OECD"
    type: sdmx
    base_url: "https://sdmx.oecd.org/..."
    update_frequency: quarterly
```

### update-calendar.yaml
Update-Zeitplan für automatische Aktualisierungen:

```yaml
schedule:
  daily:
    - owid  # Our World in Data (GitHub)

  monthly:
    - bfs
    - destatis
    - statistik_austria

  quarterly:
    - oecd
    - ecb

  annual:
    - ess  # European Social Survey
    - wvs  # World Values Survey
```

### schema.yaml
Datenschema für Validierung:

```yaml
schema:
  required_columns:
    - date
    - value
    - unit
    - region
    - source

  date_format: "YYYY-MM-DD"

  value_constraints:
    unemployment:
      min: 0
      max: 100
      unit: percent
```

## Erstellen neuer Konfigurationen

1. YAML-Datei in diesem Ordner erstellen
2. Skripte in `../scripts/` anpassen
3. In README dokumentieren
