# MOD-TEL-001 v1.2 — A1 Telekom Austria: Youth Switching Model
## Vollintegrierter Report mit allen Primärdaten

**Session:** EBF-S-2026-02-20-ORG-001
**Report:** F3 (Finale Synthese)
**Datum:** 2026-02-20
**Modell-ID:** MOD-TEL-001 v1.2
**Validation Status:** `fully_calibrated_with_all_primary_data`

---

## Executive Summary

A1 Telekom Austria steht im Youth-Segment (18–29) vor einer strukturellen Herausforderung: Die «ATTACK»-Strategie (Verdoppelung der Net Adds) ist ambitioniert, aber die Primärdaten zeigen eine mehrdimensionale Lücke zwischen strategischer Absicht und Marktwahrnehmung. MOD-TEL-001 v1.2 integriert erstmals alle verfügbaren Primärdatenquellen zu einem kohärenten Verhaltensmodell und liefert konkrete, testbare Interventionsempfehlungen.

**Zentrale Befunde:**
1. **Conviction Gap, kein Awareness-Problem.** Xcite/bob wird in Fokusgruppen spontan nicht erwähnt — trotz 50% Awareness. Dies ist ein Überzeugungsproblem, das durch soziale Beweise und Loss-Frame-Messaging adressiert werden kann.
2. **Wien: Emotionale Unterlegenheit kostet 22–18 Prozentpunkte.** A1 erzielt bei «makes my life easier» nur 18%, Magenta 40% (+22pp). Ohne Intervention stagniert A1 Youth-Präferenz in Wien bei 19%.
3. **Internet NPS Youth: Kritische Verschlechterung.** Von -4.4 (Apr 2025) auf -11.5 (Okt 2025) — ein Warnsignal, das sofortiger Massnahmen bedarf.
4. **Loss Aversion bestätigt: λ = 2.1.** Die JTBD-Studie (n=2134) zeigt λ~2.0–2.5 für Abrechnungserlebnisse — konsistent mit dem Modellparameter.
5. **Pick-and-Swap löst JTBD «Flexibility»-Job.** Dieser Lever adressiert direkt die Crowding-Out-Problematik zwischen u_F und u_S (γ_FS = −0.35) und reduziert die Wechselangst.

---

## 1. Primärdaten-Übersicht (7 Quellen)

| # | Quelle | Typ | N | Datum | Schlüssel-Beitrag |
|---|--------|-----|---|-------|-------------------|
| 1 | Youth Concept Sinus Milieus | Segmentierungsstudie | Qual | 2024 | 3 Kern-Milieus, γ-Matrix-Justierung |
| 2 | Youth Zahlen AT | Marktdaten | Quant | 2024 | GfK 33.7% Marktanteil (tarif-basiert, <18 inkl.) |
| 3 | Focus Groups Urban Youth | Qualitativ | n=32 | Jan 2026 | Conviction Gap, 4 strategische Säulen |
| 4 | Jobs-to-be-Done ConsumerLifetime | Survey | n=2134 | 2025 | 5 Job-Dimensionen, λ=2.0–2.5 bestätigt |
| 5 | Urban Push Vienna Wave 1+2 | Tracking | n≈3000 | Apr+Okt 2025 | Wien-Marktanteile, NPS-Trend, Driver-Analyse |
| 6 | PRNPS Youth Strategy | Intern | — | 2025/2026 | ATTACK-Strategie, Net-Adds-Ambition, Pick-and-Swap |
| 7 | CVA YAML (mkt/cus/fin/ris/org/tec) | Intern | — | 2025 | Kundensegment-KPIs, Finanzstruktur, Marktkontext |

---

## 2. Modell-Spezifikation (MOD-TEL-001 v1.2)

### 2.1 Utility-Funktion (WHAT — 10C)

```
U_Youth = w_F · u_F + w_S · u_S + w_P · u_P + w_E · u_E
        + γ_FS · u_F · u_S + γ_PS · u_P · u_S + γ_SE · u_S · u_E
        + γ_FP · u_F · u_P
        - λ · max(L - V_expected, 0)
        + ε_idiosyncratic
```

