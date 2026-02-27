# HHH Cross-Reference Roadmap

> Systematische Integration von Appendix TKT (METHOD-TOOLKIT) ins EBF Framework

---

## Executive Summary

Appendix TKT (Intervention Design Toolkit) ist ein **zentraler Methodologie-Appendix** mit Impact auf:
- Alle 8 CORE Appendices (10C)
- Alle METHOD Appendices (EEE, FFF, GGG, AN, R)
- Alle DOMAIN Appendices (Anwendungskontexte)
- FORMAL Appendices (mathematische Fundierung)

Die vollständige Integration erfordert **bidirektionale Links** in ~25 Appendices.

---

## Phase 1: CORE Appendices (10C) — KRITISCH

### 1.1 B (CORE-HOW: Complementarity) ↔ HHH

**Problem:** γ_ij Complementarity ist ZENTRAL für HHH Axiom HHH-A4, aber B referenziert HHH nicht.

**Änderungen in B:**
```latex
% In Cross-Reference Map hinzufügen:
\textbf{HHH} & Intervention Design & $\gamma_{ij}$ for portfolios & \cellcolor{red!20}Strong
```

**Änderungen in HHH:**
```latex
% In Axiom HHH-A4 explizit verlinken:
where $\gamma_{ij}$ is the complementarity coefficient from Appendix UNMAPPED_HOW (CORE-HOW, Definition B.3)
```

**Neue Tabelle in B:** "Intervention-Complementarity Matrix"
| Type i | Type j | γ_ij | Evidence |
|--------|--------|------|----------|
| Normative | Incentive | -0.3 | Crowding Out |
| Default | Escalation | +0.6 | Thaler & Benartzi |
| Feedback | Social Norm | +0.5 | Allcott 2011 |

---

### 1.2 C (CORE-WHAT: FEPSDE) ↔ HHH

**Problem:** C definiert 6 FEPSDE-Dimensionen, HHH nutzt sie in F5, aber kein Link.

**Änderungen in C:**
```latex
% Neue Section hinzufügen:
\subsection{FEPSDE × Intervention Design}
Field F5 in Appendix TKT (METHOD-TOOLKIT) specifies which FEPSDE dimension(s)
an intervention targets. The mapping:
- F (Financial) → Incentive-based interventions (Type 4)
- E (Emotional) → Identity-based interventions (Type 7)
- P (Physical) → Structural interventions (Type 3)
- S (Social) → Normative interventions (Type 2)
- D (Digital) → Feedback interventions (Type 6)
- E (Ecological) → Multi-mechanism (Type 9)
```

---

### 1.3 AAA (CORE-WHO: Levels) ↔ HHH

**Problem:** AAA definiert Welfare-Levels, HHH nutzt sie in F3, aber disconnected.

**Änderungen in AAA:**
```latex
% Cross-Reference Map erweitern:
\textbf{HHH} & F3 Context Level & L-specific interventions & Strong

% Neue Section:
\subsection{Interventions by Welfare Level}
Appendix TKT Field F3 (Context Level) maps directly to AAA welfare levels:
- L_Individual → Individual-targeted interventions
- L_Family → Household interventions
- L_Organization → Workplace interventions
- L_State → Policy interventions
- L_Global → International coordination
```

---

### 1.4 BBB (CORE-WHERE: Parameters) ↔ HHH

**Problem:** BBB enthält keine Interventions-Parameter (σ_s, γ_ij Schätzwerte).

**Änderungen in BBB:**
```latex
% Neue Section:
\section{Intervention Effectiveness Parameters}

\subsection{Segment Multipliers $\sigma_s$}
% Table: σ_s by segment and intervention type
\begin{table}
\caption{Segment-Specific Effectiveness Multipliers}
\begin{tabular}{lccccc}
Segment & Informative & Normative & Structural & Incentive & Commitment \\
Social-oriented & 0.8 & 1.6 & 1.0 & 0.7 & 1.2 \\
Autonomy-seekers & 1.0 & -0.3 & 0.8 & 1.4 & 0.5 \\
Present-biased & 0.6 & 0.9 & 1.4 & 0.8 & 1.8 \\
\end{tabular}
\end{table}

\subsection{Complementarity Coefficients $\gamma_{ij}$}
% Reference to B, actual values from meta-analyses
See Appendix UNMAPPED_HOW Table B.7 for calibrated values.
```

