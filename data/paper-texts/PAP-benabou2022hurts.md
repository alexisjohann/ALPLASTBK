# It Hurts To Ask

**Authors:** Roland Bénabou, Ania Jaroszewicz, and George Loewenstein
**Publication:** NBER Working Paper No. 30486
**Date:** September 2022
**DOI:** 10.3386/w30486

---

## Abstract

For agents who interact repeatedly or can communicate, we study the offering, asking, and granting (or not) of help when generosity is costly and the potential recipient's need is their private information. Asking entails the risk of rejection, which we allow to be painful: not just because it means no help is obtained, but because being turned down (or refused in advance) may reveal something negative about oneself or one's relationship with the other party. We analyze two models: one in which a Receiver can only accept or refuse offers (it is "too late to ask"), and one in which they can also ask first, before any offer is made. We characterize when an offer will be made, when a request, and when neither—in which case help is foregone even though there are gains from trade.

---

## 1. Introduction

Consider the following situations:
- A colleague struggles with a task you could help with, but they have not asked
- An elderly relative needs assistance but refuses to acknowledge it
- A student is failing but does not seek extra help during office hours
- A patient avoids getting tested for a condition they may have

In all these cases, help is available but not sought. Why? The standard economic answer would focus on transaction costs or information problems. But another, arguably more important factor is at play: **the fear of asking**.

### 1.1 The Psychology of Asking

Asking for help is difficult for several reasons:
1. **Admission of need**: Asking reveals that one is in a situation requiring assistance
2. **Risk of rejection**: The request may be denied
3. **Image concerns**: Both self-image and social image may be affected

### 1.2 Overview of Results

Our main findings are:
1. **Fear of rejection creates non-monotonic asking**: Higher need does not always lead to more asking
2. **Discouragement effect**: Non-offers discourage subsequent asking
3. **Waiting trap**: Equilibria exist where both parties wait, leading to inefficiency
4. **Offering can dominate asking**: When rejection is very costly, a norm of offering emerges

---

## 2. The Basic Model

### 2.1 Setup

**Players:**
- **Sender (S)**: Has generosity $g \sim F$ on $[0, \bar{g}]$, privately observed
- **Receiver (R)**: Has need $w \sim G$ on $[0, \bar{w}]$, privately observed

**Timing (Three Stages):**
1. **Stage 1 (Offer)**: S decides whether to offer help
2. **Stage 2 (Ask)**: If no offer made, R decides whether to ask
3. **Stage 3 (Grant)**: If asked (or offer accepted), S decides whether to grant help

### 2.2 Payoffs

**Receiver's Utility:**
$$U_R(h, F) = wh + \psi(F)$$

where:
- $h \in \{0, 1\}$ is help received
- $F \in \{A, D, N, O\}$ is the outcome (Accept, Deny, No-interaction, Offer)
- $\psi(F)$ captures the psychological payoff from each outcome

**Sender's Utility:**
$$U_S(h; g, w) = (gw - c)h + \mu\phi(F)$$

where:
- $g$ is the Sender's generosity type
- $c$ is the cost of helping
- $\mu \geq 0$ is the weight on image concerns
- $\phi(F)$ is the image payoff from each outcome

### 2.3 The Psychology of Rejection

The key insight is that rejection is not just the absence of help—it also conveys information:

$$\psi(\text{reject}) = -\lambda\alpha[\tilde{g} - \bar{g}_N]$$

where:
- $\lambda > 1$ is rejection sensitivity (akin to loss aversion)
- $\alpha \in [0, 1]$ scales the informational content
- $\tilde{g}$ is the threshold below which S rejects
- $\bar{g}_N$ is the average generosity when no offer is made

---

## 3. Analysis: When Asking is Costly

### 3.1 Asking Threshold

The Receiver asks if and only if need exceeds a threshold:

$$w \geq w^* \equiv \lambda\alpha[M^+_N(\hat{g}(w^*)) - \bar{g}_N]$$

where $M^+_N(\hat{g})$ is the conditional mean generosity given rejection.

**Key Properties:**
1. $w^*$ is increasing in $\lambda$ (rejection sensitivity)
2. $w^*$ is increasing in $\alpha$ (informational content)
3. $w^*$ can be non-monotonic in prior beliefs about generosity

### 3.2 The Discouragement Effect

**Proposition 1 (Discouragement):** If the Sender does not offer, the Receiver is less likely to ask:

$$w^*_N > w^*_O$$

