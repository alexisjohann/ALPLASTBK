# /build-all - Alle Papers kompilieren

Kompiliere alle LaTeX-Dokumente im Repository zu PDFs.

## Verwendung
```
/build-all
/build-all --outputs-only
/build-all --chapters
```

## Optionen

| Option | Beschreibung |
|--------|--------------|
| (keine) | Kompiliert alles: outputs/, papers/ |
| `--outputs-only` | Nur outputs/ Verzeichnis |
| `--chapters` | Auch chapters/ (dauert länger) |

## Anweisungen

1. Finde alle .tex Dateien in den relevanten Verzeichnissen:
   ```bash
   find outputs/ -name "*.tex" -type f
   find papers/ -name "*.tex" -type f 2>/dev/null
   ```

2. Für jede Datei:
   ```bash
   latexmk -pdf -interaction=nonstopmode -cd <datei>
   ```

3. Sammle Ergebnisse:
   - ✅ Erfolgreich kompiliert
   - ❌ Fehler (zeige Log-Auszug)

4. Zusammenfassung am Ende:
   ```
   === Build Summary ===
   ✅ 5 erfolgreich
   ❌ 1 fehlgeschlagen

   Fehlgeschlagen:
   - outputs/broken.tex: Missing \end{document}
   ```

## Beispiel-Output

```
=== Building all papers ===

[1/3] outputs/paper_chapter3_limits_utility.tex
      latexmk -pdf ... ✓ (18 pages)

[2/3] outputs/paper_bcj_fehr_style.tex
      latexmk -pdf ... ✓ (12 pages)

[3/3] papers/WP_2026_01.tex
      latexmk -pdf ... ✓ (24 pages)

=== Build Summary ===
✅ 3/3 erfolgreich
```
