# Customer experience measurement: Implications for customer loyalty

**Authors:** Francisco Villarroel Ordenes, Liliana Solis, Dennis Herhausen
**Book:** Handbook of Research on Customer Loyalty
**Editors:** Lerzan Aksoy, Alexander J. Buoye, Timothy L. Keiningham
**Year:** 2022
**Pages:** 187-202
**DOI:** 10.4337/9781800371637.00013
**Publisher:** Edward Elgar Publishing

---

## Abstract

This chapter addresses the customer experience (CX) measurement from a customer journey perspective and its implications for customer loyalty. We cover main CX conceptual aspects and a nomenclature composed of touchpoints, context, and qualities (TCQ). We then explain methods to extract CX insights from structured data and then from unstructured data, including text and non-textual data. Furthermore, we describe the main aspects of customer loyalty as an outcome metric. We offer a four-step framework to bridge the CX measurement and loyalty, and provide detailed guidance for research and practice.

**Keywords:** customer experience, CX measurement, touchpoints, context, qualities, TCQ framework, customer loyalty, attitudinal loyalty, behavioral loyalty, smooth journey, sticky journey, text mining

---

## Introduction

The importance of customer experience (CX) management has grown exponentially. CX is defined as:

> "The customer's subjective response to the holistic direct and indirect encounter with the firm, including but not necessarily limited to the communication encounter, the service encounter, and the consumption experience" (Lemke et al., 2011).

### The CX-Loyalty Connection

CX is intrinsically related to customer loyalty outcomes:
- Superior CX → Higher satisfaction → Increased loyalty
- Poor CX → Dissatisfaction → Defection and negative WOM

### Research Gap

Despite extensive CX research, a systematic framework linking CX measurement to loyalty metrics remains underdeveloped. This chapter bridges this gap.

---

## The TCQ Framework

### Touchpoints (T)

Interaction points between customers and firms. Classification:

| Type | Description | Examples |
|------|-------------|----------|
| **Retailer-owned** | Controlled by the firm | Website, stores, call centers |
| **Partner-owned** | Shared with partners | Distribution channels, co-branded services |
| **Customer-owned** | Controlled by customers | User-generated content, personal devices |
| **External** | Beyond firm control | Reviews, social media, competitors |

### Context (C)

Situational factors affecting CX:

| Dimension | Description | Examples |
|-----------|-------------|----------|
| **Social** | Who is present | Alone, with family, with strangers |
| **Temporal** | When it occurs | Morning, evening, busy periods |
| **Physical** | Where it happens | In-store, online, mobile |

### Qualities (Q)

Experience dimensions:

| Quality | Focus | Examples |
|---------|-------|----------|
| **Cognitive** | Thinking, beliefs | Understanding, learning |
| **Emotional** | Feelings | Joy, frustration, surprise |
| **Sensorial** | Senses | Visual appeal, sounds, textures |
| **Behavioral** | Actions | Ease of use, convenience |
| **Social** | Relationships | Belonging, community |

### TCQ Integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CX = f(Touchpoints × Context × Qualities)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TOUCHPOINTS        × CONTEXT           × QUALITIES                    │
│  ─────────────        ─────────           ───────────                   │
│  • Retailer-owned     • Social            • Cognitive                   │
│  • Partner-owned      • Temporal          • Emotional                   │
│  • Customer-owned     • Physical          • Sensorial                   │
│  • External                               • Behavioral                  │
│                                           • Social                      │
│                                                                         │
│  → Each touchpoint is experienced in a context with multiple qualities  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Data Modalities for CX Measurement

### 2×2 Data Matrix

| | **Static** | **Dynamic** |
|---|------------|-------------|
| **Structured** | Surveys, ratings, NPS | Clickstream, transactions, app usage |
| **Unstructured** | Reviews, social posts | Real-time chat, video, voice |

### Structured Data Methods

1. **Surveys:** Direct measurement of CX qualities
2. **Transaction data:** Behavioral proxies for CX
3. **Operational metrics:** Wait times, resolution rates

