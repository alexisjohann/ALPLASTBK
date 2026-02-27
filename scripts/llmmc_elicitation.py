#!/usr/bin/env python3
"""
LLMMC Elicitation Pipeline (E1–E3): GPT-4o as Measurement Instrument.

Implements the operational epistemic chain for LLMMC prior generation:
  E1: Elicitation Design — structured prompt for parameter estimation
  E2: Repeated Measurement — N independent draws with temperature > 0
  E3: Aggregation — mean, std, distribution diagnostics

Architecture (Three-Layer compliant):
  GPT-4o (external LLM) = Measurement Instrument
  Python (this script)   = Layer 1 (formal computation)
  YAML output            = Layer 2 (parameter store)
  Claude                 = Layer 3 (translation only)

Usage:
    # Single parameter elicitation
    python scripts/llmmc_elicitation.py --param PAR-BEH-001

    # With specific context
    python scripts/llmmc_elicitation.py --param PAR-BEH-001 \\
        --context "Swiss retirees replacing heating systems"

    # All behavioral parameters
    python scripts/llmmc_elicitation.py --all-behavioral

    # Custom parameter (not in registry)
    python scripts/llmmc_elicitation.py \\
        --symbol "alpha_trust" \\
        --description "Trust propensity in institutional context" \\
        --bounds 0.0 1.0

    # Dry run (show prompts without API calls)
    python scripts/llmmc_elicitation.py --param PAR-BEH-001 --dry-run

Environment:
    OPENAI_API_KEY  — Required (or set in .env file)
"""

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

DEFAULT_MODEL = "gpt-4o"
DEFAULT_N_DRAWS = 15       # E2: number of independent draws
DEFAULT_TEMPERATURE = 0.8  # Higher = more variance between draws
DEFAULT_MAX_TOKENS = 512
RETRY_ATTEMPTS = 3
RETRY_DELAY_BASE = 2.0     # Exponential backoff base (seconds)

SYSTEM_PROMPT = """You are a behavioral economics research assistant specializing in parameter estimation.

Your task: Estimate a specific behavioral parameter value based on the scientific literature and the given context.

RULES:
1. Provide a SINGLE numerical point estimate
2. Provide a 90% confidence interval [low, high]
3. Base your estimate on published empirical research
4. Consider the specific context provided
5. If the parameter has known bounds (e.g., [0,1] for probabilities), respect them
6. Respond ONLY in the JSON format specified — no commentary

Your response must be valid JSON, nothing else."""

ELICITATION_TEMPLATE = """Estimate the following behavioral parameter:

**Parameter:** {symbol} — {name}
**Description:** {description}
{bounds_line}
{context_line}
{anchor_line}

Respond with ONLY this JSON (no markdown, no explanation):
{{"estimate": <float>, "ci_low": <float>, "ci_high": <float>, "confidence": <float 0-1>, "reasoning_keywords": [<3-5 keywords>]}}"""


# ──────────────────────────────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────────────────────────────

@dataclass
class ParameterSpec:
    """Specification for a parameter to elicit."""
    id: str                          # PAR-BEH-001 or custom
    symbol: str                      # λ, β, etc.
    name: str                        # Human-readable name
    description: str                 # What it measures
    bounds: Optional[Tuple[float, float]] = None  # e.g. (0, 1)
    literature_value: Optional[float] = None      # Tier 1/2 reference
    literature_ci: Optional[Tuple[float, float]] = None
    context: Optional[str] = None    # Target context for estimation
    domain: Optional[str] = None     # finance, health, etc.


@dataclass
class ElicitationDraw:
    """Single draw from E2 (one LLM response)."""
    draw_index: int
    estimate: float
    ci_low: float
    ci_high: float
    confidence: float
    reasoning_keywords: List[str]
    latency_seconds: float
    tokens_total: Optional[int] = None
    raw_response: Optional[str] = None
    parse_error: Optional[str] = None


