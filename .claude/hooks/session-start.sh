#!/bin/bash
# SessionStart Hook for EBF Repository
# Installs LaTeX and Python dependencies for PDF generation and LLM Monte Carlo
set -euo pipefail

# Only run in remote/web environment
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "=== EBF SessionStart Hook ===" >&2

# -----------------------------------------------------------------------------
# LaTeX Installation
# Required for: PDF generation from chapters, appendices, and papers
# -----------------------------------------------------------------------------
if ! command -v pdflatex &> /dev/null; then
  echo "Installing LaTeX (texlive)..." >&2
  apt-get update -qq
  apt-get install -y -qq \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-science \
    --no-install-recommends
  echo "LaTeX installed successfully" >&2
else
  echo "LaTeX already installed" >&2
fi

# -----------------------------------------------------------------------------
# Build Tools Installation
# Required for: Automated builds, format conversion, PR management
# -----------------------------------------------------------------------------
echo "Installing build tools..." >&2
apt-get install -y -qq \
  latexmk \
  pandoc \
  gh \
  --no-install-recommends
echo "Build tools installed" >&2

# -----------------------------------------------------------------------------
# Python Dependencies
# Required for: LLM Monte Carlo scripts, paper generator
# -----------------------------------------------------------------------------
if [ -f "$CLAUDE_PROJECT_DIR/scripts/llm_monte_carlo/requirements.txt" ]; then
  echo "Installing Python dependencies..." >&2
  pip install -q -r "$CLAUDE_PROJECT_DIR/scripts/llm_monte_carlo/requirements.txt"
  echo "Python dependencies installed" >&2
fi

echo "=== EBF SessionStart Hook Complete ===" >&2

# ─────────────────────────────────────────────────────────────────────────
# Database Initialization
# Load and validate all 5 EBF databases at session start
# ─────────────────────────────────────────────────────────────────────────
echo "" >&2
echo "Loading EBF Databases..." >&2

if command -v python3 &> /dev/null && [ -f "$CLAUDE_PROJECT_DIR/scripts/init-databases.py" ]; then
  python3 "$CLAUDE_PROJECT_DIR/scripts/init-databases.py"
else
  echo "⚠️  Database initialization script not available" >&2
fi

echo "" >&2

# ─────────────────────────────────────────────────────────────────────────
# Appendix Code Availability Check
# Show current code usage status for creating new appendices
# ─────────────────────────────────────────────────────────────────────────
if command -v python3 &> /dev/null && [ -f "$CLAUDE_PROJECT_DIR/scripts/check_appendix_available.py" ]; then
  echo "📝 Appendix Code Status:" >&2
  python3 "$CLAUDE_PROJECT_DIR/scripts/check_appendix_available.py" --status 2>&1 | head -5 >&2
  echo "" >&2
  echo "💡 TIP: Before creating a new appendix, run:" >&2
  echo "   python scripts/check_appendix_available.py <CODE>" >&2
  echo "" >&2
else
  echo "⚠️  Appendix code checker not available" >&2
fi

echo "" >&2

# ─────────────────────────────────────────────────────────────────────────
# EBF Model-Building Workflow Reminder
# Ensures the 6-step workflow is triggered for every question
# ─────────────────────────────────────────────────────────────────────────
echo "┌─────────────────────────────────────────────────────────────────┐" >&2
echo "│  🔴 REMINDER: EBF Model-Building Workflow                       │" >&2
echo "├─────────────────────────────────────────────────────────────────┤" >&2
echo "│  Bei JEDER inhaltlichen Frage den 6-Schritt-Workflow nutzen:   │" >&2
echo "│                                                                 │" >&2
echo "│  /find-model --mode schnell    (10 min, ~800 Worte)            │" >&2
echo "│  /find-model --mode standard   (45 min, ~3000 Worte)           │" >&2
echo "│  /find-model --mode tief       (2+ Stunden, ~5000 Worte)       │" >&2
echo "│                                                                 │" >&2
echo "│  Workflow: Kontext → Modell → Parameter → Antwort → Report     │" >&2
echo "└─────────────────────────────────────────────────────────────────┘" >&2
echo "" >&2

# ─────────────────────────────────────────────────────────────────────────
# GitHub Token Reminder
# For gh CLI and GitHub Actions triggering
# ─────────────────────────────────────────────────────────────────────────
echo "┌─────────────────────────────────────────────────────────────────┐" >&2
echo "│  🔑 GITHUB TOKEN                                                │" >&2
echo "├─────────────────────────────────────────────────────────────────┤" >&2
echo "│  Für gh CLI Befehle (PRs, Issues, Workflows triggern):         │" >&2
echo "│                                                                 │" >&2
echo "│  Sage: \"Aktiviere GitHub Token: ghp_xxx...\"                    │" >&2
echo "│                                                                 │" >&2
echo "│  Oder erstelle neuen Token: /github-token                      │" >&2
echo "└─────────────────────────────────────────────────────────────────┘" >&2
echo "" >&2
