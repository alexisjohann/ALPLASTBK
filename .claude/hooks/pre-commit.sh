#!/bin/bash
# PreCommit Hook for EBF Repository
# Validates chapter/appendix compliance before allowing commits
# Auto-generates TOC/Index from SSOT YAML
set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────
# MERGE CONFLICT PREVENTION: Check branch freshness before commit
# Warns if branch has diverged from main with overlapping file changes
# ─────────────────────────────────────────────────────────────────────────
if [ -f "$CLAUDE_PROJECT_DIR/scripts/check_branch_freshness.py" ]; then
  # Only check if we're on a feature branch (not main)
  CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

  if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "unknown" ]; then
    # Fetch main silently (with timeout to not block commits if offline)
    timeout 10 git fetch origin main --quiet 2>/dev/null || true

    # Check for potential file conflicts
    FRESHNESS_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/check_branch_freshness.py" --file-conflicts 2>&1 || true)
    FRESHNESS_STATUS=$?

    if [ $FRESHNESS_STATUS -eq 1 ]; then
      echo "" >&2
      echo "┌─────────────────────────────────────────────────────────────────────────┐" >&2
      echo "│  ⚠️  MERGE CONFLICT WARNING                                              │" >&2
      echo "├─────────────────────────────────────────────────────────────────────────┤" >&2
      echo "│                                                                         │" >&2
      echo "│  Files you're committing have ALSO been changed on main.               │" >&2
      echo "│  This will cause merge conflicts when creating a PR!                    │" >&2
      echo "│                                                                         │" >&2
      echo "$FRESHNESS_RESULT" | while IFS= read -r line; do
        printf "│  %-71s│\n" "$line" >&2
      done
      echo "│                                                                         │" >&2
      echo "│  FIX NOW (recommended):                                                │" >&2
      echo "│    git stash                                                            │" >&2
      echo "│    git fetch origin main && git rebase origin/main                      │" >&2
      echo "│    git stash pop                                                        │" >&2
      echo "│                                                                         │" >&2
      echo "│  Or continue and resolve conflicts later in the PR.                     │" >&2
      echo "└─────────────────────────────────────────────────────────────────────────┘" >&2
      echo "" >&2
      # Warning only - don't block the commit, but make it very visible
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# TASK-LOG CHECK: Remind to track tasks in task-log.yaml
# ─────────────────────────────────────────────────────────────────────────
TASK_LOG="$CLAUDE_PROJECT_DIR/data/task-log.yaml"
if [ -f "$TASK_LOG" ]; then
  # Check if there's an in_progress task
  HAS_OPEN_TASK=$(grep -c "status: in_progress" "$TASK_LOG" 2>/dev/null || echo "0")

  if [ "$HAS_OPEN_TASK" -eq 0 ]; then
    echo "" >&2
    echo "┌─────────────────────────────────────────────────────────────────────────┐" >&2
    echo "│  ⚠️  TASK-LOG REMINDER                                                  │" >&2
    echo "├─────────────────────────────────────────────────────────────────────────┤" >&2
    echo "│  Kein offener Task in data/task-log.yaml gefunden.                      │" >&2
    echo "│  Pflicht-Workflow: Empfehlung → Coding-Mode → Task loggen → Arbeiten   │" >&2
    echo "│  Siehe CLAUDE.md: Experiment-First + Empfehlungs-Workflow               │" >&2
    echo "└─────────────────────────────────────────────────────────────────────────┘" >&2
    echo "" >&2
    # Warning only - don't block (task may have just been completed)
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# POST-TASK COMPLETION CHECK: Validate task-log entries when modified
# ─────────────────────────────────────────────────────────────────────────
STAGED_TASK_LOG=$(git diff --cached --name-only --diff-filter=ACM | grep 'task-log.yaml$' || true)
if [ -n "$STAGED_TASK_LOG" ] && [ -f "$CLAUDE_PROJECT_DIR/scripts/check_task_completion.py" ]; then
  echo "=== EBF PreCommit: Post-Task Completion Check ===" >&2
  TASK_CHECK=$(python "$CLAUDE_PROJECT_DIR/scripts/check_task_completion.py" --last 2>&1)
  TASK_CHECK_STATUS=$?

  if [ $TASK_CHECK_STATUS -ne 0 ]; then
    echo "" >&2
    echo "┌─────────────────────────────────────────────────────────────────────────┐" >&2
    echo "│  ❌ POST-TASK COMPLETION VIOLATION                                      │" >&2
    echo "├─────────────────────────────────────────────────────────────────────────┤" >&2
    echo "$TASK_CHECK" | while IFS= read -r line; do
      printf "│  %-71s│\n" "$line" >&2
    done
    echo "│                                                                         │" >&2
    echo "│  Fix: Ergänze outcome, ebf_impact und timing in task-log.yaml          │" >&2
    echo "│  Dann: SOFORT nächste 3-Tier-Box zeigen (NICHT fragen!)                │" >&2
    echo "└─────────────────────────────────────────────────────────────────────────┘" >&2
    echo "" >&2
    # Warning — don't block, but make visible
  else
    echo "   Post-Task Check: OK ✅" >&2
  fi
fi

# Get list of staged files
STAGED_TEX=$(git diff --cached --name-only --diff-filter=ACM | grep '\.tex$' || true)
STAGED_YAML_MAPPING=$(git diff --cached --name-only --diff-filter=ACM | grep 'chapter-appendix-mapping.yaml$' || true)

