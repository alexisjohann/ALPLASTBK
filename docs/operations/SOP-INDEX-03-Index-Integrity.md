# SOP-INDEX-03: Appendix Index Integrity & Validation

> **Purpose:** Ensure appendix index remains consistent with actual files and cross-references
> **Version:** 1.0
> **Date:** 2026-01-15
> **Owner:** Index Integrity Team
> **Review Cycle:** Every 100 appendices added
> **Related:** SOP-SCRIPT-01, SOP-APPEND-02, SOP-RECOVERY-04

---

## 1. Scope

The appendix index (`appendices/00_appendix_index.tex`) is the **Single Source of Truth** for:
- All active appendix codes
- Appendix categories and metadata
- Reading paths and dependencies
- Cross-reference mapping

This SOP ensures index integrity and prevents the cascading bugs that occurred when:
- Files existed but weren't in index (VVV orphans)
- Index entries existed but files were missing
- Codes were duplicated across categories
- Cross-references broke

---

## 2. The Index Structure (4 Critical Tables)

The index contains 4 interconnected tables that MUST stay synchronized:

### Table 1: Appendix Summary (Main registry)

```latex
\begin{tabular}{|l|l|l|l|}
\hline
\textbf{Code} & \textbf{Category} & \textbf{Title} & \textbf{Lines} \\
\hline
AAA & CORE-WHO & The Welfare Hierarchy & 450 \\
C & CORE-WHAT & The FEPSDE Utility Matrix & 320 \\
...
\hline
\end{tabular}
```

**What this table does:**
- Lists every active appendix
- Maps code → category → title
- Indicates size (lines)

### Table 2: Status & Progress (Metadata)

```latex
\begin{tabular}{|l|l|l|l|}
\hline
\textbf{Code} & \textbf{Title} & \textbf{Category} & \textbf{Status} \\
\hline
AAA & The Welfare Hierarchy & CORE & 100\% Complete \\
C & The FEPSDE Matrix & CORE & 100\% Complete \\
...
\hline
\end{tabular}
```

**What this table does:**
- Shows completion status (100%, 80%, DRAFT, DEPRECATED)
- Helps identify work-in-progress
- Flags deprecated or archived appendices

### Table 3: Category Counts

```latex
\textbf{CORE-} & ... & 9 Appendices \\
\textbf{FORMAL-} & ... & 11 Appendices \\
\textbf{DOMAIN-} & ... & 17 Appendices \\
...
\textbf{TOTAL} & ... & 93 Appendices \\
```

**What this table does:**
- Counts appendices per category
- Used for quick validation ("Should be 10 CORE, found N")
- Helps detect missing or extra entries

### Table 4: Reading Paths (Cross-references)

```latex
\begin{tabular}{|l|l|l|l|}
\hline
\textbf{Code} & \textbf{Category} & \textbf{Core Reference} & \textbf{Chapter Links} \\
\hline
AAA & CORE-WHO & ... & Ch. 5, 10, 14 \\
C & CORE-WHAT & ... & Ch. 3, 9, 15 \\
...
\hline
\end{tabular}
```

**What this table does:**
- Maps appendices to chapters
- Shows which chapters use which appendices
- Enables bidirectional linking

---

## 3. Pre-Modification Validation

**BEFORE any script modifies the index, run:**

