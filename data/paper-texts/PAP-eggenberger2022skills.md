# IT Skills, Occupation Specificity and Job Separations

**Authors:** Eggenberger, Christian and Backes-Gellner, Uschi
**Year:** 2022

---

DISCUSSION PAPER SERIES

IZA DP No. 15694

IT Skills, Occupation Specificity and Job
Separations

Christian Eggenberger
Uschi Backes-Gellner

NOVEMER 2022

DISCUSSION PAPER SERIES

IZA DP No. 15694

IT Skills, Occupation Specificity and Job
Separations

Christian Eggenberger
University of Zurich

Uschi Backes-Gellner

University of Zurich and IZA

NOVEMER 2022

Any opinions expressed in this paper are those of the author(s) and not those of IZA. Research published in this series may
include views on policy, but IZA takes no institutional policy positions. The IZA research network is committed to the IZA
Guiding Principles of Research Integrity.
The IZA Institute of Labor Economics is an independent economic research institute that conducts research in labor economics
and offers evidence-based policy advice on labor market issues. Supported by the Deutsche Post Foundation, IZA runs the
world’s largest network of economists, whose research aims to provide answers to the global labor market challenges of our
time. Our key objective is to build bridges between academic research, policymakers and society.
IZA Discussion Papers often represent preliminary work and are circulated to encourage discussion. Citation of such a paper
should account for its provisional character. A revised version may be available directly from the author.
ISSN: 2365-9793

IZA – Institute of Labor Economics
Schaumburg-Lippe-Straße 5–9
53113 Bonn, Germany

Phone: +49-228-3894-0
Email: publications@iza.org

www.iza.org

IZA DP No. 15694

NOVEMER 2022

ABSTRACT
IT Skills, Occupation Specificity and Job
Separations*
This paper examines how workers’ earnings change after involuntary job separations
depending on the workers’ acquired IT skills and the specificity of their occupational
training. We categorize workers’ occupational skill bundles along two independent
dimensions. First, we distinguish between skill bundles that are more specific or less specific
compared to the skill bundles needed in the overall labor market. Second, as digitalization
becomes ever more important, we distinguish between skill bundles that contain two
different types of IT skills, generic or expert IT skills. We expect that after involuntary
separations, these different types of IT skills can have opposing effects, either reducing or
amplifying earnings losses of workers with specific skill bundles. We find clearly opposing
results for workers in specific occupations – but not in general occupations: Having more
generic IT skills is positively correlated with earnings after involuntary separations, whereas
more expert IT skills is negatively correlated.
JEL Classification:

J24, J63, M53

Keywords:

IT skills, human capital specificity, vocational education and
training

Corresponding author:
Christian Eggenberger
Department of Business Administration
University of Zurich
Plattenstrasse 14
8032 Zurich
Switzerland
E-mail: christian.eggenberger@business.uzh.ch

* Funded partly by the SNSF within the framework of the national research program "Digital Transformation" (NRP
77) and partly by the Swiss State Secretariat for Education, Research and Innovation through its Leading House on
the Economics of Education, Firm Behavior and Training Policies. We thank the Swiss Federal Statistical Office for data
provision. Declarations of interest: none.

1. Introduction
Given ever-increasing digitalization, researchers and policymakers alike consider information
technology (IT) skills crucial for success in today’s society and the labor market. European
Commission Vice-President Neelie Kroes, for example, calls computer programming skills “the
new literacy”—a skill similar to basic language or math. The provision of IT skills in formal
education, to an ever-wider population, is thus a key element in promoting workers’
employability and long-term adaptability, and guaranteeing a high and stable income over the
lifecycle (Autor, 2015; Bundesrat, 2017; Düll et al., 2016).
While the calls for including IT skills in training curricula, even in non-IT occupations, are
growing louder, the empirical basis for such policy calls remain scarce. Many empirical studies
on the relationship between IT skills and labor market outcomes have focused on the subgroup
of the IT workforce and on careers in IT (e.g., Bassellier, Benbasat, & Reich, 2003; Tambe, Ye,
& Cappelli, 2020). Moreover, the literature on the effect of IT skills on labor market outcomes
for the wider workforce, and on adaptability in particular, is mixed. Some studies find IT skills
correlated with higher short- and long-term earnings (e.g., DiMaggio & Bonikowski, 2008;
Falck, Heimisch, & Wiederhold, 2021; Hanushek, Schwerdt, Wiederhold, & Woessmann,
2015).1 Other studies find no such positive correlation in the short term, or even negative
correlations in the long term (e.g., D. J. Deming & Noray, 2018; Oosterbeek & Ponce, 2011).
In this study, we hypothesize that these mixed results are attributable to the existence of
different types of IT skills, differences not yet distinguished in empirical studies. Moreover, we
argue that the effect of different IT skills also depends on the type and the weights of the other
skills with which workers combine these IT skills. In particular, we attribute a major role to the
interaction of IT skills with the specificity of workers’ skill bundles. Using occupational
training curricula and natural language processing (NLP) tools, we create a data-driven skills
taxonomy and extract a dataset of the different types of IT skills workers acquire during
training. We examine the way in which workers combine these IT skills with other skills in
their skill bundle and the effect of these skill bundles on workers’ adaptability in the labor
market.

1
Whether this wage premium is a causal effect of having IT skills or partly due to selection bias or reverse
causality is the subject of lively debate. For a discussion of the evidence, see, e.g., DiNardo and Pischke (1997),
Falck, Heimisch, and Wiederhold (2021), or Fairlie and Bahr (2018).

2

We argue that, from a labor market perspective, researchers need to distinguish two types of IT
skills—“generic” and “expert”—because they have different effects on labor market outcomes.
Given that computers are a ubiquitous general-purpose technology with the potential for
increasing productivity in many different tasks (Bertschek, Polder, & Schulte, 2019;
Brynjolfsson & McAfee, 2011), generic IT skills—such as data management, or online
research—complement a wide range of other skills, thereby increasing a worker’s labor market
adaptability (Murnane & Levy, 1996).2 In contrast, expert IT skills—such as particular
programming languages or computer aided design (CAD)—might be highly valuable when
added to a particular skill bundle but do not complement many other skills bundles. Thus expert
IT skills, like most (technical) skills, are not likely to increase the labor market adaptability of
workers.
Theoretically, we build on Lazear’s (2009) “skill-weights” model, which we extend to account
for generic and expert IT skills. In our extension of his model, workers acquire different
amounts of generic and expert IT skills, which they combine with different types of overall skill
bundles. These overall skill bundles can vary in their degree of specificity. Some skill bundles
overlap with the skill requirements in many jobs (general bundles) while others are overlap only
with very few jobs (specific bundles). Lazear’s original (2009) model predicts that workers with
specific skill bundles have, on average, the largest wage losses after involuntary separations.
Our extension of the model predicts that generic IT skills will decrease such earnings losses
after involuntary separations, particularly for workers with specific skill bundles, while expert
IT skills do not have this positive effect. Distinguishing between generic and expert IT skills
will thus help solve the puzzle of mixed results in previous studies by showing (a) which types
of IT skills are best suited for increasing worker adaptability and (b) for which types of skill
bundles these IT skills have the largest effects.
Previous empirical studies have mostly measured IT skills as a unidimensional concept. In
contrast, we identify eleven distinct IT skills. Using our theoretical model and the OECD
(2016b) IT skills framework, we classify each of these IT skills as either generic or expert.
Moreover, we calculate a measure of the specificity of a whole occupational skill bundle,
following Eggenberger, Rinawi, and Backes-Gellner (2018). This measure reflects how similar,

2
“Generic” IT skills should not be considered “basic” IT skills in the sense of skills that are prerequisites for
interacting with IT systems, such as starting up a computer, using a mouse, or creating files. Such basic IT skills
are not the focus of our study; instead, we focus on IT skills acquired during formal education.

3

and thus transferable, the skill bundle of a worker’s training occupation is to the average skill
requirements in the labor market.
To measure occupational skill bundles, we apply NLP methods to the curricula of training
occupations of Swiss apprenticeship graduates, thereby creating a dataset of the skills these
middle-skilled workers have acquired.3 Within the past decade, economic research has begun
using automatic text analysis for generating structured datasets (Gentzkow, Kelly, & Taddy,
2019). Swiss vocational (apprenticeship) training curricula provide detailed textual descriptions
on all skills—including IT skills—that apprentices acquire during their three- to four-year
training. We employ machine learning tools—such as word embeddings, clustering, and
neuronal networks—to generate a data-driven skill taxonomy and assign each text passage in a
curriculum to each skill in the taxonomy. This approach allows us not only to identify different
types of IT skills and their importance in a curriculum but also to obtain a picture of a worker’s
overall occupational skill bundle.
To examine the labor market effects of different IT skills and skill bundles, we use wage
information from Swiss register data (the Social Protection and Labour Market survey)
spanning 1999–2010.4 Examining workers’ earnings losses after involuntary job separations,
we study how these losses are affected by (a) the specificity of the skill bundle of workers’
training occupations and (b) different types of IT skills acquired during the training. The panel
structure of the dataset allows us to hold time-invariant unobserved factors constant, that is, we
use only the variation from the change in earnings before and after an involuntary job separation
(similar to, e.g., Balestra & Backes-Gellner, 2017).
Our results show, as expected from the extension of the Lazear model, that generic and expert
IT skills have opposing effects on earnings after involuntary separations. We find that workers
in highly specific occupations (e.g., dental technicians) have the highest earnings losses after
involuntary separations.
However, we also find that earnings losses are lower if workers in highly specific occupations
also acquired generic IT skills. This positive interaction effect of generic IT skills and
occupational specificity indicates that, when involuntary separations occur, knowledge of
generic IT skills can at least partially offset the loss resulting from the specificity of skill

3
In Switzerland, apprenticeship training is the predominant type of education at the secondary level, with about
two-thirds of a cohort of Swiss students choosing this educational path.
4
Unfortunately, we cannot identify involuntary separations after 2010 due to changes in the survey method.

4

bundles. This result supports the arguments in the educational literature (e.g., Ainley, Schulz,
& Fraillon, 2016) that generic IT skills increase individuals’ problem-solving capacity and
productivity in a wide variety of tasks, thereby enabling them to adjust after involuntary
separations. However, for workers with lower levels of occupational specificity (e.g., logistics
planner) this offsetting effect is less important, i.e., we find no significant correlation between
generic IT skills and earnings losses after an involuntary separation.
In contrast, we find that earnings losses are not lower if workers in highly specific occupations
also acquired expert IT skills, i.e., there are no positive interaction effects between occupational
specificity and expert IT skills. Indeed, we even find that, for older workers with highly specific
skill bundles, earnings losses are higher if they possess expert IT skills. This result indicates
that expert IT skills limit the ability of workers with specific skill bundles to recover after
involuntary separations, possibly because the occupational specificity of their human capital
restricts their search to an even narrower occupational field.
Looking closer again at the degree of specificity, we find that the association between expert
IT skills and higher earnings losses holds only for workers with highly specific skill bundles.
At the mean level of specificity and below, we find no economically significant correlation.
One explanation is that workers with a lower level of specificity (i.e., with more general skill
bundles) can potentially find work in many occupations. This larger occupational flexibility
allows them to find well-paid jobs that value their expert IT skills without their having to forgo
the rents for the rest of their skill bundle.
This paper contributes to two strands of the economics literature. First, we contribute to the
literature on the returns to IT skills by being the first to show that researchers need to distinguish
between generic and expert IT skills – not only in theoretical models, but also empirically.
Generic IT skills are associated with smaller earnings losses after involuntary separations,
whereas expert IT skills are not avoiding earnings losses. For older workers with specific skill
bundles expert IT skills even lead to larger earnings losses, possibly because of skill
obsolescence. Second, we contribute to the literature that examines how different types of skill
combinations affect labor market outcomes. We show that even when we differentiate between
different types of IT skills, the effects of these different skills also depend on the degree of
specificity of the overall skill bundles (specific or more general) that they are combined with.
Evaluating the effect of generic and expert IT skills in combination with the specificity of the
rest of the skill bundle is therefore essential for developing accurate policy recommendations.
Thus we argue that the assumption that IT skills will always help secure the future
5

