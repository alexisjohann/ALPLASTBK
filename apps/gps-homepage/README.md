# GPS Homepage — Global Preference Survey Dashboard

Interactive dashboard for the [Global Preference Survey (GPS)](https://gps.econ.uni-bonn.de) data, integrated with the Evidence-Based Framework (EBF).

## Overview

The GPS is a globally representative dataset on economic preferences from 80,000 individuals across 76 countries, collected as part of the 2012 Gallup World Poll.

**Publication:** Falk, A., Becker, A., Dohmen, T., Enke, B., Huffman, D., & Sunde, U. (2018). Global Evidence on Economic Preferences. *Quarterly Journal of Economics*, 133(4), 1645-1692. [DOI: 10.1093/qje/qjy013](https://doi.org/10.1093/qje/qjy013)

## Features

- **Home**: Overview of the 6 preference dimensions with key statistics and variance decomposition chart
- **Rankings**: Interactive country rankings by any preference dimension, filterable by region
- **Compare**: Side-by-side comparison of two countries with radar chart visualization
- **About**: Methodology, EBF integration details, research team, and data access links

## Quick Start

```bash
cd apps/gps-homepage
pip install flask
python app.py
# Open http://localhost:5001
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/data` | Full GPS dataset |
| `GET /api/countries` | All countries with preference scores |
| `GET /api/country/<ISO>` | Single country by ISO 3166-1 alpha-3 code |
| `GET /api/rankings/<pref>` | Countries ranked by preference (patience, risktaking, posrecip, negrecip, altruism, trust) |
| `GET /api/compare/<ISO_A>/<ISO_B>` | Compare two countries with Euclidean distance |
| `GET /api/regions` | Regional averages |
| `GET /api/metadata` | Dataset metadata and EBF integration info |
| `GET /api/findings` | Key findings (variance decomposition, GDP correlations) |

## EBF Integration

GPS preference dimensions map to EBF context dimensions:

| GPS Dimension | EBF Psi Mapping | 10C CORE | Parameter Ref |
|---------------|-----------------|----------|---------------|
| Patience | Psi_T (Temporal) | WHEN (V) | PAR-GPS-001 |
| Risk Taking | Psi_C (Cognitive) | READY (AV) | PAR-GPS-002 |
| Positive Reciprocity | Psi_S (Social) | HOW (B) | PAR-GPS-003 |
| Negative Reciprocity | Psi_S (Social) | HOW (B) | PAR-GPS-004 |
| Altruism | Psi_S (Social) | WHAT (C) | PAR-GPS-005 |
| Trust | Psi_S (Social) | WHO (AAA) | PAR-GPS-006 |

GPS data serve as **anchor parameters** for the Parameter Context Transformation (PCT).

## Data

Country-level preference scores are stored in `static/gps_data.json`. Values are standardized z-scores (mean=0, sd=1 across countries) from the published GPS dataset.

## Structure

```
apps/gps-homepage/
    app.py                  # Flask backend
    README.md               # This file
    templates/
        index.html          # Main dashboard (HTML/CSS/JS)
    static/
        gps_data.json       # Country-level preference data (76 countries)
```
