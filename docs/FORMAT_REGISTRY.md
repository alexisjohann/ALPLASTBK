# EBF Format Registry

> Vollständige Spezifikation aller Dokumenten-Formate mit GitHub-Strukturen

---

## 📋 Übersicht: 16 Formate in 4 Kategorien

| Kategorie | Formate | Seiten | Ordner |
|-----------|---------|--------|--------|
| **KURZ** | 1-Pager, Exec Summary, Memo, Abstract | 1-5 | `outputs/short/` |
| **MITTEL** | Proposal, Report, Working Paper, Case Study | 5-30 | `outputs/medium/` |
| **LANG** | White Paper, Technical Report, Journal Article | 30-100 | `outputs/long/` |
| **SEHR LANG** | Monograph, Handbook, Textbook, Treatise | 100+ | Root + chapters/ |

---

## 📁 GitHub-Struktur für Outputs

```
complementarity-context-framework/
│
├── outputs/                              # ALLE PRODUZIERTEN DOKUMENTE
│   │
│   ├── README.md                         # Outputs-Übersicht
│   │
│   ├── short/                            # KURZ (1-5 Seiten)
│   │   ├── README.md
│   │   ├── one-pagers/                   # 1-Pager
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   ├── summaries/                    # Executive Summaries
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   ├── memos/                        # Memos
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   └── abstracts/                    # Abstracts
│   │       ├── README.md
│   │       └── [Dokumente]
│   │
│   ├── medium/                           # MITTEL (5-30 Seiten)
│   │   ├── README.md
│   │   ├── proposals/                    # Proposals
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   ├── reports/                      # Reports
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   ├── working-papers/               # Working Papers
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   └── case-studies/                 # Case Studies
│   │       ├── README.md
│   │       ├── 00_template.tex
│   │       └── [Dokumente]
│   │
│   ├── long/                             # LANG (30-100 Seiten)
│   │   ├── README.md
│   │   ├── white-papers/                 # White Papers
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   ├── technical-reports/            # Technical Reports
│   │   │   ├── README.md
│   │   │   ├── 00_template.tex
│   │   │   └── [Dokumente]
│   │   └── papers/                       # Journal Articles
│   │       ├── README.md
│   │       ├── 00_template.tex
│   │       └── [submissions/]
│   │
│   ├── policy/                           # POLICY DOKUMENTE
│   │   ├── README.md
│   │   ├── 00_template.docx
│   │   └── [Dokumente]
│   │
│   └── presentations/                    # PRÄSENTATIONEN
│       ├── README.md
│       ├── 00_template.pptx
│       └── [Präsentationen]
│
├── chapters/                             # SEHR LANG (Hauptdokument)
├── appendices/                           # SEHR LANG (Appendices)
└── ...
```

---

# 📄 FORMAT-SPEZIFIKATIONEN

---

## 1️⃣ ONE-PAGER

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 1 (max. 2) |
| **Aufwand** | 2-4 Stunden |
| **Qualität** | Q2-Q3 |
| **Ziel** | Entscheidung / Briefing |
| **Leser** | Entscheider, Führungskräfte |

### Ordner-Struktur

```
outputs/short/one-pagers/
├── README.md                    # Format-Beschreibung
├── 00_template.tex              # LaTeX-Template
├── 00_template.md               # Markdown-Template
├── 00_checklist.md              # Qualitäts-Checkliste
│
└── [YYYY-MM-DD]_[topic]/        # Pro Dokument ein Ordner
    ├── one-pager.tex            # Quelldatei
    ├── one-pager.pdf            # Kompiliert
    └── metadata.yaml            # Metadaten
```

### Template-Struktur

```
┌─────────────────────────────────────┐
│ TITEL                               │
│ Datum | Autor | Version             │
├─────────────────────────────────────┤
│ KONTEXT (2-3 Sätze)                 │
│ Was ist die Situation?              │
├─────────────────────────────────────┤
│ KERNAUSSAGE (1-2 Sätze)             │
│ Was ist die Hauptbotschaft?         │
├─────────────────────────────────────┤
│ ARGUMENTE (3-5 Bullets)             │
│ • Punkt 1                           │
│ • Punkt 2                           │
│ • Punkt 3                           │
├─────────────────────────────────────┤
│ EMPFEHLUNG / NEXT STEPS             │
│ Was soll passieren?                 │
└─────────────────────────────────────┘
```

### Namenskonvention

```
[YYYY-MM-DD]_[topic]_one-pager.tex
Beispiel: 2026-01-06_bcm-intro_one-pager.tex
```

---

## 2️⃣ EXECUTIVE SUMMARY

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 1-2 |
| **Aufwand** | 4-8 Stunden |
| **Qualität** | Q3 |
| **Ziel** | Zusammenfassung eines längeren Dokuments |
| **Leser** | Führungskräfte, Stakeholder |

### Ordner-Struktur

```
outputs/short/summaries/
├── README.md
├── 00_template.tex
│
└── [source-doc]_summary/         # Verlinkt zum Quelldokument
    ├── summary.tex
    ├── summary.pdf
    └── metadata.yaml             # Enthält Link zum Quelldokument
```

