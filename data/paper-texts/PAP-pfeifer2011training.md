# Effects of Training on Employee Suggestions and Promotions in an Internal Labor Market

**Authors:** Pfeifer, Christian and Janssen, Simon and Yang, Philip and Backes-Gellner, Uschi
**Year:** 2011

---

SERIES
PAPER
DISCUSSION

IZA DP No. 5671

Effects of Training on Employee Suggestions and
Promotions in an Internal Labor Market
Christian Pfeifer
Simon Janssen
Philip Yang
Uschi Backes-Gellner
April 2011

Forschungsinstitut
zur Zukunft der Arbeit
Institute for the Study
of Labor

Effects of Training on Employee
Suggestions and Promotions in an
Internal Labor Market
Christian Pfeifer
Leuphana University Lüneburg
and IZA

Simon Janssen
University of Zurich

Philip Yang
Leibniz University Hannover

Uschi Backes-Gellner
University of Zurich

Discussion Paper No. 5671
April 2011

IZA
P.O. Box 7240
53072 Bonn
Germany
Phone: +49-228-3894-0
Fax: +49-228-3894-180
E-mail: iza@iza.org

Any opinions expressed here are those of the author(s) and not those of IZA. Research published in
this series may include views on policy, but the institute itself takes no institutional policy positions.
The Institute for the Study of Labor (IZA) in Bonn is a local and virtual international research center
and a place of communication between science, politics and business. IZA is an independent nonprofit
organization supported by Deutsche Post Foundation. The center is associated with the University of
Bonn and offers a stimulating research environment through its international network, workshops and
conferences, data service, project support, research visits and doctoral program. IZA engages in (i)
original and internationally competitive research in all fields of labor economics, (ii) development of
policy concepts, and (iii) dissemination of research results and concepts to the interested public.
IZA Discussion Papers often represent preliminary work and are circulated to encourage discussion.
Citation of such a paper should account for its provisional character. A revised version may be
available directly from the author.

IZA Discussion Paper No. 5671
April 2011

ABSTRACT
Effects of Training on Employee Suggestions and
Promotions in an Internal Labor Market*
We evaluate the effects of employer-provided formal training on employee suggestions for
productivity improvements and on promotions among male blue-collar workers. More than
twenty years of personnel data of four entry cohorts in a German company allow us to
address issues such as unobserved heterogeneity and the length of potential training effects.
Our main finding is that workers have larger probabilities to make suggestions and to be
promoted after they have received formal training. The effect on suggestions is however only
short term. Promotion probabilities are largest directly after training but also seem to be
affected in the long term.

JEL Classification:
Keywords:

J24, M53

human capital, insider econometrics, productivity, promotions, training

Corresponding author:
Christian Pfeifer
Leuphana University Lüneburg
Scharnhorststr. 1
C4.220b
21335 Lüneburg
Germany
E-mail: christian.pfeifer@uni.leuphana.de

*

This work was financially supported by the VolkswagenStiftung. We thank seminar participants at
Leuphana University Lüneburg, University Paderborn, and 14th Colloquium in Personnel Economics in
Zurich for their comments.

1. Introduction
Returns on human capital investments have received large attention in policy and
research over recent decades (e.g., Bartel, 1995; Bishop, 1997; Bartel, 2000; Asplund,
2005; Frazis and Loewenstein, 2005). Next to schooling, human capital accumulation
after entry into the labor market is considered key to economic performance at both the
micro and the macro level. Research however faces some problems when studying the
impact of employer-provided formal training on workers’ productivity. Problems
include the aggregation of heterogeneous training types across industries and firms as
well as the lack of adequate variables to proxy productivity. For example, survey data of
workers compare individuals across firms with different training programs and often use
workers’ wage increases as a proxy for productivity increases. Whereas wages might
indeed be good proxies for productivity in perfect labor markets, they are obviously not
so in imperfect labor markets. Survey data of firms, on the other hand, comprise only
information about aggregated productivity (e.g., sales), which allows a comparison
between firms but not between workers. Moreover, survey data often suffer from
imprecise or even false statements about wages, training, and other variables. To
overcome some of these problems, researchers have recently used personnel records of
single firms. Although personnel data sets are not representative and are only
econometric case studies ('insider econometrics'), they have the advantage of comparing
workers in the same environment (firm, job, training) and of unbiased information about
wages, productivity, and training.
Another potential problem when evaluating causal effects of training is that training
participation is likely to be non-random. Thus, if participation depends on unobservable
characteristics, a cross-section comparison between workers who participate in training
1

