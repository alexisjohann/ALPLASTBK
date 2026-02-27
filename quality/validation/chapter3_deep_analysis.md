# Chapter 3: Limits of Utility Maximization - Deep Quality Analysis

**Version:** v46  
**Date:** 2025-01-03  
**Lines:** 318

---

## 1. INHALTLICHE KOHÄRENZ

### Logical Flow Assessment

```
Stable Preferences Assumption
    ↓ What it claims + Why economists use it
Stigler-Becker Defense
    ↓ Addiction example - saves stability but unfalsifiable
Five Domains Where It Fails
    ↓ Social Preferences (ultimatum, dictator, public goods, trust)
    ↓ Identity (moral wiggle room)
    ↓ Reference Dependence (endowment effect)
    ↓ Framing (organ donation defaults)
    ↓ Preference Construction (contingent valuation)
The Deeper Problem
    ↓ Three types of interdependence
What Maximization Gets Wrong
    ↓ Not wrong, but incomplete
The Required Extension
    ↓ From optimization to coherence
```

**Assessment:** ✅ Excellent structure. Each domain builds case, then synthesizes.

---

## 2. CLAIM-EVIDENCE MATCHING

### Section: Stable Preferences
| Claim | Evidence | Status |
|-------|----------|--------|
| Stigler-Becker defense | citet{stiglerbecker1977} | ✅ |
| "De gustibus" quote | stiglerbecker1977 | ✅ |

### Section: Domain 1 - Social Preferences
| Claim | Evidence | Status |
|-------|----------|--------|
| Ultimatum game results | General knowledge | ⚠️ Could cite Güth |
| Modal offer $4-5 | Empirical fact | ✅ |
| Offers below $2 rejected | Empirical fact | ✅ |

### Section: Domain 2 - Identity
| Claim | Evidence | Status |
|-------|----------|--------|
| Moral wiggle room | citet{danaberton2007} | ✅ |
| Chose ignorance then A | danaberton2007 | ✅ |

### Section: Domain 3 - Reference Dependence
| Claim | Evidence | Status |
|-------|----------|--------|
| Prospect theory | citet{kahnemantversky1979} | ✅ |
| λ ≈ 2 | kahnemantversky1979 | ✅ |
| Endowment effect | citet{knetschetal1990} | ✅ |
| WTT < 50% | knetschetal1990 | ✅ |

### Section: Domain 4 - Framing
| Claim | Evidence | Status |
|-------|----------|--------|
| Organ donation rates | citet{johnsonetal2003} | ✅ |
| Germany 12% vs Austria 99% | johnsonetal2003 | ✅ |

### Section: Domain 5 - Preference Construction
| Claim | Evidence | Status |
|-------|----------|--------|
| Contingent valuation issues | General knowledge | ⚠️ No citation |

---

## 3. FIVE DOMAINS STRUCTURE ✅

| Domain | Key Experiment | Citation | Framework Link |
|--------|---------------|----------|----------------|
| Social Preferences | Ultimatum Game | (guth1982 in Ch1) | $C_{ij} \neq 0$ |
| Identity | Moral Wiggle Room | danaberton2007 ✅ | $U^{IDN}$ |
| Reference Dependence | Endowment Effect | knetschetal1990 ✅ | $r = r(\Psi)$ |
| Framing | Organ Donation | johnsonetal2003 ✅ | $Choice(\Psi)$ |
| Preference Construction | Contingent Valuation | — | $U = f(construction)$ |

---

## 4. MATHEMATICAL NOTATION ✅

| Equation | Purpose | Correct? |
|----------|---------|----------|
| $U_i(x, t) = U_i(x)$ | Stable preferences | ✅ |
| $\partial^2 U_i / \partial x_i \partial x_j \neq 0$ | Complementarity | ✅ |
| $v(x) = x^\alpha$ or $-\lambda(-x)^\beta$ | Prospect theory | ✅ |
| $\lambda \approx 2$ | Loss aversion | ✅ |
| $U = U(x - r(\Psi))$ | Reference dependence | ✅ |
| $C_{ij} = C_{ij}(\Psi)$ | Context-dependent complementarity | ✅ |

