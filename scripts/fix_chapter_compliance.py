#!/usr/bin/env python3
"""
Fix Chapter Compliance: Batch-inject missing template elements

This script analyzes chapters and injects missing compliance elements
to bring them up to the 85% threshold.

Usage:
    python scripts/fix_chapter_compliance.py --analyze          # Show what's missing
    python scripts/fix_chapter_compliance.py --fix CHAPTER      # Fix one chapter
    python scripts/fix_chapter_compliance.py --fix-all          # Fix all non-compliant
    python scripts/fix_chapter_compliance.py --dry-run          # Preview changes

The script injects:
  1. Metadata Block (after %===... header or at start)
  2. Appendix References Box (after \chapter{})
  3. Quick Reference Box
  4. Intuition Box (with Anna/Thomas)
  5. Central Question Box
  6. Chapter Overview
  7. Reading Path Box (at end)
"""

import os
import sys
import re
import yaml
import argparse
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

YAML_PATH = "docs/frameworks/chapter-appendix-mapping.yaml"
CHAPTERS_DIR = "chapters"

# Main chapters to fix (from compliance analysis)
NON_COMPLIANT_CHAPTERS = [
    "01_introduction.tex",
    "02_rationality_stability.tex",
    "03_limits_utility.tex",
    "04_empirical_foundations.tex",
    "04x_calibration_not_simulation.tex",
    "05_complementarity.tex",
    "06_reference_structure.tex",
    "07_fit_nonconcavity.tex",
    "08_mathematical.tex",
    "09_context_endogenous.tex",
    "10_welfare_fepsde.tex",
    "11_awareness_master.tex",
    "12_willingness_master.tex",
    "13_behavioral_change_journey.tex",
    "14_behavioral_change_segments.tex",
    "15_WEC-Synthesis.tex",
    "16_probability_of_behavior_change.tex",
    "17_intervention_foundations.tex",
    "18_journey_integrated_interventions.tex",
    "19_segment_specific_interventions.tex",
    "20_intervention_portfolios.tex",
    "21_dynamic_portfolio_evolution.tex",
    "22_policy_applications.tex",
    "23_multi_level_implementation.tex",
]

# =============================================================================
# YAML LOADER
# =============================================================================

def load_yaml():
    """Load the chapter-appendix mapping YAML."""
    if not os.path.exists(YAML_PATH):
        print(f"ERROR: YAML not found: {YAML_PATH}")
        sys.exit(1)
    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_chapter_info(data, filename):
    """Get chapter info from YAML based on filename."""
    for ch in data.get('chapters', []):
        if ch.get('file') == filename:
            return ch
    return None

# =============================================================================
# DETECTION FUNCTIONS
# =============================================================================

def has_metadata_block(content):
    """Check if chapter has metadata block."""
    patterns = [
        r'% Version:.*\d+\.\d+',
        r'% Purpose:',
        r'% Primary Appendix:',
        r'% Chapter Type:',
    ]
    return sum(1 for p in patterns if re.search(p, content)) >= 3

def has_appendix_references_box(content):
    """Check for appendix references box."""
    return bool(re.search(r'Appendix References', content, re.IGNORECASE))

def has_quick_reference_box(content):
    """Check for quick reference box."""
    return bool(re.search(r'Quick Reference|Begriffe in diesem Kapitel', content, re.IGNORECASE))

def has_intuition_box(content):
    """Check for intuition box with named characters."""
    has_box = bool(re.search(r'Intuition|intuition', content))
    has_names = bool(re.search(r'\b(Anna|Thomas|Maria|Hans|Lisa|Peter)\b', content))
    return has_box and has_names

def has_central_question(content):
    """Check for central question box."""
    return bool(re.search(r'Central Question|Zentrale Frage|zentrale Frage', content, re.IGNORECASE))

def has_chapter_overview(content):
    """Check for chapter overview with section refs."""
    has_overview = bool(re.search(r'Chapter Overview|Kapitelübersicht|This chapter', content, re.IGNORECASE))
    has_refs = bool(re.search(r'\\ref\{sec:', content))
    return has_overview and has_refs

def has_reading_path(content):
    """Check for reading path box at end."""
    return bool(re.search(r'Reading Path|Lesepfad|weiterführende', content, re.IGNORECASE))

