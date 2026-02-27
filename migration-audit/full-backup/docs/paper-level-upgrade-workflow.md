# Paper Level Upgrade Workflow

> Version 1.0 | Januar 2026 | Status: PFLICHT-Workflow

---

## Übersicht: Das 2D Klassifikationssystem

Papers werden in **zwei Dimensionen** klassifiziert:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  2D PAPER CLASSIFICATION SYSTEM                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DIMENSION 1: CONTENT LEVEL (Was haben wir?)                           │
│  ───────────────────────────────────────────                           │
│  Level 0 │ BIBTEX ONLY     │ Nur bibliographische Daten               │
│  Level 1 │ BASIC TEMPLATE  │ BibTeX + Abstract + Key Findings (~2k)   │
│  Level 2 │ FULL TEMPLATE   │ BibTeX + vollständiges Template (~6k)    │
│  Level 3 │ FULL TEXT       │ Kompletter Paper-Text (>50k chars)       │
│                                                                         │
│  DIMENSION 2: INTEGRATION LEVEL (Wie tief integriert?)                 │
│  ─────────────────────────────────────────────────────                 │
│  Level 1 │ MINIMAL    │ Nur BibTeX in bcm_master.bib                  │
│  Level 2 │ STANDARD   │ + theory_support, use_for, parameter Felder   │
│  Level 3 │ CASE       │ + Case Registry Eintrag (CAS-XXX)             │
│  Level 4 │ THEORY     │ + Theory Catalog (MS-XX-XXX)                  │
│  Level 5 │ FULL       │ + Appendix + Chapter References               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Content Level Anforderungen

### Level 0: BibTeX Only
- **Dateien:** `bibliography/bcm_master.bib`
- **Inhalt:** Nur bibliographische Felder (title, author, year, journal, doi)
- **Keine EBF-Felder**

### Level 1: Basic Template (~2k chars)
- **Dateien:** `papers/fulltext/PAP-xxx.txt`
- **Inhalt:**
  ```
  PAPER_ID: PAP-xxx
  TITLE: ...
  AUTHORS: ...
  YEAR: ...
  JOURNAL: ...
  ABSTRACT: [200-500 Wörter]
  KEY_FINDINGS: [3-5 Bullet Points]
  EBF_RELEVANCE: [1-2 Sätze]
  ```

### Level 2: Full Template (~6k chars)
- **Dateien:** `papers/fulltext/PAP-xxx.txt`
- **Zusätzlich zu Level 1:**
  - METHODOLOGY
  - PARAMETERS_EXTRACTED
  - LIMITATIONS
  - RELATED_PAPERS
  - CHAPTER_REFERENCES
  - APPENDIX_REFERENCES

### Level 3: Full Text (>50k chars)
- **Dateien:** `papers/fulltext/PAP-xxx.txt`
- **Inhalt:** Kompletter Paper-Text
- **Anforderung:** >50,000 Zeichen (ca. 8,000 Wörter)
- **Validierung:** `wc -c papers/fulltext/PAP-xxx.txt`

---

## Integration Level Komponenten

### Level 1: MINIMAL (5 min)
```
☐ BibTeX-Eintrag in bcm_master.bib
  ├── title, author, year, journal
  ├── doi (wenn verfügbar)
  └── evidence_tier (1-3)
```

### Level 2: STANDARD (10-15 min)
```
☐ Level 1 Komponenten
☐ EBF-Felder in BibTeX:
  ├── theory_support = {MS-XX-XXX, ...}
  ├── use_for = {LIT-XX, DOMAIN-XX, CORE-XX, ...}
  ├── parameter = {lambda = X, beta = Y, ...}
  └── notes = {Key insight...}
```

### Level 3: CASE (15-20 min)
```
☐ Level 2 Komponenten
☐ Case Registry Eintrag (data/case-registry.yaml):
  ├── id: CAS-XXX
  ├── paper_ref: PAP-xxx
  ├── 10c_mapping (alle 10 Dimensionen)
  ├── formulas (mathematische Formulierungen)
  └── insight + implication
```

### Level 4: THEORY (20-30 min)
```
☐ Level 3 Komponenten
☐ Theory Catalog Update (data/theory-catalog.yaml):
  ├── Neuer MS-XX-XXX Eintrag ODER
  ├── Bestehendes MS-XX-XXX erweitern mit bib_keys
  └── ebf_restrictions dokumentieren
☐ Parameter Registry (data/parameter-registry.yaml):
  ├── PAR-XXX-NNN für neue Parameter
  └── source: PAP-xxx
```

