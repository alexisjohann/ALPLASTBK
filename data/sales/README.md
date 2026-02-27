# Sales Pipeline - FehrAdvice & Partners AG

> Zentrale Datenbank für alle Kundenbeziehungen

---

## Quick Start

```bash
/new-lead                  # Neuen Lead erfassen (interaktiv)
/new-lead --quick          # Schnelleingabe
/new-lead --from-note "..."# Aus Freitext extrahieren
```

**Workflow-Dokumentation:** [LEAD-ENTRY-WORKFLOW.md](LEAD-ENTRY-WORKFLOW.md)

---

## Übersicht

Die Lead-Datenbank (`lead-database.yaml`) ist die **Single Source of Truth (SSOT)** für alle Kundenbeziehungen bei FehrAdvice:

| Kategorie | Beschreibung | Beispiele |
|-----------|--------------|-----------|
| **Aktive Kunden** | Laufende Projekte oder Verträge | ALPLA, LUKB, BFE |
| **Ruhende Kunden** | Keine aktiven Projekte, aber Beziehung intakt | UBS |
| **Ehemalige Kunden** | Beziehung beendet (Churned) | - |
| **Verlorene Deals** | Nie Kunde geworden (Lost) | - |
| **Prospects** | Potenzielle Neukunden in Akquise | Post, Swisscom |
| **Fördergeber** | Forschungsfinanzierung | Innosuisse |

---

## Pipeline-Stages

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AKQUISE-PHASE                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  SUSPECT → PROSPECT → QUALIFIED → PROPOSAL → NEGOTIATION → WON         │
│     │         │           │           │            │          │         │
│     └─────────┴───────────┴───────────┴────────────┘          │         │
│                           ↓                                    │         │
│                         LOST ←─────────────────────────────────┘         │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  KUNDEN-PHASE                                                           │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│                      WON → ACTIVE → DORMANT → CHURNED                   │
│                                       ↑                                 │
│                                       │                                 │
│                               REACTIVATION ←──────────────────────┐     │
│                                       ↓                           │     │
│                               ┌───────┴───────┐                   │     │
│                               ↓               ↓                   │     │
│                            ACTIVE           LOST                  │     │
│                                                                   │     │
│                      CHURNED ─────────────────────────────────────┘     │
│                      LOST ────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Stage-Definitionen

| Stage | Phase | Beschreibung | Nächste Stages |
|-------|-------|--------------|----------------|
| **SUSPECT** | Akquise | Identifiziert, aber noch kein Kontakt | PROSPECT |
| **PROSPECT** | Akquise | Erster Kontakt hergestellt | QUALIFIED, LOST |
| **QUALIFIED** | Akquise | Bedarf und Budget qualifiziert (SQL) | PROPOSAL, LOST |
| **PROPOSAL** | Akquise | Angebot erstellt und präsentiert | NEGOTIATION, LOST |
| **NEGOTIATION** | Akquise | Vertragsverhandlung | WON, LOST |
| **WON** | Kunde | Deal gewonnen, Onboarding | ACTIVE |
| **ACTIVE** | Kunde | Aktiver Kunde mit laufenden Projekten | DORMANT, CHURNED |
| **DORMANT** | Kunde | Kunde ohne aktive Projekte (ruhend) | ACTIVE, REACTIVATION, CHURNED |
| **CHURNED** | Ehemalig | Ehemaliger Kunde (Beziehung beendet) | REACTIVATION |
| **LOST** | Ehemalig | Deal verloren (nie Kunde geworden) | REACTIVATION |
| **REACTIVATION** | Reaktivierung | Reaktivierungsversuch läuft | PROSPECT, QUALIFIED, ACTIVE, LOST |

---

## Team Registry (Owner-Verzeichnis)

Jeder Lead hat einen **Owner** - die verantwortliche Person bei FehrAdvice.

### Superkey-System

```
OWN-{CODE}  →  Eindeutige Owner-ID
```

### Aktuelle Owner

| Superkey | Code | Name | Rolle |
|----------|------|------|-------|
| `OWN-GF` | GF | Gerhard Fehr | CEO & Founder |
| `OWN-EB` | EB | Ernst Fehr | Scientific Director |
| `OWN-MR` | MR | [Partner MR] | Partner |

### Automatische Zuweisung

