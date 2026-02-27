# KI GESTALTEN, NICHT NUR NUTZEN
## Erste Bank KI-Adoption Analyse

**Session:** EBF-S-2026-01-29-ORG-001
**Projekt:** PRJ-ERS014
**Modell:** MOD-KIA-001 v2.0
**Datum:** 2026-01-29
**Modus:** STANDARD

---

## Executive Summary

| Metrik | Wert |
|--------|------|
| Baseline | 18.4% (8.650 aktive Nutzer:innen) |
| Ziel (16 Wochen) | 38.5% (18.097 aktive Nutzer:innen) |
| Delta | +20.1pp (+9.447 Nutzer:innen) |
| Konfidenz | 95% CI [+15.5pp, +24.5pp] |
| Budget | EUR 59.900 |

**Haupttreiber:**
1. Smart Defaults (27%)
2. Interaktionseffekte (20%)
3. Leadership Signaling (13%)
4. Permission Framing (12%)
5. Kompetenzaufbau (10%)

**Kritische Erfolgsfaktoren:**
- CEO-Commitment in SK/RS/RO essentiell (PDI > 85)
- Identitätsschutz VOR Defaults bei Skeptikern
- Crowding-Out vermeiden: Social + Financial nicht kombinieren

---

## 1. Ausgangslage & Fragestellung

Die Erste Bank Gruppe steht vor der Herausforderung, Microsoft Copilot bei 47.000 Mitarbeiter:innen in 7 Ländern einzuführen. Die aktuelle Adoption liegt bei 18.4%, das Ziel ist eine nachhaltige Nutzung.

**Zentrale Frage:** Wie können wir KI-Adoption verhaltensökonomisch so gestalten, dass Mitarbeiter:innen Copilot nicht nur nutzen, sondern als wertvolles Werkzeug in ihren Arbeitsalltag integrieren?

---

## 2. Kontextanalyse (5 Ebenen)

### MACRO (Länder)
- 7 Märkte mit unterschiedlichen Hofstede-Profilen
- UAI (Unsicherheitsvermeidung): 49-90 (SK niedrig, RO höchste)
- PDI (Machtdistanz): 10-99 (AT flach, SK/RS höchste)

### MESO (Organisation)
- 47.000 MA, Durchschnittsalter 42 Jahre
- George-Plattform als Digital-Erfahrung vorhanden
- Copilot-Rollout technisch abgeschlossen, Nutzung gering

### MICRO (Arbeitssituation)
- Technologie verfügbar, aber Regeln unklar
- Zeit knapp (Tagesgeschäft dominiert)
- Implizite Verbote («Darf ich das überhaupt?»)

### INDIVIDUAL (Segmente)
| Segment | Anteil | Baseline | Barrieren |
|---------|--------|----------|-----------|
| Skeptiker | 15% | 5% | Identitätsbedrohung, Kontrollverlust |
| Vorsichtige | 35% | 12% | Kompetenzangst, Prozessunsicherheit |
| Hypothetische | 30% | 8% | Implizite Verbote, fehlende Trigger |
| Enthusiasten | 20% | 65% | Fehlende Legitimation, Isolation |

### META (Choice Architecture)
- Copilot nicht als Default aktiviert
- Keine klare Permission-Kommunikation
- Führungskräfte nutzen nicht sichtbar

---

## 3. Modellspezifikation (MOD-KIA-001 v2.0)

### Formel
```
P(Adopt) = σ(β₀ + Σβᵢ·Xᵢ + Σγⱼ·(Xₐ×Xᵦ) + Ψ_Land + Ψ_Gen + Ψ_Funk)
```

### 12 Variablen
| Variable | 10C-Dim. | β | Bedeutung |
|----------|----------|---|-----------|
| D Default | WHEN | +0.86 | Copilot als Standard |
| I Identity | WHAT(X) | +0.70 | «KI macht mich besser» |
| K Kompetenz | AWARE | +0.55 | Selbstwirksamkeit |
| L Leadership | WHO | +0.54 | Führung als Vorbild |
| U Usefulness | WHAT(F) | +0.55 | Wahrgenommener Nutzen |
| P Permission | AWARE | +0.48 | «Du darfst KI nutzen» |
| T Trigger | WHEN | +0.65 | Kontextuelle Hinweise |
| N Normen | WHO | +0.42 | Soziale Normen |
| A Awareness | AWARE | +0.38 | Wissen über Existenz |
| Z Zeit | WHEN | +0.32 | Verfügbare Zeit |
| M Motivation | READY | +0.28 | Intrinsische Motivation |
| φ Phase | STAGE | var. | BCJ-Phase |

