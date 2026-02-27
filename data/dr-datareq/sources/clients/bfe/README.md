# BFE Kontextvektor-Architektur

> Bundesamt für Energie - FehrAdvice Behavioral Context Integration

## Übersicht

Diese Struktur implementiert einen **bidirektionalen Learning Loop** zwischen:
- **Generischen Kontextvektoren** (MAKRO/MESO)
- **Projektspezifischen Modellen** (10C-basiert)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        KONTEXTVEKTOR-HIERARCHIE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  MAKRO (BCM2_04_KON)           384 Faktoren Schweiz                    │
│  └── context/ch/*.yaml                                                  │
│           │                                                             │
│           │ erbt & filtert                                              │
│           ▼                                                             │
│  MESO (BCM2_MESO_ENERGY_CH)    34 Faktoren Energie-Sektor              │
│  └── industry/energy/                                                   │
│           │                                                             │
│           │ erbt & filtert                                              │
│           ▼                                                             │
│  MIKRO (BCM2_MIKRO_BFE)        Organisation + Zielgruppen              │
│  └── clients/bfe/external/                                              │
│           │                                                             │
│           │ instanziiert                                                │
│           ▼                                                             │
│  PROJEKTE                       10C-Modelle + Kontext-Subset           │
│  └── clients/bfe/projects/                                              │
│           │                                                             │
│           │ generiert                                                   │
│           ▼                                                             │
│  LEARNINGS                      Parameter-Updates + Neue Faktoren      │
│  └── projects/*/learnings.yaml                                          │
│           │                                                             │
│           └─────────────────────────────────────────────────────────┐   │
│                                                                     │   │
│           ▲ propagiert zurück                                       │   │
│           │                                                         ▼   │
│  MIKRO ◄──┴─────────────────────────────────────────────────────────┘   │
│  MESO  ◄────────────────────────────────────────────────────────────┘   │
│  MAKRO ◄────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Verzeichnisstruktur

```
clients/bfe/
├── external/
│   └── BCM2_MIKRO_BFE_context.yaml    # Organisations-Kontextvektor
│
├── projects/
│   ├── template/                       # Vorlage für neue Projekte
│   │   ├── model.yaml                  # 10C-Modell Template
│   │   ├── context_subset.yaml         # Kontext-Selektion Template
│   │   └── learnings.yaml              # Learnings Template
│   │
│   ├── 2026_heizungsersatz/           # Beispiel-Projekt (anzulegen)
│   │   ├── model.yaml
│   │   ├── context_subset.yaml
│   │   └── learnings.yaml
│   │
│   └── [weitere Projekte]/
│
├── learnings/
│   └── BFE_context_enrichments.yaml   # Aggregierte Learnings
│
└── README.md                          # Diese Datei
```

## Workflow

### 1. Neues Projekt starten

```bash
# Projekt-Ordner aus Template erstellen
cp -r projects/template projects/YYYY_projektname

# model.yaml ausfüllen mit 10C-Modell
# context_subset.yaml: Relevante Kontextfaktoren selektieren
```

### 2. Kontext-Faktoren selektieren

Im `context_subset.yaml`:
1. **MAKRO-Faktoren** aus `BCM2_04_KON_*.yaml` selektieren
2. **MESO-Faktoren** aus `BCM2_MESO_energy_ch.yaml` selektieren
3. **MIKRO-Faktoren** aus `BCM2_MIKRO_BFE_context.yaml` übernehmen
4. **Hypothesen** formulieren über Kontextfaktoren

### 3. Projekt durchführen

- Intervention implementieren
- Daten erheben
- Ergebnisse messen

### 4. Learnings dokumentieren

Im `learnings.yaml`:
1. **Ergebnisse vs. Vorhersagen** dokumentieren
2. **Hypothesen-Tests** auswerten
3. **Neue Faktoren** identifizieren
4. **Parameter-Updates** für existierende Faktoren
5. **Propagation** in MESO/MAKRO planen

### 5. Learnings propagieren

