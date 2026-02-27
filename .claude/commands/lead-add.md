# /lead-add - Neuen Lead hinzufügen

Fügt einen neuen Lead zur Lead-Datenbank hinzu.

## Syntax

```bash
/lead-add                           # Interaktiver Modus
/lead-add "Company Name" industry   # Schnell-Modus
```

## Interaktiver Modus

Claude fragt nacheinander:

1. **Firmendaten**
   - Name (Pflicht)
   - Kurzname
   - Website
   - Land & Stadt

2. **Klassifikation**
   - Branche (aus Taxonomie)
   - Segment (enterprise/mid_market/smb/government)
   - Mitarbeiterzahl
   - Umsatz

3. **Pipeline**
   - Stage (Default: SUSPECT)
   - Owner

4. **Source**
   - Channel (REFERRAL/INBOUND/OUTBOUND/RESEARCH)
   - Subchannel
   - Referrer (falls REFERRAL)

5. **Scoring** (optional)
   - Fit Score (0-100)
   - Engagement Score (0-100)

## Workflow

### 🔴 PFLICHT: Atomare ID-Vergabe via Script

```bash
# SCHRITT 1: ID via Script holen (NIEMALS manuell!)
python scripts/get_next_lead_id.py
# → Gibt z.B. "LEAD-061" zurück
# → Incrementiert automatisch next_lead_id auf 62
```

```yaml
# SCHRITT 2: Lead-Eintrag erstellen mit dieser ID
- id: LEAD-061  # ← ID aus Script-Output
  company:
    name: $USER_INPUT
    short_name: $DERIVED
  industry: $USER_INPUT
  stage: SUSPECT
  stage_history:
    - stage: SUSPECT
      date: $TODAY
      owner: $USER_INPUT
  source:
    channel: $USER_INPUT
    first_touch_date: $TODAY
  created: $TODAY
  updated: $TODAY

# SCHRITT 3: (entfällt - Script hat bereits incrementiert!)
```

**⚠️ KRITISCH: ID-Vergabe NUR via Script!**

| Schritt | Aktion | Command |
|---------|--------|---------|
| 1 | ID holen + Auto-Increment | `python scripts/get_next_lead_id.py` |
| 2 | Lead mit dieser ID erstellen | YAML-Eintrag schreiben |
| 3 | Commit | Pre-Commit Hook validiert |

**VERBOTEN:**
```
❌ ID manuell aus metadata lesen
❌ next_lead_id manuell incrementieren
❌ ID "schätzen" oder annehmen
```

**ERLAUBT / ERFORDERLICH:**
```
✅ IMMER: python scripts/get_next_lead_id.py
✅ Script-Output direkt verwenden
✅ Pre-Commit Hook blockiert Duplikate als Sicherheitsnetz
```

**Validierung:**
```bash
# Prüfen ob Datenbank konsistent ist
python scripts/get_next_lead_id.py --validate

# Nur schauen was die nächste ID wäre (ohne Increment)
python scripts/get_next_lead_id.py --peek
```

## Validierung

- Firmenname muss eindeutig sein
- Branche muss aus Taxonomie sein
- Stage muss gültig sein (SUSPECT, PROSPECT, QUALIFIED, etc.)
- Owner muss gesetzt sein

## Output

Nach Erstellung:
1. Lead-ID zurückgeben
2. Zusammenfassung anzeigen
3. **Automatische E-Mails versenden** (NEU)
4. **Deadline setzen** (NEU)
5. Nächste Aktion vorschlagen

```
✅ Lead erstellt: LEAD-013

┌─────────────────────────────────────────────────────────────┐
│  LEAD-013: Neue Firma AG                                    │
├─────────────────────────────────────────────────────────────┤
│  Stage:     SUSPECT                                         │
│  Industry:  technology                                      │
│  Country:   CH                                              │
│  Owner:     EB                                              │
│  Source:    OUTBOUND / linkedin                             │
│  Created:   2026-01-27                                      │
│  Deadline:  2026-02-10 (14 Tage)                            │
└─────────────────────────────────────────────────────────────┘

📧 E-Mail versendet an:
   ├── nora.gavazajsusuri@fehradvice.com
   ├── maria.neumann@fehradvice.com
   └── ernst.fehr@fehradvice.com (Owner)

Nächste Aktion: Erstkontakt aufnehmen → /lead-update LEAD-013 PROSPECT
```

## Automatische Benachrichtigungen

Bei jedem neuen Lead werden automatisch benachrichtigt:

| Empfänger | Rolle | E-Mail |
|-----------|-------|--------|
| Nora Gavazaj Susuri | Sales Operations | nora.gavazajsusuri@fehradvice.com |
| Maria Neumann | Sales Operations | maria.neumann@fehradvice.com |
| **Owner** | (variiert) | Aus Team Registry |

## Automatische Deadlines

Die Deadline wird automatisch basierend auf dem Stage gesetzt:

| Stage | Default-Deadline |
|-------|------------------|
| SUSPECT | +14 Tage |
| PROSPECT | +7 Tage |
| QUALIFIED | +14 Tage |

Manuelle Überschreibung möglich mit `--deadline`.

## Beispiele

```bash
# Interaktiv (empfohlen für neue Leads)
/lead-add

# Schnell-Modus für bekannte Prospects
/lead-add "Migros" retail

# Mit zusätzlichen Optionen
/lead-add "Swisscom" technology --stage PROSPECT --owner MR
```
