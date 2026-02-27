#!/usr/bin/env python3
"""
Universal Parameter-Lookup API
===============================

Single entry point for parameter retrieval in the EBF framework.
Connects Layer 2 (YAML registry) with Layer 1 (formal computation).

Pipeline:
    1. Load parameter from parameter-registry.yaml (Layer 2)
    2. Optionally transform via PCT (Layer 1)
    3. Optionally calibrate via LLMMC (Layer 1)

Usage:
    # Python API
    from parameter_api import lookup_parameter, get_parameter
    result = lookup_parameter("PAR-BEH-001", domain="finance")
    result = lookup_parameter("PAR-BEH-016",
                              target_psi={"psi_S": "competence_signaling"},
                              anchor_context="welfare")

    # CLI
    python parameter_api.py --id PAR-BEH-001
    python parameter_api.py --symbol lambda_R --domain finance
    python parameter_api.py --id PAR-BEH-016 --target-psi psi_S=competence_signaling

Author: EBF Framework
Date: 2026-02-15
Layer: 1+2 (Orchestrator between Formal Computation and Parameter Store)
"""

import sys
import json
import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any

REPO_ROOT = Path(__file__).resolve().parent.parent
PARAMETER_REGISTRY_PATH = REPO_ROOT / "data" / "parameter-registry.yaml"

# Add scripts/ to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ParameterValue:
    """A resolved parameter value with full provenance."""
    parameter_id: str
    symbol: str
    name: str
    value: float
    ci_95: tuple = (0.0, 0.0)
    source: str = ""
    domain: str = ""
    tier: int = 2
    tier_note: str = ""

    # PCT transformation (if applied)
    pct_applied: bool = False
    pct_anchor_context: str = ""
    pct_target_context: str = ""
    pct_product_M: float = 1.0

    # LLMMC calibration (if applied)
    llmmc_applied: bool = False
    llmmc_shrinkage: float = 1.0

    def to_dict(self) -> Dict:
        """JSON-serializable output."""
        d = {
            "parameter_id": self.parameter_id,
            "symbol": self.symbol,
            "name": self.name,
            "value": round(self.value, 4),
            "ci_95": [round(self.ci_95[0], 4), round(self.ci_95[1], 4)],
            "source": self.source,
            "domain": self.domain,
            "tier": self.tier,
            "tier_note": self.tier_note,
        }
        if self.pct_applied:
            d["pct"] = {
                "applied": True,
                "anchor_context": self.pct_anchor_context,
                "target_context": self.pct_target_context,
                "product_M": round(self.pct_product_M, 4),
            }
        if self.llmmc_applied:
            d["llmmc"] = {
                "applied": True,
                "shrinkage": round(self.llmmc_shrinkage, 4),
            }
        return d


# ---------------------------------------------------------------------------
# Registry loading
# ---------------------------------------------------------------------------

_REGISTRY_CACHE = None