### Level 5: FULL (60-90 min)
```
☐ Level 4 Komponenten

☐ Appendix Reference:
  ├── Passenden LIT-Appendix identifizieren
  │   ├── LIT-LEARNING (Belief Updating, Experience Goods)
  │   ├── LIT-FEHR, LIT-THALER, etc. (nach Autor)
  │   └── LIT-O (Other) als Fallback
  ├── Paper in Annotated Bibliography einfügen
  └── use_for in BibTeX auf LIT-XX setzen

☐ Chapter Reference:
  ├── Relevantes Kapitel identifizieren (siehe Mapping unten)
  ├── Passende Section finden
  ├── Citation mit \citet{PAP-xxx} oder \citealt{PAP-xxx}
  └── Kontext-Satz mit Key Finding
```

---

## Kapitel-Thema Mapping

| Thema | Kapitel | Section | Appendix |
|-------|---------|---------|----------|
| Belief Updating, Advice | Ch. 11 | §11.3 Motivated vs Informed Beliefs | LRN (LIT-LEARNING) |
| Loss Aversion, Prospect Theory | Ch. 10 | §10.x FEPSDE | LIT-KT |
| Time Preferences | Ch. 8 | §8.x Temporal | LIT-DISCOUNTING |
| Social Preferences | Ch. 7 | §7.x Fairness | LIT-FEHR |
| Nudging, Defaults | Ch. 17 | §17.x Interventions | HHH (METHOD-TOOLKIT) |
| Framing | Ch. 9 | §9.x Context | LIT-FRAMING |

---

## Workflow: Paper von Level X zu Level Y upgraden

### Schritt 1: Status prüfen
```bash
# Content Level prüfen
wc -c papers/fulltext/PAP-xxx.txt
# >50k = Level 3, >6k = Level 2, >2k = Level 1, nicht vorhanden = Level 0

# Integration Level prüfen
grep "PAP-xxx" bibliography/bcm_master.bib    # Level 1+
grep "PAP-xxx" data/case-registry.yaml        # Level 3+
grep "PAP-xxx" data/theory-catalog.yaml       # Level 4+
grep -r "PAP-xxx" appendices/                 # Level 5
grep -r "PAP-xxx" chapters/                   # Level 5
```

### Schritt 2: Fehlende Komponenten identifizieren
```bash
# Validierungsskript (falls vorhanden)
python scripts/validate_paper_integration.py PAP-xxx
```

### Schritt 3: Content Level erhöhen

**Level 0 → 1:**
```bash
# Template erstellen
cp templates/paper-template-basic.txt papers/fulltext/PAP-xxx.txt
# Abstract via WebSearch füllen
```

**Level 1 → 2:**
```bash
# Vollständiges Template ausfüllen
# METHODOLOGY, PARAMETERS, LIMITATIONS hinzufügen
```

**Level 2 → 3:**
```bash
# WICHTIG: Zuerst prüfen ob Full Text bereits existiert!
git fetch origin main
git show origin/main:papers/fulltext/PAP-xxx.txt 2>/dev/null | wc -c

# Falls auf main vorhanden:
git checkout origin/main -- papers/fulltext/PAP-xxx.txt

# Falls nicht vorhanden: Via WebSearch/PDF suchen
```

### Schritt 4: Integration Level erhöhen

**Level 1 → 2:**
```yaml
# In bcm_master.bib hinzufügen:
theory_support = {MS-XX-XXX},
use_for = {LIT-XX, DOMAIN-XX},
parameter = {key = value},
```

**Level 2 → 3:**
```yaml
# In data/case-registry.yaml:
CAS-XXX:
  id: CAS-XXX
  paper_ref: PAP-xxx
  title: "..."
  10c_mapping:
    WHO: "..."
    WHAT: "..."
    # ... alle 10 Dimensionen
```

**Level 3 → 4:**
```yaml
# In data/theory-catalog.yaml:
# Entweder neue Theorie oder bestehende erweitern
- id: MS-XX-XXX
  bib_keys: ["PAP-xxx", ...]
```

**Level 4 → 5:**
```latex
% In appendices/LRN_LIT-LEARNING_xxx.tex (oder passendem LIT):
\item \textbf{Author (Year).} ``Title.'' \textit{Journal}.
\begin{quote}
\textit{Key finding summary.}
\end{quote}

% In chapters/XX_yyy.tex:
\citet{PAP-xxx} zeigt, dass ...
```

