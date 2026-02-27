# /paper-search - Paper Web Search & Enrichment

Systematische Paper-Suche via WebSearch mit zwei Modulen:
**Modul 1 (Enrich):** Bestehende Papers mit Volltext anreichern (L0/L1 → L2/L3)
**Modul 2 (Discover):** Neue Papers zu einem Thema finden und integrieren

## Verwendung

```bash
/paper-search enrich PAP-xxx              # 1 Paper anreichern
/paper-search enrich --batch 10           # 10 Papers anreichern (Priorität: Tier 1 zuerst)
/paper-search enrich --author "Fehr"      # Alle Fehr-Papers anreichern
/paper-search discover "loss aversion"    # Neue Papers zu einem Thema finden
/paper-search discover --theory MS-RD-001 # Papers zu einer Theorie finden
/paper-search discover --gap              # Lücken in der DB identifizieren und füllen
/paper-search status                      # Enrichment-Statistiken anzeigen
```

## Modul 1: ENRICH (Bestehende Papers anreichern)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MODUL 1: ENRICH                                                        │
│  Input:  Bestehendes Paper (PAP-xxx) mit L0/L1                          │
│  Output: Upgrade auf L2/L3 mit Volltext                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: Paper laden                                                 │
│  → PAP-xxx.yaml lesen                                                   │
│  → Titel, Autor, Jahr, DOI extrahieren                                 │
│                                                                         │
│  SCHRITT 2: WebSearch nach Volltext                                     │
│  → Query 1: "{Titel} {Autor} {Jahr} full text PDF"                      │
│  → Query 2: "{DOI}" (falls vorhanden)                                   │
│  → Query 3: "{Titel} site:nber.org OR site:ssrn.com OR site:arxiv.org"  │
│                                                                         │
│  SCHRITT 3: Beste Quelle auswählen                                     │
│  → Priorität: NBER > SSRN > arXiv > Journal > Other                    │
│  → Open Access bevorzugen                                               │
│  → WebFetch auf beste URL                                               │
│                                                                         │
│  SCHRITT 4: Content extrahieren                                         │
│  → Abstract, Key Findings, Methodology, Sample                          │
│  → Strukturelle Merkmale S1-S6 bestimmen                               │
│  → Content Level bestimmen (L1/L2/L3)                                  │
│                                                                         │
│  SCHRITT 5: In DB speichern                                             │
│  → Volltext → data/paper-texts/PAP-xxx.md                              │
│  → YAML updaten (content_level, full_text, summary)                    │
│  → prior_score.content_level aktualisieren                             │
│                                                                         │
│  SCHRITT 6: Validieren                                                  │
│  → YAML parst korrekt                                                   │
│  → Content Level stimmt mit S1-S6 überein                              │
│  → Volltext-Datei existiert und ist nicht leer                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Enrichment-Priorität (--batch Modus)

Bei `--batch N` werden Papers in dieser Reihenfolge abgearbeitet:

| Priorität | Kriterium | Begründung |
|-----------|-----------|------------|
| 1 | Evidence Tier 1 + L1 | Höchste Qualität, fehlt Volltext |
| 2 | Evidence Tier 1 + L0 | Höchste Qualität, fehlt alles |
| 3 | Evidence Tier 2 + L1 + has_theory_support | Theoretisch wichtig |
| 4 | Evidence Tier 2 + L1 | Solide Qualität |
| 5 | Rest | Niedrigere Priorität |

### WebSearch Query-Strategie

```
Query-Kaskade (stoppt beim ersten Treffer mit Volltext):

1. DOI-basiert (wenn vorhanden):
   → "doi.org/{DOI}" oder "{DOI} PDF"
   → Höchste Trefferquote für Journal-Papers

2. Titel-basiert:
   → "{Exakter Titel}" filetype:pdf
   → Gut für eindeutige Titel

3. NBER/SSRN/arXiv-basiert:
   → "{Titel} {Erstautor}" site:nber.org
   → "{Titel} {Erstautor}" site:ssrn.com
   → "{Titel} {Erstautor}" site:arxiv.org

4. Google Scholar:
   → "{Titel} {Erstautor} {Jahr}" scholar
```

