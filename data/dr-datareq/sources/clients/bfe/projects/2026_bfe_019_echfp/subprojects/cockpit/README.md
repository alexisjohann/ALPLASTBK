# Behavioral Impact Cockpit

> Sub-Projekt von BFE_019_ECHfP (Energie Schweiz für Private)

## Übersicht

Das **Behavioral Impact Cockpit** ist ein Dashboard zur Messung der Kampagnenwirkung der ECHfP-Kampagne über vier Kerndimensionen plus Gesamt-Score.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BEHAVIORAL IMPACT COCKPIT                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
│   │    A    │  │    W    │  │    I    │  │    T    │  │   GESAMT    │  │
│   │Awareness│  │Willing- │  │ Impact  │  │  Trust  │  │    SCORE    │  │
│   │         │  │  ness   │  │         │  │         │  │             │  │
│   │  ████   │  │  ███    │  │  ██     │  │  ████   │  │    ███      │  │
│   │  72%    │  │  58%    │  │  34%    │  │  81%    │  │    61%      │  │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────────┘  │
│                                                                         │
│   Filter: [Zeit ▼] [Zielgruppe ▼] [Region ▼]    Export: [PDF] [CSV]    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## KPI-Framework: A-W-I-T

| KPI | Name | Beschreibung | 10C Dimension |
|-----|------|--------------|---------------|
| **A** | Awareness | Bekanntheit der Kampagne/Massnahmen | AWARE |
| **W** | Willingness | Handlungsbereitschaft der Zielgruppe | READY |
| **I** | Impact | Tatsächliche Verhaltensänderung | STAGE |
| **T** | Trust | Vertrauen in Absender/Massnahmen | WHAT (u_S) |
| **G** | Gesamt-Score | Aggregierter Index | - |

## Timeline

```
Dez 2025                Jan 2026                Feb 2026                Mär 2026
    │                       │                       │                       │
    ▼                       ▼                       ▼                       ▼
┌───────┐ ┌─────────────────────────┐ ┌─────────────────────┐ ┌───────────────┐
│ AP1   │ │ AP2    AP3    AP4       │ │ AP7    AP8    AP9   │ │ AP8           │
│ KPI   │ │ Frage- Review Briefing  │ │ CMS    Überg. Ausw. │ │ Übergabe      │
│ Logik │ │ bogen        Intervista │ │                     │ │ Abschluss     │
└───────┘ └─────────────────────────┘ └─────────────────────┘ └───────────────┘
    │           │                           │                       │
  19.12       15-23.01                    15.02                   01.03
    ▲                                                               ▲
    │                                                               │
 MS1: KPI-Architektur                                    MS6: Cockpit übergeben
```

## Arbeitspakete

| AP | Name | Verantwortlich | Deadline | Status |
|----|------|----------------|----------|--------|
| AP 1 | KPI-Logik & Architektur | Lucas, Manuel | 19.12.25 | ✅ |
| AP 2 | Fragebogenerstellung | Andrea, Lucas, Manuel | 15.01.26 | 🔄 |
| AP 3 | Review & Freigabe | Alexis, Andrea | 23.01.26 | ⏳ |
| AP 4 | Briefing Intervista | Andrea, Alexis | 15.03.26 | ⏳ |
| AP 5 | Dashboard-Entwicklung | Alexis, Manuel, Isabella | 15.01.26 | 🔄 |
| AP 6 | Integration externer Daten | Alexis, Isabella | 31.01.26 | 🔄 |
| AP 7 | CMS/Textlösung | Alexis, Isabella | 15.02.26 | ⏳ |
| AP 8 | Übergabe & Dokumentation | Alexis, Andrea | 01.03.26 | ⏳ |
| AP 9 | Auswertung der Daten | Manuel, Lucas, Andrea | 08.02.26 | ⏳ |
| AP 10 | Abstimmung Hakuna Matata | Manuel, Lucas, Andrea | 31.01.26 | ⏳ |
| AP 11 | Projektmanagement | - | tbd | 🔄 |

**Legende:** ✅ Abgeschlossen | 🔄 In Bearbeitung | ⏳ Ausstehend

## Team

### FehrAdvice
- **Lucas** - KPI-Architektur, Datenmodell
- **Manuel** - KPI-Architektur, Dashboard-Entwicklung
- **Andrea** - Fragebogen, Review, Übergabe
- **Alexis** - Review, Dashboard, Integration, Übergabe
- **Isabella Danda** - Dashboard-Entwicklung, Integration

### Externe Partner
- **Intervista** - Feldarbeit, Online-Befragung
- **Hakuna Matata** - Abstimmung Auswertung
- **EVAI** - Social-Listening-Tool

### Kunde
- **BFE** - Auftraggeber, Freigabe
- **c-rk** - Review

## Dateien

| Datei | Beschreibung |
|-------|--------------|
| `projektplan.yaml` | Vollständiger Terminplan mit allen APs |
| `kpi_architecture.yaml` | KPI-Definitionen, Formeln, Gewichtungen |
| `README.md` | Diese Datei |

## EBF Integration

Das Cockpit misst die Wirkung entlang der **Behavioral Customer Journey (BCJ)**:

```
BCJ Phase        │ Primärer KPI │ Was wird gemessen?
─────────────────┼──────────────┼────────────────────────────────
unaware          │ A            │ Kennen sie die Kampagne?
aware            │ A, T         │ Vertrauen sie dem Absender?
considering      │ W            │ Sind sie bereit zu handeln?
intending        │ W, I         │ Planen sie konkret?
acting           │ I            │ Haben sie gehandelt?
maintaining      │ I, T         │ Bleibt das Verhalten stabil?
```

## Nächste Schritte

1. **Bis 15.01.26:** Fragebogen fertigstellen (AP2)
2. **Bis 23.01.26:** BFE-Freigabe einholen (AP3)
3. **Bis 31.01.26:** Externe Daten integrieren (AP6)

---

*Version 1.0 | 2026-01-26 | FehrAdvice & Partners AG*
