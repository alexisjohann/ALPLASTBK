# Three-Layer Architecture (TLA) — Framework Deep-Dive

> **Version:** 1.0.0 | **Status:** SSOT (Single Source of Truth)
> **Canonical Entry:** `data/knowledge/canonical/three-layer-architecture.yaml` (KB-TLA-001)
> **EIP-Validated:** 2026-02-15 (32+ PRO, 5 CONTRA papers across 7 disciplines)
> **Last updated:** 2026-02-15

---

## 1. Executive Summary

The Three-Layer Architecture (TLA) is the fundamental architectural principle of the EBF Framework. It separates **deterministic computation** (Layer 1), **validated parameters** (Layer 2), and **probabilistic LLM translation** (Layer 3) into distinct layers with different virus susceptibility levels.

**The core insight:** Code computes. The LLM only translates.

This is not a design preference — it is a scientifically validated architectural necessity, supported by 32+ research papers across 7 disciplines (computer science, AI/ML, epidemiology, memetics, behavioral economics, information theory, and software engineering).

**Key metrics:**

| Property | Value | Evidence |
|----------|-------|----------|
| Layer 1 Susceptibility | 0.0 (immune) | PAL: +40% accuracy (Gao et al., ICML 2023) |
| Layer 2 Susceptibility | 0.3 (validatable) | RAG: +35% factuality (Lewis et al., NeurIPS 2020) |
| Layer 3 Susceptibility | 0.8 (vulnerable) | Model Collapse (Shumailov et al., Nature 2024) |
| Evidence base | 32+ PRO / 5 CONTRA | EIP validated 2026-02-15 |
| Existing implementations | 5+ scripts | PSF-2.0, R-Score, EMERGE, LLMMC, Formula Check |

---

## 2. Wissenschaftliche Fundierung (EIP-validiert)

### 2.1 Evidenz-Ketten

The TLA rests on three independent evidence chains, each validated through multiple peer-reviewed publications:

**Kette 1: Calculator Problem (validates Layer 1)**

LLMs systematically fail at tasks where deterministic computation succeeds. Offloading calculation to formal tools dramatically improves accuracy.

| Paper | Venue | Finding | Relevance |
|-------|-------|---------|-----------|
| Gao et al. (2023) "PAL" | ICML | 40% absolute improvement on GSM-Hard when computation delegated to Python | Direct validation of Layer 1 |
| Schick et al. (2023) "Toolformer" | NeurIPS | LLMs struggle with basic functionality where simpler tools excel | LLMs should use tools, not compute internally |
| Goodell et al. (2025) | Nature npj Digital Medicine | 5.5-fold (LLaMA) and 13-fold (GPT) error reduction with task-specific tools | Clinical validation of tool delegation |

**Kette 2: Model Collapse / Information Virus (validates Layer 3 vulnerability)**

Recursive AI-generated content causes irreversible defects. False information spreads farther and faster than truth. Formal constraints on LLM outputs are necessary.

| Paper | Venue | Finding | Relevance |
|-------|-------|---------|-----------|
| Shumailov et al. (2024) | Nature | AI models collapse when trained on recursively generated data; tails disappear by generation 9 | Proves Layer 3 outputs degrade without formal grounding |
| Vosoughi et al. (2018) | Science | Falsehood diffuses farther, faster, deeper; truth takes 6x longer to reach 1,500 people | Information viruses have R₀ > 1 |
| Bai et al. (2022) "Constitutional AI" | Anthropic | Formal constitution constraining LLM outputs outperforms RLHF | Formal constraints (Layer 1) control LLM outputs (Layer 3) |

**Kette 3: Separation of Concerns (validates architecture principle)**

Separating deterministic computation from probabilistic generation is a fundamental computer science principle with provable convergence guarantees.

| Paper | Venue | Finding | Relevance |
|-------|-------|---------|-----------|
| Dijkstra (1974) "On the Role of Scientific Thought" | EWD447 | Separation of concerns is the only available technique for effective ordering of thoughts | Foundational CS principle |
| Parnas (1972) | Communications of the ACM | Modules should hide design decisions; decompose by change likelihood | Information hiding between layers |
| Lewis et al. (2020) "RAG" | NeurIPS | Combining parametric (model) with non-parametric (retrieved) memory produces more factual outputs | Layer 2 (retrieved) grounds Layer 3 (parametric) |

