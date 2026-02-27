# Context Vector Architecture (CVA)
## 3-Stufen Choice Architecture für Unternehmenskontexte

**Version:** 1.0.0
**Erstellt:** 2026-01-27
**Status:** SSOT (Single Source of Truth)
**Framework:** EBF v54+

---

## Übersicht

Die Context Vector Architecture (CVA) definiert **drei Stufen** für Unternehmenskontextvektoren im EBF Framework. Jede Stufe hat einen spezifischen Use Case, Umfang und Struktur.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONTEXT VECTOR ARCHITECTURE (CVA) - 3 STUFEN                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  STUFE 1          STUFE 2              STUFE 3                              │
│  SCHNELL          STANDARD             VERTIEFT                             │
│  ~30 Faktoren     400 Faktoren         400+ Faktoren                        │
│                                                                             │
│  ┌─────────┐      ┌─────────────┐      ┌─────────────────┐                  │
│  │ 1 YAML  │      │  8 YAMLs    │      │  8 YAMLs        │                  │
│  │         │  →   │  + Master   │  →   │  + Vertiefungen │                  │
│  │ MIKRO   │      │  customers/ │      │  + Spezial-DBs  │                  │
│  └─────────┘      └─────────────┘      └─────────────────┘                  │
│                                                                             │
│  Use Case:        Use Case:            Use Case:                            │
│  Quick Assess     Vollprojekt          Langzeit-Mandat                      │
│  Pitch            Strategie            Transformation                       │
│  Screening        Intervention         M&A Due Diligence                    │
│                                                                             │
│  Zeit: 2-4h       Zeit: 1-2 Tage       Zeit: 1-2 Wochen                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Stufe 1: SCHNELL (~30 Faktoren)

### Definition
Kompakter Kontextvektor für schnelle Assessments und Pitches. Fokus auf Ψ-Dimensionen und Kernsegmente.

### Struktur
```
data/dr-datareq/sources/clients/<kunde>/external/
└── BCM2_MIKRO_<KUNDE>_context.yaml    # ~30-50 Faktoren, 1 Datei
```

### Inhalt (Pflichtfelder)
| Sektion | Faktoren | Beschreibung |
|---------|----------|--------------|
| metadata | 5 | Name, Code, Version, Hierarchie |
| organisation | 8 | Profil, Grösse, Branche, Strategie |
| psi_dimensions | 8 | Alle 8 Ψ-Dimensionen (Basiswerte) |
| customer_segments | 4-6 | Kernsegmente mit Verhaltensparametern |
| behavioral_parameters | 6 | λ, β, κ, σ, γ Aggregatwerte |

### Use Cases
- **Pitch-Vorbereitung:** Schneller Kundenüberblick vor Meeting
- **Screening:** Passt der Kunde zu unserem Angebot?
- **Quick Assessment:** Erste Hypothesen für Intervention Design

### Beispiel
```yaml
# BCM2_MIKRO_ZKB_context.yaml (SCHNELL)
metadata:
  name: "ZKB Schnellkontext"
  layer: "mikro"
  total_factors: 32

psi_dimensions:
  psi_I_institutional: 0.78
  psi_S_social: 0.72
  # ... (8 Dimensionen)

customer_segments:
  - id: "SEG-DIGITAL"
    share: 0.35
    lambda: 2.10
```

### Referenz-Implementierung
- `data/dr-datareq/sources/clients/zkb/external/BCM2_MIKRO_ZKB_context.yaml`

---

## Stufe 2: STANDARD (400 Faktoren)

### Definition
Vollständiger Kontextvektor für strategische Projekte. Strukturiert in 8 thematische Dateien mit je 30-80 Faktoren.

### Struktur
```
data/customers/<kunde>/
├── <kunde>_context_master_overview.yaml   # Index & Metadaten
├── <kunde>_context_fin_financial.yaml     # 80 Faktoren
├── <kunde>_context_mkt_market.yaml        # 60 Faktoren
├── <kunde>_context_org_governance.yaml    # 50 Faktoren
├── <kunde>_context_peo_people.yaml        # 80 Faktoren
├── <kunde>_context_ris_risk.yaml          # 30 Faktoren
├── <kunde>_context_stk_stakeholder.yaml   # 20 Faktoren
├── <kunde>_context_str_strategy.yaml      # 40 Faktoren
└── <kunde>_context_tec_technology.yaml    # 40 Faktoren
                                           ─────────────────
                                           TOTAL: 400 Faktoren
```

