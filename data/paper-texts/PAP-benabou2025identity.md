# Identity as Self-Image

**Authors:** Roland Bénabou and Luca Henkel
**Publication:** Handbook of the Economics of Identity, Elsevier (forthcoming)
**NBER Working Paper:** No. 34297
**Date:** September 2025
**DOI:** 10.3386/w34297

---

## Abstract

This chapter surveys economic models of identity based on self-image concerns—the desire to see or present oneself as a certain type of person. We first present a general framework unifying past approaches: the value of any object, action, or belief, in terms of its implications for the agent's perception (conscious or unconscious) of who they are. We then use this framework to organize the literature and highlight how different specifications within this paradigm can account for a wide variety of phenomena, while potentially leading to different predictions in other situations.

---

## 1. Introduction

Consider the following decisions:
- A patient decides to get tested for a particular genetic disease or to remain ignorant of their predisposition.
- A person reflects on their past relationship and ponders the causes for its ending, even though the other person has moved on and is no longer reachable.
- A donor deliberates whether to give the same monthly amount to UNICEF in one larger lump sum, or in four parts, more regularly.

Each of these decisions can be analyzed in a standard neoclassical economic framework. However, such an analysis seems to miss crucial aspects of what we might consider the true motives for these choices, which hinge on how they affect the person's perception of their own traits or morals.

### The Self-Image Approach

The self-image approach to identity economics examines how people value their actions, beliefs, and choices based on their implications for self-perception. The key insight is that utility depends not only on material outcomes but also on maintaining a favorable view of oneself.

**General Framework:**
$$U = u(a, \theta) + \mu \cdot v(\sigma)$$

where:
- $u(a, \theta)$ is standard utility from actions and outcomes
- $\mu$ is the weight on self-image
- $v(\sigma)$ is the value of self-perceived type $\sigma = E[\theta|I]$

---

## 2. A Unifying Framework

### 2.1 Building Blocks

Any model of self-image is built from these components:

1. **Types** ($\theta$): The underlying characteristic about which the agent cares
2. **Self-image** ($\sigma$): The agent's belief about their type
3. **Image utility** ($v(\sigma)$): The intrinsic value of self-perceived type
4. **Image concern** ($\mu$): Weight on image utility in overall welfare

### 2.2 Three Approaches

**Contemporaneous (Self-Esteem):**
$$U_S = E[v(\sigma)|I_t]$$

Utility from current self-image, as in ego utility models.

**Anticipatory:**
$$U = E[v(c)] + \lambda_A \cdot E_0[E[v(c)|\xi]]$$

Following Caplin and Leahy (2001), agents derive utility from anticipating future consumption.

**Retrospective:**
$$U = E[v(\sigma_T)|I_0]$$

Agents care about how they will view their past selves.

---

## 3. Self-Signaling

### 3.1 The Basic Model

Actions serve as signals about one's type to oneself. When an agent chooses action $a$, they update their belief about their type:

$$\sigma' = E[\theta|a, I]$$

This creates **diagnostic utility**: the value of learning about oneself through choices.

### 3.2 Diagnostic Utility

Following Dillenberger and Sadowski (2012):

$$v(\sigma) = \sigma \cdot v(1) + (1-\sigma) \cdot v(0)$$

The value function is linear in beliefs when utility is separable.

### 3.3 Applications

**Menu Effects:** People may prefer menus that exclude temptation because choosing the virtuous option from a restricted menu provides no diagnostic value.

**Moral Licensing:** After behaving morally, agents feel licensed to behave less morally because their self-image has been bolstered.

---

## 4. Motivated Beliefs

### 4.1 Optimal Beliefs (Brunnermeier-Parker)

Agents choose beliefs to maximize a trade-off:

$$\max_{\pi} \left[ U(a^*(\pi), \pi) - \kappa \cdot D(\pi||\pi_0) \right]$$

where:
- $\pi$ is the chosen belief
- $\pi_0$ is the Bayesian benchmark
- $\kappa$ is the cost of self-deception
- $D(\cdot||\cdot)$ is the divergence measure

