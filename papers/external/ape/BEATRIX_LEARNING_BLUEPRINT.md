# BEATRIX × APE: Systematisches Lern-Blueprint

## Quelle

> APE Research Project. "Autonomous Policy Evaluation."  
> Social Catalyst Lab, Department of Economics, University of Zurich.  
> Led by Prof. David Yanagizawa-Drott. 2026.  
> https://ape.socialcatalystlab.org/  
> GitHub: https://github.com/SocialCatalystLab/ape-papers

---

## 1. Was APE macht – und was BEATRIX daraus lernt

APE hat in 3 Wochen (17. Jan – 6. Feb 2026) über 188 empirische Forschungspapiere autonom produziert. Nicht Zusammenfassungen – originale Forschung mit echten Daten. Das System identifiziert Policy-Fragen, holt Daten von Census/BLS/FRED APIs, führt ökonometrische Analysen durch (DiD, RDD), schreibt LaTeX-Papers und durchläuft Multi-Modell Peer Review.

BEATRIX macht heute: Papers hochladen → klassifizieren → in Knowledge Base integrieren → per Chat abfragen.

**Der Sprung:** Von passiver Wissensorganisation zu aktiver Wissenserzeugung und -bewertung.

---

## 2. Die 7 APE-Module, die BEATRIX übernehmen kann

### Modul 1: Ideen-Generierung und Ranking

**APE-System:**
- `ideas.md` – 5-6 Forschungsideen pro Durchlauf, mit detaillierter Beschreibung
- `ideas_ranked.json` – GPT-5.2 bewertet jede Idee auf 100-Punkte-Skala
- Drei Kategorien: **PURSUE** (>65), **CONSIDER** (45-65), **SKIP** (<45)
- Bewertungskriterien: Novelty, DiD-Tauglichkeit, Datenverfügbarkeit, Power

**BEATRIX-Adaption: "Research Relevance Scorer"**

Wenn ein Paper hochgeladen wird, generiert BEATRIX nicht nur eine Klassifikation (Paper/Book/Study), sondern bewertet:

```json
{
  "relevance_score": 78,
  "recommendation": "PURSUE",
  "criteria": {
    "bcm_relevance": 85,
    "methodological_rigor": 72,
    "data_novelty": 68,
    "practical_applicability": 88
  },
  "reasoning": "Dieses Paper zu Loss Aversion in Pensionsplanung hat direkte Anwendbarkeit im FehrAdvice-Kontext..."
}
```

**Implementierung:** Erweiterung des `/api/text/analyze` Endpoints um ein Ranking-Modul.

---

### Modul 2: Forschungsplan-Struktur

**APE-Template (aus initial_plan.md):**

1. **Research Question** – Eine klare, beantwortbare Frage
2. **Policy Background** – Kontext und Relevanz
3. **Identification Strategy** – Wie wird Kausalität etabliert?
4. **Expected Effects and Mechanisms** – Hypothesen vorab formuliert
5. **Primary Specification** – Exakte statistische Methode (mit Code)
6. **Data Sources** – Wo kommen die Daten her?
7. **Planned Robustness Checks** – Vorab definierte Sensitivitätsanalysen
8. **Timeline** – Zeitplan
9. **Potential Concerns** – Bekannte Limitationen

**Schlüsselprinzip:** Der Plan wird vor der Analyse gesperrt (`LOCKED – do not modify after commit`). Git-Timestamps beweisen die Sequenz.

**BEATRIX-Adaption: "Paper Analysis Template"**

Für jedes hochgeladene Paper erstellt BEATRIX eine strukturierte Analyse nach diesem Schema:

```
papers/evaluated/integrated/{paper_id}/
├── paper.pdf                    # Original
├── metadata.json                # Basis-Metadaten
├── beatrix_analysis.md          # Strukturierte Analyse
│   ├── Research Question
│   ├── Identification Strategy
│   ├── BCM-Einordnung (Ψ-Dimensionen)
│   ├── Methodological Assessment
│   ├── Practical Applicability (FehrAdvice)
│   └── Connections to KB
└── relevance_score.json         # Scoring
```

---

### Modul 3: Multi-Modell Quality Review

**APE-System:**
- 3-4 verschiedene LLMs reviewen jedes Paper unabhängig
- Modelle: GPT-5-mini, Grok-4.1-Fast, Gemini-3-Flash, Codex-Mini
- Jeder gibt Verdict: ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT AND RESUBMIT
- Strukturierte Review-Sections:
  - Format Check
  - Statistical Methodology
  - Identification Strategy
  - Literature
  - Writing Quality
  - Constructive Suggestions

**BEATRIX-Adaption: "Dual-Review System"**

Statt nur Claude für die Analyse zu nutzen, können zwei Durchläufe mit unterschiedlichen Prompts laufen:

1. **Analytical Review** (streng, methodisch): Prüft Statistik, Identifikationsstrategie, Daten-Provenienz
2. **Practical Review** (anwendungsorientiert): Prüft FehrAdvice-Relevanz, BCM-Einordnung, Handlungsempfehlungen

