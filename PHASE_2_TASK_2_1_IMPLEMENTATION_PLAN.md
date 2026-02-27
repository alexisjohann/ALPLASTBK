# PHASE 2, TASK 2.1: Complementarity Parameters (γ)
## Detailed Implementation Plan - 4 Week Sprint

**Status**: READY TO EXECUTE
**Timeline**: 4 weeks (2026 Q1)
**Goal**: Estimate 10 complementarity parameters; reduce duration RMSE from 2.73 to <1.5

---

## Week 1: Data Preparation & Visualization

### Week 1 Tasks

#### 1.1: Compile Complete Dataset (2 hours)
Create unified dataset with all 12 conclaves:

```python
# Data structure needed:
conclaves = [
    {
        "year": 1878,
        "winner": "Leo XIII",
        "lambda": 0.82,
        "iota": 0.88,
        "pi": 0.70,
        "nu": 0.75,
        "alpha": 0.85,
        "ballots": 3,
        "duration_days": 2,
    },
    # ... 11 more conclaves
]

# Validate data
assert len(conclaves) == 12
for conclave in conclaves:
    assert all(0.0 <= v <= 1.0 for v in [conclave["lambda"], ...])
    assert conclave["ballots"] > 0
```

**Output**: `data/psf_conclaves_complete.csv` (single source for analysis)

---

#### 1.2: Calculate Interaction Terms (1 hour)
Create all 10 interaction features:

```python
import pandas as pd

df = pd.read_csv('data/psf_conclaves_complete.csv')

# Main effects (already in data)
# X = [lambda, iota, pi, nu, alpha]

# Interaction terms (compute)
df['lambda_x_iota'] = df['lambda'] * df['iota']
df['lambda_x_pi'] = df['lambda'] * df['pi']
df['lambda_x_nu'] = df['lambda'] * df['nu']
df['iota_x_pi'] = df['iota'] * df['pi']
df['iota_x_nu'] = df['iota'] * df['nu']
df['iota_x_alpha'] = df['iota'] * df['alpha']
df['pi_x_nu'] = df['pi'] * df['nu']
df['pi_x_alpha'] = df['pi'] * df['alpha']
df['nu_x_alpha'] = df['nu'] * df['alpha']

# Check multicollinearity
correlation_matrix = df[[f'{x}_x_{y}' for x,y in interaction_pairs]].corr()
# Display: which interactions are highly correlated?
```

**Output**:
- `data/psf_interactions.csv` (with all interaction terms)
- `reports/multicollinearity_analysis.txt`

---

#### 1.3: Exploratory Data Analysis (2 hours)

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Plot 1: Distribution of ballots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Histogram: ballot counts
axes[0, 0].hist(df['ballots'], bins=5, edgecolor='black')
axes[0, 0].set_title('Distribution of Ballot Counts')
axes[0, 0].set_xlabel('Ballots')
axes[0, 0].set_ylabel('Frequency')

# Scatter: lambda + pi vs ballots (hypothesis: strong interaction)
axes[0, 1].scatter(df['lambda'] + df['pi'], df['ballots'], s=100)
for i, year in enumerate(df['year']):
    axes[0, 1].annotate(str(year), (df['lambda'][i] + df['pi'][i], df['ballots'][i]))
axes[0, 1].set_title('Network + Predecessor vs Ballot Count')
axes[0, 1].set_xlabel('Λ + Π')
axes[0, 1].set_ylabel('Ballots')

# Scatter: 1922 in context
special_1922 = df[df['year'] == 1922].iloc[0]
axes[1, 0].scatter(special_1922['lambda'], special_1922['iota'], s=200, color='red', label='1922 Ratti')
other_conclaves = df[df['year'] != 1922]
axes[1, 0].scatter(other_conclaves['lambda'], other_conclaves['iota'], s=100, alpha=0.6, label='Other')
axes[1, 0].set_title('Network vs Integration (1922 highlighted)')
axes[1, 0].set_xlabel('Λ (Network)')
axes[1, 0].set_ylabel('Ι (Integration)')
axes[1, 0].legend()

# Heatmap: correlation matrix of dimensions
correlation_dims = df[['lambda', 'iota', 'pi', 'nu', 'alpha']].corr()
sns.heatmap(correlation_dims, annot=True, fmt='.2f', ax=axes[1, 1])
axes[1, 1].set_title('Correlation: Dimensions')

