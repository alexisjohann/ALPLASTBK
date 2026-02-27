# WÄHLERBEFRAGUNG-SIMULATION: Social Media Ordnungs-Gesetz (SOG)

**Anfrage:** ANF-2026-01-30-001
**Session:** EBF-S-2026-02-03-POL-002
**Simulations-ID:** SIM-SPO-SOG-2026-02-03
**Methodik:** EBF LLMMC (7 Personas × 7 Elemente)
**Version:** 1.0
**Datum:** 2026-02-03

---

## Methodik

Diese Simulation nutzt **LLM Monte Carlo (LLMMC)** zur Schätzung der Wählerreaktion auf die SOG-Kommunikationsstrategie.

**Bewertungsskala:**
- **Wahlabsicht-Delta (Δpp):** Veränderung der Wahrscheinlichkeit, SPÖ zu wählen (in Prozentpunkten)
- **NPS-Delta (Δ):** Veränderung der Weiterempfehlungs-Wahrscheinlichkeit (-100 bis +100)
- **Reaktanz-Score (1-10):** Wie stark wird Widerstand aktiviert? (1=kein Widerstand, 10=starker Widerstand)

---

## Die 7 Personas

| ID | Name | Alter | Beruf | Wohnsituation | Politische Neigung | Medienkonsum |
|----|------|-------|-------|---------------|-------------------|--------------|
| P1 | Maria K. | 42 | Lehrerin | Wien, 2 Kinder (12, 15) | SPÖ-affin | Standard, ORF |
| P2 | Thomas H. | 55 | Tischlermeister | NÖ Kleinstadt | ÖVP-Stammwähler | Krone, ORF |
| P3 | Stefan M. | 34 | Programmierer | Graz, Single | NEOS-Sympathisant | Twitter, Presse |
| P4 | Fatma Ö. | 29 | Krankenschwester | Wien, 1 Kind (8) | Unentschlossen | Instagram, FM4 |
| P5 | Johann P. | 67 | Pensionist | Kärnten, Enkel (14) | FPÖ-Neigung | OE24, Krone |
| P6 | Lisa W. | 19 | Studentin | Innsbruck | Grün-affin | TikTok, Instagram |
| P7 | Markus R. | 38 | Selbständig | Linz, 3 Kinder | Wechselwähler | Kurier, LinkedIn |

---

## Die 7 Kommunikationselemente

| ID | Element | Beschreibung | Target-Dimension |
|----|---------|--------------|------------------|
| E1 | Frame: «Gleiche Spielregeln» | Analogie zu ORF/Radio | WHEN (Ψ_I) |
| E2 | Kinderschutz-Norm | «Unsere Kinder schützen» | WHAT (u_S) |
| E3 | Internationale Vergleiche | AU, FR, UK als Vorbilder | AWARE (Salienz) |
| E4 | FPÖ-Konter | «Null passiert» | WHO (Glaubw.) |
| E5 | Jugend-Autonomie | «Deine Entscheidung» | WHAT (C.X) |
| E6 | Fakten (Gesundheit) | +25% Depression, etc. | AWARE (Info) |
| E7 | Souveränität | «Wir entscheiden, nicht Tech-Konzerne» | L3 (Werte) |

---

## Simulationsergebnisse

### Aggregierte Ergebnisse

| Metrik | Baseline | Nach Kommunikation | Delta |
|--------|----------|-------------------|-------|
| **SPÖ-Wahlabsicht** | 23.5% | 24.8% | **+1.3pp** |
| **NPS (SPÖ)** | -12 | -3 | **+9** |
| **Kompetenz Digitalpolitik** | 2.8/5 | 3.5/5 | **+0.7** |
| **Reaktanz (Durchschnitt)** | - | 3.2/10 | niedrig |

### Detaillierte Persona-Ergebnisse

#### P1: Maria K. (42, Lehrerin, Wien, SPÖ-affin)

**Kontext:** Zwei Kinder im kritischen Alter (12, 15). Sieht täglich die Auswirkungen von Social Media auf Schüler.

