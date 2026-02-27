# /new-chapter - Neues Kapitel erstellen

Erstelle ein neues Kapitel gemäß dem EBF Pflicht-Workflow.

## Verwendung
```
/new-chapter <NUMMER> <NAME> <TITEL>
/new-chapter 20 future_directions "Future Research Directions"
```

## Die 3 Kapiteltypen

| Typ | Kapitel | Besonderheit |
|-----|---------|--------------|
| **A** (CORE) | 5, 9, 10, 11, 12, 13 | CORE Connection Box PFLICHT |
| **B** (Foundation) | 1-4, 6-8 | Standard-Struktur |
| **C** (Application) | 14-19 | Multiple Worked Examples PFLICHT |

## Pflicht-Workflow (aus CLAUDE.md)

### Phase 1: Vorbereitung
1. Kapiteltyp bestimmen (A/B/C)
2. Kapitelnummer prüfen: `ls chapters/*.tex`

### Phase 2: Datei erstellen
3. Template kopieren: `cp chapters/00_chapter_template.tex chapters/<NR>_<name>.tex`

4. **Pflicht-Elemente (ALLE Typen):**
   - Metadata Block (Version, Purpose, Primary Appendix, Prerequisites)
   - Quick Reference Box
   - Appendix References Box
   - Intuition Box mit benannten Charakteren (Anna, Thomas, Maria...)
   - Central Question Box
   - Chapter Overview mit Section-Referenzen
   - Section Labels (`\label{sec:...}`) für ALLE Subsections
   - Reading Path Box am Ende

5. **Typ-spezifische Elemente:**
   - **TYPE A:** CORE Connection Box (farbig) + 10C Integration Table
   - **TYPE C:** Multiple Worked Examples (≥2) + Policy Implications Section

### Phase 3: Compliance
6. Compliance-Check: `python scripts/check_chapter_compliance.py chapters/<datei>.tex`
7. Score ≥85% erforderlich

### Phase 4: Navigation
8. Reading Path im VORHERIGEN Kapitel aktualisieren
9. Reading Path im FOLGENDEN Kapitel aktualisieren (falls vorhanden)

### Phase 5: Cross-References
10. Appendix-Verweise im Kapitel referenzieren
11. Rück-Referenzen in Appendices hinzufügen