and workers who do not participate is likely to suffer from omitted variable or selection
bias. Panel data that exploit within variances can help to deal with this problem, because
first differences or conventional fixed effects estimators address the issue of unobserved
heterogeneity. More precisely, outcomes such as wages or productivity of a specific
worker are compared before and after training. A number of empirical studies have
recently used longitudinal data to close the research gap, but most attempts still suffer
from measurement and aggregation biases in survey data. Moreover, few datasets
provide sufficient long panels to be able to exploit the time dimension in more detail.
But the length of training effects in particular is important to get an understanding of
actual depreciation rates of human capital investments, which are largely unexplored.
In this paper, we evaluate the causal effects of training at the lowest micro level by
using personnel records from one German company. The data allows us to follow 415
male blue-collar workers, who entered the company during the late 1970s, over the
majority of their working life, i.e., for more than twenty years. In addition to
information about participation in formal training courses, our data set provides unique
information about employee suggestions that are of productive value for the firm.
Although we cannot calculate returns on investments (ROI) due to missing information
about training costs, actual benefits and costs of the implementation of suggestions, we
think that the analysis of training effects on the probability to make suggestions is still
important. First, employee suggestions have not been used previously to study training
effects and are an interesting alternative to the often used supervisors’ performance
ratings in personnel data, which might suffer from subjectivity bias. Second, employee
suggestions are important for firms to permanently improve the efficiency of their
production processes. Although training and suggestion systems are often idiosyncratic

2

to firms, the question as to whether training increases the probability of making
suggestions for productivity improvements is of a general nature.
We further analyze training effects on promotions, which are defined as upward
movement from one wage group to another and are hence associated with a wage
increase. Promotions are important from the point of view of both employer and
employee. Employees benefit from promotions by monetary gains and higher
reputation, whereas employers can use promotions to make efficient job assignments.
On the one hand, training can serve as a screening device without increasing individual
productivity, i.e., the firm learns about abilities and skills of workers and can promote
the best fitting (most productive) worker to the next job in the hierarchy. On the other
hand, training might indeed increase individual productivity by teaching skills and
knowledge that are important to fulfill tasks at higher job levels.
In order to estimate the causal effects of formal training on the likelihood of workers
making suggestions and getting promotions, we use individual fixed effects linear
probability and logit models. Our fixed effects approach helps to mitigate problems
stemming from unobserved heterogeneity and non-random training participation. We
further exploit the length of the panel by constructing four lagged training variables that
allow us to analyze the length of training effects. Thus, we are able to identify whether
the effects of training on productivity and promotions are short term or long term. The
main findings of our econometric case study are that past training participation has
significant positive effects on present suggestion and promotion probabilities. Training
has the largest impact on suggestion and promotion probabilities in the year directly
after participation. The further in the past the training participation has been, the more
the training effect decreases in size and significance. This finding emphasizes the
3

importance on the provision of employer-provided training throughout working life and
not only in the early years of employment.
This paper is structured as follows. The next section summarizes previous empirical
findings on the effects of employer-provided training. Section 3 informs about the
personnel data set, provides descriptive statistics, and discusses the econometric
framework. Section 4 presents the estimation results. The paper concludes with a short
summary and a discussion of the results in Section 5.

2. Literature Review
Following the pioneering contributions by Becker (1962) and Mincer (1974), a
substantial body of economic literature on human capital investments has addressed the
determinants1 and outcomes of training. A reason for the continuously growing number
of empirical studies on the outcomes of training is rooted in recent advancements in
overcoming methodological challenges and new data when trying to identify a causal
effect of training participation.
The methodological problem in the attempt to evaluate training effects is based upon the
potential endogeneity of the training variable. One source of this endogeneity stems
from the concern about selection bias. Training participation is expected to be unevenly
distributed across workers with different abilities. Workers and firms are likely to select
those workers for training, for whom the expected returns are most favorable (Leuven
and Oosterbeek, 2002). Endogeneity of the training variable might lead to omitted
variable bias. If training represents one of many determinants of wages and

4

