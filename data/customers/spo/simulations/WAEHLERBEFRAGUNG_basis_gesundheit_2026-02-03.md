# WÄHLERBEFRAGUNG-SIMULATION: Basis-Gesundheitsversorgung

**ANF-2026-02-03-002** | LLMMC Focus Group Simulation
**Datum:** 3. Februar 2026
**Simulations-ID:** SIM-SPO-GESUND-2026-02-03

---

## Methodik

**Ansatz:** EBF LLMMC (Large Language Model Monte Carlo)
**Personas:** 7 Wähler-Archetypen aus österreichischem Elektorat
**Elemente:** 6 Strategie-Elemente aus dem Wording
**Metriken:** Wahlabsicht-Delta, NPS-Delta, Kompetenz-Rating, Reaktanz-Score

---

## Die 7 Personas

| # | Persona | Profil | Aktuell | Migration-Haltung |
|---|---------|--------|---------|-------------------|
| P1 | **SPÖ-Stammwähler** | 52, Gewerkschafter, Wien | SPÖ sicher | Pro EMRK, pragmatisch |
| P2 | **Wechselwähler Mitte** | 38, Angestellte, Linz | Unentschieden | Unsicher, beeinflusst |
| P3 | **ÖVP-Enttäuschte** | 61, Pensionist, NÖ | ÖVP→? | Ordnung ja, fair ja |
| P4 | **FPÖ-Sympathisant** | 45, Handwerker, Stmk | FPÖ-nah | Restriktiv, misstrauisch |
| P5 | **Grün-NEOS Progressive** | 29, Studentin, Graz | NEOS/Grüne | Pro Menschenrechte |
| P6 | **Politikverdrossene** | 44, Verkäuferin, Sbg | Nichtwähler | "Alle gleich" |
| P7 | **Babler-Skeptiker** | 55, Selbstständig, Tirol | SPÖ früher | Zu links, unsicher |

---

## Die 6 Strategie-Elemente

| # | Element | Kernbotschaft |
|---|---------|---------------|
| E1 | **Rechtliche Unmöglichkeit** | "§ 9 ASVG sieht keine Differenzierung vor" |
| E2 | **Ökonomisches Eigentor** | "Unbehandelt → chronisch → teurer" |
| E3 | **Public Health Argument** | "Übertragbare Krankheiten gefährden ALLE" |
| E4 | **Scheinlösung entlarven** | "Notfallversorgung kann nicht verweigert werden" |
| E5 | **Zahlen-Killer** | "4,8% Bevölkerung, 2,75% Leistungen" |
| E6 | **Closer** | "Ordnung = Prävention, Chaos = Zwei-Klassen-Medizin" |

---

## Simulations-Ergebnisse

### Reaktionen pro Persona × Element

```
                  E1      E2      E3      E4      E5      E6
                 Recht   Ökon    Public  Schein  Zahlen  Closer
Persona          │       │       Health  lösung  │       │
─────────────────┼───────┼───────┼───────┼───────┼───────┼───────
P1 Stammwähler   │ +2    │ +2    │ +3    │ +2    │ +3    │ +3
P2 Wechselwähler │ +1    │ +3    │ +2    │ +2    │ +3    │ +2
P3 ÖVP-Entt.     │ +1    │ +3    │ +2    │ +1    │ +2    │ +2
P4 FPÖ-Symp.     │ -1    │ +1    │ +1    │ 0     │ +1    │ 0
P5 Progressiv    │ +2    │ +2    │ +3    │ +2    │ +2    │ +3
P6 Verdrossen    │ 0     │ +2    │ +1    │ +1    │ +2    │ +1
P7 Skeptiker     │ +1    │ +2    │ +2    │ +1    │ +2    │ +1
─────────────────┴───────┴───────┴───────┴───────┴───────┴───────
MITTELWERT:        +0.9    +2.1    +2.0    +1.3    +2.1    +1.7

Legende: -3 bis +3 (sehr negativ bis sehr positiv)
```

---

### Aggregierte Metriken

| Metrik | Baseline | Nach Wording | Delta | Bewertung |
|--------|----------|--------------|-------|-----------|
| **Wahlabsicht SPÖ** | 20.0% | 22.1% | **+2.1pp** | ✅ Positiv |
| **NPS SPÖ** | -15 | -2 | **+13** | ✅ Positiv |
| **Kompetenz Gesundheit** | 5.2/10 | 6.8/10 | **+1.6** | ✅ Stark |
| **Kompetenz Migration** | 4.1/10 | 4.9/10 | **+0.8** | ✅ Moderat |
| **Reaktanz-Score** | - | 1.2/10 | - | ✅ Niedrig |