```bash
#!/bin/bash
# Validate index before modifications

echo "🔍 PRE-MODIFICATION INDEX VALIDATION"
echo "===================================="

# 1. Count entries
echo ""
echo "1. Counting entries..."
TOTAL_TABLE1=$(grep -E "^[A-Z]+ & " appendices/00_appendix_index.tex | wc -l)
TOTAL_TABLE2=$(grep -E "^[A-Z]+ & " appendices/00_appendix_index.tex | wc -l)

if [ $TOTAL_TABLE1 -ne $TOTAL_TABLE2 ]; then
    echo "❌ MISMATCH: Table 1 has $TOTAL_TABLE1 entries, Table 2 has $TOTAL_TABLE2 entries"
    exit 1
fi
echo "   ✅ Both tables have $TOTAL_TABLE1 entries (consistent)"

# 2. Check file-index sync
echo ""
echo "2. Checking file-index synchronization..."

FILES_NOT_IN_INDEX=0
for file in appendices/*_*.tex; do
    CODE=$(basename "$file" | sed 's/_.*//g')
    if ! grep -q "^$CODE " appendices/00_appendix_index.tex; then
        echo "   ❌ File $file not in index!"
        ((FILES_NOT_IN_INDEX++))
    fi
done

if [ $FILES_NOT_IN_INDEX -gt 0 ]; then
    echo "❌ Found $FILES_NOT_IN_INDEX files not in index"
    exit 1
fi
echo "   ✅ All files in index (0 orphans)"

# 3. Check category counts
echo ""
echo "3. Validating category counts..."

CORE_INDEX=$(grep -E "^CORE-" appendices/00_appendix_index.tex | grep -oE '[0-9]+' | tail -1)
CORE_ACTUAL=$(grep "^C\|^AAA\|^B\|^V\|^BBB\|^AU\|^AV\|^AW\|^HI" appendices/00_appendix_index.tex | wc -l)

if [ $CORE_INDEX -ne $CORE_ACTUAL ]; then
    echo "   ⚠️  CORE count in index: $CORE_INDEX, actual: $CORE_ACTUAL"
fi
echo "   ✅ Category counts verified"

# 4. Check for duplicate codes
echo ""
echo "4. Checking for duplicate codes..."

DUPLICATES=$(cut -d'&' -f1 appendices/00_appendix_index.tex | sed 's/ //g' | sort | uniq -d)

if [ -n "$DUPLICATES" ]; then
    echo "   ❌ DUPLICATE CODES FOUND: $DUPLICATES"
    exit 1
fi
echo "   ✅ No duplicate codes"

echo ""
echo "===================================="
echo "✅ PRE-MODIFICATION VALIDATION PASSED"
echo "Safe to proceed with modifications"
```

---

## 4. The 4-Location Update Pattern

When ANY appendix is added/renamed/removed, 4 locations in the index MUST be updated:

```latex
% LOCATION 1: Main Summary Table (line ~430)
\begin{tabular}{...}
AAA & CORE-WHO & The Welfare Hierarchy & 450 \\
[YOUR_NEW_ENTRY_HERE]  ← ADD HERE
\end{tabular}

% LOCATION 2: Category Count Summary (line ~68)
\textbf{CORE-} & Core Theory & 9 & ← UPDATE COUNT

% LOCATION 3: Status & Progress Table (line ~612)
AAA & The Welfare Hierarchy & CORE & 100\% \\
[YOUR_NEW_ENTRY_HERE]  ← ADD HERE

% LOCATION 4: Reading Paths (line ~898)
AAA & CORE-WHO & ... & Ch. 5, 10, 14 \\
[YOUR_NEW_ENTRY_HERE]  ← ADD HERE
```

### 4.1 The Bug: register_lit_appendices.py Updated Location 1 & 2 & 3, But:

```python
# ❌ BUG in register_lit_appendices.py:

# Updated Location 1 ✅
insert_point_2 = content.find("Q & LIT-BLOOM")
content = content[:end_of_line] + insertion_text + content[end_of_line:]

# Updated Location 2 ✅
old_count = r"\textbf{LIT-} & Literature & 16 &"
content = content.replace(old_count, new_count)

# Updated Location 3 ✅
insert_point_3 = content.find("Q & LIT-BLOOM: Nick Bloom")
content = content[:end_of_line_3] + insertion_text_3 + content[end_of_line_3:]

# FORGOT Location 4! ❌
# (No code to update reading paths)

# RESULT:
# - Index is inconsistent
# - Reading paths broken
# - Downstream cross-refs fail
```

---

## 5. Safe Index Modification Protocol

**INSTEAD of `register_lit_appendices.py`, use this:**

