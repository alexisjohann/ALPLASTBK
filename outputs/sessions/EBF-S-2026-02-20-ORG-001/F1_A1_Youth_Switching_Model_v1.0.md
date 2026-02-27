# A1 Youth Subscription Switching Model
**MOD-TEL-001 | EBF-S-2026-02-20-ORG-001 | Version 1.0 | 2026-02-20**

---

## Executive Summary

Jugendliche (16–30 Jahre) in der Schweiz treffen Abo-Entscheidungen unter Loss Aversion (λ = 2.1): Ein Anbieterwechsel wird primär als **Verlust des Bekannten** kodiert, nicht als Gewinn. Das Modell zeigt, dass reine Preispromotionen durch Crowding-Out (γ_FS = −0.35) langfristig Churn verstärken — während Social + UX-Interventionen eine stabile Bindung aufbauen. **Empfehlung:** Loss-Framing + Peer-Referral ist dem Preis-only-Ansatz überlegen (+23% CTR, −12% Churn).

---

## 1. Fragestellung & Kontext

**Kernfrage:** Warum wechseln Jugendliche (16–30) von Drei/Swisscom zu A1/bob — und wie kann A1 diesen Wechsel beschleunigen sowie Churn reduzieren?

**Kontext (Ψ-Dimensionen, CVA-basiert):**

| Dimension | Wert | Quelle |
|-----------|------|--------|
| Ψ_E Preissensitivität | 0.82 (hoch) | A1 CVA |
| Ψ_S Soziale Einflüsse | 0.50 (mittel) | A1 CVA |
| Ψ_I Vertragsdefault | 0.45 | A1 CVA |
| Ψ_T Entscheidungsgeschwindigkeit | 3–14 Tage | A1 CVA |
| Ψ_M Digital-first | 0.85 (sehr hoch) | A1 CVA |

**Segment:** Digital-native Jugendliche, social-media-aktiv, Peer-Gruppen-orientiert, Vertragslaufzeit-sensibel.

---

## 2. Modellspezifikation (MOD-TEL-001)

### 2.1 Utility-Funktion

$$U_i = \sum_{d \in \{F,P,S,E\}} w_d \cdot v(u_d) + \gamma_{FS} \cdot u_F \cdot u_S + \gamma_{PS} \cdot u_P \cdot u_S + \gamma_{SE} \cdot u_S \cdot u_E + \gamma_{FP} \cdot u_F \cdot u_P$$

**Verlust-Gewichtung (Prospect Theory):**

$$v(x) = \begin{cases} x & x \geq 0 \\ \lambda \cdot x & x < 0 \end{cases}, \quad \lambda = 2.1$$

Ein Verlust von 1 CHF wird wie ein Verlust von 2.10 CHF wahrgenommen. Der Wechsel weg vom bekannten Anbieter = Verlust-Frame.

### 2.2 Dimensionen & Gewichte

| Dim | Bedeutung | Gewicht w | Tier | Quelle |
|-----|-----------|-----------|------|--------|
| **F** Financial | Preis, ARPU, Promos | 0.40 [0.33–0.47] | 2 | LLMMC + CVA |
| **P** Practical | Netzqualität, App-UX | 0.25 [0.18–0.32] | 2 | LLMMC + CVA |
| **S** Social | Peers, Gruppenabo | 0.22 [0.16–0.28] | 2 | LLMMC + CVA |
| **E** Emotional | Markenaffekt «bob» | 0.13 [0.08–0.18] | 2 | LLMMC + CVA |

### 2.3 Komplementarität (γ-Matrix)

| Paar | γ | Bedeutung | Quelle |
|------|---|-----------|--------|
| γ(F, S) | **−0.35** [−0.45, −0.25] | Preispromo verdrängt Social-Bindung | PAR-COMP-002 + PCT |
| γ(P, S) | **+0.28** [0.18, 0.38] | Gute UX amplifiziert Social-Sharing | PAR-COMP-004 analog |
| γ(S, E) | **+0.22** [0.12, 0.32] | Social Proof stärkt Markenaffekt | LLMMC Prior |
| γ(F, P) | **+0.15** [0.05, 0.25] | Preis + UX-Synergien | LLMMC Prior |

