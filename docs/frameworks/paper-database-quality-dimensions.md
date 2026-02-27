# Paper Database Quality: 2-Dimensionen Framework

> **Version 2.0** | Februar 2026 | Aktualisiert auf strukturelle S1-S6 Definitionen
>
> **Changelog v2.0:** Content Level jetzt STRUKTURELL (S1-S6), nicht mehr
> zeichenbasiert. L3 Anforderungen R1-R4 dokumentiert. Phase A/B/ISBN
> Enrichment Ergebnisse integriert. Dashboard aktualisiert.
>
> ## SSOT (Single Source of Truth):
>
> | Datei | Beschreibung |
> |-------|--------------|
> | `appendices/BM_METHOD-PAPERINT_*.tex` | **Formale Definitionen** (L0-L3 × I0-I5) |
> | `docs/workflows/paper-level-upgrade-workflow.md` | **Upgrade-Workflow** (Phase A/B/ISBN) |
> | `data/paper-integration-queue.yaml` | Papers to upgrade |
>
> Erstellt: 2026-02-01
> Letzte Aktualisierung: 2026-02-11

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
F_C = {abstract, structural_characteristics (S1-S6), full_text, paper_bib}

Integration-Felder (EBF-spezifisch):
F_I = {use_for, evidence_tier, theory_support, case_links, parameter, appendix_refs, chapter_refs}

MECE-Constraint:
F_C ∩ F_I = ∅  (Mutually Exclusive)
```

### Level-Funktionen

```
Content Level C: Paper → {L0, L1, L2, L3}
- L0: nur bibliographische Felder, kein S1-S6
- L1: S1 (Research Question) bekannt
- L2: S1-S4 vorhanden (Summary/Extract, kein Volltext)
- L3: KOMPLETTER Originaltext + References (R1-R4 erfüllt)

Integration Level I: Paper → {I0, I1, I2, I3, I4, I5}
- I0: Nur Metadata (kein use_for)
- I1: use_for zugewiesen
- I2: I1 ∧ theory_support zugewiesen
- I3: I2 ∧ case_registry Eintrag
- I4: Dedicated Appendix
- I5: Full Framework Integration (alle Komponenten)
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

## Dimension 1: CONTENT LEVEL (L0-L3) — Paper-Intern

**Frage:** "Was wissen wir ÜBER das Paper?" (unabhängig von EBF)

### ⚠️ STRUKTURELLE Definition (S1-S6) — NICHT Zeichenzahl!

> **KRITISCH:** Content Level basiert auf dem Vorhandensein **struktureller
> Charakteristika S1-S6**, NICHT auf der Zeichenanzahl. Dies wurde in v2.0
> korrigiert (vorher fälschlicherweise zeichenbasiert).

### Die 6 Strukturellen Charakteristika (S1-S6)

| Code | Name | Beschreibung | Typische Quelle |
|------|------|-------------|-----------------|
| **S1** | Research Question | Forschungsfrage / Hypothese | Abstract, Einleitung |
| **S2** | Methodology | Methodik (RCT, Survey, Theory, etc.) | Methods-Sektion |
| **S3** | Sample/Data | Stichprobe, Daten, N | Methods/Data-Sektion |
| **S4** | Findings | Kernbefunde, Effektgrössen | Results-Sektion |
| **S5** | Validity | Interne/externe Validität, Limitationen | Discussion-Sektion |
| **S6** | Reproducibility | Reproduzierbarkeit, Daten-Zugang | Methods/Appendix |

**YAML-Feld:** `structural_characteristics` in `data/paper-references/PAP-{key}.yaml`

```yaml
structural_characteristics:
  S1_research_question: "How does loss aversion affect..."
  S2_methodology: "RCT with 2x2 design, N=450..."
  S3_sample_data: "Undergraduate students, University of Zurich..."
  S4_findings: "Loss aversion λ=2.25, significant at p<0.01..."
  S5_validity: "Internal validity high (randomized), external..."
  S6_reproducibility: "Data available on request, code in appendix..."
```

### Die 4 Content Levels (Strukturell)

| Level | Name | Definition | S-Felder |
|-------|------|-----------|----------|
| **L0** | Metadata Only | Nur bibliographische Daten (Author, Title, Year, DOI) | Kein S1-S6 |
| **L1** | Research Question | S1 (Research Question) bekannt, typischerweise aus Abstract | S1 |
| **L2** | Summary/Extract | S1-S4 vorhanden. Zusammenfassung oder Extract, aber KEIN Volltext | S1-S4 (optional S5-S6) |
| **L3** | Full Text | KOMPLETTER Originaltext archiviert, erfüllt R1-R4 | S1-S6 (alle) |