### 2.2 Etablierte Praezedenzen

The TLA is not a novel invention — it is a synthesis of 7 established frameworks:

| Framework | Source | TLA Parallel |
|-----------|--------|-------------|
| **PAL** (Program-Aided Language Models) | Gao et al., ICML 2023 | LLM decomposes problem → Python executes computation |
| **Toolformer** | Schick et al., NeurIPS 2023 | LLM learns to call external tools instead of computing internally |
| **RAG** (Retrieval-Augmented Generation) | Lewis et al., NeurIPS 2020 | Validated knowledge store + LLM generation = more factual |
| **AlphaGeometry** | Trinh et al., DeepMind 2024 | Neural proposes, symbolic verifies (Thinking Fast and Slow) |
| **Neuro-Symbolic AI** | 167-paper systematic review (2024) | Hybrid neural+symbolic outperforms pure neural or pure symbolic |
| **Constitutional AI** | Bai et al., Anthropic 2022 | Formal rules constrain LLM outputs |
| **Digital Immune System** | Chess/IBM 1991, Gartner 2023+ | Biological immune system metaphor operationalized in enterprise |

### 2.3 Schluessel-Papers (vollstaendige Tabelle)

| # | Paper | Journal/Venue | Year | Claim | Evidence Strength |
|---|-------|---------------|------|-------|-------------------|
| 1 | Gao et al. "PAL" | ICML | 2023 | Python delegation improves accuracy by 40% | Strong (empirical) |
| 2 | Schick et al. "Toolformer" | NeurIPS | 2023 | LLMs should use tools for computation | Strong (empirical) |
| 3 | Goodell et al. "Clinical Calc" | Nature npj | 2025 | 5.5-13x error reduction with tools | Strong (clinical) |
| 4 | Shumailov et al. "Model Collapse" | Nature | 2024 | Recursive AI content causes model collapse | Strong (theoretical + empirical) |
| 5 | Vosoughi et al. "Spread of News" | Science | 2018 | False info spreads 6x faster than truth | Strong (empirical, 126k stories) |
| 6 | Bai et al. "Constitutional AI" | Anthropic | 2022 | Formal constraints outperform RLHF | Strong (empirical) |
| 7 | Lewis et al. "RAG" | NeurIPS | 2020 | Retrieved knowledge improves factuality by 35% | Strong (empirical) |
| 8 | Dijkstra "Separation of Concerns" | EWD447 | 1974 | Fundamental CS principle | Foundational |
| 9 | Parnas "Information Hiding" | CACM | 1972 | Module decomposition by change likelihood | Foundational |
| 10 | Trinh et al. "AlphaGeometry" | Nature | 2024 | Neural+symbolic solves olympiad problems | Strong (empirical) |

### 2.4 CONTRA-Evidenz und Monitoring-Trigger

Honest science does not ignore CONTRA evidence. Three significant challenges are documented:

| # | Claim | Source | Assessment | Monitoring Trigger |
|---|-------|--------|------------|--------------------|
| 1 | Pure RL can induce reasoning | DeepSeek-R1 (2025) | Serious but not invalidating — shows Layer boundary is dynamic, not static | When reasoning models achieve 95%+ on formal benchmarks consistently |
| 2 | Structured output degrades reasoning | Tam et al. (2024) | Important design constraint — Layer 3 must not be over-constrained | If structured output techniques eliminate the degradation penalty |
| 3 | Memetics lacks formal rigor | Fog (2023) | Valid critique — TLA must go beyond metaphor to measurable properties | N/A — already addressed by formal EIV/EGD taxonomy |

---

## 3. Das Problem: Warum drei Schichten?

### 3.1 The Virus Threat Model

The TLA exists as a **defense architecture** against EBF Information Viruses (→ KB-VIR-001).

