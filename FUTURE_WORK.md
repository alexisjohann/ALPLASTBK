# Future Work: Technical Specifications

**Document:** Detailed specifications for OPTION A, B, C roadmap items
**Audience:** Developers, researchers, technical contributors
**Status:** Planning phase

---

## OPTION A: System Dynamics (Ch24 + Appendix OOO)

### A.1 Mathematical Formulation

#### Core State Vector (Continuous)
```
S(t) = [L(t), d(t), γ(t), Ψ(t), Θ(t), A(t), W(t), φ(t), ζ(t)]

Where:
  L(t) ∈ {subpopulation levels}                [Discrete, usually constant]
  d(t) = (u_F, u_E, u_P, u_S, u_D, u_E) ∈ ℝ^6 [Utility weights; change slowly]
  γ(t) ∈ ℝ^{6×6}                              [Complementarity matrix; changes with context]
  Ψ(t) ∈ ℝ^8                                  [Context; usually external shock]
  Θ(t) ∈ ℝ^n                                  [Intervention effectiveness params]
  A(t) ∈ [0,1]                                [Awareness; increases with info]
  W(t) ∈ [0,1]                                [Willingness/readiness threshold]
  φ(t) ∈ [0,1]                                [BCJ phase; increases monotonically]
  ζ(t) ∈ ℝ^3                                  [Segment distribution; (PB, SO, AS) proportions]
```

#### Coupled Differential Equations
```
(1) dA/dt = α_A(t) · T_1(t) · (1 - A(t)) - β_A · A(t)
    Interpretation:
    - T_1(t) is information intervention intensity at time t
    - α_A is effectiveness of T_1 on awareness
    - β_A is awareness decay (forgetting)
    - Natural upper bound: dA/dt → 0 as A → 1

(2) dW/dt = f_W(A(t), φ(t), u(t), γ(t)) + Σ_i σ_W^i(t) · T_i(t)
    Where f_W is complex:
    - W increases if A > A_min (must be aware to be willing)
    - W increases faster if already in Triggered phase
    - W depends on utility configuration (easier if Financial not critical)
    - γ_effects: Peer pressure (I_WHO,others) reduces individual willingness (negative γ)

(3) dφ/dt = g_φ(W(t), A(t), Ψ(t), {T_i(t)})
    Where g_φ handles phase progression:
    - φ increases only if W > W_threshold
    - φ increases with urgency (I_WHEN temporal push)
    - φ increases with commitment (I_HOW binding)
    - Rate depends on segment: AS moves faster than PB

(4) dθ_j/dt = λ · (θ̂_obs,j(t) - θ_j(t))  ∀ j ∈ {1..n interventions}
    Bayesian learning: Observed effectiveness θ̂_obs,j(t) updates estimate
    - λ ∈ [0, 1]: Learning rate
    - Typically λ = 0.1-0.3 (slow learning to avoid overfitting noise)

(5) dΨ_k/dt = η_external_k(t) + ρ_k · (Ψ_target_k - Ψ_k(t))  ∀ k ∈ {1..8}
    Context evolution (mostly external):
    - η_external: Policy changes, economic shocks, etc.
    - ρ_k: Mean reversion / persistence parameter
    - Most Ψ_k are exogenous; may have feedback from φ (social acceptance)

(6) dγ_ij/dt = μ_ij · [E_i(t) · E_j(t) · corr_residuals(t) - γ_ij(t)]
    Complementarity learning:
    - μ_ij: Learning rate for interaction terms
    - If residuals of E_i, E_j correlated, γ_ij increases (detected synergy)
    - Usually NOT updated in real-time (estimated from theory)

(7) dζ(t)/dt = Transition Matrix × ζ(t) + Selection Pressure
    Segment dynamics (MISSING from current model!):
    - 3×3 transition matrix: how many PB→SO per month?
    - Depends on portfolio: I_WHO,others (peer) strong PB→SO driver
    - Selection: If SO interventions work better, segment grows
```

#### Key Parameters to Estimate

