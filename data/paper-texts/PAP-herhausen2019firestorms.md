# Detecting, Preventing, and Mitigating Online Firestorms in Brand Communities

**Authors:** Dennis Herhausen, Stephan Ludwig, Dhruv Grewal, Jochen Wulf, Marcus Schoegel
**Journal:** Journal of Marketing, Vol. 83, No. 3, pp. 1-21
**Year:** 2019
**DOI:** 10.1177/0022242918822300
**Publisher:** American Marketing Association

---

## Abstract

Online firestorms pose severe threats to online brand communities. Any negative electronic word of mouth (eWOM) has the potential to become an online firestorm, yet not every post does, so finding ways to detect and respond to negative eWOM constitutes a critical managerial priority. The authors develop a comprehensive framework that integrates different drivers of negative eWOM and the response approaches that firms use to engage in and disengage from online conversations with complaining customers. A text-mining study of negative eWOM demonstrates distinct impacts of high- and low-arousal emotions, structural tie strength, and linguistic style match (between sender and brand community) on firestorm potential. The firm's response must be tailored to the intensity of arousal in the negative eWOM to limit the virality of potential online firestorms. The impact of initiated firestorms can be mitigated by distinct firm responses over time, and the effectiveness of different disengagement approaches also varies with their timing. For managers, these insights provide guidance on how to detect and reduce the virality of online firestorms.

**Keywords:** message dynamics, online brand community, online firestorms, text mining, word of mouth

---

## Introduction

More than 65 million firms leverage online brand communities to connect with customers and achieve known performance benefits, such as increased online reputation, brand patronage, and customer spending (Baker, Donthu, and Kumar 2016; Hollenbeck 2018, Kumar et al. 2016). However, online communities also engender significant risks of online firestorms—that is, negative electronic word of mouth (eWOM) that receives substantial support from other customers in a short period of time (Pfeffer, Zorbach, and Carley 2014). Similar to prominent online firestorm examples, such as #deleteUber and United Airlines' passenger removal incidents, less publicized negative eWOM messages by dissatisfied customers also can go viral; a single 466-word Facebook post by a disgruntled customer in Odeon Cinemas' Facebook brand community prompted more than 94,000 likes, damaging the firm's reputation and causing it to lose thousands of customers (Dunphy 2012).

Detecting, preventing, and mitigating this virality of negative eWOM in online brand communities therefore constitutes a critical managerial priority (Hewett et al. 2016), yet 72% of firms rate their preparedness for online firestorms as "below average" (Ethical Corporation 2012). Managers seem to have a limited understanding of how to respond to negative eWOM describing dissatisfactory consumption experiences (Wang and Chaudhry 2018), nor do they know how to predict the evolution of negative eWOM messages or address angered mass audiences exposed to such negative eWOM. Lacking clear guidelines, firms continue to suffer damages from negative eWOM. We aim to address this gap by identifying sources of firestorms and detailing appropriate sequences for firm responses to negative viral content.

---

## Conceptual Foundations and Hypotheses

### Detecting Potential Online Firestorms

Conventional wisdom suggests that customers in online brand communities first read about the cause of negative eWOM messages and then decide whether to approve and share them. However, faced with the information overload that tends to characterize communication exchanges on social media platforms, customers might not elaborate in detail on the arguments and instead could resort to heuristic processing (Hatfield et al. 2014).

#### H1: High-Arousal vs Low-Arousal Emotions

For example, particularly expressive people seem to transmit emotions effectively (Barsade 2002). Although emotions are not verbal properties, the verbal use of emotional words makes them relatively accessible and contagious. At a granular, word-use level, increasing the number of negative emotion words in eWOM translates directly into stronger behavioral responses by message recipients (Ludwig et al. 2013).

**H1:** The intensity of high-arousal emotion words in negative eWOM messages relates to greater virality in online brand communities compared with the intensity of low-arousal emotion words.

#### H2: Strength of Structural Ties

The decision to approve or share eWOM also depends on the relationship and relational cues between the sender and receiver (Berger and Schwartz 2011). Strong ties reflect members of a community who interact frequently with each other.

**H2:** Stronger structural ties between the sender of negative eWOM and the receiving online brand community relate to greater virality.

#### H3: Linguistic Style Matching (LSM)

In addition, perceived similarity (or homophily perceptions; Brown and Reingen 1987) between the sender and customers in online brand communities may relate to the virality of negative eWOM messages. The similar use of function words—or LSM between two or more conversation partners—represents a form of psychological synchrony that elicits perceptions of similarity, approval, and trust in receivers.

**H3:** Closer LSM between the sender of negative eWOM and the receiving online brand community relates to greater virality.

### Preventing Potential Online Firestorms

A disengaging approach to emotion regulation implies reacting in ways to avoid or block elaboration, rather than preparing an adaptive response (Sheppes et al. 2011). Firms might try to halt an ongoing public online conversation by suggesting a communication channel change.

Active engagement with negative eWOM messages might be more appropriate (Wang and Chaudhry 2018). Service recovery literature has outlined two primary response approaches: empathic or explanatory.

