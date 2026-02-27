#!/usr/bin/env python3
"""Assign JEP 2026 papers to specific LIT-Appendices and update BibTeX use_for.

Maps labor papers to LIT-CARD, demography/family to LIT-BECKER,
then runs sync_bib_to_lit.py to auto-insert.

Usage:
    python scripts/assign_jep2026_lit.py            # dry-run
    python scripts/assign_jep2026_lit.py --execute   # update BibTeX
"""

import argparse
import re

BIB_FILE = "bibliography/bcm_master.bib"

# Mapping: paper_key → additional LIT tags to add
LIT_ASSIGNMENTS = {
    'berger2026labor': ['LIT-CARD'],       # Labor market power
    'geruso2026likelihood': ['LIT-BECKER'], # Fertility/demography
    'gobbi2026family': ['LIT-BECKER'],      # Family institutions
    'johnson2026occupational': ['LIT-CARD'], # Occupational licensing
    'khanna2026asia': ['LIT-CARD'],         # Immigration/labor
    'postel2026asian': ['LIT-CARD'],        # Immigration history
    'prager2026antitrust': ['LIT-CARD'],    # Antitrust in labor
    'pritchett2026global': ['LIT-BECKER'],  # Global labor/demography
    'starr2026economics': ['LIT-CARD'],     # Noncompete/labor
    'taylor2026recommendations': ['LIT-OTHER'],  # Reading recommendations
    'weil2026continued': ['LIT-BECKER'],    # Fertility/living standards
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()

    with open(BIB_FILE, 'r') as f:
        content = f.read()

    updates = 0
    for key, new_lits in LIT_ASSIGNMENTS.items():
        # Find existing use_for
        pattern = rf'(@article\{{{key},.*?use_for = \{{)(.*?)(\}})'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            print(f"  SKIP {key}: not found in bib")
            continue

        current = match.group(2).strip()
        current_tags = [t.strip() for t in current.split(',')]

        # Add new LIT tags if not already present
        added = []
        for lit in new_lits:
            if lit not in current_tags:
                current_tags.append(lit)
                added.append(lit)

        if added:
            new_use_for = ', '.join(current_tags)
            content = re.sub(pattern, rf'\g<1>{new_use_for}\3', content, flags=re.DOTALL)
            updates += 1
            if args.execute:
                print(f"  UPDATE {key}: +{', '.join(added)}")
            else:
                print(f"  [DRY-RUN] {key}: +{', '.join(added)} → [{new_use_for}]")
        else:
            print(f"  OK {key}: already has {new_lits}")

    if args.execute and updates > 0:
        with open(BIB_FILE, 'w') as f:
            f.write(content)
        print(f"\nUpdated {updates} entries in {BIB_FILE}")
        print("Run: python scripts/sync_bib_to_lit.py --update  to sync to LaTeX")
    elif not args.execute:
        print(f"\nWould update {updates} entries. Use --execute.")


if __name__ == '__main__':
    main()
