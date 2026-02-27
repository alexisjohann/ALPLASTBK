# Kontext (Ψ) im EBF

> **SSOT:** `data/knowledge/canonical/psi-context.yaml`
> **Upload-Tags:** canonical, psi, context, ebf, ssot
> **Prioritaet:** HOECHSTE — Kontext ist der zentrale theoretische Beitrag des EBF

---

## ACHTUNG: Die zentrale Erkenntnis

**Kontext ist keine Kontrollvariable — Kontext ist das Explanans.** Dieselbe Person trifft in unterschiedlichen Kontexten **systematisch unterschiedliche** Entscheidungen, und diese Variation ist kein Rauschen, sondern ein erklaerbares Signal.

```
DIESELBE FRAGE + ANDERER KONTEXT = KOMPLETT ANDERE ANTWORT
```

Beispiel: «Soll ich mehr sparen?»
- 25-jaehrige Berufseinsteigerin in Zuerich → «Ja, 3. Saeule nutzen»
- 58-jaehriger Arbeitsloser in Berlin → «Nein, Liquiditaet sichern»

**Ohne Kontext ist jede Antwort falsch.**

---

## Die 8 Ψ-Dimensionen

Jede Situation wird durch 8 Dimensionen charakterisiert:

| Symbol | Dimension | Frage |
|--------|-----------|-------|
| **Ψ_I** | Institutional | Welche Regeln, Gesetze, Defaults gelten? |
| **Ψ_S** | Social | Wer ist dabei? Welche sozialen Normen? |
| **Ψ_C** | Cognitive | Muede? Gestresst? Aufmerksam? Motiviert? |
| **Ψ_K** | Cultural | Welche Werte, Traditionen, Religion? |
| **Ψ_E** | Economic | Wieviel Budget, Zeit, Energie verfuegbar? |
| **Ψ_T** | Temporal | Wann? Zeitdruck? Welche Lebensphase? |
| **Ψ_M** | Material | Welche Technologie, Infrastruktur, Objekte? |
| **Ψ_F** | Physical | Wo physisch? Zuhause, Buero, oeffentlich, online? |

---

## Parameter Context Transformation (PCT)

Die revolutionaere Idee: Verhaltensparameter sind **keine Konstanten**, sondern Funktionen des Kontexts.

```
Traditionell:  λ = 2.25  (Loss Aversion ist eine Konstante)
EBF:           λ(Ψ, 10C) = variabel
               λ_welfare_stigma = 2.5
               λ_workplace_peers = 1.8
```

Die Transformation:
```
θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)

Wobei:
  θ_A = Parameter im Anchor-Kontext (aus Paper)
  θ_B = Parameter im Target-Kontext (Vorhersage)
  ΔΨᵢ = Ψ_i(Target) − Ψ_i(Anchor)
  M(·) = Ψ-Multiplikator
```

---

## Die 5-Ebenen Kontext-Hierarchie

Bei jeder Analyse werden 5 Ebenen in strenger Reihenfolge durchlaufen:

| Ebene | Was? | Faktoren | Datenbank |
|-------|------|----------|-----------|
| 1. MACRO | Land/Markt | 404 | BCM2 Kontextdatenbank |
| 2. MESO | Branche/Kunde | variabel | Kundenprofile |
| 3. MICRO | Situation | 5 | Kontext-Dimensionen |
| 4. INDIVIDUAL | Person | 48 | Individuelle Faktoren |
| 5. META | Entscheidung | 42 | Entscheidungsarchitektur |

**PFLICHT-Reihenfolge:** MACRO → MESO → MICRO → INDIVIDUAL → META

**VERBOTEN:** Mit MICRO beginnen ohne MACRO/MESO!

---

## Die BCM2 Kontextdatenbank

Die Kontextdimensionen werden durch die BCM2-Datenbank operationalisiert:

| Achse | Code | Faktoren | Quellen |
|-------|------|----------|---------|
| Demografisch | DEM | 60 | BFS, SECO, BSV |
| Oekonomisch | ECO | 54 | SECO, SNB, BFS, KOF |
| Institutionell-Politisch | POL | 59 | Bundeskanzlei, World Bank |
| Technologisch-Oekologisch | TEC | 65 | BFS, BFE, BAFU |
| Sozio-Kulturell | SOC | 166 | BFS, ESS, WVS, gfs.bern, Sotomo |

**Laender:** Schweiz (CH), Oesterreich (AT), Deutschland (DE)

---

## Warum Menschen Kontext nicht selbst liefern

| Grund | Erklaerung |
|-------|-----------|
| Fisch im Wasser | Kontext ist unsichtbar fuer den Handelnden |
| Fundamental Attribution Error | Menschen erklaeren Verhalten durch Persoenlichkeit, nicht Situation |
| Curse of Knowledge | Offensichtliches wird nicht erwaehnt |
| System 1 | Schnelles Denken = keine Kontext-Reflexion |

→ Deshalb analysiert das EBF den Kontext **aktiv und systematisch**.

---

## Context Vector Architecture (CVA) fuer Kunden

| Stufe | Faktoren | Use Case | Zeit |
|-------|----------|----------|------|
| SCHNELL | ~30 | Pitch, Screening | 2-4h |
| STANDARD | 400 | Vollprojekt, Strategie | 1-2 Tage |
| VERTIEFT | 400+ | Langzeitmandat, M&A | 1-2 Wochen |

---

## 10C-Zuordnung

Kontext ist die **WHEN-Dimension** (CORE V) im 10C Framework:
- **Frage**: Wann (in welchem Kontext) zaehlt was?
- **Output**: Der Kontext-Vektor Ψ
- **Appendix**: V (CORE-WHEN)
- **Chapter**: 9

---

*Quelle: data/knowledge/canonical/psi-context.yaml (v1.0, 2026-02-13)*
