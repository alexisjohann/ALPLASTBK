# FA-SM-2.0: Organizational Design Layer

> Erweiterung des FA-SM-2.0 um die fehlende Verbindung:
> **Wie erzeugt Organisationsstruktur S die Value Dimensions V?**

## Kontext: Warum dieser Layer?

Das bestehende FA-SM-2.0 definiert:
- **Layer 0:** Value Dimensions V (was die Organisation produziert)
- **Layer 1:** Verhalten B (wie Actor Groups agieren)
- **Layer 2:** Kontext Ψ (was Verhalten beeinflusst)

Was **fehlte:** Die konkreten Stellschrauben der Organisationsgestaltung — die Struktur S, die V produziert und Ψ formt. Ohne S ist das Modell deskriptiv (beschreibt was passiert) aber nicht preskriptiv (empfiehlt was zu tun ist).

```
VORHER:   V ← B ← Ψ         "Was passiert?"
NACHHER:  V ← f(S, Ψ) ← B   "Was sollen wir ÄNDERN?"
                ↑
            Org-Design-Layer (NEU)
```

## 1. Structure Dimensions S

Fünf Stellschrauben der Organisationsgestaltung, jeweils auf [0,1]:

| Symbol | Name | Frage | 0 = | 1 = |
|--------|------|-------|-----|-----|
| s₁ | Formalisierung | Wie viel ist schriftlich geregelt? | Nichts geregelt | Alles dokumentiert |
| s₂ | Zentralisierung | Wo werden Entscheide getroffen? | Komplett dezentral | Alles bei GL |
| s₃ | Spezialisierung | Wie eng sind Rollen definiert? | Generalisten | Spezialisten |
| s₄ | Koordination | Wie wird horizontal abgestimmt? | Keine Abstimmung | Intensive Vernetzung |
| s₅ | Delegation | Wie viel Autonomie haben MA? | Keine Autonomie | Volle Autonomie |

**Anmerkungen:**
- s₄ = **horizontale** Koordination (zwischen Abteilungen/Teams). Vertikale Koordination ist weitgehend durch s₂ (Zentralisierung) abgedeckt.
- s₂ und s₅ sind konzeptionell verwandt aber nicht redundant: s₂ = wo Entscheide formal liegen, s₅ = wie viel Spielraum in der Ausführung besteht.

## 2. Value Dimensions (aktualisiert)

Umbenennung V_OC → V_RE basierend auf Perspektiven-Stress-Test:

| Symbol | Name | Definition |
|--------|------|-----------|
| **V_RE** | **Operative Verlässlichkeit** | Grad, zu dem die Organisation vorhersagbar, konsistent und klar funktioniert. Umfasst Prozess-Zuverlässigkeit, Rollen-Klarheit, Standard-Einhaltung, Vorhersagbarkeit. |
| V_RC | Beziehungskapital | Vertrauen, Loyalität, Netzwerkqualität intern und extern |
| V_AC | Anpassungsfähigkeit | Fähigkeit UND Geschwindigkeit, auf Veränderungen zu reagieren |
| V_IC | Innovationskapazität | Fähigkeit zu erneuern — umfasst sowohl radikale Innovation als auch kontinuierliche Verbesserung (Kaizen) |
| V_WTP | Zahlungsbereitschaft | Abgeleitet aus V_RE, V_RC, V_AC, V_IC (siehe Section 4) |
| V_WTS | Talent Value | Bereits in FA-SM-2.0 definiert, bleibt unverändert |

### Warum V_OC → V_RE?

Entdeckt durch Perspektiven-Stress-Test (siehe Section 6):
- B_L meint "Verlässlichkeit" wenn sie V_OC hört
- B_O meint "Klarheit" wenn sie V_OC hört
- Beide meinen NICHT "Kontrolle" im Sinn von Überwachung

"Operative Verlässlichkeit" deckt beides ab und eliminiert die negative Konnotation.

## 3. Production Functions

### Funktionale Form

Additiv mit abnehmenden Grenzerträgen (EXC-1 konform):

```
V_d(S, Ψ) = Σ_i [ β_di(Ψ) · s_i  −  κ_di · s_i² ]
```

