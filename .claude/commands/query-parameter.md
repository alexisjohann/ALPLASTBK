# /query-parameter - Three-Layer Parameter Query

Query EBF parameters through the formal Three-Layer Orchestrator with full provenance tracking.

This wraps `scripts/orchestrator.py` for interactive use in EBF sessions, ensuring **every number comes from Layer 1 (Python) or Layer 2 (YAML), never from LLM memory**.

## Usage

```
/query-parameter                           # Interactive mode
/query-parameter PAR-BEH-001              # Simple lookup (Layer 2)
/query-parameter PAR-BEH-016 --context    # Contextual query (Layer 2 + PCT)
/query-parameter --health                 # Pipeline health check
/query-parameter --list                   # List all parameters
```

---

## Query Modes

### Mode 1: Simple Lookup (Layer 2 Only)

When a parameter ID or symbol is provided without context:

```
/query-parameter PAR-BEH-001
/query-parameter lambda_R
```

**What happens:**
1. Layer 2: Load parameter from `data/parameter-registry.yaml`
2. Return: value, CI, source, tier — no transformation

**Output:**
```
┌─────────────────────────────────────────────────────────────┐
│  PAR-BEH-001: Loss Aversion Coefficient (λ)                 │
│  Value: 2.3500                                              │
│  CI 95%: [1.8000, 3.1000]                                   │
│  Source: kahneman1979prospect                               │
│  Tier: 1 (Literature)                                       │
│  Layers: [Layer 2]                                          │
└─────────────────────────────────────────────────────────────┘
```

### Mode 2: Contextual Query (Layer 2 + Layer 1 PCT)

When target and anchor Ψ-contexts are provided:

```
/query-parameter PAR-BEH-016 --context
```

Claude will ask for:
- **Target Ψ:** The context you want the parameter for (e.g., workplace, competence signaling)
- **Anchor Ψ:** The measurement context from the paper (e.g., welfare, stigma) — **OPTIONAL with auto-anchor**
- **Anchor context name:** Short label for the paper's context — **OPTIONAL with auto-anchor**

**Auto-Anchor Discovery (NEU):** If only `target_psi` is provided (no `anchor_psi`), the orchestrator automatically discovers the best anchor from `data/pct-measurement-contexts.yaml` (39 triplets from 8 papers). The closest matching measurement context is selected based on Ψ-dimension overlap.

**What happens:**
1. Layer 2: Load base parameter from YAML
2. Layer 1 (PCT): Transform θ_A → θ_B via `θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)`
3. Return: transformed value + multiplier chain

**Output:**
```
┌─────────────────────────────────────────────────────────────┐
│  PAR-BEH-016: Reference-Dependent Utility (λ_R)             │
│  Base (anchor): 2.0000                                      │
│  Transformed:   1.5300                                      │
│  PCT Product M: 0.7650                                      │
│  Multipliers:                                               │
│    Ψ_S: stigma_decrease → 0.85                              │
│    Ψ_I: formality_decrease → 0.90                           │
│  Layers: [Layer 2, Layer 1 PCT]                             │
└─────────────────────────────────────────────────────────────┘
```

### Mode 3: Calibrated Query (Full Pipeline)

Add `--calibrate` for LLMMC calibration on top of PCT:

```
/query-parameter PAR-BEH-016 --context --calibrate
```

**What happens:**
1. Layer 2: Load base parameter
2. Layer 1 (PCT): Context transformation
3. Layer 1 (LLMMC): Bayesian calibration with empirical anchors
4. Return: calibrated value + shrinkage factor + full provenance

**Output:**
```
┌─────────────────────────────────────────────────────────────┐
│  PAR-BEH-016: Reference-Dependent Utility (λ_R)             │
│  Base (anchor):  2.0000                                     │
│  PCT transform:  1.5300  (M = 0.7650)                       │
│  LLMMC calibr:   1.4850  (shrinkage = 0.127)               │
│  CI 95%: [1.2100, 1.7600]                                   │
│  Layers: [Layer 2, Layer 1 PCT, Layer 1 LLMMC]             │
│  Tier: 2.5 (PCT-informed calibration)                       │
└─────────────────────────────────────────────────────────────┘
```

### Mode 4: Batch Query

Query multiple parameters at once:

```
/query-parameter --batch PAR-BEH-001,PAR-BEH-016,PAR-COMP-001
```

### Mode 5: Health Check

Verify the entire Layer 1 pipeline is operational:

```
/query-parameter --health
```

Runs 6 stages: Registry → Symbols → PCT → LLMMC → Integration → Parameter API

### Mode 6: Explain

Get a human-readable explanation of a parameter:

```
/query-parameter PAR-BEH-001 --explain
```

### Mode 7: Translated Markdown Output

Get provenance-tracked markdown via Layer 3 translation templates:

```
/query-parameter PAR-BEH-001 --translate
/query-parameter PAR-BEH-016 --context --translate
/query-parameter --health --translate
```

Auto-detects the best template (SIMPLE, CONTEXTUAL, CALIBRATED, HEALTH) based on the result. Output is structured markdown with tables, provenance notes, and Three-Layer Compliance markers.

---

## Interactive Workflow (DEFAULT)

When called without arguments, Claude runs the interactive workflow:

```
┌─────────────────────────────────────────────────────────────┐
│  /query-parameter INTERACTIVE MODE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SCHRITT 1: Parameter identifizieren                        │
│     → ID (PAR-BEH-001) oder Symbol (λ_R) oder Stichwort    │
│                                                             │
│  SCHRITT 2: Query-Typ bestimmen                             │
│     → SIMPLE:     Nur Layer 2 (Wert aus Registry)           │
│     → CONTEXTUAL: + Layer 1 PCT (Kontext-Transformation)    │
│     → CALIBRATED: + Layer 1 LLMMC (Bayesian Kalibrierung)   │
│                                                             │
│  SCHRITT 3: Kontext spezifizieren (wenn CONTEXTUAL/CALIBR.) │
│     → Target Ψ: Wofür brauchen Sie den Parameter?          │
│     → Anchor Ψ: Aus welchem Mess-Kontext stammt der Wert?  │
│                                                             │
│  SCHRITT 4: Ergebnis mit Provenance                         │
│     → Wert + CI + Layers + Multiplikatoren                  │
│     → JSON-Export möglich (--json)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Claude MUSS bei /query-parameter

1. **NIEMALS** Parameter-Werte aus dem Gedaechtnis nennen
2. **IMMER** `scripts/orchestrator.py` oder `scripts/parameter_api.py` verwenden
3. **IMMER** die verwendeten Layer dokumentieren (Layer 2, Layer 1 PCT, Layer 1 LLMMC)
4. **IMMER** Provenance zeigen (Quelle, Tier, Multiplikatoren)
5. Bei kontextabhaengigen Fragen: **IMMER** PCT anwenden (nicht schaetzen)
6. Bei Unsicherheit ueber Kontext: **FRAGEN**, nicht annehmen

## Implementation

Claude fuehrt die Abfrage durch via:

```python
import sys
sys.path.insert(0, "scripts")
from orchestrator import Orchestrator

orch = Orchestrator()

# Simple
result = orch.query("PAR-BEH-001")

# Contextual
result = orch.query("PAR-BEH-016", context={
    "target_psi": {"psi_S": "competence_signaling"},
    "anchor_psi": {"psi_S": "welfare_stigma"},
    "anchor_context": "welfare",
})

# Calibrated
result = orch.query("PAR-BEH-016", context={...}, calibrate=True)

# Health
health = orch.health_check()

# Batch
results = orch.batch_query(["PAR-BEH-001", "PAR-BEH-016"])
```

Or via CLI:

```bash
# Simple lookup
python scripts/orchestrator.py --id PAR-BEH-001

# Contextual with explicit anchor
python scripts/orchestrator.py --id PAR-BEH-016 \
    --target-psi psi_S=competence_signaling \
    --anchor-psi psi_S=welfare_stigma \
    --anchor-context welfare --calibrate --json

# Auto-anchor discovery (only target_psi needed)
python scripts/orchestrator.py --id PAR-BEH-016 \
    --target-psi psi_S=competence_signaling

# Formatted markdown output (Layer 3 translation)
python scripts/orchestrator.py --id PAR-BEH-001 --translate
python scripts/orchestrator.py --health --translate

# Other modes
python scripts/orchestrator.py --health
python scripts/orchestrator.py --batch PAR-BEH-001,PAR-BEH-016
python scripts/orchestrator.py --symbol lambda_R --explain

# REST API server (Layer 1 Gateway)
python scripts/parameter_api.py --serve --port 8080
```

---

## Three-Layer Compliance

This skill enforces AXIOM 6 (Three-Layer Architecture):

| Layer | Role | Susceptibility | What it does |
|-------|------|---------------|--------------|
| 1 | Formal Computation (Python) | 0.0 (immune) | PCT transform, LLMMC calibrate |
| 2 | Parameter Store (YAML) | 0.3 (validatable) | Load values with schema, sources, ranges |
| 3 | LLM Translation | 0.8 (susceptible) | Explain results in natural language |

**The LLM is TRANSLATOR, not THINKER.** Numbers come from Layer 1+2. Language comes from Layer 3.

---

## References

- **Orchestrator:** `scripts/orchestrator.py` (7 query types incl. --translate)
- **Parameter API:** `scripts/parameter_api.py` (universal lookup + REST server via --serve)
- **Translation Templates:** `scripts/translation_templates.py` (Layer 3 structured markdown)
- **PCT:** `scripts/pct.py` (Parameter Context Transformation)
- **LLMMC:** `scripts/llmmc_calibration.py` (Bayesian calibration)
- **Measurement Contexts:** `data/pct-measurement-contexts.yaml` (39 triplets, auto-anchor discovery)
- **Psi Scales:** `data/pct-psi-scales.yaml` (101 labels across 8 dimensions)
- **Smoke Test:** `scripts/pct_smoke_test.py` (8-stage pipeline test)
- **Tests:** `tests/test_orchestrator.py` (40 tests), `tests/test_parameter_api.py` (21 tests), `tests/test_pct.py` (33 tests), `tests/test_translation_templates.py` (38 tests), `tests/test_llmmc_pct_integration.py` (22 tests), `tests/test_end_to_end_pipeline.py` (53 tests)
- **Pipeline Architecture:** `docs/frameworks/pipeline-architecture.md`
- **AXIOM 6:** `data/knowledge/canonical/three-layer-architecture.yaml`
