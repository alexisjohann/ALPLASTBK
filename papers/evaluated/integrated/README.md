# Full-Text Paper Intake Directory

> **Upload Location** for paper full-texts (PDF uploads + text entry on GitHub).
> Only files registered in `fulltext-intake.yaml` will be processed.

---

## How to Add a Paper

1. **Upload PDF** or **create text file** directly on GitHub in this directory
2. Add an entry in `fulltext-intake.yaml` with `status: pending`
3. Claude processes pending entries via `/integrate-paper`
4. Processed content moves to SSOT:
   - `data/paper-texts/PAP-{key}.md` (full-text)
   - `data/paper-references/PAP-{key}.yaml` (metadata)
   - `bibliography/bcm_master.bib` (bibliography)

## Manifest: fulltext-intake.yaml

The manifest is the **gate** — only registered files get analyzed.

```
fulltext-intake.yaml
├── status: pending     → waiting for processing
├── status: processing  → currently being analyzed
├── status: done        → moved to SSOT
└── status: skipped     → not a paper / duplicate
```

## SSOT Architecture

```
THIS DIRECTORY (INTAKE):
papers/evaluated/integrated/  ← Upload PDFs + text here

MANIFEST (GATE):
papers/evaluated/integrated/fulltext-intake.yaml  ← Register here

PROCESSED (SSOT):
data/paper-references/PAP-{key}.yaml  ← Metadata
data/paper-texts/PAP-{key}.md         ← Full-text (Markdown)
bibliography/bcm_master.bib           ← BibTeX
```

## Legacy: PAP-*.txt Templates

336 PAP-*.txt L1 templates remain in this directory (migrated to SSOT on 2026-02-01).
They are NOT listed in the manifest. See migration details:

| Status | Count |
|--------|-------|
| Templates migrated | 285 |
| YAML not found | 45 |
| Parse failed | 6 |

---

*Established: 2026-02-08 | Manifest: fulltext-intake.yaml*
