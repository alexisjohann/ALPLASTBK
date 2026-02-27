# Paper Workflow Overview

> **Zentrale Übersicht** über den gesamten Paper-Lebenszyklus im EBF Framework.
> Dieses Dokument verlinkt alle Detail-Dokumentationen — es ist selbst KEIN SSOT für Regeln.

---

## Architektur auf einen Blick

```
                    ┌─────────────────────────┐
                    │   USER NENNT PAPER       │
                    │   (Titel, DOI, Abstract,  │
                    │    PDF oder Volltext)      │
                    └────────────┬──────────────┘
                                 │
                    ┌────────────▼──────────────┐
                    │  SCHRITT 1: DUPLIKAT?      │
                    │  grep in bcm_master.bib    │
                    └────┬──────────────┬────────┘
                         │              │
                    JA (existiert)   NEIN (neu)
                         │              │
                         ▼              ▼
              ┌──────────────┐  ┌───────────────────┐
              │  UPGRADE     │  │  /integrate-paper  │
              │  L1→L2→L3    │  │  (Auto-Trigger)    │
              │              │  │                     │
              │  Skill:      │  │  7-Kriterien-       │
              │  /upgrade-   │  │  Klassifikation     │
              │  paper       │  │  → Level 1-5        │
              └──────────────┘  └─────────┬───────────┘
                                          │
                         ┌────────────────┼────────────────┐
                         ▼                ▼                ▼
                   Level 1-2         Level 3-4         Level 5
                   ┌─────────┐     ┌──────────┐     ┌──────────┐
                   │ BibTeX  │     │ + Case   │     │ Alle 9   │
                   │ + YAML  │     │ + Theory │     │ Komponen.│
                   └────┬────┘     └────┬─────┘     └────┬─────┘
                        │               │                │
                        └───────────────┼────────────────┘
                                        ▼
                         ┌──────────────────────────────┐
                         │  PRE-COMMIT CHECKS            │
                         │  ├── Duplikat-Check (blockiert)│
                         │  ├── BIB↔YAML Konsistenz      │
                         │  ├── Auto-Tag (LIT-Zuweisung)  │
                         │  └── Auto-Sync (LIT-Appendix)  │
                         └──────────────────────────────┘
```

---

## Die 2 SSOTs (Single Sources of Truth)

| SSOT | Pfad | Format | Inhalt |
|------|------|--------|--------|
| **BibTeX** | `bibliography/bcm_master.bib` | BibTeX | Zitierbare Einträge mit EBF-Feldern (`use_for`, `theory_support`, `evidence_tier`) |
| **Paper-YAML** | `data/paper-references/PAP-{key}.yaml` | YAML | Metadaten, Content Level, Key Findings, Behavioral Mapping |

**Bidirektionale Konsistenz:** Jeder BIB-Eintrag hat genau 1 YAML-Datei und umgekehrt.
Validation: `python scripts/check_paper_consistency.py`

---

## Einstiegspunkte (wann welcher Skill?)

| Situation | Skill | Doku |
|-----------|-------|------|
| Neues Paper integrieren | `/integrate-paper` | [integrate-paper.md](../../.claude/commands/integrate-paper.md) |
| Paper manuell aufnehmen (PIP) | `/add-paper` | [add-paper.md](../../.claude/commands/add-paper.md) |
| Paper direkt auf GitHub hochladen | — (automatisch) | [inbox/README.md](../../data/paper-texts/inbox/README.md) |
| Content Level upgraden (L1→L2→L3) | `/upgrade-paper` | [paper-level-upgrade-workflow.md](paper-level-upgrade-workflow.md) |
| Paper-Queue abarbeiten | `/paper-queue` | [paper-integration-queue.yaml](../../data/paper-integration-queue.yaml) |
| Papers klassifizieren (Batch) | `/classify-papers` | [classify-papers.md](../../.claude/commands/classify-papers.md) |

---

## Integration Levels

| Level | Name | Komponenten | Wann? |
|-------|------|-------------|-------|
| **1** | MINIMAL | BibTeX | Paper erwähnt, keine tiefe Relevanz |
| **2** | STANDARD | BibTeX + theory_support + use_for | Stützt bestehende Theorie |
| **3** | CASE | + Case Registry Eintrag | Liefert Praxisbeispiel |
| **4** | THEORY | + Theory Catalog Eintrag | Erweitert/modifiziert Theorie |
| **5** | FULL | Alle 9 Komponenten | Neues Framework/Domain |

**Level 5 — 9 Pflicht-Komponenten:**
1. BibTeX-Eintrag
2. Paper-YAML (`PAP-*.yaml`)
3. theory_support in BIB
4. Case Registry Eintrag
5. Theory Catalog Eintrag
6. Parameter Registry Einträge
7. Volltext (`data/paper-texts/PAP-*.md`)
8. LIT-Appendix Integration
9. Chapter Cross-References

