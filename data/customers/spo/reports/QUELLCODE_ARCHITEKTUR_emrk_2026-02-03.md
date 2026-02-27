# EBF-Quellcode-Architektur: SPÖ EMRK-Strategie

**Version:** 1.0
**Datum:** 2026-02-03
**Session-ID:** REV-EMRK-I1-001

---

## Executive Summary

Dieses Dokument analysiert die **Quellcode-Architektur** der vier SPÖ EMRK-Strategie-Dokumente:
1. TAKTIK (v3.1)
2. WORDING (v5.1)
3. BRIEFING (v4.1)
4. EMRK_STRATEGIE_KOMPLETT (v1.4)

Es zeigt, **woher die Analysen kommen**, welche **Beliefs und Axiome** dahinterstehen, und wie diese durch das EBF-Framework **operationalisiert** werden.

---

## 1. Die Quellcode-Hierarchie

```
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 0: EBF WISSENSCHAFTLICHE THEORIEN (Primärquellen)               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  CAT-05: Identity & Beliefs (12 Theorien)                        │   │
│  │  ├── MS-IB-001: Identity Economics (Akerlof/Kranton 2000)       │   │
│  │  │   → U_IDN > 0: Gruppenidentität formt Nutzen                 │   │
│  │  ├── MS-IB-008: Social Identity (Tajfel/Turner 1979)            │   │
│  │  │   → In-group/Out-group Dynamik                               │   │
│  │  ├── MS-IB-003: Motivated Reasoning (Kunda 1990)                │   │
│  │  │   → Beliefs folgen Wünschen, nicht umgekehrt                 │   │
│  │  └── MS-IB-012: Narrative Economics (Shiller 2017)              │   │
│  │      → Narrative sind «ansteckend» und ökonomisch wirksam       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  CAT-21: Political Psychology & Authoritarianism (5 Theorien)   │   │
│  │  ├── MS-PP-001: Right-Wing Authoritarianism (Altemeyer 1981)    │   │
│  │  │   → RWA-Prejudice r = 0.50-0.60                              │   │
│  │  ├── MS-PP-002: Social Dominance Orientation (Sidanius 1999)    │   │
│  │  │   → SDO-Hierarchy: Zero-Sum-Denken                           │   │
│  │  ├── MS-PP-003: Conspiracy Mentality (Imhoff/Bruder 2014)       │   │
│  │  │   → AT: 47% «Great Replacement»-Glaube (DÖW 2024)            │   │
│  │  ├── MS-PP-004: Populism Theory (Mudde/Kaltwasser 2017)         │   │
│  │  │   → «Reines Volk vs. korrupte Elite»                         │   │
│  │  └── MS-PP-005: Generalized Prejudice (Asbrock et al. 2010)     │   │
│  │      → RWA + SDO erklären generalisierte Vorurteile             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 1: KERN-BELIEFS (Fundamentale Annahmen)                          │
│                                                                         │
│  B1: Identität dominiert Rationalität                                   │
│      Quelle: MS-IB-001, MS-PP-001                                       │
│      → Bei politischen Entscheidungen gilt: U_IDN >> U_IND             │
│                                                                         │
│  B2: Populismus ist strukturell (nicht inhaltlich)                      │
│      Quelle: MS-PP-004                                                  │
│      → «Volk vs. Elite» ist FORM, nicht INHALT                         │
│                                                                         │
│  B3: Medien-Anreize erzwingen Spaltung                                 │
│      Quelle: Boulevard-Theorem (eigene Ableitung)                       │
│      → max π(c) ⟹ max E(c) · S(c) → Spaltung ist profitabel           │
│                                                                         │
│  B4: Ordnung ist universeller Wert                                      │
│      Quelle: Moral Foundations Theory, Conservation values              │
│      → «Ordnung» spricht ALLE an, «Härte» nur Autoritäre               │
│                                                                         │
│  B5: Komplementarität erzeugt Synergie                                  │
│      Quelle: EBF-Kerntheorie (Appendix B)                              │
│      → W(A+B) > W(A) + W(B) bei komplementären Strategien              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 2: AXIOME (K1-K10) - Formalisierte Entscheidungsregeln          │
│  Quelle: AXIOME_ordnung_statt_spalten.yaml v1.7                        │
│                                                                         │
│  K1: KICKL-DIFFERENZIERUNG                                             │
│      ∀ k ∈ K: f_K(k) > f_B(k) ⟹ k ∉ S_B                               │
│      → NIEMALS auf Kickls Terrain konkurrieren                         │
│      Belief-Basis: B1, B2                                               │
│                                                                         │
│  K2: ZAHLEN ALS BELEG                                                  │
│      Zahlen = Beweis, nicht Botschaft                                   │
│      → Emotionale Wirkung durch Framing, Fakten durch Zahlen           │
│      Belief-Basis: B4 (Ordnung durch Fakten)                           │
│                                                                         │
│  K3: ORDNUNG-FRAME                                                     │
│      Frame(Policy) = «Ordnung schaffen» ≠ «Härte zeigen»               │
│      → Universell statt partikular                                     │
│      Belief-Basis: B4 (Ordnung ist universell)                         │
│                                                                         │
│  K4: USP-PFLICHT                                                       │
│      ∀ Argument A: ∃ USP(A) = Alleinstellungsmerkmal SPÖ              │
│      → Warum nur SPÖ das kann (vs. FPÖ/ÖVP)                           │
│      Belief-Basis: B1 (Differenzierung nötig)                          │
│                                                                         │
│  K5: EMRK-WÜRDIGUNG                                                    │
│      EMRK = Schutzschild, nicht Hindernis                              │
│      → Narrativ-Umkehrung                                              │
│      Belief-Basis: B2 (Framing vor Fakten)                             │
│                                                                         │
│  K6: GEGNER-MOTIVE                                                     │
│      FPÖ-Ziel = Allmacht, nicht Problemlösung                          │
│      → EMRK-Ausstieg = Kontrollverlust für Bürger                     │
│      Belief-Basis: B2 (Populismus entlarven)                           │
│                                                                         │
│  K7: WEITERENTWICKLUNG                                                 │
│      SPÖ = Fortschritt, FPÖ = Rückschritt                              │
│      → EU-Zukunft vs. Isolation                                        │
│      Belief-Basis: B4 (Ordnung durch Entwicklung)                      │
│                                                                         │
│  K8: LEVEL-KOMPLEMENTARITÄT (META-STRUKTUR)                            │
│      W(L1+L2+L3) > W(L1) + W(L2) + W(L3)                               │
│      ├── L1: Policy = BEWEISEN (das THEMA ordnen)                     │
│      ├── L2: Kommunikation = FRAMEN (die DEBATTE ordnen)              │
│      └── L3: Werte = BEDEUTEN (das LAND ordnen)                       │
│      Belief-Basis: B5 (Komplementarität)                               │
│                                                                         │
│  K9: POPULÄR STATT POPULISTISCH                                        │
│      Populär = breite Zustimmung                                       │
│      Populistisch = «Volk vs. Elite»-Spaltung                         │
│      → SPÖ kann populär sein ohne populistisch                        │
│      Belief-Basis: B2 (Populismus = Struktur)                          │
│                                                                         │
│  K10: DREI NUTZEN-EBENEN (META-AXIOM)                                  │
│       U = w₁·U_IND + w₂·U_COLL + w₃·U_IDN                             │
│       ├── U_IND: «Was bringt mir das?» (individuell)                  │
│       ├── U_COLL: «Was bringt uns das?» (kollektiv)                   │
│       └── U_IDN: «Wer bin ich?» (Identität)                           │
│       → SPÖ: U_IND + U_COLL stark, U_IDN schwach vs. FPÖ             │
│       Belief-Basis: B1 (Identität dominiert)                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 3: KONTEXT-FAKTOREN (Ψ-Dimensionen)                             │
│  Quelle: AXIOME_ordnung_statt_spalten.yaml + BCM2-Kontextdatenbank     │
│                                                                         │
│  Ψ_C (Kognitiv): C3_MIXED                                              │
│      → Zielgruppe nutzt System 1 UND System 2                          │
│      → Implikation: Einfache Botschaften + faktenbasierte Tiefe       │
│                                                                         │
│  Ψ_F (Medial): F4_BOULEVARD_THEOREM                                    │
│      → Bezahl-Boulevard ≡ Spalt-Boulevard                              │
│      → Implikation: Presseförderung-Argument nutzen                   │
│                                                                         │
│  Ψ_E (Ökonomisch): E3_ASYMMETRY                                        │
│      → FPÖ-nahe Medien dominieren numerisch                           │
│      → Implikation: Qualität vor Quantität, virales Potenzial         │
│                                                                         │
│  Ψ_M (Material): M3_HYBRID                                             │
│      → TV + Social Media + Print mischen                               │
│      → Implikation: Multi-Channel-Strategie                           │
│                                                                         │
│  AWARE-Faktor: Manipulations-Bewusstsein                               │
│      → Wähler sind manipulierbar, aber misstrauen Manipulation        │
│      → Implikation: FPÖ-Methoden entlarven                            │
│                                                                         │
│  READY-Faktor: Veränderungsbereitschaft                                │
│      → 64% unzufrieden mit Status quo (Eurobarometer 2025)            │
│      → Implikation: «Ordnung» als Veränderungsangebot framen         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  EBENE 4: OPERATIONALISIERUNG → DOKUMENTE                              │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  STRATEGIE-ENTSCHEIDUNGEN (EMRK_STRATEGIE_KOMPLETT v1.4)        │   │
│  │                                                                  │   │
│  │  Entscheidung S1: Ordnungs-Frame statt Härte-Frame              │   │
│  │  ├── Axiom-Basis: K3, K9                                        │   │
│  │  ├── Belief-Basis: B4                                           │   │
│  │  └── Theorie: Moral Foundations (universelle Werte)             │   │
│  │                                                                  │   │
│  │  Entscheidung S2: Drei-Level-Architektur                        │   │
│  │  ├── Axiom-Basis: K8                                            │   │
│  │  ├── Belief-Basis: B5                                           │   │
│  │  └── Theorie: Complementarity (EBF Appendix B)                  │   │
│  │                                                                  │   │
│  │  Entscheidung S3: USP-Fokus (Staatsmännisch)                    │   │
│  │  ├── Axiom-Basis: K1, K4                                        │   │
│  │  ├── Belief-Basis: B1                                           │   │
│  │  └── Theorie: Differentiation, Identity Economics               │   │
│  │                                                                  │   │
│  │  Entscheidung S4: EMRK-Weiterentwicklung                        │   │
│  │  ├── Axiom-Basis: K5, K7                                        │   │
│  │  ├── Belief-Basis: B4                                           │   │
│  │  └── Theorie: Progress Narrative                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  TAKTIK-ENTSCHEIDUNGEN (TAKTIK v3.1)                            │   │
│  │                                                                  │   │
│  │  Entscheidung T1: Tonalitäts-Transformation                     │   │
│  │  ├── Defensiv → Offensiv                                        │   │
│  │  ├── Axiom-Basis: K1 (Terrain wechseln)                         │   │
│  │  └── Beispiel: «Wir verteidigen» → «Wir schaffen Ordnung»      │   │
│  │                                                                  │   │
│  │  Entscheidung T2: FPÖ-Entlarvung                                │   │
│  │  ├── Methode: Fragen stellen, nicht anklagen                   │   │
│  │  ├── Axiom-Basis: K6 (Gegner-Motive offenlegen)                │   │
│  │  └── Beispiel: «Warum braucht Kickl diese Macht?»              │   │
│  │                                                                  │   │
│  │  Entscheidung T3: Zahlen-Einsatz                                │   │
│  │  ├── 800 Tage = Beleg, nicht Botschaft                         │   │
│  │  ├── Axiom-Basis: K2                                            │   │
│  │  └── Format: «In 800 Tagen haben wir X erreicht»               │   │
│  │                                                                  │   │
│  │  Entscheidung T4: Level-spezifische Argumentation               │   │
│  │  ├── L1 (Policy): Konkrete Massnahmen mit Zahlen               │   │
│  │  ├── L2 (Framing): Ordnungs-Narrative                          │   │
│  │  └── L3 (Werte): Österreichs Zukunft in Europa                 │   │
│  │      Axiom-Basis: K8 (Komplementarität)                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  KOMMUNIKATIONS-ELEMENTE (WORDING v5.1 + BRIEFING v4.1)         │   │
│  │                                                                  │   │
│  │  Element K1: Haupt-Botschaft                                    │   │
│  │  «Wir schaffen Ordnung. Ohne Chaos. Ohne EMRK-Ausstieg.»       │   │
│  │  ├── Level: L3 (Werte)                                          │   │
│  │  ├── Axiom: K3, K8                                              │   │
│  │  └── USP: Ordnung OHNE Isolation                                │   │
│  │                                                                  │   │
│  │  Element K2: Zahlen-Beweis                                      │   │
│  │  «52.000 Abschiebungen. 800 Tage. 40% mehr.»                   │   │
│  │  ├── Level: L1 (Policy)                                         │   │
│  │  ├── Axiom: K2                                                  │   │
│  │  └── Funktion: Fakten, nicht Emotionen                         │   │
│  │                                                                  │   │
│  │  Element K3: Gegner-Frage                                       │   │
│  │  «Warum braucht Kickl die Macht, ohne Kontrolle?»              │   │
│  │  ├── Level: L2 (Framing)                                        │   │
│  │  ├── Axiom: K6                                                  │   │
│  │  └── Mechanismus: Zweifel säen, nicht anklagen                 │   │
│  │                                                                  │   │
│  │  Element K4: USP-Statement                                      │   │
│  │  «Nur die SPÖ kann beides: Ordnung UND Rechtsstaat.»           │   │
│  │  ├── Level: L1 + L3                                             │   │
│  │  ├── Axiom: K4                                                  │   │
│  │  └── Differenzierung: vs. FPÖ (nur «Härte»)                    │   │
│  │                                                                  │   │
│  │  Element K5: Zukunfts-Vision                                    │   │
│  │  «Österreich in Europa. Modern. Souverän. Ordentlich.»         │   │
│  │  ├── Level: L3 (Werte)                                          │   │
│  │  ├── Axiom: K7                                                  │   │
│  │  └── Kontrast: vs. Isolation/Rückschritt                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Belief → Axiom → Operationalisierung: Vollständiges Mapping

### 2.1 Belief B1: Identität dominiert Rationalität

| Theorie-Quelle | Axiome | Strategie | Taktik | Kommunikation |
|----------------|--------|-----------|--------|---------------|
| MS-IB-001 (Identity Economics) | K1, K10 | S3: USP-Fokus | T1: Tonalitäts-Transformation | K4: USP-Statement |
| MS-PP-001 (RWA) | K6 | - | T2: FPÖ-Entlarvung | K3: Gegner-Frage |
| MS-IB-008 (Social Identity) | K10 | S1: Ordnungs-Frame | - | K1: Haupt-Botschaft |

**Operationalisierungs-Kette:**
```
Identität dominiert (B1)
    ↓
