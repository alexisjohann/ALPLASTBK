# SPÖ KOMMUNIKATION: Master-Index

**Single Source of Truth (SSOT) der SSOTs**
**Version:** 1.1
**Datum:** 6. Februar 2026
**Klassifikation:** INTERN

---

## 1. Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                        SPÖ KOMMUNIKATIONS-SYSTEM                        │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EBENE 0: FUNDAMENT (Authentizität)                                    │
│  ═══════════════════════════════════                                    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  BABLER_erkenntnisse.md                                           │ │
│  │  Persönliche Sprache, Learnings, Werte                            │ │
│  │  PFLEGE: Babler / engstes Team                                    │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                          │                                              │
│                          ▼ informiert                                   │
│                                                                         │
│  EBENE 1: FRAMEWORKS (Struktur)                                        │
│  ══════════════════════════════                                         │
│                                                                         │
│  ┌─────────────────────────┐     ┌─────────────────────────┐           │
│  │  FRAMEWORK_3_levels.md  │     │  FRAMEWORK_ordnung_     │           │
│  │  Strategische Levels    │     │  der_dinge.md           │           │
│  │  (Thema→Debatte→Land)   │     │  Operative 9 Akte       │           │
│  │                         │     │  (GEFÜHL→...→JETZT)     │           │
│  │  PFLEGE: Strategieteam  │     │  PFLEGE: Strategieteam  │           │
│  └─────────────────────────┘     └─────────────────────────┘           │
│                          │                                              │
│                          ▼ angewendet auf                              │
│                                                                         │
│  EBENE 2: STRATEGIE (Gesamtbild)                                       │
│  ═══════════════════════════════                                        │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  spo_strategiebriefing_parteitag_2026.md                          │ │
│  │  Gesamtstrategie für Regierungsperiode                            │ │
│  │  PFLEGE: Strategieteam + Parteiführung                            │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                          │                                              │
│                          ▼ konkretisiert in                            │
│                                                                         │
│  EBENE 3: THEMEN (Konkret)                                             │
│  ═════════════════════════                                              │
│                                                                         │
│  ┌─────────────────────────┐     ┌─────────────────────────┐           │
│  │  wordings/WORDING_*.md  │     │  wordings/BRIEFING_*.md │           │
│  │  Themenspezifische      │────►│  Operative Briefings    │           │
│  │  Positionen             │     │  für Kommunikationsteam │           │
│  │                         │     │                         │           │
│  │  PFLEGE: Strategieteam  │     │  PFLEGE: Strategieteam  │           │
│  └─────────────────────────┘     └─────────────────────────┘           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. SSOT-Register

| SSOT-ID | Dokument | Autorität für | Pfad |
|:--------|:---------|:--------------|:-----|
| **SSOT-0** | Dieser Index | Gesamtarchitektur | `SPO_KOMMUNIKATION_INDEX.md` |
| **SSOT-1** | Babler Erkenntnisse | Persönliche Sprache, Learnings | `frameworks/BABLER_erkenntnisse.md` |
| **SSOT-2** | 3-Level-Framework | Strategische Kommunikationsebenen | `frameworks/FRAMEWORK_3_levels.md` |
| **SSOT-3** | 9-Akt-Framework | Operative Redestruktur | `templates/.../FRAMEWORK_ordnung_der_dinge.md` |
| **SSOT-4** | Strategiebriefing | Gesamtstrategie Regierung | `spo_strategiebriefing_parteitag_2026.md` |
| **SSOT-5** | Wordings | Themenspezifische Positionen | `wordings/WORDING_*.md` |
| **SSOT-6** | Briefings | Operative Umsetzung | `wordings/BRIEFING_*.md` |
| **SSOT-7** | Taktik-Template | Standardisierte Ableitung | `templates/TEMPLATE_taktische_ableitung.md` |
| **SSOT-8** | Workflow | Prozess strategische Frage | `workflows/WORKFLOW_strategische_frage.md` |
| **SSOT-9** | Infografik-Workflow | NotebookLM Infografiken (Design, QA, Presets) | `workflows/WORKFLOW_infographic.yaml` |

### Hierarchie-Regel

Bei Widersprüchen gilt die höhere Ebene:

```
SSOT-1 (Babler) > SSOT-2/3 (Frameworks) > SSOT-4 (Strategie) > SSOT-5/6 (Themen)
```

**Beispiel:** Wenn ein Wording einen Satz enthält, der nicht zu Bablers Sprach-DNA passt (SSOT-1), muss das Wording angepasst werden.

---

## 3. Pflege-Matrix

