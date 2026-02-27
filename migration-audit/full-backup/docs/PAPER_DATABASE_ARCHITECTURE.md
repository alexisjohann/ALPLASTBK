# Paper Database Architecture: Die 3 Quellen

> **⚠️ DEPRECATED (2026-02-08)** — Dieses Dokument beschreibt die alte 3-Quellen-Architektur.
> Die aktuelle SSOT-Architektur ist:
> - **Metadata:** `data/paper-references/PAP-{key}.yaml` (2,322 Dateien)
> - **Bibliography:** `bibliography/bcm_master.bib` (2,322 Einträge)
> - **Workflow:** `/integrate-paper`
> - **Aktuelle Doku:** `docs/workflows/paper-workflow-overview.md`

**Erstellt**: 17. Januar 2026
**Status**: ~~Dokumentation der gewachsenen Struktur~~ DEPRECATED — siehe Header
**Zweck**: Klarheit schaffen über die 3 Paper-Quellen und deren Beziehung

---

## Executive Summary

Das EBF hat **DREI PAPER-QUELLEN**, die historisch gewachsen sind:

| Quelle | Format | Anzahl | Zweck |
|--------|--------|--------|-------|
| **LIT-Appendices** | LaTeX (textuell) | ~2,700 | Menschenlesbare Literatur-Reviews |
| **paper-sources.yaml** | YAML (strukturiert) | 1,438 | Master-Datenbank für Skills & Analysen |
| **bcm_master.bib** | BibTeX | 1,862 | LaTeX-Kompilierung (`\cite{}`) |

---

## 1. Warum 3 Quellen? Historische Entwicklung

### Phase 1: Akademisches Schreiben (Ursprung)

```
SITUATION: Ein Forscher schreibt einen Literatur-Appendix über Ernst Fehr.

AKTION:
  → Listet 80 Papers als \item \textbf{Fehr (1999)} Title...
  → Copy-Paste aus Google Scholar, schnell erstellt
  → Menschenlesbar, gut für PDF-Output

RESULTAT: LIT-FEHR Appendix mit 80 Papers

PROBLEM:
  → Keine Struktur (kein Year, Journal, DOI als separate Felder)
  → Nicht maschinenlesbar
  → Keine Verknüpfung zu anderen Systemen
```

### Phase 2: LaTeX-Kompilierung (Bedarf entsteht)

```
SITUATION: Jemand will ein Paper kompilieren mit \cite{PAP-fehr1999theory}.

AKTION:
  → Erstellt manuell BibTeX-Eintrag in bcm_master.bib
  → Nur für die Papers, die gerade gebraucht werden

RESULTAT: bcm_master.bib mit ~200 Einträgen (Subset)

PROBLEM:
  → Nur Teilmenge erfasst
  → Keine systematische Synchronisierung
  → Duplikate möglich
```

### Phase 3: EBF Framework & Skills (Heute)

```
SITUATION: Skills wie /case, /design-model brauchen strukturierte Daten.

FRAGEN:
  → Welche Papers haben Effect Sizes für Loss Aversion?
  → Welche Papers betreffen Domain "Health" + Stage "Action"?
  → Welche Cases sind mit welchen Papers verlinkt?

AKTION:
  → paper-sources.yaml als strukturierte Master-Datenbank
  → Mit 10C-Koordinaten, Effect Sizes, Linked Cases

RESULTAT: paper-sources.yaml mit 1,438 Papers

PROBLEM:
  → Parallel zu den anderen beiden gewachsen
  → Keine klare Hierarchie definiert
  → Synchronisierung unklar
```

---

## 2. Die 3 Quellen im Detail

### 2.1 LIT-Appendices (Input/Archiv)

**Speicherort**: `appendices/*LIT-*.tex`, `appendices/*_papers.tex`
**Format**: LaTeX mit textuellen Paper-Listen
**Anzahl**: ~2,700 Paper-Referenzen
**Anzahl Dateien**: ~50 LIT-Appendices

**Beispiel** (aus `appendices/FEH_fehr_papers.tex`):
```latex
\begin{enumerate}
  \item \textbf{Fehr, E., \& Schmidt, K. M. (1999).}
        A Theory of Fairness, Competition, and Cooperation.
        \textit{Quarterly Journal of Economics}, 114(3), 817-868.

  \item \textbf{Fehr, E., \& Gächter, S. (2000).}
        Cooperation and Punishment in Public Goods Experiments.
        \textit{American Economic Review}, 90(4), 980-994.
  ...
\end{enumerate}
```

