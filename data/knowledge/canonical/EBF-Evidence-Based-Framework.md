# Das Evidence-Based Framework (EBF)

> **SSOT:** `data/knowledge/canonical/ebf.yaml`  
> **Upload-Tags:** canonical, ebf, framework, ssot  
> **Priorität:** HÖCHSTE — ersetzt alle bisherigen EBF-Einträge in der Knowledge Base

---

## Was ist das EBF?

Das **Evidence-Based Framework for Social and Economic Behavior and Decision Making (EBF)** ist zwei Dinge gleichzeitig:

### 1. Eine Wissensdatenbank
Eine systematische, kuratierte Sammlung und Ordnung wissenschaftlicher Erkenntnisse zu menschlichem Verhalten — 2'000+ Studien, 191 Theorien, 852 Cases, 404+ Kontextfaktoren.

### 2. Ein Meta-Framework
Eine Methodik, mit der **jede wissenschaftliche Theorie** eingeordnet und **für die Praxis anwendbar** gemacht werden kann.

Seit 2010 von FehrAdvice & Partners AG in Zusammenarbeit mit der Universität Zürich entwickelt.

### Was das EBF NICHT ist
Das EBF konkurriert **nicht** mit Prospect Theory, Inequity Aversion oder anderen Theorien. Es **ordnet** sie ein und macht sie **anwendbar**. Das EBF ist kein Konkurrent — es ist der Ordnungsrahmen.

### Epistemologische Position: Klare Rollenverteilung
Ob etwas wissenschaftlich anwendbar ist oder nicht, wird durch die **wissenschaftliche Forschung** entschieden — **nicht** durch das EBF. Das EBF nimmt was die Wissenschaft liefert und validiert hat, und macht es für die Praxis nutzbar.

| Rolle | Wer | Was |
|-------|-----|-----|
| **Validieren** | Wissenschaft (Falsifikation, Replikation) | «Ist die Theorie valide?» |
| **Kontextualisieren** | EBF (Einordnung, Modellsprache) | «Wann und wo ist sie anwendbar?» |
| **Anwenden** | BCM (Beratung) | «Wie nutzen wir sie für diesen Kunden?» |

```
EBF sagt NICHT:  "Prospect Theory ist wahr"
EBF sagt:        "Die Wissenschaft hat Prospect Theory validiert.
                  In DIESEM Kontext (Ψ) gilt sie mit DIESEN
                  Parametern (λ, β, ...) und interagiert SO
                  mit anderen Theorien (γ)"
```

### Die Beziehung zum BCM
EBF = wissenschaftliche Grundlage für die Weiterentwicklung des BCM (dem Beratungs-Tool). Neues Paper erscheint → EBF ordnet es ein → BCM wird besser.

### Die EBF-Methodik: Von Theorie zur Praxis

Wie macht das EBF eine wissenschaftliche Theorie praxistauglich?

```
Neue Studie erscheint
    ↓
1. 10C-Einordnung:           Welche der 10 Dimensionen adressiert sie?
    ↓
2. Ψ-Kontextualisierung:    Unter welchen Kontextbedingungen gilt sie?
    ↓
3. Parameter-Extraktion:      Welche messbaren Werte liefert sie?
    ↓
4. Komplementaritäts-Analyse: Wie interagiert sie mit anderen Theorien?
    ↓
5. Case-Zuordnung:            In welchen Praxisfällen wurde sie angewendet?
    ↓
→ Theorie ist jetzt im BCM nutzbar
```

**Konkretes Beispiel:**
```
Studie: "Loss Aversion λ = 2.5 bei Welfare-Takeup"

→ EBF ordnet ein:
  10C:             AWARE + READY + WHEN
  Ψ:               Ψ_I = bureaucratic, Ψ_S = stigma_high
  Parameter:       PAR-BEH-016, λ_R = 2.5, Tier 1 (RCT)
  Komplementarität: γ(AWARE, WHEN) dokumentiert
  Case:            CAS-xxx (Welfare Non-Takeup)

→ BCM wird besser:
  Berater:innen wissen jetzt, dass λ bei Stigma höher ist
```

## Die zentrale Innovation

