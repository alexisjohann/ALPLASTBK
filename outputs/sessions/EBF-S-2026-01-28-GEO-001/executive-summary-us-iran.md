# EXECUTIVE SUMMARY
## US-Iran Crisis Escalation Model

**28. Januar 2026** | Session: EBF-S-2026-01-28-GEO-001

---

## FRAGESTELLUNG

Wie wahrscheinlich ist ein US-Militärschlag gegen Iran in den nächsten 48 Stunden?

---

## METHODIK

**Sequential Game** (Spieltheorie) mit 2 Hauptakteuren und je 3 Strategien, gelöst via **Backward Induction**. Parameter aus LLMMC-Prior + Bayesian Update mit aktueller Nachrichtenlage.

**Kontext-Dimensionen:** Temporal (frühe Amtszeit), Sozial (5'002 Tote bei Protesten), Ressourcen (USS Abraham Lincoln vor Ort), Kultur (Face-Saving beidseitig).

---

## KEY FINDING

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│     P(US-MILITÄRSCHLAG IN 48h) = 18%  [12%-25%]                    │
│                                                                     │
│     ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░              │
│                                                                     │
│     GLEICHGEWICHT: Verhandlung → Deal (Pareto-optimal)             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## GAME TREE (Vereinfacht)

```
                              USA
                             / | \
                           /   |   \
                         /     |     \
                   DROHEN    STRIKE   VERHANDELN ←── GLEICHGEWICHT
                     |         |           |
                    IRAN      IRAN        IRAN
                   / | \     / | \       / | \
                 /   |  \   /  |  \     /  |  \
              TROTZ NACHG. VERGELT. ABSORB. ACCEPT REJECT
                |     |      |       |       |      |
               USA  ENDE    USA    ENDE    DEAL ←─ BESTES OUTCOME
              / \          / \            (+5.3/+2.3)
         STRIKE ZURÜCK  ESKL. DE-ESK.

Legende: Zahlen = (U_USA / U_Iran), normalisiert [-10, +10]
Grün markiert: Gleichgewichtspfad
```

---

## TRIGGER-SZENARIEN

| Status | Trigger-Ereignis | P(Strike) | Δ vs. Baseline |
|:------:|-----------------|:---------:|:--------------:|
| 🔴 | Iran exekutiert Demonstranten | 45% | +27% |
| 🔴 | Proxy greift US-Truppen an | 60% | +42% |
| 🟡 | Trump-Tweet mit Deadline | 33% | +15% |
| 🟢 | Direkter Trump-Iran Call | 5% | -13% |

**Aktuell:** Davos-Signal (24.01.) de-eskalierend, aber Armada vor Ort hält Drohkulisse aufrecht.

---

## INTERPRETATION

> «Das rationale Gleichgewicht ist Verhandlung – beide Seiten gewinnen mehr durch einen Deal als durch Krieg. Die Gefahr liegt nicht im Kalkül, sondern in **Trigger-Ereignissen** (Hinrichtungen, Proxy-Angriffe), **Trumps Impulsivität** und **Irans Face-Saving-Zwang**.
>
> Die maximale Drohkulisse dient der Verhandlung, nicht dem Krieg. Klassische **Coercive Diplomacy**.»

---

## QUELLEN

- Al Jazeera: Iran rejects Trump's threats (28.01.2026)
- Military.com: USS Abraham Lincoln arrives (26.01.2026)
- Washington Post: Trump hints at Iran decision (13.01.2026)
- RFE/RL: Likelihood of strikes 'very high' (26.01.2026)

**Methodik:** Evidence-Based Framework (EBF), Game Theory (Selten 1965), LLMMC

---

**Modell-ID:** MOD-GEO-001 | **Session:** EBF-S-2026-01-28-GEO-001

---

**FehrAdvice & Partners AG** | Prof. Ernst Fehr | www.fehradvice.com

*Evidence-Based Framework for Economic and Social Behavior (EBF)*
