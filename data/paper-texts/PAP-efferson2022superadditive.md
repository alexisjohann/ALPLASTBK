# Super-Additive Cooperation

**Authors:** Charles Efferson, Helen Bernhard, Urs Fischbacher, Ernst Fehr
**Year:** 2022
**Type:** CESifo Working Paper No. 10133
**URL:** https://ssrn.com/abstract=4301645
**GitHub:** www.github.com/cmefferson/superAdditiveCooperation

---

## Abstract

We study whether and how repeated interactions within groups and intergroup competition support cooperative behaviours. Neither mechanism reliably supports the evolution of cooperation when actions vary continuously. Two critical limitations explain the result. First, under repeated interactions, ambiguous reciprocity invades and destabilises populations of cooperative reciprocators. Second, intergroup competitions support cooperation only when groups compete frequently, competition outcomes are sensitive to intergroup differences, and migration between groups is low. Although repeated interactions and group competitions do not support cooperation by themselves, combining them often triggers powerful synergies because group competitions can stabilise cooperative strategies against the corrosive effect of ambiguous reciprocity. Consistent with this scenario, reciprocity in social dilemmas observed among Ngenika and Perepka people in Papua New Guinea is cooperative within groups but not between groups.

## 1. Introduction

Humans cooperate with each other in a wide range of contexts. From an evolutionary perspective, this raises a puzzle: if cooperation is costly to the individual, how can it evolve? Two major classes of mechanisms have been proposed:

1. **Repeated interactions (direct reciprocity)**: When individuals interact repeatedly, cooperation can be sustained through reciprocal strategies like tit-for-tat.

2. **Intergroup competition (group selection)**: When groups compete for resources, more cooperative groups may outcompete less cooperative ones.

Both mechanisms have received theoretical and empirical support, but each has critical limitations. This paper examines what happens when both mechanisms operate simultaneously.

## 2. A Framework for Continuous Cooperation

### 2.1 The Game

We study a sequential social dilemma where a first mover transfers resources to a second mover, and the second mover responds. Transfers are multiplied by a factor greater than 1, creating the social dilemma: full cooperation is socially optimal but individually costly.

### 2.2 Strategy Space

We parameterize response functions with varying dimensionality:
- **2D**: Initial transfer + slope (escalating or de-escalating only)
- **3D**: Initial transfer + left/right intercepts (allows ambiguous reciprocity)
- **4D**: Nonlinear response functions

This is critical because **cooperative strategies only persist with 2D strategy space** and fail with 3D or higher dimensionality.

### 2.3 Types of Reciprocity

1. **Perfect reciprocity**: current_transfer = partner_last_transfer
2. **Escalating reciprocity**: current_transfer > partner_last_transfer (cooperative)
3. **De-escalating reciprocity**: current_transfer < partner_last_transfer (uncooperative)
4. **Ambiguous reciprocity**: Escalates low transfers, de-escalates high transfers (undermines cooperation)

## 3. Evolutionary Simulations

### 3.1 Population Structure

- 40 groups, 24 individuals per group (N = 960)
- Three scenarios: Repeated interactions only, Group competition only, Joint (both)

### 3.2 Model Characteristics

Six systematically varied characteristics:
1. Strategy dimensionality (2D, 3D, 4D)
2. Individual-level cancellation (coupled vs decoupled life cycle)
3. Group-level cancellation (Ξ = 0, 20, 40)
4. Competition sensitivity (λ = 0, 10, 25, 100)
5. Migration rate (mj = 8, 16)
6. Initial conditions (cooperative, selfish, random)

Total: 896 parameter combinations

### 3.3 Key Finding: Repeated Interactions Alone Fail

With 3D+ strategy space:
1. Escalating strategies become common
2. Variation in escalation becomes selectively neutral
3. Drift makes population vulnerable
4. Ambiguous reciprocity invades
5. De-escalating strategies displace ambiguous
6. Result: uncooperative equilibrium

### 3.4 Key Finding: Intergroup Competition Alone Fails

Requires delicate three-part mix:
- Coupled life cycle (game play before migration)
- λ = 100 (high sensitivity)
- mj = 8 (low migration)

Without all three, cooperation fails.