```python
#!/usr/bin/env python3
"""
Safe Appendix Registration with 4-Location Validation.
"""

import re
from pathlib import Path
from datetime import datetime

class AppendixIndexManager:
    """Safely manage appendix index with 4-location sync."""

    def __init__(self, index_path="appendices/00_appendix_index.tex"):
        self.index_path = Path(index_path)
        self.backup_path = self._create_backup()
        self.content = self._load_content()

    def _create_backup(self):
        """Create timestamped backup before ANY modifications."""
        backup = self.index_path.with_stem(
            f"{self.index_path.stem}.BACKUP.{datetime.now().isoformat()}"
        )
        import shutil
        shutil.copy(self.index_path, backup)
        print(f"✅ Backup created: {backup}")
        return backup

    def _load_content(self):
        """Load index file."""
        with open(self.index_path) as f:
            return f.read()

    def add_appendix(self, code, category, title, lines, chapter_refs):
        """Add single appendix with all 4 locations updated."""

        print(f"\nAdding: {code} {category}: {title}")

        # Validate preconditions
        if self._code_exists(code):
            raise ValueError(f"Code {code} already exists!")
        if not self._is_valid_code(code):
            raise ValueError(f"Invalid code format: {code}")

        # Location 1: Main Summary Table
        self._update_location_1(code, category, title, lines)
        print(f"  ✅ Location 1: Summary table")

        # Location 2: Category Counts
        self._update_location_2(category)
        print(f"  ✅ Location 2: Category counts")

        # Location 3: Status & Progress Table
        self._update_location_3(code, title, category)
        print(f"  ✅ Location 3: Status table")

        # Location 4: Reading Paths
        self._update_location_4(code, category, chapter_refs)
        print(f"  ✅ Location 4: Reading paths")

        # Validate all 4 locations updated
        self._validate_all_locations()

    def _update_location_1(self, code, category, title, lines):
        """Update main summary table (~line 430)."""
        # Find insertion point (after last entry in table)
        insertion_point = self.content.rfind(r"\end{tabular}")
        if insertion_point == -1:
            raise ValueError("Could not find end of summary table!")

        new_entry = f"{code} & {category} & {title} & {lines} \\\\\n"

        # Insert before \end{tabular}
        self.content = (
            self.content[:insertion_point] +
            new_entry +
            self.content[insertion_point:]
        )

    def _update_location_2(self, category):
        """Update category count (~line 68)."""
        # Find category line: \textbf{CORE-} & ... & 9 &
        category_prefix = category.split('-')[0] + '-'

        pattern = rf"(\textbf{{{re.escape(category_prefix)}\}}\s*&[^&]*&\s*)(\d+)(\s*&)"
        match = re.search(pattern, self.content)

        if not match:
            raise ValueError(f"Could not find category {category_prefix} in counts table!")

        old_count = int(match.group(2))
        new_count = old_count + 1

        self.content = re.sub(pattern, rf"\g<1>{new_count}\g<3>", self.content, count=1)

    def _update_location_3(self, code, title, category):
        """Update status & progress table (~line 612)."""
        insertion_point = self.content.rfind(r"\end{tabular}", 0, self.content.rfind(r"\end{tabular}"))

        new_entry = f"{code} & {title} & {category} & 100\\% \\\\\n"

        self.content = (
            self.content[:insertion_point] +
            new_entry +
            self.content[insertion_point:]
        )

    def _update_location_4(self, code, category, chapter_refs):
        """Update reading paths (~line 898)."""
        insertion_point = self.content.rfind(r"\end{tabular}")

        # Format chapter references
        chapters = ", ".join([f"Ch. {c}" for c in chapter_refs])
        new_entry = f"{code} & {category} & ... & {chapters} \\\\\n"

        self.content = (
            self.content[:insertion_point] +
            new_entry +
            self.content[insertion_point:]
        )

    def _code_exists(self, code):
        """Check if code already in index."""
        return re.search(rf"^{re.escape(code)}\s+&", self.content, re.MULTILINE) is not None

    def _is_valid_code(self, code):
        """Validate code format."""
        return re.match(r"^[A-Z]{2,3}$", code) is not None

    def _validate_all_locations(self):
        """Ensure all 4 locations are consistent."""
        # Count entries in each location
        loc1_count = len(re.findall(r"[A-Z]{2,3}\s+&\s+\w+-\w+", self.content))
        loc2_total = sum(int(m) for m in re.findall(r"&\s+(\d+)\s+&\s*\\\\", self.content))

        if loc1_count != loc2_total:
            raise ValueError(
                f"Location mismatch: {loc1_count} entries but counts sum to {loc2_total}"
            )

        print(f"  ✅ 4-location validation passed")

    def save(self):
        """Write modified content back to file."""
        with open(self.index_path, 'w') as f:
            f.write(self.content)
        print(f"\n✅ Index saved: {self.index_path}")

    def rollback(self):
        """Restore from backup."""
        import shutil
        shutil.copy(self.backup_path, self.index_path)
        print(f"\n✅ Rolled back to: {self.backup_path}")

# Usage:
manager = AppendixIndexManager()

# Add multiple appendices (all 4 locations updated for each!)
manager.add_appendix(
    code="BF",
    category="DOMAIN-GENERALIZATION",
    title="Cross-System Elite Selection Learning",
    lines=468,
    chapter_refs=[14, 15]
)

manager.add_appendix(
    code="BG",
    category="FORMAL-LEARNING",
    title="Mathematical Theorems for Cross-System Generalization",
    lines=2500,
    chapter_refs=[9, 10, 11]
)

# Validate all 4 locations
manager._validate_all_locations()

# Save (or rollback if validation failed)
manager.save()
```

---

## 6. Post-Modification Validation

**AFTER any index modification, run:**

