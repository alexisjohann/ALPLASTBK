# /intervention-manage - Project Tracking Skill

Interaktiver Skill zum Anlegen, Aktualisieren und Abschließen von Interventions-Projekten.

## Modi

```bash
/intervention-manage new           # Neues Projekt anlegen
/intervention-manage update PRJ-X  # Projekt aktualisieren
/intervention-manage close PRJ-X   # Projekt abschließen (Results + Learnings)
/intervention-manage analyze       # Übergreifende Analyse
```

---

## MODUS 1: NEW - Neues Projekt anlegen

### Phase 1: Meta-Daten

```
NEUES INTERVENTIONS-PROJEKT

1. Projektname:
   >

2. Client (anonymisiert):
   >

3. Domain:
   [1] finance    [2] health     [3] energy
   [4] government [5] education  [6] workplace
   [7] other: ___

4. Geplanter Zeitraum:
   Start: YYYY-MM-DD
   Ende:  YYYY-MM-DD
```

### Phase 2: Context

```
KONTEXT

5. Zielverhalten (was soll sich ändern?):
   >

6. Zielgruppe:
   >

7. Geschätzte Stichprobengröße:
   > n = ___

8. Baseline-Verhalten (aktueller Zustand):
   > ___ % oder Wert: ___

9. Journey-Phase der Zielgruppe:
   [1] Precontemplation - wissen nicht, dass Problem existiert
   [2] Contemplation - denken darüber nach
   [3] Preparation - planen zu handeln
   [4] Action - handeln bereits (teilweise)
   [5] Maintenance - Verhalten stabilisieren
```

### Phase 3: Segmente

```
SEGMENTE

10. Wie heterogen ist die Zielgruppe?
    [1] Homogen - ein Segment reicht
    [2] 2-3 Segmente
    [3] 4+ Segmente

Für jedes Segment:
  Name: ___
  Anteil: ___ %
  σ (Reaktionsstärke auf Interventionen):
    [1] Niedrig (0.5-0.8)
    [2] Mittel (0.9-1.2)
    [3] Hoch (1.3-2.0)
    [4] Custom: ___
```

### Phase 4: Intervention Mix

```
INTERVENTIONS-MIX

Intervention 1:
  ID: I1

  Typ:
    [1] nudge         [2] incentive    [3] information
    [4] commitment    [5] social       [6] environmental

  Subtyp (je nach Typ):
    nudge: [default, labeling, framing, simplification]
    incentive: [monetary, gamification, reward]
    social: [descriptive_norm, injunctive_norm, peer]
    ...

  Beschreibung:
    >

  Timing (Journey-Phase):
    >

  Target-Segment:
    [1] Alle
    [2] Spezifisch: ___

  Erwarteter Beitrag E_i:
    > 0.___

  Konfidenz:
    [1] Hoch (0.8+) - Meta-Analyse vorhanden
    [2] Mittel (0.5-0.8) - Einzelstudien
    [3] Niedrig (0.3-0.5) - Pilot/Expert

  Quelle:
    [1] Literatur - Referenz: ___
    [2] Eigener Pilot
    [3] Expert Estimate

Weitere Intervention hinzufügen? [j/n]
```

### Phase 5: Komplementaritäts-Matrix

```
KOMPLEMENTARITÄTEN

Für jedes Interventions-Paar:

I1 × I2:
  γ_ij:
    [1] Starke Synergie (+0.3 bis +0.5)
    [2] Moderate Synergie (+0.1 bis +0.3)
    [3] Neutral (0)
    [4] Leichte Interferenz (-0.1 bis -0.3)
    [5] Starke Interferenz (-0.3 bis -0.5)
    [6] Custom: ___

  Mechanismus (warum diese Interaktion?):
    >
```

### Phase 6: Predictions generieren

```
PREDICTIONS

Portfolio-Effekt berechnen...

E(P) = Σ E_i + Σ γ_ij · √(E_i · E_j)
     = {E_1} + {E_2} + ... + {γ_12}·√({E_1}·{E_2}) + ...
     = {E_P}

95% Konfidenzintervall: [{CI_lower}, {CI_upper}]

KPIs definieren:
  KPI 1 - Name: ___
         Baseline: ___
         Predicted: ___ (berechnet aus E_P)

  Weitere KPIs? [j/n]
```

