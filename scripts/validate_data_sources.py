#!/usr/bin/env python3
"""
Data Sources Validation Script

Validates freshness and completeness of external data sources used in the
Swiss context vector (BCM2_04_KON) and survey data (ESS, WVS, etc.).

Checks:
1. Data freshness (last_updated vs. source update frequency)
2. API endpoint availability
3. Data completeness (missing values)
4. Cross-source consistency

Usage:
    python scripts/validate_data_sources.py
    python scripts/validate_data_sources.py --check-apis
    python scripts/validate_data_sources.py --source ess
    python scripts/validate_data_sources.py --verbose

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple
import urllib.request
import urllib.error

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_SOURCES_CONFIG = {
    "ess": {
        "name": "European Social Survey (ESS)",
        "yaml_path": "data/dr-datareq/sources/surveys/ESS_CH_values.yaml",
        "update_frequency_days": 730,  # Every 2 years
        "check_url": "https://ess.sikt.no/",
        "updater_script": "scripts/fetch_ess_data.py",
        "priority": "high",
    },
    "fehradvice_norms": {
        "name": "FehrAdvice Social Norms Research",
        "yaml_path": "data/dr-datareq/sources/surveys/FehrAdvice_CH_norms.yaml",
        "update_frequency_days": 365,  # Yearly review
        "check_url": "https://www.fehradvice.com/",
        "priority": "high",
    },
    "fehradvice_sustainability": {
        "name": "FehrAdvice Sustainability Governance Research",
        "yaml_path": "data/dr-datareq/sources/surveys/FehrAdvice_CH_sustainability_gov.yaml",
        "update_frequency_days": 365,  # Yearly review
        "check_url": "https://www.fehradvice.com/",
        "priority": "high",
    },
    "fehradvice_energy": {
        "name": "FehrAdvice Energy & Resources Research",
        "yaml_path": "data/dr-datareq/sources/surveys/FehrAdvice_CH_energy_resources.yaml",
        "update_frequency_days": 365,  # Yearly review
        "check_url": "https://www.fehradvice.com/",
        "priority": "high",
    },
    "owid": {
        "name": "Our World in Data (OWID)",
        "yaml_path": "data/dr-datareq/sources/international/OWID_indicators.yaml",
        "update_frequency_days": 365,  # Yearly review
        "check_url": "https://ourworldindata.org/",
        "api_url": "https://github.com/owid/owid-datasets",
        "priority": "medium",
    },
    "oecd": {
        "name": "OECD Statistics",
        "yaml_path": "data/dr-datareq/sources/international/OECD_indicators.yaml",
        "update_frequency_days": 365,  # Yearly review
        "check_url": "https://data.oecd.org/",
        "api_url": "https://sdmx.oecd.org/public/rest",
        "priority": "high",
    },
    "worldbank": {
        "name": "World Bank Open Data",
        "yaml_path": "data/dr-datareq/sources/international/WorldBank_indicators.yaml",
        "update_frequency_days": 365,  # Yearly review
        "check_url": "https://data.worldbank.org/",
        "api_url": "https://api.worldbank.org/v2",
        "priority": "high",
    },
    "ecb": {
        "name": "European Central Bank (ECB)",
        "yaml_path": "data/dr-datareq/sources/international/ECB_indicators.yaml",
        "update_frequency_days": 365,
        "check_url": "https://www.ecb.europa.eu/",
        "api_url": "https://sdw-wsrest.ecb.europa.eu/service",
        "priority": "high",
    },
    "oenb": {
        "name": "Österreichische Nationalbank (OeNB)",
        "yaml_path": "data/dr-datareq/sources/international/OeNB_indicators.yaml",
        "update_frequency_days": 365,
        "check_url": "https://www.oenb.at/",
        "priority": "medium",
    },
    "eurostat": {
        "name": "Eurostat (EU Statistics)",
        "yaml_path": "data/dr-datareq/sources/international/Eurostat_indicators.yaml",
        "update_frequency_days": 365,
        "check_url": "https://ec.europa.eu/eurostat",
        "api_url": "https://ec.europa.eu/eurostat/api/dissemination",
        "priority": "high",
    },
    "fred": {
        "name": "US Federal Reserve / FRED",
        "yaml_path": "data/dr-datareq/sources/international/US_Fed_FRED_indicators.yaml",
        "update_frequency_days": 365,
        "check_url": "https://fred.stlouisfed.org/",
        "api_url": "https://api.stlouisfed.org/fred",
        "priority": "high",
    },
    "germany_gov": {
        "name": "German Government (BMF/BMWK/Destatis)",
        "yaml_path": "data/dr-datareq/sources/international/Germany_gov_indicators.yaml",
        "update_frequency_days": 365,
        "check_url": "https://www.destatis.de/",
        "priority": "medium",
    },
    "bfs": {
        "name": "Bundesamt für Statistik (BFS)",
        "yaml_path": "data/dr-datareq/sources/context/ch/BCM2_04_KON_demographic.yaml",
        "update_frequency_days": 365,  # Yearly
        "check_url": "https://www.bfs.admin.ch/",
        "api_url": "https://www.pxweb.bfs.admin.ch/api/v1/de",
        "priority": "high",
    },
    "snb": {
        "name": "Schweizerische Nationalbank (SNB)",
        "yaml_path": "data/dr-datareq/sources/context/ch/BCM2_04_KON_economic.yaml",
        "update_frequency_days": 90,  # Quarterly
        "check_url": "https://www.snb.ch/",
        "api_url": "https://data.snb.ch/api/cube",
        "priority": "high",
    },
    "seco": {
        "name": "Staatssekretariat für Wirtschaft (SECO)",
        "yaml_path": "data/dr-datareq/sources/context/ch/BCM2_04_KON_economic.yaml",
        "update_frequency_days": 90,  # Quarterly
        "check_url": "https://www.seco.admin.ch/",
        "priority": "medium",
    },
    "wvs": {
        "name": "World Values Survey (WVS)",
        "yaml_path": None,  # Not yet integrated
        "update_frequency_days": 1825,  # Every 5 years
        "check_url": "https://www.worldvaluessurvey.org/",
        "priority": "low",
    },
}

CONTEXT_FILES = [
    "data/dr-datareq/sources/context/ch/BCM2_04_KON_demographic.yaml",
    "data/dr-datareq/sources/context/ch/BCM2_04_KON_economic.yaml",
    "data/dr-datareq/sources/context/ch/BCM2_04_KON_institutional_political.yaml",
    "data/dr-datareq/sources/context/ch/BCM2_04_KON_tech_ecological.yaml",
    "data/dr-datareq/sources/context/ch/BCM2_04_KON_socio_cultural.yaml",
]


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def check_file_freshness(yaml_path: str, max_age_days: int) -> Tuple[bool, str, Dict]:
    """Check if a YAML file's data is fresh enough."""
    path = Path(yaml_path)

    if not path.exists():
        return False, f"File not found: {yaml_path}", {"status": "missing"}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return False, f"Failed to parse YAML: {e}", {"status": "parse_error"}

    # Look for last_updated in metadata
    last_updated = None
    metadata = data.get("metadata", {})

    if "last_updated" in metadata:
        last_updated = metadata["last_updated"]
    elif "version_date" in metadata:
        last_updated = metadata["version_date"]
    elif "version" in metadata:
        # Try to extract date from version string
        version = metadata["version"]
        if isinstance(version, str) and len(version) >= 10:
            try:
                last_updated = version[:10]
            except:
                pass

    if not last_updated:
        return False, "No last_updated field in metadata", {"status": "no_date"}

    # Parse date
    try:
        if isinstance(last_updated, str):
            update_date = datetime.strptime(last_updated[:10], "%Y-%m-%d")
        else:
            update_date = last_updated
    except ValueError:
        return False, f"Invalid date format: {last_updated}", {"status": "invalid_date"}

    # Check age
    age = datetime.now() - update_date
    age_days = age.days

    result = {
        "status": "ok" if age_days <= max_age_days else "stale",
        "last_updated": str(last_updated),
        "age_days": age_days,
        "max_age_days": max_age_days,
        "file": yaml_path,
    }

    if age_days > max_age_days:
        return False, f"Data is {age_days} days old (max: {max_age_days})", result

    return True, f"Data is {age_days} days old (within {max_age_days} day limit)", result