# ─────────────────────────────────────────────────────────────────────────
# AUTO-GENERATE: Update TOC/Index from YAML SSOT
# ─────────────────────────────────────────────────────────────────────────
if [ -n "$STAGED_YAML_MAPPING" ]; then
  echo "=== EBF PreCommit: Auto-Generating Tables from YAML ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/generate_chapter_tables.py" ]; then
    echo "Regenerating LaTeX tables from chapter-appendix-mapping.yaml..." >&2

    # Run the generator for BOTH index files
    python "$CLAUDE_PROJECT_DIR/scripts/generate_chapter_tables.py" --update-all 2>&1 | sed 's/^/   /' >&2

    # Stage the updated appendix index file if it changed
    if [ -f "$CLAUDE_PROJECT_DIR/appendices/00_appendix_index.tex" ]; then
      git add "$CLAUDE_PROJECT_DIR/appendices/00_appendix_index.tex" 2>/dev/null || true
      echo "✅ AUTO-STAGED: appendices/00_appendix_index.tex" >&2
    fi

    # Stage the updated chapter index file if it changed
    if [ -f "$CLAUDE_PROJECT_DIR/chapters/00_chapter_index.tex" ]; then
      git add "$CLAUDE_PROJECT_DIR/chapters/00_chapter_index.tex" 2>/dev/null || true
      echo "✅ AUTO-STAGED: chapters/00_chapter_index.tex" >&2
    fi

    echo "" >&2
  fi
fi

# Skip remaining checks if no .tex files staged
if [ -z "$STAGED_TEX" ] && [ -z "$STAGED_YAML_MAPPING" ]; then
  exit 0
fi

echo "=== EBF PreCommit: Checking Template Compliance ===" >&2

# ─────────────────────────────────────────────────────────────────────────
# Check if new appendices use valid codes
# ─────────────────────────────────────────────────────────────────────────
echo "Checking appendix code availability..." >&2

NEW_APPENDICES=$(git diff --cached --name-only --diff-filter=A | grep 'appendices/.*\.tex$' | grep -v '00_' || true)

FAILED=0

for file in $NEW_APPENDICES; do
  # Extract code from filename (e.g., "BD_alesina.tex" -> "BD")
  CODE=$(basename "$file" | cut -d'_' -f1)

  # Check if code is valid
  USED=$(grep "^${CODE} &" "$CLAUDE_PROJECT_DIR/appendices/00_appendix_index.tex" || echo "")

  if [ -n "$USED" ]; then
    echo "❌ CONFLICT: Code $CODE already in use in $file" >&2
    echo "   Run: python scripts/check_appendix_available.py --suggest" >&2
    FAILED=1
  else
    echo "✅ Code $CODE is available" >&2
  fi
done

