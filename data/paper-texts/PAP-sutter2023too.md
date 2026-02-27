---
paper_id: PAP-sutter2023too
doi: 10.1162/rest_a_01394
source: mpg_pure
fetch_date: 2026-02-18
word_count: 22332
has_references: True
pure_item_id: item_3652804
---

This paper was originally published by MIT Press as:
Bortolotti, S., Soraperra, I., Sutter, M., & Zoller, C. (2025). Too lucky
to be true: Fairness views under the shadow of cheating. The
Review of Economics and Statistics, 107(3), 771– 785.
https://doi.org/10.1162/rest_a_01394

Supplementary material to this article is available. For more information see
https://hdl.handle.net/21.11116/0000-0011-5071-3

Nutzungsbedingungen:                             Terms of use:

Dieser Text wird unter einer Deposit-Lizenz      This document is made available under
(Keine     Weiterverbreitung      -     keine    Deposit Licence (No Redistribution - no
Bearbeitung) zur Verfügung gestellt.             modifications). We grant a non-exclusive,
Gewährt wird ein nicht exklusives, nicht         nontransferable, individual and limited right
übertragbares,       persönliches         und    to using this document. This document is
beschränktes Recht auf Nutzung dieses            solely intended for your personal, non-
Dokuments.      Dieses      Dokument       ist   commercial use. All of the copies of this
ausschließlich für den persönlichen, nicht-      documents must retain all copyright
kommerziellen Gebrauch bestimmt. Auf             information    and      other   information
sämtlichen Kopien dieses Dokuments               regarding legal protection. You are not
müssen alle Urheberrechtshinweise und            allowed to alter this document in any way,
sonstigen Hinweise auf gesetzlichen              to copy it for public or commercial
Schutz beibehalten werden. Sie dürfen            purposes, to exhibit the document in public,
dieses Dokument nicht in irgendeiner             to perform, distribute or otherwise use the
Weise abändern, noch dürfen Sie dieses           document in public. By using this particular
Dokument       für      öffentliche      oder    document, you accept the above-stated
kommerzielle     Zwecke       vervielfältigen,   conditions of use.
öffentlich ausstellen, aufführen, vertreiben
oder anderweitig nutzen. Mit der
Verwendung dieses Dokuments erkennen
Sie die Nutzungsbedingungen an.

Provided by:
Max Planck Institute for Human Development
Research Data & Information
rdi-service@mpib-berlin.mpg.de
                       Too Lucky to be True
       Fairness views under the shadow of cheating∗

             Stefania Bortolotti†                               Ivan Soraperra

            University of Bologna & IZA                  CREED – University of Amsterdam

               Matthias Sutter                                   Claudia Zoller

        Max Planck Institute for Research on               Management Center Innsbruck
       Collective Goods, Bonn & University of
         Cologne & University of Innsbruck

                                   November 21, 2022

                                           Abstract

Income inequalities within societies are often associated with evidence that the rich
are more likely to behave unethically and evade more taxes. We study how fairness
   ∗
     The authors thank Johannes Abeler, Loukas Balafoutas, Maria Bigoni, Alexander Cappelen,
Marco Casari, Gary Charness, Brian Cooper, Uri Gneezy, Matthias Heinz, James Konow, Michel
Maréchal, Johanna Möllerström, Pedro Rey-Biel, Bertil Tungodden, and participants at the CESifo
Area Conference on Behavioural Economics, EWEBE Workshop in Bertinoro, EEA Conference in
Lisbon, IMEBESS Workshop in Barcelona, C-SEB Workshop in Cologne, and MPI Munich Work-
shop, as well as seminar participants at UC San Diego, UC Santa Barbara, NHH Bergen, Loyola
Marymount University, WHU – Otto Beisheim School of Management, and University of Turin for
helpful comments and suggestions. We gratefully acknowledge the financial support from the C-
SEB Start-up Grant at the University of Cologne and the Deutsche Forschungsgemeinschaft (DFG,
German Research Foundation) under Germany’s Excellence Strategy – EXC 2126/1– 390838866.
Ivan Soraperra has received funding by the European Research Council (ERC) under the European
Union’s Horizon 2020 research and innovation program (grant agreement ERC-StG-637915). The
usual disclaimer applies.
   †
     Bortolotti   : University of Bologna, Piazza Scaravilli 2, 40126 Bologna, Italy; stefa-
nia.bortolotti@unibo.it, Phone: +39 051 20 9 2677.

                                                1
views and preferences for redistribution are affected when cheating may, but need
not, be the cause of income inequalities. In our experiment, we let third parties
redistribute income between a rich and a poor stakeholder. In one treatment, in-
come inequality was only due to luck, while in two others rich stakeholders might
have cheated. The mere suspicion of cheating changes third parties’ fairness views
considerably and leads to a strong polarization that is even more pronounced when
cheating generates negative externalities.

JEL classification: C91, D63, D81, H26
Keywords: fairness views, redistribution, unethical behavior, inequality, experi-
ment

1         Introduction

The unequal distribution of income within countries has become a major issue in the
academic and the public debate in recent years (Corak, 2013; Chetty et al., 2014;
Piketty, 2014). The general public, as well as the media, have often blamed the
rich of exploiting their advantageous position, often in unethical ways. The recent
financial crisis, illicit offshore financial activities such as the ones reported in the
“Panama papers”, and the practice at banks such as Wells Fargo to open up fake
bank accounts to meet the monthly targets of sales personnel,1 have rekindled this
belief. In line with general sentiment, recent studies have estimated that the unpaid
federal taxes by the top 1% amounts to $175 billion annually in the USA only (Guy-
ton et al., 2021), and that the 0.01% richest households evade about 25% of their
taxes. (Alstadsæter et al., 2019). More generally, Piff et al. (2012) also show that the
rich are more likely to break the law while driving and behave unethically in general.

    1
        http://fortune.com/2017/04/13/wells-fargo-report-earnings/

                                             2
   Here we focus on how the mere suspicion about the integrity of the fortunes
acquired by the rich can affect fairness views with respect to redistribution. It is
in fact important to understand how members of a society want to deal with such
inequalities and to which degree they are willing to reduce them through redistribu-
tion. We are particularly interested in situations in which it is untraceable whether
the source of a person’s fortunes may have originated from cheating or from honest
behavior. We hence talk about redistribution under the shadow of cheating and not
in the obvious presence of cheating. This is a paradigmatic case of redistribution
under limited information where the decision maker faces a trade-off between taking
away too much from a deserving claimant and not punishing an undeserving one.
Such a conundrum is pervasive in the judicial system, as well as in the welfare sys-
tem and in work relationships, and it is particularly occurring when the rule of law
is weak.

   To test how suspected cheating affects redistribution, we present a carefully con-
trolled experimental study in which we have rich and poor subjects, where in some
treatments the rich may, but need not, have acquired their income by cheating. We
study how unbiased third parties redistribute income from rich to poor subjects in
our experiment. It is a priori unclear if the shadow of cheating blurs the distinc-
tion between risk-takers and safe players, and if third parties are more inclined to
redistribute even among people who made different choices. Yet, it is important
to notice that by increasing redistribution, one takes away money not only from
cheaters, but also from potentially honest risk-takers. Moreover, third parties not
supportive of any redistribution might consider mere suspicion of cheating as a solid
enough reason to start promoting at least some redistribution to reduce inequality.

   In our experiment, we let stakeholders choose between a safe option and a po-

                                         3
tentially more profitable, but risky investment.2 We exogenously manipulate the
availability of cheating opportunities and hence the causes that can create income
disparities among stakeholders. In one treatment – called the Nature treatment,
which follows Cappelen et al. (2013) – the outcome of the risky investment is de-
termined by a random computer draw that yields either a high or a low income
for the stakeholder with 50% probability, respectively. The safe option, in contrast,
yields an intermediate income for sure. In the other treatments – Self-Report and
Externality – stakeholders face the same choice between a safe option and a risky
investment. Here, the investment’s outcome is resolved by the stakeholders them-
selves by flipping a coin and self-reporting the outcome. They are explicitly asked
to report the outcome – which yields either the high or low income with 50% prob-
ability – truthfully. Our request is, nonetheless, non-verifiable – mimicking many
real-world situations in which monitoring is too costly.3

       Both Self-Report and Externality capture situations where cheating is possible.
Yet, the treatments differ from one another with respect to the costs cheating im-
poses on other players. Self-Report is a very mild manipulation as no harm is done to
anybody in case of cheating. Misreporting the outcome of the lottery is a violation
of a rule but such a rule is not meant to protect the other parties. The Externality
treatment takes cheating a step forward: a stakeholder who cheats automatically
appropriates resources that were allocated to another (idle) player. This mimics
situations where the perpetrators benefit from their dishonest action at the expense
of other people’s income. Misreporting the high income here is a violation of a more
important rule aimed at protecting vulnerable parties.
   2
     This choice is intended to capture many real-world situations, ranging from job choices to
health or farming decisions, where subjects have to trade off risk and expected return. For instance,
one could think of people having to select either into a low-pay, but secure job, or a potentially
lucrative, but highly risky sector.
   3
     Contrary to most real-world examples, our design does not implement a probability of being
audited. As the likelihood of being caught and suffer sizable costs can be small, especially in
countries with a weak rule of law, we preferred to keep the design as simple as possible.

                                                 4
   After the stakeholders’ decisions, we let third parties – henceforth called specta-
tors – redistribute the total sum of earnings within a pair of stakeholders. Spectators
in the Self-Report and Externality treatment, however, cannot identify whether a
high income of a stakeholder was the consequence of either a lucky coin toss or
of misreporting the true (i.e., low) outcome of the coin toss. Although spectators
can form expectations about the likelihood of cheating, there is no certainty. This
ambiguity creates a difficult challenge for those spectators who want to eliminate
income inequality whenever the high income resulted from dishonest behavior, but
simultaneously want to refrain from redistribution if a stakeholder’s high income
was righteously acquired.

   We contribute to two strands of the literature on distributive justice. First, our
paper is related to the literature on the link between fairness views and the source of
inequality. It has been shown that fairness views depend on whether or not income
inequalities have been caused by differences in effort and hard work (Alesina and
Angeletos, 2005), or whether someone can be held accountable for one’s (mis)fortune
(Konow, 2000; Cappelen et al., 2013; Möllerström et al., 2015; Akbaş et al., 2019;
Lefgren et al., 2016; Tinghög et al., 2017). Judgments about the fairness of an in-
come distribution are also highly sensitive to the available information about, and
the subjective perception of, the income distribution (Kuziemko et al., 2015). More-
over, fairness views about the preferred extent of redistribution within a society have
been found to be affected by concerns about procedural fairness or efficiency (Bolton
et al., 2005; Balafoutas et al., 2013; Almås et al., 2020; Cassar and Klein, 2019), cul-
tural background or political orientation (Rey-Biel et al., 2011; Almås et al., 2020;
Cappelen et al., 2020; Konow et al., 2020; Klimm, 2019), or conflicts between social
classes (Fehr, 2018).

                                           5
       Second, our paper is related to two recent contributions on the role of limited
information on redistribution. Cappelen et al. (2018) also consider redistribution
in groups composed of honest and dishonest stakeholders.4 Unlike Cappelen et al.
(2018), we concentrate on choice egalitarianism5 and on cheating by the rich because
the sentiment against the so-called elites in many countries is fueled by the poorer
people’s concerns that the rich have achieved their fortunes also through dishonest
means. Cappelen et al. (2022) instead focus on a situation where there is uncertainty
about whether the source of inequality is merit or luck. Unlike the other two papers,
we consider ambiguity rather than uncertainty. This allows to test if fairness ideals
are correlated to beliefs about cheating. This is particularly relevant in light of the
recent literature on motivated beliefs and errors which suggests that agents tend to
rationalize their decisions in a favorable way, trying to maintain a positive image of
themselves (Di Tella et al., 2015; Exley, 2015; Zimmermann, 2020; Bašić and Quer-
cia, 2022; Exley and Kessler, 2022). Our setting creates some leeway for spectators
to misreport their perception of cheating to justify their fairness view. For instance,
libertarian spectators might trick themselves into believing that cheating is almost
non-existent. By doing so, they would not need to think they might be failing to
take away from someone who undeservedly claimed the high reward.

       Third, our paper is linked to the the flourishing literature on deception and cheat-
ing (Gneezy, 2005; Fischbacher and Föllmi-Heusi, 2013; Gächter and Schulz, 2016;
Abeler et al., 2019). Virtually all papers on this topic test how cheating depends
on different contextual cues and conditions, including the structure of incentives
(Conrads et al., 2013), loss avoidance (Grolleau et al., 2016), the nature of the task
(Kajackaite, 2018), the costs associated with cheating (Gneezy et al., 2018), or the
   4
    Their paper and ours were developed at the same time and independently of each other.
   5
    We enlarge the choice set by having a safe option, while in Cappelen et al. (2018) all group
members were asked to work on a real effort task and were then paid according to a lottery
system. Having a safe option is intended to mimic different types of behavior in the field, such
as in educational or professional choices, and it allows examining whether spectators condition
redistribution choices on stakeholders having made the same decisions or not.

                                               6
role of collaboration (Weisel and Shalvi, 2015). We take a completely different stand
on the problem by not focusing on the causes of cheating, but rather on the conse-
quences of dishonesty on fairness views and distributional preferences of unaffected
bystanders.

   We document a strong and significant shift in fairness views across treatments.
We use a discrete choice random utility model to estimate three types of spectators
(Cappelen et al., 2007, 2013): Libertarians are spectators who never redistribute,
independent of the degree of income inequality between stakeholders. Egalitarians
always redistribute resources equally, while Choice Egalitarians redistribute only
among stakeholders who chose the risky investment, but do not redistribute if one
stakeholder chose the risky option and the other the safe option. The share of
Libertarians is practically the same across all treatments, capturing about 40% of
spectators. However, the other types differ sharply across treatments. The share
of Egalitarians is three to four times larger in Self-Report and Externality than
in Nature. Hence, if income inequalities might have been generated from cheat-
ing behavior, the fraction of egalitarian fairness views increases substantially. At
the same time, Choice Egalitarians are much more frequent in Nature than in the
treatments where the shadow of cheating prevails. Overall, therefore, the shadow
of cheating leads to a strong polarization of fairness views where two diametrically
opposing views – Libertarians who never redistribute and Egalitarians who always
redistribute equally – become about equally strong in the population of spectators.

   Notably, beliefs about risk-taking and cheating are not distinguishable across
types. Libertarians, Choice Egalitarians, as well as Egalitarians infer that cheating
is present and a non-negligible share of stakeholders did not legitimately earn their
fortune. However, fairness views are not driven by beliefs – it is not the case that
Libertarians do not anticipate cheating while Egalitarians expect a disproportionate

                                         7
level of misbehavior on the side of the rich. This finding suggests that different types
of spectators react in contrasting ways to an otherwise equal level of dishonesty in
the society.

    The remainder of the paper is organized as follows. Section 2 describes the ex-
perimental design and data collection. Section 3 presents the aggregate results for
both stakeholders and spectators. Section 4 focuses on individual-level behavior
and reports the results of a discrete choice random utility model estimating fairness
views. Section 5 concludes.

2     Experimental design

Our design builds on Cappelen et al. (2013). We have two types of players – stake-
holders and spectators – and two stages. We start by presenting the details of the
first stage, in which stakeholders made their decisions. After that, we introduce
the three experimental treatments. We then explain the second stage where specta-
tors made a series of redistributive decisions. Finally, we describe the experimental
procedures.

2.1    Stage 1: Stakeholders’ risk-taking decisions

Each stakeholder independently had to make five ordered decisions between a safe
and a risky option. The risky option paid either a high income of 800 tokens or
a low income of 0 tokens. While the risky option remained fixed in all five de-
cisions, the intermediate income paid by the safe option varied across decisions.
This amount increased linearly from 100 tokens in the first decision to 500 tokens
in the fifth decision, making the safe option more attractive as the stakeholders
proceeded through the five decisions. After all five decisions had been made, the

                                           8
risky option – if chosen – was resolved for each decision separately. The resolution
of the risky option and its consequences depended upon the experimental treatment.

2.2    Experimental treatments