**Dimensionen:**
| Dim | Bezeichnung | Gewicht (w) | Quelle |
|-----|-------------|-------------|--------|
| u_F | Financial/Preis-Fairness | 0.30 | JTBD «Sicherheit», Urban Push 70% Preis-Ablehnung |
| u_S | Soziale Identität / Brand-Fit | 0.28 | Focus Groups Sinus Milieu, BCM2 |
| u_P | Funktionale Performance | 0.24 | JTBD «Konnektivität», GfK |
| u_E | Hedonistisches Erleben | 0.18 | JTBD «Entertain & Relax», PRNPS |

### 2.2 Komplementarität (HOW — γ-Matrix)

| Paar | γ | Richtung | Quelle | Erklärung |
|------|---|----------|--------|-----------|
| γ_FS (u_F × u_S) | −0.35 | Crowding-Out | PAR-COMP-002 | Günstige Tarife beschädigen Premium-Identität |
| γ_PS (u_P × u_S) | +0.28 | Synergy | PAR-COMP-001 | Starkes Netz stärkt Brand-Credibility |
| γ_SE (u_S × u_E) | +0.22 | Synergy | PAR-COMP-004 | Gaming/Streaming als Social-Currency |
| γ_SE_kos (Kosmopoliten) | +0.35 | Verstärkte Synergie | Focus Groups | Identitäts-Markierung stärker bei Kosmopoliten |
| γ_FP (u_F × u_P) | +0.15 | Schwache Synergie | PAR-COMP | Preis-Fairness × Netz-Performance |

**Kritischer Hinweis γ_FS:** Pick-and-Swap (Sommer 2026) reduziert den Crowding-Out-Effekt, weil Flexibilität als separater Wert-Treiber positioniert wird (kein Preis-Discount, sondern Autonomie-Gewinn).

### 2.3 Verlust-Aversion (Prospect Theory)

| Parameter | Wert | Quelle | Kontext |
|-----------|------|--------|---------|
| λ (Verlustaversion) | 2.1 | JTBD (λ~2.0–2.5), BCM2 AT | Abrechnung, unerwartete Kosten |
| Referenzpunkt | V_expected = 0 | Modell-Annahme | Kein Zuschlag = kein Verlust |
| Wechselkosten (psychisch) | Ψ_I: hoch | Status-Quo-Bias 38% (JTBD) | 38% verbleiben aus Trägheit |

### 2.4 Kontext-Dimensionen (WHEN — Ψ)

| Ψ | Dimension | Wert AT | Quelle |
|---|-----------|---------|--------|
| Ψ_E | Preissensitivität | 0.82 | BCM2, Urban Push (70% Preis-Ablehnung) |
| Ψ_S | Soziale Normen (Peer-Einfluss) | 0.71 | Focus Groups, BCM2 |
| Ψ_K | Kultureller Kontext | AT-spezifisch | CVA mkt |
| Ψ_I | Regulatorischer Kontext | Telekommarkt AT | Niedrige Wechselbarrieren (EU-Richtlinie) |
| Wien-Verstärker | Urbaner Kontext | ×1.2 | Urban Push Driver-Analyse |

---

## 3. Marktsituation (Primärdaten-Synthese)

### 3.1 Kundensegment-KPIs (CVA — a1_cus.yaml)

| Segment | Abonnenten | Anteil | ARPU | Churn/Mo |
|---------|-----------|--------|------|----------|
| Youth (16–25) | 680k | 13% | €16.5 | 1.8% |
| Young Adults (26–35) | 1.04M | 20% | €28.5 | 1.4% |
| Familien | 1.56M | 30% | €45.0 | 1.0% |
| Senioren | 780k | 15% | €22.0 | 0.8% |
| Budget (bob/yesss!) | 620k | 12% | €12.0 | 2.2% |
| Prepaid (yesss!) | 780k | 15% | €8.5 | — |

**Kritische Beobachtung:** Senioren = 43% der A1-Basis (PRNPS). Die ATTACK-Strategie muss den Generationen-Mix aktiv steuern — Youth-Positionierung darf nicht die Senioren-Basis verprellen.