for file in $STAGED_TEX; do
  # Skip template and index files
  if [[ "$file" == *"00_"* ]] || [[ "$file" == *"template"* ]]; then
    continue
  fi

  # Check chapters
  if [[ "$file" == chapters/*.tex ]]; then
    echo "Checking chapter: $file" >&2
    SCORE=$(python "$CLAUDE_PROJECT_DIR/scripts/check_chapter_compliance.py" "$CLAUDE_PROJECT_DIR/$file" 2>/dev/null | grep "OVERALL SCORE" | grep -oE '[0-9]+' | head -1 || echo "0")

    if [ "$SCORE" -lt 85 ]; then
      echo "❌ FAILED: $file (Score: $SCORE% < 85%)" >&2
      FAILED=1
    else
      echo "✅ PASSED: $file (Score: $SCORE%)" >&2
    fi
  fi

  # Check appendices
  if [[ "$file" == appendices/*.tex ]]; then
    echo "Checking appendix: $file" >&2
    SCORE=$(python "$CLAUDE_PROJECT_DIR/scripts/check_template_compliance.py" "$CLAUDE_PROJECT_DIR/$file" 2>/dev/null | grep "OVERALL SCORE" | grep -oE '[0-9]+' | head -1 || echo "0")

    if [ "$SCORE" -lt 85 ]; then
      echo "❌ FAILED: $file (Score: $SCORE% < 85%)" >&2
      FAILED=1
    else
      echo "✅ PASSED: $file (Score: $SCORE%)" >&2
    fi
  fi
done

if [ "$FAILED" -eq 1 ]; then
  echo "" >&2
  echo "⛔ Commit blocked: Some files have compliance < 85%" >&2
  echo "   Fix issues or use --no-verify to bypass (not recommended)" >&2
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────────
# EXC Check: Formula Compliance (Exclusion Principle EXC-1 to EXC-4)
# ─────────────────────────────────────────────────────────────────────────
STAGED_FORMULA_REGISTRY=$(git diff --cached --name-only --diff-filter=ACM | grep 'formula-registry.yaml$' || true)

if [ -n "$STAGED_TEX" ] || [ -n "$STAGED_FORMULA_REGISTRY" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Checking Formula Compliance (EXC-1 to EXC-4) ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/check_formula_compliance.py" ]; then
    # Run formula compliance check
    FORMULA_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/check_formula_compliance.py" --summary 2>&1 || true)

    # Check for formulas needing revision
    NEEDS_REVISION=$(echo "$FORMULA_RESULT" | grep "Needs revision:" | grep -oE '[0-9]+' || echo "0")

    if [ "$NEEDS_REVISION" -gt 0 ]; then
      echo "⚠️  FORMULA WARNING: $NEEDS_REVISION formulas need revision per Exclusion Principle" >&2
      echo "   Run: python scripts/check_formula_compliance.py" >&2
      echo "   Reference: Appendix FRM, Axioms EXC-1 to EXC-4" >&2
      # Note: This is a warning, not a blocking error (yet)
      # To make it blocking, uncomment the next line:
      # FAILED=1
    else
      echo "✅ All formulas comply with Exclusion Principle (EXC-1 to EXC-4)" >&2
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# EIP Check: Validate concept-registry.yaml if modified
# ─────────────────────────────────────────────────────────────────────────
STAGED_YAML=$(git diff --cached --name-only --diff-filter=ACM | grep 'concept-registry.yaml$' || true)

if [ -n "$STAGED_YAML" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Checking EIP Compliance ===" >&2

  EIP_SCORE=$(python "$CLAUDE_PROJECT_DIR/scripts/check_eip_compliance.py" 2>/dev/null | grep "Overall Score" | grep -oE '[0-9]+' | head -1 || echo "0")

  if [ "$EIP_SCORE" -lt 85 ]; then
    echo "❌ EIP FAILED: concept-registry.yaml (Score: $EIP_SCORE% < 85%)" >&2
    echo "   Run: python scripts/check_eip_compliance.py --verbose" >&2
    FAILED=1
  else
    echo "✅ EIP PASSED: concept-registry.yaml (Score: $EIP_SCORE%)" >&2
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# REGISTRY ID COLLISION PREVENTION (CAT-XX, MS-XX-XXX, CAS-XXX, PAR-XX-XXX)
# Prevents merge conflicts by detecting duplicate IDs BEFORE commit
# ─────────────────────────────────────────────────────────────────────────
STAGED_THEORY=$(git diff --cached --name-only --diff-filter=ACM | grep 'theory-catalog.yaml$' || true)
STAGED_CASE=$(git diff --cached --name-only --diff-filter=ACM | grep 'case-registry.yaml$' || true)
STAGED_PARAM=$(git diff --cached --name-only --diff-filter=ACM | grep 'parameter-registry.yaml$' || true)

if [ -n "$STAGED_THEORY" ] || [ -n "$STAGED_CASE" ] || [ -n "$STAGED_PARAM" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Checking Registry ID Collisions ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/check_registry_ids.py" ]; then
    # Run collision check
    ID_CHECK=$(python "$CLAUDE_PROJECT_DIR/scripts/check_registry_ids.py" --check 2>&1)
    ID_STATUS=$?

    if [ $ID_STATUS -eq 1 ]; then
      echo "❌ REGISTRY ID COLLISION DETECTED:" >&2
      echo "$ID_CHECK" | grep -E '^\s*(CAT|MS|CAS|PAR):' >&2
      echo "" >&2
      echo "   This prevents merge conflicts in shared registries." >&2
      echo "   Run: python scripts/check_registry_ids.py --status" >&2
      echo "   To get next available ID: python scripts/check_registry_ids.py --next <TYPE>" >&2
      echo "" >&2
      FAILED=1
    else
      echo "✅ All registry IDs are unique (CAT, MS, CAS, PAR)" >&2

      # Show next available IDs for reference
      if [ -n "$STAGED_THEORY" ]; then
        NEXT_CAT=$(python "$CLAUDE_PROJECT_DIR/scripts/check_registry_ids.py" --next CAT 2>/dev/null || true)
        echo "   ℹ️  Next CAT: $NEXT_CAT" >&2
      fi
      if [ -n "$STAGED_CASE" ]; then
        NEXT_CAS=$(python "$CLAUDE_PROJECT_DIR/scripts/check_registry_ids.py" --next CAS 2>/dev/null || true)
        echo "   ℹ️  Next CAS: $NEXT_CAS" >&2
      fi
    fi

    # Option A: Recommend registry_manager for new IDs
    if [ -f "$CLAUDE_PROJECT_DIR/scripts/registry_manager.py" ]; then
      echo "" >&2
      echo "   💡 TIP: Use registry_manager.py for auto-ID generation:" >&2
      echo "      python scripts/registry_manager.py case --next" >&2
      echo "      python scripts/registry_manager.py --status" >&2
    fi

    # Option B: Auto-assign IDs for entries with "id: AUTO"
    if [ -f "$CLAUDE_PROJECT_DIR/scripts/auto_assign_ids.py" ]; then
      AUTO_CHANGES=$(python "$CLAUDE_PROJECT_DIR/scripts/auto_assign_ids.py" --quiet 2>&1 || true)
      if [ -n "$AUTO_CHANGES" ]; then
        echo "" >&2
        echo "=== EBF PreCommit: Auto-Assigning Registry IDs ===" >&2
        python "$CLAUDE_PROJECT_DIR/scripts/auto_assign_ids.py" --apply >&2
        echo "" >&2
        echo "   ✅ AUTO IDs replaced with real IDs" >&2
        echo "   Please review and re-stage the changed files:" >&2
        echo "      git add data/case-registry.yaml data/theory-catalog.yaml data/parameter-registry.yaml" >&2
        echo "" >&2
        # Don't fail - user needs to re-stage
      fi
    fi
  else
    echo "⚠️  Warning: check_registry_ids.py not found - skipping ID check" >&2
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# Chapter-Appendix Mapping: Validate SSOT if chapter/appendix files changed
# ─────────────────────────────────────────────────────────────────────────
STAGED_CHAPTERS=$(git diff --cached --name-only --diff-filter=ACM | grep 'chapters/.*\.tex$' || true)
STAGED_APPENDICES=$(git diff --cached --name-only --diff-filter=ACM | grep 'appendices/.*\.tex$' || true)
STAGED_MAPPING=$(git diff --cached --name-only --diff-filter=ACM | grep 'chapter-appendix-mapping.yaml$' || true)

if [ -n "$STAGED_CHAPTERS" ] || [ -n "$STAGED_APPENDICES" ] || [ -n "$STAGED_MAPPING" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Checking Chapter-Appendix Mapping ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_chapter_mapping.py" ]; then
    MAPPING_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/validate_chapter_mapping.py" --quiet 2>&1 || true)
    MAPPING_STATUS=$?

    if [ $MAPPING_STATUS -eq 1 ]; then
      echo "❌ MAPPING ERROR: chapter-appendix-mapping.yaml has errors" >&2
      echo "$MAPPING_RESULT" | grep -E '^\s*\[ERROR\]' | head -5 >&2
      echo "   Run: python scripts/validate_chapter_mapping.py" >&2
      FAILED=1
    elif [ $MAPPING_STATUS -eq 0 ]; then
      echo "✅ MAPPING PASSED: chapter-appendix-mapping.yaml consistent" >&2
    fi

    # Remind to update YAML if new chapter/appendix added
    NEW_CHAPTERS=$(git diff --cached --name-only --diff-filter=A | grep 'chapters/[0-9].*\.tex$' || true)
    NEW_APPENDICES_ADDED=$(git diff --cached --name-only --diff-filter=A | grep 'appendices/[A-Z].*\.tex$' || true)

    if [ -n "$NEW_CHAPTERS" ] && [ -z "$STAGED_MAPPING" ]; then
      echo "⚠️  REMINDER: New chapter added but chapter-appendix-mapping.yaml not updated" >&2
      echo "   Please add the new chapter to the SSOT YAML file" >&2
    fi

    if [ -n "$NEW_APPENDICES_ADDED" ] && [ -z "$STAGED_MAPPING" ]; then
      echo "⚠️  REMINDER: New appendix added but chapter-appendix-mapping.yaml not updated" >&2
      echo "   Please add the new appendix to the SSOT YAML file" >&2
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# BIB DUPLICATE KEY CHECK: Block commit if bcm_master.bib has duplicate keys
# ─────────────────────────────────────────────────────────────────────────
STAGED_BIB=$(git diff --cached --name-only --diff-filter=ACM | grep 'bcm_master.bib$' || true)

if [ -n "$STAGED_BIB" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: BibTeX Duplicate Key Check ===" >&2

  BIB_FILE="$CLAUDE_PROJECT_DIR/bibliography/bcm_master.bib"
  if [ -f "$BIB_FILE" ]; then
    # Extract all BIB keys: @type{key, → key
    DUPLICATES=$(grep -oE '^@[a-zA-Z]+\{[^,]+,' "$BIB_FILE" | sed 's/^@[a-zA-Z]*{//' | sed 's/,$//' | sort | uniq -d)

    if [ -n "$DUPLICATES" ]; then
      DUP_COUNT=$(echo "$DUPLICATES" | wc -l)
      echo "❌ BLOCKED: $DUP_COUNT duplicate BibTeX key(s) found in bcm_master.bib:" >&2
      echo "" >&2
      echo "$DUPLICATES" | while read -r dup_key; do
        # Show line numbers for each duplicate
        LINE_NUMS=$(grep -n "^@[a-zA-Z]*{${dup_key}," "$BIB_FILE" | cut -d: -f1 | tr '\n' ', ' | sed 's/,$//')
        echo "   ❌ Key: $dup_key (lines: $LINE_NUMS)" >&2
      done
      echo "" >&2
      echo "   Fix: Remove duplicate entries before committing." >&2
      echo "   Use: grep -n '^@.*{KEY,' bibliography/bcm_master.bib" >&2
      exit 1
    else
      TOTAL_KEYS=$(grep -cE '^@[a-zA-Z]+\{[^,]+,' "$BIB_FILE" || echo "0")
      echo "✅ No duplicate BibTeX keys ($TOTAL_KEYS unique entries)" >&2
    fi
  fi

  echo "" >&2
fi

# ─────────────────────────────────────────────────────────────────────────
# AUTO-TAG: BibTeX entries with LIT-* based on author (≥5 papers rule)
# ─────────────────────────────────────────────────────────────────────────
# Re-use STAGED_BIB from above

if [ -n "$STAGED_BIB" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Auto-Tag BibTeX entries (≥5 papers rule) ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/auto_tag_bib_lit.py" ]; then
    # Run auto-tag script with --update flag
    TAG_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/auto_tag_bib_lit.py" --update 2>&1 || true)

    # Check if any entries were tagged
    ENTRIES_TAGGED=$(echo "$TAG_RESULT" | grep "Entries to tag:" | grep -oE '[0-9]+' || echo "0")

    if [ "$ENTRIES_TAGGED" -gt 0 ]; then
      echo "✅ AUTO-TAGGED: $ENTRIES_TAGGED entries with LIT-* based on author" >&2
      # Re-stage the updated bib file
      git add "$CLAUDE_PROJECT_DIR/bibliography/bcm_master.bib" 2>/dev/null || true
    else
      echo "✅ All entries already tagged" >&2
    fi

    echo "" >&2
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# AUTO-SYNC: BibTeX → LIT-Appendix Synchronization
# ─────────────────────────────────────────────────────────────────────────
# Re-use STAGED_BIB from duplicate key check above

if [ -n "$STAGED_BIB" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Auto-Sync BibTeX → LIT-Appendices ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/sync_bib_to_lit.py" ]; then
    # Run sync script with --update flag
    SYNC_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/sync_bib_to_lit.py" --update 2>&1 || true)

    # Check if any files were updated
    PAPERS_ADDED=$(echo "$SYNC_RESULT" | grep "Papers to add:" | grep -oE '[0-9]+' || echo "0")

    if [ "$PAPERS_ADDED" -gt 0 ]; then
      echo "✅ AUTO-SYNCED: $PAPERS_ADDED papers added to LIT-Appendices" >&2

      # Stage all modified LIT-Appendix files
      MODIFIED_LIT=$(git status --porcelain | grep '^ M.*LIT.*\.tex$' | awk '{print $2}' || true)
      for lit_file in $MODIFIED_LIT; do
        git add "$CLAUDE_PROJECT_DIR/$lit_file" 2>/dev/null || true
        echo "   AUTO-STAGED: $lit_file" >&2
      done
    else
      echo "✅ All papers already synced to LIT-Appendices" >&2
    fi

    echo "" >&2
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# AUTO-SYNC: Theory Learning - Paper → Theory Sync
# ─────────────────────────────────────────────────────────────────────────
if [ -n "$STAGED_BIB" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Auto-Sync Papers → Theory Catalog ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/theory_learning.py" ]; then
    # Run paper sync
    THEORY_SYNC=$(python "$CLAUDE_PROJECT_DIR/scripts/theory_learning.py" --sync-papers 2>&1 || true)

    # Check if any links were added
    LINKS_ADDED=$(echo "$THEORY_SYNC" | grep "Synced" | grep -oE '[0-9]+' || echo "0")

    if [ "$LINKS_ADDED" -gt 0 ]; then
      echo "✅ AUTO-SYNCED: $LINKS_ADDED paper-theory links added" >&2
      # Stage the updated theory catalog
      git add "$CLAUDE_PROJECT_DIR/data/theory-catalog.yaml" 2>/dev/null || true
      git add "$CLAUDE_PROJECT_DIR/data/theory-learning-log.yaml" 2>/dev/null || true
      echo "   AUTO-STAGED: data/theory-catalog.yaml" >&2
    else
      echo "✅ All papers already linked to theories" >&2
    fi

    echo "" >&2
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# EIP Check: Warn if new concepts might need EIP
# ─────────────────────────────────────────────────────────────────────────
STAGED_MD=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$' || true)
STAGED_INTERVENTION=$(git diff --cached --name-only --diff-filter=ACM | grep 'interventions/.*\.yaml$' || true)

if [ -n "$STAGED_MD" ] || [ -n "$STAGED_INTERVENTION" ]; then
  # Check for EIP trigger patterns in staged content
  TRIGGER_PATTERNS="Mental.*Budget|Type.*Transform|gamma.*=|γ.*=|new.*mechanism|neue.*Intervention"

  for file in $STAGED_MD $STAGED_INTERVENTION; do
    if [ -f "$CLAUDE_PROJECT_DIR/$file" ]; then
      TRIGGERS=$(git diff --cached "$CLAUDE_PROJECT_DIR/$file" | grep -iE "$TRIGGER_PATTERNS" || true)
      if [ -n "$TRIGGERS" ]; then
        echo "" >&2
        echo "⚠️  EIP REMINDER: Potential new concept detected in $file" >&2
        echo "   Ensure EIP was completed and concept-registry.yaml updated" >&2
        echo "   Trigger patterns found:" >&2
        echo "$TRIGGERS" | head -3 | sed 's/^/     /' >&2
      fi
    fi
  done
fi

if [ "$FAILED" -eq 1 ]; then
  echo "" >&2
  echo "⛔ Commit blocked: EIP compliance check failed" >&2
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────────
# DATA CONSISTENCY: Validate referential integrity, parameters, context
# ─────────────────────────────────────────────────────────────────────────
STAGED_DATA_YAML=$(git diff --cached --name-only --diff-filter=ACM | grep 'data/.*\.yaml$' || true)
STAGED_REGISTRIES=$(echo "$STAGED_DATA_YAML" | grep -E '(model-registry|theory-catalog|case-registry|intervention-registry|concept-registry|parameter-registry)' || true)

if [ -n "$STAGED_REGISTRIES" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Data Consistency Validation ===" >&2

  # 1. Referential Integrity Check
  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_referential_integrity.py" ]; then
    echo "Checking referential integrity..." >&2
    REF_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/validate_referential_integrity.py" 2>&1 || true)
    REF_SCORE=$(echo "$REF_RESULT" | grep "Score:" | grep -oE '[0-9.]+' | head -1 || echo "100")
    REF_SCORE_INT=${REF_SCORE%.*}

    if [ "$REF_SCORE_INT" -lt 85 ]; then
      echo "❌ REFERENTIAL INTEGRITY: Score $REF_SCORE% < 85%" >&2
      echo "   Critical errors found in database references" >&2
      echo "   Run: python scripts/validate_referential_integrity.py --verbose" >&2
      FAILED=1
    else
      CRITICAL=$(echo "$REF_RESULT" | grep "Critical Errors:" | grep -oE '[0-9]+' || echo "0")
      echo "✅ REFERENTIAL INTEGRITY: Score $REF_SCORE% (${CRITICAL} critical errors)" >&2
    fi
  fi

  # 2. Parameter Consistency Check
  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_parameter_consistency.py" ]; then
    echo "Checking parameter consistency..." >&2
    PARAM_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/validate_parameter_consistency.py" 2>&1 || true)
    PARAM_SCORE=$(echo "$PARAM_RESULT" | grep "Score:" | grep -oE '[0-9.]+' | head -1 || echo "100")
    PARAM_SCORE_INT=${PARAM_SCORE%.*}

    if [ "$PARAM_SCORE_INT" -lt 85 ]; then
      echo "⚠️  PARAMETER CONSISTENCY: Score $PARAM_SCORE% < 85%" >&2
      echo "   Run: python scripts/validate_parameter_consistency.py --verbose" >&2
      # Warning only, not blocking (parameters may legitimately vary by context)
    else
      echo "✅ PARAMETER CONSISTENCY: Score $PARAM_SCORE%" >&2
    fi
  fi

  # 3. Context Consistency Check
  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_context_consistency.py" ]; then
    echo "Checking context consistency..." >&2
    CTX_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/validate_context_consistency.py" 2>&1 || true)
    CTX_SCORE=$(echo "$CTX_RESULT" | grep "Score:" | grep -oE '[0-9.]+' | head -1 || echo "100")
    CTX_SCORE_INT=${CTX_SCORE%.*}

    if [ "$CTX_SCORE_INT" -lt 85 ]; then
      echo "⚠️  CONTEXT CONSISTENCY: Score $CTX_SCORE% < 85%" >&2
      echo "   Run: python scripts/validate_context_consistency.py --verbose" >&2
      # Warning only, not blocking (context analysis may be incremental)
    else
      echo "✅ CONTEXT CONSISTENCY: Score $CTX_SCORE%" >&2
    fi
  fi

  echo "" >&2
fi

if [ "$FAILED" -eq 1 ]; then
  echo "" >&2
  echo "⛔ Commit blocked: Data consistency check failed" >&2
  exit 1
fi

# ─────────────────────────────────────────────────────────────────────────
# LEAD-ID UNIQUENESS: Auto-fix duplicate LEAD-IDs
# ─────────────────────────────────────────────────────────────────────────
STAGED_LEAD_DB=$(git diff --cached --name-only --diff-filter=ACM | grep 'lead-database.yaml$' || true)

if [ -n "$STAGED_LEAD_DB" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Checking LEAD-ID Uniqueness ===" >&2

  LEAD_DB="$CLAUDE_PROJECT_DIR/data/sales/lead-database.yaml"
  LEAD_SCRIPT="$CLAUDE_PROJECT_DIR/scripts/get_next_lead_id.py"

  if [ -f "$LEAD_DB" ]; then
    # Extract all LEAD-IDs and check for duplicates
    DUPLICATES=$(grep -E "^  - id: LEAD-[0-9]+" "$LEAD_DB" | sort | uniq -d || true)

    if [ -n "$DUPLICATES" ]; then
      echo "⚠️  LEAD-ID CONFLICT: Duplicate IDs found - AUTO-FIXING..." >&2

      # Process each duplicate
      echo "$DUPLICATES" | while read -r line; do
        DUP_ID=$(echo "$line" | sed 's/.*id: //' | tr -d ' ')

        # Find line numbers of all occurrences
        LINE_NUMBERS=$(grep -n "^  - id: $DUP_ID" "$LEAD_DB" | cut -d: -f1)

        # Skip the first occurrence (keep it), fix the rest
        FIRST=true
        for LINE_NUM in $LINE_NUMBERS; do
          if [ "$FIRST" = true ]; then
            FIRST=false
            echo "   Keeping $DUP_ID at line $LINE_NUM (original)" >&2
          else
            # Get new ID via script
            if [ -f "$LEAD_SCRIPT" ]; then
              NEW_ID=$(python3 "$LEAD_SCRIPT" 2>/dev/null)
              echo "   🔄 Renaming $DUP_ID → $NEW_ID at line $LINE_NUM (auto-fix)" >&2

              # Replace only at that specific line
              sed -i "${LINE_NUM}s/id: $DUP_ID/id: $NEW_ID  # Auto-fixed from $DUP_ID/" "$LEAD_DB"
            else
              echo "   ❌ Script not found: $LEAD_SCRIPT" >&2
              FAILED=1
            fi
          fi
        done
      done

      # Re-stage the fixed file
      git add "$LEAD_DB"
      echo "   ✅ Fixed and re-staged lead-database.yaml" >&2
    else
      echo "✅ All LEAD-IDs are unique" >&2
    fi

    # Verify next_lead_id is higher than all existing IDs
    HIGHEST_ID=$(grep -E "^  - id: LEAD-[0-9]+" "$LEAD_DB" | sed 's/.*LEAD-//' | sed 's/ .*//' | sort -n | tail -1 || echo "0")
    NEXT_ID=$(grep 'next_lead_id:' "$LEAD_DB" | head -1 | grep -oE '[0-9]+' || echo "0")

    if [ "$NEXT_ID" -le "$HIGHEST_ID" ]; then
      echo "⚠️  Fixing next_lead_id: $NEXT_ID → $((HIGHEST_ID + 1))" >&2
      sed -i "s/next_lead_id: $NEXT_ID/next_lead_id: $((HIGHEST_ID + 1))/" "$LEAD_DB"
      git add "$LEAD_DB"
    fi
  fi

  echo "" >&2
fi

# ─────────────────────────────────────────────────────────────────────────
# LEARNINGS REMINDER: Check if Report Formatter changed without learnings
# ─────────────────────────────────────────────────────────────────────────
STAGED_FORMAT_REPORT=$(git diff --cached --name-only --diff-filter=ACM | grep -E '(scripts/format_report\.py|templates/fehradvice-)' || true)
STAGED_LEARNINGS=$(git diff --cached --name-only --diff-filter=ACM | grep 'report-formatter-learnings.yaml$' || true)

if [ -n "$STAGED_FORMAT_REPORT" ] && [ -z "$STAGED_LEARNINGS" ]; then
  echo "" >&2
  echo "┌─────────────────────────────────────────────────────────────────────────┐" >&2
  echo "│  💡 LEARNINGS REMINDER                                                  │" >&2
  echo "├─────────────────────────────────────────────────────────────────────────┤" >&2
  echo "│  Du hast Änderungen am Report-Formatter gemacht:                        │" >&2
  for f in $STAGED_FORMAT_REPORT; do
    printf "│    • %-63s │\n" "$f" >&2
  done
  echo "│                                                                         │" >&2
  echo "│  Vergiss nicht, relevante Learnings zu dokumentieren!                   │" >&2
  echo "│                                                                         │" >&2
  echo "│  → python scripts/format_report.py --add-learning                       │" >&2
  echo "│  → Oder: data/report-formatter-learnings.yaml manuell bearbeiten        │" >&2
  echo "└─────────────────────────────────────────────────────────────────────────┘" >&2
  echo "" >&2
  # Note: This is a reminder, not a blocking error
  # User can proceed without adding learnings if they choose
fi

# ─────────────────────────────────────────────────────────────────────────
# PAPER INTEGRATION: Validate 12-step PIP workflow completeness
# ─────────────────────────────────────────────────────────────────────────
STAGED_PIP=$(git diff --cached --name-only --diff-filter=ACM | grep 'paper-intake/.*\.yaml$' || true)
STAGED_PAPER_REF=$(git diff --cached --name-only --diff-filter=ACM | grep 'paper-references/PAP-.*\.yaml$' || true)
STAGED_FULL_TEXT=$(git diff --cached --name-only --diff-filter=ACM | grep 'papers/evaluated/integrated/PAP-.*\.txt$' || true)

if [ -n "$STAGED_PIP" ] || [ -n "$STAGED_PAPER_REF" ] || [ -n "$STAGED_FULL_TEXT" ] || [ -n "$STAGED_BIB" ]; then
  echo "" >&2
  echo "=== EBF PreCommit: Paper Integration Validation (12-Step PIP) ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_paper_integration.py" ]; then
    # Extract paper IDs from staged files
    PAPER_IDS=""

    # From PIP files
    for pip_file in $STAGED_PIP; do
      if [ -f "$CLAUDE_PROJECT_DIR/$pip_file" ]; then
        PID=$(grep "^paper_id:" "$CLAUDE_PROJECT_DIR/$pip_file" | sed 's/paper_id: *"\?\([^"]*\)"\?/\1/' | tr -d ' ' || true)
        if [ -n "$PID" ]; then
          PAPER_IDS="$PAPER_IDS $PID"
        fi
      fi
    done

    # From paper-references
    for ref_file in $STAGED_PAPER_REF; do
      PID=$(basename "$ref_file" .yaml)
      PAPER_IDS="$PAPER_IDS $PID"
    done

    # From full text files
    for txt_file in $STAGED_FULL_TEXT; do
      PID=$(basename "$txt_file" .txt)
      PAPER_IDS="$PAPER_IDS $PID"
    done

    # Remove duplicates
    PAPER_IDS=$(echo "$PAPER_IDS" | tr ' ' '\n' | sort -u | tr '\n' ' ')

    # Validate each paper
    INCOMPLETE_PAPERS=""
    for paper_id in $PAPER_IDS; do
      if [ -n "$paper_id" ] && [ "$paper_id" != "template" ]; then
        echo "Validating: $paper_id" >&2
        RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/validate_paper_integration.py" "$paper_id" 2>&1 || true)

        if echo "$RESULT" | grep -q "INCOMPLETE"; then
          INCOMPLETE_PAPERS="$INCOMPLETE_PAPERS $paper_id"
          SCORE=$(echo "$RESULT" | grep "Score:" | head -1 || echo "Score: ?/?")
          echo "❌ INCOMPLETE: $paper_id ($SCORE)" >&2

          # Show what's missing
          MISSING=$(echo "$RESULT" | grep "Missing components:" -A 10 | grep "^    -" | head -5 || true)
          if [ -n "$MISSING" ]; then
            echo "$MISSING" >&2
          fi
        else
          SCORE=$(echo "$RESULT" | grep "Score:" | head -1 || echo "")
          echo "✅ COMPLETE: $paper_id ($SCORE)" >&2
        fi
      fi
    done

    if [ -n "$INCOMPLETE_PAPERS" ]; then
      echo "" >&2
      echo "📋 PAPER INTEGRATION QUEUE: Adding incomplete papers" >&2

      # Add each incomplete paper to the queue
      for paper_id in $INCOMPLETE_PAPERS; do
        if [ -n "$paper_id" ]; then
          # Add to queue using paper_queue_manager.py
          QUEUE_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/paper_queue_manager.py" --add "$paper_id" 2>&1 || true)
          echo "   → $paper_id: Added to queue" >&2
        fi
      done

      echo "" >&2
      echo "   ℹ️  Papers will be completed automatically in future sessions." >&2
      echo "   ℹ️  At least 1 paper per session will be processed." >&2
      echo "" >&2
      echo "   Queue status: python scripts/paper_queue_manager.py --status" >&2
      echo "" >&2
      # Note: Not blocking - papers will be completed asynchronously
    fi

    echo "" >&2
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# PAPER INTEGRATION: Check for new BibTeX entries without PIP
# ─────────────────────────────────────────────────────────────────────────
if [ -n "$STAGED_BIB" ]; then
  echo "=== EBF PreCommit: Checking BibTeX entries have PIP ===" >&2

  # Get newly added entries (lines starting with @)
  NEW_ENTRIES=$(git diff --cached "$CLAUDE_PROJECT_DIR/bibliography/bcm_master.bib" | grep "^+@" | grep -v "^+++" || true)

  if [ -n "$NEW_ENTRIES" ]; then
    # Extract entry keys
    for entry in $NEW_ENTRIES; do
      KEY=$(echo "$entry" | sed 's/.*{\([^,]*\),.*/\1/' || true)
      if [ -n "$KEY" ]; then
        # Check if PIP exists for this entry
        PIP_EXISTS=$(find "$CLAUDE_PROJECT_DIR/data/paper-intake" -name "*.yaml" -exec grep -l "paper_id:.*PAP-$KEY" {} \; 2>/dev/null | head -1 || true)

        if [ -z "$PIP_EXISTS" ]; then
          # Check if pip_id field exists in the BibTeX entry
          HAS_PIP_FIELD=$(git diff --cached "$CLAUDE_PROJECT_DIR/bibliography/bcm_master.bib" | grep -A 20 "^+@.*{$KEY," | grep "pip_id" || true)

          if [ -z "$HAS_PIP_FIELD" ]; then
            echo "⚠️  NEW BIBTEX: $KEY added without PIP workflow" >&2
            echo "   Consider using /integrate-paper for proper integration" >&2
          fi
        fi
      fi
    done
  fi

  echo "" >&2
fi

# ─────────────────────────────────────────────────────────────────────────
# FIX 7: PAPER SSOT CONSISTENCY CHECK
# Ensures every BibTeX entry has a matching YAML in paper-references/
# ─────────────────────────────────────────────────────────────────────────
if [ -n "$STAGED_BIB" ]; then
  if [ -f "$CLAUDE_PROJECT_DIR/scripts/check_paper_consistency.py" ]; then
    echo "=== EBF PreCommit: Paper SSOT Consistency ===" >&2
    CONSISTENCY_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/check_paper_consistency.py" --summary 2>&1 || true)
    echo "   $CONSISTENCY_RESULT" >&2

    if echo "$CONSISTENCY_RESULT" | grep -q "\[GAPS\]"; then
      GAP_COUNT=$(echo "$CONSISTENCY_RESULT" | grep -oP 'BIB→YAML gaps: \K[0-9]+' || echo "0")
      echo "" >&2
      echo "⚠️  $GAP_COUNT BibTeX-Einträge ohne YAML detected." >&2
      echo "   Run: python scripts/check_paper_consistency.py" >&2
      echo "   Fix: Generate missing YAMLs or add to paper-integration-queue" >&2
      echo "" >&2
      # Warning only - don't block (new papers may be added incrementally)
    fi
    echo "" >&2
  fi
fi

# FIX 6: BIBTEX ↔ YAML CONSISTENCY CHECK (Level Gate)
# Prevents claiming Level 5 without meeting requirements
# ─────────────────────────────────────────────────────────────────────────
if [ -n "$STAGED_BIB" ] || [ -n "$STAGED_YAML" ]; then
  echo "=== EBF PreCommit: BibTeX ↔ YAML Consistency Check ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_bibtex_yaml_consistency.py" ]; then
    # Check for papers claiming Level 4+ in staged files
    HIGH_LEVEL_PAPERS=""

    if [ -n "$STAGED_BIB" ]; then
      # Find papers claiming integration_level >= 4
      HIGH_LEVEL_PAPERS=$(git diff --cached "$CLAUDE_PROJECT_DIR/bibliography/bcm_master.bib" | \
        grep -B 5 "integration_level.*=.*{[45]}" | \
        grep "@.*{PAP-" | \
        sed 's/.*{PAP-\([^,]*\),.*/PAP-\1/' || true)
    fi

    if [ -n "$HIGH_LEVEL_PAPERS" ]; then
      echo "📊 Validating high-level paper claims..." >&2

      for paper in $HIGH_LEVEL_PAPERS; do
        RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/validate_bibtex_yaml_consistency.py" "$paper" --json 2>&1 || true)

        # Check if result contains "is_consistent": false
        if echo "$RESULT" | grep -q '"is_consistent": false'; then
          echo "" >&2
          echo "❌ LEVEL GATE FAILED: $paper" >&2
          echo "   Paper claims high integration level but doesn't meet requirements." >&2
          echo "   Run: python scripts/validate_bibtex_yaml_consistency.py $paper" >&2
          echo "" >&2

          # Extract missing components
          MISSING=$(echo "$RESULT" | grep -o '"missing_components": \[[^]]*\]' | head -1 || true)
          if [ -n "$MISSING" ]; then
            echo "   Missing: $MISSING" >&2
          fi

          echo "" >&2
          echo "   OPTIONS:" >&2
          echo "   1. Complete the missing components" >&2
          echo "   2. Downgrade integration_level in BibTeX" >&2
          echo "   3. Use --no-verify to skip (NOT RECOMMENDED)" >&2
          echo "" >&2

          # Block commit for Level 5 overclaims
          CLAIMED=$(echo "$RESULT" | grep -o '"claimed_level": [0-9]' | grep -o '[0-9]' || echo "0")
          ACTUAL=$(echo "$RESULT" | grep -o '"calculated_level": [0-9]' | grep -o '[0-9]' || echo "0")

          if [ "$CLAIMED" = "5" ] && [ "$ACTUAL" -lt "5" ]; then
            echo "🚫 COMMIT BLOCKED: Level 5 (FOUNDATIONAL) claims require all 13 components" >&2
            exit 1
          fi
        fi
      done
    fi
  fi

  echo "" >&2
