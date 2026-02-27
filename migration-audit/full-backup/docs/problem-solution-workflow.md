# Problem-to-Solution Workflow (PSW)

> Ein strukturierter Learning Loop für systematische Problemlösung im EBF Framework.

**Version:** 1.0
**Date:** January 2026
**Status:** Active
**Derived from:** Data Consistency Validation Implementation (2026-01-26)

---

## Overview

Dieser Workflow dokumentiert den systematischen Prozess von der Problem-Identifikation bis zur vollständigen Lösung mit Quality Assurance und Learning Loop.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROBLEM-TO-SOLUTION WORKFLOW (PSW)                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌───────┐ │
│  │ PHASE 1 │───►│ PHASE 2 │───►│ PHASE 3 │───►│ PHASE 4 │───►│PHASE 5│ │
│  │ PROBLEM │    │ ANALYSE │    │ DESIGN  │    │IMPLEMENT│    │QUALITY│ │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └───────┘ │
│       │                                                           │     │
│       │              ┌─────────────────────────────────┐          │     │
│       └──────────────│         PHASE 6: LEARN         │◄─────────┘     │
│                      │     (Feedback → Improvement)    │                │
│                      └─────────────────────────────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: PROBLEM (Problemstellung verstehen)

### Schritte

| # | Schritt | Output | Tool/Methode |
|---|---------|--------|--------------|
| 1.1 | Problem in eigenen Worten formulieren | Problem Statement | User-Frage analysieren |
| 1.2 | Kontext identifizieren | Kontext-Dimensionen (Ψ) | BCM2, context-dimensions.yaml |
| 1.3 | Scope abgrenzen | In-Scope / Out-of-Scope | Stakeholder-Input |
| 1.4 | Erfolgskriterien definieren | Messbare Ziele | SMART-Kriterien |

### Beispiel: Data Consistency

```
Problem Statement:
"Wie stellen wir sicher, dass Daten über mehrere EBF-Quellen hinweg
konsistent, korrekt und widerspruchsfrei verwendet werden?"

Kontext: Ψ_I (institutionell: Git, YAML), Ψ_M (technisch: Pre-Commit)
In-Scope: Referenzen, Parameter, Kontext-Hierarchie
Out-of-Scope: Semantische Validierung, Infrastruktur
Erfolgskriterien: Score ≥ 85%, automatisiert, dokumentiert
```

### Checkliste Phase 1

```
☐ Problem klar formuliert (1 Satz)
☐ Kontext-Dimensionen identifiziert
☐ In-Scope / Out-of-Scope definiert
☐ Messbare Erfolgskriterien (≥3)
```

---

## Phase 2: ANALYSE (Ist-Zustand verstehen)

### Schritte

| # | Schritt | Output | Tool/Methode |
|---|---------|--------|--------------|
| 2.1 | Bestehendes erkunden | Gap-Analyse | Task/Explore Agent |
| 2.2 | Ähnliche Lösungen suchen | Referenz-Patterns | Grep, case-registry |
| 2.3 | Stakeholder identifizieren | Stakeholder-Map | Interview, Docs |
| 2.4 | Constraints dokumentieren | Constraint-Liste | Technical Review |

### Beispiel: Data Consistency

```
Gap-Analyse:
├── 13 Validierungsskripte existieren (Template, Chapter, etc.)
├── ABER: Keine Cross-Database-Validierung
├── ABER: Keine Parameter-Drift-Erkennung
└── ABER: Keine Kontext-Hierarchie-Prüfung

Referenz-Patterns:
├── EIP (Evidence Integration Pipeline) → Konzept-Validierung
├── EXC (Exclusion Principle) → Formel-Validierung
└── Template Compliance → Struktur-Validierung

Constraints:
├── Python 3.x (bestehende Skripte)
├── YAML-Format (bestehende Datenbanken)
└── Pre-Commit Hook (bestehende Automatisierung)
```

### Checkliste Phase 2

```
☐ Bestehende Lösungen analysiert
☐ Gaps identifiziert (≥3)
☐ Referenz-Patterns gefunden
☐ Constraints dokumentiert
```

---

## Phase 3: DESIGN (Lösung entwerfen)

### Schritte

| # | Schritt | Output | Tool/Methode |
|---|---------|--------|--------------|
| 3.1 | Architektur skizzieren | Architektur-Diagramm | ASCII/Mermaid |
| 3.2 | Komponenten definieren | Komponenten-Liste | Modularisierung |
| 3.3 | Schnittstellen festlegen | Interface-Spec | API-Design |
| 3.4 | Axiome/Regeln formalisieren | Axiom-System | Formale Methoden |

