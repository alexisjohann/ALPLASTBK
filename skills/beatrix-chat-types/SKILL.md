# BEATRIX Chat-Types Skill

## Trigger
Use this skill when:
- Working on BEATRIX frontend or backend
- Discussing chat session types
- Implementing intent routing
- Updating labels or keywords for chat modes

## Overview

BEATRIX has **6 chat session types** that determine how the system behaves:

| Key | Label | Icon | Purpose |
|-----|-------|------|---------|
| `lead` | Pipeline | 🎯 | Akquise & Neugeschäft – neuer Kontakt, Anfrage, Angebot |
| `project` | Mandat | 📋 | Aktive Kundenprojekte – Auftrag erteilt, Arbeit läuft |
| `model` | Modell | 🔬 | BCM-Modellierung – Axiome, Interventionen designen |
| `context` | Kontext Ψ | 🧠 | Situationsanalyse – 8 Ψ-Dimensionen, Stakeholder |
| `research` | Literatur | 📚 | Akademische Recherche – Paper, Studien, KB/RAG |
| `general` | Fragen | 💬 | Alles andere – schnelle Antworten, Hilfe |

## Key Distinctions

**Pipeline → Mandat:** "Noch kein Auftrag" vs "Auftrag erteilt"
**Modell ↔ Kontext Ψ:** "Intervention bauen" vs "Situation verstehen"
**Literatur:** Immer wenn Paper/Studien/Theorie im Fokus

## Architecture

### Master Definition
```
GitHub: FehrAdvice-Partners-AG/complementarity-context-framework
Path: data/beatrix/chat-types.yaml
```

### Frontend (Vercel)
- `SESSION_TYPES` object in index.html
- Session Type Picker with tooltips
- Badge display in chat header

### Backend (Railway)
- `INTENT_ROUTER_SYSTEM` prompt
- `INTENT_TO_SESSION_TYPE` mapping
- `get_session_type()` function

## Intent Mapping

Backend intents map to frontend session types:

```python
INTENT_TO_SESSION_TYPE = {
    "lead": "lead",        # Pipeline
    "project": "project",  # Mandat
    "company": "lead",     # Teil der Pipeline
    "task": "project",     # Tasks gehören zu Mandaten
    "model": "model",      # Modell
    "context": "context",  # Kontext Ψ
    "knowledge": "research", # Literatur
    "general": "general",  # Fragen
}
```

## Keywords per Type

### Pipeline (lead)
lead, anfrage, akquise, prospect, angebot, pitch, neugeschäft, offerte, präsentation, erstgespräch, kontakt

### Mandat (project)
projekt, mandat, kunde, auftrag, deliverable, timeline, milestone, workshop, lieferung, abschluss

### Modell (model)
modell, bcm, axiom, intervention, nudge, design, bauen, behavior, verhalten, change, wirkung

### Kontext Ψ (context)
kontext, psi, dimension, situation, zielgruppe, analyse, umfeld, stakeholder, kultur, umgebung, einfluss

### Literatur (research)
paper, studie, literatur, forschung, theorie, quelle, evidenz, autor, referenz, zitat, beleg, nachweis

### Fragen (general)
frage, was ist, erkläre, hilfe, allgemein, wie geht, kannst du

## Files to Modify

| Change | File | Location |
|--------|------|----------|
| Labels/Icons | index.html | `SESSION_TYPES` object |
| Intent keywords | server.py | `INTENT_ROUTER_SYSTEM` |
| Type mapping | server.py | `INTENT_TO_SESSION_TYPE` |
| Master definition | chat-types.yaml | GitHub data/beatrix/ |

## Related Skills
- `fehradvice-docx` – Corporate Design documents
- `bcm2-psi-context` – 8 Ψ-Dimensions framework
