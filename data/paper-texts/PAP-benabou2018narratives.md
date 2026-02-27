# Narratives, Imperatives, and Moral Reasoning

**Authors:** Roland Bénabou, Armin Falk, Jean Tirole
**Source:** NBER Working Paper No. 24798
**Date:** July 2018
**JEL Codes:** D62, D64, D78, D83, D91, H41, K42, L14, Z13

---

## Abstract

By downplaying externalities, magnifying the cost of moral behavior, or suggesting not being pivotal, exculpatory narratives can allow individuals to maintain a positive image when in fact acting in a morally questionable way. Conversely, responsibilizing narratives can help sustain better social norms. We investigate when narratives emerge from a principal or the actor himself, how they are interpreted and transmitted by others, and when they spread virally. We then turn to how narratives compete with imperatives (general moral rules or precepts) as alternative modes of communication to persuade agents to behave in desirable ways.

---

## 1. Introduction

### 1.1 Moral decisions and moral reasoning

What is the moral thing to do? The aim of this paper is not to answer that immemorial question, but instead to analyze the production and circulation of arguments seeking to justify different courses of action on the basis of morality. Such appeals to notions of "right or wrong" pervade the social and political discourse, often trumping any argument of economic efficiency (bans on "immoral" transactions, trade wars, undeservedness of some group, etc.). And, of course, everyone experiences inner struggles over these issues.

Moral arguments can provide reasons for what one "should do," or on the contrary justifications for acting according to self-interest, under given circumstances. Alternatively, they may be broad "fiat" prescriptions, dictating a fixed behavior across most situations, without explaining why. We refer to these two classes as **moral narratives** and **imperatives**, respectively, and explore how they combine with more standard motivations such as social preferences, self-control, and image or identity concerns to shape behaviors and ultimately favor the emergence of pro- or anti-social norms.

### 1.2 Narratives and imperatives: an economic view

**Narratives** are stories people tell themselves, and each other, to make sense of human experience—that is, to organize, explain, justify, predict and sometimes influence its course; they are "instrument[s] of mind in the construction of reality" (Bruner 1991, p. 6).

We define a **moral narrative** as any news, story, life experience or heuristic that has the potential to alter an agent's beliefs about the tradeoff between private benefits and social costs (or the reverse) faced by a decision-maker, who could be himself, someone he observes, or someone he seeks to influence.

We see **imperatives** as located at the opposite end of the independent-persuasiveness spectrum: whereas narratives either are, or at least act like, hard information, imperatives are entirely soft messages of the type "thou shalt (not) do this," seeking to constrain behavior without offering any reasons why.

### 1.3 Main Results

1. **Viral transmission**: What types of social structures lead exculpatory versus responsibilizing rationales to spread widely, or remain clustered within subgroups?

2. **Moral standards**: How tolerant is a society of excuses for self-interested behavior, how much stigma is borne by those who fail to produce one, and how hard do people search for receivable arguments?

3. **Imperatives vs narratives**: How do imperatives work, what characteristics confer moral legitimacy to issue them, and when will this be more effective than communicating specific reasons?

---

## 2. Basic Model

### 2.1 Moral decisions and moral types

At date 1, a risk-neutral individual chooses whether to engage in moral behavior (a = 1) or not (a = 0). Choosing a = 1 is prosocial: it involves a personal cost c > 0 but may yield benefits for the rest of society, generating an expected externality e ∈ [0,1].

Agents differ by their **intrinsic motivation** (or "core values") to act morally: given e, it is either vHe (high, moral type) or vLe (low, immoral type), with probabilities π and 1−π and vH > vL ≥ 0.

In addition to intrinsic enjoyment, acting morally confers a **social or self-image benefit**, reaped at date 2. An agent of type v = vH, vL has expected utility:

```
U = (ve − c/β)a + μv̂(a)
```

where:
- v̂(a) is the expected type conditional on action a ∈ {0,1}
- μ measures the strength of self or social image concerns
- β ≤ 1 is the individual's degree of self-control

**Proposition 1 (determinants of moral behavior)**: The moral type contributes if and only if e > e*, where e* is uniquely defined by:

```
vHe* − c/β + μ(vH − v̄) ≥ 0
```

Immoral behavior is encouraged by:
- Low perceived social benefit e
- High personal cost c or low self-control β
- Weak reputational concern μ

### 2.2 Related evidence

1. **Social and self-image concerns (μ)**: Increased visibility induces more moral behaviors (Ariely et al. 2009, DellaVigna et al. 2012)

2. **Initial reputation**: Higher initial reputation leads to "moral licensing" (Bradley-Geist et al. 2010, Monin and Miller 2001)

3. **Self-control (β)**: Lower self-control associates with more selfish behavior (Achtziger et al. 2015, Gino et al. 2011)

4. **Costs (c)**: Prosocial behavior responds to personal costs (Goeree et al. 2002)

5. **Social externality (e)**: Prosocial choices are sensitive to implied consequences (Brock et al. 2013, Gneezy et al. 2014)

### 2.4 Exoneration and responsibility: narratives as justifications

Two main types of narratives:

**(1) Absolving narratives** (negative/excuses):
- (a) Downplaying the harm
- (b) Blaming the victims
- (c) Denying agency and responsibility
- (d) Appealing to higher loyalties

**(2) Responsibilizing narratives** (positive):
- (a) Appeals to moral and religious precepts
- (b) Arguments inducing empathy ("What if it were you?")
- (c) Stressing common identities
- (d) Kantian-like arguments ("What if everyone did the same?")

