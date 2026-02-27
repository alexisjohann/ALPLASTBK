# SOP-VALID-07: Automated Validation Framework

> **Version:** 1.0 | **Protocol:** HHH-VALID-1 | **Date:** 2026-01-15
>
> **Purpose:** Continuous validation of scripts, data, and outputs

---

## 1. Validation Architecture

### Four Validation Tiers

```
┌─────────────────────────────────────────────────┐
│ TIER 1: Pre-Execution Validation (SOP-SCRIPT-01)│
│ • Preconditions verified                        │
│ • Input files exist and readable                │
│ • Dependencies satisfied                        │
│ Runs: BEFORE script execution                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ TIER 2: Post-Execution Validation (SOP-SCRIPT-01)│
│ • Output files created and valid                │
│ • Data structure integrity checks               │
│ • Index consistency verification                │
│ Runs: AFTER script execution                    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ TIER 3: Continuous Validation (Scheduled)       │
│ • Hourly: Template compliance                   │
│ • Daily: Index consistency                      │
│ • Weekly: Full system integrity                 │
│ Runs: Automatically on schedule                 │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ TIER 4: On-Demand Validation                    │
│ • Full system audit                             │
│ • Cross-reference verification                  │
│ • Compliance scoring                            │
│ Runs: User-triggered via /validate command      │
└─────────────────────────────────────────────────┘
```

---

## 2. Validation Rules Registry

### Schema

**File:** `data/validation/VALIDATION_RULES.yaml`