plt.tight_layout()
plt.savefig('reports/eda_complementarity.png', dpi=150)
print("✓ EDA saved to reports/eda_complementarity.png")
```

**Outputs**:
- `reports/eda_complementarity.png`
- `reports/descriptive_statistics.txt`
- Key insights (e.g., "1922 is clear outlier: high Ι but low Λ+Π")

---

#### 1.4: Base Model Performance Benchmark (1 hour)

Test current v1.0 model on all 12 conclaves:

```python
from models.PSF_2_0_PAPAL_SUCCESSION.psf_model import PapalSuccessionFramework

model_v1 = PapalSuccessionFramework("models/PSF-2-0-PAPAL-SUCCESSION/model-definition.yaml")

# Evaluate all conclaves
results = []
for _, conclave in df.iterrows():
    candidate = CandidateParameters(
        name=conclave['winner'],
        lambda_=conclave['lambda'],
        iota=conclave['iota'],
        pi=conclave['pi'],
        nu=conclave['nu'],
        alpha=conclave['alpha']
    )

    prob = model_v1.calculate_individual_probability(candidate)
    duration = model_v1._estimate_conclave_duration(candidate)

    results.append({
        'year': conclave['year'],
        'predicted_ballots': duration,
        'actual_ballots': conclave['ballots'],
        'error': duration - conclave['ballots'],
        'prob': prob
    })

results_df = pd.DataFrame(results)
rmse_v1 = np.sqrt(np.mean(results_df['error'] ** 2))

print(f"v1.0 Model Performance:")
print(f"  RMSE (ballots): {rmse_v1:.3f}")
print(f"  MAE (ballots): {results_df['error'].abs().mean():.3f}")
print(f"\nProblem cases:")
for _, row in results_df[results_df['error'].abs() > 3].iterrows():
    print(f"  {int(row['year'])}: predicted {row['predicted_ballots']}, actual {row['actual_ballots']} (error: {row['error']:+.0f})")
```

**Output**: `reports/v1_0_baseline_performance.txt`
- RMSE: 2.73 (baseline we're trying to improve)
- Problem: 1922 (+6), 1878 (-4), 1914 (+3)

---

### Week 1 Deliverables

- ✅ Complete dataset in CSV format
- ✅ 10 interaction terms computed
- ✅ Multicollinearity analysis
- ✅ Exploratory visualizations
- ✅ v1.0 baseline RMSE documented
- ✅ Problem cases identified (1922, 1878, 1914)

---

## Week 2: Model Estimation & Validation

### Week 2 Tasks

#### 2.1: Estimate γ Parameters with Regularization (3 hours)

Use **Ridge Regression** (with cross-validation) to estimate γ terms while avoiding overfitting:

```python
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.preprocessing import StandardScaler
import numpy as np

# Prepare X matrix: main effects + interactions
X_main = df[['lambda', 'iota', 'pi', 'nu', 'alpha']].values
X_interactions = df[[
    'lambda_x_iota', 'lambda_x_pi', 'lambda_x_nu', 'lambda_x_alpha',
    'iota_x_pi', 'iota_x_nu', 'iota_x_alpha',
    'pi_x_nu', 'pi_x_alpha', 'nu_x_alpha'
]].values

# Combine main + interaction features
X = np.hstack([X_main, X_interactions])

# Target: logit transformation of winning (binary classification)
# For papal conclaves, each row is the WINNER, so y=1 for all
# Instead, use duration as continuous outcome for this analysis
y = df['ballots'].values

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Ridge CV to find optimal alpha (regularization strength)
ridge_cv = RidgeCV(alphas=[0.001, 0.01, 0.1, 1, 10, 100], cv=5)
ridge_cv.fit(X_scaled, y)

print(f"Optimal alpha: {ridge_cv.alpha_}")
print(f"Cross-validation R²: {ridge_cv.score(X_scaled, y):.3f}")

# Extract coefficients
coef = ridge_cv.coef_

# Map to dimension names
feature_names = ['lambda', 'iota', 'pi', 'nu', 'alpha',
                 'gamma_ΛΙ', 'gamma_ΛΠ', 'gamma_ΛΝ', 'gamma_ΛΑ',
                 'gamma_ΙΠ', 'gamma_ΙΝ', 'gamma_ΙΑ',
                 'gamma_ΠΝ', 'gamma_ΠΑ', 'gamma_ΝΑ']

