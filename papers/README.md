# Papers Directory [MIGRATED]

> **MIGRATION COMPLETE**: All paper content has been migrated to the SSOT Architecture.
>
> **Migration Date:** 2026-02-01

---

## SSOT Architecture (New Structure)

```
data/paper-references/PAP-{key}.yaml  ← SINGLE SOURCE OF TRUTH
  └── All metadata, EBF fields, prior_score, summary

data/paper-texts/PAP-{key}.md  ← FULL-TEXT CONTAINER
  └── Complete paper text (L0-L3 Content Levels)

bibliography/bcm_master.bib  ← GENERATED OUTPUT
  └── Generated from YAML for LaTeX compilation
```

## Subdirectories Status

| Directory | Status | New Location |
|-----------|--------|--------------|
| `papers/fulltext/` | **DEPRECATED** | `data/paper-texts/` |
| `papers/evaluated/integrated/` | **DEPRECATED** | `data/paper-references/*.yaml` (summary section) |
| `papers/inbox/` | Active | For new unprocessed papers |

## Migration Statistics

| Content | Count | Migrated |
|---------|-------|----------|
| Full-text papers | 8 | `data/paper-texts/` |
| L1/L2 templates | 285 | `data/paper-references/*.yaml` |
| YAML files total | 2,530 | `data/paper-references/` |

## DO NOT ADD NEW FILES HERE

For new papers, use the Paper Intake Protocol:
1. Create `data/paper-references/PAP-{key}.yaml`
2. If full-text available: `data/paper-texts/PAP-{key}.md`
3. Run `/integrate-paper` or `/add-paper` skills

---

*Migrated: 2026-02-01 | See Appendix BM for formal documentation*
