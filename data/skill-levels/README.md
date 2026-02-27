# Skill-Levels Architecture

**SSOT for:** Multi-tier skill taxonomy, Kaufland role profiles, cross-framework mappings
**Version:** 1.1
**Created:** 2026-02-22
**Model Reference:** MOD-013 (KIBSM)

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│  SKILL TIER HIERARCHY (Top → Bottom = Abstract → Concrete)    │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  TIER -1 (Executive):  Bartram Great Eight (8 factors)         │
│                        ↑ Aggregation layer                     │
│  TIER 0 (Meta):        O*NET Abilities (52 latent capacities)  │
│                        ↑ Psychometric reference                │
│  TIER 1 (Cross-Func):  WEF Global Skills (~120 items, L4)     │
│                        ↑ WEF → O*NET Mapping (expert loadings) │
│  TIER 2 (EU):          ESCO Transversal Skills (97 clusters)   │
│                        ↑ ESCO → WEF Mapping (coverage scores)  │
│  TIER 3 (Qualif):      DQR/EQF Levels (8 qualification levels)│
│                        ↑ O*NET cross-reference                 │
│  TIER 4 (Domain):      Kaufland Role Profiles (7 roles)        │
│                        ↑ Application: skill requirements       │
│                                                                │
│  MEASUREMENT:          1-7 Scale (O*NET Fleishman 1992)        │
│  GAP ANALYSIS:         Person Level vs. Job Requirement        │
│  TRANSFERABILITY:      Cosine Similarity (52-dimensional)      │
└────────────────────────────────────────────────────────────────┘
```

### Transitive Chain

```
Kaufland Role → WEF L3 Skill → O*NET Ability → Bartram Factor
                  ↑                                    ↓
             ESCO T-Skill           DQR/EQF Qualification Level
```

### Cross-Reference Topology (DACH)

```
kaufland-role-profiles.yaml
    ├── dach_qualifikation per role ←→ dach-transferability.yaml
    ├── dqr_ref ────────────────────→ dqr-eqf-levels.yaml
    ├── nqr_ch_ref ─────────────────→ nqr-ch-levels.yaml
    └── nqr_at_ref ─────────────────→ nqr-at-levels.yaml

dach-transferability.yaml
    ├── kaufland_role_eqf_mapping ──→ kaufland-role-profiles.yaml (ROLE-K-*)
    ├── dqr_eqf_ref ───────────────→ dqr-eqf-levels.yaml
    ├── nqr_ch_ref ────────────────→ nqr-ch-levels.yaml
    └── nqr_at_ref ────────────────→ nqr-at-levels.yaml

dqr-eqf-levels.yaml
    ├── eqf_dach_bridge ───────────→ nqr-ch-levels.yaml + nqr-at-levels.yaml
    ├── dach_transferability_ref ──→ dach-transferability.yaml
    └── kaufland_roles_ref ────────→ kaufland-role-profiles.yaml

nqr-ch-levels.yaml ←→ nqr-at-levels.yaml (bidirectional)
    Both reference: dqr-eqf, dach-transferability, kaufland-roles