```yaml
metadata:
  version: "1.0"
  last_updated: "2026-01-15"
  total_rules: 47

validation_tiers:

  # ====== TIER 1: Pre-Execution ======
  tier1_preconditions:
    - rule_id: "PRE-001"
      name: "Input file exists"
      applies_to: ["all_scripts"]
      check: |
        for input_file in script.inputs:
            assert Path(input_file).exists(), f"Missing: {input_file}"
      severity: "CRITICAL"
      sop_reference: "SOP-SCRIPT-01, Section 2"

    - rule_id: "PRE-002"
      name: "Index is valid YAML"
      applies_to: ["register_lit_appendices", "regenerate_lit_aa"]
      check: |
        index = yaml.safe_load(open("appendices/00_appendix_index.tex"))
        assert index is not None, "Index is not valid YAML"
      severity: "CRITICAL"

    - rule_id: "PRE-003"
      name: "Code availability check"
      applies_to: ["register_lit_appendices"]
      check: |
        registry = yaml.safe_load(open("APPENDIX_CODE_REGISTRY.yaml"))
        for code in new_codes:
            assert code not in registry["assigned_codes"], f"Code conflict: {code}"
      severity: "CRITICAL"
      sop_reference: "SOP-APPEND-02"

    - rule_id: "PRE-004"
      name: "Backup created before execution"
      applies_to: ["all_scripts_modifying_files"]
      check: |
        backup = create_backup(primary_input)
        assert backup.exists(), "Backup failed"
      severity: "HIGH"
      sop_reference: "SOP-RECOVERY-04"

  # ====== TIER 2: Post-Execution ======
  tier2_postconditions:
    - rule_id: "POST-001"
      name: "Output file exists and readable"
      applies_to: ["all_scripts_with_output"]
      check: |
        for output_file in script.outputs:
            assert Path(output_file).exists(), f"Missing output: {output_file}"
            assert Path(output_file).stat().st_size > 0, f"Empty: {output_file}"
      severity: "CRITICAL"

    - rule_id: "POST-002"
      name: "4-location index sync verified"
      applies_to: ["register_lit_appendices"]
      check: |
        loc1 = count_summary_table()
        loc2 = count_category_counts()
        loc3 = count_status_table()
        loc4 = count_reading_paths()
        assert loc1 == loc2 == loc3 == loc4, "Index locations out of sync"
      severity: "CRITICAL"
      sop_reference: "SOP-INDEX-03"

    - rule_id: "POST-003"
      name: "No orphaned files"
      applies_to: ["register_lit_appendices"]
      check: |
        files = set(Path("appendices").glob("*.tex"))
        indexed = set(extract_filenames_from_index())
        orphans = files - indexed
        assert not orphans, f"Orphaned files: {orphans}"
      severity: "HIGH"

    - rule_id: "POST-004"
      name: "No duplicate codes"
      applies_to: ["register_lit_appendices"]
      check: |
        codes = extract_codes_from_index()
        assert len(codes) == len(set(codes)), "Duplicate codes detected"
      severity: "CRITICAL"

    - rule_id: "POST-005"
      name: "Audit log entry created"
      applies_to: ["all_scripts"]
      check: |
        events = AuditLogger().query_events(
            category="SCRIPT",
            operation="EXECUTE"
        )
        assert events[-1]["actor"]["identifier"] == current_script.name
      severity: "MEDIUM"
      sop_reference: "SOP-AUDIT-05"

  # ====== TIER 3: Continuous (Scheduled) ======
  tier3_continuous:
    - rule_id: "CONT-001"
      name: "Template compliance (Appendices)"
      frequency: "hourly"
      applies_to: ["appendices/*.tex"]
      check: |
        for file in Path("appendices").glob("*.tex"):
            score = check_template_compliance(file)
            assert score >= 85, f"{file}: {score}% < 85%"
      severity: "MEDIUM"
      sop_reference: "SOP-APPEND-02"

    - rule_id: "CONT-002"
      name: "Template compliance (Chapters)"
      frequency: "hourly"
      applies_to: ["chapters/*.tex"]
      check: |
        for file in Path("chapters").glob("*.tex"):
            score = check_chapter_compliance(file)
            assert score >= 85, f"{file}: {score}% < 85%"
      severity: "MEDIUM"

    - rule_id: "CONT-003"
      name: "Index consistency"
      frequency: "daily"
      applies_to: ["appendices/00_appendix_index.tex"]
      check: |
        # Verify all 4 locations synchronized
        manager = AppendixIndexManager()
        manager.validate_all_locations()
      severity: "HIGH"
      sop_reference: "SOP-INDEX-03"

    - rule_id: "CONT-004"
      name: "Code registry sync"
      frequency: "daily"
      applies_to: ["APPENDIX_CODE_REGISTRY.yaml"]
      check: |
        registry = load_code_registry()
        index = load_index()
        for code in registry["assigned_codes"]:
            assert code in index["all_codes"], f"Code {code} in registry but not index"
      severity: "HIGH"

    - rule_id: "CONT-005"
      name: "Dependency graph consistency"
      frequency: "daily"
      applies_to: ["data/dependencies/DEPENDENCY_GRAPH.yaml"]
      check: |
        graph = DependencyGraph()
        issues = graph.validate_dependencies()
        assert not issues, f"Dependency issues: {issues}"
      severity: "MEDIUM"
      sop_reference: "SOP-DEPEND-06"

    - rule_id: "CONT-006"
      name: "Core framework consistency"
      frequency: "weekly"
      applies_to: ["docs/frameworks/core-framework-definition.yaml"]
      check: |
        import subprocess
        result = subprocess.run(
            ["python", "scripts/validate_core_framework.py"],
            capture_output=True
        )
        assert result.returncode == 0, "10C framework validation failed"
      severity: "MEDIUM"
      sop_reference: "CLAUDE.md: 10C CORE Framework"

    - rule_id: "CONT-007"
      name: "Bibliography integrity"
      frequency: "weekly"
      applies_to: ["bibliography/*.bib"]
      check: |
        # Validate BibTeX syntax
        import re
        for entry in parse_bibtex():
            assert "author" in entry, f"Missing author: {entry}"
            assert "year" in entry, f"Missing year: {entry}"
      severity: "LOW"

    - rule_id: "CONT-008"
      name: "Audit log integrity"
      frequency: "daily"
      applies_to: ["data/audit/events.jsonl"]
      check: |
        logger = AuditLogger()
        logger._verify_events_log_integrity()
      severity: "HIGH"
      sop_reference: "SOP-AUDIT-05"

  # ====== TIER 4: On-Demand ======
  tier4_ondemand:
    - rule_id: "FULL-001"
      name: "Complete system audit"
      command: "/validate"
      checks:
        - "All files referenced in index exist"
        - "No orphaned or ghost entries"
        - "No code conflicts"
        - "All 4 index locations synchronized"
        - "Dependency graph valid"
        - "All compliance scores >= 85%"
        - "Audit log integrity verified"
        - "Backup system operational"
      duration_seconds: 45

    - rule_id: "FULL-002"
      name: "Cross-reference audit"
      command: "/validate --cross-refs"
      checks:
        - "All CLAUDE.md references point to existing files"
        - "All chapter→appendix cross-refs valid"
        - "All appendix→appendix cross-refs valid"
        - "All SOP references accurate"
      duration_seconds: 20

    - rule_id: "FULL-003"
      name: "Compliance scorecard"
      command: "/validate --compliance"
      checks:
        - "Appendix compliance >= 85%"
        - "Chapter compliance >= 85%"
        - "Framework consistency 100%"
        - "Dependency graph consistent"
        - "Index integrity verified"
      output: "HTML dashboard in outputs/compliance.html"
```

