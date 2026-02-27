# Three-Layer Architecture Deviation Study

> **Research Design: LLM-Only vs. Layer-1 Computation**
> Version: 0.1 (Stufe 1 — Forschungsdesign)
> Date: 2026-02-16
> Status: DESIGN PHASE

---

## 1. Forschungsfrage

**Primäre Frage:**
Wie stark weichen LLM-generierte Parameterwerte (Layer 3) von formal berechneten Werten (Layer 1 + Layer 2) ab, und in welchen Kontexten ist die Deviation systematisch?

**Sekundäre Fragen:**
1. Ist die LLM-Deviation kontextabhängig? (Variiert sie über Ψ-Dimensionen?)
2. Gibt es systematische Bias-Muster? (Über-/Unterschätzung bestimmter Parameter?)
3. Wie stark verbessert jede Pipeline-Stufe die Genauigkeit?
4. Welche Parameter-Typen sind besonders anfällig für LLM-Halluzination?

---

## 2. Hypothesen

### H1: Systematische Deviation (Haupthypothese)
**H1:** LLM-Schätzungen weichen im Mittel ≥15% von Layer-1-berechneten Werten ab.

*Begründung:* Layer-3-Susceptibility = 0.8 (TLA-Axiom). LLMMC-Literatur zeigt θ_llm ≈ θ_true × 1.12 + noise (orchestrator.py bootstrap anchors).

### H2: Monotone Verbesserung über Pipeline-Stufen
**H2:** MAE(Layer 3) > MAE(Layer 2) > MAE(Layer 2+PCT) > MAE(Layer 2+PCT+LLMMC)

*Begründung:* Jede Pipeline-Stufe fügt Information hinzu (Registry → Context → Calibration).

### H3: Kontext-Abhängigkeit der Deviation
**H3:** Die LLM-Deviation ist bei kontextsensitiven Parametern (z.B. λ_R mit Ψ_S-Abhängigkeit) grösser als bei kontextfreien Parametern (z.B. β_present_bias).

*Begründung:* LLMs geben typischerweise «mittlere» Werte ohne Kontextanpassung zurück.

### H4: Domänen-Asymmetrie
**H4:** LLM-Deviation ist in «populären» Domänen (Finance, Health) kleiner als in spezialisierten Domänen (Antitrust, Digital Platforms).

*Begründung:* LLM-Trainingsdaten enthalten mehr populäre Domänen.

### H5: Uncertainty Miscalibration
**H5:** LLM-Konfidenzintervalle sind systematisch zu eng (Overconfidence) verglichen mit kalibrierten LLMMC-Intervallen.

*Begründung:* Bekanntes LLM-Phänomen; LLMMC korrigiert dies via Bayesian Shrinkage.

---

## 3. Experimentelles Design

### 3.1 Architektur: 4-Arm-Vergleich

```
                    QUERY BATTERY (N=100)
                           |
          +--------+-------+-------+--------+
          |        |               |        |
          v        v               v        v
       ARM 0    ARM 1           ARM 2    ARM 3
      Layer 3   Layer 2        Layer 2   Layer 2
      (LLM     (Registry      + PCT     + PCT
       only)    only)                    + LLMMC
          |        |               |        |
          v        v               v        v
      θ_LLM    θ_registry      θ_PCT    θ_full
          |        |               |        |
          +--------+-------+------+--------+
                           |
                     DEVIATION MATRIX
                     (Δ_01, Δ_02, Δ_03)
```

| Arm | Pipeline | Tier | Input | Output |
|-----|----------|------|-------|--------|
| **Arm 0** | LLM-Only (kein Tool-Aufruf) | — | Prompt: «Schätze Parameter X» | θ_LLM, CI_LLM |
| **Arm 1** | Layer 2 Only | Tier 2 | `parameter_api.get_parameter(id)` | θ_registry, CI_registry |
| **Arm 2** | Layer 2 + PCT | Tier 2 | `orchestrator.query(id, context, calibrate=False)` | θ_PCT, CI_PCT |
| **Arm 3** | Layer 2 + PCT + LLMMC | Tier 2.5/3 | `orchestrator.query(id, context, calibrate=True)` | θ_full, CI_full |

### 3.2 Ground Truth

Die Ground Truth kommt aus zwei Quellen:

| Quelle | N | Beschreibung | Unsicherheit |
|--------|---|--------------|--------------|
| **Tier 1** (Literatur) | ~15 | LLMMC CalibrationAnchors (Madrian & Shea, Goldstein et al., etc.) | SE bekannt |
| **Tier 2** (Registry) | ~119 | Parameter-Registry mit CI_95 aus Meta-Analysen | CI bekannt |

**Benchmark-Definition:**
- Für Arm 0 vs. Arm 1: Ground Truth = Tier-1/2 Literaturwert
- Für Arm 1 vs. Arm 2: Ground Truth = Tier-1/2 Literaturwert + Kontextanpassung
- Für Arm 2 vs. Arm 3: Ground Truth = LLMMC LOO Cross-Validation

### 3.3 Randomisierung

Die 100 Queries werden stratifiziert nach:

| Stratum | Kriterium | Anteil | N |
|---------|-----------|--------|---|
| **S1** | Kontextfrei (SIMPLE query) | 30% | 30 |
| **S2** | 1 Ψ-Dimension (CONTEXTUAL, 1D) | 25% | 25 |
| **S3** | 2-3 Ψ-Dimensionen (CONTEXTUAL, multi-D) | 25% | 25 |
| **S4** | Volle Pipeline mit LLMMC (CALIBRATED) | 20% | 20 |

Innerhalb jedes Stratums: Zufällige Auswahl aus verfügbaren Parametern × Kontexten.

---

## 4. Query Battery Design

### 4.1 Kategorien (10 × 10 Matrix)

Die Battery kombiniert **10 Parameter-Typen** × **10 Kontext-Variationen**:

**Parameter-Typen (Zeilen):**

| # | Typ | Beispiel-Parameter | Symbol | Registry ID |
|---|-----|-------------------|--------|-------------|
| P1 | Loss Aversion | Verlustaversion | λ | PAR-BEH-001 |
| P2 | Present Bias | Gegenwartspräferenz | β | PAR-BEH-003 |
| P3 | Crowding Out | Motivationsverdrängung | φ | PAR-BEH-002 |
| P4 | Social Norms | Normenstärke | σ_S | PAR-BEH-004 |
| P5 | Default Effect | Default-Compliance | α_D | PAR-BEH-005 |
| P6 | Anchoring | Ankereffekt | α_A | PAR-BEH-006 |
| P7 | Endowment | Besitztumseffekt | ε | PAR-BEH-007 |
| P8 | Fairness | Inequity Aversion | α_F | PAR-BEH-008 |
| P9 | Trust | Vertrauensparameter | τ | PAR-BEH-009 |
| P10 | Reciprocity | Reziprozitätsstärke | ρ_R | PAR-BEH-010 |

**Kontext-Variationen (Spalten):**

| # | Kontext | Ψ-Dimensionen | Beschreibung |
|---|---------|---------------|--------------|
| K1 | Kein Kontext | — | Nur Parameter-Name |
| K2 | Domäne | — | «...im Finanzbereich» |
| K3 | Ψ_S variiert | Social | «...mit Peers» vs. «...allein» |
| K4 | Ψ_I variiert | Institutional | «...mit Default» vs. «...ohne Default» |
| K5 | Ψ_C variiert | Cognitive | «...unter Zeitdruck» vs. «...entspannt» |
| K6 | Ψ_K variiert | Cultural | «...in der Schweiz» vs. «...in den USA» |
| K7 | Ψ_E variiert | Economic | «...bei Knappheit» vs. «...bei Überfluss» |
| K8 | Multi-Ψ (2D) | S + I | Social × Institutional |
| K9 | Multi-Ψ (3D) | S + I + C | Social × Institutional × Cognitive |
| K10 | Volle Kaskade | Alle 8 Ψ | MACRO → MESO → MICRO |

### 4.2 Prompt-Template für Arm 0 (LLM-Only)

```
Du bist ein Experte für Verhaltensökonomie.

Schätze den Parameter {PARAMETER_NAME} ({SYMBOL})
{KONTEXT_BESCHREIBUNG}

Gib an:
1. Punktschätzung (numerischer Wert)
2. 95% Konfidenzintervall [lower, upper]
3. Hauptquelle(n) für deine Schätzung

Format: JSON
{
  "estimate": <float>,
  "ci_95_lower": <float>,
  "ci_95_upper": <float>,
  "sources": ["<string>", ...],
  "reasoning": "<string>"
}
```