def _load_registry() -> Dict:
    """Load parameter-registry.yaml."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML required. Install with: pip install pyyaml")
        return {}

    if not PARAMETER_REGISTRY_PATH.exists():
        return {}

    with open(PARAMETER_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_registry() -> Dict:
    """Get parameter registry (cached)."""
    global _REGISTRY_CACHE
    if _REGISTRY_CACHE is None:
        _REGISTRY_CACHE = _load_registry()
    return _REGISTRY_CACHE


def _find_all_parameters() -> List[Dict]:
    """Collect all parameters from all sections of the registry."""
    reg = get_registry()
    params = []
    # Registry has multiple top-level sections: behavioral_parameters,
    # contextual_parameters, complementarity_parameters, etc.
    for key, value in reg.items():
        if key == "metadata":
            continue
        if isinstance(value, list):
            params.extend(value)
    return params


def _find_parameter(parameter_id: str = None, symbol: str = None) -> Optional[Dict]:
    """
    Find a parameter by ID or symbol.

    Args:
        parameter_id: e.g. "PAR-BEH-001"
        symbol: e.g. "λ" or "lambda_R"

    Returns:
        Parameter dict from registry, or None
    """
    all_params = _find_all_parameters()

    for p in all_params:
        if parameter_id and p.get("id") == parameter_id:
            return p
        if symbol and p.get("symbol") == symbol:
            return p
        # Also check symbol aliases (e.g. "lambda_R" matches "λ_R")
        if symbol:
            psym = p.get("symbol", "")
            # Normalize: λ → lambda, β → beta, etc.
            normalized = (psym
                          .replace("λ", "lambda")
                          .replace("β", "beta")
                          .replace("γ", "gamma")
                          .replace("φ", "phi")
                          .replace("σ", "sigma")
                          .replace("τ", "tau")
                          .replace("α", "alpha")
                          .replace("δ", "delta")
                          .replace("ω", "omega")
                          .replace("κ", "kappa")
                          .replace("η", "eta")
                          .replace("ε", "epsilon")
                          .replace("θ", "theta")
                          .replace("μ", "mu"))
            if normalized == symbol or normalized.replace("_", "") == symbol.replace("_", ""):
                return p

    return None


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def get_parameter(
    parameter_id: str = None,
    symbol: str = None,
    domain: str = None,
) -> Optional[ParameterValue]:
    """
    Look up a parameter value from the registry (Layer 2 only).

    Args:
        parameter_id: Registry ID, e.g. "PAR-BEH-001"
        symbol: Parameter symbol, e.g. "lambda" or "λ"
        domain: Optional domain for domain-specific value, e.g. "finance"

    Returns:
        ParameterValue with registry data, or None if not found
    """
    p = _find_parameter(parameter_id, symbol)
    if p is None:
        return None

    values = p.get("values", {})

    # Determine which value to use
    if domain and "domain_specific" in values:
        ds = values["domain_specific"]
        if domain in ds:
            val = ds[domain]
            mean = val.get("mean", 0.0)
            ci = val.get("ci_68", val.get("ci_95", [mean - 0.1, mean + 0.1]))
            source = f"domain_specific:{domain}"
            tier_note = f"Domain-specific ({domain})"
        else:
            # Fall back to literature
            lit = values.get("literature", {})
            mean = lit.get("mean", 0.0)
            ci = lit.get("ci_95", lit.get("ci_68", [mean - 0.3, mean + 0.3]))
            source = lit.get("source", "")
            tier_note = "Literature (domain not found)"
    elif "dach_adjusted" in values:
        dach = values["dach_adjusted"]
        mean = dach.get("mean", 0.0)
        ci = dach.get("ci_68", dach.get("ci_95", [mean - 0.2, mean + 0.2]))
        source = dach.get("source", "")
        tier_note = "DACH-adjusted"
    elif "literature" in values:
        lit = values["literature"]
        mean = lit.get("mean", 0.0)
        ci = lit.get("ci_95", lit.get("ci_68", [mean - 0.3, mean + 0.3]))
        source = lit.get("source", "")
        tier_note = "Literature"
    else:
        # Try to find any numeric value
        mean = 0.0
        ci = [0.0, 0.0]
        source = ""
        tier_note = "No value found"
        for _k, v in values.items():
            if isinstance(v, dict) and "mean" in v:
                mean = v["mean"]
                ci = v.get("ci_95", v.get("ci_68", [mean - 0.2, mean + 0.2]))
                source = v.get("source", "")
                tier_note = f"From: {_k}"
                break

    return ParameterValue(
        parameter_id=p.get("id", ""),
        symbol=p.get("symbol", ""),
        name=p.get("name", ""),
        value=mean,
        ci_95=tuple(ci) if len(ci) == 2 else (ci[0], ci[-1]),
        source=source,
        domain=domain or "",
        tier=1 if "literature" in values else 2,
        tier_note=tier_note,
    )


def lookup_parameter(
    parameter_id: str = None,
    symbol: str = None,
    domain: str = None,
    target_psi: Dict[str, str] = None,
    anchor_context: str = None,
    anchor_psi: Dict[str, str] = None,
    calibrate: bool = False,
) -> Optional[ParameterValue]:
    """
    Universal parameter lookup with optional PCT transformation and LLMMC calibration.

    This is the main entry point connecting Layer 2 (registry) with Layer 1 (computation).

    Pipeline:
        1. Load from parameter-registry.yaml
        2. If target_psi provided: transform via PCT
        3. If calibrate=True: calibrate via LLMMC

    Args:
        parameter_id: Registry ID, e.g. "PAR-BEH-001"
        symbol: Parameter symbol (alternative to parameter_id)
        domain: Domain for domain-specific value
        target_psi: Target Psi-conditions for PCT transform
                    e.g. {"psi_S": "competence_signaling", "psi_I": "professional_hierarchy"}
        anchor_context: Name of the anchor context (default: inferred from registry)
        anchor_psi: Anchor Psi-conditions (default: inferred from registry literature context)
        calibrate: Whether to apply LLMMC calibration after PCT

    Returns:
        ParameterValue with full provenance chain
    """
    # Step 1: Load from registry
    base = get_parameter(parameter_id, symbol, domain)
    if base is None:
        return None

    # Step 2: PCT transformation (if requested)
    if target_psi:
        try:
            from pct import transform_from_contexts
        except ImportError:
            # PCT not available — return base value with warning
            base.tier_note += " (PCT unavailable)"
            return base

        # Build anchor psi from provided or defaults
        a_psi = anchor_psi or {}
        a_ctx = anchor_context or "literature"
        t_ctx = "target"

        # If no anchor_psi provided, try to infer from parameter's literature context
        if not a_psi and not anchor_psi:
            # Use default: a mild context (no specific labels)
            # The user should provide anchor_psi for accurate transforms
            a_psi = {}

        # Only transform if we have both anchor and target dimensions
        if a_psi:
            pct_result = transform_from_contexts(
                theta_A=base.value,
                anchor_psi=a_psi,
                target_psi=target_psi,
                anchor_context=a_ctx,
                target_context=t_ctx,
                parameter_id=base.parameter_id,
                parameter_symbol=base.symbol,
            )

            # Update the value
            base.value = pct_result.theta_B
            base.pct_applied = True
            base.pct_anchor_context = a_ctx
            base.pct_target_context = t_ctx
            base.pct_product_M = pct_result.product_M
            base.tier = 2
            base.tier_note = f"PCT-transformed (M={pct_result.product_M:.4f})"

            # Adjust CI proportionally
            if base.ci_95[1] > base.ci_95[0]:
                ratio = pct_result.product_M
                mid = base.value
                half_width = (base.ci_95[1] - base.ci_95[0]) / 2.0 * abs(ratio)
                base.ci_95 = (mid - half_width, mid + half_width)
        else:
            # No anchor_psi: cannot transform, but note the target
            base.tier_note += f" (provide anchor_psi for PCT transform)"

    # Step 3: LLMMC calibration (if requested)
    if calibrate and base.pct_applied:
        try:
            from llmmc_calibration import LLMMCCalibrator
        except ImportError:
            base.tier_note += " (LLMMC unavailable)"
            return base

        cal = LLMMCCalibrator(min_anchors=5)
        # Add example anchors
        from llmmc_calibration import create_example_calibration_set
        cal.add_anchors_from_dict(create_example_calibration_set())
        cal.add_pct_anchors()
        cal.fit()

        # Build a mock PCT result for calibrate_with_pct
        from pct import PCTResult, PsiDelta
        mock_pct = PCTResult(
            theta_A=base.value / base.pct_product_M if base.pct_product_M != 0 else base.value,
            theta_B=base.value,
            product_M=base.pct_product_M,
            psi_deltas=[],
            anchor_context=base.pct_anchor_context,
            target_context=base.pct_target_context,
            parameter_id=base.parameter_id,
            parameter_symbol=base.symbol,
        )

        result = cal.calibrate_with_pct(mock_pct, eu_pct=0.10)
        base.value = result.theta_final
        base.ci_95 = result.ci_95
        base.llmmc_applied = True
        base.llmmc_shrinkage = result.shrinkage_factor
        base.tier_note = result.tier_note

    return base


def list_parameters(domain: str = None) -> List[Dict]:
    """
    List all available parameters, optionally filtered by domain.

    Args:
        domain: Filter by applicable domain (e.g. "FIN", "HLT")

    Returns:
        List of {id, symbol, name, domains} dicts
    """
    all_params = _find_all_parameters()
    results = []

    for p in all_params:
        pid = p.get("id", "")
        if not pid:
            continue

        domains = p.get("applicable_domains", [])
        if domain and domain.upper() not in [d.upper() for d in domains]:
            continue

        results.append({
            "id": pid,
            "symbol": p.get("symbol", ""),
            "name": p.get("name", ""),
            "domains": domains,
        })

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Universal Parameter-Lookup API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parameter_api.py --id PAR-BEH-001
  python parameter_api.py --symbol lambda --domain finance
  python parameter_api.py --id PAR-BEH-016 --target-psi psi_S=competence_signaling
  python parameter_api.py --list
  python parameter_api.py --list --domain FIN

REST API Server:
  python parameter_api.py --serve                    # Start on port 8080
  python parameter_api.py --serve --port 9090        # Custom port
  python parameter_api.py --serve --host 0.0.0.0     # Bind to all interfaces

Pipeline: Registry (Layer 2) → PCT (Layer 1) → LLMMC (Layer 1)
        """
    )

    parser.add_argument("--id", type=str, help="Parameter ID (e.g. PAR-BEH-001)")
    parser.add_argument("--symbol", type=str, help="Parameter symbol (e.g. lambda, lambda_R)")
    parser.add_argument("--domain", type=str, help="Domain filter (e.g. finance, health)")
    parser.add_argument("--target-psi", type=str,
                        help="Target Psi-conditions for PCT: psi_S=label,psi_I=label")
    parser.add_argument("--anchor-psi", type=str,
                        help="Anchor Psi-conditions: psi_S=label,psi_I=label")
    parser.add_argument("--anchor-context", type=str, help="Anchor context name")
    parser.add_argument("--calibrate", action="store_true",
                        help="Apply LLMMC calibration after PCT")
    parser.add_argument("--list", action="store_true",
                        help="List all available parameters")
    parser.add_argument("--json", action="store_true",
                        help="JSON output only")

    args = parser.parse_args()

    # List mode
    if args.list:
        params = list_parameters(args.domain)
        if args.json:
            print(json.dumps(params, indent=2))
        else:
            print(f"\nAvailable Parameters ({len(params)}):")
            print(f"{'ID':20s} {'Symbol':15s} {'Name':40s} {'Domains'}")
            print("-" * 95)
            for p in params:
                print(f"{p['id']:20s} {p['symbol']:15s} {p['name']:40s} {', '.join(p['domains'])}")
            print()
        return

    # Lookup mode
    if not args.id and not args.symbol:
        parser.print_help()
        return

    # Parse psi args
    target_psi = None
    if args.target_psi:
        target_psi = {}
        for pair in args.target_psi.split(","):
            k, v = pair.split("=", 1)
            target_psi[k.strip()] = v.strip()

    anchor_psi = None
    if args.anchor_psi:
        anchor_psi = {}
        for pair in args.anchor_psi.split(","):
            k, v = pair.split("=", 1)
            anchor_psi[k.strip()] = v.strip()

    result = lookup_parameter(
        parameter_id=args.id,
        symbol=args.symbol,
        domain=args.domain,
        target_psi=target_psi,
        anchor_psi=anchor_psi,
        anchor_context=args.anchor_context,
        calibrate=args.calibrate,
    )

    if result is None:
        print(f"Parameter not found: {args.id or args.symbol}")
        sys.exit(1)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print()
        print("=" * 60)
        print("PARAMETER LOOKUP RESULT")
        print("=" * 60)
        print(f"\n   ID:      {result.parameter_id}")
        print(f"   Symbol:  {result.symbol}")
        print(f"   Name:    {result.name}")
        print(f"   Value:   {result.value:.4f}")
        print(f"   95% CI:  [{result.ci_95[0]:.4f}, {result.ci_95[1]:.4f}]")
        print(f"   Source:  {result.source}")
        if result.domain:
            print(f"   Domain:  {result.domain}")
        print(f"   Tier:    {result.tier} ({result.tier_note})")

        if result.pct_applied:
            print(f"\n   PCT Transform:")
            print(f"     Anchor: {result.pct_anchor_context}")
            print(f"     Target: {result.pct_target_context}")
            print(f"     M:      {result.pct_product_M:.4f}")

        if result.llmmc_applied:
            print(f"\n   LLMMC Calibration:")
            print(f"     Shrinkage: {result.llmmc_shrinkage:.4f}")

        print()