We ran three between-subjects treatments: Nature, Self-Report, and Externality.
The first two – Nature and Self-Report – differ only in the way in which the outcome
of the risky option was determined. The Externality treatment builds on Self-Report
and imposes a negative externality on another player in case of cheating.

   • In the Nature treatment, the outcome of the risky option was determined by
      a random draw performed by the computer. The probability of the high or
      low income was 50% for each level. The outcome of each random draw was
      shown to the stakeholder after all decisions between the safe and risky option
      had been made.

   • In the Self-Report treatment, the outcome of the risky option was determined
      by a self-reported coin toss. The coin tosses had to be performed only after
      all five decisions had been made. Stakeholders were asked to get a coin or to
      use an online website (justflipacoin.com) to flip a coin for each decision in
      which they had chosen the risky option. We explicitly requested stakeholders
      to report the results of the coin tosses truthfully (see Instructions in the Online
      Appendix). Misreporting was hence a clear violation of the rules. Under the
      assumption of honest reporting, our procedure guarantees the same likelihood
      (of 50%) of earning the high income across treatments, conditional on choosing
      the risky option. However, our request for honest reporting could not be
      enforced as there was no possibility to detect lies at the individual level (for
      further details, see the experimental procedure below). This set-up mimics
      situations in which rules are not enforceable or the cost of monitoring is too

                                           9
       large.

    • In the Externality treatment, the outcome of the risky option was determined
       by a self-reported coin toss as in Self-Report. This time, we built in an exter-
       nality of cheating. Each stakeholder was matched with an idle player whose
       earnings might depend on the choices of the stakeholder. The idle player was
       informed about the rules but was not eligible to make any decision. Stake-
       holders knew that the idle player received a bonus payment of either 0 or 800
       tokens which was determined as follows:

        (i) if the matched stakeholder chose the safe option, the earnings of the idle
             player were independently determined by a random draw of the computer
             and both outcomes (0 and 800 tokens) were equally likely;

        (ii) if the matched stakeholder chose the risky option, the earnings of the idle
             player were negatively correlated with the ones of the stakeholder. This
             means that if the stakeholder reported a winning coin toss, the matched
             idle player received the low income of 0 tokens. If the stakeholder reported
             a losing coin toss, the matched idle player received the high income of
             800 tokens.

    While the latter two treatments – Self-Report and Externality – both allow for
cheating, it is important to remark the differences between the two. In the Self-
Report treatment, one might see cheating as a rather innocent deviation from the
rules, as it does not entail any loss for any other player. In the Externality treat-
ment, falsely reporting a winning coin toss yields a high income for the stakeholder
at the expense of the idle player’s earnings. In this case, stakeholders are imposing
a negative externality on someone to (illegitimately) seek their own profit.6
    6
      Technically, a negative externality is always imposed on the idle player when a lucky draw is
reported (regardless of the true outcome). Here we refer to externalities with a narrower meaning
and consider the increase in the probability of imposing a negative externality. If there was no
change of misreporting the outcome of the coin flip, the possibility of imposing an externality on the
idle player would be 50%. When deciding to misreport the outcome of the draw, the stakeholder

                                                 10
    Note that in all treatments the rules used to resolve the outcome of the risky
option were common knowledge from the beginning of the experiment – i.e., before
stakeholders made any decision. We also informed stakeholders at the beginning of
the experiment that the study comprised two stages. For comparability, we use the
same wording as in Cappelen et al. (2013): “Stage 2 of the experiment concerns the
distribution of earnings from Stage 1. Details of the second stage will be provided
after the first stage is complete.” Only at the end of a session were stakeholders
informed about the rules of stage 2.

2.3     Stage 2: Spectators’ redistribution decisions

In stage 2, spectators decided how to redistribute the sum of earnings within a pair
of stakeholders. Each spectator had to make 20 redistribution decisions (see Table
A-3 in the Online Appendix). One of these redistribution choices was payoff relevant
for a pair of stakeholders, but spectators were not informed which one was relevant.
For each pair, the spectator was informed about the stakeholders’ choices (safe vs.
risky) and of the outcomes if the risky option had been chosen. It is important to
notice that spectators always redistributed between two stakeholders who faced the
same initial situation, meaning that the amount associated with the safe option was
the same for both stakeholders in the pair – the safe amount can change from one
decision to the other, but not within the same redistribution decision.7
increases such a probability to 100%. In addition, note that a fair minded stakeholder would
not choose the risky option and purposefully report a losing coin toss. In the absence of lying
costs, when choosing the lottery the stakeholder faces the choice to allocate 800 tokens to either
him/herself or to the idle player. Models of inequity aversion would predict that the stakeholder
would keep the 800 tokens (Fehr and Schmidt, 1999). When lying costs are high enough, instead,
the stakeholder would not misreport the outcome of the coin and, hence, he/she would never lie
downwards. If instead stakeholders have reputational concerns, they may report a losing coin toss
when choosing the lottery. In such a case the choice of the safe option is preferable for fair minded
stakeholders since it removes the reputational concerns and, at the same time, it gives a higher
payoff and reduces inequality. A sufficient condition is that advantageous inequality is disliked at
most as much as disadvantageous inequality.
   7
     Different safe levels were introduced for comparability with Cappelen et al. (2013) and to test
the robustness of fairness types estimated in Section 4.

                                                 11
       In the Externality treatment, for stakeholders who chose the risky option, the
earnings of the idle player were reported. If the stakeholder chose the safe option,
the consequences for the idle player read: “outcome determined by the computer.”
No further information about the exact amount for the idle player was given in this
case. When redistributing money between the two stakeholders (not between the
idle players with which the two stakeholders were paired), spectators could redis-
tribute the sum of the earnings of the two stakeholders from stage 1 in steps of 25
tokens. The payment for spectators themselves was a fixed amount and they were
not affected by the stakeholders’ decisions, and hence had no material self-interest
at stake. This avoids any kind of personal self-serving bias on the part of spectators
and allows us to elicit impartial and unbiased fairness views (Konow, 2000, 2009).

       In the Nature treatment, spectators were informed that the mechanism used to
determine the outcome of the risky option was a random draw performed by the
computer, yielding the high or low income with equal probability. In the Self-Report
and Externality treatments, instead, they were informed that stakeholders had to
self-report the outcome of a coin toss to resolve the risky option and that stakehold-
ers were requested to report their coin toss truthfully. In the Externality treatment,
spectators were also informed about the idle players and how their earnings were
determined.

2.4       Experimental procedures

Stakeholders. Stakeholders were recruited via Amazon Mechanical Turk (MTurk,
henceforth) using the behavioral research platform TurkPrime (Litman et al., 2017).8
   8
    MTurk participants – often referred to as “workers” – represent a massive dataset of potential
participants from a wide range of countries and with diverse backgrounds. Monetary incentives
for MTurk workers are often lower (at least in absolute terms, much less so in relative terms) than

                                                12
For our study, we recruited a total of 600 online participants - 120 in Nature and 240
each in Self-Report 9 and in Externality. In Externality, 120 online participants were
assigned to the role of stakeholders and the other 120 to the role of idle players. The
latter were asked to read the instructions given to the stakeholders and to answer
the same control questions. They were made aware of how their potential bonus
payment was generated but had no decision to make.

    Participation was restricted to subjects from the U.S. with a high completion
rate to minimize attrition.10 Decisions were collected via SoSci (Leiner, 2014). Only
participants who were able to answer all control questions correctly were allowed
to participate. After two incorrect trials, stakeholders were automatically excluded
from the study and were prevented from re-taking it. The stakeholders’ average
payment was about $2, including a $0.60 participation fee. The task lasted on aver-
age 8 minutes (implying an average hourly rate of about $15, which is comparable
to many laboratory experiments). Idle players spent on average 7 minutes until
completion, and earned on average $1.20, including a $.30 participation fee.

    We believe the task in Stage 1 is particularly well suited for MTurk for two main
reasons. First, the task is extremely simple and short, hence reducing potential
concerns about understanding and concentration. Second, conducting the experi-
ment on MTurk grants a degree of privacy to participants that would be difficult
to achieve in the lab. Stakeholders were identified by a code and they completed
their assignment over the internet from home or a place of their choice. Hence,
in the laboratory; however, there is evidence that reduced incentives have little or no effect on
behavior (Buhrmester et al., 2011; Horton et al., 2011; Litman et al., 2015).
   9
     Initially, we had 120 online stakeholders in Self-Report, as in the other two treatments. Af-
ter feedback from seminar participants, we added 120 more participants in Self-Report because
we wanted to collect beliefs among spectators. That also required additional data collection of
stakeholders on MTurk.
  10
     We recruited only experienced online workers. All of them had taken part in at least 50
previous assignments and had successfully completed at least 95% of these assignments. The
average completion rate was 97.5%.

                                               13
there was no possibility for the experimenter to observe the result of the coin toss
used in the Self-Report and Externality treatments to determine the outcome of the
risky option. Given the complete separation between participants and experimenter,
stakeholders could easily infer that the experimenter had no way to detect cheating.

Spectators. A total of 237 students from the University of Cologne participated
in our experiment. We first recruited 117 spectators divided in four sessions over
two consecutive days. Two sessions, with a total of 57 subjects, were assigned to the
Nature treatment.11 Two sessions, with a total of 60 subjects, were assigned to the
Self-Report treatment. On a later date, we run two additional Self-Report sessions
(including beliefs) with a total of 60 subjects. Finally, we had two further sessions,
with a total of 60 participants who were assigned to the Externality treatment.12 All
sessions were conducted at the Cologne Laboratory for Economic Research (CLER)
a few days after collecting data on MTurk. Subjects were recruited using ORSEE
(Greiner, 2015) and the experiment was programmed using z-Tree (Fischbacher,
2007). Upon arrival, subjects were randomly assigned to a cubicle and no form
of communication was allowed. A paper copy of the instructions was distributed
to spectators and instructions were read aloud to assure common knowledge (see
Online Appendix). Spectators could proceed to the proper experiment only after
having answered all control questions correctly. Socio-demographic characteristics
and personality traits (HEXACO Personality Inventory-Revised, Ashton and Lee
2009) were collected at the end of the experiment. Spectators were paid a fixed
amount of €10 for the redistribution part, including a show-up fee of €4. The av-
erage session lasted about 45 minutes.
  11
     Due to a low show-up rate in one Nature session, we have only 57 spectators in this treatment.
The number of pairs of stakeholders from MTurk was instead 60. The three extra-pairs were paid
exactly the amount they had earned in Stage 1, as if there was no redistribution.
  12
     Since not all sessions and treatments were properly randomized, we present the results of the
balance tests in Tables A-2 and A-1 in the Online Appendix. In the results section, additional
robustness tests are provided to account for the fact that not all sessions were randomized.

                                                14
   In two of the four Self-Report sessions (60 spectators) and in both Externality
sessions (60 spectators), we additionally elicited beliefs and risk aversion. After mak-
ing their redistribution choices, spectators were asked to answer the two following
questions about the stakeholders:

   • What is the percentage of participants in the online assignment that chose the
      risky option?

   • Consider now only the online participants who have chosen the risky option:
      what is the percentage of participants who reported Heads? Please recall that
      Heads yielded an income of 800 tokens and Tails 0 tokens.

   For the sake of simplicity, we elicited beliefs only for a safe level of 300 tokens.
Beliefs were incentivized with a stepwise quadratic scoring rule (see Instructions
in the Online Appendix) and six randomly selected spectators per session – of 30
subjects each – were paid based on one of the two questions.

   To elicit a spectator’s risk aversion (as a control variable for the redistribution
choices), we followed the task proposed by Eckel and Grossman (2008). Spectators
were presented with five options, of which they had to pick one. In each option,
there was a 50% chance of a low payoff and a 50% chance of a high payoff. The low
and high payoffs changed for each option. Higher expected payoffs were associated
with higher risk (see Figure C-5 in the Online Appendix). One randomly selected
spectator per session was paid for this task. On average, spectators earned addi-
tionally €4 from the belief-elicitation and risk task.

                                          15
3      Results: Aggregate results

3.1     Stakeholders’ risk-taking and cheating behavior

We focus on two main aspects: first, risk-taking behavior, and, second, the extent
of cheating in treatments where misreporting is possible. The bars in Figure 1 show
the relative frequencies with which stakeholders choose the risky option, conditional
on the income from the safe option (ranging from 100 to 500 tokens) and on the
treatment (left for Nature, right for Self-Report, bottom for Externality). We ob-
serve a clear downward trend in the relative frequencies of choosing the risky option
in all treatments, dropping from 75-79% for a safe income of 100 tokens to 17-27%
for a safe income of 500 tokens. A series of χ2 tests fail to reveal any significant
difference in risk-taking between Nature and Self-Report as well as between Nature
and Externality for any safe income level (the p-values range from p = 0.122 to
p = 0.875).13 For the comparison between Self-Report and Externality, χ2 tests re-
veal a significant difference only for the safe income level of 500 (p = .042), while the
other four comparisons are insignificant. The fraction of stakeholders who always
choose the safe option is also similar across all three treatments, with 17% in Nature,
20% in Self-Report and 18% in Externality. Moreover, stakeholders display a high
degree of consistency in their choices in all treatments, as less than 7% switch more
than once between the risky option and the safe option.

Result 1 The relative frequency of choosing the risky option is not significantly
different between Nature and the other two treatments. In all treatments, risk-taking
  13
    It is interesting to note that the possibility to report a favorable outcome at one’s discretion
does not induce a change in risk-taking behavior in Self-Report and Externality. Compared to
Nature, one would think that stakeholders in the two treatments with cheating opportunities only
switch from the safe option to the risky one, but not vice versa. However, if subjects have a
preference for being seen as honest, even risk-lovers could prefer to choose the safe option to avoid
looking dishonest when reporting a lucky draw. In line with the evidence by Abeler et al. (2019)
and Gneezy et al. (2018), our results suggest that direct costs of lying and reputation concerns are
not negligible for a sufficiently large fraction of stakeholders, which could explain that the relative
frequency of choosing the risky option does not differ between treatments.

                                                  16
                                                                  Figure 1: Relative frequency of risky choices and high income
                                                                               (a) Nature                                                                                                                                                                              (b) Self-Report
Relative frequency of risky option and high income (%)

                                                                                                                                                                                      Relative frequency of risky option and high income (%)
                                                         100

                                                                                                                                                                                                                                               100
                                                                                                                                                                                                                                                                                                           78.6
                                                         80

                                                                                                                                                                                                                                               80
                                                                                                                                                                                                                                                            ●
                                                                                                                                                                                                                                                             75.7                                73.5     ●
                                                                                                                                                                                                                                                                            69.4                ●
                                                                                                                                                                                                                                                                           ●
                                                                                                                                                                                                                                                                                     ●
                                                                                                                                                                                                                                                                                      67.2
                                                         60

                                                                                                                                                                                                                                               60
                                                                   49.5        50.6                                                             49.1    ●
                                                                                                                                                         51.6
                                                                  ●           ●                                   ●                                                   45.5
                                                                                                                                                                      ●
                                                         40

                                                                                                                                                                                                                                               40
                                                         20

                                                                                                                                                                                                                                               20

                                                                 79.2         69.2             47.5                                                     25.8        18.3                                                                                    75.4           72.1      52.1      28.3       17.5
                                                         0

                                                                                                                                                                                                                                               0

                                                                  100         200                      300                                              400         500                                                                                     100            200       300       400        500

                                                                              Income from safe option                                                                                                                                                                      Income from safe option

                                                          Frequency of        Frequency of high income                                                                                                                                          Frequency of               Frequency of high income
                                                                          ●                                                                                               Random                                                                                       ●                                      Random
                                                          risky option        with 95% Confidence Interval                                                                                                                                      risky option               with 95% Confidence Interval

                                                                                                                                                                          (c) Externality
                                                                                       Relative frequency of risky option and high income (%)

                                                                                                                                                  100

                                                                                                                                                               78.7                                                                                   80.0         ●
                                                                                                                                                                                                                                                                    81.2
                                                                                                                                                  80

                                                                                                                                                               ●                                                                                     ●
                                                                                                                                                                                      70.5
                                                                                                                                                                           ●
                                                                                                                                                                            67.7     ●
                                                                                                                                                  60
                                                                                                                                                  40
                                                                                                                                                  20

                                                                                                                                                            78.3           77.5      50.8                                                            33.3          26.7
                                                                                                                                                  0

                                                                                                                                                              100          200       300                                                             400           500

                                                                                                                                                                          Income from safe option

                                                                                                                                                   Frequency of            Frequency of high income
                                                                                                                                                                      ●                                                                                                Random
                                                                                                                                                   risky option            with 95% Confidence Interval

                                                                                                                                                                                   17
