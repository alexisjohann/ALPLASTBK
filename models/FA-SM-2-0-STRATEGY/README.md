# FA-SM-2.0: FehrAdvice Strategy Model

> Meta-Modell fuer verhaltensbasiertes Organisationsdesign.
> Verknuepft Wertsteigerung, Verhalten und Kontext-Design formal.

## Ueberblick

```
LAYER 0: Welchen WERT schaffen?          V(t) — 6 Dimensionen
LAYER 1: Welches VERHALTEN erzeugt ihn?  B(t) — 4 Akteurgruppen
LAYER 2: Welcher KONTEXT erzeugt es?     Ψ(t) — 14 Dimensionen in 4 Tiers
LAYER 3: Welche STRUKTUR braucht es?     S    — 5 Dimensionen (→ org-design-layer.md)
```

**Kausalkette (bidirektional):**
- **Top-down:** V\*(t) → B\*(t) → Ψ\*(t) — «Was brauchen wir?»
- **Bottom-up:** Ψ(t) → B(t) → V(t) — «Was wird passieren?»
- **Feedback:** V(t) → ΔΨ(t+1) — «Erfolg veraendert Kontext»

## Was ist neu in 2.0?

| # | Innovation | Beschreibung |
|---|-----------|--------------|
| I1 | 6 Wertdimensionen | + Relational Capital (V_RC), + Adaptive Capacity (V_AC) |
| I2 | 4-Tier Kontext | 14 Dimensionen + Emergenz-α + dΨ/dt Dynamik |
| I3 | Geschichtetes γ | 4 Typen: Ψ×Ψ, B×Ψ, V×V, Cross-Level |
| I4 | Multi-Scale ODE | Micro (Tage), Meso (Monate), Macro (Jahre) |
| I5 | Kipppunkte | Regime-Switching bei Schwellenwert θ_tip |
| I6 | Netzwerkeffekte | Adjacency Matrix A — «Wer beeinflusst wen?» |
| I7 | Bayesian Hierarchical | Individuum → Team → Org → Branche Priors |
| I8 | 12 Predictions | 3 Ebenen mit Cascading Falsification |
| I9 | Design Gates | CEO-Test, Berater-Test, Falsifiability |
| I10 | **S×U×K Configuration** | Modellstruktur passt sich an Org-Kontext an |
| I11 | **Org-Design-Layer (S→V)** | 5 Strukturdimensionen, Produktionsfunktionen, S*-Optimierung |

## G0: Configuration Gate — S×U×K (NEU)

**Kernidee:** Nicht jedes Unternehmen braucht jede Komponente. Die Modellstruktur
selbst ist kontextabhaengig — genau wie die Parameter.

```
Traditionell:    Modell = fix,       θ = fix
EBF v1:          Modell = fix,       θ = f(Ψ, 10C)
FA-SM-2.0 + G0:  Modell = f(S,U,K),  θ = f(Ψ, 10C)
```

### Die 3 Meta-Dimensionen

| Dim | Name | Frage | Skala |
|-----|------|-------|-------|
| **S** | Groesse | Wie viele Mitarbeitende? | S1 (1-50) → S4 (1000+) |
| **U** | Unsicherheit | Wie vorhersehbar ist das Umfeld? | U1 (stabil) → U4 (chaotisch) |
| **K** | Komplexitaet | Wie viele interagierende Teile? | K1 (einfach) → K4 (sehr hoch) |

### 6 Konfigurationsprofile

| Profil | S×U×K | Aktive Komp. | Beispiel |
|--------|-------|-------------|----------|
| **LEAN** | S1/U1/K1 | 8 | Handwerksbetrieb |
| **AGILE** | S1/U3/K2 | 14 | Tech-Startup, Neon |
| **STRUCTURED** | S2/U2/K2 | 18 | Zindel, LUKB |
| **DYNAMIC** | S3/U3/K3 | 26 | ALPLA, PORR |
| **ENTERPRISE** | S4/U2/K4 | 30 | UBS, ZKB |
| **VUCA** | S4/U4/K4 | 34 | Post-Merger, Krise |

### Scoring: C = max(S, U, K)

