#!/usr/bin/env python3
"""
Lead Enrichment - Get comprehensive profile data from LinkedIn.

Fetches all available information about a person before meetings:
- Professional background
- Current role & company
- Education
- Skills
- Contact info (email, phone if available)

Usage:
    python scripts/enrich_lead.py "https://linkedin.com/in/johndoe"
    python scripts/enrich_lead.py "John Doe" --company "UBS"
    python scripts/enrich_lead.py --email "john.doe@ubs.com"

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


def get_profile_by_url(linkedin_url: str) -> dict:
    """Fetch full profile from LinkedIn URL."""
    if not PROXYCURL_API_KEY:
        print("Error: PROXYCURL_API_KEY not set")
        return {}

    headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}
    params = {
        'url': linkedin_url,
        'fallback_to_cache': 'on-error',
        'use_cache': 'if-present',
        'skills': 'include',
        'inferred_salary': 'include',
        'personal_email': 'include',
        'personal_contact_number': 'include',
        'twitter_profile_id': 'include',
        'facebook_profile_id': 'include',
        'github_profile_id': 'include',
        'extra': 'include',
    }

    try:
        response = requests.get(
            f"{PROXYCURL_BASE_URL}/v2/linkedin",
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: API returned {response.status_code}")
            return {}

    except Exception as e:
        print(f"Error: {e}")
        return {}


def search_person(name: str, company: str = None) -> dict:
    """Search for a person by name and optionally company."""
    if not PROXYCURL_API_KEY:
        print("Error: PROXYCURL_API_KEY not set")
        return {}

    headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}
    params = {
        'first_name': name.split()[0] if ' ' in name else name,
        'last_name': name.split()[-1] if ' ' in name else '',
        'enrich_profiles': 'enrich',
    }

    if company:
        params['current_company_name'] = company

    try:
        response = requests.get(
            f"{PROXYCURL_BASE_URL}/search/person",
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                return results[0]  # Return first match
        return {}

    except Exception as e:
        print(f"Error: {e}")
        return {}


def lookup_by_email(email: str) -> dict:
    """Find LinkedIn profile from email."""
    if not PROXYCURL_API_KEY:
        print("Error: PROXYCURL_API_KEY not set")
        return {}

    headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}
    params = {
        'email': email,
        'enrich_profile': 'enrich',
    }

    try:
        response = requests.get(
            f"{PROXYCURL_BASE_URL}/linkedin/profile/resolve/email",
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        return {}

    except Exception as e:
        print(f"Error: {e}")
        return {}


def format_profile(profile: dict) -> str:
    """Format profile data for display."""
    if not profile:
        return "No profile data found."

    lines = []
    lines.append("=" * 70)
    lines.append(f"  {profile.get('full_name', 'Unknown')}")
    lines.append(f"  {profile.get('headline', '')}")
    lines.append("=" * 70)

    # Current Position
    lines.append("\n📍 CURRENT POSITION")
    lines.append("-" * 40)
    experiences = profile.get('experiences', [])
    if experiences:
        current = experiences[0]
        lines.append(f"  {current.get('title', 'N/A')}")
        lines.append(f"  {current.get('company', 'N/A')}")
        lines.append(f"  {current.get('location', '')}")
        if current.get('starts_at'):
            start = current['starts_at']
            lines.append(f"  Since: {start.get('month', '?')}/{start.get('year', '?')}")

    # Contact Info
    lines.append("\n📧 CONTACT INFO")
    lines.append("-" * 40)
    if profile.get('personal_emails'):
        for email in profile['personal_emails']:
            lines.append(f"  Email: {email}")
    if profile.get('personal_numbers'):
        for phone in profile['personal_numbers']:
            lines.append(f"  Phone: {phone}")
    lines.append(f"  LinkedIn: {profile.get('public_identifier', 'N/A')}")
    if profile.get('twitter_profile_id'):
        lines.append(f"  Twitter: @{profile['twitter_profile_id']}")

    # Summary
    if profile.get('summary'):
        lines.append("\n📝 SUMMARY")
        lines.append("-" * 40)
        summary = profile['summary'][:500] + "..." if len(profile.get('summary', '')) > 500 else profile.get('summary', '')
        lines.append(f"  {summary}")

    # Experience
    lines.append("\n💼 EXPERIENCE")
    lines.append("-" * 40)
    for exp in experiences[:5]:
        title = exp.get('title', 'N/A')
        company = exp.get('company', 'N/A')
        start = exp.get('starts_at', {})
        end = exp.get('ends_at', {})
        start_str = f"{start.get('year', '?')}" if start else "?"
        end_str = f"{end.get('year', '?')}" if end else "Present"
        lines.append(f"  • {title} @ {company}")
        lines.append(f"    {start_str} - {end_str}")

    # Education
    lines.append("\n🎓 EDUCATION")
    lines.append("-" * 40)
    for edu in profile.get('education', [])[:3]:
        school = edu.get('school', 'N/A')
        degree = edu.get('degree_name', '')
        field = edu.get('field_of_study', '')
        lines.append(f"  • {school}")
        if degree or field:
            lines.append(f"    {degree} {field}".strip())

    # Skills
    if profile.get('skills'):
        lines.append("\n🔧 SKILLS")
        lines.append("-" * 40)
        skills = profile['skills'][:10]
        lines.append(f"  {', '.join(skills)}")

    # Languages
    if profile.get('languages'):
        lines.append("\n🌐 LANGUAGES")
        lines.append("-" * 40)
        lines.append(f"  {', '.join(profile['languages'])}")

    lines.append("\n" + "=" * 70)
    lines.append(f"  Enriched at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_to_registry(profile: dict, output_path: str = None):
    """Save profile to leads registry."""
    if not profile:
        return

    lead_id = f"LEAD-{profile.get('public_identifier', 'unknown')}"

    lead_data = {
        'id': lead_id,
        'name': profile.get('full_name'),
        'linkedin_url': f"https://linkedin.com/in/{profile.get('public_identifier')}",
        'headline': profile.get('headline'),
        'current_company': profile.get('experiences', [{}])[0].get('company') if profile.get('experiences') else None,
        'current_title': profile.get('experiences', [{}])[0].get('title') if profile.get('experiences') else None,
        'location': profile.get('city'),
        'emails': profile.get('personal_emails', []),
        'phones': profile.get('personal_numbers', []),
        'enriched_at': datetime.now().isoformat(),
        'full_profile': profile
    }

    # Save to file
    output_file = output_path or f"data/leads/{lead_id}.yaml"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        yaml.dump(lead_data, f, default_flow_style=False, allow_unicode=True)

    print(f"\n✅ Saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Enrich lead profile from LinkedIn'
    )
    parser.add_argument(
        'query',
        nargs='?',
        help='LinkedIn URL or person name'
    )
    parser.add_argument(
        '--company', '-c',
        help='Company name (for name search)'
    )
    parser.add_argument(
        '--email', '-e',
        help='Email address to lookup'
    )
    parser.add_argument(
        '--save', '-s',
        action='store_true',
        help='Save to leads registry'
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

    if not any([args.query, args.email]):
        parser.print_help()
        print("\n\nExamples:")
        print('  python scripts/enrich_lead.py "https://linkedin.com/in/johndoe"')
        print('  python scripts/enrich_lead.py "John Doe" --company "UBS"')
        print('  python scripts/enrich_lead.py --email "john.doe@ubs.com"')
        sys.exit(1)

    profile = {}

    # Determine lookup method
    if args.email:
        print(f"🔍 Looking up email: {args.email}")
        result = lookup_by_email(args.email)
        if result.get('profile'):
            profile = result['profile']
        elif result.get('linkedin_profile_url'):
            profile = get_profile_by_url(result['linkedin_profile_url'])

    elif args.query and args.query.startswith('http'):
        print(f"🔍 Fetching profile: {args.query}")
        profile = get_profile_by_url(args.query)

    else:
        print(f"🔍 Searching for: {args.query}" + (f" at {args.company}" if args.company else ""))
        result = search_person(args.query, args.company)
        if result.get('profile'):
            profile = result['profile']

    if not profile:
        print("\n❌ No profile found.")
        sys.exit(1)

    # Output
    if args.json:
        print(json.dumps(profile, indent=2))
    else:
        print(format_profile(profile))

    # Save
    if args.save:
        save_to_registry(profile, args.output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
