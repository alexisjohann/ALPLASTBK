#!/usr/bin/env python3
"""Add final batch of ISBNs."""

from pathlib import Path

# Final batch of ISBNs
FINAL_ISBNS = {
    # Anthropology and ethnography
    "gavron2000kibbutz": "978-0742503441",
    "graeber2011debt": "978-1612191294",
    "lee1979kung": "978-0521295611",
    "malinowski1922argonauts": "978-0881330847",
    "marlowe2010hadza": "978-0520253421",
    "kraybill2001riddle": "978-0801867712",
    "heilman1992defenders": "978-0520204478",
    "spiro1970kibbutz": "978-0674505308",
    "kehlbodrogi1988kizilbas": "978-3922968740",
    "melikoff1998hadji": "978-9004108264",
    "shankland2003alevis": "978-0700716791",
    "soekefeld2008struggling": "978-1845456535",

    # Behavioral and decision making
    "gneezy2020field": "978-1610393119",
    "gneezy2004doing": "978-0199246137",
    "schwartz2004paradox": "978-0060005696",
    "halpern2015": "978-0753556559",
    "service2014think": "978-0007522835",
    "stanovich2011": "978-0195341140",

    # Economics classics
    "pigou1920welfare": "978-1614270171",
    "ohlin1933interregional": "978-0674436014",
    "thunen1826isolierte": "978-3428035038",
    "mincer1974schooling": "978-0870142659",
    "spence1974market": "978-0674868809",

    # Game theory and mechanism design
    "klemperer2004auctions": "978-0691119250",
    "roth1982axiomatic": "978-3540115113",
    "roth1990twosided": "978-0521437882",
    "roth2015gets": "978-0544705289",
    "roth1995bargaining": "978-0691043517",
    "wilson1987game": "978-0521251051",
    "maynardsmith1982evolution": "978-0521288842",
    "weibull1995evolutionary": "978-0262731218",
    "hofbauer1998evolutionary": "978-0521625708",
    "topkis1998supermodularity": "978-0691032443",

    # Complexity and agent-based
    "holland1992adaptation": "978-0262581110",
    "holland1995hidden": "978-0201442304",
    "sornette2003crashes": "978-0691118505",
    "tesfatsion2006handbook": "978-0444512536",
    "arthur2014complexity": "978-0199334292",

    # Institutions and economic history
    "hall2001varieties": "978-0199247752",
    "hodgson2004": "978-0415323192",
    "vanhorn2009": "978-0521117999",
    "lavoie2014": "978-1847204837",

    # Psychology and sociology
    "harris1998nurture": "978-0684857077",
    "rosch1978principles": "978-0898591637",
    "triandis1995individualism": "978-0813318509",
    "hofstede2001cultures": "978-0803973244",
    "polanyi1966": "978-0226672984",

    # Health and behavior change
    "marlatt1985relapse": "978-0898628005",
    "prochaska1994changing": "978-0380725724",

    # Immigration
    "portes2006immigrant": "978-0520250413",
    "oliver_shapiro_2006_wealth": "978-0415951678",
    "shapiro_2004_hidden_cost": "978-0195181388",

    # Law and causation
    "hart1985causation": "978-0198254744",

    # Information economics
    "shapiro1999information": "978-0875848631",

    # Linguistics
    "halliday1985functional": "978-0340761670",
    "sinclair1975towards": "978-0194370271",

    # Business and leadership
    "kotter1996": "978-1422186435",
    "schor1998overspent": "978-0060977580",

    # Economic geography
    "moretti2012geography": "978-0544028050",
    "rosenthal2004evidence": "978-0444501752",

    # Goldin
    "goldin2008race": "978-0674028678",

    # Newer economics
    "niederle2021markets": "978-0691200569",
    "odonoghue2003selfawareness": "978-0226643700",

    # Economic theory
    "hurwicz1960optimality": "978-0804743518",
    "sargent1993bounded": "978-0198288695",

    # Statistics
    "robert2004monte": "978-0387212395",
    "ohagan2006uncertain": "978-0470029039",

    # More classics
    "laffont1993incentives": "978-0262621397",
    "zablocki1980alienation": "978-0029359600",
    "greiff2017microdynamapproach": "978-3030289447",
    "robins2004optimal": "978-0387004518",
    "stern2007economics": "978-0521700801",
    "heckman2006earnings": "978-0691121263",
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

        for db_key, isbn in FINAL_ISBNS.items():
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
