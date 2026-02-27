# /lead-update - Lead-Stage aktualisieren

Aktualisiert den Pipeline-Stage eines Leads.

## Syntax

```bash
/lead-update LEAD-013 PROSPECT              # Stage ändern
/lead-update LEAD-013 QUALIFIED --notes "Budget bestätigt"
/lead-update LEAD-013 LOST --competitor "McKinsey" --reason "Brand preference"
/lead-update LEAD-013 --score 85            # Nur Fit Score updaten
/lead-update LEAD-013 --owner MR            # Owner ändern
```

## Stage-Übergänge

```
SUSPECT    → PROSPECT
PROSPECT   → QUALIFIED | LOST
QUALIFIED  → PROPOSAL | LOST
PROPOSAL   → NEGOTIATION | LOST
NEGOTIATION→ WON | LOST
WON        → ACTIVE
ACTIVE     → DORMANT | CHURNED
DORMANT    → ACTIVE | REACTIVATION | CHURNED
CHURNED    → REACTIVATION
LOST       → REACTIVATION
REACTIVATION → PROSPECT | QUALIFIED | ACTIVE | LOST
```

## Workflow

```yaml
# 1. Lead laden
lead = load("LEAD-013")

# 2. Stage-Übergang validieren
validate_transition(lead.stage, new_stage)

# 3. Stage History erweitern
lead.stage_history.append({
  stage: new_stage,
  date: $TODAY,
  owner: $OWNER,
  notes: $NOTES
})

# 4. Lead aktualisieren
lead.stage = new_stage
lead.updated = $TODAY

# 5. Bei LOST: lost_analysis hinzufügen
if new_stage == LOST:
  lead.lost_analysis = {
    competitor: $COMPETITOR,
    reason: $REASON,
    lessons_learned: $LESSONS
  }

# 6. Bei CHURNED: churn_analysis hinzufügen
if new_stage == CHURNED:
  lead.churn_analysis = {
    reason: $REASON,
    preventable: $BOOL,
    win_back_potential: $POTENTIAL
  }

# 7. Bei WON → ACTIVE: EBF Integration vorschlagen
if old_stage == WON and new_stage == ACTIVE:
  suggest_ebf_integration(lead)

# 8. Pipeline Summary aktualisieren
update_pipeline_summary()
```

## Bei LOST - Pflichtfelder

```yaml
lost_analysis:
  competitor: "Name des Konkurrenten"      # Wer hat gewonnen?
  reason: "Kurze Begründung"               # Warum verloren?
  decision_maker: "CEO/CFO/etc."           # Wer hat entschieden?
  price_competitive: true/false            # War Preis das Problem?
  proposal_quality: high/medium/low        # Wie war unser Angebot?
  lessons_learned: |                       # Was lernen wir?
    - Punkt 1
    - Punkt 2
  reapproach_date: "2027-01-01"            # Wann wieder ansprechen?
```

## Bei CHURNED - Pflichtfelder

```yaml
churn_analysis:
  reason: "Budgetkürzungen"                # Warum weg?
  preventable: true/false                  # Hätten wir es verhindern können?
  win_back_potential: high/medium/low      # Chance auf Rückgewinnung?
  last_project: "Projektname"              # Letztes Projekt
  total_lifetime_value_eur: 85000          # Gesamtumsatz mit Kunde
```

## Bei WON → ACTIVE

Claude schlägt automatisch vor:

```
🎉 Deal gewonnen! LEAD-013 ist jetzt ACTIVE.

Nächste Schritte für EBF-Integration:

1. Customer Registry updaten:
   /customer-add LEAD-013

2. Customer Profile erstellen:
   data/customers/{code}/{code}_profile.yaml

3. 10C-Analyse durchführen:
   /design-model --customer {code}

Soll ich mit Schritt 1 beginnen? (j/n)
```

## Output

```
✅ Lead aktualisiert: LEAD-013

┌─────────────────────────────────────────────────────────────┐
│  LEAD-013: Swisscom AG                                      │
├─────────────────────────────────────────────────────────────┤
│  Stage:     QUALIFIED → PROPOSAL                            │
│  Updated:   2026-01-27                                      │
│  Owner:     MR                                              │
│  Notes:     Workshop-Angebot erstellt                       │
└─────────────────────────────────────────────────────────────┘

Stage History:
  2025-09-01  SUSPECT      MR
  2025-10-15  PROSPECT     MR  "Intro via Board-Kontakt"
  2025-12-01  QUALIFIED    MR  "Budget vorhanden"
  2026-01-27  PROPOSAL     MR  "Workshop-Angebot erstellt"  ← NEU
```

## Beispiele

```bash
# Einfache Stage-Änderung
/lead-update LEAD-008 QUALIFIED

# Mit Notizen
/lead-update LEAD-010 PROPOSAL --notes "Workshop-Angebot für 150k"

# Deal verloren
/lead-update LEAD-012 LOST --competitor "BCG" --reason "Existing relationship"

# Kunde verloren
/lead-update LEAD-005 CHURNED --reason "Budgetkürzungen" --preventable false

# Owner ändern
/lead-update LEAD-009 --owner MR

# Fit Score aktualisieren
/lead-update LEAD-008 --score 88 --engagement 45
```