productivity, the training effects could be over- or underestimated (Barron et al., 1989).
To correct for endogeneity, recent empirical training literature mainly draws on
methodological approaches such as a Heckman-type selection (Lynch, 1992; Veum,
1995), instrumental variables (Leuven and Oosterbeek, 2002), or fixed effects
estimation (Booth, 1993; Barron et al., 1999).
Despite the improved methodological approaches to correct for endogeneity, data
availability still represents a major problem for three main reasons. First, few studies
find instruments which arguably affect training, yet not the outcome variable (Leuven
and Oosterbeek, 2004). Second, most panel data sets are relatively short so that either
variation is low or training cases are rare (Dearden et al., 2006). Short panels also do not
allow inference about the length of training effects through the use of lagged variables
(Frazis and Loewenstein, 2005). Third, despite increased efforts to find adequate
measurements of training participation, few studies obtain distinct outcome variables,
which unambiguously denote promotions in hierarchy and productivity on the
individual level (Bartel, 2000).
Most empirical studies on training outcomes have addressed the wage effects of training
participation (Bishop, 1997; Bartel, 2000; Asplund, 2005). The investigation of the
effects of training on workers’ promotions in hierarchies and on productivity has not
received as much attention. The main explanation is that wages, according to traditional
human capital theory, serve as an adequate proxy for hierarchy and productivity. In
perfect labor markets, wages are equal to the value of marginal products of workers
(Becker, 1962). Accordingly, promotions serve as recognitions of workers’ increased
productivities (Frazis and Loewenstein, 2005). However, in imperfect labor markets,
employers are able to pay employees below their marginal product (Acemoglu and
5

Pischke, 1998). Increased wages from training participation would then fail to proxy the
enhanced productivity of workers. Also, several empirical studies find significant
variations of wages within job levels (Baker et al., 1994a, 1994b; Lazear and Oyer,
2007). Hence, a wage increase is not necessarily associated with more responsibility at
work or a shift to higher job levels. For this reason, recent empirical literature
emphasizes the need to distinguish between wages, promotions, and productivity
(Asplund, 2005).
Frazis and Loewenstein (2005) use survey data of the National Longitudinal Study of
Youth and the Employer Opportunity Pilot Project to evaluate the effect of training on
subsequent promotions. Promotions are self-reported by workers and indicate if they
have received a promotion in hierarchy or whether their job responsibilities have
increased. The authors estimate fixed effects regressions and find positive effects of
current and past training participation on promotion probabilities. Surveys entail,
however, subjective responses of individuals, which are likely to be subject to
measurement errors (Bartel, 1995). Furthermore, the training variable underlies
significant heterogeneity so that questions remain as to how adequate the aggregation of
different training types is, despite the effort to enhance the informational value of
training measures through the observation of hours spent on training spells.
Krueger and Rouse (1998) examine the impact of workplace education programs for
one blue-collar and one white-collar company. They limit training heterogeneity by
observing one standardized type of training form, which is partially governmentally
financed and undertaken at the local community college between 1991 and 1995. By
estimating an ordered probit model, the authors find that trained workers are much more
likely to make job bids and to receive job upgrades in comparison to untrained workers.
6

Yet, the results suffer from a relatively low number of observations and insufficient
panel length. Instead of using econometric approaches to limit selection bias, they have
to assume that selection is controlled for by sufficient information on observed
characteristics.
Most empirical studies on training effects on productivity use industry data or matched
employer–employee data (Bartel, 2000). This slowly growing branch of literature
typically makes use of the standard Cobb–Douglas production function and observes
firms over several years.2 In general, most of these studies find positive effects of the
share of trained workers on labor productivity, which diminishes with the inclusion of
human resource management characteristics. Few empirical studies have, however,
looked at productivity effects of training participation at the individual worker level.
Pischke (2001) uses data from the German Socio Economic Panel from 1986 to 1989.
He observes detailed information on workers’ participation in formal training programs.
As a training outcome, the author makes use of workers’ responses on benefits from
training participation. He finds support for a positive effect of formal training on selfreported performances of workers and interprets this finding as increased productivity.
Despite the comprehensive design of the training variable, his results are questionable
with respect to the implication for productivity.
Bartel (1995) recommends the use of data from personnel records of a single firm
(econometric case study) for three main reasons. First, personnel records provide exact
training time and type. Second, training of workers is done by the same firm,
corresponding to more homogeneous training measures. Third, workers’ outcomes are
more comparable if they work for the same firm. Bartel (1995) uses personnel records

7

from a large manufacturing company from 1986 to 1990. To determine the effect of
training on productivity, she uses information on performance evaluations by
supervisors. Formal training has a positive and significant effect on the performance
evaluations of workers, from which she draws the conclusion that formal training has a
productivity-increasing effect. The short panel does not, however, allow any
implications on the length of training effects, and supervisors’ performance ratings
might suffer from potential biases such as subjectivity. A recent study by Breuer and
Kampkötter (2010) uses three years of personnel records from a German multinational
company and fixed effects methods. The main finding is that training only has a positive
effect on several performance-related outcomes in the same year that training
participation takes place. The research design might however suffer from the short panel
length.
In sum, the potential endogeneity of the training variable demands sophisticated
econometric methods in order to determine the causal effects of training participation on
distinct outcomes such as wages, promotions, and productivity. Although several
approaches to estimate causal effects exist, data availability represents a major problem.
Panels are usually rather short so that the variation of training and outcomes is low.
Furthermore, few data sets offer persuasive information with regard to training and
outcome variables. The training variable in survey data is usually aggregated through
heterogeneous training types across firms and industries. As training outcomes, most
empirical papers use wages to proxy hierarchy or productivity, and those which actually
observe hierarchy and productivity rely on either heterogeneous outcomes or subjective
evaluations. We complement existing studies by using an insider econometric approach
with long balanced panel data for one firm, which comprise unique information about

8

training and outcomes such as employee suggestions and promotions. The data set
allows us to apply fixed effects estimation techniques with lagged training variables to
make inference about the length of training effects.