---

### 1.5 AU, AV, AW (CORE-AWARE/READY/STAGE) ↔ HHH

**Problem:** Diese 3 COREs sind bereits verlinkt, aber Rück-Referenzen fehlen.

**Änderungen in AU:**
```latex
% Add in Cross-Reference Map:
\textbf{HHH} & Intervention Design & A(·) as intervention target & Medium
```

**Änderungen in AV:**
```latex
% Add:
\textbf{HHH} & Intervention Design & WAX determines F6 phase & Strong
```

**Änderungen in AW:**
```latex
% Add section:
\subsection{Journey-Intervention Alignment (Link to HHH)}
Appendix TKT Axiom HHH-A3 formalizes the critical alignment between
intervention type and journey phase. The mapping:

\begin{table}
\caption{Optimal Intervention Types by Journey Phase}
\begin{tabular}{lll}
Phase & Optimal Types & Suboptimal Types \\
Awareness & Informative (1) & Commitment (5), Stabilizer \\
Trigger & Normative (2), Structural (3) & Informative (redundant) \\
Action & Feedback (6), Incentive (4) & Awareness interventions \\
Maintenance & Commitment (5), Feedback (6) & Door-openers \\
Stabilization & Identity (7), Social norm & All non-identity \\
\end{tabular}
\end{table}
```

---

## Phase 2: METHOD Appendices

### 2.1 EEE (METHOD-DESIGN) ↔ HHH

**Problem:** 9-Step Workflow endet mit Output, aber Intervention-Design als Step fehlt.

**Änderungen in EEE:**
```latex
% Step 9 erweitern oder Step 10 hinzufügen:
\subsection{Step 10: Intervention Design (Optional)}
For models requiring behavioral change interventions:
→ Use Appendix TKT (METHOD-TOOLKIT) 20-field schema
→ Apply 3+1 Choice Architecture for intervention selection
→ Check Axioms HHH-A1 to HHH-A5 for design validation
```

---

### 2.2 FFF (METHOD-REGISTRY) ↔ HHH

**Problem:** FFF speichert Modelle, aber keine Interventions-Templates.

**Änderungen in FFF:**
```latex
% Neue Registry-Kategorie:
\section{Intervention Template Registry}

\subsection{Seed Interventions (DACH-Validated)}
\begin{table}
\caption{Pre-Validated Intervention Templates}
\begin{tabular}{llll}
ID & Name & Type & Domain \\
INT-001 & Auto-Enrollment Default & Structural (3) & Retirement \\
INT-002 & Social Norm Energy Report & Normative (2) & Energy \\
INT-003 & Commitment Savings Contract & Commitment (5) & Finance \\
\end{tabular}
\end{table}
```

---

### 2.3 GGG (METHOD-CONFIG) ↔ HHH

**Problem:** GGG hat 7 Mapping Tables, aber keine Intervention-Defaults.

**Änderungen in GGG:**
```latex
% Neue Table 8:
\section{Table 8: Intervention Defaults by Domain}

\begin{table}
\caption{Domain → Intervention Type Mapping}
\begin{tabular}{lll}
Domain & Primary Types & Secondary Types \\
Health & Commitment (5), Feedback (6) & Informative (1) \\
Finance & Structural (3), Commitment (5) & Incentive (4) \\
Environment & Normative (2), Feedback (6) & Identity (7) \\
Workplace & Structural (3), Normative (2) & Feedback (6) \\
\end{tabular}
\end{table}
```

---

## Phase 3: FORMAL Appendices

### 3.1 BB (FORMAL-EQUILIBRIA) ↔ HHH

**Problem:** BB formalisiert I(t) Intervention, aber Schema-Link fehlt.

**Änderungen in BB:**
```latex
% In Section on Intervention:
\subsection{Intervention Specification via HHH Schema}
Each intervention $I(t)$ in the equilibrium model corresponds to a
fully-specified intervention tuple $\mathcal{I}$ from Appendix TKT:
$$I(t) = E(\mathcal{I}) \cdot \mathbb{1}[t \in \text{active period}]$$
where $E(\mathcal{I})$ is effectiveness from HHH Equation (3).
```

