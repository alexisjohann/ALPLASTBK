#!/bin/bash
# =============================================================================
# Setup GitHub Branch Protection Rules for Merge Conflict Prevention
# =============================================================================
# Run this script once to configure branch protection on the repository.
# Requires: gh CLI authenticated with admin access
#
# Key setting: "Require branches to be up to date before merging"
# This ensures PRs must be rebased/merged with main before they can be merged.
#
# Usage:
#   bash scripts/setup_branch_protection.sh
# =============================================================================

set -euo pipefail

REPO="FehrAdvice-Partners-AG/complementarity-context-framework"
BRANCH="main"

echo "=== Setting up branch protection for $REPO:$BRANCH ==="

# Check if gh is available
if ! command -v gh &> /dev/null; then
    echo "ERROR: gh CLI not found. Install with: apt-get install gh"
    echo ""
    echo "MANUAL ALTERNATIVE:"
    echo "Go to: https://github.com/$REPO/settings/branches"
    echo ""
    echo "1. Click 'Add branch protection rule' (or edit existing)"
    echo "2. Branch name pattern: main"
    echo "3. Enable: 'Require branches to be up to date before merging'"
    echo "4. Save changes"
    echo ""
    echo "This prevents PRs with merge conflicts from being merged."
    exit 1
fi

# Check authentication
if ! gh auth status &> /dev/null; then
    echo "ERROR: Not authenticated. Run: gh auth login"
    exit 1
fi

# Apply branch protection using GitHub API
echo "Applying branch protection rules..."

gh api \
    --method PUT \
    "repos/$REPO/branches/$BRANCH/protection" \
    --input - << 'EOF'
{
    "required_status_checks": {
        "strict": true,
        "contexts": []
    },
    "enforce_admins": false,
    "required_pull_request_reviews": null,
    "restrictions": null,
    "allow_force_pushes": false,
    "allow_deletions": false
}
EOF

echo ""
echo "Branch protection configured:"
echo "  - Require branches to be up to date before merging: ENABLED"
echo "  - Force pushes to main: BLOCKED"
echo "  - Branch deletion: BLOCKED"
echo ""
echo "PRs with merge conflicts will now be blocked from merging until conflicts"
echo "are resolved."
