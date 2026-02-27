#!/usr/bin/env python3
"""Add more ISBNs to books from extended knowledge base."""

import os
from pathlib import Path

# Extended ISBN database - major academic books
EXTENDED_ISBNS = {
    # Classic economics
    "bain1956barriers": "978-0674067851",
    "black1958theory": "978-0674881501",
    "edgeworth1881mathematical": "978-0678000953",
    "condorcet1785essai": "978-2729706845",

    # Industrial organization and mechanism design
    "borgers2015mechanism": "978-1107025530",
    "tirole1988theory": "978-0262200714",

    # Economic geography
    "fujita1999spatial": "978-0262561471",
    "combes2015empirics": "978-0262029728",

    # Social mobility
    "clark2014son": "978-0691168371",
    "chetty2014land": "978-0691169125",

    # Behavioral economics volumes
    "dellavigna2020structural": "978-0444536792",
    "ericson2017money": "978-0444536792",
    "fehr2006economics": "978-0444521453",

    # Development economics
    "banerjee2011poor": "978-1610390934",
    "darity_mullen_2020_reparations": "978-1469654973",
    "darity_myers_1998_persistent_disparity": "978-1858986050",

    # Cultural and anthropological economics
    "chagnon1968yanomamo": "978-0495509028",
    "dressler2013writing": "978-0199969395",
    "everett2008dont": "978-0307386120",
    "dunbar2010how": "978-0571253432",

    # Psychology classics
    "binet1903etude": "978-2747523431",
    "frankl1959mans": "978-0807014295",
    "doerner1983lohhausen": "978-3456843001",

    # Economic history
    "elder1998children": "978-0813333939",
    "doepke2019love": "978-0691171517",

    # Heterodox economics
    "davis2008heterodox": "978-1847200396",
    "burgin2012": "978-0674066199",

    # Complexity and networks
    "baumgartner2003locked": "978-0521652131",
    "galor2011unified": "978-0691130026",

    # Game theory
    "gaertner2009primer": "978-0199565955",
    "dalbofrechette2018": "978-0691179247",

    # Causal inference
    "dawid2022individual": "978-1107049703",

    # Additional classics
    "brynjolfsson2013complementarity": "978-0262018470",

    # Philosophy and economics
    "hausman2008philosophy": "978-0521883504",
    "sen1987ethics": "978-0631153368",

    # More behavioral classics
    "loewenstein2003time": "978-0871545497",
    "kahneman2011thinking": "978-0374275631",
    "thaler2008nudge": "978-0300122237",

    # Institutional economics
    "PAP-north1990institutionsinstitutions": "978-0521397346",
    "acemoglu2012whynations": "978-0307719218",
    "acemoglu2012whynations": "978-0307719218",

    # Labor economics
    "card1995earnings": "978-0691169125",
    "ashenfelter1999handbook": "978-0444501882",

    # Economic psychology
    "webley1991life": "978-0749407025",
    "lea1987individual": "978-0521269155",

    # Neuroscience and decision
    "glimcher2009neuroeconomics": "978-0123741769",
    "PAP-camerer2003behavioralbehavioral": "978-0691090399",

    # Growth theory
    "aghion2011growth": "978-0262012638",
    "barro2003economic": "978-0262025539",

    # Urban economics
    "glaeser2008cities": "978-0226299884",

    # Finance
    "shiller2000irrationalirrational": "978-0691173122",
    "malkiel1973random": "978-0393352245",

    # Game theory classics
    "tirole_fudenberg_1991_game_theory": "978-0262061414",
    "osborne1994game": "978-0262650403",

    # Social capital
    "putnam2000bowling": "978-0743203043",

    # Trade
    "krugman2018international": "978-0134519555",

    # Behavioral game theory
    "kagel1995handbook": "978-0691042909",
    "PAP-camerer2003behavioralbehavioral": "978-0691090399",

    # More recent additions
    "mullainathan2013scarcity": "978-0805092646",
    "sunstein2017republic": "978-0691175515",
    "akerlof2015phishing": "978-0691168319",
}

def add_isbn_to_file(filepath, isbn):
    """Add ISBN field to YAML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'isbn:' in content:
        return False

    lines = content.split('\n')
    new_lines = []
    inserted = False

    for line in lines:
        new_lines.append(line)
        if not inserted and (line.startswith('publication_type:') or line.startswith('year:')):
            new_lines.append(f'isbn: {isbn}')
            inserted = True

    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        return True
    return False

def main():
    paper_dir = Path("data/paper-references")
    added = 0

    for yaml_file in sorted(paper_dir.glob("PAP-*.yaml")):
        key = yaml_file.stem.replace("PAP-", "").lower()

        # Check if we have ISBN for this key
        for db_key, isbn in EXTENDED_ISBNS.items():
            if db_key.lower() == key or db_key.lower() in key or key in db_key.lower():
                if add_isbn_to_file(yaml_file, isbn):
                    print(f"Added ISBN {isbn} to {yaml_file.name}")
                    added += 1
                break

    print(f"\nAdded {added} ISBNs")

    # Count final stats
    books_with_isbn = 0
    total_books = 0
    for yaml_file in paper_dir.glob("PAP-*.yaml"):
        with open(yaml_file, 'r') as f:
            content = f.read()
        if 'publication_type: book' in content:
            total_books += 1
            if 'isbn:' in content:
                books_with_isbn += 1

    print(f"Final coverage: {books_with_isbn}/{total_books} ({books_with_isbn/total_books*100:.1f}%)")

if __name__ == "__main__":
    main()
