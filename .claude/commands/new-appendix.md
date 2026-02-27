# /new-appendix - Neuen Appendix erstellen

Erstelle einen neuen Appendix gemäß dem EBF Pflicht-Workflow.

## Verwendung
```
/new-appendix <CODE> <KATEGORIE> <TITEL>
/new-appendix AX DOMAIN-FINANCE "Financial Market Applications"
/new-appendix AY METHOD-SURVEY "Survey Methodology Integration"
```

## Die 8 Kategorien

| Prefix | Frage | Wann verwenden? |
|--------|-------|-----------------|
| `CORE-` | Was ist EBF? | Beantwortet eine der 10C Fragen |
| `FORMAL-` | Ist es rigoros? | Mathematische Beweise |
| `DOMAIN-` | Wo anwenden? | Ökonomie-Subfeld Anwendung |
| `CONTEXT-` | Wie wirkt Ψ? | Kontextdimension vertiefen |
| `METHOD-` | Wie messen? | Schätzung/Validierung |
| `PREDICT-` | Was vorhersagen? | Testbare Hypothesen |
| `LIT-` | Worauf basiert es? | Literatur-Integration |
| `REF-` | Wie nutzen? | Glossar, Beispiele |

## Pflicht-Workflow (aus CLAUDE.md)

1. **Template kopieren:** `cp appendices/00_appendix_template.tex appendices/<KATEGORIE>-<NAME>.tex`

2. **Pflicht-Elemente ausfüllen:**
   - Header Block (Category, Version, Dependencies)
   - Cross-Reference Map
   - Abstract + Quick Reference
   - Fundamental Question
   - Glossary Section (mit Link zu Appendix G)
   - Critical Foundations
   - References Section (mit `\nocite{bcm_master}`)

3. **Compliance prüfen:** Score ≥85% erforderlich

4. **Index aktualisieren (ALLE 4 Stellen in 00_appendix_index.tex):**
   - Haupttabelle (ca. Zeile 430)
   - Status-Tabelle (ca. Zeile 612)
   - Reading-Path-Tabelle (ca. Zeile 898)
   - Kategorie-Count erhöhen (ca. Zeile 68)

5. **Cross-References:** Bidirektionale Links zu verwandten Appendices
