# EBF Appendix-Kategorien: Definitive Spezifikation

> Version 1.2 | Januar 2026 | Status: Authoritative

---

## Übersicht

Das EBF Framework verwendet **50 Appendices** organisiert in **8 Kategorien**. Jede Kategorie hat eine spezifische Funktion im Gesamtsystem.

| # | Prefix | Kategorie | Anzahl | Priorität | Funktion |
|---|--------|-----------|--------|-----------|----------|
| 1 | `CORE-` | Core Theory | 10 | Essential | Was ist EBF? |
| 2 | `FORMAL-` | Formalization | 2 | High | Ist es mathematisch rigoros? |
| 3 | `DOMAIN-` | Application Domains | 13 | Medium | Wo kann man es anwenden? |
| 4 | `CONTEXT-` | Context Dimensions | 3 | Medium | Wie wirkt Kontext im Detail? |
| 5 | `METHOD-` | Methodology | 4 | High | Wie operationalisiert man es? |
| 6 | `PREDICT-` | Predictions | 7 | Essential | Was sagt es vorher? |
| 7 | `LIT-` | Literature | 10 | Medium-High | Worauf baut es auf? |
| 8 | `REF-` | Reference | 4 | High (G) | Wie nutzt man es? |

---

## 1. CORE- (Core Theory)

### Definition
Die fundamentalen Bausteine des EBF Frameworks. Ohne diese Appendices funktioniert das Framework nicht. Jeder CORE beantwortet genau EINE der zehn fundamentalen Fragen der Wohlfahrtstheorie (10C).

### Funktion
- Definiert den kompletten Utility-Raum U^L_d(Ψ)
- Spezifiziert Parameter und deren Kalibrierung
- Etabliert den Awareness-Filter A(·) und Action-Threshold WAX ≥ θ

### Zusätzliche Anforderungen (über Standard hinaus)
- [ ] Vollständiges Axiomensystem (min. 8-200 Axiome je nach CORE)
- [ ] 80-150+ Referenzen, kategorisiert
- [ ] 5-10 Critical Foundations (Einwände + Antworten)
- [ ] 5-8 Open Issues mit Research Roadmap
- [ ] Bidirektionale Integration mit ALLEN anderen COREs
- [ ] Min. 20 Symbol-Definitionen

### Mitglieder

| Code | Name | Frage | Output |
|------|------|-------|--------|
| AAA | CORE-WHO | Wer hat Utility? | Levels L |
| C | CORE-WHAT | Was ist Utility? | Dimensionen d (FEPSDE) |
| B | CORE-HOW | Wie interagieren sie? | Komplementarität γ |
| V | CORE-WHEN | Wann zählt Kontext? | Kontext Ψ |
| BBB | CORE-WHERE | Woher die Zahlen? | Parameter Θ, E(θ) |
| AU | CORE-AWARE | Wie bewusst? | Awareness A(·) |
| AV | CORE-READY | Wie handlungsbereit? | Willingness WAX, θ |
| AW | CORE-STAGE | Wo in der Veränderung? | Journey S(t), dS/dt |
| HI | CORE-HIERARCHY | Wie stratifizieren Entscheidungen? | Levels L0-L3, N_L2 |
| IE | CORE-EIT | Wie emergieren Interventionen? | T1-T8 Primitives, W_eff |

### Output: Die EBF Verhaltensgleichung

```
Stage 1: U^pot = Σ_L α^L(Ψ) · [Σ_d ω^L_d · U^L_d + Σ γ^L_dd' · U^L_d·U^L_d']
Stage 2: U^eff(t*) = A(t*) × U^pot
Stage 3: Action ⟺ WAX(U^eff, φ, Ψ) ≥ θ(Ψ)
Stage 4: dS/dt = (1/τ) · [S*(A, WAX, Ψ) - S(t)]
```

---

## 2. FORMAL- (Formalization)

### Definition
Mathematische Grundlagen, Derivationen und formale Beweise, die die theoretische Rigorosität des EBF Frameworks sicherstellen.

### Funktion
- Ableitung der Kerngleichungen aus Grundprinzipien
- Formale Beweise aller Propositionen und Theoreme
- Mathematische Konsistenzprüfung
- Verbindung zu etablierter Mathematik (Topologie, Maßtheorie, etc.)