employability of all workers, even those in non-IT occupations (Curtarelli, Gualtieri, Shater
Jannati, & Donlevy, 2016), is too broad. While we find that generic IT skills can increase the
adaptability of workers, this finding does not hold for expert IT skills. We show that expert IT
skills, particularly when combined with specific skill bundles, can lead to even larger earnings
losses after involuntary separations for older workers, because their expert IT skills might often
be outdated and obsolescent and this combination reduces the number of potential jobs that fit
workers’ profiles. Educational policymakers that are involved in the design of training curricula
therefore need to weight these effects and trade-offs carefully when determining which type of
IT skills to include in which kind of training curricula.

2. Theoretical Background
Our theoretical analysis builds on Lazear’s “skill-weights” approach, an economic model that
considers human capital as a bundle of single skills. According to the skill-weights model, the
adaptability of workers after an involuntary separation depends to a large part on the bundle of
skills they have acquired and bring to the labor market when searching for a new job. More
precisely, the probability to become reemployed and earn a high wage after an involuntary
separation depends on the specificity of the worker’s skill bundle: if a worker’s bundle of skills
overlaps to a large extent with the skill requirements in the universe of alternative jobs (outside
job options on the external labor market), the chances of finding a high wage job are high. If,
in contrast, the skill bundle does not (or hardly) overlap with the universe of alternative jobs
outside, the chances are low.5 In the first case the skill bundle is called general, in the second
case it is called specific.6

Lazear’s skill-weights model assumes that, in principle, all single skills could be useful in any job; there are no
technical barriers that make skills more firm-, industry-, or occupation-specific or less firm-, industry-, or
occupation-specific (unlike the traditional literature on human capital specificity assumed, e.g., Becker, 1964;
Neal, 1995). In order to determine the specificity of a skill bundle according to the skill-weights model, it has to
be considered where, or how broadly, the skills in the bundle can be used in the overall labor market. Thereby, it
is not just a matter of how widespread single skills are, but also how they are usually combined with other skills
in the external labor market. A combination of skills in marketing and materials science, for example, is likely to
be much less common than a combination of marketing and customer servicing.
6
A measure for the specificity of a given skills bundle can be obtained by calculating the overlap of this skill
bundle with the expected skill bundle a worker would need if he or she would go to the job market. A general skill
bundle would be one where the worker can be sure to find an employment option that values all existing skills.
According to the skill-weights model, the overlaps of the worker’s existing skill bundle and the skill bundle
required in a potential new job determines the change in productivity a worker experiences after a job change.
5

6

This basic model of the skill weights approach has already been shown to lead to powerful and
empirically well supported hypotheses (Mure, 2007; Eggenberger et al., 2018; Eggenberger et
al. 2019). For example, Eggenberger, Janssen, and Backes-Gellner (2022) calculate a specificity
measure based on the skill weights approach and show that specificity leads to a risk-return
trade-off for workers in case of labor market shocks. In this paper, we introduce an important
extension to the basic model that allows us to study the particular effects of IT skills, which
may come in two different features. First, “expert IT skills” and second, “generic IT skills.”
Expert IT skills behave like any other single skill (like welding, casting or brick laying) in the
Lazear model. Like any other single skill, they add expertise to a bundle of skills in an additive
way, in this case they add IT-expertise, which is why we call them “expert IT skills”. Such
expert IT skills (such as CNC or coding in Java) are only useful in particular production contexts
but do not generally help to increase the productivity of other skills. These expert IT skills can
be highly rewarded if a job requires them, but they are of no use if a job does not require them.
Therefore, in the logic of the skill weights model, we can treat them like any other single skill.
"Expert IT skills” thus do not require a modification of the original model.
In contrast, “generic IT skills” are skills that can be used for many purposes and in many
production contexts and we call them “generic IT skills” in accordance with the OECD
definition (OECD, 2016b). Such generic IT skills are for example “online research” or
“spreadsheet skills”. Their important feature is that they enhance the productivity of a worker’s
other skills, i.e., they exhibit high complementarities with many other skills. Because generic
IT skills enhance the productivity of all (or at least many) other (additive) skills, they increase
the adaptability of workers when they are forced to change their job irrespective of the particular
skill bundles that a new job requires. Generic IT skills are always valuable after involuntary
separations, because they make a worker’s skill bundle more productive in any outside job.
Therefore, generic IT skills can play a particular role for the adaptability of workers after
involuntary separations.
To illustrate the effect of generic vs. expert IT skills, imagine two workers who are forced to
change jobs. Each of them has one IT skill but of a different type: One of the workers is skilled
at online research (a generic IT skill), the other one is skilled at CNC programming for particular
machinery (an expert IT skill). After changing the job, both workers may need to accept a job,
which asks for a range of skills that may or may not be part of their skill bundle. However, the
worker with the online research skills can use this generic IT skill to increase the productivity
of whatever skills the new job requires (for example by finding relevant information or learning
7

materials that may be needed in the new job). However, for the worker with the CNC
programming skills this expert IT skill will most likely be of limited use, as they are only
required in very particular production processes.
How can these two types of IT skills be integrated in the skill weights model and what
hypotheses can we draw with respect to adaptability after involuntary separations? In the
original Lazear model, all single skills are linked in an additive way. This means, to calculate
workers’ overall productivity, the productivity of the single skills can simply be added up (e.g.,
if one skill has a productivity of 10 and the other of 15, the overall productivity is 25). So, single
skills in the original Lazear model do not interact. However, in our extended model, which aims
to represent the particularities of IT skills, we need to take into account that generic IT skills
are complements to other single skills. In this case the overall productivity of a skill bundle will
be more than the sum of its parts (e.g., 35 instead of 25). Just as production theory (e.g., Goldin
& Katz, 1998) shows that physical production inputs may be complementary (e.g., machinery
and transportation capital), skills can also be complementary to each other (D. J. Deming, 2017;
Weinberger, 2014). We therefore extend Lazear’s (2009) model by allowing for the existence
of skill complementarities between generic IT skills and the rest of the single skills.
Following our model and assumptions, two dimensions of the workers’ skill bundles determine
their adaptability in case of adverse events (such as involuntary separations): the specificity of
the workers’ skill bundle (the overlap of workers’ skill bundles with the expected skill
requirements of the new job) and the amount of generic IT skills within their skill bundles.
Furthermore, these two dimensions also interact with each other. For workers with very specific
occupational skill bundles the advantage of generic IT skills is larger than for workers with very
general occupational skill bundles. Workers with specific skill bundles likely can only use a
small part of their previously acquired skill bundle in a new job (because the expected overlap
with external skill requirements is, by definition, smaller for specific than for general
occupations). Due to the lower skill overlap, workers with specific skill bundles will on average
suffer more from having to find a new job after an involuntary separation than workers with
general bundles. The lower overlap is also the reason why generic IT skills are particularly
valuable for workers with specific skill bundles. Generic IT skills do not lose their value when
changing jobs but instead increase the productivity of the few skills that can be transferred to
the new job. The more specific the original skill bundle, the more important are these few
transferable skills in the new job and having generic IT skills helps workers with specific skill

8

bundles to leverage these skills and to keep (stay close to) their original productivity and wage.7
In contrast, for very general skill bundles almost all skills can (by definition) be transferred to
the new job anyway, which makes generic IT skills less important to keep the original wage.
Thus, from our extension of Lazear’s (2009) model, we derive the following empirically
testable hypothesis:
Hypothesis 1: Generic IT skills reduce earnings losses of workers with specific occupational
skill bundles after involuntary separations.

In other words, for workers with more specific occupational skill bundles our model predicts a
moderating (positive) effect of generic IT skills with earnings after an involuntary separation
(i.e., skill bundles that have fewer overlaps with the skill requirements on the external job
market gain more from generic IT skills).
In contrast, expert IT skills—according to our theoretical model—are skills that behave like
any other additive skill (such as milling, welding or tax accounting). Their productivity is
additive to all other skills in the occupational bundle and they do not increase the productivity
of the other skills (by definition). Therefore, expert IT skills cannot increase the productivity of
the skills that are transferable to a new job and cannot reduce productivity losses that specific
workers have to expect.8 We thus derive the following empirically testable hypothesis:
Hypothesis 2: Unlike generic IT skills, expert IT skills do not reduce the earnings losses of
workers with specific occupational skill bundles after involuntary separations.

7

Post separation wages in equilibrium are determined by a bargaining game between the worker and the firm
that offers the best alternative job. As the workers can use their skills in more than one alternative firm, we, in line
with the original Lazear model, assume that wages are proportional to the workers’ productivity in the best
alternative job.
8
To the contrary, some scholars raise concerns that rapid technological change could lead to a rapid obsolescence
of expert IT skills for older workers. D. J. Deming and Noray (2018), for example, show that IT skills in specific
subjects (e.g., specific software and business process requirements) pay off in the short run because they are at the
technological frontier. However, given that IT requirements quickly change, technological progress erodes the
value of these skills over time.

9

3. Data and Measures
In this section, we first describe our skill dataset, which we derive from an in-depth analysis of
different apprenticeship training curricula. These curricula provide information on all skills,
including IT skills, that apprentices acquire during their training. Drawing on inputs from the
educational and IT-related literature, we then classify the IT skills into the two distinct
categories: generic and expert. Finally, we construct our measure of occupational specificity,
following Eggenberger et al. (2018), by combining the occupational skill datasets with
representative labor market data. This occupational specificity measure allows us to analyze the
role of the interaction between specific skill bundles and IT skills in determining the
consequences of involuntary job separations.

3.1 Extracting Data on Occupational Skill Bundles
Our source for the data on occupational skill bundles is the training curricula texts of Swiss
vocational education (apprenticeship) training programs, from which we extract skill
information by using a novel machine learning method. Earlier papers (Eggenberger et al. 2018)
have used methods to manually extract skill information from apprenticeship curricula, but only
for a limited number of occupations. Our novel machine learning approach allows us to extract
skill information more efficiently, thus reducing extraction costs and allowing us to
substantially expand the number of analyzed occupations.
Apprenticeship training is the most commonly chosen training path in Switzerland; about two
thirds of a cohort follow this path; training is available in about 220 different occupations.
Switzerland has a strong occupational labor market (Marsden, 1990) with an institutionalized
system of training, skill-based occupational job titles, and clearly defined occupational
structures. The training curricula thus also closely correspond to the skills that are later required
to work in the respective occupation.
Swiss apprenticeship training combines on-the-job learning at a training company (three to four
days per week) with learning at a vocational school (one to two days per week). Both training
locations follow predetermined and strictly regulated training curricula, which describe the
legally binding learning goals for the students. Extensive examinations, carried out by
independent examiners at the end of the training period, guarantee that all students who receive
a diploma have acquired the specified skills to meet their curriculum goals. Thus, training

10

curricula provide us with an exhaustive description of all the skills individuals need for an
occupation.9
Each training curriculum contains a structured, three-hierarchical level catalogue of learning
goals. These learning goals describe specific observable actions and behaviors that students
must apply in well-defined tasks—i.e., these goals describe skills. In our dataset of all 164
available training curricula10, we find 22,009 individual learning goals (on average 134 per
curriculum). Each learning goal is about 15.5 words long on average and the curricula texts
contain a total of 342,566 words.
To transform the raw curriculum texts into a usable skill database, we apply a novel machine
learning methodology with a two-stage procedure. In the first stage, we develop a data-driven
skills taxonomy. To develop this taxonomy, we start by transforming each of the 22,009
learning goals into a distributed vector representation. These vector representations leverage
information from large external text corpora to transform sentences (or words) into vectors that
encode semantic meaning. We then use these vectors to create clusters of learning goals with
similar semantic meanings, leading to 248 clusters. We interpret each of these clusters as a
distinct skill category. The definition of single skills is thus derived algorithmically, without
using any prior assumptions, and is specifically tailored for our dataset of apprenticeship
curricula. At the end of stage one, we extract keywords (single words and bi-grams) that
describe these skill clusters, using a combination of statistical measures and (minimal) human
judgement.11
In the second stage, we use the keywords we generated in the first stage as training data in a
neural network. After training, this neural network can recognize patterns in any given text
input and map these patterns to one (or more) of the skills categories we defined in stage one.
Using the network, we assign each learning goal a probability of belonging to any of the 248

9

