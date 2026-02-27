"""
MOD-REF-002: Referral Incentive Optimization Model
===================================================

Two-Stage Hurdle Model for Banking Referral Programs

Stage 1: Participation Decision (Logistic)
Stage 2: Referral Intensity (Zero-Truncated Poisson)

Author: FehrAdvice & Partners AG
Session: EBF-S-2026-02-09-FIN-002
Date: February 9, 2026
Framework: EBF (Evidence-Based Framework)
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from scipy.stats import norm, poisson
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


@dataclass
class ContextFactors:
    """
    Ψ-Context Dimensions (7 dimensions)
    """
    # Institutional (Ψ_I)
    default_structure: str = "opt-in"  # "opt-in" or "opt-out"
    regulatory_environment: str = "FINMA"
    program_visibility: float = 0.70  # [0,1]

    # Social (Ψ_S)
    peer_activity: float = 0.30  # [0,1]
    social_norms: float = 0.50  # [-1,1], 0.5 = neutral-positive
    relationship_quality: float = 0.60  # [0,1]

    # Cultural (Ψ_K)
    trust_banks: float = 0.72  # Switzerland baseline
    individualism: float = 0.68  # Switzerland
    gift_giving_acceptability: float = 0.50  # [0,1]

    # Cognitive (Ψ_C)
    awareness_program: int = 1  # 0 or 1
    complexity_perception: float = 0.30  # [0,1], 0=simple
    cognitive_load: float = 0.40  # [0,1], 0=relaxed

    # Economic (Ψ_E)
    incentive_salience: float = 0.50  # Incentive/Monthly Income
    opportunity_cost: float = 50.0  # CHF/hour

    # Temporal (Ψ_T)
    months_since_onboarding: float = 12.0  # Months
    program_maturity: str = "established"  # "new" or "established"


@dataclass
class IncentiveDesign:
    """
    Incentive Program Design
    """
    # Financial component
    financial_amount: float = 100.0  # CHF
    structure: str = "flat"  # "flat", "tiered", "lottery"
    tiered_amounts: Optional[List[float]] = None  # [50, 100, 150] for tiered

    # Social component
    recognition_program: bool = True
    leaderboard: bool = False
    exclusive_events: bool = True

    # Identity component
    identity_messaging: bool = True
    charity_option: bool = True
    charity_amount: float = 25.0  # CHF to charity


@dataclass
class CustomerSegment:
    """
    Customer Segment Characteristics
    """
    name: str = "Quiet Satisfied"

    # Demographics
    age_range: Tuple[int, int] = (35, 55)
    digital_adoption: float = 0.60  # [0,1]

    # Behavioral
    nps: int = 7  # Net Promoter Score (0-10)
    satisfaction: float = 0.70  # [0,1]
    network_size: int = 50  # Number of potential referees

    # Segment-specific modifiers
    financial_sensitivity: float = 1.0  # Multiplier on β_F
    social_sensitivity: float = 1.0  # Multiplier on β_S
    identity_sensitivity: float = 1.0  # Multiplier on β_I


@dataclass
class ModelParameters:
    """
    Model Parameters with Bayesian Priors

    All parameters are Normal distributions: N(mean, sd)
    """
    # Stage 1: Participation (Utility components)
    beta_F_mean: float = 0.40  # Financial sensitivity
    beta_F_sd: float = 0.10

    beta_S_mean: float = 0.55  # Social sensitivity
    beta_S_sd: float = 0.12

    beta_I_mean: float = 0.50  # Identity sensitivity
    beta_I_sd: float = 0.10

    beta_P_mean: float = 0.35  # Practical sensitivity
    beta_P_sd: float = 0.08

    beta_E_mean: float = 0.20  # Emotional sensitivity
    beta_E_sd: float = 0.08

    beta_0: float = -1.5  # Intercept (baseline log-odds)

    # Utility weights (FIPSE)
    w_F: float = 0.25  # Financial
    w_S: float = 0.30  # Social
    w_I: float = 0.25  # Identity
    w_P: float = 0.15  # Practical
    w_E: float = 0.05  # Emotional

    # Complementarity matrix (γ)
    gamma_FI: float = -0.68  # ⚠️ CRITICAL: Financial crowds out Identity
    gamma_SI: float = +0.40  # ✓ Social reinforces Identity
    gamma_FS: float = -0.15  # Financial weakens Social
    gamma_PS: float = +0.20  # Practical boosts Social
    gamma_EI: float = +0.30  # Emotional reinforces Identity

    # Stage 2: Intensity (Count model)
    alpha_0_mean: float = 0.50  # Baseline log-rate
    alpha_0_sd: float = 0.15

    alpha_F_mean: float = 0.30  # Financial boost
    alpha_F_sd: float = 0.10

    alpha_S_mean: float = 0.45  # Social boost
    alpha_S_sd: float = 0.10

    theta_peer_mean: float = 0.60  # Peer activity multiplier
    theta_peer_sd: float = 0.12

    theta_time_mean: float = -0.15  # Temporal decay
    theta_time_sd: float = 0.05


class ReferralIncentiveModel:
    """
    Two-Stage Hurdle Model for Referral Behavior

    Stage 1: Participation Decision (Binary)
    Stage 2: Referral Intensity (Count | Participate=1)
    """

    def __init__(self, params: ModelParameters):
        self.params = params

        # Sample parameters from priors (for uncertainty quantification)
        self.beta_F = params.beta_F_mean
        self.beta_S = params.beta_S_mean
        self.beta_I = params.beta_I_mean
        self.beta_P = params.beta_P_mean
        self.beta_E = params.beta_E_mean

        self.alpha_0 = params.alpha_0_mean
        self.alpha_F = params.alpha_F_mean
        self.alpha_S = params.alpha_S_mean
        self.theta_peer = params.theta_peer_mean
        self.theta_time = params.theta_time_mean

    def calculate_utility_financial(
        self,
        incentive_amount: float,
        context: ContextFactors
    ) -> float:
        """
        U_F = β_F × log(Incentive + 1) × Ψ_incentive_salience
        """
        log_incentive = np.log(incentive_amount + 1)
        U_F = self.beta_F * log_incentive * context.incentive_salience
        return U_F

    def calculate_utility_social(
        self,
        context: ContextFactors,
        incentive_design: IncentiveDesign
    ) -> float:
        """
        U_S = β_S × Ψ_relationship_quality × Ψ_social_norms

        Boosted by recognition program
        """
        U_S = self.beta_S * context.relationship_quality * context.social_norms

        # Recognition program boosts social utility
        if incentive_design.recognition_program:
            U_S *= 1.20  # +20% boost

        return U_S

    def calculate_utility_identity(
        self,
        U_F: float,
        context: ContextFactors,
        incentive_design: IncentiveDesign
    ) -> float:
        """
        U_I = β_I × (Identity_baseline - Crowding_Out_Effect)

        Crowding_Out_Effect = γ(F,I) × U_F × Identity_baseline
        """
        # Baseline identity utility
        identity_baseline = self.beta_I * 1.0  # Normalized to 1.0

        # Crowding-Out Effect (negative interaction with financial)
        crowding_out = self.params.gamma_FI * U_F * identity_baseline

        U_I = identity_baseline + crowding_out  # crowding_out is negative

        # Identity messaging buffers crowding-out
        if incentive_design.identity_messaging:
            U_I *= 1.15  # +15% buffer

        return U_I

    def calculate_utility_practical(
        self,
        context: ContextFactors
    ) -> float:
        """
        U_P = β_P × (1 - Ψ_complexity) × (1 - Ψ_cognitive_load)
        """
        ease_factor = (1 - context.complexity_perception) * (1 - context.cognitive_load)
        U_P = self.beta_P * ease_factor
        return U_P

    def calculate_utility_emotional(
        self,
        incentive_design: IncentiveDesign
    ) -> float:
        """
        U_E = β_E × Warm_Glow_Factor

        Boosted by charity option
        """
        warm_glow = self.beta_E * 1.0  # Baseline

        # Charity option enhances warm glow
        if incentive_design.charity_option:
            warm_glow *= 1.25  # +25% boost

        return warm_glow

    def calculate_total_utility(
        self,
        incentive_design: IncentiveDesign,
        context: ContextFactors,
        segment: CustomerSegment
    ) -> float:
        """
        U_total = Σ w_i × U_i + Σ γ_ij × U_i × U_j + β_0

        With complementarity effects (γ)
        """
        # Calculate individual utilities
        U_F = self.calculate_utility_financial(
            incentive_design.financial_amount,
            context
        )
        U_S = self.calculate_utility_social(context, incentive_design)
        U_I = self.calculate_utility_identity(U_F, context, incentive_design)
        U_P = self.calculate_utility_practical(context)
        U_E = self.calculate_utility_emotional(incentive_design)

        # Apply segment-specific modifiers
        U_F *= segment.financial_sensitivity
        U_S *= segment.social_sensitivity
        U_I *= segment.identity_sensitivity

        # Weighted sum
        U_linear = (
            self.params.w_F * U_F +
            self.params.w_S * U_S +
            self.params.w_I * U_I +
            self.params.w_P * U_P +
            self.params.w_E * U_E
        )

        # Complementarity terms (γ_ij × U_i × U_j)
        U_complementarity = (
            self.params.gamma_FI * U_F * U_I +  # ⚠️ Negative (Crowding-Out)
            self.params.gamma_SI * U_S * U_I +  # ✓ Positive (Synergy)
            self.params.gamma_FS * U_F * U_S +  # Negative (weak)
            self.params.gamma_PS * U_P * U_S +  # Positive
            self.params.gamma_EI * U_E * U_I    # Positive
        )

        # Total utility
        U_total = U_linear + U_complementarity + self.params.beta_0

        return U_total

    def predict_participation(
        self,
        incentive_design: IncentiveDesign,
        context: ContextFactors,
        segment: CustomerSegment
    ) -> float:
        """
        P(Participate = 1) = 1 / (1 + exp(-U_total))

        Logistic transformation of utility
        """
        # Zero participation if not aware
        if context.awareness_program == 0:
            return 0.0

        U_total = self.calculate_total_utility(
            incentive_design,
            context,
            segment
        )

        # Logistic transformation
        P_participate = 1.0 / (1.0 + np.exp(-U_total))

        return P_participate

    def predict_intensity(
        self,
        incentive_design: IncentiveDesign,
        context: ContextFactors,
        segment: CustomerSegment
    ) -> float:
        """
        λ = exp(α_0 + Σ α_i × U_i + θ_peer × Ψ_peer + θ_time × log(months+1))

        Expected referrals per year (given participation)
        """
        # Calculate utilities (same as Stage 1)
        U_F = self.calculate_utility_financial(
            incentive_design.financial_amount,
            context
        )
        U_S = self.calculate_utility_social(context, incentive_design)

        # Log-linear model
        log_lambda = (
            self.alpha_0 +
            self.alpha_F * U_F +
            self.alpha_S * U_S +
            self.theta_peer * context.peer_activity +
            self.theta_time * np.log(context.months_since_onboarding + 1)
        )

        # Cap network size effect
        max_referrals = min(segment.network_size * 0.20, 10)  # Max 20% of network or 10
        lambda_rate = min(np.exp(log_lambda), max_referrals)

        return lambda_rate

    def predict_total_referrals(
        self,
        incentive_design: IncentiveDesign,
        context: ContextFactors,
        segment: CustomerSegment
    ) -> float:
        """
        E[Referrals] = P(Participate) × E[Referrals | Participate=1]
        """
        P_participate = self.predict_participation(
            incentive_design,
            context,
            segment
        )

        lambda_intensity = self.predict_intensity(
            incentive_design,
            context,
            segment
        )

        expected_referrals = P_participate * lambda_intensity

        return expected_referrals

    def predict_with_uncertainty(
        self,
        incentive_design: IncentiveDesign,
        context: ContextFactors,
        segment: CustomerSegment,
        n_samples: int = 1000
    ) -> Dict[str, Tuple[float, float, float]]:
        """
        Monte Carlo sampling for uncertainty quantification

        Returns 90% Confidence Intervals for:
        - P(Participate)
        - E[Referrals | Participate]
        - E[Total Referrals]
        """
        # Sample parameters from priors
        beta_F_samples = np.random.normal(
            self.params.beta_F_mean,
            self.params.beta_F_sd,
            n_samples
        )
        beta_S_samples = np.random.normal(
            self.params.beta_S_mean,
            self.params.beta_S_sd,
            n_samples
        )
        alpha_0_samples = np.random.normal(
            self.params.alpha_0_mean,
            self.params.alpha_0_sd,
            n_samples
        )

        P_samples = []
        lambda_samples = []
        total_samples = []

        for i in range(n_samples):
            # Temporarily set sampled parameters
            self.beta_F = beta_F_samples[i]
            self.beta_S = beta_S_samples[i]
            self.alpha_0 = alpha_0_samples[i]

            # Predict
            P = self.predict_participation(incentive_design, context, segment)
            lam = self.predict_intensity(incentive_design, context, segment)
            total = P * lam

            P_samples.append(P)
            lambda_samples.append(lam)
            total_samples.append(total)

        # Reset to mean values
        self.beta_F = self.params.beta_F_mean
        self.beta_S = self.params.beta_S_mean
        self.alpha_0 = self.params.alpha_0_mean

        # Calculate percentiles (90% CI: 5th to 95th percentile)
        def get_ci(samples):
            return (
                np.percentile(samples, 5),
                np.percentile(samples, 50),
                np.percentile(samples, 95)
            )

        return {
            'participation': get_ci(P_samples),
            'intensity': get_ci(lambda_samples),
            'total_referrals': get_ci(total_samples)
        }

    def optimize_incentive_amount(
        self,
        context: ContextFactors,
        segment: CustomerSegment,
        incentive_design_template: IncentiveDesign,
        clv: float = 1000.0,
        conversion_rate: float = 0.20,
        amount_range: Tuple[float, float] = (0, 500)
    ) -> Dict[str, float]:
        """
        Find optimal incentive amount that maximizes NET VALUE

        NET VALUE = CLV × Conversion_Rate × Total_Referrals - Program_Cost
        """
        def objective(amount):
            # Create design with this amount
            design = IncentiveDesign(
                financial_amount=amount,
                structure=incentive_design_template.structure,
                recognition_program=incentive_design_template.recognition_program,
                identity_messaging=incentive_design_template.identity_messaging,
                charity_option=incentive_design_template.charity_option
            )

            # Predict total referrals
            total_refs = self.predict_total_referrals(design, context, segment)

            # Calculate NET VALUE
            gross_value = clv * conversion_rate * total_refs
            program_cost = amount * total_refs
            net_value = gross_value - program_cost

            # Minimize negative NET VALUE (to maximize NET VALUE)
            return -net_value

        # Optimize
        result = minimize(
            objective,
            x0=100.0,  # Start at CHF 100
            bounds=[(amount_range[0], amount_range[1])],
            method='L-BFGS-B'
        )

        optimal_amount = result.x[0]
        optimal_net_value = -result.fun

        # Calculate details at optimal
        optimal_design = IncentiveDesign(
            financial_amount=optimal_amount,
            structure=incentive_design_template.structure,
            recognition_program=incentive_design_template.recognition_program,
            identity_messaging=incentive_design_template.identity_messaging,
            charity_option=incentive_design_template.charity_option
        )

        P = self.predict_participation(optimal_design, context, segment)
        lam = self.predict_intensity(optimal_design, context, segment)
        total = P * lam

        gross = clv * conversion_rate * total
        cost = optimal_amount * total
        roi = (gross - cost) / cost if cost > 0 else 0

        return {
            'optimal_amount': optimal_amount,
            'participation': P,
            'intensity': lam,
            'total_referrals': total,
            'gross_value': gross,
            'program_cost': cost,
            'net_value': optimal_net_value,
            'roi': roi
        }

    def simulate_market_potential(
        self,
        customer_base: int,
        segment_distribution: Dict[str, float],
        incentive_design: IncentiveDesign,
        context: ContextFactors,
        segments: Dict[str, CustomerSegment],
        clv: float = 1000.0,
        conversion_rate: float = 0.20
    ) -> pd.DataFrame:
        """
        Simulate market potential across all segments

        Returns DataFrame with segment-level and total predictions
        """
        results = []

        for seg_name, seg_prop in segment_distribution.items():
            if seg_name not in segments:
                continue

            segment = segments[seg_name]
            n_customers = int(customer_base * seg_prop)

            # Predict with uncertainty
            pred = self.predict_with_uncertainty(
                incentive_design,
                context,
                segment,
                n_samples=1000
            )

            P_low, P_med, P_high = pred['participation']
            lam_low, lam_med, lam_high = pred['intensity']
            total_low, total_med, total_high = pred['total_referrals']

            # Total referrals for this segment
            refs_low = n_customers * total_low
            refs_med = n_customers * total_med
            refs_high = n_customers * total_high

            # New customers
            new_cust_low = refs_low * conversion_rate
            new_cust_med = refs_med * conversion_rate
            new_cust_high = refs_high * conversion_rate

            # Value
            gross_low = new_cust_low * clv
            gross_med = new_cust_med * clv
            gross_high = new_cust_high * clv

            cost_low = refs_low * incentive_design.financial_amount
            cost_med = refs_med * incentive_design.financial_amount
            cost_high = refs_high * incentive_design.financial_amount

            net_low = gross_low - cost_high  # Conservative: low gross, high cost
            net_med = gross_med - cost_med
            net_high = gross_high - cost_low  # Optimistic: high gross, low cost

            results.append({
                'segment': seg_name,
                'n_customers': n_customers,
                'participation_low': P_low,
                'participation_med': P_med,
                'participation_high': P_high,
                'intensity_low': lam_low,
                'intensity_med': lam_med,
                'intensity_high': lam_high,
                'total_referrals_low': refs_low,
                'total_referrals_med': refs_med,
                'total_referrals_high': refs_high,
                'new_customers_low': new_cust_low,
                'new_customers_med': new_cust_med,
                'new_customers_high': new_cust_high,
                'gross_value_low': gross_low,
                'gross_value_med': gross_med,
                'gross_value_high': gross_high,
                'program_cost_low': cost_low,
                'program_cost_med': cost_med,
                'program_cost_high': cost_high,
                'net_value_low': net_low,
                'net_value_med': net_med,
                'net_value_high': net_high
            })

        df = pd.DataFrame(results)

        # Add total row
        total_row = {
            'segment': 'TOTAL',
            'n_customers': df['n_customers'].sum(),
            'participation_low': np.nan,
            'participation_med': np.nan,
            'participation_high': np.nan,
            'intensity_low': np.nan,
            'intensity_med': np.nan,
            'intensity_high': np.nan,
            'total_referrals_low': df['total_referrals_low'].sum(),
            'total_referrals_med': df['total_referrals_med'].sum(),
            'total_referrals_high': df['total_referrals_high'].sum(),
            'new_customers_low': df['new_customers_low'].sum(),
            'new_customers_med': df['new_customers_med'].sum(),
            'new_customers_high': df['new_customers_high'].sum(),
            'gross_value_low': df['gross_value_low'].sum(),
            'gross_value_med': df['gross_value_med'].sum(),
            'gross_value_high': df['gross_value_high'].sum(),
            'program_cost_low': df['program_cost_low'].sum(),
            'program_cost_med': df['program_cost_med'].sum(),
            'program_cost_high': df['program_cost_high'].sum(),
            'net_value_low': df['net_value_low'].sum(),
            'net_value_med': df['net_value_med'].sum(),
            'net_value_high': df['net_value_high'].sum()
        }

        df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

        return df


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":

    print("="*80)
    print("MOD-REF-002: Referral Incentive Optimization Model")
    print("="*80)
    print()

    # Initialize model
    params = ModelParameters()
    model = ReferralIncentiveModel(params)

    # Define context (Swiss banking)
    context = ContextFactors(
        trust_banks=0.72,
        individualism=0.68,
        peer_activity=0.30,
        relationship_quality=0.60,
        months_since_onboarding=12.0
    )

    # Define segments
    segments = {
        'Active Ambassadors': CustomerSegment(
            name='Active Ambassadors',
            nps=10,
            satisfaction=0.90,
            network_size=80,
            financial_sensitivity=0.70,  # Less sensitive to money
            social_sensitivity=1.30,  # More sensitive to social
            identity_sensitivity=1.40  # Much more sensitive to identity
        ),
        'Quiet Satisfied': CustomerSegment(
            name='Quiet Satisfied',
            nps=7,
            satisfaction=0.70,
            network_size=50,
            financial_sensitivity=1.00,
            social_sensitivity=1.00,
            identity_sensitivity=1.00
        ),
        'Occasional Recommenders': CustomerSegment(
            name='Occasional Recommenders',
            nps=6,
            satisfaction=0.60,
            network_size=40,
            financial_sensitivity=1.30,  # More sensitive to money
            social_sensitivity=0.80,  # Less sensitive to social
            identity_sensitivity=0.70  # Much less sensitive to identity
        )
    }

    # Test 1: Compare incentive types
    print("\n" + "="*80)
    print("TEST 1: Compare Incentive Types")
    print("="*80)

    designs = {
        'Pure Financial (CHF 100)': IncentiveDesign(
            financial_amount=100,
            recognition_program=False,
            identity_messaging=False,
            charity_option=False
        ),
        'Pure Social (Recognition)': IncentiveDesign(
            financial_amount=0,
            recognition_program=True,
            identity_messaging=True,
            charity_option=False
        ),
        'Hybrid (CHF 50 + Social)': IncentiveDesign(
            financial_amount=50,
            recognition_program=True,
            identity_messaging=True,
            charity_option=True
        )
    }

    for design_name, design in designs.items():
        print(f"\n{design_name}:")
        print("-" * 60)

        segment = segments['Quiet Satisfied']

        # Point prediction
        P = model.predict_participation(design, context, segment)
        lam = model.predict_intensity(design, context, segment)
        total = model.predict_total_referrals(design, context, segment)

        print(f"  Participation: {P:.2%}")
        print(f"  Intensity (given participate): {lam:.2f} referrals/year")
        print(f"  Total Expected: {total:.2f} referrals/customer")

        # Uncertainty
        pred = model.predict_with_uncertainty(design, context, segment)
        P_low, P_med, P_high = pred['participation']
        total_low, total_med, total_high = pred['total_referrals']

        print(f"  90% CI: Participation [{P_low:.2%}, {P_high:.2%}]")
        print(f"  90% CI: Total Referrals [{total_low:.2f}, {total_high:.2f}]")

    # Test 2: Optimize incentive amount
    print("\n" + "="*80)
    print("TEST 2: Optimize Incentive Amount")
    print("="*80)

    template = IncentiveDesign(
        recognition_program=True,
        identity_messaging=True,
        charity_option=True
    )

    opt_result = model.optimize_incentive_amount(
        context,
        segments['Quiet Satisfied'],
        template,
        clv=1000.0,
        conversion_rate=0.20
    )

    print(f"\nOptimal Incentive Amount: CHF {opt_result['optimal_amount']:.2f}")
    print(f"Participation: {opt_result['participation']:.2%}")
    print(f"Intensity: {opt_result['intensity']:.2f} referrals/year")
    print(f"Total Referrals: {opt_result['total_referrals']:.2f} per customer")
    print(f"Gross Value: CHF {opt_result['gross_value']:.2f}")
    print(f"Program Cost: CHF {opt_result['program_cost']:.2f}")
    print(f"NET VALUE: CHF {opt_result['net_value']:.2f}")
    print(f"ROI: {opt_result['roi']:.1%}")

    # Test 3: Market potential simulation
    print("\n" + "="*80)
    print("TEST 3: Market Potential Simulation")
    print("="*80)

    design_hybrid = IncentiveDesign(
        financial_amount=100,
        structure="flat",
        recognition_program=True,
        identity_messaging=True,
        charity_option=True
    )

    segment_distribution = {
        'Active Ambassadors': 0.15,
        'Quiet Satisfied': 0.45,
        'Occasional Recommenders': 0.30
        # Private/Disengaged: 0.10 excluded
    }

    market_df = model.simulate_market_potential(
        customer_base=100000,
        segment_distribution=segment_distribution,
        incentive_design=design_hybrid,
        context=context,
        segments=segments,
        clv=1000.0,
        conversion_rate=0.20
    )

    print("\nMarket Potential Summary:")
    print("-" * 80)
    print(market_df[['segment', 'n_customers', 'participation_med',
                     'total_referrals_med', 'new_customers_med',
                     'net_value_med']].to_string(index=False))

    print("\n" + "="*80)
    print("Total Market Impact (90% CI):")
    print("="*80)
    total_row = market_df[market_df['segment'] == 'TOTAL'].iloc[0]
    print(f"Total Referrals: {total_row['total_referrals_low']:.0f} - {total_row['total_referrals_high']:.0f}")
    print(f"New Customers: {total_row['new_customers_low']:.0f} - {total_row['new_customers_high']:.0f}")
    print(f"NET VALUE: CHF {total_row['net_value_low']/1e6:.1f}M - CHF {total_row['net_value_high']/1e6:.1f}M")
    print(f"ROI: {(total_row['net_value_low']/total_row['program_cost_med']):.0%} - {(total_row['net_value_high']/total_row['program_cost_med']):.0%}")

    print("\n" + "="*80)
    print("Model run complete!")
    print("="*80)