drops as the income from the safe option increases.

   Figure 1 also shows the relative frequency of getting the high income from the
risky option (see circles for averages and whiskers for confidence intervals). On the
left-hand side, we see that in the Nature treatment this relative frequency is not sig-
nificantly different from 50%, due to the fact that the outcome of the risky option
was determined by a random computer draw. On the right-hand side of Figure 1,
we note instead that in the Self-Report treatment stakeholders report having been
lucky in their coin toss significantly more often than chance would predict (see con-
fidence intervals in Figure 1). In fact, conditional on choosing the risky option, they
claim the high income in 72% of cases. Among all stakeholders in Self-Report, 32%
declared having been lucky in all instances where they chose the risky option. In
the bottom part of Figure 1, we can observe that the behavior in the Externality
treatment is remarkably similar to Self-Report. Among the stakeholders who chose
the risky option in Externality, 76% claimed the high income (significantly more
than predicted by a fair coin) and 35% of the stakeholders report to always have
been lucky. This seems to suggest that the presence of negative externalities did not
deter stakeholders from cheating.

Result 2 Many stakeholders cheat in the Self-Report and Externality treatments
as the observed fraction of stakeholders reporting the high income from the risky
option is above 70% and significantly larger than 50% in these two treatments. Yet,
stakeholders do not cheat to the full extent, as in roughly one quarter of the cases
they report the low income (of zero tokens) when they could have easily claimed the
high income.

                                          18
3.2       Spectators’ redistribution decisions

Our 237 spectators made a total of 4,740 redistribution decisions. In 316 cases, there
was nothing to redistribute because both stakeholders had earned the low income
of zero tokens from the risky option. In addition, there are 1,133 cases where both
stakeholders had the same positive income (either by having chosen the same safe
option or by having earned the high income from the risky option). In virtually
all of these instances (97.3%), spectators did not redistribute any income from one
stakeholder to the other, as they had the same income to begin with. Therefore, we
have a total of 3,291 (out of 4,740) cases with income inequality between the two
stakeholders. In the majority of these cases (59%), spectators modified the initial
distribution of earnings and their intervention was almost always aimed at reducing
disparities. Only in less than 5% of cases (169 in total) did they increase inequal-
ity. In this section, we focus on cases with strictly positive inequality and test for
treatment differences in the extent of redistribution. In section 4, we dig deeper into
individual-level behavior and study fairness views.

      To gain a first understanding of the effect of the shadow of cheating on the
aggregate level of redistribution, we consider a simple measure of redistribution
that we call Redistribution Index (RI) which is defined as follows:

                                             R      R
                                            πpre − πpost
                                        RI = R
                                            πpre − X/2

where πtR are the earnings for a stakeholder R before (t = pre) or after (t = post)
the redistribution stage, and X are the pair’s total earnings. We indicate as the
richer stakeholder R the person in the pair with the larger earnings before the re-
distribution stage.14 An index RI = 0 indicates no redistribution at all, while
 14
      Please recall that we only consider cases with pre-redistribution inequality and therefore can

                                                 19
Figure 2: Redistribution Index by treatment pair composition
                             1.0

                                          ***                       ***                      ***
                             0.8

                                                                                                   0.72
      Redistribution Index

                                                                          0.67
                                                0.62                                  0.60
                             0.6

                                                             0.47
                             0.4

                                   0.32
                             0.2
                             0.0

                                     Nature                  Self−Report               Externality

                                                              Treatment

                                                       Risky−Safe                Risky−Risky

                             Notes: The Redistribution Index compares the
                             extent of redistribution within each pair of stake-
                             holders before and after redistribution. An index
                             of zero indicates no redistribution, while an index
                             of 1 indicates that spectators have equally split
                             the pair’s total earnings. Symbol ∗ ∗ ∗ indicate
                             significance at the 1% based on a GLS regression
                             with individual random effects, where the depen-
                             dent variable is the Redistribution Index and the
                             regressor is a dummy for pairs of the Risky-Safe
                             type. We run a regression separately for each
                             treatment and we only include pairs with strictly
                             positive pre-redistribution inequality.

                                                              20
RI > 0 indicates that spectators have shifted resources to the poorer stakeholder.
An RI = 1 means that spectators have implemented an equal split of the pair’s
total earnings. For RI > 1 the pre-redistribution ranking of stakeholders is reversed
– what used to be the richer stakeholder before the redistribution is now the poorer
one.

    Following the literature, we distinguish two cases, one in which the stakeholders
made different choices (Risky-Safe), and one in which both stakeholders made the
same risky choice (Risky-Risky). Figure 2 reports the Redistribution Index by case
and treatment. In line with previous evidence on choice egalitarianism, significantly
lower levels of redistribution are observed when stakeholders made different choices
(dark grey bars), compared to the cases where both stakeholders made the same
ex-ante choice (risky) but ended up with different earnings (light grey bars). While
this is the case in all treatments, one can notice some interesting differences. In par-
ticular, in the Nature treatment we observe that the Redistribution Index is almost
double for Risky-Risky pairs compared to Risky-Safe ones (0.62 vs. 0.32). This sup-
ports the idea that people who went for a safe choice should not be entitled to enjoy
the gains of lucky risk takers and, at the same time, should not pay the burden of
stepping up for the misfortunes of unlucky risk takers. However, the gap narrows as
we introduce the possibility to misreport and externalities, due to a sharp increase
in the redistribution in Risky-Safe pairs. In treatments Self-Report and Externality,
the reluctance to redistribute between risk takers and safe players seems to be less
of a concern and safe stakeholders might be asked to share their profits with unlucky
(and honest) stakeholder. At the same time, safe stakeholders now might enjoy a
share of the profits of the lucky (and potentially dishonest) stakeholders. While
both effects are present in our data, the latter is stronger.

always uniquely identify the richer stakeholder in the pair.

                                                21
       Table 1 reports a series of GLS estimations providing statistical support for
the evidence in Figure 2. The dependent variable is the Redistribution Index and
the main explanatory variables of interest are dummies for the Self-Report and the
Externality treatment. In the baseline specification, we also included two control
variables – Age (in years) and Male (d) – to account for a slight imbalance in the
distribution of these observable characteristics across treatments (see Table A-2 in
the Online Appendix). Model 1 in Table 1 only considers pairs of the Risky-Risky
type. Both for Self-Report and Externality the coefficients are positive, but only
for Externality it is marginally significant – showing that the level of redistribution
gets only slightly larger when cheating is associated with externalities on powerless
third parties even for the case when ex-ante actions are the same.15 In Model 2, we
control for safe levels by adding a dummy for each level, and find that the value of
the safe level does not affect the redistribution index. In Models 3 and 4, we re-
peat the same analyses for pairs where the two stakeholders made different choices
(Risky-Safe) and confirm that redistribution levels are higher for both Self-Report
and Externality, compared to the baseline in Nature. Once more, safe levels (Model
4) do not drive our results.16 We further divide Risky-Safe pairs in two types: in
the first type the risk taker reported an unlucky draw (0-Safe, Model 5) and in the
second type the risk taker reported a lucky draw (800-Safe, Model 6). In both types,
the coefficients for Self-Report and Externality are positive, but they are statistically
significant only for the 800-Safe pairs. However, it is important to notice that in a
0-Safe pair there cannot be any suspicion of self-serving cheating even in the Self-
Report and Externality treatments. By definition, the stakeholders who chose safe
  15
      As we will discuss later in the individual-level analysis, this finding is perfectly in line with the
estimated distribution of types. In fact, we will observe that the share of Libertarians is remarkably
similar across treatments, and this is the only fairness type who does not redistribute in this case.
All other types behave in the same way when facing a Risky-Risky pair.
   16
      In Table 1 we pool all the data from all sessions. However, as discussed in the design section,
some treatments were run at a later point in time. As a robustness check, we re-run the same
specification (Model 1 to 4) and included the sub-sample of sessions which were properly random-
ized, that is Nature and Self-Report (no beliefs). Results are robust, as shown in Table A-4 in the
Online Appendix.

                                                    22
have no possibility to misreport and the ones who earned an income of 0 tokens cer-
tainly did not lie for their own benefit (as they earned the lowest possible outcome).17

Result 3 In all treatments, redistribution is higher in pairs where both stakeholders
made the same ex-ante risky choice compared to pairs where one stakeholder chose
safe and the other risky. This general pattern is more pronounced in Nature than
in treatments where cheating is an option. In fact, in Self-Report and especially in
Externality, we observe a sizable and significant increase in redistribution between
rich and poor even when they made different choices to start with.

       So far we have mostly focused on redistribution at the aggregate level and we
have established that it depends on whether both stakeholders made the same choice
or not, but the extent of this phenomenon varies greatly across treatments. This
evidence seems to suggest that there should be more spectators supporting an egal-
itarian rather than a choice egalitarian ideal when cheating is possible. However,
to properly test for the distribution of fairness views across treatments, we need to
move to the analysis of the individual-level behavior.

  17
     The only reason why one might expect more redistribution in Self-Report and Externality than
in Nature is that there could be a premium for honest stakeholders that resisted the temptation
despite choosing the risky option. This could be a compelling argument especially when external-
ities are present: in fact, a low income in the Externality treatment automatically grants a high
income to an idle player. Such an action can hence be interpreted as an additional sign of kindness
and not only of honesty, suggesting that spectators reward kindness. We do find some suggestive
evidence in this direction.

                                                23
                                   Table 1: Determinants of the Redistribution Index

     Dependent variable:                 Model 1        Model 2         Model 3        Model 4        Model 5       Model 6
     Redistribution Index (RI)                 Risky-Risky                     Risky-Safe              0-Safe       800-Safe
     Self-Report treatment (d)            0.069          0.059           0.162*         0.169*         0.066         0.213*
                                        (0.078)        (0.079)         (0.097)        (0.097)        (0.084)       (0.118)
     Externality treatment (d)            0.160*         0.149           0.305***       0.315***       0.160         0.376***
                                        (0.091)        (0.091)         (0.112)        (0.113)        (0.098)       (0.135)
     Male (d)                            -0.176***      -0.176***       -0.043         -0.042         -0.002        -0.069
                                        (0.066)        (0.065)         (0.081)        (0.081)        (0.070)       (0.095)
     Age (years)                         -0.011         -0.011          -0.020**       -0.021**       -0.003        -0.026**
                                        (0.008)        (0.008)         (0.010)        (0.010)        (0.009)       (0.012)
     Safe Level 200 (d)                                  0.009                          0.008          0.048         0.000
                                                       (0.029)                        (0.047)        (0.071)       (0.050)
     Safe Level 300 (d)                                  0.030                          0.009         -0.043         0.067

24
                                                       (0.033)                        (0.042)        (0.047)       (0.060)
     Safe Level 400 (d)                                 -0.010                          0.053         -0.111**       0.074*
                                                       (0.044)                        (0.036)        (0.047)       (0.040)
     Safe Level 500 (d)                                  0.025                          0.156***      -0.068         0.230***
                                                       (0.046)                        (0.042)        (0.048)       (0.046)
     Constant                             0.920***       0.915***        0.799***       0.748***       0.478**       0.813***
                                        (0.201)        (0.200)         (0.249)        (0.250)        (0.215)       (0.295)
     Post estimation F tests
     Self-Report = Externality               .238           .235            .132            .124            .258       .145
     N. obs.                                  955            955            2336            2336             594       1742
     R2 (overall)                          0.039          0.041            0.025           0.031           0.018      0.037
     Notes: GLS regression with individual random effects. Symbols ∗ ∗ ∗ and ∗∗ indicate significance at the 1% and 5%,
     respectively. The regressions only include pairs with strictly positive pre-redistribution inequality. Dummy variables
     are indicated by (d). Male takes value 1 for males and 0 otherwise. Age is expressed in years.
4        Fairness views and the role of beliefs

4.1       Estimation of fairness views

Our experimental design allows estimating spectators’ fairness views based on their
20 redistribution choices. In this subsection, we are going to introduce a discrete
choice random utility model (following Cappelen et al. 2007, 2013) and then present
the distribution of fairness views, showing how the shadow of cheating leads to a
strong shift in this distribution. In the next subsection, we will examine how the
estimated fairness views depend on spectators’ beliefs.

       For the estimation of different types we assume spectators are only motivated
by fairness views, because self-interest does not play a role in our set-up, given
the flat payment of spectators. Specifically, if X is the total income in the pair of
stakeholders to which a spectator is assigned, we assume that the spectator’s utility
from giving y to the first and X − y to the second stakeholder is given by:

                                V (y; ·) = −β(y − F k )2 /2X                                 (1)

where F k is the fair amount allocated to the first stakeholder according to the spec-
tator’s fairness view k and where β is the weight attached to fairness. A spectator’s
utility is decreasing in the distance between the amount (y) allocated to the first
stakeholder and the fair amount F k prescribed by the fairness view k.

       Spectators can differ along two dimensions: (i) how much they care about fairness
(β); and (ii) their fairness views (F k ). In line with previous papers (e.g., Cappelen
et al., 2013) and the suggestive evidence presented in section 3.2, we consider three
possible types of fairness views:18
  18
    For the sake of simplicity, we define types based on stakeholders’ outcomes. One could define
types based both on the self-reported outcome and the true state of the world. This would enlarge

                                               25
    • Libertarians never support redistribution, and no matter what the severity
      of (or the reason for) the inequality is, they leave the earnings within a pair
      of stakeholders unaltered. If x is the income of the first stakeholder before
      redistribution, we have F Libertarians = x, which yields the optimal choice y = x.

    • Choice Egalitarians are an intermediate type and differentiate between
      ex-ante and ex-post inequality. They eliminate inequality only when the dis-
      parities are generated by luck in case two stakeholders have chosen the same
      option (pair 800-0 where both chose the risky option), but do not redistribute
      if inequality reflects differences in choices (safe option vs risky option, as in
      the pairs 800-Safe and 0-Safe):
                                                     
                                                     
                                                     X/2
                                                               if C1 = C2
                            F ChoiceEgalitarians =
                                                     
                                                     x
                                                               if C1 6= C2

      where Ci takes value 1 if stakeholder i chooses the risky option and 0 if he/she
      chooses the safe option with the safe income level. The stark difference in the
      Redistribution Index between pairs of the 800-0 type and pairs involving a
      stakeholder with a safe choice suggests that this intermediate type has some
      bearing in our data.

    • Egalitarians are on the opposite end of the spectrum compared to Liber-
      tarians. They always eliminate inequality within a pair and split the earnings
      equally: F Egalitarians = X/2, which yields the optimal choice y = X/2. Ac-
      cording to this fairness view, inequality is unjust both when the stakeholders
      made the same choice but ended up with different incomes (pair 800-0 ) and
      when the stakeholders chose different options ex-ante (pairs 800-Safe and 0-
the set of relevant pairs, as we should distinguish between genuinely lucky stakeholders and dis-
honest stakeholders reporting a high earning despite the unlucky draw. While it is plausible that
spectators would take into account the true state of the world if they had a chance to do so, this
is not possible in our experiment. We hence opt for keeping the definition of types tractable and
only focus on outcomes.

                                               26
         Safe).

       It is important to notice that having multiple safe levels serves as a robustness
check for the estimation of the fairness types. The heuristics behind each type are
universal and apply to each situation – e.g., Egalitarians always share equally, and
Libertarians never redistribute. However, these heuristics do translate into action
–i.e., proposed redistribution of payoffs – which change from pair to pair, depend-
ing on the safe level. For instance, sharing equally in a pair with Safe=200 and
Risky=0, means giving 100 tokens to each stakeholder. This would be different if
Safe=300 and Risky=0. While this distinction is not relevant when considering a
standardized redistribution index (see Table 2), it will become important when mov-
ing to the individual-level data. Looking at the descriptive data, we observe that
73.1% of all decisions correspond exactly to one of the three types (68.8% in Nature,
75.4% in Self-Report and 71.5 % in Externality).19 These fractions correspond to
the number of decisions consistent with the action prescribed by at least one fairness
view, but they do not indicate the fraction of spectators being classified as pure types.

       Since we let all spectators make 20 redistribution decisions, we can estimate
the likelihood with which a spectator belongs to any of the three different types of
fairness views. Given a spectator’s fairness view k, we consider a discrete choice
random utility model of the form

                      U (y; ·) = V (y; ·) + εiy        for y = 0, 25, . . . , X                (2)