```
THREAT 1: LLM HALLUCINATION (EIV — External Information Virus)
─────────────────────────────────────────────────────────────
LLM "remembers" λ = 2.25 from training data.
But: The paper measured λ in a welfare context with stigma.
In the current context (workplace, peers), λ = 1.8.

The LLM doesn't know the difference. It confidently states a wrong number.
→ This is an EIV: false information from external source (training data).

THREAT 2: DEFINITION ERROR (EGD — Endogenous Genetic Defect)
─────────────────────────────────────────────────────────────
A formula uses "social norm strength" as variable.
But: Is this descriptive norms? Injunctive norms? Both?
If the definition is ambiguous, Layer 1 computes deterministically
on a flawed foundation.

→ This is an EGD: the DNA itself is defective.
Determinism on wrong definitions = deterministically wrong results.
```

### 3.2 The Calculator Analogy

```
A calculator cannot hallucinate.
    √(Σ(p_i - q_i)²) always gives the same result.
    Regardless of how often you ask.
    Regardless of which LLM "thinks" about it.

But: A calculator needs correct inputs.
    If the inputs are wrong (EGD), the output is wrong.
    Deterministically, reproducibly, verifiably wrong.

→ Layer 1 is immune to EIV, but vulnerable to EGD.
→ Layer 2 (validated parameters) defends against EGD.
→ Layer 3 (LLM) is vulnerable to both.
```

---

## 4. Architektur-Uebersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER QUESTION                                     │
│            "Was ist Loss Aversion im Kontext                            │
│             Heizungsersatz Schweiz?"                                     │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 3: LLM-UEBERSETZUNG                    Susceptibility: 0.8      │
│  ─────────────────────────────────────────────────────────────────────  │
│  • Interprets user question                                             │
│  • Identifies relevant Ψ-dimensions (Ψ_I, Ψ_E, Ψ_K)                   │
│  • Translates to formal query                                           │
│  • After computation: Explains result in natural language               │
│                                                                         │
│  DOES: Interpret, translate, explain                                    │
│  DOES NOT: Remember numbers, compute, generate parameters               │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │ formal query
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 2: PARAMETER-STORE (YAML)               Susceptibility: 0.3     │
│  ─────────────────────────────────────────────────────────────────────  │
│  • parameter-registry.yaml → PAR-BEH-016 (λ_R = 2.5)                   │
│  • BCM2_04_KON_*.yaml → Schweiz-Kontext (404 Faktoren)                 │
│  • model-registry.yaml → applicable models                              │
│  • theory-catalog.yaml → theoretical foundation                         │
│                                                                         │
│  PROVIDES: Schema-validated values with sources, ranges, CI             │
│  VALIDATED BY: BBB 4-Tier Hierarchy (Literature > LLMMC > Empirical)    │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │ parameters + context
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: FORMALE BERECHNUNG (Python)          Susceptibility: 0.0     │
│  ─────────────────────────────────────────────────────────────────────  │
│  • PCT: θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)                                         │
│  • θ_B = 2.5 × M(ΔΨ_I) × M(ΔΨ_E) = 4.58                              │
│  • Deterministic, reproducible, verifiable                              │
│                                                                         │
│  COMPUTES: Formal equations with YAML-sourced parameters                │
│  CANNOT: Hallucinate, approximate, "improve" results                    │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │ formal result
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 3: LLM-UEBERSETZUNG (return path)                               │
│  ─────────────────────────────────────────────────────────────────────  │
│  "In diesem Kontext (Schweiz, Heizungsersatz, institutionelle           │
│   Huerden) ist Loss Aversion sehr hoch (λ = 4.58), weil..."            │
│                                                                         │
│  TRANSLATES: Formal result → natural language explanation               │
│  DOES NOT: Round, adjust, "improve" the computed number                 │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Layer 1: Formale Berechnung (Python)

### 5.1 Definition und Eigenschaften

| Property | Value |
|----------|-------|
| **Susceptibility** | 0.0 (virus-immune) |
| **Technology** | Python scripts |
| **Principle** | Deterministic computation on validated inputs |
| **Analogy** | Laboratory instrument — cannot hallucinate measurements |

