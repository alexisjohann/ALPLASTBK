# /generate-paper - Paper aus Kapitel/Appendix generieren

Generiere ein akademisches Paper basierend auf einem Kapitel oder Appendix mit dem 8D-Algorithmus und SWSM Framework.

## Verwendung
```
/generate-paper <quelle> [--style <stil>]
/generate-paper chapters/03_limits_utility.tex --style ernst_fehr
/generate-paper appendices/AU_bcm_axiom_formalization.tex --style nature
```

## Verfügbare Styles (8D-Profile)

| Style | Zielgruppe | D₁ | D₇ | Charakteristik |
|-------|------------|----|----|----------------|
| `ernst_fehr` | AER/JPE | 0.9 | 0.1 | Formal, testbare Hypothesen |
| `kahneman_tversky` | Broad Academic | 0.8 | 0.2 | Zugänglich, Heuristiken |
| `nature` | Science/Nature | 0.85 | 0.2 | Cross-disciplinary, high impact |
| `policy_brief` | Policy Makers | 0.6 | 0.25 | Action-oriented, kurz |
| `der_spiegel` | Bildungsbürger | 0.4 | 0.5 | Narrativ, engaging |
| `ted_talk` | General Public | 0.4 | 0.7 | Inspirierend, emotional |

## Workflow mit SWSM Integration

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: 8D-Profil bestimmen                                   │
│  → Style wählen oder 8D-Koordinaten manuell setzen              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: Genre aus 8D ableiten (SWSM)                          │
│  → scientific_paper / policy_brief / executive_summary / etc.   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: Move-Sequenz planen (SWSM E8)                         │
│  → Territory → Niche → Occupy → Methods → Results → Discussion  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: Text generieren (SWSM E9)                             │
│  → SFL-basierte Realisierung der Move-Sequenz                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 5: Qualitätsprüfung (SWSM E3)                            │
│  → Move Coverage ≥ 90%?                                         │
│  → Kohäsions-Score ≥ 0.7?                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 6: Output Format (8D Regel O-1)                          │
│  → D₈ > 0.6 → LaTeX                                             │
│  → 0.3 < D₈ ≤ 0.6 → Markdown                                    │
└─────────────────────────────────────────────────────────────────┘
```

## 8D-Algorithmus (aus CLAUDE.md)

### Phase 1: 8D-Koordinaten bestimmen
| D | Dimension | Skala |
|---|-----------|-------|
| D₁ | Wissen | 0=Laie → 1=Expert |
| D₂ | Nähe | 0=Fern → 1=Gleiches Feld |
| D₃ | Reichweite | 0=Persönlich → 1=Gesellschaftlich |
| D₄ | Zeit | 0=Wenig → 1=Viel Lesezeit |
| D₅ | Ziel | G₁-G₇ |
| D₆ | Kontext | 0=Intern → 1=Extern |
| D₇ | Emotion | 0=Sachlich → 1=Emotional |
| D₈ | Persistenz | 0=Kurzlebig → 1=Archiv |

### Phase 2-4: Struktur/Style/Vocabulary emergieren lassen
- Aus 8D-Koordinaten automatisch ableiten (Axiome DT-5 bis DT-9)
- **NEU**: SWSM Move-Planung für Genre-konforme Struktur

### Phase 5: Output generieren
- D₈ > 0.6 → LaTeX
- 0.3 < D₈ ≤ 0.6 → Markdown
- D₈ ≤ 0.3 → Plain Text

### Kompilierung
Nach Generierung automatisch PDF kompilieren mit `/compile`

## SWSM Qualitätsmetriken

| Metrik | Schwellwert | Prüfung |
|--------|-------------|---------|
| Move Coverage | ≥ 90% | Alle obligatorischen Moves vorhanden? |
| Kohäsion | ≥ 0.7 | Referenzketten, lexikalische Dichte |
| RST-Tiefe | 3-5 | Nicht zu flach, nicht zu tief |

## Beispiel

```bash
/generate-paper appendices/AU_CORE-AWARE.tex --style ernst_fehr
```

Output:
```
8D-Profil: ernst_fehr
  D₁=0.9, D₂=0.9, D₃=0.7, D₄=0.8, D₅=G₁, D₆=1.0, D₇=0.1, D₈=0.95

Genre: scientific_paper

Move-Sequenz (SWSM E8):
  1. ★ Establish_Territory - Centrality claiming
  2. ★ Establish_Niche - Gap indication
  3. ★ Occupy_Niche - Purpose statement
  4. ★ Methods - Methodology description
  5. ★ Results - Findings presentation
  6. ★ Discussion - Implications
  7. ◆ Conclusion - Summary

Generiere LaTeX...
Prüfe Qualität...
  Move Coverage: 100% ✓
  Kohäsion: 0.78 ✓

Output: outputs/paper_AU_CORE-AWARE_ernst_fehr.tex
```

## Verwandte Skills

- `/swsm` - Direkte SWSM Analyse/Generierung
- `/new-appendix` - Neuen Appendix mit SWSM Genre-Template
- `/compile` - LaTeX kompilieren
- `/check-compliance` - Template-Compliance prüfen
