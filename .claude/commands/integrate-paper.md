# /integrate-paper - Paper Integration Workflow (12 Schritte)

## Übersicht

Automatischer Workflow zur Integration wissenschaftlicher Papers in das EBF Framework.
**MUSS bei JEDEM neuen Paper verwendet werden** - nicht optional!

## Der 12-Schritt PIP-Workflow (PFLICHT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  12-SCHRITT PAPER INTAKE PROTOCOL (PIP)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1:  KLASSIFIZIEREN    → 7 Kriterien, Score berechnen          │
│  SCHRITT 2:  LEVEL BESTIMMEN   → 1-MINIMAL bis 5-FULL                  │
│  SCHRITT 3:  WP-PUB-CHECK      → Bei Working Paper: Journal prüfen     │
│  SCHRITT 4:  PIP ERSTELLEN     → data/paper-intake/YYYY/PIP-xxx.yaml   │
│  SCHRITT 5:  BIBTEX ANLEGEN    → bibliography/bcm_master.bib           │
│  SCHRITT 6:  PAPER-REFERENCE   → data/paper-references/PAP-xxx.yaml    │
│  SCHRITT 7:  FULL TEXT         → data/paper-texts/PAP-xxx.md (SSOT!)   │
│  SCHRITT 8:  THEORY CATALOG    → data/theory-catalog.yaml (Level 4-5)  │
│  SCHRITT 9:  PARAMETER REG.    → data/parameter-registry.yaml          │
│  SCHRITT 10: CASE REGISTRY     → data/case-registry.yaml (Level 3-5)   │
│  SCHRITT 11: APPENDIX-LINKS    → Relevante Appendices verknüpfen       │
│  SCHRITT 12: CHAPTER-LINKS     → Relevante Kapitel verknüpfen          │
│  SCHRITT 13: COMMIT + PUSH     → Alle Dateien auf GitHub               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Integration Levels

| Level | Name | Schritte | Dateien | Zeit |
|-------|------|----------|---------|------|
| **1** | MINIMAL | 1-5, 13 | PIP, BibTeX | 5-10 min |
| **2** | STANDARD | 1-7, 9, 11-13 | + Paper-Ref, Full Text | 15-20 min |
| **3** | CASE | 1-13 (ohne 8) | + Case Registry | 20-30 min |
| **4** | THEORY | 1-13 | + Theory Catalog | 30-45 min |
| **5** | FOUNDATIONAL | 1-13 + LaTeX Appendix | Alle + neuer Appendix | 60-90 min |

## Automatische Trigger

Claude erkennt automatisch Paper-Erwähnungen und startet den Workflow:

| Trigger | Beispiel |
|---------|----------|
| Paper-Titel genannt | "Consumer Demand and Market Competition..." |
| DOI oder NBER WP | "10.3386/w34743", "NBER WP 34743" |
| Autoren + Jahr | "Goodman et al. (2026)" |
| Paper-Abstract geteilt | "We leverage Becker's time allocation theory..." |
| Explizite Anfrage | "Neues Paper integrieren", "Paper hinzufügen" |

**DANN:**
```
Claude: "Ich erkenne ein neues Paper. Starte /integrate-paper Workflow..."
→ Schritt 1: Klassifikation zeigen
→ Schritt 2: Level bestimmen
→ Schritt 3-13: Durchführen
```

## Schritt-für-Schritt Details

### Schritt 1: KLASSIFIZIEREN (7 Kriterien)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  KRITERIUM                    GEWICHT    INDIKATOREN                    │
│  ─────────────────────────────────────────────────────────────────────  │
│  new_theory_category              5      "new framework", "unified"     │
│  extends_existing_theory          3      "extends", "builds on"         │
│  new_domain                       4      "first study", "platform"      │
│  empirical_parameters             2      "we estimate", "β ="           │
│  policy_implications              2      "policy", "regulation"         │
│  field_experiment                 2      "RCT", "field experiment"      │
│  case_study_worthy                1      "case study", "practical"      │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 2: LEVEL BESTIMMEN