| Priorität | Regel | Beschreibung |
|-----------|-------|--------------|
| 1 | **Bestehende Kunden** | Behalten ihren Owner (`relationship.owner`) |
| 2 | **Neue Leads** | Owner = wer den Lead einbringt |
| 3 | **Explizit** | Überschreiben via `/lead-update LEAD-XXX --owner CODE` |

### Owner ändern

```bash
# Owner für einen Lead ändern
/lead-update LEAD-003 --owner GF

# Neuen Lead mit spezifischem Owner
/lead-add "Neue Firma AG" technology --owner EB
```

### Neuen Owner hinzufügen

In `lead-database.yaml` unter `team_registry.owners`:

```yaml
- id: OWN-XX
  code: "XX"
  full_name: "Vorname Nachname"
  role: "Rolle"
  email: "email@fehradvice.com"
  github_user: "github-username"  # Optional
  active: true
  created: "2026-01-27"
```

---

## Automatische Benachrichtigungen

Bei der Erstellung eines neuen Leads werden automatisch E-Mails versendet.

### Empfänger

| Empfänger | E-Mail | Wann |
|-----------|--------|------|
| **Sales Operations** | nora.gavazajsusuri@fehradvice.com | Immer bei neuem Lead |
| **Sales Operations** | maria.neumann@fehradvice.com | Immer bei neuem Lead |
| **Owner** | (aus Team Registry) | Immer bei Zuweisung |

### E-Mail-Inhalt

Die Benachrichtigung enthält:
- Firmenname und Branche
- Zugewiesener Stage und Owner
- **Deadline** für Follow-up
- Fit Score (falls vorhanden)
- Lead-Quelle

### Beispiel-Workflow

```
1. /lead-add "Neue Firma AG" technology --owner EB
   ↓
2. Lead wird in Datenbank erstellt (LEAD-013)
   ↓
3. Automatische E-Mails an:
   ├── nora.gavazajsusuri@fehradvice.com
   ├── maria.neumann@fehradvice.com
   └── ernst.fehr@fehradvice.com (Owner EB)
   ↓
4. Deadline automatisch gesetzt: +14 Tage (SUSPECT Stage)
```

---

## Automatische Deadlines

Jeder Lead erhält automatisch eine Follow-up-Deadline basierend auf seinem Stage.

### Default-Fristen

| Stage | Deadline | Begründung |
|-------|----------|------------|
| SUSPECT | 14 Tage | Zeit für Erstkontakt |
| PROSPECT | 7 Tage | Qualifikation abschließen |
| QUALIFIED | 14 Tage | Angebot erstellen |
| PROPOSAL | 7 Tage | Follow-up nach Angebot |
| NEGOTIATION | 3 Tage | Schnelle Reaktion bei Verhandlung |
| WON | 2 Tage | Onboarding-Start |
| ACTIVE | 30 Tage | Regelmäßiger Check-in |
| DORMANT | 90 Tage | Reaktivierungsversuch |
| REACTIVATION | 14 Tage | Reaktivierung abschließen |

### Erinnerungen

Der Owner erhält eine Erinnerung **1 Tag vor Deadline**.

### E-Mail Script

```bash
# Neue Lead-Benachrichtigung senden
python scripts/send_lead_notification.py --new-lead LEAD-013

# Deadline-Erinnerungen prüfen und senden
python scripts/send_lead_notification.py --check-deadlines

# Test-Modus (keine echten E-Mails)
python scripts/send_lead_notification.py --new-lead LEAD-013 --dry-run

# System testen
python scripts/send_lead_notification.py --test
```

**Umgebungsvariablen für E-Mail-Versand:**
```bash
export SMTP_SERVER="smtp.office365.com"
export SMTP_PORT="587"
export SMTP_USER="user@fehradvice.com"
export SMTP_PASSWORD="..."
export FROM_EMAIL="noreply@fehradvice.com"
```

### Deadline manuell setzen

```bash
# Deadline explizit setzen
/lead-update LEAD-013 --deadline "2026-02-15"

# Deadline relativ setzen
/lead-update LEAD-013 --deadline "+7d"
```

---

## Lead-Scoring

### Fit Score (0-100)

Wie gut passt der Lead zu unserem Ideal Customer Profile (ICP)?

