# HR Retention Portfolio - Strukturierte Übersicht

**Portfolio ID:** PORT-HR-001
**Domain:** HR / Churn Reduction
**Track:** Financial + Identity
**Erstellt:** 2026-01-19
**Datei:** `hr-retention-financial.yaml`

---

## 1. Portfolio-Übersicht

### 1.1 Interventions-Matrix

| ID | Name | Typ | Phase | Target Segment | Score |
|----|------|-----|-------|----------------|-------|
| INT-HR-001 | Career Path Visibility | I_AWARE (Awareness) | awareness | sophisticates, autonomy_seeking | 100% |
| INT-HR-002 | Development Dashboard | I_AWARE_k (Feedback) | action, maintenance | present_biased, loss_averse | 100% |
| INT-HR-003 | Auto-Enrollment Training | I_WHEN (Contextual) | triggered, action | present_biased, naifs | 100% |
| INT-HR-004 | Retention Bonus | I_WHAT_F-a (Financial) | action | loss_averse, sophisticates | 100% |
| INT-HR-005 | Certification Program | I_WHO-a (Identity) | stable, maintenance | social_oriented, sophisticates | 97% |
| INT-HR-006 | Benefits Package | I_WHAT_F-b (Financial) | maintenance, stable | loss_averse, present_biased | 94% |
| INT-HR-007 | Mental Budgets System | I_WHO-b (Identity) | maintenance, stable | ALL SEGMENTS | 100% |

### 1.2 Journey Coverage

```
              awareness    triggered    action    maintenance    stable
                 │            │           │            │           │
I_AWARE ─────────●────────────┼───────────┼────────────┼───────────┤
I_AWARE_k ───────┼────────────┼───────────●────────────●───────────┤
I_WHEN ──────────┼────────────●───────────●────────────┼───────────┤
I_WHO-a ─────────┼────────────┼───────────┼────────────●───────────●
I_WHO-b ─────────┼────────────┼───────────┼────────────●───────────●
I_WHAT_F-a ──────┼────────────┼───────────●────────────┼───────────┤
I_WHAT_F-b ──────┼────────────┼───────────┼────────────●───────────●
                 │            │           │            │           │
              ✅ I_AWARE  ✅ I_WHEN  ✅ Multiple   ✅ Multiple   ✅ I_WHO
```

### 1.3 Synergien (γ > 0)

| Paar | γ | Mechanismus |
|------|---|-------------|
| I_AWARE + I_WHEN | +0.4 | Awareness macht Defaults effektiver |
| I_AWARE_k + I_WHEN | +0.3 | Feedback verstärkt Kontextänderungen |
| I_AWARE + I_WHO-b | +0.3 | Awareness + Community Service |
| I_AWARE + I_WHO-a | +0.2 | Career visibility + Identity |
| I_AWARE_k + I_WHO-b | +0.2 | Impact-Feedback + Identity |

### 1.4 Crowding-Out Status

```
✅ Kein I_WHO_o (Social) im Portfolio → Keine I_WHO_o+I_WHAT_F Konflikte
✅ Kein I_HOW (Commitment) im Portfolio → Keine I_WHAT_F+I_HOW Konflikte
✅ I_WHAT_F → I_WHO Transformation bei INT-HR-007 vermeidet Crowding-Out
```

---

## 2. Detailstruktur der Datei

### 2.1 Datei-Navigation (Zeilennummern)

```yaml
# PORTFOLIO HEADER
portfolio:                           # Zeile 10-39
  coherence:                         # Zeile 17-38

# INTERVENTIONEN
INT-HR-001 (I_AWARE):                # Zeile 42-122
INT-HR-002 (I_AWARE_k):              # Zeile 123-209
INT-HR-003 (I_WHEN):                 # Zeile 210-300
INT-HR-004 (I_WHAT_F-a Bonus):       # Zeile 301-406
INT-HR-005 (I_WHO-a Certification):  # Zeile 407-504
INT-HR-006 (I_WHAT_F-b Benefits):    # Zeile 505-1085
  ├── benefits_examples:             # Zeile 620-632
  ├── benefit_complementarities:     # Zeile 634-695
  ├── marginal_utility_analysis:     # Zeile 697-771
  ├── optimal_portfolio_design:      # Zeile 773-859
  └── choice_architecture:           # Zeile 861-1085

INT-HR-007 (I_WHO-b Mental Budgets): # Zeile 1087-1505
  ├── company_value_profiles:        # Zeile 1216-1274
  ├── exit_rules:                    # Zeile 1276-1341
  └── mental_budgets:                # Zeile 1410-1505

# VALIDATION CHECKLIST                # Zeile 1507-1519
```

