# BIS-Berechnungslogik: Behavioral Impact Score

**Projekt:** BFE-019 ECHfP Wirkungsmessung
**Version:** 2.1
**Datum:** 2026-02-23
**Änderungen v2.1:** Exaktes INTRO→Modul-Mapping aus Nullmessung-SSOT (nicht-sequenziell!), Antwortskalen korrigiert, Worked Examples korrigiert
**Änderungen v2.0:** Gewichte Model B, korrektes Item-Mapping, Namespace-Auflösung
**SSOT:** `260113_BFE_Nullmessung ECHfP_Fragebogen_Review intervista_sib.xlsx` (Intervista-Original, PRIMÄR), `fragebogen_parameter_analyse.yaml` (Item→Parameter), `fragebogen_tracking_v5_ebf.yaml` (Items)
**Zielgruppe:** Intervista (Programmierung), FehrAdvice (Auswertung), BFE (Reporting)

---

## 1. Übersicht

Der **Behavioral Impact Score (BIS)** ist ein gewichteter Komposit-Index, der die Wirkung der ECHfP-Kampagne entlang von vier Verhaltensdimensionen misst.

### Gesamt-Formel

```
G = 0.20 × A + 0.30 × W + 0.30 × I + 0.20 × T

Wobei:
  G ∈ [0, 100]    Behavioral Impact Score (Gesamt)
  A ∈ [0, 100]    Awareness
  W ∈ [0, 100]    Willingness
  I ∈ [0, 100]    Impact          ← zusammen mit W höchstes Gewicht
  T ∈ [0, 100]    Trust
```

### Gewichtungs-Rationale (Model B: Progressions-Logik)

| Dimension | Gewicht | Begründung |
|-----------|---------|------------|
| **A** Awareness | 0.20 | Notwendig, aber nicht hinreichend — übergewichtet in v1.0 |
| **W** Willingness | 0.30 | Kernhebel — W erklärt die grösste Varianz im Übergang zu Handlung |
| **I** Impact | 0.30 | Tatsächliche Verhaltensänderung — gleichrangig mit Willingness |
| **T** Trust | 0.20 | Enabler — moderiert W und I, wirkt aber nicht eigenständig |

**Warum Model B (0.20/0.30/0.30/0.20) statt v1.0 (0.25/0.25/0.30/0.20):**

1. **W ist der grösste Hebel**: W enthält Motivation, Self-Efficacy, Normen und Barrieren — alles gleichzeitig. Diese Dimension kann durch Kampagnen-Interventionen am stärksten beeinflusst werden.
2. **A wird schnell gesättigt**: Awareness steigt nach 1–2 Kampagnenwellen auf 70+ und stagniert. Ein Score, der A mit 0.25 gewichtet, zeigt dann kaum noch Veränderung.
3. **Symmetrie W=I**: Der BIS misst Wirkung. Bereitschaft (W) und Handlung (I) sind die zwei Seiten der Wirkung. Gleiche Gewichtung erzwingt, dass BIS nur steigt, wenn beides zusammen wächst.

### Score-Interpretation

| Bereich | Label | Farbe | Handlungsbedarf |
|---------|-------|-------|-----------------|
| 0–30 | Kritisch | Rot | Sofortige Intervention nötig |
| 31–50 | Verbesserungsbedarf | Orange | Gezielte Massnahmen |
| 51–70 | Zufriedenstellend | Gelb | Monitoring, punktuelle Optimierung |
| 71–85 | Gut | Hellgrün | Kurs halten, Feinschliff |
| 86–100 | Exzellent | Grün | Best Practice dokumentieren |

### Zielwerte

| Dimension | Baseline | Jahr 1 | Jahr 3 |
|-----------|----------|--------|--------|
| A (Awareness) | 35 | 55 | 75 |
| W (Willingness) | 30 | 45 | 60 |
| I (Impact) | 15 | 25 | 40 |
| T (Trust) | 65 | 72 | 80 |
| **G (Gesamt)** | **~33** | **~47** | **~62** |

---

## 2. KRITISCH: Item-Quellen und Namenskonventionen

### ⚠️ Namespace-Kollision (aufgelöst in v2.0)

In v1.0 existierte eine **Namespace-Kollision** zwischen zwei Dokumenten:

| ID | In `kpi_architecture.yaml` (v1.0) | In `fragebogen_parameter_analyse.yaml` |
|----|-----------------------------------|-----------------------------------------|
| **W1** | «Generelle Bereitschaft» (1 Likert-Item) | «Grosse persönliche Vorteile» → u_F |
| **W2** | «Spezifische Motivation» (5-Item-Matrix) | «Positives für Gemeinwohl» → u_S |
| **W3** | «Barrieren-Wahrnehmung» (5-Item-Matrix) | «Einklang mit Werten» → u_X |

**Das kpi_architecture-W2** (5-Item-Matrix mit Kosteneinsparung, Umweltschutz, Wertsteigerung, Unabhängigkeit, Fördergelder) **existiert nicht als solches im Fragebogen**. Ebenso existiert das kpi_architecture-W3 (5-Item Barrieren-Matrix) nicht.

### v2.0-Konvention (verbindlich)

Ab v2.0 gelten folgende Namenskonventionen:

| Prefix | Quelle | Beispiel |
|--------|--------|----------|
| **W1–W6** | ECHfP Attitudinal Likert Block | W1 = u_F, W4 = θ_inv |
| **A1–A5** | ECHfP Awareness Likert Block | A1 = Exposure, A4 = Knowledge |
| **T0–T7** | ECHfP Trust Likert Block | T1 = Source Trust, T5 = σ_i |
| **I1–I2** | ECHfP Impact Indikatoren | I1 = Förderprogramme, I2 = Fachleute |
| **F*n*.*m*** | Tracking-Fragebogen «erneuerbar heizen» | F2.1 = Planungsabsicht |
| **INTRO*n*** | Screening + Impact-Items | INTRO4–8 = Bestand, INTRO9–13 = Planung |

