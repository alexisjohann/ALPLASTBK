# Chapter ↔ Appendix Mapping

> **EBF Framework - Vollständiges Navigationsverzeichnis**
>
> Letzte Aktualisierung: 2026-01-06

---

## Übersicht

Das EBF Dokument folgt einer dualen Struktur:
- **Hauptkapitel (1-19):** Konzeptuelle Darstellung, narrativer Fluss
- **Appendices (49):** Technische Details, formale Spezifikationen, Beweise

Jedes Appendix ist mit mindestens einem Hauptkapitel verlinkt. Dieses Dokument bietet bidirektionale Navigation.

---

## Die acht 9C CORE-Appendices

Die 9C CORE-Appendices beantworten die acht fundamentalen Fragen des EBF Frameworks:

| CORE | Code | Appendix | Frage | Symbol | Primary Chapter |
|------|------|----------|-------|--------|-----------------|
| **WHO** | AAA | [Aggregation Levels](../appendices/AAA_aggregation_levels.tex) | Wer hat Utility? | $L$ | Ch. 2 |
| **WHAT** | C | [FEPSDE Matrix](../appendices/C_fepsde_matrix.tex) | Was ist Utility? | $d$ | Ch. 3 |
| **HOW** | B | [Complementarity](../appendices/B_complementarity_levels.tex) | Wie interagieren sie? | $\gamma$ | Ch. 4 |
| **WHEN** | V | [Ψ-Dimensions](../appendices/V_psi_dimensions.tex) | Wann zählt Kontext? | $\Psi$ | Ch. 5 |
| **WHERE** | BBB | [Estimation Methodology](../appendices/BBB_estimation_methodology.tex) | Woher kommen die Zahlen? | $\Theta, E(\theta)$ | Ch. 6 |
| **AWARE** | AU | [The Awareness Function](../appendices/AU_bcm_axiom_formalization.tex) | Wie bewusst bin ich mir? | $A(\cdot)$ | Ch. 11 |
| **READY** | AV | [The Willingness Function](../appendices/AV_willingness_formalization.tex) | Wie handlungsbereit bin ich? | $WAX, \theta$ | Ch. 12 |
| **STAGE** | AW | [Behavioral Change Journey](../appendices/AW_behavioral_change_journey.tex) | Wo in der Veränderung? | $S(t), dS/dt$ | Ch. 13 |

### Die integrierte EBF Formel

```
Stage 1: Utility Definition (COREs 1-5)
U^{pot}_{total}(Ψ) = Σ_L α^L(Ψ) · [ Σ_d ω^L_d · U^L_d + Σ_{d<d'} γ^L_{dd'} · U^L_d · U^L_{d'} ]

Stage 2: Awareness Filter (CORE 6: AWARE)
U^{eff}_{total}(t*) = A(t*) × U^{pot}_{total}

Stage 3: Action Threshold (CORE 7: READY)
Action ⟺ WAX(U^{eff}, φ, Ψ) ≥ θ(Ψ)

Stage 4: Behavioral Change Journey (CORE 8)
dS/dt = (1/τ) · [S*(A, WAX, Ψ) - S(t)]

Wobei:
  L        ← CORE-WHO (AAA): Ebenen
  d        ← CORE-WHAT (C): Dimensionen
  γ        ← CORE-HOW (B): Interaktionen
  Ψ, α     ← CORE-WHEN (V): Kontext
  E(θ)     ← CORE-WHERE (BBB): Parameterschätzungen
  A(t*)    ← CORE-AWARE (AU): Salienz-Filter (Transformation U_pot → U_eff)
  WAX, θ   ← CORE-READY (AV): Handlungsschwelle (Brücke Wissen → Handeln)
  S(t), τ  ← CORE-STAGE (AW): Behavioral Change Journey (Veränderungsdynamik)
```

---

## Kapitel → Appendix Mapping

### Kapitel 1: Introduction
| Appendix | Name | Relevanz |
|----------|------|----------|
| I | Nobel Contributions | Historische Einordnung |
| H | Computational History | Entwicklungsgeschichte |
| G | Glossary | Terminologie |

### Kapitel 2: Rationality as Stability
| Appendix | Name | Relevanz |
|----------|------|----------|
| T | Metatheory | Philosophische Grundlagen |
| U | Kahneman-Tversky | Behavioral Foundations |

