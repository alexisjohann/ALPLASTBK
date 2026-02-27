# Paper Database Quality: 2-Dimensionen Framework

> **ACHTUNG:** Diese Datei ist eine **Zusammenfassung** des formalen Systems.
>
> ## SSOT (Single Source of Truth):
>
> | Datei | Beschreibung |
> |-------|--------------|
> | `appendices/BM_METHOD-PAPERINT_*.tex` | **Formale Definitionen** (L0-L3 × 1-5) |
> | `data/paper-integration-metrics.yaml` | Workflow-Metriken pro Paper |
> | `data/paper-integration-learnings.yaml` | Learning Database |
> | `data/paper-integration-queue.yaml` | Papers to upgrade |
>
> Erstellt: 2026-02-01
> Letzte Aktualisierung: 2026-02-01

---

## Das Problem: Wir vergessen es dauernd

Paper-Qualität hat **ZWEI unabhängige Dimensionen**, die beide erfüllt sein müssen. Wir arbeiten oft nur an einer und vergessen die andere.

**Referenz:** Appendix BM §1 "The 2D Classification System"

---

## Formale Mathematische Definitionen

**Referenz:** Appendix BM §1.1 "Formal Mathematical Definitions"

### Feld-Mengen (Semantische Partition)

```
Content-Felder (paper-intern):
F_C = {abstract, keywords, methodology, sample, findings, limitations, full_text, paper_bib}

Integration-Felder (EBF-spezifisch):
F_I = {use_for, evidence_tier, theory_support, case_links, parameter, appendix_refs, chapter_refs}

MECE-Constraint:
F_C ∩ F_I = ∅  (Mutually Exclusive)
```

### Level-Funktionen

```
Content Level C: Paper → {L0, L1, L2, L3}
- L0: nur bibliographische Felder
- L1: + abstract, |p|_C < 6000 chars
- L2: + methodology + findings, |p|_C < 50000 chars
- L3: + full_text, |p|_C ≥ 50000 chars

Integration Level I: Paper → {I1, I2, I3, I4, I5}
- I1: use_for ∈ φ_I(p) ∧ evidence_tier ∈ φ_I(p)
- I2: I1 ∧ theory_support ∈ φ_I(p)
- I3: I2 ∧ case_links ∈ φ_I(p)
- I4: I3 ∧ parameter ∈ φ_I(p)
- I5: I4 ∧ appendix_refs ∈ φ_I(p) ∧ chapter_refs ∈ φ_I(p)
```

### Qualitäts-Metrik

```
Q(p) = (q_C, q_I) ∈ [0,1]²

Ziel: Q* = (1, 1) ⟺ (L3, I5)

Distanz zum Ziel: d(p) = √[(1-q_C)² + (1-q_I)²]
```

---

## MECE-Axiome (Formal)

### Axiom MECE-1: Orthogonale Definition

> Die zwei Dimensionen sind **semantisch orthogonal**:
> - **CONTENT** = Was wir ÜBER das Paper wissen (paper-intern)
> - **INTEGRATION** = Wie das Paper mit EBF VERKNÜPFT ist (EBF-spezifisch)

### Axiom MECE-2: Statistische Unabhängigkeit

```
∀p ∈ P: P(C(p) = L_x | I(p) = I_y) = P(C(p) = L_x)

⟺ P(C, I) = P(C) · P(I)
```

**Implikation:** Wissen über Integration Level gibt **keine Information** über Content Level.

### Axiom MECE-3: Vollständigkeit (Collectively Exhaustive)

```
∀f ∈ F_all: (f ∈ F_C) ⊕ (f ∈ F_I)   (XOR)
```

Jedes Feld gehört zu **genau einer** Dimension.

### Theorem 1: Parameter-Zuweisung

> **Behauptung:** Extrahierte Parameter (λ, β, γ) gehören zu F_I, nicht F_C.
>
> **Beweis:**
> 1. Parameter-Extraktion erfordert PAR-XXX Registry (EBF-spezifisch)
> 2. Generische Literaturübersicht würde λ = 2.25 nicht extrahieren
> 3. Feld-Struktur (Behavioral Economics Keys) ist EBF-spezifisch
> 4. Nach MECE-3: `parameter` ∈ F_I ∎

