# /find-model - EBF Model-Building Workflow

> ⚠️ **WORK IN PROGRESS (WIP)** - Dieser Workflow ist in aktiver Entwicklung.
> Feedback und Verbesserungsvorschläge willkommen!

Startet den vollständigen EBF Model-Building Workflow für eine beliebige Frage.

## Usage

```
/find-model                           # Interaktiv (fragt nach Modus)
/find-model --mode schnell            # SCHNELL: 10 min, ~800 Worte
/find-model --mode standard           # STANDARD: 45 min, ~3000 Worte
/find-model --mode tief               # TIEF: 2+ Stunden, ~5000 Worte
```

## Workflow

Der Workflow folgt immer denselben 6 Schritten:

### Schritt 0: Session Initialisieren (aus Frage ableiten)
- Session-ID generieren: `EBF-S-{YYYY}-{MM}-{DD}-{DOMAIN}-{SEQ}`
- Domain aus Frage ableiten: REL/FIN/HLT/ENV/POL/ORG/EDU/OTH
- Modus bestätigen
- **Frage-Klassifikation (aus Frage ableiten):**
  - Frage-Typ: Analyse vs. Verhaltensänderung
  - Verhaltensziel: Ja/Nein (→ aktiviert/deaktiviert Schritt 5)
  - Scope: In-Scope / Out-of-Scope
  - Lieferobjekte: Was bekommt der User?
- **Output-Format:**
  - **SCHNELL:** Automatisch 1-Pager PDF (keine Wahl)
  - **STANDARD/TIEF:** Wahl aus F1-F6 (siehe unten)
- User bestätigt oder korrigiert

### Schritt 1: Kontext
- Ψ-Dimensionen identifizieren (Ψ_I, Ψ_S, Ψ_K, Ψ_C, Ψ_T, Ψ_E, Ψ_F)
- 10C CORE Fragen zuordnen
- **Bei STANDARD:** Verbesserungsvorschläge (K1-K5 / Alle)
- User-Feedback abwarten

### Schritt 2: Modell
- Datenbank-Lookup: `model-registry.yaml` + `theory-catalog.yaml`
- Passendes Modell wählen oder aus 10C bauen
- **Bei STANDARD:** Verbesserungsvorschläge (M1-M7 / Alle)
- User-Feedback abwarten → Modell-Evolution

### Schritt 3: Parameter
- LLMMC Prior generieren
- **Bei STANDARD:** Bayesian Updating mit BCM2 + Papers
- Posterior-Tabelle zeigen
- **Bei STANDARD:** Verbesserungsvorschläge (P1-P6 / Alle)
- User-Feedback abwarten

### Schritt 4: Antwort
- Modell anwenden → Ergebnis berechnen
- Sensitivitätsanalyse
- Robustheit prüfen
- **Bei STANDARD:** Verbesserungsvorschläge (A1-A6 / Alle)
- User-Feedback abwarten

### Schritt 5: Intervention (NUR wenn Verhaltensziel in Schritt 0)
- **Wird übersprungen wenn:** `has_behavior_goal: false` in Schritt 0
- **Wird aktiviert wenn:** `has_behavior_goal: true` (z.B. "Wie bringe ich...")
- Ziel-Verhalten definieren (Δ)
- 10C-Target identifizieren (AWARE, WHO, WHAT, HOW, WHEN)
- Intervention aus Toolkit wählen (Appendix HHH)
- Phase-Affinity prüfen (Chapter 18)
- Crowding-Out Risiken prüfen
- **Bei STANDARD:** Verbesserungsvorschläge (I1-I6 / Alle)
- User-Feedback abwarten

### Schritt 6: Abschlussbericht
- SCHNELL: ~500 Worte
- STANDARD: ~3000 Worte
- TIEF: ~5000+ Worte

### Schritt 7: Speichern & Sync (AUTOMATISCH bei STANDARD/TIEF)

**PFLICHT:** Am Ende jedes STANDARD/TIEF-Workflows werden ALLE 5 Datenbanken automatisch beschrieben.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AUTOMATISCHE SPEICHERUNG (Schritt 7)                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  7a. SESSION speichern                                                  │
│      → data/model-building-session.yaml                                 │
│      → Alle Schritte 0-6, User-Feedback, Learnings                     │
│                                                                         │
│  7b. MODELL speichern (wenn neu/geändert)                              │
│      → data/model-registry.yaml                                         │
│      → 10C-Spec, Segmente, γ-Matrix, Theorien                          │
│                                                                         │
│  7c. INTERVENTION speichern (wenn Schritt 5 aktiv)                     │
│      → data/intervention-registry.yaml                                  │
│      → PRJ-XXX + INT-XXX Einträge                                      │
│                                                                         │
│  7d. OUTPUT speichern                                                   │
│      → data/output-registry.yaml (Registry-Eintrag)                    │
│      → outputs/sessions/{SESSION_ID}/F{N}_{name}_v1.md (Datei)         │
│                                                                         │
│  7e. PARAMETER updaten (wenn neue/geänderte Werte)                     │
│      → data/parameter-registry.yaml                                     │
│      → Neue Parameter oder Updates aus Analyse                         │
│                                                                         │
│  7f. GIT: Commit + Push                                                │
│      → Alle geänderten Dateien committen                               │
│      → Auf aktuellen Branch pushen                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Claude MUSS am Ende von Schritt 6:**
1. User informieren: "Speichere in Datenbanken..."
2. Alle 5 YAML-Dateien aktualisieren (Edit/Write)
3. Report-Datei schreiben (outputs/sessions/...)
4. `git add` + `git commit` + `git push` ausführen
5. User bestätigen: "Gespeichert in: [Liste der Dateien]"

