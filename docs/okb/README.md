---
title: "OKB - Operational Knowledge Base"
version: "1.0"
date: "2026-01-28"
author: "FehrAdvice & Partners AG"
---

# OKB - Operational Knowledge Base

> **Das Handwerkswissen von FehrAdvice**

---

## Was ist OKB?

Die **Operational Knowledge Base (OKB)** ist das System, das unser operatives Handwerkswissen erfasst, speichert und weitergibt.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   EBF FRAMEWORK                    vs.         OKB                      │
│   ─────────────────────────────────────────────────────────────────     │
│                                                                         │
│   WAS wir wissen                              WIE wir arbeiten          │
│   (Verhaltensokonomie)                        (Produktion)              │
│                                                                         │
│   Theorien, Modelle, Cases                    Prozesse, Fehler, Fixes   │
│                                                                         │
│   Inhaltliches Wissen                         Operatives Wissen         │
│                                                                         │
│   "Was ist Loss Aversion?"                    "Wie kompiliere ich       │
│                                                fehlerfrei ein PDF?"     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Warum OKB?

| Problem ohne OKB | Losung mit OKB |
|:-----------------|:---------------|
| Gleiche Fehler wiederholen | Fehler werden nur EINMAL gemacht |
| Wissen in Kopfen verschwindet | Tacit Knowledge wird explizit |
| Neue Mitarbeiter machen alte Fehler | Onboarding aus der Geschichte |
| Qualitat schwankt | Qualitat verbessert sich stetig |
| Zeit geht verloren | 70+ min Ersparnis pro Projekt |

---

## OKB Architektur

```
docs/okb/
├── README.md                     <- Du bist hier
├── OKB-001-document-production.md   <- Dokumentenproduktion
├── OKB-002-[next].md                <- Nachstes Thema
└── ...
```

### Naming Convention

```
OKB-[NNN]-[thema].md

NNN = Laufende Nummer (001, 002, ...)
thema = Kebab-case Beschreibung
```

---

## OKB Datenbanken

| ID | Name | Thema | Workflow | Learnings |
|:---|:-----|:------|:---------|:----------|
| **OKB-001** | Document Production | Dokumente erstellen | `/doc` | 6 (L1-L6) |
| **OKB-002** | Design Handoff | Übergabe an Google Workspace | - | 0 |
| OKB-003 | *reserviert* | Client CI/CD Setup | `/client-ci` | - |
| OKB-004 | *reserviert* | Data Analysis | `/data` | - |

---

## Learning Loop

```
┌──────────────────┐
│  PROJEKT START   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  OKB LESEN       │◄────────────────┐
│  (Learnings)     │                 │
└────────┬─────────┘                 │
         │                           │
         ▼                           │
┌──────────────────┐                 │
│  WORKFLOW        │                 │
│  AUSFUHREN       │                 │
└────────┬─────────┘                 │
         │                           │
         ▼                           │
┌──────────────────┐                 │
│  NEUES LEARNING? │                 │
│  [ ] JA  [ ] NEIN│                 │
└────────┬─────────┘                 │
         │                           │
         ▼                           │
┌──────────────────┐                 │
│  OKB             │                 │
│  AKTUALISIEREN   │─────────────────┘
└──────────────────┘
```

---

## OKB Entry Format

Jedes Learning in einer OKB-Datenbank folgt diesem Format:

```markdown
| Datum | Projekt | Learning | Kategorie | Zeitersparnis |
|:------|:--------|:---------|:----------|:--------------|
| YYYY-MM-DD | [PROJEKT] | [WAS GELERNT] | [KAT] | [MIN] min |
```

### Kategorien

| Kategorie | Beschreibung |
|:----------|:-------------|
| FORMAT | Dateiformat, Struktur |
| ENCODING | Unicode, Zeichensatze |
| LAYOUT | Tabellen, Grafiken, Abstande |
| PACKAGES | LaTeX Pakete, Dependencies |
| PROCESS | Workflow, Reihenfolge |
| TOOLS | Software, CLI Commands |

---

## Regeln

### R1: Jeder Fehler wird dokumentiert

```
WENN Fehler passiert
UND Fehler war vermeidbar
DANN Learning in OKB eintragen
```

### R2: Learnings werden VOR Projektstart gelesen

```
WENN Projekt startet
DANN zuerst relevante OKB lesen
DANN erst arbeiten
```

### R3: OKB ist Teil des Workflows

```
Learnings lesen  → Im Workflow integriert (Schritt 0)
Learning erfassen → Im Workflow integriert (letzter Schritt)
```

### R4: Quantifizieren wenn moglich

```
SCHLECHT: "Unicode vermeiden"
GUT:      "Unicode vermeiden → spart 10+ min pro Dokument"
```

---

## Quick Start

### Neues Learning erfassen

1. Offne die relevante OKB-Datei
2. Fuge einen Eintrag in die Lessons Learned Registry hinzu
3. Aktualisiere die Metriken
4. Commit mit `feat(OKB): Add learning [BESCHREIBUNG]`

### Neue OKB-Datenbank erstellen

1. Erstelle `docs/okb/OKB-[NNN]-[thema].md`
2. Kopiere Struktur von OKB-001
3. Registriere in dieser README
4. Erstelle zugehorigen Workflow in `.claude/commands/`

---

## Metriken (Gesamt)

| Metrik | Wert | Stand |
|:-------|:-----|:------|
| OKB Datenbanken | 1 | 2026-01-28 |
| Learnings gesamt | 6 | 2026-01-28 |
| Geschatzte Zeitersparnis | 75+ min/Projekt | 2026-01-28 |

---

*OKB - Weil Fehler nur einmal gemacht werden mussen.*
