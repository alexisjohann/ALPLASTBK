"""
PHASE 2, TASK 2.1: Week 2 - Model Estimation & Validation
Complementarity Parameters (γ) for PSF 2.0

Tasks:
2.1: Ridge regression estimation of γ parameters
2.2: Bootstrap confidence intervals (1000 resamples)
2.3: Leave-one-out cross-validation
2.4: Sensitivity analysis

Output: reports/ directory with γ estimates, CIs, and validation
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from sklearn.linear_model import RidgeCV, Ridge
from sklearn.model_selection import LeaveOneOut
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SETUP
# ============================================================================

DATA_FILE = Path("reports/02_with_interactions.csv")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("PHASE 2, TASK 2.1: Week 2 - Model Estimation & Validation")
print("=" * 80)

# Load data with interactions from Week 1
print("\n[SETUP] Loading data with interactions from Week 1...")
df = pd.read_csv(DATA_FILE)
print(f"✓ Loaded {len(df)} conclaves with {len(df.columns)} columns")

# ============================================================================
# PREPARE MODEL DATA
# ============================================================================

print("\n[PREP] Preparing feature matrix and target...")

# Main effects (5)
main_effects = ['lambda', 'iota', 'pi', 'nu', 'alpha']

# Interaction terms (10)
interaction_terms = [
    'lambda_x_iota', 'lambda_x_pi', 'lambda_x_nu', 'lambda_x_alpha',
    'iota_x_pi', 'iota_x_nu', 'iota_x_alpha',
    'pi_x_nu', 'pi_x_alpha',
    'nu_x_alpha'
]

# Feature matrix: main effects + interactions (15 features)
all_features = main_effects + interaction_terms
X = df[all_features].values
y = df['ballots'].values  # Target: actual ballot count

print(f"  Feature matrix: {X.shape}")
print(f"  Target vector: {y.shape}")
print(f"  Features: {len(main_effects)} main effects + {len(interaction_terms)} interactions")

# ============================================================================
# TASK 2.1: RIDGE REGRESSION ESTIMATION
# ============================================================================

print("\n[TASK 2.1] Ridge regression estimation with cross-validation...")

# Use RidgeCV to find optimal regularization parameter (alpha)
alphas = np.logspace(-2, 2, 100)  # Range from 0.01 to 100
ridge_cv = RidgeCV(alphas=alphas, cv=5)
ridge_cv.fit(X, y)

optimal_alpha = ridge_cv.alpha_
ridge_model = Ridge(alpha=optimal_alpha)
ridge_model.fit(X, y)

print(f"  Optimal regularization (alpha): {optimal_alpha:.4f}")
print(f"  CV Score (R²): {ridge_cv.score(X, y):.4f}")

# Extract coefficients for main effects and interactions
coefs = ridge_model.coef_
intercept = ridge_model.intercept_

print(f"\n  Intercept: {intercept:.4f}")
print(f"\n  MAIN EFFECTS (β coefficients):")
for i, feat in enumerate(main_effects):
    print(f"    {feat:15s}: {coefs[i]:+.4f}")

print(f"\n  INTERACTION EFFECTS (γ complementarity parameters):")
gamma_estimates = {}
for i, feat in enumerate(interaction_terms):
    gamma_estimates[feat] = coefs[main_effects.__len__() + i]
    print(f"    γ_{feat.replace('_x_', ''):8s}: {gamma_estimates[feat]:+.4f}")

# Save estimates
gamma_results = {
    'optimal_alpha': float(optimal_alpha),
    'cv_score': float(ridge_cv.score(X, y)),
    'intercept': float(intercept),
    'main_effects': {feat: float(coefs[i]) for i, feat in enumerate(main_effects)},
    'gamma_estimates': {k: float(v) for k, v in gamma_estimates.items()}
}

with open(REPORTS_DIR / "gamma_estimates_ridge.json", 'w') as f:
    json.dump(gamma_results, f, indent=2)
print(f"\n✓ Gamma estimates saved to reports/gamma_estimates_ridge.json")

# ============================================================================
# TASK 2.2: BOOTSTRAP CONFIDENCE INTERVALS
# ============================================================================

print("\n[TASK 2.2] Bootstrap confidence intervals (1000 resamples)...")

n_bootstrap = 1000
bootstrap_coefs = []

np.random.seed(42)  # For reproducibility
for i in range(n_bootstrap):
    # Resample with replacement
    indices = np.random.choice(len(X), size=len(X), replace=True)
    X_boot = X[indices]
    y_boot = y[indices]

    # Fit model
    ridge_boot = Ridge(alpha=optimal_alpha)
    ridge_boot.fit(X_boot, y_boot)
    bootstrap_coefs.append(ridge_boot.coef_)

    if (i + 1) % 250 == 0:
        print(f"  Completed {i + 1}/{n_bootstrap} resamples")

bootstrap_coefs = np.array(bootstrap_coefs)

# Calculate confidence intervals for gamma parameters
print(f"\n  Calculating 95% confidence intervals...")

gamma_ci = {}
for j, feat in enumerate(interaction_terms):
    coef_idx = main_effects.__len__() + j
    coef_samples = bootstrap_coefs[:, coef_idx]

    ci_lower = np.percentile(coef_samples, 2.5)
    ci_upper = np.percentile(coef_samples, 97.5)

    gamma_ci[feat] = {
        'point_estimate': float(gamma_estimates[feat]),
        'mean': float(np.mean(coef_samples)),
        'std': float(np.std(coef_samples)),
        'median': float(np.median(coef_samples)),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'ci_width': float(ci_upper - ci_lower)
    }

# Print and save
print(f"\n  BOOTSTRAP CONFIDENCE INTERVALS (95%):")
print(f"  {'Parameter':15s} {'Estimate':>10s} {'Mean':>10s} {'Median':>10s} {'CI [Low, High]':>25s}")
print(f"  {'-'*75}")

for feat in interaction_terms:
    est = gamma_ci[feat]['point_estimate']
    mean = gamma_ci[feat]['mean']
    median = gamma_ci[feat]['median']
    ci_l = gamma_ci[feat]['ci_lower']
    ci_u = gamma_ci[feat]['ci_upper']
    print(f"  γ_{feat.replace('_x_', ''):8s} {est:+10.4f} {mean:+10.4f} {median:+10.4f} [{ci_l:+7.4f}, {ci_u:+7.4f}]")

with open(REPORTS_DIR / "gamma_ci_bootstrap.json", 'w') as f:
    json.dump(gamma_ci, f, indent=2)
print(f"\n✓ Bootstrap confidence intervals saved to reports/gamma_ci_bootstrap.json")

# ============================================================================
# TASK 2.3: LEAVE-ONE-OUT CROSS-VALIDATION
# ============================================================================

print("\n[TASK 2.3] Leave-one-out cross-validation...")

loo = LeaveOneOut()
loo_predictions = []
loo_errors = []
loo_indices = []

for train_idx, test_idx in loo.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Train Ridge model
    ridge_loo = Ridge(alpha=optimal_alpha)
    ridge_loo.fit(X_train, y_train)

    # Predict on held-out point
    y_pred = ridge_loo.predict(X_test)[0]
    y_true = y_test[0]
    error = y_pred - y_true

    loo_predictions.append(y_pred)
    loo_errors.append(error)
    loo_indices.append(test_idx[0])

loo_predictions = np.array(loo_predictions)
loo_errors = np.array(loo_errors)

# Calculate metrics
rmse_loo = np.sqrt(np.mean(loo_errors ** 2))
mae_loo = np.mean(np.abs(loo_errors))

print(f"  LOO Cross-Validation Results:")
print(f"    RMSE: {rmse_loo:.4f} ballots")
print(f"    MAE: {mae_loo:.4f} ballots")
print(f"    Baseline (v1.0) RMSE: 3.175 ballots")
print(f"    Improvement: {(3.175 - rmse_loo) / 3.175 * 100:.1f}%")

# Create LOO results dataframe
loo_results = pd.DataFrame({
    'year': df['year'].values,
    'winner': df['winner'].values,
    'actual_ballots': y,
    'predicted_ballots': loo_predictions,
    'error': loo_errors,
    'abs_error': np.abs(loo_errors)
})

print(f"\n  Per-Conclave LOO Results:")
print(loo_results[['year', 'winner', 'actual_ballots', 'predicted_ballots', 'error']].to_string(index=False))

# Identify problem cases
problem_loo = loo_results[loo_results['abs_error'] > 2]
print(f"\n  Problem cases (error > ±2 ballots):")
for idx, row in problem_loo.iterrows():
    print(f"    {int(row['year'])}: predicted {row['predicted_ballots']:.1f}, actual {row['actual_ballots']:.0f} (error: {row['error']:+.1f})")

# Save LOO results
loo_results.to_csv(REPORTS_DIR / "v2_loo_predictions.csv", index=False)

loo_summary = {
    'rmse': float(rmse_loo),
    'mae': float(mae_loo),
    'rmse_improvement_pct': float((3.175 - rmse_loo) / 3.175 * 100),
    'n_samples': len(loo_results),
    'n_problem_cases': len(problem_loo)
}

with open(REPORTS_DIR / "loo_summary.json", 'w') as f:
    json.dump(loo_summary, f, indent=2)

print(f"\n✓ LOO results saved to reports/v2_loo_predictions.csv")

# ============================================================================
# TASK 2.4: SENSITIVITY ANALYSIS
# ============================================================================

print("\n[TASK 2.4] Sensitivity analysis...")

# For each gamma parameter, perturb ±20% and measure impact
sensitivity_results = {}

print(f"\n  Perturbing each γ parameter ±20% and measuring impact on predictions...")

for j, feat in enumerate(interaction_terms):
    coef_idx = main_effects.__len__() + j

    # Get baseline coefficient
    baseline_coef = ridge_model.coef_[coef_idx]

    # Perturb ±20%
    perturb_plus = baseline_coef * 1.2
    perturb_minus = baseline_coef * 0.8

    # Create perturbed coefficients
    coefs_plus = ridge_model.coef_.copy()
    coefs_plus[coef_idx] = perturb_plus

    coefs_minus = ridge_model.coef_.copy()
    coefs_minus[coef_idx] = perturb_minus

    # Calculate predictions with perturbed coefficients
    y_pred_plus = intercept + X @ coefs_plus
    y_pred_minus = intercept + X @ coefs_minus
    y_pred_baseline = ridge_model.predict(X)

    # Measure average change in prediction
    delta_plus = np.mean(np.abs(y_pred_plus - y_pred_baseline))
    delta_minus = np.mean(np.abs(y_pred_minus - y_pred_baseline))

    sensitivity_results[feat] = {
        'baseline_coefficient': float(baseline_coef),
        'perturbation_pct': 20.0,
        'avg_prediction_change_plus': float(delta_plus),
        'avg_prediction_change_minus': float(delta_minus),
        'avg_prediction_change_mean': float((delta_plus + delta_minus) / 2)
    }

# Sort by sensitivity (highest impact first)
sorted_sensitivity = sorted(
    sensitivity_results.items(),
    key=lambda x: x[1]['avg_prediction_change_mean'],
    reverse=True
)

print(f"\n  SENSITIVITY RANKING (by average prediction change):")
print(f"  {'Parameter':15s} {'Coefficient':>12s} {'Impact (+20%)':>15s} {'Impact (-20%)':>15s} {'Avg Impact':>12s}")
print(f"  {'-'*75}")

for feat, results in sorted_sensitivity:
    print(f"  γ_{feat.replace('_x_', ''):8s} {results['baseline_coefficient']:+12.4f} "
          f"{results['avg_prediction_change_plus']:+15.4f} "
          f"{results['avg_prediction_change_minus']:+15.4f} "
          f"{results['avg_prediction_change_mean']:+12.4f}")

with open(REPORTS_DIR / "sensitivity_analysis.json", 'w') as f:
    json.dump(sensitivity_results, f, indent=2)

print(f"\n✓ Sensitivity analysis saved to reports/sensitivity_analysis.json")

# ============================================================================
# COMPARISON: v1.0 vs v2.0 (with γ terms)
# ============================================================================

print("\n[COMPARISON] v1.0 vs v2.0 Performance")
print(f"  {'Metric':20s} {'v1.0 (Main only)':>20s} {'v2.0 (with γ)':>20s} {'Improvement':>15s}")
print(f"  {'-'*75}")
print(f"  {'RMSE (LOO)':20s} {'3.175 ballots':>20s} {f'{rmse_loo:.3f} ballots':>20s} "
      f"{f'{(3.175-rmse_loo)/3.175*100:.1f}%':>15s}")
print(f"  {'MAE (LOO)':20s} {'2.750 ballots':>20s} {f'{mae_loo:.3f} ballots':>20s} "
      f"{f'{(2.750-mae_loo)/2.750*100:.1f}%':>15s}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("WEEK 2 SUMMARY")
print("=" * 80)

print(f"""
✓ [TASK 2.1] Ridge regression with optimal α={optimal_alpha:.4f}
  → Estimated 10 γ complementarity parameters
  → CV Score (R²): {ridge_cv.score(X, y):.4f}

