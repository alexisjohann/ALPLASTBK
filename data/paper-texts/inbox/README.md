# Paper Inbox

> **Drop-Zone** für Papers die direkt auf GitHub hochgeladen werden.
> Established: 2026-02-21

## Zweck

Hier können Papers hochgeladen werden, **ohne** vorher einen BibTeX-Key zu vergeben.
Claude verarbeitet sie automatisch bei der nächsten Session.

## Unterstützte Formate

| Format | Empfohlen | Hinweis |
|--------|-----------|---------|
| `.md` | Ja | Markdown, direkt nutzbar |
| `.txt` | Ja | Plain Text, wird zu .md konvertiert |
| `.pdf` | Bedingt | GitHub zeigt keine Preview; wird bei Verarbeitung extrahiert |

## Namenskonvention (optional)

Am besten den Dateinamen so wählen, dass das Paper identifizierbar ist:

```
nachname_jahr_kurzwort.md       (ideal)
nachname_jahr.md                (ok)
paper_title_keywords.md         (ok)
beliebiger_name.md              (auch ok)
```

**Beispiele:**
- `kahneman_1979_prospect.md`
- `fehr_schmidt_1999_inequity.md`
- `loss_aversion_new_paper.md`

## Was passiert nach dem Upload?

Claude verarbeitet jede Datei automatisch:

```
1. Paper identifizieren (Autor, Jahr, Titel, DOI)
2. BibTeX-Key generieren: {nachname}{jahr}{kurzwort}
3. Umbenennen zu: PAP-{key}.md
4. Verschieben nach: data/paper-texts/
5. YAML-Metadaten erstellen in: data/paper-references/PAP-{key}.yaml
6. BibTeX-Eintrag hinzufügen in: bibliography/bcm_master.bib
7. Content Level bestimmen (L1/L2/L3)
8. Aus inbox/ entfernen
```

## Regeln

1. **Nur wissenschaftliche Papers** (keine Bücher, Blogposts, etc.)
2. **Copyright beachten** - nur Open Access oder mit Erlaubnis
3. **Ein Paper pro Datei**
4. **Keine Duplikate** - wird automatisch geprüft gegen bcm_master.bib

## Dateiformat für Volltext (empfohlen)

```markdown
# Paper Title

**Authors:** Author List
**Year:** 2026
**Journal:** Journal Name
**DOI:** 10.xxxx/xxxxx

---

## Abstract

Abstract text...

## 1. Introduction

Section text...

## References

Reference list...
```

---

*Established: 2026-02-21 | Version: 1.0*
