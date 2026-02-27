# Paper Database Strategy

> **⚠️ DEPRECATED (2026-02-08)** — Dieses Dokument beschreibt die alte Architektur.
> Die aktuelle SSOT-Architektur ist:
> - **Metadata:** `data/paper-references/PAP-{key}.yaml` (2,322 Dateien)
> - **Bibliography:** `bibliography/bcm_master.bib` (2,322 Einträge)
> - **Workflow:** `/integrate-paper`
> - **Aktuelle Doku:** `docs/workflows/paper-workflow-overview.md`

## Zwei Datenbanken, Ein System

Das EBF verwendet zwei Paper-Datenbanken, die **immer synchronisiert** sein müssen.

---

## 📊 paper-sources.yaml — MASTER

**Location:** `data/paper-sources.yaml`

**Role:** Single Source of Truth für alle Paper-Daten

**Format:** YAML (hierarchisch, reich strukturiert)

**Primäre Nutzer:**
- LLMs und AI-Assistenten
- LLMMC-Pipeline für Parameter-Extraktion
- Python-Skripte und Analysen
- `/case` und `/intervention` Skills

**Enthält:**
```yaml
- id: PAP-kahneman1979prospectprospect
  authors: [Kahneman, Daniel; Tversky, Amos]
  year: 1979
  title: "Prospect Theory: An Analysis of Decision under Risk"
  evidence_tier: 1
  use_for: [CORE-WHERE, parameter, LLMMC]
  parameter: "lambda = 2.25, alpha = 0.88"
  key_findings:
    - finding: "Loss aversion λ ≈ 2.25"
      domain: finance
      stage: action
      effect_size: 2.25
  9c_coordinates:
    - domain: finance
      psi_dominant: framing
      gamma: 0.5
      key_insight: "Reference-dependent utility"
  linked_cases: [CASE-010, CASE-012]
```

**Wann hier ändern:**
- ✅ Neue Papers hinzufügen
- ✅ evidence_tier aktualisieren
- ✅ key_findings ergänzen
- ✅ 9c_coordinates verfeinern
- ✅ linked_cases verknüpfen

---

## 📋 framework_paper_mapping.csv — DERIVED VIEW

**Location:** `bibliography/framework_paper_mapping.csv`

**Role:** Flache Projektion für menschliche Nutzung

**Format:** CSV (tabellarisch, Excel-kompatibel)

**Primäre Nutzer:**
- Forscher für Quick Reference
- Excel/Google Sheets Analysen
- Reports und Präsentationen
- Schnelle Filterung nach Appendix/Tier

**Enthält:**
```csv
Paper_ID,Author,Year,Title,Appendix,Framework_Element,Psi_Dimension,...,Evidence_Tier
PAP-kahneman1979prospectprospect,"Kahneman, Daniel; Tversky, Amos",1979,Prospect Theory,U,"CORE-WHERE,parameter",framing,...,1
```

**⚠️ WICHTIG:**
- Diese Datei wird **automatisch aus YAML generiert**
- **Nie manuell editieren** — Änderungen werden überschrieben!

---

## 🔄 Synchronisation

### Nach jeder YAML-Änderung:

```bash
python3 scripts/yaml_to_csv_sync.py
```

### Workflow:

```
1. Paper in YAML hinzufügen/ändern
   └── data/paper-sources.yaml

2. Sync-Skript ausführen
   └── python3 scripts/yaml_to_csv_sync.py

3. Beide Dateien committen
   └── git add data/paper-sources.yaml bibliography/framework_paper_mapping.csv
   └── git commit -m "feat: Add new paper XYZ"
```

---

## 🛠️ Verfügbare Skripte

| Skript | Zweck |
|--------|-------|
| `yaml_to_csv_sync.py` | YAML → CSV Synchronisation |
| `sync_paper_databases.py` | Bidirektionale Sync (Legacy) |
| `classify_evidence_tiers.py` | Automatische Tier-Klassifikation |

---

## 📈 Aktuelle Statistiken

| Metrik | Wert |
|--------|------|
| **Total Papers** | 828 |
| **Tier 1 (Causal)** | 194 (23.4%) |
| **Tier 2 (Experimental)** | 452 (54.6%) |
| **Tier 3 (Correlational)** | 116 (14.0%) |
| **Tier 4 (Anecdotal)** | 14 (1.7%) |
| **Tier 5 (Theory)** | 52 (6.3%) |

---

## 🎯 Entscheidungsbaum: Welche DB nutzen?

```
Willst du...

├─ Paper-Daten programmatisch verarbeiten?
│  └─ → paper-sources.yaml
│
├─ Schnell ein Paper nachschlagen?
│  └─ → framework_paper_mapping.csv (Excel öffnen)
│
├─ LLMMC-Parameter extrahieren?
│  └─ → paper-sources.yaml (evidence_tier filtern)
│
├─ Report/Präsentation erstellen?
│  └─ → framework_paper_mapping.csv (Export)
│
└─ Neues Paper hinzufügen?
   └─ → paper-sources.yaml (dann sync!)
```

---

*Letzte Aktualisierung: 2026-01-17*
