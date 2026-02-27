# /design-model - Verhaltensmodell designen (EEE Workflow)

Designen Sie ein evidenzbasiertes Verhaltensmodell mit dem **EEE Workflow** (Appendix EEE: METHOD-DESIGN).

Dies ist der **standardisierte Single Source of Truth** für alle Modelldesign-Aufgaben.

## Verwendung

```
/design-model
/design-model --mode schnell
/design-model --mode geführt
/design-model --mode template
/design-model --mode custom
```

## Der EEE Workflow: 9-Schritt System

Der Workflow garantiert **3+1 Choice Architecture** (Axiom MD-1) bei jedem Schritt:
- **3 kuratierte Optionen** basierend auf Best Practices
- **1 Custom Option** für freie Gestaltung

---

## Step 0: Workflow-Modus wählen

| Modus | Beschreibung | Zeit | Resultat |
|-------|-------------|------|----------|
| **⚡ SCHNELL** | 3 Fragen → komplettes 10C Modell via GGG Defaults | 10 min | Sofort einsatzbereit |
| **🎯 GEFÜHRT** | Alle 9 Steps mit Erklärungen & 3+1 Optionen | 45 min | Umfassend dokumentiert |
| **📦 TEMPLATE** | Seed-Modell aus FFF Registry anpassen | 20 min | Validiertes Fundament |
| **🔧 CUSTOM** | Freie Gestaltung mit allen 9 Steps | Variabel | Maximal kontrolliert |

---

## Steps 1-9: Der EEE Workflow (GEFÜHRT-Modus)

### **Step 1: Entry Point** (Theory vs. Practice)

**3+1 Optionen:**
1. **Theory-Driven** (Begin with EBF concept)
   - Start mit existierenden CORE Appendices (AAA-AW)
   - Passt, wenn Sie ein EBF-Konzept anwenden möchten

2. **Practice-Driven** (Begin with Gestaltungsanlass)
   - Start mit konkretem Problem/Situation
   - Passt, wenn Sie ein reales Verhalten modellieren müssen

3. **Hybrid** (Theory ↔ Practice Iteration)
   - Abwechselnde Theorie-Praxis-Zyklen
   - Passt, wenn Iteration erforderlich ist

4. **CUSTOM** (Freie Wahl)

**Output:** Gestaltungsanlass (falls Practice) oder EBF Concept (falls Theory)

---

### **Step 2: Scope Definition** (Verhalten eingrenzen)

**3+1 Optionen für Verhaltentyp:**
1. **Decision** (Einmalentscheidung)
   - z.B. Rentenmodell wählen, Impfung, Jobwechsel
   - Mathematik: Logistic/Binary Choice

2. **Continuous** (Wiederholtes Verhalten)
   - z.B. Sparbetrag, Energieverbrauch, Trainingsfrequenz
   - Mathematik: Linear/CES Functional Form

3. **Process** (Veränderung über Zeit)
   - z.B. Habit-Bildung, Learning, Adoption Journey
   - Mathematik: Dynamic/BCJ Models

4. **CUSTOM** (Spezifisch definieren)

**Output:** Scope-Definiton (Decision/Continuous/Process)

---

### **Step 3: Context Specification** (Kontext Ψ)

**3+1 Optionen für Kontextdimensionen:**

**GGG-Default auswählen nach Domain + Level:**

1. **Vorkonfiguriert (GGG Tabelle 1)**
   - Auswahl: Domain (Vorsorge, Health, Finance, HR, Energy, Public)
   - Auswahl: Level (Individual, Household, Organization)
   - System generiert: Ψ mit (trust, digital_adoption, autonomy, risk_aversion)
   - Quelle: Tabelle GGG-1 (Level × Geography)

2. **Custom Context Dimensions**
   - Sie definieren explizit welche Ψ-Faktoren relevant sind
   - z.B. Saisonalität, Peer Effects, Availability, Cost

3. **Literatur-basiert**
   - Start mit Kontext aus existierendem Seed-Modell (FFF Registry)
   - Anpassung an Ihre Situation

4. **CUSTOM** (Vollständig frei)

**Output:** Kontext Ψ (Dimensionen + Werte)

---

### **Step 3b: Lifespan Context** (NEU - Chapter 24 Integration)

**Frage:** Ist das Verhalten Teil einer langfristigen Life Journey?

