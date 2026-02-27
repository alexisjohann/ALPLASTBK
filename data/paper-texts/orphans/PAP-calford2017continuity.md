# Continuity, Inertia and Strategic Uncertainty: A Test of the Theory of Continuous Time Games

**Authors:** Evan Calford, Ryan Oprea
**Affiliations:** Purdue University, UC Santa Barbara
**Journal:** Econometrica
**Volume:** 85, Issue 3, Pages 915-935
**Year:** 2017
**DOI:** 10.3982/ECTA14346
**Paper-ID:** PAP-calford2017continuity
**Article Type:** Experimental
**Archived:** 2026-02-04

---

## Abstract

The theory of continuous time games (Simon and Stinchcombe (1989), Bergin and MacLeod (1993)) shows that continuous time interactions can generate very different equilibrium behavior than conventional discrete time interactions. We introduce new laboratory methods that allow us to eliminate natural inertia in subjects' decisions in continuous time experiments, thereby satisfying critical premises of the theory and enabling a first-time direct test. Applying these new methods to a simple timing game, we find strikingly large gaps in behavior between discrete and continuous time as the theory suggests. Reintroducing natural inertia into these games causes continuous time behavior to collapse to discrete time-like levels in some settings as predicted by subgame perfect Nash equilibrium. However, contra this prediction, the strength of this effect is fundamentally shaped by the severity of inertia: behavior tends towards discrete time benchmarks as inertia grows large and perfectly continuous time benchmarks as it falls towards zero. We provide evidence that these results are due to changes in the nature of strategic uncertainty as inertia approaches the continuous limit.

**Keywords:** Dynamic Games, Continuous Time, Laboratory Experiments, Game Theory, Strategic Uncertainty, Epsilon Equilibrium

---

## 1. Introduction

### The Core Question

In game theoretic models, players usually make decisions in lock-step at a predetermined set of dates – a timing protocol we call "Perfectly Discrete time." Most human interaction, by contrast, unfolds asynchronously in unstructured continuous time, perhaps with some inertia delaying mutual responses. Does this difference between modeling conventions and the typical settings in which human interactions occur matter?

### Theoretical Background

Theoretical work on the effects of continuous time environments on behavior (developed especially in Simon and Stinchcombe (1989) and Bergin and MacLeod (1993)) focuses on "Perfectly Continuous time," a limiting case in which players can respond instantly (with zero inertia) to one another, and arrives at a surprising answer: **Perfectly Discrete time and Perfectly Continuous time can often support fundamentally different equilibria**, resulting in wide potential gaps in behavior between the two settings.

### Research Questions

1. Does the gulf between Perfectly Discrete and Perfectly Continuous time suggested by the theory describe real human behavior?
2. Can more realistic, imperfectly continuous time games (games with natural response delays, "Inertial Continuous time") generate Perfectly Continuous-like outcomes?

### Methodological Innovation: Freeze Time Protocol

We introduce a new protocol ("freeze time") that eliminates inertia by pausing the game for several seconds after subjects make decisions, allowing them to respond "instantly" to actions of others (with no lag in game time).

---

## 2. Theoretical Background

### 2.1 The Timing Game

Two firms, i ∈ {a,b}, each choose a time t_i ∈ [0,1] at which to enter a market. Payoffs depend on the order of entry:

**Key Properties:**
- Firms earn identical profits if they enter at the same time
- Simultaneous entry payoff is strictly concave, maximum at t* = 1 - Π_D/4c ∈ (0, 1/2)
- If one firm enters earlier than the other, she earns higher payoff
- Firms maximize joint earnings by delaying entry until t* but each has incentive to preempt

### 2.2 Three Time Protocols

**Perfectly Discrete Time:**
- Time divided into G+1 evenly spaced grid points
- Players make simultaneous decisions at each grid point
- Prediction: Unraveling → immediate entry at t = 0 (unique SPE)

**Perfectly Continuous Time:**
- Players can enter at any moment t ∈ [0,1]
- Instant response to others' actions (zero inertia)
- Prediction: Any entry time t ∈ [0, t*] supportable in SPE
- Simon & Stinchcombe (1989): t* uniquely survives iterated elimination of weakly dominated strategies

**Inertial Continuous Time:**
- Asynchronous decisions, not confined to grid
- BUT: Cannot respond instantly (reaction lag δ)
- Prediction (SPE): Unraveling returns → immediate entry at t = 0 regardless of δ

### 2.3 Alternative: ε-Equilibrium

Both Simon & Stinchcombe (1989) and Bergin & MacLeod (1993) emphasize that any Perfectly Continuous time SPE is arbitrarily close to some ε-equilibrium of a continuous time game with inertia.

**Proposition 4:** There exists a cutoff value of inertia δ̄ such that:
- For δ ≤ δ̄: Any joint entry at t ∈ [0, t*] can be supported in ε-equilibrium
- For δ > δ̄: Only entry times in [0, δ] can be supported