@dataclass
class ElicitationResult:
    """Aggregated result from E1-E3 pipeline."""
    parameter: ParameterSpec
    model: str
    n_draws: int
    temperature: float
    timestamp: str

    # E3: Aggregated statistics
    theta_llm: float                 # Mean of draws
    sigma_elicit: float              # Std of draws
    ci_90_llm: Tuple[float, float]   # 90% CI from draws
    median: float
    iqr: Tuple[float, float]         # Interquartile range

    # Diagnostics
    draws: List[float]               # Raw draw values
    n_valid: int                     # Draws successfully parsed
    n_failed: int                    # Draws that failed parsing
    skewness: float
    kurtosis: float
    cv: float                        # Coefficient of variation

    # Comparison with literature (if available)
    literature_value: Optional[float] = None
    literature_deviation: Optional[float] = None  # (theta_llm - lit) / lit

    # Cost
    total_tokens: int = 0
    total_latency_seconds: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary for YAML/JSON export."""
        d = {
            "parameter_id": self.parameter.id,
            "parameter_symbol": self.parameter.symbol,
            "parameter_name": self.parameter.name,
            "model": self.model,
            "n_draws": self.n_draws,
            "n_valid": self.n_valid,
            "temperature": self.temperature,
            "timestamp": self.timestamp,
            "theta_llm": round(self.theta_llm, 6),
            "sigma_elicit": round(self.sigma_elicit, 6),
            "ci_90": [round(self.ci_90_llm[0], 6), round(self.ci_90_llm[1], 6)],
            "median": round(self.median, 6),
            "iqr": [round(self.iqr[0], 6), round(self.iqr[1], 6)],
            "skewness": round(self.skewness, 4),
            "kurtosis": round(self.kurtosis, 4),
            "cv": round(self.cv, 4),
            "draws": [round(d, 6) for d in self.draws],
            "total_tokens": self.total_tokens,
            "total_latency_seconds": round(self.total_latency_seconds, 2),
        }
        if self.literature_value is not None:
            d["literature_value"] = self.literature_value
            d["literature_deviation"] = round(self.literature_deviation, 4)
        if self.parameter.context:
            d["context"] = self.parameter.context
        if self.parameter.bounds:
            d["bounds"] = list(self.parameter.bounds)
        return d


# ──────────────────────────────────────────────────────────────────────
# E1: Elicitation Design
# ──────────────────────────────────────────────────────────────────────

def build_prompt(param: ParameterSpec) -> str:
    """E1: Construct structured elicitation prompt for a parameter."""
    bounds_line = ""
    if param.bounds:
        bounds_line = f"**Bounds:** [{param.bounds[0]}, {param.bounds[1]}]"

    context_line = ""
    if param.context:
        context_line = f"**Context:** {param.context}"

    anchor_line = ""
    if param.literature_value is not None:
        # Don't reveal exact value — give broad range to avoid anchoring bias
        # Show the domain but not the number
        anchor_line = (
            "**Note:** Literature estimates exist for this parameter in "
            "some contexts. Provide YOUR independent estimate for the "
            "context above."
        )

    return ELICITATION_TEMPLATE.format(
        symbol=param.symbol,
        name=param.name,
        description=param.description,
        bounds_line=bounds_line,
        context_line=context_line,
        anchor_line=anchor_line,
    )


# ──────────────────────────────────────────────────────────────────────
# E2: Repeated Measurement (API Calls)
# ──────────────────────────────────────────────────────────────────────

def call_openai_single(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> dict:
    """Single OpenAI API call with retry logic."""
    try:
        import openai
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    client = openai.OpenAI(api_key=api_key)

    for attempt in range(RETRY_ATTEMPTS):
        t0 = time.time()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            elapsed = time.time() - t0
            choice = response.choices[0]
            usage = response.usage

            return {
                "content": choice.message.content,
                "tokens_total": usage.total_tokens if usage else None,
                "latency_seconds": round(elapsed, 2),
            }
        except Exception as e:
            if attempt < RETRY_ATTEMPTS - 1:
                wait = RETRY_DELAY_BASE * (2 ** attempt)
                print(f"  Retry {attempt + 1}/{RETRY_ATTEMPTS} after {wait}s: {e}")
                time.sleep(wait)
            else:
                return {"error": str(e)}


def parse_draw(raw_content: str, draw_index: int, latency: float,
               tokens: Optional[int] = None) -> ElicitationDraw:
    """Parse a single LLM response into an ElicitationDraw."""
    # Try to extract JSON from response (may have markdown fences)
    content = raw_content.strip()
    # Remove markdown code fences if present
    content = re.sub(r'^```(?:json)?\s*', '', content)
    content = re.sub(r'\s*```$', '', content)
    content = content.strip()

    try:
        data = json.loads(content)
        return ElicitationDraw(
            draw_index=draw_index,
            estimate=float(data["estimate"]),
            ci_low=float(data.get("ci_low", data["estimate"] - 0.1)),
            ci_high=float(data.get("ci_high", data["estimate"] + 0.1)),
            confidence=float(data.get("confidence", 0.5)),
            reasoning_keywords=data.get("reasoning_keywords", []),
            latency_seconds=latency,
            tokens_total=tokens,
        )
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        # Try regex fallback for estimate
        match = re.search(r'"estimate"\s*:\s*([0-9.eE+-]+)', content)
        if match:
            est = float(match.group(1))
            return ElicitationDraw(
                draw_index=draw_index,
                estimate=est,
                ci_low=est * 0.8,
                ci_high=est * 1.2,
                confidence=0.3,
                reasoning_keywords=["parse_fallback"],
                latency_seconds=latency,
                tokens_total=tokens,
                parse_error=f"Partial parse: {e}",
            )

        return ElicitationDraw(
            draw_index=draw_index,
            estimate=float('nan'),
            ci_low=float('nan'),
            ci_high=float('nan'),
            confidence=0.0,
            reasoning_keywords=[],
            latency_seconds=latency,
            tokens_total=tokens,
            raw_response=content[:200],
            parse_error=str(e),
        )


def elicit_draws(
    param: ParameterSpec,
    n_draws: int = DEFAULT_N_DRAWS,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
) -> List[ElicitationDraw]:
    """E2: Generate N independent draws from the LLM."""
    prompt = build_prompt(param)
    draws = []

    for i in range(n_draws):
        result = call_openai_single(prompt, model=model, temperature=temperature)

        if "error" in result:
            draws.append(ElicitationDraw(
                draw_index=i,
                estimate=float('nan'),
                ci_low=float('nan'),
                ci_high=float('nan'),
                confidence=0.0,
                reasoning_keywords=[],
                latency_seconds=0.0,
                parse_error=result["error"],
            ))
        else:
            draw = parse_draw(
                result["content"], i,
                result["latency_seconds"],
                result.get("tokens_total"),
            )
            draws.append(draw)

        # Progress indicator
        status = f"θ={draw.estimate:.4f}" if not np.isnan(draw.estimate) else "FAIL"
        print(f"  Draw {i + 1}/{n_draws}: {status}")

    return draws


# ──────────────────────────────────────────────────────────────────────
# E3: Aggregation
# ──────────────────────────────────────────────────────────────────────

def aggregate_draws(
    draws: List[ElicitationDraw],
    param: ParameterSpec,
    model: str,
    temperature: float,
) -> ElicitationResult:
    """E3: Aggregate N draws into summary statistics."""
    valid_estimates = [d.estimate for d in draws if not np.isnan(d.estimate)]
    n_valid = len(valid_estimates)
    n_failed = len(draws) - n_valid

    if n_valid < 3:
        raise ValueError(
            f"Only {n_valid} valid draws (need ≥3). "
            f"{n_failed} failed. Check API key and model."
        )

    arr = np.array(valid_estimates)

    # Clip to bounds if specified
    if param.bounds:
        arr = np.clip(arr, param.bounds[0], param.bounds[1])

    theta_llm = float(np.mean(arr))
    sigma_elicit = float(np.std(arr, ddof=1))  # Sample std
    median = float(np.median(arr))
    q25, q75 = float(np.percentile(arr, 25)), float(np.percentile(arr, 75))
    ci5, ci95 = float(np.percentile(arr, 5)), float(np.percentile(arr, 95))

    # Distribution shape
    if sigma_elicit > 0:
        centered = (arr - arr.mean()) / sigma_elicit
        skewness = float(np.mean(centered ** 3))
        kurtosis = float(np.mean(centered ** 4) - 3)
        cv = sigma_elicit / abs(theta_llm) if theta_llm != 0 else float('inf')
    else:
        skewness = 0.0
        kurtosis = 0.0
        cv = 0.0

    # Literature comparison
    lit_dev = None
    if param.literature_value is not None and param.literature_value != 0:
        lit_dev = (theta_llm - param.literature_value) / abs(param.literature_value)

    # Cost
    total_tokens = sum(d.tokens_total for d in draws if d.tokens_total)
    total_latency = sum(d.latency_seconds for d in draws)

    return ElicitationResult(
        parameter=param,
        model=model,
        n_draws=len(draws),
        temperature=temperature,
        timestamp=datetime.now(timezone.utc).isoformat(),
        theta_llm=theta_llm,
        sigma_elicit=sigma_elicit,
        ci_90_llm=(ci5, ci95),
        median=median,
        iqr=(q25, q75),
        draws=valid_estimates,
        n_valid=n_valid,
        n_failed=n_failed,
        skewness=skewness,
        kurtosis=kurtosis,
        cv=cv,
        literature_value=param.literature_value,
        literature_deviation=lit_dev,
        total_tokens=total_tokens,
        total_latency_seconds=total_latency,
    )


# ──────────────────────────────────────────────────────────────────────
# Parameter Registry Integration
# ──────────────────────────────────────────────────────────────────────

def load_parameter_from_registry(param_id: str) -> ParameterSpec:
    """Load parameter spec from data/parameter-registry.yaml."""
    registry_path = Path("data/parameter-registry.yaml")
    if not registry_path.exists():
        raise FileNotFoundError(f"Parameter registry not found: {registry_path}")

    with open(registry_path) as f:
        registry = yaml.safe_load(f)

    # Search across all parameter categories
    for category in registry:
        if category == "metadata":
            continue
        params = registry[category]
        if not isinstance(params, list):
            continue
        for p in params:
            if p.get("id") == param_id:
                # Extract values
                values = p.get("values", {})
                lit = values.get("literature", {})
                lit_mean = lit.get("mean")
                lit_ci = None
                if "ci_95" in lit:
                    lit_ci = tuple(lit["ci_95"])

                # Determine bounds from parameter type
                bounds = None
                symbol = p.get("symbol", "")
                if symbol in ("β", "φ_crowding") or "rate" in p.get("name", "").lower():
                    bounds = (0.0, 1.0)

                return ParameterSpec(
                    id=p["id"],
                    symbol=p["symbol"],
                    name=p["name"],
                    description=p.get("description", ""),
                    bounds=bounds,
                    literature_value=lit_mean,
                    literature_ci=lit_ci,
                )

    raise ValueError(f"Parameter {param_id} not found in registry")


# ──────────────────────────────────────────────────────────────────────
# Output
# ──────────────────────────────────────────────────────────────────────

def save_result(result: ElicitationResult, output_dir: Path) -> Path:
    """Save elicitation result as YAML for calibration pipeline."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"LLMMC_{result.parameter.id}_{ts}.yaml"
    path = output_dir / filename

    output = {
        "llmmc_elicitation": result.to_dict(),
        "pipeline_status": {
            "e1_prompt": "completed",
            "e2_draws": "completed",
            "e3_aggregation": "completed",
            "e4_calibration": "pending",
            "e5_validation": "pending",
        },
        "calibration_input": {
            "theta_llm": result.theta_llm,
            "eu_llm": result.sigma_elicit,
            "parameter_id": result.parameter.id,
            "ready_for_calibration": result.n_valid >= 10,
        },
    }

    with open(path, "w") as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False)

    return path


