# Complementarity in Organizations

**Authors:** Erik Brynjolfsson and Paul Milgrom

**Source:** The Handbook of Organizational Economics, edited by Robert Gibbons and John Roberts, Princeton University Press, 2013, Chapter 1, pp. 11–55.

---

## Introduction

Why do resistance to new technologies, resistance to new strategies, resistance to new management techniques, and the resistance to organizational change more generally seem to be so pervasive and so difficult to overcome? Why do organizational changes, when they are attempted, so frequently fail? Why do successful firms in an industry tend to look alike in many details of their practices and strategies, while at the same time differing markedly from less successful firms? Why do successful competitors find it so hard to imitate the practices and strategies of the most successful firms? In short, what are the main features of organizations, and especially of organizational design, that most demand an explanation and that most shape the behavior of the people working in those organizations?

In this chapter, we argue that much of the answer to these questions lies in a single concept: complementarity. Our objective in this chapter is to develop this concept formally, to give it empirical content, and to use it to explain the features of organizations that we have highlighted above.

A modern manufacturing company may employ flexible machinery, just-in-time inventory management, rapid product development, a broad job classification scheme for production workers, and decentralized authority over production decisions. These practices are complements: if you ask why the firm uses flexible production machines rather than rigid special-purpose ones, part of the answer is that it keeps its inventories low (so it needs to respond flexibly to demand), it introduces new products rapidly (so it needs to handle frequent changes in specifications), its workers are broadly skilled (so they can handle the variety of tasks), and its managers on the shop floor can make rapid decisions in response to changing needs without sending a request up the hierarchy.

The need for system-wide change to achieve improvements was evident even in Adam Smith's pin factory, where the resistance to improvements was particularly noteworthy. More recently, the resistance to adopting new information technologies seems to come from the resistance to new information-enabled practices such as new organizational structures.

This chapter is organized as follows. In Section 1, we develop the formal theory of complementarity. In Section 2, we review some of the most important recent empirical research on complementarity in organizations. In Section 3, we apply the theory to explain the difficulty of organizational change. In Section 4, we discuss when complementarities matter most. In Section 5, we discuss substitutes. In Section 6, we offer conclusions.

## 1. A Theory of Complementarity

### 1.1 Lattice Theory and Supermodularity

The formal foundations for the theory of complementarity were laid by Topkis (1978, 1998) and developed and applied to economics by Milgrom and Roberts (1990, 1994, 1995) and Milgrom and Shannon (1994). A key concept is that of a lattice.

A partially ordered set (S, ≥) is a set S together with a binary relation ≥ that is reflexive (x ≥ x for all x), antisymmetric (x ≥ y and y ≥ x implies x = y), and transitive (x ≥ y and y ≥ z implies x ≥ z). Given x and y in S, the join x ∨ y is the smallest element greater than or equal to both x and y, and the meet x ∧ y is the largest element less than or equal to both x and y. A lattice is a partially ordered set in which every pair of elements has a join and a meet.

For a familiar example, let S = Rn with the usual componentwise partial ordering: x ≥ y if and only if xi ≥ yi for all i. Then x ∨ y = (max(x1,y1), ..., max(xn,yn)) and x ∧ y = (min(x1,y1), ..., min(xn,yn)). Rn is a lattice under this ordering. The set {0,1}n of binary vectors is a sublattice of Rn.

A sublattice of a lattice is a subset T such that for all x, y in T, x ∨ y in T and x ∧ y in T.

**Definition.** A function f: S → R defined on a lattice S is *supermodular* if for all x, y in S,

f(x ∨ y) + f(x ∧ y) ≥ f(x) + f(y).

Supermodularity captures the idea of complementarity: raising several arguments together generates more value than raising them separately. When S is a subset of Rn and f is twice differentiable, supermodularity is equivalent to

d²f / dxi dxj ≥ 0 for all i ≠ j.

That is, the marginal return to increasing one variable is nondecreasing in all the other variables. Activities are complements when doing more of any one activity increases the marginal return to each other activity.

### 1.2 Optimization with Complementarities

We consider a decision maker who chooses x in S to maximize f(x;theta), where S is a sublattice of some lattice, f is supermodular in (x,theta), and theta is a parameter.

**Theorem 1.** (Existence) If S is a finite lattice and f: S → R, then f has a maximum on S. More generally, if S is a compact sublattice of Rn and f is upper semicontinuous, then f has a maximum on S.

