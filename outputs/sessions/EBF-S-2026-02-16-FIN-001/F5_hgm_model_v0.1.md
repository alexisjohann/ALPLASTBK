# Hauptbank-Gravitationsmodell (HGM v0.1)

**Session:** EBF-S-2026-02-16-FIN-001
**Kunde:** UBS Key Club
**Erstellt:** 2026-02-16
**Status:** v0.1 (Prototyp — Kalibrierung mit echten Daten ausstehend)

---

## 1. Modellformel

```
P(Hauptbank) = σ( Σᵢ gᵢ·wᵢ + Σᵢⱼ γᵢⱼ·gᵢ·gⱼ - SQ )

Wo:
  P(Hauptbank) = Wahrscheinlichkeit, dass Kundin Hauptbank-Status erreicht
  gᵢ           = Gravitationskraft (Lock-in) von Produkt i ∈ [0, 1]
  wᵢ           = Alltags-Gewicht (Touchpoint-Frequenz) von Produkt i ∈ [0, 1]
  γᵢⱼ          = Komplementarität zwischen Produkt i und j ∈ [-1, +1]
  SQ            = Status Quo Bias (Trägheit, zu überwinden)
  σ(·)          = Sigmoid-Funktion: σ(x) = 1 / (1 + e^(-x))
```

---

## 2. Produkt-Gravitationskarte

| Produkt | g (Lock-in) | w (Alltags-Gewicht) | g × w (Gravitation) | Tier | Quelle |
|---------|-------------|---------------------|---------------------|------|--------|
| Lohnkonto/Zahlungsverkehr | 0.90 | 0.95 | **0.855** | T1 | Samuelson & Zeckhauser 1988 |
| Hypothek | 0.95 | 0.30 | 0.285 | T1 | Samuelson & Zeckhauser 1988 |
| Kreditkarte | 0.35 | 0.80 | 0.280 | T2 | LLMMC (Anker: empirische Switching-Daten) |
| 3. Säule (3a/3b) | 0.60 | 0.15 | 0.090 | T2 | LLMMC (Anker: CH Steuersystem) |
| Vorsorge (2. Säule) | 0.70 | 0.10 | 0.070 | T2 | LLMMC |
| Advisory/Vermögen | 0.50 | 0.20 | 0.100 | T2 | Bereits bei UBS (Key Club) |

### Parameterbegründungen

**g (Lock-in):**
- g = 0.95 (Hypothek): 5-10 Jahre Vertragsbindung, höchste Wechselkosten
- g = 0.90 (Lohnkonto): Daueraufträge, LSV, Arbeitgeber-Meldung, psychologischer Anker
- g = 0.70 (2. Säule): Arbeitgeber-gebunden, selten gewechselt
- g = 0.60 (3a): Jährliche Entscheidung, aber Steuer-Lock-in
- g = 0.50 (Advisory): Performance-abhängig, wechselbar
- g = 0.35 (Kreditkarte): Leicht kündbar, niedrige Bindung

**w (Alltags-Gewicht):**
- w = 0.95 (Lohnkonto): Tägliche Nutzung (E-Banking, Überweisungen, Zahlungen)
- w = 0.80 (Kreditkarte): Tägliche Nutzung (Zahlungen, Online-Shopping)
- w = 0.30 (Hypothek): Monatliche Zahlung, sonst unsichtbar
- w = 0.20 (Advisory): Quartalsweise Gespräche, Performance-Check
- w = 0.15 (3a): Jährliche Einzahlung, Steuererklärung
- w = 0.10 (2. Säule): Kaum aktive Interaktion

---

## 3. Komplementaritäts-Matrix

| | Lohn | Hypo | 3a | Karte | Vorsorge | Advisory |
|------|------|------|------|-------|----------|----------|
| **Lohn** | — | +0.5 | +0.3 | +0.4 | +0.2 | +0.1 |
| **Hypo** | +0.5 | — | **+0.6** | +0.1 | +0.3 | +0.2 |
| **3a** | +0.3 | **+0.6** | — | +0.0 | +0.4 | +0.3 |
| **Karte** | +0.4 | +0.1 | +0.0 | — | +0.0 | +0.1 |
| **Vorsorge** | +0.2 | +0.3 | +0.4 | +0.0 | — | +0.3 |
| **Advisory** | +0.1 | +0.2 | +0.3 | +0.1 | +0.3 | — |

### Komplementaritäts-Begründungen

| Paar | γ | Begründung | Tier |
|------|---|-----------|------|
| Hypo × 3a | +0.6 | Steuer-Synergie: 3a-Amortisation der Hypothek. Doppelter Nutzen (weniger Schuldzinsen + Steuervorteil) | T1 (CH Steuerrecht) |
| Lohn × Hypo | +0.5 | Convenience: Amortisation/Zinszahlung automatisch. «Alles aus einer Hand» | T2 (LLMMC) |
| Lohn × Karte | +0.4 | Identitäts-Shift: Tägliche Nutzung beider → «Das ist MEINE Bank für alles Tägliche» | T2 (Akerlof & Kranton 2000) |
| 3a × Vorsorge | +0.4 | Vorsorge-Cluster: Gesamtvorsorge-Beratung als Paket | T2 (LLMMC) |
| Lohn × 3a | +0.3 | Einzahlung direkt vom Lohnkonto, automatisierbar | T2 (LLMMC) |
| Hypo × Vorsorge | +0.3 | Vorbezug/Verpfändung 2. Säule für Wohneigentum | T1 (CH Vorsorgerecht) |

---

## 4. Verhaltens-Mauern (Barrieren)

