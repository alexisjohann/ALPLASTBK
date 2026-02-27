# Fördergeber-Datenbank (Funders Database)

**Version:** 1.0.0 | **Erstellt:** 2026-01-27

---

## Übersicht

Diese Datenbank enthält strukturierte Informationen über **Fördergeber** (Funding Agencies), bei denen FehrAdvice Förderanträge stellt oder plant.

**Wichtig:** Fördergeber sind **keine Beratungskunden** wie ALPLA oder PORR. Sie sind Partner für Forschungsförderung und Innovation.

---

## Struktur

```
data/funders/
├── README.md                    # Diese Datei
└── innosuisse/                  # Innosuisse (Schweizer Innovationsagentur)
    ├── innosuisse_profile.yaml      # Organisationsprofil
    ├── innosuisse_programs.yaml     # Förderprogramme
    ├── innosuisse_requirements.yaml # Anforderungen & Checklisten
    └── innosuisse_projects.yaml     # Unsere Projekte
```

---

## Unterschied: Fördergeber vs. Kunden

| Aspekt | Fördergeber (`data/funders/`) | Kunden (`data/customers/`) |
|--------|-------------------------------|----------------------------|
| **Beziehung** | Wir beantragen Förderung | Wir beraten sie |
| **Beispiele** | Innosuisse, SNF, EU | ALPLA, PORR, LUKB |
| **Dateien** | Profile, Programme, Anforderungen, Projekte | Profile, Modelle, Szenarien, KPIs |
| **Ziel** | Fördergelder erhalten | Beratungsmandate ausführen |

---

## Aktive Fördergeber

| Fördergeber | Status | Aktive Projekte |
|-------------|--------|-----------------|
| **Innosuisse** | AKTIV | 1 (BEATRIX) |

---

## Geplante Fördergeber (Erweiterung möglich)

- **SNF** (Schweizerischer Nationalfonds) - Grundlagenforschung
- **EU Horizon** - Europäische Forschungsförderung
- **Hasler Stiftung** - IT-Forschung
- **Gebert Rüf Stiftung** - Innovation

---

## Verwendung

### Neuen Antrag vorbereiten

```bash
# 1. Fördergeber-Profil lesen
cat data/funders/innosuisse/innosuisse_profile.yaml

# 2. Passendes Programm identifizieren
cat data/funders/innosuisse/innosuisse_programs.yaml

# 3. Anforderungen prüfen
cat data/funders/innosuisse/innosuisse_requirements.yaml

# 4. Projekt dokumentieren
# → data/funders/innosuisse/innosuisse_projects.yaml aktualisieren
```

### Neuen Fördergeber hinzufügen

```bash
# 1. Verzeichnis erstellen
mkdir data/funders/<funder_name>/

# 2. Dateien anlegen (Vorlage: innosuisse/)
# - <funder>_profile.yaml
# - <funder>_programs.yaml
# - <funder>_requirements.yaml
# - <funder>_projects.yaml
```

---

## Verknüpfung mit anderen Datenbanken

| Datenbank | Verknüpfung |
|-----------|-------------|
| `data/projects/` | Detaillierte Projektdokumentation |
| `docs/funding/` | Antragstexte und Strategie-Dokumente |
| `data/model-building-session.yaml` | EBF-Sessions für Projekte |

---

## Changelog

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.0.0 | 2026-01-27 | Initiale Erstellung mit Innosuisse |

---

*Maintainer: Strategic Analysis Team*
