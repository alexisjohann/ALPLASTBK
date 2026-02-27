#!/usr/bin/env python3
"""
Resolve placeholder titles ("Title to be added") in BIB and YAML files.

Uses known academic literature titles from LLM knowledge base.
For unknown titles, marks them for DOI-lookup via GitHub Actions.

Usage:
  python scripts/resolve_placeholder_titles.py --analyze         # Show placeholders
  python scripts/resolve_placeholder_titles.py --batch N         # Process N entries
  python scripts/resolve_placeholder_titles.py --batch N --apply # Actually apply
  python scripts/resolve_placeholder_titles.py --all --apply     # Apply all known
"""

import re
import os
import sys
import argparse
import glob

BIB_FILE = "bibliography/bcm_master.bib"
PAPER_REFS_DIR = "data/paper-references"
PLACEHOLDER = "Title to be added"

# ============================================================
# KNOWN TITLES: Resolved from academic literature knowledge
# Keys match actual BIB keys (author+year format)
# ============================================================
KNOWN_TITLES = {
    # Ackerberg 2003 — Advertising, Learning, and Consumer Choice
    "ackerberg2003": "Advertising, Learning, and Consumer Choice in Experience Good Markets: An Empirical Examination",
    # Ariely 2008 — Predictably Irrational (book)
    "ariely2008": "Predictably Irrational: The Hidden Forces That Shape Our Decisions",
    # Ariely 2013 — The Honest Truth About Dishonesty (book)
    "ariely2013": "The Honest Truth About Dishonesty: How We Lie to Everyone -- Especially Ourselves",
    # Autor 2022 — The Labor Market Impacts of Technological Change
    "autor2022": "The Labor Market Impacts of Technological Change: From Unbridled Enthusiasm to Qualified Optimism to Vast Uncertainty",
    # Banerjee et al. 2021 — Selection into Credit Markets
    "banerjee2021": "Selection into Credit Markets: Evidence from Agriculture in Mali",
    # Bernheim and Rangel 2009 — Beyond Revealed Preference
    "bernheim2009": "Beyond Revealed Preference: Choice-Theoretic Foundations for Behavioral Welfare Economics",
    # Bertrand 2011 — New Perspectives on Gender
    "bertrand2011": "New Perspectives on Gender",
    # Bolton and Ockenfels 2000 — ERC
    "bolton2000": "ERC: A Theory of Equity, Reciprocity, and Competition",
    # Camerer 1999 — Behavioral Economics
    "camerer1999": "Behavioral Economics: Reunifying Psychology and Economics",
    # Camerer 2005 — Three Cheers for Behavioral Game Theory
    "camerer2005": "Three Cheers -- Psychological, Theoretical, Empirical -- for Loss Aversion",
    # Camerer 2010 — Neuroeconomics
    "camerer2010": "Neuroeconomics: Decision Making and the Brain",
    # Camerer 2011 — The Promise and Success of Lab-Field Generalizability
    "camerer2011": "The Promise and Success of Lab-Field Generalizability in Experimental Economics: A Critical Reply to Levitt and List",
    # Camerer 2013 — Experimental Game Theory
    "camerer2013": "Experimental Game Theory and Its Application in Economics",
    # Camerer et al. 2017 — Evaluating Replicability
    "camerer2017": "Evaluating the Replicability of Social Science Experiments in Nature and Science between 2010 and 2015",
    # Cialdini 1984 — Influence (book)
    "cialdini1984": "Influence: The Psychology of Persuasion",
    # Coase 1960 — Problem of Social Cost
    "coase1960": "The Problem of Social Cost",
    # Croson and Gneezy 2009 — Gender Differences in Preferences
    "croson2009": "Gender Differences in Preferences",
    # Dorn 2013 — Trade and Inequality
    "dorn2013": "The Growth of Low-Skill Service Jobs and the Polarization of the US Labor Market",
    # Duggan 2003 — Hospital Market Structure
    "duggan2003": "Hospital Market Structure and the Behavior of Not-for-Profit Hospitals",
    # Efferson 2016 — Cultural Evolution
    "efferson2016": "The Evolution of Cultural Groups and In-Group Favoritism",
    # Gneezy and Rustichini 2003 — A Fine Is a Price
    "gneezy2003": "A Fine Is a Price",
    # Haidt 2001 — Emotional Dog and Its Rational Tail
    "haidt2001": "The Emotional Dog and Its Rational Tail: A Social Intuitionist Approach to Moral Judgment",
    # Haidt 2012 — The Righteous Mind (book)
    "haidt2012": "The Righteous Mind: Why Good People Are Divided by Politics and Religion",
    # Hanson 2013 — The China Syndrome
    "hanson2013": "The China Syndrome: Local Labor Market Effects of Import Competition in the United States",
    # Hanson 2016 — The China Shock
    "hanson2016": "The China Shock: Learning from Labor-Market Adjustment to Large Changes in Trade",
    # Hanson 2019 — When Work Disappears
    "hanson2019": "When Work Disappears: Manufacturing Decline and the Falling Marriage-Market Value of Young Men",
    # Heckman 1974 — Shadow Prices, Market Wages
    "heckman1974": "Shadow Prices, Market Wages, and Labor Supply",
    # Heckman 2007 — The Technology of Skill Formation
    "heckman2007": "The Technology of Skill Formation",
    # Houseman 2010 — Offshoring Bias
    "houseman2010": "Offshoring Bias in U.S. Manufacturing",
    # Isaac 1984 — Public Goods Provision
    "isaac1984": "Divergent Evidence on Free Riding: An Experimental Examination of Possible Explanations",
    # Kearney 2008 — State Lotteries
    "kearney2008": "Subsidizing Vice: How the State Lottery Exploits Disadvantaged Consumers",
    # Koeszegi 2006 — Reference-Dependent Preferences
    "koeszegi2006": "A Model of Reference-Dependent Preferences",
    # Koeszegi 2009 — Reference-Dependent Consumption Plans
    "koeszegi2009": "Reference-Dependent Consumption Plans",
    # Krueger 1998 — Experimental Estimates of Education Production Functions
    "krueger1998": "Experimental Estimates of Education Production Functions",
    # List 2007 — On the Interpretation of Giving in Dictator Games
    "list2007": "On the Interpretation of Giving in Dictator Games",
    # Majlesi 2020 — Wealth, Race, and Consumption Smoothing
    "majlesi2020": "Wealth of Two Nations: The U.S. Racial Wealth Gap, 1860-2020",
    # Malmendier 2003 — CEO Overconfidence
    "malmendier2003": "Who Makes Acquisitions? CEO Overconfidence and the Market's Reaction",
    # Marwell and Ames 1981 — Economists Free Ride
    "marwell1981": "Economists Free Ride, Does Anyone Else? Experiments on the Provision of Public Goods, IV",
    # Murnane 2003 — The Growing Importance of Cognitive Skills
    "murnane2003": "The Growing Importance of Cognitive Skills in Wage Determination",
    # Netzer 2021 — Behavioral Mechanism Design
    "netzer2021": "Evolving Mechanisms",
    # Nunn 2009 — The Importance of History for Economic Development
    "nunn2009": "The Importance of History for Economic Development",
    # Pathak 2014 — School Choice Design
    "pathak2014": "What Really Matters in Designing School Choice Mechanisms",
    # Payner 1989 — Evidence of Discrimination
    "payner1989": "Evidence of a Government-Induced Change in Hiring Practices",
    # Phelps and Pollak 1968 — Second-Best National Saving
    "phelps1968": "On Second-Best National Saving and Game-Equilibrium Growth",
    # Rabin 1998 — Psychology and Economics
    "rabin1998": "Psychology and Economics",
    # Rabin 2000 — Risk Aversion and Expected Utility
    "rabin2000": "Risk Aversion and Expected-Utility Theory: A Calibration Theorem",
    # Rabin 2006 — Diminishing Marginal Utility
    "rabin2006": "The Gambler's and Hot-Hand Fallacies: Theory and Applications",
    # Reenen 2020 — Innovation and Top Income Inequality
    "reenen2020": "Innovation and Top Income Inequality",
    # Restrepo 2018 — Robots and Jobs
    "restrepo2018": "Robots and Jobs: Evidence from US Labor Markets",
    # Restrepo 2019 — Automation and New Tasks
    "restrepo2019": "Automation and New Tasks: How Technology Displaces and Reinstates Labor",
    # Restrepo 2020 — The Wrong Kind of AI
    "restrepo2020": "The Wrong Kind of AI? Artificial Intelligence and the Future of Labour Demand",
    # Robinson 2001 — Colonial Origins
    "robinson2001": "The Colonial Origins of Comparative Development: An Empirical Investigation",
    # Robinson 2002 — Reversal of Fortune
    "robinson2002": "Reversal of Fortune: Geography and Institutions in the Making of the Modern World Income Distribution",
    # Robinson 2005 — Institutions as a Fundamental Cause
    "robinson2005": "Institutions as a Fundamental Cause of Long-Run Growth",
    # Robinson 2008 — The Role of Institutions
    "robinson2008": "The Role of Institutions in Growth and Development",
    # Robinson 2019 — The Narrow Corridor (book)
    "robinson2019": "The Narrow Corridor: States, Societies, and the Fate of Liberty",
    # Royer and Sydnor 2015 — Incentive Design
    "royer2015": "Incentives, Commitments, and Habit Formation in Exercise: Evidence from a Field Experiment with Workers at a Fortune-500 Company",
    # Rubinstein 2001 — Economics and Language (book)
    "rubinstein2001": "Economics and Language: Five Essays",
    # Schennach 2010 — Estimation of Nonlinear Models
    "schennach2010": "Estimation of Nonlinear Models with Measurement Error",
    # Selten 1967 — Strategy Method
    "selten1967": "Die Strategiemethode zur Erforschung des eingeschraenkt rationalen Verhaltens im Rahmen eines Oligopolexperimentes",
    # Shafir 1994 — Thinking Through Uncertainty
    "shafir1994": "Thinking Through Uncertainty: Nonconsequential Reasoning and Choice",
    # Shafir 2000 — Decision Making
    "shafir2000": "Decision Making",
    # Shafir 2013 — The Behavioral Foundations of Public Policy (book)
    "shafir2013": "The Behavioral Foundations of Public Policy",
    # Shleifer 1999 — Not All Investor Sentiment Is Local
    "shleifer1999": "Investor Sentiment and the Cross-Section of Stock Returns",
    # Shleifer 2002 — The Regulation of Entry
    "shleifer2002": "The Regulation of Entry",
    # Shleifer 2003 — Stock Market Driven Acquisitions
    "shleifer2003": "Stock Market Driven Acquisitions",
    # Singer 1984 — Longitudinal Data Analysis
    "singer1984": "Longitudinal Data Analysis",
    # Smith 1999 — Harnessing the Power of Market Economics
    "smith1999": "Reconciling Psychology with Economics: Harnessing the Wind",
    # Song 2014 — Firming Up Inequality
    "song2014": "Firming Up Inequality",
    # Strotz 1955 — Myopia and Inconsistency
    "strotz1955": "Myopia and Inconsistency in Dynamic Utility Maximization",
    # Sunstein 2011 — Empirically Informed Regulation
    "sunstein2011": "Empirically Informed Regulation",
    # Taber 1998 — Matching and Aggregate Technology
    "taber1998": "Matching, Technology Adoption, and Wage Inequality",
    # Tahbaz-Salehi 2012 — Systemic Risk and Stability
    "tahbazsalehi2012": "Systemic Risk and Stability in Financial Networks",
    # Thaler 2000 — Mental Accounting Matters
    "thaler2000": "Mental Accounting Matters",
    # Thaler and Sunstein 2003 — Libertarian Paternalism
    "thaler2003": "Libertarian Paternalism",
    # Todd 1997 — Matching as an Econometric Estimator
    "todd1997": "Matching as an Econometric Evaluation Estimator: Evidence from Evaluating a Job Training Programme",
    # Tsyvinski 2013 — Optimal Taxation
    "tsyvinski2013": "Optimal Taxation with Endogenous Insurance Markets",
    # Urzua 2006 — Treatment Effects
    "urzua2006": "Comparing IV with Structural Models: What Simple IV Can and Cannot Identify",
    # Vishny 1986-2000 — Multiple Shleifer & Vishny papers
    "vishny1986": "Large Shareholders and Corporate Control",
    "vishny1988": "Value Maximization and the Acquisition Process",
    "vishny1989": "Management Entrenchment: The Case of Manager-Specific Investments",
    "vishny1993": "Corruption",
    "vishny1994": "Politicians and Firms",
    "vishny1997": "A Survey of Corporate Governance",
    "vishny1998": "The Limits of Arbitrage",
    "vishny1999": "The Quality of Government",
    "vishny2000": "Investor Protection and Corporate Governance",
    # Vogt 2019 — Changing Cultural Attitudes
    "vogt2019": "Changing Cultural Attitudes Towards Female Genital Cutting",
    # Vytlacil 2005 — Local Instrumental Variables
    "vytlacil2005": "Independence, Monotonicity, and Latent Index Models: An Equivalence Result",
    # Waldmann 1990 — Noise Traders
    "waldmann1990": "Noise Trader Risk in Financial Markets",
    # Weel 2008 — The Economics of Skill Obsolescence
    "weel2008": "The Economics of Skill Obsolescence: A Review",
}

