# A Formal Theory of Strategy

**Author:** Eric Van den Steen
**Year:** 2017
**Journal:** Management Science, Vol. 63, No. 8, pp. 2616-2636
**DOI:** 10.1287/mnsc.2016.2468
**Working Paper Version:** HBS Working Paper 14-058, December 2013
**Archived Date:** 2026-02-24 (updated)
**Content Level:** L2 (Comprehensive structured summary with S1-S6)

---

## Abstract

What makes a decision strategic? When is strategy most important? This paper formally studies these questions, starting from a (functional) definition of strategy as the smallest set of choices to optimally guide (or force) other choices. The paper shows that this definition coincides with the equilibrium outcome of a "strategy formulation game," in which such strategy endogenously creates a hierarchy among decisions. With respect to what makes a decision strategic and what makes strategy valuable, the paper considers the effect of commitment, reliability, and irreversibility of a decision; the presence of uncertainty (and the type of uncertainty); the number and strength of its interactions and the centrality of a decision; its level and importance; the development of capabilities; and competition.

---

## 1. Introduction

Strategy is an issue of great interest to business, with over 70,000 management books on the topic. But the importance of strategy goes beyond business: a central bank needs a strategy to fight a financial crisis and a health agency needs a strategy to fight an epidemic. But what makes a decision strategic? How do you determine whether some set of decisions constitutes a strategy? And why does strategy matter?

The purpose of this paper is to develop a formal economic theory of strategy that captures existing ideas in the management literature but that is formalized in a way that permits analysis and transparent interpretations. The analysis explores the foundational questions what makes decisions strategic and what makes strategy important.

### The Gap in Existing Literature

The management strategy literature has produced influential frameworks — Porter's five forces (1980), the resource-based view (Barney 1991), dynamic capabilities (Teece et al. 1997) — but these are largely informal verbal theories. While intuitive and practically useful, they lack the formal structure needed to generate precise, falsifiable predictions about what makes decisions strategic and when strategy matters most.

Formal economic models of strategy exist (e.g., Casadesus-Masanell and Ricart 2010; Chatain and Zemsky 2011) but typically focus on specific strategic choices (pricing, entry, positioning) rather than addressing the foundational question of what strategy IS.

### A Functional Definition

The paper starts from a functional definition: **Strategy is "the smallest set of (core) choices to optimally guide the other choices."**

This definition captures several important ideas from the management literature:

1. **Strategy as guidance:** Strategy provides direction, enabling coherent action across an organization. When people say "this organization lacks a strategy," they usually mean that various actions each made sense individually but did not make sense together — they lacked a unifying logic.

2. **Strategy as minimal set:** Strategy is not a complete plan. It is the smallest set of choices sufficient to enable all other choices to be made correctly. A complete plan would specify every decision; a strategy specifies only the core decisions from which all others follow.

3. **Strategy as adaptable:** Because strategy specifies only core choices, it allows flexibility and adaptation in non-strategic decisions. This captures the distinction between strategic intent (stable) and tactical execution (adaptive).

---

## 2. Model

### 2.1 Payoff Structure

Consider a project that generates revenue Π, which depends on K choices {C₁, ..., Cₖ}. Each choice Cₖ has a correct answer that depends on an unknown state θₖ.

The project revenue depends both on whether the choices are correct by themselves (on a standalone basis) and on whether the choices align correctly:

$$\Pi = \sum_{k=1}^{K} \alpha_k I_k + \sum_{k=1}^{K} \sum_{l=1}^{k-1} \gamma_{kl} I_{kl}$$

where:
- $I_k$ is an indicator function equal to 1 if choice Cₖ is correct (i.e., matches the optimal action given state θₖ)
- $\alpha_k > 0$ is the **standalone importance** of choice k — how much it matters to get this choice right, independently of other choices
- $I_{kl}$ is an indicator function equal to 1 if choices Cₖ and Cₗ are **aligned correctly** (i.e., their relationship matches what the states require)
- $\gamma_{kl} \geq 0$ is the **interaction importance** — how much it matters that these two choices are aligned

**Key properties of this payoff function:**

1. It separates standalone value (getting each choice right individually) from interaction value (getting choices aligned with each other)
2. It nests standard models: when all γₖₗ = 0, decisions are independent; when all αₖ = 0, only alignment matters
3. It is a supermodular function in the {Iₖ, Iₖₗ} variables, connecting to the formal theory of complementarities (Milgrom and Roberts 1990; Topkis 1978)

### 2.2 Information Structure

Each state θₖ is initially unknown. Information arrives through **signals:**

- Each decision maker may receive a signal sₖ about the state θₖ relevant to their decision
- The signal has **precision** pₖ — the probability that it correctly reveals the true state
- Signals are conditionally independent across decisions

The strategist may **investigate** states (at a cost) and then **announce** choices as part of the strategy.