```
TRADITIONELL:                    EBF:
θ = Konstante                    θ = f(Ψ, 10C)
λ = 2.25 (immer)                 λ(Ψ, 10C) = variabel

"Loss Aversion IST 2.25"         "Loss Aversion in welfare
                                  mit stigma = 2.5, aber in
                                  workplace mit peers = 1.8"

DIE VARIATION IST NICHT NOISE — SIE IST DAS SIGNAL!
```

## Parameter Context Transformation (PCT)

Die zentrale Gleichung:

```
θ_B = θ_A × ∏ᵢ M(ΔΨᵢ) × ∏ⱼ N(Δ10Cⱼ)
```

| Variable | Bedeutung |
|----------|-----------|
| θ_A | Parameter im Anchor-Kontext (aus Paper) |
| θ_B | Parameter im Target-Kontext (Vorhersage) |
| ΔΨᵢ | Kontext-Differenz |
| M(·) | Ψ-Multiplikator |

## Wissenschaftliche Basis

| Ressource | Anzahl |
|-----------|--------|
| Papers (BibTeX) | 2,347 |
| Theorien | 153 |
| Cases | 852 |
| Kontextfaktoren (CH) | 404+ |
| Parameter | 64+ |

## Die 8 Kontext-Dimensionen (Ψ-Framework)

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

## Das 10C CORE Framework

10 komplementäre Dimensionen die gemeinsam menschliches Verhalten erklären:

| # | CORE | Frage | Output |
|---|------|-------|--------|
| 1 | **WHO** | Wer hat Utility? | Welfare Hierarchy: Individual → Dyad → Group → Society |
| 2 | **WHAT** | Was ist Utility? | FEPSDE: Financial, Emotional, Physical, Social, Digital, Ecological |
| 3 | **HOW** | Wie interagieren Dimensionen? | Komplementarität γ |
| 4 | **WHEN** | Wann zählt Kontext? | 8 Ψ-Dimensionen |
| 5 | **WHERE** | Woher die Zahlen? | Parameter-Kalibrierung, 4-Tier BBB |
| 6 | **AWARE** | Wie bewusst? | Awareness-Filter A(·) ∈ [0,1] |
| 7 | **READY** | Handlungsbereit? | Willingness WAX ≥ θ |
| 8 | **STAGE** | Wo in der Journey? | Behavioral Change Journey S(t) |
| 9 | **HIERARCHY** | Wie stratifizieren Entscheidungen? | L0-L3 |
| 10 | **EIT** | Wie emergieren Interventionen? | Vektor I⃗ ∈ [0,1]⁹ |

## EBF Grundaxiome

| # | Axiom | Regel |
|---|-------|-------|
| 1 | **Empirische Fundierung** | Parameter basieren auf 2,347+ Papers, nicht auf Annahmen |
| 2 | **Parameter-Hierarchie (BBB 4-Tier)** | Literature → LLMMC → Empirical → Expert |
| 3 | **Referentielle Integrität** | Jeder Parameter verweist auf die Parameter-Registry |
| 4 | **Komplementarität ist begründet** | γ ≠ 0 Werte haben Paper-Quellen |
| 5 | **Additivität ist Default** | Komplementarität nur wenn Additivität nicht ausreicht |

## Was das EBF NICHT ist

| Falsche Annahme | Realität |
|-----------------|----------|
| ❌ Chatbot | Es ist ein wissenschaftliches Analyse-Framework |
| ❌ Big-Data-System | Es nutzt Smart Data (kuratierte Kontextfaktoren) |
| ❌ Black Box | Alle Parameter sind transparent und nachvollziehbar |
| ❌ Meinungsmaschine | Jede Aussage hat eine Quellenangabe |

## Verwandte Komponenten

| Komponente | SSOT | Beziehung |
|------------|------|-----------|
| BCM | `data/knowledge/canonical/bcm.yaml` | Kernmodell innerhalb des EBF |
| 10C CORE | `docs/frameworks/core-framework-definition.yaml` | Strukturelle Dimensionen des EBF |
| Terminology | `data/beatrix/terminology-registry.yaml` | Namenskonventionen |

---

*Letzte Aktualisierung: 2026-02-15*
