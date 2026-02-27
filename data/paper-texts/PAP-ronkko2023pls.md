The current issue and full text archive of this journal is available on Emerald Insight at:
https://www.emerald.com/insight/0309-0566.htm
Marketing or methodology?
Exposing the fallacies of PLS
with simple demonstrations
Mikko Rönkkö
Jyväskylä University School of Business and Economics, University of Jyväskylä,
Jyväskylä, Finland
Nick Lee
Department of Marketing, Warwick Business School, Coventry, UK
Joerg Evermann
Faculty of Business Administration, Memorial University of Newfoundland,
St. John’s, Canada
Cameron McIntosh
Employment and Social Development Canada, Gatineau, Canada, and
John Antonakis
Department of Organizational Behavior, University of Lausanne,
Lausanne, Switzerland
Marketing or
methodology?
1597
Received 10 February 2021
Revised 4 June 2021
11 June 2021
21 June 2021
Accepted 28 February 2022
Abstract
Purpose– Over the past 20 years, partial least squares (PLS) has become a popular method
in marketing research. At the same time, several methodological studies have demonstrated
problems with the technique but have had little impact on its use in marketing research practice.
This study aims to present some of these criticisms in a reader-friendly way for non-
methodologists.
Design/methodology/approach– Key critiques of PLS are summarized and demonstrated using
existing data sets in easily replicated ways. Recommendations are made for assessing whether PLS is a useful
method for a given research problem.
Findings– PLS is fundamentally just a way of constructing scale scores for regression. PLS provides no
clear bene ts for marketing researchers and has disadvantages that are features of the original design and
cannot be solved within the PLS framework itself. Unweighted sums of item scores provide a more robust
way of creating scale scores.
Research limitations/implications– The ndings strongly suggest that researchers abandon the use
of PLS in typical marketing studies.
© Mikko Rönkkö, Nick Lee, Joerg Evermann, Cameron McIntosh and John Antonakis. Published by
Emerald Publishing Limited. This article is published under the Creative Commons Attribution (CC
BY 4.0) licence. Anyone may reproduce, distribute, translate and create derivative works of this
article (for both commercial and non-commercial purposes), subject to full attribution to the original
publication and authors. The full terms of this licence may be seen at http://creativecommons.org/
licences/by/4.0/legalcode
European Journal of Marketing
Vol. 57 No. 6, 2023
pp. 1597-1617
Emerald Publishing Limited
0309-0566
DOI 10.1108/EJM-02-2021-0099
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
EJM
57,6
1598
Practical implications– This paper provides concrete examples and techniques to practicing marketing
and social science researchers regarding how to incorporate composites into their work, and how to make
decisions regarding such.
Originality/value– This work presents a novel perspective on PLS critiques by showing
how researchers can use their own data to assess whether PLS (or another composite method) can
provide any advantage over simple sum scores. A composite equivalence index is introduced for
this purpose.
Keywords Partial least squares, Measurement, Composites, Structural equation models,
Model testing, Theory testing
Paper type Research paper
Most people use statistics like a drunk man uses a lamppost; more for support than illumination–
Andrew Lang, Scottish Novelist
Partial least squares (PLS) is an algorithm developed by Herman Wold in the 1960s and 1970s
(Wold, 1982) and was originally positioned as an alternative to the LISREL program (Jöreskog
and Wold, 1982, equations (4)–(8)). The main stated advantage at that time was that the“PLS
approach is easy and speedy on the computer” (Wold, 1982, p. 29), but this came with the trade-
off that PLS produces incorrect estimates of model parameters:“LISREL gives consistent
estimates of the structural parameters, whereas the corresponding PLS estimates are biased”
(Wold, 1982, p. 52). Given advances in computing power since Wold’s work, any advantage
PLS may hold in computational simplicity is moot. However, the disadvantages remain.
Despite early exposure in the marketing discipline (Fornell and Bookstein, 1982), PLS
remained a niche method until the early 2000s when its popularity began to increase. This
trend accelerated from around 2010 (Hair et al., 2014, Figure I.1; Rönkkö, 2014, Figure 1),
driven by advocacy papers with titles like“PLS-SEM: Indeed a Silver Bullet” (Hair et al.,
2011). At the same time, several critiques of PLS appeared (Goodhue et al., 2012; Rönkkö and
Evermann, 2013) but have had little impact on PLS’s use in marketing journals, for three
possible reasons. First, some critiques of PLS are in methodological journals (Rönkkö and
Evermann, 2013) that applied researchers may not follow. Indeed, a researcher following
only marketing journals might have read at least half-a-dozen advocacy papers but not a
single critical one. Second, there is a widespread belief that the critical arguments have been
refuted. For example, Ali et al. (2018) claim that“most of the criticism has been refuted as
inaccurate” (p. xi), whereas Ravand and Baghaei (2016) state that“Henseler et al. (2014) refuted
the critiques of Rönkkö and Evermann” (p. 3). It is dif cult to see what these conclusions are
based on because the evidence presented by Henseler et al. (2014) mostly supported Rönkkö
and Evermann’s (2013) arguments (McIntosh et al., 2014). Third, researchers may conclude that
because more papers champion than critique PLS, it must be valid. This is a logical fallacy
because the number of advocacy articles is not evidence of PLS’s usefulness; it simply shows
that the advocates are more proli c writers than the skeptics.
This article presents a few key methodological criticisms of PLS using simple examples that
any reader capable of using PLS can replicate on publicly available data or their own data sets.
For each claim, the arguments presented in literature advocating PLS are summarized, and
their invalidity is demonstrated. A new metric is proposed for researchers to assess whether
PLS– or any other indicator weighting system– can make a difference in a given situation.
What partial least squares does and why it is problematic?
Introductory texts (Hair et al., 2014) describe PLS as a structural equation model (SEM)
estimation technique that is compared to the maximum likelihood estimation of SEMs with
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
latent variables (ML-SEM). These techniques are often presented as“second-generation”
techniques that are claimed to be a-priori superior to regression, exploratory factor analysis,
or ANOVA, which are presented as“ rst-generation” techniques as shown in Panel A of
Figure 1. However, this classi cation is based simply on when the techniques were
introduced to the marketing discipline (Fornell, 1987), rather than any methodological
principle suggesting that“second-generation” methods are superior to“ rst-generation”
methods.
Methods should be chosen based on their characteristics, instead of when they were
introduced to a eld. With multiple-item data, the most fundamental decision is whether to
aggregate the data as scale scores or use them to estimate a latent variable model. Although
latent variable models are often considered superior because they can model measurement
error, this advantage rests on the correct measurement model speci cation. Unfortunately,
incorrect measurement models may cause larger bias than simply using scale scores
(Rhemtulla et al., 2020), complicating the choice between these approaches.
After deciding between latent variables and scale scores, more speci c choices are needed as
shown in Panel B of Figure 1. When using scale scores, researchers often default to linear
composites (i.e. weighted sums) for simplicity, leaving only the choice of weighting system, of
which PLS is one alternative. Unfortunately, researchers are ill-served by the existing literature
regarding both awareness of these choices and guidance in making them. Most PLS articles
obscure the fact that PLS is not a latent-variable method at all, but an indicator weighting system
that creates composite scores for subsequent regression analysis (Evermann and Rönkkö, 2021;
Goodhue et al., 2012; Rönkkö and Ylitalo, 2010). In fact, the indicator weighting is the only
difference between PLS and using regression with scale scores calculated as sums or means of
items, which many researchers learn as a rst technique for analyzing multiple-item data.
Marketing or
methodology?
1599
Figure 1.
Comparison of how
PLS is marketed and
how it positions
methodologically
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
EJM
57,6
1600
Because one of the best ways to communicate an idea is to help a person to demonstrate it to
themselves, this paper illustrates PLS using three publicly available data sets, allowing readers to
replicate these examples on their own and in the classroom. The data are the European Customer
Satisfaction Index (ECSI) data set from Tenenhaus et al. (2005), the“corporate reputation”
example from Hair et al. (2014, Chapter 2), and the technology acceptance model (TAM) data set
from SmartPLS (2020). These data sets were not chosen to obtain a particular result; rather, they
were chosen for availability and potential familiarity to the reader. Figure 2 shows the path
diagrams for the ECSI and corporate reputation models (the TAM) model is omitted because this
data set is not discussed in detail in the article). The analyses use R but the online supplement
provides screencasts for replication with SPSS and SmartPLS.
Fallacy 1: partial least square maximizes explained variance or R2
The PLS textbook by Hair et al. (2014) starts explaining PLS by stating that“PLS-SEM
estimates coef cients (i.e. path model relationships) that maximize the R2 values of the
(target) endogenous constructs” (p. 14). This claim is never explained but is repeated
throughout the book, making it appear important. The same is also stated in some PLS
criticisms (Goodhue et al., 2012, p. 984) and countless empirical applications, making it
important to address.
The R2 maximization claim is a variant of a more general claim that the PLS weights are
somehow optimal (Chin, 1998, p. 307; Henseler and Sarstedt, 2013, p. 566). These optimality
claims are typically vague, lacking explanations for what purpose the weights would be
optimal for, and are evidence-free, lacking any proofs of optimality. The speci c R2
maximization claim is imprecise as there may be multiple R2 values in a model, and it is
unclear which function of R2 is maximized (mean, sum of squares, etc.), and because PLS is a
combination of multiple inner and outer estimation algorithms, and it is unclear which
combination produces the maximum. It is also unclear why R2 maximization would be
useful for estimating parameters in a complex model consisting of multiple equations.
cusl1
cusl2
imag2
imag4
cusl3
comp2
imag1 imag3
imag5
comp1
comp3
cusco
COMP
cuex1
cuex2
cuex3
Image
Expectation
Quality
Loyalty
Value
cusa1
CUSA CUSL
Complaints
Satisfaction
LIKE
cusl1
cusl3
cusl2
like1
like3
like2
perv1 perv2
perq1
perq3
perq5
perq7
cusa2
Figure 2.
Path diagrams of the
example model
perq2 peq4
perq6
cusa1
cusa3
(a) (b)
Notes: (a) ECSI model; (b) corporate reputation model
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Empirical demonstration that partial least square does not maximize R2
To show that PLS does not maximize R2, it is suf cient to show that another technique
produces a larger R2 value. Indeed, Rönkkö (2020a, Section 2.3) calculates indicator weights
to explicitly optimize R2, leading to an R2 value more than double that produced by PLS. The
same can be done with any empirical data set. First, specify a model with one dependent
composite. To illustrate, Loyalty is predicted by image, satisfaction and complaints using
the ECSI data. Next, run this model using PLS. For comparison, run a canonical correlation
analysis with image, satisfaction and complaints indicators as x variables and loyalty
indicators as y variables. The results are shown in Table 1. PLS Mode A does not perform
well in maximizing R2. Mode B is better but still produces a smaller R2 than canonical
correlation weights do.
Conclusions on R2 maximization
If the objective is to maximize R2, PLS is demonstrably the wrong choice. If maximization of
a single R2 value (or any other statistic) was of interest, the rst step should be to de ne a
clear maximization objective. Then, the maximization problem could be solved by a general
optimization routine or by a problem-speci c algorithm. Instead, PLS seems to be a solution
in search of a problem.
Marketing or
methodology?
1601
Fallacy 2: Partial least square weights improve reliability
The most important question about PLS is whether it produces better composites than the
alternatives. That is, after a researcher has chosen to use scale scores instead of latent
variables and linear composites as the calculation strategy (Figure 1), she needs to ask
whether PLS weights are somehow better than, for example, equal or unit weights [1]. Of the
many explanations regarding the potential advantages of PLS weights (Rönkkö et al.,
2016a), the assertion that PLS weights maximize reliability is the most popular. For
example, Gefen et al. (2011) state that:
PLS Mode A PLS Mode B Canonical correlation weights
Composite weights
imag1 0.263 0.138 0.521
imag2 0.226 0.204–0.118
imag3 0.229 0.123–0.266
imag4 0.342 0.383–0.251
imag5 0.366 0.520–0.850
cusa1 0.371 0.347–0.351
cusa2 0.366 0.146–0.107
cusa3 0.462 0.676–0.703
cusco 1 1 1
cusl1 0.452 0.208–0.244
cusl2 0.133 0.105–0.092
cusl3 0.658 0.856–0.833
Regression of loyalty
Image 0.206 0.183 0.201
Satisfaction 0.481 0.524 0.560
Complaints 0.066 0.074–0.086
R2 0.462 0.499 0.514
Table 1.
Comparison of R2
between PLS mode
A, PLS mode B and
canonical correlation
weights using the
ECSI data set
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
EJM
57,6
1602
Optimization of [the] weights aims to maximize the explained variance of dependent variables.
[. . .] maximizing explained variance will also tend to minimize the presence of random
measurement error in these latent variable proxies (p. v).
Hair et al. (2014) note that PLS“prioritizes the indicators according to their individual
reliability” (p. 101). However, no evidence has been reported to support these claims.
Decades of literature show that as far as reliability is concerned“there is overwhelming
evidence that the use of differential weights [over unit weights] seldom makes an important
difference” (Nunnally, 1978, p. 297; see Wang and Stanley, 1970 for a review). Because
empirically-determined weights can provide only marginal advantages and may have
serious drawbacks, the usual recommendation is to use unweighted composites (Cohen,
1990; Graefe, 2015; Grice, 2001). Indeed, Rönkkö and Ylitalo (2010) demonstrated that PLS
weights can harm reliability and validity (Rönkkö and Evermann, 2013). Henseler et al.
(2014) objected to these conclusions, but their simulations demonstrated only trivial
advantages of PLS weights over unit weights– only a 0.6% increase in reliability in
favorable situations– and a serious loss in reliability of 16.8% in less favorable scenarios
(Henseler et al., 2014, Table 1). Recently, Henseler (2021) appears to concede the superiority
of unit weights, writing that“Sum scores can be a good choice [. . .] Particularly if the
observed variables are highly correlated, [. . .] differential weighting hardly excels over sum
scores” (p. 87). The simulations by Rönkkö et al. (2016b) suggest that inter-item correlations
of 0.4 or greater are suf cient to eliminate the effects of PLS weights on reliability even in
otherwise ideal conditions.
Gefen et al. (2011) provide another perspective on indicator weights, stating that the
“weights of the measurement items associated with the same latent variable should be
approximately the same, unless researchers have a-priori theory-based expectations of
substantial differences in performance across items” (p. viii). This leaves little room for the PLS
weights because on the one hand, if weights are not suggested by a theory, using equal weights
is a simpler and more robust solution, and on the other hand, if a theory suggests a set of
weights, that set should be used instead of empirically determined weights (Lee et al., 2013).
Empirical demonstration that partial least square does not improve reliability
If PLS composites were to provide any advantage over unweighted composites, i.e. simple
item sums, they should at least differ from them. Yet, Table 2 shows that when the ECSI
model in Figure 2 is estimated, the two kinds of composites are nearly indistinguishable,
correlating perfectly at two-digit precision. The correlation between loyalty composites at
0.93 is an exception. To understand whether the PLS composite is better than the
unweighted one, it is essential to check the weights and to understand why they differ. In
this case, the PLS weights are 0.45, 0.13 and 0.66, showing that PLS downweighted the
second indicator. Factor analysis of the loyalty scale produces a loading of 0.10 for the
second indicator. Normally, an indicator with such a low loading would be dropped and this
is what Tenenhaus et al. (2005) did. After this, the unweighted and the PLS composites
correlate at 0.99 and thus one cannot have a meaningful advantage over the other.
Repeating the same analysis with the other two data sets did not produce a single
correlation below the 0.99 level (online supplement). Rönkkö et al. (2015, 2016a) show similar
results with two additional data sets, establishing a clear pattern: PLS weights do not
appear to provide any advantages for data that they are commonly applied to.
Conclusions on reliability improvement
The comparisons of PLS and unweighted composites show what has been known for
decades: differential weights rarely make a difference. As long as the indicators are at least
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
PLS Mode A composites Unit weight composites
1 2 3 4 5 6 7 8 9 10 11 12 13 15 16
1 Image 1
2 Expectation 0.505 1
3 Quality 0.749 0.557 1
4 Value 0.508 0.361 0.586 1
5 Satisfaction 0.693 0.510 0.795 0.606 1
6 Complaints 0.475 0.257 0.532 0.355 0.526 1
7 Loyalty 0.564 0.380 0.538 0.530 0.656 0.418 1
8 Image 0.997 0.507 0.744 0.510 0.685 0.463 0.557 1
9 Expectation 0.506 0.999 0.557 0.361 0.510 0.257 0.380 0.508 1
10 Quality 0.744 0.554 0.999 0.578 0.788 0.528 0.533 0.739 0.553 1
11 Value 0.501 0.359 0.579 0.999 0.599 0.351 0.524 0.503 0.359 0.572 1
12 Satisfaction 0.690 0.512 0.794 0.600 0.999 0.519 0.652 0.683 0.513 0.788 0.593 1
13 Complaints 0.475 0.257 0.532 0.355 0.526 1.000 0.418 0.463 0.257 0.528 0.351 0.519 1
14 Loyalty 0.513 0.355 0.473 0.499 0.585 0.386 0.932 0.507 0.356 0.466 0.497 0.580 0.386 1
16 Loyalty, excl item 2 0.554 0.370 0.528 0.516 0.637 0.390 0.986 0.548 0.370 0.525 0.510 0.632 0.390 0.879 1
Notes: Correlations between a PLS composite and corresponding unweighted composite are italic
ECSI data and model
composites using the
and unit weighted
the PLS composites
Correlations between
Table 2.
1603
methodology?
Marketing or
EJM
57,6
1604
moderately correlated, advantages from weights are trivial (Cohen, 1990; Graefe, 2015; Grice,
2001). Nevertheless, a few recent articles have presented simulations where PLS weights
make a difference (Becker et al., 2013; Hair et al., 2017). These studies appear not to be
designed to be representative of real data sets but simply to nd scenarios where indicator
weights make a maximal difference. For example, Becker et al. (2013) used four-variable
scales consisting of two uncorrelated pairs. It is dif cult to imagine what kind of
measurement process would produce such data [2], and none of the empirical data sets used
for demonstrating PLS have this kind of correlational pattern.
Although the idea that weighted composites may have advantages over unweighted
composites is intuitively appealing, there is clear evidence that such bene ts do not exist in
practice. As Cohen (1990) puts it:
[. . .] as a practical matter, most of the time, we are better o using unit weights: þ1 for positively
related predictors, 1 for negatively related predictors, and 0, that is, throw away poorly related
predictors (p. 1306).
Considering the potential disadvantages of PLS, covered next, improving reliability is
certainly not a reason to use PLS.
Untold fact: partial least square weights can bias correlations
There are two important cases where PLS composites do differ from unweighted composites
but in a negative way. First, when two scales are only weakly correlated, PLS can in ate
regression coef cients. Second, if there are cross-loadings or correlated errors between
different scales, PLS tends to in ate the resulting biases. Consider the simple model in
Figure 3. In this case, PLS weights the a indicators by their correlations with the b indicators
(Rönkkö, 2014). The population correlations are equal at 0.147, and when applied to
population data, PLS produces equal weights as seen in Table 3. If for some reason a1
correlated more strongly with the b indicators than a2 or a3 do, a1 would receive a higher
weight than a2 or a3. We demonstrate these effects by increasing one correlation by 0.1 and
decreasing another one by 0.1, marked by dashed lines in Figure 3. As shown in Table 3,
PLS weights the indicators with the positive error correlation higher and those with the
negative correlation lower, producing a 6% larger correlation between composites.
Figure 3.
Example of chance
correlations
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Eﬀects of chance correlations on partial least square weights
Recent studies have shown that PLS capitalizes on chance in small samples (Goodhue
et al., 2015; Rönkkö, 2014; Rönkkö and Evermann, 2013). In sample data, the
correlations between the a and b indicators vary around their population values simply by
chance. With a sample of 100, the standard deviation of the correlation is 0.100, making the
in ation of composite correlations likely in any given sample, i.e. PLS capitalizes on chance
correlations. The magnitude of the bias depends on the strength of the latent variable
correlations. Figure 4 shows the results of applying different analysis techniques to 1,000
simulated samples (N = 100) from Figure 3, varying the latent variable correlation. The
differences are clear: both sets of PLS results are biased away from zero, producing a small
secondary peak (mode) of negative estimates. As the population correlation increases the PLS
estimates approach equal-weight estimates. In all cases, ML-SEM estimates are unbiased.
Capitalization on chance explains the simulation results by Chin and Newsted
(1999), which were pivotal in starting the myth that PLS would be particularly
appropriate for small samples (Rönkkö, 2014; Rönkkö and Evermann, 2013). This bias
is also solely because of sampling error and could be completely avoided with no
downsides by using equal weights. Indeed, when discussing these nding,s Henseler
(2021) agrees that“sum scores are a viable approach to mitigate problems of‘chance
correlations’ as described by Rönkkö (2014)” (p. 87). However, because it is dif cult to
know a priori if constructs are highly correlated (and estimating these is surely a key
purpose of a typical research study), using equal weights is always a better choice in
real research situations.
Equal correlations Unequal correlations
PLS Mode A Equal weights PLS Mode A Equal weights
Indicator weights
a1, b1 0.410 0.410 0.506 0.410
a2, b2 0.410 0.410 0.324 0.410
a3, b3 0.410 0.410 0.395 0.410
Composite correlation 0.223 0.223 0.236 0.223
Notes: Models based on Figure 3. Weights of a and b indicators are symmetric
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Marketing or
methodology?
1605
Table 3.
Effects of chance
correlations on PLS
weights and
composite
correlations
Figure 4.
Comparison of
regression with
unweighted
composites, PLS
composites and latent
variable SEM using
1,000 replications of
simulated data
EJM
57,6
1606
Empirical demonstration of bias because of chance correlations
Because none of the example data sets contain any weakly correlated scales, the problem of
chance correlations is demonstrated here by generating additional variables for the ECSI
data set. A six-sided die was rolled (simulated in R) and the values were recorded into four
new variables (Latent die, Error die 1, Error die 2 and Error die 3), with three new variables
die1, die2 and die3 created as sums of the latent die and each of the error die variables. Thus,
the die variables form a scale that is uncorrelated with the other scales.
PLS analysis was run in three different con gurations shown in Figure 5, using a subset
of the variables for simplicity. The table provides three key takeaways: rst, the PLS
weights, particularly for loyalty and satisfaction, vary widely from one analysis to the next.
Second, the correlations involving the die composite are always stronger when using PLS
weights than when using unit weights because of capitalization on chance. Third, the
correlations between PLS composites are always larger when the correlation corresponds to
a regression path (are“adjacent”). For empirical demonstrations of this PLS feature, see
Rönkkö et al. (2016b, Table 1). The capitalization on chance effect can be seen in the
distribution of the bootstrap replications of the regression estimates shown in Figure 6.
Empirical demonstration of the eﬀects of cross-loadings on partial least sqaure weights
The effect of cross-loadings is demonstrated using the corporate reputation data from Hair
et al. (2014, Chapter 2). Factor analysis results in Table 4 show that indicator Comp1 cross-
loads strongly on the comp and like factors and the Cusl1 indicator has a weaker cross-
loading on like. Recommended research practice is to omit the problematic indicator (Hair,
2010, Chapter 3), but Table 5 shows that PLS does the exact opposite, assigning Comp1
indicator the highest weight. This overweighting of Comp1 causes the comp composite to
contain more variance of like than it should, and the regression coef cient of the comp
composite is increased at the cost of decreasing the coef cient of the like composite.
In the previous example, the cross-loading affected two non-adjacent scales. To demonstrate
the effects of a cross-loading between two adjacent scales, one was arti cially created between
Like2 and Cusl by calculating a new variable as Like2new ¼ Like2 þ Cusl1þCusl2þCusl3
3 . The second
PLS analysis 1 PLS analysis 2 PLS analysis 3 Unit weights
Loyalty
Loyalty
Loyalty
Die
Die
Die
Satisfaction
Satisfaction
Satisfaction
Figure 5.
Weights and
composite
correlations for three
different PLS
analyses and unit
weights using the
ECSI data set
Composite correlations
Loyalty -
0.650 0.022 0.659 0.580
Satisfaction
Die -
0.012-0.160 -0.044 -0.009
Satisfaction
Die -
-0.088 -0.109 0.023-0.048
Loyalty
Indicator weights
cusa1 0.370 1.165 0.437 0.400
cusa2 0.367 -0.814 0.318 0.400
cusa3 0.462 0.015 0.446 0.400
cusl1 0.505 0.973 0.453 0.478
cusl2 0.136 0.551 0.104 0.478
cusl3 0.609 -0.385 0.663 0.478
die1 0.972 0.340 -0.302 0.407
die2 0.255 0.428 0.826 0.407
die3 -0.275 0.450 0.465 0.407
Note: Adjacent PLS composites are bolded
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Indicator
Factors
Factor 1: Like Factor 2: Cusl Factor 3: Comp
comp1 0.412 0.083 0.302
comp2–0.017 0.033 0.777
comp3 0.017–0.027 0.833
like1 0.796 0.015 0.031
like2 0.846–0.007–0.071
like3 0.655 0.033 0.096
cusl1 0.210 0.548 0.043
cusl2–0.025 0.983–0.023
cusl3–0.003 0.713 0.038
Notes: Principal axis factoring with oblimin rotation. Loadings exceeding 0.1 in absolute value are Italic
set of columns of Table 5 shows the results from rerunning the analyses using these
manipulated data. For unit weights, the cross-loading in ates the regression
coef cient by 60% from 0.333 to 0.535. For PLS weights, the coef cient is in ated by
80% from 0.331 to 0.599. Thus, PLS exacerbates the problem of cross-loadings.
Unfortunately, PLS is often applied without following the strict recommendation
that one should“never create a [composite] without rst assessing its
unidimensionality with exploratory or con rmatory factor analysis” (Hair, 2010, p.
127), causing problems like the ones shown above to easily escape detection.
Conclusions on bias because of partial least square weights
With correlated indicators, indicator weights rarely make a difference. Two known
scenarios where PLS weights do make a difference are capitalization on chance when
indicators are only weakly correlated across scales and in ating the effects of cross-
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Marketing or
methodology?
1607
Figure 6.
Bootstrap
distributions of the
estimates for the
three example PLS
analyses. The vertical
line marks the
original estimate
Table 4.
Factor analysis of the
corporate reputation
data set
EJM
57,6
Data with artificially
Original data
generated cross-loading
PLS Mode A Unit weights PLS Mode A Unit weights
1608
Table 5.
Regressions with
PLS and unit
weighted composites
using the corporate
reputation data set
Regression estimates
Comp! Cusa 0.152 0.122 0.058 0.045
Comp! Cusl 0.016 0.011–0.095–0.074
Like ! Cusa 0.433 0.452 0.578 0.570
Like ! Cusl 0.331 0.333 0.599 0.535
Cusa ! Cusl 0.509 0.511 0.364 0.401
Weights
comp1 0.539 0.401 0.539 0.401
comp2 0.343 0.401 0.343 0.401
comp3 0.323 0.401 0.323 0.401
like1 0.419 0.386 0.348 0.382
like2 0.378 0.386 0.489 0.382
like3 0.360 0.386 0.300 0.382
cusa 1.000 1.000 1.000 1.000
cusl1 0.368 0.385 0.373 0.385
cusl2 0.418 0.385 0.416 0.385
cusl3 0.366 0.385 0.363 0.385
loadings. Rigdon (2016) claims that weakly correlated scales present a well-known violation
of the assumptions of PLS. Unfortunately, except for the new book by Henseler (2021), not a
single introductory text makes this assumption explicit. Further, it is unclear how a
researcher could know that their scales are weakly correlated in advance, nor is it clear why
a method that cannot deal with weakly correlated scales would be of any use in real research
situations. Fortunately, these problems are easily avoided by using equal weights in the
analysis.
New methodological proposal: composite equivalence index
The previous sections demonstrated that using PLS does not improve reliability
meaningfully and can lead to problems in small samples or for cross-loading items. Hence,
researchers should always consider unweighted composites as the rst choice and“always
include this simple contender and test more sophisticated alternatives against it” (Dijkstra,
2009, p. 5).
The composite equivalence index (CEI) is proposed to determine if the PLS composites
differ substantially from unweighted composites. The CEI can be calculated by exporting
the composites from PLS software and correlating these with unit-weighted composites.
Two variants of the index are proposed. CEIindividual is the correlation of each PLS
composite with the corresponding unweighted composite; CEIminimum is the minimum of
the CEIindividual and quanti es whether PLS weights make a difference at all for the
analysis.
The CEI statistic can be expressed in matrix form:
CEI¼ diag WPLS SW0
Unit
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
where CEI is a vector of the CEIindividual values, WPLS is the PLS weight matrix and WUnit is
the unit weight matrix and S is the sample correlation matrix. Using the ECSI data (Table 2),
the CEI indices would be calculated as follows:
Marketing or
methodology?
1609
The CEIindividual values on the diagonal are 1.00, except for the loyalty composite, which has
a CEIindividual value of 0.93, which is also the CEIminimum value.
The CEI index is applied by comparing it against a cutoff, as shown in Figure 7. Further
research is required for establishing cutoffs and how the choice of cutoff affects the
regression estimates but 0.95 is proposed as a conservative starting point. If there is no
meaningful difference, unweighted composites are recommended because they avoid the
potential problems of PLS. Indeed, it is a solid research practice to prefer simpler techniques
over complex ones unless the complex technique provides a clear advantage (Kline, 2019,
pp. 224–226; Wilkinson, 1999).
Small CEI values call for a choice by the researcher. In this case, researchers must
interpret the weights and explain why the particular weights are sensible in the application
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
EJM
57,6
1610
Figure 7.
Guidelines for
choosing between
unit weights and
differential weights
based on CEI
statistics
context. If no“a-priori theory-based expectations of substantial differences in performance
across items” (Gefen et al., 2011, p. viii) exists, equal weights should be preferred for their
robustness. Indeed, as Hair et al. (2010) state“summated [sic] scales are recommended as the
rst choice as a remedy for measurement error where possible” (p. 172).
If empirical indicator weights are used, CEIindividual values should always be reported
because this increases transparency and forces researchers to justify their choice of weights.
CEI statistics are a standard part of the output in the matrixpls R package (Rönkkö, 2021)
and could easily be added to other software.
Fallacy 3: using average variance extracted and composite reliability with
partial least squares to validate measurement
A problem with pls not related to indicator weights is the assessment of measurement
quality using the average variance extracted (AVE) and composite reliability (CR) values.
Fornell and Larcker (1981) introduced the AVE and CR values to the marketing discipline as
a way to evaluate con rmatory factor analysis (CFA) results. The logic of using these
statistics with PLS seems to be as follows:
Premise A: PLS is a useful technique for CFA.
Premise B: AVE and CR are useful for summarizing CFA results for model
assessment.
Conclusion: AVE and CR are useful for summarizing PLS results for model
assessment.
Unfortunately, the conclusion is incorrect because Premise A fails. PLS does not do factor
analysis. The reported“loadings” are simply correlations between indicators and
composites that they form, leading to severe bias in the AVE and CR values. Yet, the use of
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
AVE and CR continues to be advocated (Hair et al., 2020) although strong evidence against
the practice has been available for a decade (Evermann and Tate, 2010), has been published
in a leading research methods journal (Rönkkö and Evermann, 2013) and has been
corroborated by PLS advocates’ own research (Henseler et al., 2014; McIntosh et al., 2014)!
PLS proponents have developed two responses. The rst is to deny its relevance by
arguing that the studies by Evermann and coauthors (Evermann and Tate, 2010; Rönkkö
and Evermann, 2013) are based on factor models, which PLS is not intended to estimate.
This claim is contradicted by both the original (Jöreskog and Wold, 1982, eq. (5),7; Wold,
1982, eq. 1a–10b) and more recent PLS literature (Chin, 1998, eq. (1), 7, 9; Tenenhaus et al.,
2005, pp. 163–166), which discuss factor models. Also, Hair et al. (2014) position PLS
within“a class of multivariate techniques that combine aspects of factor analysis and
regression” (p. xi). In research practice, PLS is used nearly exclusively for estimating
factor models. To demonstrate, Google Scholar was searched for PLS-based articles
published in European Journal of Marketing in 2020. Of the rst ve results, two used
PLS with the AVE and CR statistics, and used the terms“loadings,” “factors” and“factor
loadings” (Bandara et al., 2021; Cuong et al., 2020). The other three articles (Kalra et al.,
2020; Mo et al., 2020; Tarabashkina et al., 2020) explicitly used factor analysis. Against
this background, claims that PLS is not used for estimating factor models are simply
disingenuous.
A second and more productive approach has been the development of new model quality
statistics (Henseler, 2021). The most notable is the Heterotrait-Monotrait (HTMT) method
for discriminant validity assessment (Henseler et al., 2015). Importantly, HTMT does not use
PLS, but is calculated independently of any model estimates (Voorhees et al., 2016).
Although abandoning PLS in favor of other methods for measurement assessment is
certainly commendable, HTMT is not an ideal technique. Although its performance is
comparable with CFA in ideal conditions, CFA works better more generally. That Voorhees
et al. (2016) report otherwise is simply because of their incorrect application of CFA (Rönkkö
and Cho, 2020).
Empirical demonstration that partial least square results are not useful for measurement
assessment
The rst row of Table 6 shows the AVE and CR values for the model shown in Panel B of
Figure 2 using the corporate reputation data set (Hair et al., 2014, Chapter 2). Following the
recommended cutoffs (Hair et al., 2014), the rst row would be interpreted as evidence that
the comp, like, and cusa scales are reliable and have convergent and discriminant validity.
The problem is that the model quality indices indicate a model as acceptable even when
they should not: For the second row of Table 6, the model was misspeci ed by assigning the
indicators incorrectly as shown in the rst path diagram in Figure 8. This too passes the
model quality heuristics with clear margins. For the third row, the like composite was
dropped and its indicators were assigned to the comp composite as shown in the second
path diagram in Figure 8. Again, no problems are indicated. That is, the original analysis
indicates that comp and like measure two different things (discriminant validity), whereas
the current demonstration indicates that they measure the same thing (convergent validity).
The nal ten rows of Table 6 show results for models where the indicators were assigned to
composites randomly (third path diagram in Figure 8). Even in these cases, the CR and AVE
values never indicate convergent validity problems and the AVE discriminant validity rule
detects only half of the models as problematic.
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Marketing or
methodology?
1611
EJM
57,6
1612
Table 6.
Comparing the AVE
and CR statistics for
the original model
and 12 misspeci ed
models using the
corporate reputation
data set
Figure 8.
Three misspeci ed
corporate reputation
models
AVE– largest
squared
CR AVE
correlation
Comp Like Cusl Comp Like Cusl Comp Like Cusl
Original 0.864 0.898 0.900 0.680 0.746 0.751 0.263 0.329 0.273
Misspeci ed 1 0.793 0.852 0.899 0.562 0.661 0.749 0.044 0.143 0.249
Misspeci ed 2 0.892 0.900 0.581 0.751 0.581 0.273
Random 1 0.869 0.811 0.831 0.689 0.589 0.621 0.104 0.009 0.037
Random 2 0.831 0.804 0.868 0.623 0.583 0.687 0.084–0.021 0.083
Random 3 0.816 0.864 0.785 0.600 0.680 0.550–0.026 0.111–0.075
Random 4 0.843 0.822 0.900 0.642 0.609 0.750 0.080 0.047 0.273
Random 5 0.874 0.838 0.806 0.698 0.636 0.581 0.119 0.049–0.006
Random 6 0.818 0.839 0.840 0.601 0.634 0.637–0.024–0.015–0.013
Random 7 0.806 0.820 0.875 0.582 0.603 0.699 0.058–0.048 0.048
Random 8 0.806 0.848 0.852 0.584 0.651 0.658 0.016 0.082 0.093
Random 9 0.797 0.809 0.898 0.571 0.587 0.746–0.044–0.028 0.213
Random 10 0.817 0.847 0.854 0.601 0.649 0.662 0.000 0.047 0.086
Note: Italic values would be considered as problematic
Conclusions on using partial least squares for measurement validation
Methodological studies have used simulations shown that AVE and CR values calculated
from PLS results cannot detect model misspeci cation. However, the same can be shown
even without simulations. If these statistics are calculated from multiple different models
estimated from the same data, at least some of the models are incorrect and should be
identi ed as such, yet PLS fails to do so. PLS as a measurement validation method can thus
be likened to a forecaster who always says it is going to be sunny tomorrow. It is certainly
nice to hear, but ultimately useless, and you will get wet at least some of the time. In
contrast, factor analysis techniques can demonstrably detect problematic models and
provide more useful input for the AVE and CR statistics.
Discussion and conclusions
Public data sets were used to demonstrate that claims about the capabilities and advantages
of PLS are either simply untrue or at best only trivially correct. In almost every case, claims
about PLS’s advantages are advanced with virtually no evidence– seemingly more like
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
marketing strategies than methodological principles. Instead of advantages, PLS comes
with strong drawbacks, some of which are features of the core PLS algorithm, and no
amount of ad hoc retro tting will remove them (Rönkkö et al., 2016c).
Given that evidence of these problems has been available for years, it leads one to ask
why there is such a big disconnect between the methodological evidence that speaks
strongly against PLS, and the continued use of PLS in journals such as the European Journal
of Marketing. PLS is an attractive method for reasons other than the quality of its results.
PLS is easy to apply and will return results from virtually any data set (Hair et al., 2011) and
the model quality indices hardly ever reject the model (Rönkkö and Evermann, 2013). In a
research culture that prizes publication of results over their usefulness or correctness and
where there is little downside to publishing incorrect results, there are clear incentives to
using PLS. As such, it falls to the reviewers and editors to challenge authors on their choice
of methods (Rönkkö et al., 2016a).
What about the thousands of papers published using PLS? In the best case, the PLS weights
simply do not make a difference over unit weights, and the only downside is the needlessly
complicated reporting of what is essentially regression with unweighted scale scores. In other
cases, PLS weights may increase the bias due to cross-loadings or in ate weak regression
coef cients, producing false-positive results. Unfortunately, the weights are rarely reported,
making it is dif cult to assess what effect they may have had in the literature.
Using PLS to“validate” measures may have more negative consequences that are particularly
serious for newly developed scales. Scale development requires iteration because the initial scale
items do not always work well (DeVellis, 2003, Chapter 5). Because these problems go undetected
with PLS, the literature is contaminated with scales that are not properly validated and may not
t their intended measurement purposes. Thus, researchers are cautioned about building on prior
PLS work and encouraged to revalidate their scales with a more robust analysis before any
investments in large-scale data collection.
But, there are also some points of agreement between both PLS advocates and
skeptics. First, weighted and unweighted composites have their uses (Rönkkö et al.,
2016a, p. 2). Indeed, the rst author starts his research methods course by explaining
that most participants should not use SEM at all but simply use regression with
unweighted composites (Rönkkö, 2020b). If used, indicator weights must serve a clear
purpose aligned with research goals. Then, a suitable weighting algorithm can be
chosen.
Second, PLS should be explicitly presented only as a composite-based technique
(Henseler, 2021), that is, as an indicator weighting system, instead of using latent variable
and factor analysis terminology and indices (e.g. AVE, CR). Additionally, the authors
suggest dropping labels such as“structural equation modeling technique” or “second-
generation multivariate technique” when discussing PLS because, regardless of their
technical correctness, these labels have fundamentally misled researchers on the
capabilities of the PLS technique (Rönkkö et al., 2016a; Rönkkö and Evermann, 2013). Yet,
presenting PLS as“regression with weighted composites” faces two key hurdles: rst, the
PLS-SEM label has simply worked too well in terms of marketing the method and
associated tools. Second, the more transparent labeling raises the question of the purpose
of PLS weights, which the PLS literature has not answered. Ultimately, however, such a
change is an essential starting point for improving empirical research in the marketing
discipline.
The present article and the accompanying online supplementary material will hopefully
contribute to educating researchers, reviewers and editors on the fallacies and lesser-known
facts in the use of PLS. The simple demonstrations will hopefully inspire researchers to
Marketing or
methodology?
1613
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
EJM
57,6
apply them to their own data sets to advance their understanding of PLS. Hopefully, the CEI
will become de rigueur in studies applying any composite method, especially PLS. Authors
are strongly encouraged to provide more robust logic behind (and evidence for) their
methodological choices, and for reviewers and editors to demand such.
1614
Notes
1. Unit weights refer to applying equal weights after standardization. These terms are used
interchangeably in this article because standardization is used in all examples.
2. Proponents of“formative measurement” state that form ative indicators do not need to be correlated.
Even so, they generally are at least moderately correlated in practice.
References
Ali, F., Rasoolimanesh, S.M. and Cobanoglu, C. (2018), Applying Partial Least Squares in Tourism and
Hospitality Research, Emerald Group Publishing, Bingley.
Bandara, R., Fernando, M. and Akter, S. (2021),“Managing consumer privacy concerns and defensive
behaviours in the digital marketplace”
, European Journal of Marketing, Vol. 55 No. 1,
pp. 219-246, doi: 10.1108/EJM-06-2019-0515.
Becker, J.-M., Rai, A. and Rigdon, E. (2013),“Predictive validity and formative measurement in
structural equation modeling: embracing practical relevance”
, ICIS 2013 Proceedings, available
at: http://aisel.aisnet.org/icis2013/proceedings/ResearchMethods/5
Chin, W.W. (1998),“The partial least squares approach to structural equation modeling”, in
Marcoulides, G.A. (Ed.), Modern Methods for Business Research, Lawrence Erlbaum Associates
Publishers, Mahwah, NJ, pp. 295-336.
Chin, W.W. and Newsted, P.R. (1999),“Structural equation modeling analysis with small samples using
partial least squares”, in Hoyle, R.H. (Ed.), Statistical Strategies for Small Sample Research, Sage
Publications, Thousand Oaks, CA, pp. 307-342.
Cohen, J. (1990),“Things I have learned (so far)”
, American Psychologist, Vol. 45 No. 12, pp. 1304-1312,
doi: 10.1037/0003-066X.45.12.1304.
Cuong, P.H., Nguyen, O.D.Y., Ngo, L.V. and Nguyen, N.P. (2020),“Not all experiential consumers are
created equals: the interplay of customer equity drivers on brand loyalty”
, European Journal of
Marketing, Vol. 54 No. 9, pp. 2257-2286, doi: 10.1108/EJM-04-2018-0228.
DeVellis, R.F. (2003), Scale Development Theory and Applications, Sage, Thousand Oaks.
Dijkstra, T.K. (2009),“PLS for path diagrams revisited, and extended”
, Proceedings of the 6th
International Conference on Partial Least Squares, Beijing.
Evermann, J. and Rönkkö, M. (2021),“Recent developments in PLS”
, Communications of the
Association for Information Systems.
Evermann, J. and Tate, M. (2010),“Testing models or tting models? Identifying model misspeci cation in
PLS”
, ICIS 2010 Proceedings, available at: http://aisel.aisnet.org/icis2010_submissions/21
Fornell, C. (1987),“A second generation of multivariate analysis: classi cation of methods and
implications for marketing research”
, Review of Marketing, Vol. 87, pp. 407-450.
Fornell, C. and Bookstein, F.L. (1982),“Two structural equation models: LISREL and PLS applied to
consumer exit-voice theory”
, Journal of Marketing Research, Vol. 19 No. 4, pp. 440-452.
Fornell, C. and Larcker, D.F. (1981),“Evaluating structural equation models with unobservable
variables and measurement error”
, Journal of Marketing Research, Vol. 18 No. 1, pp. 39-50.
Gefen, D., Rigdon, E.E. and Straub, D.W. (2011),“An update and extension to SEM guidelines for
administrative and social science research”
, MIS Quarterly, Vol. 35 No. 2, pp. 3-14.
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Goodhue, D.L., Lewis, W. and Thompson, R. (2012),“Does PLS have advantages for small sample size
or non-normal data”
, MIS Quarterly, Vol. 36 No. 3, pp. 981-1001.
Goodhue, D.L., Lewis, W. and Thompson, R. (2015),“PLS pluses and minuses in path estimation
accuracy”
, AMCIS 2015 Proceedings, available at: http://aisel.aisnet.org/amcis2015/ISPhil/
GeneralPresentations/3
Graefe, A. (2015),“Improving forecasts using equally weighted predictors”
, Journal of Business
Research, Vol. 68 No. 8, pp. 1792-1799, doi: 10.1016/j.jbusres.2015.03.038.
Grice, J.W. (2001),“A comparison of factor scores under conditions of factor obliquity”
, Psychological
Methods, Vol. 6 No. 1, pp. 67-83, doi: 10.1037//1082-989X.6.1.67.
Hair, J.F., Howard, M.C. and Nitzl, C. (2020),“Assessing measurement model quality in PLS-SEM using
con rmatory composite analysis”
, Journal of Business Research, Vol. 109, pp. 101-110,
doi: 10.1016/j.jbusres.2019.11.069.
Hair, J.F., Ringle, C.M. and Sarstedt, M. (2011),“PLS-SEM: indeed a silver bullet”
, Journal of Marketing
Theory and Practice, Vol. 19 No. 2, pp. 139-152, doi: 10.2753/MTP1069-6679190202.
Hair, J.F., Hult, G.T.M., Ringle, C.M. and Sarstedt, M. (2014), A Primer on Partial Least Squares
Structural Equations Modeling (PLS-SEM), SAGE Publications.
Hair, J.F., Black, W.C., Babin, B.J., and Anderson, R.E. (2010), Multivariate Data Analysis: A Global
Perspective (7th ed.), Pearson Education, Upper Saddle River, NJ.
Hair, J.F., Hult, G.T.M., Ringle, C.M., Sarstedt, M. and Thiele, K.O. (2017),“Mirror, mirror on the wall: a
comparative evaluation of composite-based structural equation modeling methods”
, Journal of
the Academy of Marketing Science, Vol. 45 No. 5, pp. 1-17, doi: 10.1007/s11747-017-0517-x.
Henseler, J. (2021), Composite-Based Structural Equation Modeling: Analyzing Latent and Emergent
Variables, The Guilford Press, New York, NY.
Henseler, J. and Sarstedt, M. (2013),“Goodness-of- t indices for partial least squares path modeling”
,
Computational Statistics, Vol. 28 No. 2, pp. 565-580, doi: 10.1007/s00180-012-0317-1.
Henseler, J., Ringle, C.M. and Sarstedt, M. (2015),“A new criterion for assessing discriminant validity in
variance-based structural equation modeling”
, Journal of the Academy of Marketing Science,
Vol. 43 No. 1, pp. 115-135, doi: 10.1007/s11747-014-0403-8.
Henseler, J., Dijkstra, T.K., Sarstedt, M., Ringle, C.M., Diamantopoulos, A., Straub, D.W., Ketchen, D.J.,
Hair, J.F., Hult, G.T.M. and Calantone, R.J. (2014),“Common beliefs and reality about PLS:
comments on Rönkkö and Evermann (2013)”
, Organizational Research Methods, Vol. 17 No. 2,
pp. 182-209, doi: 10.1177/1094428114526928.
Jöreskog, K.G. and Wold, H. (1982),“The ML and PLS techniques for modeling with latent variables”, in
Jöreskog, K.G. and Wold, H. (Eds.), Systems under Indirect Observation: Causality, Structure,
Prediction, North-Holland, Amsterdam.
Kalra, A., Agnihotri, R., Singh, R., Puri, S. and Kumar, N. (2020),“Assessing the drivers and outcomes
of behavioral self-leadership”
, European Journal of Marketing, Vol. 55 No. 4, pp. 1227-1257,
doi: https://doi.org/10.1108/EJM-11-2018-0769.
Kline, R.B. (2019), Becoming a Behavioral Science Researcher: A Guide to Producing Research That
Matters, 2nd ed., The Guilford Press, New York.
Lee, N., Cadogan, J.W. and Chamberlain, L. (2013),“The MIMIC model and formative variables:
problems and solutions”
, AMS Review, Vol. 3 No. 1, pp. 3-17, doi: 10.1007/s13162-013-0033-1.
McIntosh, C.N., Edwards, J.R. and Antonakis, J. (2014),“Re ections on partial least squares
path modeling”
, Organizational Research Methods, Vol. 17 No. 2, pp. 210-251, doi: 10.1177/
1094428114529165.
Mo, C.(J.)., Yu, T. and de Ruyter, K. (2020),“Don’t you (forget about me): the impact of out-of-the-
channel-loop perceptions in distribution channels”
, European Journal of Marketing, Vol. 54
No. 4, pp. 761-790, doi: 10.1108/EJM-05-2018-0324.
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Marketing or
methodology?
1615
EJM
57,6
1616
Nunnally, J. (1978), Psychometric Theory, McGraw-Hill, New York.
Ravand, H. and Baghaei, P. (2016),“Partial least squares structural equation modeling with R”
, Review
of Practical Assessment, Research, and Evaluation, Vol. 21 No. 1, p. 11.
Rhemtulla, M., van Bork, R. and Borsboom, D. (2020),“Worse than measurement error: consequences of
inappropriate latent variable measurement models”
, Psychological Methods, Vol. 25 No. 1,
pp. 30-45, doi: 10.1037/met0000220.
Rigdon, E.E. (2016),“Choosing PLS path modeling as analytical method in European management
research: a realist perspective”
, European Management Journal, Vol. 34 No. 6, pp. 598-605,
doi: 10.1016/j.emj.2016.05.006.
Rönkkö, M. (2014),“The effects of chance correlations on partial least squares path modeling”
,
Organizational Research Methods, Vol. 17 No. 2, pp. 164-181, doi: 10.1177/1094428114525667.
Rönkkö, M. (2020a),“Introduction to matrixpls”, available at: https://cran.r-project.org/web/packages/
matrixpls/vignettes/matrixpls-intro.pdf
Rönkkö, M. (2020b),“Back to basics approach”, available at: www.youtube.com/watch?v=ROiClgEz2No
Rönkkö, M. (2021),“Matrixpls: matrix-based partial least squares estimation (1.0.12) [computer
software]”, available at: https://github.com/mronkko/matrixpls
Rönkkö, M. and Cho, E. (2020),“An updated guideline for assessing discriminant validity”
,
Organizational Research Methods, Vol. 25 No. 1, pp. 6-14, doi: 10.1177/1094428120968614.
Rönkkö, M. and Evermann, J. (2013),“A critical examination of common beliefs about partial least
squares path modeling”
, Organizational Research Methods, Vol. 16 No. 3, pp. 425-448,
doi: 10.1177/1094428112474693.
Rönkkö, M. and Ylitalo, J. (2010),“Construct validity in partial least squares path modeling”
, ICIS 2010
Proceedings, available at: http://aisel.aisnet.org/icis2010_submissions/155
Rönkkö, M., McIntosh, C.N. and Antonakis, J. (2015),“On the adoption of partial least squares in
psychological research: caveat emptor”
, Personality and Individual Differences, Vol. 87, pp. 76-84,
doi: 10.1016/j.paid.2015.07.019.
Rönkkö, M. Evermann, J. and Aguirre-Urreta, M.I. (2016c),“Estimating formative measurement models
in is research: analysis of the past and recommendations for the future”, Unpublished Working
Paper, available at: http://urn. /URN:NBN: :aalto-201605031907
Rönkkö, M. McIntosh, C.N. and Aguirre-Urreta, M.I. (2016b),“Improvements to PLSc: remaining
problems and simple solutions”
, Unpublished Working Paper, available at: http://urn. /URN:
NBN: :aalto-201603051463
Rönkkö, M., McIntosh, C.N., Antonakis, J. and Edwards, J.R. (2016a),“Partial least squares
path modeling: time for some serious second thoughts”
, Journal of Operations Management,
Vols 47/48 No. 1, pp. 9-27, doi: 10.1016/j.jom.2016.05.002.
SmartPLS (2020),“Technology acceptance model project”, available at: www.smartpls.com/
documentation/sample-projects/tam
Tarabashkina, L., Quester, P.G. and Tarabashkina, O. (2020),“How much rms ‘give’ to CSR vs how
much they‘gain’ from it: inequity perceptions and their implications for CSR authenticity”
,
European Journal of Marketing, Vol. 54 No. 8, pp. 1987-2012, doi: 10.1108/EJM-11-2018-0772.
Tenenhaus, M., Esposito Vinzi, V., Chatelin, Y.-M. and Lauro, C. (2005),“PLS path modeling”
, Computational
Statistics and Data Analysis, Vol. 48 No. 1, pp. 159-205, doi: 10.1016/j.csda.2004.03.005.
Voorhees, C.M., Brady, M.K., Calantone, R. and Ramirez, E. (2016),“Discriminant validity testing in
marketing: an analysis, causes for concern, and proposed remedies”
, Journal of the Academy of
Marketing Science, Vol. 44 No. 1, pp. 119-134, doi: 10.1007/s11747-015-0455-4.
Wang, M.W. and Stanley, J.C. (1970),“Differential weighting: a review of methods and empirical
studies”
, Review of Educational Research, Vol. 40 No. 5, pp. 663-705, doi: 10.3102/
00346543040005663.
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
Wilkinson, L. (1999),“Statistical methods in psychology journals: guidelines and explanations”
,
American Psychologist, Vol. 54 No. 8, p. 594.
Wold, H. (1982),“Soft modeling: the basic design and some extensions”, in Jöreskog, K.G. and Wold, S.
(Eds), Systems under Indirect Observation: Causality, Structure, Prediction, North-Holland,
Amsterdam, pp. 1-54.
Marketing or
methodology?
Appendix. Online supplements
The article has the following supplementary material available online: http://doi.org/10.17605/OSF.
IO/ASGMD
alternative versions of the tables included in the article using different data sets;
data sets as an excel le, including all manipulations;
R code that reproduces all tables and gures included in the article; and
YouTube playlist contains screencast demonstrations and short video lectures https://
youtube.com/playlist?list=PL6tc6IBlZmOWOd0OUIHkQMU3kUz1VkxY
1617
Corresponding author
Mikko Rönkkö can be contacted at: mikko.ronkko@jyu.
For instructions on how to order reprints of this article, please visit our website:
www.emeraldgrouppublishing.com/licensing/reprints.htm
Or contact us for further details: permissions@emeraldinsight.com
Downloaded from http://www.emerald.com/ejm/article-pdf/57/6/1597/534020/ejm-02-2021-0099.pdf by guest on 21 February 2026