where εiy is assumed to be i.i.d extreme value distributed and, to control for indi-
vidual heterogeneity in noisy behavior, the β parameter in equation 1 is assumed to
be log normally distributed with log(β) ∼ N (ζ, σ 2 ). Denoting by Li,k the individual
likelihood conditional on being of type k, we can obtain the total likelihood of an
  19
    Note that our fraction of 73.1% of decisions that match at least one type is remarkably similar
to the 71.1% reported in Cappelen et al. (2013) for their experiment in Norway.

                                                  27
                                                                               k              k
                                                                        P
individual by considering the finite mixture of types Li =                  k λ Li,k , where λ is

the probability of being of type k.20

       Figure 3 and Table A-5 in the Online Appendix report the estimated propor-
tion of types, λk . Libertarians account for a fairly large share of the spectators in
all treatments, ranging from 40% in Self-Report and Externality to 46% in Nature.
Apart from this similarity, the distribution of fairness types differs substantially be-
tween Nature and the two treatments where cheating is possible (likelihood ratio
tests: Nature versus Self-Report, χ2 (4) = 13.696; p = .008; Nature vs. Externality,
χ2 (4) = 17.468, p = .002).

       In Nature, a large share of spectators (41%) are Choice Egalitarians – the in-
termediate type – and only 12% of spectators are Egalitarians. This pattern is
completely reversed when cheating is possible. In Self-Report, the share of Choice
Egalitarians drops to only 24%, while 36% of spectators are classified as Egalitar-
ians. When cheating comes with an externality, the reversal becomes even more
striking, as in Externality we classify only 15% as Choice Egalitarians and Egali-
tarians are the most prominent type, with 45%. In other words, under the shadow
of cheating spectators are much less likely to condition their redistribution decision
on whether the two stakeholders chose the same action – i.e., the risky option –
or not. Rather, unconditional egalitarianism becomes much more prominent. As a
consequence, there are two diametrically opposed fairness views that dominate in
the treatments with a possibility to cheat (to get rich): Libertarians who do not
want to redistribute anything, and Egalitarians who prefer redistribution to the
fullest extent.

  20
    For further details on the estimation strategy, please refer to section 5 in the Online Appendix
or see Cappelen et al. (2013).

                                                28
                               Figure 3: Estimation of fairness views

                         100
                         80
Relative frequency (%)

                         60      46.3                                                  44.7
                                        40.3 39.9   41.5
                         40

                                                                                35.6

                                                           24.1
                         20

                                                                  15.4
                                                                         12.3
                         0

                                                       Choice
                                   Libertarian        Egalitarian          Egalitarian

                                                    Fairness views

                                        Nature             Self−Report          Externality

                         Notes: The bars report the share of λk (in %).
                         The results are based on a discrete choice random
                         utility model.

                                                      29
       We observe a difference also in the distribution of fairness views between Self-
Report and Externality – albeit this difference is much smaller than the one between
Nature and the other treatments. The fact that cheating imposes negative conse-
quences on an idle player leads to an even stronger shift in spectators’ fairness
views compared to costless cheating (χ2 (4) = 9.282, p = .054 for Self-Report versus
Externality). The potentially illegitimate claim of the high income now intercepts
another person’s income, making cheating not just an unethical, but also harm-
ful action. This leads spectators to redistribute more than when stakeholders only
cheated for their own benefit, without causing negative externalities on others.21

Result 4 The shadow of cheating produces a large and statistically significant shift
in fairness views. While the fraction of Libertarians is similar across treatments,
the share of Egalitarians becomes three to four times larger in the treatments where
cheating is an opportunity than when this is not possible. This implies that the
shadow of cheating creates a polarization of fairness views, even more so in Exter-
nality than in Self-Report.

  21
    In the estimation of types we pooled data from all treatments. To account for any possible
problem coming from the imperfect randomization of the sessions, we re-ran the model limiting
our analysis to the sub-sample of sessions which were properly randomized. The distribution of
types and the precision of the estimates is qualitatively and quantitatively in line with the one
estimated for the overall sample (Table A-6 in the Appendix).

                                               30
              Figure 4: Fairness views and posterior probabilities
                (a) Nature                                                    (b) Self-Report

                 Libertarian                                                      Libertarian

                    37%                                                                 34%

   7%                                       35%               30%                                   19%

Egalitarian                              Choice             Egalitarian                          Choice
                                        Egalitarian                                             Egalitarian

                                            (c) Externality

                                                Libertarian

                                                      33%

                            40%                                                5%

                          Egalitarian                                      Choice
                                                                          Egalitarian

         Notes: Each vertex of the triangle represents a fairness view and the
         bubbles in the corners report the relative frequency of spectators for
         whom we estimate a posterior probability higher than 90% of holding
         that particular view.

                                                      31
       To test the accuracy of our type classification, we compute the ex-post probability
of any specific spectator to belong to a particular fairness type. Figure 4 reports the
simplex with the posterior probability for each spectator – see Conte and Hey (2013)
for a similar exercise. Each vertex of the triangle represents one fairness type and
each dot represents one spectator. The bubbles in the corners report the percentage
of spectators who have a posterior probability higher than 90% of being that type.
We can observe that the vast majority of the spectators – 79% in Nature, 83% in
Self-Report, and 78% in Externality – are located in one of the three corners, hence
suggesting that types are identified with great precision. The shift in fairness types
from Nature to the other two treatments is illustrated on the horizontal axis at the
bottom of all triangles in Figure 4 where we see the shift from Choice Egalitarians
(in Nature) to Egalitarians (in Self-Report and Externality).22

4.2       The role of beliefs for fairness views

A straightforward candidate to drive one’s fairness views is beliefs. It could be that
spectators with different fairness views hold significantly different beliefs about the
likelihood with which a stakeholder’s high income might have been caused by cheat-
ing. For instance, one could imagine that some spectators want to abstain from any
kind of redistribution because they expect stakeholders to be (mostly) honest and
therefore see no reason to take money away from them. Similarly, one could argue
that others favor extensive redistribution because they expect high income to be
undeserved and (mostly) the result of cheating. While this might sound plausible,
Figure 5 shows that there is no correlation between beliefs and types.23 This figure
is based on data from two Self-Report and two Externality sessions in which we
asked a total of 60 spectators in each treatment to guess (in an incentive compatible
  22
     Actual and predicted redistribution choices are reported in the Online Appendix in Figures
A-1 to A-3.
  23
     See also Tables A-7 and A-8 in the Online Appendix for regressions. Both in Figure 5 and
Tables A-7 and A-8 we define types based on posterior probabilities. Each spectator is assigned to
a particular type if the posterior probability of being of that type is at least 0.5. The results are
robust to more demanding cut-offs of 0.7 and 0.9, for instance.

                                                 32
way) the fraction of stakeholders who choose the risky option and how many of the
latter report the high income. To avoid any priming or experimenter demand effect,
we elicited beliefs only at the end of the session, after spectators had made all their
distributive choices. For the sake of brevity, we elicited beliefs only for the income
level of 300 tokens in the safe option.

   For this safe level, spectators expect 58% of stakeholders to choose the risky
option in Self-Report and 59% in Externality. The expected fraction is quite close
to the actual frequency (of 52% in Self-Report and 51% in Externality) with which
stakeholders choose the risky option when the safe option pays 300 tokens (see
right-hand side and bottom of Figure 1). Spectators expect on average that 74%
of stakeholders who choose the risky option in Self-Report report the high income
(70% in Externality), even though truthful reporting would yield a 50% chance for
the high income. The expected fraction of reporting the high income (74%, respec-
tively 70%) is again very close to the actual share of stakeholders reporting the high
income (in case the safe option pays 300 tokens: 67% and 71% in Self-Report and
Externality, respectively).

                                          33
                          Figure 5: Spectators’ beliefs about stakeholders’ behavior by fairness view
                                          (a) Self-Report                                                                       (b) Externality
                         100

                                                                                                               100
                                                         ●
                                                   ●
                         80

                                                                                                               80
                                                                          ●
Relative frequency (%)

                                                                                      Relative frequency (%)
                                      ●                                                                                     ●                  ●
                                                         ●                                                                                                      ●

                                ●                                                                                                        ●
                                                                     ●                                                                                     ●
                         60

                                                                                                               60
                                                   ●                                                                  ●

                                                         ●
                                                         ●
                         40

                                                                                                               40
                                                                                                                                                                ●
                                                                                                                            ●                              ●
                                                                                                                                                           ●
                                                                                                                                                           ●
                         20

                                                                                                               20
                                                                          ●
                         0

                                                                                                               0
                                                   Choice                                                                                Choice
                               Libertarian        Egalitarian      Egalitarian                                       Libertarian        Egalitarian      Egalitarian

                                                Fairness views                                                                        Fairness views

                                          Risky option           High income                                                    Risky option           High income

                                      Notes: The figure shows the distribution of spectators’ beliefs about
                                      the percentage of stakeholders choosing the risky option (black) and
                                      about the percentage of stakeholders reporting the high income (light
                                      gray), by fairness views. The white line inside the boxes indicates the
                                      median of the distribution, the box represents the interquartile range,
                                      and the whiskers extend to the most extreme data point which is no
                                      more than 1.5 times the interquartile range. Dots indicate outliers,
                                      i.e., data points lying outside the whiskers.

                                                                                 34
   Interestingly, Figure 5 reveals that there are no differences in the beliefs of spec-
tators with different fairness views and this is true for both treatments. We consider
this a noteworthy finding. For instance, both Libertarians and Egalitarians expect
three quarters of stakeholders who choose the risky option to report the high in-
come. The remarkable similarities across types speaks against the idea that specta-
tors could form some sort of self-serving beliefs aimed at justifying their distributive
behavior – e.g., Egalitarians report high levels of cheating not because they believe
that is the case but just to provide a justification for taking away from the rich. Ev-
idently, both Libertarians and Egalitarians can infer from this large fraction of high
income that cheating is going on, but they nevertheless make opposite redistribution
choices.The lack of significant differences in beliefs across fairness types also implies
that there is not a relationship between beliefs and the extent of redistribution. This
stems from the fact that in each pair, the action prescribed by each type is to either
share equally or not redistribute and this is indeed what we observe in the majority
of the choices made by our spectators. A series of regressions confirms this intuition.
This suggests that different people might have different levels of tolerance toward
cheating, for some it is enough to have a slight suspicion of cheating to become Egal-
itarian, for some others, instead, even a reasonable doubt is not enough to switch
type.

   In order to address potential concerns about spectators’ beliefs being elicited
after 20 redistribution choices, we also elicited beliefs among students not involved
in the redistribution task. For that robustness check, we invited 289 additional
students from an Introductory Microeconomics course at the University of Cologne
to predict (in an incentive compatible way) the stakeholders’ behavior, conditional
on the different levels of income from the safe option. For the safe amount of
300 tokens, they expected 66% of stakeholders to choose the risky option (where
the actual relative frequency is 52%). Students estimated that on average 69% of

                                           35
stakeholders who choose the risky option would report the high income while, in
fact, the actual number is 67%. Hence, these new students who had not taken
part in any of our treatments before were very capable of predicting the relative
frequency of cheating among stakeholders, even when they were not asked to make
redistribution choices themselves. This evidence suggests that our design did not
induce any bias in spectators’ beliefs.

Result 5 Libertarians, Egalitarians, and Choice Egalitarians hold very similar be-
liefs about risk-taking and cheating among stakeholders (in the Self-Report and in
the Externality treatment), but nevertheless make different redistribution choices.

    As a last point, we check to what extent the observable characteristics of our
spectators can explain their posterior probability of being of one of the three types.
We consider the role of socio-demographic information (age and gender), political
views, tolerance for inequality, and a subscale of the HEXACO-PI. In particular,
we consider the Honesty Humility sub-scale, where people with a high score tend to
“avoid manipulating others for personal gain, feel little temptation to break rules,
are uninterested in lavish wealth and luxuries, and feel no special entitlement to
elevated social status.” Table A-9 in the Appendix reports three fractional outcome
regression models where the dependent variable is the probability of being of one
type. As one might expect, males and people with a low Honesty Humility index
are more likely to be Libertarians. While one might be surprised by the lack of
significance of the political orientation variables, it is worth mentioning that the
distribution is skewed with 13% of participants reporting to be right wing.

5     Conclusion

The growing gap between the rich and poor members within our societies has revived
a debate about what constitutes a fair level of redistribution to alleviate income in-
equalities. The support for more redistribution, taxation, and regulation depends

                                          36
largely on the perceived sources of income inequality (Konow, 2000; Alesina and
Angeletos, 2005; Cappelen et al., 2013; Möllerström et al., 2015; Almås et al., 2020;
Konow et al., 2020). Yet, it can be difficult to unequivocally establish the source of
inequality and decisions about what is deemed to be fair are often based on limited
information.

   In this paper, we have introduced the possibility of cheating as a potentially
important source of income inequality, and have focused on situations where it is
not clear to what extent one’s fortunes have been achieved by honest means or not.
We have studied how the shadow of cheating affects redistribution when disparities
have emerged as a consequence of risky investments. Studying situations involving
risk-taking is particularly important, as differences in risk taking behavior and in
the outcomes of a risky choice can themselves generate substantial inequality. It
is understood that a sizable share of people who support redistribution polices in
this context are in favour of a choice egalitarian view of fairness (Cappelen et al.,
2013); they tend to reduce inequality only among people who took a risk in the
first place and ended up with different outcomes due to luck, but draw a clear line
between risk-takers and non risk-takers when it comes to redistribution. By means
of a controlled laboratory experiment, we have tested to what extent fairness views
are affected when high returns on an investment can be due to luck or dishonesty
but one has no means to detect the actual cause.

   We have found a substantial shift in the distribution of fairness views when
spectators know that cheating is possible. More precisely, under the shadow of
cheating, we have observed a split of the spectators into two diametrically opposed
subpopulations. On one side of the spectrum are Libertarians who abstain from any
redistribution, no matter what might be the source of income inequalities. On the
other side of the spectrum are Egalitarians who implement perfect equality.

                                          37
   The polarization of fairness views under the shadow of cheating is mainly driven
by a strong shift from Choice Egalitarians – who do not redistribute between stake-
holders when they have generated their income from different actions – to Egali-
tarians. Under the shadow of cheating, spectators face the conundrum of whether
to take money away from a rich person who has either rightfully earned it or who
may have purposefully acted dishonestly to profit from an unobservable situation.
The strong increase in egalitarian fairness views in such an environment may reflect
the spectators’ wish to have a more progressive taxation systems where people who
do not engage in risky investments may enjoy a share of the profits of the lucky
investors, but might be asked to contribute when the risky choices did not lead to a
high return. Support for higher taxation might as well reduce the attractiveness of
the risky options and cheating.

   While the shadow of cheating has led to a large increase in the number of Egal-
itarians, we find it remarkable that the proportion of spectators with a Libertarian
point of view has remained practically the same across all treatments. The fairness
views of these spectators have not been significantly altered by suspected unethical
behavior. This suggests that either dishonesty itself is not a good reason for these
spectators to reduce inequality or they are concerned to wrongfully take money
away from truly lucky stakeholders who have truthfully reported their income. This
view should not be too surprising in light of the fact that excessive redistribution or
regulation of market transactions could lead to inefficiencies and reduce productive
investments.

   We can rule out that Libertarians have different beliefs about the honesty of
stakeholders compared to the beliefs of Egalitarians or Choice Egalitarians. We
consider the lack of differences in beliefs an important finding. Indeed, we do not

                                          38
find evidence of increased perceived corruption among those who are more inclined
toward redistribution or distort their beliefs to provide a justification for their redis-
tribution behavior. Moreover, Libertarians deliberately refrain from redistributing
despite knowing that some of the income disparities are caused by cheating on the
part of the rich. Likewise, Egalitarians support an equal distribution of income
although they acknowledge that some inequalities were not caused by dishonesty
on the part of the rich. This finding suggests that people have a different tolerance
level for type-I and type-II mistakes.

   Overall, the shadow of cheating has created a polarization of fairness views at
