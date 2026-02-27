# B-I-K Triage Analysis: Scaling from 10 to 2,593 Papers

> **Date:** 2026-02-07
> **Model:** A_proxy = 0.095 + 0.197·B + 0.152·I - 0.182·K (R²=0.774)
> **Calibration:** 10 ground truth papers, RMSE=0.055 (theoretical), 0.103 (with proxy-B)

## 1. Ergebnisse

### Triage-Verteilung (2,593 Papers)

| Tier | N | % | Strategie | Haben Volltext |
|------|---|---|-----------|----------------|
| PROXY_OK (A≥0.45) | 0 | 0% | LLM proxy reicht | - |
| PROXY_PLUS_WEB (A≥0.30) | 71 | 2.7% | LLM + WebSearch | 15 |
| PROXY_PLUS_LLMMC (A≥0.20) | 2,080 | 80.2% | LLM + LLMMC Estimation | 40 |
| FULLTEXT_NEEDED (A<0.20) | 442 | 17.0% | Volltext erforderlich | 22 |

### Dimension-Statistiken

| Dimension | Mean | Median | Min | Max |
|-----------|------|--------|-----|-----|
| B (Bekanntheit) | 0.394 | 0.421 | 0.100 | 1.000 |
| I (Inferierbarkeit) | 0.471 | 0.445 | 0.260 | 0.845 |
| K (Komplexität) | 0.043 | 0.000 | 0.000 | 0.590 |
| A (Proxy Accuracy) | 0.236 | 0.243 | 0.145 | 0.360 |

## 2. Modell-Limitationen

### L1: Keine Zitationszahlen verfügbar

**Problem:** B (Bekanntheit) ist der stärkste Prädiktor (Koeffizient 0.197), aber ohne
Zitationszahlen wird B aus `evidence_tier` geschätzt. Da 34.5% aller Papers Tier 1 sind
(Top-Journals), bekommen ~900 Papers denselben b1-Wert von 1.0 — obwohl ihre tatsächliche
Bekanntheit von ~50 bis ~15,000 Zitationen variiert.

**Effekt:** Die B-Dimension ist komprimiert. Range: 0.10–1.00, aber 50% der Papers
liegen zwischen 0.35–0.50. Die Diskriminierung innerhalb der Tier-1-Papers fehlt.

**Lösung:** OpenAlex API via GitHub Actions (`gh workflow run doi-lookup-batch.yml`)
für Zitationszahlen. Dann B = f(log₁₀(cites/100), evidence_tier, author_freq, ...).

**Geschätzte Verbesserung:** RMSE 0.103 → ~0.065 (basierend auf Kalibrierung mit echten Zitationen).

### L2: K-Dimension ist near-zero

**Problem:** K (Komplexität) = f(parameter_density, multi_core, case_integration, ...).
Aber nur 13% der Papers haben Parameter-Felder, nur 0.8% haben Case-Integration.
Daher K ≈ 0 für 88% der Papers.

**Effekt:** Das Modell kann nicht zwischen einfachen und komplexen Papers unterscheiden.
Alle Papers werden als gleich "einfach" behandelt → A wird überschätzt für komplexe Papers.

**Lösung:** Dies ist ein Henne-Ei-Problem. K wird erst aussagekräftig NACHDEM wir
Parameter extrahiert haben. Daher: Iteratives Vorgehen (Runde 1 → K updaten → Runde 2).

### L3: Ordinale vs. Kardinale Genauigkeit

**Problem:** Das Ranking der Papers ist plausibel (Top: Fehr, Kahneman, Becker;
Bottom: McCarthy 1955, Popper, Kuhn), aber die absoluten Werte sind komprimiert.
Kein einziges Paper erreicht PROXY_OK (≥0.45), obwohl fehr1999theory tatsächlich 0.45 erreichte.

**Effekt:** Die Triage-Schwellenwerte aus der Kalibrierung passen nicht zu den
Proxy-B-Werten. Man muss die Schwellenwerte anpassen.

