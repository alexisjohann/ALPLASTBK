# Theory Catalog: 191 Theorien in 31 Kategorien

> **SSOT:** `data/theory-catalog.yaml`
> **Upload-Tags:** canonical, theory, catalog, ebf, ssot
> **Prioritaet:** HOCH — erklaert welche wissenschaftlichen Theorien BEATRIX kennt

---

## Was ist der Theory Catalog?

Der Theory Catalog ist die **strukturierte Sammlung aller wissenschaftlichen Theorien**, die das EBF Framework integriert. Jede Theorie hat:
- Eine eindeutige ID (MS-XX-XXX Format)
- EBF-Restriktionen (wie die Theorie ins Framework passt)
- Validitaetsbereich (wo die Theorie gilt)
- Verknuepfung zu Papers (via bib_keys)

---

## Die 31 Kategorien

| CAT | Name | Beispiel-Theorien |
|-----|------|-------------------|
| CAT-01 | Classical Economics | Arrow-Debreu, Expected Utility, CAPM |
| CAT-02 | Social Preferences | Inequity Aversion (Fehr & Schmidt), Reciprocity |
| CAT-03 | Reference Dependence | Prospect Theory (Kahneman & Tversky), Endowment Effect |
| CAT-04 | Time Preferences | Hyperbolic Discounting, Rational Addiction |
| CAT-05 | Identity & Beliefs | Identity Economics (Akerlof & Kranton) |
| CAT-06 | Institutions | Ostrom Commons, Property Rights |
| CAT-07 | Information | Asymmetric Information, Signaling |
| CAT-08 | Strategic Interaction | Nash Equilibrium, Mechanism Design |
| CAT-09 | Behavioral Finance | Overconfidence, Disposition Effect |
| CAT-10 | Nudge & Choice Architecture | Default Effects, Libertarian Paternalism |
| CAT-11 | Neuroeconomics & Dual Systems | System 1/2, Somatic Marker |
| CAT-12 | Wellbeing & Happiness | Easterlin Paradox, Set-Point Theory |
| CAT-13 | Development & Poverty | Poverty Traps, Microfinance |
| CAT-14 | Causal Inference & Heterogeneity | Treatment Effects, Mediation |
| CAT-15 | Mechanism Design & Causal ML | Causal Forests, Policy Learning |
| CAT-16 | Sequential Causal Inference | Adaptive Experiments |
| CAT-17 | Household Economics & Time Allocation | Becker Time Allocation |
| CAT-18 | Econometric Causality Foundations | Heckman Causality Framework |
| CAT-19 | Skill Formation & Human Capital | Technology of Skill Formation |
| CAT-20 | Labor Market & Migration Economics | Places vs People Framework |
| CAT-21 | Political Psychology & Authoritarianism | RWA, Social Dominance |
| CAT-22 | Moral Reasoning & Ethics | Context-Dependent Moral Reasoning |
| CAT-23 | Virtue Ethics & Character Development | Heckman Virtue Ethics |
| CAT-24 | Crisis Management & Online Communication | Firestorm Detection |
| CAT-25 | AI Consumer Experience | AI Capabilities Framework |
| CAT-26 | Customer Experience & Journey Management | Journey Segments |
| CAT-27 | Entrepreneurship & Innovation | Pragmatist Entrepreneurship |
| CAT-28 | Technology, Power & Institutional Direction | AI Governance |
| CAT-29 | Infrastructure Economics & NIMBY | Public Investment |
| CAT-30 | Voting Theory & Social Choice | QRE, Consensus Formation |
| CAT-31 | Replication Science & Methodology Quality | Replicability |

---

## Das ID-Format: MS-XX-XXX

```
MS = Model Space (Appendix MS)
XX = Kategorie-Kuerzel (2 Buchstaben)
XXX = Laufnummer (3 Ziffern)
```

Beispiele:
- **MS-RD-001** = Prospect Theory (Reference Dependence)
- **MS-SP-001** = Inequity Aversion (Social Preferences)
- **MS-TP-001** = Quasi-Hyperbolic Discounting (Time Preferences)
- **MS-IB-001** = Identity Economics (Identity & Beliefs)

---

## Was jede Theorie enthaelt

| Feld | Erklaerung |
|------|------------|
| `id` | Eindeutige ID (MS-XX-XXX) |
| `name` | Name der Theorie |
| `authors` | Hauptautoren |
| `year` | Erstpublikation |
| `ebf_restrictions` | Wie die Theorie ins EBF passt |
| `validity` | Wo die Theorie gilt (und wo nicht!) |
| `bib_keys` | Verknuepfte Papers in der Bibliographie |

---

## EBF-Restriktionen: Was bedeutet das?

Jede Theorie im EBF hat **Restriktionen** — Bedingungen unter denen sie gilt:

```yaml
# Beispiel: Prospect Theory (MS-RD-001)
ebf_restrictions:
  C_ij: 0           # Keine Komplementaritaet
  lambda: "> 1"     # Loss Aversion muss groesser 1 sein
  alpha: "< 1"      # Diminishing Sensitivity
```

```yaml
# Beispiel: Inequity Aversion (MS-SP-001)
ebf_restrictions:
  C_ij: "!= 0"      # Komplementaritaet aktiv
  beta_envy: "> alpha_guilt"  # Neid staerker als Schuld
```

---

## Die Top-5 Theorien fuer BEATRIX

| Theorie | ID | Wann relevant? |
|---------|-----|---------------|
| **Prospect Theory** | MS-RD-001 | Bei JEDER Entscheidung unter Unsicherheit |
| **Inequity Aversion** | MS-SP-001 | Bei sozialen Vergleichen, Fairness |
| **Identity Economics** | MS-IB-001 | Bei Identitaet, Zugehoerigkeit, Normen |
| **Default Effects** | MS-NU-002 | Bei Choice Architecture, Opt-in/Opt-out |
| **Hyperbolic Discounting** | MS-TP-001 | Bei Zeitpraeferenzen, Prokrastination |

---

## Wie Theorien mit Papers verknuepft sind

```
Theory Catalog (data/theory-catalog.yaml)
     │
     │  bib_keys: ["kahneman1979prospect", ...]
     │
     ▼
Paper Database (bibliography/bcm_master.bib)
     │
     │  theory_support = {MS-RD-001, MS-SP-001}
     │
     ▼
Bidirektionale Verknuepfung:
  Theorie → Papers (welche Papers stuetzen diese Theorie?)
  Paper → Theorien (welche Theorien stuetzt dieses Paper?)
```

---

## Warum der Theory Catalog wichtig ist

1. **Keine erfundenen Theorien**: BEATRIX referenziert NUR Theorien aus dem Catalog
2. **EBF-Restriktionen**: Jede Theorie hat klare Grenzen — wird nicht ueber-generalisiert
3. **Paper-Verknuepfung**: Jede Theorie ist empirisch fundiert (via bib_keys)
4. **Modell-Design**: Beim Modell-Bau werden passende Theorien aus dem Catalog gewaehlt

---

*Quelle: data/theory-catalog.yaml (v1.22, 191 Theorien, 31 Kategorien)*