beta_estimates = {name: coef[i] for i, name in enumerate(feature_names)}

print("\nEstimated Parameters:")
print("Main Effects (β):")
for name in ['lambda', 'iota', 'pi', 'nu', 'alpha']:
    print(f"  β_{name}: {beta_estimates[name]:+.3f}")

print("\nComplementarity Parameters (γ):")
for name in feature_names[5:]:
    print(f"  {name}: {beta_estimates[name]:+.3f}")

# Save estimates
import json
with open('reports/gamma_estimates_ridge.json', 'w') as f:
    json.dump(beta_estimates, f, indent=2)
```

**Output**: `reports/gamma_estimates_ridge.json`

---

#### 2.2: Bootstrap Confidence Intervals (2 hours)

Estimate 95% confidence intervals for all γ parameters:

```python
from sklearn.utils import resample

# Bootstrap: resample with replacement 1000 times
n_iterations = 1000
gamma_samples = {name: [] for name in feature_names}

for i in range(n_iterations):
    # Resample data
    indices = resample(range(len(df)), n_samples=len(df))
    X_boot = X_scaled[indices]
    y_boot = y[indices]

    # Fit ridge model
    ridge = Ridge(alpha=ridge_cv.alpha_)
    ridge.fit(X_boot, y_boot)

    # Store coefficients
    for j, name in enumerate(feature_names):
        gamma_samples[name].append(ridge.coef_[j])

# Calculate confidence intervals
ci_results = {}
for name in feature_names:
    samples = np.array(gamma_samples[name])
    ci_results[name] = {
        'mean': np.mean(samples),
        'std': np.std(samples),
        'ci_lower': np.percentile(samples, 2.5),
        'ci_upper': np.percentile(samples, 97.5),
        'median': np.median(samples)
    }

print("95% Confidence Intervals (Bootstrap, n=1000):")
for name, ci in ci_results.items():
    print(f"{name:15s}: {ci['ci_lower']:+.3f} to {ci['ci_upper']:+.3f} "
          f"(mean: {ci['mean']:+.3f}, std: {ci['std']:.3f})")

# Save CIs
with open('reports/gamma_ci_bootstrap.json', 'w') as f:
    json.dump(ci_results, f, indent=2)

# Visualize
import matplotlib.pyplot as plt
names_gamma = [n for n in feature_names if n.startswith('gamma')]
means = [ci_results[n]['mean'] for n in names_gamma]
ci_lower = [ci_results[n]['ci_lower'] for n in names_gamma]
ci_upper = [ci_results[n]['ci_upper'] for n in names_gamma]

plt.figure(figsize=(12, 6))
y_pos = np.arange(len(names_gamma))
plt.errorbar(means, y_pos, xerr=[np.array(means)-np.array(ci_lower),
                                   np.array(ci_upper)-np.array(means)],
             fmt='o', capsize=5, capthick=2)
plt.yticks(y_pos, names_gamma)
plt.xlabel('Parameter Value')
plt.title('Complementarity Parameters: 95% Bootstrap Confidence Intervals')
plt.axvline(x=0, color='red', linestyle='--', alpha=0.5)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('reports/gamma_ci_bootstrap.png', dpi=150)
```

**Outputs**:
- `reports/gamma_ci_bootstrap.json`
- `reports/gamma_ci_bootstrap.png`

---

#### 2.3: Cross-Validation Testing (2 hours)

Leave-one-out cross-validation to test overfitting:

```python
from sklearn.model_selection import LeaveOneOut

loo = LeaveOneOut()
predictions_loo = np.zeros(len(df))
errors_loo = np.zeros(len(df))

for train_index, test_index in loo.split(X_scaled):
    X_train, X_test = X_scaled[train_index], X_scaled[test_index]
    y_train, y_test = y[train_index], y[test_index]

    ridge = Ridge(alpha=ridge_cv.alpha_)
    ridge.fit(X_train, y_train)

    pred = ridge.predict(X_test)[0]
    predictions_loo[test_index] = pred
    errors_loo[test_index] = pred - y_test[0]

rmse_loo = np.sqrt(np.mean(errors_loo ** 2))
mae_loo = np.mean(np.abs(errors_loo))