**Superkey-Verbindungen sicherstellen:**
- Alle Einträge verwenden dieselbe Session-ID
- model_id in intervention + output + parameter referenzieren
- Similarity-Index in output-registry aktualisieren

## Datenbank-Verbindungen (5-Datenbank-Architektur)

Alle Datenbanken sind über den **Superkey** (Session-ID) verbunden:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  5-DATENBANK-ARCHITEKTUR mit SUPERKEY                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                     ┌─────────────────────────┐                        │
│                     │  1️⃣ SESSION             │                        │
│                     │  model-building-        │                        │
│                     │  session.yaml           │                        │
│                     │  EBF-S-YYYY-MM-DD-..    │  ← SUPERKEY (Root)     │
│                     └───────────┬─────────────┘                        │
│                                 │                                       │
│          ┌──────────────────────┼──────────────────────┐               │
│          │                      │                      │               │
│          ▼                      ▼                      ▼               │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐          │
│  │ 2️⃣ MODEL      │    │ 3️⃣ INTERVENTION│    │ 4️⃣ OUTPUT     │          │
│  │ model-        │    │ intervention- │    │ output-       │          │
│  │ registry.yaml │    │ registry.yaml │    │ registry.yaml │          │
│  │ EBF-MOD-XXX   │    │ PRJ-XXX       │    │ EBF-OUT-XXX   │          │
│  └───────┬───────┘    └───────┬───────┘    └───────┬───────┘          │
│          │                    │                    │                   │
│          └────────────────────┼────────────────────┘                   │
│                               │                                        │
│                               ▼                                        │
│                     ┌─────────────────────────┐                        │
│                     │  5️⃣ PARAMETER           │                        │
│                     │  parameter-registry.yaml│                        │
│                     │  PAR-XXX-NNN            │                        │
│                     │                         │                        │
│                     │  Verbindet:             │                        │
│                     │  • Literatur (BibTeX)   │                        │
│                     │  • Beobachtete Werte    │                        │
│                     │  • DACH-Anpassungen     │                        │
│                     └─────────────────────────┘                        │
│                                                                         │
│  ZUSÄTZLICH:                                                           │
│  ├── theory-catalog.yaml (Theorien für Modelle)                        │
│  ├── bcm_master.bib (Paper-Referenzen)                                 │
│  └── outputs/sessions/{SESSION_ID}/ (Report-Dateien)                   │
│                                                                         │
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
| Report-Datei | `outputs/sessions/{SESSION_ID}/F{N}_{name}_v{V}.md` |

## Beispiel

```
User: /find-model --mode standard

Claude:
┌─────────────────────────────────────────────────────────────────┐
│  SESSION INITIALISIERT                                          │
├─────────────────────────────────────────────────────────────────┤
│  Session-ID: EBF-S-2026-01-25-XXX-001                          │
│  Modus: STANDARD                                                │
│                                                                 │
│  Bitte stelle deine Frage:                                      │
└─────────────────────────────────────────────────────────────────┘

User: Ist Alevitentum näher zu Zoroastrismus oder Sunnismus?

Claude: [Startet Schritt 1: Kontext...]
```

## Vergleich der Modi

| Aspekt | SCHNELL | STANDARD | TIEF |
|--------|---------|----------|------|
| User-Feedback | Minimal | Pro Schritt | Pro Schritt + Iteration |
| Modell-Quelle | Direkt 10C | Registry + Catalog | Alle + Alternativen |
| Parametrisierung | LLMMC | LLMMC + Bayes | Monte Carlo |
| Intervention | Wenn Ziel | Wenn Ziel + Optionen | Wenn Ziel + Alternativen |
| **Output-Format** | **1-Pager (fix)** | **Wahl F1-F6** | **Wahl F1-F6 + Multiple** |
| Report | ~500 Worte | ~3000 Worte | ~5000+ Worte |
| Dauer | ~10 min | ~45 min | ~2+ Stunden |

## Frage-Klassifikation (Schritt 0)

| Signal in Frage | → Ableitung |
|-----------------|-------------|
| "Ist X näher zu Y oder Z?" | Analyse, kein Verhaltensziel |
| "Wie bringe ich... dazu..." | Verhaltensänderung, Ziel = Δ |
| "Warum machen Menschen X?" | Analyse, kein Verhaltensziel |
| "Was kann ich tun, damit..." | Verhaltensänderung, Ziel = Δ |
| "Soll ich X oder Y?" | Entscheidung, evtl. Verhaltensziel |
| Domainwörter (Heizung, Sparen...) | → Domain (ENV, FIN...) |

## Output-Format (Schritt 0)

**SCHNELL:** Automatisch 1-Pager PDF (keine Wahl nötig)

**STANDARD/TIEF:** User wählt aus:

| Code | Format | Beschreibung | Seiten |
|------|--------|--------------|--------|
| F1 | PowerPoint | Board-Präsentation | 10 Slides |
| F2 | Executive Summary | Management-Entscheidung | 1-2 Seiten |
| F3 | Vollbericht | Dokumentation | 10-20 Seiten |
| F4 | Technical Note | Methodische Details | 5 Seiten |
| F5 | Markdown/Chat | Inline-Antwort | - |
| F6 | Alle | Komplettes Package | F1+F2+F3 |