### Besonderheit

- **MUSS** auf Quelldokument verweisen
- Versionierung parallel zum Quelldokument

### Namenskonvention

```
[source-doc]_v[N]_summary.tex
Beispiel: complementarity_context_v51_summary.tex
```

---

## 3️⃣ MEMO

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 1-3 |
| **Aufwand** | 2-4 Stunden |
| **Qualität** | Q2-Q3 |
| **Ziel** | Interne Kommunikation |
| **Leser** | Team, Stakeholder |

### Ordner-Struktur

```
outputs/short/memos/
├── README.md
├── 00_template.tex
│
└── [YYYY-MM-DD]_[topic]/
    ├── memo.tex
    ├── memo.pdf
    └── metadata.yaml
        ├── to: [Empfänger]
        ├── from: [Absender]
        ├── date: [Datum]
        ├── subject: [Betreff]
        └── status: [draft/final]
```

### Template-Struktur

```
TO:      [Empfänger]
FROM:    [Absender]
DATE:    [Datum]
RE:      [Betreff]
─────────────────────────────────────
[Inhalt]
```

---

## 4️⃣ REPORT

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 10-30 |
| **Aufwand** | 1-2 Wochen |
| **Qualität** | Q3-Q4 |
| **Ziel** | Analyse, Evaluation |
| **Leser** | Fachleute, Entscheider |

### Ordner-Struktur

```
outputs/medium/reports/
├── README.md
├── 00_template.tex
│
└── [YYYY-MM]_[project]_report/    # Pro Report ein Ordner
    ├── report.tex                 # Hauptdatei
    ├── report.pdf
    ├── sections/                  # Bei großen Reports
    │   ├── 01_intro.tex
    │   ├── 02_analysis.tex
    │   └── ...
    ├── data/                      # Daten für den Report
    │   ├── raw/
    │   └── processed/
    ├── figures/                   # Abbildungen
    └── metadata.yaml
```

### Pflicht-Elemente

- Executive Summary
- Inhaltsverzeichnis
- Einleitung
- Methodik
- Ergebnisse
- Schlussfolgerungen
- Appendix (optional)

---

## 5️⃣ WORKING PAPER

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 15-30 |
| **Aufwand** | 2-4 Wochen |
| **Qualität** | Q2-Q3 |
| **Ziel** | Forschung in Progress |
| **Leser** | Forscher, Team |

### Ordner-Struktur

```
outputs/medium/working-papers/
├── README.md
├── 00_template.tex
│
└── WP-[NNN]_[short-title]/        # Nummerierte Working Papers
    ├── WP-001_title_v1.tex        # Versionierte Quelldatei
    ├── WP-001_title_v1.pdf
    ├── WP-001_title_v2.tex        # Neue Version
    ├── WP-001_title_v2.pdf
    ├── figures/
    ├── code/                      # Analyse-Code
    └── metadata.yaml
        ├── number: WP-001
        ├── title: [Titel]
        ├── authors: [...]
        ├── status: [draft/review/final]
        ├── versions:
        │   ├── v1: 2026-01-01
        │   └── v2: 2026-01-15
        └── abstract: [...]
```

### Besonderheit

- **Nummerierung:** WP-001, WP-002, ...
- **Versionierung:** v1, v2, v3, ...
- **Status-Tracking:** draft → review → final

---

## 6️⃣ CASE STUDY

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 10-20 |
| **Aufwand** | 1-2 Wochen |
| **Qualität** | Q3 |
| **Ziel** | Anwendungsbeispiel |
| **Leser** | Praktiker, Studenten |

### Ordner-Struktur

```
outputs/medium/case-studies/
├── README.md
├── 00_template.tex
│
└── CS-[NNN]_[subject]/            # Nummerierte Case Studies
    ├── case-study.tex
    ├── case-study.pdf
    ├── data/                      # Fall-Daten
    ├── analysis/                  # Analyse-Code
    ├── figures/
    └── metadata.yaml
        ├── number: CS-001
        ├── subject: [Fallname]
        ├── domain: [Anwendungsgebiet]
        ├── bcm_components: [WHO/WHAT/HOW/WHEN]
        └── key_findings: [...]
```

### Template-Struktur

```
1. EINLEITUNG
   - Kontext
   - Fragestellung

2. DER FALL
   - Beschreibung
   - Relevante Daten

3. EBF ANALYSE
   - Angewandte Komponenten
   - Modellierung

4. ERGEBNISSE
   - Erkenntnisse
   - Vergleich mit Standard-Ansatz

5. IMPLIKATIONEN
   - Für Theorie
   - Für Praxis
```

---

## 7️⃣ WHITE PAPER

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 20-50 |
| **Aufwand** | 2-4 Wochen |
| **Qualität** | Q3-Q4 |
| **Ziel** | Thought Leadership |
| **Leser** | Fachleute, Entscheider |

### Ordner-Struktur

