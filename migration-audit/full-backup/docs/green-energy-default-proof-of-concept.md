# Proof of Concept: Green Energy Default (A10)

> **Zeigt:** Wie α den Kontext formalisiert, ohne U zu verändern.

---

## 1. Der Fall

**Intervention:** Green Energy Default (Opt-out statt Opt-in)
**Kontext:** Deutsche Haushalte, Energieversorger
**Quelle:** Ebeling & Lotz (2015), Energy Policy

**Die Fakten:**

| Szenario | Wahl "Grün" | Mechanismus |
|----------|-------------|-------------|
| Opt-in (Standard grau) | < 1% | Aktive Wahl erforderlich |
| Opt-out (Standard grün) | **69.1%** | Bleiben beim Default |

**Effekt:** Δ = 69pp
- 41,952 Haushalte
- Tier-1 Evidenz

---

## 2. Stage 1: Die α-Analyse (Der Filter)

> *Hier fragen wir nicht "Wollen die Leute Grün?", sondern "Passt das Instrument Default hier?"*

### 2.1 Der Kontext-Check (Ψ)

```
┌─────────────────────────────────────────────────────────────┐
│  KONTEXT-DIAGNOSE                                           │
├─────────────────────────────────────────────────────────────┤
│  Ψ₁ Low Attention:                                          │
│      → Strom = "Low-Involvement"-Gut                        │
│      → Niemand denkt aktiv über Tarife nach                 │
│                                                             │
│  Ψ₂ Decision Cost:                                          │
│      → Tarifwechsel = nervig (Formulare, Recherche)         │
│      → Selbst kleine Barrieren wirken prohibitiv            │
│                                                             │
│  Ψ₃ Trust:                                                  │
│      → Stadtwerke gelten als seriös                         │
│      → Default wird als implizite Empfehlung gesehen        │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Der Mechanismus-Check (a)

**Was tut ein Default?**
- Nutzt **Trägheit** (Inertia)
- Setzt **implizite Empfehlung** (Social Proof)
- Reduziert **Handlungskosten** auf null

### 2.3 Das Match: α = Fit(a, Ψ)

```
Mechanismus (a):     Trägheit nutzen, Handlungskosten eliminieren
         ↓
Kontext (Ψ):         Niemand will sich kümmern, hohe Barrieren
         ↓
Passung (α):         PERFEKT → α ≈ 0.98
```

**Die 6 α-Dimensionen:**

| Dimension | αᵢ | Begründung |
|-----------|-----|------------|
| **α₁ Phase-Fit** | 0.95 | Trigger-Phase: klarer Entscheidungspunkt (Vertragsabschluss) |
| **α₂ Awareness-Fit** | 0.85 | Bekannt, aber Handlungsbarriere (Status-quo Bias) |
| **α₃ Dimension-Fit** | 0.98 | Default = idealer Hebel für passive Entscheidungen |
| **α₄ Skalen-Fit** | 0.90 | Versorgerskala, automatisierbar |
| **α₅ Ressourcen-Fit** | 0.92 | Keine zusätzlichen Kosten (nur IT-Änderung) |
| **α₆ Kontext-Fit** | 0.88 | DACH: hohe Akzeptanz für "grüne" Defaults |

**Σαᵢ = 5.48** (außergewöhnlich hoch)

### 2.4 Das Gegenbeispiel: Niedriges α

> **Frage:** Was, wenn wir denselben Default bei **Ehepartner-Wahl** einsetzen würden?

| Kontext | α | Begründung |
|---------|---|------------|
| Stromtarif | ≈ 0.98 | Low-Involvement, hohe Trägheit |
| Ehepartner | ≈ 0.00 | High-Involvement, niemand akzeptiert Default |

→ **Das Modell hätte 0% Effekt vorhergesagt.**

---

## 3. Was α NICHT sagt

### 3.1 α sagt nicht, dass der Default "gut" ist

| Dimension | α-Aussage | Nicht α-Aussage |
|-----------|-----------|-----------------|
| Passung | ✅ "Der Default passt zum Kontext" | ❌ "Der Default ist normativ richtig" |
| Wirkung | ✅ "Der Default wird wahrscheinlich wirken" | ❌ "Die Wirkung ist welfare-verbessernd" |
| Design | ✅ "Der Default ist technisch machbar" | ❌ "Der Default ist ethisch zulässig" |

### 3.2 Die normative Frage bleibt offen

```
α = 0.98 für Green Energy Default