opposite ends of the spectrum, having Egalitarians on the one end and Libertarians
on the other end. While findings should be taken with caution due to the lack of
proper randomization, it is interesting to notice that this tendency is even more
pronounced in treatment Externality, hence suggesting that a considerable portion
of the population might feel especially strongly about supporting the welfare state
when innocent parties suffer losses as a byproduct of someone else’s unethical be-
havior. We consider it a plausible assumption that negative externalities of cheating
are rather the rule than the exception, for which reason we argue that the extent of
the polarization of fairness views observed in Self-Report is most likely measuring a
lower bound.

   To summarize, our findings suggest that the shadow of cheating could lead to
increased social tensions and more disruptive changes in redistribution policies when
political majorities swing back and forth between one camp (Egalitarians) and the
other camp (Libertarians). Politicians might want to take this factor into account
when establishing the legal and institutional framework that is intended to prevent
illicit behavior of citizens. In fact, failing to fight dishonesty will not only cause an
increase in illicit activities, but – according to our findings – it will also contribute

                                           39
to a polarization of fairness views and a demand for redistribution. The latter effect
is likely an overlooked side-effect of failed attempts to fight corruption and illegal ac-
tivities, which are often at the root of large income inequalities (Glaeser et al., 2003).

References

Abeler, J., D. Nosenzo, and C. Raymond (2019). Preferences for Truth-Telling.
  Econometrica 87(4), 1115–1153.

Akbaş, M., D. Ariely, and S. Yuksel (2019). When is inequality fair? An experiment
  on the effect of procedural justice and agency. Journal of Economic Behavior &
  Organization 161, 114–127.

Alesina, A. and G.-M. Angeletos (2005). Fairness and Redistribution. American
  Economic Review 95 (4), 960–980.

Almås, I., A. W. Cappelen, and B. Tungodden (2020). Cutthroat Capitalism Versus
  Cuddly Socialism: Are Americans More Meritocratic and Efficiency-Seeking than
  Scandinavians? Journal of Political Economy 128 (5), 1753–1788.

Alstadsæter, A., N. Johannesen, and G. Zucman (2019). Tax evasion and inequality.
  American Economic Review 109 (6), 2073–2103.

Ashton, M. C. and K. Lee (2009). The hexaco–60: A short measure of the major
  dimensions of personality. Journal of Personality Assessment 91 (4), 340–345.

Balafoutas, L., M. G. Kocher, L. Putterman, and M. Sutter (2013). Equality, Equity
  and Incentives: An Experiment . European Economic Review 60, 32–51.

Bašić, Z. and S. Quercia (2022). The influence of self and social image concerns on
  lying. Games and Economic Behavior 133, 162–169.

                                           40
Bolton, G. E., J. Brandts, and A. Ockenfels (2005). Fair Procedures: Evidence from
  Games Involving Lotteries. Economic Journal 115 (506), 1054–1076.

Buhrmester, M., T. Kwang, and S. D. Gosling (2011). Amazon’s Mechanical Turk.
  Perspectives on Psychological Science 6 (1), 3–5.

Cappelen, A., S. Fest, E. O. Sørensen, and B. Tungodden (2020). Choice and
  Personal Responsibility: What is a Morally Relevant Choice?      The Review of
  Economics and Statistics, 1–35.

Cappelen, A. W., C. Cappelen, and B. Tungodden (2018). Second-Best Fairness
  Under Limited Information: The Trade-Off between False Positives and False
  Negatives. Discussion paper, NHH Dept. of Economics Discussion Paper No.
  18/2018.

Cappelen, A. W., A. D. Hole, E. O. Sørensen, and B. Tungodden (2007). The
  Pluralism of Fairness Ideals: An Experimental Approach. American Economic
  Review 97 (3), 818–827.

Cappelen, A. W., J. Konow, E. O. Sørensen, and B. Tungodden (2013). Just Luck:
  An Experimental Study of Risk-Taking and Fairness. American Economic Re-
  view 103 (4), 1398–1413.

Cappelen, A. W., J. Mollerstrom, B.-A. Reme, and B. Tungodden (2022). A Meri-
  tocratic Origin of Egalitarian Behaviour. The Economic Journal 132 (646), 2101–
  2117.

Cassar, L. and A. H. Klein (2019). A Matter of Perspective: How Experience Shapes
  Preferences for Redistribution. Management Science 65 (11), 5050–5064.

Chetty, R., N. Hendren, P. Kline, E. Saez, and N. Turner (2014). Is the United
  States Still a Land of Opportunity? Recent Trends in Intergenerational Mobility.
  American Economic Review 104 (5), 141–47.

                                        41
Conrads, J., B. Irlenbusch, R. Rilke, and G. Walkowitz (2013). Lying and Team
  Incentives. Journal of Economic Psychology 34 (C), 1–7.

Conte, A. and J. D. Hey (2013). Assessing Multiple Prior Models of Behaviour
  under Ambiguity. Journal of Risk and Uncertainty 46 (2), 113–132.

Corak, M. (2013). Income Inequality, Equality of Opportunity, and Intergenerational
  Mobility. Journal of Economic Perspectives 27 (3), 79–102.

Di Tella, R., R. Perez-Truglia, A. Babino, and M. Sigman (2015). Conveniently
  upset: Avoiding altruism by distorting beliefs about others’ altruism. American
  Economic Review 105 (11), 3416–42.

Eckel, C. C. and P. J. Grossman (2008). Forecasting Risk Attitudes: An Experi-
  mental Study using Actual and Forcasted Gamble Choices. Journal of Economic
  Behavior & Organization 68 (1), 1–17.

Exley, C. L. (2015). Excusing Selfishness in Charitable Giving: The Role of Risk.
  The Review of Economic Studies 83 (2), 587–628.

Exley, C. L. and J. B. Kessler (2022). The Gender Gap in Self-Promotion*. The
  Quarterly Journal of Economics 137 (3), 1345–1381. qjac003.

Fehr, D. (2018). Is increasing inequality harmful? experimental evidence. Games
  and Economic Behavior 107, 123 – 134.

Fehr, E. and K. M. Schmidt (1999). A Theory of Fairness, Competition, and Coop-
  eration. Quarterly Journal of Economics 114 (3), 817–868.

Fischbacher, U. (2007). z-Tree: Zurich Toolbox for Ready-made Economic Experi-
  ments. Experimental Economics 10 (2), 171–178.

Fischbacher, U. and F. Föllmi-Heusi (2013). Lies in Disguise: An Experimental
  Study on Cheating. Journal of the European Economic Association 11 (3), 525–
  547.

                                        42
Gächter, S. and J. F. Schulz (2016). Intrinsic Honesty and the Prevalence of Rule
  Violations across Societies. Nature 531 (7595), 496–499.

Glaeser, E., J. Scheinkman, and A. Shleifer (2003). The Injustice of Inequality.
  Journal of Monetary Economics 50 (1), 199–222.

Gneezy, U. (2005). Deception: The Role of Consequences. American Economic
  Review 95 (1), 384–394.

Gneezy, U., A. Kajackaite, and J. Sobel (2018). Lying Aversion and the Size of the
  Lie. American Economic Review 108 (2), 419–53.

Greiner, B. (2015). Subject Pool Recruitment Procedures: Organizing Experiments
  with ORSEE. Journal of the Economic Science Association 1 (1), 114–125.

Grolleau, G., M. G. Kocher, and A. Sutan (2016). Cheating and Loss Aversion: Do
  People Cheat More to Avoid a Loss? Management Science 62 (12), 3428–3438.

Guyton, J., P. Langetieg, D. Reck, M. Risch, and G. Zucman (2021). Tax evasion at
  the top of the income distribution: Theory and evidence. Working Paper 28542,
  National Bureau of Economic Research.

Horton, J. J., D. G. Rand, and R. J. Zeckhauser (2011). The Online Laboratory:
  Conducting Experiments in a Real Labor Market. Experimental Economics 14 (3),
  399–425.

Kajackaite, A. (2018). Lying about Luck versus Lying about Performance. Journal
  of Economic Behavior & Organization 153, 194–199.

Klimm, F. (2019). Suspicious success – Cheating, inequality acceptance, and polit-
  ical preferences. European Economic Review 117, 36–55.

Konow, J. (2000). Fair Shares: Accountability and Cognitive Dissonance in Alloca-
  tion Decisions. American Economic Review 90 (4), 1072–1091.

                                        43
Konow, J. (2009). Is Fairness in the Eye of the Beholder? An Impartial Spectator
  Analysis of Justice. Social Choice and Welfare 33 (1), 101–127.

Konow, J., T. Saijo, and K. Akai (2020). Equity versus Equality: Spectators,
  Stakeholders and Groups. Journal of Economic Psychology 77, 101–127.

Kuziemko, I., M. I. Norton, E. Saez, and S. Stantcheva (2015). How Elastic Are
  Preferences for Redistribution? Evidence from Randomized Survey Experiments.
  American Economic Review 105 (4), 1478–1508.

Lefgren, L. J., D. P. Sims, and O. B. Stoddard (2016). Effort, Luck, and Voting for
  Redistribution. Journal of Public Economics 143, 89–97.

Leiner, D. J. (2014). SoSci Survey (Version 2.5.00-i) [Computer software].

Litman, L., J. Robinson, and T. Abberbock (2017). TurkPrime.com: A Versatile
  Crowdsourcing data Acquisition Platform for the Behavioral Sciences. Behavior
  Research Methods 49, 433–442.

Litman, L., J. Robinson, and C. Rosenzweig (2015). The Relationship between
  Motivation, Monetary Compensation, and Data Quality among US- and India-
  based Workers on Mechanical Turk. Behavior Research Methods 47 (2), 519–528.

Möllerström, J., B.-A. Reme, and E. O. Sørensen (2015). Luck, Choice and Re-
  sponsibility — An Experimental Study of Fairness Views. Journal of Public Eco-
  nomics 131, 33–40.

Piff, P. K., D. M. Stancato, S. Côté, R. Mendoza-Denton, and D. Keltner (2012).
  Higher social class predicts increased unethical behavior. Proceedings of the Na-
  tional Academy of Sciences 109 (11), 4086–4091.

Piketty, T. (2014). Capital in the Twenty-First Century. Harvard University Press.

                                        44
Rey-Biel, P., R. M. Sheremeta, and N. Uler (2011). (Bad) Luck or (Lack of) Effort?:
  Comparing Social Sharing Norms between US and Europe. Discussion paper,
  Availalable at http://pareto.uab.es/prey/Neslihansub.pdf.

Tinghög, G., D. Andersson, and D. Västfjäll (2017). Are Individuals Luck Egal-
  itarians? An Experiment on the Influence of Brute and Option Luck on Social
  Preferences. Frontiers in Psychology 8 (460).

Train, K. (2009). Discrete Choice Methods with Simulation. Cambridge University
  Press.

Weisel, O. and S. Shalvi (2015). The Collaborative Roots of Corruption. Proceedings
  of the National Academy of Sciences 112 (34), 10651–10656.

Zimmermann, F. (2020). The dynamics of motivated beliefs. American Economic
  Review 110 (2), 337–61.

                                        45
Online Appendix A: Tables and Figures

                      46
Figure A-1: Actual and predicted income redistribution - Nature treatment
                                                                                        (a) 800-0
                                                                   Actual                                                                              Predicted

                                 10 20 30 40 50 60

                                                                                                                       10 20 30 40 50 60
        Relative frequency (%)

                                                                                              Relative frequency (%)
                                 0

                                                                                                                       0
                                                     0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                 Share to 800                                                                          Share to 800

                                                                                        (b) 0-Safe
                                                                   Actual                                                                              Predicted
                                 10 20 30 40 50 60

                                                                                                                       10 20 30 40 50 60
        Relative frequency (%)

                                                                                              Relative frequency (%)
                                 0

                                                                                                                       0

                                                     0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                 Share to Safe                                                                         Share to Safe

                                                                                       (c) 800-Safe
                                                                   Actual                                                                              Predicted
                                 10 20 30 40 50 60

                                                                                                                       10 20 30 40 50 60
        Relative frequency (%)

                                                                                              Relative frequency (%)
                                 0

                                                                                                                       0

                                                     0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                 Share to 800                                                                          Share to 800

      Notes: “Actual” refers to the choice made by the spectators. “Predicted”
      refers to simulated choices obtained using the discrete choice random util-
      ity model and the estimated parameters in Table A-5. For each spectator,
      we run 1000 simulations of the 20 choices he/she faced. In each simula-
      tion, we randomly draw a fairness view F k and a β in accordance with
      the estimated parameters. Panel (a) shows actual and predicted choices
      in pairs of the type 800-0 where the both stakeholders chose risky and the
      first earned 800 and the second 0; Panel (b) shows actual and predicted
      choices in pairs of the type 0-Safe where the first stakeholder chose risky
      and was unlucky and the second chose safe; and Panel (c) shows actual and
      predicted choices in pairs of the type 800-Safe where the first stakeholder
      chose risky and was lucky and the second chose safe.

                                                                                             47
Figure A-2: Actual and predicted income redistribution - Self-Report treatment
                                                                                          (a) 800-0
                                                                     Actual                                                                              Predicted
                                   10 20 30 40 50 60

                                                                                                                         10 20 30 40 50 60
          Relative frequency (%)

                                                                                                Relative frequency (%)
                                   0

                                                                                                                         0
                                                       0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                   Share to 800                                                                          Share to 800

                                                                                          (b) 0-Safe
                                                                     Actual                                                                              Predicted
                                   10 20 30 40 50 60

                                                                                                                         10 20 30 40 50 60
          Relative frequency (%)

                                                                                                Relative frequency (%)
                                   0

                                                                                                                         0

                                                       0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                   Share to Safe                                                                         Share to Safe

                                                                                         (c) 800-Safe
                                                                     Actual                                                                              Predicted
                                   10 20 30 40 50 60

                                                                                                                         10 20 30 40 50 60
          Relative frequency (%)

                                                                                                Relative frequency (%)
                                   0

                                                                                                                         0

                                                       0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                   Share to 800                                                                          Share to 800

        Notes: “Actual” refers to the choice made by the spectators. “Predicted”
        refers to simulated choices obtained using the discrete choice random util-
        ity model and the estimated parameters in Table A-5. For each spectator,
        we run 1000 simulations of the 20 choices he/she faced. In each simula-
        tion, we randomly draw a fairness view F k and a β in accordance with
        the estimated parameters. Panel (a) shows actual and predicted choices
        in pairs of the type 800-0 ; Panel (b) shows actual and predicted choices in
        pairs of the type 0-Safe; and Panel (c) shows actual and predicted choices
        in pairs of the type 800-Safe.

                                                                                               48
Figure A-3: Actual and predicted income redistribution - Externality treatment
                                                                                          (a) 800-0
                                                                     Actual                                                                              Predicted
                                   10 20 30 40 50 60

                                                                                                                         10 20 30 40 50 60
          Relative frequency (%)

                                                                                                Relative frequency (%)
                                   0

                                                                                                                         0
                                                       0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                   Share to 800                                                                          Share to 800

                                                                                          (b) 0-Safe
                                                                     Actual                                                                              Predicted
                                   10 20 30 40 50 60

                                                                                                                         10 20 30 40 50 60
          Relative frequency (%)

                                                                                                Relative frequency (%)
                                   0

                                                                                                                         0

                                                       0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                   Share to Safe                                                                         Share to Safe

                                                                                         (c) 800-Safe
                                                                     Actual                                                                              Predicted
                                   10 20 30 40 50 60

                                                                                                                         10 20 30 40 50 60
          Relative frequency (%)

                                                                                                Relative frequency (%)
                                   0

                                                                                                                         0

                                                       0.0   0.2     0.4   0.6     0.8   1.0                                                 0.0   0.2     0.4   0.6     0.8   1.0

                                                                   Share to 800                                                                          Share to 800

        Notes: “Actual” refers to the choice made by the spectators. “Predicted”
        refers to simulated choices obtained using the discrete choice random util-
        ity model and the estimated parameters in Table A-5. For each spectator,
        we run 1000 simulations of the 20 choices he/she faced. In each simula-
        tion, we randomly draw a fairness view F k and a β in accordance with
        the estimated parameters. Panel (a) shows actual and predicted choices
        in pairs of the type 800-0 ; Panel (b) shows actual and predicted choices in
        pairs of the type 0-Safe; and Panel (c) shows actual and predicted choices
        in pairs of the type 800-Safe.

                                                                                               49