**Theorem 2.** (Topkis 1978) If S is a sublattice of Rn and f: S → R is supermodular, then the set of maximizers of f is a sublattice.

The implication of Theorem 2 is that the optimal choices form a sublattice: if two different optima differ in several coordinates, then the point obtained by moving to the higher value in every coordinate where they differ is also optimal, as is the point obtained by moving to the lower value. The complementary activities cluster together at optima.

### 1.3 Comparative Statics

**Theorem 3.** (Topkis 1978; Milgrom and Shannon 1994) If f(x;theta) is supermodular in (x,theta) and S does not depend on theta, then the set of maximizers of f is nondecreasing in theta (in the strong set order).

In particular, the largest and smallest optimal choices x*(theta) are nondecreasing in theta.

**Theorem 4.** (Milgrom and Roberts 1990) Suppose that f(x;theta) is supermodular in (x,theta) and the vector theta increases. Then the optimal response involves increasing all the x variables, even those whose direct dependence on theta is zero, provided that f is strictly supermodular in the relevant pairs.

This is the indirect or cascade effect of complementarity: a change that directly affects only one or a few activities leads to adjustments in all the complementary activities.

### 1.4 Testing for Complementarity

**Theorem 5.** (Milgrom and Roberts 1990; Athey and Stern 2002) If activities are complements (f is supermodular in the activities), then the optimal levels of the activities are positively correlated across observations with different parameter values.

This result underlies the empirical approach of testing for complementarity by looking for clustering of activities. However, as Athey and Stern (2002) emphasize, the converse is not necessarily true: positive correlation of activities does not necessarily imply complementarity, because it can also arise from unobserved heterogeneity.

### 1.5 Uniqueness and Stability

**Theorem 6.** If f is strictly supermodular, then the set of maximizers is a singleton for generic parameter values.

**Theorem 7.** (Milgrom and Roberts 1996) In a system of complements, long-run responses to parameter changes are always at least as large as short-run responses.

This is a generalization of the LeChatelier principle from thermodynamics to economics. When a parameter changes, the short-run response accounts for direct effects only. In the long run, all the complementary adjustments can be made, and each reinforces the others, leading to a larger total response.

*Proof sketch.* Suppose theta increases and we first allow only x1 to adjust, arriving at a short-run optimum. Then we let x2 adjust as well. By supermodularity, the increase in x1 raises the marginal return to x2, so x2 increases. But then the increase in x2 further raises the marginal return to x1, so x1 increases still more. The total long-run adjustment must therefore exceed the initial short-run one.

### 1.6 Organizational Inertia

**Theorem 8.** In a system of complements with multiple local optima, the cost of switching from one optimum to another can be much larger than the cost of any single change.

Consider a firm at a local optimum A that contemplates switching to a different local optimum B. If the activities are complements, then changing some but not all of them from A to B is costly—worse than either A or B. The firm must change all the activities simultaneously, or at least must be willing to endure a period of losses as it transitions from one system to another.

### 1.7 Imitation Difficulty

**Theorem 9.** In a system of complements, imitating a subset of a successful firm's practices may actually reduce performance.

Suppose firm A has a system of complementary practices (high, high, high, high) and firm B has (low, low, low, low). If firm B tries to imitate firm A by adopting just two of A's four practices, arriving at (high, high, low, low), firm B may find that its performance is lower than before. The reason is that the two practices it has changed are no longer complementary with the two it has not changed.

### 1.8 Performance Measurement

**Theorem 10.** In a system of complements, the performance contribution of any individual practice is difficult to measure because it depends on the values of all complementary practices.

If a firm raises one practice from low to high while holding all others constant, the measured effect will be small. Standard empirical methods that look for the effect of one variable while controlling for others will underestimate the returns to system-wide changes.

## 2. Empirical Evidence on Complementarity

### 2.1 Information Technology and Complementary Organizational Investments

The empirical study of complementarities in organizations is closely associated with information technology (IT). Brynjolfsson and Hitt (2000, 2003) documented that the returns to IT investment depend critically on complementary organizational investments.

Brynjolfsson and Hitt (2003) found that firms that invested in IT and also made complementary organizational changes—adopting team-based work structures, broad job classifications, decentralized decision making, and increased worker training—had output that was about 5% higher than would be predicted from the IT investment alone. Moreover, this effect grew substantially over time: the one-year returns to IT were similar to the returns to other types of capital, but the five-to-seven year returns were much larger.

