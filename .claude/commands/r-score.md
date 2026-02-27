# /r-score - LLMMC → R-Score Pipeline

Führe die vollständige LLMMC → R-Score Pipeline aus für GO/PILOT/NO-GO Entscheidungen.

Dies ist der **standardisierte Workflow** für Interventions-Priorisierung (Appendix III: METHOD-LLMMC).

## Verwendung

```
/r-score                    # Interaktiver Modus
/r-score --demo             # Demo mit Beispielparametern
/r-score --config <file>    # Config aus JSON-Datei
```

---

## Was die Pipeline macht

```
┌─────────────────────────────────────────────────────────────┐
│  LLMMC → R-SCORE PIPELINE                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. LLM Elicitation                                         │
│     → Strukturierte Abfragen für 6 α-Dimensionen            │
│     → Output: θ_llm, EU_llm für jede Dimension              │
│                                                             │
│  2. Scale-Local Calibration                                 │
│     → d/SMD: θ_true = 0.03 + 0.79 × θ_llm                   │
│     → pp:    pp_true = -0.48 + 1.007 × pp_llm               │
│                                                             │
│  3. Piecewise Linear Mapping                                │
│     → d → θ ∈ [0,1] via Knoten                              │
│     → pp → θ ∈ [0,1] via Knoten                             │
│                                                             │
│  4. R-Score Monte Carlo                                     │
│     → R(a,K) = Σαᵢ + γ·‖a‖·‖K‖                              │
│     → 50,000 Draws für Unsicherheitspropagation             │
│                                                             │
│  5. Decision                                                │
│     → P(R > T) < 5%   → NO-GO                               │
│     → P(R > T) 5-25%  → PILOT                               │
│     → P(R > T) ≥ 25%  → GO                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Die 6 α-Dimensionen

| Dim | Name | Frage | Skala |
|-----|------|-------|-------|
| α₁ | Phase-Fit | Wo in der Journey? | d |
| α₂ | Awareness-Fit | Welche Barriere? | d |
| α₃ | Dimension-Fit | Welcher Hebel? | pp |
| α₄ | Scale-Fit | Welche Ebene? | d |
| α₅ | Resource-Fit | Machbar? | d |
| α₆ | Context-Fit | Passt es hier? | d |

---

## Interaktiver Modus

Im interaktiven Modus werden Sie durch alle Parameter geführt:

### Schritt 1: α-Parameter eingeben

Für jeden der 6 Parameter:
- **Typ:** `d` (Cohen's d/SMD) oder `pp` (Prozentpunkte)
- **LLM-Schätzung:** Ihr Effekt-Schätzwert
- **Elicitation Uncertainty:** Unsicherheit der Schätzung

### Schritt 2: Komplementarität (γ)

- **γ LLM-Schätzung:** Wie stark verstärken sich die Maßnahmen?
- **γ Uncertainty:** Unsicherheit

### Schritt 3: Normen

- **‖a‖ (Design-Norm):** Stärke des Interventions-Designs
- **‖K‖ (Kontext-Norm):** Rezeptivität des Kontexts

### Schritt 4: Schwelle

- **T (Threshold):** Entscheidungs-Schwelle (Default: 6.0)

---

## Demo-Modus

```bash
cd scripts && python llmmc_to_rscore.py --demo
```

Zeigt einen vollständigen Durchlauf mit Beispielparametern:

```
📥 INPUTS
   n_α = 6 Parameter
   γ = 0.18 ± 0.10
   ‖a‖ = 2.15, ‖K‖ = 2.45
   Schwelle T = 5.0

📊 MAPPING RESULTS (v1)
   α = [0.68, 0.56, 0.62, 0.76, 0.36, 0.60]
   EU = [0.11, 0.10, 0.09, 0.09, 0.15, 0.11]
   Σα = 3.60 ± 0.27

📈 R-SCORE DISTRIBUTION
   E[R] = 4.55
   95% CI: [3.42, 5.68]
   P(R > 5.0) = 32.1%