**Wichtig:** Arm 0 wird OHNE Zugriff auf Registry, PCT, oder LLMMC ausgeführt. Das LLM schätzt rein aus Trainings-Wissen.

### 4.3 Beispiel-Queries (Sample aus Battery)

| ID | Parameter | Kontext | Stratum | Erwartete Layer-1-Antwort |
|----|-----------|---------|---------|--------------------------|
| Q001 | λ (Loss Aversion) | Kein Kontext | S1 | 2.25 [1.5, 3.0] |
| Q002 | λ (Loss Aversion) | Finance, DACH | S1 | 2.40 [2.1, 2.7] |
| Q003 | λ (Loss Aversion) | Welfare + Stigma (Ψ_S high) | S2 | ~2.50 (PCT) |
| Q004 | λ (Loss Aversion) | Workplace + Peers (Ψ_S low) | S2 | ~2.22 (PCT) |
| Q005 | λ (Loss Aversion) | Welfare + Zeitdruck (Ψ_S + Ψ_T) | S3 | ~2.80 (PCT multi-D) |
| Q010 | β (Present Bias) | Kein Kontext | S1 | 0.70 [0.575, 0.825] |
| Q011 | β (Present Bias) | Health, Langzeitentscheidung | S2 | PCT-transformiert |
| Q020 | φ (Crowding) | Social + Financial kombiniert | S3 | γ = -0.68 (PAR-COMP-002) |
| Q050 | α_D (Default) | Opt-in vs. Opt-out | S2 | Madrian & Shea: 0.85 |
| Q080 | τ (Trust) | CH vs. DE vs. AT (Ψ_K) | S3 | BCM2-kalibriert |

---

## 5. Metriken (Dependent Variables)

### 5.1 Genauigkeitsmetriken

| Metrik | Formel | Interpretation |
|--------|--------|----------------|
| **MAE** | (1/N) Σ\|θ_arm - θ_true\| | Mittlerer absoluter Fehler |
| **MAPE** | (1/N) Σ\|θ_arm - θ_true\|/θ_true × 100 | Prozentualer Fehler |
| **RMSE** | √[(1/N) Σ(θ_arm - θ_true)²] | Root Mean Squared Error |
| **Bias** | (1/N) Σ(θ_arm - θ_true) | Systematische Über-/Unterschätzung |
| **Direction** | Sign(θ_arm - θ_true) | Bias-Richtung |

### 5.2 Kalibrierungsmetriken

| Metrik | Formel | Interpretation |
|--------|--------|----------------|
| **Coverage_95** | P(θ_true ∈ CI_95) | Soll ≈ 0.95 |
| **Coverage_68** | P(θ_true ∈ CI_68) | Soll ≈ 0.68 |
| **Sharpness** | Mittlere CI-Breite | Schmaler = besser (bei korrekter Coverage) |
| **Brier Score** | (p_arm - outcome)² | Für binäre Outcomes |

### 5.3 Ranking-Metriken

| Metrik | Formel | Interpretation |
|--------|--------|----------------|
| **Spearman ρ** | Rang-Korrelation | Relative Ordnung korrekt? |
| **Kendall τ** | Paarweise Konkordanz | Robuster als Spearman |
| **Top-K Precision** | Korrekte Top-K | Bei Ranking-Aufgaben |

### 5.4 Operational Metriken

| Metrik | Messung | Relevanz |
|--------|---------|----------|
| **Latenz** | elapsed_ms pro Query | Praxistauglichkeit |
| **Token-Kosten** | Input/Output Tokens × Preis | Wirtschaftlichkeit |
| **Provenance-Tiefe** | Anzahl belegter Pipeline-Steps | Nachvollziehbarkeit |

---

## 6. Analyse-Plan

### 6.1 Deskriptive Analyse

```
Für jeden Arm (0-3):
├── Verteilung der Deviations (Histogramm)
├── Mittlere MAE, MAPE, RMSE, Bias
├── Coverage-Analyse (Kalibrierungsplot)
└── Stratum-Aufschlüsselung (S1-S4)
```

### 6.2 Inferenzstatistik