Der HOECHSTE Wert bestimmt die Mindestkomplexitaet. Beispiel:
- Startup (S1) in chaotischem Markt (U4) → C=4 → nicht LEAN sondern AGILE/VUCA
- Grosskonzern (S4) in stabilem Umfeld (U1) → Override: STRUCTURED statt ENTERPRISE

### Aktivierungsmatrix (Auszug)

| Komponente | LEAN | AGILE | STRUCT | DYNAM | ENTER | VUCA |
|-----------|:----:|:-----:|:------:|:-----:|:-----:|:----:|
| V_WTP, V_WTS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| V_RE, V_IC | — | V_IC | ✅ | ✅ | ✅ | ✅ |
| V_RC, V_AC | — | — | — | ✅ | ✅ | ✅ |
| Context Tier 1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Context Tier 2 | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| Context Tier 3-4 | — | — | — | T3 | T3+4 | T3+4 |
| γ^ΨΨ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| γ^BΨ | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| γ^VV | — | — | — | ✅ | ✅ | ✅ |
| γ^cross | — | — | — | — | ✅ | ✅ |
| Tipping Points | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| Network Effects | — | — | — | ✅ | ✅ | ✅ |
| Regime-Switch | — | — | — | ✅ | — | ✅ |
| Bayesian Hier. | — | — | — | — | ✅ | ✅ |

### Zindel United: STRUCTURED (S2/U2/K2)

Komplexitaetsreduktion **~50%** gegenueber vollem FA-SM-2.0:
- 4 statt 6 Value-Dimensionen
- 2 statt 4 Context-Tiers
- 2 statt 4 γ-Typen
- Micro + Meso ODE (keine Macro)
- 8 statt 12 Predictions
- Keine Network Effects, kein Regime-Switching

Details: `examples/zindel-united/configuration.yaml`

## Wertdimensionen (Layer 0)

| Symbol | Name | Default w | Depreciation |
|--------|------|-----------|-------------|
| V_WTP | Customer Value (WTP) | 0.25 | 0.10-0.20/J |
| V_WTS | Talent Value (WTS) | 0.20 | 0.05-0.15/J |
| V_RE | Operative Verlaesslichkeit (ex V_OC) | 0.20 | 0.05-0.15/J |
| V_IC | Innovationskapital | 0.15 | 0.15-0.30/J |
| V_RC | Beziehungskapital (NEU) | 0.10 | 0.03-0.10/J |
| V_AC | Anpassungsfaehigkeit (NEU) | 0.10 | 0.10-0.25/J |

## Komplementaritaetsstruktur (4 Typen)

### γ^ΨΨ — Kontext × Kontext
| Paar | γ | Interpretation |
|------|---|----------------|
| INC × CUL | -0.35 | Crowding-Out: Geldanreize untergraben Kultur |
| GOV × INF | +0.25 | Governance + Information verstaerken sich |
| INF × CAP | +0.30 | Staerkste Komplementaritaet (Ichniowski) |
| CAP × CUL | +0.20 | Faehigkeiten in Kultur verankert = langlebiger |

### γ^BΨ — Verhalten × Kontext
| Paar | γ | Interpretation |
|------|---|----------------|
| Leadership × GOV | +0.25 | Fuehrung braucht Governance-Struktur |
| Middle Mgmt × INF | +0.20 | Manager skalieren mit Info-Qualitaet |
| Operations × INC | +0.15 | Frontline reagiert auf Anreize (⚠️ Crowding!) |

### γ^VV — Wert × Wert
| Paar | γ | Interpretation |
|------|---|----------------|
| RE × IC | +0.20 | Verlaesslichkeit ermoeglichen Innovation |
| WTP × WTS | -0.10 | Kurzfristiger Ressourcenkonflikt |
| RC × RE | +0.15 | Vertrauen foerdert Lernen (NEU) |
| AC × IC | +0.25 | Adaptivitaet + Innovation verstaerken sich (NEU) |

### γ^cross — Cross-Level (NEU)
| Triplet | γ | Interpretation |
|---------|---|----------------|
| V_RE moderiert B_M × INF | +0.10 | RE verstaerkt Manager-Info-Effekt |
| V_RC moderiert B_L × CUL | +0.12 | Vertrauen beschleunigt Kulturwandel |