def check_api_availability(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Check if an API endpoint is reachable."""
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'EBF-DataValidator/1.0')
        response = urllib.request.urlopen(req, timeout=timeout)
        return True, f"OK (HTTP {response.status})"
    except urllib.error.HTTPError as e:
        if e.code in [403, 405]:  # Some APIs don't allow HEAD
            return True, f"Reachable (HTTP {e.code})"
        return False, f"HTTP Error: {e.code}"
    except urllib.error.URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, f"Error: {e}"


def check_data_completeness(yaml_path: str) -> Tuple[bool, str, Dict]:
    """Check for missing values in YAML data."""
    path = Path(yaml_path)

    if not path.exists():
        return False, "File not found", {"status": "missing"}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return False, f"Parse error: {e}", {"status": "error"}

    # Count factors and missing values
    factors = data.get("factors", [])
    total_factors = len(factors)
    missing_values = 0
    incomplete_factors = []

    for factor in factors:
        # Check for required fields
        required = ["id", "name", "definition"]
        for field in required:
            if not factor.get(field):
                missing_values += 1
                if factor.get("id") not in incomplete_factors:
                    incomplete_factors.append(factor.get("id", "unknown"))

        # Check for values (if applicable)
        if "values" in factor:
            values = factor["values"]
            if isinstance(values, dict):
                for year, val in values.items():
                    if val is None:
                        missing_values += 1

    completeness = ((total_factors * 3 - missing_values) / (total_factors * 3)) * 100 if total_factors > 0 else 0

    result = {
        "status": "ok" if completeness >= 90 else "incomplete",
        "total_factors": total_factors,
        "missing_values": missing_values,
        "completeness_pct": round(completeness, 1),
        "incomplete_factors": incomplete_factors[:5],  # First 5
    }

    if completeness < 90:
        return False, f"Completeness {completeness:.1f}% (target: 90%)", result

    return True, f"Completeness {completeness:.1f}%", result


def check_ess_round_currency() -> Tuple[bool, str, Dict]:
    """Check if ESS data includes the latest available round."""
    yaml_path = DATA_SOURCES_CONFIG["ess"]["yaml_path"]
    path = Path(yaml_path)

    if not path.exists():
        return False, "ESS YAML not found", {"status": "missing"}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return False, f"Parse error: {e}", {"status": "error"}

    metadata = data.get("metadata", {})
    data_rounds = metadata.get("data_rounds", [])

    # Latest ESS round (as of 2024)
    latest_available = 11  # ESS Round 11 (2023)

    result = {
        "status": "ok",
        "rounds_in_data": data_rounds,
        "latest_available": latest_available,
    }

    if not data_rounds:
        result["status"] = "unknown"
        return False, "No round information in metadata", result

    if latest_available not in data_rounds:
        result["status"] = "outdated"
        return False, f"Missing latest ESS Round {latest_available}", result

    return True, f"Includes ESS Round {latest_available}", result


# =============================================================================
# MAIN VALIDATION
# =============================================================================

def validate_all(check_apis: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """Run all validations and return results."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "passed": 0,
            "warnings": 0,
            "failed": 0,
        },
        "checks": [],
    }

    print("=" * 70)
    print("DATA SOURCES VALIDATION")
    print("=" * 70)
    print()

    # 1. Check data freshness for each source
    print("[1/4] Data Freshness Checks")
    print("-" * 40)

    for source_id, config in DATA_SOURCES_CONFIG.items():
        yaml_path = config.get("yaml_path")
        if not yaml_path:
            if verbose:
                print(f"  ⏭️  {config['name']}: No YAML (skipped)")
            continue

        ok, msg, details = check_file_freshness(yaml_path, config["update_frequency_days"])

        check_result = {
            "check": "freshness",
            "source": source_id,
            "name": config["name"],
            "passed": ok,
            "message": msg,
            "details": details,
        }
        results["checks"].append(check_result)

        if ok:
            print(f"  ✅ {config['name']}: {msg}")
            results["summary"]["passed"] += 1
        else:
            status = details.get("status", "unknown")
            if status == "stale":
                print(f"  ⚠️  {config['name']}: {msg}")
                print(f"      → Run: python {config.get('updater_script', 'manual update')}")
                results["summary"]["warnings"] += 1
            else:
                print(f"  ❌ {config['name']}: {msg}")
                results["summary"]["failed"] += 1

    print()

    # 2. Check context files completeness
    print("[2/4] Data Completeness Checks")
    print("-" * 40)

    for yaml_path in CONTEXT_FILES:
        ok, msg, details = check_data_completeness(yaml_path)

        filename = Path(yaml_path).stem
        check_result = {
            "check": "completeness",
            "file": yaml_path,
            "passed": ok,
            "message": msg,
            "details": details,
        }
        results["checks"].append(check_result)

        if ok:
            print(f"  ✅ {filename}: {msg}")
            results["summary"]["passed"] += 1
        else:
            print(f"  ⚠️  {filename}: {msg}")
            results["summary"]["warnings"] += 1

    print()

    # 3. Check ESS round currency
    print("[3/4] ESS Round Currency")
    print("-" * 40)

    ok, msg, details = check_ess_round_currency()
    check_result = {
        "check": "ess_currency",
        "passed": ok,
        "message": msg,
        "details": details,
    }
    results["checks"].append(check_result)

    if ok:
        print(f"  ✅ ESS: {msg}")
        results["summary"]["passed"] += 1
    else:
        print(f"  ⚠️  ESS: {msg}")
        print("      → Run: python scripts/fetch_ess_data.py --download")
        results["summary"]["warnings"] += 1

    print()

    # 4. Optional: Check API availability
    if check_apis:
        print("[4/4] API Availability Checks")
        print("-" * 40)

        for source_id, config in DATA_SOURCES_CONFIG.items():
            api_url = config.get("api_url") or config.get("check_url")
            if not api_url:
                continue

            ok, msg = check_api_availability(api_url)

            check_result = {
                "check": "api_availability",
                "source": source_id,
                "url": api_url,
                "passed": ok,
                "message": msg,
            }
            results["checks"].append(check_result)

            if ok:
                print(f"  ✅ {config['name']}: {msg}")
                results["summary"]["passed"] += 1
            else:
                print(f"  ❌ {config['name']}: {msg}")
                results["summary"]["failed"] += 1

        print()
    else:
        print("[4/4] API Checks: Skipped (use --check-apis to enable)")
        print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    total = results["summary"]["passed"] + results["summary"]["warnings"] + results["summary"]["failed"]

    print(f"  ✅ Passed:   {results['summary']['passed']}/{total}")
    print(f"  ⚠️  Warnings: {results['summary']['warnings']}/{total}")
    print(f"  ❌ Failed:   {results['summary']['failed']}/{total}")
    print()

    if results["summary"]["failed"] > 0:
        print("Status: ❌ FAILED - Critical issues found")
        results["overall_status"] = "FAILED"
    elif results["summary"]["warnings"] > 0:
        print("Status: ⚠️  WARNING - Some data sources need attention")
        results["overall_status"] = "WARNING"
    else:
        print("Status: ✅ PASSED - All data sources current")
        results["overall_status"] = "PASSED"

    # Recommendations
    if results["summary"]["warnings"] > 0 or results["summary"]["failed"] > 0:
        print()
        print("Recommendations:")
        for check in results["checks"]:
            if not check["passed"]:
                if check["check"] == "freshness":
                    source = check.get("source", "")
                    if source in DATA_SOURCES_CONFIG:
                        script = DATA_SOURCES_CONFIG[source].get("updater_script")
                        if script:
                            print(f"  → Update {check['name']}: python {script}")
                elif check["check"] == "ess_currency":
                    print("  → Update ESS: python scripts/fetch_ess_data.py --download")

    return results