3. Personnel Data, Variables, and Econometric Method
We analyze the personnel records of a large company from the energy sector located in
Western Germany. The company is subject to a collective contract and has a works
council. Due to data protection reasons we are neither allowed to name the company nor
to give detailed information. The data comprise yearly information about a subsample
of 438 blue-collar workers in the company’s mining business, who entered the firm in
four subsequent cohorts from 1976 until 1979 and stayed in the company over the entire
observation period up to the year 2002. The sample represents a share of about a quarter
of all employees in the company’s operation unit and 3.5 percent of the company’s
entire workforce.
For our analysis, we restrict the sample to German male blue-collar workers without
missing values in the used variables. This restriction reduces our sample by 5 percent to
415 different workers. As we are interested in the long term effects of training, we use
four lags of training participation so that the first four yearly observations of every
worker are dropped from the estimation sample. Moreover, all observations from the
last observation year 2002 are dropped from the estimation sample, because no
promotion variable can be constructed. The final sample contains 8,469 yearly
observations of 415 different workers.3 Nearly 20 percent of these blue-collar workers
do not have any secondary school degree, about 72 percent have the lowest secondary

9

school degree (Volks-/Hauptschulabschluss), and about 8 percent have at least
successfully completed medium secondary school (Realschule). We further know that
about a quarter of these workers have no apprenticeship qualification, about a quarter
have completed their apprenticeship in the analyzed company, and the remaining 50
percent have performed their apprenticeship in other firms.
Formal employer-provided training in the company is divided in four different types:
(1) short training course (kurze Schulung) (one or two days); (2) longer training course
(längere Schulung) (up to several weeks); (3) longer vocational re-training (längere
Umschulung) (up to several weeks); and (4) longer academy of vocational training
(Berufsakademie) (up to several weeks). We observe a total of 626 training cases. More
than two thirds are short training courses, whereas the other training types are nearly
equally distributed. Due to the rather small number of cases in most training types, we
use a binary variable that takes the value one if a worker participated in any kind of
training. To reduce heterogeneity in the training courses, we also analyze the effects of
short training courses separately. Unfortunately, we do not have information about the
direct and indirect costs of these training courses or about their actual contents. We
know however that workers are paid during the training period and do not have to cover
any direct costs. Thus, all costs are covered by the employer.
In order to evaluate the effects of formal training in the company, we use two outcome
variables. The first outcome is a binary variable that indicates if a worker makes a
suggestion. These suggestions are of productive value for the firm and workers receive
monetary rewards for them. Unfortunately, we do not know more about the value of the
suggestions and of potential implementation costs. As we analyze blue-collar workers in
the mining business, it seems likely that most suggestions are about more efficient work
10

arrangements. Formal training courses might teach new aspects in work arrangements or
stimulate thoughts about the current work arrangements so that workers might have
larger probabilities to make suggestions after such training. We observe 356 suggestions
by workers, which results in a yearly average of about 4 percent. The second outcome
variable to assess the training effects is a binary variable that indicates if a worker gets
promoted from one wage group in a given year (t) to a higher wage group in the
subsequent year (t+1). The underlying wage groups are obtained from the collective
contract and promotions are by definition associated with a significant wage increase,
which might be explained by a productivity increase due to training. We observe 511
promotions, which results in a yearly average of about 6 percent.
Since we have introduced our main variables, we can turn to our econometric
framework that is described in equation (1). In principal, we estimate the impact of
lagged training participation T of worker i on his outcomes Y in year t, which are worker
suggestions and promotions. We further include a set of time variant control variables X
(age in years, squared age divided by 100, wage groups as continuous variable), time
fixed effects t , and worker fixed effects  i .  it is the usual error term. The parameters
to be estimated are denoted with β and δ. Descriptive statistics of the variables are
presented in Table 1.

Yit  1Ti ,t 1   2Ti ,t  2   3Ti ,t 3   4Ti ,t  4   X it  t  i   it
-

(1)

insert Table 1 about here

The coefficients of interest are the βs, which are the effects of formal employerprovided training on the probability that a worker makes a suggestion or gets promoted.
Using the lags of training participation has the advantage of estimating the correct
11

causal direction, because past training participation has to affect current outcomes.
Moreover, a comparison of the βs allows inference about the length of training effects.
The inclusion of time and worker fixed effects reduces efficiency of the estimates but
makes it more likely that estimates of the βs are consistent because omitted variable
biases are reduced. Since worker fixed effects are jointly significant in all estimated
specifications and Hausman tests reject the null hypothesis of no systematic differences
with random effects estimates, we choose to use only fixed effects models. Because of
potential problems in fixed effects probit and logit models, we prefer to estimate fixed
effects linear probability models (LPM) using ordinary least squares. As a robustness
check, a fixed effects (conditional) logit model is applied, which supports the findings
from the linear models. According to Angrist (2001) linear models can be appropriate
even for limited dependent variables if the main objective is to estimate causal effects
and not structural parameters.
In order to provide consistent effects for the βs, the Ti,t 1 to Ti,t 4 must be strictly
exogenously conditional on our variables in X it and the unobserved effects  i , i.e., Ti,t 1
to Ti,t 4 must be uncorrelated not only with  it but also with  i,t 1 and  i,t 1. In our case,
one might argue that the firm selects a worker for training because the worker made a
particularly good suggestion in the former period, which signals his ability to the
employer. If this were the case, Ti,t 1 to Ti,t 4 should be correlated with  i,t 1 and,
consequently, our estimates of β would not be consistent. Therefore, we carried out a
test of strict exogeneity proposed by Wooldridge (2002, p. 285). The test is performed
by incorporating Ti,t 1 into regression equation (1). Under strict exogeneity, the
coefficient of Ti,t 1 should not be significantly different from zero. As we cannot find a

