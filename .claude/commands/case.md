# /case - EBF Case Registry Query

Query the 10C-indexed case library for examples, insights, and intervention patterns.

## Usage

```bash
/case CASE-001                    # Spezifischen Case abrufen
/case --domain health             # Alle Gesundheits-Cases
/case --tag nudge                 # Alle Nudge-Cases
/case --stage action              # Cases in Action-Phase
/case --gamma ">0.5"              # Hohe Komplementarität
/case --segment present-biased    # Bestimmtes Segment
/case --hierarchy L2              # L2-Interventionen
/case --list                      # Alle Cases auflisten
/case --stats                     # Statistiken anzeigen
/case --similar CASE-001          # Ähnliche Cases finden
```

## Kombinations-Abfragen

```bash
/case --domain health --stage contemplation
/case --segment loss-averse --hierarchy L3
/case --tag default --domain finance
```

## 10C Filter-Dimensionen

| Filter | Dimension | Beispiele |
|--------|-----------|-----------|
| `--who` | WHO | `heterogeneity=high`, `levels=individual` |
| `--what` | WHAT | `primary=health_behavior` |
| `--gamma` | HOW | `">0.5"`, `"<0.3"` |
| `--psi` | WHEN | `culture`, `choice_architecture` |
| `--confidence` | WHERE | `high`, `medium`, `low` |
| `--aware` | AWARE | `">0.5"`, `type=implicit` |
| `--ready` | READY | `">0.6"` |
| `--stage` | STAGE | `precontemplation`, `action`, `maintenance` |
| `--hierarchy` | HIERARCHY | `L0`, `L1`, `L2`, `L3` |

## Output-Formate

- **Default:** Vollständige Case-Anzeige mit allen 10C-Dimensionen
- `--brief`: Einzeilige Zusammenfassung pro Case
- `--json`: JSON-Output für Weiterverarbeitung
- `--table`: Tabellenformat für Vergleiche

## Beispiel-Workflow

1. **Exploration:** `/case --stats` → Überblick über verfügbare Cases
2. **Filterung:** `/case --domain health --stage contemplation`
3. **Detail:** `/case CASE-004` → Vollständige Analyse
4. **Ähnlichkeit:** `/case --similar CASE-004` → Verwandte Cases

## Case hinzufügen

Neue Cases werden in `data/case-registry.yaml` eingetragen:

```yaml
CASE-XXX:
  name: "Kurzer prägnanter Name"
  description: "1-2 Sätze Beschreibung"

  10C:
    WHO:
      levels: [individual]
      heterogeneity: medium
    # ... alle 9 Dimensionen ...

  domain: [health, finance]
  tags: [nudge, default]

  insight: "Kern-Einsicht in einem Satz"
  implication: "Praktische Anwendung"
```

## Referenzen

- **Registry:** `data/case-registry.yaml`
- **Query Script:** `scripts/query_cases.py`
- **10C Framework:** `docs/frameworks/core-framework-definition.yaml`