### 7 Interaktionseffekte (γ)
| Interaktion | γ | Interpretation |
|-------------|---|----------------|
| D × T | +0.60 | Default × Trigger (stärkste Synergie) |
| L × N | +0.60 | Leadership × Normen |
| K × Z | +0.50 | Kompetenz × Zeit |
| I × N | ±0.40 | Identity × Normen (VORSICHT bei Skeptikern!) |
| P × D | +0.35 | Permission × Default |
| A × K | +0.30 | Awareness × Kompetenz |
| U × T | +0.25 | Usefulness × Trigger |

---

## 4. Ergebnisse & Prognosen

### Länder-Prognosen
| Land | Baseline | Ziel W16 | Δ | Haupthebel |
|------|----------|----------|---|------------|
| 🇦🇹 AT | 22.0% | 44.5% | +22.5pp | Peer Champions |
| 🇨🇿 CZ | 16.5% | 38.0% | +21.5pp | Learning + Defaults |
| 🇸🇰 SK | 14.0% | 35.5% | +21.5pp | Leadership (+50%) |
| 🇭🇺 HU | 12.5% | 32.0% | +19.5pp | Kompetenz (+40%) |
| 🇷🇴 RO | 10.0% | 28.0% | +18.0pp | Struktur (+50%) |
| 🇭🇷 HR | 15.0% | 35.0% | +20.0pp | Team-Effekte |
| 🇷🇸 RS | 11.0% | 30.0% | +19.0pp | Leadership (+60%) |

### Segment-Beiträge
| Segment | Δ | Beitrag zum Gesamteffekt |
|---------|---|--------------------------|
| Hypothetische | +38.0pp | +11.4pp (GRÖSSTES POTENZIAL) |
| Vorsichtige | +22.5pp | +7.9pp |
| Enthusiasten | +15.0pp | +3.0pp (Multiplikator) |
| Skeptiker | +8.2pp | +1.2pp |

---

## 5. Interventions-Portfolio

### 7 Kern-Interventionen
| INT | Name | 10C-Target | Δ_expect | Budget |
|-----|------|------------|----------|--------|
| 001 | Smart Defaults | WHEN | +5.4pp | EUR 10.516 |
| 002 | Leadership Signaling | WHO | +2.6pp | EUR 11.926 |
| 003 | Permission Framing | AWARE | +2.4pp | EUR 6.917 |
| 004 | Augmentation Narrative | WHAT(X) | +2.8pp | EUR 4.161 |
| 005 | Micro-Learning | AWARE | +2.2pp | EUR 13.268 |
| 006 | Peer Champions | WHO | +2.1pp | EUR 6.077 |
| 007 | Trigger-Momente | WHEN | +2.6pp | EUR 2.007 |

### Segment-spezifische Bundles
- **Skeptiker:** Identity → Defaults (Opt-out) → Learning (freiwillig)
- **Vorsichtige:** Permission + Learning + Leadership parallel
- **Hypothetische:** Permission + Defaults SOFORT → Quick Win!
- **Enthusiasten:** Champion-Rolle geben → Multiplikator aktivieren

---

## 6. Länder-spezifische Szenarien

### Kulturelle Anpassungen
| Land | UAI | PDI | Anpassung |
|------|-----|-----|-----------|
| 🇦🇹 AT | 68 | 10 | Peers +20%, Leadership -20% |
| 🇨🇿 CZ | 74 | 55 | Default +20%, Learning +20% |
| 🇸🇰 SK | 49 | 99 | Leadership +50%, Peers -30% |
| 🇭🇺 HU | 80 | 48 | Learning +40%, Identity +20% |
| 🇷🇴 RO | 90 | 89 | Struktur +50%, Zertifikate |
| 🇭🇷 HR | 77 | 73 | Leadership +35%, Team-Fokus |
| 🇷🇸 RS | 87 | 88 | Leadership +60%, Peers -50% |

---

## 7. KPI-Metriken

### Primäre KPIs (alle Länder)
- K1: Adoption Rate
- K2: Nutzungsfrequenz
- K3: Feature-Tiefe
- K4: Sentiment-Score
- K5: Kompetenz-Index