### ⚠️ Kritisch: INTRO→Modul-Mapping ist NICHT sequenziell (v2.1)

Die INTRO-Nummern folgen **nicht** der Modul-Reihenfolge M1→M2→M3→M4→M5. Das exakte Mapping aus der Nullmessung-SSOT (Intervista-Original):

| Modul | Beschreibung | Bestand (INTRO) | Planung (INTRO) |
|-------|-------------|-----------------|-----------------|
| **M1** | Gesamtmodernisierung | INTRO4 | INTRO9 |
| **M2** | Gebäudehülle | INTRO6 | INTRO11 |
| **M3** | Heizungsersatz | INTRO7 | INTRO12 |
| **M4** | Solarenergie | INTRO8 | INTRO13 |
| **M5** | E-Mobilität | INTRO5 | INTRO10 |

**Reihenfolge im Fragebogen:** M1 → M5 → M2 → M3 → M4 (für Bestand und Planung identisch)

### Item-Verfügbarkeit pro Dimension

| Dimension | Items im ECHfP-Block | Ergänzende Tracking-Items | Status |
|-----------|---------------------|---------------------------|--------|
| **A** | A1–A5 (5 Likert) | F6.1, F6.2, F6.6, F3.6 | ✅ Berechenbar |
| **W** | W1–W6 (6 Likert) | F2.1, F2.2, F2.3, F4.3 | ✅ Berechenbar |
| **I** | I1, I2 | INTRO4–13, F2.12, F6.7, F5.2 | ✅ Berechenbar |
| **T** | T0–T7 (8 Items) | — | ✅ Berechenbar (mit Korrekturen) |

---

## 3. Dimension A — Awareness

### Definition

Mass für die Bekanntheit der Kampagne, der Förderprogramme und der konkreten Massnahmen bei der Zielgruppe.

### Items und Quellen

| Sub-KPI | Item-Text | Quelle | Skala | BCM-Parameter |
|---------|-----------|--------|-------|---------------|
| A1 | Information/Werbung gesehen (12 Monate) | ECHfP-Block | Ja/Nein/Unsicher | A_exposure |
| A2 | Thema beschäftigt mich | ECHfP-Block | Likert 1–5 | A_salience |
| A3 | Betrifft mich persönlich | ECHfP-Block | Likert 1–5 | A_personal_relevance |
| A4 | Weiss, um was es geht | ECHfP-Block | Likert 1–5 | A_subjective_knowledge |

**Nicht in A-Score (Reklassifizierung):**

| Item | Grund | Fliesst stattdessen in |
|------|-------|------------------------|
| A5 «Verhalten bedeutsam für Gesellschaft» | Misst Werte/Motivation, nicht Wissen | W_base (u_E) |

### Formel

```
A = 0.25 × A1 + 0.25 × A2 + 0.25 × A3 + 0.25 × A4
```

**Normalisierung:**

| Item | Skala | Normalisierung |
|------|-------|----------------|
| A1 | Ja/Nein/Unsicher | Ja=100, Unsicher=50, Nein=0 |
| A2 | Likert 1–5 | (Likert − 1) / 4 × 100 |
| A3 | Likert 1–5 | (Likert − 1) / 4 × 100 |
| A4 | Likert 1–5 | (Likert − 1) / 4 × 100 |

### Ergänzende Tracking-Items (nicht im A-Score, aber im Bericht)

| Item | Was es misst | Reporting-Verwendung |
|------|-------------|---------------------|
| F6.1 | Unaided Recall (offene Frage) | Kampagnen-Awareness qualitativ |
| F6.2 | Aided Recall «erneuerbar heizen» | Kampagnen-Bekanntheit quantitativ |
| F6.6 | Impulsberatung bekannt? | Instrument-Bekanntheit |
| F3.6 | Subjektive Informiertheit | Selbsteinschätzung Wissen |

### Vollständiges A-Beispiel

```
A1 = 100  (Ja, Werbung gesehen)
A2: Likert=4 → A2 = (4-1)/4 × 100 = 75.0
A3: Likert=3 → A3 = (3-1)/4 × 100 = 50.0
A4: Likert=3 → A4 = (3-1)/4 × 100 = 50.0

A = 0.25 × 100 + 0.25 × 75.0 + 0.25 × 50.0 + 0.25 × 50.0
  = 25.0 + 18.75 + 12.5 + 12.5
  = 68.75
```

---

## 4. Dimension W — Willingness

### Definition

Mass für die Handlungsbereitschaft der Zielgruppe, energetische Massnahmen am eigenen Gebäude umzusetzen. Umfasst Motivation, Self-Efficacy, wahrgenommene Barrieren und soziale Normen.

### ⚠️ Korrektur gegenüber v1.0

In v1.0 wurden drei fiktive Sub-KPIs definiert (W1 «Generelle Bereitschaft», W2 «5-Item Motivations-Matrix», W3 «5-Item Barrieren-Matrix»), die im realen Fragebogen nicht existieren. v2.0 basiert auf den **6 tatsächlichen Likert-Items** W1–W6 aus dem ECHfP Attitudinal Block.

### Items und Quellen

| Item | Item-Text | Skala | BCM-Parameter | Konzept |
|------|-----------|-------|---------------|---------|
| W1 | Grosse persönliche Vorteile | Likert 1–5 | u_F | Finanzielle Motivation |
| W2 | Positives für Gemeinwohl/Umwelt | Likert 1–5 | u_S | Prosoziale Motivation |
| W3 | Einklang mit Werten | Likert 1–5 | u_X | Identitäts-Motivation |
| W4 | Traue mir zu, erfolgreich umzusetzen | Likert 1–5 | θ_inv | Self-Efficacy |
| W5 | Prozess erscheint kompliziert | Likert 1–5 | τ | Wahrgenommene Komplexität |
| W6 | Viele andere haben modernisiert | Likert 1–5 | σ_d | Deskriptive Sozialnorm |