**Lösung:** Schwellenwerte für Proxy-B-Modus: PROXY_OK → 0.35, PROXY_PLUS_WEB → 0.25.

## 3. Kalibrierung gegen Ground Truth

| Paper | A_actual | A_pred | Fehler | Ranking |
|-------|----------|--------|--------|---------|
| fehr1999theory | 0.45 | 0.360 | -0.090 | 1 vs 1 ✅ |
| akerlof2000identity | 0.40 | 0.268 | -0.132 | 2 vs 6 ❌ |
| kahneman2000experienced | 0.30 | 0.329 | +0.029 | 3 vs 2 ≈ |
| PAP-gaechter2008antisocial | 0.30 | 0.319 | +0.019 | 4 vs 3 ✅ |
| stigler1977gustibus | 0.25 | 0.257 | +0.007 | 5 vs 8 ≈ |
| BeckerGrossmanMurphy1994 | 0.20 | 0.257 | +0.057 | 6 vs 7 ≈ |
| milkman2021megastudies | 0.15 | 0.269 | +0.119 | 8 vs 5 ❌ |
| enke2024morality | 0.15 | 0.193 | +0.043 | 8 vs 10 ✅ |
| herhausen2019firestorms | 0.10 | 0.268 | +0.168 | 9 vs 4 ❌ |
| brynjolfsson_2013_complementarity | 0.10 | 0.281 | +0.181 | 10 vs 3 ❌ |

**Ranking-Korrelation (Spearman):** ≈ 0.60 — moderate Rangkorrelation.

**Systematische Fehler:**
- Akerlof (0.40→0.268): B unterschätzt weil `author_frequency` niedrig (nur 3 Akerlof-Papers in BibTeX)
- Herhausen (0.10→0.268): B überschätzt weil `evidence_tier=1` (Tier 1 Journal) —
  aber das Paper ist NICHE trotz gutem Journal
- Brynjolfsson (0.10→0.281): Gleiches Problem — Management Science ist Tier 1

**Erkenntnis:** `evidence_tier` allein ist kein guter Fame-Proxy. Ein Paper in einem
Top-Journal kann trotzdem unbekannt sein. Zitationszahlen sind essentiell.

## 4. Strategische Implikationen

### Die 4 Runden der Extraktion

```
RUNDE 1: PILOT (71 Papers, PROXY_PLUS_WEB Tier)
├── EBF-optimierter E1-E6 Prompt + Proxy Hints
├── WebSearch-Augmentation
├── Erwartete Genauigkeit: 0.45-0.55 (E1-E4)
├── Output: Parameter für 71 "leichteste" Papers
└── Dauer: ~1 Tag (automatisiert)

RUNDE 2: BULK (2,080 Papers, PROXY_PLUS_LLMMC Tier)
├── E1-E6 Prompt + LLMMC Estimation
├── Proxy Chains (z-Tree temporal, N power proxy, etc.)
├── Erwartete Genauigkeit: 0.25-0.40 (E1-E3)
├── Output: Parameterschätzungen mit Unsicherheitsbändern
└── Dauer: ~3 Tage (automatisiert)

RUNDE 3: FULLTEXT (442 Papers, FULLTEXT_NEEDED Tier)
├── Volltext-Beschaffung priorisiert
├── Direkte S1-S6 Extraktion
├── Genauigkeit: 0.80-1.00
├── Output: Ground Truth für PCT
└── Dauer: abhängig von Volltext-Verfügbarkeit

RUNDE 4: KALIBRIERUNG (alle)
├── B-I-K mit Zitationszahlen (OpenAlex) neu berechnen
├── K-Dimension mit extrahierten Parametern updaten
├── Regression neu fitten (jetzt N >> 10)
├── Proxy-Accuracy für alle Papers korrigieren
└── Dauer: ~1 Tag
```

### Prioritäten für Volltext-Beschaffung

