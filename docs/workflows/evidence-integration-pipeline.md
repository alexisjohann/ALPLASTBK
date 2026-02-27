# Evidence Integration Pipeline (EIP)

> Version 1.0 | Januar 2026 | Status: PFLICHT-Workflow

---

## Übersicht

Die **Evidence Integration Pipeline (EIP)** ist der standardisierte Workflow für die Integration neuer Konzepte ins EBF Framework. Sie stellt sicher, dass:

1. Alle Konzepte wissenschaftlich fundiert sind
2. Pro- und Contra-Evidenz systematisch erfasst wird
3. Papers korrekt in alle relevanten Stellen integriert werden
4. Die Literatur-Datenbank konsistent bleibt

---

## Der 5-Stufen-Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│  EVIDENCE INTEGRATION PIPELINE (EIP)                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  STUFE 1: KONZEPT ENTWICKELT                                        │
│     ↓                                                               │
│  STUFE 2: LITERATURRECHERCHE (PRO/CONTRA)                           │
│     ↓                                                               │
│  STUFE 3: ENTSCHEIDUNG (Integrieren / Verwerfen)                    │
│     ↓                                                               │
│  STUFE 4: FRAMEWORK-INTEGRATION (Appendix + Kapitel)                │
│     ↓                                                               │
│  STUFE 5: PAPER-INTEGRATION (BibTeX + LIT + Zitate)                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Trigger-Kriterien: Wann wird EIP aktiviert?

**KRITISCH:** Claude muss automatisch erkennen, wann ein neues Konzept entwickelt wurde!

### Automatische Trigger (mindestens 1 erfüllt)

| # | Trigger | Beispiel | Aktion |
|---|---------|----------|--------|
| TR1 | **Neue Terminologie** eingeführt | "Mental Identity Budgeting" | EIP starten |
| TR2 | **Neuer Mechanismus** beschrieben | "$I_{\text{WHAT},F} → I_{\text{WHO}}$ Transformation" | EIP starten |
| TR3 | **Neue γ-Werte** behauptet | "γ($I_{\text{AWARE}}$,$I_{\text{WHEN}}$) = +0.4" | Evidenz prüfen |
| TR4 | **Neue Formel/Gleichung** entwickelt | "Z(n) = Z_max × (1-0.03×...)" | EIP starten |
| TR5 | **Neue Intervention** vorgeschlagen | "Benefits Choice Box" | EIP starten |

### Claude-Anweisung bei Trigger-Erkennung

```
WENN mindestens ein Trigger erkannt:
│
├── SOFORT pausieren
├── Konzept dokumentieren (Stufe 1)
├── Interne Quellen prüfen (bcm_master.bib, LIT)
├── Bei Bedarf externe Quellen
└── Entscheidung: Integrieren / Verwerfen / Modifizieren

NIEMALS: Konzept ohne Evidenz-Prüfung integrieren!
```

### Beispiel-Erkennung

```yaml
# Trigger TR1 + TR2 erkannt:
user_input: "Wir könnten ein 'Mental Identity Budgeting' System einführen,
            das Überstunden in Purpose-Budgets transformiert."

erkannte_trigger:
  - TR1: "Mental Identity Budgeting" (neue Terminologie)
  - TR2: "transformiert" (neuer Mechanismus impliziert)

claude_aktion: |
  "Ich erkenne ein neues Konzept. Bevor ich es integriere,
   starte ich die Evidence Integration Pipeline..."
```

---

## Stufe 1: Konzept entwickelt

**Trigger:** Ein neues Konzept, Mechanismus oder Feature wird vorgeschlagen.

**Dokumentation erforderlich:**

| Feld | Beschreibung | Beispiel |
|------|--------------|----------|
| `concept_id` | Eindeutige ID | `CONC-2026-001` |
| `name` | Kurzer Name | "Mental Identity Budgeting" |
| `description` | Was macht es? | "$I_{\text{WHAT},F}$ → $I_{\text{WHO}}$ Transformation" |
| `proposed_location` | Wo soll es hin? | "Appendix TKT, Chapter 17" |
| `proposer` | Wer hat es vorgeschlagen? | "Session 2026-01-19" |

**Output:** Konzept-Proposal dokumentiert

---

## Stufe 2: Literaturrecherche (PRO/CONTRA)

**PFLICHT:** Für jedes neue Konzept müssen Papers recherchiert werden.

### 2.1 PRO-Evidenz suchen

> Welche wissenschaftlichen Papers **unterstützen** dieses Konzept?