**Zusätzlich aus Reklassifizierung:**

| Item | Herkunft | BCM-Parameter | Konzept |
|------|----------|---------------|---------|
| A5 | Awareness-Block (reklassifiziert) | u_E | Environmental Utility |
| T5 | Trust-Block (reklassifiziert) | σ_i | Injunktive Sozialnorm |

### Formel

```
W = 0.15 × W1 + 0.10 × W2 + 0.10 × W3 + 0.20 × W4 + 0.20 × (100 − W5) + 0.10 × W6 + 0.10 × A5 + 0.05 × T5

Wobei:
  W1–W4, W6, A5, T5:  (Likert − 1) / 4 × 100  [direkt: höher = besser]
  W5:                   INVERTIERT (höherer Likert = höhere Barriere = schlechterer Score)
```

### Gewichtungs-Rationale W

| Item | Gewicht | Begründung |
|------|---------|------------|
| W4 (Self-Efficacy) | 0.20 | Stärkster Prädiktor für Übergang zur Handlung (Bandura 1977) |
| W5 (Komplexität, inv.) | 0.20 | Zentrale Barriere; verstärkt Present Bias β (Enke et al. 2024) |
| W1 (u_F) | 0.15 | Finanzieller Nutzen ist Hauptmotivator in Umfragen |
| W2 (u_S) | 0.10 | Warm Glow; Social Desirability Bias (~0.7 Korrektur) |
| W3 (u_X) | 0.10 | Identitäts-Kongruenz; stabilisiert Verhalten langfristig |
| W6 (σ_d) | 0.10 | Deskriptive Norm; Peer-Effekt |
| A5 (u_E) | 0.10 | Environmental Utility; Brücke A→W |
| T5 (σ_i) | 0.05 | Injunktive Norm; puffert Boomerang-Effekt |

### Normalisierung

| Item | Richtung | Normalisierung auf [0, 100] |
|------|----------|-----------------------------|
| W1 | direkt | (Likert − 1) / 4 × 100 |
| W2 | direkt | (Likert − 1) / 4 × 100 |
| W3 | direkt | (Likert − 1) / 4 × 100 |
| W4 | direkt | (Likert − 1) / 4 × 100 |
| W5 | **invertiert** | (Likert − 1) / 4 × 100, dann 100 − Score |
| W6 | direkt | (Likert − 1) / 4 × 100 |
| A5 | direkt | (Likert − 1) / 4 × 100 |
| T5 | direkt | (Likert − 1) / 4 × 100 |

### Ergänzende Tracking-Items (nicht im W-Score, aber im Bericht)

| Item | Was es misst | Reporting-Verwendung |
|------|-------------|---------------------|
| F2.1 | Planungsabsicht (Ja in 2J/5J/Nein) | BCJ-Phase-Indikator |
| F2.2 | Barrieren (Mehrfachauswahl, 8 Optionen) | Barrieren-Profil qualitativ |
| F2.3 | Treiber (Mehrfachauswahl, 7 Optionen) | Motivations-Profil qualitativ |
| F4.3 | 12-Item Einstellungs-Matrix (Likert 1–4) | Vertiefte Einstellungsanalyse |
| F3.10 | Present Bias Choice (CHF 5'000 sofort vs. 6'000 später) | β-Indikator |
| F3.11 | Trigger Events (Was würde Sie bewegen?) | θ-Diagnostik |

### Vollständiges W-Beispiel

```
W1: Likert=4 → 75.0   (persönliche Vorteile: eher ja)
W2: Likert=4 → 75.0   (Gemeinwohl: eher ja)
W3: Likert=3 → 50.0   (Werte: teils/teils)
W4: Likert=3 → 50.0   (Self-Efficacy: teils/teils)
W5: Likert=4 → 75.0   (Komplexität: eher hoch) → invertiert: 100 − 75 = 25.0
W6: Likert=2 → 25.0   (Sozialnorm: wenige andere)
A5: Likert=4 → 75.0   (Umwelt-Bedeutsamkeit: eher ja)
T5: Likert=3 → 50.0   (Umfeld findet sinnvoll: teils/teils)

W = 0.15 × 75 + 0.10 × 75 + 0.10 × 50 + 0.20 × 50
  + 0.20 × 25 + 0.10 × 25 + 0.10 × 75 + 0.05 × 50
  = 11.25 + 7.5 + 5.0 + 10.0 + 5.0 + 2.5 + 7.5 + 2.5
  = 51.25
```

---

## 5. Dimension I — Impact

### Definition

Mass für die tatsächliche Verhaltensänderung — durchgeführte oder konkret geplante energetische Massnahmen.

### ⚠️ Korrektur gegenüber v1.0

In v1.0 referenzierten I1/I2/I3 abstrakte Matrix-Fragen, die nicht 1:1 im Fragebogen existieren. v2.0 nutzt die **tatsächlich verfügbaren Items**: INTRO-Block (Bestand + Planung pro Modul), F2.12 (BCJ Stage), und die Impact-Indikatoren I1/I2 aus dem ECHfP Attitudinal Block.

### Items und Quellen

**Primäre Impact-Items — Bestand (INTRO4–8):**

⚠️ **Mapping ist NICHT sequenziell!** Siehe Abschnitt 2 für kanonische Zuordnungstabelle.

| Item | Modul | Exakter Text (Nullmessung-SSOT) | Antworten |
|------|-------|--------------------------------|-----------|
| INTRO4 | **M1** | Wurde Ihr Gebäude in den letzten 10 Jahren umfassend energetisch modernisiert? | Ja / Nein / Weiss nicht |
| INTRO5 | **M5** | Besitzen Sie aktuell ein Elektroauto und laden Sie dieses zu Hause? | Ja / Nein / Weiss nicht |
| INTRO6 | **M2** | Wurde die Gebäudehülle Ihres Hauses oder Ihrer Wohnung (z.B. Dach, Fassade, Fenster) in den letzten 10 Jahren saniert? | Ja / Nein / Weiss nicht |
| INTRO7 | **M3** | Wird Ihre Heizung aktuell mit erneuerbarer Energie betrieben? | Ja / Nein / Weiss nicht |
| INTRO8 | **M4** | Haben Sie aktuell eine Photovoltaikanlage auf dem Dach oder an der Fassade Ihres Gebäudes installiert? | Ja / Nein / Weiss nicht |