```
outputs/long/white-papers/
├── README.md
├── 00_template.tex
│
└── [YYYY]_[topic]_whitepaper/
    ├── whitepaper.tex
    ├── whitepaper.pdf
    ├── sections/
    ├── figures/
    ├── review/                    # Review-Tracking
    │   ├── reviewer_comments.md
    │   └── response.md
    └── metadata.yaml
```

---

## 8️⃣ JOURNAL ARTICLE (Paper)

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 20-40 |
| **Aufwand** | 2-6 Monate |
| **Qualität** | Q4 |
| **Ziel** | Peer-reviewed Publication |
| **Leser** | Akademiker |

### Ordner-Struktur

```
outputs/long/papers/
├── README.md
├── 00_template.tex
│
└── [short-title]/
    ├── paper.tex                  # Hauptdatei
    ├── paper.pdf
    ├── paper_supplementary.tex    # Supplementary Material
    ├── figures/
    ├── tables/
    ├── code/                      # Replikations-Code
    ├── data/                      # Daten (oder Link)
    │
    ├── submissions/               # Submission-Tracking
    │   ├── [journal1]/
    │   │   ├── submission_v1.pdf
    │   │   ├── cover_letter.tex
    │   │   ├── response_r1.tex    # Response to Reviewers
    │   │   └── decision.md
    │   └── [journal2]/
    │
    └── metadata.yaml
        ├── title: [...]
        ├── authors: [...]
        ├── abstract: [...]
        ├── keywords: [...]
        ├── jel_codes: [...]
        └── submissions:
            ├── journal1:
            │   ├── submitted: 2026-01-01
            │   ├── decision: reject
            │   └── date: 2026-03-01
            └── journal2:
                └── submitted: 2026-03-15
```

### Besonderheit

- **Submission-Tracking** pro Journal
- **Response to Reviewers** dokumentiert
- **Replikations-Material** vollständig

---

## 9️⃣ POLICY MEMO

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Seiten** | 2-5 |
| **Aufwand** | 4-8 Stunden |
| **Qualität** | Q3 |
| **Ziel** | Policy-Empfehlung |
| **Leser** | Policy Maker |

### Ordner-Struktur

```
outputs/policy/
├── README.md
├── 00_template.docx               # Word für Policy Maker
├── 00_template.md
│
└── [YYYY-MM-DD]_[topic]/
    ├── policy-memo.docx           # Word-Version
    ├── policy-memo.pdf
    ├── policy-memo.md             # Markdown-Backup
    ├── stakeholders.md            # Stakeholder-Analyse
    └── metadata.yaml
        ├── topic: [...]
        ├── target_audience: [...]
        ├── key_recommendations: [...]
        └── stakeholders: [...]
```

---

## 🔟 PRESENTATION

### Spezifikation

| Dimension | Wert |
|-----------|------|
| **Folien** | 10-30 |
| **Aufwand** | 4-16 Stunden |
| **Qualität** | Q3 |
| **Ziel** | Präsentation |
| **Leser** | Verschiedene Audiences |

### Ordner-Struktur

```
outputs/presentations/
├── README.md
├── 00_template.pptx
├── 00_template_beamer.tex         # LaTeX Beamer
│
└── [YYYY-MM-DD]_[event]_[topic]/
    ├── slides.pptx                # PowerPoint
    ├── slides.pdf                 # PDF-Export
    ├── speaker_notes.md           # Notizen
    ├── figures/                   # Verwendete Grafiken
    │
    └── versions/                  # Audience-spezifisch
        ├── academic/              # Für Konferenz
        ├── executive/             # Für Management
        └── public/                # Für Öffentlichkeit
```

---

# 📊 Format-Entscheidungsmatrix

## Schnellwahl nach Situation

| Situation | Format | Ordner |
|-----------|--------|--------|
| "Kurze Entscheidungsvorlage" | 1-Pager | `short/one-pagers/` |
| "Zusammenfassung für Chef" | Exec Summary | `short/summaries/` |
| "Interne Info verteilen" | Memo | `short/memos/` |
| "Projektantrag" | Proposal | `medium/proposals/` |
| "Analyse-Ergebnisse" | Report | `medium/reports/` |
| "Forschung dokumentieren" | Working Paper | `medium/working-papers/` |
| "Praxisbeispiel zeigen" | Case Study | `medium/case-studies/` |
| "Thought Leadership" | White Paper | `long/white-papers/` |
| "Akademisch publizieren" | Journal Article | `long/papers/` |
| "Policy-Empfehlung" | Policy Memo | `policy/` |
| "Vortrag halten" | Presentation | `presentations/` |

---

# ✅ Checkliste: Neues Dokument erstellen

1. [ ] **Format bestimmen** (via Master Framework, Schritt 2)
2. [ ] **Ordner anlegen** nach Konvention
3. [ ] **Template kopieren** aus `00_template.*`
4. [ ] **metadata.yaml erstellen** mit allen Pflichtfeldern
5. [ ] **README.md aktualisieren** im Format-Ordner
6. [ ] **Commit** mit korrekter Nachricht
7. [ ] **Status tracken** (bei Working Papers, Papers)

---

*Letzte Aktualisierung: Januar 2026*