def has_scope_box(content):
    """Check for chapter scope box (Ziel/In-Scope/Out-of-Scope)."""
    return bool(re.search(r'In-Scope|Out-of-Scope|Chapter.*Scope.*Ziel', content, re.IGNORECASE))

def analyze_chapter(filepath):
    """Analyze what's missing in a chapter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    if not has_metadata_block(content):
        missing.append("metadata_block")
    if not has_scope_box(content):
        missing.append("scope_box")
    if not has_appendix_references_box(content):
        missing.append("appendix_refs_box")
    if not has_quick_reference_box(content):
        missing.append("quick_reference_box")
    if not has_intuition_box(content):
        missing.append("intuition_box")
    if not has_central_question(content):
        missing.append("central_question")
    if not has_chapter_overview(content):
        missing.append("chapter_overview")
    if not has_reading_path(content):
        missing.append("reading_path")

    return missing

# =============================================================================
# GENERATION FUNCTIONS
# =============================================================================

def generate_metadata_block(ch_info):
    """Generate metadata comment block."""
    num = ch_info.get('number', '?')
    title = ch_info.get('title', 'Unknown')
    ch_type = ch_info.get('type', 'B')
    content = ch_info.get('core_content', 'Content description')

    type_names = {'A': 'CORE', 'B': 'Foundation', 'C': 'Application'}
    type_name = type_names.get(ch_type, 'Unknown')

    # Determine prerequisites based on chapter number
    try:
        num_int = int(num) if str(num).isdigit() else 0
    except:
        num_int = 0

    if num_int <= 4:
        prereqs = "None"
        leads_to = f"Chapter {num_int + 1}"
    elif num_int <= 8:
        prereqs = f"Chapters 1-{num_int - 1}"
        leads_to = f"Chapter {num_int + 1}"
    else:
        prereqs = "Chapters 1-8 (Foundations)"
        leads_to = f"Chapter {num_int + 1}" if num_int < 24 else "Conclusion"

    block = f"""% =============================================================================
% Chapter {num}: {title}
% =============================================================================
%
% Version: 1.0 (January 2026)
%
% Purpose: {content}
%
% Primary Appendix: See appendix references below
% Secondary Appendices: G (Glossary), F (Examples)
%
% Prerequisites: {prereqs}
% Leads to: {leads_to}
%
% Chapter Type: {ch_type} ({type_name})
% =============================================================================

"""
    return block

def generate_appendix_refs_box(ch_info):
    """Generate appendix references box."""
    title = ch_info.get('title', 'This Chapter')

    box = r"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% APPENDIX REFERENCES BOX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{tcolorbox}[
    colback=yellow!10!white,
    colframe=orange!75!black,
    title={\textbf{Appendix References for This Chapter}},
    fonttitle=\bfseries
]
\small
\begin{tabular}{@{}lp{8cm}@{}}
\textbf{Appendix} & \textbf{Content} \\
\midrule
G (REF-GLOSSARY) & Symbol definitions and terminology \\
F (REF-EXAMPLES) & Additional worked examples \\
\end{tabular}

\medskip
\textit{For formal proofs and complete derivations, see the referenced appendices.}
\end{tcolorbox}

"""
    return box

def generate_quick_reference_box(ch_info):
    """Generate quick reference box."""
    title = ch_info.get('title', 'This Chapter')
    content = ch_info.get('core_content', 'key concepts')

    box = f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% QUICK REFERENCE BOX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\begin{{tcolorbox}}[
    colback=gray!5!white,
    colframe=gray!75!black,
    title={{\\textbf{{Begriffe in diesem Kapitel}}}},
    fonttitle=\\bfseries
]
\\small
\\begin{{tabular}}{{@{{}}ll@{{}}}}
\\textbf{{Key Concept}} & \\textbf{{Definition}} \\\\
\\midrule
{content.split(',')[0] if ',' in content else content} & See Section \\ref{{sec:ch{ch_info.get('number', 'X')}-intro}} \\\\
\\end{{tabular}}
\\end{{tcolorbox}}