Wobei:
- **β_di(Ψ)** = Grenzertrag von Struktur-Dimension i für Value d — kontextabhängig via PCT
- **κ_di** = Krümmungsparameter (abnehmender Grenzertrag)
- Optimum pro Dimension: **s_i\*(d) = β_di / (2κ_di)**

### β-Matrix (hypothesiert, zu kalibrieren)

```
              s₁        s₂        s₃        s₄        s₅
            Formal.   Zentral.  Spezial.  Koord.    Deleg.

V_RE        +0.80     +0.60     +0.70     +0.50     −0.30
V_RC        −0.30     −0.40     −0.50     +0.80     +0.75
V_AC        −0.50     −0.60     −0.40     +0.65     +0.80
V_IC        −0.60     −0.70     +0.20     +0.70     +0.85
```

**Strukturelle Muster:**

1. **Kontroll-Cluster** (s₁, s₂, s₃): Positiv für V_RE, negativ für V_RC/V_AC/V_IC
2. **Flexibilitäts-Cluster** (s₄, s₅): Positiv für V_RC/V_AC/V_IC, gemischt für V_RE
3. **Koordination (s₄)** ist die einzige Dimension mit durchgehend positivem Effekt
4. **Spezialisierung (s₃) bei V_IC** ist positiv (+0.20) — Tiefenwissen fördert Innovation

### Kontext-Abhängigkeit der β-Werte

```
β_di(Ψ_target) = β_di(Ψ_anchor) × Π_k M(ΔΨ_k)
```

Hypothesierte Kontext-Effekte:

| Kontext-Shift | Effekt auf β | Begründung |
|---|---|---|
| Ψ_competition ↑ | β für V_IC steigt | Dynamischer Markt → Innovation wichtiger |
| Ψ_size ↑ | β für V_RE steigt | Grössere Firma → Verlässlichkeit wichtiger |
| Ψ_regulation ↑ | β für s₁ steigt | Regulierung erzwingt Formalisierung |
| Ψ_lifecycle = mature | β für V_RE ↑, V_IC ↓ | Reife → Effizienz vor Innovation |
| Ψ_lifecycle = growth | β für V_IC ↑, V_RE ↓ | Wachstum → Innovation vor Effizienz |
| Ψ_ownership = family | β für V_RC ↑ | Beziehungen zentral im Familienbetrieb |

## 4. V_WTP Ableitung

### EXC-Begründung

V_RE hat Veto-Eigenschaft (EXC-5, V1): Wenn V_RE = 0 (komplett unzuverlässig), zahlt kein Kunde, egal wie innovativ. → V_RE ist multiplikativ. Die anderen Value Dimensions sind untereinander additiv (kein Veto-Argument).

### Formel

```
V_WTP(Ψ) = V_RE × (α₀ + α_RC · V_RC + α_AC · V_AC + α_IC · V_IC)
```

Wobei:
- **V_RE** = Hygiene-Faktor (multiplikativ, Veto bei 0)
- **α₀** = Baseline-WTP aus reiner Verlässlichkeit (Commodity-Level)
- **α_RC, α_AC, α_IC** = kontextabhängige Differenzierungs-Gewichte

### α-Gewichte nach Branche (hypothesiert)

```
                  α₀      α_RC    α_AC    α_IC
Bau               0.50    0.30    0.10    0.10
Banking           0.40    0.35    0.15    0.10
Tech/Software     0.20    0.10    0.25    0.45
Beratung          0.15    0.40    0.20    0.25
Retail            0.35    0.15    0.20    0.30
```

**Interpretation:**
- Bau: Hoher α₀ (Zuverlässigkeit allein hat Wert), hoher α_RC (Beziehungen entscheiden)
- Tech: Niedriger α₀, hoher α_IC (Innovation ist das Produkt)
- Beratung: Höchster α_RC (reines Beziehungsgeschäft)

## 5. Geschlossene Lösung für S*

### Welfare Function

```
W(S, Ψ) = Σ_a ω_a(Ψ, t) · U_a(S, Ψ)

U_a(S, Ψ) = Σ_d w_ad(Ψ) · V_d(S, Ψ) + Σ_{d<d'} γ_dd' · V_d · V_d'
```

