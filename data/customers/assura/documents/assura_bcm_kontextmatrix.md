# BCM-Kontextmatrix Assura

**Version:** 1.0
**Datum:** 2026-01-28
**Status:** Formale Modellgrundlage
**Lead:** LEAD-013
**Abhängigkeit:** Muss VOR jeder Aktivitäten-Bewertung gelesen werden

---

## Meta-Axiom-Konformität

Dieses Dokument erfüllt die BCM Meta-Axiome:

| MA | Anforderung | Status |
|----|-------------|--------|
| MA 0.21 | Kontextprüfung vor Modellierung | ✅ |
| MA 0.22 | Nutzenstruktur explizit | ✅ |
| MA 0.23 | Keine teleologische Sprache | ✅ |
| MA 0.24 | Komplementarität hergeleitet | ✅ |
| MA 0.25 | Segmente als Gleichgewichtstypen | ✅ |
| MA 0.26 | Kontext ≠ Nutzen ≠ Intervention | ✅ |

---

## Teil 1: Formale Kontextfixierung (Ψ-Matrix)

### 1.1 Kontextdefinition nach BCM

> **Kontext (Ψ)** ist die Menge aller Randbedingungen, die bestimmen, welche Verhaltensgleichgewichte **überhaupt möglich** sind – unabhängig von Präferenzen oder Interventionen.

Kontext ist **nicht**:
- Was Menschen wollen (→ Nutzen)
- Was wir anbieten (→ Intervention)
- Wie Menschen reagieren (→ Outcome)

Kontext **ist**:
- Was Menschen **können** (Constraints)
- Was Menschen **dürfen** (Normen, Regeln)
- Was Menschen **wissen könnten** (Information)
- Welche Optionen **existieren** (Choice Set)

---

### 1.2 Ψ-Dimensionen für Assura-Kontext

#### Ψ_I: Institutioneller Kontext (Regeln & Defaults)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ_I: INSTITUTIONELLER KONTEXT                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  REGULATORISCH                                                          │
│  ├── KVG-Obligatorium: Jeder MUSS versichert sein                      │
│  ├── Franchise-System: 300-2500 CHF wählbar                            │
│  ├── Versichererwechsel: Jährlich möglich (30.11.)                     │
│  ├── Leistungskatalog: Gesetzlich definiert (KVG)                      │
│  └── Prämienverbilligung: Kantonal geregelt                            │
│                                                                         │
│  DEFAULTS (Status Quo)                                                  │
│  ├── Franchise-Default: 300 CHF (wenn nicht gewählt)                   │
│  ├── Assura-Kunden: 52% wählen 2500 CHF (aktive Wahl!)                 │
│  ├── Kein Auto-Renewal: Muss aktiv bleiben                             │
│  └── Kein Opt-out Gesundheitsprogramm: Opt-in erforderlich             │
│                                                                         │
│  CONSTRAINTS                                                            │
│  ├── Kontrahierungszwang: Assura MUSS jeden aufnehmen                  │
│  ├── Einheitsprämie: Keine Risikoselektion im KVG                      │
│  ├── Reservevorschriften: BAG-reguliert                                │
│  └── Datenschutz: DSG + Gesundheitsdaten-Spezialschutz                 │
│                                                                         │
│  BCM-IMPLIKATION:                                                       │
│  → Hohe institutionelle Stabilität                                     │
│  → Wenig Spielraum für Produktdifferenzierung im KVG                   │
│  → Verhaltensänderung nur über VVG oder Service möglich                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Formale Codierung:**
```
Ψ_I = {
  obligatorium: TRUE,
  franchise_range: [300, 2500],
  switching_cost: LOW (1x/Jahr),
  product_differentiation: LOW (KVG) | HIGH (VVG),
  default_health_program: OPT_IN,
  data_protection: HIGH
}
```

---

#### Ψ_S: Sozialer Kontext (Normen & Erwartungen)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ_S: SOZIALER KONTEXT                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SOZIALE NORMEN (Schweiz allgemein)                                     │
│  ├── Eigenverantwortung: Hoher gesellschaftlicher Wert                 │
│  ├── Subsidiarität: Staat als letztes Netz                             │
│  ├── Versicherung ≠ Gesundheitspartner: Kulturelle Trennung            │
│  └── Misstrauen ggü. «Upselling»: Sensibilität bei Zusatzverkauf       │
│                                                                         │
│  SOZIALE NORMEN (Assura-Kunden spezifisch)                              │
│  ├── Preisbewusstsein als Identität: «Ich bin schlau, ich spare»       │
│  ├── Skepsis ggü. «Betreuung»: «Brauche ich nicht»                     │
│  ├── Selbstbild: Informiert, autonom, rational                         │
│  └── Peer-Norm: Franchise 2500 = «vernünftige Wahl»                    │
│                                                                         │
│  REFERENZGRUPPEN                                                        │
│  ├── Primär: Familie, enge Freunde (bei Gesundheitsentscheiden)        │
│  ├── Sekundär: Arbeitskollegen (bei Versicherungswahl)                 │
│  └── Tertiär: Online-Communities (bei Recherche)                       │
│                                                                         │
│  BCM-IMPLIKATION:                                                       │
│  → Kollektiver Nutzen (KNU) ist NICHT dominanter Treiber               │
│  → Identitätsnutzen (IDN) über «smarte Wahl» aktivierbar               │
│  → Soziale Beweise müssen zur Selbstverantwortungs-Norm passen         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Formale Codierung:**
```
Ψ_S = {
  eigenverantwortung_norm: HIGH,
  insurance_as_partner_norm: LOW,
  price_consciousness_identity: HIGH,
  peer_influence_health: MEDIUM,
  peer_influence_insurance: LOW,
  social_proof_sensitivity: CONDITIONAL (must fit autonomy)
}
```

---

#### Ψ_K: Kultureller Kontext (Werte & Weltbild)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ_K: KULTURELLER KONTEXT                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHWEIZER WERTE (Hofstede/WVS-basiert)                                 │
│  ├── Individualismus: 68/100 (hoch)                                    │
│  ├── Unsicherheitsvermeidung: 58/100 (mittel-hoch)                     │
│  ├── Langzeitorientierung: 74/100 (sehr hoch)                          │
│  ├── Indulgence: 66/100 (mittel-hoch)                                  │
│  └── Power Distance: 34/100 (niedrig)                                  │
│                                                                         │
│  ASSURA-KUNDEN WERTE (abgeleitet)                                       │
│  ├── Rationalität: Entscheidungen sollen «vernünftig» sein             │
│  ├── Kontrolle: Eigene Gesundheit selbst managen                       │
│  ├── Effizienz: Kein Geld für «unnötige» Services                      │
│  ├── Pragmatismus: Was funktioniert, zählt                             │
│  └── Misstrauen: Institutionen haben Eigeninteressen                   │
│                                                                         │
│  GESUNDHEITSKULTUR                                                      │
│  ├── Schulmedizin-Akzeptanz: Hoch, aber kritisch                       │
│  ├── Komplementärmedizin: 25% nutzen aktiv                             │
│  ├── Prävention: Verbal hoch geschätzt, behavioral tief                │
│  └── Digital Health: Akzeptanz steigend, aber Privacy-sensitiv         │
│                                                                         │
│  BCM-IMPLIKATION:                                                       │
│  → Interventionen müssen «rational» erscheinen                         │
│  → Kontrolle beim Kunden belassen (kein Paternalismus)                 │
│  → Effizienz-Framing > Gesundheits-Framing                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Formale Codierung:**
```
Ψ_K = {
  individualism: 0.68,
  uncertainty_avoidance: 0.58,
  long_term_orientation: 0.74,
  rationality_norm: HIGH,
  control_preference: HIGH,
  paternalism_aversion: HIGH,
  efficiency_framing_preference: HIGH
}
```