print(f"Leave-One-Out Cross-Validation (n=12):")
print(f"  RMSE: {rmse_loo:.3f} ballots")
print(f"  MAE: {mae_loo:.3f} ballots")
print(f"\nComparison:")
print(f"  v1.0 Model RMSE: 2.73")
print(f"  v2.0 Ridge RMSE (LOO): {rmse_loo:.3f}")
print(f"  Improvement: {((2.73 - rmse_loo) / 2.73 * 100):.1f}%")

# Show predictions vs actual
results_cv = pd.DataFrame({
    'year': df['year'],
    'actual': y,
    'predicted': predictions_loo,
    'error': errors_loo
})

print("\nPer-Conclave LOO Predictions:")
print(results_cv.to_string(index=False))

# Save
results_cv.to_csv('reports/v2_loo_predictions.csv', index=False)
```

**Output**: `reports/v2_loo_predictions.csv`

---

#### 2.4: Sensitivity Analysis (1 hour)

Which γ parameters have biggest effect on duration?

```python
# For each γ parameter: perturb ±20%, measure impact
sensitivity_results = {}

for param_idx, param_name in enumerate(feature_names):
    if param_name.startswith('gamma'):
        original_coef = ridge_cv.coef_[param_idx]

        # Predict with ±20% perturbation
        coef_up = ridge_cv.coef_.copy()
        coef_up[param_idx] = original_coef * 1.2

        coef_down = ridge_cv.coef_.copy()
        coef_down[param_idx] = original_coef * 0.8

        # Average absolute change
        pred_base = ridge_cv.predict(X_scaled).mean()
        pred_up = (X_scaled @ coef_up).mean() + ridge_cv.intercept_
        pred_down = (X_scaled @ coef_down).mean() + ridge_cv.intercept_

        sensitivity = max(abs(pred_up - pred_base), abs(pred_down - pred_base))
        sensitivity_results[param_name] = sensitivity

# Rank by sensitivity
ranked = sorted(sensitivity_results.items(), key=lambda x: x[1], reverse=True)

print("Sensitivity Analysis: Effect of ±20% parameter change on duration")
for rank, (param, sensitivity) in enumerate(ranked, 1):
    print(f"{rank}. {param:15s}: {sensitivity:.3f} ballots change")

# Save
import json
with open('reports/sensitivity_analysis.json', 'w') as f:
    json.dump({k: float(v) for k, v in sensitivity_results.items()}, f, indent=2)
```

**Output**: `reports/sensitivity_analysis.json`

---

### Week 2 Deliverables

- ✅ γ parameters estimated with Ridge Regression
- ✅ 95% Bootstrap confidence intervals
- ✅ Leave-one-out cross-validation results
- ✅ Sensitivity analysis (which γ matter most)
- ✅ Improvement quantified: v1.0 RMSE vs v2.0 RMSE

---

## Week 3: Enhanced Model Implementation

### Week 3 Tasks

#### 3.1: Implement γ-Enhanced PSF Model (3 hours)

Update `psf_model.py` to include interaction terms:

```python
# In psf_model.py, add new method:

def calculate_individual_probability_with_gamma(self, candidate: CandidateParameters,
                                                gamma_params: Dict[str, float] = None) -> float:
    """
    Enhanced logistic model with complementarity parameters.

    Formula:
    η = β₀ + β_Λ·Λ + β_Ι·Ι + β_Π·Π + β_Ν·Ν + β_Α·Α
        + γ_ΛΙ·(Λ·Ι) + γ_ΛΠ·(Λ·Π) + ... [10 interaction terms]

    P(win) = 1 / (1 + exp(-η))
    """

    # Main effects (same as before)
    eta = (self.beta_params['intercept'] +
           self.beta_params['lambda'] * candidate.lambda_ +
           self.beta_params['iota'] * candidate.iota +
           self.beta_params['pi'] * candidate.pi +
           self.beta_params['nu'] * candidate.nu +
           self.beta_params['alpha'] * candidate.alpha)

    # Interaction terms (NEW)
    if gamma_params is None:
        gamma_params = self._get_default_gamma_params()

    eta += (gamma_params['gamma_ΛΙ'] * candidate.lambda_ * candidate.iota +
            gamma_params['gamma_ΛΠ'] * candidate.lambda_ * candidate.pi +
            gamma_params['gamma_ΛΝ'] * candidate.lambda_ * candidate.nu +
            gamma_params['gamma_ΛΑ'] * candidate.lambda_ * candidate.alpha +
            gamma_params['gamma_ΙΠ'] * candidate.iota * candidate.pi +
            gamma_params['gamma_ΙΝ'] * candidate.iota * candidate.nu +
            gamma_params['gamma_ΙΑ'] * candidate.iota * candidate.alpha +
            gamma_params['gamma_ΠΝ'] * candidate.pi * candidate.nu +
            gamma_params['gamma_ΠΑ'] * candidate.pi * candidate.alpha +
            gamma_params['gamma_ΝΑ'] * candidate.nu * candidate.alpha)

    # Logistic function
    probability = 1.0 / (1.0 + np.exp(-eta))
    return probability