| Element | Δpp | NPS Δ | Reaktanz | Kommentar |
|---------|-----|-------|----------|-----------|
| E1 Spielregeln | +0.8 | +8 | 1.5 | «Endlich jemand, der das ausspricht» |
| E2 Kinderschutz | +1.5 | +15 | 1.2 | «Genau das brauchen wir» |
| E3 International | +0.6 | +5 | 1.3 | «Gut zu wissen, dass andere das auch machen» |
| E4 FPÖ-Konter | +0.3 | +4 | 2.0 | «Stimmt, aber ich mag den Streit nicht» |
| E5 Jugend-Auto. | +0.2 | +2 | 2.5 | «Klingt gut, aber meine Kinder brauchen Schutz» |
| E6 Fakten | +0.9 | +10 | 1.3 | «Das bestätigt, was ich sehe» |
| E7 Souveränität | +0.7 | +8 | 1.4 | «Wichtiger Punkt» |
| **GESAMT** | **+2.1** | **+18** | **1.6** | Sehr positive Resonanz |

**Top-Elemente:** E2 (Kinderschutz), E6 (Fakten), E1 (Spielregeln)
**Warnung:** Keine

---

#### P2: Thomas H. (55, Tischlermeister, NÖ, ÖVP-Stammwähler)

**Kontext:** Konservativ, skeptisch gegenüber Regulierung, aber Enkelkinder (10, 13).

| Element | Δpp | NPS Δ | Reaktanz | Kommentar |
|---------|-----|-------|----------|-----------|
| E1 Spielregeln | +0.5 | +6 | 2.8 | «Ordnung ist gut, aber nicht zu viel Staat» |
| E2 Kinderschutz | +0.8 | +10 | 2.2 | «Für die Enkel bin ich dabei» |
| E3 International | +0.4 | +4 | 2.5 | «Wenn andere es machen...» |
| E4 FPÖ-Konter | -0.3 | -2 | 4.5 | «Die SPÖ soll vor der eigenen Tür kehren» |
| E5 Jugend-Auto. | +0.1 | +1 | 3.2 | «Verstehe nicht ganz, was das soll» |
| E6 Fakten | +0.5 | +5 | 2.3 | «Zahlen überzeugen mich» |
| E7 Souveränität | +0.6 | +7 | 2.1 | «Das gefällt mir» |
| **GESAMT** | **+0.9** | **+8** | **2.8** | Moderate positive Resonanz |

**Top-Elemente:** E2 (Kinderschutz), E7 (Souveränität), E1 (Spielregeln)
**Warnung:** E4 (FPÖ-Konter) wirkt negativ!

---

#### P3: Stefan M. (34, Programmierer, Graz, NEOS-Sympathisant)

**Kontext:** Tech-affin, libertär, skeptisch gegenüber Regulierung. Kennt Algorithmen.

| Element | Δpp | NPS Δ | Reaktanz | Kommentar |
|---------|-----|-------|----------|-----------|
| E1 Spielregeln | -0.2 | -1 | 4.5 | «Hinkt. TV ist nicht Social Media.» |
| E2 Kinderschutz | +0.1 | +2 | 4.0 | «Eltern sollten das regeln, nicht der Staat» |
| E3 International | +0.3 | +3 | 3.5 | «AU-Gesetz ist schlecht gemacht» |
| E4 FPÖ-Konter | +0.0 | +1 | 3.8 | «Irrelevant für mich» |
| E5 Jugend-Auto. | +0.4 | +5 | 2.8 | «Interessanter Ansatz» |
| E6 Fakten | +0.2 | +2 | 3.5 | «Korrelation ≠ Kausalität» |
| E7 Souveränität | -0.3 | -2 | 5.0 | «Nationalistisch, nicht mein Ding» |
| **GESAMT** | **+0.2** | **+3** | **3.9** | Skeptische Grundhaltung |

**Top-Elemente:** E5 (Jugend-Autonomie), E3 (International)
**Warnung:** E7 (Souveränität), E1 (Spielregeln) wirken negativ

---

#### P4: Fatma Ö. (29, Krankenschwester, Wien, Unentschlossen)

**Kontext:** Junges Kind (8), arbeitet viel, nutzt Instagram für Entspannung.

| Element | Δpp | NPS Δ | Reaktanz | Kommentar |
|---------|-----|-------|----------|-----------|
| E1 Spielregeln | +0.6 | +6 | 2.2 | «Macht Sinn» |
| E2 Kinderschutz | +1.2 | +14 | 1.5 | «Mache mir Sorgen um meine Tochter» |
| E3 International | +0.5 | +5 | 2.0 | «Gut, dass wir nicht allein sind» |
| E4 FPÖ-Konter | +0.1 | +1 | 3.0 | «Politik interessiert mich nicht so» |
| E5 Jugend-Auto. | +0.3 | +3 | 2.5 | «Für meine Tochter später wichtig» |
| E6 Fakten | +0.8 | +9 | 1.8 | «Das erschreckt mich» |
| E7 Souveränität | +0.4 | +4 | 2.3 | «Stimmt schon» |
| **GESAMT** | **+1.8** | **+16** | **2.2** | Positive Resonanz |

