# EBF Literaturüberblick — State of the Literature

> **Version:** auto-generated (2026-02-11)
> **Status:** Automatisch generiert aus `bcm_master.bib` + 2'347 Paper-YAMLs
> **SSOT:** `bibliography/bcm_master.bib` (BibTeX) + `data/paper-references/PAP-*.yaml` (Metadaten)
> **Script:** `python scripts/generate_literature_overview.py`

---

## Auf einen Blick

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EBF PAPER DATABASE — STATE OF THE LITERATURE                           │
│  Stand: 2026-02-11                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  📚 2'347 Papers    94 LIT-Appendices    153 Theorien    852 Cases      │
│                                                                         │
│  QUALITÄTS-PROFIL:                                                      │
│  ├── Evidence Tier 1 (Gold):     820 Papers (34%)                     │
│  ├── Evidence Tier 2 (Silver): 1'221 Papers (52%)                   │
│  ├── Evidence Tier 3 (Bronze):   290 Papers (12%)                     │
│  └── Sonstige:                    16 Papers  (0%)                     │
│                                                                         │
│  TIEFE-PROFIL:                                                          │
│  ├── Content L0 (Metadata):     343 Papers (14%)                     │
│  ├── Content L1 (Research Q.):   911 Papers (38%)                    │
│  ├── Content L2 (Summary):   1'078 Papers (45%)                   │
│  └── Content L3 (Full Text):     15 Papers  (0%)                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Publikationstypen

| Typ | Anzahl | Anteil |
|-----|--------|--------|
| **article (Peer-reviewed)** | 1'916 | 81.6% |
| **book** | 272 | 11.6% |
| **techreport (Working Papers)** | 78 | 3.3% |
| **incollection (Buchkapitel)** | 46 | 2.0% |
| **misc** | 12 | 0.5% |
| **inproceedings (Konferenzen)** | 12 | 0.5% |
| **unpublished** | 11 | 0.5% |
| **Total** | **2'347** | **100%** |

## 2. Zeitliche Verteilung

```
Dekade     Papers   Balken
─────────────────────────────────────────────────────
vor 1950      34   ██
1950er      31   █
1960er      46   ██
1970er      90   █████
1980er     166   █████████
1990er     331   ███████████████████
2000er     670   ████████████████████████████████████████
2010er     648   ██████████████████████████████████████
2020er     330   ███████████████████
─────────────────────────────────────────────────────
```

**Median-Jahr:** 2007
**Temporal Decay:** τ(p) = 2^(-age/15) mit Halbwertszeit 15 Jahre.

---

## 3. Top-Journals

| # | Journal | Papers | Tier |
|---|---------|--------|------|
| 1 | **American Economic Review** | 169 | 1 |
| 2 | **Quarterly Journal of Economics** | 110 | 1 |
| 5 | **Journal of Political Economy** | 69 | 1 |
| 6 | **Journal of Economic Behavior \& Organization** | 68 | 2 |
| 7 | **Econometrica** | 59 | 1 |
| 8 | **Journal of Economic Literature** | 56 | 1 |
| 9 | **Journal of Economic Perspectives** | 53 | 1 |
| 10 | **Review of Economic Studies** | 41 | 1 |
| 11 | **Science** | 30 | 1 |
| 12 | **Games and Economic Behavior** | 28 | 2 |
| 13 | **Journal of the European Economic Association** | 22 | 1 |
| 14 | **NBER Working Paper** | 22 | 2 |
| 15 | **Management Science** | 21 | 1 |
| 16 | **Journal of Finance** | 19 | 1 |

**Top-5 Ökonomie:** AER + QJE + JPE + Econometrica + RES = **448 Papers (19%)**

**Interdisziplinär:** Science + Nature = **47 Papers**

---

## 4. Evidence Tiers

```
Tier 1 (Gold)    █████████████████████████████████  820 (34%)
Tier 2 (Silver)  ██████████████████████████████████████████████████  1'221 (52%)
Tier 3 (Bronze)  ███████████  290 (12%)
```

**86% der Literatur ist Tier 1 oder 2** — eine starke empirische Basis.

---

## 5. Content Level (Strukturelle Tiefe)

Basierend auf den 6 Strukturellen Charakteristika S1-S6:

| Level | Name | Kriterium | Papers | Anteil |
|-------|------|-----------|--------|--------|
| **L0** | Metadata Only | Kein S₁-S₆ | 343 | 14.6% |
| **L1** | Research Question | S₁ vorhanden | 911 | 38.8% |
| **L2** | Summary/Extract | S₁-S₄ vorhanden | 1'078 | 45.9% |
| **L3** | Full Text | S₁-S₆ + R1-R4 | 15 | 0.6% |