### Optimales S (ohne γ-Interaktionsterme, vereinfacht)

```
s_i* = [ Σ_a Σ_d ω_a · w_ad · β_di ] / [ 2 · Σ_a Σ_d ω_a · w_ad · κ_di ]
```

Berechenbar mit geschlossener Formel — kein Solver nötig.

### Gap-Analyse

```
Gap_i = s_i* − s_i^ist

|Gap| gross + β hoch  →  Höchste Priorität (grösster Hebel)
|Gap| klein            →  Niedrige Priorität (bereits nah am Optimum)
```

### Transformationspfad

```
S(t+1) = S(t) + ΔS(t)

Anpassungskosten: C(ΔS) = Σ_i c_i · |Δs_i|²
Transformations-Dip: V_d(t) = V_d^neu − D_d(ΔS)
```

**Reihenfolge-Logik:**
1. ZUERST s₄↑ (Koordination) — schafft Basis für alles andere
2. DANN s₅↑ (Delegation) — braucht funktionierende Koordination
3. DANN s₂↓ (Dezentralisierung) — braucht funktionierende Delegation
4. ZULETZT s₁↓ (Entformalisierung) — erst wenn neues System läuft

## 6. Perspektiven-Stress-Test

### Methodik

Das Modell wurde systematisch durch die Augen jeder Actor Group betrachtet, um Lücken zu identifizieren:

### B_L (Leadership) — Gefundene Lücken

| # | Lücke | Bewertung | Aktion |
|---|---|---|---|
| 1 | Talent/Menschen fehlt | In V_RC + V_AC enthalten | Keine Änderung |
| 2 | Geschwindigkeit fehlt | Teil von V_AC | V_AC Definition erweitert |
| 3 | Reputation fehlt | Abgeleitet wie V_WTP | Keine Änderung |
| 4 | Kultur fehlt | Ψ-Faktor | Ψ_culture ergänzt |
| 5 | Informationsfluss fehlt | Teil von s₄ | s₄ Definition geschärft |

### B_M (Middle Management) — Gefundene Lücken

| # | Lücke | Bewertung | Aktion |
|---|---|---|---|
| 6 | Struktur-Dimensionen zu aggregiert | Bewusste Vereinfachung | Keine Änderung |
| 7 | Koordination ohne Richtung | s₄ = horizontal, vertikal ≈ s₂ | Definition geschärft |
| 8 | Ressourcen/Budget fehlt | Constraint (bereits im Modell) | Keine Änderung |
| 9 | Übersetzungsfunktion B_M | Emergiert aus s₂ × s₄ | Keine Änderung |
| 10 | Verbesserung ≠ Innovation | Branchenabhängig via β(Ψ) | V_IC Definition erweitert |

### B_O (Operations) — Gefundene Lücken

| # | Lücke | Bewertung | Aktion |
|---|---|---|---|
| 11 | Klarheit ≠ Kontrolle | **ECHTE LÜCKE** | V_OC → V_RE umbenannt |
| 12 | Fairness fehlt | Ψ-Faktor | Ψ_fairness ergänzt |
| 13 | Sicherheit/Stabilität fehlt | Kehrseite von V_AC (negatives w_O,AC) | Keine Änderung |
| 14 | Voice/Mitsprache fehlt | Teil von s₄ (aufwärts) | Keine Änderung |
| 15 | Entwicklung/Karriere fehlt | Effekt von V_AC + V_RC | Keine Änderung |
| 16 | Anerkennung fehlt | Teil von Ψ_culture | Keine Änderung |

### B_E (External) — Gefundene Lücken

| # | Lücke | Bewertung | Aktion |
|---|---|---|---|
| 17 | V_WTP Ableitung unspezifiziert | **ECHTE LÜCKE** | V_WTP Formel spezifiziert |

### Ergebnis

```
17 Lücken geprüft:
  2 ECHTE LÜCKEN        → Modell geändert (V_OC→V_RE, V_WTP Ableitung)
  5 DEFINITIONEN        → Bestehende Dimensionen geschärft
  4 Ψ-FAKTOREN          → Kontext ergänzt (Ψ_culture, Ψ_fairness)
  5 BEREITS IM MODELL   → Nur nicht offensichtlich genug
  1 BEWUSSTE WAHL       → Aggregiert lassen
```

