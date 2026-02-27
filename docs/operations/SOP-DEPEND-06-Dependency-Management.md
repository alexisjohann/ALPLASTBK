# SOP-DEPEND-06: Dependency Management & Script Relations

> **Version:** 1.0 | **Protocol:** HHH-DEPEND-1 | **Date:** 2026-01-15
>
> **Purpose:** Track and validate dependencies between scripts, data, and outputs

---

## 1. Dependency Management Framework

### Why Dependencies Matter

**Problem:** 69 scripts in `/scripts/` with undocumented relationships:
- Script A writes `data/papers.yaml`
- Script B reads `data/papers.yaml`
- If Script B runs before Script A completes → **Data is stale**

**Solution:** Document ALL dependencies so:
1. Scripts run in correct order
2. Missing inputs are detected early
3. Impact of changes is understood
4. Execution can be parallelized where safe

### Three Dependency Types

```
┌─────────────────────────────────────────────────┐
│ TYPE 1: Data Dependencies                       │
│ Script A produces → Script B consumes            │
│ Example: papers.yaml flows from add_papers → case_linker │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ TYPE 2: Code Dependencies                       │
│ Script imports utility from other module        │
│ Example: llmmc_calibration imports from theta_mapping │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ TYPE 3: Execution Dependencies                  │
│ Script must complete before next can start      │
│ Example: generate_cases_auto must finish        │
│          before query_cases can execute         │
└─────────────────────────────────────────────────┘
```

---

## 2. Dependency Declaration Schema

### In Every Script: Metadata Block

```python
#!/usr/bin/env python3
"""
Script: register_lit_appendices.py
Version: 2.0
SOP: SOP-SCRIPT-01, SOP-APPEND-02, SOP-INDEX-03

Dependencies:
  INPUT:
    - data/papers.yaml (read): List of papers to register
    - appendices/*.tex (read): Appendix files to catalog
    - APPENDIX_CODE_REGISTRY.yaml (read): Code availability
    - appendices/00_appendix_index.tex (read-modify): Index to update

  OUTPUT:
    - appendices/00_appendix_index.tex (write): Updated index (4 locations)
    - APPENDIX_CODE_REGISTRY.yaml (write): Updated code registry
    - data/audit/events.jsonl (append): Audit log

  RUNTIME:
    - python 3.9+
    - modules: pyyaml, pathlib
    - disk space: 100MB
    - memory: 256MB

  PRECONDITION_SCRIPTS:
    - generate_lit_appendices.py (must complete first)

  DEPENDENT_SCRIPTS:
    - None (this is a leaf operation)

  IMPACT_LEVEL: CRITICAL (modifies index in 4 locations)
"""
```

### Dependency Registry File

**File:** `data/dependencies/DEPENDENCY_GRAPH.yaml`

