# Full Paper Text Storage [DEPRECATED]

> ⚠️ **DEPRECATED**: This directory has been superseded by `data/paper-texts/`
> as part of the SSOT (Single Source of Truth) Architecture.
>
> **New Location:** `data/paper-texts/PAP-{key}.md`
>
> All fulltext files have been migrated on 2026-02-01.
> See Appendix BM for the formal 2D Classification System.

---

## Original Purpose (Historical)

This directory stored complete paper texts for deep analysis within the EBF framework.

## Directory Structure

```
papers/fulltext/
├── README.md                          # This file
├── PAP-akerlof2000identity.txt        # Full text (when available)
├── PAP-kahneman1979prospect.txt       # Full text (when available)
└── ...
```

## Naming Convention

Files follow the BibTeX key pattern: `PAP-{author}{year}{keyword}.txt`

## Content Format

Each fulltext file should contain:

```
================================================================================
PAPER METADATA
================================================================================
BibTeX Key: PAP-xxx
Title: ...
Authors: ...
Journal: ...
Year: ...
DOI: ...
Pages: ...

================================================================================
FULL TEXT
================================================================================

[Complete paper text including all sections, equations, tables, and references]
```

## How to Add Papers

1. **Obtain legally**: Download from publisher with institutional access, or use author's preprint
2. **Convert to text**: Use PDF extraction or copy from HTML
3. **Format consistently**: Follow the template above
4. **Name correctly**: Use the BibTeX key as filename

## Integration with EBF

Full texts enable:
- Deep semantic analysis
- Parameter extraction
- Theory validation
- Cross-reference verification
- LLM-based content analysis

## Copyright Notice

Papers in this directory are for academic research purposes only.
Respect publisher copyright and licensing terms.
Prefer open-access versions or author preprints where available.

## Related Directories

- `papers/evaluated/integrated/` - Level 1/2 templates (summaries)
- `bibliography/bcm_master.bib` - BibTeX entries
- `data/theory-catalog.yaml` - Theory references