# ---------------------------------------------------------------------------
# REST API Server (Layer 1 Gateway)
# ---------------------------------------------------------------------------

class ParameterAPIHandler:
    """HTTP request handler for the Parameter Lookup API.

    Endpoints:
        GET /api/v1/parameter/<id>         — Single parameter lookup
        GET /api/v1/parameter/<id>?psi_S=x — With PCT transform
        GET /api/v1/parameters             — List all parameters
        GET /api/v1/parameters?domain=FIN  — List filtered by domain
        GET /api/v1/health                 — Pipeline health check
        GET /api/v1/batch?ids=A,B,C        — Batch query
    """

    def __init__(self):
        self._orch = None

    def _get_orchestrator(self):
        """Lazy-load orchestrator to avoid import overhead at module load."""
        if self._orch is None:
            from orchestrator import Orchestrator
            self._orch = Orchestrator()
        return self._orch

    def handle_request(self, method: str, path: str, query: Dict[str, str]) -> tuple:
        """
        Route an HTTP request and return (status_code, response_dict).

        Args:
            method: HTTP method (GET, POST, etc.)
            path: URL path (e.g. /api/v1/parameter/PAR-BEH-001)
            query: Parsed query parameters

        Returns:
            Tuple of (int status_code, dict response_body)
        """
        if method != "GET":
            return 405, {"error": "Method not allowed", "allowed": ["GET"]}

        # Route matching
        if path == "/api/v1/health":
            return self._handle_health()
        elif path == "/api/v1/parameters":
            return self._handle_list(query)
        elif path == "/api/v1/batch":
            return self._handle_batch(query)
        elif path.startswith("/api/v1/parameter/"):
            param_id = path[len("/api/v1/parameter/"):]
            return self._handle_single(param_id, query)
        elif path == "/":
            return self._handle_index()
        else:
            return 404, {"error": f"Not found: {path}"}

    def _handle_index(self) -> tuple:
        """Return API documentation."""
        return 200, {
            "name": "EBF Parameter Lookup API",
            "version": "1.0",
            "layer": "Layer 1 Gateway",
            "principle": "Compute, Don't Hallucinate",
            "endpoints": {
                "GET /api/v1/parameter/<id>": "Single parameter lookup (optional: psi_S, psi_I, ... for PCT)",
                "GET /api/v1/parameters": "List all parameters (optional: domain=FIN)",
                "GET /api/v1/batch?ids=A,B,C": "Batch query (optional: calibrate=true)",
                "GET /api/v1/health": "Pipeline health check",
            },
            "examples": [
                "/api/v1/parameter/PAR-BEH-001",
                "/api/v1/parameter/PAR-BEH-016?psi_S=competence_signaling&calibrate=true",
                "/api/v1/parameters?domain=FIN",
                "/api/v1/batch?ids=PAR-BEH-001,PAR-BEH-016",
                "/api/v1/health",
            ],
        }

    def _handle_health(self) -> tuple:
        """Run pipeline health check."""
        orch = self._get_orchestrator()
        result = orch.health_check()
        return 200, result.to_dict()

    def _handle_list(self, query: Dict[str, str]) -> tuple:
        """List parameters, optionally filtered by domain."""
        domain = query.get("domain")
        params = list_parameters(domain)
        return 200, {"count": len(params), "parameters": params}

    def _handle_batch(self, query: Dict[str, str]) -> tuple:
        """Batch query multiple parameters."""
        ids_str = query.get("ids", "")
        if not ids_str:
            return 400, {"error": "Missing required parameter: ids (comma-separated)"}

        ids = [x.strip() for x in ids_str.split(",") if x.strip()]
        calibrate = query.get("calibrate", "").lower() in ("true", "1", "yes")

        # Build context from query params
        ctx = self._build_context(query)

        orch = self._get_orchestrator()
        results = orch.batch_query(ids, context=ctx, calibrate=calibrate)

        output = []
        for pid, r in zip(ids, results):
            if r is not None:
                output.append(r.to_dict())
            else:
                output.append({"parameter_id": pid, "error": "not found"})

        return 200, {"count": len(output), "results": output}

    def _handle_single(self, param_id: str, query: Dict[str, str]) -> tuple:
        """Look up a single parameter with optional PCT/LLMMC."""
        calibrate = query.get("calibrate", "").lower() in ("true", "1", "yes")
        ctx = self._build_context(query)

        orch = self._get_orchestrator()
        result = orch.query(
            parameter_id=param_id,
            context=ctx,
            calibrate=calibrate,
        )

        if result is None:
            return 404, {"error": f"Parameter not found: {param_id}"}

        return 200, result.to_dict()

    def _build_context(self, query: Dict[str, str]) -> Optional[Dict]:
        """Extract Psi context from query parameters."""
        ctx = {}
        target_psi = {}
        anchor_psi = {}

        psi_dimensions = ["psi_S", "psi_I", "psi_C", "psi_K", "psi_E", "psi_T", "psi_M", "psi_F"]

        for dim in psi_dimensions:
            if dim in query:
                target_psi[dim] = query[dim]
            anchor_key = f"anchor_{dim}"
            if anchor_key in query:
                anchor_psi[dim] = query[anchor_key]

        if target_psi:
            ctx["target_psi"] = target_psi
        if anchor_psi:
            ctx["anchor_psi"] = anchor_psi
        if "anchor_context" in query:
            ctx["anchor_context"] = query["anchor_context"]
        if "domain" in query:
            ctx["domain"] = query["domain"]

        return ctx if ctx else None


