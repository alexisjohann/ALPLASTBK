# /integration-test - Integration Test Suite for EBF Framework

## Overview

The **Integration Test Suite** validates that new appendices, chapters, and changes are properly integrated into the EBF Framework. It checks:

- **LaTeX syntax** consistency (balanced environments)
- **Cross-references** and citations (label matching)
- **Appendix index** accuracy (counts and entries)
- **Parameter sourcing** discipline (formulas, citations, disclosures)
- **Chapter consistency** (worked examples, sourcing, documentation)

## Quick Start

```bash
# Run all 9 integration tests
/integration-test

# Run specific test (1-9)
/integration-test --test 5

# Test specific chapter
/integration-test --chapter 20

# Test specific appendix
/integration-test --appendix JJJ

# Verbose output
/integration-test --verbose

# JSON output format
/integration-test --json
```

## The 9 Integration Tests

### Test 1: LaTeX Syntax Balance
**What it checks:** Opening `\begin{}` and closing `\end{}` environments are balanced.

```bash
/integration-test --test 1
```

**Why it matters:** Unbalanced LaTeX environments prevent PDF compilation.

**Pass Criteria:**
- Opening count = Closing count

**Example Output:**
```
✅ Test 1: LaTeX Syntax Balance
   Status: PASS | Severity: INFO
   Details: Opening: 67 ✓, Closing: 67 ✓
```

---

### Test 2: Internal Cross-References
**What it checks:** All `\ref{}` and `\eqref{}` references have matching `\label{}` definitions.

```bash
/integration-test --test 2
```

**Why it matters:** Broken references cause LaTeX warnings and unclear documentation.

**Pass Criteria:**
- Every reference has a corresponding label
- No undefined references

**Example Output:**
```
✅ Test 2: Internal Cross-References
   Status: PASS | Severity: INFO
   Details: All 15 references have matching labels ✓
```

---

### Test 3: Appendix Index Entry
**What it checks:** New appendix is registered in `00_appendix_index.tex`.

```bash
/integration-test --test 3
```

**Why it matters:** Omitting index entries makes appendices unfindable in the framework.

**Pass Criteria:**
- Entry exists in appropriate category table (METHOD, CORE, etc.)
- Code and category name are correct

**Example Output:**
```
✅ Test 3: Appendix Index Entry
   Status: PASS | Severity: INFO
   Details: JJJ & METHOD-PSG entry found in METHOD table ✓
```

---

### Test 4: Appendix Counts
**What it checks:** Total appendix count and category counts are updated correctly.

```bash
/integration-test --test 4
```

**Why it matters:** Stale counts create confusion about framework scope.

**Pass Criteria:**
- METHOD count updated (+1 per new METHOD appendix)
- Total appendix count updated

**Example Output:**
```
✅ Test 4: Appendix Counts
   Status: PASS | Severity: INFO
   Details: METHOD: 15 ✓, Total: 129 ✓
```

---

### Test 5: Rente Formula Documentation
**What it checks:** Rente example has visible formula, derivation table, and Ch18 citations.

```bash
/integration-test --test 5
```

**Why it matters:** Hidden formulas make examples non-reproducible.

**Pass Criteria:**
- Formula: $E_\varphi = E_\text{baseline} \times \alpha(\varphi)$ is visible
- Derivation table with phase-affinity multipliers
- Ch18 citation with line numbers (440-485)

**Example Output:**
```
✅ Test 5: Rente Formula Documentation
   Status: PASS | Severity: INFO
   Details: Formula ✓, Table ✓, Ch18 refs (440-485) ✓
```

---

### Test 6: Energie Segment Multipliers
**What it checks:** Energie example has correct (sourced) segment multipliers.

```bash
/integration-test --test 6
```

**Why it matters:** Unsourced segment values create false backfire claims.

**Pass Criteria:**
- Autonomy-Seeking σ = 0.8 (from Ch19, not 0.4)
- Three segments documented (Present-Biased, Social-Oriented, Autonomy-Seeking)
- Baseline: 13.6% (recalculated from weighted average)
- Ch19 citation with line numbers (1128-1135)

**Example Output:**
```
✅ Test 6: Energie Segment Multipliers
   Status: PASS | Severity: INFO
   Details: AS σ=0.8 ✓, Ch19 refs ✓, Baseline 13.6% ✓, 3 segments ✓
```

---

### Test 7: Engagement Disclosure
**What it checks:** Engagement example has transparency disclosure and segment-specific insights.

```bash
/integration-test --test 7
```

**Why it matters:** Illustrative parameters must be disclosed to practitioners.

**Pass Criteria:**
- IMPORTANT DISCLOSURE box present
- References Ch17 and Ch19
- Mentions synthesized parameters
- Recommends practitioner validation
- Segment-specific $I_F$ suppression values from Ch19

**Example Output:**
```
✅ Test 7: Engagement Disclosure
   Status: PASS | Severity: INFO
   Details: Disclosure ✓, Ch19 suppression values ✓
```

---

### Test 8: Cross-References (Ch20 to Appendix)
**What it checks:** JJJ appendix documents all four worked examples from Ch20.

```bash
/integration-test --test 8
```

**Why it matters:** Appendix should be discoverable from the examples it documents.

**Pass Criteria:**
- All 4 examples mentioned (Diabetes, Rente, Energie, Engagement)
- Case Studies section present
- Problem statements match actual examples