### Beispiel: Data Consistency

```
Architektur: 3-Pillar Model
├── Pillar 1: Referential Integrity (DCV-1, DCV-2)
├── Pillar 2: Parameter Consistency (DCV-3, DCV-4)
└── Pillar 3: Context Consistency (DCV-5, DCV-6)

Komponenten:
├── validate_referential_integrity.py
├── validate_parameter_consistency.py
├── validate_context_consistency.py
└── pre-commit.sh Integration

Axiome:
├── DCV-1: Existenz-Axiom (Referenzen müssen existieren)
├── DCV-2: Konsistenz-Axiom (Referenzen müssen konsistent sein)
├── DCV-3: Bounds-Axiom (Parameter in definierten Grenzen)
├── DCV-4: Drift-Axiom (Abweichung < 20%)
├── DCV-5: Hierarchie-Axiom (MACRO→MESO→MICRO)
└── DCV-6: Kohärenz-Axiom (Modell ↔ Theorie)
```

### Checkliste Phase 3

```
☐ Architektur-Diagramm erstellt
☐ Komponenten modular definiert
☐ Schnittstellen spezifiziert
☐ Axiome/Regeln formalisiert
```

---

## Phase 4: IMPLEMENT (Lösung umsetzen)

### Schritte

| # | Schritt | Output | Tool/Methode |
|---|---------|--------|--------------|
| 4.1 | Kern-Implementierung | Funktionierender Code | Python/Bash |
| 4.2 | Integration | Hook/Workflow | Pre-Commit, CI/CD |
| 4.3 | Dokumentation (Technical) | Markdown Docs | docs/workflows/ |
| 4.4 | Dokumentation (Formal) | LaTeX Appendix | appendices/ |

### Beispiel: Data Consistency

```
4.1 Kern-Implementierung:
    ├── scripts/validate_referential_integrity.py (250 LOC)
    ├── scripts/validate_parameter_consistency.py (200 LOC)
    └── scripts/validate_context_consistency.py (180 LOC)

4.2 Integration:
    └── .claude/hooks/pre-commit.sh (erweitert)

4.3 Dokumentation (Technical):
    └── docs/workflows/data-consistency-validation.md

4.4 Dokumentation (Formal):
    └── appendices/VC_METHOD-VALIDATE_data_consistency.tex
```

### Checkliste Phase 4

```
☐ Code implementiert und getestet
☐ In bestehende Workflows integriert
☐ Markdown-Dokumentation erstellt
☐ LaTeX-Appendix erstellt (wenn formale Axiome)
```

---

## Phase 5: QUALITY (Qualität sichern)

### Schritte

| # | Schritt | Output | Tool/Methode |
|---|---------|--------|--------------|
| 5.1 | Compliance prüfen | Score ≥ 85% | check_template_compliance.py |
| 5.2 | Cross-References | Bidirektionale Links | Appendix X-Refs |
| 5.3 | Scope formalisieren | Z/IS/OS/L Struktur | Scope Box |
| 5.4 | SSOT aktualisieren | YAML-Updates | chapter-appendix-mapping.yaml |

### Beispiel: Data Consistency

```
5.1 Compliance:
    └── VC Appendix: 77.5% → 100% (nach Fixes)

5.2 Cross-References:
    ├── VC → BBB, V, FRM, AN (outgoing)
    ├── BBB → VC (incoming)
    ├── CAL → VC (incoming)
    └── FRM → VC (incoming)

5.3 Scope formalisiert:
    ├── Z1-Z4: Erfolgskriterien
    ├── IS1-IS4: In-Scope mit Axiom-Referenzen
    ├── OS1-OS4: Out-of-Scope mit Delegation
    └── L1-L5: Lieferobjekte mit Section-Referenzen

5.4 SSOT:
    └── chapter-appendix-mapping.yaml: VC-Eintrag mit related_appendices
```

### Checkliste Phase 5

```
☐ Template Compliance ≥ 85%
☐ Bidirektionale Cross-References
☐ Scope Box formalisiert (Z/IS/OS/L)
☐ SSOT (YAML) aktualisiert
☐ Alle Commits gepusht
```

---

## Phase 6: LEARN (Lernen und verbessern)

### Schritte