### 2.3 Timing: The Strategy Formulation Game

The model proceeds in two stages:

**Stage 1: Strategy Formulation**
1. The strategist decides which states to investigate
2. For each investigated state, the strategist observes a signal
3. The strategist announces a set of choices — the strategy

**Stage 2: Strategy Implementation**
1. Each participant observes signals about their assigned decisions
2. Each participant makes their choice, considering both their own signal and the announced strategy
3. Payoffs are realized

**Key features:**
- The strategist cannot dictate all choices (bounded rationality of central planning)
- Participants retain decision rights but are guided by the strategy
- The strategy is public information — all participants observe it

### 2.4 Formal Definitions

**Definition 1 (Strategic Degree):** The degree to which a decision is "strategic" equals the probability that it is, in equilibrium, investigated or announced as part of the optimal strategy.

**Definition 2 (Strategy):** A strategy S is a set of choices for a subset of decisions K_S ⊂ K such that:
1. The choices match the target outcome for all possible states
2. The outcome is an equilibrium of the subgame when announced
3. There does not exist a smaller set K_S' ⊂ K_S satisfying conditions 1 and 2

**Definition 3 (Value of Strategy):** The value of strategy is the difference in expected payoff between having a strategy and having no strategy (i.e., each participant acts independently based on their own information).

---

## 3. Main Results

### 3.1 Persistence, Commitment, and Irreversibility (Propositions 1-3)

The paper begins by distinguishing three related but distinct concepts:

- **Irreversibility:** A decision is irreversible to the degree that it is hard to change once made
- **Persistence:** A decision is persistent if it tends to remain unchanged over time (parametrized by Δₖ, the probability the state changes)
- **Commitment:** An intentionally irreversible and visible choice

**Proposition 1a:** A decision Cₖ is more strategic when it is more persistent (when Δₖ decreases). The value of strategy increases in the persistence of the decisions.

*Intuition:* If a decision is likely to change soon, there is little value in getting it right as part of a strategy — it will soon need to be revisited anyway. Persistent decisions, however, set the stage for all subsequent choices.

**Proposition 1b:** A choice Cₖ is more strategic when it is more persistent, conditional on the interaction of Cₖ with other decisions being sufficiently strong.

**Proposition 2:** The option to commit makes a decision more strategic. However:
- The strategist may not commit even when possible (commitment forecloses learning)
- Persistence through stability makes a decision more strategic than persistence through commitment
- Stability (natural persistence) is more valuable because it does not preclude adaptation

**Proposition 3a:** Irreversibility of Cₖ increases the value of strategy but does not make Cₖ more strategic.

*Intuition:* Irreversibility increases the stakes (getting it wrong is costly) but does not affect whether the decision should be part of the core strategy. What matters is whether the decision guides other decisions.

**Proposition 3b:** Irreversibility of Cₖ makes decisions that interact strongly with Cₖ more strategic.

*Intuition:* If a decision is irreversible, other decisions must align with it (since it cannot be changed). This increases the strategic importance of decisions that interact with the irreversible one.

### 3.2 Uncertainty, Clarity, and Strategic Bets (Propositions 4-6)

**Proposition 4:** Decision Cₖ is more strategic and the value of strategy is higher when there is more uncertainty (prior uncertainty about the state θₖ). Moreover, uncertainty and interactions are complements with respect to the value of strategy.

*Key insight:* Prior uncertainty matters not because it makes it hard to find the right decision, but because it makes it hard to predict what others will do and thus to align. When there is high uncertainty, participants cannot independently figure out what the right coordinated action should be — they need strategic guidance.

**Corollary:** High-level generic choices like "maximize shareholder value" are typically NOT strategic, because there is little uncertainty about them. Choices about what NOT to do are often very strategic, because they reduce uncertainty about the firm's direction.

**Proposition 5:** A decision Cₖ is more strategic, and the value of strategy increases, when the confidence in its interactions increases (i.e., when the strategist is more certain about the nature of the interactions γₖₗ).

*Intuition:* Strategy requires knowing how decisions interact. If interactions are uncertain, strategy cannot effectively guide coordination.

**Proposition 6 (Strategy Bets):** There is value from a "strategy bet" — committing to a choice whose standalone optimal action is uncertain — when the strength of interactions γₖₗ and confidence in interactions are large, and when standalone importance αₖ is small.

*Intuition:* A strategy bet sacrifices standalone optimization (may get the individual decision wrong) to gain coordination (ensures all other decisions align consistently). This is valuable when coordination matters more than individual accuracy.

### 3.3 Interactions, Level, Centrality, and Overlap (Propositions 7-9)

**Proposition 7:** A decision with no interactions is NEVER strategic. Absent interactions, a company should have no strategy.

*This is the paper's most fundamental result:* Strategy exists because decisions interact. Without interactions, each decision can be optimized independently, and there is no need for a coordinating framework.