def print_result(result: ElicitationResult) -> None:
    """Print formatted result to console."""
    p = result.parameter
    print()
    print("=" * 65)
    print(f"  LLMMC Elicitation Result: {p.symbol} ({p.name})")
    print("=" * 65)
    print(f"  Parameter:  {p.id} — {p.symbol}")
    if p.context:
        print(f"  Context:    {p.context}")
    print(f"  Model:      {result.model} (T={result.temperature})")
    print(f"  Draws:      {result.n_valid}/{result.n_draws} valid")
    print()
    print(f"  E3 Aggregation:")
    print(f"    θ_LLM     = {result.theta_llm:.4f}")
    print(f"    σ_elicit  = {result.sigma_elicit:.4f}")
    print(f"    90% CI    = [{result.ci_90_llm[0]:.4f}, {result.ci_90_llm[1]:.4f}]")
    print(f"    Median    = {result.median:.4f}")
    print(f"    IQR       = [{result.iqr[0]:.4f}, {result.iqr[1]:.4f}]")
    print(f"    CV        = {result.cv:.4f}")
    print(f"    Skewness  = {result.skewness:.3f}")
    print(f"    Kurtosis  = {result.kurtosis:.3f}")

    if result.literature_value is not None:
        print(f"\n  Literature Comparison:")
        print(f"    Lit value = {result.literature_value:.4f}")
        print(f"    LLM value = {result.theta_llm:.4f}")
        print(f"    Deviation = {result.literature_deviation:+.1%}")
        direction = "overestimates" if result.literature_deviation > 0 else "underestimates"
        print(f"    → GPT-4o {direction} by {abs(result.literature_deviation):.1%}")

    print(f"\n  Cost:")
    print(f"    Tokens:   {result.total_tokens:,}")
    print(f"    Latency:  {result.total_latency_seconds:.1f}s")

    # Individual draws
    print(f"\n  Draws: {result.draws}")
    print("=" * 65)