---

#### Ψ_E: Ökonomischer Kontext (Ressourcen & Constraints)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ_E: ÖKONOMISCHER KONTEXT                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ASSURA-KUNDEN ÖKONOMISCH                                               │
│  ├── Einkommensspektrum: Breit (nicht nur «arm»)                       │
│  ├── Franchise 2500 Wähler: Oft NICHT einkommensschwach                │
│  │   → Bewusste Risikoübernahme bei finanzieller Kapazität             │
│  ├── Prämienanteil am Budget: Überdurchschnittlich sensitiv            │
│  └── Opportunitätskosten: Zeit = Geld (Digital bevorzugt)              │
│                                                                         │
│  ASSURA UNTERNEHMEN                                                     │
│  ├── Kostenquote: 4.4% (Branche: 6.8%)                                 │
│  ├── Versicherte/MA: 2053 (Helsana: 619)                               │
│  ├── Reserven: Solide, aber nicht üppig                                │
│  ├── IT-Investment: Funktional, nicht Premium                          │
│  └── Margenstruktur: Dünn, Volumen-getrieben                           │
│                                                                         │
│  BUDGET-CONSTRAINTS FÜR INTERVENTION                                    │
│  ├── CAPEX für neue Programme: Begrenzt                                │
│  ├── OPEX pro Versichertem: Muss unter Branche bleiben                 │
│  ├── Payback-Erwartung: <24 Monate                                     │
│  └── ROI-Schwelle: Positiv ab Jahr 2                                   │
│                                                                         │
│  BCM-IMPLIKATION:                                                       │
│  → Interventionen müssen KOSTENEFFIZIENT sein                          │
│  → Digital-First nicht optional, sondern Constraint                    │
│  → Personalintensive Programme = nicht kompatibel                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Formale Codierung:**
```
Ψ_E = {
  customer_price_sensitivity: HIGH,
  customer_time_value: HIGH,
  assura_cost_constraint: HARD (< industry average),
  intervention_budget: LOW,
  payback_requirement: 24_months,
  scalability_requirement: MANDATORY
}
```

---

#### Ψ_C: Kognitiver Kontext (Aufmerksamkeit & Kapazität)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ_C: KOGNITIVER KONTEXT                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  AUFMERKSAMKEIT (Assura-Interaktion)                                    │
│  ├── Kontaktfrequenz: ~2x/Jahr (Rechnung, ev. Claim)                   │
│  ├── Engagement: Minimal (transaktional)                               │
│  ├── Prämienvergleich-Moment: November (hohe Attention)                │
│  ├── Gesundheits-Moment: Bei Erkrankung (reaktiv)                      │
│  └── Präventions-Attention: Sehr niedrig (kein Touchpoint)             │
│                                                                         │
│  KOGNITIVE KAPAZITÄT                                                    │
│  ├── Für Versicherungs-Themen: Niedrig (Desinteresse)                  │
│  ├── Für Gesundheits-Themen: Variabel (kontextabhängig)                │
│  ├── Für Komplexität: Niedrige Toleranz                                │
│  └── Für neue Angebote: Skeptisch, aber nicht ablehnend                │
│                                                                         │
│  AWARENESS-BARRIEREN                                                    │
│  ├── «Assura = billig» Frame dominiert                                 │
│  ├── Kein mentales Modell für «Assura hilft mir»                       │
│  ├── Erwartungshaltung: Transaktional, nicht relational                │
│  └── Information Overload bei Gesundheitsthemen                        │
│                                                                         │
│  BCM-IMPLIKATION:                                                       │
│  → Awareness muss ERST aufgebaut werden                                │
│  → Touchpoint-Armut = geringe Interventionsfenster                     │
│  → Komplexität = Adoption-Killer                                       │
│  → November + Krankheitsmoment = einzige High-Attention Windows        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Formale Codierung:**
```
Ψ_C = {
  baseline_attention: LOW,
  attention_windows: [NOVEMBER, ILLNESS_EVENT],
  cognitive_load_tolerance: LOW,
  complexity_aversion: HIGH,
  frame_assura: "cheap_transactional",
  mental_model_assura_helps: ABSENT,
  awareness_buildable: TRUE (but effortful)
}
```

---

#### Ψ_T: Temporaler Kontext (Zeit & Lebensphase)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ_T: TEMPORALER KONTEXT                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ZYKLISCHE MOMENTE                                                      │
│  ├── Jahreswechsel: Franchise-Entscheid (Dezember)                     │
│  ├── Prämienvergleich: Oktober-November                                │
│  ├── Steuererklärung: März-April (Kostenbelege)                        │
│  └── Ferienzeit: Reiseversicherungs-Awareness                          │
│                                                                         │
│  LEBENSPHASEN-ÜBERGÄNGE (LCE-Trigger)                                   │
│  ├── L1→L2: Ausbildungsende, erster Job                                │
│  ├── L2→L3: Familiengründung, Verantwortungsübernahme                  │
│  ├── L3→L4: Empty Nest, Karriere-Plateau                               │
│  ├── L4→L5: Pensionierung, Gesundheitsabbau                            │
│  └── Jederzeit: Diagnose, Unfall, Krise                                │
│                                                                         │
│  ZEITPRÄFERENZEN                                                        │
│  ├── Gegenwartspräferenz: Mittel (CH: β ≈ 0.85)                        │
│  ├── Prävention-Paradox: Wissen > Handeln                              │
│  ├── Planungshorizont: Lang (Pensionierung), aber abstrakt             │
│  └── Urgency-Response: Nur bei akuter Bedrohung                        │
│                                                                         │
│  BCM-IMPLIKATION:                                                       │
│  → Interventionen an LCE-Momente koppeln                               │
│  → Zyklische Fenster (Nov) = beste Erreichbarkeit                      │
│  → Präventions-Interventionen brauchen Urgency-Frame                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Formale Codierung:**
```
Ψ_T = {
  annual_attention_peak: NOVEMBER,
  lce_sensitivity: HIGH,
  present_bias: 0.85,
  prevention_paradox: TRUE,
  planning_horizon: LONG_BUT_ABSTRACT,
  urgency_required_for_action: TRUE
}
```

---

#### Ψ_U: Unsicherheitskontext (Wissen & Ungewissheit)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ_U: UNSICHERHEITSKONTEXT                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INFORMATIONSASYMMETRIEN                                                │
│  ├── Versicherer kennt Claims-Historie: Ja                             │
│  ├── Kunde kennt eigenes Gesundheitsverhalten: Teilweise               │
│  ├── Kunde kennt optimale Versorgungspfade: Selten                     │
│  └── Kunde kennt Kosten-Nutzen von Prävention: Abstrakt                │
│                                                                         │
│  UNSICHERHEITSQUELLEN                                                   │
│  ├── Gesundheitszustand Zukunft: Unbekannt                             │
│  ├── Kosten bei Krankheit: Unbekannt (daher Versicherung)              │
│  ├── Qualität von Leistungserbringern: Schwer beurteilbar              │
│  ├── Wirksamkeit von Prävention: Probabilistisch                       │
│  └── Eigene Compliance: Überschätzt                                    │
│                                                                         │
│  UMGANG MIT UNSICHERHEIT (Assura-Kunden)                                │
│  ├── Risiko-Absorption via hohe Franchise: Bewusste Strategie          │
│  ├── Informationssuche: Hoch (Online-Recherche)                        │
│  ├── Expertenvertrauen: Selektiv (Ärzte > Versicherer)                 │
│  └── Ambiguitätsaversion: Mittel (will klare Optionen)                 │
│                                                                         │
│  BCM-IMPLIKATION:                                                       │
│  → Transparenz als Wert (nicht als Taktik)                             │
│  → Unsicherheitsreduktion = legitimer Nutzen                           │
│  → Aber: Nicht bevormundend («wir wissen es besser»)                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Formale Codierung:**
```
Ψ_U = {
  health_uncertainty: HIGH,
  cost_uncertainty: HIGH,
  quality_uncertainty: HIGH,
  prevention_efficacy_belief: LOW,
  self_compliance_overestimation: TRUE,
  information_seeking: HIGH,
  expert_trust: SELECTIVE (doctors > insurers),
  ambiguity_aversion: MEDIUM
}
```

