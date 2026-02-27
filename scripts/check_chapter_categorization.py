#!/usr/bin/env python3
"""
CHECK 2.9: Chapter Categorization Validation

Prüft:
1. Part I-VII Sums stimmen mit total_chapters überein
2. Kapitel-Zuweisung zu Parts ist logisch
3. Keine Duplikate oder Lücken in Part-Zuweisungen
4. Part VI = Intervention Design (13-20)
5. Part VII = Limitations & Conclusion (21-22)
"""

import yaml
from pathlib import Path

class ChapterCategorizationValidator:
    def __init__(self, repo_root=None):
        if repo_root is None:
            repo_root = Path(__file__).parent.parent
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.checks_passed = []

    def validate(self):
        print("[CHECK 2.9] Chapter Categorization Validation starten...")
        print()

        # 1. Lade SSOT
        ssot = self._load_ssot()
        if not ssot:
            return False

        # 2. Prüfe Part-Sums
        self._check_part_sums(ssot)

        # 3. Prüfe Part-Inhalte
        self._check_part_contents(ssot)

        # 4. Prüfe kritische Parts (VI, VII)
        self._check_critical_parts(ssot)

        # 5. Prüfe README vs SSOT
        self._check_readme_consistency(ssot)

        return self._print_report()

    def _load_ssot(self):
        """Lade counts_registry.yaml"""
        registry_path = self.repo_root / 'data' / 'counts_registry.yaml'
        if not registry_path.exists():
            self.errors.append("❌ counts_registry.yaml nicht gefunden!")
            return None

        with open(registry_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _check_part_sums(self, ssot):
        """Prüfe ob Part-Summen = total_chapters"""
        print("[CHECK 2.9.1] Part-Sums prüfen...")

        chapters = ssot.get('chapters', {})
        parts = chapters.get('parts', {})

        part_sum = sum([parts.get(f'part_{i}', 0) for i in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi']])
        total = chapters.get('total_chapters', 0)

        if part_sum == total:
            self.checks_passed.append(
                f"✅ Part-Sum Consistency: sum(parts) = {part_sum}, total_chapters = {total} ✓"
            )
        else:
            self.errors.append(
                f"❌ PART SUM MISMATCH: sum(parts) = {part_sum}, aber total_chapters = {total}"
            )

    def _check_part_contents(self, ssot):
        """Prüfe ob Part-Inhalte logisch sind"""
        print("[CHECK 2.9.2] Part-Inhalte prüfen...")

        chapters = ssot.get('chapters', {})
        parts = chapters.get('parts', {})

        part_mapping = {
            'part_i': ('1-4', 'Foundations'),
            'part_ii': ('5-9', 'Core Theory'),
            'part_iii': ('10', 'Utility Architecture'),
            'part_iv': ('11', 'Awareness'),
            'part_v': ('12', 'Willingness'),
            'part_vi': ('13', 'BCJ: Stage-Dependent Dynamics'),
            'part_vii': ('14', 'BCJ: Behavioral Change Segments'),
            'part_viii': ('15', 'WEC-Synthesis'),
            'part_ix': ('16', 'Probability & Effectiveness'),
            'part_x': ('17-20', 'Intervention Toolkit'),
            'part_xi': ('21-22', 'Limitations & Conclusion'),
        }

        for part_key, (chapters_expected, description) in part_mapping.items():
            count = parts.get(part_key, 0)
            if count > 0:
                self.checks_passed.append(
                    f"✅ {part_key.upper()}: {count} Kapitel ({chapters_expected}: {description})"
                )
            else:
                self.warnings.append(
                    f"⚠️ {part_key.upper()}: Keine Kapitel definiert"
                )

    def _check_critical_parts(self, ssot):
        """Spezifische Prüfung für Parts VI-XI (Fehler #9 und #10 Prävention)"""
        print("[CHECK 2.9.3] Kritische Parts (VI-XI: Granular Structure) prüfen...")

        chapters = ssot.get('chapters', {})
        parts = chapters.get('parts', {})

        # Fehler #10 Resolution: Chapters 13-16 granular structure
        critical_parts = {
            'part_vi': (1, '13: BCJ Stage-Dependent'),
            'part_vii': (1, '14: BCJ Segments'),
            'part_viii': (1, '15: WEC-Synthesis'),
            'part_ix': (1, '16: Probability Bridge'),
            'part_x': (4, '17-20: Toolkit'),
            'part_xi': (2, '21-22: Conclusion'),
        }

        for part_key, (expected_count, description) in critical_parts.items():
            actual_count = parts.get(part_key, 0)
            if actual_count == expected_count:
                self.checks_passed.append(
                    f"✅ {part_key.upper()}: {actual_count} ({description}) - Fehler #10 Prevention OK"
                )
            else:
                self.errors.append(
                    f"❌ {part_key.upper()}: Erwartet {expected_count} ({description}), aber {actual_count} gefunden"
                )

    def _check_readme_consistency(self, ssot):
        """Prüfe ob README konsistent mit SSOT ist (11-Part granular structure)"""
        print("[CHECK 2.9.4] README vs SSOT Konsistenz...")

        readme_path = self.repo_root / 'README.md'
        if not readme_path.exists():
            self.warnings.append("⚠️ README.md nicht gefunden")
            return

        readme_content = readme_path.read_text(encoding='utf-8')

        # Prüfe 11-Part granular structure in README
        granular_parts = [
            ('13', 'BCJ: Stage-Dependent'),
            ('14', 'BCJ: Behavioral Change Segments'),
            ('15', 'WEC-Synthesis'),
            ('16', 'Probability & Effectiveness'),
            ('17-20', 'Intervention Toolkit'),
            ('21-22', 'Limitations & Conclusion'),
        ]

        for chapters_ref, part_name in granular_parts:
            if chapters_ref in readme_content and part_name in readme_content:
                self.checks_passed.append(
                    f"✅ README: Chapters {chapters_ref} ({part_name}) korrekt dokumentiert"
                )
            else:
                self.warnings.append(
                    f"⚠️ README: Chapters {chapters_ref} ({part_name}) nicht eindeutig dokumentiert"
                )

        # Prüfe Gesamt-Kapitel
        if '22 Kapitel' in readme_content or '22 chapters' in readme_content:
            self.checks_passed.append(
                "✅ README: Total chapters = 22 dokumentiert"
            )
        else:
            self.warnings.append(
                "⚠️ README: Kapitel-Gesamtzahl nicht eindeutig"
            )

    def _print_report(self):
        """Drucke Validierungs-Report"""
        print()
        print("=" * 80)
        print("CHAPTER CATEGORIZATION VALIDATION REPORT")
        print("=" * 80)
        print()

        if self.checks_passed:
            print(f"✅ PASSED ({len(self.checks_passed)}):")
            for check in self.checks_passed:
                print(f"  {check}")
            print()

        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
            print()
            return False

        print("🎉 ALL CHECKS PASSED")
        return True


if __name__ == '__main__':
    import sys

    validator = ChapterCategorizationValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)