| # | Schritt | Output | Tool/Methode |
|---|---------|--------|--------------|
| 6.1 | Prozess dokumentieren | Workflow-Dokument | docs/workflows/ |
| 6.2 | Lessons Learned | LL-Eintrag | quality/lessons_learned.md |
| 6.3 | CLAUDE.md aktualisieren | Workflow-Integration | CLAUDE.md |
| 6.4 | Metriken tracken | Score-History | data/quality/ |

### Beispiel: Data Consistency

```
6.1 Prozess dokumentieren:
    └── docs/workflows/problem-solution-workflow.md (dieses Dokument)

6.2 Lessons Learned:
    ├── LL-1: Scope Box braucht "Lieferobjekte" für Compliance
    ├── LL-2: Cross-References müssen bidirektional sein
    └── LL-3: YAML-Mapping braucht related_appendices Feld

6.3 CLAUDE.md:
    └── Neuer Workflow "Problem-to-Solution" dokumentiert

6.4 Metriken:
    └── data/quality/validation-history.yaml (TODO)
```

### Checkliste Phase 6

```
☐ Workflow-Dokument erstellt
☐ Lessons Learned dokumentiert
☐ CLAUDE.md aktualisiert
☐ Metriken-Tracking eingerichtet
```

---

## Learning Loop Integration

### Feedback-Schleifen

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FEEDBACK LOOPS                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LOOP 1: Immediate (Pre-Commit)                                         │
│  ┌─────────┐                                                            │
│  │ Commit  │───► Validation ───► Score < 85%? ───► Fix ───► Commit      │
│  └─────────┘                                                            │
│                                                                         │
│  LOOP 2: Session (Workflow-Ende)                                        │
│  ┌─────────┐                                                            │
│  │ Phase 5 │───► Quality Check ───► Gaps? ───► Phase 3-4 ───► Phase 5   │
│  └─────────┘                                                            │
│                                                                         │
│  LOOP 3: Strategic (Quartalsweise)                                      │
│  ┌─────────┐                                                            │
│  │ Review  │───► Score-Trend ───► Degradation? ───► Root Cause ───► Fix │
│  └─────────┘                                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Wann diesen Workflow verwenden?

| Trigger | Beispiel | Einstiegspunkt |
|---------|----------|----------------|
| Neue Anforderung | "Wie validieren wir X?" | Phase 1 |
| Gap identifiziert | "Es fehlt Y" | Phase 2 |
| Lösung bekannt | "Wir brauchen Z" | Phase 3 |
| Bug gefunden | "Script X funktioniert nicht" | Phase 4 |
| Compliance-Fehler | "Score < 85%" | Phase 5 |

---

## Quick Reference

### Phasen-Übersicht

| Phase | Frage | Hauptoutput |
|-------|-------|-------------|
| **1. PROBLEM** | Was ist das Problem? | Problem Statement + Erfolgskriterien |
| **2. ANALYSE** | Was existiert bereits? | Gap-Analyse + Constraints |
| **3. DESIGN** | Wie lösen wir es? | Architektur + Axiome |
| **4. IMPLEMENT** | Wie setzen wir es um? | Code + Docs + Appendix |
| **5. QUALITY** | Ist es gut genug? | Compliance + X-Refs + SSOT |
| **6. LEARN** | Was haben wir gelernt? | Workflow-Doc + LL + CLAUDE.md |

### Minimal Viable Workflow

Für kleinere Probleme (< 1h):

```
1. Problem → 1 Satz
2. Analyse → Grep/Read bestehender Code
3. Design  → Skizze im Kopf
4. Implement → Code + Commit
5. Quality → Compliance-Check
6. Learn   → (Optional) LL-Eintrag
```

### Full Workflow

Für größere Probleme (> 1h):

```
1. Problem → Problem Statement + Z1-Z4
2. Analyse → Task/Explore Agent + Gap-Analyse
3. Design  → Architektur + DCV-1 bis DCV-n Axiome
4. Implement → Scripts + Hook + MD + LaTeX
5. Quality → 100% Compliance + Bidirektionale X-Refs
6. Learn   → Workflow-Doc + LL + CLAUDE.md + Metriken
```

---

## Related Documentation

- [Data Consistency Validation](data-consistency-validation.md) - Beispiel-Implementation
- [Evidence Integration Pipeline](evidence-integration-pipeline.md) - Konzept-Validierung
- [Appendix VC](../../appendices/VC_METHOD-VALIDATE_data_consistency.tex) - Formale Dokumentation

---

*Version 1.0 | January 2026 | Derived from DCV Implementation*