**Suchstrategie (INTERNE QUELLEN ZUERST!):**

```
SCHRITT 1: INTERNE QUELLEN (PFLICHT)
├── a) bcm_master.bib durchsuchen (1,922+ Papers)
│   → Keywords, Autoren, ebf_tags
├── b) LIT-Appendices prüfen
│   → LIT-R (Researcher), LIT-D (Domain), LIT-M (Meta)
└── c) Case Registry prüfen
    → Ähnliche Cases mit Evidenz-Links

SCHRITT 2: EXTERNE QUELLEN (nur wenn intern nicht ausreichend)
├── d) Google Scholar: Schlüsselbegriffe
├── e) SSRN, NBER, arXiv
└── f) Referenzen in gefundenen Papers verfolgen
```

**Warum intern zuerst?**
- bcm_master.bib enthält kuratierte, EBF-relevante Literatur
- LIT-Appendices haben bereits Integration-Analysen
- Vermeidet Duplikate und inkonsistente Zitationen

**Dokumentation:**

```yaml
pro_evidence:
  - paper: "thaler1999"
    finding: "Mental Accounting erklärt Budgetierung"
    relevance: "Direkte theoretische Grundlage"
    strength: "high"  # high/medium/low

  - paper: "grant2008"
    finding: "Prosocial Motivation erhöht Engagement"
    relevance: "Unterstützt Community Budget"
    strength: "medium"
```

### 2.2 CONTRA-Evidenz suchen

> Welche wissenschaftlichen Papers **widersprechen** diesem Konzept?

**KRITISCH:** Contra-Evidenz aktiv suchen, nicht ignorieren!

**Suchstrategie (INTERNE QUELLEN ZUERST!):**

```
SCHRITT 1: INTERNE QUELLEN (PFLICHT)
├── a) LIT-M-CRITIQUE prüfen (Meta: Kritik-Papers)
├── b) bcm_master.bib: "critique", "replication", "failed"
└── c) Case Registry: Failed Interventions

SCHRITT 2: EXTERNE QUELLEN
├── d) Google Scholar: "critique of [Konzept]"
├── e) Replikationsstudien suchen
└── f) Meta-Analysen mit Null-Effekten
```

**NIEMALS:** Nur PRO-Evidenz suchen und CONTRA überspringen!

**Dokumentation:**

```yaml
contra_evidence:
  - paper: "binmore2008"
    finding: "BE-Effekte oft nicht robust"
    threat_level: "medium"  # high/medium/low
    mitigation: "Fokus auf gut-replizierte Effekte"

  - paper: null
    note: "Keine direkte Contra-Evidenz gefunden"
```

### 2.3 Evidenz-Bilanz erstellen

```yaml
evidence_summary:
  pro_papers: 5
  contra_papers: 1
  pro_strength_avg: "high"
  contra_threat_level: "low"
  confidence: "high"  # high/medium/low
  recommendation: "integrate"  # integrate/reject/modify
```

---

## Stufe 3: Entscheidung

### 3.1 Entscheidungsmatrix

| PRO-Evidenz | CONTRA-Evidenz | Entscheidung |
|-------------|----------------|--------------|
| Stark (≥3 high) | Keine/Schwach | ✅ INTEGRIEREN |
| Stark | Mittel | ⚠️ INTEGRIEREN mit Caveats |
| Mittel | Keine | ✅ INTEGRIEREN (vorsichtig) |
| Mittel | Mittel | 🔄 MODIFIZIEREN |
| Schwach | Stark | ❌ VERWERFEN |
| Keine | - | ❌ VERWERFEN (keine Evidenz) |

### 3.2 Bei VERWERFEN

**Dokumentation in `quality/rejected_concepts.md`:**

```yaml
rejected_concept:
  id: "CONC-2026-002"
  name: "Gamification Points"
  reason: "Starke Contra-Evidenz zu Crowding-Out"
  contra_papers:
    - "deci1999"
    - "gneezy2000"
  lesson_learned: "Extrinsische Rewards mit Vorsicht"
  date: "2026-01-19"
```

### 3.3 Bei INTEGRIEREN

Weiter zu Stufe 4.

---

## Stufe 4: Framework-Integration

### 4.1 Appendix-Integration

**Entscheidungsbaum: Welcher Appendix?**

