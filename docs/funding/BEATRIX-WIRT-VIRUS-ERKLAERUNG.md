# BEATRIX: Wirt, Virus und das Immunsystem — Eine Erklärung

**Version:** 1.0 | **Datum:** 2026-02-17 | **Autor:** EBF Framework
**Kontext:** Gerhard Fehrs Wirt-Virus-Metapher für die Three-Layer Architecture
**Zielgruppe:** Stakeholder, Projektpartner, neue Teammitglieder

---

## Die Begriffe zuerst

### BEATRIX

**BEATRIX** (Behavioral Economics AI Technology for Research and Implementation eXcellence) ist ein Projekt von FehrAdvice Partners und der Universität Zürich. Es soll 50 Jahre verhaltensökonomische Forschung — Tausende von Studien, Parametern und Modellen — für die Managementpraxis nutzbar machen. Ein evidenzbasiertes Entscheidungssystem, das analysiert, warum Menschen in bestimmten Kontexten bestimmte Entscheidungen treffen.

### LLM (Large Language Model)

Ein **LLM** ist die KI-Technologie hinter Chatbots wie ChatGPT oder Claude. Ein LLM hat Milliarden von Texten gelesen und kann Sprache verstehen und erzeugen. Aber: Es *rechnet* nicht wirklich — es *erinnert sich* an Muster. Und Erinnerungen können falsch sein.

### Claude Code

**Claude Code** ist das konkrete Werkzeug — Anthropics KI-Assistent Claude, der direkt im Code-Repository arbeitet: Dateien lesen, schreiben, Scripts ausführen, Analysen durchführen. Claude Code ist das LLM, das BEATRIX antreibt.

### Layer (Schicht)

**Layer** bedeutet «Schicht». So wie ein Gebäude aus Fundament, Tragwerk und Fassade besteht, besteht BEATRIX aus drei Schichten, die jeweils eine klar getrennte Aufgabe haben:

| Layer | Technologie | Analogie | Aufgabe | Virus-Anfälligkeit |
|-------|-------------|----------|---------|---------------------|
| **Layer 1** | Python-Scripts | Taschenrechner | Berechnet Formeln deterministisch. 2 + 2 = 4, immer. | 0.0 — **immun** |
| **Layer 2** | YAML-Dateien | Laborhandbuch | Enthält validierte Parameterwerte mit Quellenangabe. Nicht ausgedacht, sondern aus Studien. | 0.3 — **niedrig** |
| **Layer 3** | LLM (Claude) | Dolmetscher | Versteht die Frage des Users und erklärt das Ergebnis in natürlicher Sprache. Rechnet nicht selbst, erfindet keine Zahlen. | 0.8 — **hoch** |

### Virus

Ein **Virus** ist falsche Information, die korrekt *aussieht*. Zum Beispiel: Das LLM «erinnert sich» aus seinen Trainingsdaten, dass Loss Aversion λ = 2.25 beträgt. Die Zahl klingt plausibel, stimmt aber im konkreten Kontext nicht — dort wäre der korrekte Wert 4.58. Diese falsche Zahl ist der Virus: Sie widerspricht der Wahrheit, sieht aber richtig aus, und kann sich verbreiten, wenn sie in eine Datei geschrieben wird.

Formal muss ein Virus vier Bedingungen gleichzeitig erfüllen (CPRE):

1. **C** (Contradiction) — Widerspricht einer validierten Quelle
2. **P** (Plausibility) — Sieht bei oberflächlicher Prüfung korrekt aus
3. **R** (Replication) — Kann sich im System verbreiten
4. **E** (Evasion) — Wird von bestehenden Checks nicht erkannt

### Wirt (Host)

Der **Wirt** ist die Entität, in der der Virus lebt. In BEATRIX ist der Hauptwirt das LLM selbst (Claude Code). Es erzeugt den Virus (durch Halluzination) und verbreitet ihn (indem es falsche Werte in Dateien schreibt oder dem User präsentiert).

Es gibt vier Wirt-Typen:

| Wirt | Was | Anfälligkeit | Biologische Analogie |
|------|-----|-------------|----------------------|
| **H-GEN** (Generativ) | Das LLM selbst | 1.0 (maximal) | Zelle mit aktiver Virus-Replikation |
| **H-STORE** (Speicher) | Dateien im Repository | 0.3–1.0 | Reservoir-Wirt (trägt Virus ohne Symptome) |
| **H-DIST** (Distribution) | System-Prompts, Templates | 0.1 (selten, aber maximaler Schaden) | Super-Spreader |
| **H-COG** (Kognitiv) | Der menschliche User | variabel | Symptomatischer Wirt |

---

## Der Infektionszyklus

Wie ein biologischer Virus zirkuliert auch ein Informationsvirus zwischen den Wirten:

```
LLM halluziniert eine falsche Zahl (H-GEN)
    ↓
Schreibt sie in eine YAML-Datei (H-STORE)
    ↓
Die Datei fliesst in ein Template (H-DIST)
    ↓
Nächste Session liest das infizierte Template (H-GEN)
    ↓
User akzeptiert die falsche Zahl (H-COG)
    ↓
User speichert sie in einem neuen Dokument (H-STORE)
    ↓
... Zyklus wiederholt sich
```

---

## Das Paradoxon: «Der Wirt entscheidet, ob der Virus leben darf»

Das ist der Kernsatz von Gerhard Fehrs Erklärung.

**Das Problem:** BEATRIX hat ein Immunsystem — Layer 1, die formale Berechnung. Dieser Taschenrechner ist komplett immun gegen Halluzinationen. Aber: In der ursprünglichen Architektur entschied das LLM (Layer 3) selbst, ob es den Taschenrechner benutzt — oder einfach aus dem Gedächtnis antwortet.

