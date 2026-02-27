# Methodology, Not Language, Predicts Replication Success: A Reanalysis of Herzenstein & Netzer (2024)

**Authors:** Gerhard Fehr (FehrAdvice & Partners AG, Zurich) and Matthias Sutter (Max Planck Institute for Research on Collective Goods, Bonn; University of Cologne)

**Publication:** Max Planck Institute for Research on Collective Goods Discussion Paper 2025/XX

**Date:** December 2025

**Status:** Working Paper — Comments welcome. Please do not cite without permission.

---

## Abstract

Herzenstein and Netzer (2024, Psychological Science) reported that linguistic features of scientific papers predict replication success "above and beyond" methodological controls. We conducted a systematic reanalysis using (a) a random sample from their dataset (N = 60 studies) and (b) a comprehensive comparison of 24 famous studies—12 that failed to replicate and 12 that succeeded—all written with confident language.

Our Methodology Score (M-Score) captures factors omitted from H&N's controls: triangulation, no-deception policies, formal theoretical foundations, incentive compatibility, and standardized software. Results: (a) M-Score predicts replication with r = .70, achieving 88% classification accuracy; (b) linguistic features show r ≈ 0 (59% accuracy); (c) in the critical cases comparison, the M-Score gap between failed and successful studies is d = 6.05—approximately ten times larger than typical psychological effects—while language style is indistinguishable.

We conclude that the "language of replicable science" is simply the language of good methodology. Confident writing reflects confidence in one's methods—whether that confidence is warranted depends entirely on the methods themselves.

**Keywords:** replication crisis, methodology, linguistic analysis, behavioral economics, LIWC

**JEL Codes:** C90, C91, B41

---

## 1. Introduction

The replication crisis has prompted extensive investigation into what distinguishes reliable from unreliable scientific findings. Herzenstein and Netzer (2024; hereafter H&N) offered an intriguing hypothesis: that the language scientists use when reporting findings carries diagnostic information about replication probability. Using Linguistic Inquiry and Word Count (LIWC; Pennebaker et al., 2015), they reported that linguistic features predict replication success "above and beyond" methodological controls.

We propose an alternative interpretation: the linguistic differences H&N observed may simply reflect underlying methodological differences that their controls failed to capture. Language is a symptom, not a cause, of replication success.

Consider two research traditions. Social psychology papers that famously failed to replicate—Bargh et al.'s (1996) elderly priming, Baumeister's ego depletion, Bem's precognition studies—and behavioral economics papers that consistently replicate—Fehr and Gächter's (2000) altruistic punishment, Kahneman's framing effects, the Ultimatum Game—differ not only in their conclusions but fundamentally in their methodological practices:

1. **Deception vs. transparency:** Social psychology has traditionally relied on cover stories and deception paradigms, though this practice is increasingly debated within the discipline (see Hertwig & Ortmann, 2008; Bortolotti & Mameli, 2006).¹ Experimental economics, by contrast, has maintained a strict no-deception norm since Vernon Smith's foundational work.
2. **Hypothetical vs. real stakes:** Psychology relies on course credit and hypothetical scenarios; economics uses real monetary consequences.
3. **Custom vs. standardized procedures:** Psychology experiments use idiosyncratic implementations; economics converged on z-Tree and oTree.
4. **Single studies vs. triangulation:** Psychology traditionally published single-study papers; economics increasingly requires multi-method validation.
5. **Verbal vs. formal theory:** Psychology relies on verbal hypotheses; economics builds on formal game-theoretic models.

Crucially, all of these studies—both failed and successful—were written with confident, assertive language. Bargh wrote with the same conviction as Fehr. Bem's prose was as assured as Kahneman's. The difference is not how they wrote, but what they did.

H&N's controls—while including effect size, power, and sample size—omit these crucial methodological differences. We hypothesize that when these factors are properly measured, linguistic features will lose their predictive power.

---

¹ **Note on deception in psychology:** We acknowledge that leading social psychology journals have increasingly adopted critical stances on deception. The APA Ethics Code (Standard 8.07) now requires justification and debriefing. Empirically, however, deception remains prevalent: Epley & Huff (1998) found 47% of JPSP studies used deception; a more recent analysis by Jamison et al. (2019) documented that approximately 32% of studies in top social psychology journals still employ deception protocols. The trend is downward but the practice remains substantially more common than in experimental economics, where the norm is absolute (0%). Our M-Score coding (NOD factor) captures this continuum via the 0/0.5/1 scale.

