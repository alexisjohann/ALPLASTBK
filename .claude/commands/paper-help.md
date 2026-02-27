# /paper-help - Kontextabhängige Paper-Workflow-Hilfe

Zeigt die richtige Hilfe je nach Situation — statt 8 Dateien selbst durchsuchen zu müssen.

## Verwendung

```bash
/paper-help                    # Was kann ich mit Papers machen?
/paper-help add                # Wie füge ich ein neues Paper hinzu?
/paper-help upgrade            # Wie upgrade ich ein Paper (L1→L3)?
/paper-help find               # Wie finde ich ein Paper in der DB?
/paper-help levels             # Was bedeuten die 5 Integration Levels?
/paper-help content            # Was bedeuten Content Levels L0-L3?
/paper-help deprecated         # Was ist deprecated?
/paper-help architecture       # Wo liegt was? (SSOTs, Pfade)
/paper-help queue              # Wie funktioniert die Paper-Queue?
/paper-help fulltext           # Wie funktioniert das Volltext-Archiv?
```

## Workflow

Claude liest das Argument (oder fragt nach) und zeigt die passende Hilfe:

### Ohne Argument → Übersicht

Zeige eine kompakte Übersicht mit den wichtigsten Aktionen:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📚 PAPER WORKFLOW — WAS WILLST DU TUN?                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  NEUES PAPER HINZUFÜGEN:                                                │
│  ├── /integrate-paper     Automatische Klassifikation + Integration     │
│  ├── /add-paper           Manuelles Intake (PIP-Protokoll)              │
│  └── /add-paper --quick   Schnellmodus (nur BibTeX)                     │
│                                                                         │
│  BESTEHENDES PAPER VERBESSERN:                                          │
│  ├── /upgrade-paper PAP-x  Content Level upgraden (L1→L2→L3)           │
│  └── /paper-queue          Offene Integrationen abarbeiten              │
│                                                                         │
│  PAPER FINDEN:                                                          │
│  ├── python scripts/search_bibliography.py "suchbegriff"               │
│  ├── python scripts/search_bibliography.py --author "Fehr"             │
│  └── python scripts/theory_papers.py --theory MS-RD-001                │
│                                                                         │
│  QUALITÄT PRÜFEN:                                                       │
│  ├── python scripts/check_paper_consistency.py  BIB↔YAML Check         │
│  └── /classify-papers                           Batch-Klassifikation    │
│                                                                         │
│  MEHR INFO: /paper-help [topic]                                         │
│  VOLLE DOKU: docs/workflows/paper-workflow-overview.md                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### `add` → Neues Paper hinzufügen

Referenz: `.claude/commands/integrate-paper.md` und `.claude/commands/add-paper.md`

Zeige:
1. Unterschied /integrate-paper vs /add-paper
2. Die 5 Auto-Trigger (Titel, DOI, Autoren+Jahr, Abstract, expliziter Request)
3. Die 7 Klassifikations-Kriterien + Level-Bestimmung
4. Checkliste je nach Level

### `upgrade` → Paper upgraden

Referenz: `docs/workflows/paper-level-upgrade-workflow.md`

Zeige:
1. Content Level Definitionen (L0-L3)
2. Was für ein Upgrade nötig ist (S1-S6 Kriterien)
3. L3-Anforderungen (R1-R4)
4. Auto-Upgrade Regel (Claude upgradet automatisch wenn Content geteilt wird)

### `find` → Paper in DB finden

Zeige Script-Beispiele:
```bash
# Volltextsuche
python scripts/search_bibliography.py "mental accounting"

# Autorensuche
python scripts/search_bibliography.py --author "Thaler"

# EIP-formatiert (mit PRO/CONTRA)
python scripts/search_bibliography.py --eip "framing"

# Theorie → Papers
python scripts/theory_papers.py --theory MS-RD-001

# Paper → Theorien
python scripts/theory_papers.py --paper kahneman1979prospect

# Statistiken
python scripts/search_bibliography.py --stats
```

### `levels` → Integration Levels 1-5

Referenz: CLAUDE.md → /integrate-paper Sektion

Zeige die 5 Levels mit Komponenten-Liste und wann welches Level gilt.

### `content` → Content Levels L0-L3

Referenz: `docs/frameworks/paper-database-quality-dimensions.md`

Zeige die 4 Content Levels mit S1-S6 und R1-R4 Kriterien.

### `deprecated` → Was ist deprecated?

Zeige:
```
DEPRECATED Dateien (NICHT bearbeiten):
├── data/paper-sources.yaml          → Migriert zu PAP-*.yaml
├── data/extracted_papers.yaml       → 137 Papers als Backlog
├── papers/fulltext/                 → Migriert zu data/paper-texts/
└── 44 Scripts in scripts/           → Alle mit DEPRECATED-Header
    (add_*_papers*.py, generate_lit_*.py, fix_*.py, etc.)

AKTIVE Alternativen:
├── /integrate-paper                 → Neues Paper hinzufügen
├── scripts/check_paper_consistency.py → Konsistenz prüfen
└── scripts/search_bibliography.py   → Papers suchen
```

### `architecture` → Wo liegt was?

Zeige die SSOT-Tabelle + Speicherorte aus `docs/workflows/paper-workflow-overview.md`.

### `queue` → Paper Integration Queue

Referenz: `data/paper-integration-queue.yaml`

Zeige:
```bash
/paper-queue                  # Status anzeigen
/paper-queue --next           # Nächstes Paper
/paper-queue --process 5      # 5 Papers abarbeiten
```

### `fulltext` → Volltext-Archiv

Referenz: `data/paper-texts/README.md`

Zeige:
- Pfad: `data/paper-texts/PAP-{key}.md`
- Nur Original-Text, KEIN EBF-Kommentar
- Referenz in YAML: `full_text.available: true`
- L3-Anforderungen: R1 (alle Sektionen), R2 (References), R3 (>10k Wörter), R4 (kein EBF im Text)

## Referenzen

| Dokument | Pfad |
|----------|------|
| **Gesamtübersicht** | `docs/workflows/paper-workflow-overview.md` |
| /integrate-paper Skill | `.claude/commands/integrate-paper.md` |
| /add-paper Skill | `.claude/commands/add-paper.md` |
| /upgrade-paper Skill | `.claude/commands/upgrade-paper.md` |
| Level 5 Workflow | `docs/workflows/level5-paper-integration-workflow.md` |
| Upgrade Workflow | `docs/workflows/paper-level-upgrade-workflow.md` |
| 2D Quality Framework | `docs/frameworks/paper-database-quality-dimensions.md` |
| PIP Template | `data/paper-intake/template.yaml` |
| Volltext-Archiv | `data/paper-texts/README.md` |
