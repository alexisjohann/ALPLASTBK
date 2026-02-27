# /infographic — NotebookLM Infographic Prompt Generator

## Beschreibung
Generiert fertige Copy-Paste Prompts für Google NotebookLM Infografiken in 3 Formaten (Landscape, Portrait, Square) basierend auf dem FehrAdvice Design System. Enthält einen **3-Iterationen QA-Loop** als Pflicht-Qualitätssicherung.

## SSOT
- **Design System:** `templates/infographic-design-system.yaml`
- **Prompt Templates:** `templates/notebooklm-prompt-{landscape,portrait,square}.md`
- **Scoring Checklist:** `templates/infographic-scoring-checklist.yaml`
- **Presets:** `templates/infographic-presets/{kunde}.yaml`

## Verwendung

```
/infographic                          # Interaktiver Modus (geführt)
/infographic --preset spo             # Mit SPÖ-Preset (Farben, Hashtag, Ehrlichkeit vorausgefüllt)
/infographic --preset spo --thema inflation   # SPÖ + Thema → fast alles vorausgefüllt
/infographic --format landscape       # Nur Landscape generieren
/infographic --format all             # Alle 3 Formate generieren
/infographic --score                  # Bestehende Infografik bewerten (Einzelbild)
/infographic --qa                     # Vollen 3-Iterationen QA-Loop starten
```

## Verfügbare Presets

| Preset | Datei | Primärfarbe | Hashtag |
|--------|-------|-------------|---------|
| `spo` | `templates/infographic-presets/spo.yaml` | #E3000F (Rot) | #OrdnenStattSpalten |

Presets enthalten: Farben, Hashtag, Ehrlichkeits-Linien pro Thema, Standard-Vergleiche, bekannte Verwundbarkeiten, Themen-Bibliothek mit vorkonfigurierten Datenpunkten.

---

## DER WORKFLOW (6 Phasen)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  /infographic WORKFLOW                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Phase 0  →  Modus wählen (Generieren / Bewerten / QA-Loop)            │
│      ↓                                                                  │
│  Phase 1  →  Briefing sammeln (oder Preset laden)                      │
│      ↓                                                                  │
│  Phase 2  →  Template befüllen + Pre-Generation Gate                   │
│      ↓                                                                  │
│  Phase 3  →  Prompt ausgeben → User generiert in NotebookLM            │
│      ↓                                                                  │
│  Phase 4  →  3-ITERATIONEN QA-LOOP (PFLICHT!)                          │
│      │       ┌──────────────────────────────────────────┐              │
│      │       │  R1: Struktur & Vollständigkeit → Score  │              │
│      │       │  R2: Daten & Halluzinationen → Score     │              │
│      │       │  R3: Feinschliff & BehavEcon → Score     │              │
│      │       │  R4*: Exzellenz (optional)               │              │
│      │       └──────────────────────────────────────────┘              │
│      ↓                                                                  │
│  Phase 5  →  Freigabe (Score ≥ 8.5) + Iterations-Protokoll            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 0: Modus wählen