```
Score ≥ 20 + (new_theory ≥ 10 OR new_domain ≥ 8)  → Level 5: FOUNDATIONAL
Score ≥ 15 + extends_theory + parameters          → Level 4: THEORY
Score ≥ 10 + (case_study OR field_experiment)     → Level 3: CASE
Score ≥ 5 + (extends_theory OR parameters)        → Level 2: STANDARD
Sonst                                              → Level 1: MINIMAL
```

### ⚠️ KRITISCHE ZUSATZPRÜFUNG: Framework vs. Estimation Paper (PFLICHT!)

**NACH der automatischen Level-Bestimmung IMMER diese Frage stellen:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LIEFERT DAS PAPER SELBST PUNKT-SCHÄTZUNGEN?                            │
│                                                                         │
│  JA, direkte Schätzungen im Paper  → Level bleibt wie berechnet        │
│  NEIN, nur Framework               → Prüfen ob Level 5 FOUNDATIONAL!   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Beispiele für FOUNDATIONAL Papers (etablieren Framework, keine Schätzungen):**
- Kahneman & Tversky (1979) - Prospect Theory
- Becker (1965) - Household Production
- Cunha & Heckman (2007) - Skill Formation Technology
- Heckman, Galaty & Tian (2023) - Virtue Ethics Framework

**Lesson Learned (2026-02-05):**
Ein Paper kann hohen Score haben (z.B. 19 = Level 4 THEORY nach Formel) und trotzdem
Level 5 FOUNDATIONAL sein, wenn es:
1. Das theoretische GERÜST etabliert (Framework Paper)
2. Aber selbst KEINE direkten Punkt-Schätzungen liefert
3. Numerische Werte im Paper sind "informed priors" aus verwandter Literatur

**Bei Framework Papers MUSS dokumentiert werden:**
```yaml
# In parameter-registry.yaml:
estimation_status: "FRAMEWORK ONLY - paper provides structure, not point estimates"
note: "⚠️ INFORMED PRIOR from [Quelle], NOT direct estimate from this paper"
prior_sources: ["author1year", "author2year"]
```

### Schritt 3: WP-PUB-CHECK (nur bei Working Papers)

```
IST DAS EIN WORKING PAPER?
├── NBER Working Paper
├── SSRN Preprint
├── arXiv
└── Unveröffentlicht

JA → Journal-Publikation suchen:
     1. Google Scholar: "exact title" + "journal"
     2. CrossRef: DOI lookup
     3. Autor-Website

     GEFUNDEN → Als Journal-Paper integrieren (mit WP als Vorstufe)
     NICHT GEFUNDEN → Als WP integrieren, Review-Datum setzen
```

### Schritt 4: PIP ERSTELLEN

```yaml
# data/paper-intake/YYYY/PIP-YYYY-MM-DD-NNN.yaml

pip_id: "PIP-2026-01-30-016"
paper_id: "PAP-nachnamejahrkurzwort"

identification:  # ★ PFLICHT
  title: "..."
  authors: [...]
  year: 2025
  journal: "..."
  doi: "..."

quality:
  evidence_tier: 2  # 1=GOLD, 2=SILVER, 3=BRONZE
  methodology: {...}

ebf_integration:  # ★ PFLICHT
  integration_level: 3
  core_dimensions: {...}
  theory_support: [...]
  use_for: [...]

decision:  # ★ PFLICHT
  status: "accept"
  rationale: "..."
```

### Schritt 5: BIBTEX ANLEGEN

```bibtex
@article{nachname2025kurzwort,
  title={...},
  author={...},
  journal={...},
  year={2025},
  doi={...},
  % EBF-FELDER (PFLICHT):
  evidence_tier = {2},
  integration_level = {3},
  pip_id = {PIP-2026-01-30-016},
  use_for = {LIT-O, DOMAIN-XX},
  theory_support = {MS-XX-XXX},
  parameter = {beta = 0.XX (SE 0.XX)},
  identification = {RCT: ...},
  external_validity = {...},
  session_ref = {EBF-S-YYYY-MM-DD-XXX-NNN},
  notes = {...}
}
```

### Schritt 6: PAPER-REFERENCE YAML

