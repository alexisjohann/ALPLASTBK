#!/bin/bash
# =============================================================================
# TRIGGER LINKEDIN COMPANY MONITOR
# =============================================================================
# Triggers the GitHub Actions workflow to check LinkedIn companies.
#
# Usage:
#   ./scripts/trigger_linkedin_monitor.sh              # All companies
#   ./scripts/trigger_linkedin_monitor.sh COMP-UBS     # Specific company
#
# Requires: GH_TOKEN environment variable or ~/.gh_token file
# =============================================================================

COMPANY_ID="${1:-all}"
BRANCH="${2:-claude/researcher-paper-database-FJ7kO}"
REPO="FehrAdvice-Partners-AG/complementarity-context-framework"

# Get token
if [ -z "$GH_TOKEN" ]; then
    if [ -f ~/.gh_token ]; then
        GH_TOKEN=$(cat ~/.gh_token)
    else
        echo "Error: Set GH_TOKEN environment variable or create ~/.gh_token"
        exit 1
    fi
fi

echo "🔄 Triggering LinkedIn Company Monitor..."
echo "   Company: $COMPANY_ID"
echo "   Branch: $BRANCH"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/workflows/linkedin-company-monitor.yml/dispatches" \
  -d "{\"ref\":\"$BRANCH\",\"inputs\":{\"company_id\":\"$COMPANY_ID\"}}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "204" ]; then
    echo "✅ Workflow triggered successfully!"
    echo ""
    echo "View runs: https://github.com/$REPO/actions/workflows/linkedin-company-monitor.yml"
else
    echo "❌ Failed to trigger workflow (HTTP $HTTP_CODE)"
    echo "$RESPONSE"
    exit 1
fi
