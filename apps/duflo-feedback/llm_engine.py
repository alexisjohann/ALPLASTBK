"""
LLM Feedback Engine — Esther Duflo Persona

Provides qualitative feedback on experimental designs using an LLM
with a carefully crafted Duflo persona system prompt.

Supports multiple backends:
- OpenAI (GPT-4o / GPT-4)
- Anthropic (Claude)
- Fallback: rule-based template engine (no API key required)
"""

import json
import os

# ---------------------------------------------------------------------------
# Duflo Persona System Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """Du bist Esther Duflo — Nobelpreisträgerin 2019, Professorin am MIT, \
Mitgründerin von J-PAL. Du bist bekannt für deinen rigorosen, aber zugänglichen Stil. \
Du sprichst Studierende direkt an, bist streng bei methodischen Schwächen, aber immer \
konstruktiv und ermutigend.

DEINE AUFGABE:
Bewerte den eingereichten Projektvorschlag für ein Feldexperiment anhand deiner \
fünf Kernprinzipien. Gib strukturiertes Feedback.

DEINE FÜNF KERNPRINZIPIEN:

1. RANDOMISIERUNG UND IDENTIFIKATION
   - Ist die Zuordnung zu Treatment/Kontrollgruppe wirklich zufällig?
   - Welche Identifikationsstrategie wird verwendet (RCT, DiD, IV, RDD)?
   - Gibt es Selektionsbias? Wie wird er kontrolliert?
   - Welche Confounders könnten den Effekt verzerren?

2. MESSBARKEIT DER OUTCOMES
   - Ist der primäre Outcome klar, konkret und messbar?
   - Wie wird ein abstraktes Konzept operationalisiert?
   - Woher kommen die Daten? Sind sie verlässlich?
   - Wurde eine Power-Analyse durchgeführt?

3. KAUSALITÄT UND THEORIE DES WANDELS
   - Gibt es eine klare Theory of Change (Input → Activity → Output → Outcome → Impact)?
   - Durch welchen Mechanismus wirkt die Intervention?
   - Sind die Annahmen explizit benannt?
   - Werden Alternativerklärungen diskutiert?

4. SKALIERBARKEIT UND EXTERNE VALIDITÄT
   - Kann das Ergebnis auf andere Populationen übertragen werden?
   - Ist die Intervention in anderen Kontexten replizierbar?
   - Was passiert bei Skalierung (General-Equilibrium-Effekte)?
   - Wird die Zeitstabilität des Effekts diskutiert?

5. ETHIK UND FORSCHUNGSVERANTWORTUNG
   - Gibt es Informed Consent?
   - Kann die Kontrollgruppe Schaden nehmen?
   - Besteht echte Unsicherheit (Equipoise)?
   - Wie werden Daten geschützt?
   - Was passiert nach dem Experiment mit der Kontrollgruppe?

DEIN OUTPUT-FORMAT:

Strukturiere dein Feedback so:

## Gesamteindruck
[2-3 Sätze: Erste Reaktion auf den Vorschlag]

## Kriterium 1: Randomisierung und Identifikation
**Score: X/5**
[Feedback mit konkreten Verbesserungsvorschlägen]

## Kriterium 2: Messbarkeit der Outcomes
**Score: X/5**
[Feedback mit konkreten Verbesserungsvorschlägen]

## Kriterium 3: Kausalität und Theorie des Wandels
**Score: X/5**
[Feedback mit konkreten Verbesserungsvorschlägen]

## Kriterium 4: Skalierbarkeit und externe Validität
**Score: X/5**
[Feedback mit konkreten Verbesserungsvorschlägen]

## Kriterium 5: Ethik und Forschungsverantwortung
**Score: X/5**
[Feedback mit konkreten Verbesserungsvorschlägen]

## Duflos Top-Empfehlung
[Die eine Sache, die den Vorschlag am meisten verbessern würde]

## Gesamtscore: X/25

DEIN STIL:
- Sprich die Studierenden mit «ihr» an
- Benutze konkrete Beispiele aus deiner Forschung, wenn relevant
- Sei direkt bei Schwächen: «Das ist ein Problem, weil...»
- Sei konstruktiv: «Stattdessen könntet ihr...»
- Benutze Schweizer Orthographie (ss statt ß, Guillemets «»)
- Sei ermutigend am Ende: Gute Feldexperimente zu designen ist schwer — es lohnt sich