### 3.2 Wien-Marktdaten (Urban Push)

| Anbieter | Mobile-Marktanteil Wien | Internet-Marktanteil Wien |
|----------|------------------------|--------------------------|
| **A1** | **19%** | **23%** |
| Magenta | 23% | **47% (dominant)** |
| Drei | 26% | — |
| HoT | 13% | — |
| Spusu | 10% | — |

**Wien ist der härteste Markt.** A1 ist im mobilen Markt Wien Dritter (19%), im Internet sogar nur auf Platz 2 mit grossem Abstand. Youth-Präferenz sinkt von 23% (Apr) auf 19% (Okt 2025).

### 3.3 NPS-Entwicklung (Urban Push — Kritischer Trend)

| Segment | NPS Apr 2025 | NPS Okt 2025 | Delta | Status |
|---------|-------------|-------------|-------|--------|
| A1 Mobile (Youth) | −3.9 | −0.1 | +3.8 | Stabil |
| **A1 Internet (Youth)** | **−4.4** | **−11.5** | **−7.1** | **⚠ KRITISCH** |
| Magenta Youth Mobile | +12.8 | +26.8 | +14.0 | Stark wachsend |

**Interventionsbedarf NPS Internet:** −11.5 und fallend. Ohne Massnahme droht weiterer Verfall (Prediction P12).

---

## 4. Segmentierungsanalyse (Sinus Milieus + Focus Groups)

### 4.1 Drei Kern-Milieus (Strategischer Fokus)

| Milieu | A1-Relevanz | Key Insight | Empfohlene Botschaft |
|--------|-------------|-------------|----------------------|
| **Performer** | ★★★★★ | Netzqualität = Statussymbol; Verlässlichkeit nicht verhandelbar | «A1: Das Netz, das performt.» + Gaming Hub Aktivierung |
| **Kosmopolitische Individualisten** | ★★ → ★★★★ (Ziel) | Brand-Fit-Lücke; γ_SE=+0.35 (Social × Entertainment stärker); suchen Identität | «A1: Dein Netz, deine Welt.» + Youth Ambassador + Peer-Referral |
| **Adaptiv-Pragmatische Mitte** | ★★★ | Preis-Leistung; Familien-Empfehlung; Pick-and-Swap passt gut | «A1: Alles, was du brauchst. Ohne Schnickschnack.» |

### 4.2 Xcite Conviction Gap (Focus Groups → Modell)

```
Markt-Journey: Awareness (50%) → Consideration → Trial → Xcite Usage (13%)
                                    ↑___________________________________↑
                                         Conviction Gap = 37pp
                                    Focus Groups: Xcite/bob nicht erwähnt
                                    → Problem ist NICHT Bekanntheit
                                    → Problem ist ÜBERZEUGUNG
```

**Modellimplikation:** I3 (Loss-Frame + Peer-Referral) muss primär auf Überzeugungsbarriere zielen. Botschaft: «Andere in deinem Umfeld haben gewechselt und bereuen es nicht.» (Sozialer Beweis + Verlustaversion: λ=2.1 gegen Wechselzögerung)

---

## 5. JTBD-Mapping auf Utility-Dimensionen

| JTBD Job | Utility | Gewicht | A1-Performance | Gap |
|----------|---------|---------|----------------|-----|
| Konnektivität sichern | u_P | 0.24 | Gut (Netz) | Klein |
| Entertain & Relax | u_S + u_E | 0.18 | Mittel (kein Youth-Content) | Mittel |
| Sicherheit im Griff | u_F | 0.30 | Schlecht (Hidden Costs Angst) | Gross |
| Einfaches Management | u_P | 0.24 | Mittel (App-NPS) | Mittel |
| Flexibilität behalten | u_F | 0.30 | Schlecht (Lock-in-Wahrnehmung) | Gross |

**Kritischster Gap:** «Sicherheit im Griff» und «Flexibilität» — beide u_F-getrieben. Personal Support Gap = −25pp (JTBD). 82% bevorzugen menschlichen Kontakt → KI-Chatbot-Rollout für Youth nicht empfohlen.

---

