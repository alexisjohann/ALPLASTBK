#!/bin/bash
# =============================================================================
# CLASP SETUP — Einmaliges Setup fuer Google Apps Script Sync
# =============================================================================
#
# Was macht das?
#   Verbindet dieses Repo mit deinem Google Apps Script Projekt.
#   Danach pushed eine GitHub Action automatisch bei .gs-Aenderungen.
#
# Voraussetzungen:
#   - Node.js installiert (node --version)
#   - Zugriff auf das Apps Script Projekt auf script.google.com
#
# Usage:
#   bash scripts/setup_clasp.sh
#
# =============================================================================

set -e

echo ""
echo "============================================"
echo "  CLASP SETUP — Google Apps Script Sync"
echo "============================================"
echo ""

# --- Schritt 1: clasp installieren ---
echo "Schritt 1/4: clasp installieren..."
if command -v clasp &> /dev/null; then
    echo "  clasp bereits installiert: $(clasp --version)"
else
    echo "  Installiere @google/clasp..."
    npm install -g @google/clasp
    echo "  OK: $(clasp --version)"
fi
echo ""

# --- Schritt 2: Login ---
echo "Schritt 2/4: Google Login..."
echo "  Ein Browserfenster oeffnet sich. Melde dich mit deinem Google-Konto an."
echo "  (Das Konto muss Zugriff auf das Apps Script Projekt haben.)"
echo ""
clasp login
echo ""
echo "  OK: Login erfolgreich."
echo ""

# --- Schritt 3: Script ID ---
echo "Schritt 3/4: Apps Script ID eingeben..."
echo ""
echo "  So findest du die Script ID:"
echo "  1. Oeffne script.google.com"
echo "  2. Oeffne dein 'EBF Drive Watcher' Projekt"
echo "  3. Klicke Zahnrad (Projekteinstellungen)"
echo "  4. Kopiere die 'Skript-ID'"
echo ""
read -p "  Script ID: " SCRIPT_ID

if [ -z "$SCRIPT_ID" ]; then
    echo "  FEHLER: Keine Script ID eingegeben!"
    exit 1
fi

# .clasp.json aktualisieren
cat > scripts/google-apps-script/.clasp.json << EOF
{
  "scriptId": "$SCRIPT_ID",
  "rootDir": "."
}
EOF
echo "  OK: .clasp.json aktualisiert."
echo ""

# --- Schritt 4: Test-Push ---
echo "Schritt 4/4: Test-Push..."
cd scripts/google-apps-script
clasp push --force
echo ""
echo "  OK: Apps Script aktualisiert!"
echo ""

# --- GitHub Secret Anleitung ---
echo "============================================"
echo "  FAST FERTIG — Noch GitHub Secret setzen"
echo "============================================"
echo ""
echo "  Fuer automatische Syncs bei jedem Commit:"
echo ""
echo "  1. Kopiere den Inhalt von ~/.clasprc.json:"
echo "     cat ~/.clasprc.json"
echo ""
echo "  2. Gehe zu GitHub → Repo → Settings → Secrets → Actions"
echo ""
echo "  3. Erstelle zwei Secrets:"
echo "     CLASP_TOKEN    = Inhalt von ~/.clasprc.json"
echo "     APPS_SCRIPT_ID = $SCRIPT_ID"
echo ""
echo "  Danach pushed die GitHub Action automatisch bei .gs-Aenderungen."
echo ""
echo "============================================"
echo "  SETUP ABGESCHLOSSEN"
echo "============================================"
echo ""
echo "  Neuen Forscher hinzufuegen:"
echo "    → data/researcher-scraper-config.json editieren"
echo "    → git commit + push"
echo "    → Fertig (Config wird von Apps Script zur Laufzeit geladen)"
echo ""
echo "  Apps Script Code aendern:"
echo "    → scripts/google-apps-script/*.gs editieren"
echo "    → git commit + push auf main"
echo "    → GitHub Action pushed automatisch zu Apps Script"
echo ""
