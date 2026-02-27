#!/usr/bin/env python3
"""Find books without ISBN and add them from extended database."""

import os
import yaml
from pathlib import Path

# Extended ISBN database for common economics/behavioral science books
KNOWN_ISBNS = {
    # Handbook of Labor Economics volumes
    "card1999causal": "978-0444501882",  # Handbook of Labor Economics Vol 3A
    "card1995earnings": "978-0691169125",  # Labor Economics
    "ashenfelter1999handbook": "978-0444501882",
    "ashenfelter1986handbook": "978-0444878564",

    # Handbook of Industrial Organization
    "bresnahan1989empirical": "978-0444704344",
    "schmalensee1989handbook": "978-0444704344",

    # Handbook of Behavioral Economics
    "bernheim2018behavioral": "978-0444633897",
    "ericson2015handbook": "978-0444633897",

    # Psychology classics
    "brentano1874psychology": "978-0415106610",

    # Game theory and experimental
    "camerer2003behavioral": "978-0691090399",
    "kagel1995handbook": "978-0691042909",
    "plott2008handbook": "978-0444826428",

    # Decision making
    "kahneman1982judgment": "978-0521284141",
    "gilovich2002heuristics": "978-0521796798",
    "kahneman2000choices": "978-0521627498",

    # Behavioral economics classics
    "thaler1992winner": "978-0691019345",
    "thaler1994quasi": "978-0871541277",
    "thaler2015misbehaving": "978-0393352795",
    "sunstein2008nudge": "978-0300122237",
    "ariely2008predictably": "978-0061353239",

    # Social preferences and fairness
    "fehr2000fairness": "978-0262062046",
    "bowles2011cooperative": "978-0691151250",

    # Neuroeconomics
    "glimcher2009neuroeconomics": "978-0123741769",
    "glimcher2014neuroeconomics": "978-0124160088",

    # Economic psychology
    "webley1991life": "978-0749407025",
    "lea1987individual": "978-0521269155",

    # Bounded rationality
    "gigerenzer1999simple": "978-0195143812",
    "gigerenzer2001adaptive": "978-0195157000",
    "gigerenzer2007gut": "978-0143113768",

    # Institutional economics
    "north1990institutions": "978-0521397346",
    "williamson1985economic": "978-0029348208",
    "ostrom1990governing": "978-0521405997",

    # Public choice
    "buchanan1962calculus": "978-0865972186",
    "tullock1967toward": "978-0899501109",

    # Macroeconomics classics
    "keynes1936general": "978-0230004764",
    "friedman1963monetary": "978-0691003542",

    # Information economics
    "akerlof2015phishing": "978-0691168319",
    "stiglitz2001information": "978-0199255856",

    # Happiness economics
    "layard2005happiness": "978-0143037019",
    "frey2008happiness": "978-0262062770",

    # Health economics
    "culyer2000handbook": "978-0444504708",
    "pauly2011handbook": "978-0444535924",

    # Development economics
    "banerjee2011poor": "978-1610390934",
    "duflo2017economics": "978-1610397278",

    # Environmental economics
    "kolstad2000environmental": "978-0195119541",
    "tietenberg2000environmental": "978-0321348906",

    # Labor economics
    "borjas2020labor": "978-1260004724",
    "ehrenberg2016modern": "978-0134037158",

    # Industrial organization
    "tirole1988theory": "978-0262200714",
    "cabral2017introduction": "978-0262035941",

    # Finance
    "fama1976foundations": "978-0465024995",
    "shiller2000irrational": "978-0691173122",
    "malkiel1973random": "978-0393352245",

    # Microeconomics theory
    "varian2014intermediate": "978-0393919677",
    "mas1995microeconomic": "978-0195073409",

    # Econometrics
    "wooldridge2019introductory": "978-1337558860",
    "angrist2008mostly": "978-0691120355",
    "stock2019introduction": "978-0135161098",

    # Contracts and organizations
    "bolton2005contract": "978-0262025768",
    "milgrom1992economics": "978-0132246507",

    # Game theory
    "fudenberg1991game": "978-0262061414",
    "osborne1994game": "978-0262650403",

    # Social capital
    "putnam2000bowling": "978-0743203043",
    "coleman1990foundations": "978-0674312265",

    # Economic growth
    "aghion2009economics": "978-0262012638",
    "barro2003economic": "978-0262025539",

    # International trade
    "krugman2018international": "978-0134519555",
    "feenstra2017international": "978-1429278447",

    # Monetary policy
    "taylor1993discretion": "978-0521442367",
    "woodford2003interest": "978-0691010496",

    # Urban economics
    "glaeser2008cities": "978-0226299884",

    # Philosophy of economics
    "sen1987ethics": "978-0631153368",
    "hausman2008philosophy": "978-0521883504",

    # More behavioral classics
    "shiller2019narrative": "978-0691182292",
    "tversky1974judgment": "978-0521284141",
    "loewenstein2003time": "978-0871545497",

    # Economic history
    "mokyr2016culture": "978-0691180960",
    "allen2009british": "978-0521144186",
}

