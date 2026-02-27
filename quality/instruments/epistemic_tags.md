# Epistemic Status Tags für EBF

## Übersicht

Jeder Parameter, jede Behauptung und jedes Konstrukt sollte mit einem Epistemic Tag versehen sein, der den Vertrauenslevel angibt.

## Die 5 Tag-Kategorien

### EMP - Empirically Validated
```
Vertrauenslevel: ★★★★★
```

**Definition:** Direkter empirischer Nachweis aus peer-reviewed Publikation.

**Kriterien:**
- Publiziert in peer-reviewed Journal
- Eigene oder replizierte Datenanalyse
- Identifikationsstrategie dokumentiert (RCT, IV, DiD, etc.)

**Beispiele:**
- `λ = 2.25` [EMP: Tversky & Kahneman 1992]
- `β = 0.7` [EMP: Laibson 1997, repliziert in DellaVigna 2009]

**LaTeX-Syntax:**
```latex
\epistemic{EMP}{Quelle}
```

---

### THR - Theoretically Derived
```
Vertrauenslevel: ★★★★☆
```

**Definition:** Logisch aus etablierten Axiomen/Theoremen abgeleitet.

**Kriterien:**
- Formaler Beweis vorhanden
- Basiert auf peer-reviewed Theorie
- Ableitungsschritte dokumentiert

**Beispiele:**
- Monotone Comparative Statics [THR: Milgrom 1994 Theorem 4]
- Supermodularität impliziert Komplementarität [THR: Topkis 1998]

**LaTeX-Syntax:**
```latex
\epistemic{THR}{Ableitung aus [Quelle]}
```

---

### LLM - LLM-Monte-Carlo Estimated
```
Vertrauenslevel: ★★★☆☆
```

**Definition:** Via LLM-MC Simulation geschätzt.

**Kriterien:**
- Persona-Spezifikation dokumentiert
- Sample Size angegeben (n ≥ 100)
- Confidence Intervals berichtet
- Validierung gegen bekannte Werte (wo möglich)

**Beispiele:**
- `γ_FP = 0.09 ± 0.02` [LLM: n=500, Claude 3.5, Jan 2026]
- `δ_S = 0.04` [LLM: Swiss persona, n=200]

**LaTeX-Syntax:**
```latex
\epistemic{LLM}{n=X, Model, Date}
```

**Wichtig:** LLM-Schätzungen sind NICHT peer-reviewed und sollten als vorläufig behandelt werden.

---

### ILL - Illustrative
```
Vertrauenslevel: ★★☆☆☆
```

**Definition:** Beispielhafte Werte ohne empirische oder theoretische Basis.

**Kriterien:**
- Plausibel im Größenordnungsbereich
- Dient der Demonstration
- MUSS als illustrativ gekennzeichnet sein

**Beispiele:**
- `γ_DE = 0.05` [ILL: Annahme für Beispielrechnung]
- Anna's Diskontfaktor `β = 0.6` [ILL: Persona-Konstruktion]

**LaTeX-Syntax:**
```latex
\epistemic{ILL}{Zweck}
```

**Warnung:** ILL-Parameter dürfen NICHT als Grundlage für Schlussfolgerungen dienen.

---

### HYP - Hypothetical
```
Vertrauenslevel: ★☆☆☆☆
```

**Definition:** Spekulative Annahme für theoretische Exploration.

**Kriterien:**
- Keine empirische Basis beansprucht
- Dient Gedankenexperimenten
- Kann kontrafaktisch sein

**Beispiele:**
- "Falls γ > 0.5, dann..." [HYP]
- Level L∞ Utility [HYP: Theoretisches Limit]

**LaTeX-Syntax:**
```latex
\epistemic{HYP}{Annahme}
```

---

## Aggregationsregeln

Wenn ein Konstrukt aus mehreren Parametern besteht:

| Komponenten | Gesamt-Tag |
|-------------|------------|
| Alle EMP | EMP |
| EMP + THR | THR |
| Enthält LLM | LLM |
| Enthält ILL | ILL |
| Enthält HYP | HYP |

**Regel:** Der Gesamt-Tag ist der schwächste Einzeltag.

---

## Visualisierung

### Farbschema für Dokumente

| Tag | Farbe | RGB |
|-----|-------|-----|
| EMP | Grün | #22c55e |
| THR | Blau | #3b82f6 |
| LLM | Gelb | #eab308 |
| ILL | Orange | #f97316 |
| HYP | Rot | #ef4444 |

### LaTeX-Makros

```latex
\newcommand{\tagEMP}[1]{\textcolor{green!70!black}{\textbf{[EMP:} #1\textbf{]}}}
\newcommand{\tagTHR}[1]{\textcolor{blue!70!black}{\textbf{[THR:} #1\textbf{]}}}
\newcommand{\tagLLM}[1]{\textcolor{yellow!70!black}{\textbf{[LLM:} #1\textbf{]}}}
\newcommand{\tagILL}[1]{\textcolor{orange!70!black}{\textbf{[ILL:} #1\textbf{]}}}
\newcommand{\tagHYP}[1]{\textcolor{red!70!black}{\textbf{[HYP:} #1\textbf{]}}}
```

---

## Audit-Protokoll

Für jedes Assessment dokumentieren:

1. **Parameter-Zählung:**
   - Total Parameter
   - Davon getaggt
   - Verteilung EMP/THR/LLM/ILL/HYP

2. **Konstrukt-Status:**
   - Neue Konstrukte (FEPSDE, 8Ψ, etc.)
   - Deren aggregierter Tag

3. **Referenz-Audit:**
   - Peer-reviewed vs. Working Papers
   - Verifizierte vs. nicht-verifizierte Zitate