### Kapitel 3: Limits of Classical Utility
| Appendix | Name | Relevanz |
|----------|------|----------|
| U | Kahneman-Tversky | Prospect Theory |
| AD | Evolutionary Game Theory | Alternative Ansätze |
| AF | Social Choice | Aggregationsprobleme |
| M | Shleifer Papers | Behavioral Finance |

### Kapitel 4: Empirical Foundations
| Appendix | Name | Relevanz |
|----------|------|----------|
| E | Operationalization | Messprotokoll |
| R | Evaluation Protocol | Validierung |
| J | Recent Papers | Aktuelle Evidenz |
| K | Fehr Papers | Experimentelle Evidenz |
| N | Heckman Papers | Kausalidentifikation |
| P | Duflo Papers | RCT-Methodik |

### Kapitel 4x: Calibration not Simulation
| Appendix | Name | Relevanz |
|----------|------|----------|
| **AN** | **LLM Monte Carlo** | **Kernmethodik** |
| BBB | Parameter Estimation | Schätzmethodik |

### Kapitel 5: Complementarity ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **B** | **CORE-HOW** | **Kerntheorie** |
| X | Milgrom-Roberts | Supermodularität |
| AC | Industrial Organization | Firmen-Komplementarität |
| AB | Matching Theory | Marktdesign |
| AE | Mechanism Design | Incentive-Komplementarität |

### Kapitel 6: Reference Structure
| Appendix | Name | Relevanz |
|----------|------|----------|
| C | CORE-WHAT | Referenzpunkte nach Dimension |
| U | Kahneman-Tversky | Prospect Theory Foundations |

### Kapitel 7: Fit and Non-Concavity
| Appendix | Name | Relevanz |
|----------|------|----------|
| B | CORE-HOW | Nicht-additive Strukturen |
| A | Formal Derivations | Mathematische Grundlagen |
| AC | Industrial Organization | Empirische Anwendung |

### Kapitel 8: Mathematical Foundations
| Appendix | Name | Relevanz |
|----------|------|----------|
| A | Formal Derivations | Herleitungen |
| D | Proofs | Beweise |
| AU | CORE-AWARE: The Awareness Function | 6th CORE: $U_{eff} = A \times U_{pot}$ |

### Kapitel 9: Context as Endogenous ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **V** | **CORE-WHEN** | **Kerntheorie** |
| AH | Temporal Context | Zeit-Dimension |
| AI | Spatial Context | Raum-Dimension |
| AAA | CORE-WHO | Level Salience |
| AG | Complexity Economics | Emergente Eigenschaften |
| L | Acemoglu Papers | Institutionen |
| Q | Bloom Papers | Unsicherheit |
| W | Information Economics | Informationsasymmetrien |

### Kapitel 10: Die Nutzenarchitektur (INU/KNU/IDN) ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| **C** | **CORE-WHAT** | **Kerntheorie** |
| **AAA** | **CORE-WHO** | **Aggregationsebenen** |
| AU | CORE-AWARE: The Awareness Function | 6th CORE |
| AJ | Social Preferences | INU/KNU/IDN |

#### Unterkapitel 10.1-10.9
| Unterkapitel | Appendix | Relevanz |
|--------------|----------|----------|
| 10.1 Three Utility Categories | AJ | Social Preferences |
| 10.2 FEPSDE Dimensions | C | Vollständige Matrix |
| 10.3 144 Components | C | Komponenten-Struktur |
| 10.6 Inter-Category Compl. | B | Interaktionsstruktur |
| 10.7 Context Modulation | V | Ψ-Modulation |
| 10.8 Aggregate Welfare | AAA | Hierarchie-Aggregation |
| 10.9.1 Labor Transitions | AA | Arbeitsmarkt |
| 10.9.2 Health Prevention | F | Worked Examples |
| 10.9.3 Financial Decisions | Y | Kapitalmärkte |
| 10.9.4 Sustainability | Z | Wachstumstheorie |

### Kapitel 11: Awareness ⭐
| Appendix | Name | Relevanz |
|----------|------|----------|
| AV | Willingness Formalization | Formale Grundlagen |
| AL | Self-Reinforcement Learning | Lernmechanismen |
| AK | Epistemics of Deviation | Belief-Formation |
| AAA | CORE-WHO | Level-spezifische Awareness |