### Phase 7: Speichern

```
PROJEKT SPEICHERN

Projekt PRJ-{XXX} wurde angelegt.

Zusammenfassung:
- {n} Interventionen
- E(P) = {value} [{CI}]
- Status: planning

Soll ich committen?
  [1] Ja
  [2] Nein, später
```

---

## MODUS 2: UPDATE - Projekt aktualisieren

```bash
/intervention-manage update PRJ-001
```

```
Was möchtest du aktualisieren?

[1] Status ändern (planning → active → completed)
[2] Intervention hinzufügen
[3] Intervention ändern
[4] Komplementarität anpassen
[5] Prediction neu berechnen
[6] Notizen hinzufügen
```

---

## MODUS 3: CLOSE - Projekt abschließen

```bash
/intervention-manage close PRJ-001
```

### Phase 1: Results erfassen

```
ERGEBNISSE ERFASSEN

Messdatum: YYYY-MM-DD

Für jeden KPI:
  {KPI-Name}:
    Predicted: {value}
    Actual:    > ___
```

### Phase 2: Interventions-Attribution

```
INTERVENTIONS-EFFEKTE

Für jede Intervention:
  {I1} - {description}:
    Predicted E_i: {value}
    Observed E_i (geschätzt): > ___
    Attribution-Konfidenz:
      [1] Hoch - kontrollierter Vergleich
      [2] Mittel - zeitliche Analyse
      [3] Niedrig - Expert Judgment
```

### Phase 3: Deviation Analysis

```
ABWEICHUNGSANALYSE

Overall:
  Predicted E(P): {value}
  Actual E(P):    {value}
  Δ: {delta} ({delta_pct}%)
  Direction: {overestimate|underestimate|accurate}

Für jede Intervention mit |Δ| > 0.02:
  {I1}: Predicted {p} → Actual {a} (Δ = {d})

  Mögliche Ursachen (wähle alle zutreffenden):
    [ ] Kontext anders als angenommen
    [ ] Segment-Verteilung anders
    [ ] Implementation nicht wie geplant
    [ ] Interaktionseffekte anders
    [ ] Parameter-Schätzung falsch
    [ ] Andere: ___

Root Causes (Hauptursachen):
  1. Ursache: ___
     Evidenz: ___
     Konfidenz: [high|medium|low]
```

### Phase 4: Learnings

```
LEARNINGS

Was hat funktioniert?
  Intervention: ___
  Insight: ___
  Generalisierbar? [j/n]

Was hat NICHT funktioniert?
  Intervention: ___
  Insight: ___
  War es vermeidbar? [j/n]

Parameter-Updates (automatisch vorgeschlagen):
  {parameter}: {old} → {new}
  Übernehmen? [j/n]

Recommendations:
  Kategorie: [design|timing|targeting|measurement]
  Empfehlung: ___
  Priorität: [high|medium|low]
```

### Phase 5: Speichern & Aggregate Update

```
PROJEKT ABGESCHLOSSEN

PRJ-{XXX} wurde mit Status 'analyzed' gespeichert.

Aggregierte Learnings wurden aktualisiert:
- {n} neue Parameter-Updates
- {n} neue Design Principles
- {n} neue Recommendations

Soll ich die Parameter in BBB (Parameter Repository) aktualisieren?
  [1] Ja, alle übernehmen
  [2] Einzeln bestätigen
  [3] Nein, nur lokal speichern
```

---

## MODUS 4: ANALYZE - Übergreifende Analyse

```bash
/intervention-manage analyze
```

```
ÜBERGREIFENDE ANALYSE

[1] Prediction Accuracy über Zeit
[2] Systematische Über-/Unterschätzungen
[3] Parameter-Drift erkennen
[4] Best/Worst Interventions
[5] Segment-Response-Patterns
[6] DACH vs. Literatur Vergleich
```

---

## Integration

```
/case-manage find     →  Ähnliche Cases für Design finden
        ↓
/design-model         →  Intervention Mix designen
        ↓
/intervention-manage new  →  Projekt anlegen mit Predictions
        ↓
[Durchführung]
        ↓
/intervention-manage close  →  Results & Learnings erfassen
        ↓
/case-manage add      →  Neuen Case aus Projekt erstellen
```
