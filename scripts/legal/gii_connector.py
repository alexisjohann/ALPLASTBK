#!/usr/bin/env python3
"""
gesetze-im-internet.de Connector — German Federal Law
======================================================

Downloads and parses German federal laws from gesetze-im-internet.de.
Free, no authentication, 6,000+ federal laws and regulations.

Data: XML files via TOC at https://www.gesetze-im-internet.de/gii-toc.xml

Usage:
    python scripts/legal/gii_connector.py --toc                    # Download TOC
    python scripts/legal/gii_connector.py --download bgb           # Download BGB
    python scripts/legal/gii_connector.py --download-all --output data/legal/de/
    python scripts/legal/gii_connector.py --search "Sorgfalt"      # Search in TOC
    python scripts/legal/gii_connector.py --status
"""

import argparse
import io
import json
import os
import re
import sys
import time
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

BASE_URL = "https://www.gesetze-im-internet.de"
TOC_URL = f"{BASE_URL}/gii-toc.xml"


class GiiClient:
    """Client for gesetze-im-internet.de (German Federal Law XML)."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "BEATRIX-Legal/0.1 (FehrAdvice EBF Framework)",
        })

    def fetch_toc(self) -> list[dict]:
        """Fetch and parse the Table of Contents XML."""
        response = self.session.get(TOC_URL, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        laws = []
        for item in root.iter("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            if title_el is not None and link_el is not None:
                laws.append({
                    "title": title_el.text or "",
                    "link": link_el.text or "",
                    "abbreviation": self._extract_abbrev(link_el.text or ""),
                })
        return laws

    def search_toc(self, query: str) -> list[dict]:
        """Search the TOC by keyword."""
        toc = self.fetch_toc()
        query_lower = query.lower()
        return [law for law in toc if query_lower in law["title"].lower() or query_lower in law["abbreviation"].lower()]

    def download_law(self, abbreviation: str, output_dir: str = "data/legal/de/") -> dict:
        """Download a specific law as XML."""
        url = f"{BASE_URL}/{abbreviation}/xml.zip"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Extract ZIP
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            zf.extractall(output_path / abbreviation)

        # Parse the XML
        xml_files = list((output_path / abbreviation).glob("*.xml"))
        if xml_files:
            return self._parse_law_xml(xml_files[0])
        return {"abbreviation": abbreviation, "error": "No XML found in ZIP"}

    def download_all(self, output_dir: str = "data/legal/de/", max_laws: int = 10000) -> int:
        """Bulk download all German federal laws."""
        toc = self.fetch_toc()
        total = 0
        errors = 0

        for i, law in enumerate(toc[:max_laws]):
            abbrev = law["abbreviation"]
            if not abbrev:
                continue

            try:
                self.download_law(abbrev, output_dir)
                total += 1
                if total % 100 == 0:
                    print(f"  Downloaded {total}/{len(toc)} laws...")
                time.sleep(0.2)  # Be nice
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  Error downloading {abbrev}: {e}")

        return total

    def status(self) -> dict:
        """Check availability."""
        try:
            toc = self.fetch_toc()
            return {"status": "OK", "laws_count": len(toc), "url": TOC_URL}
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def _extract_abbrev(self, link: str) -> str:
        """Extract law abbreviation from URL."""
        # https://www.gesetze-im-internet.de/bgb/ -> bgb
        parts = link.rstrip("/").split("/")
        return parts[-1] if parts else ""

    def _parse_law_xml(self, xml_path: Path) -> dict:
        """Parse a GII XML file into structured data."""
        tree = ET.parse(xml_path)
        root = tree.getroot()

        norms = []
        for norm in root.iter("norm"):
            meta = norm.find("metadaten")
            text = norm.find("textdaten")

            entry = {}
            if meta is not None:
                for child in meta:
                    entry[child.tag] = child.text

            if text is not None:
                content = text.find(".//Content")
                if content is not None:
                    entry["text"] = ET.tostring(content, encoding="unicode", method="text")[:2000]

            if entry:
                norms.append(entry)

        return {
            "file": str(xml_path),
            "norms_count": len(norms),
            "norms": norms[:5],  # Preview first 5
        }


def main():
    parser = argparse.ArgumentParser(description="GII Connector — German Federal Law")
    parser.add_argument("--toc", action="store_true", help="Fetch Table of Contents")
    parser.add_argument("--search", type=str, help="Search TOC by keyword")
    parser.add_argument("--download", type=str, metavar="ABBREV", help="Download specific law (e.g. bgb)")
    parser.add_argument("--download-all", action="store_true", help="Bulk download all laws")
    parser.add_argument("--output", type=str, default="data/legal/de/", help="Output directory")
    parser.add_argument("--status", action="store_true", help="Check availability")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    client = GiiClient()

    if args.status:
        print(json.dumps(client.status(), indent=2))
        return

    if args.toc:
        toc = client.fetch_toc()
        print(f"  {len(toc)} German federal laws found")
        if args.json:
            print(json.dumps(toc[:20], indent=2, ensure_ascii=False))
        else:
            for law in toc[:20]:
                print(f"  {law['abbreviation']:20s} {law['title'][:60]}")
            print(f"  ... and {len(toc)-20} more")
        return

    if args.search:
        results = client.search_toc(args.search)
        print(f"\n  Search: '{args.search}' — {len(results)} results")
        for law in results[:20]:
            print(f"  {law['abbreviation']:20s} {law['title'][:60]}")
        return

    if args.download:
        print(f"  Downloading {args.download}...")
        result = client.download_law(args.download, args.output)
        print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else f"  Done: {result.get('norms_count', 0)} norms parsed")
        return

    if args.download_all:
        print(f"  Bulk downloading to {args.output}...")
        total = client.download_all(args.output)
        print(f"  Done: {total} laws downloaded")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