For each occupation, we analyze the most recent training curricula that were in force and legally binding for
apprenticeships during our observation period (1999-2010). We assume that workers who graduated in an
occupation prior to our observation period updated their skill bundle on the job to meet the latest requirements in
that occupation, i.e., we assume that all workers, young or old, currently working in an occupation hold the skill
bundle that roughly corresponds to the skill bundle as specified in the current occupational training curriculum.
10
We do not include the curricula of the shorter two year EBA programs, because they are mostly aimed at
students with difficulties in school and pursued by only a small minority of each cohort.
11
The statistical measures to identify relevant keywords include term-frequency statistics (TF-IDF) and the
maximal marginal relevance (MMR) metric. The human judgement consists of an additional manual check of all
keywords that were selected by the statistical measures. In this step we eliminate keywords that are close
duplicates, overfit the texts, or do not contribute relevant information to the skill description. For example, we
eliminate the keyword “inter-company course,” as it only specifies the place where students learn skills but it does
not contribute relevant information about the skills themselves.

11

previously defined skill categories. If the network comes to the conclusion that a learning goal
describes more than one skill, it can, as opposed to the clustering approach, assign a learning
goal to one, two, or more skill categories proportionally. As a final step, we weight each
learning goal, or the assigned skill probabilities respectively, with the inverse of the total
number of learning goals in a curriculum.12 This procedure yields a database with detailed
information on the categories and weights of different skills in a curriculum. We provide more
details on the skill extraction procedure in Online Appendix A.
3.2 IT Skills
The practitioners literature makes clear the importance of distinguishing among different types
of IT skills (Grundke, Marcolin, Nguyen, & Squicciarini, 2018; OECD, 2016b). Nevertheless,
in empirical studies, IT skills are still measured mostly as a unidimensional concept or
operationalized with measures that represent a combination of different types of IT skills.
As explained in Section 3.1, we define IT skills by following a data-driven clustering approach.
The clustering algorithm in stage one is free to choose any number of skills, as long as they are
sufficiently different from one another. Therefore, the algorithm is also free to choose any
number of IT skills, rather than being constrained to select IT skills from a predefined number
of skill groups. One advantage of this approach is that we define and measure IT skills based
on real texts in real training curricula. Moreover, our approach and detailed skill descriptions
allow us to find IT skills that would likely be overlooked had we used predefined descriptions
or keywords. Many earlier papers, for example, identify IT skills by using a set of words for
particular IT tools, such as “computer,” “spreadsheets,” or “Java” (D. Deming & Kahn, 2017).
In contrast, we are able to use more recent NLP methods to capture IT skill descriptions that do
not even mention IT or specific IT tools. For example, we identify sentences such as “students
structure a digital data archive in a way that they and their colleagues can manage the data
efficiently” or “students create test cases and execute tests (black box) and automate them where
possible” as learning goals describing IT skills.
We use the OECD (2016a) IT skills framework to classify IT skills. As we do in the theory
section, the OECD distinguishes between two types of IT skills. They call them “generic” and
“specialist” IT skills and provide a practical definition of both types of IT skills. We use the

12
If, for example, a curriculum has 100 learning goals, and the total proportion of learning goals assigned to skill
No. X is twelve, then skill No. X has a weight of twelve percent in the curriculum.

12

same distinction but call them “generic” vs. “expert” IT skills,13 because these expressions
correspond well with our theoretical differentiation (and avoids confusing “specific skills
bundles” with “specialist IT skills”). Using the OECD’s practical definition, we examine all
248 skill categories that our algorithm has identified and label eleven of them “IT skills.”14
The OECD defines generic IT skills as skills that allow individuals to “use IT for professional
purposes to increase efficiency (…) in multiple work settings” (OECD, 2016a). This definition
corresponds to our theoretical conception of generic IT skills as complementary skills that
increase a worker’s productivity across a broad set of tasks and that augment many other skills
in many workplaces. As examples, the OECD lists skills such as “accessing information online”
or “using standard software.” In our self-collected skill data based on curricula texts, we identify
four types of IT skills that fit this definition of a generic IT skill.15 These are “using office suite
software,” “using (other) standard software,” “using data management,” and “using online
research/internet skills.” They are considered to be generic IT skills for the following reasons:
Using office and other standard software is a skill that most individuals apply in their daily
work to optimize their workflow and to perform a wide range of tasks more efficiently (Burning
Glass Technologies, 2017; UN, 2018). Data management skills augment a worker’s ability to
make informed decisions, plan work steps efficiently, locate possible errors, and react
accordingly (Levy & Murnane, 1996; Tambe, 2021). Online research skills help workers more
quickly search, select, organize, and communicate information and integrate these information
sources into a large variety of work processes (Greene, Yu, & Copeland, 2014; Siddiq, Scherer,
& Tondeur, 2016). As hypothesized by our theoretical model, we expect these generic IT skills
to increase a worker’s adaptability and to lower wage losses after involuntary separations.
In contrast, the OECD defines expert IT skills as skills necessary “for the production of IT
products and services,” such as the abilities to program, develop applications, and manage the
use of IT (OECD, 2016a). From the viewpoint of the skill-weights model, these expert IT skills

13

Other organizations use different categorizations. The International Labour Organization (ILO), for example,
distinguishes between “basic digital skills” (skills related to the basic use of technologies) and “advanced digital
skills” (including other algorithmic skills).
14
Our algorithm does not provide names for the skill clusters it finds. As with any clustering approach, the
researcher has to label the skill categories that make up each cluster (Gentzkow et al., 2019). We named each IT
skill based on the most often occurring keywords our algorithm assigned to the respective cluster.
15
As previously mentioned, we argue that the IT skills we identify as “generic” should not be considered “basic”
IT skills in the sense of skills that are prerequisites for acquiring expert IT skills, such as starting up a computer or
creating files. Such basic IT skills are seldom mentioned in the training curricula. Given that the target age group
of the training curricula is teenagers, the curriculum develops appear to take these skills granted. We therefore
cannot measure such very basic IT skills. Insofar as they are required of all students, they should not affect our
estimations.

13

behave like any other single skill (like milling, welding or tax accounting skills), they are
additive skills that may be used in particular production contexts only. In our self-collected skill
data, we find the following seven expert IT skill categories: “programming,” “developing
microcontroller systems,” “IT safety and data protection,” “configuring network technology,”
“configuring (other) IT systems,” “digital image editing and media handling,” and “computeraided design/manufacturing.” These expert IT skills are only useful in particular production
processes, e.g., CNC skills are only useful in very particular production context (see also
Djumalieva & Sleeman, 2018) and have no productivity-enhancing effect when a worker
changes to a different type of job after an involuntary separation. Thus, as hypothesized by our
theoretical model, we expect that these expert IT skills do not increase a worker’s adaptability
nor do they lower wage losses after involuntary separations in general.
Table 1 provides descriptive statistics of the IT skills we have identified, including the number
of occupations that require each skill. More details on the definitions of different IT skills, as
well as a sample of corresponding learning goals, can be found in Online Appendix B.

14

Table 1: IT Skills Categories
Skill label

Keywords (random selection)

Number of Av. weight
occupations (if required)

Generic IT skills
Using standard
user programs, operating systems, select file format, digital
software/periphery data organization, user software, main computer components,
tablets, data carrier, IT periphery
Using office suite IT documents, informatics spreadsheets, word processors,
software
digital documents, VLOOKUP, templates series letters,
standard office programs, pc authoring, document creation
informatics, tabulators
Data management data analysis, sql, metadata information systems, data
hierarchy, data models, integrate data, data migration,
information systems archive environment, data structure, data
master
Online research /
extranet, internet research, search engines, internet resources,
internet skills
full text search, information retrieval, eservices, IT internet,
data communication, computer information

57

0.020

17

0.014

15

0.019

11

0.009

Total Generic IT

61

0.029

46

0.016

30

0.024

27

0.028

10

0.024

9

0.021

8

0.011

4

0.036

75

0.038

Expert IT skills
Computer aided
design/manufacturi
ng
Digital image
editing & media
handling
Programming (web
& applications)

Developing
microcontroller
systems
Configuring
network
technology
IT safety and data
protection
Configuring
(other) IT systems

CAD design, CAD software, CAD technology, CAD systems
engineering, model assembly, creating components, CAD
mathematics, technical drawing, CAD output, digital design
software image editing, images, digital, vector creation, pixel
data, image storage methods, image editing tools, image tonal
values, professional image formats, image types
testing applications, applications test cases, application
development, use automation scripts, code conventions,
object-oriented programming, software engineering, CSS
websites, compilers, high-level languages
block diagrams, bus systems, hardware engineering,
computer hardware, microcontroller technology,
microprocessor, CPU, digital technology, microcontroller
system standards, RAM
network requirements, application traffic, IP addressing,
realize server services, network topologies, network
components, media server, dns dhcp, cloud services, IT user
terminals
backup, data, data protection, data security, data loss, IT
security, threats IT, malware, firewall, automatic backup
install operating systems, install drivers, locate hardware
problems, configure software, bios settings, firmware
updates, software installation, software problems,
automatically installed, IT standard configuration

Total Expert IT

Notes: Authors’ compilation based on Swiss apprenticeship training curricula. For each identified IT skill, the
table shows our self-defined skill label, a selection of ten typical associated keywords, the number of occupations
requiring the skill (total number of occupations 164), and the average weight of the skill in the curricula that
require this skill.

For our estimations, we aggregate all generic and all expert IT skills into two variables. Put
differently, for each occupation we generate two variables that contain the sum of the skill
15

weights of all generic skills and the sum of the weights on all expert IT skills, respectively.
Because many IT skills are correlated, including them separately in the regression models
would be impossible.
3.3 Specificity Measure
Our goal is to examine how generic and expert IT skills interact with the specificity of a
worker’s occupational skill bundle in determining a worker’s adaptability after involuntary
separations. Our extended Lazear model predicts that IT skills are particularly important for the
adaptability of individuals with specific skill bundles. To determine the specificity of an
occupational skill bundle, we follow Eggenberger et al.’s (2018) procedure and compare the
weighted skill bundle of a particular apprenticeship occupation to the average skill bundles of
all apprenticeship occupations (i.e. of all middle skilled workers) in the overall Swiss labor
market.16
More precisely, we first calculate the “skill distance” between all pairs of occupations, using
the data generated by our NLP approach, i.e., the 248-dimensional skill vectors of all
occupations. This skill distance measure captures the overlap between the skill bundles of
occupations and thus the extent to which the skill bundle of one occupation is transferable to
another occupation.17 We then calculate the degree of specificity of an occupation as the
average distance of the skill bundle of this particular occupation to all other skill bundles in the
overall labor market, according to the following formula:
𝑁

𝑆𝑝𝑒𝑐𝑎 = ∑ 𝑑𝑖𝑠𝑡𝑎𝑏 ∗
𝑏=1

𝐿𝑏
𝐿𝑇

(1)

where distab represents the skill distance between two particular occupations a and b, i.e., distab
is a proxy for the potential skill transferability between both occupations. A higher skill distance
means that the skill bundle of occupation a is far away from the skill bundle of occupation b,
so that individuals switching from occupation a to b will not be able to use most of their skills
after the switch. To obtain an average skill distance for each occupation, we sum up these skill

16

As apprenticeship training covers all sectors of the labor market in Switzerland, we assume that the skill
information we extract from the apprenticeship curricula adequately reflects the labor market options for all middle
skilled workers, i.e., all jobs for workers with an apprenticeship degree.
17
The distance measure is calculated as the angular separation (cosine distance) between the 248-dimensional
skill vectors of occupations a and b, i.e., the workers’ entire occupational skill bundles. The angular separation
measure is well suited and widely used for measuring the distance between high-dimensional skill vectors. We
normalize the angular separation measure such that it lies between 0 (no alignment) and 1 (perfect alignment). For
more details, see Eggenberger et al. (2018).

16

