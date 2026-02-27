# EBF Three-Layer Pipeline Architecture

> Architecture Decision Record (ADR) and operational reference for the
> formal parameter computation pipeline.

**Created:** 2026-02-15
**SSOT:** This document describes the runtime pipeline. For the theoretical
foundation, see `data/knowledge/canonical/three-layer-architecture.yaml`.

---

## 1. Executive Summary

The EBF pipeline transforms a user's parameter query into a provenance-tracked
result through three deterministic layers. Every number in the output can be
traced to a YAML source, a Python computation, or both — never to LLM memory.

```
User Query
    |
    v
Orchestrator (scripts/orchestrator.py)
    |
    +-- Layer 2: Parameter Store (YAML)
    |       data/parameter-registry.yaml
    |
    +-- Layer 1a: PCT (Python)
    |       scripts/pct.py
    |       data/pct-multiplier-tables.yaml
    |       data/pct-psi-scales.yaml
    |       data/pct-measurement-contexts.yaml
    |
    +-- Layer 1b: LLMMC (Python)
    |       scripts/llmmc_calibration.py
    |
    +-- Layer 3: Translation Templates (Markdown)
    |       scripts/translation_templates.py
    |
    v
OrchestratorResult (full provenance chain)
```

---

## 2. Architecture Decisions

### ADR-001: Separation of Computation and Translation

**Status:** Accepted (2026-02-15)
**Context:** LLMs hallucinate numeric values. The EBF framework requires
parameter values to be deterministic and reproducible.
**Decision:** All numeric computation happens in Python (Layer 1).
The LLM is restricted to translating formal results into natural language
(Layer 3). No number passes through the LLM.
**Consequences:** Every output value has a verifiable provenance chain.
LLM creative capabilities are limited to explanation, not computation.
**Evidence:** Gao et al. (2023) PAL: 40% improvement when delegating
computation to Python. Goodell et al. (2025): 5.5-13x error reduction
with deterministic tools.

### ADR-002: Auto-Anchor Discovery via Measurement Contexts

**Status:** Accepted (2026-02-15)
**Context:** Users often know what context they want a parameter for
(target) but not which paper measured it (anchor). Requiring explicit
anchor specification creates friction.
**Decision:** When only `target_psi` is provided, the orchestrator
searches `data/pct-measurement-contexts.yaml` (39 triplets from 8 papers)
to find the best matching anchor based on Psi-dimension overlap.
**Consequences:** Users can query with just a target context. The system
automatically finds the closest measured context to anchor from. Quality
depends on measurement context coverage (currently 39 triplets).

### ADR-003: Lightweight REST API via stdlib

**Status:** Accepted (2026-02-15)
**Context:** The pipeline needs to be accessible from external tools
(dashboards, notebooks, other scripts) beyond the CLI.
**Decision:** Use Python's `http.server` from stdlib for the REST API.
No external dependencies (no Flask, FastAPI, etc.).
**Consequences:** Zero additional dependencies. Suitable for local
development and internal tooling. Not production-grade for high-traffic
deployment (use a proper WSGI/ASGI server for that).

### ADR-004: Translation Templates as Structured Markdown

**Status:** Accepted (2026-02-15)
**Context:** Layer 3 output needs to be consistent across sessions
while preserving provenance tracking.
**Decision:** Six template types (SIMPLE, CONTEXTUAL, CALIBRATED,
BATCH, HEALTH, EXPLAIN) generate structured markdown with tables,
provenance notes, and compliance markers.
**Consequences:** Output format is deterministic for the same input.
Templates can be extended without modifying core computation logic.

---

## 3. Component Reference

### 3.1 Orchestrator (`scripts/orchestrator.py`)

The central coordinator connecting all three layers.

**Key classes:**
- `Orchestrator` — Main pipeline class
- `OrchestratorResult` — Provenance-tracked result dataclass
- `HealthCheckResult` — Pipeline health status
- `QueryType` (enum) — SIMPLE, CONTEXTUAL, CALIBRATED, BATCH, HEALTH, EXPLAIN

**Key methods:**
| Method | Layer(s) | Description |
|--------|----------|-------------|
| `query(id, context, calibrate)` | 2 + 1a + 1b | Full pipeline query |
| `batch_query(ids, context, calibrate)` | 2 + 1a + 1b | Multiple parameters |
| `health_check()` | 2 + 1a + 1b | 6-stage health check |
| `explain(id, context, calibrate)` | 2 + 1a + 1b + 3 | Human-readable explanation |
| `list_parameters(domain)` | 2 | List available parameters |
| `find_best_anchor(id, target_psi)` | 2 | Auto-anchor discovery |