## Multi-Scale ODE

```
MICRO  (Tage):   dB_jk/dt = β · U(Ψ) · B(1-B) · (1-R) · (1+M)
MESO   (Monate): dΨ^org/dt = μ·I + ν·B - ξ·Ψ + φ·ΔV
MACRO  (Jahre):  dV_k/dt = η·B·[1+Σγ·B_j] - δ·V + ε
```

## 12 Predictions

| # | Ebene | Vorhersage | Horizont |
|---|-------|------------|----------|
| P1 | Micro | Leadership-Adoption β_L ∈ [0.05, 0.15] | 3-6 Mo |
| P2 | Micro | Crowding-Out bei INC↑ ohne CUL | 6-12 Mo |
| P3 | Micro | Netzwerk-Diffusion (Conditional Cooperators) | 3-9 Mo |
| P4 | Micro | R sinkt mit INF-Transparenz | 1-6 Mo |
| P5 | Meso | Tipping Point bei ~60% Adoption | 6-18 Mo |
| P6 | Meso | CUL aendert sich 3-5× langsamer als INF | 12-36 Mo |
| P7 | Meso | Cluster-Adoption (Ichniowski-Effekt) | 6-12 Mo |
| P8 | Meso | Cross-Level γ^cross sichtbar | 12-24 Mo |
| P9 | Macro | V_RE akkumuliert mit η, depreziert mit δ | 2-5 J |
| P10 | Macro | V_IC depreziert 2-3× schneller als V_RE | 1-3 J |
| P11 | Macro | Hoehere γ → hoeherer Steady-State V* | 3-7 J |
| P12 | Macro | V→Ψ Feedback messbar | 2-5 J |

**Cascading Falsification:** Micro scheitert → Meso fragwuerdig → Macro ungueltig.

## Design Gates (G0-G3)

| Gate | Frage | Kriterium |
|------|-------|-----------|
| **G0-CONFIG** | Welche Komponenten braucht diese Org? | S×U×K → Profil → Aktivierungsmatrix |
| G1-CEO | Kann ein CEO damit entscheiden? | Konkrete Empfehlungen, klare Prioritaeten |
| G2-BERATER | Kann ein Berater es in 15 Min erklaeren? | Kausalkette in 3 Saetzen |
| G3-FALSIFIABILITY | Kann das Modell scheitern? | ≥4 Micro-Predictions mit Intervallen |

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `model-definition.yaml` | Formale SSOT (vollstaendige Modelldefinition) |
| `org-design-layer.md` | **Org-Design-Layer: S→V** (Strukturdimensionen, Produktionsfunktionen, S*) |
| `README.md` | Diese Dokumentation |
| `predictions/` | Prediction Cards (nach Erstanwendung) |
| `examples/zindel-united/configuration.yaml` | **Zindel STRUCTURED-Profil** (S2/U2/K2) |

## Theoretische Grundlagen

- Van den Steen (2017): Formale Strategiedefinition
- Ichniowski et al. (1997): HRM-Cluster Komplementaritaet (+6.7%)
- Bloom/Sadun/Van Reenen (2012): Management Practices
- Oberholzer-Gee (2021): WTP-WTS Value Framework
- Bandiera et al. (2020): CEO-Verhaltenstypen
- Heckman (2007): Dynamische Komplementaritaet
- Teece (2007): Dynamic Capabilities (V_AC)
- Granovetter (1985): Einbettung oekonomischen Handelns (V_RC)

## Status

- **Version:** 2.1 (11 Innovationen I1-I11)
- **Status:** EXPERIMENTAL
- **Erstanwendung:** Zindel United (ZIN005) — Profil STRUCTURED
- **Supersedes:** FA-SM-2.0
- **Neu in 2.1:** Org-Design-Layer (S→V), V_OC umbenannt zu V_RE, V_WTP-Ableitung
- **Naechster Schritt:** β-Kalibrierung (Bloom/Van Reenen, Ichniowski), empirische Validierung bei Zindel