> **MECE-Regel:** Content Level enthält KEINE EBF-spezifischen Felder!
> Keine Parameter-Extraktion, keine theory_support, keine use_for — das gehört zu Integration.

### L3 Anforderungen (R1-R4)

L3 erfordert **alle vier** Bedingungen:

| Req | Anforderung | Validierung |
|-----|-------------|-------------|
| **R1** | Alle Original-Sektionen vorhanden | Sections prüfen |
| **R2** | References-Sektion mit allen Zitaten | Ref-Count prüfen |
| **R3** | >10k Wörter (Artikel) / >5k (Short Paper) | `wc -w` auf .md |
| **R4** | KEINE EBF-Sektionen im Volltext (.md) | Grep auf EBF-Keywords |

**Separation of Concerns:**
- `.md` Datei = NUR Original-Text des Papers (R4!)
- `.yaml` Datei = ALLE EBF-Metadaten (S1-S6, use_for, theory_support, etc.)

```bash
# L3 Validierung
python scripts/validate_fulltext_completeness.py PAP-{key}
```

### Content-Felder im YAML

| Feld | Beschreibung | Level |
|------|--------------|-------|
| `title`, `author`, `year`, `doi` | Bibliographische Daten | L0+ |
| `abstract` | Zusammenfassung | L1+ |
| `abstract_fetched`, `abstract_source` | Herkunft des Abstracts | L1+ |
| `structural_characteristics.S1-S6` | Strukturelle Charakteristika | L1+ (S1) bis L2+ (S1-S4) |
| `full_text.available`, `full_text.path` | Volltext-Referenz | L3 |
| `publication_type` | Taxonomie | L0+ |
| `isbn` | Für Bücher/Buchkapitel | L0+ |

### Publication Type Taxonomie

```
journal_article   → DOI erwartet
book              → ISBN erwartet, DOI optional
book_chapter      → ISBN optional, DOI optional
handbook_chapter  → ISBN optional, DOI optional
conference_paper  → DOI erwartet
working_paper     → DOI optional
report            → DOI optional
```

---

## Dimension 2: INTEGRATION LEVEL (I0-I5) — EBF-Spezifisch

**Frage:** "Wie tief ist das Paper mit EBF VERKNÜPFT?" (unabhängig vom Paper-Inhalt)

### Die 6 Integration Levels

| Level | Name | Komponenten |
|-------|------|-------------|
| **I0** | None | Nur Metadata (kein use_for) |
| **I1** | Minimal | `use_for` zugewiesen |
| **I2** | Standard | + `theory_support` (MS-XX-XXX Links) |
| **I3** | Case | + Case Registry Eintrag (CAS-XXX) |
| **I4** | Dedicated | Dedicated Appendix (LIT-XX, DOMAIN-XX) |
| **I5** | Full | Full Framework Integration (alle Komponenten) |

> **MECE-Regel:** Integration Level enthält KEINE paper-internen Informationen!
> Kein Abstract, keine Methodology, keine Findings — das gehört zu Content.

### Integration-Felder pro Level (MECE-konform)

| Level | BibTeX-Felder | YAML-Felder | Registry-Einträge |
|-------|---------------|-------------|-------------------|
| I0 | Basis (title, author, year) | superkey, paper | - |
| I1 | `use_for`, `evidence_tier` | ebf_integration.use_for | - |
| I2 | + `theory_support` | ebf_integration.theory_support | MS-XX-XXX Links |
| I3 | I2 | + case_integration | CAS-XXX |
| I4 | I3 | + appendix_integration | Dedizierter Appendix |
| I5 | I4 | + chapter_relevance, parameter_contributions | Volle Cross-Refs |

### I5 Vollständige Komponenten (9 Required)

Für Level I5 müssen **alle 9 Komponenten** vorhanden sein:

```
☐ 1. BibTeX-Eintrag (bcm_master.bib)
☐ 2. Paper-YAML (data/paper-references/PAP-{key}.yaml)
☐ 3. theory_support (MS-XX-XXX)
☐ 4. Case Registry (CAS-XXX)
☐ 5. Theory Catalog Eintrag (wenn neue Theorie)
☐ 6. Parameter Registry (PAR-XXX, wenn Parameter extrahiert)
☐ 7. Full Text (data/paper-texts/PAP-{key}.md)
☐ 8. LIT-Appendix Integration
☐ 9. Chapter References
```

---

