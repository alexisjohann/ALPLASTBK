# ALPLA Plant Comparability Index (PCI)
## Methodik zur Werkskategorisierung für Feldexperimente

**Version:** 1.0
**Datum:** 2026-01-19
**Autor:** Strategic Analysis Team (EBF Framework)
**Anwendungsfall:** Churn-Reduktion Feldexperiment

---

## 1. Executive Summary

Der **Plant Comparability Index (PCI)** ist eine quantitative Methodik zur Messung der strukturellen Ähnlichkeit zwischen Produktionswerken. Er ermöglicht:

1. **Valide Vergleiche** zwischen Werken für Feldexperimente
2. **Ökonometrische Kontrolle** von Confounding-Variablen
3. **Matched-Pairs-Design** für Treatment/Control-Zuordnung
4. **Cluster-Bildung** für Fixed-Effects-Schätzungen

---

## 2. Theoretischer Rahmen

### 2.1 Problem

Bei Feldexperimenten in Multi-Site-Organisationen wie ALPLA besteht die Gefahr, dass beobachtete Effekte durch strukturelle Unterschiede zwischen Werken verzerrt werden (Selection Bias, Confounding).

### 2.2 Lösung

Der PCI quantifiziert die multidimensionale Distanz zwischen Werken auf Basis relevanter Vergleichsdimensionen. Werke mit niedrigem PCI sind strukturell ähnlich und daher besser vergleichbar.

### 2.3 Mathematische Definition

$$
PCI(i,j) = \sqrt{\sum_{k=1}^{K} w_k \cdot \left(\frac{X_{ik} - X_{jk}}{\sigma_k}\right)^2}
$$

wobei:
- $PCI(i,j)$ = Distanz zwischen Werk $i$ und Werk $j$
- $w_k$ = Gewicht der Dimension $k$ (normalisiert: $\sum w_k = 1$)
- $X_{ik}$ = Wert von Werk $i$ auf Dimension $k$
- $\sigma_k$ = Standardabweichung der Dimension $k$ über alle Werke

**Interpretation:**
- $PCI = 0$: Identische Werke
- $PCI < 0.5$: Hohe Vergleichbarkeit (innerhalb 0.5 SD)
- $PCI > 1.0$: Geringe Vergleichbarkeit

---

## 3. SLOP-Dimensionsframework

### 3.1 Übersicht

Das Framework umfasst **20 Dimensionen** in **4 Kategorien**:

| Code | Kategorie | Anzahl | Rationale für Churn |
|------|-----------|--------|---------------------|
| **S** | Strukturell | 6 | Arbeitsbedingungen, physische Umgebung |
| **L** | Labor Market | 5 | Externe Alternativen, Wettbewerb um Talent |
| **O** | Organisatorisch | 5 | Management, Kultur, HR-Praktiken |
| **P** | Performance | 4 | Baseline-Zustand vor Intervention |

### 3.2 S: Strukturelle Faktoren

| ID | Dimension | Operationalisierung | Skala | Gewicht | Quelle |
|----|-----------|---------------------|-------|---------|--------|
| S1 | Werkstyp | In-House=1, Near-Customer=2, Standalone=3 | Kategorial | 0.15 | Intern |
| S2 | Werksgröße | Anzahl Mitarbeiter (FTE) | Kontinuierlich | 0.12 | HR |
| S3 | Werksalter | Jahre seit Eröffnung | Kontinuierlich | 0.08 | Intern |
| S4 | Technologie-Komplexität | (EBM×1 + SBM×2 + IM×3) / Linien | Index 1-3 | 0.07 | Ops |
| S5 | Automatisierungsgrad | % automatisierte Prozesse | 0-100% | 0.05 | Ops |
| S6 | Schichtmodell | 1-Schicht=1, 2-Schicht=2, 3-Schicht=3, Konti=4 | Ordinal | 0.08 | HR |

**Rationale:** Strukturelle Faktoren beeinflussen die Arbeitsbedingungen direkt (Schichtarbeit, Automatisierung) und indirekt (Werkskultur in etablierten vs. neuen Werken).

### 3.3 L: Labor Market Faktoren

| ID | Dimension | Operationalisierung | Skala | Gewicht | Quelle |
|----|-----------|---------------------|-------|---------|--------|
| L1 | Arbeitslosenquote | County-Level Unemployment Rate | % | 0.10 | BLS LAUS |
| L2 | Mfg. Wettbewerbsdichte | # Mfg. Establishments im 30-mi-Radius | Count | 0.08 | Census CBP |
| L3 | Urbanisierung | Rural=1, Suburban=2, Urban=3 | Kategorial | 0.05 | Census |
| L4 | Lohnniveau Region | Median Hourly Wage Mfg. (MSA) | $/hr | 0.07 | BLS OES |
| L5 | Cost of Living | COLI Index (100 = US avg) | Index | 0.05 | C2ER |