| Parameter | Interpretation | Typical Range | Sensitivity |
|-----------|-----------------|---------------|------------|
| α_A | Info effectiveness on awareness | 0.001-0.01/week | HIGH |
| β_A | Awareness decay | 0.01-0.05/week | MEDIUM |
| λ_learning | Bayesian update rate | 0.1-0.3 | HIGH |
| ρ_context | Context mean-reversion | 0.02-0.1/week | MEDIUM |
| μ_γ | Complementarity learning | 0.05-0.2 | LOW |
| Segment transition | PB→SO per month | 0.02-0.05 | UNKNOWN |

### A.2 Equilibrium Analysis

#### Fixed Points
```
Find S* where dS/dt = 0:

A* = T_1* / (T_1* + β_A)  [Steady-state awareness given constant T_1]
W* = f_W(A*, φ*, ...)     [Steady-state willingness]
φ* = 1 or φ* < 1 depending on W*, A*

Stability: Compute Jacobian at equilibrium
- If all eigenvalues have Re < 0: Stable (good)
- If any eigenvalue Re > 0: Unstable (runaway)
- If eigenvalue ≈ 0: Bifurcation point
```

#### Bifurcation Analysis
```
For which parameter values does system behavior change qualitatively?

Example: Budget allocation to I_AWARE vs I_WHO,others
- Low I_WHO,others: φ increases slowly (no social pressure)
- Medium I_WHO,others: φ increases faster (peer effects)
- High I_WHO,others: φ increases then plateaus (saturation from backlash)

Identify:
1. Saddle-node bifurcation: Where behavior "jumps"?
2. Hopf bifurcation: Where oscillations emerge?
3. Transcritical: Where equilibria exchange stability?
```

### A.3 Implementation Plan

**Step 1: Parameter Estimation (4-5 weeks)**
- Extract values from Ch20-21 worked examples
- Fit ODEs to Diabetes, Rente, Energia, Engagement timelines
- Estimate {α_A, β_A, λ, ρ, μ_γ, segment transitions}
- Cross-validate on held-out week in each case study

**Step 2: Theory Writing (2-3 weeks)**
- Ch24 (600 lines): Derivation, assumptions, equilibrium theory
- Prove convergence under certain conditions
- Discuss when/why stability breaks down

**Step 3: Code Implementation (2-3 weeks)**
- Python: scipy.integrate.odeint solver
- Input: Parameter vector Θ, intervention schedule T(t), context shocks Ψ(t)
- Output: S(t) trajectories
- Plotting: Phase portraits, bifurcation diagrams

**Step 4: Validation (1-2 weeks)**
- Reproduce known results (4 case studies)
- Sensitivity analysis: How sensitive is φ(t=52 weeks) to α_A?
- Out-of-sample: Predict new domain?

### A.4 Deliverables
- [ ] Ch24 (600 lines, LaTeX)
- [ ] Appendix OOO (400 lines Python + math)
- [ ] 4 Jupyter notebooks with ODEs for each case study
- [ ] Parameter estimation module (open-source)
- [ ] Bifurcation diagrams (publication-ready figures)

---

## OPTION B: Agent-Based Modeling (Ch24b + Appendix PPP)

### B.1 Agent Architecture