```yaml
# In learnings.yaml definieren:
context_updates:
  new_factors_meso:
    - factor:
        id: "ENE-PSY-XX"
        name: "Neuer Faktor"
        ...
      propagation_status: "pending"

  parameter_updates_meso:
    - factor_id: "ENE-PSY-02"
      field: "salienz"
      old_value: 0.68
      new_value: 0.73
      propagation_status: "pending"
```

Dann in `BCM2_MESO_energy_ch.yaml`:
```yaml
learning_log:
  entries:
    - date: "2026-06-15"
      project: "BFE-2026-001"
      type: "parameter_update"
      content:
        factor_id: "ENE-PSY-02"
        field: "salienz"
        old_value: 0.68
        new_value: 0.73
```

## Dateien

### BCM2_MIKRO_BFE_context.yaml

**Zweck:** Organisations-spezifischer Kontextvektor für das BFE

**Inhalt:**
- Organisation (Mandat, Zuständigkeiten)
- Zielgruppen (WHO - Haushalte, KMU, Kantone, etc.)
- Interventionsfelder (WHAT - Heizung, Solar, E-Mobilität, Effizienz)
- Kontext-Relevanz-Mapping (welche MESO/MAKRO Faktoren sind relevant)
- Strategische Implikationen
- BCM-Modul-Kopplung

### Projekt-Templates

| Datei | Zweck |
|-------|-------|
| `model.yaml` | Vollständiges 10C-Modell für das Projekt |
| `context_subset.yaml` | Selektierte Kontextfaktoren + Hypothesen |
| `learnings.yaml` | Ergebnisse + Propagations-Tracking |

## Integration mit EBF

### 10C Dimensionen im BFE-Kontext

| 10C | BFE-Anwendung |
|-----|---------------|
| **WHO** | Haushalte, KMU, Kantone - differenzierte Zielgruppen |
| **WHAT** | u_F (Kosten), u_E (Klima), u_P (Komfort), u_S (Normen) |
| **HOW** | Intervention-Mix (10C dimensions), Komplementarität |
| **WHEN** | Kritische Momente (Heizungsdefekt, Hauskauf) |
| **WHERE** | Choice Architecture, Defaults, Kontext |
| **AWARE** | Awareness-Gaps, Wissensbarrieren |
| **READY** | Handlungsbereitschaft, Barrieren |
| **STAGE** | BCJ Phase (Unaware → Maintaining) |
| **HIERARCHY** | Entscheidungsebenen (L0-L3) |

### Psi-Dimensionen

Primär für BFE:
- `kappa_INST` - Regulierung, Förderung, Gesetze
- `kappa_ARCH` - Defaults, Opt-outs, Vereinfachung
- `kappa_SOCIAL` - Normen, Social Proof
- `kappa_AWX` - Awareness, Information

## Beispiel-Anwendung

### Projekt "Heizungsersatz Nudge 2026"

1. **Projekt anlegen:**
   ```bash
   cp -r projects/template projects/2026_heizungsersatz
   ```

2. **10C-Modell definieren** (model.yaml):
   - WHO: Eigentümer EFH, >50 Jahre, fossile Heizung >15 Jahre
   - WHAT: Wechsel zu Wärmepumpe
   - WHEN: Bei Heizungsdefekt (kritischer Moment)
   - ...

3. **Kontext selektieren** (context_subset.yaml):
   - ENE-PSY-02 (Heizungs-Identität) → Barriere
   - ENE-SOC-01 (Nachbarschafts-Norm) → Enabler
   - ENE-REG-06 (Heizungsersatz-Pflichten) → Rahmen

4. **Nach Abschluss** (learnings.yaml):
   - ENE-PSY-02 Salienz höher als erwartet → Update MESO
   - Neuer Faktor "Installateur-Vertrauen" entdeckt → Neuer MESO-Faktor

## Verwandte Dateien

| Ebene | Datei | Faktoren |
|-------|-------|----------|
| MAKRO | `context/ch/BCM2_04_KON_*.yaml` | 384 |
| MESO | `industry/energy/BCM2_MESO_energy_ch.yaml` | 34 |
| MIKRO | `clients/bfe/external/BCM2_MIKRO_BFE_context.yaml` | - |

---

*Version 1.0 | 2026-01-23 | FehrAdvice & Partners AG*
