# /forecast - Umsatzprognose generieren

Generiert einen Forecast Report basierend auf Pipeline und Wahrscheinlichkeiten.

## Usage

```bash
/forecast                       # Aktueller Forecast
/forecast --quarter Q1-2026     # Für spezifisches Quartal
/forecast --scenario all        # Alle Szenarien (Best/Expected/Worst)
/forecast --top 10              # Top 10 Opportunities
```

## Workflow

### Schritt 1: Aktive Opportunities laden

```python
def load_opportunities():
    leads = load_yaml("data/sales/lead-database.yaml")

    opportunities = []
    for lead in leads:
        if lead['stage'] in ['QUALIFIED', 'PROPOSAL', 'NEGOTIATION']:
            for opp in lead.get('opportunities', []):
                opportunities.append({
                    'lead_id': lead['id'],
                    'company': lead['company']['short_name'],
                    'stage': lead['stage'],
                    'name': opp.get('name', 'Unnamed'),
                    'value': opp.get('value_eur', 0),
                    'probability': opp.get('probability', 0)
                })

    return opportunities
```

### Schritt 2: Gewichtung nach Stage

```python
STAGE_WEIGHTS = {
    'QUALIFIED': 0.30,    # 30% Wahrscheinlichkeit
    'PROPOSAL': 0.50,     # 50% Wahrscheinlichkeit
    'NEGOTIATION': 0.80   # 80% Wahrscheinlichkeit
}

def calculate_weighted_value(opp):
    base_weight = STAGE_WEIGHTS.get(opp['stage'], 0.5)
    custom_prob = opp['probability'] / 100 if opp['probability'] else base_weight
    return opp['value'] * custom_prob
```

### Schritt 3: Szenarien berechnen

```python
def calculate_scenarios(opportunities):
    scenarios = {
        'total_pipeline': sum(o['value'] for o in opportunities),
        'weighted_forecast': sum(calculate_weighted_value(o) for o in opportunities),
        'best_case': sum(o['value'] for o in opportunities if o['probability'] >= 70),
        'worst_case': sum(o['value'] for o in opportunities if o['probability'] >= 90)
    }

    # By stage breakdown
    by_stage = {}
    for stage in ['QUALIFIED', 'PROPOSAL', 'NEGOTIATION']:
        stage_opps = [o for o in opportunities if o['stage'] == stage]
        by_stage[stage] = {
            'count': len(stage_opps),
            'value': sum(o['value'] for o in stage_opps),
            'weighted': sum(calculate_weighted_value(o) for o in stage_opps)
        }

    scenarios['by_stage'] = by_stage
    return scenarios
```

### Schritt 4: Output generieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  💰 FORECAST REPORT                                       {PERIOD}      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ZUSAMMENFASSUNG                                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Pipeline-Wert (Brutto):     CHF {TOTAL_VALUE}                         │
│  Gewichtete Prognose:        CHF {WEIGHTED}                            │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SZENARIEN                                                      │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │  Best Case (≥70%):      CHF {BEST}     ████████████████████    │   │
│  │  Expected Case:         CHF {EXPECTED} ████████████░░░░░░░░    │   │
│  │  Worst Case (≥90%):     CHF {WORST}    ████████░░░░░░░░░░░░    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  NACH STAGE                                                             │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Stage         │ Anzahl │ Brutto-Wert    │ Gewichtet                   │
│  ──────────────┼────────┼────────────────┼──────────────────────────── │
│  QUALIFIED     │   {N}  │ CHF {VALUE}    │ CHF {WEIGHTED} (×0.3)       │
│  PROPOSAL      │   {N}  │ CHF {VALUE}    │ CHF {WEIGHTED} (×0.5)       │
│  NEGOTIATION   │   {N}  │ CHF {VALUE}    │ CHF {WEIGHTED} (×0.8)       │
│  ──────────────┼────────┼────────────────┼──────────────────────────── │
│  TOTAL         │   {N}  │ CHF {VALUE}    │ CHF {WEIGHTED}              │
│                                                                         │
│  TOP OPPORTUNITIES                                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│  1. {COMPANY} │ CHF {VALUE} │ {PROBABILITY}% │ {STAGE}                 │
│  2. ...                                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Gewichtungsfaktoren

| Stage | Default-Gewichtung | Begründung |
|-------|-------------------|------------|
| QUALIFIED | 30% | Bedarf bestätigt, aber noch kein Angebot |
| PROPOSAL | 50% | Angebot liegt vor, Entscheidung steht aus |
| NEGOTIATION | 80% | Verhandlung läuft, hohe Abschlusswahrscheinlichkeit |

## Szenario-Definitionen

| Szenario | Berechnung | Bedeutung |
|----------|------------|-----------|
| **Best Case** | Alle Opps mit ≥70% Prob | Optimistisches Szenario |
| **Expected Case** | Gewichtete Summe aller Opps | Realistische Prognose |
| **Worst Case** | Alle Opps mit ≥90% Prob | Konservatives Szenario |

## Beispiel-Output

```
┌─────────────────────────────────────────────────────────────────────────┐
│  💰 FORECAST REPORT                                       Q1 2026       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ZUSAMMENFASSUNG                                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Pipeline-Wert (Brutto):     CHF 850'000                               │
│  Gewichtete Prognose:        CHF 467'500                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  SZENARIEN                                                      │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │  Best Case (≥70%):      CHF 650'000  ████████████████████       │   │
│  │  Expected Case:         CHF 467'500  ██████████████░░░░░░       │   │
│  │  Worst Case (≥90%):     CHF 200'000  ██████░░░░░░░░░░░░░░       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  NACH STAGE                                                             │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Stage         │ Anzahl │ Brutto-Wert    │ Gewichtet                   │
│  ──────────────┼────────┼────────────────┼──────────────────────────── │
│  QUALIFIED     │   2    │ CHF 300'000    │ CHF  90'000 (×0.3)          │
│  PROPOSAL      │   2    │ CHF 350'000    │ CHF 175'000 (×0.5)          │
│  NEGOTIATION   │   1    │ CHF 200'000    │ CHF 160'000 (×0.8)          │
│  ──────────────┼────────┼────────────────┼──────────────────────────── │
│  TOTAL         │   5    │ CHF 850'000    │ CHF 425'000                 │
│                                                                         │
│  TOP 5 OPPORTUNITIES                                                    │
│  ─────────────────────────────────────────────────────────────────────  │
│  1. ALPLA Regional Expansion  │ CHF 200'000 │  90% │ NEGOTIATION       │
│  2. BFE Heizungsersatz        │ CHF 180'000 │  70% │ PROPOSAL          │
│  3. Novartis Patient Program  │ CHF 170'000 │  60% │ PROPOSAL          │
│  4. Swisscom Digital Workshop │ CHF 150'000 │  40% │ QUALIFIED         │
│  5. Post Innovation Lab       │ CHF 150'000 │  30% │ QUALIFIED         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Dateien

- **Datenquelle:** `data/sales/lead-database.yaml`
- **Template:** `data/sales/report-templates.yaml` (RPT-004)
