# /followup - Kontaktsteuerung & Follow-up Management

Tägliche Arbeitsliste für aktives Nachfassen und Kontaktsteuerung.

## Schnellstart

```bash
/followup                  # Heutige Prioritäten anzeigen
/followup --week           # Wochenübersicht
/followup --overdue        # Nur überfällige Kontakte
/followup --owner GF       # Nur Leads von Gerhard Fehr
```

## Befehle

### Übersicht anzeigen

| Befehl | Beschreibung |
|--------|--------------|
| `/followup` | Heutige Aufgaben (sortiert nach Priorität) |
| `/followup --week` | Wochenplanung Mo-Fr |
| `/followup --overdue` | Überfällige Kontakte (SOFORT!) |
| `/followup --owner CODE` | Leads eines bestimmten Owners |
| `/followup --stage STAGE` | Leads in bestimmter Stage |
| `/followup --hot` | Nur Hot Leads anzeigen |

### Kontakt loggen

```bash
/followup log LEAD-XXX
```

Interaktiver Dialog:
1. Kontakttyp (call/email/meeting/linkedin/other)
2. Richtung (outbound/inbound)
3. Kontaktperson
4. Ergebnis (reached/voicemail/no_answer/meeting_set/...)
5. Notizen
6. Nächstes Follow-up Datum

### Nächste Aktion planen

```bash
/followup plan LEAD-XXX
```

Interaktiver Dialog:
1. Aktion beschreiben
2. Datum wählen
3. Typ (call/email/meeting/proposal/other)
4. Priorität (critical/high/medium/low)

### Quick Actions

```bash
/followup call LEAD-XXX      # Anruf planen (heute)
/followup email LEAD-XXX     # Email-Reminder setzen
/followup meeting LEAD-XXX   # Termin-Follow-up
```

### Statistiken

```bash
/followup stats              # Kontakt-Statistiken
/followup stats --owner GF   # Pro Owner
/followup stats --week       # Wochenstatistik
```

## Tägliche Übersicht (Standard-Output)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📅 FOLLOW-UP ÜBERSICHT - Dienstag, 28. Januar 2026                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🔴 ÜBERFÄLLIG (3)                                                      │
│  ──────────────────────────────────────────────────────────────────── │
│  LEAD-015  Beispiel AG       +5 Tage   Call     GF   Phase 2           │
│  LEAD-023  Muster GmbH       +3 Tage   Email    MR   Phase 1           │
│  LEAD-041  Test Corp         +1 Tag    Meeting  EB   Phase 3           │
│                                                                         │
│  🟠 HEUTE (5)                                                           │
│  ──────────────────────────────────────────────────────────────────── │
│  LEAD-001  ALPLA             Heute     Call     EB   Phase 5  ⭐ HOT   │
│  LEAD-007  LUKB              Heute     Meeting  GF   Phase 4           │
│  LEAD-012  Neue AG           Heute     Email    MR   Phase 2           │
│  LEAD-019  Firma XY          Heute     Call     GF   Phase 1           │
│  LEAD-033  Prospect Ltd      Heute     LinkedIn AJ   Phase 0           │
│                                                                         │
│  🟡 DIESE WOCHE (8)                                                     │
│  ──────────────────────────────────────────────────────────────────── │
│  LEAD-002  PORR              Mi 29.    Call     MR   Phase 3           │
│  LEAD-005  Helsana           Do 30.    Meeting  GF   Phase 2           │
│  ...                                                                    │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  📊 QUICK STATS                                                         │
│  Überfällig: 3 | Heute: 5 | Diese Woche: 8 | Hot Leads: 2             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Workflow: Kontakt nachfassen

### 1. Morgens: Übersicht prüfen

```bash
/followup
```

### 2. Kontakt durchführen

Anruf tätigen, Email senden, Meeting halten...

### 3. Ergebnis loggen

```bash
/followup log LEAD-XXX
```

### 4. Nächste Aktion planen

Wird automatisch beim Loggen abgefragt, oder:

```bash
/followup plan LEAD-XXX
```

### 5. Bei Hot Lead oder Eskalation

```bash
/followup hot LEAD-XXX --reason "Grosses Budget, Q1 Entscheidung"
```

## Datenquellen

| Datei | Inhalt |
|-------|--------|
| `data/sales/lead-database.yaml` | Master-Daten (Leads, Stages, Contacts) |
| `data/sales/contact-tracking.yaml` | Tägliche Arbeitsliste & Logs |

## Automatische Berechnungen

- **days_since_contact**: Tage seit letztem Kontakt-Log
- **follow_up_overdue**: `next_action_date < heute`
- **priority_score**: Stage-Frequenz + Fit-Score + Hot-Lead-Bonus

## Integration mit anderen Skills

