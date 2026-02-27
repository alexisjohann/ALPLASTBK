#!/usr/bin/env python3
"""
bibtex_key_generator.py - SINGLE SOURCE OF TRUTH for canonical BibTeX key generation.

SSOT: docs/standards/bibtex-key-convention.md

Canonical format: {nachname}{jahr}{kurzwort}
Regex: ^[a-z]+\\d{4}[a-z]+$

Rules:
  R1: All lowercase ASCII (no accents, no uppercase)
  R2: No separators (no _, -, spaces)
  R3: Lastname = first author, letters only
  R4: Year = exactly 4 digits (publication year)
  R5: Kurzwort = 1 meaningful word from title (MANDATORY)
  R6: Disambiguation via longer/different kurzwort
  R7: Skip stop words when selecting kurzwort

This module is the ONLY place where key generation logic lives.
All other scripts MUST import from here.

Usage as library:
    from scripts.bibtex_key_generator import generate_canonical_key
    key = generate_canonical_key("Kahneman", "1979", "Prospect Theory")
    # -> "kahneman1979prospect"

Usage as CLI:
    python scripts/bibtex_key_generator.py "Kahneman" "1979" "Prospect Theory"
    python scripts/bibtex_key_generator.py --test
"""

import re
import sys
import unicodedata
from typing import Optional


# Canonical format regex
CANONICAL_PATTERN = re.compile(r'^[a-z]+\d{4}[a-z]+$')

# Stop words to skip when selecting kurzwort (from SSOT: bibtex-key-convention.md)
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'of', 'in', 'on', 'for', 'to', 'with',
    'from', 'by', 'as', 'at', 'about', 'into', 'toward', 'towards', 'beyond',
    'through', 'between', 'among', 'across', 'is', 'are', 'was', 'were',
    'do', 'does', 'did', 'can', 'could', 'will', 'would', 'shall', 'should',
    'may', 'might', 'how', 'what', 'when', 'where', 'why', 'who', 'which',
    'that', 'this', 'not', 'no', 'new', 'its', 'has', 'have', 'been', 'more',
    'some', 'all', 'but', 'than', 'too', 'very', 'just', 'also', 'only'
}


def normalize_to_ascii(text: str) -> str:
    """Convert accented characters to ASCII equivalents.

    Examples:
        Bénabou -> Benabou
        Müller -> Muller
        Straße -> Strasse
    """
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ñ': 'n', 'ç': 'c', 'ß': 'ss', 'ø': 'o', 'å': 'a',
        'æ': 'ae', 'œ': 'oe', 'ð': 'd', 'þ': 'th',
        'ý': 'y', 'ÿ': 'y',
    }
    result = text
    for char, replacement in replacements.items():
        result = result.replace(char, replacement)
        result = result.replace(char.upper(), replacement)

    # Fallback: NFKD decomposition for any remaining non-ASCII
    result = unicodedata.normalize('NFKD', result)
    result = result.encode('ascii', 'ignore').decode('ascii')
    return result


def extract_kurzwort(title: str) -> str:
    """Extract first meaningful word from title for use as kurzwort.

    Skips stop words and LaTeX commands. Returns lowercase.

    Examples:
        "Prospect Theory: An Analysis" -> "prospect"
        "A Theory of Fairness" -> "theory"
        "The Fox News Effect" -> "fox"
        "Does Level-k Behavior Imply..." -> "level"
    """
    if not title:
        return ''

    # Remove LaTeX commands and braces
    clean = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)
    clean = re.sub(r'[{}\\$]', '', clean)
    clean = normalize_to_ascii(clean)

    # Split into words
    words = re.findall(r'[a-zA-Z]+', clean)

    # First non-stopword with >= 3 chars
    for word in words:
        w_lower = word.lower()
        if w_lower not in STOP_WORDS and len(w_lower) >= 3:
            return w_lower

    # Fallback: first word >= 2 chars
    for word in words:
        if len(word) >= 2:
            return word.lower()

    return ''


def extract_first_author_lastname(author: str) -> str:
    """Extract first author's last name from various author formats.

    Handles:
        "Kahneman, Daniel and Tversky, Amos" -> "kahneman"
        "Daniel Kahneman" -> "kahneman"
        "Kahneman" -> "kahneman"
        "DellaVigna, Stefano" -> "dellavigna"
        "Bénabou, Roland" -> "benabou"

    Args:
        author: Author string in any common format.

    Returns:
        Lowercase ASCII last name of first author.
    """
    if not author:
        return 'unknown'

    # Get first author (split on " and ")
    first_author = author.split(' and ')[0].strip()

    # Handle "Last, First" format
    if ',' in first_author:
        lastname = first_author.split(',')[0].strip()
    else:
        # "First Last" format — last token is surname
        parts = first_author.strip().split()
        lastname = parts[-1] if parts else ''

    # Normalize: ASCII, lowercase, letters only
    lastname = normalize_to_ascii(lastname).lower()
    lastname = re.sub(r'[^a-z]', '', lastname)

    return lastname if lastname else 'unknown'


