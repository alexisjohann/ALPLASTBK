#!/usr/bin/env python3
"""
EUR-Lex CELLAR SPARQL Connector — EU Legal Database
====================================================

Connects to the EU Publications Office CELLAR SPARQL endpoint.
Free, no authentication, 25,000+ EU legal acts.

Endpoint: https://publications.europa.eu/webapi/rdf/sparql

Usage:
    # Search EU directives
    python scripts/legal/eurlex_connector.py --search "supply chain due diligence"

    # Get CSDDD specifically
    python scripts/legal/eurlex_connector.py --celex 32024L1760

    # List all directives in force
    python scripts/legal/eurlex_connector.py --directives-in-force

    # Search CJEU case law
    python scripts/legal/eurlex_connector.py --caselaw "due diligence"

    # Status check
    python scripts/legal/eurlex_connector.py --status
"""

import argparse
import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

SPARQL_ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"


class EurLexClient:
    """Client for EUR-Lex CELLAR SPARQL endpoint."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/sparql-results+json",
            "User-Agent": "BEATRIX-Legal/0.1 (FehrAdvice EBF Framework)",
        })

    def sparql_query(self, query: str) -> dict:
        """Execute a SPARQL query against CELLAR."""
        response = self.session.get(
            SPARQL_ENDPOINT,
            params={"query": query},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    def search_legislation(self, keywords: str, limit: int = 50) -> dict:
        """Search EU legislation by keywords."""
        query = f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT ?work ?title ?celex ?date ?type WHERE {{
            ?work cdm:work_has_resource-type ?type .
            ?work cdm:resource_legal_id_celex ?celex .
            ?work cdm:work_date_document ?date .
            ?exp cdm:expression_belongs_to_work ?work .
            ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
            ?exp cdm:expression_title ?title .
            FILTER(CONTAINS(LCASE(?title), LCASE("{keywords}")))
        }}
        ORDER BY DESC(?date)
        LIMIT {limit}
        """
        return self.sparql_query(query)

    def get_by_celex(self, celex: str) -> dict:
        """Get a specific legal act by CELEX number."""
        query = f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>

        SELECT ?work ?title ?date ?type ?eli WHERE {{
            ?work cdm:resource_legal_id_celex "{celex}" .
            ?work cdm:work_date_document ?date .
            ?work cdm:work_has_resource-type ?type .
            OPTIONAL {{
                ?work cdm:resource_legal_eli ?eli .
            }}
            OPTIONAL {{
                ?exp cdm:expression_belongs_to_work ?work .
                ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
                ?exp cdm:expression_title ?title .
            }}
        }}
        LIMIT 10
        """
        return self.sparql_query(query)

    def directives_in_force(self, limit: int = 200) -> dict:
        """List all EU directives currently in force."""
        query = f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>

        SELECT DISTINCT ?celex ?title ?date WHERE {{
            ?work cdm:resource_legal_id_celex ?celex .
            ?work cdm:work_has_resource-type <http://publications.europa.eu/resource/authority/resource-type/DIR> .
            ?work cdm:work_date_document ?date .
            ?work cdm:resource_legal_in-force "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
            ?exp cdm:expression_belongs_to_work ?work .
            ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
            ?exp cdm:expression_title ?title .
        }}
        ORDER BY DESC(?date)
        LIMIT {limit}
        """
        return self.sparql_query(query)

    def search_caselaw(self, keywords: str, limit: int = 50) -> dict:
        """Search CJEU case law."""
        query = f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>

        SELECT DISTINCT ?work ?title ?celex ?date WHERE {{
            ?work cdm:work_has_resource-type <http://publications.europa.eu/resource/authority/resource-type/JUDG> .
            ?work cdm:resource_legal_id_celex ?celex .
            ?work cdm:work_date_document ?date .
            ?exp cdm:expression_belongs_to_work ?work .
            ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
            ?exp cdm:expression_title ?title .
            FILTER(CONTAINS(LCASE(?title), LCASE("{keywords}")))
        }}
        ORDER BY DESC(?date)
        LIMIT {limit}
        """
        return self.sparql_query(query)

    def status(self) -> dict:
        """Check SPARQL endpoint availability."""
        test_query = """
        SELECT (COUNT(*) AS ?count) WHERE {
            ?s ?p ?o .
        } LIMIT 1
        """
        try:
            result = self.sparql_query(test_query)
            return {"status": "OK", "endpoint": SPARQL_ENDPOINT}
        except Exception as e:
            return {"status": "ERROR", "endpoint": SPARQL_ENDPOINT, "error": str(e)}


def format_sparql_results(results: dict) -> str:
    """Format SPARQL JSON results for display."""
    lines = []
    bindings = results.get("results", {}).get("bindings", [])

    if not bindings:
        return "  No results found."

    for i, row in enumerate(bindings, 1):
        lines.append(f"\n{'='*70}")
        lines.append(f"  [{i}]")
        for key, val in row.items():
            value = val.get("value", "")
            # Truncate long URIs
            if value.startswith("http") and len(value) > 80:
                value = value[:77] + "..."
            lines.append(f"  {key}: {value}")

    lines.append(f"\n  Total: {len(bindings)} results")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="EUR-Lex CELLAR SPARQL Connector")
    parser.add_argument("--search", type=str, help="Search EU legislation by keywords")
    parser.add_argument("--celex", type=str, help="Get specific act by CELEX number")
    parser.add_argument("--directives-in-force", action="store_true", help="List all directives in force")
    parser.add_argument("--caselaw", type=str, help="Search CJEU case law")
    parser.add_argument("--status", action="store_true", help="Check endpoint status")
    parser.add_argument("--json", action="store_true", help="Raw JSON output")
    parser.add_argument("--limit", type=int, default=50, help="Max results")

    args = parser.parse_args()
    client = EurLexClient()

    if args.status:
        print(json.dumps(client.status(), indent=2))
        return

    result = None

    if args.search:
        print(f"\n  Searching EU legislation: '{args.search}'")
        result = client.search_legislation(args.search, args.limit)
    elif args.celex:
        print(f"\n  Fetching CELEX: {args.celex}")
        result = client.get_by_celex(args.celex)
    elif args.directives_in_force:
        print(f"\n  Fetching all directives in force...")
        result = client.directives_in_force(args.limit)
    elif args.caselaw:
        print(f"\n  Searching CJEU case law: '{args.caselaw}'")
        result = client.search_caselaw(args.caselaw, args.limit)
    else:
        parser.print_help()
        return

    if result:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_sparql_results(result))


if __name__ == "__main__":
    main()
