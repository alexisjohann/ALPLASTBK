#!/bin/bash
# =============================================================================
# UNIVERSAL API TRIGGER - All APIs via GitHub Actions
# =============================================================================
# Triggers any API through GitHub Actions as proxy.
# Works from Claude or any environment where direct API calls are blocked.
#
# Usage:
#   ./scripts/api.sh <api> <command> [args]
#
# APIs: crossref, openalex, orcid, unpaywall, ssrn, linkedin, serpapi
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

trigger_workflow() {
    local workflow="$1"
    local inputs="$2"

    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
      -H "Authorization: token $GH_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/$REPO/actions/workflows/${workflow}/dispatches" \
      -d "{\"ref\":\"$BRANCH\",\"inputs\":$inputs}")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

    if [ "$HTTP_CODE" = "204" ]; then
        echo "✅ Triggered: $workflow"
        echo "   View: https://github.com/$REPO/actions/workflows/$workflow"
        return 0
    else
        echo "❌ Failed (HTTP $HTTP_CODE)"
        return 1
    fi
}

show_help() {
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║  UNIVERSAL API TRIGGER - All APIs via GitHub                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  CROSSREF (DOI Metadata, Citations):                                         ║
║    ./scripts/api.sh crossref doi <DOI>                                       ║
║    ./scripts/api.sh crossref enrich [--find-dois|--citations]                ║
║                                                                              ║
║  OPENALEX (250M+ Papers):                                                    ║
║    ./scripts/api.sh openalex doi <DOI>                                       ║
║    ./scripts/api.sh openalex author <name>                                   ║
║    ./scripts/api.sh openalex query <search>                                  ║
║                                                                              ║
║  ORCID (Researcher Profiles):                                                ║
║    ./scripts/api.sh orcid <ORCID>                                            ║
║    ./scripts/api.sh orcid search <name>                                      ║
║                                                                              ║
║  UNPAYWALL (Open Access):                                                    ║
║    ./scripts/api.sh unpaywall <DOI>                                          ║
║    ./scripts/api.sh unpaywall batch                                          ║
║                                                                              ║
║  SSRN (Working Papers):                                                      ║
║    ./scripts/api.sh ssrn researcher <RES-ID>                                 ║
║    ./scripts/api.sh ssrn topic <topic>                                       ║
║                                                                              ║
║  LINKEDIN (via Proxycurl):                                                   ║
║    ./scripts/api.sh linkedin lead <url|name> [company]                       ║
║    ./scripts/api.sh linkedin dm <company> [--level] [--role]                 ║
║    ./scripts/api.sh linkedin company [COMP-ID]                               ║
║                                                                              ║
║  SERPAPI (Google Scholar):                                                   ║
║    ./scripts/api.sh serpapi researcher <RES-ID>                              ║
║    ./scripts/api.sh serpapi search <query>                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
}

