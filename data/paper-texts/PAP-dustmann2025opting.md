# Opting Out of Centralized Collective Bargaining: Evidence from Italy

**Authors:** Christian Dustmann, Chiara Giannetto, Lorenzo Incoronato, Chiara Lacava, Vincenzo Pezone, Raffaele Saggio, Benjamin Schoefer
**Year:** 2025
**Source:** NBER Working Paper No. 34076
**DOI:** 10.3386/w34076

---

NBER WORKING PAPER SERIES

OPTING OUT OF CENTRALIZED COLLECTIVE BARGAINING:
EVIDENCE FROM ITALY
Christian Dustmann
Chiara Giannetto
Lorenzo Incoronato
Chiara Lacava
Vincenzo Pezone
Raffaele Saggio
Benjamin Schoefer
Working Paper 34076
http://www.nber.org/papers/w34076
NATIONAL BUREAU OF ECONOMIC RESEARCH
1050 Massachusetts Avenue
Cambridge, MA 02138
July 2025
We thank Manudeep Bhuller, David Card, Pat Kline, Salvatore Lattanzio (discussant), Katrine
Løken, Enrico Moretti, Uta Schoenberg, and audiences at the NBER Labor Studies meeting, the
6th Bank of Italy-CEPR Workshop on Labour Market Policies and Institutions, the 18th CSEFIGIER Symposium on Economics and Institutions, the Bergen Labor Workshop, CReAMRFBerlin Workshops, the 17th Nordic Summer Institute in Labor Economics in Uppsala,
VisitINPS seminars, VisitINPS VI Conference, UC Berkeley, University of Southern California,
University of Siena, LMU Munich, University of Barcelona, Universitat Autonoma de Barcelona,
VATT Helsinki, University of Konstanz, ifo Institute Fürth, and IWH-Halle. We also thank
Gabriele Rovigatti and coauthors for sharing their data on shop opening hours liberalization.
Several details regarding the institutional context are drawn from conversations with Mario Sassi
and Guido Lazzarelli, who we also thank. Dustmann, Giannetto and Incoronato acknowledge
funding from the Rockwool Foundation Berlin (RFBerlin) through the project "Institutions, Wage
Setting and Labour Market Performance in Continental Europe: Evidence from Italy." Lacava
acknowledges funding by Next Generation EU (Growing Resilient, INclusive and Sustainable
PE00000018 – CUP E63C22002140007). The realization of this article was made possible thanks
to the VisitINPS Scholars program. The findings and conclusions expressed are solely those of
the authors and do not represent the views of INPS or the National Bureau of Economic
Research.
NBER working papers are circulated for discussion and comment purposes. They have not been
peer-reviewed or been subject to the review by the NBER Board of Directors that accompanies
official NBER publications.
© 2025 by Christian Dustmann, Chiara Giannetto, Lorenzo Incoronato, Chiara Lacava, Vincenzo
Pezone, Raffaele Saggio, and Benjamin Schoefer. All rights reserved. Short sections of text, not
to exceed two paragraphs, may be quoted without explicit permission provided that full credit,
including © notice, is given to the source.


---
Opting Out of Centralized Collective Bargaining: Evidence from Italy
Christian Dustmann, Chiara Giannetto, Lorenzo Incoronato, Chiara Lacava, Vincenzo Pezone,
Raffaele Saggio, and Benjamin Schoefer
NBER Working Paper No. 34076
July 2025
JEL No. E02, E24, J0, J3, J5, J6
ABSTRACT
This paper presents micro-empirical evidence on the effects of wage-setting decentralization. Our
setting is Italy, where employers are required to comply with occupation- and industry-specific
wage floors set by national collective bargaining agreements. We show that opting out of these
agreements reduces wages but increases workers’ employment and retention within firms. These
effects are most pronounced in the more productive North, where the overall impact on workers’
earnings is slightly positive. In contrast, in the South, wage losses outweigh employment gains,
leading to a net decline in earnings. We also find that increased wage-setting flexibility is associated
with higher firm survival rates in both regions. The regional divergence in outcomes aligns with a
monopsony framework in which productivity and labor supply elasticities vary spatially.

Christian Dustmann
University College London
Department of Economics
c.dustmann@ucl.ac.uk

Vincenzo Pezone
Tilburg University
Department of Finance
v.pezone@tilburguniversity.edu

Chiara Giannetto
University College London
c.giannetto@ucl.ac.uk

Raffaele Saggio
University of British Columbia
Department of Economics
and NBER
rsaggio@mail.ubc.ca

Lorenzo Incoronato
University of Naples Federico II
lorenzoincoronato@gmail.com
Chiara Lacava
University of Naples Federico II
Department of Economics and Statistics
chiara.lacava@unina.it

Benjamin Schoefer
University of California, Berkeley
Department of Economics
and NBER
schoefer@berkeley.edu


---
1 Introduction
A widely recognized feature of centralized, high-coverage collective bargaining regimes, prevalent
in many European countries (see Bhuller, Moene, Mogstad, and Vestad, 2022; Jäger, Naidu, and
Schoefer, 2024), is their role in establishing minimum labor standards for workers and firms, such as
wage floors for various occupations. However, their rigidity can also lead to significant distortions
(Visser, 2013). For instance, strict coverage requirements often ignore firm-specific challenges and
regional labor market differences. As a result, firms facing downturns or unfavorable regional
conditions may be forced to reduce employment or shut down entirely in response to negative shocks.
To address these trade-offs, the OECD (2019) has proposed a system of "coordinated
decentralization," in which centralized agreements, such as national or sector-level frameworks, set
broad negotiation guidelines while allowing individual firms to opt out and negotiate wages and other
labor provisions directly with their workforces. Such decentralization could enhance competitiveness
and employment stability but may also lead to wage reductions—a mechanism referred to as the
"competitiveness channel," emphasized in models of optimal decentralization of bargaining regimes
(Calmfors and Driffill, 1988; Jimeno and Thomas, 2013).1 Moreover, in frictional labor markets,
allowing firms to opt out of centralized collective bargaining can reduce both wages and employment,
leading to clear losses in aggregate earnings.2
Despite the central role that collective bargaining regimes play in many labor markets, microempirical evidence on the benefits and costs of decentralization for firms and workers remains
limited. The main challenges for empirical assessment are twofold: first, accurately identifying in
micro-data which firms and workers opt out of centralized collective bargaining regimes, and, second,
obtaining suitable quasi-experimental variation in opt-out events to enable causal inference.

1

Dustmann et al. (2014) highlight that the German system of industrial relations provided precisely this kind of flexibility
through "opening clauses," which allowed firms to renegotiate sector- and region-specific agreements at the firm level.
They argue that while this mechanism may have constrained wage growth at the lower end of the earnings distribution, it
enhanced the competitiveness of German firms and helped preserve jobs within the country.
2
This result is the mirror image of the well-known finding that minimum wages can increase employment in
monopsonistic labor markets (Card and Krueger, 2016).

2


---
This paper addresses these challenges by examining important episodes of decentralization of
industrial relations in Italy. Italy is an ideal laboratory, as it features rigid, heavily centralized
collective bargaining institutions and imposes national wage floor schedules for each sector that are
frequently binding, particularly in low-productivity firms and regions (see, e.g., Boeri, Ichino,
Moretti, and Posch, 2021). Following the Great Recession, pressure to reform Italy’s labor market
institutions has intensified (Boeri and Garibaldi, 2019; Damiani, Pompei and Ricci, 2023).3 At the
same time, employers have increasingly sought to circumvent rigid regulations and achieve greater
flexibility within the existing system. Our paper examines these emerging strategies firms use to opt
out of centralized collective bargaining, investigating two separate settings.
First, we analyze a prominent case of withdrawal by a group of 56 large employers in the mass-retail
sector (including some multinationals, such as IKEA, ZARA, and Carrefour, but mainly consisting
of Italian companies) from their employer association, Confcommercio (CC), in 2011. The CC
represented virtually all retail sector employers, and their provisions, such as restrictions on opening
hours, tended to favor small businesses. The opt-out from the CC collective agreement allowed large
retail employers to negotiate separately with unions, gaining greater flexibility in labor arrangements.
This event lends itself to a research design that compares the outcomes of workers in the mass-retail
sector with those of similar workers who remained covered by the CC collective agreement, before
and after the opt-out occurred.
Second, we examine opt-outs where individual employers leave their original collective bargaining
agreement (CBA—Contratti Collettivi Nazionali del Lavoro) to adopt so-called "pirate
agreements"—contracts with small unions that offer more flexible working conditions and lower
wage floors. These opt-outs were facilitated by a regulatory loophole that gained traction after the

3

A prominent example is Sergio Marchionne, the CEO of Fiat (and later Fiat Chrysler Automobiles) from 2004 until
2018. Marchionne advocated for more flexible labor relations, arguing that centralized wage bargaining constrained Fiat’s
competitiveness. He aimed to shift wage bargaining to the company level, enabling Fiat to negotiate directly with workers
at individual plants instead of adhering to a national contract negotiated by industry-wide employer associations and
unions.

3


---
Great Recession. Pirate agreements grew rapidly during the 2010s, and by 2019, covered half a
million workers, representing 3% of total private-sector employment. This event complements the
first one described above, as it allows us to study the consequences of opting out not only in the massretail sector but also across a broader set of industries and firms.
To examine the effects of firms' opt-outs on worker outcomes, we combine data on collective
bargaining agreements (CBAs) with detailed matched employer-employee records from the Italian
Social Security Institute (INPS), covering the universe of private-sector workers and firms in Italy
from 2005 to 2019. A key advantage of this dataset is that it allows us to observe the specific CBA
applied to each job, enabling precise identification of firm opt-outs from their existing CBA. In our
data, we can precisely identify the firms involved in the retail-sector opt-out and the affected workers.
Moreover, our matched contract-firm-worker data allow us to directly observe idiosyncratic
transitions of individual firms from a standard CBA to a pirate CBA at the worker level.4
To study the effects of opt-out events, we employ a matched difference-in-differences design to
compare workers (and firms) subject to the opt-out to a suitable control group. Specifically, for each
of the two opt-out events that we have described above, we match each treated observation with a
comparable control peer with the same standard CBA before the opting-out event and other similar
observable characteristics. We then track changes in outcomes between this treatment and control
group before and after the opt-out event. Our main analysis centers on the consequences of opting out
for incumbent workers, i.e., existing employees whose employer has decided to opt out of centralized
collective bargaining.
Our findings broadly support the competitiveness channel, both in the case of the retail secession and
the pirate agreements, indicating that opt-outs lead to significant wage reductions for affected
workers. This suggests that firms leveraged increased flexibility to lower wages (relative to suitable

4
Throughout the text, we use the terms “standard CBA,” “traditional CBA,” and “national CBA” interchangeably to refer
to collective agreements signed by Italy’s main unions, as detailed in Section 2.

4


---
control firms). At the same time, employment stability improves, as workers subject to an opt-out are
more likely to remain employed at their original firm. The positive employment effect offsets the
negative wage impact, leaving overall earnings unchanged. In the longer run, wages decline by 2-3%
for both types of opt-outs compared to control workers, while the probability of remaining employed
(with any employer) increases by 3-4 percentage points, primarily due to higher retention with the
original employer.
We also estimate firm-level effects of opting out. For firms adopting pirate agreements, labor costs
decline by approximately 3% compared to control firms, suggesting that firms leverage opt-outs to
reduce wage expenses. Moreover, we observe a positive impact on firm survival, with the probability
of remaining in operation increasing by approximately four percentage points in the first one to two
years following the opt-out, but then declining.
Finally, we examine regional heterogeneity by comparing the effects of opt-outs in the Center-North
and the South of Italy, where national CBA wage floors are particularly restrictive due to lower
average productivity (Boeri et al., 2021). Across both settings, the positive employment effects are
concentrated primarily among incumbent workers in the Center-North. In contrast, the overall
employment probability for Southern workers does not increase significantly, particularly over longer
time horizons. Consequently, opting out reduces total labor earnings for workers in the South, while
the effects are negligible or even positive for those in the Center-North. We speculate that this
asymmetry may stem from differences in labor market competition faced by Southern versus
Northern firms. In the South, firms tend to be less productive but also face less labor market
competition than in the North (Mottironi, 2024). As a result, a Southern firm opting out of its national
CBAs can exert a higher degree of monopsonistic labor market power, which results in lower wages
and employment after the opt-out event (Card and Krueger, 2016; Azar, Huet-Vaughn, Marinescu,
Taska, and von Wachter, 2023).

5


---
Our paper contributes to the emerging literature on the effects of opting out of centralized collective
bargaining, which has so far relied on smaller datasets and survey data to identify opt-outs (Dahl, le
Maire and Munch, 2013; Gürtzgen 2016) rather than administrative, population-level data. Moreover,
it has primarily focused on wages (Lucifora and Vigani, 2021), whereas we examine the trade-off
between wage flexibility and employment gains. In the context of Italy, Lucifora and Vigani (2021)
analyze the rise of pirate agreements, one of our two sources of variation, and document substantial
wage penalties. We extend their analysis in several ways: we examine a broader set of outcomes,
particularly employment probabilities; we leverage the entire universe of Italian private-sector
workers rather than a smaller random sample, allowing us to study the full scope of pirate agreements
in Italy; and we incorporate a second source of variation by studying the retail-sector opt-out event,
applying a harmonized research design across both cases.
Dahl et al. (2013) examine the gradual decentralization of wage bargaining in Denmark, utilizing
longitudinal data and a fuzzy approach based on occupation and sector codes to identify shifts in joblevel bargaining regimes. Gürtzgen (2016) studies the effects of manufacturing and mining firms
leaving industry-level agreements in Germany but relies on survey data to infer opt-out events. Our
paper extends these analyses by identifying opt-outs directly from administrative data, allowing for
sharper variation in identifying bargaining regime shifts. Moreover, our setting—Italy—features a
more rigid, more centralized and higher-coverage bargaining system at baseline than Denmark or
Germany (Dustmann, Fitzenberger, Schönberg, and Spitz-Oener, 2014; Jäger, Noy, and Schoefer,
2022). Finally, whereas Dahl et al. (2013) and Gürtzgen (2016) focus on periods of relative stability
(1992–2001 and 1999–2007, respectively), our analysis covers a period of severe economic
challenges for European labor markets, making it particularly relevant to the policy debate that
motivates our study.
The paper is structured as follows. Sections 2 and 3 describe the institutional set-up, providing details
on the Italian collective bargaining system (Section 2) and the two opting-out settings we study

6


