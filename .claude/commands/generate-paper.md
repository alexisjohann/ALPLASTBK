# /generate-paper - Wissenschaftliches Paper schreiben

Generiere ein wissenschaftliches Paper — entweder aus einer bestehenden Quelle (REFORMAT) oder als originales Paper aus EBF-Modellen und -Daten (COMPOSE).

## Zwei Modi

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MODE A: REFORMAT                     │  MODE B: COMPOSE                │
├───────────────────────────────────────┼─────────────────────────────────┤
│  Input: Appendix oder Chapter .tex     │  Input: Model-ID oder Session   │
│  Methode: Parse → 8D Style → Reformat  │  Methode: Registry-Pull →       │
│  Output: Reformatiertes Paper          │           Section-by-Section    │
│  Zeit: ~10 min                         │  Zeit: ~60-120 min              │
│                                       │                                 │
│  Für: Bestehenden Content umschreiben  │  Für: NEUES Paper schreiben     │
│  Beispiel: Appendix → Journal-Paper    │  Beispiel: PSF-2.0 → WP        │
└───────────────────────────────────────┴─────────────────────────────────┘
```

## Verwendung

```bash
# MODE A: REFORMAT (bestehend)
/generate-paper appendices/AU_bcm_axiom_formalization.tex --style ernst_fehr
/generate-paper chapters/03_limits_utility.tex --style nature