Das ist, als hätte eine infizierte Zelle ein **Vetorecht** gegen die weissen Blutkörperchen.

```
BIOLOGIE (funktioniert):          BEATRIX vorher (Problem):
──────────────────────────         ─────────────────────────────
Immunsystem arbeitet AUTONOM       Layer 1 (Python) rechnet korrekt
Die Zelle entscheidet NICHT,       ABER: Das LLM entscheidet,
ob das Immunsystem aktiviert       ob es Layer 1 aufruft
wird                               oder einfach selbst antwortet

→ Das Immunsystem schützt          → «Der Wirt entscheidet,
  den Wirt OHNE dessen                ob der Virus leben darf»
  Erlaubnis
```

**Die Lösung: Der Immune Gateway** — ein automatischer Mechanismus, der *vor* dem LLM läuft, wie ein angeborenes Immunsystem:

```
VORHER (krank):
    User fragt → LLM denkt nach → LLM entscheidet ob es rechnet
                                   ↑
                          Der Wirt kontrolliert
                          das Immunsystem ❌

NACHHER (gesund):
    User fragt → Immune Gateway feuert AUTOMATISCH
                     → Layer 1 rechnet
                         → Ergebnis wird dem LLM injiziert
                             → LLM MUSS Ergebnis verwenden

                 Das Immunsystem arbeitet
                 AUTONOM — wie in der Biologie ✅
```

---

## Der Datenfluss durch die drei Layer

Ein konkretes Beispiel: Ein User fragt «Was ist Loss Aversion bei Heizungsersatz in der Schweiz?»

```
User-Frage
    │
    ▼
LAYER 3 (LLM / Dolmetscher)       "Was ist λ bei Heizungsersatz CH?"
Anfälligkeit: 0.8                   → Versteht die Frage
    │                                → Identifiziert Kontext
    ▼
LAYER 2 (YAML / Laborhandbuch)     parameter-registry.yaml
Anfälligkeit: 0.3                   → λ_R = 2.5 (Quelle: Kahneman & Tversky 1979)
    │                                → Kontext-Faktoren Schweiz
    ▼
LAYER 1 (Python / Taschenrechner)   pct.py
Anfälligkeit: 0.0                   → θ_B = 2.5 × 1.2 × 1.3 × 1.4 = 4.58
    │                                → Deterministisch, reproduzierbar
    ▼
LAYER 3 (LLM / zurück zum Dolmetscher)
    │                                → "Loss Aversion ist hier 4.58, weil..."
    ▼
User bekommt korrekte Antwort
```

**Ohne die drei Layer** hätte das LLM einfach gesagt: «Loss Aversion ist ungefähr 2.25» — eine Zahl aus dem Gedächtnis, ohne Kontextanpassung, ohne Quellenangabe. Der Virus hätte gelebt.

---

## Merksatz

> **BEATRIX ist der Patient — ein evidenzbasiertes Entscheidungssystem, das korrekte Analysen liefern soll. Dieses System wird angetrieben von einem LLM (Claude Code), das als Dolmetscher arbeitet: Es versteht Fragen und erklärt Ergebnisse. Aber dieser Dolmetscher ist gleichzeitig der Wirt — denn in ihm können Viren entstehen: falsche Zahlen, die er aus seiner Erinnerung «halluziniert» statt sie nachzuschlagen oder zu berechnen.**
>
> **Damit diese Viren keinen Schaden anrichten, hat BEATRIX ein dreischichtiges Immunsystem — die drei Layer: Layer 1 (der Taschenrechner) rechnet deterministisch und kann nicht halluzinieren. Layer 2 (das Laborhandbuch) liefert validierte Werte mit Quellenangabe. Layer 3 (der Dolmetscher, das LLM) darf nur übersetzen, nie erfinden.**
>
> **Das Paradoxon, das Gerhard Fehr beschreibt: Ursprünglich entschied der Wirt selbst, ob er das Immunsystem aktiviert — das LLM entschied, ob es den Taschenrechner benutzt oder einfach aus dem Gedächtnis antwortet. Das ist, als hätte eine infizierte Zelle ein Vetorecht gegen die weissen Blutkörperchen. Die Lösung: Ein autonomes Immunsystem (der Immune Gateway), das automatisch vor dem LLM läuft — so wie das biologische Immunsystem arbeitet, ohne die Zelle um Erlaubnis zu fragen.**

---

## Zwei Virentypen

| Typ | Biologische Analogie | Greift an | Abwehr |
|-----|---------------------|-----------|--------|
| **EIV** (External Information Virus) | Grippe — kommt von aussen | Layer 3 (LLM halluziniert aus Trainingsdaten) | Layer 1 rechnet unabhängig |
| **EGD** (Endogenous Genetic Defect) | Sichelzellenanämie — die DNA selbst ist defekt | Layer 1 (mehrdeutige Definitionen führen zu falschen Berechnungen) | Saubere Definitionen, eindeutige Symbole |

---

## Referenzen

| Dokument | Pfad |
|----------|------|
| Virus-Definition (SSOT) | `data/knowledge/canonical/virus-definition.yaml` |
| Three-Layer Architecture (SSOT) | `data/knowledge/canonical/three-layer-architecture.yaml` |
| Three-Layer Architecture (Deep-Dive) | `docs/frameworks/three-layer-architecture.md` |
| Immune Gateway (Code) | `scripts/immune_gateway.py` |
| BEATRIX Overview | `docs/funding/BEATRIX-INNOSUISSE-OVERVIEW.md` |
