#!/usr/bin/env python3
"""
Decision Maker Finder - Find C-Level and key executives at a company.

Identifies decision makers by searching for:
- C-Suite (CEO, CFO, COO, CTO, CMO, CHRO, etc.)
- VP/SVP/EVP level
- Directors
- Heads of departments

Usage:
    python scripts/find_decision_makers.py "UBS"
    python scripts/find_decision_makers.py "https://linkedin.com/company/ubs"
    python scripts/find_decision_makers.py "UBS" --role "HR"
    python scripts/find_decision_makers.py "UBS" --level c-suite

API: Proxycurl (requires PROXYCURL_API_KEY)

Author: EBF Team
Version: 1.0.0
"""

import argparse
import json
import os
import sys
from datetime import datetime

import requests
import yaml

PROXYCURL_API_KEY = os.environ.get('PROXYCURL_API_KEY')
PROXYCURL_BASE_URL = "https://nubela.co/proxycurl/api"

# Role patterns for different levels
ROLE_PATTERNS = {
    'c-suite': [
        'CEO', 'Chief Executive', 'Chief Operating', 'COO',
        'CFO', 'Chief Financial', 'CTO', 'Chief Technology',
        'CMO', 'Chief Marketing', 'CHRO', 'Chief Human',
        'CIO', 'Chief Information', 'CDO', 'Chief Digital',
        'Chief Data', 'Chief Strategy', 'CSO', 'Chief Revenue', 'CRO',
        'Managing Director', 'President', 'Geschäftsführer', 'Vorstand',
    ],
    'vp': [
        'Vice President', 'VP', 'SVP', 'EVP', 'Senior Vice',
        'Executive Vice', 'Group Vice',
    ],
    'director': [
        'Director', 'Head of', 'Leiter', 'Direktor',
        'Managing', 'General Manager',
    ],
    'hr': [
        'HR', 'Human Resources', 'People', 'Talent', 'CHRO',
        'Chief People', 'Recruiting', 'L&D', 'Learning',
    ],
    'sales': [
        'Sales', 'Business Development', 'Revenue', 'Commercial',
        'Account', 'Client', 'Customer Success',
    ],
    'marketing': [
        'Marketing', 'Brand', 'Communications', 'CMO', 'Growth',
        'Digital Marketing', 'Content',
    ],
    'finance': [
        'Finance', 'CFO', 'Financial', 'Treasury', 'Controller',
        'Accounting', 'FP&A',
    ],
    'tech': [
        'Technology', 'CTO', 'Engineering', 'IT', 'CIO',
        'Software', 'Data', 'AI', 'Digital', 'Tech',
    ],
}


def get_company_url(company_name: str) -> str:
    """Resolve company name to LinkedIn URL."""
    if company_name.startswith('http'):
        return company_name

    if not PROXYCURL_API_KEY:
        return None

    headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}
    params = {'company_name': company_name}

    try:
        response = requests.get(
            f"{PROXYCURL_BASE_URL}/linkedin/company/resolve",
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get('url')
        return None

    except Exception as e:
        print(f"Error resolving company: {e}")
        return None


def search_employees(company_url: str, role_patterns: list = None, limit: int = 50) -> list:
    """Search for employees at a company matching role patterns."""
    if not PROXYCURL_API_KEY:
        print("Error: PROXYCURL_API_KEY not set")
        return []

    headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}

    # Build role filter
    role_filter = None
    if role_patterns:
        role_filter = '|'.join(role_patterns)

    params = {
        'url': company_url,
        'role_search': role_filter,
        'enrich_profiles': 'enrich',
        'page_size': min(limit, 100),
    }

    try:
        response = requests.get(
            f"{PROXYCURL_BASE_URL}/linkedin/company/employees/search",
            headers=headers,
            params=params,
            timeout=60
        )

        if response.status_code == 200:
            return response.json().get('employees', [])
        else:
            print(f"Error: API returned {response.status_code}")
            return []

    except Exception as e:
        print(f"Error: {e}")
        return []


def categorize_by_level(employees: list) -> dict:
    """Categorize employees by seniority level."""
    categorized = {
        'c_suite': [],
        'vp_level': [],
        'director_level': [],
        'other_senior': [],
    }

    for emp in employees:
        profile = emp.get('profile', {})
        title = (profile.get('headline', '') or '').lower()

        # Check C-Suite
        if any(pattern.lower() in title for pattern in ROLE_PATTERNS['c-suite']):
            categorized['c_suite'].append(emp)
        # Check VP
        elif any(pattern.lower() in title for pattern in ROLE_PATTERNS['vp']):
            categorized['vp_level'].append(emp)
        # Check Director
        elif any(pattern.lower() in title for pattern in ROLE_PATTERNS['director']):
            categorized['director_level'].append(emp)
        else:
            categorized['other_senior'].append(emp)

    return categorized


