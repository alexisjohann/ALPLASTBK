#!/usr/bin/env python3
"""
Generate key_findings for papers without abstracts.

Uses the paper title to generate a structured key_finding entry.
This serves as a fallback when no abstract is available.

Schema-compliant with data/paper-sources.schema.yaml
"""

import re
import yaml
from pathlib import Path

YAML_DIR = Path("data/paper-references")

# Domain keywords mapping
DOMAIN_KEYWORDS = {
    "finance": ["financial", "money", "investment", "saving", "retirement", "pension",
                "bank", "credit", "debt", "wealth", "income", "price", "market", "stock"],
    "health": ["health", "medical", "disease", "patient", "treatment", "drug", "smoking",
               "obesity", "diet", "exercise", "mental", "addiction", "alcohol"],
    "sustainability": ["environment", "climate", "energy", "carbon", "green", "sustainable",
                       "pollution", "renewable", "conservation", "recycling"],
    "hr": ["employee", "worker", "workplace", "job", "career", "hiring", "wage", "labor",
           "productivity", "team", "management", "organization"],
    "social_policy": ["policy", "welfare", "government", "regulation", "tax", "public",
                      "poverty", "inequality", "redistribution", "voting"],
    "education": ["education", "school", "student", "learning", "teacher", "university",
                  "college", "training", "skill", "literacy"],
    "behavior": ["behavior", "decision", "choice", "preference", "bias", "heuristic",
                 "cognitive", "psychological", "experimental", "game", "cooperation",
                 "trust", "fairness", "reciprocity", "altruism", "punishment", "norm"]
}

# Stage keywords mapping
STAGE_KEYWORDS = {
    "awareness": ["awareness", "information", "knowledge", "attention", "salience",
                  "perception", "recognition", "understanding"],
    "contemplation": ["intention", "attitude", "belief", "consider", "evaluate",
                      "preference", "valuation", "willingness"],
    "preparation": ["plan", "goal", "commitment", "strategy", "preparation", "ready"],
    "action": ["action", "behavior", "choice", "decision", "implement", "adopt",
               "change", "response", "participation"],
    "maintenance": ["maintain", "sustain", "persist", "habit", "routine", "long-term",
                    "stable", "continue"],
    "termination": ["quit", "stop", "end", "terminate", "abandon", "exit"]
}

# FEPSDE dimension keywords
DIMENSION_KEYWORDS = {
    "F": ["financial", "monetary", "economic", "money", "cost", "benefit", "incentive",
          "price", "wage", "income", "wealth", "budget"],
    "E": ["emotion", "feeling", "affect", "mood", "anxiety", "fear", "happiness",
          "regret", "anticipation", "visceral"],
    "P": ["cognitive", "psychological", "mental", "thinking", "reasoning", "bias",
          "heuristic", "framing", "anchor", "reference", "prospect"],
    "S": ["social", "norm", "peer", "group", "cooperation", "trust", "fairness",
          "reciprocity", "reputation", "identity", "status", "altruism"],
    "D": ["development", "learning", "habit", "addiction", "time", "delay",
          "present", "future", "discount", "patience", "self-control"],
    "E2": ["environment", "context", "situation", "setting", "physical", "default",
           "architecture", "nudge", "frame"]
}


def detect_domain(title: str) -> str:
    """Detect primary domain from title."""
    title_lower = title.lower()
    scores = {}

    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in title_lower)
        if score > 0:
            scores[domain] = score

    if scores:
        return max(scores, key=scores.get)
    return "behavior"  # Default


def detect_stage(title: str) -> str:
    """Detect behavior change stage from title."""
    title_lower = title.lower()
    scores = {}

    for stage, keywords in STAGE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in title_lower)
        if score > 0:
            scores[stage] = score

    if scores:
        return max(scores, key=scores.get)
    return "action"  # Default


def detect_dimension(title: str) -> str:
    """Detect FEPSDE dimension from title."""
    title_lower = title.lower()
    scores = {}

    for dim, keywords in DIMENSION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in title_lower)
        if score > 0:
            scores[dim] = score

    if scores:
        return max(scores, key=scores.get)
    return "P"  # Default: Psychological