```
Neues Konzept integrieren?
│
├─► Ist es eine METHODIK?
│   └─► METHOD-Appendix (z.B. HHH, CMP, LLMMC)
│
├─► Ist es eine DOMÄNEN-ANWENDUNG?
│   └─► DOMAIN-Appendix (z.B. LABOR, FINANCE)
│
├─► Erweitert es einen CORE?
│   └─► CORE-Appendix (z.B. AAA, B, C)
│
└─► Ist es eine VORHERSAGE?
    └─► PREDICT-Appendix
```

**Dokumentation:**

```yaml
appendix_integration:
  primary_appendix: "HHH"
  section: "Example 3: Type Transformation"
  line_range: [450, 520]
  cross_refs:
    - "CMP:sec:worked-example-benefits"
    - "Chapter 17:sec:mental-budgeting"
```

### 4.2 Kapitel-Integration

**Entscheidungsbaum: Welches Kapitel?**

| Konzept-Typ | Kapitel | Section |
|-------------|---------|---------|
| Intervention Design | Ch. 17 | Worked Example |
| Phase-Affinity | Ch. 18 | Matrix-Erweiterung |
| Segment-Targeting | Ch. 19 | Segment-Section |
| Portfolio-Design | Ch. 20 | Worked Example |
| Komplementarität | Ch. 5 (CORE) | Theory Section |

**Dokumentation:**

```yaml
chapter_integration:
  primary_chapter: 17
  section: "Beispiel 4: Mental Identity Budgeting"
  secondary_chapters:
    - chapter: 19
      section: "Choice Architecture"
    - chapter: 20
      section: "HR Retention Portfolio"
```

---

## Stufe 5: Paper-Integration

### 5.1 BibTeX-Eintrag (bcm_master.bib)

**PFLICHT:** Jedes zitierte Paper muss in `bibliography/bcm_master.bib` sein.

```bibtex
@article{grant2008,
  author = {Grant, Adam M.},
  title = {The Significance of Task Significance},
  journal = {Journal of Applied Psychology},
  year = {2008},
  volume = {93},
  number = {1},
  pages = {108--124},
  doi = {10.1037/0021-9010.93.1.108},
  keywords = {prosocial, motivation, meaning, identity},
  ebf_tags = {WHO, identity, prosocial}
}
```

**EBF-spezifische Felder:**
- `ebf_tags`: 10C Dimensionen (AWARE, WHO, WHAT, HOW, WHEN, etc.), Konzepte
- `ebf_integration`: Wo integriert? (Appendix-Codes)

### 5.2 LIT-Appendix-Integration

**Entscheidungsbaum:** (siehe `appendix-category-definitions.md`)

```
Paper in LIT integrieren?
│
├─► SCHRITT 0: Methodisches/Historisches/Kritisches Paper?
│   └─► JA → LIT-M (META, HISTORY, CRITIQUE, etc.)
│
├─► SCHRITT 1: Existiert LIT-R für diesen Autor?
│   └─► JA → In diesem LIT-R integrieren
│
├─► SCHRITT 2: Direkte Erweiterung eines LIT-R Autors?
│   └─► JA → Im LIT-R des Primärautors
│
├─► SCHRITT 3: Threshold für eigenen LIT-R erreicht?
│   └─► JA → Neuen LIT-R-[AUTOR] erstellen
│
└─► SCHRITT 4: In LIT-O (Other) mit Cluster
```

**Dokumentation:**

```yaml
lit_integration:
  paper: "grant2008"
  target_lit: "OT"  # LIT-OTHER
  cluster: "Prosocial Motivation"
  section_in_lit: "subsec:prosocial-cluster"
  full_integration: true  # false = nur Referenz
```

### 5.3 Appendix-Section-Zitat

**PFLICHT:** Paper muss im relevanten Appendix als Evidenz zitiert werden.

```latex
% In HHH_METHOD-TOOLKIT.tex
\subsection{Evidence Base}

Mental Identity Budgeting is supported by research on:
\begin{itemize}
    \item Prosocial motivation and task significance \citep{grant2008}
    \item Mental accounting and budgeting behavior \citep{thaler1999}
    \item Intrinsic vs. extrinsic motivation \citep{deci1999}
\end{itemize}
```

---

## Checkliste: EIP Vollständigkeit

