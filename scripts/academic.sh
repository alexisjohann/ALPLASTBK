#!/bin/bash
# =============================================================================
# ACADEMIC APIs - Unified CLI Access
# =============================================================================
# Quick access to OpenAlex, ORCID, and Unpaywall APIs.
#
# Usage:
#   ./scripts/academic.sh openalex <command> [args]
#   ./scripts/academic.sh orcid <command> [args]
#   ./scripts/academic.sh unpaywall <command> [args]
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_help() {
    echo "Academic APIs - Unified CLI Access"
    echo ""
    echo "OPENALEX (250M+ papers, citations, authors):"
    echo "  ./scripts/academic.sh openalex doi <DOI>          # Paper by DOI"
    echo "  ./scripts/academic.sh openalex author <name>      # Search author"
    echo "  ./scripts/academic.sh openalex author-id <ID>     # Author by OpenAlex ID"
    echo "  ./scripts/academic.sh openalex query <query>      # Search papers"
    echo "  ./scripts/academic.sh openalex related <work-id>  # Related papers"
    echo "  ./scripts/academic.sh openalex citations <work-id> # Papers citing this"
    echo ""
    echo "ORCID (Researcher IDs & publications):"
    echo "  ./scripts/academic.sh orcid <ORCID>               # Full profile"
    echo "  ./scripts/academic.sh orcid search <name>         # Search by name"
    echo "  ./scripts/academic.sh orcid works <ORCID>         # Publications only"
    echo ""
    echo "UNPAYWALL (Open Access finder):"
    echo "  ./scripts/academic.sh unpaywall <DOI>             # Check OA status"
    echo "  ./scripts/academic.sh unpaywall batch <file.bib>  # Process BibTeX"
    echo "  ./scripts/academic.sh unpaywall pdf <DOI>         # Get PDF URL"
    echo ""
    echo "Examples:"
    echo "  ./scripts/academic.sh openalex author \"Ernst Fehr\""
    echo "  ./scripts/academic.sh orcid 0000-0002-1193-4689"
    echo "  ./scripts/academic.sh unpaywall 10.1257/aer.91.5.1369"
}

case "$1" in
    openalex|oa)
        shift
        case "$1" in
            doi|d)
                python "$SCRIPT_DIR/openalex_api.py" --doi "$2" ${@:3}
                ;;
            author|a)
                python "$SCRIPT_DIR/openalex_api.py" --author "$2" ${@:3}
                ;;
            author-id|A)
                python "$SCRIPT_DIR/openalex_api.py" --author-id "$2" ${@:3}
                ;;
            orcid|O)
                python "$SCRIPT_DIR/openalex_api.py" --orcid "$2" ${@:3}
                ;;
            query|q)
                python "$SCRIPT_DIR/openalex_api.py" --query "$2" ${@:3}
                ;;
            related|r)
                python "$SCRIPT_DIR/openalex_api.py" --related "$2" ${@:3}
                ;;
            citations|c)
                python "$SCRIPT_DIR/openalex_api.py" --citations "$2" ${@:3}
                ;;
            institution|i)
                python "$SCRIPT_DIR/openalex_api.py" --institution "$2" ${@:3}
                ;;
            concept)
                python "$SCRIPT_DIR/openalex_api.py" --concept "$2" ${@:3}
                ;;
            *)
                echo "OpenAlex commands: doi, author, author-id, orcid, query, related, citations, institution, concept"
                ;;
        esac
        ;;

    orcid)
        shift
        case "$1" in
            search|s)
                python "$SCRIPT_DIR/orcid_api.py" --search "$2" ${@:3}
                ;;
            works|w)
                python "$SCRIPT_DIR/orcid_api.py" --works "$2" ${@:3}
                ;;
            *)
                # Default: lookup by ORCID
                if [[ "$1" =~ ^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$ ]]; then
                    python "$SCRIPT_DIR/orcid_api.py" --orcid "$1" ${@:2}
                else
                    echo "ORCID commands: <ORCID>, search <name>, works <ORCID>"
                    echo "Example: ./scripts/academic.sh orcid 0000-0002-1193-4689"
                fi
                ;;
        esac
        ;;

    unpaywall|oa-check)
        shift
        case "$1" in
            batch|b)
                python "$SCRIPT_DIR/unpaywall_api.py" --batch "$2" ${@:3}
                ;;
            pdf|p)
                python "$SCRIPT_DIR/unpaywall_api.py" --doi "$2" --download
                ;;
            *)
                # Default: check DOI
                if [[ "$1" =~ ^10\. ]]; then
                    python "$SCRIPT_DIR/unpaywall_api.py" --doi "$1" ${@:2}
                else
                    echo "Unpaywall commands: <DOI>, batch <file.bib>, pdf <DOI>"
                    echo "Example: ./scripts/academic.sh unpaywall 10.1257/aer.91.5.1369"
                fi
                ;;
        esac
        ;;

    help|-h|--help|"")
        show_help
        ;;

    *)
        echo "Unknown API: $1"
        echo "Available: openalex, orcid, unpaywall"
        echo ""
        show_help
        ;;
esac
