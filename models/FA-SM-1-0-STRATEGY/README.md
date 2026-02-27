# FA-SM-1.0: FehrAdvice Strategy Model

> **Meta-Modell für wertschöpfungsgetriebenes Strategiedesign**
> Version 1.0 | Februar 2026 | Status: EXPERIMENTAL

---

## Philosophische Grundlage

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  WERTSTEIGERUNG  ←  VERHALTEN  ←  KONTEXT-DESIGN                       │
│     (Ziel)          (Hebel)        (Instrument)                         │
│     V(t)            B(t)           Ψ(t)                                 │
│                                                                         │
│  Strategie OHNE Verhalten = nicht umsetzbar                             │
│  Strategie NUR an Verhalten = kein Ziel                                 │
│  Strategie MIT Verhalten FÜR Wertschöpfung = FA-SM                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Drei-Schichten-Architektur

| Schicht | Name | Symbol | Frage | Rolle |
|---------|------|--------|-------|-------|
| **0** | Wertschöpfungsziel | V(t) | Welchen Wert schaffen? | NORDSTERN |
| **1** | Verhaltensübersetzung | B(t) | Wessen Verhalten ändern? | HEBEL |
| **2** | Kontext-Design | Ψ(t) | Welchen Kontext gestalten? | INSTRUMENT |

## Master-Gleichung

```
V(t) = f(B(t), Ψ(t))

wobei:
  V(t) = Σ_k w_k · [α_k · Σ_j λ_j · B_j(t) + β_k · Ψ_market(t) + γ_k · B(t)·Ψ(t)]

  dB_j/dt = β_j · U_j(Ψ) · B_j · (1 - B_j) · (1 - R_j) · (1 + M_j)
```

## Wertdimensionen (Schicht 0)

| Symbol | Name | Gewicht | Zeithorizont |
|--------|------|---------|-------------|
| V_F | Finanzielle Wertschöpfung | 0.30 | 1-5 Jahre |
| V_S | Strategische Wertschöpfung | 0.25 | 3-10 Jahre |
| V_O | Organisationale Wertschöpfung | 0.20 | 2-7 Jahre |
| V_C | Kundenwertschöpfung | 0.15 | 1-3 Jahre |
| V_I | Innovationswertschöpfung | 0.10 | 3-10 Jahre |

## Akteursgruppen (Schicht 1)

| Symbol | Gruppe | Value-Leverage (λ) |
|--------|--------|-------------------|
| B_L | Leadership (VR, GL) | 0.35 |
| B_M | Mittleres Management | 0.30 |
| B_O | Operations (Frontline) | 0.20 |
| B_E | Externe Stakeholder | 0.15 |

## Kontextdimensionen (Schicht 2)

### Organisational (gestaltbar)

| Symbol | Name | Gestaltbar? |
|--------|------|------------|
| Ψ_GOV | Governance & Entscheidungsarchitektur | Ja |
| Ψ_INC | Anreizarchitektur | Ja |
| Ψ_INF | Informationsarchitektur | Ja |
| Ψ_CUL | Kulturarchitektur | Teilweise (2-5 Jahre) |
| Ψ_CAP | Fähigkeitsarchitektur | Ja |

### Markt (extern, nicht gestaltbar)

| Symbol | Name | Gestaltbar? |
|--------|------|------------|
| Ψ_MKT | Marktdynamik | Nein |
| Ψ_REG | Regulatorisches Umfeld | Nein |
| Ψ_MAC | Makroumfeld | Nein |

## Sub-Modell-Integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FA-SM-1.0 (META)                                                       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Schicht 0: WERTSCHÖPFUNG                                      │    │
│  │  V(t) = Σ w_k · V_k(t)                                         │    │
│  │                                                                 │    │
│  │  ┌───────────────────────────────────────────────────────────┐  │    │
│  │  │  SOCM-1.0: Welche strategischen Optionen maximieren V?   │  │    │
│  │  │  Portfolio-Optimierung, γ zwischen Optionen               │  │    │
│  │  └───────────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              ↕                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Schicht 1: VERHALTEN                                           │    │
│  │  B(t) = [B_L, B_M, B_O, B_E]                                   │    │
│  │                                                                 │    │
│  │  ┌───────────────────────────────────────────────────────────┐  │    │
│  │  │  SDM-1.0: 4-Phasen BCJ (Awareness→Readiness→Action→     │  │    │
│  │  │  Embedding) für Verhaltensänderung                        │  │    │
│  │  └───────────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              ↕                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  Schicht 2: KONTEXT                                             │    │
│  │  Ψ(t) = [Ψ_GOV, Ψ_INC, Ψ_INF, Ψ_CUL, Ψ_CAP, Ψ_MKT, ...]   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Bidirektionaler Workflow

### Top-Down: Auslegeordnung → Zielableitung

```
Schritt 1: Wertschöpfungsziel definieren (V*)
    ↓
Schritt 2: Verhaltensübersetzung (B* ableiten)
    ↓
Schritt 3: Kontext-Diagnostik (ΔΨ identifizieren)
    ↓
Schritt 4: Strategische Architektur (via SOCM-1.0)
    ↓
Schritt 5: Implementierungsdesign (via SDM-1.0)
    ↓
Schritt 6: Dynamisches Modell (ODE Simulation)
```

### Bottom-Up: Realitätscheck → Machbarkeit

```
Schritt 1: Kontext-Ist-Analyse (Ψ(t₀))
    ↓
Schritt 2: Verhaltensvorhersage (B_predicted)
    ↓
Schritt 3: Wertschöpfungs-Prognose (V_predicted)
    ↓
Schritt 4: Gap-Analyse (V* - V_predicted)
    → zurück zu Top-Down für Iteration
```

## Erste Instanziierung: Zindel United (ZIN005)

Das FA-SM-1.0 wird erstmals im Projekt ZIN005 (Organisationsentwicklung) für Zindel United angewendet. Zindel United ist ein idealer Erstanwendungsfall:

- **Familienunternehmen** (8. Generation, 210+ Jahre)
- **Laufende Projekte:** ZIN003 (Kreislaufwirtschaft), ZIN004 (Organisationsentwicklung)
- **VERTIEFT CVA:** 983 Kontextfaktoren bereits erfasst
- **ODE-Modell:** MOD-ZIN-001 bereits kalibriert
- **M&A-Kontext:** INKOH AG Transaktion aktiv

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `model-definition.yaml` | Formale Modelldefinition |
| `README.md` | Diese Dokumentation |
| `examples/zindel-united/` | Erste Instanziierung (ZIN005) |

## Referenzen

- SDM-1.0: `models/models.registry.yaml` (Zeile 778)
- SOCM-1.0: `models/models.registry.yaml` (Zeile 1023)
- ZIN003 ODE-Modell: `outputs/sessions/EBF-S-2026-02-02-ORG-ZIN003/`
- Zindel CVA: `data/customers/zindel-united/kontextvektoren/`
