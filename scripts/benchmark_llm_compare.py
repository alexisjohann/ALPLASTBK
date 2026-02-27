#!/usr/bin/env python3
"""
EBF Benchmark: Claude vs. OpenAI LLM Comparison

Sends identical questions to OpenAI (GPT-4o) and optionally Anthropic (Claude)
to produce structured comparison reports.

Usage:
    # Single question
    python scripts/benchmark_llm_compare.py --question "Was ist Loss Aversion?"

    # From benchmark config file
    python scripts/benchmark_llm_compare.py --config data/benchmark-questions.yaml

    # Specific question from config
    python scripts/benchmark_llm_compare.py --config data/benchmark-questions.yaml --id BQ-001

    # With specific models
    python scripts/benchmark_llm_compare.py --question "..." --openai-model gpt-4o --anthropic-model claude-sonnet-4-5-20250929

Environment:
    OPENAI_API_KEY     - Required for OpenAI calls
    ANTHROPIC_API_KEY  - Optional for Anthropic calls (fair comparison)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)


# ---------------------------------------------------------------------------
# API Callers
# ---------------------------------------------------------------------------

def call_openai(question: str, model: str = "gpt-4o", system_prompt: str = "",
                temperature: float = 0.3, max_tokens: int = 4096) -> dict:
    """Call OpenAI API and return structured result."""
    try:
        import openai
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"error": "OPENAI_API_KEY not set", "model": model}

    client = openai.OpenAI(api_key=api_key)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": question})

    t0 = time.time()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        elapsed = time.time() - t0

        choice = response.choices[0]
        usage = response.usage

        return {
            "model": model,
            "provider": "openai",
            "answer": choice.message.content,
            "finish_reason": choice.finish_reason,
            "tokens_prompt": usage.prompt_tokens if usage else None,
            "tokens_completion": usage.completion_tokens if usage else None,
            "tokens_total": usage.total_tokens if usage else None,
            "latency_seconds": round(elapsed, 2),
            "temperature": temperature,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except Exception as e:
        return {"error": str(e), "model": model, "provider": "openai"}


def call_anthropic(question: str, model: str = "claude-sonnet-4-5-20250929",
                   system_prompt: str = "", temperature: float = 0.3,
                   max_tokens: int = 4096) -> dict:
    """Call Anthropic API and return structured result."""
    try:
        import anthropic
    except ImportError:
        return {"error": "anthropic package not installed", "model": model, "provider": "anthropic"}

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set", "model": model, "provider": "anthropic"}

    client = anthropic.Anthropic(api_key=api_key)

    t0 = time.time()
    try:
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": question}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = client.messages.create(**kwargs)
        elapsed = time.time() - t0

        answer_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                answer_text += block.text

        return {
            "model": model,
            "provider": "anthropic",
            "answer": answer_text,
            "finish_reason": response.stop_reason,
            "tokens_prompt": response.usage.input_tokens if response.usage else None,
            "tokens_completion": response.usage.output_tokens if response.usage else None,
            "tokens_total": (
                (response.usage.input_tokens + response.usage.output_tokens)
                if response.usage else None
            ),
            "latency_seconds": round(elapsed, 2),
            "temperature": temperature,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    except Exception as e:
        return {"error": str(e), "model": model, "provider": "anthropic"}


# ---------------------------------------------------------------------------
# Comparison Report
# ---------------------------------------------------------------------------

def generate_comparison_report(question: str, question_id: str,
                                results: list, category: str = "",
                                system_prompt: str = "") -> str:
    """Generate a Markdown comparison report."""
    lines = []
    lines.append(f"# EBF Benchmark: LLM Comparison Report")
    lines.append(f"")
    lines.append(f"**Benchmark ID:** {question_id}")
    lines.append(f"**Datum:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if category:
        lines.append(f"**Kategorie:** {category}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Frage")
    lines.append(f"")
    lines.append(f"> {question}")
    lines.append(f"")
    if system_prompt:
        lines.append(f"**System Prompt:** {system_prompt[:200]}...")
        lines.append(f"")

    # Metrics table
    lines.append(f"## Metriken")
    lines.append(f"")
    lines.append(f"| Metrik | " + " | ".join(r.get("model", "?") for r in results) + " |")
    lines.append(f"|--------|" + "|".join("-----" for _ in results) + "|")
    lines.append(f"| Provider | " + " | ".join(r.get("provider", "?") for r in results) + " |")
    lines.append(f"| Latenz (s) | " + " | ".join(str(r.get("latency_seconds", "?")) for r in results) + " |")
    lines.append(f"| Tokens (prompt) | " + " | ".join(str(r.get("tokens_prompt", "?")) for r in results) + " |")
    lines.append(f"| Tokens (completion) | " + " | ".join(str(r.get("tokens_completion", "?")) for r in results) + " |")
    lines.append(f"| Tokens (total) | " + " | ".join(str(r.get("tokens_total", "?")) for r in results) + " |")
    lines.append(f"| Temperatur | " + " | ".join(str(r.get("temperature", "?")) for r in results) + " |")
    lines.append(f"")

    # Answers
    for r in results:
        model_name = r.get("model", "Unknown")
        provider = r.get("provider", "unknown")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## Antwort: {model_name} ({provider})")
        lines.append(f"")
        if "error" in r:
            lines.append(f"**ERROR:** {r['error']}")
        else:
            lines.append(r.get("answer", "(keine Antwort)"))
        lines.append(f"")

    # Comparison placeholder
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Vergleichs-Analyse (manuell auszufuellen)")
    lines.append(f"")
    lines.append(f"| Dimension | " + " | ".join(r.get("model", "?") for r in results) + " | Gewinner |")
    lines.append(f"|-----------|" + "|".join("-----" for _ in results) + "|----------|")
    lines.append(f"| Korrektheit | | " + "| " * (len(results) - 1) + "| |")
    lines.append(f"| Kontextverstaendnis | | " + "| " * (len(results) - 1) + "| |")
    lines.append(f"| Parametrisierung | | " + "| " * (len(results) - 1) + "| |")
    lines.append(f"| Quellenangaben | | " + "| " * (len(results) - 1) + "| |")
    lines.append(f"| Strukturiertheit | | " + "| " * (len(results) - 1) + "| |")
    lines.append(f"| EBF-Konformitaet | | " + "| " * (len(results) - 1) + "| |")
    lines.append(f"")
    lines.append(f"**Gesamtbewertung:** _TODO_")
    lines.append(f"")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_benchmark(question: str, question_id: str, category: str = "",
                  system_prompt: str = "", openai_model: str = "gpt-4o",
                  anthropic_model: str = "claude-sonnet-4-5-20250929",
                  skip_anthropic: bool = False, output_dir: str = "outputs/benchmarks") -> str:
    """Run a single benchmark comparison and save report."""

    print(f"\n{'='*60}")
    print(f"  EBF BENCHMARK: {question_id}")
    print(f"{'='*60}")
    print(f"  Frage: {question[:80]}...")
    print()

    results = []

    # OpenAI
    print(f"  [1/2] Calling OpenAI ({openai_model})...", end=" ", flush=True)
    r_openai = call_openai(question, model=openai_model,
                           system_prompt=system_prompt)
    if "error" in r_openai:
        print(f"ERROR: {r_openai['error']}")
    else:
        print(f"OK ({r_openai['latency_seconds']}s, {r_openai['tokens_total']} tokens)")
    results.append(r_openai)

    # Anthropic (optional)
    if not skip_anthropic:
        print(f"  [2/2] Calling Anthropic ({anthropic_model})...", end=" ", flush=True)
        r_anthropic = call_anthropic(question, model=anthropic_model,
                                     system_prompt=system_prompt)
        if "error" in r_anthropic:
            print(f"SKIP: {r_anthropic['error']}")
        else:
            print(f"OK ({r_anthropic['latency_seconds']}s, {r_anthropic['tokens_total']} tokens)")
        results.append(r_anthropic)
    else:
        print(f"  [2/2] Anthropic skipped (--skip-anthropic)")

    # Generate report
    report = generate_comparison_report(
        question=question,
        question_id=question_id,
        results=results,
        category=category,
        system_prompt=system_prompt,
    )

    # Save
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{question_id}_{date_str}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    # Also save raw JSON
    raw_path = os.path.join(output_dir, f"{question_id}_{date_str}.json")
    raw_data = {
        "benchmark_id": question_id,
        "question": question,
        "category": category,
        "system_prompt": system_prompt,
        "results": results,
        "generated": datetime.utcnow().isoformat() + "Z",
    }
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    print(f"\n  Report: {filepath}")
    print(f"  Raw:    {raw_path}")
    print(f"{'='*60}\n")

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="EBF Benchmark: Claude vs. OpenAI LLM Comparison"
    )
    parser.add_argument("--question", "-q", help="Single question to benchmark")
    parser.add_argument("--config", "-c", help="YAML config with benchmark questions")
    parser.add_argument("--id", help="Run specific question ID from config")
    parser.add_argument("--openai-model", default="gpt-4o",
                        help="OpenAI model (default: gpt-4o)")
    parser.add_argument("--anthropic-model", default="claude-sonnet-4-5-20250929",
                        help="Anthropic model (default: claude-sonnet-4-5-20250929)")
    parser.add_argument("--skip-anthropic", action="store_true",
                        help="Skip Anthropic API call (only OpenAI)")
    parser.add_argument("--system-prompt", "-s", default="",
                        help="System prompt for both models")
    parser.add_argument("--output-dir", "-o", default="outputs/benchmarks",
                        help="Output directory (default: outputs/benchmarks)")
    parser.add_argument("--list", action="store_true",
                        help="List available benchmark questions from config")

    args = parser.parse_args()

    # List mode
    if args.list and args.config:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
        print("\nVerfuegbare Benchmark-Fragen:")
        print(f"{'ID':<12} {'Kategorie':<20} {'Frage'}")
        print("-" * 70)
        for q in config.get("questions", []):
            print(f"{q['id']:<12} {q.get('category', '-'):<20} {q['question'][:50]}...")
        return

    # Single question mode
    if args.question:
        run_benchmark(
            question=args.question,
            question_id=f"BQ-ADHOC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            system_prompt=args.system_prompt,
            openai_model=args.openai_model,
            anthropic_model=args.anthropic_model,
            skip_anthropic=args.skip_anthropic,
            output_dir=args.output_dir,
        )
        return

    # Config mode
    if args.config:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        sys_prompt = config.get("system_prompt", args.system_prompt)
        questions = config.get("questions", [])

        if args.id:
            questions = [q for q in questions if q["id"] == args.id]
            if not questions:
                print(f"ERROR: Question ID '{args.id}' not found in config")
                sys.exit(1)

        print(f"\n  EBF BENCHMARK SUITE")
        print(f"  {len(questions)} Fragen zu verarbeiten")
        print(f"  OpenAI:    {args.openai_model}")
        if not args.skip_anthropic:
            print(f"  Anthropic: {args.anthropic_model}")
        print()

        reports = []
        for q in questions:
            q_system = q.get("system_prompt", sys_prompt)
            filepath = run_benchmark(
                question=q["question"],
                question_id=q["id"],
                category=q.get("category", ""),
                system_prompt=q_system,
                openai_model=args.openai_model,
                anthropic_model=args.anthropic_model,
                skip_anthropic=args.skip_anthropic,
                output_dir=args.output_dir,
            )
            reports.append(filepath)

        print(f"\n  BENCHMARK ABGESCHLOSSEN")
        print(f"  {len(reports)} Reports erstellt in {args.output_dir}/")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