Verdicts pro Paper: ⭐⭐⭐ (Core KB) / ⭐⭐ (Reference) / ⭐ (Archive)

---

### Modul 4: Integritäts-Scan (scan_report.json)

**APE-System – 6 Flag-Kategorien:**

| Kategorie | Beschreibung | Häufigkeit |
|-----------|-------------|------------|
| `METHODOLOGY_MISMATCH` | Text beschreibt andere Methode als Code ausführt | 11× |
| `HARD_CODED_RESULTS` | Ergebnisse manuell eingetragen statt aus Code generiert | 9× |
| `DATA_PROVENANCE_MISSING` | Datenquellen nicht nachvollziehbar | 8× |
| `SUSPICIOUS_TRANSFORMS` | Fragwürdige Datentransformationen | 6× |
| `SELECTIVE_REPORTING` | Ergebnisse selektiv berichtet | 4× |
| `DATA_FABRICATION` | Hinweise auf fabrizierte/simulierte Daten | 4× |

Jedes Flag hat: Severity (HIGH/MEDIUM/LOW), File, Lines, Evidence, Confidence (0-1)

Verdicts: **CLEAN** (keine HIGH flags) / **SUSPICIOUS** (mind. 1 HIGH flag)

**BEATRIX-Adaption: "Paper Integrity Check"**

Beim Upload eines Papers prüft BEATRIX automatisch auf:

1. **Claim-Data Consistency**: Stimmen die im Text genannten Zahlen mit den Tabellen überein?
2. **Methodology Clarity**: Ist die verwendete Methode klar beschrieben?
3. **Sample Description**: Sind Stichprobengröße und -auswahl transparent?
4. **Result Robustness**: Werden Sensitivitätsanalysen berichtet?
5. **Citation Completeness**: Fehlen relevante Referenzen?

Output als `integrity_check.json` mit Confidence-Scores pro Kategorie.

---

### Modul 5: Revision Chain Tracking

**APE-System:**
- Papers haben `parent` Referenzen: apep_0136 → apep_0134 → (original)
- Jede Revision hat: `revision_plan_1.md`, `reply_to_reviewers_1.md`
- Revisionsplan listet systematisch: Issue → Action → Priorität
- Revision-Tabelle:

```
| Reviewer | Decision | Key Concerns |
|----------|----------|-------------|
| GPT-5-mini | MAJOR REVISION | SCM confidence intervals |
| Grok-4.1-Fast | MINOR REVISION | Explicit SCM weights |
| Gemini-3-Flash | CONDITIONALLY ACCEPT | Synthetic DiD robustness |
```

**BEATRIX-Adaption: "Knowledge Evolution Tracking"**

Wenn ein Paper aktualisiert oder eine neue Version hochgeladen wird:
- Automatische Erkennung, ob es ein Update zu einem bestehenden Paper ist
- Diff-Tracking: Was hat sich geändert?
- Versions-History im Ordner auf GitHub
- BEATRIX-Chat kann fragen: "Was sind die Unterschiede zwischen Version 1 und 2 dieses Papers?"

---

### Modul 6: Tournament/Benchmark System

**APE-System:**
- `ranking.md` vergleicht Papers Head-to-Head mit publizierter AER/AEJ-Forschung
- Scoring auf 100-Punkte-Skala mit detaillierten Kriterien
- Novelty Assessment: High/Moderate/Low
- DiD/RDD-spezifische Bewertung (Pre-treatment periods, Selection into treatment, etc.)

**BEATRIX-Adaption: "KB Quality Dashboard"**

Monatlicher automatischer Report:
- Top 10 Papers nach Relevance Score
- Methodologische Verteilung (wie viele DiD, RDD, RCT, etc.)
- Abdeckungs-Gaps: Welche BCM-Dimensionen sind unterrepräsentiert?
- Trend: Wie entwickelt sich die KB-Qualität über die Zeit?

---

### Modul 7: Automatische Daten-Beschaffung

**APE-System:**
- R-Skripte holen automatisch Daten von Census, BLS, FRED APIs
- `01_fetch_data.R` → `02_analysis.R` → `03_figures.R`
- Cached data files für Replikation

**BEATRIX-Adaption: "Evidence Connector"**

Langfristig: BEATRIX verbindet Papers mit echten Datenquellen:
- Semantic Scholar API für Zitationsdaten
- OpenAlex für Open-Access-Versionen
- CrossRef für DOI-Resolution
- SSRN für Working Papers
- Google Scholar für Impact-Metriken

---

## 3. Priorisierte Implementierungs-Roadmap

### Phase 1: Sofort (diese Woche)
✅ **APE-Katalog importiert** – 118 Papers in BEATRIX KB
✅ **GitHub-Struktur** – `papers/external/ape/` mit README, catalog.json, CITATION.md

### Phase 2: Kurzfristig (2-4 Wochen)
- [ ] **Relevance Scorer** – Score + PURSUE/CONSIDER/SKIP für jedes hochgeladene Paper
- [ ] **Strukturierte Analyse** – Ordner-Struktur pro Paper auf GitHub (nicht nur PDF)
- [ ] **Integrity Check Light** – Basis-Qualitätsprüfung beim Upload

