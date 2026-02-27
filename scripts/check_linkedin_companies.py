#!/usr/bin/env python3
"""
Check LinkedIn company profiles for updates and changes.

Uses Proxycurl API to access LinkedIn data without restrictions.
Proxycurl: https://proxycurl.com - $10/month for 300 credits

Usage:
    python scripts/check_linkedin_companies.py --registry data/linkedin-company-registry.yaml
    python scripts/check_linkedin_companies.py --company COMP-UBS
    python scripts/check_linkedin_companies.py --output updates.json

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
import yaml

# Proxycurl API (reliable LinkedIn data provider)
PROXYCURL_API_KEY = os.environ.get('PROXYCURL_API_KEY')
PROXYCURL_BASE_URL = "https://nubela.co/proxycurl/api"


def load_registry(registry_path: str) -> dict:
    """Load company registry YAML."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_company_profile(linkedin_url: str) -> dict:
    """
    Fetch company profile from LinkedIn via Proxycurl.

    Args:
        linkedin_url: LinkedIn company URL (e.g., "https://linkedin.com/company/ubs")

    Returns:
        Company data dict
    """
    if not PROXYCURL_API_KEY:
        print("  Warning: PROXYCURL_API_KEY not set")
        return {}

    try:
        headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}
        params = {
            'url': linkedin_url,
            'resolve_numeric_id': 'true',
            'categories': 'include',
            'funding_data': 'include',
            'extra': 'include',
            'exit_data': 'include',
            'acquisitions': 'include',
        }

        response = requests.get(
            f"{PROXYCURL_BASE_URL}/linkedin/company",
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"  Warning: Proxycurl API error {response.status_code}: {response.text[:100]}")
            return {}

    except Exception as e:
        print(f"  Warning: Error fetching company profile: {e}")
        return {}


def get_company_employees_count(linkedin_url: str) -> int:
    """Get employee count for a company."""
    if not PROXYCURL_API_KEY:
        return 0

    try:
        headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}
        params = {'url': linkedin_url}

        response = requests.get(
            f"{PROXYCURL_BASE_URL}/linkedin/company/employees/count",
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('total_employee', 0)
        return 0

    except Exception:
        return 0


def get_company_jobs(linkedin_url: str) -> list:
    """Get job openings for a company."""
    if not PROXYCURL_API_KEY:
        return []

    try:
        headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}
        params = {
            'url': linkedin_url,
            'job_type': 'anything'
        }

        response = requests.get(
            f"{PROXYCURL_BASE_URL}/linkedin/company/job",
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get('job', [])
        return []

    except Exception:
        return []


def detect_changes(company: dict, new_data: dict) -> list:
    """
    Detect significant changes that should trigger alerts.

    Args:
        company: Existing company data from registry
        new_data: Fresh data from API

    Returns:
        List of alert strings
    """
    alerts = []
    current = company.get('current', {})

    # Employee count change > 10%
    old_count = current.get('employee_count', 0)
    new_count = new_data.get('employee_count', 0)
    if old_count and new_count:
        change_pct = abs(new_count - old_count) / old_count * 100
        if change_pct > 10:
            direction = "📈 increased" if new_count > old_count else "📉 decreased"
            alerts.append(f"Employee count {direction} by {change_pct:.1f}% ({old_count:,} → {new_count:,})")

    # Follower count change > 20%
    old_followers = current.get('follower_count', 0)
    new_followers = new_data.get('follower_count', 0)
    if old_followers and new_followers:
        change_pct = abs(new_followers - old_followers) / old_followers * 100
        if change_pct > 20:
            direction = "📈 increased" if new_followers > old_followers else "📉 decreased"
            alerts.append(f"Follower count {direction} by {change_pct:.1f}%")

    # New job openings spike
    old_jobs = current.get('job_openings', 0)
    new_jobs = new_data.get('job_openings_count', 0)
    if new_jobs > old_jobs + 10:
        alerts.append(f"🆕 {new_jobs - old_jobs} new job openings posted")

    return alerts


def check_company(company: dict) -> dict:
    """
    Check a single company for updates.

    Args:
        company: Company dict from registry

    Returns:
        Update data dict
    """
    company_id = company.get('id', 'Unknown')
    linkedin_url = company.get('linkedin_url')

    if not linkedin_url:
        print(f"  Warning: No LinkedIn URL for {company_id}")
        return {}

    print(f"  Fetching profile...")
    profile = get_company_profile(linkedin_url)

    if not profile:
        print(f"  Warning: Could not fetch profile")
        return {}

    # Extract relevant data
    result = {
        'employee_count': profile.get('company_size_on_linkedin'),
        'follower_count': profile.get('follower_count'),
        'headquarters': profile.get('hq', {}).get('city'),
        'industry': profile.get('industry'),
        'description': profile.get('description', '')[:500],
        'website': profile.get('website'),
        'founded_year': profile.get('founded_year'),
        'specialties': profile.get('specialities', []),
        'job_openings_count': len(get_company_jobs(linkedin_url)),
        'fetched_at': datetime.now().isoformat()
    }

    # Detect significant changes
    result['alerts'] = detect_changes(company, result)

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Check LinkedIn company profiles for updates'
    )
    parser.add_argument(
        '--registry',
        default='data/linkedin-company-registry.yaml',
        help='Path to company registry YAML'
    )
    parser.add_argument(
        '--company',
        default='all',
        help='Specific company ID or "all"'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file for updates'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Load registry
    registry_path = Path(args.registry)
    if not registry_path.exists():
        print(f"Error: Registry not found: {registry_path}")
        print("Create it with: data/linkedin-company-registry.yaml")
        sys.exit(1)

    registry = load_registry(registry_path)
    companies = registry.get('companies', {})

    if not companies:
        print("No companies found in registry")
        sys.exit(0)

    # Filter if specific company requested
    if args.company != 'all':
        if args.company not in companies:
            print(f"Company not found: {args.company}")
            sys.exit(1)
        companies = {args.company: companies[args.company]}

    # Check each company
    results = {}
    total_alerts = 0
    changes_found = False

    print(f"\n{'='*60}")
    print(f"LINKEDIN COMPANY CHECK - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    for company_id, company in companies.items():
        company['id'] = company_id
        name = company.get('name', company_id)

        print(f"Checking: {name} ({company_id})")

        update_data = check_company(company)
        results[company_id] = update_data

        if update_data:
            changes_found = True
            if update_data.get('alerts'):
                total_alerts += len(update_data['alerts'])
                print(f"  ⚠️  ALERTS: {len(update_data['alerts'])}")
                for alert in update_data['alerts']:
                    print(f"      - {alert}")
            else:
                print(f"  ✓ No significant changes")
        else:
            print(f"  ✗ Could not fetch data")

        print()

    # Summary
    print(f"{'='*60}")
    print(f"SUMMARY: {len(results)} companies checked, {total_alerts} alerts")
    print(f"{'='*60}\n")

    # Output for GitHub Actions
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)

        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"changes_found={'true' if changes_found else 'false'}\n")
                f.write(f"significant_changes={'true' if total_alerts > 0 else 'false'}\n")
                f.write(f"alert_count={total_alerts}\n")
        else:
            print(f"changes_found={'true' if changes_found else 'false'}")
            print(f"significant_changes={'true' if total_alerts > 0 else 'false'}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