The explanation is that IT is complementary with organizational change, and organizational change takes time. In the short run, a firm can buy computers, but it takes years to redesign work processes, retrain workers, and reorganize the firm to take full advantage of the new technology.

Bresnahan, Brynjolfsson, and Hitt (2002) found evidence of three-way complementarity among IT capital, workplace organization, and the use of skilled labor. They argued that the demand for skilled labor was driven not by IT per se, but by the organizational practices that are complementary with IT.

### 2.2 Human Resource Management Practices

Ichniowski, Shaw, and Prennushi (1997) provide some of the most compelling evidence for complementarity in organizations. They studied 36 homogeneous steel finishing lines, collecting monthly data on productivity and detailed information on human resource management (HRM) practices.

They identified a cluster of complementary HRM practices: incentive pay, teams, flexible job assignments, employment security, and training. Lines that adopted the full cluster of practices had productivity about 6.7% higher than lines with the traditional approach (narrow job definitions, no teams, strict work rules, etc.).

Crucially, they found that individual HRM practices had no statistically significant effects on productivity when adopted in isolation. The whole system was greater than the sum of its parts. This result is exactly what the theory predicts: in a system of complements, the marginal return to any single practice depends on the levels of all the other practices.

### 2.3 CompStat Policing

Garicano and Heaton (2010) studied the adoption of the CompStat management system by police departments. CompStat involves the intensive use of information technology (crime mapping, real-time data analysis) combined with organizational changes (regular meetings of top commanders, accountability for results, delegation of authority to precinct commanders, and rapid response to emerging crime patterns).

They found that departments adopting the full CompStat system achieved crime clearance rates about 2.2 percentage points higher than departments that did not adopt it. However, departments that adopted only the IT component or only the organizational component showed no statistically significant improvement.

This is a classic complementarity finding: the bundle of IT and organizational practices works, but neither component alone has a detectable effect.

### 2.4 Supermarkets

The supermarket industry provides another illustration. The introduction of scanners and barcodes in the 1970s and 1980s was complementary with changes in inventory management, just-in-time delivery, and product variety. Scanners provided the data needed for fine-grained inventory management; just-in-time delivery reduced the need for large inventories; and the resulting efficiency gains made it profitable to offer a wider variety of products.

Firms that adopted scanners without making the complementary changes in inventory management and supply chain practices gained less than those that adopted the full system.

## 3. Why Is Organizational Change So Difficult?

The theory of complementarity provides a compelling explanation for the well-known difficulty of organizational change. The basic idea is illustrated by a fitness landscape argument.

Consider a firm that has two practices, each of which can be either low or high. If the practices are complements, the fitness landscape has two peaks—(low, low) and (high, high)—and two valleys—(low, high) and (high, low). A firm at the (low, low) peak that wants to move to the (high, high) peak must cross one of the valleys.

The difficulty increases dramatically with the number of complementary practices. If there are n complementary practices, the firm must change all n simultaneously. Any partial change—changing k < n practices from low to high—is a valley: the changed practices are no longer complementary with the unchanged ones.

This explains several well-documented facts about organizational change:

1. **Organizational change often fails.** The firm may change some practices but not others, ending up in a valley.

2. **Successful change requires a comprehensive vision.** The leader must understand the entire system of complementary practices and how they fit together.

3. **Change is all-or-nothing.** Firms are observed either at the old system or the new system, with few in between.

4. **Crises can facilitate change.** If a negative shock pushes the firm into a valley anyway, the cost of completing the transition to the new peak is reduced.

5. **Outside leaders may be more effective at implementing change.** They are less committed to the existing system and may find it easier to envision comprehensive changes.

The difficulty of organizational change is compounded by information and coordination problems. Even if the leader knows that the entire system must be changed, it may be difficult to communicate this to all the people whose behavior must change.

## 4. When Do Complementarities Matter Most?

Complementarities are always present in organizations, but they matter most in environments with rapid change and high uncertainty. The reason is that complementarities create inertia, and inertia is most costly when the environment is changing rapidly.

Information technology has been a major driver of increased complementarities in organizations. IT enables new organizational forms (decentralized decision making, team-based work, flexible manufacturing) that are strongly complementary with each other and with IT itself. As IT improves, the optimal organizational form shifts, and the complementarities among the components of the new form create strong incentives to change the entire system.

