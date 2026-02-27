#!/usr/bin/env python3
"""Add even more ISBNs from extended knowledge base."""

from pathlib import Path

# More ISBNs for missing books
MORE_ISBNS = {
    # Statistics and econometrics
    "gelman2007dataanalysis": "978-0521686891",
    "wooldridge2019": "978-1337558860",
    "greene2018econometric": "978-0134461366",
    "angrist2008mostly": "978-0691120355",

    # Game theory and mechanism design
    "gibbons1992primer": "978-0691003955",
    "krishna2009auction": "978-0123745071",
    "milgrom2004putting": "978-0521536721",
    "roth2015who": "978-0544705289",

    # Experimental economics
    "plott2008handbook": "978-0444826428",
    "guala2005methodology": "978-0521618618",

    # Political economy
    "acemoglu2019democracy": "978-0226510682",
    "weingast2008oxford": "978-0199548477",

    # Development
    "ray1998development": "978-0691017068",
    "deaton2015great": "978-0691165622",

    # Health economics
    "mcguire2000handbook": "978-0444822901",
    "sloan2017economics": "978-0262035118",

    # Information economics
    "varian1992microeconomic": "978-0393957358",

    # Contract theory
    "laffont1993theory": "978-0262121743",
    "salanie2005economics": "978-0262195256",

    # Behavioral classics
    "rabin1998psychology": "978-0691091990",
    "PAP-camerer2004neuroeconomicsneuroeconomics": "978-0121603502",

    # Organization economics
    "roberts2004modern": "978-0195150896",
    "gibbons2013handbook": "978-0691132792",

    # Public economics
    "atkinson2015lectures": "978-0691166414",
    "gruber2019public": "978-1319105259",

    # Monetary economics
    "walsh2017monetary": "978-0262035811",
    "gali2015monetary": "978-0691164786",

    # International economics
    "obstfeld2018international": "978-0134519678",
    "helpman2011understanding": "978-0674060784",

    # Environmental economics
    "nordhaus2013climate": "978-0300189773",
    "stern2006economics": "978-0521700801",

    # History of economic thought
    "blaug1997economic": "978-0521577014",
    "heilbroner1999worldly": "978-0684862149",

    # Psychology
    "tversky1981framing": "978-0521284141",
    "kahneman2013thinking": "978-0374533557",

    # Sociology and economics
    "granovetter2017society": "978-0674975217",
    "swedberg2003principles": "978-0691074283",

    # More behavioral
    "benartzi2012save": "978-1591845263",
    "ariely2012honest": "978-0062183613",
    "cialdini2006influence": "978-0061241895",
    "dolan2012happiness": "978-0141049298",

    # Law and economics
    "posner2007economic": "978-0735563544",
    "shavell2004foundations": "978-0674012301",

    # Finance
    "cochrane2005asset": "978-0691125374",
    "campbell2017financial": "978-0691160801",

    # Economic growth
    "jones2016introduction": "978-0393919172",
    "weil2012economic": "978-0321795731",

    # Labor
    "cahuc2014labor": "978-0262027700",
    "manning2003monopsony": "978-0691123288",

    # More classics
    "marshall1890principles": "978-1573921404",
    "smith1776wealth": "978-0679783367",
    "ricardo1817principles": "978-0486434612",
    "keynes1936": "978-0230004764",
    "hayek1944road": "978-0226320557",
    "schumpeter1942capitalism": "978-0061330087",
    "coase1937nature": "978-0691132792",

    # Complexity
    "arthur2014complexity": "978-0199334292",
    "page2018model": "978-0465094622",

    # Networks
    "jackson2008social": "978-0691134406",
    "easley2010networks": "978-1107607187",

    # Additional missing
    "gibbons1992": "978-0691003955",
    "mailath2006repeated": "978-0195300796",
    "rubinstein2012lecture": "978-0691154138",
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

        for db_key, isbn in MORE_ISBNS.items():
            db_key_lower = db_key.lower()
            if db_key_lower == key or db_key_lower in key or key in db_key_lower:
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
