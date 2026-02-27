# Evidence-Based Framework for Economic and Social Behavior (EBF)

## Comprehensive Framework Report

**FehrAdvice & Partners AG | Prof. Ernst Fehr**

*Version 1.0 — Februar 2026*

---

## Executive Summary

Das **Evidence-Based Framework for Economic and Social Behavior (EBF)** ist ein integratives wissenschaftliches Framework, das über 50 Jahre verhaltensökonomische Forschung in ein einheitliches, berechenbares System überführt. Es verbindet die Arbeiten von Kahneman & Tversky (Prospect Theory), Thaler (Nudging), Fehr (Soziale Präferenzen) und Sunstein (Choice Architecture) zu einem kohärenten Ganzen.

**Das EBF ist kein Chatbot.** Es ist ein evidenzbasiertes Analysesystem, das zeigt, *warum* Menschen handeln — und wie man dieses Verhalten systematisch und ethisch beeinflussen kann.

### Kerninnovation

Die zentrale Erkenntnis des EBF lautet:

> **Dieselbe Frage + anderer Kontext = komplett andere Antwort.**

Traditionelle Verhaltensökonomie behandelt Parameter wie Loss Aversion (λ = 2.25) als universelle Konstanten. Das EBF zeigt: Diese Parameter sind *Funktionen des Kontexts*. Loss Aversion im Wohlfahrtskontext mit Stigma beträgt λ ≈ 2.5, am Arbeitsplatz mit Kolleg:innen nur λ ≈ 1.8. **Die Variation ist nicht Noise — sie ist das Signal.**

### Zahlen auf einen Blick

| Ressource | Umfang |
|-----------|--------|
| Wissenschaftliche Papers | 2'472 (kuratiert, indexiert) |
| Verhaltensökonomische Theorien | 212 in 27 Kategorien |
| Praxisfälle (Case Registry) | 936 dokumentierte Fälle |
| Verhaltensparameter | 140+ mit Konfidenzintervallen |
| Validierte Modelle | 24 (10C-spezifiziert) |
| Kontext-Faktoren (BCM2) | 404+ für CH/AT/DE |
| Kundenprofile | 69 Unternehmensprofile |
| Python-Automatisierung | 297 Skripte |
| LaTeX-Appendices | 244 in 8 Kategorien |

---

## 1. Einleitung: Warum EBF?

### 1.1 Das Problem

Verhaltensökonomische Erkenntnisse sind heute weit verbreitet. Doch ihre Anwendung scheitert häufig an drei fundamentalen Problemen:

1. **Kontextblindheit:** Erkenntnisse aus dem Labor werden 1:1 auf die Praxis übertragen — ohne Berücksichtigung des Kontexts.
2. **Fragmentierung:** 50+ Jahre Forschung existieren als isolierte Theorien ohne systematische Verbindung.
3. **Halluzinationsgefahr:** KI-Systeme «erinnern» sich an Parameterwerte aus ihrem Training, statt sie zu berechnen.

### 1.2 Die Lösung

Das EBF adressiert alle drei Probleme:

- **Kontext-First-Methodik:** Jeder Parameter wird als Funktion des Kontexts behandelt (θ = f(Ψ, 10C)).
- **Integratives Framework:** 212 Theorien, 2'472 Papers und 936 Cases in einer kohärenten Architektur.
- **Three-Layer Architecture:** Deterministische Berechnung (Layer 1) statt LLM-Halluzination (Layer 3).

### 1.3 Wer steht dahinter?

Das EBF wurde von **FehrAdvice & Partners AG** in Zusammenarbeit mit dem wissenschaftlichen Team um **Prof. Ernst Fehr** (Universität Zürich) entwickelt. Es baut auf der Grundlagenforschung der führenden Verhaltensökonomen auf und erweitert diese um eine systematische Kontext- und Komplementaritätstheorie.

---

## 2. Das 10C CORE Framework

### 2.1 Überblick

Das Herzstück des EBF ist das **10C CORE Framework** — zehn interdependente Dimensionen, die menschliches Verhalten vollständig beschreiben:

| Nr. | Code | CORE | Leitfrage | Output |
|-----|------|------|-----------|--------|
| 1 | AAA | **WHO** | Wer hat Utility? | Welfare-Levels L (Individual → Gesellschaft) |
| 2 | C | **WHAT** | Was ist Utility? | FEPSDE-Dimensionen (Financial, Emotional, Physical, Social, Development, Ecological) |
| 3 | B | **HOW** | Wie interagieren die Dimensionen? | Komplementarität γ |
| 4 | V | **WHEN** | Wann zählt Kontext? | 8 Ψ-Dimensionen |
| 5 | BBB | **WHERE** | Woher kommen die Zahlen? | Parameter Θ aus Literatur/Empirie |
| 6 | AU | **AWARE** | Wie bewusst ist die Person? | Awareness A(·) ∈ [0,1] |
| 7 | AV | **READY** | Ist die Person handlungsbereit? | Willingness W\_AX ≥ θ |
| 8 | AW | **STAGE** | Wo in der Verhaltensreise? | Behavior Change Journey φ(t) |
| 9 | HI | **HIERARCHY** | Wie stratifizieren Entscheidungen? | Decision Levels L0–L3 |
| 10 | IE | **EIT** | Wie emergieren Interventionen? | Interventionsvektor I⃗ ∈ [0,1]⁹ |

### 2.2 FEPSDE: Die sechs Utility-Dimensionen

Menschliches Wohlbefinden (Utility) ist nicht eindimensional. Das EBF unterscheidet sechs fundamentale Dimensionen:

- **F — Financial:** Monetäre Anreize, Einkommen, Kosten
- **E — Emotional:** Gefühle, Zufriedenheit, Stress
- **P — Physical:** Körperliche Gesundheit, Anstrengung, Komfort
- **S — Social:** Soziale Anerkennung, Normen, Zugehörigkeit
- **D — Development:** Persönliche Entwicklung, Lernen, Kompetenz
- **E — Ecological:** Umwelt, Nachhaltigkeit, Generationengerechtigkeit

### 2.3 Komplementarität: Warum 1 + 1 ≠ 2

Das EBF modelliert explizit, wie Dimensionen *interagieren*. Diese Interaktionen (γ-Koeffizienten) sind empirisch fundiert:

| Interaktion | γ-Wert | Bedeutung | Quelle |
|-------------|--------|-----------|--------|
| Social × Financial | −0.68 | **Crowding-Out:** Finanzielle Anreize untergraben soziale Motivation | PAR-COMP-002 |
| Identity × Social | +0.35 | **Verstärkung:** Identität und soziale Normen verstärken sich | PAR-COMP-001 |
| Social × Warm Glow | +0.28 | **Synergie:** Soziale Anerkennung und intrinsische Motivation | PAR-COMP-004 |

**Praxisrelevanz:** Wer finanzielle Anreize mit sozialen Normen kombiniert, riskiert Crowding-Out (γ = −0.68). Das EBF warnt systematisch vor solchen Konflikten.

### 2.4 Die 8 Ψ-Dimensionen (Kontext)

Jede Situation wird durch acht Kontext-Dimensionen beschrieben:

| Symbol | Dimension | Frage | Beispiel |
|--------|-----------|-------|----------|
| Ψ\_I | Institutionell | Welche Regeln gelten? | Opt-in vs. Opt-out |
| Ψ\_S | Sozial | Wer ist dabei? | Allein vs. beobachtet |
| Ψ\_C | Kognitiv | In welchem Zustand? | Ausgeruht vs. erschöpft |
| Ψ\_K | Kulturell | Welche Werte? | CH vs. DE vs. TR |
| Ψ\_E | Ökonomisch | Welche Ressourcen? | Reich vs. knapp |
| Ψ\_T | Temporal | Wann? Zeitdruck? | Montag früh vs. Freitag spät |
| Ψ\_M | Materiell | Welche Tools? | Papier vs. App |
| Ψ\_F | Physisch | Wo? | Zuhause vs. Amt |

---

## 3. Die zentrale Gleichung: Parameter Context Transformation (PCT)

### 3.1 Das Paradigma

Das EBF überwindet die traditionelle Annahme fester Parameter:

| Aspekt | Traditionell | EBF |
|--------|-------------|-----|
| Parameter | Konstante (λ = 2.25) | Funktion θ(Ψ, 10C) |
| Variation | Noise, Methodenfehler | Signal, erklärbar durch Kontext |
| Transfer | Meta-Analyse (Mittelwert) | Systematische Transformation |

### 3.2 Die PCT-Gleichung

```
θ_B = θ_A × ∏ᵢ M(ΔΨᵢ) × ∏ⱼ N(Δ10Cⱼ)
```

Dabei gilt:

- **θ\_A** = Parameter im Anchor-Kontext (aus der Originalstudie)
- **θ\_B** = Parameter im Target-Kontext (Vorhersage für neues Projekt)
- **ΔΨᵢ** = Kontext-Differenz zwischen Anchor und Target
- **M(·)** = Ψ-Multiplikator (aus validierten Tabellen)
- **N(·)** = 10C-Multiplikator

### 3.3 Praktisches Beispiel

**Frage:** Wie hoch ist die Loss Aversion (λ) für ein Heizungsersatz-Programm in der Schweiz?

**Schritt 1 — Anchor laden:**
λ\_A = 2.5 (gemessen in US-Wohlfahrtsprogramm mit Stigma)

**Schritt 2 — Kontext-Differenzen berechnen:**

| Dimension | Anchor (USA, Welfare) | Target (CH, Heizung) | Multiplikator |
|-----------|----------------------|---------------------|---------------|
| Ψ\_S (Sozial) | Stigma hoch | Stigma niedrig | M = 0.85 |
| Ψ\_K (Kultur) | USA | Schweiz | M = 0.92 |
| Ψ\_I (Institutionell) | Freiwillig | Subventioniert | M = 1.10 |

**Schritt 3 — Transformieren:**
λ\_B = 2.5 × 0.85 × 0.92 × 1.10 = **2.16**

**Schritt 4 — Interpretieren:**
Im Schweizer Heizungsersatz-Kontext ist die Loss Aversion mit λ = 2.16 moderat. Empfehlung: Moderate Defaults mit klarer Kommunikation des Status quo.

---

## 4. Three-Layer Architecture

### 4.1 Das Problem: «Compute, Don't Hallucinate»

Large Language Models (LLMs) haben ein fundamentales Problem: Sie «erinnern» sich an Werte aus ihrem Training, statt sie zu berechnen. Ein LLM könnte behaupten, λ = 2.25 — auch wenn der korrekte Wert im aktuellen Kontext λ = 4.58 beträgt.

Das EBF löst dieses Problem durch eine **Three-Layer Architecture (TLA)**, die am 15. Februar 2026 mit 32 PRO-Papers aus 7 Disziplinen validiert wurde.

### 4.2 Die drei Schichten

```
┌─────────────────────────────────────────────────────┐
│  LAYER 3: LLM-Übersetzung                           │
│  Anfälligkeit: 0.8 (hoch)                           │
│  Funktion: Formale Ergebnisse in Sprache übersetzen │
│  ERLAUBT: Erklären, interpretieren, kommunizieren   │
│  VERBOTEN: Werte erinnern, berechnen, generieren    │
├─────────────────────────────────────────────────────┤
│  LAYER 2: Parameter-Store (YAML)                    │
│  Anfälligkeit: 0.3 (validierbar)                    │
│  Funktion: Werte mit Schema, Quellen, Bereichen     │
│  140+ Parameter, 404+ Kontext-Faktoren              │
├─────────────────────────────────────────────────────┤
│  LAYER 1: Formale Berechnung (Python)               │
│  Anfälligkeit: 0.0 (immun)                          │
│  Funktion: EBF-Gleichungen deterministisch berechnen│
│  PCT, LLMMC, ODE-Simulation, R-Score                │
└─────────────────────────────────────────────────────┘
```

### 4.3 Die vier Grundprinzipien

1. **Compute, Don't Hallucinate** — Jede EBF-Zahl stammt aus formaler Berechnung (Layer 1), nicht aus LLM-Erinnerung.
2. **Parameters from Registry, Not from Memory** — Werte werden aus YAML gelesen (Layer 2), nicht erinnert.
3. **Translate, Don't Generate** — Das LLM erklärt berechnete Ergebnisse, es erfindet keine.
4. **Formal Layer is the Immune System** — Determinismus ist die virenfreie Zone.

### 4.4 Immune Gateway: Autonomes Immunsystem

Ein zentrales Problem wurde im Februar 2026 gelöst: Bisher entschied das LLM (Anfälligkeit 0.8) *selbst*, ob es Layer 1 aufruft. Das ist so, als würde der Wirt entscheiden, ob der Virus leben darf.

Die **Immune Gateway** löst dies: Layer 1 läuft *automatisch* via Hook, *bevor* das LLM antwortet. Das LLM entscheidet nicht mehr — die formale Berechnung geschieht autonom.

```
User-Prompt → Hook → immune_gateway.py (Keyword-Erkennung)
                         ├── Match?  → orchestrator.py (Layer 1)
                         │               → Ergebnis im LLM-Kontext
                         └── No match → still (kein Output)
```

### 4.5 Wissenschaftliche Validierung