#### Predictions (Ch. 11 Unterkapitel)
| Prediction | Appendix | Thema |
|------------|----------|-------|
| 11.1 | AO | Trade War Dynamics |
| 11.2 | AP | Cross-Level Spillovers |
| 11.3 | AQ | Asymmetric Response |
| 11.4 | AR | Techlash Dynamics |
| 11.5 | AS | Identity Activation |
| 11.6 | AT | Coherence Trap |

### Kapitel 12: Willingness
| Appendix | Name | Relevanz |
|----------|------|----------|
| **AV** | **Willingness Formalization** | **Kerntheorie** |
| AL | Self-Reinforcement Learning | Dynamik |

### Kapitel 13: Behavioral Change Journey
| Appendix | Name | Relevanz |
|----------|------|----------|
| — | — | Stage-Logik im Haupttext |

### Kapitel 14: Behavioral Change Segments
| Appendix | Name | Relevanz |
|----------|------|----------|
| — | — | Segment-Typologien im Haupttext |

### Kapitel 15: Function of Willingness, Journey & Segment
| Appendix | Name | Relevanz |
|----------|------|----------|
| AU | CORE-AWARE | Awareness-Baustein |
| AV | Willingness Formalization | Schwelle & WAX |

### Kapitel 16: Probability of Behavior Change
| Appendix | Name | Relevanz |
|----------|------|----------|
| — | — | Output-Transformation |

### Kapitel 17: Policy Implications
| Appendix | Name | Relevanz |
|----------|------|----------|
| S | Falsifiable Predictions | Testbare Vorhersagen |
| P | Duflo Papers | Policy-Evaluierung |
| F | Worked Examples | Anwendungen |

### Kapitel 18: Limitations
| Appendix | Name | Relevanz |
|----------|------|----------|
| S | Falsifiable Predictions | Was noch getestet werden muss |
| R | Evaluation Protocol | Validierungslücken |
| T | Metatheory | Philosophische Grenzen |

### Kapitel 19: Conclusion
| Appendix | Name | Relevanz |
|----------|------|----------|
| G | Glossary | Terminologie-Referenz |
| T | Metatheory | Abschließende Reflexion |

---

## Appendix → Kapitel Mapping (Alphabetisch)

| Code | Name | Category | Primary Ch. | Secondary Ch. |
|------|------|----------|-------------|---------------|
| A | Formal Derivations | FORMAL | 8 | 5, 10 |
| AA | Labor Economics | DOMAIN | 10.9.1 | 4 |
| AAA | **CORE-WHO** | **CORE** | **10.8** | 9, 11 |
| AB | Matching Theory | DOMAIN | 5 | 10.6 |
| AC | Industrial Organization | DOMAIN | 5 | 7 |
| AD | Evolutionary GT | DOMAIN | 3 | 5 |
| AE | Mechanism Design | DOMAIN | 5 | 9 |
| AF | Social Choice | DOMAIN | 3 | 10.8 |
| AG | Complexity Economics | DOMAIN | 9 | 5 |
| AH | Temporal Context | CONTEXT | 9 | 10.7 |
| AI | Spatial Context | CONTEXT | 9 | 10.7 |
| AJ | Social Preferences | DOMAIN | 10.1 | 4 |
| AK | Epistemics | DOMAIN | 11.03 | 9 |
| AL | Self-Reinforcement | METHOD | 11 | 9 |
| AN | LLM Monte Carlo | METHOD | 4x | 4 |
| AO | Prediction 1 | PREDICT | 11.1 | 9 |
| AP | Prediction 2 | PREDICT | 11.2 | 10.8 |
| AQ | Prediction 3 | PREDICT | 11.3 | 10 |
| AR | Prediction 4 | PREDICT | 11.4 | 9 |
| AS | Prediction 5 | PREDICT | 11.5 | 10.1 |
| AT | Prediction 6 | PREDICT | 11.6 | 10.8 |
| AU | CORE-AWARE: The Awareness Function | CORE | 11 | 10, 12 |
| AV | **CORE-READY: The Willingness Function** | **CORE** | **12** | 11 |
| B | **CORE-HOW** | **CORE** | **5** | 10.6, 7 |
| BBB | **CORE-WHERE** | **CORE** | **4x** | 4, 8 |
| C | **CORE-WHAT** | **CORE** | **10** | 6 |
| D | Proofs | FORMAL | 8 | All |
| E | Operationalization | METHOD | 4 | 10 |
| F | Worked Examples | REF | 10.9 | All |
| G | Glossary | REF | All | — |
| H | Computational History | REF | 1 | — |
| I | Nobel Contributions | LIT | 1 | All |
| J | Recent Papers | LIT | 4 | All |
| K | Fehr Papers | LIT | 4 | 10.1 |
| L | Acemoglu Papers | LIT | 9 | 10.8 |
| M | Shleifer Papers | LIT | 3 | 5 |
| N | Heckman Papers | LIT | 4 | 10.9 |
| O | Autor Papers | LIT | 10.9.1 | 4 |
| P | Duflo Papers | LIT | 4 | 17 |
| Q | Bloom Papers | LIT | 9 | 5 |
| QQQ | Quality Assessment | METHOD | — | All |
| R | Evaluation Protocol | METHOD | 4 | 18 |
| S | Falsifiable Predictions | PREDICT | 18 | 4 |
| T | Metatheory | REF | 2 | 18 |
| U | Kahneman-Tversky | LIT | 3, 6 | 10 |
| V | **CORE-WHEN** | **CORE** | **9** | 10.7, 11.15 |
| W | Information Economics | DOMAIN | 9 | 5 |
| X | Milgrom-Roberts | DOMAIN | 5 | 7 |
| Y | Capital Markets | DOMAIN | 10.2 | 5 |
| Z | Growth Theory | DOMAIN | 10.8 | 9 |