Table A-1: Randomization check: Self-Report with and without beliefs

                                  (1)                   (2)                  (3)
   Variable                   Self report           Self report          (1) vs. (2)
                            without beliefs         with beliefs
                              Mean (SD)             Mean (SD)             p-value
   Age (in years)             23.32 (3.36)           22.8 (2.72)           0.357
   Male (d)                 36.67% (n = 60)       38.33% (n = 60)           0.85
   Local (d)                 60% (n = 60)         58.33% (n = 60)          0.853
   STEM Major (d)            20% (n = 60)         13.33% (n = 60)          0.327
   Right                    11.67% (n = 60)       11.67% (n = 60)             1
   Center                   33.33% (n = 60)       36.67% (n = 60)          0.702
   Inequality (survey)         4.17 (1.99)            4.4 (2.23)           0.547
   Honesty Humility           13.16 (2.66)          12.79 (2.46)           0.432
   Notes: Balancing tests for continuous variable are performed with a two
   sample Welch t-test. Balancing tests for binary variables are based on a
   χ2 test. Dummy variables are indicated by (d). Male takes value 1 for
   males and 0 otherwise. Age is expressed in years. Local (d) takes value 1
   for participants studying in their region of origin and 0 otherwise. STEM
   Major (d) takes value 1 for students enrolled in a STEM major and 0
   otherwise. Political orientation was measured on a scale from 1 (left) to
   10 (right) in the final questionnaire. Center takes value 1 for participants
   that indicated a value from 4 to 7, and 0 otherwise. Right takes value
   1 for participants that indicated a value from 8 to 10, and 0 otherwise.
   The Honesty-Humility score is based on the HEXACO-PI (Ashton and
   Lee, 2009). “Persons with very high scores on the Honesty-Humility scale
   avoid manipulating others for personal gain, feel little temptation to break
   rules, are uninterested in lavish wealth and luxuries, and feel no special
   entitlement to elevated social status.” Inequality (survey) is a self-reported
   variable ranging from 1 (a society should aim to equalize incomes) to 10
   (a society should not aim to equalize income).

                                         50
                               Table A-2: Randomization check: All treatments

                           (1)                  (2)                 (3)             (4)           (5)             (6)
Variable                 Nature            Self-Report          Externality     (1) vs. (2)   (1) vs. (3)     (2) vs. (3)
                        Mean (SD)          Mean (SD)            Mean (SD)         p-value       p-value         p-value
Age (in years)           22.74 (2.86)      23.06 (3.05)        24.03 (5.47)       0.496         0.109           0.203
Male (d)              29.82% (n = 57)    37.5% (n = 120)     46.67% (n = 60)      0.317        0.061*           0.238
Local (d)             64.91% (n = 57)   59.17% (n = 120)     56.67% (n = 60)      0.464         0.361           0.748
STEM Major (d)        12.28% (n = 57)   16.67% (n = 120)     13.33% (n = 60)      0.448         0.865           0.561
Right                 14.04% (n = 57)   11.67% (n = 120)      15% (n = 60)        0.655         0.882           0.528
Center                 38.6% (n = 57)     35% (n = 120)      36.67% (n = 60)      0.642         0.829           0.826
Inequality (survey)       3.96 (2.15)       4.28 (2.11)         4.18 (2.12)       0.356         0.581           0.766
Honesty Humility         13.46 (2.13)      12.98 (2.56)         13.19 (2.3)       0.193          0.52            0.57
Notes: Balancing tests for continuous variable are performed with a two sample Welch t-test. Balancing tests for
binary variables are based on a χ2 test. Dummy variables are indicated by (d). Male takes value 1 for males and
0 otherwise. Age is expressed in years. Local (d) takes value 1 for participants studying in their region of origin
and o otherwise. STEM Major (d) takes value 1 for students enrolled in a STEM major and 0 otherwise. Political
orientation was measured on a scale from 1 (left) to 10 (right) in the final questionnaire. Center takes value 1 for
participants that indicated a value from 4 to 7, and 0 otherwise. Right takes value 1 for participants that indicated
a value from 8 to 10, and 0 otherwise. The Honesty-Humility score is based on the HEXACO-PI. “Persons with
very high scores on the Honesty-Humility scale avoid manipulating others for personal gain, feel little temptation to
break rules, are uninterested in lavish wealth and luxuries, and feel no special entitlement to elevated social status.”
Inequality (survey) is a self-reported variable ranging from 1 (a society should aim to equalize incomes) to 10 (a society
should not aim to equalize income).

                                                           51
             Table A-3: Procedures and generation of decision sequence
                              Nature                              Self-Report and Externality
 Scenario    Stakeholder 1    Stakeholder 2   Safe level   Stakeholder 1   Stakeholder 2    Safe level

 Based on pilot experiments
 1               Safe              800           300           Safe             800             400
 2               800                0            200           Safe              0              300
 3                0                 0            200           Safe             800             200
 4                0                 0            100           800               0              300
 5               800                0            100           800               0              200
 6                0                 0            100           Safe             Safe            400
 7               Safe              800           300            0               800             200
 8               Safe              800           100           800              800             100
 9                0                Safe          100           800              800             200
 10              Safe              Safe          400           800              Safe            100
 11              800               Safe          500           Safe             800             400
 12               0                 0            100           800              Safe            400
 13               0                Safe          500           Safe             Safe            500
 14               0                 0            300           Safe             800             500
 15              800                0            100           Safe             800             400
 16              Safe               0            400           800              800             200

 Pre-defined by the experimenter
 17              Safe             0              Si            Safe              0              Si
 18              800            Safe             Si            800              Safe            Si
 19               0              800             Si             0               800             Si

 Relevant for stakeholders’ earnings
 20          stakeholder 1    stakeholder 2       S        stakeholder 1    stakeholder 2        S

 Notes: Each stakeholder faced 20 scenarios. Scenarios 1 to 16 were based on a pilot experiment
 with 30 stakeholders per treatment and ran a few weeks prior to the proper experiment. Even
 though the sequences were pre-determined, all pairs were a possible outcome. Each scenario was
 generated by randomly drawing a pair (with reposition) and by randomly selecting a safe level
 for each chosen pair. The relevant outcomes for the selected pairs and safe level are reported
 in the table. The first 16 scenarios were treatment specific. Data from the pilot experiment on
 MTurk and the code to generate the sequence are available upon request from the authors. The
 outcomes (Safe, 800, 0) for the scenarios 17 to 19 were defined by experimenters and represent
 pairs with initial inequality. The safe level for these scenarios, Si , was randomly drawn. An
 independent random draw was performed for each spectator. The randomly selected safe level
 was kept constant across scenarios 17 to 19. Finally, the last scenario was the payoff-relevant
 one. Each spectator was assigned to one pair of stakeholders.

Table A-4: Redistribution Index: Sample restricted to Nature and Self-Report (no
beliefs)

 Dependent variable:                   Model 1         Model 2         Model 3      Model 4
 Redistribution Index (RI)           Risky-Risky      Risky-Safe        0-Safe      800-Safe
 Self-Report treatment (d)             0.056            0.241**         0.150*       0.280*
                                     (0.094)          (0.120)         (0.090)      (0.144)
 Constant                              0.618***         0.321***        0.349***     0.298***
                                     (0.067)          (0.086)         (0.063)      (0.104)
 N.obs.                                  468             1113             348          765
 R2                                    0.003            0.019           0.018        0.019
 Notes: GLS regression with individual random effect Nature and Self Report (without
 beliefs only). Symbols ∗ ∗ ∗, ∗∗, and ∗ indicate significance at the 1%, 5% and 10% level,
 respectively.

                                               52
                                     Table A-5: Estimation of types
                        Nature         Self-Report      Externality      Pooled           Pooled           Pooled             Pooled
                                                                         Nature    &      Nature    &      Self-Report &      All
                                                                         Self-Report      Externality      Externality
                        Model 1        Model 2          Model 3          Model 4          Model 5          Model 6            Model 7

 Libertarians
λ                        0.463           0.403            0.399             0.418          0.419             0.401             0.411
                         (0.071)         (0.047)          (0.069)           (0.039)        (0.049)           (0.039)           (0.034)
λEgalitarians            0.123           0.356            0.447             0.282          0.293             0.216             0.323
                         (0.048)         (0.046)          (0.068)           (0.036)        (0.045)           (0.034)           (0.032)
  ChoiceEgalitarians
λ                        0.415           0.241            0.154             0.300          0.288             0.384             0.266
                         (0.072)         (0.043)          (0.057)           (0.038)        (0.047)           (0.038)           (0.032)
ζ                        4.635           5.297            5.026             5.110          5.019             5.092             5.082
                         (0.117)         (0.059)          (0.062)           (0.051)        (0.059)           (0.040)           (0.038)
σ                        3.161           3.351            2.937             3.103          2.978             3.045             3.049
                         (0.127)         (0.070)          (0.077)           (0.058)        (0.065)           (0.047)           (0.044)
logLik                   -               -5413.893        -3064.689         -7292.313      -4944.996         -8483.223         -
                         1871.573                                                                                              10362.72
Degrees of freedom       4               4                4                 4              4                 4                 4
Notes: The likelihood is maximized in R using the BFGS method with mle2 function (bbmle package). One population share and
its standard error are calculated residually. Numerical integration is perfomed using 100 halton draws for each observation (Train,
2009). Models 1 to 3 report estimates separately by treatment: Nature, Self-Report, and Externality. Model 3 to 6 estimate pooled
data from a pair of treatments, while Model 7 pools all the data.

                    Table A-6: Estimation of types — Restricted sample
                                       Nature                     Self-Report             Pooled
                                                                  (no beliefs)            Nature & Self-Report
                                                                                          (no beliefs)
                                       Model 1                    Model 2                 Model 3

       λLibertarians                   0.463                      0.427                   0.439
                                       (0.071)                    (0.067)                 (0.049)
       λEgalitarians                   0.123                      0.400                   0.268
                                       (0.048)                    (0.067)                 (0.044)
       λChoiceEgalitarians             0.415                      0.172                   0.293
                                       (0.072)                    (0.055)                 (0.046)
       ζ                               4.635                      4.945                   4.943
                                       (0.117)                    (0.064)                 (0.063)
       σ                               3.161                      3.087                   3.089
                                       (0.127)                    (0.073)                 (0.063)
       logLik                          -1871.573                  -2746.547               -4624.943
       Degrees of freedom              4                          4                       4

       Notes: We replicate the exercise of Table A-5 on a sub-sample of the obser-
       vations. We only include sessions who were properly randomized. Nature vs.
       Self-Report: χ2 (4) = 13.646; p = 0.0085. The likelihood is maximized in R using
       the BFGS method with mle2 function (bbmle package). One population share
       and its standard error are calculated residually. Numerical integration is per-
       fomed using 100 halton draws for each observation (Train, 2009). Models 1 and
       2 are estimated separately with Nature and Self-Report data respectively; Model
       3 is estimated using pooled data;

                                                            53
        Table A-7: Beliefs and fairness views – Self-Report treatment

Dep. var.:                             Risky choices                    High income
Ex-post beliefs                  Model 1         Model 2         Model 3          Model 4
Egalitarians (d)                 -1.506          -0.266          -1.979           -0.424
                                (5.109)         (5.728)         (5.127)          (5.705)
Choice egalitarians (d)          -0.245           0.216          -1.527            0.691
                                (5.250)         (5.853)         (5.268)          (5.829)
Male (d)                                         -3.201                            3.818
                                                (4.948)                          (4.928)
Age (years)                                      -0.007                            0.207
                                                (0.869)                          (0.866)
Honesty-Humility score                           -1.254                           -0.052
                                                (0.926)                          (0.922)
Center (d)                                        1.835                            2.488
                                                (5.426)                          (5.404)
Right (d)                                         4.764                            1.064
                                                (8.249)                          (8.215)
Inequality (survey)                              -0.986                            0.970
                                                (1.090)                          (1.086)
Risk aversion                                    -1.996                           -2.300
                                                (1.637)                          (1.632)
Constant                         58.941***       85.837***       75.122***        71.084***
                                (3.336)        (25.859)         (3.348)         (25.754)
N.obs.                               60              60              60               60
R2                                0.002           0.068           0.003            0.082
Notes: OLS regression. In Models 1 and 2, the dependent variable is the estimated
frequency of risky choices; in Models 3 and 4, the dependent variable is the esti-
mated fraction of subjects who report the high income from the risky investment.
Symbols ∗ ∗ ∗ indicates significance at the 1% level, respectively. Dummy variables
are indicated by (d). Risk aversion takes values from 1 to 6, where 1 indicates risk
aversion and 6 risk loving. See Table 1 for the explanation of the other regressors.
Post estimation tests for Egalitarians = Choice Egalitarians: Model 1: p = .824;
Model 2: p = .938; Model 3: p = .937; Model 4: p = .857.

                                            54
        Table A-8: Beliefs and fairness views – Externality treatment

Dep. var.:                             Risky choices                   High income
Ex-post beliefs                  Model 1          Model 2       Model 3           Model 4
Egalitarians (d)                  1.964           -1.072        -1.007             3.945
                                (3.899)          (4.362)       (3.955)           (4.553)
Choice egalitarians (d)           4.784            0.923         1.688             8.513
                                (6.137)          (7.258)       (6.225)           (7.575)
Male (d)                                          -1.598                           9.247**
                                                 (4.081)                         (4.259)
Age (years)                                       -1.000***                       -0.065
                                                 (0.329)                         (0.343)
Honesty-Humility (score)                           0.179                          -0.396
                                                 (0.766)                         (0.799)
Center (d)                                         0.612                          -0.283
                                                 (4.724)                         (4.931)
Right (d)                                         -3.328                          -4.074
                                                 (6.667)                         (6.959)
Inequality (survey)                                0.223                           1.144
                                                 (1.088)                         (1.136)
Risk aversion                                      1.516                          -0.359
                                                 (1.456)                         (1.520)
Constant                         57.217***        75.430***     69.872***         66.304***
                                (2.837)        (15.394)        (2.877)          (16.067)
N.obs.                               60               60            60                60
R2                                0.011            0.213         0.004             0.161
Notes: OLS regression. In Models 1 and 2, the dependent variable is the estimated
frequency of risky choices; in Models 3 and 4, the dependent variable is the estimated
fraction of subjects who report the high income from the risky investment. Symbols
∗ ∗ ∗ and ∗∗ indicate significance at the 1% and 5%, respectively. Dummy variables
are indicated by (d). Risk aversion takes values from 1 to 6, where 1 indicates risk
aversion and 6 risk loving. See Table 1 for the explanation of the other regressors.
Post estimation tests for Egalitarians = Choice Egalitarians: Model 1: p = .636;
Model 2: p = .759; Model 3: p = .656; Model 4: p = .502.

                                            55
       Table A-9: Determinants of the posterior probabilities

Dep. var.: Posterior          Libertarians           Choice           Egalitarians
probability                                      Egalitarians
Male (d )                         0.388**          -0.419**          -0.047
                                (0.169)          (0.180)            (0.185)
Age (in years)                    0.049**          -0.001            -0.057**
                                (0.024)          (0.022)            (0.028)
Honesty Humility index           -0.084**           0.040             0.055
                                (0.036)          (0.036)            (0.036)
Center (d )                       0.387**          -0.028            -0.479**
                                (0.182)          (0.192)            (0.194)
Right (d )                       -0.325             0.524*           -0.174
                                (0.298)          (0.282)            (0.304)
Inequality (survey)               0.111            -0.057            -0.115
                                (0.200)          (0.203)            (0.213)
Externality (d )                 -0.302            -0.785***          1.133***
                                (0.227)          (0.225)            (0.264)
Self-Report (d )                 -0.234            -0.448**           0.844***
                                (0.203)          (0.194)            (0.236)
Constant                         -0.382            -0.633            -0.348
                                (0.752)          (0.764)            (0.798)
N.obs.                              237               237               237
Pseudo R2                         0.075             0.076             0.094
Notes: Fractional outcome regression model. In each coulum, the dependent
variable is the posterior probability of being of a specific fairness view. Symbols
∗ ∗ ∗, ∗∗, and ∗ indicate significance at the 1%, 5% and 10% level, respectively.
Dummy variables are indicated by (d). Male takes value 1 for males and 0
otherwise. Age is expressed in years. Political orientation was measured on a
scale from 1 (left) to 10 (right) in the final questionnaire. Center takes value
1 for participants that indicated a value between 4 and 7, and 0 otherwise.
Right takes value 1 for participants that indicated a value between 8 and 10,
and 0 otherwise. Inequality (survey) is a self-reported variable ranging from 1
(a society should aim to equalize incomes) to 10 (a society should not aim to
equalize income).

                                        56
