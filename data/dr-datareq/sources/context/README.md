# Context Data

> Kontextdaten für Ψ-Dimensionen (Verhaltensökonomische Kontextvektoren)

## Struktur

```
context/
├── ch/                   ← Schweiz-spezifische Kontextvektoren
│   ├── BCM2_04_KON_institutional_political.yaml  ← 59 Faktoren
│   ├── BCM2_04_KON_socio_cultural.yaml           ← 178 Faktoren (inkl. REG)
│   ├── BCM2_XX_*.yaml   ← Weitere BCM-Achsen
│   └── ...
├── at/                   ← Österreich-spezifische Kontextvektoren
├── de/                   ← Deutschland-spezifische Kontextvektoren
└── global/               ← Länderübergreifende Kontextvektoren
    ├── BCM2_05_IND_individual.yaml        ← 48 Faktoren (Person, Psyche, Zustand)
    ├── BCM2_06_META_decision.yaml         ← 42 Faktoren (Framing, Defaults, Channel)
    └── BCM2_10_SPT_sports_prediction.yaml ← 18 Faktoren (xG, Biases, Market)
```

## BCM Kontextvektor-System

Das BCM2 (Behavioral Context Model) System definiert mehrere Achsen:

| Code | Achse | Faktoren | Beschreibung |
|------|-------|----------|--------------|
| BCM2_04_KON | Institutionell-Politisch | 59 | Politik, Governance, Justiz, Sicherheit |
| BCM2_04_KON | Sozio-Kulturell | 178 | Kultur, Religion, Regionale Unterschiede (REG) |
| BCM2_05_IND | Individual | 48 | Demografie, Psychografie, Zustand, Motivation |
| BCM2_06_META | Meta Decision | 42 | Framing, Defaults, Channel, Timing, Incentives |
| BCM2_03_IDN | Identitätsnutzen | TBD | Kulturelle Identität, Werte |
| BCM2_02_KNU | Kollektiver Nutzen | TBD | Gesellschaftlicher Beitrag |
| BCM2_10_SPT | Sports Prediction | 18 | xG-Metriken, Behavioral Biases, Marktkontext |
| BCM2_01_* | Weitere Achsen | TBD | ... |

## YAML-Schema

Jede Kontextvektor-Datei folgt diesem Schema:

```yaml
metadata:
  name: "Achsen-Name"
  code: "BCM2_XX_YYY"
  total_factors: 59
  sub_axes: 5
  bcm_coupling:
    primary: "BCM2_XX_XXX"
    secondary: "BCM2_YY_YYY"

summary:
  trends:
    steigend: 42
    fallend: 5
    stabil: 12

AXIS_CODE:
  name: "Unterachsen-Name"
  factors:
    - id: CH-AXIS-01
      name: "Faktor-Name"
      definition: "Kurzdefinition"
      trend: "steigend|fallend|stabil"
      uncertainty: "gering|mittel|hoch"
```

## EBF-Integration

Diese Kontextdaten kalibrieren die Ψ-Dimensionen:

| BCM-Achse | EBF Ψ-Dimension | Verwendung |
|-----------|-----------------|------------|
| BCM2_04_KON (POL, GOV, JUS, ORG, MIL) | κ_INST | Institutionelles Vertrauen |
| BCM2_03_IDN | κ_SOCIAL | Soziale Identität |
| BCM2_02_KNU | κ_SOCIAL | Kollektive Normen |

## Aktualisierung

1. YAML-Datei im entsprechenden Länderordner bearbeiten
2. Trend/Unsicherheit aktualisieren
3. In Appendix DR referenzieren
4. Commit mit: `chore(context): Update BCM2_XX_YYY`

## Quelle

FehrAdvice Kontextvektor System (Beatrix 2.0)