Die TLA wurde durch eine Evidence Integration Pipeline (EIP) mit folgenden Ergebnissen validiert:

| Evidenz | Quelle | Erkenntnis |
|---------|--------|------------|
| PAL (Gao et al., ICML 2023) | +40% Genauigkeit durch Python-Delegation | Layer 1 verbessert Ergebnisse massiv |
| Model Collapse (Shumailov et al., Nature 2024) | Rekursive KI-Inhalte degradieren Modelle | Layer 3 allein ist unzureichend |
| RAG (Lewis et al., NeurIPS 2020) | +35% Faktentreue durch Retrieval | Layer 2 als Wissensbasis validiert |
| Constitutional AI (Bai et al., 2022) | Formale Constraints nötig | Prinzipienbasierte Kontrolle bestätigt |

---

## 5. Methodologie

### 5.1 BBB: Die 4-Tier Parameter-Hierarchie

Jeder Parameter im EBF hat eine klar definierte Herkunft:

| Tier | Quelle | Unsicherheit | Priorität |
|------|--------|-------------|-----------|
| 1 | Literatur (Meta-Analyse) | Niedrig | **Höchste** |
| 2 | LLMMC Prior | Mittel | Fallback |
| 3 | Empirische Kalibrierung | Variabel | Bei Primärdaten |
| 4 | Expert:innen-Befragung | Hoch | Letzte Option |

**Literatur-Werte haben immer Vorrang.** LLMMC ist Fallback, nicht Default.

### 5.2 LLMMC: LLM Monte Carlo Kalibrierung

Wenn keine Literaturwerte verfügbar sind, nutzt das EBF ein innovatives Verfahren: **LLM Monte Carlo (LLMMC)**. Dabei werden LLM-Schätzungen systematisch gegen bekannte Anker-Werte kalibriert.

**Vier-Komponenten-Framework:**

| Komponente | Funktion |
|-----------|----------|
| CAL-1 | Kalibrierungsanker definieren |
| CAL-2 | Level-Kalibrierung (Bias & Skalierung) |
| CAL-3 | Unsicherheits-Kalibrierung (Coverage) |
| CAL-4 | Evidenz-gewichtete Schrumpfung |

**Ergebnis:** Kalibrierte Parameterschätzungen mit 95%-Konfidenzintervallen.

### 5.3 ODE-Verhaltensdynamik-Simulator

Für die Simulation von Verhaltensänderungen über die Zeit bietet das EBF einen **6-Zustand ODE-Simulator**:

| Zustand | Symbol | Beschreibung |
|---------|--------|-------------|
| Utility | U(t) | Wahrgenommener Nutzen der Verhaltensänderung |
| Adoption | A(t) | Adoptionsrate (logistisch) |
| Resistance | R(t) | Widerstand gegen Veränderung |
| Habit | H(t) | Gewohnheitsbildung |
| Momentum | M(t) | Veränderungsdynamik |
| Decision Capacity | D(t) | Entscheidungsfähigkeit |

Das System wird durch Euler-Integration gelöst und berücksichtigt explizit Komplementaritäten zwischen den Dimensionen.

### 5.4 Exclusion Principle: Additiv ist Default

Ein häufiger Fehler in der Verhaltensökonomie ist die unreflektierte Multiplikation von Faktoren. Das EBF folgt dem **Exclusion Principle (EXC-1 bis EXC-6)**:

- **γ = 0** (additiv) ist der **Default** — keine Begründung nötig.
- **γ ≠ 0** (komplementär) erfordert eine **empirische Begründung** mit Verweis auf PAR-COMP-xxx.

Multiplikative Verknüpfung wird nur akzeptiert, wenn eine der 10 Whitelist-Bedingungen erfüllt ist (z.B. f = 0 → Y = 0, oder kausale Identifikation via RCT).

---

## 6. Evidenzbasis

### 6.1 Paper-Datenbank

Die EBF-Bibliothek umfasst **2'472 wissenschaftliche Papers**, systematisch klassifiziert nach:

**Content Level C(p):**

| Level | Beschreibung | Anzahl |
|-------|-------------|--------|
| L0 | Nur Metadaten | ~21 |
| L1 | Research Question bekannt | ~1'237 |
| L2 | Summary/Extract verfügbar | ~1'079 |
| L3 | Kompletter Originaltext | ~10 |

**Integration Level I(p):**