## Kombinierte Qualitäts-Matrix (L0-L3 × I0-I5)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER QUALITY = CONTENT (L0-L3) × INTEGRATION (I0-I5)                  │
│  [MECE: Content = paper-intern | Integration = EBF-spezifisch]          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                        INTEGRATION LEVEL                                │
│                        I0-I2               I4-I5                        │
│                    ┌───────────────────┬───────────────────┐            │
│                    │                   │                   │            │
│        L3          │   CONTENT-ONLY    │   VOLLSTÄNDIG     │            │
│        (Full Text) │   ⚠️ Isoliert     │   ✅ Ideal        │            │
│                    │   (kein EBF-Link) │   (L3, I5)        │            │
│ CONTENT LEVEL      ├───────────────────┼───────────────────┤            │
│ (L0-L3)            │                   │                   │            │
│ (paper-intern)     │   MINIMAL         │   INTEGRATION-    │            │
│        L0-L1       │   ❌ Nur Entry    │   ONLY ⚠️         │            │
│        (Metadata)  │                   │   (EBF-Links ohne │            │
│                    │                   │    Paper-Inhalt)  │            │
│                    └───────────────────┴───────────────────┘            │
│                                                                         │
│  ZIEL: Content L3 × Integration I5 = Complete + Full Integration        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Prior Score π(p) ∈ [0,1] — Integrations-Entscheidung

**Referenz:** Appendix BM §1.1 Definitionen 5-8

### Kernidee

```
Prior Score = Σ (Gewicht × EBF-Bedarf × Paper-Angebot × Zeitfaktor × Konfidenz)

π(p) = Σᵢ wᵢ · gᵢ · sᵢ(p) · τ(p) · ρ(C)
```

wobei:
- **G = (g₁...g₆)**: Gap-Vektor (was EBF braucht)
- **S(p) = (s₁...s₆)**: Supply-Vektor (was Paper liefert)
- **τ(p)**: Temporal Decay Factor (Halbwertszeit 15 Jahre)
- **ρ(C)**: Confidence Multiplier basierend auf Content Level

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

### Temporal Decay Factor τ(p)

```
τ(p) = 2^(-age/15)

wobei age = current_year - publication_year
Halbwertszeit: 15 Jahre
```

| Alter | τ(p) | Beispiel |
|-------|------|----------|
| 0 Jahre | 1.00 | Paper von 2026 |
| 15 Jahre | 0.50 | Paper von 2011 |
| 30 Jahre | 0.25 | Paper von 1996 |
| 50 Jahre | 0.10 | Paper von 1976 |

### Confidence Multiplier ρ(C)

| Content Level | ρ(C) | Begründung |
|---------------|------|------------|
| L0 (Metadata Only) | 0.60 | Nur Heuristiken (Journal, Autor, Title) |
| L1 (Research Question) | 0.80 | Abstract gibt Methodik- und Domain-Signale |
| L2 (Summary) | 0.95 | Konkrete Findings und Sample-Details |
| L3 (Full Text) | 1.00 | Volle Beobachtung, keine Unsicherheit |

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

### Axiom MECE-5: Monotone Informationsverfeinerung

```
k₁ < k₂ ⟹ Var[Ŝ_k₁(p)] ≥ Var[Ŝ_k₂(p)]
```

Mehr Content = weniger Unsicherheit (nie mehr).

---

## Phase A/B: Automatisierte Content Level Upgrades

### Phase A: Abstract-Parsing (L1→L2)

**Script:** `scripts/upgrade_l1_to_l2_from_abstract.py`
**Methodik:** Automatische Extraktion von S2-S4 aus vorhandenen Abstracts
**Ergebnis:** 594 Papers L1→L2 upgegraded

Drei Ansätze:
1. **Explicit Pattern Matching** — Direktes Erkennen von Methodik-Keywords
2. **Sentence-Level Classification** — Sätze nach S2/S3/S4 Gehalt klassifizieren
3. **Structured Summary** — Zusammenfassung wenn keine klare Struktur

### Phase B: Multi-Source Mining (L1→L2)

**Script:** `scripts/upgrade_l1_to_l2_phase_b.py`
**Methodik:** 5 komplementäre Enrichment-Ansätze für verbleibende L1 Papers
**Ergebnis:** 429 Papers L1→L2 upgegraded

Die 5 Ansätze:
- **B1:** BibTeX-Feld-Mining (journal, note, keywords, etc.)
- **B2:** Titel-Analyse (Methodik-Signale im Titel)
- **B3:** Cross-Reference (verwandte Papers als Kontext)
- **B4:** Journal-basierte Inferenz (typische Methodik für das Journal)
- **B5:** DOI-basierte Typ-Inferenz