---

## Lesepfade

### Pfad 1: Core Theory (Essential) — 9C CORE
```
1. AAA (CORE-WHO) → Verstehe Ebenen
2. C (CORE-WHAT) → Verstehe Dimensionen
3. B (CORE-HOW) → Verstehe Interaktionen
4. V (CORE-WHEN) → Verstehe Kontext
5. BBB (CORE-WHERE) → Verstehe Parameterschätzung
6. AU (CORE-AWARE) → Verstehe Salienz-Filter (U_pot → U_eff)
7. AV (CORE-READY) → Verstehe Handlungsbereitschaft (WAX ≥ θ)
8. AW (CORE-STAGE) → Verstehe BCJ-Phase (φ ∈ {1,...,5})
```

### Pfad 2: Empirischer Forscher
```
1. CORE-WHO + CORE-WHAT → Basis-Framework
2. E (Operationalization) → Messung
3. AN (LLM Monte Carlo) → Schätzung
4. S (Predictions) → Testbare Hypothesen
```

### Pfad 3: Domain-Spezialist
```
1. CORE Appendices → Grundlagen
2. Relevantes DOMAIN Appendix → Dein Feld
3. LIT Appendices → Schlüsselforscher
```

### Pfad 4: Quick Reference
```
1. G (Glossary) → Terminologie
2. F (Worked Examples) → Anwendungen
3. Spezifisches Appendix nach Bedarf
```

---

## Cross-Reference Matrix

### CORE-WHO (AAA) referenziert:
- CORE-WHAT (C): Dimensionen auf jeder Ebene
- CORE-HOW (B): Cross-Level Komplementarität
- CORE-WHEN (V): Level Salience Funktion
- LIT-FEHR (K): Empirische Grundlagen

### CORE-WHAT (C) referenziert:
- CORE-WHO (AAA): Level-spezifische Dimensionen
- LIT-KT (U): Prospect Theory Foundations
- FORMAL-AXIOM (AU): Axiom-System

### CORE-HOW (B) referenziert:
- CORE-WHO (AAA): Cross-Level Interaktionen
- CORE-WHAT (C): Dimension-Interaktionen
- DOMAIN-COMPLEMENT (X): Milgrom-Roberts Theorie

### CORE-WHEN (V) referenziert:
- CORE-WHO (AAA): Level Salience α^L(Ψ)
- CONTEXT-TIME (AH): Temporale Details
- CONTEXT-SPACE (AI): Räumliche Details

### CORE-WHERE (BBB) referenziert:
- CORE-WHO (AAA): Level-spezifische Parameter
- CORE-WHAT (C): Dimension-spezifische Parameter
- CORE-HOW (B): Komplementaritätsparameter γ
- METHOD-LLMMC (AN): LLM Monte Carlo Schätzungen

---

## Cross-Referenzierungsregeln

Diese Regeln definieren, wann bidirektionale vs. unidirektionale Verlinkung zwischen Dokumenten erforderlich ist.

### Regel 1: Bidirektionale Verlinkung (REQUIRED)