Kickl hat Identitäts-Vorteil bei «Härte» (Analyse)
    ↓
K1: Nicht auf Kickls Terrain konkurrieren (Axiom)
    ↓
S3: USP = «Staatsmännisch» statt «Hart» (Strategie)
    ↓
T1: Defensive → Offensive Tonalität (Taktik)
    ↓
K4: «Nur SPÖ kann Ordnung UND Rechtsstaat» (Kommunikation)
```

### 2.2 Belief B2: Populismus ist strukturell

| Theorie-Quelle | Axiome | Strategie | Taktik | Kommunikation |
|----------------|--------|-----------|--------|---------------|
| MS-PP-004 (Populism Theory) | K5, K6, K9 | - | T2: FPÖ-Entlarvung | K3: Gegner-Frage |
| MS-PP-003 (Conspiracy Mentality) | K6 | - | T2 | K3 |

**Operationalisierungs-Kette:**
```
Populismus = Struktur, nicht Inhalt (B2)
    ↓
FPÖ nutzt «Volk vs. Elite»-Struktur (Analyse)
    ↓
K9: Populär sein OHNE populistisch (Axiom)
    ↓
K6: FPÖ-Motive entlarven (Axiom)
    ↓
T2: Fragen stellen, nicht anklagen (Taktik)
    ↓