case "$1" in
    # =========================================================================
    # CROSSREF
    # =========================================================================
    crossref|cr)
        case "$2" in
            doi)
                echo "🔍 CrossRef: Looking up DOI $3"
                trigger_workflow "crossref-bibtex-enrichment.yml" "{\"mode\":\"report\",\"limit\":\"1\"}"
                echo "   Note: Check workflow output for DOI: $3"
                ;;
            enrich)
                mode="report"
                [[ "$3" == "--find-dois" ]] && mode="find-dois"
                [[ "$3" == "--citations" ]] && mode="citations"
                [[ "$3" == "--full" ]] && mode="full"
                echo "🔍 CrossRef: Enriching BibTeX (mode: $mode)"
                trigger_workflow "crossref-bibtex-enrichment.yml" "{\"mode\":\"$mode\",\"apply_updates\":true,\"limit\":\"${4:-100}\"}"
                ;;
            *)
                echo "CrossRef commands: doi <DOI>, enrich [--find-dois|--citations|--full]"
                ;;
        esac
        ;;

    # =========================================================================
    # OPENALEX
    # =========================================================================
    openalex|oa)
        case "$2" in
            doi|author|query|sync)
                echo "🔍 OpenAlex: $2 '$3'"
                trigger_workflow "academic-api-sync.yml" "{\"api\":\"openalex\",\"task\":\"report\",\"limit\":\"${4:-50}\"}"
                echo "   Query: $2 = $3"
                ;;
            *)
                echo "OpenAlex commands: doi <DOI>, author <name>, query <search>"
                ;;
        esac
        ;;

    # =========================================================================
    # ORCID
    # =========================================================================
    orcid)
        case "$2" in
            search)
                echo "🔍 ORCID: Searching for '$3'"
                trigger_workflow "academic-api-sync.yml" "{\"api\":\"orcid\",\"task\":\"sync-researchers\",\"limit\":\"10\"}"
                ;;
            *)
                # Assume it's an ORCID ID
                if [[ "$2" =~ ^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$ ]]; then
                    echo "🔍 ORCID: Looking up $2"
                    trigger_workflow "academic-api-sync.yml" "{\"api\":\"orcid\",\"task\":\"sync-researchers\",\"limit\":\"10\"}"
                else
                    echo "ORCID commands: <ORCID-ID>, search <name>"
                fi
                ;;
        esac
        ;;

    # =========================================================================
    # UNPAYWALL
    # =========================================================================
    unpaywall|oa-check)
        case "$2" in
            batch)
                echo "🔍 Unpaywall: Checking BibTeX for Open Access"
                trigger_workflow "academic-api-sync.yml" "{\"api\":\"unpaywall\",\"task\":\"find-oa\",\"limit\":\"${3:-100}\"}"
                ;;
            *)
                # Assume it's a DOI
                if [[ "$2" =~ ^10\. ]]; then
                    echo "🔍 Unpaywall: Checking OA status for $2"
                    trigger_workflow "academic-api-sync.yml" "{\"api\":\"unpaywall\",\"task\":\"find-oa\",\"limit\":\"1\"}"
                else
                    echo "Unpaywall commands: <DOI>, batch [limit]"
                fi
                ;;
        esac
        ;;

    # =========================================================================
    # SSRN
    # =========================================================================
    ssrn)
        case "$2" in
            researcher|r)
                echo "🔍 SSRN: Checking researcher $3"
                trigger_workflow "ssrn-paper-monitor.yml" "{\"researcher_id\":\"$3\",\"save_results\":true}"
                ;;
            topic|t)
                echo "🔍 SSRN: Searching topic '$3'"
                trigger_workflow "ssrn-paper-monitor.yml" "{\"topic\":\"$3\",\"save_results\":true}"
                ;;
            *)
                echo "SSRN commands: researcher <RES-ID>, topic <topic>"
                ;;
        esac
        ;;

    # =========================================================================
    # LINKEDIN (via Proxycurl)
    # =========================================================================
    linkedin|li)
        case "$2" in
            lead|l)
                if [[ "$3" == http* ]]; then
                    echo "🔍 LinkedIn: Enriching lead from URL"
                    trigger_workflow "linkedin-lead-enrichment.yml" "{\"linkedin_url\":\"$3\"}"
                elif [ -n "$4" ]; then
                    echo "🔍 LinkedIn: Searching '$3' at '$4'"
                    trigger_workflow "linkedin-lead-enrichment.yml" "{\"name\":\"$3\",\"company\":\"$4\"}"
                else
                    echo "Usage: linkedin lead <url> OR linkedin lead <name> <company>"
                fi
                ;;
            dm|decision-makers)
                COMPANY="$3"
                LEVEL="all"
                ROLE="all"
                shift 3
                while [[ $# -gt 0 ]]; do
                    case $1 in
                        --level|-l) LEVEL="$2"; shift 2 ;;
                        --role|-r) ROLE="$2"; shift 2 ;;
                        *) shift ;;
                    esac
                done
                echo "🔍 LinkedIn: Finding decision makers at '$COMPANY'"
                echo "   Level: $LEVEL, Role: $ROLE"
                trigger_workflow "linkedin-decision-makers.yml" "{\"company\":\"$COMPANY\",\"level\":\"$LEVEL\",\"role\":\"$ROLE\"}"
                ;;
            company|c)
                COMP_ID="${3:-all}"
                echo "🔍 LinkedIn: Monitoring company $COMP_ID"
                trigger_workflow "linkedin-company-monitor.yml" "{\"company_id\":\"$COMP_ID\"}"
                ;;
            *)
                echo "LinkedIn commands: lead <url|name> [company], dm <company> [--level] [--role], company [COMP-ID]"
                ;;
        esac
        ;;

    # =========================================================================
    # SERPAPI (Google Scholar)
    # =========================================================================
    serpapi|scholar)
        case "$2" in
            researcher|r)
                echo "🔍 SerpAPI: Checking researcher $3"
                trigger_workflow "researcher-paper-monitor.yml" "{\"researcher_id\":\"$3\"}"
                ;;
            all)
                echo "🔍 SerpAPI: Checking all researchers"
                trigger_workflow "researcher-paper-monitor.yml" "{\"researcher_id\":\"all\"}"
                ;;
            *)
                echo "SerpAPI commands: researcher <RES-ID>, all"
                ;;
        esac
        ;;

    # =========================================================================
    # HELP
    # =========================================================================
    help|-h|--help|"")
        show_help
        ;;

    *)
        echo "Unknown API: $1"
        echo "Available: crossref, openalex, orcid, unpaywall, ssrn, linkedin, serpapi"
        echo ""
        echo "Run './scripts/api.sh help' for full usage"
        ;;
esac
