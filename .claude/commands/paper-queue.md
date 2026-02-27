# /paper-queue - Paper Integration Queue Management

## Beschreibung

Verwaltet die Staging-Queue für Papers vor der Integration in bcm_master.bib.

**Primary Key:** `bibtex_key` (kein separater SuperKey)

## Aufruf

```bash
/paper-queue                              # Status-Übersicht
/paper-queue add funke2017cps             # Paper hinzufügen
/paper-queue list                         # Alle pending Papers
/paper-queue list --priority HIGH         # Nach Priorität filtern
/paper-queue start funke2017cps           # EIP starten
/paper-queue done funke2017cps            # Integriert → entfernen
```

## Datenbank

```
data/papers-to-integrate.yaml
```

## Struktur (vereinfacht)

```yaml
papers:
  - bibtex_key: "funke2017cps"       # Primary ID = bcm_master key
    doi: "10.3389/fpsyg.2017.01153"
    status: PENDING
    priority: MEDIUM
    added: "2026-01-28"

    title: "Complex Problem Solving"
    authors: ["Joachim Funke"]
    year: 2017
    source: JOURNAL

    target: "CP"
    use_for: ["DOMAIN-CPS"]

    eip:
      pro: []
      contra: []
      decision: null

    notes: "Kern-Review für CPS-Appendix"
```

## Workflow

```
Discovery → PENDING → IN_PROGRESS (EIP) → bcm_master.bib → Remove
```

## Status

| Status | Bedeutung |
|--------|-----------|
| `PENDING` | Wartet auf EIP |
| `IN_PROGRESS` | EIP läuft |
| `BLOCKED` | Fehlt Info |

## Integration Checklist

```
[ ] DOI verifiziert (Crossref)
[ ] EIP: PRO + CONTRA Evidenz
[ ] Entscheidung dokumentiert
[ ] BibTeX in bcm_master.bib (6 EBF-Felder)
[ ] Cross-References gesetzt
[ ] Aus Queue entfernt
```

## Verwandte Skills

- `/lookup-paper` - Crossref API
- `/classify-papers` - use_for, theory_support Tags
