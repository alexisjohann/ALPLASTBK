# Quality Layer: Inhaltliche Qualitätssicherung

## Theoretische Fundierung

Das EBF Quality Framework (TERAN) ist **keine Ad-hoc-Konstruktion**, sondern eine systematische Adaption etablierter, peer-reviewed Frameworks:

| Quelle | Framework | Beitrag zu TERAN |
|--------|-----------|------------------|
| Belcher et al. (2016) | QAF | Relevance, Credibility, Legitimacy, Effectiveness |
| TACT (2023) | Validated | Trustworthiness, Auditability, Credibility, Transferability |
| Glassick (1997) | Scholarship | Preparation, Methods, Results, Presentation |
| Guba (1981) | Naturalistic | Truth Value, Applicability, Consistency, Neutrality |
| IDRC RQ+ (2017) | Development | Rigor, Legitimacy, Importance, Positioning |

**Primäre Quelle:** Belcher, B.M. et al. (2016). Defining and assessing research quality 
in a transdisciplinary context. *Research Evaluation*, 25(1), 1-17. 
[Systematic Review, 38 peer-reviewed Artikel, 500+ Zitationen]

→ Siehe `instruments/theoretical_foundation.md` für vollständiges Mapping.

## Zweck

Dieser Layer trennt **Template-Compliance** (formale Struktur) von **inhaltlicher Qualität** (wissenschaftlicher Substanz).

## Struktur

```
quality/
├── README.md                         # Diese Datei
├── instruments/                      # Messinstrumente
│   ├── theoretical_foundation.md     # NEU: Wissenschaftliche Fundierung
│   ├── quality_dimensions.md         # TERAN-Framework (T/E/R/A/N)
│   ├── epistemic_tags.md             # EMP/THR/LLM/ILL/HYP System
│   ├── assessment_template.md        # Vorlage für Assessments
│   └── check_quality.py              # Automatisierter Checker
├── assessments/                      # Einzelbewertungen
│   └── YYYY-MM-DD_appendix_X.md      # Datierte Assessments
└── reports/                          # Aggregierte Berichte
    └── YYYY-MM-DD_summary.md         # Periodische Zusammenfassungen
```

## Das TERAN-Framework

### Die 5 Dimensionen (adaptiert von Belcher et al. 2016)

| Dim | EBF | Belcher QAF | Gewicht |
|-----|---------|-------------|---------|
| **T** | Theory | Credibility (prep) | 25% |
| **E** | Evidence | Credibility (data) | 30% |
| **R** | Rigor | Credibility (method) | 15% |
| **A** | Applicability | Relevance + Effectiveness | 15% |
| **N** | Transparency | Legitimacy | 15% |

### Begründung der Gewichtung

- **Evidence (30%):** Höher als Standard, weil EBF quantitative Parameter-Behauptungen macht
- **Theory (25%):** Konsistent mit Glassick "Adequate Preparation"
- **R/A/N (je 15%):** Standard-Gewichtung für methodische Aspekte

### Bewertungsskala

| Score | Sterne | Bedeutung | Belcher-Äquivalent |
|-------|--------|-----------|-------------------|
| 9.0+ | ★★★★★ | Publication Ready | "Fully satisfies" |
| 7.0-8.9 | ★★★★☆ | Minor Revisions | "Fully satisfies" |
| 5.0-6.9 | ★★★☆☆ | Working Paper | "Partially satisfies" |
| 3.0-4.9 | ★★☆☆☆ | Draft | "Partially satisfies" |
| <3.0 | ★☆☆☆☆ | Concept | "Fails to satisfy" |

## Epistemic Status Tags

| Tag | Level | Definition | Quelle |
|-----|-------|------------|--------|
| EMP | ★★★★★ | Empirisch validiert | Peer-reviewed publication |
| THR | ★★★★☆ | Theoretisch abgeleitet | Formal proof or derivation |
| LLM | ★★★☆☆ | LLM-MC geschätzt | Simulation estimate |
| ILL | ★★☆☆☆ | Illustrativ | Example value |
| HYP | ★☆☆☆☆ | Hypothetisch | Speculative |

## Workflow

1. **Assessment erstellen:** Template aus `instruments/assessment_template.md`
2. **Subdimensionen bewerten:** Nach `quality_dimensions.md`
3. **Epistemic Audit:** Parameter-Tags prüfen
4. **Report generieren:** In `reports/` dokumentieren

## Aktueller Status (2026-01-07)

| Metrik | Wert | Ziel Q2 |
|--------|------|---------|
| Durchschnitt TERAN | 5.5/10 | 7.0/10 |
| Tag Coverage | 16% | 60% |
| Problematic Refs | 2-4 | 0 |

## Zitation

Bei Verwendung dieses Frameworks:

> EBF Quality Framework (TERAN), adaptiert von Belcher et al. (2016) QAF, 
> ergänzt um TACT (2023), Glassick (1997), und Guba (1981). 
> Gewichtung angepasst für quantitativ-parametrische Verhaltensmodelle.

## Referenzen

- Belcher, B.M. et al. (2016). *Research Evaluation*, 25(1), 1-17.
- Daniel, B.K. (2018). TACT Framework.
- Glassick, C.E. et al. (1997). *Scholarship Assessed*. Jossey-Bass.
- Guba, E.G. (1981). *ECTJ*, 29, 75-91.
- IDRC (2017). Research Quality Plus (RQ+).