## 6. Interventions-Empfehlungen (I1–I4, v1.2 Update)

### I1 — Sinus Milieu-spezifisches Branding
- **10C-Target:** u_S (WHO × WHAT)
- **Kanal:** TikTok, YouTube, Gaming Events, Youth Ambassador Programm
- **Botschaft pro Milieu:** Performer = Leistung/Status; Kosmopoliten = Identität/Weltoffen; Adaptiv-Pragmatisch = Einfachheit/Fairness
- **α (Phase Affinity):** 0.75 (Consideration → Decision)
- **Erwartete Wirkung:** +5–8pp Youth-Präferenz Wien (6M)

### I2 — App Self-Service Onboarding Redesign
- **10C-Target:** u_P (HOW — Einfaches Management)
- **JTBD-Basis:** Personal Support Gap −25pp; 35% bevorzugen App-Kanal
- **Massnahme:** Onboarding-Flow vereinfachen, FAQ proaktiv, Kosten-Dashboard sichtbar
- **Erwartete Wirkung:** +15pp JTBD «Einfaches Management» Zufriedenheit (P13)

### I3 — Loss-Frame + Peer-Referral für Xcite
- **10C-Target:** u_F × u_S (Crowding-Out minimieren durch sozialen Beweis)
- **Basis:** Conviction Gap 37pp; λ=2.1 gegen Wechselzögerung nutzbar
- **Botschaft:** «Deine Freunde sparen X€/Monat — du noch nicht.»
- **Erwartete Wirkung:** +10pp Xcite-Conversion (P4/P9); Xcite Usage 13% → 23%

### I4 — Pick-and-Swap Einführung (Sommer 2026)
- **10C-Target:** u_F (Flexibility) + γ_FS Crowding-Out reduzieren
- **PRNPS-Basis:** Key Lever in ATTACK-Strategie
- **JTBD-Basis:** «Flexibilität behalten» = kritischer Job; Status-Quo-Bias 38%
- **Erwartete Wirkung:** Youth Churn 1.8% → <1.4% (12M post-Launch, P14)

---

## 7. Testbare Prognosen (P1–P14)

### Bestehende Prognosen (v1.0/v1.1, P1–P10)

| ID | Statement | Test |
|----|-----------|------|
| P1 | GfK-Marktanteil real <33.7% (Altersfilter 18-29) | GfK Q2 2026 |
| P2 | Sinus Milieu-Tarif: +15% Conversion vs. Generik-Tarif | A/B-Test Q2 2026 |
| P3 | Streaming-Bundle: u_E +0.15 → Churn −8% | DWH 6M |
| P4 | Loss-Frame: +23% CTR auf Xcite-Landingpage | A/B-Test Q1 2026 |
| P5 | Gaming Hub Wien: +12% Youth Neuabschlüsse | DWH 3M |
| P6 | Pick-and-Swap Pilot: Churn −20% Kosmopoliten | DWH Q4 2026 |
| P7 | Social Proof Kampagne: Xcite Conversion +10pp | DWH H1 2026 |
| P8 | Bundle Preiserhöhung: Churn nur +0.2pp vs. erwartete 0.8pp | DWH |
| P9 | Xcite Conversion Gap 50→13% → Loss-Frame schliesst +10pp | DWH H1 2026 |
| P10 | Kosmopoliten: A1-Marktanteil 13% → 20% via Identitäts-Kampagne | Brand Monitor Q3 2026 |

### Neue Prognosen (v1.2, P11–P14)

| ID | Statement | Basis | Test |
|----|-----------|-------|------|
| P11 | Wien: A1 Youth-Präferenz stagniert bei 19% ohne Emotionskampagne | Magenta +22pp «makes life easier» | Urban Push Wave 3 Q2 2026 |
| P12 | A1 Internet-NPS Youth <−15 (Q2 2026) ohne Eingriff | −11.5 (Okt 2025), fallend | Urban Push Wave 3 |
| P13 | App-Redesign: JTBD «Einfaches Management» +15pp | JTBD Gap −25pp | App NPS pre/post |
| P14 | Pick-and-Swap: Youth Churn 1.8% → <1.4% (12M) | JTBD Flexibility + γ_FS | DWH Kohorte |