**Proposition 8:** A decision Cₖ is more strategic when the number and strength of its (inbound) interactions increase. The value of strategy increases in the number and strength of interactions.

*Implications:*
- More central choices (with more interaction partners) are more strategic
- Higher-level choices (with implications for many downstream decisions) are more strategic
- Strategy will typically specify one choice per function, because functional choices tend to have the most cross-functional interactions

**Proposition 9:** The added value from investigating and announcing decreases with overlap in interactions. When multiple decisions interact with the same set of other decisions, announcing one of them reduces the marginal value of announcing the others.

### 3.4 Standalone Importance (Propositions 10-11)

**Proposition 10:** A decision Cₖ is more likely to be a root choice of strategy when its standalone importance αₖ and eventual confidence pₖ increase.

*Intuition:* Standalone importance determines which decisions get investigated first. The strategist investigates the most important decisions and uses what is learned to guide others.

**Proposition 11:** No matter how standalone important, a decision is NOT strategic unless it has sufficient interactions.

*Critical example:* An airline's decision to hedge currency contracts has tremendous bottom-line impact (high αₖ) but typically does not guide other decisions (low γₖₗ). Therefore it is not strategic — it can be delegated to the treasury department without affecting the airline's strategy.

### 3.5 Specific Investments and Capabilities (Proposition 12)

**Proposition 12:** A decision Cₖ is more strategic and the value of strategy increases when more, and more important, choice-specific capabilities depend on Cₖ. Moreover, choice-specific capabilities and persistence are complements.

*Examples:*
- IKEA's decision to sell flat-pack furniture created specific capabilities in low-cost furniture design, warehouse retail, and customer self-service that reinforced the strategic choice
- Walmart's early investment in distribution logistics created capabilities that made its low-price strategy increasingly difficult to reverse
- These capabilities make strategic choices persistent AND make persistence more valuable (complementarity)

### 3.6 Competition (Propositions 13-14)

**Proposition 13:** A decision Cₖ is more (resp. less) strategic when it influences a competitor's choices in a sufficiently favorable (resp. unfavorable) direction.

**Proposition 14:** Firm G is a "strategic rival" to F if and only if both the competitive effect and interaction effect are sufficiently different from zero.

*Insight:* Competition makes strategy more important when rivals' actions affect the value of the firm's choices. This connects to the commitment literature (Ghemawat 1991) — strategic commitments are valuable precisely because they influence rivals' behavior.

### 3.7 Strategy Process (Section 5)

The model has implications for the strategy formulation process:

1. **Parsimony:** For K = 1,000 choices with equal interactions, investigating only 6-7 states is sufficient to formulate the optimal strategy. Strategy is efficient precisely because it focuses on the few choices that guide all others.

2. **Team theory result:** In team-theory settings (aligned incentives), a strategy consisting of just one choice can achieve first-best when interactions are strong enough.

3. **Hierarchy creation:** Strategy endogenously creates a hierarchy among decisions — some decisions become "higher" (strategic, guiding) while others become "lower" (operational, guided). This hierarchy emerges from the structure of interactions, not from any imposed organizational chart.

---

## 4. Endogenous Hierarchy

A key theoretical contribution is showing that strategy **endogenously creates a hierarchy** among decisions:

- **Strategic decisions** (at the top) are investigated, decided, and announced by the strategist
- **Guided decisions** (in the middle) are made by participants using both their own signals and the announced strategy
- **Independent decisions** (at the bottom) are made purely based on local information

This hierarchy is not imposed externally — it emerges from the pattern of interactions (γₖₗ). Decisions with many strong interactions naturally become strategic; decisions with few or weak interactions are naturally operational.

**Connection to organizational hierarchy:** The endogenous decision hierarchy maps naturally onto organizational hierarchy, explaining why higher-level managers focus on strategic decisions while lower-level managers handle operational ones. The model provides a formal foundation for this common organizational pattern.

---

## 5. Extensions and Discussion

### 5.1 Dynamic Strategy

In dynamic settings, the optimal strategy changes over time as:
- States evolve (creating new uncertainties)
- Capabilities develop (changing the interaction pattern)
- Competitors respond (altering the strategic landscape)

**Key dynamic insight:** Learning may make a choice both more or less strategic, depending on whether the value of coordination (which requires stability) outweighs the value of adaptation (which requires flexibility).

### 5.2 Multiple Strategists

When strategy formulation is distributed among multiple decision makers, coordination becomes more challenging but may be necessary when:
- No single person has sufficient knowledge of all interactions
- Speed of decision-making requires parallel strategy formulation
- Different parts of the organization face different external environments

### 5.3 Strategy vs. Culture