def load_yaml(filepath):
    """Load a YAML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        # If YAML parsing fails, try to extract just the key fields
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        data = {}
        for line in content.split('\n'):
            if line.startswith('publication_type:'):
                data['publication_type'] = line.split(':', 1)[1].strip()
            elif line.startswith('isbn:'):
                data['isbn'] = line.split(':', 1)[1].strip()
            elif line.startswith('title:'):
                data['title'] = line.split(':', 1)[1].strip().strip('"')
        return data if data else None

def save_yaml(filepath, data):
    """Save data to YAML file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def add_isbn_to_file(filepath, isbn):
    """Add ISBN field to YAML file without full parsing."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if ISBN already exists
    if 'isbn:' in content:
        return False

    # Find a good place to insert (after publication_type or year)
    lines = content.split('\n')
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and (line.startswith('publication_type:') or line.startswith('year:')):
            new_lines.append(f'isbn: {isbn}')
            inserted = True

    if not inserted:
        # Add after first few metadata lines
        for i, line in enumerate(lines):
            if i > 5 and not line.startswith('#') and ':' in line:
                new_lines = lines[:i+1] + [f'isbn: {isbn}'] + lines[i+1:]
                inserted = True
                break

    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        return True
    return False

def main():
    paper_dir = Path("data/paper-references")

    books_without_isbn = []
    books_with_isbn = 0
    total_books = 0
    added_isbns = 0

    for yaml_file in sorted(paper_dir.glob("PAP-*.yaml")):
        data = load_yaml(yaml_file)
        if not data:
            continue

        pub_type = data.get("publication_type", "")
        if pub_type not in ["book", "book_chapter"]:
            continue

        total_books += 1
        key = yaml_file.stem.replace("PAP-", "")

        if data.get("isbn"):
            books_with_isbn += 1
            continue

        # Try to find ISBN in our database
        key_lower = key.lower()
        isbn = None
        for db_key, db_isbn in KNOWN_ISBNS.items():
            if db_key.lower() == key_lower or db_key.lower() in key_lower or key_lower in db_key.lower():
                isbn = db_isbn
                break

        if isbn:
            if add_isbn_to_file(yaml_file, isbn):
                added_isbns += 1
                print(f"Added ISBN {isbn} to {yaml_file.name}")
        else:
            books_without_isbn.append((key, data.get("title", "Unknown")))

    print(f"\n=== Summary ===")
    print(f"Total books/chapters: {total_books}")
    print(f"Already had ISBN: {books_with_isbn}")
    print(f"Added ISBN: {added_isbns}")
    print(f"Still missing ISBN: {len(books_without_isbn)}")
    print(f"New coverage: {(books_with_isbn + added_isbns) / total_books * 100:.1f}%")

    if books_without_isbn:
        print(f"\nBooks still missing ISBN (first 30):")
        for key, title in books_without_isbn[:30]:
            print(f"  - {key}: {title[:60]}...")

if __name__ == "__main__":
    main()