### Unstructured Data Methods

1. **Text mining:** Extracting CX insights from reviews, social media
2. **Sentiment analysis:** Emotional valence detection
3. **Topic modeling:** Identifying CX themes
4. **Machine learning:** Classification and prediction

---

## Customer Loyalty Metrics

### Attitudinal Loyalty

Internal, psychological commitment:

| Metric | Description |
|--------|-------------|
| **NPS** | Net Promoter Score (likelihood to recommend) |
| **Satisfaction** | Overall satisfaction with experience |
| **Commitment** | Emotional attachment to brand |
| **Trust** | Confidence in brand reliability |

### Behavioral Loyalty

Observable, action-based:

| Metric | Description |
|--------|-------------|
| **Share of Wallet** | Proportion of category spending |
| **Purchase Frequency** | Number of transactions per period |
| **Retention Rate** | Proportion of customers retained |
| **CLV** | Customer Lifetime Value |

### Attitudinal-Behavioral Relationship

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ATTITUDINAL → BEHAVIORAL                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  High Attitudinal + High Behavioral = TRUE LOYALTY (ideal)              │
│  High Attitudinal + Low Behavioral  = LATENT LOYALTY (barriers exist)   │
│  Low Attitudinal + High Behavioral  = SPURIOUS LOYALTY (inertia)        │
│  Low Attitudinal + Low Behavioral   = NO LOYALTY (at risk)              │
│                                                                         │
│  → Both metrics needed for complete picture                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Four-Step Framework: CX Measurement → Loyalty

### Step 1: Define Research Questions

Key questions to address:
- Which CX touchpoints matter most for loyalty?
- How does context moderate CX-loyalty relationship?
- Which CX qualities drive attitudinal vs. behavioral loyalty?

### Step 2: Identify Data Sources

Based on research questions, select appropriate data:

| Question Type | Recommended Data |
|---------------|------------------|
| Diagnostic (why?) | Unstructured (reviews, interviews) |
| Descriptive (what?) | Structured (surveys, transactions) |
| Predictive (future?) | Dynamic (clickstream, real-time) |

### Step 3: Extract CX Insights

Methods depend on data type:

| Data Type | Methods |
|-----------|---------|
| Structured | Regression, factor analysis, SEM |
| Unstructured text | Topic modeling, sentiment analysis, NLP |
| Unstructured non-text | Image recognition, video analysis |

### Step 4: Connect to Loyalty Metrics

Link CX insights to loyalty outcomes:

```
CX Insights → Attitudinal Metrics → Behavioral Metrics
              (NPS, Satisfaction)    (CLV, Retention)
```

---

## Journey Types: Smooth vs. Sticky

### Smooth Journeys

**Characteristics:**
- Goal-directed, instrumental
- Efficiency valued
- Quick resolution preferred
- Friction minimization critical

**Examples:** Banking, utilities, insurance claims

**Measurement focus:**
- Transaction efficiency
- Problem resolution time
- Ease of use

### Sticky Journeys

**Characteristics:**
- Experience-seeking, recreational
- Immersion valued
- Extended engagement preferred
- Emotional connection critical

**Examples:** Gaming, entertainment, hospitality

**Measurement focus:**
- Engagement depth
- Emotional resonance
- Social connection

### Comparison Table

| Aspect | Smooth Journey | Sticky Journey |
|--------|----------------|----------------|
| **Goal** | Complete task | Enjoy experience |
| **Time** | Minimize | Maximize |
| **Emotion** | Neutral/Positive | High positive |
| **Loyalty driver** | Convenience | Emotional bond |
| **Key metric** | Effort score | Engagement score |

---

## Implementation Examples

### Example 1: Gaming Industry (Sticky Journey)

**Context:** Online gaming platform

**Research question:** Which CX qualities drive player loyalty?

**Data sources:**
- In-game behavioral data (structured, dynamic)
- Player reviews and forums (unstructured, static)
- Real-time chat logs (unstructured, dynamic)

