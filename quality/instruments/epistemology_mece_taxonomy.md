# EBF Epistemology: MECE Taxonomy of Scientific Constructs

> **SSOT Reference:** `docs/frameworks/core-framework-definition.yaml` (Section: `epistemology`)
> **Version:** 2.3 (2026-01-20)

---

## Quick Reference: Die 15 Konstrukte in 6 Kategorien

| Kat. | Symbol | Konstrukt | Formal | Beweisbar? | Evidenz? |
|------|--------|-----------|--------|------------|----------|
| **1** | α | **Axiom** | α ∈ 𝒜(EBF) | Nein (Prämisse) | Typ-abhängig |
| | ι | **Assumption** | ι ∈ Assumptions | Nein (implizit) | Nein |
| **2** | δ | **Definition** | t_new ≡ expr | Tautologisch | Nein |
| | ν | **Notation** | symbol ↦ meaning | Metasprachlich | Nein |
| **3** | τ | **Theorem** | ∃𝒫: 𝒜 ⊢ τ | Ja (σ ≥ θ_thm) | Beweis |
| | π | **Proposition** | ∃𝒫: 𝒜 ⊢ π | Ja (σ mittel) | Beweis |
| | λ | **Lemma** | λ in proof(τ) | Ja (Hilfssatz) | Beweis |
| | κ | **Corollary** | τ ⊨ κ direkt | Ja (≤2 Schritte) | Ableitung |
| **4** | ξ | **Conjecture** | ¬∃𝒫: 𝒜 ⊢ ξ | Nein (offen) | Plausibilität |
| | ω | **Open Issue** | Frage Q | Nein (Lücke) | Begründung |
| **5** | ε | **Example** | Instanz von C | Nein (illustrativ) | Nein |
| | ρ | **Remark** | Bezug auf X | Nein (Kommentar) | Nein |
| | ο | **Observation** | Muster M | Nein (empirisch) | Daten |
| | φ | **Critical Foundation** | Externe Einsicht | Nein (extern) | Zitat |
| **6** | η | **Heuristic** | P(korrekt) ≥ θ | Nein (Faustregel) | Erfahrung |

---

## Die 6 MECE Kategorien

### Kategorie 1: PRÄMISSEN (Inputs)
**Definition:** Aussagen, die als wahr akzeptiert werden, ohne innerhalb von EBF bewiesen zu werden.

| Konstrukt | Wann verwenden? |
|-----------|-----------------|
| **Axiom** (α) | Explizite, nummerierte Grundannahme |
| **Assumption** (ι) | Implizite Annahme (sollte explizit werden, wenn zentral) |

**Axiom-Subtypen:**
- `structural` (α_struct): Modellierungsentscheidung, nicht falsifizierbar
- `empirical` (α_emp): Empirische Tatsache, MUSS Zitat haben
- `theoretical` (α_theo): Von externer Theorie importiert

---

### Kategorie 2: NAMENGEBUNG (Tautologisch)
**Definition:** Konstrukte, die Namen oder Symbole einführen, ohne inhaltliche Behauptungen zu machen.

| Konstrukt | Wann verwenden? |
|-----------|-----------------|
| **Definition** (δ) | Neuen Begriff/Konzept benennen |
| **Notation** (ν) | Neues Symbol einführen |

**Unterschied:**
- Definition: Semantisch (Bedeutung erklären)
- Notation: Syntaktisch (nur Zeichen einführen)

---

### Kategorie 3: BEWIESENE AUSSAGEN (Outputs)
**Definition:** Aussagen, die aus Axiomen bewiesen werden.

| Konstrukt | Signifikanz | Wann verwenden? |
|-----------|-------------|-----------------|
| **Theorem** (τ) | Hoch (σ ≥ θ_thm) | Hauptresultat, zentrale Erkenntnis |
| **Proposition** (π) | Mittel | Wichtiges Zwischenresultat |
| **Lemma** (λ) | Gering | Hilfsaussage für Theorem-Beweis |
| **Corollary** (κ) | Abhängig | Direkte Folge (≤2 Schritte) |

**Hierarchie:** Theorem > Proposition > Lemma > Corollary

---

### Kategorie 4: OFFENE AUSSAGEN (Noch nicht bewiesen)
**Definition:** Aussagen, die noch nicht bewiesen oder widerlegt wurden.

| Konstrukt | Präzision | Wann verwenden? |
|-----------|-----------|-----------------|
| **Conjecture** (ξ) | Hoch | Spezifische Vermutung, prinzipiell beweisbar |
| **Open Issue** (ω) | Niedrig | Forschungsfrage, noch nicht präzise genug |

---

### Kategorie 5: ILLUSTRATIONEN (Veranschaulichung)
**Definition:** Konstrukte, die etwas veranschaulichen, aber nichts beweisen.

