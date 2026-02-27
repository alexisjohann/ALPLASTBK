#!/bin/bash
# ============================================================
# FehrAdvice DOCX Skill — Build Script
# Erstellt eine korrekt strukturierte ZIP-Datei für den
# Upload in Claude.ai (Admin Settings → Skills)
#
# Verwendung:
#   ./build-skill.sh
#
# Output:
#   dist/fehradvice-docx.zip
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$SCRIPT_DIR/skill"
DIST_DIR="$SCRIPT_DIR/dist"
OUTPUT="$DIST_DIR/fehradvice-docx.zip"

# Prüfe ob skill/ Ordner existiert
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "❌ Fehler: skill/SKILL.md nicht gefunden."
  echo "   Bitte aus dem Repository-Root ausführen."
  exit 1
fi

# Erstelle dist/ Ordner
mkdir -p "$DIST_DIR"

# Lösche alte Version
rm -f "$OUTPUT"

# WICHTIG: SKILL.md muss im Root des ZIP liegen, nicht in einem Unterordner
cd "$SKILL_DIR"
zip -r "$OUTPUT" \
  SKILL.md \
  scripts/ \
  assets/ \
  references/ \
  -x "*.DS_Store" \
  -x "__MACOSX/*" \
  -x "node_modules/*"

echo ""
echo "✅ Skill-Paket erstellt: dist/fehradvice-docx.zip"
echo ""
echo "Nächster Schritt:"
echo "  1. Claude.ai → Admin Settings → Skills"
echo "  2. Alten Skill entfernen"
echo "  3. dist/fehradvice-docx.zip hochladen"
echo "  4. 'Enabled by default' aktivieren"
echo ""
