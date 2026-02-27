#!/usr/bin/env python3
"""
DependencyGraph: Script dependency tracking and validation

Implements SOP-DEPEND-06: Dependency Management & Script Relations
- Maps all script dependencies
- Computes execution order via topological sort
- Identifies critical path
- Performs impact analysis

Usage:
    graph = DependencyGraph("data/dependencies/DEPENDENCY_GRAPH.yaml")
    order = graph.get_execution_order(['script1', 'script2', 'script3'])
    issues = graph.validate_dependencies()
"""

import yaml
from pathlib import Path
from collections import defaultdict, deque


class DependencyGraph:
    """Analyze and validate script dependencies"""

    def __init__(self, graph_file="data/dependencies/DEPENDENCY_GRAPH.yaml"):
        """Load dependency graph from YAML"""
        self.graph_file = Path(graph_file)

        if self.graph_file.exists():
            with open(self.graph_file, 'r') as f:
                self.graph = yaml.safe_load(f)
                self.scripts = self.graph.get("scripts", {})
        else:
            # Default empty graph
            self.graph = {"scripts": {}}
            self.scripts = {}

    def get_execution_order(self, scripts_to_run):
        """
        Compute optimal execution order using topological sort.

        Args:
            scripts_to_run: List of script names to execute

        Returns:
            List of scripts in execution order (respecting dependencies)
        """
        # Build adjacency list for specified scripts
        adj = defaultdict(list)
        in_degree = defaultdict(int)

        for script in scripts_to_run:
            if script not in in_degree:
                in_degree[script] = 0

        for script in scripts_to_run:
            if script not in self.scripts:
                continue

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
        """
        Find longest path (critical path) through dependency graph.

        Returns:
            (path, total_duration) tuple
        """
        scripts = list(self.scripts.keys())

        if not scripts:
            return [], 0

        durations = {}
        for s in scripts:
            exec_info = self.scripts[s].get("execution", {})
            duration = exec_info.get("estimated_duration_seconds", 1)
            durations[s] = duration

        # Find path with maximum total duration
        critical_duration = 0
        critical_path = []

        for script in scripts:
            if not self.scripts[script]["dependencies"].get("upstream"):
                # Start from root nodes
                path = self._trace_path(script, durations)
                duration = sum(durations.get(s, 1) for s in path)

                if duration > critical_duration:
                    critical_duration = duration
                    critical_path = path

        return critical_path, critical_duration

    def _trace_path(self, script, durations):
        """Trace longest path from given script"""
        if script not in self.scripts:
            return [script]

        downstream = self.scripts[script]["dependencies"].get("downstream", [])

        if not downstream:
            return [script]

        longest = [script]
        for dep in downstream:
            path = self._trace_path(dep, durations)
            if len(path) + 1 > len(longest):
                longest = [script] + path

        return longest

    def validate_dependencies(self):
        """
        Check for issues in dependency graph.

        Returns:
            List of issue strings (empty if all valid)
        """
        issues = []

        for script, meta in self.scripts.items():
            deps = meta.get("dependencies", {})

            # Check for undefined dependencies
            for upstream in deps.get("upstream", []):
                if upstream not in self.scripts:
                    issues.append(
                        f"UNDEFINED: {script} depends on non-existent {upstream}")

            for downstream in deps.get("downstream", []):
                if downstream not in self.scripts:
                    issues.append(
                        f"UNDEFINED: {script} lists non-existent downstream {downstream}")

            # Check for bidirectional consistency
            for upstream in deps.get("upstream", []):
                if upstream in self.scripts:
                    upstream_downstream = (self.scripts[upstream]
                                          .get("dependencies", {})
                                          .get("downstream", []))
                    if script not in upstream_downstream:
                        issues.append(
                            f"INCONSISTENT: {script} depends on {upstream}, "
                            f"but {upstream} doesn't list {script} as downstream")

        return issues

    def impact_analysis(self, changed_file):
        """
        Determine which scripts would be affected by changing a file.

        Args:
            changed_file: Path to file that changed

        Returns:
            List of affected scripts with impact info
        """
        affected = []

        for script_name, meta in self.scripts.items():
            # Check if script reads this file
            for input_file in meta.get("inputs", []):
                if input_file.get("path") == changed_file:
                    affected.append({
                        "script": script_name,
                        "impact": "DIRECT_INPUT",
                        "critical": input_file.get("required", False),
                        "mode": input_file.get("mode")
                    })
                    break

        # Find downstream scripts
        for affected_script in list(affected):
            downstream = self.scripts[affected_script["script"]].get(
                "dependencies", {}).get("downstream", [])
            for downstream_script in downstream:
                affected.append({
                    "script": downstream_script,
                    "impact": "INDIRECT_DEPENDENCY",
                    "critical": False
                })

        return affected

    def get_parallel_groups(self, scripts_to_run):
        """
        Identify groups of scripts that can run in parallel.

        Args:
            scripts_to_run: List of script names

        Returns:
            List of lists, where each inner list can run in parallel
        """
        order = self.get_execution_order(scripts_to_run)
        groups = []
        used = set()

        while len(used) < len(order):
            # Find scripts that can run now (no dependencies on unused scripts)
            group = []
            for script in order:
                if script in used:
                    continue

                deps = self.scripts[script].get("dependencies", {})
                upstream = set(deps.get("upstream", []))
                conflicts = set(deps.get("conflicts", []))

                # Can run if all upstream done and no conflicts in group
                if upstream.issubset(used) and not conflicts.intersection(set(group)):
                    group.append(script)

            if not group:
                break

            groups.append(group)
            used.update(group)

        return groups


if __name__ == "__main__":
    # Test dependency graph
    graph = DependencyGraph()

    # Create test data
    test_scripts = {
        "paper_add": {
            "dependencies": {
                "upstream": [],
                "downstream": ["case_gen"]
            }
        },
        "case_gen": {
            "dependencies": {
                "upstream": ["paper_add"],
                "downstream": ["case_link"]
            }
        },
        "case_link": {
            "dependencies": {
                "upstream": ["case_gen"],
                "downstream": []
            }
        }
    }

    graph.scripts = test_scripts

    # Test execution order
    order = graph.get_execution_order(["paper_add", "case_gen", "case_link"])
    print(f"✓ Execution order: {order}")

    # Test critical path
    path, duration = graph.get_critical_path()
    print(f"✓ Critical path: {' → '.join(path)} ({duration}s)")

    # Test validation
    issues = graph.validate_dependencies()
    if not issues:
        print(f"✓ Dependencies valid")
    else:
        print(f"✗ Issues found: {issues}")