distances across all other occupations. In doing so we weight the distances by relative
employment shares of the corresponding occupations in the overall labor market (Lb/LT). A
higher average skill distance implies a lower overlap of the skill bundle of one occupation with
the average skill bundle in the labor market and thus a higher specificity. Because this definition
factors in the dependence of the specificity of workers’ skills on the thickness of the market for
a particular skill bundle, the definition closely follows the theoretical concept of Lazear’s skillweights model.18
3.4 Labor Market Histories and Sample Construction
Our analysis of individual labor market outcomes draws on data from the Social Protection and
Labour Market (SESAM) survey from 1999 through 2010.19 The data is provided by the Swiss
Federal Statistical Office and is representative for the adult population aged 15 or over living
permanently in Switzerland, including non-citizens. The SESAM combines the Swiss Labour
Force survey (SLFS) with additional data from social insurance registers. The SLFS has a
rotating panel structure and is based on a sample of about 50,000 interviews per year.20 It
contains detailed questions about each individual’s employment status (according to
international definitions), socio-demographic information, and educational background. The
educational background contains information on the training occupation at the 5-digit SBN2000
level, allowing us to match all individuals to the skill bundle of their own training occupation.21
As individuals participate in the SLFS annually for five consecutive years, we can follow
individual employment histories for up to five years.22 The SLFS contains a question for the
reason of the last job loss or last job change, allowing us to distinguish involuntary separations
(employer-initiated separations) from voluntary ones (e.g., quitting or retiring).23 By using the

Effectively, this approach approximates the distribution of the skill weights λ in the labor market. It measures
the local density of the probability density function (pdf of λ) for different occupational skill bundles.
19
In 2010, the SLFS survey was restructured, so that individuals are now interviewed for five consecutive
quarters instead of five consecutive years, making it impossible for us to add newer years to the existing data.
20
Before 2001 the sample was smaller (about 16,000 individuals).
21
In some rare cases, closely related training occupations are included in the same SBN2000 code, e.g., 3- and
4-year training programs of the same occupational field, such as Automobil-Fachmann EFZ (automotive
technician) and Automobil-Mechatroniker EFZ (automotive mechatronics technician). If more than one training
occupation is included in one SBN, we use the skills of the more common one. Additionally, as in Eggenberger et
al. (2018), we have merged predecessor occupations to their respective successor occupations.
22
Because the time horizon that we can use for our analysis begins in 1999 and ends in 2010 (due to changes in
the survey structure), a substantial number of individuals are in the data for less than five years. In addition, some
individuals dropped out of the data for other reasons (e.g., non-response, emigration, or death). An attrition analysis
shows that these cases are not correlated with our main explanatory variables.
23
We do not consider separations due to accidents or illnesses to be involuntary, because these separations (a)
were not employer-initiated and (b) are likely to have a sustainable impact on an individual’s ability to work.
18

17

same dataset to analyze systematic differences in earnings patterns for different separation
reasons, Balestra and Backes-Gellner (2017) show that the validity of this self-reported measure
is high. Because subsequent separations are likely to be endogenous to the first separation, we
focus only on the earnings consequences of the first reported separation of each worker.24
Similarly, we do not exclude observations with voluntary separations when estimating the effect
of involuntary separations, because these separations reflect the normal alternative labor market
histories of individuals.
Via the social security number (AHV), the SESAM is supplemented with earnings data from
social insurance registers. These registers contain the income and contribution periods subject
to social security taxation, including contributions from self-employed workers. Because the
registers serve as the basis for calculating pensions, they are highly reliable.
For our earnings analysis, we include individuals who are between ages 18 and 65 when we
first observe them in the data. In additional analyses, we restrict the sample to workers who are
at most aged 45, because younger workers are more likely to have exactly the skills that the
training curricula demand.25 Moreover, we also perform estimations with even lower age limits
(see Section 5.2). We include all individuals who have completed an apprenticeship training
and were employed at least once during the observation period. In our main estimations, as we
want to capture the effects of the initial training, we include all workers, even those who might
have left their initial training occupation. However, in the robustness section we also run
estimations including individuals who remained in their original occupation until they first enter
our sample, because these workers are most likely to have the exact skills (and no others)
described in the curriculum. As part-time work is very common in Switzerland (in 2009, about
33 percent of all workers worked part-time, although about 60 percent of them worked more
than half-time), we include part-time workers.
We focus on cumulated annual earnings—workers’ total realized annual labor incomes—as our
outcome of interest. The effects on earnings thus measure the total effect on realized earnings
and combine variation stemming from changes in weeks worked (unemployment spells), hours
worked per week, and earnings per hour of work. In other words, we treat changes in workers’

24

In our main sample, we observe 137 individuals with two involuntary separations and 14 with three such
separations during the observation period.
25
Moreover, choosing a lower age limit ensures that we only include workers who have no or little incentives
for early retirement, which could lead to possible confounding effects. The minimum early retirement age in
Switzerland is 58. Employment rates in Switzerland are very stable until age 55, after which they slowly decrease
(Bundesamt für Statistik [BFS], 2018).

18

workloads and the corresponding earnings changes after the separation as part of the workers’
endogenous labor market outcomes.26 In additional estimations, we also examine the effects on
time (months) spent in employed work after the separation.27
After creating the panel and removing observations with missing values in essential variables,
we are left with a sample of 39,517 individuals (i.e., 88,136 observations). Table 2 contains
descriptive statistics for our main sample. The average annual income during our observation
period 1999-2010 (adjusted for inflation with base year 2010) is 60,687 Swiss Francs
(approximately 66,440 U.S. Dollars). We observe 1,582 involuntary separations.
Table 2: Descriptive statistics - Full sample
Variable

N

Mean

St. Dev.

Min

Max

Annual earnings

88,136

60,686.8

49,907.2

50.2

6,278,586

Male

88,136

0.50

0.50

0

1

Swiss

88,136

0.76

0.42

0

1

Age

88,136

41.6

11.6

18

65

Tenure

88,136

9.75

9.45

0

50.4

88,136

0.020

0.14

0

1

Individual characteristics

Separations
Involuntary Separation
Specificity & IT Skills
Occupational specificity measure (std.)

88,136

0

1.00

-1.91

1.52

Generic IT skills (weight, in percent)

88,136

1.70

2.20

0

18.0

Expert IT skills (weight, in percent)

88,136

0.98

2.50

0

26.0

Note: Data from SESAM, authors’ calculations. Observations from 39,517 individuals.

One common concern may be that expert IT skills only appear in very specific skill bundles,
because expert IT skills are less widely used than generic ones. However, many occupations
with general skill bundles also require expert IT skills (see Online Appendix B). We find that
the specificity measure is slightly negatively correlated with expert IT skills and moderately
negatively correlated with generic IT skills. Expert IT skills thus do not only appear in specific

26

Using cumulated annual or quarterly earnings as the dependent variable is a widespread practice in the literature
examining labor market shocks or displacements. See, e.g., Autor et al. (2014), Balestra and Backes-Gellner
(2017), and Jacobson, LaLonde, and Sullivan (1993).
27
Unfortunately, our data only provides us with information on months spent in employment, and not with
individual work loads.

19

skill bundles and there is significant variation in the amount of IT skills within specific skill
bundles.
We also observe a weak but positive correlation of the generic and expert IT skills, as well as
the specificity measure, with pre-separation earnings.28 This observation reinforces our decision
to use the panel dimension of our data to control for time-invariant individual characteristics.
The positive correlation between the specificity measure and the pre-separation earnings are in
line with previous research (Eggenberger et al., 2018). However, although highly specific
occupations may come with a wage premium as long as the apprenticeship graduates can remain
in their training occupation, these occupations are also riskier than general occupations, and
workers will find it difficult to find a new job that requires the same specific skill bundle
(Eggenberger et al., 2018). The next section examines whether IT skills can help reduce the
earnings losses that—according to the skills weights approach—are expected for workers with
specific skill bundles after involuntary separations.

4. Empirical strategy
We are interested in the impact of workers’ skill bundles on the earnings loss after an
involuntary separation. We hypothesize that, after an involuntary separation, workers with
specific skill bundles are at a disadvantage relative to workers with more general skill bundles,
and that this disadvantage decreases with the amount of generic IT skills (but not expert ones)
in the workers’ skill bundle. To test this hypothesis, we compare the earnings patterns of
workers with specific and general training, and different amounts of IT skills, after an
involuntary separation using an individual fixed-effects model. We estimate a simple eventstudy like equation taking the following form:
ln(𝑒𝑎𝑟𝑛𝑖𝑛𝑔𝑠𝑖,𝑡 )
= ∝𝑖 + 𝛽1 𝑆𝑝𝑒𝑐𝑖𝑓𝑖𝑐𝑖𝑡𝑦𝑜,𝑡 + 𝛽2 𝐼𝑛𝑣𝑜𝑙. 𝑆𝑒𝑝𝑎𝑟𝑎𝑡𝑖𝑜𝑛𝑖,𝑡
+ 𝛽3 𝐼𝑇_𝑆𝑘𝑖𝑙𝑙𝑜,𝐼𝑇∈[𝐺𝑒𝑛,𝐸𝑥𝑝] × 𝑆𝑝𝑒𝑐𝑖𝑓𝑖𝑐𝑖𝑡𝑦𝑜,𝑡
+ 𝛽4 𝐼𝑛𝑣𝑜𝑙. 𝑆𝑒𝑝𝑎𝑟𝑎𝑡𝑖𝑜𝑛𝑖,𝑡 × 𝑆𝑝𝑒𝑐𝑖𝑓𝑖𝑐𝑖𝑡𝑦𝑜,𝑡
+ 𝛽5 𝐼𝑛𝑣𝑜𝑙. 𝑆𝑒𝑝𝑎𝑟𝑎𝑡𝑖𝑜𝑛𝑖,𝑡 × 𝐼𝑇_𝑆𝑘𝑖𝑙𝑙𝑜,𝐼𝑇∈[𝐺𝑒𝑛,𝐸𝑥𝑝]
+ 𝛽6 𝐼𝑛𝑣𝑜𝑙. 𝑆𝑒𝑝𝑎𝑟𝑎𝑡𝑖𝑜𝑛𝑖,𝑡 × 𝑆𝑝𝑒𝑐𝑖𝑓𝑖𝑐𝑖𝑡𝑦𝑜,𝑡
′
× 𝐼𝑇_𝑆𝑘𝑖𝑙𝑙𝑜,𝐼𝑇∈[𝐺𝑒𝑛,𝐸𝑥𝑝] + 𝑋𝑖,𝑡
𝛿 + 𝜀𝑖,𝑡

(2)

28
However, as previously mentioned, estimating whether this positive correlation is due to a causal effect of
different IT skill on base wage levels or due to selection of workers into different occupations is not the aim of
this paper.

20

In Equation (2), ln(earningsi,t) denotes the logarithm of worker i’s annual (cumulated) labor
income in year t. Invol.Separationi,t is equal to one for observations after a worker has
experienced an involuntary separation and zero otherwise (e.g., if a worker has separated in the
first year of the five-year observation period, Invol.Separationi,t is equal to one for all following
four years). As we are interested in the effect of the worker’s initial skill bundle, we keep
workers’ occupational skill bundles fixed during the whole five-year observation period and
assume they correspond to the skills described in the curriculum of their initial training
occupation o (even if the workers might have changed occupations in the meantime).
Specificityo,t stands for the specificity in year t (the time of the observation) of the worker’s
initial training occupation (o).29 IT_Skillo,IT∈[Gen,Exp] stands for the weight of IT skills (in percent)
in the skill bundle of individual i’s training occupation o. To estimate the incremental effect of
different types of IT skills, we include two continuous variables representing the weights of
both IT skills in workers’ training curricula: One variable for the weights of generic IT skills
(Gen) and one for the weights of expert IT skills (Exp).
Xi,t is a vector of time-varying control variables that might affect earnings patterns—including,
importantly, age, age squared, and tenure—to account for general experience and potential
firm-specific human capital (e.g., Sullivan, 2010). Moreover, to control for differences in the
business cycle over the years and gauge the general time pattern of earnings, we include a set
of year dummies.
Finally, αi denotes individual fixed effects that capture the impact of any time-invariant
differences among individuals in observed and unobserved characteristics, such as
socioeconomic characteristics or earnings or job position before the separation.30 In other
words, we are only comparing changes in earnings patterns after an involuntary separation and
not in the differences in the base earnings between individuals with training in different
occupations. As the worker’s initially acquired skills are fixed, the individual fixed effects
would also absorb the IT_Skill variables when they are not interacted with the separation

The specificity of a worker’s skill bundle can change over time even though we keep the worker’s initial skills
fixed, because the specificity depends—per construction—on the distribution of occupations in the labor market
and the labor market shares of different occupations can increase or decrease over time. Although we include
individual fixed effects, we can thus also include the specificity measure of a worker’s initially acquired skill
bundle without interacting it with the separation indicator.
30
We use Stata’s xtreg command to estimate the model, i.e., we perform the regression on the mean detrended
dataset and using only within-individual variation.
29