## 7. View-Architektur

### Actor Group Views (Dokumente für verschiedene Zielgruppen)

Jede Actor Group bekommt ein eigenes Dokument aus demselben Modell:

| View | Zeigt | Tiefe | Format |
|---|---|---|---|
| B_L | S* Ergebnis, Gap-Analyse, Business Case | 2-3 Seiten | Entscheidungsvorlage |
| B_M | Rollenveränderungen, neue Verantwortungen | 3-5 Seiten | Rollen-Dokument |
| B_O | Was ändert sich im Alltag, Zeitplan, FAQ | 1-2 Seiten | Kommunikation |
| B_E | Servicekontinuität, neue Ansprechpartner | 1 Seite | Stakeholder-Brief |

### Meta-Views (über dem Modell)

| View | Funktion | Tiefe |
|---|---|---|
| Theorie | Formale Modellspezifikation, Validierung | 30+ Seiten |
| Beratung | Delivery-Methodik, Workshop-Design, Deliverables | 10-15 Seiten |

### Perspektiven als Entwicklungs-Tool

Die Views dienen nicht nur der Kommunikation, sondern der **Modellentwicklung**: Jede Perspektive stress-testet das Modell und deckt Lücken auf (siehe Section 6).

## 8. Kontextabhängige Actor Group Auffächerung

B_L spaltet sich je nach Ψ_ownership:

| Ψ_ownership | B_L wird zu | Zentrale Spannung |
|---|---|---|
| family_business | B_LE (Eigentümer) + B_LN (Nachfolger) + B_LF (angest. Führung) | Tradition vs. Modernisierung |
| publicly_traded | B_LB (Board) + B_LC (CEO) + B_LF (angest. Führung) | Governance vs. operative Freiheit |
| founder_led | B_LG (Gründer) + B_LF (angest. Führung) | Vision vs. Professionalisierung |
| cooperative | B_LV (Vorstand/Mitglieder) + B_LF (angest. Führung) | Mitbestimmung vs. Effizienz |

Die Spannung innerhalb B_L wird durch unterschiedliche Gewichtungsvektoren w modelliert:

```
Beispiel family_business:
  B_LE: hoher w für V_RE (Stabilität), V_RC (Beziehungen)
  B_LN: hoher w für V_AC (Anpassung), V_IC (Innovation)
  → Generationen-Alignment γ(B_LE, B_LN) bestimmt Übergangserfolg
```

## 9. Offene Fragen

1. **β-Kalibrierung:** Literatur (Bloom/Van Reenen, Ichniowski), LLMMC, oder empirisch?
2. **κ-Werte:** Uniform (κ = 0.5 für alle) oder dimensionsspezifisch?
3. **γ zwischen V_RE und V_AC/V_IC:** Aktualisieren auf V_RE (statt V_OC)?
4. **V_WTS Integration:** Bestehende V_WTS mit V_WTP Ableitung konsistent machen
5. **Validierung:** Mintzberg-Konfigurationen als Plausibilitätscheck (erzeugt S* bekannte Org-Typen?)

## 10. Bezug zum bestehenden FA-SM-2.0

Dieser Org-Design-Layer ist eine **Erweiterung**, kein Ersatz:

```
Bestehendes FA-SM-2.0:
  V ← B(t) ← Ψ(t)         Dynamik, ODE, Predictions

Org-Design-Layer (NEU):
  V ← f(S, Ψ)              Statisches Optimum S*
  S(t+1) = S(t) + ΔS       Transformationspfad

Verbindung:
  S beeinflusst Ψ^org      (Struktur ist Teil des organisatorischen Kontexts)
  Ψ^org beeinflusst B       (bestehende ODE-Dynamik)
  B erzeugt V               (bestehende Akkumulationslogik)
```

Der Org-Design-Layer beantwortet: **"Welche Struktur S sollen wir wählen?"**
Das bestehende FA-SM-2.0 beantwortet: **"Was passiert dann dynamisch?"**

---

*Entwickelt: 2026-02-24*
*Status: EXPERIMENTAL*
*Methode: Perspektiven-Stress-Test (B_L → B_M → B_O → B_E)*