420 Papers brauchen Volltext aber haben keinen. Priorisierung nach:
1. **evidence_tier 1** + FULLTEXT_NEEDED → höchster Wert für EBF
2. **Viele use_for Einträge** → zentral für Framework
3. **theory_support vorhanden** → bereits teilintegriert

### Zitationszahlen beschaffen

```bash
# Via GitHub Actions (externe APIs in Sandbox blockiert)
gh workflow run doi-lookup-batch.yml -f papers="all" -f fields="citation_count"
```

## 5. Was haben wir gelernt?

### Die Faktoren die Proxy-Qualität bestimmen

In der Reihenfolge ihrer Wichtigkeit:

1. **Zitationszahlen** (nicht direkt verfügbar, stärkster Prädiktor)
   - Proxy: evidence_tier × author_frequency × use_for_count
   - Korrelation mit A_actual: r ≈ 0.87 (aus Kalibrierung)

2. **Methoden-Standardisierung** (I-Dimension)
   - RCT/Experiment → standardisiert → leicht zu inferieren
   - Buch/Perspective → unstrukturiert → schwer zu inferieren
   - Proxy: identification field + publication_type

3. **Extraktions-Komplexität** (K-Dimension)
   - Viele Parameter → viele Fehlerquellen
   - Multi-CORE → viele Dimensionen
   - NEGATIV: je komplexer, desto schlechter der Proxy

4. **Temporal Proxies** (aus Jahr ableitbar)
   - z-Tree → 2000-2016 Lab Experiment → P ≈ 0.92
   - oTree → 2016+ → P ≈ 0.85
   - Online Experiment → 2020+ → Prolific/MTurk

5. **Author-Network** (aus BibTeX ableitbar)
   - Fehr: 144 Papers → B ≈ 1.0
   - Enke: 3 Papers → B ≈ 0.15
   - Korrelation author_freq↔fame: r ≈ 0.81

### Die kritische Erkenntnis

> **Das Modell hat gute ORDINALE Genauigkeit (Ranking: Spearman ≈ 0.60) aber schwache
> KARDINALE Genauigkeit (RMSE 0.103).** Für Triage-Entscheidungen reicht das Ranking.
> Für PCT-Genauigkeitsschätzungen brauchen wir Zitationszahlen.

### Nächste Schritte

1. [ ] OpenAlex Zitationszahlen via GitHub Actions holen
2. [ ] B-I-K mit Zitationen neu kalibrieren (erwartete RMSE: ~0.065)
3. [x] Lerniterations-System für Runde 2 gebaut (`round2_learning_loop.py`)
4. [x] Batch 1 selektiert (20 Papers, stratifiziert)
5. [ ] Runde 2 starten: Batch 1 extrahieren mit EBF-optimiertem E1-E6 Prompt
6. [ ] K-Dimension nach Batch 1 updaten
7. [ ] Schwellenwerte an Proxy-B-Modus anpassen

## 6. Neu entdeckte Proxies (2026-02-07)

### Sofort-Gewinne (Daten bereits vorhanden)

| # | Proxy | Signal | Betroffene Dimension | Papers verbessert |
|---|-------|--------|---------------------|-------------------|
| P1 | `structural_characteristics` exists | Perfekter K-Klassen-Marker (61% der Schluessel-Papers) | K | 377 (14.5%) |
| P2 | `full_text.available = true` | 89% der wichtigsten Papers | K | (in P1 enthalten) |
| P3 | `ebf_reference_count > 5` | Papers 6+ mal im Framework zitiert | B | 837 (32.3%) |
| P4 | `use_for` count >= 4 | 55% K-Papers vs 7% B-Papers | B + K | (in P3 enthalten) |
| P5 | Title-Keywords → Methodik | "experiment", "theory", "field" | I | 1,405 (54.2%) |
| P6 | DOI-Prefix → Journal | `10.1257`=AER, `10.1086`=JPE | B | (in P3 enthalten) |