```bash
/lead-card LEAD-XXX          # Vollständige Lead-Details
/lead-update LEAD-XXX        # Lead-Daten aktualisieren
/pipeline-summary            # Pipeline-Gesamtübersicht
```

## Prioritäts-Logik

| Priorität | Farbe | Bedeutung |
|-----------|-------|-----------|
| **Critical** | 🔴 | Überfällig ODER Hot Lead mit Deadline |
| **High** | 🟠 | Heute fällig ODER >50k Opportunity |
| **Medium** | 🟡 | Diese Woche fällig |
| **Low** | ⚪ | Später als 7 Tage |

## Kontakt-Frequenz (Defaults)

| Stage | Frequenz | Begründung |
|-------|----------|------------|
| SUSPECT | 14 Tage | Langsames Aufwärmen |
| PROSPECT | 7 Tage | Aktives Qualifizieren |
| QUALIFIED | 5 Tage | Momentum halten |
| PROPOSAL | 3 Tage | Entscheidung treiben |
| NEGOTIATION | 2 Tage | Abschluss sichern |
| ACTIVE | 30 Tage | Beziehungspflege |
| DORMANT | 60 Tage | Reaktivierung prüfen |

## Beispiel-Session

```
User: /followup

Claude:
┌─────────────────────────────────────────────────────────────────────────┐
│  📅 FOLLOW-UP ÜBERSICHT - Dienstag, 28. Januar 2026                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🔴 ÜBERFÄLLIG (1)                                                      │
│  LEAD-015  Muster Bank       +2 Tage   Call     GF   QUALIFIED         │
│            Letzte Aktion: Email am 23.01. - keine Antwort              │
│                                                                         │
│  🟠 HEUTE (2)                                                           │
│  LEAD-001  ALPLA             Heute     Call     EB   ACTIVE    ⭐      │
│            Q1 Review besprechen                                         │
│  LEAD-007  LUKB              Heute     Meeting  GF   PROPOSAL          │
│            Angebotspräsentation 14:00 Uhr                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

Was möchtest du tun?
1. Kontakt loggen (/followup log LEAD-XXX)
2. Aktion planen (/followup plan LEAD-XXX)
3. Lead-Details (/lead-card LEAD-XXX)

User: /followup log LEAD-015

Claude:
📝 KONTAKT LOGGEN - LEAD-015 (Muster Bank)

1. Kontakttyp?
   [1] 📞 Call  [2] 📧 Email  [3] 🤝 Meeting  [4] 💼 LinkedIn  [5] Andere

User: 1

Claude:
2. Richtung?
   [1] ➡️ Outbound (wir haben angerufen)
   [2] ⬅️ Inbound (Kunde hat angerufen)

User: 1

Claude:
3. Kontaktperson?
   Bekannte Kontakte: Max Müller (CEO), Anna Schmidt (CFO)
   Oder neuen Namen eingeben:

User: Max Müller

Claude:
4. Ergebnis?
   [1] ✅ Erreicht  [2] 📱 Mailbox  [3] ❌ Nicht erreicht
   [4] 📅 Termin vereinbart  [5] 📄 Angebot versendet  [6] 🚫 Kein Interesse

User: 1

Claude:
5. Notizen (optional):

User: Budget für Q2 bestätigt, will nächste Woche Angebot sehen

Claude:
6. Nächstes Follow-up?
   [1] Morgen  [2] In 3 Tagen  [3] Nächste Woche  [4] Datum eingeben

User: 3

Claude:
✅ Kontakt geloggt!

┌─────────────────────────────────────────────────────────────────────────┐
│  LEAD-015 - Muster Bank                                                 │
│  ─────────────────────────────────────────────────────────────────────  │
│  Kontakt:    📞 Call (outbound) mit Max Müller                         │
│  Ergebnis:   ✅ Erreicht                                                │
│  Notizen:    Budget für Q2 bestätigt, will nächste Woche Angebot sehen │
│  Follow-up:  📅 04.02.2026 (in 7 Tagen)                                │
│  Owner:      GF                                                         │
│                                                                         │
│  → Stage-Empfehlung: QUALIFIED → PROPOSAL (Angebot vorbereiten)        │
└─────────────────────────────────────────────────────────────────────────┘

Soll ich die Stage auf PROPOSAL ändern? [j/n]
```

## Technische Details

### Daten-Synchronisation

- `lead-database.yaml` ist Master (SSOT)
- `contact-tracking.yaml` wird bei jedem `/followup` Aufruf aktualisiert
- Kontakt-Logs werden in beide Dateien geschrieben

### Berechnete Felder

```yaml
# In lead-database.yaml pro Lead
computed_fields:
  days_since_contact: 5        # Berechnet aus contact_log
  follow_up_overdue: true      # next_action_date < today
  priority_score: 85           # Gewichtete Berechnung
  next_contact_due: "2026-01-28"  # Basierend auf Stage-Frequenz
```
