# /review - Interaktiver Review mit Konsequenz-Analyse

## Übersicht

Maschinengeführter Review-Prozess, der den User durch Outputs führt und bei jeder Option die **Konsequenzen transparent macht**:

- **Axiom-Auswirkungen** (K1-K10)
- **Parameter-Effekte** (U_IND, U_COLL, U_IDN)
- **Partei-Positionierung** (FPÖ, ÖVP, Grüne, NEOS)
- **Risiko-Analyse**

Nach jeder Wahl: **Bewusstseins-Check** + **Feinadjustierungs-Option**

## Verwendung

```bash
# Review durchführen
/review                              # Review für aktive Anfrage starten
/review ANF-2026-02-02-001           # Spezifische Anfrage reviewen
/review --mode schnell               # Nur Kernfragen (5 min)
/review --mode standard              # Hauptfragen (15 min) [DEFAULT]
/review --mode vollstaendig          # Alle Fragen (30 min)
/review --frage Q-KERN               # Zu spezifischer Frage springen
/review --session REV-EMRK-I1-001    # Bestehende Session fortsetzen
/review --neue-session               # Neue Session starten

# Übersicht & Historie
/review --dashboard                  # Review-Dashboard anzeigen
/review --historie                   # Alle Sessions anzeigen
/review --historie EMRK              # Sessions für Thema
/review --lernerfolge                # Alle Lernerfolge anzeigen
/review --objekt EMRK-WORDING-001    # Status eines Lieferobjekts
```

## Session-Tracking

Jede Review-Session erhält eine eindeutige ID:

```
REV-{THEMA}-I{ITERATION}-{SEQ}

Beispiele:
  REV-EMRK-I1-001    # EMRK, Iteration 1, Session 1
  REV-EMRK-I1-002    # EMRK, Iteration 1, Session 2 (Fortsetzung)
  REV-EMRK-I2-001    # EMRK, Iteration 2, nach Überarbeitung
```

**Session-Status:**
| Status | Bedeutung |
|--------|-----------|
| `gestartet` | Session läuft |
| `pausiert` | Unterbrochen, kann mit `--session` fortgesetzt werden |
| `abgeschlossen` | Alle Fragen beantwortet, Feedback gespeichert |
| `abgebrochen` | Vorzeitig beendet |

## Modi

| Modus | Fragen | Zeit | Wann verwenden |
|-------|--------|------|----------------|
| `schnell` | 3 | ~5 min | Schnelles Feedback zu Kernthemen |
| `standard` | 8 | ~15 min | Normaler Review-Durchlauf |
| `vollstaendig` | 12+ | ~30 min | Umfassender Review inkl. Interview-Situationen |

## Workflow-Struktur

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 0: INITIALISIERUNG                                               │
│  → Anfrage laden, Outputs identifizieren, Axiome laden                  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1-4: FÜR JEDE FRAGE                                              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  1. FRAGE ZEIGEN                                                   │  │
│  │     "Wie bewerten Sie die Kernaussage?"                            │  │
│  │                                                                    │  │
│  │  2. OPTIONEN MIT KONSEQUENZEN                                      │  │
│  │     [A] ✅ PASST SO                                                │  │
│  │         Axiom K2: ✅ | K3: ✅ | K4: ⚠️                             │  │
│  │         U_IND: +0.8 | U_COLL: +0.6 | U_IDN: 0.0                    │  │
│  │         FPÖ-Überschneidung: 60%                                    │  │
│  │         ⚠️ RISIKO: SPÖ-Handschrift nicht erkennbar                 │  │
│  │                                                                    │  │
│  │     [B] 🔄 VARIANTE                                                │  │
│  │         ...                                                        │  │
│  │                                                                    │  │
│  │  3. USER WÄHLT                                                     │  │
│  │                                                                    │  │
│  │  4. BEWUSSTSEINS-CHECK                                             │  │
│  │     "Sind Sie sich bewusst, dass..."                               │  │
│  │     [A1] ✅ JA, so belassen                                        │  │
│  │     [A2] 🔧 FEINADJUSTIEREN                                        │  │
│  │     [A3] ↩️ ANDERE OPTION                                          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: FEEDBACK SAMMELN                                              │
│  → Alle Wahlen in REVIEW_FEEDBACK_{id}_{date}.yaml speichern            │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 6: KONSISTENZ-CHECK                                              │
│  → Widersprechen sich Wahlen? U_IDN-Limit prüfen                        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 7: ITERATION 2 GENERIEREN                                        │
│  → Outputs aktualisieren, neue Version erstellen                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Fragen-Katalog