### Mitglieder

| Code | Name | Inhalt |
|------|------|--------|
| A | FORMAL-DERIVE | Mathematische Grundlagen & Derivationen |
| D | FORMAL-PROOF | Formale Beweise der Theoreme |

### Beziehung zu CORE
- Beweist, was CORE postuliert
- Zeigt Ableitungspfade
- Validiert mathematische Konsistenz

### Zielgruppe
Mathematiker, theoretische Ökonomen, Peer-Reviewer

---

## 3. DOMAIN- (Application Domains)

### Definition
Anwendung des EBF Frameworks auf spezifische Subfelder der Ökonomie. Zeigt, wie die allgemeine Theorie domänenspezifische Phänomene erklärt.

### Funktion
- Translation der 10C CORE Konzepte in Domänensprache
- Identifikation domänenspezifischer Parameter
- Verknüpfung mit etablierter Literatur des Feldes
- Generierung domänenspezifischer Vorhersagen

### Struktur jedes DOMAIN-Appendix
1. **Übersetzung:** 10C → Domänenkonzepte
2. **Literaturverbindung:** BCM vs. Standard-Modelle
3. **Mehrwert:** Was erklärt BCM, was Standard nicht kann?
4. **Kalibrierung:** Domänenspezifische Parameterwerte
5. **Case Study:** Mindestens ein durchgerechnetes Beispiel

### Mitglieder

| Code | Name | Feld |
|------|------|------|
| AA | DOMAIN-LABOR | Arbeitsmarktökonomie |
| AB | DOMAIN-MATCH | Matching & Market Design |
| AC | DOMAIN-IO | Industrial Organization |
| AD | DOMAIN-EVO | Evolutionäre Spieltheorie |
| AE | DOMAIN-MECH | Mechanism Design |
| AF | DOMAIN-CHOICE | Social Choice Theory |
| AG | DOMAIN-COMPLEX | Complexity Economics |
| AJ | DOMAIN-SOCIAL | Soziale Präferenzen |
| AK | DOMAIN-EPISTEMIC | Epistemik & Beliefs |
| W | DOMAIN-INFO | Informationsökonomie |
| X | DOMAIN-COMPLEMENT | Milgrom-Roberts Supermodularität |
| Y | DOMAIN-CAPITAL | Kapitalmärkte |
| Z | DOMAIN-GROWTH | Wachstumstheorie |

---

## 4. CONTEXT- (Context Dimensions)

### Definition
Detaillierte Analyse einzelner Ψ-Dimensionen des Kontextframeworks. Erweiterung von CORE-WHEN (V) mit Tiefenanalyse spezifischer Kontexte.

### Funktion
- Spezifikation, wie einzelne Ψ-Dimensionen Verhalten modulieren
- Messprotokolle für Kontextvariablen
- Interaktionseffekte zwischen Kontextdimensionen
- Dynamik: Wie Kontext sich über Zeit/Raum verändert

### Die 8 Ψ-Dimensionen (definiert in V)

| Ψ₁ | Ψ₂ | Ψ₃ | Ψ₄ |
|----|----|----|---|
| Economic | Social | Temporal | Spatial |

| Ψ₅ | Ψ₆ | Ψ₇ | Ψ₈ |
|----|----|----|---|
| Institutional | Cultural | Technological | Environmental |

### Mitglieder

| Code | Name | Ψ-Dimension |
|------|------|-------------|
| AH | CONTEXT-TIME | Temporaler Kontext (Ψ_T) |
| AI | CONTEXT-SPACE | Räumlicher Kontext (Ψ_Sp) |
| V | CONTEXT-MASTER | Alle 8 Ψ-Dimensionen (= CORE-WHEN) |

### Beziehung zu CORE-WHEN
- CORE-WHEN (V) definiert das Framework
- CONTEXT-TIME/SPACE vertiefen einzelne Dimensionen
- Weitere CONTEXT-Appendices möglich (CONTEXT-CULTURE, etc.)

---

## 5. METHOD- (Methodology)

### Definition
Methodologische Tools für Parameterschätzung, Operationalisierung, Validierung und dynamische Modellierung innerhalb EBF.