| Dokument | Wer pflegt? | Wann aktualisieren? | Review-Zyklus |
|:---------|:------------|:--------------------|:--------------|
| **BABLER_erkenntnisse.md** | Babler / engstes Team | Nach jedem wichtigen Auftritt | Laufend |
| **FRAMEWORK_3_levels.md** | Strategieteam | Bei grundlegenden Änderungen | Quartalsweise |
| **FRAMEWORK_ordnung_der_dinge.md** | Strategieteam | Bei grundlegenden Änderungen | Quartalsweise |
| **Strategiebriefing** | Strategieteam + Parteiführung | Bei strategischen Weichenstellungen | Monatlich |
| **WORDING_*.md** | Strategieteam | Bei neuem Thema / neuer Lage | Nach Bedarf |
| **BRIEFING_*.md** | Strategieteam | Vor jedem grossen Auftritt | Nach Bedarf |
| **Dieser Index** | Strategieteam | Bei Architektur-Änderungen | Quartalsweise |

---

## 4. Workflow: Neues Thema aufbereiten

### Schritt-für-Schritt

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WORKFLOW: NEUES THEMA AUFBEREITEN                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: Fundament prüfen                                           │
│  ───────────────────────────                                            │
│  → Passt das Thema zu Bablers Werten? (SSOT-1)                         │
│  → Gibt es relevante persönliche Erfahrungen?                          │
│  → Welche Sprach-DNA-Elemente verwenden?                               │
│                                                                         │
│  SCHRITT 2: 3 Levels ausfüllen                                         │
│  ─────────────────────────────                                          │
│  → Level 1: Zahlen, Fakten, Massnahmen (Policy)                        │
│  → Level 2: Frame, Gegner-Position, Cross-Party (Kommunikation)        │
│  → Level 3: Geschichte, Identität, Geopolitik (Kreisky-Ebene)          │
│  → Template verwenden aus FRAMEWORK_3_levels.md                        │
│                                                                         │
│  SCHRITT 3: WORDING erstellen                                          │
│  ────────────────────────────                                           │
│  → Vollständige themenspezifische Positionierung                       │
│  → Alle Szenarien durchspielen                                          │
│  → Dateiname: WORDING_babler_[thema]_[aspekt].md                       │
│                                                                         │
│  SCHRITT 4: BRIEFING ableiten                                          │
│  ────────────────────────────                                           │
│  → Operatives Dokument für Kommunikationsteam                          │
│  → 9-Akt-Struktur anwenden (FRAMEWORK_ordnung_der_dinge.md)            │
│  → Quick-Reference Cards erstellen                                      │
│  → Dateiname: BRIEFING_babler_[thema]_operativ.md                      │
│                                                                         │
│  SCHRITT 5: Interview-Simulation                                       │
│  ───────────────────────────────                                        │
│  → Härtesten Interviewer simulieren (Wolf, Thür)                       │
│  → Alle 9 Akte durchspielen                                             │
│  → Simulation ins Briefing integrieren                                  │
│                                                                         │
│  SCHRITT 6: Review                                                      │
│  ─────────────                                                          │
│  → Konsistenz mit SSOT-1 (Babler) prüfen                               │
│  → Konsistenz mit SSOT-4 (Gesamtstrategie) prüfen                      │
│  → Bei Widersprüchen: höhere Ebene gilt                                │
│                                                                         │
│  SCHRITT 7: Infografik (optional, SSOT-9)                               │
│  ────────────────────────────────────────                                │
│  → /infographic --preset spo --thema [THEMA]                            │
│  → 3 Formate: Landscape (Parteitag), Square (Social), Portrait (Mobile)│
│  → 3-Iterationen QA-Loop → Freigabe bei Score ≥ 8.5                   │
│  → Siehe: workflows/WORKFLOW_infographic.yaml                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Checkliste für neues Thema

```
☐ SSOT-1 geprüft: Passt zu Bablers Sprache/Werten
☐ Level 1 ausgefüllt: Zahlen, Fakten, Massnahmen
☐ Level 2 ausgefüllt: Frame, Gegner, Cross-Party
☐ Level 3 ausgefüllt: Geschichte, Identität
☐ WORDING erstellt: wordings/WORDING_babler_[thema].md
☐ BRIEFING erstellt: wordings/BRIEFING_babler_[thema]_operativ.md
☐ Interview-Simulation durchgeführt
☐ Quick-Reference Cards erstellt
☐ Review auf Konsistenz mit Gesamtstrategie
```

---

## 5. Qualitätssicherung

### Konsistenz-Checks

| Check | Frage | Wenn NEIN → |
|:------|:------|:------------|
| **Sprach-DNA** | Verwendet das Wording Bablers authentische Sprache? | SSOT-1 konsultieren, anpassen |
| **3-Level-Struktur** | Sind alle 3 Levels abgedeckt? | SSOT-2 Template ausfüllen |
| **9-Akt-Struktur** | Folgt das Briefing den 9 Akten? | SSOT-3 anwenden |
| **Strategie-Alignment** | Passt zur Gesamtstrategie? | SSOT-4 prüfen, ggf. eskalieren |
| **Interview-Test** | Hält es einem Wolf-Interview stand? | Simulation durchführen |