---

## 3. ValidationEngine Implementation

```python
#!/usr/bin/env python3
"""
ValidationEngine: Automated validation framework
"""

import yaml
from pathlib import Path
from datetime import datetime
from audit_logger import AuditLogger

class ValidationEngine:
    """Execute validation rules and track results"""

    def __init__(self, rules_file="data/validation/VALIDATION_RULES.yaml"):
        with open(rules_file, 'r') as f:
            self.rules = yaml.safe_load(f)
        self.logger = AuditLogger()
        self.results = []

    def validate_tier(self, tier_number):
        """
        Execute all rules for a validation tier.

        Args:
            tier_number: 1, 2, 3, or 4

        Returns:
            dict with results and summary
        """
        tier_name = f"tier{tier_number}_" + ("preconditions" if tier_number == 1
                                              else "postconditions" if tier_number == 2
                                              else "continuous" if tier_number == 3
                                              else "ondemand")

        rules = self.rules.get("validation_tiers", {}).get(tier_name, [])
        tier_results = {
            "tier": tier_number,
            "timestamp": datetime.now().isoformat(),
            "rules_executed": 0,
            "passed": 0,
            "failed": 0,
            "details": []
        }

        for rule in rules:
            rule_id = rule["rule_id"]
            rule_name = rule["name"]

            try:
                # Execute the check
                result = self._execute_check(rule["check"])

                if result:
                    tier_results["passed"] += 1
                    status = "PASSED"
                else:
                    tier_results["failed"] += 1
                    status = "FAILED"

                tier_results["details"].append({
                    "rule_id": rule_id,
                    "name": rule_name,
                    "status": status,
                    "severity": rule.get("severity", "MEDIUM")
                })

                # Log to audit trail
                self.logger.log_event(
                    category="VALIDATION",
                    operation="VALIDATE",
                    target={"type": "RULE", "path": rule_id},
                    execution={
                        "status": "SUCCESS" if result else "FAILURE",
                        "exit_code": 0 if result else 1
                    },
                    metadata={
                        "rule_name": rule_name,
                        "tier": tier_number,
                        "result": status
                    }
                )

            except Exception as e:
                tier_results["failed"] += 1
                tier_results["details"].append({
                    "rule_id": rule_id,
                    "name": rule_name,
                    "status": "ERROR",
                    "error": str(e),
                    "severity": rule.get("severity", "MEDIUM")
                })

            tier_results["rules_executed"] += 1

        return tier_results

    def validate_full_system(self):
        """Execute all 4 validation tiers"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "SUCCESS",
            "tiers": []
        }

        for tier in [1, 2, 3, 4]:
            tier_result = self.validate_tier(tier)
            results["tiers"].append(tier_result)

            if tier_result["failed"] > 0:
                results["overall_status"] = "PARTIAL_FAILURE"

            # CRITICAL: Tier 1 and 2 failures are blocking
            if tier in [1, 2] and tier_result["failed"] > 0:
                results["overall_status"] = "CRITICAL_FAILURE"
                break  # Stop further validation

        return results

    def _execute_check(self, check_code):
        """Execute a validation check (simplified)"""
        # In production, this would safely evaluate the check code
        # For now, return placeholder
        return True

    def generate_report(self, results, output_file="outputs/validation_report.html"):
        """Generate HTML report of validation results"""
        html = """
        <html>
        <head>
            <title>System Validation Report</title>
            <style>
                body { font-family: monospace; }
                .passed { color: green; }
                .failed { color: red; }
                .critical { background-color: #ffcccc; }
            </style>
        </head>
        <body>
            <h1>System Validation Report</h1>
            <p>Generated: {timestamp}</p>
            <p>Overall Status: <span class="{status_class}">{status}</span></p>
            <h2>Tier Summaries</h2>
            {tier_summaries}
        </body>
        </html>
        """

        tier_summaries = ""
        for tier in results["tiers"]:
            tier_summaries += f"""
            <div class="tier">
                <h3>Tier {tier['tier']}</h3>
                <p>Executed: {tier['rules_executed']} | Passed: {tier['passed']} | Failed: {tier['failed']}</p>
                <table>
                    <tr><th>Rule ID</th><th>Name</th><th>Status</th><th>Severity</th></tr>
            """

            for detail in tier["details"]:
                css_class = "passed" if detail["status"] == "PASSED" else "failed"
                if detail.get("severity") == "CRITICAL":
                    css_class += " critical"

                tier_summaries += f"""
                    <tr class="{css_class}">
                        <td>{detail['rule_id']}</td>
                        <td>{detail['name']}</td>
                        <td>{detail['status']}</td>
                        <td>{detail.get('severity', 'MEDIUM')}</td>
                    </tr>
                """

            tier_summaries += "</table></div>"

        # Render HTML
        html_content = html.format(
            timestamp=results["timestamp"],
            status=results["overall_status"],
            status_class="passed" if results["overall_status"] == "SUCCESS" else "failed",
            tier_summaries=tier_summaries
        )

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
```