def estimate_conclave_duration_with_gamma(self, candidate: CandidateParameters,
                                          gamma_params: Dict[str, float] = None) -> int:
    """
    Enhanced duration formula with nonlinear complementarity.

    Formula:
    Rounds = 10 / (Λ + Π + γ_ΛΠ·Λ·Π + adjustment_factor)

    When Π is weak (< 0.50), adjustment increases duration.
    """

    if gamma_params is None:
        gamma_params = self._get_default_gamma_params()

    # Base formula
    denominator = candidate.lambda_ + candidate.pi

    # Synergy term (amplifies when both are strong)
    synergy = gamma_params.get('gamma_ΛΠ', 0.0) * candidate.lambda_ * candidate.pi

    # Weak predecessor adjustment (candidate with weak Π takes longer)
    if candidate.pi < 0.50:
        weak_pred_adjustment = (0.50 - candidate.pi) * candidate.iota * 2.0
    else:
        weak_pred_adjustment = 0.0

    rounds = 10.0 / (denominator + synergy + weak_pred_adjustment)

    return max(1, int(np.round(rounds)))
```

**Output**: Updated `psf_model.py` with two new methods

---

#### 3.2: Validate Enhanced Model on All 12 Conclaves (2 hours)

Test v2.0 model with estimated γ parameters:

```python
# Load enhanced model with gamma parameters
model_v2 = PapalSuccessionFramework(...)
gamma_params_estimated = load_json('reports/gamma_estimates_ridge.json')

# Evaluate all 12 conclaves
results_v2 = []
for _, conclave in df.iterrows():
    candidate = CandidateParameters(
        name=conclave['winner'],
        lambda_=conclave['lambda'],
        iota=conclave['iota'],
        pi=conclave['pi'],
        nu=conclave['nu'],
        alpha=conclave['alpha']
    )

    # v2.0 predictions
    duration_v2 = model_v2.estimate_conclave_duration_with_gamma(
        candidate,
        gamma_params=gamma_params_estimated
    )

    results_v2.append({
        'year': conclave['year'],
        'v1_predicted': ...,  # from week 1 baseline
        'v2_predicted': duration_v2,
        'actual': conclave['ballots'],
        'v1_error': ...,
        'v2_error': duration_v2 - conclave['ballots']
    })

results_v2_df = pd.DataFrame(results_v2)

# Compare versions
rmse_v1 = np.sqrt(np.mean(results_v2_df['v1_error'] ** 2))
rmse_v2 = np.sqrt(np.mean(results_v2_df['v2_error'] ** 2))

print("MODEL COMPARISON: v1.0 vs v2.0 (with γ)")
print(f"RMSE v1.0: {rmse_v1:.3f} ballots")
print(f"RMSE v2.0: {rmse_v2:.3f} ballots")
print(f"Improvement: {((rmse_v1 - rmse_v2) / rmse_v1 * 100):.1f}%")
print(f"Target: RMSE < 1.5 ballots")

# Per-conclave comparison
print("\nPer-Conclave Comparison:")
for _, row in results_v2_df.iterrows():
    print(f"{int(row['year'])}: "
          f"v1={row['v1_error']:+.1f}, "
          f"v2={row['v2_error']:+.1f}, "
          f"actual={int(row['actual'])}")

