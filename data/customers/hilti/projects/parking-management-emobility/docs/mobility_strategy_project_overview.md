# Mobility Strategy Project Overview

**Quelle:** Hilti interne Praesentation, Mobility | December 2025
**Seiten:** 3-4 (Pt. 1 und Pt. 2)

---

## Pt. 1

### Project Sponsor / Management

- **Project Sponsor:** Jan Doongaji, Felix Hess
- **Project Manager:** Kim Koula
- **Project Owners:** Christian Ranacher

---

### Business Case & Description

#### Project Justification

Too many colleagues still drive alone to work, adding to traffic and emissions. By making public transport and active mobility more convenient, we can reduce peak-hour cars, support our CO2 sustainability goals, and improve the daily commute for our people — without introducing a general parking fee.

#### Project Description

We're improving mobility at HQ by making alternatives to solo car use easier and more comfortable. Key measures include a Public Transportation Abo, a new Buchs–Schaan shuttle, and an expanded e-bike offer — all supported by digital parking and mobility management tools.

---

### Objectives & Scope

#### Objectives

- Reduce up to 100 peak-hour cars at HQ in 2026.
- Increase use of public transport, e-bikes, and shared mobility.
- Prepare parking management for transparent, data-based access control.
- Raise awareness for sustainable commuting choices.
- Align with government mobility goals while enhancing employee comfort and experience.

#### In Scope

- All Headquarter's based team members located in Buchs, Schaan, Nendeln, and Bendern.
- External team members
- Apprentices / Interns

#### Out of Scope

- Visitors
- Facility-related Contractors

---

### Deliverables

Mobility Strategy, Public Transportation Abo, EcoPoints Exchange, Parking Management (Software & Hardware), Travel Infrastructure (E-bikes, Bus line)

---

### Key Milestones

| # | Milestone | Date |
|---|-----------|------|
| — | Start | Apr. 2025 |
| 1 | Scoping | Jul. 2025 |
| 2 | Mobility Strategy | Nov. 2025 |
| 3 | Go-live | May 2026 |
| — | Closing | Jun. 2026 |

---

### Status

| Dimension | Status |
|-----------|--------|
| Time | Gelb (Warnung) |
| Quality | Gruen |
| Budget | Gelb (Warnung) |

---

---

## Pt. 2

### Core Project Team

| Name | Role |
|------|------|
| Kim Koula | Project Manager Business |
| Timo Tello | IT Product Owner |
| Molli-Lynn Naji-Sepasgosar | Project Manager IT |
| Matej Preparc | IT Consultant |
| MK Yap | Solution Architect |
| Philipp Haeusle | Legal |
| Nicolas Thierry | Data Protection |
| Stefan Sanft | Project Manager Facilities |
| Karl-Michael Kinzl | Facilities Support |
| Elisabeth Gehrer | Tax |
| Judith Glueck | Procurement |
| Carolin Scholz | Communication |

---

### Project Tracking Elements

#### Project KPIs

- Reduction of 100 peak-hour cars (baseline 1,000)
- ≥100 new public transport or e-bike users by 2026
- Employee satisfaction with commuting comfort ≥80% (GEOS)

#### Risks (3 top)

- Government delays in subsidy/ticket approval.
- Technical integration challenges (EcoPoints–Interflex).
- Employee Frustration (decreased GEOS/GPTW).

#### Next steps (3 top)

- SteerCo decision on Swiss pilot (CHF 365 ticket)
- Finalize parking management setup and cost plan
- Launch awareness campaign and monitor modal-shift metrics

---

### Project Stakeholders

#### SteerCo

- Marion Keiper-Knorr (HR)
- Rohit Jain (IT)
- Gerrit Probst (MIT)

#### Stakeholders (Approval Status)

| Stakeholder | Status |
|-------------|--------|
| EB | Yes / No |
| SteerCo | Yes / No |
| HRLT | Yes / No |
| BU Heads | Yes / **No** |
| Region Heads | Yes / **No** |
| Legal | **Yes** / No |
| Tax | Yes / No |
| Finance | Yes / No |
| IT | **Yes** / No |
| TA Community | Yes / No |
| Rewards Community | **Yes** / No |
| TM Community | Yes / **No** |
| DEI Community | Yes / **No** |
| Team Members | Yes / **No** |

(Fettgedruckte Eintraege = markierte/hervorgehobene Antwort im Original)

---

---

## Current Model

**Quelle:** Hilti interne Praesentation, Mobility | December 2025

### Decision Tree: Parking Fee Structure