# MODE B: COMPOSE (neu)
/generate-paper --compose MOD-PSF-2.0 --style ernst_fehr
/generate-paper --compose EBF-S-2026-02-14-POL-001 --style nber_working_paper
/generate-paper --compose MOD-PSF-2.0 --style policy_brief --sections intro,model,results
```

## Verfuegbare Styles (8D-Profile)

### Akademisch

| Style | Zielgruppe | D1 | D7 | Charakteristik |
|-------|------------|----|----|----------------|
| `ernst_fehr` | AER/JPE/QJE | 0.9 | 0.1 | Formal, testbare Hypothesen, experimentelles Design |
| `kahneman_tversky` | Broad Academic | 0.8 | 0.2 | Zugaenglich, Heuristiken-first, breite Zielgruppe |
| `nber_working_paper` | NBER/WP | 0.85 | 0.1 | Technical, ausfuehrlich, Working Paper Format |
| `nature` | Science/Nature | 0.85 | 0.2 | Cross-disciplinary, high impact, knapp |
| `ebf_appendix` | EBF Framework | 0.85 | 0.15 | Framework-intern, Axiome, Cross-Refs |

### Policy & Business

| Style | Zielgruppe | D1 | D7 | Charakteristik |
|-------|------------|----|----|----------------|
| `policy_brief` | Policy Makers | 0.6 | 0.25 | Action-oriented, Executive Summary |
| `mckinsey_quarterly` | C-Level | 0.5 | 0.3 | Business-Insight, Handlungsempfehlung |

### Journalistisch

| Style | Zielgruppe | D1 | D7 | Charakteristik |
|-------|------------|----|----|----------------|
| `der_spiegel` | Bildungsbuerger | 0.4 | 0.5 | Narrativ, Szene-Einstieg |
| `economist` | Informed Public | 0.6 | 0.3 | Analytisch, knapp, witzig |
| `ted_talk` | General Public | 0.4 | 0.7 | Inspirierend, storytelling |

---

## MODE B: COMPOSE — Vollstaendiger Workflow

### PHASE 0: Registry Pull (automatisch)

Claude fuehrt diese Schritte AUTOMATISCH aus:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 0: DATEN SAMMELN                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Input: Model-ID (z.B. MOD-PSF-2.0)                                    │
│         ODER Session-ID (z.B. EBF-S-2026-02-14-POL-001)                │
│                                                                         │
│  Claude liest:                                                          │
│  1. data/model-registry.yaml                                            │
│     → Modell-Definition, Variablen, Functional Form                    │
│     → Kalibrierung, Validation Metrics                                 │
│     → Appendix-Referenzen, Theorie-Basis                               │
│                                                                         │
│  2. data/model-building-session.yaml                                    │
│     → Session-Kontext, Fragestellung, Domain                           │
│     → Deliverables, Learnings                                          │
│                                                                         │
│  3. data/parameter-registry.yaml                                        │
│     → Alle Parameter mit PAR-IDs                                       │
│     → Literatur-Quellen, Kalibrierungswerte                            │
│     → Confidence Intervals                                             │
│                                                                         │
│  4. data/output-registry.yaml                                           │
│     → Deliverables, Code-Pfade                                         │
│     → Key Findings                                                     │
│                                                                         │
│  5. bibliography/bcm_master.bib                                         │
│     → Alle Papers mit theory_support zum Modell                        │
│     → use_for Referenzen                                               │
│                                                                         │
│  6. Modell-Verzeichnis (z.B. models/PSF-2-0-PAPAL-SUCCESSION/)         │
│     → README.md, model-definition.yaml                                 │
│     → Code, Tests, Kalibrierungsdaten                                  │
│                                                                         │
│  7. Appendix-Dateien (aus appendix_refs)                                │
│     → Axiome, Worked Examples, Formeln                                 │
│                                                                         │
│  OUTPUT: Strukturiertes Data-Bundle fuer Paper-Komposition              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### PHASE 1: Paper-Architektur planen

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: PAPER-ARCHITEKTUR                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1a. GENRE bestimmen (aus Style):                                       │
│      ernst_fehr        → research_article                               │
│      nber_working_paper → working_paper                                 │
│      nature            → letter                                         │
│      policy_brief      → policy_brief                                   │
│                                                                         │
│  1b. SWSM MOVE-SEQUENZ planen:                                         │
│                                                                         │
│  research_article:                                                      │
│    ★ M1: Establish_Territory  (Warum ist das Thema wichtig?)            │
│    ★ M2: Establish_Niche      (Welche Luecke gibt es?)                  │
│    ★ M3: Occupy_Niche         (Was machen WIR?)                         │
│    ★ M4: Model_Specification  (Formales Modell)                         │
│    ★ M5: Data_Methods         (Daten und Methodik)                      │
│    ★ M6: Results              (Ergebnisse praesentieren)                │
│    ★ M7: Discussion           (Interpretation, Limitationen)            │
│    ◆ M8: Conclusion           (Zusammenfassung, Ausblick)              │
│                                                                         │
│  working_paper:                                                         │
│    Wie research_article, aber:                                          │
│    + ★ M4b: Derivations       (Ausfuehrliche Herleitungen)             │
│    + ★ M6b: Robustness_Checks (Sensitivitaetsanalyse)                  │
│    + ◆ M9: Technical_Appendix (Code, Daten, Proofs)                    │
│                                                                         │
│  letter:                                                                │
│    ★ M1+M2+M3 komprimiert in 1 Paragraph                               │
│    ★ M4+M5 komprimiert in 1 Sektion                                    │
│    ★ M6+M7 komprimiert in 1 Sektion                                    │
│    Keine separate Conclusion (letzter Paragraph von Discussion)         │
│                                                                         │
│  policy_brief:                                                          │
│    ★ Executive_Summary (vor allem anderen!)                             │
│    ★ Problem_Statement                                                  │
│    ★ Evidence                                                           │
│    ★ Recommendations                                                    │
│    ◆ Implementation                                                     │
│                                                                         │
│  1c. SECTION-PLAN User zeigen:                                          │
│      → Titel pro Section                                                │
│      → Geschaetzter Umfang (Woerter)                                    │
│      → Key Content Points                                               │
│      → User-Feedback einholen                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### PHASE 2: 8D-Profil anwenden

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: 8D-PROFIL → STYLE + VOCABULARY                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Axiom DT-5/DT-6: Struktur emergiert aus 8D                            │
│  ├── D1 > 0.7 → Technical Glossary erforderlich                        │
│  ├── D4 < 0.3 → Executive Summary erforderlich                         │
│  ├── D4 > 0.6 → Detaillierte Subsections erlaubt                       │
│  └── D8 > 0.8 → References + Version Control                           │
│                                                                         │
│  Axiom DT-7/DT-8: Style emergiert aus 8D                               │
│  ├── D1 > 0.7 → Fachvokabular, Formeln erlaubt                        │
│  ├── D1 < 0.3 → Einfache Sprache, Analogien                           │
│  ├── D7 < 0.3 → Unpersoenlicher Stil, kein Narrativ                    │
│  └── D8 > 0.8 → Hedging ("suggests", "may")                            │
│                                                                         │
│  Axiom DT-9: Vocabulary emergiert aus Style                             │
│  ├── Hedging=True → "suggests", "indicates", "appears"                 │
│  ├── Register=Formal → "therefore", "consequently"                     │
│  └── Pronouns=False → "the study", "the analysis"                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### PHASE 3: Section-by-Section Komposition

Dies ist der KERN des COMPOSE-Modus. Claude schreibt jede Section einzeln.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: CONTENT GENERATION (Section-by-Section)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Fuer JEDE Section:                                                     │
│  1. SWSM-Move identifizieren (M1-M8)                                   │
│  2. Registry-Daten fuer diese Section laden                             │
│  3. Content generieren                                                  │
│  4. BibTeX-Referenzen einfuegen (\cite{key})                           │
│  5. Formeln aus model-registry uebernehmen                             │
│  6. User-Review anbieten                                               │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 0: ABSTRACT                                                    │
│  ──────────────────────────────────────────────────────────────────── │
│  Quelle: Key Findings aus output-registry + session                    │
│  Struktur: Problem → Methode → Ergebnis → Implikation                  │
│  Laenge: 150-300 Woerter (Style-abhaengig)                              │
│  REGEL: Abstract wird ZULETZT geschrieben, aber ZUERST gezeigt!        │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 1: INTRODUCTION (M1 + M2 + M3)                                │
│  ──────────────────────────────────────────────────────────────────── │
│  M1 Establish Territory:                                                │
│    → Warum ist das Thema wichtig?                                       │
│    → Breiter Kontext, gesellschaftliche Relevanz                       │
│    → 2-3 Referenzen zu etablierten Arbeiten                            │
│                                                                         │
│  M2 Establish Niche:                                                    │
│    → "However, existing approaches..."                                  │
│    → Gap identifizieren (was fehlt in der Literatur?)                  │
│    → Contra-Referenzen oder Limitationen bestehender Arbeit            │
│                                                                         │
│  M3 Occupy Niche:                                                       │
│    → "In this paper, we..."                                             │
│    → Beitrag klar benennen (Contribution Statement)                    │
│    → Vorschau auf Ergebnisse (Preview of Results)                      │
│    → Paper-Struktur skizzieren                                         │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 2: LITERATURE REVIEW / RELATED WORK                           │
│  ──────────────────────────────────────────────────────────────────── │
│  Quelle: bcm_master.bib (theory_support + use_for des Modells)         │
│  Struktur:                                                              │
│    → Thematische Cluster (nicht chronologisch!)                        │
│    → Pro Cluster: 3-5 Schluesselpaper                                   │
│    → Positionierung: Wie baut UNSER Ansatz darauf auf?                  │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 3: MODEL (M4)                                                  │
│  ──────────────────────────────────────────────────────────────────── │
│  Quelle: model-registry.yaml → functional_form                        │
│  Struktur:                                                              │
│    → Setup & Notation                                                   │
│    → Axiome/Annahmen (aus Appendix)                                    │
│    → Modell-Spezifikation (Formeln aus Registry)                       │
│    → Interpretation der Parameter                                      │
│    → Verbindung zu bestehender Theorie                                 │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 4: DATA & METHODOLOGY (M5)                                    │
│  ──────────────────────────────────────────────────────────────────── │
│  Quelle: parameter-registry.yaml + calibration data                    │
│  Struktur:                                                              │
│    → Datenbeschreibung (Quelle, Umfang, Zeitraum)                      │
│    → Variablen-Definition (mit PAR-IDs)                                │
│    → Schaetzmethode (Kalibrierung, MLE, ABM, etc.)                     │
│    → Robustheits-Strategie                                             │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 5: RESULTS (M6)                                               │
│  ──────────────────────────────────────────────────────────────────── │
│  Quelle: calibration metrics aus model-registry                        │
│  Struktur:                                                              │
│    → Hauptergebnis (zuerst, prominent)                                 │
│    → Detailergebnisse (Tabellen, Figures)                              │
│    → Sensitivitaetsanalyse                                              │
│    → Robustness Checks                                                 │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 6: DISCUSSION (M7)                                            │
│  ──────────────────────────────────────────────────────────────────── │
│  Struktur:                                                              │
│    → Zusammenfassung der Hauptergebnisse                               │
│    → Interpretation im Kontext der Literatur                           │
│    → Implikationen (theoretisch + praktisch)                           │
│    → Limitationen (ehrlich, spezifisch)                                │
│    → Zukunftsforschung                                                 │
│                                                                         │
│  ──────────────────────────────────────────────────────────────────── │
│  SECTION 7: CONCLUSION (M8)                                            │
│  ──────────────────────────────────────────────────────────────────── │
│  Struktur:                                                              │
│    → 1 Paragraph: Was haben wir getan?                                 │
│    → 1 Paragraph: Was haben wir gefunden?                              │
│    → 1 Paragraph: Warum ist das wichtig?                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### PHASE 4: Qualitaetspruefung

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: QUALITAET                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CHECK                                STATUS    SCHWELLWERT             │
│  ─────────────────────────────────────────────────────────────────────  │
│  SWSM Move Coverage                  ≥ 90%     Alle ★ Moves vorhanden  │
│  Referenz-Vollstaendigkeit            ≥ 80%     Papers aus Registry     │
│  Parameter-Dokumentation              100%      Alle PAR-IDs zitiert    │
│  Formel-Konsistenz                    100%      Registry = Paper        │
│  Abstract ≤ 300 Woerter               ✓/✗      Style-abhaengig         │
│  Contribution Statement vorhanden     ✓/✗      In Introduction         │
│  Limitations Section vorhanden        ✓/✗      In Discussion           │
│                                                                         │
│  Bei ✗: Claude benennt Problem und bietet Fix an                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### PHASE 5: Output generieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: OUTPUT                                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  FORMAT (Regel O-1 aus 8D):                                             │
│  ├── D8 > 0.6 → LaTeX (.tex)                                           │
│  ├── 0.3 < D8 ≤ 0.6 → Markdown (.md)                                   │
│  └── D8 ≤ 0.3 → Plain Text                                             │
│                                                                         │
│  AUTO-COMPILE (Regel O-2):                                              │
│  └── LaTeX + D8 > 0.5 → PDF automatisch via /compile                   │
│                                                                         │
│  SPEICHERORT:                                                           │
│  └── outputs/papers/WP_{YEAR}_{NNN}_{MODEL}_{STYLE}.{ext}              │
│                                                                         │
│  REGISTRY:                                                              │
│  └── Neuen Eintrag in output-registry.yaml (OUT-XXX)                   │
│                                                                         │
│  GIT:                                                                   │
│  └── Commit + Push mit Message:                                         │
│      "feat(paper): Generate WP-{NNN} from {MODEL} ({STYLE})"           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## MODE A: REFORMAT — Bestehender Workflow

Fuer Appendix/Chapter → Paper Reformatierung:

```bash
/generate-paper <quelle.tex> [--style <stil>]
```

Verwendet `scripts/generate_paper.py` mit 32 Style-Profilen.
Parst LaTeX, wendet 8D-Profil an, generiert reformatiertes Paper.

---

## User-Interaktion (COMPOSE Modus)

Claude fuehrt den Workflow INTERAKTIV durch:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  INTERAKTIONS-PROTOKOLL                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: User waehlt Modus                                          │
│    Claude: "Welchen Modus?"                                             │
│    → REFORMAT (bestehenden Content umschreiben)                        │
│    → COMPOSE (neues Paper aus EBF-Modell)                              │
│                                                                         │
│  SCHRITT 2 (COMPOSE): Model-ID eingeben                                │
│    Claude: "Welches Modell?"                                            │
│    → Model-ID (z.B. MOD-PSF-2.0)                                       │
│    → Session-ID (z.B. EBF-S-2026-02-14-POL-001)                        │
│    → "aktuell" (nutzt session-context.yaml)                            │
│                                                                         │
│  SCHRITT 3: Style waehlen                                               │
│    Claude zeigt passende Styles mit [DEFAULT]                          │
│    → ernst_fehr / nber_working_paper / nature / etc.                   │
│                                                                         │
│  SCHRITT 4: Section-Plan reviewen                                       │
│    Claude zeigt: Sections + Inhaltspunkte + Woerter                     │
│    User: "ok" / "Section 3 ausfuehrlicher" / "skip Literature Review"  │
│                                                                         │
│  SCHRITT 5: Section-by-Section schreiben                                │
│    Claude schreibt Section 1 → zeigt → User Feedback                   │
│    Claude schreibt Section 2 → zeigt → User Feedback                   │
│    ...                                                                  │
│    ODER User sagt "schnell" → Claude schreibt alles auf einmal         │
│                                                                         │
│  SCHRITT 6: Qualitaet + Output                                         │
│    Claude prueft, kompiliert, registriert                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Mapping: Registry-Daten → Paper-Sections

| Paper Section | Primaer-Quelle | Sekundaer-Quellen |
|---------------|----------------|-------------------|
| Abstract | output-registry (key_findings) | session (question) |
| Introduction | session (question, domain) | bcm_master.bib |
| Literature Review | bcm_master.bib (theory_support) | theory-catalog.yaml |
| Model | model-registry (functional_form) | appendix .tex |
| Data & Methods | parameter-registry (values) | model directory |
| Results | model-registry (calibration) | output-registry |
| Discussion | session (learnings) | bcm_master.bib |
| Conclusion | output-registry (key_findings) | session |
| References | bcm_master.bib | parameter sources |

## Beispiel: PSF-2.0 Paper generieren

```bash
/generate-paper --compose MOD-PSF-2.0 --style nber_working_paper
```

```
Phase 0: Registry Pull...
  ✅ model-registry.yaml → MOD-PSF-2.0 (5 Variablen, 3 Komponenten)
  ✅ session → EBF-S-2026-02-14-POL-001
  ✅ parameter-registry → PAR-VTM-001 bis PAR-VTM-008
  ✅ output-registry → OUT-029
  ✅ bibliography → 14 Methodologie-Papers + 4 existierende
  ✅ appendix → BP (METHOD-VOTING, 8 VTM Axiome)

