# Power Analysis is Essential: High-Powered Tests Suggest Minimal to No Effect of Rounded Shapes on Click-Through Rates

**Authors:** Ron Kohavi, Jakub Linowski, Lukas Vermeer, Fabrice Boisseranc, Joachim Furuseth, Andrew Gelman, Guido Imbens, Ravikiran Rajagopal
**Source:** arXiv preprint (2512.24521)
**Year:** 2026
**URL:** https://arxiv.org/abs/2512.24521
**Part of:** Trustworthy A/B Patterns Project

---

## Abstract

A study by Biswas, Abell, and Chacko published in the Journal of Consumer Research (2023) reported that in an A/B test simply rounding the corners of square buttons increased the online click-through rate by 55% (p-value 0.037), a striking finding with potentially wide-ranging implications for a digital industry that is seeking to enhance consumer engagement.

Given our experience with similar changes, we felt this result was implausible, and this was our first pattern that we replicated as part of the Trustworthy A/B Patterns project. Our four high-powered A/B tests each had over two thousand times as many users than the original study. All experiments yielded effect size estimates that were approximately two orders of magnitude smaller than initially reported, with 95% confidence intervals that include zero.

**Keywords:** A/B testing, replication, power analysis, winner's curse, effect size exaggeration, small telescopes, rounded corners, CTR

---

## The Original Claim

### Biswas, Abell & Chacko (2023)

The original study claimed:

> "In an A/B test simply rounding the corners of square buttons increased the online click-through rate by 55%"

| Study | N Control | N Treatment | CTR Control | CTR Treatment | Lift | p-value |
|-------|-----------|-------------|-------------|---------------|------|---------|
| Study 2 | 445 | 474 | 7.19% | 11.18% | **55.49%** | 0.037 |
| Study 3 | 50 | 54 | 52.00% | 75.93% | 46.01% | 0.011 |
| Study D | 32 | 33 | 21.88% | 45.45% | 107.79% | 0.045 |

### Why We Were Skeptical

1. **Effect size implausibly large:** 55% lift from minor UI change
2. **Small sample sizes:** N < 1,000 for main study
3. **Multiple studies with varying N:** Pattern suggests selective reporting
4. **No pre-registration:** Researcher degrees of freedom
5. **Experience:** Similar changes typically yield <1% effects

---

## The Replication Study

### Four High-Powered A/B Tests

| Site | N Control | N Treatment | Total N | Power vs Original |
|------|-----------|-------------|---------|-------------------|
| SeaWorld Orlando | 1,448,041 | 1,448,066 | 2,896,107 | 3,152x |
| Obs-BYGG | 1,126,132 | 1,124,100 | 2,250,232 | 2,450x |
| Obs | 977,499 | 976,653 | 1,954,152 | 2,127x |
| **Metro Russia** | 3,699,177 | 3,701,231 | **7,400,408** | **8,053x** |
| **TOTAL** | | | **14,500,899** | **~15,000x** |

### Results Summary

| Site | CTR Control | CTR Treatment | Lift | p-value | Significant? |
|------|-------------|---------------|------|---------|--------------|
| SeaWorld Orlando | 47.13% | 47.21% | **+0.16%** | 0.20 | NO |
| Obs-BYGG | 5.43% | 5.45% | **+0.29%** | 0.60 | NO |
| Obs | 10.07% | 10.14% | **+0.73%** | 0.09 | NO |
| Metro Russia | 4.40% | 4.40% | **-0.07%** | 0.83 | NO |

### Key Finding

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ORIGINAL CLAIM vs REPLICATION                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Original (BAC 2023):                                                   │
│  • Claimed lift: +55%                                                   │
│  • Sample size: N = 919                                                 │
│  • p-value: 0.037                                                       │
│                                                                         │
│  Replications (Kohavi et al. 2026):                                     │
│  • Observed lift: ~0% (range: -0.07% to +0.73%)                        │
│  • Sample size: N = 14,500,899 (15,000x larger!)                       │
│  • p-values: 0.09 to 0.83 (ALL non-significant)                        │
│                                                                         │
│  → Effect estimates ~100x SMALLER than originally claimed               │
│  → All 95% CIs include zero                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Metro Russia Replication Details

### Pre-Registration (OSF)

- **Registered:** Aug 4, 2025
- **OSF DOI:** 10.17605/OSF.IO/YK62M
- **Pre-declared runtime:** 16 weeks
- **Pre-declared OEC:** Add-to-cart per user (Boolean)

### Experimental Setup

| Aspect | Specification |
|--------|---------------|
| **Platform** | METRO Russia (metro-cc.ru) |
| **Treatment** | Rounded vs almost-square "Add to Cart" button |
| **Duration** | Sept 4 - Dec 25, 2025 (exactly 16 weeks) |
| **Total Users** | 7,400,408 |
| **Split** | 50/50 randomization |
| **SRM Test** | Passed (p=0.45) |

### Power Analysis

| Metric | MDE (80% power) |
|--------|-----------------|
| Add-to-cart (Boolean) | 1.0% |
| Add-to-cart (Count) | 2.7% |
| Add-to-cart (Capped at 10) | 1.2% |

### Results