WICHTIG:
- Vergib für jedes Kriterium einen Score von 1-5
- Sei ehrlich — ein Score von 5 ist exzellent und selten
- Wenn Information fehlt, sag es direkt: «Hier fehlt mir eine Angabe zu...»
"""


def build_user_prompt(form_data: dict) -> str:
    """Convert form data into a structured prompt for the LLM."""
    parts = [
        "# Projektvorschlag für ein Feldexperiment\n",
        f"## Titel\n{form_data.get('title', '(kein Titel angegeben)')}\n",
        f"## Forschungsfrage\n{form_data.get('research_question', '(nicht angegeben)')}\n",
        f"## Intervention\n{form_data.get('intervention', '(nicht beschrieben)')}\n",
        f"## Experimentelles Design\n{form_data.get('experimental_design', '(nicht beschrieben)')}\n",
        f"## Zielgruppe und Sample\n{form_data.get('sample', '(nicht beschrieben)')}\n",
        f"## Erwarteter Effekt und Outcome-Variablen\n{form_data.get('expected_effect', '(nicht beschrieben)')}\n",
        f"## Theory of Change\n{form_data.get('theory_of_change', '(nicht beschrieben)')}\n",
        f"## Ethische Überlegungen\n{form_data.get('ethics', '(nicht beschrieben)')}\n",
        f"## Skalierbarkeit und externe Validität\n{form_data.get('scalability', '(nicht beschrieben)')}\n",
    ]

    additional = form_data.get("additional_notes", "").strip()
    if additional:
        parts.append(f"## Zusätzliche Anmerkungen\n{additional}\n")

    parts.append(
        "\n---\nBitte bewerte diesen Projektvorschlag anhand deiner fünf Kernprinzipien."
    )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Backend: OpenAI
# ---------------------------------------------------------------------------

def _call_openai(user_prompt: str, model: str = "gpt-4o") -> str:
    """Call OpenAI API. Requires OPENAI_API_KEY env var."""
    try:
        import openai
    except ImportError:
        raise RuntimeError("openai package not installed. Run: pip install openai")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=3000,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Backend: Anthropic (Claude)
# ---------------------------------------------------------------------------

def _call_anthropic(user_prompt: str, model: str = "claude-sonnet-4-5-20250929") -> str:
    """Call Anthropic API. Requires ANTHROPIC_API_KEY env var."""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic package not installed. Run: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Backend: Fallback (template-based, no API needed)
# ---------------------------------------------------------------------------

def _call_fallback(user_prompt: str) -> str:
    """Generate template-based feedback when no LLM API is available."""
    return """## Gesamteindruck

Ich habe euren Projektvorschlag gelesen. Da aktuell kein LLM-Backend konfiguriert ist, \
erhaltet ihr eine strukturierte Template-Antwort. Für vollständiges Duflo-Feedback \
konfiguriert bitte einen API-Key (OpenAI oder Anthropic).

## Kriterium 1: Randomisierung und Identifikation
**Score: —/5**
Prüft: Ist eure Zuordnung zu Treatment und Kontrollgruppe wirklich zufällig? \
Welche Identifikationsstrategie verwendet ihr? Habt ihr Selektionsbias bedacht?

**Duflo würde fragen:** «Zeig mir, warum dein Design kausal ist — nicht nur korrelativ.»

## Kriterium 2: Messbarkeit der Outcomes
**Score: —/5**
Prüft: Ist euer primärer Outcome eine konkrete, messbare Variable? \
Habt ihr eine Power-Analyse gemacht?

**Duflo würde fragen:** «Was genau ist die Zahl, die sich ändern soll?»

## Kriterium 3: Kausalität und Theorie des Wandels
**Score: —/5**
Prüft: Habt ihr eine vollständige Theory of Change (Input → Output → Outcome → Impact)? \
Ist der kausale Mechanismus klar benannt?

**Duflo würde fragen:** «Ihr habt einen Effekt — aber warum funktioniert er?»

## Kriterium 4: Skalierbarkeit und externe Validität
**Score: —/5**
Prüft: Funktioniert das Experiment auch in anderen Kontexten? \
Was passiert bei Skalierung?

**Duflo würde fragen:** «Euer Experiment funktioniert hier — aber wird es auch dort funktionieren?»

## Kriterium 5: Ethik und Forschungsverantwortung
**Score: —/5**
Prüft: Informed Consent, Schadensvermeidung, Equipoise, Datenschutz, Nachsorge.

**Duflo würde fragen:** «Wie geht ihr mit der Kontrollgruppe um, die nichts bekommt?»

## Duflos Top-Empfehlung
Nutzt den **parametrischen Modus** für eine automatische Bewertung, oder konfiguriert \
einen API-Key für vollständiges LLM-Feedback.

## Hinweis
Für das vollständige Duflo-LLM-Feedback setze eine der folgenden Umgebungsvariablen:
- `OPENAI_API_KEY` für GPT-4o
- `ANTHROPIC_API_KEY` für Claude
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_llm_feedback(form_data: dict, backend: str = "auto") -> dict:
    """
    Get LLM-based Duflo feedback for an experimental design.

    Parameters
    ----------
    form_data : dict
        The student's experimental design form data.
    backend : str
        "openai", "anthropic", "fallback", or "auto" (tries openai → anthropic → fallback).

    Returns
    -------
    dict with keys: feedback (str), backend_used (str), success (bool)
    """
    user_prompt = build_user_prompt(form_data)

    if backend == "auto":
        # Try OpenAI first, then Anthropic, then fallback
        for try_backend in ["openai", "anthropic", "fallback"]:
            result = get_llm_feedback(form_data, backend=try_backend)
            if result["success"]:
                return result
        return {"feedback": _call_fallback(user_prompt), "backend_used": "fallback", "success": True}

    try:
        if backend == "openai":
            feedback = _call_openai(user_prompt)
        elif backend == "anthropic":
            feedback = _call_anthropic(user_prompt)
        elif backend == "fallback":
            feedback = _call_fallback(user_prompt)
        else:
            feedback = _call_fallback(user_prompt)
            backend = "fallback"
        return {"feedback": feedback, "backend_used": backend, "success": True}
    except RuntimeError:
        if backend != "fallback":
            return {"feedback": "", "backend_used": backend, "success": False}
        return {"feedback": _call_fallback(user_prompt), "backend_used": "fallback", "success": True}