Phase 1: Paper-Architektur...
  Genre: working_paper
  Sections:
    1. Introduction (~800 Woerter)
    2. Institutional Background: The Papal Conclave (~600)
    3. Model (~1200)
       3.1 Mechanism-Dimension Mapping
       3.2 Logistic Model with Complementarity
       3.3 Agent-Based Conclave Simulation
    4. Data & Calibration (~800)
    5. Results (~1000)
       5.1 Historical Accuracy
       5.2 Duration Prediction
       5.3 Sensitivity Analysis
    6. Discussion (~600)
    7. Conclusion (~400)
    A. Technical Appendix

Phase 2: 8D-Profil: nber_working_paper
  D1=0.85, D2=0.8, D3=0.7, D4=0.8, D5=G1, D6=1.0, D7=0.1, D8=0.9

Phase 3: Content Generation (Section-by-Section)...
  [Claude schreibt jede Section interaktiv]

Phase 4: Qualitaet...
  Move Coverage: 100% ✓
  Referenzen: 18/18 ✓
  Parameter: 8/8 ✓

Phase 5: Output...
  → outputs/papers/WP_2026_001_PSF-2.0_nber.tex
  → outputs/papers/WP_2026_001_PSF-2.0_nber.pdf
  → output-registry: OUT-030