Zwei Inferenz-Methoden:
- **Direct Evidence:** Explizite Informationen in vorhandenen Feldern
- **Structured Inference:** Logische Ableitung aus bekannten Metadaten

### ISBN Enrichment

**Script:** `scripts/add_isbn_to_books.py`
**Methodik:** 7 Batches via WebSearch
**Ergebnis:** 313/318 Bücher (98.4%) haben ISBN-13

**Vollständige Dokumentation:** `docs/workflows/paper-level-upgrade-workflow.md`

---

## Workflow: /upgrade-paper

**Skill:** `/upgrade-paper PAP-xxx`

### Automatische Level-Erkennung

```bash
/upgrade-paper PAP-fehr1999theory

# Output:
# Current: Content L1, Integration I2
# Target:  Content L3, Integration I5
#
# Upgrade path:
# CONTENT (paper-intern):
# 1. [ ] Extract S2-S4 from abstract (L1 → L2)
# 2. [ ] Full text acquisition (L2 → L3)
#
# INTEGRATION (EBF-spezifisch):
# 3. [ ] Case Registry (I2 → I3)
# 4. [ ] Dedicated Appendix (I3 → I4)
# 5. [ ] Full cross-refs (I4 → I5)
```

### Level-spezifische Checklisten (MECE-konform)

**Content L0 → L1 (Metadata → Research Question):**
```
├── [ ] abstract (REQUIRED)
├── [ ] S1_research_question extrahiert
├── [ ] keywords
└── [ ] publication_type, doi/doi_missing_reason
```

**Content L1 → L2 (Research Question → Summary):**
```
├── [ ] S2_methodology — Methodik identifiziert
├── [ ] S3_sample_data — Stichprobe/Daten bekannt
├── [ ] S4_findings — Kernbefunde extrahiert
└── [ ] Optional: S5_validity, S6_reproducibility
```
> ⚠️ MECE: Keine "parameters" hier! Das gehört zu Integration I4+.

**Content L2 → L3 (Summary → Full Text):**
```
├── [ ] Full text in data/paper-texts/PAP-xxx.md
├── [ ] R1: Alle Original-Sektionen vorhanden
├── [ ] R2: References-Sektion komplett
├── [ ] R3: >10k Wörter (Artikel) / >5k (Short Paper)
├── [ ] R4: KEINE EBF-Sektionen im Volltext
└── [ ] python scripts/validate_fulltext_completeness.py PAP-xxx
```

**Integration I0 → I1 (None → Minimal):**
```
├── [ ] use_for = {LIT-XX, ...} in BibTeX
└── [ ] evidence_tier in BibTeX
```

**Integration I1 → I2 (Minimal → Standard):**
```
└── [ ] theory_support = {MS-XX-XXX, ...} in BibTeX
```

**Integration I2 → I3 (Standard → Case):**
```
└── [ ] Case Registry entry (CAS-XXX) in case-registry.yaml
```

**Integration I3 → I4 (Case → Dedicated):**
```
└── [ ] Dedicated Appendix (LIT-XX oder DOMAIN-XX)
```

**Integration I4 → I5 (Dedicated → Full):**
```
├── [ ] chapter_relevance in Paper-YAML
├── [ ] parameter_contributions (wenn Parameter extrahiert)
├── [ ] theory_integration
├── [ ] case_integration
└── [ ] context_integration
```

### NIEMALS

```
❌ Paper nur mit Content hinzufügen → Integration vergessen
❌ Paper nur verknüpfen ohne Content → Metadaten fehlen
❌ "Integration mache ich später" → Wird vergessen
❌ Batch-Content ohne Batch-Integration → Drift entsteht
❌ L3 behaupten ohne R1-R4 Validierung
❌ L2 behaupten ohne S1-S4 strukturelle Felder
❌ Content Level nach Zeichenzahl beurteilen → Ist STRUKTURELL (S1-S6)!
❌ Parameter bei Content L2 eintragen → Gehört zu Integration I4! (MECE)
❌ Dimensionen vermischen → Hält MECE-Axiom nicht ein
```

---

## Validierungs-Scripts

### Content-Dimension prüfen

```bash
# Paper-YAML Schema validieren (S1-S6 Struktur)
python scripts/validate_paper_yaml_schema.py

# Volltext-Completeness (R1-R4 für L3)
python scripts/validate_fulltext_completeness.py

# DOI-Reasons validieren
python scripts/validate_doi_missing_reasons.py
```

### Integration-Dimension prüfen