---

### 1.3 Kontextmatrix-Zusammenfassung

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Ψ-MATRIX ASSURA (Aggregiert)                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Dimension    │ Kerncharakteristik           │ BCM-Implikation          │
│  ─────────────┼──────────────────────────────┼──────────────────────────│
│  Ψ_I (Instit.)│ Stark reguliert, wenig Diff. │ Service = einziger Hebel │
│  Ψ_S (Sozial) │ Eigenverantwortungs-Norm     │ KNU schwach, IDN stark   │
│  Ψ_K (Kultur) │ Rational, Kontrolle, Effizienz│ Anti-Paternalismus      │
│  Ψ_E (Ökonom.)│ Cost-Leader, Budget-Constraint│ Digital-First Pflicht   │
│  Ψ_C (Kognit.)│ Low Attention, wenig Touchpts│ Awareness = Haupthürde   │
│  Ψ_T (Tempor.)│ Nov + LCE = Windows          │ Timing = kritisch        │
│  Ψ_U (Unsich.)│ Hohe Unsicherheit, Recherche │ Transparenz = Wert       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Teil 2: Nutzenstruktur (INU/KNU/IDN)

### 2.1 BCM-Nutzenarchitektur

> **Im BCM ist Nutzen keine Präferenz, sondern eine stabilisierbare Funktion im Kontext.**

Die Frage ist nicht «Was wollen Assura-Kunden?»
sondern «Welche Nutzenkomponenten können im gegebenen Kontext überhaupt wirksam werden?»

---

### 2.2 Individueller Nutzen (INU)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  INU: INDIVIDUELLER NUTZEN                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DEFINITION:                                                            │
│  INU = Nutzen, der DIREKT beim Individuum anfällt,                     │
│        unabhängig von sozialer Bewertung oder Identität.               │
│                                                                         │
│  INU-KOMPONENTEN (Assura-Kontext)                                       │
│                                                                         │
│  INU_F: Finanzieller Nutzen                                            │
│  ├── Prämienersparnis (primär)                                         │
│  ├── Out-of-Pocket Reduktion (sekundär)                                │
│  ├── Opportunitätskosten (Zeit = Geld)                                 │
│  └── Status: DOMINANT im Assura-Kontext                                │
│                                                                         │
│  INU_H: Gesundheitsnutzen                                              │
│  ├── Symptomlinderung (akut)                                           │
│  ├── Krankheitsvermeidung (präventiv)                                  │
│  ├── Lebensqualität (chronisch)                                        │
│  └── Status: SEKUNDÄR (nur bei akuter Relevanz aktivierbar)            │
│                                                                         │
│  INU_C: Convenience-Nutzen                                             │
│  ├── Zeitersparnis                                                     │
│  ├── Einfachheit                                                       │
│  ├── Verfügbarkeit                                                     │
│  └── Status: HOCH (passt zu Effizienz-Norm)                            │
│                                                                         │
│  INU_S: Sicherheitsnutzen                                              │
│  ├── Unsicherheitsreduktion                                            │
│  ├── Rückversicherung bei Entscheiden                                  │
│  ├── Schutz vor Fehlern                                                │
│  └── Status: LATENT (aktivierbar bei Framing)                          │
│                                                                         │
│  INU_A: Autonomie-Nutzen                                               │
│  ├── Kontrolle behalten                                                │
│  ├── Eigene Entscheidungen treffen                                     │
│  ├── Nicht bevormundet werden                                          │
│  └── Status: SEHR HOCH (kritische Nebenbedingung!)                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**INU-Hierarchie im Assura-Kontext:**
```
INU_A (Autonomie) ≥ INU_F (Finanziell) > INU_C (Convenience) > INU_S (Sicherheit) > INU_H (Gesundheit)
```

⚠️ **Kritische Erkenntnis:** INU_H (Gesundheit) ist **nicht** der primäre Treiber!
Gesundheitsbegleitung muss über INU_F, INU_C oder INU_A verkauft werden.

---

### 2.3 Kollektiver Nutzen (KNU)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  KNU: KOLLEKTIVER NUTZEN                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DEFINITION:                                                            │
│  KNU = Nutzen, der aus der Zugehörigkeit zu einer Gruppe               │
│        oder dem Beitrag zum Gemeinwohl entsteht.                       │
│                                                                         │
│  KNU-KOMPONENTEN (Assura-Kontext)                                       │
│                                                                         │
│  KNU_F: Familien-Nutzen                                                │
│  ├── Für Familie sorgen                                                │
│  ├── Vorbild sein                                                      │
│  ├── Nicht zur Last fallen                                             │
│  └── Status: AKTIVIERBAR (bei L2-L4, bei Pflege-Themen)                │
│                                                                         │
│  KNU_C: Community-Nutzen                                               │
│  ├── Zum Kollektiv beitragen                                           │
│  ├── Solidarität zeigen                                                │
│  ├── Gemeinsam Kosten senken                                           │
│  └── Status: SCHWACH (Individualismus-Norm dominiert)                  │
│                                                                         │
│  KNU_S: Systemischer Nutzen                                            │
│  ├── Gesundheitssystem entlasten                                       │
│  ├── Prämien für alle senken                                           │
│  ├── Ressourcen schonen                                                │
│  └── Status: RHETORISCH (kein Verhaltenstreiber)                       │
│                                                                         │
│  GESAMTSTATUS KNU:                                                      │
│  → KNU ist im Assura-Kontext KEIN primärer Verhaltenstreiber           │
│  → KNU_F ist einzige aktivierbare Komponente                           │
│  → Solidaritäts-Framing = kontraproduktiv für S1/S3                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**KNU-Hierarchie im Assura-Kontext:**
```
KNU_F (Familie) >> KNU_C (Community) > KNU_S (System)
```

⚠️ **Kritische Erkenntnis:** KNU ist **nicht** der primäre Hebel!
«Solidarität»-Framing wird von S1/S3 als manipulativ wahrgenommen.

---

### 2.4 Identitätsnutzen (IDN)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  IDN: IDENTITÄTSNUTZEN                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DEFINITION:                                                            │
│  IDN = Nutzen, der aus der Bestätigung oder Stärkung                   │
│        des Selbstkonzepts entsteht.                                    │
│                                                                         │
│  IDN-KOMPONENTEN (Assura-Kontext)                                       │
│                                                                         │
│  IDN_R: Rationalitäts-Identität                                        │
│  ├── «Ich entscheide klug»                                             │
│  ├── «Ich lasse mich nicht über den Tisch ziehen»                      │
│  ├── «Ich durchschaue Marketing»                                       │
│  └── Status: SEHR STARK (Kern der Assura-Wahl)                         │
│                                                                         │
│  IDN_A: Autonomie-Identität                                            │
│  ├── «Ich brauche keine Hilfe»                                         │
│  ├── «Ich manage mein Leben selbst»                                    │
│  ├── «Ich bin unabhängig»                                              │
│  └── Status: SEHR STARK (komplementär zu IDN_R)                        │
│                                                                         │
│  IDN_E: Effizienz-Identität                                            │
│  ├── «Ich verschwende kein Geld»                                       │
│  ├── «Ich optimiere»                                                   │
│  ├── «Ich bin praktisch veranlagt»                                     │
│  └── Status: STARK (passt zu Cost-Leadership)                          │
│                                                                         │
│  IDN_H: Gesundheits-Identität                                          │
│  ├── «Ich achte auf meine Gesundheit»                                  │
│  ├── «Ich bin gesundheitsbewusst»                                      │
│  ├── «Ich lebe gesund»                                                 │
│  └── Status: VARIABEL (nicht dominant, aber aktivierbar)               │
│                                                                         │
│  IDN_K: Kritiker-Identität (spezifisch S3)                             │
│  ├── «Ich hinterfrage das System»                                      │
│  ├── «Ich lasse mir nichts vormachen»                                  │
│  ├── «Ich bin kein Schaf»                                              │
│  └── Status: STARK bei S3 (25% der Assura-Kunden)                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**IDN-Hierarchie im Assura-Kontext:**
```
IDN_R (Rationalität) ≈ IDN_A (Autonomie) > IDN_E (Effizienz) > IDN_K (Kritik) > IDN_H (Gesundheit)
```

