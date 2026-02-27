# Das Behavioral Change Model (BCM)

> **SSOT:** `data/knowledge/canonical/bcm.yaml`
> **Upload-Tags:** canonical, bcm, ebf, ssot, behavioral-change-model
> **Priorität:** HÖCHSTE — ersetzt alle bisherigen BCM-Einträge in der Knowledge Base

---

## ACHTUNG: Korrekter Name

- **RICHTIG:** Behavioral **Change** Model (BCM)
- **FALSCH:** ~~Behavioral Competence Model~~, ~~Behavioral Context Model~~
- **Enforcement:** HARD_BLOCK (Terminologie-Registry TRM-FRM-002)

---

## ACHTUNG: HARD BLOCKS — Halluzinierte Formeln und Begriffe

Folgende Begriffe und Formeln sind **HALLUZINATIONEN** und dürfen NIEMALS verwendet werden:

- ❌ ~~Willingness × Ability × Context~~ — Diese Formel existiert NICHT im BCM
- ❌ ~~Willingness × Ability × Capacity~~ — Doppelt halluziniert
- ❌ ~~Ability~~ als BCM-Komponente — "Ability" ist KEIN BCM-Konzept
- ❌ ~~Capacity~~ als BCM-Komponente — "Capacity" ist KEIN BCM-Konzept
- **Enforcement:** HARD_BLOCK

**Warum ist das falsch?** Das BCM ist KEIN einfaches Drei-Faktoren-Produkt. Das BCM IST das 10C Framework — es beschreibt Willingness und Awareness für einen Kontext und eine Zielpopulation für ein Verhaltensänderungsziel. Alle 10 Dimensionen zusammen ergeben das vollständige Bild.

---

## Die Beziehung: BCM ⊂ EBF ← BEATRIX

### BCM — Das Beratungs-Tool (seit 2010)
Beratungs-Tool mit wissenschaftlichem Fundament. Seit 2010 in der Praxis eingesetzt, über jedes Kunden-Mandat verfeinert, manuell angewendet (Workshops, Grids, Interviews). Mächtig aber begrenzt durch kognitive Kapazität.