21

indicator. Thus, the individual fixed effects prevent us from including the IT_Skill variables
without the interaction term and thus from estimating the influence of the IT skill weights on
workers’ average earnings levels.31
Our main interest lies in the interaction of the IT skills and the specificity of the individual’s
training occupations with the Invol.Separation indicator, i.e., the effect of the worker’s
occupational skills on earnings changes after an involuntary separation. In equation (2), β4
reflects the divergence in the earnings patterns of workers with more or less specific
occupational skill bundles after an involuntary separation. The coefficient measures how the
specificity affects the difference (in log points) between a worker’s annual earnings before the
separation and the annual earnings after the separation. More precisely, β4 reflects the effect of
an increase in Specificity by one standard deviation on the earnings change after the separation.
Likewise, β5 and β6 reflect the divergence according to whether an individual has—or does not
have—a particular IT skill. More precisely, because the specificity measure is standardized with
mean zero, β5 reflects the effects of an increase of a particular IT skill at the mean level of
Specificity. The triple interaction between Invol.Separation, Specificity and IT_Skill, β6, then
measures whether the IT skills have a different effect on the earnings after a separation,
depending on the specificity of the worker’s skill bundle.
According to the (extended) skill-weights model, we expect individuals with specific skill
bundles to have larger earnings losses (lower earnings) after an involuntary separation, i.e., a
negative coefficient for β4. However, according to hypothesis 1, we expect individuals with
generic IT skills in their specific skill bundles to have lower earnings losses (higher earnings)
after an involuntary separation. In other words, the model predicts a significant positive
interaction effect between Specificity and generic IT skills, i.e., a positive coefficient for β6. In
contrast, and according to hypothesis 2, we expect no positive coefficient on β6 for expert IT
skills, as expert IT skills are ordinary additive (non-complementary) skills. It should be noted
here that, while positive interaction effects can serve as supportive evidence of
complementarities, they cannot serve as a definitive test (Tate Twinam, 2017).
As discussed in the theory section, the skill-weights model does not make clear whether generic
IT skills already have a positive influence on earnings after the separation at the mean level of
Specificity, or whether the positive effects only manifests at higher levels of Specificity.

31

However, as we focus on worker adaptability after negative shocks, estimating the returns to IT skills in
general (i.e., the earnings levels before the separation) is not the aim of this paper.

22

Therefore, we have no clear guidance for the expected sign of β5 for generic IT skills. Likewise,
whether expert IT skills have a negative or positive effect at the mean level of Specificity
remains an empirical question.
As previously mentioned, the individual fixed effects model prevents us from estimating the
effects of occupational skills on worker’s average earnings levels. Estimating the effect of
occupational skills on average earnings levels would be challenging because individuals likely
self-selected into occupations based on their ability to earn high wages.
For the identification of the effects on earnings changes after involuntary separations however,
this type of self-selection is not necessarily a problem. For the interaction terms to measure the
causal effect of individuals’ skill bundles on their earnings losses after involuntary separations
(i.e., their adaptability), the crucial assumption is that individuals who have selected themselves
into occupations with different degrees of specificity, or occupations with or without IT skills,
do not differ in their ability to quickly recover from involuntary separations. Even if the skill
bundle might be an endogenous factor when it comes to earnings losses after a separation, our
variables of interest, the interaction terms, can still be consistent. Nizalova and Murtazashvili
(2016) show that the OLS estimate of the interaction term between an treatment variable and
an endogenous covariate is consistent if the endogenous factor of interest and the unobservables
are jointly independent of the treatment.
In our case, this condition requires that, when choosing their training, more able individuals,
for example, were not able to foresee in which occupations they would have a higher risk of an
involuntary separation, suffer more from it, and choose occupations with high or low IT skill
weights or specificity accordingly. In Online Appendix C we examine whether workers have
different pre-separation earnings patterns depending on their IT skill weights or specificity.
Finding such differences would indicate that workers selected themselves into different
occupations according to their motivation or ability to perform well in times of adverse events
(e.g., before an involuntary separation). We find no statistically significant differences, which
strengthens our confidence that our results are causal.
We are confident that our research design allows us to come as close as possible to a causal
interpretation. However, we cannot entirely rule out the possibility that unobserved variables
(e.g., unobserved ability) and the skill variables are not jointly independent of the treatment.
Therefore, we perform additional robustness tests where we include additional controls for
occupational and individual characteristics. Importantly, to dismiss the possibility that the
specificity and IT skills measure capture differences in the average required intellectual ability
23

levels between different occupations, we include a variable in our estimations (or its interaction
with the Invol.Separation indicator and Specificity measure, respectively) that measures these
ability differences. Moreover, we include controls for occupational unemployment rates, gender
and the probability of holding a managerial position (see Section 5.2).

5. Results
5.1 Main Results
Table 3 reports the main results of this paper. The table provides estimates of equation (2),
using individual fixed effects estimations, and shows the differences in the earnings patterns
after involuntary separations for workers with different skill bundles. Columns (I) and (II)
present the results of a regression without any IT skills interactions (i.e., only with the
interaction between the involuntary separation indicator and the specificity measure). Columns
(II) and (IV) include the interactions between the separation indicator, the specificity measure,
and the IT skills in a worker’s skill bundle, thereby testing hypotheses 1 and 2. Columns (I) and
(III) show the results without including additional time-varying control variables. Columns (II)
and (IV) add controls for age, age squared, and tenure.
We first examine the results without including the IT skill interactions, focusing on the
interaction between the Invol.Separation indicator and the (standardized) specificity measure.
Both earlier studies (e.g., Eggenberger et al., 2018; Kambourov & Manovskii, 2009) and the
descriptive statistics in this paper show that workers with specific skill bundles start out at a
higher wage level than workers with general skill bundles. However, according to the skillweights model, these individuals also have a higher potential for earnings losses after an
involuntary separation.
The results in Columns (I) are in line with this prediction. For years after an involuntary
separation and at the mean level of specificity, we find on average a highly significant and
economically large decline in cumulated annual earnings. A worker’s earnings in the years after
the separation are about 27 percent lower, relative to the average earnings in the years

24

immediately before the separation.32 This earnings loss is larger for workers with more specific
skill bundles and smaller for workers with more general skill bundles. The estimated coefficient
on the interaction term between the involuntary separation dummy and the specificity measure
(β4) is -0.054, showing that an increase of the specificity measure by one standard deviation is
associated with an increase of the earnings loss by about five percentage points.
Workers in the most specific occupations (e.g., dairy technologists, with a standardized
specificity measure of 1.5) thus have an estimated earnings loss of about 0.35 log points (-0.27
+ -0.054 × 1.5 = -0.351). In other words, in the first years after the separation the annual
earnings of diary technologists are about 35 percent lower compared to their own average
earnings before the separation. Workers in general occupations have a much smaller average
earnings loss after involuntary separations. Workers in the most general occupations (e.g.,
commercial employees, with a standardized specificity measure of -1.9) have an earnings loss
of only about 17 percent (-0.27 + -0.054 × -1.9 = 0.167).33 Adding time-varying control
variables for age and tenure in Column (II) barely changes the results.

Our separation indicator pools all of a worker’s observations after the separation. As on average we observe
individuals for 2.4 years after the separation, the coefficient represents the average annual earnings loss for the 2.4
years following the separation. As our dependent variable measures cumulated annual earnings, this loss includes
any losses caused by potential unemployment spells after the separation. The size of our estimates are in line with
estimated short term-earnings losses in similar studies (e.g., Balestra & Backes-Gellner, 2017; Couch & Placzek,
2010; Hijzen, Upward, & Wright, 2010).
33
Specific human capital is, of course, not the only reason why workers might experience difficult transitions
after involuntary separations. Other reasons may include losing rents from incentive contracts that raised earnings
beyond market wages (Lazear, 1979), search costs (Topel, 1991), or stigma effects (Biewen & Steffes, 2010).
32

25

Table 3: Main results: IT skills and annual earnings after involuntary separations
ln(annual earnings)
(I)
Specificity
only

(II)
Specificity
only

(II)
IT Skill
Interactions

(IV)
IT Skill
Interactions

-0.265***
(0.024)
0.017
(0.026)
-0.054*
(0.027)

-0.294***
(0.025)
0.005
(0.027)
-0.059**
(0.027)

Time-varying controls
Individual fixed effects
Year dummies

No
Yes
Yes

Yes
Yes
Yes

-0.221***
(0.033)
0.086
(0.066)
-0.098*
(0.054)
0.004
(0.026)
0.052***
(0.016)
0.011
(0.020)
-0.075***
(0.018)
No
Yes
Yes

-0.248***
(0.035)
0.088
(0.069)
-0.104*
(0.055)
0.005
(0.025)
0.051***
(0.017)
0.007
(0.020)
-0.071***
(0.019)
Yes
Yes
Yes

R-squared (within)
F-value
Number of observations

0.0065
24.31
88,136

0.0159
35.24
88,136

0.0073
142.3
88,136

0.0167
137.7
88,136

Invol.Separation (years after separation = 1)
Specificity of training (std.)
Invol.Separation × Specificity
Invol.Separation × Generic IT_Skills
Invol.Separation × Specificity × Generic IT
Invol.Separation × Expert IT_Skills
Invol.Separation × Specificity × Expert IT

Notes: Dependent variable: (log)annual earnings. OLS FE Regressions. Clustered standard errors (on the training
occupation) in parentheses. The Invol.Separation dummy is equal to one for years after an involuntary separation.
All regressions include the interaction between Specificity and IT_skill. Levels of significance: * p<0.1; ** p<0.05;
*** p<0.01.

Having established that occupational specificity is a major cause for earnings losses after
involuntary separations, we now analyze whether generic IT skills can moderate these losses.
We examine the associations between IT skills and the earnings losses after involuntary
separations in Columns (III) and (IV). These columns include measures for the weight of both
types of IT skills, generic and expert, in a skill bundle and interactions of these measures with
the specificity measure and the separation indicator. Column (IV) includes time-varying control
variables; however, the results are very similar to Column (III). Column (IV) is thus our
preferred specification.
We find that both generic and expert IT skills moderate – but in opposite directions – the
relationship between the specificity of the skill bundle and the earnings loss after the
involuntary separation, i.e., we find significant interaction effects between Specificity and
IT_Skill (β6) after a separation (Invol.Separation = 1). For easier interpretation, Figure 1 shows
the marginal effects of an increase of generic and expert IT skills by one percentage point on
26

log(annual earnings) after an involuntary separation, for different levels of training specificity.
Panel A of Figure 1 shows the marginal effects for the model specified in Table 3; Panel B
shows the marginal effects for an equivalent non-linear model. In this non-linear model, we
replaced the Specificity variable with a dummy variable indicating whether the specificity of an
individual’s occupation is above or below the sample mean, thereby allowing the effects to
differ for low or high values of Specificity in a non-linear way.
Figure 1: Marginal Effects of IT Skills at Different Levels of Specificity

Notes: The graphs show the marginal effects and 90% confidence intervals of an increase of generic and expert IT
skills by one percentage point on log(annual earnings) after an involuntary separation, for different levels of
training specificity (exclusive of the interaction between Specificity and IT_skill before the separation). Panel A
shows the marginal effects of the main model in Table 3; Panel B shows the marginal effects of an equivalent
model that includes dummy variable for Specificity (and all its interactions).

For generic IT skills, we find a positive and significant β6 coefficient of 0.051 (Table 3, Column
IV). With each standard deviation increase in Specificity, an increase of generic IT skills by one
percentage point in a curriculum is associated with post-separation earnings that are 5.1

27

