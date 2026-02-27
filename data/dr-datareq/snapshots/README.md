# Snapshots

> Zeitpunkt-bezogene Datensnapshots für Reproduzierbarkeit

## Struktur

```
snapshots/
├── YYYY-MM/              ← Monatliche Snapshots
│   ├── dach/            ← DACH-Daten zum Zeitpunkt
│   ├── international/   ← Internationale Daten
│   └── CHANGELOG.md     ← Änderungsprotokoll
└── archive/              ← Ältere Snapshots (>12 Monate)
```

## Verwendung

### Snapshot erstellen

```bash
# Automatisch (empfohlen)
python ../scripts/create_snapshot.py

# Manuell
mkdir -p $(date +%Y-%m)
cp ../sources/dach/*.csv $(date +%Y-%m)/dach/
```

### Snapshot laden

```python
import pandas as pd
from pathlib import Path

def load_snapshot(year_month: str, source: str = "dach"):
    """Lädt Daten aus einem spezifischen Snapshot."""
    path = Path(f"snapshots/{year_month}/{source}")
    return {f.stem: pd.read_csv(f) for f in path.glob("*.csv")}

# Beispiel
data = load_snapshot("2026-01", "dach")
```

## Aufbewahrungsrichtlinie

- **Letzte 12 Monate**: Vollständige Snapshots
- **Älter als 12 Monate**: Komprimiert in `archive/`
- **Jährliche Snapshots**: Permanent aufbewahrt (z.B. 2025-12, 2024-12)

## Changelog-Format

Jeder Snapshot-Ordner enthält ein `CHANGELOG.md`:

```markdown
# Snapshot YYYY-MM

## Datenquellen
- BFS: v2026.1
- OECD: Abruf 2026-01-15
- ESS: Round 11

## Änderungen vs. Vormonat
- [UPDATED] Arbeitslosenquote CH
- [NEW] WGI Governance Indicators 2025
- [FIXED] OWID CO2 Daten korrigiert
```
