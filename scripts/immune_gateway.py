#!/usr/bin/env python3
"""
Immune Gateway — Pre-Response Layer 1 Computation
===================================================

Solves the fundamental architectural paradox identified in KB-VIR-001:

    "Der Wirt entscheidet, ob der Virus leben darf"
    (The host decides whether the virus lives)

Problem:
    The LLM (Layer 3, susceptibility=0.8) decides whether to route
    through the formal kernel (Layer 1, susceptibility=0.0). This means
    the most virus-susceptible component controls immune system activation.

Solution:
    This script runs AUTOMATICALLY via the UserPromptSubmit hook, BEFORE
    Claude generates any response. If parameter-relevant keywords are
    detected, the orchestrator is invoked and its output is injected into
    Claude's context. The LLM no longer decides — the immune system
    activates autonomously.

Architecture:
    User types question
        |
        v
    UserPromptSubmit hook fires (BEFORE Claude thinks)
        |
        v
    immune_gateway.py detects keywords    <-- THIS SCRIPT
        |                  |
        no match           match found
        |                  |
        v                  v
    exit silently      orchestrator.py --query "..." --json
                           |
                           v
                       Output to stdout (Claude sees this)
                           |
                           v
                       Claude responds WITH Layer 1 data in context

Design Principles:
    1. AUTONOMOUS: Runs without LLM decision (hook-driven)
    2. FAST: Keyword detection is O(n) string matching, <10ms
    3. SILENT: No output when no parameter keywords detected
    4. SAFE: Timeout protection, graceful failure
    5. TRANSPARENT: Output clearly marks provenance as Layer 1

Usage:
    echo "What is loss aversion?" | python immune_gateway.py
    python immune_gateway.py "How strong is present bias?"
    python immune_gateway.py --test  # Run self-test

Called by: .claude/hooks/user-prompt-submit.sh
Author: EBF Framework
Date: 2026-02-16
Layer: Meta (Immune System Gateway)
SSOT: data/knowledge/canonical/three-layer-architecture.yaml
Virus Framework: data/knowledge/canonical/virus-definition.yaml
"""

import sys
import json
import signal
from pathlib import Path
from typing import Optional, List, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Maximum time for orchestrator execution (seconds)
ORCHESTRATOR_TIMEOUT = 8

# Minimum keyword score to trigger orchestrator
TRIGGER_THRESHOLD = 0.5


# ---------------------------------------------------------------------------
# Keyword Detection (mirrored from orchestrator._match_keywords)
# ---------------------------------------------------------------------------

# Each group: (keywords, parameter_id, base_score)
# Score logic: 1 keyword match = base_score, 2+ = base_score + bonus
_KEYWORD_GROUPS: List[Tuple[tuple, str, float]] = [
    # Core behavioral parameters
    # German forms use ae/oe/ue (prompt is umlaut-normalized before matching)
    (("loss", "aversion", "verlustaversion", "verlust",
      "verlustangst", "verlustaversiv"), "PAR-BEH-001", 0.9),
    (("crowding", "crowd", "intrinsic", "extrinsic",
      "verdraengung", "verdraengen", "verdraengt",
      "intrinsisch", "intrinsische", "extrinsisch", "extrinsische"),
     "PAR-BEH-002", 0.85),
    (("present", "bias", "hyperbolic", "discounting", "impatience",
      "geduld", "zeitpraeferenz", "gegenwartspraeferenz",
      "ungeduld", "gegenwartsverzerrung"), "PAR-BEH-003", 0.85),
    (("inequity", "inequality", "fairness", "unfairness",
      "disadvantageous", "ungleichheit",
      "ungerecht", "ungerechtigkeit", "gerechtigkeit"), "PAR-BEH-012", 0.85),
    (("advantageous", "guilt", "schuld", "vorteilhaft",
      "schuldgefuehl", "vorteilhafte"), "PAR-BEH-013", 0.8),
    (("identity", "identitaet", "self", "selbst", "prescription",
      "selbstbild", "selbstkonzept"), "PAR-BEH-009", 0.8),
    (("image", "reputation", "signaling", "visibility", "ruf",
      "sichtbarkeit", "ansehen"), "PAR-BEH-014", 0.85),
    (("exclusion", "ostracism", "ausschluss", "belonging",
      "zugehoerigkeit", "ausgrenzung"), "PAR-BEH-011", 0.85),
    (("rejection", "stigma", "ablehnung", "welfare", "sozialhilfe",
      "stigmatisierung", "zurueckweisung"), "PAR-BEH-016", 0.85),
    (("network", "segregation", "homophily", "netzwerk",
      "netzwerkeffekt"), "PAR-BEH-015", 0.8),
    (("trust", "vertrauen", "institutional",
      "institutionell", "misstrauen"), "PAR-CTX-002", 0.7),
    (("taboo", "tabu", "finance", "money", "geld", "finanzen",
      "finanziell", "finanzielle"), "PAR-CTX-001", 0.7),
    (("privacy", "datenschutz", "privatsphaere"), "PAR-CTX-003", 0.8),
    (("addiction", "sucht", "smoking", "rauchen",
      "abhaengigkeit", "suchtverhalten"), "PAR-BEH-004", 0.85),
    (("shadow", "opportunity", "schattenpreis"), "PAR-TA-001", 0.7),
    (("complementarity", "komplementaritaet", "interaction", "synergy",
      "wechselwirkung", "zusammenspiel"), "PAR-COMP-001", 0.8),
    # Risk aversion
    (("risk", "risiko", "risikoaversion", "risikoscheu"), "PAR-BEH-001", 0.7),
]