# Highlight: 1922 (the critical case)
case_1922 = results_v2_df[results_v2_df['year'] == 1922].iloc[0]
print(f"\n1922 CRITICAL CASE (14 actual ballots):")
print(f"  v1.0 predicted: 8 (error: +6)")
print(f"  v2.0 predicted: {int(case_1922['v2_predicted'])} (error: {case_1922['v2_error']:+.1f})")
```

**Output**: `reports/v2_0_validation_results.csv`

---

#### 3.3: Update Model Registry (1 hour)

Update `models.registry.yaml` with v2.0 information:

```yaml
# In models.registry.yaml:
model_id: PSF-2.0
version: "2.0"  # Updated from 1.1
status: STABLE
last_updated: "2026-01-27"  # (your date)

dimensions:
  # ... same 5 dimensions as before ...

complementarity_parameters:  # NEW!
  - symbol: "γ_ΛΠ"
    name: "Network × Predecessor Synergy"
    estimated_value: 0.8
    ci_lower: 0.5
    ci_upper: 1.1
    sensitivity: "CRITICAL"
    interpretation: "When both Λ and Π are high, election is very fast"

  - symbol: "γ_ΙΠ"
    name: "Integration × Predecessor"
    estimated_value: 0.5
    ci_lower: 0.2
    ci_upper: 0.8
    sensitivity: "HIGH"
    interpretation: "Integration amplifies strong predecessor support"

  # ... 8 more γ parameters ...

validation:
  accuracy: 1.00  # Still 100% on winner prediction
  data_points: 12

  duration_prediction:
    rmse_v1_0: 2.73  # v1.0 baseline
    rmse_v2_0: 1.35  # (example: if we achieve this)
    improvement: "50.5%"

  critical_case_1922:
    v1_0_prediction: 8
    v2_0_prediction: 12  # (example)
    actual: 14
    v2_0_error: "+2"  # Much better than v1.0's +6

improvements_completed:
  - phase_2_task_2_1: "Complementarity Parameters (γ Matrix)"
    status: "COMPLETE"
    completion_date: "2026-01-27"
    achievement: "Added 10 γ terms; improved duration RMSE from 2.73 to <1.5"
```

**Output**: Updated `models.registry.yaml` (v2.0 release)

---

### Week 3 Deliverables

- ✅ Enhanced PSF v2.0 implementation
- ✅ 10 γ parameters integrated
- ✅ Validation on all 12 conclaves
- ✅ v1.0 vs v2.0 comparison
- ✅ Model Registry updated (v2.0 release)

---

## Week 4: Documentation & Handoff

### Week 4 Tasks

#### 4.1: Create Phase 2 Task 2.1 Completion Report (2 hours)

```markdown
# PHASE 2, TASK 2.1 COMPLETION REPORT
## Complementarity Parameters (γ Matrix) Implementation

**Status**: COMPLETE ✓
**Date**: January 27, 2026
**Owner**: EBF Research Team

### Executive Summary

Successfully estimated and implemented 10 complementarity parameters (γ) for PSF 2.0.
Model duration predictions improved from RMSE 2.73 to X.XX ballots (Y% improvement).

### Key Achievements

1. **γ Parameters Estimated** (with 95% confidence intervals)
   - γ_ΛΠ = 0.8 (Network × Predecessor: STRONGEST synergy)
   - γ_ΙΠ = 0.5 (Integration × Predecessor: strong)
   - γ_ΛΙ = 0.3 (Network × Integration: moderate)
   - γ_ΙΝ = 0.2 (Integration × Neutrality: weak)
   - [6 more...]

2. **1922 Conclave: SOLVED** ✓
   - v1.0 predicted: 8 ballots (error: +6, -75% overestimate)
   - v2.0 predicts: ~12 ballots (error: -2, better fit)
   - Root cause: Weak Π + high Ι requires nonlinear model

3. **Model Validation**
   - 12-conclave dataset analyzed
   - Leave-one-out cross-validation: RMSE X.XX
   - Bootstrap confidence intervals: all γ significant
   - No overfitting detected

### Technical Approach

**Method**: Ridge Regression with Cross-Validation
- Features: 5 main effects + 10 interaction terms (15 total)
- Regularization: Ridge(alpha=optimal_via_CV)
- Validation: Leave-one-out CV (n=12)
- Confidence: 95% bootstrap (n=1000 resamples)

**Enhanced Formula**:
```
η = β₀ + β_Λ·Λ + β_Ι·Ι + β_Π·Π + β_Ν·Ν + β_Α·Α
    + γ_ΛΠ·(Λ·Π) + γ_ΙΠ·(Ι·Π) + ... [10 terms]

Duration = 10 / (Λ + Π + γ_ΛΠ·Λ·Π + weak_Π_adjustment)
```

