# Erste Hypothesen aus dem Zielvariablen-Modell

> **Internes Arbeitsdokument** | FehrAdvice & Partners AG | 19. Februar 2026
> Projekt: IVO002 | Kunde: Industriellenvereinigung Oberösterreich
> Status: Educated Guesses – Validierung durch Messung ausstehend

---

## 1. Zielvariablen-Modell (Kurzübersicht)

### Top-KPI

**Y_top: Unterstützungsbereitschaft (Willingness to Support)**
Operationalisierung: «Wie wahrscheinlich ist es, dass Sie die IV OÖ bei ihren Vorhaben unterstützen?» (Skala 1–10)

### Drei Nutzen-Dimensionen (Level 2)

| Dimension | Operationalisierung | β-Gewicht |
|-----------|-------------------|:---------:|
| D1: Individueller Nutzen | «Ich ziehe persönliche Vorteile daraus, wenn ich die IV OÖ unterstütze» | 0.30 |
| D2: Kollektiver Nutzen | «Mein Umfeld zieht Vorteile daraus, wenn ich die IV OÖ unterstütze» | 0.30 |
| D3: Identitätsnutzen | «Die IV OÖ zu unterstützen, passt zu meinem Selbstbild» | 0.40 |

**Regressionsmodell:** Y_top = 0.30 × D1 + 0.30 × D2 + 0.40 × D3

### 15 Treiber-Faktoren (Level 3) mit Diagnostik

| ID | Faktor | w | V | B | Beitrag | Diagnostik |
|----|--------|:---:|:---:|:---:|:---:|------------|
| **3A.1** | **Einkommenssicherheit** | **0.30** | 0.65 | 0.45 | 0.088 | Awareness Gap |
| **3A.2** | **Arbeitsplatzsicherheit** | **0.30** | 0.65 | 0.55 | 0.107 | Awareness Gap |
| 3A.3 | Karrierechancen | 0.15 | 0.70 | 0.30 | 0.032 | Awareness Gap |
| 3A.4 | Arbeitserleichterung KI | 0.10 | 0.30 | 0.25 | 0.008 | Blinder Fleck |
| 3A.5 | Kompetenzentwicklung | 0.15 | 0.55 | 0.25 | 0.021 | Blinder Fleck |
| **3B.1** | **Regionale Arbeitsplätze** | **0.30** | 0.90 | 0.70 | 0.189 | Stärke |
| 3B.2 | Wohlstand in OÖ | 0.25 | 0.80 | 0.45 | 0.090 | Awareness Gap |
| **3B.3** | **Stabilität Sozialsystem** | **0.25** | **0.85** | **0.20** | 0.043 | **Awareness Gap ★** |
| 3B.4 | Bildung & Ausbildung | 0.10 | 0.65 | 0.35 | 0.023 | Awareness Gap |
| 3B.5 | Standort-Wettbewerbsfähigkeit | 0.10 | 0.45 | 0.15 | 0.007 | Blinder Fleck |
| 3C.1 | Werteübereinstimmung | 0.20 | 0.50 | 0.20 | 0.020 | Blinder Fleck |
| **3C.2** | **Stolz auf Industrieregion** | **0.30** | 0.90 | 0.55 | 0.149 | Stärke |
| 3C.3 | Innovationsidentität | 0.20 | 0.55 | 0.25 | 0.028 | Blinder Fleck |
| 3C.4 | Zugehörigkeitsgefühl | 0.10 | 0.35 | 0.15 | 0.005 | Blinder Fleck |
| 3C.5 | Verantwortung für Zukunft | 0.20 | 0.65 | 0.15 | 0.020 | Awareness Gap |

**Legende:**
- **w** = Gewichtung (Relevanz für die Bevölkerung)
- **V** = Anreiz vorhanden (Ist der Nutzen real gegeben?)
- **B** = Anreiz bekannt (Weiss die Bevölkerung davon?)
- **Beitrag** = w × V × B (effektiver Beitrag zur Dimension)

---

## 2. Diagnostik-Matrix