Das sagt:
→ "Dieser Nudge wird funktionieren"

Das sagt NICHT:
→ "Dieser Nudge sollte implementiert werden"
```

Die normative Bewertung erfolgt NACH der α-Analyse:
- Ist der Default im Interesse der Verbraucher?
- Ist er transparent?
- Ist er reversibel?

---

## 4. Stage 2: Die U-Analyse (Das ökonomische Modell)

> *Hier zeigen wir, dass wir die Präferenzen (U) nicht angefasst haben.*

### 4.1 Die neoklassische Kritik

**Ein Standardökonom würde sagen:**

> *"Wenn Leute von 1% auf 69% springen, habt ihr ihre Präferenzen manipuliert! Das ist Paternalismus!"*

### 4.2 Unsere Antwort

❌ **Nein.** Die Utility-Funktion U war die ganze Zeit konstant:

- Die meisten Menschen haben eine **leichte Präferenz für Grün** (θ_green > 0)
- Aber sie haben auch **Transaktionskosten** (c > 0)

### 4.3 Das formale Modell

**Utility-Funktion:**

```
U(x) = v(x) - c(x)

wobei:
  v(green) > v(grey)     für die meisten (latente Präferenz)
  c(switch) > 0          Transaktionskosten (Wechselaufwand)
```

**Entscheidungsregel:**

```
Wähle green wenn:  v(green) - c(switch) > v(grey) - c(stay)
```

### 4.4 Die zwei Szenarien

| Szenario | Standard | Entscheidung | Outcome |
|----------|----------|--------------|---------|
| **Opt-in** | Grau | v(green) - c(switch) vs v(grey) | 1% wählen Grün |
| **Opt-out** | Grün | v(green) vs v(grey) - c(switch) | 69% bleiben Grün |

**Interpretation:**

```
Szenario A (Opt-in):
  U(green) - Kosten(Wechsel) < U(grey)
  → Niemand wechselt, OBWOHL sie Grün mögen

Szenario B (Opt-out):
  U(green) > U(grey) - Kosten(Wechsel)
  → Wechselkosten fallen weg
  → Die WAHRE Präferenz wird enthüllt
```

### 4.5 Was sich verändert hat

```
┌─────────────────────────────────────────────────────────────┐
│  WAS DER DEFAULT VERÄNDERT                                  │
├─────────────────────────────────────────────────────────────┤
│  ✅ Verändert:                                              │
│     • Aufmerksamkeit (Salience)                             │
│     • Handlungskosten (Effort)                              │
│     • Implizite Empfehlung (Social Proof)                   │
│                                                             │
│  ❌ NICHT verändert:                                        │
│     • Präferenzen (θ_green)                                 │
│     • Werte (v(green), v(grey))                             │
│     • Utility-Funktion U                                    │
└─────────────────────────────────────────────────────────────┘
```

**Fazit:**
> Wir haben nicht U geändert (Leute umerzogen), sondern durch das hohe α die Barriere entfernt, die U blockiert hat.

---

## 5. Der Kalibrations-Check

### 5.1 Was das Modell vorhergesagt hat

```
1. LLM-Schätzung:
   → Kontext "Stromvertrag" erkannt
   → High-α-Szenario identifiziert
   → Schätzung: ~74 pp

2. Kalibration:
   → pp_true = -0.48 + 1.007 × pp_llm
   → pp_true = -0.48 + 1.007 × 74 ≈ 74 pp

3. Realität:
   → 69.1 pp
```

### 5.2 Interpretation

Das Modell hat korrekt erkannt:
- ✅ **High-α-Szenario** (Default + Low-Involvement)
- ✅ **Extrem hohe Wirkung** (im Gegensatz zu ~4pp bei klinischen Reminders)
- ✅ **Präzise Vorhersage** (Fehler < 5pp)

**Vergleich zu anderen Ankern:**

| Intervention | Kontext | α | Effekt |
|--------------|---------|---|--------|
| Green Energy Default (A10) | Low-Involvement | 0.98 | 69 pp |
| Clinical Reminders (A8) | High-Complexity | 0.40 | 4 pp |
| Tax Compliance Letters (A12) | Social Norm | 0.65 | 16 pp |

→ **α erklärt die Varianz in den Effektstärken.**

---

## 6. Der R-Score für diesen Fall

### 6.1 Inputs

```python
alpha_specs = [
    {"type": "pp", "llm_hat": 70, "eu_llm": 8, "name": "α_Phase"},
    {"type": "d",  "llm_hat": 0.75, "eu_llm": 0.10, "name": "α_Awareness"},
    {"type": "pp", "llm_hat": 72, "eu_llm": 6, "name": "α_Dimension"},
    {"type": "d",  "llm_hat": 0.72, "eu_llm": 0.09, "name": "α_Scale"},
    {"type": "d",  "llm_hat": 0.78, "eu_llm": 0.08, "name": "α_Resource"},
    {"type": "d",  "llm_hat": 0.70, "eu_llm": 0.11, "name": "α_Context"},
]