```

---

## Files

| File | Lines | Tier | Description |
|------|-------|------|-------------|
| `level-scale.yaml` | 117 | Scale | 7-point ordinal scale (Fleishman 1992) with gap interpretation |
| `onet-abilities.yaml` | 541 | 0 | 52 latent abilities across 4 categories (cognitive 21, psychomotor 10, physical 9, sensory 12) |
| `bartram-factors.yaml` | 339 | -1 | 8 higher-order competency factors (Great Eight) with Big Five mapping + 7 role profiles |
| `wef-taxonomy-official.yaml` | 602 | 1 | Complete WEF Global Skills Taxonomy (L1-L4, ~120 items) |
| `wef-to-onet-mapping.yaml` | 517 | 0↔1 | Expert-informed loadings: WEF L3 skills → O*NET abilities + ID crosswalk |
| `esco-taxonomy.yaml` | 640 | 2 | ESCO v1.2.1 structure: 3 pillars, 97 transversal skills, 8 EU countries |
| `esco-to-wef-mapping.yaml` | 573 | 1↔2 | Conceptual mapping: ESCO clusters → WEF L3 skills (coverage scores) + name crosswalk |
| `dqr-eqf-levels.yaml` | 662 | 3-DE | All 8 DQR/EQF qualification levels with Kaufland career mapping + DACH bridge |
| `nqr-ch-levels.yaml` | 752 | 3-CH | Swiss NQR: 8 levels, SBFI Berufsverzeichnis, retail career ladder |
| `nqr-at-levels.yaml` | 576 | 3-AT | Austrian NQR: 8 levels, BHS/HAK system, retail career ladder |
| `dach-transferability.yaml` | 659 | 3↔3 | DACH cross-country transferability: scores, scenarios, legal basis + Kaufland role mapping |
| `kaufland-role-profiles.yaml` | 548 | 4 | 7 Kaufland roles with WEF skill requirements + transferability matrix + DACH qualifications |

**Total:** ~6,530 lines

---

## Taxonomies

### 1. O*NET Abilities (Tier 0) — Psychometric Reference

- **Source:** Fleishman & Reilly (1992), U.S. Department of Labor
- **Count:** 52 abilities in 4 categories (Cognitive 21, Psychomotor 10, Physical 9, Sensory 12)
- **Purpose:** Gold standard for latent capacity measurement

### 2. Bartram Great Eight (Tier -1) — Executive Reporting

- **Source:** Bartram (2005), Journal of Applied Psychology, 90(6), 1185-1203
- **Count:** 8 higher-order competency factors
- **Validation:** Meta-analysis, N=4,861, operational validity = 0.53
- **Purpose:** Board-level aggregation, Big Five personality mapping

### 3. WEF Global Skills Taxonomy (Tier 1) — Cross-Functional Skills

- **Source:** World Economic Forum (2021/2025)
- **Structure:** L1 (2) → L2 (~14) → L3 (~35) → L4 (~120)
- **Purpose:** Global business language for skills

### 4. ESCO (Tier 2) — EU Standard

- **Source:** EU Commission + Cedefop, v1.2.1
- **Count:** 3,039 occupations, 13,939 skill concepts, 97 transversal skills
- **Purpose:** EU-wide standard (EURES mandate since 2021), multi-language support

### 5. DQR/EQF (Tier 3-DE) — German Qualification Levels

- **Source:** DQR-Handbuch (2013/2022), EQF Recommendation 2017/C 189/03
- **Count:** 8 levels (1:1 DQR↔EQF)
- **Purpose:** Formal qualification recognition, Kaufland career ladder alignment

### 6. NQR-CH (Tier 3-CH) — Swiss Qualification Levels

- **Source:** V-NQR (SR 412.105.1), SBFI Berufsverzeichnis
- **Count:** 8 levels (NQR-CH → EQF referenced)
- **Scope:** Vocational education only (academic degrees in nqf.ch-HS)
- **Unique:** Berufsmaturitaet (BM), Hoehere Fachschulen (HF), SBFI Berufsverzeichnis
- **Retail Berufe:** EBA Detailhandelsassistent/in, EFZ Detailhandelsfachmann/-frau, BP/HFP

### 7. NQR-AT (Tier 3-AT) — Austrian Qualification Levels

- **Source:** NQR-Gesetz (BGBl. I Nr. 14/2016), qualifikationsregister.at
- **Count:** 8 levels (NQR-AT → EQF referenced)
- **Scope:** All qualifications (vocational + academic)
- **Unique:** BHS-Matura (HAK = NQR 5 at age 19!), Berufsreifepruefung, Ingenieurgesetz 2017
- **Retail Berufe:** Lehrabschluss Einzelhandel, HAK-Matura, Meisterpruefung

### 8. DACH Transferability (Tier 3↔3) — Cross-Country Mapping

- **Source:** EU Berufsqualifikationsrichtlinie 2005/36/EG, Bilaterale I (CH-EU)
- **Coverage:** CH ↔ DE ↔ AT (all 6 directions, EQF 1-7)
- **Scores:** Quantitative transferability (0.0-1.0) per EQF level
- **Scenarios:** 4 typical retail transfer cases with gap analysis

---

## Kaufland Role Profiles (Tier 4)

7 roles from operative to executive, each with WEF skill requirements (level 1-7 + importance 0-5):

| ID | Role | Career Level | DQR | Key Skills |
|----|------|-------------|-----|------------|
| ROLE-K-001 | Regaleinraeumer:in | Einstieg | 2 | Dependability, Manual Dexterity |
| ROLE-K-002 | Kassierer:in | Einstieg | 3 | Service Orientation, Resilience |
| ROLE-K-003 | Verkaufsberater:in | Fachkraft | 3-4 | Service, Empathy, Product Knowledge |
| ROLE-K-004 | Abteilungsleiter:in | Erste Fuehrung | 4 | Leadership, Resource Management |
| ROLE-K-005 | Stellv. Marktleiter:in | Mittlere Fuehrung | 5 | Leadership, Analytics, Talent Mgmt |
| ROLE-K-006 | Marktleiter:in | Senior Fuehrung | 5-6 | Leadership, P&L, Systems Thinking |
| ROLE-K-007 | Bezirksleiter:in | Top Fuehrung | 6 | Multi-Store Leadership, Strategy |

### Transferability Matrix (Cosine Similarity)

```
              REGAL  KASSE  VERK.  ABT.L  ST.ML  ML    BZL
