# Paper Level Upgrade Workflow

> Version 2.0 | Februar 2026 | Status: PFLICHT-Workflow
>
> **Changelog v2.0:** Komplett überarbeitet. Content Level jetzt STRUKTURELL
> (S1-S6), nicht mehr zeichenbasiert. Pfade aktualisiert. Phase A/B/ISBN
> Enrichment dokumentiert.

---

## Übersicht: Das 2D Klassifikationssystem

Papers werden in **zwei orthogonalen Dimensionen** klassifiziert (Axiom MECE-1):

```
┌─────────────────────────────────────────────────────────────────────────┐
│  2D PAPER CLASSIFICATION SYSTEM (Definition 2 + Definition 3)           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DIMENSION 1: CONTENT LEVEL C(p) — Was wissen wir über das Paper?      │
│  ─────────────────────────────────────────────────────────────────      │
│  L0 │ METADATA ONLY  │ Kein S1-S6 vorhanden                            │
│  L1 │ RESEARCH Q.    │ S1 (Research Question) bekannt                   │
│  L2 │ SUMMARY        │ S1-S4 vorhanden (Summary/Extract, kein Volltext) │
│  L3 │ FULL TEXT      │ KOMPLETTER Originaltext + References (R1-R4)     │
│                                                                         │
│  DIMENSION 2: INTEGRATION LEVEL I(p) — Wie tief EBF-integriert?        │
│  ─────────────────────────────────────────────────────────────────      │
│  I0 │ NONE       │ Nur Metadata                                        │
│  I1 │ MINIMAL    │ use_for zugewiesen                                   │
│  I2 │ STANDARD   │ + theory_support                                     │
│  I3 │ CASE       │ + case_registry                                      │
│  I4 │ DEDICATED  │ Dedicated Appendix                                   │
│  I5 │ FULL       │ Full Framework Integration                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### MECE-Axiome

| Axiom | Aussage |
|-------|---------|
| **MECE-1** | Content und Integration sind **semantisch orthogonal** |
| **MECE-2** | P(C=Lx \| I=Iy) = P(C=Lx) — statistisch unabhängig |
| **MECE-3** | Jedes Feld gehört zu **genau einer** Dimension (XOR) |

**Formale SSOT:** `appendices/BM_METHOD-PAPERINT_paper_integration_methodology.tex`
**Zusammenfassung:** `docs/frameworks/paper-database-quality-dimensions.md`

---

## Content Level: Strukturelle Definition (S1-S6)

### Die 6 Strukturellen Charakteristika

| Code | Name | Beschreibung |
|------|------|-------------|
| **S1** | Research Question | Forschungsfrage / Hypothese |
| **S2** | Methodology | Methodik (RCT, Survey, Theory, etc.) |
| **S3** | Sample/Data | Stichprobe, Daten, N |
| **S4** | Findings | Ergebnisse, Koeffizienten, Effektgrössen |
| **S5** | Validity | Interne/externe Validität, Limitationen |
| **S6** | Reproducibility | Reproduzierbarkeit, Daten/Code verfügbar |

### Content Level Definitionen

#### Level 0: Metadata Only
- **Kriterium:** Kein S1-S6 vorhanden
- **Dateien:** Nur `bibliography/bcm_master.bib` (bibliographische Felder)
- **YAML:** `data/paper-references/PAP-{key}.yaml` mit `content_level: L0`

#### Level 1: Research Question (S1)
- **Kriterium:** Mindestens S1 vorhanden (Research Question bekannt)
- **Typisch:** Abstract vorhanden → S1 kann abgeleitet werden
- **YAML-Felder:**
  ```yaml
  structural_characteristics:
    S1_research_question: "..."
  ```

#### Level 2: Summary/Extract (S1-S4)
- **Kriterium:** S1 + S2 + S3 + S4 vorhanden ODER Summary/Extract
- **KEIN Volltext erforderlich** — eine gute Zusammenfassung reicht
- **YAML-Felder:**
  ```yaml
  structural_characteristics:
    S1_research_question: "..."
    S2_methodology: "..."
    S3_sample_data: "..."
    S4_findings: "..."
  ```
- **Optional:** S5, S6 (erhöhen Qualitätsscore, aber nicht Level-relevant)

#### Level 3: Full Text (R1-R4)
- **Kriterium:** Alle 4 R-Anforderungen erfüllt
- **Dateien:** `data/paper-texts/PAP-{key}.md` (SSOT für Volltext)
- **YAML-Verweis:**
  ```yaml
  full_text:
    available: true
    path: "data/paper-texts/PAP-{key}.md"
    format: "markdown"
    archived_date: "YYYY-MM-DD"
  ```

**R-Anforderungen für L3:**

| Code | Anforderung | Prüfung |
|------|-------------|---------|
| **R1** | Alle Original-Sektionen vorhanden | Sektionsstruktur des Originals |
| **R2** | References-Sektion mit allen Zitaten | Vollständige Bibliographie |
| **R3** | >10k Wörter (Artikel) / >5k (Short Paper) | `wc -w` |
| **R4** | Keine EBF-Sektionen im Volltext | Nur Original-Text, kein "Key Parameters Extracted" etc. |

**Validierung:**
```bash
python scripts/validate_fulltext_completeness.py PAP-{key}
```

**KRITISCH — Separation of Concerns:**
- `.md` Datei = **NUR** Original-Text (R4!)
- `.yaml` Datei = **ALLE** EBF-Metadaten (S1-S6, parameter_contributions, etc.)

---

## SSOTs (Single Sources of Truth)

| Was | SSOT-Pfad | Format |
|-----|-----------|--------|
| **BibTeX-Einträge** | `bibliography/bcm_master.bib` | BibTeX |
| **Paper-Metadaten** | `data/paper-references/PAP-{key}.yaml` | YAML |
| **Volltexte** | `data/paper-texts/PAP-{key}.md` | Markdown |

**Bidirektionale Konsistenz:** Jeder BIB-Eintrag hat genau 1 YAML-Datei.
**Validation:** `python scripts/validate_bibtex_yaml_consistency.py`

---

## Integration Level Komponenten

### I0: None
- Nur Metadata in YAML, keine EBF-Felder

### I1: MINIMAL (~5 min)
```
☐ BibTeX-Eintrag in bcm_master.bib
  ├── title, author, year, journal, doi
  ├── evidence_tier (1/2/3)
  └── use_for = {LIT-XX, ...}
