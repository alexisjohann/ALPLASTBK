# {{TITLE}}

**SLA-ID:** {{SLA_ID}}
**Modus:** {{MODE}} (RAPID | STANDARD | SYSTEMATIC)
**Datum:** {{DATE}}
**Session:** {{SESSION_ID}}
**Status:** {{STATUS}}

---

## 1. Executive Summary

**Forschungsfrage:** {{PRIMARY_QUESTION}}

**Methodik:**
- {{N0}} Papers identifiziert → {{N1}} inkludiert ({{MODE}}-Modus)
- Quellen: bcm_master.bib ({{N_INTERNAL}}), WebSearch ({{N_EXTERNAL}}), Snowballing ({{N_SNOW}})
- Screening: 5-Kriterien-Score (REL, MET, TIR, CTX, AKT)

**Schlüsselbefunde:**
1. {{FINDING_1}}
2. {{FINDING_2}}
3. {{FINDING_3}}

**Konfidenz:** {{OVERALL_CONFIDENCE}} (HOCH | MITTEL | NIEDRIG)

**PRO/CONTRA Bilanz:** {{WEIGHTED_VERDICT}}

---

## 2. Einleitung & Forschungsfrage

### 2.1 Hintergrund

{{BACKGROUND}}

### 2.2 Forschungsfrage ({{FORMAT}}-Format)

