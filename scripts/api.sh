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
BRANCH="${API_BRANCH:-claude/beatrix-hallucination-investigation-HLDWb}"

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
║  MPG PURE (Institutional Repository):                                        ║
║    ./scripts/api.sh mpg find [person] [name]                                 ║
║    ./scripts/api.sh mpg fetch [person] [name] [batch]                        ║
║    ./scripts/api.sh mpg dry-run [person] [name]                              ║
║                                                                              ║
║  MULTISOURCE (PDF from Unpaywall/OpenAlex/EconStor/S2):                      ║
║    ./scripts/api.sh multisource scan [author] [batch]                        ║
║    ./scripts/api.sh multisource fetch [author] [batch]                       ║
║    ./scripts/api.sh multisource dois "10.xxx,10.yyy" [batch]                 ║
║                                                                              ║
║  JEP CATALOG (Journal of Economic Perspectives):                             ║
║    ./scripts/api.sh jep fetch [from_year] [to_year]                          ║
║    ./scripts/api.sh jep dry-run                                              ║
║                                                                              ║
║  GOOGLE DRIVE (File Download):                                               ║
║    ./scripts/api.sh drive download <FILE_ID> [output_name]                   ║
║    ./scripts/api.sh drive split <FILE_ID> [output_name]                      ║
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
    # MPG PURE (Institutional Repository Full-Texts)
    # =========================================================================
    mpg|pure)
        case "$2" in
            find)
                PERSON="${3:-persons206813}"
                NAME="${4:-sutter}"
                echo "🔍 MPG PuRe: Finding INTERNAL_MANAGED files"
                echo "   Person: $PERSON, Author: $NAME"
                trigger_workflow "fetch-mpg-fulltext.yml" "{\"person_id\":\"$PERSON\",\"author_name\":\"$NAME\",\"mode\":\"find-only\",\"dry_run\":\"false\",\"target_branch\":\"$BRANCH\"}"
                ;;
            fetch)
                PERSON="${3:-persons206813}"
                NAME="${4:-sutter}"
                BATCH="${5:-100}"
                echo "🔍 MPG PuRe: Fetching full texts"
                echo "   Person: $PERSON, Author: $NAME, Batch: $BATCH"
                trigger_workflow "fetch-mpg-fulltext.yml" "{\"person_id\":\"$PERSON\",\"author_name\":\"$NAME\",\"batch_size\":\"$BATCH\",\"mode\":\"both\",\"dry_run\":\"false\",\"target_branch\":\"$BRANCH\"}"
                ;;
            dry-run)
                PERSON="${3:-persons206813}"
                NAME="${4:-sutter}"
                echo "🔍 MPG PuRe: Dry run (scan only)"
                trigger_workflow "fetch-mpg-fulltext.yml" "{\"person_id\":\"$PERSON\",\"author_name\":\"$NAME\",\"mode\":\"both\",\"dry_run\":\"true\",\"target_branch\":\"$BRANCH\"}"
                ;;
            *)
                echo "MPG PuRe commands: find [person] [name], fetch [person] [name] [batch], dry-run [person] [name]"
                ;;
        esac
        ;;

    # =========================================================================
    # MULTISOURCE (PDF from Unpaywall/OpenAlex/EconStor/Semantic Scholar)
    # =========================================================================
    multisource|ms)
        case "$2" in
            scan)
                AUTHOR="${3:-}"
                BATCH="${4:-50}"
                echo "🔍 Multi-Source: Scanning for PDF sources"
                echo "   Author: ${AUTHOR:-all}, Batch: $BATCH"
                trigger_workflow "fetch-fulltext-multisource.yml" "{\"author_name\":\"$AUTHOR\",\"batch_size\":\"$BATCH\",\"mode\":\"scan-only\",\"dry_run\":\"false\",\"target_branch\":\"$BRANCH\"}"
                ;;
            fetch)
                AUTHOR="${3:-}"
                BATCH="${4:-50}"
                echo "🔍 Multi-Source: Scanning + Fetching PDFs"
                echo "   Author: ${AUTHOR:-all}, Batch: $BATCH"
                trigger_workflow "fetch-fulltext-multisource.yml" "{\"author_name\":\"$AUTHOR\",\"batch_size\":\"$BATCH\",\"mode\":\"scan-and-fetch\",\"dry_run\":\"false\",\"target_branch\":\"$BRANCH\"}"
                ;;
            dois)
                DOIS="${3:-}"
                BATCH="${4:-50}"
                if [ -z "$DOIS" ]; then
                    echo "Usage: multisource dois \"10.xxx,10.yyy\" [batch]"
                    exit 1
                fi
                echo "🔍 Multi-Source: Fetching specific DOIs"
                echo "   DOIs: $DOIS"
                trigger_workflow "fetch-fulltext-multisource.yml" "{\"dois\":\"$DOIS\",\"batch_size\":\"$BATCH\",\"mode\":\"scan-and-fetch\",\"dry_run\":\"false\",\"target_branch\":\"$BRANCH\"}"
                ;;
            dry-run)
                AUTHOR="${3:-}"
                BATCH="${4:-50}"
                echo "🔍 Multi-Source: Dry run (scan only, no downloads)"
                echo "   Author: ${AUTHOR:-all}, Batch: $BATCH"
                trigger_workflow "fetch-fulltext-multisource.yml" "{\"author_name\":\"$AUTHOR\",\"batch_size\":\"$BATCH\",\"mode\":\"scan-only\",\"dry_run\":\"true\",\"target_branch\":\"$BRANCH\"}"
                ;;
            *)
                echo "Multi-Source commands: scan [author] [batch], fetch [author] [batch], dois \"10.xxx,10.yyy\" [batch], dry-run [author] [batch]"
                ;;
        esac
        ;;

    # =========================================================================
    # JEP CATALOG (Journal of Economic Perspectives)
    # =========================================================================
    jep)
        case "$2" in
            fetch)
                FROM_YEAR="${3:-}"
                TO_YEAR="${4:-}"
                INPUTS="{\"batch_size\":\"100\",\"dry_run\":false,\"skip_paper_yamls\":false"
                [ -n "$FROM_YEAR" ] && INPUTS="$INPUTS,\"from_year\":\"$FROM_YEAR\""
                [ -n "$TO_YEAR" ] && INPUTS="$INPUTS,\"to_year\":\"$TO_YEAR\""
                INPUTS="$INPUTS}"
                echo "📚 JEP: Fetching catalog from CrossRef via GitHub Actions"
                [ -n "$FROM_YEAR" ] && echo "   From: $FROM_YEAR"
                [ -n "$TO_YEAR" ] && echo "   To: $TO_YEAR"
                trigger_workflow "jep-catalog-fetch.yml" "$INPUTS"
                ;;
            dry-run)
                echo "📚 JEP: Dry run (first page only)"
                trigger_workflow "jep-catalog-fetch.yml" "{\"batch_size\":\"100\",\"dry_run\":true,\"skip_paper_yamls\":false}"
                ;;
            *)
                echo "JEP commands: fetch [from_year] [to_year], dry-run"
                echo "  fetch           - Fetch ALL JEP papers (~2300)"
                echo "  fetch 1987 2023 - Fetch specific year range"
                echo "  dry-run         - Test with first page only"
                ;;
        esac
        ;;

    # =========================================================================
    # GOOGLE DRIVE (File Download)
    # =========================================================================
    drive|gdrive|gd)
        case "$2" in
            download|d)
                FILE_ID="${3:-}"
                OUTPUT_NAME="${4:-}"
                if [ -z "$FILE_ID" ]; then
                    echo "Usage: drive download <FILE_ID> [output_name]"
                    echo "  FILE_ID: From Google Drive share URL"
                    echo "  output_name: e.g., jep_vol40_winter2026.pdf"
                    exit 1
                fi
                echo "📁 Google Drive: Downloading file"
                echo "   File ID: $FILE_ID"
                [ -n "$OUTPUT_NAME" ] && echo "   Output: $OUTPUT_NAME"
                trigger_workflow "fetch-google-drive.yml" "{\"file_id\":\"$FILE_ID\",\"output_name\":\"${OUTPUT_NAME:-}\",\"convert_pdf\":\"true\",\"split_papers\":\"false\",\"target_branch\":\"$BRANCH\"}"
                ;;
            split)
                FILE_ID="${3:-}"
                OUTPUT_NAME="${4:-}"
                if [ -z "$FILE_ID" ]; then
                    echo "Usage: drive split <FILE_ID> [output_name]"
                    echo "  Downloads PDF, converts to text, splits into individual papers"
                    exit 1
                fi
                echo "📁 Google Drive: Download + Convert + Split"
                echo "   File ID: $FILE_ID"
                [ -n "$OUTPUT_NAME" ] && echo "   Output: $OUTPUT_NAME"
                trigger_workflow "fetch-google-drive.yml" "{\"file_id\":\"$FILE_ID\",\"output_name\":\"${OUTPUT_NAME:-}\",\"convert_pdf\":\"true\",\"split_papers\":\"true\",\"target_branch\":\"$BRANCH\"}"
                ;;
            *)
                echo "Google Drive commands:"
                echo "  download <FILE_ID> [name]  - Download file from Google Drive"
                echo "  split <FILE_ID> [name]     - Download + convert PDF + split into papers"
                echo ""
                echo "  FILE_ID is from the Google Drive share URL:"
                echo "  https://drive.google.com/file/d/<FILE_ID>/view"
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
        echo "Available: crossref, openalex, orcid, unpaywall, ssrn, linkedin, serpapi, mpg, multisource, jep, drive"
        echo ""
        echo "Run './scripts/api.sh help' for full usage"
        ;;
esac