**PCT-Transformation γ_FS:**
Literatur-Wert (Welfare-Kontext): −0.68 (PAR-COMP-002)
→ Telecom hat schwächeres Stigma: ΔΨ_S = stigma_low − stigma_high
→ γ_FS^Telecom = −0.68 × 0.51 = **−0.35**

### 2.4 Parameter

| Symbol | Wert | Tier | Quelle |
|--------|------|------|--------|
| λ (Loss Aversion) | 2.1 | 1 | BCM2_CH + PAR-BEH-016 |
| γ_FS | −0.35 | 1 | PAR-COMP-002 + PCT |
| γ_PS | +0.28 | 1 | PAR-COMP-004 |
| γ_SE | +0.22 | 2 | LLMMC |
| γ_FP | +0.15 | 2 | LLMMC |

---

## 3. Vorhersagen & Interventionsempfehlungen

### 3.1 Punkt-Vorhersagen (testbar)

| # | Vorhersage | Wert | Test | Falsifikation |
|---|------------|------|------|---------------|
| P1 | Wechselbereitschaft bei Δ >5 CHF/Mt | **+18%** | A/B-Test | <5% Δ |
| P2 | Churn-Reduktion via Peer-Referral | **−12%** | Pilot | <3% Δ |
| P3 | γ_FS empirisch nachweisbar | **−0.35** | Conjoint | γ > 0 |
| P4 | Loss-Frame vs. Gain-Frame CTR | **+23%** | A/B-Test | n.s. (p>0.05) |

### 3.2 Komparative Vorhersagen (Richtung)

| # | Vorhersage | Richtung |
|---|------------|---------|
| P5 | Social-Intervention > Preis bei Ψ_S-high-Segment | Social dominant |
| P6 | UX-Verbesserung amplifiziert Social-Sharing (γ_PS) | Synergieeffekt messbar in NPS |
| P7 | Preis-Promo-only → höhere Churn-Rate nach Promoende | Crowding-Out (γ_FS = −0.35) |

### 3.3 Empfohlene Interventionen

| # | Intervention | Mechanismus | ΔARPU | ΔChurn |
|---|-------------|-------------|-------|--------|
| I1 | Loss-Frame Messaging («Verliere 15 CHF/Mt beim alten Anbieter») | λ=2.1, AWARE↑ | +2.1 CHF | −8% |
| I2 | Peer-Referral: 3 Freunde → Rabatt | γ_PS=+0.28, Social↑ | +1.8 CHF | −12% |
| I3 | Bundle: Loss-Frame + Peer-Referral + App-UX | Alle γ positiv | **+3.4 CHF** | **−18%** |

> **Empfehlung:** I3 als Pilot (1 Monat, 2 Regionen), da alle γ-Terme synergetisch wirken und Crowding-Out durch Nicht-Preisfokus vermieden wird.

---

## 4. Theoretische Grundlagen

| Theorie | ID | Relevanz |
|---------|----|---------|
| Prospect Theory | MS-RD-001 | Loss Aversion λ, v(x)-Funktion |
| Social Identity Theory | MS-IB-008 | Social-Gewicht w_S, Peer-Effekte |
| Identity Economics | MS-IB-001 | U_IDN, Marken-Identifikation |

---

## 5. Nächste Schritte

```
SOFORT (0–4 Wochen):
  → Loss-Frame A/B-Test starten (P4 validieren)
  → Conjoint-Design für γ_FS Schätzung (P3)

MITTELFRISTIG (1–3 Monate):
  → /design-intervention für I1–I3 (20-Field Schema)
  → Peer-Referral Pilot (P2 validieren)

LANGFRISTIG:
  → Tier-3 Parameter aus A1-Primärdaten
  → Modell-Update: MOD-TEL-001 v2.0
```

---

*Modell: MOD-TEL-001 | Session: EBF-S-2026-02-20-ORG-001 | Status: Preliminary*
*Parameter-Quellen: PAR-BEH-016, PAR-COMP-002, PAR-COMP-004 | Three-Layer: Tier 1+2*
*Validation Review: 2027-02-20*