**Primäre Impact-Items — Planung (INTRO9–13):**

| Item | Modul | Exakter Text (Nullmessung-SSOT) | Antworten |
|------|-------|--------------------------------|-----------|
| INTRO9 | **M1** | Planen Sie, Ihr Gebäude in den nächsten 2 Jahren umfassend energetisch zu modernisieren? | Ja / Nein / Weiss nicht |
| INTRO10 | **M5** | Planen Sie, in den nächsten 2 Jahren ein Elektroauto anzuschaffen und dieses zu Hause zu laden? | Ja / Nein / Weiss nicht |
| INTRO11 | **M2** | Planen Sie, die Gebäudehülle Ihres Hauses oder Ihrer Wohnung (z.B. Dach, Fassade, Fenster) in den nächsten 2 Jahren zu sanieren? | Ja / Nein / Weiss nicht |
| INTRO12 | **M3** | Planen Sie, Ihre Heizung oder Warmwasseranlage in den nächsten 2 Jahren auf erneuerbare Energie umzustellen? | Ja / Nein / Weiss nicht |
| INTRO13 | **M4** | Planen Sie, in den nächsten 2 Jahren eine Photovoltaikanlage auf dem Dach oder an der Fassade Ihres Gebäudes zu installieren? | Ja / Nein / Weiss nicht |

**Sekundäre Impact-Items:**

| Item | Text | Quelle | Antworten |
|------|------|--------|-----------|
| F2.12 | BCJ Stage (Wo stehen Sie?) | Tracking v5 | 6 Phasen (UNAWARE→ADVOCACY) |
| I1 | Über Förderprogramme informiert | ECHfP-Block | Ja / Nein |
| I2 | Mit Fachleuten gesprochen | ECHfP-Block | Ja / Nein |
| F6.7 | Impulsberatung in Anspruch genommen | Tracking | Ja / Geplant / Nein |
| F5.2 | Rentabilitätsberechnung gemacht | Tracking | Ja / Geplant / Nein |

### Formel (3 Komponenten)

```
I = 0.45 × I_act + 0.30 × I_plan + 0.25 × I_engage
```

**Komponente I_act (Umgesetzte Massnahmen):**
```
I_act = (Σₘ INTRO_m_done / 5) × 100

Wobei:
  INTRO_m_done pro Modul m ∈ {M1,...,M5}:
    Ja = 1,  Weiss nicht = 0,  Nein = 0

  Modul-Mapping (NICHT sequenziell!):
    M1 = INTRO4,  M2 = INTRO6,  M3 = INTRO7,  M4 = INTRO8,  M5 = INTRO5

  Begründung «Weiss nicht = 0»: Für Bestand zählen nur bestätigte Massnahmen.
  Wer nicht weiss, ob die eigene Heizung erneuerbar ist, hat die Entscheidung
  wahrscheinlich nicht selbst getroffen → konservative Wertung.
```

**Komponente I_plan (Geplante Massnahmen):**
```
I_plan = (Σₘ INTRO_m_plan / 5) × 100

Wobei:
  INTRO_m_plan pro Modul m ∈ {M1,...,M5}:
    Ja = 1,  Weiss nicht = 0.3,  Nein = 0

  Modul-Mapping (NICHT sequenziell!):
    M1 = INTRO9,  M2 = INTRO11,  M3 = INTRO12,  M4 = INTRO13,  M5 = INTRO10
```

**Komponente I_engage (Engagement-Indikatoren):**
```
I_engage = 0.30 × BCJ + 0.25 × Info + 0.25 × Consult + 0.20 × Advice

Wobei:
  BCJ     = F2.12 Stage normalisiert: UNAWARE=0, AWARE=20, CONSIDERATION=40,
            PLANNING=60, ACTION=80, ADVOCACY=100
  Info    = I1 (Förderprogramme informiert): Ja=100, Nein=0
  Consult = I2 (Fachleute gesprochen): Ja=100, Nein=0
  Advice  = F6.7 (Impulsberatung): Ja=100, Geplant=50, Nein=0
```

### Modulspezifischer Impact-Score

Zusätzlich zum aggregierten I-Score wird **pro Modul** ein Impact-Score berechnet:

```
I_Modul_m = 0.50 × INTRO_m_done × 100
          + 0.30 × INTRO_m_plan_norm × 100
          + 0.20 × I_engage

Wobei:
  INTRO_m_done:      Ja=1, Nein=0
  INTRO_m_plan_norm: Ja=1, Weiss nicht=0.3, Nein=0
  I_engage:          gleich für alle Module (nicht modulspezifisch)
```

### Vollständiges I-Beispiel

```
Person: Hat Heizung auf erneuerbar umgestellt (INTRO7=Ja, M3), plant Solar (INTRO13=Ja, M4), Rest nein.
        Ist in BCJ Phase PLANNING (F2.12=4), hat sich über Förderung informiert (I1=Ja),
        mit Installateur gesprochen (I2=Ja), keine Impulsberatung (F6.7=Nein).

I_act:  M1(INTRO4)=0, M2(INTRO6)=0, M3(INTRO7)=1, M4(INTRO8)=0, M5(INTRO5)=0
I_act = (0 + 0 + 1 + 0 + 0) / 5 × 100 = 20.0

I_plan: M1(INTRO9)=0, M2(INTRO11)=0, M3(INTRO12)=0, M4(INTRO13)=1, M5(INTRO10)=0
I_plan = (0 + 0 + 0 + 1 + 0) / 5 × 100 = 20.0

I_engage:
  BCJ = 60 (PLANNING)
  Info = 100 (Ja)
  Consult = 100 (Ja)
  Advice = 0 (Nein)

  I_engage = 0.30 × 60 + 0.25 × 100 + 0.25 × 100 + 0.20 × 0
           = 18 + 25 + 25 + 0 = 68.0

I = 0.45 × 20.0 + 0.30 × 20.0 + 0.25 × 68.0
  = 9.0 + 6.0 + 17.0
  = 32.0
```

