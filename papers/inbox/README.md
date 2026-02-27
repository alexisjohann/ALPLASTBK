# Papers Inbox

> Upload-Ordner für neue Research Papers zur EBF-Evaluation

## Workflow

```
1. PDF hier hochladen (via GitHub UI oder git push)
2. GitHub Action extrahiert Metadaten
3. Paper wird zu papers-to-integrate.yaml hinzugefügt
4. EIP-Evaluation entscheidet: INTEGRATE / REJECT / MODIFY
5. Bei INTEGRATE → bcm_master.bib + Appendix-Referenz
6. PDF wird nach papers/evaluated/ verschoben
```

## Dateinamens-Konvention

```
{autor}_{jahr}_{kurztitel}.pdf
```

**Beispiele:**
- `fehr_2024_cooperation.pdf`
- `kahneman_1979_prospect.pdf`
- `thaler_2008_nudge.pdf`

## Upload-Methoden

### Via GitHub UI (einfachste)
1. Navigiere zu `papers/inbox/`
2. "Add file" → "Upload files"
3. PDF hochladen
4. Commit message: `paper: Add {autor}_{jahr}_{kurztitel}`

### Via Git
```bash
cp ~/Downloads/fehr_2024_paper.pdf papers/inbox/
git add papers/inbox/fehr_2024_paper.pdf
git commit -m "paper: Add fehr_2024_cooperation"
git push
```

## Was passiert nach Upload?

1. **GitHub Action** wird getriggert
2. **Metadaten-Extraktion** (aus Dateiname + optional PDF)
3. **Crossref-Lookup** (DOI suchen falls nicht im Namen)
4. **papers-to-integrate.yaml** wird aktualisiert
5. **Notification** im Action-Log

## Ordnerstruktur

```
papers/
├── inbox/           ← Neue Papers hierhin
├── evaluated/       ← Nach EIP-Evaluation
│   ├── integrated/  ← In EBF aufgenommen
│   └── rejected/    ← Nicht passend für EBF
└── README.md
```

## Hinweise

- **Max. Dateigrösse:** GitHub erlaubt bis 100 MB pro Datei
- **Formate:** Nur PDF (`.pdf`)
- **Duplikate:** Werden automatisch erkannt via DOI
- **Ohne DOI:** Paper wird trotzdem erfasst, DOI-Feld bleibt leer
