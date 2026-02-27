# Complementarity (γ) im EBF

> **SSOT:** `data/knowledge/canonical/complementarity.yaml`
> **Upload-Tags:** canonical, complementarity, gamma, ebf, ssot
> **Prioritaet:** HOECHSTE — erklaert warum Interventionen manchmal schaden

---

## Was ist Complementarity?

**Complementarity** beschreibt, **wie verschiedene Nutzendimensionen miteinander interagieren** — ob sie sich gegenseitig verstaerken oder untergraben.

---

## Die Kernidee

```
ADDITIV (γ = 0):         Gesamtnutzen = U_F + U_S + U_E
KOMPLEMENTAER (γ > 0):   Gesamtnutzen = U_F + U_S + γ·U_F·U_S  (verstaerkend)
SUBSTITUTIV (γ < 0):     Gesamtnutzen = U_F + U_S + γ·U_F·U_S  (unterminierend)
```

---

## Die formale Gleichung

```
Q = Σᵢ ωᵢ · Uⁱ + Σᵢ≠ⱼ γᵢⱼ · Uⁱ · Uⱼ
```

Wobei:
- **Q** = Gesamtnutzen (Total Welfare)
- **ωᵢ** = Gewicht der Dimension i
- **Uⁱ** = Nutzen in Dimension i
- **γᵢⱼ** = Komplementaritaetsparameter zwischen Dimension i und j

---

## Die 3 Faelle

| γ-Wert | Bedeutung | Beispiel |
|--------|-----------|----------|
| **γ = 0** | Additiv (Default) | Einkommen und Gesundheit unabhaengig |
| **γ > 0** | Komplementaer | Soziale Anerkennung verstaerkt intrinsische Motivation |
| **γ < 0** | Substitutiv (Crowding-Out) | Finanzielle Anreize untergraben soziale Normen |

---

## Die EXC-Regeln (Exclusion Principle)

**Additivitaet ist DEFAULT** — Komplementaritaet (γ ≠ 0) muss begruendet werden:

- **EXC-1**: Additiv braucht keine Begruendung
- **EXC-2**: Multiplikativ erfordert Veto-Analyse
- **EXC-5**: Nur Whitelist V1-T1 akzeptiert

---

## Empirisch validierte γ-Werte (PAR-COMP)

| Parameter | γ-Wert | Interaktion | Quelle |
|-----------|--------|-------------|--------|
| PAR-COMP-001 | **+0.35** | Identity × Social | Akerlof & Kranton |
| PAR-COMP-002 | **−0.68** | Social × Financial (Crowding-Out) | Fehr & Falk |
| PAR-COMP-004 | **+0.28** | Social × Warm Glow | Andreoni |

Diese Werte sind **NICHT willkuerlich** — sie stammen aus der wissenschaftlichen Literatur und Projektvalidierungen.

---

## Der wichtigste Crowding-Out-Effekt

```
Finanzielle Anreize + Soziale Normen = GEFAEHRLICH (γ = −0.68)
```

Wenn man fuer freiwilliges Verhalten bezahlt, zerstoert das die soziale Motivation. Klassisches Beispiel: Blutspende-Paradox (Titmuss 1970, Frey & Jegen 2001).

**WARNUNG:** Niemals Social (Ψ_S) und Financial (U_F) kombinieren ohne Crowding-Out-Analyse!

---

## Warum Complementarity wichtig ist

1. **Erklaert Interventionsversagen**: Warum gut gemeinte Massnahmen manchmal schaden
2. **Warnt vor Crowding-Out**: Nicht jede Kombination von Anreizen funktioniert
3. **Ermoeglicht synergetisches Design**: Dimensionen gezielt verstaerkend kombinieren
4. **Ist empirisch fundiert**: Jeder γ-Wert hat Paper-Referenzen (PAR-COMP-xxx)

---

## Wechselwirkungen in der Realitaet (Ernst Fehr Formulierung)

Ein zentraler Mehrwert des EBF liegt in der Faehigkeit, **Wechselwirkungen zu erfassen, die in der Realitaet zwischen psychologischen, finanziellen, kulturellen und institutionellen Faktoren stattfinden**. In realen Entscheidungssituationen wirken diese Faktoren nahezu immer gleichzeitig und beeinflussen sich gegenseitig. Diese Interdependenzen konnten bisher aufgrund ihrer Komplexitaet nur begrenzt beruecksichtigt werden.

Das EBF modelliert diese Wechselwirkungen formal ueber die γ-Matrix. BEATRIX macht sie erstmals konsistent analysierbar und schlaegt auf dieser Basis geeignete Massnahmen vor.

**KRITISCH:** Die korrekte Formulierung ist: BEATRIX "erfasst Wechselwirkungen, die in der Realitaet stattfinden" — NICHT "Wechselwirkungen zwischen Massnahmen".

---

## 10C-Zuordnung

Complementarity ist die **HOW-Dimension** (CORE B) im 10C Framework:
- **Frage**: Wie interagieren die Nutzendimensionen?
- **Output**: Die Γ-Matrix (Komplementaritaetsmatrix)
- **Appendix**: B (CORE-HOW)

---

*Quelle: data/knowledge/canonical/complementarity.yaml (v1.0, 2026-02-13)*