```

## Helper Script

```bash
# Registry-Daten fuer ein Modell extrahieren (JSON fuer Paper-Komposition)
python scripts/paper_compose_helper.py --model MOD-PSF-2.0
python scripts/paper_compose_helper.py --session EBF-S-2026-02-14-POL-001
python scripts/paper_compose_helper.py --model MOD-PSF-2.0 --section results
```

## Anti-Patterns (VERBOTEN)

```
❌ Paper schreiben OHNE Registry-Daten zu laden
❌ Formeln erfinden statt aus model-registry zu uebernehmen
❌ Parameter-Werte ohne PAR-ID zitieren
❌ Literatur erfinden statt aus bcm_master.bib zu ziehen
❌ Abstract zuerst schreiben (wird ZULETZT geschrieben!)
❌ Alle Sections auf einmal ohne User-Feedback (ausser "schnell" Modus)
❌ Paper generieren ohne in output-registry zu registrieren
```

## Verwandte Skills

- `/compile` - LaTeX kompilieren
- `/check-compliance` - Template-Compliance pruefen
- `/find-model` - Modell in Registry finden
- `/design-model` - Neues Modell designen (VOR paper-writing)
- `/integrate-paper` - Externes Paper integrieren (NACH paper-writing: eigenes Paper als Referenz)

## SWSM Qualitaetsmetriken

| Metrik | Schwellwert | Pruefung |
|--------|-------------|---------|
| Move Coverage | ≥ 90% | Alle ★ Moves vorhanden? |
| Kohaesion | ≥ 0.7 | Referenzketten, lexikalische Dichte |
| RST-Tiefe | 3-5 | Nicht zu flach, nicht zu tief |
| Parameter-Coverage | 100% | Alle PAR-IDs aus Registry zitiert |
| Reference-Coverage | ≥ 80% | Papers aus Registry im Paper |