### Funktion
- **WIE** man EBF Parameter empirisch schätzt
- **WIE** man EBF Konzepte messbar macht
- **WIE** man EBF Vorhersagen validiert
- **WIE** Lerndynamiken modelliert werden

### Mitglieder

| Code | Name | Methode |
|------|------|---------|
| AN | METHOD-LLMMC | LLM Monte Carlo Estimation |
| AL | METHOD-SRL | Self-Reinforcement Learning |
| E | METHOD-OPS | Operationalization Protocol |
| R | METHOD-EVAL | Evaluation Framework |

### Beziehung zu CORE-WHERE (BBB)
- BBB definiert **WAS** geschätzt werden muss
- METHOD definiert **WIE** es geschätzt wird
- AN (LLM MC) ist die primäre Schätzmethode für BBB

### Epistemic Status Tags (aus AN)

| Tag | Bedeutung | Konfidenz |
|-----|-----------|-----------|
| EMP | Empirisch validiert | Höchste |
| THR | Theoretisch abgeleitet | Hoch |
| LLM | LLM Monte Carlo geschätzt | Mittel |
| ILL | Illustrativ | Niedrig |
| HYP | Hypothetisch | Niedrigste |

---

## 6. PREDICT- (Predictions)

### Definition
Falsifizierbare Vorhersagen, die aus EBF abgeleitet werden. Macht die Theorie empirisch testbar und wissenschaftlich rigorös.

### Funktion
- Ableitung testbarer Hypothesen aus 10C CORE
- Spezifikation von Falsifikationsbedingungen
- Dokumentation von Vorhersage-Erfolgen und -Fehlern
- Unterscheidung EBF von konkurrierenden Theorien

### Struktur jeder Prediction
1. **Ableitung:** Welche CORE-Axiome implizieren diese Vorhersage?
2. **Formalisierung:** Mathematische Spezifikation
3. **Testdesign:** Wie könnte man diese Vorhersage testen?
4. **Falsifikation:** Was würde die Vorhersage widerlegen?
5. **Status:** Getestet/Ungetestet/Bestätigt/Widerlegt

### Mitglieder

| Code | Name | Vorhersage-Fokus |
|------|------|------------------|
| S | PREDICT-MASTER | 10 Kern-Hypothesen |
| AO | PREDICT-01 | Trade War Dynamics |
| AP | PREDICT-02 | Cross-Level Spillovers |
| AQ | PREDICT-03 | Asymmetric Response |
| AR | PREDICT-04 | Techlash Dynamics |
| AS | PREDICT-05 | Identity Activation |
| AT | PREDICT-06 | Coherence Trap |

### Wissenschaftlicher Wert
> "Eine Theorie, die nichts verbietet, erklärt nichts." — Karl Popper

EBF macht riskante Vorhersagen → empirisch prüfbar

---

## 7. LIT- (Literature)

### Definition
Systematische Integration der Forschungsliteratur in EBF, organisiert nach Schlüsselautoren und deren Beiträgen.

### Funktion
- Verbindung EBF zu etablierter Forschung
- Nachweis der empirischen Fundierung
- Identifikation, wo EBF über bestehende Arbeit hinausgeht
- Kredibilitätsaufbau durch Literaturverankerung

### Struktur jedes LIT-Appendix
1. **Autor-Profil:** Schlüsselbeiträge, Nobel-Status
2. **Paper-Review:** Wichtigste 10-20 Papers
3. **BCM-Mapping:** Welche CORE-Konzepte entsprechen welchen Findings?
4. **Erweiterung:** Wo geht EBF über diesen Autor hinaus?
5. **Offene Fragen:** Was bleibt ungeklärt?

### Mitglieder