### Kernbotschaften
| ID | Frage | Optionen |
|----|-------|----------|
| Q-KERN | Kernaussage bewerten | A: Passt / B: Anpassen / C: Tonalität / D: Neu |
| Q-CLOSE | Closer bewerten | A: Passt / B: Variante / C: Anpassen / D: Neu |

### Differenzierung
| ID | Frage | Optionen |
|----|-------|----------|
| Q-DIFF-FPOE | FPÖ-Differenzierung | A: Stark genug / B: Schärfer / C: Softer / D: Anders |
| Q-DIFF-DK | Dänemark-Position | A: Respektvoll / B: Zahlen / C: Ignorieren / D: Warnung |

### 3-Level-System
| ID | Frage | Optionen |
|----|-------|----------|
| Q-L1 | Level 1 (Fakten) | A: Ausreichend / B: Mehr / C: Weniger / D: Andere |
| Q-L2 | Level 2 (Frame) | A: Passt / B: Anpassen / C: Werte-Frame / D: Anderer |
| Q-L3 | Level 3 (Werte) | A: Richtig / B: Mehr Pathos / C: Weniger / D: Weglassen |

### Gesamt
| ID | Frage | Optionen |
|----|-------|----------|
| Q-TON | Gesamttonalität | A: Richtig / B: Zu weich / C: Zu hart / D: Inkonsistent |
| Q-MISS | Fehlende Elemente | Multi-Choice (A-I) |
| Q-PRIO | Prioritäten | Ranking Top 3 |

## Konsequenz-Dimensionen

Bei jeder Option werden angezeigt:

### 1. Axiom-Auswirkungen
```
Axiom K2 (Zahlen):     ✅ Erfüllt
Axiom K3 (Ordnung):    ✅ Erfüllt
Axiom K4 (USP):        ⚠️ Teilweise
Axiom K10 (Nutzen):    ❌ Verletzt → WARNUNG!
```

### 2. Parameter-Effekte
```
U_IND (Individuelle Sicherheit):  +0.8
U_COLL (Kollektive Ordnung):      +0.6
U_IDN (Identität):                 0.0  ← Sollte niedrig bleiben!
```

### 3. Partei-Positionierung
```
| Partei | Überschneidung | Differenzierung |
|--------|----------------|-----------------|
| FPÖ    | 60%            | ❌ Schwach       |
| ÖVP    | 80%            | ⚠️ Kaum         |
| Grüne  | 20%            | ✅ Stark        |
```

### 4. Risiko-Analyse
```
⚠️ RISIKO: Bei dieser Wahl...
• SPÖ-Handschrift nicht erkennbar
• FPÖ-Wähler könnten sich angegriffen fühlen
• Linke Flanke irritiert
```

## Bewusstseins-Check Template

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Sie haben Option {X} gewählt. Sind Sie sich bewusst, dass:             │
│                                                                         │
│  • {Konsequenz 1}                                                       │
│  • {Konsequenz 2}                                                       │
│  • {Konsequenz 3}                                                       │
│                                                                         │
│  Bestätigen Sie diese Wahl?                                             │
│                                                                         │
│  [{X}1] ✅ JA, so belassen                                              │
│  [{X}2] 🔧 FEINADJUSTIEREN                                              │
│         → z.B. "SPÖ-Marker hinzufügen"                                  │
│  [{X}3] ↩️ ANDERE OPTION WÄHLEN                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Output-Dateien

| Datei | Beschreibung |
|-------|--------------|
| `REVIEW_FEEDBACK_{id}_{date}.yaml` | Alle Wahlen strukturiert |
| `REVIEW_PROZESS_{topic}_{date}.md` | Review-Dokumentation |
| `{output}_v{n+1}.md` | Aktualisierte Outputs (Iteration 2) |

## Workflow-Definition

**SSOT:** `data/customers/spo/workflows/WORKFLOW_interaktiver_review.yaml`

## Beispiel-Session