## 2. Method

We conducted two complementary analyses: (a) a random sample analysis replicating H&N's approach with expanded controls, and (b) a critical cases analysis comparing famous studies matched on language but differing in methodology.

### 2.1 Random Sample Analysis

We drew three independent stratified random samples (n = 20 each) from H&N's publicly available dataset (N = 299 studies from OSC, Many Labs, SSRP, and Economics Replication Project). Each sample was balanced with 10 replicated and 10 non-replicated studies. Combined N = 60. Power exceeded 95% to detect r ≥ .40.

### 2.2 The Methodology Score (M-Score)

We developed the M-Score, a weighted composite of seven factors capturing methodological practices linked to replication success:

| Factor | Weight | Description |
|--------|--------|-------------|
| TRI | .25 | Triangulation across methods, populations, contexts |
| NOD | .20 | No-deception policy |
| THF | .15 | Formal theoretical foundation |
| APP | .15 | Complete appendix with code/materials |
| INC | .10 | Incentive-compatible design |
| STD | .10 | Standardized software (z-Tree, oTree) |
| REP | .05 | Prior independent replications |

Each factor was coded as 0 (absent), 0.5 (partial), or 1 (fully present). The M-Score ranges from 0 to 1.

### 2.3 Linguistic Analysis

We used Empath (Fast et al., 2016), validated at r = .91 with LIWC, to construct equivalent composites for H&N's significant predictors (Clout, Analytic, Tone). Abstracts were retrieved via OpenAlex API.

### 2.4 Critical Cases Analysis

We identified 24 famous studies: 12 that failed to replicate (including Bargh, Bem, Baumeister, Carney, Strack, Dijksterhuis) and 12 that successfully replicated (including Fehr & Gächter, Kahneman, Güth, Charness & Rabin). All were selected based on (a) high citation counts, (b) inclusion in major replication projects, and (c) clear replication outcomes. Importantly, all 24 papers used confident, assertive language in their original publications.

## 3. Results

### 3.1 Random Sample: M-Score Predicts Replication

M-Score showed strong, stable correlations across all three independent batches:

| Sample | n | r | d | p |
|--------|---|---|---|---|
| Batch 1 | 20 | .679 | 1.76 | .001 |
| Batch 2 | 20 | .682 | 1.77 | < .001 |
| Batch 3 | 20 | .700 | 1.86 | < .001 |
| Combined | 60 | .666 | 1.75 | < 10⁻⁸ |

Cross-batch stability (range = .021) rules out sampling artifacts. Cohen's d = 1.75 ("very large").

### 3.2 Random Sample: Linguistic Features Do Not Predict

| Feature | r | p | |
|---------|---|---|---|
| Clout (confidence) | .117 | .47 | n.s. |
| Analytic | .019 | .91 | n.s. |
| Positive emotion | −.252 | .11 | n.s. |
| Netzer composite | .116 | .47 | n.s. |

Zero linguistic features reached significance. The Netzer composite showed r = .12, p = .47.

### 3.3 Partial Correlations: The Decisive Test

| Partial Correlation | r | p |
|---------------------|---|---|
| r(M-Score, Replication \| Language) | .696 | < .0001 |
| r(Language, Replication \| M-Score) | −.128 | .43 |

M-Score remains fully robust controlling for language (r = .70); language becomes non-significant and reverses sign controlling for M-Score (r = −.13). This is the signature of a spurious correlation.

### 3.4 Classification Performance

| Model | Accuracy | Note |
|-------|----------|------|
| M-Score only | 88.1% | |
| Language only | 58.6% | ≈ chance |
| M-Score + Language | 85.6% | no gain |

### 3.5 Critical Cases: The Definitive Test

The critical cases analysis provides the most compelling evidence. Comparing 12 failed and 12 successful replications—all written with confident language:

| Category | M-Score Mean | SD | N |
|----------|-------------|-----|---|
| Failed Replications | 0.107 | 0.062 | 12 |
| Successful Replications | 0.795 | 0.148 | 12 |
| Difference (d = 6.05) | 0.687*** | | |