**H4:** More explanation, rather than more empathy, in firm responses is better suited to contain negative eWOM with more intensive high-arousal emotions.

**H5:** More empathy, rather than more explanation, in firm responses is better suited to contain negative eWOM with more intensive low-arousal emotions.

### Mitigating Evolved Online Firestorms

Through observational learning processes, as an online firestorm evolves, and other members support the negative eWOM, its perceived reliability should increase (Dholakia, Basuroy, and Soltysinski 2002).

**H6:** Consecutive firm responses with varying rather than repeated (a) empathic intensity and (b) explanatory intensity are better suited to mitigating evolved online firestorms.

---

## Methods

### Sampling Frame

We used Facebook's Application Programming Interface (API) and processed detailed information on potential online firestorms from the official Facebook brand communities of all U.S. firms listed on the S&P 500 between October 1, 2011 and January 31, 2016.

**Final Sample:** 472,995 negative customer posts in English across 89 online brand communities.

**Post Characteristics:**
- Average length: 99 words (SD = 121.44, range: 3-8,121 words)
- Average likes/comments: 2.95 (SD = 59.22, range: 1-37,760)
- 78% emerged and dissolved within 24 hours
- 93% of firm responses arrived within one hour

### Key Measures

**Virality:** Combined sum of likes and comments the post receives from other customers (brand community-centered, log-transformed).

**Intensity of High Arousal:** LIWC dictionaries "anx" (fear/anxiety), "anger", and new "disgust" dictionary.

**Intensity of Low Arousal:** LIWC dictionary "sad" (sadness).

**Strength of Structural Ties (SST):**
```
SST_ic = Σ(Received Likes + Received Comments + Received Shares + Likes Given + Comments Given)
```

**Linguistic Style Match (LSM):**
```
LSM_jic = 1 - |FW_ji - FW_jic| / (FW_ji + FW_jic + 0.0001)
```

---

## Results

### Detecting Potential Online Firestorms (Table 2)

| Predictor | Coefficient (γ) | Effect Size (r) | Significance |
|-----------|-----------------|-----------------|--------------|
| **Intensity of high arousal (H1)** | 0.186 | 0.07 | p < .01 |
| **Intensity of low arousal (H1)** | 0.026 | 0.01 | p < .01 |
| **Strength of structural ties (H2)** | 1.432 | 0.13 | p < .01 |
| **LSM (H3)** | 0.025 | 0.04 | p < .01 |
| No firm response | 0.029 | 0.14 | p < .01 |
| Average tie strengths | -0.247 | — | p < .05 |
| Variance in linguistic style | 5.550 | — | p < .10 |

**Key Finding:** High-arousal emotions drive virality significantly more than low-arousal emotions (t = 35.15, p < .01). **H1 supported.**

**Key Finding:** Structural tie strength has the LARGEST effect on virality (all t ≥ 77.97, p < .01). **H2 supported.**

### Preventing Potential Online Firestorms (Table 3)

| Firm Response | Effect on Virality | Significance |
|---------------|-------------------|--------------|
| **Intensity of empathy** | -0.069 | p < .01 |
| **Intensity of explanation** | -0.011 | p < .01 |
| Apology | -0.004 | p < .01 |
| Channel change | -0.005 | p < .01 |
| Compensation | +0.003 | p < .01 (BACKFIRE) |

**Interaction Effects:**

| Interaction | Coefficient | Interpretation |
|-------------|-------------|----------------|
| High arousal × Empathy | +2.678*** | Empathy INCREASES virality for high-arousal |
| High arousal × Explanation | -1.437*** | Explanation DECREASES virality for high-arousal |
| Low arousal × Empathy | +0.042 (NS) | No significant interaction |
| Low arousal × Explanation | -0.206*** | Explanation helps for low-arousal too |

**SURPRISING FINDING:** For high-arousal crises, **Explanation > Empathy**. **H4 supported, H5 not supported.**

### Mitigating Evolved Online Firestorms (Table 4)

Sample: 15,762 negative posts with above-average virality and multiple firm responses.

| Response Strategy | First Response | Subsequent Responses |
|-------------------|----------------|---------------------|
| Compensation | +0.017 (NS) | **-0.045*** (GOOD) |
| Apology | +0.012** | **+0.031*** (BACKFIRE) |
| Channel change | +0.010* | **+0.038*** (BACKFIRE) |
| Empathy | +0.072 (NS) | +0.021 (NS) |
| Explanation | **+0.127*** | **+0.083*** |

**Cross-Response Variation:**

| Strategy | Effect on Virality | Significance |
|----------|-------------------|--------------|
| **Variance in empathy (H6a)** | -0.185 | p < .05 |
| **Variance in explanation (H6b)** | -0.205 | p < .01 |

**Key Finding:** Varying response approaches reduces virality. **H6a and H6b supported.**

---

## Summary of Hypotheses Results

