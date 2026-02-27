# The Dynamics of Corporate Culture

**Author:** Eric Van den Steen
**Year:** 2024
**Institution:** Harvard Business School
**Type:** Working Paper
**Archived Date:** 2026-02-24
**Content Level:** L2 (Comprehensive structured summary with S1-S6)

---

## Abstract

This paper develops a formal model of how corporate culture evolves over time and what drives its dynamics. Building on Van den Steen (2010) and Gibbons and Henderson (2012), the paper models culture as the set of shared expectations about "what is normal" (behavioral norms) and "what is valued" (organizational values) within a firm. Culture changes through selection (hiring and attrition), socialization (incumbent influence on newcomers), and external shocks. The model predicts that culture change is inherently slow (2-5 year horizons), that attempted rapid culture change often fails due to complementarities between cultural elements, and that culture depreciation rates vary systematically across organizational dimensions. The paper provides formal foundations for the empirical observation that organizational transformation requires sustained effort over multiple years.

---

## 1. Introduction

Corporate culture is widely recognized as both important and difficult to change. Survey evidence suggests that over 70% of organizational transformation efforts fail, and the most commonly cited reason is "culture." Yet the economics literature has provided limited formal guidance on why culture changes slowly and what determines the pace of cultural evolution.

### Research Questions

This paper addresses three questions:

1. **Dynamics:** How does corporate culture evolve over time, and what are the key mechanisms of cultural change?
2. **Speed:** Why is culture change inherently slow, and what determines the rate of cultural depreciation and renewal?
3. **Complementarities:** How do interactions among cultural elements affect the feasibility and dynamics of culture change?

### Definition of Culture

Following Van den Steen (2010) and building on Gibbons and Henderson (2012), the paper defines culture along two dimensions:

**"What is normal" (Behavioral Norms):** Shared expectations about how people behave in the organization. These norms are self-reinforcing: people conform because they expect others to conform, and observation confirms this expectation.

**"What is valued" (Organizational Values):** Shared beliefs about what the organization considers important, desirable, or worth pursuing. Values guide behavior in novel situations where specific norms do not exist.

The dual definition captures the distinction between:
- Culture as coordination device (norms: "we do things this way")
- Culture as identity/motivation device (values: "we care about these things")

---

## 2. Model

### 2.1 Cultural State

The cultural state of an organization at time t is represented by a vector:

$$\mathbf{C}(t) = \{n_1(t), n_2(t), ..., n_J(t), v_1(t), v_2(t), ..., v_M(t)\}$$

where:
- $n_j(t) \in [0,1]$ represents the strength of norm j (0 = absent, 1 = fully established)
- $v_m(t) \in [0,1]$ represents the salience of value m

### 2.2 Mechanisms of Cultural Change

The paper identifies three primary mechanisms:

**Mechanism 1: Selection (Hiring and Attrition)**

New hires bring beliefs and behavioral tendencies from their prior experience. Over time, the composition of the workforce shifts toward the new culture:

$$\frac{dn_j}{dt}\bigg|_{\text{selection}} = \lambda_{\text{hire}} \cdot (n_j^{\text{target}} - n_j(t)) - \lambda_{\text{attrit}} \cdot n_j(t) \cdot (1 - f_j)$$

where:
- $\lambda_{\text{hire}}$ is the hiring rate (fraction of workforce replaced per year)
- $n_j^{\text{target}}$ is the desired norm strength
- $\lambda_{\text{attrit}}$ is the natural attrition rate
- $f_j$ is the "fit" of existing employees with norm j

**Mechanism 2: Socialization (Incumbent Influence)**

Existing employees socialize newcomers into existing norms and values. This creates inertia — the larger the existing culture's footprint, the more resistant it is to change:

$$\frac{dn_j}{dt}\bigg|_{\text{social}} = \sigma \cdot n_j(t) \cdot (1 - n_j(t))$$

where σ is the socialization strength. Note this is a logistic-type dynamic: socialization reinforces norms that are already partially established but does not establish entirely new norms.

**Mechanism 3: External Shocks**

Major events (crises, leadership changes, market disruptions) can shift cultural elements discontinuously:

$$n_j(t^+) = n_j(t^-) + \Delta_j \cdot \text{shock}(t)$$

The model shows that shocks are necessary for rapid culture change because selection and socialization are inherently slow processes.

### 2.3 Cultural Depreciation

A key contribution is formalizing **cultural depreciation** — the rate at which cultural elements decay absent reinforcement:

$$\frac{dn_j}{dt}\bigg|_{\text{depreciation}} = -\delta_j \cdot n_j(t)$$

where $\delta_j$ is the depreciation rate of cultural element j.

**Key insight:** Depreciation rates vary systematically across cultural dimensions:

| Cultural Element | Depreciation Rate δ | Half-Life | Mechanism |
|-----------------|---------------------|-----------|-----------|
| Operational norms | 0.15-0.30/year | 2-5 years | Staff turnover, process changes |
| Strategic orientation | 0.10-0.20/year | 3-7 years | Market evolution, leadership |
| Core values | 0.03-0.10/year | 7-23 years | Generational replacement |
| Identity/founding myths | 0.01-0.05/year | 14-69 years | Institutional memory loss |

**Why do values depreciate slower than norms?** Norms depend on behavioral equilibria that can be disrupted by turnover; values are internalized and transmitted through stories, rituals, and symbols that persist even as specific people leave.

### 2.4 Complementarity Effects

Cultural elements interact. Some pairs are complements (adopting both together is more effective than either alone) and some are substitutes or conflicts:

$$V(\mathbf{C}) = \sum_j \alpha_j n_j + \sum_j \sum_{k>j} \gamma_{jk} n_j n_k$$

where $\gamma_{jk}$ captures the interaction between cultural elements j and k.

**Key result:** Complementarities make culture change harder because:
1. Changing one element without its complements reduces value (the "coherence trap")
2. The optimal change is to move all complementary elements simultaneously
3. Simultaneous change is organizationally difficult (requires coordination across many dimensions)

This explains the "all-or-nothing" pattern in culture change: partial reforms often fail because they break cultural complementarities without establishing new ones.

---

## 3. Main Results

### 3.1 The 2-5 Year Horizon (Proposition 1)

**Proposition 1:** Under standard parameter values (hiring rate 10-15%, socialization strength σ = 0.3-0.5, depreciation rate δ = 0.05-0.15), significant culture change requires 2-5 years.

*This result emerges from the interaction of three forces:*
- Selection takes time (turnover is typically 10-20% per year)
- Socialization by incumbents slows the adoption of new norms
- Complementarities require coordinated multi-dimensional change

**Calibration:** Using data from Bloom et al. (2012) on management practice adoption and persistence:
- Average time for management practice adoption: 3-4 years
- Average time for full culture shift after CEO change: 3-5 years (consistent with Bandiera et al. 2020)
- Average time for post-merger cultural integration: 5-7 years

### 3.2 Why Rapid Culture Change Fails (Proposition 2)

**Proposition 2:** Attempted rapid culture change (δt < 1 year) fails with probability > 0.7 under standard complementarity conditions, because:

1. **Coordination failure:** Changing multiple cultural elements simultaneously requires coordination that exceeds organizational capacity
2. **Backlash:** Rapid change triggers resistance from incumbents whose identity is tied to existing culture (Van den Steen 2010: "Culture Clash")
3. **Incompleteness:** Rapid change typically addresses visible norms but not underlying values, creating surface compliance without genuine cultural shift

### 3.3 Culture and Strategy Interaction (Proposition 3)

**Proposition 3:** Strategy changes are more successful when they are consistent with existing culture, and culture changes are more successful when they are consistent with current strategy.

*Formal statement:* The joint value V(S, C) is supermodular in (S, C) — strategy and culture are complements. Changing both simultaneously is better than changing either alone, but the coordination cost makes sequential change (strategy first, culture follows) more practical.

**Implication for the FA-SM-1.1 model:** The depreciation rate of organizational culture (δ_OC) determines how quickly behavioral changes translate into value changes. When δ_OC is low (strong culture), the organization is stable but slow to change; when δ_OC is high (weak culture), change is easier but harder to sustain.

### 3.4 Founder Effects and Cultural Persistence (Proposition 4)

**Proposition 4:** Cultures established by founders are more persistent (lower δ) than cultures imposed by hired CEOs, because:
1. Founders select the initial workforce based on cultural fit
2. Founding conditions create "origin stories" that are transmitted culturally
3. Founder-established norms have no competing prior culture to displace

*Connection to Zellweger (2023):* Family firms, where founder culture persists through generational transmission, exhibit systematically different strategic behaviors than non-family firms.

---

## 4. Applications

### 4.1 Post-Merger Integration

The model predicts that cultural integration after mergers follows a characteristic S-curve:
- **Year 0-1:** Surface-level changes (new branding, unified policies)
- **Year 1-3:** Behavioral norm convergence (work practices, decision processes)
- **Year 3-5:** Value alignment (strategic priorities, organizational identity)
- **Year 5+:** Deep cultural integration (shared assumptions, implicit coordination)

This S-curve explains why many mergers fail to deliver promised synergies within the typical 2-3 year planning horizon — the cultural prerequisites for synergy realization take 3-5 years.

### 4.2 Digital Transformation

Digital transformation requires both technological and cultural change. The model predicts that:
- Technology adoption is faster than cultural adaptation (δ_tech > δ_culture)
- The gap creates a "culture lag" that reduces the value of technology investments
- Successful digital transformation requires simultaneous investment in culture change
- The complementarity between digital tools and cultural norms (e.g., data-driven decision-making) means partial transformation is suboptimal

