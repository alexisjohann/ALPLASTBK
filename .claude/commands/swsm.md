# /swsm - Structured Writing Structure Model

Text-Analyse und -Generierung mit dem SWSM Framework (SFL + RST + CARS).

## Verwendung

```bash
# Text analysieren
/swsm analyze <datei> [--genre <genre>]
/swsm analyze docs/report.md --genre policy_brief

# Struktur planen (8D → Move-Sequenz)
/swsm plan --genre <genre> [--8d <profil>]
/swsm plan --genre ebf_appendix

# Text generieren
/swsm generate --genre <genre> --topic "<thema>"
/swsm generate --genre scientific_paper --topic "Context effects in decision-making"

# Qualitätsprüfung
/swsm check <datei> [--genre <genre>]
/swsm check outputs/paper.tex --genre scientific_paper
```

## Verfügbare Genres

| Genre | Move-Sequenz | Typischer Use Case |
|-------|--------------|-------------------|
| `scientific_paper` | CARS: Territory→Niche→Occupy→Methods→Results→Discussion | Journal Paper |
| `policy_brief` | Problem→Evidence→Recommendation→Call-to-Action | Entscheidungsvorlage |
| `executive_summary` | Context→Key Findings→Implications→Next Steps | Board Report |
| `ebf_appendix` | Abstract→Axioms→Theory→Worked Examples→Integration | EBF Dokumentation |
| `blog_post` | Hook→Problem→Solution→Takeaway | Öffentlichkeit |
| `consulting_memo` | Situation→Analysis→Recommendation→Implementation | Kundenberatung |

## SWSM Komponenten

```
ANALYSE (Text → Struktur):
┌─────────────────────────────────────────────────────────────────┐
│  E1 Clause Segmenter     → SFL Metafunktionen                   │
│  E2 RST Discourse Parser → Rhetorische Relationen               │
│  E3 CARS Move Tagger     → Genre-Moves (Swales 1990)            │
│  E4 RST-SFL Bridge       → Discourse-Clause Mapping             │
│  E5 Cohesion Analyzer    → Referenzketten, Lexikalische Kohäsion│
│  E6 Info Structure       → Theme-Rheme, Given-New               │
│  E7 Lexicogrammatical    → Register-Variablen                   │
└─────────────────────────────────────────────────────────────────┘

GENERIERUNG (8D → Text):
┌─────────────────────────────────────────────────────────────────┐
│  E8 Move Planner         → Dokumentstruktur aus Genre           │
│  E9 Text Generator       → SFL-basierte Textgenerierung         │
└─────────────────────────────────────────────────────────────────┘
```

## 8D → Genre Mapping

| 8D-Profil | Genre |
|-----------|-------|
| D₁>0.8, D₄>0.7, D₈>0.9 | scientific_paper |
| D₁<0.7, D₄<0.4, D₅=G₂ | policy_brief |
| D₁<0.5, D₄<0.3, D₆>0.8 | executive_summary |
| D₁>0.8, D₂>0.7, D₈>0.8 | ebf_appendix |
| D₁<0.4, D₇>0.4, D₆=1.0 | blog_post |
| D₁=0.6, D₄<0.4, D₆<0.5 | consulting_memo |

## Qualitätsmetriken

| Metrik | Gut | Verbesserungsbedarf |
|--------|-----|---------------------|
| Move Coverage | >90% | <70% |
| Kohäsions-Score | >0.7 | <0.5 |
| RST-Tiefe | 3-5 | <2 oder >7 |
| Info-Flow | Alternierend | Monoton |

## Integration mit anderen Skills

```
/generate-paper → verwendet SWSM für Move-Planung
/new-appendix   → verwendet SWSM Genre-Template "ebf_appendix"
/check-compliance → prüft Move-Coverage
```

## Beispiel: Policy Brief analysieren

```bash
/swsm analyze docs/policy-brief.md --genre policy_brief
```

Output:
```
=== SWSM ANALYSE ===
Genre: policy_brief
Move Coverage: 85%

Gefundene Moves:
  ★ Problem Statement (92%)
  ★ Evidence (78%)
  ★ Recommendation (85%)
  ◆ Call-to-Action (65%)

Fehlende Moves:
  ○ Cost-Benefit (nicht gefunden)

Kohäsion: 0.72
Info-Flow: front_loaded (New→New→Given)
```

## Scripts

| Script | Funktion |
|--------|----------|
| `swsm_sfl_annotator.py` | E1: Clause-Level Analyse |
| `swsm_rst_parser.py` | E2: RST-Baum Konstruktion |
| `swsm_move_tagger.py` | E3: Move-Identifikation |
| `swsm_rst_sfl_bridge.py` | E4: Discourse-Clause Mapping |
| `swsm_cohesion_analyzer.py` | E5: Kohäsionsanalyse |
| `swsm_info_structure.py` | E6: Informationsstruktur |
| `swsm_lexicogrammar.py` | E7: Register-Analyse |
| `swsm_move_planner.py` | E8: Dokumentplanung |
| `swsm_text_generator.py` | E9: Textgenerierung |

## Theoretische Basis

- **SFL**: Halliday (1985) - Systemic Functional Linguistics
- **RST**: Mann & Thompson (1988) - Rhetorical Structure Theory
- **CARS**: Swales (1990) - Create A Research Space
- **8D**: EBF Appendix DTE - Document Type Theory
