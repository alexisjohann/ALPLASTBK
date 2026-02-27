# /lead-card - Lead-Detailansicht

Zeigt eine detaillierte Übersicht eines einzelnen Leads.

## Usage

```bash
/lead-card LEAD-001             # Nach Lead-ID
/lead-card ALPLA                # Nach Kurzname
/lead-card --stage PROPOSAL     # Alle Leads in Stage
```

## Workflow

### Schritt 1: Lead finden

```python
def find_lead(identifier):
    leads = load_yaml("data/sales/lead-database.yaml")

    for lead in leads:
        if lead['id'] == identifier:
            return lead
        if lead['company']['short_name'].lower() == identifier.lower():
            return lead

    return None
```

### Schritt 2: Phase-Name auflösen

```python
def get_phase_name(phase):
    phase_names = {
        0: "Erstgespräch / Kennenlernen",
        1: "Themen- & Rahmenprüfung",
        2: "Erwartungsklärung & Vorgehen",
        3: "Angebotsphase",
        4: "Abschluss & Commitment",
        5: "Umsetzung & laufendes Projekt",
        None: "Keine aktive Phase"
    }
    return phase_names.get(phase, "Unbekannt")
```

### Schritt 3: Output generieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🏢 LEAD CARD: {COMPANY_NAME}                             {LEAD_ID}     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  UNTERNEHMEN                                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Name:        {FULL_NAME}                                               │
│  Kurzname:    {SHORT_NAME}                                              │
│  Website:     {WEBSITE}                                                 │
│  Branche:     {INDUSTRY}                                                │
│  Segment:     {SEGMENT}                                                 │
│  Standort:    {CITY}, {COUNTRY}                                        │
│  Mitarbeiter: {EMPLOYEE_COUNT}                                          │
│                                                                         │
│  STATUS                                                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  Pipeline:    {STAGE}                                                   │
│  Phase:       {PHASE} ({PHASE_NAME})                                    │
│  Phase-Note:  {PHASE_NOTE}                                              │
│  Owner:       {OWNER}                                                   │
│  Fit Score:   {FIT}/100  {BAR}                                         │
│  Engagement:  {ENG}/100  {BAR}                                         │
│                                                                         │
│  HISTORIE                                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  {DATE} │ {STAGE} │ {OWNER} │ {NOTES}                                  │
│  ...                                                                    │
│                                                                         │
│  KONTAKTE                                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  👤 {NAME} - {ROLE}                                                     │
│     Beziehung: {STRENGTH}                                               │
│                                                                         │
│  OPPORTUNITIES                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  💰 {NAME}: CHF {VALUE} @ {PROBABILITY}%                               │
│                                                                         │
│  NÄCHSTE AKTION                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  📅 {DATE} │ {TYPE}                                                     │
│  {DESCRIPTION}                                                          │
│                                                                         │
│  NOTIZEN                                                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  {NOTES}                                                                │
│                                                                         │
│  TAGS: {TAG1} {TAG2} {TAG3}                                            │
│                                                                         │
│  EBF INTEGRATION                                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  Customer Registry: {CUS_REF}                                           │
│  Profile Path:      {PROFILE_PATH}                                      │
│  10C Analysis:      {HAS_10C}                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Score-Balken Rendering

```python
def render_score_bar(score, max_score=100, width=10):
    if score is None:
        return "░" * width + " (nicht bewertet)"
    filled = int((score / max_score) * width)
    return '█' * filled + '░' * (width - filled)
```

## Relationship Strength Mapping

| Wert | Anzeige |
|------|---------|
| strong | 💚 Stark |
| medium | 🟡 Mittel |
| weak | 🔴 Schwach |

## Beispiel-Output

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🏢 LEAD CARD: ALPLA Werke Alwin Lehner GmbH & Co KG        LEAD-001   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  UNTERNEHMEN                                                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Name:        ALPLA Werke Alwin Lehner GmbH & Co KG                     │
│  Kurzname:    ALPLA                                                     │
│  Website:     https://www.alpla.com                                     │
│  Branche:     packaging (plastics)                                      │
│  Segment:     enterprise                                                │
│  Standort:    Hard, AT                                                  │
│  Mitarbeiter: 23'300                                                    │
│                                                                         │
│  STATUS                                                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  Pipeline:    ACTIVE                                                    │
│  Phase:       5 (Umsetzung & laufendes Projekt)                         │
│  Phase-Note:  Aktives Projekt "Sustainability Transformation 2030"      │
│  Owner:       EB                                                        │
│  Fit Score:   92/100  █████████░                                       │
│  Engagement:  95/100  █████████░                                       │
│                                                                         │
│  HISTORIE                                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  2024-03-15 │ SUSPECT    │ EB │ Identifiziert via Branchenanalyse      │
│  2024-04-20 │ PROSPECT   │ EB │ Erstkontakt auf Packaging Fair         │
│  2024-06-10 │ QUALIFIED  │ EB │ Workshop-Interesse bestätigt           │
│  2024-07-15 │ PROPOSAL   │ EB │ Offerte für Sustainability-Projekt     │
│  2024-08-20 │ NEGOTIATION│ EB │ Vertragsverhandlung                    │
│  2024-09-15 │ WON        │ EB │ Vertrag unterschrieben                 │
│  2024-10-01 │ ACTIVE     │ EB │ Projekt gestartet                      │
│                                                                         │
│  KONTAKTE                                                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  👤 Walter Knes - VP Sustainability                                     │
│     Beziehung: 💚 Stark                                                 │
│  👤 Anna Müller - Project Manager                                       │
│     Beziehung: 🟡 Mittel                                                │
│                                                                         │
│  OPPORTUNITIES                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│  💰 Sustainability Transformation 2030: CHF 350'000 @ 100%             │
│                                                                         │
│  NÄCHSTE AKTION                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  📅 2026-02-28 │ review                                                 │
│  Quarterly Review Meeting Q1                                            │
│                                                                         │
│  NOTIZEN                                                                │
│  ─────────────────────────────────────────────────────────────────────  │
│  Familienunternehmen mit starkem Nachhaltigkeitsfokus. Sehr gute        │
│  Zusammenarbeit. Potenzial für Follow-up Projekte in anderen            │
│  Regionen (APAC, Americas).                                             │
│                                                                         │
│  TAGS: packaging sustainability family_business austria                 │
│                                                                         │
│  EBF INTEGRATION                                                        │
│  ─────────────────────────────────────────────────────────────────────  │
│  Customer Registry: CUS-ALPLA                                           │
│  Profile Path:      data/customers/alpla/                               │
│  10C Analysis:      ✓ Vorhanden                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Dateien

- **Datenquelle:** `data/sales/lead-database.yaml`
- **Template:** `data/sales/report-templates.yaml` (RPT-003)