Detail-Workflow: [level5-paper-integration-workflow.md](level5-paper-integration-workflow.md)

---

## Content Levels (C-Dimension)

| Level | Definition | Kriterium |
|-------|-----------|-----------|
| **L0** | Metadata only | Kein S1-S6 |
| **L1** | Research Question bekannt | S1 vorhanden |
| **L2** | Summary/Extract | S1-S4 vorhanden |
| **L3** | Kompletter Originaltext | R1-R4 erfüllt (alle Sektionen, References, >10k Wörter, kein EBF im Text) |

**Auto-Upgrade:** Wenn User Paper-Content teilt, upgradet Claude automatisch (ohne zu fragen).

Detail-Framework: [paper-database-quality-dimensions.md](../frameworks/paper-database-quality-dimensions.md)

---

## Speicherorte

```
data/
├── paper-references/          ← YAML-Metadaten (2,451 Dateien, SSOT)
│   └── PAP-{key}.yaml
├── paper-texts/               ← Volltexte (Separation of Concerns)
│   ├── PAP-{key}.md              Nur Original-Text, KEIN EBF-Kommentar
│   └── inbox/                 ← Drop-Zone für direkte GitHub-Uploads
│       └── *.md / *.txt          Ohne BibTeX-Key, wird automatisch verarbeitet
├── paper-intake/              ← PIP-Protokolle (Aufnahme-Entscheidungen)
│   ├── template.yaml
│   └── 2026/PIP-*.yaml
└── paper-integration-queue.yaml ← Offene Integrationen

bibliography/
└── bcm_master.bib             ← BibTeX-Einträge (2,451, SSOT)
```

---

## Automatische Schutzmechanismen

| Check | Wann | Blockiert? | Script |
|-------|------|------------|--------|
| BIB-Duplikat-Keys | Pre-Commit | **JA** | `.claude/hooks/pre-commit.sh` |
| BIB↔YAML Konsistenz | Pre-Commit | **JA** | `scripts/check_paper_consistency.py` |
| Level-5-Overclaim | Pre-Commit | **JA** | Level Gate in pre-commit |
| LIT-Appendix Auto-Tag | Pre-Commit | Nein (auto) | `scripts/sync_bib_to_lit.py` |
| LIT-Appendix Auto-Sync | Pre-Commit | Nein (auto) | `scripts/sync_bib_to_lit.py` |

---

## Externe APIs (blockiert in Sandbox)

Externe API-Calls (CrossRef, OpenAlex, ORCID) sind in der Claude Code Sandbox **blockiert**.

**Lösung:** GitHub Actions Workflows nutzen.

| Aufgabe | GitHub Action |
|---------|---------------|
| DOI nachschlagen | `gh workflow run doi-lookup.yml` |
| Batch DOI-Lookup | `gh workflow run doi-lookup-batch.yml` |
| Paper generieren | `gh workflow run generate-papers.yml` |

---

## Deprecated (nicht mehr nutzen)

| Was | Ersetzt durch |
|-----|---------------|
| `data/paper-sources.yaml` | `data/paper-references/PAP-*.yaml` |
| `data/extracted_papers.yaml` | Backlog für `/integrate-paper` |
| 44 Scripts in `scripts/` (DEPRECATED-Header) | `/integrate-paper` Workflow |
| `scripts/sync_paper_databases.py` | `scripts/check_paper_consistency.py` |

---

## Alle Detail-Dokumentationen

| Datei | Inhalt |
|-------|--------|
| [.claude/commands/integrate-paper.md](../../.claude/commands/integrate-paper.md) | 12-Schritte Auto-Trigger Workflow |
| [.claude/commands/add-paper.md](../../.claude/commands/add-paper.md) | Manuelles Paper Intake Protocol (PIP) |
| [level5-paper-integration-workflow.md](level5-paper-integration-workflow.md) | Level 5 FULL mit 6-Faktoren-Entscheidung |
| [paper-level-upgrade-workflow.md](paper-level-upgrade-workflow.md) | Content Level Upgrades (L1→L3) |
| [evidence-integration-pipeline.md](evidence-integration-pipeline.md) | Konzept-Validierung mit PRO/CONTRA |
| [../frameworks/paper-database-quality-dimensions.md](../frameworks/paper-database-quality-dimensions.md) | 2D-System (Content × Integration) |
| [data/paper-intake/README.md](../../data/paper-intake/README.md) | PIP-Template + Beispiele |
| [data/paper-texts/README.md](../../data/paper-texts/README.md) | Volltext-Archiv-Spezifikation |
| CLAUDE.md (Abschnitte: Paper-Architektur, /integrate-paper, Content Level Auto-Upgrade) | Regeln + Referenz |
