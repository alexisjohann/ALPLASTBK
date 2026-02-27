# /compile - LaTeX zu PDF kompilieren

Kompiliere eine LaTeX-Datei zu PDF mit latexmk (automatische Dependency-Auflösung).

## Verwendung
```
/compile <datei.tex>
/compile outputs/paper_chapter3_limits_utility.tex
/compile chapters/03_limits_utility.tex
```

## Anweisungen

1. Prüfe, ob die angegebene .tex Datei existiert
2. Führe aus:
   ```bash
   latexmk -pdf -interaction=nonstopmode -cd <datei.tex>
   ```
   - `-pdf`: Erzeuge PDF
   - `-interaction=nonstopmode`: Keine interaktiven Prompts
   - `-cd`: Wechsle ins Verzeichnis der Datei

3. Bei Erfolg: Berichte Seitenzahl und Dateigröße
4. Bei Fehler: Zeige relevante Fehlermeldungen aus dem Log

5. Optional: Aufräumen mit `latexmk -c` (behält PDF, löscht .aux/.log/.toc)

## Vorteile von latexmk

- Automatische Erkennung, wie oft pdflatex laufen muss
- Automatische bibtex/biber Ausführung wenn nötig
- Dependency-Tracking (nur neu kompilieren wenn nötig)

## Beispiel-Output

```
Kompiliere: outputs/paper.tex
  latexmk -pdf ... ✓
PDF erstellt: outputs/paper.pdf (18 Seiten, 263 KB)
```