```
User: /review

Claude:
┌─────────────────────────────────────────────────────────────────────────┐
│  🔍 INTERAKTIVER REVIEW                                                 │
│  Anfrage: ANF-2026-02-02-001 (EMRK-Strategie)                          │
│  Modus: STANDARD (8 Fragen, ~15 min)                                   │
│  Axiome: K1-K10 (Ordnung statt Spalten)                                │
└─────────────────────────────────────────────────────────────────────────┘

FRAGE 1/8: KERNAUSSAGE (Q-KERN)

Aktuelle Formulierung:
> «14.156 Abschiebungen. Höchststand. 50% Straftäter. Das funktioniert.»

┌─────────────────────────────────────────────────────────────────────────┐
│  [A] ✅ PASST SO                                                        │
│      Axiom K2: ✅ | K3: ✅ | K4: ⚠️                                     │
│      U_IND: +0.8 | U_COLL: +0.6 | U_IDN: 0.0                           │
│      ⚠️ SPÖ-Handschrift nicht erkennbar                                │
├─────────────────────────────────────────────────────────────────────────┤
│  [B] 🔄 VARIANTE ("40 pro Tag")                                         │
│      Axiom K9: ✅ (populärer)                                          │
│      Salienz: ×1.3                                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  [C] ⚠️ TONALITÄT ANPASSEN                                              │
│      Härter: U_IDN +0.3 ❌ | Weicher: Glaubwürdigkeit -15%             │
├─────────────────────────────────────────────────────────────────────────┤
│  [D] ❌ KOMPLETT NEU                                                    │
│      Empfohlen: "Ordnung im Asylsystem: 14.156..."                     │
└─────────────────────────────────────────────────────────────────────────┘

Ihre Wahl? (A/B/C/D)

User: A

Claude:
┌─────────────────────────────────────────────────────────────────────────┐
│  BEWUSSTSEINS-CHECK                                                     │
│                                                                         │
│  Sie haben Option A gewählt. Sind Sie sich bewusst, dass:               │
│  • Die Aussage KEINE eindeutige SPÖ-Handschrift hat                     │
│  • FPÖ-Überschneidung bei 60% liegt                                    │
│  • U_IDN neutral bleibt (gut für "Ordnung statt Spalten")              │
│                                                                         │
│  [A1] ✅ JA, so belassen                                                │
│  [A2] 🔧 FEINADJUSTIEREN (SPÖ-Marker hinzufügen)                        │
│  [A3] ↩️ ANDERE OPTION WÄHLEN                                           │
└─────────────────────────────────────────────────────────────────────────┘

User: A2

Claude:
Welche Feinadjustierung?
• "Diese Regierung liefert: 14.156 Abschiebungen..."
• "Unter unserer Regierung: 14.156..."
• Eigene Formulierung (Freitext)

User: "Diese Regierung liefert"

Claude: ✅ Notiert. Weiter zu Frage 2/8...
```

## Review-Übersicht & Dashboard

**SSOT:** `data/customers/spo/database/REVIEW_UEBERSICHT.yaml`

### Dashboard anzeigen

```bash
/review --dashboard
```

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 REVIEW-DASHBOARD                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LIEFEROBJEKTE          REVIEWS         COMPLIANCE      LERNERFOLGE     │
│       7                    1               59%              0           │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│  ANFRAGE        OBJEKTE   REVIEWS   AVG SCORE   STATUS                  │
│  ─────────────────────────────────────────────────────────────────────  │
│  EMRK              4         1       6.5/11     🟡 Review läuft         │
│  SOG               2         0         -        ⬜ Nicht reviewed        │
│  SPITAL            1         0         -        ⬜ Nicht reviewed        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Lieferobjekt-Status

```bash
/review --objekt EMRK-WORDING-001
```

Zeigt:
- Aktuelle Version
- Review-Historie (alle Sessions)
- Axiom-Compliance (aktuell + Trend)
- Gaps und offene Punkte

### Lernerfolge

```bash
/review --lernerfolge
```

Zeigt alle dokumentierten Erkenntnisse aus Reviews:
- Was wurde gelernt?
- Aus welcher Session?
- Für welche zukünftigen Outputs relevant?
- Wo bereits umgesetzt?

**Lernerfolg-Schema:**
```yaml
- id: "LEARN-EMRK-001"
  erkenntnis: "Pro-Kopf-Vergleich (AT 156 vs. DK 16) ist stärkstes Argument"
  kategorie: "Inhalt"
  axiom_bezug: "K2 (Zahlen als Beleg)"
  anwendbar_auf: ["Dänemark-Vergleiche", "Migrations-Themen"]
  umgesetzt_in: ["EMRK-WORDING-001 v5.0"]
```

## Verwandte Skills

- `/design-intervention` - Interventions-Design
- `/axiom-check` - Axiom-Compliance prüfen
- `/wording` - Wording erstellen/bearbeiten