### Warnzeichen (sofort beheben)

| Warnzeichen | Problem | Lösung |
|:------------|:--------|:-------|
| "Wir versuchen..." | Unverbindlich | → "Wir tun" |
| Frage am Ende | Schwächt Closer | → Statement. Punkt. |
| EMRK/Rechtslage erklären | Verliert Publikum | → Ergebnisse zuerst |
| "Aber" nach Zugeständnis | Negiert sich selbst | → Punkt. Neuer Satz. |
| Prozent-Zahlen | Weniger greifbar | → Absolute Zahlen |

---

## 6. Dokumenten-Register

### Aktuelle Dokumente

| Typ | Thema | Datei | Version | Datum |
|:----|:------|:------|:--------|:------|
| **Framework** | 3 Levels | `frameworks/FRAMEWORK_3_levels.md` | 1.0 | 2026-02-02 |
| **Framework** | 9 Akte | `templates/.../FRAMEWORK_ordnung_der_dinge.md` | 1.0 | 2026-02-01 |
| **Playbook** | Babler | `frameworks/BABLER_erkenntnisse.md` | 1.0 | 2026-02-02 |
| **Strategie** | Gesamt | `spo_strategiebriefing_parteitag_2026.md` | 3.4 | 2026-02-02 |
| **Wording** | EMRK | `wordings/WORDING_babler_emrk_position.md` | 2.0 | 2026-02-01 |
| **Wording** | Dänemark | `wordings/wording_daenemark_emrk_2026-02-01.md` | 1.0 | 2026-02-01 |
| **Briefing** | EMRK | `wordings/BRIEFING_babler_emrk_operativ.md` | 1.1 | 2026-02-02 |
| **Template** | Taktische Ableitung | `templates/TEMPLATE_taktische_ableitung.md` | 1.0 | 2026-02-02 |
| **Workflow** | Strategische Frage | `workflows/WORKFLOW_strategische_frage.md` | 1.0 | 2026-02-02 |
| **Workflow** | Infografik (NotebookLM) | `workflows/WORKFLOW_infographic.yaml` | 1.0 | 2026-02-06 |
| **Template** | Infografik Strategie (v2) | `templates/TEMPLATE_infografik_strategie.md` | 2.0 | 2026-02-06 |

### Namenskonventionen

| Typ | Format | Beispiel |
|:----|:-------|:---------|
| **Framework** | `FRAMEWORK_[name].md` | `FRAMEWORK_3_levels.md` |
| **Playbook** | `BABLER_[was].md` | `BABLER_erkenntnisse.md` |
| **Wording** | `WORDING_babler_[thema]_[aspekt].md` | `WORDING_babler_emrk_position.md` |
| **Briefing** | `BRIEFING_babler_[thema]_operativ.md` | `BRIEFING_babler_emrk_operativ.md` |
| **Infografik** | `INFOGRAFIK_[thema]_[datum].md` | `INFOGRAFIK_basis_gesundheitsversorgung_2026-02-03.md` |

---

## 7. Glossar der Konzepte

| Konzept | Definition | SSOT |
|:--------|:-----------|:-----|
| **3-Level-Framework** | Thema ordnen → Debatte ordnen → Land ordnen | SSOT-2 |
| **9-Akt-Struktur** | GEFÜHL → ALLE → HALTUNG → WEISHEIT → REGELN → BEWEIS → WERTE → GESCHICHTE → JETZT | SSOT-3 |
| **Sprach-DNA** | Bablers authentische Wörter und Redewendungen | SSOT-1 |
| **Traiskirchen-Beweis** | Persönliche Erfahrung als Glaubwürdigkeitsanker | SSOT-1 |
| **Leadership-Ownership** | "Das haben WIR erreicht" | SSOT-1 |
| **Cross-Party-Konsens** | "Unabhängig von der Partei" | SSOT-2 |
| **Kreisky-Ebene** | Staatsmann-Kommunikation (Level 3) | SSOT-2 |
| **Luftschlösser für niemals** | Punchline gegen unpraktische Vorschläge | SSOT-1 |

---

## 8. Änderungsprotokoll

| Version | Datum | Änderung | Autor |
|:--------|:------|:---------|:------|
| 1.0 | 2026-02-02 | Erstversion | Strategieteam |
| 1.1 | 2026-02-06 | SSOT-9 Infografik-Workflow hinzugefügt, Schritt 7 im Themen-Workflow | Strategieteam |

---

## 9. Kontakt

| Rolle | Verantwortung |
|:------|:--------------|
| **Strategieteam** | Frameworks, Wordings, Briefings |
| **Babler / engstes Team** | BABLER_erkenntnisse.md |
| **Kommunikationsteam (Susanne)** | Operative Umsetzung |

---

*FehrAdvice & Partners AG — VERTRAULICH*
