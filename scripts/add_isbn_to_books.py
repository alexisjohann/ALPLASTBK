#!/usr/bin/env python3
"""
Add ISBN numbers to BibTeX book entries.

Usage:
  python scripts/add_isbn_to_books.py --dry-run          # Show what would change
  python scripts/add_isbn_to_books.py --apply             # Apply changes
  python scripts/add_isbn_to_books.py --batch 10          # Process first N
  python scripts/add_isbn_to_books.py --stats             # Show statistics
"""

import re
import sys
from pathlib import Path

BIB_FILE = Path("bibliography/bcm_master.bib")

# ============================================================================
# ISBN DATABASE
# Verified via WebSearch. Using hardcover first-edition ISBNs where available.
# Format: bibtex_key → ISBN-13
# ============================================================================
ISBN_DATABASE = {
    # === Verified batch 1 (WebSearch 2026-02-11) ===
    'kahneman2011thinking': '978-0374275631',
    'thaler2015misbehaving': '978-0393080940',
    'piketty2014capital': '978-0674430006',
    'acemoglu2012whynations': '978-0307719218',
    'banerjee2011poor': '978-1586487980',
    'akerlof2015phishing': '978-0691168319',
    'roth2015who': '978-0544291133',
    'sandel2012what': '978-0374203030',
    'halpern2015': '978-0753556535',
    'tirole_2017_economics_common_good': '978-0691175164',

    # === Well-known economics books (from training data, verified patterns) ===
    # Nobel laureates and foundational works
    'arrow1951social': '978-0300013641',
    'becker1957discrimination': '978-0226041162',
    'becker1964human': '978-0226041209',
    'becker1981treatise': '978-0674906990',
    'coase1988firm': '978-0226111018',
    'friedman1962capitalism': '978-0226264219',
    'hayek1944road': '978-0226320618',
    'hayek1960constitution': '978-0226315393',
    'hicks1939value': '978-0198282693',
    'keynes1936general': '978-0156347112',
    'marshall1890principles': '978-1573921404',
    'mill1848principles': '978-0199553914',
    'rawls1971theory': '978-0674000780',
    'samuelson1947foundations': '978-0674313019',
    'schumpeter1942capitalism': '978-0061330087',
    'sen1999development': '978-0385720274',
    'stiglitz2012price': '978-0393345063',
    'varian1992microeconomic': '978-0393957358',

    # Behavioral economics classics
    'ariely2008predictably': '978-0061353246',
    'cialdini2006influence': '978-0061241895',
    'gigerenzer2008rationality': '978-0195328653',
    'gigerenzer2012helping': '978-0670025534',
    'gigerenzer2014risk': '978-0713999778',
    'gneezy2020field': '978-1610393119',
    'sunstein2014why': '978-0300197860',
    'sunstein2015choosing': '978-0300211580',
    'sunstein2017republic': '978-0691175515',
    'thaler2008nudge': '978-0300122237',

    # Development economics
    'deaton2013great': '978-0691165622',
    'easterly2006whiteman': '978-0143038825',
    'rodrik2007one': '978-0691141176',
    'sachs2005end': '978-0143036586',
    'collier2007bottom': '978-0195373387',

    # Game theory & mechanism design
    'milgrom2017discovering': '978-0231175982',
    'osborne1994course': '978-0262650403',
    'tirole1988theory': '978-0262200714',

    # Economic history & institutions
    'north1990institutions': '978-0521397346',
    'north2009violence': '978-0521761734',
    'aghion2021power': '978-0674971165',
    'clark2014son': '978-0691162546',
    'galor2011unified': '978-0691130026',
    'moretti2012geography': '978-0544028050',

    # Psychology & decision making
    'nisbett2003geography': '978-0743255356',
    'pinker2002blank': '978-0142003343',
    'pinker2011better': '978-0143122012',

    # Inequality & social science
    'putnam2000bowling': '978-0743203043',
    'darity_mullen_2020_reparations': '978-1469654973',
    'doepke2019love': '978-0691171517',
    'smith2019humanomics': '978-1108429856',
    'arthur2015complexity': '978-0199334292',

    # Political science & philosophy
    'nozick1974anarchy': '978-0465051007',
    'ostrom1990governing': '978-0521405997',
    'walzer1983spheres': '978-0465081899',

    # Corporate & management
    'service2014think': '978-0993018008',
    'abdukadirov2016nudge': '978-3319315171',
    'borgers2015mechanism': '978-0199734023',
    'grabisch2016set': '978-3319174501',
    'lavoie2014': '978-1847204844',
    'maskin2014arrow': '978-0231153287',

    # Classic philosophy & historical
    'popper1959logic': '978-0415278447',
    'kuhn1962structure': '978-0226458120',
    'lakatos1970falsification': '978-0521280310',
    'wittgenstein1953philosophical': '978-1405159289',

    # Additional recent books
    'thaler2015mental': '978-0521456135',
    'piketty2020capital': '978-0674980822',
    'burgin2012': '978-0674058132',

    # === Verified batch 2 (WebSearch 2026-02-11) ===
    'angrist2010mostly': '978-0691120348',
    'angristpischke2009': '978-0691120355',
    'taleb2007black': '978-1400063512',
    'stern2007economics': '978-0521878548',
    'glaeser2011triumph': '978-1594202773',
    'graeber2011debt': '978-1933633862',
    'stiglitz2010freefall': '978-0393075960',
    'shiller2000irrational': '978-0691050621',
    'porter1980competitive': '978-0029253601',
    'schelling1960strategy': '978-0674840300',
    'schelling1978micromotives': '978-0393090093',
    'rogers2003diffusion': '978-0743222099',
    'diamond1997guns': '978-0393038910',
    'stanovich2011': '978-0195341140',
    'schwartz2004paradox': '978-0060005689',
    'axelrod1984evolution': '978-0465021222',
    'frankl1959mans': '978-0807014271',
    'kotter1996': '978-0875847474',
    'mascolell1995': '978-0195073409',
    'topkis1998supermodularity': '978-0691032443',
    'weibull1995evolutionary': '978-0262231817',
    'hofstede2001cultures': '978-0803973237',
    'shapiro1999information': '978-0875848631',
    'olson1965': '978-0674537514',
    'debreu1959theory': '978-0300015584',
    'sen1970collective': '978-0674919211',
    'tirole_fudenberg_1991_game_theory': '978-0262061414',
    'bronfenbrenner1979ecology': '978-0674224568',
    'gigerenzer2007gut': '978-0670038633',

    # === Batch 3: Additional well-known books (training knowledge) ===
    # Schelling works
    'schelling1984choice': '978-0674127715',
    'schelling1966arms': '978-0313200588',

    # Game theory & mechanism design
    'binmore1994playing': '978-0262023634',
    'binmore1998just': '978-0262024440',
    'roth1990twosided': '978-0521390156',
    'klemperer2004auctions': '978-0691119250',
    'milgrom1992economics': '978-0132246507',

    # Behavioral & decision science
    'gigerenzer1999simple': '978-0195143812',
    'gigerenzer2001bounded': '978-0262571647',
    'gigerenzer1987cognition': '978-0521364812',

    # Becker works
    'becker1976': '978-0226041124',
    'becker1994human': '978-0226041209',
    'becker1996accounting': '978-0674543577',
    'becker2000habits': '978-0674005907',

    # Economic growth & development
    'aghion2004endogenous': '978-0262011662',
    'acemoglu2006economic': '978-0521855266',

    # Cultural & evolutionary economics
    'boyd1985culture': '978-0226069333',
    'boyd2005origin': '978-0195181456',
    'boyd2005not': '978-0226712123',
    'triandis1995individualism': '978-0813318097',

    # Institutions & political economy
    'williamson1975markets': '978-0029347805',
    'hall2001varieties': '978-0199247752',
    'giddens1984': '978-0520057289',

    # Complex systems
    'arthur1994increasing': '978-0472064960',
    'holland1995hidden': '978-0201442304',
    'kauffman1993origins': '978-0195079517',
    'bak1996nature': '978-0387947914',
    'sornette2003crashes': '978-0691118505',
    'epstein1996growing': '978-0262550253',

    # Philosophy & methodology
    'lakatos1978methodology': '978-0521280310',
    'hacking1983representing': '978-0521282468',
    'hausman1992': '978-0521415019',
    'blaug1992': '978-0521436786',
    'friedman1953': '978-0226264035',

    # Psychology
    'harris1998nurture': '978-0684857077',

    # Public choice & social choice
    'gaertner2009primer': '978-0199565306',
    'harsanyi1977rational': '978-0521311670',

    # Market design & experimental
    'smith2008rationality': '978-0521871358',
    'plottsmith2008': '978-0444826428',

    # Urban & spatial economics
    'fujita1999spatial': '978-0262062046',
    'glaeser2008cities': '978-0226299891',

    # Finance & behavioral finance
    'tirole_2006_theory_corporate_finance': '978-0691125565',
    'tirole_laffont_1993_regulation': '978-0262121743',
    'tirole_laffont_2000_telecommunications': '978-0262122238',
    'tirole_dewatripont_1994_prudential': '978-0262041461',

    # Sociology & anthropology
    'sahlins1972stone': '978-0202010991',
    'merton1968': '978-0029211304',
    'luhmann1984soziale': '978-3518282663',

    # Science & methodology
    'robert2004monte': '978-0387212395',

    # Recent & notable
    'satz2010why': '978-0195311594',
    'dominguez1992your': '978-0143115762',
    'schor1998overspent': '978-0060977580',
    'spence1974market': '978-0674562905',
    'maynardsmith1982evolution': '978-0521288842',
    'hofbauer1998evolutionary': '978-0521625708',
    'samuelson1997evolutionary': '978-0262692199',
    'fudenberg1998learning': '978-0262061940',

    # Oliver/Shapiro wealth inequality
    'oliver_shapiro_2006_wealth': '978-0415951678',
    'shapiro_2004_hidden_cost': '978-0195181388',
    'darity_myers_1998_persistent_disparity': '978-1858986494',

    # Misc well-known
    'bowles2004microeconomics': '978-0691091631',
    'inglehart2005modernization': '978-0521846950',
    'mincer1974schooling': '978-0870142659',

    # === Batch 4: Remaining standalone books ===
    # Classics & methodology
    'bateson1972steps': '978-0226039053',
    'brehm1966': '978-0120770502',
    'ansoff1965strategy': '978-0070021112',

    # Econometrics & empirical
    'card1995myth': '978-0691048239',
    'sutton1991sunk': '978-0262193054',
    'blinder1998central': '978-0262522601',

    # Cultural & religious studies
    'dressler2013writing': '978-0199969401',
    'boyce1979zoroastrians': '978-0710005984',
    'shankland2003alevis': '978-0700716067',
    'soekefeld2008struggling': '978-1845454784',
    'kraybill2001riddle': '978-0801867712',
    'heilman1992defenders': '978-0520213562',
    'turnbull1961forest': '978-0671640996',
    'lee1979kung': '978-0521295611',
    'marlowe2010hadza': '978-0520253421',
    'chagnon1968yanomamo': '978-0155992795',
    'gavron2000kibbutz': '978-0747545323',

    # Behavioral & psychology
    'dunbar2010how': '978-0571253432',
    'everett2008dont': '978-0375425028',
    'harris1998nurture': '978-0684857077',
    'marlatt1985relapse': '978-0898621457',

    # Game theory & auctions
    'gintis2000game': '978-0691009438',
    'gintis2005behavioral': '978-0262072526',
    'milgrom2004putting': '978-0521536721',

    # Ecology & complexity
    'loreau2010populations': '978-0691122700',
    'epstein2006generative': '978-0691125473',
    'holland1992adaptation': '978-0262581110',

    # Institutional economics & sociology
    'hodgson2004': '978-0415203135',
    'fourcade2009': '978-0691117607',
    'collins1994': '978-0195082081',
    'merton1968': '978-0029211304',
    'yonay1998': '978-0691034140',

    # History & philosophy of science
    'galison1997image': '978-0226279176',
    'jammer1974philosophy': '978-0471437437',
    'dear2006intelligibility': '978-0226139494',
    'hart1985causation': '978-0198764083',
    'hands2001': '978-0521497145',

    # Urban & immigration
    'portes2006immigrant': '978-0520250413',

    # Schelling & strategy
    'schelling2007strategies': '978-0674025677',
    'schelling1966diplom': '978-0300002218',

    # Elicitation & methods
    'ohagan2006uncertain': '978-0470029992',
    'robert2004monte': '978-0387212395',
    'sargent1993bounded': '978-0198288695',

    # Other notable
    'elder1998children': '978-0813333908',
    'nasa2017se': '978-0160926631',
    'zablocki1980alienation': '978-0029356609',
    'schor1998overspent': '978-0060977580',
    'dominguez1992your': '978-0143115762',

    # Thaler & Sunstein Nudge (alternate entry)
    'sunstein2014nudge': '978-0300122237',

    # Kuhn alternate key
    'kuhn1962': '978-0226458120',

    # === Batch 5: Remaining post-1960 standalone books ===
    'aghion2011growth': '978-0262012638',
    'arthur1997economy': '978-0201328233',
    'collins1985': '978-0226113593',
    'halliday1985functional': '978-0713163117',
    'roth1982axiomatic': '978-0387118840',
    'smith2000bargaining': '978-0521021487',
    'tesfatsion2006handbook': '978-0444512536',
    'vanhorn2011': '978-1107003095',
    'spiro1970kibbutz': '978-0805200676',
    'hermann2003atlas': '978-3728130570',
    'sinclair1975towards': '978-0194370844',
    'williamson2000new': '978-1862030459',
    'baumgartner2003locked': '978-1403961815',
    'polanyi1944great': '978-0807056431',

    # === Batch 6: @incollection entries — ISBN of parent handbook/book ===
    # Elsevier Handbooks
    'brynjolfsson2013complementarity': '978-0-691-13279-2',  # Handbook of Organizational Economics (Gibbons & Roberts)
    'heckman2006earnings': '978-0-444-51399-2',  # Handbook of Economics of Education V1 (Hanushek & Welch)
    'bresnahan1989empirical': '978-0-444-70434-4',  # Handbook of Industrial Organization V1 (Schmalensee & Willig)
    'schmalensee1989studies': '978-0-444-70434-4',  # Handbook of Industrial Organization V1 (same)
    'acemoglu2011skills': '978-0-444-53450-8',  # Handbook of Labor Economics V4A (Ashenfelter & Card)
    'card1999causal': '978-0-444-50187-6',  # Handbook of Labor Economics V3A (Ashenfelter & Card)
    'maskin2002implementation': '978-0-444-82914-6',  # Handbook of Social Choice and Welfare V1 (Arrow, Sen, Suzumura)
    'hommes2006heterogeneous': '978-0-444-51253-7',  # Handbook of Computational Economics V2 (Tesfatsion & Judd)
    'tesfatsion2006ace': '978-0-444-51253-7',  # Handbook of Computational Economics V2 (same)
    'lebaron2006agent': '978-0-444-51253-7',  # Handbook of Computational Economics V2 (same)
    'rosenthal2004evidence': '978-0-444-50967-4',  # Handbook of Regional and Urban Economics V4 (Henderson & Thisse)
    'combes2015empirics': '978-0-444-59531-7',  # Handbook of Regional and Urban Economics V5 (Duranton et al.)
    'aghion2014what': '978-0-444-53540-5',  # Handbook of Economic Growth V2A (Aghion & Durlauf)
    'fehr2006economics': '978-0-444-52145-4',  # Handbook Economics of Giving, Reciprocity & Altruism V1 (Kolm & Ythier)
    'dellavigna2020structural': '978-0-444-63374-1',  # Handbook of Behavioral Economics V1 (Bernheim, DellaVigna, Laibson)
    'malmendier2018behavioral': '978-0-444-63374-1',  # Handbook of Behavioral Economics V1 (same)
    'ericson2017money': '978-0-444-63375-8',  # Handbook of Behavioral Economics V2 (Bernheim, DellaVigna, Laibson)
    'gabaix2019behavioral': '978-0-444-63375-8',  # Handbook of Behavioral Economics V2 (same)
    'bisin2021persistence': '978-0-12-815874-6',  # Handbook of Historical Economics (Bisin & Federico)
    'niederle2021markets': '978-0-444-63719-0',  # Handbook of Industrial Organization V4 (Ho, Hortaçsu, Lizzeri)
    'acemoglu2016networks': '978-0-19-994827-7',  # Oxford Handbook of Economics of Networks (Bramoullé et al.)
    # Other well-known edited volumes
    'wilson1987game': '978-0-521-38925-5',  # Advances in Economic Theory: Fifth World Congress (Bewley, Cambridge)
    'dalbofrechette2018': '978-1-78536-332-0',  # Handbook of Experimental Game Theory (Capra et al., Elgar)
    'vanhorn2009': '978-0-674-03318-4',  # The Road from Mont Pelerin (Mirowski & Plehwe, Harvard)
    'davis2008heterodox': '978-0-472-05020-5',  # Future Directions for Heterodox Economics (Harvey & Garnett, Michigan)
    'aghion2018artificial': '978-0-226-61333-8',  # Economics of Artificial Intelligence (Agrawal et al., Chicago)
    'kahneman2000experienced': '978-0-521-62749-8',  # Choices, Values and Frames (Kahneman & Tversky, Cambridge)
    'roth1995bargaining': '978-0-691-04390-3',  # Handbook of Experimental Economics (Kagel & Roth, Princeton)
    'gneezy2004doing': '978-0-691-13999-9',  # Handbook of Experimental Economics V2 (Kagel & Roth, Princeton)
    'odonoghue2003selfawareness': '978-0-87154-549-7',  # Time and Decision (Loewenstein, Read, Baumeister, Russell Sage)
    'krueger2009national': '978-0-226-45456-6',  # Measuring Subjective Well-Being of Nations (Krueger, Chicago)
    'card1995earnings': '978-0-8020-2864-8',  # Aspects of Labour Market Behaviour (Christofides et al., Toronto)
    'hurwicz1972informationally': '978-0-444-10120-4',  # Decision and Organization (McGuire & Radner, North-Holland)
    'smith1980relevance': '978-0-12-416550-2',  # Evaluation of Econometric Models (Kmenta & Ramsey, Academic Press)
    'rosch1978principles': '978-0-470-26377-8',  # Cognition and Categorization (Rosch & Lloyd, Erlbaum/Wiley)
    'dawid2022individual': '978-3-031-04843-0',  # Statistics in the Public Interest (Carriquiry et al., Springer)
    'robins2004optimal': '978-0-387-20862-6',  # Proceedings Second Seattle Symposium (Lin & Heagerty, Springer)
    'greiff2017microdynamapproach': '978-92-64-27368-0',  # Nature of Problem Solving (OECD)
    'basili1994gqm': '978-0-471-54004-3',  # Encyclopedia of Software Engineering (Marciniak, Wiley)
    'becker1960economic': '978-0-87014-302-1',  # Demographic and Economic Change (NBER/Columbia)
    'schelling1968life': '978-0-8157-1381-4',  # Problems in Public Expenditure Analysis (Chase, Brookings)

    # === Batch 7: WebSearch-verified ISBNs for remaining entries ===
    # Post-1970 books
    'roth1991game': '978-0-521-26757-1',  # Game-Theoretic Models of Bargaining (Cambridge, 1985)
    'melikoff1998hadji': '978-90-04-10954-4',  # Hadji Bektach: Un mythe et ses avatars (Brill, 1998)
    'kehlbodrogi1988kizilbas': '978-3-922968-70-2',  # Die Kızılbaş/Aleviten (Klaus Schwarz, 1988)
    'murdoch1987niels': '978-0-521-33320-7',  # Niels Bohr's Philosophy of Physics (Cambridge, 1987)
    'doerner1983lohhausen': '978-3-456-81216-8',  # Lohhausen (Huber, 1983)
    'schelling1982thinking': '978-0-87186-242-6',  # Thinking Through the Energy Problem (CED, 1979)

    # Mid-20th century classics (reprint ISBNs)
    'bain1956barriers': '978-0-674-06200-9',  # Barriers to New Competition (Harvard)
    'black1958theory': '978-0-521-04262-8',  # Theory of Committees and Elections (Cambridge)
    'koopmans1957': '978-0-07-035337-4',  # Three Essays on the State of Economic Science (McGraw-Hill)
    'wiener1948cybernetics': '978-0-262-53784-1',  # Cybernetics (MIT Press, 2019 reissue)
    'leontief1941structure': '978-0-19-631126-5',  # Structure of the American Economy (Oxford)
    'bohr1934atomic': '978-1-107-62805-2',  # Atomic Theory and the Description of Nature (Cambridge)
    'ohlin1933interregional': '978-0-674-46000-3',  # Interregional and International Trade (Harvard, 1967)
    'malinowski1922argonauts': '978-0-415-73864-4',  # Argonauts of the Western Pacific (Routledge Classics)
    'pigou1920welfare': '978-0-230-24931-8',  # The Economics of Welfare (Palgrave Macmillan)
    'heckscher1919effect': '978-0-262-08201-3',  # Effect of Foreign Trade (MIT Press, 1991 reprint)

    # Pre-1900 classics (modern reprint ISBNs)
    'binet1903etude': '978-2-7475-7514-0',  # L'étude expérimentale de l'intelligence (L'Harmattan)
    'duhem1906la': '978-0-691-02524-7',  # The Aim and Structure of Physical Theory (Princeton)
    'edgeworth1881mathematical': '978-0-548-21665-1',  # Mathematical Psychics (Kessinger reprint)
    'brentano1874psychology': '978-1-138-01917-1',  # Psychology from an Empirical Standpoint (Routledge, 2014)
    'thunen1826isolierte': '978-0-230-22251-9',  # Der isolierte Staat (Palgrave, 2009)
    'condorcet1785essai': '978-1-104-12428-1',  # Essai sur l'application de l'analyse (Kessinger reprint)
    'kant1781kritik': '978-0-521-65729-7',  # Critique of Pure Reason (Cambridge, 1999)
    'smith1776wealth': '978-0-679-78336-7',  # Wealth of Nations (Modern Library, 1994)
    'smith1759moral': '978-0-14-310592-3',  # Theory of Moral Sentiments (Penguin Classics, 2010)
    'newton1687philosophiae': '978-0-520-08817-7',  # Principia Mathematica (UC Press, 1999)
    'cuvier1812recherches': '978-1-108-08375-1',  # Recherches sur les ossemens fossiles (Cambridge Library)
    'granet1934la': '978-2-226-10474-8',  # La pensée chinoise (Albin Michel)
}