**Eigenschaften**:
- Menschenlesbar, gut für PDF-Output
- Keine strukturierten Felder (Jahr, Journal, DOI nicht separat)
- Nicht maschinenlesbar
- Keine Verknüpfung zu Cases oder 10C-Koordinaten

**Rolle im System**:
- **Input**: Rohdaten aus Literatur-Reviews
- **Archiv**: Vollständige Dokumentation pro Autor/Thema
- **Referenz**: Für menschliche Leser der Appendices

---

### 2.2 paper-sources.yaml (Master Database)

**Speicherort**: `data/paper-sources.yaml`
**Format**: YAML (strukturiert, maschinenlesbar)
**Anzahl**: 1,438 Papers
**Dateigröße**: ~62,000 Zeilen

**Beispiel**:
```yaml
- id: PAP-fehr1999theory
  authors:
    - Fehr, Ernst
    - Schmidt, Klaus M.
  year: 1999
  title: 'A Theory of Fairness, Competition, and Cooperation'
  journal: Quarterly Journal of Economics
  volume: 114
  issue: 3
  doi: 10.1162/003355399556151
  citations: 12500
  status: seminal
  type: journal_article

  key_findings:
    - finding: 'Inequity aversion explains rejections in ultimatum games'
      domain: cooperation
      stage: action
      primary_dimension: S
      effect_size: 0.6

  9c_coordinates:
    - domain: cooperation
      stages: [contemplation, action]
      primary_dimension: S
      psi_dominant: social_context
      gamma: 0.7
      A_level: 0.8
      W_level: 0.6

  linked_cases:
    - CASE-042
    - CASE-089
    - CASE-156

  evidence_tier: 1
  lit_appendix: K
```

**Eigenschaften**:
- Vollständig strukturiert
- 10C-Koordinaten für jedes Paper
- Effect Sizes und Key Findings
- Verknüpfung zu Cases
- Evidence Tiers (1-3)
- Maschinenlesbar für Skills

**Rolle im System**:
- **Master Database**: Single Source of Truth für Paper-Metadaten
- **Skill-Backend**: Datenquelle für `/case`, `/design-model`, etc.
- **Analyse-Grundlage**: Für Bayesian Priors, LLMMC, etc.

---

### 2.3 bcm_master.bib (LaTeX Export)

**Speicherort**: `bibliography/bcm_master.bib`
**Format**: BibTeX
**Anzahl**: 1,862 Einträge
**Dateigröße**: ~16,000 Zeilen

**Beispiel**:
```bibtex
@article{fehr1999theory,
  title={A Theory of Fairness, Competition, and Cooperation},
  author={Fehr, Ernst and Schmidt, Klaus M.},
  journal={Quarterly Journal of Economics},
  volume={114},
  number={3},
  pages={817--868},
  year={1999},
  doi={10.1162/003355399556151},
}
```

**Eigenschaften**:
- Standard-BibTeX-Format
- Kompatibel mit LaTeX `\cite{}`
- Keine 10C-Koordinaten oder Effect Sizes
- Automatisch generierbar aus YAML

**Rolle im System**:
- **Export**: Generiert aus paper-sources.yaml
- **LaTeX-Integration**: Ermöglicht `\cite{PAP-fehr1999theory}`
- **PDF-Kompilierung**: Für akademische Outputs

---

## 3. Beziehung zwischen den Quellen