---

## 3. The Viral Transmission of Narratives

### 3.1 Setup

Agents are arranged on a line, each can be "Passive" (P) or "Active" (A). Types follow a Markov process with persistence ρ ∈ [0,1]:

```
Pr[i+1 ∈ A | i ∈ A] = Pr[i+1 ∈ P | i ∈ P] = ρ
```

**Key tradeoffs:**
- **Reputational motive**: Sharing excuses protects reputation
- **Social influence motive**: Sharing excuses may trigger cascades of bad behavior

**Result**: Negative narratives are **strategic substitutes**, positive narratives are **strategic complements**.

### 3.2 Default action is moral (aH(∅) = 1)

The "influence factor" for negative narratives:

```
N⁻_A = π(1−x) / [1 − ρ(1−x)]
```

**Proposition 3**: In this equilibrium:
1. Positive narratives are transmitted by no one (redundant)
2. Negative narratives are transmitted by all active agents
3. Greater mixing (lower ρ) raises prosocial behavior

### 3.3 Default action is immoral (aH(∅) = 0)

**Proposition 4**: In this equilibrium:
1. Negative narratives are transmitted but have no behavioral impact
2. Positive narratives are transmitted by passive agents and high-morality active ones
3. Greater mixing (lower ρ) raises prosocial behavior

### 3.4 Implications

**Proposition 5 (polarization)**: In either equilibrium, the gaps between active and passive agents' awareness of narratives are both U-shaped in network segregation ρ, with minimum at ρ = 1/2 and maximum at ρ = 1.

---

## 4. Moral Standards: What is Justifiable?

### 4.1 Search for reasons

The key factors determining whether a prosocial or antisocial culture prevails:

1. People's **prior mean e₀** about whether actions have important externalities
2. The **tail risks** in uncertainty surrounding that question

**Definition 1**: A distribution F₁ is more ê-bottom heavy than F₂ if M⁻_F₁(ê) < M⁻_F₂(ê), where M⁻(ê) = E[e | e < ê].

### 4.2 Looking for "reasons not to act"

**Proposition 6 (prosocial norm)**: For high enough e₀, there exists an equilibrium where:
1. Moral behavior is the default choice
2. Violating standards carries maximal stigma (v̂_ND = vL)
3. If F(e) is sufficiently bottom-heavy, high types search more: xH > xL

### 4.3 Looking for "reasons to act"

**Proposition 8 (selfish norm)**: For low enough e₀, there exists an equilibrium where:
1. Abstaining is the default choice
2. High types always search more: xH > xL
3. Moral standard is low (ê > e*)

**Proposition 9 (multiple norms)**: There exists a range [e₀, ē₀] where both equilibria coexist.

---

## 5. Narratives Versus Imperatives

### 5.1 Setup

Principal (she) learns narrative e ~ F(e), agent (he) chooses a ∈ {0,1}.

- **Narrative**: Arguments about externalities
- **Imperative**: Precept "do a = 1" without reasons

Agent utility: UA(e) = vH(e − e*)
Principal utility: UP(e) ≈ (w + vH)e − c, with indifference point e*P < e*

### 5.2 Coarse versus noisy communication

**Condition for imperative effectiveness**:
```
M⁺(e*P) ≡ E[e | e ≥ e*P] ≥ e*
```

**Proposition 10 (clarity vs credibility)**:
1. If M⁺(e*P) > e*, principal issues imperative when e ≥ e*P
2. If M⁺(e*P) ≤ e*, principal discloses narrative when e > e*

Imperatives are more likely when:
- Greater congruence between principal and agent
- Principal perceived as having better judgment
- Larger expected externalities

### 5.3 The value of flexibility

**Proposition 11 (congruence and flexibility)**:
1. Imperatives are used iff M⁺(ey) ≥ e*, where ey > e*P
2. Probability of imperative is hump-shaped in congruence
3. Effect of self-control on imperatives is similarly hump-shaped

---

## 6. Conclusion

Key findings:
1. Narratives serve as justifications that enable maintaining positive self-image while acting selfishly
2. Network structure determines viral spread of moral arguments
3. Moral standards emerge endogenously from search for reasons
4. Imperatives require moral authority but provide commitment benefits

Future directions:
- Competing narratives
- Identity and in-group/out-group dynamics
- Combined narrative-imperative systems

---

## Key Parameters for EBF Integration

| Parameter | Symbol | Description | Typical Range |
|-----------|--------|-------------|---------------|
| Image concern | μ | Strength of reputational/self-image motivation | μ > 0 |
| Self-control | β | Inverse hyperbolicity (β ≤ 1 implies present bias) | β ∈ [0.7, 1.0] |
| Externality | e | Expected social benefit from moral action | e ∈ [0, 1] |
| Moral type spread | vH − vL | Difference between high and low moral types | > 0 |
| Network persistence | ρ | Correlation of types on network | ρ ∈ [0, 1] |
| Prior mean | e₀ | Prior belief about externality importance | e₀ ∈ [0, 1] |

---

## References

Key citations from the paper:
- Bénabou, R. and J. Tirole (2006a) "Incentives and Prosocial Behavior"
- Bénabou, R. and J. Tirole (2011a) "Identity, Morals and Taboos: Beliefs as Assets"
- Falk, A. and N. Szech (2013) "Morals and Markets"
- Sykes, G. M. and D. Matza (1957) "Techniques of Neutralization"
