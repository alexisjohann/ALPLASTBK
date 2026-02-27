# MECE-Taxonomie: Wie das EBF Wissen ordnet

> **SSOT:** `quality/instruments/epistemology_mece_taxonomy.md`
> **Upload-Tags:** canonical, mece, epistemology, ebf, ssot, taxonomy
> **Prioritaet:** HOCH — stellt sicher dass BEATRIX Konstrukte korrekt klassifiziert

---

## Was ist MECE?

**MECE** steht fuer **Mutually Exclusive, Collectively Exhaustive**.

Es ist das Ordnungssystem des EBF: Jedes wissenschaftliche Konstrukt (Axiom, Theorem, Beispiel, Heuristik etc.) gehoert in **genau eine** von 6 Kategorien — keine Ueberlappung, keine Luecken.

---

## Die 6 Kategorien auf einen Blick

| Kat. | Name | Was ist das? | Beispiel im EBF |
|------|------|-------------|------------------|
| **1** | PRAEMISSEN | Annahmen die als wahr akzeptiert werden | "Additivitaet ist Default" (EXC-1) |
| **2** | NAMENGEBUNG | Definitionen und Symbole | "Ψ_S = soziale Dimension" |
| **3** | BEWIESENE AUSSAGEN | Aus Axiomen abgeleitete Resultate | "γ ≠ 0 impliziert Komplementaritaet" |
| **4** | OFFENE AUSSAGEN | Noch nicht bewiesene Vermutungen | "Kontext erklaert 60% der Varianz" |
| **5** | ILLUSTRATIONEN | Beispiele und Beobachtungen | Case CAS-500, Worked Example |
| **6** | PRAKTISCHE REGELN | Faustregeln die meist funktionieren | "Loss Aversion ≈ 2x in der Schweiz" |

---

## Die 15 Konstrukte im Detail

### Kategorie 1: PRAEMISSEN (Inputs — als wahr akzeptiert)

| Symbol | Konstrukt | Wann verwenden? |
|--------|-----------|-----------------|
| **α** | **Axiom** | Explizite, nummerierte Grundannahme |
| **ι** | **Assumption** | Implizite Annahme |

Axiome haben 3 Subtypen:
- `structural` — Modellierungsentscheidung (z.B. "Utility ist additiv")
- `empirical` — Empirische Tatsache mit Quellenangabe
- `theoretical` — Von externer Theorie importiert

### Kategorie 2: NAMENGEBUNG (Tautologisch — fuehrt Namen ein)

| Symbol | Konstrukt | Wann verwenden? |
|--------|-----------|-----------------|
| **δ** | **Definition** | Neuen Begriff benennen (Bedeutung erklaeren) |
| **ν** | **Notation** | Neues Symbol einfuehren (nur Zeichen) |

### Kategorie 3: BEWIESENE AUSSAGEN (Outputs — logisch abgeleitet)

| Symbol | Konstrukt | Signifikanz | Wann verwenden? |
|--------|-----------|-------------|-----------------|
| **τ** | **Theorem** | Hoch | Hauptresultat, zentrale Erkenntnis |
| **π** | **Proposition** | Mittel | Wichtiges Zwischenresultat |
| **λ** | **Lemma** | Gering | Hilfsaussage fuer Theorem-Beweis |
| **κ** | **Corollary** | Abhaengig | Direkte Folge aus Theorem (max 2 Schritte) |

Hierarchie: Theorem > Proposition > Lemma > Corollary

### Kategorie 4: OFFENE AUSSAGEN (Noch nicht bewiesen)

| Symbol | Konstrukt | Wann verwenden? |
|--------|-----------|-----------------|
| **ξ** | **Conjecture** | Spezifische Vermutung, prinzipiell beweisbar |
| **ω** | **Open Issue** | Forschungsfrage, noch nicht praezise genug |

### Kategorie 5: ILLUSTRATIONEN (Veranschaulichung)