```yaml
# data/paper-references/PAP-nachname2025kurzwort.yaml

paper: nachname2025kurzwort
superkey: PAP-nachname2025kurzwort
title: "..."
evidence_tier: 2
integration_level: 3
pip_id: "PIP-2026-01-30-016"

methodology: {...}
key_findings: [...]
parameters: [...]
ebf_relevance: {...}
related_papers: [...]
```

### Schritt 7: FULL TEXT DATEI

```
# papers/evaluated/integrated/PAP-nachname2025kurzwort.txt

ABSTRACT
...

RESEARCH DESIGN
...

KEY FINDINGS
...

EBF INTEGRATION
- CORE Dimensions: ...
- Theory Support: ...
- Parameters: ...
```

### Schritt 8: THEORY CATALOG (Level 4-5)

```yaml
# data/theory-catalog.yaml - Neuer Eintrag

- id: MS-XX-NNN
  name: "Theory Name"
  category: CAT-XX
  source_paper: "PAP-nachname2025kurzwort"
  ebf_restrictions: {...}
  validity: {...}
```

### Schritt 9: PARAMETER REGISTRY

Parameter werden entweder:
- In Case Registry eingebettet (Level 3)
- In Parameter Registry separat (Level 4-5)
- In Paper Reference YAML (Level 2)

### Schritt 10: CASE REGISTRY (Level 3-5)

```yaml
# data/case-registry.yaml - Neuer Eintrag CAS-XXX

- id: CAS-XXX
  title: "..."
  domain: [...]
  ten_c_mapping: {...}
  behavioral_insight: {...}
  parameters: [...]
  source_paper: "PAP-nachname2025kurzwort"
```

### Schritt 11-12: APPENDIX & CHAPTER LINKS

Identifiziere relevante Verknüpfungen:
- CORE Appendices (AU, B, C, V, AAA, etc.)
- Domain Appendices (DOMAIN-XX)
- LIT Appendices (LIT-XX)
- Kapitel (1-25)

### Schritt 13: VALIDIERUNG (PFLICHT!)

**VOR dem Commit MUSS die Konsistenz-Validierung laufen:**

```bash
# Konsistenz-Check zwischen BibTeX und Paper-YAML
python scripts/validate_bibtex_yaml_consistency.py PAP-nachname2025kurzwort

# Bei Level 5: Vollständige 13-Komponenten Validierung
python scripts/validate_level5_integration.py PAP-nachname2025kurzwort
```

**ERGEBNIS MUSS "CONSISTENT" sein.** Wenn nicht:
- Fehlende Komponenten ergänzen ODER
- Level in BibTeX herunterstufen

### Schritt 14: COMMIT + PUSH

```bash
git add data/paper-intake/YYYY/PIP-*.yaml \
        data/paper-references/PAP-*.yaml \
        data/paper-texts/PAP-*.md \
        bibliography/bcm_master.bib \
        data/case-registry.yaml

git commit -m "feat(paper): Add [Author] ([Year]) [Kurztitel]

Integrated via PIP workflow (Level X: NAME):
- PIP-ID: PIP-YYYY-MM-DD-NNN
- Evidence Tier: X (NAME)
- Validation: CONSISTENT ✓
- Key finding: ...

https://claude.ai/code/session_xxx"

git push -u origin <branch>
```

## Validierungs-Checkliste

Nach Abschluss IMMER prüfen:

```
☐ PIP-Datei erstellt und vollständig
☐ BibTeX-Eintrag mit allen 9 EBF-Feldern
☐ Paper-Reference YAML erstellt (content_level = tatsächliches Level!)
☐ Full Text in data/paper-texts/PAP-xxx.md (SSOT!)
☐ Case Registry Eintrag (Level 3+)
☐ Theory Catalog Eintrag (Level 4+)
☐ Appendix-Links dokumentiert UND tatsächlich im Appendix referenziert
☐ Chapter-Links dokumentiert
☐ VALIDIERUNG BESTANDEN (validate_bibtex_yaml_consistency.py)
☐ Git commit mit vollständiger Message
☐ Git push erfolgreich
```