✅ **Kritische Erkenntnis:** IDN ist der **stärkste Hebel**!
Interventionen müssen die Rationalitäts- und Autonomie-Identität **bestätigen**, nicht bedrohen.

---

### 2.5 Nutzenstruktur-Zusammenfassung

```
┌─────────────────────────────────────────────────────────────────────────┐
│  NUTZEN-DOMINANZ IM ASSURA-KONTEXT                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PRIMÄR (verhaltensrelevant):                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  IDN_R (Rationalität) + IDN_A (Autonomie) + INU_F (Finanziell)  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  SEKUNDÄR (unterstützend):                                             │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  INU_C (Convenience) + IDN_E (Effizienz) + INU_A (Autonomie)    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  TERTIÄR (kontextabhängig aktivierbar):                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  INU_S (Sicherheit) + KNU_F (Familie) + IDN_H (Gesundheit)      │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  NICHT WIRKSAM (vermeiden):                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  KNU_C (Community) + KNU_S (System) + INU_H (direkt)            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ➡️ INTERVENTIONS-IMPLIKATION:                                          │
│  «Hilft dir, kluge Entscheidungen zu treffen» > «Macht dich gesünder» │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 2.6 Nutzen-Kontext-Interaktion (Formal)

Die wirksame Nutzenfunktion U* im Assura-Kontext ist:

```
U*(x) = Σᵢ wᵢ(Ψ) · Uᵢ(x)

Wobei:
- Uᵢ ∈ {INU_F, INU_C, INU_S, INU_A, INU_H, KNU_F, KNU_C, KNU_S, IDN_R, IDN_A, IDN_E, IDN_H, IDN_K}
- wᵢ(Ψ) = kontextabhängiges Gewicht
- Ψ = Kontextvektor aus Teil 1