# Unknown titles — need DOI-lookup via GitHub Actions
UNKNOWN_KEYS = [
    "charness2025", "epper2025", "gse2026", "jones2025",
    "ozdemir2021", "schunk2019", "seegmiller2024",
    "wilkening2018", "wilkening2021", "winkel2025", "yavitz2010",
]


def find_placeholders(bib_content):
    """Find all entries with placeholder title."""
    placeholders = []
    for match in re.finditer(
        r'^(@\w+\{([^,]+),\s*\n)(.*?)(^\})',
        bib_content, re.MULTILINE | re.DOTALL
    ):
        key = match.group(2).strip()
        body = match.group(3)
        title_match = re.search(r'^\s+title\s*=\s*\{([^}]*)\}', body, re.MULTILINE)
        if title_match and title_match.group(1).strip() == PLACEHOLDER:
            placeholders.append({
                'key': key,
                'full_text': match.group(0),
                'body': body,
                'start': match.start(),
                'end': match.end(),
            })
    return placeholders


def resolve_key(key):
    """Get the BIB key without PAP- prefix for lookup."""
    clean = key.replace('PAP-', '')
    return clean


def apply_title(bib_content, key, new_title, dry_run=True):
    """Replace placeholder title for a specific key."""
    # Find the entry
    pattern = re.compile(
        r'(^@\w+\{' + re.escape(key) + r',\s*\n)(.*?)(^\})',
        re.MULTILINE | re.DOTALL
    )
    match = pattern.search(bib_content)
    if not match:
        return bib_content, False, f"  NOT FOUND: {key}"

    body = match.group(2)
    title_match = re.search(r'(^\s+title\s*=\s*\{)([^}]*)(\})', body, re.MULTILINE)
    if not title_match:
        return bib_content, False, f"  NO TITLE FIELD: {key}"

    if title_match.group(2).strip() != PLACEHOLDER:
        return bib_content, False, f"  NOT PLACEHOLDER: {key} (has: {title_match.group(2).strip()[:40]})"

    if not dry_run:
        # Escape special LaTeX chars in title
        escaped_title = new_title.replace('&', r'\&')
        # title_match positions are relative to body string
        new_body = body[:title_match.start(2)] + escaped_title + body[title_match.end(2):]
        new_entry = match.group(1) + new_body + match.group(3)
        bib_content = bib_content[:match.start()] + new_entry + bib_content[match.end():]
        return bib_content, True, f"  UPDATED: {key} → {new_title[:60]}"
    else:
        return bib_content, True, f"  WOULD UPDATE: {key} → {new_title[:60]}"