| Code | Name | Forscher | Beitrag zu BCM |
|------|------|----------|----------------|
| I | LIT-NOBEL | Nobel-Laureaten | Foundational Economics |
| J | LIT-RECENT | Papers 2020-2025 | State of the Art |
| K | LIT-FEHR | Ernst Fehr | Soziale Präferenzen |
| L | LIT-ACEMOGLU | Daron Acemoglu | Institutionen |
| M | LIT-SHLEIFER | Andrei Shleifer | Behavioral Finance |
| N | LIT-HECKMAN | James Heckman | Humankapital |
| O | LIT-AUTOR | David Autor | Arbeitsmärkte |
| P | LIT-DUFLO | Esther Duflo | RCTs |
| Q | LIT-BLOOM | Nick Bloom | Uncertainty |
| U | LIT-KT | Kahneman-Tversky | Prospect Theory |
| OT | LIT-OTHER | Miscellaneous | Catch-all for unassigned papers |

### LIT-Appendix Typen (Unified Taxonomy)

Das EBF verwendet eine **einheitliche LIT-Taxonomie** mit vier Subtypen:

```
LIT-Kategorie (alle Paper-Sammlungen)
├── LIT-R-[AUTOR]    → Researcher: Autoren-basiert
├── LIT-D-[FELD]     → Domain: Feld-Literatur (Cross-Ref zu DOMAIN-Appendix)
├── LIT-M-[THEMA]    → Meta: Methodisch/Historisch/Kritisch
└── LIT-O            → Other: Catch-all für Einzelpapers
```

| Subtyp | Code-Pattern | Beispiele | Zweck | Anzahl |
|--------|--------------|-----------|-------|--------|
| **LIT-R** (Researcher) | `LIT-R-[NACHNAME]` | LIT-R-FEHR, LIT-R-THALER, LIT-R-GNEEZY | Forschung eines Autors/Teams | 45 |
| **LIT-D** (Domain) | `LIT-D-[FELD]` | LIT-D-LABOR, LIT-D-FINANCE | Feld-spezifische Literaturübersicht | (via DOMAIN) |
| **LIT-M** (Meta) | `LIT-M-[THEMA]` | LIT-M-META, LIT-M-HISTORY, LIT-M-CRITIQUE | Methodisch/Historisch/Kritisch | 6 |
| **LIT-O** (Other) | `LIT-O` | OT | Catch-all mit thematischen Clustern | 1 |

#### LIT-R (Researcher) — Autoren-basiert

> **Logische Mapping:** Bestehende Codes bleiben, Subtyp implizit LIT-R

| Code | Implizit | Name | Forscher |
|------|----------|------|----------|
| K | LIT-R-FEHR | LIT-FEHR | Ernst Fehr |
| THL | LIT-R-THALER | LIT-THALER | Richard Thaler |
| GN | LIT-R-GNEEZY | LIT-GNEEZY | Uri Gneezy |
| U | LIT-R-KT | LIT-KT | Kahneman-Tversky |
| ... | ... | (45 weitere) | ... |

#### LIT-M (Meta) — Methodisch/Historisch/Kritisch

| Code | Implizit | Name | Inhalt | Wann hierher? |
|------|----------|------|--------|---------------|
| AX | LIT-M-META | LIT-META | Metascience & Integration | Papers über wissenschaftliche Methodik |
| AY | LIT-M-PARADIGMS | LIT-PARADIGMS | Multi-disciplinary | Paradigmen-Vergleiche, Theoriegeschichte |
| XV | LIT-M-HISTORY | LIT-HISTORY | Scientific History | Historische Entwicklung (>50 Jahre alt) |
| XVI | LIT-M-CRITIQUE | LIT-CRITIQUE | Critical Literature | Kritiken am EBF oder Verhaltensökonomie |
| XVII | LIT-M-THERMO | LIT-THERMODYNAMICS | Economic Impact | Physik-Ökonomie Analogien |
| XIX | LIT-M-LEARNING | LIT-LEARNING | Experience Goods | Lerndynamiken, Belief Updating |

#### LIT-D (Domain) — Feld-Literatur

> **Wichtig:** LIT-D ist kein separater Appendix, sondern eine **logische Verknüpfung** zu DOMAIN-Appendices.
> Papers werden primär in LIT-R integriert, DOMAIN-Appendices enthalten Cross-Referenzen.

| DOMAIN-Code | Implizit LIT-D | Inhalt |
|-------------|----------------|--------|
| AA | (LIT-D-LABOR) | Arbeitsmarkt-Papers → Refs zu LIT-R-FEHR, LIT-R-AUTOR, etc. |
| Y | (LIT-D-CAPITAL) | Kapitalmarkt-Papers → Refs zu LIT-R-SHLEIFER, etc. |