def run_server(host: str = "127.0.0.1", port: int = 8080):
    """
    Start a lightweight HTTP server for the Parameter Lookup API.

    Uses Python stdlib http.server — no external dependencies.
    Suitable for local development and internal tool integration.

    Args:
        host: Bind address (default: 127.0.0.1)
        port: Port number (default: 8080)
    """
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    api = ParameterAPIHandler()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            # Flatten query params (take first value for each key)
            query = {k: v[0] for k, v in parse_qs(parsed.query).items()}

            status, body = api.handle_request("GET", parsed.path, query)

            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(body, indent=2).encode("utf-8"))

        def log_message(self, format, *args):
            """Suppress default logging for cleaner output."""
            pass

    server = HTTPServer((host, port), Handler)
    print(f"\nEBF Parameter Lookup API")
    print(f"========================")
    print(f"Server:    http://{host}:{port}")
    print(f"Endpoints:")
    print(f"  GET /api/v1/parameter/<id>   — Single lookup")
    print(f"  GET /api/v1/parameters       — List all")
    print(f"  GET /api/v1/batch?ids=A,B    — Batch query")
    print(f"  GET /api/v1/health           — Health check")
    print(f"\nLayer: 1 Gateway (Compute, Don't Hallucinate)")
    print(f"Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    # Check if --serve flag is present (before argparse takes over)
    if "--serve" in sys.argv:
        port = 8080
        host = "127.0.0.1"
        # Extract port if provided
        for i, arg in enumerate(sys.argv):
            if arg == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
            if arg == "--host" and i + 1 < len(sys.argv):
                host = sys.argv[i + 1]
        run_server(host, port)
    else:
        main()