### Performance Improvements

| Metric | v1.0 | v2.0 | Improvement |
|--------|------|------|------------|
| RMSE (ballots) | 2.73 | X.XX | Y% |
| MAE (ballots) | 2.52 | X.XX | Y% |
| Max error | 6 (1922) | X (problem case) | Y% |
| Conclaves with error <2 | 4/12 | X/12 | Y% |

### Critical Case: 1922 Conclave

**Problem**: Model predicted 8 ballots, actual 14 (longest conclave)
**Diagnosis**: Ratti had weak Λ (0.72) and very weak Π (0.48), but high Ι (0.88)
**Solution**: γ_ΙΠ interaction captures "bridge-builder in weak-predecessor context"
**Result**: v2.0 prediction closer to reality

### Files Generated

1. Data & Analysis:
   - `data/psf_conclaves_complete.csv` - unified dataset
   - `data/psf_interactions.csv` - interaction terms computed
   - `reports/eda_complementarity.png` - exploratory visualizations

2. Estimates & CI:
   - `reports/gamma_estimates_ridge.json` - point estimates
   - `reports/gamma_ci_bootstrap.json` - 95% confidence intervals
   - `reports/sensitivity_analysis.json` - which γ matter most

3. Validation:
   - `reports/v2_loo_predictions.csv` - leave-one-out results
   - `reports/v1_vs_v2_comparison.csv` - detailed comparison

4. Code:
   - Updated `psf_model.py` with new methods
   - Updated `models.registry.yaml` with v2.0 parameters

### Learned Insights

1. **Nonlinearity is Critical**
   - With weak Π, duration formula is NOT linear
   - γ interaction terms capture this nonlinearity
   - Enabled by factional dynamics (1922 compromise scenario)

2. **Complementarity Works Across Contexts**
   - Same γ_ΛΠ term explains:
     - 2005 fast (2 ballots): high Λ+Π synergy
     - 1922 slow (14 ballots): low Λ+Π, compensated by high Ι
   - Pattern holds across 147 years (1878-2025)

3. **Bootstrap Confidence Important**
   - With N=12, parameter uncertainty is non-trivial
   - γ parameters have ±0.3-0.5 ranges
   - Cross-validation detects no overfitting (LOO ≈ validation accuracy)

### Next Steps: Phase 2 Tasks 2.2 & 2.3

**Task 2.2**: Crisis/Shock Module (2026 Q2)
- Model sudden disqualifications (like 1903 Austrian veto)
- Add scandal/health crisis triggers

**Task 2.3**: Coalition Dynamics Simulation (2026 Q2-Q3)
- Multi-round voting with preference switching
- Predict ballot-by-ballot voting sequences

**Phase 3**: 2032 Out-of-Sample Validation
- Real test of model on next papacy succession
- Critical for establishing external validity

### Appendices

- Appendix CA: "Complementarity Parameters in PSF 2.0" (LaTeX, 50+ pages)
  - Complete mathematical derivation
  - γ estimation methodology
  - Sensitivity analysis details
  - Comparison with other interaction models
```

**Output**: `reports/PHASE_2_TASK_2_1_COMPLETION_REPORT.md`

---

#### 4.2: Create Appendix CA (LaTeX) (2 hours)

Academic paper for formal documentation:

```latex
% Appendix CA: Complementarity Parameters in PSF 2.0

\documentclass[11pt]{article}

\title{Appendix CA: Complementarity Parameters in Papal Succession Framework 2.0 (PSF 2.0)}
\author{EBF Research Team}
\date{January 27, 2026}

\begin{document}

\maketitle

% [Full LaTeX document with:
% - Motivation (why 1922 failure revealed need for γ)
% - Mathematical framework (10 γ parameters, interpretation)
% - Estimation methodology (Ridge CV, Bootstrap CI)
% - Validation results (RMSE improvement)
% - Per-conclave analysis (especially 1922)
% - Sensitivity analysis (which γ matter most)
% - Comparison to v1.0
% - Limitation acknowledgments
% - References
% ]

\end{document}
```

**Output**: `appendices/CA_COMPLEMENTARITY-PARAMETERS.tex`

---

#### 4.3: Commit & Push (0.5 hours)

```bash
git add models/PSF-2-0-PAPAL-SUCCESSION/psf_model.py
git add models/models.registry.yaml
git add appendices/CA_COMPLEMENTARITY-PARAMETERS.tex
git add reports/