```
                           Anreiz BEKANNT
                     HOCH                  TIEF
                ┌──────────────────┬──────────────────┐
  Anreiz        │                  │                  │
  vorhanden     │   STÄRKE         │  AWARENESS GAP   │
  HOCH          │   (verstärken)   │  (Narrativ kann  │
                │                  │   es lösen)       │
                │  3B.1 Jobs       │  3B.3 Sozial ★★★ │
                │  3C.2 Stolz      │  3B.2 Wohlstand  │
                │  3A.2 Jobsicher. │  3A.3 Karriere   │
                │                  │  3C.5 Verantwort.│
                │                  │  3C.3 Innovation │
                ├──────────────────┼──────────────────┤
  Anreiz        │                  │                  │
  vorhanden     │  REALITY GAP     │  BLINDER FLECK   │
  TIEF          │  (Industrie muss │  (erst aufbauen,  │
                │   erst handeln)  │   dann komm.)     │
                │                  │                  │
                │  (keiner)        │  3A.4 KI-Erleich.│
                │                  │  3C.4 Zugehörigk.│
                │                  │  3B.5 Standort   │
                │                  │  3C.1 Werte      │
                └──────────────────┴──────────────────┘
```

**Kernbefund:** Kein einziger Reality Gap mit hoher Bekanntheit – die Bevölkerung «weiss» nicht, wo etwas fehlt. Das ist strategisch günstig. Dafür gibt es 6+ klare Awareness Gaps, wo Narrative direkt wirken können.

---

## 3. Hypothesen

### Kategorie A: Werttreiber-Hypothesen

Diese Hypothesen betreffen, **welche Faktoren für die Bevölkerung am wichtigsten sind**.

> **H-W1: Arbeitsplatz dominiert**
> Arbeitsplatzsicherheit (individuell: 3A.2 + kollektiv: 3B.1) ist der stärkste Einzeltreiber für Unterstützungsbereitschaft – stärker als Innovation, KI oder Nachhaltigkeit.
>
> *Messbar über:* Regressionsgewichte D1/D2 → Y_top, Faktorgewichte 3A.2 und 3B.1

> **H-W2: Stolz schlägt Werte**
> Identifikation über «Stolz auf die Industrieregion» (3C.2) ist wirksamer als über «gemeinsame Werte» (3C.1) oder «Zugehörigkeit zur Industriegemeinschaft» (3C.4).
>
> *Messbar über:* Vergleich der Faktorladungen 3C.2 vs. 3C.1 vs. 3C.4 auf D3

> **H-W3: Konkret schlägt abstrakt**
> Die Bevölkerung bewertet konkrete, persönlich erfahrbare Faktoren (Einkommen, Jobs) systematisch höher als abstrakte Konzepte (Standort, Wettbewerb, Innovation).
>
> *Messbar über:* Ranking der Faktorgewichte; Korrelation «Abstraktionsgrad» × «Gewicht»

---

### Kategorie B: Narrativ-Hypothesen (Awareness Gaps)

Diese Hypothesen betreffen, **welche Narrative den grössten Einstellungsshift erzeugen**.

> **H-N1: Sozialsystem-Narrativ als grösster Hebel ★★★**
> Das Narrativ «Starke Industrie sichert deine Pension» (3B.3) erzeugt den grössten Einstellungsshift aller getesteten Narrative – weil es den grössten Awareness Gap (V=0.85, B=0.20, Gap=0.65) schliesst und ein emotional aufgeladenes Thema adressiert (69% besorgt über Gesundheits-/Pflegesystem).
>
> *Testbar über:* A/B-Experiment; Kontrollgruppe vs. Sozialsystem-Narrativ; Messung von D2 und Y_top

> **H-N2: Stolz-Aktivierung als Identitätshebel**
> Das Narrativ «OÖ-Industrie: Europas Innovationsregion Nr. 1» (3C.2 + 3C.3) erhöht die Identifikation stärker als «Die IV OÖ vertritt deine Werte» (3C.1) – weil Stolz bereits latent vorhanden ist (V=0.90) und nur aktiviert werden muss.
>
> *Testbar über:* A/B-Experiment; Stolz-Narrativ vs. Werte-Narrativ; Messung von D3

