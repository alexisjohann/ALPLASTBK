#!/usr/bin/env python3
"""
Complete Appendix-Chapter Link Mapping System
Purpose: Document ALL connections between appendices and chapters
Strategy: Create complete bidirectional reference map with audit trail

Usage:
    python scripts/map-all-appendix-chapter-links.py --scan
    python scripts/map-all-appendix-chapter-links.py --report
    python scripts/map-all-appendix-chapter-links.py --validate
    python scripts/map-all-appendix-chapter-links.py --export-yaml
"""

import os
import re
import json
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple

class AppendixChapterLinker:
    """Map all appendix-chapter connections with complete audit trail"""

    def __init__(self, repo_root="/home/user/complementarity-context-framework"):
        self.repo_root = Path(repo_root)
        self.appendices_dir = self.repo_root / "appendices"
        self.chapters_dir = self.repo_root / "chapters"
        self.docs_dir = self.repo_root / "docs"
        self.models_dir = self.repo_root / "models"

        self.mapping_dir = self.repo_root / "link-mapping"
        self.mapping_dir.mkdir(exist_ok=True)

        # Data structures
        self.appendix_to_chapters = defaultdict(set)      # Appendix A → [Ch 1, Ch 5, ...]
        self.chapter_to_appendices = defaultdict(set)     # Chapter 1 → [A, B, C, ...]
        self.reference_details = defaultdict(list)        # Complete reference metadata
        self.axiom_references = defaultdict(list)         # Appendix axioms → chapters
        self.theorem_references = defaultdict(list)       # Appendix theorems → chapters
        self.equation_references = defaultdict(list)      # Appendix equations → chapters

        # Patterns to search for
        self.patterns = [
            (r'Appendix\s+([A-Z]{1,3})\b(?:\s*\(([^)]+)\))?', 'text_reference'),
            (r'Appendix\s+([A-Z]{1,3})-([0-9A-Z]+)\b', 'axiom_reference'),
            (r'Theorem\s+([A-Z]{1,3})-T(\d+)', 'theorem_reference'),
            (r'Equation\s+\(([A-Z]{1,3})[.-](\d+)\)', 'equation_reference'),
            (r'\\ref{app:([a-z0-9\-]+)}', 'latex_ref'),
            (r'appendix{([A-Z]{1,3})}', 'latex_appendix'),
        ]

    def scan_appendix_files(self):
        """Document all appendices with metadata"""
        print("📋 Scanning appendix files...")

        appendix_metadata = {}

        for filepath in self.appendices_dir.glob("*.tex"):
            filename = filepath.name
            match = re.match(r'^([A-Z]{1,3})[_.]', filename)
            if not match:
                continue

            code = match.group(1)

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract category and title
            title_match = re.search(r'\\title{[^}]*?([A-Z]{1,3}):[^}]*?}', content)
            category_match = re.search(r'Category.*?([A-Z]+-[A-Z-]+)', content)

            appendix_metadata[code] = {
                'filename': filename,
                'path': str(filepath.relative_to(self.repo_root)),
                'size_lines': len(content.split('\n')),
                'title': title_match.group(1) if title_match else 'Unknown',
                'category': category_match.group(1) if category_match else 'Unknown',
            }

        report_file = self.mapping_dir / "appendix-metadata.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(appendix_metadata, f, indent=2)

        print(f"✅ Found {len(appendix_metadata)} appendices")
        print(f"📄 Saved to: {report_file}")
        return appendix_metadata

    def scan_chapter_files(self):
        """Document all chapters with metadata"""
        print("📋 Scanning chapter files...")

        chapter_metadata = {}

        for filepath in self.chapters_dir.glob("*.tex"):
            filename = filepath.name
            match = re.match(r'^(\d+)', filename)
            if not match:
                continue

            chapter_num = match.group(1)

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract title
            title_match = re.search(r'\\chapter{([^}]+)}|\\title{([^}]+)}', content)
            title = title_match.group(1) or title_match.group(2) if title_match else 'Unknown'

            chapter_metadata[chapter_num] = {
                'filename': filename,
                'path': str(filepath.relative_to(self.repo_root)),
                'size_lines': len(content.split('\n')),
                'title': title,
            }

        report_file = self.mapping_dir / "chapter-metadata.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_metadata, f, indent=2)

        print(f"✅ Found {len(chapter_metadata)} chapters")
        print(f"📄 Saved to: {report_file}")
        return chapter_metadata

    def scan_all_links(self):
        """Scan ALL files for appendix-chapter links"""
        print("🔍 Scanning all reference links...")

        all_links = []
        search_dirs = [
            (self.chapters_dir, 'chapter'),
            (self.appendices_dir, 'appendix'),
            (self.docs_dir, 'doc'),
            (self.models_dir, 'model'),
        ]

        for search_dir, file_type in search_dirs:
            if not search_dir.exists():
                continue

            filepaths = list(search_dir.rglob("*.tex")) + list(search_dir.rglob("*.md"))
            for filepath in filepaths:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Apply all patterns
                    for pattern, ref_type in self.patterns:
                        for match in re.finditer(pattern, content):
                            line_num = content[:match.start()].count('\n') + 1

                            link_info = {
                                'source_file': str(filepath.relative_to(self.repo_root)),
                                'source_type': file_type,
                                'line': line_num,
                                'reference_type': ref_type,
                                'match': match.group(0),
                                'timestamp': datetime.now().isoformat(),
                            }

                            # Extract code(s) from match groups
                            if ref_type == 'text_reference':
                                link_info['appendix_code'] = match.group(1)
                                link_info['context'] = match.group(2) or ''
                            elif ref_type == 'axiom_reference':
                                link_info['appendix_code'] = match.group(1)
                                link_info['axiom_id'] = match.group(2)
                            elif ref_type == 'theorem_reference':
                                link_info['appendix_code'] = match.group(1)
                                link_info['theorem_num'] = match.group(2)
                            elif ref_type in ['equation_reference', 'latex_ref']:
                                link_info['appendix_code'] = match.group(1)
                            elif ref_type == 'latex_appendix':
                                link_info['appendix_code'] = match.group(1)

                            all_links.append(link_info)

                            # Index by chapter/appendix
                            if file_type == 'chapter' and 'appendix_code' in link_info:
                                chapter_match = re.match(r'chapters/(\d+)', link_info['source_file'])
                                if chapter_match:
                                    chapter_num = chapter_match.group(1)
                                    self.chapter_to_appendices[chapter_num].add(link_info['appendix_code'])

                            if file_type == 'appendix' and 'appendix_code' in link_info:
                                source_match = re.match(r'appendices/([A-Z]{1,3})', link_info['source_file'])
                                if source_match:
                                    source_code = source_match.group(1)
                                    # Check if it's a cross-appendix reference
                                    if link_info['appendix_code'] != source_code:
                                        self.appendix_to_chapters[link_info['appendix_code']].add(source_code)

                except Exception as e:
                    print(f"  ⚠️  Error processing {filepath}: {e}")

        # Save all links
        links_file = self.mapping_dir / "all-links-detailed.json"
        with open(links_file, 'w', encoding='utf-8') as f:
            json.dump(all_links, f, indent=2, default=str)

        print(f"✅ Found {len(all_links)} reference links")
        print(f"📄 Saved to: {links_file}")
        return all_links

    def build_bidirectional_map(self):
        """Create complete bidirectional reference map"""
        print("🗺️  Building bidirectional reference map...")

        # Scan chapters → appendices
        for filepath in self.chapters_dir.glob("*.tex"):
            chapter_match = re.match(r'chapters/(\d+)', str(filepath.relative_to(self.repo_root)))
            if not chapter_match:
                continue

            chapter_num = chapter_match.group(1)

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Find all appendix references
            for pattern, ref_type in self.patterns:
                for match in re.finditer(pattern, content):
                    if 'appendix_code' in [g for g in match.groups() if g]:
                        # First group is usually the code
                        code = match.group(1)
                        if code and re.match(r'^[A-Z]{1,3}$', code):
                            self.chapter_to_appendices[chapter_num].add(code)

        # Scan appendices → appendices
        for filepath in self.appendices_dir.glob("*.tex"):
            source_match = re.match(r'appendices/([A-Z]{1,3})', str(filepath.relative_to(self.repo_root)))
            if not source_match:
                continue

            source_code = source_match.group(1)

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for pattern, ref_type in self.patterns:
                for match in re.finditer(pattern, content):
                    if match.group(1) and re.match(r'^[A-Z]{1,3}$', match.group(1)):
                        target_code = match.group(1)
                        if target_code != source_code:
                            self.appendix_to_chapters[source_code].add(target_code)

        # Export bidirectional map
        bidirectional_map = {
            'chapters_to_appendices': {k: list(v) for k, v in self.chapter_to_appendices.items()},
            'appendices_to_appendices': {k: list(v) for k, v in self.appendix_to_chapters.items()},
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_chapters': len(self.chapter_to_appendices),
                'total_appendices': len(self.appendix_to_chapters),
                'total_references': sum(len(v) for v in self.chapter_to_appendices.values()) +
                                   sum(len(v) for v in self.appendix_to_chapters.values()),
            }
        }

        map_file = self.mapping_dir / "bidirectional-reference-map.json"
        with open(map_file, 'w', encoding='utf-8') as f:
            json.dump(bidirectional_map, f, indent=2)

        print(f"✅ Built bidirectional map")
        print(f"   - Chapters: {bidirectional_map['summary']['total_chapters']}")
        print(f"   - Appendices: {bidirectional_map['summary']['total_appendices']}")
        print(f"   - Total references: {bidirectional_map['summary']['total_references']}")
        print(f"📄 Saved to: {map_file}")

        return bidirectional_map

    def generate_dependency_graph(self):
        """Generate dependency graph for visualization"""
        print("📊 Generating dependency graph...")

        # Create graph in DOT format
        dot_content = "digraph AppendixChapterDependencies {\n"
        dot_content += "  rankdir=LR;\n"
        dot_content += "  node [shape=box];\n\n"

        # Add nodes
        chapters = set()
        appendices = set()

        for ch, apps in self.chapter_to_appendices.items():
            chapters.add(f"Ch{ch}")
            for app in apps:
                appendices.add(app)
                dot_content += f"  Ch{ch} -> {app};\n"

        # Add cross-appendix references
        for app, targets in self.appendix_to_chapters.items():
            appendices.add(app)
            for target in targets:
                if target not in [a for a in appendices]:
                    appendices.add(target)
                dot_content += f"  {app} -> {target} [style=dashed];\n"

        dot_content += "}\n"

        dot_file = self.mapping_dir / "dependency-graph.dot"
        with open(dot_file, 'w', encoding='utf-8') as f:
            f.write(dot_content)

        print(f"✅ Generated dependency graph (Graphviz DOT format)")
        print(f"📄 Saved to: {dot_file}")
        print(f"   To visualize: dot -Tpng dependency-graph.dot -o dependency-graph.png")

        return dot_file

    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("📊 Generating summary report...")

        report = f"""# Complete Appendix-Chapter Link Mapping Report

**Generated:** {datetime.now().isoformat()}
**Status:** DOCUMENTATION PHASE

## Summary Statistics

### Chapters
- Total chapters: {len(self.chapter_to_appendices)}
- Chapters with appendix references: {len([c for c in self.chapter_to_appendices.values() if c])}
- Total chapter→appendix links: {sum(len(v) for v in self.chapter_to_appendices.values())}

### Appendices
- Total appendices with cross-references: {len(self.appendix_to_chapters)}
- Total appendix→appendix links: {sum(len(v) for v in self.appendix_to_chapters.values())}

### Total References
- All link types: {sum(len(v) for v in self.chapter_to_appendices.values()) + sum(len(v) for v in self.appendix_to_chapters.values())}

## Chapter → Appendix References

| Chapter | Appendices Referenced | Count |
|---------|----------------------|-------|
"""
        for chapter in sorted(self.chapter_to_appendices.keys()):
            appendices = sorted(self.chapter_to_appendices[chapter])
            report += f"| {chapter} | {', '.join(appendices)} | {len(appendices)} |\n"

        report += """
## Appendix → Appendix Cross-References

| Appendix | References | Count |
|----------|-----------|-------|
"""
        for app in sorted(self.appendix_to_chapters.keys()):
            targets = sorted(self.appendix_to_chapters[app])
            report += f"| {app} | {', '.join(targets)} | {len(targets)} |\n"

        report += """
## Files Generated

1. **appendix-metadata.json** - Complete appendix inventory with metadata
2. **chapter-metadata.json** - Complete chapter inventory with metadata
3. **all-links-detailed.json** - Every single reference link with context
4. **bidirectional-reference-map.json** - Chapter↔Appendix mapping
5. **dependency-graph.dot** - Graphviz visualization of dependencies
6. **LINK-MAPPING-COMPLETE.md** - This report

## Next Phase: Verification

Before any migration:
1. ✅ Review all reference types
2. ✅ Check for orphaned appendices (no references)
3. ✅ Check for circular dependencies
4. ✅ Validate axiom/theorem numbering
5. ✅ Create migration safety checks

## Migration Impact Analysis

**Questions to answer:**

1. **Axiom/Theorem Renaming:**
   - How many "Appendix AU-1", "Theorem AW-T5" references exist?
   - Can we automate these updates?

2. **Bidirectional Links:**
   - How many chapter→appendix links point to appendix→appendix links?
   - Risk: Chain breaks if one link fails

3. **Circular Dependencies:**
   - Do any appendices reference back to chapters that reference them?
   - Or appendix A → B → C → A?

4. **Hard-coded References:**
   - Are there any references in comments/documentation?
   - How many are regular text vs. LaTeX refs?

## Recommendation

**Do NOT migrate until:**
- ✅ All 4+ JSON reports reviewed
- ✅ All broken link risks identified
- ✅ Rollback plan in place
- ✅ Automated testing suite ready

**The 99.9% certainty point:**
- Scan reports are 100% accurate
- All migration paths documented
- All failure scenarios planned
"""

        report_file = self.mapping_dir / "LINK-MAPPING-COMPLETE.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ Generated summary report")
        print(f"📄 Saved to: {report_file}")

        return report

    def run_all_scans(self):
        """Execute all scans and generate complete mapping"""
        print("\n" + "="*80)
        print("COMPLETE APPENDIX-CHAPTER LINK MAPPING SYSTEM")
        print("="*80 + "\n")

        print("PHASE 1: DOCUMENT EXISTING STATE\n")

        appendix_meta = self.scan_appendix_files()
        print()
        chapter_meta = self.scan_chapter_files()
        print()
        all_links = self.scan_all_links()
        print()

        print("PHASE 2: BUILD REFERENCE MAP\n")

        bidirectional = self.build_bidirectional_map()
        print()
        graph_file = self.generate_dependency_graph()
        print()
        report = self.generate_summary_report()
        print()

        print("="*80)
        print("✅ MAPPING COMPLETE")
        print("="*80)
        print(f"\n📁 All output saved to: {self.mapping_dir}/")
        print(f"\nFiles created:")
        print(f"  1. appendix-metadata.json")
        print(f"  2. chapter-metadata.json")
        print(f"  3. all-links-detailed.json")
        print(f"  4. bidirectional-reference-map.json")
        print(f"  5. dependency-graph.dot")
        print(f"  6. LINK-MAPPING-COMPLETE.md")

        print(f"\n📊 Next Steps:")
        print(f"  1. Review LINK-MAPPING-COMPLETE.md")
        print(f"  2. Analyze bidirectional-reference-map.json")
        print(f"  3. Run verification checks")
        print(f"  4. Create migration test suite")
        print(f"  5. Execute migration when 99.9% ready\n")

def main():
    linker = AppendixChapterLinker()
    linker.run_all_scans()

if __name__ == '__main__':
    main()