### Hierarchie (SOLL-Zustand)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LIT-APPENDICES (~2,700)                          │
│                    [INPUT / ARCHIV]                                 │
│                                                                     │
│  Menschenlesbare Paper-Listen in LaTeX                              │
│  → Vollständige Dokumentation pro Autor/Thema                       │
│  → Quelle für neue Papers                                           │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ Extraktion & Anreicherung
                            │ (manuell oder per Script)
                            │ + 10C-Koordinaten
                            │ + Effect Sizes
                            │ + Case Links
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 PAPER-SOURCES.YAML (1,438)                          │
│                 [MASTER DATABASE / SSOT]                            │
│                                                                     │
│  Strukturierte Metadaten für Skills & Analysen                      │
│  → Einzige Quelle der Wahrheit für Paper-Daten                      │
│  → Backend für /case, /design-model, Bayesian Priors                │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ Automatischer Export
                            │ (sync_yaml_to_bibtex.py)
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  BCM_MASTER.BIB (1,862)                             │
│                  [LATEX EXPORT]                                     │
│                                                                     │
│  BibTeX für LaTeX-Kompilierung                                      │
│  → Ermöglicht \cite{} in Kapiteln und Appendices                    │
│  → Automatisch synchronisiert mit YAML                              │
└─────────────────────────────────────────────────────────────────────┘
```

### Datenfluss

```
[Neues Paper entdeckt]
        │
        ▼
┌──────────────────┐
│  LIT-Appendix    │  Forscher fügt Paper zu Literatur-Review hinzu
│  (textuell)      │  → \item \textbf{Autor (Jahr)} Title...
└────────┬─────────┘
         │
         │ Extraktion (manuell/Script)
         ▼
┌──────────────────┐
│ paper-sources    │  Paper wird strukturiert erfasst
│ .yaml            │  → ID, Autoren, Jahr, Journal, DOI
│                  │  → 10C-Koordinaten hinzugefügt
│                  │  → Effect Sizes dokumentiert
│                  │  → Cases verlinkt
└────────┬─────────┘
         │
         │ sync_yaml_to_bibtex.py (automatisch)
         ▼
┌──────────────────┐
│ bcm_master.bib   │  BibTeX-Eintrag generiert
│                  │  → \cite{id} funktioniert in LaTeX
└──────────────────┘
```

---

## 4. Aktueller Stand (Januar 2026)

### Zahlen

| Quelle | Anzahl | Vollständigkeit |
|--------|--------|-----------------|
| LIT-Appendices | ~2,700 | 100% (Archiv) |
| paper-sources.yaml | 1,438 | 53% der LIT-Papers |
| bcm_master.bib | 1,862 | 100% der YAML (+ Legacy) |

### Lücken

```
LIT-Appendices:        ~2,700 Papers
paper-sources.yaml:    -1,438 Papers
─────────────────────────────────────
NICHT in YAML:         ~1,262 Papers (noch zu extrahieren)
```

### Synchronisierungsstatus

| Sync-Richtung | Status | Tool |
|---------------|--------|------|
| YAML → BibTeX | ✅ 100% synchron | `sync_yaml_to_bibtex.py` |
| LIT → YAML | ⚠️ 53% erfasst | Noch kein automatisches Tool |

---

## 5. Warum diese Struktur?

### Problem: Organisches Wachstum

```
TYPISCHES SZENARIO (vor Dokumentation):

1. Forscher A schreibt LIT-MALMENDIER Appendix
   → 192 Papers als Textliste

2. Forscher B braucht \cite{PAP-malmendier2005ceo} für ein Kapitel
   → Fügt 5 Einträge zu bcm_master.bib hinzu

3. Entwickler C baut /case Skill
   → Braucht strukturierte Daten
   → Erfasst 30 Malmendier-Papers in paper-sources.yaml

RESULTAT:
- LIT-Appendix: 192 Papers
- BibTeX: 5 Papers
- YAML: 30 Papers
→ 3 verschiedene Teilmengen, keine synchronisiert!
```

### Konsequenzen ohne Ordnung

| Problem | Konsequenz |
|---------|------------|
| **Inkonsistenz** | Paper in LIT-Appendix existiert, aber `\cite{}` funktioniert nicht |
| **Redundanz** | Gleiche Information 3x pflegen, 3x Fehlerquellen |
| **Unvollständigkeit** | Skills sehen nur 1,438 Papers, nicht die 2,700 in LIT-Appendices |
| **Keine SSOT** | Bei Widersprüchen: Welche Quelle ist "richtig"? |
| **Wartungsaufwand** | Änderungen müssen manuell an 3 Stellen gemacht werden |

### Lösung: Klare Hierarchie + Automatisierung

1. **LIT-Appendices = Input/Archiv**
   - Hier werden neue Papers erstmals dokumentiert
   - Vollständige Literatur-Reviews pro Autor/Thema
   - Nicht die "Wahrheit", sondern die "Rohdaten"

2. **paper-sources.yaml = Single Source of Truth**
   - Einzige autoritative Quelle für Paper-Metadaten
   - Strukturiert für maschinelle Verarbeitung
   - Angereichert mit 10C, Effect Sizes, Cases

3. **bcm_master.bib = Automatischer Export**
   - Generiert aus YAML, nicht manuell gepflegt
   - Immer synchron mit YAML
   - Nur für LaTeX-Kompilierung relevant

---

## 6. Workflows

### 6.1 Neues Paper hinzufügen

```
SCHRITT 1: Paper in LIT-Appendix dokumentieren (optional)
           → Wenn Teil eines Literatur-Reviews