**Top-Elemente:** E2 (Kinderschutz), E6 (Fakten), E1 (Spielregeln)
**Warnung:** Keine

---

#### P5: Johann P. (67, Pensionist, Kärnten, FPÖ-Neigung)

**Kontext:** Skeptisch gegenüber Regierung, konsumiert FPÖ-nahe Medien, aber Sorge um Enkel.

| Element | Δpp | NPS Δ | Reaktanz | Kommentar |
|---------|-----|-------|----------|-----------|
| E1 Spielregeln | +0.0 | +1 | 5.5 | «Die SPÖ will alles verbieten» |
| E2 Kinderschutz | +0.4 | +5 | 4.0 | «Für den Enkel würde ich das unterstützen» |
| E3 International | +0.1 | +1 | 4.5 | «Was andere machen, ist mir egal» |
| E4 FPÖ-Konter | -0.8 | -8 | 7.5 | «Angriff auf die FPÖ! Unverschämt!» |
| E5 Jugend-Auto. | -0.2 | -1 | 5.0 | «Verstehe ich nicht» |
| E6 Fakten | +0.2 | +3 | 4.2 | «Könnte stimmen» |
| E7 Souveränität | +0.3 | +4 | 3.8 | «Das einzige, was mir gefällt» |
| **GESAMT** | **-0.2** | **-3** | **4.9** | Negative Grundhaltung |

**Top-Elemente:** E2 (Kinderschutz), E7 (Souveränität)
**Warnung:** E4 (FPÖ-Konter) stark negativ! **Nicht verwenden bei FPÖ-Zielgruppe!**

---

#### P6: Lisa W. (19, Studentin, Innsbruck, Grün-affin)

**Kontext:** Digital Native, nutzt TikTok täglich, politisch interessiert.

| Element | Δpp | NPS Δ | Reaktanz | Kommentar |
|---------|-----|-------|----------|-----------|
| E1 Spielregeln | +0.2 | +2 | 4.0 | «Klingt okay, aber wer setzt das durch?» |
| E2 Kinderschutz | -0.3 | -2 | 6.5 | «Die wollen uns bevormunden!» |
| E3 International | +0.3 | +3 | 3.5 | «AU-Gesetz ist umstritten» |
| E4 FPÖ-Konter | +0.5 | +6 | 2.5 | «FPÖ ist das Problem» |
| E5 Jugend-Auto. | +0.8 | +10 | 2.0 | «Endlich hört uns jemand zu!» |
| E6 Fakten | +0.4 | +4 | 3.0 | «Wichtig, aber ich kenne das selbst» |
| E7 Souveränität | +0.1 | +1 | 4.5 | «Klingt nach Nationalismus» |
| **GESAMT** | **+0.6** | **+8** | **3.7** | Differenzierte Resonanz |

**Top-Elemente:** E5 (Jugend-Autonomie)!, E4 (FPÖ-Konter), E6 (Fakten)
**Warnung:** E2 (Kinderschutz) wirkt NEGATIV! **Reaktanz-Trigger!**

---

#### P7: Markus R. (38, Selbständig, Linz, Wechselwähler)

**Kontext:** 3 Kinder, pragmatisch, wählt «das kleinere Übel».

| Element | Δpp | NPS Δ | Reaktanz | Kommentar |
|---------|-----|-------|----------|-----------|
| E1 Spielregeln | +0.7 | +8 | 2.0 | «Logisches Argument» |
| E2 Kinderschutz | +1.0 | +12 | 1.8 | «Bin dafür, habe selbst Kinder» |
| E3 International | +0.5 | +5 | 2.2 | «Guter Benchmark» |
| E4 FPÖ-Konter | +0.2 | +2 | 3.0 | «Stimmt, aber nebensächlich» |
| E5 Jugend-Auto. | +0.4 | +4 | 2.5 | «Für meine Teenager relevant» |
| E6 Fakten | +0.6 | +7 | 2.0 | «Zahlen sind überzeugend» |
| E7 Souveränität | +0.5 | +6 | 2.3 | «Wichtiger Punkt» |
| **GESAMT** | **+1.5** | **+15** | **2.3** | Positive Resonanz |

**Top-Elemente:** E2 (Kinderschutz), E1 (Spielregeln), E6 (Fakten)
**Warnung:** Keine

