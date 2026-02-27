# /project-setup - Projekt-Setup Workflow

Automatisierter Workflow zum Aufsetzen eines neuen Kundenprojekts. Orchestriert alle Schritte von Lead-Erfassung bis Scope-Definition.

## Quick Start

```bash
/project-setup                           # Interaktiv (empfohlen)
/project-setup "Helsana" "Sales-Strategie"  # Schnellstart mit Kunde + Projekt
/project-setup --from-lead LEAD-047      # Von bestehendem Lead starten
```

---

## Workflow-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  /project-setup WORKFLOW                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: Lead prüfen/erstellen                                         │
│  ├── Existiert Lead bereits? → Verknüpfen                              │
│  └── Nein → Lead-Daten erfassen → LEAD-{NNN} erstellen                 │
│                                                                         │
│  PHASE 2: CVA prüfen/erstellen                                          │
│  ├── Existiert Kundenprofil? → Verwenden                               │
│  └── Nein → "Soll ich CVA erstellen?" (SCHNELL/STANDARD)               │
│                                                                         │
│  PHASE 3: Projekt-Scope definieren                                      │
│  ├── Ziel (SMART)                                                      │
│  ├── In-Scope / Out-of-Scope                                           │
│  ├── Lieferobjekte                                                     │
│  ├── Nebenbedingungen                                                  │
│  └── Stakeholder                                                       │
│                                                                         │
│  PHASE 4: Dateien erstellen                                             │
│  ├── Lead in lead-database.yaml                                        │
│  ├── Scope in customers/{kunde}/projects/                              │
│  └── Git commit                                                        │
│                                                                         │
│  OUTPUT: PRJ-{KUNDE}-{NNN} ready                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: Lead prüfen/erstellen

### 1.1 Lead-Suche

```
PROJEKT-SETUP

Schritt 1: Lead identifizieren

Kunde: _______________

[Suche in lead-database.yaml...]

□ Lead gefunden: LEAD-047 (Helsana) - Stage: PROSPECT
  → Diesen Lead verwenden? [J/n]

□ Kein Lead gefunden
  → Neuen Lead erstellen? [J/n]
```

### 1.2 Lead-Daten (falls neu)

```
NEUER LEAD

Unternehmen:
  Name: _______________
  Kurzname: _______________
  Website: _______________

Branche:
  [1] finance      [2] insurance    [3] health
  [4] energy       [5] retail       [6] manufacturing
  [7] government   [8] other: ___

Kontaktperson:
  Name: _______________
  Rolle: _______________
  Email: _______________ (optional)

Owner (FehrAdvice):
  [GF] Gerhard Fehr    [EB] Ernst Fehr    [MR] Partner MR
  [AJ] Partner AJ      [MDL] Partner MdL  [andere]: ___
```

---

## PHASE 2: CVA prüfen/erstellen (PFLICHT)

> ⚠️ **CVA ist Voraussetzung für Projekt-Erstellung!**
> Ohne Kontextvektor kann kein Projekt gestartet werden.
> Grund: EBF-Modelle benötigen Kontext-Parameter (Ψ-Dimensionen).

### 2.1 CVA-Check

```
Schritt 2: Kundenprofil (CVA) prüfen [PFLICHT]

[Suche in data/customers/...]

□ CVA gefunden: data/customers/helsana/ (STANDARD, 400 Faktoren)
  → Profil verwenden ✓
  → Weiter zu Phase 3

□ Kein CVA gefunden
  ⚠️ STOPP: CVA muss erstellt werden!

  Welche Stufe?
    [1] SCHNELL  - 30 Faktoren, 1 YAML (~30 min)
                  → Für Sounding, erste Gespräche
    [2] STANDARD - 400 Faktoren, 8 YAMLs (~2h)
                  → Für vollständige Projekte

  → CVA wird jetzt erstellt, dann Weiter zu Phase 3
```

### 2.2 CVA erstellen (AUTOMATISCH falls nicht vorhanden)

Verwendet `/new-customer` Skill automatisch.

**Warum CVA Pflicht?**
- 10C-Modelle benötigen Kontext-Parameter (Ψ)
- Interventions-Design braucht MACRO/MESO-Ebene
- Parameter-Kaskade (λ, β, γ) hängt vom Kontext ab
- Ohne CVA: Keine valide Analyse möglich

---

## PHASE 3: Projekt-Scope definieren

### 3.1 Basis-Informationen

```
Schritt 3: Projekt-Scope

Projektname: _______________
(z.B. "Sounding der Sales-Strategie")

Projekt-Typ:
  [1] Sounding/Exploration  - Erstgespräch, Potentialanalyse
  [2] Analyse              - Diagnose, Assessment
  [3] Strategie            - Konzept, Roadmap
  [4] Umsetzung            - Implementation, Pilot
  [5] Evaluation           - Messung, Review
```

### 3.2 Ziel (SMART)

```
ZIEL

Was soll erreicht werden? (1-2 Sätze)
> _______________________________________________

Wie messen wir Erfolg?
> _______________________________________________

Bis wann?
  [1] Offen (Sounding)
  [2] Q1 2026
  [3] Q2 2026
  [4] Datum: _______________
```

### 3.3 Scope

