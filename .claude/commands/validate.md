# /validate - Alle Validierungen ausführen

Führe alle Validierungsskripte aus und erstelle einen Gesamtbericht.

## Verwendung
```
/validate
/validate --core-only
/validate --quick
```

## Optionen

| Option | Beschreibung |
|--------|--------------|
| (keine) | Vollständige Validierung |
| `--core-only` | Nur 10C CORE Framework |
| `--quick` | Nur kritische Checks (schneller) |

## Validierungen

### 1. 10C CORE Framework Validierung
```bash
python scripts/validate_core_framework.py
```
Prüft Konsistenz der 10C CORE Definition (SSOT).

### 2. Kapitel-Compliance (Stichprobe)
```bash
for f in chapters/0[1-5]*.tex; do
  python scripts/check_chapter_compliance.py "$f"
done
```
Prüft Template-Compliance der Kapitel.

### 3. Appendix-Compliance (Stichprobe)
```bash
for f in appendices/A[AU]*.tex; do
  python scripts/check_template_compliance.py "$f"
done
```
Prüft Template-Compliance der CORE Appendices.

## Anweisungen

1. Führe alle Validierungsskripte aus
2. Sammle Ergebnisse in Kategorien:
   - ✅ PASSED
   - ⚠️ WARNING (Score 70-84%)
   - ❌ FAILED (Score <70% oder Fehler)

3. Erstelle Zusammenfassung:
   ```
   === Validation Report ===

   10C CORE Framework:     ✅ PASSED
   Chapter Compliance:    ⚠️ 3/5 passed (2 warnings)
   Appendix Compliance:   ✅ 8/8 passed

   Overall: ⚠️ WARNINGS PRESENT
   ```

4. Bei Fehlern: Zeige Details und Empfehlungen

## Beispiel-Output

```
=== EBF Validation Suite ===

[1/3] 10C CORE Framework
      python scripts/validate_core_framework.py
      ✅ PASSED - All 8 CORE questions consistent

[2/3] Chapter Compliance (5 samples)
      chapters/01_introduction.tex         ✅ 92%
      chapters/02_rationality_stability.tex ⚠️ 78%
      chapters/03_limits_utility.tex       ⚠️ 45%
      chapters/04_empirical_foundations.tex ✅ 88%
      chapters/05_complementarity.tex      ✅ 95%

[3/3] Appendix Compliance (CORE)
      appendices/AAA_aggregation_levels.tex ✅ 91%
      appendices/AU_bcm_axiom_formalization.tex ✅ 89%

=== Summary ===
✅ 10C CORE: Consistent
⚠️ Chapters: 3/5 compliant (2 need attention)
✅ Appendices: 2/2 compliant

Empfehlungen:
- chapters/02: Fehlende Reading Path Box
- chapters/03: Fehlende Metadata, Intuition Box, etc.
```
