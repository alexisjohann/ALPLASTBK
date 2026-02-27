# /case-manage - Case Identification & Storage Skill

Interaktiver Skill zum Finden ähnlicher Cases und Anlegen neuer Cases.

## Modi

```bash
/case-manage find              # Ähnliche Cases suchen (geführt)
/case-manage add               # Neuen Case anlegen (geführt)
/case-manage quick             # Schnell-Erfassung (minimal)
```

---

## MODUS 1: FIND - Ähnliche Cases identifizieren

**Workflow:**

### Schritt 1: Kontext erfassen
Frage den User nach dem aktuellen Kontext:

```
Beschreibe kurz deine Situation:
- Was ist das Zielverhalten?
- Welche Domain (health/finance/energy/...)?
- Welche Zielgruppe?
```

### Schritt 2: 10C-Koordinaten ableiten
Aus der Beschreibung die 10C-Koordinaten extrahieren:

| C | Frage an User (falls unklar) |
|---|------------------------------|
| WHO | Wie heterogen ist die Zielgruppe? (low/medium/high) |
| WHAT | Welche Utility-Dimensionen? (F/E/P/S/D/E) |
| HOW | Wie stark hängen Faktoren zusammen? (γ niedrig/mittel/hoch) |
| WHEN | Welcher Kontext dominiert? (culture/environment/social/...) |
| WHERE | Woher kommen deine Daten? (literature/pilot/expert) |
| AWARE | Wie bewusst ist der Zielgruppe das Problem? (0-1) |
| READY | Wie handlungsbereit? (0-1) |
| STAGE | Journey-Phase? (precontemplation/.../maintenance) |
| HIERARCHY | Welche Entscheidungsebene? (L0/L1/L2/L3) |

### Schritt 3: Query ausführen
```bash
python scripts/query_cases.py --domain {domain} --stage {stage} --hierarchy {level}
```

### Schritt 4: Matches präsentieren
Zeige die Top-3-5 ähnlichsten Cases mit:
- Name und Kern-Insight
- 10C-Übereinstimmung (%)
- Relevante Formeln/Parameter
- Link zum vollständigen Case

### Schritt 5: Anwendung
Für jeden relevanten Case fragen:
- "Wie lässt sich dieser Insight auf deine Situation übertragen?"
- Parameter-Anpassungen vorschlagen

---

## MODUS 2: ADD - Neuen Case anlegen

**Workflow:**

### Schritt 1: Basis-Informationen
```
1. Gib dem Case einen kurzen Namen (max 50 Zeichen):
   >

2. Beschreibe den Case in 1-2 Sätzen:
   >

3. Domain(s) - wähle alle zutreffenden:
   [ ] health     [ ] finance    [ ] energy
   [ ] government [ ] nonprofit  [ ] digital
   [ ] education  [ ] workplace  [ ] other: ___
```

### Schritt 2: 10C-Koordinaten (geführt)

Für jede Dimension 3 Optionen + Custom anbieten:

```
WHO - Wer ist betroffen?
  [1] Individual, low heterogeneity
  [2] Individual, high heterogeneity (multiple segments)
  [3] Group/Organization level
  [4] Custom: ___

WHAT - Welche Utility-Dimensionen?
  [1] Financial (F) + Psychological (P)
  [2] Health (P) + Social (S)
  [3] Environmental (E) + Social (S)
  [4] Custom: ___

HOW - Wie stark die Komplementarität?
  [1] Niedrig (γ < 0.3) - Faktoren weitgehend unabhängig
  [2] Mittel (γ 0.3-0.5) - moderate Interaktionen
  [3] Hoch (γ > 0.5) - starke Abhängigkeiten
  [4] Custom: ___

... [analog für alle 10C]
```

### Schritt 3: Insight & Implication
```
Was ist die Kern-Einsicht dieses Cases (1 Satz)?
>

Was bedeutet das für Interventionsdesign (1-2 Sätze)?
>
```

### Schritt 4: Formeln (optional)
```
Gibt es relevante Formeln oder quantitative Beziehungen?
  [1] Ja, ich habe Effektstärken
  [2] Ja, ich habe eine Formel
  [3] Nein, nur qualitativ
```

### Schritt 5: Referenzen
```
Welche Appendices sind relevant?
> (z.B. S, K, V)

Welche Kapitel?
> (z.B. 17, 19)

Literatur-Keys (falls bekannt)?
> (z.B. thaler2008nudge)
```

### Schritt 6: Tags
```
Freie Tags für Suche (kommasepariert):
> nudge, default, retirement, opt-out
```

### Schritt 7: Generieren & Speichern

1. YAML-Entry generieren
2. Nächste freie CASE-ID ermitteln
3. In `data/case-registry.yaml` einfügen
4. Validierung durchführen
5. User das Ergebnis zeigen

```yaml
# Generierter Entry:
CASE-011:
  name: "..."
  description: "..."
  10C:
    WHO: ...
    # ...
  domain: [...]
  tags: [...]
  insight: "..."
  implication: "..."
  references:
    appendices: [...]
    chapters: [...]
```

### Schritt 8: Commit
```
Case CASE-011 wurde angelegt. Soll ich committen?
  [1] Ja, mit Standard-Message
  [2] Ja, mit Custom-Message
  [3] Nein, später
```

---

## MODUS 3: QUICK - Schnell-Erfassung

Für erfahrene User - minimaler Dialog:

```bash
/case-manage quick "Opt-Out erhöht Organspende um 70%" --domain health --insight "Default dominiert bei hohem θ"
```

Generiert automatisch:
- 10C-Koordinaten aus Kontext inferieren
- Fehlende Werte mit Defaults füllen
- Zur Bestätigung vorlegen

---

## Automatische ID-Vergabe

```python
# Nächste freie ID ermitteln
existing_ids = [int(c.split('-')[1]) for c in cases.keys()]
next_id = max(existing_ids) + 1
new_id = f"CASE-{next_id:03d}"
```

---

## Beispiel-Session

```
User: /case-manage add