| Mauer | Stärke | SQ-Beitrag | Mechanismus | Quelle |
|-------|--------|-----------|-------------|--------|
| **Status Quo Bias** | ████░ (0.8) | 1.80 | λ ≈ 2.25 → Wechselkosten 2.25× überschätzt | Samuelson & Zeckhauser (1988), Kahneman & Tversky (1979) |
| **Mental Accounting** | ███░░ (0.6) | 0.60 | «UBS = Anlagen, KB = Alltag» — mentale Trennung | Thaler (1985, 1999) |
| **Verlust-Angst** | ██░░░ (0.4) | 0.40 | Endowment Effect auf bestehende Bankbeziehung | Kahneman, Knetsch & Thaler (1991) |
| **Identität** | ██░░░ (0.4) | 0.40 | «Ich bin KB-Kundin» → Identitäts-Wechselkosten | Akerlof & Kranton (2000) |
| **TOTAL SQ** | | **3.20** | | |

---

## 5. Sequenz-Strategien

### Sequenz A: Alltags-Pfad (ohne Life Event)

```
Karte (T=0) → [3-6 Monate] → Lohn (T=1) → [sofort] → 3a (T=2) → [bei Erneuerung] → Hypo (T=3)
```

| Schritt | Produkt | Behavioral Mechanism | Intervention | ΔSQ |
|---------|---------|---------------------|--------------|-----|
| 1 | Kreditkarte | Identity Priming (Akerlof & Kranton) | Exklusive Key Club Card, Status-Signal | -0.40 |
| 2 | Lohnkonto | Hassle Reduction (Thaler & Sunstein) | «Wir erledigen ALLES für Sie» Wechselservice | -1.20 |
| 3 | 3. Säule | Loss Framing (Kahneman & Tversky) | «Sie verschenken CHF X Steuerersparnis» | -0.30 |
| 4 | Hypothek | Natural Moment (Erneuerung) | Gesamtbeziehungs-Kondition + Steuer-Synergie | -0.80 |

**Geschätzte Conversion:** P(Hauptbank | Sequenz A) ≈ 0.15-0.25

### Sequenz B: Life-Event-Pfad (mit Life Event)

```
Life Event → Hypo (natürlich) → Lohn (sofort) → 3a (Jahresende) → Karte (beiläufig)
```

**Trigger-Events:**
- Immobilienkauf / Hypothekar-Erneuerung
- Heirat / Scheidung
- Geburt eines Kindes
- Jobwechsel / Beförderung / Grosser Bonus
- Erbschaft / Schenkung
- Pensionierung (Kapitalbezug 2. Säule)

**Schlüssel-Insight:** Bei Life Events sinkt SQ von λ ≈ 2.25 auf λ ≈ 1.3 (Status Quo bereits gebrochen).

**Geschätzte Conversion:** P(Hauptbank | Sequenz B) ≈ 0.45-0.65

---

## 6. Crowding-Out Warnung

```
γ(finanzieller Bonus × Vertrauensbeziehung) = -0.68
Quelle: PAR-COMP-002, Frey & Jegen (2001), Deci, Koestner & Ryan (1999)
```

**VERBOTEN:**
- ❌ CHF-Bonus für Lohnkonto-Wechsel
- ❌ Prozent-Rabatt auf Hypothek bei Gesamtbeziehung
- ❌ Gratis-Kreditkarte als Wechselanreiz

**STATTDESSEN:**
- ✅ Exklusivität (Events, Services nur für Hauptbankkund:innen)
- ✅ Convenience (Wechselservice, Hassle-Reduktion)
- ✅ Steueroptimierung (Loss Frame auf bestehende Verluste)
- ✅ Social Proof («73% unserer Key-Club-Mitglieder haben Hauptbank bei uns»)

---

## 7. Kalibrierungsbedarf

Für HGM v1.0 werden folgende Daten benötigt:

| Datenpunkt | Beschreibung | Zweck |
|-----------|--------------|-------|
| Produkt-Penetration | % Key-Club-Kund:innen mit Lohn/Hypo/3a/Karte bei UBS | IST-Gravitation berechnen |
| Hauptbank-Quote | Aktuelle Quote + Ziel-Quote | SQ-Parameter kalibrieren |
| Life-Event-Daten | Hypo-Erneuerungen, Pensionierungen (12-24 Monate) | Sequenz-B-Opportunitäten quantifizieren |

---

## 8. Modell-Metadaten

| Feld | Wert |
|------|------|
| **Modell-ID** | HGM-UBS-001 |
| **Version** | v0.1 (Prototyp) |
| **Session** | EBF-S-2026-02-16-FIN-001 |
| **Kunde** | UBS Key Club |
| **Domain** | FIN (Banking, Wealth Management) |
| **10C-Dimensionen** | WHO (HNWI Key Club), WHAT (Finanzprodukte, Identität), HOW (Komplementarität), WHEN (Life Events, Timing), AWARE (Status Quo Awareness), READY (Switching Readiness), STAGE (Customer Journey) |
| **Theorien** | Prospect Theory (MS-RD-001), Mental Accounting (MS-RD-003), Identity Economics (MS-IB-001), Status Quo Bias (Samuelson & Zeckhauser), Motivation Crowding (Frey & Jegen) |
| **Parameter-Quellen** | PAR-COMP-002 (Crowding-Out), Tier 1 (Prospect Theory), Tier 2 (LLMMC für g, w, γ) |
| **Falsifizierbarkeit** | P(Hauptbank\|Seq A) ≈ 0.20, P(Hauptbank\|Seq B) ≈ 0.55, P(Hauptbank\|Bonus) ≈ 0.12 |
| **Nächster Schritt** | Kalibrierung mit echten UBS-Daten |

---

*Erstellt: 2026-02-16 | HGM v0.1 | EBF-S-2026-02-16-FIN-001*