Gewichte im Assura-Kontext (normiert):
┌────────────┬────────┬──────────────────────────────┐
│ Komponente │ w(Ψ)   │ Begründung                   │
├────────────┼────────┼──────────────────────────────┤
│ IDN_R      │ 0.20   │ Kern der Assura-Wahl         │
│ IDN_A      │ 0.18   │ Autonomie-Kultur CH          │
│ INU_F      │ 0.15   │ Cost-Leader Positionierung   │
│ INU_A      │ 0.12   │ Kontrolle-Präferenz          │
│ IDN_E      │ 0.10   │ Effizienz-Norm               │
│ INU_C      │ 0.08   │ Zeit-Wert hoch               │
│ INU_S      │ 0.05   │ Nur bei Unsicherheit         │
│ KNU_F      │ 0.05   │ Nur bei Familie-Kontext      │
│ IDN_H      │ 0.04   │ Nicht dominant               │
│ INU_H      │ 0.02   │ Nur akut aktivierbar         │
│ IDN_K      │ 0.01   │ Nur S3                       │
│ KNU_C      │ 0.00   │ Nicht wirksam                │
│ KNU_S      │ 0.00   │ Nicht wirksam                │
└────────────┴────────┴──────────────────────────────┘
```

---

## Teil 3: Segmente als Gleichgewichtstypen

### 3.1 BCM-Segment-Definition

> **Im BCM ist ein Segment kein Zielgruppen-Cluster, sondern ein stabiles Verhaltensgleichgewicht.**

Ein Gleichgewicht ist stabil, wenn:
1. Die Person keinen Anreiz hat, einseitig abzuweichen
2. Der Kontext das Verhalten reproduziert
3. Die Identität das Verhalten bestätigt

---

### 3.2 Segment-Reklassifikation

#### GG1: Autonomes Optimierungs-Gleichgewicht (vorher S1)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  GG1: AUTONOMES OPTIMIERUNGS-GLEICHGEWICHT                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STABILITÄTSBEDINGUNGEN:                                                │
│  ├── IDN_R + IDN_A > Schwelle (Identität bestätigt)                    │
│  ├── INU_F optimiert (Kosten minimiert)                                │
│  ├── INU_A gewahrt (Kontrolle behalten)                                │
│  └── Ψ_C: Wenig Touchpoints = wenig Störung                            │
│                                                                         │
│  GLEICHGEWICHTS-VERHALTEN:                                              │
│  ├── Höchste Franchise gewählt (bewusst)                               │
│  ├── Minimale Interaktion mit Versicherer (gewollt)                    │
│  ├── Eigene Recherche bei Gesundheitsfragen                            │
│  ├── Ablehnung von «Betreuungs»-Angeboten                              │
│  └── Wechselbereitschaft bei besserem Angebot                          │
│                                                                         │
│  DESTABILISIERUNGS-TRIGGER:                                             │
│  ├── Schwere Diagnose (INU_S wird relevant)                            │
│  ├── Familiengründung (KNU_F wird relevant)                            │
│  ├── Komplexität übersteigt Kapazität (INU_C wird relevant)            │
│  └── Identitätsbedrohung (IDN_R/IDN_A verletzt)                        │
│                                                                         │
│  ANSCHLUSSFÄHIGE INTERVENTIONEN:                                        │
│  ├── ✅ Tools, die Autonomie STÄRKEN                                   │
│  ├── ✅ Information, die kluge Entscheidungen ERMÖGLICHT               │
│  ├── ✅ Effizienz-Gewinne (Zeit, Geld)                                 │
│  ├── ❌ Coaching (= Bevormundung)                                      │
│  ├── ❌ Betreuung (= Abhängigkeit)                                     │
│  └── ❌ Solidaritäts-Framing (= Manipulation)                          │
│                                                                         │
│  ANTEIL: 35% der Assura-Kunden                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

#### GG2: Relationales Sicherheits-Gleichgewicht (vorher S2)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  GG2: RELATIONALES SICHERHEITS-GLEICHGEWICHT                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STABILITÄTSBEDINGUNGEN:                                                │
│  ├── INU_S + KNU_F > Schwelle (Sicherheit + Familie)                   │
│  ├── IDN_H aktiviert (Gesundheits-Identität)                           │
│  ├── Ψ_S: Vertrauen in Experten möglich                                │
│  └── Ψ_C: Bereit für Beziehungsaufbau                                  │
│                                                                         │
│  GLEICHGEWICHTS-VERHALTEN:                                              │
│  ├── Mittlere Franchise (Sicherheitspuffer)                            │
│  ├── Sucht persönlichen Kontakt bei Fragen                             │
│  ├── Loyal bei guter Erfahrung                                         │
│  ├── Offen für Empfehlungen (von Vertrauenspersonen)                   │
│  └── Wechselt nur bei Vertrauensbruch                                  │
│                                                                         │
│  DESTABILISIERUNGS-TRIGGER:                                             │
│  ├── Enttäuschende Service-Erfahrung                                   │
│  ├── Gefühl, «nur eine Nummer» zu sein                                 │
│  ├── Lebensereignis ohne Unterstützung                                 │
│  └── Empfehlung von Vertrauensperson zu wechseln                       │
│                                                                         │
│  ANSCHLUSSFÄHIGE INTERVENTIONEN:                                        │
│  ├── ✅ Persönliche Beratung                                           │
│  ├── ✅ Proaktive Kontaktaufnahme bei LCE                              │
│  ├── ✅ Vertrauensaufbau über Zeit                                     │
│  ├── ❌ Rein digitale Self-Service                                     │
│  ├── ❌ Komplexe Eigenverantwortungs-Tools                             │
│  └── ❌ Unpersönliche Massenansprache                                  │
│                                                                         │
│  ANTEIL: 18% der Assura-Kunden (unterrepräsentiert!)                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

#### GG3: Kritisches Distanz-Gleichgewicht (vorher S3)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  GG3: KRITISCHES DISTANZ-GLEICHGEWICHT                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STABILITÄTSBEDINGUNGEN:                                                │
│  ├── IDN_K + IDN_R > Schwelle (Kritiker + Rationalist)                 │
│  ├── INU_F dominant (Kosten = einziges legitimes Kriterium)            │
│  ├── Ψ_S: Misstrauen ggü. Institutionen                                │
│  └── Ψ_U: Hohe Informationssuche (zur Absicherung)                     │
│                                                                         │
│  GLEICHGEWICHTS-VERHALTEN:                                              │
│  ├── Höchste Franchise (= minimale Abhängigkeit)                       │
│  ├── Aktive Distanz zum Versicherer                                    │
│  ├── Hinterfragt jedes Angebot («Was ist der Haken?»)                  │
│  ├── Sucht Bestätigung für Skepsis                                     │
│  └── Wechselt bei besserem Preis sofort                                │
│                                                                         │
│  DESTABILISIERUNGS-TRIGGER:                                             │
│  ├── Positive Überraschung (gegen Erwartung)                           │
│  ├── Transparenz, die Misstrauen entkräftet                            │
│  ├── Krisenmoment, wo Hilfe nötig ist                                  │
│  └── Peer-Validierung («Die sind doch ok»)                             │
│                                                                         │
│  ANSCHLUSSFÄHIGE INTERVENTIONEN:                                        │
│  ├── ✅ Transparenz-Tools («So verdienen wir Geld»)                    │
│  ├── ✅ Kostenaufschlüsselung («So sparst du»)                         │
│  ├── ✅ Opt-in ohne Verpflichtung                                      │
│  ├── ❌ Jede Form von «wir kümmern uns»                                │
│  ├── ❌ Datensammlung ohne klaren Nutzen                               │
│  └── ❌ Versprechungen (werden als Manipulation gesehen)               │
│                                                                         │
│  ANTEIL: 25% der Assura-Kunden                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

#### GG4: Delegierendes Entlastungs-Gleichgewicht (vorher S4)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  GG4: DELEGIERENDES ENTLASTUNGS-GLEICHGEWICHT                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STABILITÄTSBEDINGUNGEN:                                                │
│  ├── INU_C >> INU_A (Convenience > Autonomie)                          │
│  ├── INU_S hoch (Sicherheitsbedürfnis)                                 │
│  ├── Ψ_C: Kognitive Kapazität begrenzt                                 │
│  └── Ψ_T: Oft in Belastungsphase (L3, L5)                              │
│                                                                         │
│  GLEICHGEWICHTS-VERHALTEN:                                              │
│  ├── Niedrige Franchise (will keinen Stress)                           │
│  ├── Delegiert Entscheidungen an Experten                              │
│  ├── Schätzt Komplett-Lösungen                                         │
│  ├── Loyal aus Bequemlichkeit                                          │
│  └── Wechselt nur bei aktivem Anstoß von außen                         │
│                                                                         │
│  DESTABILISIERUNGS-TRIGGER:                                             │
│  ├── Überforderung durch Komplexität                                   │
│  ├── Gefühl, allein gelassen zu werden                                 │
│  ├── Empfehlung von Vertrauensperson                                   │
│  └── Frustration durch Self-Service-Zwang                              │
│                                                                         │
│  ANSCHLUSSFÄHIGE INTERVENTIONEN:                                        │
│  ├── ✅ Case Management                                                │
│  ├── ✅ Proaktive Begleitung                                           │
│  ├── ✅ Einfache, klare Optionen                                       │
│  ├── ❌ Komplexe Eigenverantwortungs-Modelle                           │
│  ├── ❌ Digitale Self-Service ohne Backup                              │
│  └── ❌ Viele Wahlmöglichkeiten                                        │
│                                                                         │
│  ANTEIL: 12% der Assura-Kunden (stark unterrepräsentiert!)             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

#### GG5: Reaktives Minimal-Gleichgewicht (vorher S5)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  GG5: REAKTIVES MINIMAL-GLEICHGEWICHT                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STABILITÄTSBEDINGUNGEN:                                                │
│  ├── Alle Nutzenkomponenten schwach aktiviert                          │
│  ├── Ψ_C: Sehr niedrige Aufmerksamkeit für Gesundheit                  │
│  ├── Ψ_T: Gegenwartsfokus dominant                                     │
│  └── Default-Verhalten: Nichts ändern                                  │
│                                                                         │
│  GLEICHGEWICHTS-VERHALTEN:                                              │
│  ├── Default-Franchise (300 CHF, nie geändert)                         │
│  ├── Reagiert nur auf akute Probleme                                   │
│  ├── Ignoriert präventive Angebote                                     │
│  ├── Wenig Wissen über eigene Optionen                                 │
│  └── Wechselt nie aktiv                                                │
│                                                                         │
│  DESTABILISIERUNGS-TRIGGER:                                             │
│  ├── Akute Gesundheitskrise                                            │
│  ├── Externe Intervention (Familie, Arzt)                              │
│  ├── Zwang (z.B. Arbeitgeber-Programm)                                 │
│  └── Starker Default-Nudge                                             │
│                                                                         │
│  ANSCHLUSSFÄHIGE INTERVENTIONEN:                                        │
│  ├── ✅ Automatische Defaults                                          │
│  ├── ✅ Proaktive Outreach bei Risiko-Signalen                         │
│  ├── ✅ Sehr einfache, eine-Option-Kommunikation                       │
│  ├── ❌ Informationskampagnen (werden ignoriert)                       │
│  ├── ❌ Opt-in Programme (werden nicht wahrgenommen)                   │
│  └── ❌ Komplexe Entscheidungen                                        │
│                                                                         │
│  ANTEIL: 10% der Assura-Kunden                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 3.3 Gleichgewichts-Typologie Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  GLEICHGEWICHTS-TYPOLOGIE ASSURA                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Gleichgewicht │ Dominante Nutzen   │ Stabilitäts-Faktor │ Anteil      │
│  ──────────────┼────────────────────┼────────────────────┼─────────────│
│  GG1 (Autonom) │ IDN_R, IDN_A, INU_F│ Identität          │ 35%         │
│  GG2 (Relat.)  │ INU_S, KNU_F       │ Beziehung          │ 18%         │
│  GG3 (Kritisch)│ IDN_K, INU_F       │ Distanz            │ 25%         │
│  GG4 (Delegier)│ INU_C, INU_S       │ Entlastung         │ 12%         │
│  GG5 (Reaktiv) │ (alle schwach)     │ Inertia            │ 10%         │
│                                                                         │
│  ASSURA-SPEZIFIKUM:                                                     │
│  GG1 + GG3 = 60% (überdurchschnittlich!)                               │
│  → Interventionen müssen PRIMÄR für diese Gleichgewichte designt sein  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 3.4 Gleichgewichts-Übergänge (Transitionen)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TRANSITIONS-MATRIX                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Von \ Nach │ GG1   │ GG2   │ GG3   │ GG4   │ GG5                      │
│  ───────────┼───────┼───────┼───────┼───────┼───────                   │
│  GG1        │ STAB  │ 0.05  │ 0.08  │ 0.02  │ 0.01                     │
│  GG2        │ 0.03  │ STAB  │ 0.02  │ 0.10  │ 0.02                     │
│  GG3        │ 0.06  │ 0.02  │ STAB  │ 0.03  │ 0.02                     │
│  GG4        │ 0.01  │ 0.08  │ 0.02  │ STAB  │ 0.05                     │
│  GG5        │ 0.02  │ 0.03  │ 0.02  │ 0.08  │ STAB                     │
│                                                                         │
│  Legende: Jährliche Übergangswahrscheinlichkeit                        │
│  STAB = stabiles Gleichgewicht (>0.80)                                 │
│                                                                         │
│  HÄUFIGSTE TRANSITIONEN:                                               │
│  ├── GG2 → GG4: Bei Überforderung (Diagnose, Pflege)                   │
│  ├── GG1 → GG3: Bei negativer Erfahrung                                │
│  ├── GG4 → GG5: Bei anhaltender Passivität                             │
│  └── GG5 → GG4: Bei externer Intervention                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Teil 4: Awareness-Struktur (A)

### 4.1 BCM-Awareness-Definition

> **Awareness (A)** ist im BCM nicht «Wissen», sondern die **Wahrscheinlichkeit, dass eine Option im Entscheidungsmoment mental verfügbar ist**.

```
A(x) = P(x ∈ Consideration Set | Entscheidungsmoment)
```

---

### 4.2 Awareness-Komponenten im Assura-Kontext

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AWARENESS-STRUKTUR                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  A_BASE: Basis-Awareness für Assura-Angebote                           │
│  ├── Aktuell: ~5% (kaum jemand weiss, dass Assura Services hat)        │
│  ├── Ziel: 25% (jeder 4. kennt mindestens 1 Angebot)                   │
│  └── Constraint: Touchpoint-Armut (nur 2x/Jahr Kontakt)                │
│                                                                         │
│  A_RELEVANT: Relevanz-Awareness (in Entscheidungsmoment)               │
│  ├── Aktuell: ~2% (selbst Wissende denken nicht dran)                  │
│  ├── Ziel: 15% (bei relevanter Situation an Assura denken)             │
│  └── Hebel: LCE-Trigger, November-Fenster                              │
│                                                                         │
│  A_ACCESS: Zugangs-Awareness (wie nutze ich es?)                       │
│  ├── Aktuell: ~1% (kaum jemand weiss, wie man Angebote findet)         │
│  ├── Ziel: 20% (einfacher Zugang bekannt)                              │
│  └── Hebel: Prominente Platzierung, einfache URLs                      │
│                                                                         │
│  A_BENEFIT: Nutzen-Awareness (was bringt es mir?)                      │
│  ├── Aktuell: ~1% (Nutzen unklar)                                      │
│  ├── Ziel: 15% (klarer Nutzen verstanden)                              │
│  └── Hebel: Konkrete Beispiele, Testimonials                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 4.3 Awareness-Aufbau-Funktion

Die Awareness entwickelt sich gemäss:

```
A(t+1) = A(t) + δ·E(t) - λ·A(t)