```python
class Agent:
    def __init__(self, segment: str, phi_0: float, A_0: float, W_0: float):
        # Identity
        self.id = unique_id
        self.segment = segment  # "PB", "SO", "AS"

        # State variables
        self.phi = phi_0        # Phase ∈ [0, 1]
        self.A = A_0            # Awareness ∈ [0, 1]
        self.W = W_0            # Willingness ∈ [0, 1]
        self.u = {...}          # Utilities (FEPSDE)
        self.gamma = {...}      # Personal complementarities
        self.psi = {...}        # Personal context perception (noisy Ψ)

        # History
        self.history = {
            'phi': [phi_0],
            'A': [A_0],
            'W': [W_0],
            'segment': [segment]
        }

    def step(self, week: int, portfolio: dict, context: Psi, peers: list):
        """
        Update state based on:
        - Portfolio interventions this week
        - Context (external shocks)
        - Peer influence (social network)
        """

        # 1. Receive interventions
        for dimension, intensity in portfolio.items():
            # AWARE: Information (increase A)
            if dimension == "AWARE":
                self.A += intensity * (1 - self.A)  # Logistic growth

            # WHO_others: Peer interaction (influence from neighbors)
            elif dimension == "WHO_others":
                peer_avg_phi = mean([p.phi for p in peers])
                self.phi += intensity * (peer_avg_phi - self.phi)  # Herding

            # ... (handle other dimensions similarly)

        # 2. Check segment transition (did peer effects change me?)
        if self.segment == "PB" and self.phi > threshold:
            self.segment = "SO"  # Transition: Present-Biased → Social-Oriented

        # 3. Update history
        self.history['phi'].append(self.phi)
        self.history['A'].append(self.A)
        self.history['segment'].append(self.segment)

class Model(Model):
    def __init__(self, n_agents: int = 1000, portfolio: dict = None):
        self.schedule = RandomActivation(self)  # Random order each step
        self.agents = []
        self.network = networkx.Graph()  # Social network

        # Create agents with realistic distribution
        for i in range(n_agents):
            segment_draw = np.random.choice(
                ["PB", "SO", "AS"],
                p=[0.4, 0.35, 0.25]  # Observed proportions
            )
            agent = Agent(segment=segment_draw, phi_0=0.2, A_0=0.18, W_0=0.1)
            self.agents.append(agent)
            self.schedule.add(agent)
            self.network.add_node(agent.id)

        # Create social connections (small-world network)
        for agent in self.agents:
            # Connect to 5-10 random peers
            peers = np.random.choice(self.agents, size=7, replace=False)
            for peer in peers:
                self.network.add_edge(agent.id, peer.id)

    def step(self, week: int):
        """Run one week of simulation"""
        # Update each agent
        for agent in self.schedule.agents:
            peers = [self.agents[peer_id] for peer_id in self.network.neighbors(agent.id)]
            agent.step(week, self.portfolio, self.context, peers)

        # Track aggregate outcomes
        self.record_metrics(week)

    def record_metrics(self, week: int):
        """Compute and store population-level statistics"""
        phi_values = [a.phi for a in self.agents]
        segment_counts = Counter([a.segment for a in self.agents])

        self.metrics[week] = {
            'phi_mean': np.mean(phi_values),
            'phi_std': np.std(phi_values),
            'phi_90pct': np.percentile(phi_values, 90),
            'segment_PB': segment_counts['PB'] / len(self.agents),
            'segment_SO': segment_counts['SO'] / len(self.agents),
            'segment_AS': segment_counts['AS'] / len(self.agents),
        }

# Run simulation
model = Model(n_agents=1000, portfolio=health_portfolio)
for week in range(52):  # 52 weeks
    model.step(week)

# Output: Distribution, not just mean!
print(f"Week 52 phase: mean={model.metrics[52]['phi_mean']:.2f}, "
      f"std={model.metrics[52]['phi_std']:.2f}")
```

### B.2 Key Emergent Phenomena to Discover

| Phenomenon | What to look for | Practical implication |
|------------|------------------|----------------------|
| **Tipping point** | When does small change in portfolio → large behavior change? | Budget allocation efficiency |
| **Social cascade** | How fast does behavior spread through network? | Optimal timing of launch |
| **Polarization** | Do subgroups diverge (some action, some refuse)? | Equity risks |
| **Backlash** | Does too-aggressive intervention reduce willingness? | Autonomy risks |
| **Heterogeneity** | How different are outcomes across segments? | Need for targeted messaging |

### B.3 Calibration Strategy

**Data needed:**
- 100-500 agent-level behavioral observations (before/after intervention)
- Social network structure (survey or admin data)
- Baseline segment proportions

**Process:**
1. Run agent-based model with baseline (no intervention)
2. Fit to match observed variance in phase, awareness
3. Add portfolio; tune intervention parameters
4. Validate: Does model φ_t match observed φ_t?
5. If yes: Use model for "what if" scenarios

### B.4 Deliverables
- [ ] Ch24b (700 lines, LaTeX theory)
- [ ] Appendix PPP (500 lines Python, Mesa framework)
- [ ] 4 case studies with fitted agents
- [ ] Tipping point analysis per case
- [ ] Social network visualization tools

---

## OPTION C: Online-Adaptive Portfolio (Ch24c + Appendix QQQ)

