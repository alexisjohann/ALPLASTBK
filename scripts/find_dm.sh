#!/bin/bash
# =============================================================================
# TRIGGER DECISION MAKER FINDER via GitHub Actions
# =============================================================================
# Usage:
#   ./scripts/find_dm.sh "McKinsey"
#   ./scripts/find_dm.sh "UBS" --level c-suite
#   ./scripts/find_dm.sh "Swisscom" --role hr
#   ./scripts/find_dm.sh "BCG" --level vp --role sales
# =============================================================================

REPO="FehrAdvice-Partners-AG/complementarity-context-framework"
BRANCH="claude/researcher-paper-database-FJ7kO"

# Get token
if [ -z "$GH_TOKEN" ]; then
    if [ -f ~/.gh_token ]; then
        GH_TOKEN=$(cat ~/.gh_token)
    else
        echo "Error: Set GH_TOKEN or create ~/.gh_token"
        exit 1
    fi
fi

# Parse arguments
COMPANY="$1"
LEVEL="all"
ROLE="all"
LIMIT="30"

shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --level|-l)
            LEVEL="$2"
            shift 2
            ;;
        --role|-r)
            ROLE="$2"
            shift 2
            ;;
        --limit|-n)
            LIMIT="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [ -z "$COMPANY" ]; then
    echo "Usage: ./scripts/find_dm.sh <company> [--level c-suite|vp|director] [--role hr|sales|marketing|finance|tech]"
    exit 1
fi

echo "🔍 Finding Decision Makers at: $COMPANY"
echo "   Level: $LEVEL"
echo "   Role: $ROLE"
echo "   Limit: $LIMIT"

# Trigger workflow
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/workflows/linkedin-decision-makers.yml/dispatches" \
  -d "{\"ref\":\"$BRANCH\",\"inputs\":{\"company\":\"$COMPANY\",\"level\":\"$LEVEL\",\"role\":\"$ROLE\",\"limit\":\"$LIMIT\"}}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "204" ]; then
    echo ""
    echo "✅ Workflow triggered!"
    echo "   View: https://github.com/$REPO/actions/workflows/linkedin-decision-makers.yml"
    echo ""
    echo "   Results will be saved to: data/contacts/"
else
    echo "❌ Failed (HTTP $HTTP_CODE)"
    exit 1
fi