🟢 DECISION: GO
```

---

## Config-Modus

Erstellen Sie eine JSON-Config-Datei:

```json
{
  "alpha_specs": [
    {"type": "d",  "llm_hat": 0.70, "eu_llm": 0.12, "name": "α_Phase"},
    {"type": "d",  "llm_hat": 0.55, "eu_llm": 0.10, "name": "α_Awareness"},
    {"type": "pp", "llm_hat": 25.0, "eu_llm": 6.0,  "name": "α_Dimension"},
    {"type": "d",  "llm_hat": 0.80, "eu_llm": 0.10, "name": "α_Scale"},
    {"type": "pp", "llm_hat": 10.0, "eu_llm": 5.0,  "name": "α_Resource"},
    {"type": "d",  "llm_hat": 0.60, "eu_llm": 0.11, "name": "α_Context"}
  ],
  "gamma_llm": 0.18,
  "gamma_eu": 0.10,
  "norm_a": 2.15,
  "norm_k": 2.45,
  "threshold": 6.0,
  "n_mc": 50000
}
```

Dann ausführen:

```bash
cd scripts && python llmmc_to_rscore.py --config ../path/to/config.json
```

---

## Kalibrations-Check

Vor der Verwendung können Sie die Kalibration prüfen:

```bash
# d/SMD Kalibration
cd scripts && python calibrate_d_smd.py

# PP Kalibration (mit 5-Point Checklist)
cd scripts && python calibrate_pp.py
```

**5-Point Deployment Checklist:**

| # | Check | Kriterium | Status |
|---|-------|-----------|--------|
| 1 | Support Coverage | pp_min ≤ 10, pp_max ≥ 60 | ✅ |
| 2 | Intercept Size | \|a\| < 5pp | ✅ |
| 3 | Slope | b ∈ [0.85, 1.05] | ✅ |
| 4 | LOO Coverage | ≥ 90% für 95%-CI | ✅ |
| 5 | Domain Robustness | Mean Residual < 10pp | ✅ |

---

## Entscheidungsregeln

| Bedingung | Entscheidung | Bedeutung |
|-----------|--------------|-----------|
| P(R > T) < 5% | 🔴 **NO-GO** | Intervention nicht empfohlen |
| P(R > T) 5-25% | 🟡 **PILOT** | Pilotprojekt empfohlen |
| P(R > T) ≥ 25% | 🟢 **GO** | Intervention empfohlen |

---

## Wichtige Konzepte

### Was α ist (und was nicht)

**α IST:**
- Ein kalibrierter **Fit-Parameter** (Intervention × Kontext)
- Empirisch verankert (Tier-1/2 Studien)
- Kontextspezifisch (ändert sich mit Ψ)

**α ist NICHT:**
- Ein Effekt (Effekte kommen aus RCTs)
- Ein Utility-Maß (Utility ist normativ)
- Eine Präferenz (Präferenzen sind subjektiv)

### Der Merksatz

> **"Effekte sagen, dass etwas wirkt. α sagt, wo und wann."**

### Die Trennung von α und U

```
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1 (α-Filter):                                        │
│    Ψ = Kontext-Diagnose                                     │
│    a = Interventions-Mechanismus                            │
│    α = Fit(a, Ψ) → Passt es?                                │
│                                                             │
│  STAGE 2 (U-Maximierung):                                   │
│    U = Utility-Funktion (unverändert!)                      │
│    Intervention entfernt Barriere, U bleibt konstant        │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementierung

| Datei | Zweck |
|-------|-------|
| `scripts/llmmc_to_rscore.py` | End-to-End Pipeline |
| `scripts/r_score.py` | R-Score Monte Carlo |
| `scripts/theta_mapping.py` | Piecewise Mapping |
| `scripts/calibrate_d_smd.py` | d/SMD Kalibration |
| `scripts/calibrate_pp.py` | PP Kalibration + 5-Point Check |

---

## Referenzen

- **Appendix III:** METHOD-LLMMC (diese Methodologie)
- **Appendix HHH:** METHOD-TOOLKIT (Intervention Design)
- **Dokumentation:** `docs/methods/alpha-definition.md`
- **Proof of Concept:** `docs/examples/green-energy-default-proof-of-concept.md`

---

## Beispiel: Green Energy Default

```
Kontext: Deutsche Haushalte, Stromversorger
Intervention: Green Energy Default (Opt-out statt Opt-in)
Effekt: 69pp (Ebeling & Lotz, 2015)

α-Analyse:
  α₁ Phase-Fit     = 0.95 (Trigger-Phase)
  α₂ Awareness-Fit = 0.85 (Status-quo Bias)
  α₃ Dimension-Fit = 0.98 (Default = perfekter Hebel)
  α₄ Scale-Fit     = 0.90 (Versorger-Ebene)
  α₅ Resource-Fit  = 0.92 (nur IT-Änderung)
  α₆ Context-Fit   = 0.88 (DACH-Akzeptanz)

  Σα = 5.48 (außergewöhnlich hoch)

R-Score:
  E[R] ≈ 5.7
  P(R > 5.0) ≈ 78%

  → Entscheidung: GO
```

---

**Quellen:**
- Appendix III: METHOD-LLMMC
- `scripts/llmmc_to_rscore.py`
- `docs/methods/alpha-definition.md`
