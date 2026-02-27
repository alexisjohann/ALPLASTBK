# BEATRIX KB-Seed Pack

> **DEPRECATED seit 2026-02-15 (v2.0)**
>
> Alle Seeds wurden nach `data/knowledge/canonical/` konsolidiert.
> Neue Seeds NUR in canonical/ erstellen.
> SSOT: `data/beatrix/ssot-seed-registry.yaml` (v2.0)

---

## Warum DEPRECATED?

Zwei separate Seed-Bereiche (canonical/ + kb-seed/) verletzten das SSOT-Prinzip.
Die Inhalte divergierten bereits (z.B. BCM-Formel: canonical hatte Halluzination,
kb-seed hatte den HARD BLOCK Fix). Seit v2.0 gibt es nur noch EINEN Bereich:
`data/knowledge/canonical/`.

Die KB-Seed-Inhalte waren in fast allen Faellen besser als die Canonical-Versionen
und wurden daher als neue Canonical-Dateien uebernommen.

## Historie

BEATRIX startet mit einer **leeren Knowledge Base**. Ohne geseedete Definitionen
erfindet der Chat halluzinierte Antworten zu EBF-Kernbegriffen (z.B. "Behavioral
**Competence** Model" statt "Behavioral **Change** Model"). Diese Seeds stellen
sicher, dass die KB von Anfang an korrekte kanonische Definitionen enthaelt.

## Enthaltene Seeds (14)

### Definitionen: «Was ist X?» (6 Seeds)

| Datei | Thema | Quelle (SSOT) |
|-------|-------|----------------|
| `KB-BCM-001.md` | Behavioral Change Model (BCM) | `data/knowledge/canonical/bcm.yaml` |
| `KB-EBF-001.md` | Evidence-Based Framework (EBF) | `CLAUDE.md`, `core-framework-definition.yaml` |
| `KB-10C-001.md` | 10C CORE Framework | `docs/frameworks/core-framework-definition.yaml` |
| `KB-FEPSDE-001.md` | FEPSDE Utility-Dimensionen | `data/knowledge/canonical/bcm.yaml` |
| `KB-ARCH-001.md` | Wie BCM, EBF, BEATRIX zusammenhaengen | `terminology-registry.yaml`, `architecture.yaml` |
| `KB-MECE-001.md` | MECE-Taxonomie (6 Kategorien, 15 Konstrukte) | `quality/instruments/epistemology_mece_taxonomy.md` |

### Operationales Wissen: «Wie funktioniert X?» (8 Seeds)

| Datei | Thema | Quelle (SSOT) |
|-------|-------|----------------|
| `KB-PSI-001.md` | 8 Ψ-Dimensionen (Kontext) | `data/knowledge/canonical/psi-context.yaml` |
| `KB-COMP-001.md` | Komplementaritaet (γ-Werte) | `data/knowledge/canonical/complementarity.yaml` |
| `KB-WHERE-001.md` | Parameter Registry (BBB, 119+ Parameter) | `data/parameter-registry.yaml` |
| `KB-WORKFLOW-001.md` | Wie man BEATRIX benutzt (EBF Workflow) | `CLAUDE.md`, `architecture.yaml` |
| `KB-EIT-001.md` | Interventionen (9D-Vektor, 20-Field Schema) | `CLAUDE.md`, `intervention-schema.yaml` |
| `KB-BCM2-001.md` | Kontextdatenbank (459 Faktoren CH) | `data/dr-datareq/sources/context/ch/` |
| `KB-STAGE-001.md` | Behavioral Change Journey (BCJ Phasen) | `CLAUDE.md`, `core-framework-definition.yaml` |
| `KB-THEORY-001.md` | Theory Catalog (191 Theorien, 31 Kategorien) | `data/theory-catalog.yaml` |

## Upload-Anleitung

### Option A: BEATRIX Upload-UI (empfohlen)

1. BEATRIX Backend oeffnen: `https://bea-lab-upload-production.up.railway.app`
2. Als Admin/Researcher einloggen
3. Fuer jede Datei:
   - "Document Upload" oder "Knowledge Base" Section oeffnen
   - Datei hochladen (Markdown-Format wird unterstuetzt)
   - Tags setzen: `canonical, ssot, ebf`
   - Source-Type: `ebf_canonical` (falls verfuegbar) oder `research`
4. Upload bestaetigen

### Option B: API-Upload (programmatisch)

```bash
# Basis-URL
BASE_URL="https://bea-lab-upload-production.up.railway.app"

# Fuer jede Seed-Datei:
for file in KB-BCM-001.md KB-EBF-001.md KB-10C-001.md KB-FEPSDE-001.md KB-ARCH-001.md KB-MECE-001.md KB-PSI-001.md KB-COMP-001.md KB-WHERE-001.md KB-WORKFLOW-001.md KB-EIT-001.md KB-BCM2-001.md KB-STAGE-001.md KB-THEORY-001.md; do
  curl -X POST "$BASE_URL/api/documents/upload" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$file" \
    -F "tags=canonical,ssot,ebf" \
    -F "source_type=ebf_canonical"
done
```

**Hinweis:** Der genaue API-Endpunkt und die Authentifizierung haengen von der
aktuellen server.py-Version ab. Pruefen Sie `/api/documents/upload` oder
`/api/knowledge/upload`.

### Option C: Direkte DB-Insertion (fuer Entwickler)

Falls die Upload-UI nicht funktioniert, koennen die Seeds direkt in die
`knowledge_base` oder `documents` Tabelle der PostgreSQL-Datenbank eingefuegt
werden. Siehe `data/beatrix/bugfix-bcm-hallucination.yaml` fuer Details.

## Nach dem Upload

### Verifikation

1. Im BEATRIX-Chat fragen: **"Was ist das BCM?"**
2. Erwartete Antwort muss enthalten:
   - "Behavioral **Change** Model" (NICHT "Competence")
   - Formel: `P(Verhaltenszielaenderung) = f(Willingness, Ability, Context)`
   - 8 Psi-Dimensionen
   - Keine erfundenen Zahlen (keine "384 API-Endpoints", kein "Lambda=3.86")
3. Im BEATRIX-Chat fragen: **"Was ist das 10C Framework?"**
4. Erwartete Antwort muss die 10 COREs korrekt auflisten
5. Im BEATRIX-Chat fragen: **"Was ist Kontext im EBF?"**
6. Erwartete Antwort muss 8 Ψ-Dimensionen + PCT enthalten
7. Im BEATRIX-Chat fragen: **"Was ist Crowding-Out?"**
8. Erwartete Antwort muss γ = -0.68 (Social × Financial) enthalten
9. Im BEATRIX-Chat fragen: **"Was ist Loss Aversion?"**
10. Erwartete Antwort muss λ = 2.25 [1.5, 3.0] mit Quelle Kahneman enthalten

### Alte Halluzinationen bereinigen (optional aber empfohlen)

Falls BEATRIX bereits halluzinierte BCM-Definitionen gecacht hat:

1. PostgreSQL-Datenbank oeffnen (Railway Dashboard → Data → Query)
2. Halluzinierte Eintraege finden:
   ```sql
   SELECT id, content_preview, source_type, created_at
   FROM documents  -- oder knowledge_base, je nach Schema
   WHERE content ILIKE '%behavioral competence%'
      OR content ILIKE '%384 API%'
      OR content ILIKE '%Lambda=3.86%';
   ```
3. Alte Eintraege loeschen oder deaktivieren:
   ```sql
   DELETE FROM documents WHERE id IN (...);
   ```
4. **Wichtig:** Auch in `chat_messages` pruefen, ob alte Antworten mit
   `source_type = 'ebf_answer'` und falschem BCM-Content existieren:
   ```sql
   UPDATE chat_messages
   SET metadata = jsonb_set(metadata, '{deprecated}', 'true')
   WHERE content ILIKE '%behavioral competence%'
     AND role = 'assistant';
   ```

## Versionierung (Seed Manifest)

Jeder Seed hat einen **SHA-256 Content-Hash** im `seed-manifest.yaml`. Das BEATRIX-Frontend
kann damit pruefen, ob die hochgeladene Version noch mit der SSOT uebereinstimmt.

### Manifest generieren

```bash
# Manifest neu generieren (nach Seed-Aenderungen)
python scripts/generate_seed_manifest.py

# Pruefen ob Seeds aktuell sind (vergleicht Hashes)
python scripts/generate_seed_manifest.py --check

# JSON-Output (fuer API-Integration)
python scripts/generate_seed_manifest.py --json
```

### Wie das Frontend vergleicht

```
1. Bei Upload: BEATRIX speichert content_hash pro Seed
2. Bei Check:  BEATRIX fetcht seed-manifest.yaml aus dem Repository
3. Vergleich:  stored_hash == manifest_hash?
   → JA:  Seed ist aktuell ✅
   → NEIN: Seed ist veraltet → Re-Upload noetig ⚠️
```

### Manifest-Struktur (Beispiel)

```yaml
seeds:
  - id: "KB-BCM-001"
    file: "KB-BCM-001.md"
    content_hash: "3485a484c59f..."   # SHA-256
    title: "Das Behavioral Change Model (BCM)"
    ssot_source: "data/knowledge/canonical/bcm.yaml"
    tags: ["canonical", "bcm", "ebf", "ssot"]
    word_count: 1672
```

### API-Endpunkt (Vorschlag fuer server.py)

```python
@app.get("/api/seeds/status")
def seed_status():
    """Vergleicht gespeicherte Hashes mit aktuellem Manifest."""
    manifest = fetch_manifest_from_repo()  # oder lokale Kopie
    stored = db.query("SELECT seed_id, content_hash FROM kb_seeds")
    return {
        "up_to_date": [...],
        "outdated": [...],     # → Re-Upload noetig
        "missing": [...],      # → Noch nie hochgeladen
    }
```

## Update-Zyklus

| Frequenz | Trigger | Aktion |
|----------|---------|--------|
| Bei SSOT-Aenderung | bcm.yaml, core-framework-definition.yaml geaendert | KB-Seeds neu generieren + `generate_seed_manifest.py` ausfuehren + hochladen |
| Quartalsweise | Review | `generate_seed_manifest.py --check` ausfuehren |
| Bei neuer server.py-Version | Deployment | Pruefen ob Upload-API sich geaendert hat |

## Beziehung zu server.py Fixes

Dieses KB-Seed-Pack ist **Track 1** der BCM-Halluzinations-Behebung.
Es funktioniert SOFORT und behebt das Symptom (leere KB).

**Track 2** (server.py Aenderungen) behebt die Ursachen:
- Falscher Name im System-Prompt korrigieren
- 3x Score-Boost fuer Halluzinationen entfernen
- Automatisches KB-Seeding beim Start implementieren

Siehe `data/beatrix/bugfix-bcm-hallucination.yaml` fuer Track 2 Details.

## SSOT-Prinzip

Diese Seeds sind **abgeleitete Kopien** der kanonischen Definitionen:

```
data/knowledge/canonical/bcm.yaml             → KB-BCM-001.md
CLAUDE.md + core-framework-definition.yaml    → KB-EBF-001.md
docs/frameworks/core-framework-definition.yaml → KB-10C-001.md
data/knowledge/canonical/bcm.yaml (FEPSDE)    → KB-FEPSDE-001.md
terminology-registry.yaml + architecture.yaml → KB-ARCH-001.md
epistemology_mece_taxonomy.md                 → KB-MECE-001.md
data/knowledge/canonical/psi-context.yaml     → KB-PSI-001.md
data/knowledge/canonical/complementarity.yaml → KB-COMP-001.md
data/parameter-registry.yaml                  → KB-WHERE-001.md
CLAUDE.md + architecture.yaml                 → KB-WORKFLOW-001.md
CLAUDE.md + intervention-schema.yaml          → KB-EIT-001.md
data/dr-datareq/sources/context/ch/           → KB-BCM2-001.md
CLAUDE.md + core-framework-definition.yaml    → KB-STAGE-001.md
data/theory-catalog.yaml                      → KB-THEORY-001.md
```

**Bei Aenderungen immer zuerst die SSOT aktualisieren, dann die Seeds neu generieren!**