```
┌─────────────────────────────────────────────────────────────────────────┐
│  /infographic — Was möchtest du?                                        │
│                                                                         │
│  1  GENERIEREN   Neue Infografik-Prompts erstellen                      │
│  2  BEWERTEN     Einzelnes Bild scoren (ohne Loop)                      │
│  3  QA-LOOP      Vollen 3-Iterationen Qualitätsprozess starten         │
│  4  ALLE 3       Prompts für Landscape + Portrait + Square              │
│                                                                         │
│  Preset?   --preset spo / --preset fehradvice / ohne                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Briefing sammeln

**Ohne Preset:** Claude stellt 10 Briefing-Fragen:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BRIEFING                                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. THEMA: Worum geht es?                                               │
│  2. KERNBOTSCHAFT: Action Title (These + Richtung)                      │
│  3. KILLER-ZAHL: Die EINE Hauptzahl + max 2 sekundäre                  │
│  4. MASSNAHMEN: 3 konkrete Massnahmen (je mit Zahl)                    │
│  5. VERGLEICH: Womit vergleichen? (optional)                            │
│  6. EHRLICHKEIT: Welche Schwäche eingestehen?                           │
│  7. QUELLE + DATUM: Konkrete Institution + Monat/Jahr                  │
│  8. FARBE: Primärfarbe (Hex)                                            │
│  9. FORMAT: Landscape / Portrait / Square / Alle 3                      │
│  10. HASHTAG: Closer-Hashtag                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Mit Preset (`--preset spo`):** Farbe, Hashtag, Ehrlichkeits-Linie, Vergleiche sind vorausgefüllt. Nur noch Thema + Zahlen eingeben.

**Mit Preset + Thema (`--preset spo --thema inflation`):** Fast alles vorausgefüllt aus der Themen-Bibliothek. User bestätigt oder passt an.

### Phase 2: Template befüllen + Pre-Generation Gate

Claude liest `templates/notebooklm-prompt-{format}.md`, ersetzt alle `{{PLATZHALTER}}` und prüft:

```
PRE-GENERATION GATE
☐ Alle Platzhalter befüllt (keine {{...}} im Output)?
☐ Alle Zahlen mit Einheit und Kontext?
☐ Action Title ist These (nicht Beschreibung)?
☐ Ehrlichkeits-Linie formuliert?
☐ Max 1 Primary + 2 Secondary Killer Numbers?
☐ Quellenangabe konkret (Institution + Monat Jahr)?
☐ Keine vagen Adjektive statt Zahlen?
☐ Bekannte Verwundbarkeiten geprüft (aus Preset)?
```

### Phase 3: Prompt ausgeben

```
═══════════════════════════════════════════════════════════════
NOTEBOOKLM PROMPT — [FORMAT] (16:9 / 9:16 / 1:1)
Thema: [THEMA] | Runde: 1/3
═══════════════════════════════════════════════════════════════

[Vollständiger Prompt — direkt in NotebookLM einfügen]

═══════════════════════════════════════════════════════════════
Generiere diesen Prompt in NotebookLM und teile das Ergebnis-Bild.
═══════════════════════════════════════════════════════════════
```

### Phase 4: 3-ITERATIONEN QA-LOOP (PFLICHT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  3-ITERATIONEN QA-LOOP                                                  │
│  PFLICHT — Minimum 3 Runden, jede findet ANDERE Fehler                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WARUM?  Erfahrungswert: 6.0 → 8.0 → 8.5 → 9.0                        │
│          Runde 1 findet Strukturfehler                                  │
│          Runde 2 findet Halluzinationen                                 │
│          Runde 3 findet Feinheiten                                      │
│                                                                         │
│  WICHTIG: NotebookLM kann NICHT iterieren!                              │
│           Jede Runde = NEUER KOMPLETTER Prompt                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**RUNDE 1 — Struktur & Vollständigkeit**

User teilt Bild → Claude bewertet mit Fokus:
```
R1 CHECKLISTE:
☐ Alle Elemente vorhanden? (Header, Killer-Zahl, Massnahmen, Vergleich, Closer)
☐ Architektur korrekt? (2 Spalten / 7 Sektionen / 2x2 Grid)
☐ Leserichtung klar? (Links=Problem, Rechts=Lösung)
☐ Alle 3 Massnahmen mit konkreten Zahlen?
☐ Ehrlichkeits-Linie vorhanden und richtig platziert?
☐ ≤ 7 Informations-Cluster?
```

Typische R1-Fehler: Fehlende Sektion, falsches Layout, Ehrlichkeit fehlt, zu viele Cluster.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  RUNDE 1 ERGEBNIS                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Score: _/10 (erwartet: 6.0-7.5)                                       │
│  Fixes für Runde 2:                                                     │
│  → [konkrete Änderungen am Prompt]                                      │
│                                                                         │
│  NEUER PROMPT FÜR RUNDE 2:                                              │
│  [Kompletter Prompt mit eingebauten Fixes]                              │
└─────────────────────────────────────────────────────────────────────────┘
```