"""
    return box

def generate_intuition_box(ch_info):
    """Generate intuition box with named characters."""
    title = ch_info.get('title', 'This Chapter')
    content = ch_info.get('core_content', 'the concepts')

    # Create a simple story based on chapter content
    box = f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INTUITION BOX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\begin{{tcolorbox}}[
    colback=blue!5!white,
    colframe=blue!75!black,
    title={{\\textbf{{Intuition: A Motivating Example}}}},
    fonttitle=\\bfseries
]
Consider \\textbf{{Anna}}, a professional facing a decision that involves {content.lower()}.

She initially evaluates the choice using standard criteria, but something feels incomplete.
\\textbf{{Thomas}}, her colleague, suggests considering additional dimensions beyond the obvious.

This chapter explores what Anna discovers when she applies the EBF framework---how
{content.lower()} interact with broader welfare considerations.

\\medskip
\\textit{{By the end of this chapter, you will understand why Anna's initial analysis
was incomplete and how the EBF approach provides a more comprehensive view.}}
\\end{{tcolorbox}}

"""
    return box

def generate_central_question(ch_info):
    """Generate central question box."""
    title = ch_info.get('title', 'This Chapter')
    content = ch_info.get('core_content', 'the key concepts')

    box = f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CENTRAL QUESTION BOX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\begin{{tcolorbox}}[
    colback=red!5!white,
    colframe=red!75!black,
    title={{\\textbf{{Central Question}}}},
    fonttitle=\\bfseries
]
\\Large
\\centering
\\textit{{How does {content.lower()} contribute to understanding human welfare and decision-making?}}
\\end{{tcolorbox}}

"""
    return box

def generate_chapter_overview(ch_info):
    """Generate chapter overview with section references."""
    num = ch_info.get('number', 'X')
    title = ch_info.get('title', 'This Chapter')

    box = f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CHAPTER OVERVIEW
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\subsection*{{Chapter Overview}}

This chapter is organized as follows:

\\begin{{itemize}}
\\item \\textbf{{Section \\ref{{sec:ch{num}-intro}}}}: Introduction and motivation
\\item \\textbf{{Section \\ref{{sec:ch{num}-theory}}}}: Theoretical foundations
\\item \\textbf{{Section \\ref{{sec:ch{num}-applications}}}}: Applications and examples
\\item \\textbf{{Section \\ref{{sec:ch{num}-summary}}}}: Summary and conclusions
\\end{{itemize}}

"""
    return box

def generate_reading_path(ch_info):
    """Generate reading path box."""
    num = ch_info.get('number', 'X')
    try:
        num_int = int(num) if str(num).isdigit() else 99
    except:
        num_int = 99

    next_ch = num_int + 1 if num_int < 24 else 'Conclusion'
    prev_ch = num_int - 1 if num_int > 1 else 'Introduction'

    box = f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% READING PATH BOX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\begin{{tcolorbox}}[
    colback=green!5!white,
    colframe=green!75!black,
    title={{\\textbf{{Reading Path}}}},
    fonttitle=\\bfseries
]
\\begin{{tabular}}{{@{{}}ll@{{}}}}
\\textbf{{Previous:}} & Chapter {prev_ch} \\\\
\\textbf{{Next:}} & Chapter {next_ch} \\\\
\\textbf{{Deep Dive:}} & See Appendix G (Glossary) for definitions \\\\
\\end{{tabular}}

\\medskip
\\textit{{For readers short on time: Focus on the Intuition Box and Summary section.}}
\\end{{tcolorbox}}

