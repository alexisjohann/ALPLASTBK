# Meeting-Report: {{NAME}} ({{ORGANISATION}})

**Datum:** {{DATUM}} | {{ZEIT_START}} - {{ZEIT_ENDE}}
**Ort:** {{ORT}}
**Teilnehmer:** {{FA_TEILNEHMER}}, {{GESPRAECHSPARTNER}}
**Meeting-ID:** {{MEETING_ID}}
**Session-ID:** {{SESSION_ID}}
**Status:** ✅ MEETING DURCHGEFÜHRT - Follow-ups dokumentiert

---

## 1. Gesprächspartner:in

| Feld | Details |
|------|---------|
| **Name** | {{NAME}} |
| **Position** | {{POSITION}} |
| **Organisation** | {{ORGANISATION}} |
| **Status** | {{STATUS}} |
| **Hintergrund** | {{HINTERGRUND}} |

### Relevante Erfahrung
{{ERFAHRUNG_LISTE}}

---

## 2. Kontext: Warum dieses Meeting?

{{KONTEXT_BESCHREIBUNG}}

**Relevanz für {{ORGANISATION}}:**
{{RELEVANZ_PUNKTE}}

---

## 3. Besprochene Themen

{{#each THEMEN}}
- {{#if BESPROCHEN}}✅{{else}}⏳{{/if}} {{THEMA}}
{{/each}}

---

## 4. Kernerkenntnisse

{{ERKENNTNISSE}}

---

## 5. Verknüpfte EBF-Analysen

| Session-ID | Thema | Status |
|------------|-------|--------|
{{#each EBF_SESSIONS}}
| {{SESSION_ID}} | {{THEMA}} | {{#if PRAESENTIERT}}Im Meeting präsentiert{{else}}Referenz{{/if}} |
{{/each}}

---

## 6. Empfohlene Gesprächspunkte (für Folgemeetings)

### A) Einstieg (Rapport)
{{EINSTIEG_PUNKTE}}

### B) Fachliche Diskussion
{{FACHLICHE_PUNKTE}}

### C) Nächste Schritte
{{NAECHSTE_SCHRITTE_PUNKTE}}

---

## 7. Hintergrundinformationen zu {{ORGANISATION}}

### Organisation
| Aspekt | Details |
|--------|---------|
{{#each ORG_INFO}}
| **{{ASPEKT}}** | {{DETAILS}} |
{{/each}}

### Aktuelle Prioritäten
{{PRIORITAETEN_LISTE}}

---

## 8. Risiken / Sensibilitäten

| Risiko | Mitigation |
|--------|------------|
{{#each RISIKEN}}
| **{{RISIKO}}** | {{MITIGATION}} |
{{/each}}

---

## 9. Strategische Optionen (falls relevant)

{{#if STRATEGISCHE_OPTIONEN}}
### Grundidee

{{STRATEGIE_GRUNDIDEE}}

### Offerten-Optionen

{{#each OFFERTEN}}
#### Option {{BUCHSTABE}}: {{TITEL}}

| Aspekt | Details |
|--------|---------|
{{#each ASPEKTE}}
| **{{KEY}}** | {{VALUE}} |
{{/each}}

{{/each}}
{{/if}}

---

## 10. Follow-up Aktionen

| # | Aktion | Verantwortlich | Deadline | Status |
|---|--------|----------------|----------|--------|
{{#each FOLLOWUPS}}
| {{INDEX}} | {{#if PRIO}}**{{AKTION}}**{{else}}{{AKTION}}{{/if}} | {{OWNER}} | {{#if PRIO}}**{{DEADLINE}}**{{else}}{{DEADLINE}}{{/if}} | {{STATUS_ICON}} |
{{/each}}

### Follow-up Paket

**Zu versenden an {{NAME}}:**

| Dokument | Datei | Format |
|----------|-------|--------|
{{#each DOKUMENTE}}
| {{DOKUMENT}} | `{{DATEI}}` | {{FORMAT}} |
{{/each}}

---

## 11. Meeting-Notizen

**Gesprächsqualität:** {{QUALITAET}}
**Beziehung:** {{FA_TEILNEHMER}} & {{NAME}} per {{ANREDE}}

**Besprochene Themen:**
{{#each THEMEN_NOTIZEN}}
- {{#if ERLEDIGT}}✅{{else}}📌{{/if}} {{NOTIZ}}
{{/each}}

**Nächster Kontakt:** {{NAECHSTER_KONTAKT}}

---

*Erstellt: {{ERSTELLT_DATUM}} | Meeting-ID: {{MEETING_ID}} | Version {{VERSION}}*

---

<!-- SSOT: templates/meeting-report-template.md | Template-Version: 1.0 | 2026-02-04 -->
<!-- Änderungen NUR hier vornehmen - siehe CLAUDE.md SSOT Registry -->
