# /action-list - Offene Aktionen anzeigen

Generiert eine Übersicht aller offenen Aktionen gruppiert nach Owner.

## Usage

```bash
/action-list                    # Alle offenen Aktionen
/action-list --owner EB         # Nur Aktionen für Owner EB
/action-list --overdue          # Nur überfällige Aktionen
/action-list --week             # Aktionen der nächsten 7 Tage
```

## Workflow

### Schritt 1: Daten laden

```python
def load_actions():
    leads = load_yaml("data/sales/lead-database.yaml")

    actions = []
    for lead in leads:
        if lead.get('next_action') and lead['stage'] not in ['CHURNED', 'LOST']:
            actions.append({
                'lead_id': lead['id'],
                'company': lead['company']['short_name'],
                'owner': lead['relationship']['owner'],
                'phase': lead['relationship'].get('project_phase'),
                'action': lead['next_action'],
                'stage': lead['stage']
            })

    return actions
```

### Schritt 2: Filtern (falls Parameter)

```python
def filter_actions(actions, owner=None, overdue=False, week=False):
    today = date.today()

    if owner:
        actions = [a for a in actions if a['owner'] == owner]

    if overdue:
        actions = [a for a in actions if parse_date(a['action']['date']) < today]

    if week:
        week_end = today + timedelta(days=7)
        actions = [a for a in actions if parse_date(a['action']['date']) <= week_end]

    return actions
```

### Schritt 3: Gruppieren und Sortieren

```python
def group_by_owner(actions):
    grouped = {}
    for action in actions:
        owner = action['owner']
        if owner not in grouped:
            grouped[owner] = []
        grouped[owner].append(action)

    # Sort each owner's actions by date
    for owner in grouped:
        grouped[owner].sort(key=lambda x: x['action']['date'])

    return grouped
```

### Schritt 4: Output generieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📋 ACTION LIST                                           {DATE}        │
├─────────────────────────────────────────────────────────────────────────┤
│  OWNER: {OWNER} ({N} offene Aktionen)                                   │
│  ═══════════════════════════════════════════════════════════════════   │
│                                                                         │
│  ☐ {COMPANY} ({LEAD_ID})                                               │
│    Phase: {PHASE} ({PHASE_NAME})                                        │
│    Aktion: {DESCRIPTION}                                                │
│    Typ: {TYPE}                                                          │
│    Fällig: {DATE} ({DAYS_HINT})                                        │
│    Priorität: {PRIORITY}                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prioritäts-Logik

| Bedingung | Priorität | Symbol |
|-----------|-----------|--------|
| Überfällig | HIGH | 🔴 |
| Fällig in ≤7 Tagen | MEDIUM | 🟡 |
| Fällig in >7 Tagen | NORMAL | 🟢 |

## Beispiel-Output

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📋 ACTION LIST                                           2026-01-27    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  OWNER: EB (2 offene Aktionen)                                          │
│  ═══════════════════════════════════════════════════════════════════   │
│                                                                         │
│  🟡 Post (LEAD-008)                                                     │
│     Phase: 0 (Erstgespräch / Kennenlernen)                              │
│     Aktion: Discovery Call vereinbaren                                  │
│     Typ: meeting                                                        │
│     Fällig: 2026-02-15 (in 19 Tagen)                                   │
│                                                                         │
│  🟢 Swisscom (LEAD-009)                                                 │
│     Phase: 1 (Themen- & Rahmenprüfung)                                  │
│     Aktion: Workshop-Scope definieren                                   │
│     Typ: workshop                                                       │
│     Fällig: 2026-02-20 (in 24 Tagen)                                   │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  OWNER: MR (1 offene Aktion)                                            │
│  ═══════════════════════════════════════════════════════════════════   │
│                                                                         │
│  🟡 Novartis (LEAD-010)                                                 │
│     Phase: 3 (Angebotsphase)                                            │
│     Aktion: Angebot finalisieren                                        │
│     Typ: proposal                                                       │
│     Fällig: 2026-02-01 (in 5 Tagen)                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

ZUSAMMENFASSUNG
───────────────
Total: 3 offene Aktionen
🔴 Überfällig: 0
🟡 Diese Woche: 1
🟢 Später: 2
```

## Dateien

- **Datenquelle:** `data/sales/lead-database.yaml`
- **Template:** `data/sales/report-templates.yaml` (RPT-001)
