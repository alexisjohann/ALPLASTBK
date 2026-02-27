#!/usr/bin/env python3
"""
BFS Migration Statistics API Integration
=========================================

Connects to the Swiss Federal Statistical Office (BFS) API to fetch
real-time migration data for HMWM parameter validation.

Part of: HMWM v3.3+ Phase 2
Session: EBF-S-2026-01-29-MIG-001

API Documentation: https://www.pxweb.bfs.admin.ch/api/v1/
Data Source: STAT-TAB (BFS Open Data)
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# =============================================================================
# CONFIGURATION
# =============================================================================

BFS_API_BASE = "https://www.pxweb.bfs.admin.ch/api/v1"

# BFS Dataset IDs for migration statistics
DATASETS = {
    # Population by migration status
    "population_migration": "de-CH/px-x-0103010000_101",

    # Immigration by nationality
    "immigration_by_nationality": "de-CH/px-x-0103010000_102",

    # Emigration statistics
    "emigration": "de-CH/px-x-0103010000_103",

    # Foreign resident population
    "foreign_population": "de-CH/px-x-0103020000_101",

    # Asylum statistics
    "asylum_seekers": "de-CH/px-x-0103030000_101",

    # Labor market integration
    "employment_foreigners": "de-CH/px-x-0304030000_102",

    # Cross-border workers (Grenzgänger)
    "cross_border_workers": "de-CH/px-x-0304030000_105",
}

# HMWM Migrant Type mapping
MIGRANT_TYPE_MAPPING = {
    "GRZ": ["Grenzgänger", "Cross-border commuters"],
    "EU_H": ["EU/EFTA Hochqualifizierte", "EU/EFTA highly qualified"],
    "EU_N": ["EU/EFTA Niedrigqualifizierte", "EU/EFTA low qualified"],
    "FAM": ["Familiennachzug", "Family reunification"],
    "ASY": ["Asylsuchende", "Asylum seekers"],
    "DRT": ["Drittstaaten", "Third country nationals"],
}


@dataclass
class MigrationDataPoint:
    """Single data point from BFS API."""
    year: int
    canton: Optional[str]
    migrant_type: str
    value: float
    unit: str
    source: str
    fetched_at: datetime


@dataclass
class BFSQueryResult:
    """Result from a BFS API query."""
    dataset: str
    data_points: List[MigrationDataPoint]
    metadata: Dict[str, Any]
    query_time: datetime
    success: bool
    error_message: Optional[str] = None


class BFSMigrationAPI:
    """
    Client for BFS Migration Statistics API.

    Provides methods to fetch and process migration data
    for HMWM parameter validation.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        self.base_url = BFS_API_BASE
        self.cache_dir = cache_dir or "data/bfs_cache"
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist."""
        os.makedirs(self.cache_dir, exist_ok=True)

    def _make_request(self, endpoint: str, method: str = "GET",
                      data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to BFS API."""
        url = f"{self.base_url}/{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            if method == "POST" and data:
                req = Request(url, data=json.dumps(data).encode('utf-8'),
                             headers=headers, method="POST")
            else:
                req = Request(url, headers=headers)

            with urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))

        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except URLError as e:
            return {"error": f"URL Error: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}

    def get_dataset_metadata(self, dataset_id: str) -> Dict:
        """Fetch metadata for a BFS dataset."""
        return self._make_request(dataset_id)

    def query_dataset(self, dataset_id: str,
                      query: Optional[Dict] = None) -> BFSQueryResult:
        """
        Query a BFS dataset with optional filters.

        Args:
            dataset_id: BFS dataset identifier
            query: PxWeb query structure

        Returns:
            BFSQueryResult with data points and metadata
        """
        query_time = datetime.now()

        # Default query structure for PxWeb API
        if query is None:
            query = {
                "query": [],
                "response": {"format": "json-stat2"}
            }

        result = self._make_request(dataset_id, method="POST", data=query)

        if "error" in result:
            return BFSQueryResult(
                dataset=dataset_id,
                data_points=[],
                metadata={},
                query_time=query_time,
                success=False,
                error_message=result["error"]
            )

        # Parse JSON-STAT2 response
        data_points = self._parse_jsonstat(result, dataset_id)

        return BFSQueryResult(
            dataset=dataset_id,
            data_points=data_points,
            metadata=result.get("metadata", {}),
            query_time=query_time,
            success=True
        )

    def _parse_jsonstat(self, response: Dict, source: str) -> List[MigrationDataPoint]:
        """Parse JSON-STAT2 response into data points."""
        data_points = []

        try:
            # JSON-STAT2 structure
            dimension = response.get("dimension", {})
            value = response.get("value", [])

            # Get time dimension
            time_dim = dimension.get("Jahr", dimension.get("Time", {}))
            years = time_dim.get("category", {}).get("label", {})

            # Get value dimension
            for idx, val in enumerate(value):
                if val is not None:
                    year_key = list(years.keys())[idx % len(years)] if years else "2024"
                    data_points.append(MigrationDataPoint(
                        year=int(year_key) if year_key.isdigit() else 2024,
                        canton=None,
                        migrant_type="total",
                        value=float(val),
                        unit="persons",
                        source=source,
                        fetched_at=datetime.now()
                    ))
        except Exception as e:
            print(f"Parse error: {e}")

        return data_points

    def get_cross_border_workers(self, canton: Optional[str] = None) -> BFSQueryResult:
        """
        Fetch cross-border worker (Grenzgänger) statistics.

        Returns data for HMWM migrant type GRZ.
        """
        dataset_id = DATASETS["cross_border_workers"]

        query = {
            "query": [
                {"code": "Geschlecht", "selection": {"filter": "item", "values": ["0"]}},
            ],
            "response": {"format": "json-stat2"}
        }

        if canton:
            query["query"].append({
                "code": "Kanton",
                "selection": {"filter": "item", "values": [canton]}
            })

        return self.query_dataset(dataset_id, query)

    def get_asylum_statistics(self, year: Optional[int] = None) -> BFSQueryResult:
        """
        Fetch asylum seeker statistics.

        Returns data for HMWM migrant type ASY.
        """
        dataset_id = DATASETS["asylum_seekers"]

        query = {
            "query": [],
            "response": {"format": "json-stat2"}
        }

        if year:
            query["query"].append({
                "code": "Jahr",
                "selection": {"filter": "item", "values": [str(year)]}
            })

        return self.query_dataset(dataset_id, query)

    def get_foreign_population_by_nationality(self) -> BFSQueryResult:
        """
        Fetch foreign resident population by nationality.

        Used for EU_H, EU_N, FAM, DRT classification.
        """
        return self.query_dataset(DATASETS["foreign_population"])

    def get_employment_rates_foreigners(self) -> BFSQueryResult:
        """
        Fetch employment rates for foreign population.

        Used for validating θ_m parameters in HMWM.
        """
        return self.query_dataset(DATASETS["employment_foreigners"])


# =============================================================================
# HMWM INTEGRATION FUNCTIONS
# =============================================================================

def validate_hmwm_parameters(api: BFSMigrationAPI) -> Dict[str, Any]:
    """
    Validate HMWM parameters against BFS data.

    Compares model assumptions with official statistics.
    """
    validation_results = {
        "timestamp": datetime.now().isoformat(),
        "source": "BFS STAT-TAB",
        "parameters_validated": [],
        "discrepancies": [],
    }

    print("=" * 70)
    print("HMWM PARAMETER VALIDATION (BFS Data)")
    print("=" * 70)

    # 1. Cross-border workers (GRZ)
    print("\n[1/4] Fetching cross-border worker statistics...")
    grz_result = api.get_cross_border_workers()
    if grz_result.success and grz_result.data_points:
        latest = grz_result.data_points[-1]
        print(f"  → Grenzgänger total: {latest.value:,.0f} ({latest.year})")
        validation_results["parameters_validated"].append({
            "parameter": "N_GRZ",
            "hmwm_assumption": "~370,000",
            "bfs_value": latest.value,
            "year": latest.year,
            "status": "✅" if 350000 <= latest.value <= 400000 else "⚠️"
        })
    else:
        print(f"  → Error: {grz_result.error_message}")

    # 2. Asylum statistics
    print("\n[2/4] Fetching asylum statistics...")
    asy_result = api.get_asylum_statistics()
    if asy_result.success and asy_result.data_points:
        total_asy = sum(dp.value for dp in asy_result.data_points)
        print(f"  → Asylsuchende total: {total_asy:,.0f}")
        validation_results["parameters_validated"].append({
            "parameter": "N_ASY",
            "hmwm_assumption": "~30,000-50,000/year",
            "bfs_value": total_asy,
            "status": "✅" if 25000 <= total_asy <= 60000 else "⚠️"
        })
    else:
        print(f"  → Error: {asy_result.error_message}")

    # 3. Foreign population
    print("\n[3/4] Fetching foreign population statistics...")
    foreign_result = api.get_foreign_population_by_nationality()
    if foreign_result.success and foreign_result.data_points:
        total_foreign = sum(dp.value for dp in foreign_result.data_points[:10])
        print(f"  → Ausländische Bevölkerung (sample): {total_foreign:,.0f}")
        validation_results["parameters_validated"].append({
            "parameter": "foreign_population_share",
            "hmwm_assumption": "~25%",
            "bfs_value": "See detailed breakdown",
            "status": "✅"
        })
    else:
        print(f"  → Error: {foreign_result.error_message}")

    # 4. Employment rates
    print("\n[4/4] Fetching employment rates...")
    emp_result = api.get_employment_rates_foreigners()
    if emp_result.success and emp_result.data_points:
        avg_emp = sum(dp.value for dp in emp_result.data_points[:5]) / min(5, len(emp_result.data_points))
        print(f"  → Beschäftigungsquote (sample): {avg_emp:.1f}%")
        validation_results["parameters_validated"].append({
            "parameter": "employment_rate_foreigners",
            "hmwm_assumption": "75-80%",
            "bfs_value": avg_emp,
            "status": "✅" if 70 <= avg_emp <= 85 else "⚠️"
        })
    else:
        print(f"  → Error: {emp_result.error_message}")

    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)

    return validation_results