### 3.5 Key Finding: Joint Scenario Produces Super-Additivity

**Effect(Joint) > Effect(RI) + Effect(GC)**

The joint scenario works across wide conditions:
- 3D and 4D strategy spaces
- High migration (mj = 16)
- λ well below maximum
- Even with strong cancellation (Ξ = 0)

## 4. Field Experiment in Papua New Guinea

### 4.1 Setting

- Western Highlands, Papua New Guinea
- Ngenikas and Perepkas: horticultural groups ~30 km apart
- Beyond reach of state institutions
- Social preferences and local norms govern social life

### 4.2 Design

Sequential social dilemma (trust game variant):
- Endowment: 5 Papua New Guinean Kina (~half high daily wage)
- Transfers: 0-5 Kina in increments of 1
- Multiplier: 2x
- Strategy method for second movers
- Between-subjects: ingroup vs outgroup partner

### 4.3 Sample

- First movers: 36 ingroup, 37 outgroup
- Second movers: 36 ingroup, 34 outgroup

### 4.4 Results

**First movers:**
- Ingroup: ~3.5 Kina average
- Outgroup: ~1.5 Kina average
- p < 0.001 (ordinal logistic regression)

**Second movers:**
- Ingroup: **Escalating reciprocity** (slope > 1)
- Outgroup: **De-escalating reciprocity** (slope < 1)
- p < 0.001 (interaction term)

**Critical:** Only the joint scenario reliably predicts this exact pattern.

## 5. Discussion

### 5.1 The Super-Additive Effect

Neither repeated interactions alone nor intergroup competition alone reliably support cooperation. But combining them triggers powerful synergies:

> "A mechanism with critical limitations on its own may be critically important in interaction with other mechanisms."

### 5.2 Why is This Important?

The combination of mechanisms responsible for human cooperation may be **unique to humans**:

> "The combination of mechanisms responsible for human cooperation can also be special or even unique."

### 5.3 Implications

1. **For theory**: Mechanisms should not be studied in isolation
2. **For empirics**: Need designs that capture mechanism interactions
3. **For policy**: Interventions combining multiple mechanisms may be super-additive

## 6. Conclusion

Human cooperation may require the interaction of multiple mechanisms. The super-additive effect—where the joint effect exceeds the sum of individual effects—suggests that studying mechanisms in isolation may systematically underestimate their importance.

## Acknowledgements

Seminars: Harvard University, Institute for Advanced Study in Toulouse, Santa Fe Institute, University of Amsterdam, University of Lausanne, University of Konstanz, University of Zurich.

Funding: Swiss National Science Foundation (100018 185417/1 to C.E.), European Research Council (Foundation of Economic Preferences to E.F.).

## References

1. Hagen, E. H. & Hammerstein, P. (2006). Game theory and human evolution. *Theoretical Population Biology*, 69, 339-348.
2. Zefferman, M. R. (2014). Direct reciprocity under uncertainty. *Evolution and Human Behavior*, 35, 358-367.
3. Jagau, S. & van Veelen, M. (2017). Intuition and deliberation in cooperation. *Nature Human Behaviour*, 1, 1-6.
4. Choi, J.-K. & Bowles, S. (2007). The coevolution of parochial altruism and war. *Science*, 318, 636-640.
5. Richerson, P. et al. (2016). Cultural group selection. *Behavioral and Brain Sciences*, 39.
6. Boyd, R. & Richerson, P. J. (2022). Large-scale cooperation in foraging societies. *Evolutionary Anthropology*.
7. De Dreu, C. K. et al. (2022). Prosociality and intergroup conflict. *Current Opinion in Psychology*, 44, 112-116.
8. Akdeniz, A. & van Veelen, M. (2020). The cancellation effect at the group level. *Evolution*.
9. Haselton, M. G. et al. (2015). The evolution of cognitive bias. *Handbook of Evolutionary Psychology*.
10. Yamagishi, T. et al. (1999). Bounded generalized reciprocity. *Advances in Group Processes*, 16, 161-197.
[... Full reference list in YAML ...]

---

*Full text archived: 2026-01-31*
*Source: CESifo Working Paper No. 10133*
*Content level: Paper structure with key sections*
