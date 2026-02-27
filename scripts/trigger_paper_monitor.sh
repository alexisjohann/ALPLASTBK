#!/bin/bash
# =============================================================================
# TRIGGER RESEARCHER PAPER MONITOR
# =============================================================================
# Triggers the GitHub Actions workflow to check for new papers.
#
# Usage:
#   ./scripts/trigger_paper_monitor.sh                    # All researchers
#   ./scripts/trigger_paper_monitor.sh RES-ENKE-B         # Specific researcher
#   ./scripts/trigger_paper_monitor.sh all main           # Different branch
#
# Requires: GH_TOKEN environment variable or ~/.gh_token file
# =============================================================================

RESEARCHER_ID="${1:-all}"
BRANCH="${2:-claude/researcher-paper-database-FJ7kO}"
REPO="FehrAdvice-Partners-AG/complementarity-context-framework"

# Get token from environment or file
if [ -z "$GH_TOKEN" ]; then
    if [ -f ~/.gh_token ]; then
        GH_TOKEN=$(cat ~/.gh_token)
    else
        echo "Error: Set GH_TOKEN environment variable or create ~/.gh_token"
        exit 1
    fi
fi

echo "🔄 Triggering Researcher Paper Monitor..."
echo "   Researcher: $RESEARCHER_ID"
echo "   Branch: $BRANCH"
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/workflows/researcher-paper-monitor.yml/dispatches" \
  -d "{\"ref\":\"$BRANCH\",\"inputs\":{\"researcher_id\":\"$RESEARCHER_ID\",\"auto_add\":\"true\"}}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "204" ]; then
    echo "✅ Workflow triggered successfully!"
    echo ""
    echo "View runs: https://github.com/$REPO/actions/workflows/researcher-paper-monitor.yml"
else
    echo "❌ Failed to trigger workflow (HTTP $HTTP_CODE)"
    echo "$BODY"
    exit 1
fi
