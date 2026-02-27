# /classify-papers - Extract Papers klassifizieren

> ⚠️ **DEPRECATED**: paper-sources.yaml + extracted_papers.yaml sind nicht mehr SSOT.
> SSOT: data/paper-references/PAP-*.yaml + bibliography/bcm_master.bib
> Neue Papers über /integrate-paper Workflow integrieren.

Klassifiziere 138 extrahierte Papers gegen paper-sources.yaml mit Fuzzy-Matching, Confidence-Scoring und Fallback-Appendix-Zuordnung.

## Kurzbeschreibung

Dieses Skill führt eine intelligente Klassifizierung von 138 extrahierten Papieren durch:

- **Direkte Matches**: 90 Papers (65.2%) via Author + Year fuzzy matching
- **Fallback Mapping**: 48 Papers (34.8%) via Domain-basierte Appendix-Zuordnung
- **100% Coverage**: Alle 138 Papiere erhalten eine `lit_appendix` Zuordnung
- **Confidence Scoring**: Jedes Match erhält ein Vertrauen-Rating (0.3-0.9)

## Verwendung

```
/classify-papers
/classify-papers --dry-run
/classify-papers --show-report
```

## Anweisungen

1. **Precondition Check**
   - Stelle sicher, dass beide Dateien existieren:
     - `data/extracted_papers.yaml` (138 Papers)
     - `data/paper-sources.yaml` (1784 Papers)

2. **Skript Ausführen**
   ```bash
   # Dry-run: Zeige was ändern würde, ohne zu schreiben
   python3 scripts/classify_extracted_papers.py --dry-run

   # Produktiv: Klassifiziere und schreibe Ergebnisse
   python3 scripts/classify_extracted_papers.py
   ```

3. **Ergebnisse Anschauen**
   - Check: `data/extracted_papers.yaml` aktualisiert
   - Reports: `outputs/paper_classification_report_*.yaml` (3 Reports)
   - Jedes Paper hat jetzt:
     - `status`: "classified" oder "extracted_unmatched"
     - `lit_appendix`: Zugeordnete Appendix (K, W, XV, etc.)
     - `match_confidence`: 0.3-0.9 für Qualitäts-Tracking

4. **Output Analysieren**
   - **Direct Matches (90 Papers)**:
     - 82 Papers @ 90% confidence (First Author + Year)
     - 6 Papers @ 80% confidence (Co-authors)
     - 2 Papers @ 70% confidence (BibTeX Key)

   - **Fallback Mapped (48 Papers)**:
     - CRT (Complex Systems) → W (LIT-ARIELY)
     - HTY (Historical) → XV (LIT-HISTORY)
     - GB (Labor) → AA (LIT-AUTOR)
     - usw. (siehe Fallback Map unten)

5. **Commit Vorbereitung**
   - Geänderte Dateien:
     - `data/extracted_papers.yaml` ✅
     - `outputs/paper_classification_report_*.yaml` ✅
   - Keine Breaking Changes - nur Klassifizierung hinzugefügt

## Fallback Appendix Mapping

| Extraction Source | LIT-Appendix | Beschreibung |
|-------------------|--------------|--------------|
| **CRT** | W | Complex Systems → LIT-ARIELY |
| **HTY** | XV | History/Philosophy → LIT-HISTORY |
| **GB** | AA | Labor/Education → LIT-AUTOR |
| **GN** | P | Game Theory → LIT-DUFLO |
| **JT** | K | Market Design → LIT-FEHR |
| **LA** | AA | Economics → LIT-AUTOR |
| **OT** | AX | Other → LIT-META |
| **RB** | K | Behavioral → LIT-FEHR |
| **SU** | K | Social → LIT-FEHR |
| **LO** | X | Loewenstein → LIT-LOEWENSTEIN |

## Matching Strategien (Priorität)

### Tier 1: Direkte Matches (Confidence 0.7-0.9)

1. **Exact Match** (conf: 1.0)
   - paper_id genau in paper-sources.yaml

