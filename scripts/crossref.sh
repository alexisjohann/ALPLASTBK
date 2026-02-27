#!/bin/bash
# =============================================================================
# CROSSREF API - Quick CLI Access
# =============================================================================
# Usage:
#   ./scripts/crossref.sh doi "10.1257/aer.91.5.1369"
#   ./scripts/crossref.sh author "Ernst Fehr"
#   ./scripts/crossref.sh title "Prospect Theory"
#   ./scripts/crossref.sh bibtex "10.1257/aer.91.5.1369"
#   ./scripts/crossref.sh citations "10.1257/aer.91.5.1369"
#   ./scripts/crossref.sh validate "10.1257/aer.91.5.1369"
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
    doi|d)
        python "$SCRIPT_DIR/crossref_api.py" --doi "$2" ${@:3}
        ;;
    author|a)
        python "$SCRIPT_DIR/crossref_api.py" --author "$2" ${@:3}
        ;;
    title|t)
        python "$SCRIPT_DIR/crossref_api.py" --title "$2" ${@:3}
        ;;
    query|q)
        python "$SCRIPT_DIR/crossref_api.py" --query "$2" ${@:3}
        ;;
    bibtex|b)
        python "$SCRIPT_DIR/crossref_api.py" --doi "$2" --bibtex
        ;;
    citations|c)
        python "$SCRIPT_DIR/crossref_api.py" --doi "$2" --citations
        ;;
    references|r)
        python "$SCRIPT_DIR/crossref_api.py" --doi "$2" --references
        ;;
    validate|v)
        python "$SCRIPT_DIR/crossref_api.py" --doi "$2" --validate
        ;;
    enrich)
        shift
        python "$SCRIPT_DIR/enrich_bibtex.py" "$@"
        ;;
    *)
        echo "CrossRef API - Quick CLI Access"
        echo ""
        echo "Usage:"
        echo "  ./scripts/crossref.sh doi <DOI>           # Get paper metadata"
        echo "  ./scripts/crossref.sh author <name>       # Search by author"
        echo "  ./scripts/crossref.sh title <title>       # Search by title"
        echo "  ./scripts/crossref.sh query <query>       # General search"
        echo "  ./scripts/crossref.sh bibtex <DOI>        # Generate BibTeX"
        echo "  ./scripts/crossref.sh citations <DOI>     # Get citation count"
        echo "  ./scripts/crossref.sh references <DOI>    # Get references"
        echo "  ./scripts/crossref.sh validate <DOI>      # Validate DOI"
        echo "  ./scripts/crossref.sh enrich [options]    # Enrich bcm_master.bib"
        echo ""
        echo "Examples:"
        echo "  ./scripts/crossref.sh doi \"10.1257/aer.91.5.1369\""
        echo "  ./scripts/crossref.sh author \"Ernst Fehr\" --rows 20"
        echo "  ./scripts/crossref.sh bibtex \"10.1257/aer.91.5.1369\""
        echo "  ./scripts/crossref.sh enrich --find-dois --limit 50"
        ;;
esac
