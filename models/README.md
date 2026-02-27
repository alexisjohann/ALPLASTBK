# ALPLA Churn Intervention Model (ACIM)

> Bayesian model for predicting and updating churn reduction effects from HR interventions

## Quick Start

```python
from models.alpla_churn_model import ALPLAChurnModel

# Initialize model
model = ALPLAChurnModel()

# Predict churn reduction
prediction = model.predict("US-006", ["INT1", "INT2", "INT6"])
print(prediction.summary())
```

## Output Example

```
╔══════════════════════════════════════════════════════════════╗
║  CHURN REDUCTION PREDICTION                                   ║
╠══════════════════════════════════════════════════════════════╣
║  Plant: US-006                                                ║
║  Interventions: INT1, INT2, INT6                              ║
╠══════════════════════════════════════════════════════════════╣
║  Expected Reduction:   10.2 pp  (SD: 1.7)                     ║
║  Median:               10.1 pp                                ║
╠══════════════════════════════════════════════════════════════╣
║  Credible Intervals:                                          ║
║    50% CI: [  9.0, 11.3] pp                                   ║
║    80% CI: [  7.8, 12.5] pp                                   ║
║    95% CI: [  6.6, 13.2] pp                                   ║
╚══════════════════════════════════════════════════════════════╝
```

## Model Structure

### EBF 10C Integration

The model implements EBF framework equations:

| Stage | Equation | Description |
|-------|----------|-------------|
| 1 | `U^pot = Σ ω_d · U_d + Σ γ · U_d · U_d'` | Potential Utility |
| 2 | `U^eff = A · U^pot` | Effective Utility (Awareness filter) |
| 3 | `P(Stay) = σ(β · (U^eff - θ))` | Stay Probability |
| 4 | `ΔChurn = Σ δ_j · I_j · Fit · A · (1 + Σ γ_jj')` | Intervention Effect |

### 8 Interventions

| Code | Name | Expected Effect | Time Constant |
|------|------|-----------------|---------------|
| INT1 | Job Rotation | 6.5 ± 2.0 pp | 8 weeks |
| INT2 | Career Pathway | 5.0 ± 1.8 pp | 16 weeks |
| INT3 | Skill-Based Pay | 4.0 ± 1.5 pp | 24 weeks |
| INT4 | Workload Management | 3.0 ± 1.2 pp | 10 weeks |
| INT5 | Autonomy Enhancement | 4.0 ± 1.5 pp | 12 weeks |
| INT6 | Recognition Program | 2.0 ± 1.0 pp | 4 weeks |
| INT7 | Onboarding Improvement | 3.0 ± 1.5 pp | 6 weeks |
| INT8 | Team Restructuring | 3.0 ± 1.5 pp | 12 weeks |

### Key Synergies (γ)

| Pair | γ | Mechanism |
|------|---|-----------|
| INT1 + INT2 | +0.35 | Rotation shows career paths |
| INT2 + INT3 | +0.40 | Career + Pay reinforce development |
| INT5 + INT6 | +0.25 | Autonomy + Recognition = Empowerment |
| INT3 + INT8 | -0.45 | Too much change simultaneously |

## Usage

### Basic Prediction

```python
from models.alpla_churn_model import ALPLAChurnModel

model = ALPLAChurnModel()

# Single plant prediction
pred = model.predict("US-006", ["INT1", "INT2", "INT6"])
print(f"Expected: {pred.mean:.1f}pp reduction")
print(f"95% CI: [{pred.ci_95[0]:.1f}, {pred.ci_95[1]:.1f}]")
```

### Scenario Analysis

```python
scenarios = model.scenario_analysis("US-006", ["INT1", "INT2", "INT6"])

for name, pred in scenarios.items():
    print(f"{name}: {pred.mean:.1f}pp [{pred.ci_95[0]:.1f}, {pred.ci_95[1]:.1f}]")
```

### Find Optimal Bundle

```python
optimal, pred = model.get_optimal_bundle(
    "US-006",
    max_interventions=3,
    budget_constraint="medium"
)
print(f"Optimal: {optimal} → {pred.mean:.1f}pp reduction")
```

### Bayesian Update (after experiment)

```python
# After collecting field data
field_data = {
    "US-006": {
        "interventions": ["INT1", "INT2", "INT6"],
        "churn_baseline": 28.0,
        "churn_observed": 18.0,
        "duration_weeks": 52,
        "implementation_quality": 0.85
    }
}

# Update model with observations
model.update(field_data)

# Get posterior predictions
posterior_pred = model.predict("US-015", ["INT1", "INT2", "INT6"], use_posterior=True)
```

### Simulate Experiment

```python
from models.alpla_churn_model import simulate_experiment

treatment = {
    "US-006": ["INT1", "INT2", "INT6"],
    "US-015": ["INT2", "INT3", "INT6"]
}
control = ["US-007", "US-008"]

results = simulate_experiment(model, treatment, control)
print(f"Simulated DiD: {results['did_estimate']:.1f}pp")
```

## Files

| File | Description |
|------|-------------|
| `alpla-churn-model.yaml` | Model specification (priors, equations, validation) |
| `alpla_churn_model.py` | Python implementation |
| `README.md` | This documentation |

## Dependencies

```
numpy
scipy
pyyaml
```

Optional for full MCMC:
```
pymc>=5.0
arviz
```

## References

- **EBF Framework**: docs/frameworks/core-framework-definition.yaml
- **Prior Sources**: appendices/BBB_estimation_methodology.tex
- **Intervention Toolkit**: appendices/HHH_intervention_toolkit.tex
- **ALPLA Integration**: data/alpla-ebf-integration.yaml

---

*Model Version: 1.0 | EBF Version: 10C | Registry: FFF-ALPLA-CHURN-001*