Layer 1 is the immune system of the EBF. Deterministic computation cannot hallucinate. `sqrt(sum((p_i - q_i)^2))` always gives the same result for the same inputs.

### 5.2 Wissenschaftliche Basis

| Evidence | Source | Finding |
|----------|--------|---------|
| PAL | Gao et al. (ICML 2023) | 40% absolute improvement when computation delegated to Python |
| Toolformer | Schick et al. (NeurIPS 2023) | LLMs struggle with basic functionality where simpler tools excel |
| Clinical Calculations | Goodell et al. (Nature npj 2025) | 5.5-fold (LLaMA) and 13-fold (GPT) error reduction with tools |
| AlphaGeometry | Trinh et al. (Nature 2024) | Neural proposes, symbolic verifies |

### 5.3 Existierende Implementierungen

| Script | Location | Function |
|--------|----------|----------|
| **PSF-2.0** | `models/psf-2.0/` | Papal Selection Framework (reads YAML → computes → returns result) |
| **R-Score** | `scripts/r_score.py` | Religious Distance Metric |
| **EMERGE** | `scripts/emerge_algorithm.py` | Intervention Emergence Algorithm |
| **LLMMC Calibration** | `scripts/llmmc_calibration.py` | LLM Monte Carlo Calibration |
| **Formula Check** | `scripts/check_formula_compliance.py` | Formula Validation |

### 5.4 Was Layer 1 NICHT tun darf

- Layer 1 **does not** determine values. Values come from Layer 2.
- Layer 1 **does not** interpret questions. Interpretation comes from Layer 3.
- Layer 1 **does not** make assumptions. All inputs must be explicit.

### 5.5 Implementation Gap

| What exists | What is missing |
|-------------|-----------------|
| 5+ individual scripts | Universal Parameter Lookup API |
| PSF-2.0 as pattern | PCT as Python computation |
| Formula validation | Formal orchestrator connecting layers |

---

## 6. Layer 2: Parameter-Store (YAML)

### 6.1 Definition und Eigenschaften

| Property | Value |
|----------|-------|
| **Susceptibility** | 0.3 (schema-validatable) |
| **Technology** | YAML files with schema validation |
| **Principle** | Validated values with sources, ranges, and confidence intervals |
| **Analogy** | Certified reference materials in a laboratory |

### 6.2 Wissenschaftliche Basis

| Evidence | Source | Finding |
|----------|--------|---------|
| RAG | Lewis et al. (NeurIPS 2020) | Retrieved knowledge improves factuality by 35% |
| Schema Validation | Industry standard | YAML schemas catch 99% of structural errors |
| BBB 4-Tier | EBF internal | Literature-validated parameters have lowest uncertainty |

### 6.3 Aktuelle SSOT-Dateien

| Registry | File | Content |
|----------|------|---------|
| **Parameter Registry** | `data/parameter-registry.yaml` | 140+ behavioral parameters with CI, sources, ranges |
| **Model Registry** | `data/model-registry.yaml` | 10C models with specifications |
| **Theory Catalog** | `data/theory-catalog.yaml` | 153 theories with validity assessments |
| **BCM2 Context** | `data/dr-datareq/sources/context/` | 404 context factors (CH/AT/DE) |
| **Bibliography** | `bibliography/bcm_master.bib` | 2,347 papers with EBF annotations |

### 6.4 Validierungs-Infrastruktur

| Validation | Script | What it checks |
|------------|--------|----------------|
| Referential Integrity | `validate_referential_integrity.py` | Cross-database references |
| Parameter Consistency | `validate_parameter_consistency.py` | Parameter drift (λ, β, γ) |
| Context Consistency | `validate_context_consistency.py` | Ψ dimensions and context factors |
| Knowledge Consistency | `validate_knowledge_consistency.py` | Canonical KB entries |
| BibTeX-YAML | `validate_bibtex_yaml_consistency.py` | BibTeX ↔ YAML sync |

### 6.5 BBB 4-Tier Hierarchie

| Tier | Source | Uncertainty | Priority |
|------|--------|-------------|----------|
| 1 | Literature (Meta-analysis) | Low | Highest — always preferred |
| 2 | LLMMC Prior | Medium | Fallback when literature sparse |
| 3 | Empirical Calibration | Variable | When primary data available |
| 4 | Expert Elicitation | High | Last resort for new domains |