---

## 3. Kernkonzepte

### 3.1 Die 10C Interventionsdimensionen

| Dimension | Name | Target | Im Portfolio |
|-----------|------|--------|--------------|
| I_AWARE | Awareness | A(·) | ✅ INT-HR-001 |
| I_AWARE_k | Feedback | κ_AWX | ✅ INT-HR-002 |
| I_WHEN | Contextual | κ_KON | ✅ INT-HR-003 |
| I_WHEN_t | Temporal | κ_JNY | ❌ nicht verwendet |
| I_WHO | Identity | W_base | ✅ INT-HR-005, INT-HR-007 |
| I_WHO_o | Social | u_S | ❌ bewusst vermieden (Crowding-Out) |
| I_WHAT_F | Financial | u_F | ✅ INT-HR-004, INT-HR-006 |
| I_HOW | Commitment | γ_ij | ❌ bewusst vermieden (Crowding-Out) |

### 3.2 Mental Identity Budgeting (INT-HR-007)

**Konzept:** Transformation I_WHAT_F → I_WHO

```
Vorher:  Überstunden → verfallen → Frustration (I_WHAT_F Verlust)
Nachher: Überstunden → Identity Budgets → Purpose (I_WHO Gewinn)
```

**4 Budgets:**

| Budget | Identity | Target Segment | σ |
|--------|----------|----------------|---|
| 🤝 Community | Contributor/Giver | social_oriented | 1.6 |
| 👨‍👩‍👧 Care | Caregiver/Protector | loss_averse | 1.4 |
| 🌴 Sabbatical | Self-Investor | autonomy_seeking | 1.5 |
| 📚 Learning | Expert/Learner | sophisticates | 1.3 |

### 3.3 Benefits Choice Architecture

**Optimale Box-Größe:**
- Kategorien: 4 (Mobility, Health, Family, Financial)
- Optionen/Kategorie: 3 (Good-Better-Best)
- Total sichtbar: 12
- Wählbar: Budget-System (100 Punkte) oder Tier-System

**Formel:**
```
Z(n) = Z_max × (1 - 0.03 × max(0, n-7))
→ Jede Option über 7 senkt Zufriedenheit um ~3%
```

### 3.4 Identity Lock-In (Exit-Regelung)

| Option | Regel | Retention | Fairness |
|--------|-------|-----------|----------|
| Forfeit | 100% Verfall | Sehr hoch | Niedrig |
| **Identity Discount** | **50% Auszahlung** | **Hoch** | **Hoch** |
| Full Payout | 100% Auszahlung | Niedrig | Sehr hoch |

**Empfehlung:** Identity Discount (50%)

---

## 4. Company Value Profiles

Je nach Unternehmenswerten andere Budgets:

| Unternehmenstyp | Primäre Budgets | Zusatz-Budget |
|-----------------|-----------------|---------------|
| Sustainability | Community, Sabbatical | 🌱 Green Budget |
| Family-friendly | Care, Sabbatical | 👨‍👩‍👧 Family+ Budget |
| Innovation | Learning, Sabbatical | 💡 Innovation Budget |
| Social Impact | Community, Care | 🌍 Impact Budget |

---

## 5. Benefit-Komplementaritäten

### 5.1 Starke Komplementäre (γ > 0.3)

| Paar | γ | Empfehlung |
|------|---|------------|
| Firmenauto + Parkplatz | +0.5 | IMMER zusammen |
| Kinderbetreuung + FlexTime | +0.4 | IMMER zusammen |
| Gym + Mental Health | +0.35 | Empfohlen |

### 5.2 Substitute (γ < 0)

