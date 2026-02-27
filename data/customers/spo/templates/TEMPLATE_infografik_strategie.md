# Template: Strategische Infografik (NotebookLM)
# ================================================
# Typ: Lieferobjekt (Infografik via NotebookLM)
# Version: 2.0
# Erstellt: 2026-02-03 | Aktualisiert: 2026-02-06
# SSOT Design System: templates/infographic-design-system.yaml
# SSOT SPÖ-Preset: templates/infographic-presets/spo.yaml
# Workflow: workflows/WORKFLOW_infographic.yaml
# Skill: /infographic --preset spo
# ================================================

## Schnellstart

```
/infographic --preset spo --thema inflation --format landscape
```

Das ist alles. Der Rest ist automatisiert.

---

## Was hat sich geändert (v1.0 → v2.0)?

| Aspekt | v1.0 (alt) | v2.0 (neu) |
|--------|------------|------------|
| **Tool** | Canva, Figma, PowerPoint | **Google NotebookLM** |
| **Farben** | #E2001A (gerundet) | **#E3000F** (exakt SPÖ-Rot) |
| **Struktur** | 5-Zonen (manuell) | **3 Format-Templates** (Landscape/Portrait/Square) |
| **QA** | 8-Punkte-Checkliste | **3-Iterationen QA-Loop mit 6-Kriterien-Scoring** |
| **Preset** | Keiner | **SPÖ-Preset mit Themen-Bibliothek** |
| **Reproduzierbarkeit** | Gering (Design-Tools) | **Hoch (Prompt = SSOT)** |
| **Verhaltensökonomie** | Nicht berücksichtigt | **6 BehavEcon-Prinzipien integriert** |

---

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│  INFOGRAPHIC SYSTEM — SPÖ                                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SSOT (global)                          SPÖ-SPEZIFISCH                  │
│  ─────────────                          ──────────────                   │
│                                                                         │
│  Design System YAML ──────────────► SPÖ Preset YAML                    │
│  (Regeln, Architektur)               (Farben, Themen, Verwundbarkeiten)│
│         │                                     │                         │
│         ▼                                     ▼                         │
│  3 Prompt Templates ◄──── befüllt mit ── SPÖ Daten                    │
│  (Landscape/Portrait/Square)                  │                         │
│         │                                     │                         │
│         ▼                                     ▼                         │
│  NotebookLM ─────────────────► Bild ─────► QA-Loop (3 Runden)         │
│                                              │                          │
│                                              ▼                          │
│                                        Score ≥ 8.5?                     │
│                                        ├── JA → Freigabe               │
│                                        └── NEIN → Neuer Prompt          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Dateien-Übersicht

### SSOT (Single Sources of Truth)

| Datei | Inhalt | Pfad |
|-------|--------|------|
| **Design System** | Farben, Typo, Icons, Layouts, BehavEcon, QA | `templates/infographic-design-system.yaml` |
| **SPÖ-Preset** | Farben, Hashtag, Ehrlichkeit, Vergleiche, Verwundbarkeiten | `templates/infographic-presets/spo.yaml` |
| **Scoring Checklist** | 6 Kriterien (K1-K6), Gewichte, Schwellenwerte | `templates/infographic-scoring-checklist.yaml` |

### Prompt Templates (Copy-Paste für NotebookLM)

| Format | Ratio | Verwendung | Pfad |
|--------|-------|------------|------|
| **Landscape** | 16:9 | Parteitag, Pressekonferenz, Desktop | `templates/notebooklm-prompt-landscape.md` |
| **Portrait** | 9:16 | Stories, Reels, Mobile, Rollups | `templates/notebooklm-prompt-portrait.md` |
| **Square** | 1:1 | Instagram, Facebook, Social Media | `templates/notebooklm-prompt-square.md` |

### SPÖ-Projekt-Dateien

| Datei | Inhalt | Pfad |
|-------|--------|------|
| **Workflow** | 6-Phasen-Workflow + Trigger | `workflows/WORKFLOW_infographic.yaml` |
| **Dieses Template** | Übersicht + Quick-Start | `templates/TEMPLATE_infografik_strategie.md` |

### Bestehende Infografiken (Pre-Workflow)

| Datei | Thema | Status |
|-------|-------|--------|
| `reports/INFOGRAFIK_basis_gesundheitsversorgung_2026-02-03.md` | Gesundheit | PRE-WORKFLOW |
| `reports/INFOGRAFIK_social_media_sog_2026-02-03.md` | SOG | PRE-WORKFLOW |
| `reports/INFOGRAFIK_spitalstouristen_2026-02-03.md` | Spitalstouristen | PRE-WORKFLOW |

---

## Format-Spezifikationen

| Eigenschaft | Landscape | Portrait | Square |
|-------------|-----------|----------|--------|
| **Pixel** | 1920 × 1080 | 1080 × 1920 | 1080 × 1080 |
| **Ratio** | 16:9 | 9:16 | 1:1 |
| **Architektur** | 3 Bänder (H/C/S) | 7 vertikale Sektionen | 2×2 Grid + H/C |
| **Farbschema** | SPÖ-Rot #E3000F, Schwarz, Weiss, Hellgrau | Gleich | Gleich |
| **Icons** | Flat Line Art, einfarbig | Gleich | Gleich |
| **Max Cluster** | 5-7 | 7 | 4+2 |

