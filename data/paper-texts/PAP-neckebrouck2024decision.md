# Decision-Making in Entrepreneurial Teams with Competing Economic and Noneconomic Goals

**Authors:** Jeroen Neckebrouck and Thomas Zellweger

**Journal:** Strategic Entrepreneurship Journal, 1–29

**Year:** 2024

**DOI:** https://doi.org/10.1002/sej.1524

---

## Abstract

We examine how entrepreneurial teams make decisions when team members have competing economic and noneconomic goals. Building on a computational model, we study how the relative importance that team members attach to their goals, team members' beliefs about available opportunities, and the decision-making process used within teams jointly shape team decisions. Our model reveals that who makes the decisions in teams matters at least as much as what preferences and beliefs team members hold and that the effects of these factors are highly intertwined. Our analysis shows that decision-making processes are an important but understudied source of heterogeneity in entrepreneurial team decision-making. We discuss implications for research on entrepreneurial teams, strategic consensus, and organizational design.

**Keywords:** computational modeling, decision-making, entrepreneurial teams, noneconomic goals, organizational design

---

## 1. Introduction

Entrepreneurial teams make a large variety of interrelated decisions, ranging from operational concerns such as hiring to more strategic decisions such as the choice of a new product-market strategy (Beckman, 2006; Klotz et al., 2014). An important insight that has emerged from recent entrepreneurship research is that these decisions are not solely driven by economic motives. Entrepreneurial team members also attach value to noneconomic goals such as maintaining control over the venture, preserving the identity of the organization, or creating positive social impact (Schulze & Zellweger, 2021; Wiklund et al., 2019). While extant research has explored the consequences of noneconomic goals in entrepreneurship (e.g., DeTienne & Chirico, 2013; Hsu et al., 2016), important questions remain as to how entrepreneurial teams make decisions when their members hold competing economic and noneconomic goals.

In this study, we explore how three key factors jointly shape team decisions in the presence of competing economic and noneconomic goals. These factors are (1) the relative importance team members attach to their economic and noneconomic goals (i.e., their goal preferences), (2) their beliefs about available opportunities (i.e., whether they think they can find solutions that satisfy both economic and noneconomic goals simultaneously), and (3) the team's decision-making process (i.e., the organizational rules for reaching a collective decision, such as the allocation of authority).

Building a formal model of decision-making in entrepreneurial teams is particularly important in this context because prior research presents seemingly contradictory findings about when noneconomic goals affect venture outcomes. Some studies suggest that pursuing noneconomic goals always hurts economic performance (e.g., Chua et al., 2015). Other studies argue that noneconomic goals can also enhance economic performance (e.g., Zellweger & Astrachan, 2008). Yet other studies indicate that the effects of noneconomic goals on economic outcomes depend on contextual factors such as the composition of the team (Neckebrouck et al., 2018). These seemingly contradictory findings suggest that the relationship between noneconomic goals and economic performance is more complex than extant theories typically assume and that a formal model can create clarity.

Our computational model specifies how teams with competing goals make collective decisions through a process of search and evaluation. Team members explore a landscape of possible decisions and evaluate them based on their goal preferences and beliefs. The team then aggregates individual evaluations into a collective decision through its decision-making process. This setup allows us to examine how the interaction between preferences, beliefs, and processes shapes team decisions in ways that would be difficult to anticipate through verbal theorizing alone.

Our model generates several core insights. First, it reveals that the decision-making process matters at least as much as preferences and beliefs in determining team decisions. Specifically, concentrating decision authority in a single team member (i.e., autocracy) can lead to very different outcomes than distributing authority more equally (i.e., majority voting). This finding is noteworthy because most existing theories of entrepreneurial decision-making focus on preferences and beliefs while paying less attention to the organizational processes through which teams reach collective decisions.

Second, our model shows that the effects of preferences, beliefs, and processes are highly intertwined. For instance, we find that concentrating authority in a team member who strongly values noneconomic goals can paradoxically improve the team's economic performance—but only under specific conditions regarding the team's beliefs about available opportunities. Similarly, the effect of team diversity in goal preferences depends critically on the decision-making process used. These complex interactions suggest that studying preferences, beliefs, or processes in isolation may yield an incomplete and sometimes misleading picture.

Third, our analysis reveals that decision-making processes are an important but underexplored source of heterogeneity in team outcomes. Even teams with identical preferences and beliefs can reach very different decisions depending on who has authority to decide. This implies that organizational design choices—such as how authority is allocated within the team—can have profound effects on venture outcomes. By highlighting the pivotal role of decision-making processes, our model opens new avenues for research at the intersection of entrepreneurship and organizational design.