2. **First Author + Year** (conf: 0.9) ⭐ 82 Papers
   - Normalisierter Nachname (é→e, ä→a) + Jahr
   - Höchste Confidence, häufigster Match

3. **Co-Authors** (conf: 0.8) ⭐ 6 Papers
   - Jeder Co-Author + Jahr
   - Fallback wenn Erste Autor nicht matcht

4. **Multiple Authors** (conf: 0.85)
   - 2+ Autoren im ID → im source_id
   - Für dual-author Papers wie "kahneman1979tversky"

5. **BibTeX Keys** (conf: 0.7) ⭐ 2 Papers
   - benabou_ok_2001_mobility → benabou2001
   - Basis-Name-Vergleich nach Jahr-Normalisierung

### Tier 2: Fallback Mapping (Confidence 0.3)

- Für ungematchte Papers: Domain → LIT-Appendix
- z.B.: "CRT_LIT-ARORA" → domain=CRT → appendix=W

## Metadata Output

Jedes Paper erhält:

```yaml
- id: acemoglu2003
  status: classified  # oder: extracted_unmatched
  lit_appendix: L     # Zugeordnete Appendix
  match_confidence: 0.9  # Oder: lit_appendix_confidence: 0.3 (fallback)
  title: "Institutions, Institutional Change, and Economic Performance"
  classification_notes: "Fuzzy matched as acemoglu2003labor"  # Oder: "Fallback: domain=CRT → appendix=W"
```

## Schwellenwerte & Metriken

| Metrik | Wert |
|--------|------|
| **Coverage Goal** | 100% (138/138) ✅ |
| **Direct Match Rate** | 65.2% (90/138) |
| **Fallback Rate** | 34.8% (48/138) |
| **High Confidence** (≥0.85) | 91.1% of matches |
| **Medium Confidence** (0.7-0.8) | 8.9% of matches |
| **Low Confidence** (0.3) | 34.8% fallback |

## Report Struktur

Automatisch generierte Reports in `outputs/`:

```yaml
statistics:
  total_papers: 138
  matched: 90
  unmatched: 48
  unmatched_with_fallback: 48  # Fallback mapped
  match_percentage: 65.2%
  overall_coverage: 100.0%     # Alle 138 klassifiziert

confidence_distribution:
  90%: 82 papers (91.1%)
  80%: 6 papers (6.7%)
  70%: 2 papers (2.2%)

appendix_breakdown:
  CRT: 26 papers
  HTY: 19 papers
  GB: 1 paper
  ...

fallback_appendix_map:
  CRT: W
  HTY: XV
  ...
```

## Tipps & Troubleshooting

### Paper wird nicht gematcht?
- Überprüfe: Ist das Paper WIRKLICH in paper-sources.yaml?
- Nutze: `grep "paper_id" data/paper-sources.yaml`
- Wenn nicht da: Fallback mapping wird angewendet ✓

### Confidence Score verstehen?
- **0.9**: Sehr zuverlässig (First Author + Year)
- **0.8**: Zuverlässig (Co-Author + Year)
- **0.7**: Moderate (BibTeX Key Match)
- **0.3**: Weniger zuverlässig (Domain Fallback)

### Fallback Map anpassen?
- Datei: `scripts/classify_extracted_papers.py`
- Suche: `FALLBACK_APPENDIX_MAP`
- Beispiel: `'CRT': 'W'` → Alle CRT Papers bekommen Appendix W

## Integration mit Git

```bash
# Nach /classify-papers Ausführung:
git add data/extracted_papers.yaml outputs/paper_classification_report_*.yaml
git commit -m "feat(data): Classify extracted papers - 90 direct + 48 fallback (100% coverage)"
git push origin <branch>
```

## Version & Maintenance

- **Script Version**: 1.2.0
- **Coverage**: 100% (138/138 papers)
- **Last Updated**: 2026-01-18
- **Maintenance**: Fallback Map kann für neue Domains erweitert werden

## Related Skills

- `/build-all` - Alle Papers kompilieren
- `/generate-paper` - Paper aus Kapitel/Appendix generieren
- `/check-compliance` - Appendix-Compliance prüfen