```
L0  ██████████████  343
L1  ██████████████████████████████████████  911
L2  █████████████████████████████████████████████  1'078
L3  █  15
```

**L3 erfordert R1-R4:** Alle Originalsektionen (R1), Referenzen (R2), >10k Wörter (R3), keine EBF-Sektionen (R4).

---

## 6. Integration Level (EBF-Verknüpfungstiefe)

| Level | Name | Kriterium | Papers | Anteil |
|-------|------|-----------|--------|--------|
| **I1** | Classified | `use_for` + `evidence_tier` | 783 | 33.4% |
| **I2** | Theorized | + `theory_support` (MS-XX-XXX) | 1'159 | 49.4% |
| **I3** | Exemplified | + Case Registry (CAS-XXX) | 4 | 0.2% |
| **I4** | Parameterized | + Parameter Registry (PAR-XXX) | 318 | 13.5% |
| **I5** | Canonized | + Appendix + Chapter | 0 | 0.0% |
| — | Nicht zugeordnet | — | 83 | 3.5% |

**1503 Papers (64%)** haben `theory_support`.
**375 Papers (15%)** haben extrahierte Parameter.

---

## 7. Autoren-Cluster (Top 25 Erstautoren)

| # | Erstautor | Papers | LIT-Appendix | Schwerpunkt |
|---|-----------|--------|-------------|-------------|
| 1 | **Fehr** | 113 | LIT-FEH/FEHR | Social Preferences, Fairness, Neuro |
| 2 | **Kahneman** | 53 | LIT-KT | Prospect Theory, Heuristiken |
| 3 | **Malmendier** | 49 | LIT-MALMENDIER | Experience Effects, Corporate Finance |
| 4 | **List** | 47 | LIT-LIST | Field Experiments, Methodology |
| 5 | **Falk** | 42 | LIT-FALK | Reciprocity, Global Preferences |
| 6 | **Bénabou** | 40 | LIT-BENABOU | Motivated Beliefs, Identity |
| 7 | **Card** | 32 | LIT-CARD | Labor Economics, Immigration |
| 8 | **Aghion** | 30 | LIT-AGHION | Innovation, Growth |
| 9 | **Goldin** | 30 | LIT-GOLDIN | Gender, Labor History |
| 10 | **Becker** | 29 | LIT-BECKER | Household Economics, Human Capital |
| 11 | **Camerer** | 29 | — | Neuroeconomics, Experimental |
| 12 | **Schelling** | 29 | LIT-SCHELLING | Strategy, Focal Points |
| 13 | **Akerlof** | 28 | LIT-AKERLOF | Identity Economics, Market for Lemons |
| 14 | **Shafir** | 28 | LIT-SHAFIR | Scarcity, Decision Making |
| 15 | **Steen** | 28 | LIT-VANDENSTEEN | Strategy, Competition |
| 16 | **Autor** | 27 | LIT-AUTOR | Labor, Trade, Technology |
| 17 | **Mullainathan** | 26 | — | Scarcity, Machine Learning |
| 18 | **Thaler** | 25 | LIT-KT | Nudging, Mental Accounting |
| 19 | **Acemoglu** | 24 | — | Institutions, Political Economy |
| 20 | **Smith** | 24 | — | Experimental Markets |
| 21 | **Ariely** | 22 | — | Irrational Behavior |
| 22 | **Sunstein** | 22 | LIT-SUT | Nudging, Regulation |
| 23 | **Roth** | 20 | — | Market Design, Matching |
| 24 | **Loewenstein** | 20 | LIT-LOEWENSTEIN | Emotions, Intertemporal Choice |
| 25 | **Ambühl** | 20 | — | Informed Consent, Experiments |