SCHRITT 2: Paper in paper-sources.yaml eintragen (PFLICHT)
           → Strukturierte Metadaten
           → 10C-Koordinaten
           → Effect Sizes (falls bekannt)

SCHRITT 3: sync_yaml_to_bibtex.py ausführen
           → BibTeX-Eintrag wird automatisch generiert

SCHRITT 4: \cite{paper_id} funktioniert in LaTeX
```

### 6.2 Bestehendes Paper aktualisieren

```
SCHRITT 1: paper-sources.yaml aktualisieren (SSOT)
           → Nur hier ändern!

SCHRITT 2: sync_yaml_to_bibtex.py ausführen
           → BibTeX wird automatisch aktualisiert

HINWEIS: LIT-Appendix muss NICHT aktualisiert werden
         (ist nur Archiv/Input, nicht SSOT)
```

### 6.3 Bulk-Import aus LIT-Appendix

```
SCHRITT 1: LIT-Appendix identifizieren mit fehlenden Papers

SCHRITT 2: Script extract_papers_from_lit.py ausführen (geplant)
           → Extrahiert Paper-Daten aus LaTeX
           → Generiert YAML-Einträge (ohne 10C)

SCHRITT 3: 10C-Koordinaten manuell/semi-automatisch hinzufügen

SCHRITT 4: sync_yaml_to_bibtex.py ausführen
```

---

## 7. Scripts & Tools

| Script | Zweck | Status |
|--------|-------|--------|
| `sync_yaml_to_bibtex.py` | YAML → BibTeX synchronisieren | ✅ Implementiert |
| `extract_papers_from_lit.py` | LIT-Appendix → YAML extrahieren | 🔲 Geplant |
| `validate_paper_sources.py` | YAML-Konsistenz prüfen | 🔲 Geplant |
| `find_missing_papers.py` | Lücken zwischen Quellen finden | 🔲 Geplant |

---

## 8. Nächste Schritte

### Priorität 1: Dokumentation (diese Datei)
- ✅ Struktur dokumentiert
- ✅ Hierarchie definiert
- ✅ Workflows beschrieben

### Priorität 2: Vollständige Synchronisierung
- [ ] ~1,262 fehlende Papers aus LIT-Appendices → YAML extrahieren
- [ ] 10C-Koordinaten für neue Papers hinzufügen
- [ ] BibTeX automatisch synchronisieren

### Priorität 3: Automatisierung
- [ ] `extract_papers_from_lit.py` implementieren
- [ ] CI/CD Pipeline für automatische Synchronisierung
- [ ] Validierungs-Checks bei Commits

---

## 9. Governance

### Rollen

| Rolle | Verantwortung |
|-------|---------------|
| **Paper Curator** | paper-sources.yaml pflegen, 10C-Koordinaten zuweisen |
| **LIT-Author** | LIT-Appendices schreiben (Input) |
| **Build System** | BibTeX automatisch synchronisieren |

### Regeln

1. **YAML ist SSOT**: Bei Widersprüchen gilt paper-sources.yaml
2. **BibTeX nie manuell editieren**: Immer über YAML + Sync-Script
3. **LIT-Appendices sind Input**: Nicht die "Wahrheit", sondern Rohdaten
4. **Neue Papers immer in YAML**: Auch wenn kein LIT-Appendix existiert

---

**Dokumentations-Version**: 1.0
**Letzte Aktualisierung**: 17. Januar 2026
**Nächste Review**: Bei Implementierung der Sync-Scripts