---

### 3.2 BA (FORMAL-SEGMENT) ↔ HHH

**Problem:** BA definiert Segmente, HHH nutzt F9, aber kein expliziter Link.

**Änderungen in BA:**
```latex
% Add:
\subsection{Segment-Intervention Interface}
Field F9 in Appendix TKT references segment IDs defined in this appendix.
The segment multiplier $\sigma_s(\mathcal{I})$ from HHH Axiom HHH-A5
depends on segment parameters defined here.
```

---

## Phase 4: DOMAIN Appendices (Examples)

Jeder DOMAIN-Appendix sollte eine "Intervention Applications" Section haben:

### Template für DOMAIN-Appendices:
```latex
\section{Intervention Applications}

\subsection{Typical Interventions in [Domain]}
\begin{table}
\caption{Domain-Specific Intervention Examples}
\begin{tabular}{llll}
Intervention & HHH Type & Evidence & Effect Size \\
[Intervention 1] & Type X & [Citation] & [d = X.XX] \\
[Intervention 2] & Type Y & [Citation] & [d = X.XX] \\
\end{tabular}
\end{table}

\textbf{Cross-Reference:} For systematic design, use Appendix TKT (METHOD-TOOLKIT).
```

---

## Phase 0: CHAPTER 15 INTEGRATION — HÖCHSTE PRIORITÄT

### Der Integrations-Hub

Chapter 15 (Willingness to Effectively Change) ist das **Herzstück** des EBF Frameworks.
Die WEC-Funktion integriert ALLE Komponenten:

```
WEC = (WAX - θ) × α_BCJ × β_BCS

     ↑         ↑       ↑       ↑
     │         │       │       └── HHH Axiom HHH-A5 (Segment Specificity)
     │         │       └────────── HHH Axiom HHH-A3 (Journey Alignment)
     │         └────────────────── HHH Field F6 (Journey Phase)
     └──────────────────────────── HHH interventions modify WAX!
```

### Kritische Appendices für Chapter 15

| Appendix | Rolle in Ch. 15 | HHH Verbindung | Status |
|----------|-----------------|----------------|--------|
| **AV (CORE-READY)** | WAX, θ Definition | Interventions modify WAX | ⚠️ Rück-Ref fehlt |
| **AW (CORE-STAGE)** | BCJ Phasen, α_BCJ | F6 = Journey Phase | ⚠️ Rück-Ref fehlt |
| **BA (FORMAL-SEGMENT)** | BCS Segmente, β_BCS | F9 = Target Segment, σ_s | ⚠️ Rück-Ref fehlt |
| **BB (FORMAL-EQUILIBRIA)** | Tipping Points, ξ | I(t) from HHH | ⚠️ Schema-Link fehlt |
| **BC (FORMAL-PROBABILITY)** | P(change) Axiome | E(I) affects P | ⚠️ Integration fehlt |

### Die mathematische Verbindung

**BC Axiom P1 (Architecture):**
```
P(i → j, t) = f(N, W, A, S, Ψ)
```

**HHH Integration:**
```
P(i → j, t | Intervention I) = f(N, W + ΔW(I), A + ΔA(I), S, Ψ)

where:
- ΔW(I) = change in Willingness from intervention I
- ΔA(I) = change in Awareness from intervention I
- E(I) = E_base × φ(Ψ) × σ_s   [from HHH Axiom HHH-A2, HHH-A5]
```

### Erforderliche Änderungen in Chapter 15 Appendices

#### In BC (FORMAL-PROBABILITY):
```latex
\section{Intervention Effects on Probability}

\subsection{Axiom P11: Intervention Modulation}
The probability of behavioral change is modulated by interventions:
$$P(i \to j | \mathcal{I}) = P_0(i \to j) + E(\mathcal{I}) \cdot \mu(\tau, \varphi) \cdot \sigma_s$$
where:
- $E(\mathcal{I})$ = intervention effectiveness from HHH
- $\mu(\tau, \varphi)$ = type-phase alignment factor (HHH Axiom HHH-A3)
- $\sigma_s$ = segment multiplier (HHH Axiom HHH-A5)

\textbf{Cross-Reference:} Appendix TKT (METHOD-TOOLKIT) for complete
intervention specification schema.
```

