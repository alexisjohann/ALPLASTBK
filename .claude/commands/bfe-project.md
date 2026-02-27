# /bfe-project - BFE Projekt erstellen und verwalten

Erstellen und verwalten Sie BFE-Projekte mit dem **10C-basierten Workflow**.

## Verwendung

```
/bfe-project new                    # Neues Projekt interaktiv erstellen
/bfe-project new --schnell          # Schnellmodus (5 Kernfragen)
/bfe-project new --name "Heizung"   # Mit Projektnamen
/bfe-project list                   # Alle Projekte anzeigen
/bfe-project status <ID>            # Status eines Projekts
/bfe-project close <ID>             # Projekt abschliessen (Learnings erfassen)
```

## Workflow-Modi

| Modus | Beschreibung | Zeit | Fragen |
|-------|--------------|------|--------|
| **⚡ SCHNELL** | 5 Kernfragen → Projekt angelegt | 5 min | WHO, WHAT, WHEN, WHERE, Intervention |
| **🎯 VOLLSTÄNDIG** | Alle 10C durchgehen | 20 min | Alle 10C + Predictions |

---

## Der Workflow

### Phase 0: Projekt-Metadaten

**Automatisch generiert:**
- `project_id`: BFE-YYYY-NNN (z.B. BFE-2026-001)
- `created`: Aktuelles Datum
- `status`: "planning"

**Abgefragt:**
- Projektname (kurz, beschreibend)
- Kurzbeschreibung (1-2 Sätze)

---

### Phase 1: WHO - Zielgruppe

**Frage:** Wer soll das Verhalten ändern?

**Optionen (aus BCM2_MIKRO_BFE):**

| # | Zielgruppe | Typische Entscheidungen |
|---|------------|------------------------|
| 1 | **Eigentümer EFH** | Heizungsersatz, Solar, Sanierung |
| 2 | **Eigentümer MFH/Stockwerk** | Kollektive Sanierung |
| 3 | **Mieter** | Stromverbrauch, Verhalten |
| 4 | **KMU** | Prozesseffizienz, Gebäude |
| 5 | **Grossindustrie** | Zielvereinbarungen |
| 6 | **Kantone** | Vollzug, Förderung |
| 7 | **Gemeinden** | Lokale Energieplanung |
| 8 | **CUSTOM** | Andere Zielgruppe |

**Output:** `who.primary_target` im model.yaml

---

### Phase 2: WHAT - Zielverhalten

**Frage:** Welches Verhalten soll erreicht werden?

**Optionen nach Interventionsfeld (aus BCM2_MIKRO_BFE):**

| # | Domain | Typische Verhaltensänderungen |
|---|--------|------------------------------|
| 1 | **DOM-HEAT** | fossil → erneuerbar Heizung |
| 2 | **DOM-SOLAR** | PV-Anlage installieren |
| 3 | **DOM-MOBILITY** | E-Auto Adoption |
| 4 | **DOM-EFFICIENCY** | Energieverbrauch senken |
| 5 | **CUSTOM** | Anderes Verhalten |

**Folgefragen:**
- Aktuelles Verhalten (Baseline)
- Gewünschtes Verhalten (Target)
- Verhaltenstyp: Decision / Continuous / Process

**Output:** `what.target_behavior` im model.yaml

---

### Phase 3: WHEN - Timing

**Frage:** Wann ist der optimale Interventionszeitpunkt?

**Optionen (kritische Momente):**

| # | Moment | Opportunity Window |
|---|--------|-------------------|
| 1 | **Heizungsdefekt** | 2-4 Wochen |
| 2 | **Hauskauf/-bau** | 3-6 Monate |
| 3 | **Renovation** | 2-3 Monate |
| 4 | **Tarifwechsel möglich** | 1-2 Monate |
| 5 | **Saisonal** | Herbst (Heizen), Frühling (Solar) |
| 6 | **Lebensereignis** | Pensionierung, Erbschaft |
| 7 | **CUSTOM** | Anderer Moment |

**Output:** `when.critical_moments` im model.yaml

---

### Phase 4: WHERE - Kontext & Choice Architecture

**Frage:** Wie sieht der Entscheidungskontext aus?

**Sub-Fragen:**

1. **Entscheidungsort:**
   - Zuhause (privat)
   - Beratungsgespräch (guided)
   - Online (selbstgesteuert)
   - Am Point-of-Sale

2. **Aktueller Default:**
   - Was passiert, wenn nichts getan wird?

3. **Vorgeschlagener Default:**
   - Wie ändern wir den Default?

**Output:** `where.choice_architecture` im model.yaml

---

### Phase 5: Intervention-Mix (HOW)

**Frage:** Welche 10C-Dimensionen sollen adressiert werden?

**Optionen (10C-Zieldimensionen):**

| # | 10C-Target | Δ-Ziel | Beispiel |
|---|------------|--------|----------|
| 1 | AWARE | A(·)↑ | Information, Vergleich |
| 2 | AWARE | κ_AWX↑ | Feedback, Tracking |
| 3 | WHEN | κ_ARCH→ | Defaults, Opt-out |
| 4 | WHEN | κ_JNY→ | Deadlines, Erinnerungen |
| 5 | WHAT(X) | W_base↑ | Selbstkonzept, Commitment |
| 6 | WHAT(S) | u_S↑ | Normen, Social Proof |
| 7 | WHAT(F) | u_F↑ | Förderung, Anreize |
| 8 | HOW | γ_ij→ | Pre-Commitment |