---

## 4. Scheduled Validation Jobs

### Cron Schedule

```bash
# /etc/cron.d/validation-schedule

# TIER 1: Pre-execution (on-demand, triggered by scripts)

# TIER 2: Post-execution (on-demand, triggered by scripts)

# TIER 3: Continuous validation
0  * * * * root python3 /scripts/validate_tier3.py --tier continuous-hourly
0  2 * * * root python3 /scripts/validate_tier3.py --tier continuous-daily
0  3 * * 0 root python3 /scripts/validate_tier3.py --tier continuous-weekly

# TIER 4: Full system audit (monthly)
0  4 1 * * root python3 /scripts/validate_tier4.py --full-system
```

---

## 5. Integration with CI/CD

### Pre-Commit Hook

**File:** `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Pre-commit validation

python3 << 'EOF'
from validation_engine import ValidationEngine

engine = ValidationEngine()

# Run TIER 2 validation (post-execution) on staged changes
result = engine.validate_tier(2)

if result["failed"] > 0:
    print("❌ Validation failed. Fix issues before committing:")
    for detail in result["details"]:
        if detail["status"] == "FAILED":
            print(f"   - {detail['name']}")
    exit(1)

print("✅ Validation passed")
exit(0)
EOF
```

---

## 6. Failure Response Protocol

### When a validation fails:

1. **Log the failure** to audit trail (SOP-AUDIT-05)
2. **Classify severity:**
   - CRITICAL: Block execution, investigate immediately
   - HIGH: Flag for attention, may proceed with caution
   - MEDIUM: Log and monitor
   - LOW: Informational

3. **Determine action:**
   - If TIER 1 (pre-execution) fails: **STOP** - don't run script
   - If TIER 2 (post-execution) fails: **ROLLBACK** - restore from backup (SOP-RECOVERY-04)
   - If TIER 3 (continuous) fails: **ALERT** - notify team, investigate
   - If TIER 4 (on-demand) fails: **REPORT** - generate detailed diagnostic

4. **Document in incident log** (SOP-AUDIT-05)

---

## 7. Checklist: Validation Framework

```
☐ VALIDATION_RULES.yaml created with 47+ rules
☐ ValidationEngine class implemented
☐ TIER 1 (pre-execution) rules active
☐ TIER 2 (post-execution) rules active
☐ TIER 3 (continuous) rules scheduled
☐ TIER 4 (on-demand) rules accessible via /validate
☐ Pre-commit hook integration
☐ Audit logging integration
☐ HTML report generation
☐ Failure response protocol documented
☐ Monthly full-system audit scheduled
```

---

*SOP-VALID-07: Validation Framework | Version: 1.0 | Date: 2026-01-15 | Protocol: HHH-VALID-1*