### Die 8 Kontext-Kategorien

| Code | Kategorie | Faktoren | Beschreibung |
|------|-----------|----------|--------------|
| **FIN** | Financial | 80 | Ertragslage, Bilanz, Kapital, Liquidität, Bewertung |
| **MKT** | Market | 60 | Marktanteile, Wettbewerb, Kunden, Pricing |
| **ORG** | Governance | 50 | Struktur, Führung, Entscheidungsprozesse |
| **PEO** | People | 80 | Mitarbeiter, Kultur, Talente, Engagement |
| **RIS** | Risk | 30 | Operationelle, strategische, regulatorische Risiken |
| **STK** | Stakeholder | 20 | Eigentümer, Regulatoren, Öffentlichkeit |
| **STR** | Strategy | 40 | Vision, Ziele, Initiativen, Roadmap |
| **TEC** | Technology | 40 | IT-Infrastruktur, Digitalisierung, Innovation |

### Faktor-Schema (Pflichtfelder pro Faktor)
```yaml
MKT-ANT-001:
  name: "Hypothekenmarktanteil Kanton Luzern"
  value: 0.38
  unit: "ratio"
  year: 2024
  trend: "stabil"                    # steigend/stabil/fallend
  benchmark_ch: 0.25                 # Optional: Vergleichswert
  source: "Geschäftsbericht"
  strategic_relevance: "critical"    # critical/high/medium/low
  ebf_mapping:                       # EBF-Verknüpfung
    psi_dimension: "psi_E"
    behavioral_parameter: "kappa_MKT"
```

### Use Cases
- **Strategieberatung:** Vollständige Kontextbasis für Empfehlungen
- **Intervention Design:** Parameter für alle 10C-Dimensionen
- **Szenario-Modellierung:** Input für Monte Carlo Simulationen
- **Board Reporting:** KPI-Dashboard mit 400 Datenpunkten

### Referenz-Implementierung
- `data/customers/lukb/` (vollständig, 400 Faktoren)
- `data/customers/alpla/` (vollständig + erweitert)

---

## Stufe 3: VERTIEFT (400+ Faktoren)

### Definition
Standard-Basis (400) plus domänenspezifische Vertiefungen. Für Langzeitmandate und komplexe Transformationen.

### Struktur
```
data/customers/<kunde>/
├── [8 Standard-Dateien]               # 400 Faktoren (wie Stufe 2)
├── <kunde>_deep_<domain>.yaml         # +50-200 Faktoren pro Vertiefung
├── <kunde>_models.yaml                # Kundenspezifische Modelle
├── <kunde>_scenarios.yaml             # Szenario-Analysen
├── <kunde>_roadmap.yaml               # Implementierungs-Roadmap
├── <kunde>_kpis.yaml                  # KPI-Framework
└── <kunde>_dependencies.yaml          # Cross-funktionale Abhängigkeiten
```

### Vertiefungs-Optionen

| Domain | Zusätzliche Faktoren | Trigger |
|--------|---------------------|---------|
| **Behavioral Deep Dive** | +100 | Komplexe Segmentierung, Personas |
| **Digital Transformation** | +80 | IT-Strategie, Change Management |
| **Sustainability/ESG** | +60 | Carbon, Circular Economy, Social |
| **M&A Integration** | +100 | Due Diligence, Cultural Fit |
| **Geographic Expansion** | +80 | Markteintritte, Lokalisierung |
| **Innovation/R&D** | +50 | Pipeline, Patents, Partnerships |

### Beispiel: ALPLA (Vertieft)
```
data/customers/alpla/
├── alpla_context_*.yaml           # 400 Basis-Faktoren
├── alpla_models.yaml              # 10 strategische Modelle
├── alpla_assumptions.yaml         # 120 Annahmen (9 Kategorien)
├── alpla_scenarios.yaml           # 3 Szenarien + Monte Carlo
├── alpla_roadmap.yaml             # 36 Quartals-Meilensteine
├── alpla_kpis.yaml                # 25 KPIs (6 Tiers)
└── alpla_dependencies.yaml        # 7 strategische Abhängigkeiten
                                   ─────────────────────────────
                                   TOTAL: ~700+ Faktoren
```