```yaml
metadata:
  version: "1.0"
  last_updated: "2026-01-15T22:30:00"
  total_scripts: 69
  total_dependencies: 147
  critical_paths: 3

scripts:

  # Example: Paper Addition Scripts
  add_fehr_papers_100:
    type: "DATA_PRODUCER"
    description: "Add 100 Fehr papers to database"
    version: "1.0"

    inputs:
      - type: "FILE"
        path: "data/papers.yaml"
        mode: "READ"
        required: true
        purpose: "Append new papers"

    outputs:
      - type: "FILE"
        path: "data/papers.yaml"
        mode: "WRITE"
        created: false  # Appends to existing
      - type: "FILE"
        path: "data/audit/events.jsonl"
        mode: "APPEND"
        created: false

    dependencies:
      upstream: []  # No predecessor scripts
      downstream: ["case_paper_linker", "paper_lit_matcher"]
      conflicts: []  # No conflicting scripts

    execution:
      estimated_duration_seconds: 5
      disk_required_mb: 50
      memory_required_mb: 256

  generate_cases_auto:
    type: "DATA_TRANSFORMER"
    description: "Generate behavioral cases from papers"
    version: "1.0"

    inputs:
      - type: "FILE"
        path: "data/papers.yaml"
        mode: "READ"
        required: true
      - type: "REGISTRY"
        path: "data/case-registry.yaml"
        mode: "READ-MODIFY"
        required: true

    outputs:
      - type: "FILE"
        path: "data/case-registry.yaml"
        mode: "WRITE"

    dependencies:
      upstream:
        - "add_fehr_papers_100"  # Papers must be loaded first
        - "add_kahneman_papers_50"
        - "expand_paper_database"
      downstream: ["deduplicate_cases", "case_paper_linker"]
      can_parallel_with:  # These scripts don't conflict
        - "mine_journal_papers"
        - "validate_paper_robustness"

  register_lit_appendices:
    type: "INDEX_MODIFIER"
    description: "Register literature appendices in main index"
    version: "2.0"  # Fixed version with SOP compliance
    sop_references: ["SOP-SCRIPT-01", "SOP-APPEND-02", "SOP-INDEX-03"]

    inputs:
      - type: "FILE"
        path: "appendices/*.tex"
        mode: "READ"
        pattern: true  # Glob pattern
      - type: "REGISTRY"
        path: "APPENDIX_CODE_REGISTRY.yaml"
        mode: "READ"
        required: true
        purpose: "Validate codes before assignment"
      - type: "FILE"
        path: "appendices/00_appendix_index.tex"
        mode: "READ-MODIFY"
        required: true
        critical: true

    outputs:
      - type: "FILE"
        path: "appendices/00_appendix_index.tex"
        locations_modified: 4  # CRITICAL: All 4 locations
      - type: "REGISTRY"
        path: "APPENDIX_CODE_REGISTRY.yaml"
        mode: "WRITE"

    dependencies:
      upstream: ["generate_lit_appendices"]
      downstream: []
      conflicts: ["regenerate_lit_aa"]  # Don't run simultaneously

    criticality:
      level: "CRITICAL"
      impact_on_failure: "Index corrupted, orphaned files"
      recovery_procedure: "SOP-RECOVERY-04 (restore from backup)"

    mutation_points:  # 4 locations modified
      - location: "appendices/00_appendix_index.tex:430"
        name: "Summary Table"
      - location: "appendices/00_appendix_index.tex:68"
        name: "Category Counts"
      - location: "appendices/00_appendix_index.tex:612"
        name: "Status Table"
      - location: "appendices/00_appendix_index.tex:898"
        name: "Reading Paths"

  query_cases:
    type: "DATA_CONSUMER"
    description: "Query case registry by filters"
    version: "1.0"

    inputs:
      - type: "REGISTRY"
        path: "data/case-registry.yaml"
        mode: "READ"
        required: true

    outputs:
      - type: "DATA_STRUCT"
        format: "JSON"
        destination: "stdout"

    dependencies:
      upstream: ["generate_cases_auto"]  # Cases must exist
      downstream: []  # Terminal operation
      can_parallel_with: "*"  # Can run anytime (read-only)

# ... continued for all 69 scripts
```

---

## 3. Dependency Graph Visualization

### Critical Path Identification

```
┌─────────────────────────────────────────────────────────┐
│ CRITICAL PATH 1: Paper → Case → Intervention            │
│                                                         │
│ add_fehr_papers_100 ──┐                                │
│ add_kahneman_papers   ├──→ generate_cases_auto ──┐     │
│ expand_paper_database ┘                          │     │
│                                                   ├──→ case_paper_linker
│ mine_journal_papers ──────────────────────────────┘     │
│                                                         │
│ TOTAL DURATION: 45 seconds (sequential)                │
│ PARALLELIZABLE SEGMENTS: 3 (paper scripts can run ║)   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ CRITICAL PATH 2: Appendix Registration                  │
│                                                         │
│ generate_lit_falk ────────┐                           │
│ generate_lit_malmendier  ├──→ register_lit_appendices
│ generate_lit_shafir ──────┘                           │
│                                                         │
│ TOTAL DURATION: 20 seconds                             │
│ MUST RUN SEQUENTIALLY (4 locations in index)          │
└─────────────────────────────────────────────────────────┘
```