### Phase 3: Mittelfristig (1-3 Monate)
- [ ] **Dual-Review System** – Zwei Analyse-Durchläufe mit unterschiedlichen Perspektiven
- [ ] **KB Quality Dashboard** – Monatliche automatische Reports
- [ ] **Evidence Connector** – Semantic Scholar + CrossRef Integration

### Phase 4: Langfristig (3-6 Monate)
- [ ] **Paper Evolution Tracking** – Versioning und Diff-System
- [ ] **Autonomous Analysis** – BEATRIX generiert eigenständig BCM-Analysen neuer Papers
- [ ] **Tournament System** – Benchmark-Vergleiche innerhalb der KB

---

## 4. Technische Spezifikationen

### Relevance Scorer (Phase 2)

**Endpoint:** `POST /api/documents/{doc_id}/score`

**Prompt-Template:**
```
Du bist ein Forschungsbewerter für Behavioral Economics. 
Bewerte dieses Paper auf einer 100-Punkte-Skala:

1. BCM-Relevanz (0-25): Wie relevant für das Behavioral Complementarity Model?
2. Methodologische Rigorosität (0-25): DiD, RDD, RCT, Quasi-Experiment?
3. Daten-Novelty (0-25): Neue Datenquellen, neue Populationen, neue Kontexte?
4. Praktische Anwendbarkeit (0-25): Direkt umsetzbar für FehrAdvice-Projekte?

Gesamtscore: Summe der 4 Dimensionen
Empfehlung: PURSUE (>65), CONSIDER (45-65), SKIP (<45)
```

**Response-Format:**
```json
{
  "score": 78,
  "recommendation": "PURSUE",
  "dimensions": {
    "bcm_relevance": { "score": 22, "reasoning": "..." },
    "methodological_rigor": { "score": 18, "reasoning": "..." },
    "data_novelty": { "score": 20, "reasoning": "..." },
    "practical_applicability": { "score": 18, "reasoning": "..." }
  },
  "key_findings": ["...", "..."],
  "connections_to_kb": ["paper_id_1", "paper_id_2"]
}
```

### Integrity Check (Phase 2)

**Endpoint:** `POST /api/documents/{doc_id}/integrity-check`

**Prüfungen:**
1. Abstract vs. Conclusions Konsistenz
2. Stichprobengröße erwähnt?
3. Effektstärke berichtet?
4. Konfidenzintervalle vorhanden?
5. Limitationen diskutiert?
6. Pre-Registration erwähnt?

**Output:**
```json
{
  "verdict": "CLEAN",
  "flags": [
    {
      "category": "MISSING_EFFECT_SIZE",
      "severity": "MEDIUM",
      "evidence": "Paper reports significance but no Cohen's d or similar...",
      "confidence": 0.82
    }
  ],
  "overall_quality": "B+"
}
```

---

## 5. Was APE NICHT macht – und wo BEATRIX weitergehen kann

| APE | BEATRIX-Vorteil |
|-----|-----------------|
| Nur Policy Evaluation (US-zentriert) | Behavioral Economics global |
| Nur DiD + RDD | Alle Methoden (RCT, Lab, Field, Survey) |
| Generiert Papers, klassifiziert nicht | Klassifiziert UND integriert in BCM-Framework |
| Kein Consulting-Kontext | Direkte Brücke zu Kunden-Projekten |
| Nur Englisch | Deutsch + Englisch |
| Öffentliche Policy-Daten | Proprietäre FehrAdvice-Daten + öffentliche |

---

## 6. Strategischer Kontext: Kontakt zu Prof. Yanagizawa-Drott

**Wer:** David Yanagizawa-Drott, Professor of Development Economics, UZH
**Wo:** Department of Economics, University of Zurich (gleiche Stadt)
**Was noch:** Co-Chair, Partnership for AI Evidence (PAIE) bei J-PAL

**Synergien:**
- Er automatisiert Policy-Evaluation → FehrAdvice evaluiert Behavioral Interventions
- APE nutzt DiD/RDD → FehrAdvice nutzt dieselben Methoden
- Er braucht Domain-Expertise in Behavioral Economics → FehrAdvice hat sie
- FehrAdvice braucht automatisierte Forschungs-Pipeline → APE hat sie gebaut

**Vorgeschlagene Kontaktaufnahme:**
"Wir haben Ihr APE-Projekt mit grossem Interesse verfolgt und systematisch analysiert. 
Als Behavioral Economics Consultancy sehen wir eine natürliche Komplementarität: 
Ihre Methodik für autonome Policy-Evaluation trifft auf unsere Expertise in 
Behavioral Interventions und das BCM-Framework. Können wir uns austauschen?"

---

*Erstellt: 12. Februar 2026*  
*BEATRIX v3.7.0 × APE Analysis*  
*Quelle: APE Research Project, Social Catalyst Lab, UZH*