**94 LIT-Appendices** decken die Autorenzuordnungen ab. Die grösste Kategorie ist **LIT-O** (1'160 Papers).

---

## 8. Theoretische Verankerung (Theory Support)

Die 10 am häufigsten gestützten Theorien:

| # | Theory ID | Theorie | Papers |
|---|-----------|---------|--------|
| 1 | **MS-RD-001** | Prospect Theory (Kahneman & Tversky) | 143 |
| 2 | **MS-LM-002** | MS-LM-002 | 138 |
| 3 | **MS-SP-004** | Social Preferences (General) | 134 |
| 4 | **MS-IN-001** | Inequality (General) | 102 |
| 5 | **MS-SP-001** | Inequity Aversion (Fehr & Schmidt) | 69 |
| 6 | **MS-BF-001** | Bounded Rationality | 45 |
| 7 | **MS-SP-002** | Reciprocity (Rabin) | 44 |
| 8 | **MS-IB-001** | Identity Economics (Akerlof & Kranton) | 43 |
| 9 | **MS-MO-003** | Motivated Beliefs (Bénabou & Tirole) | 43 |
| 10 | **MS-SF-001** | MS-SF-001 | 38 |

**1503 Papers (64%)** sind explizit mit Theorien verknüpft.

---

## 9. 10C-Dimension Coverage

| CORE | Code | Frage | Papers | Abdeckung |
|------|------|-------|--------|-----------|
| **HOW** | B | Wie interagieren? | 125 | ██████████████ Stark |
| **WHO** | AAA | Wer hat Utility? | 88 | █████████ Stark |
| **AWARE** | AU | Wie bewusst? | 65 | ███████ Stark |
| **WHEN** | V | Wann zählt Kontext? | 60 | ██████ Stark |
| **WHAT** | C | Was ist Utility? | 56 | ██████ Stark |
| **WHERE** | BBB | Woher die Zahlen? | 52 | █████ Stark |
| **INTELLIGENCE** | HI | Wie stratifizieren? | 48 | █████ Gut |
| **HIERARCHY** | HI | Entscheidungshierarchie? | 41 | ████ Gut |
| **STAGE** | AW | Wo in der Journey? | 26 | ██ Gut |
| **READY** | AV | Handlungsbereit? | 25 | ██ Gut |
| **EIT** | IE | Wie emergieren Interventionen? | 22 | ██ Gut |

**Alle 10C-Dimensionen haben gute Abdeckung (≥20 Papers).**

---

## 10. Domänen-Verteilung

| Domäne | Papers | Schwerpunkt |
|--------|--------|-------------|
| **DOMAIN-MIGRATION** | 52 | Immigration, Integration, Asyl |
| **DOMAIN-LABOR** | 33 | Arbeitsmarkt, Löhne, Beschäftigung |
| **DOMAIN-POLITICAL** | 26 | Wahlen, Politische Ökonomie |
| **DOMAIN-POLICY** | 20 | Regulierung, Nudging, Public Policy |
| **DOMAIN-HEALTH** | 19 | Gesundheitsverhalten, Prävention |
| **DOMAIN-MONETARY** | 15 | Geldpolitik, Zentralbanken |
| **DOMAIN-FINANCE** | 14 | Finanzmärkte, Behavioral Finance |
| **DOMAIN-EDUCATION** | 14 | Bildung, Skill Formation |
| **DOMAIN-PUBLIC** | 14 | Öffentliche Güter, Kooperation |
| **DOMAIN-INTEGRATION** | 14 | Soziale Integration |
| **DOMAIN-ORG** | 12 | Organisationsverhalten |
| **DOMAIN-DEVELOPMENT** | 8 | Entwicklungsökonomie |
| **DOMAIN-PLATFORM** | 7 | Digitale Plattformen |
| **DOMAIN-PREDICTION** | 6 |  |

---

## 11. Parameter-Extraktion

| Metrik | Wert |
|--------|------|
| Papers mit `parameter`-Feld | 375 (15%) |
| Papers mit `theory_support` | 1'503 (64%) |
| Papers mit ISBN | 316 (13%) |
| Papers mit `use_for` | 2'347 (100%) |

---

## 12. Verwandte Dokumente

| Priorität | Dokument | Inhalt |
|-----------|----------|--------|
| **SSOT** | `appendices/BM_METHOD-PAPERINT_*.tex` | Formale Definitionen (Axiome, Beweise) |
| **Prozess** | `docs/workflows/paper-workflow-overview.md` | Paper-Lifecycle, Skills, Architektur |
| **Qualität** | `docs/frameworks/paper-database-quality-dimensions.md` | 2D-System (C × I), S1-S6, R1-R4 |
| **Schemas** | `docs/frameworks/database-schemas-overview.md` | 5-Datenbank-Architektur |
| **Dieser** | `docs/frameworks/literature-overview.md` | Konsolidierter Gesamtüberblick |

---

## 13. Aktualisierung

Dieses Dokument wird automatisch generiert:

```bash
python scripts/generate_literature_overview.py
```

*Generiert: 2026-02-11 | Datenstand: bcm_master.bib v2347 + 2'347 Paper-YAMLs*