#!/usr/bin/env python3
"""
BEATRIX Legal Orchestrator — Parallel DACH+EU Legal Query
==========================================================

Queries ALL 4 legal databases in parallel and merges results.
This is the Layer 2 entry point for legal parameter lookup.

Architecture:
    User Query → Orchestrator → [EUR-Lex, RIS, Fedlex, GII] → Merged Results → Layer 1

Usage:
    # Search across all jurisdictions
    python scripts/legal/legal_orchestrator.py --search "Sorgfaltspflicht Lieferkette"

    # Search specific jurisdiction
    python scripts/legal/legal_orchestrator.py --search "due diligence" --jurisdiction eu

    # Extract thresholds from all jurisdictions
    python scripts/legal/legal_orchestrator.py --search "Arbeitnehmer" --extract-thresholds

    # Status of all APIs
    python scripts/legal/legal_orchestrator.py --status

    # Bulk download everything (parallel)
    python scripts/legal/legal_orchestrator.py --bulk-all --output data/legal/
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

# Import individual connectors
sys.path.insert(0, str(Path(__file__).parent.parent))
from legal.ris_ogd_connector import RisOgdClient, extract_thresholds
from legal.eurlex_connector import EurLexClient
from legal.fedlex_connector import FedlexClient
from legal.gii_connector import GiiClient


class LegalOrchestrator:
    """Parallel orchestrator for DACH+EU legal databases."""

    def __init__(self):
        self.clients = {
            "eu": {"client": EurLexClient(), "name": "EUR-Lex CELLAR", "flag": "🇪🇺"},
            "at": {"client": RisOgdClient(), "name": "RIS OGD v2.6", "flag": "🇦🇹"},
            "ch": {"client": FedlexClient(), "name": "Fedlex SPARQL", "flag": "🇨🇭"},
            "de": {"client": GiiClient(), "name": "gesetze-im-internet.de", "flag": "🇩🇪"},
        }

    def search_all(self, query: str, jurisdictions: list[str] = None) -> dict:
        """Search all databases in parallel."""
        if jurisdictions is None:
            jurisdictions = list(self.clients.keys())

        results = {}
        start = time.time()

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            for jur in jurisdictions:
                if jur not in self.clients:
                    continue
                client_info = self.clients[jur]
                futures[executor.submit(self._search_one, jur, client_info, query)] = jur

            for future in as_completed(futures):
                jur = futures[future]
                try:
                    results[jur] = future.result()
                except Exception as e:
                    results[jur] = {"error": str(e), "hits": 0}

        elapsed = time.time() - start
        return {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": round(elapsed, 2),
            "jurisdictions": results,
        }

    def _search_one(self, jur: str, client_info: dict, query: str) -> dict:
        """Search a single database."""
        client = client_info["client"]
        name = client_info["name"]

        if jur == "eu":
            result = client.search_legislation(query)
            bindings = result.get("results", {}).get("bindings", [])
            return {
                "source": name,
                "hits": len(bindings),
                "results": [
                    {
                        "title": b.get("title", {}).get("value", ""),
                        "celex": b.get("celex", {}).get("value", ""),
                        "date": b.get("date", {}).get("value", ""),
                    }
                    for b in bindings[:20]
                ],
            }

        elif jur == "at":
            result = client.search("bundesrecht", query)
            docs = client._extract_documents(result)
            hits = client._count_hits(result)
            return {
                "source": name,
                "hits": hits,
                "results": [
                    {
                        "document_id": d.get("Data", {}).get("Dokumentnummer", ""),
                        "title": d.get("Data", {}).get("Metadaten", {}).get("BrKons", {}).get("Titel",
                                 d.get("Data", {}).get("Metadaten", {}).get("Kurzinformation", "")),
                    }
                    for d in docs[:20]
                ],
            }

        elif jur == "ch":
            result = client.search_legislation(query)
            bindings = result.get("results", {}).get("bindings", [])
            return {
                "source": name,
                "hits": len(bindings),
                "results": [
                    {
                        "title": b.get("title", {}).get("value", ""),
                        "sr": b.get("sr", {}).get("value", ""),
                        "date": b.get("dateDocument", {}).get("value", ""),
                    }
                    for b in bindings[:20]
                ],
            }

        elif jur == "de":
            results = client.search_toc(query)
            return {
                "source": name,
                "hits": len(results),
                "results": [
                    {
                        "title": r["title"],
                        "abbreviation": r["abbreviation"],
                    }
                    for r in results[:20]
                ],
            }

        return {"source": name, "hits": 0, "results": []}

    def status_all(self) -> dict:
        """Check all APIs in parallel."""
        results = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            for jur, info in self.clients.items():
                futures[executor.submit(info["client"].status)] = (jur, info)

            for future in as_completed(futures):
                jur, info = futures[future]
                try:
                    status = future.result()
                    results[jur] = {
                        "flag": info["flag"],
                        "name": info["name"],
                        **status,
                    }
                except Exception as e:
                    results[jur] = {
                        "flag": info["flag"],
                        "name": info["name"],
                        "status": "ERROR",
                        "error": str(e),
                    }
        return results


def format_search_results(data: dict) -> str:
    """Format merged search results."""
    lines = [
        "",
        "=" * 70,
        f"  BEATRIX LEGAL — Parallel Search: '{data['query']}'",
        f"  Time: {data['elapsed_seconds']}s | {data['timestamp']}",
        "=" * 70,
    ]

    total_hits = 0
    for jur, result in data.get("jurisdictions", {}).items():
        flag = {"eu": "🇪🇺", "at": "🇦🇹", "ch": "🇨🇭", "de": "🇩🇪"}.get(jur, "")
        source = result.get("source", jur)
        hits = result.get("hits", 0)
        total_hits += hits

        if "error" in result:
            lines.append(f"\n  {flag} {source}: ❌ {result['error']}")
            continue

        lines.append(f"\n  {flag} {source}: {hits} Treffer")
        lines.append(f"  {'-'*60}")

        for i, r in enumerate(result.get("results", [])[:5], 1):
            title = r.get("title", "?")[:65]
            extra = r.get("celex", r.get("sr", r.get("abbreviation", r.get("document_id", ""))))
            lines.append(f"    [{i}] {title}")
            if extra:
                lines.append(f"        → {extra}")

        remaining = hits - 5
        if remaining > 0:
            lines.append(f"    ... +{remaining} weitere")

    lines.append(f"\n{'='*70}")
    lines.append(f"  TOTAL: {total_hits} Treffer aus {len(data.get('jurisdictions', {}))} Jurisdiktionen")
    lines.append(f"  Abfragezeit: {data['elapsed_seconds']} Sekunden (parallel)")
    lines.append("=" * 70)

    return "\n".join(lines)


def format_status(status: dict) -> str:
    """Format status check."""
    lines = [
        "",
        "=" * 70,
        "  BEATRIX LEGAL — API STATUS",
        "=" * 70,
    ]
    for jur, info in status.items():
        flag = info.get("flag", "")
        name = info.get("name", jur)
        st = info.get("status", "?")
        icon = "✅" if st in ("OK", 200) else "❌"
        extra = ""
        if "laws_count" in info:
            extra = f" ({info['laws_count']} laws)"
        if "sample_hits" in info:
            extra = f" (~{info['sample_hits']} sample hits)"
        lines.append(f"  {icon} {flag} {name:30s} {st}{extra}")

    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="BEATRIX Legal Orchestrator — Parallel DACH+EU Query")
    parser.add_argument("--search", type=str, help="Search across all jurisdictions")
    parser.add_argument("--jurisdiction", type=str, nargs="+", choices=["eu", "at", "ch", "de"],
                        help="Limit to specific jurisdictions")
    parser.add_argument("--extract-thresholds", action="store_true", help="Extract thresholds")
    parser.add_argument("--status", action="store_true", help="Check all APIs")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    orchestrator = LegalOrchestrator()

    if args.status:
        status = orchestrator.status_all()
        print(json.dumps(status, indent=2, ensure_ascii=False) if args.json else format_status(status))
        return

    if args.search:
        results = orchestrator.search_all(args.search, args.jurisdiction)
        print(json.dumps(results, indent=2, ensure_ascii=False) if args.json else format_search_results(results))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
