Expertise∗
David Autor†and Neil Thompson‡
June 18, 2025
Abstract
Whenjobtasksareautomated, doesthisaugmentordiminishthevalueoflaborinthetasksthat
remain? We argue the answer depends on whether removing tasks raises or reduces the exper-
tise required for remaining non-automated tasks. Since the same task may be relatively expert
in one occupation and inexpert in another, automation can simultaneously replace experts in
some occupations while augmenting expertise in others. We propose a conceptual model of oc-
cupational task bundling that predicts that changing occupational expertise requirements have
countervailing wage and employment effects: automation that decreases expertise requirements
reduces wages but permits the entry of less expert workers; automation that raises requirements
raises wages but reduces the set of qualified workers. We develop a novel, content-agnostic
method for measuring job task expertise, and we use it to quantify changes in occupational ex-
pertise demands over four decades attributable to job task removal and addition. We document
that automation has raised wages and reduced employment in occupations where it eliminated
inexpert tasks, but lowered wages and increased employment in occupations where it eliminated
expert tasks. These effects are distinct from—and in the case of employment, opposite to—the
effects of changing task quantities. The expertise framework resolves the puzzle of why routine
task automation has lowered employment but often raised wages in routine task-intensive oc-
cupations. It provides a general tool for analyzing how task automation and new task creation
reshape the scarcity value of human expertise within and across occupations.
JEL codes: E24, J11, J23, J24
Keywords: Expertise, Skills, Tasks, Technological Change, Automation, Augmentation, Artifi-
cial Intelligence, Labor Demand
∗Joseph R. Schumpeter lecture, presented to the European Economic Association on August 29, 2024 in Rotterdam,
withlecturetitle“DoesAutomationReplaceExpertsorComplementExpertise? TheAnswerisYes.” WethankDaron
Acemoglu, ErikBrynjolfsson, MatthiasDoepke, MartinFleming, JoshuaGans, AntonKorinek, SendhilMullainathan,
Ashesh Rambachan, Pascual Restrepo, Anna Salomons, and numerous seminar participants for valuable comments
that improved the paper. We are deeply indebted to Lucy Hampton, Joanne Liang, Ragini Srinivasan, Christian Vogt,
and Can Yeşildere for exceptional research assistance, and to Fredric Kong for expert review of the theoretical model.
Autor acknowledges research support from the Hewlett Foundation, the Google Technology and Society Visiting
Fellows Program, the NOMIS Foundation, the Schmidt Sciences AI2050 Fellowship, and the Smith Richardson
Foundation. Thompson acknowledges research support from Open Philanthropy.
†Massachusetts Institute of Technology and NBER.
‡Massachusetts Institute of Technology FutureTech, CSAIL and Initiative on the Digital Economy1 Introduction
Consider two occupations that were extensively transformed by computerization over the last forty
years: Accounting Clerks and Stock and Inventory Clerks. Many of the core activities of the
first occupation, accounting clerks, involved executing routine codifiable procedures (tasks) such as
recording transactions, reconciling bank statements, identifying discrepancies, and compiling tables
and graphs. As computers became cheap, powerful, and ubiquitous, these tasks were increasingly
translated into computer code and automated. The second occupation, inventory clerks, likewise
performed many routine tasks, such as examining stock to verify conformance to specifications,
compiling periodic, special, or perpetual inventories, and computing prices. These tasks were also
ripe for computerization. Should we expect the occupations of accounting clerks and inventory
clerks to be similarly affected by their exposure to automation?
Three stands of literature suggest that the answer is yes. The traditional human capital view
implies a law of one price for skill: skills used in similar activities should be equally rewarded. A
reduction in demand for the skills used to perform now-automated routine, codifiable tasks should
similarly affect accounting clerks and inventory clerks, likely by reducing wages (Katz and Murphy,
1992). The contemporary task model makes a sharper prediction (Autor et al., 2003; Acemoglu
and Autor, 2011; Acemoglu and Restrepo, 2018a; Acemoglu et al., 2024): workers who performed
newly-automated tasks will lose ‘labor share’ (a share in output), which all else equal, will lower
their wages. This displacement effect may be partially offset by higher productivity, meaning that
the net wage impact is ambiguous. Regardless, a clear prediction is that workers whose routine
labor tasks are displaced by automation will be similarly affected (negatively or positively). A
third strand of literature anticipates, albeit with less theoretical formalism, that occupations that
have a substantial share of their tasks exposed to automation (i.e., potentially subject) will likely
see falling demand, implying lower wages (Frey and Osborne, 2017; Muro et al., 2019; Webb, 2020;
Abrahams and Levy, 2024; Eloundou et al., 2024; Manning, 2024). As with the task model, worker-
level impacts are captured by their automation exposure, suggesting again that accounting clerks
and inventory clerks should be similarly affected.
This paper makes a distinctly different set of predictions. Our conceptual model, which we refer to
as an ‘expertise’ framework, makes two sets of predictions: (1) wages and employment of accounting
clerks will move in the opposite direction from wages and employment of inventory clerks; and (2)
wages and employment will move in opposite directions within each occupation—specifically, wages
of accounting clerks will rise and their employment will fall, while wages of inventory clerks will
fall while their employment will rise. (In all cases, changes in wages and employment in each
occupation are relative to the economy-wide average.) Our model makes distinct predictions for
these occupations because, despite their shared automation exposure, they differ in the tasks that
are not exposed to automation. Alongside their automatable routine tasks, core accounting tasks
includenumerousnon-automatableproblem-solvinganddecision-makingtasksrequiringspecialized
knowledge and training (what we term expertise). Conversely, most of the non-automatable tasks
1of inventory clerks, such as counting, stocking, and weighing inventory, are relatively inexpert,
requiring less training and certification than their automatable tasks. Under the key assumption,
discussed next, that remaining non-automatable tasks of accounting clerks and inventory clerks
must still be performed by workers in those occupations, we anticipate that routine task-replacing
automation will raise expertise demands in the accounting clerk occupation and lower them in the
inventory clerk occupation.
Our expertise framework is built on two pillars that are absent from (or back-grounded by) the
human capital, task, and ‘exposure’ models: expertise and indivisibility. By expertise, we refer to a
worker’s capability (AKA, skill, human capital, know-how) to perform specific tasks, e.g., entering
data in a ledger, or checking physical inventory against accounting data. Task-specific expertise
commands a wage premium but also serves as a barrier to entry: workers lacking the expertise
to perform a task cannot enter an occupation that requires it. Not all tasks require expertise,
however. We assume that effectively all workers can perform generic, physical and cognitive tasks
requiringnoformaltrainingorcertification, suchasboxinglightweightitemsorgreetingcustomers.1
Our stylized model assumes that expertise requirements can be ranked from least to most expert
along a single dimension, as in Garicano (2000); Garicano and Rossi-Hansberg (2006). While
unidimensionality makes our model tractable, what is essential is that expertise is hierarchical:
workers of a given expertise level can perform all tasks at or below their expertise level, but cannot
perform tasks above their expertise level.2 A higher-expertise worker can therefore always compete
with a lower-expertise work to perform any labor-using task, but the opposite is not true.
The second buildingblock ofthemodel is task bundling withinoccupations. All tasks bundled in an
occupation must be performed by each worker in that occupation, but expertise requirements differ
among the tasks bundled in an occupation: some will be the occupation’s expert tasks—the most
specialized, presumably requiring the most training or certification—and others will constitute the
occupation’s inexpert tasks. We do not model why tasks of different expertise levels are bundled in
occupations, but we believe this is self-evidently plausible and is likely explained by communication
frictions or proximity requirements (physical or temporal) that make bundling more efficient than
un-bundling (Becker and Murphy, 1992; Dessein and Santos, 2006). For example, most professional
workers retain receipts and file reimbursement claims for travel expenses. This is a supporting
task—there is no profession dedicated to receipt management—but it is a difficult task to fully
delegate since only the traveler knows why the expense was incurred.
The assumption of occupational task bundling represents a key departure from canonical task
models, which assume atomistic task assignment. In those models, comparative advantage ensures
that no two skill groups perform the same task in equilibrium (see Acemoglu and Autor (2011);
Acemoglu et al. (2024)). By contrast, under occupational task bundling, a given task is often
1Performing these tasks requires sophisticated human capabilities that are, even now, at the frontier of automation
(Svanberg et al., 2024). Because most adults require almost no training or certification to perform these tasks,
however, we label these tasks as generic.
2In higher dimensions this requires a partial ordering (Kwong, 2024).
2performed across multiple occupations—but by different skill (or expertise) groups. This arises
because occupations comprise a range of tasks requiring varying levels of expertise, and each worker
must have sufficient expertise to perform all non-automated tasks in their occupation.
As with contemporary task models (Autor et al., 2003; Acemoglu and Autor, 2011; Acemoglu and
Restrepo, 2018a,b), automation in our model corresponds to the case when tasks are reallocated
from labor to capital due to advancing automation. Distinct from the task model, automation
in the expertise model is not merely labor-saving, it is also expertise-displacing. Once a task is
automated, the relevant task expertise is no longer needed anywhere in the economy. Because
expertise differs among tasks bundled in an occupation, automation of any given task within an
occupation might either raise or lower the average expertise level of the set of labor-using tasks
that remain. When automation takes over an expert task within an occupation, the the relevant
task-specific worker expertise is no longer required, so less expert workers can enter the occupation.
We now return to the question of how task automation may differentially affect wages and employ-
ment in the accounting clerk and inventory clerk occupations. Here, the expertise framework makes
a set of sharp and (we believe) novel predictions. Because automation eliminates primarily expert
tasksintheinventoryclerkoccupation—forinstance, flaggingwhenitemsarebelowthegovernment
support price—our framework predicts that required expertise and hence relative wages in that oc-
cupation will decline. Conversely, as automation eliminates mostly inexpert tasks of accounting
clerks—for instance, some basic bookkeeping tasks—workers in that occupation will primarily en-
gage in more expert problem-solving tasks. Wages will rise, reflecting higher productivity in the
occupation and hence greater scarcity of the required expertise.
The expertise framework further predicts countervailing and opposite signed effects on employment.
Automation of an occupation’s formerly expertise-demanding tasks spurs a labor supply response:
the entry of new, less-expert workers. This is because the fall in expertise requirements enlarges
the set of workers eligible to perform the occupation’s remaining tasks. Conversely, rising exper-
tise requirements in the accounting clerk occupation will reduce the set of workers qualified to do
the work, so relative employment of accounting clerks will decline even as wages rise. Intuitively,
changes in occupational expertise requirements operate like shifts in the labor supply curve: task
automation that reduce occupational expertise requirements expands the effective supply of quali-
fied labor; task automation that raise occupational expertise requirements reduces the effective of
supply of qualified labor.3
Section 2 of the paper formalizes these ideas—expertise and indivisibility—in a stylized general
equilibrium model that makes precise the intuitive predictions discussed above. The remainder of
the paper tests these ideas empirically. Section 3 introduces two novel empirical tools built for
3One might hypothesize that relative employment of accounting clerks will decline not because expertise supply is
constrained but because rising productivity saturates demand for this occupation’s output. This does not occur in
our model because the elasticity of occupational demand is assumed to exceed one. But we acknowledge this as a
plausible alternative interpretation.
3these tests. The first is a content-agnostic measure of the ‘expertise’ required to perform each of
the tasks that comprises an occupation, where by content-agnostic, we mean that the measure is
not based on the meaning of the words in the task description. Our task expertise measure is
rooted in the Efficient Coding Hypothesis (ECH), which we detail in Section 3. In brief, the ECH
implies that we can identify words with high expertise content as those that, in common usage,
have low frequency of occurrence and low entropy conditional on occurring—meaning that where
an uncommon word is used, its domain origin (e.g., engineering, ornithology, plumbing, masonry)
is relatively predictable. This content-agnostic measure, calculated from a conventional word fre-
quency guide used by educators (Zeno et al., 1995), enables us to rank occupations by the average
expertise level of their constituent tasks and, moreover, to test (and confirm) as hypothesized that
expertise has significant (positive) predictive power for occupational wage levels.
Our second empirical step identifies the job tasks that have been removed from and added to
each occupation between 1977 and 2018. This step is made challenging by the fact that the
DOT and O*NET, produced four decades apart, almost invariably describe what appear to be the
same tasks using somewhat different words. To abstract from these nominal differences, we use
highdimensionalwordembeddings—geometricrepresentationsofsemanticcontent—tocharacterize
each task description in both time periods and calculate the Euclidean distance in embedding space
between all possible 1977 vs. 2018 tasks pairs. Applying a threshold cutoff value to this distance
measure,wepartitiontasksintothreegroups: thoseremoved,retained,andaddedbetween1977and
2018. We can thus measure the evolving expertise requirements of each occupation by comparing
the expertise of tasks added and removed to the tasks initially present.
Section 4 tests the wage implications of the expertise framework. We combine the occupational
expertise and task change measures with representative data, sourced from Autor et al. (2024), on
wages and employment in 303 harmonized three-digit U.S. Census and ACS occupations covering
U.S. civilian employment in 1980 and 2018. Our first finding is that changes in occupational
expertise, stemming from both the removal and addition of occupational tasks, strongly predict
changes in occupational wages. Moreover, the expertise requirements of tasks removed from or
added to an occupation affect wage levels independently of the quantity of tasks added or removed
present. Remarkably, both the removal of expert tasks and the addition of inexpert tasks predict
relative wage declines in an occupation, while, conversely both the removal of inexpert tasks and
the addition of expert tasks predict occupational wage gains.4
Consistent with recent findings on the importance of task quantities, we confirm that net changes
in the set of tasks performed by an occupation predict occupational wage changes (Acemoglu and
Restrepo,2018b,2022;Autoretal.,2024). Occupationsthatgaintasksexhibitwagegrowth, though
occupations that lose tasks do not exhibit wages declines. Changes in occupational task quantities
and task expertise are only weakly correlated, so each measure has independent explanatory power.
4In all cases, a task is labeled relatively expert or inexpert for a given occupation by comparison to the occupation’s
expertise level at the beginning of the sample, reflecting the idea that any given task may be expert for some
occupations and merely inexpert (supporting) for others.
4This result suggests that the economic content of task quantity change and expertise change are
distinct, even though both are realized through task removal and task addition.
Section 5 confirms this supposition. Our model makes the counterintuitive prediction that occupa-
tions with increasing expertise requirements will have falling employment (alongside rising wages),
while occupations with declining expertise requirements will have rising employment (alongside
falling wages). The data robustly confirm this prediction. Consistent with our running example
above, for example, we find that between 1980 and 2018, accounting clerks saw substantial employ-
ment declines (alongside substantial wage increases), while inventory clerks workers experienced
the opposite. Crucially, we find the opposite pattern for changes in task quantities. Occupations
that gain tasks expand and those that lose tasks contract. We underscore that the countervailing
employment effects of expertise change and task change on are opposite to the pattern for wages,
where increases in both task quantities and task expertise predict wage increases.
The contrasting employment relationships between rising task expertise (falling employment) and
rising task count (rising employment) suggests a fundamental difference between task quantity and
task expertise changes: a task quantity change acts like a demand shift, increasing or decreasing
the amount of work performed by an occupation; a task expertise change operates like a shift in
the labor supply curve, reducing or expanding the set of workers qualified to perform the work.
The final empirical section of the paper, Section 6, applies the expertise framework to reanalyze the
impacts of routine task-replacing automation on occupational wages. Consistent with the original
task framework in Autor et al. (2003), much evidence confirms that employment in routine task-
intensive occupations has substantially contracted in industrialized countries over the last four
decades as automation has proceeded (Goos and Manning, 2007; Autor et al., 2006, 2008; Goos
et al., 2009, 2014; Michaels et al., 2014). A longstanding puzzle remains, however: wages have
not consistently declined in routine task-intensive occupations despite reduced demand (Autor and
Dorn, 2013; Mishel et al., 2013; Green and Sand, 2015; Taber and Roys, 2019; Böhm, 2020; Böhm
et al., 2024). The expertise framework offers a novel, precise, and testable explanation. Because
routine tasks were relatively expert for a subset of occupations but were relatively inexpert for
another set, expertise requirements in routine task-intensive occupations did not uniformly rise or
fall as automation proceeded. Instead, they bifurcated, with expertise falling in the former group of
occupations and rising in the latter. The expertise framework accordingly predicts that routine task
automation should have had non-neutral wage effects: lowering wages in occupations where routine
tasks were expert and raising them in occupations where routine tasks were largely inexpert.
We test these implications by using the expertise level of routine tasks present in an occupation in
1977 to predict the change in expertise requirements during the subsequent four decades. Specif-
ically, we calculate the implied change in expertise in each occupation if hypothetically all of its
routine tasks were removed. This predictor proves powerful. Occupations that were exposed to
potential expertise loss due to routine task automation saw a fall in task expertise between 1977
and 2018 and a decline in wages. Conversely, occupations exposed to potential expertise gains due
5to routine task automation saw a rise in task expertise and wages. Moreover, the gradient between
expertise change and wage change is symmetric in these two sets of occupations, despite the fact
that some lose and others gain expertise. Consistent with our framework, occupations that were
predicted to see rising expertise demands due their routine task exposure saw falling relative em-
ployment, and those predicted to see rising expertise demands due to their routine task exposure
saw falling relative employment. We finally confirm that exposure to loss of routine task quantities
reduces occupational wages, as the task framework predicts, but that this operates independently
of the wage effects of loss or gains of expertise due to routine task removal.
Our paper complements recent studies that explore richer interactions between task automation
and occupational skills demands, including Lin (2011); Brynjolfsson and Mitchell (2017); Deming
(2021); Agrawal et al. (2023b,a); Autor et al. (2024); Aghion et al. (2024); Cavounidis et al. (2024);
Combemale et al. (2024); Lipowski et al. (2024), and Aghion et al. (2025). An innovative analysis
by Hampole et al. (2025) considers how the automation of a subset of occupational tasks affects
the productivity of workers in remaining occupational tasks. As with the expertise framework,
the Hampole et al. (2025) model implies that task automation may have non-monotone impacts
on occupational labor demand: if automation exposure varies across tasks within an occupation,
workers can reallocate effort from more to less exposed tasks to offset (in part or full) wage losses
from task displacement. A key innovation of the present paper is to distinguish between task
expertise exposure versus task quantity exposure. This yields the sharp prediction that whether
task automation raises of lowers occupational wages depends on the expertise of tasks removed
relative to those retained rather than the variance of task exposure per se.
Recent papers by Ide and Talamas (2024a,b) consider how new technologies, including AI, may
affect skill demands and wage levels building on the knowledge hierarchy framework introduced by
Garicano (2000) and developed in Garicano and Rossi-Hansberg (2006, 2015). As in our setting,
automation may have non-monotone wage impacts across occupations (‘workers’ vs. ‘solvers’), but
these effects are monotone along the knowledge hierarchy. As in our expertise framework, these
knowledgehierarchymodelsimplythatasingletechnology(AI,forexample)maycomplementmore
knowledgeable (expert) workers and reduce the wages of less knowledgeable workers.5 Our work
also builds on papers such as Violante (2002); Gathmann and Schönberg (2010); Acemoglu et al.
(2012); Huckfeldt (2022); Braxton and Taska (2023) that consider how scarce human expertise may
be rendered obsolete by technological advances. As a recent example, Kogan et al. (2024) present
a model and supporting evidence where new technology vintages erode the value of existing worker
expertise, particularly among older and higher-paid workers.
A key building block of our model is a strict expertise hierarchy, in which more expert workers com-
pete with less expert workers but not vice-versa. This assumption parallels a finding in Acemoglu
and Restrepo (2022). Studying the wage impacts of routine task-replacing automation, their paper
5Recent papers also consider macroeconomic implications of task automation, including Aghion et al. (2018); Korinek
and Stiglitz (2018); Brynjolfsson et al. (2021); Korinek and Juelfs (2022); Jones and Liu (2024); Acemoglu (2025).
We do not develop the macroeconomic implications of the expertise framework here.
6estimates the substitutability of task capabilities across detailed demographic groups, thus allowing
the automation of one demographic group’s tasks to create spillovers (‘ripples’) onto other closely
substitutable groups. Their results suggest that workers displaced from routine task-intensive occu-
pations primarily create downward wage pressure on wages of less-educated workers. Our model’s
assumption that competition among experts is hierarchical embodies (in stark form) this result.
The next section of the paper presents the formal expertise model. Section 3 develops our exper-
tise and task removal/addition measures, while Sections 4 and 5 test the expertise model’s main
predictions for wages and employment. Section 6 presents a causal test of the model’s predictions
by focusing on routine task-replacing automation. Section 7 concludes.
2 Replacing experts and augmenting expertise: A model of ex-
pertise and automation
This section develops a model of expertise and task automation based on three notions sketched
in the Introduction. A first is expertise, which define as a worker’s capability to perform specific
tasks, wheretasksarerankedbytheirexpertiserequirements. Expertiseishierarchical: moreexpert
workers can perform all tasks that less expert workers can perform, but the reverse is not true.
The second feature is bundling: occupations bundle a range of tasks of different expertise levels.
Workers must perform all non-automated tasks in an occupation, so entry into each occupation is
limited to workers capable of performing its most expert task. All occupations additionally contain
a measure of generic, labor-using tasks that are not subject to automation, require no expertise,
and hence can be performed by any worker. The third feature is automation, which, over time,
enables capital to perform an increasing range of expert tasks. Distinct from canonical task models,
automation of expert tasks affects labor demand through three channels. The first two are familiar:
automation displaces labor from the newly-automated task; and it increases productivity of workers
in remaining tasks. In the expertise model, automation has a third effect: it renders redundant
the expertise that was formerly required to perform now-automated tasks. This enables less expert
workers to enter occupations where this expertise requirement served as a barrier, raising wages of
entrants but lowering wages of incumbents.
Using the model’s general equilibrium structure, we show how automation simultaneously replaces
experts and augments expertise. Automation raises productivity and wages of occupational incum-
bents by performing their relatively inexpert tasks at reduced cost. Simultaneously, each increment
to automation renders one formerly expert occupation inexpert—that is, all of its expert tasks are
automated—so any worker can perform its remaining generic tasks. Employment initially rises in
occupations as they become inexpert, owing to the elimination of expertise requirements. Entry
causes wages in newly inexpert occupations to fall to the level of all other inexpert occupations.
As automation proceeds further, employment in these occupations slowly contracts because pro-
ductivity is higher in occupations that have become inexpert more recently (i.e., are less obsolete).
Automation is always output-increasing in the model but never Pareto-improving. Whether a
7worker of given expertise gains or loses as automation advances depends on the net effect of the
competing forces of capital-labor complementary and capital-expertise substitution.
The model’s formal structure is as follows. There is a single final consumption good, produced as
a CES aggregate of the outputs of a continuum of occupations. Each occupation is comprised of
a set of tasks that must be performed to generate the occupational output. No two occupations
are identical, and each can be uniquely identified by the most expert task it requires. Workers of
differing expertise levels choose occupations to maximize their incomes. A task-level production
function specifies the capital, labor, and expertise required to perform each task as a function of the
state of automation. Workers cannot produce output in occupations that require them to perform
tasks for which they lack expertise. Once an expert task is automated, however, this barrier is
eliminated since the task can now be completed using capital.
Our presentation of the model proceeds from micro to macro. We start with the task-level pro-
duction. We next specify what workers can produce in each occupation as a function of their own
expertise and the state of automation, and we define how these worker-level outputs are aggregated
to occupation level outputs. Finally, we introduce the aggregate production structure, solve for the
unique allocations of labor and capital to each occupation in general equilibrium, and derive the
output prices, wage levels, and capital rental rate that support this equilibrium.
2.1 Task level production: Capital, labor, and expertise
We conceptualize production as a process of combining heterogeneous tasks, differentiated by their
susceptibility to automation and the human expertise required for their completion. There is a
measure 1 + θ of tasks t∈(−θ,1) that are performed within occupations, with θ≥0.
There is a measure¯
L of workers uniformly distributed over a unit measure of expertise types
e∈(0,1). We denote the set of all workers by W and adopt the convention of referring to a worker
i∈W with expertise ei.
Assumption 1. Hierarchical expertise. Denoting a worker i′s expertise as ei, the structure of
expertise is such that i is able to complete task t if and only if ei ≥t.
The hierarchical expertise assumption formalizes the notion that workers can perform any task at
or below their expertise level but not those above it. By implication, the measure of workers who
can perform task t′is strictly greater than the measure who can perform task t′′if 1 ≥t′′>t′>0.
This is true despite the fact that expertise e is distributed uniformly on (0,1).
Assumption 2. Hierarchical automation. We say that a task is automated if it can be completed
by capital. The state of automation is given by I ∈(0,1), and determines the subset t ∈(0,I] of
tasks that are automated. An advance in automation corresponds to a rise in I.
Remark 1. The general structure of the model admits automation of tasks in any order. Our
chosen parameterization captures the notion that automation encroaches on increasingly specialized
(i.e., expert) human capabilities.
8If a task t is produced using labor, we define its production function as:
xL(t,ℓi(t)) =
  