### Use Cases
- **Transformationsprogramme:** Mehrjährige Begleitung
- **M&A Due Diligence:** Vollständige Zielanalyse
- **Board-Level Strategy:** Quartalweise Reporting
- **Organizational Redesign:** People & Culture Deep Dive

### Referenz-Implementierung
- `data/customers/alpla/` (vollständig dokumentiert)

---

## Stufenwahl: Decision Tree

```
                    ┌─────────────────────────┐
                    │ Neuer Kunde/Projekt     │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼───────────┐
                    │ Was ist das Ziel?     │
                    └───────────┬───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ Quick Assess  │      │ Strategie-    │      │ Langzeit-     │
│ Pitch         │      │ projekt       │      │ Transformation│
│ Screening     │      │ Intervention  │      │ M&A           │
└───────┬───────┘      └───────┬───────┘      └───────┬───────┘
        │                      │                      │
        ▼                      ▼                      ▼
   ┌─────────┐           ┌──────────┐          ┌───────────┐
   │ SCHNELL │           │ STANDARD │          │ VERTIEFT  │
   │ ~30     │           │ 400      │          │ 400+      │
   └─────────┘           └──────────┘          └───────────┘
```

### Entscheidungskriterien

| Kriterium | SCHNELL | STANDARD | VERTIEFT |
|-----------|---------|----------|----------|
| Projektdauer | < 1 Monat | 1-6 Monate | > 6 Monate |
| Budget | < CHF 50k | CHF 50-200k | > CHF 200k |
| Datenqualität | Schätzungen OK | Verifiziert | Auditiert |
| Stakeholder | Projektteam | Management | Board |
| Erstellungszeit | 2-4 Stunden | 1-2 Tage | 1-2 Wochen |

---

## EBF-Integration

### Verknüpfung mit 10C Framework

| CVA-Kategorie | 10C-Dimension | Ψ-Dimension |
|---------------|---------------|-------------|
| FIN | WHERE (BBB) | Ψ_E (Economic) |
| MKT | WHAT (C) | Ψ_E, Ψ_S |
| ORG | WHO (AAA) | Ψ_I (Institutional) |
| PEO | AWARE (AU), READY (AV) | Ψ_C (Cognitive) |
| RIS | WHEN (V) | Ψ_T (Temporal) |
| STK | WHO (AAA) | Ψ_S (Social) |
| STR | STAGE (AW) | Ψ_T, Ψ_I |
| TEC | HOW (B) | Ψ_M (Material) |

### Verknüpfung mit BCM2

```
MAKRO (404 Faktoren)          MESO (Branche)           MIKRO (Kunde)
context/ch/BCM2_04_KON_*      [geplant]                customers/<kunde>/
        │                           │                         │
        └───────────────────────────┴─────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │  CVA Stufe 1/2/3 erbt von    │
                    │  MAKRO und überschreibt       │
                    │  kundenspezifisch             │
                    └───────────────────────────────┘
```

---

## Templates

### Template: SCHNELL
```
templates/context-vector-schnell.yaml
```

### Template: STANDARD (8 Dateien)
```
templates/context-vector-standard/
├── template_context_master_overview.yaml
├── template_context_fin_financial.yaml
├── template_context_mkt_market.yaml
├── template_context_org_governance.yaml
├── template_context_peo_people.yaml
├── template_context_ris_risk.yaml
├── template_context_stk_stakeholder.yaml
├── template_context_str_strategy.yaml
└── template_context_tec_technology.yaml
```

---

## Validierung

### Compliance-Check
```bash
python scripts/check_context_vector_compliance.py data/customers/<kunde>/
```

### Pflicht-Scores
| Stufe | Min. Faktoren | Min. Completion | Min. EBF-Mapping |
|-------|---------------|-----------------|------------------|
| SCHNELL | 25 | 80% | 50% |
| STANDARD | 380 | 90% | 80% |
| VERTIEFT | 400 | 95% | 90% |

---

## Changelog

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.0.0 | 2026-01-27 | Initiale Erstellung, 3-Stufen-Architektur definiert |

---

## Referenzen

- **CLAUDE.md:** Kontext-First Workflow (5-Ebenen Hierarchie)
- **Appendix V (CORE-WHEN):** Ψ-Dimensionen Theorie
- **BCM2_Framework_Structure.md:** Datenbank-Hierarchie
- **EBF_DATABASE_ARCHITECTURE.md:** 5-Datenbank-System

---

*Maintainer: Strategic Analysis Team*