---

### Top 3 Elemente (nach Impact)

```
┌─────────────────────────────────────────────────────────────────┐
│  🥇 E2: ÖKONOMISCHES EIGENTOR (+2.1)                            │
│     "Unbehandelt → chronisch → teurer"                         │
│     → Resoniert bei ALLEN Gruppen außer FPÖ-Kern               │
│     → Stärkstes Argument bei Wechselwählern und ÖVP-Entt.      │
├─────────────────────────────────────────────────────────────────┤
│  🥇 E5: ZAHLEN-KILLER (+2.1)                                    │
│     "4,8% Bevölkerung, 2,75% Leistungen"                       │
│     → Überraschungseffekt: "Das wusste ich nicht"              │
│     → Entkräftet "Asylwerber belasten das System"-Narrativ     │
├─────────────────────────────────────────────────────────────────┤
│  🥉 E3: PUBLIC HEALTH (+2.0)                                    │
│     "Übertragbare Krankheiten gefährden ALLE"                  │
│     → Eigeninteresse-Argument funktioniert                     │
│     → Besonders stark bei Progressiven und Stammwählern        │
└─────────────────────────────────────────────────────────────────┘
```

---

### Persona-Tiefenanalyse

#### P1: SPÖ-Stammwähler (52, Gewerkschafter, Wien)

**Baseline:** SPÖ sicher (90%)
**Nach Wording:** SPÖ sicher (95%)

> **Reaktion:** "Endlich klare Kante! Das mit den 4,8% vs. 2,75% – das muss man den Leuten sagen. Und dass das System auseinandergebaut werden müsste, das wissen die wenigsten."

**Stärkstes Element:** E5 (Zahlen) + E3 (Public Health)
**Schwächstes Element:** E1 (Recht) – "Zu technisch, aber stimmt"
**Risiko:** Keines

---

#### P2: Wechselwähler Mitte (38, Angestellte, Linz)

**Baseline:** Unentschieden (SPÖ 25%, ÖVP 30%, FPÖ 15%, andere 30%)
**Nach Wording:** SPÖ 38%, ÖVP 25%, FPÖ 12%, andere 25%

> **Reaktion:** "Ich hab mir noch nie Gedanken gemacht, dass das auch teurer werden kann. Das mit den chronischen Krankheiten leuchtet ein. Und dass Notfälle eh behandelt werden müssen – dann ist der Vorschlag ja wirklich Quatsch."

**Stärkstes Element:** E2 (Ökonomie) + E5 (Zahlen)
**Schwächstes Element:** E6 (Closer) – "Etwas zu parteipolitisch"
**Chance:** Hoch – bewegbar durch Fakten

---

#### P3: ÖVP-Enttäuschte (61, Pensionist, NÖ)

**Baseline:** ÖVP unsicher (ÖVP 40%, SPÖ 20%, FPÖ 25%)
**Nach Wording:** ÖVP 35%, SPÖ 30%, FPÖ 20%

> **Reaktion:** "Ich bin für Ordnung, aber das klingt nach Chaos. Wenn jetzt jeder Arzt entscheiden muss, was noch Basis ist... das kann ja nicht funktionieren. Und das mit den Kosten – da haben sie recht."

**Stärkstes Element:** E2 (Ökonomie) + E4 (Scheinlösung)
**Schwächstes Element:** E1 (Recht) – "Ist mir zu kompliziert"
**Chance:** Mittel – "Ordnung"-Frame funktioniert

---

#### P4: FPÖ-Sympathisant (45, Handwerker, Stmk)

**Baseline:** FPÖ (65%), ÖVP (20%), SPÖ (5%)
**Nach Wording:** FPÖ (60%), ÖVP (22%), SPÖ (8%)

> **Reaktion:** "Die SPÖ redet immer nur, warum man nix machen kann. Aber... das mit den Krankheiten, die sich ausbreiten – da hat er schon einen Punkt. Trotzdem: Die machen eh nix."

**Stärkstes Element:** E3 (Public Health) – Eigeninteresse
**Schwächstes Element:** E1 (Recht), E6 (Closer) – "Politisches Gerede"
**Risiko:** Gering – kaum bewegbar, aber nicht reaktant
**WICHTIG:** Kein Moralisieren! Nur Fakten.

---

#### P5: Grün-NEOS Progressive (29, Studentin, Graz)

**Baseline:** NEOS 35%, Grüne 35%, SPÖ 20%
**Nach Wording:** NEOS 30%, Grüne 30%, SPÖ 30%

> **Reaktion:** "Endlich sagt wer, dass das ein Systembruch wäre! Und das Public-Health-Argument – das ist wichtig. Die SPÖ klingt hier kompetenter als sonst."