# ──────────────────────────────────────────────────────────────────────
# Synthetic Mode (for testing without API)
# ──────────────────────────────────────────────────────────────────────

def generate_synthetic_draws(
    param: ParameterSpec,
    n_draws: int = DEFAULT_N_DRAWS,
    temperature: float = DEFAULT_TEMPERATURE,
) -> List[ElicitationDraw]:
    """Generate synthetic draws that mimic LLM behavior for testing.

    Uses the literature value (if available) as center, adds noise
    proportional to temperature, and occasionally produces outliers
    to simulate real LLM measurement variance.
    """
    rng = np.random.default_rng(42)  # Reproducible

    # Center: use literature value if available, otherwise reasonable default
    center = param.literature_value if param.literature_value is not None else 1.0

    # Scale: higher temperature = more variance
    # Behavioral parameters typically have ~15-25% CV
    base_sigma = abs(center) * 0.18 * temperature

    draws = []
    for i in range(n_draws):
        # 80% normal draws, 20% slightly wider (simulates LLM variability)
        if rng.random() < 0.8:
            est = rng.normal(center, base_sigma)
        else:
            est = rng.normal(center, base_sigma * 2.0)

        # Respect bounds
        if param.bounds:
            est = np.clip(est, param.bounds[0] + 1e-4, param.bounds[1] - 1e-4)

        ci_width = base_sigma * 1.5
        draw = ElicitationDraw(
            draw_index=i,
            estimate=float(est),
            ci_low=float(est - ci_width),
            ci_high=float(est + ci_width),
            confidence=float(rng.uniform(0.5, 0.8)),
            reasoning_keywords=["synthetic", "test_mode"],
            latency_seconds=0.0,
            tokens_total=0,
        )
        draws.append(draw)
        print(f"  Draw {i + 1}/{n_draws}: θ={draw.estimate:.4f} (synthetic)")

    return draws