**Rationale:** Externe Arbeitsmarktbedingungen beeinflussen die Attraktivität von Alternativen und damit die Churn-Wahrscheinlichkeit.

### 3.4 O: Organisatorische Faktoren

| ID | Dimension | Operationalisierung | Skala | Gewicht | Quelle |
|----|-----------|---------------------|-------|---------|--------|
| O1 | Kundenkonzentration | % Revenue von Top-Kunde | % | 0.06 | Finance |
| O2 | Plant Manager Tenure | Jahre im Amt | Jahre | 0.05 | HR |
| O3 | HR-Präsenz | Dedizierter HR vor Ort (0/1) | Binär | 0.04 | HR |
| O4 | Gewerkschaftsstatus | Union=1, Non-Union=0 | Binär | 0.05 | HR |
| O5 | Training-Intensität | Trainingsstunden / MA / Jahr | Stunden | 0.04 | HR |

**Rationale:** Organisatorische Faktoren reflektieren Management-Qualität und HR-Praktiken, die Churn direkt beeinflussen.

### 3.5 P: Performance-Baseline

| ID | Dimension | Operationalisierung | Skala | Gewicht | Quelle |
|----|-----------|---------------------|-------|---------|--------|
| P1 | Baseline Churn | 12M Rolling Turnover Rate | % | 0.12 | HR |
| P2 | Absentismus | Unplanned Absence Rate | % | 0.06 | HR |
| P3 | Sicherheit | TRIR (Total Recordable Incident Rate) | Rate | 0.04 | EHS |
| P4 | Produktivität | Output / FTE (indexed, 100=avg) | Index | 0.04 | Ops |

**Rationale:** Baseline-Performance erlaubt Regression-to-Mean-Kontrolle und identifiziert systematische Unterschiede.

### 3.6 Gewichtungslogik

Die Gewichte wurden basierend auf empirischer Evidenz zur Churn-Prädiktionskraft festgelegt:

```
Höchste Gewichte (>0.10):
├── S1 Werkstyp (0.15)      → In-House vs. Standalone sehr unterschiedlich
├── S2 Werksgröße (0.12)    → Größe korreliert mit Anonymität/Kultur
├── P1 Baseline Churn (0.12) → Stärkster Prädiktor für zukünftigen Churn
└── L1 Arbeitslosenquote (0.10) → Externe Optionen entscheidend

Mittlere Gewichte (0.05-0.10):
├── S3 Werksalter (0.08)
├── S6 Schichtmodell (0.08)
├── L2 Mfg. Wettbewerbsdichte (0.08)
├── L4 Lohnniveau (0.07)
├── S4 Technologie-Komplexität (0.07)
├── P2 Absentismus (0.06)
├── O1 Kundenkonzentration (0.06)
└── Übrige (0.04-0.05 jeweils)

Summe: 1.00
```

---

## 4. Datenerhebung

### 4.1 Primärdaten (ALPLA-intern)

Diese Daten müssen von ALPLA HR/Operations bereitgestellt werden:

```yaml
plant_data_template:
  plant_id: "string"
  plant_name: "string"

  # S: Strukturell
  S2_employees_fte: int
  S3_opening_year: int
  S4_technology_mix:
    ebm_lines: int
    sbm_lines: int
    im_lines: int
  S5_automation_percent: float  # 0-100
  S6_shift_model: int  # 1, 2, 3, or 4

  # O: Organisatorisch
  O1_top_customer_revenue_pct: float  # 0-100
  O2_plant_manager_tenure_years: float
  O3_dedicated_hr_onsite: bool
  O4_union_status: bool
  O5_training_hours_per_employee: float

  # P: Performance
  P1_churn_rate_12m: float  # annualized %
  P2_absence_rate: float  # %
  P3_trir: float  # incidents per 200,000 hours
  P4_productivity_index: float  # 100 = company average
```

### 4.2 Sekundärdaten (Öffentlich)

Diese Daten können aus öffentlichen Quellen bezogen werden:

| Dimension | Quelle | URL | Granularität |
|-----------|--------|-----|--------------|
| L1 | BLS LAUS | data.bls.gov | County, monatlich |
| L2 | Census CBP | census.gov/data/datasets/cbp | County, jährlich |
| L3 | Census Urban/Rural | census.gov | Census Tract |
| L4 | BLS OES | bls.gov/oes | MSA, jährlich |
| L5 | C2ER COLI | coli.org | MSA, quarterly |