---

## Prior Score π(p) ∈ [0,1] — Integrations-Entscheidung

**Referenz:** Appendix BM §1.1 Definitionen 5-8, Axiom MECE-4, Theorem 2

### Kernidee

```
Prior Score = Σ (Gewicht × EBF-Bedarf × Paper-Angebot)

π(p) = Σᵢ wᵢ · gᵢ · sᵢ(p) · τ(p)
```

wobei:
- **G = (g₁...g₆)**: Gap-Vektor (was EBF braucht)
- **S(p) = (s₁...s₆)**: Supply-Vektor (was Paper liefert)
- **τ(p)**: Evidence Tier Multiplikator

### Gap-Vektor G (EBF-Bedarf)

| Komponente | Formel | Bedeutung |
|------------|--------|-----------|
| g_theory | 1 - (MS covered / MS total) | Theory Catalog Lücke |
| g_param | 1 - (PAR mit Evidenz / PAR total) | Parameter Registry Lücke |
| g_case | 1 - (CAS / CAS Ziel) | Case Registry Lücke |
| g_LIT | max(1 - papers in LIT_j / Ziel) | Schwächster LIT-Appendix |
| g_10C | 1 - min(papers für 10C_k / Ziel) | Schwächste 10C-Dimension |
| g_domain | Priority für unterversorgte Domains | Domain-Balance |

### Supply-Vektor S(p) (Paper-Angebot)

| Komponente | Assessment | Bedeutung |
|------------|------------|-----------|
| s_theory(p) | 𝟙[erweitert MS-XX] | Stützt Theory Catalog? |
| s_param(p) | (extrahierbare Params) / 5 | Wieviele λ, β, γ? |
| s_case(p) | 𝟙[real-world Beispiel] | Case-würdig? |
| s_LIT(p) | 𝟙[füllt LIT-Lücke] | Passt zu schwachem LIT? |
| s_10C(p) | (adressierte 10C) / 10 | Wieviele 10C-Dimensionen? |
| s_domain(p) | 𝟙[domain match] | Passt zu schwacher Domain? |

### Evidence Tier Multiplikator τ(p)

| Tier | Beschreibung | τ |
|------|--------------|---|
| **1** | RCT, Top-5 Journal (QJE, AER, Econometrica, JPE, ReStud) | 1.0 |
| **2** | Peer-reviewed, solide Methodik | 0.8 |
| **3** | Working Paper, Preprint | 0.5 |

### Gewichte W (Default)

```
W = (w_theory, w_param, w_case, w_LIT, w_10C, w_domain)
  = (0.25,     0.25,    0.15,   0.15,  0.10,   0.10)
```

### Axiom MECE-4: Integrations-Entscheidung

| Score-Bereich | Entscheidung | Integration Target |
|---------------|--------------|-------------------|
| π(p) ≥ 0.7 | **HIGH PRIORITY** | I5 (vollständig) |
| 0.5 ≤ π < 0.7 | **STANDARD** | I3–I4 |
| 0.3 ≤ π < 0.5 | **MINIMAL** | I1–I2 |
| π(p) < 0.3 | **REJECT** | Nicht integrieren |

### Beispiel: Fehr & Schmidt (1999)

```
Gap:    G = (0.4, 0.6, 0.5, 0.3, 0.2, 0.4)
Supply: S = (1.0, 1.0, 0.8, 1.0, 0.6, 0.5)
Tier:   τ = 1.0 (QJE = Tier 1)

π = 0.25·0.4·1.0 + 0.25·0.6·1.0 + 0.15·0.5·0.8
  + 0.15·0.3·1.0 + 0.10·0.2·0.6 + 0.10·0.4·0.5
  = 0.10 + 0.15 + 0.06 + 0.045 + 0.012 + 0.02
  = 0.387

→ π = 0.387 ≥ 0.3 → INTEGRATE (Target I3–I4)
```

---

## Bayesian Updating des Prior Score

**Referenz:** Appendix BM §1.1 Definitionen 9-10, Axiom MECE-5, Theorem 3

### Kernidee: Unsicherheit nimmt ab mit mehr Information