fi

# ─────────────────────────────────────────────────────────────────────────
# PAR-4 VALIDATION: Referential Integrity for γ parameters
# ─────────────────────────────────────────────────────────────────────────
STAGED_MODEL_REGISTRY=$(git diff --cached --name-only --diff-filter=ACM | grep 'model-registry.yaml$' || true)

if [ -n "$STAGED_MODEL_REGISTRY" ]; then
  echo "=== EBF PreCommit: Checking PAR-4 (Referential Integrity) ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_parameter_refs.py" ]; then
    if ! python "$CLAUDE_PROJECT_DIR/scripts/validate_parameter_refs.py" 2>&1 | sed 's/^/   /' >&2; then
      echo "" >&2
      echo "❌ PAR-4 VIOLATION: Model contains γ values without parameter_ref" >&2
      echo "   Fix: Add 'parameter_ref: PAR-COMP-xxx' or 'domain_specific: true'" >&2
      echo "   See: Appendix BBB, Axiom PAR-4" >&2
      echo "" >&2
      exit 1
    fi
  else
    echo "⚠️  Warning: validate_parameter_refs.py not found, skipping PAR-4 check" >&2
  fi

  echo "" >&2
fi

# ─────────────────────────────────────────────────────────────────────────
# FIX 2: FULL-TEXT SSOT ENFORCEMENT
# Ensures full-texts are in data/paper-texts/, not legacy locations
# ─────────────────────────────────────────────────────────────────────────
if [ -f "$CLAUDE_PROJECT_DIR/scripts/enforce_fulltext_ssot.py" ]; then
  # Only run if paper-related files are staged
  STAGED_PAPERS=$(git diff --cached --name-only | grep -E "(papers/|paper-texts/|paper-references/)" || true)

  if [ -n "$STAGED_PAPERS" ]; then
    echo "=== EBF PreCommit: Full-Text SSOT Check ===" >&2

    SSOT_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/enforce_fulltext_ssot.py" --check 2>&1 || true)

    if echo "$SSOT_RESULT" | grep -q "NOT COMPLIANT"; then
      echo "⚠️  Full-text SSOT issues detected:" >&2
      echo "$SSOT_RESULT" | grep -E "(Legacy Files|wrong path|wrong flag)" >&2
      echo "" >&2
      echo "   Run: python scripts/enforce_fulltext_ssot.py --all" >&2
      echo "" >&2
      # Warning only, don't block
    fi

    echo "" >&2
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# SPÖ DELIVERY COMPLETENESS: Check all 4 Pflicht-Deliverables per ANF
# Triggers when SPÖ files are committed
# ─────────────────────────────────────────────────────────────────────────
STAGED_SPO=$(git diff --cached --name-only --diff-filter=ACM | grep 'data/customers/spo/' || true)

