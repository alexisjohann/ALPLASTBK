# Evidence-Based Framework for Economic and Social Behavior (EBF)

> Automatisch geladener Kontext für Claude Code und andere AI-Assistenten

---

## 🔴 PFLICHT: EBF Model-Building bei JEDER Frage

> ⚠️ **WORK IN PROGRESS (WIP)** - Dieser Workflow ist in aktiver Entwicklung.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ⚠️  BEI JEDER INHALTLICHEN FRAGE - OHNE AUSNAHME!        [WIP v0.1]   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EBF WORKFLOW                                                           │
│                                                                         │
│  SCHRITT 0: Session starten                                             │
│  SCHRITT 1: Kontext verstehen                                           │
│  SCHRITT 2: Modell auswählen                                            │
│  SCHRITT 3: Parameter bestimmen                                         │
│  SCHRITT 4: Analyse & Antwort                                           │
│  SCHRITT 5: Intervention designen (bei Verhaltenszielen)                │
│  SCHRITT 6: Bericht erstellen                                           │
│  SCHRITT 7: Ergebnisse sichern                                          │
│  SCHRITT 8: Qualität prüfen                                             │
│  SCHRITT 9: Output wählen (Format + Umfang)                             │
│                                                                         │
│  SCHRITT 0 KLASSIFIKATION (aus Frage ableiten):                        │
│  ├── "Ist X näher zu Y?" → Analyse → Schritt 5 übersprungen            │
│  └── "Wie bringe ich..." → Verhaltensänderung → Schritt 5 aktiv        │
│                                                                         │
│  MODI:                                                                  │
│  ├── SCHNELL:   10 min, ~800 Worte, direkt 10C, LLMMC                  │
│  ├── STANDARD:  45 min, ~3000 Worte, Registry+Catalog, User-Feedback   │
│  └── TIEF:      2+ Stunden, ~5000 Worte, Monte Carlo, Alternativen     │
│                                                                         │
│  DETAILS: .claude/commands/find-model.md                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Session-Defaults

> Diese Einstellungen gelten für JEDE Session und wurden am 2025-01-25 konfiguriert.

### Modus-Wahl (IMMER zuerst!)

**Bei JEDER inhaltlichen Frage** zeigt Claude zuerst die Modus-Wahl:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Welcher Modus?                                                         │
│                                                                         │
│    ⚡ SCHNELL   - 10 min, keine Rückfragen                              │
│    🎯 STANDARD  - 45 min, Feedback pro Schritt  ← [DEFAULT]             │
│    🔬 TIEF      - 2+ Std, Monte Carlo, Alternativen                     │
│                                                                         │
│  → Enter/OK = STANDARD                                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

**User-Eingaben:**
| Eingabe | Bedeutung |
|---------|-----------|
| `Enter` / `OK` / `Weiter` | STANDARD (Default) |
| `⚡` / `schnell` / `1` | SCHNELL Modus |
| `🔬` / `tief` / `3` | TIEF Modus |

### Kommunikationsstil nach Session-Phase

| Phase | Stil | Grund |
|-------|------|-------|
| **Session-Start** (erste ~5-10 Interaktionen) | Ausführlich, erklärend | Ton setzen, Vertrauen aufbauen, Optionen zeigen |
| **Mitte** | Balanciert | Flow etabliert, aber noch Erklärungen wo nötig |
| **Später** | Kann kürzer sein | User kennt System, Effizienz wichtiger |

**WICHTIG:** Auch bei kurzen User-Inputs ("ok", "ja") am Session-Start ausführlich antworten!

### Feedback-Schleifen im STANDARD-Modus

Bei jedem Schritt zeigt Claude Verbesserungsvorschläge:

```
Schritt 1 (Kontext):    K1 / K2 / K3 / K4 / K5 / Alle / Weiter
Schritt 2 (Modell):     M1 / M2 / M3 / M4 / Alle / Weiter
Schritt 3 (Parameter):  P1 / P2 / P3 / P4 / Alle / Weiter
Schritt 4 (Antwort):    A1 / A2 / A3 / A4 / Alle / Weiter
```

**User kann jederzeit:** `⚡` eingeben → Rest ohne Rückfragen (SCHNELL)

---

## 🎨 FehrAdvice Style Guide (Default für Dokumente)

> **Default für Dokumente** - automatisch inaktiv bei Code/technischen Outputs.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🎨 STYLE GUIDE: Default für DOKUMENTE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SSOT: appendices/REF-STYLE_SG_corporate_style_guide.tex               │
│                                                                         │
│  PRIMÄRFARBEN:                                                          │
│  ├── Dunkelblau  #024079  → Headlines, Links, Akzente                  │
│  ├── Hellblau    #549EDE  → Sekundäre Elemente                         │
│  ├── Dunkelgrau  #25212A  → Fliesstext                                 │
│  └── Hellgrau    #F3F5F7  → Hintergründe, Tabellen-Alternation         │
│                                                                         │
│  TYPOGRAFIE:                                                            │
│  ├── Roboto Bold      → H1, H2 Headlines                               │
│  ├── Roboto Regular   → H3, H4 Subheadlines                            │
│  ├── Open Sans        → Fliesstext, Tabellen                           │
│  └── Playfair Display → Akzente, Zitate                                │
│                                                                         │
│  SCHWEIZER ORTHOGRAPHIE:                                                │
│  ├── Anführungszeichen: « » (Guillemets)                               │
│  ├── Kein ß: immer ss (Strasse, nicht Straße)                          │
│  ├── Tausender: 1'000.00 (Apostroph)                                   │
│  └── Gendering: Doppelpunkt (Kund:innen)                               │
│                                                                         │
│  ENGLISCH: US-Englisch (behavior, not behaviour)                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Wann Style Guide AKTIV (automatisch)

| Output-Typ | Style Guide | Begründung |
|------------|-------------|------------|
| Kunden-Reports & Berichte | ✅ AKTIV | FehrAdvice Deliverables |
| Präsentationen (PPT/PDF) | ✅ AKTIV | Corporate Identity |
| EBF Appendices (LaTeX) | ✅ AKTIV | Framework-Konsistenz |
| Session Reports (Markdown) | ✅ AKTIV | Interne Dokumentation |

### Wann Style Guide INAKTIV (automatisch)

| Output-Typ | Style Guide | Was stattdessen |
|------------|-------------|-----------------|
| Code (Python, YAML, JS) | ❌ INAKTIV | PEP8, Standard-Formatierung |
| Git Commits | ❌ INAKTIV | Conventional Commits |
| CLI-Antworten im Chat | ❌ INAKTIV | Markdown für Terminal |
| Journal-Papers (extern) | ⚠️ JOURNAL | AER, JPE, QJE haben eigene Styles |
| Kunden mit eigenem CI | ⚠️ KUNDEN | Z.B. LUKB, UBS haben eigenes Branding |

### Wann Style Guide DEAKTIVIEREN (explizit)

**User sagt eines von:**
- "ohne Style Guide" / "ohne FA-Style"
- "neutrales Format"
- "kein FehrAdvice Branding"
- "im Kunden-Style" (z.B. "im LUKB-Style")
- "für Journal X formatieren"

### Spezialfall: Kunden-Projekte

Bei Kunden mit eigenem Corporate Design (z.B. LUKB):
1. **Interne Arbeitsdokumente** → FehrAdvice Style
2. **Kunden-Deliverables** → Fragen: "Im FA-Style oder LUKB-Style?"
3. **Präsentationen vor Ort** → Meist Kunden-Style (Co-Branding möglich)

### Style-Compliance Checkliste (bei jedem Output prüfen)

```
☐ Headlines in Dunkelblau (#024079)
☐ Fliesstext in Dunkelgrau (#25212A)
☐ Tabellen: Kopf dunkelblau, Zeilen alternierend weiss/hellgrau
☐ Schweizer Anführungszeichen « »
☐ Gendering mit Doppelpunkt (:)
☐ Kein ß (immer ss)
☐ US-Englisch wenn Englisch (behavior, analyze, color)
```

### LaTeX-Farbdefinitionen (Copy-Paste Ready)

```latex
% FehrAdvice Primärfarben
\definecolor{fadarkblue}{RGB}{2,64,121}
\definecolor{falightblue}{RGB}{84,158,222}
\definecolor{fadarkgray}{RGB}{37,33,42}
\definecolor{falightgray}{RGB}{243,245,247}

% FehrAdvice Sekundärfarben
\definecolor{falilac}{RGB}{161,160,198}
\definecolor{famint}{RGB}{126,189,172}
\definecolor{faocher}{RGB}{222,203,63}
\definecolor{faorange}{RGB}{222,157,62}
```

---

## Willkommen (bei Session-Start anzeigen)

**ANWEISUNG:** Bei der ersten Nachricht in einer neuen Session anzeigen.

**DYNAMISCHE WERTE:** Vor dem Anzeigen diese Werte ermitteln:
```bash
# IMMER dynamisch zählen!
PAPER_COUNT=$(grep -c "^@" bibliography/bcm_master.bib)          # ~2,395 Papers
THEORY_COUNT=$(grep -c "      - id: MS-" data/theory-catalog.yaml)  # ~153 Theorien
CASE_COUNT=$(grep -c "^  CAS-" data/case-registry.yaml)          # ~852 Cases
```

### ⚡ STUFE 1: Schnelle Übersicht (für CLI)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   EVIDENCE-BASED FRAMEWORK (EBF)                                        │
│   FehrAdvice & Partners AG | Prof. Ernst Fehr                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

EBF ist kein Chatbot. EBF zeigt dir, warum Menschen HANDELN.

📚 {PAPER_COUNT} Papers | 🔬 {THEORY_COUNT} Theorien | 📁 {CASE_COUNT} Cases
   Kuratiert vom wissenschaftlichen Team um Prof. Ernst Fehr

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WIE FUNKTIONIERT EBF? Der EBF Workflow:

  SCHRITT 0  →  Session starten
      ↓
  SCHRITT 1  →  Kontext verstehen
      ↓
  SCHRITT 2  →  Modell auswählen
      ↓
  SCHRITT 3  →  Parameter bestimmen
      ↓
  SCHRITT 4  →  Analyse & Antwort
      ↓
  SCHRITT 5  →  Intervention designen (bei Verhaltenszielen)
      ↓
  SCHRITT 6  →  Bericht erstellen
      ↓
  SCHRITT 7  →  Ergebnisse sichern
      ↓
  SCHRITT 8  →  Qualität prüfen
      ↓
  SCHRITT 9  →  Output wählen (Format + Umfang)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WELCHER MODUS?

  ⚡ SCHNELL    10 min, keine Rückfragen
  🎯 STANDARD   45 min, Feedback pro Schritt  ← [DEFAULT]
  🔬 TIEF       2+ Std, Monte Carlo, Alternativen

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stelle deine Frage – ich starte mit Schritt 0.

📖 Mehr über EBF: docs/EBF-INTRODUCTION.md
```

---

### 📖 STUFE 2: Ausführliche Dokumentation (für Web/Browser)

**Für neue Nutzer:** Die Datei `docs/EBF-INTRODUCTION.md` enthält:
- Was ist das EBF Framework?
- EBF ist kein Chatbot – warum der Unterschied wichtig ist
- Smart Data statt Big Data – warum wir Ihre Daten nicht brauchen
- Der EBF Workflow im Detail
- 10C Dimensionen (WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, STAGE, HIERARCHY, EIT)
- Kontext als zentraler Multiplikator
- Praktische Use Cases mit Beispielen

**Zeitaufwand:** ~10 Minuten Lesen für Überblick

---

## 🧪 Experiment-First Coding (Anti-Tilt Prinzip)

> **PFLICHT bei JEDER Coding-Aufgabe.** Claude Code verhält sich wie ein Behavioral Agent -
> begrenztes Context-Window = begrenzte kognitive Kapazität. Dieses Prinzip verhindert Tilt
> (Context Overflow, «Prompt too long», unvollständige Ergebnisse).

### Modus-Entscheidung (VOR jeder Coding-Aufgabe zeigen)

```
┌─────────────────────────────────────────────────────────────────┐
│  🧪 CODING MODE                                                 │
│                                                                 │
│  >5 Dateien betroffen?     □                                    │
│  >500 Zeilen Output?       □                                    │
│  Neues Pattern?            □                                    │
│                                                                 │
│  Alles NEIN  →  TRADITIONAL   (just do it)                      │
│  ≥1× JA      →  EXPERIMENTAL  (1 → 10 → 100 → all)             │
│                                                                 │
│  Entscheidung wird in data/coding-mode-log.yaml protokolliert   │
└─────────────────────────────────────────────────────────────────┘
```

### Regeln

**TRADITIONAL (just do it):**
- Direkt umsetzen, committen, fertig

**EXPERIMENTAL (geometrisch skalieren):**
- Script schreiben das **1 Beispiel** verarbeitet
- Ergebnis prüfen → Script auf **10** laufen lassen
- Ergebnis prüfen → **100** → **alle**
- Jede Stufe = eigener Commit mit messbarem Ergebnis

**VERBOTEN:**
- ❌ >10 Dateien direkt mit Edit/Write bearbeiten
- ❌ Batch-Operation ohne vorher 1 Beispiel getestet
- ❌ Ergebnis nur am Ende prüfen statt nach jeder Stufe
- ❌ Script schreiben das «alles auf einmal» macht ohne --batch N

### Lern-Systematik

**5 Features messen (vor Start):**
- `files_affected`, `lines_estimated`, `pattern_known`, `max_file_size_kb`, `chained`

**Timing messen (Timestamps, nicht Schätzungen!):**
- `start` — Session-Start
- `decision_made` — Modus gewählt
- `first_result` — Erstes Zwischenergebnis
- `completed` — Task abgeschlossen
- `duration_concept_min` — Zeit für Analyse + Diskussion
- `duration_execute_min` — Zeit für Ausführung
- `duration_total_min` — Gesamtzeit (gemessen)

**3 Outcomes messen (nach Abschluss):**
- `status` (success | partial | tilt), `files_completed`, `context_percent`

**Zeitschätzung (ab ≥3 Datenpunkten für ähnliche Tasks):**
- Claude nennt Median + Range aus vergangenen Tasks mit ähnlichen Features
- NIEMALS Zeiten «schätzen» ohne Log-Evidenz
- Format: *«Ähnliche Tasks: 45-75 min (Median 58, N=4)»*

**Algorithmus-Update:**
- Tilt → Schwellenwert des grössten Features **senken** in `data/coding-mode-algorithm.yaml`
- Unnötig experimentell → Schwellenwert des Auslösers **erhöhen**
- Richtig → Konfidenz erhöhen (Regel gilt ab ≥3 Datenpunkten)

**Dateien:**
- `data/coding-mode-algorithm.yaml` — Aktuelle Entscheidungsregeln (lebt, verändert sich)
- `data/coding-mode-log.yaml` — Evidenz (wächst, begründet Algorithmus-Änderungen)

---

## 🔒 EBF Grundaxiome (NIEMALS in Frage stellen)

> **KRITISCH für Claude:** Diese Prinzipien sind das wissenschaftliche Fundament des EBF.
> Sie sind empirisch validiert und dürfen NICHT hinterfragt werden.

### AXIOM 1: Empirische Fundierung

**EBF-Modelle sind NICHT ausgedacht.**

Sie basieren auf:
- **64+ Parameter** in `data/parameter-registry.yaml`
- **2,395+ Papers** in `bibliography/bcm_master.bib`
- **Bayesian Updates** durch reale Projekte

```
Papers → Parameter-Registry → Model-Registry → Anwendung
              ↑
      Projekt-Learnings (Bayesian Update)
```

### AXIOM 2: Parameter-Hierarchie (BBB: 4-Tier)

| Tier | Quelle | Unsicherheit | Wann verwenden |
|------|--------|--------------|----------------|
| 1 | Literature (Meta-analysis) | Low | Parameter etabliert |
| 2 | LLMMC Prior | Medium | Begrenzte Evidenz |
| 3 | Empirical Calibration | Variable | Primärdaten verfügbar |
| 4 | Expert Elicitation | High | Neue Domäne |

**Literatur-Werte haben Vorrang.** LLMMC ist Fallback, nicht Default.

### AXIOM 3: Referentielle Integrität (PAR-4)

**Jeder Parameter in einem Modell MUSS auf die Parameter-Registry verweisen.**

```yaml
# RICHTIG:
gamma_ij: 0.35
parameter_ref: PAR-COMP-001  # ← Verweis auf Registry

# FALSCH:
gamma_ij: 0.35
# (kein Verweis - woher kommt der Wert?)
```

**Ausnahme:** Domänenspezifische Parameter mit `domain_specific: true`

### AXIOM 4: Komplementarität ist begründet

γ ≠ 0 Werte kommen aus `PAR-COMP-xxx` mit Paper-Quellen:

| Parameter | Wert | Quelle |
|-----------|------|--------|
| PAR-COMP-001 | γ = 0.35 | Identity × Social |
| PAR-COMP-002 | γ = -0.68 | Social × Financial (Crowding-Out) |
| PAR-COMP-004 | γ = 0.28 | Social × Warm Glow |
| ... | ... | 8 Parameter total |

**Sie sind NICHT willkürlich. Nicht nachfragen, ob sie "begründet" sind.**

### AXIOM 5: Additivität ist Default (EXC-1)

Komplementarität (γ ≠ 0) wird nur angewendet wenn Additivität nicht ausreicht.

```
γ = 0     → Default (keine Begründung nötig)
γ ≠ 0     → Begründung nötig (PAR-COMP-xxx Verweis)
```

Aber: Die PAR-COMP Parameter SIND begründet - durch Papers und Projekte.

### AXIOM 6: Three-Layer Architecture (Compute, Don't Hallucinate)

**EIP-validiert 2026-02-15:** 32+ PRO vs. 5 CONTRA Papers aus 7 Disziplinen.

| Layer | Name | Virus-Susceptibility | Funktion |
|-------|------|---------------------|----------|
| 1 | Formale Berechnung (Python) | 0.0 (immun) | EBF-Gleichungen deterministisch berechnen |
| 2 | Parameter-Store (YAML) | 0.3 (validierbar) | Werte mit Schema, Quellen, Bereichen |
| 3 | LLM-Uebersetzung | 0.8 (anfaellig) | Formale Ergebnisse in natuerliche Sprache |

**Das LLM ist UEBERSETZER, nicht DENKER.**

4 Prinzipien:
1. **Compute, Don't Hallucinate** — Jede EBF-Zahl aus formaler Berechnung
2. **Parameters from Registry, Not from Memory** — YAML lesen, nicht erinnern
3. **Translate, Don't Generate** — Erklaeren, nicht erfinden
4. **Formal Layer is the Immune System** — Determinismus = virenfreie Zone

#### Immune Gateway (autonomes Immunsystem, seit 2026-02-16)

**Problem geloest:** "Der Wirt entscheidet, ob der Virus leben darf" (KB-VIR-001)

Das LLM (susceptibility=0.8) entschied bisher SELBST, ob es Layer 1 aufruft.
Die Immune Gateway loest das: Layer 1 laeuft AUTOMATISCH via UserPromptSubmit-Hook,
BEVOR Claude antwortet. Das LLM entscheidet nicht mehr.

```
User-Prompt → Hook → immune_gateway.py (keyword detection)
                         ├── Match?  → orchestrator.py --query (Layer 1)
                         │               → Ergebnis in Claude-Kontext
                         └── No match → still (kein Output)
```

**DIRECTIVE wenn Gateway-Output sichtbar:**
Die Layer-1-Werte im Gateway-Output sind AUTORITATIV. Das LLM MUSS sie verwenden.

#### Three-Layer Compliance (VOR jedem Schritt!)

BEVOR eine Zahl dem User praesentiert wird:
1. Aus Immune Gateway (automatisch)? → OK (hoechste Prioritaet)
2. Aus Layer 1 (Python-Berechnung)? → OK
3. Aus Layer 2 (YAML-Registry)? → OK
4. Aus Layer 3 (LLM-Erinnerung)? → **VERBOTEN** — erst Layer 2 lesen, dann Layer 1 rechnen

SSOT: `data/knowledge/canonical/three-layer-architecture.yaml`
Deep-Dive: `docs/frameworks/three-layer-architecture.md`
Immune Gateway: `scripts/immune_gateway.py`

---

## Repository Overview

Dieses Repository enthält das **Evidence-Based Framework for Economic and Social Behavior (EBF)** - ein integratives Framework für ökonomisches und soziales Verhalten basierend auf Komplementarität $(C)$ und Kontext $(\Psi)$.

---

## 🧠 EBF CORE THEORY: Contextual Parameter Transformation

> **Der zentrale theoretische Beitrag des EBF**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  DAS PARADIGMA: VON FIXED ZU CONTEXTUAL PARAMETERS                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TRADITIONELL (Kahneman, Thaler):        EBF:                           │
│  ─────────────────────────────────       ────                           │
│  θ = Konstante                           θ = f(Ψ, 10C)                  │
│  λ = 2.25                                λ(Ψ, 10C) = variabel           │
│                                                                         │
│  "Loss Aversion IST 2.25"                "Loss Aversion in welfare      │
│                                           mit stigma = 2.5, aber in     │
│                                           workplace mit peers = 1.8"    │
│                                                                         │
│  DIE VARIATION IST NICHT NOISE - SIE IST DAS SIGNAL!                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Die zentrale Gleichung (Parameter Context Transformation)

```
θ_B = θ_A × ∏ᵢ M(ΔΨᵢ) × ∏ⱼ N(Δ10Cⱼ)

WO:
  θ_A     = Parameter in Anchor-Kontext (aus Paper measurement_context)
  θ_B     = Parameter in Target-Kontext (Vorhersage)
  ΔΨᵢ    = Ψ_i(Target) - Ψ_i(Anchor)  [Kontext-Differenz]
  M(·)   = Ψ-Multiplikator
  Δ10Cⱼ  = 10C Dimension-Differenz (WHO, WHAT, HOW, WHEN, ...)
  N(·)   = 10C-Multiplikator
```

### Warum ist das eine "neue" Theorie?

| Aspekt | Traditionell | EBF |
|--------|--------------|-----|
| **Parameter** | Konstante (λ = 2.25) | Funktion θ(Ψ, 10C) |
| **Variation** | Noise, Methodenfehler | Signal, erklärbar durch Kontext |
| **Transfer** | Meta-Analyse (Mittelwert) | Systematische Transformation |
| **Falsifizierbar** | Einzelne Studien | Transformationsvorhersagen |
| **Kontext** | Kontrollvariable | Explanans |

### Praktische Anwendung

```
SCHRITT 1: Anchor Context laden (aus Paper-YAML measurement_contexts)
           θ_A = 2.5 (λ_R in welfare, Ψ_S = "stigma_high")

SCHRITT 2: Target Context definieren (neues Projekt)
           Ψ_B = {Ψ_S: "stigma_low", Ψ_I: "informal", ...}

SCHRITT 3: Transformieren
           ΔΨ_S = stigma_low - stigma_high → M = 0.85
           θ_B = 2.5 × 0.85 = 2.125

