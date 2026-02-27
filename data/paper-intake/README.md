# Paper Intake Protocol (PIP)

> Standardisiertes Aufnahmeprotokoll für wissenschaftliche Papers im EBF

## Zweck

Das Paper Intake Protocol (PIP) dokumentiert die Entscheidungsgrundlage für jedes Paper, das in das EBF aufgenommen wird. Es gewährleistet:

1. **Nachvollziehbarkeit** - Warum wurde das Paper aufgenommen?
2. **Qualitätssicherung** - Systematische Bewertung jedes Papers
3. **Integration** - Klare Zuordnung zu 10C-Dimensionen und Theorien
4. **Follow-up** - Tracking von Updates und Validierungen

## Verzeichnisstruktur

```
data/paper-intake/
├── README.md           # Diese Dokumentation
├── template.yaml       # Leeres Template für neue PIPs
├── index.yaml          # Übersicht aller PIPs (auto-generiert)
└── 2026/               # Jahr-basierte Organisation
    ├── PIP-2026-01-28-001.yaml
    ├── PIP-2026-01-28-002.yaml
    └── ...
```

## PIP-ID Format

```
PIP-{YYYY}-{MM}-{DD}-{SEQ}

Beispiel: PIP-2026-01-28-001
```

## Pflicht- vs. Optionale Sections

| Section | Status | Beschreibung |
|---------|--------|--------------|
| **1. Identifikation** | PFLICHT | Paper-ID, Datum, bibliografische Daten |
| 2. Entdeckungskontext | Optional | Wie wurde das Paper gefunden? |
| 3. Qualitätsbewertung | Optional | Methodische Bewertung |
| **4. EBF-Integration** | PFLICHT | 10C-Dimensionen, Theorien, Parameter |
| **5. Entscheidung** | PFLICHT | Accept/Reject mit Begründung |
| 6. Cross-References | Optional | Verbindungen zu anderen Papers/Appendices |
| 7. Follow-up | Optional | Ausstehende Aktionen |

## Workflow

### Option A: Via Slash Command (empfohlen)

```bash
/add-paper "DOI oder Titel"
```

Der Skill führt interaktiv durch alle Pflicht-Sections.

### Option B: Manuell

1. Template kopieren:
   ```bash
   cp data/paper-intake/template.yaml data/paper-intake/2026/PIP-YYYY-MM-DD-NNN.yaml
   ```

2. Pflicht-Sections ausfüllen (1, 4, 5)

3. Paper zu `bcm_master.bib` hinzufügen

4. Validieren:
   ```bash
   python scripts/validate_pip.py data/paper-intake/2026/PIP-*.yaml
   ```

5. Commit:
   ```bash
   git add data/paper-intake/ bibliography/bcm_master.bib
   git commit -m "feat(paper): Add [Author] [Year] via PIP-YYYY-MM-DD-NNN"
   ```

## Evidence Tiers

| Tier | Beschreibung | Kriterien |
|------|--------------|-----------|
| **1 (Gold)** | Höchste Qualität | RCT, Top-5 Journal, repliziert |
| **2 (Silver)** | Gute Qualität | Peer-reviewed, solide Methodik |
| **3 (Bronze)** | Akzeptabel | Working Paper, theoretisch, Surveys |

## Entscheidungs-Outcomes

| Outcome | Wann verwenden |
|---------|----------------|
| `accept` | Paper erfüllt alle Kriterien |
| `reject` | Paper nicht geeignet für EBF |
| `conditional` | Akzeptiert mit Bedingungen (z.B. "wenn publiziert") |
| `defer` | Entscheidung vertagt (z.B. mehr Info nötig) |

## Automatisierung

### Pre-Commit Hook

Der Pre-Commit Hook prüft:
- Jedes neue Paper in `bcm_master.bib` hat ein PIP
- Alle Pflicht-Sections sind ausgefüllt
- PIP-ID Format ist korrekt

### Index-Generierung

```bash
python scripts/generate_pip_index.py
```

Generiert `index.yaml` mit Übersicht aller PIPs.

## Beispiel

Siehe `2026/PIP-2026-01-28-001.yaml` für ein vollständiges Beispiel (Al-Najjar & Uhlig 2026).

## Änderungshistorie

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 2026-01-28 | Initial release |