percentage points higher. The left panel of Figure 1, Panel A, shows the marginal effect of
generic IT skills at different levels of Specificity. At the mean level of specificity (Specificity =
0), we find no statistically significant marginal effect (correlation) of generic IT skills on
earnings after a separation (i.e., we find no significant β5 coefficient for the two-way interaction
of the Invol.Separation indicator and the IT_Skill measure). For higher levels of Specificity,
however, generic IT skills are positively correlated with earnings after a separation (i.e.,
correlated with lower earnings losses). For a worker with a standardized specificity of 1.5, for
example, an increase of generic IT skills by one percentage point is associated with earnings
that are 8.1 (= 0.005 + 1.5 × 0.051) percentage points higher after a separation.
Because of the linear specification of our model, the correlation of generic IT skills with
earnings after a separation turns negative for lower levels of specificity. For a worker with a
standardized specificity measure of -1.3, the model estimated with equation (2) suggest that an
increase of generic IT skills by one percentage point is associated with earning that are 6.1 (=
0.005 + -1.3 × 0.051) percentage points lower. However, if we allow for the non-linear effects
of specificity by replacing the Specificity variable with a dummy variable (Figure 1, Panel B),
we observe that the correlation of generic IT skills with post-separation earnings is not
significantly different from zero for low levels of specificity (below the mean). However, the
correlation stays significant and positive for high levels of specificity (above the mean). The
correlation of generic IT skills with earnings after an involuntary separation thus appears to be
limited to workers with higher levels of specificity, for whom generic IT skills have a positive
effect.
The results for generic IT skills thus support our hypothesis 1. As expected, generic IT skills
are complementary skills that increase the adaptability and reduce the earnings losses of
workers with specific skill bundles. This result supports the argument in the educational
literature (e.g., Ainley et al., 2016) that generic IT skills can be applied across a range of
contexts and that they can increase workers’ problem-solving capacity in a wide variety of
tasks, allowing them to adjust to negative labor market shocks. However, for workers with
general skill bundles, who are already very adaptable and therefore have lower earnings losses,
generic IT appears less important, as they do not moderate earnings losses after an involuntary
separation.
For expert IT skills, we find a negative and significant β6 coefficient of -0.071. At the mean
level of specificity (Specificity = 0), we find no statistically significant marginal effect
(correlation) of expert IT skills on earnings after a separation (no significant β5 coefficient),
28

similar to the pattern for generic IT skills. With each standard deviation increase in Specificity
however, an increase of expert IT skills by one percentage point in a curriculum is associated
with post-separation earnings that are 7.1 percentage points lower. For higher levels of
specificity, expert IT skills are thus negatively correlated with earnings after a separation. For
a worker with a standardized specificity of 1.5, for example, an increase of expert IT skills by
one percentage point is associated with earnings that are 9.9 (= 0.007 + 1.5 × -0.071) percentage
points lower after a separation.
When we again look at the specification allowing for non-linear effects (Figure 1, Panel B), we
observe a pattern similar to that for generic IT skills: the correlation of expert IT skills for lower
levels of specificity is close to zero. Similar to generic IT skills, the correlation of expert IT
skills with earnings after an involuntary separation appears to be non-linear in specificity and
limited to workers with higher levels of specificity, for whom expert IT appears to have a
negative effect.
Taken together, the results for expert IT skills are thus in line with hypothesis 2, which states
that expert IT skills do not reduce the earnings losses of workers with specific occupational
skill bundles after involuntary separations. In contrast, we even find a negative correlation of
expert IT skills and earnings after such a separation for workers with very specific skill bundles.
This negative correlation shows that these workers’ capacity to recover from negative
employment shocks might be limited, possibly because their occupational specificity constricts
their search for a job that also requires their expert IT skills to a narrow occupational field.
However, for workers with general skill bundles (i.e., a specificity measure lower than the
mean), expert IT skills are not negatively correlated to earnings. Workers with general skill
bundles are more flexible than workers with specific skill bundles. As expert IT skills are
relatively scarce (Burning Glass Technologies, 2017) and costly to acquire (Broadband
Commission, 2017), this flexibility seems to allow workers with general skill bundles to find
well paid job offers that value these scarce expert IT skills without having to forgo the rents for
the rest of their skill bundle.
5.2 Effects on Employment
The earnings losses we find in our main estimations reflect the total effect of the separation
stemming from changes in weeks worked (potential unemployment spells), hours worked per
week, and earnings per hour of work. The skill-weights model is a particular kind of matching
model, and earnings after a separation could be reduced by two factors: the time it takes to find
29

a suitable job, and the productivity (and thus hourly wage) a worker will have in this new job.
To examine whether earnings losses are driven by time spent looking for a new job or a reduced
wage in the new job, we regress workers’ time spent in paid employment (in months) on our
main explanatory variables.
We report the results in Table A1 in the appendix. The results are broadly in line with the
estimations with (total) annual earnings as dependent variable and reveal that the effect on
earnings is partly driven by time not spent in paid work (unemployment or voluntary breaks),
however wage losses (i.e., the reduction of hourly wages) might be more important. Comparing
the reduction of the time spent in employment for the whole sample (Column V) of about 5%
(for an individual with average specificity and no IT skills)34 to the corresponding reduction in
earnings of about 20% (Table 3), we can conclude that time not spent in employment can only
explain about one fourth of the total effect on annual earnings. The estimated effect sizes for
the specificity and IT skill measures are also proportionally smaller. It thus seems that, although
unemployment might be an important factor, the total earnings effect is mainly driven by an
effect on wages.
5.3 Robustness Checks
To examine the robustness of our results, we perform three types of robustness checks. First,
we examine the results for different age groups. Second, we include controls for observable
differences between training occupations (intellectual requirement levels and occupational
unemployment rates) as well as individual characteristics of workers who chose these
occupations (gender and job positions). Third, we limit our sample to workers who had not
changed their occupation before the involuntary separation.
Different Age Groups
Table 4 repeats our main estimation for different age groups. We re-estimate our main model
(from Table 3), but we allow the Invol.Separation × IT Skills × Specificity effect to vary for
four different age groups (i.e., we introduce additional dummies for age groups which are fully

34

In the year following the involuntary separation, time spent in paid work is reduced by about 0.6 months.
Assuming that a worker was employed for 12 months before the separation (the sample mean is 11.6), these 0.6
months would correspond to a reduction of time spent in employment of about 5%.

30

interacted with our variables of interest). For readability, we report the results for the age groups
in four separate columns (however, all coefficients stem from one single regression).
Table 4: IT Skills and annual earnings after involuntary separations by age
ln(annual earnings)

Invol.Separation (years after separation = 1)
Specificity of training (std.)
Invol.Separation × Specificity
Invol.Separation × Generic IT Skills
Invol.Separation × Specificity × Generic IT
Invol.Separation × Expert IT Skills
Invol.Separation × Specificity × Expert IT

(I)
Age < 25

(II)
Age 25-34

(III)
Age 35-44

(IV)
Age 45-65

-0.113*
(0.058)
0.108
(0.075)
-0.321*
(0.145)
-0.024
(0.034)
0.118**
(0.041)
0.027*
(0.012)
-0.122
(0.089)

-0.339***
(0.051)
0.075
(0.069)
0.040
(0.074)
-0.005
(0.066)
-0.026
(0.029)
-0.002
(0.052)
0.016
(0.026)

-0.267***
(0.068)
0.059
(0.072)
0.013
(0.082)
0.067
(0.044)
0.049*
(0.027)
-0.027
(0.042)
-0.086***
(0.032)

-0.225***
(0.071)
0.125*
(0.068)
-0.215**
(0.097)
-0.001
(0.032)
0.080***
(0.026)
-0.001
(0.039)
-0.073*
(0.040)

Time-varying controls
Individual fixed effects
Year dummies

Yes
Yes
Yes

R-squared (within)
F-value
Number of observations

0.0191
1031.33
88’136

Notes: OLS FE Regression; The table reports the results from one single regression where the age group dummies
are fully interacted with the separation and skill variables. Clustered standard errors (on the training occupation)
in parentheses; The Invol.Separation dummy is equal to one for years after an involuntary separation. The
regression includes the interaction between Specificity and both IT skills for all age groups; Levels of significance:
* p<0.1; ** p<0.05; *** p<0.01.

The first column shows the results for workers no older than age 25. As apprentices begin their
training at approx. age 15 at the earliest, they will have completed it at approx. age 18 (for a
three-year apprenticeship) or 19 (for a four-year apprenticeship) at the earliest. Therefore, the
young workers in this sample will have a maximum of about six years of labor market
experience. They are thus (a) likely to have studied with the newest generation of training
curricula and (b) unlikely to have experienced a substantial depreciation of their learned skills.
The second column shows the results for workers aged 25 to 34. While these workers might not
have graduated under the newest generation of training curricula, they are likely to have
upgraded their IT skills according to the most recent requirements of their occupation. The third

31

column shows the results for workers aged 35 to 44, and the last column for those aged 45 to
65.
The division of the sample in four smaller sub-sample leads to less precisely estimated
coefficients. Nevertheless, the results reveal an interesting pattern. The results are quite
different for younger and older workers. We see two key differences: First, unlike for older
workers, for younger workers (age < 35), expert IT skills are not negatively associated with
earnings after involuntary separations.35 Second, for the youngest workers (age <25), a high
weight of expert IT skills seems to be associated with higher earnings after involuntary
separations. In other words, the youngest workers appear to profit from having expert IT skills
after involuntary separations. Importantly, this effect seems to hold at the mean level of
specificity already.
These results are quite in contrast to the results of older workers, for whom the results for expert
IT skills are in line with our main estimation. The results thus suggest that the negative effects
of expert IT skills are mainly driven by older workers; the results for younger workers are less
pronounced. This observation could be taken as evidence that the negative correlation for older
workers is caused by skill obsolescence. The previous literature provides some evidence that
expert IT skills might have a particularly short shelf live and suffer from strong depreciation if
not kept up to date (D. J. Deming & Noray, 2018; Janssen & Mohrenweiser, 2018). Expert IT
skills of younger workers are more likely to be up-to-date because they just recently acquired
them, moreover these IT skills are scarce and in high demand (Burning Glass Technologies,
2017). The expert IT skills of older workers in contrast are more likely to have suffered from
obsolescence because they acquired them a longer time ago. These skills therefore only increase
incompatibility with external labor market requirements. In this sense our results are consistent
with our skill weights model. This explanation would imply that workers who keep their expert
IT skills up to date would not have negative returns to these skills (as shown by Schultheiss &
Backes-Gellner, 2021). However, due to data limitations, we cannot directly test this hypothesis
in the context of this paper and have to leave it for future research.
For generic IT skills, in contrast, we find effects that go into the same direction for young and
for old workers (with the exception of workers aged 25-34, for which the interaction between
specificity and generic IT skills is positive, but not significant). This finding is in line with the

35

An F-test on the equality of the Invol.Separation × Specificity × Expert IT coefficients of the oldest and
younger age group is significant on the 10% level.

32

hypotheses that generic IT skills are less technology specific, adjust well to any kind of new
work environment, and thus suffer less from depreciation.

Controlling for Additional Occupational and Individual Characteristics
As outlined in Section 4, our estimates of the interaction terms of the separation indicator and
the skills variables can be valid, even in the presence of selection into occupations. Online
Appendix B reveals that student do self-select themselves into different occupations, as we
observe different characteristics between workers trained in occupations with high IT skill
weights and low IT skill weights. In particular, we show that males are more likely to work in
occupations with expert IT skills, and that occupations requiring high IT skills (generic or
expert) also have high intellectual requirements (based on expert ratings)36 and pay higher
wages on average. However, the estimates of our interaction terms in equation (2) remain
consistent if workers’ skill weights and the source of the heterogeneity are jointly independent
of the treatment (the involuntary separation). Unfortunately, it is not possible to test this
assumption empirically. However, we can include controls for time-constant variables, such as
occupational and individual characteristics, by interacting them with the separation indicator.
We present the results of these additional robustness checks in Table 5. The table includes the
interaction between a) intellectual requirement levels of occupations, b) gender, c) occupational
unemployment rates, and d) managerial position before the separation with the separation
indicator, as well as with the separation indicator and the specificity level. The results reveal
that males, and workers with specific skill bundles and workers in occupations with higher
unemployment rates, have larger earnings losses after involuntary separations, while workers
in managerial positions have lower earnings losses. Nevertheless, our estimates of interest
remain very similar in size and significance compared to our main estimation, thereby
corroborating our main results. Our main estimates thus do not appear to be biased by student’s
selection into occupations based on intellectual requirements, gender, unemployment rates or
propensity to hold a managerial position.

36