---

## 6. Dimension T — Trust

### Definition

Mass für das Vertrauen in den Absender (BFE/EnergieSchweiz), die Glaubwürdigkeit der Informationen und die wahrgenommene Kompetenz.

### ⚠️ Korrekturen gegenüber v1.0

Zwei Items werden aus dem T-Score **ausgeschlossen** (Reklassifizierung):

| Item | v1.0-Zuordnung | v2.0-Zuordnung | Begründung |
|------|---------------|----------------|------------|
| T5 «Umfeld findet sinnvoll» | Trust | → W-Score (σ_i, Gewicht 0.05) | Misst injunktive Sozialnorm, nicht Vertrauen |
| T4 «Freiheit eigene Entscheidung» | Trust | → T-Score (beibehalten) + separat als Ψ_autonomy | Misst Autonomie; bleibt in T, wird aber zusätzlich separat reportet |

### Items und Quellen

| Item | Item-Text | Skala | BCM-Parameter | Im T-Score? |
|------|-----------|-------|---------------|-------------|
| T0 | EnergieSchweiz bekannt? | Ja/Nein | Ψ_trust_gate | Gate (Voraussetzung) |
| T1 | Vertraue ES als Informationsquelle | Likert 1–5 | Ψ_trust_source | ✅ |
| T2 | Informationen glaubwürdig und verlässlich | Likert 1–5 | Ψ_trust_credibility | ✅ |
| T3 | Informationen sind transparent | Likert 1–5 | Ψ_trust_transparency | ✅ |
| T4 | Lässt Freiheit der eigenen Entscheidung | Likert 1–5 | Ψ_autonomy | ✅ |
| T5 | Umfeld findet Massnahme sinnvoll | Likert 1–5 | σ_i | ❌ → W-Score |
| T6 | Würde anderen empfehlen | Likert 1–5 | Advocacy | ✅ |
| T7 | Unsicher ob Informationen stimmen | Likert 1–5 | Ψ_trust_uncertainty | ✅ (invertiert) |

### Gate-Logik

```
WENN T0 = Nein:
  → T-Score = MISSING (Person kennt EnergieSchweiz nicht)
  → Person erhält keinen T-Score (wird bei G-Berechnung separat behandelt)

WENN T0 = Ja:
  → T-Score aus T1–T4, T6, T7 berechnen
```

### Formel (nur bei T0 = Ja)

```
T = 0.25 × T1 + 0.20 × T2 + 0.15 × T3 + 0.15 × T4 + 0.15 × T6 + 0.10 × (100 − T7)
```

### Normalisierung

| Item | Richtung | Normalisierung auf [0, 100] |
|------|----------|-----------------------------|
| T1 | direkt | (Likert − 1) / 4 × 100 |
| T2 | direkt | (Likert − 1) / 4 × 100 |
| T3 | direkt | (Likert − 1) / 4 × 100 |
| T4 | direkt | (Likert − 1) / 4 × 100 |
| T6 | direkt | (Likert − 1) / 4 × 100 |
| T7 | **invertiert** | (Likert − 1) / 4 × 100, dann 100 − Score |

### Vollständiges T-Beispiel

```
T0 = Ja (kennt EnergieSchweiz → T-Score wird berechnet)

T1: Likert=4 → 75.0    (vertraut als Quelle)
T2: Likert=4 → 75.0    (glaubwürdig)
T3: Likert=3 → 50.0    (transparent: teils/teils)
T4: Likert=4 → 75.0    (fühlt sich frei in Entscheidung)
T6: Likert=3 → 50.0    (würde teils empfehlen)
T7: Likert=2 → 25.0    (wenig Misstrauen) → invertiert: 100 − 25 = 75.0

T = 0.25 × 75.0 + 0.20 × 75.0 + 0.15 × 50.0 + 0.15 × 75.0
  + 0.15 × 50.0 + 0.10 × 75.0
  = 18.75 + 15.0 + 7.5 + 11.25 + 7.5 + 7.5
  = 67.5
```

---

## 7. Gesamt-Score: Vollständiges Worked Example

### Eingangsdaten (fiktive Person)

| Block | Item | Rohwerte | Score |
|-------|------|----------|-------|
| **A** | A1 | Ja (Werbung gesehen) | 100.0 |
| | A2 | Likert 4 (beschäftigt mich) | 75.0 |
| | A3 | Likert 3 (betrifft mich) | 50.0 |
| | A4 | Likert 3 (weiss um was es geht) | 50.0 |
| **W** | W1 | Likert 4 (persönliche Vorteile) | 75.0 |
| | W2 | Likert 4 (Gemeinwohl) | 75.0 |
| | W3 | Likert 3 (Werte) | 50.0 |
| | W4 | Likert 3 (Self-Efficacy) | 50.0 |
| | W5 | Likert 4 (Komplexität, hoch!) | 25.0 (invertiert) |
| | W6 | Likert 2 (wenige andere) | 25.0 |
| | A5 | Likert 4 (Umwelt-Bedeutsamkeit) | 75.0 |
| | T5 | Likert 3 (Umfeld: teils/teils) | 50.0 |
| **I** | INTRO4–8 | 1× Ja (INTRO7: Heizung erneuerbar, M3) | I_act = 20.0 |
| | INTRO9–13 | 1× Ja (INTRO13: Solar geplant, M4) | I_plan = 20.0 |
| | F2.12/I1/I2/F6.7 | Engagement mittel | I_engage = 68.0 |
| **T** | T0 | Ja (kennt ES) | Gate open |
| | T1–T4, T6, T7 | Siehe T-Beispiel | 67.5 |