def generate_finding_text(title: str, author: str, year: str) -> str:
    """Generate a finding statement from the title."""
    # Clean title
    title = title.strip('"').strip("'")

    # Remove common suffixes
    title = re.sub(r'\s*\.\.\.$', '', title)

    # Generate finding based on title structure
    title_lower = title.lower()

    # Pattern: "X and Y" -> "Examines the relationship between X and Y"
    if " and " in title_lower:
        return f"Examines the relationship between key concepts in: {title}"

    # Pattern: "The Effect of X on Y" -> "Investigates how X affects Y"
    effect_match = re.search(r'effect[s]?\s+of\s+(.+?)\s+on\s+(.+)', title_lower)
    if effect_match:
        return f"Investigates the effect of {effect_match.group(1)} on {effect_match.group(2)}"

    # Pattern: Questions -> "Addresses the question of..."
    if "?" in title or title_lower.startswith(("why ", "how ", "what ", "when ", "do ")):
        return f"Addresses the research question: {title}"

    # Pattern: "A Theory of X" -> "Develops theoretical framework for X"
    theory_match = re.search(r'theory\s+of\s+(.+)', title_lower)
    if theory_match:
        return f"Develops theoretical framework for understanding {theory_match.group(1)}"

    # Pattern: "Evidence from X" -> "Provides empirical evidence from X"
    evidence_match = re.search(r'evidence\s+from\s+(.+)', title_lower)
    if evidence_match:
        return f"Provides empirical evidence from {evidence_match.group(1)}"

    # Default: Use title directly
    return f"Investigates: {title}"


def get_papers_without_abstract():
    """Find YAML files without abstracts."""
    papers = []

    for yaml_file in YAML_DIR.glob("PAP-*.yaml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if abstract exists
            if 'abstract:' not in content or 'abstract: null' in content:
                # Check if key_findings already exists
                if 'key_findings:' not in content:
                    # Extract basic info
                    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
                    author_match = re.search(r'^author:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
                    year_match = re.search(r'^year:\s*["\']?(\d+)["\']?\s*$', content, re.MULTILINE)

                    if title_match:
                        papers.append({
                            'file': yaml_file,
                            'title': title_match.group(1),
                            'author': author_match.group(1) if author_match else "Unknown",
                            'year': year_match.group(1) if year_match else "Unknown"
                        })
        except Exception as e:
            print(f"Error reading {yaml_file}: {e}")

    return papers


def add_key_findings(yaml_file: Path, key_findings: dict) -> bool:
    """Add key_findings to YAML file."""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find insertion point (before references: or at end)
        lines = content.split('\n')
        new_lines = []
        inserted = False

        for line in lines:
            # Insert before references section or migration_status
            if not inserted and (line.startswith('references:') or
                                  line.startswith('reference_count:') or
                                  line.startswith('migration_status:')):
                # Add key_findings block
                new_lines.append("")
                new_lines.append("# Auto-generated key_findings (no abstract available)")
                new_lines.append("key_findings:")
                new_lines.append(f"  finding: \"{key_findings['finding']}\"")
                new_lines.append(f"  domain: {key_findings['domain']}")
                new_lines.append(f"  stage: {key_findings['stage']}")
                new_lines.append(f"  primary_dimension: {key_findings['primary_dimension']}")
                new_lines.append(f"  auto_generated: true")
                new_lines.append("")
                inserted = True
            new_lines.append(line)

        # If not inserted, add at end
        if not inserted:
            new_lines.append("")
            new_lines.append("# Auto-generated key_findings (no abstract available)")
            new_lines.append("key_findings:")
            new_lines.append(f"  finding: \"{key_findings['finding']}\"")
            new_lines.append(f"  domain: {key_findings['domain']}")
            new_lines.append(f"  stage: {key_findings['stage']}")
            new_lines.append(f"  primary_dimension: {key_findings['primary_dimension']}")
            new_lines.append(f"  auto_generated: true")

        with open(yaml_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        return True
    except Exception as e:
        print(f"Error updating {yaml_file}: {e}")
        return False


def main():
    print("=" * 60)
    print("KEY_FINDINGS GENERATOR")
    print("=" * 60)
    print("\nGenerates structured key_findings for papers without abstracts.")
    print("Schema: data/paper-sources.schema.yaml (KeyFinding entity)")

    # Find papers without abstract or key_findings
    print("\n" + "-" * 60)
    print("Finding papers without abstract or key_findings...")
    papers = get_papers_without_abstract()
    print(f"Found {len(papers)} papers to process")

    if not papers:
        print("\nAll papers already have abstract or key_findings!")
        return

    # Process papers
    print("\n" + "-" * 60)
    print("Generating key_findings...")

    stats = {'success': 0, 'errors': 0}
    domain_counts = {}

    for paper in papers:
        title = paper['title']
        author = paper['author']
        year = paper['year']

        # Generate key_findings
        domain = detect_domain(title)
        stage = detect_stage(title)
        dimension = detect_dimension(title)
        finding = generate_finding_text(title, author, year)

        key_findings = {
            'finding': finding,
            'domain': domain,
            'stage': stage,
            'primary_dimension': dimension
        }

        if add_key_findings(paper['file'], key_findings):
            stats['success'] += 1
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
            print(f"  ✓ {paper['file'].name}: {domain}/{stage}/{dimension}")
        else:
            stats['errors'] += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nSuccessfully generated: {stats['success']}")
    print(f"Errors: {stats['errors']}")

    if domain_counts:
        print("\nBy domain:")
        for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
            print(f"  {domain:20}: {count}")

    print("\n✓ Generation complete!")


if __name__ == "__main__":
    main()