To measure intellectual requirement levels of different occupations we use a variable scaling from 1 to 100,
representing the average evaluation of a training occupation’s intellectual requirement levels in four different
dimensions (mathematics, science, language, and foreign languages). This rating was developed by a team of
career counselors and occupational experts (Goetze & Aksu, 2018). The rating represents the intellectual demand
of training occupations in the year 2019. However, a comparison with previous similar ratings (Stalder, 2011)
shows that the intellectual requirements of training occupations barely change over time.

33

Table 5: Additional controls
ln(annual earnings)

Invol.Sep. (years after separation = 1)
Spec. of training (std.)
Invol.Sep. × Specificity
Invol.Sep. × Generic IT_Skills
Invol.Sep. × Spec. × Generic IT
Invol.Sep. × Expert IT_Skills
Invol.Sep. × Spec. × Expert IT
Invol.Sep. × Intellectual Req.
Invol.Sep. × Spec. × Intellectual Req.

(I)
Intellectual
requirement

(II)
Gender

(III)
Occ. Unemp.
rate

(IV)
Managerial
position

(V)
All Controls

-0.277**
(0.110)
0.216
(0.265)
-0.139
(0.168)
-0.001
(0.028)
0.061*
(0.031)
0.013
(0.019)
-0.077***
(0.020)
0.001
(0.003)
0.000
(0.005)

-0.203***
(0.051)
0.117
(0.075)
-0.128
(0.085)
0.005
(0.028)
0.059***
(0.019)
0.011
(0.020)
-0.076***
(0.019)

-0.284**
(0.114)
0.106
(0.303)
0.173
(0.178)
0.015
(0.026)
0.047**
(0.018)
0.006
(0.019)
-0.068***
(0.018)

-0.257***
(0.040)
0.098
(0.072)
-0.112*
(0.058)
0.005
(0.028)
0.053***
(0.018)
0.011
(0.020)
-0.072***
(0.020)

-0.390*
(0.234)
0.380
(0.679)
0.265
(0.289)
0.006
(0.027)
0.054*
(0.028)
0.010
(0.020)
-0.071***
(0.020)
0.003
(0.004)
-0.002
(0.004)
-0.141**
(0.054)
0.020
(0.061)
2.368
(5.437)
-12.794*
(7.654)
0.278***
(0.039)
0.021
(0.031)
Yes
Yes
Yes
0.0174
526.4
81,276

-0.087*
(0.050)
0.065
(0.059)

Invol.Sep. × Gender (male = 1)
Invol.Sep. × Spec. × Gender
Invol.Sep. × Unempl. rate

0.812
(3.950)
-11.801*
(6.511)

Invol.Sep. × Spec. × Unempl. rate

Time-varying controls
Individual fixed effects
Year dummies

Yes
Yes
Yes

Yes
Yes
Yes

Yes
Yes
Yes

0.273***
(0.040)
0.020
(0.030)
Yes
Yes
Yes

R-squared (within)
F-value
Number of observations

0.0157
273.7
81,276

0.0159
234.1
81,276

0.0159
295.3
81,276

0.0170
290.3
81,276

Invol.Sep. × Managerial pos.
Invol.Sep. × Spec. × Managerial pos.

Notes: Dependent variable: (log)annual earnings. OLS FE Regressions; Clustered standard errors (on the training
occupation) in parentheses; The Invol.Sep. dummy is equal to one for years after an involuntary separation.
Intellectual Req. measures the intellectual requirement level of training occupations, the Gender dummy is equal
to one if a person is male, Unempl. Rate measures the average annual unemployment rate in each occupation
(calculated based on SESAM data), and the Managerial Pos. dummy is equal to one if a worker holds a managerial
position within the firm. Unfortunately, the intellectual requirement measure is not available for all occupations.
As we cannot match 26 occupations, we lose about 7,000 observations. All regressions include the interaction
between Specificity and both IT skills; Levels of significance: * p<0.1; ** p<0.05; *** p<0.01.

34

Excluding Occupational Changers
In our main estimations, we include all workers, even those who might have changed out of
their original training occupation. Because we condition workers’ skills on their original
training occupation, those who changed their occupation before the observation period might
have acquired additional skills that we cannot measure. However, in a robustness check, we run
an additional estimation on a reduced sample of workers who did not change their occupation
to see whether results change. For this estimation we use only workers who, at the beginning
of their individual observation period, are still working in the (5-digit) occupation that they
were trained in. These workers have not gained additional skills from working in other
occupations and which might reduce skill measurement error. However, workers who never
changed their occupation are likely to be a selective group, which may lead to biased results.
Therefore, we prefer the full sample as our main estimations and consider this to be a robustness
test only.
Table 6: Main results for occupational stayers
ln(annual earnings)
(I)

(II)
***

Time-varying controls
Individual fixed effects
Year dummies

-0.194
(0.044)
0.162*
(0.095)
-0.131
(0.086)
-0.026
(0.030)
0.060***
(0.020)
0.079***
(0.030)
-0.075***
(0.028)
No
Yes
Yes

-0.210***
(0.046)
0.134
(0.098)
-0.152*
(0.087)
-0.027
(0.029)
0.063***
(0.020)
0.076***
(0.029)
-0.073***
(0.026)
Yes
Yes
Yes

R-squared (within)
F-value
Number of observations

0.007
1138.0
41,618

0.015
986.0
41,618

Invol.Separation (years after separation = 1)
Specificity of training (std.)
Invol.Separation × Specificity
Invol.Separation × Generic IT Skills
Invol.Separation × Specificity × Generic IT
Invol.Separation × Expert IT Skills
Invol.Separation × Specificity × Expert IT

Notes: OLS FE Regressions; Clustered standard errors (on the training occupation) in parentheses; The
Invol.Separation dummy is equal to one for years after an involuntary separation. Column (I) replicates our main
regression but controls for the interaction of the Invol.Separation dummy with the intellectual requirement level
(Intellectual Req.) of an individual’s training occupation. Column (II) shows regression results for a sub-sample
of workers who were still working in their original training occupation before the involuntary separation; All
regressions include the interaction between Specificity and both IT skills; Levels of significance: * p<0.1; **
p<0.05; *** p<0.01.

35

We report the results of this robustness check in Table 6. Again, the results are in line with our
main estimations. While the coefficients for generic IT skills are very similar to those of our
main estimation, we find some differences for expert IT skills. In comparison to our main
estimation sample, we find that expert IT skills are correlated with significantly lower earnings
losses at the mean level of specificity. The correlation between expert IT skills and earnings
after the separation becomes negative only for individuals with very specific skill bundles. This
higher return to expert IT skills even after a separation might be explained by occupational
stayers being a positively selected sample37 of younger workers who are more likely to find a
job that values their expert IT skills.

6. Conclusions
This paper investigates the role of IT skills and their combination with different skill bundles
in explaining the size of earnings losses after involuntary separations. We argue that two types
of IT skills should be differentiated because they have different effects on labor market
outcomes. We call these skills generic and expert IT skills. Drawing on Lazear’s (2009) skillweights model, we derive hypotheses about the effects of generic and expert IT skills and their
combination with specific or general skill bundles on earnings after involuntary separations.
Our findings show that generic IT skills, but not expert IT skills, are critical to the adaptability
of individuals who are in occupations with specific skill bundles.
We use training curricula of Swiss apprenticeships to measure the skills a worker holds. We
apply machine learning methods to these occupational training curricula and extract
information on the skills that the apprentices learn during their training. We empirically identify
eleven separate IT skills and classify them as either generic IT skills—skills needed to increase
efficiency in daily work and in multiple work settings—or expert IT skills—skills needed for
the production of IT products and services. Both theoretically and empirically, we show that
generic IT skills can improve labor market adaptability and reduce earnings losses after
involuntary separations. The effects depend on the specificity of the workers' occupation.

37
We observe that workers who are still in their original training occupation at the start of the observation period
are on average younger and earn about 9 log-points more than workers who have changed occupations before they
enter our data.

36

We find that workers with specific skill bundles have the largest earnings losses after
involuntary separations. However, for these workers it is essential to have generic IT skills in
their bundle because that leads to lower earnings losses after involuntary separations. In
contrast, for these workers with specific skill bundles it is a disadvantage to have expert IT
skills in the bundle because they go together with—on average—larger losses after involuntary
separations. This effect is driven by older workers with specific skill bundles and does not occur
for the youngest age group. Expert IT skills thus seem to amplify the difficulties especially of
older workers with specific skill bundles after involuntary separations, possibly because expert
IT skills are more likely to become technologically obsolete. Thus, these workers could gain
from adding generic IT skills to their existing specific skill bundle. For workers with general
skill bundles, neither generic nor expert IT skills have much effect on adaptability. Workers
with general skill bundles generally have lower problems of finding a new job with equal wages
after involuntary separations.
This paper has implications for policy and curriculum development aimed at improving
workers’ labor market adaptability. By empirically differentiating two types of IT skills with
differing economic attributes, this paper contributes to a more nuanced understanding of the
effect of IT skills on labor market outcomes. Curriculum developers need to recognize which
IT skills are of generic nature—skills that enhance productivity across a wide variety of
contexts—and which are of “expert” nature—skills that are useful in limited contexts (noncomplementary skills).
Our results provide valuable insights on how these different types of IT skills affect workers in
different occupations. Previous literature shows that specific skill bundles are associated with
high immediate returns on the labor market. At the same time, our findings also confirm that
these returns are part of a trade-off because specificity can impair long term returns on the labor
market as it bears additional risks if workers need to find new jobs. However, our findings
suggest a way to reduce this risk. We show that increasing the amount of generic IT skills, such
as data management, office-suite skills or computer-aided research skills, can increase
adaptability because these generic skills increase the productivity of highly specific skill
bundles in any future job, even in jobs with very different skill requirements. Therefore, from
an educational policy perspective, it seems a valuable strategy to integrate (to a certain extent)
generic IT-skills to very specific occupational curricula because they provide higher labor
market adaptability in case workers with specific skill bundles need to change out of their
original occupation in the long run. Instead of, or in addition to, adding such skills to initial

37

training in the context of apprenticeship training, such skills can likewise be added in the
context of lifelong learning. The latter is particularly important in ageing societies.
However, according to our analyses it is important to distinguish between the different types of
IT skills because only generic IT skills are able to offset the long run downsides of specific
occupations. For expert IT skills, such as CNC or particular coding skills, we do not find similar
effects because they are not complementary to other single skills. Thus, simply adding any type
of IT skill to all training curricula will not generally increase worker adaptability. Adding expert
IT skills to training curricula with highly specific skill bundles could make these skill bundles
even more specific and workers become less adaptable. However, as specific skill bundles are
highly valued even in highly dynamic economies, higher adaptability can, according to our
theoretical model, be achieved by incorporating generic IT skills into specific training curricula
or by fostering generic IT skills in continuing education programs.
A limitation of our approach is that we only have a measure for the weight of skills in the skill
bundle of the training occupation, not the level or “up to dateness” of those skills. The literature
provides some evidence that different skills age differently, and expert IT skills may age faster
than generic IT skills. This question should be a priority in future research. Furthermore, as
generic skills might not be limited to generic IT skills but might also include other generic skills
such as social skills, self-competence or other non-cognitive skills, more future research is
needed in this context. This research should particularly examine complementarities of other
types of potentially generic skills, such as social skills, and specific occupational skill bundles.
Finally, we argue that our results do not exclusively apply to Switzerland. In Switzerland, more
than 70 percent of all workers have a VET education, and VET provides a valuable educational
path for all middle-skill workers. Our results are thus important for all countries interested in
expanding their vocational education and training systems to train their middle skilled workers.
To which extent the results can be transferred to academic education, however, should likewise
be the subject of further research.

38

Appendix A: Additional Tables
Table A1: IT Skills and months in employment after involuntary separations by age
ln(annual earnings)
(I)
Age < 25

(II)
Age 25-34

(III)
Age 35-44

(IV)
Age 45-65

(V)
All age
groups

-0.247
(0.320)
0.019
(0.218)
-1.251**
(0.606)
-0.302
(0.191)
0.053
(0.163)
0.214**
(0.104)
0.106
(0.332)

-1.148***
(0.201)
-0.121
(0.165)
-0.018
(0.324)
-0.070
(0.343)
-0.077
(0.149)
0.042
(0.288)
0.035
(0.172)

-0.884***
(0.234)
-0.214
(0.180)
-0.007
(0.353)
0.224*
(0.130)
0.112*
(0.057)
-0.036
(0.094)
-0.176***
(0.050)