### Berechnung Schritt für Schritt

```
Schritt 1: Dimensions-Scores berechnen

  A = 0.25 × 100 + 0.25 × 75 + 0.25 × 50 + 0.25 × 50
    = 25.0 + 18.75 + 12.5 + 12.5
    = 68.75

  W = 0.15×75 + 0.10×75 + 0.10×50 + 0.20×50
    + 0.20×25 + 0.10×25 + 0.10×75 + 0.05×50
    = 11.25 + 7.5 + 5.0 + 10.0 + 5.0 + 2.5 + 7.5 + 2.5
    = 51.25

  I = 0.45 × 20.0 + 0.30 × 20.0 + 0.25 × 68.0
    = 9.0 + 6.0 + 17.0
    = 32.0

  T = 67.5  (berechnet in Abschnitt 6)

Schritt 2: Gesamt-Score berechnen (Model B)

  G = 0.20 × 68.75 + 0.30 × 51.25 + 0.30 × 32.0 + 0.20 × 67.5
    = 13.75 + 15.375 + 9.6 + 13.5
    = 52.2

Schritt 3: Interpretation
  → G = 52.2 → «Zufriedenstellend» (gelb)
  → Stärkste Dimension: A = 68.75 (Awareness gut)
  → Schwächste Dimension: I = 32.0 (Impact — tatsächliche Handlung tief)
  → W-Diagnose: Self-Efficacy (W4=50) und Komplexität (W5 inv.=25) sind die Hebel
  → Handlungsempfehlung: Vereinfachungs-Interventionen (τ senken), Beratung stärken
```

---

## 8. Sonderfall: T0 = Nein (EnergieSchweiz unbekannt)

Wenn eine Person EnergieSchweiz nicht kennt, ist T nicht berechenbar. Zwei Optionen:

### Option A: G ohne T (empfohlen für Welle 1)

```
G_ohne_T = (0.20 × A + 0.30 × W + 0.30 × I) / 0.80

→ Gewichte werden auf die drei berechenbaren Dimensionen umverteilt.
→ Effektiv: A=0.25, W=0.375, I=0.375
```

### Option B: T-Default (für Folgewellen mit Referenz)

```
T_default = T_Mittelwert_bekannte_Personen

→ Personen ohne T erhalten den Mittelwert aller Personen MIT T-Score.
→ Konservative Annahme: Unbekanntes ES = durchschnittliches Vertrauen.
```

**Empfehlung:** In Welle 1 Option A, ab Welle 2 Option B mit dem Welle-1-Mittelwert als Default.

---

## 9. Segmentierung

Alle Scores werden nach folgenden Dimensionen segmentiert berechnet:

| Dimension | Ausprägungen | Quelle |
|-----------|-------------|--------|
| **Zeit** | Welle 1, Welle 2, Welle 3, Trend | Erhebungszeitpunkt |
| **Zielgruppe** | EFH, MFH, STWE, Alle | INTRO1 + INTRO3 |
| **Region** | Deutschschweiz, Romandie, Tessin, Gesamt | Demografie (PLZ) |
| **Altersgruppe** | 18–34, 35–54, 55–69, 70+ | Demografie |
| **Verhaltenssegment** | Überzeugte, Ratlose, Skeptiker, Verhinderer | Seg_A–D Items |
| **BCJ-Phase** | Unaware, Aware, Considering, Planning, Action, Advocacy | F2.12 |

### Berechnung pro Segment

```
G_segment = 0.20 × A_segment + 0.30 × W_segment + 0.30 × I_segment + 0.20 × T_segment

Wobei jeder Dimensions-Score der MITTELWERT über alle Personen im Segment ist.
```

---

## 10. Modulspezifische Berechnung

Die Komponenten I_act und I_plan werden zusätzlich **pro Modul** ausgewertet. Dies ergibt modulspezifische Impact-Scores.

### Modul-Impact-Score

```
I_Modul_m = 0.50 × (INTRO_m_done × 100) + 0.30 × (INTRO_m_plan_norm × 100) + 0.20 × I_engage
```

### Beispiel: Modul M3 (Heizungsersatz)

```
INTRO7 = Ja   → INTRO_M3_done = 1 → 100   (⚠️ M3 = INTRO7, nicht INTRO6!)
INTRO12 = Nein → INTRO_M3_plan = 0 → 0     (⚠️ M3 Plan = INTRO12, nicht INTRO11!)
I_engage = 68.0 (wie oben)

I_M3 = 0.50 × 100 + 0.30 × 0 + 0.20 × 68.0
     = 50.0 + 0 + 13.6
     = 63.6
```

---

## 11. Normalisierungsregeln (Zusammenfassung)

| Skala | Normalisierung auf [0, 100] | Formel |
|-------|----------------------------|--------|
| **Ja/Nein** | Ja=100, Nein=0 | `Score = Rohwert × 100` |
| **Ja/Nein/Unsicher** | Ja=100, Unsicher=50, Nein=0 | `Score = Rohwert × 100` |
| **Ja/Weiss nicht/Nein** | Ja=100, Weiss nicht=30, Nein=0 | `Score = Rohwert × 100` |
| **Ja/Geplant/Nein** | Ja=100, Geplant=50, Nein=0 | siehe Scoring-Tabelle |
| **Likert 1–5** | (Likert − 1) / 4 × 100 | ergibt 0, 25, 50, 75, 100 |
| **Likert 1–4** | (Likert − 1) / 3 × 100 | ergibt 0, 33, 67, 100 |
| **BCJ 6-Phasen** | Phase × 20 | 0, 20, 40, 60, 80, 100 |
| **Invertierte Items** | 100 − Score | W5, T7 |

---

## 12. Datenqualität

### Missing Values

