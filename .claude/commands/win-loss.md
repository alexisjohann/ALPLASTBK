# /win-loss - Win/Loss Analyse generieren

Generiert eine Analyse gewonnener und verlorener Deals mit Learnings.

## Usage

```bash
/win-loss                       # Letzte 90 Tage
/win-loss --quarter Q4-2025     # Für spezifisches Quartal
/win-loss --year 2025           # Für gesamtes Jahr
/win-loss --competitor McKinsey # Nach Konkurrent filtern
```

## Workflow

### Schritt 1: Abgeschlossene Deals laden

```python
def load_closed_deals(period_days=90):
    leads = load_yaml("data/sales/lead-database.yaml")
    cutoff = date.today() - timedelta(days=period_days)

    closed = {
        'won': [],
        'lost': [],
        'churned': []
    }

    for lead in leads:
        if lead['stage'] == 'WON':
            # Find when it was won
            for hist in lead.get('stage_history', []):
                if hist['stage'] == 'WON' and parse_date(hist['date']) >= cutoff:
                    closed['won'].append(lead)
                    break

        elif lead['stage'] == 'LOST':
            for hist in lead.get('stage_history', []):
                if hist['stage'] == 'LOST' and parse_date(hist['date']) >= cutoff:
                    closed['lost'].append(lead)
                    break

        elif lead['stage'] == 'CHURNED':
            for hist in lead.get('stage_history', []):
                if hist['stage'] == 'CHURNED' and parse_date(hist['date']) >= cutoff:
                    closed['churned'].append(lead)
                    break

    return closed
```

### Schritt 2: Metriken berechnen

```python
def calculate_metrics(closed):
    won = closed['won']
    lost = closed['lost']
    churned = closed['churned']

    total_closed = len(won) + len(lost)
    win_rate = (len(won) / total_closed * 100) if total_closed > 0 else 0

    won_value = sum(
        sum(o.get('value_eur', 0) for o in lead.get('opportunities', []))
        for lead in won
    )

    lost_value = sum(
        sum(o.get('value_eur', 0) for o in lead.get('opportunities', []))
        for lead in lost
    )

    return {
        'total_closed': total_closed,
        'won_count': len(won),
        'lost_count': len(lost),
        'churned_count': len(churned),
        'win_rate': win_rate,
        'won_value': won_value,
        'lost_value': lost_value
    }
```

### Schritt 3: Analyse-Breakdowns

```python
def analyze_wins(won_leads):
    by_source = {}
    by_industry = {}
    cycle_times = []

    for lead in won_leads:
        # By source
        source = lead.get('source', {}).get('channel', 'UNKNOWN')
        by_source[source] = by_source.get(source, 0) + 1

        # By industry
        industry = lead.get('industry', 'UNKNOWN')
        by_industry[industry] = by_industry.get(industry, 0) + 1

        # Cycle time
        history = lead.get('stage_history', [])
        if len(history) >= 2:
            first_contact = parse_date(history[0]['date'])
            won_date = parse_date(history[-1]['date'])
            cycle_times.append((won_date - first_contact).days)

    avg_cycle = sum(cycle_times) / len(cycle_times) if cycle_times else 0

    return {
        'by_source': by_source,
        'by_industry': by_industry,
        'avg_cycle_time': avg_cycle
    }

def analyze_losses(lost_leads):
    by_competitor = {}
    by_reason = {}
    by_stage = {}
    lessons = []

    for lead in lost_leads:
        analysis = lead.get('lost_analysis', {})

        # By competitor
        competitor = analysis.get('competitor', 'Kein')
        by_competitor[competitor] = by_competitor.get(competitor, 0) + 1

        # By reason
        reason = analysis.get('reason', 'Unbekannt')
        by_reason[reason] = by_reason.get(reason, 0) + 1

        # Stage before lost
        history = lead.get('stage_history', [])
        if len(history) >= 2:
            prev_stage = history[-2]['stage']
            by_stage[prev_stage] = by_stage.get(prev_stage, 0) + 1

        # Lessons learned
        lesson = analysis.get('lessons_learned')
        if lesson:
            lessons.append(lesson)

    return {
        'by_competitor': by_competitor,
        'by_reason': by_reason,
        'by_stage': by_stage,
        'lessons': lessons
    }

def analyze_churn(churned_leads):
    by_reason = {}
    preventable_count = 0
    total_ltv = 0

    for lead in churned_leads:
        analysis = lead.get('churn_analysis', {})

        reason = analysis.get('reason', 'Unbekannt')
        by_reason[reason] = by_reason.get(reason, 0) + 1

        if analysis.get('preventable'):
            preventable_count += 1

        total_ltv += analysis.get('total_lifetime_value_eur', 0)

    return {
        'by_reason': by_reason,
        'preventable': preventable_count,
        'total_ltv': total_ltv
    }
```

