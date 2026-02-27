# Qualitätsdimensionen für EBF Appendices

## Übersicht

Jede Appendix wird auf 5 Dimensionen bewertet (TERAN-Framework):
- **T**heory (25%)
- **E**vidence (30%)  
- **R**igor (15%)
- **A**pplicability (15%)
- **N**ovelty/Transparency (15%)

## Dimension T: Theoretische Fundierung (25%)

### Subdimensionen (max 10 Punkte)

| Sub | Beschreibung | Max |
|-----|--------------|-----|
| T1 | Literaturanbindung: Schlüsselwerke korrekt zitiert | 2 |
| T2 | Axiomatische Konsistenz: Widerspruchsfrei | 2 |
| T3 | Vollständigkeit: Gegenstandsbereich abgedeckt | 1 |
| T4 | Minimalität: Redundanz eliminiert | 1 |
| T5 | Beweise: Theoreme bewiesen oder referenziert | 2 |
| T6 | Neuheit: Beitrag vs. Literatur klar | 2 |

### Anker
- 10: Neue Theoreme mit Beweisen
- 8: Gute Literaturanbindung, konsistente Axiome
- 6: Literatur zitiert, aber Lücken
- 4: Oberflächliche Literatur
- 2: Kaum Fundierung

## Dimension E: Empirische Verankerung (30%)

### Subdimensionen (max 10 Punkte)

| Sub | Beschreibung | Max |
|-----|--------------|-----|
| E1 | Datenquellen: Echte Daten verwendet | 3 |
| E2 | Kalibrierung: Parameter empirisch fundiert | 3 |
| E3 | Validierung: Tests der Vorhersagen | 2 |
| E4 | Falsifizierbarkeit: Testbar | 1 |
| E5 | Robustheit: Über Spezifikationen stabil | 1 |

### Anker
- 10: Eigene Daten, RCT, Out-of-sample Tests
- 8: Sekundärdaten, gute Identifikation
- 6: Parameter aus Literatur, plausibel
- 4: Einige Referenzen, keine Analyse
- 2: Nur illustrative Zahlen

### BCM-Spezifisch
- Fehlende CFA für neue Konstrukte: Max 4/10
- >50% ILL-Parameter ohne Tag: Max 3/10

## Dimension R: Formale Präzision (15%)

### Subdimensionen (max 10 Punkte)

| Sub | Beschreibung | Max |
|-----|--------------|-----|
| R1 | Notation: Konsistent | 2 |
| R2 | Definitionen: Eindeutig | 2 |
| R3 | Beweise: Lückenlos | 3 |
| R4 | Mathematik: Korrekt | 3 |

## Dimension A: Anwendbarkeit (15%)

### Subdimensionen (max 10 Punkte)

| Sub | Beschreibung | Max |
|-----|--------------|-----|
| A1 | Worked Examples: Realistisch | 3 |
| A2 | Implementierbarkeit: Umsetzbar | 3 |
| A3 | Skalierbarkeit: Für reale Größen | 2 |
| A4 | Datenerfordernis: Erhebbar | 2 |

## Dimension N: Epistemic Transparency (15%)

### Subdimensionen (max 10 Punkte)

| Sub | Beschreibung | Max |
|-----|--------------|-----|
| N1 | Status-Tags: Alle Parameter getaggt | 3 |
| N2 | Etabliert/Neu: Klar getrennt | 3 |
| N3 | Peer-Review: Referenzen klassifiziert | 2 |
| N4 | Limitations: Grenzen diskutiert | 2 |

## Score-Berechnung

```
Quality = 0.25*T + 0.30*E + 0.15*R + 0.15*A + 0.15*N
```

| Score | Sterne | Label |
|-------|--------|-------|
| 9.0+ | ★★★★★ | Publication Ready |
| 7.0-8.9 | ★★★★☆ | Minor Revisions |
| 5.0-6.9 | ★★★☆☆ | Working Paper |
| 3.0-4.9 | ★★☆☆☆ | Draft |
| <3.0 | ★☆☆☆☆ | Concept |