### 4.3 Abgeleitete Variablen

| Variable | Berechnung |
|----------|------------|
| S1 Werkstyp | Klassifikation basierend auf Kunden-Proximity |
| S4 Tech-Index | $(EBM×1 + SBM×2 + IM×3) / (EBM + SBM + IM)$ |

---

## 5. Berechnungsverfahren

### 5.1 Schritt 1: Datenaufbereitung

```python
import pandas as pd
import numpy as np

def prepare_data(df_raw):
    """
    Aufbereitung der Rohdaten für PCI-Berechnung
    """
    df = df_raw.copy()

    # Kategoriale Variablen dummy-kodieren
    df['S1_inhouse'] = (df['S1_type'] == 'in-house').astype(int)
    df['S1_near_customer'] = (df['S1_type'] == 'near-customer').astype(int)
    df['L3_urban'] = (df['L3_urbanization'] == 'urban').astype(int)
    df['L3_suburban'] = (df['L3_urbanization'] == 'suburban').astype(int)

    # Kontinuierliche Variablen z-standardisieren
    continuous_vars = ['S2', 'S3', 'S4', 'S5', 'S6',
                       'L1', 'L2', 'L4', 'L5',
                       'O1', 'O2', 'O5',
                       'P1', 'P2', 'P3', 'P4']

    for var in continuous_vars:
        df[f'{var}_z'] = (df[var] - df[var].mean()) / df[var].std()

    return df
```

### 5.2 Schritt 2: PCI-Matrix berechnen

```python
def calculate_pci_matrix(df, weights):
    """
    Berechnet N×N Matrix der paarweisen PCI-Distanzen
    """
    n = len(df)
    pci_matrix = np.zeros((n, n))

    variables = list(weights.keys())

    for i in range(n):
        for j in range(i+1, n):
            dist_sq = 0
            for var in variables:
                diff = df.iloc[i][f'{var}_z'] - df.iloc[j][f'{var}_z']
                dist_sq += weights[var] * (diff ** 2)

            pci = np.sqrt(dist_sq)
            pci_matrix[i, j] = pci
            pci_matrix[j, i] = pci

    return pd.DataFrame(pci_matrix,
                        index=df['plant_id'],
                        columns=df['plant_id'])
```

### 5.3 Schritt 3: Matching-Algorithmus

```python
def find_matched_pairs(pci_matrix, treatment_plants, threshold=0.5):
    """
    Findet für jedes Treatment-Werk das beste Control-Werk

    Args:
        pci_matrix: DataFrame mit PCI-Distanzen
        treatment_plants: Liste der Treatment-Werk-IDs
        threshold: Max. akzeptable PCI-Distanz

    Returns:
        List of tuples: [(treatment_id, control_id, pci_distance), ...]
    """
    control_plants = [p for p in pci_matrix.index if p not in treatment_plants]
    matched_pairs = []
    used_controls = set()

    for t_plant in treatment_plants:
        # Finde nächstes verfügbares Control-Werk
        distances = pci_matrix.loc[t_plant, control_plants]
        distances = distances[~distances.index.isin(used_controls)]

        if len(distances) == 0:
            print(f"Warning: Kein Control für {t_plant} verfügbar")
            continue

        best_control = distances.idxmin()
        best_distance = distances.min()

        if best_distance <= threshold:
            matched_pairs.append((t_plant, best_control, best_distance))
            used_controls.add(best_control)
        else:
            print(f"Warning: Bestes Match für {t_plant} überschreitet Threshold: {best_distance:.2f}")

    return matched_pairs
```

---

## 6. Qualitätsprüfung

### 6.1 Balance-Diagnostik

Nach dem Matching muss die Balance zwischen Treatment- und Control-Gruppe geprüft werden:

| Metrik | Formel | Akzeptabel |
|--------|--------|------------|
| **Standardized Mean Difference (SMD)** | $(μ_T - μ_C) / σ_{pooled}$ | \|SMD\| < 0.1 |
| **Variance Ratio** | $σ²_T / σ²_C$ | 0.8 < VR < 1.25 |
| **KS-Statistik** | $\max|F_T(x) - F_C(x)|$ | p > 0.05 |

### 6.2 Sensitivitätsanalyse

Die Robustheit der Ergebnisse sollte geprüft werden durch:

1. **Alternative Gewichtungen**: ±20% Variation der Gewichte
2. **Subset-Analyse**: Nur Top-50% vergleichbarste Paare
3. **Ausschluss einzelner Dimensionen**: Leave-one-out

---

## 7. Anwendung auf ALPLA USA

### 7.1 Die 17 US-Werke