### Schritt 4: Output generieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📈 WIN/LOSS ANALYSIS                                     {PERIOD}      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ÜBERSICHT                                                              │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Abgeschlossen:  {TOTAL}                                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  ✓ Gewonnen:     {WON}    │ CHF {WON_VALUE}    │ {BAR}                 │
│  ✗ Verloren:     {LOST}   │ CHF {LOST_VALUE}   │ {BAR}                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  Win Rate:       {RATE}%                                                │
│                                                                         │
│  GEWONNENE DEALS                                                        │
│  Nach Source / Nach Branche / Ø Sales Cycle                             │
│                                                                         │
│  VERLORENE DEALS                                                        │
│  Nach Konkurrent / Nach Grund / Bei welcher Stage                       │
│                                                                         │
│  LESSONS LEARNED                                                        │
│  • {LESSON_1}                                                           │
│                                                                         │
│  CHURN (Ehemalige Kunden)                                               │
│  Churned / Vermeidbar / Verlorener LTV                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Loss Reason Kategorien

| Kategorie | Beschreibung |
|-----------|--------------|
| `price` | Preis zu hoch |
| `timing` | Timing passt nicht |
| `scope` | Scope nicht passend |
| `competitor` | Konkurrent gewählt |
| `budget` | Budget gestrichen |
| `champion_left` | Ansprechpartner gewechselt |
| `other` | Andere Gründe |

## Churn Reason Kategorien

| Kategorie | Beschreibung |
|-----------|--------------|
| `budget_cuts` | Budgetkürzungen |
| `reorganization` | Reorganisation |
| `dissatisfaction` | Unzufriedenheit |
| `competitor_switch` | Wechsel zu Konkurrenz |
| `project_end` | Projekt natürlich beendet |
| `contact_left` | Hauptkontakt verlassen |

## Beispiel-Output

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📈 WIN/LOSS ANALYSIS                                     Q4 2025       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ÜBERSICHT                                                              │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Abgeschlossen:  8 Deals                                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  ✓ Gewonnen:     5       │ CHF 780'000       │ ████████████░░░░        │
│  ✗ Verloren:     3       │ CHF 320'000       │ ████████░░░░░░░░        │
│  ─────────────────────────────────────────────────────────────────────  │
│  Win Rate:       62.5%                                                  │
│                                                                         │
│  GEWONNENE DEALS                                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Nach Source:                  Nach Branche:                            │
│  ├── REFERRAL:    3            ├── Finance:      2                     │
│  ├── INBOUND:     1            ├── Energy:       2                     │
│  └── OUTBOUND:    1            └── Packaging:    1                     │
│                                                                         │
│  Ø Sales Cycle:   87 Tage                                              │
│                                                                         │
│  VERLORENE DEALS                                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  Nach Konkurrent:              Nach Grund:                              │
│  ├── McKinsey:    1            ├── Preis:        1                     │
│  ├── BCG:         1            ├── Timing:       1                     │
│  └── Kein:        1            └── Budget:       1                     │
│                                                                         │
│  Bei welcher Stage verloren:                                            │
│  ├── PROPOSAL:     2  (Angebot nicht überzeugend?)                     │
│  └── NEGOTIATION:  1  (Verhandlung gescheitert?)                       │
│                                                                         │
│  LESSONS LEARNED                                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  • "Früher C-Level Engagement bei Enterprise-Kunden"                    │
│  • "Pricing-Transparenz von Anfang an kommunizieren"                    │
│  • "Budget-Freeze-Risiken früher identifizieren"                        │
│                                                                         │
│  CHURN (Ehemalige Kunden)                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  Churned:         1                                                     │
│  Vermeidbar:      0 (0%)                                               │
│  Verlorener LTV:  CHF 85'000                                           │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  EMPFEHLUNGEN                                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  1. Referral-Channel weiter stärken (60% der Wins)                     │
│  2. Proposal-zu-Win Conversion verbessern (2 Losses in Stage)          │
│  3. Frühzeitige Budget-Validierung einführen                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Dateien

- **Datenquelle:** `data/sales/lead-database.yaml`
- **Template:** `data/sales/report-templates.yaml` (RPT-005)