### C.1 Bayesian Portfolio Optimization

```python
class OnlinePortfolio:
    def __init__(self, n_interventions: int = 5):
        # Prior: Assume all interventions equally effective
        self.theta_prior = np.ones(n_interventions) * 0.10  # 10% baseline
        self.theta_std = np.ones(n_interventions) * 0.05    # High uncertainty
        self.n_obs = np.zeros(n_interventions)              # Observations per intervention

    def update_beliefs(self, week: int, observations: dict):
        """
        Bayesian update of effectiveness θ_i given observed data

        observations = {
            'AWARE': {'n': 500, 'effect': 0.095},   # 500 people; mean effect 9.5%
            'READY': {'n': 450, 'effect': 0.132},   # 450 people; mean effect 13.2%
            ...
        }
        """
        for dim, obs in observations.items():
            idx = self.dimension_index(dim)

            # Bayesian update (conjugate normal-gamma model)
            n = obs['n']
            y_bar = obs['effect']

            # Update mean
            precision_prior = 1 / self.theta_std[idx]**2
            precision_obs = n / (self.obs_std**2)  # Assume obs noise ~0.02

            self.theta_mean[idx] = (
                precision_prior * self.theta_prior[idx] +
                precision_obs * y_bar
            ) / (precision_prior + precision_obs)

            # Update uncertainty
            self.theta_std[idx] = 1 / np.sqrt(precision_prior + precision_obs)

            # Track observations
            self.n_obs[idx] += n

    def allocate_budget(self, total_budget: float, constraint: dict = None):
        """
        Thompson sampling: Sample from posterior; optimize allocation

        Strategy:
        1. Sample θ_i ~ N(θ_mean, θ_std) for each intervention
        2. Compute portfolio effect E(P) using sampled θ
        3. Choose allocation that maximizes E(P)
        4. Repeat 1000x; average optimal allocation
        """

        allocations = []
        for sample_round in range(1000):
            # 1. Sample from posterior
            theta_sample = np.random.normal(
                loc=self.theta_mean,
                scale=self.theta_std
            )

            # 2. Optimize: argmax_b E(P) s.t. Σ b_i = total_budget
            # Using Lagrangian or linear programming
            b_opt = self.maximize_portfolio(theta_sample, total_budget)
            allocations.append(b_opt)

        # 3. Average over samples
        allocation_mean = np.mean(allocations, axis=0)

        return allocation_mean, self.theta_mean, self.theta_std

    def decide_reallocate(self, week: int) -> bool:
        """
        Decision rule: When to change allocation mid-campaign?

        Criteria:
        1. If any θ_i estimate changed >30% since last reallocation: YES
        2. If total portfolio effect declining trend: YES
        3. If synergy detected (γ_ij changed): YES
        4. Otherwise: NO (stick with plan; avoid thrashing)
        """

        if week == 1:  # First reallocation after 4 weeks
            return False  # Let it run

        # Check change in theta estimates
        theta_change = np.abs(self.theta_mean - self.theta_old) / (self.theta_old + 1e-6)
        if np.max(theta_change) > 0.30:
            return True  # Major change detected

        # Check portfolio trend
        if self.E_recent < self.E_historical * 0.95:
            return True  # Declining effectiveness

        return False

    def recommend_action(self, week: int) -> str:
        """Return actionable recommendation for practitioners"""

        # Identify strongest intervention
        best_idx = np.argmax(self.theta_mean)
        best_T = self.interventions[best_idx]

        # Identify weakest
        worst_idx = np.argmin(self.theta_mean)
        worst_T = self.interventions[worst_idx]

        # Detect synergies
        synergies = self.detect_complementarity()

        recommendation = f"""
        WEEK {week} RECOMMENDATION:

        1. INCREASE budget for {best_T} (estimated effect: {self.theta_mean[best_idx]:.1%})
           - Confidence: {1 - self.theta_std[best_idx]/(self.theta_mean[best_idx]+1e-6):.1%}

        2. CONSIDER reducing {worst_T} (estimated effect: {self.theta_mean[worst_idx]:.1%})
           - Still learning; confidence low

        3. SYNERGIES detected:
           {synergies}

        DECISION: {'REALLOCATE budget' if self.decide_reallocate(week) else 'MAINTAIN current budget'}
        """

        return recommendation
```