| Verbindung | Beispiel | Begründung |
|------------|----------|------------|
| **CORE ↔ CORE** | AAA ↔ C, B ↔ V | Kernkonzepte sind interdependent |
| **Chapter ↔ Appendix** | Ch.10 ↔ C | Navigation in beide Richtungen |
| **Gleiche Hierarchie** | AH ↔ AI (beide CONTEXT) | Gleichwertige Konzepte |

**Implementation in LaTeX:**
```latex
% In Appendix AAA:
\textbf{Cross-References:}
\begin{itemize}
    \item Appendix C (CORE-WHAT): Dimensionen pro Ebene
    \item Appendix B (CORE-HOW): Cross-Level Interaktionen
\end{itemize}

% In Appendix C (entsprechend):
\textbf{Cross-References:}
\begin{itemize}
    \item Appendix AAA (CORE-WHO): Level-spezifische Dimensionen
\end{itemize}
```

### Regel 2: Unidirektionale Verlinkung (OK)

| Verbindung | Richtung | Begründung |
|------------|----------|------------|
| **CORE → DOMAIN** | AAA → AJ | Hierarchisch: CORE definiert, DOMAIN wendet an |
| **DOMAIN → CORE** | AJ → C | DOMAIN referenziert Quelle, nicht umgekehrt |
| **ANY → LIT** | C → U | Literatur-Appendices werden nur zitiert |
| **ANY → G (Glossary)** | Alle → G | Glossar ist One-to-Many Referenz |
| **ANY → F (Examples)** | Alle → F | Beispiele werden referenziert, nicht umgekehrt |

**Hierarchie-Prinzip:**
```
CORE (definiert)
  ↓
DOMAIN/METHOD (wendet an)
  ↓
PREDICT/LIT (dokumentiert)
  ↓
REF (unterstützt)
```

### Regel 3: Chapter Linkage Box (REQUIRED in jedem Appendix)

Jedes Appendix MUSS eine Chapter Linkage Box enthalten:

```latex
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!50!black, title=Chapter Linkage]
\textbf{Primary Chapter:} Ch. X (Title)
\begin{itemize}[nosep]
    \item Ch. X.1: Specific section
    \item Ch. X.2: Another section
\end{itemize}
\textbf{Secondary:} Ch. Y, Ch. Z
\end{tcolorbox}
```

### Regel 4: Cross-Reference Map (REQUIRED für CORE/DOMAIN)

CORE und DOMAIN Appendices MÜSSEN eine Cross-Reference Map haben:

```latex
\begin{tcolorbox}[colback=purple!5!white, colframe=purple!50!black, title=Cross-Reference Map]
\textbf{Dieses Appendix referenziert:}
\begin{itemize}[nosep]
    \item Appendix X: Grund
    \item Appendix Y: Grund
\end{itemize}
\textbf{Referenziert von:}
\begin{itemize}[nosep]
    \item Appendix Z: Kontext
\end{itemize}
\end{tcolorbox}
```

### Regel 5: Wann NICHT verlinken

- **Keine zirkulären Abhängigkeiten** zwischen mehr als 3 Appendices
- **Keine Trivial-Links** (z.B. jedes Appendix zu Glossary einzeln auflisten)
- **Keine spekulativen Links** zu geplanten aber nicht existierenden Appendices

### Entscheidungsbaum

```
Neuer Link von A → B?
│
├─ Ist B ein CORE Appendix?
│  ├─ Ja: Ist A auch CORE? → Bidirektional
│  └─ Nein: A verlinkt B, B muss nicht zurück
│
├─ Ist B ein LIT/REF Appendix?
│  └─ Unidirektional (A → B nur)
│
├─ Sind A und B gleiche Kategorie?
│  └─ Bidirektional wenn inhaltlich verwandt
│
└─ Hierarchisch unterschiedlich?
   └─ Höhere Ebene wird nicht zurück verlinkt
```

### Checkliste für neue Appendices

- [ ] Chapter Linkage Box vorhanden
- [ ] Primary Chapter korrekt identifiziert
- [ ] Cross-Reference Map (wenn CORE/DOMAIN)
- [ ] Bidirektionale Links zu CORE Appendices geprüft
- [ ] Keine zirkulären Abhängigkeiten >3
- [ ] In `00_appendix_index.tex` eingetragen
- [ ] In dieser Mapping-Datei eingetragen

---

*Generiert: 2026-01-06 | Quelle: appendices/00_appendix_index.tex*
