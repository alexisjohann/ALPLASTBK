#!/usr/bin/env python3
"""
Send Daily Pipeline Report via Email
=====================================
Sendet den täglichen Pipeline-Report an Sales Operations (Maria & Nora).

Usage:
    python scripts/send_daily_report.py
    python scripts/send_daily_report.py --dry-run
"""

import os
import sys
import glob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path

# =============================================================================
# KONFIGURATION
# =============================================================================

RECIPIENTS = [
    {"name": "Maria Neumann", "email": "maria.neumann@fehradvice.com"},
    {"name": "Nora Gavazaj Susuri", "email": "nora.gavazajsusuri@fehradvice.com"},
]

REPORTS_DIR = Path("outputs/reports")

# =============================================================================
# FUNCTIONS
# =============================================================================

def get_latest_report():
    """Find the most recent Excel report."""
    pattern = str(REPORTS_DIR / "pipeline_report_*.xlsx")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)


def get_latest_pdf():
    """Find the most recent PDF report."""
    pattern = str(REPORTS_DIR / "pipeline_report_*.pdf")
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)


def create_email_body():
    """Create HTML email body."""
    today = datetime.now().strftime("%d.%m.%Y")

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Open Sans', Arial, sans-serif; color: #25212A; }}
            h1 {{ color: #024079; }}
            .highlight {{ background-color: #F3F5F7; padding: 15px; border-radius: 5px; }}
            .footer {{ color: #888; font-size: 12px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <h1>📊 Täglicher Pipeline Report</h1>
        <p>Guten Morgen,</p>

        <p>anbei der aktuelle Pipeline-Report vom <strong>{today}</strong>.</p>

        <div class="highlight">
            <strong>Im Report enthalten:</strong>
            <ul>
                <li>📋 <strong>Follow-Up Priorität</strong> – Leads nach Dringlichkeit sortiert</li>
                <li>🆕 <strong>Neueste Leads</strong> – Zuletzt erstellte Leads</li>
                <li>📈 <strong>Pipeline Übersicht</strong> – Alle aktiven Leads nach Stage</li>
            </ul>
        </div>

        <p>Der Excel-Report enthält drei Tabs mit allen Details.</p>

        <p>Bei Fragen gerne melden!</p>

        <p>Beste Grüsse,<br>
        FehrAdvice Sales Automation</p>

        <div class="footer">
            <p>—<br>
            Diese E-Mail wurde automatisch generiert.<br>
            FehrAdvice & Partners AG</p>
        </div>
    </body>
    </html>
    """
    return html


def send_email(dry_run=False):
    """Send the daily report email."""

    # Get latest report
    excel_file = get_latest_report()
    pdf_file = get_latest_pdf()

    if not excel_file:
        print("❌ Kein Report gefunden in outputs/reports/")
        return False

    print(f"📎 Excel: {excel_file}")
    if pdf_file:
        print(f"📎 PDF: {pdf_file}")

    # Email settings from environment
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.office365.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_password = os.environ.get("SMTP_PASSWORD", "")
    from_email = os.environ.get("FROM_EMAIL", smtp_user)

    if dry_run or not smtp_user:
        print("\n🧪 DRY RUN - Keine E-Mail gesendet")
        print(f"   Von: {from_email}")
        print(f"   An: {', '.join([r['email'] for r in RECIPIENTS])}")
        print(f"   Betreff: 📊 Pipeline Report {datetime.now().strftime('%d.%m.%Y')}")
        print(f"   Anhänge: {excel_file}")
        if pdf_file:
            print(f"            {pdf_file}")
        return True

    # Create message
    today = datetime.now().strftime("%d.%m.%Y")

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ", ".join([r["email"] for r in RECIPIENTS])
    msg["Subject"] = f"📊 Pipeline Report {today}"

    # Attach HTML body
    msg.attach(MIMEText(create_email_body(), "html"))

    # Attach Excel file
    with open(excel_file, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=pipeline_report_{today.replace('.', '-')}.xlsx"
        )
        msg.attach(part)

    # Attach PDF if available
    if pdf_file:
        with open(pdf_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename=pipeline_report_{today.replace('.', '-')}.pdf"
            )
            msg.attach(part)

    # Send email
    try:
        print(f"\n📧 Sende E-Mail via {smtp_server}:{smtp_port}...")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print("✅ E-Mail erfolgreich gesendet!")
        for r in RECIPIENTS:
            print(f"   → {r['name']} <{r['email']}>")

        return True

    except Exception as e:
        print(f"❌ Fehler beim Senden: {e}")
        return False


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  📧 DAILY PIPELINE REPORT - EMAIL")
    print("=" * 60)
    print()

    dry_run = "--dry-run" in sys.argv

    success = send_email(dry_run=dry_run)

    print()
    print("=" * 60)
    if success:
        print("  ✅ FERTIG")
    else:
        print("  ❌ FEHLER")
    print("=" * 60)

    sys.exit(0 if success else 1)