12

significant effect of Ti,t 1 in any of our specifications, we are confident that the
assumption of strict exogeneity is fulfilled in our fixed effects regressions.

4. Estimation Results
The estimation results for the probability of employee suggestions are presented in
Table 2. The first four specifications are estimated using fixed effects linear regressions
(LPM) for the complete sample. Specification one includes only the first lagged training
participation variable and no time fixed effects (year dummies). The predicted
probability to make a suggestion for an average worker without training is about 4
percent and for an average worker, who has received training during the last year, it is
about 6.6 percent. The absolute marginal effect of 2.6 percentage points is of statistical
significance (p=0.011) and of economic importance (relative marginal effect is 2.6/4=65
percent). Specification two includes additional time fixed effects, which are jointly
significant in an F-test. The estimated training effect is only slightly reduced to 2.4
percentage points. Specification three includes the complete four lags of training
participation and no time fixed effects, and specification four also includes the time
fixed effects. It can be seen that the marginal effect of the first lag is slightly reduced to
2.4 and 2.2 percentage points but is still highly significant. The other three lags, i.e.,
training participation at least two years ago, have no significant effect on the suggestion
probability.
-

insert Table 2 about here

13

The last column in Table 2 includes a robustness check concerning the method and
sample. A fixed effects (conditional) logit model for the complete specification (all lags
of training and time fixed effects) is estimated on a subsample of workers who have
actually made a suggestion in the observation period. The estimated coefficients support
the findings from the linear estimates that only the first training lag has a significant
effect. A noteworthy result of the estimates in Table 2 is the inverted u-shape effect of
age on the suggestion probability, which has its maximum around the ages 35 to 40
years. If suggestions are related to productivity, this finding is consistent with concave
productivity-age profiles known from other studies. In combination with the result that
the training effect on suggestions as proxy for productivity is only short term, one might
conclude that it is important for the employability of aging workers to invest more in
their human capital.
Table 3 informs about the estimation results for the probability that a worker gets
promoted, which is associated with a significant wage increase. Specification one (first
lag, no time fixed effects) reveals an absolute marginal effect of 7.7 percentage points
due to training in the last year, which is highly significant. An average worker without
training has a predicted promotion probability of 5.5 percent, whereas an average
worker with training has a predicted promotion probability of 13.2 percent. The
estimated training effect is with 8.25 percentage points even larger, if time fixed effects
are included in specification two. Specifications three and four include all four lags of
training participation. The estimated effects for the first training lag do not change
significantly. Furthermore, the effect of the second lag is not significant, whereas the
effects of the third and fourth lags are significant again. The third lag has a marginal
effect of about 4 percentage points and the fourth lag of about 3 percentage points. But

14

if these effects are compared with the effect of the first lag, it emerges that they have
only half the size. The last column in Table 3 includes again a fixed effects (conditional)
logit model for the complete specification (all lags of training and time fixed effects),
which is estimated on a subsample of workers who have actually been promoted in the
observation period. The estimated coefficients support the findings from the linear
regressions. We further find in all specifications that workers at higher wage groups are
less likely to be promoted.
-

insert Table 3 about here

One might argue that suggestions and promotions are related to each other. For
example, supervisors might be more likely to choose a worker for promotion who has
recently made a suggestion. Therefore, the linear estimates for the complete
specification (all lags of training and time fixed effects) have been repeated with
additional control variables that include four lags of promotions in the suggestion
regression and vice versa. Because these variables have no significant effects and the
results already presented in Tables 2 and 3 virtually do not change, the estimation
results of this robustness check are only presented in the Appendix (see Table A.1).
In a next step, we concentrate on short training courses to further reduce heterogeneity
in the training variable. Short training courses are one or two day courses and make up
about two thirds of all observed training cases in the data. For suggestion and promotion
probabilities, we estimate fixed effects linear models for the complete sample as well as
fixed effects logit models for subsamples of workers actually making a suggestion or
being promoted in the observation period. The results are presented in Table 4 and are
in general consistent with our previous findings on aggregated training. But two

15

noteworthy differences arise. First, the effect of short training on suggestions is larger
and significant for the last two years. Second, the effect of short training on promotions
is smaller. These differences between short training and aggregated training might be
explained by different course contents and aims. Short training courses are likely to be
more concerned with improvements of current work arrangements and less with
teaching completely new skills (e.g., re-training), which might however be important to
obtain better paid jobs in the firm’s hierarchy. Consequently, career-orientated longer
training courses might indeed be more attractive for younger workers. On the other
hand, short training courses, which seem to have only short term effects on productivity,
are still important for older workers (skill updating, employability) and justified from an
economic perspective because shorter amortization periods of old workers should play a
minor role if depreciation rates are that large.
-

