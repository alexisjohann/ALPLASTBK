#!/usr/bin/env python3
"""
RIS OGD v2.6 Connector — Austrian Legal Database API
=====================================================

Connects to the Austrian Rechtsinformationssystem (RIS) Open Government Data API.
Free, no authentication, 2+ million legal documents.

API Documentation: https://data.bka.gv.at/ris/ogd/v2.6/Documents/Dokumentation_OGD-RIS_API.pdf

Usage:
    # Search federal law
    python scripts/legal/ris_ogd_connector.py --search "Sorgfaltspflicht" --db bundesrecht

    # Search with threshold extraction
    python scripts/legal/ris_ogd_connector.py --search "Arbeitnehmer" --db bundesrecht --extract-thresholds

    # Search court decisions
    python scripts/legal/ris_ogd_connector.py --search "Lieferkette" --db judikatur-vwgh

    # Bulk download all federal law
    python scripts/legal/ris_ogd_connector.py --bulk bundesrecht --output data/legal/at/

    # Show API status
    python scripts/legal/ris_ogd_connector.py --status
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

# ============================================================================
# API CONFIGURATION
# ============================================================================

BASE_URL = "https://data.bka.gv.at/ris/api/v2.6"

DATABASES = {
    "bundesrecht": {
        "endpoint": "/Bundesrecht",
        "description": "Consolidated Austrian Federal Law",
        "params": {
            "Suchworte": "",
            "Titel": "",
            "Index": "",
            "FassungVom": "",
            "DokumenteProSeite": "OneHundred",
            "Seitennummer": 1,
        },
    },
    "landesrecht": {
        "endpoint": "/Landesrecht",
        "description": "Austrian State/Provincial Law (all 9 Bundesländer)",
        "params": {
            "Suchworte": "",
            "Bundesland": "",  # Burgenland, Kaernten, NOe, OOe, Salzburg, Steiermark, Tirol, Vorarlberg, Wien
            "DokumenteProSeite": "OneHundred",
            "Seitennummer": 1,
        },
    },
    "judikatur-vfgh": {
        "endpoint": "/Judikatur/Vfgh",
        "description": "Constitutional Court (Verfassungsgerichtshof) since 1980",
        "params": {
            "Suchworte": "",
            "DokumenteProSeite": "OneHundred",
            "Seitennummer": 1,
        },
    },
    "judikatur-vwgh": {
        "endpoint": "/Judikatur/Vwgh",
        "description": "Administrative Court (Verwaltungsgerichtshof) since 1990",
        "params": {
            "Suchworte": "",
            "DokumenteProSeite": "OneHundred",
            "Seitennummer": 1,
        },
    },
    "judikatur-justiz": {
        "endpoint": "/Judikatur/Justiz",
        "description": "Supreme Court (OGH) + lower courts",
        "params": {
            "Suchworte": "",
            "DokumenteProSeite": "OneHundred",
            "Seitennummer": 1,
        },
    },
    "judikatur-bvwg": {
        "endpoint": "/Judikatur/Bvwg",
        "description": "Federal Administrative Court since 2014",
        "params": {
            "Suchworte": "",
            "DokumenteProSeite": "OneHundred",
            "Seitennummer": 1,
        },
    },
}

# ============================================================================
# THRESHOLD EXTRACTION PATTERNS
# ============================================================================

THRESHOLD_PATTERNS = [
    # Numeric thresholds with context
    (r"(?:mehr als|mindestens|über|ab|bis zu|höchstens|maximal)\s+(\d[\d.,\']*)\s+(Arbeitnehmer|Beschäftigte|Personen|Mitarbeiter)", "employee_threshold"),
    (r"(\d[\d.,\']*)\s+(?:EUR|Euro|€)", "monetary_threshold_eur"),
    (r"(\d[\d.,\']*)\s+(?:CHF|Franken)", "monetary_threshold_chf"),
    # Deadlines
    (r"(?:innerhalb|binnen|innert)\s+(?:von\s+)?(\d+)\s+(Tage[n]?|Wochen|Monate[n]?|Jahre[n]?)", "deadline"),
    (r"(unverzüglich|ohne Verzug|umgehend)", "deadline_immediate"),
    # Sanctions
    (r"(?:Geldstrafe|Busse|Bußgeld|Geldbuße|Strafe)\s+(?:bis zu|von|in Höhe von)\s+(\d[\d.,\']*)\s+(EUR|Euro|€|CHF)", "sanction_monetary"),
    (r"Freiheitsstrafe\s+(?:bis zu|von)\s+(\d+)\s+(Jahre[n]?|Monate[n]?)", "sanction_imprisonment"),
    # Scope/applicability
    (r"(?:gilt für|Anwendungsbereich|anwendbar auf)\s+(.{10,80}?)(?:\.|;)", "scope"),
    # Cross-references
    (r"(?:gemäss|gemäß|nach|im Sinne (?:des|der|von))\s+(?:Art\.?\s*\d+|§\s*\d+)\s+(?:Abs\.?\s*\d+\s+)?([A-ZÄÖÜa-zäöüß\-]+)", "cross_reference"),
]


def extract_thresholds(text: str) -> list[dict]:
    """Extract legal thresholds, deadlines, sanctions from text."""
    results = []
    for pattern, category in THRESHOLD_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            results.append({
                "category": category,
                "match": match.group(0),
                "groups": match.groups(),
                "position": match.start(),
            })
    return results


# ============================================================================
# API CLIENT
# ============================================================================

class RisOgdClient:
    """Client for the Austrian RIS OGD API v2.6."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "BEATRIX-Legal/0.1 (FehrAdvice EBF Framework)",
        })

    def search(self, db: str, query: str, page: int = 1, page_size: str = "OneHundred") -> dict:
        """Search a RIS database."""
        if db not in DATABASES:
            raise ValueError(f"Unknown database: {db}. Available: {list(DATABASES.keys())}")

        config = DATABASES[db]
        params = dict(config["params"])
        params["Suchworte"] = query
        params["Seitennummer"] = page
        params["DokumenteProSeite"] = page_size

        # Remove empty params
        params = {k: v for k, v in params.items() if v}

        url = f"{self.base_url}{config['endpoint']}"
        print(f"  [DEBUG] GET {url}")
        print(f"  [DEBUG] Params: {params}")

        response = self.session.get(url, params=params, timeout=30)
        print(f"  [DEBUG] Status: {response.status_code}")
        print(f"  [DEBUG] Content-Type: {response.headers.get('Content-Type', '?')}")
        print(f"  [DEBUG] Response size: {len(response.content)} bytes")

        if response.status_code != 200:
            print(f"  [DEBUG] Response body (first 500 chars): {response.text[:500]}")

        response.raise_for_status()

        data = response.json()
        # Debug: show top-level keys
        print(f"  [DEBUG] Top-level keys: {list(data.keys())}")
        if "OgdSearchResult" in data:
            sr = data["OgdSearchResult"]
            print(f"  [DEBUG] OgdSearchResult keys: {list(sr.keys())}")
            if "OgdDocumentResults" in sr:
                dr = sr["OgdDocumentResults"]
                print(f"  [DEBUG] OgdDocumentResults keys: {list(dr.keys())}")
                hits = dr.get("Hits", {})
                print(f"  [DEBUG] Hits: {hits}")
        else:
            # Show first 1000 chars of response for debugging
            print(f"  [DEBUG] No OgdSearchResult! Raw (first 1000): {json.dumps(data, ensure_ascii=False)[:1000]}")

        return data

    def get_document(self, document_url: str) -> dict:
        """Fetch a specific document by its URL."""
        response = self.session.get(document_url, timeout=30)
        response.raise_for_status()
        return response.json()

    def search_all_pages(self, db: str, query: str, max_pages: int = 100) -> list[dict]:
        """Search and paginate through all results."""
        all_results = []
        page = 1

        while page <= max_pages:
            result = self.search(db, query, page=page)

            # Extract documents from response
            docs = self._extract_documents(result)
            if not docs:
                break

            all_results.extend(docs)
            page += 1

            # Rate limiting (be nice to the API)
            time.sleep(0.5)

        return all_results

    def bulk_download(self, db: str, output_dir: str, query: str = "*", max_pages: int = 1000) -> int:
        """Bulk download all documents from a database."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        total = 0
        page = 1

        while page <= max_pages:
            try:
                result = self.search(db, query, page=page)
                docs = self._extract_documents(result)

                if not docs:
                    break

                for doc in docs:
                    doc_id = doc.get("Dokumentnummer", f"unknown_{total}")
                    # Sanitize filename
                    safe_id = re.sub(r'[^\w\-.]', '_', str(doc_id))
                    filepath = output_path / f"{safe_id}.json"
                    filepath.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
                    total += 1

                print(f"  Page {page}: {len(docs)} documents (total: {total})")
                page += 1
                time.sleep(0.5)

            except requests.RequestException as e:
                print(f"  Error on page {page}: {e}")
                if page > 1:
                    time.sleep(2)  # Back off on error
                    continue
                raise

        return total

    def status(self) -> dict:
        """Check API availability."""
        results = {}
        for db_name, config in DATABASES.items():
            try:
                url = f"{self.base_url}{config['endpoint']}"
                resp = self.session.get(url, params={"Suchworte": "Gesetz", "DokumenteProSeite": "Ten", "Seitennummer": 1}, timeout=10)
                hits = self._count_hits(resp.json()) if resp.status_code == 200 else 0
                results[db_name] = {
                    "status": resp.status_code,
                    "description": config["description"],
                    "sample_hits": hits,
                }
            except Exception as e:
                results[db_name] = {
                    "status": "ERROR",
                    "description": config["description"],
                    "error": str(e),
                }
        return results

    def _extract_documents(self, response: dict) -> list[dict]:
        """Extract document list from API response (handles varying response structures)."""
        # RIS API nests results differently per database
        if "OgdSearchResult" in response:
            sr = response["OgdSearchResult"]
            if "OgdDocumentResults" in sr:
                dr = sr["OgdDocumentResults"]
                if "OgdDocumentReference" in dr:
                    refs = dr["OgdDocumentReference"]
                    return refs if isinstance(refs, list) else [refs]
        return []

    def _count_hits(self, response: dict) -> int:
        """Count total hits from response."""
        try:
            return int(response.get("OgdSearchResult", {}).get("OgdDocumentResults", {}).get("Hits", {}).get("Value", 0))
        except (ValueError, AttributeError):
            return 0


# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def format_search_results(docs: list[dict], extract: bool = False) -> str:
    """Format search results for display."""
    lines = []
    for i, doc in enumerate(docs, 1):
        data = doc.get("Data", {})
        metadata = data.get("Metadaten", {})
        doc_nr = data.get("Dokumentnummer", "?")
        titel = metadata.get("BrKons", {}).get("Titel", "")
        if not titel:
            titel = metadata.get("Kurzinformation", "Kein Titel")
        artikel = metadata.get("BrKons", {}).get("ArtikelParagraphAnlage", "")

        lines.append(f"\n{'='*70}")
        lines.append(f"  [{i}] {doc_nr}")
        lines.append(f"  Titel: {titel}")
        if artikel:
            lines.append(f"  Artikel/§: {artikel}")

        # Extract URLs
        urls = data.get("Dokumentliste", {})
        if urls and isinstance(urls, dict):
            for fmt, url_data in urls.items():
                if isinstance(url_data, dict) and "Url" in url_data:
                    lines.append(f"  {fmt}: {url_data['Url']}")
                elif isinstance(url_data, list):
                    for u in url_data:
                        if isinstance(u, dict) and "Url" in u:
                            lines.append(f"  {fmt}: {u['Url']}")

        # Threshold extraction
        if extract:
            text_parts = []
            if isinstance(titel, str):
                text_parts.append(titel)
            kurzinfo = metadata.get("Kurzinformation", "")
            if isinstance(kurzinfo, str):
                text_parts.append(kurzinfo)

            full_text = " ".join(text_parts)
            thresholds = extract_thresholds(full_text)
            if thresholds:
                lines.append(f"  --- EXTRACTED THRESHOLDS ---")
                for t in thresholds:
                    lines.append(f"  [{t['category']}] {t['match']}")

    return "\n".join(lines)


def format_status(status: dict) -> str:
    """Format status check results."""
    lines = [
        "",
        "=" * 70,
        "  RIS OGD v2.6 API STATUS",
        "=" * 70,
    ]
    for db_name, info in status.items():
        status_code = info.get("status", "?")
        icon = "✅" if status_code == 200 else "❌"
        desc = info.get("description", "")
        hits = info.get("sample_hits", "?")
        lines.append(f"  {icon} {db_name:25s} | {status_code} | ~{hits} hits | {desc}")

    lines.append("=" * 70)
    return "\n".join(lines)


# ============================================================================
# YAML EXPORT (for Layer 2 registry)
# ============================================================================

def export_to_yaml(docs: list[dict], output_path: str) -> int:
    """Export extracted legal data to YAML for Layer 2 registry."""
    try:
        import yaml
    except ImportError:
        print("WARNING: PyYAML not installed. Falling back to JSON export.")
        output_path = output_path.replace(".yaml", ".json")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(json.dumps(docs, ensure_ascii=False, indent=2))
        return len(docs)

    entries = []
    for doc in docs:
        data = doc.get("Data", {})
        metadata = data.get("Metadaten", {})
        br = metadata.get("BrKons", {})

        entry = {
            "document_id": data.get("Dokumentnummer"),
            "title": br.get("Titel", metadata.get("Kurzinformation", "")),
            "article": br.get("ArtikelParagraphAnlage"),
            "index": br.get("Index"),
            "jurisdiction": "AT",
            "source": "RIS OGD v2.6",
            "source_url": f"https://www.ris.bka.gv.at/",
        }

        # Extract thresholds from available text
        text = f"{entry['title']} {entry.get('article', '')}"
        thresholds = extract_thresholds(text)
        if thresholds:
            entry["thresholds"] = [
                {"category": t["category"], "value": t["match"]}
                for t in thresholds
            ]

        entries.append(entry)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump({"legal_registry": {"jurisdiction": "AT", "source": "RIS OGD v2.6", "entries": entries}},
                  f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return len(entries)


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="RIS OGD v2.6 Connector — Austrian Legal Database")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--db", type=str, default="bundesrecht", choices=list(DATABASES.keys()),
                        help="Database to search (default: bundesrecht)")
    parser.add_argument("--extract-thresholds", action="store_true",
                        help="Extract thresholds, deadlines, sanctions")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--bulk", type=str, metavar="DB",
                        help="Bulk download all documents from a database")
    parser.add_argument("--output", type=str, default="data/legal/at/",
                        help="Output directory for bulk download")
    parser.add_argument("--export-yaml", type=str, metavar="PATH",
                        help="Export results to YAML (for Layer 2 registry)")
    parser.add_argument("--status", action="store_true",
                        help="Check API availability for all databases")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON response")

    args = parser.parse_args()
    client = RisOgdClient()

    if args.status:
        status = client.status()
        print(format_status(status))
        return

    if args.bulk:
        if args.bulk not in DATABASES:
            print(f"ERROR: Unknown database '{args.bulk}'. Available: {list(DATABASES.keys())}")
            sys.exit(1)
        print(f"Bulk downloading {args.bulk} to {args.output}...")
        total = client.bulk_download(args.bulk, args.output)
        print(f"\nDone. {total} documents saved to {args.output}")
        return

    if args.search:
        result = client.search(args.db, args.search, page=args.page)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        docs = client._extract_documents(result)
        hits = client._count_hits(result)
        print(f"\n  Suche: '{args.search}' in {args.db}")
        print(f"  Treffer: {hits}")

        if docs:
            print(format_search_results(docs, extract=args.extract_thresholds))

            if args.export_yaml:
                count = export_to_yaml(docs, args.export_yaml)
                print(f"\n  Exported {count} entries to {args.export_yaml}")
        else:
            print("  Keine Ergebnisse.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
