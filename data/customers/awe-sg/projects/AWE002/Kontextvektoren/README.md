# AWE002 Kontextvektoren — Energiekonzept St. Gallen

> CVA-Stufe: **STANDARD** (386 Faktoren, Ziel: 400)

## Übersicht

| # | Vektor | Datei | Ebene | Faktoren | Dimensionen/Segmente |
|---|--------|-------|-------|----------|----------------------|
| 00 | Projektvektor | `CV_AWE002_00_projektvektor.yaml` | Projekt | 110 | 9 Dimensionen |
| 01 | Unternehmensvektor | `CV_AWE002_01_unternehmen.yaml` | Organisation | 89 | 9 Dimensionen |
| 02 | Kantonsvektor | `CV_AWE002_02_kanton_sg.yaml` | Kanton | 61 | 8 Dimensionen |
| 03 | Mobilitätsvektor | `CV_AWE002_03_mobilitaet_sg.yaml` | Kanton (M2) | 42 | 7 Dimensionen |
| 10 | Segmente M1 Heizen | `CV_AWE002_10_segmente_m1_heizen.yaml` | Segment | 48 | 4 Segmente |
| 11 | Segmente M2 Mobilität | `CV_AWE002_11_segmente_m2_mobilitaet.yaml` | Segment | 36 | 3 Segmente |
| | **Total** | | **4 Ebenen** | **386** | **33 Dim. + 7 Seg.** |

## EBF-Mapping

Alle Faktoren enthalten EBF-Felder:
- `psi_dimension`: Psi-Dimensionen (Psi_I, Psi_S, Psi_C, Psi_K, Psi_E, Psi_T, Psi_M, Psi_F)
- `core_10c`: 10C CORE-Dimensionen (WHO, WHAT, HOW, WHEN, WHERE, AWARE, READY, STAGE, HIERARCHY)

Enrichment-Script: `python scripts/enrich_cv_with_ebf.py` (CV 00-02)

Segment-Vektoren (CV 10-11) enthalten zusätzlich Verhaltensparameter:
- `lambda`: Loss Aversion (1.8–2.8)
- `beta`: Present Bias (0.55–0.85)
- `kappa`: Status-Quo-Bias (0.40–0.92)

## Quellen

| Datei | Ursprung |
|-------|----------|
| `AWE001_Projektvektor_2026-02-25.xlsx` | Projektseitige Kontextanalyse |
| `AWE_Unternehemen_Kontextvektor.xlsx` | Organisationsanalyse AWE SG |
| `SG_Kanton_Kontextvektor.xlsx` | Kantonaler Energierahmen |
| Projektplan + Offerte | Grundlage für CV 03, 10, 11 |

Konvertierung Excel → YAML: `python scripts/convert_excel_to_cv_yaml.py` (openpyxl)

## Dimensionen nach Ebene

### 00 Projektvektor (110 Faktoren, 9 Dimensionen)

| # | Dimension | Faktoren | ID-Bereich |
|---|-----------|----------|------------|
| 1 | Projektmandat & Zielarchitektur | 9 | AWE-P-F01 – F09 |
| 2 | Wirkungs- & Erfolgsmesslogik | 10 | AWE-P-F10 – F19 |
| 3 | Problem- & Verhaltensstruktur | 13 | AWE-P-F20 – F32 |
| 4 | Akteurs- & Stakeholderstruktur | 13 | AWE-P-F33 – F45 |
| 5 | Institutionelle & regulatorische Rahmenbedingungen | 10 | AWE-P-F46 – F55 |
| 6 | Markt- & Systemrestriktionen | 13 | AWE-P-F56 – F68 |
| 7 | Ressourcen- & Organisationsstruktur (intern) | 14 | AWE-P-F69 – F82 |
| 8 | Zeitliche Dynamik & Sequenzierung | 15 | AWE-P-F83 – F97 |
| 9 | Unsicherheits- & Legitimationsdimension | 13 | AWE-P-F98 – F110 |

### 01 Unternehmensvektor (89 Faktoren, 9 Dimensionen)

| # | Dimension | Faktoren | ID-Präfix |
|---|-----------|----------|-----------|
| 1 | Institutionelle Legitimation & Mandat | 8 | AWE-ULM |
| 2 | Strategische Zielarchitektur | 9 | AWE-SZA |
| 3 | Politische Macht- & Abhängigkeitsstruktur | 10 | AWE-PMA |
| 4 | Organisations- & Entscheidungsstruktur | 8 | AWE-OES |
| 5 | Operative Leistungsfähigkeit | 10 | AWE-OL |
| 6 | Ressourcen- & Kompetenzbasis | 10 | AWE-RKB |
| 7 | Instrumente & faktische Einflussreichweite | 10 | AWE-IFI |
| 8 | Externe Koordinations- & Netzwerkstruktur | 11 | AWE-EKN |
| 9 | Organisationskultur & Legitimitätsposition | 13 | AWE-OKL |

### 02 Kantonsvektor St. Gallen (61 Faktoren, 8 Dimensionen)

