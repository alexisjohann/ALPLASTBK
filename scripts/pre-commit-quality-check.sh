#!/bin/bash
#
# EBF Pre-Commit Quality Check Hook
# ======================================
#
# Automatische Qualitätsprüfung bei Appendix-Änderungen
#
# Installation:
#   cp scripts/pre-commit-quality-check.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Oder mit Symlink:
#   ln -sf ../../scripts/pre-commit-quality-check.sh .git/hooks/pre-commit
#

set -e

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  EBF Pre-Commit Quality Check${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"

# Finde geänderte Appendix-Dateien
CHANGED_APPENDICES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^appendices/[A-Z]+.*\.tex$' || true)

if [ -z "$CHANGED_APPENDICES" ]; then
    echo -e "${GREEN}Keine Appendix-Änderungen gefunden. Commit wird fortgesetzt.${NC}"
    exit 0
fi

echo -e "\n${YELLOW}Geänderte Appendices gefunden:${NC}"
echo "$CHANGED_APPENDICES" | while read -r file; do
    echo "  - $file"
done

# Prüfe Compliance für jedes geänderte Appendix
FAILED=0
WARNINGS=0
RESULTS=""

echo -e "\n${BLUE}Führe Compliance-Checks durch...${NC}\n"

for appendix in $CHANGED_APPENDICES; do
    if [ -f "$appendix" ]; then
        echo -e "${BLUE}Prüfe: $appendix${NC}"

        # Führe Compliance-Check aus und capture Output
        OUTPUT=$(python scripts/check_template_compliance.py "$appendix" 2>&1)

        # Extrahiere Score und Grade
        SCORE=$(echo "$OUTPUT" | grep "TOTAL SCORE:" | awk '{print $3}' | tr -d '%')
        GRADE=$(echo "$OUTPUT" | grep "GRADE:" | sed 's/.*GRADE: //')
        CATEGORY=$(echo "$OUTPUT" | grep "KATEGORIE:" | sed 's/.*KATEGORIE: //')

        if [ -z "$SCORE" ]; then
            SCORE="0"
        fi

        # Bewerte Ergebnis
        SCORE_INT=${SCORE%.*}  # Entferne Dezimalstellen

        if [ "$SCORE_INT" -lt 50 ]; then
            echo -e "  ${RED}Score: ${SCORE}% - $GRADE${NC}"
            echo -e "  ${RED}Kategorie: $CATEGORY${NC}"
            FAILED=$((FAILED + 1))
            RESULTS="${RESULTS}\n${RED}FAIL${NC}: $appendix (${SCORE}%)"
        elif [ "$SCORE_INT" -lt 85 ]; then
            echo -e "  ${YELLOW}Score: ${SCORE}% - $GRADE${NC}"
            echo -e "  ${YELLOW}Kategorie: $CATEGORY${NC}"
            WARNINGS=$((WARNINGS + 1))
            RESULTS="${RESULTS}\n${YELLOW}WARN${NC}: $appendix (${SCORE}%)"
        else
            echo -e "  ${GREEN}Score: ${SCORE}% - $GRADE${NC}"
            echo -e "  ${GREEN}Kategorie: $CATEGORY${NC}"
            RESULTS="${RESULTS}\n${GREEN}PASS${NC}: $appendix (${SCORE}%)"
        fi
        echo ""
    fi
done

# Zusammenfassung
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Zusammenfassung${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "$RESULTS"
echo ""

# Entscheidung
if [ "$FAILED" -gt 0 ]; then
    echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}  COMMIT BLOCKIERT: $FAILED Appendix(es) unter 50% Compliance${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "Bitte beheben Sie die Compliance-Probleme oder verwenden Sie:"
    echo -e "  ${YELLOW}git commit --no-verify${NC}  (um Hook zu überspringen)"
    echo ""
    echo -e "Für Details führen Sie aus:"
    echo -e "  ${BLUE}python scripts/check_template_compliance.py appendices/<file>.tex${NC}"
    echo ""
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  WARNUNG: $WARNINGS Appendix(es) unter 85% Compliance${NC}"
    echo -e "${YELLOW}  Commit wird fortgesetzt, aber Verbesserung empfohlen.${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
fi

echo -e "${GREEN}Commit wird fortgesetzt...${NC}"
exit 0