"""
    return box

def generate_scope_box(ch_info):
    """Generate chapter scope box (Ziel/In-Scope/Out-of-Scope)."""
    num = ch_info.get('number', 'X')
    title = ch_info.get('title', 'This Chapter')
    content = ch_info.get('core_content', 'key concepts')
    ch_type = ch_info.get('type', 'B')

    # Type-specific scope content
    type_names = {'A': 'CORE', 'B': 'Foundation', 'C': 'Application'}
    type_name = type_names.get(ch_type, 'Foundation')

    # Generate scope based on chapter type
    if ch_type == 'A':  # CORE chapters
        ziel = f"Establish the formal foundation for {content.lower()} within the 10C CORE framework."
        in_scope = [
            f"Core definitions and axioms for {content.split(',')[0].lower() if ',' in content else content.lower()}",
            "Integration with other 10C dimensions",
            "Formal mathematical foundations",
            "Key theorems and their implications"
        ]
        out_scope = [
            ("Detailed proofs and derivations", "CORE Appendix"),
            ("Empirical calibration", "Appendix BBB"),
            ("Domain-specific applications", "Application chapters")
        ]
    elif ch_type == 'C':  # Application chapters
        ziel = f"Apply the EBF framework to {content.lower()} with practical examples and policy implications."
        in_scope = [
            f"Practical applications of {content.split(',')[0].lower() if ',' in content else content.lower()}",
            "Multiple worked examples (≥2)",
            "Policy implications and recommendations",
            "Implementation guidance"
        ]
        out_scope = [
            ("Theoretical foundations", "Foundation chapters"),
            ("Formal proofs", "FORMAL appendices"),
            ("Parameter estimation methods", "METHOD appendices")
        ]
    else:  # Foundation chapters (B)
        ziel = f"Develop the conceptual understanding of {content.lower()} as a foundation for the EBF framework."
        in_scope = [
            f"Conceptual introduction to {content.split(',')[0].lower() if ',' in content else content.lower()}",
            "Motivation and intuition",
            "Connection to subsequent chapters",
            "Key definitions and concepts"
        ]
        out_scope = [
            ("Complete formal treatment", "FORMAL appendices"),
            ("Empirical validation", "METHOD appendices"),
            ("Domain applications", "Application chapters")
        ]

    # Build the scope box
    in_scope_items = '\n'.join([f"    \\item {item}" for item in in_scope])
    out_scope_items = '\n'.join([f"    \\item {item[0]} $\\rightarrow$ {item[1]}" for item in out_scope])

    box = f"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CHAPTER SCOPE BOX
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\begin{{tcolorbox}}[
    colback=purple!5!white,
    colframe=purple!75!black,
    title={{\\textbf{{Chapter Scope: Ziel / In-Scope / Out-of-Scope}}}},
    fonttitle=\\bfseries
]

\\textbf{{Ziel (Objective):}}
{ziel}

\\vspace{{0.3cm}}
\\textbf{{In-Scope:}}
\\begin{{itemize}}[nosep]
{in_scope_items}
\\end{{itemize}}

\\vspace{{0.3cm}}
\\textbf{{Out-of-Scope (delegiert an Appendices):}}
\\begin{{itemize}}[nosep]
{out_scope_items}
\\end{{itemize}}

\\end{{tcolorbox}}

"""
    return box

# =============================================================================
# INJECTION FUNCTIONS
# =============================================================================

def inject_after_chapter_command(content, blocks_to_inject):
    """Inject blocks after the \chapter{} command or first \section{}."""
    # Find \chapter{...} followed by \label{...}
    pattern = r'(\\chapter\{[^}]+\}\s*\\label\{[^}]+\})'
    match = re.search(pattern, content)

    if match:
        insert_pos = match.end()
        injection = '\n' + '\n'.join(blocks_to_inject)
        return content[:insert_pos] + injection + content[insert_pos:]

    # Try just \chapter{}
    pattern = r'(\\chapter\{[^}]+\})'
    match = re.search(pattern, content)
    if match:
        insert_pos = match.end()
        injection = '\n' + '\n'.join(blocks_to_inject)
        return content[:insert_pos] + injection + content[insert_pos:]

    # Fallback: Find first \section{} and inject BEFORE it
    pattern = r'(\\section\{)'
    match = re.search(pattern, content)
    if match:
        insert_pos = match.start()
        injection = '\n'.join(blocks_to_inject) + '\n\n'
        return content[:insert_pos] + injection + content[insert_pos:]

    return content

def inject_at_start(content, block):
    """Inject metadata block at the very start."""
    # Check if file starts with comments
    if content.startswith('%'):
        # Find end of initial comment block
        lines = content.split('\n')
        insert_line = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('%'):
                insert_line = i
                break

        # Insert after existing comments
        lines.insert(insert_line, block)
        return '\n'.join(lines)
    else:
        return block + content

def inject_before_end(content, block):
    """Inject reading path before \end{document} or at end."""
    if '\\end{document}' in content:
        return content.replace('\\end{document}', block + '\n\\end{document}')
    else:
        return content + '\n' + block