```
☐ STUFE 1: Konzept dokumentiert
  ☐ concept_id vergeben
  ☐ proposed_location definiert

☐ STUFE 2: Literaturrecherche
  ☐ PRO-Evidenz gesucht (≥3 Papers)
  ☐ CONTRA-Evidenz aktiv gesucht
  ☐ Evidenz-Bilanz erstellt
  ☐ Confidence-Level bestimmt

☐ STUFE 3: Entscheidung
  ☐ Entscheidungsmatrix angewendet
  ☐ Bei VERWERFEN: rejected_concepts.md aktualisiert
  ☐ Bei INTEGRIEREN: Weiter zu Stufe 4

☐ STUFE 4: Framework-Integration
  ☐ Primärer Appendix identifiziert
  ☐ Section in Appendix definiert
  ☐ Kapitel-Integration geplant
  ☐ Cross-References dokumentiert

☐ STUFE 5: Paper-Integration
  ☐ Alle Papers in bcm_master.bib
  ☐ Papers in korrektem LIT-Appendix
  ☐ Papers als Evidenz in Appendix zitiert
  ☐ ebf_tags in BibTeX eingetragen
```

---

## Beispiel: Mental Identity Budgeting

### Stufe 1: Konzept

```yaml
concept_id: "CONC-2026-MIB"
name: "Mental Identity Budgeting"
description: "$I_{\\text{WHAT},F}$ (Financial) → $I_{\\text{WHO}}$ (Identity) Transformation"
proposed_location: "HHH Example 3, Chapter 17 Example 4"
```

### Stufe 2: Literatur

```yaml
pro_evidence:
  - paper: "thaler1985"
    finding: "Mental Accounting existiert"
    strength: "high"
  - paper: "thaler1999"
    finding: "Budgets beeinflussen Verhalten"
    strength: "high"
  - paper: "akerlof2000"
    finding: "Identity beeinflusst Entscheidungen"
    strength: "high"
  - paper: "grant2008"
    finding: "Prosocial Motivation wirkt"
    strength: "medium"

contra_evidence:
  - paper: null
    note: "Keine direkte Contra-Evidenz"

evidence_summary:
  confidence: "high"
  recommendation: "integrate"
```

### Stufe 3: Entscheidung

**✅ INTEGRIEREN** - Starke PRO-Evidenz, keine CONTRA-Evidenz

### Stufe 4: Framework-Integration

```yaml
appendix_integration:
  primary: "HHH"
  section: "Example 3: Type Transformation"

chapter_integration:
  primary: 17
  section: "Beispiel 4: Mental Identity Budgeting"
```

### Stufe 5: Paper-Integration

| Paper | bcm_master.bib | LIT-Appendix | Appendix-Zitat |
|-------|----------------|--------------|----------------|
| thaler1985 | ✅ bereits | THL (LIT-R-THALER) | HHH ✅ |
| thaler1999 | ✅ bereits | THL | HHH ✅ |
| akerlof2000 | ✅ bereits | AK (LIT-R-AKERLOF) | HHH ✅ |
| grant2008 | ✅ hinzugefügt | OT (Prosocial) | HHH ✅ |

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────────────┐
│  EIP QUICK REFERENCE                                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  TRIGGER: Neue Terminologie / Mechanismus / γ-Wert / Formel?        │
│           → EIP SOFORT starten!                                     │
│                                                                     │
│  Bei JEDEM neuen Konzept:                                           │
│                                                                     │
│  1. INTERNE QUELLEN ZUERST:                                         │
│     a) bcm_master.bib (1,922+ Papers)                               │
│     b) LIT-Appendices (R/D/M/O)                                     │
│     c) Case Registry                                                │
│                                                                     │
│  2. EXTERNE QUELLEN nur wenn nötig:                                 │
│     d) Google Scholar, SSRN, NBER                                   │
│                                                                     │
│  3. PRO + CONTRA Papers suchen (≥3 PRO)                             │
│  4. Entscheidung: Integrate / Reject / Modify                       │
│  5. Papers integrieren:                                             │
│     a) bcm_master.bib                                               │
│     b) LIT-Appendix (R/D/M/O)                                       │
│     c) Zitat in relevantem Appendix                                 │
│                                                                     │
│  NIEMALS: Konzept ohne Evidenz integrieren!                         │
│  NIEMALS: Contra-Evidenz ignorieren!                                │
│  NIEMALS: Papers ohne LIT-Integration zitieren!                     │
│  NIEMALS: Externe Quellen VOR internen Quellen!                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Changelog

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.1 | 2026-01-19 | Trigger-Kriterien hinzugefügt, Suchpriorität: Intern vor Extern |
| 1.0 | 2026-01-19 | Initial specification |

---

*Dieser Workflow ist PFLICHT für alle neuen Konzepte im EBF Framework.*