**3+1 Optionen:**

1. **Kurzfristig (Standard)**
   - Zeitrahmen: Wochen bis Monate
   - Keine Lifespan-Parameter erforderlich
   - Standard P_eff Berechnung

2. **Langfristig (Decade-Scale)**
   - Zeitrahmen: Jahre bis Jahrzehnte
   - System lädt domain-spezifische Parameter:
     ```
     Domain: [Health | Money | Career | Relationships | Self-Gov | Living | Meaning]
     Decade: [20s | 30s | 40s | 50s | 60s+]

     → α_domain, β_domain aus data/lifespan-parameters.yaml
     → Decade-Roadmap mit optimalen T-Typen
     → Konvergenzzeit-Schätzung
     ```
   - Quelle: Appendix RRR (METHOD-LIFETIME), Chapter 24

3. **Intergenerational (Family-Level)**
   - Zeitrahmen: 2-3 Generationen (60+ Jahre)
   - Zusätzliche Parameter:
     ```
     φ_0 (child) = φ_base + Σ γ^inter × (φ^parent - φ̄)

     → Spillover-Matrix Γ^inter aus data/lifespan-parameters.yaml
     → Critical Transmission Windows (CTW)
     → ROI_family = 1.7 × ROI_individual
     ```
   - Quelle: Appendix BI (DOMAIN-LIFESPAN)

4. **CUSTOM** (Spezifischer Zeitrahmen)

**Output bei Option 2 oder 3:**

```yaml
lifespan_context:
  enabled: true
  timeframe: "decade" | "intergenerational"
  domain: "<health|money|career|...>"

  domain_parameters:         # Aus RRR
    alpha: <value>
    beta: <value>
    lambda: <value>
    convergence_95_weeks: <value>

  decade_roadmap:            # Falls decade-scale
    current_decade: "<20s|30s|...>"
    optimal_phase: "<awareness|triggered|action|maintenance>"
    optimal_dimensions: ["AWARE", "WHO", ...]

  intergenerational:         # Falls family-level
    phi_0_adjustment: <value>
    ctw_active: true|false
    roi_multiplier: 1.7
```

**Beispiel (Health, 30s, Individual):**

```
Domain: Health
Decade: 30s
→ α = 0.05, β = 0.02
→ Optimal Phase: Action
→ Optimal Dimensions: AWARE, WHEN, WHO
→ Convergence: ~10 Monate (95%)
→ Decade Roadmap empfiehlt: Hohe Intensität
```

**Beispiel (Money, Family-Level, Kind in CTW):**

```
Domain: Money
Timeframe: Intergenerational
Child Age: 16 (in CTW 12-22)
Parent φ_money: 0.45

→ φ_0 (child) = 0.20 + 0.50 × (0.45 - 0.40) = 0.225
→ CTW aktiv: JA
→ ROI_family = 1.7 × ROI_ind
→ Empfehlung: Eltern-Intervention während CTW priorisieren
```

---

### **Step 4: Variable Selection** (Komplementarität C und γ)

**3+1 Optionen für Utility-Dimensionen:**

**GGG-Default auswählen nach Domain:**

1. **Vorkonfiguriert (GGG Tabelle 2)**
   - Auswahl: Domain + Scope Type
   - System generiert: C = {F, E, P, S, D, E} mit Gewichten
   - FEPSDE = Financial, Emotional, Practical, Social, Deliberative, Environmental
   - Quelle: Tabelle GGG-2 (Domain × Level → C Gewichte)

2. **Reduziert** (Subset der FEPSDE)
   - z.B. nur {Financial, Social} für Pension Decision
   - Einfaches Modell, leichter zu schätzen

3. **Erweitert** (Zusatzdimensionen)
   - z.B. FEPSDE + Health, Identity, Legacy
   - Umfassenderes Modell, mehr Daten erforderlich

4. **CUSTOM** (Vollständig frei)

**GGG-Default für Komplementarität (Tabelle 3):**
- System generiert γ-Matrix basierend auf Domain
- z.B. γ(F,S) > 0 = Financial und Social verstärken sich gegenseitig

**Output:** Utility-Vektor C, Komplementarität γ

---

### **Step 5: Functional Form** (Mathematische Form)

**3+1 Optionen nach Scope Type (GGG Tabelle 4):**