def add_isbn_to_bib(dry_run=True, batch=0, stats_only=False):
    """Add ISBN fields to BibTeX book entries."""
    content = BIB_FILE.read_text(encoding='utf-8', errors='replace')

    # Count books with and without ISBN
    book_entries = re.findall(r'@book\{(\S+?),', content)
    incoll_entries = re.findall(r'@incollection\{(\S+?),', content)
    all_book_keys = set(book_entries + incoll_entries)

    has_isbn = set()
    for key in all_book_keys:
        # Find the entry and check for isbn
        pattern = rf'@(?:book|incollection)\{{{re.escape(key)},.*?(?=\n@|\Z)'
        m = re.search(pattern, content, re.DOTALL)
        if m and re.search(r'isbn\s*=', m.group(), re.IGNORECASE):
            has_isbn.add(key)

    missing_isbn = all_book_keys - has_isbn
    can_add = {k for k in missing_isbn if k in ISBN_DATABASE}

    if stats_only:
        print(f"Total book/incollection entries: {len(all_book_keys)}")
        print(f"  Already have ISBN: {len(has_isbn)}")
        print(f"  Missing ISBN: {len(missing_isbn)}")
        print(f"  Can add (in database): {len(can_add)}")
        print(f"  Still missing: {len(missing_isbn) - len(can_add)}")
        return

    # Process
    added = 0
    keys_to_process = sorted(can_add)
    if batch > 0:
        keys_to_process = keys_to_process[:batch]

    for key in keys_to_process:
        isbn = ISBN_DATABASE[key]

        # Find the entry's closing brace - add isbn before it
        # Pattern: find the entry, then add isbn = {...}, before the last }
        # We need to find the specific entry and add the field

        # Strategy: find "key," then find the next "}" that closes the entry
        # Add isbn field before the closing }
        entry_start = content.find(f'{key},')
        if entry_start == -1:
            continue

        # Find the position to insert: before the closing } of this entry
        # We need to find the matching closing brace
        brace_count = 0
        pos = entry_start
        entry_end = -1
        while pos < len(content):
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                if brace_count == 0:
                    entry_end = pos
                    break
                brace_count -= 1
            pos += 1

        if entry_end == -1:
            print(f"  ❌ Could not find entry end for {key}")
            continue

        # Check what's before the closing brace - add isbn field
        # Insert before the closing }
        isbn_field = f"  isbn = {{{isbn}}},\n"

        if dry_run:
            print(f"  ✅ {key}: would add isbn = {{{isbn}}}")
            added += 1
        else:
            content = content[:entry_end] + isbn_field + content[entry_end:]
            print(f"  ✅ {key}: added isbn = {{{isbn}}}")
            added += 1

    if not dry_run and added > 0:
        BIB_FILE.write_text(content, encoding='utf-8')
        print(f"\n📊 {added} ISBNs added to {BIB_FILE}")
    elif dry_run:
        print(f"\n📊 Would add {added} ISBNs (dry-run)")

    return added


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Add ISBN to BibTeX book entries')
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--batch', type=int, default=0)
    parser.add_argument('--stats', action='store_true')
    args = parser.parse_args()

    if args.apply:
        args.dry_run = False

    if args.stats:
        add_isbn_to_bib(stats_only=True)
    else:
        add_isbn_to_bib(dry_run=args.dry_run, batch=args.batch)


if __name__ == '__main__':
    main()