---
(Section 3). Section 4 describes the administrative data sources. Section 5 explains the harmonized
empirical design. Section 6 reports the main results, separately for the two opting-out settings. Section
7 examines regional heterogeneity in our findings and offers a theoretical framework that is consistent
with them. The last section concludes.
2 Institutional Background
Industrial relations in Italy are based on national sector-level collective bargaining agreements
(CBAs), which serve as the primary regulatory framework through which trade unions and employer
associations jointly establish the rules governing employment relationships.5 Typically, CBAs are
signed by associations that represent their respective sectors. Although no legal criteria explicitly
define representativeness, CBAs have historically been signed by the three largest workers' unions,
and the term "representative" generally refers to CBAs endorsed by these unions (henceforth referred
to as traditional unions).6 Firms could adopt any CBA available in their sector, even if not among the
signatory parties. Importantly, a sector’s representative CBA also applies to workers not members of
the union that signed the CBA. As a result, CBA coverage is universal, placing Italy at the very top
of OECD countries in terms of collective bargaining coverage (ICTWSS database, OECD, 2024).7
Besides establishing broad employment conditions (e.g., vacations and working hours), CBAs, which
typically last three years, set a schedule of wage floors for different (typically eight) job titles (livelli
di inquadramento), which roughly correspond to different occupations. Wage floors are periodically
adjusted following a predetermined schedule to account for expected inflation. Upon expiration,

The key role of CBAs is established by the Italian Constitution (Article 39): "Registered trade unions [...] may, through
a unified representation that is proportional to their membership, enter into collective labor agreements that have a
mandatory effect for all persons belonging to the categories referred to in the agreement."
6
These unions are Confederazione Generale Italiana del Lavoro (CGIL), Confederazione Italiana Sindacati Lavoratori
(CISL), and Unione Italiana del Lavoro (UIL). They have long dominated Italian industrial relations and have branches
representing workers in each sector of the Italian economy.
7
One implication is that an employer seeking to opt out of the sectoral CBA must persuade unions to sign a new
agreement. This process is not without costs. In the case of Fiat (discussed in Footnote 3), for example, the company’s
threat to shut down its Italian plants played a crucial role in securing union approval for a separate agreement.
5

7


---
CBAs are expected to be immediately renewed; however, in the frequent case of delays, the expired
CBA remains in force until a new agreement is reached.
In addition to CBA provisions, employers and firm-level union delegations can negotiate firm-level
agreements (see Boeri, 2014; Dell’Aringa, 2017). However, this second tier of bargaining is
subordinate to sector-level bargaining. Firm-level agreements may only regulate matters explicitly
authorized by the CBA and can deviate from sector-level agreements only to improve worker
conditions. For example, firm-level agreements can establish "top-ups," i.e., premia paid by the firm
above the wage floor set by the CBA (Guiso, Pistaferri and Schivardi, 2005).
The actual wage received by workers is determined by the CBA wage floor, with the possibility of
an additional top-up if a firm-level agreement is in place. However, D’Amuri and Nizzi (2017) report
that only 20% of firms with more than 20 employees adopted firm-level contracts between 2010 and
2016. As a result, firm-level bargaining in Italy remains limited in scope, particularly since such
agreements cannot set wages below the CBA floors.8 These constraints have been a key factor behind
the opt-out events examined in this paper, as discussed in Section 3.
3 The Opt-Out Events
We now outline the two forms of opt-out events that have enabled Italian firms to abandon their CBA:
(i) a coordinated departure of large retailers from their employer association (Section 3.1) and (ii)
individual employers exploiting a regulatory loophole to adopt lower-wage "pirate agreements"
(Section 3.2).
3.1 The 2011 Secession of Mass Retailers
Background. The first opt-out event we study is the 2011 withdrawal of a group of large retailers,
Federdistribuzione (FD), from their employer association, Confcommercio (CC), to negotiate a

8
Consistent with this, prior studies find large pass-through of changes to CBA wage floors onto observed wages (Fanfani,
2023; Faia and Pezone, 2024).

8


---
separate CBA. The CC comprised 90 employer sub-associations (e.g., butchers, hotels, stationers).9
FD was the sub-association for mass retailers, including large hypermarkets (e.g., Carrefour), clothing
stores (e.g., Coin), furniture retailers (e.g., IKEA), and home improvement and gardening stores (e.g.,
Leroy Merlin).10 As of 2010, the FD group comprised 56 firms, accounting for approximately 6% of
retail employment (authors’ calculation based on the matched employer-employee data described
below).
On December 23, 2011, FD announced the exit of its members from CC to lobby independently and
negotiate a separate FD-CBA. The official reason for the departure was a disagreement between large
FD employers and small retailers, who dominated CC and opposed FD's push for liberalized opening
hours and expansion of large shopping malls.
Implications for Flexibility and Wage Setting. The opt-out had important consequences for wage
floors, resulting in divergent wage-setting patterns for all workers employed at FD firms versus CC
firms. Figure 1 plots the evolution of wage floors between 2005 and 2019 for those groups, for three
job titles: title "7," the lowest rank aside from apprentices, title "4," the modal one, and for midmanagers ("quadri," i.e., the highest job title).11
Before the 2011 opt-out, the wage trajectories of FD and CC were perfectly aligned, as FD was part
of CC and therefore subject to the same CBA wage floors. FD was also bound by the three-year
collective agreement that took effect in January 2011 and was expected to remain in force through
2013. As a result, the CBA provisions, including wage floors, would have applied to all workers hired
during that period, including those hired after the opt-out. However, because of delays in the

9

The CC-CBA was first signed in 1967 by the dominant associations Confcommercio (employer) and CGIL, CISL and
UIL (the three traditional unions). This contract was then renewed periodically and became the "representative" CBA in
the sector.
10
To aid exposition, we highlight company names most recognizable to international readers, primarily multinationals,
which, however, represent less than 25% of the FD firms.
11
The CBA lists wage floors for eight different job titles, which correspond to several occupations (listed in the text of
the CBA). Job title 7 comprehends shop assistants (garzoni) and cleaners (addetti alle pulizie). Job title 4 includes cashiers
(cassieri), clerks (commessi), and window dressers (vetrinisti), among others. The job title mid-manager (quadro)
includes store managers (gestori di negozio) and product managers, among others.

9


---
bargaining process between CC and the unions, wages did not diverge even in 2014. An agreement
on a new CC-CBA was finally found on March 30, 2015, covering the period from April 2015 to
March 2018. Hence, wage floors in FD firms remained at the 2013 levels and started to diverge from
the CC wage floors in 2015, with the gap amounting to around 4.8% in 2018, an effect that is
homogeneous across job titles. Our empirical analysis, detailed in Section 5.1, aims to understand the
impact on actual wages of workers hired by FD firms before 2011 of opting out of the CC-CBA by
FD employers.12
This period of divergence in wage floors and adversarial industrial relations lasted until January 2019.
FD and the three traditional unions signed a new CBA on December 19, 2018. While formally a
separate agreement, this contract replicated the wage floors of the prevailing CC-CBA (as well as
most other provisions); hence, the two lines in Figure 1 reconverge.13 Indeed, while FD and CC
continue to bargain separately, the individual CBAs that the two associations signed in 2022 (outside
of our sample period) remain closely aligned across all dimensions, including wage floors.
3.2 Adoptions of Pirate Agreements
Background. The second dimension of opting out is the growing adoption of so-called "pirate
agreements," where individual firms opt out of their original CBA, typically negotiated by the three
traditional unions, to agree on a new CBA with a smaller union.14 These pirate CBAs generally feature
lower wage floors and more flexible working conditions than traditional agreements.

12

As conflicts between FD firms' management and unions intensified, FD firms granted partial increases in the wage
floors. As these raises are not part of a sector-level CBA but are unilateral decisions, they do not necessarily guarantee
the same level of legal enforcement. Appendix A.1 provides additional details regarding these wage raises unilaterally
granted by FD firms despite not being bound by the CBA.
13
FD firms fell out of favor under the new “Conte I” government, which took office in June 2018 and proposed repealing
the liberalization of shopping hours. While FD firms had taken extensive advantage of this reform (as discussed in Section
6.1), several unions supported its reversal. Weakened by mounting political pressure and after years of adversarial labor
relations, FD firms ultimately made significant wage concessions, agreeing to extend to their workers the same conditions
negotiated by CC.
14
This term highlights the disruptive effects on the traditional system of industrial relations, as illustrated in the following
quote (from an Italian academic legal journal): "Although the pirates we are dealing with today are not equipped with
sabers or muskets, but, probably, with pens, smartphones, and tablets, the metaphor seems to hit the mark: the proliferation
of ‘pirates’ in the industrial relations system - or in inter-union system, [...] is a symptom of the insufficient organization
of this system and its (in)ability to repel ‘incursions’ and ‘hostile acts.’" (Centamore, 2018, authors' translation).

10


---
Pirate agreements exploit a loophole in Italian labor law. In principle, firms are required to adhere to
the wage floors established by the representative standard CBA for their sector. However, as noted in
Section 2, the law does not explicitly define what constitutes a "representative CBA" for a given firm
or sector. This legal ambiguity has allowed firms to circumvent traditional CBAs by abandoning the
main sectoral agreement and instead adopting a CBA signed by "pirate" unions, rather than the three
main unions.15 This loophole has been increasingly exploited, particularly after the Great Recession,
as firms faced mounting pressure to cut labor costs and increase flexibility.
Implications for Flexibility and Wage Setting. The wage-setting implications of pirate agreements
are complex, as they depend on three key factors: (i) the original wage floors faced by the firm, (ii)
the menu of available pirate agreements, and (iii) the employer’s ultimate choice from that menu. In
principle, when a firm adopts a pirate agreement, its workforce transitions from the old to the new
wage floors, potentially allowing for outright wage reductions rather than simply freezing wages and
avoiding scheduled increases, as in the FD opt-out event described in Section 3.1. Moreover, firms
could, in principle, adopt pirate CBAs only for a share of their workforce, while keeping other
employees on traditional CBAs, differently from the previous event where all workers employed at
FD firms were subject to the opt-out (Section 3.1).16
Figure 2 presents a case study of a pirate agreement, illustrating its impact on wage floors across job
titles for workers covered by this collective contract. The example comes from the wholesale and
retail sector, where the dominant contract was the CC-CBA (as discussed above), and where both the
traditional and pirate agreements covered comparable occupational groups. Appendix A.2 presents
additional details regarding this specific opt-out event. Except for the highest wage group, the pirate

15

These unions are either minor, existing organizations competing with the three main unions or newly established unions
formed after 2010. In practice, firms allow their existing CBAs to expire without renewal and then sign new agreements
with these so-called pirate unions. In some cases, typically ruled unlawful by labor courts, firms replace valid CBAs
before expiration. Firms that are not original signatories to a CBA but have merely applied the traditional CBA for their
sector can adopt a new agreement immediately.
16
See also the previous footnote. As of 2019, among firms applying a pirate CBA to at least one worker, the share of
firms using a pirate CBA for their entire workforce ranged from 82% among small firms (2–9 employees) to 20% among
large firms (250 employees or more).

11


---
agreement established lower wage floors, particularly at the lower end of the wage distribution.
Additionally, the agreement introduced regional pay differentiation, reflecting the argument by Boeri
et al. (2021) that nominal wages should better align with regional productivity levels. To illustrate
this, the figure presents two wage floors for each title (diamonds and circles), representing the region
with the highest and lowest wage levels (Lombardia in the North and Molise in the South). Beyond
wages, the pirate agreement also provided less generous non-wage benefits, such as reduced maternity
leave provisions, further differentiating it from the CC-CBA.
Drawing on the data presented in Section 4 below, we provide descriptive statistics on the prevalence
and evolution of pirate agreements, as well as the characteristics of affected workers and firms. Figure
3 illustrates the expansion of pirate agreements following the Great Recession. Panel (a) shows the
annual number of pirate agreements signed, while Panel (b) presents the share of firms and workers
covered by pirate agreements. Despite pirate contracts constituting the majority (roughly two thirds)
of CBAs in Italy, their coverage remains limited. As of 2019, pirate agreements applied to only 3%
of private-sector workers and firms, affecting approximately half a million workers and 40,000 firms.
The disparity between the number of contracts and their coverage reflects that pirate agreements are
often tailored contracts, typically negotiated by small unions and covering narrower sets of firms. In
contrast, standard CBAs apply broadly across industries, meaning that a small number of agreements
cover a very large number of workers.
Appendix A2 provides additional descriptive evidence on pirate contracts, which we briefly
summarize here. We find substantial geographic heterogeneity in their use (Appendix Figure A2),
with pirate agreements more common in the South, a pattern consistent with Boeri et al. (2021), who
argue that wage floors are especially binding in less productive regions. Compared to workers covered
by standard CBAs, those under pirate agreements are more likely to be women, employed part-time,
and earn lower average wages. Pirate CBAs are disproportionately concentrated in the services sector
and underrepresented in manufacturing, suggesting that firms in lower-skill industries such as retail

12


---
are more likely to adopt them. Firms using pirate CBAs also tend to be larger and younger, and they
employ a higher share of women and part-time workers relative to firms adhering to traditional CBAs.
4 Data
We now describe the linked datasets that form the basis of our analysis: matched employer-employee
data (including firms’ financial balance sheets), and data on collective bargaining agreements. We
then detail how we identify the opt-out events discussed in the previous section within these datasets.
Matched Employer-Employee Data. We use comprehensive data on all worker-firm matches in the
non-agricultural private sector from 2005 to 2019, covering earnings, weeks worked, contract type
(part-time versus full-time, temporary versus permanent), occupation (apprenticeship, blue-collar,
white-collar, mid-management, manager), reasons for job separations (e.g., firing, resignation) and
demographic information such as date of birth and gender.17 These data ("INPS data") are collected
by the Italian Social Security Institute (INPS) and accessed through the VisitINPS program. We
merge accounting variables for all non-financial incorporated firms from 2005 to 2018 into our data
(which we use for matching in the firm-level design). Collected by the Cerved Group, these data can
be combined with the INPS data using a unique national tax firm identifier (codice fiscale).
Crucially, unlike in most other contexts, the dataset includes, for each job spell, the specific CBA
applied by the firm, identified by a unique code that we describe next. The requirement that firms
report the applicable CBA stems directly from Italy's coverage rules, as the CBA is used to compute
social security contributions.
CBA Contract Data. All CBAs are recorded in the web archive of CNEL (National Council for
Labor and Economic Policies), along with details about their signatory parties.18 We combine the

17
We exclude all workers employed as managers because managers are subject to a different collective agreement
legislation. We also exclude apprentices and employees of international organizations.
18
The archive can be accessed at this link: https://www.cnel.it/Archivio-Contratti.

13


