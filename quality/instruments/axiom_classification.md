# Axiom-Klassifikation im EBF Framework

> **SSOT:** `docs/frameworks/core-framework-definition.yaml` → Sektion `epistemology.axiom`

## Die 3 Axiom-Typen

### 1. Strukturelles Axiom (Structural Axiom)

**Definition:** Definiert die Struktur des Frameworks selbst.

| Eigenschaft | Wert |
|-------------|------|
| Evidenz erforderlich | **NEIN** |
| Epistemic Tag | THR |
| Kann widerlegt werden | Nein (nur "weniger nützlich") |

**Kriterien:**
- Definiert Kategorien, Taxonomien, Klassifikationen
- Ist eine Modellierungsentscheidung
- Konsistenz ist das Hauptkriterium

**Beispiele:**
```latex
\begin{axiom}[EIT-1]{10C Completeness}
\textbf{Type:} structural

\textbf{Statement:} Jede Intervention I lässt sich vollständig durch
die 10 CORE-Dimensionen kategorisieren.

\textbf{Evidence:} Nicht erforderlich (Modellierungsentscheidung)

\textbf{Interpretation:} Das 10C Framework ist hinreichend für
Interventionsbeschreibung.
\end{axiom}
```

---

### 2. Empirisches Axiom (Empirical Axiom)

**Definition:** Behauptet eine empirische Tatsache als Grundlage.

| Eigenschaft | Wert |
|-------------|------|
| Evidenz erforderlich | **JA** |
| Minimum | 1 peer-reviewed Zitat |
| Empfohlen | 3+ peer-reviewed Zitate |
| Epistemic Tag | EMP |
| Kann widerlegt werden | Ja |

**Kriterien:**
- Macht eine Behauptung über die Realität
- Könnte durch Daten widerlegt werden
- **MUSS** Literaturzitat haben
- Zitat **MUSS** peer-reviewed sein

**Beispiele:**
```latex
\begin{axiom}[EIT-9]{Crowding-Out Constraint}
\textbf{Type:} empirical

\textbf{Statement:} γ(T6, T7) < 0: Finanzielle Anreize untergraben
soziale Motivation.

\textbf{Evidence:}
- Deci (1971): Early experimental evidence
- Frey & Oberholzer-Gee (1997): Field evidence from NIMBY
- Gneezy & Rustichini (2000): Day-care late pickup study

\textbf{Interpretation:} T6 und T7 sind partielle Substitute,
nicht Komplemente.
\end{axiom}
```

---

### 3. Theoretisches Postulat (Theoretical Postulate)

**Definition:** Abgeleitet aus etablierten Theorien.

| Eigenschaft | Wert |
|-------------|------|
| Evidenz erforderlich | **JA** (Ableitung) |
| Evidenztyp | Verweis auf Quelltheorie |
| Epistemic Tag | THR |
| Kann widerlegt werden | Nur wenn Quelltheorie widerlegt |

**Kriterien:**
- Logisch aus etablierter Theorie abgeleitet
- Ableitungsschritte **MÜSSEN** dokumentiert sein
- Quelltheorie **MUSS** peer-reviewed sein

**Beispiele:**
```latex
\begin{axiom}[EIT-6]{Portfolio Composition}
\textbf{Type:} theoretical

\textbf{Statement:} I_H = Σ_i w_i · I_i mit Σ w_i = 1

\textbf{Derivation:} Folgt aus konvexer Kombinationstheorie.
Wenn I_i ∈ [0,1]^9 und Σ w_i = 1, dann I_H ∈ [0,1]^9.

\textbf{Source:} Rockafellar (1970), Convex Analysis

\textbf{Interpretation:} Intervention-Portfolios sind konvexe
Kombinationen primitiver Interventionen.
\end{axiom}
```

---

## Entscheidungsbaum: Welcher Typ?

```
Definiert das Axiom Kategorien/Struktur?
├── JA → STRUKTURELL (kein Evidenzbedarf)
└── NEIN
    ├── Abgeleitet aus etablierter Theorie?
    │   ├── JA → THEORETISCHES POSTULAT (Ableitung dokumentieren)
    │   └── NEIN → EMPIRISCHES AXIOM (Zitate PFLICHT!)
```

---

## Validierung: Checkliste

### Vor jedem Axiom prüfen:

```
☐ Axiom-Typ explizit angegeben (structural/empirical/theoretical)
☐ Code-Format korrekt ([PREFIX]-[NUMBER])
☐ Statement formal formuliert
☐ Interpretation vorhanden
☐ Implication vorhanden
☐ Cross-References vorhanden
```

### Zusätzlich für EMPIRISCHE Axiome:

```
☐ Mindestens 1 peer-reviewed Zitat
☐ Zitat in bcm_master.bib vorhanden
☐ Empfohlen: 3+ Zitate für robuste Evidenz
```

### Zusätzlich für THEORETISCHE Postulate:

```
☐ Quelltheorie zitiert
☐ Ableitungsschritte dokumentiert
```

---

## Epistemic Tag Zuordnung

| Axiom-Typ | Primärer Tag | Vertrauenslevel |
|-----------|--------------|-----------------|
| Strukturell | THR | ★★★★☆ |
| Empirisch | EMP | ★★★★★ |
| Theoretisch | THR | ★★★★☆ |

**Aggregationsregel:** Bei zusammengesetzten Konstrukten gilt der schwächste Tag.

---

## Häufige Fehler

### Fehler 1: Empirisches Axiom ohne Zitat

```latex
% FALSCH
\begin{axiom}[EIT-X]{Loss Aversion}
\textbf{Statement:} λ ≈ 2.25
\textbf{Evidence:} [FEHLT!]  ← VALIDATION ERROR
\end{axiom}

% RICHTIG
\begin{axiom}[EIT-X]{Loss Aversion}
\textbf{Type:} empirical
\textbf{Statement:} λ ≈ 2.25
\textbf{Evidence:} Tversky & Kahneman (1992), JRU
\end{axiom}
```

### Fehler 2: Typ nicht angegeben

```latex
% FALSCH
\begin{axiom}[EIT-X]{Some Axiom}
\textbf{Statement:} ...
% Type fehlt! ← VALIDATION ERROR
\end{axiom}

% RICHTIG
\begin{axiom}[EIT-X]{Some Axiom}
\textbf{Type:} structural  ← PFLICHT
\textbf{Statement:} ...
\end{axiom}
```

### Fehler 3: Theoretisches Postulat ohne Ableitung

```latex
% FALSCH
\begin{axiom}[EIT-X]{Derived Property}
\textbf{Type:} theoretical
\textbf{Statement:} X impliziert Y
% Derivation fehlt! ← VALIDATION ERROR
\end{axiom}

% RICHTIG
\begin{axiom}[EIT-X]{Derived Property}
\textbf{Type:} theoretical
\textbf{Statement:} X impliziert Y
\textbf{Derivation:} Aus Theorem Z folgt... [Quelle Jahr]
\end{axiom}
```

---

## Referenzen

- **SSOT:** `docs/frameworks/core-framework-definition.yaml` → `epistemology`
- **Epistemic Tags:** `quality/instruments/epistemic_tags.md`
- **Template:** `appendices/00_appendix_template.tex`

---

*Version 1.0 | 2026-01-20*
