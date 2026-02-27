# /add-paper - Paper Intake Protocol Workflow

Standardisierter Workflow zum Hinzufügen wissenschaftlicher Papers ins EBF.

**WICHTIG:** Claude füllt das PIP **automatisch vor** - User bestätigt nur!

## Verwendung

```bash
/add-paper                           # Interaktiver Modus
/add-paper "DOI"                     # Mit DOI starten
/add-paper "Autor Jahr Titel"        # Mit Suchbegriff starten
/add-paper --quick                   # Schnellmodus (nur Pflichtfelder)
```

## Workflow: Claude füllt vor, User bestätigt

### Phase 1: Paper identifizieren & Metadaten holen

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AUTOMATISCH (Claude macht):                                            │
├─────────────────────────────────────────────────────────────────────────┤
│  1. DOI → CrossRef API → Metadaten abrufen                             │
│  2. Oder: WebSearch → Paper finden                                      │
│  3. Prüfen ob bereits in bcm_master.bib                                │
│  4. PIP-ID generieren: PIP-YYYY-MM-DD-NNN                              │
│  5. Paper-ID generieren: PAP-nachnamejahrkurzwort                      │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 2: Claude analysiert & füllt vor

**Claude füllt ALLE Felder automatisch aus basierend auf:**

| Quelle | Was wird extrahiert |
|--------|---------------------|
| **Abstract/Paper** | 10C-Dimensionen, Theorien, Parameter |
| **DOI/CrossRef** | Titel, Autoren, Jahr, Journal, DOI |
| **Journal** | Evidence Tier, peer_reviewed |
| **Autoren** | Bekannte Autoren → LIT-Appendix Zuordnung |
| **Keywords** | use_for Klassifikation |
| **EBF-Analyse** | theory_support, consistency check |

### Phase 3: User bestätigt/korrigiert

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📄 PIP VORAUSGEFÜLLT - Bitte prüfen:                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SECTION 1: IDENTIFIKATION ✅                                           │
│  Paper-ID: PAP-alnajjar2026rationaldisagreement                        │
│  Titel: Rational Disagreement                                           │
│  Autoren: Al-Najjar, Uhlig                                             │
│  Jahr: 2026 | Quelle: NBER WP 34727 | DOI: 10.3386/w34727             │
│                                                                         │
│  SECTION 4: EBF-INTEGRATION ✅                                          │
│  10C-Dimensionen:                                                       │
│    • CORE-HOW (high) - γ-Matrix wird belief-abhängig                   │
│    • CORE-AWARE (high) - Aggregate vs Individual Awareness             │
│  Theorie: MS-SI-015 (NEU) | use_for: LIT-O, METHOD-GAME               │
│                                                                         │
│  SECTION 5: ENTSCHEIDUNG ✅                                             │
│  → ACCEPT (confidence: high)                                           │
│  Begründung: Schliesst theoretische Lücke, testbar, Top-Autoren        │
│                                                                         │
│  ─────────────────────────────────────────────────────────────────────  │
│  [Enter] = Bestätigen | [e] = Editieren | [a] = Abbrechen              │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 4: Dateien erstellen & Commit

Bei Bestätigung erstellt Claude automatisch:
1. `data/paper-intake/YYYY/PIP-YYYY-MM-DD-NNN.yaml`
2. BibTeX-Eintrag in `bcm_master.bib`
3. Theory Catalog Update (falls neue Theorie)
4. Git Commit & Push

## Evidence Tiers

| Tier | Kriterien | Beispiele |
|------|-----------|-----------|
| **1 (Gold)** | RCT, Top-5 Journal, repliziert | QJE, AER, Econometrica |
| **2 (Silver)** | Peer-reviewed, solide Methodik | JF, MS, JEBO |
| **3 (Bronze)** | Working Paper, theoretisch | NBER, SSRN, Preprints |

## Checkliste vor Abschluss

```
☐ PIP-ID korrekt formatiert
☐ Paper-ID folgt Konvention (PAP-nachname_jahr_kurzwort)
☐ Mindestens eine 10C-Dimension zugeordnet
☐ use_for enthält mindestens einen Eintrag
☐ Entscheidung mit Begründung dokumentiert
☐ BibTeX-Eintrag mit allen EBF-Feldern
☐ PIP-Datei validiert
```

## Beispiel-Session

```
> /add-paper "10.3386/w34727"

📄 Paper gefunden:
   Titel: Rational Disagreement
   Autoren: Al-Najjar, Uhlig
   Jahr: 2026
   Quelle: NBER Working Paper 34727

🔍 Prüfe ob bereits in EBF... Nicht gefunden.

📝 Starte Paper Intake Protocol...

PIP-ID: PIP-2026-01-28-001
Paper-ID: PAP-alnajjar2026rationaldisagreement

Welche 10C-Dimensionen? [CORE-HOW, CORE-AWARE]
Theorie-Zuordnung? [Neu: MS-SI-015]
use_for? [LIT-O, METHOD-GAME, CORE-HOW, CORE-AWARE]

Entscheidung? [ACCEPT]
Begründung? [Schliesst theoretische Lücke, testbar, Top-Autoren]
Confidence? [HIGH]

✅ PIP erstellt: data/paper-intake/2026/PIP-2026-01-28-001.yaml
✅ BibTeX hinzugefügt: PAP-alnajjar2026rationaldisagreement
✅ Theory Catalog: MS-SI-015 hinzugefügt

Commit erstellen? [y/n]
```

## Verwandte Skills

| Skill | Beschreibung |
|-------|--------------|
| `/classify-papers` | Mehrere Papers klassifizieren |
| `/find-model` | Theorie für Paper finden |
| `/design-model` | Neues Modell aus Paper ableiten |
