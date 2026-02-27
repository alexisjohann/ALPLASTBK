# BibTeX Key Convention (SSOT)

> **Status:** SAKROSANKT — Diese Konvention ist verbindlich für alle Papers im EBF.
> **Established:** 2026-02-11
> **Enforced by:** `scripts/validate_bibtex_key_format.py` + Pre-Commit Hook

---

## Kanonisches Format

```
{nachname}{jahr}{kurzwort}
```

**Regex:** `^[a-z]+\d{4}[a-z]+$`

---

## Regeln

| # | Regel | Beispiel |
|---|-------|----------|
| R1 | Alles lowercase, ASCII only (é→e, ä→a, ö→o, ü→u, ß→ss) | `benabou` nicht `bénabou` |
| R2 | Keine Separatoren (kein `_`, `-`, Leerzeichen) | `benabou2003democracies` nicht `benabou_2003_democracies` |
| R3 | Nachname = Erstautor, nur Buchstaben | `kahneman`, `dellavigna`, `vonderweth` |
| R4 | Jahr = exakt 4 Ziffern (Publikationsjahr) | `1979`, `2026` |
| R5 | Kurzwort = 1 bedeutungstragendes Wort aus dem Titel (PFLICHT) | `prospect`, `reciprocity`, `nudge` |
| R6 | Bei Mehrdeutigkeit: längeres Wort oder 2. Wort anhängen | `fehr2007biology` vs `fehr2007reciprocity` |
| R7 | Kurzwort-Auswahl: Erstes Wort im Titel das KEIN Stoppwort ist | Siehe Stoppwort-Liste unten |

---

## Stoppwörter (bei Kurzwort-Auswahl überspringen)

```
the, a, an, and, or, of, in, on, for, to, with, from, by, as, at,
about, into, toward, towards, beyond, through, between, among, across,
is, are, was, were, do, does, did, can, could, will, would, shall,
should, may, might, how, what, when, where, why, who, which, that, this
```

---

## Beispiele

### Korrekt

```
kahneman1979prospect       ← Kahneman & Tversky (1979) "Prospect Theory"
fehr1999theory             ← Fehr & Schmidt (1999) "A Theory of Fairness"
benabou2003democracies     ← Bénabou (2003) "Democracies and Dictatorships"
thaler2008nudge            ← Thaler & Sunstein (2008) "Nudge"
dellavigna2007fox          ← DellaVigna & Kaplan (2007) "The Fox News Effect"
```

### Falsch

```
❌ benabou_2003_democracies       (Underscores)
❌ Kahneman1979prospect           (Grossbuchstabe)
❌ costagomes2006                 (kein Kurzwort)
❌ fehr2007                       (kein Kurzwort — welches Paper?)
❌ kahneman1979                   (kein Kurzwort)
❌ bénabou2003democracies         (Akzent-Zeichen)
```

---

## Sonderfälle

| Fall | Lösung | Beispiel |
|------|--------|---------|
| Mehrere Autoren im Key | Nur Erstautor | `kahneman1979prospect` (nicht `kahnemantversky1979`) |
| Zwei Erstautoren üblich | Beide Namen, kein Separator | `fehrgachter2000cooperation` |
| Institutioneller Autor | Kurzform lowercase | `oecd2017pisa`, `who2024report` |
| Working Paper | Jahr der WP-Veröffentlichung | `fehr2026inequality` |
| Gleicher Autor + Jahr + ähnlicher Titel | Längeres/anderes Kurzwort | `fehr2007biology` vs `fehr2007reciprocity` |
| Buch (kein Artikel) | Gleiche Regeln | `thaler2008nudge` |
| Nicht-lateinische Autoren | Transliteration | `zhou2024behavioral` |

---

## Migration von Legacy-Keys

| Legacy-Format | Aktion | Beispiel |
|---------------|--------|---------|
| `name_year_words` | Underscores entfernen | `benabou_2003_democracies` → `benabou2003democracies` |
| `nameyear` (ohne Kurzwort) | Kurzwort aus Titel ergänzen | `costagomes2006` → `costagomes2006cognition` |
| `NameYear` (Grossbuchstaben) | Lowercase | `AllcottRogers2014` → `allcottrogers2014` |
| `name2024suffix2` (Nummer) | Kurzwort statt Nummer | `card2018active2` → prüfen ob sinnvoll |

---

## Validation

```bash
# Einzelnen Key prüfen
python scripts/validate_bibtex_key_format.py --check "kahneman1979prospect"

# Alle Keys prüfen
python scripts/validate_bibtex_key_format.py --all

# Nur Fehler anzeigen
python scripts/validate_bibtex_key_format.py --errors-only

# Migration-Vorschläge generieren
python scripts/validate_bibtex_key_format.py --suggest
```

---

## Durchsetzung

> **HARD BLOCK seit 2026-02-11.** Migration abgeschlossen: 2,347/2,347 = 100% kanonisch.
> Nicht-kanonische Keys werden vom Pre-Commit Hook **abgelehnt** — keine Ausnahmen.

1. **Pre-Commit Hook (BLOCK):** Commits mit nicht-kanonischen Keys werden **blockiert**
2. **`/add-paper` Skill:** Generiert Keys automatisch im kanonischen Format
3. **`/integrate-paper` Skill:** Validiert Keys bei Integration
4. **CI/CD:** GitHub Action prüft bei jedem Push

---

## Warum diese Konvention?

1. **Vorhersagbarkeit:** Aus Autor + Jahr + Titel kann der Key deterministisch abgeleitet werden
2. **Eindeutigkeit:** Kurzwort verhindert Kollisionen bei gleichem Autor/Jahr
3. **Maschinenlesbarkeit:** Regex-validierbar, keine Sonderzeichen
4. **100%-Compliance:** Alle 2,347 Keys entsprechen diesem Format (migriert 2026-02-11)
