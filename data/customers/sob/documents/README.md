# SOB Projekt-Dokumente

Dieses Verzeichnis enthält alle Projekt-Dokumente für die Schweizerische Südostbahn AG (SOB).

## Struktur

```
documents/
├── SOB001/                    # Mission Statement Projekt (Okt 2025 - Jan 2026)
│   ├── meetings/              # Meeting-Protokolle
│   ├── workshops/             # Workshop-Materialien & Ergebnisse
│   ├── analysis/              # EBF-Analysen, Modelle
│   ├── presentations/         # Präsentationen (VR, MA, etc.)
│   └── deliverables/          # Finale Lieferobjekte
│
└── SOB002/                    # Strategiemodell Projekt (Feb - Apr 2026)
    ├── meetings/              # Meeting-Protokolle
    ├── workshops/             # Workshop-Materialien
    ├── analysis/              # Strategiemodell-Analysen
    ├── presentations/         # Präsentationen
    └── deliverables/          # Finale Lieferobjekte
```

## Namenskonvention

```
YYYY-MM-DD_[TYP]_[BESCHREIBUNG].[EXT]

Beispiele:
- 2025-10-15_MTG_kickoff-workshop.md
- 2025-11-20_WS_mission-statement-entwicklung.md
- 2026-01-28_PRE_vr-praesentation.pdf
- 2026-01-28_DEL_mission-statement-final.pdf
```

## Typen-Codes

| Code | Typ | Beschreibung |
|------|-----|--------------|
| MTG | Meeting | Protokolle, Notizen |
| WS | Workshop | Workshop-Materialien |
| ANA | Analysis | Analysen, Berechnungen |
| PRE | Presentation | Präsentationen |
| DEL | Deliverable | Finale Lieferobjekte |
| INT | Internal | Interne Notizen |

## Verknüpfungen

- **Kontext-Vektor:** `../sob_context.yaml`
- **Projekt-Scopes:** `../projects/SOB001_scope.yaml`, `../projects/SOB002_scope.yaml`
- **EBF-Modell:** `MOD-MSR-001` (Mission Statement Resonance Model)
- **Lead:** `LEAD-048` in `data/sales/lead-database.yaml`
- **Person:** `PER-EXT-001` (Armin Weber) in `data/person-registry.yaml`