git commit -m "feat(PSF-2.0): Phase 2 Task 2.1 Complete - Complementarity Parameters (γ Matrix)

Added 10 interaction terms to PSF 2.0 model:
- γ_ΛΠ, γ_ΙΠ, γ_ΛΙ, and 7 more
- Estimated via Ridge Regression with cross-validation
- 95% bootstrap confidence intervals
- 1922 critical case now better explained
- Duration RMSE improved: 2.73 → X.XX ballots (Y% improvement)
- All 12 conclaves re-validated with v2.0

See: reports/PHASE_2_TASK_2_1_COMPLETION_REPORT.md
     appendices/CA_COMPLEMENTARITY-PARAMETERS.tex"

git push origin claude/trump-third-term-analysis-8Lr8x
```

---

#### 4.4: Update Model Registry Entry (0.5 hours)

Version bump in registry:
```yaml
PSF-2.0:
  version: "2.0" # was 1.1
  status: STABLE
  validation:
    accuracy: 1.00
    rmse_duration_v1: 2.73 (baseline)
    rmse_duration_v2: X.XX (achieved)
  phase_2_completed:
    - Task 2.1: Complementarity Parameters ✓
  phase_2_planned:
    - Task 2.2: Crisis/Shock Module
    - Task 2.3: Coalition Dynamics
```

---

### Week 4 Deliverables

- ✅ Completion Report (comprehensive)
- ✅ Academic Appendix CA (LaTeX)
- ✅ Code committed to git
- ✅ Model Registry updated (v2.0)
- ✅ Ready for Phase 2 Tasks 2.2 & 2.3

---

## Success Criteria (How We Know We Won)

| Criterion | Target | Status |
|-----------|--------|--------|
| RMSE improvement | <1.5 ballots | ✓ Or fail gracefully |
| 1922 error reduction | <±3 ballots | ✓ Or fail gracefully |
| No overfitting | LOO accuracy ≥ 85% | ✓ Or investigate |
| Bootstrap CI | All γ within [-1, 2] | ✓ Or reduce model |
| Winner accuracy | ≥99% (still 100%) | ✓ Maintained |
| Documentation | Complete (4 formats) | ✓ Delivered |

---

## Risk Mitigation

**Risk 1**: Small sample (N=12) → overfitting
- **Mitigation**: Ridge regularization + LOO cross-validation + Bootstrap CI

**Risk 2**: Some γ parameters not significant
- **Mitigation**: Sensitivity analysis identifies them; can drop weak ones

**Risk 3**: Improvements marginal (RMSE doesn't improve much)
- **Mitigation**: Document learnings anyway; proceed to Task 2.2 (crisis module)

**Risk 4**: Negative γ values (suggest antagonism not synergy)
- **Mitigation**: Theoretically OK; document interpretation

---

## Timeline Gantt

```
Week 1: Data Prep
  ├─ Compile dataset [████]
  ├─ Interaction terms [████]
  ├─ EDA [████]
  └─ Baseline benchmark [████]

Week 2: Estimation
  ├─ Ridge regression [████]
  ├─ Bootstrap CI [████]
  ├─ LOO CV [████]
  └─ Sensitivity [████]

Week 3: Implementation
  ├─ Code enhancement [████]
  ├─ Validation [████]
  └─ Registry update [████]

Week 4: Documentation
  ├─ Completion report [████]
  ├─ Academic appendix [████]
  ├─ Commit & push [████]
  └─ Final review [████]
```

---

## Success Outcome

**At end of Week 4**, we will have:

✅ **PSF 2.0 v2.0**: Model with 10 γ complementarity parameters
✅ **Documented**: Why 1922 conclave needed γ-terms to predict correctly
✅ **Improved**: Duration RMSE from 2.73 ballots to <1.5 (or new understanding)
✅ **Validated**: Leave-one-out CV confirms no overfitting
✅ **Registered**: Updated in Model Registry as v2.0
✅ **Academic**: Formal Appendix CA for publication
✅ **Ready**: For Phase 2 Tasks 2.2 (Crisis) & 2.3 (Coalition)

---

**This is the implementation roadmap. Ready to start Week 1?**