```
π'(p | O_k) = Posterior Score nach Beobachtung von Content Level L_k

π'(p | O_k) = Σᵢ wᵢ · gᵢ · ŝᵢ,ₖ(p) · τ(p) · ρₖ
```

wobei:
- **ŝᵢ,ₖ(p)**: Aktualisierte Supply-Schätzung bei Level k
- **ρₖ**: Konfidenz-Multiplikator (uncertainty discount)

### Konfidenz-Multiplikatoren ρ_k

| Level | ρ_k | Begründung |
|-------|-----|------------|
| L0 (Bibliographic) | 0.6 | Nur Heuristiken (Journal, Autor, Title) |
| L1 (Abstract) | 0.8 | Abstract gibt Methodik und Domain-Signale |
| L2 (Methodology) | 0.95 | Konkrete Findings und Sample-Details |
| L3 (Full Text) | 1.0 | Volle Beobachtung, keine Unsicherheit |

### Axiom MECE-5: Monotone Informationsverfeinerung

```
k₁ < k₂ ⟹ Var[Ŝ_k₁(p)] ≥ Var[Ŝ_k₂(p)]
```

Mehr Content = weniger Unsicherheit (nie mehr).

### Beispiel: Update-Trajektorie für Fehr & Schmidt (1999)

```
L0 (nur Titel/Journal):
  - Journal: QJE → τ = 1.0
  - Autor: Fehr → heuristisch ŝ_LIT = 0.9
  - Title: "Fairness" → heuristisch ŝ_theory = 0.7
  → π'(L0) ≈ 0.25 × 0.6 = 0.15

L1 (+Abstract):
  - "inequity aversion model" → ŝ_theory = 1.0
  - "ultimatum games" → ŝ_case = 0.8
  → π'(L1) ≈ 0.32 × 0.8 = 0.26

L2 (+Methodology):
  - Parameter estimation shown → ŝ_param = 1.0
  - Multiple experiments → ŝ_10C = 0.6
  → π'(L2) ≈ 0.387 × 0.95 = 0.37

L3 (+Full Text):
  - Exact α, β values extractable
  → π'(L3) = 0.387 × 1.0 = 0.387

Trajektorie:
π'_L0=0.15 → π'_L1=0.26 → π'_L2=0.37 → π'_L3=0.387
```

### Operationale Regel: Early Rejection

```
π'(p | O_k) / ρ_k < θ_min ⟹ REJECT bei Level L_k

wobei θ_min = 0.2 (Minimum Viable Score)
```

**Beispiel:** Wenn π'(p | O_1) = 0.10 mit ρ_1 = 0.8, dann:
- Max möglicher Score = 0.10 / 0.8 = 0.125 < 0.2
- → Paper kann bei L1 abgelehnt werden (kein Full-Text nötig)

---

## Die 2 Dimensionen (MECE-konform, aus Appendix BM)

```
                        INTEGRATION LEVEL (I1-I5)
                        (EBF-spezifische Verknüpfung)

                        I1-I2               I4-I5
                    ┌───────────────────┬───────────────────┐
                    │                   │                   │
        L3          │   CONTENT-ONLY    │   VOLLSTÄNDIG     │
        (>50k)      │   ⚠️ Isoliert     │   ✅ Ideal        │
                    │   (kein EBF-Link) │   (L3, I5)        │
CONTENT LEVEL       ├───────────────────┼───────────────────┤
(L0-L3)             │                   │                   │
(paper-intern)      │   MINIMAL         │   INTEGRATION-    │
        L0-L1       │   ❌ Nur Entry    │   ONLY ⚠️         │
        (<2k)       │                   │   (EBF-Links ohne │
                    │                   │    Paper-Inhalt)  │
                    └───────────────────┴───────────────────┘

ZIEL: Content L3 × Integration I5 = (L3, I5) = Complete + Canonized
```

---

## Dimension 1: CONTENT LEVEL (L0-L3) — Paper-Intern

**Frage:** "Was wissen wir ÜBER das Paper?" (unabhängig von EBF)

**Referenz:** Appendix BM, Table 1 "Content Level Definitions (MECE-Compliant)"

### Die 4 Content Levels