| Symbol | Konstrukt | Wann verwenden? |
|--------|-----------|-----------------|
| **ε** | **Example** | Konkretes Beispiel fuer abstraktes Konzept |
| **ρ** | **Remark** | Ergaenzende Bemerkung oder Vergleich |
| **ο** | **Observation** | Empirisches Muster (ohne formalen Beweis) |
| **φ** | **Critical Foundation** | Zentrale Einsicht aus externer Literatur |

### Kategorie 6: PRAKTISCHE REGELN (Heuristiken)

| Symbol | Konstrukt | Wann verwenden? |
|--------|-----------|-----------------|
| **η** | **Heuristic** | Praktische Faustregel, meist korrekt, keine Garantie |

---

## Entscheidungsbaum: Welches Konstrukt?

```
Was ist die Natur der Aussage?
│
├─ Fuehrt einen Namen oder ein Symbol ein?
│  └─ → KATEGORIE 2 (Definition oder Notation)
│
├─ Ist eine Grundannahme (nicht bewiesen)?
│  └─ → KATEGORIE 1 (Axiom oder Assumption)
│
├─ Ist logisch aus Axiomen abgeleitet?
│  └─ → KATEGORIE 3 (Theorem / Proposition / Lemma / Corollary)
│
├─ Ist eine unbewiesene Vermutung?
│  └─ → KATEGORIE 4 (Conjecture oder Open Issue)
│
├─ Veranschaulicht oder illustriert etwas?
│  └─ → KATEGORIE 5 (Example / Remark / Observation / Critical Foundation)
│
└─ Ist eine Faustregel die meist funktioniert?
   └─ → KATEGORIE 6 (Heuristic)
```

---

## Vertrauensstufen (Epistemic Tags)

| Tag | Konstrukte | Konfidenz |
|-----|-----------|-----------|
| **EMP** | Empirisches Axiom, Observation | ★★★★★ (hoechste) |
| **THR** | Theorem, Proposition, Lemma, Definition | ★★★★☆ |
| **LLM** | Parameter-Schaetzungen (LLMMC) | ★★★☆☆ |
| **ILL** | Example, Heuristic, Remark | ★★☆☆☆ |
| **HYP** | Conjecture, Open Issue | ★☆☆☆☆ (niedrigste) |

**Wichtig:** Der Gesamt-Tag ist immer der schwaechste Einzeltag. Wenn eine Aussage auf einem Theorem (THR) und einer Heuristik (ILL) basiert, ist der Gesamt-Tag ILL.

---

## Warum ist MECE wichtig?

1. **Qualitaetssicherung:** Jede Aussage im EBF wird explizit klassifiziert
2. **Transparenz:** Der Nutzer weiss sofort, ob etwas bewiesen (Theorem) oder eine Faustregel (Heuristik) ist
3. **Keine Verwechslungen:** Ein Axiom wird nicht als Beweis praesentiert, eine Vermutung nicht als Fakt
4. **Vollstaendigkeit:** Nichts faellt durch die Maschen — jedes Konstrukt hat einen Platz

---

## Anwendung in BEATRIX

Wenn BEATRIX eine Antwort formuliert, sollte klar sein:
- Basiert die Aussage auf einem **Theorem** (bewiesen) oder einer **Heuristik** (Faustregel)?
- Ist es ein **Axiom** (Grundannahme) oder eine **Observation** (empirisches Muster)?
- Handelt es sich um eine **Conjecture** (unbewiesene Vermutung)?

Beispiel:
- "Loss Aversion ≈ 2x" → **Observation** (ο) — empirisch beobachtet, kein Theorem
- "Additivitaet ist Default (EXC-1)" → **Axiom** (α) — Grundannahme des EBF
- "γ(Social, Financial) < 0" → **Proposition** (π) — aus Crowding-Out-Literatur abgeleitet

---

*Quelle: quality/instruments/epistemology_mece_taxonomy.md (v2.3, 2026-01-20)*