#### LIT-O (Other) — Catch-all

> **Code:** OT
> **Zweck:** Papers, die keinen eigenen LIT-R Appendix rechtfertigen
> **Struktur:** Thematische Cluster (siehe unten)

### LIT-Matching-Regeln (Threshold-basiert)

#### Entscheidungsbaum: Wohin gehört ein Paper?

```
Neues Paper integrieren?
│
├─► SCHRITT 0: Ist es ein METHODISCHES/HISTORISCHES/KRITISCHES Paper?
│   │   (Metascience, Paradigmen, >50 Jahre alt, Kritik an BE)
│   └─► JA → In entsprechenden THEMATISCHEN LIT-Appendix
│       ├── Metascience → LIT-META (AX)
│       ├── Paradigmenvergleich → LIT-PARADIGMS (AY)
│       ├── Historisch (>50J) → LIT-HISTORY (XV)
│       ├── Kritik → LIT-CRITIQUE (XVI)
│       ├── Physik-Analogie → LIT-THERMODYNAMICS (XVII)
│       └── Lerndynamik → LIT-LEARNING (XIX)
│
├─► SCHRITT 1: Existiert bereits ein AUTOREN-LIT für diesen Autor?
│   └─► JA → Paper in diesem LIT-Appendix integrieren ✅
│
├─► SCHRITT 2: Ist es eine DIREKTE ERWEITERUNG eines Autors im LIT?
│   │   (z.B. Heath & Soll (1996) erweitert Thaler's Mental Accounting)
│   └─► JA → Paper im LIT-Appendix des Primärautors integrieren ✅
│
├─► SCHRITT 3: Erfüllt der Autor die Threshold-Kriterien für eigenen LIT?
│   │   (Siehe Tabelle unten)
│   └─► JA → Neuen LIT-[AUTOR] Appendix erstellen
│   └─► NEIN → Weiter zu Schritt 4
│
└─► SCHRITT 4: Paper in OT (LIT-OTHER) mit thematischem Cluster
    └─► Thematische Cluster: Choice Architecture, Cognitive Psychology,
        Prosocial Motivation, Organizational Psychology, etc.
```

#### Threshold-Kriterien für eigenen LIT-Appendix

| Kriterium | Threshold | Bemerkung |
|-----------|-----------|-----------|
| **Anzahl Papers** | ≥5 relevante EBF-Papers | Von Einzelautor oder Autorenteam |
| **ODER: Nobel-Preis** | Ja | Automatisch eigener LIT-Appendix |
| **ODER: Fundamentaler EBF-Beitrag** | Ja | Kernergebnis zitiert in ≥3 CORE Appendices |
| **ODER: DACH-Relevanz** | Primärautor von ≥3 Papers | Für regionale Forschungsintegration |

#### Migration-Regeln (OT → Eigener LIT)

| Trigger | Aktion |
|---------|--------|
| Autor akkumuliert ≥5 Papers in OT | Migration zu neuem LIT-[AUTOR] Appendix |
| Autor erhält Nobel-Preis | Sofortige Migration |
| Paper wird in ≥3 CORE Appendices zitiert | Prüfung auf eigenen LIT-Appendix |

#### Struktur in OT (LIT-OTHER)

Papers in OT werden nach **thematischen Clustern** organisiert:

| Cluster | Typische Papers | Beispiel |
|---------|-----------------|----------|
| Choice Architecture | Entscheidungsdesign, Menü-Sizing | Iyengar & Lepper (2000) |
| Cognitive Psychology | Kognitive Kapazität, Aufmerksamkeit | Miller (1956) |
| Prosocial Motivation | Altruismus, Meaning at Work | Grant (2008) |
| Organizational Psychology | Commitment, Kultur | Meyer & Allen (1991) |
| Market Morality | Markt-Normen-Interaktion | Falk & Szech (2013) |

#### Aktuelle LIT-Statistik (Stand: 2026-01-19)

