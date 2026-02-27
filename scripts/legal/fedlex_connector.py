#!/usr/bin/env python3
"""
Fedlex SPARQL Connector — Swiss Federal Law
============================================

Connects to Switzerland's Fedlex Linked Data SPARQL endpoint.
Free, no authentication, 258,000+ legal objects.

Endpoint: https://fedlex.data.admin.ch/sparqlendpoint
Ontology: JOLux (FRBR-based) — https://swiss.github.io/fedlex-jolux/

Usage:
    python scripts/legal/fedlex_connector.py --search "Sorgfaltspflicht"
    python scripts/legal/fedlex_connector.py --sr 220           # OR (Obligationenrecht)
    python scripts/legal/fedlex_connector.py --laws-in-force
    python scripts/legal/fedlex_connector.py --status
"""

import argparse
import json
import sys

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

SPARQL_ENDPOINT = "https://fedlex.data.admin.ch/sparqlendpoint"


class FedlexClient:
    """Client for Fedlex SPARQL endpoint."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/sparql-results+json",
            "User-Agent": "BEATRIX-Legal/0.1 (FehrAdvice EBF Framework)",
        })

    def sparql_query(self, query: str) -> dict:
        response = self.session.post(
            SPARQL_ENDPOINT,
            data={"query": query},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    def search_legislation(self, keywords: str, limit: int = 50, lang: str = "de") -> dict:
        """Search Swiss federal law by keywords."""
        query = f"""
        PREFIX jolux: <http://data.legilux.public.lu/resource/ontology/jolux#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?act ?title ?sr ?dateDocument WHERE {{
            ?act a jolux:ConsolidationAbstract .
            ?act jolux:classifiedByTaxonomyEntry ?entry .
            ?entry skos:notation ?sr .
            ?act jolux:dateDocument ?dateDocument .
            ?act rdfs:label ?title .
            FILTER(LANG(?title) = "{lang}")
            FILTER(CONTAINS(LCASE(?title), LCASE("{keywords}")))
        }}
        ORDER BY ?sr
        LIMIT {limit}
        """
        return self.sparql_query(query)

    def get_by_sr(self, sr_number: str) -> dict:
        """Get a law by its SR (Systematische Rechtssammlung) number."""
        query = f"""
        PREFIX jolux: <http://data.legilux.public.lu/resource/ontology/jolux#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?act ?title ?sr ?dateDocument ?dateEntryInForce WHERE {{
            ?act a jolux:ConsolidationAbstract .
            ?act jolux:classifiedByTaxonomyEntry ?entry .
            ?entry skos:notation "{sr_number}" .
            ?act jolux:dateDocument ?dateDocument .
            OPTIONAL {{ ?act jolux:dateEntryInForce ?dateEntryInForce . }}
            ?act rdfs:label ?title .
            FILTER(LANG(?title) = "de")
        }}
        LIMIT 10
        """
        return self.sparql_query(query)

    def laws_in_force(self, limit: int = 200, lang: str = "de") -> dict:
        """List Swiss federal laws currently in force."""
        query = f"""
        PREFIX jolux: <http://data.legilux.public.lu/resource/ontology/jolux#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?act ?title ?sr WHERE {{
            ?act a jolux:ConsolidationAbstract .
            ?act jolux:classifiedByTaxonomyEntry ?entry .
            ?entry skos:notation ?sr .
            ?act jolux:isRealizedBy ?expression .
            ?act rdfs:label ?title .
            FILTER(LANG(?title) = "{lang}")
        }}
        ORDER BY ?sr
        LIMIT {limit}
        """
        return self.sparql_query(query)

    def status(self) -> dict:
        query = "SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o . } LIMIT 1"
        try:
            result = self.sparql_query(query)
            return {"status": "OK", "endpoint": SPARQL_ENDPOINT}
        except Exception as e:
            return {"status": "ERROR", "endpoint": SPARQL_ENDPOINT, "error": str(e)}


def format_results(results: dict) -> str:
    lines = []
    bindings = results.get("results", {}).get("bindings", [])
    if not bindings:
        return "  No results found."

    for i, row in enumerate(bindings, 1):
        lines.append(f"\n{'='*70}")
        lines.append(f"  [{i}]")
        for key, val in row.items():
            value = val.get("value", "")
            if value.startswith("http") and len(value) > 80:
                value = value[:77] + "..."
            lines.append(f"  {key}: {value}")

    lines.append(f"\n  Total: {len(bindings)} results")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fedlex SPARQL Connector — Swiss Federal Law")
    parser.add_argument("--search", type=str, help="Search by keywords")
    parser.add_argument("--sr", type=str, help="Get law by SR number (e.g. 220 for OR)")
    parser.add_argument("--laws-in-force", action="store_true", help="List laws in force")
    parser.add_argument("--status", action="store_true", help="Check endpoint")
    parser.add_argument("--json", action="store_true", help="Raw JSON")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--lang", type=str, default="de", choices=["de", "fr", "it"])

    args = parser.parse_args()
    client = FedlexClient()

    if args.status:
        print(json.dumps(client.status(), indent=2))
        return

    result = None
    if args.search:
        print(f"\n  Searching Fedlex: '{args.search}'")
        result = client.search_legislation(args.search, args.limit, args.lang)
    elif args.sr:
        print(f"\n  Fetching SR {args.sr}")
        result = client.get_by_sr(args.sr)
    elif args.laws_in_force:
        result = client.laws_in_force(args.limit, args.lang)
    else:
        parser.print_help()
        return

    if result:
        print(json.dumps(result, indent=2) if args.json else format_results(result))


if __name__ == "__main__":
    main()