```

### I2: STANDARD (~15 min)
```
☐ I1 Komponenten
☐ EBF-Felder in BibTeX:
  ├── theory_support = {MS-XX-XXX, ...}
  └── parameter = {key = value, ...} (falls vorhanden)
```

### I3: CASE (~20 min)
```
☐ I2 Komponenten
☐ Case Registry (data/case-registry.yaml):
  ├── id: CAS-XXX (via registry_manager.py!)
  ├── paper_ref: PAP-xxx
  ├── 10c_mapping (alle 10 Dimensionen)
  └── insight + implication
```

### I4: DEDICATED APPENDIX (~60 min)
```
☐ I3 Komponenten (optional — nicht alle I4 haben Cases)
☐ Appendix Reference:
  ├── Dedicated LIT-Appendix oder Section
  ├── Annotated Bibliography Eintrag
  └── use_for in BibTeX aktualisiert
```

### I5: FULL FRAMEWORK (~90+ min)
```
☐ I4 Komponenten
☐ Theory Catalog (data/theory-catalog.yaml):
  ├── Neuer MS-XX-XXX Eintrag ODER bestehenden erweitern
  └── ebf_restrictions dokumentieren
☐ Parameter Registry (data/parameter-registry.yaml):
  └── PAR-XXX-NNN für neue Parameter