### 4.2 Selective Memory

Memory as a tool for self-image maintenance:

$$\rho(a) = P(\text{recall}|a)$$

Agents may be more likely to recall positive actions/outcomes than negative ones.

### 4.3 Information Avoidance

The value of information with ego utility:

$$V(\text{info}) = V_{\text{instrumental}} - V_{\text{ego loss}}$$

When ego costs exceed instrumental benefits, agents avoid information.

---

## 5. Dual-Self Models

### 5.1 Quasi-Hyperbolic Discounting

Following Laibson (1997):

$$W_0 = \max\left[ u(c_0) + \beta \delta \sum_{t=1}^{\infty} \delta^{t-1} u(c_t) \right]$$

where $\beta < 1$ captures present bias.

### 5.2 Multiple Selves

The agent as a collection of selves with different preferences:
- **Planner**: Long-run optimizer
- **Doer**: Short-run maximizer

This creates internal conflicts and demand for commitment devices.

### 5.3 Self-Control Costs

Following Gul and Pesendorfer (2001), agents incur costs from resisting temptation:

$$U = u(c) - \gamma \cdot [\max_{c' \in C} u(c') - u(c)]$$

---

## 6. Anticipatory Utility

### 6.1 Savoring and Dreading

Utility from thinking about future consumption:

$$U = E[v(c)] + \lambda_A \cdot E_0[E[v(c)|\xi]]$$

- $\lambda_A > 0$: Savoring positive outcomes
- Can explain early resolution preference (Kreps-Porteus)

### 6.2 Health Anxiety (Köszegi)

Patients may prefer not knowing about health risks because:
- Good news provides temporary relief
- Bad news provides persistent anxiety
- Asymmetric anticipatory utility

---

## 7. Implications and Open Questions

### 7.1 Policy Implications

1. **Information provision**: May backfire if ego utility dominates
2. **Commitment devices**: Valuable for self-control
3. **Framing**: Can affect diagnostic utility of choices
4. **Feedback timing**: Affects anticipatory utility

### 7.2 Open Questions

1. How do self-image concerns interact with social image?
2. When do different specifications lead to different predictions?
3. How can we empirically distinguish between approaches?
4. What determines individual differences in $\mu$?

---

## 8. Conclusion

The self-image approach provides a unified framework for understanding how identity concerns shape economic behavior. By recognizing that people care not just about outcomes but about what those outcomes reveal about who they are, we can better understand phenomena ranging from information avoidance to self-control problems to moral licensing.

The key insight is that all self-image models share a common structure:

$$U = u(\text{material}) + \mu \cdot v(\sigma)$$

Different specifications—anticipatory, contemporaneous, retrospective—represent different timing assumptions about when self-image utility is realized.

---

## References

See bibliography for full citations.

**Foundational:**
- Akerlof and Kranton (2000): Economics and Identity
- Bénabou and Tirole (2002, 2003, 2004, 2006, 2011, 2016): Self-confidence, Intrinsic motivation, Willpower, Incentives, Identity, Mindful economics

**Anticipatory Utility:**
- Caplin and Leahy (2001): Psychological Expected Utility
- Loewenstein (1987): Anticipation and Time
- Köszegi (2003): Health Anxiety

**Self-Signaling:**
- Bodner and Prelec (2003): Self-Signaling
- Dillenberger and Sadowski (2012): Ashamed to be Selfish

**Motivated Beliefs:**
- Brunnermeier and Parker (2005): Optimal Expectations
- Kunda (1990): Motivated Reasoning

**Information Avoidance:**
- Golman, Hagmann, and Loewenstein (2017): Information Avoidance
- Oster, Shoulson, and Dorsey (2013): Genetic Testing

**Dual-Self:**
- Laibson (1997): Golden Eggs
- Thaler and Shefrin (1981): Economic Theory of Self-Control
- Fudenberg and Levine (2006): Dual-Self Model

---

*Archived: 2026-02-04*
*Session: EBF-S-2026-02-04-IDN-001*
*Source: NBER Working Paper shared in session*