**CLI flags:**
| Flag | Description |
|------|-------------|
| `--id <PAR-ID>` | Parameter ID |
| `--symbol <sym>` | Parameter symbol |
| `--target-psi key=val,...` | Target Psi-conditions |
| `--anchor-psi key=val,...` | Anchor Psi-conditions |
| `--anchor-context <name>` | Anchor context label |
| `--calibrate` | Apply LLMMC calibration |
| `--batch <id1,id2,...>` | Batch query |
| `--list` | List parameters |
| `--health` | Health check |
| `--explain` | Human-readable explanation |
| `--translate` | Layer 3 markdown output |
| `--json` | JSON output |
| `-v, --verbose` | Verbose logging |

### 3.2 Parameter API (`scripts/parameter_api.py`)

Universal entry point for parameter retrieval.

**Python API:**
```python
from parameter_api import get_parameter, lookup_parameter, list_parameters

# Layer 2 only
val = get_parameter("PAR-BEH-001")

# Full pipeline
val = lookup_parameter("PAR-BEH-016",
    target_psi={"psi_S": "competence_signaling"},
    calibrate=True)

# List
params = list_parameters(domain="FIN")
```

**REST API endpoints (via `--serve`):**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /api/v1/parameter/<id>` | GET | Single lookup |
| `GET /api/v1/parameter/<id>?psi_S=x` | GET | With PCT transform |
| `GET /api/v1/parameter/<id>?calibrate=true` | GET | With LLMMC |
| `GET /api/v1/parameters` | GET | List all |
| `GET /api/v1/parameters?domain=FIN` | GET | Filtered list |
| `GET /api/v1/batch?ids=A,B` | GET | Batch query |
| `GET /api/v1/health` | GET | Health check |
| `GET /` | GET | API documentation |

**Start server:**
```bash
python scripts/parameter_api.py --serve --port 8080
```

### 3.3 PCT (`scripts/pct.py`)

Parameter Context Transformation: `theta_B = theta_A * prod_i M(delta_Psi_i)`

**Key functions:**
| Function | Description |
|----------|-------------|
| `transform(anchor, target_psi, parameter_id)` | Core PCT computation |
| `transform_from_contexts(theta_A, anchor_psi, target_psi, ...)` | Context-based transform |
| `find_best_anchor(parameter_id, target_psi)` | Auto-anchor discovery |

**Data files:**
| File | Description | Entries |
|------|-------------|---------|
| `data/pct-multiplier-tables.yaml` | M(delta_Psi) reference ranges | 8 dimensions |
| `data/pct-psi-scales.yaml` | Categorical -> numeric mapping | 101 labels |
| `data/pct-measurement-contexts.yaml` | Paper measurement contexts | 39 triplets |

### 3.4 LLMMC (`scripts/llmmc_calibration.py`)

Bayesian calibration with empirical anchors.

**Key classes:**
- `LLMMCCalibrator` — Bayesian calibration engine
- `CalibrationResult` — Result with shrinkage factor and CI

**Pipeline:**
1. Collect empirical anchors (known parameter values)
2. Add PCT-derived anchors from measurement contexts
3. Fit Bayesian regression
4. Calibrate PCT result toward empirical mean (shrinkage)

### 3.5 Translation Templates (`scripts/translation_templates.py`)

Layer 3 structured markdown generation.

**Templates:**
| Template | When used | Key features |
|----------|-----------|-------------|
| SIMPLE | Layer 2 only result | Value table, source, tier |
| CONTEXTUAL | PCT applied | Multiplier table, direction labels |
| CALIBRATED | PCT + LLMMC | Shrinkage, confidence level |
| BATCH | Multiple params | Combined table |
| HEALTH | Health check | Stage status table |
| EXPLAIN | Explanation | Parameter description + compliance |

---

## 4. Data Flow

### 4.1 Simple Query

```
User: "What is loss aversion?"
  |
  v
Orchestrator.query("PAR-BEH-001")
  |
  +-- Layer 2: parameter-registry.yaml
  |     -> value=2.35, ci=[1.8, 3.1], source=kahneman1979prospect
  |
  v