### Content-Level Bestimmung nach WebFetch

```
S1 (Research Question) vorhanden?  → mindestens L1
S2 (Methodology) vorhanden?        → }
S3 (Sample/Data) vorhanden?        → } zusammen = L2
S4 (Findings) vorhanden?           → }
Vollständiger Originaltext?         → L3 (nur wenn R1-R4 erfüllt)
```

## Modul 2: DISCOVER (Neue Papers finden)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MODUL 2: DISCOVER                                                      │
│  Input:  Suchquery / Theorie-ID / Lücken-Analyse                       │
│  Output: Neue Papers in BibTeX + YAML + Volltext                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SCHRITT 1: Query formulieren                                           │
│  → Aus Theorie-ID: theory-catalog.yaml → Keywords                      │
│  → Aus Lücke: Welche 10C-Dimensionen sind unterrepräsentiert?          │
│  → Direkt: User-Query verwenden                                        │
│                                                                         │
│  SCHRITT 2: WebSearch ausführen                                        │
│  → Google Scholar: "{Query} {Jahr-Range}"                               │
│  → NBER: "{Query} site:nber.org"                                        │
│  → SSRN: "{Query} site:ssrn.com"                                       │
│                                                                         │
│  SCHRITT 3: Deduplizierung                                              │
│  → Gegen bcm_master.bib prüfen (Titel-Match)                          │
│  → Gegen PAP-*.yaml prüfen (DOI-Match)                                 │
│  → Nur NEUE Papers weiterverarbeiten                                   │
│                                                                         │
│  SCHRITT 4: Relevanz-Filter                                             │
│  → EBF-Relevanz prüfen (10C, Parameter, Theorie)                      │
│  → Evidence Tier schätzen (Journal-Qualität)                           │
│  → Top N relevanteste Papers auswählen                                 │
│                                                                         │
│  SCHRITT 5: Volltext holen                                              │
│  → WebFetch auf Paper-URL                                               │
│  → Content extrahieren (wie Modul 1, Schritt 4)                        │
│                                                                         │
│  SCHRITT 6: Integration                                                 │
│  → BibTeX-Eintrag erstellen                                            │
│  → PAP-xxx.yaml erstellen                                              │
│  → Volltext → data/paper-texts/PAP-xxx.md                              │
│  → /integrate-paper Workflow für Level-Bestimmung                      │
│                                                                         │
│  SCHRITT 7: Report                                                      │
│  → Gefundene Papers auflisten                                          │
│  → Relevanz-Score anzeigen                                             │
│  → Integration-Empfehlung pro Paper                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Discovery Query-Templates

| Modus | Query-Template | Beispiel |
|-------|---------------|----------|
| `--topic` | "{Topic} behavioral economics experiment" | "default effects savings" |
| `--theory` | theory-catalog → Keywords + Restrictions | MS-RD-001 → "prospect theory loss aversion" |
| `--author` | "{Author} recent papers {Year-Range}" | "Ernst Fehr 2024 2025 2026" |
| `--gap` | Unterrepräsentierte 10C × Evidence Tier | AWARE + Tier 1 = wenig Papers |

### Deduplizierungs-Logik

```
Für jedes gefundene Paper:

1. DOI-Match: Exakter DOI in bcm_master.bib?
   → JA: SKIP (bereits vorhanden)

2. Titel-Match: Fuzzy-Match (>90% Ähnlichkeit) gegen alle Titel?
   → JA: SKIP (wahrscheinlich vorhanden)

3. Autor+Jahr: Gleicher Erstautor + gleiches Jahr?
   → WARNUNG: Mögliches Duplikat, manuell prüfen
```

## Gemeinsame Regeln