if [ -n "$STAGED_SPO" ]; then
  echo "" >&2
  echo "=== SPÖ PreCommit: Delivery Completeness Check ===" >&2

  if [ -f "$CLAUDE_PROJECT_DIR/scripts/validate_spo_deliveries.py" ]; then
    DELIVERY_RESULT=$(python "$CLAUDE_PROJECT_DIR/scripts/validate_spo_deliveries.py" --strict 2>&1)
    DELIVERY_STATUS=$?

    if [ $DELIVERY_STATUS -eq 1 ]; then
      echo "$DELIVERY_RESULT" | grep -E '(KRITISCH|fehlt)' >&2
      echo "" >&2
      echo "⚠️  SPÖ DELIVERY WARNING: Abgeschlossene ANFs mit fehlenden Deliverables!" >&2
      echo "   Standard: REPORT + WORDING + INTERVIEW + WÄHLERBEFRAGUNG" >&2
      echo "   Run: python scripts/validate_spo_deliveries.py --verbose" >&2
      echo "" >&2
      # Warning only - don't block other SPÖ work
      # To make blocking: uncomment next line
      # FAILED=1
    else
      echo "✅ Alle abgeschlossenen ANFs haben vollständige Deliverables (4/4)" >&2
    fi
  fi

  echo "" >&2
fi

echo "=== All compliance checks passed ===" >&2
exit 0