**Decision Models:**
1. Logistic: U(x) = 1/(1 + exp(-β₀ - Σβᵢcᵢ - γΨ))
2. Linear-CES: U(x) = (Σαᵢcᵢ^ρ)^(1/ρ) + βΨ
3. Structured Additive: U(x) = ΣwᵢUᵢ(cᵢ) + γΨ + Noise
4. CUSTOM (Ihre Formel)

**Continuous Models:**
1. Linear: cₜ = β₀ + Σβᵢcᵢ,ₜ₋₁ + γΨ + Noise
2. CES: cₜ = A(Σαᵢcᵢ,ₜ₋₋₁^ρ)^(1/ρ) + Noise
3. Log-linear: log(cₜ) = β₀ + Σβᵢlog(cᵢ) + γΨ
4. CUSTOM (Ihre Formel)

**Process Models:**
1. Behavioral Change Journey (BCJ): S(t) = f(φ, τ, ρ, κ, Ψ)
2. Logistic Growth: S(t) = K/(1 + exp(-r(t-t₀)))
3. Habit Formation: cₜ = λcₜ₋₁ + (1-λ)c*(Ψ)
4. CUSTOM (Ihre Formel)

**Output:** Functional Form Θ

---

### **Step 6: Parameter Estimation** (Woher die Zahlen?)

**3+1 Optionen nach Domain (GGG Tabelle 5):**

1. **Literatur-basiert** (GGG Defaults)
   - Verwende Standardwerte aus Fehr/Thaler/Kahneman Literatur
   - Quelle: BBB Appendix (Parameter Repository)
   - Schnell, aber weniger präzise für Ihren Kontext

2. **Empirisch** (Ihr eigenes Datensample)
   - Schätzung mit Ihren Daten (OLS, MLE, Bayesian)
   - Zeitaufwändig, aber kontextspezifisch

3. **Hybrid** (Literatur + Anpassung)
   - Start mit Literaturwerten
   - Anpassung mit kleinem Datensample (Calibration)
   - Balance zwischen Schnelligkeit und Kontextpassung

4. **CUSTOM** (Andere Quelle)

**Output:** Parameter-Vektor Θ mit Herkunft dokumentiert

---

### **Step 7: Predictions & Statements** (Testbare Vorhersagen)

**3+1 Optionen für Vorhersagetypen:**

1. **Point Predictions**
   - Konkrete Werte: "45% werden sich anmelden"
   - Einfach, aber nicht robust gegen Unsicherheit

2. **Interval Predictions** (mit 90%-KI)
   - "40%-50% werden sich anmelden"
   - Robuster gegen Parametraunsicherheit

3. **Comparative Predictions**
   - "Intervention A > Intervention B um 15%-25%"
   - Robuster gegen absolute Fehler

4. **CUSTOM** (Ihre Vorhersageform)

**Output:** Predictions als testbare Statements

---

### **Step 8: Model Registry** (In FFF speichern)

**Automatisch:**
- Model_ID generieren
- Metadata erfassen (Gestaltungsanlass, Entry Point, Domain, Tags)
- Input/Output dokumentieren
- Validation-Status = "pending"

**Output:** Modell in FFF Registry registriert
**Link:** Appendix FFF (METHOD-REGISTRY) mit 6-Component Schema

---

### **Step 9: Output Generation** (Dokumentation)

**3+1 Optionen für Output-Format:**

1. **LaTeX Document** (für akademische Audience)
   - `.tex`-Datei mit vollständiger Modellbeschreibung
   - Math, Notation, Formal

2. **Markdown Report** (für Stakeholder-Communication)
   - `.md`-Datei mit Zusammenfassung
   - Einfache Sprache, Visualisierungen

3. **Python Code** (für Implementation)
   - `.py` Python Script zur Modellsimulation
   - Parametrisierbar, ausführbar

4. **CUSTOM** (Andere Formate)

**Output:** Modell-Dokument im gewählten Format

---

## SCHNELL-Modus: 3 Fragen → Komplettes Modell

Wenn Sie es schnell brauchen, beantworten Sie nur:

**Frage 1: Entry Point**
- Haben Sie ein konkretes Verhalten/Problem? → Practice-Driven
- Oder wollen Sie ein EBF-Konzept anwenden? → Theory-Driven