| Metric | Lift | p-value | Conclusion |
|--------|------|---------|------------|
| Add-to-cart (Boolean) | -0.07% | 0.83 | Not significant |
| Add-to-cart (Count) | +0.83% | 0.41 | Not significant |
| Add-to-cart (Capped) | +0.35% | 0.41 | Not significant |

---

## Small Telescopes Analysis

### The Methodology (Simonsohn 2015)

> "If a study is too small to detect the true effect, a significant result is more likely to be a false positive than a true positive."

### Application to BAC (2023)

**Question:** Could the original study (N=919) have detected a realistic effect?

**Analysis:**
1. Realistic effect for UI change: ~0.5% lift
2. Original study MDE: ~15-20% lift (at 80% power)
3. Original could NOT detect realistic effect
4. Therefore: Significant finding is likely false positive

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SMALL TELESCOPES VERDICT                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Original N = 919                                                       │
│  Original MDE ≈ 15-20% (for 80% power)                                 │
│  True effect ≈ 0-1% (from replications)                                │
│                                                                         │
│  → Original was UNDERPOWERED by factor of ~2000x                       │
│  → Original could NOT have detected the true (null) effect             │
│  → Significant finding is artifact of winner's curse                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Winner's Curse Explained

### The Mechanism

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WINNER'S CURSE IN A/B TESTING                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. True effect is small or zero                                        │
│                                                                         │
│  2. Underpowered study runs                                             │
│     → Most runs: No significant result (unpublished)                    │
│     → Rare run: Noise pushes estimate high enough for p < 0.05          │
│                                                                         │
│  3. Significant result gets published                                   │
│     → But estimate is inflated (it "won" by being extreme)             │
│                                                                         │
│  4. Effect size exaggeration                                            │
│     → True effect: ~0%                                                  │
│     → Published effect: +55%                                            │
│                                                                         │
│  This is NOT fraud - it's a systematic statistical artifact             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Prevention

1. **Pre-registration:** Commit to analysis plan before data
2. **Power analysis:** Ensure adequate N before running
3. **Replication:** Require independent verification
4. **Smaller effects:** Be suspicious of implausibly large effects

---

## Implications for EBF

### What This Means for Behavioral Economics

1. **Small sample studies:** Treat with skepticism
2. **Large claimed effects:** Require replication
3. **Pre-registration:** Should be standard
4. **Power analysis:** Essential before accepting findings

### Parameter Implications

| Parameter | Original Value | Revised Value | Status |
|-----------|---------------|---------------|--------|
| d_rounded_corners | +55% | ~0% | **REJECTED** |

### Theory Implications

- The original finding does NOT support theories about "curvy" preferences
- Effect size exaggeration is common in small-sample marketing studies
- Replications should be standard before incorporating findings

---

## EBF Integration

### Theory Catalog

- **Category:** METHOD (Experimental Methods, Replication)
- **Theory Support:** MS-ME-001 (Experimental Design)

### Case Registry

- **Case:** CAS-912 (Rounded Corners Replication Failure)

### 10C Dimension Mapping

| Dimension | Application |
|-----------|-------------|
| **WHO** | Kohavi (Microsoft/Airbnb), Gelman (Columbia), Imbens (Nobel 2021) |
| **WHAT** | CTR lift from rounded corners: 55% → 0% |
| **HOW** | 2000x power increase, 100x effect decrease |
| **WHEN** | Pre-registered Aug 2025, ran Sept-Dec 2025 |
| **WHERE** | USA (SeaWorld), Norway (Coop), Russia (Metro) |
| **AWARE** | Small Telescopes: Original couldn't detect true effect |
| **READY** | Pre-registration, SRM tests, MDE calculations |
| **STAGE** | Discovery (original) → Confirmation (replication) |
| **HIERARCHY** | Single study < Pre-registered replication < Multi-site replication |
| **EIT** | Power analysis BEFORE claiming effects; replicate large claims |

---

## Key Takeaways

1. **55% claimed effect → ~0% actual effect** (100x smaller)

2. **N=919 → N=14,500,899** (15,000x more power)

3. **Winner's curse explains the discrepancy** (not fraud)

4. **Small Telescopes:** Original was too small to be informative

5. **Pre-registration + Power analysis = Essential**

6. **Cross-site replication strengthens null finding**

---

## References

- Biswas, D., Abell, A., & Chacko, R. (2023). Curvy Digital Marketing Designs. JCR.
- Kohavi, R. (2025, Aug 4). Rounded Corners Replication at Metro-cc.ru. OSF.
- Simonsohn, U. (2015). Small Telescopes. Psychological Science.
- Open Science Collaboration. (2015). Estimating the Reproducibility of Psychological Science. Science.

---

## Citation

```bibtex
@article{PAP-kohavi2026poweranalysis,
  title={Power Analysis is Essential: High-Powered Tests Suggest Minimal
         to No Effect of Rounded Shapes on Click-Through Rates},
  author={Kohavi, Ron and Linowski, Jakub and Vermeer, Lukas and
          Boisseranc, Fabrice and Furuseth, Joachim and Gelman, Andrew and
          Imbens, Guido and Rajagopal, Ravikiran},
  journal={arXiv preprint},
  year={2026},
  eprint={2512.24521}
}
```

---

*Source: arXiv:2512.24521 + Trustworthy A/B Patterns Project*
*Archived: 2026-02-05*
*Content Level: L3 (Full paper text)*
*Integration Level: I3 (CASE)*