This occurs because non-offering signals lower generosity, making rejection more likely and thus asking more costly.

### 3.3 Offering Threshold

The Sender offers if and only if generosity exceeds:

$$\tilde{g} = \frac{c}{E[w | w < w^*]}$$

---

## 4. Equilibrium Characterization

### 4.1 The Waiting Trap

**Proposition 2 (Multiple Equilibria):** For intermediate parameter values, multiple equilibria exist:
1. **High-activity equilibrium**: Low $w^*$, low $\tilde{g}$, frequent interaction
2. **Low-activity equilibrium**: High $w^*$, high $\tilde{g}$, infrequent interaction

Both are self-fulfilling: if R expects S to have high threshold, R sets high threshold, confirming S's expectation.

### 4.2 Welfare Analysis

The waiting trap equilibrium is Pareto-inferior:
- More instances of unmet need
- More missed opportunities for helping
- Both parties would prefer coordination on high-activity equilibrium

---

## 5. Extensions

### 5.1 Costly Offers

When offering itself is costly (signaling cost, time, etc.):
- Offers become rarer
- Asking becomes necessary but still psychologically costly
- Trade-off between offer costs and rejection costs

### 5.2 Benefactor Image Concerns

When the Sender cares about appearing generous ($\mu > 0$):
- **Positive effect**: More offers to signal generosity
- **Negative effect**: Offers may be seen as cheap signaling
- **Interaction with asking**: Asking removes signaling value of granting

### 5.3 Repeated Interactions

In dynamic settings:
- Reputation effects can help or hurt
- "Asking history" creates path dependence
- Learning about types can overcome waiting trap

---

## 6. Applications

### 6.1 Workplace Help-Seeking

- Employees hesitate to ask supervisors for help
- Fear of appearing incompetent
- Managers should offer proactively to overcome fear

### 6.2 Welfare Take-Up

- Eligible individuals often don't claim benefits
- Stigma of asking is a barrier
- Automatic enrollment can circumvent asking costs

### 6.3 Healthcare Seeking

- Patients delay seeking diagnosis
- Fear of bad news (information avoidance)
- Interaction with fear of asking medical professionals

### 6.4 Charitable Giving

- Solicitation vs. spontaneous giving
- Being asked removes "plausible deniability"
- Askers bear psychological cost of potential rejection

---

## 7. Conclusion

The fear of asking is a powerful force that shapes social and economic interactions. By modeling the psychology of rejection and the strategic dynamics of helping, we explain:

1. Why help often goes unasked and unoffered
2. Why "waiting trap" equilibria can emerge
3. Why norms of offering may dominate norms of asking
4. How interventions can overcome asking barriers

The key policy implication is that **reducing the cost of asking**—through anonymity, default enrollment, or proactive offering—can significantly increase help-seeking and welfare.

---

## Key Equations Summary

| Name | Equation | Context |
|------|----------|---------|
| Receiver Utility | $U_R = wh + \psi(F)$ | Need × help + psychological payoff |
| Sender Utility | $U_S = (gw-c)h + \mu\phi(F)$ | Benefit - cost + image |
| Asking Threshold | $w^* = \lambda\alpha[M^+_N - \bar{g}_N]$ | When to ask |
| Offering Threshold | $\tilde{g} = c/E[w\|w<w^*]$ | When to offer |
| Fear of Rejection | $\psi(\text{reject}) < 0$ | Rejection hurts |
| Discouragement | $w^*_N > w^*_O$ | Non-offers discourage |

---

## References

See bibliography for full citations.

**Foundational:**
- Bénabou and Tirole (2002, 2003, 2006, 2011): Self-confidence, Intrinsic motivation, Incentives, Identity
- Loewenstein (1987): Anticipation and Time
- Flynn and Lake (2008): If You Need Help, Just Ask

**Information Avoidance:**
- Golman, Hagmann, and Loewenstein (2017): Information Avoidance
- Oster, Shoulson, and Dorsey (2013): Genetic Testing

**Welfare Take-Up:**
- Currie (2006): The Take-Up of Social Benefits
- Moffitt (1983): Stigma of Welfare

**Charitable Giving:**
- DellaVigna, List, and Malmendier (2012): Testing for Altruism and Social Pressure
- Andreoni and Rao (2011): The Power of Asking

---

*Archived: 2026-02-04*
*Session: EBF-S-2026-02-04-SOC-002*
*Source: NBER Working Paper shared in session*
