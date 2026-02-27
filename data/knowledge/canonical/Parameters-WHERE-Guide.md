# Parameter Registry (WHERE / BBB) im EBF

> **SSOT:** `data/parameter-registry.yaml`
> **Upload-Tags:** canonical, parameters, bbb, where, ebf, ssot
> **Prioritaet:** HOECHSTE — verhindert erfundene Parameterwerte ("Lambda=3.86")

---

## ACHTUNG: Keine Zahlen erfinden!

Jeder Parameter im EBF hat eine **dokumentierte Quelle**. Wenn ein Wert nicht in der Parameter Registry steht, darf er NICHT erfunden werden. Stattdessen: "Fuer diesen Parameter liegt keine validierte Schaetzung vor."

---

## Was ist die Parameter Registry?

Die Parameter Registry (BBB — CORE-WHERE) beantwortet die Frage: **"Woher kommen die Zahlen?"**

Sie enthaelt 119+ verhaltensoekomische Parameter mit:
- Literatur-Werten (Meta-Analysen, Originalstudien)
- DACH-adjustierten Werten (fuer Schweiz/Oesterreich/Deutschland)
- Domain-spezifischen Werten (Finanzen, Gesundheit, etc.)
- 95%-Konfidenzintervallen

---

## Die 4-Tier BBB Hierarchie

| Tier | Quelle | Unsicherheit | Wann verwenden |
|------|--------|--------------|----------------|
| **1** | Literature (Meta-Analyse) | Niedrig | Parameter ist etabliert |
| **2** | LLMMC Prior | Mittel | Begrenzte Evidenz |
| **3** | Empirical Calibration | Variabel | Primaerdaten verfuegbar |
| **4** | Expert Elicitation | Hoch | Neue Domaene |

**Literatur-Werte haben Vorrang.** LLMMC ist Fallback, nicht Default.

---

## Die wichtigsten Parameter

### Loss Aversion (λ) — PAR-BEH-001

**Was:** Verhaeltnis der Gewichtung von Verlusten zu Gewinnen

| Kontext | Wert | Quelle |
|---------|------|--------|
| Literatur | λ = 2.25 [1.5, 3.0] | Kahneman & Tversky (1979) |
| DACH | λ = 2.35 [2.1, 2.6] | BCM2 Kontext |
| Finanzen | λ = 2.4 [2.1, 2.7] | Domain-spezifisch |
| Gesundheit | λ = 1.8 [1.5, 2.1] | Domain-spezifisch |
| Karriere | λ = 2.8 [2.4, 3.2] | Domain-spezifisch |
| Beziehungen | λ = 3.0 [2.5, 3.5] | Domain-spezifisch |

**WICHTIG:** λ ist KEINE Konstante! Der Wert haengt vom Kontext ab (siehe KB-PSI-001).

### Crowding-Out (φ) — PAR-BEH-002

**Was:** Reduktion intrinsischer Motivation durch extrinsische Anreize

| Kontext | Wert | Quelle |
|---------|------|--------|
| Literatur | φ = 0.65 [0.50, 0.80] | Frey & Jegen (2001) |
| Finanzen | φ = 0.68 | UBS Referral Analysis |
| Gesundheit | φ = 0.55 | Spendeverhalten |
| Bildung | φ = 0.72 | Lernmotivation |

**WARNUNG:** Extrinsische Anreize reduzieren intrinsische Motivation um 50-80%!

### Present Bias (β) — PAR-BEH-003

**Was:** Uebergewichtung sofortiger vs. verzoegerter Belohnungen

| Kontext | Wert | Quelle |
|---------|------|--------|
| Literatur | β = 0.70 [0.60, 0.85] | Laibson (1997) |
| DACH | β = 0.75 | bAV Opt-Out Projekt |
| Sparen | β = 0.70 | Finanzentscheidungen |
| Sport | β = 0.65 | Gesundheitsverhalten |

**β = 1** waere rational (exponentiell), **β < 1** zeigt Gegenwartsverzerrung.

---

## Parameter-Typen

| Typ | Praefix | Beispiel |
|-----|---------|----------|
| BEHAVIORAL | PAR-BEH-xxx | Loss Aversion, Present Bias |
| CONTEXTUAL | PAR-CTX-xxx | Vertrauen, Institutionen |
| INTERVENTION | PAR-INT-xxx | Interventions-Effektstaerken |
| COMPLEMENTARITY | PAR-COMP-xxx | Interaktionseffekte (γ) |

---

## Update-Flow

```
Literatur → LLMMC Prior → Bayesian Posterior → Empirische Validierung
```

Neue Parameterwerte durchlaufen immer diesen Prozess:
1. **Literatur:** Was sagen die Papers? (Tier 1)
2. **LLMMC:** KI-gestuetzte Vorabschaetzung (Tier 2)
3. **Bayesian Update:** Kombination aus Prior + Daten
4. **Validierung:** Empirische Pruefung im Projekt

---

## Regeln fuer Parameter

1. **Jeder Parameter hat eine ID:** PAR-XXX-NNN Format
2. **Jeder Wert hat eine Quelle:** Paper-Key oder Projekt-ID
3. **Konfidenzintervalle sind Pflicht:** Nie nur Punktschaetzung
4. **Kontext-Abhaengigkeit dokumentieren:** Domain-spezifische Werte
5. **NIEMALS Werte erfinden:** Wenn kein Parameter existiert → transparent kommunizieren

---

## 10C-Zuordnung

Parameter Registry ist die **WHERE-Dimension** (CORE BBB) im 10C Framework:
- **Frage**: Woher kommen die Zahlen?
- **Output**: Validierte Parameter Θ
- **Appendix**: BBB (CORE-WHERE)

---

*Quelle: data/parameter-registry.yaml (v1.19, 119 Parameter, 2026-02-14)*