---

## 5. TRANSITIONS

### From Chapter 2
**Ch2 ends:** "A complete theory... must include: Utility interdependence ($C_{ij} \neq 0$)"
**Ch3 starts:** "The classical framework assumes stable preferences..."

**Assessment:** ✅ Good implicit connection - Ch2 said what's needed, Ch3 provides evidence

### To Chapter 4
**Ch3 ends:** "This is what the following sections develop."
**Ch4 is:** "Empirical Foundations"

**Assessment:** ✅ Ch3 = theoretical limits, Ch4 = empirical evidence

---

## 6. POTENTIAL ISSUES

### Issue 1: Ultimatum Game Citation
**Location:** Domain 1: Social Preferences
**Claim:** "Proposer divides $10... Modal offer is $4-5"
**Missing:** Direct citation for ultimatum game results
**Note:** guth1982 is cited in Chapter 1 but not here
**Severity:** Low - well-known result, cited elsewhere
**Recommendation:** Optional - add "as shown by \citet{guth1982}"

### Issue 2: Contingent Valuation Citation
**Location:** Domain 5: Preference Construction
**Claim:** "WTP varies wildly depending on..."
**Missing:** Citation for contingent valuation problems
**Severity:** Low - general methodological knowledge
**Recommendation:** Optional - could cite kahneman/knetsch work

### Issue 3: Reference to Appendix A
**Location:** First paragraph
**Text:** "Formal derivations... appear in Appendix~A"
**Status:** ✅ Reference exists and correct

---

## 7. STRENGTHS

1. **Comprehensive coverage** - All five major behavioral domains
2. **Clear examples** - Each domain has concrete illustration
3. **Mathematical precision** - Equations for each phenomenon
4. **Framework integration** - Every domain connects to $C_{ij}$ or $\Psi$
5. **Honest about limitations** - "Not wrong, but incomplete"
6. **Strong synthesis** - "Three Types of Interdependence" section

---

## 8. NOTABLE FEATURES

### The "Three Types of Interdependence" Section
Excellent synthesis:
- Cross-agent: $\partial U_i / \partial x_j \neq 0$
- Temporal: $\partial U_t / \partial a_{t-1} \neq 0$
- Context: $\partial U / \partial \Psi \neq 0$

This unifies all five domains into the framework's core structure.

### The "Not Wrong, But Incomplete" Argument
Strong philosophical positioning:
- Acknowledges utility maximization's validity
- Shows it's underdetermined when utilities are interdependent
- Motivates coherence criterion without dismissing optimization

---

## 9. RECOMMENDATIONS

| Priority | Issue | Action |
|----------|-------|--------|
| LOW | Ultimatum citation | Optional: add guth1982 reference in Domain 1 |
| LOW | Contingent valuation | Optional: could cite Kahneman/Knetsch |
| NONE | Structure | Excellent as-is |

---

## SUMMARY

| Check | Status |
|-------|--------|
| Logical Flow | ✅ Excellent |
| Claim-Evidence | ✅ Good (5 key citations present) |
| Five Domains | ✅ Comprehensive |
| Math Notation | ✅ Correct |
| Framework Links | ✅ Every domain connected |
| Transitions | ✅ Good |

**Overall:** ✅ HIGH QUALITY - No fixes required

---

## NOTE ON CHAPTER DESIGN

Chapter 3 is deliberately **theoretical** - it explains WHY stable preferences fail.
Chapter 4 provides **empirical** evidence from experiments and neuroscience.
This is a clean, appropriate division.

The existing citations (stiglerbecker1977, danaberton2007, kahnemantversky1979, knetschetal1990, johnsonetal2003) cover the key claims adequately.