Our study contributes to the literature in three main ways. First, we contribute to research on decision-making in entrepreneurial teams (e.g., Klotz et al., 2014; Knight et al., 1999; Shepherd et al., 2021) by explicitly modeling how competing goals, heterogeneous beliefs, and decision-making processes interact to shape team decisions. While prior research has studied these factors largely in isolation, our computational model allows us to examine their joint effects and uncover interaction patterns that verbal theorizing alone may not reveal.

Second, we contribute to the literature on strategic consensus in teams (e.g., Kellermanns et al., 2011; Knight et al., 1999) by demonstrating that the decision-making process is a critical but often overlooked determinant of whether teams can reach consensus and how the resulting consensus relates to firm performance. Our model shows that different processes can lead to consensus on very different decisions, even when team members have identical preferences and beliefs.

Third, we contribute to the emerging literature on organizational design in entrepreneurship (e.g., Lee, 2022; Piezunka & Schilke, 2023) by formally modeling how the allocation of decision authority within teams affects venture outcomes. Our analysis provides a theoretical foundation for understanding when different governance structures (e.g., autocracy vs. polyarchy) are more or less effective, depending on the team's goal structure and the nature of the opportunity landscape.

The remainder of this paper is structured as follows. We first review the relevant literature on decision-making in entrepreneurial teams and develop the theoretical foundations for our model. We then describe our computational model and present the results of our analysis. Finally, we discuss the implications of our findings for research and practice.

## 2. Theory Development

### 2.1. Decision-making in entrepreneurial teams

Entrepreneurial teams face a multitude of decisions that shape the trajectory of their ventures (Beckman, 2006; Klotz et al., 2014). While these decisions are often studied in isolation (e.g., hiring decisions, product choices, financing decisions), they share a common structure: team members evaluate available options based on their goals and beliefs, and the team uses some process to aggregate individual evaluations into a collective decision.

A growing body of research recognizes that entrepreneurial team members pursue both economic and noneconomic goals (Schulze & Zellweger, 2021; Wiklund et al., 2019). Economic goals relate to the financial performance of the venture, such as revenue growth, profitability, or firm value. Noneconomic goals encompass a wide range of objectives that team members value independently of their financial consequences, such as maintaining control over the venture (Wasserman, 2017), preserving the organizational identity (Foss et al., 2008), or creating positive social impact (Vedula et al., 2022).

The coexistence of economic and noneconomic goals creates tensions within entrepreneurial teams because team members may differ in the relative importance they attach to these goals (Schulze & Zellweger, 2021). For instance, one founder may prioritize rapid growth and be willing to accept external investors, while another may prefer to maintain control even at the cost of slower growth. These tensions can lead to conflict and disagreement within teams (Jehn et al., 2001), but they can also be a source of creativity and innovation if managed effectively (Ensley & Hmieleski, 2005).

### 2.2. Goal preferences

We define goal preferences as the relative importance that team members attach to their economic versus noneconomic goals. Following prior research (e.g., Gavetti et al., 2012; Greve, 2008), we conceptualize goal preferences as weights that team members assign to different goal dimensions when evaluating potential decisions. A team member with strong economic goal preferences will favor decisions that maximize financial performance, while a team member with strong noneconomic goal preferences will favor decisions that advance noneconomic objectives, even at some economic cost.

Prior research suggests that goal preferences vary significantly across team members (Schulze & Zellweger, 2021). In family firms, for example, family members often place greater weight on noneconomic goals such as maintaining family control or preserving the family legacy, while nonfamily managers may prioritize economic performance (Neckebrouck et al., 2018). Similarly, in social enterprises, founders may differ in the weight they place on social impact versus financial sustainability (Battilana & Lee, 2014).

### 2.3. Beliefs about opportunities

We define beliefs as team members' subjective assessments of the opportunity landscape they face—specifically, whether they believe it is possible to find decisions that satisfy both economic and noneconomic goals simultaneously. Some team members may hold optimistic beliefs, viewing the opportunity landscape as rich with options that advance both economic and noneconomic goals. Others may be more pessimistic, seeing economic and noneconomic goals as fundamentally in tension.

Beliefs about opportunities are shaped by prior experience (Gavetti & Levinthal, 2000), cognitive frameworks (Shane, 2000), and the information available to team members (Foss et al., 2008). Importantly, beliefs can differ across team members, creating additional heterogeneity within the team. For instance, team members with broader industry experience may see more opportunities for synergies between economic and noneconomic goals than team members with more limited experience.

The relationship between beliefs and the actual opportunity landscape is important. In some environments, economic and noneconomic goals are indeed aligned—for example, when investments in employee well-being also improve productivity. In other environments, trade-offs are unavoidable—for example, when maintaining family control requires foregoing profitable growth opportunities. Team members' beliefs may or may not accurately reflect the actual opportunity landscape, and this (mis)alignment has important consequences for team decisions.

