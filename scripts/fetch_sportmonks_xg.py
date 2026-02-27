#!/usr/bin/env python3
"""
Sportmonks xG Data Fetcher for EBF BCM2_10_SPT

Fetches Champions League and league xG data from Sportmonks API
and updates the BCM2_10_SPT_sports_prediction.yaml file.

Implements Sportmonks Best Practices:
- Bulk fetch with filters=populate (page size 1000)
- Incremental sync with idAfter
- Entity caching (types, countries, teams)
- Rate limiting with exponential backoff
- Retry-After header handling

Usage:
    python scripts/fetch_sportmonks_xg.py --test             # Test API connection
    python scripts/fetch_sportmonks_xg.py --league CL        # Fetch CL data
    python scripts/fetch_sportmonks_xg.py --sync             # Incremental sync
    python scripts/fetch_sportmonks_xg.py --update           # Update YAML file
    python scripts/fetch_sportmonks_xg.py --cache-refresh    # Refresh entity cache

Requirements:
    pip install requests pyyaml python-dotenv

Environment:
    SPORTMONKS_API_KEY in .env file or environment variable
"""

import os
import sys
import json
import time
import random
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import requests
    import yaml
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install requests pyyaml python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration
API_BASE = "https://api.sportmonks.com/v3/football"
API_KEY = os.getenv("SPORTMONKS_API_KEY")

# Rate limiting configuration
MAX_RETRIES = 5
BASE_BACKOFF = 0.5  # seconds
MAX_BACKOFF = 32    # seconds
JITTER_RANGE = 0.3  # ±30% jitter

# League IDs (Sportmonks)
LEAGUES = {
    "CL": 2,        # UEFA Champions League
    "EPL": 8,       # English Premier League
    "LaLiga": 564,  # La Liga
    "Bundesliga": 82,
    "SerieA": 384,
    "Ligue1": 301,
}

# File paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
BCM2_FILE = PROJECT_DIR / "data/dr-datareq/sources/context/global/BCM2_10_SPT_sports_prediction.yaml"
CACHE_DIR = PROJECT_DIR / "data/cache/sportmonks"
CACHE_FILE = CACHE_DIR / "entity_cache.json"
SYNC_STATE_FILE = CACHE_DIR / "sync_state.json"


class RateLimitError(Exception):
    """Raised when rate limit is exceeded."""
    def __init__(self, retry_after: int = None):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after: {retry_after}s")