```
All HQ Employees
│
├── Residence: Switzerland
│   │
│   ├── 3-Laender Abo: Yes
│   │   │
│   │   ├── < 6 Parking Days (Monthly) → No Fees
│   │   │
│   │   └── > 6 Parking Days (Monthly) → CHF 10 / Day
│   │
│   └── 3-Laender Abo: No → No Fees
│
└── Residence: FL, AT, DE → No Fees
```

---

---

## Tariff Structure

**Quelle:** Hilti interne Praesentation, Mobility | December 2025

**Leitprinzip:** "Driving Remains an Option for All Employees at Any Time"

| Tariff | Name | Description | Parking Fee | Notes |
|--------|------|-------------|-------------|-------|
| **Tariff A** | Public Transportation Abo | Those who opt-in for 3-Laender Abo | Yes | Encourages sustainable commuting |
| **Tariff B** | (Default) | Those who do not qualify for Tariff C | No fee | Default category |
| **Tariff C** | Shift / Disability | Shift workers or team members with disability | No fee | — |
| **Tariff D** | Private Parking | Overnight or weekend parking (HIBAG only) | Yes (CHF 5/day) | — |

---

---

## MVP Parking Management at HQ

**Quelle:** Hilti interne Praesentation, Mobility | December 2025

### System Architecture Overview

#### Locations

- **Office West** — ca. 260 Parkplaetze
- **LCN** — ca. 280 Parkplaetze
- **HAG** — ca. 170 Parkplaetze

#### Systems & Data Flows