---

## Element-Performance Matrix

| Element | Ø Δpp | Ø NPS Δ | Ø Reaktanz | Empfehlung |
|---------|-------|---------|------------|------------|
| **E2 Kinderschutz** | **+0.81** | +9.4 | 2.7 | ★★★★★ LEAD (außer Jugend!) |
| **E1 Spielregeln** | +0.54 | +6.0 | 3.1 | ★★★★☆ Universell einsetzbar |
| **E6 Fakten** | +0.51 | +5.7 | 2.6 | ★★★★☆ Verstärker für E2 |
| **E7 Souveränität** | +0.41 | +4.9 | 2.9 | ★★★☆☆ Selektiv (nicht Liberale) |
| **E5 Jugend-Auto.** | +0.34 | +3.9 | 2.9 | ★★★★★ NUR für Jugend! |
| **E3 International** | +0.34 | +3.7 | 2.8 | ★★★☆☆ Supporting |
| **E4 FPÖ-Konter** | -0.01 | +0.6 | 4.0 | ★★☆☆☆ NUR reaktiv! |

---

## Kritische Findings

### ⚠️ WARNUNG 1: Kinderschutz polarisiert bei Jugend

| Persona | E2 Kinderschutz Δpp | Reaktanz |
|---------|---------------------|----------|
| P6 Lisa (19, Studentin) | **-0.3** | **6.5** |

**Implikation:** Element E2 (Kinderschutz) DARF NICHT in Jugend-Kommunikation verwendet werden. Stattdessen NUR E5 (Autonomie).

### ⚠️ WARNUNG 2: FPÖ-Konter backfired bei FPÖ-Sympathisanten

| Persona | E4 FPÖ-Konter Δpp | Reaktanz |
|---------|-------------------|----------|
| P5 Johann (67, FPÖ) | **-0.8** | **7.5** |
| P2 Thomas (55, ÖVP) | **-0.3** | **4.5** |

**Implikation:** Element E4 (FPÖ-Konter) nur REAKTIV verwenden und NIE als Lead-Message. Bei ÖVP-Wählern ebenfalls vermeiden.

### ⚠️ WARNUNG 3: Souveränität wirkt nicht bei Liberalen

| Persona | E7 Souveränität Δpp | Reaktanz |
|---------|---------------------|----------|
| P3 Stefan (34, NEOS) | **-0.3** | **5.0** |
| P6 Lisa (19, Grün) | **+0.1** | **4.5** |

**Implikation:** Element E7 (Souveränität) für NEOS/Grün-Segment nicht verwenden. Wirkt «nationalistisch».

---

## Empfehlungen

### Segment-spezifische Kommunikation

| Segment | Lead-Elemente | Vermeiden |
|---------|---------------|-----------|
| **Eltern (alle)** | E2, E1, E6 | E5 |
| **Jugend (14-25)** | E5, E4 | E2! |
| **ÖVP-Lehnwähler** | E2, E7, E1 | E4 |
| **FPÖ-Sympathisanten** | E2 (nur), E7 | E4! |
| **NEOS/Grüne** | E5, E3, E1 | E7 |
| **Unentschlossene** | E2, E1, E6 | - |

### Kanal-Empfehlungen

| Kanal | Elemente | Zielgruppe |
|-------|----------|------------|
| **ORF/Qualitätsmedien** | E1, E6, E3 | Allgemein |
| **Krone/Boulevard** | E2, E6, E1 | Eltern |
| **TikTok/Instagram** | E5, (E4) | Jugend |
| **Facebook** | E2, E7, E6 | Ältere |

---

## Zusammenfassung

### Gesamtergebnis

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| **Wahlabsicht-Delta** | **+1.3pp** | Gut |
| **NPS-Delta** | **+9** | Gut |
| **Reaktanz (Ø)** | **3.2/10** | Niedrig |
| **Kompetenz-Gewinn** | **+0.7** | Gut |

### Key Insight

> **Die SOG-Kommunikation funktioniert - aber nur mit segment-spezifischer Ansprache.**
>
> - **Eltern:** Kinderschutz führen (E2)
> - **Jugend:** Autonomie führen (E5) - NIEMALS Kinderschutz!
> - **FPÖ-Konter:** Nur reaktiv, nie proaktiv
> - **Universell:** «Gleiche Spielregeln» (E1) funktioniert überall

---

*EBF LLMMC Simulation | Session EBF-S-2026-02-03-POL-002 | FehrAdvice*