**Stärkstes Element:** E3 (Public Health) + E6 (Closer)
**Schwächstes Element:** E5 (Zahlen) – "Klingt defensiv"
**Chance:** Hoch – SPÖ als kompetente Alternative

---

#### P6: Politikverdrossene (44, Verkäuferin, Sbg)

**Baseline:** Nichtwähler (70%), SPÖ (5%), ÖVP (5%), FPÖ (10%)
**Nach Wording:** Nichtwähler (55%), SPÖ (15%), ÖVP (8%), FPÖ (12%)

> **Reaktion:** "Normalerweise hör ich gar nicht hin. Aber das mit den Kosten, die später höher sind – das kenn ich von meiner Mutter. Die hat auch zu spät zum Arzt gehen wollen, und dann war alles viel schlimmer."

**Stärkstes Element:** E2 (Ökonomie) – persönlicher Bezug
**Schwächstes Element:** E1 (Recht) – "Interessiert mich nicht"
**Chance:** Mittel – Aktivierung möglich durch konkrete Beispiele

---

#### P7: Babler-Skeptiker (55, Selbstständig, Tirol)

**Baseline:** SPÖ früher (SPÖ 25%, ÖVP 40%, FPÖ 20%)
**Nach Wording:** SPÖ 32%, ÖVP 38%, FPÖ 18%

> **Reaktion:** "Der Babler ist mir zu links, aber hier redet er Vernunft. Das mit dem Systembruch – das will niemand. Und Zwei-Klassen-Medizin, das kann schnell auch mich treffen."

**Stärkstes Element:** E2 (Ökonomie) + E3 (Public Health)
**Schwächstes Element:** E6 (Closer) – "Zu viel Partei"
**Chance:** Mittel – "Vernunft"-Framing funktioniert

---

## Empfehlungen

### ✅ Stärken nutzen

| Element | Empfehlung |
|---------|------------|
| **E2 Ökonomie** | IMMER führen! "Unbehandelt → chronisch → teurer" |
| **E5 Zahlen** | Überraschungseffekt nutzen: "Das wissen die wenigsten" |
| **E3 Public Health** | Eigeninteresse betonen: "gefährdet ALLE" |

### ⚠️ Vorsicht bei

| Element | Warnung |
|---------|---------|
| **E1 Recht** | Zu technisch für breite Kommunikation – nur in Fachgesprächen |
| **E6 Closer** | Kann parteipolitisch wirken – besser: neutrale Formulierung |

### 🎯 Segment-spezifische Anpassungen

| Segment | Lead-Argument | Vermeiden |
|---------|--------------|-----------|
| **Wechselwähler** | E2 + E5 | Parteipolitik |
| **ÖVP-Enttäuschte** | E2 + E4 | ÖVP-Kritik |
| **FPÖ-Sympathisanten** | E3 (Eigeninteresse) | Moralisieren |
| **Progressive** | E3 + E6 | Defensive Zahlen |
| **Politikverdrossene** | E2 (persönlich) | Jargon |

---

## Gesamtbewertung

```
┌─────────────────────────────────────────────────────────────────┐
│  WORDING-PERFORMANCE: STARK ✅                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Wahlabsicht:        +2.1pp (20.0% → 22.1%)                    │
│  NPS:                +13 (-15 → -2)                            │
│  Kompetenz Gesundheit: +1.6 (5.2 → 6.8)                        │
│  Reaktanz:           NIEDRIG (1.2/10)                          │
│                                                                 │
│  FAZIT: Wording funktioniert über fast alle Segmente.          │
│         Ökonomisches Argument (E2) und Zahlen (E5) führen.     │
│         Kein Backfire-Risiko erkennbar.                        │
│                                                                 │
│  EMPFEHLUNG: Freigabe für Kommunikation ✅                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Vergleich mit anderen Anfragen

| Anfrage | Wahlabsicht Δ | NPS Δ | Stärkstes Element |
|---------|---------------|-------|-------------------|
| ANF-2026-02-02-001 (EMRK) | +3.2pp | +20 | Killer-Zahlen |
| **ANF-2026-02-03-002 (Gesundheit)** | **+2.1pp** | **+13** | **Ökonomie** |
| ANF-2026-01-30-001 (SOG) | n/a | n/a | (nicht simuliert) |

**Konsistenz:** Das "Ordnung statt Spalten"-Frame funktioniert konsistent über Themen hinweg.

---

*Erstellt mit EBF LLMMC Framework | FehrAdvice & Partners AG*
*Methodik: CAT-21 (Political Psychology), CAT-05 (Behavioral Economics)*