def _run_e2e_demo(args):
    """Run full E1→E3→E4→E5 pipeline demo with synthetic data.

    This demonstrates the complete chain:
      E1: Build prompt (shown)
      E2: Synthetic draws (15 draws)
      E3: Aggregation (mean, std, CI)
      E4: Calibration via LLMMCCalibrator
      E5: Validation (compare to literature)
    """
    print("\n" + "=" * 70)
    print("  LLMMC E2E DEMO: Full Pipeline (E1 → E3 → E4 → E5)")
    print("=" * 70)

    # Load a well-known parameter: Loss Aversion
    try:
        param = load_parameter_from_registry("PAR-BEH-001")
    except (FileNotFoundError, ValueError):
        # Fallback if registry not found
        param = ParameterSpec(
            id="PAR-BEH-001",
            symbol="λ",
            name="Loss Aversion Coefficient",
            description="Ratio of loss to gain weighting in prospect theory",
            literature_value=2.25,
        )

    # ── E1: Show prompt ──
    prompt = build_prompt(param)
    print(f"\n── E1: Elicitation Design ──")
    print(f"  Parameter: {param.symbol} ({param.name})")
    print(f"  Literature: {param.literature_value}")
    print(f"  Prompt: {len(prompt)} chars")

    # ── E2 + E3: Synthetic draws + aggregation ──
    print(f"\n── E2: Repeated Measurement (synthetic, N=15) ──")
    draws = generate_synthetic_draws(param, n_draws=15, temperature=0.8)
    result = aggregate_draws(draws, param, "synthetic-gpt-4o", 0.8)

    print(f"\n── E3: Aggregation ──")
    print(f"  θ_LLM     = {result.theta_llm:.4f}")
    print(f"  σ_elicit  = {result.sigma_elicit:.4f}")
    print(f"  90% CI    = [{result.ci_90_llm[0]:.4f}, {result.ci_90_llm[1]:.4f}]")
    print(f"  CV        = {result.cv:.4f}")
    if result.literature_value is not None:
        print(f"  Lit dev   = {result.literature_deviation:+.1%}")

    # ── E4: Calibration ──
    print(f"\n── E4: Calibration (via LLMMCCalibrator) ──")
    try:
        # Handle import from different working directories
        try:
            from llmmc_calibration import LLMMCCalibrator
        except ImportError:
            sys.path.insert(0, str(Path(__file__).parent))
            from llmmc_calibration import LLMMCCalibrator

        cal = LLMMCCalibrator()

        # Use existing Tier 1/2 anchors for calibration
        cal.add_pct_anchors()

        # Fit calibration function
        cal.fit()
        n_anchors = len(cal.anchors)

        # Compute R² for display
        theta_t12 = np.array([a.theta_t12 for a in cal.anchors])
        theta_llm_a = np.array([a.theta_llm for a in cal.anchors])
        theta_pred = cal.a + cal.b * theta_llm_a
        ss_res = np.sum((theta_t12 - theta_pred) ** 2)
        ss_tot = np.sum((theta_t12 - np.mean(theta_t12)) ** 2)
        r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

        print(f"  Anchors:  {n_anchors} (Tier 1/2 from registry)")
        print(f"  Alpha:    {cal.a:.4f}")
        print(f"  Beta:     {cal.b:.4f}")
        print(f"  R²:       {r_squared:.4f}")

        # Calibrate the E3 result
        cal_result = cal.calibrate(
            theta_llm=result.theta_llm,
            eu_llm=result.sigma_elicit,
        )
        print(f"\n  E4 Result:")
        print(f"    θ_posterior = {cal_result.theta_final:.4f}")
        print(f"    σ_posterior = {cal_result.sigma_final:.4f}")
        print(f"    95% CI     = [{cal_result.ci_95[0]:.4f}, {cal_result.ci_95[1]:.4f}]")
        print(f"    Tier       = {cal_result.tier}")

        # ── E5: Validation ──
        print(f"\n── E5: Validation ──")
        if param.literature_value is not None:
            deviation = abs(cal_result.theta_final - param.literature_value)
            rel_dev = deviation / abs(param.literature_value)
            within_ci = cal_result.ci_95[0] <= param.literature_value <= cal_result.ci_95[1]

            print(f"  Literature:     {param.literature_value:.4f}")
            print(f"  θ_posterior:    {cal_result.theta_final:.4f}")
            print(f"  |Deviation|:   {deviation:.4f} ({rel_dev:.1%})")
            print(f"  Lit in 95% CI:  {'YES ✓' if within_ci else 'NO ✗'}")

            # LLP checks
            print(f"\n  LLP Checks:")
            print(f"    LLP-1 (Reproducibility):  CV = {result.cv:.3f} {'< 0.5 ✓' if result.cv < 0.5 else '≥ 0.5 ✗'}")
            print(f"    LLP-2 (Calibration):      R² = {r_squared:.3f} {'> 0.3 ✓' if r_squared > 0.3 else '≤ 0.3 ✗'}")
            print(f"    LLP-3 (Bounded):          σ/|θ| = {cal_result.sigma_final/abs(cal_result.theta_final):.3f}")

    except ImportError:
        print("  SKIP: llmmc_calibration.py not importable from this directory")
        print("  Run from repository root: python scripts/llmmc_elicitation.py --e2e-demo")

    # Save result
    output_path = save_result(result, Path(args.output_dir if hasattr(args, 'output_dir') else "data/llmmc-draws"))
    print(f"\n  Saved E3 output: {output_path}")

    print(f"\n{'=' * 70}")
    print(f"  E2E DEMO COMPLETE")
    print(f"  Pipeline: E1 ✓ → E2 ✓ → E3 ✓ → E4 {'✓' if 'cal_result' in dir() else '—'} → E5 {'✓' if 'within_ci' in dir() else '—'}")
    print(f"{'=' * 70}\n")


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LLMMC Elicitation Pipeline (E1–E3): GPT-4o as measurement instrument"
    )
    parser.add_argument("--param", type=str, help="Parameter ID (e.g., PAR-BEH-001)")
    parser.add_argument("--symbol", type=str, help="Custom parameter symbol")
    parser.add_argument("--name", type=str, help="Custom parameter name")
    parser.add_argument("--description", type=str, help="Custom parameter description")
    parser.add_argument("--bounds", type=float, nargs=2, help="Parameter bounds (low high)")
    parser.add_argument("--context", type=str, help="Target context for estimation")
    parser.add_argument("--n-draws", type=int, default=DEFAULT_N_DRAWS,
                        help=f"Number of draws (default: {DEFAULT_N_DRAWS})")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                        help=f"OpenAI model (default: {DEFAULT_MODEL})")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE,
                        help=f"Temperature (default: {DEFAULT_TEMPERATURE})")
    parser.add_argument("--output-dir", type=str, default="data/llmmc-draws",
                        help="Output directory for results")
    parser.add_argument("--all-behavioral", action="store_true",
                        help="Elicit all behavioral parameters")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show prompts without making API calls")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of YAML")
    parser.add_argument("--synthetic", action="store_true",
                        help="Generate synthetic draws (no API needed, for testing)")
    parser.add_argument("--e2e-demo", action="store_true",
                        help="Run full E1→E3→E4→E5 pipeline demo with synthetic data")

    args = parser.parse_args()

    # E2E demo mode
    if args.e2e_demo:
        _run_e2e_demo(args)
        return

    # Build parameter spec
    if args.param:
        param = load_parameter_from_registry(args.param)
        if args.context:
            param.context = args.context
    elif args.symbol:
        param = ParameterSpec(
            id=f"CUSTOM-{args.symbol}",
            symbol=args.symbol,
            name=args.name or args.symbol,
            description=args.description or "Custom parameter",
            bounds=tuple(args.bounds) if args.bounds else None,
            context=args.context,
        )
    elif args.all_behavioral:
        _run_all_behavioral(args)
        return
    else:
        parser.error("Provide --param, --symbol, or --all-behavioral")
        return

    # Dry run: show prompt and exit
    if args.dry_run:
        prompt = build_prompt(param)
        print("\n── E1: Elicitation Prompt ──\n")
        print(f"SYSTEM:\n{SYSTEM_PROMPT}\n")
        print(f"USER:\n{prompt}")
        print(f"\n── Would make {args.n_draws} API calls to {args.model} ──")
        return

    # Run E1-E3
    mode = "SYNTHETIC" if args.synthetic else args.model
    print(f"\n── LLMMC Elicitation: {param.symbol} ({param.name}) ──")
    print(f"   Model: {mode}, N={args.n_draws}, T={args.temperature}")
    print()

    if args.synthetic:
        draws = generate_synthetic_draws(param, args.n_draws, args.temperature)
    else:
        draws = elicit_draws(param, args.n_draws, args.model, args.temperature)
    result = aggregate_draws(draws, param, args.model if not args.synthetic else "synthetic", args.temperature)

    # Output
    print_result(result)

    # Save
    output_path = save_result(result, Path(args.output_dir))
    print(f"\nSaved to: {output_path}")

    # JSON option
    if args.json:
        print(f"\nJSON:\n{json.dumps(result.to_dict(), indent=2)}")