| Level | Beschreibung | Anzahl |
|-------|-------------|--------|
| I1 | use\_for zugewiesen | ~829 |
| I2 | + theory\_support | ~1'102 |
| I3 | + case\_registry | ~418 |
| I4 | Dedizierter Appendix | ~11 |
| I5 | Volle Framework-Integration | ~2 |

### 6.2 Theory Catalog

**212 Theorien in 27 Kategorien**, darunter:

| Kategorie | Beispiel-Theorien |
|-----------|-------------------|
| Prospect Theory & Reference Dependence | Kahneman-Tversky (1979), Köszegi-Rabin (2006) |
| Social Preferences | Fehr-Schmidt (1999), Bolton-Ockenfels (2000) |
| Time Preferences | Laibson (1997), O'Donoghue-Rabin (1999) |
| Identity & Beliefs | Akerlof-Kranton (2000), Bénabou-Tirole (2002) |
| Choice Architecture | Thaler-Sunstein (2008), Default Effects |
| Voting & Social Choice | QRE, Consensus Formation, PSF-2.0 |
| Crisis Management | Herhausen (2019), Firestorm-Dynamik |
| AI Consumer Experience | Puntoni et al. (2021) |

### 6.3 Case Registry

**936 dokumentierte Praxisfälle**, indexiert nach allen 10C-Dimensionen. Jeder Case enthält:

- 10C-Mapping (welche Dimensionen relevant)
- Verwendete Formeln und Parameter
- Ergebnisse und Learnings
- Referenzen zu wissenschaftlichen Papers

### 6.4 Parameter Registry

**140+ Verhaltensparameter** mit vollständiger Provenienz:

| Parameter | Symbol | Typischer Bereich | Quelle |
|-----------|--------|-------------------|--------|
| Loss Aversion | λ | 1.8–3.0 | Kahneman-Tversky 1979 |
| Present Bias | β | 0.7–0.9 | Laibson 1997 |
| Social Utility Weight | σ | 0.3–0.7 | Fehr-Schmidt 1999 |
| Default Effect | δ | 0.15–0.45 | Madrian-Shea 2001 |
| Inequity Aversion (α) | α | 0.5–2.0 | Fehr-Schmidt 1999 |

Jeder Parameter enthält: Konfidenzintervall, Tier-Zuordnung (1–4), Messkontext und Paper-Referenz.

---

## 7. Kontext-Architektur

### 7.1 Fünf-Ebenen Kontext-Hierarchie

Das EBF operationalisiert Kontext durch eine **strenge 5-Ebenen-Hierarchie**:

```
EBENE 1: MACRO   (Land/Markt)        → 404 Faktoren (CH/AT/DE)
    ↓
EBENE 2: MESO    (Branche/Kunde)     → Variabel (CVA-Profile)
    ↓
EBENE 3: MICRO   (Situation)         → 5 Dimensionen
    ↓
EBENE 4: INDIVIDUAL (Person)         → 48 Faktoren
    ↓
EBENE 5: META    (Entscheidung)      → 42 Faktoren
```

**Reihenfolge ist Pflicht:** Land → Branche → Situation → Person → Entscheidung → Parameter.

### 7.2 Context Vector Architecture (CVA)

Für Unternehmenskontexte bietet das EBF drei Detailstufen:

| Stufe | Faktoren | Dateien | Zeit | Anwendung |
|-------|----------|---------|------|-----------|
| **SCHNELL** | ~30 | 1 YAML | 2–4 Std. | Pitch, Screening |
| **STANDARD** | 400 | 8 YAMLs | 1–2 Tage | Vollprojekt, Strategie |
| **VERTIEFT** | 400+ | 8+ YAMLs | 1–2 Wochen | Langzeit-Mandat, M&A |

**Die 8 CVA-Kategorien (STANDARD):**

| Kategorie | Faktoren | Inhalt |
|-----------|----------|--------|
| FIN (Financial) | 80 | Umsatz, Marge, Investitionen |
| MKT (Market) | 60 | Wettbewerb, Marktposition, Trends |
| ORG (Governance) | 50 | Struktur, Kultur, Prozesse |
| PEO (People) | 80 | Mitarbeitende, Kompetenzen, Fluktuation |
| RIS (Risk) | 30 | Risikoprofil, Compliance, Reputation |
| STK (Stakeholder) | 20 | Eigentümer:innen, Regulator, Öffentlichkeit |
| STR (Strategy) | 40 | Vision, Ziele, Differenzierung |
| TEC (Technology) | 40 | Digitalisierung, Innovation, Infrastruktur |

### 7.3 BCM2: Die Kontext-Datenbank