insert Table 4 about here

5. Conclusion
In this paper, we have used unique personnel records of a German company to evaluate
the effects of formal employer-provided training on employee suggestions and
promotions. Following this ‘insider econometric approach’, we could address issues
such as training course heterogeneity and unobserved worker heterogeneity. We have
found significant positive but only short term effects of training on the probability to
make suggestions, which indicate a high depreciation rate in this dimension. Moreover,
we have found that training participation increases the promotion probability. Overall,
the results are consistent with the human capital argument that training increases

16

workers’ productivities. The rather short term effect raises, however, the question of
whether depreciation rates are larger than previously assumed and ROIs smaller than
often computed. If this were the case, the often stated argument that old workers receive
no training due to short amortization periods would not be that convincing anymore.
Because we have used only a sample of blue-collar workers in one single firm and
qualitative information about employee suggestions and promotions in an econometric
case study, we cannot give concluding answers to this question. But we hope for more
studies to come that use long panels of personnel data.

17

1

For literature reviews on the determinants of training participation see Becker (1993), Leuven and

Oosterbeek (1999), Neumark and Washer (2001), Leuven (2004), and Metcalf (2004).
2

Empirical literature on the plant level uses mainly survey data of firms in the United States (Black and

Lynch, 1996; Black and Lynch, 2001), UK (Dearden et al., 2006), Italy (Conti, 2005), Germany (Zwick,
2002), and Ireland (Barrett and O’Connell, 2001).
3

The number of workers is n=105 for the entry cohort 1976. The observations included in the estimation

sample for entry cohort 1976 ranges from 1980 to 2001, which leads to a panel length in years of T=22.
For entry cohort 1977: n=96, T=21. For entry cohort 1978: n=77, T=20. For entry cohort 1979: n=137,
T=19.

18

References
Acemoglu, D., and Pischke, J.-S. (1998), Why do firms train? Theory and evidence. Quarterly Journal of
Economics 113, 79-119.
Angrist, J. D. (2001), Estimation of limited dependent variable models with dummy endogenous
regressors: Simple strategies for empirical practice. Journal of Business and Economic Statistics
19(1), 2-16.
Asplund, R. (2005), The Provision and Effects of Company Training: A Brief Review of the Literature.
Nordic Journal of Political Economy 31, 47-73.
Baker, G., Gibbs, M., and Holmstrom, B. (1994a), The Internal Economics of the Firm: Evidence from
Personnel Data. Quarterly Journal of Economics 109(4), 881-920.
Baker, G., Gibbs, M., and Holmstrom, B. (1994b), The Wage Policy of a Firm. Quarterly Journal of
Economics 109(4), 921-956.
Barrett, A., and O’Connell, P. J. (2001), Does Training Generally Work? The Return to In-Company
Training. Industrial and Labor Relations Review 54(3), 647-662.
Barron, J. M., Berger, M. C., and Black, D. A. (1999), Do Workers Pay for On-The-Job Training. Journal
of Human Resources 34(2), 235-252.
Bartel, A. P. (1995), Training, wage growth, and job performance: Evidence from a company database.
Journal of Labor Economics 13, 401-425.
Bartel, A. P. (2000), Measuring the Employer’s Return on Investments in Training: Evidence from
Literature. Industrial Relations 39(3), 502-524.
Becker, G. S. (1962), Investments in human capital: a theoretical analysis. Journal of Political Economy
7(5), 9-49.
Becker, G. S. (1993), Human Capital: A Theoretical and Empirical Analysis with a Special Reference to
Education. University Chicago Press, Chicago.
Bishop, J. H. (1997), What we know about employer-provided training: a review of the literature. In
Polachek, S. W. (ed.). Research in Labor Economics 16, pp. 19-87.

19

Black, S., and Lynch, E. (1996), Human–Capital Investments and Productivity. American Economic
Review, Paper and Proceedings 86(2), 263-267.
Black, S., and Lynch, E. (2001), How to compete: The impact of workplace Practices and Information
technology on Productivity. Review of Economics and Statistics 83(3), 434-445.
Booth, A. L. (1993), Private Sector Training and Graduate Earnings. Review of Economics and Statistics
75(1), 164-170.
Breuer, K., and Kampkötter, P. (2010), The effects of intra-firm training on earnings and job performance
- evidence from a large German company. Paper presented at EALE/SOLE Meeting 2010.
Conti, G. (2005), Training, productivity and wages in Italy. Labour Economics 12(4), 557-576.
Dearden, L., Reed, H., Van Reenen, J. (2006), The Impact of Training on Productivity and Wages:
Evidence from British Panel Data. Oxford Bulletin of Economics and Statistics 68(4), 397-421.
Frazis, H., and Loewenstein, M. (2005), Reexamining the returns to training: Functional form, magnitude,
and interpretation. Journal of Human Resources 40(2), 453-476.
Krueger, A., and Rouse, C. (1998), The Effect of Workplace Education on Earnings, Turnover, and Job
Performance. Journal of Labor Economics 16(1), 61-94.
Lazear, E., and Oyer, P. (2007), Personnel Economics, Forthcoming in R. Gibbons and J. Roberts (eds.).
Handbook of Organizational Economics.
Leuven, E. (2004), A Review of the Wage Returns to Private Sector Training. Paper presented at the
EC_OECD Seminar in Human Capital and Labour Market Performance: Evidence and Policy
Challenges. Brussels.
Leuven, E., and Oosterbeek, H. (2002), A New Approach to Estimate the Wage Returns to Work-Related
Training. IZA Discussion Paper No. 526.
Leuven, E., and Oosterbeek, H. (2004), Evaluating the Effect of Tax Deductions on Training. Journal of
Labor Economics 22(2), 461-488.
Leuven, E., and Oosterbeek, H. (1999), The demand and supply of work-related training: Evidence from
four countries. Research in Labor Economics 18, 303-330.