```bash
# BibTeX-YAML Consistency (Level Gate)
python scripts/validate_bibtex_yaml_consistency.py

# use_for / theory_support Coverage
python scripts/check_paper_integration.py
```

### Beide Dimensionen

```bash
# Vollständiger Quality Report
python scripts/paper_quality_report.py
```

---

## Dashboard (Stand: 2026-02-09)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER DATABASE QUALITY DASHBOARD (2,347 Papers)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CONTENT LEVEL (L0-L3) — Strukturell (S1-S6)                           │
│  ├── L0 (Metadata Only):  343 Papers (15%)                             │
│  ├── L1 (Research Q.):  1,933 Papers (82%)                             │
│  ├── L2 (Summary):         61 Papers  (3%)                             │
│  └── L3 (Full Text):       10 Papers  (<1%)                            │
│                                                                         │
│  CONTENT ENRICHMENT:                                                    │
│  ├── abstract:          ████████████████░░░░  82.8%                    │
│  ├── S1 (Research Q.):  █████████████████░░░  85%                      │
│  ├── S2-S4:             ████████████████████  ~44% (1,023 via A+B)     │
│  ├── publication_type:  ████████████████████ 100%                      │
│  ├── doi (+reason):     ████████████████████ 100%                      │
│  └── isbn (books):      ███████████████████░  98.4% (313/318)          │
│                                                                         │
│  INTEGRATION LEVEL (I0-I5)                                              │
│  ├── I0 (None):            0 Papers                                    │
│  ├── I1 (Minimal):     1,766 Papers (70%)                              │
│  ├── I2 (Standard):      421 Papers (17%)                              │
│  ├── I3 (Case):            0 Papers                                    │
│  ├── I4 (Dedicated):     343 Papers (13%)                              │
│  └── I5 (Full):            0 Papers                                    │
│                                                                         │
│  PRIOR SCORE π(p):                                                      │
│  ├── Confidence ρ: L0=0.60, L1=0.80, L2=0.95, L3=1.00                 │
│  └── Decay τ: half-life 15 years                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Nächste Prioritäten:**
1. L1→L2 für verbleibende ~900 Papers (weitere Enrichment-Strategien)
2. theory_support Coverage erhöhen (aktuell ~25%)
3. Case Registry Links aufbauen (aktuell ~0%)
4. L2→L3 für Kern-Papers (Volltext-Akquisition)

---

## SSOT-Hierarchie (Single Source of Truth)

| Priorität | Datei | Beschreibung |
|-----------|-------|--------------|
| **1 (Primary)** | `appendices/BM_METHOD-PAPERINT_*.tex` | Formale Definitionen (L0-L3 × I0-I5), Axiome |
| **2** | `docs/workflows/paper-level-upgrade-workflow.md` | Upgrade-Workflow, Phase A/B/ISBN Methodik |
| **3** | `docs/frameworks/paper-database-quality-dimensions.md` | Diese Datei (Zusammenfassung) |
| **4** | `data/paper-integration-queue.yaml` | Papers to upgrade |

## Referenzen

**Appendix:**
- `appendices/BM_METHOD-PAPERINT_paper_integration_methodology.tex` - **SSOT für 2D-System**

**Scripts:**
- `scripts/validate_paper_yaml_schema.py` - Schema-Validierung (S1-S6 Struktur)
- `scripts/validate_fulltext_completeness.py` - L3 Volltext-Validierung (R1-R4)
- `scripts/validate_bibtex_yaml_consistency.py` - BibTeX-YAML Level Gate
- `scripts/upgrade_l1_to_l2_from_abstract.py` - Phase A Upgrade-Script
- `scripts/upgrade_l1_to_l2_phase_b.py` - Phase B Upgrade-Script
- `scripts/add_isbn_to_books.py` - ISBN Enrichment (7 Batches)
- `scripts/add_doi_missing_reason.py` - DOI Accuracy
- `scripts/find_books_without_isbn.py` - ISBN Coverage

**Workflows:**
- `/upgrade-paper PAP-xxx` - Upgrade Content + Integration
- `/integrate-paper` - Neues Paper integrieren
- `/paper-search` - Paper suchen und anreichern

**Data:**
- `data/paper-references/PAP-{key}.yaml` - SSOT Paper-Metadaten
- `data/paper-texts/PAP-{key}.md` - SSOT Volltexte
- `bibliography/bcm_master.bib` - SSOT BibTeX
- `data/paper-integration-queue.yaml` - Upgrade Queue

---

*Version 2.0 | Februar 2026*
*Content Level ist STRUKTURELL (S1-S6), nicht zeichenbasiert.*