**Frage 2: Domain + Level**
- Welches Feld? (Vorsorge, Health, Finance, HR, Energy, Public)
- Welche Ebene? (Individual, Household, Organization)

**Frage 3: Scope Type**
- Decision, Continuous, oder Process?

**Dann generiert das System automatisch via GGG:**
- Ψ (Context) aus Tabelle GGG-1
- C, γ (Variables) aus Tabelle GGG-2, GGG-3
- Functional Form aus Tabelle GGG-4
- Parameter aus Tabelle GGG-5
- Awareness aus Tabelle GGG-6
- Willingness aus Tabelle GGG-6
- Stage aus Tabelle GGG-7

**Output:** Komplettes 10C-konformes Modell (marked as "CONFIG-derived", requires validation)

---

## TEMPLATE-Modus: Seed-Modell anpassen

Das FFF Registry enthält 8 vorkonfigurierte DACH-Seed-Modelle:

| ID | Domain | Scope | Status | Accuracy |
|----|--------|-------|--------|----------|
| SEED-CH-01 | PK Enrollment | Decision | Validated | 78% |
| SEED-CH-02 | Contribution Amount | Continuous | Validated | 82% |
| SEED-CH-03 | Change Adoption | Process | Partial | 71% |
| SEED-CH-04 | Energy Reduction | Continuous | Validated | 75% |
| SEED-AT-01 | Preventive Health | Decision | Validated | 70% |
| SEED-AT-02 | Tax Compliance | Decision | Validated | 73% |
| SEED-DE-01 | Riester Family | Decision | Partial | 68% |
| SEED-DE-02 | Digitalization | Process | Partial | 64% |

**Workflow:**
1. Seed auswählen (Ähnlichkeit zu Ihrem Gestalutungsanlass)
2. Differenzen identifizieren (Was ist anders?)
3. Nur Unterschiede anpassen
4. Validierung durchführen (against target behavior)

**Output:** Adaptiertes Seed-Modell

---

## CUSTOM-Modus: Alle 9 Steps mit Kontrolle

Sie durchlaufen alle 9 Steps mit vollständiger Kontrolle über jede Wahl.
Keine Vorgaben, keine Defaults – Sie entscheiden alles.

---

## Axiomatische Grundlagen (aus EEE)

| Axiom | Beschreibung |
|-------|-------------|
| **MD-1** | 3+1 Choice Architecture (bei jedem Step 3 Optionen + Custom) |
| **MD-2** | Registry-Based Option Selection (Optionen aus FFF Registry) |
| **MD-3** | Scope-Context Iteration (Scope bestimmt welche Ψ-Dimensionen relevant) |
| **MD-4** | Option Selection Principles (Dimension, Tradeoff, Stakeholder, Abstraction, Risk) |

---

## Validation Loop (nach Modell-Erstellung)

**Automatisch nach Step 8:**

1. **Registrierung im FFF** mit Status "pending"
2. **Validation-Review** erforderlich innerhalb 12 Monaten
3. **Accuracy Check** gegen Realverhalten
4. **Falsification Check** (welche Vorhersagen sind bereits falsch?)
5. **Learning Loop** (Insights zurück zur Modell-Verbesserung)

---

## Evidence Integration Pipeline (EIP) Check

**KRITISCH:** Bei Modelldesign können neue Konzepte entstehen, die EIP erfordern!

### Automatische Trigger-Erkennung

Während des Modelldesigns auf diese Trigger achten:

| # | Trigger | Beispiel | Aktion |
|---|---------|----------|--------|
| TR1 | Neue Terminologie eingeführt | "Mental Identity Budgeting" | EIP starten |
| TR2 | Neuer Mechanismus beschrieben | "$I_{\text{WHAT},F} \to I_{\text{WHO}}$ Transformation" | EIP starten |
| TR3 | Neue γ-Werte behauptet | "γ(AWARE,WHEN) = +0.4" | Evidenz prüfen |
| TR4 | Neue Formel/Gleichung entwickelt | "Z(n) = Z_max × (1-0.03×...)" | EIP starten |
| TR5 | Neue Variable/Dimension hinzugefügt | "Legacy-Dimension in FEPSDE" | EIP starten |

### EIP-Workflow bei Trigger