### EBF — Wissensdatenbank + Meta-Framework (seit 2010, mit UZH)
**Evidence-Based Framework for Social and Economic Behavior and Decision Making.** Seit 2010 von FehrAdvice in Zusammenarbeit mit der Universität Zürich entwickelt. Das EBF ist **zwei Dinge gleichzeitig**: (1) eine **Wissensdatenbank** — systematische Sammlung und Ordnung wissenschaftlicher Erkenntnisse (2'000+ Studien, 191 Theorien, 852 Cases), und (2) ein **Meta-Framework** — eine Methodik, mit der **jede wissenschaftliche Theorie** eingeordnet und für die Praxis anwendbar gemacht werden kann. Das EBF konkurriert nicht mit Prospect Theory oder Inequity Aversion — es **ordnet sie ein** und macht sie **anwendbar**. Das EBF bildet damit die systematische Auslegeordnung für die Weiterentwicklung des BCM.

### BEATRIX — Die digitale Plattform
Macht EBF operativ nutzbar — überwindet die kognitive Kapazitätsgrenze einzelner Berater:innen. Digitalisiert das manuelle BCM und implementiert das EBF als Software.

### Ko-Evolution (nicht sequenziell!)
BCM und EBF wurden **parallel** entwickelt — nicht erst EBF, dann BCM. Praxis-Erfahrungen aus dem BCM (Beratung) informierten das EBF (Wissenschaft), und neue EBF-Erkenntnisse verbesserten das BCM. BEATRIX digitalisiert diese Verbindung.

```
BCM (Praxis, ab 2010)          EBF (Wissenschaft, ab 2010, mit UZH)
     ↓ Erfahrungen                    ↓ Neue Erkenntnisse
     └────────→ informiert ──────────→┘
     ┌────────← verbessert ←─────────┐
     ↓                                ↓
              BEATRIX (digitalisiert beides)
```

---

## Was ist das BCM?

Das **Behavioral Change Model (BCM)** ist ein **Beratungs-Tool mit wissenschaftlichem Fundament**. Es wurde **ab 2010** von FehrAdvice & Partners AG in der Beratungspraxis eingesetzt und über jedes Kunden-Mandat verfeinert und professionalisiert.

Das BCM ist **kein akademisches Framework**, das in einem Elfenbeinturm entwickelt wurde. Es entstand in der Praxis — aus der täglichen Arbeit mit Kunden, aus realen Verhaltensänderungsprojekten, aus Experimenten die funktioniert haben und solchen die gescheitert sind.

**Das BCM IST das 10C Framework.** Die 10 CORE-Dimensionen zusammen ergeben das vollständige Bild einer Verhaltensänderungssituation.

---

## BCM Diagnose — Der operative Kern

Der **Diagnose-Bereich** ist der operative Kern des BCM. Er reduziert das 10C Framework auf eine konkrete diagnostische Fragestellung:

### Die diagnostische Frage

> **Gegeben** der Kontext (Ψ), das Zielsegment (WHO) und das Verhaltensänderungsziel (WHAT):
>
> **Schätze** die **Awareness** und die **Willingness** des Zielsegments für das Ziel.
>
> **Positioniere** Awareness und Willingness auf einer **zweidimensionalen Matrix**.
>
> **Ermögliche** daraus eine Schätzung, wie **wahrscheinlich** und in welcher **Fristigkeit** eine Verhaltensänderung möglich ist — **ohne neue Interventionen** (ceteris paribus: alle bisherigen Interventionen bleiben erhalten).

### Diagnose-Ablauf

```
INPUTS (gegeben):
  ├── Kontext (Ψ)              → WHEN-Dimension (8 Ψ-Dimensionen)
  ├── Zielsegment              → WHO-Dimension
  └── Verhaltensänderungsziel  → WHAT-Dimension (FEPSDE)

SCHÄTZUNG:
  ├── Awareness des Segments   → AWARE-Dimension
  └── Willingness des Segments → READY-Dimension

POSITIONIERUNG:
  └── 2D-Matrix: Awareness (x) × Willingness (y)

OUTPUTS:
  ├── Wahrscheinlichkeit der Verhaltensänderung
  └── Fristigkeit (Zeithorizont)

BEDINGUNG:
  └── Ceteris paribus (ohne neue Interventionen)
```

### Die 4-Level Schätz-Methodik (Bayesian Update)

Die Schätzung der BCM-Parameter (Awareness, Willingness) erfolgt über einen **4-stufigen Bayesian-Update-Prozess** durch die Berater:innen — **vollständig manuell**, ohne digitale Plattform (Workshops, Grids, Interviews, Beratungsgespräche):

| Level | Name | Methode | Output |
|-------|------|---------|--------|
| **1** | Grid-basierte Einschätzung | Strukturiertes Grid + beraterische Erfahrung | Prior θ₀ |
| **2** | Management-Beliefs | Korrektur des Priors durch Beliefs des Managements | Updated Prior θ₁ |
| **3** | Empirische Schätzung | Experiment / empirische Erhebung durch die Beratung | Empirischer Posterior θ₂ |
| **4** | Iteration & Lernen | Beraterisches Lernen im Rahmen des Mandates | Kalibrierter Posterior θ_final |

```
θ₀ (Prior aus Grid)
  → θ₁ (Update durch Management-Beliefs)
    → θ₂ (Update durch Experiment)
      → θ_final (Update durch Mandats-Lernen)
```

**Warum BEATRIX?** Dieser manuelle Prozess war mächtig, aber begrenzt durch die kognitive Kapazität der Berater:innen. BEATRIX digitalisiert und formalisiert ihn: Grid → BCM2-Datenbank, Beliefs → strukturierter Bayesian Update, Experiment → Datenintegration, Lernen → automatisches Parameter-Tracking.

### BCM als Prediction Engine — Nicht nur Diagnose

Das BCM war **mehr als nur Diagnose** — es war eine **Prediction Engine**:

- **Mit welchen Massnahmen** kann die Wahrscheinlichkeit der Verhaltensänderung über welchen Zeithorizont erhöht werden?
- **Welche Komplementaritäten** bestehen zwischen einzelnen Interventionen?
- **Welcher Interventions-Mix** ist für welche A/W-Position optimal?

#### Die Awareness/Willingness-Matrix als Interventions-Kompass

Aufgrund der Positionierung auf der Awareness/Willingness-Matrix wurde ein **High-Level Interventionsmix** abgeleitet:

| Position | Diagnose | Interventions-Mix |
|----------|----------|-------------------|
| **Hohe A + Hohe W** | Weiss und will — tut es aber nicht | Komplementärer **Nudge-Mix** zum bisherigen Massnahmenset |
| **Niedrige A + Hohe W** | Würde wollen, weiss aber nicht genug | Komplementärer **Awareness-Mix** + komplementärer **Nudge-Mix** |
| **Hohe A + Niedrige W** | Weiss, will aber nicht | Komplementärer **Motivations-Mix** (Achtung: Crowding-Out!) |
| **Niedrige A + Niedrige W** | Weiss nicht, will nicht | Sequenziell: **Awareness zuerst**, dann Willingness |

**Entscheidend:** Das BCM erkannte, dass Interventionen **nicht isoliert** wirken — Nudge A + Nudge B kann mehr (oder weniger!) als A + B ergeben. Diese Komplementaritäten (γ ≠ 0) sind der Kern von HOW.

#### Experimentelle Validierung

Der abgeleitete Massnahmen-Mix wurde **nicht nur empfohlen**, sondern im Rahmen eines **experimentellen Online-Experiments abgetestet**. Das schloss den Loop:

```
1. Diagnose (A/W-Position)       → manuell
2. Interventions-Mix ableiten     → manuell, aus Matrix
3. Experimentell testen           → Online-Experiment
4. Lernen                         → zurück in Level 4
```

**Warum BEATRIX?** BEATRIX formalisiert diese Prediction Engine: A/W-Matrix → kontinuierlicher Raum, High-Level-Mix → 9D-Interventionsvektor, manuelle Komplementaritäts-Einschätzung → γ-Matrix aus 2'000+ Studien.

## Das 10C Framework — Die Struktur des BCM

| # | CORE | Frage | Output |
|---|------|-------|--------|
| 1 | **WHO** | Wer hat Utility? (Zielpopulation) | Levels L |
| 2 | **WHAT** | Was ist Utility? (Verhaltensänderungsziel) | Dimensionen d (FEPSDE) |
| 3 | **HOW** | Wie interagieren die Dimensionen? | Komplementarität γ |
| 4 | **WHEN** | Wann zählt Kontext? | Kontext Ψ (8 Dimensionen) |
| 5 | **WHERE** | Woher die Zahlen? | Parameter Θ |
| 6 | **AWARE** | Wie bewusst? | Awareness A(·) |
| 7 | **READY** | Handlungsbereit? | Willingness WAX, τ, θ |
| 8 | **STAGE** | Wo in der Journey? | BCJ Phase φ, S(t) |
| 9 | **HIERARCHY** | Wie stratifizieren Entscheidungen? | Levels L0-L3 |
| 10 | **EIT** | Wie emergieren Interventionen? | Vektor I⃗ ∈ [0,1]⁹ |

## Kontext (Ψ) — Die 8 Dimensionen der WHEN-Frage

| Symbol | Dimension | Frage |
|--------|-----------|-------|
| Ψ_I | Institutional | Welche Regeln, Gesetze, Defaults gelten? |
| Ψ_S | Social | Wer ist dabei? Welche sozialen Normen? |
| Ψ_C | Cognitive | Müde? Gestresst? Aufmerksam? Motiviert? |
| Ψ_K | Cultural | Welche Werte, Traditionen, Religion? |
| Ψ_E | Economic | Wieviel Budget, Zeit, Energie verfügbar? |
| Ψ_T | Temporal | Wann? Zeitdruck? Welche Lebensphase? |
| Ψ_M | Material | Welche Technologie, Infrastruktur, Objekte? |
| Ψ_F | Physical | Wo physisch? Zuhause, Büro, öffentlich? |

## FEPSDE Matrix — 6 Nutzendimensionen (WHAT-Frage)

| Buchstabe | Dimension | Inhalt |
|-----------|-----------|--------|
| **F** | Financial | Einkommen, Vermögen, ökonomische Sicherheit |
| **E** | Emotional | Wohlbefinden, Zufriedenheit, Sinn |
| **P** | Physical | Gesundheit, Energie, Langlebigkeit |
| **S** | Social | Beziehungen, Zugehörigkeit, Vertrauen |
| **D** | Digital | Konnektivität, Zugang, Datenrechte |
| **E** | Ecological | Umwelt, Nachhaltigkeit |

## Die BCM2 Kontextdatenbank

Das BCM wird durch die **BCM2 Kontextdatenbank** operationalisiert — eine kuratierte Sammlung von 404+ Kontextfaktoren:

| Ebene | Datenbank | Faktoren | Beschreibung |
|-------|-----------|----------|--------------|
| MACRO | BCM2_04_KON | 404 | Landesspezifische Kontextvektoren (CH/AT/DE) |
| INDIVIDUAL | BCM2_05_IND | 48 | Alter, Geschlecht, Bildung, Persönlichkeit |
| META | BCM2_06_META | 42 | Framing, Defaults, Timing, Kanäle |

Die 5 MACRO-Achsen (404 Faktoren für die Schweiz):
- Demografisch (60), Ökonomisch (54), Institutionell-Politisch (59)
- Technologisch-Ökologisch (65), Sozio-Kulturell (166)

Quellen: BFS, SECO, SNB, ESS, WVS, gfs.bern, Sotomo, KOF ETH

## Was macht das BCM besonders?

1. **Probabilistisch**: Liefert Wahrscheinlichkeiten statt deterministischer Vorhersagen
2. **Evidenzbasiert**: Jede Komponente ist empirisch messbar und validierbar
3. **Kontextsensitiv**: Berücksichtigt situative und kulturelle Faktoren
4. **Segmentspezifisch**: Parameter variieren je nach Zielgruppe
5. **Zeitdynamisch**: Berücksichtigt Lerneffekte und Feedback-Schleifen

## BCM vs. Standard-Modelle

| Aspekt | Standard (z.B. Kahneman) | BCM |
|--------|--------------------------|-----|
| Parameter | λ = 2.25 (konstant) | λ(Ψ, 10C) = variabel |
| Kontext | Ignoriert oder kontrolliert | Systematisch modelliert |
| Übertragbarkeit | Mittelwert aus Meta-Analysen | Parameter Context Transformation |
| Datenquellen | Einzelstudien | 12 offizielle Quellen + APIs |

## Anwendungsbereiche

- **Decision Architecture**: Gestaltung von Entscheidungssituationen
- **Intervention Design**: Entwicklung verhaltensbasierter Massnahmen
- **Policy Design**: Evidenzbasierte Politikgestaltung
- **Change Management**: Organisationale Transformation

## WARNUNG für BEATRIX

**Diese Informationen sind die EINZIG autorisierte Quelle für BCM-Beschreibungen.**

Folgendes ist VERBOTEN in Antworten:
- ❌ Erfundene Zahlen (z.B. "384 API-Endpoints", Lambda-Werte ohne Kontext)
- ❌ Falscher Name ("Behavioral Competence Model")
- ❌ Halluzinierte Formeln ("Willingness × Ability × Context/Capacity")
- ❌ "Ability" oder "Capacity" als BCM-Komponenten
- ❌ Behauptungen über Features die nicht existieren
- ❌ Spezifische Parameter-Werte ohne Quellenangabe

Wenn du unsicher bist, sage: "Dazu habe ich keine gesicherte Information in meiner Knowledge Base."