### Alert-Schwellen
| Land | Woche 4 | Woche 8 | Woche 12 |
|------|---------|---------|----------|
| 🇸🇰 SK | K9 < 1.5x ⚠️ | K9 < 1.5x ⚠️ | K1 < 28% |
| 🇷🇸 RS | K9 < 2.0x ⚠️ | K9 < 1.8x ⚠️ | K1 < 24% |
| 🇷🇴 RO | K9 < 1.8x ⚠️ | K1 < 15% ⚠️ | K1 < 22% |

---

## 8. Budget-Allokation

### Verteilung nach Land
| Land | Budget | Schwerpunkt |
|------|--------|-------------|
| 🇦🇹 AT | EUR 9.015 | Peer Champions (35%) |
| 🇨🇿 CZ | EUR 10.482 | Learning (30%) + Defaults (25%) |
| 🇸🇰 SK | EUR 5.931 | Leadership (40%) + Permission (25%) |
| 🇭🇺 HU | EUR 7.069 | Learning (35%) + Identity (25%) |
| 🇷🇴 RO | EUR 10.422 | Defaults (25%) + Learning (25%) |
| 🇭🇷 HR | EUR 5.811 | Leadership (25%) + Defaults (20%) |
| 🇷🇸 RS | EUR 6.140 | Leadership (45%) + Permission (25%) |
| Reserve | EUR 5.030 | Unvorhergesehenes |

---

## 9. Kommunikationsstrategien

### Länder-Matrix
| Land | Sprache | Tonalität | Absender | Framing |
|------|---------|-----------|----------|---------|
| 🇦🇹 AT | Deutsch | Kollegial | Peers+BR | Partizipativ |
| 🇨🇿 CZ | Tschechisch | Professionell | FK+HR | Kompetenz |
| 🇸🇰 SK | Slowakisch | Direktiv | CEO! | Führungsentsch. |
| 🇭🇺 HU | Ungarisch | Ermutigend | HR+Experten | Sicherheit |
| 🇷🇴 RO | Rumänisch | Offiziell | Vorstand→ | Legitimation |
| 🇭🇷 HR | Kroatisch | Team-orient. | FK+Champions | Kollektiv |
| 🇷🇸 RS | Serbisch | Autoritativ | CEO!!! | Strateg. Entsch. |

---

## 10. Risiken & Mitigation

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| CEO-Buy-in in SK/RS/RO fehlt | 25% | -60% Effektivität | CEO-Briefings Woche 0 |
| Backfire bei Skeptikern | 15% | γ(I,N) = -0.40 | Sequenzierung einhalten |
| Crowding-Out durch Anreize | 10% | -Intrinsische Motivation | KEINE monetären Anreize |
| RO braucht mehr Zeit | 40% | Nur 22% statt 28% | Buffer/Verlängerung |

---

## 11. Empfehlungen & Nächste Schritte

### Sofort (vor Projekt-Start)
- [ ] CEO-Commitment in SK, RS, RO sichern
- [ ] Lokale Kommunikationsmaterialien erstellen (7 Sprachen)
- [ ] Champion-Rekrutierung starten (AT, CZ)
- [ ] Baseline-Messung aller KPIs

### Woche 1-4 (Phase 1)
- [ ] Augmentation Narrative ausrollen
- [ ] Permission Framing kommunizieren
- [ ] Enthusiasten als Champions aktivieren
- [ ] CEO-Videos in SK, RS, RO

### Woche 5-8 (Phase 2)
- [ ] Smart Defaults aktivieren
- [ ] Leadership Signaling sichtbar machen
- [ ] Micro-Learning starten

### Woche 9-12 (Phase 3)
- [ ] Trigger-Momente aktivieren
- [ ] Peer Champions aktiv einsetzen
- [ ] Messung durchführen

### Woche 13-16 (Phase 4)
- [ ] Playbook finalisieren
- [ ] KPIs etablieren
- [ ] Skalierungs-Roadmap
- [ ] Vorstandspräsentation

---

## Methodische Grundlagen

| Aspekt | Details |
|--------|---------|
| Framework | Evidence-Based Framework (EBF) mit 10C CORE |
| Modell | MOD-KIA-001 v2.0 (KI-Adoption Modell) |
| Methodik | LLMMC Prior + Bayesian Updating |
| Literatur | Fehr/Schmidt (1999), Akerlof/Kranton (2000), Rogers (2003), TAM (Davis 1989), Hofstede (2010) |
| Validierung | Case Registry Cross-Check, Monte Carlo (10k Draws) |

---

*Session: EBF-S-2026-01-29-ORG-001 | Projekt: PRJ-ERS014 | Modus: STANDARD*

*Generiert: 2026-01-29 | FehrAdvice & Partners AG*