20

Lynch, L. M. (1992), Private-Sector Training and the Earnings of Young Workers. American Economic
Review 82(1), 299-312.
Metcalf, D. (2004), The impact of the national minimum wage on the pay distribution, employment and
training. Economic Journal 114(494), C84-C86.
Mincer, J. (1974), Schooling, Experience, and Earnings. Columbia University Press, New York.
Neumark, D., and Wascher, W. (2001), Minimum Wages and Training Revisited. Journal of Labor
Economics 19(3), 563-595.
Pischke, J. S. (2001), Continuous Training in Germany. Journal of Population Economics 14(3), 523-548.
Veum, J. R. (1995), Sources of Training and Their Impact on Wages. Industrial and Labor Relations
Review 48(4), 812-826.
Wooldridge J.M. (2002), Econometric analysis of cross section and panel data. Cambridge: MIT Press.
Zwick, T. (2002), Continuous Training and Firm Productivity in Germany. ZEW Discussion Paper No.
02-50.

21

Appendix
Table A.1: Trainings effects when controlling for promotion and suggestion

Training in t-1
Training in t-2
Training in t-3
Training in t-4
Age
Age squared / 100
Wage group
Promotion in t-1

(1) Suggestion

(2) Promotion

0.0221**

0.0826***

(0.0107)

(0.0150)

0.0102

0.0161

(0.0101)

(0.0133)

0.0010

0.0410***

(0.0088)

(0.0133)

-0.0037

0.0298**

(0.0082)

(0.0133)

0.0081**

-0.0003

(0.0033)

(0.0053)

-0.0114**

0.0063

(0.0049)

(0.0076)

-0.0014

-0.0391***

(0.0014)

(0.0030)

0.0009
(0.0092)

Promotion in t-2

0.0068
(0.0092)

Promotion in t-3

-0.0073
(0.0074)

Promotion in t-4

0.0029
(0.0076)

Suggestion in t-1

0.0129
(0.0154)

Suggestion in t-2

0.0162
(0.0162)

Suggestion in t-3

0.0041
(0.0158)

Suggestion in t-4

-0.0118
(0.0145)

Year fixed effects

Yes

Yes

Worker fixed effects

Yes

Yes

R²

0.1891

0.1143

F value

7.5492

9.6402

Number of observations

8469

8469

Number of workers
415
415
Notes: Coefficients of fixed effects linear probability model. Robust standard
errors in parentheses. *** p<0.01, ** p<0.05, * p<0.10.

22

Tables included in text
Table 1: Descriptive statistics
Mean

Std. dev.

Min.

Max.

Suggestion in t (dummy)

0.0420

0.2007

0

1

Promotion in t (dummy)

0.0603

0.2381

0

1

Training in t-1 (dummy)

0.0661

0.2485

0

1

Training in t-2 (dummy)

0.0653

0.2471

0

1

Training in t-3 (dummy)

0.0634

0.2437

0

1

Training in t-4 (dummy)

0.0582

0.2342

0

1

Short training in t-1 (dummy)

0.0433

0.2036

0

1

Short training in t-2 (dummy)

0.0413

0.1991

0

1

Short training in t-3 (dummy)

0.0367

0.1881

0

1

Short training in t-4 (dummy)

0.0314

0.1744

0

1

Age in t (years)

33.4290

6.5271

19

53

Age squared / 100

11.6010

4.4034

3.61

28.09

Wage group in t

7.0461

2.7482

2

19

Notes: Number of yearly observations is 8469 from 415 blue-collar workers.

23

Table 2: Effects of training on employee suggestions

Training in t-1

(1) LPM

(2) LPM

(3) LPM

(4) LPM

(5) Logit

0.0260**

0.0238**

0.0240**

0.0221**

0.4000*

(0.0102)

(0.0102)

(0.0105)

(0.0104)

(0.2310)

0.0098

0.0113

0.2354

(0.0098)

(0.0097)

(0.2448)

-0.0036

0.0002

-0.0245

(0.0086)

(0.0086)

(0.2750)

-0.0107

-0.0036

-0.1174