| # | Dimension | Faktoren | ID-Präfix |
|---|-----------|----------|-----------|
| 1 | Governance- und Regulierungsarchitektur | 7 | SG-GOV |
| 2 | Energiesystem- und Infrastrukturstruktur | 7 | SG-ENE |
| 3 | Markt- und Preisstruktur | 12 | SG-MKT |
| 4 | Soziale Entscheidungs- und Vergleichsstruktur | 6 | SG-SOC |
| 5 | Institutionelle Umsetzungskapazität | 7 | SG-UMS |
| 6 | Unsicherheits- und Erwartungsstruktur | 7 | SG-UNS |
| 7 | Transformations- und Systemdynamik | 7 | SG-TRF |
| 8 | Raum- und Geografiestruktur | 8 | SG-RAU |

### 03 Mobilitätsvektor St. Gallen (42 Faktoren, 7 Dimensionen)

| # | Dimension | Faktoren | ID-Präfix |
|---|-----------|----------|-----------|
| 1 | Modal Split & Pendlerstruktur | 7 | SG-MOB-F01–F07 |
| 2 | ÖV-System & Angebotsstruktur | 6 | SG-MOB-F08–F13 |
| 3 | E-Mobilität & Ladeinfrastruktur | 6 | SG-MOB-F14–F19 |
| 4 | Arbeitgeber & betriebliche Mobilität | 6 | SG-MOB-F20–F25 |
| 5 | Verhaltensbarrieren & Habits | 6 | SG-MOB-F26–F31 |
| 6 | Siedlungsstruktur & Erreichbarkeit | 5 | SG-MOB-F32–F36 |
| 7 | Kommunikation & Anreize | 6 | SG-MOB-F37–F42 |

### 10 Segment-Vektoren M1: Erneuerbar Heizen (48 Faktoren, 4 Segmente)

| # | Segment | Faktoren | ID-Präfix |
|---|---------|----------|-----------|
| 1 | EFH-Eigentümer | 12 | SEG-M1-EFH |
| 2 | MFH-Eigentümer & STWE | 12 | SEG-M1-MFH |
| 3 | Industrie & Gewerbe | 12 | SEG-M1-IND |
| 4 | Installateure & Heizungsfachleute | 12 | SEG-M1-INST |

### 11 Segment-Vektoren M2: Mobilität (36 Faktoren, 3 Segmente)

| # | Segment | Faktoren | ID-Präfix |
|---|---------|----------|-----------|
| 1 | Auto-Pendler (MIV-Abhängige) | 12 | SEG-M2-PEN |
| 2 | KMU & Arbeitgeber | 12 | SEG-M2-KMU |
| 3 | Gemeinden & Planungsbehörden | 12 | SEG-M2-GEM |

## YAML-Struktur

### Kontextvektoren (CV 00–03)

```yaml
- id: AWE-P-F01                    # Eindeutige Faktor-ID
  dimension: Projektmandat & ...    # Zugehörige Dimension
  faktor: Formales Mandat & ...     # Faktorname
  definition: ...                   # Was wird gemessen
  kontext: ...                      # Projektspezifischer Kontext
  salienz: 0.95                     # Relevanz (0–1)
  indikator: ...                    # Operationalisierung
  gruende: ...                      # 3 Gründe für den Datenpunkt
  datenpunkt: ...                   # Aktueller Datenpunkt
  trend: stabil                     # stabil | steigend | fallend | volatil
  unsicherheit: niedrig             # niedrig | mittel | hoch
  risiko_chance: Chance             # Risiko | Chance | beides
  staerke_schwaeche: Stärke         # Stärke | Schwäche | neutral
  beeinflussbarkeit: niedrig        # niedrig | mittel | hoch | gering
  psi_dimension: [Psi_C, Psi_S]    # EBF Psi-Dimensionen
  core_10c: [WHAT, AWARE]           # EBF 10C CORE
```

### Segment-Vektoren (CV 10–11)

```yaml
- id: SEG-M1-EFH-01                # Segment-Faktor-ID
  segment: EFH-Eigentümer           # Zielgruppen-Segment
  faktor: Status-Quo-Bias ...       # Verhaltensfaktor
  definition: ...                   # Was wird gemessen
  kontext: ...                      # SG-spezifischer Kontext
  salienz: 0.95                     # Relevanz (0–1)
  behavioral_parameter: ...         # Verhaltensbeschreibung
  lambda: 2.25                      # Loss Aversion
  beta: 0.78                        # Present Bias
  kappa: 0.65                       # Status-Quo-Bias
  psi_dimension: [Psi_C, Psi_T]    # EBF Psi-Dimensionen
  core_10c: [WHAT, STAGE]           # EBF 10C CORE
```

## Nächste Schritte (Richtung 400+ Faktoren)

- [x] Psi-Dimensionen explizit zuordnen (Psi_I, Psi_S, Psi_K, etc.)
- [x] 10C-CORE-Mapping pro Faktor
- [x] Mobilitäts-Kontextvektor für Modul 2
- [x] Segment-Verhaltensprofile M1 (EFH, MFH, Industrie, Installateure)
- [x] Segment-Verhaltensprofile M2 (Pendler, KMU, Gemeinden)
- [ ] Verhaltensökonomische Mikro-Faktoren (BCM2-Mapping)
- [ ] Cross-Referenzen zu `data/dr-datareq/sources/context/ch/`
- [ ] Fehlende Ebene: Gemeinde/Quartier (optional, +14 Faktoren = 400)

---

*Erstellt: 2026-02-25 | Konvertierung: `scripts/convert_excel_to_cv_yaml.py` | EBF-Enrichment: `scripts/enrich_cv_with_ebf.py`*