| Hypothesis | Effect | Support |
|------------|--------|---------|
| H1 | High arousal > Low arousal for virality | **Supported** |
| H2 | Strong ties > Weak ties for virality | **Supported** |
| H3 | Closer LSM > Distant LSM for virality | **Supported** |
| H4 | For high arousal: Explanation > Empathy | **Supported** |
| H5 | For low arousal: Empathy > Explanation | **Not supported** |
| H6a | Variation in empathy reduces virality | **Supported** |
| H6b | Variation in explanation reduces virality | **Supported** |

---

## Key Managerial Implications

### Detecting Potential Online Firestorms

1. **Monitor arousal, not just sentiment** - High-arousal emotions predict virality regardless of valence
2. **Track structural ties** - Customers with strong community ties are more dangerous complainers
3. **Assess linguistic style matching** - Posts matching community style spread faster

### Preventing Potential Online Firestorms

1. **Never ignore** - Not responding is the worst choice
2. **Respond fast** - 93% of responses arrive within one hour in our sample
3. **Match strategy to arousal:**
   - Low-arousal: Generally use empathy
   - High-arousal: Use explanation
4. **Avoid immediate compensation** - It backfires (signals guilt)

### Mitigating Evolved Online Firestorms

1. **Vary your responses** - Don't repeat the same message
2. **Sequence matters:**
   - First response: Explanation (for high-arousal)
   - Later responses: Increase empathy
3. **Timing-dependent strategies:**
   - Compensation: **Late = good**, Early = bad
   - Apology: **Early = good**, Late = bad
   - Channel change: **Early = good**, Late = bad

---

## COUNTERINTUITIVE FINDINGS

### 1. Explanation > Empathy for High-Arousal Crises

Common wisdom suggests empathy is always best. **WRONG.** For high-arousal emotions (anger, fear, excitement), customers need cognitive reappraisal through explanation, not just emotional validation.

### 2. Early Compensation Backfires

Offering compensation immediately **increases virality** (β = +0.098***). It signals admission of guilt. Wait until later stages to offer compensation (β = -0.058*** when late).

### 3. Structural Ties > Emotional Content

Tie strength (β = 1.432***) has a **much larger effect** on virality than emotional content (β = 0.186***). Well-connected complainers are more dangerous than angry ones.

### 4. Late Apology is Worse Than No Apology

Early apology reduces virality (β = -0.058***), but late apology **increases** virality (β = +0.105***). It seems insincere.

---

## EBF Integration

### Theory Catalog

- **Category:** CAT-24 (Crisis Management & Online Communication)
- **Theory:** MS-CM-001 (Firestorm Detection-Prevention-Mitigation Model)

### Parameter Registry

| ID | Symbol | Value | Description |
|----|--------|-------|-------------|
| PAR-CM-001 | β_arousal_high | 0.186*** | High-arousal emotion virality coefficient |
| PAR-CM-002 | β_tie_strength | 1.432*** | Structural tie virality amplifier |
| PAR-CM-003 | β_empathy | -0.069*** | Empathy response effectiveness |
| PAR-CM-004 | β_explanation | -0.011 (NS) | Explanation direct effect (interaction matters) |
| PAR-CM-005 | β_compensation | Early: +0.098***, Late: -0.058*** | Compensation timing effect |
| PAR-CM-006 | β_apology | Early: -0.058***, Late: +0.105*** | Apology timing effect |
| PAR-CM-007 | β_channel | Early: -0.081***, Late: +0.096*** | Channel change timing effect |

### Case Registry

- **Case:** CAS-907 (Online Firestorm Detection, Prevention, and Mitigation)

### 10C Dimension Mapping

| Dimension | Application |
|-----------|-------------|
| **WHO** | Brands, customers, community members (complainers, bystanders, advocates) |
| **WHAT** | Emotional arousal (high vs low), response strategy utility |
| **HOW** | Timing × Strategy interaction; Empathy × Arousal interaction |
| **WHEN** | 3-phase temporal: Detecting → Preventing → Mitigating |
| **WHERE** | Field data from 89 brand communities, N = 472,995 posts |
| **AWARE** | High-arousal = high salience; monitor arousal not just sentiment |
| **READY** | Organizational crisis preparedness |
| **STAGE** | 3-phase crisis journey; maps to BCJ phases |
| **HIERARCHY** | Brand-community-customer multi-level response |
| **EIT** | Phase-specific interventions |

---

## Citation

```bibtex
@article{PAP-herhausen2019firestorms,
  title={Detecting, Preventing, and Mitigating Online Firestorms in Brand Communities},
  author={Herhausen, Dennis and Ludwig, Stephan and Grewal, Dhruv and
          Wulf, Jochen and Schoegel, Marcus},
  journal={Journal of Marketing},
  volume={83},
  number={3},
  pages={1--21},
  year={2019},
  doi={10.1177/0022242918822300},
  publisher={American Marketing Association}
}
```

---

*Source: VU Research Portal (Article 25fa Dutch Copyright Act)*
*Archived: 2026-02-05*
*Content Level: L3 (Full paper text)*
*Integration Level: I5 (FULL)*
