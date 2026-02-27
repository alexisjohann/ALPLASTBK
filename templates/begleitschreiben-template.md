# Follow-up: {{BETREFF}}

**An:** {{NAME}}
**Von:** {{FA_TEILNEHMER}}
**Datum:** {{DATUM}}
**Betreff:** {{BETREFF}} - wie besprochen

---

{{#if DU}}Liebe{{else}}Sehr geehrte{{/if}} {{VORNAME}}{{#unless DU}} {{NACHNAME}}{{/unless}}

Vielen Dank für das {{QUALITAET_ADJ}} Gespräch {{WANN}} in {{ORT}}. {{EINLEITUNG_CUSTOM}}

{{#if KERNBEFUNDE}}
## Kernbefunde auf einen Blick

| Kennzahl | Wert |
|----------|------|
{{#each KERNBEFUNDE}}
| {{KENNZAHL}} | **{{WERT}}** |
{{/each}}
{{/if}}

{{#if ZENTRALE_ERKENNTNIS}}
## Die zentrale Erkenntnis

> {{ZENTRALE_ERKENNTNIS}}
{{/if}}

## Nächste Schritte

{{NAECHSTE_SCHRITTE}}

{{#if DU}}Herzliche Grüsse{{else}}Mit freundlichen Grüssen{{/if}}
{{FA_TEILNEHMER}}

---

{{#if BEILAGEN}}
**Beilage{{#if BEILAGEN_PLURAL}}n{{/if}}:** {{BEILAGEN_TEXT}}
{{/if}}

---

<!-- SSOT: templates/begleitschreiben-template.md | Template-Version: 1.0 | 2026-02-04 -->
<!-- Änderungen NUR hier vornehmen - siehe CLAUDE.md SSOT Registry -->