**RUNDE 2 — Daten-Integrität & Halluzinationen**

User generiert mit R2-Prompt → teilt Bild → Claude bewertet:
```
R2 CHECKLISTE:
☐ ALLE Zahlen stimmen exakt mit Quelle überein?
☐ Keine NotebookLM-Halluzinationen? (Datum, Quelle, Werte)
☐ Konkrete Zahlen statt vager Adjektive? ('15.000 €' nicht 'hohe Strafen')
☐ Datum in Quellenangabe korrekt?
☐ Vergleichswerte korrekt?
☐ Österreichisches Deutsch? (Jänner, nicht Januar)
```

Typische R2-Fehler: Falsches Datum ('Oktober 2023' statt 'Jänner 2026'), erfundene Quelle, gerundete Zahlen.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  RUNDE 2 ERGEBNIS                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Score: _/10 (erwartet: 7.5-8.5)                                       │
│  Fixes für Runde 3:                                                     │
│  → [konkrete Änderungen am Prompt]                                      │
│                                                                         │
│  NEUER PROMPT FÜR RUNDE 3:                                              │
│  [Kompletter Prompt mit eingebauten Fixes]                              │
└─────────────────────────────────────────────────────────────────────────┘
```

**RUNDE 3 — Feinschliff & Verhaltensökonomie**

User generiert mit R3-Prompt → teilt Bild → Claude bewertet:
```
R3 CHECKLISTE:
☐ Anchor (Killer-Zahl) ist visuell dominantestes Element?
☐ Gain-Frame für Massnahmen wirkt? (Entlastung, nicht Kosten)
☐ Ehrlichkeits-Linie genau richtig? (nicht zu schwach, nicht zu stark)
☐ Closer passt? (Hashtag + Fazit + korrekte Quelle)
☐ Zielgruppe getroffen? (Sprache, Kanal, Format)
☐ Keine Angriffsfläche? (Cherry-Picking, fehlender Kontext)
```

```
┌─────────────────────────────────────────────────────────────────────────┐
│  RUNDE 3 ERGEBNIS                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Score: _/10 (erwartet: 8.5-9.5)                                       │
│                                                                         │
│  ≥ 8.5  →  FREIGABE                                                    │
│  < 8.5  →  RUNDE 4 (Bonus) mit spezifischen Fixes                     │
│  < 8.0  →  Grundsätzliche Überarbeitung, zurück zu Phase 1            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**RUNDE 4 (Bonus) — Exzellenz** (nur bei Score < 9.0 nach R3)
```
R4 FOKUS:
☐ Gibt es EIN Element, das den Score auf 9.0+ hebt?
☐ Emotionaler Bogen vollständig? (Problem → Lösung → Beweis → Hoffnung)
☐ Würde ein Journalist diese Grafik ohne Änderung verwenden?
```

### Phase 5: Freigabe + Iterations-Protokoll

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ITERATIONS-PROTOKOLL                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Thema:    [...]                                                        │
│  Format:   [Landscape / Portrait / Square]                              │
│  Preset:   [spo / fehradvice / keiner]                                  │
│  Datum:    [...]                                                        │
│                                                                         │
│  RUNDE  FOKUS              SCORE    FIXES                               │
│  ─────  ─────              ─────    ─────                               │
│  R1     Struktur           _/10     [...]                               │
│  R2     Daten              _/10     [...]                               │
│  R3     Feinschliff        _/10     [...]                               │
│  R4*    Exzellenz          _/10     [...]                               │
│                                                                         │
│  FINAL SCORE:  _/10                                                     │
│  VERDICT:      [Freigabe / Nachbesserung]                               │
│  FREIGABE:     [Ja, Score ≥ 8.5 / Nein]                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Bei Freigabe:** Claude speichert das Iterations-Protokoll.

---

## SCORING-KRITERIEN (6 Dimensionen, gewichtet)

