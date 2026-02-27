# /check-compliance - Template-Compliance prüfen

Prüfe die Template-Compliance einer Kapitel- oder Appendix-Datei.

## Verwendung
```
/check-compliance <datei.tex>
/check-compliance chapters/03_limits_utility.tex
/check-compliance appendices/AAA_aggregation_levels.tex
```

## Anweisungen

1. Bestimme den Dateityp:
   - `chapters/*.tex` → verwende `scripts/check_chapter_compliance.py`
   - `appendices/*.tex` → verwende `scripts/check_template_compliance.py`

2. Führe das entsprechende Skript aus

3. Zeige die Ergebnisse mit:
   - Gesamtscore (muss ≥85% sein für Commits)
   - Fehlende Elemente mit konkreten Empfehlungen
   - Kapiteltyp (A/B/C) bei Kapiteln

4. Bei Score <85%: Liste konkrete Schritte auf, um Compliance zu erreichen

## Schwellenwerte

| Score | Status |
|-------|--------|
| ≥85% | ✅ Commit erlaubt |
| 70-84% | ⚠️ Verbesserung empfohlen |
| <70% | ❌ Commit blockiert |
