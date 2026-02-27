# Reverse Engineering Workflow (REW)

**Version:** 1.0
**Erstellt:** 2026-02-03
**Kategorie:** METHOD
**Zweck:** Kausalitätsprüfung + EBF-Compliance-Validierung

---

## 1. Übersicht

Der **Reverse Engineering Workflow (REW)** ist eine systematische Methode zur Rückverfolgung von Strategie-Dokumenten zu ihren wissenschaftlichen Quellen. Er validiert die **Kausalkette** und prüft die **EBF-Compliance**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  REVERSE ENGINEERING WORKFLOW (REW)                                     │
│  Zweck: Kausalitätsprüfung + EBF-Compliance-Validierung                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  RICHTUNG: OUTPUT → INPUT (rückwärts)                                  │
│                                                                         │
│  ┌─────────────┐                                                       │
│  │ DOKUMENTE   │  ← "Was steht im Deliverable?"                        │
│  └──────┬──────┘                                                       │
│         │ REW-1: Welche Kommunikations-Elemente?                       │
│         ▼                                                              │
│  ┌─────────────┐                                                       │
│  │ OPERATIONA- │  ← "Welche K/T/S-Entscheidungen?"                     │
│  │ LISIERUNG   │     (Kommunikation, Taktik, Strategie)                │
│  └──────┬──────┘                                                       │
│         │ REW-2: Welches Axiom rechtfertigt das?                       │
│         ▼                                                              │
│  ┌─────────────┐                                                       │
│  │ AXIOME      │  ← "Welche formale Regel?"                            │
│  │             │     (Kunden-spezifische Axiom-Datenbank)              │
│  └──────┬──────┘                                                       │
│         │ REW-3: Welches Belief stützt das Axiom?                      │
│         ▼                                                              │
│  ┌─────────────┐                                                       │
│  │ BELIEFS     │  ← "Welche fundamentale Annahme?"                     │
│  │             │     (Projekt-spezifische Beliefs)                     │
│  └──────┬──────┘                                                       │
│         │ REW-4: Welche Wissenschaft belegt das?                       │
│         ▼                                                              │
│  ┌─────────────┐                                                       │
│  │ THEORIEN    │  ← "Welche peer-reviewed Evidenz?"                    │
│  │ (CAT-XX)    │     (data/theory-catalog.yaml)                        │
│  └─────────────┘                                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Die 5 Ebenen

### Ebene 0: Dokumente (Output)

Die finalen Deliverables für den Kunden.

| Element | Beschreibung | Beispiel |
|---------|--------------|----------|
| **Deliverable** | Kunden-Strategie-Dokument | EMRK_STRATEGIE_KOMPLETT |
| **Taktik** | Operative Umsetzungsanleitung | TAKTIK v3.1 |
| **Wording** | Kommunikations-Elemente | WORDING v5.1 |
| **Briefing** | Schnellreferenz | BRIEFING v4.1 |

### Ebene 1: Operationalisierung

Die konkreten Entscheidungen, die zu den Dokumenten führen.

| Kategorie | Code | Beschreibung |
|-----------|------|--------------|
| **Kommunikation** | K1-Kn | Konkrete Botschaften, Formulierungen |
| **Taktik** | T1-Tn | Operative Entscheidungen |
| **Strategie** | S1-Sn | Strategische Richtungsentscheidungen |

### Ebene 2: Axiome

Formalisierte Entscheidungsregeln, projekt-/kundenspezifisch.

| Element | Beschreibung | Quelle |
|---------|--------------|--------|
| **Axiom-ID** | Eindeutige Kennung | K1, K2, ... K10 |
| **Formale Notation** | Mathematische Definition | AXIOME.yaml |
| **Entscheidungsfunktion** | D(x) → {ERLAUBT, VERBOTEN, PRÜFEN} | AXIOME.yaml |
| **Validierungs-Checkliste** | CHK-1 bis CHK-n | AXIOME.yaml |

### Ebene 3: Beliefs

Fundamentale Annahmen, die den Axiomen zugrunde liegen.