ℓi(t) if t∈(−θ,ei]
0 otherwise,
(1)
where ℓi(t) is labor supplied to task t by worker i. Analogously, if t is produced using capital, we
define its production function as
xK(t,κi(t)) =
  
ηκi(t) if t∈(0,I]
0 otherwise,
(2)
where κi(t) is capital allocated to worker iand supplied to task t, and η>1 measures the physical
productivity of capital relative to labor.
In equilibrium, automated tasks will be completed exclusively by capital, with all remaining tasks
completed by labor. We use this equilibrium condition to simplify the derivation, but provide and
prove the supporting conditions in Appendix A.1, along with proofs for all other theoretical results.
Accordingly, we may denote the quantity of task tproduced, either by i’s labor or capital allocated
to i, as
x(t,ℓi(t),κi(t)) =
  
xL(t,ℓi(t)) if t∈(−θ,0] ∪(I,1)
xK(t,κi(t)) if t∈(0,I].
Equations (1) and (2) distinguish among three categories of tasks:
1. Expert tasks: t∈(I,1), which require labor and can be completed only by workers i with
expertise ei ≥t.
2. Automated tasks: Formerlylabor-usingexperttasksint∈(0,I], which, duetoautomation,
are efficiently completed by capital.
3. Generic tasks: t ∈(−θ,0], which require labor but do not demand specific expertise and
hence can be performed by any worker.
2.2 What workers produce
There is a unit measure of occupations ϕ∈(0,1) that are characterized by the range of tasks they
combine in production. The total measure of tasks required in occupation ϕis T(ϕ) := ϕ+θ(1−ϕ),
which combines the measure of generic tasks T(ϕ)−ϕ= θ(1−ϕ), the measure of automated tasks
I(ϕ) := min{ϕ,I}, and the measure of expert tasks ϕ−I(ϕ). We assume that θ > 1 and explain
the role played by this restriction in Remark 2 below. Each worker can supply labor to only one
occupation. The following assumption stipulates the constraints that occupational task bundling
places on occupational production and on worker occupational choice:
9Assumption 3. Occupational task bundling. Production in occupation ϕ requires the combi-
nation of tasks t∈[θ(ϕ−1),ϕ]. For a worker’s output to be non-zero in an occupation, she must
perform all of its non-automated tasks.
The assumption of occupational task bundling distinguishes the current model from canonical task
models, which feature atomistic task assignment (Acemoglu and Autor, 2011; Acemoglu et al.,
2024). Under atomistic task assignment, comparative advantage dictates that no two skill groups
perform the same task in equilibrium. Under occupational task bundling, the same task is generally
performed in many occupations, but the skill (expertise) group that performs that task generally
differs across occupations. This is because occupations contain a range of tasks of varying ex-
pertise, and each worker in an occupation must possess sufficient expertise to perform all of its
non-automated tasks.
Figure 1: The Space of Tasks and Occupations: Expert, Automated, and Generic Tasks
Performed in each Occupation ϕ at Current State of Automation I0
Task (t)
1
Expert
Automated
t′′
h
I0
t′
h
tasks in ϕ′′
ϕ′ ϕ′′
Occupation (ϕ)
0 1
t′′
l
tasks in ϕ′
Generic
t′
l
−θ
Note. For a given occupation on the horizontal axis, the vertical range of the polygon corresponds to the tasks
required for production.
Figure 1 depicts the resulting space of tasks and occupations. Occupations are ordered by expertise
requirements on the horizontal axis. Tasks are ordered by type (generic and expert) on the vertical
axis, with expert tasks ranked in ascending order of required expertise. The current state of
10ℓi(t)dt.
automation corresponds to the dashed line labeled I0.
Two example occupations, ϕ′, ϕ′′ are plotted for illustration. All expert tasks in occupation ϕ′ lie
below I0: these tasks have been automated. Occupation ϕ′ is therefore inexpert at the current
state of automation. The remaining labor-using tasks in ϕ′are generic, falling in the interval [t′
l,0].
Any worker may perform occupation ϕ′, though in equilibrium, only workers whose expertise is
technologically obsolete ei ≤I0 will choose to do so.
The second plotted occupation, ϕ′′, is partially automated. All workers in ϕ′′ perform tasks on
the intervals [t′′
l,0] ∪(I0,t′′
h], where the first interval comprises generic tasks and the second expert
tasks. Only a subset of the formerly expert tasks in ϕ′′, those in (0,I0], are automated, so ϕ′′ is
expertise-demanding at the current state of automation. A worker must have expertise ei ≥ϕ′′to
perform occupation ϕ′′. In equilibrium, only workers with ei = ϕ′′will choose to do so.
Each worker i possesses a total mass of 1 efficiency unit of labor that she supplies to the highest-
paying occupation for which she is qualified. A worker cannot subdivide her labor across occupa-
tions (Assumption 3) but can subdivide it across the non-automated tasks in an occupation ϕsuch
that:
1 =
0
θ(ϕ−1)
ℓi(t)dt+
ϕ
I(ϕ)
Similarly, ki, the total mass of capital allocated to worker i in occupation ϕ, is subdivided among
automated tasks such that:
ki =
I(ϕ)
0
The worker-level output yi(ϕ) for worker iequipped with ki units of capital in occupation ϕis given
by a Cobb-Douglas production function:
yi(ϕ) = T(ϕ) exp
ϕ
θ(ϕ−1)
ln x(t,κi(t),ℓi(t))
T(ϕ) dt (3)
The normalization by T(ϕ) ensures that yi(ϕ) is determined by the factor shares in occupation ϕ,
rather than the absolute measure of tasks. Substituting the task-level production function from
expressions (1) and (2) into the worker-level production function, (log) output is the sum of the
contributions by each of the three categories of tasks:
ln yi(ϕ)
T(ϕ)
= T(ϕ)−1
     
0
I(ϕ)
ϕ
ln(ℓi(t))dt
θ(ϕ−1)
+
ln(κi(t)η)dt
0
+
ln(ℓi(t)1{ei ≥t})dt
I(ϕ)
Generic Tasks
Automated Tasks
Expert Tasks
     
(4)
Let Ei := max{ei,I}. The third summand in equation (4) shows that yi(ϕ) = 0 if ϕ > Ei. This
implies that a worker i can be productively employed only in occupations ϕ≤Ei. We refer to Ei
as the effective expertise of worker i. It is through this quantity that automation may relax the
κi(t) dt.
11expertise requirements of an occupation.
A crucial feature of this setup, following from Assumption 3, is that the tasks bundled in an
occupation are inseparable: for a worker’s output to be non-zero, she must possess sufficient ex-
pertise to complete all tasks requiring labor in her occupation. Further, conditional on ϕ≤Ei, the
worker’s output yi(ϕ) is independent of ei. Stated differently, any two workers i and j who satisfy
the expertise requirements of occupation ϕ will achieve identical output levels in that occupation,
yi(ϕ) = yj(ϕ).
Given the Cobb-Douglas structure in equation (3), an income-maximizing worker will allocate her
labor uniformly across the non-automated tasks (both expert and generic) in her chosen occupation
ϕ, and similarly, cost minimization dictates that capital is uniformly allocated across automated
tasks, so that:
ℓi(t) =
  
1
T(ϕ)−I(ϕ) , if t∈[θ(ϕ−1),0] ∪(I(ϕ),ϕ]
0, otherwise
and
I(ϕ)
T(ϕ)
κi(t) =
  