| # | Werk | Adresse | Bekannte Attribute |
|---|------|---------|-------------------|
| 1 | McDonough, GA | 289 Highway 155 S, 30253 | HQ, Standalone, Groß |
| 2 | Bethlehem, PA | 2120 Spillman Dr, 18015 | Standalone, 2017 |
| 3 | Iowa City, IA (1) | 2258 Heinz Rd, 52240 | Near-P&G, 2003 |
| 4 | Iowa City, IA (2) | 2309 Heinz Rd, 52240 | Near-P&G |
| 5 | Jefferson City, MO | 2662 Militia Dr, 65101 | Standalone |
| 6 | St. Peters, MO (1) | 1 Gerber Industrial Dr, 63376 | Standalone, 2010 |
| 7 | St. Peters, MO (2) | 9 Cermak Blvd, 63376 | Standalone |
| 8 | Kansas City, MO | Blue River Commerce Ctr | Standalone, 2022 |
| 9 | Bowling Green, KY (1) | 215 Technology Way, 42101 | Standalone, 2013 |
| 10 | Bowling Green, KY (2) | 377 Southwood Ct, 42101 | **In-House Henkel**, 2020 |
| 11 | Florence, KY (1) | 7080 New Buffington Rd, 41042 | **In-House L'Oréal** |
| 12 | Florence, KY (2) | 7979 Vulcan Dr, 41042 | **In-House L'Oréal** |
| 13 | Lima, OH | 3320 Fort Shawnee Industrial Dr, 45806 | Standalone, 2006 |
| 14 | Dayton, OH | West National Rd (Park 70/75) | Standalone, 2019 |
| 15 | Salt Lake City, UT | 4324 Commercial Way Suite A, 84104 | Standalone, Klein, 2018 |
| 16 | Houston, TX | 5800 Armour Dr | Near-Clorox, 2001 |
| 17 | West Bend, WI | 825 Rail Way, 53095 | Standalone, Klein, 2017 |

### 7.2 Vorläufige Cluster-Hypothese

Basierend auf S1 (Werkstyp) ergeben sich drei natürliche Cluster:

**Cluster A: In-House (n=3)**
- Bowling Green (2) - Henkel
- Florence (1) - L'Oréal
- Florence (2) - L'Oréal

**Cluster B: Near-Customer (n=3)**
- Iowa City (1) - P&G
- Iowa City (2) - P&G
- Houston - Clorox

**Cluster C: Standalone (n=11)**
- Alle übrigen Werke

### 7.3 Empfohlenes Experiment-Design

Für ein Churn-Reduktions-Experiment mit komplementärem Maßnahmen-Mix:

```
Option A: Within-Cluster Design
├── Treatment: 1-2 Werke pro Cluster
├── Control: Remaining Werke im gleichen Cluster
└── Vorteil: Maximale Vergleichbarkeit

Option B: Matched-Pairs Design
├── Berechne PCI für alle 17×16/2 = 136 Paare
├── Wähle T Treatment-Werke (z.B. T=5)
├── Matche mit Control-Werken (PCI < 0.5)
└── Vorteil: Optimale Balance

Option C: Stepped Wedge
├── Rollout in 4 Wellen über 12 Monate
├── Alle Werke erhalten Treatment (sequentiell)
├── Zeitliche Variation = Identifikation
└── Vorteil: Keine "verlorenen" Controls
```

---

## 8. Limitationen

1. **Unbeobachtete Heterogenität**: PCI kontrolliert nur beobachtbare Faktoren
2. **Zeitliche Stabilität**: Labor-Market-Faktoren können sich ändern
3. **Interdependenzen**: Werke im gleichen Cluster könnten interagieren (Spillover)
4. **Gewichtungsunsicherheit**: Optimale Gewichte sind nicht bekannt

---

## 9. Referenzen

- Rosenbaum, P. R., & Rubin, D. B. (1983). The central role of the propensity score in observational studies for causal effects. *Biometrika*, 70(1), 41-55.
- Stuart, E. A. (2010). Matching methods for causal inference: A review and a look forward. *Statistical Science*, 25(1), 1-21.
- Imbens, G. W., & Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.

---

## 10. Anhänge

### Anhang A: Daten-Template (YAML)

Siehe `data/alpla-pci-data-template.yaml`

### Anhang B: Python-Implementation

Siehe `scripts/calculate_pci.py`

### Anhang C: Arbeitsmarktdaten USA

Siehe `data/alpla-usa-labor-market-data.csv`

---

**Dokumentversion:** 1.0
**Nächste Review:** Nach Datenerhebung
**Kontakt:** Strategic Analysis Team