### 2.4. Decision-making processes

We define the decision-making process as the organizational rules that a team uses to aggregate individual team members' evaluations into a collective decision. This includes the allocation of decision authority (e.g., who has the right to make which decisions), the aggregation rule (e.g., majority voting, unanimity, or autocratic decision-making), and the sequence in which options are considered.

Decision-making processes vary significantly across entrepreneurial teams. Some teams adopt autocratic processes in which a single founder or CEO makes most decisions (Wasserman, 2017). Others use more democratic processes such as majority voting or consensus-based decision-making (Sah & Stiglitz, 1986). The choice of decision-making process can depend on factors such as the team's history (Beckman, 2006), the nature of the decision (Mintzberg et al., 1976), and the legal structure of the venture (Hellmann & Wasserman, 2017).

Prior research on organizational design has long recognized that the allocation of decision authority has important consequences for organizational outcomes (Sah & Stiglitz, 1986, 1988). However, this insight has not been fully integrated into the entrepreneurship literature, where research on team decision-making has focused more on individual-level factors (preferences, cognition, experience) than on the organizational processes through which individual inputs are aggregated into team decisions (cf. Joseph & Gaba, 2020).

### 2.5. The need for a computational model

The interaction between goal preferences, beliefs, and decision-making processes creates a high-dimensional problem that is difficult to analyze through verbal theorizing alone. When team members differ in their preferences and beliefs, and when the team can choose among different decision-making processes, the number of possible configurations is large and the outcomes are often counterintuitive.

Computational modeling is well suited for studying such complex, multivariate problems (Davis et al., 2007; Harrison et al., 2007). By formally specifying the relationships between key variables and simulating outcomes under different configurations, computational models can reveal interaction effects and boundary conditions that verbal theories may not anticipate (Lomi & Larsen, 2001; Taber & Timpone, 1996).

Our model builds on the tradition of computational models in organization theory (e.g., March, 1991; Rivkin, 2000) and strategy (e.g., Rivkin & Siggelkow, 2003) but adapts this approach to the specific context of entrepreneurial teams with competing goals. Specifically, we model team members as agents who search a landscape of possible decisions, evaluate them based on their heterogeneous preferences and beliefs, and use a specified decision-making process to reach a collective choice.

## 3. Model

### 3.1. Overview

Our model represents a team of N agents (team members) who collectively make a decision by choosing a point in a two-dimensional decision space. Each point in this space is associated with an economic payoff and a noneconomic payoff. Team members evaluate points based on their goal preferences (the relative weight they assign to economic vs. noneconomic payoffs) and their beliefs (their subjective assessment of the payoff landscape). The team uses a decision-making process to aggregate individual evaluations into a collective choice.

### 3.2. The decision space

The decision space is a two-dimensional grid of size L × L, where each cell (x, y) is associated with an economic payoff E(x, y) and a noneconomic payoff NE(x, y). Both payoffs are drawn from a landscape that can exhibit varying degrees of correlation between economic and noneconomic outcomes.

We model the payoff landscape using the NK framework (Kauffman, 1993; Levinthal, 1997), which allows us to vary the ruggedness of the landscape and the correlation between economic and noneconomic payoffs. Specifically, we define a correlation parameter ρ ∈ [−1, 1] that governs the relationship between E(x, y) and NE(x, y) across the decision space:

- When ρ = 1, economic and noneconomic payoffs are perfectly positively correlated: decisions that are good for economic performance are also good for noneconomic goals.
- When ρ = 0, economic and noneconomic payoffs are uncorrelated: there is no systematic relationship between economic and noneconomic outcomes.
- When ρ = −1, economic and noneconomic payoffs are perfectly negatively correlated: any gain in economic performance comes at the cost of noneconomic goals, and vice versa.

The correlation parameter ρ captures the nature of the opportunity landscape that the team faces. High values of ρ represent environments where economic and noneconomic goals are aligned, while low or negative values represent environments characterized by trade-offs.

### 3.3. Team members

Each team member i is characterized by two parameters:

1. **Goal preference** w_i ∈ [0, 1]: The weight that team member i assigns to economic payoffs. The weight assigned to noneconomic payoffs is (1 − w_i). A team member with w_i = 1 cares only about economic performance, while a team member with w_i = 0 cares only about noneconomic goals.

2. **Belief accuracy** b_i ∈ [0, 1]: The accuracy of team member i's perception of the payoff landscape. When b_i = 1, the team member perfectly observes the true payoffs. When b_i = 0, the team member's perception is completely random. Intermediate values represent varying degrees of accuracy.

Team member i evaluates a decision at position (x, y) using a utility function:

U_i(x, y) = w_i · Ê_i(x, y) + (1 − w_i) · N̂E_i(x, y)

