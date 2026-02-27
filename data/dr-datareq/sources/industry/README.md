# Industry Context (MESO-Ebene)

> Branchenspezifische Kontextfaktoren zwischen Makro (Länder) und Mikro (Kunden)

## Struktur

```
industry/
├── finance-ch/          ← Schweizer Finanzindustrie
│   ├── basis/          ← Heutige Bankenwelt (50 Faktoren)
│   └── extended/       ← Finanzökonomie 2040 (80 Faktoren)
├── finance-at/          ← Österreichische Finanzindustrie (später)
├── finance-de/          ← Deutsche Finanzindustrie (später)
└── ...                  ← Weitere Branchen
```

## MESO-Ebene: Finanzindustrie CH (130 Faktoren)

### Basis-Dimensionen (50 Faktoren)

| Code | Dimension | Faktoren | Beschreibung |
|------|-----------|----------|--------------|
| FI-ESG | Nachhaltigkeit | 10 | ESG-Reporting, Green Finance |
| FI-GOV | Regulierung | 10 | FINMA, Compliance, Governance |
| FI-GVW | Wettbewerb | 10 | Marktanteile, Konsolidierung |
| FI-KES | Technologie | 10 | Digitalisierung, Effizienz |
| FI-KND | Kunden | 10 | Vertrauen, Experience |

### Extended-Dimensionen (80 Faktoren)

| Code | Dimension | Faktoren | Beschreibung |
|------|-----------|----------|--------------|
| FI-FIN | Finanzmarkt-Architektur | 15 | Marktstruktur 2040 |
| FI-CAP | Kapitalmärkte | 15 | Anlagetrends, Asset Classes |
| FI-RSK | Risikolandschaft | 15 | Systemrisiken, Szenarien |
| FI-DIG | Digitale Ökonomie | 20 | DeFi, CBDC, Tokenisierung |
| FI-TRU | Vertrauenslogik | 15 | Institutionelles Vertrauen |

## Namenskonvention

```
{branche}-{land}/BCM2_MESO_{code}_{name}.yaml
```

Beispiel: `finance-ch/BCM2_MESO_FI_basis.yaml`

## EBF-Integration

Die MESO-Ebene kalibriert:
- κ_INST (Institutioneller Kontext) → Branchenregulierung
- κ_ARCH (Choice Architecture) → Branchenstandards
- Komplementarität γ → Branchenspezifische Interaktionen

## Verknüpfung

```
MAKRO (context/ch/)     →  Schweizer Rahmen
        ↓
MESO (industry/finance-ch/)  →  Branchenspezifika
        ↓
MIKRO (clients/ubs/)    →  Kundenspezifika
```