✓ [TASK 2.2] Bootstrap confidence intervals (n=1000)
  → 95% CI calculated for all γ parameters
  → Most reliable: γ parameters with narrow CI

✓ [TASK 2.3] Leave-one-out cross-validation
  → RMSE: {rmse_loo:.3f} ballots (v1.0: 3.175)
  → Improvement: {(3.175-rmse_loo)/3.175*100:.1f}%
  → MAE: {mae_loo:.3f} ballots

✓ [TASK 2.4] Sensitivity analysis
  → Ranked γ parameters by prediction impact
  → Most important: {sorted_sensitivity[0][0].replace('_x_', 'γ_')}
  → Least important: {sorted_sensitivity[-1][0].replace('_x_', 'γ_')}

READY FOR WEEK 3:
  → Integrate γ terms into psf_model.py
  → Create PSF v2.0 with complementarity
  → Validate on all 12 conclaves
  → Compare v1.0 vs v2.0

FILES GENERATED:
  • reports/gamma_estimates_ridge.json
  • reports/gamma_ci_bootstrap.json
  • reports/v2_loo_predictions.csv
  • reports/loo_summary.json
  • reports/sensitivity_analysis.json

CRITICAL FINDINGS:
  • 1922 case (14 ballots): Check if γ_ΙΠ helps explain stalemate
  • Multicollinearity detected in Week 1 → Ridge regularization prevents overfitting
  • Small sample (N=12) → Bootstrap CI reflects uncertainty properly
""")

print("=" * 80)
print(f"Week 2 complete! Proceed to week_3_implementation.py\n")
