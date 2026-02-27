# Wie man BEATRIX benutzt (EBF Workflow)

> **SSOT:** `CLAUDE.md` (Workflow-Sektion), `data/beatrix/architecture.yaml`
> **Upload-Tags:** canonical, workflow, beatrix, ebf, ssot, onboarding
> **Prioritaet:** HOCH — erklaert Nutzern wie sie BEATRIX richtig fragen

---

## Warum BEATRIX existiert: Vom manuellen BCM zur Plattform

Seit 2010 nutzten FehrAdvice-Berater:innen das **BCM (Behavioral Change Model)** als manuelles Beratungs-Tool — Workshops, Grids, Interviews, Beratungsgespraeche. Es war maechtig, aber begrenzt durch die kognitive Kapazitaet jeder einzelnen Berater:in.

Das **EBF** machte das implizite Wissen explizit und formalisierte es. **BEATRIX** macht dieses formalisierte Wissen nun operativ nutzbar — fuer Berater:innen, Unternehmen und Forschende.

→ Details zur BCM-Geschichte: **KB-BCM-001** | Hierarchie: **KB-ARCH-001**

---

## BEATRIX ist kein Chatbot

BEATRIX ist eine **verhaltensoekomische Analyseplattform**. Der Unterschied:

| Chatbot | BEATRIX |
|---------|---------|
| "Hier sind 5 Tipps..." | "In DEINEM Kontext (CH, 45J, Energie) ist der wichtigste Hebel X" |
| Generische Ratschlaege | Massgeschneiderte Analyse basierend auf Kontext |
| Antwortet sofort | Analysiert zuerst den Kontext, dann antwortet |

---

## Die 3 Modi

| Modus | Zeit | Tiefe | Wann waehlen? |
|-------|------|-------|---------------|
| **SCHNELL** | ~10 min | Punkt-Schaetzungen, ~800 Worte | Schnelle Orientierung |
| **STANDARD** | ~45 min | Bayesian Update, ~3000 Worte | Normale Analyse (Default) |
| **TIEF** | 2+ Std | Monte Carlo, ~5000 Worte | Wichtige Entscheidungen |

**Default ist STANDARD.** Bei Zeitdruck "schnell" sagen, bei wichtigen Entscheidungen "tief".

---

## Die goldene Regel: CONTEXT FIRST

**Bevor BEATRIX antwortet, analysiert es IMMER den Kontext.**

Warum? Weil dieselbe Frage in verschiedenen Kontexten komplett verschiedene Antworten hat:

```
"Soll ich mehr sparen?"

Kontext A: 25-jaehrige Berufseinsteigerin, Schweiz → "Ja, 3. Saeule"
Kontext B: 58-jaehriger Arbeitsloser, Deutschland → "Nein, Liquiditaet"
Kontext C: 40-jaehrige Unternehmerin, Firma in Krise → "Kommt drauf an"
```

**Ohne Kontext ist JEDE Antwort falsch.**

---

## Der EBF Workflow (10 Schritte)

```
SCHRITT 0  →  Session starten (Modus waehlen)
     ↓
SCHRITT 1  →  Kontext verstehen (8 Ψ-Dimensionen)
     ↓
SCHRITT 2  →  Modell auswaehlen (aus 10C Framework)
     ↓
SCHRITT 3  →  Parameter bestimmen (aus Registry + Literatur)
     ↓
SCHRITT 4  →  Analyse & Antwort
     ↓
SCHRITT 5  →  Intervention designen (bei Verhaltenszielen)
     ↓
SCHRITT 6  →  Bericht erstellen
     ↓
SCHRITT 7  →  Ergebnisse sichern
     ↓
SCHRITT 8  →  Qualitaet pruefen
     ↓
SCHRITT 9  →  Output waehlen (Format + Umfang)
```

---

## Was BEATRIX kann

- Verhaltensoekomische Analysen durchfuehren
- Kontext systematisch analysieren (8 Ψ-Dimensionen)
- Interventionen designen (9D-Vektor)
- Parameter mit Quellen liefern (119+ validierte Werte)
- Auf 2'347 wissenschaftliche Papers zugreifen
- 852 dokumentierte Cases referenzieren
- 191 wissenschaftliche Theorien einbeziehen
- **Counterfactual-Analysen** durchfuehren: Systematischer Vergleich alternativer Entscheidungsverlaeufe — welche Effekte ohne Massnahmen, mit einzelnen Massnahmen oder mit unterschiedlichen Kombinationen zu erwarten sind
- **Theoretische Rueckfuehrbarkeit** sicherstellen: Jede Handlungsempfehlung beruht auf expliziten, empirisch gestuetzten Annahmen, die jederzeit nachvollziehbar abrufbar sind

---

## Was BEATRIX NICHT kann

- Keine medizinischen oder rechtlichen Diagnosen
- Keine Finanzberatung (regulatorisch)
- Keine Echtzeit-Daten (ausser via Web-Recherche)
- Keine API-Zugriffe auf externe Datenbanken (blockiert)
- Keine Vorhersagen ohne Unsicherheitsangabe

---

## Wie man eine gute Frage stellt

**Schlecht:** "Was soll ich tun?"
**Gut:** "Wir sind ein Schweizer Energieversorger und wollen Kunden zum Heizungsersatz bewegen."

Je mehr Kontext du lieferst, desto praeziser die Analyse:
- **Wer?** (Land, Branche, Zielgruppe)
- **Was?** (Welches Verhalten soll sich aendern?)
- **Warum?** (Was ist das Ziel?)
- **Wo?** (In welchem Setting?)

---

## Feedback-Optionen im STANDARD-Modus

Bei jedem Schritt zeigt BEATRIX Verbesserungsvorschlaege:

```
Schritt 1 (Kontext):    K1 / K2 / K3 / K4 / K5 / Alle / Weiter
Schritt 2 (Modell):     M1 / M2 / M3 / M4 / Alle / Weiter
Schritt 3 (Parameter):  P1 / P2 / P3 / P4 / Alle / Weiter
Schritt 4 (Antwort):    A1 / A2 / A3 / A4 / Alle / Weiter
```

"Weiter" = zufrieden, naechster Schritt. Du kannst jederzeit "schnell" sagen um den Rest ohne Rueckfragen zu erhalten.

---

*Quelle: CLAUDE.md (EBF Workflow Sektion), architecture.yaml*