| Typ | Anzahl | Beschreibung |
|-----|--------|--------------|
| Dedizierte Autoren-LIT | 45 | Fehr, Thaler, Kahneman, Gneezy, etc. |
| Thematische LIT | 6 | META, PARADIGMS, HISTORY, CRITIQUE, THERMODYNAMICS, LEARNING |
| Catch-all (OT) | 1 | LIT-OTHER mit thematischen Clustern |
| **Total LIT-Appendices** | **52** | |

#### Wann neuen thematischen LIT erstellen?

| Kriterium | Threshold |
|-----------|-----------|
| **Anzahl Papers** | ≥10 Papers zu einem Thema in OT akkumuliert |
| **ODER: Fundamentales Konzept** | Konzept wird in ≥5 CORE Appendices referenziert |
| **ODER: Methodische Grundlage** | Eigene methodische Tradition (z.B. Experimentaldesign) |

**Beispiel:** Wenn OT >10 Papers zu "Nudge Ethics" hätte → neuer LIT-ETHICS Appendix

### LIT vs. DOMAIN: Wann wohin?

Papers können sowohl in **LIT** als auch in **DOMAIN** referenziert werden - mit unterschiedlichem Fokus:

| Aspekt | LIT-Appendix | DOMAIN-Appendix |
|--------|--------------|-----------------|
| **Organisiert nach** | Autor/Forscherteam | Anwendungsfeld |
| **Fokus** | WER hat es erforscht | WO wird es angewendet |
| **Inhalt** | Vollständige Paper-Integration mit 10C-Mapping | Anwendung auf Domäne |
| **Tiefe** | Detailliert (10-20 Papers pro Autor) | Übersicht (Papers verschiedener Autoren) |
| **Primäre Quelle** | Ja (BibTeX-Keys, Evidenz-Tags) | Nein (referenziert LIT) |

#### Entscheidungsbaum: LIT oder DOMAIN?

```
Neues Paper integrieren?
│
├─► Ist das Paper eine EMPIRISCHE STUDIE oder THEORIE-BEITRAG?
│   └─► JA → Primär in LIT (nach Autor)
│           Sekundär: Cross-Referenz in DOMAIN falls relevant
│
├─► Ist das Paper eine ANWENDUNGS-STUDIE auf ein Feld?
│   └─► JA → Primär in DOMAIN
│           Sekundär: In LIT des Autors verlinken
│
└─► Ist das Paper ein REVIEW/META-ANALYSE eines Feldes?
    └─► JA → Primär in DOMAIN (zeigt Feldüberblick)
```

#### Beispiel: Fehr & Schmidt (1999) - "Inequity Aversion"

| Appendix | Wie integriert? |
|----------|-----------------|
| **LIT-FEHR (K)** | Vollständige Integration: Axiome, Formeln, 10C-Mapping, Kritik |
| **DOMAIN-LABOR (AA)** | Referenz: "Fairness in Löhnen, siehe LIT-FEHR K" |
| **DOMAIN-SOCIAL (AJ)** | Referenz: "Soziale Präferenzen Grundmodell, siehe LIT-FEHR K" |

→ **Primäre Integration in LIT, Cross-Referenz in DOMAIN**

#### Beispiele für korrekte Zuordnung

**Autoren-LIT Beispiele:**

| Paper | Zuordnung | Begründung |
|-------|-----------|------------|
| Heath & Soll (1996) | LIT-THALER (THL) | Direkte Erweiterung von Thaler's Mental Accounting |
| Gneezy & Rustichini (2000) | LIT-GNEEZY (GN) | Gneezy hat eigenen LIT-Appendix |
| Fehr & Schmidt (1999) | LIT-FEHR (K) | Fehr ist Erstautor |

**Thematische LIT Beispiele:**

| Paper | Zuordnung | Begründung |
|-------|-----------|------------|
| Kuhn (1962) Structure of Revolutions | LIT-PARADIGMS (AY) | Wissenschaftstheorie, Paradigmen |
| Open Science Collaboration (2015) | LIT-META (AX) | Metascience, Replikationskrise |
| Bernoulli (1738) | LIT-HISTORY (XV) | >50 Jahre alt, historische Grundlage |
| Binmore (2008) Critique of BE | LIT-CRITIQUE (XVI) | Kritik an Verhaltensökonomie |
| Ackerberg (2003) Learning | LIT-LEARNING (XIX) | Experience Goods, Belief Updating |

