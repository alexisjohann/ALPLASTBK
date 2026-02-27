# Rejected Concepts Registry

> Evidence Integration Pipeline: Verworfene Konzepte
> Erstellt: 2026-01-19 | Status: Active

---

## Übersicht

Dieses Dokument dokumentiert Konzepte, die durch die **Evidence Integration Pipeline (EIP)** geprüft und **verworfen** wurden.

**Zweck:**
- Verhindert wiederholte Evaluation desselben Konzepts
- Dokumentiert Gründe für Ablehnung
- Ermöglicht Re-Evaluation bei neuer Evidenz
- Dient als Lernressource (was funktioniert NICHT)

**Referenz:** `docs/workflows/evidence-integration-pipeline.md`

---

## Entscheidungsmatrix (Wann wird verworfen?)

| PRO-Evidenz | CONTRA-Evidenz | Entscheidung |
|-------------|----------------|--------------|
| Schwach | Stark | ❌ VERWERFEN |
| Keine | - | ❌ VERWERFEN (keine Evidenz) |
| Mittel | Stark | ❌ VERWERFEN oder MODIFIZIEREN |

---

## Verworfene Konzepte

### Format für Einträge

```yaml
rejected_concept:
  id: "CONC-YYYY-NNN"
  name: "Name des Konzepts"
  description: "Was sollte es tun?"
  proposed_by: "Session / Quelle"
  date: "YYYY-MM-DD"

  contra_evidence:
    - paper: "citation_key"
      finding: "Was sagt das Paper?"
      threat_level: "high/medium"

  reason: "Warum wurde es verworfen?"
  lesson_learned: "Was haben wir gelernt?"

  re_evaluation_possible: true/false
  re_evaluation_condition: "Unter welchen Bedingungen neu evaluieren?"
```

---

## Register der verworfenen Konzepte

### (Noch keine Einträge)

*Bisher wurden alle geprüften Konzepte integriert oder modifiziert.*

---

## Beispiel-Einträge (Hypothetisch)

### CONC-XXXX-001: Gamification Points System

```yaml
rejected_concept:
  id: "CONC-XXXX-001"
  name: "Gamification Points System"
  description: "Punkte für Zielerreichung mit Leaderboard und Badges"
  proposed_by: "Hypothetisches Beispiel"
  date: "XXXX-XX-XX"

  contra_evidence:
    - paper: "deci1999"
      finding: "Extrinsische Rewards untergraben intrinsische Motivation"
      threat_level: "high"
    - paper: "gneezy2000"
      finding: "Kleine Anreize können Backfire-Effekte haben"
      threat_level: "high"
    - paper: "ariely2008"
      finding: "Social vs. Market Norms - Gamification kann Social Norms zerstören"
      threat_level: "medium"

  reason: "Starke Contra-Evidenz zu Crowding-Out von intrinsischer Motivation"
  lesson_learned: "Extrinsische Gamification-Elemente nur mit großer Vorsicht einsetzen"

  re_evaluation_possible: true
  re_evaluation_condition: |
    Neue Evidenz zu kontextspezifischen Effekten
    ODER Gamification ohne direkten Performance-Link
    ODER nur für Lernkontexte (nicht Performance)
```

### CONC-XXXX-002: Peer Pressure Naming

```yaml
rejected_concept:
  id: "CONC-XXXX-002"
  name: "Peer Pressure durch öffentliche Nennung"
  description: "Schlechteste Performer werden öffentlich benannt"
  proposed_by: "Hypothetisches Beispiel"
  date: "XXXX-XX-XX"

  contra_evidence:
    - paper: "cialdini2007"
      finding: "Negative Social Proof kann unbeabsichtigte Effekte haben"
      threat_level: "high"
    - paper: "fehr2002"
      finding: "Shame-basierte Interventionen können Reaktanz auslösen"
      threat_level: "high"

  reason: "Ethisch problematisch + starke Backfire-Risiken"
  lesson_learned: "Social Interventions sollten positive Normen verstärken, nicht negative bestrafen"

  re_evaluation_possible: false
  re_evaluation_condition: "N/A - ethisch nicht vertretbar"
```

---

## Statistiken

| Metrik | Wert |
|--------|------|
| Total verworfene Konzepte | 0 |
| Davon re-evaluierbar | 0 |
| Letztes Update | 2026-01-19 |

---

## Re-Evaluation Prozess

Wenn neue Evidenz verfügbar wird:

1. **Trigger:** Neue Paper, Meta-Analyse, oder Case Study
2. **Prüfung:** Adressiert die neue Evidenz die Gründe für Ablehnung?
3. **EIP erneut durchführen:** Vollständiger Workflow mit neuer Evidenz
4. **Dokumentation:**
   - Bei Integration: In `concept-registry.yaml` verschieben
   - Bei erneuter Ablehnung: `re_evaluation_history` ergänzen

---

*Dieses Register ist Teil der Quality Assurance des EBF Frameworks.*
