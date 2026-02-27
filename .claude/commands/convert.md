# /convert - Dokument-Format konvertieren

Konvertiere Dokumente zwischen verschiedenen Formaten mit pandoc.

## Verwendung
```
/convert <quelle> <ziel-format>
/convert outputs/paper.tex docx
/convert chapters/03_limits_utility.tex markdown
/convert README.md pdf
```

## Unterstützte Formate

| Format | Extension | Beschreibung |
|--------|-----------|--------------|
| `docx` | .docx | Microsoft Word (für Kollaboration) |
| `markdown` / `md` | .md | Markdown |
| `pdf` | .pdf | PDF (via LaTeX) |
| `html` | .html | Webseite |
| `epub` | .epub | E-Book |

## Anweisungen

1. Bestimme Quell- und Zielformat
2. Führe pandoc aus:
   ```bash
   pandoc <quelle> -o <ziel>.<format> --standalone
   ```

3. Für LaTeX → DOCX (beste Qualität):
   ```bash
   pandoc <quelle> -o <ziel>.docx \
     --standalone \
     --reference-doc=template.docx  # falls vorhanden
   ```

4. Für Markdown → PDF:
   ```bash
   pandoc <quelle> -o <ziel>.pdf --pdf-engine=pdflatex
   ```

## Typische Anwendungsfälle

| Von | Nach | Anwendung |
|-----|------|-----------|
| LaTeX → DOCX | Word-Version für Reviewer/Koautoren |
| LaTeX → MD | README/Dokumentation erstellen |
| MD → PDF | Schnelle PDF aus Markdown |
| MD → DOCX | Dokument für Word-Nutzer |

## Beispiel-Output

```
Konvertiere: outputs/paper.tex → outputs/paper.docx
  pandoc ... ✓
Erstellt: outputs/paper.docx (245 KB)
```