Die BCM2-Datenbank enthält **404+ Kontext-Faktoren** für die DACH-Region:

| Kategorie | Faktoren | Beispiele |
|-----------|----------|----------|
| Demographisch | 60 | Bevölkerungsstruktur, Urbanisierung, Migration |
| Ökonomisch | 54 | BIP, Arbeitslosigkeit, Ungleichheit |
| Institutionell-Politisch | 59 | Direkte Demokratie, Föderalismus, Regulierung |
| Technologisch-Ökologisch | 65 | Digitalisierung, Energiewende, Klimawandel |
| Sozio-Kulturell | 166 | Vertrauen, Werte, Religion, Sprachen |

**Jeder Faktor enthält:** Aktuelle Werte, Quellen (BFS, ESS, WVS), Trends und API-Verbindungen.

---

## 8. Interventions-Design

### 8.1 Emergent Intervention Theory (EIT)

Das EBF behandelt Interventionen nicht als diskrete «Nudges», sondern als **9-dimensionale Vektoren** im kontinuierlichen Raum [0,1]⁹. Jede Intervention wird durch ihre Wirkung auf die 10C-Dimensionen 1–9 beschrieben.

### 8.2 Das 20-Field Schema

Jede Intervention wird durch 20 standardisierte Felder spezifiziert:

| Feld | Inhalt |
|------|--------|
| F1: Name | Bezeichnung der Intervention |
| F2: 10C-Target | Welche Dimension wird adressiert? |
| F3: Δ-Ziel | Was soll sich verändern? (z.B. A↑, γ→) |
| F4: Phase | In welcher Phase der Behavior Change Journey? |
| F5: Segment | Welche Zielgruppe? |
| F6: Mechanismus | Wie wirkt die Intervention? |
| F7–F10 | Komplementarität, Crowding-Out, Autonomie, Scope |
| F11–F15 | Implementierung, Timing, Kosten, Messung |
| F16–F20 | Risiken, Ethik, Skalierung, Learnings |

### 8.3 Komplementaritäts-Prüfung

**Bekannte Konflikte (Pflichtprüfung):**

- **Social + Financial** (γ = −0.2): Finanzielle Anreize können soziale Normen untergraben.
- **Financial + Commitment** (γ = −0.3): Externe Belohnungen können intrinsische Motivation zerstören.

Das EBF warnt automatisch, wenn solche Konflikte in einem Interventions-Portfolio auftreten.

### 8.4 Phase-Type Affinity

Nicht jede Intervention passt zu jeder Phase der Verhaltensreise:

| Phase | Empfohlene Interventionen | α-Wert |
|-------|--------------------------|--------|
| Awareness | Information, Salience | α > 0.7 |
| Willingness | Soziale Normen, Framing | α > 0.7 |
| Action | Defaults, Vereinfachung | α > 0.7 |
| Maintenance | Feedback, Gewohnheitsbildung | α > 0.7 |

Bei α < 0.5 ist die Intervention für diese Phase **nicht empfohlen**.

---

## 9. Technische Infrastruktur

### 9.1 Computational Pipeline

```
┌──────────────────────────────────────────┐
│         User-Anfrage                      │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│  IMMUNE GATEWAY (immune_gateway.py)      │
│  Keyword-Erkennung → automatisch         │
└────────┬───────────────────┬─────────────┘
         ↓                   ↓
┌────────────────┐  ┌───────────────────┐
│  Layer 2:      │  │  Layer 1:         │
│  YAML laden    │  │  PCT berechnen    │
│  (parameter-   │  │  LLMMC kalibrieren│
│   registry)    │  │  ODE simulieren   │
└────────┬───────┘  └───────┬───────────┘
         └──────────┬───────┘
                    ↓
┌──────────────────────────────────────────┐
│  ORCHESTRATOR (orchestrator.py)          │
│  Full Provenance Chain                   │
└────────────────┬─────────────────────────┘
                 ↓
┌──────────────────────────────────────────┐
│  Layer 3: LLM-Übersetzung               │
│  Formale Ergebnisse → natürliche Sprache │
└──────────────────────────────────────────┘
```

### 9.2 Kernkomponenten (Layer 1)

| Skript | Funktion |
|--------|----------|
| `orchestrator.py` | Three-Layer Orchestrator mit Query-Routing |
| `pct.py` | Parameter Context Transformation |
| `llmmc_calibration.py` | LLM Monte Carlo Kalibrierung |
| `immune_gateway.py` | Autonome Pre-Response Layer-1-Berechnung |
| `ode_simulator.py` | 6-Zustand Verhaltensdynamik-Simulation |
| `parameter_api.py` | Universal Parameter Lookup API |
| `r_score.py` | R-Score Monte Carlo (Distanzmessung) |