| Element | Beschreibung | Beispiel |
|---------|--------------|----------|
| **Belief-ID** | B1, B2, ... Bn | B1: Identität dominiert Rationalität |
| **Quelle** | Wissenschaftliche Theorien | MS-IB-001, MS-PP-001 |
| **Implikation** | Was folgt daraus? | → Bei politischen Entscheidungen: U_IDN >> U_IND |

### Ebene 4: Theorien (Wissenschaft)

Peer-reviewed wissenschaftliche Evidenz.

| Element | Quelle | Beschreibung |
|---------|--------|--------------|
| **Kategorie** | CAT-XX | Theory Catalog Kategorie |
| **Theorie-ID** | MS-XX-NNN | Spezifische Theorie |
| **Autoren** | - | Wissenschaftler |
| **Jahr** | - | Publikationsjahr |
| **EBF-Restriktionen** | - | Formale Parameter |
| **BibTeX-Keys** | - | Referenz in bcm_master.bib |

---

## 3. Die 4 REW-Prüfungen

### REW-1: Dokument → Operationalisierung

**Frage:** Hat jedes Kommunikations-Element eine dokumentierte Entscheidung?

```
Für jedes Element E in Dokument:
    ∃ K/T/S-Entscheidung, die E rechtfertigt?

    JA  → ✅ Weiter zu REW-2
    NEIN → ❌ LÜCKE: Element ohne Operationalisierung
```

**Compliance-Kriterium:** 100% Zuordnung

### REW-2: Operationalisierung → Axiom

**Frage:** Hat jede Entscheidung ein Axiom als Rechtfertigung?

```
Für jede Entscheidung D (K/T/S):
    ∃ Axiom A, sodass D aus A folgt?

    JA  → ✅ Weiter zu REW-3
    NEIN → ❌ LÜCKE: Entscheidung ohne Axiom-Basis
```

**Compliance-Kriterium:** 100% Axiom-Abdeckung

### REW-3: Axiom → Belief

**Frage:** Hat jedes Axiom ein Belief als Fundierung?

```
Für jedes Axiom A:
    ∃ Belief B, sodass A aus B abgeleitet ist?

    JA  → ✅ Weiter zu REW-4
    NEIN → ⚠️ WARNUNG: Axiom ohne Belief-Fundierung
           (Kann akzeptabel sein bei rein operativen Axiomen)
```

**Compliance-Kriterium:** Belief-Fundierung dokumentiert

### REW-4: Belief → Theorie

**Frage:** Hat jedes Belief wissenschaftliche Evidenz?

```
Für jedes Belief B:
    ∃ Theorie T in theory-catalog.yaml, die B stützt?

    JA  → ✅ EBF-COMPLIANT
    NEIN → ❌ KRITISCH: Belief ohne wissenschaftliche Basis
```

**Compliance-Kriterium:** Theorie-Nachweis (CAT-XX, MS-XX-NNN)

---

## 4. REW vs. FEW: Die zwei Richtungen

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FORWARD ENGINEERING (FEW)        REVERSE ENGINEERING (REW)            │
│  ─────────────────────────        ─────────────────────────            │
│                                                                         │
│  Theorien                         Dokumente                             │
│      ↓                                ↓                                 │
│  Beliefs                          Operationalisierung                   │
│      ↓                                ↓                                 │
│  Axiome                           Axiome                                │
│      ↓                                ↓                                 │
│  Operationalisierung              Beliefs                               │
│      ↓                                ↓                                 │
│  Dokumente                        Theorien                              │
│                                                                         │
│  DESIGN-PHASE                     VALIDIERUNGS-PHASE                   │
│  "Wie SOLL es sein?"              "Ist es EBF-compliant?"              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| Workflow | Phase | Zweck | Wann verwenden? |
|----------|-------|-------|-----------------|
| **FEW** | Design | Strategie aus Theorie ableiten | Neues Projekt starten |
| **REW** | Validierung | Kausalkette prüfen | Bestehendes Dokument auditieren |
| **FEW + REW** | Iteration | Lücken finden und schliessen | Kontinuierliche Verbesserung |

---

## 5. REW-Output: Quellcode-Architektur

Das Ergebnis eines vollständigen REW ist ein **Quellcode-Architektur-Dokument**:

```
QUELLCODE_ARCHITEKTUR_{kunde}_{projekt}_{datum}.md

Inhalt:
├── 1. Die Quellcode-Hierarchie (Diagramm)
├── 2. Belief → Axiom → Operationalisierung Mapping
│   ├── 2.1 Belief B1: [Name]
│   │   ├── Theorie-Quelle
│   │   ├── Axiome
│   │   ├── Strategie-Entscheidungen
│   │   ├── Taktik-Entscheidungen
│   │   └── Kommunikations-Elemente
│   ├── 2.2 Belief B2: [Name]
│   │   └── ...
│   └── ...
├── 3. Level-Architektur (falls vorhanden)
├── 4. Dokument-zu-Quelle Mapping (Tabelle)
├── 5. Validierungs-Checkliste
└── 6. Referenzen
```

---

## 6. REW-Checkliste

### Vor REW starten:

```
☐ Alle Dokumente identifiziert
☐ Axiom-Datenbank geladen
☐ Theory-Catalog verfügbar
☐ Belief-Liste erstellt (oder während REW erstellen)
```

### Während REW:

```
☐ REW-1: Alle Dokument-Elemente → Operationalisierung zugeordnet
☐ REW-2: Alle Entscheidungen → Axiome zugeordnet
☐ REW-3: Alle Axiome → Beliefs zugeordnet
☐ REW-4: Alle Beliefs → Theorien zugeordnet
```

### Nach REW:

```
☐ Quellcode-Architektur-Dokument erstellt
☐ Lücken identifiziert und dokumentiert
☐ Compliance-Status festgestellt
☐ Nächste Schritte definiert (falls Lücken)
```

---

## 7. REW-Compliance-Levels

| Level | Beschreibung | Kriterium |
|-------|--------------|-----------|
| **REW-0** | Nicht geprüft | Kein REW durchgeführt |
| **REW-1** | Teilweise | REW-1 + REW-2 bestanden |
| **REW-2** | Substantiell | REW-1 bis REW-3 bestanden |
| **REW-3** | Vollständig | Alle 4 REW-Prüfungen bestanden |

**Mindest-Compliance für EBF-Projekte:** REW-2

**Empfohlen für wissenschaftliche Validierung:** REW-3

---

## 8. Beispiel: SPÖ EMRK-Projekt

### REW-Ergebnis:

| Prüfung | Status | Details |
|---------|--------|---------|
| REW-1 | ✅ | 4 Dokumente → K1-K5, T1-T4, S1-S4 |
| REW-2 | ✅ | Alle K/T/S → K1-K10 Axiome |
| REW-3 | ✅ | K1-K10 → B1-B5 Beliefs |
| REW-4 | ✅ | B1-B5 → CAT-05, CAT-21 Theorien |

**Compliance-Level:** REW-3 (Vollständig)

### Identifizierte Kausalketten:

```
MS-IB-001 (Identity Economics)
    → B1 (Identität dominiert Rationalität)
    → K1 (Kickl-Differenzierung)
    → S3 (USP = Staatsmännisch)
    → T1 (Tonalitäts-Transformation)
    → K4 ("Nur SPÖ kann Ordnung UND Rechtsstaat")
```

---

## 9. Integration mit anderen Workflows

| Workflow | Beziehung zu REW |
|----------|------------------|
| **EIP (Evidence Integration Pipeline)** | REW-4 nutzt EIP für Theorie-Validierung |
| **PSW (Problem-to-Solution Workflow)** | REW ist Teil von PSW Phase 5 (Quality) |
| **FEW (Forward Engineering Workflow)** | Gegenstück zu REW (Design vs. Validierung) |

---

## 10. SSOT-Referenzen

| Quelle | Pfad |
|--------|------|
| Theory Catalog | `data/theory-catalog.yaml` |
| Model Registry | `data/model-registry.yaml` |
| Parameter Registry | `data/parameter-registry.yaml` |
| Kunden-Axiome | `data/customers/{kunde}/strategie/AXIOME_*.yaml` |

---

*Erstellt: 2026-02-03 | EBF Workflow | Version 1.0*