---

## SPÖ-Preset: Was ist vorausgefüllt?

### Immer vorausgefüllt (alle Themen)

| Element | Wert |
|---------|------|
| Primärfarbe | #E3000F (SPÖ-Rot) |
| Sekundärfarbe | #1A1A1A (Schwarz) |
| Hintergrund | #FFFFFF (Weiss) |
| Akzent | #F5F5F5 (Hellgrau) |
| Frame | «Ordnen statt Spalten» |
| Claim | «Ordnung wirkt.» |
| Hashtag | #OrdnenStattSpalten |
| Tonalität | Sachlich-entschlossen, nicht aggressiv |
| Quellen | Statistik Austria, Eurostat, OeNB |
| Orthografie | Jänner (nicht Januar), € (nicht EUR) |

### Pro Thema vorausgefüllt

**Inflation (KOMPLETT):**
- Killer-Zahl: -0,7% Preisrückgang (Jänner 2026)
- Secondary: 11% → 2% (Inflation 2023-2026), -4,9% Energiepreise
- 3 Massnahmen: MwSt-Senkung (1,4 Mrd.), Mietpreisbremse (300.000 HH), Anti-Shrinkflation (15.000 €)
- Vergleich: Österreich vs. Ungarn (Orbán)
- Ehrlichkeit: «Gegen die Teuerung gewinnt man nie ganz — aber man kann sie bremsen.»
- Verwundbarkeiten: VPI/HVPI (→ MoM verwenden), Basiseffekt

**Migration (TEILWEISE):**
- Killer-Zahl: 14.156 Abschiebungen 2025
- 3 Massnahmen: Schnellverfahren, Drittstaaten, Arbeitsmarkt-Integration
- Ehrlichkeit: «Migration lässt sich nicht auf null setzen — aber ordnen.»

**Gesundheit, Wohnen, Bildung, Energie:** Ehrlichkeits-Linien verfügbar.

---

## 3-Iterationen QA-Loop (PFLICHT)

```
RUNDE 1: Struktur & Vollständigkeit          Score: 6.0-7.5
  → Alles da? Layout richtig? Ehrlichkeit drin?
  → Neuer Prompt mit Fixes

RUNDE 2: Daten-Integrität & Halluzinationen   Score: 7.5-8.5
  → Zahlen korrekt? Datum richtig? Quellen echt?
  → Neuer Prompt mit Fixes

RUNDE 3: Feinschliff & Verhaltensökonomie     Score: 8.5-9.5
  → Anchoring? Framing? Inoculation? Angriffsfläche?
  → Freigabe oder Bonus-Runde

FREIGABE: Score ≥ 8.5
```

**Erfahrungswert:** Jede Runde findet ANDERE Fehler. Runde 1 allein reicht NIE.

**KRITISCH:** NotebookLM kann nicht iterieren. Jede Runde = komplett neuer Prompt!

---

## Scoring-Kriterien (6 Dimensionen)

| # | Kriterium | Gewicht | SPÖ-Fokus |
|---|-----------|---------|-----------|
| K1 | Frame-Konsistenz | 20% | «Ordnen statt Spalten» durchgängig? |
| K2 | Verhaltenswirksamkeit | 20% | Anchoring, Inoculation, Salience? |
| K3 | Angriffsfläche (inv.) | 20% | VPI/HVPI, Cherry-Picking, Basiseffekt? |
| K4 | Visuelle Klarheit | 15% | 3-Sekunden-Test bestanden? |
| K5 | Daten-Integrität | 15% | Jänner (nicht Januar)? Quellen korrekt? |
| K6 | Zielgruppen-Abdeckung | 10% | Wechselwähler-tauglich? |

---

## Axiom-Compliance

Jede Infografik wird gegen die 10 Kommunikations-Axiome geprüft:

| Axiom | Relevanz für Infografiken |
|-------|---------------------------|
| **K1** (Kickl-Differenzierung) | Keine FPÖ-Begriffe in Vergleichen |
| **K2** (Zahlen als Beleg) | Killer-Zahl + 3 Massnahmen-Zahlen |
| **K3** (Ordnung-Frame) | «Ordnung» im Header, nicht «Sicherheit» |
| **K4** (USP) | Was kann NUR die SPÖ? |
| **K9** (Populär, nicht populistisch) | Ehrlichkeits-Linie als Qualitätsgarantie |

---

## Qualitätskriterien (Kurzversion)

```
☐ Titel ist Action Title (These, nicht Beschreibung)
☐ Killer-Zahl visuell dominant (72pt Primärfarbe)
☐ Max 1 Primary + 2 Secondary Zahlen
☐ 3 Massnahmen mit konkreten Zahlen
☐ Ehrlichkeits-Linie vorhanden
☐ Vergleichstabelle mit Quellenangabe
☐ Nur 3+1 Farben (Rot, Schwarz, Weiss, Hellgrau)
☐ Flat Line Art Icons (keine Emojis, keine Fotos)
☐ Hashtag als Closer
☐ Score ≥ 8.5 nach 3 QA-Runden
```

---

## Änderungsprotokoll

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 2026-02-03 | Erstversion (5-Zonen, Canva/Figma) |
| **2.0** | **2026-02-06** | **Komplette Überarbeitung: NotebookLM, Design System, Preset, 3-Iterationen QA** |
