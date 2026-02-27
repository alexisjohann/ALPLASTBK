#!/bin/bash
# =============================================================================
# TRIGGER SSRN PAPER MONITOR via GitHub Actions
# =============================================================================
# Usage:
#   ./scripts/check_ssrn.sh                           # All researchers
#   ./scripts/check_ssrn.sh --researcher RES-FEHR-E   # Specific researcher
#   ./scripts/check_ssrn.sh --topic "loss aversion"   # Topic search
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
RESEARCHER="all"
TOPIC=""
SAVE="true"

while [[ $# -gt 0 ]]; do
    case $1 in
        --researcher|-r)
            RESEARCHER="$2"
            shift 2
            ;;
        --topic|-t)
            TOPIC="$2"
            shift 2
            ;;
        --no-save)
            SAVE="false"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo "📄 SSRN Paper Monitor"
echo "   Researcher: $RESEARCHER"
if [ -n "$TOPIC" ]; then
    echo "   Topic: $TOPIC"
fi
echo ""

# Build JSON payload
if [ -n "$TOPIC" ]; then
    PAYLOAD="{\"ref\":\"$BRANCH\",\"inputs\":{\"topic\":\"$TOPIC\",\"save_results\":$SAVE}}"
else
    PAYLOAD="{\"ref\":\"$BRANCH\",\"inputs\":{\"researcher_id\":\"$RESEARCHER\",\"save_results\":$SAVE}}"
fi

# Trigger workflow
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/workflows/ssrn-paper-monitor.yml/dispatches" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "204" ]; then
    echo "✅ Workflow triggered!"
    echo "   View: https://github.com/$REPO/actions/workflows/ssrn-paper-monitor.yml"
    echo ""
    echo "   Results will be saved to: data/ssrn/"
else
    echo "❌ Failed (HTTP $HTTP_CODE)"
    exit 1
fi