Globalization has also increased the importance of complementarities by increasing competition and the pace of change. The combination of rapid technological change and intense competition means that the ability to manage complementary organizational change is a critical capability.

## 5. Substitutes

The dual of supermodularity is submodularity. A function f is submodular if

f(x ∨ y) + f(x ∧ y) ≤ f(x) + f(y).

In the smooth case, this is equivalent to d²f/dxi dxj ≤ 0 for all i ≠ j. Activities are substitutes when doing more of one decreases the marginal return to others.

Substitution is common in organizations. For example, monitoring and incentive pay may be substitutes: if a firm can perfectly observe worker effort, it does not need high-powered incentive pay, and vice versa. Similarly, formal rules and informal norms may be substitutes.

Many real organizational design problems involve a mix of complements and substitutes. Milgrom and Roberts (1995) develop the theory for the case of mixed complements and substitutes. The key insight is that the grouping of activities into complementary clusters, where different clusters may be substitutes for each other, creates a natural modular structure in the organization.

## 6. Conclusions

The theory of complementarity provides a unified framework for understanding many important features of organizations. It explains why practices cluster, why organizational change is difficult, why imitation of successful competitors fails, and why individual practice contributions are hard to measure. The theory is grounded in the mathematical structure of supermodular functions and lattices, which provides clear and testable predictions.

The empirical evidence strongly supports the theory. Studies of IT and organizational change, HRM practices, policing, and supermarkets all find that practices are adopted as systems, that the system-wide effect exceeds the sum of individual effects, and that partial adoption can be counterproductive.

Looking ahead, several directions seem promising. First, better empirical methods are needed to identify complementarities, particularly methods that can distinguish complementarity from unobserved heterogeneity. Second, dynamic models of organizational change would help us understand the transition process and the conditions under which change is likely to succeed. Third, the interaction between complementarity and other features of organizations—such as incentives, authority, and communication—deserves further study.

## References

Acemoglu, D., P. Aghion, C. Lelarge, J. Van Reenen, and F. Zilibotti. 2007. "Technology, Information, and the Decentralization of the Firm." *Quarterly Journal of Economics* 122 (4): 1759–99.

Aghion, P., and J. Tirole. 1997. "Formal and Real Authority in Organizations." *Journal of Political Economy* 105 (1): 1–29.

Aral, S., E. Brynjolfsson, and D. J. Wu. 2006. "Which Came First, IT or Productivity? Virtuous Cycle of Investment and Use in Enterprise Systems." ICIS 2006 Proceedings.

Athey, S., and S. Stern. 1998. "An Empirical Framework for Testing Theories about Complementarity in Organizational Design." NBER Working Paper No. 6600.

Athey, S., and S. Stern. 2002. "The Impact of Information Technology on Emergency Health Care Outcomes." *RAND Journal of Economics* 33 (3): 399–432.

Baker, G., R. Gibbons, and K. J. Murphy. 2002. "Relational Contracts and the Theory of the Firm." *Quarterly Journal of Economics* 117 (1): 39–84.

Baker, G., and T. Hubbard. 2003. "Make versus Buy in Trucking: Asset Ownership, Job Design, and Information." *American Economic Review* 93 (3): 551–72.

Baker, G., and T. Hubbard. 2004. "Contractibility and Asset Ownership: On-Board Computers and Governance in US Trucking." *Quarterly Journal of Economics* 119 (4): 1443–79.

Bartel, A., C. Ichniowski, and K. Shaw. 2007. "How Does Information Technology Really Affect Productivity? Plant-Level Comparisons of Product Innovation, Process Improvement, and Worker Skills." *Quarterly Journal of Economics* 122 (4): 1721–58.

Bloom, N., L. Garicano, R. Sadun, and J. Van Reenen. 2009. "The Distinct Effects of Information Technology and Communication Technology on Firm Organization." NBER Working Paper No. 14975.

Bloom, N., R. Sadun, and J. Van Reenen. 2010. "Recent Advances in the Empirics of Organizational Economics." *Annual Review of Economics* 2: 105–37.

Bresnahan, T., E. Brynjolfsson, and L. Hitt. 2002. "Information Technology, Workplace Organization, and the Demand for Skilled Labor: Firm-Level Evidence." *Quarterly Journal of Economics* 117 (1): 339–76.

