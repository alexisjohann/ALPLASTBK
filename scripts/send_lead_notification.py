#!/usr/bin/env python3
"""
Send Lead Notification Emails

Sends email notifications for:
- New lead creation
- Deadline reminders (1 day before)

Usage:
    python scripts/send_lead_notification.py --new-lead LEAD-013
    python scripts/send_lead_notification.py --check-deadlines
    python scripts/send_lead_notification.py --test

Configuration is read from data/sales/lead-database.yaml
"""

import argparse
import smtplib
import yaml
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

LEAD_DB_PATH = Path(__file__).parent.parent / "data" / "sales" / "lead-database.yaml"

# Email configuration (set via environment variables for security)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.office365.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@fehradvice.com")

# =============================================================================
# LOAD DATABASE
# =============================================================================

def load_database():
    """Load the lead database YAML file."""
    with open(LEAD_DB_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_lead_by_id(db, lead_id):
    """Find a lead by its ID."""
    for lead in db.get("leads", []):
        if lead.get("id") == lead_id:
            return lead
    return None


def get_latest_lead(db):
    """Find the most recently created lead by created_at timestamp."""
    leads = db.get("leads", [])
    if not leads:
        return None

    # Sort by created_at (ISO 8601 strings sort correctly)
    # Falls back to 'created' if 'created_at' not present
    def get_timestamp(lead):
        return lead.get("created_at") or lead.get("created") or ""

    sorted_leads = sorted(leads, key=get_timestamp, reverse=True)
    return sorted_leads[0] if sorted_leads else None


def get_owner_email(db, owner_code):
    """Get owner email from team registry."""
    for owner in db.get("team_registry", {}).get("owners", []):
        if owner.get("code") == owner_code:
            return owner.get("email"), owner.get("full_name")
    return None, None


# =============================================================================
# EMAIL TEMPLATES
# =============================================================================

def create_new_lead_email(lead, db):
    """Create email content for new lead notification."""
    company_name = lead.get("company", {}).get("name", "Unbekannt")
    industry = lead.get("industry", "Unbekannt")
    stage = lead.get("stage", "SUSPECT")
    owner_code = lead.get("relationship", {}).get("owner", "")
    owner_email, owner_name = get_owner_email(db, owner_code)
    fit_score = lead.get("fit_score", "-")

    # Calculate deadline
    deadline_config = db.get("deadline_config", {})
    default_deadlines = deadline_config.get("default_deadlines", {})
    days = default_deadlines.get(stage, 14)
    deadline_date = datetime.now() + timedelta(days=days)

    subject = f"Neuer Lead erstellt: {company_name}"

    body = f"""
Neuer Lead in der Sales-Pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lead-ID:        {lead.get('id')}
Firma:          {company_name}
Branche:        {industry}
Stage:          {stage}
Owner:          {owner_name} ({owner_code})
Fit Score:      {fit_score}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEADLINE:       {deadline_date.strftime('%d.%m.%Y')} ({days} Tage)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Nächste Aktion: {lead.get('next_action', {}).get('description', 'Erstkontakt aufnehmen')}

---
Diese E-Mail wurde automatisch generiert.
FehrAdvice & Partners AG - Sales Pipeline
"""

    return subject, body, deadline_date


def create_reminder_email(lead, db, days_until_deadline):
    """Create email content for deadline reminder."""
    company_name = lead.get("company", {}).get("name", "Unbekannt")
    stage = lead.get("stage", "")
    owner_code = lead.get("relationship", {}).get("owner", "")
    next_action = lead.get("next_action", {})

    if days_until_deadline == 0:
        urgency = "HEUTE FÄLLIG"
    elif days_until_deadline == 1:
        urgency = "MORGEN FÄLLIG"
    else:
        urgency = f"in {days_until_deadline} Tagen fällig"

    subject = f"⏰ Deadline {urgency}: {company_name}"

    body = f"""
Deadline-Erinnerung

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lead-ID:        {lead.get('id')}
Firma:          {company_name}
Stage:          {stage}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏰ DEADLINE:    {urgency}

Nächste Aktion: {next_action.get('type', 'follow_up')}
Beschreibung:   {next_action.get('description', 'Follow-up erforderlich')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bitte zeitnah bearbeiten.

---
Diese E-Mail wurde automatisch generiert.
FehrAdvice & Partners AG - Sales Pipeline
"""

    return subject, body


# =============================================================================
# EMAIL SENDING
# =============================================================================

def send_email(to_emails, subject, body, test_mode=False):
    """Send an email to the specified recipients."""
    if test_mode:
        print(f"\n{'='*60}")
        print(f"TEST MODE - Email would be sent to:")
        print(f"  To: {', '.join(to_emails)}")
        print(f"  Subject: {subject}")
        print(f"{'='*60}")
        print(body)
        print(f"{'='*60}\n")
        return True

    if not SMTP_USER or not SMTP_PASSWORD:
        print("ERROR: SMTP credentials not configured.")
        print("Set environment variables: SMTP_USER, SMTP_PASSWORD")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_emails, msg.as_string())

        print(f"✅ Email sent to: {', '.join(to_emails)}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def get_notification_recipients(db, lead, include_owner=True):
    """Get all recipients for a notification."""
    recipients = []

    # Fixed recipients from config
    notifications = db.get("notifications", {}).get("lead_created", {})
    for recipient in notifications.get("recipients", []):
        email = recipient.get("email")
        if email:
            recipients.append(email)

    # Owner
    if include_owner and notifications.get("notify_owner", True):
        owner_code = lead.get("relationship", {}).get("owner", "")
        owner_email, _ = get_owner_email(db, owner_code)
        if owner_email and owner_email not in recipients:
            recipients.append(owner_email)

    return recipients


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def notify_new_lead(lead_id, test_mode=False):
    """Send notification for a new lead."""
    db = load_database()
    lead = get_lead_by_id(db, lead_id)

    if not lead:
        print(f"❌ Lead not found: {lead_id}")
        return False

    subject, body, deadline = create_new_lead_email(lead, db)
    recipients = get_notification_recipients(db, lead)

    if not recipients:
        print("❌ No recipients configured")
        return False

    print(f"\n📧 Sending new lead notification for {lead_id}")
    print(f"   Deadline: {deadline.strftime('%d.%m.%Y')}")

    return send_email(recipients, subject, body, test_mode)


def check_deadlines(test_mode=False):
    """Check all leads for upcoming deadlines and send reminders."""
    db = load_database()
    deadline_config = db.get("deadline_config", {})

    if not deadline_config.get("enabled", True):
        print("Deadline reminders are disabled")
        return

    reminder_days = deadline_config.get("reminders", {}).get("days_before", [1])
    today = datetime.now().date()

    notifications_sent = 0

    for lead in db.get("leads", []):
        # Skip inactive stages
        stage = lead.get("stage", "")
        if stage in ["CHURNED", "LOST", "WON"]:
            continue

        # Check for next_action with date
        next_action = lead.get("next_action", {})
        action_date_str = next_action.get("date")

        if not action_date_str:
            continue

        try:
            action_date = datetime.strptime(action_date_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        days_until = (action_date - today).days

        if days_until in reminder_days:
            print(f"\n⏰ Reminder for {lead.get('id')}: {days_until} day(s) until deadline")

            subject, body = create_reminder_email(lead, db, days_until)
            recipients = get_notification_recipients(db, lead)

            if send_email(recipients, subject, body, test_mode):
                notifications_sent += 1

    print(f"\n📊 Total reminders sent: {notifications_sent}")


def test_notification():
    """Test the notification system with a sample lead."""
    print("\n🧪 Testing notification system...\n")

    db = load_database()

    # Show configuration
    notifications = db.get("notifications", {}).get("lead_created", {})
    print("Configuration:")
    print(f"  Recipients: {[r.get('email') for r in notifications.get('recipients', [])]}")
    print(f"  Notify Owner: {notifications.get('notify_owner', True)}")

    deadline_config = db.get("deadline_config", {})
    print(f"  Reminder Days: {deadline_config.get('reminders', {}).get('days_before', [1])}")

    # Test with first lead
    leads = db.get("leads", [])
    if leads:
        test_lead = leads[0]
        print(f"\nTesting with lead: {test_lead.get('id')}")
        notify_new_lead(test_lead.get("id"), test_mode=True)

    print("\n✅ Test complete")


# =============================================================================
# CLI
# =============================================================================

def show_latest_lead():
    """Show the most recently created lead."""
    db = load_database()
    lead = get_latest_lead(db)

    if not lead:
        print("❌ Keine Leads in der Datenbank")
        return None

    company_name = lead.get("company", {}).get("name", "Unbekannt")
    created_at = lead.get("created_at") or lead.get("created") or "?"

    print(f"\n📋 Neuester Lead (nach Timestamp):")
    print(f"┌{'─'*60}┐")
    print(f"│  {lead.get('id')}: {company_name:<43} │")
    print(f"├{'─'*60}┤")
    print(f"│  Stage:      {lead.get('stage', '-'):<44} │")
    print(f"│  Owner:      {lead.get('relationship', {}).get('owner', '-'):<44} │")
    print(f"│  Created:    {created_at:<44} │")
    print(f"└{'─'*60}┘\n")

    return lead


def main():
    parser = argparse.ArgumentParser(description="Send lead notification emails")
    parser.add_argument("--new-lead", help="Send notification for new lead (LEAD-XXX)")
    parser.add_argument("--latest", action="store_true", help="Show/notify the most recently created lead")
    parser.add_argument("--check-deadlines", action="store_true", help="Check and send deadline reminders")
    parser.add_argument("--test", action="store_true", help="Test the notification system")
    parser.add_argument("--dry-run", action="store_true", help="Don't actually send emails")
    parser.add_argument("--notify", action="store_true", help="Send notification (use with --latest)")

    args = parser.parse_args()

    if args.test:
        test_notification()
    elif args.latest:
        lead = show_latest_lead()
        if lead and args.notify:
            notify_new_lead(lead.get("id"), test_mode=args.dry_run)
    elif args.new_lead:
        notify_new_lead(args.new_lead, test_mode=args.dry_run)
    elif args.check_deadlines:
        check_deadlines(test_mode=args.dry_run)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