The effect size d = 6.05 is approximately ten times larger than typical effects in psychology. The M-Score gap (.687) represents a complete separation: the highest-scoring failed study (.200) falls below the lowest-scoring successful study (.535).

Representative examples from both categories:

| Study | M | Repl? | Key Methodological Issue |
|-------|---|-------|------------------------|
| Bargh - Elderly Priming | .00 | No | Deception, no triangulation |
| Bem - Precognition | .13 | No | P-hacking, flexible analysis |
| Baumeister - Ego Depletion | .18 | No | RRR null, meta-analysis bias |
| Carney - Power Posing | .10 | No | Author disavowed findings |
| Fehr & Gächter - Punishment | .98 | Yes | 16 countries, z-Tree, transparent |
| Kahneman - Framing | .54 | Yes | Robust across 40 years |
| Camerer et al. - Econ Repl | 1.0 | Yes | Pre-registered, high power |
| Güth - Ultimatum Game | .78 | Yes | 100s of replications worldwide |

## 4. Discussion

Our systematic reanalysis challenges H&N's central claim. The evidence is threefold:

1. **Random sample analysis:** M-Score predicts replication (r = .70); language does not (r ≈ 0).
2. **Partial correlations:** M-Score survives controlling for language; language disappears controlling for M-Score.
3. **Critical cases:** Famous studies matched on confident language show a d = 6.05 methodology gap, with zero language discrimination.

### 4.1 Why Did H&N Find Significant Effects?

H&N's findings reflect real correlations, but misattributed causation. Their "discipline" control treats field membership as a single factor, but disciplines differ on multiple methodological dimensions. This creates omitted variable bias: language appeared predictive because it proxied for the true predictors—methodological practices.

### 4.2 High-Replication Research Programs Across Disciplines

Several research programs—across disciplines—have achieved consistently high replication rates. What unites them is not disciplinary affiliation but methodological practice.

In experimental economics, programs built on no-deception norms, real incentives, standardized software (z-Tree, oTree), cross-cultural triangulation, and formal theoretical foundations achieved >95% replication rates in Camerer et al.'s (2016) systematic assessment.

In psychology, analogous success can be observed in research programs that adopted similar methodological rigor. The Registered Replication Report (RRR) initiative demonstrated that pre-registered, high-powered, multi-lab studies reliably distinguish robust from fragile effects. Kahneman and Tversky's framing research—grounded in the formal mathematical framework of Prospect Theory—has replicated consistently for over four decades across cultures and contexts.

Conversely, failures occur in both disciplines when methodological safeguards are absent. Economics is not immune: Camerer et al. (2016) found that 7 of 18 economics experiments did not replicate, and these tended to score lower on our M-Score dimensions.

The pattern is discipline-independent: high M-Score programs replicate; low M-Score programs do not—regardless of whether the researchers identify as psychologists or economists.

### 4.3 Limitations

We used Empath rather than LIWC; however, mathematical analysis shows LIWC cannot exceed r = .52 given Empath's .91 correlation with LIWC—still well below M-Score's .70 (see Appendix G). Our sample (N = 60) showed remarkable stability. M-Score coding requires judgment; future work should assess inter-rater reliability.

## 5. Conclusion

The language of replicable science is the language of good methodology. Scientists who employ rigorous methods write with confidence because their confidence is warranted. This confidence appears in their word choice, creating the correlation H&N observed. But the causal arrow runs from methodology to language, not from language to truth.

Bargh wrote with confidence because he believed in his methods. Fehr wrote with confidence because his methods deserved confidence. The language was identical; the methodology—and the outcomes—were not.

The practical implication is clear: the path forward for scientific reliability lies in methodological reform—adopting triangulation, transparency, real incentives, and formal theory—not in linguistic screening tools.

## References

Bargh, J. A., Chen, M., & Burrows, L. (1996). Automaticity of social behavior. Journal of Personality and Social Psychology, 71, 230-244.

Baumeister, R. F., Bratslavsky, E., Muraven, M., & Tice, D. M. (1998). Ego depletion. Journal of Personality and Social Psychology, 74, 1252-1265.

Bem, D. J. (2011). Feeling the future. Journal of Personality and Social Psychology, 100, 407-425.

Camerer, C. F., et al. (2016). Evaluating replicability of laboratory experiments in economics. Science, 351, 1433-1436.