| Regel | Beschreibung |
|-------|-------------|
| **Item-Level** | Fehlende Antwort → Item wird bei Gewichtung ausgeschlossen (Gewichte werden auf restliche Items umverteilt) |
| **Dimensions-Level** | Dimension nur berechenbar wenn ≥50% der Items beantwortet |
| **Gesamt-Level** | G berechenbar wenn mindestens A, W und I vorliegen (T kann fehlen, siehe Abschnitt 8) |
| **T-Gate** | T0=Nein → T nicht berechenbar → G nach Option A oder B |

### Beispiel: Missing in W-Block

```
W1=75, W2=MISSING, W3=50, W4=50, W5=25(inv.), W6=25, A5=75, T5=50

→ 7 von 8 Items beantwortet (≥50% → berechenbar)
→ W2-Gewicht (0.10) wird proportional auf restliche Items verteilt
→ Neue Gewichte: W1=0.167, W3=0.111, W4=0.222, W5=0.222, W6=0.111, A5=0.111, T5=0.056
```

### Ausschluss-Kriterien

| Kriterium | Aktion |
|-----------|--------|
| Abbruch vor Willingness-Block | Person ausschliessen (kein vollständiger Datensatz) |
| Straightlining (alle Likert-Items identisch) | Flaggen, im Bericht als Sensitivität zeigen |
| Speeders (<3 Min Gesamtzeit) | Flaggen, im Bericht als Sensitivität zeigen |

---

## 13. Dual-Layer-Auswertung (KPI + BCM)

### Layer 1: KPI-Score (für BFE-Dashboard)

Alle oben beschriebenen Formeln liefern die **KPI-Scores** für das Cockpit-Dashboard:

```
Dashboard-Output:
  A = 68.75  |  W = 51.25  |  I = 32.0  |  T = 67.5  |  G = 52.2
```

### Layer 2: BCM-Parameter (für Verhaltensmodell)

Dieselben Items liefern **zusätzlich** BCM-Parameter für das Verhaltensmodell:

| Item(s) | KPI-Score | BCM-Parameter | Transformation |
|---------|-----------|---------------|----------------|
| A1 | → A | A_exposure ∈ {0,1} | Binär |
| A2 | → A | A_salience ∈ [0,1] | (Likert−1)/4 |
| A5 | → W (reklassifiziert) | u_E ∈ [0,1] | (Likert−1)/4 |
| W1 | → W | u_F ∈ [0,1] | (Likert−1)/4 |
| W2 | → W | u_S ∈ [0,1] | (Likert−1)/4, ×0.7 SDB-Korrektur |
| W3 | → W | u_X ∈ [0,1] | (Likert−1)/4 |
| W4 | → W | θ_inv ∈ [0,1] | θ = 1 − (Likert−1)/4 |
| W5 | → W (invertiert) | τ ∈ [0,1] | (Likert−1)/4 (NICHT invertiert im BCM) |
| W6 | → W | σ_d ∈ [0,1] | (Likert−1)/4 |
| T1 | → T | Ψ_trust_source ∈ [0,1] | (Likert−1)/4 |
| T5 | → W (reklassifiziert) | σ_i ∈ [0,1] | (Likert−1)/4 |
| INTRO4–8 | → I | φ ∈ {acting, maintaining} | Pro Modul (M1=4, M5=5, M2=6, M3=7, M4=8) |
| INTRO9–13 | → I | φ ∈ {intending} | Pro Modul (M1=9, M5=10, M2=11, M3=12, M4=13) |
| F2.12 | → I | φ ∈ {0,...,5} | BCJ Phase direkt |
| F3.10 | nicht im BIS | β (Present Bias) | Choice-basiert |
| F4.9 | nicht im BIS | λ (Loss Aversion) | Choice-basiert |
| F5.1 | nicht im BIS | w_d (FEPSDE-Gewichte) | MaxDiff → relative Gewichte |

### Zusammenspiel

```
Fragebogen-Items
       │
       ├──→ Layer 1: KPI-Scores (A, W, I, T, G)  → Dashboard / BFE-Reporting
       │    ↳ Aggregation: Gewichtete Mittelwerte [0,100]
       │
       └──→ Layer 2: BCM-Parameter (β, λ, θ, σ, τ, u_d, Ψ)  → Verhaltensmodell
            ↳ Transformation: Item-spezifisch (siehe Tabelle oben)
```

Beide Layer nutzen dieselben Items, aber unterschiedliche Aggregationslogik. Der BCM-Layer erlaubt kausale Modellierung und Interventionsdesign.

---

## 14. Formel-Hierarchie (Zusammenfassung)