The model suggests a relationship between strategy and culture:
- **Strategy** provides explicit guidance on a few key choices
- **Culture** provides implicit guidance on many routine choices
- They are complements: strategy sets the direction; culture ensures consistent execution

---

## 6. Relation to Literature

### Strategy Definitions
- Andrews (1971): Strategy as "pattern of decisions" — the paper shows strategy guides towards a pattern but is not itself a pattern
- Porter (1996): Strategy as "choosing activities" — consistent with the model but formalized
- Mintzberg (1987): Strategy as "plan" and "guidelines" — closest to the functional definition used here

### Formal Strategy Models
- Casadesus-Masanell and Ricart (2010): Business model competition — focuses on specific strategic choices
- Chatain and Zemsky (2011): Value creation and value capture — focuses on market-level strategy
- Gibbons and Henderson (2012): Relational contracts as organizational capability — complementary to the current analysis

### Complementarity Theory
- Milgrom and Roberts (1990): Economics of modern manufacturing — foundational theory of complementarities
- Milgrom and Roberts (1995): Complementarities and fit — extension to organizational change
- Topkis (1978): Supermodular functions — mathematical foundation
- Brynjolfsson and Milgrom (2010): Complementarity in organizations — comprehensive review

### Organizational Economics
- Van den Steen (2010): Culture and beliefs — how shared beliefs enable coordination
- Gibbons and Roberts (2013): Handbook of organizational economics — comprehensive reference
- Dessein and Santos (2006): Adaptive organizations — when to centralize vs. decentralize decisions

---

## 7. Conclusion

This paper develops the first formal economic theory of strategy, starting from a functional definition and deriving precise predictions about what makes decisions strategic and when strategy is most important.

**The central message is that strategy exists because decisions interact.** Without interactions, there is no need for strategy — each decision can be optimized independently. With interactions, strategy provides the minimal coordinating framework that enables coherent action across an organization.

The fourteen propositions identify the key determinants:
- **Persistence** (not irreversibility) makes decisions strategic
- **Uncertainty** (about states, not about interactions) makes strategy valuable
- **Interactions** (number, strength, centrality) are the fundamental source of strategic importance
- **Standalone importance** affects which decisions get investigated but not which are strategic
- **Capabilities** and **competition** amplify the value of strategy through dynamic feedback

The theory also reveals that strategy endogenously creates a hierarchy among decisions — a formal foundation for the empirical observation that organizations naturally develop decision hierarchies.

---

## References

Andrews, K. R. (1971). The Concept of Corporate Strategy. Dow Jones-Irwin.

Barney, J. B. (1991). "Firm Resources and Sustained Competitive Advantage." Journal of Management, 17(1), 99-120.

Brynjolfsson, E. and Milgrom, P. (2010). "Complementarity in Organizations." In Gibbons, R. and Roberts, J. (eds.), The Handbook of Organizational Economics.

Casadesus-Masanell, R. and Ricart, J. E. (2010). "From Strategy to Business Models and onto Tactics." Long Range Planning, 43(2-3), 195-215.

Chatain, O. and Zemsky, P. (2011). "Value Creation and Value Capture with Frictions." Strategic Management Journal, 32(11), 1206-1231.

Dessein, W. and Santos, T. (2006). "Adaptive Organizations." Journal of Political Economy, 114(5), 956-995.

Ghemawat, P. (1991). Commitment: The Dynamic of Strategy. Free Press.

Gibbons, R. and Henderson, R. (2012). "Relational Contracts and Organizational Capabilities." Organization Science, 23(5), 1350-1364.

Gibbons, R. and Roberts, J. (2013). The Handbook of Organizational Economics. Princeton University Press.

Milgrom, P. and Roberts, J. (1990). "The Economics of Modern Manufacturing: Technology, Strategy, and Organization." American Economic Review, 80(3), 511-528.

Milgrom, P. and Roberts, J. (1995). "Complementarities and Fit: Strategy, Structure, and Organizational Change in Manufacturing." Journal of Accounting and Economics, 19(2-3), 179-208.

Mintzberg, H. (1987). "The Strategy Concept I: Five Ps for Strategy." California Management Review, 30(1), 11-24.

Porter, M. E. (1980). Competitive Strategy. Free Press.

Porter, M. E. (1996). "What Is Strategy?" Harvard Business Review, 74(6), 61-78.

Teece, D. J., Pisano, G., and Shuen, A. (1997). "Dynamic Capabilities and Strategic Management." Strategic Management Journal, 18(7), 509-533.

Topkis, D. M. (1978). "Minimizing a Submodular Function on a Lattice." Operations Research, 26(2), 305-321.

Van den Steen, E. (2005). "Organizational Beliefs and Managerial Vision." Journal of Law, Economics, and Organization, 21(1), 256-283.

Van den Steen, E. (2010). "Culture Clash: The Costs and Benefits of Homogeneity." Management Science, 56(10), 1718-1738.
