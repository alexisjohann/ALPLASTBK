# Key References for Chapter 4.X

## Digital Twins Mega-Study (Peng et al. 2025)

**Full Citation:**
Peng, T., Gui, G., Merlau, D. J., Fan, G. J., Ben Sliman, M., Brucks, M., Johnson, E. J., Morwitz, V., et al. (2025). A Mega-Study of Digital Twins Reveals Strengths, Weaknesses and Opportunities for Further Improvement. *arXiv preprint arXiv:2509.19088*.

**Links:**
- arXiv: https://arxiv.org/abs/2509.19088
- Data: https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500-Mega-Study
- Code: https://github.com/TianyiPeng/Twin-2K-500-Mega-Study

**Key Findings Relevant to EBF:**

1. **Accuracy Paradox**: 75% individual-level accuracy sounds high, but is no better than simple demographic personas

2. **Low Correlation**: r ≈ 0.2 correlation between digital twin and human responses

3. **Under-Dispersion**: Twins cluster around mean, losing heterogeneity

4. **Replication Failures**:
   - Attraction Effect: Not replicated by twins
   - Compromise Effect: Not replicated
   - Default Effect (Organ Donation): Twins show effect, humans don't
   - Default Effect (Green Energy): Humans show effect, twins don't
   - Accuracy Nudges: Effective for twins, not for humans

5. **WEIRD Bias**: Twins more accurate for higher education, higher income, moderate political views

6. **"Idealized Rational Agent" Problem**: Twins show theoretically expected behavior that humans don't exhibit

## BibTeX Entry

```bibtex
@article{peng2025digitaltwins,
  title={A Mega-Study of Digital Twins Reveals Strengths, Weaknesses and 
         Opportunities for Further Improvement},
  author={Peng, Tianyi and Gui, George and Merlau, Daniel J. and Fan, Grace Jiarui 
          and Ben Sliman, Malek and Brucks, Melanie and Johnson, Eric J. and 
          Morwitz, Vicki and Althenayyan, Abdullah and Bellezza, Silvia and 
          Donati, Dante and Fong, Hortense and Friedman, Elizabeth and 
          Guevara, Ariana and Hussein, Mohamed and Jerath, Kinshuk and 
          Kogut, Bruce and Kumar, Akshit and Lane, Kristen and Li, Hannah and 
          Perkowski, Patryk and Netzer, Oded and Toubia, Olivier},
  journal={arXiv preprint arXiv:2509.19088},
  year={2025},
  note={19 preregistered studies, N=2000+ with matched digital twins}
}
```

## Why This Paper Matters for Complementarity & Context

The Peng et al. findings provide the **empirical foil** for the EBF argument:

| Aspect | Digital Twins (LLM-based) | EBF (Data-calibrated) |
|--------|---------------------------|---------------------------|
| Data source | Text corpora | Experimental behavioral data |
| Heterogeneity | Lost (under-dispersion) | Explicitly modeled |
| Classic experiments | ~50% replication | By construction |
| Novel predictions | Not better than chance | Testable, expected high |

**The central claim**: EBF succeeds where digital twins fail because it is calibrated on *behavioral data*, not *text about behavior*.