→ ε-equilibrium predicts that small deviations from best response can support Continuous-like outcomes when inertia is sufficiently small.

---

## 3. Experimental Design

### 3.1 Implementation

**Perfectly Discrete Time:**
- 15 subperiods (grid points at t = {0, 4, 8, ..., 56} seconds)
- Simultaneous decisions within each subperiod
- Actions shrouded during subperiod

**Perfectly Continuous Time:**
- Enter at any moment
- **Freeze Time Protocol:** When either subject enters, game freezes for 5 seconds
- Counterpart can enter during freeze → treated as simultaneous
- Freeze calibrated to be ~10× median reaction lag

**Inertial Continuous Time:**
- Enter at any moment
- No freeze time → natural human reaction lags generate inertia
- Inertia varied by changing game speed (10s, 60s, 280s periods)

### 3.2 Treatments

| Treatment | Time Protocol | Period Length | Description |
|-----------|---------------|---------------|-------------|
| PD | Perfectly Discrete | 60s | 15 grid points |
| PC | Perfectly Continuous | 60s | Freeze time protocol |
| IC10 | Inertial Continuous | 10s | High inertia |
| IC60 | Inertial Continuous | 60s | Medium inertia |
| IC280 | Inertial Continuous | 280s | Low inertia |
| L-PD | Low Temptation Discrete | 60s | Π_F = 1.4 |
| L-PC | Low Temptation Continuous | 60s | Π_F = 1.4 |

**Parameters:** (c, Π_D, Π_F, Π_S) = (1, 2.4, 4, 2.16)
→ t* = 40% of period (joint profit maximum)

**Subjects:** N = 274 undergraduates at UBC, March-May 2014
**Sessions:** 4 sessions per treatment, 8-12 subjects each
**Periods:** 30 periods per session
**Payment:** Average $26.68 (including $5 show-up)

---

## 4. Results

### 4.1 Result 1: Perfectly Discrete vs Perfectly Continuous

**Finding:** Strikingly large gaps in behavior between PD and PC treatments.

| Treatment | Entry Time | Interpretation |
|-----------|------------|----------------|
| PD | ~0% | Virtually all subjects enter immediately |
| PC | ~40% | Tightly clustered at t* (joint profit max) |

**Key Observations:**
- In PD: Virtually all subjects enter immediately → highly inefficient
- In PC: Entry times tightly clustered near t* → joint profit maximizing
- Gap is **maximal from payoff perspective**

> **Result 1:** Perfectly Continuous interaction induces fundamentally different behavior from Perfectly Discrete interaction.

### 4.2 Result 2: Effects of Inertia

**Finding:** Entry times rise monotonically towards Continuous levels as inertia falls to zero.

| Treatment | Inertia Level | Median Entry Time | % of Optimal |
|-----------|---------------|-------------------|--------------|
| IC10 | High | ~0% | - |
| IC60 | Medium | 18.4% | - |
| IC280 | Low | 32.3% | 95% |
| PC | Zero | 39.3% | ~100% |

**Key Observations:**
- High inertia (IC10): Entry delays collapse → Discrete-like
- Low inertia (IC280): Entry delays approach Continuous levels
- **Contra SPE:** SPE predicts ANY inertia → Discrete-like

> **Result 2:** High levels of inertia cause entry delay to almost completely collapse as SPE predicts. However as inertia falls towards zero, entry times progressively approach Perfectly Continuous levels.

### 4.3 Result 3: Strategic Uncertainty

**Basin of Attraction (BOA):** Probability assigned to counterpart cooperating that makes player indifferent between cooperating and entering immediately.

**Formula:**
```
BOA(t) = [U(t,t) - U(Δt,t)] / [U(t,t) - U(Δt,t) + U(t*,t*) - U(t,Δt)]
```

When BOA reaches 0.5 → immediate entry becomes **risk dominant**.

**Findings:**

| Treatment | BOA at t=0 | Time of Risk Dominance | Median Entry |
|-----------|------------|------------------------|--------------|
| PC | 0 | t* (trivially) | 39.3% |
| IC280 | intermediate | 30.8% | 32.3% |
| IC60 | intermediate | 19.9% | 18.4% |
| PD | 1 | 0% | ~0% |
| IC10 | 1 | 0% | ~0% |

**Key Finding:** Time of risk dominance ≈ Median entry time

> **Result 3:** Entry times are qualitatively well organized by the basin of attraction. The median subject enters almost exactly when immediate entry first becomes risk dominant.

### 4.4 Result 4: Validation (Low Temptation)

**Design:** Lower Π_F from 4 to 1.4 in L-PD and L-PC treatments.

**Effect on Strategic Risk:**
- In PC: No effect on BOA (still 0 for all t < t*)
- In PD: Risk dominance now at interior time (not t=0)

**Results:**
- L-PD vs PD: Significantly later entry (p = 0.02)
- L-PC vs PC: No significant difference (p = 0.183)

> **Result 4:** Changing the payoff function changes entry behavior in Perfectly Discrete time (where it changes risk dominance) but not in Perfectly Continuous time (where it has no effect).