### 4.3 Leadership Transitions

When a new CEO takes over:
- The 3-year lag (Bandiera et al. 2020) is explained by the time needed for cultural change
- The CEO's vision (Van den Steen 2018) accelerates culture change by providing a clear target
- CEO succession planning should account for cultural transition time

---

## 5. Relation to Literature

### Corporate Culture
- Van den Steen (2010): "Culture Clash: The Costs and Benefits of Homogeneity" — formal model of culture as shared beliefs
- Gibbons and Henderson (2012): "Relational Contracts and Organizational Capabilities" — culture as shared expectations
- Kreps (1990): "Corporate Culture and Economic Theory" — early formalization
- Schein (2010): Organizational Culture and Leadership — foundational practitioner framework

### Organizational Change
- Bloom et al. (2012): Management practices across firms — empirical evidence on practice adoption speed
- Bandiera et al. (2020): CEO behavior and firm performance — 3-year lag for CEO effects
- Kotter (1995): Leading Change — 8-step change process (practitioner)
- Hannan and Freeman (1984): Structural Inertia and Organizational Change — ecological perspective

### Complementarities
- Milgrom and Roberts (1990): Economics of Modern Manufacturing — foundational complementarity theory
- Ichniowski et al. (1997): HRM practices — empirical complementarities in production
- Brynjolfsson and Milgrom (2010): Complementarity in Organizations — comprehensive review

### Family Firms and Persistence
- Zellweger (2023): Entrepreneurs in the Making — family firm dynamics
- Bertrand and Schoar (2006): The Role of Family in Family Firms — governance and culture

---

## 6. Conclusion

This paper provides a formal framework for understanding why corporate culture changes slowly and what determines the pace of cultural evolution. The key findings are:

1. **Culture change requires 2-5 years** under standard conditions, driven by the interaction of selection, socialization, and complementarity forces.

2. **Depreciation rates vary systematically:** Operational norms depreciate fastest (δ = 0.15-0.30/year), while core values and identity persist for decades (δ = 0.01-0.05/year).

3. **Complementarities are the key barrier:** Cultural elements are interconnected, making partial change suboptimal and simultaneous change organizationally difficult.

4. **Strategy and culture are complements:** Successful organizational transformation requires aligned changes in both strategy and culture, typically implemented sequentially.

5. **Founder effects persist:** Cultures established by founders are more persistent than those imposed by hired managers, explaining the distinctive character of founder-led and family firms.

The model provides formal foundations for the managerial wisdom that "culture eats strategy for breakfast" (attributed to Peter Drucker) — not because culture is more important than strategy, but because culture change is slower and therefore constrains the pace of strategic transformation.

---

## References

Bandiera, O., Prat, A., Hansen, S., and Sadun, R. (2020). "CEO Behavior and Firm Performance." Journal of Political Economy, 128(4), 1325-1369.

Bertrand, M. and Schoar, A. (2006). "The Role of Family in Family Firms." Journal of Economic Perspectives, 20(2), 73-96.

Bloom, N., Genakos, C., Sadun, R., and Van Reenen, J. (2012). "Management Practices Across Firms and Countries." Academy of Management Perspectives, 26(1), 12-33.

Brynjolfsson, E. and Milgrom, P. (2010). "Complementarity in Organizations." In Gibbons, R. and Roberts, J. (eds.), The Handbook of Organizational Economics.

Gibbons, R. and Henderson, R. (2012). "Relational Contracts and Organizational Capabilities." Organization Science, 23(5), 1350-1364.

Hannan, M. T. and Freeman, J. (1984). "Structural Inertia and Organizational Change." American Sociological Review, 49(2), 149-164.

Ichniowski, C., Shaw, K., and Prennushi, G. (1997). "The Effects of Human Resource Management Practices on Productivity." American Economic Review, 87(3), 291-313.

Kotter, J. P. (1995). "Leading Change: Why Transformation Efforts Fail." Harvard Business Review, 73(2), 59-67.

Kreps, D. M. (1990). "Corporate Culture and Economic Theory." In Alt, J. and Shepsle, K. (eds.), Perspectives on Positive Political Economy. Cambridge University Press.

Milgrom, P. and Roberts, J. (1990). "The Economics of Modern Manufacturing." American Economic Review, 80(3), 511-528.

Schein, E. H. (2010). Organizational Culture and Leadership (4th ed.). Jossey-Bass.

Van den Steen, E. (2010). "Culture Clash: The Costs and Benefits of Homogeneity." Management Science, 56(10), 1718-1738.

Van den Steen, E. (2017). "A Formal Theory of Strategy." Management Science, 63(8), 2616-2636.

Van den Steen, E. (2018). "Strategy and the Strategist." Management Science, 64(10), 4533-4551.

Zellweger, T. (2023). Entrepreneurs in the Making: From Necessity to Willingness. Cambridge University Press.