where Ê_i(x, y) and N̂E_i(x, y) are team member i's perceived economic and noneconomic payoffs, which depend on the true payoffs and the belief accuracy parameter b_i.

### 3.4. Search process

The team's decision-making unfolds over T periods. In each period, the team occupies a position in the decision space and considers moving to an adjacent position. The search process proceeds as follows:

1. **Proposal generation:** Each team member proposes a move to one of the neighboring positions, choosing the neighbor that maximizes their individual utility.

2. **Evaluation:** Each team member evaluates the proposed moves based on their utility function.

3. **Aggregation:** The team uses its decision-making process to select one of the proposed moves (or to stay at the current position).

4. **Movement:** The team moves to the selected position.

This process repeats for T periods, and the team's final position determines the team's economic and noneconomic payoffs.

### 3.5. Decision-making processes

We model three decision-making processes that differ in how individual evaluations are aggregated into a collective choice:

1. **Autocracy:** A single team member (the "autocrat") has the authority to select the move. The team adopts whichever move the autocrat prefers.

2. **Majority voting:** Each team member votes for their preferred move. The team adopts the move that receives the most votes. In case of a tie, the status quo (staying at the current position) is maintained.

3. **Unanimity:** All team members must agree on a move for it to be adopted. If any team member prefers the status quo, the team stays at the current position.

These three processes represent archetypes of real-world decision-making arrangements in entrepreneurial teams (Sah & Stiglitz, 1986, 1988). Autocracy corresponds to situations where a single founder or CEO has unilateral decision authority. Majority voting represents more democratic arrangements common in partnerships or boards. Unanimity represents consensus-based decision-making or situations where any team member can veto a proposed move.

### 3.6. Model parameters and simulation design

We study the model's behavior by systematically varying the key parameters:

- **Team size (N):** We vary the team size from N = 1 (solo founder) to N = 5 (larger team).
- **Goal preference distribution:** We vary the distribution of w_i across team members, from homogeneous teams (all members have the same w_i) to heterogeneous teams (members differ in w_i).
- **Landscape correlation (ρ):** We vary ρ from −1 to 1 to capture different opportunity environments.
- **Belief accuracy (b_i):** We vary b_i to study the effects of different levels of information accuracy.
- **Decision-making process:** We compare autocracy, majority voting, and unanimity.

For each parameter configuration, we run 1,000 simulations to account for stochastic variation in the payoff landscape and report average outcomes across simulations. We measure two primary outcomes: (1) the team's economic payoff at the end of the search process and (2) the team's noneconomic payoff at the end of the search process.

## 4. Results

### 4.1. Baseline: Solo founders versus teams

We first establish a baseline by comparing solo founders (N = 1) with teams of varying sizes. Solo founders serve as a benchmark because they face no aggregation problem—their individual preferences directly determine the venture's decisions.

Our simulations reveal that teams can outperform solo founders in terms of both economic and noneconomic payoffs, but only under certain conditions. Specifically, teams outperform solo founders when (1) team members bring diverse and accurate beliefs about the opportunity landscape, and (2) the team uses a decision-making process that effectively aggregates these diverse perspectives. When beliefs are inaccurate or the decision-making process is poorly suited to the team's goal structure, teams can underperform solo founders.

### 4.2. The role of goal preferences

We next examine how the distribution of goal preferences within the team affects outcomes. We compare homogeneous teams (all members share the same goal preference) with heterogeneous teams (members differ in their goal preferences).

**Finding 1: In teams with homogeneous goal preferences, the level of emphasis on noneconomic goals has a nonlinear effect on economic performance.**

When all team members share the same goal preference w, increasing the emphasis on noneconomic goals (decreasing w) initially has little effect on economic performance, but beyond a threshold, economic performance drops sharply. This nonlinear relationship arises because the payoff landscape contains regions where economic and noneconomic payoffs are partially aligned. Teams that place moderate weight on noneconomic goals can exploit these regions without sacrificing much economic performance. However, teams that place very high weight on noneconomic goals are pulled toward regions of the landscape where economic payoffs are low.

**Finding 2: Teams with heterogeneous goal preferences can outperform homogeneous teams, but only under specific conditions.**

Goal preference heterogeneity has a complex effect that depends on both the opportunity landscape and the decision-making process. In aligned landscapes (high ρ), heterogeneity has little effect because economic and noneconomic goals point in the same direction regardless of individual weights. In misaligned landscapes (low ρ), heterogeneity can be beneficial if it broadens the team's search across the landscape, but it can also be detrimental if it leads to conflict and gridlock.

### 4.3. The role of beliefs

We next examine how team members' beliefs about the opportunity landscape affect outcomes.

**Finding 3: Diverse beliefs improve team performance when combined with an appropriate decision-making process.**