| Paar | γ | Empfehlung |
|------|---|------------|
| Firmenauto + ÖV-Abo | -0.3 | NUR eines anbieten |
| Essenszuschuss + Kantine | -0.2 | Entweder-Oder |

---

## 6. Grenznutzen-Tiers

| Tier | Benefits | MU | Beispiele |
|------|----------|-----|-----------|
| 1 Essential | 0.8-1.0 | Gehalt, KV, Pension |
| 2 Expected | 0.5-0.8 | FlexTime, HO, Weiterbildung |
| 3 Differentiating | 0.3-0.5 | Kinderbetreuung, Gym, ÖV |
| 4 Premium | 0.15-0.3 | Firmenauto, Private Schule |
| 5 Luxury | <0.1 oder negativ | Concierge, Privatjet |

**Stopp-Regel:** MU < 0.2

---

## 7. Validierung

```bash
# Portfolio validieren
python scripts/check_intervention_compliance.py --portfolio data/interventions/hr-retention-financial.yaml

# Einzelne Intervention validieren
python scripts/check_intervention_compliance.py data/interventions/hr-retention-financial.yaml
```

**Aktuelle Scores:**
- INT-HR-001 bis 004: 100% ✅
- INT-HR-005: 97% ✅
- INT-HR-006: 94% ✅
- INT-HR-007: 100% ✅

---

## 8. Nächste Schritte

### 8.1 Empfohlene Erweiterungen

1. **I_WHEN_t (Temporal) hinzufügen** für triggered Phase
   - z.B. "Onboarding Urgency" oder "Review Deadline"

2. **Pilotierung planen** mit `/intervention-manage new`
   - Predictions erfassen
   - KPIs definieren

3. **Measurement Framework** entwickeln
   - Baseline messen
   - Tracking-System aufsetzen

### 8.2 Nicht empfohlen

- ❌ I_WHO_o (Social/Recognition) hinzufügen → Crowding-Out mit I_WHAT_F
- ❌ I_HOW (Commitment/Goals) hinzufügen → Crowding-Out mit I_WHAT_F

### 8.3 Appendix-Integration (abgeschlossen)

Die Konzepte aus diesem Portfolio wurden in die EBF-Appendices integriert:

| Konzept | Appendix | Section |
|---------|----------|---------|
| Mental Identity Budgeting (I_WHAT_F→I_WHO) | HHH (METHOD-TOOLKIT) | Example 3: Type Transformation |
| Choice Architecture / Menu Sizing | HHH (METHOD-TOOLKIT) | Example 4: Menu Sizing |
| Benefits Complementarities (γ-Werte) | CMP (METHOD-COMP) | Worked Example: Benefits |
| Marginal Utility Analysis | CMP (METHOD-COMP) | Subsection: Marginal Utility |
| Identity Lock-In Mechanism | HHH (METHOD-TOOLKIT) | Example 3: Exit Rules |

**Kapitel-Integration:**
- Chapter 17: Beispiel 4 (Mental Identity Budgeting)
- Chapter 19: Choice Architecture Section
- Chapter 20: Beispiel 4 (HR Retention Portfolio)

---

## 9. Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│ HR RETENTION PORTFOLIO - QUICK REFERENCE                        │
├─────────────────────────────────────────────────────────────────┤
│ 7 Interventionen: I_AWARE, I_AWARE_k, I_WHEN, I_WHO, I_WHAT_F  │
│ Alle Journey-Phasen abgedeckt ✅                                │
│ Alle Segmente angesprochen ✅                                   │
│ Crowding-Out vermieden ✅                                       │
│                                                                 │
│ Kern-Innovation: Mental Identity Budgeting (INT-HR-007)         │
│ → Überstunden werden zu Purpose statt zu Verfall                │
│ → Aktiviert ALLE Segmente (σ > 1.0)                             │
│ → Identity Lock-In schafft Switching Costs                      │
│                                                                 │
│ Benefits Choice Box: 4 Kategorien × 3 Optionen = 12 sichtbar    │
│ Defaults: Smart Default nach Mitarbeiter-Profil                 │
│ Änderbar: 1x jährlich                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

*Generiert: 2026-01-19 | EBF Framework v1.7*
