# /new-lead - Neuen Lead erfassen

Erfasst einen neuen Lead in der Lead-Datenbank mit automatischem Projekt-Phasen-Vorschlag.

## Usage

```bash
/new-lead                          # Interaktiver Modus
/new-lead --quick                  # Schnelleingabe
/new-lead --from-note "..."        # Aus Freitext extrahieren
```

## Workflow

### Interaktiver Modus (Default)

Führe den Benutzer durch die 5 Schritte:

**SCHRITT 1: BASIS-IDENTIFIKATION**
```
Unternehmensname (vollständig)? → z.B. "Schweizerische Post AG"
Kurzname (für Anzeige)? → z.B. "Post"
Website (optional)? → z.B. "https://www.post.ch"
```

**SCHRITT 2: KLASSIFIKATION**
```
Branche? → finance | packaging | construction | fmcg | pharma_health |
           energy | technology | public_sector | manufacturing |
           retail | professional_services

Land? → CH | AT | DE | Andere

Segment? → enterprise | mid_market | smb | government
```

**SCHRITT 3: PIPELINE-STATUS**
```
Aktueller Status? → SUSPECT | PROSPECT | QUALIFIED | PROPOSAL | NEGOTIATION

Owner? → EB | MR | Andere

Source? → REFERRAL | INBOUND | OUTBOUND | RESEARCH
```

**SCHRITT 4: PROJEKT-PHASE (AUTO-SUGGEST)**

Wende den Auto-Suggest Algorithmus an:

```python
def suggest_phase(stage, next_action=None):
    # Primär-Mapping
    mapping = {
        'SUSPECT': 0,
        'PROSPECT': 0,
        'QUALIFIED': 1,  # oder 2 bei Scope-Diskussion
        'PROPOSAL': 3,
        'NEGOTIATION': 4,
        'WON': 4,  # oder 5 bei aktivem Projekt
        'ACTIVE': 5,
        'DORMANT': 5,
        'REACTIVATION': 0,
        'CHURNED': None,
        'LOST': None
    }

    phase = mapping.get(stage, 0)

    # Override für QUALIFIED
    if stage == 'QUALIFIED' and next_action:
        if 'scope' in next_action.lower() or 'erwartung' in next_action.lower():
            phase = 2

    return phase
```

Zeige dem Benutzer:
```
┌─────────────────────────────────────────────────────────────────┐
│  🤖 AUTO-VORSCHLAG                                              │
│                                                                 │
│  Basierend auf: Stage = {STAGE}                                 │
│  → Vorgeschlagene Phase: {PHASE} ({PHASE_NAME})                │
│  Begründung: "{REASON}"                                         │
│                                                                 │
│  Bestätigen (Enter) oder ändern (0-5)?                         │
└─────────────────────────────────────────────────────────────────┘
```

**SCHRITT 5: ZUSATZINFORMATIONEN (optional)**
```
Nächste Aktion? → Typ, Datum, Beschreibung
Kontaktperson? → Name, Rolle
Notizen? → Freitext
Tags? → Auswahl oder Freitext
```

### Schnelleingabe (--quick)

Nur Pflichtfelder abfragen:
```
Unternehmen | Branche | Land | Stage | Owner | Source
```

Beispiel:
```
Post | professional_services | CH | PROSPECT | EB | OUTBOUND
```

Phase wird automatisch vorgeschlagen und ohne Rückfrage übernommen.

### Aus Freitext (--from-note)

Extrahiere automatisch aus Freitext:

```
/new-lead --from-note "Hatte heute ein gutes Gespräch mit Hans Müller
von der Migros. Er ist Head of Sustainability und interessiert sich
für Behavioral Interventions. Sollten nächste Woche einen Call machen."
```

Extrahiere:
- Unternehmen: Migros
- Kontakt: Hans Müller, Head of Sustainability
- Stage: PROSPECT (implizit durch "Gespräch")
- Next Action: Call nächste Woche
- Phase: 0 (auto-suggest)

Zeige Extraktion zur Bestätigung, dann Lead anlegen.

## Output

Nach Erstellung:
1. Zeige Lead-Zusammenfassung
2. Füge Lead zu `data/sales/lead-database.yaml` hinzu
3. Aktualisiere `pipeline_summary`
4. Generiere nächste Lead-ID (LEAD-{NNN})

```
✓ Lead LEAD-013 erstellt

  Unternehmen:    Post
  Stage:          PROSPECT
  Phase:          0 (Erstgespräch / Kennenlernen)
  Owner:          EB
  Nächste Aktion: Discovery Call (2026-02-15)
```

## Dateien

- **Datenbank:** `data/sales/lead-database.yaml`
- **Workflow-Doku:** `data/sales/LEAD-ENTRY-WORKFLOW.md`
- **Schema:** Siehe `schema` Sektion in lead-database.yaml

## Validierung

| Feld | Pflicht | Validierung |
|------|---------|-------------|
| company.name | ✓ | Nicht leer |
| company.short_name | ✓ | Nicht leer |
| industry | ✓ | In Taxonomie |
| stage | ✓ | In pipeline_stages |
| headquarters.country | ✓ | ISO-Code |
| relationship.owner | ✓ | Nicht leer |
| project_phase | Auto | 0-5 oder null |

## Beispiel-Session

```
> /new-lead

SCHRITT 1: BASIS-IDENTIFIKATION
Unternehmensname? Novartis AG
Kurzname? Novartis
Website? https://www.novartis.com

SCHRITT 2: KLASSIFIKATION
Branche? pharma_health
Land? CH
Segment? enterprise

SCHRITT 3: PIPELINE-STATUS
Status? QUALIFIED
Owner? MR
Source? REFERRAL

SCHRITT 4: PROJEKT-PHASE

┌─────────────────────────────────────────────────────────────────┐
│  🤖 AUTO-VORSCHLAG                                              │
│                                                                 │
│  Basierend auf: Stage = QUALIFIED                               │
│  → Vorgeschlagene Phase: 1 (Themen- & Rahmenprüfung)           │
│  Begründung: "Thema & Rahmen geprüft (SQL)"                    │
│                                                                 │
│  Bestätigen (Enter) oder ändern (0-5)? _                       │
└─────────────────────────────────────────────────────────────────┘

> 2

Phase geändert auf: 2 (Erwartungsklärung & Vorgehen)
Begründung? Workshop-Scope wird aktuell definiert

SCHRITT 5: ZUSATZINFORMATIONEN
Nächste Aktion? proposal | 2026-02-10 | Workshop-Angebot erstellen
Kontaktperson? Dr. Anna Schmidt | VP Innovation
Notizen? Interesse an Patient Adherence Programm
Tags? pharma, innovation, switzerland

✓ Lead LEAD-014 erstellt

  Unternehmen:    Novartis
  Stage:          QUALIFIED
  Phase:          2 (Erwartungsklärung & Vorgehen)
  Owner:          MR
  Nächste Aktion: Workshop-Angebot (2026-02-10)
```
