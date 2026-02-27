# Interventionen im EBF: Der 9D-Vektor

> **SSOT:** `CLAUDE.md` (Interventions-Sektion), `templates/intervention-schema.yaml`
> **Upload-Tags:** canonical, intervention, eit, 9d, ebf, ssot
> **Prioritaet:** HOCH — erklaert wie Interventionen im EBF designt werden

---

## Was ist eine Intervention im EBF?

Eine Intervention ist **KEIN** ad-hoc Ratschlag. Im EBF ist jede Intervention ein **9-dimensionaler Vektor**:

```
I⃗ ∈ [0,1]⁹
```

Das bedeutet: Jede Intervention wird als Punkt in einem 9-dimensionalen Raum beschrieben, wobei jede Dimension einer der ersten 9 COREs des 10C Frameworks entspricht.

---

## Warum 9D bei 10C Framework?

| Konzept | Erklaerung |
|---------|------------|
| **10C** | Das theoretische Framework (10 CORE Fragen) |
| **9D** | Der Interventionsvektor (targetiert COREs 1-9) |
| **EIT** | CORE 10 — ist die *Methodologie* fuer Interventionen, nicht ein Target selbst |

Die 9 Zieldimensionen sind:

```
WHO → WHAT → HOW → WHEN → WHERE → AWARE → READY → STAGE → HIERARCHY
 1      2      3     4      5       6       7       8        9
```

---

## Die 10C-Zieldimensionen fuer Interventionen

| 10C-Target | Δ-Ziel | Typische Interventionen |
|------------|--------|-------------------------|
| **AWARE** (AU) | A(·)↑ | Information, Salience, Aufmerksamkeit erhoehen |
| **AWARE** (AU) | κ_AWX↑ | Feedback, Tracking, Bewusstseins-Loops |
| **WHEN** (V) | κ_KON→ | Choice Architecture, Defaults aendern |
| **WHEN** (V) | κ_JNY→ | Timing, Urgency, Deadlines setzen |
| **WHAT** (C.X) | W_base↑ | Selbstkonzept, Rollenidentitaet staerken |
| **WHAT** (C.S) | u_S↑ | Soziale Normen, Peer Effects, Anerkennung |
| **WHAT** (C.F) | u_F↑ | Monetaere Anreize, Kompensation |
| **HOW** (B) | γ_ij→ | Pre-Commitment, Zielsetzung, Bundling |

---

## WARNUNG: Crowding-Out bei Interventionen

**Nicht jede Kombination funktioniert!** Bekannte Konflikte:

```
Social + Financial → γ = -0.2 (GEFAEHRLICH)
  → Finanzielle Anreize untergraben soziale Normen

Financial + Commitment → γ = -0.3 (GEFAEHRLICH)
  → Externe Belohnungen untergraben intrinsische Motivation
```

**Goldene Regel:** NIEMALS Social (u_S) und Financial (u_F) kombinieren ohne Crowding-Out-Analyse!

---

## Phase-Affinity (α-Werte)

Nicht jede Intervention wirkt in jeder Phase der Verhaltensaenderung gleich:

```
α > 0.7:  Stark empfohlen ✅
α 0.5-0.7: Mit Vorsicht empfohlen ⚠️
α 0.3-0.5: Suboptimal
α < 0.3:  Nicht empfohlen ❌
```

Beispiel: Information (AWARE-Intervention) wirkt stark in fruehen Phasen (α = 0.8), aber schwach in spaeten Phasen (α = 0.3).

---

## Segment-Multiplier (σ-Werte)

Interventionen wirken unterschiedlich stark je nach Zielgruppe:

```
σ > 1.3:  Sehr effektiv fuer dieses Segment ✅
σ < 0.5:  Nicht empfohlen fuer dieses Segment ⚠️
σ < 0:    BACKFIRE RISK ❌ (Intervention schadet!)
```

**KRITISCH:** Bei σ < 0 muss das Segment explizit gewarnt werden!

---

## Das 20-Field Schema

Jede vollstaendige Intervention wird im EBF mit 20 Feldern beschrieben:

| Felder | Inhalt |
|--------|--------|
| **F1-F6** | Basis (Name, Typ, 10C-Ziel, Beschreibung, Zielgruppe, Phase) |
| **F7-F12** | Mechanismen (Theorie, Parameter, α-Wert, σ-Wert, Autonomie, Scope) |
| **F13-F20** | Validierung (Evidenz, Risiken, γ-Werte, Kosten, Timeline, KPIs, Portfolio, Review) |

3 Modi verfuegbar:
- **SCHNELL** (F1-F6): 10 Minuten
- **STANDARD** (F1-F12): 30 Minuten
- **VOLLSTAENDIG** (F1-F20): 60 Minuten

---

## Vom manuellen BCM zur digitalen Intervention

Im manuellen BCM (seit 2010) wurde der Interventions-Mix aus der **Awareness/Willingness-Matrix** abgeleitet:

| A/W-Position | Interventions-Strategie |
|-------------|------------------------|
| Hohe A + Hohe W | Komplementaerer Nudge-Mix zum bestehenden Massnahmenset |
| Niedrige A + Hohe W | Awareness-Mix + Nudge-Mix (sequenziell) |
| Hohe A + Niedrige W | Motivations-Mix (ACHTUNG: Crowding-Out-Risiko!) |
| Niedrige A + Niedrige W | Sequenziell: ZUERST Awareness, DANN Willingness |

Der abgeleitete Mix wurde dann im Rahmen eines **experimentellen Online-Experiments** abgetestet.

BEATRIX formalisiert diesen manuellen Prozess: Die A/W-Matrix wird zum kontinuierlichen A/W-Raum, der High-Level-Mix zum 9D-Interventionsvektor I⃗ ∈ [0,1]⁹.

→ Details: **KB-BCM-001** (BCM als Prediction Engine)

---

## Was BEATRIX bei Interventions-Fragen tut

1. **10C-Zieldimension** identifizieren (PFLICHT)
2. **Phase-Affinity** pruefen (welche Phase der Journey?)
3. **Segment-Multiplier** pruefen (welche Zielgruppe?)
4. **Crowding-Out** pruefen (gefaehrliche Kombinationen?)
5. Intervention im 20-Field Schema beschreiben

---

## Was BEATRIX NICHT tut

- Keine ad-hoc Listen von «5 Tipps»
- Keine Interventionen ohne 10C-Zuordnung
- Keine Kombination von Social + Financial ohne Warnung
- Keine Interventionen ohne Phasen-Pruefung

---

*Quelle: CLAUDE.md (Interventions-Sektion), templates/intervention-schema.yaml, Appendix IE (CORE-EIT)*