### Copyright-Respekt

```
ERLAUBT:
✅ Open Access Papers (Creative Commons, etc.)
✅ NBER Working Papers (öffentlich zugänglich)
✅ SSRN Preprints (öffentlich zugänglich)
✅ arXiv Papers (öffentlich zugänglich)
✅ Autoren-Websites (self-hosted PDFs)
✅ Abstracts und Metadaten (immer frei)

NICHT ERLAUBT:
❌ Paywalled Journal-Artikel (nur Abstract extrahieren)
❌ Sci-Hub oder ähnliche Piraterie-Seiten
❌ Copyright-geschützte PDFs ohne Open Access
```

### Volltext-Speicherung (SSOT)

```
Pfad:    data/paper-texts/PAP-{bibtex_key}.md
Format:  Markdown
Inhalt:  NUR Originaltext (keine EBF-Analyse!)
         EBF-Metadaten gehören in PAP-{key}.yaml
```

### Sandbox-Limitation (KRITISCH!)

```
⚠️  WebFetch ist in der Claude Code Sandbox BLOCKIERT (403 Forbidden)!

KONSEQUENZ:
├── WebSearch FUNKTIONIERT → Metadaten, Abstracts, Key Findings extrahierbar
├── WebFetch BLOCKIERT     → Volltexte können NICHT direkt geholt werden
│
├── L1 → L2 MÖGLICH: Via WebSearch-Daten (Methodology, Sample, Findings)
├── L2 → L3 NICHT MÖGLICH: Erfordert Volltext (manueller Download nötig)
│
└── WORKAROUND für L3:
    1. User lädt PDF manuell herunter
    2. User teilt Text in Chat → Auto-Upgrade auf L3
    3. GitHub Actions Workflow für API-basierte Extraktion (geplant)
```

### Rate Limiting

```
WebSearch: Max 3 Queries pro Paper
WebFetch:  Max 2 Fetches pro Paper (falls nicht blockiert)
Pause:     2 Sekunden zwischen Queries
Batch:     Max 10 Papers pro Session (ohne explizite Freigabe)
```

## Beispiel-Workflow

### Modul 1: Einzelnes Paper anreichern

```
User: /paper-search enrich PAP-AllcottRogers2014

Claude:
  📖 Paper: AllcottRogers2014
  📊 Aktuell: L1 (Abstract vorhanden, kein Volltext)
  🔍 Suche Volltext...

  Query 1: "10.1257/aer.104.10.3003" → AER Paywall ❌
  Query 2: "Short-Run Long-Run Effects Behavioral Interventions Allcott" PDF
           → Harvard Scholar PDF gefunden ✅

  📥 Fetching: scholar.harvard.edu/.../allcott_rogers.aer_.2014.pdf
  📝 Extrahiere: S1✓ S2✓ S3✓ S4✓ S5✓ S6✗
  📈 Upgrade: L1 → L2

  Gespeichert:
  → data/paper-texts/PAP-AllcottRogers2014.md
  → PAP-AllcottRogers2014.yaml (content_level: L2)
```

### Modul 2: Neue Papers finden

```
User: /paper-search discover "social norms energy conservation"

Claude:
  🔍 Suche: "social norms energy conservation behavioral economics 2023-2026"

  Gefunden: 8 Papers
  Davon neu: 5 (3 bereits in DB)

  | # | Titel | Autor | Jahr | Tier | Relevanz |
  |---|-------|-------|------|------|----------|
  | 1 | "Persistent Effects of..." | Allcott | 2024 | 1 | 0.92 |
  | 2 | "Social Comparison..." | Ferraro | 2025 | 1 | 0.88 |
  | 3 | "Nudging Energy..." | Costa | 2024 | 2 | 0.75 |
  | ...

  Empfehlung: Paper 1 + 2 integrieren (Tier 1, hohe Relevanz)

  Soll ich Paper 1 + 2 via /integrate-paper aufnehmen?
```