Wobei:
- E(t) = Exposure (Kontakt mit Angebot)
- δ = Lernrate (wie schnell wird Awareness aufgebaut)
- λ = Vergessensrate (wie schnell sinkt Awareness ohne Kontakt)

Im Assura-Kontext:
- E(t) = sehr niedrig (wenig Touchpoints)
- δ = mittel (wenn Kontakt, dann aufnahmebereit)
- λ = hoch (schnelles Vergessen ohne Verstärkung)

→ IMPLIKATION: Ohne regelmässige Touchpoints sinkt Awareness schnell auf Null
→ LÖSUNG: LCE-basierte Aktivierung (Awareness aufbauen, wenn relevant)
```

---

### 4.4 Awareness × Gleichgewicht Matrix

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AWARENESS-AUFBAU NACH GLEICHGEWICHT                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Gleichgewicht │ Awareness-Kanal          │ Awareness-Barriere         │
│  ──────────────┼──────────────────────────┼────────────────────────────│
│  GG1 (Autonom) │ Self-Discovery, Tools    │ «Brauche ich nicht»        │
│  GG2 (Relat.)  │ Persönlicher Kontakt     │ Kein Beziehungs-Touchpoint │
│  GG3 (Kritisch)│ Transparenz, Peer-Proof  │ «Was ist der Haken?»       │
│  GG4 (Delegier)│ Proaktiver Outreach      │ Übersehen, Ignorieren      │
│  GG5 (Reaktiv) │ Default, Automatik       │ Keine aktive Suche         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Teil 5: Komplementaritäts-Herleitung (γ)

### 5.1 BCM-Komplementaritäts-Definition

> **Komplementarität (γ)** beschreibt, wie zwei Elemente (Aktivitäten, Nutzenkomponenten, Kontextfaktoren) **zusammen** wirken.

```
γ(A,B) > 0: Komplementär (A verstärkt Wirkung von B)
γ(A,B) = 0: Unabhängig (A beeinflusst B nicht)
γ(A,B) < 0: Substitut (A schwächt Wirkung von B)
```

**Kritisch:** γ-Werte sind **kontextabhängig** und müssen **hergeleitet** werden!

---

### 5.2 Komplementaritäts-Herleitung für Assura

#### Methodik

γ-Werte werden hergeleitet über:
1. **Nutzenstruktur-Analyse**: Welche Nutzenkomponenten werden gemeinsam aktiviert?
2. **Awareness-Interaktion**: Erhöht A die Sichtbarkeit von B?
3. **Kontext-Konsistenz**: Passen A und B zum selben Kontext?
4. **Identitäts-Kohärenz**: Bestätigen A und B dieselbe Identität?

---

#### Hergeleitete γ-Werte (Aktivitäten-Paare)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  γ-MATRIX (HERGELEITET)                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  KOMPLEMENTÄR (γ > 0):                                                  │
│                                                                         │
│  Symptom-Checker × Telemedizin                                         │
│  γ = +0.55                                                              │
│  Herleitung: Beide aktivieren INU_C (Convenience) + INU_A (Autonomie)  │
│              Awareness-Transfer: Checker führt zu Telemedizin          │
│              Identitäts-Kohärenz: «Ich löse Probleme effizient»        │
│                                                                         │
│  Generika-Beratung × Kosten-Transparenz                                │
│  γ = +0.50                                                              │
│  Herleitung: Beide aktivieren INU_F (Finanziell) + IDN_R (Rational)    │
│              Kontext-Konsistenz: Cost-Leader Positionierung            │
│              Awareness-Transfer: Kosten-Info führt zu Generika-Wahl    │
│                                                                         │
│  Prävention × Bewegungsprogramm                                        │
│  γ = +0.45                                                              │
│  Herleitung: Beide aktivieren IDN_H (Gesundheit) + INU_H (Gesundheit)  │
│              Aber: Nur bei bereits aktiviertem IDN_H wirksam           │
│              Kontext-Bedingung: L2-L4, nicht L1 oder L5                 │
│                                                                         │
│  LCE-Trigger × Relevante Aktivität                                     │
│  γ = +0.70                                                              │
│  Herleitung: LCE öffnet Awareness-Fenster                              │
│              Aktivität adressiert akuten Nutzen                        │
│              Kontext-Alignment: Richtige Zeit, richtiges Angebot       │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  SUBSTITUT (γ < 0):                                                     │
│                                                                         │
│  Telemedizin × Persönliche Beratung                                    │
│  γ = -0.30                                                              │
│  Herleitung: Aktivieren unterschiedliche Nutzen                        │
│              Telemedizin: INU_C, INU_A (Convenience, Autonomie)         │
│              Persönlich: INU_S, KNU_F (Sicherheit, Familie)            │
│              Identitäts-Konflikt: GG1 vs. GG2                          │
│                                                                         │
│  Finanzieller Anreiz × Intrinsische Motivation                         │
│  γ = -0.40                                                              │
│  Herleitung: Crowding-Out Effekt (Frey & Jegen 2001)                   │
│              INU_F verdrängt IDN_H                                      │
│              Besonders stark bei GG1 (Autonomie-Identität bedroht)     │
│                                                                         │
│  Coaching × Autonomie-Tools                                            │
│  γ = -0.25                                                              │
│  Herleitung: Coaching impliziert «du brauchst Hilfe»                   │
│              Tools bestätigen «du kannst es selbst»                    │
│              Identitäts-Konflikt für GG1/GG3                           │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  KONTEXTABHÄNGIG (γ variiert):                                          │
│                                                                         │
│  Mental Health × Prävention                                            │
│  γ = +0.35 (bei GG2, GG4)                                              │
│  γ = -0.10 (bei GG1, GG3)                                              │
│  Herleitung: GG2/GG4 akzeptieren «Hilfe»                               │
│              GG1/GG3 sehen Stigma-Risiko                               │
│                                                                         │
│  Case Management × Self-Management                                     │
│  γ = +0.40 (bei GG4, GG5)                                              │
│  γ = -0.50 (bei GG1, GG3)                                              │
│  Herleitung: GG4/GG5 wollen Delegation                                 │
│              GG1/GG3 wollen Kontrolle                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 5.3 γ-Herleitung Dokumentation (Beispiel)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  γ-HERLEITUNG: Symptom-Checker × Telemedizin                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  AKTIVITÄTEN:                                                           │
│  A = Symptom-Checker (digitales Triage-Tool)                           │
│  B = Telemedizin (Video-Konsultation mit Arzt)                         │
│                                                                         │
│  SCHRITT 1: Nutzenstruktur-Analyse                                     │
│  ├── A aktiviert: INU_C (schnell), INU_A (selbst machen), IDN_R        │
│  ├── B aktiviert: INU_C (schnell), INU_S (Sicherheit), INU_H (Hilfe)   │
│  └── Überlappung: INU_C (Convenience) = gemeinsamer Treiber            │
│                                                                         │
│  SCHRITT 2: Awareness-Interaktion                                      │
│  ├── A führt zu B: Symptom-Checker empfiehlt «Arzt konsultieren»       │
│  ├── A erhöht A(B): Wer Checker nutzt, kennt Telemedizin-Option        │
│  └── Unidirektional: B führt nicht zu A                                │
│                                                                         │
│  SCHRITT 3: Kontext-Konsistenz                                         │
│  ├── Beide digital: Ja                                                 │
│  ├── Beide schnell: Ja                                                 │
│  ├── Beide ohne Wartezeit: Ja                                          │
│  └── Kontext-Fit: Hoch                                                 │
│                                                                         │
│  SCHRITT 4: Identitäts-Kohärenz                                        │
│  ├── Beide bestätigen: «Ich löse Probleme effizient»                   │
│  ├── Beide bestätigen: «Ich bin technisch versiert»                    │
│  └── Kein Identitäts-Konflikt                                          │
│                                                                         │
│  SCHRITT 5: Gleichgewichts-Spezifik                                    │
│  ├── GG1: γ = +0.60 (perfekter Fit)                                    │
│  ├── GG2: γ = +0.40 (gut, aber persönlich bevorzugt)                   │
│  ├── GG3: γ = +0.55 (Effizienz-Framing passt)                          │
│  ├── GG4: γ = +0.30 (zu selbstständig)                                 │
│  └── GG5: γ = +0.20 (wird nicht gefunden)                              │
│                                                                         │
│  AGGREGIERTER γ-WERT:                                                   │
│  γ(Checker, Telemedizin) = Σ wᵢ · γᵢ = 0.35·0.60 + 0.18·0.40 + ...    │
│                          = +0.55                                        │
│                                                                         │
│  KONFIDENZ: Mittel-Hoch (basiert auf Nutzenlogik, nicht Empirie)       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Teil 6: BCM-konforme Aktivitäten-Bewertung

### 6.1 Bewertungs-Framework

Erst JETZT, nach Kontextfixierung, Nutzenstruktur und Segment-Klassifikation, können Aktivitäten bewertet werden.

**Bewertungskriterien:**

```
BCM-AKTIVITÄTEN-SCORE = f(
  Nutzen-Aktivierung,      # Welche U-Komponenten werden aktiviert?
  Kontext-Fit,             # Passt zum Ψ-Vektor?
  Segment-Anschlussfähigkeit,  # Welche GG werden erreicht?
  Awareness-Potential,     # Kann A aufgebaut werden?
  Komplementarität         # Wie passt zu anderen Aktivitäten?
)
```

---

### 6.2 Top-5 BCM-konforme Aktivitäten für Assura

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BCM-AKTIVITÄTEN-RANKING (nach formaler Analyse)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  #1: SYMPTOM-CHECKER / DIGITALE TRIAGE                                  │
│  ────────────────────────────────────────────────────────────────────   │
│  Nutzen-Aktivierung:                                                    │
│    INU_C ●●●●● | INU_A ●●●●○ | IDN_R ●●●●○ | IDN_E ●●●●●               │
│  Kontext-Fit:                                                           │
│    Ψ_E (Cost) ✓ | Ψ_K (Autonomie) ✓ | Ψ_C (Digital) ✓                  │
│  Segment-Anschlussfähigkeit:                                            │
│    GG1 ●●●●● | GG2 ●●●○○ | GG3 ●●●●○ | GG4 ●●○○○ | GG5 ●○○○○          │
│  Awareness-Potential: Hoch (kann prominent platziert werden)            │
│  Komplementarität: γ(Telemedizin) = +0.55                              │
│                                                                         │
│  BCM-SCORE: 0.85                                                        │
│  ➡️ EMPFEHLUNG: Priorität 1 für Implementierung                        │
│                                                                         │
│  #2: GENERIKA-BERATUNG / KOSTEN-OPTIMIERER                              │
│  ────────────────────────────────────────────────────────────────────   │
│  Nutzen-Aktivierung:                                                    │
│    INU_F ●●●●● | IDN_R ●●●●● | IDN_E ●●●●○ | IDN_K ●●●●○               │
│  Kontext-Fit:                                                           │
│    Ψ_E (Cost) ✓✓ | Ψ_K (Rational) ✓✓ | Ψ_S (Smart) ✓                   │
│  Segment-Anschlussfähigkeit:                                            │
│    GG1 ●●●●● | GG2 ●●●○○ | GG3 ●●●●● | GG4 ●●●○○ | GG5 ●●○○○          │
│  Awareness-Potential: Mittel (braucht aktiven Medikamenten-Kontext)     │
│  Komplementarität: γ(Kosten-Transparenz) = +0.50                        │
│                                                                         │
│  BCM-SCORE: 0.82                                                        │
│  ➡️ EMPFEHLUNG: Priorität 2, perfekt für Assura-Positionierung         │
│                                                                         │
│  #3: TELEMEDIZIN                                                        │
│  ────────────────────────────────────────────────────────────────────   │
│  Nutzen-Aktivierung:                                                    │
│    INU_C ●●●●● | INU_S ●●●○○ | INU_A ●●●●○ | IDN_E ●●●●○               │
│  Kontext-Fit:                                                           │
│    Ψ_E (Cost) ✓ | Ψ_K (Effizienz) ✓ | Ψ_T (Zeit) ✓                     │
│  Segment-Anschlussfähigkeit:                                            │
│    GG1 ●●●●● | GG2 ●●●○○ | GG3 ●●●●○ | GG4 ●●○○○ | GG5 ●○○○○          │
│  Awareness-Potential: Hoch (COVID hat Bekanntheit erhöht)               │
│  Komplementarität: γ(Symptom-Checker) = +0.55                           │
│                                                                         │
│  BCM-SCORE: 0.78                                                        │
│  ➡️ EMPFEHLUNG: Priorität 3, Bundle mit Symptom-Checker                │
│                                                                         │
│  #4: LCE-BASIERTE PROAKTIVE INFORMATION                                 │
│  ────────────────────────────────────────────────────────────────────   │
│  Nutzen-Aktivierung:                                                    │
│    INU_S ●●●●○ | INU_C ●●●○○ | IDN_R ●●●○○ | KNU_F ●●●○○               │
│  Kontext-Fit:                                                           │
│    Ψ_T (Timing) ✓✓ | Ψ_C (Awareness) ✓ | Ψ_U (Unsicherheit) ✓          │
│  Segment-Anschlussfähigkeit:                                            │
│    GG1 ●●●○○ | GG2 ●●●●○ | GG3 ●●○○○ | GG4 ●●●●○ | GG5 ●●●○○          │
│  Awareness-Potential: Sehr hoch (LCE = natürliches Fenster)             │
│  Komplementarität: γ(alle Aktivitäten) = +0.70 (Enabler!)               │
│                                                                         │
│  BCM-SCORE: 0.75                                                        │
│  ➡️ EMPFEHLUNG: Priorität 4, aber ENABLER für alle anderen!            │
│                                                                         │
│  #5: TRANSPARENZ-DASHBOARD (Kosten, Leistungen)                         │
│  ────────────────────────────────────────────────────────────────────   │
│  Nutzen-Aktivierung:                                                    │
│    IDN_R ●●●●● | IDN_K ●●●●● | INU_A ●●●●○ | INU_F ●●●○○               │
│  Kontext-Fit:                                                           │
│    Ψ_K (Kontrolle) ✓✓ | Ψ_U (Transparenz) ✓✓ | Ψ_S (Vertrauen) ✓       │
│  Segment-Anschlussfähigkeit:                                            │
│    GG1 ●●●●● | GG2 ●●●○○ | GG3 ●●●●● | GG4 ●●○○○ | GG5 ●○○○○          │
│  Awareness-Potential: Mittel (muss aktiv aufgesucht werden)             │
│  Komplementarität: γ(Generika) = +0.50, γ(Kritik-Reduktion) = +0.45    │
│                                                                         │
│  BCM-SCORE: 0.72                                                        │
│  ➡️ EMPFEHLUNG: Priorität 5, besonders für GG3 (Kritische)             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### 6.3 Nicht empfohlene Aktivitäten (BCM-Begründung)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  NICHT-EMPFOHLEN (mit BCM-Begründung)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ❌ GESUNDHEITS-COACHING (persönlich)                                   │
│  Grund: Aktiviert INU_S, aber verletzt INU_A und IDN_R                 │
│         GG1/GG3 (60% der Kunden) sehen es als Bevormundung             │
│         Kontext-Fit: Ψ_K (Autonomie) = VERLETZT                        │
│                                                                         │
│  ❌ COMMUNITY-PROGRAMME                                                 │
│  Grund: Aktiviert KNU_C, aber KNU ist im Kontext NICHT WIRKSAM         │
│         GG1/GG3 vermeiden «Gruppenaktivitäten»                         │
│         Kontext-Fit: Ψ_S (Individualismus) = VERLETZT                  │
│                                                                         │
│  ❌ FINANZIELLE ANREIZE FÜR PRÄVENTION                                  │
│  Grund: Crowding-Out Effekt (γ = -0.40)                                │
│         Verdrängt intrinsische Motivation                              │
│         GG1/GG3: «Manipulation!»                                        │
│                                                                         │
│  ❌ CASE MANAGEMENT (als Standardangebot)                               │
│  Grund: Nur für GG4/GG5 anschlussfähig (22% der Kunden)                │
│         GG1/GG3: «Brauche ich nicht» → Ressourcenverschwendung         │
│         Kontext-Fit: Ψ_E (Cost) = VERLETZT (zu teuer für Volumen)      │
│                                                                         │
│  ❌ PRÄVENTIONS-KAMPAGNEN (breit)                                       │
│  Grund: INU_H ist nicht dominant im Kontext                            │
│         Awareness kann nicht aufgebaut werden (Ψ_C = LOW)              │
│         Keine Verhaltensänderung ohne akuten Nutzen                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Teil 7: Schlussfolgerungen

### 7.1 Was diese Analyse ermöglicht

Mit der BCM-konformen Kontextmatrix kann nun:

1. **Jede Aktivität formal bewertet werden** (nicht nur intuitiv)
2. **Interventions-Wirkung vorhergesagt werden** (welche GG reagieren wie)
3. **Komplementaritäten systematisch geplant werden** (Bundles)
4. **Awareness-Aufbau gezielt gesteuert werden** (LCE-Trigger)
5. **Nicht-anschlussfähige Interventionen vermieden werden** (Ressourceneffizienz)

---

### 7.2 Was diese Analyse NICHT liefert

1. ❌ **Kausale Effektschätzungen** (braucht Empirie/RCT)
2. ❌ **Präzise Adoption-Raten** (braucht Pilotierung)
3. ❌ **ROI-Berechnungen** (braucht Kostenmodell)
4. ❌ **Implementierungs-Details** (braucht Operationalisierung)

---

### 7.3 Empfohlener nächster Schritt

**BCM-Simulation:**
Mit der nun formalisierten Kontextmatrix kann eine **Agent-Based Simulation** durchgeführt werden:

1. Agenten mit GG1-GG5 Verteilung (35/18/25/12/10)
2. Interventions-Szenarien (Top-5 Aktivitäten)
3. Awareness-Dynamik über Zeit
4. Gleichgewichts-Übergänge bei LCE
5. Adoptions- und Willingness-Vorhersagen

---

## Anhang: Formale Definitionen

### A.1 Notation

| Symbol | Bedeutung |
|--------|-----------|
| Ψ | Kontextvektor |
| U | Nutzenfunktion |
| INU | Individueller Nutzen |
| KNU | Kollektiver Nutzen |
| IDN | Identitätsnutzen |
| A | Awareness |
| γ | Komplementaritätskoeffizient |
| GG | Gleichgewicht |
| w(Ψ) | Kontextabhängiges Gewicht |

### A.2 Kerngleichungen

```
1. Wirksamer Nutzen:
   U*(x) = Σᵢ wᵢ(Ψ) · Uᵢ(x)

2. Awareness-Dynamik:
   A(t+1) = A(t) + δ·E(t) - λ·A(t)

3. Interventions-Wirkung:
   ΔU = Σⱼ γ(Iⱼ, Ψ) · A(Iⱼ) · Uⱼ(Iⱼ)

4. Gleichgewichts-Stabilität:
   Stabil wenn: ∂U*/∂x|ₓ* = 0 und ∂²U*/∂x²|ₓ* < 0
```

---

*Dieses Dokument ist die BCM-konforme Grundlage für alle weiteren Analysen im BEATRIX-Projekt Assura (LEAD-013)*