**Example Output:**
```
✅ Test 8: Ch20 to JJJ Cross-References
   Status: PASS | Severity: INFO
   Details: All 4 examples documented ✓, Case studies section ✓
```

---

### Test 9: Citation Specificity
**What it checks:** All chapter citations include specific locations (line numbers, equations).

```bash
/integration-test --test 9
```

**Why it matters:** Non-specific citations prevent readers from finding sourced material.

**Pass Criteria:**
- Ch17 citations include equation numbers (e.g., "Eq. 684")
- Ch18 citations include line numbers
- Ch19 citations include line numbers
- No vague references like "See Ch17"

**Example Output:**
```
✅ Test 9: Citation Specificity
   Status: PASS | Severity: INFO
   Details: Ch17 ✓, Ch18 lines ✓, Ch19 lines ✓
```

---

## Advanced Usage

### Test Specific Chapter
```bash
/integration-test --chapter 20
# Runs all tests relevant to Chapter 20
```

### Test Specific Appendix
```bash
/integration-test --appendix JJJ
# Runs all tests relevant to Appendix JJJ
```

### Verbose Output (Debug Mode)
```bash
/integration-test --verbose
# Shows all checks, even passing ones
# Useful for debugging test failures
```

### JSON Output Format
```bash
/integration-test --json
# Output in machine-readable JSON format
# Useful for CI/CD integration
```

Example JSON output:
```json
{
  "summary": {
    "total": 9,
    "passed": 9,
    "failed": 0,
    "skipped": 0,
    "status": "PASS"
  },
  "tests": [
    {
      "test_id": 1,
      "test_name": "LaTeX Syntax Balance",
      "status": "PASS",
      "details": "Opening: 67 ✓, Closing: 67 ✓",
      "severity": "INFO"
    },
    ...
  ]
}
```

---

## Test Severity Levels

- **CRITICAL**: Blocks publication (breaks PDF compilation, core functionality)
- **HIGH**: Should be fixed before merge (incomplete integration, missing references)
- **MEDIUM**: Should be addressed (specific citations, documentation completeness)
- **LOW**: Nice-to-have improvements (formatting, consistency)
- **INFO**: Informational only (passed tests, skipped tests)

---

## Exit Codes

```
0 = All tests passed (✅ ready to merge)
1 = One or more tests failed (❌ fix required)
2 = Configuration error (❌ check setup)
```

---

## Common Failures & Solutions

### ❌ Test 1 Failed: "Mismatch: 68 opening vs 67 closing"
**Problem:** Unbalanced LaTeX environments in new content.

**Solution:**
1. Search for `\begin{` in the new file
2. Verify each has matching `\end{`
3. Check for typos: `\begin{table}` → `\end{table}` (not `\end{Table}`)

### ❌ Test 2 Failed: "Missing labels: eq:new-formula"
**Problem:** Reference exists but label not defined.

**Solution:**
1. Find the `\ref{eq:new-formula}` reference
2. Go to that equation/environment
3. Add `\label{eq:new-formula}` right after it

### ❌ Test 3 Failed: "JJJ entry not found in appendix index"
**Problem:** New appendix not added to `00_appendix_index.tex`.

**Solution:**
1. Open `appendices/00_appendix_index.tex`
2. Find the appropriate category table (METHOD, DOMAIN, etc.)
3. Add entry: `CODE & CATEGORY-NAME & Title & Description \\`
4. Update count in category summary table

### ❌ Test 6 Failed: "Missing: AS σ=0.8, Ch19 reference"
**Problem:** Energie example uses unsourced segment multipliers.

**Solution:**
1. Check Ch19 for actual segment multipliers
2. Replace unsourced values with Ch19 values
3. Add citation: `(Ch19, lines 1128-1135)`
4. Remove any false backfire claims

---

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Integration Tests
on: [push, pull_request]

jobs:
  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Integration Tests
        run: python scripts/integration_test.py --json > results.json
      - name: Check Results
        run: |
          if grep -q '"status": "FAIL"' results.json; then
            echo "Integration tests failed"
            exit 1
          fi
```

---

## Performance

Typical test suite runtime:
- **All 9 tests**: ~2-3 seconds
- **Single test**: ~0.5 seconds
- **Verbose mode**: ~3-4 seconds

---

## Troubleshooting

### Script not found error
```bash
# Make sure you're in project root
cd /path/to/complementarity-context-framework

# Then run
python scripts/integration_test.py
```

### Permission denied
```bash
# Make script executable
chmod +x scripts/integration_test.py
```

### Python not found
```bash
# Use python3 explicitly
python3 scripts/integration_test.py
```

---

## Related Documentation

- **Appendix Index**: `appendices/00_appendix_index.tex`
- **Ch17-20 Sourcing Guide**: Appendix JJJ (METHOD-PSG)
- **Parameter Sourcing Workflow**: Section 2 of Appendix JJJ
- **CLAUDE.md Instructions**: `./../CLAUDE.md` (template compliance, audit procedures)

---

## Version History

- **v1.0** (2026-01-21): Initial release with 9 integration tests
  - Tests 1-4: Framework structure and indexing
  - Tests 5-7: Chapter 20 worked examples
  - Tests 8-9: Cross-references and citations

---

**Last Updated:** 2026-01-21 | **Status:** Production Ready ✅
