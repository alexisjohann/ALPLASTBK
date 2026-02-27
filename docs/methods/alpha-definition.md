# α-Parameter: Definition und Abgrenzung

> **Kernaussage:** α ist ein kalibrierter Passungsparameter, kein Effekt.

---

## Was ist α?

### Formal

```
αᵢ ∈ [0,1]

αᵢ = Fit(Interventionᵢ, Kontextᵢ)
```

### Intuitiv

α beantwortet die Frage:

> „Wenn ich diese Maßnahme hier und jetzt einsetze – passt sie überhaupt?"

---

## Was α NICHT ist

| ❌ Missverständnis | Warum falsch |
|--------------------|--------------|
| Effektstärke | Effekte kommen aus RCTs (d, pp). α ist kontextuell. |
| Nutzen/Welfare | Nutzen ist normativ. α ist deskriptiv. |
| Präferenz | Präferenzen sind subjektiv. α ist evidenzbasiert. |
| Wahrscheinlichkeit | α ist kein Risiko. |
| Regressionskoeffizient | Keine Schätzgleichung, kein SEM. |

---

## Die 6 α-Komponenten (Standard)

| Komponente | Bedeutung | Frage |
|------------|-----------|-------|
| α₁ | **Phase-Fit** | Awareness / Action / Maintenance – wo steht die Zielgruppe? |
| α₂ | **Awareness-Fit** | Kognitiv, emotional, habitual – welche Barriere? |
| α₃ | **Dimension-Fit** | Information, Default, Incentive, Feedback – welcher Hebel? |
| α₄ | **Skalen-Fit** | Individuell, organisatorisch, systemisch – welche Ebene? |
| α₅ | **Ressourcen-Fit** | Budget, Zeit, Implementierbarkeit – machbar? |
| α₆ | **Kontext-Fit** | Land, Kultur, Institutionen – passt es hier? |

---

## Wie entsteht αᵢ?

### Pipeline

```
1. Evidenz sammeln
   → Meta-Analysen, RCTs, Systematic Reviews

2. LLMMC-Elicitation (Tier 3)
   → Strukturierte Abfragen, 4 Perspektiven, Temperaturvariation

3. Kalibration
   → d/SMD: θ = 0.03 + 0.79 × θ_llm
   → pp:    pp = -0.48 + 1.007 × pp_llm

4. Mapping auf 0-1
   → Piecewise linear (v1)

5. Ergebnis
   → αᵢ = α̂ᵢ ± EUᵢ
```

---

## Verhältnis zu γ (Komplementarität)

| Parameter | Misst | Frage |
|-----------|-------|-------|
| α | Einzelpassung | Passt diese Maßnahme? |
| γ | Zusammenspiel | Verstärken sich die Maßnahmen? |

### R-Score Formel

```
R = Σαᵢ + γ·‖a‖·‖K‖
```

- Ohne gute α: γ ist bedeutungslos
- Ohne γ: α bleibt additiv und blind für Synergien

---

## Beispiel: Default-Nudge in Altersvorsorge

**Intervention:** Auto-Enrollment
**Kontext:** Altersvorsorge, Arbeitnehmer, DACH

| Dimension | αᵢ | Begründung |
|-----------|-----|------------|
| Phase-Fit | 0.95 | Trigger-Phase, klarer Entscheidungspunkt |
| Awareness-Fit | 0.90 | Bekannt, aber Handlungsbarriere |
| Dimension-Fit | 0.98 | Default = idealer Hebel |
| Skalen-Fit | 0.92 | Arbeitgeberebene, skalierbar |
| Ressourcen-Fit | 0.85 | Geringe Implementierungskosten |
| Kontext-Fit | 0.88 | DACH-Akzeptanz hoch |

**Σαᵢ = 5.48**

> Diese Maßnahme passt außergewöhnlich gut – bevor wir über Synergien reden.

---

## Der wichtigste Satz

> **α macht Wirkung anwendbar, nicht größer.**

Oder:

> **Effekte sagen, dass etwas wirkt.**
> **α sagt, wo und wann.**

---

## Abgrenzung zu klassischen Utility-Funktionen

| Konzept | Utility (ökonomisch) | α (EBF) |
|---------|---------------------|---------|
| Charakter | Normativ (Präferenzen) | Deskriptiv (Evidenz) |
| Quelle | Revealed/Stated Preferences | LLMMC + Kalibration |
| Aggregation | Cardinal/Ordinal | Additiv + Komplementär |
| Kontext | Oft kontextfrei | Kontextgebunden |
| Unsicherheit | Oft ignoriert | Propagiert (MC) |

### Warum nicht einfach Utility?

1. **Utility ist subjektiv** – α ist intersubjektiv (evidenzbasiert)
2. **Utility ist aggregiert** – α ist modular (6 Dimensionen)
3. **Utility ist statisch** – α ist kontextabhängig
4. **Utility ignoriert Fit** – α misst explizit Passung

---

## Technische Spezifikation

### Datentypen