-0.373
(0.447)
-0.075
(0.197)
-0.580
(0.571)
-0.246
(0.163)
0.337**
(0.140)
0.310**
(0.115)
-0.420***
(0.093)

Time-varying controls
Individual fixed effects
Year dummies

Yes
Yes
Yes

-0.654***
(0.226)
-0.161
(0.177)
-0.381
(0.331)
-0.099
(0.121)
0.167*
(0.087)
0.150*
(0.088)
-0.224***
(0.073)
Yes
Yes
Yes

R-squared (within)
F-value
Number of observations

0.021
912.5
88’079

0.019
292.0
88’079

Invol.Separation (years after separation = 1)
Specificity of training (std.)
Invol.Separation × Specificity
Invol.Separation × Generic IT Skills
Invol.Separation × Spec. × Generic IT
Invol.Separation × Expert IT Skills
Invol.Separation × Spec. × Expert IT

Notes: OLS FE Regressions; Clustered standard errors (on the training occupation) in parentheses; the results for
Columns I-IV stem from one single model with age group interactions (corresponding to Table 4); the
Invol.Separation dummy is equal to one for years after an involuntary separation. All regressions include the
interaction between Specificity and both IT skills; Levels of significance: * p<0.1; ** p<0.05; *** p<0.01.

39

References
Ainley, J., Schulz, W., & Fraillon, J. (2016). A global measure of digital and ICT literacy
skills: Paper commissioned for the Global Education Monitoring Report 2016. Paris.
Autor, D. H. (2015). Why Are There Still So Many Jobs? The History and Future of
Workplace Automation. Journal of Economic Perspectives, 29(3), 3–30.
https://doi.org/10.1257/jep.29.3.3
Balestra, S., & Backes-Gellner, U. (2017). When a Door Closes, a Window Opens? LongTerm Labor Market Effects of Involuntary Separations. German Economic Review, 18(1),
1–21. https://doi.org/10.1111/geer.12086
Bassellier, G., Benbasat, I., & Reich, B. H. (2003). The Influence of Business Managers' IT
Competence on Championing IT. Information Systems Research, 14(4), 317–336.
https://doi.org/10.1287/isre.14.4.317.24899
Becker, G. S. (1964). Human capital: A theoretical and empirical analysis, with special
reference to education. National Bureau of Economic Research, General series: Vol. 80.
New York.
Bertschek, I., Polder, M., & Schulte, P. (2019). ICT and resilience in times of crisis: evidence
from cross-country micro moments data. Economics of Innovation and New Technology,
20(1), 1–16. https://doi.org/10.1080/10438599.2018.1557417
Biewen, M., & Steffes, S. (2010). Unemployment persistence: Is there evidence for stigma
effects? Economics Letters, 106(3), 188–190. https://doi.org/10.1016/j.econlet.2009.11.016
Broadband Commission (2017). Working group on education—Digital skills for life and
work. Paris: UNESCO. Retrieved from http://unesdoc. unesco. org/images/0025/002590
…: Paris: UNESCO. Retrieved from http://unesdoc. unesco. org/images/0025/002590 …
Brynjolfsson, E., & McAfee, A. (2011). Race against the machine: How the digital revolution
is accelerating innovation, driving productivity, and irreversibly transforming employment
and the economy. Lexington, Massachusetts: Digital Frontier Press.
Bundesamt für Statistik (2018). Erwerbsquote und Erwerbsquoten in Vollzeitäquivalenten
(VZÄ) nach Geschlecht, Nationalität und Alter [Dataset].
Bundesrat (2017). Bericht über die zentralen Rahmenbedingungen für die digitale Wirtschaft.
Burning Glass Technologies (2017). The Digital Edge: Middle-skills workers and careers.
Couch, K. A., & Placzek, D. W. (2010). Earnings Losses of Displaced Workers Revisited.
American Economic Review, 100, 572–589. Retrieved from
http://www.jstor.org/stable/27804942
Curtarelli, M., Gualtieri, V., Shater Jannati, M., & Donlevy, V. (2016). Ict for work: Digital
skills in the workplace: Final report. Publications Office. https://doi.org/10.2759/498467
Deming, D., & Kahn, L. B. (2017). Skill Requirements across Firms and Labor Markets:
Evidence from Job Postings for Professionals. Journal of Labor Economics, 36(S1), 337369. https://doi.org/10.1086/694106
Deming, D. J. (2017). The Growing Importance of Social Skills in the Labor Market The
Quarterly Journal of Economics, 132(4), 1593–1640. https://doi.org/10.1093/qje/qjx022
Deming, D. J., & Noray, K. L. (2018). STEM Careers and Technological Change.

40

DiMaggio, P., & Bonikowski, B. (2008). Make Money Surfing the Web? The Impact of
Internet Use on the Earnings of U.S. Workers. American Sociological Review, 73(2), 227–
250. https://doi.org/10.1177/000312240807300203
DiNardo, J. E., & Pischke, J.‑S. (1997). The Returns to Computer Use Revisited: Have
Pencils Changed the Wage Structure Too? Quarterly Journal of Economics, 112, 291–303.
Djumalieva, J., & Sleeman, C. (2018). An Open and Data-driven Taxonomy of Skills
Extracted from Online Job Adverts. In C. Larsen, S. Rand, A. Schmid, & A. Dean (Eds.),
Developing Skills in a Changing World of Work: Concepts, Measurement and Data
Applied in Regional and Local Labour Market Monitoring Across Europe (1st ed.,
pp. 425–454). Augsburg: Rainer Hampp Verlag. https://doi.org/10.5771/9783957103154425
Düll, N., Bertschek, I., Dworschak, B., Meil, P., Niebel, T., Ohnemus, J., . . . Zaiser, H.
(2016). Arbeitsmarkt 2030: Digitalisierung der Arbeitswelt. Fachexpertisen zur Prognose
2016.
Eggenberger, C., Janssen, S., & Backes-Gellner, U. (2022). The value of specific skills under
shock: High risks and high returns. Labour Economics. Advance online publication.
https://doi.org/10.1016/j.labeco.2022.102187
Eggenberger, C., Rinawi, M., & Backes-Gellner, U. (2018). Occupational specificity: A new
measurement based on training curricula and its effect on labor market outcomes. Labour
Economics, 51, 97–107. https://doi.org/10.1016/j.labeco.2017.11.010
Fairlie, R. W., & Bahr, P. R. (2018). The effects of computers and acquired skills on earnings,
employment and college enrollment: Evidence from a field experiment and California UI
earnings records. Economics of Education Review, 63, 51–63.
https://doi.org/10.1016/j.econedurev.2018.01.004
Falck, O., Heimisch, A., & Wiederhold, S. (2021). Returns to ICT skills. Research Policy, 50.
Gentzkow, M., Kelly, B., & Taddy, M. (2019). Text as Data. Journal of Economic Literature,
57(3), 535–574. https://doi.org/10.1257/jel.20181020
Goetze, W., & Aksu, B. (2018). Anforderungsprofile: Die Methode. Thalwil. Retrieved from
http://www.anforderungsprofile.ch/index.cfm?action=act_getfile&doc_id=100053&
Goldin, C., & Katz, L. F. (1998). The Origins of Technology-Skill Complementarity.
Quarterly Journal of Economics, 113(3), 693–732.
https://doi.org/10.1162/003355398555720
Greene, J. A., Yu, S. B., & Copeland, D. Z. (2014). Measuring critical components of digital
literacy and their relationships with learning. Computers & Education, 76, 55–69.
https://doi.org/10.1016/j.compedu.2014.03.008
Grundke, R., Marcolin, L., Nguyen, T. L. B., & Squicciarini, M. (2018). Which skills for the
digital era? OECD Science, Technology and Industry Working Papers.
Hanushek, E. A., Schwerdt, G., Wiederhold, S., & Woessmann, L. (2015). Returns to skills
around the world: Evidence from PIAAC. European Economic Review, 73, 103–130.
https://doi.org/10.1016/j.euroecorev.2014.10.006
Hijzen, A., Upward, R., & Wright, P. W. (2010). The Income Losses of Displaced Workers.
The Journal of Human Resources, 45, 243–269. Retrieved from
http://www.jstor.org/stable/20648942

41

Jacobson, L. S., LaLonde, R. J., & Sullivan, D. G. (1993). Earnings Losses of Displaced
Workers. The American Economic Review, 83, 685–709. Retrieved from
http://www.jstor.org/stable/2117574
Janssen, S., & Mohrenweiser, J. (2018). The Shelf-Life of Incumbent Workers during
Accelarating Technological Change (IZA Working Paper).
Kambourov, G., & Manovskii, I. (2009). Occupational Specificity of Human Capital.
International Economic Review, 50(1), 63–115. https://doi.org/10.1111/j.14682354.2008.00524.x
Lazear, E. P. (1979). Why Is There Mandatory Retirement? Journal of Political Economy, 87,
1261–1284. Retrieved from http://www.jstor.org/stable/1833332
Lazear, E. P. (2009). Firm‐Specific Human Capital: A Skill‐Weights Approach. Journal of
Political Economy, 117(5), 914–940. https://doi.org/10.1086/648671
Levy, F., & Murnane, R. J. (1996). With What Skills Are Computers a Complement?
American Economic Review, 86, 258–262. Retrieved from
http://www.jstor.org/stable/2118133
Marsden, D. (1990). Institutions and labour mobility: occupational and internal labour
markets in Britain, France, Italy and West Germany. In Labour relations and economic
performance (pp. 414–438). Springer.
Neal, D. (1995). Industry-specific human capital: Evidence from displaced workers. Journal
of Labor Economics, 653–677.
Nizalova, O. Y., & Murtazashvili, I. (2016). Exogenous Treatment and Endogenous Factors:
Vanishing of Omitted Variable Bias on the Interaction Term. Journal of Econometric
Methods, 5(1), 1. https://doi.org/10.1515/jem-2013-0012
OECD (2016a). New skills for the digital economy: measuring the demand and supply of ICT
skills at work. Paris. https://doi.org/10.1787/5jlwnkm2fc9x-en
OECD (2016b). Skills for a digital world: Ministerial Meeting on the Digital Economy
Background Report.
Oosterbeek, H., & Ponce, J. (2011). The impact of computer use on earnings in a developing
country: Evidence from Ecuador. Labour Economics, 18(4), 434–440.
https://doi.org/10.1016/j.labeco.2010.11.002
Schultheiss, T., & Backes-Gellner, U. (2021). Different degrees of skill obsolescence across
hard and soft skills and the role of lifelong learning for labor market outcomes (Working
Paper).
Siddiq, F., Scherer, R., & Tondeur, J. (2016). Teachers' emphasis on developing students'
digital information and communication skills (TEDDICS): A new construct in 21st century
education. Computers & Education, 92-93, 1–14.
https://doi.org/10.1016/j.compedu.2015.10.006
Stalder, B. E. (2011). Das intellektuelle Anforderungsniveau beruflicher Grundbildungen in
der Schweiz. Ratings der Jahre 1999‐2005. Institut für Soziologie der Universität
Basel/TREE.
Sullivan, P. (2010). Empirical Evidence on Occupation and Industry Specific Human Capital.
Labour Economics, 17(3), 567–580. https://doi.org/10.1016/j.labeco.2009.11.003
Tambe, P. (2021). The Growing Importance of Algorithmic Literacy (Working Paper).

42

Tambe, P., Ye, X., & Cappelli, P. (2020). Paying to Program? Engineering Brand and HighTech Wages. Management Science, 66(7), 3010–3028.
https://doi.org/10.1287/mnsc.2019.3343
Tate Twinam (2017). COMPLEMENTARITY AND IDENTIFICATION. Econometric
Theory, 33(5), 1154–1185. https://doi.org/10.1017/S0266466616000359
Topel, R. (1991). Specific Capital, Mobility, and Wages: Wages Rise with Job Seniority.
Journal of Political Economy, 99, 145–176. Retrieved from
http://www.jstor.org/stable/2937716
UN (2018). Building digital competencies to benefit from existing and emerging technologies,
with a special focus on gender and youth dimensions.
Weinberger, C. J. (2014). The Increasing Complementarity between Cognitive and Social
Skills. The Review of Economics and Statistics, 96(5), 849–861.
https://doi.org/10.1162/REST_a_00449

43