**WICHTIG:** Der Pre-Commit Hook blockiert Level 5 Commits wenn die Validierung fehlschlägt!

## Verwendung

```bash
# Interaktiv (empfohlen)
/integrate-paper

# Mit DOI
/integrate-paper --doi 10.3386/w34743

# Mit Titel
/integrate-paper --title "Paper Title"

# Nur Klassifikation
/integrate-paper --classify-only

# Via Script
python scripts/classify_paper_integration.py --interactive
```

## PFLICHT-Regeln

**JEDES neue Paper MUSS durch den 12-Schritt Workflow.**

**VERBOTEN:**
```
❌ Paper manuell in BibTeX ohne PIP-Datei
❌ BibTeX ohne die 9 EBF-Felder
❌ Case erstellen ohne Paper-Reference
❌ "Das mache ich schnell ohne Workflow"
```

**ERLAUBT / ERFORDERLICH:**
```
✅ IMMER /integrate-paper bei neuem Paper
✅ IMMER PIP-Datei erstellen (auch bei Level 1)
✅ IMMER BibTeX mit EBF-Feldern
✅ IMMER alle Schritte des Levels durchführen
✅ IMMER am Ende committen und pushen
```

## Level 5: FOUNDATIONAL Integration (6-Faktoren-Framework)

**KRITISCH:** Bei Level 5 Integrationen MUSS das **6-Faktoren-Framework** angewendet werden!

### Architektur-Prinzip

```
LIT-Appendix (Primary)     → Vollständige Formalisierung (Axiom, Beweise)
    ↓
CORE-Appendices            → NUR strukturelle Erweiterungen (nach 6-Faktoren)
    ↓
Chapters                   → NUR Cross-References
```

### 6-Faktoren-Entscheidung für CORE-Erweiterungen

Für **JEDEN** potenziell relevanten CORE diese 6 Faktoren prüfen:

| Faktor | Frage | Erweiterung wenn JA |
|--------|-------|---------------------|
| **F1** | Führt Paper NEUE Struktur ein? | Potenzielle Erweiterung |
| **F2** | Erfordert Paper NEUES Axiom? | Axiom hinzufügen |
| **F3** | Ändert Paper Dimensionalität? | Struktur erweitern |
| **F4** | Ist es Struktur (nicht nur Parameter)? | CORE ändern |
| **F5** | Gilt Erweiterung UNIVERSAL? | In CORE aufnehmen |
| **F6** | Neuer MECHANISMUS beschrieben? | Mechanismus formalisieren |

### 11-Komponenten-Checkliste (Level 5)

```
☐ 1.  BibTeX Entry (6 EBF-Felder)
☐ 2.  Theory Catalog (MS-XX-XXX)
☐ 3.  Case Registry (CAS-XXX)
☐ 4.  Parameter Registry (PAR-XXX-XXX)
☐ 5.  LIT Appendix Section (PRIMARY!)
☐ 6.  CORE Extensions (nach 6-Faktoren!)
☐ 7.  BCM2 Context Factors
☐ 8.  Chapter-Appendix Mapping
☐ 9.  Chapter Cross-References
☐ 10. Paper YAML (vollständig)
☐ 11. Paper Full-Text Archive
```

### Kapitel-Relevanz-Analyse

| Relevanz | Kriterien | Aktion |
|----------|-----------|--------|
| **HIGH** | Paper erweitert CORE des Kapitels | Cross-Ref Box + Appendix Ref |
| **MEDIUM** | Paper liefert Evidenz | Appendix Reference nur |
| **LOW** | Keine direkte Verbindung | Keine Aktion |

**Detaillierte Dokumentation:** `docs/workflows/level5-paper-integration-workflow.md`

---

## Verwandte Commands

| Command | Beschreibung |
|---------|--------------|
| `/add-paper` | Quick-Add (nur BibTeX, Level 1) |
| `/upgrade-paper` | Bestehendes Paper auf höheres Level upgraden |
| `/classify-papers` | Batch-Klassifikation |
| `/find-model` | Passende Modelle finden |
| `/case-manage add` | Case manuell hinzufügen |