OrchestratorResult(value=2.35, layers=["layer2"], tier=1)
```

### 4.2 Contextual Query (PCT)

```
User: "Loss aversion in workplace context?"
  |
  v
Orchestrator.query("PAR-BEH-016", context={target_psi: {psi_S: "competence_signaling"}})
  |
  +-- Layer 2: parameter-registry.yaml
  |     -> theta_A = 2.0
  |
  +-- Auto-anchor: pct-measurement-contexts.yaml
  |     -> best anchor: benabou2022hurts (welfare_stigma)
  |
  +-- Layer 1a (PCT): pct.py
  |     -> delta_psi_S = competence_signaling(0.55) - welfare_stigma(0.85)
  |     -> M(delta_psi_S) = 0.85 (dampening)
  |     -> theta_B = 2.0 * 0.85 = 1.70
  |
  v
OrchestratorResult(value=1.70, pct_applied=True, layers=["layer2", "layer1_pct"])
```

### 4.3 Full Pipeline (PCT + LLMMC)

```
User: "Calibrated loss aversion for workplace?"
  |
  v
Orchestrator.query("PAR-BEH-016", context={...}, calibrate=True)
  |
  +-- Layer 2 + Layer 1a (PCT) -> theta_B = 1.70
  |
  +-- Layer 1b (LLMMC): llmmc_calibration.py
  |     -> anchors from measurement contexts + empirical data
  |     -> Bayesian shrinkage = 0.127
  |     -> theta_final = 1.485
  |     -> ci_95 = [1.21, 1.76]
  |
  v
OrchestratorResult(value=1.485, llmmc_applied=True, tier=2.5,
                   layers=["layer2", "layer1_pct", "layer1_llmmc"])
```

### 4.4 Translated Output

```
OrchestratorResult
  |
  +-- translation_templates.py
  |     -> detect_template(result) -> CALIBRATED
  |     -> render_calibrated(result) -> markdown with tables
  |
  v
## Loss Aversion (lambda_R) - Kalibrierte Transformation
| Eigenschaft | Wert |
|-------------|------|
| **Wert** | 1.4850 |
| **95% CI** | [1.2100, 1.7600] |
| **Tier** | 2.5 (PCT-informed calibration) |
...
```

---

## 5. Pipeline Health Check

The health check validates all 6 pipeline stages:

| Stage | What it checks | Pass condition |
|-------|---------------|----------------|
| `registry` | parameter-registry.yaml loadable | >0 parameters found |
| `symbols` | Symbol normalization works | lambda -> PAR-BEH-001 |
| `pct` | PCT module importable + functional | transform() runs |
| `llmmc` | LLMMC module importable + functional | calibrate() runs |
| `full_pipeline` | End-to-end query succeeds | result.value > 0 |
| `data_files` | Required YAML files exist | All 4 files present |

**CLI:**
```bash
python scripts/orchestrator.py --health
python scripts/orchestrator.py --health --json
python scripts/orchestrator.py --health --translate
```

---

## 6. Test Coverage

| Test Suite | Tests | What it covers |
|-----------|-------|----------------|
| `test_orchestrator.py` | 40 | Query types, health, batch, provenance |
| `test_pct.py` | 33 | PCT transforms, scales, multipliers, auto-anchor |
| `test_translation_templates.py` | 38 | All 6 template types, helpers |
| `test_end_to_end_pipeline.py` | 53 | Full pipeline flows, REST API handler, edge cases |
| `test_parameter_api.py` | 21 | Parameter lookup, domain filtering |
| `test_llmmc_pct_integration.py` | 22 | LLMMC + PCT combined flows |
| **Total** | **207** | |

**Run all tests:**
```bash
python -m pytest tests/test_orchestrator.py tests/test_pct.py \
    tests/test_translation_templates.py tests/test_end_to_end_pipeline.py \
    tests/test_parameter_api.py tests/test_llmmc_pct_integration.py -v
```

---

## 7. File Map

```
scripts/
  orchestrator.py              # Central orchestrator (Layer 1+2+3)
  parameter_api.py             # Universal API + REST server
  pct.py                       # Parameter Context Transformation
  llmmc_calibration.py         # Bayesian calibration
  translation_templates.py     # Layer 3 structured templates
  pct_smoke_test.py            # 8-stage integration smoke test