### C.2 Implementation Phases

**Phase 1: Preparation (Week -4 to 0)**
- Establish measurement infrastructure
- Define KPIs: What counts as "effect"?
- Setup data pipeline (weekly data collection)

**Phase 2: Baseline (Week 1-4)**
- Run initial portfolio; collect baseline data
- No reallocation yet
- Build priors for θ_i

**Phase 3: Learning (Week 5-48)**
- Weekly Bayesian update
- Biweekly reallocation decisions
- Track recommendations vs. actual changes

**Phase 4: Exploitation (Week 49-52)**
- Shift toward confirmed high-effect interventions
- Minimal exploration

### C.3 Dashboard & Tools

```python
# Streamlit dashboard for practitioners
import streamlit as st

st.title("Online Portfolio Optimization Dashboard")

# Sidebar: Load data
uploaded_file = st.file_uploader("Weekly outcome data (CSV)")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    model = OnlinePortfolio(data)

    # Main display
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Portfolio Effectiveness", f"{model.E_current:.1%}",
                  delta=f"{model.E_change:+.1%p}")

    with col2:
        st.metric("Most Effective Intervention", model.best_T,
                  f"Effect: {model.best_effect:.1%}")

    with col3:
        st.metric("Confidence (avg)", f"{model.confidence_mean:.1%}")

    # Visualization: Effectiveness trends
    st.line_chart(model.theta_history)

    # Recommendation
    st.write(model.recommend_action(week=model.current_week))

    # Advanced: Posterior distributions
    st.subheader("Posterior Distributions (Thompson Sampling)")
    for i, T in enumerate(model.interventions):
        fig, ax = plt.subplots()
        samples = np.random.normal(model.theta_mean[i], model.theta_std[i], 10000)
        ax.hist(samples, bins=50, alpha=0.7)
        st.pyplot(fig)
```

### C.4 Deliverables
- [ ] Ch24c (500 lines, LaTeX theory)
- [ ] Appendix QQQ (400 lines Python, Bayesian module)
- [ ] Streamlit dashboard (open-source)
- [ ] 2-3 case studies showing learning curves
- [ ] Decision rules guide for practitioners

---

## Appendix: Test Cases & Validation

### Test Case 1: Diabetes (All Three Options)

**Input:** 52-week intervention with I_AWARE + I_READY + I_WHO,others portfolio

**Expected:** φ moves from 0.2 (PreAware) → 0.8+ (Action)

**Validation:**
- A: Verify φ ODE trajectory matches empirical data from Ch21
- B: Verify agent-based mean converges to ODE solution
- C: Verify Bayesian posterior concentrates on true θ values

### Test Case 2: Tipping Point (B & C)

**Input:** Varying I_WHO,others intensity (0%, 5%, 10%, 15%)

**Expected:** Nonlinear response (tipping point ~ 10%)

**Validation:**
- B: ABM shows bifurcation visually
- C: Online learning detects sudden portfolio efficiency change

### Test Case 3: Robustness (All Three)

**Input:** Add noise to observations (±5% random error)

**Expected:** Methods still converge to true effect, but slower

**Validation:**
- A: Equilibrium stable under small perturbations
- B: Agent variance increases; mean still converges
- C: Posterior bands widen; central estimate unchanged

---

## Dependencies & Tools

### OPTION A (System Dynamics)
- **Python:** scipy, numpy, matplotlib
- **Math:** Sympy (symbolic derivatives)
- **Visualization:** Matplotlib, Plotly

### OPTION B (Agent-Based Modeling)
- **Python:** Mesa (ABM framework), networkx (graph theory)
- **Visualization:** Pygame (animation), Plotly (aggregates)
- **Validation:** scikit-learn (calibration)

### OPTION C (Online Learning)
- **Python:** Pymc3 (Bayesian inference), scipy
- **Dashboard:** Streamlit
- **Visualization:** Plotly Dash

---

**End of Technical Specifications**

For additional questions, see GitHub Issues or contact: [Project maintainer]
