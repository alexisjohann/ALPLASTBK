# /design-intervention - EBF-konforme Intervention erstellen

> Geführter Workflow zur Erstellung EBF-konformer Interventionen nach dem 20-Field Schema (Kapitel 17)

---

## Übersicht

Dieser Skill führt durch die systematische Erstellung einer EBF-konformen Intervention.
Jede Intervention wird gegen das 20-Field Schema validiert.

**Referenz:** Kapitel 17, Appendix HHH (METHOD-TOOLKIT)

---

## Workflow

### Phase 0: 10C Status Quo Assessment (PFLICHT vor Interventions-Design)

**NEU (Kapitel 17, Section 0):** Vor JEDER Intervention muss der 10C Status Quo erfasst werden.

```
10C STATUS QUO ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dieser Schritt erstellt den BASELINE-VEKTOR vor der Intervention.
→ Kapitel 1-16 definieren das "WAS IST"
→ Kapitel 17-20 definieren das "WAS TUN WIR"
→ Der Delta wird nach Intervention gemessen (Kapitel 20, Sec. 7.4)

10C STATUS QUO VEKTOR: S₀ = (L, d, γ, Ψ, Θ, A₀, W₀, φ₀, Scope)
```

**Erfasse die 9 Dimensionen:**

```
┌──────────────┬────────────────────────────────────────────────────────┐
│ CORE         │ FRAGE                                                  │
├──────────────┼────────────────────────────────────────────────────────┤
│ WHO (AAA)    │ Wer ist die Zielgruppe? Welfare Level (L1-L4)?         │
│              │ → L = ___                                              │
├──────────────┼────────────────────────────────────────────────────────┤
│ WHAT (C)     │ Welche FEPSDE-Dimensionen sind betroffen?              │
│              │ → d = {F:__, E:__, P:__, S:__, D:__, X:__}             │
├──────────────┼────────────────────────────────────────────────────────┤
│ HOW (B)      │ Welche Komplementaritäten bestehen bereits?            │
│              │ → γ_current = ___                                      │
├──────────────┼────────────────────────────────────────────────────────┤
│ WHEN (V)     │ Welcher Kontext (8Ψ)?                                  │
│              │ → Ψ = {physisch:__, sozial:__, temporal:__,            │
│              │        institutional:__, resource:__, informational:__,│
│              │        affective:__, identity:__}                      │
├──────────────┼────────────────────────────────────────────────────────┤
│ WHERE (BBB)  │ Woher stammen die Parameter?                           │
│              │ → Θ-Quelle: [literature / empirical / hybrid]          │
├──────────────┼────────────────────────────────────────────────────────┤
│ AWARE (AU)   │ Wie hoch ist die aktuelle Awareness?                   │
│              │ → A₀ = ___ (0-1 Skala)                                 │
├──────────────┼────────────────────────────────────────────────────────┤
│ READY (AV)   │ Wie hoch ist die aktuelle Willingness?                 │
│              │ → W₀ = ___ (0-1 Skala)                                 │
├──────────────┼────────────────────────────────────────────────────────┤
│ STAGE (AW)   │ In welcher Journey-Phase ist die Zielgruppe?           │
│              │ → φ₀ = [awareness/triggered/action/maintenance/stable] │
├──────────────┼────────────────────────────────────────────────────────┤
│ HIERARCHY    │ Welcher Scope/Decision Level?                          │
│ (HI)         │ → Scope = [instant/operative/tactical/strategic/system]│
└──────────────┴────────────────────────────────────────────────────────┘
```

**Status Quo Vektor dokumentieren:**

```yaml
9c_status_quo:
  timestamp: "YYYY-MM-DD"
  context: "<Beschreibung der Ausgangssituation>"

  vector:
    WHO_L: <L1|L2|L3|L4>
    WHAT_d:
      F: <0-1>
      E: <0-1>
      P: <0-1>
      S: <0-1>
      D: <0-1>
      X: <0-1>
    HOW_gamma: <aktueller γ-Wert oder "none">
    WHEN_psi:
      physisch: "<Beschreibung>"
      sozial: "<Beschreibung>"
      temporal: "<Beschreibung>"
    WHERE_theta: <literature|empirical|hybrid>
    AWARE_A0: <0-1>
    READY_W0: <0-1>
    STAGE_phi: <awareness|triggered|action|maintenance|stable>
    HIERARCHY_scope: <instant|operative|tactical|strategic|systemic>

  gaps_identified:
    - "<z.B. A₀ = 0.3 ist niedrig → hohe $I_{AWARE}$ empfohlen>"
    - "<z.B. φ₀ = awareness → hohe $I_{WHEN}$ erst später>"
```

