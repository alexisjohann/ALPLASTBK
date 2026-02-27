# /upgrade-paper - Paper Integration Upgrade Workflow

> **Zweck:** Systematisches Upgrade eines bestehenden Papers auf ein höheres Integration Level
>
> **SSOT:** `docs/workflows/level5-paper-integration-workflow.md`

---

## Verwendung

```bash
/upgrade-paper                                          # Interaktiv
/upgrade-paper PAP-benabou_2018_narratives --level 5    # Spezifisches Paper
/upgrade-paper --list-pending                           # Papers mit niedrigem Level
/upgrade-paper --check PAP-xxx                          # Level eines Papers prüfen
```

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: STATUS PRÜFEN                                                 │
│     ├── Aktuelles Level (I0-I5) aus Paper YAML                         │
│     └── Fehlende Komponenten identifizieren                            │
│                                                                         │
│  PHASE 2: ZIEL-LEVEL BESTIMMEN                                         │
│     ├── Klassifikation mit 7 Kriterien                                 │
│     └── User-Bestätigung                                               │
│                                                                         │
│  PHASE 3: ARCHITEKTUR (nur Level 5)                                    │
│     └── 6-Faktoren-Framework für CORE-Erweiterungen                    │
│                                                                         │
│  PHASE 4: KOMPONENTEN HINZUFÜGEN                                       │
│     └── Level-spezifische Checkliste                                   │
│                                                                         │
│  PHASE 5: VALIDIERUNG + COMMIT                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6-Faktoren-Framework (Level 5)

Für **JEDEN** CORE-Appendix:

| Faktor | Frage | Erweitern wenn... |
|--------|-------|-------------------|
| **F1** | Neue Struktur? | JA |
| **F2** | Neues Axiom nötig? | JA |
| **F3** | Dimensionalität ändert? | JA |
| **F4** | Struktur (nicht nur Parameter)? | JA |
| **F5** | Gilt universal? | JA |
| **F6** | Neuer Mechanismus? | JA |

### Architektur-Prinzip

```
LIT (Primary) → CORE (nur strukturell) → Chapters (nur Cross-Ref)
```

---

## 11-Komponenten-Checkliste (Level 5)

```
☐ 1.  BibTeX Entry (6 EBF-Felder)
☐ 2.  Theory Catalog (MS-XX-XXX)
☐ 3.  Case Registry (CAS-XXX)
☐ 4.  Parameter Registry (PAR-XXX-XXX)
☐ 5.  LIT Appendix Section (PRIMARY!)
☐ 6.  CORE Extensions (6-Faktoren!)
☐ 7.  BCM2 Context Factors
☐ 8.  Chapter-Appendix Mapping
☐ 9.  Chapter Cross-References
☐ 10. Paper YAML (vollständig)
☐ 11. Paper Full-Text Archive
```

---

## Referenz-Implementation

**Paper:** Bénabou/Falk/Tirole (2018) "Narratives, Imperatives, and Moral Reasoning"
**YAML:** `data/paper-references/PAP-benabou_2018_narratives.yaml`
**Branch:** `claude/add-nber-paper-R9r8Y`

**Dokumentation:** `docs/workflows/level5-paper-integration-workflow.md`

---

*Version 1.0 | 2026-02-04*