| Level | Name | Threshold | Content (Paper-Intern) |
|-------|------|-----------|---------|
| **L0** | Bibliographic | 0 chars | Author, Title, Year, Journal, DOI |
| **L1** | Descriptive | ~2k chars | + Abstract, Keywords, Publication Type |
| **L2** | Analytical | ~6k chars | + Methodology, Sample, Findings, Limitations |
| **L3** | Complete | **>50k chars** | + Full Text, Paper's Bibliography |

> **MECE-Regel:** Content Level enthält KEINE EBF-spezifischen Felder!
> Keine Parameter-Extraktion, keine theory_support, keine use_for — das gehört zu Integration.

### Kritischer Schwellenwert

> **WICHTIG:** L3 erfordert **mehr als 50.000 Zeichen** (~8.000 Wörter).
> Ein Paper mit 20.000 Zeichen ist L2, NICHT L3!

```bash
# Validierung
wc -c data/paper-texts/PAP-xxx.md
# Muss >50000 zeigen für L3
```

### Content-Felder (für L1+)

**Frage:** "Was steht IN der Paper-Datei?"

### Pflicht-Felder (YAML)

| Feld | Beschreibung | Validierung |
|------|--------------|-------------|
| `paper` | BibTeX Key | Muss existieren |
| `superkey` | PAP-{key} | Format prüfen |
| `title` | Vollständiger Titel | Nicht leer |
| `author` | Erstautor | Nicht leer |
| `year` | Publikationsjahr | 1900-2030 |
| `publication_type` | Taxonomie | Einer von 6 Typen |
| `doi` | Digital Object Identifier | Gültige DOI oder null |
| `doi_missing_reason` | Grund wenn null | Pflicht wenn doi=null |
| `abstract` | Zusammenfassung | Empfohlen |
| `isbn` | Für Bücher | Pflicht wenn book/book_chapter |

### Publication Type Taxonomie

```
journal_article   → DOI erwartet
book              → ISBN erwartet, DOI optional
book_chapter      → ISBN optional, DOI optional
conference_paper  → DOI erwartet
working_paper     → DOI optional
report            → DOI optional
```

### DOI Missing Reasons

```
book_no_doi       → Bücher haben typischerweise keine DOIs
chapter_no_doi    → Buchkapitel haben typischerweise keine DOIs
working_paper     → Working Papers/Preprints ohne DOI
pre_doi_era       → Vor 2000 publiziert
not_found         → DOI sollte existieren, Lookup fehlgeschlagen
```

### Content-Qualitäts-Metriken

| Metrik | Formel | Ziel |
|--------|--------|------|
| **Coverage** | Felder gefüllt / Pflichtfelder | 100% |
| **Accuracy** | Validierte Werte / Gefüllte Felder | 100% |

---

## Dimension 2: INTEGRATION LEVEL (I1-I5) — EBF-Spezifisch

**Frage:** "Wie tief ist das Paper mit EBF VERKNÜPFT?" (unabhängig vom Paper-Inhalt)

**Referenz:** Appendix BM, Table 2 "Integration Level Definitions (MECE-Compliant)"

### Die 5 Integration Levels

| Level | Name | Zeit | EBF-spezifische Komponenten |
|-------|------|------|-------------|
| **I1** | Classified | 5 min | BibTeX + `use_for`, `evidence_tier` |
| **I2** | Theorized | 10-15 min | + `theory_support` (MS-XX-XXX Links) |
| **I3** | Exemplified | 15-20 min | + Case Registry entry (CAS-XXX) |
| **I4** | Parameterized | 20-30 min | + Parameter Registry (PAR-XXX), λ, β, γ extrahiert |
| **I5** | Canonized | 60-90 min | + Appendix Reference + Chapter Reference |

> **MECE-Regel:** Integration Level enthält KEINE paper-internen Informationen!
> Kein Abstract, keine Methodology, keine Findings — das gehört zu Content.

### Integration-Felder pro Level (MECE-konform)

