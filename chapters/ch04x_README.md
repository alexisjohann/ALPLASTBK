# Chapter 4x: Calibration, not Simulation

> Das Kernargument: Kalibrierung vs. Simulation

---

## Übersicht

| Metrik | Wert |
|--------|------|
| **Datei** | `04x_calibration_not_simulation.tex` |
| **Teil** | I (Grundlagen) |
| **Seiten** | ~15 |
| **CORE-Appendix** | **BBB (CORE-WHERE)** |

---

## Das zentrale Argument

> **Warum kann ChatGPT menschliches Verhalten nicht vorhersagen?**
>
> Weil es auf *Texten über* Experimente trainiert wurde,
> nicht auf *experimentellen Daten*.

---

## EBF vs. LLM/Digital Twin

| Aspekt | LLM / Digital Twin | EBF |
|--------|-------------------|---------|
| Datenquelle | Textkorpora | Experimentelle Verhaltensdaten |
| Wissensform | "Der Endowment-Effekt ist..." | E(Ψ) = 0.31 + 0.24·Ψ_C |
| Heterogenität | Weggemittelt | Explizit modelliert |
| Replikationsrate | ~50% | >85% (by construction) |
| Selbstverbesserung | Keine | Abweichungen triggern Revision |

---

## LLM Monte Carlo Methodik

```
N Queries × M Variations → Distribution → μ, σ, CI₉₅
```

- **Prompt Variation**: 5 semantisch äquivalente Templates
- **Temperature Variation**: τ ∈ {0.3, 0.5, 0.7, 0.9}
- **Varianz-Dekomposition**: Woher kommt die Unsicherheit?

---

## Schlüsselkonzepte

| Konzept | Definition |
|---------|------------|
| **LLM-MC** | LLM Monte Carlo Estimation |
| **Epistemic Tags** | EMP/THR/LLM/ILL/HYP |
| **C*** | Kalibrierte Referenzstruktur |

---

## Verbindungen

| Zu Kapitel | Thema |
|------------|-------|
| ← Ch. 4 | Empirische Grundlagen |
| → Appendix AN | LLM Monte Carlo (Detail) |
| → Appendix BBB | Parameter Estimation |

---

*10C CORE Framework — EBF*
