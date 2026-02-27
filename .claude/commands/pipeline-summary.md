# /pipeline-summary - Pipeline-Übersicht generieren

Generiert eine kompakte Übersicht der gesamten Sales Pipeline.

## Usage

```bash
/pipeline-summary               # Standard-Übersicht
/pipeline-summary --period week # Mit Bewegungen diese Woche
/pipeline-summary --period month # Mit Bewegungen diesen Monat
/pipeline-summary --phase       # Fokus auf Projekt-Phasen
```

## Workflow

### Schritt 1: Daten aggregieren

```python
def aggregate_pipeline():
    leads = load_yaml("data/sales/lead-database.yaml")

    stats = {
        'total': len(leads),
        'by_stage': {},
        'by_phase': {},
        'pipeline_value': 0
    }

    for lead in leads:
        # Stage counts
        stage = lead['stage']
        stats['by_stage'][stage] = stats['by_stage'].get(stage, 0) + 1

        # Phase counts
        phase = lead.get('relationship', {}).get('project_phase')
        phase_key = str(phase) if phase is not None else 'null'
        stats['by_phase'][phase_key] = stats['by_phase'].get(phase_key, 0) + 1

        # Pipeline value
        for opp in lead.get('opportunities', []):
            if lead['stage'] in ['QUALIFIED', 'PROPOSAL', 'NEGOTIATION']:
                stats['pipeline_value'] += opp.get('value_eur', 0)

    return stats
```

### Schritt 2: Bewegungen berechnen (optional)

```python
def calculate_movements(leads, period_days=7):
    cutoff = date.today() - timedelta(days=period_days)

    movements = {
        'new_leads': 0,
        'stage_changes': 0,
        'won': 0,
        'lost': 0
    }

    for lead in leads:
        for hist in lead.get('stage_history', []):
            hist_date = parse_date(hist['date'])
            if hist_date >= cutoff:
                movements['stage_changes'] += 1
                if hist['stage'] == 'WON':
                    movements['won'] += 1
                elif hist['stage'] == 'LOST':
                    movements['lost'] += 1

        if parse_date(lead.get('created', '')) >= cutoff:
            movements['new_leads'] += 1

    return movements
```

### Schritt 3: Output generieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 PIPELINE SUMMARY                                      {DATE}        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  GESAMT: {TOTAL} Leads | Pipeline-Wert: CHF {VALUE}                    │
│                                                                         │
│  AKQUISE-PHASE                          KUNDEN-PHASE                    │
│  ─────────────────────────────────────  ────────────────────────────── │
│  SUSPECT      ████░░░░░░  {N}           ACTIVE       ████████░░  {N}   │
│  PROSPECT     ██░░░░░░░░  {N}           DORMANT      ██░░░░░░░░  {N}   │
│  QUALIFIED    ███░░░░░░░  {N}           CHURNED      █░░░░░░░░░  {N}   │
│  PROPOSAL     █░░░░░░░░░  {N}                                          │
│  NEGOTIATION  █░░░░░░░░░  {N}           LOST         ██░░░░░░░░  {N}   │
│                                                                         │
│  PROJEKT-PHASEN                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  Phase 0 (Erstgespräch)     ███░░░░░░░  {N}                            │
│  Phase 1 (Rahmenprüfung)    ██░░░░░░░░  {N}                            │
│  Phase 2 (Erwartungen)      █░░░░░░░░░  {N}                            │
│  Phase 3 (Angebot)          ██░░░░░░░░  {N}                            │
│  Phase 4 (Abschluss)        █░░░░░░░░░  {N}                            │
│  Phase 5 (Umsetzung)        ████░░░░░░  {N}                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Balkendiagramm-Logik

```python
def render_bar(count, max_count, width=10):
    filled = int((count / max_count) * width) if max_count > 0 else 0
    return '█' * filled + '░' * (width - filled)
```

## Phase-Namen Mapping

| Phase | Name |
|-------|------|
| 0 | Erstgespräch / Kennenlernen |
| 1 | Themen- & Rahmenprüfung |
| 2 | Erwartungsklärung & Vorgehen |
| 3 | Angebotsphase |
| 4 | Abschluss & Commitment |
| 5 | Umsetzung & laufendes Projekt |
| null | Keine aktive Phase |

## Beispiel-Output

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 PIPELINE SUMMARY                                      2026-01-27    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  GESAMT: 12 Leads | Pipeline-Wert: CHF 850'000                         │
│                                                                         │
│  AKQUISE-PHASE                          KUNDEN-PHASE                    │
│  ─────────────────────────────────────  ────────────────────────────── │
│  SUSPECT      █░░░░░░░░░  1             ACTIVE       ████░░░░░░  4     │
│  PROSPECT     ██░░░░░░░░  2             DORMANT      █░░░░░░░░░  1     │
│  QUALIFIED    █░░░░░░░░░  1             CHURNED      █░░░░░░░░░  1     │
│  PROPOSAL     █░░░░░░░░░  1                                            │
│  NEGOTIATION  ░░░░░░░░░░  0             LOST         █░░░░░░░░░  1     │
│                                                                         │
│  PROJEKT-PHASEN                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  Phase 0 (Erstgespräch)     ███░░░░░░░  3                              │
│  Phase 1 (Rahmenprüfung)    █░░░░░░░░░  1                              │
│  Phase 2 (Erwartungen)      ░░░░░░░░░░  0                              │
│  Phase 3 (Angebot)          █░░░░░░░░░  1                              │
│  Phase 4 (Abschluss)        ░░░░░░░░░░  0                              │
│  Phase 5 (Umsetzung)        █████░░░░░  5                              │
│  Keine Phase                ██░░░░░░░░  2                              │
│                                                                         │
│  BEWEGUNG DIESE WOCHE                                                   │
│  ─────────────────────────────────────────────────────────────────────  │
│  + Neue Leads:     0                                                    │
│  → Stage-Wechsel:  2                                                    │
│  ✓ Gewonnen:       0                                                    │
│  ✗ Verloren:       0                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Dateien

- **Datenquelle:** `data/sales/lead-database.yaml`
- **Template:** `data/sales/report-templates.yaml` (RPT-002)