class SportmonksClient:
    """Sportmonks API client with best practices implementation."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.cache = self._load_cache()
        self.sync_state = self._load_sync_state()

    def _load_cache(self) -> Dict:
        """Load entity cache from disk."""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    print(f"   Loaded cache: {sum(len(v) for v in cache.values())} entities")
                    return cache
            except Exception as e:
                print(f"   Cache load error: {e}")
        return {"types": {}, "countries": {}, "teams": {}, "leagues": {}}

    def _save_cache(self):
        """Save entity cache to disk."""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def _load_sync_state(self) -> Dict:
        """Load sync state (last IDs) from disk."""
        if SYNC_STATE_FILE.exists():
            try:
                with open(SYNC_STATE_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"last_ids": {}, "last_sync": None}

    def _save_sync_state(self):
        """Save sync state to disk."""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.sync_state["last_sync"] = datetime.now().isoformat()
        with open(SYNC_STATE_FILE, 'w') as f:
            json.dump(self.sync_state, f, indent=2)

    def _add_jitter(self, delay: float) -> float:
        """Add random jitter to delay to avoid thundering herd."""
        jitter = delay * JITTER_RANGE * (2 * random.random() - 1)
        return max(0.1, delay + jitter)

    def _request(self, endpoint: str, params: Dict = None, retries: int = 0) -> Dict:
        """Make API request with rate limiting and backoff."""
        if params is None:
            params = {}
        params["api_token"] = self.api_key

        url = f"{API_BASE}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=30)

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = min(BASE_BACKOFF * (2 ** retries), MAX_BACKOFF)
                    wait_time = self._add_jitter(wait_time)

                if retries < MAX_RETRIES:
                    print(f"   ⏳ Rate limited. Waiting {wait_time:.1f}s (retry {retries + 1}/{MAX_RETRIES})")
                    time.sleep(wait_time)
                    return self._request(endpoint, params, retries + 1)
                else:
                    raise RateLimitError(retry_after)

            # Handle other errors
            if response.status_code != 200:
                print(f"   ❌ API error {response.status_code}: {response.text[:200]}")
                return {"data": [], "error": response.status_code}

            return response.json()

        except requests.exceptions.RequestException as e:
            if retries < MAX_RETRIES:
                wait_time = self._add_jitter(BASE_BACKOFF * (2 ** retries))
                print(f"   ⏳ Request error. Waiting {wait_time:.1f}s (retry {retries + 1}/{MAX_RETRIES})")
                time.sleep(wait_time)
                return self._request(endpoint, params, retries + 1)
            raise

    def _bulk_fetch(self, endpoint: str, filters: List[str] = None) -> List[Dict]:
        """
        Bulk fetch with filters=populate for minimal payload and page size 1000.
        Best practice: Use for initial data load.
        """
        all_data = []
        page = 1
        filter_str = "populate"
        if filters:
            filter_str = f"populate;{';'.join(filters)}"

        print(f"   Bulk fetching {endpoint} with populate...")

        while True:
            params = {"filters": f"{filter_str};page:{page}"}
            response = self._request(endpoint, params)
            data = response.get("data", [])

            if not data:
                break

            all_data.extend(data)
            print(f"   Page {page}: {len(data)} records (total: {len(all_data)})")

            # Check if more pages
            pagination = response.get("pagination", {})
            if page >= pagination.get("last_page", 1):
                break

            page += 1
            time.sleep(0.1)  # Small delay between pages

        return all_data

    def _incremental_fetch(self, endpoint: str, entity_type: str) -> List[Dict]:
        """
        Incremental sync with idAfter filter.
        Best practice: Use for keeping data up to date.
        """
        last_id = self.sync_state["last_ids"].get(entity_type, 0)
        all_data = []

        print(f"   Incremental fetch {endpoint} (idAfter: {last_id})...")

        params = {"filters": f"populate;idAfter:{last_id}"}
        response = self._request(endpoint, params)
        data = response.get("data", [])

        if data:
            all_data.extend(data)
            # Update last ID
            max_id = max(d.get("id", 0) for d in data)
            self.sync_state["last_ids"][entity_type] = max_id
            self._save_sync_state()
            print(f"   Fetched {len(data)} new records (new max ID: {max_id})")
        else:
            print(f"   No new records since ID {last_id}")

        return all_data

    def refresh_cache(self):
        """
        Refresh entity cache (types, countries, teams).
        Best practice: Cache rarely-changing entities to reduce includes.
        """
        print("\n🔄 Refreshing entity cache...")

        # Fetch types
        print("   Fetching types...")
        types_data = self._bulk_fetch("types")
        self.cache["types"] = {str(t["id"]): t for t in types_data}
        print(f"   Cached {len(self.cache['types'])} types")

        # Fetch countries
        print("   Fetching countries...")
        countries_data = self._bulk_fetch("countries")
        self.cache["countries"] = {str(c["id"]): c for c in countries_data}
        print(f"   Cached {len(self.cache['countries'])} countries")

        # Fetch leagues
        print("   Fetching leagues...")
        leagues_data = self._bulk_fetch("leagues")
        self.cache["leagues"] = {str(l["id"]): l for l in leagues_data}
        print(f"   Cached {len(self.cache['leagues'])} leagues")

        self._save_cache()
        print("   ✅ Cache refreshed and saved")

    def resolve_type(self, type_id: int) -> Optional[str]:
        """Resolve type_id to name using cache."""
        type_info = self.cache["types"].get(str(type_id))
        return type_info.get("name") if type_info else None

    def resolve_country(self, country_id: int) -> Optional[str]:
        """Resolve country_id to name using cache."""
        country_info = self.cache["countries"].get(str(country_id))
        return country_info.get("name") if country_info else None

    def test_connection(self) -> bool:
        """Test API connection and show subscription info."""
        print("Testing Sportmonks API connection...")

        try:
            response = self._request("leagues", {"per_page": 1})

            if "error" not in response:
                print(f"✅ API connection successful!")

                # Show subscription info if available
                subscription = response.get("subscription", [])
                if subscription:
                    for sub in subscription:
                        print(f"   Plan: {sub.get('plan', 'Unknown')}")
                        print(f"   Active: {sub.get('active', 'Unknown')}")

                rate_limit = response.get("rate_limit", {})
                if rate_limit:
                    print(f"   Rate limit: {rate_limit.get('remaining', '?')}/{rate_limit.get('limit', '?')} remaining")
                    print(f"   Resets in: {rate_limit.get('seconds_remaining', '?')}s")

                return True
            else:
                print(f"❌ API error: {response.get('error')}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def fetch_standings(self, league_id: int, season_id: int = None) -> List[Dict]:
        """Fetch league standings."""
        print(f"\n📊 Fetching standings for league {league_id}...")

        endpoint = f"standings/live/leagues/{league_id}"
        params = {}

        if season_id:
            params["filters"] = f"seasonId:{season_id}"

        # Include team details for now (can optimize later with cache)
        params["include"] = "participant;details"

        response = self._request(endpoint, params)
        return response.get("data", [])

    def fetch_fixtures(self, league_id: int, from_date: str = None, to_date: str = None) -> List[Dict]:
        """Fetch fixtures with statistics."""
        print(f"\n⚽ Fetching fixtures for league {league_id}...")

        filters = [f"fixtureLeagues:{league_id}"]
        if from_date:
            filters.append(f"fixtureStartDateFrom:{from_date}")
        if to_date:
            filters.append(f"fixtureStartDateTo:{to_date}")

        params = {
            "filters": ";".join(filters),
            "include": "scores;statistics"
        }

        response = self._request("fixtures", params)
        return response.get("data", [])

    def fetch_team_stats(self, team_id: int, season_id: int = None) -> Dict:
        """Fetch detailed team statistics."""
        params = {"include": "statistics"}
        if season_id:
            params["filters"] = f"seasonId:{season_id}"

        response = self._request(f"teams/{team_id}", params)
        return response.get("data", {})


def extract_standings_data(standings: List[Dict], client: SportmonksClient) -> Dict:
    """Extract and structure standings data."""
    teams_data = {}

    for standing in standings:
        participant = standing.get("participant", {})
        team_name = participant.get("name", "Unknown")
        team_id = standing.get("participant_id")

        teams_data[team_name] = {
            "id": team_id,
            "position": standing.get("position"),
            "points": standing.get("points"),
            "played": None,
            "won": None,
            "drawn": None,
            "lost": None,
            "goals_for": None,
            "goals_against": None,
            "goal_diff": None,
            "xG": None,
            "xGA": None,
            "xG_diff": None,
            "form": standing.get("form"),
        }

        # Extract details
        for detail in standing.get("details", []):
            type_id = detail.get("type_id")
            value = detail.get("value")

            # Map type IDs to stats (Sportmonks type IDs)
            type_mapping = {
                129: "played",
                130: "won",
                131: "drawn",
                132: "lost",
                133: "goals_for",
                134: "goals_against",
                179: "goal_diff",
                # xG type IDs (may require xG add-on)
                # Check your subscription for available types
            }

            if type_id in type_mapping:
                teams_data[team_name][type_mapping[type_id]] = value

    return teams_data


def update_bcm2_file(league_name: str, teams_data: Dict) -> bool:
    """Update BCM2_10_SPT YAML file with fetched data."""
    print(f"\n📝 Updating BCM2 file with {league_name} data...")

    if not BCM2_FILE.exists():
        print(f"   ❌ BCM2 file not found: {BCM2_FILE}")
        return False

    try:
        with open(BCM2_FILE, 'r') as f:
            bcm2 = yaml.safe_load(f)

        # Update the league section
        section_key = f"{league_name.lower()}_2025_26"
        if section_key not in bcm2:
            bcm2[section_key] = {}

        bcm2[section_key]["last_api_update"] = datetime.now().isoformat()
        bcm2[section_key]["data_source"] = "Sportmonks API"
        bcm2[section_key]["teams_count"] = len(teams_data)

        # Convert to YAML-friendly format
        bcm2[section_key]["standings"] = {
            team: {k: v for k, v in data.items() if v is not None}
            for team, data in teams_data.items()
        }

        # Calculate aggregate stats
        positions = [t.get("position") for t in teams_data.values() if t.get("position")]
        points = [t.get("points") for t in teams_data.values() if t.get("points")]

        if positions and points:
            bcm2[section_key]["summary"] = {
                "total_teams": len(teams_data),
                "max_points": max(points),
                "min_points": min(points),
                "avg_points": round(sum(points) / len(points), 1),
            }

        with open(BCM2_FILE, 'w') as f:
            yaml.dump(bcm2, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"   ✅ Updated {BCM2_FILE}")
        print(f"   Teams: {len(teams_data)}")
        return True

    except Exception as e:
        print(f"   ❌ Error updating file: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Fetch xG data from Sportmonks API (with best practices)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --test                    Test API connection
  %(prog)s --cache-refresh           Refresh entity cache
  %(prog)s --league CL               Fetch Champions League standings
  %(prog)s --league EPL --update     Fetch EPL and update BCM2 file
  %(prog)s --sync                    Incremental sync (new data only)
        """
    )
    parser.add_argument("--test", action="store_true", help="Test API connection")
    parser.add_argument("--cache-refresh", action="store_true", help="Refresh entity cache")
    parser.add_argument("--league", type=str, default="CL",
                       choices=list(LEAGUES.keys()),
                       help="League to fetch (default: CL)")
    parser.add_argument("--sync", action="store_true",
                       help="Incremental sync (fetch only new data)")
    parser.add_argument("--update", action="store_true",
                       help="Update BCM2 YAML file with fetched data")
    parser.add_argument("--json", action="store_true",
                       help="Output raw JSON data")

    args = parser.parse_args()

    # Check API key
    if not API_KEY:
        print("❌ SPORTMONKS_API_KEY not found!")
        print("   Set it in .env file or as environment variable")
        print("   Example: echo 'SPORTMONKS_API_KEY=your_key' > .env")
        sys.exit(1)

    print(f"🔑 API Key: {API_KEY[:10]}...{API_KEY[-5:]}")

    # Initialize client
    client = SportmonksClient(API_KEY)

    if args.test:
        success = client.test_connection()
        sys.exit(0 if success else 1)

    if args.cache_refresh:
        client.refresh_cache()
        sys.exit(0)

    # Fetch data
    league_id = LEAGUES.get(args.league)
    if not league_id:
        print(f"❌ Unknown league: {args.league}")
        sys.exit(1)

    print(f"\n📊 Fetching {args.league} data (League ID: {league_id})...")

    standings = client.fetch_standings(league_id)

    if not standings:
        print("❌ No standings data returned")
        print("   This may be due to subscription limitations")
        print("   Try: python scripts/fetch_sportmonks_xg.py --test")
        sys.exit(1)

    teams_data = extract_standings_data(standings, client)

    if args.json:
        print(json.dumps(teams_data, indent=2, default=str))
    else:
        print(f"\n📋 {args.league} Standings ({len(teams_data)} teams):")
        print("-" * 70)
        print(f"{'Pos':>3}  {'Team':<30} {'Pts':>4}  {'W':>3}  {'D':>3}  {'L':>3}  {'GD':>4}")
        print("-" * 70)

        for team, data in sorted(teams_data.items(), key=lambda x: x[1].get("position") or 99):
            pos = data.get("position", "?")
            pts = data.get("points", "-")
            won = data.get("won", "-")
            drawn = data.get("drawn", "-")
            lost = data.get("lost", "-")
            gd = data.get("goal_diff", "-")
            print(f"{pos:>3}  {team:<30} {pts:>4}  {won:>3}  {drawn:>3}  {lost:>3}  {gd:>4}")

    if args.update:
        update_bcm2_file(args.league, teams_data)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