> **H-N3: Karriere-Narrativ wirkt bei Gen Z überproportional**
> Karriere-Narrative («Industrie = Aufstiegschance», 3A.3) wirken bei Gen Z (16–25) überproportional stark, weil der Awareness Gap in dieser Gruppe am grössten ist (Image-Problem «rauchender Schlot» × hohe Karriereorientierung).
>
> *Testbar über:* Interaktionseffekt Narrativ × Alter; Subgruppenanalyse Gen Z

> **H-N4: Wohlstand braucht Konkretisierung**
> «Wohlstand durch Industrie» (3B.2) wirkt stärker, wenn es über konkrete Beispiele (Kaufkraft, Infrastruktur in OÖ) vermittelt wird, als über abstrakte Wirtschaftszahlen – weil die Attribution «Industrie → mein Wohlstand» heute fehlt (B=0.45).
>
> *Testbar über:* A/B-Experiment; abstraktes vs. konkretes Wohlstands-Narrativ

> **H-N5: Verantwortung wirkt nur bei positiv Eingestellten**
> «Die Zukunft OÖs mitgestalten» (3C.5) resoniert primär bei bereits positiv eingestellten Segmenten (Enthusiasten, Offene), nicht bei Skeptikern – weil Verantwortungsübernahme eine hohe Grundidentifikation voraussetzt (Interaktion D3 × 3C.5).
>
> *Testbar über:* Moderationsanalyse; Wirkung des Verantwortungs-Narrativs je Baseline-Identifikation

---

### Kategorie C: Reality-Gap-Hypothesen (Grenzen der Narrative)

Diese Hypothesen betreffen Faktoren, **wo Narrative allein nicht ausreichen**.

> **H-R1: KI-Arbeitserleichterung ist (noch) nicht narrativ vermittelbar**
> KI-Narrative, die auf «persönliche Arbeitserleichterung» (3A.4) setzen, scheitern in der breiten Bevölkerung – weil die Erfahrung fehlt (V=0.30). Sie wirken nur bei KI-affinen Segmenten (Gen Z: 59% wollen KI nutzen), die bereits eigene Erfahrung haben.
>
> *Testbar über:* Interaktionseffekt KI-Narrativ × KI-Erfahrung (Moderator)
>
> *Implikation:* KI-Kommunikation erst nach konkreten Anwendungsfällen in OÖ-Betrieben

> **H-R2: Zugehörigkeit ist kein Massenhebel**
> «Zugehörigkeit zur Industriegemeinschaft» (3C.4) ist kein wirksamer Identitätshebel für die breite Bevölkerung (V=0.35) – Stolz (3C.2) und Verantwortung (3C.5) sind stärkere Identitäts-Anker, weil sie keine Gruppenmitgliedschaft voraussetzen.
>
> *Testbar über:* Vergleich der Effektstärken 3C.2 vs. 3C.4 vs. 3C.5

> **H-R3: Werte-Spannung bei Work-Life-Balance-Orientierten**
> Wo die IV OÖ «Leistung und Eigenverantwortung» kommuniziert (3C.1), erzeugt dies bei Work-Life-Balance-orientierten Segmenten (v.a. Gen Z) aktiven Widerstand – das Narrativ muss diese Spannung auflösen, nicht ignorieren.
>
> *Testbar über:* Subgruppenanalyse; negative Effekte des Leistungs-Narrativs bei WLB-Segmenten
>
> *Implikation:* Leistungs-Narrativ als «Selbstbestimmung» framen, nicht als «Mehrarbeit»

> **H-R4: Standortwettbewerb ist kein Bevölkerungsargument**
> «Standortwettbewerbsfähigkeit» (3B.5) ist kein bevölkerungstaugliches Argument (V=0.45, B=0.15, w=0.10). Es funktioniert nur in der Stakeholder-Kommunikation (Politik, Wirtschaft), nicht in der breiten Öffentlichkeit.
>
> *Testbar über:* Effektstärke des Standort-Narrativs in der Gesamtpopulation vs. Teilstichprobe «politisch Interessierte»

---

## 4. Priorisierung für das Experiment

### Top-3 Narrative zum Testen (höchstes Wirkungspotenzial)