```
┌─────────────────────────────────────────────────────────────────┐
│  EIP Check während Modelldesign                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Bei jedem Step prüfen:                                         │
│  ├── Wird neue Terminologie eingeführt? → TR1                   │
│  ├── Wird neuer Mechanismus beschrieben? → TR2                  │
│  ├── Werden γ-Werte ohne Quelle verwendet? → TR3                │
│  ├── Wird neue Formel entwickelt? → TR4                         │
│  └── Wird neue Variable/Dimension hinzugefügt? → TR5            │
│                                                                 │
│  Bei Trigger:                                                   │
│  1. INTERNE QUELLEN ZUERST (bcm_master.bib, LIT, Case Registry) │
│  2. Externe Quellen (Google Scholar, SSRN) nur wenn nötig       │
│  3. PRO/CONTRA Evidenz dokumentieren                            │
│  4. Entscheidung: integrate / reject / modify                   │
│  5. In concept-registry.yaml dokumentieren                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Integration mit Step 8 (Model Registry)

Bei Registrierung in FFF prüfen:
- Welche Konzepte wurden entwickelt?
- Haben alle Konzepte EIP durchlaufen?
- Sind alle PRO/CONTRA in concept-registry.yaml?

**Referenz:** `docs/workflows/evidence-integration-pipeline.md`

---

## Referenz-Appendices

| Appendix | Kategorie | Zweck |
|----------|-----------|-------|
| **EEE** | METHOD-DESIGN | Dieser Workflow (9 Steps + Axiome) |
| **GGG** | METHOD-CONFIG | Model Configurator (7 Mapping Tables) |
| **FFF** | METHOD-REGISTRY | Model Archive (8 Seed Models) |
| **AAA-AW** | CORE | 10C Fragen (WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, STAGE) |
| **BBB** | CORE | Parameter Repository (Literaturwerte) |
| **RRR** | METHOD-LIFETIME | Domain-spezifische α, β, λ, ρ Parameter (Step 3b) |
| **OOO** | FORMAL-SYSTEM | ODE-System für 7 Domains, Konvergenzanalyse |
| **BI** | DOMAIN-LIFESPAN | Intergenerationale Spillover-Matrix Γ^inter, CTWs |
| **BJ** | METHOD-DOMAINVAL | Cross-Cultural Validation, N_eff Spectrum |

**Konfigurationsdatei:** `data/lifespan-parameters.yaml` (Chapter 24 Integration)

---

## Checkliste: "Habe ich den EEE Workflow korrekt verwendet?"

```
☐ Mit Step 0 (Modus-Wahl) gestartet
☐ Mindestens einen der 4 Modi (SCHNELL, GEFÜHRT, TEMPLATE, CUSTOM) gewählt
☐ 3+1 Choice Architecture bei jedem Step eingehalten
☐ Alle notwendigen 10C Dimensionen (AAA-AW) beantwortet
☐ GGG Configurator für Defaults verwendet (nicht ad-hoc)
☐ FFF Registry für Seed-Modelle geprüft
☐ EIP-Trigger geprüft (TR1-TR5) bei jedem Step
☐ Neue Konzepte in concept-registry.yaml dokumentiert
☐ Model in FFF Registry registriert (Step 8)
☐ Output-Format gewählt und generiert (Step 9)
☐ Validation-Review geplant (12-Monats-Zyklus)
```

---

## Fehler vermeiden

❌ **Nicht:** Ad-hoc Fragen stellen (ohne EEE Struktur)
✅ **Stattdessen:** Immer mit Step 0 starten

❌ **Nicht:** Defaults selbst erfinden
✅ **Stattdessen:** GGG Mapping Tables verwenden

❌ **Nicht:** Modelle in Isolation designen
✅ **Stattdessen:** FFF Registry für ähnliche Modelle prüfen

❌ **Nicht:** Ohne Seed-Modell starten
✅ **Stattdessen:** TEMPLATE-Modus ausprobieren (schneller + validiert)

---

**Quellen:**
- Appendix EEE: METHOD-DESIGN (Workflow, System Prompts, Axiome)
- Appendix GGG: METHOD-CONFIG (Mapping Tables, Defaults)
- Appendix FFF: METHOD-REGISTRY (Seed Models, Validation)
- docs/frameworks/core-framework-definition.yaml (10C Definitionen)
