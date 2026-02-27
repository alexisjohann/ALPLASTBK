# Client Context (MIKRO-Ebene)

> Kundenspezifische Kontextfaktoren für individuelle Organisationen

## Struktur

```
clients/
├── ubs/                 ← UBS-spezifisch (161 Faktoren)
│   ├── external/       ← Externe Wahrnehmung (75)
│   ├── internal/       ← Interne Führung (50)
│   └── theory/         ← Organisationstheorie (36)
├── [weitere-kunden]/    ← Erweiterbar
└── ...
```

## MIKRO-Ebene: UBS-Spezifisch (161 Faktoren)

### External (75 Faktoren) - Marktwahrnehmung

| Code | Schicht | Faktoren | Beschreibung |
|------|---------|----------|--------------|
| UBS-INS | Institutionell | 20 | Regulatorische Position, Systemrelevanz |
| UBS-BHV | Behavioral | 30 | Kundenverhalten, Touchpoints, Experience |
| UBS-INT | Transnational | 25 | Globale Positionierung, Cross-Border |

### Internal (50 Faktoren) - Operative Führung

| Code | Dimension | Faktoren | Beschreibung |
|------|-----------|----------|--------------|
| D1 | Strategie & Geschäftsmodell | 10 | Vision, Positionierung |
| D2 | Governance & Struktur | 10 | Organisation, Entscheidungswege |
| D3 | Kultur & Kommunikation | 10 | Werte, interne Kommunikation |
| D4 | Nachhaltigkeit & Verantwortung | 10 | ESG, Purpose |
| D5 | Vertrauen & Wahrnehmung | 10 | Reputation, Stakeholder |

### Theory (36 Faktoren) - Organisationslogik

| Code | Kategorie | Faktoren | Quelle |
|------|-----------|----------|--------|
| UBS-STRAT | Strategie (Meta) | 6 | Roberts/Van den Steen |
| UBS-HR | People | 6 | Organisationstheorie |
| UBS-ARC | Architecture | 6 | Entscheidungsarchitektur |
| UBS-ROU | Routines | 6 | Prozesslogik |
| UBS-CUL | Culture | 6 | Kulturtheorie |
| UBS-LEAD | Leadership | 6 | Führungslogik |

## Unterschied der drei Ebenen

| Aspekt | External (75) | Internal (50) | Theory (36) |
|--------|---------------|---------------|-------------|
| Charakter | Marktposition | Operative Führung | Organisationslogik |
| Fokus | Wahrnehmung | Strategie & Kultur | Entscheidungsarchitektur |
| Quelle | Stakeholder-Sicht | Management-Sicht | Akademische Theorie |
| Wirkung | Reputation | Leistungsfähigkeit | Koordination & Lernen |

## Namenskonvention

```
{kunde}/BCM2_MIKRO_{ebene}_{code}.yaml
```

Beispiele:
- `ubs/external/BCM2_MIKRO_UBS_INS.yaml`
- `ubs/internal/BCM2_MIKRO_UBS_D1_strategy.yaml`
- `ubs/theory/BCM2_MIKRO_UBS_STRAT.yaml`

## EBF-Integration

Die MIKRO-Ebene kalibriert:
- Individuelle Parameter Θ für den Kunden
- Kundenspezifische Komplementarität γ
- Awareness A(·) und Willingness W für Interventionen

## Verknüpfung

```
MAKRO (context/ch/)          →  Schweizer Rahmen (384)
        ↓
MESO (industry/finance-ch/)  →  Branchenspezifika (130)
        ↓
MIKRO (clients/ubs/)         →  Kundenspezifika (161)
────────────────────────────────────────────────────────
TOTAL BEATRIX Complete:                          675 Faktoren
```

## Vertraulichkeit

⚠️ **ACHTUNG:** Kundenspezifische Daten können vertraulich sein.
- `.gitignore` für sensible Dateien verwenden
- Anonymisierte Versionen für öffentliche Repos