| Dimension | Gewicht | Beschreibung |
|-----------|---------|--------------|
| Industry Fit | 25% | Branche passt zu unseren Kernkompetenzen |
| Size Fit | 20% | Unternehmensgrösse passt |
| Budget Fit | 20% | Budget für EBF-Projekte vorhanden |
| Culture Fit | 15% | Evidenzbasierte Entscheidungskultur |
| Geographic Fit | 10% | DACH-Region oder erreichbar |
| Timing Fit | 10% | Aktueller Bedarf erkennbar |

### Engagement Score (0-100)

Wie engagiert ist der Lead?

| Aktivität | Punkte |
|-----------|--------|
| Website-Besuch | +2 |
| Content-Download | +5 |
| Event-Teilnahme | +10 |
| Meeting-Anfrage | +20 |
| RFP erhalten | +30 |
| Angebot angefordert | +40 |

---

## Superkey-System

Die Lead-Datenbank verwendet das EBF Superkey-System:

```
LEAD-{NNN}                         → Lead-Eintrag
  └── ebf_integration:
        customer_registry_ref      → CUS-{CODE}
        profile_path               → data/customers/{code}/
        funder_path                → data/funders/{code}/
```

### Cross-References

| Von | Nach | Pfad |
|-----|------|------|
| Lead | Customer Registry | `ebf_integration.customer_registry_ref` |
| Lead | Customer Profile | `ebf_integration.profile_path` |
| Lead | Funder Profile | `ebf_integration.funder_path` |
| Lead | Projekte | `projects[].id` |

---

## Branchen-Taxonomie

| Industrie | Subkategorien |
|-----------|---------------|
| `finance` | banking, insurance, asset_management, fintech |
| `packaging` | plastics, paper, glass, metal |
| `construction` | general_contractor, specialty, real_estate, infrastructure |
| `fmcg` | food_beverage, personal_care, household |
| `pharma_health` | pharma, medtech, healthcare_provider, health_insurance |
| `energy` | oil_gas, renewables, utilities, energy_services |
| `technology` | software, hardware, it_services, telecom |
| `public_sector` | federal, cantonal, municipal, ngo |
| `manufacturing` | automotive, machinery, chemicals, electronics |
| `retail` | retail, wholesale, ecommerce |
| `professional_services` | consulting, legal, accounting, hr_services |

---

## Source Channels

| Channel | Subchannels | Beschreibung |
|---------|-------------|--------------|
| **REFERRAL** | client_referral, partner_referral, employee_referral, fehr_network | Empfehlungen |
| **INBOUND** | website, content, event, speaking, publication | Inbound Marketing |
| **OUTBOUND** | cold_outreach, linkedin, conference, direct_mail | Outbound Sales |
| **EXISTING** | upsell, cross_sell, renewal, expansion | Bestandskunden |
| **RESEARCH** | academic_collaboration, grant_project, research_partner | Forschung |

---

## Dateien in diesem Verzeichnis

```
data/sales/
├── README.md                    ← Diese Dokumentation
├── lead-database.yaml           ← Haupt-Datenbank (SSOT)
├── LEAD-ENTRY-WORKFLOW.md       ← Lead-Eingabe Workflow
├── report-templates.yaml        ← Report-Vorlagen (NEU v1.1)
└── lead-database.schema.yaml    ← JSON Schema für Validierung
```

---

## Verwendung

### Lead hinzufügen

```yaml
- id: LEAD-013
  company:
    name: "Neue Firma AG"
    short_name: "NeueFirma"
    website: "https://www.neuefirma.ch"

  industry: technology
  segment: mid_market
  employee_count: 500
  headquarters:
    country: CH
    city: "Zürich"

  stage: PROSPECT
  stage_history:
    - stage: PROSPECT
      date: "2026-01-27"
      owner: "EB"
      notes: "Erstkontakt via LinkedIn"

  fit_score: 75
  engagement_score: 20

  relationship:
    owner: "EB"

  source:
    channel: OUTBOUND
    subchannel: linkedin
    first_touch_date: "2026-01-27"

  notes: "Vielversprechender Lead aus Tech-Sektor"
  tags: [technology, startup, switzerland]
  created_at: "2026-01-27T14:35:22+01:00"  # ISO 8601 mit Uhrzeit
```

### Timestamp-Format

Das `created_at` Feld verwendet **ISO 8601** Format mit Zeitzone:

```
YYYY-MM-DDTHH:MM:SS+HH:MM
│    │  │  │  │  │  └── Zeitzone (z.B. +01:00 für CET)
│    │  │  │  │  └───── Sekunden
│    │  │  │  └──────── Minuten
│    │  │  └─────────── Stunden
│    │  └────────────── Tag
│    └───────────────── Monat
└────────────────────── Jahr
```