| Level | BibTeX-Felder | YAML-Felder | Registry-Einträge |
|-------|---------------|-------------|-------------------|
| I1 | `use_for`, `evidence_tier` | - | - |
| I2 | + `theory_support` | - | MS-XX-XXX Links |
| I3 | I2 | + `case_links` | CAS-XXX |
| I4 | I3 | + `parameter` | PAR-XXX (λ, β, γ) |
| I5 | I4 | + `appendix_refs`, `chapter_refs` | Full cross-refs |

### Aktuelle Metriken (2026-02-01)

| Metrik | Wert | Ziel |
|--------|------|------|
| **use_for Coverage** | 100% | 100% ✅ |
| **theory_support** | 25% | >50% ⚠️ |
| **evidence_tier** | 100% | 100% ✅ |
| **parameter** | 13% | >30% ⚠️ |
| **case_links** | 0.1% | >10% ❌ |
| **model_links** | 0% | >5% ❌ |

---

## Kombinierte Qualitäts-Matrix (L0-L3 × I1-I5)

**Referenz:** Appendix BM §1.3 "MECE Independence of Dimensions"

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER QUALITY = CONTENT (L0-L3) × INTEGRATION (I1-I5)                  │
│  [MECE: Content = paper-intern | Integration = EBF-spezifisch]          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CONTENT    INTEGRATION    STATUS          AKTION                       │
│  ────────   ───────────    ──────          ──────                       │
│  L3         I5             ✅ IDEAL        Wartung                      │
│  L3         I1-I2          ⚠️ ISOLIERT     /upgrade-paper --integrate   │
│  L0-L1      I4-I5          ⚠️ FRAGIL       /upgrade-paper --content     │
│  L0-L1      I1-I2          ❌ MINIMAL      /upgrade-paper (beides)      │
│                                                                         │
│  ZIEL-ZUSTAND: (L3, I5) = Complete + Canonized                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Workflow: /upgrade-paper

**Skill:** `/upgrade-paper PAP-xxx`

**Referenz:** Appendix BM §2 "The Upgrade Workflow"

### Automatische Level-Erkennung

```bash
/upgrade-paper PAP-fehr1999theory

# Output:
# Current: Content L1, Integration I2
# Target:  Content L3, Integration I5
#
# Upgrade path:
# CONTENT (paper-intern):
# 1. [ ] Full text acquisition (L1 → L3)
#
# INTEGRATION (EBF-spezifisch):
# 2. [ ] Case Registry (I2 → I3)
# 3. [ ] Parameter extraction (I3 → I4)
# 4. [ ] Appendix + Chapter refs (I4 → I5)
```

### Level-spezifische Checklisten (MECE-konform)

**Content L0 → L1 (Bibliographic → Descriptive):**
```
├── [ ] abstract (REQUIRED)
├── [ ] keywords
└── [ ] publication_type, doi/doi_missing_reason
```

**Content L1 → L2 (Descriptive → Analytical):**
```
├── [ ] methodology
├── [ ] sample_description
├── [ ] key_findings
├── [ ] limitations
└── [ ] ~6k chars total
```
> ⚠️ MECE: Keine "parameters" hier! Das gehört zu Integration I4.

**Content L2 → L3 (Analytical → Complete):**
```
├── [ ] Full text in data/paper-texts/PAP-xxx.md
├── [ ] Paper's own bibliography extracted
└── [ ] >50k chars (CRITICAL THRESHOLD)
```

**Integration I1 (Classified):**
```
├── [ ] use_for = {LIT-XX, ...}
└── [ ] evidence_tier
```

**Integration I1 → I2 (Classified → Theorized):**
```
└── [ ] theory_support = {MS-XX-XXX, ...}
```

**Integration I2 → I3 (Theorized → Exemplified):**
```
└── [ ] Case Registry entry (CAS-XXX)
```

**Integration I3 → I4 (Exemplified → Parameterized):**
```
└── [ ] parameter = {lambda = X, beta = Y, ...}
└── [ ] Parameter Registry entry (PAR-XXX)
```
> ⚠️ MECE: Parameter-Extraktion gehört HIERHER, nicht zu Content!

**Integration I4 → I5 (Parameterized → Canonized):**
```
├── [ ] Appendix Reference
└── [ ] Chapter Reference
```

### NIEMALS