Online Appendix B: Estimation procedure

In this Appendix, we provide further details about the estimation of fairness views
(based on Cappelen et al. 2007, 2013).

   Given the random utility model in equation (2) and under the assumption that
εiy is i.i.d. extreme value distributed and that log(β) is N (ζ, σ 2 ), we can write the
likelihood contribution of a spectator i conditional on fairness view k as follows:

                                      ji
                                Z ∞                     k
                                                                     !
                                      Y     eV (yij ;F ,β,·)
                Li,k (ζ, σ) =             P         V (s;F k ,β,·)
                                                                         f (β; ζ, σ)dβ   (3)
                                0     j=1  s∈Yij e

where f (·) is the density function of the log normal distribution and yij is the alloca-
tion chosen by spectator i from the choice set Yij = {0, 25, . . . , Xij } that spectator
i faces in the redistribution decision j.

   To calculate the total likelihood contribution of spectator i, we take the weighted
sum of the conditional likelihood Li,k

                                                            X
                        Li (λL , λE , λCE , ζ, σ) =                  λk Li,k             (4)
                                                      k∈{L,E,CE}

where λk is the population share of spectators with fairness view k ∈ {L, E, CE}.
k L corresponds to Libertarians view, k E corresponds to Egalitarians view, and k CE
corresponds to Choice Egalitarian view. Finally, the total log-likelihood is obtained
by taking the sum of the log of the total likelihood contributions of each spectator.

   Parameters are estimated by simulated maximum likelihood with 100 Halton
draws for each observation (Train, 2009). One population share and its standard
error are calculated residually. The estimation is performed in R using the BFGS
method with mle2 function (bbmle package).

                                               57
Online Appendix C: Instructions

Instructions for stakeholders (MTurk)

   The study comprises two stages. Please find below the instructions for stage 1.
Stage 2 of the study concerns the distribution of earnings from stage 1. Details of
the second stage will be provided after the first stage is completed.

Stage 1

If you complete the study, you will earn a fixed amount of $0.60 plus a bonus
that depends on your choices. All earnings are expressed in tokens that will be
converted into real money at the end of the study ($1=300 tokens).

   The study will take about 10 minutes to complete (including the time for reading
the instructions). You will receive a code to collect your payment via MTurk upon
completion.

Your task

You will face five decisions. In each decision, you have to choose between two
options: option A and option B (see Table C-1).

                                        Table C-1

              Decision   Option A                     Option B
                 1       100 for sure    800 with prob 50% or 0 with prob 50%
                 2       200 for sure    800 with prob 50% or 0 with prob 50%
                 3       300 for sure    800 with prob 50% or 0 with prob 50%
                 4       400 for sure    800 with prob 50% or 0 with prob 50%
                 5       500 for sure    800 with prob 50% or 0 with prob 50%

Option A is safe. The safe amount changes in each decision: it ranges from 100
tokens in decision 1 to 500 tokens in decision 5.

                                           58
Option B is risky. Option B is the same for all five decisions. If you select op-
tion B, you have a 50% probability of earning 0 tokens and a 50% probability of
earning 800 tokens. [Nature only: If you choose option B for a given decision, the
computer will resolve the lottery. The outcome will be reported in the end.] [Coin
& Ext. only: If you choose option B for a given decision, after the last decision
you have to flip a coin. If the coin lands face-up on Tails you get 0 tokens, if it
lands face-up on Heads you get 800 tokens. Please notice that you have to report the
outcome of the coin flip truthfully. You may also use justflipacoin.com to virtually
flip a coin.]

   [Ext. only:
You will be matched with another worker. The other worker will be informed about
the rules and will have to answer control questions.
The bonus of this other worker will be either 0 or 800 tokens. The bonus is deter-
mined as follows:

   • If you choose Option A (safe), the bonus for the other worker is randomly
       determined by the computer (each outcome has the same probability of being
       drawn). That is, your choice will not affect the bonus of the other worker;

   • If you choose Option B (risky), your bonus and the bonus of the other
       worker will depend on your coin flip:

         – If you report that the coin landed face-up on TAILS, you earn 0 tokens
            and the other worker earns 800 tokens;

         – If you report that the coin landed face-up on HEADS, you earn 800 tokens
            and the other worker earns 0 tokens

   ]

                                          59
   At the end of the study, the computer will randomly select one decision that
will be relevant for stage 2. Further details about stage 2 will be provided later.
If the instructions are clear, please enter your MTurk worker ID and proceed to the
control questions for stage 1.

                        =⇒ ——— new screen ——— ⇐=

   Suppose you chose Option A (safe) in decision 2. What is your outcome in this
decision?

  2
   The outcome is 200 for sure

  2 The outcome is 800 for sure

  2 The outcome can be either 0 or 800

  2 There is no bonus for sure

                        =⇒ ——— new screen ——— ⇐=

   Suppose you chose Option B (risky) in decision 4. What is your outcome in this
decision?

  2 The outcome is 400 for sure

  2 The outcome is 800 for sure

  2
   [Coin & Ext. only: You will toss a coin to determine] [Nature only: A
     random draw of the computer will determine] the outcome that can be either
     0 or 800

                                         60
  2 There is no bonus for sure

                      =⇒ ——— new screen ——— ⇐=

   Ext. only Suppose you chose Option B (risky) in decision 4. You flip a coin
and self-report HEADS. What is the outcome?

  2 You will receive 0 and the other worker 800

  2
   You will receive 800 and the other worker 0

  2 Both, you and the other worker will receive 800

  2 Both, you and the other worker will receive 0

                      =⇒ ——— new screen ——— ⇐=

    Ext. only Suppose you chose Option A (safe) in decision 4. What is the
outcome?

  2 You will receive 0 and the other worker 400

  2 You will receive 400 and the other worker 0

  2 You will receive 800 and the other worker 0

  2
   You will receive 400 and the bonus of the other worker will be determined by
     the computer

             =⇒ ——— text in case of wrong answer ——— ⇐=

        =⇒ ——— new screen: sample screen for decision 1 ——— ⇐=

                                      61
Decision 1 Please decide between option A and B.

  # Option A (safe): 100 tokens

  # Option B (risky): 0 or 800 tokens

Please remember that in option B the two outcomes (0 and 800 tokens) are equally
likely. [Nature only: If you choose option B, the computer will resolve the lottery.
The outcome will be reported in the end.]
[Ext. only: If you choose option A you will receive that amount for sure while the
other worker will determine his outcome independently.] Coin and Ext.: If you
choose option B after the last decision you have to flip a coin. If it lands face-up
on Tails you will get 0 tokens [Ext. only: and the other worker 800]. If it lands
face-up on Heads you get 800 tokens [Ext. only: and the other worker 0]. Please
notice that you have to report the outcome of the coin flip truthfully. You may also
use justflipacoin.com to virtually flip a coin.

          =⇒ ——— new screen: sample screen for result 1 ——— ⇐=

Decision 1 – Coin flip [Coin and Ext. only]               You chose Option B (risky) in
decision 1.
Please flip a coin and indicate the outcome. If it lands on Heads you receive 800
tokens, if it lands on Tails you will receive 0 tokens.
Please report your answer truthfully.

  # Tails: 0 tokens [Ext. only: for you and 800 tokens for the other worker ]

  # Heads: 800 tokens [Ext. only: for you and 0 tokens for the other worker ]

   You may also use justflipacoin.com to virtually flip a coin.

              =⇒ ——— new screen: stage 2 and beliefs ——— ⇐=

                                           62
Stage 2

Thank you for completing stage 1 of the study. We will now explain stage 2. In
stage 2 you will be randomly matched with another worker (partner, henceforth),
who has completed the exact same study as you have. One of the 5 decisions will
be randomly selected.

   A third person will be informed about the assignment, the rules, your choice and
your partner’s choice in the selected decision. In case you or your partner chose
option B (risky), the third person is also informed about the [Coin & Ext. only:
self-reported] outcome of the [Nature only: random draw.] [Coin & Ext. only:
coin toss.]

   The third person will be given the opportunity to redistribute the total amount
of tokens generated between you and your partner. The total amount redistributed
to you and to your partner must be equal to the sum of tokens you two got in the
selected decision. The third person can leae everything as it is, or he/she can give
some of your tokens to your partner or vice-versa. The redistribution done by the
third person will determine your bonus for the present assignment. You will receive
your bonus within one week from the completion of the assignment.

   Please answer the following questions for stage 2:

   In decision 3 you selected Option [A safe/B risky - and your [Coin &Ext.
only: self-reported] outcome was [XX] tokens]. Suppose your partner chose
Option A (safe) for decision 3. A third person will now redistribute the sum of
tokens, which equals [SUM], between you and your partner. How do you think the
tokens will be redistributed?
(NOTE: The distributed tokens must sum up to [SUM] tokens.)

                                        63
 Amount of tokens you will receive: [blank]

Amount of tokens your partner will receive: [blank]

   In decision 3 you selected Option [A safe/B risky -and your [Coin & Ext.
only: self-reported] outcome was [XX] tokens]. Suppose your partner chose
Option B (risky) with the [Coin & Ext. only: self-reported] outcome of
0 tokens for decision 3. A third person will now redistribute the sum of tokens,
which equals [SUM], between you and your partner. How do you think the tokens
will be redistributed?
(NOTE: The distributed tokens must sum up to [SUM] tokens.)
 Amount of tokens you will receive: [blank]

Amount of tokens your partner will receive: [blank]

   In decision 3 you selected Option [A safe/B risky - and your [Coin & Ext.
only: self-reported] outcome was [XX] tokens]. Suppose your partner chose
Option B (risky) with the [Coin & Ext. only: self-reported] outcome of
800 tokens for decision 3. A third person will now redistribute the sum of tokens,
which equals [SUM], between you and your partner. How do you think the tokens
will be redistributed?
(NOTE: The distributed tokens must sum up to [SUM] tokens.)
 Amount of tokens you will receive: [blank]

Amount of tokens your partner will receive: [blank]

                =⇒ ——— new screen: validation code ——— ⇐=

Validation code. Please enter this code <code here> in the MTurk HIT
to complete the study.

                                       64
IMPORTANT: you need to enter this code to collect your payments.

                =⇒ ——— new screen: last screen ——— ⇐=

Thank you for completing this study. Your answers were transmitted. You
may close the browser, window or tab now.

                                      65
Instructions for idle stakeholders (Ext. treatment only )

   If you complete the study, you will earn a fixed amount of $0.30 plus a
bonus which can be either 800 tokens or 0 tokens. All earnings are expressed in to-
kens that will be converted into real money at the end of the study ($1=300 tokens).

   In this HIT there are two types of roles: worker 1 and worker 2. You have been
assigned to the role of worker 2.

Your task:

Your task is to read worker 1’s instructions. The instructions will give a detailed
explanation of the task carried out by worker 1 and are also important for you as
they explain how your bonus – either 0 tokens or 800 tokens – is determined. It is
important that you read the instructions for worker 1 carefully, as you will be asked
to answer a number of questions concerning these instructions.
The study will take about 10 minutes to complete (including the time for reading
the instructions). You will receive a code to collect your payment via MTurk upon
completion. You will only be able to receive the code if you answer all questions
correctly.

                        =⇒ ——— new screen ——— ⇐=

   Please read the instructions for worker 1 below and then proceed to the next
page to answer the questions.

                                         66
Instructions for worker 1

Worker 1 will face five decisions. In each decision, he has to choose between two
options: option A and option B (see Table C-2).

                                         Table C-2

               Decision   Option A                    Option B
                  1       100 for sure   800 with prob 50% or 0 with prob 50%
                  2       200 for sure   800 with prob 50% or 0 with prob 50%
                  3       300 for sure   800 with prob 50% or 0 with prob 50%
                  4       400 for sure   800 with prob 50% or 0 with prob 50%
                  5       500 for sure   800 with prob 50% or 0 with prob 50%

Option A is safe. The safe amount changes in each decision: it ranges from 100
tokens in decision 1 to 500 tokens in decision 5.

Option B is risky. Option B is the same for all five decisions. If worker 1 selects
option B, he has a 50% probability of earning 0 tokens and a 50% probability of
earning 800 tokens. If he chooses option B for a given decision, after the last deci-
sion he has to flip a coin. If the coin lands face-up on Tails he gets 0 tokens, if it
lands face-up on Heads he gets 800 tokens. Please notice that he has to report the
outcome of the coin flip truthfully. He may also use justflipacoin.com to virtually
flip a coin.

   Worker 1 will be matched with another worker - worker 2 (you). Worker 2 will
be informed about the rules and will have to answer control questions.
The bonus of worker 2 will be either 0 or 800 tokens. The bonus is determined as
follows:

   • If worker 1 chooses Option A (safe), the bonus for worker 2 is randomly
      determined by the computer (each outcome has the same probability of being
      drawn). That is, his choice will not affect worker 2’s bonus;

                                            67
   • If worker 1 chooses Option B (risky), his bonus and worker 2’s bonus
      will depend on your coin flip:

        – If worker 1 reports that the coin landed face-up on TAILS, he earns 0
           tokens and worker 2 earns 800 tokens;

        – If worker 1 reports that the coin landed face-up on HEADS, he earns 800
           tokens and worker 2 earns 0 tokens

                        =⇒ ——— new screen ——— ⇐=

   Suppose worker 1 chose Option A (safe) in decision 2. What is worker 1’s outcome
in this decision?

   2
    The outcome is 200 for sure

  2 The outcome is 800 for sure

  2 The outcome can be either 0 or 800

  2 There is no bonus for sure

                        =⇒ ——— new screen ——— ⇐=

   Suppose worker 1 chose Option B (risky) in decision 4. What is worker 1’s
outcome in this decision?

  2 The outcome is 400 for sure

  2 The outcome is 800 for sure

   2
    Worker 1 will toss a coin to determine the outcome that can be either 0 or 800

  2 There is no bonus for sure

                        =⇒ ——— new screen ——— ⇐=

                                        68
   Suppose worker 1 chose Option B (risky) in decision 4. Worker 1 flips a coin and
self-reports HEADS. What is the outcome?

  2 Worker 1 will receive 0 and worker 2 receives 800

  2
   Worker 1 will receive 800 and worker 2 recieves 0

  2 Both, worker 1 and worker 2 will receive 800

  2 Both, worker 1 and worker 2 will receive 0

                       =⇒ ——— new screen ——— ⇐=

   Suppose worker 1 chose Option A (safe) in decision 4. What is the outcome?

  2 Worker 1 will receive 0 and worker 2 receives 400

  2 Worker 1 will receive 400 and worker 2 receives 0

  2 Worker 1 will receive 800 and worker 2 receives 0

  2
   Worker 1 will receive 400 and worker 2’s bonus will be determined by the
     computer

              =⇒ ——— text in case of wrong answer ——— ⇐=

                       =⇒ ——— new screen ——— ⇐=

   Your bonus. Your bonus is XX tokens.

                =⇒ ——— new screen: validation code ——— ⇐=

                                        69
Validation code. Please enter this code <code here> in the MTurk HIT
to complete the study.

IMPORTANT: you need to enter this code to collect your payments.

                =⇒ ——— new screen: last screen ——— ⇐=

Thank you for completing this study. Your answers were transmitted. You
may close the browser, window or tab now.

                                      70
Instructions for Spectators24

      Welcome. The purpose of this study is to investigate how people make decisions.
From now until the end of the study, any communication with other participants is
not allowed. If you have a question, please raise your hand and one of us will come
to your desk to answer it. [Nature & Self-Report sessions without beliefs
only: Upon completion of the study, you will receive a payment of €10, includ-
ing €4 show-up fee.] [Ext. & Self-Report sessions with beliefs only: For
showing-up on time, you will receive €4. This study comprises three parts and you
can earn additional money during the study. Payments will be made upon comple-
tion of the study, anonymously, and in cash.]

      [Ext. & Self-Report sessions with beliefs only:

                                Instructions for Part 1

      For Part 1, you will receive a fixed payment of €6.]

Overview. You will be presented with 20 decisions, one after the other. In each
decision, your task is to decide how to redistribute the money between an ORANGE
and a BLUE player. One of these decisions will have real monetary consequences for
two individuals that we recruited via an international online marketplace to conduct
an assignment. We will first explain in detail the task we gave to the individuals
[Ext. only:, ORANGE and BLUE,] who participated in the online assignment.
After that, we will provide you with further information about your task.

