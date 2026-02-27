# Kontextvektoren - ZIN003 Kreislaufwirtschaft

**CVA-Stufe:** VERTIEFT (983 Faktoren)
**Projekt:** ZIN003 - Kreislaufwirtschaft
**Kunde:** Zindel United
**Version:** 1.0.0
**Erstellt:** 2026-02-02

## Übersicht

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONTEXT VECTOR ARCHITECTURE (CVA) - VERTIEFT                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TOTAL: 983 FAKTOREN                                                        │
│                                                                             │
│  ├── 01_unternehmen          150 Faktoren  (Zindel United Profil)          │
│  ├── 02_branchen_ch          150 Faktoren  (Schweizer Baubranche)          │
│  ├── 03_kreislaufwirtschaft  183 Faktoren  (Circular Economy Studien)      │
│  ├── 04_branchen_global      160 Faktoren  (Globale Baubranche)            │
│  ├── 05_wettbewerber_ch      120 Faktoren  (CH Wettbewerber)               │
│  ├── 06_wettbewerber_global  100 Faktoren  (Globale Wettbewerber)          │
│  └── 07_graubuenden_regional 120 Faktoren  (Regionales Profil GR)          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Dateien

| Datei | Faktoren | Beschreibung | Quelle |
|-------|----------|--------------|--------|
| `CV_ZIN003_00_master_overview.yaml` | - | Master-Index | - |
| `CV_ZIN003_01_unternehmen.yaml` | 150 | Zindel United Unternehmensprofil | ZindelUnited_Unternehmen_Kontextvektor.xlsx |
| `CV_ZIN003_02_branchen_ch.yaml` | 150 | Schweizer Baubranche | Bau_CH_Branchen_Kontextvektor.xlsx |
| `CV_ZIN003_03_kreislaufwirtschaft.yaml` | 183 | Circular Economy Wissenschaft | Kreislaufwirtschaft-Bauindustrie_Studien_Kontextvektor.xlsx |
| `CV_ZIN003_04_branchen_global.yaml` | 160 | Globale Baubranche | Bau_Global_Branchen_Kontextvektor.xlsx |
| `CV_ZIN003_05_wettbewerber_ch.yaml` | 120 | Schweizer Wettbewerber | Bauindustrie_CH_Wettbewerber_Kontextvektor.xlsx |
| `CV_ZIN003_06_wettbewerber_global.yaml` | 100 | Globale Wettbewerber | Bauindustrie_Global_Wettbewerber_Kontextvektor.xlsx |
| `CV_ZIN003_07_graubuenden_regional.yaml` | 120 | Regionales Profil Graubünden | Graubünden_CH_Zindel_Kontextvektor.xlsx |

## EBF-Integration

### 10C Coverage
- WHO: Stakeholder, Mitarbeiter, Kunden
- WHAT: Utility-Dimensionen, Geschäftsmodell
- HOW: Komplementaritäten, Innovation
- WHEN: Kontext, Regulierung, Konjunktur
- WHERE: Markt, Parameter, Geografie
- AWARE: Awareness, Risikobewusstsein
- READY: Handlungsbereitschaft
- STAGE: Strategische Phase
- HIERARCHY: Entscheidungsebenen

### Ψ-Dimensionen Coverage
- Ψ_I (Institutional): Regulierung, Governance
- Ψ_S (Social): Mitarbeiter, Stakeholder
- Ψ_C (Cognitive): Komplexität, Bewusstsein
- Ψ_K (Cultural): Identität, Werte
- Ψ_E (Economic): Markt, Finanzen
- Ψ_T (Temporal): Strategie, Trends
- Ψ_M (Material): Technologie, Innovation
- Ψ_F (Physical): Regional, Standort

## Faktor-Schema

Jeder Faktor enthält:

```yaml
- id: "ZIN-D1-F01"
  dimension: "Identität & Geschichte"
  faktor: "Gründungsjahr"
  definition: "Zeitpunkt Ursprung / HR-Eintrag"
  kontext: "Ursprung 1808, HR-Eintrag 1930"
  salienz: 1.0
  indikator: "Jahr der Gründung"
  gruende: "1. Längste Tradition... 2. Familienunternehmen..."
  datenpunkt: "1808 Ursprung, 1930 HR"
  trend: "stabil"
  unsicherheit: "gering"
  risiko_chance: "Chance: Vertrauen, Reputation"
  staerke_schwaeche: "Stärke: Historische Verwurzelung"
  beeinflussbarkeit: "nicht beeinflussbar"
  ebf_mapping:
    10c_dimensions: ["WHO", "STAGE"]
    psi_dimension: "Ψ_T"
```

## Nächste Schritte

1. **Behavioral Parameters kalibrieren** via `/design-model`
2. **Interventions-Design** via `/design-intervention`
3. **Monte Carlo Simulation** für Szenario-Analyse
4. **KPI-Dashboard** erstellen

## Referenzen

- CVA-Dokumentation: `docs/frameworks/context-vector-architecture.md`
- SCHNELL-Template: `templates/context-vector-schnell.yaml`
- ALPLA-Beispiel (VERTIEFT): `data/customers/alpla/`