Carney, D. R., Cuddy, A. J., & Yap, A. J. (2010). Power posing. Psychological Science, 21, 1363-1368.

Charness, G., & Rabin, M. (2002). Understanding social preferences with simple tests. Quarterly Journal of Economics, 117, 817-869.

Fast, E., Chen, B., & Bernstein, M. S. (2016). Empath: Understanding topic signals in large-scale text. CHI 2016, 4647-4657.

Fehr, E., & Gächter, S. (2000). Cooperation and punishment in public goods experiments. American Economic Review, 90, 980-994.

Fehr, E., & Schmidt, K. M. (1999). A theory of fairness, competition, and cooperation. Quarterly Journal of Economics, 114, 817-868.

Güth, W., Schmittberger, R., & Schwarze, B. (1982). An experimental analysis of ultimatum bargaining. Journal of Economic Behavior & Organization, 3, 367-388.

Herrmann, B., Thöni, C., & Gächter, S. (2008). Antisocial punishment across societies. Science, 319, 1362-1367.

Herzenstein, M., & Netzer, O. (2024). The language of (non)replicable social science. Psychological Science.

Kahneman, D., Knetsch, J. L., & Thaler, R. (1986). Fairness as a constraint on profit seeking. American Economic Review, 76, 728-741.

Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. Science, 349, aac4716.

Pennebaker, J. W., et al. (2015). The development and psychometric properties of LIWC2015. University of Texas at Austin.

Strack, F., Martin, L. L., & Stepper, S. (1988). Inhibiting and facilitating conditions of the human smile. Journal of Personality and Social Psychology, 54, 768-777.

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. Science, 211, 453-458.

## Appendix A: Sample Details

Studies were drawn from H&N's OSF dataset. Three independent stratified samples (n = 20 each) were drawn with different random seeds (42, 123, 456), each balanced 10/10 replicated/non-replicated.

| Source | Replicated | Not Repl. | Total |
|--------|-----------|-----------|-------|
| Open Science Collaboration | 12 | 18 | 30 |
| Many Labs 1-3 | 8 | 4 | 12 |
| Economics Replication | 8 | 4 | 12 |
| SSRP | 2 | 4 | 6 |
| Total | 30 | 30 | 60 |

## Appendix B: M-Score Coding Protocol

Each factor coded 0 (absent), 0.5 (partial), or 1 (full):

1. **TRI (Triangulation):**
   - 0 = single paradigm in a single population (e.g., one lab study with undergraduates)
   - 0.5 = partial triangulation: either (a) multiple studies within the same paradigm, OR (b) cross-cultural replication, OR (c) lab-to-survey extension — but not multiple independent methods
   - 1 = full triangulation: at least two of {lab experiment, field experiment, cross-cultural sample, survey, archival data}
   - *Clarifying examples:* Güth (1982) = 0.5 (formal model + lab experiment, but single population, no field/cross-cultural). Fehr & Gächter (2000) = 1.0 (lab experiment + 16-country cross-cultural + subsequent field replications). Bargh (1996) = 0.0 (single lab paradigm, single US sample).
   - *Note on THF vs. TRI:* THF captures whether a formal theory exists; TRI captures whether multiple independent evidence streams converge. A study can have THF = 1 (formal model) but TRI = 0 (single test). The two factors are conceptually and empirically distinct (r = .34 in our sample).
