# Systematische Literaturanalyse — EBF Workflow (SLA)

> **Version:** 1.0 | **Erstellt:** 2026-02-11 | **Status:** ACTIVE
> **Skill:** `/literature-analysis` | **SSOT:** Dieses Dokument
> **Abhängigkeiten:** /paper-search, /integrate-paper, /add-paper, EIP, 8D-Algorithmus

---

## Warum dieser Workflow?

Das EBF hat exzellente Werkzeuge für **einzelne Papers** (9 Skills, 40+ Scripts, 2'358 Papers).
Was fehlte: Ein systematischer Prozess für die Frage **«Was weiss die Wissenschaft zu Thema X?»**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EINZELNES PAPER          vs.          SYSTEMATISCHE ANALYSE            │
│  ─────────────────────                 ──────────────────────           │
│  /add-paper                            /literature-analysis             │
│  /integrate-paper                                                       │
│  /upgrade-paper                                                         │
│                                                                         │
│  «Integriere Frey 1997»               «Was weiss die Wissenschaft      │
│                                         über NIMBY und Kompensation?»   │
│                                                                         │
│  1 Paper → EBF                         N Papers → Synthese → EBF       │
│                                                                         │
│  Ziegelstein                           Gebäude                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Übersicht: 7 Phasen

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ PHASE 0  │──►│ PHASE 1  │──►│ PHASE 2  │──►│ PHASE 3  │
│ PROTOKOLL│   │ SUCHE    │   │ SCREENING│   │ KODIERUNG│
└──────────┘   └──────────┘   └──────────┘   └──────────┘
                                                   │
┌──────────┐   ┌──────────┐   ┌──────────┐        │
│ PHASE 6  │◄──│ PHASE 5  │◄──│ PHASE 4  │◄───────┘
│INTEGRATION   │ REPORT   │   │ SYNTHESE │
└──────────┘   └──────────┘   └──────────┘
```

| Phase | Name | Frage | Hauptoutput | Qualitäts-Gate |
|-------|------|-------|-------------|----------------|
| **0** | Protokoll | Was genau suchen wir? | Suchprotokoll (YAML) | Forschungsfrage SMART? |
| **1** | Suche | Welche Papers gibt es? | Kandidatenliste (N₀) | ≥3 Quellen durchsucht? |
| **2** | Screening | Welche sind relevant? | Inkludierte Papers (N₁) | Kriterien dokumentiert? |
| **3** | Kodierung | Was sagen die Papers? | Kodierungstabelle | Alle Papers kodiert? |
| **4** | Synthese | Was ist die Antwort? | Evidenz-Synthese | PRO + CONTRA? |
| **5** | Report | Wie präsentieren? | Professioneller Report | 8D-konform? |
| **6** | Integration | Wie ins EBF? | Neue Papers/Parameter/Cases | /integrate-paper pro Paper? |

---

## Modi

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WELCHER MODUS?                                                         │
│                                                                         │
│    ⚡ RAPID      15-30 min, 10-20 Papers, interner Fokus                │
│    🎯 STANDARD   1-2 Std, 20-50 Papers, intern + extern  ← [DEFAULT]   │
│    🔬 SYSTEMATIC  4+ Std, 50-200 Papers, PRISMA-konform, publizierbar  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| Aspekt | RAPID | STANDARD | SYSTEMATIC |
|--------|-------|----------|------------|
| **Quellen** | Nur bcm_master.bib | + WebSearch + Scholar | + Scopus + WoS + Cochrane |
| **Screening** | Titel-basiert | Titel + Abstract | Titel + Abstract + Volltext |
| **Kodierung** | 3-5 Dimensionen | 8-12 Dimensionen | Vollständiges Kodebuch |
| **Synthese** | Narrativ | Narrativ + Tabellen | Meta-Analyse (wenn möglich) |
| **Output** | Markdown (3-pager) | Markdown/LaTeX (10-pager) | LaTeX/PDF (30-pager) |
| **PRISMA** | Nein | Vereinfacht | Vollständig |
| **Reproduzierbar** | Teilweise | Ja (Protokoll) | Vollständig (pre-registrierbar) |

---

## PHASE 0: Suchprotokoll definieren

> **Ziel:** Exakte Definition von WAS gesucht wird, WO, und nach WELCHEN Kriterien.
> **Qualitäts-Gate:** Forschungsfrage muss SMART sein. Kriterien müssen VOR der Suche stehen.

### 0.1 Forschungsfrage(n) definieren (PICO/SPIDER)

**Für empirische Fragen (PICO):**

| Element | Abkürzung | Frage | Beispiel |
|---------|-----------|-------|----------|
| **P**opulation | P | Wer? | Schweizer Stimmbürger:innen |
| **I**ntervention | I | Was wird getan? | Finanzielle Kompensation für Infrastruktur |
| **C**omparison | C | Verglichen mit? | Keine Kompensation / Prozessuale Fairness |
| **O**utcome | O | Welches Ergebnis? | Akzeptanzrate, Zustimmung in Volksabstimmung |

**Für qualitative/explorative Fragen (SPIDER):**

| Element | Abkürzung | Frage | Beispiel |
|---------|-----------|-------|----------|
| **S**ample | S | Wer/Was? | Infrastruktur-Abstimmungen DACH |
| **P**henomenon of Interest | PI | Phänomen? | NIMBY-Effekt und Motivation Crowding |
| **D**esign | D | Studiendesign? | RCT, Survey-Experiment, natürliches Experiment |
| **E**valuation | E | Was messen? | Effektstärke, Mechanismus, Moderatoren |
| **R**esearch type | R | Forschungstyp? | Quantitativ und Mixed Methods |

**Format der Forschungsfrage:**

```yaml
research_questions:
  primary: "Wie beeinflusst finanzielle Kompensation die lokale Akzeptanz
            von Infrastrukturprojekten in der Schweiz?"
  secondary:
    - "Welche Kompensationsformen vermeiden Crowding-Out?"
    - "Wie interagiert Status Quo Bias mit Infrastruktur-Framing?"
    - "Welche Rolle spielt Ψ_K (Kultur) bei Infrastruktur-Akzeptanz?"
```

### 0.2 Inklusions-/Exklusionskriterien (VOR der Suche!)

```yaml
inclusion_criteria:
  population: "Bürger:innen in demokratischen Ländern"
  intervention: "Infrastrukturprojekte (Transport, Energie, Abfall, Digital)"
  outcome: "Akzeptanz, Zustimmung, Widerstand (quantifiziert)"
  study_design: ["RCT", "quasi-experiment", "survey-experiment", "natural-experiment", "panel"]
  time_range: "1990-2026"
  languages: ["en", "de", "fr"]
  evidence_tier: [1, 2]  # Nur Tier 1 (Gold) und Tier 2 (Silver)

exclusion_criteria:
  - "Rein theoretische Arbeiten ohne empirische Daten"
  - "Studien mit n < 50"
  - "Nicht-demokratische Kontexte (keine Partizipation)"
  - "Studien ohne klare Identifikationsstrategie"
  - "Bücher, Konferenzbeiträge ohne Peer-Review (außer NBER WP)"
```

### 0.3 Suchstrategie definieren

```yaml
search_strategy:
  # PFLICHT: Interne Quellen ZUERST (EBF Quellen-Hierarchie!)
  internal_sources:
    priority_1_bcm_master:
      tool: "python scripts/search_bibliography.py"
      queries:
        - "NIMBY infrastructure acceptance"
        - "compensation crowding-out"
        - "referendum voting infrastructure"
        - "status quo bias voting"
      filters: ["--parameter", "--eip"]

    priority_2_theory_catalog:
      tool: "python scripts/theory_papers.py"
      queries:
        - "--match-10c 'psi_I, U_S, gamma_negative'"
        - "--category CAT-29"
        - "--restriction 'crowding'"

    priority_3_case_registry:
      tool: "grep case-registry.yaml"
      queries:
        - "infrastructure"
        - "NIMBY"
        - "referendum"

  # NUR wenn intern nicht ausreichend
  external_sources:
    priority_4_web:
      tool: "WebSearch"
      queries:
        - "NIMBY compensation acceptance infrastructure site:scholar.google.com"
        - "status quo bias referendum voting behavior 2020-2026"
        - "Swiss infrastructure voting behavioral economics"
      databases:
        - "Google Scholar"
        - "SSRN"
        - "NBER Working Papers"
        - "RepEc/IDEAS"

    priority_5_specialized:  # Nur bei SYSTEMATIC Modus
      databases:
        - "Scopus"
        - "Web of Science"
        - "EconLit"
```

### 0.4 Protokoll als YAML speichern

```yaml
# Datei: data/literature-analyses/SLA-{YYYY}-{MM}-{DD}-{TOPIC}-{SEQ}.yaml

protocol:
  id: "SLA-2026-02-11-NIMBY-001"
  title: "NIMBY und Infrastruktur-Akzeptanz: Systematische Literaturanalyse"
  mode: "STANDARD"
  date_started: "2026-02-11"
  research_questions: [...]
  inclusion_criteria: [...]
  exclusion_criteria: [...]
  search_strategy: [...]
  registered: false  # true bei SYSTEMATIC Modus
```

**Qualitäts-Gate Phase 0:**
```
☐ Forschungsfrage SMART (spezifisch, messbar, erreichbar, relevant, zeitgebunden)?
☐ PICO/SPIDER vollständig?
☐ Inklusions-/Exklusionskriterien VOR Suche definiert?
☐ Suchstrategie dokumentiert (Quellen, Queries, Filter)?
☐ Protokoll als YAML gespeichert?
☐ Bei SYSTEMATIC: Protokoll pre-registriert?
```

---

## PHASE 1: Systematische Suche

> **Ziel:** ALLE relevanten Papers finden. Keine vorzeitige Selektion.
> **Qualitäts-Gate:** ≥3 Quellen durchsucht. Suchergebnisse dokumentiert.

### 1.1 Interne Suche (IMMER ZUERST!)

```bash
# Schritt 1: bcm_master.bib durchsuchen
python scripts/search_bibliography.py --eip "NIMBY infrastructure"
python scripts/search_bibliography.py --eip "compensation crowding"
python scripts/search_bibliography.py --eip "referendum status quo bias"
python scripts/search_bibliography.py --author "Frey" --parameter "crowding"

# Schritt 2: Theory Catalog durchsuchen
python scripts/theory_papers.py --match-10c "psi_I, U_S, gamma_negative"
python scripts/theory_papers.py --category CAT-29

# Schritt 3: Case Registry durchsuchen
# grep für relevante Cases
```

**Output:** Liste mit Paper-IDs + Relevanz-Score

### 1.2 Externe Suche (wenn intern nicht ausreichend)

```
# WebSearch für jede Query aus dem Protokoll
# Google Scholar / SSRN / NBER
# Bei SYSTEMATIC: Scopus, WoS, EconLit
```

### 1.3 Snowballing (vorwärts + rückwärts)

```
Backward Snowballing: Referenzen der gefundenen Papers durchgehen
Forward Snowballing: Wer zitiert die gefundenen Papers?
```

### 1.4 Suchergebnisse dokumentieren

```yaml
search_results:
  total_identified: 87  # N₀
  by_source:
    bcm_master_bib: 34
    theory_catalog: 8
    case_registry: 5
    google_scholar: 25
    ssrn: 10
    snowballing: 5
  duplicates_removed: 12
  unique_candidates: 75  # N₀ - Duplikate
```

**PRISMA-Flussdiagramm (vereinfacht):**

```
┌─────────────────────────────────────────────┐
│  IDENTIFIKATION                             │
│  Interne Suche: 47                          │
│  Externe Suche: 40                          │
│  Total: 87 (N₀)                              │
└────────────────────┬────────────────────────┘
                     │ -12 Duplikate
                     ▼
┌─────────────────────────────────────────────┐
│  SCREENING (Phase 2)                        │
│  Titel/Abstract: 75                         │
└────────────────────┬────────────────────────┘
                     │ -45 exkludiert
                     ▼
┌─────────────────────────────────────────────┐
│  ELIGIBILITY                                │
│  Volltext-Prüfung: 30                       │
└────────────────────┬────────────────────────┘
                     │ -8 exkludiert (mit Grund)
                     ▼
┌─────────────────────────────────────────────┐
│  INKLUDIERT (Phase 3-4)                     │
│  In Synthese: 22 (N₁)                       │
└─────────────────────────────────────────────┘
```

**Qualitäts-Gate Phase 1:**
```
☐ ≥3 Quellen systematisch durchsucht?
☐ Interne Quellen VOR externen durchsucht?
☐ Alle Suchergebnisse dokumentiert (N₀)?
☐ Duplikate identifiziert und entfernt?
☐ Snowballing durchgeführt (min. auf Top-10 Papers)?
```

---

## PHASE 2: Screening & Bewertung

> **Ziel:** Aus N₀ Kandidaten die N₁ relevanten Papers identifizieren.
> **Qualitäts-Gate:** Jede Exklusion muss begründet sein.

### 2.1 Titel/Abstract-Screening

Jedes Paper wird gegen die Inklusions-/Exklusionskriterien geprüft:

```yaml
screening:
  - paper_id: "PAP-frey1997costofprice"
    title_relevant: true
    abstract_relevant: true
    decision: "INCLUDE"
    reason: "Core NIMBY study, Swiss context, empirical"

  - paper_id: "PAP-smith2020generic"
    title_relevant: true
    abstract_relevant: false
    decision: "EXCLUDE"
    reason: "EX-3: Keine klare Identifikationsstrategie"
```

### 2.2 Volltext-Prüfung (bei STANDARD/SYSTEMATIC)

Für inkludierte Papers nach Titel/Abstract:
- Volltext lesen (wenn verfügbar in data/paper-texts/)
- Methodik prüfen (Evidence Tier zuweisen)
- Relevanz für Forschungsfrage(n) bewerten

### 2.3 Qualitätsbewertung (Evidence Tier)

| Tier | Kriterien | Beispiele |
|------|-----------|-----------|
| **1 (Gold)** | RCT/IV/DiD, Top-Journal, repliziert | AER, QJE, Econometrica, JEEA |
| **2 (Silver)** | Peer-reviewed, solide Methodik | EJPE, JEBO, JPubE, NBER WP |
| **3 (Bronze)** | Working Paper, theoretisch, schwache ID | SSRN, Preprints, Umfragen |

### 2.4 Exklusions-Log

**PFLICHT:** Jedes exkludierte Paper muss eine Begründung haben.

```yaml
exclusions:
  - paper: "Author (Year)"
    reason: "EX-1: Rein theoretisch, keine empirischen Daten"
  - paper: "Author (Year)"
    reason: "EX-4: Keine Identifikationsstrategie (OLS ohne IV)"
  - paper: "EX-5: Kontext nicht demokratisch (China)"
```

**Qualitäts-Gate Phase 2:**
```
☐ Jedes Paper gegen Kriterien geprüft?
☐ Jede Exklusion dokumentiert und begründet?
☐ Evidence Tier für inkludierte Papers zugewiesen?
☐ N₁ (finale Anzahl) dokumentiert?
☐ Bei SYSTEMATIC: Zweite Person hat Screening validiert?
```

---

## PHASE 3: Kodierung & Datenextraktion

> **Ziel:** Strukturierte Daten aus jedem inkludierten Paper extrahieren.
> **Qualitäts-Gate:** Einheitliches Kodebuch. Alle Papers vollständig kodiert.

### 3.1 Kodebuch definieren

Das Kodebuch hängt von der Forschungsfrage ab. Standard-Dimensionen:

**Bibliographische Daten (automatisch aus bcm_master.bib):**

| Feld | Quelle |
|------|--------|
| Autor:innen, Jahr, Journal | BibTeX |
| Evidence Tier | BibTeX (evidence_tier) |
| 10C-Dimensionen | Paper-YAML |
| Theory Support | BibTeX (theory_support) |

**Inhaltliche Kodierung (manuell):**

| Dimension | Code | Beschreibung | Skala/Werte |
|-----------|------|--------------|-------------|
| **Effektrichtung** | DIR | Haupteffekt positiv/negativ/null? | +1 / 0 / -1 |
| **Effektstärke** | ES | Quantifizierter Effekt | Numerisch (z.B. -0.51, +14pp) |
| **Mechanismus** | MEC | Durch welchen Kanal? | Crowding-Out / Status Quo / Framing / ... |
| **Moderatoren** | MOD | Was verstärkt/schwächt den Effekt? | Ψ-Dimensionen |
| **Kontext** | CTX | In welchem Setting? | Land, Branche, Zeitraum |
| **Identifikation** | ID | Kausale Identifikation? | RCT / IV / DiD / RDD / Korrelation |
| **EBF-Parameter** | PAR | Welche EBF-Parameter ableitbar? | PAR-xxx-xxx IDs |
| **Richtung (PRO/CONTRA)** | PC | Unterstützt/widerspricht Hypothese? | PRO / CONTRA / NEUTRAL |
| **Replikationsstatus** | REP | Wurde repliziert? | replicated / partial / failed / none |

### 3.2 Kodierungstabelle erstellen

```yaml
coding:
  - paper_id: "PAP-frey1997costofprice"
    direction: -1  # Compensation REDUCES acceptance
    effect_size: -0.51  # Acceptance halved
    mechanism: "motivation_crowding_out"
    moderators: ["Ψ_S: community_size", "Ψ_K: civic_duty_culture"]
    context: "Switzerland, nuclear waste siting, 1993"
    identification: "survey_experiment"
    ebf_parameters: ["PAR-INF-001", "PAR-COMP-002"]
    pro_contra: "PRO"  # Supports: compensation can backfire
    replication: "conceptual_replications_in_other_domains"

  - paper_id: "PAP-duranton2011fundamentallaw"
    direction: 0  # Road building has NO net effect on congestion
    effect_size: 1.0  # Elasticity = 1.0 (proportional induced demand)
    mechanism: "induced_demand"
    moderators: ["population_density", "ÖV_alternative"]
    context: "USA, interstate highways, 1983-2003"
    identification: "IV_1947_highway_plan"
    ebf_parameters: ["PAR-INF-002"]
    pro_contra: "CONTRA"  # Against: road expansion solves congestion
    replication: "replicated_in_multiple_countries"
```

### 3.3 Abweichungsprotokoll

Bei schwierigen Kodierungsentscheidungen:

```yaml
coding_decisions:
  - paper_id: "PAP-xxx"
    dimension: "mechanism"
    ambiguity: "Paper mentions both crowding-out AND selection effect"
    decision: "Coded as crowding_out (primary mechanism per author)"
    confidence: 0.7
```

**Qualitäts-Gate Phase 3:**
```
☐ Kodebuch vor der Kodierung definiert?
☐ Alle N₁ Papers vollständig kodiert?
☐ Effektstärken extrahiert (wo verfügbar)?
☐ PRO/CONTRA für jedes Paper zugewiesen?
☐ Mechanismen identifiziert?
☐ EBF-Parameter-Referenzen zugewiesen?
☐ Abweichungsprotokoll für schwierige Entscheidungen?
```

---

## PHASE 4: Synthese

> **Ziel:** Aus kodierten Einzelbefunden eine Gesamtantwort ableiten.
> **Qualitäts-Gate:** PRO + CONTRA Evidenz. Konfidenz-Bewertung. Gap-Analyse.

### 4.1 Evidenz-Synthese-Tabelle (Kern-Deliverable)

```
┌───────────────────────────────────────────────────────────────────────┐
│  EVIDENZ-SYNTHESE: [Forschungsfrage]                                  │
├──────────┬──────────┬──────────┬───────────┬─────────┬───────────────┤
│ Befund   │ Richtung │ Stärke   │ Tier 1    │ Tier 2  │ Konfidenz     │
├──────────┼──────────┼──────────┼───────────┼─────────┼───────────────┤
│ Kompensa-│ NEGATIV  │ γ=-0.51  │ 1 (AER)   │ 3       │ HOCH          │
│ tion → ↓ │          │          │           │         │ (repliziert)  │
│ Akzeptanz│          │          │           │         │               │
├──────────┼──────────┼──────────┼───────────┼─────────┼───────────────┤
│ Induced  │ NULL     │ ε=1.0    │ 1 (AER)   │ 2       │ HOCH          │
│ Demand   │ (kein    │          │           │         │ (IV-basiert)  │
│          │ Effekt)  │          │           │         │               │
├──────────┼──────────┼──────────┼───────────┼─────────┼───────────────┤
│ Status   │ NEGATIV  │ -5.6pp   │ 1 (EJPE)  │ 1       │ MITTEL        │
│ Quo Bias │ (gegen   │          │           │         │ (CH-spezif.)  │
│          │ Ausbau)  │          │           │         │               │
├──────────┼──────────┼──────────┼───────────┼─────────┼───────────────┤
│ Framing  │ POSITIV  │ +14pp    │ 0         │ 0       │ NIEDRIG       │
│ Effekt   │ (Sicher- │          │           │         │ (LLMMC Prior, │
│ (Sicherung│ung > Aus│         │           │         │ keine Studie) │
│ vs Ausbau)│ bau)    │          │           │         │               │
└──────────┴──────────┴──────────┴───────────┴─────────┴───────────────┘
```

### 4.2 Narrativ-Synthese (Textform)

Struktur:
1. **Konsens:** Was ist unbestritten?
2. **Kontroverse:** Wo widersprechen sich Befunde?
3. **Kontext-Abhängigkeit:** Wann gilt was? (Ψ-Dimensionen)
4. **Mechanismen:** Warum funktioniert es so?
5. **Moderatoren:** Was verstärkt/schwächt den Effekt?

### 4.3 PRO/CONTRA Bilanz (PFLICHT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PRO/CONTRA BILANZ: "Kompensation erhöht Infrastruktur-Akzeptanz"      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ PRO (Kompensation wirkt positiv):                                   │
│  ├── [3 Papers] Höhere Beträge → höhere Akzeptanz (in Laborkontexten) │
│  ├── [2 Papers] Community Benefit Agreements funktionieren              │
│  └── [1 Paper] In-kind Kompensation wirkt (Brunner 2025)               │
│                                                                         │
│  ❌ CONTRA (Kompensation wirkt negativ oder null):                      │
│  ├── [1 Paper, Tier 1] Crowding-Out halbiert Akzeptanz (Frey 1997)    │
│  ├── [2 Papers] Self-Signaling: Geld = negatives Identitätssignal     │
│  └── [1 Paper] Höhere Beträge signalisieren höhere Gefahr              │
│                                                                         │
│  ⚖️ GEWICHTETE BILANZ:                                                  │
│  → CONTRA überwiegt QUALITATIV (stärkere Identifikation, repliziert)  │
│  → PRO hat Volumen (mehr Papers), aber schwächere Methodik             │
│  → KONTEXT ENTSCHEIDET: Ψ_K (Kultur), Ψ_S (Gemeinschaft), Ψ_I (Prozess)│
│                                                                         │
│  📊 KONFIDENZ: MITTEL-HOCH                                              │
│  → Mechanismus klar (Crowding-Out), aber Moderatoren untererforscht    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.4 Gap-Analyse

```yaml
gaps:
  empirical:
    - "Keine RCT zu In-kind vs. monetärer Kompensation in CH"
    - "Fehlende Langzeitstudien: Was passiert 10 Jahre nach Siting-Entscheidung?"
    - "Kein Experiment zu Framing (Sicherung vs. Ausbau) isoliert"

  theoretical:
    - "Wie interagiert Crowding-Out mit Status Quo Bias?"
    - "Identity Economics × NIMBY: formales Modell fehlt"

  contextual:
    - "Fast alle Studien westlich/demokratisch — keine DACH-Replikation von Duranton/Turner"
    - "Digitale Infrastruktur (5G, Glasfaser) unterrepräsentiert"

  methodological:
    - "Endogenitätsproblem: Kompensation wird meist dort angeboten wo Opposition hoch"
    - "Fehlende Meta-Analyse über NIMBY-Studien hinweg"
```

### 4.5 EBF-Parameter-Aggregation

```yaml
parameter_synthesis:
  - parameter: "PAR-INF-001 (γ_crowd)"
    papers: 4
    range: [-0.68, -0.35]
    weighted_mean: -0.51
    confidence: "HIGH"
    note: "Konsistent über Studien. Swiss-specific estimate robust."

  - parameter: "PAR-INF-005 (Δ_frame)"
    papers: 0  # Kein Paper direkt, nur abgeleitet
    range: [8, 20]
    weighted_mean: 14
    confidence: "LOW — LLMMC Prior, needs empirical validation"
    gap: "CRITICAL: No direct experimental estimate of framing effect"
```

**Qualitäts-Gate Phase 4:**
```
☐ Evidenz-Synthese-Tabelle erstellt?
☐ PRO + CONTRA Evidenz BEIDE dokumentiert?
☐ CONTRA aktiv gesucht (nicht nur PRO)?
☐ Konfidenz für jeden Befund bewertet?
☐ Gap-Analyse durchgeführt?
☐ EBF-Parameter-Aggregation (wo möglich)?
☐ Mechanismen UND Moderatoren identifiziert?
```

---

## PHASE 5: Report erstellen

> **Ziel:** Professioneller, zitierbarer Output.
> **Qualitäts-Gate:** 8D-konform. Alle Quellen verlinkt.

### 5.1 Report-Struktur (Standard)

```
1. Executive Summary (1 Seite)
   - Forschungsfrage
   - Methodik (N₀ → N₁)
   - Schlüsselbefunde (3-5 Bullet Points)
   - Konfidenz-Bewertung

2. Einleitung & Forschungsfrage
   - PICO/SPIDER
   - Warum relevant? (EBF-Kontext)

3. Methodik
   - Suchstrategie (Quellen, Queries)
   - Inklusion-/Exklusionskriterien
   - PRISMA-Flussdiagramm (bei STANDARD/SYSTEMATIC)
   - Kodebuch

4. Ergebnisse
   - Deskriptive Statistik (N₁ Papers nach Tier, Jahr, Methodik)
   - Evidenz-Synthese-Tabelle
   - Narrativ-Synthese nach Themen/Mechanismen

5. PRO/CONTRA Bilanz
   - Gewichtete Evidenz
   - Konfidenz-Bewertung pro Befund

6. Gap-Analyse
   - Empirische Lücken
   - Theoretische Lücken
   - Methodische Lücken

7. EBF-Integration
   - Neue/aktualisierte Parameter
   - Neue Cases
   - Neue Theorien
   - Cross-References zu Appendices/Chapters

8. Schlussfolgerungen & Empfehlungen
   - Antwort auf Forschungsfrage(n)
   - Implikationen für Praxis
   - Forschungsbedarf

Anhang A: Vollständige Kodierungstabelle
Anhang B: Exklusions-Log
Anhang C: Bibliographie (alle inkludierten Papers)
```

### 5.2 Output-Format (via 8D)

Die 8D-Koordinaten für eine Literaturanalyse:

| D | Dimension | Typischer Wert | Begründung |
|---|-----------|----------------|------------|
| D₁ | Wissen | 0.8 | Fachpublikum |
| D₂ | Nähe | 0.7 | EBF-Feld |
| D₃ | Reichweite | 0.5 | Projekt-spezifisch |
| D₄ | Zeit | 0.6 | Detailliert aber fokussiert |
| D₅ | Ziel | G₁ (Informieren) | Wissens-Synthese |
| D₆ | Kontext | 0.7 | Projekt-intern aber teilbar |
| D₇ | Emotion | 0.1 | Sachlich |
| D₈ | Persistenz | 0.8 | Archivwürdig |

→ **Regel O-1:** D₈ > 0.6 → LaTeX/PDF
→ **Regel O-4:** D₄ = 0.6 → 10-pager

### 5.3 Speicherort

```
outputs/literature-analyses/SLA-{ID}/
├── SLA-{ID}_report_v1.md          # Report (Markdown)
├── SLA-{ID}_report_v1.tex         # Report (LaTeX, falls O-1)
├── SLA-{ID}_report_v1.pdf         # Report (PDF, falls O-2)
├── SLA-{ID}_evidence_table.yaml   # Kodierungstabelle
├── SLA-{ID}_prisma.md             # PRISMA-Diagramm
└── SLA-{ID}_protocol.yaml         # Suchprotokoll (Phase 0)
```

**Qualitäts-Gate Phase 5:**
```
☐ Executive Summary vorhanden?
☐ Methodik transparent dokumentiert?
☐ PRISMA-Diagramm (bei STANDARD/SYSTEMATIC)?
☐ Evidenz-Tabelle im Anhang?
☐ Exklusions-Log im Anhang?
☐ Alle Quellen korrekt zitiert (BibTeX-Keys)?
☐ 8D-Format korrekt?
☐ Report in output-registry.yaml registriert?
```

---

## PHASE 6: EBF-Integration

> **Ziel:** Alle relevanten Ergebnisse ins EBF überführen.
> **Qualitäts-Gate:** Jedes neue Paper via /integrate-paper. Jeder neue Parameter dokumentiert.

### 6.1 Neue Papers integrieren

Für jedes Paper das noch NICHT in bcm_master.bib ist:

```bash
# Via /integrate-paper (AUTO-TRIGGER)
/integrate-paper --doi <DOI>  # oder interaktiv
```

### 6.2 Neue/aktualisierte Parameter

```bash
# Via Parameter-Registry aktualisieren
# Format: PAR-{PREFIX}-{NNN}
# PFLICHT: Quellenverweis, Measurement Context, CI
```

### 6.3 Neue Cases

```bash
# Via /case-manage add
/case-manage add  # interaktiv
```

### 6.4 Neue Theorien

Wenn die Synthese eine neue Theorie/ein neues Muster identifiziert:
→ EIP-Workflow (Evidence Integration Pipeline) starten

### 6.5 Cross-References aktualisieren

- BCM2-Kontextdaten ergänzen (wenn neue Faktoren)
- Chapter-Appendix-Mapping prüfen
- Theory-Paper Bidirektionalität sicherstellen

**Qualitäts-Gate Phase 6:**
```
☐ Alle neuen Papers via /integrate-paper integriert?
☐ Neue Parameter in parameter-registry.yaml?
☐ Neue Cases in case-registry.yaml?
☐ Neue Theorien via EIP geprüft?
☐ BCM2-Kontextdaten aktualisiert?
☐ Cross-References bidirektional?
☐ Git commit + push?
```

---

## Vollständige Checkliste (alle Phasen)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SLA VOLLSTÄNDIGE CHECKLISTE                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 0: PROTOKOLL                                                     │
│  ☐ Forschungsfrage SMART (PICO/SPIDER)                                 │
│  ☐ Inklusion-/Exklusionskriterien VOR Suche                            │
│  ☐ Suchstrategie mit ≥3 Quellen                                        │
│  ☐ Protokoll-YAML gespeichert                                          │
│                                                                         │
│  PHASE 1: SUCHE                                                         │
│  ☐ Interne Quellen ZUERST (bcm_master.bib, theory-catalog)             │
│  ☐ Externe Quellen (WebSearch, Scholar)                                 │
│  ☐ Snowballing (vorwärts + rückwärts)                                   │
│  ☐ N₀ dokumentiert, Duplikate entfernt                                  │
│                                                                         │
│  PHASE 2: SCREENING                                                     │
│  ☐ Titel/Abstract-Screening gegen Kriterien                            │
│  ☐ Volltext-Prüfung (bei STANDARD/SYSTEMATIC)                          │
│  ☐ Evidence Tier zugewiesen                                             │
│  ☐ Jede Exklusion begründet im Log                                     │
│  ☐ N₁ dokumentiert                                                      │
│                                                                         │
│  PHASE 3: KODIERUNG                                                     │
│  ☐ Kodebuch VOR Kodierung definiert                                    │
│  ☐ Alle N₁ Papers kodiert                                               │
│  ☐ Effektstärken extrahiert                                             │
│  ☐ PRO/CONTRA zugewiesen                                               │
│  ☐ Mechanismen + Moderatoren identifiziert                             │
│  ☐ EBF-Parameter-Referenzen zugewiesen                                 │
│                                                                         │
│  PHASE 4: SYNTHESE                                                      │
│  ☐ Evidenz-Synthese-Tabelle                                            │
│  ☐ PRO/CONTRA Bilanz                                                   │
│  ☐ Konfidenz-Bewertung                                                 │
│  ☐ Gap-Analyse (empirisch, theoretisch, methodisch)                    │
│  ☐ Parameter-Aggregation                                               │
│                                                                         │
│  PHASE 5: REPORT                                                        │
│  ☐ Executive Summary                                                    │
│  ☐ Methodik transparent                                                │
│  ☐ PRISMA-Diagramm                                                     │
│  ☐ Evidenz-Tabelle + Exklusions-Log                                    │
│  ☐ 8D-Format korrekt                                                   │
│  ☐ In output-registry.yaml registriert                                 │
│                                                                         │
│  PHASE 6: INTEGRATION                                                   │
│  ☐ Neue Papers via /integrate-paper                                    │
│  ☐ Neue Parameter in Registry                                          │
│  ☐ Neue Cases in Registry                                              │
│  ☐ EIP für neue Konzepte                                               │
│  ☐ Cross-References aktualisiert                                       │
│  ☐ Git commit + push                                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns (VERBOTEN)

| Anti-Pattern | Warum schlecht | Stattdessen |
|--------------|---------------|-------------|
| ❌ «Hier sind 10 relevante Papers» ohne Methodik | Nicht reproduzierbar, Bias | Suchprotokoll + PRISMA |
| ❌ Nur PRO-Evidenz sammeln | Confirmation Bias | PRO + CONTRA PFLICHT |
| ❌ Exklusion ohne Begründung | Undurchsichtig | Exklusions-Log führen |
| ❌ Google-Suche als einzige Quelle | Nicht systematisch | ≥3 Quellen, intern zuerst |
| ❌ Effektstärken ignorieren | Narrative vs. quantitativ | Effektstärken + CI extrahieren |
| ❌ Tier 3 Papers = Tier 1 Papers | Qualität nicht gleich | Evidence Tier immer angeben |
| ❌ Kodierung improvisieren | Inkonsistent | Kodebuch VOR Kodierung definieren |
| ❌ Gap-Analyse weglassen | Verpasste Chancen | IMMER Gaps identifizieren |
| ❌ Papers finden, nicht integrieren | Verlust für EBF | Phase 6 PFLICHT |

---

## Referenzen

### Interne Referenzen (EBF)

| Dokument | Pfad | Relevanz |
|----------|------|----------|
| Paper Workflow Overview | `docs/workflows/paper-workflow-overview.md` | Kontext |
| Evidence Integration Pipeline | `docs/workflows/evidence-integration-pipeline.md` | Phase 6 |
| Level 5 Integration | `docs/workflows/level5-paper-integration-workflow.md` | Phase 6 |
| 8D-Algorithmus | Appendix CCC/DDD | Phase 5 (Report) |
| Quellen-Hierarchie | CLAUDE.md | Phase 1 (Suche) |

### Methodische Referenzen (extern)

| Standard | Beschreibung | Anwendung |
|----------|--------------|-----------|
| PRISMA 2020 | Preferred Reporting Items for Systematic Reviews | Phase 1-2, Report |
| Cochrane Handbook | Systematic Review Methodik | Phase 3-4 (Kodierung, Synthese) |
| Campbell Collaboration | Sozialwissenschaftliche Systematic Reviews | Gesamter Workflow |
| PROSPERO | Pre-Registration für Systematic Reviews | Phase 0 (SYSTEMATIC Modus) |
