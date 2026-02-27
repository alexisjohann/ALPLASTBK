"""
Neobank Switching Behavior Model (MOD-SWITCH-001)

Implementation of the EBF Neobank Switching Model.
Predicts probability of switching from traditional banks to neobanks.

Author: EBF Framework / Claude
Session: EBF-S-2026-02-09-FIN-001
Version: 1.0
Date: 2026-02-09
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ModelParameters:
    """Parameter container for the Neobank Switching Model."""

    # Utility Weights
    w_F: float = 0.35  # Financial utility weight
    w_P: float = 0.30  # Practical utility weight
    w_S: float = 0.20  # Social utility weight
    w_I: float = 0.15  # Identity utility weight

    # Complementarity (gamma)
    gamma_FP: float = 0.25   # Financial × Practical
    gamma_PS: float = 0.30   # Practical × Social
    gamma_SI: float = 0.40   # Social × Identity
    gamma_FI: float = -0.10  # Financial × Identity (crowding-out)

    # Financial Sub-Parameters
    beta_fee: float = 0.80
    beta_fx: float = 0.60
    beta_cashback: float = 0.40
    beta_interest: float = 0.50
    beta_safety: float = 0.60

    # Practical Sub-Parameters
    beta_app: float = 0.70
    beta_onboard: float = 0.50
    beta_speed: float = 0.60
    beta_247: float = 0.50
    beta_branch: float = 0.40
    beta_advisor: float = 0.35
    beta_swiss: float = 0.55

    # Social Sub-Parameters
    beta_peer: float = 0.65
    beta_cool: float = 0.50
    beta_talk: float = 0.45
    beta_legacy: float = 0.30
    beta_status: float = 0.40

    # Identity Sub-Parameters
    beta_digital: float = 0.75
    beta_global: float = 0.60
    beta_sustain: float = 0.50
    beta_rebel: float = 0.45
    beta_tradition: float = 0.35
    beta_security: float = 0.40

    # Context Modifiers (Psi)
    iban_penalty: float = -0.15      # For primary account with shared IBAN
    fx_bonus: float = 0.25           # For high FX needs
    digital_bonus: float = 0.20      # For high digital skills
    trust_penalty: float = -0.10     # For foreign license
    switching_cost: float = -0.45    # Status quo bias (per 20 years tenure)
    inertia: float = -0.30           # No life event


@dataclass
class CustomerProfile:
    """Customer profile with characteristics."""

    # Demographics
    age: int
    income: float  # Annual income in CHF

    # Banking Behavior
    current_bank_tenure_years: float
    primary_account_intention: bool

    # Financial Characteristics
    fee_current_bank: float  # Monthly fees in CHF
    fx_need_score: float  # 0-1 scale
    deposit_amount: float  # CHF

    # Digital & Skills
    digital_skills_score: float  # 0-1 scale
    app_quality_preference: float  # 0-1 scale

    # Social
    peer_adoption_rate: float  # 0-1: proportion of friends using neobank
    brand_coolness_sensitivity: float  # 0-1 scale

    # Identity
    digital_native_identity: float  # 0-1 scale
    global_citizen_identity: float  # 0-1 scale
    sustainability_identity: float  # 0-1 scale
    rebel_identity: float  # 0-1 scale

    # Life Events
    has_life_event: bool  # Job change, move, divorce, etc.


@dataclass
class NeobankProfile:
    """Neobank-specific characteristics."""

    name: str  # "Revolut", "Neon", etc.

    # Financial
    monthly_fee: float  # CHF
    fx_fee_rate: float  # 0-1 (e.g., 0.01 = 1%)
    cashback_rate: float  # 0-1
    interest_rate: float  # Annual interest on deposits

    # Practical
    app_store_rating: float  # 1-5 stars
    onboarding_time_minutes: float
    transaction_speed: float  # 0-1 (1 = instant)
    digital_access: float  # 0-1 (1 = 24/7)

    # Regulatory
    has_personal_iban: bool  # True = personal, False = shared
    has_swiss_license: bool  # True = CH, False = foreign

    # Features
    has_twint: bool
    has_qr_bill: bool
    has_ebill: bool


class NeobankSwitchingModel:
    """
    EBF Neobank Switching Behavior Model (MOD-SWITCH-001).

    Predicts probability of switching from traditional bank to neobank
    based on 4 utility dimensions (Financial, Practical, Social, Identity)
    with complementarity effects.
    """

    def __init__(self, params: ModelParameters = None):
        """
        Initialize the model.

        Args:
            params: Model parameters. If None, uses defaults.
        """
        self.params = params or ModelParameters()

    def calculate_financial_utility(
        self,
        customer: CustomerProfile,
        neobank: NeobankProfile,
        is_neobank: bool
    ) -> float:
        """Calculate Financial Utility (U_F)."""

        if is_neobank:
            # Neobank financial utility
            fee_savings = customer.fee_current_bank - neobank.monthly_fee
            fx_savings = customer.fx_need_score * (0.015 - neobank.fx_fee_rate)
            cashback_value = neobank.cashback_rate

            U_F = (
                self.params.beta_fee * fee_savings / 50.0 +  # Normalize by CHF 50
                self.params.beta_fx * fx_savings * 100.0 +
                self.params.beta_cashback * cashback_value
            )
        else:
            # Traditional bank financial utility
            interest_value = neobank.interest_rate  # Using as baseline
            safety_premium = (
                (0.85 - 0.75) *  # trust_ch - trust_foreign
                customer.deposit_amount / 100000.0
            )

            U_F = (
                self.params.beta_interest * interest_value +
                self.params.beta_safety * safety_premium
            )

        return U_F

    def calculate_practical_utility(
        self,
        customer: CustomerProfile,
        neobank: NeobankProfile,
        is_neobank: bool
    ) -> float:
        """Calculate Practical Utility (U_P)."""

        if is_neobank:
            # Neobank practical utility
            app_value = neobank.app_store_rating / 5.0
            onboard_value = 1.0 / (neobank.onboarding_time_minutes / 10.0)
            speed_value = neobank.transaction_speed
            access_value = neobank.digital_access

            U_P = (
                self.params.beta_app * app_value +
                self.params.beta_onboard * onboard_value +
                self.params.beta_speed * speed_value +
                self.params.beta_247 * access_value
            )
        else:
            # Traditional bank practical utility
            branch_value = 0.6  # Assume moderate branch proximity
            advisor_value = 0.7  # Personal service advantage
            swiss_features = 1.0  # Full Swiss features (TWINT, QR, eBill)

            U_P = (
                self.params.beta_branch * branch_value +
                self.params.beta_advisor * advisor_value +
                self.params.beta_swiss * swiss_features
            )

        return U_P

    def calculate_social_utility(
        self,
        customer: CustomerProfile,
        neobank: NeobankProfile,
        is_neobank: bool
    ) -> float:
        """Calculate Social Utility (U_S)."""

        if is_neobank:
            # Neobank social utility
            peer_value = customer.peer_adoption_rate
            cool_value = customer.brand_coolness_sensitivity
            talk_value = 0.7  # Conversation value (moderate for neobanks)

            U_S = (
                self.params.beta_peer * peer_value +
                self.params.beta_cool * cool_value +
                self.params.beta_talk * talk_value
            )
        else:
            # Traditional bank social utility
            legacy_value = 0.5  # Family tradition (moderate)
            status_value = 0.6  # Bank prestige (e.g., UBS)

            U_S = (
                self.params.beta_legacy * legacy_value +
                self.params.beta_status * status_value
            )

        return U_S

    def calculate_identity_utility(
        self,
        customer: CustomerProfile,
        neobank: NeobankProfile,
        is_neobank: bool
    ) -> float:
        """Calculate Identity Utility (U_I)."""

        if is_neobank:
            # Neobank identity utility
            digital_value = customer.digital_native_identity
            global_value = customer.global_citizen_identity
            sustain_value = customer.sustainability_identity
            rebel_value = customer.rebel_identity

            U_I = (
                self.params.beta_digital * digital_value +
                self.params.beta_global * global_value +
                self.params.beta_sustain * sustain_value +
                self.params.beta_rebel * rebel_value
            )
        else:
            # Traditional bank identity utility
            tradition_value = 1.0 - customer.digital_native_identity
            security_value = 0.7  # Security seeker identity

            U_I = (
                self.params.beta_tradition * tradition_value +
                self.params.beta_security * security_value
            )

        return U_I

    def calculate_context_modifiers(
        self,
        customer: CustomerProfile,
        neobank: NeobankProfile,
        is_neobank: bool
    ) -> float:
        """Calculate Context Modifiers (Psi)."""

        if is_neobank:
            # Neobank context modifiers
            iban_penalty = (
                self.params.iban_penalty
                if (customer.primary_account_intention and not neobank.has_personal_iban)
                else 0.0
            )

            fx_bonus = self.params.fx_bonus * customer.fx_need_score
            digital_bonus = self.params.digital_bonus * customer.digital_skills_score

            trust_penalty = (
                self.params.trust_penalty if not neobank.has_swiss_license else 0.0
            )

            psi_modifier = iban_penalty + fx_bonus + digital_bonus + trust_penalty
        else:
            # Traditional bank context modifiers
            tenure_penalty = (
                self.params.switching_cost *
                (customer.current_bank_tenure_years / 20.0)
            )

            inertia_penalty = (
                self.params.inertia if not customer.has_life_event else 0.0
            )

            psi_modifier = tenure_penalty + inertia_penalty

        return psi_modifier

    def calculate_total_utility(
        self,
        customer: CustomerProfile,
        neobank: NeobankProfile,
        is_neobank: bool
    ) -> float:
        """
        Calculate total utility with complementarity effects.

        U = w_F·U_F + w_P·U_P + w_S·U_S + w_I·U_I
            + γ(F,P)·U_F·U_P + γ(P,S)·U_P·U_S
            + γ(S,I)·U_S·U_I + γ(F,I)·U_F·U_I
            + Ψ_modifier
        """

        # Calculate base utilities
        U_F = self.calculate_financial_utility(customer, neobank, is_neobank)
        U_P = self.calculate_practical_utility(customer, neobank, is_neobank)
        U_S = self.calculate_social_utility(customer, neobank, is_neobank)
        U_I = self.calculate_identity_utility(customer, neobank, is_neobank)

        # Additive component
        U_additive = (
            self.params.w_F * U_F +
            self.params.w_P * U_P +
            self.params.w_S * U_S +
            self.params.w_I * U_I
        )

        # Complementarity component
        U_complementarity = (
            self.params.gamma_FP * U_F * U_P +
            self.params.gamma_PS * U_P * U_S +
            self.params.gamma_SI * U_S * U_I +
            self.params.gamma_FI * U_F * U_I
        )

        # Context modifiers
        psi_modifier = self.calculate_context_modifiers(customer, neobank, is_neobank)

        # Total utility
        U_total = U_additive + U_complementarity + psi_modifier

        return U_total

    def predict_switching_probability(
        self,
        customer: CustomerProfile,
        neobank: NeobankProfile
    ) -> float:
        """
        Predict probability of switching to neobank.

        P(Switch) = 1 / (1 + exp(-ΔU))
        ΔU = U(Neobank) - U(Traditional)

        Args:
            customer: Customer profile
            neobank: Neobank profile

        Returns:
            Probability of switching (0-1)
        """

        U_neobank = self.calculate_total_utility(customer, neobank, is_neobank=True)
        U_traditional = self.calculate_total_utility(customer, neobank, is_neobank=False)

        delta_U = U_neobank - U_traditional

        # Logistic function
        p_switch = 1.0 / (1.0 + np.exp(-delta_U))

        return p_switch

    def predict_segment(
        self,
        customer: CustomerProfile
    ) -> str:
        """
        Predict customer segment.

        Segments:
        - A: Digital Natives (20-35)
        - B: Young Professionals (25-40)
        - C: Tech-Savvy Adults (35-50)
        - D: Traditional Bankers (50+)
        """

        if customer.age < 35 and customer.digital_skills_score > 0.7:
            return "A"
        elif 25 <= customer.age <= 40 and customer.fx_need_score > 0.5:
            return "B"
        elif 35 <= customer.age <= 50 and customer.income > 100000:
            return "C"
        else:
            return "D"


# Example Usage
if __name__ == "__main__":

    # Create model
    model = NeobankSwitchingModel()

    # Example customer: Digital Native
    customer_digital_native = CustomerProfile(
        age=28,
        income=80000,
        current_bank_tenure_years=5,
        primary_account_intention=False,  # Secondary account
        fee_current_bank=15.0,
        fx_need_score=0.7,
        deposit_amount=20000,
        digital_skills_score=0.9,
        app_quality_preference=0.85,
        peer_adoption_rate=0.6,
        brand_coolness_sensitivity=0.7,
        digital_native_identity=0.85,
        global_citizen_identity=0.75,
        sustainability_identity=0.6,
        rebel_identity=0.5,
        has_life_event=False
    )

    # Revolut profile
    revolut = NeobankProfile(
        name="Revolut",
        monthly_fee=0.0,
        fx_fee_rate=0.01,  # 1% on weekends/over limit
        cashback_rate=0.0,
        interest_rate=0.0,
        app_store_rating=4.8,
        onboarding_time_minutes=5,
        transaction_speed=1.0,
        digital_access=1.0,
        has_personal_iban=False,  # Shared IBAN
        has_swiss_license=False,
        has_twint=False,
        has_qr_bill=False,
        has_ebill=False
    )

    # Neon profile
    neon = NeobankProfile(
        name="Neon",
        monthly_fee=0.0,
        fx_fee_rate=0.0035,  # 0.35% surcharge
        cashback_rate=0.0,
        interest_rate=0.0,
        app_store_rating=4.7,
        onboarding_time_minutes=10,
        transaction_speed=1.0,
        digital_access=1.0,
        has_personal_iban=True,  # Personal CH-IBAN
        has_swiss_license=True,  # Via Hypi Lenzburg
        has_twint=True,
        has_qr_bill=True,
        has_ebill=True
    )

    # Predict switching probabilities
    p_revolut = model.predict_switching_probability(customer_digital_native, revolut)
    p_neon = model.predict_switching_probability(customer_digital_native, neon)

    print("=" * 60)
    print("Neobank Switching Model - Example Prediction")
    print("=" * 60)
    print(f"\nCustomer: Digital Native, Age {customer_digital_native.age}")
    print(f"Segment: {model.predict_segment(customer_digital_native)}")
    print(f"\nP(Switch to Revolut): {p_revolut:.2%}")
    print(f"P(Switch to Neon): {p_neon:.2%}")
    print(f"\nNeon more likely by: {(p_neon - p_revolut) * 100:.1f} percentage points")

    # Test with primary account intention
    customer_primary = CustomerProfile(
        age=28,
        income=80000,
        current_bank_tenure_years=5,
        primary_account_intention=True,  # PRIMARY account
        fee_current_bank=15.0,
        fx_need_score=0.7,
        deposit_amount=20000,
        digital_skills_score=0.9,
        app_quality_preference=0.85,
        peer_adoption_rate=0.6,
        brand_coolness_sensitivity=0.7,
        digital_native_identity=0.85,
        global_citizen_identity=0.75,
        sustainability_identity=0.6,
        rebel_identity=0.5,
        has_life_event=False
    )

    p_revolut_primary = model.predict_switching_probability(customer_primary, revolut)
    p_neon_primary = model.predict_switching_probability(customer_primary, neon)

    print("\n" + "=" * 60)
    print("With PRIMARY Account Intention:")
    print("=" * 60)
    print(f"P(Switch to Revolut): {p_revolut_primary:.2%} (IBAN penalty: -15%)")
    print(f"P(Switch to Neon): {p_neon_primary:.2%} (No penalty)")
    print(f"\nRevolut penalty: {(p_revolut - p_revolut_primary) * 100:.1f} pp")
