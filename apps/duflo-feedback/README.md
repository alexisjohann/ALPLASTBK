# Duflo Feedback Web-App

> **Was wuerde Esther Duflo ueber dein Feld-Experiment sagen?**
>
> Web-App fuer Studierende im Kurs «Feldexperimente» (Nils Handler).
> Studierende geben ihr Experimental Design ein und erhalten Feedback
> in zwei Modi.

## Architektur

```
┌──────────────────────────────────────────────────────────┐
│  Browser (Frontend)                                       │
│  ┌────────────────────┐   ┌────────────────────────────┐ │
│  │ Parametrisch-Modus │   │ LLM-Modus                  │ │
│  │ (Dropdowns, Scores)│   │ (Freitext → Duflo-Persona) │ │
│  └────────┬───────────┘   └────────────┬───────────────┘ │
└───────────┼────────────────────────────┼─────────────────┘
            │ POST /api/feedback/        │
            │ parametric                 │ POST /api/feedback/llm
            ▼                            ▼
┌──────────────────────────────────────────────────────────┐
│  Flask Backend (app.py)                                   │
│  ┌──────────────────┐   ┌──────────────────────────────┐ │
│  │ parametric_model  │   │ llm_engine                   │ │
│  │ 5 Kriterien       │   │ Duflo System-Prompt          │ │
│  │ 22 Sub-Dimensionen│   │ OpenAI / Anthropic / Fallback│ │
│  │ Gewichtetes Score │   │                              │ │
│  └──────────────────┘   └──────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

## Zwei Feedback-Modi

### 1. Parametrisches Modell (kein API-Key noetig)

Studierende waehlen fuer 22 Sub-Dimensionen ueber 5 Duflo-Kriterien
aus Dropdown-Menues. Das Modell berechnet sofort:

- **Score pro Kriterium** (0-5) mit gewichteten Sub-Dimensionen
- **Gesamtscore** mit Prozent und Note
- **Duflo-Stil Feedback** pro Kriterium

| Kriterium | Gewicht | Sub-Dimensionen |
|-----------|---------|-----------------|
| 1. Randomisierung & Identifikation | 25% | Design, Zuweisung, Selektionsbias, Confounders |
| 2. Messbarkeit der Outcomes | 20% | Outcome, Operationalisierung, Datenquelle, Timing, Power |
| 3. Kausalitaet & Theory of Change | 20% | ToC, Mechanismus, Verhaltenskanal, Alternativerk. |
| 4. Skalierbarkeit & ext. Validitaet | 15% | Population, Kontext, Zeit, Skalierung, GE-Effekte |
| 5. Ethik & Forschungsverantwortung | 20% | Consent, Schaden, Equipoise, Datenschutz, Nachsorge |

### 2. LLM-Modus (API-Key erforderlich fuer volles Feedback)

Studierende beschreiben ihr Experiment in Freitext-Feldern.
Ein LLM mit Esther-Duflo-Persona gibt qualitatives Feedback.

**Unterstuetzte Backends:**
- OpenAI (GPT-4o) — `OPENAI_API_KEY`
- Anthropic (Claude) — `ANTHROPIC_API_KEY`
- Fallback (Template) — kein Key noetig, strukturiertes Template-Feedback

## Schnellstart

```bash
# 1. Abhaengigkeiten installieren
pip install flask

# 2. (Optional) API-Key setzen fuer LLM-Modus
export OPENAI_API_KEY="sk-..."
# oder
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. App starten
cd apps/duflo-feedback
python app.py

# 4. Browser oeffnen
# → http://localhost:5000
```

## API-Endpunkte

| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| GET | `/` | Frontend (HTML) |
| POST | `/api/feedback/parametric` | Parametrisches Scoring |
| POST | `/api/feedback/llm` | LLM-Feedback |
| GET | `/api/criteria` | Kriterien-Definitionen (JSON) |

### Beispiel: Parametrisches Scoring

```bash
curl -X POST http://localhost:5000/api/feedback/parametric \
  -H "Content-Type: application/json" \
  -d '{
    "responses": {
      "randomization": {
        "design_type": "rct",
        "assignment_mechanism": "stratified_random",
        "selection_bias_control": "balance_test_planned",
        "confounders_addressed": "systematic_list"
      },
      "measurability": {
        "primary_outcome": "quantitative_specific",
        "operationalization": "validated_instrument",
        "data_source": "admin_data",
        "measurement_timing": "baseline_endline_followup",
        "power_analysis": "formal_calculation"
      }
    }
  }'
```

### Beispiel: LLM-Feedback

```bash
curl -X POST http://localhost:5000/api/feedback/llm \
  -H "Content-Type: application/json" \
  -d '{
    "form_data": {
      "title": "Effekt von Peer-Feedback auf Recycling",
      "research_question": "Erhoeht soziales Feedback die Recycling-Quote?",
      "intervention": "Wöchentliches Feedback-Poster im Hauseingang...",
      "experimental_design": "Cluster-RCT, 50 Wohnblocks, 6 Monate..."
    },
    "backend": "auto"
  }'
```

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `app.py` | Flask-Backend mit Routes |
| `parametric_model.py` | Scoring-Engine (5 Kriterien, 22 Sub-Dimensionen) |
| `llm_engine.py` | LLM-Engine mit Duflo-Persona System-Prompt |
| `templates/index.html` | Frontend (HTML/CSS/JS, Single Page) |

## Kurs-Kontext

- **Kurs:** Feldexperimente
- **Dozent:** Nils Handler
- **Zielgruppe:** Masterstudierende
- **Zweck:** Studierende erhalten strukturiertes Feedback auf ihre Experimental Designs