gamma_llm = 0.15  # Moderate positive complementarity
gamma_eu = 0.08

norm_a = 2.3  # Strong design
norm_k = 2.5  # Supportive context
```

### 6.2 Erwartetes Ergebnis

```
E[R] ≈ 5.5 - 6.0
P(R > 5.0) ≈ 70-85%

→ Entscheidung: GO
```

---

## 7. Was dieser Fall demonstriert

### 7.1 Die Trennung funktioniert

| Komponente | Rolle | Status |
|------------|-------|--------|
| **α** | Sagt "dieser Nudge passt" | ✅ Bestätigt |
| **U** | Bleibt unverändert | ✅ Respektiert |
| **Outcome** | 69pp Effekt | ✅ Erklärt durch Passung, nicht Präferenz |

### 7.2 Die Falsifizierbarkeit funktioniert

**Hypothetisches Gegenbeispiel:**

Wenn wir α = 0.98 schätzen und der RCT nur 10pp zeigt:
→ α war falsch kalibriert
→ Revision erforderlich
→ Modell ist falsifizierbar

### 7.3 Die Disziplinierung funktioniert

Wir können nicht sagen:
- ❌ "Der Nudge wirkt, weil die Leute grüne Energie mögen" (das wäre U)
- ❌ "Der Nudge wirkt, weil wir es so wollten" (das wäre ad hoc)

Wir müssen sagen:
- ✅ "Der Nudge wirkt, weil er zum Kontext passt (α)"
- ✅ "Die Passung ist empirisch kalibriert"
- ✅ "Die Präferenzen (U) sind unverändert"

---

## 8. Zusammenfassung für Stakeholder

### Die Kernaussage

> *"Sehen Sie A10 (Green Energy)?*
>
> *Wir behaupten nicht, dass wir Menschen manipulieren.*
>
> 1. *Unser **α-Parameter** erkennt, dass Defaults bei Stromverträgen technisch extrem gut funktionieren (Passung).*
>
> 2. *Unser **Utility-Modell** zeigt, dass Menschen Ökostrom eigentlich wollen, aber zu träge sind.*
>
> *Das Ergebnis (69% statt 1%) ist keine Magie, sondern das Resultat aus **hoher Passung (α)** und **vorhandener latenter Präferenz (U)**.*
>
> *Hätten wir denselben Nudge bei der Partnerwahl eingesetzt (niedriges α), hätte unser Modell 0% Effekt vorhergesagt."*

### Die Zusammenfassung

```
┌─────────────────────────────────────────────────────────────┐
│  GREEN ENERGY DEFAULT: PROOF OF CONCEPT                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STAGE 1 (α-Filter):                                        │
│    Ψ = Low-Involvement + hohe Trägheit                      │
│    a = Default (nutzt Inertia)                              │
│    α = Fit(a, Ψ) ≈ 0.98 (perfekt)                           │
│                                                             │
│  STAGE 2 (U-Maximierung):                                   │
│    U(green) > U(grey) für die meisten                       │
│    c(switch) blockierte Präferenzoffenbarung                │
│    Default entfernt Barriere, U bleibt konstant             │
│                                                             │
│  ERGEBNIS:                                                  │
│    Effekt = 69pp (vorhergesagt durch hohes α)               │
│    Präferenzen = unverändert                                │
│    Modell = falsifizierbar                                  │
│                                                             │
│  → α macht Modelle anwendbar, ohne sie umzuschreiben        │
└─────────────────────────────────────────────────────────────┘
```

---

## Referenzen

- **Quelle:** Ebeling & Lotz (2015). Domestic uptake of green energy. Energy Policy.
- **Anchor:** `T12_10_green_energy_default_germany`
- **Theorie:** `docs/methods/alpha-vs-utility-formal.md`
- **α-Definition:** `docs/methods/alpha-definition.md`
- **Pipeline:** `scripts/llmmc_to_rscore.py`

---

*Version 2.0 | Januar 2025 | EBF Framework*