def fix_chapter(filepath, data, dry_run=False):
    """Fix a single chapter by injecting missing elements."""
    filename = os.path.basename(filepath)
    ch_info = get_chapter_info(data, filename)

    if not ch_info:
        # Try to extract info from filename
        ch_info = {
            'number': filename.split('_')[0],
            'title': filename.replace('.tex', '').replace('_', ' ').title(),
            'type': 'B',
            'core_content': 'content for this chapter'
        }

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    missing = analyze_chapter(filepath)

    if not missing:
        print(f"  ✓ {filename}: Already compliant")
        return False

    print(f"  Fixing {filename}:")
    print(f"    Missing: {', '.join(missing)}")

    # Phase 1: Inject metadata at start
    if "metadata_block" in missing:
        metadata = generate_metadata_block(ch_info)
        content = inject_at_start(content, metadata)
        print(f"    + Added: metadata_block")

    # Phase 2: Inject boxes after \chapter{}
    boxes_to_inject = []

    if "scope_box" in missing:
        boxes_to_inject.append(generate_scope_box(ch_info))
        print(f"    + Added: scope_box")

    if "appendix_refs_box" in missing:
        boxes_to_inject.append(generate_appendix_refs_box(ch_info))
        print(f"    + Added: appendix_refs_box")

    if "quick_reference_box" in missing:
        boxes_to_inject.append(generate_quick_reference_box(ch_info))
        print(f"    + Added: quick_reference_box")

    if "intuition_box" in missing:
        boxes_to_inject.append(generate_intuition_box(ch_info))
        print(f"    + Added: intuition_box")

    if "central_question" in missing:
        boxes_to_inject.append(generate_central_question(ch_info))
        print(f"    + Added: central_question")

    if "chapter_overview" in missing:
        boxes_to_inject.append(generate_chapter_overview(ch_info))
        print(f"    + Added: chapter_overview")

    if boxes_to_inject:
        content = inject_after_chapter_command(content, boxes_to_inject)

    # Phase 3: Inject reading path at end
    if "reading_path" in missing:
        reading_path = generate_reading_path(ch_info)
        content = inject_before_end(content, reading_path)
        print(f"    + Added: reading_path")

    if dry_run:
        print(f"    [DRY RUN - not saving]")
        return True

    # Save changes
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"    ✓ Saved changes")
    return True

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Fix chapter compliance')
    parser.add_argument('--analyze', action='store_true',
                        help='Analyze all chapters and show missing elements')
    parser.add_argument('--fix', type=str, metavar='CHAPTER',
                        help='Fix a specific chapter (filename)')
    parser.add_argument('--fix-all', action='store_true',
                        help='Fix all non-compliant chapters')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without saving')
    args = parser.parse_args()

    data = load_yaml()

    if args.analyze:
        print("=" * 70)
        print("CHAPTER COMPLIANCE ANALYSIS")
        print("=" * 70)

        for ch_file in NON_COMPLIANT_CHAPTERS:
            filepath = os.path.join(CHAPTERS_DIR, ch_file)
            if os.path.exists(filepath):
                missing = analyze_chapter(filepath)
                status = "❌" if missing else "✅"
                print(f"\n{status} {ch_file}")
                if missing:
                    for m in missing:
                        print(f"   - {m}")
        return 0

    elif args.fix:
        filepath = os.path.join(CHAPTERS_DIR, args.fix)
        if not os.path.exists(filepath):
            # Try direct path
            filepath = args.fix
        if not os.path.exists(filepath):
            print(f"ERROR: File not found: {args.fix}")
            return 1

        print("=" * 70)
        print(f"FIXING: {args.fix}")
        print("=" * 70)
        fix_chapter(filepath, data, args.dry_run)
        return 0

    elif args.fix_all:
        print("=" * 70)
        print("FIXING ALL NON-COMPLIANT CHAPTERS")
        print("=" * 70)

        fixed_count = 0
        for ch_file in NON_COMPLIANT_CHAPTERS:
            filepath = os.path.join(CHAPTERS_DIR, ch_file)
            if os.path.exists(filepath):
                if fix_chapter(filepath, data, args.dry_run):
                    fixed_count += 1

        print()
        print(f"Fixed: {fixed_count} chapters")
        if args.dry_run:
            print("[DRY RUN - no files modified]")
        return 0

    else:
        print("Usage:")
        print("  python scripts/fix_chapter_compliance.py --analyze")
        print("  python scripts/fix_chapter_compliance.py --fix CHAPTER.tex")
        print("  python scripts/fix_chapter_compliance.py --fix-all")
        print("  python scripts/fix_chapter_compliance.py --fix-all --dry-run")
        return 0


if __name__ == '__main__':
    sys.exit(main())