### 9.3 Validierung und Qualitätssicherung

| Prüfung | Skript | Schwelle |
|---------|--------|----------|
| Template Compliance | `check_template_compliance.py` | ≥ 85% |
| Kapitel Compliance | `check_chapter_compliance.py` | ≥ 85% |
| Referentielle Integrität | `validate_referential_integrity.py` | ≥ 85% |
| Parameter-Konsistenz | `validate_parameter_consistency.py` | Warnung bei Drift |
| Kontext-Konsistenz | `validate_context_consistency.py` | Warnung |
| BibTeX-YAML Konsistenz | `validate_bibtex_yaml_consistency.py` | Level Gate |

**Pre-Commit Hooks** blockieren automatisch:
- Appendices/Kapitel mit Compliance < 85%
- Doppelte Registry-IDs (CAS, MS, PAR, CAT)
- Level-5-Claims ohne alle 9 Komponenten
- Potenzielle Merge-Konflikte

### 9.4 Automatisierung

| System | Umfang |
|--------|--------|
| Python-Skripte | 297 |
| Slash Commands | 41+ |
| GitHub Actions | 15 CI/CD Workflows |
| Pre-Commit Hooks | 8 automatische Prüfungen |
| YAML-Datenbanken | 354+ Dateien |

---

## 10. Anwendungsbereiche

### 10.1 Anwendungshierarchie

| Anwendung | 10C-Target | Dauer | Komplexität |
|-----------|-----------|-------|-------------|
| Schnelle Verhaltensanalyse | WHAT + WHEN | 10 Min. | Niedrig |
| Interventions-Design | HOW + AWARE + READY | 30 Min. – 2 Std. | Mittel |
| Kunden-Strategiemodell | Alle 10C | 1–2 Tage | Hoch |
| Transformationsprogramm | Alle 10C + Sequenzierung | 2–12 Wochen | Sehr hoch |
| M&A Due Diligence | Alle 10C + CVA-Vertieft | 2–4 Wochen | Kritisch |

### 10.2 Branchenbeispiele

**Banking & Finance:**
LUKB, UBS, Migros Bank, BEKB, ZKB, Raiffeisen, PostFinance, Valiant, Vontobel, Julius Bär, GKB, Neon — Verhaltensbasierte Kundenstrategien, Anlageberatung, Default-Optimierung.

**Industrie & Produktion:**
ALPLA, PORR — Arbeitssicherheit, Transformationsprogramme, Langfrist-Strategiemodelle.

**Versicherung & Gesundheit:**
Helsana — Prävention, Gesundheitsverhalten, Compliance-Optimierung.

**Konsumgüter & Retail:**
Lindt, Peek & Cloppenburg, BMW — Kaufverhalten, Pricing, Customer Experience.

**Politik:**
SPÖ — Evidenzbasierte Politikberatung, Wähler:innen-Verhalten, Kommunikationsstrategie.

### 10.3 Nachgewiesene Vorhersagegenauigkeit

| Modell | Anwendung | Ergebnis |
|--------|-----------|----------|
| PSF-2.0 (Papal Selection Framework) | Papst-Konklaven 1903–2024 | 100% Gewinner-Genauigkeit (12/12) |
| Religious Distance Metric | Alevitentum–Zoroastrismus–Sunnismus | d = 0.87 vs. 1.48 (70% näher an Zoro) |
| M-Score Replikation | Replikationsvorhersage | r = 0.70 Korrelation mit tatsächlichen Raten |

---

## 11. Qualitätssicherung und Governance

### 11.1 Evidence Integration Pipeline (EIP)

Jedes neue Konzept im EBF durchläuft eine **5-Stufen-Prüfung**:

1. **Konzept dokumentieren** — Was wird behauptet?
2. **PRO-Evidenz suchen** — Mindestens 3 unterstützende Papers
3. **CONTRA-Evidenz aktiv suchen** — Gegenargumente identifizieren
4. **Entscheidung treffen** — Integrieren / Verwerfen / Modifizieren
5. **Framework-Integration** — Appendix + Kapitel + BibTeX

### 11.2 Paper Integration Workflow

Jedes neue Paper durchläuft den `/integrate-paper` Workflow mit automatischer Klassifikation (7 Kriterien, 5 Levels):

