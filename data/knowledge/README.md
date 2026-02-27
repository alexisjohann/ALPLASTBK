# Knowledge Base Architecture

## Retrieval Priority (SSOT)

```
Priority 1: Canonical entries       — ALWAYS wins
Priority 2: Chat-insights (tagged)  — fallback
Priority 3: LLM generation          — last resort
```

**Rule**: When a user question matches a canonical entry (by slug or alias),
the canonical answer MUST be returned. Chat-insights are NEVER authoritative
for topics covered by a canonical entry.

## Directory Structure

```
data/knowledge/
├── canonical/              ← Single Source of Truth (SSOT)
│   ├── index.yaml          ← Master index of all canonical entries
│   ├── bcm.yaml            ← KB-BCM-001: Was ist das BCM?
│   ├── complementarity.yaml← KB-COMP-001: Was ist Complementarity?
│   └── psi-context.yaml    ← KB-PSI-001: Was ist Kontext (Ψ)?
│
├── chat-insights/          ← AI-generated answers (may contain errors)
│   └── 2026-02/            ← Monthly directories
│       └── *.yaml          ← Individual chat-insight files
│
└── README.md               ← This file
```

## Canonical Entries

Canonical entries are the authoritative, human-verified answers for key EBF
topics. They are stored in `canonical/` and listed in `canonical/index.yaml`.

Each canonical entry has:
- **`ssot: true`** — Marks it as Single Source of Truth
- **`slug`** — Short identifier for matching (e.g., `bcm`)
- **`aliases`** — List of questions/phrases that trigger this entry
- **`covers_topics`** — Topics this entry is authoritative for
- **`ssot_refs`** — References to the underlying source documents

### Current Canonical Entries

| ID | Slug | Title |
|----|------|-------|
| KB-BCM-001 | `bcm` | Was ist das BCM? |
| KB-COMP-001 | `complementarity` | Was ist Complementarity? |
| KB-PSI-001 | `psi-context` | Was ist Kontext (Ψ) im EBF? |

### Planned Entries

See `canonical/index.yaml` → `planned:` section.

## Chat-Insights

Chat-insights are AI-generated answers stored during user sessions. They may
contain terminology errors or outdated information. They serve as fallback
when no canonical entry exists for a topic.

**Important**: Chat-insights are NOT authoritative. If a chat-insight
contradicts a canonical entry, the canonical entry wins.

## Validation

A validation script ensures chat-insights don't contain known terminology
errors that contradict canonical SSOTs:

```bash
# Check all chat-insights for errors
python scripts/validate_knowledge_consistency.py

# Auto-fix known errors
python scripts/validate_knowledge_consistency.py --fix

# Strict mode (exit code 1 on any error) — used in CI/CD
python scripts/validate_knowledge_consistency.py --strict
```

### What Gets Validated

- BCM name (must be "Behavioral Change Model", not "Competence" or "Context")
- FEPSDE dimensions (P=Physical, D=Digital, E=Ecological)
- Ψ-dimension symbols (Ψ_M not Ψ_Co, Ψ_K not Ψ_Cu, Ψ_F not Ψ_P)
- Ψ-dimension labels (Ψ_K=Cultural not Knowledge, Ψ_E=Economic not Environmental)
- SCARF model dimensions vs. EBF Ψ-dimensions

## Adding New Canonical Entries

1. Create a new YAML file in `canonical/` following the schema of existing entries
2. Add the entry to `canonical/index.yaml` under `entries:`
3. Run validation: `python scripts/validate_knowledge_consistency.py --strict`
4. Commit both files together

## Frontend Integration

The frontend retrieval system should:
1. Match user questions against canonical `aliases` (case-insensitive, substring)
2. If match found → return canonical answer (Priority 1)
3. If no match → fall back to chat-insights by tag matching (Priority 2)
4. If no chat-insight → generate from CLAUDE.md context (Priority 3)