**OT (LIT-OTHER) Beispiele:**

| Paper | Zuordnung | Begründung |
|-------|-----------|------------|
| Iyengar & Lepper (2000) | OT → Choice Architecture | Einzelnes einflussreiches Paper |
| Miller (1956) | OT → Cognitive Psychology | Kognitive Grundlage, nicht BE-Autor |
| Grant (2008) | OT → Prosocial Motivation | Einzelpaper, kein eigener LIT |
| Meyer & Allen (1991) | OT → Organizational Psych | Commitment-Theorie, Einzelpaper |

---

## 8. REF- (Reference)

### Definition
Referenzmaterialien zur Unterstützung der Nutzung des EBF Frameworks. Keine neue Theorie, sondern Hilfsmittel für Verständnis und Anwendung.

### Funktion
- Schneller Nachschlag von Begriffen und Symbolen
- Durchgerechnete Beispiele zum Lernen
- Historischer Kontext der Framework-Entwicklung
- Philosophische Grundlagen (Metatheorie)

### Mitglieder

| Code | Name | Inhalt |
|------|------|--------|
| F | REF-EXAMPLES | Worked Examples |
| G | REF-GLOSSARY | Complete Glossary |
| H | REF-HISTORY | Computational History |
| T | REF-META | Metatheoretical Foundations |

### Besondere Rolle von G (GLOSSARY)

**G ist die "Single Source of Truth" für Notation:**

- [ ] JEDER Appendix MUSS auf G verweisen
- [ ] ALLE neuen Symbole müssen in G aufgenommen werden
- [ ] Konsistenzprüfung gegen G vor Veröffentlichung

---

## Entscheidungsbaum: Welche Kategorie?

```
Neuer Appendix erstellen?
│
├─► Beantwortet eine der 10C Fragen?
│   └─► JA → CORE-
│
├─► Enthält mathematische Beweise?
│   └─► JA → FORMAL-
│
├─► Wendet BCM auf ein Ökonomie-Subfeld an?
│   └─► JA → DOMAIN-
│
├─► Vertieft eine spezifische Ψ-Dimension?
│   └─► JA → CONTEXT-
│
├─► Beschreibt Schätzung/Messung/Validierung?
│   └─► JA → METHOD-
│
├─► Formuliert testbare Vorhersagen?
│   └─► JA → PREDICT-
│
├─► Integriert Forschungsliteratur eines Autors?
│   └─► JA → LIT-
│
└─► Ist ein Hilfsmittel (Glossar, Beispiele)?
    └─► JA → REF-
```

---

## Namenskonvention

Jeder Appendix folgt dem Muster:

```
[CODE] [CATEGORY]-[NAME]: [Descriptive Title]
```

**Beispiele:**
- `AAA CORE-WHO: The Welfare Hierarchy`
- `AN METHOD-LLMMC: LLM Monte Carlo Estimation`
- `K LIT-FEHR: Ernst Fehr Research Integration`

---

## Qualitätskriterien

### Alle Appendices MÜSSEN:
- [ ] Auf Appendix GLS (Glossary) verweisen
- [ ] Konsistente Symbole verwenden
- [ ] Quick Reference Box haben
- [ ] Mindestens ein Worked Example enthalten
- [ ] Cross-References zu verwandten Appendices haben

### CORE Appendices MÜSSEN zusätzlich:
- [ ] Vollständiges Axiomensystem
- [ ] 80-150+ Referenzen
- [ ] 5-10 Critical Foundations
- [ ] Bidirektionale Integration mit allen anderen COREs

---

## Changelog

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.2 | 2026-01-19 | Unified LIT-Taxonomie (Option C): LIT-R, LIT-D, LIT-M, LIT-O Subtypen |
| 1.1 | 2026-01-19 | LIT-Matching-Regeln hinzugefügt (Threshold-Kriterien, Migration, OT-Cluster) |
| 1.0 | 2026-01 | Initial definitive specification |

---

*Dieses Dokument ist die autoritative Quelle für Appendix-Kategorien im EBF Framework.*