(0.0080)

(0.0079)

(0.3034)

Training in t-2
Training in t-3
Training in t-4
Age

0.0221***

0.0080**

0.0221***

0.0080**

0.2367

(0.0025)

(0.0033)

(0.0025)

(0.0033)

(0.2137)

-0.0282***

-0.0113**

-0.0282***

-0.0114**

-0.1575

(0.0037)

(0.0049)

(0.0037)

(0.0049)

(0.2777)

-0.0007

-0.0012

-0.0006

-0.0012

-0.0182

(0.0013)

(0.0013)

(0.0013)

(0.0013)

(0.0734)

Year fixed effects

No

Yes

No

Yes

Yes

Worker fixed effects

Yes

Yes

Yes

Yes

Yes

R²

0.1778

0.1888

0.1781

0.1889

F value

43.7426

9.6093

25.3282

8.5678

Age squared / 100
Wage group

Pseudo R² (McFadden)

0.1596

Chi² value

255.9914

Number of observations

8469

8469

8469

8469

2979

Number of workers
415
415
415
415
146
Notes: Mean yearly suggestion probability for an average worker without training is approximately 4
percent. Coefficients of fixed effects linear probability model for specifications (1) to (4) and fixed effects
(conditional) logit model for specification (5). Robust standard errors in parentheses. *** p<0.01, **
p<0.05, * p<0.10.

24

Table 3: Effects of training on promotions

Training in t-1

(1) LPM

(2) LPM

(3) LPM

(4) LPM

(5) Logit

0.0774***

0.0825***

0.0783***

0.0830***

0.9977***

(0.0148)

(0.0148)

(0.0150)

(0.0150)

(0.1535)

0.0124

0.0165

0.2420

(0.0133)

(0.0133)

(0.1805)

0.0390***

0.0415***

0.6637***

(0.0133)

(0.0133)

(0.1746)

0.0318**

0.0298**

0.4640**

(0.0132)

(0.0133)

(0.1881)

Training in t-2
Training in t-3
Training in t-4
Age

0.0009

0.0012

0.0019

-0.0001

-0.0640

(0.0042)

(0.0054)

(0.0042)

(0.0054)

(0.1031)

0.0020

0.0044

0.0004

0.0061

0.2671*

(0.0061)

(0.0076)

(0.0061)

(0.0076)

(0.1552)

-0.0383***

-0.0381***

-0.0393***

-0.0392***

-0.4447***

(0.0030)

(0.0030)

(0.0030)

(0.0030)

(0.0395)

Year fixed effects

No

Yes

No

Yes

Yes

Worker fixed effects

Yes

Yes

Yes

Yes

Yes

R²

0.1023

0.1109

0.1051

0.1139

F value

47.5890

11.7954

29.4158

11.0083

Age squared / 100
Wage group

Pseudo R² (McFadden)

0.1229

Chi² value

326.5321

Number of observations

8469

8469

8469

8469

5757

Number of workers
415
415
415
415
281
Notes: Mean yearly promotion probability for an average worker without training is approximately 5.5
percent. Coefficients of fixed effects linear probability model for specifications (1) to (4) and fixed effects
(conditional) logit model for specification (5). Robust standard errors in parentheses. *** p<0.01, **
p<0.05, * p<0.10.

25

Table 4: Effects of short training
Suggestion

Promotion

(1) LPM

(2) Logit

(3) LPM

(4) Logit

0.0375***

0.5419**

0.0299**

0.5092**

(0.0144)

(0.2556)

(0.0143)

(0.2409)

0.0325**

0.5304*

-0.0066

-0.3523

(0.0140)

(0.2722)

(0.0118)

(0.3074)

0.0051

-0.0009

0.0248*

0.4534*

(0.0121)

(0.3292)

(0.0147)

(0.2694)

0.0131

0.2874

0.0160

0.2497

(0.0122)

(0.3647)

(0.0163)

(0.2844)

0.0077**

0.2196

0.0010

-0.0218

(0.0033)

(0.2139)

(0.0054)

(0.1014)

-0.0112**

-0.1399

0.0045

0.1854

(0.0049)

(0.2780)

(0.0076)

(0.1527)

-0.0020

-0.0356

-0.0387***

-0.4161***

(0.0013)

(0.0733)

(0.0031)

(0.0378)

Year fixed effects

Yes

Yes

Yes

Yes

Worker fixed effects

Yes

Yes

Yes

Yes

R²

0.1904

0.1053

F value

8.7319

10.0131

Short training in t-1
Short training in t-2
Short training in t-3
Short training in t-4
Age
Age squared / 100
Wage group

Pseudo R² (McFadden)

0.1625

0.1017

Chi² value

260.6811

270.1058

Number of observations

8469

2979

8469

5757

Number of workers
415
146
415
281
Notes: Coefficients of fixed effects linear probability model for specifications (1) and (3) and fixed
effects (conditional) logit model for specifications (2) and (4). Robust standard errors in parentheses.
*** p<0.01, ** p<0.05, * p<0.10.

26