def validate_source(source_id: str, verbose: bool = False) -> Dict[str, Any]:
    """Validate a specific data source."""
    if source_id not in DATA_SOURCES_CONFIG:
        print(f"ERROR: Unknown source '{source_id}'")
        print(f"Available: {', '.join(DATA_SOURCES_CONFIG.keys())}")
        return {"error": "unknown_source"}

    config = DATA_SOURCES_CONFIG[source_id]
    print(f"Validating: {config['name']}")
    print("-" * 40)

    results = {"source": source_id, "checks": []}

    # Freshness
    yaml_path = config.get("yaml_path")
    if yaml_path:
        ok, msg, details = check_file_freshness(yaml_path, config["update_frequency_days"])
        print(f"Freshness: {'✅' if ok else '⚠️'} {msg}")
        results["checks"].append({"check": "freshness", "passed": ok, "details": details})

        # Completeness
        ok, msg, details = check_data_completeness(yaml_path)
        print(f"Completeness: {'✅' if ok else '⚠️'} {msg}")
        results["checks"].append({"check": "completeness", "passed": ok, "details": details})

    # API
    api_url = config.get("api_url") or config.get("check_url")
    if api_url:
        ok, msg = check_api_availability(api_url)
        print(f"API: {'✅' if ok else '❌'} {msg}")
        results["checks"].append({"check": "api", "passed": ok})

    return results


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate EBF data sources for freshness and completeness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_data_sources.py              # Run all checks
  python scripts/validate_data_sources.py --check-apis # Include API checks
  python scripts/validate_data_sources.py --source ess # Check ESS only
  python scripts/validate_data_sources.py --json       # Output as JSON
        """
    )

    parser.add_argument("--check-apis", action="store_true",
                        help="Also check API endpoint availability")
    parser.add_argument("--source", metavar="ID",
                        help="Validate specific source (ess, bfs, snb, seco, wvs)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    args = parser.parse_args()

    if args.source:
        results = validate_source(args.source, verbose=args.verbose)
    else:
        results = validate_all(check_apis=args.check_apis, verbose=args.verbose)

    if args.json:
        print()
        print(json.dumps(results, indent=2, default=str))

    # Exit code
    if results.get("overall_status") == "FAILED":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