Brynjolfsson, E., and L. Hitt. 2000. "Beyond Computation: Information Technology, Organizational Transformation and Business Performance." *Journal of Economic Perspectives* 14 (4): 23–48.

Brynjolfsson, E., and L. Hitt. 2003. "Computing Productivity: Firm-Level Evidence." *Review of Economics and Statistics* 85 (4): 793–808.

Brynjolfsson, E., L. M. Hitt, and S. Yang. 2002. "Intangible Assets: Computers and Organizational Capital." *Brookings Papers on Economic Activity* 2002 (1): 137–81.

Brynjolfsson, E., A. McAfee, M. Sorell, and F. Zhu. 2008. "Scale without Mass: Business Process Replication and Industry Dynamics." Harvard Business School Technology & Operations Management Unit Research Paper No. 07-016.

Brynjolfsson, E., A. Renshaw, and M. Van Alstyne. 1997. "The Matrix of Change." *Sloan Management Review* 38 (2): 37–54.

Caroli, E., and J. Van Reenen. 2001. "Skill-Biased Organizational Change? Evidence from a Panel of British and French Establishments." *Quarterly Journal of Economics* 116 (4): 1449–92.

Dessein, W., and T. Santos. 2006. "Adaptive Organizations." *Journal of Political Economy* 114 (5): 956–95.

Garicano, L. 2000. "Hierarchies and the Organization of Knowledge in Production." *Journal of Political Economy* 108 (5): 874–904.

Garicano, L., and P. Heaton. 2010. "Information Technology, Organization, and Productivity in the Public Sector: Evidence from Police Departments." *Journal of Labor Economics* 28 (1): 167–201.

Garicano, L., and E. Rossi-Hansberg. 2006. "Organization and Inequality in a Knowledge Economy." *Quarterly Journal of Economics* 121 (4): 1383–1435.

Holmstrom, B., and P. Milgrom. 1991. "Multitask Principal-Agent Analyses: Incentive Contracts, Asset Ownership, and Job Design." *Journal of Law, Economics, and Organization* 7 (special issue): 24–52.

Holmstrom, B., and P. Milgrom. 1994. "The Firm as an Incentive System." *American Economic Review* 84 (4): 972–91.

Ichniowski, C., and K. Shaw. 1999. "The Effects of Human Resource Management Systems on Economic Performance: An International Comparison of US and Japanese Plants." *Management Science* 45 (5): 704–21.

Ichniowski, C., K. Shaw, and G. Prennushi. 1997. "The Effects of Human Resource Management Practices on Productivity: A Study of Steel Finishing Lines." *American Economic Review* 87 (3): 291–313.

Kandel, E., and E. P. Lazear. 1992. "Peer Pressure and Partnerships." *Journal of Political Economy* 100 (4): 801–17.

Lazear, E. P. 2000. "Performance Pay and Productivity." *American Economic Review* 90 (5): 1346–61.

MacDuffie, J. P. 1995. "Human Resource Bundles and Manufacturing Performance: Organizational Logic and Flexible Production Systems in the World Auto Industry." *Industrial and Labor Relations Review* 48 (2): 197–221.

Milgrom, P., and J. Roberts. 1990. "The Economics of Modern Manufacturing: Technology, Strategy, and Organization." *American Economic Review* 80 (3): 511–28.

Milgrom, P., and J. Roberts. 1994. "Comparing Equilibria." *American Economic Review* 84 (3): 441–59.

Milgrom, P., and J. Roberts. 1995. "Complementarities and Fit: Strategy, Structure, and Organizational Change in Manufacturing." *Journal of Accounting and Economics* 19 (2–3): 179–208.

Milgrom, P., and J. Roberts. 1996. "The LeChatelier Principle." *American Economic Review* 86 (1): 173–79.

Milgrom, P., and C. Shannon. 1994. "Monotone Comparative Statics." *Econometrica* 62 (1): 157–80.

Rivkin, J. W. 2000. "Imitation of Complex Strategies." *Management Science* 46 (6): 824–44.

Roberts, J. 2004. *The Modern Firm: Organizational Design for Performance and Growth.* Oxford: Oxford University Press.

Topkis, D. M. 1978. "Minimizing a Submodular Function on a Lattice." *Operations Research* 26 (2): 305–21.

Topkis, D. M. 1998. *Supermodularity and Complementarity.* Princeton, NJ: Princeton University Press.