def generate_canonical_key(author: str, year: str, title: str) -> str:
    """Generate a canonical BibTeX key: {nachname}{jahr}{kurzwort}.

    This is the SINGLE SOURCE OF TRUTH for key generation.
    All scripts and the frontend MUST use this function.

    Args:
        author: Author string (any format: "Last, First", "First Last",
                "Last, First and Last2, First2", or just "Last")
        year: Publication year (4 digits). Falls back to "0000" if empty.
        title: Paper title (may contain LaTeX commands).

    Returns:
        Canonical key like "kahneman1979prospect".

    Examples:
        >>> generate_canonical_key("Kahneman, Daniel", "1979", "Prospect Theory")
        'kahneman1979prospect'
        >>> generate_canonical_key("Bénabou, Roland", "2003", "Democracies and Dictatorships")
        'benabou2003democracies'
        >>> generate_canonical_key("Allcott, Hunt and Rogers, Todd", "2014", "The Short-Run Effects")
        'allcott2014short'
    """
    lastname = extract_first_author_lastname(author)
    year = str(year).strip() if year else '0000'
    kurzwort = extract_kurzwort(title)

    if not kurzwort:
        kurzwort = 'unknown'

    # Validate year format
    if not re.match(r'^\d{4}$', year):
        year = '0000'

    return f"{lastname}{year}{kurzwort}"


def is_canonical(key: str) -> bool:
    """Check if a key matches the canonical format."""
    return bool(CANONICAL_PATTERN.match(key))


def to_pap_superkey(key: str) -> str:
    """Convert a BibTeX key to PAP-superkey format.

    Example: "kahneman1979prospect" -> "PAP-kahneman1979prospect"
    """
    return f"PAP-{key}"


def to_filename(key: str, extension: str = '.yaml') -> str:
    """Convert a BibTeX key to the canonical filename.

    Examples:
        to_filename("kahneman1979prospect", ".yaml") -> "PAP-kahneman1979prospect.yaml"
        to_filename("kahneman1979prospect", ".md") -> "PAP-kahneman1979prospect.md"
        to_filename("kahneman1979prospect", ".txt") -> "PAP-kahneman1979prospect.txt"
    """
    return f"PAP-{key}{extension}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run_tests():
    """Run built-in test cases to verify key generation consistency."""
    test_cases = [
        # (author, year, title, expected_key)
        ("Kahneman, Daniel", "1979", "Prospect Theory: An Analysis of Decision under Risk", "kahneman1979prospect"),
        ("Fehr, Ernst and Schmidt, Klaus M.", "1999", "A Theory of Fairness, Competition, and Cooperation", "fehr1999theory"),
        ("Bénabou, Roland", "2003", "Democracies and Dictatorships", "benabou2003democracies"),
        ("Thaler, Richard H. and Sunstein, Cass R.", "2008", "Nudge: Improving Decisions", "thaler2008nudge"),
        ("DellaVigna, Stefano and Kaplan, Ethan", "2007", "The Fox News Effect", "dellavigna2007fox"),
        ("Allcott, Hunt and Rogers, Todd", "2014", "The Short-Run and Long-Run Effects of Behavioral Interventions", "allcott2014short"),
        ("Akerlof, George A.", "1970", "The Market for Lemons", "akerlof1970market"),
        ("Müller, Hans", "2020", "Über die Straßen Europas", "muller2020uber"),
        ("Daniel Kahneman", "2011", "Thinking, Fast and Slow", "kahneman2011thinking"),
        ("OECD", "2017", "PISA Results in Focus", "oecd2017pisa"),
        # Edge cases
        ("", "2020", "Some Paper Title", "unknown2020paper"),
        ("Fehr, Ernst", "", "Inequality Aversion", "fehr0000inequality"),
        ("Fehr, Ernst", "2026", "", "fehr2026unknown"),
        # Multi-author
        ("Ichniowski, Casey and Shaw, Kathryn and Prennushi, Giovanna", "1997", "The Effects of Human Resource Management Practices", "ichniowski1997effects"),
        # LaTeX in title
        ("Arrow, Kenneth", "1954", "Existence of an {Equilibrium} for a Competitive Economy", "arrow1954existence"),
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("  BIBTEX KEY GENERATOR — TEST SUITE")
    print("  SSOT: docs/standards/bibtex-key-convention.md")
    print("=" * 70)

    for author, year, title, expected in test_cases:
        result = generate_canonical_key(author, year, title)
        ok = result == expected
        if ok:
            passed += 1
            status = "PASS"
        else:
            failed += 1
            status = "FAIL"
        print(f"  {status}  {author[:30]:<30} {year}  -> {result:<35} {'' if ok else f'(expected: {expected})'}")

    print("-" * 70)
    print(f"  {passed}/{passed + failed} passed, {failed} failed")
    print("=" * 70)

    return failed == 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == '--test':
        success = run_tests()
        sys.exit(0 if success else 1)

    if len(sys.argv) >= 4:
        author = sys.argv[1]
        year = sys.argv[2]
        title = ' '.join(sys.argv[3:])
        key = generate_canonical_key(author, year, title)
        print(key)
    else:
        print("Usage:")
        print("  python scripts/bibtex_key_generator.py AUTHOR YEAR TITLE...")
        print("  python scripts/bibtex_key_generator.py --test")
        print()
        print("Examples:")
        print('  python scripts/bibtex_key_generator.py "Kahneman, Daniel" 1979 "Prospect Theory"')
        print("  -> kahneman1979prospect")
        sys.exit(1)


if __name__ == '__main__':
    main()