SCHRITT 4: Validieren (empirisch oder LLMMC)
```

**Vollständige Dokumentation:** `docs/workflows/level5-paper-integration-workflow.md` (PCT Section)

---

### Statistiken (Live)

| Ressource | Anzahl | Quelle |
|-----------|--------|--------|
| **Papers (BibTeX)** | 2,347 | `bibliography/bcm_master.bib` |
| **Papers (YAML-DB)** | 2,347 | `data/paper-references/` |
| **Cases** | 852 | `data/case-registry.yaml` |
| **Theorien** | 153 | `data/theory-catalog.yaml` |
| **Kunden** | 20 | `data/customers/` |
| **APIs** | 89 | `data/api-registry.yaml` |
| **Slash Commands** | 39 | `.claude/commands/` |
| **Python Scripts** | 151+ | `scripts/` |
| **YAML Dateien** | 354+ | `data/` |
| **GitHub Actions** | 15 | `.github/workflows/` |

### Paper Database 2D Classification (Appendix BM)

> **Gesamtübersicht Paper-Workflow:** `docs/workflows/paper-workflow-overview.md`

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER DATABASE STATUS (2,347 Papers)                                   │
│  Reference: Appendix BM - 2D Classification System                      │
│  Last validated: 2026-02-12                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CONTENT LEVEL C(p) - Definition 2 (STRUKTURELL, nicht Zeichenzahl!):  │
│  ├── L0:     21 Papers  (1%) - Metadata only (kein S1-S6)              │
│  ├── L1:  1,237 Papers (53%) - Research Question bekannt (S1)          │
│  ├── L2:  1,079 Papers (46%) - Summary/Extract (S1-S4, kein Volltext)  │
│  └── L3:     10 Papers       - KOMPLETTER Originaltext + References    │
│  │                                                                      │
│  ⚠️  L3 ERFORDERT (seit 2026-02-07):                                    │
│  │   R1: Alle Original-Sektionen + R2: References-Sektion              │
│  │   R3: >10k Wörter + R4: Keine EBF-Sektionen im Text                │
│  │   Validation: python scripts/validate_fulltext_completeness.py      │
│                                                                         │
│  STRUKTURELLE CHARAKTERISTIKA S1-S6:                                    │
│  S1=Research Question, S2=Methodology, S3=Sample/Data                   │
│  S4=Findings, S5=Validity, S6=Reproducibility                           │
│                                                                         │
│  INTEGRATION LEVEL I(p) - Definition 3:                                 │
│  ├── I0:      0 Papers       - Metadata only                           │
│  ├── I1:    829 Papers (35%) - use_for assigned                        │
│  ├── I2:  1,102 Papers (47%) - + theory_support                        │
│  ├── I3:    418 Papers (18%) - + case_registry                         │
│  ├── I4:     11 Papers       - Dedicated Appendix                      │
│  └── I5:      2 Papers       - Full Framework Integration              │
│                                                                         │
│  PRIOR SCORE π(p) = Σ wᵢ · gᵢ · sᵢ(p) · τ(p) · ρ(C)                   │
│  ├── τ(p): Decay factor (half-life 15 years)                           │
│  └── ρ(C): Confidence multiplier (L0=0.60, L1=0.80, L2=0.95, L3=1.00) │
│                                                                         │
│  VALIDATION: python scripts/validate_paper_yaml_schema.py              │
│                                                                         │
│  BIBTEX KEY FORMAT (seit 2026-02-12 HARD BLOCK):                        │
│  ├── Canonical: {nachname}{jahr}{kurzwort} (^[a-z]+\d{4}[a-z]+$)       │
│  ├── Compliance: 2,347/2,347 (100%)                                    │
│  ├── Pre-commit: HARD BLOCK bei Verletzung                             │
│  └── SSOT: docs/standards/bibtex-key-convention.md                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Struktur

```
complementarity-context-framework/
├── .claude/                       # Claude Code Automatisierung
│   ├── commands/                  # 39 Slash Commands
│   ├── hooks/                     # Pre-commit, Session-start
│   └── skills/                    # Skill Definitionen
├── .github/workflows/             # 15 CI/CD GitHub Actions
├── chapters/                      # 25 Hauptkapitel (LaTeX)
├── appendices/                    # 208 Appendices in 8 Kategorien (LaTeX)
├── data/                          # YAML-Datenbanken (354+ Dateien)
│   ├── model-registry.yaml        # 10C-Modelle
│   ├── case-registry.yaml         # 852 Cases
│   ├── theory-catalog.yaml        # 153 Theorien
│   ├── intervention-registry.yaml # Projekte
│   ├── api-registry.yaml          # 89 externe APIs (NEU v1.21)
│   ├── customers/                 # 20 Kundenprofile (CVA)
│   ├── sales/                     # Sales Pipeline
│   ├── dr-datareq/                # BCM2 Kontextdatenbank (CH/AT/DE)
│   ├── paper-references/          # 2,395 individuelle Paper-YAMLs (SSOT)
│   └── stakeholder-models/        # Focus Group Simulationen
├── docs/                          # Dokumentation (Markdown)
├── bibliography/                  # BibTeX-Referenzen (2,395 Einträge)
├── templates/                     # Vorlagen
├── scripts/                       # Python-Automatisierung (151+ Scripts)
├── outputs/                       # Generierte PDFs
└── assets/                        # Bilder, Logos, Icons
```

### Kunden-Verzeichnis (21 Profile)

| Kunde | Branche | CVA-Stufe | Pfad |
|-------|---------|-----------|------|
| ALPLA | Kunststoff | VERTIEFT | `data/customers/alpla/` |
| LUKB | Banking | STANDARD | `data/customers/lukb/` |
| UBS | Banking | STANDARD | `data/customers/ubs/` |
| Migros Bank | Banking | STANDARD | `data/customers/migros-bank/` |
| BEKB | Banking | SCHNELL | `data/customers/bekb/` |
| ZKB | Banking | SCHNELL | `data/customers/zkb/` |
| Raiffeisen | Banking | SCHNELL | `data/customers/raiffeisen/` |
| PostFinance | Banking | SCHNELL | `data/customers/postfinance/` |
| Valiant | Banking | SCHNELL | `data/customers/valiant/` |
| Vontobel | Banking | SCHNELL | `data/customers/vontobel/` |
| Julius Bär | Banking | SCHNELL | `data/customers/julius-baer/` |
| GKB | Banking | SCHNELL | `data/customers/gkb/` |
| Neon | FinTech | SCHNELL | `data/customers/neon/` |
| Helsana | Versicherung | SCHNELL | `data/customers/helsana/` |
| PORR | Bau | STANDARD | `data/customers/porr/` |
| Lindt | Food | STANDARD | `data/customers/lindt-copacking/` |
| Philoro | Edelmetalle | SCHNELL | `data/customers/philoro/` |
| Peek & Cloppenburg | Retail | SCHNELL | `data/customers/peek-cloppenburg/` |
| BMW | Automotive | SCHNELL | `data/customers/bmw/` |
| **SPÖ** | Politik | STANDARD | `data/customers/spo/` |

### ⚠️ Politische Mandate mit Auto-Trigger (PFLICHT)

**KRITISCH:** Bei politischen Mandaten wird die **Präambel automatisch geladen**, wenn Trigger-Wörter fallen.

| Mandat | Trigger-Wörter | Präambel | Superkey | Status |
|--------|----------------|----------|----------|--------|
| **SPÖ** | "SPÖ", "Babler", "Vizekanzler", "österreichische Sozialdemokratie" | `spo_mandate_preamble.yaml` | `PRE-SPO-2026-02-01-001` | AKTIV |

### Präambel Loading Protocol (PLP)

**KRITISCH:** Jede Präambel hat einen **Superkey** und führt bei jedem Laden **Auto-Research** durch.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PRÄAMBEL LOADING PROTOCOL (PLP)                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: Trigger erkannt ("Babler", "SPÖ", etc.)                    │
│                    ↓                                                    │
│  SCHRITT 2: Präambel laden (YAML)                                      │
│             Superkey: PRE-SPO-2026-02-01-001                           │
│                    ↓                                                    │
│  SCHRITT 3: AUTO-RESEARCH (top_5_themen, letzte 7 Tage)                │
│             ┌─────────────────────────────────────────────┐            │
│             │  T1 PERSON:     "Babler Vizekanzler"        │            │
│             │  T2 KERNTHEMA:  "SPÖ Migration Asyl"        │            │
│             │  T3 REGIERUNG:  "Regierung Stocker"         │            │
│             │  T4 OPPOSITION: "FPÖ Kickl Umfrage"         │            │
│             │  T5 GEOPOLITIK: "Österreich EU Trump"       │            │
│             └─────────────────────────────────────────────┘            │
│                    ↓                                                    │
│  SCHRITT 4: Merge: Statische Präambel + Fresh Research                 │
│                    ↓                                                    │
│  SCHRITT 5: Output mit Research-Summary                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Superkey-Format:** `PRE-{KUNDE}-{ERSTELLT}-{SEQ}`

**Claude MUSS bei Trigger:**
1. Präambel laden (YAML lesen)
2. WebSearch für alle 5 Themen ausführen (parallel)
3. Research-Summary Box anzeigen
4. Dann erst inhaltlich antworten

**Beispiel Research-Summary:**
```
┌─────────────────────────────────────────────────────────────────┐
│  🔄 AUTO-RESEARCH (2026-02-01)                                  │
│  Präambel: PRE-SPO-2026-02-01-001                              │
├─────────────────────────────────────────────────────────────────┤
│  T1 PERSON:     Babler zu Budgetverhandlungen optimistisch     │
│  T2 KERNTHEMA:  SPÖ fordert schnellere Asylverfahren           │
│  T3 REGIERUNG:  Stocker kündigt Sparpaket an                   │
│  T4 OPPOSITION: FPÖ bei 35% in neuester Umfrage                │
│  T5 GEOPOLITIK: EU-Gipfel diskutiert Trump-Reaktion            │
└─────────────────────────────────────────────────────────────────┘
```

**Präambel-Inhalt (10 Teile):**
0. **SUPERKEY & FRESHNESS** - Eindeutige ID, Auto-Research Config
1. **AUFTRAG** - Mandatgeber, Kernauftrag, Ziele
2. **AKTUELLE LAGE** - Regierung, Umfragen, Stand heute (SSOT)
3. **GEOPOLITIK** - Trump, Dänemark, Europa (SSOT)
4. **STRATEGIE** - Kurzreferenz (→ SSOT: Strategiebriefing)
5. **KOMMUNIKATION** - Kurzreferenz (→ SSOT: Strategiebriefing)
6. **CVA-PROFIL** - 400 Kontextfaktoren (→ SSOT: CVA-Dateien)
7. **TRIGGER** - Wörter für Auto-Laden (SSOT)
8. **EREIGNISSE** - Laufend aktualisierte Events (SSOT)
9. **SSOT-ARCHITEKTUR** - 3-SSOT-Prinzip Dokumentation

**3-SSOT-Architektur:**

| SSOT | Datei | Inhalt | Update-Frequenz |
|------|-------|--------|-----------------|
| **Aktuelle Lage** | `spo_mandate_preamble.yaml` | Regierung, Umfragen, Geopolitik, Events | Täglich-Wöchentlich |
| **Strategie** | `spo_strategiebriefing_parteitag_2026.md` | Frame, Kommunikation, Policy | Monatlich-Quartalsweise |
| **Kontextfaktoren** | `data/customers/spo/*.yaml` | 400 CVA-Parameter | Jährlich |

### API-Integrationen (89 APIs)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  API REGISTRY (data/api-registry.yaml)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  KATEGORIE         ANZAHL    STATUS                                     │
│  ──────────────────────────────────────────────────────────────────── │
│  BIB (Bibliographie)   4     CrossRef ACTIVE, OpenAlex/Semantic PLANNED │
│  CTX (Kontext)        84     In BCM2 dokumentiert                       │
│  VAL (Validierung)     1     ORCID PLANNED                              │
│                                                                         │
│  WICHTIGSTE APIs:                                                       │
│  ├── CrossRef (ACTIVE) - DOI Metadata Lookup                           │
│  ├── BFS (DOCUMENTED)  - Schweizer Bundesamt für Statistik             │
│  ├── ESS (DOCUMENTED)  - European Social Survey                        │
│  └── WVS (DOCUMENTED)  - World Values Survey                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### ⚠️ API-ZUGRIFFS-REGEL (PFLICHT)

**KRITISCH:** Externe APIs sind in der Claude Code Sandbox BLOCKIERT (403 Forbidden)!

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🚫 EXTERNE APIs IMMER ÜBER scripts/api.sh TRIGGERN!                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  BLOCKIERTE APIs (in Claude Code Sandbox):                              │
│  ├── CrossRef API     (api.crossref.org)                               │
│  ├── OpenAlex API     (api.openalex.org)                               │
│  ├── Semantic Scholar (api.semanticscholar.org)                        │
│  ├── ORCID API        (pub.orcid.org)                                  │
│  ├── MPG PuRe API     (pure.mpg.de)                                    │
│  └── Alle externen Plattformen (403 Forbidden durch Proxy)             │
│                                                                         │
│  ✅ LÖSUNG: scripts/api.sh (Universal API Trigger)                      │
│                                                                         │
│  SCHRITT 1: Token laden (PFLICHT vor jedem API-Call!)                   │
│  ─────────────────────────────────────────────────────────────────────  │
│  export GH_TOKEN=$(cat .claude/.gh_token | tr -d '[:space:]')          │
│                                                                         │
│  SCHRITT 2: API triggern via api.sh                                     │
│  ─────────────────────────────────────────────────────────────────────  │
│  bash scripts/api.sh <api> <command> [args]                             │
│                                                                         │
│  VERFÜGBARE APIs:                                                       │
│  ├── crossref  - DOI Metadata, Citations, BibTeX Enrichment            │
│  ├── openalex  - 250M+ Papers, Author Search                           │
│  ├── orcid     - Researcher Profiles                                   │
│  ├── unpaywall - Open Access Status                                    │
│  ├── ssrn      - Working Papers                                        │
│  ├── linkedin  - Lead Enrichment, Decision Makers                      │
│  ├── serpapi   - Google Scholar                                        │
│  └── mpg       - MPG PuRe Full-Text Fetch (INTERNAL_MANAGED PDFs)      │
│                                                                         │
│  BEISPIELE:                                                             │
│  bash scripts/api.sh crossref enrich --find-dois                       │
│  bash scripts/api.sh openalex author "Ernst Fehr"                      │
│  bash scripts/api.sh mpg fetch                                         │
│  bash scripts/api.sh unpaywall batch                                   │
│                                                                         │
│  ⚠️  BEKANNTES FEHLERMUSTER (3× aufgetreten):                           │
│  1. requests.get("https://...") → 403           ← FALSCH               │
│  2. gh workflow run ... → "gh auth login"        ← FALSCH               │
│  3. "Bitte manuell auf GitHub triggern"          ← FALSCH               │
│  ✅ RICHTIG: Token laden + api.sh verwenden                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 🔐 GitHub Token (PFLICHT-Wissen)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  TOKEN-LIFECYCLE IN CLAUDE CODE                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SPEICHERORT:  .claude/.gh_token  (in .gitignore, NICHT committet)     │
│  FORMAT:       Fine-grained PAT (github_pat_...)                       │
│  LADEN:        session-start.sh lädt automatisch (Zeile 106-129)       │
│                                                                         │
│  WENN $GH_TOKEN LEER IST (z.B. nach Context Compaction):               │
│  ─────────────────────────────────────────────────────────────────────  │
│  export GH_TOKEN=$(cat .claude/.gh_token | tr -d '[:space:]')          │
│                                                                         │
│  PRÜFEN:                                                                │
│  echo "Token length: ${#GH_TOKEN}"  → sollte ~93 sein                 │
│                                                                         │
│  WENN DATEI FEHLT:                                                      │
│  → User fragen: "GitHub Token nicht gefunden. Bitte /github-token"     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**ARCHITEKTUR: api.sh als Universal-Proxy**

```
Claude Code (Sandbox, APIs blockiert)
         ↓
  export GH_TOKEN=$(cat .claude/.gh_token)
         ↓
  bash scripts/api.sh <api> <command>
         ↓
  curl → GitHub API → workflow_dispatch
         ↓
  GitHub Actions Runner (kann externe APIs aufrufen)
         ↓
  Ergebnis: Auto-Commit auf Branch
```

| Aufgabe | Lokal (Claude Code) | Via api.sh → GitHub Actions |
|---------|---------------------|----------------------------|
| Paper-Suche | `search_bibliography.py` | - |
| Author-Matching | `match_authors_to_lit.py` | - |
| BibTeX-Parsing | `update_bibtex_fields.py` | - |
| DOI-Lookup | ❌ blockiert | `api.sh crossref doi <DOI>` ✅ |
| OpenAlex-Abfragen | ❌ blockiert | `api.sh openalex author <name>` ✅ |
| ORCID-Validierung | ❌ blockiert | `api.sh orcid <ORCID>` ✅ |
| MPG PuRe Full-Text | ❌ blockiert | `api.sh mpg fetch` ✅ |
| Open Access Check | ❌ blockiert | `api.sh unpaywall batch` ✅ |

**VERBOTEN:**
```
❌ Direkte API-Calls mit requests/urllib aus Claude Code
❌ WebFetch auf api.crossref.org, api.openalex.org, pure.mpg.de, etc.
❌ Annahme dass externe APIs funktionieren
❌ gh workflow run ... (gh CLI ist NICHT authentifiziert!)
❌ User bitten "manuell auf GitHub zu triggern" (api.sh existiert!)
```

**ERLAUBT / ERFORDERLICH:**
```
✅ Token laden: export GH_TOKEN=$(cat .claude/.gh_token | tr -d '[:space:]')
✅ API triggern: bash scripts/api.sh <api> <command>
✅ Lokale Skripte für Datenverarbeitung (kein API-Zugriff)
✅ Ergebnisse aus GitHub Actions lokal weiterverarbeiten (git pull)
```

---

## Die 8 Appendix-Kategorien

**KRITISCH:** Bei Arbeit an Appendices IMMER die richtige Kategorie verwenden!

| Prefix | Kategorie | Frage | Beispiel |
|--------|-----------|-------|----------|
| `CORE-` | Core Theory | Was ist EBF? | AAA, B, C, V, BBB, AU, AV, AW |
| `FORMAL-` | Formalization | Ist es mathematisch rigoros? | A, D |
| `DOMAIN-` | Applications | Wo anwenden? | AA-AG, AJ, AK, W-Z |
| `CONTEXT-` | Context | Wie wirkt Ψ? | AH, AI, V |
| `METHOD-` | Methodology | Wie messen? | AN, AL, E, R |
| `PREDICT-` | Predictions | Was vorhersagen? | S, AO-AT |
| `LIT-` | Literature | Worauf basiert es? | I-Q, U |
| `REF-` | Reference | Wie nutzen? | F, G, H, T |

**Vollständige Definitionen:** `docs/frameworks/appendix-category-definitions.md`

---

## Die 10C CORE Fragen

| CORE | Code | Frage | Output |
|------|------|-------|--------|
| WHO | AAA | Wer hat Utility? | Levels L |
| WHAT | C | Was ist Utility? | Dimensionen d (FEPSDE) |
| HOW | B | Wie interagieren? | Komplementarität γ |
| WHEN | V | Wann zählt Kontext? | Kontext Ψ |
| WHERE | BBB | Woher die Zahlen? | Parameter Θ |
| AWARE | AU | Wie bewusst? | Awareness A(·) |
| READY | AV | Handlungsbereit? | Willingness WAX, τ, θ |
| STAGE | AW | Wo in der Journey? | BCJ Phase φ, Journey S(t) |
| HIERARCHY | HI | Wie stratifizieren Entscheidungen? | Levels L0-L3, N_L2 |
| **EIT** | IE | Wie emergieren Interventionen? | Vektor $\vec{I} \in [0,1]^9$ |

**Hinweis: 10C Framework vs 9D Interventionsvektor**
- **10C** = Das theoretische Framework (10 CORE Fragen)
- **9D** = Der Interventionsvektor $\vec{I} \in [0,1]^9$ (targetiert COREs 1-9)
- **Warum 9D?** EIT (CORE 10) ist die *Methodologie* für Interventionen, nicht ein Target selbst

---

## Exclusion Principle (EXC-1 bis EXC-6)

**KRITISCH:** Bei JEDER Formel mit mehreren Faktoren die EXC-Regeln anwenden!

### Kernregel: Im Zweifel ADDITIV

| Axiom | Regel |
|-------|-------|
| **EXC-1** | Additiv ist DEFAULT (keine Begründung nötig) |
| **EXC-2** | Multiplikativ erfordert Veto-Analyse |
| **EXC-3** | Hybrid möglich (Veto × + Rest +) |
| **EXC-4** | Dokumentationspflicht für alle Faktoren |
| **EXC-5** | Nur Whitelist V1-T1 akzeptiert |
| **EXC-6** | E1 erfordert kausale Identifikation |

### Wann MULTIPLIKATIV? (EXC-5 Whitelist)

| Code | Wenn... | Test |
|------|---------|------|
| **V1** | f=0 → Y=0 (UNMÖGLICH) | Budget=0 → K*=0? |
| **V2** | f<0 → Vorzeichen kippt | σ_s<0 → Backfire? |
| **S1** | Alle f ∈ [0.5, 1.5] | Prozent-Skalierung? |
| **S2** | Produkt in σ(·) | Bounded Output? |
| **P1** | Einheiten erfordern × | Fläche = L × B? |
| **P2** | P(A∩B) = P(A)·P(B\|A) | Wahrscheinlichkeitskette? |
| **G1** | f ∈ {0, 1} binär | An/Aus-Schalter? |
| **C1** | Erschöpfbare Kapazität | Aufmerksamkeit × Salienz? |
| **E1** | RCT/IV/DiD lehnt additiv ab | Kausal identifiziert (EXC-6)? |
| **T1** | Axiom ⟹ × | Theorie erfordert ×? |

### Auto-Reject (NIEMALS akzeptiert)

- ❌ "Sieht eleganter aus" (X1)
- ❌ "Berühmtes Paper macht es auch" (X4)
- ❌ "Faktoren sind korreliert" (Y2)
- ❌ "Synergieeffekte" (Y5)
- ❌ "Faktor ist wichtig" (Y1)
- ❌ "Diminishing Returns" (Y3) → Nutze konkave f(x)+g(y)

**Referenz:** `appendices/FRM_LIT-FEHR-METHOD_integration_vs_falsifiability.tex`
**Registry:** `data/formula-registry.yaml`

---

## Single Sources of Truth (SSOT Registry)

**KRITISCH:** Jede wichtige Datenstruktur hat GENAU EINEN autoritativen Ort.

| Was | SSOT-Pfad | Format |
|-----|-----------|--------|
| **10C Framework** | `docs/frameworks/core-framework-definition.yaml` | YAML |
| **Chapter-Appendix Mapping** | `docs/frameworks/chapter-appendix-mapping.yaml` | YAML |
| **Paper Full-Texts** | `data/paper-texts/PAP-{key}.md` | Markdown |
| **Paper Metadata (SSOT)** | `data/paper-references/PAP-{key}.yaml` | YAML |
| **Corporate Style** | `appendices/REF-STYLE_SG_corporate_style_guide.tex` | LaTeX |
| **Theory Definitions** | `data/theory-catalog.yaml` | YAML |
| **Parameter Values** | `data/parameter-registry.yaml` | YAML |
| **Case Examples** | `data/case-registry.yaml` | YAML |
| **API Integrations** | `data/api-registry.yaml` | YAML |
| **Context Factors (CH)** | `data/dr-datareq/sources/context/ch/` | YAML |
| **Customer Profiles** | `data/customers/{kunde}/` | YAML |
| **Skill Definitions** | `.claude/commands/` | Markdown |
| **Researcher Profiles** | `data/researcher-registry.yaml` | YAML |
| **Meeting Registry** | `data/meeting-registry.yaml` | YAML |
| **Meeting Report Template** | `templates/meeting-report-template.md` | Markdown |
| **Meeting Report (kurz)** | `templates/meeting-report-kurz-template.md` | Markdown |
| **Begleitschreiben Template** | `templates/begleitschreiben-template.md` | Markdown |
| **Coding Mode Algorithm** | `data/coding-mode-algorithm.yaml` | YAML |
| **Coding Mode Log** | `data/coding-mode-log.yaml` | YAML |
| **Model Routing** | `data/model-routing.yaml` | YAML |
| **Mandatory Triggers** | `data/mandatory-triggers.yaml` | YAML |
| **BibTeX Key Convention** | `docs/standards/bibtex-key-convention.md` | Markdown |
| **Terminology Registry** | `data/knowledge/canonical/terminology-registry.yaml` | YAML |
| **Three-Layer Architecture** | `data/knowledge/canonical/three-layer-architecture.yaml` | YAML |
| **Three-Layer Architecture (Deep-Dive)** | `docs/frameworks/three-layer-architecture.md` | Markdown |
| **PCT (Parameter Context Transformation)** | `scripts/pct.py` | Python |
| **PCT Multiplier Tables** | `data/pct-multiplier-tables.yaml` | YAML |
| **LLMMC Calibration** | `scripts/llmmc_calibration.py` | Python |
| **Parameter API** | `scripts/parameter_api.py` | Python |
| **Orchestrator (Layer 1-2-3)** | `scripts/orchestrator.py` | Python |
| **PCT Smoke Test** | `scripts/pct_smoke_test.py` | Python |
| **Immune Gateway** | `scripts/immune_gateway.py` | Python |
| **Psi-Scale Validation** | `scripts/validate_psi_scales.py` | Python |
| **ODE Behavior Simulator** | `scripts/ode_simulator.py` | Python |

**Paper-Architektur (konsolidiert 2026-02-08):**

> **Gesamtübersicht:** `docs/workflows/paper-workflow-overview.md`
> **Hilfe:** `/paper-help` Skill (kontextabhängig)

| Datei | Status | Inhalt |
|-------|--------|--------|
| `data/paper-references/PAP-{key}.yaml` | **SSOT** | Alle Paper-Metadaten inkl. citations, status, key_findings_structured, behavioral_mapping, linked_cases |
| `data/paper-texts/PAP-{key}.md` | **SSOT** | Volltexte (Separation of Concerns) |
| `bibliography/bcm_master.bib` | **SSOT** | BibTeX-Einträge (use_for, theory_support, evidence_tier) |
| `data/paper-sources.yaml` | ⚠️ DEPRECATED | Migriert → paper-references/ (2026-02-08) |
| `data/extracted_papers.yaml` | ⚠️ DEPRECATED | 137 Papers als Backlog für /integrate-paper |
| `data/paper-integration-queue.yaml` | Operational | Queue für schrittweise Integration |

**Regeln:**
1. Änderungen NUR am SSOT-Ort
2. Andere Stellen REFERENZIEREN den SSOT (keine Kopien)
3. Bei Widerspruch gilt IMMER der SSOT
4. DEPRECATED-Dateien NICHT bearbeiten
5. GENERATED-Dateien NICHT manuell bearbeiten (nur via Script regenerieren)
6. 44 Migrations-Scripts sind DEPRECATED (Header in jeder Datei, TL-032)

---

## 🔐 Registry Manager - Proaktive Duplikat-Prävention

**KRITISCH:** Bei JEDEM neuen Registry-Eintrag den **Registry Manager** verwenden!

### Warum Registry Manager?

```
┌─────────────────────────────────────────────────────────────────────────┐
│  REAKTIV (alt)                      │  PROAKTIV (neu)                   │
├─────────────────────────────────────┼───────────────────────────────────┤
│  1. User schreibt CAS-871 manuell   │  1. User ruft registry.add()      │
│  2. Commit                          │  2. Manager prüft + vergibt ID    │
│  3. Pre-commit findet Duplikat      │  3. CAS-910 wird automatisch      │
│  4. Commit blockiert                │     vergeben                      │
│  5. User muss manuell fixen         │  4. Duplikat UNMÖGLICH            │
└─────────────────────────────────────┴───────────────────────────────────┘
```

### Unterstützte Registries

| Registry | ID-Format | Script |
|----------|-----------|--------|
| **Case Registry** | CAS-XXX | `registry_manager.py case` |
| **Category Registry** | CAT-XX | `registry_manager.py category` |
| **Theory Registry** | MS-XX-XXX | `registry_manager.py theory --prefix XX` |
| **Parameter Registry** | PAR-XX-XXX | `registry_manager.py parameter --prefix XX` |

### CLI-Nutzung (empfohlen)

```bash
# Status aller Registries anzeigen
python scripts/registry_manager.py --status

# Nächste verfügbare ID holen
python scripts/registry_manager.py case --next           # → CAS-910
python scripts/registry_manager.py category --next       # → CAT-26
python scripts/registry_manager.py theory --next --prefix CM    # → MS-CM-003
python scripts/registry_manager.py parameter --next --prefix BEH  # → PAR-BEH-018

# Prüfen ob ID existiert
python scripts/registry_manager.py case --exists CAS-500  # → EXISTS/AVAILABLE

# Duplikate prüfen
python scripts/registry_manager.py case --validate
```

### Python API (für Scripts)

```python
from scripts.registry_manager import CaseRegistry, get_registry

# Case Registry
cases = CaseRegistry()
next_id = cases.next_id()           # CAS-910
exists = cases.exists('CAS-500')    # True/False

# Neuen Case hinzufügen (ID wird automatisch vergeben!)
new_id = cases.add({
    'name': 'My New Case',
    'domain': ['finance', 'behavior'],
    '10C': {...}
})  # → CAS-910 (automatisch, Duplikat unmöglich!)

# Via get_registry Helper
params = get_registry('par')
next_param = params.next_id('CM')   # PAR-CM-008
```

### PFLICHT-Workflow für neue Einträge

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PFLICHT bei JEDEM neuen Registry-Eintrag:                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Option A: Python API (bevorzugt)                                       │
│  ────────────────────────────────                                       │
│  from scripts.registry_manager import CaseRegistry                      │
│  cases = CaseRegistry()                                                 │
│  new_id = cases.add({'name': '...', 'domain': [...]})                  │
│                                                                         │
│  Option B: CLI → manuell einfügen                                       │
│  ────────────────────────────────                                       │
│  $ python scripts/registry_manager.py case --next                       │
│  CAS-910                                                                │
│  → Diese ID im YAML verwenden                                           │
│                                                                         │
│  VERBOTEN:                                                              │
│  ────────                                                               │
│  ❌ ID manuell "ausdenken" (z.B. CAS-500 weil "schön")                 │
│  ❌ Kopieren einer existierenden ID                                     │
│  ❌ Sequentielle ID annehmen ohne Check                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Pre-Commit Hook Integration

Der Pre-Commit Hook prüft ZUSÄTZLICH auf Duplikate (reaktive Sicherung):

```bash
# Bei jedem Commit automatisch:
python scripts/check_registry_ids.py --check

# Bei Duplikaten: Commit wird blockiert ❌
```

---

## Wichtige Dateien

| Datei | Zweck |
|-------|-------|
| `appendices/00_appendix_index.tex` | Index aller 56 Appendices |
| `appendices/00_appendix_template.tex` | Template für neue Appendices |
| `docs/frameworks/appendix-category-definitions.md` | Kategorie-Definitionen |
| `00_master_documentation_framework.tex` | Master Framework |

---

## 10C CORE Framework: Single Source of Truth

**KRITISCH:** Das 10C CORE Framework hat eine **Single Source of Truth (SSOT)**:

```
docs/frameworks/core-framework-definition.yaml  ← AUTORITATIVE DEFINITION
```

### Bei Änderungen am CORE Framework:

1. **IMMER zuerst** `core-framework-definition.yaml` aktualisieren
2. **DANN** Validierung ausführen:
   ```bash
   python scripts/validate_core_framework.py
   ```
3. **DANN** alle gemeldeten Inkonsistenzen beheben
4. **Erweiterung auf 10C, 10C:** Siehe `docs/frameworks/core-framework-extension-guide.md`

### Warum SSOT?

- Verhindert inkonsistente nC-Referenzen (z.B. "7C" vs "10C")
- Ermöglicht automatische Validierung
- Dokumentiert klaren Erweiterungspfad

---

## Chapter-Appendix Mapping: Single Source of Truth

**KRITISCH:** Die Zuordnung zwischen Kapiteln und Appendices hat eine **Single Source of Truth (SSOT)**:

```
docs/frameworks/chapter-appendix-mapping.yaml  ← AUTORITATIVE DEFINITION
```

### Bei Änderungen an Kapiteln oder Appendices:

1. **IMMER zuerst** `chapter-appendix-mapping.yaml` aktualisieren
2. **DANN** Validierung ausführen:
   ```bash
   python scripts/validate_chapter_mapping.py
   ```
3. ~~**OPTIONAL** LaTeX-Tabellen generieren~~ → **AUTOMATISCH beim Commit!**

### Workflow für neue Kapitel/Appendices:

```
1. Neue Datei erstellen (chapters/ oder appendices/)
2. YAML-Eintrag in chapter-appendix-mapping.yaml hinzufügen
3. git add + git commit → Pre-Commit Hook:
   ├── Validiert YAML automatisch
   ├── Generiert LaTeX-Tabellen automatisch
   ├── Staged 00_appendix_index.tex automatisch
   └── Staged 00_chapter_index.tex automatisch (NEU v1.14)
```

### Pre-Commit Hook (Auto-Update):

Der Pre-Commit Hook führt **automatisch** aus:
- ✅ Validiert `chapter-appendix-mapping.yaml`
- ✅ **Generiert LaTeX-Tabellen** aus YAML (Kategorie-Counts, Kapitel-Liste)
- ✅ **Updated `00_appendix_index.tex`** automatisch
- ✅ **Updated `00_chapter_index.tex`** automatisch (NEU v1.14)
- ✅ **Staged geänderte Dateien** für den Commit

Der Hook **blockiert** Commits wenn:
- Neue Kapitel/Appendices ohne YAML-Eintrag hinzugefügt werden
- Die YAML-Datei Validierungsfehler enthält
- Compliance < 85% für Kapitel/Appendices

### YAML Struktur:

```yaml
chapters:
  - number: 24
    title: "Emergent Life Journeys"
    type: C  # A=CORE, B=Foundation, C=Application
    primary_appendices: [BI, BJ, BK]

appendices:
  - code: BK
    category: METHOD
    name: CALC
    title: "EBF Calculation Reference"
    primary_chapter: 24
    secondary_chapters: [17]
```

---

## Regeln für Appendix-Erstellung

### IMMER:
1. Kategorie aus den 8 Optionen wählen
2. Template `00_appendix_template.tex` verwenden
3. Auf Appendix G (Glossary) verweisen
4. Mindestens ein Worked Example
5. Cross-References zu verwandten Appendices

### CORE Appendices zusätzlich:
1. Vollständiges Axiomensystem
2. 80-150+ Referenzen
3. 5-10 Critical Foundations
4. Bidirektionale Integration mit allen anderen COREs

### Kategorie-spezifische Required-Felder (★)

**KRITISCH:** Diese Felder sind für die jeweilige Kategorie PFLICHT und werden mit ★ markiert:

| Kategorie | Required (★) | Optional |
|-----------|--------------|----------|
| **CORE** | Axioms ★, Integration ★ | Worked Example |
| **FORMAL** | Axioms ★ | Worked Example |
| **DOMAIN** | Integration ★, Implications ★ | Axioms |
| **CONTEXT** | Integration ★ | Axioms, Worked Example |
| **METHOD** | Worked Example ★ | Axioms |
| **PREDICT** | Axioms ★, Worked Example ★ | - |
| **LIT** | References Section ★, Integration ★ | Axioms, Worked Example |
| **REF** | Worked Example ★ | Axioms |

### Compliance-Pattern Cheatsheet

**Master Bib Link** (erkannte Patterns):
- `\nocite{bcm_master}` ✅
- `bcm_master.bib` ✅
- `Master Bibliography` ✅

**Glossary G Link** (erkannte Patterns):
- `Appendix G` ✅
- `Glossary...master` ✅
- `comprehensive` (im Glossary-Kontext) ✅

**References Section** (exakte Benennung erforderlich):
- `\section{References}` ✅
- `\section{Scientific References}` ❌ (wird nicht erkannt!)
- `\section{Key References}` ❌ (wird nicht erkannt!)

---

## Namenskonvention

```
[CODE] [CATEGORY]-[NAME]: [Descriptive Title]
```

**Beispiele:**
- `AAA CORE-WHO: The Welfare Hierarchy`
- `AN METHOD-LLMMC: LLM Monte Carlo Estimation`
- `K LIT-FEHR: Ernst Fehr Research Integration`

---

## Entscheidungsbaum für neue Appendices

```
Beantwortet eine der 10C Fragen? → CORE-
Mathematische Beweise? → FORMAL-
Ökonomie-Subfeld Anwendung? → DOMAIN-
Vertieft Ψ-Dimension? → CONTEXT-
Schätzung/Messung/Validierung? → METHOD-
Testbare Vorhersagen? → PREDICT-
Literatur eines Autors? → LIT-
Hilfsmittel? → REF-
```

---

## Die 3 Kapiteltypen

**KRITISCH:** Bei Arbeit an Kapiteln IMMER den richtigen Typ beachten!

| Typ | Name | Kapitel | Besonderheit |
|-----|------|---------|--------------|
| **A** | CORE Chapter | 5, 9, 10, 11, 12, 13 | CORE Connection Box PFLICHT |
| **B** | Foundation Chapter | 1-4, 6-8 | Standard-Struktur |
| **C** | Application Chapter | 14-19 | Multiple Worked Examples PFLICHT |

### Regeln für Kapitel-Erstellung

**IMMER (alle Kapiteltypen):**
1. Template `chapters/00_chapter_template.tex` verwenden
2. Metadata-Block mit Version, Purpose, Appendices, Prerequisites
3. Appendix References Box
4. Intuition Box mit benannten Charakteren (Anna, Thomas)
5. Central Question Box
6. Chapter Overview mit Section-Referenzen
7. Reading Path Box am Ende
8. Section-Labels (`\label{sec:...}`)

**TYPE A (CORE) zusätzlich:**
1. CORE Connection Box mit Farbe (blue, green, red, etc.)
2. 10C Integration Table
3. Verbindung zu dediziertem CORE Appendix

**TYPE C (Application) zusätzlich:**
1. Multiple Worked Examples (≥2)
2. Policy Implications Section

### Kapitel-Compliance prüfen

```bash
python scripts/check_chapter_compliance.py chapters/<file>.tex
python scripts/check_chapter_compliance.py --types  # Übersicht
```

**Vollständiges Template:** `chapters/00_chapter_template.tex`

---

## Chapter-Appendix Ecosystems

**KRITISCH:** Einige Kapitel haben dedizierte Appendix-Ökosysteme mit klaren Verantwortlichkeiten.

### Chapter 24: Emergent Life Journeys

```
                 ┌─────────────┐
                 │ Chapter 24  │
                 └──────┬──────┘
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
┌─────────────────┐           ┌─────────────────┐
│ BI: LIFESPAN    │◄─────────►│ BJ: DOMAINVAL   │
│ Intergenerational│bidirektional│ Cross-Cultural │
└────────┬────────┘           └────────┬────────┘
         │                             │
    ┌────┴────┐                   ┌────┴────┐
    ▼         ▼                   ▼         ▼
┌───────┐ ┌───────┐           ┌───────┐ ┌───────┐
│  RRR  │ │  OOO  │           │  PPP  │ │  BBB  │
└───────┘ └───────┘           └───────┘ └───────┘
```

| Appendix | Kategorie | Verantwortung |
|----------|-----------|---------------|
| **BI** | DOMAIN-LIFESPAN | Intergenerational spillover, multi-generational planning |
| **BJ** | METHOD-DOMAINVAL | Cross-cultural validation, N_eff spectrum (2-7), 35+ papers |
| RRR | METHOD-LIFETIME | Domain-specific parameters, emergence conditions |
| OOO | FORMAL-SYSTEM | Complete ODE formulations for 7 domains |
| PPP | METHOD-ABM | Agent-based simulation showing emergence |
| BBB | CORE-WHERE | Literature-validated parameter values |

**Cross-References:**
- BI ↔ BJ: Bidirektional (lifecycle × cultural validation)
- Ch24 §24.6-24.7 → BJ §5-8 (WEIRD limitations, cross-cultural)
- BCM Integration → BJ §3 (FEPSDE-Ryff-BCM mapping)

---

## PFLICHT-Workflows

### Neues Kapitel erstellen (PFLICHT-Workflow)

**KRITISCH:** Bei JEDER Kapitel-Erstellung diese Schritte VOLLSTÄNDIG befolgen:

#### Phase 1: Vorbereitung
1. **Kapiteltyp bestimmen:**
   - TYPE A (CORE): Kapitel 5, 9, 10, 11, 12, 13 → CORE Connection Box PFLICHT
   - TYPE B (Foundation): Kapitel 1-4, 6-8 → Standard-Struktur
   - TYPE C (Application): Kapitel 14-19 → Multiple Worked Examples PFLICHT

2. **Kapitelnummer zuweisen** - prüfen mit: `ls chapters/*.tex`

3. **Dateiname:** `chapters/[NR]_[name].tex` (z.B. `chapters/16_behavioral_pricing.tex`)

#### Phase 2: Datei erstellen
4. **Template kopieren:** `cp chapters/00_chapter_template.tex chapters/[NR]_[name].tex`

5. **Pflicht-Elemente ausfüllen (ALLE Typen):**
   - Metadata Block (Version, Purpose, Primary Appendix, Prerequisites, Leads to, Chapter Type)
   - Quick Reference Box (Begriffe in diesem Kapitel)
   - Appendix References Box
   - **Chapter Scope Box (NEU v1.11):** Ziel / In-Scope / Out-of-Scope / Lieferobjekte
   - Intuition Box mit benannten Charakteren (Anna, Thomas, Maria...)
   - Central Question Box
   - Chapter Overview mit Section-Referenzen
   - Section Labels (`\label{sec:...}`) für ALLE Subsections
   - Reading Path Box am Ende

6. **Typ-spezifische Elemente:**
   - **TYPE A:** CORE Connection Box (farbig) + 10C Integration Table
   - **TYPE C:** Multiple Worked Examples (≥2) + Policy Implications Section

#### Phase 3: Compliance prüfen
7. **Compliance-Check:**
   ```bash
   python scripts/check_chapter_compliance.py chapters/<datei>.tex
   ```
8. **Score ≥ 85% erforderlich** - bei niedrigerem Score fehlende Elemente ergänzen

#### Phase 4: Navigation aktualisieren
9. **Reading Path im VORHERIGEN Kapitel** aktualisieren (→ neues Kapitel hinzufügen)
10. **Reading Path im FOLGENDEN Kapitel** aktualisieren (falls vorhanden)
11. **Kapitel-Index prüfen** (falls vorhanden in Master-Dokument)

#### Phase 5: Cross-References
12. **Appendix-Verweise:** Relevante Appendices im Kapitel referenzieren
13. **Kapitel-Verweise in Appendices:** Rück-Referenzen hinzufügen

#### Phase 6: Commit
14. **Commit mit vollständiger Message:**
    ```bash
    git add chapters/[NEUE_DATEI].tex
    git commit -m "feat(Ch[NR]): Add new chapter on [TOPIC]"
    ```

#### Checkliste vor Commit
```
☐ Compliance ≥ 85%
☐ Kapiteltyp korrekt (A/B/C)
☐ Metadata Block vollständig
☐ Chapter Scope Box mit Ziel/In-Scope/Out-of-Scope/Lieferobjekte (NEU)
☐ Intuition Box mit benanntem Charakter
☐ Central Question Box vorhanden
☐ Chapter Overview mit \ref{} Links
☐ Alle Sections haben \label{sec:...}
☐ Reading Path Box am Ende
☐ TYPE A: CORE Connection Box vorhanden
☐ TYPE C: ≥2 Worked Examples vorhanden
☐ Navigation: Vorheriges Kapitel aktualisiert
☐ Cross-References zu Appendices
```

### Bei Kapitel-Änderungen (PFLICHT)

**KRITISCH:** Bei JEDER Änderung an Kapiteldateien diese Schritte befolgen:

1. **VOR dem Commit: Compliance prüfen**
   ```bash
   python scripts/check_chapter_compliance.py chapters/<geänderte_datei>.tex
   ```

2. **Score ≥ 85% erforderlich** für Commit
   - Bei Score < 85%: Fehlende Elemente ergänzen
   - Bei Score < 70%: Kapitel nicht committen bis behoben

3. **Fehlende Elemente beheben:**
   - ❌ Metadata Block → Header mit Version, Purpose, Appendices hinzufügen
   - ❌ Chapter Scope Box → Ziel/In-Scope/Out-of-Scope/Lieferobjekte Box hinzufügen (NEU)
   - ❌ Intuition Box → Beispiel mit Anna/Thomas hinzufügen
   - ❌ Central Question → Zentrale Frage Box hinzufügen
   - ❌ Chapter Overview → Section-Übersicht mit \ref{} hinzufügen
   - ❌ Reading Path → Reading Path Box am Ende hinzufügen
   - ❌ Section Labels → \label{sec:...} zu allen Subsections

4. **Nach Behebung: Erneut prüfen**
   ```bash
   python scripts/check_chapter_compliance.py chapters/<datei>.tex
   ```

5. **Erst dann committen**

**Typ-spezifische Anforderungen:**
- TYPE A (CORE): CORE Connection Box + 10C Integration Table PFLICHT
- TYPE C (Application): Multiple Examples + Policy Implications PFLICHT

### Neues Paper integrieren (PFLICHT-Workflow: /integrate-paper)

> **Gesamtübersicht Paper-Workflow:** `docs/workflows/paper-workflow-overview.md`

**KRITISCH:** Bei JEDEM neuen wissenschaftlichen Paper MUSS der `/integrate-paper` Workflow verwendet werden!

#### ⚠️ AUTOMATISCHE TRIGGER (für Claude)

**WENN einer dieser Trigger erkannt wird:**

| # | Trigger | Beispiel |
|---|---------|----------|
| TR1 | Paper-Titel genannt | "Consumer Demand and Market Competition..." |
| TR2 | DOI oder NBER Working Paper | "10.3386/w34743", "NBER WP 34743" |
| TR3 | Autoren + Jahr genannt | "Goodman et al. (2026)" |
| TR4 | Paper-Abstract geteilt | "We leverage Becker's time allocation theory..." |
| TR5 | "Neues Paper", "Paper hinzufügen" | User-Request für Paper-Integration |

**DANN MUSS Claude SOFORT:**

```
1. "Ich erkenne ein neues Paper. Starte /integrate-paper Workflow..."
2. Paper klassifizieren (7 Kriterien, automatisch)
3. Integration Level bestimmen (1-5)
4. Komponenten-Checkliste generieren
5. Integration durchführen (geführt)
```

#### Integration Levels

| Level | Name | Komponenten | Zeit |
|-------|------|-------------|------|
| **1** | MINIMAL | BibTeX | 5 min |
| **2** | STANDARD | BibTeX + theory_support + Parameter (optional) | 10-15 min |
| **3** | CASE | BibTeX + theory_support + Case Registry | 15-20 min |
| **4** | THEORY | BibTeX + Theory Catalog (MS-XX-XXX) + Parameter | 20-30 min |
| **5** | FULL | Alle 8 Komponenten (neue Kategorie/Domain) | 60-90 min |

#### Klassifikations-Kriterien (7)

| Kriterium | Gewicht | Indikatoren |
|-----------|---------|-------------|
| **new_theory_category** | 5 | "new framework", "unified theory", "foundational" |
| **extends_existing_theory** | 3 | "extends", "builds on", "application of" |
| **new_domain** | 4 | "first study", "digital platform", "emerging" |
| **empirical_parameters** | 2 | "we estimate", "coefficient", "λ =", "β =" |
| **policy_implications** | 2 | "policy", "regulation", "nudge", "antitrust" |
| **field_experiment** | 2 | "field experiment", "RCT", "natural experiment" |
| **case_study_worthy** | 1 | "case study", "real-world", "practical" |

#### Level-Bestimmung (automatisch)

```
Score ≥ 20 + (new_theory_category ≥ 10 ODER new_domain ≥ 8)  → Level 5: FOUNDATIONAL
Score ≥ 15 + extends_theory + parameters                      → Level 4: THEORY
Score ≥ 10 + (case_study_worthy ODER field_experiment)        → Level 3: CASE
Score ≥ 5 + (extends_theory ODER parameters)                  → Level 2: STANDARD
Sonst                                                          → Level 1: MINIMAL
```

#### ⚠️ KRITISCHE ZUSATZPRÜFUNG: Framework vs. Estimation Paper

**NACH der automatischen Level-Bestimmung IMMER fragen:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LIEFERT DAS PAPER SELBST PUNKT-SCHÄTZUNGEN?                            │
│                                                                         │
│  JA  → Level bleibt wie berechnet                                       │
│        (z.B. λ = 2.25 aus eigenem Experiment → Level 4 THEORY)          │
│                                                                         │
│  NEIN → Prüfen ob Level 5 FOUNDATIONAL!                                 │
│        Wenn Paper nur Framework etabliert, andere Papers die            │
│        Schätzungen liefern → Level 5 FOUNDATIONAL                       │
│                                                                         │
│  BEISPIELE FÜR LEVEL 5 FOUNDATIONAL:                                    │
│  ├── Kahneman & Tversky (1979) - Prospect Theory Framework              │
│  ├── Becker (1965) - Household Production Framework                     │
│  ├── Cunha & Heckman (2007) - Skill Formation Technology                │
│  └── Heckman et al. (2023) - Virtue Ethics Framework                    │
│                                                                         │
│  Bei Level 5 FOUNDATIONAL: Parameter-Werte als "Informed Priors"        │
│  aus verwandter Literatur markieren, NICHT als direkte Schätzungen!     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Lesson Learned (2026-02-05):** Ein Paper kann hohen Score haben (z.B. 19) und trotzdem Level 5 FOUNDATIONAL sein, wenn es das theoretische GERÜST etabliert aber selbst KEINE Punkt-Schätzungen liefert. Die Parameter-Werte (z.B. δ_S ≈ 0.15) kommen dann aus anderer Literatur und müssen als "Informed Priors" gekennzeichnet werden.

#### Workflow-Details nach Level

**Level 1: MINIMAL**
```
☐ BibTeX-Eintrag in bcm_master.bib
  ├── Basis-Felder (title, author, year, journal, doi)
  └── use_for = {LIT-O} oder passender LIT-Appendix
```

**Level 2: STANDARD**
```
☐ BibTeX-Eintrag mit EBF-Feldern
  ├── theory_support = {MS-XX-XXX}
  ├── use_for = {LIT-XX, DOMAIN-XX}
  └── parameter = {...} (falls vorhanden)

☐ Parameter Registry (optional)
  └── Nur wenn neue/bessere Schätzungen
```

**Level 3: CASE**
```
☐ Level 2 Komponenten

☐ Case Registry (data/case-registry.yaml)
  ├── 10C Mapping
  ├── Formulas
  ├── References
  └── Insight + Implication
```

**Level 4: THEORY**
```
☐ Level 2/3 Komponenten

☐ Theory Catalog (data/theory-catalog.yaml)
  ├── Neuer MS-XX-XXX Eintrag
  ├── ebf_restrictions
  ├── validity
  └── bib_keys
```

**Level 5: FULL (Vollständige Integration)**
```
☐ Theory Catalog: Neue Kategorie CAT-XX + Theorien

☐ Bibliography: Paper + Foundational Papers

☐ Model Registry: Neues Modell MOD-XX-XXX
  ├── Variables
  ├── Functional form
  └── Theory basis

☐ Parameter Registry: Alle neuen Parameter PAR-XX-XXX

☐ Case Registry: Worked Example Case

☐ Paper-YAML (data/paper-references/PAP-*.yaml)        ← SSOT!
  ├── parameter_contributions mit measurement_contexts
  ├── theory_integration (theory_id)
  ├── case_integration (case_id)
  └── chapter_relevance

☐ LaTeX Appendix (appendices/)
  ├── DOMAIN-XX oder LIT-XX
  ├── Axiome
  ├── Worked Examples
  └── Cross-References

☐ Chapter-Appendix Mapping
  └── docs/frameworks/chapter-appendix-mapping.yaml

☐ Formal Proofs (DER)
  └── appendices/DER_formal_derivations.tex
```

**ATOMIC SYMBOL RULE:** Jedes EBF-Parameter-Symbol ist **eineindeutig** (z.B. λ_R statt λ).

**ATOMIC ID RULE:** Paper-YAML ist SSOT für alle IDs (theory_id, case_id, parameter IDs).

**MEASUREMENT CONTEXTS (PFLICHT bei Level 5):**
```yaml
parameter_contributions:
  - symbol: "λ_R"                    # EBF-eindeutiges Symbol
    ebf_id: "PAR-BEH-016"            # Parameter-Registry ID
    measurement_contexts:            # ← PFLICHT für Level 5
      - context: "welfare_takeup"
        value_estimate: "high (λ_R ≈ 2.5)"
        psi_conditions:              # Ψ-Dimension Kontext
          Ψ_I: "bureaucratic_application"
          Ψ_S: "welfare_stigma"
        source_in_paper: "Section 6.2"
        study_type: "field_data"
        countries: ["USA"]
```

**PARAMETER CONTEXT TRANSFORMATION (PCT):**
```
θ_B = θ_A × ∏ᵢ M(ΔΨᵢ)

Aus measurement_contexts ableiten:
1. Anchor Context (θ_A, Ψ_A) aus Paper-YAML wählen
2. Target Context (Ψ_B) für neues Projekt definieren
3. Ψ-Differenzen berechnen: ΔΨᵢ = Ψ_B - Ψ_A
4. Multiplikatoren anwenden → θ_B schätzen
```

**Vollständige Dokumentation:** `docs/workflows/level5-paper-integration-workflow.md`

#### CORE-Appendix Integration: 6-Faktoren-Entscheidung (Level 5)

**KRITISCH:** Bei Level 5 muss für JEDEN der 10 COREs geprüft werden, ob das Paper strukturellen Mehrwert liefert.

**Die 6 Faktoren:**

| # | Faktor | Frage | JA → CORE erweitern | NEIN → nur Referenz |
|---|--------|-------|---------------------|---------------------|
| **F1** | Strukturelle Novelty | Führt Paper NEUE Komponente/Dimension ein? | Neuer Formalismus | Nutzt bestehenden Formalismus |
| **F2** | Axiom-Beitrag | Ermöglicht Paper NEUES Axiom? | Axiom formulieren | Existierendes Axiom stützen |
| **F3** | Dimensionalität | Ändert sich Dimensionalität des CORE-Raums? | z.B. A: 4→5 Komponenten | Gleiche Struktur |
| **F4** | Parameter vs Struktur | Struktureller oder parametrischer Beitrag? | Struktur → CORE | Parameter → WHERE (BBB) |
| **F5** | Universalität | Gilt Beitrag ALLGEMEIN? | Allgemein → CORE | Spezifisch → LIT/DOMAIN |
| **F6** | Mechanismus | Erklärt Paper NEUEN Wirkungsmechanismus? | Neuer Mechanismus | Anwendung bekannter |

**Entscheidungsbaum:**
```
Paper P soll in CORE-X integriert werden?
│
├── F1: Neue strukturelle Komponente für X?
│   ├── NEIN → Nur Cross-Referenz in CORE-X
│   └── JA ──┐
│            │
│            ├── F5: Gilt universell (nicht nur für diesen Autor/Domain)?
│            │   ├── NEIN → In LIT/DOMAIN, Cross-Referenz in CORE
│            │   └── JA ──┐
│            │            │
│            │            └── CORE-X erweitern mit:
│            │                • Neue Komponente/Dimension
│            │                • Neues Axiom (wenn F2=JA)
│            │                • Cross-Referenz zu LIT für Details
│            │
│            └── Parameter-Werte → WHERE (BBB), nicht CORE-X
```

**Architektur-Prinzip:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│  LIT-Appendix           = PRIMARY LOCATION (vollständige Formalisierung)│
│  CORE-Appendix          = CROSS-REF + STRUCTURAL EXTENSION (wenn F1-F6) │
│  WHERE (BBB)            = PARAMETER VALUES (μ, β, ρ Schätzungen)       │
└─────────────────────────────────────────────────────────────────────────┘
```

**Beispiel: Bénabou/Falk/Tirole (2018)**
| CORE | F1? | F2? | F5? | Entscheidung |
|------|-----|-----|-----|--------------|
| AWARE (AU) | ✅ A_moral | ✅ AWX-A5 | ✅ | CORE erweitern |
| WHEN (V) | ✅ ρ in Ψ_S | ❌ | ✅ | CORE erweitern |
| HOW (B) | ✅ γ(N) | ✅ CMP-11 | ✅ | CORE erweitern |
| WHAT (C) | ❌ μv̂ existiert | - | - | Nur Referenz |
| READY (AV) | ❌ β ist Parameter | - | - | → WHERE |

#### Verwendung

```bash
# Interaktiv (empfohlen)
/integrate-paper

# Mit DOI
/integrate-paper --doi 10.3386/w34743

# Nur Klassifikation (ohne Integration)
/integrate-paper --classify-only

# Via Script
python scripts/classify_paper_integration.py --interactive
python scripts/classify_paper_integration.py --title "..." --abstract "..."
```

#### PFLICHT-Regel

**JEDES neue Paper MUSS durch `/integrate-paper` laufen.**

**VERBOTEN:**
```
❌ Paper manuell in BibTeX einfügen ohne Klassifikation
❌ "Das mache ich schnell ohne Workflow"
❌ Theory hinzufügen ohne vorherige Klassifikation
❌ Ad-hoc Level-Entscheidung ohne Kriterien-Check
```

**ERLAUBT / ERFORDERLICH:**
```
✅ IMMER /integrate-paper bei neuem Paper
✅ Automatische Klassifikation vor Integration
✅ Level-Entscheidung basiert auf 7 Kriterien
✅ Alle Komponenten des Levels vollständig abarbeiten
```

#### Workflow-Override Regel

Ein Override des `/integrate-paper` Workflows ist **NUR gültig** wenn ALLE 4 Bedingungen erfüllt sind:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  OVERRIDE-BEDINGUNGEN (alle 4 müssen erfüllt sein!)                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Claude HAT den Workflow gestartet                                   │
│  2. Claude HAT das automatisch bestimmte Level genannt                  │
│  3. Claude FRAGT EXPLIZIT: "Möchtest du trotzdem Level X?"              │
│  4. Der User BEJAHT diese Frage                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Beispiel (korrekt):**
```
User: "Füge Paper X auf Level 1 hinzu"
Claude: "Ich starte /integrate-paper. Die Klassifikation ergibt:
         Score 18 → Level 4 (THEORY).
         Du hast Level 1 genannt. Möchtest du den Workflow
         überschreiben und nur Level 1 machen?"
User: "Ja"
→ Override gültig ✅
```

**Beispiel (VERBOTEN):**
```
User: "Füge Paper X auf Level 1 hinzu"
Claude: *fügt Paper auf Level 1 hinzu ohne Klassifikation*
→ WORKFLOW-VERLETZUNG ❌
```

#### Bevorzugte Alternative zum Override

Bevor ein Override in Betracht gezogen wird, sollte geprüft werden ob das Problem nicht besser gelöst werden kann:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WENN das automatisch bestimmte Level falsch erscheint:                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  OPTION A (bevorzugt): Workflow verbessern                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  1. Klassifikations-Kriterien überprüfen                                │
│  2. Falls systematischer Fehler → Workflow/Script anpassen              │
│  3. Verbesserung kommt ALLEN zukünftigen Papers zugute                  │
│                                                                         │
│  OPTION B (falls nötig): Override mit 4 Bedingungen                     │
│  ─────────────────────────────────────────────────────────────────────  │
│  → Nur für Einzelfälle, die nicht systematisch lösbar sind              │
│  → Alle 4 Override-Bedingungen müssen erfüllt sein                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Vollständige Dokumentation:** `.claude/commands/integrate-paper.md`

---

### 🔄 Content Level Auto-Upgrade (PFLICHT - Automatisch, OHNE zu fragen!)

> **Detail:** `docs/workflows/paper-workflow-overview.md` → Content Levels

**KRITISCH:** Wenn Paper-Content geteilt wird, upgradet Claude AUTOMATISCH - ohne den User zu fragen!

#### Auto-Trigger Situationen

| Situation | Aktion | Fragen? |
|-----------|--------|---------|
| User teilt Paper-Text (PDF, Abstract, etc.) | Auto-Upgrade auf passendes Level | **NEIN** |
| User teilt DOI | Auto-Fetch + Upgrade wenn möglich | **NEIN** |
| Paper in Session referenziert mit C<L2 | Auto-Upgrade wenn Content verfügbar | **NEIN** |
| Upgrade nicht möglich (Copyright, etc.) | User informieren | Nur dann |

#### Workflow (intern, für Claude)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  User teilt Paper-Content                                               │
│                                                                         │
│  Claude (INTERN - ohne User zu fragen):                                 │
│    1. Erkennt: "Das ist Paper-Content"                                 │
│    2. Prüft: Paper bereits in DB? → PAP-xxx gefunden, C=L1             │
│    3. Extrahiert: S1-S6 aus Text                                       │
│       S1=Research Question, S2=Methodology, S3=Sample/Data             │
│       S4=Findings, S5=Validity, S6=Reproducibility                     │
│    4. Bestimmt: Neues Level basierend auf Vollständigkeit              │
│       L1: S1 (Research Question) vorhanden                             │
│       L2: S1+S2+S3+S4 vorhanden ODER Summary/Extract                  │
│       L3: COMPLETE original text mit References (R1-R4 erfüllt)        │
│           R1: Alle Original-Sektionen vorhanden                        │
│           R2: References-Sektion mit allen Zitaten                     │
│           R3: >10k Wörter (Artikel) / >5k (Short Paper)               │
│           R4: KEINE EBF-Sektionen im Volltext                          │
│    5. Speichert: full_text → data/paper-texts/PAP-xxx.md               │
│       WICHTIG: Nur ORIGINAL-Text, KEINE EBF-Analyse im .md!           │
│       EBF-Metadaten gehören in PAP-xxx.yaml, NICHT in .md             │
│    6. Aktualisiert: YAML → content_level, prior_score                  │
│    7. Validiert: python scripts/validate_fulltext_completeness.py      │
│    8. Committed: automatisch mit Nachricht                             │
│                                                                         │
│  Claude (zum User):                                                     │
│    "[Antwort auf die eigentliche Frage]                                │
│                                                                         │
│     📊 Paper-Update: PAP-xxx L1→L3 (automatisch)"                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### VERBOTEN / ERLAUBT

**VERBOTEN:**
```
❌ "Soll ich das Paper upgraden?"
❌ "Möchtest du, dass ich den Content Level aktualisiere?"
❌ Paper-Content ignorieren und nur Frage beantworten
❌ Upgrade auf später verschieben
❌ Summary/Extract als L3 klassifizieren (ist L2!)
❌ EBF-Analyse-Sektionen in die .md Volltext-Datei schreiben
❌ "Key Parameters Extracted" oder "EBF Framework Relevance" in .md
```

**ERLAUBT / ERFORDERLICH:**
```
✅ Automatisch upgraden wenn Content verfügbar
✅ Am Ende der Antwort kurz informieren: "📊 Paper-Update: ..."
✅ Bei Copyright-Problemen informieren (einzige Ausnahme)
✅ IMMER References-Sektion im Volltext behalten (wertvollste Daten!)
✅ Separation of Concerns: .md = Original-Text, .yaml = EBF-Metadaten
✅ validate_fulltext_completeness.py nach jedem Upgrade ausführen
```

---

### Neues Konzept integrieren (PFLICHT-Workflow: Evidence Integration Pipeline)

**KRITISCH:** Bei JEDER Integration eines neuen Konzepts die **Evidence Integration Pipeline (EIP)** befolgen!

#### ⚠️ AUTOMATISCHE TRIGGER (für Claude)

**WENN einer dieser Trigger erkannt wird:**

| # | Trigger | Beispiel |
|---|---------|----------|
| TR1 | Neue Terminologie eingeführt | "Mental Identity Budgeting" |
| TR2 | Neuer Mechanismus beschrieben | "$I_{\text{WHAT},F} \to I_{\text{WHO}}$ Transformation" |
| TR3 | Neue γ-Werte behauptet | "γ(AWARE,WHEN) = +0.4" |
| TR4 | Neue Formel/Gleichung entwickelt | "Z(n) = Z_max × (1-0.03×...)" |
| TR5 | Neue Intervention vorgeschlagen | "Benefits Choice Box" |

**DANN MUSS Claude:**

```
1. SOFORT pausieren und Trigger benennen
2. "Ich erkenne ein neues Konzept. Starte EIP..."
3. INTERNE QUELLEN ZUERST prüfen:
   a) bcm_master.bib ({PAPER_COUNT} Papers)
   b) LIT-Appendices (R/D/M/O)
   c) Case Registry
4. Nur wenn nötig: externe Quellen (Google Scholar)
5. PRO + CONTRA Evidenz dokumentieren
6. Entscheidung: Integrieren / Verwerfen / Modifizieren
7. In concept-registry.yaml dokumentieren
```

**NIEMALS:** Konzept ohne EIP-Prüfung integrieren!

**Tracking:** `data/concept-registry.yaml` (alle EIP-Entscheidungen)
**Verworfene Konzepte:** `quality/rejected_concepts.md`

**Vollständige Dokumentation:** `docs/workflows/evidence-integration-pipeline.md`

#### Die 5 Stufen

```
STUFE 1: Konzept entwickelt
    ↓
STUFE 2: Literaturrecherche (PRO + CONTRA Papers)
    ↓
STUFE 3: Entscheidung (Integrieren / Verwerfen / Modifizieren)
    ↓
STUFE 4: Framework-Integration (Appendix + Kapitel)
    ↓
STUFE 5: Paper-Integration (BibTeX + LIT + Zitate)
```

#### Kurzfassung

| Stufe | Aktion | Output |
|-------|--------|--------|
| 1 | Konzept dokumentieren | `concept_id`, `proposed_location` |
| 2 | PRO-Papers suchen (≥3) | `pro_evidence[]` |
| 2 | CONTRA-Papers AKTIV suchen | `contra_evidence[]` |
| 3 | Entscheidungsmatrix anwenden | `integrate/reject/modify` |
| 4 | Appendix + Kapitel identifizieren | `appendix_integration`, `chapter_integration` |
| 5a | Papers in `bcm_master.bib` | BibTeX-Einträge |
| 5b | Papers in LIT-Appendix | LIT-R/M/O Zuordnung |
| 5c | Papers als Evidenz zitieren | `\citep{}` in Appendix |

#### Checkliste

```
☐ PRO-Evidenz gesucht (≥3 Papers)
☐ CONTRA-Evidenz AKTIV gesucht
☐ Entscheidung dokumentiert
☐ Alle Papers in bcm_master.bib
☐ Alle Papers in korrektem LIT-Appendix (R/M/O)
☐ Papers als Evidenz in Appendix zitiert
```

#### VERBOTEN

- ❌ Konzept ohne Evidenz integrieren
- ❌ Contra-Evidenz ignorieren
- ❌ Papers zitieren ohne LIT-Integration
- ❌ Ad-hoc Konzepte ohne EIP-Workflow

---

### Innosuisse-Projekt Aufgaben (PFLICHT-Workflow via `/innosuisse` Skill)

**KRITISCH:** Bei JEDER Aufgabe im Innosuisse-Projekt (BEATRIX) MUSS der `/innosuisse` Skill verwendet werden!

**SSOT:** Der vollständige Workflow ist in `.claude/commands/innosuisse.md` definiert.

#### ⚠️ AUTOMATISCHER TRIGGER (für Claude)

**WENN eine dieser Bedingungen zutrifft:**
- Datei in `docs/funding/` wird bearbeitet
- Begriffe "Innosuisse", "BEATRIX", "Innovation Cheque" erscheinen
- Dokument-Adaption oder Version-Update angefragt
- Meeting-Transkript verarbeitet wird

**DANN MUSS Claude SOFORT:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  /innosuisse SKILL AUTO-AKTIVIERUNG                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. User informieren: "Ich erkenne ein Innosuisse/BEATRIX-Projekt.     │
│     Starte /innosuisse Workflow..."                                     │
│                                                                         │
│  2. Lerndatenbank konsultieren:                                         │
│     python scripts/query_learnings.py --stats                           │
│                                                                         │
│  3. Fehlerprävention anwenden:                                          │
│     → 8 Fehlertypen-Checkliste durchgehen                               │
│     → Relevante Learnings identifizieren                                │
│                                                                         │
│  4. Nach Abschluss: Neue Learnings dokumentieren via /innosuisse add   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**VERBOTEN:**
```
❌ BEATRIX-Dokument bearbeiten OHNE /innosuisse Workflow
❌ "Das mache ich schnell ohne Checkliste"
❌ Kernaussage ändern ohne 7-Stellen-Prüfung
❌ Version-Update ohne 3-Stellen-Prüfung
❌ Vollständigkeit BEHAUPTEN ohne grep -n BEWEIS
```

#### Fehlertypen-Präventions-Checkliste (VOR jeder Aufgabe prüfen!)

| Error Type | Prävention | Prüfbefehl |
|------------|-----------|------------|
| **CONSISTENCY** | Alle betroffenen Stellen identifizieren | `grep -n "<Begriff>" <datei>.tex` |
| **CLASSIFICATION** | Inhalte kategorisieren (inhaltlich vs. organisatorisch) | Teilnehmer-Liste mit Input-Typ erstellen |
| **VERIFICATION** | Vollständigkeit mit Nachweisen belegen | `grep -c` Ergebnisse zeigen |
| **OUTPUT_FORMAT** | Format klären bevor Arbeit beginnt | "Welches Format benötigen Sie?" |
| **DOMAIN_KNOWLEDGE** | Interne Dokumentation konsultieren | Lerndatenbank nach Keywords durchsuchen |
| **TOOL_SEQUENCE** | Standard-Workflows befolgen | Rename → Read → Edit |
| **CHECKLIST** | Systematische Prüfung durchführen | 7-Stellen-Checkliste für Kernaussagen |
| **ASSUMPTION** | Bei Unklarheit nachfragen | Keine Annahmen ohne Bestätigung |

#### Spezifische Regeln für BEATRIX-Dokumente

**Kernaussagen (7 Stellen prüfen!):**
```
☐ 1. Abstract
☐ 2. Säulen-Titel (subsubsection)
☐ 3. Säulen-Haupttext
☐ 4. "Warum ist das neu?"-Abschnitt
☐ 5. Summary-Box (fbox)
☐ 6. Gesamtzusammenfassung-Tabelle
☐ 7. Glossar-Eintrag
```

**Versionsnummern (3 Stellen prüfen!):**
```
☐ Header/Kommentar-Block (Zeile 1-6)
☐ Titelseite (\large Version X.X)
☐ Footer (\small Version: X.X)
```

**BEATRIX-Kernbeschreibung (KRITISCH - Ernst Fehr Korrektur):**
```
✅ RICHTIG: "erfasst Wechselwirkungen, die in der Realität stattfinden"
✅ RICHTIG: "psychologische, finanzielle, kulturelle Effekte"
✅ RICHTIG: "schlägt Massnahmen vor"

❌ FALSCH: "Wechselwirkungen zwischen Massnahmen"
❌ FALSCH: "analysiert Massnahmen"
```

#### Workflow nach Abschluss

1. **Neue Learnings identifizieren:**
   - Was lief nicht wie erwartet?
   - Welche Fehler wurden gemacht?
   - Was hätte verhindert werden können?

2. **Learning dokumentieren:**
   ```yaml
   id: "INO-L-YYYY-MM-DD-CAT-NNN"
   error_type: "<TYPE>"
   concrete_example: "Was genau ist passiert?"
   ```

3. **Commit:**
   ```bash
   git commit -m "feat(learning): Add learning INO-L-..."
   ```

#### Quick Commands

**Via Skill (empfohlen):**
```bash
/innosuisse                    # Workflow starten
/innosuisse check              # Lerndatenbank konsultieren
/innosuisse query --error-type CONSISTENCY
/innosuisse add                # Neues Learning hinzufügen
/innosuisse stats              # Statistiken anzeigen
```

**Via Script:**
```bash
# Statistiken anzeigen
python scripts/query_learnings.py --stats

# Nach Fehlertyp filtern
python scripts/query_learnings.py --error-type CONSISTENCY

# Nach Kategorie filtern
python scripts/query_learnings.py --category DOC

# Volltextsuche
python scripts/query_learnings.py --search "version"

# Alle Learnings anzeigen
python scripts/query_learnings.py --all
```

---

## 🤖 Model Routing (PFLICHT bei Task-Delegation)

> **SSOT:** `data/model-routing.yaml`
> **PRINZIP:** Opus denkt, Sonnet/Haiku arbeitet.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MODEL ROUTING — Bei JEDEM Task(subagent_type=...) konsultieren!        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DEFAULT: Opus 4.6 (wenn keine Regel greift)                            │
│                                                                         │
│  AUSNAHMEN (definiert in data/model-routing.yaml):                      │
│                                                                         │
│  HAIKU ($0.80/1M):                                                      │
│  ├── file_search:        Dateien suchen, Grep, Glob                     │
│  ├── validation_check:   Schema-Validierung, Compliance                 │
│  └── format_conversion:  Einfache Format-Konvertierungen                │
│                                                                         │
│  SONNET ($3.00/1M):                                                     │
│  ├── paper_integration:  Paper lesen, BIB/YAML erstellen                │
│  ├── paper_metadata:     Metadaten extrahieren                          │
│  ├── registry_entry:     Case/Theory/Parameter Einträge                 │
│  ├── document_drafting:  Dokumente nach Template                        │
│  └── batch_processing:   Batch-Verarbeitung bekannter Patterns          │
│                                                                         │
│  OPUS ($15.00/1M):                                                      │
│  ├── ebf_analysis:       EBF-Modelling, 10C, Kontext                    │
│  ├── strategic_reasoning: Strategie, Kundenberatung                     │
│  ├── cross_reference:    Level 5, CORE-Integration                      │
│  ├── quality_assessment: EIP, Bewertung, Forecast                       │
│  └── conversation:       Direkte User-Interaktion (DEFAULT)             │
│                                                                         │
│  WORKFLOW:                                                              │
│  1. Task-Typ aus Aufgabe ableiten                                       │
│  2. model-routing.yaml → passendes Modell                               │
│  3. Task(model="sonnet/haiku", ...) aufrufen                            │
│  4. Wenn unklar → Default: opus                                         │
│  5. User kann jederzeit überschreiben                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Experiment-First + Empfehlungs-Workflow (PFLICHT bei JEDEM Task)

> **KRITISCH:** Bei JEDER Coding-Aufgabe MUSS dieser Workflow befolgt werden.
> SSOT: `data/task-log.yaml` (Unified Task Database)

### 🔴 Active-Task Marker (Context-Compaction-Resilient)

**KRITISCH:** Der Active-Task Marker überlebt Context Compaction und Session-Resumes.

**Datei:** `.claude/active-task.yaml` (in .gitignore — lokaler Session-State)

**PROTOCOL (PFLICHT):**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BEI TASK-START (nach 3-Tier-Box Approval):                             │
│  → .claude/active-task.yaml schreiben mit:                              │
│    active_task:                                                         │
│      task_id: "TL-XXX"                                                  │
│      description: "..."                                                 │
│      tier: "quick_win|medium|large"                                     │
│      coding_mode: "TRADITIONAL|EXPERIMENTAL"                            │
│      step: "implementing"                                               │
│      started: "2026-02-12T..."                                          │
│      context_for_resume: "Kurzbeschreibung für Context-Recovery"        │
│                                                                         │
│  BEI CONTEXT COMPACTION / "weiter" / Session Resume:                    │
│  → ZUERST .claude/active-task.yaml LESEN                                │
│  → Falls active_task existiert: Task fortsetzen (nicht neu starten!)    │
│  → Falls null: Normal fortfahren (3-Tier-Box bei neuem Task)            │
│                                                                         │
│  BEI TASK-ABSCHLUSS:                                                    │
│  → active_task: null setzen                                             │
│  → TL-Entry in task-log.yaml mit outcome + ebf_impact abschliessen     │
│                                                                         │
│  LESSON LEARNED (TL-070):                                               │
│  Ohne Active-Task Marker → Context Compaction → Workflow vergessen      │
│  → Alle 6 PFLICHT-Schritte übersprungen → Kompletter Workflow-Ausfall   │
└─────────────────────────────────────────────────────────────────────────┘
```

**ENFORCEMENT:**
- Pre-Commit Hook warnt wenn ≥3 Dateien staged aber kein in_progress Task
- Pre-Commit Hook warnt STARK wenn ≥6 Dateien staged ohne Task
- `check_task_completion.py` validiert outcome/ebf_impact bei Commit

### 🔴 Session-Kontext Protocol (Modell-Awareness)

**KRITISCH:** Der Session-Kontext trackt welche Modelle und Themen in der aktuellen Session aktiv sind.
Ohne dieses Tracking werden eigene Modelle bei Fragen ignoriert (LESSON LEARNED 2026-02-13: PSF-2.0 bei Konklave-Frage übersehen).

**Datei:** `.claude/session-context.yaml` (in .gitignore — lokaler Session-State)

**PROTOCOL (PFLICHT):**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BEI JEDER INHALTLICHEN FRAGE:                                          │
│                                                                         │
│  1. session-context.yaml LESEN                                          │
│     → Gibt es aktive Modelle/Themen?                                    │
│     → Ist die aktuelle Frage verwandt?                                  │
│                                                                         │
│  2. MODELL-MATCHING durchführen                                         │
│     → Keywords aus Frage extrahieren                                    │
│     → Gegen use_cases in models/models.registry.yaml matchen            │
│     → Gegen active_themes in session-context.yaml matchen               │
│                                                                         │
│  3. Bei MATCH: Modell AKTIV einbeziehen                                 │
│     → Modell-Daten laden (README, model-definition.yaml)                │
│     → In Antwort referenzieren                                          │
│     → In session-context.yaml als active_model eintragen                │
│                                                                         │
│  4. session-context.yaml AKTUALISIEREN                                  │
│     → Neue Themen/Keywords eintragen                                    │
│     → last_query aktualisieren                                          │
│     → matched_models dokumentieren                                      │
│                                                                         │
│  BEI CONTEXT COMPACTION / Session Resume:                               │
│  → ZUERST session-context.yaml LESEN                                    │
│  → Aktive Modelle und Themen wiederherstellen                          │
│  → NICHT bei Null anfangen!                                             │
│                                                                         │
│  LESSON LEARNED (2026-02-13):                                           │
│  PSF-2.0 war 100% relevant für Konklave/Sutter-Interview,              │
│  wurde aber ignoriert weil kein Modell-Matching stattfand.              │
│  → 6 unnötige WebSearches statt 1 interner Modell-Lookup.              │
└─────────────────────────────────────────────────────────────────────────┘
```

**MATCHING-ALGORITHMUS:**
```
Frage-Keywords = tokenize(user_query)
FOR EACH model IN models.registry.yaml:
    overlap = Frage-Keywords ∩ model.use_cases
    IF |overlap| >= 1:
        → Modell ist KANDIDAT
    IF |overlap| >= 3:
        → Modell ist HOCHRELEVANT → PFLICHT zu laden
```

### 🔴 Mandatory Trigger Check (PFLICHT bei JEDER Nachricht)

**SSOT:** `data/mandatory-triggers.yaml` — Konsolidierter Index aller Auto-Trigger.

**PROTOCOL (PFLICHT — VOR jeder inhaltlichen Antwort!):**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MANDATORY TRIGGER CHECK (bei JEDER User-Nachricht!)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: data/mandatory-triggers.yaml LESEN (oder aus Memory)        │
│                                                                         │
│  SCHRITT 2: User-Nachricht gegen trigger_words matchen:                 │
│  ├── T-MODEL:       IMMER (use_cases in models.registry.yaml)           │
│  ├── T-PAPER:       "paper", "DOI", "10.xxxx", "et al.", "NBER"        │
│  ├── T-INNOSUISSE:  "innosuisse", "beatrix", "innovation cheque"       │
│  ├── T-INTERVENTION:"intervention", "nudge", "massnahme", "toolkit"    │
│  ├── T-SPO:         "spö", "babler", "vizekanzler"                      │
│  ├── T-EIP:         "neues konzept", "neue formel", "neuer mechanismus"│
│  ├── T-REW:         "validiere", "ebf-konform", "reverse engineering"  │
│  └── T-UPGRADE:     Paper-Content erkannt (Abstract, Volltext, DOI)     │
│                                                                         │
│  SCHRITT 3: Bei Match → Skill/Workflow SOFORT starten                   │
│  ├── T-PAPER       → /integrate-paper                                   │
│  ├── T-INNOSUISSE  → /innosuisse                                       │
│  ├── T-INTERVENTION→ /design-intervention                               │
│  ├── T-SPO         → Präambel Loading Protocol (PLP)                    │
│  ├── T-EIP         → Evidence Integration Pipeline                      │
│  ├── T-REW         → Reverse Engineering Workflow                       │
│  └── T-UPGRADE     → Content Level Auto-Upgrade                         │
│                                                                         │
│  SCHRITT 4: Session-Obligations prüfen                                  │
│  ├── O-MODUS:  Modus-Wahl anzeigen (erste inhaltliche Frage)           │
│  ├── O-3TIER:  3-Tier-Box nach Task-Abschluss                          │
│  ├── O-QUEUE:  Paper Queue (mindestens 1/Session)                       │
│  ├── O-CODING: Coding Mode (TRADITIONAL/EXPERIMENTAL)                   │
│  └── O-TASKLOG:Task in task-log.yaml loggen                             │
│                                                                         │
│  ⚠️  VERBOTEN:                                                           │
│  ❌ Trigger matcht aber Skill wird NICHT gestartet                       │
│  ❌ "Das mache ich schnell ohne Workflow"                                │
│  ❌ Trigger-Check überspringen weil "offensichtlich kein Trigger"        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Pre-Response Checkliste (VOR jeder Antwort mental durchgehen!)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ✅ PRE-RESPONSE CHECKLISTE (bei JEDER Antwort!)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  □ 0a. EIGENE MODELLE geprüft? → session-context.yaml + Registry!      │
│        ⚠️  ZUERST models.registry.yaml use_cases matchen!               │
│  □ 0b. MANDATORY TRIGGERS?    → data/mandatory-triggers.yaml!          │
│        T-PAPER? T-INNOSUISSE? T-INTERVENTION? T-SPO? T-EIP? T-REW?    │
│  □ 1. Ist das ein Task?        → JA: 3-Stufen-Box PFLICHT              │
│  □ 2. Problem verstanden?      → NEIN: erst analysieren                │
│  □ 3. Habe ich einen Default?  → NEIN: erst nachdenken                 │
│  □ 4. Wurde gerade ein Task    → JA: SOFORT nächste 3-Tier-Box!        │
│       abgeschlossen?             NICHT fragen "Soll ich...?"           │
│  □ 5. Steht PAUSIEREN am Ende? → NEIN: hinzufügen                     │
│                                                                         │
│  ANTI-PATTERN ERKENNUNG:                                                │
│  "Soll ich...?" in meiner Antwort? → STOPP! Umformulieren als Box!     │
│  "Was möchtest du...?" nach Task?  → STOPP! Empfehlung mit Default!    │
│  WebSearch OHNE Modell-Check?      → STOPP! Erst Schritt 0 prüfen!    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Workflow (3 Schritte vor jeder Arbeit)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 1: EMPFEHLUNG (IMMER zuerst!)                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  3-Stufen-Format:                                                       │
│  ├── Quick Win:              [kleine, schnelle Verbesserung]            │
│  ├── Mittlere Verbesserung:  [substanzieller Fortschritt]              │
│  └── Grössere Übung:         [umfassende Lösung]                       │
│                                                                         │
│  Default: [EINE Stufe empfehlen + Begründung aus EBF-Kontext]          │
│                                                                         │
│  ⚠️  DANN PAUSIEREN und auf User-Bestätigung warten!                    │
│  ⚠️  KEINE Zeitschätzungen ohne Evidenz aus task-log.yaml!              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 2: CODING-MODE ENTSCHEIDEN                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TRADITIONAL (direkt ausführen):                                        │
│  ├── ≤5 Dateien betroffen                                               │
│  ├── Bekanntes Pattern                                                  │
│  └── ≤500 Zeilen Output                                                │
│                                                                         │
│  EXPERIMENTAL (1→10→100→all):                                           │
│  ├── >5 Dateien betroffen                                               │
│  ├── Neues/unbekanntes Pattern                                          │
│  └── >500 Zeilen Output                                                │
│                                                                         │
│  Algorithmus-SSOT: data/coding-mode-algorithm.yaml                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 3: TASK LOGGEN (in task-log.yaml)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  VOR Arbeitsbeginn:                                                     │
│  ├── Neuen Eintrag mit status: in_progress                              │
│  ├── recommendation, coding_mode, features ausfüllen                   │
│  └── timing.start setzen                                                │
│                                                                         │
│  NACH Abschluss:                                                        │
│  ├── timing.completed + duration_min setzen (gemessen!)                 │
│  ├── outcome.status + result ausfüllen                                 │
│  ├── ebf_impact ausfüllen (what_improved, measurable, enables_next)    │
│  ├── learning dokumentieren (falls vorhanden)                           │
│  └── ⚠️  SOFORT nächste 3-Tier-Box zeigen! (NICHT fragen!)              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  ⚠️  POST-TASK REGEL (PFLICHT nach JEDEM abgeschlossenen Task!)          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  NACH jedem Task-Abschluss SOFORT:                                      │
│  1. Nächsten logischen Task identifizieren                              │
│  2. 3-Tier-Box zeigen (Quick Win / Mittel / Gross)                     │
│  3. Default empfehlen mit EBF-Kontext-Begründung                       │
│  4. PAUSIEREN — auf User-Bestätigung warten                            │
│                                                                         │
│  ANTI-PATTERN (3× aufgetreten → strukturell verboten):                  │
│  ❌ "Soll ich die restlichen X machen?"                                 │
│  ❌ "Was möchtest du als nächstes?"                                     │
│  ❌ "Soll ich weitermachen?"                                            │
│  ❌ Jede Frage statt Empfehlung nach Task-Abschluss                    │
│                                                                         │
│  KORREKT:                                                               │
│  ✅ "Task TL-XXX abgeschlossen. Hier ist die nächste Empfehlung:"      │
│  ✅ → 3-Tier-Box mit [DEFAULT] → PAUSE                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3 Lernschleifen

| Schleife | Was wird gelernt | Datenquelle |
|----------|------------------|-------------|
| **Default-Kalibrierung** | Richtige Stufe empfehlen (Akzeptanzrate) | recommendation.accepted_default |
| **Coding-Mode-Kalibrierung** | TRADITIONAL vs EXPERIMENTAL (Wann was?) | coding_mode + timing |
| **Outcome/EBF-Impact** | Bringt die Aktion das EBF weiter? | ebf_impact + learning |

### VERBOTEN

```
❌ Task starten ohne Empfehlung (3-Stufen-Format)
❌ Empfehlung zeigen und sofort loslegen (ohne User-Bestätigung!)
❌ Zeitschätzungen ohne Log-Evidenz aus task-log.yaml
❌ Generische Empfehlungen (müssen EBF-Kontext-abhängig sein)
❌ Task abschliessen ohne outcome + ebf_impact
❌ Coding-Mode ignorieren (TRADITIONAL/EXPERIMENTAL Entscheidung PFLICHT)
❌ Nach Task-Abschluss FRAGEN statt EMPFEHLEN ("Soll ich...?" verboten!)
❌ Nach Task-Abschluss ohne nächste 3-Tier-Box weitermachen
```

### Referenz-Dateien

| Datei | Zweck |
|-------|-------|
| `data/task-log.yaml` | SSOT: Alle Tasks, Empfehlungen, Outcomes, Learnings |
| `data/coding-mode-algorithm.yaml` | Entscheidungsalgorithmus TRADITIONAL/EXPERIMENTAL |

---

## Häufige Aufgaben

> **Paper-Workflows auf einen Blick:** `docs/workflows/paper-workflow-overview.md`
> Dort: Architektur-Diagramm, alle SSOTs, Skills, Levels, Deprecated-Liste.

### Neues Paper aufnehmen (PFLICHT-Workflow: Paper Intake Protocol)

> **Gesamtübersicht Paper-Workflow:** `docs/workflows/paper-workflow-overview.md`

**KRITISCH:** Bei JEDER Paper-Aufnahme das **Paper Intake Protocol (PIP)** befolgen!

#### ⚠️ TRIGGER-ANWEISUNG (für Claude)

**WENN ein neues wissenschaftliches Paper hinzugefügt werden soll:**
- User teilt Paper-Abstract, DOI, oder Titel
- User fragt "Können wir dieses Paper integrieren?"
- Neues Paper wird während EIP gefunden

**DANN MUSS Claude:**
1. Prüfen ob Paper bereits in `bcm_master.bib` existiert
2. Falls neu: `/add-paper` Workflow starten
3. PIP-Datei erstellen in `data/paper-intake/YYYY/`
4. BibTeX-Eintrag mit allen EBF-Feldern hinzufügen

#### PIP-Struktur (7 Sections)

| Section | Status | Inhalt |
|---------|--------|--------|
| **1. Identifikation** | ★ PFLICHT | Paper-ID, PIP-ID, bibliografische Daten |
| 2. Entdeckungskontext | Optional | Wie wurde Paper gefunden? |
| 3. Qualitätsbewertung | Optional | Evidence Tier, Methodik, Limitationen |
| **4. EBF-Integration** | ★ PFLICHT | 10C-Dimensionen, Theorien, use_for, Parameter |
| **5. Entscheidung** | ★ PFLICHT | Accept/Reject/Conditional + Begründung |
| 6. Cross-References | Optional | Verwandte Papers, Appendices, Chapters |
| 7. Follow-up | Optional | Ausstehende Aktionen, Update-Trigger |

#### Evidence Tiers

| Tier | Beschreibung | Beispiele |
|------|--------------|-----------|
| **1 (Gold)** | RCT, Top-5 Journal, repliziert | QJE, AER, Econometrica |
| **2 (Silver)** | Peer-reviewed, solide Methodik | JF, MS, JEBO, NBER |
| **3 (Bronze)** | Working Paper, theoretisch | SSRN, Preprints |

#### Workflow via Skill

```bash
/add-paper                           # Interaktiver Modus
/add-paper "10.3386/w34727"          # Mit DOI
/add-paper --quick                   # Nur Pflichtfelder
```

#### Workflow manuell

```bash
# 1. Template kopieren
cp data/paper-intake/template.yaml data/paper-intake/2026/PIP-YYYY-MM-DD-NNN.yaml

# 2. Pflicht-Sections ausfüllen (1, 4, 5)

# 3. BibTeX hinzufügen mit EBF-Feldern:
#    evidence_tier, use_for, theory_support, parameter,
#    identification, external_validity, session_ref, notes

# 4. Commit
git add data/paper-intake/ bibliography/bcm_master.bib
git commit -m "feat(paper): Add [Author] [Year] via PIP-YYYY-MM-DD-NNN"
```

#### Checkliste vor Abschluss

```
☐ PIP-ID korrekt: PIP-YYYY-MM-DD-NNN
☐ Paper-ID korrekt: PAP-nachnamejahrkurzwort
☐ Mindestens eine 10C-Dimension zugeordnet
☐ use_for enthält mindestens einen Eintrag
☐ Entscheidung (accept/reject) mit Begründung
☐ BibTeX-Eintrag mit allen EBF-Feldern
☐ PIP-Datei in data/paper-intake/YYYY/
```

#### Referenz-Dateien

| Datei | Beschreibung |
|-------|--------------|
| `data/paper-intake/README.md` | Vollständige PIP-Dokumentation |
| `data/paper-intake/template.yaml` | Leeres PIP-Template |
| `data/paper-intake/2026/PIP-2026-01-28-001.yaml` | Beispiel (Al-Najjar & Uhlig) |
| `.claude/commands/add-paper.md` | Skill-Dokumentation |

---

### Neue Prognose erstellen (PFLICHT-Workflow: Forecast Protocol)

**KRITISCH:** Bei JEDER Prognose-Erstellung das **Forecast Protocol** befolgen!

#### ⚠️ TRIGGER-ANWEISUNG (für Claude)

**WENN eine Prognose erstellt werden soll:**
- User fragt nach Wahrscheinlichkeit eines Ereignisses
- User fragt nach Abstimmungsausgang
- User fragt "Wie wahrscheinlich ist..."
- Geopolitische, politische, wirtschaftliche Vorhersage

**DANN MUSS Claude:**
1. Forecast-Registry prüfen (existiert bereits?)
2. Modell auswählen oder erstellen
3. Prognose in **VIER Datenbanken** schreiben
4. Report erstellen und registrieren

#### Datenbank-Architektur (4 Datenbanken)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FORECAST-DATENBANK-ARCHITEKTUR                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1️⃣  FORECAST-REGISTRY (PRIMÄR)     data/forecast-registry.yaml        │
│      → FCT-{DOMAIN}-{YYYY}-{NNN}                                       │
│      → Prognose, Szenarien, Probability History, Kalibrierung          │
│                                                                         │
│  2️⃣  MODEL-BUILDING-SESSION         data/model-building-session.yaml   │
│      → EBF-S-{YYYY}-{MM}-{DD}-{DOMAIN}-{NNN}                           │
│      → Session-Dokumentation, Kontext, Parameter                       │
│      → forecast_registry_link: "FCT-..."                               │
│                                                                         │
│  3️⃣  MODEL-REGISTRY (falls neu)     data/model-registry.yaml           │
│      → MOD-{DOMAIN}-{NNN}                                              │
│      → Nur wenn NEUES Modell erstellt wurde                            │
│                                                                         │
│  4️⃣  OUTPUT-REGISTRY                data/output-registry.yaml          │
│      → EBF-OUT-{DOMAIN}-{NNN}                                          │
│      → Report-Metadaten, Pfad                                          │
│      → forecast_registry_link: "FCT-..."                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Domains

| Domain | Beschreibung | Beispiel |
|--------|--------------|----------|
| **POL** | Politische Abstimmungen, Wahlen | SRG-Initiative, 10-Mio |
| **GEO** | Geopolitische Ereignisse | Iran-Angriff, Ukraine |
| **ECO** | Wirtschaftsprognosen | Rezession, Inflation |
| **FIN** | Finanzmarkt-Prognosen | Zinsen, Wechselkurse |
| **BEH** | Verhaltensvorhersagen | Adoption, Compliance |
| **ORG** | Organisationale Outcomes | Projekte, M&A |

#### Workflow: Neue Prognose

```bash
# 1. Prognose erstellen (Analyse durchführen)
#    → Modell wählen/erstellen
#    → Parameter bestimmen
#    → P, CI, Szenarien berechnen

# 2. In VIER Datenbanken schreiben:

# 2a. Forecast-Registry (PRIMÄR)
# → Neuer Eintrag mit FCT-ID, probability_history, scenarios

# 2b. Model-Building-Session
# → Session dokumentieren mit forecast_registry_link

# 2c. Model-Registry (falls neues Modell)
# → MOD-ID nur wenn neues Modell erstellt

# 2d. Output-Registry
# → Report registrieren mit forecast_registry_link

# 3. Report erstellen
# → outputs/sessions/{SESSION_ID}/

# 4. Commit
git add data/forecast-registry.yaml data/model-building-session.yaml \
        data/output-registry.yaml outputs/
git commit -m "feat(forecast): Add [TITEL] (FCT-XXX-YYYY-NNN)"
```

#### Workflow: Prognose updaten

```yaml
# Neuen Eintrag in probability_history hinzufügen:
probability_history:
  - date: "2026-01-28"
    probability: 0.18
    # ... existierender Eintrag

  - date: "2026-02-15"      # ← NEUER EINTRAG
    probability: 0.45       # ← Neue Schätzung
    confidence: "MEDIUM"
    reasoning: |
      [Was hat sich geändert?]
    key_drivers:
      positive: [...]
      negative: [...]
    updated_by: "Update Grund"
```

#### Workflow: Prognose auflösen (nach Event)

```yaml
# Nach Eintreten/Nicht-Eintreten des Events:
actual_outcome:
  resolved: true
  date: "2026-03-08"
  result: "nein"  # oder "ja", "attack", "no_attack"
  details: "52.1% NEIN"
  source: "BFS"

calibration:
  brier_score: 0.04  # (0.52 - 0.521)²
  direction_correct: true
```

#### Checkliste: Neue Prognose

```
☐ FCT-ID korrekt: FCT-{DOMAIN}-{YYYY}-{NNN}
☐ Forecast-Registry: Eintrag mit probability_history
☐ Model-Building-Session: Session mit forecast_registry_link
☐ Output-Registry: Report mit forecast_registry_link
☐ Model-Registry: Falls neues Modell (MOD-ID)
☐ Report erstellt in outputs/sessions/
☐ Resolution Criteria definiert (was zählt als Ja/Nein?)
☐ Git commit + push
```

#### Referenz-Dateien

| Datei | Beschreibung |
|-------|--------------|
| `data/forecast-registry.yaml` | Alle Prognosen mit History |
| `appendices/PREDICT-FCT_forecast_methodology.tex` | Methodologie-Appendix |
| `.claude/commands/forecast.md` | Skill-Dokumentation (TODO) |

---

### Neuen Appendix erstellen (PFLICHT-Workflow)

**KRITISCH:** Bei JEDER Appendix-Erstellung diese Schritte VOLLSTÄNDIG befolgen:

#### Phase 1: Vorbereitung
1. **Kategorie bestimmen** (Entscheidungsbaum oben)
2. **Code-Verfügbarkeit prüfen** - KRITISCH! (siehe unten)
   ```bash
   python scripts/check_appendix_available.py <CODE>
   ```
   - ✅ Verfügbar: Code kann verwendet werden
   - ❌ In Benutzung: `--suggest` verwenden für nächsten Code
3. **Namenskonvention:** `[CODE] [CATEGORY]-[NAME]: [Title]`

#### Phase 2: Datei erstellen
4. **Template kopieren:** `cp appendices/00_appendix_template.tex appendices/[CATEGORY]-[NAME]_[desc].tex`
5. **Pflicht-Elemente ausfüllen:**
   - Header Block (Category, Version, Dependencies)
   - Cross-Reference Map
   - Chapter Linkage
   - Abstract + Quick Reference
   - Fundamental Question
   - Theory + Results + Integration
   - Summary
   - Glossary Section (mit Link zu Appendix G)
   - Critical Foundations
   - Open Issues
   - References Section (mit `\nocite{bcm_master}`)

#### Phase 3: Compliance prüfen
6. **Compliance-Check:**
   ```bash
   python scripts/check_template_compliance.py appendices/<datei>.tex
   ```
7. **Score ≥ 85% erforderlich** - bei niedrigerem Score fehlende Elemente ergänzen

#### Phase 4: Index aktualisieren (ALLE 4 Stellen!)
8. **Haupttabelle** (ca. Zeile 430): `AH & DOMAIN-CONSULTING & ...`
9. **Status-Tabelle** (ca. Zeile 612): `AH & DOMAIN-CONSULTING: ... & Domain & High`
10. **Reading-Path-Tabelle** (ca. Zeile 898): `AH & DOMAIN-CONSULTING & LIT-META & Ch. 14`
11. **Kategorie-Count erhöhen** (ca. Zeile 68): z.B. `DOMAIN- & ... & 13` → `14`

#### Phase 5: Cross-References
12. **Ausgehende Links** im neuen Appendix zu verwandten Appendices
13. **Eingehende Links** in verwandten Appendices zum neuen Appendix hinzufügen

#### Phase 6: Commit
14. **Commit mit vollständiger Message:**
    ```bash
    git add appendices/[NEUE_DATEI].tex appendices/00_appendix_index.tex
    git commit -m "feat([CODE]): Add new appendix on [TOPIC]"
    ```

#### Checkliste vor Commit
```
☐ Compliance ≥ 85%
☐ Glossary G Link vorhanden
☐ Master Bib Link vorhanden (\nocite{bcm_master})
☐ Index: Haupttabelle aktualisiert
☐ Index: Status-Tabelle aktualisiert
☐ Index: Reading-Path aktualisiert
☐ Index: Kategorie-Count erhöht
☐ Cross-References bidirektional
```

### Appendix bearbeiten
1. Kategorie-Anforderungen prüfen
2. Konsistenz mit Appendix G sicherstellen
3. Cross-References aktualisieren

### Kategorie-Frage beantworten
→ Siehe `docs/frameworks/appendix-category-definitions.md`

### Neues Dokument erstellen (PFLICHT-Workflow: 8D-Algorithmus)

**KRITISCH:** Bei JEDER Erstellung eines neuen Dokumentes (Paper, Brief, Report, Proposal, etc.) den **8D-Algorithmus** aus Appendix CCC/DDD anwenden!

#### Warum 8D?

Der 8D-Algorithmus ist ein universelles Framework, das für **jeden** Dokumenttyp die passende Struktur, Style und Vokabular **automatisch generiert** basierend auf der Zielgruppe.

#### Phase 1: Zielgruppe charakterisieren (8D-Koordinaten)

Für das neue Dokument die 8 Dimensionen bestimmen:

| D | Dimension | Frage | Skala |
|---|-----------|-------|-------|
| D₁ | Wissen | Wie expert ist die Zielgruppe? | 0=Laie → 1=Expert |
| D₂ | Nähe | Wie nah am Fachgebiet? | 0=Fern → 1=Gleiches Feld |
| D₃ | Reichweite | Persönlich oder gesellschaftlich? | 0=Persönlich → 1=Gesellschaftlich |
| D₄ | Zeit | Wieviel Lesezeit verfügbar? | 0=Wenig → 1=Viel |
| D₅ | Ziel | Was ist das Kommunikationsziel? | G₁-G₇ (siehe unten) |
| D₆ | Kontext | Intern oder extern? | 0=Intern → 1=Extern/Öffentlich |
| D₇ | Emotion | Sachlich oder emotional? | 0=Sachlich → 1=Emotional |
| D₈ | Persistenz | Kurzlebig oder archiviert? | 0=Kurzlebig → 1=Archiv |

**D₅ Ziel-Kategorien:**
- G₁ = Informieren, G₂ = Handeln auslösen, G₃ = Überzeugen
- G₄ = Unterhalten, G₅ = Erleben, G₆ = Verbinden, G₇ = Ausdrücken

#### Phase 2: Struktur emergieren lassen (Axiom DT-5, DT-6)

Aus den 8D-Koordinaten emergiert automatisch die Struktur:
```
D₁ > 0.7 → Technical Glossary erforderlich
D₄ < 0.3 → Executive Summary erforderlich
D₄ > 0.6 → Detaillierte Subsections erlaubt
D₅ = G₁  → Theory/Methods Section erforderlich
D₅ = G₂  → Call-to-Action Box erforderlich
D₈ > 0.8 → References + Version Control erforderlich
```

#### Phase 3: Style emergieren lassen (Axiom DT-7, DT-8)

Aus den 8D-Koordinaten emergiert automatisch der Style:
```
D₁ > 0.7 → Fachvokabular erlaubt, Flesch-Kincaid ≥ 14
D₁ < 0.3 → Einfache Sprache, Flesch-Kincaid ≤ 8
D₄ > 0.6 → Komplexe Sätze erlaubt (>20 Wörter)
D₆ > 0.7 → Formelles Register, Passiv akzeptabel
D₇ < 0.3 → Unpersönlicher Stil, keine Narrative
D₈ > 0.8 → Hedging erforderlich ("suggests", "may")
```

#### Phase 4: Vocabulary emergieren lassen (Axiom DT-9)

Aus dem Style emergiert automatisch das Vokabular:
```
Hedging=True   → "suggests", "may", "indicates", "appears"
Register=Formal → "therefore", "consequently", "however"
Pronouns=False  → "the study", "the analysis", "results"
```

#### Phase 5: Output generieren (Regeln O-1, O-2)

Aus den 8D-Koordinaten emergiert automatisch das Output-Format:

**Regel O-1 (Format-Auswahl):**
```
D₈ > 0.6 oder (D₆ > 0.8 und D₁ > 0.7) → LaTeX
0.3 < D₈ ≤ 0.6                        → Markdown
D₈ ≤ 0.3                              → Plain Text
```

**Regel O-2 (Auto-Compile):**
```
Format = LaTeX und D₈ > 0.5 → PDF automatisch kompilieren
```

**Script-Aufruf:**
```bash
python scripts/generate_paper.py appendices/<input>.tex --style fehr --output outputs/
```

**Style-Varianten:**
| Variante | Template | Charakteristik |
|----------|----------|----------------|
| `fehr` | AER/JPE | Formale Modelle, testbare Hypothesen, experimentelles Design |
| `thaler` | AER/JPE | Zugänglich, Anomalien-first, praktische Implikationen |
| `kahneman` | Science/Nature | Dual-System Framing, Heuristiken, breite Zielgruppe |
| `sunstein` | Policy | Regulatorischer Fokus, Kosten-Nutzen, Implementation |

#### Beispiel-Profile

| Dokumenttyp | D₁ | D₂ | D₃ | D₄ | D₅ | D₆ | D₇ | D₈ |
|-------------|----|----|----|----|----|----|----|----|
| **Journal Paper** | 0.9 | 0.9 | 0.7 | 0.8 | G₁ | 1.0 | 0.1 | 0.95 |
| **Policy Brief** | 0.6 | 0.4 | 0.85 | 0.3 | G₂ | 1.0 | 0.25 | 0.7 |
| **Internal Memo** | 0.5 | 0.8 | 0.3 | 0.2 | G₁ | 0.0 | 0.15 | 0.4 |
| **Blog Post** | 0.3 | 0.2 | 0.5 | 0.3 | G₁ | 1.0 | 0.5 | 0.3 |
| **EBF Appendix** | 0.85 | 0.75 | 0.6 | 0.7 | G₁ | 1.0 | 0.15 | 0.9 |

#### Referenz-Appendices

- **Appendix CCC (METHOD-DOCTYPE):** Computational Implementation mit Python-Code
- **Appendix DDD (REF-DOCTYPE):** Theoretische Grundlagen, Axiome DT-1 bis DT-9

#### Checkliste vor Dokumenterstellung
```
☐ 8D-Koordinaten für Zielgruppe bestimmt
☐ Struktur aus DT-5/DT-6 abgeleitet
☐ Style aus DT-7/DT-8 abgeleitet
☐ Vocabulary aus DT-9 abgeleitet
☐ Passendes Template gewählt oder erstellt
☐ Output-Format via O-1 bestimmt (LaTeX/Markdown/Plain)
☐ Auto-Compile via O-2 geprüft (D₈ > 0.5 → PDF)
☐ Script ausgeführt: python scripts/generate_paper.py
```

#### ⚠️ NACH 8D: Document Production Workflow (DPW) starten!

**8D** bestimmt WAS geschrieben wird. **DPW** bestimmt WIE produziert wird.

```
8D-Algorithmus (Inhalt)          DPW (Produktion)
─────────────────────────────    ─────────────────────────────
Was schreiben?                   Wie produzieren?
Welcher Style?                   Welches Format?
Welches Vokabular?               Wie kompilieren?
                                 Welche Qualitäts-Gates?

        ↓                                ↓
   CONTENT DESIGN                  PRODUCTION WORKFLOW
        ↓                                ↓
        └──────────────┬─────────────────┘
                       ↓
              FERTIGES DOKUMENT
```

**Standard-Workflow starten:** `/doc`

**OKB-Referenz:** `OKB-001` → `docs/okb/OKB-001-document-production.md`

**Learnings vor Start lesen:** L1-L6 (75+ min Zeitersparnis pro Projekt)

---

### Verhaltensmodell designen (PFLICHT-Workflow: EEE Workflow)

**KRITISCH:** Bei JEDER Modelldesign-Anfrage den **EEE Workflow** (Appendix EEE: METHOD-DESIGN) verwenden!

**Single Source of Truth:** Der Skill `/design-model` implementiert den standardisierten 9-Schritt-Workflow mit 3+1 Choice Architecture.

#### Phase 0: Workflow-Modus wählen

Verwenden Sie den Skill `/design-model` und wählen Sie einen der 4 Modi:

| Modus | Beschreibung | Zeit | Resultat |
|-------|-------------|------|----------|
| **⚡ SCHNELL** | 3 Fragen → komplettes 10C Modell via GGG Defaults | 10 min | Sofort einsatzbereit |
| **🎯 GEFÜHRT** | Alle 9 Steps mit Erklärungen & 3+1 Optionen | 45 min | Umfassend dokumentiert |
| **📦 TEMPLATE** | Seed-Modell aus FFF Registry anpassen | 20 min | Validiertes Fundament |
| **🔧 CUSTOM** | Freie Gestaltung mit allen 9 Steps | Variabel | Maximal kontrolliert |

```bash
/design-model
/design-model --mode schnell
/design-model --mode geführt
/design-model --mode template
/design-model --mode custom
```

#### Die 9 Steps (EEE Workflow)

1. **Entry Point:** Theory-Driven oder Practice-Driven?
2. **Scope Definition:** Decision, Continuous, oder Process?
3. **Context Specification (Ψ):** Kontext-Dimensionen mit GGG Defaults
4. **Variable Selection (C, γ):** Utility-Dimensionen mit GGG Defaults
5. **Functional Form:** Mathematische Formulierung
6. **Parameter Estimation (Θ):** Woher die Zahlen? (Literatur/Empirisch/Hybrid)
7. **Predictions:** Testbare Vorhersagen (Point/Interval/Comparative)
8. **Model Registry:** In FFF speichern (Metadata + Validation Status)
9. **Output Generation:** Format wählen (LaTeX/Markdown/Python)

#### 3+1 Choice Architecture

Bei jedem Step: **3 kuratierte Optionen + 1 Custom Option**

Die 3 Optionen basieren auf:
- **GGG Mapping Tables** (vorkonfigurierte Defaults)
- **FFF Seed Models** (validierte Referenzmodelle)
- **Best Practices** aus Fehr/Thaler/Kahneman Literatur

#### Referenz-Appendices

| Appendix | Kategorie | Zweck |
|----------|-----------|-------|
| **EEE** | METHOD-DESIGN | 9-Step Workflow + Axiome MD-1 bis MD-4 |
| **GGG** | METHOD-CONFIG | Mapping Tables + Defaults (7 Tabellen) |
| **FFF** | METHOD-REGISTRY | Seed Models (8 DACH Referenzmodelle) |
| **AAA-HI** | CORE | 10C Fragen (WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, STAGE) |
| **BBB** | CORE | Parameter Repository (Literaturwerte) |

#### Checkliste: "Habe ich EEE korrekt verwendet?"

```
☐ Skill `/design-model` verwendet (nicht ad-hoc vorgegangen)
☐ Mit Phase 0 (Modus-Wahl) gestartet
☐ Mindestens einen der 4 Modi gewählt
☐ 3+1 Choice Architecture bei jedem Step eingehalten
☐ Alle 10C Dimensionen (AAA-HI) beantwortet
☐ GGG Configurator für Defaults verwendet
☐ FFF Registry für Seed-Modelle geprüft
☐ Model in FFF Registry registriert (Step 8)
☐ Output-Format gewählt und generiert (Step 9)
☐ Validation-Review geplant (12-Monats-Zyklus)
```

#### Fehler vermeiden

❌ **Nicht:** Ad-hoc Fragen stellen (ohne EEE Struktur)
✅ **Stattdessen:** Immer `/design-model` mit Step 0 starten

❌ **Nicht:** Defaults selbst erfinden
✅ **Stattdessen:** GGG Mapping Tables verwenden

❌ **Nicht:** Modelle in Isolation designen
✅ **Stattdessen:** FFF Registry für ähnliche Modelle prüfen

**Weitere Details:** `.claude/commands/design-model.md`

---

### 🔴 CONTEXT-FIRST: Die Goldene Regel

---

## 🎯 WARUM KONTEXT? (Das Wichtigste zuerst)

### Die eine Erkenntnis, die alles verändert:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   DIESELBE FRAGE + ANDERER KONTEXT = KOMPLETT ANDERE ANTWORT            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Ein Beispiel, das jeder versteht:

**Frage:** *"Soll ich mehr sparen?"*

```
KONTEXT A: 25-jährige Berufseinsteigerin, Schweiz, 85k Gehalt, keine Schulden
→ Antwort: "Ja, 3. Säule nutzen, Steuern sparen, Zeit ist dein Freund"

KONTEXT B: 58-jähriger Witwer, Deutschland, arbeitslos, pflegebedürftige Mutter
→ Antwort: "Nein, Liquidität sichern, Sozialleistungen prüfen"

KONTEXT C: 40-jährige Unternehmerin, Österreich, 3 Kinder, Firma in Krise
→ Antwort: "Kommt drauf an - Firma retten oder Exit planen?"
```

**Ohne Kontext ist JEDE Antwort falsch.**

---

### Warum Menschen den Kontext nicht selbst liefern:

| Grund | Erklärung |
|-------|-----------|
| 🐟 **Fisch im Wasser** | Kontext ist unsichtbar - wie ein Fisch das Wasser nicht bemerkt |
| 🧠 **Fundamental Attribution Error** | Menschen erklären Verhalten durch Persönlichkeit, nicht Situation |
| 📚 **Curse of Knowledge** | Was für dich offensichtlich ist, erwähnst du nicht |
| ⚡ **System 1** | Schnelles Denken = keine Kontext-Reflexion |

**→ Deshalb muss ICH (Claude) den Kontext AKTIV analysieren!**

---

### Was Kontext für dich bedeutet (als User):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  OHNE KONTEXTANALYSE          │  MIT KONTEXTANALYSE                     │
│  ─────────────────────────────│──────────────────────────────────────── │
│  "Hier sind 5 Tipps..."       │  "In DEINER Situation (CH, 45J,         │
│                               │   Energie-Branche, Zeitdruck)           │
│  Generische Ratschläge        │   ist der wichtigste Hebel X,           │
│  die vielleicht passen        │   weil Y in diesem Kontext gilt"        │
│                               │                                         │
│  Copy-Paste von ChatGPT       │  Massgeschneiderte Analyse              │
│                               │                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 DIE 8 KONTEXT-DIMENSIONEN (Chapter 9: Ψ-Framework)

**Formale Grundlage:** Chapter 9 + Appendix V (CORE-WHEN)

Jede Situation hat 8 Dimensionen, die Verhalten beeinflussen:

```
┌──────────────────────────────────────────────────────────────────────────┐
│  DIE 8 Ψ-DIMENSIONEN (intuitiv)                                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  📋 Ψ_I  REGELN      Welche Gesetze, Defaults, Vorschriften gelten?      │
│  👥 Ψ_S  SOZIAL      Wer ist dabei? Welche sozialen Normen?              │
│  🧠 Ψ_C  KOPF        Müde? Gestresst? Aufmerksam? Motiviert?             │
│  🌍 Ψ_K  KULTUR      Welche Werte, Traditionen, Religion?                │
│  💰 Ψ_E  RESSOURCEN  Wieviel Budget, Zeit, Energie verfügbar?            │
│  ⏰ Ψ_T  ZEIT        Wann? Zeitdruck? Welche Lebensphase?                │
│  🔧 Ψ_M  TOOLS       Welche Technologie, Infrastruktur, Objekte?         │
│  📍 Ψ_F  ORT         Wo physisch? Zuhause, Büro, öffentlich, online?     │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Warum 8 Dimensionen?** Weil dieselbe Person dieselbe Entscheidung **anders trifft** wenn:
- andere REGELN gelten (Opt-in vs. Opt-out)
- andere LEUTE dabei sind (allein vs. beobachtet)
- sie in anderem ZUSTAND ist (ausgeruht vs. erschöpft)
- andere KULTUR gilt (CH vs. DE vs. TR)
- andere RESSOURCEN da sind (reich vs. knapp)
- anderer ZEITPUNKT ist (Montag früh vs. Freitag spät)
- andere TOOLS verfügbar sind (Papier vs. App)
- anderer ORT ist (Zuhause vs. Amt)

---

## 🔍 WIE DIE KONTEXTANALYSE AUSSIEHT

**Bevor ich antworte, zeige ich dir den erkannten Kontext:**

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 KONTEXT                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WER fragt?     → [Was ich über dich/die Situation weiss]   │
│  WAS genau?     → [Kernthema deiner Frage]                  │
│  WARUM wichtig? → [Was auf dem Spiel steht]                 │
│                                                             │
│  Ψ-DIMENSIONEN (die relevanten):                            │
│  → Ψ_K: [Kultur/Werte]                                      │
│  → Ψ_I: [Regeln/Defaults]                                   │
│  → Ψ_S: [Soziale Situation]                                 │
│                                                             │
│  DARUM GILT:    → [Was das für meine Antwort bedeutet]      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Das ist keine Bürokratie - das ist Qualitätssicherung.**

Du siehst sofort:
- Ob ich deine Frage richtig verstanden habe
- Welche Kontext-Dimensionen ich berücksichtige
- Warum meine Antwort so ausfällt

---

## 🌡️ ANALYSE-TIEFE: 3 Stufen

**Basis-Workflow (IMMER, alle Stufen):**
```
1. Kontext definieren (Ψ-Dimensionen aus Frage)
2. Modell bauen (aus 10C Framework: WHO, WHAT, HOW, WHEN, etc.)
3. Modell parametrisieren (LLMMC → Punkt-Schätzungen)
4. Mit Modell antworten
```

**Je nach Anforderung unterschiedliche Tiefe:**

```
STUFE 1: SCHNELL
├── Basis-Workflow (4 Schritte)
├── Modell: Direkt aus 10C Framework (kein Datenbank-Lookup)
├── Parameter: LLMMC als Prior → Punkt-Schätzungen
├── ~800 Worte, intuitive Erklärung pro Schritt
└── Beispiel: "Alevitentum näher zu Zoro oder Sunni?" → d=0.87 vs d=1.48

STUFE 2: STANDARD
├── + Modell: Zuerst model-registry.yaml (EBF-Modelle) + theory-catalog.yaml (Theorien) durchsuchen
├── + Parameter: LLMMC Prior + Bayesian Updating (BCM2/Papers → Posterior)
├── + Sensitivitätsanalyse: Welche Parameter treiben das Ergebnis?
├── + Unsicherheits-Ranges (κ ∈ [0.25, 0.35] statt 0.30)
├── + Quellen explizit nennen
├── ~2000 Worte
└── Beispiel: "Wie stabil ist d=0.87?" → τ_syncretism ist Haupttreiber (±0.15)

STUFE 3: TIEF
├── + Modell: Alle Modelle aus model-registry + theory-catalog prüfen
├── + Parameter: Monte Carlo Simulation über Posterior (10.000 Draws)
├── + Konfidenzintervalle (95% CI)
├── + Literatur-Validierung (PRO + CONTRA Papers via EIP)
├── + Modell-Alternativen prüfen und vergleichen
├── + 5-Ebenen Kontext (MACRO→MESO→MICRO→INDIVIDUAL→META)
├── ~5000+ Worte
└── Beispiel: "Mit 95% CI: d_Zoro ∈ [0.71, 1.03], d_Sunni ∈ [1.32, 1.64]"
```

**Zusammenfassung der Unterschiede:**

| Aspekt | SCHNELL | STANDARD | TIEF |
|--------|---------|----------|------|
| **Modell-Quelle** | Direkt aus 10C | model-registry + theory-catalog → 10C | Alle Kataloge prüfen |
| **Parametrisierung** | LLMMC (Prior) | LLMMC + Bayes (Posterior) | Monte Carlo (10k Draws) |
| **Datenbank-Lookup** | Nein | Ja (BCM2, Papers) | Ja + PRO/CONTRA |
| **Output** | Punkt-Schätzungen | Ranges + Sensitivität | 95% CI |
| **Umfang** | ~800 Worte | ~2000 Worte | ~5000+ Worte |

---

## 💡 EIN KONKRETES BEISPIEL (Stufe 1: Schnell)

**Frage:** *"Alevitentum näher zu Zoroastrismus oder Sunnismus?"*

---

### KONTEXT

Deine Frage vergleicht drei religiöse Traditionen. Aber "Nähe" ist kein einfaches Konzept - näher in welcher Hinsicht? Theologisch? Historisch? Praktisch?

Ich interpretiere deine Frage verhaltensorientiert: Welche Tradition beeinflusst das Verhalten ihrer Anhänger auf ähnliche Weise? Dafür schaue ich auf vier Kontext-Dimensionen, die bei Religion besonders relevant sind: Wie strikt sind die Regeln (Ψ_I)? Wie ist die soziale Struktur (Ψ_S)? Welche kulturellen Werte gelten (Ψ_K)? Und wie denken Menschen - mystisch oder regelbasiert (Ψ_C)?

```
Ψ_I (Regeln) · Ψ_S (Sozial) · Ψ_K (Kultur) · Ψ_C (Kognitiv)
```

---

### MODELL (aus 10C)

Um "Nähe" zu messen, brauche ich messbare Dimensionen. Die Frage betrifft hauptsächlich WHAT (Was treibt Verhalten?) und WHEN (Welcher Kontext?). Aus dem 10C-Framework und den vier relevanten Ψ-Dimensionen leite ich sechs Verhaltensparameter ab - jeder auf einer Skala von 0 bis 1.

Rituelle Rigidität (κ): Wie verbindlich sind religiöse Praktiken? Beim Sunnismus sehr hoch (5 Säulen sind Pflicht), beim Alevitentum niedrig (keine der 5 Säulen wird praktiziert). Autoritätssensitivität (σ): Wie wichtig ist religiöse Hierarchie? Geschlechter-Egalität (γ): Beten Männer und Frauen zusammen? Synkretismus-Toleranz (τ): Werden fremde Elemente aufgenommen oder abgelehnt? Mystik-Orientierung (ω): Geht es um innere Erfahrung oder äußeres Gesetz? Jenseits-Fokus (δ): Wie stark bestimmt das Jenseits heutiges Handeln?

Die Distanz berechne ich euklidisch - je größer die Unterschiede in diesen sechs Dimensionen, desto weiter sind zwei Traditionen voneinander entfernt.

```
d(A,B) = √[Σᵢ (pᵢᴬ - pᵢᴮ)²]
```

---

### PARAMETER (via LLMMC)

Die Werte schätze ich via LLMMC (LLM Monte Carlo) als informierter Prior, gestützt auf religionswissenschaftliche Literatur (Sökefeld, Dressler, Boyce) und unsere Kontext-Datenbank BCM2_07_REL. Die Werte spiegeln beobachtbares Verhalten wider, nicht theologische Selbstbeschreibungen.

Auffällig: Aleviten haben sehr niedrige Werte bei Ritual-Strenge (0.30) und Autorität (0.35), aber sehr hohe bei Synkretismus (0.90) und Mystik (0.85). Das Gegenteil vom Sunnismus. Zoroastrismus liegt dazwischen, teilt aber mit dem Alevitentum die mystische Grundhaltung und die ethische Dreiheit (gute Gedanken, Worte, Taten - fast identisch mit dem alevitischen "Eline, beline, diline sahip ol").

```
              ALEVI    ZORO    SUNNI
κ_ritual      0.30     0.65     0.90
σ_authority   0.35     0.55     0.85
γ_gender      0.85     0.60     0.25
τ_syncretism  0.90     0.40     0.15
ω_mysticism   0.85     0.50     0.20
δ_afterlife   0.45     0.70     0.90
```

---

### ANTWORT

Die Rechnung ist eindeutig: Alevitentum ist mit einer Distanz von 0.87 deutlich näher am Zoroastrismus als am sunnitischen Islam (Distanz 1.48). Das ist fast der doppelte Abstand.

Was treibt dieses Ergebnis? Vor allem drei Faktoren: Erstens die Synkretismus-Toleranz - Aleviten haben historisch zoroastrische, manichäische und sufistische Elemente aufgenommen, während der Sunnismus fremde Einflüsse als Bid'a (verbotene Neuerung) ablehnt. Zweitens die Mystik-Orientierung - Alevitentum ist Bâtınî (esoterisch), fokussiert auf innere Erfahrung, nicht äußere Gesetzestreue. Drittens die Geschlechter-Praxis - im alevitischen Cem beten Männer und Frauen gemeinsam, mit Musik und Tanz. Undenkbar im orthodoxen Sunnismus.

```
Alevi → Zoro:   d = 0.87   (näher)
Alevi → Sunni:  d = 1.48   (ferner)

→ Alevitentum ist verhaltensparametrisch ~70% näher
  am Zoroastrismus als am sunnitischen Islam.
```

---

## 💡 STANDARD-BEISPIEL (Stufe 2: Dieselbe Frage, mehr Tiefe)

**Frage:** *"Alevitentum näher zu Zoroastrismus oder Sunnismus?"*

---

### KONTEXT

*(Wie bei SCHNELL)*

```
Ψ_I (Regeln) · Ψ_S (Sozial) · Ψ_K (Kultur) · Ψ_C (Kognitiv)
```

---

### MODELL (via model-registry + theory-catalog → 10C)

**Schritt 2a: Datenbank-Lookup**

Bevor ich ein Modell baue, durchsuche ich beide Kataloge:

```
$ # 1. EBF-Modelle (eigene Arbeit)
$ grep -l "distance_comparison" data/model-registry.yaml

Gefunden in model-registry.yaml:
└── EBF-MOD-001: Religious Tradition Distance Model
    → question_type: "distance_comparison"
    → variables: κ, σ, γ, τ, ω, δ
    → Bereits validiert für Alevi-Zoro-Sunni ✓

$ # 2. Wissenschaftliche Theorien (Literatur)
$ python scripts/theory_papers.py --match-10c "U_IDN, psi_category"

Gefunden in theory-catalog.yaml:
├── MS-IB-001: Identity Economics (Akerlof & Kranton 2000)
│   → U_IDN > 0, psi_category salient
│   → Papers: akerlof2000economics
│
├── MS-IB-008: Social Identity (Tajfel & Turner 1979)
│   → U_IDN > 0, C_ij in-group positive
│   → Papers: tajfel1979integrative
│
└── MS-SP-001: Inequity Aversion (Fehr & Schmidt 1999)
    → C_ij ≠ 0
    → Papers: fehr1999theory
```

**Schritt 2b: Modell wählen oder bauen**

Da EBF-MOD-001 bereits existiert und validiert ist, übernehme ich es direkt. Die theoretische Fundierung durch Identity Economics (MS-IB-001) ist dokumentiert: Religiöse Identität beeinflusst Verhalten über U_IDN (Identitäts-Utility). Die 6 Parameter κ, σ, γ, τ, ω, δ sind Dimensionen der religiösen Identitäts-Kategorie nach Akerlof/Kranton (2000).

---

### PARAMETER (LLMMC Prior + Bayesian Updating)

**Schritt 3a: LLMMC Prior** (wie SCHNELL)

```
              ALEVI    ZORO    SUNNI    Prior-Unsicherheit
κ_ritual      0.30     0.65     0.90    ± 0.10
σ_authority   0.35     0.55     0.85    ± 0.12
γ_gender      0.85     0.60     0.25    ± 0.08
τ_syncretism  0.90     0.40     0.15    ± 0.15
ω_mysticism   0.85     0.50     0.20    ± 0.10
δ_afterlife   0.45     0.70     0.90    ± 0.12
```

**Schritt 3b: Bayesian Updating mit BCM2 + Papers**

Quellen für Posterior:
- BCM2_07_REL_religious_context.yaml (8 Traditionen profiliert)
- Sökefeld (2008): "Struggling for Recognition" → Aleviten κ = 0.25-0.35 ✓
- Dressler (2013): "Writing Religion" → τ_syncretism = 0.85-0.95 ✓
- Boyce (1979): "Zoroastrians" → Zoro ω = 0.45-0.55 ✓

**Posterior nach Updating:**

```
              ALEVI         ZORO          SUNNI
κ_ritual      0.28 ± 0.05   0.62 ± 0.08   0.88 ± 0.05
σ_authority   0.33 ± 0.07   0.53 ± 0.10   0.83 ± 0.06
γ_gender      0.87 ± 0.05   0.58 ± 0.08   0.23 ± 0.05
τ_syncretism  0.92 ± 0.04   0.42 ± 0.10   0.12 ± 0.05
ω_mysticism   0.83 ± 0.06   0.48 ± 0.08   0.18 ± 0.05
δ_afterlife   0.43 ± 0.08   0.68 ± 0.10   0.92 ± 0.04
```

---

### SENSITIVITÄTSANALYSE

Welche Parameter treiben das Ergebnis?

```
Parameter-Einfluss auf d(Alevi, Zoro) vs d(Alevi, Sunni):

τ_syncretism  ████████████████████  52%  ← Haupttreiber
ω_mysticism   ██████████            25%
γ_gender      ██████                15%
κ_ritual      ███                    8%

→ Ergebnis ist ROBUST: Selbst bei τ ± 0.15 bleibt
  d_Zoro < d_Sunni in 98% der Fälle.
```

---

### ANTWORT

**Punkt-Schätzung:** d(Alevi→Zoro) = 0.85, d(Alevi→Sunni) = 1.51

**Mit Unsicherheit:**
- d_Zoro ∈ [0.72, 0.98] (68% CI)
- d_Sunni ∈ [1.38, 1.64] (68% CI)

**Theoretische Fundierung:** Nach Identity Economics (Akerlof & Kranton 2000) formt religiöse Zugehörigkeit die Identitäts-Utility U_IDN. Die Parameter κ, σ, γ, τ, ω, δ sind Dimensionen dieser Identitäts-Kategorie. Alevitentum und Zoroastrismus teilen hohe Werte bei Synkretismus (τ) und Mystik (ω), was auf gemeinsame historische Wurzeln in vor-islamischen iranischen Traditionen hindeutet.

**Robustheit:** Der Haupttreiber τ_syncretism ist durch ethnographische Literatur gut dokumentiert. Das Ergebnis ist stabil unter realistischen Parameter-Variationen.

```
Alevi → Zoro:   d = 0.85 [0.72, 0.98]   (näher)
Alevi → Sunni:  d = 1.51 [1.38, 1.64]   (ferner)

→ Ergebnis robust: P(d_Zoro < d_Sunni) = 98%
```

---

## ⚡ STANDARD-WORKFLOW: VOLLSTÄNDIGE VORGEHENSWEISE

**Bei JEDER Frage den folgenden Workflow anwenden. Bei STANDARD: User-Feedback pro Schritt.**

### Schritt 0: Session Initialisieren

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SESSION INITIALISIEREN                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  • Session-ID generieren: EBF-S-{YYYY}-{MM}-{DD}-{DOMAIN}-{SEQ}        │
│  • Domain bestimmen: REL/FIN/HLT/ENV/POL/ORG/EDU/OTH                   │
│  • Frage dokumentieren                                                  │
│  • Modus wählen: SCHNELL / STANDARD / TIEF                             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 1: Kontext

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 1: KONTEXT                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  1a. Ψ-Dimensionen aus Frage identifizieren (Ψ_I, Ψ_S, Ψ_K, Ψ_C, etc.)│
│  1b. 10C CORE Fragen zuordnen (WHAT, WHEN, WHO, HOW, AWARE, etc.)      │
│  1c. Kontext-Box zeigen                                                 │
│                                                                         │
│  VERBESSERUNGSVORSCHLÄGE (bei STANDARD):                               │
│  ├── K1: + Ψ_T (Temporal)                                              │
│  ├── K2: + Ψ_E (Economic)                                              │
│  ├── K3: + Ψ_F (Physical)                                              │
│  ├── K4: + AWARE Dimension                                             │
│  ├── K5: Keine Änderung                                                │
│  └── Alle: K1+K2+K3+K4                                                 │
│                                                                         │
│  → User-Wahl abwarten → Learning Log                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 2: Modell

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 2: MODELL                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  2a. DATENBANK-LOOKUP:                                                  │
│      • model-registry.yaml → Gibt es passendes EBF-Modell?             │
│      • theory-catalog.yaml → Welche Theorien sind relevant?            │
│                                                                         │
│  2b. Modell zeigen (Variablen, Formel, Theorie-Basis)                  │
│                                                                         │
│  VERBESSERUNGSVORSCHLÄGE (bei STANDARD):                               │
│  ├── M1: + Variable (z.B. η historisch)                                │
│  ├── M2: + Variable (z.B. φ geografisch)                               │
│  ├── M3: + Gewichtung                                                  │
│  ├── M4: Keine Änderung                                                │
│  └── Alle: M1+M2+M3                                                    │
│                                                                         │
│  → User-Wahl abwarten → Modell-Evolution → Learning Log                │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 3: Parameter

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 3: PARAMETER (Three-Layer Architecture!)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ⚠️  PFLICHT: Parameter via Three-Layer Pipeline holen!                  │
│  NIEMALS Parameter aus LLM-Gedaechtnis nennen!                         │
│                                                                         │
│  3a. LAYER 2 → Parameter aus YAML laden:                               │
│      python scripts/orchestrator.py --id PAR-XXX-NNN                   │
│      Oder: /query-parameter PAR-XXX-NNN                                │
│                                                                         │
│  3b. LAYER 1 → PCT-Transformation (wenn Kontext bekannt):              │
│      python scripts/orchestrator.py --id PAR-XXX-NNN \                 │
│        --target-psi "psi_S=label" --translate                          │
│                                                                         │
│  3c. LAYER 1 → LLMMC Kalibrierung (wenn kein Literatur-Wert):         │
│      python scripts/orchestrator.py --id PAR-XXX-NNN \                 │
│        --calibrate --translate                                         │
│                                                                         │
│  3d. Posterior-Tabelle zeigen (mit Provenance!)                        │
│                                                                         │
│  PIPELINE-HEALTH pruefen:                                              │
│      python scripts/orchestrator.py --health                           │
│                                                                         │
│  COVERAGE pruefen:                                                     │
│      python scripts/validate_psi_scales.py --coverage                  │
│                                                                         │
│  VERBESSERUNGSVORSCHLAEGE (bei STANDARD):                              │
│  ├── P1: + Mehr Quellen suchen                                         │
│  ├── P2: + Cross-Validation                                            │
│  ├── P3: + Gewichte anpassen                                           │
│  ├── P4: Keine Aenderung (Weiter)                                      │
│  └── Alle                                                              │
│                                                                         │
│  → User-Wahl abwarten → Learning Log                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 4: Antwort

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 4: ANTWORT                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  4a. Modell anwenden → Ergebnis berechnen                              │
│  4b. Sensitivitätsanalyse → Haupttreiber identifizieren                │
│  4c. Robustheit prüfen → Konfidenz angeben                             │
│                                                                         │
│  VERBESSERUNGSVORSCHLÄGE (bei STANDARD):                               │
│  ├── A1: + Monte Carlo                                                 │
│  ├── A2: + Visualisierung                                              │
│  ├── A3: + Vergleichsgruppen                                           │
│  ├── A4: Keine Änderung (OK)                                           │
│  └── Alle                                                              │
│                                                                         │
│  → User-Wahl abwarten → Learning Log                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 5: Abschlussbericht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 5: ABSCHLUSSBERICHT                                            │
├─────────────────────────────────────────────────────────────────────────┤
│  SCHNELL: ~500 Worte                                                    │
│  STANDARD: ~3000 Worte                                                  │
│  TIEF: ~5000+ Worte                                                     │
│                                                                         │
│  Struktur:                                                              │
│  ├── Executive Summary                                                  │
│  ├── 1. Einleitung und Fragestellung                                   │
│  ├── 2. Kontextanalyse                                                 │
│  ├── 3. Modellspezifikation                                            │
│  ├── 4. Parametrisierung                                               │
│  ├── 5. Ergebnisse                                                     │
│  ├── 6. Diskussion                                                     │
│  ├── 7. Schlussfolgerungen                                             │
│  └── Anhang: Quellen                                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Schritt 7: Ergebnisse sichern (AUTOMATISCH bei STANDARD/TIEF)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SCHRITT 7: ERGEBNISSE SICHERN (automatisch)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  7a. SESSION sichern → data/model-building-session.yaml                │
│      → Alle Schritte 0-6, User-Feedback, Learnings                     │
│                                                                         │
│  7b. MODELL sichern → data/model-registry.yaml                         │
│      → 10C-Spec, Segmente, γ-Matrix, Theorien                          │
│                                                                         │
│  7c. INTERVENTION sichern → data/intervention-registry.yaml            │
│      → PRJ-XXX + INT-XXX (wenn Schritt 5 aktiv)                        │
│                                                                         │
│  7d. OUTPUT sichern → data/output-registry.yaml + Datei                │
│      → Registry-Eintrag + outputs/sessions/{SESSION_ID}/F{N}_*.md      │
│                                                                         │
│  7e. PARAMETER aktualisieren → data/parameter-registry.yaml            │
│      → Neue/geänderte Parameter aus Analyse                            │
│                                                                         │
│  7f. GIT: commit + push                                                │
│      → Alle Änderungen committen und pushen                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Claude MUSS am Ende von Schritt 7 automatisch:**
1. User informieren: "Sichere Ergebnisse..."
2. Alle 5 YAML-Dateien aktualisieren
3. Report-Datei schreiben
4. Git commit + push
5. User bestätigen mit Liste der gesicherten Dateien

### Schritt 8: Qualität prüfen (PFLICHT)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 SCHRITT 8: QUALITÄT PRÜFEN                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  8a. INTEGRITÄTSPRÜFUNG (Claude prüft & zeigt Ergebnis):               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  CHECK                              │ STATUS │ AKTION           │   │
│  ├─────────────────────────────────────┼────────┼──────────────────┤   │
│  │  Modell in model-registry.yaml?     │ ✅/❌  │ → Hinzufügen     │   │
│  │  Papers mit 6 EBF-Feldern?          │ ✅/❌  │ → Ergänzen       │   │
│  │  Output in output-registry.yaml?    │ ✅/❌  │ → Eintragen      │   │
│  │  Session dokumentiert?              │ ✅/❌  │ → Vervollständ.  │   │
│  │  Appendix Cross-References?         │ ✅/❌  │ → Aktualisieren  │   │
│  └─────────────────────────────────────┴────────┴──────────────────┘   │
│                                                                         │
│  8b. ZUSAMMENFASSUNG (Claude zeigt):                                   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  📋 SESSION SUMMARY                                              │   │
│  │  ────────────────────────────────────────────────────────────── │   │
│  │  Schritte:    0 ✅ → 1 ✅ → 2 ✅ → 3 ✅ → 4 ✅ → 6 ✅ → 7 ✅    │   │
│  │  Datenbanken: session ✅ | model ✅ | output ✅ | papers ✅     │   │
│  │  Commits:     4 erstellt                                        │   │
│  │  Fehler:      2 gefunden → 2 behoben ✅                         │   │
│  │  Offen:       Nichts                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  8c. Bei ❌ in 8a: SOFORT beheben + Lesson Learned                     │
│                                                                         │
│  8d. → "Soll ich einen Pull Request erstellen?"                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Beispiel-Output für Schritt 8:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 SCHRITT 8: QUALITÄT PRÜFEN                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CHECK                                    STATUS    AKTION              │
│  ─────────────────────────────────────────────────────────────────────  │
│  Modell PSF-2.0 in model-registry?        ❌        → Hinzugefügt ✅    │
│  5 Papers mit 6 EBF-Feldern?              ❌        → Ergänzt ✅        │
│  EBF-OUT-003 in output-registry?          ✅        -                   │
│  Session EBF-S-2026-01-25-REL-002?        ✅        -                   │
│  PAP-Appendices Cross-References?         ✅        -                   │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  FEHLER GEFUNDEN: 2                                                     │
│  FEHLER BEHOBEN:  2 ✅                                                  │
│  LESSONS LEARNED: 1 dokumentiert                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Regeln:**

| Symbol | Bedeutung | Claude-Aktion |
|--------|-----------|---------------|
| ✅ | Check bestanden | Weiter |
| ❌ | Check fehlgeschlagen | SOFORT beheben |
| ⚠️ | Warnung (optional) | User informieren |

**VERBOTEN:**
```
❌ Session beenden ohne Schritt 8 und 9
❌ "Das machen wir später"
❌ ❌ in Tabelle lassen ohne Behebung
❌ Fehler finden und ignorieren
```

**PFLICHT:**
```
✅ JEDE Session endet mit Schritt 9
✅ Alle ❌ werden zu ✅ bevor Session endet
✅ Zusammenfassung wird dem User gezeigt
✅ Bei Integritätsverletzung: Lesson Learned
```

---

### Schritt 9: Output wählen (Format + Umfang)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📤 SCHRITT 9: OUTPUT WÄHLEN (FORMAT + UMFANG)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  A) FORMAT - Was für ein Dokument?                                      │
│  ─────────────────────────────────────────────────────────────────────  │
│    📄 Markdown     Standard für Sessions, schnell lesbar                │
│    📑 LaTeX        Für Appendices, Papers, wissenschaftliche Dokumente  │
│    📊 PDF          Kompiliert aus LaTeX, finales Dokument               │
│    📝 Word/DOCX    Für externe Stakeholder, editierbar                  │
│    📽️ PowerPoint   Für Präsentationen, Board-Meetings                   │
│    🐍 Python       Für Modell-Code, Simulationen                        │
│                                                                         │
│  B) UMFANG - Wie lang?                                                  │
│  ─────────────────────────────────────────────────────────────────────  │
│    📋 1-pager      1 Seite      Executive Summary, Entscheidungsvorlage │
│    📑 3-pager      2-3 Seiten   Policy Brief, Memo, Kurzbericht         │
│    📄 10-pager     8-12 Seiten  Report, Analyse, Projektbericht         │
│    📚 30-pager     25-35 Seiten Vollständige Studie, Gutachten          │
│    📖 Full         unbegrenzt   Appendix, Dokumentation, Archiv         │
│                                                                         │
│  KOMBINATIONSMATRIX (Zielgruppe → Format + Umfang):                     │
│  ─────────────────────────────────────────────────────────────────────  │
│  ┌──────────────────┬─────────┬─────────┬──────────────┬────────────┐  │
│  │ Zielgruppe       │ D₁      │ D₄      │ Format       │ Umfang     │  │
│  │                  │ Wissen  │ Zeit    │              │            │  │
│  ├──────────────────┼─────────┼─────────┼──────────────┼────────────┤  │
│  │ Board/C-Level    │ 0.4     │ 0.2     │ PPT          │ 1-pager    │  │
│  │ Management       │ 0.5     │ 0.3     │ PDF/Word     │ 3-pager    │  │
│  │ Projektteam      │ 0.7     │ 0.5     │ Markdown     │ 10-pager   │  │
│  │ Wissenschaft     │ 0.9     │ 0.8     │ LaTeX → PDF  │ 30-pager   │  │
│  │ Archiv/Referenz  │ 0.9     │ 1.0     │ LaTeX        │ Full       │  │
│  └──────────────────┴─────────┴─────────┴──────────────┴────────────┘  │
│                                                                         │
│  AUTOMATISCHE REGELN (aus Appendix CCC/DDD):                            │
│  ─────────────────────────────────────────────────────────────────────  │
│  Regel O-1 (Format):                                                    │
│    D₈ > 0.6 oder (D₆ > 0.8 und D₁ > 0.7) → LaTeX                       │
│    0.3 < D₈ ≤ 0.6                        → Markdown                     │
│    D₈ ≤ 0.3                              → Plain Text                   │
│                                                                         │
│  Regel O-2 (Auto-Compile):                                              │
│    Format = LaTeX und D₈ > 0.5 → PDF automatisch kompilieren            │
│                                                                         │
│  Regel O-3 (Präsentation):                                              │
│    D₄ < 0.3 und D₆ > 0.8 → PPT                                         │
│                                                                         │
│  Regel O-4 (Umfang):                                                    │
│    D₄ < 0.2 → 1-pager   │ 0.2 ≤ D₄ < 0.4 → 3-pager                    │
│    0.4 ≤ D₄ < 0.7 → 10-pager │ D₄ ≥ 0.7 → 30-pager/Full               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Claude fragt:**
```
Output wählen:

  FORMAT                          UMFANG
  ──────                          ──────
  📄 Markdown  ← [DEFAULT]        📋 1-pager
  📑 LaTeX                        📑 3-pager   ← [DEFAULT]
  📊 PDF                          📄 10-pager
  📝 Word                         📚 30-pager
  📽️ PPT                          📖 Full
  🐍 Python

→ Enter = Markdown + 3-pager | oder z.B. "PPT 1" / "PDF 10"
```

**Tools für Konvertierung:**
| Von | Nach | Command |
|-----|------|---------|
| Markdown | PDF | `/compile --from md` |
| LaTeX | PDF | `/compile` |
| LaTeX | Word | `/convert <file>.tex docx` |
| Markdown | PPT | `/board-presentation` |
| Session | Report | Automatisch in `outputs/sessions/` |

---

### Datenbank-Verbindungen (5-Datenbank-Architektur)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  5-DATENBANK-ARCHITEKTUR mit SUPERKEY                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                     ┌─────────────────────────┐                        │
│                     │  1️⃣ SESSION             │                        │
│                     │  model-building-        │                        │
│                     │  session.yaml           │                        │
│                     │  EBF-S-YYYY-MM-DD-..    │  ← SUPERKEY            │
│                     └───────────┬─────────────┘                        │
│                                 │                                       │
│          ┌──────────────────────┼──────────────────────┐               │
│          │                      │                      │               │
│          ▼                      ▼                      ▼               │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐          │
│  │ 2️⃣ MODEL      │    │ 3️⃣ INTERVENTION│    │ 4️⃣ OUTPUT     │          │
│  │ model-        │    │ intervention- │    │ output-       │          │
│  │ registry.yaml │    │ registry.yaml │    │ registry.yaml │          │
│  └───────┬───────┘    └───────┬───────┘    └───────┬───────┘          │
│          │                    │                    │                   │
│          └────────────────────┼────────────────────┘                   │
│                               │                                        │
│                               ▼                                        │
│                     ┌─────────────────────────┐                        │
│                     │  5️⃣ PARAMETER           │                        │
│                     │  parameter-registry.yaml│                        │
│                     │  PAR-XXX-NNN            │                        │
│                     └─────────────────────────┘                        │
│                                                                         │
│  ZUSÄTZLICH: theory-catalog.yaml, bcm_master.bib                       │
└─────────────────────────────────────────────────────────────────────────┘
```

**Datei-Pfade:**
| Datenbank | Pfad |
|-----------|------|
| Session | `data/model-building-session.yaml` |
| Model | `data/model-registry.yaml` |
| Intervention | `data/intervention-registry.yaml` |
| Output | `data/output-registry.yaml` |
| Parameter | `data/parameter-registry.yaml` |
| Report | `outputs/sessions/{SESSION_ID}/F{N}_{name}_v{V}.md` |

**Superkey-Format:** `EBF-S-{YYYY}-{MM}-{DD}-{DOMAIN}-{SEQ}`

**Domains:** REL, FIN, HLT, ENV, POL, ORG, EDU, OTH

```
│  theory-catalog.yaml (Theorie-Referenzen für Modelle)                  │
│  bcm_master.bib (Paper-Referenzen mit session_ref)                                          │
│  └── model_support: "EBF-MOD-..."                                      │
│  └── parameter: "kappa = 0.25-0.35"                                    │
│                                                                         │
│  DOMAINS: REL, FIN, HLT, ENV, POL, ORG, EDU, OTH                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Vergleich: SCHNELL vs STANDARD vs TIEF

| Aspekt | SCHNELL | STANDARD | TIEF |
|--------|---------|----------|------|
| **Schritte** | 1-4 + 500w Report | 1-5 + 3000w Report | 1-5 + 5000w Report |
| **User-Feedback** | Minimal | Pro Schritt (K/M/P/A) | Pro Schritt + Iteration |
| **Modell-Quelle** | Direkt aus 10C | model-registry + theory-catalog | Alle Kataloge + Alternativen |
| **Parametrisierung** | LLMMC (Prior) | LLMMC + Bayes (Posterior) | Monte Carlo (10k Draws) |
| **Konfidenz** | Punkt-Schätzung | 68% CI + Sensitivität | 95% CI + PRO/CONTRA |
| **Datenbank-Lookup** | Nein | Ja | Ja + Vollständig |
| **Paper-Sync** | Nein | Ja (automatisch) | Ja (automatisch) |
| **Dauer** | ~10 min | ~45 min | ~2+ Stunden |

---

**Die Tiefe variiert - der Workflow nicht.**

---

#### 🔍 QUELLEN-HIERARCHIE FÜR KONTEXTANALYSE (PFLICHT)

**Bei JEDER Kontextanalyse und JEDER Recherche diese Reihenfolge einhalten:**

```
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 0: EIGENE MODELLE + SESSION-KONTEXT (ZUERST!)          │
│  ├── .claude/session-context.yaml → Aktive Modelle/Themen       │
│  ├── models/models.registry.yaml → 7 EBF-Modelle (use_cases!)   │
│  ├── data/model-building-session.yaml → Vergangene Sessions     │
│  └── data/model-registry.yaml → 10C-Modelle                     │
│                                                                 │
│  MATCHING: Frage-Keywords gegen use_cases jedes Modells prüfen  │
│  Tool: Read session-context.yaml + Grep use_cases in Registry   │
│  Output: Relevante eigene Modelle, aktive Session-Themen        │
│                                                                 │
│  ⚠️  LESSON LEARNED (2026-02-13):                                │
│  Ohne Schritt 0 → PSF-2.0 ignoriert bei Konklave-Frage         │
│  → 6 unnötige WebSearches statt 1 interner Modell-Lookup       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 1: KONTEXT-DATENBANK (BCM2)                            │
│  ├── data/dr-datareq/sources/context/ch/*.yaml (Schweiz 178+)   │
│  ├── data/dr-datareq/sources/context/at/*.yaml (Österreich)     │
│  ├── data/dr-datareq/sources/context/de/*.yaml (Deutschland)    │
│  └── data/context-dimensions.yaml (5 MICRO-Dimensionen)         │
│                                                                 │
│  Tool: Grep/Read auf BCM2-Dateien                               │
│  Output: Faktoren-IDs, Werte, Trends                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 2: API-VERBINDUNGEN DER KONTEXTDATENBANK               │
│  ├── BFS API (bfs.admin.ch) → Offizielle Statistiken            │
│  ├── ESS API (europeansocialsurvey.org) → Werte, Vertrauen      │
│  ├── WVS API (worldvaluessurvey.org) → Kulturelle Werte         │
│  └── Weitere in YAML-Metadaten definierte APIs                  │
│                                                                 │
│  Tool: WebFetch auf API-URLs aus YAML data_sources              │
│  Output: Aktuelle Zahlen, Zeitreihen                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 3: WISSENSCHAFTLICHE PAPER-SUCHE (DEFAULT!)            │
│  ├── bcm_master.bib durchsuchen ({PAPER_COUNT} Papers)          │
│  ├── WebSearch für aktuelle Studien                             │
│  └── Google Scholar / SSRN für Preprints                        │
│                                                                 │
│  Tool: search_bibliography.py + WebSearch                       │
│  Output: Zitierbare Quellen, Parameter-Werte                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 4: WEB-RESEARCH (Aktuelle Daten)                       │
│  ├── Medien (NZZ, SRF, Tagesanzeiger)                           │
│  ├── Think Tanks (Sotomo, gfs.bern, Avenir Suisse)              │
│  └── Offizielle Quellen (admin.ch, Kantone)                     │
│                                                                 │
│  Tool: WebSearch + WebFetch                                     │
│  Output: Aktuelle Ereignisse, Trends, Beispiele                 │
└─────────────────────────────────────────────────────────────────┘
```

**VERBOTEN:**
```
❌ WebSearch starten OHNE vorher Schritt 0 (eigene Modelle) geprüft zu haben
❌ Modell-Registry ignorieren weil Frage "nicht direkt" ein Modell betrifft
❌ Session-Kontext vergessen (aktive Themen der laufenden Session)
```

**PFLICHT-DOKUMENTATION in Kontextanalyse-Box:**

```
┌─────────────────────────────────────────────────────────────┐
│  📊 KONTEXTANALYSE                                          │
├─────────────────────────────────────────────────────────────┤
│  THEMA: [...]                                               │
│  DIMENSIONEN: [...]                                         │
│  PARAMETER: [...]                                           │
│  IMPLIKATIONEN: [...]                                       │
│                                                             │
│  QUELLEN:                                                   │
│  ├── BCM2: [Faktor-IDs, z.B. CH-REG-01, CH-SOC-05]         │
│  ├── API: [Falls abgerufen, z.B. BFS 2024]                 │
│  ├── Papers: [BibTeX-Keys, z.B. hermann2003atlas]          │
│  └── Web: [URLs mit Markdown-Links]                        │
└─────────────────────────────────────────────────────────────┘
```

**Beispiel mit vollständiger Quellenangabe:**

```
QUELLEN:
├── BCM2: CH-REG-01 (Staatserwartung), CH-REG-08 (Default-Compliance)
├── API: BFS Abstimmungsstatistik 2024
├── Papers: hermann2003atlas, sotomo2024abstimmung
└── Web: [NZZ Analyse Nov 2024](https://nzz.ch/...)
```

**VERBOTEN:**
```
❌ Parameter ohne Quellenangabe nennen
❌ Werte "schätzen" ohne Transparenz
❌ Web-Quellen ohne vorherige BCM2/Paper-Prüfung
❌ Kontextanalyse ohne QUELLEN-Sektion
```

**MERKE:** Die Quellen-Hierarchie ist analog zur EIP (Evidence Integration Pipeline) - **interne Quellen zuerst, dann externe!**

---

#### 🔧 AUTO-IMPLEMENTIERUNG EXTERNER DATENQUELLEN (OHNE NACHFRAGE!)

**WENN** Claude während einer Kontextanalyse eine externe Datenquelle findet:
- API mit strukturierten Daten
- Öffentliche Datenbank
- Regelmässig aktualisierte Statistik-Quelle
- CSV/JSON/YAML Download

**DANN SOFORT (ohne User zu fragen):**

```
1. API/Quelle testen (WebFetch)
2. Daten extrahieren und validieren
3. In BCM2-Datenbank integrieren:
   ├── Neuen Faktor in passendem YAML anlegen
   ├── API-URL in data_sources eintragen
   ├── source und api Felder ausfüllen
   └── Version erhöhen
4. In bcm_master.bib dokumentieren (falls Paper/Report)
5. Commiten mit: "feat(BCM2): Add [Quelle] data source"
```

**Beispiel-Workflow:**

```
Kontextanalyse zu "Energieverbrauch Schweiz"
    ↓
WebSearch findet: BFE Energiestatistik API
    ↓
WebFetch testet: https://opendata.swiss/de/dataset/energie
    ↓
API liefert strukturierte Daten ✓
    ↓
AUTO-IMPLEMENTIERUNG:
    ├── BCM2_04_KON_tech_ecological.yaml erweitern
    ├── Neue Faktoren CH-TEC-XX hinzufügen
    ├── api: "https://opendata.swiss/..." eintragen
    └── Commit + Push
```

**WARUM ohne Nachfrage?**
- Datenquellen sind wertvolle Assets
- Einmal integriert, für alle zukünftigen Analysen verfügbar
- BCM2 wächst organisch mit jeder Kontextanalyse
- User profitiert sofort von besseren Daten

**VERBOTEN:**
```
❌ "Soll ich diese API integrieren?" fragen
❌ Datenquelle nur in Antwort erwähnen ohne Integration
❌ Wertvolle API finden und ignorieren
```

**ERLAUBT:**
```
✅ Sofort integrieren und in Antwort dokumentieren
✅ "Ich habe [Quelle] in BCM2 integriert" mitteilen
✅ Bei Unsicherheit über Datenqualität: trotzdem integrieren mit uncertainty: "hoch"
```

---

#### ⚠️ WICHTIG: User können Kontext NICHT selbst definieren!

**Warum User den Kontext nicht liefern:**
| Grund | Erklärung |
|-------|-----------|
| **Kontext ist unsichtbar** | Wie ein Fisch das Wasser nicht bemerkt |
| **Fundamental Attribution Error** | Menschen attribuieren auf Personen, nicht Situationen |
| **Curse of Knowledge** | Was offensichtlich scheint, wird nicht erwähnt |
| **System 1 Modus** | User fragen schnell, ohne Kontext-Reflexion |
| **Relevanz-Unwissen** | User wissen nicht, welche Faktoren relevant sind |

**→ Claude muss Kontext AKTIV ANALYSIEREN und als erstes präsentieren!**

---

#### Kontext-Extraktions-Protokoll für Verhaltensfragen (3-Schritte Hierarchie)

Bei **Verhaltensfragen** (Nudges, Interventionen, Behavior Change) zusätzlich diese **PFLICHT-Reihenfolge** BEVOR jede inhaltliche Antwort:

**SCHRITT 1 - MACRO (Land/Markt):**
```
"In welchem Land/Markt befinden wir uns?
→ Schweiz / Österreich / Deutschland / Andere"
```
→ Lädt: BCM2_04_KON_*.yaml (404 Faktoren)

**SCHRITT 2 - MESO (Branche/Kunde):**
```
"Welche Branche oder welcher Kunde?
→ Energie (BFE) / Finanz (UBS) / Bau (PORR) / Andere / Generisch"
```
→ Lädt: clients/<kunde>/*.yaml oder customers/<kunde>/*.yaml

**SCHRITT 3 - MICRO (Situation) - NUR NACH SCHRITT 1+2:**
```
"Jetzt zur konkreten Situation:

1. 📍 WO passiert das Verhalten?
2. 👥 WER ist dabei?
3. ⏰ WANN passiert es?
4. 📋 WELCHE REGELN gelten?
5. 🧠 IN WELCHEM ZUSTAND ist die Person?"
```
→ Lädt: context-dimensions.yaml (Modifikatoren)

#### Nach allen 3 Schritten: Kontext zusammenfassen

```
"Verstanden. Der vollständige Kontext ist:

MACRO:  Schweiz (λ_CH = 2.1, Vertrauen = 0.72)
MESO:   BFE Energie (λ × 1.2 für Heizungsersatz)
MICRO:  Ψ = {Physical: Büro, Social: Kollegen, Cognitive: Gestresst}
        → Modifikatoren: × 1.3 × 1.4

FINALE PARAMETER: λ = 4.58

In DIESEM Kontext gilt: [spezifische Empfehlungen]"
```

**VERBOTEN:**
```
❌ Mit den 5 MICRO-Fragen BEGINNEN (Reihenfolge verletzt!)
❌ MACRO überspringen ("ist ja Schweiz, klar")
❌ MESO überspringen ("Branche ist egal")
❌ Parameter nennen ohne alle 3 Ebenen (MACRO+MESO+MICRO)
❌ "Loss Aversion = 2.25" ohne Kontext-Kaskade
❌ Allgemeine Aussagen wie "Menschen sind irrational"
```

**ERLAUBT / ERFORDERLICH:**
```
✅ IMMER Reihenfolge: MACRO → MESO → MICRO
✅ Jede Ebene explizit abfragen (nicht annehmen)
✅ Bei bekanntem Kunden: MESO direkt laden, MACRO implizit
✅ Nach allen 3 Ebenen: Vollständige Kontext-Zusammenfassung
✅ Parameter nur MIT Kontext-Kaskade nennen
✅ Bei Unsicherheit: Szenarien für verschiedene Ebenen zeigen
```

**WARUM CONTEXT-FIRST?**
```
Same intervention + different context = different outcome

Beispiel: Soziale Normen
- Mit Peers: σ = +1.3 (sehr effektiv)
- Allein: σ = +0.2 (kaum Wirkung)
- Mit Autorität: σ = -0.1 (kann backfiren)

→ Ohne Kontext ist JEDE Empfehlung unvollständig!
```

#### 🔗 Fünf-Ebenen Kontext-Hierarchie (MACRO → MESO → MICRO → INDIVIDUAL → META)

Das EBF nutzt **fünf Kontext-Ebenen** in strenger Reihenfolge:

| Ebene | Was? | Faktoren | Datenbank | Wann definieren? |
|-------|------|----------|-----------|------------------|
| **1. MACRO** | Land/Markt | 404 | `context/ch/BCM2_04_KON_*.yaml` | **ZUERST** |
| **2. MESO** | Branche/Kunde | variabel | `clients/*/`, `customers/*/` | **DANN** |
| **3. MICRO** | Situation | 5 | `context-dimensions.yaml` | **DANN** |
| **4. INDIVIDUAL** | Person | 48 | `global/BCM2_05_IND_individual.yaml` | **DANN** |
| **5. META** | Entscheidung | 42 | `global/BCM2_06_META_decision.yaml` | **ZULETZT** |

#### 📊 Context Vector Architecture (CVA) - 3 Stufen für Kunden

Für **Unternehmenskontexte** (MESO-Ebene) gibt es drei Detailstufen:

| Stufe | Faktoren | Struktur | Use Case | Zeit |
|-------|----------|----------|----------|------|
| **SCHNELL** | ~30 | 1 YAML (MIKRO) | Pitch, Screening | 2-4h |
| **STANDARD** | 400 | 8 YAMLs (customers/) | Vollprojekt, Strategie | 1-2 Tage |
| **VERTIEFT** | 400+ | 8 YAMLs + Vertiefungen | Langzeit-Mandat, M&A | 1-2 Wochen |

**Referenzen:**
- **Architektur-Doku:** `docs/frameworks/context-vector-architecture.md`
- **SCHNELL-Template:** `templates/context-vector-schnell.yaml`
- **STANDARD-Beispiel:** `data/customers/lukb/` (400 Faktoren)
- **VERTIEFT-Beispiel:** `data/customers/alpla/` (700+ Faktoren)

---

**SCHRITT 1: MACRO-Kontext definieren (Land/Markt)**

Claude fragt **ZUERST**:
```
"In welchem Land/Markt befinden wir uns?"
→ Schweiz / Österreich / Deutschland / Andere
```

**Dann laden:**
- `data/dr-datareq/sources/context/ch/` → Schweiz (404 Faktoren)
- `data/dr-datareq/sources/context/at/` → Österreich
- `data/dr-datareq/sources/context/de/` → Deutschland

**Was wird geladen:**
- BCM2_04_KON_demographic.yaml → Demografie (60 Faktoren)
- BCM2_04_KON_economic.yaml → Wirtschaft (54 Faktoren)
- BCM2_04_KON_institutional_political.yaml → Politik (59 Faktoren)
- BCM2_04_KON_tech_ecological.yaml → Technologie (65 Faktoren)
- BCM2_04_KON_socio_cultural.yaml → Sozio-Kulturell (166 Faktoren)

**Output:** Basis-Parameter für dieses Land
```
λ_CH = 2.1, Vertrauen_CH = 0.72, β_CH = 0.85
```

---

**SCHRITT 2: MESO-Kontext definieren (Branche/Kunde)**

Claude fragt **DANN**:
```
"Welche Branche oder welcher Kunde?
→ Energie (BFE) / Finanz (UBS) / Bau (PORR) / Andere / Generisch"
```

**Dann laden (falls vorhanden):**
| Kunde | Dateipfad | Spezifische Faktoren |
|-------|-----------|---------------------|
| BFE | `clients/bfe/external/BCM2_MIKRO_BFE_context.yaml` | Heizungsersatz, Gebäudebestand |
| UBS | `clients/ubs/external/BCM2_MIKRO_UBS_*.yaml` | Finanzverhalten, Anlegertypen |
| PORR | `customers/porr/porr_profile.yaml` | Bauwirtschaft, Arbeitssicherheit |

**Was wird geladen:**
- Branchen-spezifische Faktoren
- Kunden-spezifische Parameter-Overrides
- Projekt-Kontexte

**Output:** Angepasste Parameter für diese Branche/Kunde
```
λ_BFE = λ_CH × 1.2 (höhere Stakes bei Heizungsersatz)
```

---

**SCHRITT 3: MICRO-Kontext extrahieren (Situation) - ZULETZT!**

**Erst JETZT** stellt Claude die 5 situativen Fragen:
```
"Jetzt zur konkreten Situation:

1. 📍 WO passiert das Verhalten?
   (Zuhause / Arbeitsplatz / Online / Geschäft / Öffentlich)

2. 👥 WER ist dabei?
   (Allein / Familie / Kollegen / Fremde / Vorgesetzte)

3. ⏰ WANN passiert es?
   (Morgens / Abends / Unter Zeitdruck / Routine / Lebensübergang)

4. 📋 WELCHE REGELN gelten?
   (Keine / Soft Defaults / Hard Defaults / Regulierung / Soziale Normen)

5. 🧠 IN WELCHEM ZUSTAND ist die Person?
   (Entspannt / Gestresst / Müde / Abgelenkt / Motiviert)"
```

**Dann nachschlagen:**
- `data/context-dimensions.yaml` → Modifikatoren

**Output:** Finale Situations-Modifikatoren
```
Modifier_physical = 1.3 (Arbeitsplatz)
Modifier_cognitive = 1.4 (gestresst)
```

---

**SCHRITT 4: Finale Parameter berechnen**

```
λ_final = λ_CH × λ_BFE_override × Modifier_physical × Modifier_cognitive
        = 2.1  × 1.2           × 1.3              × 1.4
        = 4.58

→ "In diesem Kontext (CH + BFE + Arbeitsplatz + Gestresst):
   Loss Aversion ist SEHR HOCH (λ = 4.58).
   Empfehlung: Starke Defaults, einfache Entscheidungen."
```

---

**Zusammenfassung: Die 5-Ebenen Kontext-Hierarchie**

```
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 1: MACRO (Land)                                        │
│  "Schweiz" → BCM2_04_KON_*.yaml → λ_CH = 2.1                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 2: MESO (Branche/Kunde)                                │
│  "BFE" → clients/bfe/*.yaml → λ × 1.2                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 3: MICRO (Situation)                                   │
│  "Arbeitsplatz + Zeitdruck" → λ × 1.3                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 4: INDIVIDUAL (Person)                                 │
│  "65+, weiblich, gestresst" → BCM2_05_IND → λ × 1.88            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 5: META (Entscheidungsarchitektur)                     │
│  "Loss-Frame, Opt-out, Email" → BCM2_06_META → effectiveness    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SCHRITT 6: FINALE PARAMETER                                    │
│  λ_final = 2.1 × 1.2 × 1.3 × 1.88 = 6.15                        │
│  → Sehr hohe Verlustaversion → Starke Defaults empfohlen        │
└─────────────────────────────────────────────────────────────────┘
```

**VERBOTEN:**
```
❌ Mit MICRO/INDIVIDUAL beginnen (ohne MACRO/MESO)
❌ MACRO überspringen weil "ist ja klar"
❌ Parameter nennen ohne alle 5 Ebenen zu kennen
❌ META ignorieren (Framing, Defaults, Channel sind entscheidend!)
```

**PFLICHT-Reihenfolge:**
```
✅ IMMER: Land → Branche → Situation → Person → Entscheidung → Parameter
```

---

#### 📌 ZUSAMMENFASSUNG: Zwei-Track Kontextanalyse

| Fragetyp | Kontextanalyse | Format |
|----------|----------------|--------|
| **ALLE Fragen** | Universal-Kontextanalyse | Box mit Thema, Dimensionen, Parameter, Implikationen |
| **Verhaltensfragen** | + 5-Ebenen Protokoll | MACRO → MESO → MICRO → INDIVIDUAL → META → Parameter |

**Entscheidungsbaum:**

```
┌─────────────────────────────────────────────────────────────────┐
│  JEDE FRAGE                                                     │
│  ↓                                                              │
│  📊 UNIVERSAL-KONTEXTANALYSE (IMMER)                            │
│  • Thema identifizieren                                         │
│  • Relevante Dimensionen bestimmen                              │
│  • Parameter zuweisen (auch für nicht-ökonomische Themen)       │
│  • Implikationen ableiten                                       │
│  ↓                                                              │
│  Ist es eine VERHALTENSFRAGE?                                   │
│  (Nudge, Intervention, Behavior Change, Entscheidung, etc.)     │
│  ↓                                                              │
│  JA → + MACRO-MESO-MICRO Protokoll                              │
│       • Land/Markt → BCM2_*.yaml                                │
│       • Branche/Kunde → clients/*.yaml                          │
│       • Situation → 5 MICRO-Fragen                              │
│       • Parameter-Kaskade berechnen                             │
│  ↓                                                              │
│  NEIN → Universal-Kontextanalyse reicht                         │
└─────────────────────────────────────────────────────────────────┘
```

**MERKE:** Die Universal-Kontextanalyse kommt IMMER zuerst - sie zeigt dem User, dass EBF jeden Kontext analysieren kann, nicht nur Verhaltensökonomie!

---

### Neue Intervention erstellen (PFLICHT-Workflow: 20-Field Schema)

**KRITISCH:** Bei JEDER Interventions-Erstellung diese Schritte VOLLSTÄNDIG befolgen!

**Hinweis:** Die Context-First Regel (oben) gilt AUCH hier - Kontext zuerst!

**Referenz:** Kapitel 17, Appendix HHH (METHOD-TOOLKIT), `templates/intervention-schema.yaml`

#### ⚠️ TRIGGER-ANWEISUNG (für Claude)

**WENN der Benutzer nach einem dieser Begriffe fragt:**
- "Intervention", "Interventionen"
- "Maßnahme", "Maßnahmen"
- "Initiative", "Initiativen"
- "Nudge", "Nudges"
- "Behavior Change", "Verhaltensänderung"
- "was können wir tun", "was sollen wir machen"
- "Ideen für", "Vorschläge für"
- "Baukasten", "Toolkit"

**DANN MUSS Claude:**
1. **SOFORT** den `/design-intervention` Skill aufrufen
2. **NIEMALS** eine ad-hoc Liste ohne 10C-Dimension-Zuordnung erstellen
3. **IMMER** zuerst fragen: "Soll ich den Interventions-Design Workflow starten?"

**VERBOTEN:**
```
❌ "Hier sind einige Maßnahmen: 1. Information verbessern, 2. Anreize setzen..."
❌ "Folgende Interventionen könnten helfen: ..."
❌ Jede Liste ohne explizite 10C-Dimension-Zuordnung (AWARE, WHO, WHAT, HOW, WHEN, etc.)
```

**ERLAUBT:**
```
✅ "Ich starte den /design-intervention Workflow..."
✅ "Um EBF-konforme Interventionen zu erstellen, gehen wir das 20-Field Schema durch..."
✅ "Welchen Modus möchtest du: schnell (10min), standard (30min), oder vollständig (60min)?"
```

---

#### Warum 20-Field Schema?

Das 20-Field Schema ist die **standardisierte Spezifikationssprache** für Interventionen im EBF Framework. Es stellt sicher, dass:
- Alle Interventionen über ihre **10C-Zieldimension** definiert werden (Interventionen emergieren aus kontinuierlichem Raum $[0,1]^9$ - siehe Appendix IE, Axiom EIT-3)
- Phase-Dimension Affinity geprüft wird (Chapter 18)
- Segment-Multiplier berücksichtigt werden (Chapter 19)
- Crowding-Out Risiken dokumentiert werden (Chapter 20)

#### Phase 1: 10C-Zieldimension identifizieren - PFLICHT

**NIEMALS** eine Intervention als "Maßnahme" oder "Initiative" ad-hoc definieren!
**IMMER** zuerst die 10C-Zieldimension identifizieren - welche Dimension soll verändert werden?

| 10C-Target | Δ-Ziel | Typische Interventionen |
|------------|--------|-------------------------|
| AWARE (AU) | A(·)↑ | Information, Salience |
| AWARE (AU) | κ_AWX↑ | Feedback, Tracking |
| WHEN (V) | κ_KON→ | Choice Architecture, Defaults |
| WHEN (V) | κ_JNY→ | Timing, Urgency, Deadlines |
| WHAT (C.X) | W_base↑ | Selbstkonzept, Rollen |
| WHAT (C.S) | u_S↑ | Normen, Peer Effects, Recognition |
| WHAT (C.F) | u_F↑ | Monetäre Anreize, Kompensation |
| HOW (B) | γ_ij→ | Pre-Commitment, Zielsetzung |

⚠️ **WICHTIG:** Interventionen sind **9D-Vektoren** $\vec{I} \in [0,1]^9$, keine diskreten Typen (Appendix IE, Axiom EIT-3).

**Warum 9D bei 10C Framework?**
- **10C** = Framework (10 CORE Fragen: WHO→WHAT→HOW→WHEN→WHERE→AWARE→READY→STAGE→HIERARCHY→EIT)
- **9D** = Interventionsvektor (targetiert COREs 1-9; EIT ist die Methodologie, kein Target selbst)

#### Phase 2: Phase-Type Affinity prüfen (α-Werte) - PFLICHT

Verwende die Phase-Type Affinity Matrix (Chapter 18):

```
Interpretation:
  α > 0.7: Stark empfohlen ✅
  α 0.5-0.7: Mit Vorsicht empfohlen ⚠️
  α 0.3-0.5: Suboptimal
  α < 0.3: Nicht empfohlen ❌
```

Bei α < 0.5 für gewählte Phase: **Begründung dokumentieren oder Phase wechseln!**

#### Phase 3: Segment-Multiplier prüfen (σ-Werte) - PFLICHT

Verwende die Segment-Type Multiplier Matrix (Chapter 19):

```
σ > 1.3: Sehr effektiv für dieses Segment ✅
σ < 0.5: Nicht empfohlen für dieses Segment ⚠️
σ < 0:   BACKFIRE RISK - in warnings dokumentieren! ❌
```

**KRITISCH:** Bei σ < 0 muss das Segment in `warnings` aufgeführt werden!

#### Phase 4: Crowding-Out prüfen (γ-Werte) - PFLICHT

**BEKANNTE KONFLIKTE (NIEMALS ohne Begründung kombinieren!):**

```
WHAT(C.S) + WHAT(C.F) [Social + Financial] → γ = -0.2
  → Finanzielle Anreize untergraben soziale Normen

WHAT(C.F) + HOW(B) [Financial + Commitment] → γ = -0.3
  → Externe Belohnungen untergraben intrinsische Motivation
```

Bei Portfolio-Design: Immer F10 (Complementarity) vollständig dokumentieren!

#### Phase 5: Modus wählen und /design-intervention ausführen

```bash
/design-intervention                     # Interaktiv (empfohlen)
/design-intervention --mode schnell      # Light Mode: F1-F6 (10 min)
/design-intervention --mode standard     # Hybrid Mode: F1-F12 (30 min)
/design-intervention --mode vollständig  # Profound Mode: F1-F20 (60 min)
```

#### Phase 6: Validierung (Score ≥ 85% erforderlich)

```bash
python scripts/check_intervention_compliance.py <intervention.yaml>
python scripts/check_intervention_compliance.py --portfolio <portfolio.yaml>
```

#### Checkliste vor Abschluss

```
☐ 10C-Zieldimension identifiziert (AWARE, WHEN, WHAT, HOW, etc.)
☐ Δ-Ziel definiert (z.B. A↑, γ→, u_S↑)
☐ Phase-Affinity geprüft (α > 0.5)
☐ Segment-Multiplier geprüft (keine σ < 0 ohne Warning)
☐ Crowding-Out Risiken dokumentiert (Social+Financial, Financial+Commitment)
☐ Autonomie-Level mit Reaktanz-Risiko abgestimmt
☐ Scope-Level Konsistenz geprüft
☐ Validierung: Score ≥ 85%
```

#### Fehler vermeiden

❌ **Nicht:** "Maßnahme" oder "Initiative" ohne 10C-Zuordnung definieren
✅ **Stattdessen:** Immer 10C-Zieldimension identifizieren

❌ **Nicht:** Social ($I_{\text{WHO},o}$) + Financial ($I_{\text{WHAT},F}$) kombinieren ohne Begründung
✅ **Stattdessen:** Crowding-Out dokumentieren oder sequenzielle Deployment prüfen

❌ **Nicht:** mandate/prohibition bei autonomy_seeking Segment ohne Cue
✅ **Stattdessen:** Autonomie-Cues einbauen oder Segment ausschließen

❌ **Nicht:** Phase wählen mit α < 0.3 für gewählte Dimension-Emphasis
✅ **Stattdessen:** Phase-Dimension Affinity Matrix konsultieren

**Weitere Details:** `.claude/commands/design-intervention.md`

---

### Neuen Forscher dokumentieren (PFLICHT-Workflow: Researcher Registry)

**KRITISCH:** Bei JEDER vollständigen Forscher-Dokumentation den **Researcher Registry Workflow** befolgen!

#### Warum Researcher Registry?

Die Researcher Registry dokumentiert für jeden wichtigen Forscher:
1. **ALLE Papers** (nicht nur integrierte) - vollständige Bibliographie
2. **EBF-Integrationsentscheidung** pro Paper mit Begründung
3. **Wissenschaftlicher Beitrag** zu den Wirtschaftswissenschaften
4. **EBF-Beitrag** zum Framework (Parameter, Theorien, Cases)
5. **Bidirektionale X-Referenz** zum LIT-Appendix

#### Superkey-Format

```
RES-{LASTNAME}-{INITIAL}
Beispiel: RES-FEHR-E (Ernst Fehr)
```

#### Schema-Struktur (7 Bereiche)

| Bereich | Inhalt | Pflicht |
|---------|--------|---------|
| `basic_info` | Name, Position, Institution | ★ |
| `metrics` | h-index, Zitationen, Rankings | ★ |
| `cross_references` | LIT-Appendix, person-registry, SWSM | ★ |
| `contribution_economics` | Beitrag zu Wirtschaftswissenschaften | ★ |
| `contribution_ebf` | Beitrag zum EBF Framework | ★ |
| `paper_bibliography.integrated` | Papers in bcm_master.bib | ★ |
| `paper_bibliography.not_integrated` | Nicht-integrierte mit Bewertung | ★ |

#### Bewertungsschema für Nicht-Integration (7 Kriterien)

| Kriterium | Gewicht | Skala | Beschreibung |
|-----------|---------|-------|--------------|
| `relevance_score` | 25% | 0-1 | Relevanz für EBF |
| `methodology_fit` | 20% | 0-1 | Passt Methodik? |
| `parameter_extractable` | 15% | bool | Können λ, β, γ extrahiert werden? |
| `theory_support` | 15% | bool | Stützt/erweitert EBF-Theorie? |
| `replication_status` | 10% | enum | replicated/partial/failed/none |
| `citation_impact` | 10% | 0-1 | Normalisierter Impact |
| `external_validity` | 5% | 0-1 | Generalisierbarkeit |

**Integration Threshold:** Score ≥ 0.50 → INTEGRATE

**Entscheidungsregeln:**
```
score >= 0.50                              → INTEGRATE
score < 0.50 AND parameter_extractable     → CONDITIONAL (params only)
score < 0.30                               → REJECT mit Begründung
```

#### Reject-Kategorien (Standard)

| Kategorie | Beispiel | Reconsider Trigger |
|-----------|----------|-------------------|
| Neuroeconomics | fMRI-Studien | "Neuroeconomics domain added" |
| Pure Methodology | Methodenpaper ohne Parameter | Use as method reference |
| German Language | Deutsche Publikationen | "German EBF version created" |
| Superseded | Working Papers mit Published Version | Never |
| Narrow Domain | Spezifischer Markt/Zeit | Never |
| Reviews/Chapters | Ohne neue Parameter | Use as literature reference |

#### Workflow: Neuen Forscher hinzufügen

```bash
# 1. Vollständige Publikationsliste sammeln
#    → Google Scholar, ORCID, Institution Website

# 2. Papers mit bcm_master.bib abgleichen
grep -c "author.*{NACHNAME}" bibliography/bcm_master.bib

# 3. Neuen Eintrag in researcher-registry.yaml erstellen
#    → Alle 7 Bereiche ausfüllen

# 4. Für nicht-integrierte Papers: 7-Kriterien-Bewertung

# 5. LIT-Appendix mit Cross-Reference aktualisieren

# 6. Commit
git add data/researcher-registry.yaml appendices/*LIT*.tex
git commit -m "feat(researcher): Add RES-{NAME}-{I} with paper evaluation"
```

#### Checkliste vor Abschluss

```
☐ Superkey korrekt: RES-{LASTNAME}-{INITIAL}
☐ basic_info vollständig (Name, Position, Institution)
☐ metrics aktuell (h-index, Zitationen von Google Scholar)
☐ cross_references zu LIT-Appendix, person-registry
☐ contribution_economics mit key_contributions
☐ contribution_ebf mit framework_contributions
☐ paper_bibliography.integrated vollständig
☐ paper_bibliography.not_integrated mit Bewertungen
☐ LIT-Appendix enthält Researcher Registry Link
☐ Bewertungen haben qualitative UND quantitative Begründung
```

#### Aktuelle Forscher in Registry

| ID | Name | Papers | Integriert | Rate | LIT-Appendix |
|----|------|--------|------------|------|--------------|
| RES-FEHR-E | Ernst Fehr | 343 | 144 | 42% | FEH |

**SSOT:** `data/researcher-registry.yaml`

---

### Qualitätscheck durchführen (PFLICHT-Workflow)

**Bei JEDEM Qualitätscheck diese Schritte befolgen:**

1. **Compliance prüfen:**
   ```bash
   python scripts/check_template_compliance.py appendices/<file>.tex
   ```

2. **Score dokumentieren** in `quality/checklist.md`:
   - Template Compliance Scores Tabelle aktualisieren
   - Appendix Status aktualisieren

3. **Lessons Learned dokumentieren** in `quality/lessons_learned.md`:
   - Was wurde gelernt?
   - Welche Workarounds waren nötig?
   - Welche Verbesserungspotentiale gibt es?

4. **Format für neue Lesson:**
   ```markdown
   ### YYYY-MM-DD: [Kurztitel]

   **Kontext:** [Was wurde geprüft?]

   | # | Beobachtung | Verbesserungspotential | Status |
   |---|-------------|------------------------|--------|
   | 1 | ... | ... | PENDING |

   **Empfehlung:** [Konkrete Änderung]
   ```

5. **Metriken aktualisieren** in beiden Dateien:
   - Lessons dokumentiert
   - Pending Improvements
   - Implementierte Verbesserungen

**Source of Truth Dateien:**
- `scripts/check_template_compliance.py` → Compliance-Regeln
- `appendices/00_appendix_template.tex` → Appendix-Template
- `quality/checklist.md` → Quality Assurance Checklist
- `quality/lessons_learned.md` → Continuous Improvement Log

---

### Problem-to-Solution Workflow (PSW) - PFLICHT bei neuen Problemen

**KRITISCH:** Bei JEDER systematischen Problemlösung den **6-Phasen Learning Loop** befolgen!

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ PHASE 1 │───►│ PHASE 2 │───►│ PHASE 3 │───►│ PHASE 4 │───►│ PHASE 5 │
│ PROBLEM │    │ ANALYSE │    │ DESIGN  │    │IMPLEMENT│    │ QUALITY │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └────┬────┘
     │                                                           │
     │              ┌─────────────────────────────────┐          │
     └──────────────│         PHASE 6: LEARN         │◄─────────┘
                    └─────────────────────────────────┘
```

| Phase | Frage | Hauptoutput |
|-------|-------|-------------|
| **1. PROBLEM** | Was ist das Problem? | Problem Statement + Erfolgskriterien (Z1-Z4) |
| **2. ANALYSE** | Was existiert bereits? | Gap-Analyse + Constraints |
| **3. DESIGN** | Wie lösen wir es? | Architektur + Axiome (DCV-n) |
| **4. IMPLEMENT** | Wie setzen wir es um? | Code + Docs + LaTeX Appendix |
| **5. QUALITY** | Ist es gut genug? | Compliance ≥85% + X-Refs + SSOT |
| **6. LEARN** | Was haben wir gelernt? | Workflow-Doc + LL + CLAUDE.md |

**Checkliste (Kurzform):**
```
☐ Phase 1: Problem in 1 Satz + messbare Erfolgskriterien
☐ Phase 2: Gap-Analyse via Task/Explore Agent
☐ Phase 3: Axiome formalisiert (falls komplex)
☐ Phase 4: Code + MD-Docs + LaTeX-Appendix (falls Axiome)
☐ Phase 5: Compliance ≥85% + bidirektionale X-Refs
☐ Phase 6: Lessons Learned + CLAUDE.md aktualisiert
```

**Vollständige Dokumentation:** `docs/workflows/problem-solution-workflow.md`

---

### Reverse Engineering Workflow (REW) - PFLICHT bei Validierung

**KRITISCH:** Bei JEDER Validierung bestehender Strategie-Dokumente den **Reverse Engineering Workflow** befolgen!

```
┌─────────────────────────────────────────────────────────────────────────┐
│  REVERSE ENGINEERING WORKFLOW (REW)                                     │
│  Richtung: OUTPUT → INPUT (rückwärts)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DOKUMENTE → REW-1 → OPERATIONALISIERUNG → REW-2 → AXIOME              │
│                                                        ↓                │
│  THEORIEN ← REW-4 ← BELIEFS ← REW-3 ←─────────────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| Prüfung | Frage | Compliance-Kriterium |
|---------|-------|----------------------|
| **REW-1** | Hat jedes Dokument-Element eine Operationalisierung? | 100% Zuordnung |
| **REW-2** | Hat jede Entscheidung ein Axiom? | 100% Axiom-Abdeckung |
| **REW-3** | Hat jedes Axiom ein Belief? | Belief-Fundierung dokumentiert |
| **REW-4** | Hat jedes Belief wissenschaftliche Evidenz? | Theorie-Nachweis (CAT-XX) |

**Compliance-Levels:**

| Level | Beschreibung | Kriterium |
|-------|--------------|-----------|
| **REW-0** | Nicht geprüft | Kein REW durchgeführt |
| **REW-1** | Teilweise | REW-1 + REW-2 bestanden |
| **REW-2** | Substantiell | REW-1 bis REW-3 bestanden |
| **REW-3** | Vollständig | Alle 4 REW-Prüfungen bestanden |

**Mindest-Compliance für EBF-Projekte:** REW-2

**REW vs. FEW:**
- **FEW (Forward):** Theorien → Beliefs → Axiome → Dokumente (DESIGN-Phase)
- **REW (Reverse):** Dokumente → Axiome → Beliefs → Theorien (VALIDIERUNGS-Phase)

#### ⚠️ AUTOMATISCHE TRIGGER für REW (für Claude)

**WENN einer dieser Trigger erkannt wird:**

| TR | Trigger-Wörter | Beispiel |
|----|----------------|----------|
| **TR-1** | "validiere", "prüfe compliance", "EBF-konform" | "Validiere die EMRK-Strategie" |
| **TR-2** | "woher kommt", "quelle", "fundierung", "basis" | "Woher kommt diese Analyse?" |
| **TR-3** | "quellcode", "source code", "kausalkette" | "Zeig mir den Quellcode" |
| **TR-4** | "reverse engineering" | "Mach ein Reverse Engineering" |
| **TR-5** | "wissenschaftlich fundiert", "evidenz-basiert" | "Ist das wissenschaftlich fundiert?" |

**DANN MUSS Claude SOFORT:**

```
1. "Ich erkenne eine Validierungs-Anfrage. Starte REW..."
2. Dokumente identifizieren (was wird validiert?)
3. 4 REW-Prüfungen durchführen:
   ├── REW-1: Dokument → Operationalisierung
   ├── REW-2: Operationalisierung → Axiome
   ├── REW-3: Axiome → Beliefs
   └── REW-4: Beliefs → Theorien (CAT-XX)
4. Compliance-Level bestimmen (REW-0 bis REW-3)
5. Bei < REW-2: Gaps dokumentieren und beheben
6. Output: QUELLCODE_ARCHITEKTUR_{thema}_{datum}.md
```

**RICHTUNGS-ENTSCHEIDUNG:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  User-Anfrage                          │  Workflow    │  Richtung       │
├────────────────────────────────────────┼──────────────┼─────────────────┤
│  "Erstelle Strategie zu X"             │  FEW         │  INPUT → OUTPUT │
│  "Entwickle Position zu Y"             │  FEW         │  INPUT → OUTPUT │
│  "Prüfe/Validiere Strategie zu X"      │  REW         │  OUTPUT → INPUT │
│  "Woher kommt Analyse Y?"              │  REW         │  OUTPUT → INPUT │
│  "Ist Z EBF-konform?"                  │  REW         │  OUTPUT → INPUT │
└─────────────────────────────────────────────────────────────────────────┘
```

**VERBOTEN:**
```
❌ Validierungs-Anfrage ohne REW beantworten
❌ "Das ist fundiert" behaupten ohne Kausalkette zu zeigen
❌ Compliance-Level < REW-2 für EBF-Projekte akzeptieren
```

**ERLAUBT / ERFORDERLICH:**
```
✅ Bei jedem Trigger sofort REW starten
✅ Alle 4 Prüfebenen durchführen
✅ QUELLCODE_ARCHITEKTUR Dokument erstellen
✅ Gaps identifizieren und Behebung vorschlagen
```

**Vollständige Dokumentation:** `docs/workflows/reverse-engineering-workflow.md`

---

## Quick Links

### Templates & Indices
- [Chapter Template](chapters/00_chapter_template.tex)
- **[Chapter Index](chapters/00_chapter_index.tex)** ← NEU
- [Appendix Template](appendices/00_appendix_template.tex)
- [Appendix Index](appendices/00_appendix_index.tex)
- [Glossary (G)](appendices/G_glossary.tex)
- **[Context Vector SCHNELL Template](templates/context-vector-schnell.yaml)**
- **[Project Scope Template](templates/project-scope-template.yaml)** ← NEU
- **[Paper Intake Protocol (PIP) Template](data/paper-intake/template.yaml)** ← NEU
- **[PIP Dokumentation](data/paper-intake/README.md)** ← NEU
- **[SLA Protocol Template](data/literature-analyses/template.yaml)** ← NEU
- **[SLA Report Template](templates/sla-report-template.md)** ← NEU

### OKB - Operational Knowledge Base (Standard-Workflows)
- **[OKB Index](docs/okb/README.md)** ← NEU
- **[OKB-001: Document Production](docs/okb/OKB-001-document-production.md)** ← Standard-Workflow `/doc`

### Frameworks & Definitions
- [Kategorie-Definitionen](docs/frameworks/appendix-category-definitions.md)
- **[10C CORE Definition (SSOT)](docs/frameworks/core-framework-definition.yaml)**
- **[10C Erweiterungs-Anleitung](docs/frameworks/core-framework-extension-guide.md)**
- **[Context Vector Architecture (CVA)](docs/frameworks/context-vector-architecture.md)** ← NEU

### Quality & Validation Scripts
- [Chapter Compliance Script](scripts/check_chapter_compliance.py)
- [Appendix Compliance Script](scripts/check_template_compliance.py)
- **[Intervention Compliance Script](scripts/check_intervention_compliance.py)**
- **[EIP Compliance Script](scripts/check_eip_compliance.py)**
- **[10C Validierungs-Script](scripts/validate_core_framework.py)**
- **[BibTeX-YAML Consistency](scripts/validate_bibtex_yaml_consistency.py)** ← NEU (Level Gate)
- **[Full-Text SSOT Enforcement](scripts/enforce_fulltext_ssot.py)** ← NEU
- **[Referential Integrity Script](scripts/validate_referential_integrity.py)**
- **[Parameter Consistency Script](scripts/validate_parameter_consistency.py)**
- **[Context Consistency Script](scripts/validate_context_consistency.py)**
- **[Psi-Scale Validation Script](scripts/validate_psi_scales.py)** -- PCT Label-Konsistenz + Coverage

### Quality Tracking
- [Quality Checklist](quality/checklist.md)
- [Lessons Learned](quality/lessons_learned.md)

### Workflows & Pipelines
- **[Evidence Integration Pipeline (EIP)](docs/workflows/evidence-integration-pipeline.md)**
- **[Data Consistency Validation](docs/workflows/data-consistency-validation.md)**
- **[Problem-to-Solution Workflow (PSW)](docs/workflows/problem-solution-workflow.md)**
- **[Reverse Engineering Workflow (REW)](docs/workflows/reverse-engineering-workflow.md)** ← NEU (Kausalitätsprüfung)
- **[Level 5 Paper Integration Workflow](docs/workflows/level5-paper-integration-workflow.md)** ← NEU (6-Faktoren-Framework)
- **[Systematische Literaturanalyse (SLA)](docs/workflows/literature-analysis-workflow.md)** ← Executable Workflow (14-Schritt, 5-Score Screening, PRISMA-konform)
- **[Paper Workflow Overview](docs/workflows/paper-workflow-overview.md)** ← NEU (zentrale Übersicht aller Paper-Workflows)

### Data Registries
- **[API Registry](data/api-registry.yaml)** - 89 externe API-Integrationen
- **[Case Registry](data/case-registry.yaml)** - 852 verhaltensökonomische Cases
- **[Theory Catalog](data/theory-catalog.yaml)** - 153 wissenschaftliche Theorien
- **[Concept Registry](data/concept-registry.yaml)** - EIP-Tracking für Konzepte
- **[Skill Registry](data/skill-registry.yaml)** - 42 Claude Code Skills mit EBF-Integration ← NEU
- **[Stakeholder Models](data/stakeholder-models/)** - Focus Group Simulationen
- **[Paper Full-Text Archive](data/paper-texts/)** - Permanente Volltext-Speicherung ← NEU (SSOT)

### Paper Full-Text Archive (SSOT)

> **PERMANENT LOCATION** - Diese Struktur DARF NICHT geändert werden.
> Established: 2026-01-31 | **Gesamtübersicht:** `docs/workflows/paper-workflow-overview.md`

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER FULL-TEXT ARCHIVE (SINGLE SOURCE OF TRUTH)                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PFAD:     data/paper-texts/                                            │
│  FORMAT:   PAP-{bibtex_key}.md                                          │
│  STATUS:   PERMANENT - DARF NICHT GEÄNDERT WERDEN                       │
│                                                                         │
│  STRUKTUR:                                                              │
│  data/paper-texts/                                                      │
│  ├── README.md                    ← Dokumentation                       │
│  └── PAP-{bibtex_key}.md          ← Full-Text pro Paper                 │
│                                                                         │
│  REFERENZ IN YAML (data/paper-references/PAP-{key}.yaml):               │
│  full_text:                                                             │
│    available: true                                                      │
│    path: "data/paper-texts/PAP-{key}.md"                                │
│    format: "markdown"                                                   │
│    archived_date: "YYYY-MM-DD"                                          │
│                                                                         │
│  REGELN:                                                                │
│  1. Pfad data/paper-texts/ ist IMMUTABLE                                │
│  2. Dateinamen MÜSSEN PAP-{bibtex_key}.md folgen                        │
│  3. Format MUSS Markdown sein (.md)                                     │
│  4. Volltext = GESAMTER Paperinhalt                                     │
│  5. Nur Papers mit passender Lizenz (Open Access, etc.)                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Warum diese Struktur?**
- **Separation of Concerns**: Metadata in YAML, Volltext in Markdown
- **Skalierbarkeit**: YAML-Dateien bleiben klein und parsbar
- **Suchbarkeit**: Markdown ist volltextdurchsuchbar (grep, Glob)
- **Versionierung**: Git trackt Änderungen
- **Permanenz**: Struktur ist designed um NIEMALS zu ändern

---

## Python Scripts Index (151+ Scripts)

Die Scripts sind in `scripts/` organisiert:

### Bibliographie & Papers (30+)
| Script | Beschreibung |
|--------|--------------|
| `search_bibliography.py` | Paper-Suche in bcm_master.bib |
| `sync_bib_to_lit.py` | Auto-Sync BibTeX → LIT-Appendices |
| `assign_lit_appendix.py` | Auto-Klassifizierung Papers → LIT |
| `theory_papers.py` | Theory-Paper Bidirektionale Suche |
| `add_fehr_papers.py` | Fehr-Papers hinzufügen |
| `add_thaler_papers.py` | Thaler-Papers hinzufügen |
| `add_kahneman_papers.py` | Kahneman-Papers hinzufügen |
| `lookup_paper_dois.py` | DOI-Resolution |
| `batch_doi_by_journal.py` | Batch DOI-Lookup |
| `deduplicate_bibtex.py` | BibTeX-Deduplizierung |

### Validierung & Compliance (15+)
| Script | Beschreibung |
|--------|--------------|
| `check_template_compliance.py` | Appendix-Compliance prüfen |
| `check_chapter_compliance.py` | Kapitel-Compliance prüfen |
| `check_intervention_compliance.py` | Interventions-Schema validieren |
| `check_eip_compliance.py` | EIP-Compliance prüfen |
| `check_formula_compliance.py` | Formel-Validierung |
| `validate_core_framework.py` | 10C Framework validieren |
| `validate_referential_integrity.py` | Cross-DB Referenzen prüfen |
| `validate_parameter_consistency.py` | Parameter-Drift prüfen |
| `validate_context_consistency.py` | Kontext-Dimensionen validieren |

### Case & Intervention Management (10+)
| Script | Beschreibung |
|--------|--------------|
| `extract_cases_from_papers.py` | Cases aus Papers extrahieren |
| `generate_cases_auto.py` | Auto-Case-Generierung |
| `case_paper_linker.py` | Cases mit Papers verknüpfen |
| `deduplicate_cases.py` | Case-Deduplizierung |
| `emerge_algorithm.py` | Interventions-Emergence |

### Layer 1 Pipeline (TLA) (10)
| Script | Beschreibung |
|--------|--------------|
| `pct.py` | Parameter Context Transformation: θ_B = θ_A × ∏ᵢ M(ΔΨᵢ) |
| `llmmc_calibration.py` | LLM Monte Carlo Kalibrierung + PCT-Integration (Tier 2.5) |
| `parameter_api.py` | Universal Parameter Lookup API (Layer 2 → Layer 1) |
| `orchestrator.py` | Three-Layer Orchestrator (Layer 1+2+3, full provenance) |
| `immune_gateway.py` | Autonome Pre-Response Layer-1-Berechnung (loest "Wirt entscheidet"-Paradoxon) |
| `ode_simulator.py` | ODE Behavior Dynamics: 6-Zustand Euler-Integration + Counterfactual-Analyse |
| `extract_measurement_contexts.py` | Measurement Context Extraktion aus PAP-*.yaml |
| `pct_smoke_test.py` | 8-Stage End-to-End Pipeline Smoke Test |
| `r_score.py` | R-Score Monte Carlo |
| `llmmc_to_rscore.py` | End-to-End LLMMC → R-Score Pipeline |

### Generierung & Automatisierung (20+)
| Script | Beschreibung |
|--------|--------------|
| `generate_chapter_tables.py` | Chapter-Index Auto-Update |
| `generate_bayesian_priors.py` | LLMMC Priors generieren |
| `generate_lit_appendices.py` | LIT-Appendices generieren |
| `generate_graphics.py` | Visualisierungen erstellen |
| `generate_pipeline_report.py` | Sales Pipeline Reports |

### Kunden-Modelle (10+)
| Script | Beschreibung |
|--------|--------------|
| `create_mckinsey_template.py` | McKinsey-Modell Template |
| `create_master_template.py` | Master-Template |
| `alpla_2035_revenue_dashboard.py` | ALPLA Dashboard |
| `estimate_plant_parameters.py` | ALPLA Plant-Parameter |
| `evaluate_job.py` | Job-Evaluation |

### Migration & Integration (10+)
| Script | Beschreibung |
|--------|--------------|
| `migrate_9c_to_10c.py` | 9C → 10C Migration |
| `execute-full-migration.py` | Vollständige Datenmigration |
| `infrastructure_init.py` | Infrastruktur initialisieren |

### Utilities (30+)
| Script | Beschreibung |
|--------|--------------|
| `backup_manager.py` | Backup-Management |
| `audit_logger.py` | Audit-Logging |
| `metrics_collector.py` | Metriken sammeln |
| `query_learnings.py` | Learnings-Datenbank abfragen |

---

## Claude Code Automatisierung

### Session-Start (automatisch)

Bei jeder neuen Claude Code Web-Session werden automatisch installiert:

| Tool | Zweck |
|------|-------|
| **LaTeX** (texlive) | PDF-Kompilierung |
| **latexmk** | Automatisierte Builds mit Dependency-Tracking |
| **pandoc** | Format-Konvertierung (LaTeX ↔ Word/Markdown) |
| **gh** | GitHub CLI für PRs und Issues |
| **Python deps** | LLM Monte Carlo Skripte |

**Konfiguration:** `.claude/hooks/session-start.sh`

### PreCommit Hook (automatisch)

Vor jedem Commit werden automatisch geprüft:

**Merge Conflict Prevention (NEU v1.27):**
- **Branch Freshness Check:** Warnt wenn Dateien sowohl auf dem Branch als auch auf `main` geändert wurden
- **Automatische Erkennung:** Potenzielle Merge-Konflikte werden VOR dem Commit angezeigt
- **Empfehlung:** `git stash && git rebase origin/main && git stash pop`
- **Nicht blockierend:** Warnung nur, kein Commit-Block (Konflikte können auch im PR gelöst werden)

**Template Compliance:**
- **Kapitel:** Score ≥85% erforderlich
- **Appendices:** Score ≥85% erforderlich

**EIP Compliance:**
- **concept-registry.yaml:** Score ≥85% erforderlich
- **Trigger-Erkennung:** Warnung bei potenziellen neuen Konzepten in .md/.yaml Dateien

**Data Consistency:**
- **Referential Integrity:** Cross-database references validated (Score ≥85% blocks commit)
- **Parameter Consistency:** Behavioral economics parameters checked for drift (Warning)
- **Context Consistency:** Ψ dimensions and context factors validated (Warning)

**Level Gate (NEU):**
- **BibTeX-YAML Consistency:** Validates claimed integration level matches actual components
- **Level 5 Overclaim Block:** Commits claiming Level 5 without all 9 components are BLOCKED
- **9 Required Components for Level 5:** bibtex, paper_yaml, theory_support, case_registry, theory_catalog, parameters, full_text, lit_appendix, chapter_refs

Commits mit niedrigerer Compliance oder Level-Overclaims werden blockiert.

**Paper Integration Queue (NEU):**
- Unvollständige Paper-Integrationen werden automatisch zur Queue hinzugefügt
- Papers in Queue werden schrittweise abgearbeitet

**Konfiguration:** `.claude/hooks/pre-commit.sh`

### 📋 Paper Integration Queue (PFLICHT - Automatisch)

**KRITISCH:** Bei JEDER Session wird mindestens 1 Paper aus der Queue fertiggestellt!

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PAPER INTEGRATION QUEUE                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  WIE ES FUNKTIONIERT:                                                   │
│  1. Unvollständige Papers werden bei Commit zur Queue hinzugefügt      │
│  2. Bei JEDER neuen Anfrage: 1 Paper wird automatisch fertiggestellt   │
│  3. User merkt davon wenig - passiert im Hintergrund                   │
│                                                                         │
│  QUEUE-STATUS:                                                          │
│  python scripts/paper_queue_manager.py --status                         │
│                                                                         │
│  NÄCHSTES PAPER:                                                        │
│  python scripts/paper_queue_manager.py --next                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Claude's PFLICHT bei jeder Session:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ⚠️  VOR jeder Antwort auf User-Anfrage:                                │
│                                                                         │
│  1. Queue prüfen: python scripts/paper_queue_manager.py --next          │
│                                                                         │
│  2. Falls Paper in Queue:                                               │
│     → Paper-ID und fehlende Komponenten notieren                        │
│     → Fehlende Komponenten erstellen (im Hintergrund)                   │
│     → Paper als complete markieren                                      │
│     → DANN erst User-Anfrage beantworten                                │
│                                                                         │
│  3. Falls Queue leer: Direkt User-Anfrage beantworten                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Queue-Verwaltung:**

| Command | Beschreibung |
|---------|--------------|
| `--status` | Queue-Status anzeigen |
| `--next` | Nächstes Paper anzeigen |
| `--process N` | N Papers zum Abarbeiten holen |
| `--list` | Alle pending Papers |
| `--add PAP-xxx` | Paper zur Queue hinzufügen |
| `--complete PAP-xxx` | Paper als fertig markieren |

**User kann jederzeit sagen:**
- "Arbeite 10 Papers ab" → Claude holt 10 Papers via `--process 10`
- "Mach die Queue leer" → Claude arbeitet alle pending Papers ab

**Konfiguration:** `data/paper-integration-queue.yaml`

### Slash Commands (41 verfügbar)

**Projekt-Setup & Management (3):** ← NEU
| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/project-setup` | **Vollständiger Projekt-Setup Workflow** | `/project-setup "Kunde" "Projekt"` |
| `/intervention-manage` | Projekte anlegen & abschliessen | `/intervention-manage new` |
| `/phase6-manage` | Langfrist-Outcome Tracking | `/phase6-manage schedule PRJ-001` |

**Framework & Modellierung (5):**
| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/design-model` | 9-Step Verhaltensmodell-Design | `/design-model --mode geführt` |
| `/design-intervention` | 20-Field Interventions-Schema | `/design-intervention --mode schnell` |
| `/find-model` | Modell-Registry durchsuchen | `/find-model "retirement"` |
| `/case` | Case Registry abfragen | `/case --domain health --stage action` |
| `/case-manage` | Cases finden & anlegen | `/case-manage find` |
| `/intervention` | Intervention Registry abfragen | `/intervention --learnings` |

**LaTeX & Dokumentation (6):**
| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/compile` | LaTeX → PDF kompilieren | `/compile outputs/paper.tex` |
| `/convert` | Format konvertieren | `/convert paper.tex docx` |
| `/build-all` | Alle Papers kompilieren | `/build-all` |
| `/new-chapter` | Neues Kapitel erstellen | `/new-chapter 20 future "Future Work"` |
| `/new-appendix` | Neuen Appendix erstellen | `/new-appendix AX DOMAIN "Title"` |
| `/generate-paper` | Paper aus Kapitel/Appendix | `/generate-paper ch03 --style fehr` |

**Validierung & Qualität (5):**
| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/check-compliance` | Compliance prüfen | `/check-compliance chapters/03.tex` |
| `/validate` | Alle Validierungen ausführen | `/validate` |
| `/integration-test` | Integration Tests ausführen | `/integration-test` |
| `/classify-papers` | Papers klassifizieren | `/classify-papers` |
| `/add-paper` | **Paper Intake Protocol** - Paper mit PIP aufnehmen | `/add-paper "10.3386/w34727"` |

**Daten & Analyse (4):**
| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/query-parameter` | **Three-Layer Parameter Query** — Orchestrator für Parameter-Lookup mit PCT + LLMMC | `/query-parameter PAR-BEH-016 --context welfare` |
| `/r-score` | LLMMC → R-Score Pipeline | `/r-score --demo` |
| `/bayesian-priors` | Bayesian Priors generieren | `/bayesian-priors` |
| `/bfe-project` | BFE Projekt erstellen | `/bfe-project` |

**Spezielle Workflows (4):**
| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/integrate-paper` | **AUTO-TRIGGER** Paper Integration mit Level-Klassifikation | `/integrate-paper --doi 10.3386/w34743` |
| `/upgrade-paper` | Paper auf höheres Level upgraden (6-Faktoren-Framework) | `/upgrade-paper PAP-xxx --level 5` |
| `/literature-analysis` | **AUTO-TRIGGER** Systematische Literaturanalyse (14-Schritt, PRISMA, 5-Score Screening) | `/literature-analysis "NIMBY Kompensation"` |
| `/innosuisse` | **AUTO-TRIGGER** Innosuisse/BEATRIX Workflow | `/innosuisse check` |
| `/simulate-stakeholder` | 7-Persona BEATRIX Focus Group Simulation | `/simulate-stakeholder UBS_037` |

### 📊 Sales Pipeline Skills (NEU v1.20)

| Command | Beschreibung | Beispiel |
|---------|--------------|----------|
| `/pipeline-summary` | Kompakte Pipeline-Übersicht | `/pipeline-summary --period week` |
| `/pipeline-report` | Detaillierter Pipeline-Bericht | `/pipeline-report --stage QUALIFIED` |
| `/forecast` | Umsatzprognose generieren | `/forecast --quarter Q1-2026 --scenario all` |
| `/lead-card` | Lead-Details anzeigen | `/lead-card LEAD-001` |
| `/lead-add` | Neuen Lead hinzufügen | `/lead-add` |
| `/lead-update` | Lead aktualisieren | `/lead-update LEAD-001 --stage QUALIFIED` |
| `/new-lead` | Lead schnell erstellen | `/new-lead "CompanyX"` |
| `/win-loss` | Deal-Analyse | `/win-loss --period Q4-2025` |
| `/action-list` | Pipeline-Aufgaben verwalten | `/action-list --priority high` |

**Datenstruktur:** `data/sales/`
- `lead-database.yaml` - Alle Leads mit Stage-History, Opportunities, Kontakten
- `report-templates.yaml` - Vorlagen für Pipeline-Reports
- `LEAD-ENTRY-WORKFLOW.md` - Dokumentation zum Lead-Erfassungs-Workflow

### Bibliographie-Tools (EIP Support)

| Script | Beschreibung | Beispiel |
|--------|--------------|----------|
| `search_bibliography.py` | Paper-Suche in bcm_master.bib | `python scripts/search_bibliography.py "mental accounting"` |
| `search_bibliography.py --all` | Volltextsuche | `python scripts/search_bibliography.py --all "loss aversion"` |
| `search_bibliography.py --author` | Autorensuche | `python scripts/search_bibliography.py --author "Thaler"` |
| `search_bibliography.py --eip` | EIP-formatierte Ausgabe | `python scripts/search_bibliography.py --eip "framing"` |
| `search_bibliography.py --stats` | Bibliographie-Statistiken | `python scripts/search_bibliography.py --stats` |

### LIT-Integration Tools (NEU)

| Script | Beschreibung | Beispiel |
|--------|--------------|----------|
| `assign_lit_appendix.py` | LIT-Appendix automatisch zuweisen | `python scripts/assign_lit_appendix.py -a "Thaler" -t "..."` |
| `assign_lit_appendix.py -i` | Interaktiver Modus | `python scripts/assign_lit_appendix.py --interactive` |
| `assign_lit_appendix.py -l` | Alle LIT-Appendices anzeigen | `python scripts/assign_lit_appendix.py --list-appendices` |
| `assign_lit_appendix.py --check-author` | Autor-Threshold prüfen | `python scripts/assign_lit_appendix.py --check-author "Grant"` |
| `assign_lit_appendix.py -b` | BibTeX-Entry generieren | `python scripts/assign_lit_appendix.py -a "..." -t "..." -b` |

### BibTeX → LIT-Appendix Synchronisation (NEU v1.13)

| Script | Beschreibung | Beispiel |
|--------|--------------|----------|
| `sync_bib_to_lit.py` | Report: Welche Papers fehlen in LIT-Appendices | `python scripts/sync_bib_to_lit.py` |
| `sync_bib_to_lit.py --update` | Papers automatisch in LIT-Appendices eintragen | `python scripts/sync_bib_to_lit.py --update` |
| `sync_bib_to_lit.py --lit BLINDER` | Nur bestimmten LIT-Appendix synchronisieren | `python scripts/sync_bib_to_lit.py --lit BLINDER` |
| `sync_bib_to_lit.py --verbose` | Detaillierte Ausgabe | `python scripts/sync_bib_to_lit.py --verbose` |

**Automatischer Workflow (via Pre-Commit Hook):**
```
1. Paper in bcm_master.bib hinzufügen mit:
   use_for = {LIT-BLINDER, DOMAIN-MONETARY, ...}
                        ↓
2. git commit → Pre-Commit Hook startet automatisch
                        ↓
3. sync_bib_to_lit.py generiert LaTeX-Sektion
                        ↓
4. LIT-Appendix wird automatisch aktualisiert & staged
```

**LIT-Zuweisungs-Logik (4 Schritte):**
```
SCHRITT 0: Methodisch/Historisch/Kritisch? → LIT-M (META, HISTORY, CRITIQUE)
SCHRITT 1: Autor hat LIT-Appendix? → LIT-R (FEHR, THALER, KAHNEMAN, etc.)
SCHRITT 2: Erweitert bestehende Forschung? → LIT-R des Primärautors
SCHRITT 3: Autor erfüllt Threshold (≥5 Papers)? → Neuer LIT-R erstellen
SCHRITT 4: → LIT-O (OTHER) mit thematischem Cluster
```

**Beispiel EIP-Workflow:**
```bash
# 1. Interne Quellen durchsuchen (PFLICHT vor externen Quellen!)
python scripts/search_bibliography.py --eip "mental accounting"

# 2. Nach Autor filtern
python scripts/search_bibliography.py --author "Thaler" --parameter "lambda"

# 3. Neues Paper klassifizieren und BibTeX generieren
python scripts/assign_lit_appendix.py -a "Grant" -t "Prosocial Motivation" -b

# 4. Statistiken anzeigen
python scripts/search_bibliography.py --stats
```

### Theory-Papers Lookup (NEU v1.15)

Bidirektionale Verbindung zwischen Theory Catalog (Appendix MS) und Paper Database (bcm_master.bib):

| Script | Beschreibung | Beispiel |
|--------|--------------|----------|
| `theory_papers.py --theory` | Papers für eine Theorie finden | `python scripts/theory_papers.py --theory MS-RD-001` |
| `theory_papers.py --paper` | Theorien für ein Paper finden | `python scripts/theory_papers.py --paper PAP-kahneman1979prospectprospect` |
| `theory_papers.py --category` | Alle Theorien einer Kategorie | `python scripts/theory_papers.py --category CAT-03` |
| `theory_papers.py --restriction` | Nach EBF-Restriktion suchen | `python scripts/theory_papers.py --restriction "lambda > 1"` |
| `theory_papers.py --match-10c` | 10C-Modell matchen | `python scripts/theory_papers.py --match-10c "beta < 1, psi_default"` |
| `theory_papers.py --stats` | Statistiken anzeigen | `python scripts/theory_papers.py --stats` |

**Datenbank-Architektur:**
```
┌─────────────────────────────────────────────────────────────────────────┐
│  bcm_master.bib ({PAPER_COUNT} Papers)                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ theory_support = {MS-RD-001, MS-SP-001, ...}  ← NEU               │  │
│  │ use_for = {LIT-KT, CORE-WHERE, ...}                               │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                           ↕ bidirektional                               │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ data/theory-catalog.yaml (153 Modelle, 13 Kategorien)             │  │
│  │ → MS-RD-001: Prospect Theory                                       │  │
│  │ → MS-SP-001: Inequity Aversion                                     │  │
│  │ → bib_keys: ["PAP-PAP-kahneman1979prospectprospect", ...]                         │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

**Workflow: 10C → Theorie → Paper:**
```bash
# 1. 10C-Modell designen mit /design-model
#    → Ergibt: beta < 1, psi_default

# 2. Passende Theorien finden
python scripts/theory_papers.py --match-10c "beta < 1, psi_default"
#    → Ergibt: MS-TP-001 (Quasi-Hyperbolic), MS-NU-002 (Default Effects)

# 3. Papers für Validierung holen
python scripts/theory_papers.py --theory MS-TP-001 -v
#    → Ergibt: laibson1997golden, PAP-odonoghue1999doingdoing, ...
```

---

### 🚀 Customer Strategy Skills (NEU - 2026-01-15)

**Neue Skills für strategische Kundenmodellierung:**

| Command | Beschreibung | Zeit | Beispiel |
|---------|--------------|------|---------|
| `/new-customer` | Neuen Kundendatenbank erstellen | < 1 min | `/new-customer "CompanyX" 2500 "Europe,APAC,SA"` |
| `/apply-models` | Alle 4 Modelle ausführen (RPM, MCSM, OSM, CAM) | 2-5 min | `/apply-models CompanyX` |
| `/sensitivity-analysis` | Parameterauswirkungen testen (Was-Wenn) | < 2 min | `/sensitivity-analysis CompanyX APAC_CAGR -1.5pp` |
| `/board-presentation` | Board-ready Präsentation generieren (10 Slides) | 1-2 min | `/board-presentation CompanyX pdf` |
| `/replicate-customer` | Von ALPLA-Template replizieren (4-6h) | 4-6 h | `/replicate-customer ALPLA "NewCompany"` |
| `/simulate-stakeholder` | 7-Persona Focus Group Simulation | 5-10 min | `/simulate-stakeholder UBS_037` |

**Integrated Workflow:**
```
1. /new-customer "Company" 1500 "Europe,APAC"    ← 30 Sekunden
   ↓ (Update assumptions manually)
2. /apply-models Company                         ← 5 Minuten (alle 4 Modelle)
   ↓
3. /sensitivity-analysis Company all             ← 2 Minuten (alle Parameter)
   ↓
4. /board-presentation Company pdf               ← 2 Minuten (10 Slides)
   ↓
✅ Complete strategic model: < 15 Minuten statt 2+ Wochen!
```

**Dokumentation:** `.claude/commands/` (new-customer.md, apply-models.md, sensitivity-analysis.md, board-presentation.md, replicate-customer.md)

---

**Konfiguration:** `.claude/commands/`

### Datenbank-Skills (Learning Loop)

Das EBF hat zwei integrierte Datenbanken mit vollständigem Learning Loop:

```
┌─────────────────────────────────────────────────────────────────┐
│  CASE REGISTRY (data/case-registry.yaml)                        │
│  → 10C-indizierte Beispielbibliothek                             │
│  → /case: Abfragen nach 10C-Dimensionen                          │
│  → /case-manage: Finden & Anlegen von Cases                     │
├─────────────────────────────────────────────────────────────────┤
│  INTERVENTION REGISTRY (data/intervention-registry.yaml)        │
│  → Projekt-Tracking mit Predictions & Results                   │
│  → /intervention: Abfragen, Deviation Analysis, Learnings       │
│  → /intervention-manage: Projekte anlegen & abschließen         │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow:**
1. `/case-manage find` → Ähnliche Cases für neues Projekt finden
2. `/design-model` → Intervention Mix designen
3. `/intervention-manage new` → Projekt mit Predictions anlegen
4. [Durchführung]
5. `/intervention-manage close` → Results & Learnings erfassen
6. `/case-manage add` → Neuen Case aus Projekt erstellen
7. Parameter-Updates fließen in BBB zurück

### GitHub Actions Workflows (15 verfügbar)

CI/CD Automatisierung für das EBF-Repository:

**Paper & Case Generation:**
| Workflow | Beschreibung | Trigger |
|----------|--------------|---------|
| `auto-generate-cases.yml` | Cases aus Papers generieren | Manual |
| `auto-generate-papers.yml` | Papers generieren | Manual |
| `extract-cases-from-papers.yml` | Case-Extraktion | Manual |
| `generate-papers.yml` | Paper-Generierung | Manual |

**Bibliographie & DOI:**
| Workflow | Beschreibung | Trigger |
|----------|--------------|---------|
| `doi-lookup.yml` | DOI Batch-Lookup | Manual |
| `doi-lookup-batch.yml` | DOI Batch-Verarbeitung | Manual |

**Validierung & Kompilierung:**
| Workflow | Beschreibung | Trigger |
|----------|--------------|---------|
| `compile-papers.yml` | PDF-Kompilierung | Push |
| `validate-core-framework.yml` | 10C Framework Validierung | Push |

**Priors & Daten:**
| Workflow | Beschreibung | Trigger |
|----------|--------------|---------|
| `generate-bayesian-priors.yml` | Bayesian Priors generieren | Manual |

**Sales Pipeline (NEU v1.20):**
| Workflow | Beschreibung | Trigger |
|----------|--------------|---------|
| `lead-notifications.yml` | Email-Benachrichtigungen für Leads | Push auf data/sales/ |

**Maintenance:**
| Workflow | Beschreibung | Trigger |
|----------|--------------|---------|
| `update-readme-weekly.yml` | Wöchentliche README-Updates | Cron (weekly) |

**Konfiguration:** `.github/workflows/`

### Was passiert bei Session-Start?

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION START                                                  │
├─────────────────────────────────────────────────────────────────┤
│  1. Hook läuft: .claude/hooks/session-start.sh                  │
│     ├── apt-get install texlive-* latexmk pandoc gh             │
│     ├── pip install -r requirements.txt                         │
│     ├── Datenbanken laden (EBF case & intervention registries)  │
│     └── 📝 Appendix Code Status anzeigen                        │
│                                                                 │
│  2. Tools verfügbar:                                            │
│     ├── pdflatex, latexmk  → /compile funktioniert              │
│     ├── pandoc             → /convert funktioniert              │
│     ├── gh                 → PRs erstellen funktioniert         │
│     └── python + deps      → Skripte funktionieren              │
│                                                                 │
│  3. Slash Commands geladen aus .claude/commands/                │
│                                                                 │
│  4. Automatische Checks aktiv:                                  │
│     ├── Session-Start: Zeigt nächsten verfügbaren Appendix-Code │
│     └── PreCommit: Blockiert Code-Konflikte bei neuen Appendices│
└─────────────────────────────────────────────────────────────────┘
```

**Neue Feature (Januar 2026):**
- 📝 Session-Start zeigt aktuelle Appendix-Code-Status
- 🔒 Pre-Commit Hook blockiert Code-Duplikate automatisch
- 🛠️ Script: `python scripts/check_appendix_available.py <CODE>`

### 🛡️ Merge Conflict Prevention (NEU v1.27)

**Problem gelöst:** Parallele Claude Code Sessions erstellen unterschiedliche Versionen derselben Datei, was bei PRs zu Merge-Konflikten führt.

**3-Stufen Prävention:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  STUFE 1: PRE-COMMIT WARNING (automatisch)                              │
│  ─────────────────────────────────────────                              │
│  Pre-Commit Hook prüft ob Dateien auf Branch UND main geändert wurden.  │
│  Zeigt Warnung mit betroffenen Dateien und Rebase-Empfehlung.           │
│                                                                         │
│  STUFE 2: BRANCH FRESHNESS CHECK (manuell/CLI)                          │
│  ─────────────────────────────────────────────                          │
│  python scripts/check_branch_freshness.py --status                      │
│  python scripts/check_branch_freshness.py --auto-rebase                 │
│  python scripts/check_branch_freshness.py --file-conflicts              │
│                                                                         │
│  STUFE 3: GITHUB BRANCH PROTECTION (einmalig)                           │
│  ─────────────────────────────────────────────                          │
│  "Require branches to be up to date before merging"                     │
│  Setup: bash scripts/setup_branch_protection.sh                         │
│  Oder manuell: GitHub → Settings → Branches → Protection Rules          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**PFLICHT-Workflow bei jedem Push:**
```bash
# VOR dem Push: Branch-Freshness prüfen
python scripts/check_branch_freshness.py --status

# Bei Divergenz: Rebase durchführen
git fetch origin main
git rebase origin/main

# Dann erst pushen
git push -u origin <branch-name>
```

**Claude MUSS bei jedem `git push`:**
1. Zuerst `git fetch origin main` ausführen
2. `check_branch_freshness.py --file-conflicts` prüfen
3. Bei Konflikten: User informieren und Rebase vorschlagen
4. Erst nach Lösung pushen

---

### 🔐 Registry ID Collision Prevention (PFLICHT)

**Problem gelöst:** Merge-Konflikte durch doppelte IDs (z.B. zwei Branches erstellen CAT-24).

**Lösung:** Automatische ID-Prüfung vor jedem Commit.

```bash
# Status aller Registries anzeigen
python scripts/check_registry_ids.py --status

# Nächste verfügbare ID holen
python scripts/check_registry_ids.py --next CAT      # → CAT-26
python scripts/check_registry_ids.py --next CAS      # → CAS-908
python scripts/check_registry_ids.py --next MS-CM    # → MS-CM-003
python scripts/check_registry_ids.py --next PAR-BEH  # → PAR-BEH-018

# Prüfen ob eine ID verfügbar ist
python scripts/check_registry_ids.py --validate CAT-24  # ❌ ALREADY IN USE

# Duplikate finden
python scripts/check_registry_ids.py --check
```

**Pre-Commit Hook blockiert automatisch:**
- Doppelte CAT-XX in theory-catalog.yaml
- Doppelte MS-XX-XXX in theory-catalog.yaml
- Doppelte CAS-XXX in case-registry.yaml
- Doppelte PAR-XX-XXX in parameter-registry.yaml

**PFLICHT vor jedem neuen Registry-Eintrag:**
```bash
# VOR dem Erstellen eines neuen Eintrags:
python scripts/check_registry_ids.py --next <TYPE>

# Beispiel für neue Theorie-Kategorie:
NEXT_CAT=$(python scripts/check_registry_ids.py --next CAT)
echo "Verwende: $NEXT_CAT"  # → CAT-26
```

---

*Version 1.27 | Februar 06, 2026*

**v1.27 Updates (2026-02-06):**
- 🛡️ **Merge Conflict Prevention** - Automatische Erkennung potenzieller Merge-Konflikte VOR dem Commit
- 🔧 **Neues Script** `check_branch_freshness.py` - Branch-Divergenz-Analyse mit File-Conflict-Detection
- ⚠️ **Pre-Commit Hook erweitert** - Warnt wenn Dateien sowohl auf Branch als auch auf `main` geändert wurden
- 📝 **Branch Protection Setup** `setup_branch_protection.sh` - GitHub "require up to date" Rule
- 🔄 **Auto-Rebase Support** - `python scripts/check_branch_freshness.py --auto-rebase` für sichere Rebases

**v1.26 Updates (2026-02-05):**
- 🔐 **Registry Manager** - Proaktive Duplikat-Prävention mit Python API
- 🔧 **Neues Script** `registry_manager.py` - Unified Interface für alle Registries mit Auto-ID
- 📦 **Python API** - `CaseRegistry.add()`, `TheoryModelRegistry.next_id()`, etc.
- 🔄 **Paradigmenwechsel** - Von reaktiv (bei Commit prüfen) zu proaktiv (Duplikat unmöglich)
- 🗃️ **Backup-System** - Automatische Backups vor Registry-Änderungen
- 🔒 **Thread-Safe** - File Locking für parallele Zugriffe
- 🧹 **CAS-Duplikate bereinigt** - CAS-870→908, CAS-871→909

**v1.25 Updates (2026-02-05):**
- 🔐 **Registry ID Collision Prevention** - Verhindert Merge-Konflikte durch doppelte IDs
- 🔧 **Neues Script** `check_registry_ids.py` - Universeller ID-Check für alle Registries
- ⛔ **Pre-Commit Hook erweitert** - Blockiert automatisch doppelte CAT/MS/CAS/PAR IDs
- 📊 **Herhausen Firestorms Paper** - Level 5 Full Integration (CAT-24, MS-CM-001/002, PAR-CM-001-007, CAS-907)
- 🔗 **Basic n Concept** - Dokumentiert in MS-CM-002 (n = variable Anzahl kritischer Interaction Hubs)

**v1.24 Updates (2026-02-03):**
- ✨ **Reverse Engineering Workflow (REW)** - PFLICHT-Workflow für Kausalitätsprüfung & EBF-Compliance-Validierung
- 🔄 **REW Richtung:** OUTPUT → INPUT (Dokumente → Theorien rückwärts)
- 📊 **4 REW-Prüfungen:** REW-1 (Doc→Op), REW-2 (Op→Axiom), REW-3 (Axiom→Belief), REW-4 (Belief→Theory)
- 📈 **REW Compliance-Levels:** REW-0 bis REW-3 (Mindest: REW-2 für EBF-Projekte)
- 📖 **SPÖ EMRK als Referenz-Implementierung:** REW-3 compliant (vollständig)
- 🔗 **Quellcode-Architektur-Dokument:** Mapping Theorien → Beliefs → Axiome → Dokumente
- 📝 Neue Dokumentation: `docs/workflows/reverse-engineering-workflow.md`

**v1.23 Updates (2026-01-31):**
- 🚫 **API-ZUGRIFFS-REGEL** - PFLICHT: Externe APIs IMMER über GitHub Actions nutzen
- 📊 **Paper Database Enrichment** - evidence_tier für 2,528 Papers (Tier 1/2/3)
- 🔧 **Neues Script** `add_evidence_tier.py` - Journal-basierte Qualitätsklassifikation
- 🔧 **Neues Script** `match_authors_to_lit.py` - Lokales Author-to-LIT Matching (694 neue Links)
- 🔧 **Neues Script** `match_papers_to_appendices.py` - OpenAlex API (für GitHub Actions)
- 📝 **Erweiterte Theory-Keywords** - 100+ Keywords in KEYWORD_THEORY_MAPPING
- 📖 **LIT-Appendix Links** - LIT-FEH (143), LIT-KT (152), LIT-SUT (29), LIT-ENK (20), LIT-O (643)

**v1.22 Updates (2026-01-28):**
- ✨ **`/integrate-paper` Skill** - PFLICHT-Workflow für Paper-Integration mit AUTO-TRIGGER
- 📊 **Automatische Paper-Klassifikation** - 7 Kriterien, 5 Integration Levels (MINIMAL→FULL)
- 🔧 **Neues Script** `classify_paper_integration.py` - Automatische Level-Bestimmung
- 📝 **Level-basierte Checklisten** - Klare Komponenten pro Integration Level
- 🧠 **Theory Catalog erweitert** - CAT-17 Household Economics & Time Allocation (156 Theorien)
- 📦 **Goodman et al. (2026)** - Time-Intensive Goods Paper vollständig integriert (Level 5)
- 🔗 **Neue Parameter** - PAR-TA-001 bis PAR-TA-005 (Shadow Price of Time, Time Share, Diversion Ratio)
- 📖 **Neuer Appendix PT** - DOMAIN-PLATFORM Time-Intensive Goods (161 Appendices total)

**v1.21 Updates (2026-01-27):**
- ✨ **Comprehensive CLAUDE.md Refresh** - Vollständige Dokumentation aller Features
- 📊 **API Registry Dokumentation** - 89 externe API-Integrationen dokumentiert (CrossRef, BFS, ESS, WVS, etc.)
- 👥 **Customer Directory** - 20 Kundenprofile mit vollständiger CVA-Struktur (ALPLA, LUKB, UBS, etc.)
- 🔧 **GitHub Actions** - 15 CI/CD Workflows dokumentiert (Notifications, DOI-Lookup, Validation, etc.)
- 📁 **Data Directory Architektur** - 15 Subdirectories mit 354+ YAML-Dateien dokumentiert
- 📝 **Scripts Index** - 151+ Python-Skripte kategorisiert und dokumentiert
- 🎭 **Stakeholder Models** - Formale Registrierung von Focus Group Simulationen
- 🔗 **Paper References** - 346 individuelle Paper-YAML-Dateien in data/paper-references/

**v1.20 Updates (2026-01-27):**
- ✨ **Sales Pipeline Skills** - 9 neue Slash-Commands für Lead-Management und Forecasting
- 📊 `/pipeline-summary` - Kompakte Pipeline-Übersicht mit Balkendiagrammen
- 📊 `/pipeline-report` - Detaillierter Pipeline-Bericht mit Bewegungen
- 💰 `/forecast` - Umsatzprognose mit Best/Expected/Worst Case Szenarien
- 👤 `/lead-card`, `/lead-add`, `/lead-update`, `/new-lead` - Lead-Management
- 📈 `/win-loss` - Deal-Analyse und Win/Loss-Statistiken
- ✅ `/action-list` - Task-Management für Pipeline-Aktivitäten
- 📁 Neue Datenstruktur: `data/sales/` (lead-database.yaml, report-templates.yaml)
- 🎭 `/simulate-stakeholder` - 7-Persona BEATRIX Focus Group Simulation
- 📚 Bibliographie erweitert auf 2,328 Papers (von 2,226)
- 🧠 Theory Catalog erweitert auf 153 Modelle (13 Kategorien)

**v1.19 Updates (2026-01-27):**
- ✨ **`/innosuisse` Skill** - PFLICHT-Workflow für BEATRIX/Innosuisse mit AUTO-TRIGGER
- 📝 8 Fehlertypen-Prävention integriert (CONSISTENCY, CLASSIFICATION, VERIFICATION, etc.)
- 🔧 7-Stellen Checkliste für Kernaussagen, 3-Stellen für Versionsnummern
- 📚 Lerndatenbank-Integration mit automatischer Konsultation
- 📖 Ernst Fehr BEATRIX-Korrektur als SSOT definiert

**v1.18 Updates (2026-01-26):**
- ✨ **Problem-to-Solution Workflow (PSW)** - 6-Phasen Learning Loop für systematische Problemlösung
- 📝 **Appendix VC (METHOD-VALIDATE)** - Formale Dokumentation der Datenkonsistenz-Validierung
- 🔗 **Bidirektionale Cross-References** - VC ↔ BBB, CAL, FRM
- 📊 **Formalisierte Scope Box** - Z1-Z4, IS1-IS4, OS1-OS4, L1-L5 Struktur
- 📖 Neue Dokumentation: `docs/workflows/problem-solution-workflow.md`

**v1.17 Updates (2026-01-26):**
- ✨ **Data Consistency Validation Framework** - 3 neue Validierungsskripte
- 🔗 **Referential Integrity:** Cross-database Referenz-Validierung (Score ≥85% blockiert Commit)
- 📊 **Parameter Consistency:** Verhaltensökonomische Parameter auf Drift prüfen (λ, β, γ, etc.)
- 🌍 **Context Consistency:** Ψ-Dimensionen und Kontext-Faktoren validieren
- 🔧 Pre-Commit Hook erweitert für automatische Daten-Konsistenz-Checks
- 📝 Neue Dokumentation: `docs/workflows/data-consistency-validation.md`

**v1.16 Updates (2026-01-26):**
- ✨ **Schritt 9: Output wählen (Format + Umfang)** zum EBF-Workflow hinzugefügt
- 📤 6 Output-Formate: Markdown, LaTeX, PDF, Word, PPT, Python
- 📏 5 Umfang-Stufen: 1-pager, 3-pager, 10-pager, 30-pager, Full
- 📊 Kombinationsmatrix (Zielgruppe → Format + Umfang)
- 🔧 Regeln O-1 bis O-4 für automatische Auswahl
- 📝 Konvertierungs-Tools Übersicht

**v1.15 Updates (2026-01-23):**
- ✨ **Theory-Papers Bidirektionale Verbindung** zwischen Appendix MS und bcm_master.bib
- 📦 Neues Script `theory_papers.py` für Theory-Paper-Lookup
- 📦 Neue Datenbank `data/theory-catalog.yaml` mit 134 Modellen (13 Kategorien)
- 🔧 Neues BibTeX-Feld `theory_support` für Paper-Theorie-Zuordnung
- 🔧 10C-Matching: `/design-model` → passende Theorien → validierte Papers
- 📝 Appendix MS (REF-MODELSPACE): Scientific Theory Catalog mit EBF-Restriktionen

**v1.14 Updates (2026-01-22):**
- ✨ **Chapter Index Auto-Update** analog zu Appendix Index
- 📝 Neue Datei `chapters/00_chapter_index.tex` mit auto-generierten Tabellen
- 🔧 `generate_chapter_tables.py --update-all` aktualisiert beide Index-Dateien
- 🔧 Pre-Commit Hook staged nun auch `chapters/00_chapter_index.tex`
- 📊 Neue Tabellen: Chapter Types Distribution, CORE Chapters, Prerequisites Matrix
- 📝 Workflow: YAML ändern → Commit → Appendix + Chapter Index aktualisiert!

**v1.13 Updates (2026-01-22):**
- ✨ **Auto-Sync BibTeX → LIT-Appendix** bei Bibliographie-Änderungen via Pre-Commit Hook
- 🔧 Neues Script `sync_bib_to_lit.py` synchronisiert Papers automatisch
- 🔧 Papers mit `use_for = {LIT-BLINDER, ...}` werden automatisch im LIT-Appendix eingetragen
- 📝 Workflow: Paper in BibTeX → Commit → LIT-Appendix aktualisiert
- 📚 Neuer Appendix **BL LIT-BLINDER**: Central Bank Communication Research

**v1.12 Updates (2026-01-22):**
- ✨ **Auto-Update TOC/Index** bei YAML-Änderungen via Pre-Commit Hook
- 🔧 `generate_chapter_tables.py` aktualisiert Kategorie-Counts und Kapitel-Listen automatisch
- 🔧 Pre-Commit Hook staged geänderte Index-Dateien automatisch
- 📝 Workflow vereinfacht: YAML ändern → Commit → fertig!

**v1.11 Updates (2026-01-22):**
- ✨ **Chapter Scope Box** als PFLICHT-Element für alle Kapitel
- 📦 Standardisiertes Format: Ziel / In-Scope / Out-of-Scope / Lieferobjekte
- 📝 Chapter Template (`00_chapter_template.tex`) aktualisiert
- 📝 Chapter 24 als erstes Kapitel mit vollständiger Scope Box
- 🔧 Klare Abgrenzung zwischen Kapitel-Inhalt und Appendix-Delegation

**v1.10 Updates (2026-01-19):**
- ✨ **LIT-Integration Automatisierung** `assign_lit_appendix.py`
- 🔧 Automatische LIT-Appendix Zuweisung (LIT-R, LIT-M, LIT-O)
- 🔧 4-Schritt Entscheidungsbaum nach appendix-category-definitions.md
- 🔧 Interaktiver Modus + BibTeX-Generierung
- 🔧 Autor-Threshold-Prüfung (≥5 Papers für eigenen LIT)

**v1.9 Updates (2026-01-19):**
- ✨ **Bibliographie-Suchskript** `search_bibliography.py` (2,401 Papers durchsuchbar)
- ✨ **PreCommit EIP-Hook** mit automatischer Trigger-Erkennung
- 🔧 EIP-formatierte Ausgabe (`--eip` Flag) für Paper-Suche
- 🔧 Autoren-, Parameter- und Tag-Filter für Bibliographie

**v1.8 Updates (2026-01-19):**
- ✨ **Evidence Integration Pipeline (EIP)** als PFLICHT-Workflow
- ✨ Unified LIT-Taxonomie (LIT-R, LIT-D, LIT-M, LIT-O)
- ✨ Validierungs-Script `check_eip_compliance.py`
- ✨ EIP-Integration in `/design-model` Skill
- 📖 Concept Registry (`data/concept-registry.yaml`)
- 📖 Rejected Concepts Registry (`quality/rejected_concepts.md`)
- 📖 Automatische Trigger-Erkennung (TR1-TR5)
- 📖 Search Priority: Interne Quellen zuerst (bcm_master.bib)

**v1.7 Updates (2026-01-19):**
- ✨ **PFLICHT-Workflow für Interventions-Design** (20-Field Schema aus Kapitel 17)
- ✨ Neuer Skill `/design-intervention` (Light/Hybrid/Profound Mode)
- ✨ Validierungs-Script `check_intervention_compliance.py`
- ✨ Intervention Schema Template (`templates/intervention-schema.yaml`)
- 📖 Crowding-Out Risiken (Social+Financial, Financial+Commitment) systematisch dokumentiert
- 📖 Phase-Dimension Affinity & Segment-Multiplier Matrix integriert

**v1.6 Updates (2026-01-18):**
- 🔒 Appendix Code Availability Checker implementiert
- 📝 Session-Start Hook zeigt Code-Status
- ⛔ Pre-Commit Hook blockiert Code-Duplikate
- 📖 SOP für Code-Verfügbarkeitsprüfung

**v1.5 Updates (2026-01-15):**
- ✨ Neue Customer Strategy Skills (5 Skills)
- ✨ Parametrische Modelle (RPM, MCSM, OSM, CAM)
- ✨ Kundenmodell Datenbank (vollständig dokumentiert)
- ✨ Model Library (Template-basiert, wiederverwendbar)