K3: «Warum braucht Kickl diese Macht?» (Kommunikation)
```

### 2.3 Belief B3: Medien-Anreize erzwingen Spaltung

| Theorie-Quelle | Axiome | Strategie | Taktik | Kommunikation |
|----------------|--------|-----------|--------|---------------|
| Boulevard-Theorem (Ψ_F) | - | Presseförderungs-Argument | Medien-Diversifikation | Multi-Channel |

**Operationalisierungs-Kette:**
```
max π(c) ⟹ max E(c) · S(c) (B3)
    ↓
Boulevard MUSS spalten für Profit (Analyse)
    ↓
Ψ_F: F4_BOULEVARD_THEOREM (Kontext)
    ↓
Presseförderung an Qualitätskriterien binden (Policy-Idee)
    ↓
Multi-Channel: Qualitätsmedien + Social Media (Taktik)
```

### 2.4 Belief B4: Ordnung ist universeller Wert

| Theorie-Quelle | Axiome | Strategie | Taktik | Kommunikation |
|----------------|--------|-----------|--------|---------------|
| Moral Foundations Theory | K3, K7 | S1: Ordnungs-Frame | T4: Level-Argumentation | K1, K5 |
| Conservation Values | K3 | S1 | - | K1 |

**Operationalisierungs-Kette:**
```
«Ordnung» spricht alle an, «Härte» nur Autoritäre (B4)
    ↓