| Test | Hypothese | Verfahren |
|------|-----------|-----------|
| H1 (Deviation > 15%) | MAPE(Arm 0) > 15% | One-sample t-test |
| H2 (Monotone Verbesserung) | MAE_0 > MAE_1 > MAE_2 > MAE_3 | Page's Trend Test |
| H3 (Kontext-Abhängigkeit) | Deviation(kontextsensitiv) > Deviation(kontextfrei) | Wilcoxon Rank-Sum |
| H4 (Domänen-Asymmetrie) | Deviation(populär) < Deviation(spezialisiert) | Kruskal-Wallis |
| H5 (Overconfidence) | Coverage(LLM) < 0.95 | Binomial Test |

### 6.3 Regressions-Analyse

```
Deviation_ij = β_0 + β_1 × Arm_j + β_2 × Stratum_i
             + β_3 × N_psi_dimensions + β_4 × Domain_popularity
             + β_5 × Parameter_type + ε_ij
```

**Dependent Variable:** |θ_arm - θ_true| (absolute Deviation)
**Clustering:** Standard Errors geclustert nach Parameter-ID

### 6.4 Effektstärken

Für jede Pipeline-Stufe die inkrementelle Verbesserung:

```
Δ_Layer2 = MAE(Arm 0) - MAE(Arm 1)     → Wert der Registry
Δ_PCT    = MAE(Arm 1) - MAE(Arm 2)     → Wert der Kontexttransformation
Δ_LLMMC  = MAE(Arm 2) - MAE(Arm 3)     → Wert der Kalibrierung
Δ_Total  = MAE(Arm 0) - MAE(Arm 3)     → Gesamtwert der Pipeline
```

---

## 7. Erwartete Ergebnisse (Priors)

Basierend auf der LLMMC-Bootstrap-Analyse (orchestrator.py) und TLA-Literatur:

| Arm | Erwarteter MAPE | Erwartete Coverage_95 | Begründung |
|-----|----------------|-----------------------|------------|
| Arm 0 (LLM-Only) | 15-25% | 60-75% (overconfident) | Susceptibility = 0.8 |
| Arm 1 (Registry) | 5-10% | 85-92% | Empirische Werte, aber kontextfrei |
| Arm 2 (Registry+PCT) | 3-8% | 88-95% | Kontextanpassung via Multiplikatoren |
| Arm 3 (Full Pipeline) | 2-5% | 90-96% | Bayesian Shrinkage + Kalibrierung |

**LLMMC-Akzeptanzkriterien (aus llmmc_calibration.py):**
- Acceptable: MAE < 0.12, RMSE < 0.15, Coverage 85-98%, ρ > 0.70
- Good: MAE < 0.08, RMSE < 0.10, Coverage 90-96%, ρ > 0.85

---

## 8. Limitationen (ex ante)

| Limitation | Mitigation |
|------------|------------|
| **Ground Truth Unsicherheit** | Tier-1 Anchors haben bekannte SE; berücksichtigen in Analyse |
| **LLM-Modell-Abhängigkeit** | Studie mit Claude Opus 4 durchführen; Replikation mit Sonnet |
| **Registry-Zirkularität** | Arm 0 (LLM-Only) hat KEINEN Zugriff auf Registry; strikt getrennt |
| **Kontextspezifikation** | Ψ-Labels standardisiert via pct-psi-scales.yaml |
| **Stichprobengrösse** | N=100 für Stufe 3; Power-Analyse zeigt Power > 0.80 bei d=0.5 |
| **Nicht-Unabhängigkeit** | Queries für denselben Parameter sind korreliert → Clustering |

---

## 9. Zeitplan & Skalierung

| Stufe | N Queries | Deliverables | Status |
|-------|-----------|--------------|--------|
| **Stufe 1** | 10 Beispiele | Dieses Forschungsdesign | ← AKTUELL |
| **Stufe 2** | 20 Queries | Python-Script + YAML-Battery + erste Ergebnisse | NEXT |
| **Stufe 3** | 100 Queries | Vollständige Analyse + LaTeX Appendix | PLANNED |

---

## 10. Output-Spezifikation

### 10.1 Daten-Output (YAML)