---
CNEL contract data with the INPS administrative data using the INPS-CNEL crosswalk provided by
CNEL (also used in Daruich, Di Addario and Saggio, 2023; Faia and Pezone, 2024).
We obtained from FD the names of the firms that opted out of the CC-CBA in 2011. Using these
names, we manually match them with the firm-level balance sheet data to retrieve their national tax
identifiers. Out of the 56 firms in FD that opted out of the CC-CBA, we matched 52 firms to the INPS
data (see Appendix A.1 for the list of firms).
As for pirate agreements, we follow Lucifora and Vigani (2021) and classify those CBAs in the INPS
database labeled "Different Contract" as pirate agreements. Examining the CNEL records, we
confirm that nearly all these CBAs are signed by non-traditional unions.19 Additionally, we define as
pirate agreements any CBAs with a unique identifier in the INPS data—i.e., that are not recorded as
"Different Contract"—but were not signed by at least one of Italy’s three main unions, as recorded in
the CNEL archive.20
Main Outcome Variables. Our analysis focuses on four key worker-level outcomes: i) (log) weekly
wage, calculated as the worker’s annual wage net of social security contributions at their (dominant)
employer, divided by the number of weeks worked at that employer in the year,21 ii) employment,
defined as a binary indicator equal to one if a worker has at least one day of employment at any firm
in a year and zero otherwise, iii) employment at the original (opting-out) firm, a binary indicator equal
to one if a worker is employed at their original firm and zero otherwise, and iv) annual earnings,
computed as the total labor earnings a worker receives from all employers in a given year, with a
value of zero for non-employed workers.

19

The CNEL data indicate that only a small number of "Different Contracts" have been signed by the three main unions
(approximately 30), representing a tiny fraction of total contracts. These instances cannot be identified in the INPS data,
which prevents us from excluding them.
20
We exclude sectors or occupations where traditional unions have historically not signed national CBAs because
bargaining has always been handled by specialized minor unions. For example, as noted in Footnote 17, managers in Italy
have their own CBAs, which are never signed by the three traditional unions since they do not represent managers.
21
This outcome is not available for non-employed workers. If a worker holds multiple jobs in a year, we define their
dominant employer as the one where they have worked the highest number of weeks during that year.

14


---
5 Econometric Framework
This section presents the harmonized matched difference-in-differences (DiD) research design used
to analyze the effects of the FD opt-out event (Section 5.1) and the adoption of pirate agreements
(Section 5.2) on workers. We then discuss the identification assumptions and the firm-level analog in
Section 5.3.
5.1 The 2011 Secession of Mass Retailers
Specification. We compare a worker employed in an FD firm in 2010, the year before the opt-out
event of FD employers occurred, with a similar worker employed by a firm that applied the CC-CBA
in 2010 and that has not opted out of this CBA (henceforth, a CC firm). We thus fit regression
equations of the following type:
!!" = #! + d" + % b" ∙ '(! + u!" ,

(1)

"#$%&%

where !!" represents an outcome of individual . in year / (e.g., total earnings), #! and d" are worker
and year fixed effects, and '(! is an indicator of whether an FD firm was worker .'s dominant
employer in 2010 (i.e., having employed . for the most weeks that year). The b" are DiD regression
coefficients normalized relative to 2010. We cluster standard errors at the level of the 2010 employer.
Sample and Matching. The analysis sample consists of workers employed by either an FD firm or
a CC firm in 2010, who are similar in various observables up to the opt-out event. To construct this
sample, we fit a propensity score for the probability of being employed by an FD firm in 2010 (similar
to Goldschmidt and Schmieder, 2017; Jäger and Heining, 2022). We restrict the sample to workers
with at least four years of labor market experience and three years of tenure with their 2010 dominant
employer, following the job displacement literature (e.g., Bertheau, Acabbi, Barceló, Gulyas,
Lombardi and Saggio, 2023; Schmieder, Von Wachter and Heining, 2023). We also restrict the

15


---
analysis to firms with at least 15 employees in 2010.22 The propensity score includes region-fixed
effects and covariates such as age, tenure, gender, contract type (temporary versus permanent, fullversus part-time), broad occupation dummies, and the log weekly wage in 2010, 2009, and 2008.
Each FD worker is matched to a single control worker by selecting the CC-CBA worker with the
closest propensity score without replacement.
Table 1 presents summary statistics for the full and the matched samples. Columns (1) and (2) show
the average characteristics of workers in the analysis sample, respectively for 2010 FD and CC
employees, before matching. FD firms are substantially larger than CC firms, reflecting the context
of the opt-out decision: FD firms are large retailers aiming to bypass the CBA designed for small and
medium-sized enterprises.23 FD firms are also more likely to use part-time contracts, which may help
explain the higher fraction of women among FD employees. However, in some respects, such as
wages, FD and CC firms appear quite similar even before matching. Columns (3) and (4) of Table 1
present the characteristics of the matched sample, where matched workers represent about 90% of
the original FD-firm worker sample and closely resemble the broader population of FD employees—
as expected given the strict matching strategy described above.
5.2 Adoptions of Pirate Agreements
To estimate the impact of adopting pirate agreements, we also employ a matched DiD research design.
We tightly harmonize this design with the FD analog above, with two modifications. First, since the
adoption of a pirate agreement occurs in different years across different worker-firm matches, we use
a staggered DiD specification.24 Second, since firm size is more balanced between firms using pirate

22

This restriction is imposed to reduce the imbalances in firm size that exist between FD and CC firms (see Table 1). We
set the cutoff at 15, as it is a key size threshold in the Italian labor law as it affects dismissal protection (Kugler and Pica,
2008).
23
Firm size is not included in the propensity score for the FD design, as its inclusion would result in significant violations
of the overlap assumption.
24
Specifically, the adoption of a pirate agreement event occurs in month ! of a given year if a worker is employed with
a standard CBA in months ! − 2 and ! − 1 of the same spell but is then moved to a pirate CBA in month ! and is still
covered by that pirate CBA in month ! + 1. We also drop the (rare) spells in which at least two transitions of the same
nature (e.g., standard-to-pirate) occur within 12 months or those where the worker returns to be hired under their regular
CBA within the same calendar year.

16


