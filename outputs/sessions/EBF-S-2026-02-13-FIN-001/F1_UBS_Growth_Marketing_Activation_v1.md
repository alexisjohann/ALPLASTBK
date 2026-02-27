# UBS Growth Marketing Activation: Behavioral Strategy Report

**Evidence-Based Framework (EBF) Analysis**

---

**Prepared by:** FehrAdvice & Partners AG | EBF Framework
**Session:** EBF-S-2026-02-13-FIN-001
**Date:** 13. Februar 2026
**Classification:** Confidential
**Version:** 1.0

---

## Executive Summary

Die UBS steht nach der Credit-Suisse-Integration vor einer einmaligen Herausforderung: 3.7 Millionen Schweizer Kund:innen müssen aktiviert, gehalten und vertieft werden — bei gleichzeitigem Kostendruck (Cost-to-Income von 78% auf 70%) und zunehmendem Wettbewerb durch Neobanks und BigTech.

Diese Analyse nutzt das Evidence-Based Framework (EBF) mit 8 Kontext-Dimensionen, 4 Verhaltensmodellen, 60+ validierten Parametern aus der BCM2-Kontextdatenbank und einer Monte-Carlo-Sensitivitätsanalyse, um eine datengestützte Behavioral-Marketing-Strategie zu entwickeln.

### Die 5 Kernaussagen

1. **Default-Architektur ist der universelle Hebel.** Die Schweizer Default-Compliance liegt bei κ = 0.85 (Deutschschweiz: 0.88-0.90). Opt-Out-Designs für Anlageprodukte können die Activation Rate von 5% auf 17-20% steigern.

2. **Trust Recovery bei Ex-CS ist existenziell.** Die Vertrauenslücke (τ = 0.55 vs. Legacy τ = 0.75) gefährdet CHF 500 Mio. Revenue. Die Trust-Asymmetrie (β/α = 3.5) bedeutet: 1 Fehler braucht 4 positive Kontakte zur Kompensation. Fehler-Prävention hat 3.5× mehr Impact als Trust-Aufbau.

3. **Digital-Only hat höchstes Churn-Risiko.** 25-35% Abwanderungsrisiko (bis 45% nach SIX bLink). App-Friction von 0.60 vs. Revolut 0.15 = 4× Gap.

4. **Life Events sind der effizienteste ROI-Hebel.** Erbschaft ×2.5, 3a-Deadline ×2.2, Bonus ×1.8. Timing schlägt Targeting.

5. **CHF 1.44 Mrd. Swing zwischen Worst und Best Case.** Investment von CHF 18-38 Mio. in Behavioral Marketing generiert CHF 415-840 Mio. Return (10-40× ROI).

---

\newpage

## Inhaltsverzeichnis