```
❌ Paper nur mit Content hinzufügen → Integration vergessen
❌ Paper nur verknüpfen ohne Content → Metadaten fehlen
❌ "Integration mache ich später" → Wird vergessen
❌ Batch-Content ohne Batch-Integration → Drift entsteht
❌ L3 behaupten ohne >50k chars Validierung
❌ Parameter bei Content L2 eintragen → Gehört zu Integration I4! (MECE)
❌ Dimensionen vermischen → Hält MECE-Axiom nicht ein
```

---

## Validierungs-Scripts

### Content-Dimension prüfen

```bash
# Felder-Coverage
python scripts/check_paper_content_coverage.py

# DOI-Reasons validieren
python scripts/validate_doi_missing_reasons.py
```

### Integration-Dimension prüfen

```bash
# use_for Coverage
python scripts/check_paper_integration.py --use-for

# theory_support Coverage
python scripts/check_paper_integration.py --theory
```

### Beide Dimensionen

```bash
# Vollständiger Quality Report
python scripts/paper_quality_report.py
```

---

## Dashboard (Gemessen 2026-02-01)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER DATABASE QUALITY DASHBOARD                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CONTENT LEVEL (L0-L3)                                                  │
│  ├── publication_type:     ████████████████████ 100%                   │
│  ├── doi (+reason):        ████████████████████ 100%                   │
│  ├── isbn (books):         ███████████████████░  98.6%                 │
│  ├── abstract:             ████████████████░░░░  82.8%                 │
│  └── key_findings:         ████████████████████ 100% (auto)            │
│                                                                         │
│  → Meiste Papers bei L1 (Basic Template)                               │
│  → Wenige bei L3 (Full Text >50k chars)                                │
│                                                                         │
│  INTEGRATION LEVEL (1-5)                                                │
│  ├── use_for:              ████████████████████ 100%                   │
│  ├── theory_support:       █████░░░░░░░░░░░░░░░  25%  ⚠️               │
│  ├── evidence_tier:        ████████████████████ 100%                   │
│  ├── parameter:            ███░░░░░░░░░░░░░░░░░  13%  ⚠️               │
│  ├── case_links:           ░░░░░░░░░░░░░░░░░░░░   0%  ❌               │
│  └── model_links:          ░░░░░░░░░░░░░░░░░░░░   0%  ❌               │
│                                                                         │
│  → Meiste Papers bei Level 2 (STANDARD)                                │
│  → Wenige bei Level 5 (FULL)                                           │
│                                                                         │
│  INTEGRATION SCORE: 68.8 / 100                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Nächste Prioritäten:**
1. theory_support 25% → 50%
2. case_links 0% → 10%
3. parameter 13% → 30%

---

## SSOT-Hierarchie (Single Source of Truth)

| Priorität | Datei | Beschreibung |
|-----------|-------|--------------|
| **1 (Primary)** | `appendices/BM_METHOD-PAPERINT_*.tex` | Formale Definitionen (L0-L3 × 1-5), Axiome |
| **2** | `data/paper-integration-metrics.yaml` | Workflow-Metriken, Zeitmessungen |
| **3** | `data/paper-integration-learnings.yaml` | Learnings, Error Patterns |
| **4** | `data/paper-integration-queue.yaml` | Papers to upgrade |
| **5** | `docs/frameworks/paper-database-quality-dimensions.md` | Diese Datei (Zusammenfassung) |

## Referenzen

**Appendix:**
- `appendices/BM_METHOD-PAPERINT_paper_integration_methodology.tex` - **SSOT für 2D-System**

**Scripts:**
- `scripts/check_paper_integration.py` - Misst Integration Level
- `scripts/add_doi_missing_reason.py` - DOI Accuracy
- `scripts/find_books_without_isbn.py` - ISBN Coverage

**Workflows:**
- `/upgrade-paper PAP-xxx` - Upgrade Content + Integration
- `/integrate-paper` - Neues Paper integrieren

**Data:**
- `data/paper-integration-metrics.yaml` - Workflow-Zeiten
- `data/paper-integration-learnings.yaml` - Learning Database
- `quality/lessons_learned.md` - Allgemeine Learnings

---

*Diese Datei ist eine Zusammenfassung. Die SSOT ist Appendix BM.*
