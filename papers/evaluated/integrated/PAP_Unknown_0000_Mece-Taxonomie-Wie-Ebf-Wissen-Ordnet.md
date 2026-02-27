# MECE-Taxonomie: Wie das EBF Wissen ordnet — SSOT

**Status:** Canonical Definition | **Tags:** mece, epistemology, taxonomy, ssot, canonical

## Definition

**MECE** = **Mutually Exclusive, Collectively Exhaustive**

Ordnungssystem des EBF: Jedes wissenschaftliche Konstrukt gehört in **genau eine** von 6 Kategorien — keine Überlappung, keine Lücken.

## Die 6 Kategorien

| Kat. | Name | Was ist das? | Beispiel |
|------|------|-------------|----------|
| **1** | PRÄMISSEN | Als wahr akzeptierte Annahmen | "Additivität ist Default" (EXC-1) |
| **2** | NAMENGEBUNG | Definitionen und Symbole | "Ψ_S = soziale Dimension" |
| **3** | BEWIESENE AUSSAGEN | Aus Axiomen abgeleitet | "γ ≠ 0 impliziert Komplementarität" |
| **4** | OFFENE AUSSAGEN | Noch nicht bewiesen | "Kontext erklärt 60% der Varianz" |
| **5** | ILLUSTRATIONEN | Beispiele, Beobachtungen | Case CAS-500, Worked Example |
| **6** | PRAKTISCHE REGELN | Faustregeln | "Loss Aversion ≈ 2x in CH" |

## Die 15 Konstrukte

### Kategorie 1: PRÄMISSEN (α, ι)
- **α Axiom** — Explizite Grundannahme (structural/empirical/theoretical)
- **ι Assumption** — Implizite Annahme

### Kategorie 2: NAMENGEBUNG (δ, ν)
- **δ Definition** — Neuen Begriff benennen
- **ν Notation** — Neues Symbol einführen

### Kategorie 3: BEWIESENE AUSSAGEN (τ, π, λ, κ)
- **τ Theorem** — Hauptresultat (höchste Signifikanz)
- **π Proposition** — Wichtiges Zwischenresultat
- **λ Lemma** — Hilfsaussage für Beweis
- **κ Corollary** — Direkte Folge (max 2 Schritte)

Hierarchie: τ > π > λ > κ

### Kategorie 4: OFFENE AUSSAGEN (ξ, ω)
- **ξ Conjecture** — Spezifische Vermutung, beweisbar
- **ω Open Issue** — Forschungsfrage

### Kategorie 5: ILLUSTRATIONEN (ε, ρ, ο, φ)
- **ε Example** — Konkretes Beispiel
- **ρ Remark** — Ergänzende Bemerkung
- **ο Observation** — Empirisches Muster
- **φ Critical Foundation** — Einsicht aus Literatur

### Kategorie 6: PRAKTISCHE REGELN (η)
- **η Heuristic** — Faustregel, meist korrekt

## Vertrauensstufen (Epistemic Tags)

| Tag | Konstrukte | Konfidenz |
|-----|-----------|-----------|
| **EMP** | Empirisches Axiom, Observation | ★★★★★ |
| **THR** | Theorem, Proposition, Lemma, Definition | ★★★★☆ |
| **LLM** | LLMMC Parameter-Schätzungen | ★★★☆☆ |
| **ILL** | Example, Heuristic, Remark | ★★☆☆☆ |
| **HYP** | Conjecture, Open Issue | ★☆☆☆☆ |

**Regel:** Gesamt-Tag = schwächster Einzeltag

## Entscheidungsbaum

```
Führt Namen/Symbol ein?     → Kat. 2 (δ/ν)
Grundannahme (nicht bewiesen)? → Kat. 1 (α/ι)
Logisch abgeleitet?         → Kat. 3 (τ/π/λ/κ)
Unbewiesene Vermutung?      → Kat. 4 (ξ/ω)
Veranschaulicht etwas?      → Kat. 5 (ε/ρ/ο/φ)
Faustregel?                 → Kat. 6 (η)
```

## BEATRIX Anwendung

Jede Antwort sollte klarstellen:
- **Theorem** (bewiesen) vs **Heuristic** (Faustregel)?
- **Axiom** (Grundannahme) vs **Observation** (empirisch)?
- **Conjecture** (Vermutung)?

Beispiele:
- "Loss Aversion ≈ 2x" → **ο Observation**
- "Additivität ist Default" → **α Axiom**
- "γ(S,F) < 0 Crowding-Out" → **π Proposition**