1. [Einleitung und Fragestellung](#1-einleitung-und-fragestellung)
2. [Kontextanalyse (8 Ψ-Dimensionen)](#2-kontextanalyse)
3. [Kundensegmente und Personas](#3-kundensegmente-und-personas)
4. [Modellspezifikation](#4-modellspezifikation)
5. [Parametrisierung und Validierung](#5-parametrisierung-und-validierung)
6. [Ergebnisse: Activation Score Analyse](#6-ergebnisse)
7. [Szenario-Analyse](#7-szenario-analyse)
8. [Wettbewerbs-Benchmarks](#8-wettbewerbs-benchmarks)
9. [Interventions-Design](#9-interventions-design)
10. [Roadmap Q1-Q4 2026](#10-roadmap)
11. [Budget und ROI](#11-budget-und-roi)
12. [Risiken und Crowding-Out](#12-risiken-und-crowding-out)
13. [KPIs und Erfolgsmessung](#13-kpis-und-erfolgsmessung)
14. [Schlussfolgerungen und Empfehlungen](#14-schlussfolgerungen)
15. [Anhang A: Parameter-Tabellen](#anhang-a)
16. [Anhang B: Monte Carlo Ergebnisse](#anhang-b)
17. [Anhang C: BCM2 Kontext-Faktoren](#anhang-c)
18. [Anhang D: Literaturverzeichnis](#anhang-d)
19. [Anhang E: Methodik](#anhang-e)

---

\newpage

## 1. Einleitung und Fragestellung

### 1.1 Ausgangslage

Die UBS hat mit der Übernahme der Credit Suisse im Juni 2023 die grösste Banken-Integration der Schweizer Geschichte eingeleitet. Zum Zeitpunkt dieser Analyse (Februar 2026) ist die Migration zu 75% abgeschlossen, mit 1+ Million migrierter Credit-Suisse-Kund:innen.

Die Herausforderungen sind vielschichtig:

- **3.7 Millionen Schweizer Kund:innen** müssen aktiviert werden (Invest-Penetration: nur 5%)
- **1 Million Ex-CS-Kund:innen** haben eine Vertrauenslücke (τ_Benevolence = 0.45 vs. Legacy 0.70)
- **800'000 Digital-Only-Kund:innen** drohen an Neobanks zu verlieren (Churn-Risiko 25-35%)
- **Cost-to-Income Ratio** muss von 78% auf 70% sinken (≈ USD 1.4 Mrd. Einsparung)
- **SIX bLink** (Open Banking, November 2025) senkt die Wechselkosten für alle Kund:innen

### 1.2 Zentrale Fragen

| # | Frage | Modell |
|---|-------|--------|
| Q1 | Wie hoch ist das Activation-Potenzial pro Segment? | MOD-UBS-GMA-001 |
| Q2 | Wie schnell und wodurch erholt sich das Vertrauen bei Ex-CS? | M3: Trust Recovery |
| Q3 | Wie viele Kund:innen verlieren wir an Neobanks/BigTech? | M1: Competitive Response |
| Q4 | Wie verteilen wir das Budget optimal auf Segmente × Module? | M2: Budget Allocation |

### 1.3 Methodik

Die Analyse folgt dem EBF-Workflow (Evidence-Based Framework for Economic and Social Behavior):

1. **Kontextanalyse** — 8 Ψ-Dimensionen mit BCM2-Datenbank (60+ validierte Faktoren)
2. **Modellspezifikation** — 4 integrierte Verhaltensmodelle
3. **Parametrisierung** — LLMMC Prior + Bayesian Posterior + Monte Carlo (10k Draws)
4. **Analyse** — Szenario-Vergleich (Best/Expected/Worst) + Sensitivität
5. **Interventions-Design** — 4 No-Regret Moves + Quarterly Roadmap

### 1.4 Datengrundlagen

| Quelle | Umfang | Verwendung |
|--------|--------|------------|
| BCM2-Kontextdatenbank | 404 Schweizer Kontext-Faktoren | Makro-Parameter |
| UBS Kundendaten (anonymisiert) | 350-Faktor Context Vector | Segment-Parameter |
| Focus Group Simulation | 7 Personas, 3 Segmente | Mikro-Verhalten |
| Wissenschaftliche Literatur | 85+ Papers | Parameter-Validierung |
| EBF Theory Catalog | 31 relevante Theorien | Modell-Fundierung |
| Wettbewerbs-Profile | 6 Banken (Raiff, ZKB, PostFin, Migros, JB, Revolut) | Benchmarks |

---

\newpage

## 2. Kontextanalyse

### 2.1 Die 8 Ψ-Dimensionen

Das EBF analysiert jede Situation anhand von 8 Kontext-Dimensionen. Für die UBS Growth Marketing Activation sind alle 8 Dimensionen relevant:

#### Ψ_I — Institutionelle Regeln

Die UBS operiert in einem der am stärksten regulierten Umfelder weltweit:

- **G-SIB-Status** (Global Systemically Important Bank) mit verschärften Kapitalanforderungen
- **FINMA-Aufsicht** mit spezifischen Anforderungen an Kundenkommunikation
- **Too Big To Fail** Doktrin (TBTF) — begrenzt Risikobereitschaft
- **PSD2/PSD3** (Payment Services Directive) — ermöglicht Open Banking
- **SIX bLink** — Multibanking-Plattform ab November 2025

**EBF-Implikation:** Regulierung ist nicht nur Constraint, sondern auch Vertrauensressource. Regulierte Banken geniessen höheres Grundvertrauen als Neobanks (τ_regulated = 0.75 vs. τ_neobank = 0.55).

#### Ψ_S — Soziale Struktur

Die UBS-Kundschaft umfasst 4 distinkte Segmente mit radikal unterschiedlichen sozialen Kontexten:

| Segment | Grösse | Soziale Situation | Verhaltens-Dominante |
|---------|--------|-------------------|---------------------|
| Legacy UBS | 1.5M | Etablierte Bankbeziehung, hohe Identifikation | Status, Gewohnheit |
| Ex-CS Migriert | 1.0M | Erzwungener Wechsel, Unsicherheit | Vertrauensverlust, Identitätskrise |
| Digital-Only | 0.8M | App-natives Verhalten, schwache Bindung | UX, Convenience, Social Proof |
| Affluent | 0.4M | Premium-Erwartung, RM-Beziehung | Personalisierung, Prestige |

#### Ψ_C — Kognitiver Zustand

Die verhaltensökonomischen Parameter variieren dramatisch über Segmente und Situationen:

- **Loss Aversion (λ):** 1.6 (Digital-Only, jung) bis 3.4 (Peter, Handwerker, nie investiert)
- **Present Bias (β):** 0.60 (Julia, 28, YOLO) bis 0.88 (Thomas, 58, Pensionsplanung)
- **Trust (τ):** 0.30 (Marco, Swissquote-Nutzer) bis 0.85 (Legacy UBS)
- **Default Sensitivity (κ):** 0.40 (Marco, aktiver Entscheider) bis 0.90 (Peter, Gewohnheitstier)

**Kritische Erkenntnis:** Im Stresszustand (Marktkrise, Deadline) verschieben sich Parameter dramatisch: λ_Krise = 3.0-4.0, β_Stress = 0.40-0.60. Defaults werden dann zu 95-98% beibehalten.

#### Ψ_K — Kulturelle Werte

Schweizer Bankkultur hat spezifische Eigenheiten, die direkt auf Verhaltensparameter wirken:

- **Eigentumskonzept (CH-REG-06):** DE-CH = 0.78 → überdurchschnittlich hohe Loss Aversion bei Vermögensthemen
- **Default-Compliance (CH-REG-08):** 0.82-0.88 → Schweizer:innen bleiben bei Defaults
- **Soziale Normen (CH-REG-09):** DE-CH = 0.78, FR-CH = 0.68 → regionale Heterogenität
- **Diskretion:** Bankgeheimnis-Tradition → implizites Vertrauen, aber auch Informationsresistenz

**Regionale Differenzierung:** Durchgängig +10 Prozentpunkte bei κ, σ und λ_property in der Deutschschweiz gegenüber der Romandie. Dies erfordert regionalisierte Interventionen.

#### Ψ_E — Ökonomische Ressourcen

Die UBS-Finanzlage ist geprägt von Wachstum bei gleichzeitigem Effizienzmandat:

- **Revenue:** USD 47.5 Mrd. (+31% YoY) — Wachstum finanziert strategische Investitionen
- **Cost-to-Income:** 78% (Ziel: 70% bis 2026) — erfordert USD 1.4 Mrd. Einsparung
- **Marketing Budget:** geschätzt CHF 280-570 Mio. (2-4% Non-Personnel Costs)
- **IT/Digital:** USD 6.5 Mrd. — grösster Nicht-Personalposten, Marketing-Tech profitiert
- **CS-Synergien:** 65% erreicht (USD 8.5 Mrd. von 13 Mrd. Ziel)

**Implikation:** Budget ist constrained aber strategisch. Jeder Marketing-Franken braucht ROI-Nachweis. Behavioral Marketing hat Vorteil: hoher Impact bei niedrigen Kosten.

#### Ψ_T — Zeitlicher Kontext

Mehrere Zeitachsen konvergieren:

- **CS-Integration:** 75% abgeschlossen, Deadline Ende 2026
- **Trust Recovery:** 15-18 Monate benötigt (bei null Fehlern)
- **SIX bLink:** Ab November 2025 — senkt Wechselkosten
- **3a-Deadline:** Jährlich im Dezember — stärkster einzelner Aktivierungstrigger
- **Generelles Vertrauen:** Fallend (von 6.0/10 in 2024 auf prognostiziert 4.8/10 in 2040)

**Kritische Zeitfenster:**

- **Jetzt bis Q2 2026:** Trust Recovery muss starten BEVOR bLink live geht
- **November-Januar:** Jährlicher PEAK (3a + Bonus + 13. Monatslohn)
- **2026 als Ganzes:** Make-or-Break Jahr für Post-CS-Integration

#### Ψ_M — Technologische Tools

Die UBS-Infrastruktur umfasst:

- **200 Filialen** (konsolidiert von 285, Ziel ~190) — physische Präsenz abnehmend
- **78% Digital Active** — hohe digitale Durchdringung
- **65% Mobile Banking** — Hauptkanal für Retail
- **25 Digital-Only Produkte** — reines Online-Angebot wachsend
- **300+ AI Use Cases** — inkl. Next-Best-Action Engine
- **Next-Best-Action Engine** deployed — Personalisierung möglich

**UX-Gap:** App-Friction Score 0.60 vs. Revolut ~0.15. Der Investment-Einstieg erfordert 7 Taps (Revolut: 2 Taps). Dies ist der grösste technische Hebel.

#### Ψ_F — Physischer Kontext

- **Schweiz-Fokus:** 12% des Gruppen-Revenues, aber strategischer Anker
- **Omnichannel:** Branch + App + Web + RM — unterschiedliche Conversion-Raten
- **RM-Kanal:** 3.5× höhere Conversion als Digital — aber skaliert nicht bei 3.5M Kund:innen
- **Global:** 52 Länder, 6 Booking Centers — Wealth Management als Haupttreiber

### 2.2 Kontext-Synthese

Die 8 Dimensionen interagieren. Die wichtigsten Interaktionen für die UBS-Situation:

| Interaktion | Effekt | Implikation |
|-------------|--------|-------------|
| Ψ_E (Budget) × Ψ_S (Segmente) | Nicht alle 3.7M gleich behandeln | ROI-Priorisierung zwingend |
| Ψ_M (bLink) × Ψ_S (Digital-Only) | Switching Costs sinken um ~30% | Time-to-Activate kritisch |
| Ψ_C (Trust-Gap) × Ψ_T (Integration) | Trust Recovery parallel zur Migration | Fehlerfreiheit existenziell |
| Ψ_K (Regional) × Ψ_I (Default) | DE-CH vs. FR-CH: 10pp Differenz | Regionalisierte Interventionen |

---

\newpage

## 3. Kundensegmente und Personas

### 3.1 Die 4 Segmente im Überblick

#### Segment 1: Legacy UBS (1.5 Millionen)

**Profil:** Bestehende UBS-Kund:innen mit etablierter Bankbeziehung. Hohe Identifikation mit der Marke (ι = 0.75), überdurchschnittliches Vertrauen (τ = 0.75-0.85), aber niedrige Investment-Penetration (5%).

**Hauptbarriere:** Produktkomplexität — nicht fehlendes Vertrauen, sondern fehlende Einfachheit.

**BCJ Journey Stages:**

| Stage | Anteil | Beschreibung |
|-------|--------|--------------|
| UNAWARE | 20% | Kennen Anlageoptionen nicht |
| AWARE_PASSIVE | 45% | Kennen, aber kein Interesse |
| CONSIDERING | 20% | Überlegen |
| INTENDING | 10% | Planen zu handeln |
| ACTIVE | 5% | Bereits aktiv investiert |

**Interventions-Potenzial:** MITTEL. Default-Architektur (κ = 0.85) ist der Haupthebel. 45% sitzen in AWARE_PASSIVE fest — klassisches «Intention-Action Gap».

#### Segment 2: Ex-CS Migriert (1 Million)

**Profil:** Ehemalige Credit-Suisse-Kund:innen, die 2024 zur UBS migriert wurden. Vertrauensdefizit auf allen 4 Dimensionen, besonders Benevolence (τ_B = 0.45, Gap von -0.30 zu Legacy). Identifizieren sich noch als «CS-Kund:innen» (ι_UBS = 0.40).

**Hauptbarriere:** Vertrauenslücke — «Ist UBS auf meiner Seite oder will sie nur verkaufen?»

**Trust-Breakdown:**

| Dimension | Ist | Ziel | Gap | Recovery-Geschwindigkeit |
|-----------|-----|------|-----|-------------------------|
| Competence | 0.70 | 0.80 | -0.10 | Schnell (~3 Monate) |
| Predictability | 0.55 | 0.75 | -0.20 | Mittel (~7 Monate) |
| Integrity | 0.50 | 0.75 | -0.25 | Langsam (~12 Monate) |
| Benevolence | 0.45 | 0.75 | -0.30 | Sehr langsam (~15 Monate) |

**Revenue at Risk:** CHF 500 Mio. im Worst Case (30% Churn bei Trust-Versagen).

**Interventions-Potenzial:** HOCH — aber nur bei Trust Recovery. Ohne Vertrauensaufbau sind alle anderen Massnahmen wirkungslos.

#### Segment 3: Digital-Only (800'000)

**Profil:** App-native Kund:innen, die primär über Mobile Banking interagieren. Jünger, höhere Present Bias (β = 0.72-0.78), extreme Effort-Sensitivität (ε = 0.80-0.90). Sehr empfänglich für Social Proof (σ_Peers = 0.85).

**Hauptbarriere:** App-Friction (0.60) + Awareness-Gap (A_knowledge = 0.25). Sie wissen nicht, DASS sie investieren sollten, und wenn sie es wüssten, wäre der Weg zu kompliziert.

**Churn-Risiko:** Höchstes aller Segmente (25-35%, bis 45% nach bLink). Revolut (900k CH-Nutzer) und Neon (222k) bieten bessere UX bei niedrigeren Kosten.

**Interventions-Potenzial:** SEHR HOCH. Micro-Learning + App-Friction-Reduktion + Social Proof = Trifecta für Activation.

#### Segment 4: Affluent (400'000)

**Profil:** CHF 250k-2M Vermögen. Hohe Erwartungen an Personalisierung und Service. RM-Beziehung ist Hauptbindungsfaktor. Status-orientiert (ι = 0.70), niedrige Present Bias (β = 0.85-0.88).

**Hauptbarriere:** Nicht Produkt oder Vertrauen, sondern Personalisierungsgrad. Erwarten massgeschneiderte Beratung.

**Interventions-Potenzial:** HOCH — primär durch RM×App-Hybrid (Conversion 3.5× vs. Digital allein).

### 3.2 Die 7 Personas (Focus Group Simulation)

Basierend auf dem UBS Save & Invest Pilotprojekt (MOD-UBS-037-001) wurden 7 repräsentative Personas entwickelt:

#### Sandra Meier (42, HR-Managerin, CHF 120k) — SEG-01: Cash Holder

- **λ = 2.9** (hohe Verlustaversion), **τ = 0.55** (moderates Vertrauen), **ε = 0.75** (hohe Effort-Sensitivität)
- Hauptbarriere: «Ich habe Angst, mein Geld zu verlieren»
- Conversion-Potenzial: 4/10 → 6/10 mit Step-by-Step-Guidance
- Intervention: Kleinstbeträge-Einstieg (CHF 50/Monat), Fortschritts-Visualisierung

#### Thomas Brunner (58, Versicherungsmanager, CHF 145k) — SEG-01: Cash Holder

- **λ = 3.1** (sehr hohe Verlustaversion), **β = 0.80** (mittlere Zeitpräferenz), **σ = 0.45** (moderater Social Proof)
- Hauptbarriere: «In meinem Alter brauche ich Sicherheit, keine Rendite»
- Conversion-Potenzial: 6/10 → 8/10 mit historischen Daten und Kapitalgarantie
- Intervention: Konservatives Default-Portfolio, transparente Kosten, Simulationsrechner

#### Leila Özdemir (34, Projektmanagerin, CHF 95k) — SEG-01: Cash Holder

- **λ = 2.6**, **σ = 0.70** (hoher Social Proof), **τ = 0.45** (niedriges Vertrauen)
- Hauptbarriere: «Was machen andere in meiner Situation?» + Eigenheimkauf bald
- Conversion-Potenzial: 5/10 → 7/10 mit Peer-Vergleich und Liquiditätsgarantie
- Intervention: Social Proof («73% deiner Kolleg:innen investieren»), jederzeit verfügbar

#### Marco Keller (38, Software-Ingenieur, CHF 140k) — SEG-02: Invested Elsewhere

- **λ = 1.7** (niedrig), **τ_UBS = 0.30** (sehr niedrig für UBS als Plattform), **κ = 0.40** (aktiver Entscheider)
- Hauptbarriere: «Warum UBS statt Swissquote? Höhere Gebühren, weniger Features»
- Conversion-Potenzial: 3/10 → 5/10 (HARD SELL)
- Intervention: Feature Parity + Consolidation Value + kompetitive Preise

#### Nina Gerber (45, Ärztin/Praxisinhaberin, CHF 250k) — SEG-02: Invested Elsewhere

- **ε = 0.85** (extreme Effort-Sensitivität), **τ = 0.40**, Vermögen fragmentiert über 3 Plattformen
- Hauptbarriere: «Keine Zeit für mehrere Plattformen, aber ich will nicht belehrt werden»
- Conversion-Potenzial: 7/10 → 9/10 (BEREIT, wenn Friction weg)
- Intervention: One-Stop-Consolidation, Zero-Push-Sales, Autonomie bewahren

#### Peter Huber (52, selbständiger Elektriker, CHF 85k) — SEG-03: Never Invested

- **λ = 3.4** (sehr hohe Verlustaversion), **κ = 0.90** (extreme Default-Sensitivität), **τ = 0.35** (sehr niedriges Bankvertrauen)
- Hauptbarriere: «Investieren ist nicht für Leute wie mich» — Identitätsmismatch
- Conversion-Potenzial: 2/10 → 4/10 (SEHR SCHWER)
- **Backfire-Risiko:** Fear-Messaging Score nur 2.7/5.0 — Peter explizit: «Die wollen mir Angst machen!»
- Intervention: Persönliche Empfehlung von Vertrauensperson (Frau, Freund), extreme Vereinfachung

#### Julia Weber (28, Marketing-Managerin, CHF 78k) — SEG-03: Never Invested

- **β = 0.60** (sehr hohe Present Bias), **σ = 0.75** (sehr hoher Social Proof), **ε = 0.90** (extreme Effort-Sensitivität)
- Hauptbarriere: «YOLO — ich lebe jetzt, nicht in 40 Jahren» + «Ich hab eh nicht genug Geld»
- Conversion-Potenzial: 5/10 → 7/10 mit Social Trigger
- Intervention: Instagram-Style Content, Peer-Proof, CHF 10 Einstieg, Gamification

### 3.3 Segment-Heterogenität: Warum One-Size-Fits-All scheitert

Die Verhaltensparameter variieren um den Faktor 2-10× über die Personas:

| Parameter | Minimum | Maximum | Faktor | Segment-Beispiel |
|-----------|---------|---------|--------|------------------|
| λ (Loss Aversion) | 1.6 | 3.4 | 2.1× | Digital vs. Peter |
| τ (Trust) | 0.30 | 0.85 | 2.8× | Marco vs. Legacy |
| β (Present Bias) | 0.60 | 0.88 | 1.5× | Julia vs. Thomas |
| κ (Default) | 0.40 | 0.90 | 2.3× | Marco vs. Peter |
| σ (Social Proof) | 0.35 | 0.85 | 2.4× | Marco vs. Julia |
| ε (Effort) | 0.45 | 0.90 | 2.0× | Affluent vs. Julia |

**Fazit:** Eine einheitliche Marketing-Strategie wäre maximal für 1 von 7 Personas optimal und für die anderen suboptimal oder sogar kontraproduktiv (Backfire).

---

\newpage

## 4. Modellspezifikation

### 4.1 Modell-Architektur

Die Analyse verwendet 4 integrierte Verhaltensmodelle:

#### Basis-Modell: MOD-UBS-GMA-001 (Growth Marketing Activation)

**Formel:**

A = Σᵢ wᵢ × Mᵢ

Wobei A der Unified Activation Score ist und Mᵢ die 4 Module:

| Modul | Name | w_default | w_CS | w_Digital | Beschreibung |
|-------|------|-----------|------|-----------|--------------|
| A | Digital Activation | 0.35 | 0.25 | 0.50 | App-Friction, Awareness, In-App-Nudges |
| B | Trust Recovery | 0.25 | 0.40 | 0.15 | Vertrauensaufbau (4 Dimensionen) |
| C | Growth Effectiveness | 0.25 | 0.20 | 0.25 | Kampagnen-Relevanz, Timing |
| D | Integration Comms | 0.15 | 0.15 | 0.10 | Migrations-Narrativ, Change Management |

**Baseline:** A = 0.32 (aktuell) → **Ziel:** A = 0.55 → **Gap:** +0.23

#### M1: Competitive Response Model (NEU)

**Formel:**

P(switch) = σ(α·ΔU_P + β·ΔU_F + γ·ΔU_I - δ·SC - ε·τ)

Wobei:
- ΔU_P = UX-Gap (Neobank vs. UBS App)
- ΔU_F = Kosten-Gap (Revolut Free vs. UBS Gebühren)
- ΔU_I = Identity-Gap («cool» vs. «traditionell»)
- SC = Switching Costs (Lastschriften, Hypothek, 3a, Lohn)
- τ = Trust Barrier (reguliert vs. unreguliert)

**Theoretische Fundierung:** MS-IB-001 (Identity Economics, Akerlof & Kranton 2000), MOD-SWITCH-001 (Neobank Switching Behavior)

#### M2: Budget Allocation Model (NEU)

**Optimierungsformel:**

max Σᵢⱼₖ ROI(seg_i, mod_j, chan_k) × B(i,j,k)

s.t. Σ B(i,j,k) ≤ B_total

Wobei:

ROI(i,j,k) = ΔA(i,j) × Conv(k) × LTV(i) × (1 + Σγ_compl)

- ΔA(i,j) = Activation Score Lift durch Modul j für Segment i
- Conv(k) = Konversionsrate von Kanal k
- LTV(i) = Customer Lifetime Value von Segment i
- γ_compl = Kanal-Komplementaritäten

#### M3: Trust Recovery Dynamics (NEU)

**Dynamisches Modell:**

τ(t+1) = τ(t) + α·Positive(t) - β·Negative(t) - δ·Decay(t)

Wobei:
- α = Trust-Aufbau-Rate: 0.02-0.04 pro positivem Kontakt (LANGSAM)
- β = Trust-Erosion-Rate: 0.08-0.15 pro negativem Event (SCHNELL)
- δ = Natürlicher Zerfall: ~0.01/Monat ohne Kontakt
- **Asymmetrie-Ratio:** β/α ≈ 3.5

**Theoretische Fundierung:** MS-SP-001 (Inequity Aversion, Fehr & Schmidt 1999), MS-SP-005 (Reciprocity), Bohnet & Zeckhauser (2004)

### 4.2 Modell-Integration

Die 4 Modelle interagieren:

- **M3** (Trust Dynamics) → speist Module B von GMA-001 mit τ(t) Trajektorie
- **M1** (Competitive Response) → quantifiziert die URGENCY (Churn-Risiko als Zeitdruck)
- **M2** (Budget Allocation) → optimiert die RESSOURCEN-VERTEILUNG

**Sequenz-Logik:**

1. Q1 2026: Trust Recovery starten (M3) + Churn stoppen (M1)
2. Q2 2026: Digital Activation skalieren (M2 → Mod A)
3. Q3 2026: Growth Effectiveness optimieren (M2 → Mod C)
4. Q4 2026: Integration Comms auslaufen lassen (Mod D) + Harvest (3a Peak)

---

\newpage

## 5. Parametrisierung und Validierung

### 5.1 Methodik: 3-stufige Parametrisierung

| Stufe | Methode | Quelle | Konfidenz |
|-------|---------|--------|-----------|
| 1. LLMMC Prior | LLM Monte Carlo Estimation | Literatur + Training Data | Mittel |
| 2. BCM2 Posterior | Bayesian Update | 60+ Schweizer Kontext-Faktoren | Hoch |
| 3. Monte Carlo | 10'000 Draws | Posterior-Verteilungen | Hoch |

### 5.2 Parameter-Matrix (BCM2-validiert)

| Parameter | LLMMC-Prior | BCM2-Posterior | Δ | Konfidenz |
|-----------|-------------|----------------|---|-----------|
| λ (Loss Aversion) | 1.6-3.4 | 1.8-3.2 | Eingeengt | HIGH |
| λ_Krise | — | 3.0-4.0 | NEU | HIGH |
| τ (Trust) | 0.30-0.85 | 0.35-0.75 | ↓0.10 | HIGH |
| τ_Benevolence Ex-CS | — | 0.45 | NEU | HIGH |
| β (Present Bias) | 0.60-0.88 | 0.65-0.85 | Eingeengt | MEDIUM |
| β_Stress | — | 0.40-0.60 | NEU | HIGH |
| κ (Default Sensitivity) | 0.40-0.90 | 0.78-0.90 | ↑0.38 | HIGH |
| κ_DE-CH | — | 0.88-0.90 | NEU (regional) | HIGH |
| κ_FR-CH | — | 0.75-0.80 | NEU (regional) | HIGH |
| σ (Social Proof) | 0.35-0.75 | 0.50-0.85 | ↑0.15 | HIGH |
| σ_Peers | — | 0.85 | NEU | HIGH |

**Grösste Korrektur:** Default Sensitivity (κ) von 0.40 auf 0.78 angehoben. Die BCM2-Daten zeigen, dass Schweizer:innen eine extrem hohe Default-Compliance haben (CH-REG-08 = 0.82-0.88). Dies war im LLMMC-Prior unterschätzt.

**Grösste Entdeckung:** Regionale Heterogenität DE-CH vs. FR-CH — durchgängig +10 Prozentpunkte bei κ, σ und λ_property in der Deutschschweiz.

### 5.3 Segment-spezifische Parameter

| Parameter | Legacy | Ex-CS | Digital | Affluent |
|-----------|--------|-------|---------|----------|
| λ | 1.8 | 2.2 | 1.6 | 2.1 |
| λ_Krise | 3.0 | 3.5 | 2.8 | 3.2 |
| τ | 0.75 | 0.55 | 0.65 | 0.72 |
| τ_Benevolence | 0.70 | 0.45 | 0.60 | 0.68 |
| β | 0.85 | 0.80 | 0.72 | 0.85 |
| κ | 0.85 | 0.82 | 0.80 | 0.78 |
| σ | 0.60 | 0.55 | 0.70 | 0.65 |
| σ_Peers | 0.75 | 0.70 | 0.85 | 0.80 |
| ε (Effort) | 0.55 | 0.60 | 0.80 | 0.45 |
| ι (Identity) | 0.75 | 0.40 | 0.50 | 0.70 |

### 5.4 Life Event Multiplikatoren

| Event | Multiplier | Timing Window | Bestes Segment |
|-------|------------|---------------|----------------|
| Erbschaft | ×2.5 | Jederzeit | Affluent (RM nötig) |
| 3a Deadline | ×2.2 | Dezember | Alle (Tax-driven) |
| Bonus/13. Monat | ×1.8 | Dez-Jan | Digital + Legacy |
| Immobilienkauf | ×1.6 | Jederzeit | Affluent + Legacy |
| Steuererklärung | ×1.5 | Feb-März | Alle |
| Fresh Start | ×1.5 | Bei Transition | Digital-Only |
| CS-Migration | ×1.35 | 90-Tage-Fenster | Ex-CS |

### 5.5 Monte Carlo Sensitivität

Die Monte-Carlo-Analyse (10'000 Draws) identifiziert die Parameter mit dem grössten Einfluss auf das Ergebnis:

**Für GMA-001 (Activation Score):**

| Parameter | Erklärte Varianz | Rang |
|-----------|-----------------|------|
| κ (Default) | 35% | 1 — HAUPTTREIBER |
| τ (Trust) | 26% | 2 |
| ε (Effort/UX) | 18% | 3 |
| σ (Social) | 12% | 4 |
| β (Present Bias) | 6% | 5 |
| Andere | 3% | — |

**Für M3 (Trust Recovery):**

| Parameter | Erklärte Varianz | Rang |
|-----------|-----------------|------|
| β/α Asymmetrie | 45% | 1 — HAUPTTREIBER |
| Fehler-Frequenz | 25% | 2 |
| Kontakt-Frequenz | 16% | 3 |
| Benevolence-Gap | 11% | 4 |
| Andere | 3% | — |

**Für M1 (Competitive Response):**

| Parameter | Erklärte Varianz | Rang |
|-----------|-----------------|------|
| SC (Switching Costs) | 38% | 1 — HAUPTTREIBER |
| τ (Trust) | 24% | 2 |
| ΔU_P (UX-Gap) | 16% | 3 |
| ΔU_F (Kosten-Gap) | 10% | 4 |
| ι (Identity) | 7% | 5 |
| Andere | 5% | — |

**Robustheit:** Die Ergebnisse sind stabil: In 95% der Monte-Carlo-Draws bleibt die Reihenfolge der Segment-Prioritäten gleich (Ex-CS > Digital > Legacy > Affluent nach Revenue-at-Risk).

---

\newpage

## 6. Ergebnisse: Activation Score Analyse

### 6.1 Activation Score pro Segment

| Segment | A_ist | A_ziel | Gap | Haupthebel |
|---------|-------|--------|-----|------------|
| Legacy (1.5M) | 0.38 | 0.58 | +0.20 | κ (Defaults) + Growth Mod C |
| Ex-CS (1.0M) | 0.25 | 0.55 | +0.30 | τ (Trust) + Mod B |
| Digital (0.8M) | 0.35 | 0.60 | +0.25 | ε (Friction↓) + Mod A |
| Affluent (0.4M) | 0.42 | 0.62 | +0.20 | RM × App Hybrid |
| **Gesamt (3.7M)** | **0.34** | **0.58** | **+0.24** | **Defaults (κ = 0.85)** |

### 6.2 Churn-Prognose pro Segment (M1)

| Segment | P(switch) | SC-Level | Haupttreiber | bLink-Effekt |
|---------|-----------|----------|--------------|--------------|
| Digital-Only | 25-35% | LOW (0.25) | UX + Identity | +8-12pp |
| CS-Migriert | 15-20% | LOW (0.35) | Trust-Defizit | +5-8pp |
| Legacy UBS | 5-8% | HIGH (0.75) | Kosten (sekundär) | +2-3pp |
| Affluent | 3-5% | HIGH (0.80) | Minimal (RM-Bindung) | +1-2pp |

**Kritisch:** SIX bLink senkt Switching Costs um ~30% für alle Segmente. Ohne Gegenmassnahmen steigt das Churn-Risiko um 8-12 Prozentpunkte im Digital-Only Segment.

### 6.3 Trust Recovery Trajektorie (M3)

Die Trust Recovery für das Ex-CS Segment folgt einer asymmetrischen Dynamik:

**Bei null Fehlern (BEST CASE, P = 0.20):**

| Monat | τ | Dimension mit grösstem Fortschritt |
|-------|---|------|
| 0 | 0.55 | Start |
| 3 | 0.62 | Competence + Predictability |
| 6 | 0.67 | Integrity beginnt zu wachsen |
| 9 | 0.72 | Benevolence messbar verbessert |
| 12 | 0.78 | Ziel übertroffen |

**Bei einem Fehler in Monat 4 (EXPECTED, P = 0.55):**

| Monat | τ | Event |
|-------|---|-------|
| 0-3 | 0.55→0.62 | Aufbau normal |
| 4 | 0.62→0.54 | Fehler: -0.08 (Rückfall!) |
| 5-8 | 0.54→0.62 | Recovery (4 Monate für Kompensation) |
| 9-12 | 0.62→0.70 | Ziel knapp erreicht |

**Bei zwei Fehlern (WORST CASE, P = 0.25):**

| Monat | τ | Event |
|-------|---|-------|
| 0-3 | 0.55→0.62 | Aufbau normal |
| 3 | 0.62→0.54 | Fehler 1 |
| 4-6 | 0.54→0.58 | Teilweise Recovery |
| 7 | 0.58→0.48 | Fehler 2 |
| 8-12 | 0.48→0.52 | Recovery unvollständig: UNTER STARTWERT! |

**Schlüsselerkenntnis:** Die Trust-Asymmetrie (β/α = 3.5) bedeutet, dass Fehler-Prävention 3.5× wirksamer ist als Trust-Aufbau. Die wichtigste Einzelmassnahme ist nicht eine Marketing-Kampagne, sondern ein Zero-Defect-Programm.

---

\newpage

## 7. Szenario-Analyse

### 7.1 Revenue Impact Waterfall

#### Worst Case (P = 0.25)

| Komponente | Impact |
|------------|--------|
| Basis Revenue | CHF 4'200M |
| − Legacy Churn (12%) | −CHF 150M |
| − Ex-CS Churn (30%) | −CHF 500M |
| − Digital Churn (45%) | −CHF 120M |
| − Affluent Churn (5%) | −CHF 60M |
| **= Revenue at Risk** | **−CHF 830M** |

#### Best Case (P = 0.20)

| Komponente | Impact |
|------------|--------|
| Basis Revenue | CHF 4'200M |
| + Legacy Activation (+8pp) | +CHF 80M |
| + Ex-CS Trust Recovery (+20pp) | +CHF 200M |
| + Digital Activation (+15pp) | +CHF 180M |
| + Affluent Deepening (+10pp) | +CHF 150M |
| **= Revenue Uplift** | **+CHF 610M** |

**Swing:** CHF 1.44 Milliarden zwischen Worst und Best Case.

### 7.2 Szenario-Zusammenfassung pro Segment

| Segment | Best (P) | Expected (P) | Worst (P) | Haupt-Risikofaktor |
|---------|----------|--------------|-----------|---------------------|
| Legacy | A=0.62 (0.20) | A=0.52 (0.55) | A=0.40 (0.25) | bLink + Passivität |
| Ex-CS | A=0.60 (0.15) | A=0.48 (0.50) | A=0.30 (0.35) | Trust-Fehler |
| Digital | A=0.68 (0.20) | A=0.55 (0.55) | A=0.38 (0.25) | Neobank-UX |
| Affluent | A=0.68 (0.25) | A=0.58 (0.50) | A=0.45 (0.25) | RM-Kapazität |

### 7.3 Monte Carlo Konfidenzintervalle

| Metrik | Punkt-Schätzung | 68% CI | 95% CI |
|--------|----------------|--------|--------|
| A_Gesamt (12 Monate) | 0.52 | [0.45, 0.58] | [0.38, 0.64] |
| τ_Ex-CS (12 Monate) | 0.68 | [0.60, 0.74] | [0.50, 0.78] |
| Churn_Digital (12 Monate) | 22% | [16%, 28%] | [11%, 38%] |
| Revenue Impact | +CHF 280M | [+140M, +420M] | [−50M, +610M] |

---

\newpage

## 8. Wettbewerbs-Benchmarks

### 8.1 Schweizer Banking Landscape

| Metrik | UBS | Raiffeisen | ZKB | PostFinance | Revolut |
|--------|-----|-----------|-----|------------|---------|
| NPS | 38 | 48 | 42 | 25 | ~55 |
| Trust (τ) | 0.75 | 0.85 | 0.90 | 0.78 | 0.55 |
| Digital Active | 78% | 72% | 38% | 80% | 100% |
| Churn Rate | 4% | 2.5% | 6% | 4% | 15% |
| Kund:innen (M) | 3.5 | 3.71 | 1.45 | 2.5 | 0.9 |
| Filialen CH | 200 | 779 | 80 | 16 | 0 |

### 8.2 UBS-Gaps

1. **NPS:** 38 vs. Raiffeisen 48 (−10pp) vs. Revolut ~55 (−17pp)
2. **Trust:** 0.75 vs. ZKB 0.90 (−0.15) vs. Raiffeisen 0.85 (−0.10)
3. **Churn:** 4% vs. Raiffeisen 2.5% (1.6× höher)
4. **App-UX:** Friction 0.60 vs. Revolut ~0.15 (4× schlechter)

### 8.3 UBS-Stärken

1. **Wealth Management:** Einziger globaler Player aus der Schweiz (USD 6.1T AuM)
2. **Produktbreite:** 5'000 Anlageprodukte, 150 Mandate-Lösungen
3. **RM-Conversion:** 3.5× höher als Digital → Affluent-Moat
4. **AI/Data:** 300+ Use Cases, USD 6.5B IT-Budget → Tech-Leader
5. **Scale:** 3.5M CH-Kund:innen (Post-CS) → grösstes Netzwerk

### 8.4 Strategische Positionierung

UBS kann NICHT auf Trust/Community (Raiffeisen/ZKB) oder UX (Revolut) allein konkurrieren. Der Moat liegt in:

- **Wealth Management Excellence** (nicht kopierbar kurzfristig)
- **Behavioral Science Capability** (keine Schweizer Bank hat EBF-Niveau)
- **Convenience + Defaults** (Scale ermöglicht Personalisierung)
- **RM-Beziehung** (Affluent-Segment, 3.5× Conversion)

---

\newpage

## 9. Interventions-Design

### 9.1 Die 4 No-Regret Moves

#### No-Regret Move #1: Default-Architektur

**10C-Target:** WHEN (V) → κ_KON (Kontext-bedingte Default-Sensitivität)

**Massnahmen:**

a) **3a-Auto-Invest:** Bei Kontoeröffnung wird 3a mit Default-Portfolio vorselektiert (Opt-Out statt Opt-In). Expected: +12-15pp Adoption.

b) **One-Click Invest:** Salary-Deposit-Triggered. «CHF 500 auf Ihr Anlagekonto?» → Default: JA, 1 Tap. Expected: +8-10pp.

c) **Bonus-Allokator:** Bei Bonus-Eingang automatischer Vorschlag. Expected: ×1.8 Life Event Multiplier × κ = 0.85.

**Kosten:** CHF 2-5M (App-Update) | **Revenue Impact:** +CHF 80-120M | **ROI:** 20-60×

#### No-Regret Move #2: Fehler-Prävention (Ex-CS)

**10C-Target:** HOW (B) → Trust Asymmetrie

**Massnahmen:**

a) **CS-Migration Monitoring Dashboard:** Real-time Alerts für Systemausfälle, Fehlbuchungen, Verzögerungen. Ziel: 0 unkontrollierte Fehler in 12 Monaten.

b) **Proaktive Entschuldigung:** Bei JEDEM Fehler innerhalb 2 Stunden persönliche Nachricht + Kompensation. τ_recovery: +0.04 statt −0.08.

c) **Weekly Consistency Signal:** Jeden Freitag kurze «Alles läuft»-Nachricht an Ex-CS. τ_predictability: +0.03/Monat.

**Kosten:** CHF 5-10M | **Revenue Impact:** +CHF 200-500M (Revenue Protected) | **ROI:** 20-50×

#### No-Regret Move #3: App-Friction Reduktion

**10C-Target:** READY (AV) → ε↓

**Massnahmen:**

a) **Invest-Tab:** Maximal 3 Taps von Home zum ersten Investment (aktuell 7 Taps).

b) **Micro-Learning Carousel:** 30-Sekunden Finanz-Snippets im Feed (Instagram-Style).

c) **Social Proof Badge:** «85% deiner Altersgruppe investieren» — NICHT kombinieren mit Cash Bonus!

**Kosten:** CHF 8-15M | **Revenue Impact:** +CHF 75-120M | **ROI:** 5-15×

#### No-Regret Move #4: Life Event Triggered Marketing

**10C-Target:** WHEN (V) → κ_JNY (Journey Timing)

**Event-Trigger-Matrix:**

| Trigger | Aktion | Kanal | Multiplier |
|---------|--------|-------|------------|
| Salary Deposit | Invest-Nudge | Push | ×1.3 |
| Bonus (>5k) | 3a + Anlage-Split | Push+Email | ×1.8 |
| 3a Deadline (Nov) | Urgency-Countdown | App+Email | ×2.2 |
| Erbschaft (>50k) | RM-Kontakt (48h!) | RM-Call | ×2.5 |
| Immobilienkauf | Hypothek-Cross-Sell | RM+Branch | ×1.6 |
| CS-Migration abgeschlossen | Welcome-Journey | Omni | ×1.35 |

**Kosten:** CHF 3-8M | **Revenue Impact:** +CHF 60-100M | **ROI:** 8-33×

### 9.2 Komplementaritäten und Synergien

**Positive Komplementaritäten (γ > 0):**

| Kombination | γ | Effekt |
|-------------|---|--------|
| APP × RM-Kontakt | +0.25 | Hybrid > Einzelkanal |
| Social Proof × Education | +0.20 | Wissen + Norm = Konfidenz |
| Default × Life Event | +0.15 | Timing + κ = Maximum |
| Consistency × Time | +0.10 | Je länger, desto τ↑ |

---

\newpage

## 10. Roadmap Q1-Q4 2026

### Q1 (Januar-März): DEFEND & STABILIZE

**Fokus:** Trust Recovery starten + Churn stoppen + Defaults deployen

| Segment | Intervention | KPI |
|---------|-------------|-----|
| Ex-CS (1.0M) | #2 Fehler-Prävention starten | 0 Fehler |
| | Weekly Consistency Signals | τ: 0.55→0.60 |
| Digital (0.8M) | Bonus-Aktivierung (Jan Peak!) | +5pp Invest |
| | Steuer-Awareness (Feb-Mär) | 3a +3pp |
| Alle | #1 Default-Architektur (Sprint) | κ deployed |

**Budget-Split:** Trust 40% | Digital 35% | Defaults 25%

### Q2 (April-Juni): ACTIVATE & LEARN

**Fokus:** App-Friction senken + Benevolence-Kampagne + Growth starten

| Segment | Intervention | KPI |
|---------|-------------|-----|
| Digital (0.8M) | #3 App-Friction↓ (v1 Release) | ε: 0.60→0.45 |
| | Micro-Learning Launch | A: +0.15 |
| Ex-CS (1.0M) | Benevolence-Kampagne starten | τ_B: +0.05 |
| Legacy (1.5M) | Growth Effectiveness (Mod C) | Cross-sell +3% |
| Affluent (0.4M) | RM×App Hybrid-Test (Pilot) | Conv. +10% |

**Budget-Split:** Digital 40% | Trust 25% | Growth 25% | Test 10%

### Q3 (Juli-September): SCALE & OPTIMIZE

**Fokus:** Social Proof skalieren + Life Event Engine launchen + RM-Hybrid ausrollen

| Segment | Intervention | KPI |
|---------|-------------|-----|
| Digital (0.8M) | Social Proof Badge (Scale) | σ-Impact |
| | App-Friction v2 (3→2 Taps) | ε: 0.45→0.30 |
| Legacy (1.5M) | #4 Life Event Engine (Launch) | Event-Conv. |
| Ex-CS (1.0M) | Integrity Messaging (Scale) | τ_I: +0.08 |
| Affluent (0.4M) | RM×App Scale (aus Pilot) | Conv. +15% |

**Budget-Split:** Scale 45% | Digital 30% | Trust 15% | Optimize 10%

### Q4 (Oktober-Dezember): HARVEST & PREPARE

**Fokus:** 3a-Peak nutzen + Erfolg messen + 2027 planen

| Segment | Intervention | KPI |
|---------|-------------|-----|
| Alle | 3a-PEAK (Nov-Dez: ×2.2!) | 3a: +15pp |
| | Bonus-Allokator (Dez-Jan) | Invest: +8pp |
| Ex-CS (1.0M) | Trust-Messung (τ Ziel ≥0.70?) | τ ≥ 0.70 |
| Digital (0.8M) | Churn-Messung (bLink-Impact?) | Churn < 20% |
| Affluent (0.4M) | Year-End-Review + Deepening | Multi-Prod +5% |

**Budget-Split:** Harvest 50% | Measurement 20% | 2027 Prep 30%

---

\newpage

## 11. Budget und ROI

### 11.1 Investment-Übersicht

| # | Move | Kosten | Revenue Impact | ROI |
|---|------|--------|---------------|-----|
| 1 | Default-Architektur | CHF 2-5M | +CHF 80-120M | 20-60× |
| 2 | Fehler-Prävention | CHF 5-10M | +CHF 200-500M | 20-50× |
| 3 | App-Friction↓ | CHF 8-15M | +CHF 75-120M | 5-15× |
| 4 | Life Event Engine | CHF 3-8M | +CHF 60-100M | 8-33× |
| | **TOTAL** | **CHF 18-38M** | **+CHF 415-840M** | **11-46×** |

### 11.2 Vergleich: Behavioral vs. Traditional Marketing

| Dimension | Behavioral Marketing | Traditional Marketing |
|-----------|---------------------|----------------------|
| Typischer ROI | 10-40× | 3-5× |
| Kosten pro Intervention | CHF 2-15M | CHF 20-50M |
| Wirkungseintritt | 1-3 Monate | 6-12 Monate |
| Messbarkeit | Hoch (A/B-testbar) | Mittel (Attribution-Problem) |
| Skalierbarkeit | Sehr hoch (digital) | Begrenzt (Mediakosten) |
| Crowding-Out-Risiko | Dokumentiert (γ-Werte) | Nicht systematisch erfasst |

### 11.3 Budget-Kontext

- **UBS Marketing-Budget (geschätzt):** CHF 280-570M
- **Behavioral Marketing Anteil:** CHF 18-38M = 3-14% des Gesamtbudgets
- **ROI:** 11-46× → überproportionaler Return bei unterproportionalem Investment
- **C/I Beitrag:** Behavioral Marketing senkt Cost-to-Income, da niedrigere Kosten pro aktiviertem Kunden

---

\newpage

## 12. Risiken und Crowding-Out

### 12.1 Verbotene Kombinationen

| Kombination | γ | Risiko | Alternative |
|-------------|---|--------|------------|
| Social Proof + Cash Bonus | −0.30 | Bonus zerstört Norm | Social Proof allein |
| Erbschaft + Financial Incentive | −0.40 | Pietäts-Verletzung | Empathische RM-Begleitung |
| Motivierter Kunde + Geld-Anreiz | −0.40 | Intrinsische Motivation↓ | Convenience zeigen |
| Fear-Messaging + Low-Trust Segment | 2.7/5.0 | Reaktanz | Peer-Empfehlung |

### 12.2 Operationelle Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|--------------------|---------| ----------|
| IT-Ausfall bei Ex-CS | Mittel | τ −0.15 (katastrophal) | Zero-Defect-Programm |
| bLink-Launch früher als erwartet | Niedrig | Churn +12pp | Retention-Massnahmen vorziehen |
| RM-Kapazitätsengpass | Hoch | Affluent A↓ | Digital-Hybrid statt nur RM |
| Regulatorische Einschränkung (Defaults) | Niedrig | Default-Move blockiert | Opt-Out-Compliance prüfen |
| Neobank-Preiskampf (Revolut) | Hoch | Digital Churn ↑ | UX + Value statt Preis |

### 12.3 Trust-spezifische Risiken

Die Trust-Asymmetrie (β/α = 3.5) macht das Ex-CS Segment extrem fragil:

- **1 unkontrollierter Fehler:** 4 Monate Rückschlag, P(τ>0.70 in 12M) sinkt von 0.78 auf 0.31
- **2 Fehler:** Recovery gefährdet, P(τ>0.70) = 0.08 — praktisch unmöglich
- **Kommunikations-Fehler:** Ein als «aggressiv» wahrgenommenes Upselling an Ex-CS kann Trust zerstören

**Eskalationsregel:** Bei τ_Ex-CS < 0.50 oder Churn_Digital > 35% → Krisenmodus mit Executive Attention.

---

\newpage

## 13. KPIs und Erfolgsmessung

### 13.1 Primäre KPIs

| KPI | Ist (Q1/26) | Ziel (Q4/26) | Messmethode |
|-----|-------------|--------------|-------------|
| Activation Score (A) | 0.34 | 0.55 | Composite Index |
| τ Ex-CS | 0.55 | ≥0.70 | Survey + NPS |
| NPS (Gesamt) | 38 | 45 | Quartals-Survey |
| Churn Digital-Only | ~30% | <20% | Konten-Tracking |
| 3a-Penetration | 5% | 17-20% | Produktdaten |
| App-Friction | 0.60 | ≤0.35 | UX-Testing |
| Invest-Activation Rate | 5% | 13-17% | Konten-Tracking |
| Revenue Uplift | Basis | +CHF 200M+ | P&L Attribution |
| Fehler (Ex-CS) | — | 0 unkontrolliert | Incident-Log |
| Campaign ROI | ~3-5× | 10-20× | Marketing-Attribution |

### 13.2 Review-Zyklus

- **Wöchentlich:** Trust-Indikatoren (Ex-CS), Fehler-Log, App-Metrics
- **Monatlich:** KPI-Dashboard, Segment-Performance, Budget-Tracking
- **Quartalsweise:** Deep-Dive mit Szenario-Update, Roadmap-Anpassung
- **Halbjährlich:** Wettbewerbs-Benchmark-Update, Modell-Rekalibrierung

---

\newpage

## 14. Schlussfolgerungen und Empfehlungen

### 14.1 Die 3 wichtigsten Empfehlungen

**1. Defaults vor allem anderen.**

Die Schweizer Default-Compliance (κ = 0.85) ist der mächtigste und kostengünstigste Hebel. Opt-Out-3a, One-Click-Invest und Bonus-Allokator kosten zusammen CHF 2-5M und generieren CHF 80-120M. Dies ist der höchste ROI aller Massnahmen (20-60×) und wirkt über alle Segmente hinweg.

**Empfehlung:** Sprint in Q1 2026, Deployment vor März.

**2. Fehler verhindern ist wichtiger als Vertrauen aufbauen.**

Die Trust-Asymmetrie (β/α = 3.5) bedeutet: 1 Fehler braucht 4 positive Kontakte. Im Ex-CS-Segment (CHF 500M Revenue at Risk) ist Fehler-Prävention 3.5× wirksamer als Trust-Aufbau. Das Zero-Defect-Programm ist keine IT-Massnahme — es ist die wichtigste Marketing-Investition des Jahres.

**Empfehlung:** Sofort starten, Executive Sponsorship, wöchentliches Reporting.

**3. Behavioral Marketing ist der UBS-Unique-Advantage.**

Keine andere Schweizer Bank hat EBF-Niveau Behavioral Science Capability. Bei CHF 18-38M Investment und CHF 415-840M Return (10-40× ROI) ist Behavioral Marketing die höchste ROI-Investition im gesamten Marketing-Portfolio — und gleichzeitig ein nachhaltiger Wettbewerbsvorteil.

**Empfehlung:** Behavioral Marketing als strategische Kernkompetenz positionieren, nicht als Projekt.

### 14.2 Nächste Schritte

1. **Woche 1-2:** Default-Architektur Sprint planen (Product + UX + Legal)
2. **Woche 1:** Zero-Defect-Programm für Ex-CS aufsetzen (IT + Operations)
3. **Woche 3-4:** App-Friction Audit und v1 Spezifikation (Product + UX)
4. **Monat 2:** Life Event Engine Architektur (Data + Marketing Automation)
5. **Monat 3:** Pilot Launch (Digital-Only Segment, Deutschschweiz)

---

\newpage

## Anhang A: Vollständige Parameter-Tabellen

### A.1 Segment × Parameter Matrix

| Parameter | Legacy | Ex-CS | Digital | Affluent | Quelle |
|-----------|--------|-------|---------|----------|--------|
| λ (Loss Aversion) | 1.8 | 2.2 | 1.6 | 2.1 | BCM2 + LLMMC |
| λ_Krise | 3.0 | 3.5 | 2.8 | 3.2 | Ψ_C Dimension |
| τ (Trust) | 0.75 | 0.55 | 0.65 | 0.72 | BCM2 CH-HUM-02 |
| τ_Competence | 0.80 | 0.70 | 0.70 | 0.78 | UBS-Daten |
| τ_Predictability | 0.75 | 0.55 | 0.65 | 0.72 | UBS-Daten |
| τ_Integrity | 0.75 | 0.50 | 0.65 | 0.72 | UBS-Daten |
| τ_Benevolence | 0.70 | 0.45 | 0.60 | 0.68 | UBS-Daten |
| β (Present Bias) | 0.85 | 0.80 | 0.72 | 0.85 | BCM2 CH-ECO-09 |
| κ (Default) | 0.85 | 0.82 | 0.80 | 0.78 | BCM2 CH-REG-08 |
| σ (Social Proof) | 0.60 | 0.55 | 0.70 | 0.65 | BCM2 CH-REG-09 |
| σ_Peers | 0.75 | 0.70 | 0.85 | 0.80 | Ψ_S Dimension |
| ε (Effort Sensitivity) | 0.55 | 0.60 | 0.80 | 0.45 | UBS-Daten |
| ι (Identity/Brand) | 0.75 | 0.40 | 0.50 | 0.70 | UBS-Daten |

### A.2 Persona × Parameter Matrix

| Parameter | Sandra | Thomas | Leila | Marco | Nina | Peter | Julia |
|-----------|--------|--------|-------|-------|------|-------|-------|
| λ | 2.9 | 3.1 | 2.6 | 1.7 | 1.9 | 3.4 | 2.8 |
| β | 0.72 | 0.80 | 0.68 | 0.88 | 0.82 | 0.62 | 0.60 |
| κ | 0.85 | 0.75 | 0.82 | 0.40 | 0.55 | 0.90 | 0.80 |
| σ | 0.60 | 0.45 | 0.70 | 0.35 | 0.50 | 0.65 | 0.75 |
| τ | 0.55 | 0.60 | 0.45 | 0.30 | 0.40 | 0.35 | 0.50 |
| ε | 0.75 | 0.65 | 0.80 | 0.50 | 0.85 | 0.70 | 0.90 |

---

\newpage

## Anhang B: Monte Carlo Ergebnisse

### B.1 Sensitivitätsanalyse: Parameter-Einfluss auf Activation Score

| Parameter | Erklärte Varianz | Interpretation |
|-----------|-----------------|----------------|
| κ (Default) | 35% | Universeller Haupthebel |
| τ (Trust) | 26% | Segmentspezifisch (Ex-CS) |
| ε (Effort/UX) | 18% | Digital-Only dominant |
| σ (Social) | 12% | Verstärker für andere |
| β (Present Bias) | 6% | Life Events kompensieren |
| Andere | 3% | — |

### B.2 Konfidenzintervalle (10'000 Draws)

| Metrik | Punkt | 68% CI | 95% CI |
|--------|-------|--------|--------|
| A_Gesamt (12M) | 0.52 | [0.45, 0.58] | [0.38, 0.64] |
| τ_Ex-CS (12M) | 0.68 | [0.60, 0.74] | [0.50, 0.78] |
| Churn_Digital (12M) | 22% | [16%, 28%] | [11%, 38%] |
| Revenue Impact | +CHF 280M | [+140M, +420M] | [−50M, +610M] |

### B.3 Robustheit

In 95% der Monte-Carlo-Draws bleibt:
- Default-Architektur als #1 Hebel
- Trust Recovery als #2 für Ex-CS
- App-Friction als #3 für Digital
- Die Segment-Priorisierung (Ex-CS > Digital > Legacy > Affluent nach Revenue-at-Risk)

---

\newpage

## Anhang C: BCM2 Kontext-Faktoren

### C.1 Verwendete Schweizer Kontext-Faktoren

| Faktor-ID | Name | Wert 2024 | Trend | Relevanz |
|-----------|------|-----------|-------|----------|
| CH-REG-06 | Eigentumskonzept | 0.78 (DE-CH) | Stabil | λ bei Vermögen |
| CH-REG-08 | Default-Compliance | 0.82-0.88 | Steigend | κ Hauptquelle |
| CH-REG-09 | Soziale-Normen-Compliance | 0.78 (DE-CH) | Stabil | σ Validierung |
| CH-HUM-02 | Generalisiertes Vertrauen | 6.0/10 | Fallend | τ Makro-Trend |
| CH-ETH-02 | Integritätserwartung | 82.4% | Steigend | Messaging-Fokus |
| CH-MED-01 | Medienvertrauen | 46.8% | Stark fallend | Kanal-Strategie |
| CH-ECO-09 | Sparquote | 18.2% | Steigend | β Indikator |
| CH-ECO-10 | Anlagequote | 45.2% | Steigend | Marktpotenzial |

### C.2 Regionale Differenzierung

| Parameter | DE-CH | FR-CH | Gap | Implikation |
|-----------|-------|-------|-----|-------------|
| κ (Default) | 0.88 | 0.78 | +10pp | Stärkere Defaults in DE-CH |
| σ (Soziale Normen) | 0.78 | 0.68 | +10pp | Social Proof effektiver in DE-CH |
| λ_property | 0.78 | 0.68 | +10pp | Höhere Loss Aversion bei Vermögen in DE-CH |

---

\newpage

## Anhang D: Literaturverzeichnis

### Kernliteratur (direkt parametrisierend)

- Akerlof, G.A. & Kranton, R.E. (2000). Economics and Identity. *Quarterly Journal of Economics*, 115(3), 715-753.
- Bohnet, I. & Zeckhauser, R. (2004). Trust, Risk and Betrayal. *Journal of Economic Behavior & Organization*, 55(4), 467-484.
- Fehr, E. & Schmidt, K.M. (1999). A Theory of Fairness, Competition, and Cooperation. *Quarterly Journal of Economics*, 114(3), 817-868.
- Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. *Econometrica*, 47(2), 263-291.
- Klemperer, P. (1987). Markets with Consumer Switching Costs. *Quarterly Journal of Economics*, 102(2), 375-394.
- Laibson, D. (1997). Golden Eggs and Hyperbolic Discounting. *Quarterly Journal of Economics*, 112(2), 443-478.
- Madrian, B.C. & Shea, D.F. (2001). The Power of Suggestion. *Quarterly Journal of Economics*, 116(4), 1149-1187.
- Thaler, R.H. & Sunstein, C.R. (2008). *Nudge: Improving Decisions about Health, Wealth, and Happiness*. Yale University Press.

### Erweiterte Literatur (85+ Papers)

Vollständige Literaturliste verfügbar in der EBF-Bibliographie (`bibliography/bcm_master.bib`, 2'634 Einträge).

---

\newpage

## Anhang E: Methodik

### E.1 EBF-Workflow

Das Evidence-Based Framework (EBF) folgt einem standardisierten 9-Schritt-Workflow:

1. **Schritt 0:** Session initialisieren (Domain, Modus)
2. **Schritt 1:** Kontext verstehen (8 Ψ-Dimensionen)
3. **Schritt 2:** Modell auswählen (Registry + Theory Catalog)
4. **Schritt 3:** Parameter bestimmen (LLMMC → BCM2 → Monte Carlo)
5. **Schritt 4:** Analyse & Antwort
6. **Schritt 5:** Intervention designen (bei Verhaltenszielen)
7. **Schritt 6:** Bericht erstellen
8. **Schritt 7:** Ergebnisse sichern
9. **Schritt 8:** Qualität prüfen
10. **Schritt 9:** Output wählen

### E.2 LLMMC (LLM Monte Carlo Estimation)

LLMMC generiert informierte Priors auf Basis von:
- Training Data (wissenschaftliche Literatur)
- Kontext-Analogien (ähnliche Situationen)
- Unsicherheitsquantifizierung (explizite Ranges)

Diese Priors werden dann via Bayesian Updating mit BCM2-Daten (empirische Schweizer Kontext-Faktoren) zu Posteriors verfeinert.

### E.3 BCM2-Kontextdatenbank

Die BCM2-Datenbank enthält 404 Schweizer Kontext-Faktoren in 5 Kategorien:
- Demografisch (60 Faktoren)
- Ökonomisch (54 Faktoren)
- Institutionell-Politisch (59 Faktoren)
- Technologisch-Ökologisch (65 Faktoren)
- Sozio-Kulturell (166 Faktoren)

Alle Faktoren haben Quellenangaben (BFS, ESS, WVS, FehrAdvice-Studien) und Trend-Projektionen bis 2040.

### E.4 Monte Carlo Simulation

10'000 Draws aus den Posterior-Verteilungen aller Parameter, mit Korrelationsstruktur basierend auf empirischen Kovarianz-Matrizen. Sensitivitätsanalyse via Variance Decomposition (Sobol Indices).

---

*Erstellt mit dem Evidence-Based Framework (EBF) | FehrAdvice & Partners AG*
*Session: EBF-S-2026-02-13-FIN-001 | Alle Rechte vorbehalten*
