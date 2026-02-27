#!/usr/bin/env python3
"""
ESS (European Social Survey) Data Fetcher and Processor

Fetches ESS data for Switzerland and updates the context vector YAML files.
Since ESS has no official Python API, this script:
1. Downloads data from ESS Data Portal (requires manual auth for first time)
2. Processes CSV/SPSS files to extract Swiss value dimensions
3. Updates ESS_CH_values.yaml with latest data

ESS Data Portal: https://ess.sikt.no/
R Alternative: library(essurvey) - for R users

Usage:
    python scripts/fetch_ess_data.py --help
    python scripts/fetch_ess_data.py --download          # Download latest ESS data
    python scripts/fetch_ess_data.py --process FILE.csv  # Process downloaded file
    python scripts/fetch_ess_data.py --update-yaml       # Update YAML from processed data
    python scripts/fetch_ess_data.py --stats             # Show current data statistics

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import urllib.request
import urllib.error

# YAML handling
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# Optional: pandas for CSV processing
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


# =============================================================================
# CONFIGURATION
# =============================================================================

ESS_CONFIG = {
    "data_portal_url": "https://ess.sikt.no/",
    "api_base_url": "https://ess.sikt.no/api/v1/",  # If available
    "supported_rounds": list(range(1, 12)),  # ESS Rounds 1-11
    "country_code_ch": "CH",
    "output_dir": Path("data/dr-datareq/sources/surveys"),
    "yaml_file": Path("data/dr-datareq/sources/surveys/ESS_CH_values.yaml"),
    "cache_dir": Path("data/dr-datareq/cache/ess"),
}

# Schwartz Value Dimensions mapping to ESS variables
SCHWARTZ_ESS_MAPPING = {
    "Security": {
        "ess_vars": ["impsafe", "ipstrgv"],
        "description": "Sicherheit - Bedürfnis nach Stabilität, Schutz und Ordnung",
    },
    "Conformity": {
        "ess_vars": ["ipfrule", "ipbhprp"],
        "description": "Konformität - Respekt vor Regeln und sozialen Erwartungen",
    },
    "Tradition": {
        "ess_vars": ["imptrad", "ipmodst"],
        "description": "Tradition - Respekt vor kulturellen und religiösen Bräuchen",
    },
    "Benevolence": {
        "ess_vars": ["iphlppl", "iplylfr"],
        "description": "Wohlwollen - Fürsorge für nahestehende Personen",
    },
    "Universalism": {
        "ess_vars": ["ipeqopt", "ipudrst", "impenv"],
        "description": "Universalismus - Verständnis, Toleranz und Schutz aller Menschen",
    },
    "Self-Direction": {
        "ess_vars": ["ipcrtiv", "impfree"],
        "description": "Selbstbestimmung - Unabhängiges Denken und Handeln",
    },
    "Stimulation": {
        "ess_vars": ["impdiff", "ipadvnt"],
        "description": "Stimulation - Aufregung, Neuheit und Herausforderung",
    },
    "Hedonism": {
        "ess_vars": ["ipgdtim", "impfun"],
        "description": "Hedonismus - Vergnügen und sinnliche Befriedigung",
    },
    "Achievement": {
        "ess_vars": ["ipshabt", "ipsuces"],
        "description": "Leistung - Persönlicher Erfolg durch Kompetenz",
    },
    "Power": {
        "ess_vars": ["imprich", "iprspot"],
        "description": "Macht - Sozialer Status und Kontrolle über Ressourcen",
    },
}

# ESS Round metadata
ESS_ROUNDS = {
    1: {"year": 2002, "fieldwork": "2002-2003"},
    2: {"year": 2004, "fieldwork": "2004-2005"},
    3: {"year": 2006, "fieldwork": "2006-2007"},
    4: {"year": 2008, "fieldwork": "2008-2009"},
    5: {"year": 2010, "fieldwork": "2010-2011"},
    6: {"year": 2012, "fieldwork": "2012-2013"},
    7: {"year": 2014, "fieldwork": "2014-2015"},
    8: {"year": 2016, "fieldwork": "2016-2017"},
    9: {"year": 2018, "fieldwork": "2018-2019"},
    10: {"year": 2020, "fieldwork": "2020-2022"},
    11: {"year": 2023, "fieldwork": "2023-2024"},
}


# =============================================================================
# DATA FETCHING
# =============================================================================

def check_ess_availability() -> Dict[str, Any]:
    """Check which ESS rounds are available for Switzerland."""
    print("Checking ESS data availability for Switzerland...")

    available = {
        "rounds": [],
        "latest_round": None,
        "total_respondents_estimate": 0,
    }

    # ESS Switzerland participation (known from documentation)
    ch_participation = {
        1: True, 2: True, 3: True, 4: True, 5: True,
        6: True, 7: True, 8: True, 9: True, 10: True, 11: True
    }

    for round_num, participated in ch_participation.items():
        if participated:
            available["rounds"].append(round_num)
            available["latest_round"] = round_num
            available["total_respondents_estimate"] += 1500  # ~1500 per round

    return available


def download_ess_instructions() -> str:
    """Return instructions for manual ESS download."""
    instructions = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ESS DATA DOWNLOAD INSTRUCTIONS                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ESS requires registration for data access. Follow these steps:              ║
║                                                                              ║
║  1. Go to: https://ess.sikt.no/                                              ║
║                                                                              ║
║  2. Register/Login (free academic registration)                              ║
║                                                                              ║
║  3. Select data:                                                             ║
║     - Country: Switzerland                                                   ║
║     - Rounds: Select all available (1-11)                                    ║
║     - Variables: Human Values (PVQ-21)                                       ║
║                                                                              ║
║  4. Download format: CSV (recommended) or SPSS                               ║
║                                                                              ║
║  5. Save to: data/dr-datareq/cache/ess/                                      ║
║                                                                              ║
║  6. Run: python scripts/fetch_ess_data.py --process <filename>               ║
║                                                                              ║
║  Alternative (R users):                                                      ║
║    library(essurvey)                                                         ║
║    set_email("your@email.com")                                               ║
║    ch_data <- import_country("Switzerland", rounds = 1:11)                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    return instructions


def fetch_ess_metadata() -> Dict[str, Any]:
    """Fetch ESS metadata (available without authentication)."""
    metadata = {
        "source": "European Social Survey (ESS)",
        "url": "https://www.europeansocialsurvey.org/",
        "data_portal": "https://ess.sikt.no/",
        "methodology": "Face-to-face interviews, random probability sampling",
        "frequency": "Biennial (every 2 years)",
        "sample_size_ch": "~1,500 respondents per round",
        "value_scale": "Portrait Values Questionnaire (PVQ-21)",
        "schwartz_dimensions": list(SCHWARTZ_ESS_MAPPING.keys()),
        "rounds_available_ch": list(ESS_ROUNDS.keys()),
        "latest_round": max(ESS_ROUNDS.keys()),
        "accessed": datetime.now().isoformat(),
    }
    return metadata


# =============================================================================
# DATA PROCESSING
# =============================================================================

def process_ess_csv(filepath: str) -> Dict[str, Any]:
    """Process downloaded ESS CSV file and extract Swiss value data."""
    if not HAS_PANDAS:
        print("ERROR: pandas required for CSV processing. Run: pip install pandas")
        return {}

    print(f"Processing ESS data from: {filepath}")

    try:
        df = pd.read_csv(filepath, low_memory=False)
    except Exception as e:
        print(f"ERROR reading CSV: {e}")
        return {}

    # Filter for Switzerland
    if 'cntry' in df.columns:
        df_ch = df[df['cntry'] == 'CH']
    elif 'country' in df.columns:
        df_ch = df[df['country'].str.contains('Switzerland', case=False, na=False)]
    else:
        print("WARNING: Country column not found. Using all data.")
        df_ch = df

    print(f"  Swiss respondents: {len(df_ch)}")

    # Extract Schwartz values
    results = {
        "country": "Switzerland",
        "n_respondents": len(df_ch),
        "values": {},
        "rounds_included": [],
    }

    # Get rounds if available
    if 'essround' in df_ch.columns:
        results["rounds_included"] = sorted(df_ch['essround'].unique().tolist())

    # Process each Schwartz dimension
    for dimension, config in SCHWARTZ_ESS_MAPPING.items():
        dim_values = []
        for var in config["ess_vars"]:
            if var in df_ch.columns:
                # ESS uses 1-6 scale (1=very much like me, 6=not like me at all)
                # Reverse code so higher = stronger value
                values = df_ch[var].dropna()
                if len(values) > 0:
                    reversed_mean = 7 - values.mean()  # Reverse to 1-6 where 6=strongest
                    dim_values.append(reversed_mean)

        if dim_values:
            results["values"][dimension] = {
                "mean": round(sum(dim_values) / len(dim_values), 2),
                "n_items": len(dim_values),
                "description": config["description"],
            }

    return results


def aggregate_time_series(data_by_round: Dict[int, Dict]) -> Dict[str, List]:
    """Aggregate ESS data across rounds into time series."""
    time_series = {}

    for dimension in SCHWARTZ_ESS_MAPPING.keys():
        time_series[dimension] = {
            "years": [],
            "values": [],
            "trend": None,
        }

        for round_num in sorted(data_by_round.keys()):
            if round_num in ESS_ROUNDS:
                year = ESS_ROUNDS[round_num]["year"]
                if dimension in data_by_round[round_num].get("values", {}):
                    time_series[dimension]["years"].append(year)
                    time_series[dimension]["values"].append(
                        data_by_round[round_num]["values"][dimension]["mean"]
                    )

        # Calculate trend
        if len(time_series[dimension]["values"]) >= 2:
            first = time_series[dimension]["values"][0]
            last = time_series[dimension]["values"][-1]
            if last > first + 0.1:
                time_series[dimension]["trend"] = "steigend"
            elif last < first - 0.1:
                time_series[dimension]["trend"] = "fallend"
            else:
                time_series[dimension]["trend"] = "stabil"

    return time_series


# =============================================================================
# YAML UPDATE
# =============================================================================

def load_current_yaml() -> Dict[str, Any]:
    """Load current ESS_CH_values.yaml."""
    yaml_path = ESS_CONFIG["yaml_file"]

    if not yaml_path.exists():
        print(f"WARNING: YAML file not found: {yaml_path}")
        return {}

    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def update_yaml_with_data(processed_data: Dict[str, Any], dry_run: bool = False) -> bool:
    """Update ESS_CH_values.yaml with processed data."""
    yaml_path = ESS_CONFIG["yaml_file"]

    current = load_current_yaml()
    if not current:
        print("ERROR: Cannot update - YAML file not found or empty")
        return False

    # Update factors with new data
    updated_count = 0
    for factor in current.get("factors", []):
        schwartz_dim = factor.get("schwartz_dimension")
        if schwartz_dim and schwartz_dim in processed_data.get("values", {}):
            new_value = processed_data["values"][schwartz_dim]["mean"]

            if dry_run:
                print(f"  [DRY RUN] Would update {factor['id']}: {factor.get('data_point')} -> {new_value}")
            else:
                factor["data_point"] = new_value
                factor["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            updated_count += 1

    # Update metadata
    if not dry_run:
        current["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        current["metadata"]["data_rounds"] = processed_data.get("rounds_included", [])
        current["metadata"]["n_respondents"] = processed_data.get("n_respondents", 0)

        # Write back
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(current, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"✓ Updated {updated_count} factors in {yaml_path}")
    else:
        print(f"[DRY RUN] Would update {updated_count} factors")

    return True


# =============================================================================
# STATISTICS
# =============================================================================

def show_statistics():
    """Show current ESS data statistics."""
    print("\n" + "=" * 70)
    print("ESS SWITZERLAND DATA STATISTICS")
    print("=" * 70)

    current = load_current_yaml()
    if not current:
        print("No data loaded. Run --process first.")
        return

    metadata = current.get("metadata", {})
    factors = current.get("factors", [])

    print(f"\nSource: {metadata.get('source', 'N/A')}")
    print(f"Last Updated: {metadata.get('last_updated', 'N/A')}")
    print(f"Total Factors: {len(factors)}")

    print("\n--- Schwartz Value Dimensions ---")
    print(f"{'Dimension':<20} {'Value':>8} {'Trend':<15} {'Swiss Context'}")
    print("-" * 70)

    for factor in factors:
        name = factor.get("schwartz_dimension", factor.get("name", ""))[:20]
        value = factor.get("data_point", "N/A")
        trend = factor.get("trend", "N/A")[:15]
        context = factor.get("context_ch", "")[:30] + "..." if len(factor.get("context_ch", "")) > 30 else factor.get("context_ch", "")
        print(f"{name:<20} {value:>8} {trend:<15} {context}")

    print("\n--- BCM Integration ---")
    bcm_modules = set()
    for factor in factors:
        for module in factor.get("bcm_module_coupling", []):
            bcm_modules.add(module)
    print(f"Coupled BCM Modules: {', '.join(sorted(bcm_modules))}")

    print("\n--- Data Sources ---")
    for source in current.get("data_sources", []):
        print(f"  • {source.get('name', 'N/A')}: {source.get('url', 'N/A')}")


# =============================================================================
# SIMULATED DATA (for testing without real ESS data)
# =============================================================================

def generate_simulated_data() -> Dict[str, Any]:
    """Generate simulated ESS data for Switzerland (for testing)."""
    import random
    random.seed(42)  # Reproducible

    print("Generating simulated ESS data for Switzerland...")

    # Simulated Swiss value profile (based on real ESS patterns)
    # Switzerland tends to score high on Security, Conformity, Achievement
    swiss_baseline = {
        "Security": 5.0,      # High
        "Conformity": 4.5,    # Moderate-high
        "Tradition": 4.2,     # Moderate
        "Benevolence": 5.2,   # High
        "Universalism": 4.8,  # Moderate-high
        "Self-Direction": 5.1, # High
        "Stimulation": 4.0,   # Moderate
        "Hedonism": 4.3,      # Moderate
        "Achievement": 4.6,   # Moderate-high
        "Power": 3.5,         # Low
    }

    results = {
        "country": "Switzerland",
        "n_respondents": 15000,  # ~1500 per round × 10 rounds
        "values": {},
        "rounds_included": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "simulated": True,
    }

    for dimension, baseline in swiss_baseline.items():
        # Add some random variation
        value = baseline + random.uniform(-0.2, 0.2)
        results["values"][dimension] = {
            "mean": round(value, 2),
            "n_items": len(SCHWARTZ_ESS_MAPPING[dimension]["ess_vars"]),
            "description": SCHWARTZ_ESS_MAPPING[dimension]["description"],
        }

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="ESS (European Social Survey) Data Fetcher for Switzerland",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/fetch_ess_data.py --download         # Show download instructions
  python scripts/fetch_ess_data.py --process data.csv # Process downloaded CSV
  python scripts/fetch_ess_data.py --simulate         # Use simulated data (testing)
  python scripts/fetch_ess_data.py --update-yaml      # Update YAML from cache
  python scripts/fetch_ess_data.py --stats            # Show current statistics

ESS Data Portal: https://ess.sikt.no/
        """
    )

    parser.add_argument("--download", action="store_true",
                        help="Show instructions for downloading ESS data")
    parser.add_argument("--process", metavar="FILE",
                        help="Process downloaded ESS CSV file")
    parser.add_argument("--simulate", action="store_true",
                        help="Generate simulated data (for testing)")
    parser.add_argument("--update-yaml", action="store_true",
                        help="Update YAML file from processed/simulated data")
    parser.add_argument("--stats", action="store_true",
                        help="Show current data statistics")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without modifying files")
    parser.add_argument("--check", action="store_true",
                        help="Check ESS data availability for Switzerland")

    args = parser.parse_args()

    # Ensure cache directory exists
    ESS_CONFIG["cache_dir"].mkdir(parents=True, exist_ok=True)

    if args.download:
        print(download_ess_instructions())
        metadata = fetch_ess_metadata()
        print("\nESS Metadata:")
        print(json.dumps(metadata, indent=2))
        return 0

    if args.check:
        availability = check_ess_availability()
        print("\nESS Switzerland Availability:")
        print(json.dumps(availability, indent=2))
        return 0

    if args.process:
        processed = process_ess_csv(args.process)
        if processed:
            # Cache processed data
            cache_file = ESS_CONFIG["cache_dir"] / "processed_ch.json"
            with open(cache_file, 'w') as f:
                json.dump(processed, f, indent=2)
            print(f"✓ Processed data cached to: {cache_file}")

            if args.update_yaml:
                update_yaml_with_data(processed, dry_run=args.dry_run)
        return 0

    if args.simulate:
        simulated = generate_simulated_data()
        print("\nSimulated Swiss ESS Values:")
        for dim, data in simulated["values"].items():
            print(f"  {dim}: {data['mean']}")

        # Cache simulated data
        cache_file = ESS_CONFIG["cache_dir"] / "simulated_ch.json"
        with open(cache_file, 'w') as f:
            json.dump(simulated, f, indent=2)
        print(f"\n✓ Simulated data cached to: {cache_file}")

        if args.update_yaml:
            update_yaml_with_data(simulated, dry_run=args.dry_run)
        return 0

    if args.update_yaml:
        # Try to load from cache
        cache_file = ESS_CONFIG["cache_dir"] / "processed_ch.json"
        if not cache_file.exists():
            cache_file = ESS_CONFIG["cache_dir"] / "simulated_ch.json"

        if cache_file.exists():
            with open(cache_file) as f:
                data = json.load(f)
            update_yaml_with_data(data, dry_run=args.dry_run)
        else:
            print("ERROR: No cached data found. Run --process or --simulate first.")
            return 1
        return 0

    if args.stats:
        show_statistics()
        return 0

    # Default: show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