```
Level 3: Gesamt-Score
──────────────────────────────────────────────────────────────────────
  G = 0.20×A + 0.30×W + 0.30×I + 0.20×T


Level 2: Dimensions-Scores
──────────────────────────────────────────────────────────────────────
  A = 0.25×A1 + 0.25×A2 + 0.25×A3 + 0.25×A4

  W = 0.15×W1 + 0.10×W2 + 0.10×W3 + 0.20×W4
    + 0.20×(100−W5) + 0.10×W6 + 0.10×A5 + 0.05×T5

  I = 0.45×I_act + 0.30×I_plan + 0.25×I_engage

  T = 0.25×T1 + 0.20×T2 + 0.15×T3 + 0.15×T4 + 0.15×T6 + 0.10×(100−T7)
      (nur wenn T0 = Ja)


Level 1: Item-Scores (aus Fragebogen)
──────────────────────────────────────────────────────────────────────
  A1: Kampagnen-Awareness       → Ja/Nein/Unsicher → [0,100]
  A2: Salienz                   → Likert 1–5 → normiert → [0,100]
  A3: Persönliche Relevanz      → Likert 1–5 → normiert → [0,100]
  A4: Subjektives Wissen        → Likert 1–5 → normiert → [0,100]

  W1: Finanzielle Motivation    → Likert 1–5 → [0,100]
  W2: Prosoziale Motivation     → Likert 1–5 → [0,100]
  W3: Identitäts-Kongruenz      → Likert 1–5 → [0,100]
  W4: Self-Efficacy             → Likert 1–5 → [0,100]
  W5: Wahrgen. Komplexität      → Likert 1–5 → [0,100] ⚠️ INVERTIERT
  W6: Deskriptive Sozialnorm    → Likert 1–5 → [0,100]
  A5: Environmental Utility     → Likert 1–5 → [0,100] (aus A-Block reklassifiziert)
  T5: Injunktive Sozialnorm     → Likert 1–5 → [0,100] (aus T-Block reklassifiziert)

  I_act: Umgesetzte Massnahmen  → 5 Items (Ja/WN/Nein), WN=0 → Mittelwert → [0,100]
         M1=INTRO4, M2=INTRO6, M3=INTRO7, M4=INTRO8, M5=INTRO5
  I_plan: Geplante Massnahmen   → 5 Items (Ja/WN/Nein), WN=0.3 → Mittelwert → [0,100]
         M1=INTRO9, M2=INTRO11, M3=INTRO12, M4=INTRO13, M5=INTRO10
  I_engage: Engagement          → 4 Items gewichtet → [0,100]

  T1: Quell-Vertrauen           → Likert 1–5 → [0,100]
  T2: Glaubwürdigkeit           → Likert 1–5 → [0,100]
  T3: Transparenz               → Likert 1–5 → [0,100]
  T4: Autonomie                 → Likert 1–5 → [0,100]
  T6: Empfehlungs-Bereitschaft  → Likert 1–5 → [0,100]
  T7: Misstrauen                → Likert 1–5 → [0,100] ⚠️ INVERTIERT
```

---

## 15. Sensitivitätsanalyse (Gewichtsvariation)

Die Gewichte (0.20/0.30/0.30/0.20) basieren auf Model B. Um die Robustheit zu prüfen, werden folgende Szenarien berechnet:

| Szenario | w_A | w_W | w_I | w_T | Rationale |
|----------|-----|-----|-----|-----|-----------|
| **Model A (Gleich)** | 0.25 | 0.25 | 0.25 | 0.25 | Keine Priorisierung |
| **Model B (Basis)** | 0.20 | 0.30 | 0.30 | 0.20 | Progressionslogik ← empfohlen |
| **Model C (Impact)** | 0.15 | 0.25 | 0.40 | 0.20 | Handlung zählt stark |
| **v1.0 (Referenz)** | 0.25 | 0.25 | 0.30 | 0.20 | Vergleich mit kpi_architecture.yaml |

Die Sensitivitätsanalyse wird im Bericht als Robustheits-Check dokumentiert. Bei Baseline-Werten (A=35, W=30, I=15, T=65):

| Szenario | G (Baseline) |
|----------|-------------|
| Model A | 36.3 |
| Model B | **33.5** |
| Model C | 32.3 |
| v1.0 | 35.8 |

**Beobachtung:** Model B und C sind konservativer (tiefere Baseline), weil sie Impact stärker gewichten und Impact (15) der tiefste Wert ist. Das ist gewollt: Der BIS soll nicht durch hohe Awareness-Werte «geschönt» werden können.

---

## 16. Veränderungsmessung (Δ zwischen Wellen)

### Score-Δ pro Dimension (Reporting-Level B)

```
Δ_Dimension = Dimension_Welle2 − Dimension_Welle1

Beispiel:
  W_W1 = 45,  W_W2 = 52  →  ΔW = +7 Punkte
```

### Statistische Signifikanz

| n pro Welle | Detektierbares Δ (80% Power, α=0.05) | Interpretation |
|-------------|---------------------------------------|----------------|
| 150 | ≥ 8 Punkte | Grobe Veränderungen |
| 300 | ≥ 5 Punkte | Praxisrelevante Veränderungen |
| 900 (kumuliert) | ≥ 3 Punkte | Feine Veränderungen |

### Standardfehler für Proportionen

```
SE = √(p × (1−p) / n) × 100

Beispiel (n=300, p=0.50):
  SE = √(0.50 × 0.50 / 300) × 100 = ±2.89 PP
  95% KI: 50.0 ± 5.7 PP → [44.3, 55.7]
```

---

## 17. Änderungsprotokoll

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 2026-02-23 | Erstversion basierend auf kpi_architecture.yaml |
| 2.0 | 2026-02-23 | **Korrektur:** Namespace-Kollision W1/W2/W3 aufgelöst; Gewichte auf Model B (0.20/0.30/0.30/0.20) aktualisiert; W-Formel auf 8 tatsächliche Items umgebaut (W1–W6 + A5 + T5); I-Formel auf INTRO4–13 + F2.12 + Engagement-Items umgebaut; T-Score: T5 reklassifiziert (→W), T7 invertiert; Sonderfall T0=Nein dokumentiert |
| 2.1 | 2026-02-23 | **Kritische Korrektur INTRO→Modul-Mapping:** v2.0 nahm sequenzielle Zuordnung an (INTRO4=M1, INTRO5=M2, ...), aber die Nullmessung-SSOT (Intervista-Original) zeigt nicht-sequenzielles Mapping: INTRO4=M1, INTRO5=**M5**, INTRO6=**M2**, INTRO7=**M3**, INTRO8=**M4**. Gleiches Muster für INTRO9–13 (Planung). Antwortskalen korrigiert: ALLE INTRO-Items haben «Ja / Nein / Weiss nicht» (auch Bestand, nicht nur Planung). I_act-Scoring: «Weiss nicht» = 0 bei Bestand (konservativ). Worked Examples mit korrekten INTRO-Nummern aktualisiert. SSOT-Hierarchie: Nullmessung Intervista-Original als primäre Quelle. |

---

*Erstellt von FehrAdvice & Partners AG, 2026-02-23.*
*SSOT (primär): 260113_BFE_Nullmessung ECHfP_Fragebogen_Review intervista_sib.xlsx*
*SSOT (sekundär): fragebogen_parameter_analyse.yaml + fragebogen_tracking_v5_ebf.yaml*