{{#if PICO}}
| Element | Beschreibung |
|---------|-------------|
| **P** (Population) | {{POPULATION}} |
| **I** (Intervention) | {{INTERVENTION}} |
| **C** (Comparison) | {{COMPARISON}} |
| **O** (Outcome) | {{OUTCOME}} |
{{/if}}

{{#if SPIDER}}
| Element | Beschreibung |
|---------|-------------|
| **S** (Sample) | {{SAMPLE}} |
| **PI** (Phenomenon) | {{PHENOMENON}} |
| **D** (Design) | {{DESIGN}} |
| **E** (Evaluation) | {{EVALUATION}} |
| **R** (Research Type) | {{RESEARCH_TYPE}} |
{{/if}}

**Primärfrage:** {{PRIMARY_QUESTION}}

{{#if SECONDARY_QUESTIONS}}
**Sekundärfragen:**
{{#each SECONDARY_QUESTIONS}}
- {{this}}
{{/each}}
{{/if}}

### 2.3 EBF-Relevanz

{{EBF_RELEVANCE}}

---

## 3. Methodik

### 3.1 Suchstrategie

| Quelle | Queries | Treffer |
|--------|---------|---------|
| bcm_master.bib | {{INTERNAL_QUERIES}} | {{N_BIB}} |
| Theory Catalog | {{THEORY_QUERIES}} | {{N_THEORY}} |
| Case Registry | — | {{N_CASES}} |
| WebSearch | {{EXTERNAL_QUERIES}} | {{N_WEB}} |
| Snowballing | Top-{{SNOW_N}} Papers | {{N_SNOW}} |
| **Total** | | **{{N0}}** |

### 3.2 Inklusions-/Exklusionskriterien

**Inklusion:**
{{#each INCLUSION_CRITERIA}}
- {{this}}
{{/each}}

**Exklusion:**
| Code | Kriterium |
|------|-----------|
{{#each EXCLUSION_CRITERIA}}
| {{this.code}} | {{this.description}} |
{{/each}}

### 3.3 Screening-Verfahren (5-Kriterien-Score)

| Kriterium | Code | 0 = Nein | 1 = Teilweise | 2 = Ja |
|-----------|------|----------|---------------|--------|
| Relevanz | REL | Thema passt nicht | Teilrelevant | Kernrelevant |
| Methodik | MET | Keine Identifikation | Schwache ID | RCT/IV/DiD/RDD |
| Evidenz-Tier | TIR | Tier 3 | Tier 2 | Tier 1 |
| Kontext-Match | CTX | Anderer Kontext | Ähnlicher Kontext | Exakter Kontext |
| Aktualität | AKT | Vor 2000 | 2000-2015 | 2015-2026 |

**Entscheidungsregeln:**
- Score ≥ 6 → INCLUDE
- Score 4-5 + (REL = 2 ODER MET = 2) → INCLUDE (mit Vorbehalt)
- Score 4-5 ohne REL=2/MET=2 → EXCLUDE
- Score ≤ 3 → EXCLUDE

---

## 4. PRISMA-Flow

```
Identifiziert (N₀):              {{N0}}
├── Interne Quellen:              {{N_INTERNAL}}
└── Externe Quellen:              {{N_EXTERNAL}}
                                    │
Duplikate entfernt:              -{{N_DUPLICATES}}
                                    │
Gescreent (Titel/Abstract):      {{N_SCREENED}}
├── Exkludiert:                  -{{N_EXCLUDED_SCREENING}}
│   ├── EX-1:                     {{N_EX1}}
│   ├── EX-2:                     {{N_EX2}}
│   └── EX-3+:                   {{N_EX3PLUS}}
│
Volltext-Prüfung:                 {{N_FULLTEXT}}
├── Exkludiert:                  -{{N_EXCLUDED_FULLTEXT}}
│
════════════════════════════════════
Inkludiert (N₁):                  {{N1}}
├── Tier 1 (Gold):                {{N_TIER1}}
├── Tier 2 (Silver):              {{N_TIER2}}
└── Tier 3 (Bronze):              {{N_TIER3}}
```

---

## 5. Ergebnisse

### 5.1 Deskriptive Statistik

| Merkmal | Verteilung |
|---------|------------|
| **Nach Tier** | Tier 1: {{N_TIER1}}, Tier 2: {{N_TIER2}}, Tier 3: {{N_TIER3}} |
| **Nach Jahr** | {{YEAR_DISTRIBUTION}} |
| **Nach Methodik** | {{METHOD_DISTRIBUTION}} |
| **Nach Kontext** | {{CONTEXT_DISTRIBUTION}} |

### 5.2 Evidenz-Synthese-Tabelle

| # | Befund | Richtung | Effektstärke | T1 | T2 | T3 | Konfidenz | Mechanismus |
|---|--------|----------|-------------|----|----|----|-----------|----|
{{#each EVIDENCE_TABLE}}
| {{@index}} | {{this.finding}} | {{this.direction}} | {{this.effect_size}} | {{this.tier_1}} | {{this.tier_2}} | {{this.tier_3}} | {{this.confidence}} | {{this.mechanism}} |
{{/each}}

### 5.3 Narrative Synthese nach Mechanismen

{{#each MECHANISMS}}
#### {{this.name}}

{{this.narrative}}

**Schlüssel-Papers:** {{this.key_papers}}
**Effektstärke:** {{this.effect_size}}
**Kontextabhängigkeit:** {{this.context_dependency}}

{{/each}}

---

## 6. PRO/CONTRA Bilanz

**Hypothese:** {{HYPOTHESIS}}

### 6.1 PRO-Evidenz

| # | Paper | Tier | Befund | Gewichtung |
|---|-------|------|--------|------------|
{{#each PRO_PAPERS}}
| {{@index}} | {{this.paper}} | {{this.tier}} | {{this.finding}} | {{this.weight}} |
{{/each}}

**PRO Gesamt:** {{PRO_COUNT}} Papers, {{PRO_WEIGHTED}} gewichtete Stimmen

### 6.2 CONTRA-Evidenz

| # | Paper | Tier | Befund | Gewichtung |
|---|-------|------|--------|------------|
{{#each CONTRA_PAPERS}}
| {{@index}} | {{this.paper}} | {{this.tier}} | {{this.finding}} | {{this.weight}} |
{{/each}}

**CONTRA Gesamt:** {{CONTRA_COUNT}} Papers, {{CONTRA_WEIGHTED}} gewichtete Stimmen

### 6.3 Verdict

```
PRO:    {{PRO_WEIGHTED}} gewichtete Stimmen ({{PRO_COUNT}} Papers)
CONTRA: {{CONTRA_WEIGHTED}} gewichtete Stimmen ({{CONTRA_COUNT}} Papers)
────────────────────────────────────────
VERDICT: {{WEIGHTED_VERDICT}}
KONFIDENZ: {{CONFIDENCE}}
```

**Kontextabhängigkeit:** {{CONTEXT_DEPENDENCY}}

---

## 7. Gap-Analyse

### 7.1 Empirische Lücken

{{#each EMPIRICAL_GAPS}}
- **{{this.gap}}** (Wichtigkeit: {{this.importance}})
  - Forschbar: {{this.researchable}}
  - Vorgeschlagenes Design: {{this.suggested_design}}
{{/each}}

### 7.2 Theoretische Lücken

{{#each THEORETICAL_GAPS}}
- **{{this.gap}}** (Wichtigkeit: {{this.importance}})
  - Verbindung zu: {{this.connects_to}}
{{/each}}

### 7.3 Methodologische Lücken

{{#each METHODOLOGICAL_GAPS}}
- **{{this.gap}}** (Wichtigkeit: {{this.importance}})
{{/each}}

### 7.4 Kontextuelle Lücken

{{#each CONTEXTUAL_GAPS}}
- **{{this.gap}}**
  - Fehlender Kontext: {{this.missing_context}}
{{/each}}

---

## 8. EBF-Integration

### 8.1 Neue Papers

{{#if NEW_PAPERS}}
| # | Paper | Level | Komponenten |
|---|-------|-------|-------------|
{{#each NEW_PAPERS}}
| {{@index}} | {{this.paper_id}} | Level {{this.level}} | {{this.components}} |
{{/each}}
{{else}}
Keine neuen Papers hinzugefügt (alle bereits in bcm_master.bib).
{{/if}}

### 8.2 Parameter-Updates

{{#if NEW_PARAMETERS}}
| Parameter-ID | Symbol | Wert | Konfidenz | Quelle |
|-------------|--------|------|-----------|--------|
{{#each NEW_PARAMETERS}}
| {{this.id}} | {{this.symbol}} | {{this.value}} | {{this.confidence}} | {{this.source}} |
{{/each}}
{{else}}
Keine neuen Parameter identifiziert.
{{/if}}

### 8.3 Neue Cases

{{#if NEW_CASES}}
{{#each NEW_CASES}}
- **{{this.id}}:** {{this.title}}
{{/each}}
{{else}}
Keine neuen Cases erstellt.
{{/if}}

### 8.4 Cross-References

{{#if APPENDICES_LINKED}}
Verlinkte Appendices: {{APPENDICES_LINKED}}
{{/if}}

---

## 9. Schlussfolgerungen

### 9.1 Antwort auf die Forschungsfrage

{{CONCLUSION}}

### 9.2 Implikationen für die Praxis

{{#each PRACTICAL_IMPLICATIONS}}
{{@index}}. {{this}}
{{/each}}

### 9.3 Forschungsbedarf

{{#each RESEARCH_NEEDS}}
- {{this}}
{{/each}}

---

## Anhang

### A: Vollständige Kodierungstabelle

| Paper | DIR | ES | MEC | MOD | CTX | ID | PAR | PC | REP |
|-------|-----|----|-----|-----|-----|----|----|----|----|
{{#each CODING_TABLE}}
| {{this.paper_id}} | {{this.DIR}} | {{this.ES}} | {{this.MEC}} | {{this.MOD}} | {{this.CTX}} | {{this.ID}} | {{this.PAR}} | {{this.PC}} | {{this.REP}} |
{{/each}}

### B: Exklusions-Log

| Paper | Score | Grund | EX-Code |
|-------|-------|-------|---------|
{{#each EXCLUSION_LOG}}
| {{this.paper}} | {{this.total}} | {{this.reason}} | {{this.ex_code}} |
{{/each}}

### C: Bibliographie

{{#each BIBLIOGRAPHY}}
- {{this}}
{{/each}}

---

*Erstellt via /literature-analysis ({{MODE}}-Modus) | {{DATE}} | {{SESSION_ID}}*
*Protokoll: data/literature-analyses/{{SLA_ID}}.yaml*
*Output Registry: {{OUTPUT_REGISTRY_ID}}*