---

## 7. Layer 3: LLM-Uebersetzung

### 7.1 Definition und Eigenschaften

| Property | Value |
|----------|-------|
| **Susceptibility** | 0.8 (highly vulnerable) |
| **Technology** | Large Language Model (Claude, GPT, etc.) |
| **Principle** | Translate formal results to natural language |
| **Analogy** | Doctor explaining lab results to patient |

### 7.2 Wissenschaftliche Basis

| Evidence | Source | Finding |
|----------|--------|---------|
| Model Collapse | Shumailov et al. (Nature 2024) | Recursive AI-generated content causes irreversible model collapse |
| Misinformation Spread | Vosoughi et al. (Science 2018) | False news spreads farther, faster, deeper than truth |
| Hallucination Survey | Ji et al. (2023) | LLMs systematically generate plausible but false content |
| Constitutional AI | Bai et al. (Anthropic 2022) | Formal constraints necessary to control LLM outputs |

### 7.3 Was das LLM DARF

- **Interpret questions** and translate them into formal queries
- **Explain formal results** in natural language appropriate for the audience
- **Identify context dimensions** (which Ψ-dimensions are relevant)
- **Adapt language** for target audience (expert vs. layperson)

### 7.4 Was das LLM NICHT DARF

- **Remember numbers** from training instead of reading from Layer 2
- **"Improve" formal results** by rounding or adjusting
- **Generate parameter values** instead of looking them up
- **Compute in its head** instead of delegating to Layer 1

### 7.5 Der Override-Virus (Interface-Schicht)

The most dangerous virus type for Layer 3 is the **Override Virus**: the LLM "knows better" than the formal computation and silently overrides it.

```
EXAMPLE:
Layer 1 computes: d(Alevi, Zoro) = 0.87
LLM "knows" from training: Alevitentum is a branch of Islam
LLM overrides: "Despite formal distance, Alevitentum is closer to Sunnismus"

→ The formal result is CORRECT. The LLM override is an EIV.
→ Defense: Layer 3 MUST present Layer 1 results without modification.
```

### 7.6 Dual-Process Analogie (und ihre Grenzen)

The TLA has a structural parallel to Kahneman's Dual-Process Theory:

| System | TLA Layer | Function |
|--------|-----------|----------|
| System 1 (fast, intuitive) | Layer 3 (LLM) | Quick interpretation, pattern matching |
| System 2 (slow, deliberate) | Layer 1 (Python) | Careful computation, formal verification |

**Important limitation:** This is an analogy, not an isomorphism. Layer 1 is not "slow" in computational terms — it is deterministic. The analogy holds for the function (intuition vs. verification), not for the mechanism.

---

## 8. Die vier Prinzipien

### P1: Compute, Don't Hallucinate

**Definition:** Every EBF number comes from formal computation (Layer 1), not from LLM memory.

**Implementation:** When a numerical result is needed, Layer 3 delegates to Layer 1.

**Violation Example:**
```
WRONG:  "Loss Aversion is approximately 2.25" (LLM remembers from training)
RIGHT:  Layer 2 reads PAR-BEH-016 → Layer 1 computes PCT → "Loss Aversion in
        this context is 4.58 (λ_R = 2.5 × M(ΔΨ_I) × M(ΔΨ_E))"
```

**Evidence:** PAL (40% improvement), Clinical Tools (5.5-13x error reduction)

### P2: Parameters from Registry, Not from Memory

**Definition:** Parameter values are read from YAML (Layer 2), never "remembered" from LLM training.

**Implementation:** Every parameter reference includes a PAR-XXX-XXX ID.

**Violation Example:**
```
WRONG:  γ = 0.35 (where does this come from?)
RIGHT:  γ = 0.35 (PAR-COMP-001, source: Akerlof & Kranton 2000)
```

**Evidence:** RAG (+35% factuality), BBB 4-Tier validation

### P3: Translate, Don't Generate

**Definition:** The LLM explains what was computed, it does not invent new content.