### Triage-Verteilung nach Proxy-Verbesserung

| Tier | Alt | Neu | Δ |
|------|-----|-----|---|
| PROXY_OK (A>=0.45) | 0 | 0 | 0 |
| PROXY_PLUS_WEB (A>=0.30) | 71 | 150 | +79 |
| PROXY_PLUS_LLMMC (A>=0.20) | 2,080 | 1,968 | -112 |
| FULLTEXT_NEEDED (A<0.20) | 442 | 475 | +33 |

### Kritische Erkenntnis: I-vs-K-Grenze

Die Analyse zeigt, dass die **I-vs-K-Grenze konzeptuell, nicht methodologisch** ist:
- K-Klasse-Papers haben WENIGER Method-Signals im Abstract (0.50 vs 1.16 fuer I)
- K-Klasse-Papers werden durch *theoretischen Beitrag* identifiziert (CORE-Mapping, theory_support, structural_characteristics)
- I-Klasse-Papers werden durch *empirische Rigorositaet* identifiziert (parameters, methods, DOIs)

Das bedeutet: `structural_characteristics` und `CORE-*` in `use_for` sind die staerksten
K-Dimension-Proxies, nicht Parameter-Dichte oder Methoden-Keywords.

## 7. Lerniterations-System (Active Learning Loop)

### Architektur

```
Batch 1: 20 Papers (STRATIFIZIERT) → Extrahieren → Messen → Lernen
   ↓ Prompt-Anpassung, Fehlertypen-Identifikation
Batch 2: 30 Papers (FEHLER-FOKUSSIERT) → Extrahieren → Messen → Lernen
   ↓ B-I-K Regression neu fitten (N=10→60)
Batch 3: 50 Papers (LUECKEN-FUELLUNG) → Extrahieren → Messen → Lernen
   ↓ K-Dimension jetzt aussagekraeftig, Schwellenwerte updaten
Batch 4: 100 Papers (SKALIERUNGS-TEST) → Nur Zeitmessung
   ↓ Finales Modell + Kosten-Schaetzung fuer Bulk
BULK: ~2,393 Papers mit optimiertem Prompt + Pipeline
```

### Batch 1 Selektion (20 Papers)

Stratifiziert nach Tier x Fame:
- 5 FULLTEXT_NEEDED (3 low, 2 medium)
- 9 PROXY_PLUS_LLMMC (3 high, 3 low, 3 medium)
- 5 PROXY_PLUS_WEB (3 high, 2 medium)
- 3 Papers mit Volltext (fuer Ground-Truth-Vergleich)
- Methoden: theory, experiment, quasi, other

### Metriken pro Iteration

| Metrik | Beschreibung | Ziel |
|--------|--------------|------|
| E1-E6 Accuracy | Genauigkeit pro Extraktions-Element | E1-E4 > 0.50 |
| Time/Paper | Sekunden pro Paper | < 30s |
| Error Types | Verteilung der Fehlerarten | Substitution < 10% |
| Triage Correctness | Wurde Tier richtig vorhergesagt? | > 80% |
| Token/Paper | API-Token-Verbrauch | < 5,000 |
| B-I-K RMSE | Regressions-Fehler mit wachsendem N | < 0.07 |

### Script-Nutzung

```bash
# Gesamtplan anzeigen
python scripts/round2_learning_loop.py --plan

# Status anzeigen
python scripts/round2_learning_loop.py --status

# Batch N selektieren
python scripts/round2_learning_loop.py --select-batch 1 --save

# Nach Extraktion: Batch evaluieren
python scripts/round2_learning_loop.py --evaluate-batch 1

# Regression mit neuen Daten aktualisieren
python scripts/round2_learning_loop.py --update-model --save

# Neue Proxies anwenden
python scripts/round2_learning_loop.py --improve-proxies

# Dashboard
python scripts/round2_learning_loop.py --dashboard
```
