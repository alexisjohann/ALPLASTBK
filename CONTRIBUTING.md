# Contributing to the EBF Framework

Thank you for your interest in contributing to the Evidence-Based Framework for Economic and Social Behavior (EBF)! This document explains how to get started.

---

## 🚀 Quick Start for Contributors

### Step 1: Understand the Framework
- Read: `docs/EBF-INTRODUCTION.md` (10 minutes overview)
- Read: `ROADMAP.md` (understand where we are)
- Read: `FUTURE_WORK.md` (understand what's next)

### Step 2: Choose a Task
We have three main development options. Pick one:

1. **OPTION A: System Dynamics** (Theoretical completeness)
   - Effort: ~100 hours
   - Priority: #3 (Long-term)
   - For: Researchers, mathematicians
   - See: `FUTURE_WORK.md` Section A

2. **OPTION B: Agent-Based Modeling** (Impact assessment)
   - Effort: ~140 hours
   - Priority: #2 (Medium-term)
   - For: Policy researchers, data scientists
   - See: `FUTURE_WORK.md` Section B

3. **OPTION C: Online-Adaptive Portfolio** (Real-world implementation) ⭐ **START HERE**
   - Effort: ~120 hours
   - Priority: #1 (Immediate)
   - For: Software engineers, practitioners
   - See: `FUTURE_WORK.md` Section C

### Step 3: Create an Issue
Before you start coding:

1. Go to **GitHub Issues**
2. Create issue with title: `[OPTION-A|B|C] Component Name`
3. Reference the relevant section in `FUTURE_WORK.md`
4. Discuss approach with maintainers (we'll comment on the issue)
5. Wait for approval before coding

**Example:**
```
Title: [OPTION-C] Bayesian Parameter Update Module

I want to implement the Thompson sampling update function for
online portfolio optimization. See FUTURE_WORK.md Section C.1.

Proposed approach:
- Conjugate normal-gamma model for effectiveness parameters
- scipy.stats.norm for sampling
- Weekly update cadence

Estimated effort: 20-30 hours

Any feedback?
```

### Step 4: Fork, Branch, Commit

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/complementarity-context-framework.git
cd complementarity-context-framework

# Create a feature branch
git checkout -b feature/OPTION-[A|B|C]-component-name

# Example:
git checkout -b feature/OPTION-C-bayesian-update
```

### Step 5: Code & Test

Follow these guidelines:

#### Python Code
```python
# Style: PEP 8
# Testing: pytest
# Coverage: Aim for 80%+

# Example structure:
def update_theta_beliefs(theta_mean, theta_std, observations):
    """
    Bayesian update of intervention effectiveness parameters.

    Args:
        theta_mean: Prior mean of effectiveness (n_dimensions,)
        theta_std: Prior std of effectiveness (n_dimensions,)
        observations: Dict with {'AWARE': {'n': 500, 'effect': 0.095}, ...}

    Returns:
        theta_mean_updated: Posterior mean
        theta_std_updated: Posterior std
    """
    # Implementation...
    return theta_mean_updated, theta_std_updated


# Test:
def test_update_theta_beliefs():
    theta_mean = np.array([0.10, 0.12, 0.08])
    theta_std = np.array([0.05, 0.05, 0.05])
    obs = {'AWARE': {'n': 100, 'effect': 0.095}}

    mean_out, std_out = update_theta_beliefs(theta_mean, theta_std, obs)

    assert mean_out[0] > theta_mean[0]  # Mean should shift toward observation
    assert std_out[0] < theta_std[0]    # Uncertainty should decrease
```

#### LaTeX Chapters/Appendices
```latex
% CHAPTER XX: My New Chapter
% Version: 1.0 (2026-01-21)
% Purpose: [Clear description]
% Type: [A/B/C - Foundation/Core/Application]

\chapter{My New Chapter}
\label{ch:my-chapter}

% Include Quick Reference Box
\begin{tcolorbox}[colback=blue!5!white, colframe=blue!75!black,
                  title=Key Concepts]
\small
\begin{tabular}{@{}ll@{}}
\textbf{Term} & \textbf{Definition} \\
\midrule
Concept 1 & Explanation \\
\end{tabular}
\end{tcolorbox}

% Include Appendix References Box
\begin{tcolorbox}[colback=yellow!10!white, colframe=orange!75!black,
                  title=Appendix References]
\textbf{Essential:}
\begin{itemize}[nosep]
\item Appendix XXX (CATEGORY-NAME) --- Description
\end{itemize}
\end{tcolorbox}

% Then your content...
```

### Step 6: Document Everything

**For Python modules:**
```python
# requirements.txt - add dependencies
scipy>=1.7
numpy>=1.20
pymc3>=3.11  # For OPTION C

# Add docstrings to every function
# Add type hints (Python 3.7+)
# Add unit tests in tests/test_yourmodule.py
```

**For LaTeX chapters:**
- Use `\label{}` for all sections and equations
- Cross-reference existing appendices with `\ref{}`
- Include worked examples with real numbers
- End with "Reading Paths" box pointing to next chapter

### Step 7: Validate Against Test Cases

Every option has test cases in `FUTURE_WORK.md`:

**For OPTION C (Online-Adaptive Portfolio):**

```python
# Run test cases from FUTURE_WORK.md Section C.3

def test_diabetes_case():
    """Validate against Diabetes case study from Ch21"""
    model = OnlinePortfolio()

    # Week 1-4: Baseline data
    model.update_beliefs(1, {
        'AWARE': {'n': 500, 'effect': 0.095},
        'READY': {'n': 450, 'effect': 0.132},
        'WHO_others': {'n': 380, 'effect': 0.115},
    })

    # Should converge to known effectiveness values
    assert np.isclose(model.theta_mean[AWARE_idx], 0.095, atol=0.02)
    assert np.isclose(model.theta_mean[READY_idx], 0.132, atol=0.02)

def test_tipping_point():
    """Validate tipping point detection"""
    # Varying WHO_others intensity should show nonlinear response
    # See FUTURE_WORK.md Test Case 2
    ...

def test_robustness_to_noise():
    """Validate robustness with ±5% observation noise"""
    # Add noise; verify convergence still works
    # See FUTURE_WORK.md Test Case 3
    ...
```

Run all tests:
```bash
pytest tests/ -v --cov=ebf_framework --cov-report=html
```

### Step 8: Submit Pull Request

```bash
# Push to your fork
git push origin feature/OPTION-C-bayesian-update

# Create PR on GitHub
# Title: feat(OPTION-C): Implement Bayesian parameter update
# Description: Reference the issue (#123)
# Include:
#   - Summary of changes
#   - Link to issue
#   - Test results
#   - Screenshots (if applicable)
```

**PR Template:**
```markdown
## Description
Brief summary of what you implemented.

Fixes #[issue number]

## Type of Change
- [ ] New feature (OPTION A/B/C component)
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests passing (pytest)
- [ ] Coverage >80%
- [ ] Test cases from FUTURE_WORK.md passing
- [ ] Code review checklist complete

## Checklist
- [ ] Code follows PEP 8 (Python) or LaTeX style guide
- [ ] Documentation updated
- [ ] All tests pass locally
- [ ] No new warnings generated
```

### Step 9: Respond to Feedback

Maintainers will review your PR. Be prepared to:
- Answer questions about design decisions
- Make requested changes
- Add additional tests
- Optimize performance

---

## 📋 Code Style & Standards

### Python
```bash
# Format code with Black
black ebf_framework/

# Lint with flake8
flake8 ebf_framework/ --max-line-length=100

# Type check with mypy
mypy ebf_framework/

# Test with pytest
pytest tests/ -v
```

### LaTeX
- Max line length: 80 characters
- Use `\label{sec:descriptive-name}` for all sections
- Use `\ref{}` to cross-reference
- Equations: Use `equation` environment with labels
- Figures: Use `figure` environment with captions

---

## 🧪 Testing Requirements

### Python Modules
- **Unit tests:** Test individual functions in isolation
- **Integration tests:** Test components working together
- **Validation tests:** Test against known case studies
- **Coverage:** Aim for 80%+ code coverage

Example test structure:
```
tests/
├── test_bayesian.py          # Unit tests for Bayesian module
├── test_portfolio.py         # Unit tests for portfolio optimization
├── test_integration.py       # Integration between modules
└── test_validation_diabetes.py  # Validation against Diabetes case
```

### LaTeX Chapters
- **Compilation:** `latexmk -pdf chapters/XX_myfile.tex` succeeds
- **Cross-references:** All `\ref{}` resolve correctly
- **Appendix references:** Point to existing appendices
- **Worked examples:** Have realistic numbers

---

## 📚 Documentation Standards

Every new component must include:

### Python
```python
def my_function(param1: float, param2: np.ndarray) -> Tuple[float, float]:
    """
    Brief one-line description.

    Longer description explaining the algorithm, assumptions,
    and practical use case.

    Args:
        param1: Description and units/range
        param2: Description and shape

    Returns:
        result1: Description and interpretation
        result2: Description and interpretation

    Raises:
        ValueError: When input validation fails

    Examples:
        >>> result = my_function(0.5, np.array([1, 2, 3]))
        >>> print(result)
        (0.8, array([...]))

    References:
        - Ch22, Section 3: Overview
        - FUTURE_WORK.md, Section C.1: Technical details
    """
    # Implementation...
```

### LaTeX
```latex
\section{My New Section}
\label{sec:my-section}

\textbf{Definition:} What is this concept?

\textbf{Interpretation:} How do practitioners use it?

\textbf{Example:} Concrete numerical case

See Appendix XXX for detailed theory; Ch22 for policy applications.
```

---

## 🚦 Status Checks Before PR

**Checklist before submitting:**

```
Code Quality
- [ ] Black formatting applied (python)
- [ ] Flake8 linting passes
- [ ] Type hints added (mypy clean)
- [ ] 80%+ test coverage
- [ ] No hardcoded paths (use relative paths)

Testing
- [ ] Unit tests pass (pytest)
- [ ] Integration tests pass
- [ ] Validation against case study passes
- [ ] Edge cases tested (null, extreme values, etc.)

Documentation
- [ ] Docstrings on all functions/classes
- [ ] README updated (if new module)
- [ ] Changelog updated
- [ ] Cross-references verified (LaTeX)

Process
- [ ] Issue discussed before coding
- [ ] Branch created from main
- [ ] Commits are atomic (logical grouping)
- [ ] Commit messages are clear
```

---

## 🤝 Code Review Process

1. **Maintainer reviews** your PR (within 1 week)
2. **You respond** to feedback (within 3 days)
3. **Maintainer approves** (when all concerns addressed)
4. **Merge!** 🎉

---

## 📞 Getting Help

**Questions?**
- Check `ROADMAP.md` for overview
- Check `FUTURE_WORK.md` for technical details
- Comment on the GitHub Issue (for discussion)
- Email: [Project maintainer contact]

**Found a bug?**
- Create GitHub Issue with:
  - Description of unexpected behavior
  - Steps to reproduce
  - Expected vs. actual output
  - Python/LaTeX version

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

## Acknowledgments

We appreciate all contributors! Your name will be added to:
- CONTRIBUTORS.md
- Release notes
- Documentation acknowledgments

---

**Happy contributing! 🚀**

Questions? Start an issue or contact the maintainers.

Last updated: 2026-01-21