| Prio | Narrativ | Faktor | Gap | w | Erwartete Wirkung |
|:----:|----------|--------|:---:|:---:|-------------------|
| 1 | «Industrie sichert dein Sozialsystem» | 3B.3 | 0.65 | 0.25 | Grösster Awareness Gap × hohe Gewichtung × emotional aufgeladen |
| 2 | «Stolz auf Industrieregion OÖ» verstärken | 3C.2 | 0.35 | 0.30 | Höchste Identitäts-Gewichtung × bereits latent vorhanden |
| 3 | «Industrie = Karrierechance» (v.a. Gen Z) | 3A.3 | 0.40 | 0.15 | Grösster Image-Gap × strategisch wichtigste Zielgruppe |

### Kontrolle / Gegenprobe

| Test | Hypothese | Erwartung |
|------|-----------|-----------|
| KI-Arbeitserleichterung (3A.4) | H-R1 | Kein signifikanter Effekt in der Gesamtpopulation |
| Standort-Wettbewerb (3B.5) | H-R4 | Kein signifikanter Effekt in der Gesamtpopulation |
| Leistung bei Gen Z (3C.1) | H-R3 | Negativer Effekt bei WLB-orientierten Subgruppen |

### Warnungen

1. **Kein Narrativ auf 3A.4 (KI-Arbeitserleichterung) ohne reale Beispiele** – Glaubwürdigkeitsverlust, wenn die Erfahrung fehlt
2. **3C.1 (Werteübereinstimmung) ist ein Minenfeld** – Leistungsframing kann bei WLB-Segmenten kontraproduktiv wirken
3. **Awareness allein reicht nicht** – Aus dem EBF: Awareness-Erhöhung ohne Handlungspfad kann Unsicherheit steigern (β = +0.351)

---

## 5. Nächste Schritte

- [ ] Hypothesen im Strategischen Sounding (3. März 2026) mit IV OÖ diskutieren
- [ ] Priorisierung der Narrative für das Experiment gemeinsam festlegen
- [ ] Operationalisierung der Messung: Items für V und B pro Faktor entwickeln
- [ ] Experimentaldesign: A/B/C-Gruppen für Top-3 Narrative definieren
- [ ] Kontrollvariablen bestimmen (Alter, Beruf, KI-Erfahrung, Industrienähe)

---

## Anhang: Methodik

### Datengrundlage der Educated Guesses

| Quelle | Beitrag |
|--------|---------|
| IV OÖ-Beziehungsstudie 2019 | Baseline Identifikation, Treiber «Zukunft» und «Arbeitgeber» stark, «Umwelt» und «Fairness» schwach |
| IMAS-Umfrage KI 2025 | 99% KI-Bekanntheit, 75% sehen Industrie-Chancen, 57% KI-Strategie wichtig |
| KI-Exzellenzstrategie 2025 | 40 Vorschläge, RCI Rang 19, Fokus Bildung/Forschung/Arbeitsmarkt |
| Kick-Off-Protokoll 11.02.2026 | Zielbild Wohlstand, Widerstandsfähigkeit, Leistung; «Produktivität» zu abstrakt |
| Bevölkerungsdaten OÖ | 71% Inflationssorge, 69% Gesundheitssystem-Sorge, 64% Zuwanderung, Gen Z: 86% zufrieden, 59% KI-affin |
| EBF / 10C CORE Framework | AWARE × READY Diagnostik, BCJ-Stufen, SRG-Referenz (Identity β=0.715), Loss Aversion λ=2.5 |

### Formellogik

```
Level 3 → Level 2:  D_i = Σ(w_j × V_j × B_j)  für j = 1..5
Level 2 → Level 1:  Y_top = β₁×D1 + β₂×D2 + β₃×D3
Diagnostik:          IF V>0.6 AND B>0.6 → Stärke
                     IF V>0.6 AND B≤0.4 → Awareness Gap
                     IF V≤0.4 AND B>0.6 → Reality Gap
                     ELSE → Blinder Fleck
```

---

*Erstellt: 19. Februar 2026 | FehrAdvice & Partners AG | Projekt IVO002*
