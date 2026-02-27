# Paper Full-Text Archive

> **PERMANENT LOCATION** - This directory structure MUST NOT change.
> Established: 2026-01-31

## Purpose

This directory stores the **complete full text** of scientific papers integrated into the EBF framework.

## SSOT Architecture

```
PRIMÄR (SSOT):
data/paper-references/PAP-{key}.yaml  ← All metadata + prior_score + EBF fields

FULL-TEXT CONTAINER:
data/paper-texts/PAP-{key}.md  ← Full-text (supports L0-L3 Content Levels)

GENERATED OUTPUT (for LaTeX compilation):
bibliography/bcm_master.bib  ← Generated FROM YAML, not source
```

## Directory Structure

```
data/paper-texts/
├── README.md                              ← This documentation
├── inbox/                                 ← Drop-zone for direct GitHub uploads
│   ├── README.md                          ← Upload instructions
│   └── .gitkeep                           ← Keeps directory in git
└── PAP-{bibtex_key}.md                    ← Full text per paper
```

## Naming Convention

**CRITICAL**: File names follow the pattern:
```
PAP-{bibtex_key}.md
```

Where `{bibtex_key}` matches the key in `bibliography/bcm_master.bib`.

**Examples:**
- `PAP-efferson2022superadditive.md`
- `PAP-fehr1999theory.md`
- `PAP-kahneman1979prospectprospect.md`

## File Format

Each `.md` file contains:

```markdown
# {Paper Title}

**Authors:** {Author list}
**Year:** {Year}
**Journal:** {Journal}
**DOI:** {DOI if available}

---

## Abstract

{Abstract text}

## 1. Introduction

{Section text}

## 2. {Next Section}

{Section text}

...

## References

{Reference list from paper}
```

## Content Level (L0-L3)

The 2D Classification System from Appendix BM defines four Content Levels:

| Level | Content | Typical Size | Evidence Source | Confidence ρ |
|-------|---------|--------------|-----------------|--------------|
| L0 | Metadata only | ~500 chars | BibTeX/DOI | 0.6 |
| L1 | + Abstract | 2-5k chars | DOI lookup | 0.8 |
| L2 | + Key sections | 10-30k chars | PDF extraction | 0.95 |
| L3 | Complete text | 50-150k chars | Full PDF/OCR | 1.0 |

Higher Content Levels improve Prior Score accuracy:
- **L3** enables precise parameter extraction
- **L3** allows accurate theory support identification
- **L3** improves 10C mapping accuracy

## Connection to Paper-References

The YAML file in `data/paper-references/PAP-{key}.yaml` references this full text:

```yaml
full_text:
  available: true
  path: "data/paper-texts/PAP-{key}.md"
  format: "markdown"
  content_level: L2
  character_count: 25000
  archived_date: "2026-02-01"
```

## Rules

1. **IMMUTABLE PATH**: This directory location (`data/paper-texts/`) MUST NOT change
2. **NAMING CONVENTION**: File names MUST follow `PAP-{bibtex_key}.md` pattern
3. **FORMAT**: Files MUST be Markdown (`.md`)
4. **COMPLETENESS**: Full text means the ENTIRE paper content (see Completeness Requirements below)
5. **COPYRIGHT**: Only papers with appropriate permissions (open access, author permission, fair use for research)

## Completeness Requirements (CRITICAL)

**PROBLEM (2026-02-07):** ~65% of existing files are structured summaries, not complete papers.
These summaries omit the References section, losing the most valuable bibliographic data.

**NEW RULE (ENFORCED):** A file is only `content_level: L3` if ALL of the following are true:

| Requirement | Check | Why |
|-------------|-------|-----|
| **R1: Complete text** | All sections from original paper present | No content loss |
| **R2: References section** | `## References` with all cited works | Enables reference mining |
| **R3: Minimum length** | >10,000 words for journal articles, >5,000 for short papers | Summaries are typically <3,000 words |
| **R4: No EBF-added sections** | No "Key Parameters Extracted", "EBF Framework Relevance" | These indicate a summary, not original text |

**Content Level Classification (STRICT):**

| Level | What it means | Minimum requirements |
|-------|---------------|---------------------|
| **L0** | Metadata only | BibTeX entry exists |
| **L1** | Abstract known | Abstract + research question identifiable |
| **L2** | Key sections available | Abstract + Methodology + Findings, but NOT complete text |
| **L3** | COMPLETE original text | R1 + R2 + R3 + R4 ALL satisfied |

**CRITICAL:** A structured summary with "EBF Framework Relevance" section is **L2, NOT L3**.

**Validation:** `python scripts/validate_fulltext_completeness.py`

### What to do when integrating a new paper:

```
1. If you have the COMPLETE PDF/text:
   → Save ENTIRE content as PAP-{key}.md
   → Include ALL sections, especially References
   → Set content_level: L3
   → Do NOT add EBF integration sections to the full-text file
   → EBF metadata goes in PAP-{key}.yaml, NOT in the .md file

2. If you only have a summary/extract:
   → Save as PAP-{key}.md (still valuable!)
   → Set content_level: L2 (NOT L3!)
   → Mark abstract_source: summary

3. If you only have the abstract:
   → Do NOT create a .md file
   → Put abstract in PAP-{key}.yaml
   → Set content_level: L1
```

### Separation of Concerns (CRITICAL)

```
PAP-{key}.md    = ORIGINAL paper text (verbatim, no EBF additions)
PAP-{key}.yaml  = EBF metadata (parameters, theory_support, 10C mapping)
```

**NEVER** mix EBF framework analysis INTO the full-text file.
The .md file should be a faithful reproduction of the original paper.

## Why This Location?

- **Separation of Concerns**: Metadata in YAML, full text in Markdown
- **Scalability**: YAML files stay small and parseable
- **Searchability**: Markdown is full-text searchable via grep/Glob
- **Version Control**: Git tracks changes to paper texts
- **Permanence**: This structure is designed to never change

## Prior Score Impact

Full-text availability affects the Prior Score calculation (see Appendix BM):

```
π(p) = Σ wᵢ · gᵢ · sᵢ(p) · τ(p) · ρₖ
```

Where:
- `ρₖ` = Confidence multiplier based on Content Level
- Higher Content Level → better Supply Vector estimation → better integration decisions

## Scripts

- `scripts/compute_prior_scores.py` - Compute Prior Scores using full-text
- `scripts/migrate_bibtex_to_yaml.py` - Migrate EBF fields to YAML SSOT
- `scripts/generate_bibtex_from_yaml.py` - Generate BibTeX from YAML (planned)

## First Paper

The first paper archived here is:
- `PAP-efferson2022superadditive.md` - Efferson et al. (2022) "Superadditive cooperation"

---

*Established: 2026-01-31 | Version: 1.1 (SSOT Architecture) | DO NOT MODIFY STRUCTURE*
