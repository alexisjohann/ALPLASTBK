#!/bin/bash
# =============================================================================
# TRIGGER LEAD ENRICHMENT via GitHub Actions
# =============================================================================
# Usage:
#   ./scripts/enrich_lead.sh "https://linkedin.com/in/johndoe"
#   ./scripts/enrich_lead.sh "John Doe" "UBS"
#   ./scripts/enrich_lead.sh --email "john.doe@ubs.com"
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
LINKEDIN_URL=""
NAME=""
COMPANY=""
EMAIL=""

if [ "$1" == "--email" ]; then
    EMAIL="$2"
elif [[ "$1" == http* ]]; then
    LINKEDIN_URL="$1"
else
    NAME="$1"
    COMPANY="$2"
fi

echo "🔍 Triggering Lead Enrichment..."

# Build JSON payload
PAYLOAD="{\"ref\":\"$BRANCH\",\"inputs\":{"
FIRST=true

if [ -n "$LINKEDIN_URL" ]; then
    PAYLOAD="${PAYLOAD}\"linkedin_url\":\"$LINKEDIN_URL\""
    FIRST=false
    echo "   LinkedIn: $LINKEDIN_URL"
fi

if [ -n "$EMAIL" ]; then
    [ "$FIRST" = false ] && PAYLOAD="${PAYLOAD},"
    PAYLOAD="${PAYLOAD}\"email\":\"$EMAIL\""
    FIRST=false
    echo "   Email: $EMAIL"
fi

if [ -n "$NAME" ]; then
    [ "$FIRST" = false ] && PAYLOAD="${PAYLOAD},"
    PAYLOAD="${PAYLOAD}\"name\":\"$NAME\""
    FIRST=false
    echo "   Name: $NAME"
fi

if [ -n "$COMPANY" ]; then
    [ "$FIRST" = false ] && PAYLOAD="${PAYLOAD},"
    PAYLOAD="${PAYLOAD}\"company\":\"$COMPANY\""
    echo "   Company: $COMPANY"
fi

PAYLOAD="${PAYLOAD}}}"

# Trigger workflow
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/actions/workflows/linkedin-lead-enrichment.yml/dispatches" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" = "204" ]; then
    echo ""
    echo "✅ Workflow triggered!"
    echo "   View: https://github.com/$REPO/actions/workflows/linkedin-lead-enrichment.yml"
    echo ""
    echo "   Results will be saved to: data/leads/"
else
    echo "❌ Failed (HTTP $HTTP_CODE)"
    exit 1
fi
