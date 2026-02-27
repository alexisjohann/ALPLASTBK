---
name: New Appendix
about: Template for creating a new EBF appendix
title: "[APPENDIX] [CATEGORY]-[NAME]: [Title]"
labels: documentation
assignees: ''

---

## Appendix Proposal

### Basic Information

| Field | Value |
|-------|-------|
| **Code** | (e.g., `AW`) |
| **Category** | (see below) |
| **Name** | (e.g., `DOMAIN-NEWFIELD`) |
| **Title** | (e.g., `Behavioral Finance Applications`) |
| **Primary Chapter** | (e.g., `Chapter 10`) |

### Category Selection

Select ONE category (see [appendix-category-definitions.md](/docs/frameworks/appendix-category-definitions.md)):

- [ ] `CORE-` — Answers one of 10C fundamental questions
- [ ] `FORMAL-` — Mathematical proofs and derivations
- [ ] `DOMAIN-` — Application to economics subfield
- [ ] `CONTEXT-` — Detailed Ψ-dimension analysis
- [ ] `METHOD-` — Estimation/measurement methodology
- [ ] `PREDICT-` — Falsifiable predictions
- [ ] `LIT-` — Literature integration by author
- [ ] `REF-` — Reference materials (glossary, examples)

### Fundamental Question

> What question does this appendix answer?

[Your answer here]

### Justification

> Why is this appendix needed? What gap does it fill?

[Your answer here]

### Dependencies

#### Requires (what this appendix needs):
- [ ] Appendix ___: ___
- [ ] Appendix ___: ___

#### Required by (what will use this appendix):
- [ ] Appendix ___: ___
- [ ] Chapter ___: ___

### Proposed Structure

```
[CODE] [CATEGORY]-[NAME]: [Title]
├── 1. The Fundamental Question
├── 2. Core Theory
├── 3. [Specific sections...]
├── 4. Worked Example
├── 5. Integration with Other Appendices
├── 6. Summary
├── 7. Glossary of Symbols
└── 8. References
```

### Key Formulas (if applicable)

```latex
[Key equation 1]
[Key equation 2]
```

### Estimated Scope

| Metric | Estimate |
|--------|----------|
| Pages | ~___ |
| Axioms | ~___ |
| References | ~___ |
| Worked Examples | ___ |

---

## Checklist before submission

- [ ] I have read [appendix-category-definitions.md](/docs/frameworks/appendix-category-definitions.md)
- [ ] I have verified this appendix doesn't duplicate existing content
- [ ] I have identified all dependencies
- [ ] The category selection is appropriate

---

## For CORE appendices only

If proposing a CORE appendix, additional requirements apply:

- [ ] Answers exactly ONE of the 10C questions
- [ ] Will include complete axiom system (8-200 axioms)
- [ ] Will include 80-150+ references
- [ ] Will include 5-10 critical foundations
- [ ] Will integrate bidirectionally with ALL other COREs
- [ ] Will include 20+ symbol definitions

---

*Reference: [00_appendix_template.tex](/appendices/00_appendix_template.tex)*