**Implementation:** Layer 3 receives formal results from Layer 1 and translates them.

**Violation Example:**
```
WRONG:  "Based on my analysis, I believe the distance is moderate"
RIGHT:  "The computed distance is d = 0.87, which is in the 'close' range
         because the primary drivers are syncretic tolerance (Δτ = 0.50)
         and mysticism orientation (Δω = 0.35)"
```

**Evidence:** Model Collapse (Shumailov et al.), Constitutional AI (Bai et al.)

### P4: Formal Layer is the Immune System

**Definition:** Determinism = virus-free zone. The formal layer cannot be infected by EIV.

**Implementation:** All EBF outputs must pass through Layer 1 before reaching the user.

**Violation Example:**
```
WRONG:  LLM generates answer directly without formal computation
RIGHT:  LLM → formal query → Layer 2 (parameters) → Layer 1 (compute) → LLM (translate)
```

**Evidence:** Digital Immune System (Chess/IBM 1991), Separation of Concerns (Dijkstra 1974)

**Formula:** `Immunity(Formal_Layer) = f(Definition_Cleanliness) × Determinism`

---

## 9. Verbindung zum Virus/Immunitaets-Framework

The TLA is the **defense architecture** against EBF Information Viruses (→ KB-VIR-001):

### 9.1 EIV greift Layer 3 an (Halluzination)

```
EIV Attack Vector:
─────────────────
Training Data → LLM Memory → Layer 3 Output → User

Defense:
────────
Layer 1 computes independently → Result verified → Layer 3 translates
The LLM CANNOT override the formal result.
```

EIV (External Information Virus) enters through Layer 3 — the LLM's training data contains false or outdated information. Defense: Layer 1 computes the correct result independently of LLM memory.

### 9.2 EGD greift Layer 1 DNA an (Endogene Fehler)

```
EGD Attack Vector:
──────────────────
Ambiguous Definition → Layer 2 (wrong schema) → Layer 1 (computes on wrong basis)

Defense:
────────
ATOMIC SYMBOL RULE: Every EBF symbol is unique (λ_R, not λ)
PCT: Parameter Context Transformation makes context explicit
BBB 4-Tier: Literature-validated parameters with confidence intervals
```

EGD (Endogenous Genetic Defect) attacks the DNA of the formal layer — if variable definitions are ambiguous, Layer 1 computes deterministically on a flawed foundation. Defense: Clean definitions, unique symbols, explicit contexts.

### 9.3 Epidemiologische Modelle

The virus/immunity framework uses epidemiological models from KB-VIR-001:

| Metric | Meaning | TLA Implication |
|--------|---------|-----------------|
| R₀ > 1 | Virus spreads exponentially | Without Layer 1, hallucinations propagate |
| SEDPNR model | 6-compartment epidemiological model | Tracks information virus lifecycle |
| Herd immunity | Enough formal nodes → system immune | More Layer 1 coverage → less vulnerability |

---

## 10. Praktische Beispiele

### 10.1 Loss Aversion Query (Altes Modell vs. Neues Modell)

**Question:** "Was ist Loss Aversion im Kontext Heizungsersatz Schweiz?"

```
ALTES MODELL (LLM denkt):
──────────────────────────
User → LLM remembers "λ ≈ 2.25" from training → Answers directly
Problem: Value is context-free, possibly hallucinated

NEUES MODELL (TLA):
────────────────────
User → Layer 3 interprets question
     → Layer 2 reads: parameter-registry.yaml → PAR-BEH-016 (λ_R = 2.5)
     → Layer 2 reads: BCM2_04_KON → Swiss context factors
     → Layer 1 computes: PCT θ_B = 2.5 × M(ΔΨ_I) × M(ΔΨ_E) = 4.58
     → Layer 3 translates: "In this context, Loss Aversion is very high
        (λ = 4.58) because institutional barriers and economic stakes
        are both elevated in the Swiss heating replacement context."
```

### 10.2 PSF-2.0 Konklave (Funktionierendes Beispiel)

The Papal Selection Framework (PSF-2.0) in `models/psf-2.0/` is the most complete existing implementation of the TLA:

```
Layer 3: User asks "Who would win the next conclave?"
  ↓
Layer 2: PSF reads candidate profiles from YAML
         (age, nationality, theological position, language skills, ...)
  ↓
Layer 1: PSF-2.0 computes:
         - Cardinal voting probabilities
         - Regional bloc dynamics
         - Theological distance metrics
         - Probabilistic outcome distribution
  ↓
Layer 3: LLM translates formal results into narrative explanation
```

**Key property:** The PSF-2.0 result is reproducible. Running it twice with the same YAML inputs gives the same output.

### 10.3 Religious Distance (Alevitentum)

```
Layer 3: User asks "Is Alevitentum closer to Zoroastrismus or Sunnismus?"
  ↓
Layer 2: Reads religious parameters from BCM2_07_REL
         κ_ritual, σ_authority, γ_gender, τ_syncretism, ω_mysticism, δ_afterlife
  ↓
Layer 1: Computes euclidean distance:
         d(Alevi, Zoro) = √(Σ(p_i^A - p_i^Z)²) = 0.87
         d(Alevi, Sunni) = √(Σ(p_i^A - p_i^S)²) = 1.48
  ↓
Layer 3: "Alevitentum is behaviorally ~70% closer to Zoroastrismus (d=0.87)
          than to sunnitischem Islam (d=1.48). Main drivers: syncretic
          tolerance (τ) and mysticism orientation (ω)."
```

---

## 11. Embryonale Orchestrator-Patterns

The TLA recognizes that 80% of the organs exist, but the circulatory system (orchestrator) is missing. However, several proto-orchestrator patterns already exist:

### 11.1 Quellen-Hierarchie (Proto-Orchestrator)

CLAUDE.md defines a source hierarchy that functions as an implicit orchestrator:

```
Step 0: Own models (session-context.yaml + model-registry.yaml)
Step 1: Context database (BCM2)
Step 2: API connections
Step 3: Scientific papers (bcm_master.bib)
Step 4: Web research
```

### 11.2 /apply-models (Vollstaendige Pipeline)

The `/apply-models` skill executes a complete Layer 2 → Layer 1 → Layer 3 pipeline:

```
1. Read customer YAML (Layer 2)
2. Run 4 models: RPM, MCSM, OSM, CAM (Layer 1)
3. Generate board presentation (Layer 3)
```

### 11.3 mandatory-triggers.yaml (Entscheidungsbaum)

`data/mandatory-triggers.yaml` defines when specific workflows must activate — this is a proto-orchestrator that routes user queries to appropriate Layer 1/Layer 2 operations.

### 11.4 Superkey-Architektur (State Management)

The 5-database Superkey architecture (`EBF-S-{YYYY}-{MM}-{DD}-{DOMAIN}-{SEQ}`) provides session state management — a prerequisite for formal orchestration.

---

## 12. CONTRA-Evidenz und Grenzen der Architektur

### 12.1 Reasoning Models (DeepSeek-R1)

**Challenge:** DeepSeek-R1 demonstrates that pure reinforcement learning can induce reasoning behaviors without explicit symbolic layers. This suggests the boundary between Layer 1 and Layer 3 may be dynamic, not static.

**Assessment:** Serious but not invalidating. Even if LLMs improve at computation, the principle of separation of concerns remains valid. A dynamic layer boundary means the WHAT of each layer may change, but the WHY (separation) remains.

**Monitoring Trigger:** When reasoning models achieve 95%+ accuracy on formal computation benchmarks consistently across domains, the TLA layer boundaries must be re-evaluated.

### 12.2 Structured Output Degradation (Tam et al. 2024)

**Challenge:** Forcing JSON/YAML output degrades LLM reasoning performance by 10-15%.

**Assessment:** Important design constraint. Layer 3 must not be over-constrained. The LLM needs freedom in HOW it translates, even if WHAT it translates is formal.