data/
  parameter-registry.yaml      # Layer 2: Parameter values (SSOT)
  pct-multiplier-tables.yaml   # PCT: M(delta_Psi) reference ranges
  pct-psi-scales.yaml          # PCT: Categorical -> numeric scales
  pct-measurement-contexts.yaml # PCT: Paper measurement contexts
  mandatory-triggers.yaml      # T-QUERY trigger for /query-parameter

tests/
  test_orchestrator.py         # Orchestrator unit tests
  test_pct.py                  # PCT unit tests
  test_translation_templates.py # Translation template tests
  test_end_to_end_pipeline.py  # Full pipeline integration tests
  test_parameter_api.py        # Parameter API tests
  test_llmmc_pct_integration.py # LLMMC+PCT integration tests

.claude/commands/
  query-parameter.md           # /query-parameter skill definition

docs/frameworks/
  pipeline-architecture.md     # This document
  three-layer-architecture.md  # Theoretical foundation
```

---

## 8. Usage Examples

### Python API

```python
from orchestrator import Orchestrator

orch = Orchestrator()

# Simple lookup
result = orch.query("PAR-BEH-001")
print(f"{result.name}: {result.value:.4f}")

# Contextual (auto-anchor)
result = orch.query("PAR-BEH-016", context={
    "target_psi": {"psi_S": "competence_signaling"}
})
print(f"Transformed: {result.value:.4f} (M={result.pct_product_M:.4f})")

# Full pipeline
result = orch.query("PAR-BEH-016", context={
    "target_psi": {"psi_S": "competence_signaling"},
    "anchor_psi": {"psi_S": "welfare_stigma"},
    "anchor_context": "welfare",
}, calibrate=True)
print(f"Calibrated: {result.value:.4f} [{result.ci_95[0]:.4f}, {result.ci_95[1]:.4f}]")

# Translated markdown
from translation_templates import translate
markdown = translate(result)
```

### CLI

```bash
# Simple
python scripts/orchestrator.py --id PAR-BEH-001

# Auto-anchor PCT
python scripts/orchestrator.py --id PAR-BEH-016 \
    --target-psi psi_S=competence_signaling

# Full pipeline with markdown
python scripts/orchestrator.py --id PAR-BEH-016 \
    --target-psi psi_S=competence_signaling \
    --calibrate --translate

# REST API
python scripts/parameter_api.py --serve --port 8080
# Then: curl http://localhost:8080/api/v1/parameter/PAR-BEH-001
```

### REST API

```bash
# Start server
python scripts/parameter_api.py --serve

# Simple lookup
curl http://localhost:8080/api/v1/parameter/PAR-BEH-001

# With PCT
curl "http://localhost:8080/api/v1/parameter/PAR-BEH-016?psi_S=competence_signaling"

# With calibration
curl "http://localhost:8080/api/v1/parameter/PAR-BEH-016?psi_S=competence_signaling&calibrate=true"

# List all
curl http://localhost:8080/api/v1/parameters

# Health check
curl http://localhost:8080/api/v1/health

# Batch
curl "http://localhost:8080/api/v1/batch?ids=PAR-BEH-001,PAR-BEH-016"
```

---

## 9. Monitoring Concepts

### 9.1 Health Check Automation

The pipeline health check can be integrated into CI:

```yaml
# .github/workflows/pipeline-health.yml
- name: Pipeline Health Check
  run: python scripts/orchestrator.py --health --json
```

### 9.2 Key Metrics

| Metric | Measurement | Target |
|--------|-------------|--------|
| Registry coverage | Parameters in YAML | >64 |
| PCT measurement contexts | Triplets in YAML | >39 (growing) |
| Psi scale labels | Labels in YAML | >101 |
| Test pass rate | pytest --tb=short | 100% |
| Pipeline latency | health_check elapsed_ms | <500ms |
| Auto-anchor hit rate | Queries with auto-anchor success | >80% |

### 9.3 Extension Points

| Extension | File to modify | Effort |
|-----------|---------------|--------|
| Add Psi labels | `data/pct-psi-scales.yaml` | Low |
| Add measurement contexts | `data/pct-measurement-contexts.yaml` | Low |
| New translation template | `scripts/translation_templates.py` | Medium |
| New REST endpoint | `scripts/parameter_api.py` | Medium |
| New Layer 1 module | `scripts/` + `orchestrator.py` | High |

---

*Pipeline Architecture v1.0 — 2026-02-15*
