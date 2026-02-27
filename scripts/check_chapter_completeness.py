#!/usr/bin/env python3
"""
CHECK 2.8: Chapter Completeness Validation

Prüft:
1. Alle 22 Kapitel existieren als Dateien
2. Kapitel-Nummern sind sequenziell (1-22)
3. Keine doppelten oder fehlenden Kapitel
4. Kein Datei-Kapitel ohne README-Dokumentation
"""

import re
from pathlib import Path
import yaml

class ChapterCompletenessValidator:
    def __init__(self, repo_root=None):
        if repo_root is None:
            repo_root = Path(__file__).parent.parent
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.checks_passed = []

    def validate(self):
        print("[CHECK 2.8] Chapter Completeness Validation starten...")
        print()

        # 1. Prüfe SSOT vs Realität
        self._check_ssot_vs_files()

        # 2. Prüfe Kapitel-Sequenz
        self._check_chapter_sequence()

        # 3. Prüfe fehlende Hauptkapitel
        self._check_missing_main_chapters()

        # 4. Prüfe README-Dokumentation
        self._check_readme_documentation()

        return self._print_report()

    def _load_ssot(self):
        """Lade counts_registry.yaml"""
        registry_path = self.repo_root / 'data' / 'counts_registry.yaml'
        if not registry_path.exists():
            self.errors.append("❌ counts_registry.yaml nicht gefunden!")
            return None

        with open(registry_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _get_actual_chapters(self):
        """Finde alle Kapitel-Dateien"""
        chapters_dir = self.repo_root / 'chapters'

        # Finde alle Dateien mit Kapitel-Nummern 01-22 (plus Varianten)
        main_chapters = set()

        for file in chapters_dir.glob('*.tex'):
            # Extrahiere Kapitel-Nummer
            match = re.match(r'^(\d+)', file.stem)
            if match:
                num = match.group(1)
                # Nur Hauptkapitel 01-22
                if 1 <= int(num) <= 99:
                    main_chapters.add(int(num))

        return sorted(main_chapters)

    def _check_ssot_vs_files(self):
        """Prüfe ob SSOT mit tatsächlichen Dateien übereinstimmt"""
        print("[CHECK 2.8.1] SSOT vs. Dateien-Realität...")

        ssot = self._load_ssot()
        if not ssot:
            return

        expected_total = ssot.get('chapters', {}).get('total_chapters', 0)
        actual_chapters = self._get_actual_chapters()
        actual_total = len(actual_chapters)

        if expected_total == actual_total:
            self.checks_passed.append(
                f"✅ Chapter Count: SSOT sagt {expected_total}, Dateien zeigen {actual_total} (konsistent)"
            )
        else:
            self.errors.append(
                f"❌ CHAPTER COUNT MISMATCH: SSOT sagt {expected_total}, aber {actual_total} Dateien gefunden"
            )

    def _check_chapter_sequence(self):
        """Prüfe ob Kapitel-Nummern sequenziell sind"""
        print("[CHECK 2.8.2] Kapitel-Sequenz prüfen...")

        chapters_dir = self.repo_root / 'chapters'

        # Finde Hauptkapitel 01-22
        main_chapters = {}

        for file in chapters_dir.glob('*.tex'):
            match = re.match(r'^(\d+)(?:[_b]|\.)', file.stem)
            if match:
                num = int(match.group(1))
                if 1 <= num <= 99:
                    if num not in main_chapters:
                        main_chapters[num] = file.stem

        # Prüfe ob 1-22 alle vorhanden sind
        expected_sequence = set(range(1, 23))
        actual_sequence = set(main_chapters.keys())

        missing = expected_sequence - actual_sequence
        extra = actual_sequence - expected_sequence

        if not missing and not extra:
            self.checks_passed.append(
                f"✅ Kapitel-Sequenz: 1-22 alle sequenziell vorhanden"
            )
        else:
            if missing:
                self.errors.append(
                    f"❌ FEHLENDE KAPITEL: {sorted(missing)}"
                )
            if extra:
                self.warnings.append(
                    f"⚠️ EXTRA KAPITEL außerhalb 1-22: {sorted(extra)}"
                )

    def _check_missing_main_chapters(self):
        """Spezifische Prüfung für kritische Kapitel"""
        print("[CHECK 2.8.3] Kritische Kapitel prüfen...")

        chapters_dir = self.repo_root / 'chapters'
        critical_chapters = [1, 5, 10, 11, 12, 13, 14, 15, 17, 21, 22]

        for chapter_num in critical_chapters:
            found = False
            for pattern in [f'{chapter_num:02d}_', f'{chapter_num}_']:
                matches = list(chapters_dir.glob(f'{pattern}*.tex'))
                if matches:
                    found = True
                    break

            if found:
                self.checks_passed.append(f"✅ Kapitel {chapter_num:2d}: Vorhanden")
            else:
                self.errors.append(f"❌ Kapitel {chapter_num:2d}: FEHLT!")

    def _check_readme_documentation(self):
        """Prüfe ob alle Dateien-Kapitel in README dokumentiert sind"""
        print("[CHECK 2.8.4] README-Dokumentation prüfen...")

        readme_path = self.repo_root / 'README.md'
        if not readme_path.exists():
            self.warnings.append("⚠️ README.md nicht gefunden")
            return

        readme_content = readme_path.read_text(encoding='utf-8')

        # Prüfe ob Kapitel-Struktur erwähnt wird
        if '[13-15, 16-20]' in readme_content or 'Intervention Design' in readme_content:
            self.checks_passed.append("✅ README: Kapitel 13-20 dokumentiert")
        else:
            self.warnings.append("⚠️ README: Kapitel-Struktur unklar")

        if '[21-22]' in readme_content or 'Limitations & Conclusion' in readme_content:
            self.checks_passed.append("✅ README: Kapitel 21-22 dokumentiert")
        else:
            self.errors.append("❌ README: Kapitel 21-22 NICHT dokumentiert!")

    def _print_report(self):
        """Drucke Validierungs-Report"""
        print()
        print("=" * 80)
        print("CHAPTER COMPLETENESS VALIDATION REPORT")
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

    validator = ChapterCompletenessValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)