```
IN-SCOPE (Was ist Teil des Projekts?)

Aktivitäten:
  [+] _______________
  [+] _______________
  [+] _______________

Bereiche/Abteilungen:
  □ Vertrieb/Sales     □ Marketing      □ HR
  □ Finanzen           □ Operations     □ IT
  □ Geschäftsleitung   □ Andere: ___

───────────────────────────────────────────────────

OUT-OF-SCOPE (Was ist NICHT Teil des Projekts?)

  [-] _______________
  [-] _______________
```

### 3.4 Lieferobjekte

```
LIEFEROBJEKTE

Deliverable 1:
  Name: _______________
  Format: [Report | Workshop | Präsentation | Datenbank | Andere]
  Fällig: _______________

Deliverable 2:
  Name: _______________
  Format: _______________
  Fällig: _______________

[+] Weiteres Deliverable hinzufügen
```

### 3.5 Nebenbedingungen

```
NEBENBEDINGUNGEN

Budget:
  [1] TBD (noch nicht definiert)
  [2] < CHF 50k
  [3] CHF 50-100k
  [4] CHF 100-250k
  [5] > CHF 250k

Timeline:
  Start: _______________
  Deadline: _______________ (falls vorhanden)

Constraints:
  [+] _______________
  [+] _______________
```

### 3.6 Stakeholder

```
STAKEHOLDER

Kundenseite:

  Sponsor (Auftraggeber):
    Name: _______________
    Rolle: _______________

  Weitere Stakeholder:
    [+] Name: _______________ | Rolle: _______________
    [+] Name: _______________ | Rolle: _______________

FehrAdvice:

  Project Lead: [GF | EB | MR | AJ | MDL | ___]
  Team: _______________
```

---

## PHASE 4: Dateien erstellen

### 4.1 Automatische Erstellung

```
Schritt 4: Projekt erstellen

Erstelle folgende Dateien:

  ✓ Lead:  data/sales/lead-database.yaml
           → LEAD-047 (aktualisiert/erstellt)

  ✓ Scope: data/customers/helsana/projects/PRJ-HELSANA-001_scope.yaml
           → 11 Sektionen ausgefüllt

  ✓ Git:   Commit erstellt
           → "feat(project): Add PRJ-HELSANA-001 - Sounding Sales-Strategie"

───────────────────────────────────────────────────

PROJEKT ERSTELLT ✓

  Superkey:     PRJ-HELSANA-001
  Lead:         LEAD-047
  Status:       SCOPING
  Owner:        GF

  Dateien:
  ├── data/sales/lead-database.yaml (aktualisiert)
  └── data/customers/helsana/projects/PRJ-HELSANA-001_scope.yaml

Nächste Schritte:
  1. Sounding-Termin mit Sandro Mannino vereinbaren
  2. Nach Sounding: Scope finalisieren
  3. Bei Go: /intervention-manage new PRJ-HELSANA-001
```

---

## Optionen

| Flag | Beschreibung |
|------|--------------|
| `--from-lead LEAD-XXX` | Von bestehendem Lead starten |
| `--quick` | Nur Pflichtfelder, keine optionalen |
| `--no-cva` | CVA-Erstellung überspringen |
| `--dry-run` | Zeigt was erstellt würde, ohne zu speichern |

---

## Beispiele

### Beispiel 1: Interaktiv (Standard)

```bash
/project-setup
```

Führt durch alle Phasen interaktiv.

### Beispiel 2: Schnellstart

```bash
/project-setup "Helsana" "Sounding Sales-Strategie" --from-lead LEAD-047
```

Erstellt Scope für bestehenden Lead.

### Beispiel 3: Neuer Kunde

```bash
/project-setup "NeuerKunde AG" "Digital Transformation"
```

Erstellt Lead + CVA (SCHNELL) + Scope.

---

## Verknüpfte Skills

| Skill | Wann verwendet |
|-------|----------------|
| `/new-lead` | Phase 1, wenn Lead neu |
| `/new-customer` | Phase 2, wenn CVA neu |
| `/lead-card` | Lead-Details anzeigen |
| `/intervention-manage new` | Nach Scope → Projekt starten |

---

## Template-Referenz

**Scope-Template:** `templates/project-scope-template.yaml`

**Sektionen:**
1. Ziel (SMART)
2. In-Scope
3. Out-of-Scope
4. Lieferobjekte
5. Nebenbedingungen
6. Annahmen
7. Risiken
8. Stakeholder
9. Abhängigkeiten
10. Change Management
11. Genehmigung

---

## Superkey-Format

| Typ | Format | Beispiel |
|-----|--------|----------|
| Lead | `LEAD-{NNN}` | LEAD-047 |
| Projekt | `PRJ-{KUNDE}-{NNN}` | PRJ-HELSANA-001 |
| Intervention | `PRJ-{KUNDE}-{NNN}-INT-{NN}` | PRJ-HELSANA-001-INT-01 |

---

## Checkliste nach /project-setup

```
☐ Lead in Pipeline (LEAD-XXX)
☐ CVA vorhanden oder geplant
☐ Scope-Datei erstellt (PRJ-XXX)
☐ Ziel SMART formuliert
☐ In-Scope / Out-of-Scope definiert
☐ Lieferobjekte mit Terminen
☐ Stakeholder identifiziert
☐ Nächste Schritte klar
☐ Git committed
```
