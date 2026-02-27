# BEATRIX KB-Seed Pack

> **Automatisches Seeding** mit Content Hash Synchronisation

## ✅ Auto-Sync Aktiv

```
GitHub SSOT geändert
       ↓
GitHub Action (sync-beatrix.yml)
       ↓
Railway Redeploy
       ↓
Content Hash Vergleich
       ↓
INSERT / UPDATE / SKIP
       ↓
✅ BEATRIX KB synchron
```

## Seed-Versionierung

### Dateien

| Datei | Zweck |
|-------|-------|
| `ssot-seed-registry.yaml` | Liste aller Seeds (path, title, tags) |
| `seed-manifest.yaml` | SHA-256 Content-Hash pro Seed |
| `generate_seed_manifest.py` | Generator-Script mit 3 Modi |

### Manifest Workflow

```
SSOT geändert → Seeds aktualisiert → generate_seed_manifest.py
                                            ↓
                                    seed-manifest.yaml
                                            ↓
                         BEATRIX vergleicht: stored_hash == manifest_hash?
                         → Match:    Seed aktuell ✅
                         → Mismatch: Re-Upload nötig ⚠️
```

### Script Verwendung

```bash
# Manifest neu generieren
python scripts/generate_seed_manifest.py

# Prüfen ob Seeds aktuell
python scripts/generate_seed_manifest.py --check

# JSON für API-Integration
python scripts/generate_seed_manifest.py --json

# In Datei speichern
python scripts/generate_seed_manifest.py -o data/beatrix/seed-manifest.yaml
```

## Aktuelle Seeds (12)

### Markdown Seeds (Human-readable)
| Seed | Pfad |
|------|------|
| BCM | `data/knowledge/canonical/BCM-Behavioral-Change-Model.md` |
| EBF | `data/knowledge/canonical/EBF-Evidence-Based-Framework.md` |
| 10C | `docs/frameworks/10C-CORE-Framework.md` |
| FEPSDE | `data/knowledge/canonical/FEPSDE-Matrix.md` |
| MECE | `data/knowledge/canonical/MECE-Taxonomy.md` |
| ARCH | `data/knowledge/canonical/BCM-EBF-BEATRIX-Architecture.md` |

### YAML Seeds (Structured)
| Seed | Pfad |
|------|------|
| BCM YAML | `data/knowledge/canonical/bcm.yaml` |
| EBF YAML | `data/knowledge/canonical/ebf.yaml` |
| Ψ-Context | `data/knowledge/canonical/psi-context.yaml` |
| Complementarity | `data/knowledge/canonical/complementarity.yaml` |
| Terminology | `data/knowledge/canonical/terminology-registry.yaml` |
| 10C YAML | `docs/frameworks/core-framework-definition.yaml` |

## Neuen Seed hinzufügen

1. **Datei erstellen** in `data/knowledge/canonical/`
2. **Registry aktualisieren** (`ssot-seed-registry.yaml`)
3. **Commit & Push** → GitHub Action triggert automatisch
4. **Manifest aktualisieren** (optional): `python scripts/generate_seed_manifest.py`

## Technische Details

| Komponente | Beschreibung |
|------------|--------------|
| Registry | `data/beatrix/ssot-seed-registry.yaml` |
| Manifest | `data/beatrix/seed-manifest.yaml` |
| GitHub Action | `.github/workflows/sync-beatrix.yml` |
| Server Code | `server.py` → `seed_ssot_knowledge_base()` |
| Hash Algo | SHA-256 (16 char prefix für DB, full für Manifest) |
| Trigger | Push auf `data/knowledge/canonical/**` |
