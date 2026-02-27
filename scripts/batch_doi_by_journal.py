#!/usr/bin/env python3
"""
Batch DOI Assignment by Journal Pattern
========================================
Assigns DOIs to papers based on journal-specific DOI patterns.

Usage:
    python scripts/batch_doi_by_journal.py --analyze          # Show papers needing DOI by journal
    python scripts/batch_doi_by_journal.py --journal "AER"    # Process American Economic Review
    python scripts/batch_doi_by_journal.py --all              # Process all known journals (dry-run)
    python scripts/batch_doi_by_journal.py --all --execute    # Apply DOIs to BibTeX
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

BIB_FILE = Path("bibliography/bcm_master.bib")

# Journal DOI patterns - maps journal name variants to DOI construction function
JOURNAL_PATTERNS = {
    # American Economic Association journals
    "American Economic Review": {
        "aliases": ["American Economic Review", "AER"],
        "pattern": "10.1257/aer.{volume}.{issue}.{startpage}",
        "alt_pattern": "10.1257/{year_short}.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },
    "Journal of Economic Literature": {
        "aliases": ["Journal of Economic Literature", "JEL"],
        "pattern": "10.1257/jel.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },
    "Journal of Economic Perspectives": {
        "aliases": ["Journal of Economic Perspectives", "JEP"],
        "pattern": "10.1257/jep.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },

    # Oxford/JSTOR journals
    "Quarterly Journal of Economics": {
        "aliases": ["Quarterly Journal of Economics", "QJE"],
        "pattern": "10.1162/003355{year_short}{issue}{startpage_padded}",
        "alt_pattern": "10.1093/qje/qj{suffix}",
        "requires": ["volume", "issue", "pages", "year"]
    },
    "Review of Economic Studies": {
        "aliases": ["Review of Economic Studies", "RES", "REStud"],
        "pattern": "10.1093/restud/rd{suffix}",
        "alt_pattern": "10.2307/{jstor_id}",
        "requires": ["volume", "pages"]
    },

    # University of Chicago Press
    "Journal of Political Economy": {
        "aliases": ["Journal of Political Economy", "JPE"],
        "pattern": "10.1086/{article_id}",
        "requires": ["volume", "pages"]
    },

    # Wiley/Econometric Society
    "Econometrica": {
        "aliases": ["Econometrica"],
        "pattern": "10.2307/{jstor_id}",
        "alt_pattern": "10.1111/1468-0262.{suffix}",
        "requires": ["volume", "pages"]
    },

    # Elsevier
    "Journal of Economic Behavior \\& Organization": {
        "aliases": ["Journal of Economic Behavior & Organization", "Journal of Economic Behavior \\& Organization", "JEBO"],
        "pattern": "10.1016/j.jebo.{year}.{month}.{article}",
        "alt_pattern": "10.1016/0167-2681({year_short}){volume}-{suffix}",
        "requires": ["volume", "year"]
    },
    "Games and Economic Behavior": {
        "aliases": ["Games and Economic Behavior", "GEB"],
        "pattern": "10.1016/j.geb.{year}.{month}.{article}",
        "requires": ["volume", "year"]
    },
    "Journal of Public Economics": {
        "aliases": ["Journal of Public Economics"],
        "pattern": "10.1016/j.jpubeco.{year}.{month}.{article}",
        "requires": ["volume", "year"]
    },

    # Science/Nature
    "Science": {
        "aliases": ["Science"],
        "pattern": "10.1126/science.{volume}.{issue}.{startpage}",
        "alt_pattern": "10.1126/science.{suffix}",
        "requires": ["volume", "issue", "pages"]
    },
    "Nature": {
        "aliases": ["Nature"],
        "pattern": "10.1038/{suffix}",
        "requires": ["volume", "pages"]
    },

    # INFORMS
    "Management Science": {
        "aliases": ["Management Science"],
        "pattern": "10.1287/mnsc.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },
    "Marketing Science": {
        "aliases": ["Marketing Science"],
        "pattern": "10.1287/mksc.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },

    # Springer
    "Experimental Economics": {
        "aliases": ["Experimental Economics"],
        "pattern": "10.1007/s10683-{suffix}",
        "requires": ["volume", "year"]
    },
    "Journal of Risk and Uncertainty": {
        "aliases": ["Journal of Risk and Uncertainty"],
        "pattern": "10.1007/BF{suffix}",
        "alt_pattern": "10.1007/s11166-{suffix}",
        "requires": ["volume", "year"]
    },

    # Annual Reviews
    "Annual Review of Economics": {
        "aliases": ["Annual Review of Economics"],
        "pattern": "10.1146/annurev-economics-{suffix}",
        "requires": ["volume", "year"]
    },
    "Annual Review of Psychology": {
        "aliases": ["Annual Review of Psychology"],
        "pattern": "10.1146/annurev.psych.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },

    # Psychology journals
    "Psychological Bulletin": {
        "aliases": ["Psychological Bulletin"],
        "pattern": "10.1037/0033-2909.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },
    "Psychological Review": {
        "aliases": ["Psychological Review"],
        "pattern": "10.1037/0033-295X.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },
    "Psychological Science": {
        "aliases": ["Psychological Science"],
        "pattern": "10.1177/{suffix}",
        "requires": ["volume", "year"]
    },
    "Journal of Behavioral Decision Making": {
        "aliases": ["Journal of Behavioral Decision Making"],
        "pattern": "10.1002/bdm.{article_id}",
        "requires": ["volume", "year"]
    },

    # Finance journals
    "Journal of Finance": {
        "aliases": ["Journal of Finance", "JF"],
        "pattern": "10.1111/j.1540-6261.{year}.{suffix}.x",
        "requires": ["volume", "year"]
    },
    "Journal of Financial Economics": {
        "aliases": ["Journal of Financial Economics", "JFE"],
        "pattern": "10.1016/j.jfineco.{year}.{month}.{article}",
        "requires": ["volume", "year"]
    },

    # European journals
    "European Economic Review": {
        "aliases": ["European Economic Review", "EER"],
        "pattern": "10.1016/j.euroecorev.{year}.{month}.{article}",
        "alt_pattern": "10.1016/S0014-2921({year_short}){suffix}",
        "requires": ["volume", "year"]
    },

    # Additional economics journals
    "Economic Journal": {
        "aliases": ["Economic Journal", "The Economic Journal"],
        "pattern": "10.1111/j.1468-0297.{year}.{suffix}.x",
        "alt_pattern": "10.2307/{jstor_id}",
        "requires": ["volume", "year"]
    },
    "Review of Economics and Statistics": {
        "aliases": ["Review of Economics and Statistics", "REStat"],
        "pattern": "10.1162/rest.{volume}.{issue}.{startpage}",
        "alt_pattern": "10.1162/003465{year_short}{volume}{startpage}",
        "requires": ["volume", "issue", "pages"]
    },
    "Journal of Economic Theory": {
        "aliases": ["Journal of Economic Theory", "JET"],
        "pattern": "10.1016/j.jet.{year}.{month}.{article}",
        "alt_pattern": "10.1006/jeth.{year}.{article}",
        "requires": ["volume", "year"]
    },
    "Economics Letters": {
        "aliases": ["Economics Letters"],
        "pattern": "10.1016/j.econlet.{year}.{month}.{article}",
        "alt_pattern": "10.1016/0165-1765({year_short}){suffix}",
        "requires": ["volume", "year"]
    },
    "RAND Journal of Economics": {
        "aliases": ["RAND Journal of Economics", "Bell Journal of Economics"],
        "pattern": "10.2307/{jstor_id}",
        "requires": ["volume", "pages"]
    },
    "Review of Financial Studies": {
        "aliases": ["Review of Financial Studies", "RFS"],
        "pattern": "10.1093/rfs/hh{suffix}",
        "requires": ["volume", "year"]
    },
    "Economic Inquiry": {
        "aliases": ["Economic Inquiry"],
        "pattern": "10.1111/j.1465-7295.{year}.{suffix}.x",
        "requires": ["volume", "year"]
    },
    "Journal of Labor Economics": {
        "aliases": ["Journal of Labor Economics", "JOLE"],
        "pattern": "10.1086/{article_id}",
        "requires": ["volume", "pages"]
    },
    "International Economic Review": {
        "aliases": ["International Economic Review", "IER"],
        "pattern": "10.1111/j.1468-2354.{year}.{suffix}.x",
        "requires": ["volume", "year"]
    },
    "Journal of Development Economics": {
        "aliases": ["Journal of Development Economics"],
        "pattern": "10.1016/j.jdeveco.{year}.{month}.{article}",
        "requires": ["volume", "year"]
    },
    "Journal of Economic Growth": {
        "aliases": ["Journal of Economic Growth"],
        "pattern": "10.1007/s10887-{suffix}",
        "requires": ["volume", "year"]
    },
    "Brookings Papers on Economic Activity": {
        "aliases": ["Brookings Papers on Economic Activity", "BPEA"],
        "pattern": "10.2307/{jstor_id}",
        "requires": ["volume", "year"]
    },
    "Journal of Law, Economics, and Organization": {
        "aliases": ["Journal of Law, Economics, and Organization", "JLEO"],
        "pattern": "10.1093/jleo/ew{suffix}",
        "requires": ["volume", "year"]
    },

    # Psychology journals (additional)
    "Journal of Personality and Social Psychology": {
        "aliases": ["Journal of Personality and Social Psychology", "JPSP"],
        "pattern": "10.1037/0022-3514.{volume}.{issue}.{startpage}",
        "requires": ["volume", "issue", "pages"]
    },
    "Journal of Economic Psychology": {
        "aliases": ["Journal of Economic Psychology"],
        "pattern": "10.1016/j.joep.{year}.{month}.{article}",
        "alt_pattern": "10.1016/0167-4870({year_short}){suffix}",
        "requires": ["volume", "year"]
    },
    "Organizational Behavior and Human Decision Processes": {
        "aliases": ["Organizational Behavior and Human Decision Processes", "OBHDP"],
        "pattern": "10.1016/j.obhdp.{year}.{month}.{article}",
        "alt_pattern": "10.1006/obhd.{year}.{article}",
        "requires": ["volume", "year"]
    },
    "Judgment and Decision Making": {
        "aliases": ["Judgment and Decision Making", "JDM"],
        "pattern": "10.1017/S1930297500{suffix}",
        "requires": ["volume", "year"]
    },
    "Evolution and Human Behavior": {
        "aliases": ["Evolution and Human Behavior"],
        "pattern": "10.1016/j.evolhumbehav.{year}.{month}.{article}",
        "requires": ["volume", "year"]
    },
    "Journal of the European Economic Association": {
        "aliases": ["Journal of the European Economic Association", "JEEA"],
        "pattern": "10.1093/jeea/jv{suffix}",
        "requires": ["volume", "year"]
    },
}


@dataclass
class Paper:
    key: str
    title: str = ""
    author: str = ""
    year: str = ""
    journal: str = ""
    volume: str = ""
    number: str = ""  # issue
    pages: str = ""
    doi: Optional[str] = None
    entry_text: str = ""
    line_start: int = 0

    @property
    def startpage(self) -> str:
        if self.pages and '--' in self.pages:
            return self.pages.split('--')[0]
        elif self.pages and '-' in self.pages:
            return self.pages.split('-')[0]
        return self.pages

    @property
    def year_short(self) -> str:
        return self.year[-2:] if len(self.year) >= 2 else self.year

    @property
    def startpage_padded(self) -> str:
        sp = self.startpage
        return sp.zfill(4) if sp else ""


def parse_bibtex() -> Dict[str, Paper]:
    """Parse BibTeX file and extract paper metadata."""
    content = BIB_FILE.read_text()
    papers = {}

    # Match each entry with position
    pattern = r'@\w+\{([^,]+),\s*(.*?)(?=\n@|\Z)'
    for match in re.finditer(pattern, content, re.DOTALL):
        key = match.group(1)
        entry = match.group(2)

        paper = Paper(key=key, entry_text=entry, line_start=match.start())

        # Extract fields
        for field, attr in [('title', 'title'), ('author', 'author'), ('year', 'year'),
                           ('journal', 'journal'), ('volume', 'volume'),
                           ('number', 'number'), ('pages', 'pages')]:
            field_match = re.search(rf'{field}\s*=\s*\{{([^}}]+)\}}', entry, re.IGNORECASE)
            if field_match:
                setattr(paper, attr, field_match.group(1).strip())

        # Check for existing DOI
        doi_match = re.search(r'doi\s*=\s*\{([^}]+)\}', entry, re.IGNORECASE)
        if doi_match:
            doi_val = doi_match.group(1).strip()
            if doi_val.lower() not in ('null', ''):
                paper.doi = doi_val

        papers[key] = paper

    return papers


def normalize_journal(journal: str) -> Optional[str]:
    """Find the canonical journal name from aliases."""
    journal_lower = journal.lower().strip()

    for canonical, config in JOURNAL_PATTERNS.items():
        for alias in config["aliases"]:
            if alias.lower() == journal_lower:
                return canonical
    return None


def can_generate_doi(paper: Paper, journal_config: dict) -> Tuple[bool, str]:
    """Check if we have enough info to generate DOI."""
    required = journal_config.get("requires", [])
    missing = []

    if "volume" in required and not paper.volume:
        missing.append("volume")
    if "issue" in required and not paper.number:
        missing.append("number/issue")
    if "pages" in required and not paper.pages:
        missing.append("pages")
    if "year" in required and not paper.year:
        missing.append("year")

    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "OK"


def generate_doi_candidates(paper: Paper, journal_config: dict) -> List[str]:
    """Generate possible DOI candidates based on pattern."""
    candidates = []

    pattern = journal_config.get("pattern", "")
    alt_pattern = journal_config.get("alt_pattern", "")

    # Build substitution dict
    subs = {
        "volume": paper.volume,
        "issue": paper.number,
        "number": paper.number,
        "startpage": paper.startpage,
        "startpage_padded": paper.startpage_padded,
        "year": paper.year,
        "year_short": paper.year_short,
        "pages": paper.pages,
    }

    # Try main pattern
    try:
        doi = pattern.format(**subs)
        # Clean up any remaining placeholders
        if '{' not in doi:
            candidates.append(doi)
    except (KeyError, ValueError):
        pass

    # Try alt pattern
    if alt_pattern:
        try:
            doi = alt_pattern.format(**subs)
            if '{' not in doi:
                candidates.append(doi)
        except (KeyError, ValueError):
            pass

    return candidates


def analyze_papers(papers: Dict[str, Paper]):
    """Analyze papers by journal, showing DOI coverage."""
    print("=" * 80)
    print("PAPERS BY JOURNAL - DOI COVERAGE ANALYSIS")
    print("=" * 80)
    print()

    # Group by normalized journal
    by_journal: Dict[str, List[Paper]] = {}
    unmatched = []

    for paper in papers.values():
        if not paper.journal:
            continue

        canonical = normalize_journal(paper.journal)
        if canonical:
            if canonical not in by_journal:
                by_journal[canonical] = []
            by_journal[canonical].append(paper)
        else:
            unmatched.append(paper)

    # Sort by count
    sorted_journals = sorted(by_journal.items(), key=lambda x: -len(x[1]))

    print(f"{'Journal':<45} {'Total':>6} {'Has DOI':>8} {'Can Gen':>8} {'Missing':>8}")
    print("-" * 80)

    total_can_generate = 0

    for journal, journal_papers in sorted_journals:
        config = JOURNAL_PATTERNS.get(journal, {})

        has_doi = sum(1 for p in journal_papers if p.doi)
        can_gen = 0

        for p in journal_papers:
            if not p.doi:
                ok, _ = can_generate_doi(p, config)
                if ok:
                    can_gen += 1

        total_can_generate += can_gen
        missing = len(journal_papers) - has_doi - can_gen

        print(f"{journal:<45} {len(journal_papers):>6} {has_doi:>8} {can_gen:>8} {missing:>8}")

    print("-" * 80)
    print(f"{'TOTAL (known journals)':<45} {sum(len(p) for p in by_journal.values()):>6}")
    print(f"{'Unmatched journals':<45} {len(unmatched):>6}")
    print()
    print(f"🎯 Total DOIs that can be generated: {total_can_generate}")
    print()
    print("Run with --journal 'Journal Name' to process specific journal")
    print("Run with --all --execute to process all journals")


def process_journal(papers: Dict[str, Paper], journal_name: str, execute: bool = False) -> List[Tuple[str, str]]:
    """Process papers from a specific journal."""
    canonical = normalize_journal(journal_name)
    if not canonical:
        print(f"❌ Unknown journal: {journal_name}")
        return []

    config = JOURNAL_PATTERNS[canonical]

    print(f"\n{'=' * 60}")
    print(f"Processing: {canonical}")
    print(f"{'=' * 60}\n")

    # Filter papers for this journal
    journal_papers = [p for p in papers.values()
                      if p.journal and normalize_journal(p.journal) == canonical]

    # Filter to papers without DOI
    need_doi = [p for p in journal_papers if not p.doi]

    print(f"Total papers: {len(journal_papers)}")
    print(f"Already have DOI: {len(journal_papers) - len(need_doi)}")
    print(f"Need DOI: {len(need_doi)}")
    print()

    updates = []

    for paper in need_doi:
        can_gen, reason = can_generate_doi(paper, config)

        if can_gen:
            candidates = generate_doi_candidates(paper, config)
            if candidates:
                doi = candidates[0]  # Use first candidate
                print(f"✅ {paper.key}")
                print(f"   Title: {paper.title[:50]}...")
                print(f"   DOI: {doi}")
                updates.append((paper.key, doi))
        else:
            print(f"⚠️  {paper.key} - {reason}")

    print(f"\n{'=' * 60}")
    print(f"Can generate {len(updates)} DOIs")

    if execute and updates:
        print("\n💾 Applying updates to BibTeX...")
        apply_updates(updates)
        print(f"✅ Updated {len(updates)} entries")
    elif updates:
        print("\nRun with --execute to apply changes")

    return updates


def apply_updates(updates: List[Tuple[str, str]]):
    """Apply DOI updates to BibTeX file."""
    content = BIB_FILE.read_text()

    for key, doi in updates:
        # Find the entry
        entry_pattern = r'(@\w+\{' + re.escape(key) + r',.*?)(?=\n@|\Z)'
        match = re.search(entry_pattern, content, re.DOTALL)

        if not match:
            print(f"  ⚠️ Entry not found: {key}")
            continue

        entry = match.group(1)

        # Check if DOI already exists
        if re.search(r'doi\s*=', entry, re.IGNORECASE):
            # Update existing
            new_entry = re.sub(
                r'(doi\s*=\s*\{)[^}]*(})',
                rf'\g<1>{doi}\g<2>',
                entry,
                flags=re.IGNORECASE
            )
        else:
            # Add DOI before ebf_ fields or at end
            if 'ebf_reference_count' in entry:
                new_entry = re.sub(
                    r'(,\s*\n\s*)(ebf_reference_count)',
                    rf',\n  doi = {{{doi}}},\n  \g<2>',
                    entry
                )
            else:
                # Add before closing brace
                new_entry = re.sub(
                    r'(\s*)\}$',
                    rf',\n  doi = {{{doi}}}\n}}',
                    entry
                )

        content = content.replace(entry, new_entry)

    BIB_FILE.write_text(content)


def process_all_journals(papers: Dict[str, Paper], execute: bool = False):
    """Process all known journals."""
    print("=" * 80)
    print("BATCH DOI GENERATION - ALL JOURNALS")
    print("=" * 80)

    all_updates = []

    for journal_name in JOURNAL_PATTERNS.keys():
        updates = process_journal(papers, journal_name, execute=False)
        all_updates.extend(updates)

    print("\n" + "=" * 80)
    print(f"TOTAL: {len(all_updates)} DOIs can be generated")
    print("=" * 80)

    if execute and all_updates:
        print("\n💾 Applying all updates to BibTeX...")
        apply_updates(all_updates)
        print(f"✅ Updated {len(all_updates)} entries")
    elif all_updates:
        print("\nRun with --execute to apply all changes")

    return all_updates


def main():
    parser = argparse.ArgumentParser(description="Batch DOI Assignment by Journal")
    parser.add_argument('--analyze', action='store_true', help='Analyze DOI coverage by journal')
    parser.add_argument('--journal', type=str, help='Process specific journal')
    parser.add_argument('--all', action='store_true', help='Process all known journals')
    parser.add_argument('--execute', action='store_true', help='Apply changes to BibTeX')
    parser.add_argument('--list-journals', action='store_true', help='List known journals')

    args = parser.parse_args()

    if args.list_journals:
        print("Known journals and their DOI patterns:")
        print("=" * 60)
        for journal, config in JOURNAL_PATTERNS.items():
            print(f"\n{journal}")
            print(f"  Pattern: {config['pattern']}")
            print(f"  Requires: {', '.join(config['requires'])}")
        return

    papers = parse_bibtex()

    if args.analyze or (not args.journal and not args.all):
        analyze_papers(papers)
    elif args.journal:
        process_journal(papers, args.journal, args.execute)
    elif args.all:
        process_all_journals(papers, args.execute)


if __name__ == '__main__':
    main()