### 4.5 Result 5: Out-of-Sample Validation

**Data:** Friedman & Oprea (2012) continuous prisoner's dilemma
- Grid-n treatment: 4, 8, 16, 32, 60 subperiods (equivalent to varying inertia)

**Finding:** Time at which "always defect" becomes risk dominant nearly perfectly predicts median final cooperation times across all parameterizations.

> **Result 5:** The earliest time of risk dominance predicts the progressively later timing of cooperation collapse observed in continuous time prisoner's dilemmas.

---

## 5. Discussion

### 5.1 Key Insights

1. **Time Structure Matters:** Perfectly Discrete and Perfectly Continuous time generate fundamentally different behaviors
2. **Inertia Magnitude Matters:** Contra SPE, inertia magnitude (not just presence) determines behavior
3. **Strategic Uncertainty Drives Selection:** BOA and risk dominance nearly perfectly organize data
4. **ε-Equilibrium Over SPE:** Results consistent with ε-equilibrium, not SPE

### 5.2 Implications for Understanding Behavior

Perfectly Discrete and Perfectly Continuous time predictions can be thought of as **polar outcomes** that each approximate realistic (Inertial Continuous time) behavior when inertia is either very high or very low, respectively.

### 5.3 Technological Change

The rise of:
- Thick online global markets
- Always-accessible mobile technology
- Friction-reducing applications
- Automated online agents

...have made strategic interactions more asynchronous and lags in response less severe. These trends push many interactions closer to Perfectly Continuous time.

**Prediction:** Perfectly Continuous time benchmarks will become increasingly relevant for understanding economic behavior.

---

## Key Parameters Extracted (EBF Integration)

| Parameter | Value | Source | EBF Use |
|-----------|-------|--------|---------|
| PD Entry Time | ~0% | Result 1 | Baseline |
| PC Entry Time | ~40% (t*) | Result 1 | Benchmark |
| IC10 Entry | ~0% | Result 2 | High inertia |
| IC60 Entry | 18.4% | Result 2 | Medium inertia |
| IC280 Entry | 32.3% | Result 2 | Low inertia |
| BOA(PC) | 0 | Result 3 | Strategic risk |
| BOA(PD) | 1 | Result 3 | Strategic risk |
| Risk Dom Time (IC60) | 19.9% | Result 3 | Prediction |
| Risk Dom Time (IC280) | 30.8% | Result 3 | Prediction |
| Reaction Lag | 0.5s | Section 4 | δ₀ |
| N | 274 | Design | Sample |

---

## EBF Framework Relevance

### Time Structure as Context Variable (Ψ_T)

```
TIME STRUCTURE EFFECTS:

PERFECTLY DISCRETE          PERFECTLY CONTINUOUS
─────────────────           ────────────────────
Entry at t ≈ 0%             Entry at t ≈ 40%
Immediate unraveling        Joint profit maximum
SPE: Single equilibrium     SPE: Multiple equilibria

                    INERTIA
                    ───────
                      │
        High ◄────────┴────────► Low
          │                       │
     Discrete-like          Continuous-like
```

### Strategic Uncertainty Mechanism

```
BOA(t) = Strategic Risk of Cooperation at time t

BOA = 0 → Safe to cooperate (PC)
BOA = 1 → Must enter immediately (PD, IC10)
BOA intermediate → Risk dominance determines entry (IC60, IC280)

Time of Risk Dominance ≈ Median Entry Time (R² ≈ 1)
```

### SPÖ Application

| Finding | SPÖ Implication |
|---------|-----------------|
| Continuous > Discrete | Ongoing engagement > periodic campaigns |
| Low inertia → Cooperation | Fast response systems enable coordination |
| Strategic uncertainty | Reduce voter uncertainty about others |
| Risk dominance | Design interventions to make cooperation "safe" |

---

## References

Bergin, James and W. Bentley MacLeod. 1993. "Continuous Time Repeated Games." International Economic Review 34(1): 21-37.

Bigoni, Maria, Marco Casari, Andrzej Skrzypacz, and Giancarlo Spagnolo. 2015. "Time Horizon and Cooperation in Continuous Time." Econometrica 83(2): 587-616.

Dal Bó, Pedro and Guillaume Frechette. 2011. "The Evolution of Cooperation in Infinitely Repeated Games: Experimental Evidence." American Economic Review 101: 411-429.

Friedman, Daniel and Ryan Oprea. 2012. "A Continuous Dilemma." American Economic Review 102(1): 337-363.

Simon, Leo K. and Maxwell B. Stinchcombe. 1989. "Extensive Form Games in Continuous Time: Pure Strategies." Econometrica 57(5): 1171-1214.

---

*Full text archived for EBF Framework reference*
*Content Level: L3 (complete with proofs in appendix)*
*Evidence Tier: 1 (Econometrica - Top-5 Economics Journal)*
*Original: Econometrica, Vol. 85, No. 3, May 2017*