```bash
#!/bin/bash
# Post-modification validation

echo "🔍 POST-MODIFICATION INDEX VALIDATION"
echo "====================================="

# 1. File-Index Sync
echo "1. File-Index Synchronization:"
ORPHANED_FILES=0
for file in appendices/*_*.tex; do
    CODE=$(basename "$file" | sed 's/_.*//g')
    if ! grep -q "^$CODE " appendices/00_appendix_index.tex; then
        echo "   ⚠️  Orphaned file: $file"
        ((ORPHANED_FILES++))
    fi
done

if [ $ORPHANED_FILES -eq 0 ]; then
    echo "   ✅ All files indexed (0 orphans)"
else
    echo "   ❌ Found $ORPHANED_FILES orphaned files"
    exit 1
fi

# 2. Cross-Reference Validity
echo ""
echo "2. Cross-Reference Validity:"
BROKEN_REFS=0

while IFS= read -r line; do
    # Extract referenced codes
    if [[ $line =~ \[sec:app:([A-Z]+)\] ]]; then
        REF_CODE="${BASH_REMATCH[1]}"
        if ! grep -q "^$REF_CODE " appendices/00_appendix_index.tex; then
            echo "   ⚠️  Broken reference: app:$REF_CODE"
            ((BROKEN_REFS++))
        fi
    fi
done < <(grep -h "\\ref{" appendices/*.tex chapters/*.tex)

if [ $BROKEN_REFS -eq 0 ]; then
    echo "   ✅ All cross-references valid"
else
    echo "   ⚠️  Found $BROKEN_REFS broken references"
fi

# 3. Index Integrity
echo ""
echo "3. Index Integrity:"

DUPLICATE_CODES=$(cut -d'&' -f1 appendices/00_appendix_index.tex | sed 's/ //g' | sort | uniq -d)

if [ -n "$DUPLICATE_CODES" ]; then
    echo "   ❌ DUPLICATE CODES: $DUPLICATE_CODES"
    exit 1
else
    echo "   ✅ No duplicate codes"
fi

echo ""
echo "====================================="
echo "✅ POST-MODIFICATION VALIDATION PASSED"
```

---

## 7. Quarterly Index Audit

**Run every 3 months:**

```bash
#!/bin/bash
# Quarterly appendix index audit

AUDIT_DATE=$(date +%Y-%m-%d)
AUDIT_LOG="quality/audits/index_audit_$AUDIT_DATE.log"

echo "📋 QUARTERLY APPENDIX INDEX AUDIT" | tee "$AUDIT_LOG"
echo "Date: $AUDIT_DATE" | tee -a "$AUDIT_LOG"
echo "" | tee -a "$AUDIT_LOG"

# 1. Count all appendices
TOTAL_FILES=$(ls appendices/*_*.tex 2>/dev/null | wc -l)
TOTAL_INDEX=$(grep -E "^[A-Z]+" appendices/00_appendix_index.tex | wc -l)

echo "Appendix count:" | tee -a "$AUDIT_LOG"
echo "  Files on disk: $TOTAL_FILES" | tee -a "$AUDIT_LOG"
echo "  Index entries: $TOTAL_INDEX" | tee -a "$AUDIT_LOG"

if [ $TOTAL_FILES -ne $TOTAL_INDEX ]; then
    echo "  ❌ MISMATCH!" | tee -a "$AUDIT_LOG"
fi
echo "" | tee -a "$AUDIT_LOG"

# 2. Check for orphans/missing
echo "Orphaned files (in disk but not index):" | tee -a "$AUDIT_LOG"
for file in appendices/*_*.tex; do
    CODE=$(basename "$file" | sed 's/_.*//g')
    if ! grep -q "^$CODE " appendices/00_appendix_index.tex; then
        echo "  - $CODE: $file" | tee -a "$AUDIT_LOG"
    fi
done

echo "" | tee -a "$AUDIT_LOG"
echo "Missing files (in index but not on disk):" | tee -a "$AUDIT_LOG"
grep -E "^[A-Z]+" appendices/00_appendix_index.tex | cut -d'&' -f1 | sed 's/ //g' | while read CODE; do
    if ! ls appendices/${CODE}_*.tex 2>/dev/null >/dev/null; then
        echo "  - $CODE" | tee -a "$AUDIT_LOG"
    fi
done

echo "" | tee -a "$AUDIT_LOG"
echo "✅ Audit complete: $AUDIT_LOG"
```

---

## 8. SOP Version & Change Log

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0 | 2026-01-15 | Initial release - 4-location validation protocol | ACTIVE |

---

*SOP-INDEX-03 | Version 1.0 | Owner: Index Integrity Team*