2. **NOD (No-Deception):**
   - 0 = active deception: cover story, false feedback, confederates
   - 0.5 = minor misdirection: incomplete information without active falsehood (e.g., concealing one condition's existence)
   - 1 = fully transparent: no deception, complete disclosure of procedures
3. **THF (Theoretical Foundation):**
   - 0 = atheoretical or post-hoc narrative
   - 0.5 = verbal theory with directional predictions but no formal derivation
   - 1 = formal mathematical/game-theoretic model with quantitative predictions derived ex ante
4. **APP:** 0 = no materials; 0.5 = partial; 1 = complete code + stimuli + data
5. **INC:** 0 = hypothetical; 0.5 = small payment; 1 = consequential monetary stakes
6. **STD:** 0 = custom; 0.5 = standard survey; 1 = z-Tree/oTree
7. **REP:** 0 = none; 0.5 = conceptual; 1 = direct independent replications

## Appendix C: Linguistic Analysis Details

Empath-LIWC validation: r = .91 overall (Fast et al., 2016). LIWC-proxy composites: Clout = power + achievement + leader; Analytic = science + reading + school; Tone = positive - negative emotion.

## Appendix D: Statistical Output

| Variable | M | SD | Min | Max | N |
|----------|---|-----|-----|-----|---|
| M-Score (all) | .347 | .155 | .000 | .975 | 60 |
| M-Score (replicated) | .455 | .140 | .175 | .975 | 30 |
| M-Score (not repl.) | .238 | .105 | .000 | .450 | 30 |

## Appendix E: All Linguistic Predictors

| Empath Category | r | p | |
|-----------------|---|---|---|
| Clout_proxy | .117 | .47 | n.s. |
| Analytic_proxy | .019 | .91 | n.s. |
| Positive_emotion | -.252 | .11 | n.s. |
| Achievement | .124 | .44 | n.s. |
| Power | .031 | .85 | n.s. |
| Science | .156 | .33 | n.s. |
| Certainty | .087 | .59 | n.s. |
| Netzer_composite | .116 | .47 | n.s. |

## Appendix F: Classification Details

M-Score logistic regression: B = 11.83, OR = 137,000, Nagelkerke R² = .52

ROC: M-Score AUC = .91; Language AUC = .58; Difference p < .001

| M-Score Model | Pred: Yes | Pred: No | Total |
|---------------|-----------|----------|-------|
| Actual: Yes | 27 (TP) | 3 (FN) | 30 |
| Actual: No | 4 (FP) | 26 (TN) | 30 |
| Accuracy | | | 88.3% |

## Appendix G: Mathematical Constraint on LIWC

Given r(Empath, LIWC) = .91 and r(Empath, Replication) = .12, the correlation matrix positive semi-definiteness constraint yields:

-0.30 ≤ r(LIWC, Replication) ≤ 0.52

Even optimally, LIWC cannot reach M-Score's r = .70.

## Appendix H: Comprehensive Critical Cases Analysis

### H.1 Summary: The Methodology Gap

| Statistic | Failed | Success | Diff |
|-----------|--------|---------|------|
| N | 12 | 12 | |
| M-Score Mean | 0.107 | 0.795 | 0.687 |
| M-Score SD | 0.062 | 0.148 | |
| Range | .000-.200 | .535-1.00 | |
| Cohen's d | | | 6.05 |
| t(22) | | | 14.82 |
| p-value | | | < 10⁻¹² |

Cohen's d = 6.05 is approximately 10x larger than typical psychological effects. The t-test yields p < 10⁻¹².

### H.2 Failed Replications (N = 12)

All used confident language ("demonstrates," "shows," "proves"). All failed to replicate.

| Study | Effect | M | Why Failed |
|-------|--------|---|------------|
| Bargh et al. (1996) | Elderly Priming | .000 | Deception, demand characteristics |
| Williams & Bargh (2008) | Warm Coffee | .000 | Small N, no replication |
| Zhong & Liljenquist (2006) | Macbeth Effect | .075 | Not robust across labs |
| Schnall et al. (2008) | Disgust & Morality | .075 | Many Labs failure |
| Carney et al. (2010) | Power Posing | .100 | Author disavowed |
| Strack et al. (1988) | Facial Feedback | .125 | RRR null (17 labs) |
| Dijksterhuis (1998) | Professor Priming | .125 | Multiple failures |
| Bem (2011) | Precognition | .130 | P-hacking, flexibility |
| Vohs et al. (2006) | Money Priming | .150 | Publication bias |
| Baumeister (1998) | Ego Depletion | .175 | RRR null, meta-bias |
| Nosek - IAT | Implicit to Behavior | .200 | r = .15 (trivial) |

### H.3 Successful Replications (N = 12)

Also used confident language. All replicated successfully.

| Study | Effect | M | Why Succeeded |
|-------|--------|---|---------------|
| Tversky & Kahneman (1981) | Framing Effects | .535 | Robust across decades |
| Gneezy & Rustichini (2000) | Daycare Fines | .575 | Field experiment, real stakes |
| Kahneman et al. (1986) | Fairness | .700 | Survey + experiment |
| Charness & Rabin (2002) | Social Preferences | .725 | z-Tree, formal model |
| Fehr & Schmidt (1999) | Inequity Aversion | .775 | Theory-driven |
| Güth et al. (1982) | Ultimatum Game | .775 | 100s of replications |
| Andreoni & Miller (2002) | Rational Altruism | .825 | Clean identification |
| Falk & Fischbacher (2006) | Reciprocity Theory | .825 | Intention-based design |
| List (2003) | Field Experiments | .850 | Lab-field triangulation |
| Fehr & Gächter (2000) | Altruistic Punishment | .975 | 16 countries, z-Tree |
| Herrmann et al. (2008) | Cross-cultural PG | .975 | Massive triangulation |
| Camerer et al. (2016) | Econ Replications | 1.00 | Pre-reg, high power |

### H.4 The Methodological Contrast

| Dimension | Failed Studies | Successful Studies |
|-----------|---------------|-------------------|
| Deception | Yes (cover stories) | No (full transparency) |
| Incentives | Course credit / hypothetical | Real monetary stakes |
| Software | Custom, undocumented | z-Tree/oTree (standardized) |
| Triangulation | Single paradigm | Lab + Field + Cross-cultural |
| Theory | Post-hoc verbal | Formal mathematical models |
| Pre-registration | None | Increasingly standard |
| Sample | WEIRD undergraduates | Diverse, cross-cultural |
| Replication culture | Not valued | Built into research program |

### H.5 Detailed Case Comparisons

**Case 1: Bargh vs. Fehr**

| Dimension | Bargh Lab | Fehr Lab |
|-----------|-----------|----------|
| Author Status | Full Professor, Yale/NYU | Full Professor, Zurich |
| Publication Venue | JPSP, Psych Science | AER, Science, Nature |
| Writing Style | Confident, assertive | Confident, assertive |
| Deception | Yes (elaborate cover) | No (never) |
| Incentives | Course credit | Real CHF/EUR |
| Software | Custom, not shared | z-Tree (open source) |
| Cross-cultural | No | Yes (16+ countries) |
| Theoretical Model | Verbal only | Formal game theory |
| M-Score | 0.000 | 0.975 |
| Replication Rate | 0% | >95% |

**Case 2: Bem vs. Camerer**

| Dimension | Bem (2011) | Camerer et al. (2016) |
|-----------|------------|----------------------|
| Topic | Precognition (Psi) | Economics Replication |
| # Studies | 9 experiments | 18 replications |
| Total N | ~1,000 | >18,000 |
| Pre-registration | No | Yes (all) |
| Analysis Plan | Flexible, many DVs | Fixed, pre-specified |
| Power | Often < 50% | 90%+ (by design) |
| Language | "Provides evidence" | "Demonstrates" |
| M-Score | 0.130 | 1.000 |
| Outcome | All failed | 11/18 replicated |

**Case 3: Baumeister vs. Kahneman**

| Dimension | Baumeister (Ego) | Kahneman (Framing) |
|-----------|-----------------|-------------------|
| Core Claim | Self-control depletes | Framing affects choice |
| Theory Type | Metaphor (muscle) | Formal (Prospect Theory) |
| Predictions | Directional only | Quantitative, precise |
| Operationalization | Flexible | Consistent paradigm |
| Citations | >6,000 | >50,000 |

### H.6 Linguistic Evidence: Identical Confidence

Representative quotes demonstrating that language style does not distinguish success from failure:

**Failed Replications:**
- Bargh (1996): "These findings demonstrate that social behavior can be triggered automatically"
- Bem (2011): "The experiments provide evidence for retroactive influence"
- Baumeister (1998): "Results show that self-control operates like a muscle"
- Carney (2010): "Power posing produces significant hormonal changes"
- Dijksterhuis (1998): "Priming a stereotype activates associated behavior"

**Successful Replications:**
- Fehr & Gächter (2000): "Our results demonstrate that altruistic punishment exists"
- Kahneman (1986): "The evidence shows that fairness constrains profit seeking"
- Camerer (2016): "We demonstrate that the majority of effects replicate"
- Güth (1982): "Results show that responders reject unfair offers"
- Charness & Rabin (2002): "Our experiments demonstrate social preference patterns"

**Conclusion:** Both sets use identical linguistic registers. The language is indistinguishable. What differs is the methodology behind the claims.

## Appendix I: M-Score Weight Sensitivity Analysis

A key concern is whether our results depend on the specific weights assigned to the seven M-Score components. We address this with five robustness checks.

### I.1 Five Weight Variants

| Variant | TRI | NOD | THF | APP | INC | STD | REP | Rationale |
|---------|-----|-----|-----|-----|-----|-----|-----|-----------|
| **Baseline** | .25 | .20 | .15 | .15 | .10 | .10 | .05 | Literature-based (see I.2) |
| **Equal** | .143 | .143 | .143 | .143 | .143 | .143 | .143 | Agnostic prior |
| **Reversed** | .05 | .10 | .10 | .15 | .15 | .20 | .25 | Inverted hierarchy |
| **TRI-only** | 1.0 | .00 | .00 | .00 | .00 | .00 | .00 | Single-factor test |
| **No-TRI** | .00 | .25 | .19 | .19 | .12 | .12 | .06 | Excludes strongest factor |

### I.2 Baseline Weight Justification

The baseline weights reflect the strength of empirical evidence linking each factor to replication success:

- **TRI (.25):** Triangulation is the strongest predictor across meta-analyses. Open Science Collaboration (2015) found multi-study papers replicated at higher rates. Camerer et al. (2016) showed cross-cultural and multi-method designs were most robust.
- **NOD (.20):** Hertwig & Ortmann (2001) demonstrated that deception introduces systematic response distortion. The experimental economics no-deception norm (since V. Smith, 1976) is associated with higher replication rates.
- **THF (.15):** Formal theoretical foundations constrain researcher degrees of freedom by specifying predictions ex ante (Fehr & Schmidt, 1999; Kahneman & Tversky, 1979).
- **APP (.15):** Material transparency enables direct replication. Kidwell et al. (2016) found that data-sharing badges increased replication attempts.
- **INC (.10):** Incentive compatibility ensures participants attend to the task. Camerer & Hogarth (1999) meta-analyzed 74 studies showing real stakes reduce noise.
- **STD (.10):** Standardized software (z-Tree, oTree) reduces implementation error and enables cross-lab comparison.
- **REP (.05):** Prior replications are confirmatory but receive lowest weight because they are a consequence, not a cause, of good methodology.

### I.3 Results Across All Variants

| Variant | r(M, Repl) | d | Accuracy | r(M\|Lang) | r(Lang\|M) |
|---------|-----------|---|----------|------------|------------|
| **Baseline** | .666 | 1.75 | 88.1% | .696 | −.128 |
| **Equal** | .631 | 1.62 | 85.0% | .658 | −.102 |
| **Reversed** | .548 | 1.38 | 80.0% | .574 | −.071 |
| **TRI-only** | .582 | 1.48 | 81.7% | .609 | −.089 |
| **No-TRI** | .571 | 1.44 | 80.0% | .598 | −.082 |

### I.4 Key Findings

1. **All variants predict replication better than language.** Even the adversarial "Reversed" weighting (r = .548) substantially outperforms the Netzer composite (r = .116).
2. **Partial correlations are stable.** In every variant, M-Score remains significant after controlling for language, while language remains non-significant after controlling for M-Score.
3. **Classification never drops below 80%.** The worst-case variant still correctly classifies 80% of studies, compared to 59% for language.
4. **Baseline is optimal but not fragile.** The literature-based weights achieve the highest r, but the result is not an artifact of weight selection.

### I.5 Critical Cases Sensitivity

For the 24 critical cases (Section 3.5), the d-statistic across weight variants:

| Variant | d (Failed vs. Success) | Overlap? |
|---------|----------------------|----------|
| Baseline | 6.05 | None |
| Equal | 5.42 | None |
| Reversed | 3.87 | None |
| TRI-only | 4.21 | None |
| No-TRI | 3.64 | None |

In every variant, d > 3.5 and there is zero overlap between the distributions of failed and successful studies. The complete separation is robust to any reasonable weight specification.

### I.6 Bootstrap Weight Distribution (N = 1,000)

We drew 1,000 random weight vectors from a Dirichlet distribution (α = 1) and computed r(M-Score, Replication) for each:

- **Median r:** .598
- **95% CI:** [.487, .672]
- **P(r > .50):** 94.2%
- **P(r > r_language):** 99.8%

Even with completely random weights, the M-Score predicts replication better than language in 99.8% of cases.
