# APE – Autonomous Policy Evaluation Papers

## Quelle / Source

**Project:** APE (Autonomous Policy Evaluation)  
**Institution:** Social Catalyst Lab, Department of Economics, University of Zurich  
**Lead Researcher:** Prof. David Yanagizawa-Drott  
**Website:** https://ape.socialcatalystlab.org/  
**GitHub:** https://github.com/SocialCatalystLab/ape-papers  
**Lizenz:** Research and educational purposes (see original repository)

## Zitation / Citation

> APE Research Project. "Autonomous Policy Evaluation." Social Catalyst Lab, 
> Department of Economics, University of Zurich. 
> Led by Prof. David Yanagizawa-Drott. 2026.
> https://ape.socialcatalystlab.org/

## Beschreibung / Description

APE ist ein Experiment zur autonomen wissenschaftlichen Forschung. KI-Agenten:
- Identifizieren Policy-Fragen mit glaubwürdigen Identifikationsstrategien
- Beschaffen reale Daten aus öffentlichen APIs (Census, BLS, FRED, etc.)
- Führen ökonometrische Analysen durch (Difference-in-Differences, RDD, etc.)
- Schreiben komplette Forschungspapiere
- Durchlaufen Multi-Modell Peer Review

Alle Papers werden in einem Tournament-System bewertet, in dem LLM-Richter 
sie Head-to-Head gegen publizierte AER/AEJ-Forschung vergleichen.

## Integration in BEATRIX

Dieser Katalog wurde am 2026-02-12 automatisch in die BEATRIX-Wissensdatenbank 
integriert. Die Original-Papers, Code und Daten sind im APE GitHub Repository 
verfügbar. Hier werden nur Metadaten und Katalog-Informationen gespeichert.

## Statistik

- **Papers gesamt:** 119
- **Methoden:** DiD (75), RDD (29), Andere (15)
- **Authoring Models:** Claude Opus 4.5 (56), Claude Opus 4.6 (10), Andere (53)
- **Zeitraum:** Januar - Februar 2026

## Paper-Struktur im Original-Repo

```
apep_XXXX/v1/
├── paper.pdf           # Finales PDF
├── paper.tex           # LaTeX-Quelle
├── metadata.json       # Metadaten
├── initial_plan.md     # Forschungsplan (gesperrt nach Erstellung)
├── research_plan.md    # Finaler Forschungsplan
├── code/               # R-Analyse-Skripte
├── data/               # Replikationsdaten
├── figures/            # Generierte Abbildungen
├── review_*.md         # Multi-Modell Reviews
├── revision_plan_*.md  # Revisionsplan
├── reply_to_reviewers_*.md  # Antwort an Reviewer
└── scan_report.json    # Integritäts-Check
```