| # | Kriterium | Gewicht | Beschreibung |
|---|-----------|---------|--------------|
| K1 | Frame-Konsistenz | 20% | Passt alles zur Strategie/Botschaft? |
| K2 | Verhaltenswirksamkeit | 20% | Anchoring, Framing, Inoculation, Salience, Fluency |
| K3 | Angriffsfläche (inv.) | 20% | Wie verwundbar für Gegenangriffe? |
| K4 | Visuelle Klarheit | 15% | Sofort verständlich? 3-Sekunden-Test? |
| K5 | Daten-Integrität | 15% | Zahlen korrekt? Keine Halluzinationen? |
| K6 | Zielgruppen-Abdeckung | 10% | Sprache, Kanal, Format passend? |

**Schwellenwerte:**
- **≥ 9.0** — Exzellent, sofort einsetzbar
- **≥ 8.5** — Freigabe
- **8.0-8.4** — Freigabe mit optionalen Feinheiten
- **6.0-7.9** — Nachbesserung, neu generieren
- **< 6.0** — Neustart

---

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `templates/infographic-design-system.yaml` | SSOT: Design-Regeln + QA-Loop |
| `templates/notebooklm-prompt-landscape.md` | Landscape Template (16:9) |
| `templates/notebooklm-prompt-portrait.md` | Portrait Template (9:16) |
| `templates/notebooklm-prompt-square.md` | Square Template (1:1) |
| `templates/infographic-scoring-checklist.yaml` | 6-Kriterien Bewertung |
| `templates/infographic-presets/spo.yaml` | SPÖ-Preset (Farben, Themen, Verwundbarkeiten) |

## Beispiel-Session (mit Preset + QA-Loop)

```
User: /infographic --preset spo --thema inflation
Claude: SPÖ-Preset geladen. Thema: Inflation.
        Vorausgefüllt: Rot, #OrdnenStattSpalten, -0.7% als Killer-Zahl, ...
        Format? → Landscape

        [Gibt Prompt aus — Runde 1/3]

User: [generiert in NotebookLM, teilt Bild]
Claude: RUNDE 1 — Struktur: 7.2/10
        Fixes: Vergleichstabelle fehlt, Ehrlichkeit falsch platziert
        [Gibt neuen Prompt aus — Runde 2/3]

User: [generiert neu, teilt Bild]
Claude: RUNDE 2 — Daten: 8.3/10
        Fixes: Datum zeigt 'Oktober 2023' statt 'Jänner 2026'
        [Gibt neuen Prompt aus — Runde 3/3]

User: [generiert neu, teilt Bild]
Claude: RUNDE 3 — Feinschliff: 9.0/10
        FREIGABE! Exzellent.
        [Iterations-Protokoll]
```

## NotebookLM-Einschränkungen (KRITISCH)

```
NotebookLM kann NICHT iterieren — jeder Prompt = komplett neuer Start
NotebookLM halluziniert Daten wenn nicht explizit im Prompt
NotebookLM halluziniert Quellen wenn nicht explizit im Prompt
Vage Begriffe ('hohe Strafen') werden NICHT in Zahlen umgewandelt
Bei Score < 8.0: NEUEN KOMPLETTEN Prompt generieren
```

## Verhaltensökonomische Prinzipien

| Prinzip | Anwendung | Runde |
|---------|-----------|-------|
| **Anchoring** | Killer-Zahl als erster Anker | R1 (Platzierung), R3 (Dominanz) |
| **Framing** | Gain-Frame Massnahmen, Loss-Frame Status Quo | R3 |
| **Inoculation** | Ehrlichkeits-Linie vor Hauptargument | R1 (vorhanden?), R3 (Qualität) |
| **Social Proof** | Vergleichstabelle mit Belegen | R1 (vorhanden?), R2 (korrekt?) |
| **Salience** | Grösste Zahl = wichtigstes Argument | R3 |
| **Processing Fluency** | Max 7 Cluster, max 25 Worte | R1 |