| Level | Name | Komponenten | Zeit |
|-------|------|-------------|------|
| 1 | MINIMAL | BibTeX | 5 Min. |
| 2 | STANDARD | BibTeX + Theory + Parameter | 10–15 Min. |
| 3 | CASE | + Case Registry | 15–20 Min. |
| 4 | THEORY | + Theory Catalog | 20–30 Min. |
| 5 | FULL | Alle 8 Komponenten | 60–90 Min. |

### 11.3 Reverse Engineering Workflow (REW)

Bestehende Strategie-Dokumente werden rückwärts validiert:

```
Dokumente → Operationalisierung → Axiome → Beliefs → Theorien
```

Vier Prüfebenen stellen sicher, dass jede Empfehlung auf wissenschaftlicher Evidenz basiert.

---

## 12. Ausblick

### 12.1 Aktuelle Entwicklungen

- **Immune Gateway** (Februar 2026): Autonome Layer-1-Berechnung löst das «Wirt-entscheidet»-Paradoxon.
- **PCT-Informed LLMMC** (Tier 2.5): Hybride empirisch-theoretische Priors für bessere Kalibrierung.
- **ODE-Simulator**: Counterfactual-Analyse für Interventionsvergleiche.
- **Registry Manager**: Proaktive Duplikat-Prävention mit automatischer ID-Vergabe.

### 12.2 Nächste Schritte

1. **Immune Gateway erweitern:** Vollständige Keyword-Taxonomie für alle 140+ Parameter.
2. **ODE-Validierung:** Simulationen gegen empirische Interventionsdaten validieren.
3. **Governance formalisieren:** Prozess für Layer-2-Parameter-Updates standardisieren.
4. **Monitoring:** Drift-Erkennung für Parameter-Konsistenz implementieren.
5. **Skalierung:** CVA-VERTIEFT Profile für weitere Branchen erstellen.

---

## Anhang A: Glossar

| Begriff | Definition |
|---------|-----------|
| **10C** | Die 10 CORE-Dimensionen des EBF Framework |
| **BCM2** | Behavioral Change Model 2 — die Kontext-Datenbank |
| **CVA** | Context Vector Architecture — 3-stufiges Kundenprofil |
| **EBF** | Evidence-Based Framework for Economic and Social Behavior |
| **EIP** | Evidence Integration Pipeline — 5-Stufen-Qualitätsprüfung |
| **EIT** | Emergent Intervention Theory — systematisches Interventions-Design |
| **FEPSDE** | Financial, Emotional, Physical, Social, Development, Ecological — die 6 Utility-Dimensionen |
| **LLMMC** | LLM Monte Carlo — Kalibrierungsverfahren für LLM-Schätzungen |
| **PCT** | Parameter Context Transformation — kontextabhängige Parameteranpassung |
| **TLA** | Three-Layer Architecture — die Drei-Schichten-Architektur |
| **Ψ** | Psi — die 8 Kontext-Dimensionen |
| **γ** | Gamma — Komplementaritätskoeffizient |
| **λ** | Lambda — Loss Aversion Parameter |
| **θ** | Theta — generischer Verhaltensparameter |

---

## Anhang B: Referenzen (Auswahl)

- Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. *Econometrica*, 47(2), 263–291.
- Thaler, R. H. & Sunstein, C. R. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness*. Yale University Press.
- Fehr, E. & Schmidt, K. M. (1999). A Theory of Fairness, Competition, and Cooperation. *Quarterly Journal of Economics*, 114(3), 817–868.
- Akerlof, G. A. & Kranton, R. E. (2000). Economics and Identity. *Quarterly Journal of Economics*, 115(3), 715–753.
- Laibson, D. (1997). Golden Eggs and Hyperbolic Discounting. *Quarterly Journal of Economics*, 112(2), 443–477.
- Madrian, B. C. & Shea, D. F. (2001). The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior. *Quarterly Journal of Economics*, 116(4), 1149–1187.
- Bénabou, R. & Tirole, J. (2006). Incentives and Prosocial Behavior. *American Economic Review*, 96(5), 1652–1678.
- Gao, L. et al. (2023). PAL: Program-Aided Language Models. *ICML 2023*.
- Shumailov, I. et al. (2024). AI Models Collapse When Trained on Recursively Generated Data. *Nature*, 631, 755–759.
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*.

---

*Erstellt von FehrAdvice & Partners AG*
*Evidence-Based Framework v1.27 | Februar 2026*
*Kontakt: info@fehradvice.com*