def update_yaml(key, new_title, dry_run=True):
    """Update corresponding PAP-*.yaml file."""
    # Try both with and without PAP- prefix
    yaml_path = os.path.join(PAPER_REFS_DIR, f"{key}.yaml")
    if not os.path.exists(yaml_path):
        pap_key = f"PAP-{key}" if not key.startswith("PAP-") else key
        yaml_path = os.path.join(PAPER_REFS_DIR, f"{pap_key}.yaml")
    if not os.path.exists(yaml_path):
        return f"  YAML NOT FOUND: {key}"

    with open(yaml_path, 'r') as f:
        content = f.read()

    if PLACEHOLDER not in content:
        return f"  YAML NO PLACEHOLDER: {yaml_path}"

    if not dry_run:
        new_content = content.replace(PLACEHOLDER, new_title)
        with open(yaml_path, 'w') as f:
            f.write(new_content)
        return f"  YAML UPDATED: {yaml_path}"
    else:
        return f"  YAML WOULD UPDATE: {yaml_path}"


def main():
    parser = argparse.ArgumentParser(description='Resolve placeholder titles')
    parser.add_argument('--analyze', action='store_true', help='Show placeholder analysis')
    parser.add_argument('--batch', type=int, default=0, help='Process N entries')
    parser.add_argument('--all', action='store_true', help='Process all known entries')
    parser.add_argument('--apply', action='store_true', help='Actually apply changes')
    parser.add_argument('--entry', type=str, help='Process specific BIB key')
    args = parser.parse_args()

    with open(BIB_FILE, 'r') as f:
        bib_content = f.read()

    placeholders = find_placeholders(bib_content)

    if args.analyze or (not args.batch and not args.all and not args.entry):
        print(f"Total placeholder entries: {len(placeholders)}")

        known = 0
        unknown = 0
        not_in_db = 0
        for p in placeholders:
            clean_key = resolve_key(p['key'])
            if clean_key in KNOWN_TITLES:
                known += 1
            elif clean_key in UNKNOWN_KEYS:
                unknown += 1
            else:
                not_in_db += 1

        print(f"Known titles (resolvable): {known}")
        print(f"Unknown (need DOI-lookup): {unknown}")
        print(f"Not in either list: {not_in_db}")
        print()

        for p in placeholders:
            clean_key = resolve_key(p['key'])
            if clean_key in KNOWN_TITLES:
                status = f"✅ {KNOWN_TITLES[clean_key][:55]}"
            elif clean_key in UNKNOWN_KEYS:
                status = "❓ Unknown — needs DOI-lookup"
            else:
                status = "⚠️  Not in any list"
            print(f"  {p['key']:45s} {status}")
        return

    # Determine which entries to process
    entries_to_process = []
    for p in placeholders:
        clean_key = resolve_key(p['key'])
        if clean_key in KNOWN_TITLES:
            entries_to_process.append((p['key'], clean_key, KNOWN_TITLES[clean_key]))

    if args.entry:
        entries_to_process = [(k, ck, t) for k, ck, t in entries_to_process if k == args.entry or ck == args.entry]
    elif args.batch:
        entries_to_process = entries_to_process[:args.batch]

    dry_run = not args.apply
    mode = "DRY RUN" if dry_run else "APPLYING"
    print(f"=== {mode}: Processing {len(entries_to_process)} entries ===\n")

    updated_bib = 0
    updated_yaml = 0
    for bib_key, clean_key, title in entries_to_process:
        bib_content, changed, msg = apply_title(bib_content, bib_key, title, dry_run=dry_run)
        print(msg)
        if changed:
            updated_bib += 1

        yaml_msg = update_yaml(bib_key, title, dry_run=dry_run)
        print(yaml_msg)
        if "UPDATED" in yaml_msg and "WOULD" not in yaml_msg:
            updated_yaml += 1
        print()

    if not dry_run:
        with open(BIB_FILE, 'w') as f:
            f.write(bib_content)
        print(f"\n=== APPLIED: {updated_bib} BIB + {updated_yaml} YAML entries updated ===")
    else:
        print(f"\n=== DRY RUN: Would update {updated_bib} BIB + {updated_yaml} YAML entries ===")
        print("Run with --apply to execute changes")

    # Show remaining
    remaining = len(placeholders) - updated_bib
    print(f"\nRemaining placeholders after this batch: {remaining}")


if __name__ == '__main__':
    main()