☐ Chapter References in chapters/*.tex
☐ CORE Appendix Integration (6-Faktoren-Analyse)
```

---

## Automatisierte Upgrade-Methoden

### Phase A: Abstract-Based L1→L2 (Batch)

**Script:** `scripts/upgrade_papers_l2.py`
**Methode:** Parst bestehende Abstracts und extrahiert S1-S4 automatisch

```bash
# Status prüfen
python scripts/upgrade_papers_l2.py --stats

# Dry-run (zeigt was sich ändern würde)
python scripts/upgrade_papers_l2.py --dry-run --batch 50

# Anwenden
python scripts/upgrade_papers_l2.py --apply --batch 50
```

**Wie es funktioniert:**
1. Liest Abstract aus YAML
2. Extrahiert S1 (Research Question) aus Abstract-Sätzen
3. Inferiert S2 (Methodology) aus Schlüsselwörtern (RCT, survey, model, etc.)
4. Inferiert S3 (Sample/Data) aus Abstract + Journal-Typ
5. Extrahiert S4 (Findings) aus Abstract-Schlusssätzen
6. Schreibt `structural_characteristics` in YAML
7. Aktualisiert `content_level` und `prior_score`

**Ergebnis Phase A:** 594 Papers von L1→L2 upgegraded (Februar 2026)

### Phase B: Multi-Source Mining L1→L2 (Batch)

**Script:** `scripts/upgrade_papers_l2_phase_b.py`
**Methode:** Nutzt 5 Approaches + 2 Inferenz-Methoden für Papers, die Phase A nicht upgraden konnte

```bash
# Status prüfen
python scripts/upgrade_papers_l2_phase_b.py --stats

# Anwenden
python scripts/upgrade_papers_l2_phase_b.py --apply --batch 50
```

**5 Approaches:**

| Approach | Quelle | Extrahiert |
|----------|--------|-----------|
| **B1** | `key_findings_structured` | S4 (Findings) |
| **B2** | `behavioral_mapping` | S2 (Methodology), S3 (Sample), S4 |
| **B3** | `ebf_integration.parameter_contributions` | S4 (Parameter-Werte) |
| **B4** | `abstract` (tiefes Parsing) | S2, S3, S4 via Keyword-Matching |
| **B5** | `ebf_integration.theory_support` + `theory-catalog.yaml` | S2 (von Theory-Methodik) |

**Inferenz-Methoden:**

| Methode | Logik |
|---------|-------|
| **S3-Inferenz** | Journal-Typ → Sample-Art (z.B. "AER" → "Peer-reviewed empirical") |
| **B4b** | Papers in STRONG_EMPIRICAL_JOURNALS mit Abstract >150 chars → S4 inferiert |

**Ergebnis Phase B:** 429 Papers von L1→L2 upgegraded (Februar 2026)

### Gesamt-Ergebnis Phase A+B

```
VOR Phase A:  L0=343, L1=1933, L2=61,  L3=10
NACH Phase A: L0=343, L1=1339, L2=655, L3=10
NACH Phase B: L0=343, L1=910,  L2=1084, L3=10
                                ↑ +1023 Papers upgegraded
```

---

## ISBN Enrichment (BibTeX-Qualität)

**Script:** `scripts/add_isbn_to_books.py`
**Ziel:** ISBN-13 für alle @book und @incollection Einträge

```bash
# Status
python scripts/add_isbn_to_books.py --stats

# Dry-run
python scripts/add_isbn_to_books.py --dry-run

# Anwenden
python scripts/add_isbn_to_books.py --apply
```

**7 Batches (Februar 2026):**

| Batch | Methode | Einträge | Kumulativ |
|-------|---------|----------|-----------|
| 1-5 | Standalone @book (bekannte Verlage) | 244 | 244/318 (77%) |
| 6 | @incollection (Parent-Handbook ISBNs) | 41 | 285/318 (90%) |
| 7 | WebSearch (Klassiker + Reprints) | 28 | 313/318 (98%) |

**Verbleibende 5 ohne ISBN:**
- `hurwicz1960optimality` — Parent-Volume nicht identifizierbar
- `aquinas1265summa` — Kein Standard-ISBN für Gesamtwerk
- `benabou_henkel_2025` — Forthcoming
- `schelling1974command` — Booktitle-Mismatch im BibTeX
- `schelling1988value` — Booktitle-Mismatch im BibTeX

---

## Workflow: Paper von Level X zu Level Y upgraden

### Schritt 1: Status prüfen

```bash
# Content Level aus YAML lesen
python scripts/validate_paper_yaml_schema.py PAP-{key}

# Oder direkt:
grep "content_level" data/paper-references/PAP-{key}.yaml

# Integration Level prüfen
grep "integration_level" data/paper-references/PAP-{key}.yaml

# Volltext vorhanden?
ls data/paper-texts/PAP-{key}.md 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

### Schritt 2: Content Level erhöhen

**L0 → L1:** Abstract hinzufügen
```yaml
# In PAP-{key}.yaml:
abstract: "..."
structural_characteristics:
  S1_research_question: "..."
```

**L1 → L2:** S2-S4 ergänzen (manuell oder via Phase A/B Scripts)
```yaml
structural_characteristics:
  S1_research_question: "..."
  S2_methodology: "..."
  S3_sample_data: "..."
  S4_findings: "..."
```

**L2 → L3:** Volltext archivieren
1. Original-PDF Text in `data/paper-texts/PAP-{key}.md` speichern
2. Nur Original-Text (R4: keine EBF-Sektionen!)
3. References-Sektion beibehalten (R2: wertvollste Daten!)
4. Validieren: `python scripts/validate_fulltext_completeness.py PAP-{key}`
5. YAML aktualisieren: `full_text.available: true`

### Schritt 3: Integration Level erhöhen

**I0 → I1:** `use_for` in BibTeX zuweisen
```bibtex
use_for = {LIT-FEHR, DOMAIN-SOCIAL},
evidence_tier = {1},
```

**I1 → I2:** `theory_support` in BibTeX ergänzen
```bibtex
theory_support = {MS-SP-001, MS-IB-001},
```

**I2 → I3:** Case in `data/case-registry.yaml` erstellen
```bash
python scripts/registry_manager.py case --next  # → CAS-XXX
```

**I3 → I4:** Dedicated Appendix Section erstellen

**I4 → I5:** Full Framework Integration (6-Faktoren-Analyse)
→ Siehe `docs/workflows/level5-paper-integration-workflow.md`

### Schritt 4: Validieren & Committen

```bash
# Schema-Validierung
python scripts/validate_paper_yaml_schema.py

# BibTeX↔YAML Konsistenz
python scripts/validate_bibtex_yaml_consistency.py

# Commit
git add data/paper-references/PAP-{key}.yaml bibliography/bcm_master.bib
git commit -m "feat(PAP-{key}): Upgrade to C=L2, I=I2"
```

---

## Prior Score π(p)

Der Prior Score quantifiziert den Wert eines Papers für das EBF:

```
π(p) = Σᵢ wᵢ · gᵢ · sᵢ(p) · τ(p) · ρ(C)

Wobei:
  wᵢ    = Gewicht der Komponente i
  gᵢ    = Gap-Vektor (was EBF braucht)
  sᵢ(p) = Supply-Vektor (was Paper liefert)
  τ(p)  = Temporal Decay (Halbwertszeit 15 Jahre)
  ρ(C)  = Confidence Multiplier nach Content Level:
           L0=0.60, L1=0.80, L2=0.95, L3=1.00
```

**Automatische Berechnung:** `python scripts/validate_paper_yaml_schema.py`

---

## Datenbank-Status (Live)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER DATABASE STATUS (2,347 Papers)                                   │
│  Letzte Validierung: 2026-02-11                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CONTENT LEVEL C(p):                                                    │
│  ├── L0:    343 Papers (15%) — Metadata only                            │
│  ├── L1:    910 Papers (39%) — Research Question (S1)                   │
│  ├── L2:  1,084 Papers (46%) — Summary (S1-S4)                          │
│  └── L3:     10 Papers       — Volltext (R1-R4)                         │
│                                                                         │
│  INTEGRATION LEVEL I(p):                                                │
│  ├── I0:      0 Papers       — Metadata only                            │
│  ├── I1:  1,766 Papers (70%) — use_for assigned                         │
│  ├── I2:    421 Papers (17%) — + theory_support                         │
│  ├── I3:      0 Papers       — + case_registry                          │
│  ├── I4:    343 Papers (13%) — Dedicated Appendix                       │
│  └── I5:      0 Papers       — Full Framework Integration               │
│                                                                         │
│  BIBTEX QUALITÄT:                                                       │
│  ├── Total @book/@incollection: 318                                     │
│  ├── Mit ISBN-13:               313 (98.4%)                              │
│  └── Ohne ISBN:                   5 (nicht lösbar)                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Kapitel-Thema Mapping

| Thema | Kapitel | Appendix |
|-------|---------|----------|
| Loss Aversion, Prospect Theory | Ch. 10 | LIT-KT |
| Social Preferences, Fairness | Ch. 7 | LIT-FEHR |
| Time Preferences, Discounting | Ch. 8 | LIT-DISCOUNTING |
| Belief Updating, Advice | Ch. 11 | LIT-LEARNING |
| Nudging, Defaults, Interventions | Ch. 17 | HHH (METHOD-TOOLKIT) |
| Framing, Context | Ch. 9 | LIT-FRAMING |
| Identity, Self-Image | Ch. 10 | LIT-BENABOU |

---

## Validierungs-Scripts

| Script | Prüft | Blockiert Commit? |
|--------|-------|-------------------|
| `validate_paper_yaml_schema.py` | YAML-Schema, Content/Integration Level | Nein |
| `validate_bibtex_yaml_consistency.py` | BIB↔YAML Konsistenz, Level Gate | **Ja** (Level 5 Overclaim) |
| `validate_fulltext_completeness.py` | L3 R1-R4 Anforderungen | Nein |
| `validate_referential_integrity.py` | Cross-DB Referenzen | **Ja** (Score <85%) |

---

## Referenzen

| Datei | Beschreibung |
|-------|--------------|
| `data/paper-references/PAP-{key}.yaml` | Paper-Metadaten (SSOT) |
| `data/paper-texts/PAP-{key}.md` | Volltexte (SSOT) |
| `bibliography/bcm_master.bib` | BibTeX-Einträge (SSOT) |
| `data/paper-integration-queue.yaml` | Upgrade-Queue |
| `data/paper-integration-learnings.yaml` | Learning Database |
| `docs/frameworks/paper-database-quality-dimensions.md` | Formale Axiome |
| `docs/workflows/paper-workflow-overview.md` | Zentrale Übersicht |
| `docs/workflows/level5-paper-integration-workflow.md` | Level 5 Detail |
| `appendices/BM_METHOD-PAPERINT_*.tex` | Formaler Appendix |

---

*Version 2.0 | Komplett überarbeitet 2026-02-11*
*Basiert auf Sessions 2026-01-31 bis 2026-02-11 (Phase A, Phase B, ISBN Enrichment)*