When team members hold diverse beliefs about the payoff landscape, the team can explore a broader set of options and potentially discover superior solutions. However, diverse beliefs only translate into better outcomes if the decision-making process can effectively aggregate these diverse inputs. Under autocracy, diverse beliefs have limited impact because only the autocrat's beliefs matter. Under majority voting, diverse beliefs can improve outcomes by generating a wider set of proposals. Under unanimity, diverse beliefs can lead to gridlock as team members disagree about which moves are desirable.

**Finding 4: The accuracy of beliefs matters more than their diversity under autocracy, while diversity matters more than accuracy under majority voting.**

This finding highlights a fundamental trade-off in team decision-making. Autocratic teams benefit most from having a leader with accurate beliefs, because the leader's perception directly determines the team's decisions. In contrast, majority-voting teams benefit more from having diverse (even if individually less accurate) beliefs, because the aggregation process can filter out individual errors.

### 4.4. The role of decision-making processes

The central finding of our model is that the decision-making process has a profound effect on team outcomes—an effect that is at least as large as, and often larger than, the effects of preferences and beliefs.

**Finding 5: The decision-making process explains as much variance in team outcomes as goal preferences and beliefs combined.**

Across all our simulations, the decision-making process accounts for approximately 30–40% of the variance in team economic performance, compared to approximately 25–35% for goal preferences and 20–30% for beliefs. The remaining variance is explained by interactions between these factors. This finding underscores the importance of organizational design choices in shaping venture outcomes.

**Finding 6: No single decision-making process dominates across all conditions.**

Autocracy performs best when the autocrat has accurate beliefs and preferences that are well aligned with the venture's goals. Majority voting performs best when team members bring diverse beliefs and the opportunity landscape is complex. Unanimity performs best when the cost of making a wrong move is high and the team can afford to be patient, but it performs worst in dynamic environments where quick decisions are needed.

**Finding 7: Autocracy by a team member with strong noneconomic goal preferences can paradoxically improve economic performance.**

This counterintuitive finding emerges in landscapes where economic and noneconomic goals are partially aligned (moderate positive ρ). When a team member with strong noneconomic preferences is given authority, they steer the team toward regions of the landscape where noneconomic payoffs are high. In partially aligned landscapes, these regions also tend to have above-average economic payoffs. The autocrat's noneconomic focus thus acts as a heuristic that leads the team to good economic outcomes—a result that would not emerge under majority voting, where the team's diverse preferences would pull it in multiple directions.

### 4.5. Interaction effects

Our model reveals several important interaction effects that highlight the interdependence between preferences, beliefs, and processes.

**Finding 8: The effect of goal preference heterogeneity depends critically on the decision-making process.**