Online Assignment. A few days ago we recruited participants via an interna-
tional online marketplace to conduct an assignment. They were offered a fixed
 24
      Translated from German. Original instructions are available upon request from the authors.

                                                71
participation compensation of $0.60. [Ext. only: We will now describe the assign-
ment for ORANGE and BLUE. Each ORANGE and BLUE player was also matched
with a GREEN player, whose task will be described later on.]

   The [Ext.     only: ORANGE and BLUE player’s] assignment consisted of 5
decisions. In each decision, they had to choose between two options: option A
and option B (see Table 1). All values in the assignment were expressed in tokens.
Tokens are exchanged at the rate of $1=300 tokens. Please notice that the amount
of money at stake is above the average amount for similar tasks in the same online
marketplace.

                             Table C-3: Online decisions

           Decision    Option A                     Option B
              1        100 for sure   800 with prob. 50% or 0 with prob. 50%
              2        200 for sure   800 with prob. 50% or 0 with prob. 50%
              3        300 for sure   800 with prob. 50% or 0 with prob. 50%
              4        400 for sure   800 with prob. 50% or 0 with prob. 50%
              5        500 for sure   800 with prob. 50% or 0 with prob. 50%

Option A is safe. The safe amount changed in each decision: it ranged from 100
tokens in decision 1 to 500 tokens in decision 5.

Option B is risky. Option B was the same for all five decisions. If option B
was selected, the participant had a 50% probability of earning 0 tokens and a 50%
probability of earning 800 tokens. [Nature only: If a participant chose option B
for a given decision, the computer resolved the lottery at the end of the assignment.]
[Self-Report only: If a participant chose option B, for a given decision, he/she
was asked to flip a coin. If the coin landed face-up, on Tails, the outcome was 0
tokens; if it landed face-up on Heads, the outcome was 800 tokens. Participants were
asked to report the outcome of the coin flip truthfully and were given a link to flip a
coin virtually in case they did not have a coin with them (see sample screen shot in
Figure C-1).]

                                          72
[Ext. only: Each ORANGE and BLUE player was matched with a GREEN player.
The GREEN player was informed about the rules and had to answer the same control
questions but did not make any decisions. The outcome for GREEN was either 0 or
800 and it was determined as follows:

   • If ORANGE or BLUE chose Option A (safe) it did not affect GREEN’s
       outcome. GREEN’s outcome (0 or 800) was then randomly determined by the
       computer (each outcome has the same probability of being drawn).

   • If ORANGE or BLUE chose Option B (risky) he affected GREEN’s out-
       come:

         – If ORANGE or BLUE reported Tails, his outcome was 0 tokens and
           GREEN’s outcome was 800 tokens.

         – If ORANGE or BLUE reported Heads, his outcome 800 tokens and GREEN’
           outcome was 0 tokens.

   ]

 Figure C-1: Sample screen shot from the online assignment (Self-Report only)

   Participants were allowed to take part in the assignment only if had they correctly
answered all control questions. After collecting all the data, we randomly formed
pairs and selected at random one of the 5 decisions. After completing the assignment,

                                         73
     Figure C-2: Sample screen shot from the online assignment (Ext. only)

participants were told that a third person would be informed about the rules and
the outcome of the assignment, and would be given the opportunity to redistribute
the earnings and thus determine how much they were paid for the assignment.

Your Task. You are the third person and we now want you to choose whether
to redistribute the tokens for the assignment between [Nature & Self-Report
only: two people] [Ext. only: ORANGE and BLUE ]. Your decision is completely
anonymous. The [Ext. only: ORANGE and BLUE ] people who participated in
the online assignment will receive the payment that you choose for them within a
few days, but will not receive any further information.

   Figure C-3 shows a sample decision screen. In the upper part of the screen, you
can see the initial situation for the ORANGE and BLUE player. For each player,
you can see whether they chose option A (safe) or option B (risky). In each decision,
you will be able to see the amount of tokens yielded by the safe option A. In this
example, the safe level is 500 tokens. [Ext. only: You can also see who determined
the outcome for GREEN 1 and GREEN 2.]

   In the example in Figure C-3, ORANGE chose option B and BLUE chose option
A. Recall that the outcome of option B is determined [Nature only: by a random

                                         74
             Figure C-3: Sample screen shot (Self-Report treatment)

Notes: In the Nature treatment, the sentence “ORANGE reported HEADS” was not displayed.

                 Figure C-4: Sample screen shot (Ext. treatment)

draw of the computer and both outcomes –0 and 800 tokens– have the same prob-
ability of being randomly selected.] [Self-Report & Ext. only: by the toss of a
coin. Participants [Ext. only: ORANGE and BLUE,] in the online assignment,

                                          75
were asked to toss a coin and self-report the outcome truthfully. If a participant
reported TAILS the outcome of option B was 0 tokens, [Ext. only: and 800 tokens
for GREEN]. If the participant reported HEADS the outcome of option B was 800
tokens [Ext. only: and thus GREEN’s outcome was 0 tokens].] In this example,
the outcome for ORANGE was 800 tokens [Self-Report & Ext. only: – as he re-
ported HEADS] – [Ext. only: and hence the outcome for GREEN 1 was 0. BLUE
chose option A (safe) yielding an outcome of 500 tokens. Thus GREEN 2’s outcome
was determined by a random draw of the computer.]

   In the central part of the screen you can see the sum of the tokens by ORANGE
and BLUE players. In the example, the sum of tokens is 1300. Your task is to
decide whether and how to redistribute the total amount of tokens be-
tween ORANGE and BLUE. You can choose any positive amount in steps of
25 tokens, as long as you redistribute all tokens. In our example, the sum of what
you give to ORANGE and BLUE must be exactly 1300 tokens.

   You have to make 20 decisions and one decision will be relevant – that is, it will
have actual monetary consequences – for two individuals who have completed the
online assignment. You will not know in advance which decision is relevant for the
earnings of other individuals. This means that you have to pay attention to every
decision.

   Before starting, please answer a few control questions.

                                         76
                     =⇒ ——— new section ——— ⇐=

                          Control Questions

1. Suppose a participant in the online assignment chose Option A (safe) in deci-
  sion 2 (see Table C-2). What is the outcome of this decision?

     2
      The outcome is 200 for sure.

     2 The outcome is 800 for sure.

     2 The outcome can be either 0 or 800.

     2 The outcome is 0 for sure.

2. Suppose a participant in the online assignment chose Option B (risky) in
  decision 4. What is the outcome of this decision?

     2 The outcome is 400 for sure.

     2 The outcome is 800 for sure.

     2
      [Self-Report & Ext.        only: The participant had to toss a coin to
       determine] [Nature only: A random draw of the computer determined]
       the outcome that can be either 0 or 800.

     2 The outcome is 0 for sure.

3. You are the third person who has to choose how to redistribute the tokens
  from the assignment

     2 Your identity will be revealed to the participant in the online assignment.

     2
      One of your decisions will have real monetary consequences for two par-
       ticipants in the online assignment.

                                      77
     2 You have to make only one decision.

4. Suppose ORANGE chose option A in decision 3. BLUE, instead, chose option
  B and [Nature only: the computer selected at random the low amount.]
  [Self-Report & Ext. only: self-reported TAILS.] What is the total number
  of tokens earned in this situation? (e.g., the sum of the tokens by ORANGE
  and BLUE)

     2 The total number of tokens is 200.

     2 The total number of tokens is 800.

     2 The total number of tokens is 1100.

     2
      The total number of tokens is 300.

5. Suppose the total number of tokens earned in a situation is 1600.

     2 You can give 0 tokens to both ORANGE and BLUE.

     2
      The sum of the tokens you give to ORANGE and BLUE has to be exactly
       1600.

     2 The sum of the tokens you give to ORANGE and BLUE can be larger
       than 1600.

     2 The sum of the tokens you give to ORANGE and BLUE can be smaller
       than 1600.

  Ext. only:

6. Suppose a participant chosen option B (risky) and self-reported HEADS. What
  is the outcome of this decision?

     2 The participant receives 0 and GREEN receives 800.

                                     78
     2 The participant and GREEN both receive 800.

     2 The participant and GREEN both receive 0.

     2
      The participant receives 800 and GREEN receives 0.

7. Suppose a participant chose option A (safe) in decision 4. What is the outcome
   of this decision?

     2
      The participant receives 400 and GREEN’s outcome will be randomly
        determined by the computer.

     2 The participant receives 800 and GREEN 0.

     2 The participant receives 400 and GREEN 0.

     2 The participant receives 0 and GREEN 400.

8. Which of the following statements is not correct?

     2 You will redistribute the sum of tokens between ORANGE and BLUE.

     2
      GREEN always flips a coin to decide his outcome.

     2 All participants were informed about the rules and had to answer control
        questions.

     2 GREEN’s outcome is either 0 or 800.

                       =⇒ ——— new section ——— ⇐=

                          Final Questionnaire

1. Gender

     2 Male

                                      79
     2 Female

2. Age:

3. Field of study

     2 Medicine

     2 Physics, Biology, Mathematics

     2 Computer science

     2 Social sciences

     2 Psychology

     2 Other

4. Please indicate where you were born

     2 Schleswig-Holstein

     2 Mecklenburg-Vorpommern

     2 Hamburg

     2 Bremen

     2 Niedersachsen

     2 Hessen

     2 Nordrhein-Westfalen

     2 Rheinland-Pfalz

     2 Saarland

     2 Baden-Württemberg

     2 Bayern

                                    80
       2 Brandenburg

       2 Berlin

       2 Sachsen

       2 Sachsen-Anhalt

       2 Thüringen

       2 Outside Germany

  5. In political matters, people talk of the left and the right. How would you place
     your views on this scale, generally speaking?
                  ○       ○       ○   ○       ○    ○       ○       ○        ○       ○
       Left       1       2       3       4   5        6   7        8       9       10    Right

  6. We now want you to indicate to what extent you agree with the following statement. 1
     means that you agree completely with the statement on the left, 10 means that you agree
     completely with the statement on the right, and the numbers in between indicate the extent
     to which you agree or disagree with the statements.
       A society should aim to equal-                          A society should not aim to
       ize incomes.                                            equalize incomes

              ○       ○       ○       ○       ○        ○   ○            ○       ○        ○
              1       2       3       4       5        6       7        8       9        10

  7. Generally speaking, would you say that most people can be trusted or that you need to be
     very careful in dealing with people?

       2 Most people can be trusted.

       2 Need to be very careful.

   In addition, subjects answered the 60-item version of the HEXACO Personality
Inventory-Revised Test (http://hexaco.org/hexaco-inventory).

                                                  81
Instructions for beliefs and risk aversion in the lab25

                                Instructions for Part 2

       In this part, we ask you to guess what people chose in the online assignment
explained before.

Your Task. Please consider the decision between Option A that yields 300 tokens
for sure and Option B that yields 800 with a probability of 50% and 0 with a
probability of 50%. You will have to answer the following two questions:

       • Question 1: What is the percentage of participants in the online assignment
         who chose Option B (risky)?

       • Question 2: Consider now the online participants who have chosen Option
         B: what is the percentage of participants who reported Heads? Please recall
         that Heads yielded 800 tokens for the participant and Tails 0 tokens for the
         participant.

Your Payment. You can earn a substantial amount of money based on the ac-
curacy of your guess, as reported in Table C-4. If your guess is correct, you can
earn €22. If your guess deviates from the true value by 5 percentage points (plus
or minus), you can earn €20.90. If your guess deviates by more than 21 percentage
points, you can receive €2 for this part.

       After everyone has answered both questions, six participants will be chosen at
random for payment for this part. The selected participants will be paid for one
of the two questions, selected at random. Since you do not know in advance who
  25
    Translated from German. Original instructions are available upon request from the authors.
This set of instructions was used only in two Self-Report and two Externalities sessions, for a total
of 120 participants.

                                                 82
                           Table C-4: Your payment

                   deviation in percentage points   payment
                   exact number                      €22.00
                   between 1 and 5                   €20.90
                   between 6 and 10                  €17.60
                   between 11 and 15                 €12.10
                   between 16 and 20                  €4.40
                   over 21                            €2.00

and which question will be chosen, it is important that you pay attention to both
answers.

                                       83
                          Instructions for Part 3

Your task. Now, please select one option out of six different options. The six
different options are displayed in Figure C-5. You must select one and only one of
these gambles.

                        Figure C-5: Options and payments

Options and earnings. Each option has two possible colors (green and red), each
with a 50% probabilitie of occurring. Your earnings for this part of the study will
be determined by:

   • Which of the six options you select; and

   • Which of the two possible colors (green or red) occurs

For example, if you select Option 4 and green occurs, you earn €52. If red occurs,
you earn €16.

   At the end of this task, the computer will randomly select one participant for
payment. The computer will then randomly draw one of the two colors (green or red)

                                        84
and the earnings for the selected participant will be determined. Please remember
that for every option, each color has a 50% chance of occurring.

                                        85
Instructions for beliefs in the classroom26

                                  Instructions
Welcome. The purpose of this study is to investigate how people make decisions.
[Experimenter only If you have a question please raise your hand, after the in-
structions have been read and one of us will come to your desk to answer it. Your
answers will be treated anonymously.] More specifically, you will be asked to guess
the results of a previous study. [Experimenter only We will now explain both the
previous task – an online assignment – and your task in detail.] From now until the
end of the study, any communication with other participants is not allowed.

Online Assignment. We recruited over 100 participants via an international on-
line marketplace and asked them to make a series of decisions. Participants had to
choose between:

       • Option A (safe) yields a safe payment, with the amount specified on your
         decision sheet;

       • Option B (risky) yields 800 tokens with a 50% probability and 0 tokens with
         a 50% probability. If a participant chose option B he/she was asked to flip a
         coin and self-report the result:

           – if the coin landed face-up on Heads the outcome was 800 tokens;

           – if the coin landed face-up on Tails the outcome was 0 tokens.

Participants were asked to report the outcome of the coin flip truthfully. Participants
were aware that a self-reported coin toss would resolve the outcome for Option B
before choosing between the two options. All earnings were expressed in tokens and
exchanged at the rate of $1=300 tokens.
  26
    Translated from German. Original instructions are available upon request from the authors.
A total of 289 students participated in the classroom experiment.

                                             86
Your Task. We ask you to guess what people did in the online assignment. You
will have to answer the following two questions:

   • Question 1: What is the percentage of participants who chose Option B
      (risky)?

   • Question 2: Consider now the participants who have chosen Option B: what
      is the percentage of participants who reported Heads? Please recall that Heads
      yielded 800 tokens and Tails 0 tokens.

Your Payment. You can earn a substantial amount of money based on the accu-
racy of your guess, as reported in Table C-5. If your guess is correct you can earn
€22.00. If your guess deviates from the true value by 5 percentage points (plus or
minus), you can earn €20.90. If your guess deviates by more than 21 percentage
points, you get €2.00.

                             Table C-5: Your payment

                    deviation in percentage points    payment
                    exact number                       €22.00
                    between 1 and 5                    €20.90
                    between 6 and 10                   €17.60
                    between 11 and 15                  €12.10
                    between 16 and 20                   €4.40
                    over 21                             €2.00

   After everyone has answered both questions, one out of every 20 students will be
chosen at random for payment. The selected students will be paid for one of the two
questions, selected at random. Since you do not know in advance who and which
question will be chosen, it is important that you pay attention to both answers.
You can now make your decisions. Please read the information on the decision sheet
carefully.

                                        87
                                    Decision sheet

            Safe level for Option A = 100 tokens for sure

   Participants in the online assignment had to make a decision between Option A
and Option B.

                       Option A (safe)          Option B (risky)

                             100 tokens        800 tokens if Heads
                              for sure          0 tokens if Tails

                   Please answer the following questions

Question 1: What is the percentage of participants who chose Option B (risky)?

                                                  %
                       Please write an integer number between 0 and 100

Question 2: Consider now the participants who have chosen Option B: what is
the percentage of participants who reported Heads? Please recall that Heads yielded 800
tokens and Tails 0 tokens.

                                                  %
                       Please write an integer number between 0 and 100

   Gender:

   2 Male

   2 Female

                                             88
Field of study:

2 Economics

2 Economics majoring in sociology

2 Sociology

2 Math

2 Other

                                    89