# High-confidence direct triggers (always trigger, no scoring needed)
_DIRECT_TRIGGERS = [
    "par-",       # Direct parameter ID reference
    "par_",       # Alternative format
    "lambda_",    # Greek symbol reference
    "theta_",     # Greek symbol reference
    "beta_",      # Greek symbol reference
    "gamma_",     # Greek symbol reference
]

# Question amplifiers: boost score when combined with keywords
# Note: prompt is checked in both original and umlaut-normalized form
_QUESTION_AMPLIFIERS = [
    "wie stark", "wie hoch", "wie gross",
    "how strong", "how much", "how high",
    "was ist", "what is",
    "wert", "value", "parameter",
    "schaetzung", "estimate",
    "wie koennen", "wie können",
    "warum", "weshalb",
    "welchen einfluss", "welche rolle",
]

# Skip patterns: never trigger for these
_SKIP_PATTERNS = [
    "commit", "push", "pull", "merge", "git ",
    "implementier", "erstelle", "create", "fix",
    "compile", "/compile", "/convert", "/check",
    "delete", "remove",
]


def _normalize_umlauts(text: str) -> str:
    """Normalize German umlauts and ß to ASCII equivalents."""
    return (text
            .replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
            .replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue")
            .replace("ß", "ss"))


def detect_parameter_query(prompt: str) -> Optional[Dict]:
    """
    Detect if a user prompt contains parameter-relevant keywords.

    Returns:
        None if no parameter keywords detected
        Dict with {triggered: True, query: str, matches: [...], score: float}
    """
    prompt_lower = prompt.lower().strip()
    # Normalize umlauts for German keyword matching (ä→ae, ö→oe, ü→ue, ß→ss)
    prompt_normalized = _normalize_umlauts(prompt_lower)

    # Skip patterns: check both original and normalized
    for skip in _SKIP_PATTERNS:
        if skip in prompt_lower or skip in prompt_normalized:
            return None

    # Very short prompts: skip (likely commands or confirmations)
    if len(prompt_lower) < 10:
        return None

    # Tokenize both original and umlaut-normalized prompt for matching
    words = set(
        prompt_lower
        .replace(",", " ").replace("?", " ").replace("!", " ")
        .replace(".", " ").replace("(", " ").replace(")", " ")
        .split()
    ) | set(
        prompt_normalized
        .replace(",", " ").replace("?", " ").replace("!", " ")
        .replace(".", " ").replace("(", " ").replace(")", " ")
        .split()
    )

    # Strategy 1: Direct trigger (PAR-xxx, lambda_, etc.)
    for trigger in _DIRECT_TRIGGERS:
        if trigger in prompt_lower:
            return {
                "triggered": True,
                "query": prompt,
                "matches": [{"reason": f"Direct reference: {trigger}", "score": 1.0}],
                "score": 1.0,
            }

    # Strategy 2: Keyword group matching with scoring
    matches = []
    best_score = 0.0

    for keyword_group, param_id, base_score in _KEYWORD_GROUPS:
        overlap = words & set(keyword_group)
        if overlap:
            bonus = min(len(overlap) * 0.05, 0.15)
            score = base_score + bonus
            matches.append({
                "parameter_id": param_id,
                "keywords": sorted(overlap),
                "reason": f"Keywords: {', '.join(sorted(overlap))}",
                "score": round(score, 3),
            })
            best_score = max(best_score, score)

    # Strategy 3: Question amplifier bonus (check both original and normalized)
    amplifier_bonus = 0.0
    for amp in _QUESTION_AMPLIFIERS:
        if amp in prompt_lower or amp in prompt_normalized:
            amplifier_bonus = 0.15
            break

    final_score = best_score + amplifier_bonus

    if final_score >= TRIGGER_THRESHOLD and matches:
        return {
            "triggered": True,
            "query": prompt,
            "matches": sorted(matches, key=lambda m: m["score"], reverse=True),
            "score": round(final_score, 3),
            "amplifier": amplifier_bonus > 0,
        }

    return None