### Using Python for Graph Analysis

```python
#!/usr/bin/env python3
"""
Dependency graph analysis and validation
"""

import yaml
from pathlib import Path
from collections import defaultdict

class DependencyGraph:
    """Analyze script dependencies"""

    def __init__(self, graph_file="data/dependencies/DEPENDENCY_GRAPH.yaml"):
        with open(graph_file, 'r') as f:
            self.graph = yaml.safe_load(f)
        self.scripts = self.graph["scripts"]

    def get_execution_order(self, scripts_to_run):
        """
        Compute optimal execution order using topological sort.

        Args:
            scripts_to_run: List of script names to execute

        Returns:
            List of scripts in execution order (respecting dependencies)
        """
        from collections import deque

        # Build adjacency list
        adj = defaultdict(list)
        in_degree = defaultdict(int)

        for script in scripts_to_run:
            if script not in in_degree:
                in_degree[script] = 0

        for script in scripts_to_run:
            deps = self.scripts[script].get("dependencies", {})
            upstream = deps.get("upstream", [])
            for dep in upstream:
                if dep in scripts_to_run:
                    adj[dep].append(script)
                    in_degree[script] += 1

        # Kahn's algorithm (topological sort)
        queue = deque([s for s in scripts_to_run if in_degree[s] == 0])
        order = []

        while queue:
            script = queue.popleft()
            order.append(script)

            for dependent in adj[script]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(scripts_to_run):
            # Cycle detected
            raise ValueError("Circular dependency detected!")

        return order

    def get_critical_path(self):
        """Find longest path (critical path) through dependency graph"""
        scripts = list(self.scripts.keys())
        durations = {s: self.scripts[s].get("execution", {})
                     .get("estimated_duration_seconds", 1) for s in scripts}

        # Find path with maximum total duration
        # (This is a simplified longest path algorithm)
        critical_duration = 0
        critical_path = []

        for script in scripts:
            if not self.scripts[script]["dependencies"]["upstream"]:
                # Start from root nodes
                path = self._trace_path(script)
                duration = sum(durations[s] for s in path)

                if duration > critical_duration:
                    critical_duration = duration
                    critical_path = path

        return critical_path, critical_duration

    def _trace_path(self, script):
        """Trace longest path from given script"""
        downstream = self.scripts[script]["dependencies"].get("downstream", [])

        if not downstream:
            return [script]

        longest = [script]
        for dep in downstream:
            path = self._trace_path(dep)
            if len(path) + 1 > len(longest):
                longest = [script] + path

        return longest

    def validate_dependencies(self):
        """Check for issues in dependency graph"""
        issues = []

        for script, meta in self.scripts.items():
            deps = meta.get("dependencies", {})

            # Check for undefined dependencies
            for upstream in deps.get("upstream", []):
                if upstream not in self.scripts:
                    issues.append(f"UNDEFINED: {script} depends on non-existent {upstream}")

            for downstream in deps.get("downstream", []):
                if downstream not in self.scripts:
                    issues.append(f"UNDEFINED: {script} lists non-existent {downstream}")

            # Check for bidirectional consistency
            for upstream in deps.get("upstream", []):
                if upstream in self.scripts:
                    upstream_downstream = (self.scripts[upstream]
                                          .get("dependencies", {})
                                          .get("downstream", []))
                    if script not in upstream_downstream:
                        issues.append(
                            f"INCONSISTENT: {script} depends on {upstream}, "
                            f"but {upstream} doesn't list {script} as downstream"
                        )

        return issues
```

---

## 4. Dependency Validation Workflow

### Pre-Execution Checks

Before running any script, validate:

```python
def validate_script_dependencies(script_name):
    """
    Validate that script can safely execute.

    Returns:
        dict with status, missing inputs, conflicts
    """
    graph = DependencyGraph()
    script = graph.scripts.get(script_name)

    if not script:
        return {"status": "UNKNOWN_SCRIPT"}

    result = {
        "status": "READY",
        "script": script_name,
        "issues": []
    }

    # Check input files exist
    for input_file in script.get("inputs", []):
        path = input_file["path"]
        if input_file.get("pattern"):
            # Glob pattern - at least one match required
            from glob import glob
            matches = glob(path)
            if not matches:
                result["issues"].append(f"NO_INPUT_MATCH: {path}")
                result["status"] = "MISSING_INPUT"
        else:
            # Exact file required
            if not Path(path).exists():
                result["issues"].append(f"MISSING_INPUT: {path}")
                result["status"] = "MISSING_INPUT"

    # Check upstream scripts completed
    for upstream in script.get("dependencies", {}).get("upstream", []):
        # Query audit log: did upstream script execute successfully?
        from audit_logger import AuditLogger
        logger = AuditLogger()
        events = logger.query_events(
            category="SCRIPT",
            operation="EXECUTE"
        )
        latest_upstream = [e for e in events
                          if upstream in e.get("actor", {}).get("identifier", "")]
        if not latest_upstream or latest_upstream[-1]["execution"]["status"] != "SUCCESS":
            result["issues"].append(f"UPSTREAM_NOT_COMPLETE: {upstream}")
            result["status"] = "WAITING_FOR_UPSTREAM"

    # Check for concurrent conflicts
    conflicts = script.get("dependencies", {}).get("conflicts", [])
    for conflict_script in conflicts:
        # Query audit log: is conflict script currently running?
        # This requires SOP-MONITOR-08 integration
        pass

    return result
```

---

## 5. Dependency Impact Analysis

### "If I change this file, what breaks?"

```python
def impact_analysis(changed_file):
    """
    Determine which scripts would be affected by changing a file.

    Args:
        changed_file: Path to file that changed

    Returns:
        List of affected scripts in order of impact
    """
    graph = DependencyGraph()
    affected = []

    for script_name, meta in graph.scripts.items():
        # Check if script reads this file
        for input_file in meta.get("inputs", []):
            if input_file["path"] == changed_file:
                affected.append({
                    "script": script_name,
                    "impact": "DIRECT_INPUT",
                    "critical": input_file.get("required", False),
                    "mode": input_file.get("mode")
                })
                break

    # Find downstream scripts
    for affected_script in list(affected):
        downstream = graph.scripts[affected_script["script"]].get(
            "dependencies", {}).get("downstream", [])
        for downstream_script in downstream:
            affected.append({
                "script": downstream_script,
                "impact": "INDIRECT_DEPENDENCY",
                "critical": False
            })

    return affected

# Example usage:
changes = impact_analysis("data/papers.yaml")
print("If papers.yaml changes, these scripts are affected:")
for change in changes:
    print(f"  - {change['script']} ({change['impact']})")
```

---

## 6. Automated Dependency Verification

### Scheduled Validation Job

**Cron:** Daily at 02:00 UTC

```bash
#!/bin/bash
# Daily dependency validation

python3 << 'EOF'
from dependency_graph import DependencyGraph
from datetime import datetime

print(f"🔍 Daily Dependency Verification: {datetime.now().isoformat()}")

graph = DependencyGraph()

# Check for issues
issues = graph.validate_dependencies()
if issues:
    print(f"\n⚠️  Found {len(issues)} issues:")
    for issue in issues:
        print(f"   - {issue}")
else:
    print("\n✅ All dependencies valid")

# Identify critical path
path, duration = graph.get_critical_path()
print(f"\n📊 Critical Path (execution time: {duration}s):")
for script in path:
    print(f"   → {script}")

EOF
```

---

## 7. Checklist: Dependency Management

```
☐ Dependency graph created (DEPENDENCY_GRAPH.yaml)
☐ All 69 scripts documented with dependencies
☐ Dependency validation working
☐ Topological sort for execution order
☐ Critical path identified
☐ Impact analysis tool created
☐ Conflict detection implemented
☐ Daily validation scheduled
☐ Pre-execution checks in SOP-SCRIPT-01
☐ Audit logging tracks dependencies
```

---

*SOP-DEPEND-06: Dependency Management | Version: 1.0 | Date: 2026-01-15 | Protocol: HHH-DEPEND-1*