```python
@dataclass
class AlphaSpec:
    type: str           # "d" oder "pp"
    llm_hat: float      # LLM-Schätzung
    eu_llm: float       # Elicitation Uncertainty
    name: str           # z.B. "α_Phase"
    dimension: int      # 1-6
```

### Berechnung

```python
from theta_mapping import build_alpha_theta

alpha_specs = [
    {"type": "d", "llm_hat": 0.70, "eu_llm": 0.12, "name": "α_Phase"},
    {"type": "d", "llm_hat": 0.55, "eu_llm": 0.10, "name": "α_Awareness"},
    # ...
]

alpha_hat, alpha_eu = build_alpha_theta(alpha_specs)
```

### Output

```
α = [0.68, 0.56, 0.62, 0.76, 0.36, 0.60]
EU = [0.11, 0.10, 0.09, 0.09, 0.15, 0.11]
Σα = 3.60 ± 0.27
```

---

## Referenzen

- **Pipeline:** `scripts/llmmc_to_rscore.py`
- **Kalibration:** `data/calibration/calibration_d_v1.json`, `calibration_pp_v1.json`
- **Mapping:** `scripts/theta_mapping.py`
- **R-Score:** `scripts/r_score.py`

---

## Abgrenzung zu klassischen Utility-Funktionen (für Ökonomen)

### Was ist eine Utility-Funktion?

```
U(x)
```

Eigenschaften:
- **normativ:** sagt, was gut ist
- **präferenzbasiert:** abgeleitet aus individuellen Ordnungen
- **entscheidungsendogen:** Akteure maximieren U
- **komparativ-statisch:** Wohlfahrtsvergleiche, Effizienz, Optima
- **theorie-intern:** Teil eines vollständigen Modells

> **Utility ist ein Zielmaß der Akteure.**

### Die zentrale Trennung

| Dimension | Utility U | Alpha α |
|-----------|-----------|---------|
| **Rolle** | Zielgröße | Passungsmaß |
| **Normativ?** | ✅ ja | ❌ nein |
| **Präferenzen?** | ✅ ja | ❌ nein |
| **Kontextabhängig?** | ❌ meist nein | ✅ explizit |
| **Akteur** | Individuum | Designer |
| **Zeitpunkt** | nach Wahl | vor Wahl |
| **Zweck** | Optimierung | Filter / Priorisierung |

### Merksatz

> **Utility bewertet Zustände.**
> **α bewertet Instrumente.**

### α liegt AUSSERHALB des Optimierungsproblems

**Klassisches Schema:**
```
max_x U(x)  s.t. x ∈ X
```

**EBF-Schema:**
```
1. Filter / Priorisierung
   Wähle a ∈ A mit hohem R(a,K)

2. Dann (optional): klassisches Modell
   max_x U(x | a)
```

> α bestimmt nicht das Optimum, sondern welche Instrumente überhaupt sinnvoll modelliert werden.

### Warum α kein Welfare-Maß ist

❌ **Häufiger Fehler:** „Höheres α = höhere Wohlfahrt"

Gegenbeispiele:
- Perfekt passender Nudge (α ≈ 1) kann normativ problematisch sein
- Schlecht passender Nudge (α ≈ 0.2) kann welfare-verbessernd sein

> **α ist wertfrei. Normative Bewertung kommt danach.**

### Verhältnis zu Behavioral Welfare Economics

α ist **kompatibel, aber orthogonal** zu:
- Bernheim & Rangel
- Beshears et al.
- „As judged by themselves"-Ansätze

Denn:
- Diese bewerten **Outcomes**
- α bewertet **Interventions-Eignung**

> α sagt nicht, ob ein Eingriff legitim ist – sondern ob er technisch funktioniert.

### Ein präzises Bild

```
Utility = Zielgröße im Modell
α = Modellwahl-Heuristik
```

Formaler:

> **α ist eine Meta-Größe über Modellen, nicht eine Größe im Modell.**

### Warum das eure Position stark macht

Ihr behauptet NICHT:
- ❌ „Wir ersetzen Nutzen"
- ❌ „Wir erklären Verhalten besser als alles andere"
- ❌ „Wir lösen Arrow–Debreu"

Sondern:

> **Wir machen Modelle anwendbar, ohne sie normativ umzuschreiben.**

Das ist defensiv, sauber, nicht angreifbar.

### Der Satz für Diskussionen mit Theoretikern

> „α ist kein Utility, sondern ein Passungsfilter für Instrumente.
> Wir verändern keine Präferenzen, wir entscheiden nur,
> welche Interventionen es überhaupt wert sind, modelliert zu werden."

---

## Referenzen

- **Pipeline:** `scripts/llmmc_to_rscore.py`
- **Kalibration:** `data/calibration/calibration_d_v1.json`, `calibration_pp_v1.json`
- **Mapping:** `scripts/theta_mapping.py`
- **R-Score:** `scripts/r_score.py`

---

*Version 1.1 | Januar 2025 | EBF Framework*
