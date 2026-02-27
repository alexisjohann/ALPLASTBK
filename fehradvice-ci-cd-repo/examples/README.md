# Beispiel-Dokumente

## Verfuegbare Beispiele

| Datei | Typ | Beschreibung |
|-------|-----|--------------|
| `beispiel-proposal-template.md` | Proposal | Beispiel-Proposal im FehrAdvice CI/CD |

## Generierung

Neue Beispiele koennen generiert werden mit:

```bash
# Proposal
node ../skill/scripts/create_fehradvice_docx.js --template proposal --client "Beispiel AG" --output beispiel-proposal.docx

# Report
node ../skill/scripts/create_fehradvice_docx.js --template report --client "Beispiel AG" --output beispiel-report.docx

# Brief
node ../skill/scripts/create_fehradvice_docx.js --template brief --title "Policy Brief" --output beispiel-brief.docx
```

## Hinweis

DOCX-Dateien (`*.docx`) werden erst generiert, wenn das `docx` npm-Paket installiert ist:

```bash
npm install docx
```

Bis dahin werden Markdown-Versionen erstellt.
