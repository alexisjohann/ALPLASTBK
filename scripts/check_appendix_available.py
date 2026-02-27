#!/usr/bin/env python3
"""
Check if an Appendix Code is Available

USAGE (BEFORE creating any new appendix!):
    python scripts/check_appendix_available.py BD
    python scripts/check_appendix_available.py --suggest LIT

EXIT CODES:
    0 = Code AVAILABLE
    1 = Code IN USE
    2 = Invalid format
"""

import re
import sys
from pathlib import Path

class AppendixCodeChecker:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.index_file = self.repo_root / "appendices" / "00_appendix_index.tex"
        self.codes_used = self._extract_codes()

    def _extract_codes(self):
        """Extract all codes from the appendix index"""
        codes = set()

        if not self.index_file.exists():
            print(f"❌ ERROR: Cannot find index file: {self.index_file}")
            sys.exit(2)

        with open(self.index_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Pattern: CODE & CATEGORY-NAME &
        # Examples: AL & LIT-ALESINA &
        # Examples: BD & LIT-ALESINA &
        pattern = r'^(\w+)\s+&\s+\w+-\w+\s+&'

        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                code = match.group(1).strip()
                codes.add(code)

        return sorted(codes)

    def is_available(self, code):
        """Check if a code is available"""
        code = code.upper()
        if not self._is_valid_code(code):
            print(f"❌ Invalid code format: {code}")
            print("   Valid formats: A-Z (single), AA-ZZ (double)")
            return False

        is_used = code in self.codes_used
        return not is_used

    def _is_valid_code(self, code):
        """Validate code format"""
        return bool(re.match(r'^[A-Z]{1,2}$', code))

    def suggest_next_code(self, category=None):
        """Suggest the next available code"""
        # Generate all possible codes
        singles = [chr(65+i) for i in range(26)]  # A-Z
        doubles = []
        for i in range(26):
            for j in range(26):
                doubles.append(chr(65+i) + chr(65+j))  # AA-ZZ

        all_codes = singles + doubles

        # Find first available
        for code in all_codes:
            if code not in self.codes_used:
                return code

        return None

    def show_status(self):
        """Show current code usage status"""
        print("=" * 70)
        print("APPENDIX CODE AVAILABILITY STATUS")
        print("=" * 70)
        print(f"Total codes used: {len(self.codes_used)}")
        print(f"Codes used: {', '.join(self.codes_used)}")
        print()
        print(f"Next available code: {self.suggest_next_code()}")
        print()
        print("=" * 70)

def main():
    if len(sys.argv) < 2:
        print("APPENDIX CODE CHECKER")
        print("=====================")
        print()
        print("USAGE:")
        print("  python scripts/check_appendix_available.py <CODE>")
        print("  python scripts/check_appendix_available.py --status")
        print("  python scripts/check_appendix_available.py --suggest")
        print()
        print("EXAMPLES:")
        print("  python scripts/check_appendix_available.py BD")
        print("  python scripts/check_appendix_available.py AH")
        print("  python scripts/check_appendix_available.py --status")
        print()
        print("IMPORTANT: Always check BEFORE creating a new appendix!")
        sys.exit(2)

    checker = AppendixCodeChecker()

    if sys.argv[1] == "--status":
        checker.show_status()
        sys.exit(0)

    if sys.argv[1] == "--suggest":
        next_code = checker.suggest_next_code()
        print(f"Next available code: {next_code}")
        sys.exit(0)

    code = sys.argv[1].upper()
    is_available = checker.is_available(code)

    if is_available:
        print(f"✅ Code {code:4s} is AVAILABLE ✓")
        print()
        print("You can use this code for your new appendix:")
        print(f"  File: appendices/{code}_descriptive_name.tex")
        print(f"  \\label{{app:lit-{code.lower()}}}")
        sys.exit(0)
    else:
        print(f"❌ Code {code:4s} is ALREADY IN USE ❌")
        print()
        print(f"All currently used codes ({len(checker.codes_used)} total):")

        # Group by category
        for i in range(0, len(checker.codes_used), 10):
            codes_line = checker.codes_used[i:i+10]
            print("  " + ", ".join(codes_line))

        print()
        next_code = checker.suggest_next_code()
        print(f"Use this instead: {next_code}")
        sys.exit(1)

if __name__ == "__main__":
    main()