**Weiter zu Phase 0.5 (Modus-Wahl):**

---

### Phase 0.5: Modus-Wahl

Frage den Benutzer welchen Modus er verwenden möchte:

```
┌─────────────────────────────────────────────────────────────────┐
│  /design-intervention - MODUS WÄHLEN                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1] ⚡ SCHNELL (Light Mode)                                    │
│      • 6 Felder (F1-F6)                                         │
│      • ~10 Minuten                                              │
│      • Für: Rapid Screening, initiale Ideation                  │
│                                                                 │
│  [2] 🎯 STANDARD (Hybrid Mode) ← EMPFOHLEN                      │
│      • 12 Felder (F1-F12)                                       │
│      • ~30 Minuten                                              │
│      • Für: Standard Design, Steering Committee                 │
│                                                                 │
│  [3] 📚 VOLLSTÄNDIG (Profound Mode)                             │
│      • Alle 20 Felder                                           │
│      • ~60 Minuten                                              │
│      • Für: Research-Grade, High-Stakes                         │
│                                                                 │
│  [4] 📦 TEMPLATE                                                │
│      • Vordefinierte Intervention anpassen                      │
│      • Variable Zeit                                            │
│      • Für: Bewährte Muster wiederverwenden                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Modus 1: SCHNELL (Light Mode)

### Step 1: Titel & ID (F1)

```
INTERVENTIONS-DESIGN: LIGHT MODE

F1: TITEL & ID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Domain wählen:
  [1] HR        [2] Health    [3] Finance
  [4] Energy    [5] Policy    [6] Other: ___

Kurztitel (max 50 Zeichen):
  > ___

→ ID wird generiert: INT-[DOMAIN]-[NNN]
```

### Step 2: 10C-Zieldimension (F2) - KRITISCH!

```
F2: 10C-ZIELDIMENSION IDENTIFIZIEREN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Welche 10C-Dimension soll verändert werden?

┌─────────────┬─────────┬────────────────────────────┐
│ 10C-Target  │ Δ-Ziel  │ Typische Interventionen    │
├─────────────┼─────────┼────────────────────────────┤
│ AWARE (AU)  │ A(·)↑   │ Information, Salience      │
│ AWARE (AU)  │ κ_AWX↑  │ Dashboard, Progress Track  │
│ WHEN (V)    │ κ_KON→  │ Defaults, Friction         │
│ WHEN (V)    │ κ_JNY→  │ Deadlines, Timing          │
│ WHAT (C.X)  │ W_base↑ │ Titles, Certifications     │
│ WHAT (C.S)  │ u_S↑    │ Norms, Peer Recognition    │
│ WHAT (C.F)  │ u_F↑    │ Bonuses, Benefits          │
│ HOW (B)     │ γ_ij→   │ Goals, Accountability      │
└─────────────┴─────────┴────────────────────────────┘

⚠️ THEORIE-HINWEIS (Appendix IE, Axiom EIT-3):
   Interventionen sind Vektoren I⃗ ∈ [0,1]⁹ im kontinuierlichen 10C-Raum.
   Die 10C-Dimension ist das eigentliche Target!

⚠️ CROWDING-OUT: WHAT(C.S)+WHAT(C.F) und WHAT(C.F)+HOW(B)
   haben negative Komplementarität!