Under autocracy, goal preference heterogeneity has no effect on outcomes (because only the autocrat's preferences matter). Under majority voting, moderate heterogeneity improves outcomes by broadening search, but high heterogeneity hurts outcomes by creating gridlock. Under unanimity, any heterogeneity hurts outcomes by increasing the likelihood of veto.

**Finding 9: The optimal decision-making process depends on the opportunity landscape.**

In aligned landscapes (high ρ), the choice of decision-making process matters less because all team members agree on the direction of search. In misaligned landscapes (low ρ), the choice of process becomes critical. Autocracy by an economically oriented leader performs best in highly misaligned landscapes, while majority voting performs best in moderately misaligned landscapes.

**Finding 10: Belief accuracy can substitute for an appropriate decision-making process, but only partially.**

Teams with highly accurate beliefs perform reasonably well under any decision-making process because accurate beliefs guide the team toward good solutions regardless of the aggregation rule. However, even with perfect belief accuracy, the choice of decision-making process still affects outcomes because it determines which of the team's accurate perceptions are acted upon.

### 4.6. Robustness checks

We conduct several robustness checks to ensure that our findings are not driven by specific modeling assumptions. First, we vary the size of the decision space (L) and find that our results are qualitatively robust across different landscape sizes. Second, we allow team members to update their beliefs over time based on observed outcomes and find that our main findings persist, although the magnitudes of some effects change. Third, we test alternative search heuristics (e.g., random search, long-jump search) and find that our findings about the relative importance of decision-making processes are robust to the search process used.

## 5. Discussion

### 5.1. Implications for research on entrepreneurial teams

Our study contributes to the growing literature on decision-making in entrepreneurial teams (Klotz et al., 2014; Shepherd et al., 2021) by demonstrating that the decision-making process is a critical determinant of team outcomes that has received insufficient attention. Most existing research focuses on team composition (who is on the team) and team cognition (what team members think) but pays less attention to team process (how the team reaches decisions). Our model shows that process can be as important as composition and cognition.

This finding has implications for how we study entrepreneurial teams. It suggests that researchers should not only measure team members' preferences and beliefs but also carefully document the decision-making processes that teams use. Studies that focus exclusively on team composition may miss an important source of heterogeneity in team outcomes.

### 5.2. Implications for research on strategic consensus

Our model also contributes to the literature on strategic consensus (Kellermanns et al., 2005, 2011). Prior research has debated whether strategic consensus is beneficial or harmful for firm performance (González-Benito et al., 2012; Samba et al., 2018). Our model suggests that the answer depends on the decision-making process through which consensus is reached.

Under autocracy, consensus is essentially the autocrat's preference—and the quality of this consensus depends on the autocrat's beliefs and preferences. Under majority voting, consensus reflects the majority view—and the quality depends on the diversity and accuracy of the majority's beliefs. Under unanimity, consensus requires all team members to agree—and the quality depends on whether the intersection of all members' acceptable options contains good solutions.

This analysis suggests that the existing debate about strategic consensus may be partly resolved by paying closer attention to the processes through which consensus is reached. Two teams can both reach consensus but arrive at very different decisions depending on their decision-making process.

### 5.3. Implications for organizational design

Our findings have direct implications for the organizational design of entrepreneurial ventures. The finding that the decision-making process explains a substantial portion of variance in team outcomes suggests that organizational design choices deserve more attention in both research and practice.

Specifically, our model suggests that the optimal allocation of decision authority depends on:

1. **The goal structure of the team:** When team members have aligned goals, the choice of process matters less. When goals conflict, the choice becomes critical.

2. **The nature of the opportunity landscape:** In aligned landscapes, more democratic processes (majority voting) are adequate. In misaligned landscapes, more concentrated authority may be needed to provide clear direction.

3. **The accuracy and diversity of beliefs:** Teams with accurate but homogeneous beliefs benefit from processes that preserve this accuracy (autocracy with a well-informed leader). Teams with diverse but individually less accurate beliefs benefit from processes that aggregate these diverse inputs (majority voting).

These findings connect to broader research on organizational design (Piezunka & Schilke, 2023; Sah & Stiglitz, 1986) and suggest that entrepreneurial teams should be more deliberate about choosing and adapting their decision-making processes as their ventures evolve.

### 5.4. Practical implications

Our model offers several practical insights for entrepreneurial teams and their advisors:

1. **Pay attention to process, not just preferences:** Teams often focus on aligning preferences (e.g., through team-building exercises or founder agreements) but pay less attention to designing effective decision-making processes. Our model suggests that process design deserves equal or greater attention.

2. **Match the process to the landscape:** Teams operating in environments where economic and noneconomic goals are aligned can afford more democratic processes. Teams facing sharp trade-offs may benefit from concentrating authority in a well-informed leader.

3. **Leverage the paradox of noneconomic authority:** In partially aligned landscapes, giving authority to a team member who prioritizes noneconomic goals can improve economic outcomes. This counterintuitive finding suggests that teams should not automatically give authority to the most economically oriented member.

4. **Adapt the process over time:** As the venture evolves and the opportunity landscape changes, the optimal decision-making process may also change. Teams should periodically reassess whether their current process is still appropriate.

### 5.5. Limitations and future directions

Our study has several limitations that suggest avenues for future research. First, our model assumes that team members' preferences and beliefs are stable over time. In reality, preferences and beliefs evolve as team members learn from experience and interact with each other (Gavetti & Levinthal, 2000). Future research could extend our model to incorporate preference and belief dynamics.

Second, our model focuses on three archetypical decision-making processes (autocracy, majority voting, unanimity). Real-world teams often use more nuanced processes that combine elements of these archetypes—for example, delegating certain decisions to specific team members while making other decisions collectively (Lee et al., 2024). Exploring a broader range of decision-making processes is an important direction for future work.

Third, our model does not account for the costs of decision-making, such as the time and effort required to reach consensus or the political costs of overriding a team member's preferences. Incorporating these costs could change the optimal choice of decision-making process in ways that our current model does not capture.

Fourth, our model treats the opportunity landscape as exogenous. In reality, entrepreneurial teams can shape their opportunity landscapes through strategic actions such as innovation, market creation, or institutional work (Zellweger & Zenger, 2023). Endogenizing the opportunity landscape is a challenging but important extension.

Fifth, while computational models are valuable for exploring complex interactions, they also involve simplifying assumptions that may limit their generalizability. Empirical validation of our model's predictions is an important next step. We encourage researchers to test our findings using both field data on entrepreneurial teams and controlled experiments.

## 6. Conclusion

This study set out to examine how entrepreneurial teams make decisions when their members hold competing economic and noneconomic goals. Using a computational model, we have shown that the decision-making process used within teams matters at least as much as what preferences and beliefs team members hold. Moreover, the effects of these factors are highly intertwined, suggesting that studying them in isolation may yield incomplete or misleading conclusions.

Our central message is that organizational design—and specifically the allocation of decision authority—is an important but underexplored determinant of entrepreneurial team performance. By highlighting the role of decision-making processes, our study opens new avenues for research at the intersection of entrepreneurship and organizational design and provides practical guidance for entrepreneurial teams navigating the challenge of competing goals.

---

## References

Battilana, J., & Lee, M. (2014). Advancing research on hybrid organizing—insights from the study of social enterprises. *Academy of Management Annals*, 8(1), 397–441.

Beckman, C. M. (2006). The influence of founding team company affiliations on firm behavior. *Academy of Management Journal*, 49(4), 741–758.

Chua, J. H., Chrisman, J. J., De Massis, A., & Wang, H. (2015). Reflections on family firm goals and the assessment of performance. *Journal of Family Business Strategy*, 9(2), 107–113.

Davis, J. P., Eisenhardt, K. M., & Bingham, C. B. (2007). Developing theory through simulation methods. *Academy of Management Review*, 32(2), 480–499.

DeTienne, D. R., & Chirico, F. (2013). Exit strategies in family firms: How socioemotional wealth drives the threshold of performance. *Entrepreneurship Theory and Practice*, 37(6), 1297–1318.

Ensley, M. D., & Hmieleski, K. M. (2005). A comparative study of new venture top management team composition, dynamics and performance between university-based and independent start-ups. *Research Policy*, 34(7), 1091–1105.

Foss, N. J., Klein, P. G., & Bjørnskov, C. (2019). The context of entrepreneurial judgment: Organizations, markets, and institutions. *Journal of Management Studies*, 56(6), 1197–1213.

Foss, N. J., Klein, P. G., Kor, Y. Y., & Mahoney, J. T. (2008). Entrepreneurship, subjectivism, and the resource-based view: Toward a new synthesis. *Strategic Entrepreneurship Journal*, 2(1), 73–94.

Galbraith, J. R. (1974). Organization design: An information processing view. *Interfaces*, 4(3), 28–36.

Gavetti, G., Greve, H. R., Levinthal, D. A., & Ocasio, W. (2012). The behavioral theory of the firm: Assessment and prospects. *Academy of Management Annals*, 6(1), 1–40.

Gavetti, G., & Levinthal, D. A. (2000). Looking forward and looking backward: Cognitive and experiential search. *Administrative Science Quarterly*, 45(1), 113–137.

González-Benito, J., Aguinis, H., Boyd, B. K., & Suárez-González, I. (2012). Coming to consensus on strategic consensus: A mediated moderation model of consensus and performance. *Journal of Management*, 38(6), 1685–1714.

Greve, H. R. (2008). A behavioral theory of firm growth: Sequential attention to size and performance goals. *Academy of Management Journal*, 51(3), 476–494.

Hambrick, D. C., & Mason, P. A. (1984). Upper echelons: The organization as a reflection of its top managers. *Academy of Management Review*, 9(2), 193–206.

Harrison, J. R., Lin, Z., Carroll, G. R., & Carley, K. M. (2007). Simulation modeling in organizational and management research. *Academy of Management Review*, 32(4), 1229–1245.

Hellmann, T., & Wasserman, N. (2017). The first deal: The division of founder equity in new ventures. *Management Science*, 63(8), 2647–2666.

Hmieleski, K. M., & Ensley, M. D. (2007). A contextual examination of new venture performance: Entrepreneur leadership behavior, top management team heterogeneity, and environmental dynamism. *Journal of Organizational Behavior*, 28(7), 865–889.

Hsu, D. K., Wiklund, J., & Cotton, R. D. (2016). Success, failure, and entrepreneurial reentry: An experimental assessment of the veracity of self-efficacy and prospect theory. *Entrepreneurship Theory and Practice*, 41(1), 19–47.

Jehn, K. A., & Mannix, E. A. (2001). The dynamic nature of conflict: A longitudinal study of intragroup conflict and group performance. *Academy of Management Journal*, 44(2), 238–251.

Joseph, J., & Gaba, V. (2020). Organizational structure, information processing, and decision-making: A retrospective and road map for research. *Academy of Management Annals*, 14(1), 267–302.

Kauffman, S. A. (1993). *The origins of order: Self-organization and selection in evolution*. Oxford University Press.

Kellermanns, F. W., Walter, J., Floyd, S. W., Lechner, C., & Shaw, J. C. (2011). To agree or not to agree? A meta-analytical review of strategic consensus and organizational performance. *Journal of Business Research*, 64(2), 126–133.

Kellermanns, F. W., Walter, J., Lechner, C., & Floyd, S. W. (2005). The lack of consensus about strategic consensus: Advancing theory and research. *Journal of Management*, 31(5), 719–737.

Klotz, A. C., Hmieleski, K. M., Bradley, B. H., & Busenitz, L. W. (2014). New venture teams: A review of the literature and roadmap for future research. *Journal of Management*, 40(1), 226–255.

Knight, D., Pearce, C. L., Smith, K. G., Olian, J. D., Sims, H. P., Smith, K. A., & Flood, P. (1999). Top management team diversity, group process, and strategic consensus. *Strategic Management Journal*, 20(5), 445–465.

Lee, S. R. (2022). The myth of the flat start-up: Reconsidering the organizational structure of start-ups. *Strategic Management Journal*, 43(1), 58–92.

Lee, J., Park, S., & Lee, H. (2024). Polyarchy and project performance in open, distributed forms of innovation. *Strategic Organization*, 22(4), 14761270221145568.

Levinthal, D. A. (1997). Adaptation on rugged landscapes. *Management Science*, 43(7), 934–950.

Lomi, A., & Larsen, E. R. (2001). *Dynamics of organizations: Computational modeling and organization theories*. MIT Press.

March, J. G. (1991). Exploration and exploitation in organizational learning. *Organization Science*, 2(1), 71–87.

March, J. G. (1999). *The pursuit of organizational intelligence: Decisions and learning in organizations*. Blackwell Publishers.

Mintzberg, H., Raisinghani, D., & Theoret, A. (1976). The structure of 'unstructured' decision processes. *Administrative Science Quarterly*, 21(2), 246.

Neckebrouck, J., Schulze, W. S., & Zellweger, T. (2018). Are family firms good employers? *Academy of Management Journal*, 61(2), 553–585.

Piezunka, H., & Schilke, O. (2023). The dual function of organizational structure: Aggregating and shaping individuals' votes. *Organization Science*, 34(5), 1914–1937.

Rivkin, J. W. (2000). Imitation of complex strategies. *Management Science*, 46(6), 824–844.

Rivkin, J. W., & Siggelkow, N. (2003). Balancing search and stability: Interdependencies among elements of organizational design. *Management Science*, 49(3), 290–311.

Sah, R. K., & Stiglitz, J. E. (1986). The architecture of economic systems: Hierarchies and polyarchies. *American Economic Review*, 76(4), 716–727.

Sah, R. K., & Stiglitz, J. E. (1988). Committees, hierarchies and polyarchies. *The Economic Journal*, 98(391), 451–470.

Samba, C., Van Knippenberg, D., & Miller, C. C. (2018). The impact of strategic dissent on organizational outcomes: A meta-analytic integration. *Strategic Management Journal*, 39(2), 379–402.

Schulze, W., & Zellweger, T. (2021). Property rights, owner-management, and value creation. *Academy of Management Review*, 46(3), 489–511.

Shane, S. (2000). Prior knowledge and the discovery of entrepreneurial opportunities. *Organization Science*, 11(4), 448–469.

Shepherd, D. A., Souitaris, V., & Gruber, M. (2021). Creating new ventures: A review and research agenda. *Journal of Management*, 47(1), 11–42.

Taber, C. S., & Timpone, R. J. (1996). *Computational modeling* (p. 113). Sage Publications.

Van Den Steen, E. (2018). Strategy and the strategist: How it matters who develops the strategy. *Management Science*, 64(10), 4533–4551.

Vedula, S., et al. (2022). Entrepreneurship for the public good: A review, critique, and path forward for social and environmental entrepreneurship research. *Academy of Management Annals*, 16(1), 391–425.

Wasserman, N. (2017). The throne vs. the kingdom: Founder control and value creation in startups. *Strategic Management Journal*, 38(2), 255–277.

Wiklund, J., Nikolaev, B., Shir, N., Foo, M.-D., & Bradley, S. (2019). Entrepreneurship and well-being: Past, present, and future. *Journal of Business Venturing*, 34(4), 579–588.

Zellweger, T., & Astrachan, J. H. (2008). On the emotional value of owning a firm. *Family Business Review*, 21(4), 347–363.

Zellweger, T., & Zenger, T. (2023). Entrepreneurs as scientists: A pragmatist approach to producing value out of uncertainty. *Academy of Management Review*, 48(3), 379–408.

Zott, C. (2003). Dynamic capabilities and the emergence of intra-industry differential firm performance: Insights from a simulation study. *Strategic Management Journal*, 24(2), 97–125.

---

**How to cite this article:** Neckebrouck, J., & Zellweger, T. (2024). Decision-making in entrepreneurial teams with competing economic and noneconomic goals. *Strategic Entrepreneurship Journal*, 1–29. https://doi.org/10.1002/sej.1524