| Konstrukt | Quelle | Wann verwenden? |
|-----------|--------|-----------------|
| **Example** (ε) | Konkrete Instanz | Abstraktes Konzept illustrieren |
| **Remark** (ρ) | Eigene Reflexion | Kontext/Vergleich zu anderem Konstrukt |
| **Observation** (ο) | Daten/Literatur | Empirisches Muster (ohne formalen Beweis) |
| **Critical Foundation** (φ) | Externe Literatur | Zentrale Einsicht, auf der EBF aufbaut |

---

### Kategorie 6: PRAKTISCHE REGELN (Heuristiken)
**Definition:** Regeln, die meist funktionieren, aber keine Garantie haben.

| Konstrukt | Wann verwenden? |
|-----------|-----------------|
| **Heuristic** (η) | Praktische Faustregel ohne formalen Beweis |

---

## Entscheidungsbaum: Welches Konstrukt?

```
START: Was ist die Natur der Aussage?
│
├─ Führt Notation/Terminologie ein? → KATEGORIE 2
│  ├─ Benennt ein Konzept? → Definition (δ)
│  └─ Führt Symbol ein? → Notation (ν)
│
├─ Ist eine Grundannahme? → KATEGORIE 1
│  ├─ Explizit und nummeriert? → Axiom (α)
│  │  ├─ Definiert Struktur? → structural
│  │  ├─ Empirische Tatsache? → empirical
│  │  └─ Von externer Theorie? → theoretical
│  └─ Implizit verwendet? → Assumption (ι)
│
├─ Ist logisch bewiesen? → KATEGORIE 3
│  ├─ Hauptresultat (hoch signifikant)? → Theorem (τ)
│  ├─ Mittleres Resultat? → Proposition (π)
│  ├─ Hilfsaussage für Theorem? → Lemma (λ)
│  └─ Folgt direkt aus Theorem? → Corollary (κ)
│
├─ Unbewiesene Vermutung? → KATEGORIE 4
│  ├─ Spezifisch genug für Beweis? → Conjecture (ξ)
│  └─ Offene Forschungsfrage? → Open Issue (ω)
│
├─ Veranschaulicht/illustriert? → KATEGORIE 5
│  ├─ Konkretes Beispiel? → Example (ε)
│  ├─ Ergänzende Bemerkung? → Remark (ρ)
│  ├─ Empirisches Muster? → Observation (ο)
│  └─ Wichtige externe Einsicht? → Critical Foundation (φ)
│
└─ Praktische Faustregel? → KATEGORIE 6
   └─ Meist korrekt, keine Garantie? → Heuristic (η)
```

---

## MECE-Beweis

### Mutually Exclusive (ME)
Die Kategorien sind disjunkt:
```
is_premise(X)     := ¬provable(X) ∧ accepted_as_input(X)
is_naming(X)      := tautological(X)
is_proven(X)      := ∃𝒫: 𝒜 ⊢ X
is_open(X)        := ¬proven(X) ∧ ¬disproven(X) ∧ well_formed(X)
is_illustration(X) := demonstrates(X) ∧ ¬proves(X)
is_heuristic(X)   := practical_rule(X) ∧ ¬guaranteed(X)

∀X: Genau EINE dieser Funktionen ist wahr.
```

### Collectively Exhaustive (CE)
Jedes Konstrukt fällt in eine Kategorie:
```
Universe(EBF) = 𝒜 ∪ Assumptions ∪ Definitions ∪ Notations
              ∪ 𝒯 ∪ Propositions ∪ Lemmas ∪ Corollaries
              ∪ Conjectures ∪ OpenIssues
              ∪ Examples ∪ Remarks ∪ Observations ∪ CriticalFoundations
              ∪ Heuristics
```

---

## Epistemic Tags Mapping

| Konstrukt | Tag | Konfidenz |
|-----------|-----|-----------|
| Axiom (empirical) | EMP | ★★★★★ |
| Axiom (structural/theoretical), Theorem, Proposition, Lemma, Corollary, Definition | THR | ★★★★☆ |
| Parameter Estimate | LLM | ★★★☆☆ |
| Example, Heuristic, Remark | ILL | ★★☆☆☆ |
| Conjecture, Open Issue | HYP | ★☆☆☆☆ |
| Observation, Critical Foundation | EMP | ★★★★☆ (extern) |

**Aggregationsregel:** Der Gesamt-Tag ist der schwächste Einzeltag.

---

## Checkliste: Konstrukt korrekt klassifiziert?

```
☐ Genau EINE Kategorie gewählt
☐ Symbol korrekt (α, τ, δ, etc.)
☐ Code-Format korrekt (z.B. IE-T4, IE-D1, IE-CONJ-1)
☐ Für Axiom: Typ (structural/empirical/theoretical) angegeben
☐ Für empirisches Axiom: Mindestens 1 Zitat
☐ Für Theorem/Proposition/Lemma: Beweis dokumentiert
☐ Für Corollary: Parent-Theorem referenziert
☐ Für Conjecture: Plausibilitätsargument vorhanden
☐ Epistemic Tag konsistent mit Konstrukt-Typ
```

---

*Erstellt: 2026-01-20 | SSOT: core-framework-definition.yaml v2.3*