---

## Validierung & Commit

### Validierungs-Checkliste
```
☐ Content Level verifiziert: wc -c papers/fulltext/PAP-xxx.txt
☐ BibTeX syntaktisch korrekt: bibtex-Kompilierung ohne Fehler
☐ use_for Feld auf korrekten LIT-Appendix gesetzt
☐ Alle Cross-References bidirektional (Appendix ↔ Paper)
☐ Chapter Reference mit korrekter Citation-Syntax
```

### Commit-Template
```bash
git commit -m "$(cat <<'EOF'
feat(PAP-xxx): Upgrade to Content Level X, Integration Level Y

Content Level X:
- [Beschreibung der Content-Änderungen]

Integration Level Y:
- [Liste aller Komponenten]

https://claude.ai/code/session_XXX
EOF
)"
```

---

## Learning Loop Integration

### Bei JEDEM Paper-Upgrade:

1. **VOR dem Upgrade:** Learnings-DB prüfen
   ```bash
   grep -i "paper\|upgrade\|level" data/paper-integration-learnings.yaml
   ```

2. **BEI Fehlern:** Learning dokumentieren
   ```yaml
   # In data/paper-integration-learnings.yaml hinzufügen:
   - id: "INT-L-YYYY-MM-DD-CAT-NNN"
     date: "YYYY-MM-DD"
     category: "LEVEL"  # oder BIBTEX, LIT, THEORY, etc.
     severity: "HIGH"   # oder CRITICAL, MEDIUM, LOW
     title: "Kurzbeschreibung"
     problem: "Was ist passiert?"
     solution: "Was war die Lösung?"
     prevention: "Wie verhindern wir das in Zukunft?"
   ```

3. **NACH dem Upgrade:** Checkliste validieren
   - Alle Komponenten vorhanden?
   - Cross-References korrekt?
   - Commit-Message vollständig?

---

## Bekannte Fehlerquellen (aus Learnings)

### L1: Full Text auf main vergessen
**Problem:** Full Text existiert bereits auf origin/main, wird aber nicht gefunden
**Lösung:** IMMER zuerst `git fetch origin main && git show origin/main:papers/fulltext/PAP-xxx.txt` prüfen

### L2: Content Level 3 Schwelle
**Problem:** "Full Text" bedeutet >50k chars, nicht einfach "mehr als Template"
**Lösung:** `wc -c` zur Validierung verwenden, Schwelle: 50,000 Zeichen

### L3: Appendix vs Chapter Reference verwechselt
**Problem:** Level 5 erfordert BEIDE (Appendix UND Chapter)
**Lösung:** Checkliste abhaken, nicht nur einen von beiden

### L4: Citation Syntax
**Problem:** `\cite{PAP-xxx}` statt `\citet{PAP-xxx}` in Fließtext
**Lösung:** `\citet{}` für "Author (Year) shows...", `\citep{}` für "(Author, Year)"

### L5: use_for Feld nicht aktualisiert
**Problem:** Paper in Appendix referenziert, aber `use_for` zeigt noch auf LIT-O
**Lösung:** use_for IMMER auf den tatsächlichen LIT-Appendix aktualisieren

---

## Quick Reference

```
CONTENT LEVELS:
  0 = BibTeX only
  1 = Basic template (~2k chars)
  2 = Full template (~6k chars)
  3 = Full text (>50k chars)  ← Schwelle: 50,000 Zeichen!

INTEGRATION LEVELS:
  1 = BibTeX
  2 = + EBF fields (theory_support, use_for, parameter)
  3 = + Case Registry
  4 = + Theory Catalog + Parameter Registry
  5 = + Appendix Reference + Chapter Reference

VALIDATION:
  wc -c papers/fulltext/PAP-xxx.txt  # Content Level
  grep PAP-xxx data/case-registry.yaml  # Integration Level 3+

COMMIT:
  feat(PAP-xxx): Upgrade to Content Level X, Integration Level Y
```

---

## Referenzen

- **Learnings-DB:** `data/paper-integration-learnings.yaml`
- **Case Registry:** `data/case-registry.yaml`
- **Theory Catalog:** `data/theory-catalog.yaml`
- **Parameter Registry:** `data/parameter-registry.yaml`
- **Paper Queue:** `data/paper-integration-queue.yaml`
- **BibTeX Master:** `bibliography/bcm_master.bib`

---

*Version 1.0 | Erstellt aus Session 2026-01-31 (PAP-bregolin2026advice Upgrade)*