```yaml
# data/research/tla-deviation-results.yaml
study:
  id: "TLA-DEV-2026-001"
  version: "0.1"
  date: "2026-02-16"
  n_queries: 100

results:
  - query_id: "Q001"
    parameter_id: "PAR-BEH-001"
    symbol: "λ"
    context: null
    stratum: "S1"
    arm_0:
      estimate: 2.25          # LLM estimate
      ci_95: [1.8, 2.7]
      latency_ms: 1200
      tokens: 450
    arm_1:
      estimate: 2.25          # Registry
      ci_95: [1.5, 3.0]
      latency_ms: 12
      tier: 2
    arm_2:
      estimate: null           # No context → same as Arm 1
      ci_95: null
      latency_ms: null
    arm_3:
      estimate: null           # No calibration needed for S1
      ci_95: null
      latency_ms: null
    ground_truth:
      value: 2.25
      source: "Kahneman & Tversky 1979; Tversky & Kahneman 1992"
      se: 0.38
    deviations:
      d_01: 0.0               # |LLM - Registry|
      d_02: null
      d_03: null
```

### 10.2 Analyse-Output (Markdown/LaTeX)

```
outputs/research/TLA-DEV-2026-001/
├── F1_study_design.md          ← Dieses Dokument
├── F2_query_battery.yaml       ← 100 Queries (Stufe 3)
├── F3_raw_results.yaml         ← Rohdaten aller 4 Arme
├── F4_analysis_report.md       ← Statistische Analyse
├── F5_visualizations/          ← Plots (Histogramme, Kalibrierung)
│   ├── deviation_by_arm.png
│   ├── calibration_plot.png
│   ├── stratum_comparison.png
│   └── pipeline_improvement.png
└── F6_appendix_TLA_DEV.tex     ← LaTeX Appendix (Stufe 3)
```

---

## 11. Verbindung zum EBF Framework

### 11.1 Theoretische Einbettung

Diese Studie ist eine **empirische Validierung** von TLA Axiom 3 («Compute, Don't Hallucinate»):

| TLA-Axiom | Studie testet |
|-----------|---------------|
| **Axiom 1** (Susceptibility Ordering: 0.0 < 0.3 < 0.8) | H2 (Monotone Verbesserung) |
| **Axiom 2** (Formal Layer = Immune System) | H1 (Deviation > 15% ohne Layer 1) |
| **Axiom 3** (Compute, Don't Hallucinate) | Alle Hypothesen |
| **Axiom 4** (Parameters from Registry, Not Memory) | H1, H3 |

### 11.2 Appendix-Zuordnung

| Appendix | Verbindung |
|----------|------------|
| **METHOD-TLA** (Three-Layer Architecture) | Primärer theoretischer Rahmen |
| **CORE-WHERE (BBB)** | Parameter-Registry als Ground Truth |
| **METHOD-LLMMC (AN)** | LLMMC-Kalibrierung als Arm 3 |
| **CORE-WHEN (V)** | Ψ-Dimensionen als Kontext-Variablen |

### 11.3 Implikation für die Praxis

Wenn H1-H5 bestätigt werden:
1. **Layer 1 ist nicht optional** — sondern notwendig für <5% MAPE
2. **PCT liefert messbaren Mehrwert** — besonders bei Multi-Ψ-Kontexten
3. **LLMMC-Kalibrierung** korrigiert systematischen LLM-Bias
4. **Immune Gateway** ist gerechtfertigt als Pre-Response-Hook

---

## 12. Nächste Schritte

### Stufe 2 (Python Benchmark-Script)

```
1. benchmark_tla_deviation.py erstellen
   ├── Arm 0: LLM-Prompt generieren + Antwort parsen
   ├── Arm 1-3: orchestrator.query() mit verschiedenen Parametern
   ├── Deviation berechnen
   └── Ergebnisse in YAML speichern

2. query_battery.yaml erstellen
   ├── 20 repräsentative Queries
   ├── Stratifiziert nach S1-S4
   └── Mit erwarteten Ground-Truth-Werten

3. Erste Analyse ausführen
   ├── Deskriptive Statistik
   ├── Deviation-Histogramm
   └── Pipeline-Verbesserung quantifizieren
```

### Stufe 3 (Skalierung auf 100 Queries)

```
1. query_battery.yaml auf 100 Queries erweitern
2. Monte Carlo über LLM-Varianz (k=10 Wiederholungen pro Query)
3. Vollständige Inferenzstatistik
4. LaTeX Appendix (METHOD-TLADEV)
5. Visualisierungen
```

---

*Forschungsdesign erstellt: 2026-02-16*
*Nächster Schritt: Stufe 2 — Python Benchmark-Script*