def _run_all_behavioral(args):
    """Elicit all behavioral parameters from registry."""
    registry_path = Path("data/parameter-registry.yaml")
    with open(registry_path) as f:
        registry = yaml.safe_load(f)

    params = registry.get("behavioral_parameters", [])
    print(f"\n── LLMMC Batch Elicitation: {len(params)} behavioral parameters ──\n")

    results = []
    for p in params:
        param_id = p["id"]
        try:
            param = load_parameter_from_registry(param_id)
            if args.context:
                param.context = args.context

            if args.dry_run:
                prompt = build_prompt(param)
                print(f"\n{param_id} ({param.symbol}):")
                print(f"  Prompt length: {len(prompt)} chars")
                continue

            print(f"\n{'─' * 50}")
            print(f"  {param_id}: {param.symbol} ({param.name})")
            print(f"{'─' * 50}")

            if args.synthetic:
                draws = generate_synthetic_draws(param, args.n_draws, args.temperature)
            else:
                draws = elicit_draws(param, args.n_draws, args.model, args.temperature)
            result = aggregate_draws(draws, param, args.model, args.temperature)
            print_result(result)

            output_path = save_result(result, Path(args.output_dir))
            print(f"  Saved: {output_path}")
            results.append(result)

        except Exception as e:
            print(f"  ERROR for {param_id}: {e}")

    if results:
        print(f"\n{'=' * 65}")
        print(f"  BATCH SUMMARY: {len(results)}/{len(params)} parameters elicited")
        print(f"{'=' * 65}")
        for r in results:
            lit = f"(lit: {r.literature_value:.3f}, dev: {r.literature_deviation:+.1%})" \
                if r.literature_value else ""
            print(f"  {r.parameter.id}: θ={r.theta_llm:.4f} ± {r.sigma_elicit:.4f} {lit}")


if __name__ == "__main__":
    main()