Regaleinr.    1.00   0.72   0.58   0.45   0.38   0.32  0.25
Kassierer     0.72   1.00   0.78   0.55   0.48   0.42  0.30
Verkaufsber.  0.58   0.78   1.00   0.70   0.62   0.55  0.40
Abt.Leiter    0.45   0.55   0.70   1.00   0.88   0.78  0.62
Stellv.ML     0.38   0.48   0.62   0.88   1.00   0.92  0.75
Marktleiter   0.32   0.42   0.55   0.78   0.92   1.00  0.85
Bezirksleiter 0.25   0.30   0.40   0.62   0.75   0.85  1.00
```

**Critical Transition:** Verkaufsberater → Abteilungsleitung (0.70) — erster Fuehrungssprung

---

## Scale

The 7-point level scale (defined in `level-scale.yaml`):

| Level | Label | Description | Cognitive Equivalent |
|-------|-------|-------------|---------------------|
| 1 | Minimal | Ability barely required | Recognition/recall |
| 2 | Basic | Routine application | Apply simple rules |
| 3 | Intermediate | Some judgment needed | Apply with adaptation |
| 4 | Advanced | Analysis and judgment | Analyze, choose approaches |
| 5 | High | Complex, ambiguous situations | Synthesize, create approaches |
| 6 | Expert | Novel situations | Generate original solutions |
| 7 | Master | Redefines standards | Create paradigms |

### Gap Interpretation

| Gap | Meaning | Timeline |
|-----|---------|----------|
| 0 | Person meets requirement | — |
| 1 | On-the-job training | 1-3 months |
| 2 | Structured development | 3-12 months |
| 3+ | Significant upskilling or role mismatch | 12+ months |

---

## Computation

### Skill Gap Analysis

```bash
python scripts/skill_gap_analysis.py --role marktleiter --person-profile my_profile.yaml
```

### Transferability Between Roles

```bash
python scripts/skill_gap_analysis.py --transferability --from kassierer --to abteilungsleiter
```

### Development Path

```bash
python scripts/skill_gap_analysis.py --development-path --from verkaufsberater --to marktleiter
```

---

## Calibration Status

| Component | Status | Method |
|-----------|--------|--------|
| O*NET Abilities | Validated | Fleishman & Reilly (1992), O*NET 29.0 |
| Bartram Great Eight | Validated | Meta-analysis, N=4,861 |
| WEF Taxonomy | Official | WEF 2021/2025 |
| ESCO Taxonomy | Official | EU Commission v1.2.1 |
| DQR/EQF Levels | Official | German/EU government standard |
| NQR-CH Levels | Official | Swiss government standard (SBFI) |
| NQR-AT Levels | Official | Austrian government standard (OeAD) |
| DACH Transferability | Expert-informed | Based on EQF referencing + bilateral agreements |
| WEF → O*NET Loadings | Expert-informed | To be calibrated with Kaufland data |
| ESCO → WEF Coverage | Expert-informed | To be validated with ESCO Crosswalk |
| Kaufland Role Profiles | Expert-informed | To be validated with Kaufland PX team |

---

## Integration Points

- **KIBSM Model (MOD-013):** Role profiles reference WHO segments + Psi-context modifiers
- **EBF Parameter Registry:** Skill-related parameters to be registered as PAR-SKILL-*
- **Phase 5 Skills:** Connected via 10C CORE dimensions (see `docs/phase-5-skill-enhancements.md`)

---

## DACH Qualification Comparison

### Key Differences at EQF 5 (Biggest Divergence!)

```
CH: Berufspruefung (BP)     → Age 25-30, deep practice + specialization
DE: Fachwirt/in (IHK)       → Age 25-30, deep practice + IHK exam
AT: HAK-Matura (BHS)        → Age 19(!), broad education + business qualification

Same EQF level, completely different profiles!
```

### Unique Elements per Country

| Feature | CH | DE | AT |
|---------|:--:|:--:|:--:|
| Berufsmaturitaet (BM) | Yes | — | — |
| Hoehere Fachschule (HF) | Strong | Weak | Medium |
| BHS (5yr school + Matura + profession) | — | — | Yes |
| Lehre mit Matura (BRP) | — | — | Yes |
| Bachelor Professional (title) | — | Yes | — |
| Passerelle (BM → University) | Yes | — | — |

### Transferability Heat Map (Retail)

```
         → CH    → DE    → AT
CH →     -----   0.85    0.80
DE →     0.82    -----   0.87
AT →     0.77    0.83    -----

Average (EQF 3-7). Lowest scores at EQF 5 due to HAK/BP/Fachwirt divergence.
```

---

## References

- Fleishman, E.A. & Reilly, M.E. (1992). *Handbook of Human Abilities*
- Bartram, D. (2005). The Great Eight Competencies. *Journal of Applied Psychology*, 90(6), 1185-1203
- WEF (2025). *Global Skills Taxonomy Adoption Toolkit*
- WEF (2025). *Future of Jobs Report 2025*
- ESCO v1.2.1 (2024). European Commission, DG EMPL + Cedefop
- DQR-Handbuch (2022). Bundesministerium fuer Bildung und Forschung
- NQR-CH Verordnung (SR 412.105.1). Staatssekretariat fuer Bildung, Forschung und Innovation (SBFI)
- NQR-Gesetz Oesterreich (BGBl. I Nr. 14/2016). OeAD/BMBWF
- Bildung Detailhandel Schweiz (2022). Neue Bildungsverordnungen EBA/EFZ
- EU Berufsqualifikationsrichtlinie 2005/36/EG (konsolidiert 2013/55/EU)