**Crowding-Out Warnung bei:**
- WHAT(S) + WHAT(F) kombiniert → γ = -0.2 (Social + Financial)
- WHAT(F) + HOW kombiniert → γ = -0.3 (Financial + Intrinsic)

**Output:** `how.intervention_mix` im model.yaml

---

### Phase 6: Kontext-Selektion (automatisch)

**Basierend auf WHO + WHAT + WHERE** werden automatisch:
- Relevante **MESO-Faktoren** aus BCM2_MESO_energy_ch.yaml selektiert
- Relevante **MAKRO-Faktoren** aus BCM2_04_KON vorgeschlagen
- **context_subset.yaml** vorausgefüllt

**Mapping-Logik:**

| Domain | Auto-selektierte MESO-Faktoren |
|--------|-------------------------------|
| DOM-HEAT | ENE-REG-06, ENE-PSY-02, ENE-SOC-04, ENE-ECO-02 |
| DOM-SOLAR | ENE-REG-02, ENE-SOC-01, ENE-ECO-03, ENE-PSY-03 |
| DOM-MOBILITY | ENE-SOC-02, ENE-PSY-05, ENE-REG-07 |
| DOM-EFFICIENCY | ENE-PSY-01, ENE-PSY-07, ENE-PSY-08, ENE-SOC-03 |

---

### Phase 7: Predictions (optional im Schnellmodus)

**Frage:** Was sind die erwarteten Ergebnisse?

- **Primary Outcome:** Metrik + Baseline + Target
- **Confidence Interval:** 95% CI
- **Behavioral KPIs:** Conversion Rate, etc.

---

## Output-Dateien

Nach Abschluss werden erstellt:

```
projects/YYYY_projektname/
├── model.yaml           # Ausgefülltes 10C-Modell
├── context_subset.yaml  # Selektierte Kontextfaktoren
└── learnings.yaml       # Vorbereitetes Learnings-Template
```

---

## Projekt abschliessen

```
/bfe-project close BFE-2026-001
```

Führt durch:
1. **Ergebnisse erfassen** (vs. Predictions)
2. **Hypothesen-Tests dokumentieren**
3. **Neue Erkenntnisse** erfassen
4. **Kontext-Updates** für MESO/MAKRO vorschlagen
5. **Propagation** der Learnings einleiten

---

## Beispiel-Session (Schnellmodus)

```
> /bfe-project new --schnell

📋 BFE Projekt erstellen (Schnellmodus)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Projekt-ID: BFE-2026-001
Datum: 2026-01-23

1️⃣ WHO: Wer ist die Zielgruppe?
   [1] Eigentümer EFH
   [2] Eigentümer MFH
   [3] Mieter
   [4] KMU
   > 1

2️⃣ WHAT: Welches Verhalten?
   [1] Heizungsersatz (DOM-HEAT)
   [2] Solar-Installation (DOM-SOLAR)
   [3] E-Auto Adoption (DOM-MOBILITY)
   [4] Energiesparen (DOM-EFFICIENCY)
   > 1

3️⃣ WHEN: Kritischer Moment?
   [1] Heizungsdefekt
   [2] Renovation
   [3] Hauskauf
   > 1

4️⃣ WHERE: Default ändern?
   Aktuell: Fossile Heizung ersetzen durch fossile Heizung
   Vorschlag: Wärmepumpe als Standardempfehlung bei Defekt
   > ja

5️⃣ HOW: Interventions-Mix?
   [1] WHEN (Default) + WHAT(S) (Social) + WHAT(F) (Förderung)
   [2] AWARE (Info) + WHEN (Default)
   [3] WHAT(S) (Social) + WHAT(F) (Förderung) ⚠️ Crowding-Risk
   > 1

✅ Projekt erstellt: projects/2026_heizungsersatz_nudge/

Dateien:
 - model.yaml (10C-Modell ausgefüllt)
 - context_subset.yaml (12 Faktoren selektiert)
 - learnings.yaml (Template)

Nächste Schritte:
 1. model.yaml verfeinern (Predictions hinzufügen)
 2. Intervention implementieren
 3. /bfe-project close BFE-2026-001 nach Abschluss
```

---

## Script-Aufruf (für Automatisierung)

```bash
python scripts/create_bfe_project.py --interactive
python scripts/create_bfe_project.py --name "Heizung" --who efh --what heat --when defekt
python scripts/create_bfe_project.py --list
python scripts/create_bfe_project.py --close BFE-2026-001
```

---

## Verwandte Skills

| Skill | Verwendung |
|-------|------------|
| `/design-model` | Detailliertes 10C-Modell (allgemein) |
| `/design-intervention` | 20-Field Intervention Schema |
| `/case` | Ähnliche Cases finden |
| `/intervention` | Intervention Registry abfragen |

---

## Referenz-Dateien

| Datei | Zweck |
|-------|-------|
| `BCM2_MIKRO_BFE_context.yaml` | Zielgruppen, Domains, Strategien |
| `BCM2_MESO_energy_ch.yaml` | 34 Energie-Kontext-Faktoren |
| `projects/template/` | Projekt-Templates |