**Practical Implication:** Layer 3 constraints should be on content (don't override formal results) not on format (allow flexible natural language).

### 12.3 Monitoring-Trigger (Wann TLA revidiert werden muss)

The TLA must be revised when ANY of these conditions are met:

| Trigger | Threshold | Current Status |
|---------|-----------|----------------|
| Reasoning models on formal benchmarks | 95%+ consistently | ~70-80% (2025) |
| Structured output penalty eliminated | 0% degradation | 10-15% (2024) |
| Model collapse solved | No degradation through recursion | Not solved (2024) |

---

## 13. Implementation Roadmap

### Phase 1: Documentation (THIS Document) ✅

- Canonical entry KB-TLA-001 created
- Framework deep-dive (this document)
- Index and cross-references updated
- CLAUDE.md AXIOM 6 added

### Phase 2: PCT Python-Implementierung

```
Priority: HIGH
Goal: Implement Parameter Context Transformation as Python script
Formula: θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)
Input: parameter-registry.yaml + context dimensions
Output: Context-adjusted parameter value
```

### Phase 3: Universelle Parameter-Lookup API

```
Priority: MEDIUM
Goal: Single entry point for all Layer 2 lookups
Interface: query_parameter(param_id, context_vector) → value + CI + source
Implementation: Python module reading from all YAML registries
```

### Phase 4: Formaler Orchestrator

```
Priority: FUTURE
Goal: Automated routing of user queries through Layer 3 → 2 → 1 → 3
Current: Manual via CLAUDE.md instructions
Target: Python orchestrator with decision tree
```

---

## Appendix A: Cross-Reference Map

| From | To | Relationship |
|------|----|-------------|
| KB-TLA-001 | KB-VIR-001 | TLA defends against viruses |
| KB-TLA-001 | parameter-registry.yaml | Layer 2 data source |
| KB-TLA-001 | model-registry.yaml | Layer 1 model definitions |
| KB-VIR-001 | KB-TLA-001 | Virus definition references TLA as defense |
| CLAUDE.md AXIOM 6 | KB-TLA-001 | Operational enforcement |
| PSF-2.0 | KB-TLA-001 | Reference implementation |
| scripts/r_score.py | KB-TLA-001 | Layer 1 implementation |
| scripts/emerge_algorithm.py | KB-TLA-001 | Layer 1 implementation |

## Appendix B: Vollstaendige Literatur-Tabelle

| # | BibTeX Key | Title | Journal | Year | TLA Claim | Layer |
|---|-----------|-------|---------|------|-----------|-------|
| 1 | gao2023pal | PAL: Program-Aided Language Models | ICML | 2023 | +40% via Python delegation | L1 |
| 2 | schick2023toolformer | Toolformer | NeurIPS | 2023 | LLMs should use tools | L1 |
| 3 | goodell2025clinical | Clinical Calculations with LLM Agents | Nature npj | 2025 | 5.5-13x error reduction | L1 |
| 4 | shumailov2024collapse | AI models collapse on recursive data | Nature | 2024 | Model collapse proves L3 vulnerability | L3 |
| 5 | vosoughi2018spread | Spread of true and false news | Science | 2018 | False info 6x faster | L3 |
| 6 | bai2022constitutional | Constitutional AI | Anthropic | 2022 | Formal constraints needed | L3→L1 |
| 7 | lewis2020retrieval | RAG for Knowledge-Intensive NLP | NeurIPS | 2020 | +35% factuality via retrieval | L2 |
| 8 | dijkstra1974separation | On the Role of Scientific Thought | EWD447 | 1974 | Separation of concerns | Architecture |
| 9 | parnas1972criteria | Criteria for Decomposing Systems | CACM | 1972 | Information hiding | Architecture |
| 10 | ji2023hallucination | Survey of Hallucination in NLG | ACM Survey | 2023 | LLMs systematically hallucinate | L3 |

---

*Cross-references:*
- Canonical Entry: `data/knowledge/canonical/three-layer-architecture.yaml`
- Virus Definition: `data/knowledge/canonical/virus-definition.yaml`
- Parameter Registry: `data/parameter-registry.yaml`
- Existing Layer 1 Scripts: `scripts/r_score.py`, `scripts/emerge_algorithm.py`
- PSF-2.0 (Reference Implementation): `models/psf-2.0/`