Welche 10C-Dimension? [AWARE/WHEN/WHAT/HOW]: ___
Welches Δ-Ziel? ___
```

### Step 3: Target Structure (F4)

```
F4: TARGET STRUCTURE (aus WHO/AAA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wen adressiert die Intervention?

  [1] IND - Individual
      → Einzelperson trifft Entscheidung
      → Beispiel: Mitarbeiter wählt Weiterbildung

  [2] IDN - Dyadic (Interaktionspartner)
      → Zwei Parteien interagieren
      → Beispiel: Manager-Mitarbeiter Gespräch

  [3] COL - Collective
      → Gruppe als Ganzes
      → Beispiel: Team-Entscheidung, Abteilung

Target Level: [1-3]: ___
```

### Step 4: FEPSDE Dimension (F5)

```
F5: FEPSDE DIMENSION (aus WHAT/C)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Welche Utility-Dimension wird primär angesprochen?

  [F] Financial    → Geld, materielle Ressourcen
  [E] Emotional    → Gefühle, Zufriedenheit
  [P] Physical     → Gesundheit, Energie
  [S] Social       → Beziehungen, Status
  [D] Development  → Wachstum, Lernen
  [X] Existential  → Sinn, Identität

Primäre Dimension: [F/E/P/S/D/X]: ___
Sekundäre (optional): ___
```

### Step 5: Journey Phase (F6)

```
F6: JOURNEY PHASE (aus STAGE/AW)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In welcher Phase der Behavior Change Journey ist die Zielgruppe?

┌─────────────┬─────────────────────────────────────────────────┐
│ Phase       │ Beschreibung                                    │
├─────────────┼─────────────────────────────────────────────────┤
│ awareness   │ Weiß nicht, dass Problem existiert              │
│ triggered   │ Denkt darüber nach, plant zu handeln            │
│ action      │ Handelt (teilweise)                             │
│ maintenance │ Verhalten stabilisieren                         │
│ stable      │ Verhalten ist zur Gewohnheit geworden           │
└─────────────┴─────────────────────────────────────────────────┘

PHASE-TYPE AFFINITY MATRIX (Chapter 18):
```

[Zeige Matrix basierend auf gewählter 10C-Dimension aus Step 2]

```
Für 10C-Target {10C_TARGET} (≈{CLUSTER}):
  awareness:   α = {value} {recommendation}
  triggered:   α = {value} {recommendation}
  action:      α = {value} {recommendation}
  maintenance: α = {value} {recommendation}
  stable:      α = {value} {recommendation}

Optimale Phase(n) für {10C_TARGET}: {phases}

Zielphase wählen: ___
```

### Step 5b: Lifespan Integration (NEU - Chapter 24)

```
F6b: LIFESPAN INTEGRATION (aus Chapter 24)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Handelt es sich um eine langfristige Life Journey Intervention?

  [1] NEIN - Standard (Wochen/Monate)
      → Überspringen, weiter zu Step 6

  [2] JA - Decade-Scale (Jahre)
      → Decade-Roadmap laden
      → Domain-spezifische Parameter anwenden

  [3] JA - Intergenerational (Family-Level)
      → ROI-Multiplier: 1.7×
      → Critical Transmission Windows prüfen
```

**Bei Option 2 (Decade-Scale):**

```
DECADE-ROADMAP INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Domain: {aus F1}
Zielgruppen-Alter: [20s | 30s | 40s | 50s | 60s+]: ___

→ Lade Roadmap aus data/lifespan-parameters.yaml

┌───────────┬─────────────┬──────────────────┬────────────┐
│ Domain    │ Decade      │ Optimale Phase   │ Opt. Types │
├───────────┼─────────────┼──────────────────┼────────────┤
│ {domain}  │ {decade}    │ {phase}          │ {types}    │
└───────────┴─────────────┴──────────────────┴────────────┘

⚠️ PRÜFUNG:
  Gewählter Typ: {F2}
  Domain-Type Affinity: α_eff = {value}
  Decade-Empfehlung: {types}

  {✅ Typ ist optimal | ⚠️ Typ suboptimal - Empfehlung: {alt_types}}
```

**Bei Option 3 (Intergenerational):**

```
INTERGENERATIONAL INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Domain: {domain}
Kind-Alter: ___

→ Prüfe Critical Transmission Window (CTW):

┌───────────┬─────────────┬────────────────────────────────┐
│ Domain    │ CTW         │ Mechanismus                    │
├───────────┼─────────────┼────────────────────────────────┤
│ Health    │ 0-6 Jahre   │ Food habits, activity patterns │
│ Self-Gov  │ 3-12 Jahre  │ Executive function modeling    │
│ Relations │ 0-5, 12-18  │ Attachment, dating models      │
│ Money     │ 12-22 Jahre │ Financial socialization        │
│ Career    │ 14-22 Jahre │ Aspiration formation           │
│ Living    │ 0-18 Jahre  │ Housing quality effects        │
│ Meaning   │ 15-25 Jahre │ Value transmission             │
└───────────┴─────────────┴────────────────────────────────┘

CTW für {domain}: {ctw_range}
Kind-Alter: {age}

{✅ In CTW - Eltern-Intervention priorisieren! | ⚠️ Außerhalb CTW}

ROI-MULTIPLIER:
  Standard ROI:      1.0×
  Family-Level ROI:  1.7× ← ANWENDEN

Begründung: Eltern-Intervention (partial lifespan) + Kind-Effekt
            (full lifespan) + γ^inter ≈ 0.4 = 70% ROI-Boost
```

**Output für Lifespan Integration:**

```yaml
lifespan_integration:
  enabled: true
  mode: "decade" | "intergenerational"

  decade_context:        # Falls decade
    target_decade: "<20s|30s|...>"
    optimal_phase: "<phase>"
    optimal_dimensions: ["AWARE", "WHO", ...]
    domain_dimension_affinity: <value>

  intergenerational:     # Falls family-level
    child_age: <age>
    ctw_active: true|false
    ctw_domain: "<domain>"
    roi_multiplier: 1.7
    recommendation: "<Eltern-Intervention priorisieren|Standard>"
```

### Light Mode: Zusammenfassung & Validierung

```
LIGHT MODE ZUSAMMENFASSUNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

F1: {id} - {title}
F2: {type_code} ({type_name}) → {target}
F4: {level}
F5: {fepsde_primary}
F6: {phase}

Phase-Type Affinity: α = {affinity_value}
  {affinity_assessment}

Validierung läuft...
```

Führe aus:
```bash
python scripts/check_intervention_compliance.py --depth light <file>
```

---

## Modus 2: STANDARD (Hybrid Mode)

Alle Steps aus Light Mode PLUS:

### Step 6: Framing (F7)

```
F7: FRAMING LOGIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wie wird die Intervention geframed?

  [1] positive - Vorteile hervorheben ("Gewinne X")
  [2] negative - Verluste hervorheben ("Verpasse nicht X")
  [3] social   - Soziale Vergleiche ("80% tun X")
  [4] neutral  - Sachliche Information

Für Segment 'loss_averse': [2] negative empfohlen (σ = 1.4)
Für Segment 'social_oriented': [3] social empfohlen (σ = 1.6)

Framing wählen: [1-4]: ___
```

### Step 7: Autonomie (F8) - KRITISCH für Reaktanz!

```
F8: AUTONOMIE LEVEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wie viel Wahlfreiheit hat die Zielgruppe?

  [1] voluntary   → Völlig freiwillig
  [2] default     → Opt-out (Standard gesetzt)
  [3] mandate     → Verpflichtend
  [4] prohibition → Verboten (bei unerwünschtem Verhalten)

⚠️ REAKTANZ-RISIKO:
  voluntary:   LOW    - Keine Autonomie-Cues nötig
  default:     MEDIUM - Opt-out klar kommunizieren
  mandate:     HIGH   - Autonomie-Cues PFLICHT!
  prohibition: HIGH   - Autonomie-Cues PFLICHT!

Für Segment 'autonomy_seeking':
  mandate/prohibition → σ < 0 (BACKFIRE RISK!)

Autonomie-Level: [1-4]: ___
Autonomie-Cue einbauen? [j/n]: ___
```

### Step 8: Segment Targeting (F9)

```
F9: TARGET SEGMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEGMENT-TARGET MULTIPLIER MATRIX (Chapter 19):

Für 10C-Target {10C_TARGET} (≈{CLUSTER}):
┌──────────────────┬───────┬─────────────────────────────┐
│ Segment          │ σ     │ Empfehlung                  │
├──────────────────┼───────┼─────────────────────────────┤
│ present_biased   │ {σ}   │ {recommendation}            │
│ social_oriented  │ {σ}   │ {recommendation}            │
│ autonomy_seeking │ {σ}   │ {recommendation}            │
│ loss_averse      │ {σ}   │ {recommendation}            │
│ sophisticates    │ {σ}   │ {recommendation}            │
│ naifs            │ {σ}   │ {recommendation}            │
└──────────────────┴───────┴─────────────────────────────┘

σ > 1.3: Sehr effektiv ✅
σ < 0.5: Nicht empfohlen ⚠️
σ < 0:   BACKFIRE RISK ❌

Optimale Segmente: {segments}
Zu vermeidende Segmente: {avoid_segments}

Target-Segmente wählen (kommasepariert): ___
```

### Step 9: Komplementarität (F10) - KRITISCH!

```
F10: KOMPLEMENTARITÄT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ CROWDING-OUT MATRIX (Chapter 20):

┌─────────────────────────────────────────────────────────────────┐
│  BEKANNTE KONFLIKTE (γ < 0)                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHAT(C.S) + WHAT(C.F) [Social + Financial] → γ = -0.2          │
│  → Finanzielle Anreize untergraben soziale Normen               │
│  → NIEMALS kombinieren ohne explizite Begründung!               │
│                                                                 │
│  WHAT(C.F) + HOW(B) [Financial + Commitment] → γ = -0.3         │
│  → Externe Belohnungen untergraben intrinsische Motivation      │
│  → NIEMALS kombinieren ohne explizite Begründung!               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

BEKANNTE SYNERGIEN (γ > 0.3):

  AWARE + WHEN: γ = +0.4 (Awareness macht Kontextänderungen effektiver)
  AWARE(feedback) + WHEN: γ = +0.3 (Feedback verstärkt Kontextänderungen)
  WHEN + HOW: γ = +0.4 (Zeitdruck verstärkt Commitment)
  WHAT(C.X) + WHAT(C.S): γ = +0.3 (Identität und soziale Normen verstärken sich)

Für 10C-Target {10C_TARGET}:
  Synergien mit: {synergy_targets}
  Konflikte mit: {conflict_targets}

Wird diese Intervention mit anderen kombiniert? [j/n]: ___
  Falls ja, welche? ___
```

### Step 10: Side Effects (F11)

```
F11: SIDE EFFECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Risiko-Level:
  [1] low    - Geringe Nebenwirkungen erwartet
  [2] medium - Einige Spillover-Effekte möglich
  [3] high   - Signifikante Risiken vorhanden

Positive Spillovers (Beispiele):
  > ___

Negative Spillovers (Beispiele):
  > ___

Crowding-Out Risiken (automatisch aus F10):
  {crowding_out_warnings}
```

### Step 11: Temporal Scope (F12)

```
F12: TEMPORAL SCOPE (aus HIERARCHY/HI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌───────────┬──────────────────┬─────────────────────────────────┐
│ Scope     │ Zeitrahmen       │ Typische Entscheidungsebene     │
├───────────┼──────────────────┼─────────────────────────────────┤
│ instant   │ Sofort           │ L0 (Operative)                  │
│ operative │ Tage - Wochen    │ L0-L1                           │
│ tactical  │ Wochen - Monate  │ L1 (Strategic), L1+ (Corporate) │
│ strategic │ Monate - Jahre   │ L1+, L2 (Derived)               │
│ systemic  │ Jahre            │ L2, L3 (Emergent)               │
└───────────┴──────────────────┴─────────────────────────────────┘

Scope wählen: [instant/operative/tactical/strategic/systemic]: ___
Dauer (Wochen): ___
Decision Level: [L0/L1/L1+/L2/L3]: ___
```

### Hybrid Mode: Zusammenfassung & Validierung

```
HYBRID MODE ZUSAMMENFASSUNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIER 1 (Emergent):
  F1: {id} - {title}
  F2: {type_code} ({type_name}) → {target}
  F4: {level}
  F5: {fepsde_primary}
  F6: {phase}

TIER 2 (Operational):
  F7:  {framing}
  F8:  {autonomy} (Reaktanz: {reactance_risk})
  F11: {side_effect_risk}
  F12: {scope} ({duration} Wochen, {decision_level})

TIER 3 (Interface):
  F9:  Segmente: {segments}
  F10: Synergien: {synergies}, Konflikte: {conflicts}

VALIDIERUNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Führe aus:
```bash
python scripts/check_intervention_compliance.py --depth hybrid <file>
```

---

## Modus 3: VOLLSTÄNDIG (Profound Mode)

Alle Steps aus Hybrid Mode PLUS:

### F13: Evaluation Plan
### F14: Path Function (door_opener, escalator, amplifier, stabilizer)
### F15: Repetition Pattern
### F16: Responsibility Assignment
### F17: Evidence & Literature Sources
### F18: System Integration
### F19: Detailed Description & Mechanism
### F20: Status Tracking

---

## Modus 4: TEMPLATE

```
VERFÜGBARE TEMPLATES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] HR: Onboarding Nudge (I_WHEN high)
    → Auto-enrollment in Weiterbildung
    → Bewährt bei: present_biased, naifs

[2] HR: Recognition Program (I_WHO,others high)
    → Peer Recognition System
    → Bewährt bei: social_oriented
    → ⚠️ NICHT mit Financial (I_WHAT,F) kombinieren!

[3] HR: Development Goal Setting (I_HOW high)
    → Strukturierte Zielvereinbarung
    → Bewährt bei: sophisticates, autonomy_seeking
    → ⚠️ NICHT mit Financial (I_WHAT,F) kombinieren!

[4] Health: Feedback Dashboard (I_AWARE high)
    → Fortschritts-Tracking
    → Bewährt bei: present_biased

[5] Finance: Default Savings (I_WHEN high)
    → Auto-enrollment in Sparplan
    → Bewährt bei: present_biased, naifs

[6] Custom: Leere Vorlage
```

---

## Integration mit anderen Skills

```
WORKFLOW INTEGRATION (10C Learning Loop)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/case-manage find              → Ähnliche Cases suchen
        ↓
/design-model                  → Gesamtmodell designen
        ↓
┌───────────────────────────────────────────────────────────────────┐
│ /design-intervention                                              │
│                                                                   │
│   Phase 0: 10C STATUS QUO ERFASSEN ← S₀ Vektor (Kap. 17, Sec. 0)  │
│        ↓                                                          │
│   Phase 0.5: Modus wählen                                         │
│        ↓                                                          │
│   Phase 1-n: Intervention spezifizieren (F1-F20)                  │
│        ↓                                                          │
│   ⚠️ EIP CHECK (automatisch) → Neues Konzept? → Evidence prüfen! │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
        ↓
/intervention-manage new       → Projekt anlegen (inkl. S₀)
        ↓
[Durchführung]
        ↓
/intervention-manage close     → Results erfassen
        ↓
┌───────────────────────────────────────────────────────────────────┐
│ 10C DELTA MESSUNG (Kapitel 20, Sec. 7.4)                           │
│                                                                   │
│   ΔS = S₁ - S₀ = (ΔL, Δd, Δγ, ΔΨ, ΔΘ, ΔA, ΔW, Δφ, ΔScope)       │
│                                                                   │
│   → ΔA, ΔW: Updates für AU, AV Modelle                           │
│   → Δγ: Neue Komplementaritäts-Schätzungen → HOW (B)             │
│   → ΔΘ: Parameter-Repository (BBB) aktualisiert                  │
│   → Δφ: Journey-Übergangswahrscheinlichkeiten (AW) verfeinert    │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
        ↓
/case-manage add               → Neuen Case erstellen (mit Δ-Werten)
        ↓
[Loop: Nächste Intervention profitiert von aktualisierten Parametern]
```

---

## Evidence Integration Pipeline (EIP) Check

**KRITISCH:** Bei jeder Intervention prüfen ob EIP-Trigger vorliegen!

### Automatische Trigger-Prüfung

Nach Abschluss der Intervention-Spezifikation MUSS geprüft werden:

```
EIP TRIGGER CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☐ TR1: Wird neue TERMINOLOGIE eingeführt?
       → Neue Namen, Konzeptbezeichnungen?

☐ TR2: Wird ein neuer MECHANISMUS beschrieben?
       → Neue Transformation, Wirkmechanismus?

☐ TR3: Werden neue γ-WERTE behauptet?
       → Komplementaritäten, Synergien, Konflikte?

☐ TR4: Wird eine neue FORMEL entwickelt?
       → Gleichungen, Algorithmen?

☐ TR5: Ist die Intervention SELBST neu?
       → Nicht aus bestehendem Template?

Mindestens ein Trigger? → EIP STARTEN!
```

### EIP Workflow (wenn Trigger erkannt)

```
1. INTERNE QUELLEN ZUERST prüfen:
   a) bcm_master.bib durchsuchen (1,922+ Papers)
   b) LIT-Appendices prüfen (R/D/M/O)
   c) Case Registry prüfen

2. NUR WENN NÖTIG: Externe Quellen
   d) Google Scholar
   e) SSRN, NBER, arXiv

3. PRO + CONTRA Evidenz dokumentieren:
   → ≥3 PRO-Papers erforderlich
   → CONTRA-Evidenz AKTIV suchen!

4. Entscheidung treffen:
   → Integrieren / Verwerfen / Modifizieren

5. In concept-registry.yaml dokumentieren
```

### Dokumentation

| Datei | Zweck |
|-------|-------|
| `data/concept-registry.yaml` | Alle EIP-Entscheidungen |
| `quality/rejected_concepts.md` | Verworfene Konzepte |
| `docs/workflows/evidence-integration-pipeline.md` | Vollständige EIP-Doku |

---

## Phase FINAL: Automatische Portfolio-Generierung

**NEU (Kapitel 20, Section 4.4):** Nach der Interventions-Spezifikation werden automatisch **3 Portfolio-Varianten** zum Vergleich generiert.

### Automatische Archetyp-Auswahl

Basierend auf dem 10C Status Quo Vektor ($\vec{S}_0$) werden passende Archetypen vorgeschlagen:

```
PORTFOLIO-GENERIERUNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Basierend auf deinem 10C Status Quo:
  → A₀ = {aware_level}
  → W₀ = {ready_level}
  → φ₀ = {phase}
  → Segment = {segment}

Ich generiere 3 vergleichbare Portfolios:
```

### Die 7 verfügbaren Archetypen

| Archetyp | Fokus | Constraint | Wann wählen? |
|----------|-------|------------|--------------|
| 🚀 **Quick Wins** | Schnell | Zeit ≤ 4 Wochen | Budget/Zeit knapp |
| ⭐ **Optimal Mix** | Max E(P) | C(P) ≥ 0.85 | Ressourcen vorhanden |
| 💰 **Budget-Constrained** | Max ROI | Cost ≤ B | Festes Budget |
| 🛡️ **Low-Risk** | Min Backfire | γ ≥ 0.1 | Risiko-avers |
| 🔄 **Sustainable** | Langfristig | Scope ≥ identity | Habit-Formation |
| 📈 **Max BC** | Max P(BC) | E(P\|S₀) max | Verhaltensänderung kritisch |
| 🌱 **Eco-Sustainable** | Ökologisch | Δd_X ≥ 0 | Nachhaltigkeit wichtig |

### Automatische Selektion basierend auf Kontext

```
KONTEXT-BASIERTE PORTFOLIO-AUSWAHL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IF Budget begrenzt:
    → IMMER 💰 Budget-Constrained als Option 1

IF Zeit kritisch (< 4 Wochen):
    → IMMER 🚀 Quick Wins als Option 1

IF Risiko-avers oder Stakeholder skeptisch:
    → IMMER 🛡️ Low-Risk als Option 1

IF Langfristige Wirkung wichtig:
    → IMMER 🔄 Sustainable als Option 1

IF Ökologie/Nachhaltigkeit relevant (d_X gewichtet):
    → IMMER 🌱 Eco-Sustainable als Option

ELSE:
    → Default: 🚀 Quick Wins + ⭐ Optimal + 📈 Max BC
```

### Generiertes Output Format

```
┌─────────────────────────────────────────────────────────────────┐
│  PORTFOLIO-VERGLEICH: 3 Optionen                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  OPTION A: 🚀 QUICK WINS                                        │
│  ───────────────────────────────────────────────────────────── │
│  Interventionen:                                                │
│    • I_AWARE: {info_campaign}                                   │
│    • I_WHEN: {default_change}                                   │
│  E(P) erwartet: 20%                                             │
│  Kosten: €{cost_a}                                              │
│  Zeit bis Wirkung: 2-4 Wochen                                   │
│  Backfire-Risiko: Niedrig                                       │
│  ROI (kurz): ★★★                                                │
│                                                                 │
│  OPTION B: ⭐ OPTIMAL MIX                                       │
│  ───────────────────────────────────────────────────────────── │
│  Interventionen:                                                │
│    • I_AWARE: {info_campaign}                                   │
│    • I_WHO: {identity_intervention}                             │
│    • I_WHO,o: {social_norm} (⚠️ nicht mit I_WHAT,F!)            │
│    • I_HOW: {commitment}                                        │
│  E(P) erwartet: 45%                                             │
│  Kosten: €{cost_b}                                              │
│  Zeit bis Wirkung: 3-6 Monate                                   │
│  Backfire-Risiko: Mittel                                        │
│  ROI (lang): ★★★★                                               │
│                                                                 │
│  OPTION C: 🌱 ECO-SUSTAINABLE                                   │
│  ───────────────────────────────────────────────────────────── │
│  Interventionen:                                                │
│    • I_AWARE: {digital_info} (kein Papier)                      │
│    • I_WHEN: {green_default}                                    │
│    • I_WHO: {eco_identity}                                      │
│  E(P) erwartet: 25%                                             │
│  Kosten: €{cost_c}                                              │
│  Zeit bis Wirkung: 4-8 Wochen                                   │
│  Backfire-Risiko: Minimal                                       │
│  Δd_X: +0.15 (ökologisch positiv)                               │
│  ROI (lang): ★★★★                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Vergleichs-Matrix generieren

```
PORTFOLIO-VERGLEICHS-MATRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌───────────────────┬──────────┬──────────┬──────────┐
│ Dimension         │ Option A │ Option B │ Option C │
├───────────────────┼──────────┼──────────┼──────────┤
│ E(P) erwartet     │ 20%      │ 45%      │ 25%      │
│ P(BC|S₀)          │ 18%      │ 42%      │ 23%      │
│ Kosten (relativ)  │ 1×       │ 4×       │ 1.5×     │
│ Zeit bis Wirkung  │ 2-4 W    │ 3-6 M    │ 4-8 W    │
│ Backfire-Risiko   │ Niedrig  │ Mittel   │ Minimal  │
│ Nachhaltigkeit    │ Kurz     │ Mittel   │ Hoch     │
│ Δd_X (Ökologie)   │ 0        │ 0        │ +0.15    │
│ ROI (kurz)        │ ★★★      │ ★★       │ ★★★      │
│ ROI (lang)        │ ★★       │ ★★★★     │ ★★★★     │
└───────────────────┴──────────┴──────────┴──────────┘

EMPFEHLUNG basierend auf deinem Kontext:
  → {recommendation_text}
```

### FEPSDE-KPI Zuordnung pro Portfolio

```
FEPSDE-KPIs PRO PORTFOLIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────┬───────────────────┬───────────────────┬───────────────────┐
│ Dim.    │ Option A KPIs     │ Option B KPIs     │ Option C KPIs     │
├─────────┼───────────────────┼───────────────────┼───────────────────┤
│ F       │ Conversion Rate Δ │ CLV Impact        │ Cost Savings      │
│ E       │ Engagement Score  │ NPS               │ Sentiment Score   │
│ P       │ Adoption Rate     │ Habit Strength    │ Usage Frequency   │
│ S       │ -                 │ Referral Rate     │ Community Part.   │
│ D       │ -                 │ Skill Acquisition │ -                 │
│ X       │ -                 │ -                 │ Carbon Δ, Waste Δ │
└─────────┴───────────────────┴───────────────────┴───────────────────┘

Primäre KPIs für Messung:
  Option A: {kpi_list_a}
  Option B: {kpi_list_b}
  Option C: {kpi_list_c}
```

### Benutzer-Entscheidung

```
ENTSCHEIDUNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Welches Portfolio implementieren?

  [A] 🚀 Quick Wins - Schnell starten, moderate Wirkung
  [B] ⭐ Optimal Mix - Maximale Wirkung, mehr Aufwand
  [C] 🌱 Eco-Sustainable - Ökologisch positiv
  [X] Alle 3 parallel (A/B Test)
  [M] Manuell anpassen

Wahl: ___
```

---

## Validierung

Nach jeder Intervention:

```bash
# Einzelne Intervention prüfen
python scripts/check_intervention_compliance.py <file.yaml>

# Portfolio prüfen (mehrere Interventionen)
python scripts/check_intervention_compliance.py --portfolio <portfolio.yaml>

# Alle Interventionen im Verzeichnis
python scripts/check_intervention_compliance.py --all data/interventions/
```

**Mindestanforderung: Score ≥ 85%**

---

## Checkliste vor Abschluss

```
☐ 10C-Zieldimension identifiziert (AWARE, WHEN, WHAT, HOW)
☐ Δ-Ziel definiert (z.B. A↑, κ_KON→, u_S↑, γ→)
☐ Phase-Affinity geprüft (α > 0.5)
☐ Segment-Multiplier geprüft (keine σ < 0 ohne Warning)
☐ Crowding-Out Risiken dokumentiert (WHAT(C.S)+WHAT(C.F), WHAT(C.F)+HOW(B))
☐ Autonomie-Level mit Reaktanz-Risiko abgestimmt
☐ Scope-Level Konsistenz geprüft
☐ Validierung: Score ≥ 85%
```

---

## Fehler vermeiden

❌ **NICHT:** "Maßnahme" oder "Initiative" ohne 10C-Zuordnung
✅ **STATTDESSEN:** Immer 10C-Zieldimension identifizieren

❌ **NICHT:** Social ($I_{\text{WHO},o}$) + Financial ($I_{\text{WHAT},F}$) kombinieren ohne Begründung
✅ **STATTDESSEN:** Crowding-Out dokumentieren, alternative Sequenzierung prüfen

❌ **NICHT:** mandate/prohibition bei autonomy_seeking Segment
✅ **STATTDESSEN:** Autonomie-Cues einbauen oder Segment ausschließen

❌ **NICHT:** Phase wählen mit α < 0.3 für gewählte Dimension
✅ **STATTDESSEN:** Phase-Dimension Affinity Matrix konsultieren

---

*Version 1.3 | Januar 2026*
*Referenz: Kapitel 17, Kapitel 20 (Sec. 4.4, 4.5, 7.4), templates/intervention-schema.yaml*

**Changelog:**
- v1.3: Automatische Portfolio-Generierung (Phase FINAL), 7 Archetypen, FEPSDE-KPI Framework
- v1.2: 10C Status Quo Assessment (Phase 0) hinzugefügt, 10C Learning Loop vollständig integriert
- v1.1: EIP-Integration hinzugefügt (Evidence Integration Pipeline)