**CX insights extraction:**
- Topic modeling reveals importance of "social connection" and "achievement"
- Sentiment analysis shows emotional peaks during multiplayer events

**Loyalty connection:**
- Social CX qualities → Attitudinal loyalty (commitment to community)
- Achievement CX → Behavioral loyalty (session frequency, purchases)

### Example 2: Banking Industry (Smooth Journey)

**Context:** Retail banking services

**Research question:** How does app CX affect account retention?

**Data sources:**
- Transaction data (structured, dynamic)
- App store reviews (unstructured, static)
- Customer service interactions (unstructured, dynamic)

**CX insights extraction:**
- Clickstream analysis reveals friction points in fund transfers
- Review mining identifies "ease" and "speed" as key themes

**Loyalty connection:**
- Behavioral CX qualities → Attitudinal loyalty (satisfaction)
- Low effort → Behavioral loyalty (primary account status)

---

## Future Considerations

### Emerging Data Sources

1. **IoT devices:** Wearables, smart home data
2. **Voice assistants:** Conversational data
3. **Augmented reality:** Immersive experience data

### Methodological Advances

1. **Deep learning:** More accurate text and image analysis
2. **Real-time analytics:** Instant CX monitoring
3. **Causal inference:** Moving beyond correlation

### Integration Challenges

1. **Data privacy:** GDPR, CCPA compliance
2. **Data silos:** Connecting disparate sources
3. **Skill gaps:** Need for data science capabilities

---

## EBF Integration

### Theory Catalog

- **Category:** CAT-26 (Customer Experience & Journey Management)
- **Theory Support:** MS-CX-001 (TCQ Framework), MS-CJ-001 (Customer Journey Theory), MS-CJ-002 (Journey Segmentation)

### 10C Dimension Mapping

| Dimension | Application |
|-----------|-------------|
| **WHO** | Customers (data providers), Analysts (insight extractors), Marketers (action takers) |
| **WHAT** | TCQ Framework: Touchpoints × Context × Qualities → CX |
| **HOW** | Four-step process: Questions → Data → Insights → Loyalty |
| **WHEN** | Static vs. Dynamic data; Journey stage timing |
| **WHERE** | Cross-industry (gaming, banking examples) |
| **AWARE** | Explicit (surveys) vs. Implicit (text mining) CX measurement |
| **READY** | Data readiness: Structured (high) vs. Unstructured (capability needed) |
| **STAGE** | Pre-purchase, Purchase, Post-purchase touchpoint mapping |
| **HIERARCHY** | Attitudinal (higher order) → Behavioral (observable) loyalty |
| **EIT** | Tailor measurement to journey type; Combine data modalities |

---

## Key Takeaways

1. **TCQ provides systematic nomenclature** for CX measurement across touchpoints, contexts, and qualities

2. **Data modality choice matters:** Match data type to research question (diagnostic → unstructured, predictive → dynamic)

3. **Journey type determines measurement strategy:** Smooth journeys prioritize efficiency metrics; Sticky journeys prioritize engagement metrics

4. **Both loyalty types required:** Attitudinal loyalty predicts behavioral loyalty but both must be measured

5. **Text mining enables scale:** Unstructured data provides rich CX insights at scale

6. **Four-step framework operationalizes connection:** Research questions → Data → Insights → Loyalty metrics

---

## Citation

```bibtex
@incollection{PAP-ordenes2022cxmeasurement,
  title={Customer experience measurement: Implications for customer loyalty},
  author={Ordenes, Francisco Villarroel and Solis, Liliana and Herhausen, Dennis},
  booktitle={Handbook of Research on Customer Loyalty},
  editor={Aksoy, Lerzan and Buoye, Alexander J. and Keiningham, Timothy L.},
  pages={187--202},
  year={2022},
  publisher={Edward Elgar Publishing},
  doi={10.4337/9781800371637.00013}
}
```

---

*Source: Handbook of Research on Customer Loyalty, Edward Elgar Publishing*
*Archived: 2026-02-05*
*Content Level: L3 (Full chapter text)*
*Integration Level: I2 (STANDARD)*