**Beispiele:**
- `2026-01-27T14:35:22+01:00` → 27. Januar 2026, 14:35:22 Uhr (CET)
- `2026-01-27T08:00:00Z` → 27. Januar 2026, 08:00:00 Uhr (UTC)

**Neuesten Lead finden:**
```bash
python scripts/send_lead_notification.py --latest
```

### Stage ändern

Bei jeder Stage-Änderung einen neuen Eintrag in `stage_history` hinzufügen:

```yaml
stage: QUALIFIED
stage_history:
  - stage: PROSPECT
    date: "2026-01-15"
    owner: "EB"
  - stage: QUALIFIED          # NEU
    date: "2026-01-27"
    owner: "EB"
    notes: "Budget bestätigt, Entscheider identifiziert"
```

### Lost/Churn dokumentieren

Bei `LOST` oder `CHURNED` immer Analyse hinzufügen:

```yaml
# Für LOST (nie Kunde geworden)
lost_analysis:
  competitor: "McKinsey"
  reason: "Brand preference"
  lessons_learned: "Früher C-Level Engagement"
  reapproach_date: "2027-01-01"

# Für CHURNED (ehemaliger Kunde)
churn_analysis:
  reason: "Budgetkürzungen"
  preventable: false
  win_back_potential: medium
  total_lifetime_value_eur: 85000
```

---

## Slash Commands

### Lead Management

| Command | Beschreibung |
|---------|--------------|
| `/new-lead` | **Neuen Lead erfassen mit Auto-Suggest Phase** |
| `/new-lead --quick` | Schnelleingabe (nur Pflichtfelder) |
| `/new-lead --from-note "..."` | Aus Freitext extrahieren |
| `/lead-update` | Lead-Stage aktualisieren |
| `/lead-search` | Leads suchen/filtern |
| `/lead-card LEAD-001` | Lead-Detailansicht |

### Reports (NEU v1.1)

| Command | Beschreibung |
|---------|--------------|
| `/action-list` | **Offene Aktionen pro Owner** |
| `/action-list --owner EB` | Nur Aktionen für Owner EB |
| `/action-list --overdue` | Nur überfällige Aktionen |
| `/pipeline-summary` | Pipeline-Übersicht mit Statistiken |
| `/pipeline-summary --phase` | Fokus auf Projekt-Phasen |
| `/forecast` | Umsatzprognose mit Szenarien |
| `/forecast --quarter Q1-2026` | Forecast für Quartal |
| `/win-loss` | Win/Loss Analyse mit Learnings |
| `/win-loss --quarter Q4-2025` | Analyse für Quartal |

---

## Integration mit EBF

Wenn ein Lead zum Kunden wird (Stage: `WON` → `ACTIVE`):

1. **Customer Registry** updaten: `data/customer-registry.yaml`
2. **Customer Profile** erstellen: `data/customers/{code}/`
3. **EBF Integration** verlinken:
   ```yaml
   ebf_integration:
     customer_registry_ref: "CUS-NEUEFIRMA"
     profile_path: "data/customers/neuefirma/neuefirma_profile.yaml"
     has_10c_analysis: false
   ```

---

## Statistiken aktualisieren

Die `pipeline_summary` Sektion sollte bei jeder Änderung aktualisiert werden:

```yaml
pipeline_summary:
  last_updated: "2026-01-27"
  total_leads: 12
  by_stage:
    SUSPECT: 1
    PROSPECT: 1
    # ... etc.
```

---

*Version 1.2.0 | Januar 2026*

**v1.2.0 Updates:**
- Report-Vorlagen hinzugefügt (`report-templates.yaml`)
- 6 standardisierte Report-Formate (Action List, Pipeline Summary, Lead Card, Forecast, Win/Loss, Owner Dashboard)
- Neue Slash-Commands für Reports (`/action-list`, `/pipeline-summary`, `/forecast`, `/win-loss`)

**v1.1.0 Updates:**
- Projekt-Phasen (Phase 0-5) hinzugefügt
- Auto-Suggest Algorithmus für Phase-Zuweisung
- Neuer Slash-Command `/new-lead` mit Workflow
- LEAD-ENTRY-WORKFLOW.md Dokumentation