```
┌──────────────────────────────────────────────────────────────────────────┐
│  MVP PARKING MANAGEMENT - SYSTEM ARCHITECTURE                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────┐     ┌─────────────────┐     ┌────────────────┐          │
│  │  Calendar   │────►│  Benefits Portal │────►│   EcoPoints    │          │
│  │  (Booking)  │     │  (Abo Mgmt)     │     │   (Rewards)    │          │
│  └────────────┘     └────────┬────────┘     └───────┬────────┘          │
│                              │                       │                   │
│                              ▼                       ▼                   │
│                      ┌───────────────┐       ┌───────────────┐          │
│                      │   Interflex   │◄─────►│   SAP-web     │          │
│                      │   (Access     │       │   (Payroll /   │          │
│                      │    Control)   │       │    Deduction)  │          │
│                      └───────┬───────┘       └───────────────┘          │
│                              │                                           │
│               ┌──────────────┼──────────────┐                           │
│               ▼              ▼              ▼                           │
│        ┌────────────┐ ┌────────────┐ ┌────────────┐                    │
│        │ Office West│ │    LCN     │ │    HAG     │                    │
│        │ ~260 spots │ │ ~280 spots │ │ ~170 spots │                    │
│        └────────────┘ └────────────┘ └────────────┘                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

#### Key System Interactions

| System | Function | Integration |
|--------|----------|-------------|
| **Calendar** | Parking day booking / reservation | → Benefits Portal |
| **Benefits Portal** | Abo management, opt-in/opt-out | → Interflex, EcoPoints |
| **Interflex** | Physical access control (barriers, gates) | ← Benefits Portal, → SAP-web |
| **EcoPoints** | Reward system for sustainable commuting | ← Benefits Portal |
| **SAP-web** | Payroll deduction for parking fees | ← Interflex |

#### Process Flow

1. **Employee** books parking day via **Calendar**
2. **Benefits Portal** manages Abo status (Tariff A/B/C/D)
3. **Interflex** controls physical access at parking locations
4. Parking fee data flows from Interflex to **SAP-web** for payroll deduction
5. Sustainable commuting behavior earns rewards via **EcoPoints**

---

---

## 2026 Mobility Shift: Comfort + Flexibility + Fairness

**Quelle:** Seite 8

**Single-occupancy cars down from 61% to 54% — validates readiness to shift.**

### Goal

- Reduce **~100 peak-hour cars** at Hilti HQ in 2026
- Enable commuting by **comfort, not habit**
- Provide a **fair and attractive mobility offering**

### Barriers

- Public transport **slower** or less predictable than car
- Switzerland **higher price** vs AT (~EUR 400) & LI (~CHF 370) vs. CH (~CHF 1'800–3'000)
- Employees need **flexibility** — not "all or nothing" switch
- Benchmark today = **drive to the door**

### What We Deliver

| Measure | Impact |
|---------|--------|
| **New Buchs–Hilti Bus Line 28 (LIEMobil)** | Avoids peak traffic; impact ~20 cars |
| **E-bike Expansion (LIEMobil)** | Door-to-door comfort; impact ~10 cars |
| **EcoPoints Exchange** | Incentivized sustainable commuting |
| **3-Country Public Transport Ticket + 300 CHF REKA (OSTWind)** | Levels CH price gap; impact ~40–120 cars |

### How We Govern It

- **Interflex chip** issued to all drivers
  - Enables policy fairness & transparency
- **OSTWind Ticket Rule:**
  - Hilti subsidizes the ticket (~300K)
  - Parking fee **CHF 10/day after 6 flex days/month**
  - Provides **flexibility + accountability**

### Expected Impact

- ~100 peak-hour cars
- Lower CO2 footprint (currently 1.97 CO2 per TM)
- Clear, attractive mobility offering for employees
- Hilti positioned as regional sustainability leader

> **"We shift mobility by closing the comfort gap — not by pushing behavioral change."**

---

---

## Key Messages

**Quelle:** Seite 11

|  | **Purpose & Impact** | **Closing the Comfort Gap** | **Infrastructure & Awareness** |
|---|---|---|---|
| **Behavior Change Through Comfort** | Reducing solo-car use is essential. Our ambition is to **remove ~100 cars** by making sustainable options more attractive than driving. | We must make public transport, cycling, and **shared modes more comfortable** — and reduce solo-car advantages where needed. | **Convenience shapes behavior.** Today's "park close to the entrance" standard must shift toward more sustainable comfort options. |
| **Shared Responsibility & Partnership** | Mobility shifts succeed only when Hilti, employees, the community and authorities **work together** toward better daily commuting choices. | **New bus line 28**, e-bikes, and the **3-Laender ticket** for Swiss-based team members improve comfort and remove cars from peak-hour traffic. | Hilti, employees, the community and authorities must build **reliable infrastructure** and fair incentives for all commuting modes. |
| **Data-Driven & Future-Ready** | Comfort — not enforcement — guides us. Data ensures we **invest smartly** and stay prepared for future mobility requirements. | Understanding commuting flows helps us **close comfort gaps** and deploy the right solutions at the right time. | Parking management (EcoPoints & Interflex) and awareness campaigns will enable **fair policies** and informed mobility choices. |

---

---

## Timeline & Major Milestones

**Quelle:** Seite 19

### Phase Overview

| Phase | Zeitraum | Status |
|-------|----------|--------|
| **Scope** | Q1/Q2 2025 | Complete |
| **Concept** | Q3/Q4 2025 | In progress |
| **Solution** | Q4 2025 / January 2026 | In progress |
| **Communication & Launch prep** | Q1 2026 | Not started |
| **Rollout & Closing** | April 2026 | Not started |

### Milestones per Phase

#### Scope (Q1/Q2 2025) — Complete

- Project Start
- Project Team Established
- Parking Management: Scope Hardware
- EcoPoints Exchange

#### Concept (Q3/Q4 2025) — In progress

- Mobility Strategy Sign-off
- Parking Management: Scope Software
- Software: Project Order
- Public Transportation Abo & Infrastructure Negotiations

#### Solution (Q4 2025 / January 2026) — In progress

- Software: EA Security Review
- Change Management: Strategy Communication
- Software: DPA Signed
- Software: Cloud Board Approval

#### Communication & Launch prep (Q1 2026) — Not started

- Change Management: Public Transportation Abo
- Change Management: Parking Management
- Pilot Project

#### Rollout & Closing (April 2026) — Not started

- Go-live
- Customer Service
- Reporting

---

---

## Tariff Variants (Detail)

**Quelle:** Seite 29

### Tariff Definitions

| Tariff | Who | What | Charging Model |
|--------|-----|------|----------------|
| **Tariff A** – Public Transport | Eligible only for Swiss residents who opt in for Public Transport Abo | Parking with Public Transport Abo | 6 flex days (0 payment), after that CHF 10/day |
| **Tariff B** – Office Workers | All office workers in all locations | Parking during normal working hours | CHF 0/day |
| **Tariff C** – Shift Workers | All shift workers in all locations | Parking during normal working hours | CHF 0/day |
| **Tariff D** – Private Parking | Office West employees | Parking at Office West overnight, on holidays or weekends | CHF 5/day |

### Example and Possible Tariff Combinations

#### Office Tariffs

| Combination | Description |
|-------------|-------------|
| **B** | Office workers without public transport abo or any additional parking use cases. |
| **B + A** | Office workers with public transport abo but no private parking. |
| **B + D** | Office workers without public transport abo, and uses private parking in Office West. |
| **B + A + D** | Office workers with public transport abo, and uses private parking in Office West. |

#### Shift Tariffs

| Combination | Description |
|-------------|-------------|
| **C** | Shift workers without public transport abo or any additional parking use cases. |
| **C + A** | Shift workers with public transport abo but no private parking. |
| **C + D** | Shift workers without public transport abo, and uses private parking in Office West. |
| **C + A + D** | Shift workers with public transport abo, and uses private parking in Office West. |

---

---

## Our Focus: Our Path to 100 Fewer Peak-Hour Cars

**Quelle:** Seite 34

### Purpose & Ambition

- **Goal:** Achieve a reduction of around 100 peak-hour cars at Hilti HQ in 2026.
- **Context:** A 1% reduction in Liechtenstein equals ~400 fewer cars; Hilti's share ≈ 20.
- **Focus:** Shift from "driving by habit" to "choosing by comfort."
- **Insight:** The real barrier is comfort, not cost — driving and parking at the door remain today's benchmark.

### Insights by Country

| Country | Barrier | Annual Cost | Key Insight |
|---------|---------|-------------|-------------|
| **Austria (AT)** ~700 TM | Comfort | ~EUR 400 | Already strong OeV use |
| **Liechtenstein (LI)** ~500 TM | Comfort | ~CHF 370 | OeV slower than car |
| **Switzerland (CH)** ~900 TM | Price and comfort | ~CHF 2'000–3'000 | OeV same as traffic, high cost |

### Closing the Comfort Gap

| Measure | Expected Impact |
|---------|-----------------|
| **Additional Connections** — Buchs–Hilti Bus Line (LIEMobil) avoiding traffic | ~20 cars reduced |
| **E-bike Expansion (LIEMobil)** | ~10 cars reduced |
| **EcoPoints Exchange** | Awareness, e.g. carpooling |
| **Public Transportation Abo (3-Country Ticket)** | ~40–120 conversions expected |

→ **Comfort ↑ Alternatives | Comfort ↓ Solo Car**

### Pre-requisite from the Government

Prepare our infrastructure for parking management.

Parking management helps us organize how cars are used on campus. To offer the Public Transportation Abo (3-Country Ticket), we need to pay a fixed fee, which is largely supported by the state. To keep this system fair, anyone who chooses the Abo will pay a daily parking fee of CHF 10 if they still come to work by car.

---

---

## Shaping the Future of Mobility — Easing Today's Commutes, Enabling Tomorrow's Sustainability

**Quelle:** Seite 35

Every day, over **20'000 cross-border commuters** travel into Liechtenstein — including **~1'500 Hilti team members**.

Our goal is clear: **reduce ~100 solo cars during peak hours** by making sustainable alternatives more comfortable and convenient than driving.

The mobility strategy aims to build a sustainable, healthier commuting ecosystem that:

- encourages **multimodal and flexible** transport choices,
- improves **comfort and reliability** for daily commuters,
- promotes **equitable access** for all employees, and
- reduces **congestion** and eases pressure on Liechtenstein's infrastructure.

By doing so, we reduce carbon emissions (Scope 3) and contribute to our global ambition of reaching **net zero by 2050**.

---

---

## Driving Remains an Option for All Employees at Any Time

**Quelle:** Seite 22

Each user is assigned a **base tariff group (B or C)**. Only those who opt in for the Public Transport Abo are subject to parking management fees.

| Tariff | Who it Applies To | Parking Management Fee | Purpose / Notes |
|--------|-------------------|------------------------|-----------------|
| **Tariff A** – Public Transportation Abo | Those who opt-in for the 3-Laender Abo. | **Yes** | Encourages sustainable commuting; small parking management fee reflects shared system costs. **Flex parking:** 6 days/month: MSQ tariff C/D (CHF 0), 6+ uses per month: CHF 10/day |
| **Tariff B** | Those who do not qualify for Tariff C. | **No** | Default category. Registered in the system and receive a chip, but no fee applies at this stage. |
| **Tariff C** – Shift / Disability | Shift workers or team members with a disability. | **No** | Recognizes operational or physical needs. Registered in the system and receive a chip, but no fee applies at this stage. |
| **Tariff D** – Private Parking | Those who require overnight or weekend parking. (HIBAG only) | **Yes** | TBD: HIBAG Only CHF 5/day |

> **"Our strategy remains evidence-based, fair, and flexible — evolving with real commuting behavior rather than assumptions."**
