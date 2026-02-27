# /lookup-paper - Paper Metadata Lookup via Crossref

## Beschreibung

Sucht wissenschaftliche Paper-Metadaten über das Crossref REST API. Primäre Datenquelle für DOI-basierte Paper-Suche.

## Aufruf

```bash
/lookup-paper "Prospect Theory"                    # Titel-Suche
/lookup-paper --doi 10.3386/w12345                # DOI direkt
/lookup-paper --author "Kahneman"                  # Autor-Suche
/lookup-paper --nber 2024                          # Alle NBER Papers 2024
/lookup-paper --ssrn 1234567                       # SSRN Paper (wenn DOI existiert)
```

## Crossref API Grundlagen

### Endpoint
```
https://api.crossref.org/works
```

### Wichtige Query-Parameter

| Parameter | Beschreibung | Beispiel |
|-----------|--------------|----------|
| `query` | Volltext-Suche | `query=behavioral+economics` |
| `query.title` | Titel-Suche | `query.title=prospect+theory` |
| `query.author` | Autor-Suche | `query.author=Thaler` |
| `filter` | Filter kombinieren | `filter=prefix:10.3386` |
| `rows` | Ergebnisse pro Seite (max 1000) | `rows=50` |
| `cursor` | Pagination für große Sets | `cursor=*` |

### Wichtige Filter

| Filter | Beschreibung | Beispiel |
|--------|--------------|----------|
| `prefix` | DOI-Prefix | `prefix:10.3386` (NBER) |
| `from-pub-date` | Ab Datum | `from-pub-date:2024-01-01` |
| `until-pub-date` | Bis Datum | `until-pub-date:2024-12-31` |
| `type` | Publikationstyp | `type:journal-article` |

## DOI-Patterns nach Publisher

| Publisher | Prefix | Format | Coverage |
|-----------|--------|--------|----------|
| **NBER** | `10.3386` | `10.3386/wXXXXX` | Fast alle Working Papers |
| **SSRN** | `10.2139` | `10.2139/ssrn.XXXXXXX` | Viele, nicht alle |
| **AER** | `10.1257` | `10.1257/aer.XXXXXXX` | Alle |
| **Econometrica** | `10.3982` | `10.3982/ECTA...` | Alle |

## Beispiel-Requests

### 1. Paper nach DOI
```bash
curl "https://api.crossref.org/works/10.3386/w12345" \
  -H "User-Agent: EBF-Research (mailto:research@fehradvice.com)"
```

### 2. Alle NBER Papers 2024
```bash
curl "https://api.crossref.org/works?filter=prefix:10.3386,from-pub-date:2024-01-01&cursor=*&rows=100" \
  -H "User-Agent: EBF-Research (mailto:research@fehradvice.com)"
```

### 3. Titel-Suche
```bash
curl "https://api.crossref.org/works?query.title=mental+accounting&rows=10" \
  -H "User-Agent: EBF-Research (mailto:research@fehradvice.com)"
```

### 4. Autor-Suche
```bash
curl "https://api.crossref.org/works?query.author=Fehr+Ernst&rows=50" \
  -H "User-Agent: EBF-Research (mailto:research@fehradvice.com)"
```

## Error Handling

### Kein DOI gefunden
```
WICHTIG: Wenn kein DOI existiert, kann Crossref das Paper NICHT liefern.
Explizit sagen: "Kein DOI → nicht über Crossref auffindbar"
```

### Fallback-Strategie
1. **OpenAlex** - Breite Abdeckung, auch ohne DOI
2. **Semantic Scholar** - AI-powered, Paper-Embeddings
3. **Google Scholar** - Manuell, letzte Option

### NIEMALS
- DOIs erfinden/halluzinieren
- Paper als "gefunden" melden wenn nicht in Crossref
- Ohne Bestätigung behaupten, ein Paper existiert

## Output-Format

Strukturierte Ausgabe:
```yaml
paper:
  title: "Prospect Theory: An Analysis of Decision under Risk"
  authors:
    - "Daniel Kahneman"
    - "Amos Tversky"
  year: 1979
  journal: "Econometrica"
  doi: "10.2307/1914185"
  source: "crossref_confirmed"
  url: "https://doi.org/10.2307/1914185"
```

## Integration mit EBF

Nach erfolgreichem Lookup:
1. Paper in `bcm_master.bib` eintragen (wenn relevant)
2. `use_for` Tags setzen (LIT-KT, DOMAIN-*, etc.)
3. `theory_support` Tags setzen (MS-RD-001, etc.)
4. Optional: In Appendix referenzieren

## Scripts

- `scripts/lookup_paper_dois.py` - Einzel-DOI Lookup
- `scripts/batch_doi_by_journal.py` - Batch-Verarbeitung

## API Registry

Vollständige Konfiguration: `data/api-registry.yaml` → API-BIB-001 (CrossRef)

## Typische Use Cases

1. **Neues Paper für Bibliographie prüfen**
   - Existiert DOI? → Crossref lookup
   - Metadaten korrekt? → Validieren
   - In bcm_master.bib eintragen

2. **NBER Working Papers tracken**
   - Alle neuen NBER Papers eines Zeitraums finden
   - Prefix-Filter `10.3386` verwenden

3. **Autor-Publikationsliste**
   - Alle Papers eines Autors finden
   - Mit bcm_master.bib abgleichen

4. **DOI-Validierung**
   - Prüfen ob BibTeX-DOI korrekt ist
   - Metadaten aktualisieren