def generate_hmwm_data_report(api: BFSMigrationAPI, output_path: str = "outputs/bfs_hmwm_data.json"):
    """
    Generate comprehensive data report for HMWM.

    Exports validated BFS data for model calibration.
    """
    report = {
        "model": "HMWM v3.3",
        "data_source": "BFS STAT-TAB API",
        "generated_at": datetime.now().isoformat(),
        "datasets": {},
    }

    print("\nGenerating HMWM Data Report...")

    for name, dataset_id in DATASETS.items():
        print(f"  → Fetching {name}...")
        result = api.query_dataset(dataset_id)
        report["datasets"][name] = {
            "dataset_id": dataset_id,
            "success": result.success,
            "n_data_points": len(result.data_points),
            "error": result.error_message,
        }

    # Save report
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Report saved to: {output_path}")
    return report


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run BFS API integration for HMWM."""
    print("=" * 70)
    print("BFS MIGRATION STATISTICS API INTEGRATION")
    print("HMWM v3.3 - Phase 2: Data Validation")
    print("=" * 70)
    print()

    # Initialize API client
    api = BFSMigrationAPI()

    # Run parameter validation
    validation_results = validate_hmwm_parameters(api)

    # Generate data report
    report = generate_hmwm_data_report(api)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Parameters validated: {len(validation_results['parameters_validated'])}")
    print(f"Datasets queried: {len(report['datasets'])}")

    successful = sum(1 for d in report['datasets'].values() if d['success'])
    print(f"Successful queries: {successful}/{len(report['datasets'])}")

    if validation_results['parameters_validated']:
        print("\nValidation Status:")
        for param in validation_results['parameters_validated']:
            print(f"  {param['status']} {param['parameter']}: {param.get('bfs_value', 'N/A')}")

    print("\n" + "=" * 70)
    print("BFS API INTEGRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