---
CBAs and other firms, we can now include firm size in the matching procedure, which differs from
the analysis of the FD opt-out, as this does not lead to violations of the overlap assumption.
Specification. The specification we use to analyze the effects of adopting a pirate CBA is a staggered
DiD design that takes the following form:
(

(

!!" = #! + d" + % g' ∙ 0[/ = /!∗ + 2] + % b' ∙ 0[/ = /!∗ + 2 ] ∙ 4! + u!" ,
')*(
')*(

(2)

where 4! is an indicator for a worker . experiencing a within-employer transition to a pirate CBA, and
/!∗ ∈ [2008, 2009, …, 2016] denotes the year of the event. For a control worker, this is the year the
matched treated worker was switched to the pirate agreement. For the few treated workers who
experienced a within-employer pirate CBA transition more than once over the sample period, we refer
to their first transition. We normalize the coefficient b*& to zero. Standard errors are clustered at the
level of the /!∗ − 1 employer.
Sample and Matching. To construct a comparable control group, we implement a matching
algorithm analogous to that used in the FD design. The pool of potential control workers is
represented by workers who have the same (standard) CBA as treated workers before transitioning to
a pirate CBA (period /!∗ − 1) and were never employed at a firm that used a pirate CBA prior to 2019.
We restrict the sample to workers with at least four years of labor market experience and three years
of tenure with their dominant employer at /!∗ . We then estimate the same propensity score model used
in the FD analysis, but with two modifications to the matching algorithm: we include firm size and
sector dummies.25 The inclusion of firm size is explained above, while the addition of sector dummies
is inconsequential, as all FD and CC control firms operate within the same sector (retail) by design.

25

Our set of transitions excludes those that took place in the automotive sector in 2012 as they capture the opt-out of Fiat,
which we cannot study due to VisitINPS privacy restrictions on single firms. Additionally, we exclude those transitions
to a CBA flagged as "Different Contract" in the retail sector in 2015, as this designation was also applied to jobs that
continued under the old "frozen" CC contract following the renewal of the CC-CBA.

17


---
Unlike the FD analysis, we can and do now include firms with fewer than 15 employees to account
for the greater variation in firm size among treated firms.
Similar to Table 1 for the FD design, Table 2 compares the baseline characteristics of treated and
control workers, both before and after matching. Columns (1) and (2) present descriptive statistics
for 2008–2016, before matching. Column (1) reports characteristics of treated workers as of period
/!∗ − 1, while Column (2) shows the same for other workers covered by a standard CBA, who do not
undergo treatment. Treated workers are more likely to be women, work part-time, hold white-collar
positions, be located in the South, and earn lower wages compared to other workers. On average, they
are also employed in larger firms. Columns (3) and (4) report characteristics for the matched sample
used to estimate Equation (2). Out of approximately 38,000 within-spell pirate agreement opt-outs
between 2008 and 2016, we successfully matched around 25,000 cases. As expected, matched treated
and control workers are similar across all observed dimensions, including average firm size.26
5.3 Discussion
Our research designs focus on incumbent workers already employed when their firm decides to opt
out. In the FD event, incumbent workers are employees of FD firms in 2010. In the case of the pirate
CBA opt-out, they are workers whose employer transferred them from a traditional CBA to a pirate
CBA in the event year. This approach aligns with a broader literature that examines the impact of
firm-level events, such as mass layoffs (Jacobson, LaLonde and Sullivan, 1993) or outsourcing events
(Goldschmidt and Schmieder, 2017), on workers. Next, we outline the assumptions required for a
causal interpretation of our results and discuss the strengths and limitations of this approach.
Identification. A causal interpretation of the DiD coefficients 8b" 9 and 8b' 9 in Equations (1) and (2)
relies on a parallel trend assumption. In the context of the FD event, this assumption implies that, in
the counterfactual scenario where FD firms had remained under the CC-CBA, the differences in

26
We match 2,497 treated workers in 2008, 879 in 2009, 1,567 in 2010, 2,115 in 2011, 4,638 in 2012, 4,882 in 2013,
2,603 in 2014, 3,454 in 2015 and 2,317 in 2016.

18


---
outcomes between workers employed by FD firms in 2010 and those under a CC-CBA would have
remained constant. A similar assumption is required to evaluate the effects of adopting pirate CBAs.
To assess the plausibility of this assumption, we will examine the evolution of outcomes in the years
preceding the opt-out decision, with particular attention to periods not directly accounted for in the
propensity score. While these tests are reassuring and while we present two worker-level and one
firm-level design with similar results, we acknowledge that they do not definitely warrant a fully
causal interpretation of the evidence. Yet, we believe these results are important in light of the scarcity
of evidence on the effects of opt-outs.
Workers vs. Firm Perspective. Our empirical analysis examines how an employer's decision to opt
out of its CBA affects the career trajectories of its employees. A key advantage of focusing on workers
is that we can track their outcomes even if they eventually leave their employer. However, restricting
the analysis to incumbent workers may provide only a partial perspective, particularly if opting out
significantly impacts the hiring margin of opting-out firms. To address this, we also present firmlevel effects of adopting pirate agreements, based on a matched DiD research design that mimics
Equation (2) but is conducted at the firm level (see Section 6.3 below and Appendix C).27 This design
requires stronger assumptions for validity as it examines how an endogenous firm decision impacts
firm-level outcomes. Nevertheless, this analysis is valuable for providing a more comprehensive
picture of the overall effects of opting out—on which even basic descriptive micro evidence is scant—
and its broader implications.
6 Results
We next present the results, focusing on the effects of the opt-out events on the wages, employment,
job separation, and earnings of incumbent workers, i.e., workers who experience a change in their
CBA as a result of their employer opting-out from their “status-quo” CBA. Section 6.1 analyzes the

27
The small number of treated firms present in the FD mass-retailers opt-out makes firm-level analysis for such event
underpowered and we thus only focus on pirate agreements for this analysis.

19


---
FD withdrawal event, while Section 6.2 examines the adoption of pirate agreements. Section 6.3
presents results for the firm-level analysis.
6.1 The 2011 Secession of Mass Retailers
Figure 4 reports the DiD effects (b" ) of the FD opt-out on the cohort of workers employed at the FD
firms in 2010 relative to the (matched) cohort of workers employed instead at CC firms in 2010.
Table 3 reports full regression results for three points in time, corresponding to the stages of FD optout, see discussion in Section 3.1: 2011 (immediate impact), 2013 (medium run effect), and 2016
(longer run effect).
Wages. We begin by analyzing the effect of the opt-out event on wages, the primary channel through
which opt-outs influence labor market outcomes. We do so separately for the full matched sample
described in Section 5.1 ("overall") and for the subsample of treated and control workers that remain
at their 2010 employer ("stayer"). Panel (a) of Figure 4 (and Table 3, Column (1)) presents these
effects. We first analyze the evolution of (log) wages for the full matched sample, without imposing
a condition that the treated worker remains employed with an FD employer (blue hollow circles,
"overall"). Before the 2011 opt-out, Panel (a) of Figure 4 shows no evidence of a differential wage
evolution between FD firms and CC firms. This indicates parallel pre-event trends, supporting our
identification strategy. In the first post-period time window, wages decrease slightly right after the
2011 opt-out event. Estimates in this time window are mostly insignificant and very moderate (e.g.,
around 1%, SE 0.0058 in 2011).
After 2015, following the adoption of the new CC-CBA by the control firms, which introduced higher
wage floors, wages decline strongly for FD workers compared to their CC peers. The wage effect
peaks at around -4% (SE 0.0095) in 2018, which is only slightly lower in magnitude than the
maximum divergence in CBA wage floors between FD and CC firms (4.8%) documented in Figure
1. This suggests that the relative wage reductions for FD workers are primarily driven by the higher
wage floors introduced in the CC-CBA.
20


---
Figure 4, Panel (a), further confirms this result by showing that the bulk of the wage decrease is found
among stayers (in full red triangles), i.e., individuals that remain with their 2010 employer and are
thus mechanically exposed to the differences in wage floors following the opting-out decision of FD
employers.28 Hence, the wage effects reflect wage policy shifts induced by the opting-out event rather
than compositional changes.
We find some evidence that FD workers recover part of their wage losses in the last year of our
sample, 2019, which is the year in which FD firms effectively re-adopted the CC-CBA (see the
discussion in Section 3.1). However, these wage gains are pretty small: even after the realignment in
wage floors, workers subject to the FD opt-out still experience wage losses of about 3-4% overall and
4-5% for stayers.
To summarize, firms that opt out of centralized collective bargaining benefit from increased
downward wage flexibility. As a result, incumbent workers exposed to the opt-out experience
significant relative wage losses, which they are unable to offset, either by re-negotiating wage premia
or by switching employers, even in the year when the FD and CC CBAs were realigned, as discussed
in Section 3.1.29
Employment. Figure 4, Panel (b) (and Table 3, Column (2)) presents the results for employment,
defined as the probability that a worker employed in a treated or control firm in 2010 remains
employed in a given year (i.e., has positive labor earnings). Pre-trends are flat, including in the early
years (2005-2006), where no employment restrictions are imposed on the analysis sample.

28

For the analysis of stayers, we estimate Equation (1) restricting the sample to pairs of matched treated and control
workers who are both, for each year after 2010, still employed by their 2010 employer in that given year. These pairs are
assumed to represent "always-takers"—that is, individuals who would have remained with the same employer regardless
of whether their firm opted out. Under this assumption, we can identify the effect of the opting-out event on wages, net
of selection on the retention margin, along the lines discussed in Lee (2009).
29
One concern is that our results may be influenced by the nationwide deregulation of shop hours under Decree 201/2011
(“Salva Italia”) (Rizzica, et al. 2023), which may have affected FD firms. Appendix Figure B1 addresses this by exploiting
municipal variation in exposure: municipalities already liberalized before 2011 show wage patterns similar to those in
exposed areas.

21


---
We estimate a positive employment effect of approximately 3 percentage points, which emerged
during the "interim period" (2011–2014), following the opt-out but before the new CC-CBA was
signed. After 2015, the positive impact persists and stabilizes at approximately 4 percentage points.
This positive employment effect appears to be driven by retention, as evidenced by a significant
increase in the likelihood of remaining with the 2010 employer (Figure 4, Panel (c), and Table 3,
Column (3)). Post-opt-out, FD employees are about 19 percentage points (SE 0.0439) more likely to
stay with their FD employer, despite no significant pre-opt-out differences, even before 2008, when
no tenure restrictions are imposed. The fact that we observe positive employment effects even before
the divergence in wage floors begins (see Figure 1) is noteworthy and suggests the presence of
anticipation effects as dismissal decisions are forward looking and incorporate present value
considerations with long-term employment relationships. Specifically, firms’ retention decisions
appear to reflect expectations that incumbent workers’ wages could be restrained after 2015.
Consistent with this interpretation, Section 7 will show that increased retention is primarily driven by
a decline in involuntary separations, indicating that employers began dismissing fewer workers in
anticipation of future wage-setting flexibility.
This evidence suggests that employment and wages adjust along the firm's labor demand curve. By
opting out, FD firms can offer lower wages than CC firms. As a result, FD firms experience a relative
increase in labor demand, improving employment prospects for incumbent FD workers.
Earnings. So far, the evidence suggests that allowing firms to deviate downward from wage floors
lowers the wages of incumbent workers but increases their retention and, ultimately, their
employment prospects. We next examine how the opt-out event impacts incumbent workers' overall
earnings on net, shown in Figure 4, Panel (d) (and Table 3, Column (4)). Earnings show no clear
positive or negative effect post-opt-out, with estimates remaining largely insignificant. This suggests
that the gains in employment and losses in wages largely offset each other, resulting in average
earnings remaining unchanged.

22


---
6.2 Adoptions of Pirate Agreements
We now examine the effects of pirate agreement adoption, leveraging a much larger sample of firmlevel opt-out events. Figure 5 presents the estimated effects from Equation (2), and Table 4 reports
the corresponding regression results.
Wages. Estimates in Figure 5, Panel (a), and Table 4, Column (1), show results for wages, again
separately for the full matched sample described in Section 5.2 (“overall”, blue hollow circles) and
for the subset of treated and control workers in the matched sample that stay employed at the /!∗ − 1
firm (“stayer”, red full triangles). We find that workers experience a sharp decline in log weekly
wages following their employer’s transition to a pirate agreement, relative to matched control
workers. The wage loss is approximately 2% (SE 0.0041) and emerges almost immediately after the
opt-out, stabilizing around 2.5% in subsequent years.30 Among stayers, the wage reduction is of
similar magnitude, suggesting that the decline is driven primarily by changes in wage-setting policy
rather than by compositional shifts in the workforce of adopting firms.
Employment. Similar to the FD opt-out event, we find a positive employment effect, reaching
approximately two percentage points two years after the event and increasing to three percentage
points (see Figure 5, Panel (b) and Table 4, Column (2)). This effect appears in part to be driven by
a higher, though not precisely estimated, probability of staying at the opting-out firm (Panel (c) and
Column (3)).31
Earnings. As in the FD opt-out event, earnings seem largely unaffected by the adoption of pirate
CBAs, consistent with the positive employment effect offsetting the negative effect on wages. These

30

Estimating the actual pass-through from wage floors to realized wages is more complex for the pirate CBA design, as
we cannot observe wage floors for most pirate agreements and, as a result, we cannot properly quantify the drop in
negotiated wage floors.
31
The observed employment effect is not driven by different survival probabilities of the initial employer of treated and
control workers following the adoption of the pirate CBA, as shown in Appendix B, specifically Appendix Figure B2.
We directly investigate the effects of pirate CBAs' adoptions on firm survival in the firm-level design in Section 6.3.

23


---
results are shown in Panel (d) of Figure 5 (and Table 4, Column (4)). However, confidence intervals
remain wide for this outcome.
Interim Summary. The adoption of pirate agreements leads to similar worker outcomes as the FD
opt-out event: lower wages, higher employment probability, and statistically insignificant net effects
on earnings, centered around zero. Both FD and pirate opt-outs point to the same economic
mechanism: firms reduce wages when given the opportunity, and these wage cuts are accompanied
by positive, rather than negative, employment effects.
6.3 Firm-Level Design
We complement the worker-level evidence with a firm-level analysis, with results presented in Figure
6. This design is a natural counterpart to the worker-level analysis; detailed methodology, a regression
table, and summary statistics are provided in Appendix C. We concentrate exclusively on the pirate
agreement setting, due to the small number of FD firms and substantial baseline differences with CC
firms. A key advantage of the firm-level design is that it allows us to assess the impact of opt-out
events on all the firm employees over time, rather than focusing solely on incumbent treated workers.
We however reiterate the associated identification challenges discussed in Section 5.3.
Appendix Figure C1 reports effects on the share of employees covered by a pirate CBA before and
after the firm adopts such an agreement for at least one worker (our event definition). Coverage jumps
to 60% in the event year and declines only moderately thereafter. This indicates that adopting a pirate
CBA is a systematic shift impacting the majority of the firm's workforce.
Figure 6 shows effects on firm-level outcomes. Panel (a) shows that mean weekly wages paid by the
firm quickly persistently decline by approximately 3%. Panel (b) shows that this reduction is
accompanied by an about 3 percentage point higher survival probability for treated firms in the optout year (versus a baseline survival probability of 85% for control firms in the post-opt-out years);
this effect remains positive for two years before converging to zero.

24


---
Panels (c) and (d) report results on log employment. In the baseline specification shown in Panel (c),
we find a positive effect. But treated firms also exhibit faster employment growth before the event.
This pattern contradicts the notion of “Ashenfelter’s dip,” the idea that negative shocks systematically
trigger opt-out decisions. Correcting for pretrends in Panel (d), we find that the growth effect quickly
fades after an initial jump, and by year 5, even turns somewhat negative.32 Overall, we conclude that
these findings do not permit clear-cut conclusions regarding the long-run effects on firm size.
In Panels (e) and (f), we analyze the impact on the hiring margin alone. Panel (e) shows effects on
the employment share of new hires at the firm. This share spikes in the event year but quickly fades
out. Panel (f) shows effects on the average wage paid to new hires, which drops significantly after
the adoption of the pirate agreement, with an effect that is larger in absolute value (about -10%)
compared to what we found for incumbent employees (about -3%). This suggests that adopting the
pirate CBA enables firms to circumvent existing wage rigidities among incumbent workers.
7 Does Opting Out Lead to Higher Employment in the South of Italy?
The inability of Italian firms to deviate from national CBAs has been identified as a potential
contributor to persistently high unemployment in Southern Italy (Boeri et al., 2021). Firms in the
South typically have lower productivity than their Northern counterparts. Yet, national CBA wage
floors prevent them from adjusting wages to reflect their economic conditions, potentially leading to
higher unemployment. The opting-out events analyzed in this paper provide a unique opportunity to
empirically evaluate the impact of allowing firms to deviate from national CBAs on employment
levels in Southern Italy. As mentioned in Section 3.2, Appendix Figure A2 presents a heat map of
Italy and shows that pirate agreements are more common in the South.

32
We apply the detrending procedure proposed by Dustmann et al. (2022), which involves estimating and extrapolating
a linear time trend based on the pre-event period.

25


---
7.1 Wages, Retention and Employment
Figure 7 replicates our incumbent worker design (Sections 6.1 and 6.2), displaying the results for
wages, retention, employment, and earnings separately for the Center-North and South of Italy, across
the two opting-out events: the withdrawal of mass retailers (Panels (a) and (b)) and the adoption of
pirate agreements (Panels (c) and (d)).33 A consistent pattern emerges across both events: the positive
employment effects are concentrated among incumbent workers employed by firms in the CenterNorth. In contrast, the overall employment probability for Southern workers shows no significant
increase. As in the baseline estimates, employment effects are primarily driven by the probability of
remaining employed with the original employer. Workers in the North are significantly more likely
to remain with their employer after the opt-out event. In contrast, in the South, retention effects are
statistically insignificant for the FD event and even negative for pirate agreements. Thus, the evidence
in Figure 7 suggests that Southern workers do not see improved employment probabilities following
their employer's opt-out.
The negative effects of pirate CBAs on log wages are larger in magnitude in the South than in the
North (–5.13% vs. –1.57% five years post-event). A similar pattern holds for the FD opt-out, with
2018 wage effects of -6.06% in the South and -3.73% in the North. As shown in Figure 7, Southern
workers experience overall earnings losses in both cases, as wage reductions are not offset by
improved employment prospects. Specifically, five years after the pirate CBA event, earnings in the
South decrease by €607 (approximately 4% of the mean) and by €2,679 (around 12%) following the
FD event in 2018. In contrast, for pirate CBAs in the North, the employment gains eventually
outweigh the wage losses, leading to a modest increase in earnings.

33

Specifically, we re-estimate Equations (1) and (2) based on the job's location in the year preceding the event,
distinguishing between Center-North and the South. Southern Italy includes the two NUTS 1 macro-regions of the South
and the Islands (i.e., the following regions: Abruzzo, Molise, Campania, Apulia, Basilicata, Calabria, Sicily, and
Sardinia). The Center-North includes the three NUTS 1 regions of the Northwest, Northeast, and Center of Italy
(Piedmont, Aosta Valley, Liguria, Lombardy, Trentino-Alto Adige, Veneto, Friuli-Venezia Giulia, Emilia-Romagna,
Tuscany, Umbria, Marche, and Lazio).

26


---
7.2 Evidence on Voluntary and Involuntary Separations
To understand these regional differences, we leverage information on job separation reasons. This
allows us to distinguish between involuntary separations (initiated by the employer due to financial
difficulties, outsourcing/mergers, temporary contract expiration, or firings for just cause), and
voluntary separations (worker resignations).34
Figure 8 shows the probability of voluntary and involuntary separations for workers in the North and
South, for the pirate agreements and the FD event. For pirate agreements, the decline in retention
among Southern workers (Figure 7, Panel (d)) is mainly driven by a rise in voluntary resignations
(Figure 8, Panel (b)). Involuntary separations increase slightly but not significantly, suggesting that
adopting a pirate agreement does not decrease the risk of involuntary job loss in the South.
This stands in stark contrast to the North. For Northern workers whose CBA was converted to a pirate
agreement (Figure 8, Panel (a)), the probability of involuntary separation declines significantly, while
resignation rates remain stable. Thus, pirate CBAs appear to improve employment prospects in the
North by reducing employer-initiated separations. In the South, by contrast, pirate CBAs do not
significantly reduce involuntary separations and lead to more voluntary resignations, likely in
response to larger wage cuts. These regional differences may help explain why employment rises in
the North but not in the South over the medium to long term.
For the FD event (Panels (c) and (d)), we observe a similar pattern in involuntary separations:
Southern workers whose employers opt out of the CC-CBA do not see a reduction in involuntary
separation probabilities, while Northern workers do. This helps explain the regional differences in
employment trajectories shown in Figure 7, Panels (a) and (b). Unlike pirate agreements, however,

34

Separations due to other reasons (e.g., retirements) are coded as "Other Reasons" and are not included in our definition
of either voluntary or involuntary separations. The reason for separation is reported by the employer and is used for
determining pension contributions and severance payments. This information is available for approximately 75% of all
separations in our data. Missing values are most common in cases where the employer shuts down or when the separation
occurs on the last day of December. See Di Addario et al. (2023) and Daruich et al. (2024) for recent studies that have
made use of this information.

27


---
the FD opt-out also affects resignation behavior. Specifically, workers in both regions are less likely
to resign, and more so in the South. These patterns may reflect improvements in job amenities, such
as greater flexibility in working hours, which were a key motivation for FD employers’ secession, as
noted in Section 3. As discussed in Section 6.1, the liberalization of shop opening hours likely
enhanced flexibility in weekly scheduling, a feature especially valued by part-time workers.
In summary, opting out of national CBAs increases employment probabilities only for workers in the
North. Northern firms appear to use the added wage flexibility to preserve jobs by reducing
involuntary separations. In contrast, opting out does not significantly boost employment among
Southern workers. Appendix Figure C2 supports this, showing no clear increase in overall
employment at Southern firms, even when accounting for hiring. However, these results should be
interpreted with the caveats noted in Section 5.3, as well as considered jointly with the more negative
wage effects in the South. The reduction in labor costs due the opting-out event can also lead to higher
survival rates for both firms in the North and the South, as we show in Figure C2, Panel (b).
7.3 Interpreting the Evidence
A monopsony framework with heterogeneous productivity levels and labor supply elasticities across
firms provides a potential explanation for our overall findings and in particular the geographic
heterogeneity. The opting-out event enables firms to transition from a nationally determined wage
equilibrium to one where wages are set more freely, reflecting each firm's productivity and the labor
supply it faces.
Figure 9 illustrates this mechanism by comparing two firms that initially paid the same nationally
mandated wage floors, but differ, first, in productivity, as captured by the different marginal revenue
product of labor (MRPL curves) and, second, in labor market competition as captured by the different
curvatures of the firm-specific (inverse) labor supply curves, w(L). The Northern firm (in blue) is
highly productive and operates in a fairly competitive labor market, which gives rise to a relatively
elastic firm-specific labor supply curve. As a result, after opting out, this firm sets wages below the
28


---
CBA floor (the intersection of the MRPL curve with the marginal cost curve of labor, MFC(L)),
which allows the firm to expand employment. The employment-level response observed in the North
is thus consistent with what one would expect to find when removing a minimum wage or wage floor
in a competitive labor market: employment will rise as firms are now able to pay lower wages.
Now focus on the Southern firm (in red). This firm has lower productivity and is also positioned in a
less competitive labor market. The latter gives rise to a more inelastic labor supply curve, consistent
with recent evidence on the geographical distribution of labor market power in Italy documented by
Mottironi (2024). As a result, following the opt-out event, the Southern firm reduces wages even
further but also has lower employment compared to the CBA-determined equilibrium. This occurs
because the opt-out event lets the Southern firm exert its monopsony power. This firm can mark down
wages considerably and finds it optimal to have a lower level of employment than with the CBA wage
floor. Thus, opting out lowers wages for both firms, with a larger negative effect for the Southern
firm; however, it results in divergent employment outcomes: employment rises in the North, but
declines or remains unchanged in the South.
These patterns in a standard monopsony model applied to a CBA context align with our empirical
findings, and echo results in the minimum wage literature (Card and Krueger, 2016; Azar et al., 2023),
here suggesting that CBA wage floors, too, can mitigate inefficiencies in imperfect labor markets
(Acemoglu, 2001; Dustmann et al., 2022).
8 Conclusions
This study has aimed to provide micro-empirical evidence on the benefits and costs of wage-setting
decentralization for firms and workers, addressing whether increased flexibility undermines workers’
earnings or delivers broader gains by boosting employment and reducing firm closures. Overall, our
findings lend support to both perspectives. Both episodes of wage-setting flexibilization in the Italian
labor market led to wage reductions. At the same time, employment stability improves, as workers
are more likely to remain with their original employer.
29


---
These effects are particularly pronounced in Italy’s North, where firms are more productive. There,
the overall impact of decentralization, measured by changes in worker earnings, is null or even
positive. By contrast, in the South, employment gains do not compensate for wage losses, which are
larger than in the North, resulting in slightly negative earnings effects. While employment gains in
the North are mainly due to a reduction in involuntary separations, this is not the case in the South.
Nonetheless, in both regions, increased flexibility is associated with a higher likelihood of firm
survival.
Our results can be rationalized within a standard monopsony framework, in which CBA wage floors
constrain firms’ wage setting power. The differences between the South and the North in particular
would imply that Northern firms have higher productivity and face more competitive labor markets
than those in the South.
We conclude by acknowledging the limitations of our study and outlining directions for future
research. Our main research design focuses on the effects of opting out on workers directly impacted
by this institutional change, specifically, those whose CBAs transition from a nationally
representative agreement to a more flexible collective contract, such as a pirate agreement. This
approach allows us to examine retention probabilities and track employment outcomes even after
workers leave the opting-out employer. However, our complementary firm-level designs suggest that
the effects on hiring dynamics and broader effects on firm size are rather limited. Further research,
using research designs better suited to firm-level impacts as well as aggregate market-level impacts,
will provide a more comprehensive picture.

30


---
References
Acemoglu, Daron, “Good Jobs versus Bad Jobs,” Journal of Labor Economics, 2001, 19 (1), 1–21.
Azar, José, Emiliano Huet-Vaughn, Ioana Marinescu, Bledi Taska, and Till von Wachter,
“Minimum Wage Employment Eﬀects and Labour Market Concentration,” The Review of Economic
Studies, 2023, 91(4), 1843––1883.
Bertheau, Antoine, Edoardo Maria Acabbi, Cristina Barceló, Andreas Gulyas, Stefano
Lombardi, and Raﬀaele Saggio, “The Unequal Consequences of Job Loss Across Countries,”
American Economic Review: Insights, 2023, 5 (3), 393–408.
Bhuller, Manudeep, Karl Ove Moene, Magne Mogstad, and Ola Vestad, “Facts and fantasies
about wage setting and collective bargaining,” Journal of Economic Perspectives, 2022, 36 (4), 29–
52.
Boeri, Tito, “Two-Tier Bargaining,” IZA Discussion Paper 8358, Institute of Labor Economics (IZA)
2014.
- and Pietro Garibaldi, “A Tale of Comprehensive Labor Market Reforms: Evidence from the
Italian Jobs Act,” Labour Economics, 2019, 59(C), 33–48.
- , Andrea Ichino, Enrico Moretti, and Johanna Posch, “Wage Equalization and Regional
Misallocation: Evidence from Italian and German Provinces,” Journal of the European Economic
Association, 2021,19 (6), 3249–3292.
Calmfors, Lars and John Driffill, “Bargaining Structure, Corporatism and Macroeconomic
Performance,” Economic Policy, 1988, 3 (6), 14–61.
Card, David and Alan Krueger, Myth and Measurement: The New Economics of the Minimum
Wage, Princeton University Press, 2016.
Centamore, Giulio, “Contratti Collettivi o Diritto del Lavoro «Pirata»?,” Variazioni su Temi di
Diritto del Lavoro, 2018,2, 471.
D’Amuri, Francesco and Raﬀaella Nizzi, “Recent Developments of Italy’s Industrial Relations
System,” Questioni di Economia e Finanza (Occasional Papers) 416, Bank of Italy 2017.
Dahl, Christian, Daniel le Maire, and Jakob Munch, “Wage Dispersion and Decentralization of
Wage Bargaining,” Journal of Labor Economics, 2013, 31(3), 501–533.
Damiani, Mirella, Fabrizio Pompei, and Andrea Ricci, “Tax breaks for incentive pay, productivity
and wages: Evidence from a reform in Italy,” British Journal of Industrial Relations, London School
of Economics, 2023, 61(1), 188-213.
Daruich, Diego, Martino Kuntze, Pascuel Plotkin, and Raﬀaele Saggio, “The Consequences of
Domestic Outsourcing on Workers: New Evidence from Italian Administrative Data,” WorkINPS
Papers 84, INPS 2024.
- , Sabrina Di Addario, and Raﬀaele Saggio, “The Eﬀects of Partial Employment Protection
Reforms: Evidence from Italy,” Review of Economic Studies, 2023, 90(6), 2880–2942.
31


---
Dell’Aringa, Carlo, “Dai Minimi Tabellari ai Salari di Garanzia,” in Carlo Dell’Aringa, Claudio
Lucifora, and Tiziano Treu, eds., Produttività, Diseguaglianze, Il Mulino, 2017.
Di Addario, Sabrina, Patrick Kline, Raﬀaele Saggio, and Mikkel Sølvsten, “It Ain’t Where
You’re From, It’s Where You’re At: Hiring Origins, Firm Heterogeneity, and Wages,” Journal of
Econometrics, 2023,233 (2),340–374.
Dustmann, Christian, Attila Lindner, Uta Schönberg, Matthias Umkehrer, and Philipp Vom
Berge, “Reallocation Eﬀects of the Minimum Wage,” The Quarterly Journal of Economics, 2022,137
(1), 267–328.
- , Bernd Fitzenberger, Uta Schönberg, and Alexandra Spitz-Oener, “From Sick Man of Europe
to Economic Superstar: Germany’s Resurgent Economy,” Journal of Economic Perspectives, 2014,
28(1), 167–88.
Faia, Ester and Vincenzo Pezone, “The Cost of Wage Rigidity,” The Review of Economic Studies,
2024, 91(1), 301–339.
Fanfani, Bernardo, “The Employment Eﬀects of Collective Wage Bargaining,” Journal of Public
Economics, 2023, 227, 105006.
Goldschmidt, Deborah and Johannes Schmieder, “The Rise of Domestic Outsourcing and the
Evolution of the German Wage Structure,” The Quarterly Journal of Economics, 2017, 132 (3),
1165–1217.
Green, David, Benjamin Sand, and Iain Snoddy, “The Impact of Unions on Nonunion Wage
Setting: Threats and Bargaining,” Technical Report 22/31, Institute for Fiscal Studies2022.
Guiso, Luigi, Luigi Pistaferri, and Fabiano Schivardi, “Insurance within the Firm,” Journal of
Political Economy, 2005,113 (5),1054–1087.
Gürtzgen, Nicole, “Estimating the Wage Premium of Collective Wage Contracts: Evidence from
Longitudinal Linked Employer–Employee Data,” Industrial Relations: A Journal of Economy and
Society, 2016, 55(2), 294–322.
Hermo, Santiago, “Collective Bargaining Networks, Rent-sharing, and the Propagation of Shocks,”
2024.
Jacobson, Louis, Robert LaLonde, and Daniel Sullivan, “Earnings Losses of Displaced Workers,”
The American Economic Review, 1993, pp. 685–709.
Jäger, Simon and Jörg Heining, “How Substitutable are Workers? Evidence from Worker Deaths,”
National Bureau of Economic Research Working Paper 2022.
- , Shakked Noy, and Benjamin Schoefer, “The German Model of Industrial Relations: Balancing
Flexibility and Collective Action,” Journal of Economic Perspectives, 2022, 36(4), 53–80.
- , Suresh Naidu, and Benjamin Schoefer, “Collective Bargaining, Unions, and the Wage Structure:
An International Perspective,” National Bureau of Economic Research Working Paper 33267 2024.

32


---
Jimeno, Juan and Carlos Thomas, “Collective Bargaining, Firm Heterogeneity and
Unemployment,” European Economic Review, 2013, 59, 63–79.
Kugler, Adriana and Giovanni Pica, “Eﬀects of Employment Protection on Worker and Job Flows:
Evidence from the 1990 Italian Reform,” Labour Economics, 2008, 15(1), 78–95.
Lee, David, “Training, Wages, and Sample Selection: Estimating Sharp Bounds on Treatment
Eﬀects,” The Review of Economic Studies, 2009, 76(3), 1071–1102.
Lucifora, Claudio and Daria Vigani, “Losing Control? Unions’ Representativeness, Pirate
Collective Agreements, and Wages,” Industrial Relations: A Journal of Economy and Society, 2021,
60 (2), 188–218.
Mottironi, Bernardo, “Labour Market Power and Aggregate Productivity,” 2024.
OECD, “Negotiating Our Way Up,” 2019, p.270.
- ,“Trade Unions: Collective Bargaining Coverage (Edition 2023),” 2024.
Rizzica, Lucia, Giacomo Roma, and Gabriele Rovigatti, “The Eﬀects of Deregulating Retail
Operating Hours: Empirical Evidence from Italy,” The Journal of Law and Economics, 2023, 66(1),
21–52.
Schmieder, Johannes, Till Von Wachter, and Jörg Heining, “The Costs of Job Displacement over
the Business Cycle and its Sources: Evidence from Germany,” American Economic Review, 2023,
113 (5), 1208–1254.
Visser, Jelle, “Wage Bargaining Institutions – from Crisis to Crisis,” European Economy - Economic
Papers 2008-2015 488, Directorate General Economic and Financial Aﬀairs (DGECFIN), European
Commission 2013.

33


---
Figures
Figure 1. The 2011 Secession of Mass Retailers from their CBA: Timeline of Wage Floors for Three
Job Titles
3000

FD

Nominal monthly wage floor (euro)

CC
Max Δ: 148€
(4.8 %)
2500

Job title mid-manager

2000

Max Δ: 85€
(4.8 %)
1500
Job title 4

Max Δ: 59€
(4.8 %)

Job title 7
1000
20

20

20

20

20

20

20

20

20

20

20

20

20

20

20

20

20

19

18

17

16

15

14

13

12

11

10

09

08

07

06

05

Notes: The figure shows wage floors for the workers of firms remaining in Confcommercio (in solid blue lines—denoted
as “CC" in the paper) and for the Federdistribuzione firms (denoted as “FD" in the paper) that opt out of the collective
agreement (in red dashed lines) between 2005 and 2019. The two vertical dashed lines correspond to FD’s opt-out (in
December 2011) and to the beginning of the divergence in FD’s and CC’s wage floors (in April 2015). Three out of eight
job titles are displayed. The texts of the CBAs list the occupations corresponding to each job title. Job title 7 comprehends
shop assistants (garzoni) and cleaners (addetti alle pulizie). Job title 4 includes cashiers (cassieri), clerks (commessi), and
window dressers (vetrinisti), among others. The job title mid-manager (quadro) includes store managers (gestori di negozio)
and product managers, among others. We collect the CC wage floors in the web archive of the National Council for
Economics and Labour (cnel.it). The wage floors are manually collected from the four Commercio e Servizi (Retail and
Services) CBAs in force for the periods 01/01/2003–12/31/2006, 01/01/2007–12/31/2010, 01/01/2011–12/31/2013,
04/01/2015-12/31/2019. The latter CBA is not signed by FD, whose floors remained frozen at the 03/31/2015 level
until the end of 2018. The FD wage floors for the year 2019 are obtained from the December 2018 Distribuzione Moderna
Organizzata (Modern Organized Retail) CCNL, which can be downloaded from the website of the ADAPT think thank
https://www.bollettinoadapt.it/ccnl-distribuzione-moderna-organizzata-dmo/.

34


---
Figure 2. Case Study of Pirate Agreement vs. Conventional CBA: Wage Floors in the Wholesale
and Retail Sector, 2018
3000

2500

2000

1500

1000
Mid-Manager

1

2

3

4

5

6

7

Job Title
CC-CBA

Pirate CBA - Lombardy

Pirate CBA - Molise

Notes: Wage floors across job titles for the CC-CBA (CNEL CBA code H011, white bars) and pirate CBA (CNEL CBA
code H024, red and blue markers) in the retail sector in 2018. For the pirate CBA, the top (red) marker is the wage
floor for Lombardy, in the North (the region with the largest equalization element) and the bottom (blue) marker is the
wage floor for Molise, in the South (the region with the lowest equalization element). The equalization element was
introduced by the pirate CBA to diﬀerentiate wage floors across regions based on the regional cost of living. Appendix
A2 provides more details.

Figure 3. The Evolution of Pirate Agreements
(b) Share of Workers and Firms With Pirate Contract

 








































 
















































(a) Counts of Contracts

7RWDOQXPEHURI&%$V

3LUDWH&%$V

:RUNHUV

)LUPV

Notes: Panel (a) depicts the total number of CBAs in Italy per year, separately for pirate agreements (dashed line) and
the total number including them (solid line). Pirate agreements are defined as those not signed by at least one of the
three traditional unions (CGIL, CISL, UIL). Panel (b) shows the fraction of firms (dashed line) and workers (solid line)
covered by pirate CBAs. For firms, the share is computed as the number of firms adopting a pirate contract for at least
one employee as a share of the total number of private-sector firms in the INPS data each year. For workers, the share is
computed as the total number of workers covered by a pirate contract as a fraction of the total number of private-sector
workers in the INPS data each year. See Section 4 for a description of the INPS administrative data.

35


---
Figure 4. The Eﬀects of the 2011 Secession of Mass Retail Employers on Workers
(a) Log Weekly Wages

(b) Employed

(c) Employed at 2010 Firm

(d) Earnings

Notes: This figure displays the event-study coeﬃcients from Equation (1) estimated on the matched sample defined in
Section 5.1. Panel (a): Log weekly wages are calculated for the dominant job, i.e., the job with most weeks worked in
a given year. We report the eﬀects for the full matched sample ("Overall", hollow circles), and additionally the eﬀects
conditioning on the worker staying with their 2010 employer ("Stayer", full triangles). To construct the latter, we fit
Equation (1) just among pairs of matched treated and control workers who, for each year after 2010, are both still
employed with their 2010 employer in that given year. Panel (b): Employed is an indicator equal to 1 if a given worker
in year C has at least one day of employment according to social security records. Panel (c): the outcome is an indicator
equal to 1 if a given worker in year C is employed by their 2010 employer. Panel (d): Earnings are calculated as the sum
of labor earnings obtained by a worker in a given year and are expressed in 2010 euros (earnings are set equal to zero
for non-employed workers). Table 3 reports these event-study coeﬃcients along with additional summary statistics.
The two vertical lines correspond to 2011—the year when FD abandoned the CC employer organization— and 2015, the
year when a new CC-CBA was signed. Standard errors are clustered at the level of the 2010 employer.

36


---
Figure 5. The Eﬀects of Pirate Agreement Adoptions on Workers
(a) Log Weekly Wages

(c) Employed at (C ⇤

(b) Employed

1) Firm

(d) Earnings

Notes: This figure displays the event-study coeﬃcients from Equation (2) estimated on the matched sample defined in
Section 5.2. Panel (a): Log weekly wages are calculated for the dominant job, i.e., the job with most weeks worked in
a given year. We report the eﬀects for the full matched sample ("Overall", hollow circles), and additionally the eﬀects
conditioning on the worker staying with their C ⇤ 1 employer ("Stayer", full triangles). To construct the latter, we fit
Equation (2) just among pairs of matched treated and control workers who, for each period after C ⇤ 1, are both still
employed with their C ⇤ 1 employer in that given period. Panel (b): Employed is an indicator equal to 1 if a given worker
in year C has at least one day of employment according to social security records. Panel (c): the outcome is an indicator
equal to 1 if a given worker in year C is employed by their C ⇤ 1 employer, where C ⇤ denotes the year of transition to
a pirate agreement. Panel (d): Earnings are calculated as the sum of labor earnings obtained by a worker in a given
year and are expressed in 2010 euros (earnings are set equal to zero for non-employed workers). Table 4 reports these
event-study coeﬃcients along with additional summary statistics. Standard errors are clustered at the level of the C ⇤ 1
employer.

37


---
Figure 6. The Eﬀects of Pirate Agreement Adoptions on Firms
(a) Log Weekly Wages

(b) Survival Probability

(c) Log Firm Size

(d) Log Firm Size (De-trended)

(e) Share of New Hires

(f) Log Weekly Wages of New Hires

Notes: This figure displays the event-study coeﬃcients from Appendix Equation (C1) estimated on the matched sample
defined in Appendix C. Panel (a): Log weekly wages is the mean log weekly wage paid by firm 9 to its workers, expressed
in 2010 euros; Panel (b): the outcome is a year-to-year binary indicator taking value of 1 if firm 9 is observed in the data;
Panel (c): the outcome is the logarithm of the total number of the firm’s employees; Panel (d) reproduces the coeﬃcients
of Panel (c) after subtracting their linear time trend estimated in the pre-event periods and extrapolated for the later
years as in Dustmann et al. (2022). Panel (e): the share of new hires at the firm is the number of new hires in firm 9
scaled by total firm employment each period. Panel (f): the outcome is the mean log weekly wage paid by firm 9 to its
newly hired employees, regardless of whether they are hired under a pirate CBA or not. Appendix Table C2 reports
these event-study coeﬃcients along with additional summary statistics. Standard errors are clustered at the firm level.

38


---
Figure 7. The Eﬀects of Opt-Outs on Workers: Heterogeneity by Geography
(a) FD design: Center-North

(b) FD design: South

(c) Pirate CBAs design: Center-North

(d) Pirate CBAs design: South

Notes: This figure displays the event-study coeﬃcients from Equation (1) estimated on the matched sample defined in
Section 5.1 (Panels (a) and (b)) and from Equation (2) estimated on the matched sample defined in Section 5.2 (Panels
(c) and (d)). The regressions are run separately for workers in the Center-North and South of Italy in 2010 (Panel a for
Center-North, Panel b for South) or at time C ⇤ 1 (Panel c for Center North, Panel d for South). Southern regions are
Abruzzo, Basilicata, Calabria, Campania, Molise, Apulia, Sardinia and Sicily. Log weekly wages are calculated for the
dominant job, i.e., the job with most weeks worked in a given year. Employed is an indicator equal to 1 if a given worker
in year C has at least one day of employment according to social security records. Employed at 2010 firm or (C ⇤ 1) firm
is an indicator equal to 1 if a given worker in year C is employed by their 2010 employer or their C ⇤ 1 employer (C ⇤
denotes the year of transition to a pirate agreement). Earnings are calculated as the sum of labor earnings obtained by
a worker in a given year and are expressed in 2010 euros. Mean earnings for the control group in the pre-event years
for FD design: Ä22,581 in the South, Ä22,230 in the Center-North; for Pirate CBAs design: Ä15,944 in the South, Ä19,520
in the Center-North. Coeﬃcients for Log Weekly Wages, Employment, and Employment at the 2010 or (C ⇤ 1) Firm are
displayed on the left vertical axis. Coeﬃcients for Earnings are displayed on the right vertical axis. Standard errors are
clustered at the level of the 2010 employer (Panels (a) and (b)) or the C ⇤ 1 employer (Panels (c) and (d)).

39


---
Figure 8. The Eﬀects of Opt-Outs on Worker Separations: Heterogeneity by Geography
(a) Pirate CBAs design: Center-North

(b) Pirate CBAs design: South

(c) FD design: Center-North

(d) FD design: South

Notes: This figure displays the event-study coeﬃcients from Equation (1) estimated on the matched sample defined in
Section 5.1 (Panels (c) and (d)) and from Equation (2) estimated on the matched sample defined in Section 5.2 (Panels
(a) and (b)). The regressions are run separately for workers in the Center-North and South of Italy in 2010 (Panel (c) for
Center-North, Panel (d) for South) or at time C ⇤ 1 (Panel (a) for Center-North, Panel (b) for South). Southern regions
are Abruzzo, Basilicata, Calabria, Campania, Molise, Apulia, Sardinia and Sicily. Voluntary separations is a binary
indicator taking value of one if the worker has resigned from their 2010 job (Panels (c) and (d)) or their C ⇤ 1 job (Panels
(a) and (b)). Once the worker resigns, the outcome stays equal to one for the following years. Involuntary separations
is a binary indicator taking value of one if the worker has been fired from their 2010 job (Panels (c) and (d)) or their
C ⇤ 1 job (Panels (a) and (b)). Once the worker has been fired, the outcome stays equal to one for the following years.
Standard errors are clustered at the level of the 2010 employer (Panels (c) and (d)) or the C ⇤ 1 employer (Panels (a) and
(b)).

40


---
Figure 9. Opt-Outs with Heterogeneous Productivity and Labor Supply Elasticities

Notes: The figure highlights the predicted eﬀects of an opt-out from a CBA in a simple monopsony model
where there are two firms: (# , (). Firm # has higher productivity than firm ( as captured by the rightward
parallel shift in its marginal revenue product of labor (MRPL) curve while firm ( has a less elastic labor
supply curve (and thus more elastic inverse labor supply curve F ( (!)). In the status quo, both firms are
mandated to pay a wage set by the national CBA, F̄ ⇠⌫ . The level of employment in the status quo is
thus found at the intersection of F̄ ⇠⌫ with labor demand (the MRPL curve). If both firms opt out, then
each employer becomes a wage setter. The level of employment chosen by the firm after the opting out
>?C8= 6 >DC

event—! 9

— is found at the intersection of the MRPL curve with the marginal cost curve of the
>?C8= 6 >DC

firm " ⇠ 9 and the wage is found on the inverse labor supply curve at the point F 9

. The more

productive firm with a higher labor supply elasticities (the firm in the North) pays a lower wage but has
higher employment level following the opting-out event. The less productive firm (but with a very inelastic
labor supply curve)—the firm in the South—sets the wage even lower than the more productive firm and
has lower employment compared to the status quo given its more inelastic labor supply curve.

41


---
Tables
Table 1. The 2011 Secession of Mass Retailers from their CBA: Descriptive Statistics of Workers
Full sample

Female
Age
Full time
Temporary contract
Log weekly wage
Earnings
Blue collar
White collar
Mid manager
Firm size*
South
N. observations

(1)
Treated
0.60
(0.49)
38.18
(8.48)
0.58
(0.49)
0.01
(0.09)
6.19
(0.31)
22,317
11,539
0.07
(0.26)
0.90
(0.29)
0.16
(0.16)
3,292
(4,516)
0.15
(0.36)
102,911

(2)
Controls
0.47
(0.50)
39.35
(9.09)
0.82
(0.38)
0.02
(0.12)
6.25
(0.38)
26,191
14,819
0.35
(0.48)
0.61
(0.49)
0.20
(0.20)
62
(204)
0.18
(0.38)
419,448

Matched sample
(3)
Treated
0.59
(0.49)
38.94
(8.33)
0.63
(0.48)
0.01
(0.09)
6.21
(0.31)
23,250
11,505
0.08
(0.26)
0.90
(0.3)
0.16
(0.16)
3,292
(4,516)
0.15
(0.36)
91,753

(4)
Controls
0.58
(0.49)
38.81
(8.39)
0.63
(0.48)
0.01
(0.09)
6.21
(0.35)
23,190
12,197
0.08
(0.27)
0.89
(0.31)
0.16
(0.16)
69
(227)
0.14
(0.35)
91,753

Notes: This table reports averages of the characteristics by group: workers in FD
firms in 2010, and those in CC firms (but not FD) in 2010. Standard deviations
are reported in parentheses. Statistics are reported separately before (Columns (1)(2)) and after (Columns (3)-(4)) matching. Female, Full time, Temporary contract,
Blue collar, White collar, Mid-manager and South are all indicator variables. Age
is measured in years. Log weekly wages are expressed in log euros (2010 prices).
Earnings are the total labor earnings received by the worker from all employers in
a given year (euros, 2010 prices). Earnings are set equal to zero for non-employed
workers. *Firm size is firm-weighted.

42


---
Table 2. Pirate Agreement Adoptions: Descriptive Statistics of Workers
Full sample

Female
Age
Full-time
Temporary contract
Log weekly wage
Earnings
Blue collar
White collar
Mid manager
Firm size*
South
N. observations

(1)
Treated
0.51
(0.50)
41.38
(9.47)
0.68
(0.47)
0.07
(0.26)
6.00
(0.43)
21,312
(14,251)
0.50
(0.50)
0.47
(0.50)
0.03
(0.16)
299
(3,294)
0.30
(0.46)
38,248

(2)
Controls
0.40
(0.49)
41.93
(9.62)
0.79
(0.40)
0.07
(0.26)
6.13
(0.43)
19,825
(15,384)
0.57
(0.49)
0.39
(0.49)
0.04
(0.20)
10
(163)
0.22
(0.42)
67,285,888

Matched sample
(3)
Treated
0.53
(0.50)
41.51
(9.33)
0.68
(0.47)
0.05
(0.23)
6.01
(0.42)
20,056
(12,290)
0.48
(0.50)
0.49
(0.50)
0.03
(0.18)
179
(547)
0.28
(0.45)
24,952

(4)
Controls
0.53
(0.50)
41.48
(9.58)
0.67
(0.47)
0.06
(0.23)
6.00
(0.45)
19,992
(13,081)
0.48
(0.50)
0.48
(0.50)
0.04
(0.19)
176
(1,046)
0.27
(0.45)
24,952

Notes: This table reports descriptive statistics averaged between 2008 and 2016 by group.
Columns (1) and (2) refer to the sample before the matching. Column (1) reports the C ⇤ 1
descriptives for workers on a standard CBA that will experience a within-job transition
to a pirate CBA at C ⇤ ; Column (2) reports descriptives for potential control workers, that
is, workers never covered by a pirate CBA. Columns (3) and (4) show descriptives for the
matched sample, obtained as described in Section 5.2. Standard deviations are reported
in parentheses. Female, Full time, Temporary contract, Blue collar, White collar, Midmanager and South are all indicator variables. Age is measured in years. Log weekly
wages are expressed in log euros (2010 prices). Earnings are the total labor earnings
received by the worker from all employers in a given year (euros, 2010 prices). Earnings
are set equal to zero for non-employed workers. *Firm size is firm-weighted.

43


---
Table 3. The Eﬀects of the 2011 Secession of Mass Retail Employers on Workers

On Impact (C ⇤ )
Medium Run (C ⇤ +2)
Long Run (C ⇤ +5)
N. observations
Mean Outcome
Average of Pre-Event Coeﬀs
p-value Pre-Event Coeﬀs = 0

(1)
Log Weekly Wages

(2)
Employed
0.0027
(0.0043)
0.0262
(0.0087)***
0.0430
(0.0138)***

(3)
Employed
at 2010 Firm
0.0298
(0.0093)***
0.0911
(0.0420)**
0.1962
(0.0439)***

-0.0136
(0.0058)**
-0.0054
(0.0081)
-0.0322
(0.0101)***
2,523,222
6.1363
-0.0021
(0.0082)
0.8001

(4)
Earnings
-358.97
(180.90)**
433.42
(296.56)
0.03
(442.35)

2,732,810
0.9988
0.0010
(0.0004)***
0.0087

2,732,810
0.9321
0.0026
(0.0188)
0.8890

2,732,810
22,283
-493.36
(207.92)**
0.02

Notes: This table reports three event-study coeﬃcients from Equation (1) estimated on the matched sample
defined in Section 5.1. ‘On Impact’ denotes the coeﬃcient estimated for the year 2011, ‘Medium Run’ corresponds
to the coeﬃcient for the year 2013, and ‘Long Run’ refers to the coeﬃcient for the year 2016. ‘Mean Outcome’
represents the mean of the outcome of interest over the period 2005-2010, computed considering the control group
only. The last rows show the mean event-study coeﬃcient between 2005 and 2010 (‘Average of Pre-Event Coeﬀs’),
the standard error in parentheses, and the p-value of the test that the mean pre-event coeﬃcient is equal to zero,
all computed using the lincom command in Stata. Log weekly wages are calculated for the dominant job, i.e., the
job with higher weeks worked in a given year. Employed is an indicator equal to 1 if a given worker in year C
has at least one day of employment according to social security records. Employed at 2010 firm is an indicator
equal to 1 if a given worker in year C is employed by their 2010 employer. Earnings are calculated as the sum of
labor earnings obtained by a worker in a given year and are expressed in 2010 euros (earnings are set equal to
zero for non-employed workers). Standard errors, clustered at the firm level of the 2010 employer, are shown in
parentheses. * p<0.10, ** p<0.05, *** p<0.01.

44


---
Table 4. The Eﬀects of Pirate Agreement Adoptions on Workers

On Impact (C ⇤ )
Medium Run (C ⇤ + 2)
Long Run (C ⇤ + 5)
N. observations
Mean Outcome
Average of Pre-Event Coeﬀs
p-value Pre-Event Coeﬀs = 0

(1)
Log Weekly Wages

(2)
Employed

(4)
Earnings

0.0000
(0.0003)
0.0189
(0.0052)***
0.0306
(0.0087)***

(3)
Employed
at (C ⇤ 1) Firm
0.0000
(0.0005)
0.0041
(0.0146)
0.0262
(0.0221)

-0.0202
(0.0041)***
-0.0238
(0.0044)***
-0.0248
(0.0074)***
477,920
6.0011
-0.0050
(0.0040)
0.2170

521,022
0.9445
0.0091
(0.0055)
0.1040

521,022
0.8062
0.0037
(0.0141)
0.7924

521,022
18,561
-165.89
(111.18)
0.14

-98.19
(94.40)
-121.73
(125.26)
194.57
(192.38)

Notes: This table reports three event-study coeﬃcients from Equation (2) estimated on the matched sample defined
in Section 5.2. ‘On Impact’ denotes the coeﬃcient estimated in the opt-out year C ⇤ , ‘Medium Run’ corresponds
to the coeﬃcient two years after the opt-out, and ‘Long Run’ refers to the coeﬃcient five years after the opt-out.
‘Mean Outcome’ represents the mean of the outcome of interest in the five years before the opt-out, computed
considering the control group only. The last rows show the mean event-study coeﬃcient in the five years before
the opt-out (‘Average of Pre-Event Coeﬀs’), the standard error in parentheses, and the p-value of the test that
the mean pre-event coeﬃcient is equal to zero, all computed using the lincom command in Stata. Log weekly
wages are calculated for the dominant job, i.e., the job with higher weeks worked in a given year. Employed is
an indicator equal to 1 if a given worker in year C has at least one day of employment according to social security
records. Employed at (C ⇤ 1) firm is an indicator equal to 1 if a given worker in year C is employed by their C ⇤ 1
employer. Earnings are calculated as the sum of labor earnings obtained by a worker in a given year and are
expressed in 2010 euros (earnings are set equal to zero for non-employed workers). Standard errors, clustered at
the firm level of the C ⇤ 1 employer, are shown in parentheses. * p<0.10, ** p<0.05, *** p<0.01.

45


---
Opting Out of Centralized Collective Bargaining:
Evidence from Italy
Christian Dustmann, Chiara Giannetto, Lorenzo Incoronato, Chiara Lacava,
Vincenzo Pezone, Raffaele Saggio, Benjamin Schoefer

July 18, 2025

Online Appendix

1


---
A Further Details on the Opt-out Events
In this Appendix we provide additional institutional details and descriptive statistics related to the
two opt-out events studied in the paper.

A.1 The 2011 Secession of Mass Retailers
Set of FD Firms. To identify our set of ''treated'' firms, we obtain the 2010 list of FD members,
published on the association's website. We then manually match the firms' names with their fiscal
identifiers (which correspond to the Cerved identifier, see Section 4). The firms are: A&O,
Assofranchising, Auchan, Bennet, Bricocenter, Bricoman, C&A, Cadoro, Carrefour, Coin, Conbipel,
Conforama, Decathlon, Despar – Eurospar – Spar, D Per Dì, Douglas, Eldo, Elite, Emmezeta Moda,
Esselunga, Etruria Retail, Euronics, Expert, Famila, Finiper, Fiordaliso, Gre, Grosmarket, Gruppo
Vege’, Gruppo Zambaiti, GS, Ikea, Il Gigante, In’S Mercato, Iperal, Italmark, Jysk, Kiko, La
Gardenia, Ld Market, Leroy Merlin, Limoni, Max & Co., Max Mara, Maxi Zoo, Mediaworld –
Saturn, Metro Italia, Gruppo Miroglio Fashion, Oasi – Gruppo Gabrielli – Tigre, OVS, Pac 2000A,
Pam – Panorama, Pellicano, Penny Market, Percassi, Prix, Rinascente, Selex, Self, Sinergy, Sisa,
SSC, Superconti, Unes, Unieuro, Universo Sport, Zara. Less than a quarter of the FD firms are
multinationals.
Firm-Level Unilateral Wage Raises. As discussed in Section 3.1, FD firms' wages did not remain
frozen to the level established by the pre-opt-out CBA. Indeed, FD firms voluntarily and unilaterally
granted some small wage raises between 2015 and 2018. After a new CBA was signed in 2015 by
CC firms, unions rejected FD's proposal to merely replicate CC-CBA wage floor increases. Unions
believed that the larger FD firms should provide more meaningful wage increases than those designed
for small CC retailers. As part of this conflict, the unions implemented three short strikes between
November 2015 and May 2016. FD firms also engaged in hostile industrial relations actions, e.g.,
they cut the generosity of supplementary health insurance and abolished lower-level work councils
(Enti Bilaterali Territoriali). To partially accommodate unions' demands, FD firms implemented
2


---
unilateral raises that took effect on May 2016 and June 2017 and that only partially match those
established by the CC-CBA. The resulting wage floors for FD firms' employees are depicted in Figure
A1 (green dashed line), which integrates Figure 1 in the main text. Differences between these wage
floors and those enforced in CC firms reflect the degree to which FD firms (i) were able to deviate
from the CC-CBA wage floors and (ii) decided to take advantage of the former. We view all of the
aforementioned events as outcomes of the opt-out, which complement our econometric analysis on
how this opt-out event impacted actual wages and employment outcomes.

A.2 Adoptions of Pirate Agreements
Descriptive Statistics on the Adoption of Pirate Agreements. Table A1 summarizes the
characteristics of workers employed under pirate and standard CBAs between 2008 and 2016. The
sample includes all contracts, with each observation representing a unique job-year pair. Pirate CBAs
account for approximately 1.2% of all observations. Each column distinctly reports the share of
workers with a given characteristic within each type of collective agreement.

Workers under pirate CBAs are more likely to be women and to work part-time. On average, they
also receive lower weekly wages. Differences in age and the prevalence of temporary contracts are
negligible. Additionally, workers on pirate contracts are more likely to be employed in white-collar
occupations and to work in Southern regions. These regional differences are also evident in Figure
A2. Panel (a) shows the share of pirate CBAs relative to total contracts by province in 2019, while
Panel (b) presents the share of firms applying at least one pirate CBA to their workers. Both panels
highlight the substantially higher prevalence of pirate contracts in Southern Italy.

Table A2 presents the distribution of pirate and standard CBAs across sectors. Pirate contracts are
relatively more common in trade (22% of pirate CBAs vs. 15% of standard CBAs), administrative
and support services (12% vs. 10%), human health and social work (7% vs. 4%), and information and
3


---
communication technology (7% vs. 3%). In contrast, pirate CBAs are less prevalent in manufacturing
(20% vs. 27%) and finance and insurance (0.54% vs. 4%) compared to standard CBAs.

Finally, Appendix Table A3 summarizes the characteristics of firms that use at least one pirate CBA
between 2008 and 2016 compared to those that do not. The sample includes all firms, with each
observation representing a unique firm-year pair. Firms using pirate CBAs tend to be larger than the
average firm (14 vs. 8 employees, on average), are more likely to be headquartered in the South, and
have been in operation for fewer years on average (11 vs. 13). They also employ a higher share of
women (0.59 vs. 0.47). While firms with pirate CBAs show no major differences in average worker
age, share of temporary contracts, log weekly wages, or leverage, their average log productivity is
lower than that of firms using only standard CBAs.

An Example of a Pirate Agreement. Section 3.2 in the main text briefly discusses the example of a
pirate CBA introduced in the retail sector. We present additional details here to illustrate the typical
motivations behind signing a pirate agreement. In 2012, a set of smaller employer and employee
associations (Confazienda, Fedimpresa, Unica and Cisal) signed a new CBA in the retail sector, which
by 2018 covered 731 firms and 12,000 workers (the 0.2% and 0.5% of the total number of firms and
workers covered by the CC-CBA, respectively). An excerpt of the contract sheds light on the stated
motivations:
The old contracts prefer the death of companies and jobs rather than giving in, albeit
marginally, to previous economic and regulatory achievements [...]. The system thus prefers
to talk about 'Pirate Contracts' whenever there is a search for a contractual solution compatible
with the existing difficulties [...]. Any CBA that is not a bad copy of the corresponding text
written down by the so-called 'comparatively more representative trade unions at national
level' is qualified as a 'pirate' [...]. The knowledge of the market situation by all the parties
involved (companies, workers, trade associations and trade unions) [...] is the only
4


---
contractually possible way to effectively combat the crisis [...]. The parties now find
anachronistic the claim to define all the various contractual institutions and salaries in a
homogeneous way for the entire national territory, which has many and significant
heterogeneities [...]. The choice of this CBA is: (a) to lay down essential wages and standards
which meet the primary needs of all workers; (b) to give priority to second-level bargaining;
c) to recognize a Regional Equalization Element, proportionate to the Regional Cost of Living
Indices, to reduce differences in purchasing power at the same nominal wage.

As shown in Figure 2 in the main text, this location-based adjustment—the Regional Equalization
Element set in provision (c) above—amounts to roughly 5.3% of the national wage floor in the
northern region of Lombardia, where the Regional Equalization Element was largest. In the southern
region of Molise, the Regional Equalization Element was lowest, at 0.4% for mid-managers up to
0.9% for the lowest occupational group.

5


---
B Additional Results
This section presents additional results and robustness tests.

Concurrent Liberalization of Shop Opening Hours. As discussed in Section 6.1, the FD opt-out
coincided with the nationwide liberalization of shop opening hours for the retail sector, namely the
retailers' possibility to keep their stores open on Sundays or national holidays. In principle, such a
liberalization could differentially affect mass-retail firms, i.e., precisely the FD firms that decided to
opt-out from the CC-CBA, as they could be better equipped to take advantage of this opportunity.
Importantly, a staggered liberalization of shop opening hours for municipalities most reliant on
tourism had already started in 1998, with specific application criteria set by regional governments
(Rizzica, Roma and Rovigatti, 2023). To show that this reform does not explain our results, we
replicate our wage analysis only on the workers employed in municipalities that had not already
liberalized shop opening hours in the year prior to the FD opt-out.35 These workers were thus affected
by both the opt-out decision and the lifting of the restriction. However, as shown in Figure B1, the
effect on wages for this group of workers (blue line) is very similar to the baseline estimate obtained
on the full sample (red line).

Employment effects conditional on firm survival. Results in Section 6.2 show a positive
employment effect for workers subject to a pirate agreement opt-out. Here, we show that these effects
are not driven by higher survival probabilities of firms adopting pirate CBAs as opposed to firms that
do not. Figure B2 shows event study coefficients resulting from estimating Equation (2) on the
matched sample defined in Section 5.2, focusing exclusively on workers’ employment probability at
any firm (corresponding to Figure 5, Panel (b)) and restricting the estimation sample to matched
treated and control workers whose starting (!!∗ − 1) firm is still in business. Coefficient estimates are

35

We thank Lucia Rizzica, Giacomo Roma and Gabriele Rovigatti for sharing these data with us.

6


---
positive and quantitatively similar to those obtained without imposing restrictions on firm survival,
suggesting that the positive effect on workers’ employment probability following a pirate CBA optout is not driven by differential effects on firm survival probabilities.

7


---
C Firm-level Analysis
This appendix describes our firm-level analysis of the effects of opt-out via the signing of a pirate
CBA.

Econometric analysis. We employ a matched difference-in-differences strategy that compares
treated firms—those that opt out—with a matched group of control firms that do not. We define the
treatment year as the first year a firm uses a pirate CBA for at least one worker. As in the workerlevel design, we focus on all the firms for which the treatment year is between 2008 and 2016. We
then run the following event-study regression:
(

(

!," = #, + d" + % g' ∙ 0:/ = /,∗ + 2; + % b' ∙ 0:/ = /,∗ + 2; ∙ 4, + u," ,
')*(
')*(

(<1)

where !," is the outcome of interest for firm = in year /, #, and d" are firm and year dummies and g'
is a set of event-study coefficients capturing the effect of being 2 years away from the event year, /,∗
(that is, the year of the opt-out).36 4, is a treatment indicator equal to one if firm = adopts the pirate
agreement and zero otherwise. The coefficients of interest (the b' ’s) capture the change in !,"
between treated and control firms 2 years before/after the opt-out relative to the same difference in
the year before the opt-out, which is normalized to zero. The outcomes we focus on in the main text
are the firm’s average wage paid to its employees, its survival probability (a dummy taking value of
one if the firm is observed in the data and zero otherwise), the (log) number of employees, the
employment share of new hires at the firm and the average wage of new hires. In this appendix we
also report an event-study having as outcome the share of workers subject to a pirate agreement
(Figure C1), and firm-level results separately for firms located in the Center-North versus South of
Italy (Figure C2).

36
For a control firm, this is the year of the adoption of the pirate agreement of the treated firm matched to this particular
control firm.

8


---
Matching Strategy and Sample. We implement a matching algorithm that assigns each treated firm
to a control one with similar characteristics prior to the opt-out. Potential control firms are all those
that never applied a pirate contract. The propensity score model controls for the firm's average wage
paid in the three years before the opt-out, firm size, sector, value added per worker, sales growth,
profits-to-assets ratio and financial leverage. The matching procedure delivers a sample of 2,144
treated firms and an equal number of control firms. Table C1 reports descriptive statistics for the full
sample of firms and for the matched sample. With the exception of firm size, which remains larger
on average in treated firms, the matching algorithm is successful in balancing the key covariates.
Table C2 shows regression results corresponding to the event study estimates in Figure 6 in the main
text.

9


---
Online Appendix Figures and Tables
Appendix Figure A1. The 2011 Secession of Mass Retailers from their CBA: Timeline of Wage
Floors for Three Job Titles (Including Unilateral Wage Raises)
3000

FD

Nominal monthly wage floor (euro)

CC
FD with firm floors

Max Δ: 148€
(4.8 %)

2500

Job title mid-manager

2000

Max Δ: 85€
(4.8 %)
1500
Job title 4

Max Δ: 59€
(4.8 %)

Job title 7
1000
20

20

20

20

20

20

20

20

20

20

20

20

20

20

20

20

20

19

18

17

16

15

14

13

12

11

10

09

08

07

06

05

Notes: The figure shows wage floors for the workers of firms remaining in Confcommercio (in solid blue lines—
denoted as “CC" in the paper) and for the Federdistribuzione firms (denoted as “FD" in the paper) that opt out of the
collective agreement (in red dashed lines) between 2005 and 2019. The two vertical dashed lines correspond to FD’s
opt-out (in December 2011) and to the beginning of the divergence in FD’s and CC’s wage floors (in April 2015). Three
out of eight job titles are displayed. The texts of the CBAs list the occupations corresponding to each job title. Job
title 7 comprehends shop assistants (garzoni) and cleaners (addetti alle pulizie). Job title 4 includes cashiers (cassieri),
clerks (commessi), and window dressers (vetrinisti), among others. The job title mid-manager (quadro) includes store
managers (gestori di negozio) and product managers, among others. The green dashed lines depict the wage floors wages
granted by FD firms via unilateral raises. We collect the CC wage floors in the web archive of the National Council for
Economics and Labour (cnel.it). The wage floors are manually collected from the four Commercio e Servizi (Retail and
Services) CBAs in force for the periods 01/01/2003–12/31/2006, 01/01/2007–12/31/2010, 01/01/2011–12/31/2013,
04/01/2015-12/31/2019. The latter CBA is not signed by FD, whose floors remained frozen at the 03/31/2015 level
until the end of 2018. The FD wage floors for the year 2019 are obtained from the December 2018 Distribuzione
Moderna Organizzata (Modern Organized Retail) CCNL, which can be downloaded from the website of the ADAPT
think thank https://www.bollettinoadapt.it/ccnl-distribuzione-moderna-organizzata-dmo/. The wage floors
resulting from the unilateral raises are obtained from the website of FILCAMS-CGIL, one of the largest unions in the
retail sector (https://www.filcams.cgil.it/page/federdistribuzione)

10


---
Appendix Table A1. Worker Characteristics by Type of Agreement

Female
Age
Full-time
Temporary contract
Log weekly wage
Blue collar
White collar
Mid manager
South
N. Observations

(1)
Pirate contracts
0.47
(0.50)
39.67
(10.70)
0.67
(0.47)
0.18
(0.38)
5.95
(0.51)
0.50
(0.50)
0.42
(0.49)
0.03
(0.18)
0.33
(0.47)
1,402,379

(2)
Standard contracts
0.41
(0.49)
39.46
(10.89)
0.74
(0.44)
0.19
(0.39)
6.03
(0.51)
0.56
(0.50)
0.35
(0.47)
0.03
(0.17)
0.24
(0.43)
120,028,877

Notes: This table reports descriptive statistics for all workers in the INPS
data between 2008 and 2016. Column (1) refers to the sample of workers
covered by a pirate CBA at any point in time in 2008-2016, Column (2)
to other workers (those not covered by a pirate CBA). All statistics are
computed as averages between 2008 and 2016. Standard deviations are
reported in parentheses. Female, Full time, Temporary contract, Blue collar,
White collar, Mid-manager and South are all indicator variables. Age is
measured in years. Log weekly wages are expressed in log euros (2010
prices).

11


---
Appendix Table A2. Distribution (%) of Workers across Sectors by Type of Agreement

Agriculture, Forestry and Fishing
Mining and Quarrying
Manufacturing
Electricity, Gas, Steam and Air Conditioning Supply
Water Supply, Sewerage, Waste Management
Construction
Wholesale and Retail Trade
Transportation and Storage
Accommodation and Food
Information and Communication
Finance and Insurance
Real Estate Activities
Professional, Scientific and Technical Activities
Administrative and Support Service Activities
Public Administration and Defence
Education
Human Health and Social Work
Arts, Entertainment and Recreation
Other Service Activities
Activities of Households as Employers
Activities of Extraterritorial Organisations

(1)
Pirate contracts
2.11
0.01
19.92
0.07
0.24
0.75
22.29
7.98
1.89
8.69
0.54
0.73
3.74
12.11
0.67
1.32
7.22
1.64
7.63
0.05
0.43

(2)
Standard contracts
0.63
0.35
27.24
0.53
0.89
8.33
15.16
6.74
9.59
2.74
3.94
0.30
3.02
9.95
0.57
1.38
4.39
0.58
3.34
0.31
0.03

Notes: This table reports descriptive statistics for all workers in the INPS data between 2008 and 2016. Column (1) refers
to the sample of workers covered by a pirate CBA at any point in time in those years, column (2) to other workers (those
not covered by a pirate CBA). All statistics are computed as averages between 2008 and 2016.

12


---
Appendix Table A3. Firm Characteristics by Type of Agreement

Firm size
South
Firm age
Share of full-time
Share of temporary jobs
Share of women
Share of blue collar
Share of white collar
Share of apprentices
Share of mid-managers
Share of managers
Mean worker age
Log weekly wage
Log assets
Log productivity
Leverage
N. Observations

(1)
Pirate firms
14.14
(374.39)
0.15
(0.36)
10.53
(10.9)
0.50
(0.43)
0.15
(0.30)
0.59
(0.41)
0.43
(0.46)
0.47
(0.45)
0.08
(.23)
0.004
(0.05)
0.006
(0.06)
37.1
(8.7)
5.85
(0.39)
5.89
(1.66)
3.33
(0.92)
0.81
(0.33)
190,873

(2)
Other firms
8.39
(157.69)
0.08
(0.27)
13.06
(12.2)
0.60
(0.43)
0.15
(0.29)
0.47
(0.42)
0.58
(0.43)
0.31
(0.41)
0.10
(.24)
0.005
(0.05)
0.002
(0.03)
37.8
(9.0)
5.85
(0.38)
6.50
(1.63)
3.51
(0.87)
0.81
(0.32)
14,151,780

Notes: This table reports descriptive statistics for all firms in the INPS
data between 2008 and 2016. Column (1) refers to the sample of firms
using a pirate agreement for at least one worker at any point in time
between 2008 and 2016, column (2) to firms not using pirate agreements.
All statistics are computed as averages between 2008 and 2016. Standard
deviations are reported in parentheses. Log weekly wages and assets
are expressed in log euros (2010 prices). Productivity is computed as
value added per worker. Leverage is computed as 1-equity/assets (for
pirate firms, it is computed in the year before the adoption of the pirate
CBA). South is an indicator variable. Firm age is measured in years.

13


---
Appendix Figure A2. Geographical Distribution of Pirate Contracts, 2019
(a) Workers

(b) Firms

Notes: For workers, the share of pirate contracts is computed as the total number of workers covered by a pirate
contract as a fraction of the total number of workers in the INPS data in each province in 2019. For firms, the
share is computed as the number of firms applying a pirate contract to at least one employee as a share of the total
number of firms in the INPS data in each province in 2019.

14


---
Appendix Figure B1. Robustness on liberalization of shop opening hours

Notes: This figure displays the event-study coeﬃcients from Equation (1) estimated on the matched sample defined in
Section 5.1, using log weekly wages as outcome. The red coeﬃcients denote the baseline results for the entire matched
sample ("Overall" in Figure 4 Panel a). The blue event-study coeﬃcients are obtained when excluding workers in
municipalities where shop opening hours were not liberalized in 2010 (see Section 6.1 and Appendix B for details).

Appendix Figure B2. The Eﬀects of Pirate Agreements on Workers, Conditional on Firm Survival

Notes: This figure displays the event-study coeﬃcients from Equation (2) estimated on the matched sample defined
in Section 5.2, using worker employment probability as outcome. The regressions are estimated conditional on the
C ⇤ 1 employer still existing for both treated and control workers. Standard errors are clustered at the level of the C ⇤ 1
employer.

15


---
Appendix Table C1. Pirate Agreement Adoptions: Descriptive Statistics of Firms
Full sample

Firm size
Firm age
Share of full-time
Share of temporary
Share of females
Share of blue collar
Share of white collar
Share of apprentice
Share of mid-managers
Share of managers
Mean worker age
Log weekly wage
Log assets
Log productivity
Leverage
N. Observations

(1)
Treated
28.18
(370.35)
10.39
(11.6)
0.53
(0.42)
0.19
(0.32)
0.55
(0.40)
0.47
(0.45)
0.44
(0.45)
0.07
(0.22)
0.006
(0.05)
.006
(0.06)
37.4
(8.3)
5.84
(0.40)
6.21
(1.85)
3.32
(1.01)
0.83
(0.30)
14,128

(2)
Controls
8.13
(143.45)
13.07
(12.2)
0.60
(0.43)
0.15
(0.29)
0.47
(0.42)
0.58
(0.43)
0.31
(0.41)
0.10
(0.25)
0.005
(0.05)
.002
(0.03)
37.8
(9.0)
5.85
(0.38)
6.50
(1.62)
3.52
(.87)
0.81
(0.33)
13,930,620

Matched sample
(3)
Treated
118.61
(865.14)
14.19
(11.54)
0.66
(0.34)
0.18
(0.24)
0.49
(0.33)
0.49
(0.40)
0.44
(0.38)
0.06
(0.13)
0.01
(0.05)
.005
(0.03)
38.6
(5.6)
5.92
(0.32)
6.94
(1.78)
3.37
(.82)
0.80
(0.27)
2,144

(4)
Controls
29.92
(156.48)
14.60
(11.32)
0.68
(0.34)
0.16
(0.24)
0.48
(0.36)
0.49
(0.39)
0.42
(0.38)
0.05
(0.14)
0.01
(0.03)
.004
(0.03)
38.5
(5.8)
5.92
(0.32)
6.64
(1.52)
3.36
(.82)
0.81
(0.28)
2,144

Notes: This table reports descriptive statistics averaged between 2008 and 2016 by group.
Columns (1) and (2) refer to the firm sample before the matching. In particular, Column (1)
reports C ⇤ 1 descriptives for firms that will transition to a pirate CBA at C ⇤ ; Column (2) reports
descriptives for potential control firms, that is, firms that have never used a pirate CBA. Columns
(3) and (4) show descriptives for the matched sample, obtained as described in Appendix C.
Standard deviations are reported in parentheses. Log weekly wages and assets are expressed
in log euros. Productivity is computed as value added per worker. Leverage is computed as
1-equity/assets (for pirate firms, it is computed in the year before the adoption of the pirate
CBA). Firm age is measured in years.

16


---
Appendix Table C2. The Eﬀects of Pirate Agreement Adoptions on Firms

On Impact (C ⇤ )
Medium Run (C ⇤ + 2)
Long Run (C ⇤ + 5)
N. Observations
Mean outcome
Average of Pre-Event Coeﬀs
p-value Pre-Event Coeﬀs = 0

(1)
Log Weekly
Wages
-0.0311
(0.0050)***
-0.0283
(0.0063)***
-0.0332
(0.0078)***

(2)
Survival
Probability
0.0289
(0.0036)***
0.0247
(0.0100)**
-0.0058
(0.0150)

(3)
Log Firm
Size
0.0739
(0.125)***
0.0338
(0.0198)*
0.0427
(0.0276)

(4)
Share of
New Hires
0.0586
(0.0070)***
-0.0019
(0.0073)
-0.0038
(0.0085)

(5)
Log Weekly
Wages New Hires
-0.0698
(0.0289)**
-0.0669
(0.0317)**
-0.0711
(0.0371)*

39,938
5.99753
0.0047
(0.0049)
0.3262

44,216
0.9423
-0.0096
(0.0053)*
0.0668

39,938
2.2820
-0.0381
(0.0146)***
0.0090

39,938
0.2251
0.0078
(0.0067)
0.2436

6,926
5.7137
-0.0188
(0.0218)
0.3890

Notes: This table reports three event-study coeﬃcients from Equation (C1) estimated on the matched sample defined
in Appendix C. ‘On Impact’ denotes the coeﬃcient estimated in the opt-out year C ⇤ , ‘Medium Run’ corresponds to
the coeﬃcient two years after the opt-out, and ‘Long Run’ refers to the coeﬃcient five years after the opt-out. ‘Mean
Outcome’ represents the mean of the outcome of interest in the five years before the opt-out, computed considering the
control group only. The last rows show the mean event-study coeﬃcient in the five years before the opt-out (‘Average of
Pre-Event Coeﬀs’), the standard error in parentheses, and the p-value of the test that the mean pre-event coeﬃcient is
equal to zero, all computed using the lincom command in Stata. Log weekly wages is the mean log weekly wage paid by
firm 9 to its workers, expressed in euros; Survival probability is a year-to-year binary indicator taking value of 1 if firm
9 is observed in the data; Log firm size is the logarithm of the total number of the firm’s employees; Share of new hires
is the number of new hires in firm 9 scaled by total firm employment each period; Log weekly wages of new hires is the
mean log weekly wage paid by firm 9 to its newly hired employees, regardless of whether they are hired under a pirate
CBA or not. Standard errors, clustered at the firm level, are shown in parentheses. * p<0.10, ** p<0.05, *** p<0.01.

17


---
Appendix Figure C1. The Share of Workers under Pirate Agreements around the Opt-Out Event

Notes: This figure displays the event-study coeﬃcients from Equation (C1) estimated on the matched sample defined
in Appendix C. The outcome variable is the number of employees subject to a pirate agreement scaled by total firm
employment. Standard errors are clustered at the firm level.

18


---
Appendix Figure C2. The Eﬀects of Pirate Agreement Adoptions on Firms: Heterogeneity by
Geography
(a) Log Weekly Wages

(b) Survival Probability

(c) Log Firm Size

(d) Log Firm Size (De-trended)

Notes: This figure displays the event-study coeﬃcients from Equation (C1) estimated on the matched sample defined in
Appendix C. The regressions are run separately for firms in the Center-North and South of Italy at time C ⇤ 1. Southern
regions are Abruzzo, Basilicata, Calabria, Campania, Molise, Apulia, Sardinia and Sicily. Panel (a): Log weekly wages
is the mean log weekly wage paid by firm 9 to its workers, expressed in euros; Panel (b): the outcome is a year-to-year
binary indicator taking value of 1 if firm 9 is observed in the data; Panel (c): the outcome is the logarithm of the total
number of the firm’s employees; Panel (d) reproduces the coeﬃcients of Panel (c) after subtracting their linear time
trend estimated in the pre-event periods and extrapolated for the later years as in Dustmann et al. (2022). Standard
errors are clustered at the firm level.

19


---