---

## 8. Risiken und Limitationen

| Risiko | Schwere | Massnahme |
|--------|---------|-----------|
| γ_FS Crowding-Out bleibt ohne Pick-and-Swap | Hoch | Pick-and-Swap Priorisierung (Sommer 2026) |
| GfK-Daten tarif-basiert, <18 inkl. | Mittel | Altersfilter-Anfrage an GfK Q2 2026 |
| Internet NPS Wien kritisch fallend | Hoch | Sofort-Massnahme Internet-Service Q1 2026 |
| Senioren-Basis (43%) vs. Youth-Positionierung | Mittel | Dual-Brand Architektur A1 ↔ yesss!/bob |
| Wien ≠ AT-Gesamt | Mittel | Separate Modelle Wien vs. Österreich-gesamt |
| KI-Chatbot-Rollout schadet Youth-Erfahrung | Mittel | 82% Menschenpräferenz beachten (JTBD) |

---

## 9. Nächste Schritte

| Priorität | Massnahme | Deadline | Owner |
|-----------|-----------|----------|-------|
| 🔴 P0 | A1 Internet Wien Youth: Sofort-Analyse und Ursachen-Deep-Dive | Q1 2026 | A1 Service/NPS Team |
| 🔴 P0 | BEATRIX POC: 3 Sinus Milieu Image Propositions testen | Feb 2026 | FehrAdvice + A1 Marketing |
| 🟠 P1 | Loss-Frame A/B-Test Xcite-Landingpage (P4/P9) | Q1 2026 | A1 Digital |
| 🟠 P1 | /design-intervention I1–I3 Rollout-Plan mit Milieu-Targeting | Q1 2026 | FehrAdvice |
| 🟡 P2 | Urban Push Wave 3 (P11+P12 testen) | Q2 2026 | A1 Research |
| 🟡 P2 | Pick-and-Swap Launch-Tracking-Setup | vor Sommer 2026 | A1 Produkt |
| 🟢 P3 | MOD-TEL-001 v1.3: GfK Q2 2026 Daten (Altersfilter 18–29) | Q3 2026 | FehrAdvice |

---

## 10. Datenbank-Updates (v1.2)

- **model-registry.yaml** — MOD-TEL-001 v1.2 aktualisiert: `fully_calibrated_with_all_primary_data`
  - Neue Sektionen: `qualitative_validation`, `urban_push_vienna`, `jtbd_framework`, `prnps_youth_strategy`, `predictions_v12`, `jugendstudie_at_2024`
- **Folge-Updates ausstehend:**
  - `intervention-registry.yaml` — I1–I4 formalisieren
  - `case-registry.yaml` — A1 Youth als Case
  - `output-registry.yaml` — diesen Report registrieren

---

## Anhang: Datenquellen (Alle 7)

1. **Sinus Milieu Youth Concept AT 2024** — Segmentierungsstudie, Sinus Institut, AT 2024
2. **Youth Zahlen AT 2024** — GfK Marktdaten (Hinweis: tarif-basiert, <18 inkl., Altersfilter ausstehend)
3. **Präs Focus Groups Urban Youth_ohne Video.pdf** — Integral Marktforschung, Wien, Jan 20–22, 2026, n=32
4. **Jobs2beDone_ConsumerLifetime_FINAL_2025.pdf** — n=2134, AT 2025
5. **Urban Push Vienna Wave 1 (Apr 2025) + Wave 2 (Okt 2025)** — Market Research, n≈3000
6. **PRNPS Youth.pptx** — A1 Telekom Austria, interne Strategiepräsentation, 2025/2026
7. **CVA YAML Dateien** — a1_mkt, a1_cus, a1_fin, a1_ris, a1_org, a1_tec — FehrAdvice, 2025

---

*MOD-TEL-001 v1.2 | EBF-S-2026-02-20-ORG-001 | FehrAdvice & Partners AG*
*Nächste Review: Juli 2026 | Nächste Version: v1.3 (GfK Q2 2026 + Urban Push Wave 3)*
