#!/usr/bin/env python3
"""
README Consistency & Quality Validation Script
Automatisierte Prüfung aller README-Dateien auf Konsistenz und Fehler

Version: 1.0 | 2026-01-20
Autor: Claude Code QA
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import json
from datetime import datetime
import subprocess


class ReadmeValidator:
    """Systematische Validierung aller README-Dateien"""

    def __init__(self, repo_root: str = None):
        if repo_root is None:
            # Derive repo root from script location: scripts/ -> repo root
            repo_root = str(Path(__file__).resolve().parent.parent)
        self.repo_root = Path(repo_root)
        self.errors = []
        self.warnings = []
        self.checks_passed = []
        self.version = "1.0"

    def validate_all(self):
        """Führe alle Validierungen durch"""
        print("=" * 80)
        print("README CONSISTENCY & QUALITY VALIDATION")
        print("=" * 80)
        print(f"Repo: {self.repo_root}")
        print(f"Zeit: {datetime.now().isoformat()}")
        print()

        # Hauptvalidierungen
        self._check_numerical_consistency()
        self._check_version_consistency()
        self._check_9c_completeness()  # CHECK 2.5: Framework Completeness
        self._check_links_validity()
        self._check_formatting_errors()
        self._check_cross_references()
        self._check_table_integrity()
        self._check_duplicate_entries()
        self._check_broken_structures()
        self._check_chapter_completeness()  # CHECK 2.8: Chapter Completeness (NEU)
        self._check_chapter_categorization()  # CHECK 2.9: Chapter Categorization (NEU)

        self._print_report()
        return len(self.errors) == 0

    # ========== CHECK 1: ZAHLENKONSISTENZ ==========
    def _check_numerical_consistency(self):
        """Prüfe Konsistenz von Zahlenwerten über alle READMEs"""
        print("\n[CHECK 1] Zahlenkonsistenz prüfen...")

        readme_paths = {
            'main': self.repo_root / 'README.md',
            'chapters': self.repo_root / 'chapters' / 'README.md',
            'appendices': self.repo_root / 'appendices' / 'README.md',
            'docs': self.repo_root / 'docs' / 'README.md',
        }

        numbers_dict = {
            'appendices': {},
            'chapters': {},
            'papers': {},
            'skills': {},
        }

        for name, path in readme_paths.items():
            if not path.exists():
                self.warnings.append(f"README nicht gefunden: {path}")
                continue

            content = path.read_text(encoding='utf-8')

            # Appendices-Zahl
            appendix_match = re.search(r'(\d+)\s*(?:Appendices?|appendices?)', content)
            if appendix_match:
                numbers_dict['appendices'][name] = int(appendix_match.group(1))

            # Chapters-Zahl
            chapter_match = re.search(r'(\d+)\s*(?:\+\s*)?(?:\d+\s*)?(?:Kapitel|Chapters?)', content)
            if chapter_match:
                numbers_dict['chapters'][name] = int(chapter_match.group(1))

            # Papers/References
            papers_match = re.search(r'(\d+(?:,\d+)?)\s*(?:Papers?|scientific works)', content)
            if papers_match:
                number_str = papers_match.group(1).replace(',', '')
                numbers_dict['papers'][name] = int(number_str)

            # Skills
            skills_match = re.search(r'(\d+)\+?\s*(?:Skills?|Commands?|slash commands)', content)
            if skills_match:
                numbers_dict['skills'][name] = int(skills_match.group(1))

        # Validiere Konsistenz
        for category, values in numbers_dict.items():
            if len(values) > 1:
                unique_values = set(values.values())
                if len(unique_values) > 1:
                    self.errors.append(
                        f"INKONSISTENZ ({category}): {values}\n"
                        f"  Verschiedene Werte gefunden in: {list(values.keys())}"
                    )
                else:
                    self.checks_passed.append(f"✅ {category.upper()}: Konsistent ({list(unique_values)[0]})")

    # ========== CHECK 2: VERSIONSKONSISTENZ ==========
    def _check_version_consistency(self):
        """Prüfe Version ist überall gleich (v54 im Dezember 2025)"""
        print("[CHECK 2] Versionskonsistenz prüfen...")

        readme_main = self.repo_root / 'README.md'
        if readme_main.exists():
            content = readme_main.read_text(encoding='utf-8')
            version_match = re.search(r'Version\s*(\d+)', content)
            if version_match:
                main_version = version_match.group(1)
            else:
                main_version = None
        else:
            return

        if main_version:
            readme_paths = [
                self.repo_root / 'chapters' / 'README.md',
                self.repo_root / 'appendices' / 'README.md',
                self.repo_root / 'docs' / 'README.md',
            ]

            for path in readme_paths:
                if path.exists():
                    content = path.read_text(encoding='utf-8')
                    if f'v{main_version}' not in content and main_version not in content:
                        self.warnings.append(
                            f"VERSIONSWARNUNG: {path.name} hat möglicherweise Version v{main_version} nicht"
                        )
                    else:
                        self.checks_passed.append(f"✅ {path.name}: Version konsistent")

    # ========== CHECK 2.5: 10C FRAMEWORK COMPLETENESS (NEU) ==========
    def _check_9c_completeness(self):
        """Prüfe ob 10C Framework vollständig dokumentiert ist"""
        print("[CHECK 2.5] 10C Framework Completeness prüfen...")

        CORE_QUESTIONS = ['WHO', 'WHAT', 'HOW', 'WHEN', 'WHERE', 'AWARE', 'READY', 'STAGE', 'HIERARCHY']

        readme_main = self.repo_root / 'README.md'
        if not readme_main.exists():
            return

        content = readme_main.read_text(encoding='utf-8')

        # Prüfe ob alle 9 Fragen vorhanden sind
        found_questions = []
        for question in CORE_QUESTIONS:
            if f'**{question}**' in content:
                found_questions.append(question)

        if len(found_questions) == 9:
            self.checks_passed.append(f"✅ 10C CORE Framework: Alle 9 Fragen vorhanden")
        else:
            missing = [q for q in CORE_QUESTIONS if q not in found_questions]
            self.errors.append(
                f"❌ 10C CORE FRAMEWORK INCOMPLETE: {len(found_questions)}/9 Fragen vorhanden\n"
                f"  Fehlend: {missing}\n"
                f"  Red Flag: Framework ist unvollständig!"
            )

        # Prüfe ob Zahlen konsistent sind (8 vs 9)
        if '10C' in content or '9c' in content:
            # Framework wird als 10C bezeichnet
            if 'Die 9 fundamentalen Fragen' not in content and 'Die 9 fundamentalen Fragen' not in content:
                self.warnings.append(
                    "⚠️ WARNING: Framework wird als '10C' erwähnt, "
                    "aber nicht als '9 fundamentale Fragen' beschrieben"
                )

    # ========== CHECK 3: LINK-VALIDITÄT ==========
    def _check_links_validity(self):
        """Prüfe ob alle Markdown-Links existieren"""
        print("[CHECK 3] Link-Validität prüfen...")

        readme_paths = [
            self.repo_root / 'README.md',
            self.repo_root / 'chapters' / 'README.md',
            self.repo_root / 'appendices' / 'README.md',
        ]

        for path in readme_paths:
            if not path.exists():
                continue

            content = path.read_text(encoding='utf-8')

            # Finde alle Markdown-Links: [text](path)
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

            for text, link in links:
                # Ignoriere externe Links
                if link.startswith('http://') or link.startswith('https://'):
                    continue

                # Ignoriere Anker-Links
                if link.startswith('#'):
                    continue

                # Prüfe ob lokale Datei existiert
                target_path = path.parent / link
                if not target_path.exists() and not target_path.exists():
                    # Versuche relativen Pfad vom repo_root
                    target_path = self.repo_root / link
                    if not target_path.exists():
                        self.errors.append(
                            f"BROKEN LINK in {path.name}: [{text}]({link})\n"
                            f"  Versucht: {target_path}"
                        )
                    else:
                        self.checks_passed.append(f"✅ Link ok: {link}")

    # ========== CHECK 4: FORMATIERUNGSFEHLER ==========
    def _check_formatting_errors(self):
        """Prüfe auf häufige Formatierungsfehler"""
        print("[CHECK 4] Formatierungsfehler prüfen...")

        readme_paths = [
            self.repo_root / 'README.md',
            self.repo_root / 'chapters' / 'README.md',
            self.repo_root / 'appendices' / 'README.md',
        ]

        formatting_issues = {
            'double_asterisks': r'\*\*\*+',  # *** statt **
            'unclosed_bold': r'\*\*[^*]*$',  # ** am Ende
            'mismatched_parens': r'\([^)]*$',  # Ungeschlossene Klammer
            'table_errors': r'\|\s*\|',  # Doppelte Pipes in Tabellen
        }

        for path in readme_paths:
            if not path.exists():
                continue

            content = path.read_text(encoding='utf-8')

            # Spezifischer Check: doppelte Sternchen
            if '**' in content and '***' in content:
                matches = re.findall(r'\*{3,}', content)
                if matches:
                    self.errors.append(
                        f"FORMATTING ERROR in {path.name}: Doppelte/mehrfache Sternchen\n"
                        f"  Beispiele: {matches[:3]}"
                    )

    # ========== CHECK 5: CROSS-REFERENCES ==========
    def _check_cross_references(self):
        """Prüfe Konsistenz von Cross-References"""
        print("[CHECK 5] Cross-References prüfen...")

        main_readme = self.repo_root / 'README.md'
        if not main_readme.exists():
            return

        content = main_readme.read_text(encoding='utf-8')

        # Finde alle Appendix-Referenzen [AAA], [B], [C], etc.
        appendix_refs = re.findall(r'\[([A-Z]+)\]\(appendices/', content)

        # Prüfe ob diese Dateien existieren
        for code in set(appendix_refs):
            # Verschiedene mögliche Dateinamen
            possible_names = [
                f'{code}_*.tex',
                f'appendix_{code}_*.tex',
                f'{code.lower()}_*.tex',
            ]

            appendix_dir = self.repo_root / 'appendices'
            found = False
            for pattern in possible_names:
                matches = list(appendix_dir.glob(pattern))
                if matches:
                    found = True
                    break

            if found:
                self.checks_passed.append(f"✅ Appendix {code}: Referenz korrekt")
            else:
                self.warnings.append(f"WARNING: Appendix {code} nicht gefunden (aber möglicherweise OK)")

    # ========== CHECK 6: TABELLENINTEGRITÄT ==========
    def _check_table_integrity(self):
        """Prüfe Markdown-Tabellen auf Integrität"""
        print("[CHECK 6] Tabellenintegrität prüfen...")

        main_readme = self.repo_root / 'README.md'
        if not main_readme.exists():
            return

        content = main_readme.read_text(encoding='utf-8')

        # Finde alle Tabellen (Zeilen mit |)
        lines = content.split('\n')

        in_table = False
        table_start = 0
        table_col_count = None

        for i, line in enumerate(lines):
            if '|' not in line:
                if in_table:
                    in_table = False
                continue

            if line.strip().startswith('|'):
                col_count = line.count('|') - 1  # -1 weil erste/letzte | zählen

                if not in_table:
                    in_table = True
                    table_start = i
                    table_col_count = col_count
                else:
                    # Prüfe ob Spaltenanzahl konsistent
                    if col_count != table_col_count:
                        self.warnings.append(
                            f"TABLE STRUCTURE WARNING at line {i}: "
                            f"Spaltenanzahl inkonsistent ({col_count} vs {table_col_count})"
                        )

        self.checks_passed.append(f"✅ Tabellen: Strukturiert validiert")

    # ========== CHECK 7: DOPPELTE EINTRÄGE ==========
    def _check_duplicate_entries(self):
        """Prüfe auf doppelte Einträge in Tabellen"""
        print("[CHECK 7] Doppelte Einträge prüfen...")

        main_readme = self.repo_root / 'README.md'
        if not main_readme.exists():
            return

        content = main_readme.read_text(encoding='utf-8')

        # Finde STAGE Einträge (bekannter Fehler)
        stage_matches = re.findall(r'\|\s*8\s*\|\s*\*\*STAGE\*\*', content)

        if len(stage_matches) > 1:
            self.errors.append(
                f"DUPLICATE ENTRY: {len(stage_matches)} × '8 | **STAGE**' gefunden\n"
                f"  Sollte: 1 konsolidierter Eintrag sein"
            )
        else:
            self.checks_passed.append(f"✅ STAGE Einträge: Keine Duplikate")

    # ========== CHECK 8: STRUKTUR-INTEGRITÄT ==========
    def _check_broken_structures(self):
        """Prüfe auf beschädigte Strukturen"""
        print("[CHECK 8] Struktur-Integrität prüfen...")

        main_readme = self.repo_root / 'README.md'
        if not main_readme.exists():
            return

        content = main_readme.read_text(encoding='utf-8')

        # Prüfe Heading-Struktur
        headings = re.findall(r'^#+\s+', content, re.MULTILINE)

        if headings:
            self.checks_passed.append(f"✅ Headings: {len(headings)} Überschriften found")

        # Prüfe auf ungeschlossene Code-Blöcke
        code_blocks = content.count('```')
        if code_blocks % 2 != 0:
            self.errors.append(
                f"BROKEN CODE BLOCK: Ungerade Anzahl von ``` ({code_blocks})\n"
                f"  Mindestens ein Code-Block ist nicht geschlossen"
            )
        else:
            self.checks_passed.append(f"✅ Code-Blöcke: {code_blocks // 2} Blöcke korrekt geschlossen")

    # ========== CHECK 2.8: CHAPTER COMPLETENESS ==========
    def _check_chapter_completeness(self):
        """Prüfe ob alle 22 Kapitel dokumentiert sind"""
        print("[CHECK 2.8] Chapter Completeness prüfen...")

        script_path = self.repo_root / 'scripts' / 'check_chapter_completeness.py'
        if not script_path.exists():
            self.warnings.append("⚠️ check_chapter_completeness.py nicht gefunden")
            return

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root)
            )

            if result.returncode == 0:
                self.checks_passed.append("✅ CHECK 2.8: Chapter Completeness PASSED")
            else:
                self.errors.append("❌ CHECK 2.8: Chapter Completeness FAILED")
                if result.stdout:
                    self.errors.append(result.stdout)

        except Exception as e:
            self.warnings.append(f"⚠️ CHECK 2.8 konnte nicht ausgeführt werden: {str(e)}")

    # ========== CHECK 2.9: CHAPTER CATEGORIZATION ==========
    def _check_chapter_categorization(self):
        """Prüfe ob Kapitel-Kategorisierung konsistent ist"""
        print("[CHECK 2.9] Chapter Categorization prüfen...")

        script_path = self.repo_root / 'scripts' / 'check_chapter_categorization.py'
        if not script_path.exists():
            self.warnings.append("⚠️ check_chapter_categorization.py nicht gefunden")
            return

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(self.repo_root)
            )

            if result.returncode == 0:
                self.checks_passed.append("✅ CHECK 2.9: Chapter Categorization PASSED")
            else:
                self.errors.append("❌ CHECK 2.9: Chapter Categorization FAILED")
                if result.stdout:
                    self.errors.append(result.stdout)

        except Exception as e:
            self.warnings.append(f"⚠️ CHECK 2.9 konnte nicht ausgeführt werden: {str(e)}")

    # ========== REPORTING ==========
    def _print_report(self):
        """Gebe strukturierten Report aus"""
        print("\n" + "=" * 80)
        print("VALIDIERUNGSERGEBNIS")
        print("=" * 80)

        # Erfolge
        if self.checks_passed:
            print(f"\n✅ BESTANDEN ({len(self.checks_passed)}):")
            for check in self.checks_passed:
                print(f"  {check}")

        # Warnungen
        if self.warnings:
            print(f"\n⚠️  WARNUNGEN ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")

        # Fehler
        if self.errors:
            print(f"\n❌ FEHLER ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}\n")

        # Zusammenfassung
        print("\n" + "-" * 80)
        total_passed = len(self.checks_passed)
        total_warnings = len(self.warnings)
        total_errors = len(self.errors)

        print(f"ZUSAMMENFASSUNG:")
        print(f"  ✅ Bestanden: {total_passed}")
        print(f"  ⚠️  Warnungen: {total_warnings}")
        print(f"  ❌ Fehler: {total_errors}")
        print(f"  Status: {'FAILED' if total_errors > 0 else 'PASSED'}")
        print("=" * 80)

        return total_errors == 0

    def export_json(self, output_path: str):
        """Exportiere Ergebnisse als JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'validator_version': self.version,
            'summary': {
                'passed': len(self.checks_passed),
                'warnings': len(self.warnings),
                'errors': len(self.errors),
                'status': 'PASSED' if len(self.errors) == 0 else 'FAILED',
            },
            'checks_passed': self.checks_passed,
            'warnings': self.warnings,
            'errors': self.errors,
        }

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Report exportiert zu: {output_path}")


def main():
    validator = ReadmeValidator()
    success = validator.validate_all()

    # Exportiere als JSON (relativer Pfad zum Repo-Root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    output_path = os.path.join(repo_root, 'quality', 'readme-validation-report.json')
    validator.export_json(output_path)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