#### In AV (CORE-READY):
```latex
\subsection{Intervention Impact on Willingness}
Interventions from Appendix TKT affect WAX through:
- Informative (Type 1): Increases $U_{eff}$ → increases WAX
- Structural (Type 3): Reduces $\theta$ → lowers barrier
- Commitment (Type 5): Locks in WAX at high level
- Identity (Type 7): Shifts $IDN$ component of WAX

See HHH Section 2 (Nine Intervention Types) for complete taxonomy.
```

#### In AW (CORE-STAGE):
```latex
\subsection{Journey-Intervention Mapping (from HHH)}
% Add reference to existing section
See also Appendix TKT Axiom HHH-A3 (Journey Phase Alignment):
- Misaligned interventions achieve < 30% effectiveness
- Optimal type-phase combinations in HHH Table 3
```

#### In BA (FORMAL-SEGMENT):
```latex
\subsection{Segment Multipliers for Interventions}
The segment-specific intervention effectiveness $\sigma_s(\mathcal{I})$
from HHH Axiom HHH-A5 depends on parameters defined in this appendix:
- Social orientation → affects normative intervention response
- Present bias β → affects commitment intervention response
- Autonomy preference → affects all intervention types (potential reactance)

See HHH Table 4 for calibrated multiplier values.
```

#### In BB (FORMAL-EQUILIBRIA):
```latex
\subsection{Intervention Specification for Equilibrium Analysis}
Each intervention $I(t)$ in the equilibrium model corresponds to a
HHH-compliant specification:
$$I(t) = E(\mathcal{I}) \cdot \mathbb{1}[t \in [t_{start}, t_{end}]]$$

Required HHH fields for equilibrium analysis:
- F12 (Time Horizon): Determines $[t_{start}, t_{end}]$
- F14 (Path Function): Maps to equilibrium transition type
- F15 (Repetition): Determines continuous vs. discrete I(t)
```

---

## Implementation Priority

| Priority | Appendix | Effort | Impact | Chapter 15? |
|----------|----------|--------|--------|-------------|
| 🔴 **P0** | **BC (FORMAL-PROBABILITY)** | Medium | **CRITICAL** - P(change) | ✅ Core |
| 🔴 **P0** | **AV (CORE-READY)** | Low | **CRITICAL** - WAX | ✅ Core |
| 🔴 **P0** | **AW (CORE-STAGE)** | Low | **CRITICAL** - α_BCJ | ✅ Core |
| 🔴 **P0** | **BA (FORMAL-SEGMENT)** | Low | **CRITICAL** - β_BCS, σ_s | ✅ Core |
| 🔴 **P0** | **BB (FORMAL-EQUILIBRIA)** | Medium | **CRITICAL** - I(t) | ✅ Core |
| 🔴 P1 | B (CORE-HOW) | Medium | Critical - γ_ij foundation | |
| 🔴 P1 | BBB (CORE-WHERE) | High | Critical - Parameter source | |
| 🟡 P2 | C (CORE-WHAT) | Low | High - FEPSDE mapping | |
| 🟡 P2 | AAA (CORE-WHO) | Low | High - Level targeting | |
| 🟡 P2 | EEE, FFF, GGG | Medium | High - Workflow integration | |
| 🟢 P3 | Domain Appendices | Low each | Medium - Examples | |

---

## Estimated Total Effort

- **Phase 1 (CORE):** 8-12 hours
- **Phase 2 (METHOD):** 4-6 hours
- **Phase 3 (FORMAL):** 2-4 hours
- **Phase 4 (DOMAIN):** 1 hour per appendix × ~15 = 15 hours

**Total:** ~30-40 hours for complete integration

---

## Next Steps

1. ☐ Update B (CORE-HOW) with γ_ij intervention table
2. ☐ Update BBB (CORE-WHERE) with σ_s, γ_ij parameters
3. ☐ Add back-references in AW, AU, AV
4. ☐ Extend EEE with Step 10 (Intervention Design)
5. ☐ Add Intervention Registry section to FFF
6. ☐ Add Table 8 (Intervention Defaults) to GGG
7. ☐ Update BB with HHH schema linkage
8. ☐ Template domain appendices

---

*Document created: January 2026*
*For: EBF Framework Integration*