def run_orchestrator(query: str, timeout: int = ORCHESTRATOR_TIMEOUT) -> Optional[Dict]:
    """
    Run the orchestrator with timeout protection.

    Two-phase resolution:
      1. --query → get matches (array of candidates)
      2. --id <best_match> → get full parameter data (flat dict)

    Returns parsed JSON result or None on failure/timeout.
    """
    import subprocess

    orchestrator_path = REPO_ROOT / "scripts" / "orchestrator.py"
    if not orchestrator_path.exists():
        return None

    try:
        # Phase 1: Find matches via natural language query
        result = subprocess.run(
            [sys.executable, str(orchestrator_path), "--query", query, "--json"],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(REPO_ROOT),
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None

        data = json.loads(result.stdout)

        # Case 1: Orchestrator returned a fully resolved result
        # (has "result" key with nested parameter data)
        if "result" in data and isinstance(data.get("result"), dict):
            full_data = data["result"]
            prov = data.get("provenance", {})
            if prov:
                full_data["provenance"] = prov.get("layers_used", "")
            l2 = data.get("layer2_registry", {})
            if l2:
                full_data.setdefault("registry_value", l2.get("value"))
                full_data.setdefault("source", l2.get("source", ""))
            l1 = data.get("layer1_pct", {})
            if l1:
                full_data["pct_result"] = l1.get("value")
                full_data["anchor_context"] = l1.get("anchor_context", "")
            return full_data

        # Case 2: Flat result (direct match at top level)
        if "parameter_id" in data and "matches" not in data:
            return data

        # Case 3: Matches array — pick best and resolve via --id
        matches = data.get("matches", [])
        if not matches:
            return None

        best_match = matches[0]  # Already sorted by score
        param_id = best_match.get("parameter_id")
        if not param_id:
            return None

        # Phase 2: Get full parameter data via --id
        result2 = subprocess.run(
            [sys.executable, str(orchestrator_path), "--id", param_id, "--json"],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(REPO_ROOT),
        )
        if result2.returncode == 0 and result2.stdout.strip():
            raw = json.loads(result2.stdout)
            # Orchestrator nests data under 'result' — flatten for format_output
            full_data = raw.get("result", raw)
            # Merge provenance and layer info
            prov = raw.get("provenance", {})
            if prov:
                full_data["provenance"] = prov.get("layers_used", "")
            l2 = raw.get("layer2_registry", {})
            if l2:
                full_data.setdefault("registry_value", l2.get("value"))
                full_data.setdefault("source", l2.get("source", ""))
            l1 = raw.get("layer1_pct", {})
            if l1:
                full_data["pct_result"] = l1.get("value")
                full_data["anchor_context"] = l1.get("anchor_context", "")
            # Preserve match reason for transparency
            full_data["match_reason"] = best_match.get("match_reason", "")
            full_data["match_score"] = best_match.get("score", 0)
            return full_data

        # Fallback: return the best match info even without full data
        return best_match

    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return None

    return None


def format_output(detection: Dict, orchestrator_result: Optional[Dict]) -> str:
    """
    Format the immune gateway output for Claude's context.

    This output is injected into Claude's context BEFORE it generates
    a response, ensuring Layer 1 data is available.
    """
    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append("  IMMUNE GATEWAY — Layer 1 Pre-Computation (autonomous)")
    lines.append("  Virus Framework: The host no longer decides.")
    lines.append("=" * 72)

    if orchestrator_result:
        r = orchestrator_result

        # Parameter info
        pid = r.get("parameter_id", "")
        symbol = r.get("symbol", "")
        name = r.get("name", "")
        if pid or symbol:
            lines.append(f"  Parameter: {pid} ({symbol}) — {name}")

        # Registry value (Layer 2)
        reg = r.get("registry_value", r.get("value"))
        if reg is not None:
            rng = r.get("range", r.get("plausible_range", ""))
            tier = r.get("evidence_tier", r.get("tier", ""))
            lines.append(f"  Registry Value:  {reg}")
            if rng:
                lines.append(f"  Range:           {rng}")
            if tier:
                lines.append(f"  Evidence Tier:   {tier}")

        # PCT result (Layer 1)
        pct = r.get("pct_result", r.get("transformed_value"))
        if pct is not None:
            lines.append(f"  PCT Transform:   {pct}")
            anchor = r.get("anchor_context", "")
            if anchor:
                lines.append(f"  Anchor Context:  {anchor}")

        # Source info
        source = r.get("source", r.get("sources", ""))
        if source:
            if isinstance(source, list):
                source = ", ".join(source[:3])
            lines.append(f"  Source:          {source}")

        # Provenance
        provenance = r.get("provenance", r.get("pipeline", ""))
        if provenance:
            lines.append(f"  Pipeline:        {provenance}")

        lines.append("")
        lines.append("  DIRECTIVE: Use THESE values. Do NOT cite from LLM memory.")
        lines.append("  Layer: 1+2 (formal computation + registry)")
        lines.append("  Susceptibility: 0.0 (immune)")

    else:
        # Orchestrator failed or no result — still signal detection
        matches_list = detection.get("matches", [])
        kw = matches_list[0].get("keywords", []) if matches_list else []
        lines.append(f"  Detected keywords: {', '.join(kw) if kw else 'parameter reference'}")
        lines.append(f"  Score: {detection.get('score', 0)}")
        lines.append("")
        lines.append("  Orchestrator returned no result.")
        lines.append("  DIRECTIVE: Use /query-parameter or orchestrator.py for values.")
        lines.append("  Do NOT cite parameter values from LLM memory.")

    lines.append("=" * 72)
    lines.append("")

    return "\n".join(lines)


def self_test() -> bool:
    """Run self-test to verify keyword detection works."""
    test_cases = [
        # (prompt, should_trigger, description)
        ("What is loss aversion?", True, "Basic behavioral keyword"),
        ("How strong is present bias?", True, "Behavioral keyword + amplifier"),
        ("PAR-BEH-001 value", True, "Direct parameter ID"),
        ("lambda_R in welfare context", True, "Greek symbol reference"),
        ("git push origin main", False, "Git command (skip)"),
        ("ok", False, "Short confirmation (skip)"),
        ("erstelle eine Datei", False, "Technical command (skip)"),
        ("Wie stark ist Verlustaversion?", True, "German behavioral keyword + amplifier"),
        ("Tell me about trust and fairness", True, "Multiple behavioral keywords"),
        ("How is the weather today?", False, "Non-parameter question"),
        ("What about rejection stigma?", True, "Stigma keyword"),
        # German umlaut tests (NEW — umlaut normalization)
        ("Wie können wir intrinsische Motivation schützen?", True, "German umlaut: intrinsische"),
        ("Verdrängt extrinsische Belohnung die Motivation?", True, "German umlaut: Verdrängt"),
        ("Welche Rolle spielt Zugehörigkeit?", True, "German umlaut: Zugehörigkeit"),
    ]

    passed = 0
    failed = 0

    print("\n  Immune Gateway Self-Test")
    print("  " + "-" * 50)

    for prompt, expected, desc in test_cases:
        result = detect_parameter_query(prompt)
        triggered = result is not None
        ok = triggered == expected
        status = "PASS" if ok else "FAIL"
        if not ok:
            failed += 1
        else:
            passed += 1
        score = f" (score={result['score']})" if result else ""
        print(f"  [{status}] {desc}")
        print(f"         Prompt: \"{prompt}\"")
        print(f"         Expected: {expected}, Got: {triggered}{score}")

    print(f"\n  Results: {passed}/{passed + failed} passed")
    if failed > 0:
        print(f"  WARNING: {failed} tests failed!")
    print()

    return failed == 0


def main():
    """
    Main entry point. Called by UserPromptSubmit hook.

    Reads user prompt from argv[1] or stdin.
    Outputs formatted Layer 1 pre-computation to stdout (if triggered).
    Exits silently if no parameter keywords detected.
    """
    # Handle --test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = self_test()
        sys.exit(0 if success else 1)

    # Get user prompt
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = sys.stdin.read().strip()

    if not prompt:
        sys.exit(0)

    # Step 1: Detect parameter keywords
    detection = detect_parameter_query(prompt)
    if detection is None:
        sys.exit(0)  # No parameter keywords — exit silently

    # Step 2: Run orchestrator (with timeout)
    orchestrator_result = run_orchestrator(prompt)

    # Step 3: Format and output
    output = format_output(detection, orchestrator_result)
    print(output)


if __name__ == "__main__":
    main()