def format_employee(emp: dict, index: int) -> str:
    """Format single employee for display."""
    profile = emp.get('profile', {})
    lines = []

    name = profile.get('full_name', 'Unknown')
    title = profile.get('headline', 'N/A')
    location = profile.get('city', '')
    linkedin = profile.get('public_identifier', '')

    lines.append(f"  {index}. {name}")
    lines.append(f"     📋 {title}")
    if location:
        lines.append(f"     📍 {location}")
    if linkedin:
        lines.append(f"     🔗 linkedin.com/in/{linkedin}")

    return "\n".join(lines)


def format_results(company_name: str, categorized: dict) -> str:
    """Format all results for display."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  DECISION MAKERS: {company_name}")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)

    total = sum(len(v) for v in categorized.values())
    lines.append(f"\n  Total found: {total}")

    # C-Suite
    if categorized['c_suite']:
        lines.append("\n" + "─" * 70)
        lines.append("  👔 C-SUITE")
        lines.append("─" * 70)
        for i, emp in enumerate(categorized['c_suite'], 1):
            lines.append(format_employee(emp, i))
            lines.append("")

    # VP Level
    if categorized['vp_level']:
        lines.append("\n" + "─" * 70)
        lines.append("  🎯 VP / SVP / EVP")
        lines.append("─" * 70)
        for i, emp in enumerate(categorized['vp_level'], 1):
            lines.append(format_employee(emp, i))
            lines.append("")

    # Director Level
    if categorized['director_level']:
        lines.append("\n" + "─" * 70)
        lines.append("  📊 DIRECTORS / HEADS")
        lines.append("─" * 70)
        for i, emp in enumerate(categorized['director_level'][:10], 1):  # Limit to 10
            lines.append(format_employee(emp, i))
            lines.append("")
        if len(categorized['director_level']) > 10:
            lines.append(f"  ... and {len(categorized['director_level']) - 10} more")

    lines.append("\n" + "=" * 70)

    return "\n".join(lines)


def save_results(company_name: str, categorized: dict, output_path: str = None):
    """Save results to YAML file."""
    # Flatten for saving
    all_contacts = []

    for level, employees in categorized.items():
        for emp in employees:
            profile = emp.get('profile', {})
            all_contacts.append({
                'name': profile.get('full_name'),
                'title': profile.get('headline'),
                'level': level,
                'linkedin': f"https://linkedin.com/in/{profile.get('public_identifier')}",
                'location': profile.get('city'),
                'emails': profile.get('personal_emails', []),
            })

    data = {
        'company': company_name,
        'generated_at': datetime.now().isoformat(),
        'total_contacts': len(all_contacts),
        'by_level': {
            'c_suite': len(categorized['c_suite']),
            'vp_level': len(categorized['vp_level']),
            'director_level': len(categorized['director_level']),
        },
        'contacts': all_contacts
    }

    # Save to file
    safe_name = company_name.lower().replace(' ', '_').replace('/', '_')[:30]
    output_file = output_path or f"data/contacts/DM-{safe_name}.yaml"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    print(f"\n✅ Saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Find decision makers at a company'
    )
    parser.add_argument(
        'company',
        help='Company name or LinkedIn URL'
    )
    parser.add_argument(
        '--role', '-r',
        choices=['hr', 'sales', 'marketing', 'finance', 'tech'],
        help='Filter by department/role'
    )
    parser.add_argument(
        '--level', '-l',
        choices=['c-suite', 'vp', 'director', 'all'],
        default='all',
        help='Filter by seniority level'
    )
    parser.add_argument(
        '--limit', '-n',
        type=int,
        default=50,
        help='Maximum results (default: 50)'
    )
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save results to file'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    # Resolve company URL
    print(f"🔍 Finding decision makers at: {args.company}")

    company_url = get_company_url(args.company)
    if not company_url:
        print(f"\n❌ Could not find company: {args.company}")
        sys.exit(1)

    print(f"   LinkedIn: {company_url}")

    # Build role patterns
    patterns = []
    if args.level == 'c-suite':
        patterns.extend(ROLE_PATTERNS['c-suite'])
    elif args.level == 'vp':
        patterns.extend(ROLE_PATTERNS['vp'])
    elif args.level == 'director':
        patterns.extend(ROLE_PATTERNS['director'])
    else:
        # All senior levels
        patterns.extend(ROLE_PATTERNS['c-suite'])
        patterns.extend(ROLE_PATTERNS['vp'])
        patterns.extend(ROLE_PATTERNS['director'])

    # Add role filter if specified
    if args.role:
        patterns = [p for p in patterns if any(
            rp.lower() in p.lower() for rp in ROLE_PATTERNS[args.role]
        )] + ROLE_PATTERNS[args.role]

    # Search
    print(f"   Searching for {len(patterns)} role patterns...")
    employees = search_employees(company_url, patterns, args.limit)

    if not employees:
        print("\n❌ No decision makers found.")
        sys.exit(1)

    # Categorize
    categorized = categorize_by_level(employees)

    # Output
    if args.json:
        output = {
            'company': args.company,
            'company_url': company_url,
            'results': categorized
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print(format_results(args.company, categorized))

    # Save
    if args.save:
        save_results(args.company, categorized, args.output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