85% wollen «Ordnung», nur 35% wollen «Härte» (Analyse)
    ↓
K3: Ordnung-Frame statt Härte-Frame (Axiom)
    ↓
S1: Strategie = «Ordnung schaffen» (Strategie)
    ↓
T4: Alle 3 Levels mit Ordnungs-Narrativ (Taktik)
    ↓
K1: «Wir schaffen Ordnung. Ohne Chaos.» (Kommunikation)
```

### 2.5 Belief B5: Komplementarität erzeugt Synergie

| Theorie-Quelle | Axiome | Strategie | Taktik | Kommunikation |
|----------------|--------|-----------|--------|---------------|
| EBF Appendix B (γ-Matrix) | K8 | S2: Drei-Level-Architektur | T4: Level-spezifisch | K1-K5 kombiniert |

**Operationalisierungs-Kette:**
```
W(A+B) > W(A) + W(B) bei Komplementarität (B5)
    ↓
Policy allein ≠ Wirkung (Analyse)
    ↓
K8: L1+L2+L3 > L1+L2+L3 einzeln (Axiom)
    ↓
S2: Drei-Level-Architektur (Strategie)
    ↓
T4: Jede Aussage auf richtigem Level (Taktik)
    ↓
K1-K5: Integriertes Message-Set (Kommunikation)
```

---

## 3. Die Drei-Level-Architektur im Detail

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEVEL 1: Das THEMA ordnen (Policy = BEWEISEN)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WAS:     Konkrete Massnahmen mit messbaren Ergebnissen                │
│  WIE:     Zahlen, Fakten, Vergleiche                                   │
│  AXIOME:  K2 (Zahlen als Beleg)                                        │
│  NUTZEN:  U_IND + U_COLL (individuell + kollektiv)                     │
│                                                                         │
│  BEISPIELE:                                                             │
│  • 52.000 Abschiebungen in 800 Tagen                                   │
│  • 40% mehr als Vorgängerregierung                                     │
│  • Rückführungsabkommen mit 5 Ländern                                  │
│  • 800 Tage Regierungsarbeit dokumentiert                              │
│                                                                         │
│  DOKUMENT-QUELLE:                                                       │
│  → WORDING v5.1: Schritte 1-7 (Policy-Beweise)                        │
│  → BRIEFING v4.1: Zahlen-Fakten Sektion                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  LEVEL 2: Die DEBATTE ordnen (Kommunikation = FRAMEN)                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WAS:     Die Diskussion auf SPÖ-Terrain bringen                       │
│  WIE:     Reframing, Gegner-Entlarvung, Fragen                        │
│  AXIOME:  K1 (Differenzierung), K3 (Ordnung-Frame), K6 (Motive)       │
│  NUTZEN:  Reduziert gegnerischen U_IDN-Vorteil                         │
│                                                                         │
│  BEISPIELE:                                                             │
│  • «Ordnung» statt «Härte» als Frame                                   │
│  • «Warum braucht Kickl diese Macht?» (Frage)                         │
│  • «Wer profitiert vom EMRK-Ausstieg?» (Entlarvung)                   │
│  • «Staatsmännisch» statt «Populistisch» (Selbstbild)                 │
│                                                                         │
│  DOKUMENT-QUELLE:                                                       │
│  → TAKTIK v3.1: Tonalitäts-Transformation                             │
│  → WORDING v5.1: Schritte 8-14 (Framing-Elemente)                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  LEVEL 3: Das LAND ordnen (Werte = BEDEUTEN)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WAS:     Grössere Bedeutung, Zukunftsvision                          │
│  WIE:     Narrative, Identität, Zugehörigkeit                          │
│  AXIOME:  K7 (Weiterentwicklung), K8 (Komplementarität), K10 (Nutzen) │
│  NUTZEN:  U_IDN (Identität: «Wer sind wir als Österreicher?»)         │
│                                                                         │
│  BEISPIELE:                                                             │
│  • «Österreich in Europa. Modern. Souverän. Ordentlich.»              │
│  • «Ordnung vs. Chaos» als Grundentscheidung                          │
│  • «Rechtsstaat ist österreichische Tradition»                        │
│  • «Zukunft vs. Rückschritt»                                          │
│                                                                         │
│  DOKUMENT-QUELLE:                                                       │
│  → WORDING v5.1: Schritte 15-19 (Werte-Ebene)                         │
│  → EMRK_STRATEGIE: Vision-Sektion                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Dokument-zu-Quelle Mapping

| Dokument | Primär-Quelle | Axiome | Kontext | Theorien |
|----------|---------------|--------|---------|----------|
| **EMRK_STRATEGIE** | K8, K10 | Alle K1-K10 | Alle Ψ | CAT-05, CAT-21 |
| **TAKTIK v3.1** | K1, K3, K6 | K1-K6, K9 | Ψ_C, Ψ_F | MS-PP-001, MS-PP-004 |
| **WORDING v5.1** | K2, K3, K8 | K2, K3, K4, K5, K8 | Ψ_C | MS-IB-001, MS-IB-012 |
| **BRIEFING v4.1** | K1, K2, K4 | K1-K6 | Ψ_F, Ψ_M | MS-PP-004 |

---

## 5. Validierungs-Checkliste (aus AXIOME v1.7)

Jede Kommunikation muss folgende Checks bestehen:

| Check | Regel | Dokument-Compliance |
|-------|-------|---------------------|
| CHK-1 | Kickl-Differenzierung | ✅ Kein Härte-Wettbewerb |
| CHK-2 | Zahlen = Beleg | ✅ 52.000, 800, 40% |
| CHK-3 | Ordnung-Frame | ✅ «Ordnung» durchgehend |
| CHK-4 | USP vorhanden | ✅ «Nur SPÖ kann beides» |
| CHK-5 | EMRK-Würdigung | ✅ Schutzschild-Narrativ |
| CHK-6 | Gegner-Motive | ✅ Allmachts-Entlarvung |
| CHK-7 | Weiterentwicklung | ✅ Zukunft vs. Rückschritt |
| CHK-8 | Level-Balance | ✅ L1+L2+L3 alle vertreten |
| CHK-9 | Populär ≠ Populistisch | ✅ Keine «Volk vs. Elite» |
| CHK-10 | Drei Nutzen-Ebenen | ✅ U_IND, U_COLL, U_IDN |
| CHK-11 | Tonalität Offensiv | ✅ «Wir schaffen» nicht «Wir verteidigen» |

---

## 6. Zusammenfassung: Die Quellcode-Architektur

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  QUELLCODE-ARCHITEKTUR: SPÖ EMRK-STRATEGIE                             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  WISSENSCHAFT (EBF Theory Catalog)                               │   │
│  │  CAT-05: Identity & Beliefs │ CAT-21: Political Psychology       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                         │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  BELIEFS (5 Kern-Annahmen)                                       │   │
│  │  B1: Identität > Rationalität │ B2: Populismus = Struktur       │   │
│  │  B3: Medien-Anreize → Spaltung │ B4: Ordnung = universell       │   │
│  │  B5: Komplementarität = Synergie                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                         │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  AXIOME (10 formalisierte Regeln)                               │   │
│  │  AXIOME_ordnung_statt_spalten.yaml v1.7                         │   │
│  │  K1-K10: Entscheidungsregeln mit formaler Notation              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                         │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  KONTEXT (Ψ-Dimensionen)                                        │   │
│  │  Ψ_C: Kognitiv │ Ψ_F: Medial │ Ψ_E: Ökonomisch │ Ψ_M: Material │   │
│  │  + AWARE + READY Faktoren                                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                         │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  OPERATIONALISIERUNG                                             │   │
│  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐          │   │
│  │  │ STRATEGIE     │ │ TAKTIK        │ │ KOMMUNIKATION │          │   │
│  │  │ (S1-S4)       │ │ (T1-T4)       │ │ (K1-K5)       │          │   │
│  │  └───────────────┘ └───────────────┘ └───────────────┘          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                         │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  DOKUMENTE (4 Deliverables)                                      │   │
│  │  ├── EMRK_STRATEGIE_KOMPLETT v1.4  (Vollständige Strategie)    │   │
│  │  ├── TAKTIK v3.1                    (Operative Umsetzung)      │   │
│  │  ├── WORDING v5.1                   (19-Schritte-Argumentar)   │   │
│  │  └── BRIEFING v4.1                  (Schnellreferenz)          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Referenzen

### 7.1 EBF-Quellen
- **AXIOME_ordnung_statt_spalten.yaml** v1.7 - Axiom-System
- **spo_profile.yaml** v1.0.0 - Kundenprofil
- **theory-catalog.yaml** - Wissenschaftliche Theorien
- **model-registry.yaml** - EBF-Modelle

### 7.2 Wissenschaftliche Theorien
- Akerlof, G. & Kranton, R. (2000). Economics and Identity. QJE.
- Altemeyer, B. (1981). Right-Wing Authoritarianism.
- Mudde, C. & Kaltwasser, C.R. (2017). Populism: A Very Short Introduction.
- Tajfel, H. & Turner, J.C. (1979). An Integrative Theory of Intergroup Conflict.

### 7.3 Österreich-Daten
- DÖW (2024). Rechtsextremismus-Bericht.
- IFES (2022). Antisemitismus-Studie.
- Eurobarometer (2025). Österreich-Werte.

---

*Erstellt: 2026-02-03 | EBF Model: MOD-POL-001 | Session: REV-EMRK-I1-001*