ki
I(ϕ) , if t∈(0,I(ϕ)]
0, otherwise
Substituting these allocations back into the task-level production function (4) yields the maximized
output of worker i in occupation ϕ:
yi(ϕ) = T(ϕ)
T(ϕ)−I(ϕ)
T(ϕ)−I(ϕ)
T(ϕ) T(ϕ)kiη
I(ϕ)
=
1
1−α(ϕ)
1−α(ϕ) kiη
α(ϕ)
α(ϕ)
(5)
The Cobb-Douglas structure implies that the capital share in occupation ϕ is:
α(ϕ) := I(ϕ)/T(ϕ) = min{ϕ,I}
θ(1−ϕ) + ϕ
Remark 2. The parameter θ governs the capital share at each level of ϕ. The restriction θ > 1
means that this share is increasing in ϕ for all ϕ∈(0,1). Accordingly, more expert occupations are
more sensitive to the productivity of capital, η.
2.3 What occupations produce
Wenowaggregate worker-level production to the occupation level. We assume that capital is rented
to occupations at a competitive market rate r > 0 and allocated efficiently to workers employed
in that occupation. Let K(ϕ) ∈R+ denote the capital stock available to occupation ϕ, and let
L(ϕ) ∈R+ be the measure of workers employed in occupation ϕ. Denote by o : W →(0,1)
the function that maps workers to their occupational choices. The capital allocated to workers in
12occupation ϕ sums to the occupation’s capital stock:6
kidµ= K(ϕ), (6)
i∈o−1(ϕ)
while worker-level outputs in each occupation ϕ aggregate linearly to total occupational output
Y(ϕ):
Y(ϕ) =
i∈o−1(ϕ)
yi(ϕ)dµ.
Since α(ϕ) <1, returns to capital used by individual workers are diminishing. Hence, maximizing
Y(ϕ) subject to (6) requires capital to be uniformly distributed across workers in that occupation.
The implied level of capital per worker is ki = K(ϕ)/L(ϕ) for all workers iemployed in occupation
ϕ.
Substituting this optimal labor and capital allocation into the occupation-level production function
yields maximized output in occupation ϕ:
Y(ϕ) = L(ϕ)
1−α(ϕ)
1−α(ϕ) K(ϕ)η
α(ϕ)
α(ϕ)
(7)
Linear aggregation ensures that the Cobb-Douglas form reemerges at the occupation level and can
be written compactly as:
Y(ϕ) = A(ϕ)L(ϕ)1−α(ϕ)K(ϕ)α(ϕ)
where the occupation-specific total factor productivity (TFP) term is:
A(ϕ) := 1
1−α(ϕ)
1−α(ϕ) η
α(ϕ)
α(ϕ)
The supply of labor and capital to occupations
Let g(e,ϕ) denote the joint density of workers with expertise e in occupation ϕ. Since the total
measure of workers supplied is¯
L= µ(W), we have:
¯
L=
1
0
1
0
g(e,ϕ)dedϕ=
1
0
L(ϕ)dϕ
Assumption 4. Fixed capital stock. The aggregate capital stock denoted by¯
K ∈R+ is fixed,
6The measure µ in equation (6) and subsequent equations is the Lebesgue measure on W. We use that W can be
¯
written as W = (0,1) ×(0,
L) where the first dimension corresponds to workers’ expertise types and the second is a
continuous index running from 0 to¯
L, the measure of workers of each expertise type.
13so that total capital usage across occupations satisfies:
¯
K=
1
0
K(ϕ)dϕ
With an elastic capital stock, average wages will generally rise as new technologies are adopted
(Caselli and Manning, 2019). With a fixed capital stock this result is not automatic. We therefore
derive in Proposition 1 the productivity criterion that the automation technology must satisfy to
raise wages in occupations that are not fully automated. As is standard, we also assume that the
supply of labor (and hence expertise) is fixed.
Markets for both capital and labor are competitive. Capital is homogeneous, so that the rate of
return rmust be equalized across occupations. Given the heterogeneity of worker expertise and the
varying expertise demands across occupations, there is in general no single wage for all labor. As
established above, all workers in an occupation are equally productive, provided they have sufficient
expertise to perform the occupation’s non-automated tasks. Therefore, a worker’s wage depends
solely on the chosen occupation ϕ. A worker of expertise ei and effective expertise Ei = max{ei,I}
will thus choose an occupation ϕ that maximizes income:
o(i) = arg max ϕ≤Ei
w(ϕ)
The demand for labor and capital in occupations
Let p(ϕ) denote the price of Y(ϕ). Each occupation minimizes its production costs, taking factor
prices r and w(ϕ) as given. The first-order conditions for cost minimization yield the standard
Cobb-Douglas demand functions for occupation-level labor and capital:
L∗(ϕ) = 1−α(ϕ)
w(ϕ) Y(ϕ)p(ϕ) (8)
K∗(ϕ) = α(ϕ)
Y(ϕ)p(ϕ) (9)
r
2.4 General equilibrium
This section describes the general equilibrium of the model. Occupational outputs are combined
with a CES production function to create the final consumption good Y,
λ
Y=
1
Y(ϕ)λ−1
0
λ dϕ
, (10)
λ−1
14where λ is the elasticity of substitution between occupation-level inputs. We set the price of the
aggregate good, P, to unity as the numeraire.
Assumption 5. All occupations are gross-substitutes in final good production, that is λ > 1,
meaning that an increase in the productivity of an occupation raises that occupation’s share in total
output.
This assumption rules out the case where automation-induced occupational productivity gains
reduce the marginal revenue product of workers in the occupation. Adopting this assumption
places in stark relief the key subsequent result in Proposition 3 that productive automation of
expert tasks may nevertheless lower wages of experts.
Competitive markets
Many firms compete in each occupation. Competitive supply of occupation-level outputs and
constant returns to scale production technologies impose a zero-profit condition. Using factor
demands (8) and (9), the cost of production in occupation ϕ can be expressed as:
C∗(ϕ) = w(ϕ) L∗(ϕ)
1−α(ϕ)
Setting revenue equal to cost and using the cost-minimizing capital-labor ratio, we can derive the
supply price of Y(ϕ):
p(ϕ) = w(ϕ)1−α(ϕ) (r/η)α(ϕ)
Expression (10) allows us to derive the demand for Y(ϕ) as a share of aggregate demand Y:
1
p(ϕ) = Y(ϕ)
Y
−
λ
Clearing of occupation-level product markets implies the following equilibrium factor demands for
labor and capital in each occupation ϕ:
L(ϕ) = Y 1−α(ϕ)
w(ϕ) w(ϕ)1−α(ϕ) (r/η)α(ϕ) 1−λ
K(ϕ) = Y α(ϕ)
r
w(ϕ)1−α(ϕ) (r/η)α(ϕ) 1−λ
, (11)
. (12)
The worker optimization problem pins down the equilibrium distribution of labor across occupa-
tions. Each worker i chooses an occupation o(i) satisfying:
o(i) = arg max ϕ≤Ei
Y 1−α(ϕ)
L(ϕ) (r/η)α(ϕ)(1−λ)
. (13)
Since Ei ≥I for all workers i, all workers are capable of working in occupations with ϕ ≤I, i.e.,
in inexpert occupations. Workers with expertise ei ≤I are qualified to work only in inexpert
15
1
λ−α(ϕ)(λ−1)occupations—they lack sufficient expertise to enter expert occupations—but they can move freely
amongtheformer. Accordingly, wagesmustbeconstantacrossinexpertoccupations, andwedenote
this inexpert wage by wg := w(ϕ) for all ϕ≤I.
Inexpert occupations also serve as an outside option for workers with expertise ei > I. This is
because any worker employed in an expert occupation ϕ > I could instead move to an inexpert
occupation if it offered a higher wage. In equilibrium, therefore, the wage in any occupation cannot
be lower than the generic wage. More generally, any occupation ϕ′ ≤ϕ constitutes an outside
option for a worker choosing occupation ϕ. This implies that equilibrium wages must be weakly
increasing in the occupation index ϕ. This result is formalized in the following lemma which is
proved in the Appendix:
Lemma 1. In equilibrium, for any ϕ,ϕ′∈(0,1) such that ϕ>ϕ′, we have:
w(ϕ) ≥w(ϕ′).
Moreover, for any ϕ,ϕ′∈(0,I], we have:
ρ−1
w(ϕ) = w(ϕ′).
We additionally make the following assumption on the productivity of capital:
Assumption 6. Productive automation. Let ρ:= λ−1
λ and¯
I <1. Define
η:=
¯
¯
L
I
¯
K
1−
I exp
¯
−
I
¯
1−
I
¯
For all subsequent results, we assume that η>η and I ≤¯
I.
.
Under this assumption, Proposition 1 below establishes the existence and quasi-uniqueness of a
separating equilibrium, where separating refers to the property that the mapping from expertise
types ei to occupational choice o(i) is one-to-one on the domain (I,1). Specifically, workers i
with ei > I will choose the most expert occupation in which they can produce non-zero output,
i.e., o(i) = ei. Workers i with ei ≤I will be distributed across generic occupations such that
generic wages are equal. In brief, all workers who are not qualified to perform expert work pool in
generic occupations. Each worker who is qualified to perform expert work selects the most expert
occupation for which she is qualified. (Proof provided in Appendix A.1.)
Proposition 1. There exists an equilibrium in which for all workers i with ei >I:
o(i) = ei.
This equilibrium is unique up to reallocation of workers i with ei ≤I across occupations ϕ≤I that
respect Lemma 1.
16The resulting equilibrium factor prices are an immediate corollary:
Corollary 1. The equilibrium factor prices and outputs are the unique solution to the following
system of equations:
I¯
L
Y=
I
(1−α(ϕ))w(1−α(ϕ))(1−λ)−1
g (r/η)α(ϕ)(1−λ) dϕ (14)
0
¯
L
Y = (1−α(ϕ))w(ϕ)(1−α(ϕ))(1−λ)−1 (r/η)α(ϕ)(1−λ)
, ∀ϕ>I (15)
¯
K
Y=
I
α(ϕ)
w(1−α(ϕ))(1−λ)
g (r/η)α(ϕ)(1−λ)−1 dϕ (16)
0
+
1
w(ϕ)(1−α(ϕ))(1−λ) (r/η)α(ϕ)(1−λ)−1 dϕ
I
1 =
1
w(ϕ)(1−α(ϕ))(1−λ)(r/η)α(ϕ)(1−λ)dϕ (17)
0
η
α(ϕ)
η
(Proof provided in Appendix A.1.)
2.5 Results and implications
Figure 2 illustrates how advancing automation affects the wages of workers with differing levels
of expertise. The x-axis of this figure corresponds to the state of automation I, and the vertical
axis corresponds to the real wage and capital rental rate index. Real wages in occupations ϕ ∈
{0.2,0.4,0.6,0.8}are depicted in graduated shades of blue. The wage in inexpert occupations, wg,
is plotted in green, and the capital-rental rate, r, is plotted in red.
Themainresultdepictedinthisfigureisthatasmallexpansioninthesetofautomatedtasksreduces
the real wage in newly inexpert occupations but raises the wage in all other expert occupations.
Propositions 2 and 3 below state this implication formally.
Proposition 2. In general equilibrium, w(ϕ) has a jump discontinuity at ϕ= I. Specifically,
w(I) = wg < lim
ϕ→I+
w(ϕ).
Proposition 3. Let ϕ be an arbitrary occupation and let wϕ(I) denote the equilibrium wage w(ϕ)
in that occupation as function of the state of automation I. wϕ(I) is increasing on I ∈(0,
¯
I] with
the exception of a discontinuous drop at I= ϕ.
17Figure 2: Real Wages by Expertise Level, and Capital Rental Rate r,
in General Equilibrium as a Function of the State of Automation I
5
4
w(0.8)
w(0.6)
w(0.4)
w(0.2)
wg
3
r
2
1
0
0.1 0.2 0.3 0.4 0.5 0.6 0.7
I
Note. Parameter values:¯
L= 1,¯
K = 1, λ= 4, θ=
3
2 , η= 15.
Figure 2 also shows that wages wg in inexpert occupations increase as automation ascends the
expertise hierarchy, reflecting the fact that all occupations are q-complements in the production of
the final good (equation 10). Also visible is that the capital rental rate rises as automation expands
the task domain performed by a fixed quantity of capital.
The labor supply dynamics accompanying these wages changes are illustrated in Figure 3, which
plots the allocation of labor to occupations at selected values of ϕas a function of I. A small expan-
sion in the set of automated tasks raises employment in newly inexpert occupations. Employment
in remaining expert occupations stays constant in accordance with Proposition 1, and thus de-
clines relative to employment in newly inexpert occupations. This is formalized in the following
corollaries.
Corollary 2. In general equilibrium, L(ϕ) has a jump discontinuity at ϕ= I. Specifically,
L(I) >¯
L= lim
ϕ→I+
L(ϕ).
Corollary 3. Let ϕ be an arbitrary occupation and let Lϕ(I) denote the equilibrium quantity of
labor L(ϕ) employed in that occupation as function of the state of automation I. Lϕ(I) is constant
¯
on I ∈(0,ϕ] and decreasing on (ϕ,
I]. There is a discontinuous jump at I= ϕ, i.e.
Lϕ(ϕ) >¯
L= lim
I→ϕ−
Lϕ(I).
18Falling occupational expertise requirements therefore operate like outwards shifts in the labor sup-
ply curve: as expertise barriers to an occupation fall, its employment rises and its wage falls.
Further automation beyond this crossover point, however, gradually draws labor out of ϕ′and into
higher-ranked but also inexpert occupations, ϕ′′: ϕ′<ϕ′′≤I.
7
Figure 3: General Equilibrium Allocation of Labor to Selected Occupations as a Function of the
State of Automation I.
3
φ > I
φ = 0.6
φ = 0.4
φ = 0.2
2
L(φ)
1
0
0.1 0.2 0.3 0.4 0.5 0.6 0.7
I
Note. Parameter values:¯
L= 1,¯
K = 1, λ= 4, θ=
3
2 , η= 15.
Testable implications
Our conceptual model is illustrative but not directly estimable. The empirical sections that fol-
low instead evaluate the model’s first-order implications that follow from its three foundational
assumptions on expertise, inseparability, and automation. In mapping these implications to data,
we equate rising I in the model with changes in the expertise requirements of occupations, which
we measure empirically. When inexpert tasks are removed from an occupation, we equate this
to occupation becoming ‘more expert.’ When expert tasks are removed from an occupation, we
equate this with the occupation becoming less expert (‘more inexpert’), as defined above. Our
model does not consider the addition of new occupational tasks, but this is an important feature of
the data (Lin, 2011; Acemoglu and Restrepo, 2019; Autor et al., 2024). We treat task addition sym-
metrically to task removal: adding expert tasks to an occupation makes it ‘more expert’; adding
inexpert tasks to an occupation makes it ‘more inexpert’. Finally, our model does not directly
consider how changes in the quantity of tasks, rather than the expertise of tasks, performed by an
occupation affect labor demand. But changes in expertise demands occur through changes in task
7Because capital intensity α(ϕ) is increasing in ϕ, higher-ranked (higher ϕ) inexpert occupations will attract a larger
set of workers than lower-ranked inexpert occupations.
19quantities—specifically, through the expertise level of tasks removed and added. Our empirical
analysis thus jointly considers the effects of changes in task quantities and task expertise on wages
and employment.8 We test the following implications:
1. Occupations requiring greater expertise pay higher wages. While this implication is unsur-
prising, it is a necessary condition for the relevance of our framework. We test it in Section
3 and find robust evidence that occupational expertise plays a substantial role in wage deter-
mination, alongside education and broad occupational categories.
2. Themodelpredictsthatariseintheaverageexpertiselevelofanoccupation’staskbundlewill
yield an increase in wages and the opposite will occur if the bundle’s expertise requirements
fall.9 We test these implications in Section 4, and we further corroborate the symmetry of
this result: removing tasks raises wages if the tasks removed are inexpert and lowers them
if the tasks removed are expert; adding tasks raises wages if the tasks added are expert and
lowers them if the tasks added are inexpert. These implications are opposite to the case for
the canonical task model, where task addition always raises labor demand and where task
removal always lowers it. We empirically test the implications of both the expertise and task
models.
3. The model makes the counterintuitive prediction that reductions in occupational expertise
demands raise occupational employment, while increases in occupational expertise demand
fail to raise employment (and lower it relative to employment in newly-inexpert occupations).
We test these implications in Section 5.
4. The final empirical section of the paper (Section 6) causally tests these implications by as-
sessing whether changes in expertise demands caused by the removal of routine tasks—which
lowers expertise demands in some occupations and raises them in others—moves occupational
wages and employment in a manner consistent with the second and third implications above.
3 Measuring levels and changes in occupational expertise
This section describes our data and measurement, as summarized by the schematic in Figure 4.
8For wage and employment implications of task addition and removal, we draw on Acemoglu and Restrepo (2018a);
Acemoglu et al. (2024).
9We are implicitly mapping the maximum expertise required in an occupation, which is the relevant object in the
model, to the average expertise required in an occupation, which is the relevant object in the data.
20Figure 4: Overview of Data Sources and Data Construction
Dictionary of
Occupational
Titles (DOT)
1977
O* NET
2018
1. Harmonize tasks, identify tasks added and removed
Process job descriptions into tasks
- Split tasks
- Remove extraneous titles
M atching
Drop
- specializations
(e.g.
" may be
designated as" )
- green tasks
Educator's Word Frequency Guide (1995) M ap to embedding
space using OpenAI
text-embedding-3-small
2. M easure word expertise (XPT)
Dale-Chall List (1995)
- remove non-lemmas
- subtract from 100
Use Dale-Chall list to Winsorize
the SFI: top-code high-XPT words in
the Dale-Chall list and bottom-code
low-XPT words not in the list
lemma XPT
w1 x1
w2 x2
w3 x3
w4 x4
... ...
assign XPT to words not
in EWFG using closest
embeddings match
Classify
tasks as
routine, manual
and/ or
abstract
(GPT 4.1)
3. Aggregate to census occupation level
Occupation 1
Matched Added
T1 XPT1
T1 XPT1
T2 XPT2
T2 XPT2
... ...
... ...
Aggregate expertise to DOT/ O* NET
occupation level by taking average
Calculate expertise change
M ap O* NET/ DOT
occupations to census
occupations
Removed T1 XPT1
T2 XPT2
... ...
Google ngrams CPS 1971 OEWS 2018
Harmonized
census crosswalk
(Autor et al., 2024)
1980 census
ACS 2018
occ year routine XPT (?) ? XPT ? task Ln(wage) Ln(emp) share < HS educ ... broad occ
Chief executives 1980 0.01 0.57 0.009 0.02 3.03 10.77 0.06 ... Managers and executives
Chief executives 2018 0.004 0.80 .... ... 3.90 10.41 0.01 ... Managers and executives
... ... ... ... ... ... ... ... ... ...
213.1 A content-agnostic measure of occupational expertise
Our task expertise measure is rooted in the Efficient Coding Hypothesis (ECH), which originated in
sensory neuroscience (Barlow, 1961) but is now widely applied across information theory, cognitive
science, auditory science, and machine learning. The ECH explains why expert words emerge,
when they are used, and how they can be statistically identified without specific knowledge of their
semantic content.
At its foundation, the ECH observes that natural language speakers face a tradeoff when choosing
words to convey ideas between brevity (minimizing bandwidth utilization) and clarity (minimizing
miscommunication risk). To conserve bandwidth, a speaker can for example use a specialized
(‘expert’) word, such as elasticity, to convey the relationship between two variables. This usage is
efficient if the speaker is confident that the listener knows the term. If not, the information may not
be delivered. Alternatively, the speaker can employ commonplace terminology, e.g, “the percentage
change in one variable caused by the percentage change in another.” This phrase consumes more
bandwidth than elasticity, but it reduces the risk of misunderstanding because it conveys the
substantive content to the listener, independent of her knowledge of the word elasticity.10 The ECH
predicts, forexample, thatiftwoeconomistsmeetforthefirsttimeataprofessionalconference, they
will immediately employ expert terminology. Conversely, if two economists meet on an airplane,
they will initially employ commonplace terminology—until they discover their shared profession.
Both instances reflect efficient coding.
In distinguishing between commonplace and expert words, we underscore that the concepts en-
coded in commonplace words (e.g., profit, inflation) are neither trivial nor imprecise; they are
commonplace only because they are frequently encountered and discussed. Similarly, what distin-
guishes expert words (e.g., arbitrage, elasticity) from commonplace words is not their substantive
complexity—elasticity is arguably a less complex concept than inflation—but the frequency with
which laypeople encounter and discuss them.
The ECH provides an intuitive explanation for why domain experts develop and use specialized
language (AKA jargon). Social groups (e.g. professions, peer groups) that regularly encounter
concepts that are commonplace within their domain but uncommon outside their domain will
communicate efficiently by developing specialized words (such as arbitrage) that convey domain-
specific concepts (Cremer et al., 2007). Non-domain experts will typically be unfamiliar with these
words.11 This social learning process explains why, for example, phrases like Large Language Model
10More familiar to economists, Zipf’s Law observes that, in natural languages, word frequency follows a power law,
with the frequency of a words usage proportional to the inverse of its rank. Zipf’s Law can be interpreted as
an empirical manifestation of the ECH: reusing a small number of words with high frequency conveys the most
information with the least effort (Zipf, 1949).
11If generating and mastering new concepts and associated vocabulary were costless, the ECH would predict that
every known concept would have its own precise word and that every speaker would know that word. But the
process is frictional. New words emerge organically when a community collectively and repeatedly encounters a
previously unfamiliar concept. These words are known initially only to those in the shared domain and become
commonplace only if many others outside the domain begin to encounter and discuss the concept.
22spread from the domain of Artificial Intelligence labs to dinner table conversations in the course of
two years, and gained a widely understood acronym, LLM, along the way.
In our empirical setting, the ECH motivates a simple statistical, content-agnostic approach for
identifying expert words. Expert words are: (1) relatively infrequently encountered in common vo-
cabulary; and (2) have relatively low entropy, meaning that their domain of occurrence is relatively
predictable when they are encountered. Elasticity is, for example, a low entropy word because,
when encountered, it is easy to predict its domain of usage (economics). Conversely, despite being
infrequently used, the word pernicious has high entropy because its domain of (occasional) usage
is diverse, including literature, journalism, law, philosophy, medicine, etc.
We apply this logic to analyze the expertise content of job tasks enumerated in the 1977 Dictionary
of Occupational Titles (U.S. Department of Labor, Employment and Training Administration,
1977) and the 2018 O*NET release 23.0 (U.S. Department of Labor, Employment and Training
Administration, 2018). We identify task descriptions signifying expertise as those that have a low
Standard Frequency Index (SFI) score, where the SFI is an index commonly used in corpus analyses
that combines word frequency and word entropy to measure how ‘predictable’ a word is. The SFI
is enumerated for 140,000 unique English language words culled from 60,000 text samples (Zeno
et al., 1995). It is defined as 10 ×(log10(U) + 4), where U is frequency weighted by entropy and
entropyisdefinedasthelevelofdispersionacrosscontentareas.12 Asalogarithmicscale, arithmetic
differences in SFI correspond to geometric differences in word frequency. For instance, the word
‘luminance’ (SFI 30.5), with an approximate frequency of 0.1 per million words, is almost 1000
times less common than the word ‘color’ (SFI 61.0). The Efficient Coding Hypothesis implies that
words with high frequency and high entropy are non-specialized, while those with low frequency
and low entropy are typically used by experts.
Ashortcoming of the SFIis thatit willtend to underestimate expertise in cases where: job tasks are
under-specified; where the task descriptor fails to use existing specialized terminology; and where
specialized tasks have not condensed to single terms but instead emerge through the combination of
common words (e.g. ‘analyze’, ‘test’, ‘develop’, ‘properties’, ‘materials’), as often occurs in STEM
occupation tasks. For instance, the task, “Devises procedures for physical testing of materials,”
is performed by physicists but has an SFI of 55.0, which is low relative to the task average of
61.6. Additionally, the SFI measure attributes high expertise level to words that are archaic even
if inexpert, e.g., ‘workpiece’ and ‘mop’ – SFI 25.9 and 44.0 respectively. To limit this form of
mis-measurement (and recognizing that the Efficient Coding Hypothesis is not deterministic), we
discipline the SFI using the Dale-Chall readability list—developed by Edgar Dale and Jeanne S.
12The Educator’s Word Frequency Guide (EWFG) draws from 6,333 sources, ranging from Grade 4-level to college-
level and covering 9 broad subject areas. Some of the sources were submitted by states and school districts for
readability analysis, some were acquired based on surveys of textbook usage, and some were obtained from recom-
mended reading lists published by professional or educational institutions. The sample is broadly representative of
materials encountered during a standard American education during the 1980s. For example, all of the prose titles
used by at least 30% of schools in a 1989 survey by Applebee (1993) are in the EWFG. The additional 4 in the EFI
formula ensures that the value is positive.
23Chall (Dale and Chall, 1948) and updated in 1995 (Chall and Dale, 1995). This list comprises 3,000
words that were found in 1995 to be familiar to 4th graders. Cross-tabulating the SFI against the
Dale-Chall index, we identify the most-expert 10% of SFI words that were known by 4th graders
and Winsorize them by assigning each the least expert SFI score within the set. Similarly, we
identify the least expert 10% of SFI words that are not known by 4th graders and Winsorize them
by assigning each the most-expert SFI within the set. We exclude words not in the EWFG from
our calculations (approximately 1% of the sample by frequency).13. For clarity, we also subtract
the SFI from 100 so that it is increasing in expertise.
Tocalculatetheexpertiselevelofatask, wetaketheaverageSFIofeachterminthetaskdescription
after dropping stop words and lemmatizing. To calculate occupational expertise, XPT, we take the
mean expertise of all tasks associated with an occupational title in the DOT or O*Net.14 We then
aggregate scores from the occupational title level to the Census occupation level covering all of U.S.
employment, compiled by Autor et al. (2024). Since there are considerably more occupational titles
than there are harmonized occupations, we compute XPTj in each of 303 harmonized occupations
j as an employment-weighted average of occupational titles.15 We standardize XPTJ to have an
employment-weighted mean of zero in 1980 and a cross-occupation standard deviation of one. We
apply the same standardization to tasks, so a task XPT score of 1σ implies a level of expertise one
standard deviation above the occupation average. Also drawn from Autor et al. (2024) are occupa-
tional employment, hourly earnings, and demographic composition, calculated from the 1980 U.S.
Census and 2018 American Community Survey. We restrict our sample to harmonized occupations
with matching titles in both DOT 1977 and O*Net 2018 and exclude three occupations (Physical
scientists, n.e.c., Physicians’ assistants and Teacher’s aides) that don’t meet this criterion. These
occupations comprise less than 0.1% and 1% of employment hours in 1980 and 2018, respectively.
In applying the SFI expertise measure to DOT and O*NET job task descriptions, we implicitly
assume that the Bureau of Labor Statistics applies a form of efficient coding in crafting these de-
scriptions. Because the intended users of the DOT and, even more so, the O*NET, are job-seekers,
guidance counselors, and employers, the job task descriptions provided largely eschew professional
13As a robustness exercise, we approximate SFI values based ontheir closest matchin embeddings space and manually
verify each match. In cases where a suitable single-word substitute is available, we use the one-word option. In
cases where no single word is fitting (e.g., new acronyms), we take the average SFI of relevant combinations of
words. For instance, EKG is not in the EWFG, so we took the average SFI of ‘electric’, ‘cardio’ and ‘sonogram’.
Our results are unchanged in this alternative, more speculative specification.
14We exclude tasks that describe occupational subspecialization in the 1971 DOT that start with the phrase “May
be designated as ...” These sentences seldom contain information related to the task content of the occupation. We
also exclude so-called ‘green tasks’ and ‘green emerging occupations’ as identified by O*Net in 2018. These niche
tasks appear to reflect policy priorities rather than occupational content at the time of their inclusion.
15For 1977 DOT data, we use the 1971 Current Population Survey (CPS), which provides employment data for 3810
occupational titles/DOT codes. We drop occupational titles without a match in the CPS from our analysis. For
2018O*Netdata, weuse2018OccupationalEmploymentandWageStatistics(OEWS),whichprovidesemployment
data at the 6-digit SOC code level. Since task data are available at the 8-digit SOC level, there are 207 occupational
titles retained in our sample where multiple O*Net occupations match to the same OEWS occupation. Rather than
applying equal weighting, we use the frequency of O*Net job titles on Google Ngram in 2018 to proportionally
distribute employment weights.
24jargon—but not entirely.16 In numerous instances, BLS uses expert (though never abstruse) ter-
minology to describe job tasks, e.g., “Operate diagnostic imaging equipment” (O*NET 29-2035.00:
Magnetic Resonance Imaging Technologists); “Thread wire or cable through ducts or conduits”
(O*NET 47-2111.00: Electricians); or “Forecast economic, political, or social trends” (O*NET 19-
3011.00: Economists). Our maintained hypothesis is that BLS deploys expert terminology when
it would require substantially more description (consuming more reader bandwidth) to convey the
relevant concept absent that terminology (e.g., the word conduit). If, as we hypothesize, job task
descriptions contain expert terms only when they are largely unavoidable, these task descriptions
will implicitly encode expertise.17
To illustrate the operation of the expertise measure, Table 1 reports occupational titles, estimated
XPTj, and mean log real hourly wage at the 25th and 75th percentiles of the employment-weighted
expertise distribution, both overall and within each of 12 broad categories encompassing the full
set of occupations, using the mean value for each occupation across 1980 and 2018. The first row
reports that the occupations at the 25th and 75th percentiles of the overall expertise distribution
are, respectively, Proofreaders and Electricians, with corresponding expertise levels of−0.41σ and
0.91σ, and mean log hourly wages of 2.76 and 3.07. The subsequent rows report the 25th and
75th percentile occupations within each broad category. Averaging across these 12 groups, the
mean inter-quartile expertise gap is 1.13σ and the mean inter-quartile wage gap is 21.6 log points.
Evident from the table are both strengths and limitations of the expertise measure: in 9 of 12
categories, the more expert occupation has a higher hourly wage, with an average gap of +31.6 log
points. In 3 of 12 categories, the more expert occupation has a lower hourly wage, with an average
gap of−8.3 log points.18
16The Bureau of Labor Statistics’ website reports that “O*NET information is used by millions of individuals ev-
ery year, including those taking advantage of O*NET OnLine, My Next Move, and other publicly and privately
developed applications. The data have proven vital in helping people find the training and jobs they need, and
employers the skilled workers necessary to be competitive in the marketplace.”
17As an alternative data source, we explored the Google Ngram Viewer, which provides word frequencies calculated
from the texts of millions of English-language books published between 1800 and the present. We found that this
corpus substantially over-represents words used by college-educated adults, likely because they buy a dispropor-
tionate share of all books. By contrast, the EWFG text corpus is a more balanced sample of reading materials
used in each grade level from one through college.
18One of these three exceptions is the contrast between Miners (XPT=−0.97σ, ln ¯ w=3.06) and Farmers: owners and
tenants (XPT=−0.31σ, ln ¯ w= 2.98). In the Wealth of Nations (Book X, Part I), Adam Smith (1776) writes “[T]he
wages of labour vary with the ease or hardship, the cleanliness or dirtiness, the honourableness or dishonourableness
of the employment. A... blacksmith... seldom earns so much... as a [coal miner]... His work is not quite so dirty, is
less dangerous, and is carried on in daylight, and above ground...” (Smith, 2000).
25Table 1: Expertise and Earnings by Major Occupational Category: Averaging 1980 and 2018 Values
25th percentile 75th percentile
Occupation group Title XPT (σ) ln(Wage) Title XPT (σ) ln(Wage)
26
All occupations Proofreaders−0.41 2.76 Electricians 0.91 3.07
Professionals Social workers 0.09 2.92 Computer scientists 1.33 3.35
Technicians, fire, police Programmers of machine tools 0.17 2.99 Chemical technicians 1.08 3.08
Managers and executives Real estate managers 0.81 2.99 Financial managers 1.14 3.39
Clerical and administrative Bank tellers−0.66 2.46 Weighers and measurers 0.49 2.78
Sales minus financial/advertising Cashiers−1.34 2.31 Sales demonstrators−0.19 2.66
Construction and mechanics Carpenters−0.01 2.84 Electricians 0.91 3.07
Production and operative Hand molders/shapers−0.44 2.74 Electrical equipment assemblers 0.61 2.65
Transportation Vehicle washers−0.48 2.41 Supervisors of vehicle transport 0.24 2.96
Farm and mining Miners−0.97 3.06 Farmers (owners and tenants)−0.31 2.98
Services: Cleaning/protective Janitors−1.23 2.54 Landscaping supervisors 0.45 2.88
Services: Health Health and nursing aides−0.65 2.43 Dental assistants 2.11 2.56
Services: Personal Baggage porters−1.13 2.58 Food preparation supervisors 0.10 2.50
Notes: This table uses the average values of expertise and ln wages over 1980 and 2018. There are only 2 occupations in the Services: Health group.Figure 5: Expertise and Mean Log Wages by Occupation in 1980 and 2018: Binscatters
A. Bivariate wage-expertise regressions
1980
2018
Log hourly wage
2.0 2.5 3.0 3.5 4.0
Aerospace engineers
Air traffic controllers Sales engineers
Veterinarians
Accountants and auditors
Primary school teachers
Photographers Editors and reporters
Machinists
Automobile mechanics and repairers
Retail salespersons and sales clerks
Cashiers
Log hourly wage
2.0 2.5 3.0 3.5 4.0
Sales engineers
Veterinarians
Air traffic controllers
Aerospace engineers
Accountants and auditors
Editors and reporters
Primary school teachers Photographers
Machinists
Retail salespersons and sales clerks
Automobile mechanics and repairers
Cashiers
-3σ -2σ -1σ 0 1σ 2σ 3σ
Expertise (XPT)
Slope: 0.16 (0.01), R2: 0.32, N: 303
-3σ -2σ -1σ 0 1σ 2σ 3σ
Expertise (XPT)
Slope: 0.31 (0.02), R2: 0.49, N: 303
B. Conditioning on education (5 categories, one omitted)
1980
2018
Log hourly wage controlling for education
2.0 2.5 3.0 3.5 4.0
Air traffic controllers
Aerospace engineers
Sales engineers
Veterinarians
Machinists
Automobile mechanics and repairers
Photographers
Accountants and auditors
Editors and reporters
Retail salespersons and sales clerks
Primary school teachers
Cashiers
Log hourly wage controlling for education
2.0 2.5 3.0 3.5 4.0
Air traffic controllers
Sales engineers
Machinists
Aerospace engineers
Automobile mechanics and repairers
Photographers
Accountants and auditors
Veterinarians
Editors and reporters
Retail salespersons and sales clerks
Primary school teachers
Cashiers
-3σ -2σ -1σ 0 1σ 2σ 3σ
Expertise (XPT) controlling for education
Slope: 0.14 (0.01), Partial R2: 0.31, N: 303
-3σ -2σ -1σ 0 1σ 2σ 3σ
Expertise (XPT) controlling for education
Slope: 0.17 (0.01), Partial R2: 0.32, N: 303
Notes: This figure presents scatter plots of the relationship between occupations’ wages and expertise levels in 1980
and 2018. Panel A corresponds to the regression specification in column (1) of Table 2, and panel B corresponds to
column (3) of Table 2. Each point corresponds to the expertise XTP level (x-axis) and log hourly wage (y-axis) of
one consistently defined three-digit Census occupation with its employment share of the year as weights (N=303).
A strong testable implication of our framework is that occupations that require greater expertise
will pay higher wages. We test that prediction in Table 2 by fitting the following OLS model:
ln wjt= α+ β1XPTjt + β2Educjt + γJ(j) + ϵjt, (18)
where the dependent variable is the mean log hourly wage in occupation j in 1980 or 2018, the
primary explanatory variable is occupational expertise, XPTjt, and additional controls include
measures of occupational educational attainment and indicator variables for the broad occupation
categories used in Table 1. Models are weighted by occupational employment shares.
The upper and lower panels of Table 2 report estimates of equation 18 for year 1980 and 2018.
27As shown in the upper two panels of Figure 5, occupational expertise is a powerful predictor of
occupational wages. The point estimates of 0.164 (se = 0.014) and 0.305 (se = 0.018) indicate
that 1σ greater expertise is associated with 16 and 31 log points higher wages in 1980 and 2018,
respectively.19. The explanatory power of expertise is high, with bivariate R-squared values of
0.32 in 1980 and 0.49 in 2018, respectively (much of which is retained even after controlling for
education).
Table 2: The Relationship between Occupation Expertise and Mean Log Hourly Wages in 1980
and 2018: Cross-Sectional Regressions
(1) (2) (3) (4) (5) (6)
A. 1980
Expertise 0.164∗∗∗ 0.137∗∗∗ 0.087∗∗∗ 0.135∗∗∗ 0.069∗∗∗
(0.014) (0.011) (0.013) (0.012) (0.013)
Share of College+ 0.737∗∗∗ 0.615∗∗∗ 0.612∗∗∗
(0.061) (0.051) (0.087)
Expertise Partial R-squared 0.322 0.141 0.310 0.093
Education Partial R-squared 0.322 0.147 0.548 0.459
Adjusted R-squared 0.323 0.323 0.539 0.661 0.548 0.698
B. 2018
Expertise 0.305∗∗∗ 0.171∗∗∗ 0.135∗∗∗ 0.167∗∗∗ 0.123∗∗∗
(0.018) (0.014) (0.013) (0.014) (0.013)
Share of College+ 1.231∗∗∗ 0.928∗∗∗ 1.053∗∗∗
(0.052) (0.050) (0.072)
Occupation Group FE × ×
Full Education Controls × ×
Expertise Partial R-squared 0.324 0.269 0.325 0.234
Education Partial R-squared 0.536 0.424 0.524 0.412
Adjusted R-squared 0.486 0.647 0.761 0.851 0.785 0.861
Observations 303 303 303 303 303 303
Notes: Standard errors in parentheses. All regressions are weighted by employment hours in their respective years.
Column (1) regresses expertise alone on hourly wages in log points. Column (2) regresses the combined share of
workers in that occupation with college and graduate school degrees on hourly wages in log points. Column (3) runs
a regression of both expertise and college plus share on hourly wages in log points. Column (4) is the same regression
as column (4) but also controlling for 12 occupational group dummies. Column (5) parametrizes education through
controlling for the shares of workers at five different educational attainment levels: less than high school, only high
school, some college, 4-year college degree and graduate school degrees. Column (6) runs the same regression as (5)
but also controlling for 12 occupational group dummies.
Plausibly, XPT could proxy for conventional measures of the human capital of an occupation’s
workers. The lower two panels of Figure 5 demonstrate that the expertise-wage relationship is
highly robust to inclusion of detailed education controls. The detailed estimates in panel A of
Table 2 test robustness further by controlling, variously, for the share of an occupation’s workers
who have a college or post-college degree, the share of workers in each of four educational categories
(less than high school, some college or two-year degree, four-year degree, post-baccalaureate degree,
19The near-doubling of the expertise premium between 1980 and 2018 (compare panels A and B of Table 2) parallels
the steep rise in the return to education and cognitive skills during this period (Katz and Murphy, 1992; Murnane
et al., 1995; Katz and Autor, 1999; Autor et al., 2008; Hoffmann et al., 2020)
28with high school graduate omitted), eleven occupational dummies, and all combinations of these
variables. The inclusion of these covariates reduces the expertise slope, as expected, but in all
cases, XPT has robust predictive power for earnings, with a t-ratio never below 5 and a partial
R-squared value of 0.09 or higher.
Figure 6: Occupational Wages and Occupational Expertise: Plots by Major Occupation Group,
Averaging over 1980 and 2018 Values
Blue Collar Professional & Information Personal Services Commercial Services
Farm and mining
Managers and executives
Services:
Health
Sales minus
financial/advertising sales
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
Occupational mean wage (log)
-2σ -1σ 0 1σ 2σ
Slope: 0.40 (0.36)
-2σ -1σ 0 1σ 2σ
Slope: -0.17 (0.10)
-2σ -1σ 0 1σ 2σ
Slope: 0.05 (0.00)
-2σ -1σ 0 1σ 2σ
Slope: 0.64 (0.11)
Construction and mechanics
Professionals and
financial/advertising sales
Service: Personal
Technicians + fire, and police
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
-2σ -1σ 0 1σ 2σ
Slope: 0.08 (0.03)
-2σ -1σ 0 1σ 2σ
Slope: 0.18 (0.03)
-2σ -1σ 0 1σ 2σ
Slope: 0.14 (0.04)
-2σ -1σ 0 1σ 2σ
Slope: 0.07 (0.08)
Production and operative
Clerical and
administrative support
Services:
Cleaning and protective
Transportation
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
2.0 2.5 3.0 3.5 4.0
-2σ -1σ 0 1σ 2σ
Slope: 0.16 (0.03)
-2σ -1σ 0 1σ 2σ
Slope: 0.08 (0.03)
-2σ -1σ 0 1σ 2σ
Slope: 0.19 (0.06)
-2σ -1σ 0 1σ 2σ
Slope: 0.04 (0.06)
Occupational expertise (XPT)
Notes: This figure presents scatter plots of the relationship between occupations’ wages and expertise levels for 12
major occupation groups, pooling 1980 and 2018 data. Each point corresponds to the expertise XTP level (x-axis)
and log hourly wage (y-axis) of one consistently defined three-digit Census occupation with its average employment
shares over 1980 and 2018 as weights. Plotted lines correspond to the weighted fitted values.
The Table 2 estimates that contain major occupation dummies suggest that the predictive relation-
ship between expertise and wages stems from within as well as across-category contrasts among
detailed occupations (e.g., Parking lot attendants vs. Vehicle transportation supervisors within
Transportation, as well as Parking lot attendants vs. Licensed practical nurses in Health). Figure
6 confirms this inference by reporting the expertise-wage gradient within each of the 12 major
occupation groups, here pooling data for 1980 and 2018. The wage-expertise gradient is positive
29in 11 of 12 occupational categories and significantly positive in 8 of 12 categories.20 The wage-
expertise slope is puzzlingly negative and borderline significant for the occupational category of
Managers and executives. The proximate explanation is that executive occupations are charac-
terized with broad, vague task descriptions that generate low XPT values (e.g., “prepare plans,”
“improve efficiency”).21 We do not attempt to correct for this deficiency, but we suspect it is less
consequential for our within-occupation, longitudinal expertise change measure, which implicitly
takes out occupational fixed effects.
3.2 Measuring occupational task removal and addition
To assess the correlation and, ultimately, the causal relationship between changing occupational
expertise levels, wages, and employment, we construct a direct measure of the tasks removed from
and added to occupations. The DOT and O*NET databases, produced four decades apart, almost
invariably describe what appear to be the same tasks using somewhat different words. To abstract
from these nominal differences, we map all the tasks from each period into a high-dimensional
word embedding space, using the OpenAI text-embedding-3-small model with 1,536 dimensions.
Text embeddings enable us to match tasks on their semantic content rather than particularities of
wording. To form these matches, we calculate the Euclidean distance in embedding space between
all possible 1977 vs. 2018 task pairs and apply a matching caliper of 0.95, which we derive by
manually verifying 600 proposed matches. The resulting match considers two tasks (one from
1977, one from 2018) to be retained for an occupation over time if they sit within the same high-
dimensional hypersphere.
As illustrated in Figure 7, our matching technique partitions tasks into three groups. Retained
tasks are those that are present in 1977 and within the threshold distance of at least one task that
is present in 2018. Removed tasks are those that are present in 1977 but lack a sufficiently close
2018 counterpart. Added tasks are those that are present in 2018 but lack a sufficiently close 1977
counterpart.
20Because the category of Services: Health contains only two occupations, the R-squared of this regression is one by
definition.
21Examples include: “Prepare plans of action for investment, using financial analyses”; “Seek new ways to improve
efficiency and increase profits”’ and “Plan security for special and high-risk events.”
30Figure 7: Identifying Retained, Removed, and Added Tasks between 1977 and 2018: Schematic
Representation
Dimension 1
Dimension 2
Removed
Present in 1977
Not Matched in 2018
Retained
Present in 1977
Matched in 2018
Retained
Present in 2018
Matched in 1977
Added
Present in 2018
Not Matched in 1977
Notes: This figure is a 2-dimensional stylized representation of the high-dimensional embedding
space utilized to identify tasks Removed, Retained, and Added between 1977 and 2018. Each point
represents a task, surrounded by a larger circular shaded area representing a hyper-sphere of radius
.95. If the hypersphere around a task from 1977/2018 contains a task from 2018/1977, the task is
considered retained. If not, the task is considered removed/added.
Figure 8 provides a concrete example by comparing five sample tasks in the File Clerk occupation
in 1977 vs. 2018. Three of five 1977 tasks are designated as retained because semantically close
matches are found in 2018, though none use identical wording across periods. One 1977 task, “May
operate keypunch to enter data on tabulating cards,” is designated as removed because we find no
semantically nearby task in 2018. Finally, one 2018 task, “Input data... into computer systems,”
is marked as new because we find no semantically nearby task in 1977.
31Figure 8: Examples of Tasks Retained, Removed and Added
between 1977 and 2018: File Clerks
File Clerks
1977
May operate keypunch to enter data on tabulating cards
Reads incoming material and sorts according to file system
Keeps records of material removed, stamps material received, traces
missing file folders, and types indexing information on folders
Places material in file cabinet, drawers, boxes, or in special filing cases
-
(many other tasks) Share of removed tasks: 13.16%
Average XPT in 1977: 0.22
XPT of removed: -1.55, Effect of removal: + 0.23
File Clerks
2018
-
Scan or read incoming materials to determine how and where they
should be classified or filed.
Keeps records of materials filed or removed, using log books or
computers and generate computerized reports.
Place materials into storage receptables, such as file cabinets, boxes,
bins, or drawers, according to classification and identification
information.
Input data, such as file numbers, new or updated information, or
document information codes into computer systems to support
document and information retrieval.
(many other tasks)
Share of added tasks: 5.26%
Average XPT in 2018: 0.51
XPT of added: -4.79, Effect of adddition: -0.28
Notes: This table provides examples of tasks added and removed for the file clerk occupation (census code 335).
Expertise change due to removal is calculated as ∆XPTsub
j ≡ TASKsub
j,1977/TASKj,1977 XPTj,1977−XPTsub
j,1977 ,
and expertise change due to addition as ∆XPTadd
j ≡ TASKadd
j,2018/TASKj,2018 XPTadd
j,2018−XPTj,2018 . These are
equivalent to the definitions in equation (19).
We use this classification of retained, added, and subtracted tasks to calculate the net change in
expertise in each occupation due to task removal and task addition between 1977 and 2018 as:
∆XPTsub
j ≡XPTret
j,1977−XPTj,1977
∆XPTadd
j ≡XPTj,2018−XPTret
j,2018 (19)
∆XPTnet
j ≡∆XPTsub
j + ∆XPTadd
j.
The first term defined above, ∆XPTsub
j , is occupational expertise change due to task removal,
equal to the average expertise of tasks in occupation j that are present in 1977 and retained
(super-scripted by ret) to 2018 minus the average expertise of all tasks present in j in 1977.22
The second term, ∆XPTadd
j , is occupational expertise change due to task addition, equal to the
average expertise of all tasks present in j in 2018 minus the average expertise of all tasks in 2018
22The DOT originated in 1939 and was updated three additional times (in 1965, 1977, and partially in 1991), while
retaining much of its original material, particularly from 1965 forward. The O*NET originated in 1998 and, in
its now-mature form, uses no content from the DOT. Because the DOT and O*NET use different words for the
same retained task, the calculated expertise of retained tasks will generally differ between 1977 and 2018 (i.e.,
XPTret
j,1977 ̸= XPTret
j,2018). To abstract from this artifactual source of variation, equation (19) calculates within-
occupation expertise changes using only tasks removed in 1977 and tasks added in 2018, omitting any variation
stemming from changes in the wording of retained tasks.
32that were retained from 1977. The third term, ∆XPTnet
j , is the sum of these two effects. Observe
that because both task removal and task addition can raise or lower occupational expertise, each
of the three terms defined above may be positive, negative, or zero.
Figure 9 documents how occupational expertise changes as a result of task removal and addition.
This figure plots the histogram of initial task expertise within three example occupations: Dis-
patchers, Management Support Occupations, and Proofreaders. Retained tasks are color-coded in
purple, removed tasks in orange, and added tasks in blue. As this figure illustrates, the impact
of task removal or addition on the expertise level of an occupation depends on both the expertise
level and probability mass of each of the tasks added or removed relative to the occupation’s mean
task expertise level in 1977. In panel A, the expertise level of Dispatchers falls due to the removal
of comparatively expert tasks. In panel B, the expertise level of Management Support Occupations
rises due to the removal of inexpert tasks and the addition of expert tasks. In panel C, the expertise
level of Proofreaders rises due to the removal of inexpert tasks.
This figure also highlights that occupational expertise change is inextricable from task removal
and addition. We therefore directly control for the loss and gain of occupational tasks (percentage
changes in tasks), as task models would dictate. We calculate the net percentage change in the
number of tasks in each occupation tasks due to task removal and addition as follows:
∆TASKsub
j ≡1−N1977
j∈ret/N1977
j
∆TASKadd
j ≡1−N2018
j∈ret/N2018
j
∆TASKnet
j ≡∆TASKadd
j−∆TASKsub
j
Toassesstheexternalvalidityofthetaskadditionmeasure, weharnessdatafromAutoretal.(2024)
to test whether ∆TASKadd
j , predicts the addition of new job titles over the same time interval. As
detailed in Autor et al. (2024), the new title measure is derived from an entirely distinct data
source, the Census Alphabetical Index of Occupations and Industries (U.S. Census Bureau, 2018),
and has no intrinsic relationship to the task addition measure constructed. Nevertheless, the new
task measure proves highly predictive of the flow of new occupational titles, as shown in Appendix
Figure A1. This figure presents a regression of the decadalized log count of new titles added to each
occupation on ∆TASKadd
j , which yields a coefficient of 4.49 (se = 1.36). This implies that a 1%
additiontothesetoftasksperformedbyanoccupationpredictsa4.5% increaseinnewtitles. While
the magnitude of this association lacks a cardinal interpretation due to the incommensurate units
of these measures, its statistical significance confirms that ∆TASKadd
j captures new task growth
within occupations.
33Figure 9: Examples of Expertise Change and Task Change between 1977 and 2018 in Three
Occupations
1980 2018
30
25
Compares photographic blowup of written or typed specimen obtained from separate sources to ascertain similarity or differences.
(XPT=0.18)
Number of Tasks
20
Ensures compliance of employees with established security, sales, and record keeping procedures and practices. (XPT=0.43)
15
10
5
0
Implement security
practices to preserve assets, minimize
liabilities,
or ensure customer privacy, using parallel
servers, hardware redundancy, fail-safe technology, information encryption, or firewalls. (XPT=4.70)
Determine location for product listings to maximize exposure to online traffic.
(XPT=4.92)
-8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7
Expertise (XPT)
A. Management support occupations: tasks added, expertise added
2018
1980
Orders irregular routing of telegrams to prevent congestion or wire shortage. (XPT=1.56)
Records information, such as name, address, article to be repaired, or service to be rendered. (XPT=-1.31)
Number of Tasks
25
20
15
10
5
0
Establishes and reroutes telegraph and submarine cable circuits to ensure flow of messages. (XPT=5.79)
-9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7
Expertise (XPT)
B. Dispatchers: tasks removed, expertise removed
1980 2018
Consult reference books or secure aid of readers to check references with rules of grammar and composition. (XPT=-0.63)
5
4
Compares information or figures on one record against the same data on other records. (XPT=-1.50)
Number of Tasks
3
2
Places proof and copy side by side on reading board. (XPT=-6.24)
1
0
Corrects or records omissions, errors, or inconsistencies found. (XPT=-0.09)
-7 -6 -5 -4 -3 -2 -1 0 1 2 3
Expertise (XPT)
C. Proofreaders: tasks removed expertise added
34To provide more descriptive details on the expertise measure, Table 3 reports levels and changes
(per decade) in task expertise, real log wages, employment shares, and education (college or higher
attainment) by sex and major occupation between 1980 and 2018. The expertise demands of
U.S. employment rose by an average of 0.82µ per decade between 1980 and 2018. (For clarity of
exposition, we report 100×decadal changes, where µ≡∆σ/100 per decade, following the format
of Table 3.) The increase was substantially larger among female than male workers at 1.26µ and
0.52µ respectively. Expertise requirements rose in 10 of 12 occupational categories, falling only in
Farm and mining (µ=−0.84) and Services: Cleaning and protective (µ=−1.09), both from a low
expertise base.
Table 3: Levels and Changes of Expertise, Wages, and Employment Share, 1980–2018: Overall,
by Sex, and by Occupation Group
XPT (σ) ln(Wage) % Employment % College+
1980 100×∆decade 1980 ∆decade 1980 ∆decade 1980 ∆decade
All workers 0.00 0.82 2.78 0.06 100.00 0.00 20.34 4.04
(0.04) (0.17) (0.01) (0.01) Men 0.18 0.52 2.92 0.04 63.78−1.86 22.41 2.82
(0.05) (0.20) (0.02) (0.01) Women−0.31 1.26 2.52 0.09 36.22 1.86 16.70 5.84
(0.06) (0.30) (0.01) (0.01) (1.03) (0.41)
(1.51) (0.58)
(1.35) (0.59)
Professionals and financial/advertising sales 0.09 0.86 3.01 0.07 15.96 1.66 61.57 2.22
(0.09) (0.54) (0.02) (0.01) (2.35) (0.78)
Technicians + fire, and police 0.52 0.19 2.90 0.09 4.41 0.34 22.19 5.05
(0.11) (0.62) (0.03) (0.02) (2.19) (1.31)
Managers and executives 1.09 0.80 3.10 0.09 12.57 1.06 40.09 5.37
(0.04) (0.38) (0.04) (0.01) (2.48) (0.81)
Clerical and administrative support−0.35 3.16 2.63 0.04 16.21−0.97 9.75 3.44
(0.09) (0.66) (0.02) (0.01) (0.93) (0.37)
Sales minus financial/advertising sales−0.92 0.02 2.64 0.03 5.83−0.17 16.51 2.74
(0.22) (0.45) (0.11) (0.04) (3.95) (1.59)
Construction and mechanics 0.69 0.23 2.91 0.01 9.21−0.51 4.39 0.66
(0.09) (0.21) (0.02) (0.01) (0.37) (0.16)
Production and operative 0.18 0.40 2.75 0.00 16.64−2.12 4.09 1.18
(0.07) (0.20) (0.03) (0.01) (0.39) (0.17)
Transportation−0.63 0.28 2.74 0.00 6.86−0.04 2.68 1.01
(0.09) (0.31) (0.03) (0.01) (0.23) (0.19)
Farm and mining−0.72−0.84 2.24 0.08 2.97−0.41 7.86 1.21
(0.07) (0.49) (0.06) (0.02) (0.40) (0.48)
Services: Cleaning and protective−1.08−1.09 2.44 0.03 3.53 0.18 3.99 1.32
(0.14) (0.52) (0.05) (0.02) (0.63) (0.45)
Services: Health−1.30 1.39 2.33 0.05 1.50 0.35 5.28 1.74
(0.70) (0.22) (0.04) (0.02) (2.44) (0.88)
Service: Personal−0.84 0.41 2.22 0.04 4.32 0.63 5.37 1.82
(0.16) (0.64) (0.03) (0.01) (0.88) (0.49)
Notes: Standarderrorsinparentheses. Decadalizedchangesarereportedforexpertise, logwages, groups’employment
shares, and the share of workers with at least a college education. Changes of XPT are decadalized and multiplied
by 100 for clarity. XPT changes report the net changes in expertise due to task removal and addition. All descriptive
statistics are weighted by the demographic group’s employment hours in the occupations in the corresponding year.
Appendix Table A1 reports analogous statistics by sex and major education category. Average
occupational expertise, XPT, is strongly increasing in workers’ education levels. The average
35occupational expertise of workers by education level in 1980 was: less than high school=−0.22σ;
exactly high school=−0.07σ; some college = 0.08σ; four-year degree = 0.22σ; and post-college
degree = 0.28σ. Average occupational expertise of women in 1980 was substantially lower than men
in each education category, with the smallest gap among those with less than a high school degree
(−0.45σ) and the largest gap among those with graduate degrees (−0.82σ). In all but the highest
degree category, occupational expertise of women rose faster than men and the gender wage gap
contracted. Among workers with a graduate degree, however, the gender gap in both expertise and
wages rose between 1980 and 2018.
4 Changing occupational expertise and occupational tasks: Wage
implications
This section analyzes the relationship between task changes and occupational wage changes. Our
model predicts that a rise in the average expertise level of an occupation’s task bundle will yield an
increase in wages and the opposite will occur if the bundle’s expertise requirements fall. Occupa-
tional expertise changes when tasks are removed from or added to its bundle: removing expert tasks
or adding inexpert tasks lowers required expertise; removing inexpert (supporting) tasks or adding
expert tasks raises required expertise.23 We remain agnostic for now about why occupational tasks
are removed or added, but we take this question head on in the final empirical section (Section 6).
We characterize the relationship between task change and occupational wage change by fitting the
following longitudinal (within-occupation) regression,
∆ ln wj= α+ β1∆XPTnet
j + β2∆TASKnet
j + γJ(j) + ϵj, (20)
where the dependent variable, ∆ ln wj is the change in the mean log hourly wage of occupation j
between 1980 and 2018. The principle explanatory variables are the net change in task expertise
∆XPTnet
j and task quantity ∆TASKnet
j . The vector γ contains indicator variables corresponding to
the 12 broad occupation categories above (one omitted). All first-differenced variables are scaled on
a per-decade basis to account for uneven period lengths. Estimates are weighted by start-of-period
occupational employment shares.
Figure 10 plots the central findings from these estimates, with detailed regression estimates enumer-
ated in Table 4A. Changes in occupational task expertise robustly predict changes in occupational
wages, as shown in the left-hand panel of Figure 10. The point estimate of 0.175 (se = 0.047)
implies that a 1σ rise in the expertise level of tasks performed in an occupation predicts an 18%
rise in wages. This point estimate is remarkably close to the cross-sectional relationship between
expertise and log wages reported in Table 2.
23As above, the terms expert and inexpert refer to the expertise of tasks removed or added relative to those initially
present in the task bundle.
36Figure 10: Changes in Task Expertise, Task Quantities, and Log Hourly Wages by Occupation,
1980–2018: Binscatters
∆ ln wj= α+ β1∆XPTnet
j + β2∆TASKnet
j + γJ(j) + ϵj,
A. Change in Expertise (σ) B. Change in Tasks (%)
Wage change (decadalized, log pts)
0.00 0.03 0.06 0.09 0.12
Wage change (decadalized, log pts)
0.00 0.03 0.06 0.09 0.12
-0.3σ -0.2σ -0.1σ 0.0 0.1σ 0.2σ 0.3σ
Net Expertise change (σ)
Slope: 0.18 (0.05), Partial R2: 0.04, N: 303
-8% -4% 0 4% 8%
Net task change (%)
Slope: 0.33 (0.12), Partial R2: 0.02, N: 303
Notes: This figure reports bin scatters of the employment-weighted conditional correlation between decadalized
percent wage growth and net expertise change due to task change (left-hand side) and task quantity change (right-
hand side). The corresponding regression specification is column (5) panel A of Table 4 using 303 consistently defined
Census occupations over 1980-2018. Each point is weighted by employment share in 1980.
The right-hand panel of Figure 10 shows that changes in task quantities also robustly predict wages
changes: the point estimate of 0.334 (se = 0.123) indicates that a 10% expansion in the set of tasks
performed by an occupation predicts a 3.3 log point rise in wages. Both of the wage relationships
reported in Figure 10 derive from a single wage equation that also accounts for 12 major occupation
group fixed effects (one omitted). Conditioning on these covariates matters little for the estimates,
however, as is visible in the detailed estimates in Table 4A. Both expertise change and task change
individually and jointly predict occupational wage change, and this remains true whether or not
occupation group main effects are included. The point estimates for task expertise change and
task quantity change are each slightly larger and more precise when both are included in the same
regression, indicating that these variables are negatively correlated, but only moderately so. These
results confirm a key prediction of the expertise model: changes in occupational task expertise
robustly predict changes in occupational wages.
We next test a further stringent and, arguably, non-obvious, prediction of the expertise model:
the wage effect of task addition and removal depend on the expertise level of tasks added and
subtracted, not (merely) on their quantity. Specifically, task removal lowers wages if expert tasks
are removed and raises wages if inexpert tasks are removed. Conversely, task addition lowers wages
if inexpert tasks are added and raises wages if expert tasks are added. We test these predictions
by fitting the following occupational wage equation:
∆ ln wj= α+ β1∆XPTsub
j + β2∆XPTadd
j + β3∆TASKsub
j + +β4∆TASKadd
j + γJ(j) + ϵj. (21)
37Table 4: The Relationship between Changes in Task Expertise, Task Quantities,
and Occupational Wages, 1980–2018
(1) (2) (3) (4) (5)
A. Net Change
Net Expertise Change 0.194∗∗∗ 0.161∗∗∗ 0.175∗∗∗
(0.057) (0.047) (0.047)
Net Task Change 0.702∗∗∗ 0.282∗ 0.334∗∗
(0.133) (0.125) (0.123)
Occupation Group FE × × ×
Adjusted R-squared Observations 0.035 0.416 0.081 0.402 0.428
303 303 303 303 303
B. Removal and Addition Separately
Expertise Change due to Task Removal 0.103∗ 0.126∗ 0.147∗∗
(0.052) (0.051) (0.051)
Expertise Change due to Task Addition 0.208∗ 0.279∗∗ 0.255∗∗
(0.088) (0.086) (0.088)
Share of Tasks Removed−0.111−0.156−0.230
(0.142) (0.143) (0.141)
Share of Tasks Added 0.443∗ 0.579∗∗ 0.549∗∗
(0.206) (0.205) (0.206)
Occupation Group FE × × × × ×
ˆ
ˆ
H1
0 :
βXPTsub =
βXPTadd (p-value) 0.103 0.260
ˆ
ˆ
H2
0 :
βTASKsub =−
βTASKadd (p-value) 0.070 0.176
H1
0 and H2
0 : (joint p-value) 0.130
Adjusted R-squared 0.399 0.416 0.419 0.407 0.432
Observations 303 303 303 303 303
Notes: Standard errors in parentheses. All regressions are weighted by employment hours in 1980. The outcome in
everyspecificationisthedecadalizedchangeinrealwagesinlogpointsfrom1980to2018, followingAutoretal.(2024).
All predictors are also decadalized. Occupational group fixed effects refer to 12 broad occupational group dummies.
Expertise change is normalized according to the standard deviation of the employment hours weighted distribution
of XPTj in 1980. The share of tasks removed and added is the positive fraction. In Panel B, Column (3) displays
the significance level of an F-test that checksˆ
ˆ
βXPTsub =
βXPTadd , column (4) for the test thatˆ
ˆ
βTASKsub =
βTASKadd
and column (5) runs both tests separately as well as jointly.
Distinct from equation (10) above, this specification allows task removal and task addition to
predict wage changes through four channels: expertise change due to task removal (β1); expertise
change due to task addition (β2); task quantity change due to task removal (β3); and task quantity
change due to task addition (β4). Per the expertise model, we expect that increases (decreases) in
occupational task expertise to predict gains (losses) in occupational wages, regardless of whether
expertise changes stem from task removal or task addition (β1, β2 > 0). Per the task model, we
expect task quantity removal to predict wage declines and task addition to predict wage gains
(β3 <0, β4 >0).
38Figure 11: Changes in Task Expertise, Task Quantities, and Log Hourly Wages by Occupation,
1980–2018: Distinguishing between Task Removal and Task Addition
∆ ln wj= α+ β1∆XPTsub
j + β2∆XPTadd
j + β3∆TASKsub
j + +β4∆TASKadd
j + γJ(j) + ϵj
A. Expertise Change: Task Removal B. Expertise Change: Task Addition
Wage change (decadalized, log pts)
0.00 0.03 0.06 0.09 0.12
Wage change (decadalized, log pts)
0.00 0.03 0.06 0.09 0.12
-0.2σ -0.1σ 0.0 0.1σ 0.2σ
Expertise change due to removal
Slope: 0.15 (0.05), Partial R2: 0.43, N: 303
-0.2σ -0.1σ 0.0 0.1σ 0.2σ
Expertise change due to addition
Slope: 0.26 (0.09), Partial R2: 0.43, N: 303
C. Task Removal D. Task Addition
Wage change (decadalized, log pts)
0.00 0.03 0.06 0.09 0.12
Wage change (decadalized, log pts)
0.00 0.03 0.06 0.09 0.12
-5% 0 5% 10% 15%
Share tasks removed (%)
Slope: -0.23 (0.14), Partial R2: 0.43, N: 303
-5% 0 5% 10% 15%
Share tasks added (%)
Slope: 0.55 (0.21), Partial R2: 0.43, N: 303
Notes: This figure reports bin scatters of the employment-weighted conditional correlation between decadalized
percent wage growth and expertise change due to task change and task quantity change. Changes are decomposed
into task removal (left-hand side) and task addition (right-hand side). The corresponding regression specification
is column (5) panel B of Table 4 using 303 consistently defined Census occupations over 1980-2018. Each point is
weighted by employment share in 1980.
The four panels of Figure 11 confirm these predictions. As shown in the upper two panels,
task removal and task addition predict wage changes approximately symmetrically: task removal
that raises or lowers expertise requirements predicts falling and rising wages, respectively (ˆ
β1 =
0.147, se = 0.051), and similarly, task addition that raises or lowers expertise requirements predicts
falling and rising wages (ˆ
β2 = 0.255, se = 0.088). Moreover, an F-test of the equality of these two
coefficients accepts the null at p= 0.260.
Task quantity also matters. The bottom two panels of Figure 11 confirm that, holding task ex-
pertise constant, task removal predicts falling wages (ˆ
β3 =−0.230, se = 0.141) and task addition
39predicts rising wages (ˆ
β4 = 0.549, se = 0.206). (An F-test that these coefficients are equal and
opposite weakly accepts the null at p= 0.176) As detailed by the regressions in Table 4B, the four
distinct predictive relationships between expertise changes and wage changes (ˆ
ˆ
β1,
β2 >0 and task
quantity changes andˆ
ˆ
β3 <0,
β4 >0) are robustly evident—particularly those for task expertise—
whether estimated individually or jointly, reflecting the fact that task expertise change and task
quantity change are only weakly correlated, as documented in Appendix Figure A2. The expla-
nation is substantive. Because neither task quantity removal nor task quantity addition has any
intrinsic relationship to task expertise change, either task removal or task addition can raise or
lower expertise requirements.24
5 Changes in the quantity and expertise of occupational tasks:
Employment implications
This section tests the employment implications of the expertise model, which stands in sharp con-
trast to those of the task model. Perhaps counterintuitively, the expertise model predicts that task
changes (removal or addition) that reduce occupational expertise demands raise (relative) occu-
pational employment and, conversely, task changes (removal or addition) that raise occupational
expertise demands lower occupational employment. This is because changes in occupational ex-
pertise requirements operate like labor supply shifts: task automation that reduces occupational
expertise requirements expands the effective supply of qualified labor; task automation that raises
occupational expertise requirements reduces the effective of supply of qualified labor. Behind these
predictions is an important assumption: occupational demand is in all cases elastic, so that when
task automation raises an occupation’s productivity, employment rises (though in all cases, labor
share falls).
24Is the wage-expertise relationship identified above driven by changes in wage premia in occupations undergoing
expertise change or instead by changes in the composition of workers in these occupations? Our conceptual model
admits both channels: when automation renders all formerly expert tasks in an occupation generic, wages fall
relative to other still-expert occupations. Simultaneously, less expert workers enter. Both channels lead to wage
declines. Following Autor et al. (2024), we explore which channels appear operative by decomposing occupational
wage changes into components due to compositional change versus occupational wage premia. While our analysis
suggests that expertise change predicts wage changes through changes in the composition of occupational incum-
bents and changes in the wages paid to incumbents, we lack sufficient precision to confidently differentiate these
mechanisms.
40Table 5: The Relationship between Changes in Task Expertise, Task Quantities,
and Occupational Employment, 1980 – 2018: Panel Regressions
(1) (2) (3) (4) (5)
A. Net Change
Net Expertise Change−0.690∗∗
−0.570∗∗
−0.510∗
(0.244) (0.200) (0.199)
Net Task Change 3.830∗∗∗ 1.580∗∗ 1.430∗∗
(0.553) (0.525) (0.523)
Occupation Group FE × × ×
Adjusted R-squared Observations 0.023 0.422 0.134 0.424 0.435
303 303 303 303 303
B. Net Change, Dropping Outliers
−0.646∗∗∗
Net Expertise Change−0.697∗∗
−0.589∗∗
(0.228) (0.185) (0.184)
Net Task Change 3.570∗∗∗ 1.474∗∗ 1.296∗∗
(0.521) (0.489) (0.485)
Occupation Group FE × × ×
Adjusted R-squared Observations 0.027 0.438 0.134 0.432 0.449
299 299 299 299 299
C. Removal and Addition Separately, Dropping Outliers
Expertise Change due to Task Removal−0.737∗∗∗
−0.775∗∗∗
−0.716∗∗∗
(0.199) (0.203) (0.204)
Expertise Change due to Task Addition−0.117−0.208−0.144
(0.354) (0.341) (0.348)
Share of Tasks Removed−1.369∗
−1.569∗∗
−1.419∗
(0.547) (0.563) (0.559)
Share of Tasks Added 1.005 1.253 0.879
(0.832) (0.809) (0.818)
Occupation Group FE × × × × ×
ˆ
ˆ
H1
0 :
βXPTsub =
βXPTadd (p-value) 0.128 0.135
ˆ
ˆ
H2
0 :
βTASKsub =−
βTASKadd (p-value) 0.731 0.564
H1
0 and H2
0 (joint p-value) 0.321
Adjusted R-squared 0.451 0.415 0.440 0.430 0.450
Observations 299 299 299 299 299
Notes: Standard errors in parentheses. All regressions are weighted by employment hours in 1980. The outcome
in every specification is the decadalized change in employment in log points from 1980 to 2018, following Autor
et al. (2024). Occupational group fixed effects refer to 12 broad occupational group dummies. Expertise change is
normalized according to the standard deviation of the employment hours weighted distribution of XPTj in 1980.
Share of tasks removed and added are positive fractions. All predictors are also decadalized. In Panel B and C, 4
outlier occupations experiencing the highest decline in employmentare dropped. In Panel C, Column (3) displays the
significance level of an F-test that checksˆ
ˆ
βXPTsub =
βXPTadd , column (4) for the test thatˆ
ˆ
βTASKsub =
βTASKadd and
column (5) runs both tests separately as well as jointly.
41Figure 12: Changes in Task Expertise, Task Quantities, and Occupational Employment, 1980 –
2018: Binscatters
A. ∆ ln EMPj= α+ β1∆XPTnet
j + ϵj
Employment change (decadalized, log pts)
-0.25 0.00 0.25 0.50
-0.3σ -0.15σ 0.0 0.15σ 0.3σ
Net Expertise change
Slope: -0.69 (0.24), Partial R2: 0.02, N: 303
B. ∆ ln EMPj= α+ β1∆XPTnet
j + β2∆TASKnet
j + γJ(j) + ϵj
Employment change (decadalized, log pts)
-0.25 0.00 0.25 0.50
-0.3σ -0.15σ 0.0 0.15σ 0.3σ
Net Expertise change
Slope: -0.51 (0.20), Partial R2: 0.43, N: 303
Employment change (decadalized, log pts)
-0.25 0.00 0.25 0.50
-8% -4% 0 4% 8%
Change in number of tasks (%)
Slope: 1.43 (0.52), Partial R2: 0.43, N: 303
Notes: This figure reports bin scatters of the employment-weighted conditional
correlation between decadalized percent employment growth and net expertise
change due to task change and task quantity change. Panel A corresponds to
column (1) panel A of table 5. Panel B corresponds to column (5) panel A of
table 5 using 303 consistently defined Census occupations over 1980-2018. Each
point is weighted by employment share in 1980.
42Paralleling the analysis of occupational wage change above, we fit the following models for changes
in log occupational employment between 1980 and 2018:
∆ ln EMPj= α+ β1∆XPTnet
j + β2∆TASKnet
j + γJ(j) + ϵj. (22)
Here, the dependent variable, ∆ ln EMPj is the per-decade log change in employment in occupation
j between 1980 and 2018. The principal explanatory variables are the net change in task expertise
∆XPTnet
j and task quantity ∆TASKnet
j in each occupation. As above, the vector γ contains indica-
tor variables corresponding to the 12 broad occupation categories above (one omitted). Estimates
are weighted by start-of-period occupational employment shares, while first-differenced variables
are decadalized as above.
The top panel of Table 5 provides detailed estimates of equation (22), with principle results plotted
as binscatters in Figure 12. As shown in Panel A, the bivariate relationship between expertise
change and employment change has a fitted regression slope of˜
β1 =−0.690 (se = 0.244). This
implies that a 0.1σ rise in occupational task expertise predicts a 6.9 log points (relative) fall in
employment over the corresponding decade. This negative relationship between expertise change
and employment change is predicted by the model.
The next two panels of Figure 12 report a more stringent test of the model’s predictions. The single
regression estimate that underlies both panels now accounts for both task expertise change and task
quantity change, and further includes main effects for the broad occupational categories above. The
coefficient on task expertise in this multivariate model in panel B,˜
β1 =−0.510 (se = 0.199), is
comparable to the bivariate estimate in panel A in magnitude and precision. Holding task quantity
constant, a 0.1σ rise in an occupation’s task expertise predicts a 5.1% employment decline. Panel
C shows that the coefficient on task quantity change is opposite in sign to that for task expertise
change, Consistent with the task model. It is also precisely estimated, with˜
β2 = 1.430 (se = 0.523).
Holding task expertise constant, a 10% increase in the quantity of tasks performed by an occupation
predicts a 14% employment rise.
Close inspection reveals four outlying occupations that attenuate the relationship between exper-
tise change and employment change: Lathe, milling, and turning machine operatives; Miscellaneous
textile machine operators; Office Machine operators not elsewhere classified; and Telephone oper-
ators (as detailed in Feigenbaum and Gross (2024)). As documented in Appendix Figure A3,
employment in these occupations contracted dramatically over the most recent four decades, a
pattern almost surely explained by a combination of automation and international trade (see Autor
et al. (2013); Acemoglu and Restrepo (2020)). These examples run counter to our model, which
assumes that all occupations contain both expert tasks that are potentially subject to automation,
and inexpert (generic) tasks that are not automatable. As an exploratory step, we re-estimate
the employment-expertise regressions in Table 5 excluding these four outliers. As shown in panel
B, the point estimates for both task expertise change and task quantity change are slightly more
43precise but not qualitatively different from the main estimates in Table 5A when these outliers are
trimmed.
Figure 13: Changes in Task Expertise, Task Quantities, and Occupational Employment,
1980–2018: Distinguishing between Task Removal and Task Addition: Binscatters
∆ ln EMPj= α+ β1∆XPTsub
j + β2∆XPTadd
j + β3∆TASKsub
j + +β4∆TASKadd
j + γJ(j) + ϵj
A. Expertise Change: Task Removal B. Expertise Change: Task Addition
Employment change (decadalized, log pts)
-0.25 0.00 0.25 0.50
Employment change (decadalized, log pts)
-0.25 0.00 0.25 0.50
-0.2σ -0.1σ 0.0 0.1σ 0.2σ
Expertise change due to removal
Slope: -0.72 (0.20), Partial R2: 0.45, N: 299
-0.2σ -0.1σ 0.0 0.1σ 0.2σ
Expertise change due to addition
Slope: -0.14 (0.35), Partial R2: 0.45, N: 299
C. Task Removal D. Task Addition
Employment change (decadalized, log pts)
-0.25 0.00 0.25 0.50
Employment change (decadalized, log pts)
-0.25 0.00 0.25 0.50
-5% 0 5% 10% 15%
Share tasks removed (%)
Slope: -1.42 (0.56), Partial R2: 0.45, N: 299
-5% 0 5% 10% 15%
Share tasks added (%)
Slope: 0.88 (0.82), Partial R2: 0.45, N: 299
Notes: This figure reports bin scatters of the employment-weighted conditional correlation between decadalized per-
cent employment growth and expertise change due to task change and task quantity change. Changes are decomposed
into task removal (left-hand side) and task addition (right-hand side). The corresponding regression specification is
column (5) panel B of Table 5 using 299 consistently defined Census occupations over 1980-2018. Four outliers are
trimmed. Each point is weighted by employment share in 1980.
Paralleling the analysis of expertise and wages above, Table 5C reports a richer model that permits
task change to affect employment through four channels: (1) expertise changes due to task removal;
(2)expertisechangesduetotaskaddition; (3)taskquantityremoval; and(4)taskquantityaddition.
Themodelpredictsthatexpertisechangewillhaveanegativerelationshipwithemploymentchange,
whether stemming from task removal or task addition. This is opposite to the prediction for
wages. Similar to the case for wages, however, we expect task quantity removal to predict falling
44employment and task quantity addition to predict rising employment. We estimate this model on
the restricted sample, excluding the four outliers.
As shown in Figure 13 and detailed in Table 5C, all four point estimates are qualitatively consistent
with predictions: task expertise gains predict employment reductions, regardless of whether these
gains stem from task removal or task addition; task removal predicts employment reductions; and
task addition predicts employment gains. Moreover, the data accept the null hypotheses that the
relationship between expertise change and employment change is symmetric for task removal and
addition, that it is equal and opposite for task quantity removal and addition, and that both hy-
pothesesholdjointly(Table5C).Wecaveatthatmostoftheidentifyingvariationfortheseestimates
stems from task removal, both through its effects on task expertise and task quantity. Task addition
also predicts employment change in the expected direction—whether operating through task ex-
pertise change or task quantity change—but the point estimates are imprecise. These bidirectional
tests are highly demanding and yet are largely confirmed. We view the evidence as supportive of
the model’s sharp and arguably counterintuitive employment predictions.
6 Task removal and expertise bifurcation: The case of routine
tasks
We have so far remained agnostic about the variation that drives correlations between employment
and wage changes on the one hand, and task expertise and task quantity changes on the other. This
section applies the expertise framework to causally assess the effect of changes in task expertise and
task quantities on occupational earnings and employment, focusing on the case of routine tasks.
As noted in the Introduction, many studies confirm that employment in routine task-intensive
occupations has substantially contracted in industrialized countries, as first noted by Autor et al.
(2003); Goos and Manning (2007).25 Yet wages have not consistently declined in routine task-
intensive occupations (Mishel et al., 2013; Green and Sand, 2015; Taber and Roys, 2019; Böhm,
2020; Böhm et al., 2024)). The expertise framework provides a novel, testable explanation for
this puzzle. Because routine tasks were among the most expert in some occupations but were
inexpert (supporting) in others, task expertise in routine task-intensive occupations should not
have uniformly risen or fallen as automation proceeded. Instead, it should have bifurcated, falling
in occupations where routine tasks were expert and rising in occupations where routine tasks were
primarily supporting. The expertise framework makes a strong prediction, accordingly: routine
task automation should have lowered wages in occupations where routine tasks were expert and
raised wages in occupations where routine tasks were inexpert.
We test this hypotheses in three stages: first, confirming that between 1977 and 2018, routine tasks
were disproportionately eliminated from occupations in which they were present; second, showing
25Influential contributions on routine task automation include Spitz-Oener (2006); Black and Spitz-Oener (2010);
Acemoglu and Autor (2011); Autor and Handel (2013); Goos et al. (2009); Frey and Osborne (2017); Arntz et al.
(2017); Acemoglu and Restrepo (2018b); Battisti et al. (2023).
45that routine task removal uniformly reduced task quantities in routine task-intensive occupations
while bifurcating task expertise demands in these occupations; and finally, demonstrating that
wages in exposed occupations bifurcated along with expertise requirements.
Following Autor et al. (2003), we partition the tasks in our data set into Abstract, Routine, and
Manual categories. We do this using GPT 4.1 using a prompt shown in Appendix A.2. The
results are summarized in Table 6.
26 Our classifier finds that in 1977, 33.2% of job tasks were
predominantlyabstract, 50.4% werepredominantlyroutine, and16.4% werepredominantlymanual.
These frequencies were substantially reshaped by task removal and addition over the next four
decades. We estimate that 66.1% of tasks removed between 1977 and 2018 were routine versus
only 16.8% of those added. Conversely, only 20.2% of tasks removed were abstract as compared
to 77.1% of those added. Finally, only a small share of tasks removed were manual, and an even
smaller share was added. In net, the prevalence of routine tasks declined from more than half in
1977 to less than one-third in 2018.
Table 6: The Distribution of Tasks across Abstract, Routine, Manual
Categories: Task Shares in 1977 and 2018, Tasks Removed and Tasks
Added between 1977 and 2018
A. Raw Task Count
Abstract (%) Routine (%) Manual (%)
Tasks In Use in 1977 33.24 50.37 16.38
Tasks In Use in 2018 53.58 32.22 14.19
Removed Tasks in 1977 20.22 66.06 13.72
New Tasks in 2018 77.11 16.77 6.12
B. Employment Weighted
Abstract (%) Routine (%) Manual (%)
Tasks In Use in 1977 37.33 41.88 20.79
Tasks In Use in 2018 49.02 36.30 14.68
Removed Tasks in 1977 43.67 46.32 10.02
New Tasks in 2018 71.65 20.56 7.79
Notes: Panel A displays the share of the raw count of tasks, without reference to occu-
pation. Panel B display the employment weighted shares. For removed and new tasks,
the average shares are obtained by weighing by employment scaled by the share of re-
moved/new tasks in that occupation.
We use the systematic elimination of routine tasks between 1977 and 2018 to provide identifying
variation for changes in task expertise and task quantities by occupation. For each occupation, we
26To evaluate this classifier, we conducted a manual review of 100 of these tasks and agreed with GPT’s classification
in 89% of cases.
46calculate two routine task exposure indices:
∆XPTj ≡XPTnr
j,1977−XPTj,1977
∆TASKj ≡1−N1977
j∈nr/N1977
j.
where XPTnr
j,1977 is the average expertise of non-routine tasks in occupation j in 1977. We refer to
the first term above, ∆XPTj, as expertise exposure, equal to the change in the expertise level of
occupation j in 1977 if all of its routine tasks were hypothetically removed. We refer to the second
term, ∆TASKj, as task (loss) exposure, equal to the percentage of tasks lost by j if all routine
tasks present in 1977 were removed.
Table 7: The Relationship between Occupational Exposure to Expertise Change and Task
Change from Routine Task Removal in 1980, and Realized Changes in Expertise and Task
Quantities, 1980–2018
(1) (2) (3) (4) (5)
A. Net Change in Task Expertise (σ)
Expertise Gain Exposure 0.052∗∗∗ 0.036∗∗ 0.039∗∗∗
(0.010) (0.011) (0.011)
Task Loss Exposure 0.129∗∗∗ 0.154∗∗ 0.173∗∗∗
(0.032) (0.053) (0.052)
Adjusted R-squared 0.078 0.113 0.050 0.108 0.143
B. Net Change in Task Quantity (%)
Expertise Gain Exposure−0.005−0.005−0.006
(0.004) (0.004) (0.004)
Task Loss Exposure−0.082∗∗∗
−0.040−0.043∗
(0.013) (0.020) (0.021)
Occupation Group FE × × ×
Adjusted R-squared 0.001 0.235 0.117 0.242 0.244
Observations 300 300 300 300 300
Notes: Standard errors in parentheses. All regressions are weighted by employment hours in 1980. Expertise gain
exposure is calculated as the hypothetical change in expertise (normalized to correspond to one standard deviation in
1980) had all routine tasks in an occupation been removed. Task loss exposure is based on the share of routine tasks
in an occupation in 1980. For Panel A, the outcome variable is the observed net change in expertise (normalized
to correspond to one standard deviation in 1980). For Panel B, the outcome variable is the observed net change in
task volume. All measures are decadalized for consistency. Columns (2), (4) and (5) include 12 broad occupational
group dummies. Three occupations with 100% routine share (namely, typists, mail carriers for postal services and
bank tellers) are excluded from the regression since the expertise for those occupations if all their routine tasks were
removed is undefined.
47To evaluate the predictive power of expertise change exposure and task loss exposure for observed
expertise and task quantity changes, we estimate models of the form:
∆Yj= α+ β1∆XPTj + β2∆TASKj + γJ(j) + ϵj, (23)
WeexcludethreeoccupationswhereXPTnr
j,1977 and∆XPTj areundefinedbecause100% oftasksare
classified as routine (Typists, Mail carriers for postal services, and Bank tellers). As shown in Table
7 Panel A, expertise exposure, ∆XPTj, is a robust predictor of realized changes in task expertise,
∆XPTnet
j . The column (1) point estimate ofˆ
β1
XPT = 0.052 (se = 0.010) in Table 7A indicates that
each 1σof expertise exposure generated a 0.05σrealized change in occupational expertise.Task loss
exposure, ∆TASKj, also predicts expertise gains. The column (3) point estimate ofˆ
β2
XPT = 0.129
(se = 0.032) indicates that each 10% of task loss exposure predicts a gain of 0.013 in task expertise,
suggesting that most routine tasks were relatively inexpert for their occupation.
The next panel of Table 7 Panel B reports analogous estimates for changes in task quantities.
Occupations with higher routine task exposure, ∆TASKj, saw a significantly larger loss in job tasks
between 1977 and 2018, withˆ
TASK
β2
=−0.082 (se = 0.013). This is consistent with expectations.
But occupations with higher expertise exposure, ∆XPTj, did not see a differential loss of job tasks
between 1977 and 2018 (column 3), withˆ
β1
TASK = 0.005 (se = 0.005). This pattern is logical:
neither the sign nor magnitude of the expected change in task expertise from routine task removal
depends on the share of tasks at risk for removal (or the share removed).
We argued above that routine task automation should polarize occupational expertise demands.
Figure 14 establishes this claim by plotting the relationship between expertise change exposure,
∆XPTj andrealizedexpertisechange, ∆XPTnet
j fortwodistinctgroupsofoccupations: thosewhere
expertiseispredictedtofallduetoroutinetaskremoval(∆XPTj<0)andthosewhereitispredicted
to rise (∆XPTj > 0).27 As shown in the upper two panels of Figure 14, task expertise exposure
significantly predicts occupational expertise loss in the subset of occupations where ∆XPTj is
negative, and it significantly predicts occupational expertise gain in the subset of occupations
where ∆XPTj is positive. These slopes are of roughly equal and opposite magnitude. Notably,
the count of occupations is closely perfectly balanced between those with positive versus negative
predicted values of expertise change. Nothing in our data construction enforces this regularity.
27There are 21 occupations which we identify to have no routine tasks in 1980. These are excluded from the figure.
48Figure 14: Changes in Occupational Expertise and Earnings, 1980–2018, versus Occupational
Exposure to Expertise Change from Routine Task Removal: Distinguishing between Occupations
Predicted to Lose and Gain Expertise
A. Expertise Loss: Routine Task Removal B. Expertise Gain: Routine Task Removal
Expertise change due to task removal
-0.10σ -0.05σ 0.0 0.05σ 0.10σ 0.15σ
Expertise change due to task removal
-0.10σ -0.05σ 0.0 0.05σ 0.10σ 0.15σ
0.0σ -0.2σ -0.4σ -0.6σ -0.8σ -1σ
Expertise exposure: Δ XPT < 0 if routine tasks removed
Slope: -0.05 (0.02), Partial R2: 0.07, N: 127
0.0σ 0.2σ 0.4σ 0.6σ 0.8σ 1σ
Expertise exposure: Δ XPT > 0 if routine tasks removed
Slope: 0.09 (0.02), Partial R2: 0.10, N: 173
C. Wage Change: Routine Task Removal D. Wage Change: Routine Task Removal
Wage change (decadalized, log pts)
-0.05 0.00 0.05 0.10
Wage change (decadalized, log pts)
-0.05 0.00 0.05 0.10
0.0σ -0.2σ -0.4σ -0.6σ -0.8σ -1σ
Expertise exposure: Δ XPT < 0 if routine tasks removed
Slope: -0.05 (0.01), Partial R2: 0.12, N: 127
0.0σ 0.2σ 0.4σ 0.6σ 0.8σ 1σ
Expertise exposure: Δ XPT > 0 if routine tasks removed
Slope: 0.05 (0.02), Partial R2: 0.03, N: 173
Notes: Figure reports binscatters of the conditional correlation between realized changes in occupational expertise
between 1980 and 2018 in panels A and B and expertise change exposure for negative values of expertise change
exposure (∆XPTj < 0) in panel A, and for positive values of expertise change exposure (∆XPTj > 0) in panel B.
Panels C and D present analogous binscatters for changes in log wages. All plotted variables partial out the 12 major
occupation dummies used above (one omitted). Observations are split into negative and positive values of expertise
change exposure after partialing. Estimates are weighted by occupational employment shares in 1980.
The final two panels of Figure 14 complete the argument. Panel C documents that relative wages
fell in occupations predicted to lose expertise from routine task removal, while Panel D shows
that relative wages rose in occupations predicted to gain expertise from routine task removal.
These point estimates are significant and symmetric on both sides of this prediction (∆XPTj<0,
∆XPTj>0), and again are robust to inclusion of broad occupation main effects. Routine task
removal bifurcated occupational expertise demands—and wages along with them. All regression
specifications include 12 broad occupational group dummies.
We report a final set of detailed estimates for both wages and employment in Table 8. The
49first three columns of panel A, containing wage estimates, confirms that (positive) task expertise
exposure strongly predicts wage gains while task loss exposure strongly predicts wage declines.
The corresponding three columns of panel B for employment present estimates in the expected
direction: positive task expertise exposure predicts a decline in occupational employment, as does
greater task loss exposure. But neither point estimate is statistically significant.
Table 8: The Relationship between Occupational Exposure to Expertise and Task Quantity
Change in 1980 due to Routine Task Removal versus Realized Changes in Wages and
Employment between 1980–2018
Baseline Sample Dropping Outliers
(1) (2) (3) (4) (5) (6)
A. Wages
Expertise Gain Exposure 0.055∗∗∗ 0.053∗∗∗ 0.048∗∗∗ 0.046∗∗∗
(0.009) (0.009) (0.010) (0.010)
Task Loss Exposure−0.129∗∗
−0.103∗
−0.116∗∗
−0.101∗
(0.043) (0.041) (0.042) (0.041)
Adjusted R-squared 0.467 0.413 0.476 0.462 0.433 0.472
B. Employment
Expertise Gain Exposure−0.016−0.016−0.164∗∗∗
−0.163∗∗∗
(0.040) (0.040) (0.041) (0.041)
Task Loss Exposure 0.006−0.002 0.096 0.040
(0.186) (0.187) (0.173) (0.169)
Occupation Group FE × × × × × ×
Adjusted R-squared 0.404 0.404 0.402 0.445 0.414 0.443
Observations 300 300 300 296 296 296
Notes: Standard errors in parentheses. All regressions are weighted by employment hours in 1980. Expertise gain
exposure is calculated as the hypothetical change in expertise (normalized to correspond to one standard deviation
in 1980) had all routine tasks in an occupation been removed. Task loss exposure is based on the share of routine
tasks in an occupation in 1980. For Panel A, the outcome variable is the observed wage change in log points from
1980 to 2018. For Panel B, the outcome variable is the observed wage change in log points from 1980 to 2018.
All outcomes and predictors are decadalized for consistency. Three occupations with 100% routine share (namely,
typists, mail carriers for postal services and bank tellers) are excluded from all regressions since the expertise for
those occupations if all their routine tasks were removed is undefined. In columns (4) to (6), four more occupations
experiencing extreme task displacement and employment decline are also dropped from the sample. All columns
include 12 broad occupational group dummies.
The final three columns of each panel repeat these wage and employment estimates while trimming
the four outlying occupations highlighted above. Wage results are little affected by trimming: pos-
itive expertise exposure predicts rising wages; task loss exposure predicts falling wages. Trimming
substantially increases the precision of the employment estimates, however. As plotted in Figure
15A and reported in the final column of Table 8B, positive expertise exposure strongly predicts
declining employment, as the expertise model anticipates. The evidence that routine task removal
explains declining employment in routine task-intensive occupations is weaker, as shown in Fig-
ure 15B. Our estimates suggest instead that rising expertise requirements more than falling task
quantities contribute to falling employment in formerly routine task-intensive occupations.
50Figure 15: Occupational Employment Changes 1980–2018 versus Occupational Exposure to
Task Expertise Change and Task Quantity Change due to Routine Task Removal
A. Change in Expertise (σ) B. Change in Tasks (%)
Employment change (decadalized, log pts)
-0.5 0.0 0.5 1.0
Lathe/milling machine ops
Office/Computer/Telecom ops
Textile/Knitter ops
Telephone ops
Employment change (decadalized, log pts)
-0.5 0.0 0.5 1.0
Textile/Knitter ops
Lathe/milling machine ops
Telephone ops Office/Computer/Telecom ops
-1.0σ -0.5σ 0.0σ 0.5σ
Expertise change exposure
Slope: -0.16 (0.04), Partial R2: 0.05, N: 296
-8% 0% 8% 16% 24%
Task change exposure (%)
Slope: 0.04 (0.17), Partial R2: -0.00, N: 296
Notes: Figuresreportscattersoftheemployment-weightedconditionalpartialcorrelationbetweendecadalizedpercent
employment growth and expertise exposure to routine tasks (left-hand side) and task share exposure to routine tasks
(right-hand side). Three occupations with 100% routine share are excluded. The four outlier occupations we exclude
from regressions are plotted in gray. The corresponding regression specification is column (6) panel B of Table 8.
Twelve broad occupation group dummies are included.
7 Conclusions
Our analysis is motivated by a simple observation: automation of any given task can simultaneously
replace experts in some occupations and augment expertise in others. We build on this insight using
three conceptual pillars. The first is expertise, which denotes a worker’s capability to perform
specific tasks. The second is bundling: occupations bundle a range of tasks of different expertise
levels. The third is automation. Automation enables capital to perform an increasing range of
expert tasks.
From this foundation, our conceptual model shows how automation simultaneously replaces experts
and augments expertise. Automation raises productivity and wages of occupational incumbents by
performing their relatively inexpert tasks at reduced cost. Simultaneously, automation renders
some formerly expert occupations inexpert, meaning that any worker can perform their remaining
generic tasks. Employment initially rises in occupations as they become inexpert, owing to the
elimination of expertise requirements. Entry causes wages in newly inexpert occupations to fall the
level of all other inexpert occupations. As automation proceeds further, employment in these occu-
pations slowly contracts because productivity is higher in occupations that have become inexpert
more recently (i.e., are less obsolete). Automation is always output-increasing in the model but
never Pareto-improving. Which workers gain and which lose as automation advances depends on
whether automation makes their expertise scarcer, via capital-labor complementary, or redundant,
via capital-expertise substitution.
Our model makes strong predictions about the relationship between expertise wages and employ-
51ment that are distinct from both canonical human capital models and from contemporary task
models. Specifically, the model predicts that changing expertise requirements have countervailing
effects on wages and employment: automation that decreases expertise requirements reduces wages
but permits the entry of less expert workers; automation that raises requirements raises wages but
reduces the set of qualified workers.
We introduce a novel content-agnostic tool for measuring occupational expertise from job task
descriptions. ThistoolisgroundedintheEfficientCodingHypothesisandrequiresonlyinformation
on the statistical frequency and entropy of words occurring in commonplace usage. We introduce
a second tool for measuring longitudinal changes in occupational expertise. This tool uses word
embeddings—geometricrepresentationsofthesemanticcontentofwords—todeterminewhichtasks
have been removed, retained, and added to occupations across epochs without requiring that the
tasks are described consistently across time.
Analyzingdataonemploymentandearningsbyoccupation overfourdecades, weshow thatchanges
in occupational expertise, stemming from both the removal and addition of occupational tasks,
strongly predict changes in occupational wages. Moreover, the expertise requirements of tasks
removed from or added to an occupation affect wage levels independently of the quantity of tasks
added or removed present. Remarkably, both the removal of expert tasks the addition of inexpert
tasks predict relative wage declines in an occupation, while, conversely both the removal of inexpert
tasks and the addition of expert tasks predict occupational wage gains.
Ourmodelmakesthecounterintuitivepredictionthatoccupationswithincreasingexpertiserequire-
ments see falling employment (alongside rising wages), while occupations with declining expertise
requirements see rising employment alongside falling wages. The data robustly confirm this predic-
tion. Crucially, we find the opposite pattern for changes in task quantities. Occupations that gain
tasks expand and those that lose tasks contract. This is also opposite to the pattern for wages,
where increases in both task quantities and task expertise predict wage increases.
We apply the expertise framework to revisit and reinterpret the closely studied relationship between
automation of routine, codifiable tasks and changes in employment and wages in occupations that
were historically specialized in such tasks. Distinct from a large literature predicted on the as-
sumption that automation of routine tasks is deskilling, we show that routine task automation has
bifurcated occupational expertise demands by lowering wages and raising employment in occupa-
tions where routine tasks were relatively expert, while raising wages and lowering employment in
occupations where routine tasks were relatively inexpert.
Our core results also affirm key implications of the contemporary task model, which focuses on the
quantity rather than the content of the tasks that workers perform. Consistent with that model, we
document an important role for changes in task quantities in the evolution of employment and wage
setting. Nevertheless, our expertise framework suggests a complementary but distinct conceptual
focus for analyzing the relationship between automation and the value of labor: it is not merely
52the quantity of tasks performed by an occupation or demographic group that determines demand
for its labor, but also the scarcity of the expertise required to perform those tasks.
Our analysis focuses on evidence from recent economic history, specifically, the last four decades,
whichareassociatedwiththecomputerrevolution. Butthereisnothinginourmodelthatisspecific
to the computer era. The same conceptual framework can be equally well applied to other historical
and contemporary technological epochs, including for example, the First Industrial Revolution and
the rapidly advancing era of Artificial Intelligence. While the empirical evidence presented here—
based on a relatively coarse set of occupations studied over a relatively short interval—should be
viewed as illustrative rather than definitive, we believe that the expertise framework offers a general
tool for analyzing how the removal and addition of specific job tasks reshape the scarcity value of
human expertise within and across occupations, and in the labor market as a whole.
53References
Abrahams, S. and Levy, F. S. (2024). Could Savannah be the Next San Jose? The Downstream
Effects of Large Language Models. SSRN Working Paper.
Acemoglu, D. (2025). The Simple Macroeconomics of AI. Economic Policy, 40(121):13–58.
Acemoglu, D. and Autor, D. (2011). Skills, Tasks and Technologies: Implications for Employment
and Earnings. In Handbook of Labor Economics, volume 4, pages 1043–1171. Elsevier.
Acemoglu, D., Gancia, G., and Zilibotti, F. (2012). Competing Engines of Growth: Innovation and
Standardization. Journal of Economic Theory, 147(2):570–601.
Acemoglu, D., Kong, F., and Restrepo, P. (2024). Tasks at Work: Comparative Advantage, Tech-
nology and Labor Demand. Technical report, National Bureau of Economic Research.
Acemoglu, D. and Restrepo, P. (2018a). Artificial Intelligence, Automation, and Work. In The
Economics of Artificial Intelligence: An Agenda, pages 197–236. University of Chicago Press.
Acemoglu,D.andRestrepo, P.(2018b). TheRaceBetweenManandMachine: ImplicationsofTech-
nology for Growth, Factor Shares, and Employment. American Economic Review, 108(6):1488–
1542.
Acemoglu, D. and Restrepo, P. (2019). Automation and New Tasks: How Technology Displaces
and Reinstates Labor. Journal of Economic Perspectives, 33(2):3–30.
Acemoglu, D.andRestrepo, P.(2020). RobotsandJobs: EvidencefromUSLaborMarkets. Journal
of Political Economy, 128(6):2188–2244.
Acemoglu, D. and Restrepo, P. (2022). Tasks, Automation, and the Rise in US Wage Inequality.
Econometrica, 90(5):1973–2016.
Aghion, P., Antonin, C., Bunel, S., andJaravel, X.(2024). WhataretheLaborandProductMarket
Effects of Automation? New Evidence from France. Technical report, Centre for Economic Policy
Discussion Paper.
Aghion, P., Bunel, S., Jaravel, X., Mikaelsen, T., Roulet, A., and Søgaard, J. (2025). How Different
Uses of AI Shape Labor Demand: Evidence from France. In AEA Papers and Proceedings,
volume 115, pages 62–67. American Economic Association 2014 Broadway, Suite 305, Nashville,
TN 37203.
Aghion, P., Jones, B. F., and Jones, C. I. (2018). Artificial Intelligence and Economic Growth.
In The Economics of Artificial Intelligence: An Agenda, pages 197–236. University of Chicago
Press.
Agrawal, A., Gans, J. S., and Goldfarb, A. (2023a). Do We Want Less Automation? 381(6654):155–158.
Science,
54Agrawal, A. K., Gans, J. S., and Goldfarb, A. (2023b). The Turing Transformation: Artificial
Intelligence, Intelligence Augmentation, and Skill Premiums. Technical report, National Bureau
of Economic Research.
Applebee, A. N. (1993). Literature in the Secondary School: Studies of Curriculum and Instruction
in the United States. National Council of Teachers of English.
Arntz, M., Gregory, T., and Zierahn, U. (2017). Revisiting the Risk of Automation. Economics
Letters, 159:157–160.
Autor, D., Chin, C., Salomons, A., and Seegmiller, B. (2024). New Frontiers: The Origins and
Content of New Work, 1940–2018. The Quarterly Journal of Economics, 139(3):1399–1465.
Autor, D.andKausik, B.N.(2025). Wage-MaximizingAutomation. Technicalreport, MITWorking
Paper.
Autor, D. H. and Dorn, D. (2013). The Growth of Low-Skill Service Jobs and the Polarization of
the US Labor Market. American Economic Review, 103(5):1553–97.
Autor, D. H., Dorn, D., and Hanson, G. H. (2013). The China Syndrome: Local Labor Market
Effects of Import Competition in the United States. American Economic Review, 103(6):2121–68.
Autor, D. H. and Handel, M. J. (2013). Putting Tasks to the Test: Human Capital, Job Tasks,
and Wages. Journal of labor Economics, 31(S1):S59–S96.
Autor, D. H., Katz, L. F., and Kearney, M. S. (2006). The Polarization of the US Labor Market.
American economic review, 96(2):189–194.
Autor, D. H., Katz, L. F., and Kearney, M. S. (2008). Trends in us wage inequality: Revising the
revisionists. The Review of economics and statistics, 90(2):300–323.
Autor, D. H., Levy, F., and Murnane, R. J. (2003). The Skill Content of Recent Technological
Change: An Empirical Exploration. The Quarterly Journal of Economics, 118(4):1279–1333.
Barlow, H. B. (1961). Possible Principles Underlying the Transformation of Sensory Messages.
Sensory communication, 1(01):217–233.
Battisti, M., Dustmann, C., and Schönberg, U. (2023). Technological and Organizational Change
and the Careers of Workers. Journal of the European Economic Association, 21(4):1551–1594.
Becker, G. S. and Murphy, K. M. (1992). The Division of Labor, Coordination Costs, and Knowl-
edge. The Quarterly journal of economics, 107(4):1137–1160.
Black, S. E. and Spitz-Oener, A. (2010). Explaining Women’s Success: Technological Change and
the Skill Content of Women’s Work. The Review of Economics and Statistics, 92(1):187–194.
55Böhm, M. J. (2020). The Price of Polarization: Estimating Task Prices Under Routine-Biased
Technical Change. Quantitative Economics, 11(2):761–799.
Böhm, M. J., von Gaudecker, H.-M., and Schran, F. (2024). Occupation Growth, Skill prices, and
Wage Inequality. Journal of Labor Economics, 42(1):201–243.
Braxton, J. C. and Taska, B. (2023). Technological Change and the Consequences of Job Loss.
American Economic Review, 113(2):279–316.
Brynjolfsson, E.andMitchell, T.(2017). WhatCanMachineLearningDo? WorkforceImplications.
Science, 358(6370):1530–1534.
Brynjolfsson, E., Rock, D., and Syverson, C. (2021). The Productivity J-Curve: How Intangibles
Complement General Purpose Technologies. American Economic Journal: Macroeconomics,
13(1):333–372.
Caselli, F. and Manning, A. (2019). Robot Arithmetic: New Technology and Wages. American
Economic Review: Insights, 1(1):1–12.
Cavounidis, C., Dicandia, V., Lang, K., and Malhotra, R. (2024). The Nature of Technological
Change 1960-2016. Technical report, University of Warwick.
Chall, J. S. and Dale, E. (1995). Readability Revisited: The New Dale-Chall Readability Formula.
Brookline Books.
Combemale, C., Ales, L., Fuchs, E. R., and Whitefoot, K. S. (2024). How It’s Made: A General
Theory of the Labor Implications of Technological Change. Technical report, Carnegie Mellon
University.
Cremer, J., Garicano, L., and Prat, A. (2007). Language and the theory of the firm. The Quarterly
Journal of Economics, 122(1):373–407.
Dale, E. and Chall, J. S. (1948). A Formula for Predicting Readability: Instructions. Educational
research bulletin, pages 37–54.
Deming, D. J. (2021). The Growing Importance of Decision-Making on the Job. Technical report,
National Bureau of Economic Research.
Dessein, W. and Santos, T. (2006). Adaptive Organizations. Journal of Political Economy,
114(5):956–995.
Eloundou, T., Manning, S., Mishkin, P., and Rock, D. (2024). GPTs are GPTs: Labor Market
Impact Potential of LLMs. Science, 384(6702):1306–1308.
Feigenbaum, J. and Gross, D. P. (2024). Answering the Call of Automation: How the Labor
Market Adjusted to Mechanizing Telephone Operation. The Quarterly Journal of Economics,
139(3):1879–1939.
56Frey, C. B. and Osborne, M. A. (2017). The Future of Employment: How Susceptible are Jobs to
Computerisation? Technological forecasting and social change, 114:254–280.
Garicano, L. (2000). Hierarchies and the Organization of Knowledge in Production. Journal of
political economy, 108(5):874–904.
Garicano, L.andRossi-Hansberg, E.(2006). OrganizationandInequalityinaKnowledgeEconomy.
The Quarterly Journal of Economics, 121(4):1383–1435.
Garicano, L. and Rossi-Hansberg, E. (2015). Knowledge-Based Hierarchies: Using Organizations
to Understand the Economy. Annual Review of Economics, 7(1):1–30.
Gathmann, C.andSchönberg, U.(2010). HowGeneralisHumanCapital? ATask-BasedApproach.
Journal of Labor Economics, 28(1):1–49.
Goos, M. and Manning, A. (2007). Lousy and Lovely Jobs: The Rising Polarization of Work in
Britain. Review of Economics and Statistics, 89(1):118–133.
Goos, M., Manning, A., and Salomons, A. (2009). Job Polarization in Europe. American Economic
Review, 99(2):58–63.
Goos, M., Manning, A., and Salomons, A. (2014). Explaining Job Polarization: Routine-Biased
Technological Change and Offshoring. American Economic Review, 104(8):2509–2526.
Green, D. A. and Sand, B. M. (2015). Has the Canadian Labour Market Polarized? Journal of Economics/Revue canadienne d’économique, 48(2):612–646.
Canadian
Hampole, M., Papanikolaou, D., Schmidt, L. D., and Seegmiller, B. (2025). Artificial Intelligence
and the Labor Market. Technical report, National Bureau of Economic Research.
Hoffmann, F., Lee, D. S., and Lemieux, T. (2020). Growing Income Inequality in the United States
and other Advanced Economies. Journal of Economic Perspectives, 34(4):52–78.
Huckfeldt, C. (2022). Understanding the Scarring Effect of Recessions. American Economic Review,
112(4):1273–1310.
Ide, E. and Talamas, E. (2024a). Artificial Intelligence in the Knowledge Economy. In Proceedings
of the 25th ACM Conference on Economics and Computation, pages 834–836.
Ide, E. and Talamas, E. (2024b). The Turing Valley: How AI Capabilities Shape Labor Income.
arXiv preprint arXiv:2408.16443.
Jones, B. F. and Liu, X. (2024). A Framework for Economic Growth with Capital-Embodied
Technical Change. American Economic Review, 114(5):1448–1487.
Katz, L. F. and Autor, D. (1999). Changes in the Wage Structure and Earnings Inequality. In
Handbook of Labor Economics, volume 3, pages 1463–1555. Elsevier.
57Katz, L.F.andMurphy, K.M.(1992). ChangesinRelativeWages, 1963–1987: SupplyandDemand
Factors. The Quarterly Journal of Economics, 107(1):35–78.
Kogan, L., Papanikolaou, D., Schmidt, L. D., and Seegmiller, B. (2024). Technology-Skill Com-
plementarity and Labor Displacement: Evidence from Linking Two Centuries of Patents with
Occupations. Technical report, National Bureau of Economic Research.
Korinek, A. and Juelfs, M. (2022). Preparing for the (Non-Existent?) Future of Work. Technical
report, National Bureau of Economic Research.
Korinek, A. and Stiglitz, J. E. (2018). Artificial Intelligence and its Implications for Income Dis-
tribution and Unemployment. In The Economics of Artificial Intelligence: An Agenda, pages
349–390. University of Chicago Press.
Kwong, H. (2024). 7.4: Partial and Total Ordering. In A Spiral Workbook for Discrete Mathematics.
Mathematics LibreTexts. Accessed: 2025-06-02; Licensed under CC BY-NC-SA.
Lin, J. (2011). Technological Adaptation, Cities, and New Work. Review of Economics and Statis-
tics, 93(2):554–574.
Lipowski, C., Salomons, A., and Zierahn-Weilage, U. (2024). Expertise at Work: New Technologies,
New Skills, and Worker Impacts. ZEW Discussion Papers, 24.
Manning, S. (2024). The Impact of AI on Income Inequality in the United States. Brookings
Institution.
Michaels, G., Natraj, A., and Van Reenen, J. (2014). Has ICT Polarized Skill Demand? Evidence
from Eleven Countries over Twenty-Five Years. Review of Economics and Statistics, 96(1):60–77.
Mishel, L., Shierholz, H., and Schmitt, J. (2013). Don’t Blame the Robots: Assessing the Job
Polarization Explanation of Growing Wage Inequality. EPI-CEPR working paper.
Murnane, R. J., Willett, J. B., and Levy, F. (1995). The Growing Importance of Cognitive Skills
in Wage Determination. The Review of Economics and Statistics, 77(2):251–266.
Muro, M., Maxim, R., and Whiton, J. (2019). Automation and Artificial Intelligence: How Ma-
chines are Affecting People and Places. Brookings Institution: Metropolitan Policy Program.
Smith, A. (2000). The Wealth of Nations. Modern Library, New York. Originally published in
1776.
Spitz-Oener, A. (2006). Technical Change, Job Tasks, and Rising Educational Demands: Looking
Outside the Wage Structure. Journal of labor economics, 24(2):235–270.
Svanberg, M., Li, W., Fleming, M., Goehring, B., and Thompson, N. (2024). Beyond AI Exposure:
WhichTasksareCost-EffectivetoAutomatewithComputerVision? Available at SSRN 4700751.
58Taber, C. and Roys, N. (2019). Skill Prices, Occupations, and Changes in the Wage Structure for
Low Skilled Men. NBER Working Paper, (w26453).
U.S. Census Bureau (1915–2018). Census of Population: Alphabetical Index of Industries and
Occupations. US Bureau of the Census.
U.S. Department of Labor, Employment and Training Administration (1977). Dictionary of Occu-
pational Titles: Fourth Edition. U.S. Government Printing Office.
U.S. Department of Labor, Employment and Training Administration (2018). O*NET Database
(version 23.0). https://www.onetcenter.org/db_releases.html. Accessed 18 May 2025.
Violante, G. L. (2002). Technological Acceleration, Skill Transferability, and the Rise in Residual
Inequality. The Quarterly Journal of Economics, 117(1):297–338.
Webb, M. (2020). The Impact of Artificial Intelligence on the Labor Market. Working paper.
Zeno, S., Ivens, S. H., Millard, R. T., and Duvvuri, R. (1995). The Educator’s Word Frequency
Guide. Touchstone Applied Science Associates.
Zipf, G. K. (1949). Human Behavior and the Principle of Least Effort: An Introduction to Human
Ecology. Addison-Wesley Press, Cambridge, MA.
598 Appendix figures and tables
Figure A1: Flow of New Occupational Tasks Added between 1977 and 2018
(DOT and O*NET) versus Flow of New Occupational Titles Added (Census Alphabetical Index of
Industries and Occupations)
Count of titles added (log)
0.0 0.5 1.0 1.5
Subject instructors, college
Physicians
Computer software developers
Registered nurses
Taxi cab drivers and chauffeurs
Management support occupations
Cashiers
Architects
Primary school teachers
Veterinarians
Statistical clerks
Art performers
Dancers
Paper folding machine operators
Typists
Aerospace engineers
0 3% 6% 9% 12%
New tasks added (%)
Slope: 4.49 (1.36), Partial R2: 0.03, N: 296
Notes: This figure reports scatters of the employment-weighted conditional correlation be-
tween decadalized new titles added (y-axis) and share task added (x-axis). Seven out of the
total 303 occupations with no new titles added between 1980-2018 are excluded. New occu-
pation tasks added are measured following Autor et al. (2024).Figure A2: The Occupation-Level Relationship between Net Task Change
and Net Expertise Change, 1980–2018
Notes: This figure reports scatters of the employment-weighted correlation between net ex-
pertise change and net task share changes. We do not plot the regression fit because the
statistical relationship between these series is essentially null.
Figure A3: Expertise and Employment Changes by Occupation between 1980 and 2018:
Binscatters with Employment Outliers Highlighted
A. Change in Expertise (σ) B. Change in Tasks (%)
Employment change (decadalized, log pts)
-0.6 -0.4 -0.2 0.0 0.2 0.4 0.6 0.8
Textile/Knitter ops
Office/Computer/Telecom ops
Telephone ops
Lathe/milling machine ops
Employment change (decadalized, log pts)
-0.6 -0.4 -0.2 0.0 0.2 0.4 0.6 0.8
Textile/Knitter ops
Telephone ops
Office/Computer/Telecom ops
Lathe/milling machine ops
-0.30σ -0.15σ 0.00 0.15σ 0.30σ
Net Expertise change
Slope: -0.70 (0.23), Partial R2: 0.03, N: 299
-8% -4% 0 4% 8%
Net task change (%)
Slope: 3.57 (0.52), Partial R2: 0.13, N: 299
Notes: Figures report scatters of the employment-weighted correlation between decadalized percent employment
growth and net expertise change (left-hand side) and net task change (right-hand side). The four outlier occupations
we exclude from regressions are plotted in gray.
61Table A1: Levels and Changes of Expertise, Log Wage, and Employment Share by Education
and Sex, 1980 – 2018
Education, Sex XPT (σ) ln(Wage) % Employment
1980 100×∆decade 1980 ∆decade 1980 ∆decade
< High School−0.22 0.31 2.55−0.01 20.86−3.48
(0.04) (0.12) (0.01) (0.00)
Men−0.07 0.23 2.67−0.02 22.26−3.50
(0.05) (0.14) (0.02) (0.01)
Women−0.52 0.50 2.28 0.02 18.39−3.30
(0.05) (0.22) (0.01) (0.00)
High School−0.07 0.91 2.71 0.00 36.04−2.55
(0.04) (0.16) (0.01) (0.00)
Men 0.12 0.37 2.87−0.02 33.53−1.21
(0.05) (0.15) (0.01) (0.00)
Women−0.33 1.75 2.47 0.03 40.47−4.56
(0.06) (0.29) (0.01) (0.00)
Some College 0.08 1.03 2.78 0.02 22.76 1.99
(0.04) (0.18) (0.01) (0.00)
Men 0.24 0.52 2.93 0.01 21.80 1.88
(0.05) (0.19) (0.01) (0.01)
Women−0.16 1.67 2.55 0.05 24.44 2.02
(0.06) (0.31) (0.01) (0.01)
College 0.22 0.66 3.06 0.05 10.61 3.07
(0.04) (0.19) (0.01) (0.01)
Men 0.42 0.61 3.19 0.05 11.26 2.56
(0.05) (0.25) (0.01) (0.01)
Women−0.20 0.73 2.78 0.09 9.48 3.79
(0.07) (0.31) (0.01) (0.01)
Graduate 0.28 0.88 3.20 0.10 9.73 0.97
(0.05) (0.20) (0.01) (0.01)
Men 0.50 1.11 3.28 0.11 11.15 0.27
(0.06) (0.27) (0.02) (0.01)
Women−0.32 0.58 2.98 0.11 7.22 2.05
(0.07) (0.30) (0.01) (0.01)
Notes: Standard errors in parentheses. Decadalized changes are reported for expertise, log
wages, and groups’ employment shares. Changes of XPT are decadalized and multiplied by
100 for clarity. XPT changes only report the net changes due to task removal and addition.
All descriptive statistics are weighted by the demographic group’s employment hours in the
occupations in the corresponding year.
62Table A2: Examples of Tasks Added and Removed between 1977–2018
Occupation Task Description XPT(σ) Class
Recording engineer Threads tape through recording device or places blank
disk on turntable -0.108 RM
Salesperson, millinery Fits hats on customer -2.642 NI
Transcribing-machine operator Types message heard through earphones -0.848 RC
Vault attendant Stamps exit time on customer’s access slip -2.492 RC
Classified-ad clerk ii Computes and records total number of lines expired and
number of lines for new advertisements -1.833 RC
Transcribing-machine operator Types message heard through earphones -0.848 RC
Automobile tester Applies inspection sticker to vehicles that pass and
rejection sticker to those that do not 2.421 RM
Horseshoer May forge steel bar into shoe -0.061 NM
Bottling-line attendant Wipes excess glue and moisture from bottles -0.462 RM
Occupation Task Description XPT(σ) Class
63
PR and Fundraising Managers Manage in-house communication courses. Online Merchants Determine location for product listings to maximize
exposure to online traffic. Video Game Designers Balance and adjust gameplay experiences to ensure the
critical and commercial success of the product. Bioinformatics Scientists Create or modify web-based bioinformatics tools. Acupuncturists Apply moxibustion directly or indirectly to patients using
Chinese, non-scarring, stick, or pole moxa. Manipulate and enhance scanned or digital images to
Photographers
create desired effects, using computers and specialized
software.
Word Processors and Typists Transmit work electronically to other locations. Align photo mask pattern on photoresist layer, expose
Semiconductor Processors
pattern to ultraviolet light, and develop pattern, using
specialized equipment.
-3.924 NI
4.918 NC
0.567 NC
0.273 NC
4.921 NM
2.458 NC
0.539 RC
0.683 RM
Notes: This table shows examples of tasks added and removed. Tasks are classified by GPT 4.1 as being either routine manual (RM), routine cognitive (RC),
nonroutine manual (NM), nonroutine cognitive (NC) or nonroutine interpersonal (NI).A Proofs and additional results
A.1 Proofs
Proof of Lemma 1. Write the labor demand curve in occupation ϕ as
w(ϕ,L(ϕ)) = Y 1−α(ϕ)
L(ϕ) (r/η)α(ϕ)(1−λ)
.
To prove the first statement, suppose for sake of contradiction that the equilibrium labor demands
L(ϕ)∗and L(ϕ′)∗are such that
1
λ−α(ϕ)(λ−1)
w(ϕ′,L(ϕ′)∗) >w(ϕ,L(ϕ)∗)
for some ϕ,ϕ′∈(0,1) s.t. ϕ>ϕ′. Since w(ϕ,L) is monotone decreasing in L and w(ϕ,L) →∞as
L→0, there must exist some B >0, s.t. ∀L<B,
w(ϕ′,L(ϕ′)∗) ≤w(ϕ,L)
and thus L(ϕ)∗≥B >0. Consequently, there exists some i∈W s.t. o(i) = ϕ and
Ei ≥o(i) = ϕ>ϕ′
.
This directly contradicts the worker-optimization condition in equation (13).
For the second statement, suppose
w(ϕ′,L(ϕ′)∗) >w(ϕ,L(ϕ)∗)
for some ϕ,ϕ′ ∈(0,I]. By the same argument as above, we have that L(ϕ)∗ > 0. That is, in
equilibrium, there exists some i∈W s.t. o(i) = ϕ. But since Ei ≥I ≥ϕ′, equation (13) is again
contradicted.
The proof of Proposition 1 relies on Lemma 2 below:28
Lemma 2. Suppose that all markets except labor markets are in equilibrium.29 Suppose that As-
sumption 6 holds and consider the marginal revenue product of labor in an occupation ϕat L(ϕ) =
¯
L.
¯
We denote this quantity by w(ϕ,
L). We have that ∀ϕ∈(0,1),
∂
∂ϕw(ϕ,
¯
L) >0.
28Recall that η is the productivity of capital relative to labor, measured in efficiency units. The lower bound¯
η
provided in Lemma 2 guarantees that wages in expert occupations rise as automation advances. This is akin to
Lemma 3 in Autor and Kausik (2025), which shows that if capital is sufficiently productive, wages in the two-factor
CES model rise as the labor share falls.
29That is, labor markets may or may not be in equilibrium.
64Proof of Lemma 2. Begin by taking the logarithm of w(ϕ,
¯
L) :
ln w(ϕ,
¯
ln Y/
¯
L 1−α(ϕ) η/rα(ϕ)(λ−1)
L) =
λ−α(ϕ) λ−1 (24)
For
¯
g(α) := Y/
L 1−α η/rα(λ−1)
, and
h(α) := λ−α λ−1 ,
we can write equation (24) as
ln w(ϕ,
¯
L) = f(α(ϕ)) := ln g α(ϕ)
h α(ϕ).
Since α(ϕ) is strictly increasing in ϕ, it suffices to show that f(α) increases in α. Taking the
derivative with respect to α gives
f′(α) = g′(α)
h′(α) ln g(α)
g(α)h(α)−
h(α)2
1
=
h(α)2 h(α)g′(α)
g(α)−h′(α) ln g(α).
Hence,
f′(α) >0 ⇐⇒ h(α)g′(α)
g(α) >h′(α) ln g(α)
⇐⇒
h(α)
h′(α)
⇐⇒ α−
g′(α)
g(α) <ln g(α)
λ
λ−1 (λ−1) ln η/r−
1
1−α
1
⇐⇒ −λln η/r <
1−α
λ
α−
λ−1 + ln Y/
¯
L 1−α
1
λ
<ln Y/
¯
L 1−α η/rα(λ−1)
⇐⇒ η>r
1−α
¯
L
Y
−
exp
λ−α(λ−1)
λ(λ−1)(1−α).
Recall that α(ϕ) ≤I, ∀ϕ∈(0,1) and notice that
∂
λ−α(λ−1)
=
∂α
λ(1−α)(λ−1)
λ−α(λ−1)
λ(1−α)(λ−1) ≤
and
1−α−
1
λ(λ−1)(1−α)2 >0, so
λ−I(λ−1)
λ(λ−1)(1−I),
1
1
λ ≤ 1−I−
λ
.
65λ
To show that ∂f α(ϕ)
∂α(ϕ) >0, ∀ϕ∈(0,1), it is therefore sufficient to show that
1
η>r
1−I
¯
L
Y
−
exp
λ−I(λ−1)
λ(1−I)(λ−1). (25)
Since capital markets are in equilibrium, we have:
r¯
K=
1
0
α(ϕ)Y(ϕ)p(ϕ)dϕ
= Y
≤Y
1
λ
1
0
1
λI
1
0
α(ϕ)Y(ϕ)λ−1
λ dϕ
Y(ϕ)λ−1
λ dϕ
= YI ⇐⇒ r≤
IY
¯
K
.
Further, write
Y(ϕ) = L(ϕ)
1−α(ϕ)
1−α(ϕ) ηK(ϕ)
α(ϕ)
α(ϕ)
≤
L(ϕ)
1−α(ϕ)∗
1−α(ϕ)∗
ηK(ϕ)
α(ϕ)∗
α(ϕ)∗
(26)
where
α(ϕ)∗= arg max
α∈(0,I)
L(ϕ)
1−α
= I, ηK(ϕ)
ηK(ϕ) + L(ϕ).
1−α ηK(ϕ)
α
α
Substituting α(ϕ)∗into (26) yields
ηK(ϕ)
Y(ϕ) ≤ ηK(ϕ) + L(ϕ)
= ηK(ϕ) + L(ϕ).
Consequently, Jensen’s inequality gives:
L(ϕ)
ηK(ϕ)+L(ϕ)
ηK(ϕ) + L(ϕ)
ηK(ϕ)+L(ϕ)
66Y
λ−1
λ =
1
Y(ϕ)λ−1
λ dϕ
0
≤
1
(L(ϕ) + ηK(ϕ))λ−1
λ dϕ
0
¯
¯
≤(
L+ η
K)λ−1
λ
.
Since
¯
L
¯
K
¯
L
I
η>
1−I exp
I
>
¯
K
⇐⇒¯
L< 1−I
¯
I η
K,
ρ−I
1−I
1−I (27)
we can further simplify and write:
λ−1
Y
λ−1
λ < η
¯
K
I
λ
. (28)
This shows that
1
1−I
λ
r
¯
L
Y
−
λ
exp
λ−I(λ−1)
λ(1−I)(λ−1)
1
≤Y
λ−1
λ
< η
¯
K
I
I
K
¯
1−I
L
¯
λ−1
λ I
K
¯
−
exp
1
1−I
L
¯
−
= η
λ−1
λ
I
1−I
−
1
λ
exp
λ−I(λ−1)
λ(1−I)(λ−1)
exp
λ−I(λ−1)
λ(1−I)(λ−1)
λ−I(λ−1)
λ(1−I)(λ−1) (29)
λ
¯
L
¯
K
67Finally, since
¯
L
¯
I
η>
¯
K
≥¯
L
¯
K
⇐⇒ η
1
λ >
⇐⇒ η>η
¯
L
¯
K
λ−1
λ
1−
I exp
¯
ρ−1
1−
¯
−
I
I
¯
I
1−I exp
ρ−1
−I
1−I
I
1−I
1
λ
exp
λ−(λ−1)I
λ(1−I)(λ−1)
¯
L
I
1−I
1
λ
exp
λ−I(λ−1)
λ(1−I)(λ−1),
¯
K
inequality (25) holds by (29).
Proof of Proposition 1. Denote the set of expert workers by
We := {i∈W : ei >I}.
Suppose that every expert worker chooses the most expert occupation they can access, i.e. o(i) = ei
¯
for all i ∈We, implying that L(ϕ) =
L for all ϕ > I. Suppose additionally that for all ϕ,ϕ′≤I,
L(ϕ) and L(ϕ′) are such that
w(ϕ,L(ϕ)) = w(ϕ′,L(ϕ′)) =: wg
as required in equilibrium by Lemma 1. We show that this is an equilibrium by showing that no
expert worker would benefit from deviating to o(i) <ei.
Notice that it suffices to show that no expert worker would benefit from deviating to working in an
inexpert occupation, i.e. that for all i∈We,
arg max ϕ≤ei
w(ϕ,L(ϕ)) >I.
If this statement holds, then for all i∈We,
arg max ϕ≤ei
w(ϕ,L(ϕ)) = arg max ϕ∈(I,ei]
w(ϕ,
¯
L).
Lemma 2 tells us that the objective function on the right hand side increases in ϕ and is therefore
maximized at ϕ= ei.
Toseethatexpertworkerswouldindeednotbenefitbydeviatingtoaninexpertoccupationo(i) ≤I,
write the labor demand curve for an inexpert occupation ϕ≤I as:
L(ϕ) = Y 1−α(ϕ)
1−λ
wg
w1−α(ϕ)
g r/ηα(ϕ)
.
By continuity of that function in ϕ and the observation that
I¯
L≤
I
0
L(ϕ)dϕ,
68there must exist some ϕ′≤I such that L(ϕ) ≥¯
L. In fact, the intermediate value theorem implies
¯
that there must exist a ϕ≤I such that L(ϕ) =
L. Consequently,
wg = w(ϕ′,L(ϕ′)) ≤w(ϕ′
,
¯
L).
By Lemma 2, we have
wg <w(ϕ,
¯
L)
for all ϕ>I which concludes the proof.
To see that this equilibrium is unique up to reallocations of i∈W\We respecting the constancy of
inexpert wages, suppose that workers occupational choices are such that there exists some expert
¯
worker i ∈We choosing o(i) < ei. If we still have L(ϕ) =
L for all ϕ > I, we have shown above
that i’s wage cannot be maximized at o(i), so we cannot be in equilibrium. We may therefore limit
our consideration to cases where L(ϕ) <¯
L for some ϕ>I. Let
Φ := ϕ>I : L(ϕ) <¯
L
be the set of all such occupations. There must exist some i∈W with ei ∈Φ such that o(i) <inf Φ.
If o(i) ≤I, we have shown above that
w(o(i),L(o(i))) <w(ei,
¯
L) <w(ei,L(ei)).
¯
If o(i) >I, we have L(o(i)) =
L by construction, and, by Lemma 2, it follows that
w(o(i),L(o(i))) = w(o(i),
¯
L) <w(ϕ′
,
¯
L) <w(ϕ′,L(ϕ′)).
Both cases imply that
o(i) / ∈arg max ϕ≤ei
w(ϕ,L(ϕ))
so we cannot be in equilibrium.
Proof of Proposition 2. This result follows immediately from the the proof of proposition 1 above.
¯
In particular, we have already shown that wg <w(ϕ,
L) for all ϕ>I.
¯
Proof of Proposition 3. To see that wϕ(I) is increasing on I ∈(0,ϕ) and I ∈(ϕ,
I] is immediately
evident from Corollary 1 and the proof of Lemma 2. We proceed by showing that there is a
discontinuous drop at I= ϕ. Let wg(I) denote the equilibrium generic wage as a function of I. Let
δ>0 and consider a state of automation I∗such that¯
I−I∗>δ. By continuity of wϕ(I∗) in ϕ on
(I∗
,1), there exists a ϵ∈(0,δ) sufficiently small so that for all ϕ∈(I∗,I∗+ ϵ),
wϕ(I∗) >wg(I∗) and wϕ(I∗+ δ) = wg(I∗+ δ).
Hence,
wϕ(I∗)−wg(I∗) =wϕ(I∗)−wg(I∗) + wg(I∗+ δ)−wg(I∗+ δ)
=wϕ(I∗)−wϕ(I∗+ δ)−wg(I∗) + wg(I∗+ δ)
⇐⇒ wϕ(I)−wϕ(I+ δ) >wϕ(Iδ)−wg(Iδ) + wg(I) + wg(I+ δ)
69Clearly
lim
δ→0
wϕ(Iδ)−wg(Iδ) >0.
Further, we know from corollary 1 that wg(I) is continuous on I ∈(0,
lim
δ→0
wg(I∗) + wg(I∗+ δ) = 0
¯
I], so
We therefore conclude that indeed
wϕ(I∗)−lim
δ→0
wϕ(I∗+ δ) >0.
The proofs of Corollaries 2 and 3 follow immediately from Propositions 2 and 3 respectively and
the observation that L(ϕ) is a continuous and strictly decreasing function of w(ϕ).
The last claim that remains to be proven is that, in equilibrium and under the constraint imposed
on ηin Lemma 2, cost-minimizing producers in all occupations ϕ∈(0,1) would choose to complete
automated tasks using capital rather than labor.
Proof. The statement above amounts to the equivalent statement that, in all occupations, the unit
cost of producing any task t ∈(0,1) with capital is less than that of producing it with labor.
Formally, since wg = minϕ∈(0,1) w(ϕ), this is true if and only if
r
η>
.
wg
¯
Suppose η>η. Holding L(ϕ) =
Lconstant, Lemma 2 states that the marginal revenue product of
labor increases in ϕ, i.e. for all ϕ∈(0,1), we have:
¯
L) >0
∂
∂ϕw(ϕ,
The proof of Lemma 2 can be directly applied to find lower bounds on η that extend this result to
cases where L(ϕ) is held constant at any different level˜
¯
L̸=
L. Yet, since η is a function of¯
L, the
extension to˜
¯
L̸=
L is not ensured by a general η>η. However, the inequality η>η is strict, and
¯
we have shown in the proof of proposition 1 that there exists some ϕ′≤I for which L(ϕ′) =
L in
equilibrium. Hence, by continuity of L(ϕ) on ϕ∈(0,I], there must exist some δ >0 such that for
any ϕ′′∈B(ϕ′,δ), the equilibrium labor demand L(ϕ′′) is sufficiently close to¯
L to ensure that for
˜
L:= L(ϕ′′), we also have:
˜
∂w(ϕ,
L)
∂ϕ >0
Given diminishing marginal revenue products of labor, implicit differentiation yields that for all
ϕ∈B(ϕ′,δ):
∂
∂ϕL(ϕ,wg) >0.
70Write the labor demand in occupation ϕ∈B(ϕ′,δ) as:
1
L(ϕ,wg) = 1−α(ϕ)
wg
Y(ϕ)λ−1
λ Y
λ
Taking the logarithm and differentiating gives:
λ−1
∂ln Y(ϕ)
λ
= ⇒
∂ϕ
∂ln Y(ϕ)
−
−
∂ϕ
α′(ϕ)
1−α(ϕ) >0
α′(ϕ)
1−α(ϕ) >0
Finally, write the nominal wage in occupation ϕ∈B(ϕ′,δ) as:
wg
p(ϕ)
=
wg
r
η
α(ϕ)
Differentiating both sides yields the following equivalence:
r
η>
⇐⇒
wg
∂
∂ϕp(ϕ) <0
The RHS of must be true since
∂
∂ϕp(ϕ) <0 ⇐⇒
∂
∂ϕY(ϕ) >0
and we showed above that
∂ln Y(ϕ)
∂ϕ >
α′(ϕ)
1−α(ϕ) >0.
We therefore conclude that
r
η>
wg
as required.
A.2 Additional results
Prompt to identify routine tasks (GPT 4.1)
You will be provided with a task description. Carefully read and understand the description,
then classify it into one of the following five categories based strictly on its characteristics.
71Use the following definitions:
1. Routine Cognitive Tasks (RC)
• Definition: Tasks involving cognitive processes that are codifiable, i.e., that be fully
specified through a set of ordered instructions. These tasks are procedural, structured,
repetitive, and rule-based, and often require precision.
• Examples: Data entry, basic bookkeeping, standardized clerical work, repetitive customer
service (e.g. bank teller).
2. Routine Manual Tasks (RM)
• Definition: Tasks that involve physical labor that are codifiable, i.e., can be accomplished
by following explicit rules. They rely on predictable, consistent operations with clear
steps.
• Examples: Picking/sorting, repetitive assembly.
3. Non-Routine Cognitive Analytic Tasks (NC)
• Definition: Non-codifiable tasks that require analytical skills. They are analytic in that
they require cognitive capacity such as judgment, strategic thinking, problem-solving,
creativity, intuition, visual processing and/or analysis. They are non-codifiable, meaning
that the rules for accomplishing the task are not sufficiently well understood to be
specified explicitly in computer code and executed by machines.
• Examples: Deciphering handwriting on a check, strategic planning, forming and testing
hypotheses, medical diagnoses, legal writing, complex problem solving, creative design.
4. Non-Routine Manual Tasks (NM)
• Definition: Tasks that involve physical work which cannot be fully codified due to the
need for on-the-spot adaptation, fine motor processing skills and/or situational judgment.
These tasks demand manual dexterity and flexibility in response to changing conditions.
• Examples: Skilled craftsmanship, janitorial services, truck driving, complex repair work.
5. Non-Routine Interpersonal Tasks (NI)
• Definition: Non-codifiable tasks that fundamentally require human interaction, communication,
and social skills. These social skills may include establishing and maintaining relationships,
guiding, directing and motivating subordinates, and coaching/developing others.
• Examples: Counseling, negotiation, persuading/selling, managing others, caregiving, relationship
building.
For the task description provided, carefully analyze its features. Then classify the task as
belonging to one of these categories, based on how well the task matches. Output only a single
class (e.g. RC, RM, NC, NM or NI).
Classify the following task description: (description)
72