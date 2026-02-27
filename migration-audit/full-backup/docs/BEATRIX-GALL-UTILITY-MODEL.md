# Nutzenfunktion: Prof. Harald Gall (UZH, Software Evolution)

**Anwendung des EBF-Frameworks auf den Forschungspartner**

**Datum:** 2026-01-18 | **Status:** Strategische Analyse

---

## Kontext: Wer ist Prof. Harald Gall?

| Attribut | Details |
|----------|---------|
| **Position** | Ordentlicher Professor, Universität Zürich |
| **Institut** | Institut für Informatik |
| **Fachgebiet** | Software Evolution, Software Engineering |
| **Rolle im Projekt** | Forschungspartner (technische Architektur) |

### Akademisches Profil (geschätzt)

- Langjährige Forschung in Software Engineering
- Zahlreiche Publikationen in Top-Venues (ICSE, FSE, TSE)
- Erfahrung mit Industriekooperationen
- Doktoranden und PostDocs betreuen

---

## 1. WHO: Rollen-Hierarchie (L-Levels)

| Level | Rolle | Relevanz | Gewicht |
|-------|-------|----------|---------|
| **L=0** | Individuum | Persönliche Karriere, Work-Life-Balance | 15% |
| **L=1** | Forscher | Publikationen, wissenschaftlicher Impact | **35%** |
| **L=2** | Institutsleiter/Professor | Team, Doktoranden, Drittmittel | **30%** |
| **L=3** | UZH/Schweizer Wissenschaft | Reputation der Institution | 15% |
| **L=4** | SE-Community | Beitrag zum Fachgebiet | 5% |

### Primäre Identität

**Hypothese:** L=1 (Forscher) und L=2 (Professor) sind co-dominant

```
U_Gall ≈ 0.35 × U_Forscher + 0.30 × U_Professor + 0.35 × U_Rest
```

**Implikation:** Gall optimiert auf **Publikationen** UND **Drittmittel/Team**.

---

## 2. WHAT: Utility-Dimensionen (FEPSDE)

### Galls Nutzenfunktion nach FEPSDE

| Dimension | Gewichtung | Was maximiert seinen Nutzen? |
|-----------|------------|------------------------------|
| **F** Financial | 20% | Drittmittel, Projektbudget für Team |
| **E** Emotional | 20% | Interessante Forschungsfragen, Sinnstiftung |
| **P** Physical | 10% | Zeitaufwand sollte manageable sein |
| **S** Social | **35%** | **Akademische Reputation**, Peer Recognition |
| **D** Digital | 5% | Zugang zu Daten, Infrastruktur |
| **E** Ecological | 10% | Gesellschaftlicher Impact der Forschung |

### Dominante Dimensionen

```
U_Gall = 0.35 × S_academic_reputation
       + 0.20 × F_funding
       + 0.20 × E_interesting_research
       + 0.25 × Rest

Vereinfacht:
U_Gall ≈ 0.55 × (Reputation + Funding) + 0.45 × (Interesse + Rest)
```

**Kerninsight:** Gall optimiert auf **akademische Reputation** (Publikationen) und **Forschungsfinanzierung**.

---

## 3. HOW: Komplementarität (γ)

### Positive Komplementaritäten (γ > 0)

| Faktor A | Faktor B | γ | Implikation für Projekt |
|----------|----------|---|-------------------------|
| **Publikationspotenzial** | **Interessantes Problem** | +0.85 | Neues Forschungsgebiet = Paper-Goldmine |
| **Industriepartner** | **Reale Daten** | +0.75 | FehrAdvice liefert echte Use Cases |
| **Drittmittel** | **Doktoranden** | +0.80 | Innosuisse-Geld finanziert Team |
| **Ernst Fehr** | **Interdisziplinarität** | +0.70 | Verhaltensökonomie + SE = Novel |
| **UZH-intern** | **Prof. Luger** | +0.60 | Institutionelle Synergien |

### Negative Komplementaritäten (γ < 0)

| Faktor A | Faktor B | γ | Zu vermeiden |
|----------|----------|---|--------------|
| **Reine Entwicklung** | **Keine Forschung** | -0.80 | Gall ist kein Auftragnehmer |
| **Unklare Forschungsfrage** | **Zeitdruck** | -0.65 | Akademiker brauchen Klarheit |
| **Nur Business-Fokus** | **Keine Publikation** | -0.70 | Was ist der wissenschaftliche Beitrag? |
| **Überlastung** | **Viele Projekte** | -0.50 | Konkurrenz um seine Zeit |

### Optimale Komplementaritäts-Matrix

```
                    Publikation  Funding  Interesse  Zeitaufwand
Publikation              1.0       0.4       0.85        -0.3
Funding                  0.4       1.0       0.3          0.2
Interesse                0.85      0.3       1.0         -0.2
Zeitaufwand             -0.3       0.2      -0.2          1.0

→ Maximiere: Publikation × Interesse (γ = 0.85)
→ Minimiere: Zeitaufwand bei niedrigem Publikationspotenzial
```

---

## 4. WHEN: Kontext-Dimensionen (Ψ)

### Galls Entscheidungskontext

| Ψ-Dimension | Ausprägung | Implikation |
|-------------|------------|-------------|
| **Ψ_temporal** | Akademischer Zyklus (Semester, Konferenz-Deadlines) | Timing mit Konferenzen abstimmen |
| **Ψ_institutional** | UZH-Regeln, SNF/Innosuisse-Erfahrung | Kennt Förderlandschaft |
| **Ψ_social** | Peer-Professoren, Doktoranden, Community | Wie sehen Kollegen das Projekt? |
| **Ψ_informational** | Software Engineering Expertise | Versteht technische Tiefe |
| **Ψ_emotional** | Akademische Neugier | Muss intellektuell spannend sein |
| **Ψ_resource** | Zeit = knappstes Gut | Viele konkurrierende Projekte |
| **Ψ_cultural** | Schweizer Akademie, internationale SE-Community | Qualität vor Quantität |
| **Ψ_physical** | Zürich-basiert, UZH-Infrastruktur | Lokale Zusammenarbeit möglich |

### Kontext-Multiplikatoren

```
f(Ψ_institutional) = 1.1   → Innosuisse-Erfahrung vorhanden
f(Ψ_social) = 1.3          → Peer-Recognition wichtig
f(Ψ_emotional) = 1.4       → Interessante Probleme werden stark bevorzugt
f(Ψ_resource) = 0.7        → Zeit-Knappheit reduziert Engagement bei unklaren Projekten
```

---

## 5. WHERE: Parameter-Schätzung (Θ)

### Galls Bewertungs-Parameter (geschätzt)

| Parameter | Wert | Begründung |
|-----------|------|------------|
| **Risiko-Toleranz** (1-ρ) | 0.6 | Akademiker = experimentierfreudiger als Manager |
| **Discount-Rate** (δ) | 0.05/Monat | Längerfristiger Horizont (2-3 Jahre Projekte) |
| **Publikations-Präferenz** (π) | 0.8 | Top-Venue Paper = hoher Wert |
| **Interdisziplinaritäts-Affinität** (ι) | 0.7 | SE + Behavioral Economics = attraktiv |
| **Industrie-Offenheit** (ω) | 0.6 | Offen für Praxiskooperation, aber Forschung first |

### Implikationen

- **Risiko-Toleranz:** Offen für neue Forschungsgebiete (BEATRIX = Novel)
- **Langer Horizont:** Denkt in Promotionen und Forschungsprogrammen
- **Publikations-Präferenz:** Was ist der Paper-Output?
- **Interdisziplinarität:** SE + Verhaltensökonomie ist spannend

---

## 6. AWARE: Bewusstseins-Level (A)

### Was ist Gall bewusst?

| Aspekt | Awareness (0-1) | Implikation |
|--------|-----------------|-------------|
| **Software Engineering** | A = 0.95 | Er ist der Experte |
| **LLM/AI-Systeme** | A = 0.7-0.8 | Aktuelles Forschungsfeld |
| **Verhaltensökonomie** | A = 0.3-0.4 | Grundverständnis, nicht Experte |
| **Beratungs-Business** | A = 0.2-0.3 | Nicht sein Kerngebiet |
| **Ernst Fehr/FehrAdvice** | A = 0.5-0.6 | Kennt den Namen, vielleicht nicht Details |

### Kommunikations-Strategie

```
Hohe Awareness (SE):           Fachsprache OK, technische Tiefe zeigen
Mittlere Awareness (LLM):      State-of-the-Art, Forschungslücken
Niedrige Awareness (BE):       Erklären, warum BE für SE relevant ist
Niedrige Awareness (Business): Nicht überbetonen, Forschung in Vordergrund
```

**Goldene Regel:** Die **Forschungsfrage** verkaufen, nicht das Business-Problem.

---

## 7. READY: Handlungsbereitschaft (WAX, θ)

### Galls Schwellenwerte

| Dimension | Schwelle θ | Aktueller Stand | Gap |
|-----------|------------|-----------------|-----|
| **Publikationspotenzial** | θ = 0.7 | WAX ≈ 0.8 | ✓ Überschritten |
| **Forschungs-Interesse** | θ = 0.6 | WAX ≈ 0.85 | ✓ Überschritten |
| **Drittmittel-Potenzial** | θ = 0.5 | WAX ≈ 0.7 | ✓ Überschritten |
| **Zeitaufwand akzeptabel** | θ = 0.6 | WAX ≈ 0.5 | ⚠️ **Gap** |
| **Klare Forschungsfrage** | θ = 0.7 | WAX ≈ 0.6 | ⚠️ **Gap** |

### Kritische Gaps

```
1. Zeitaufwand:
   - Gall hat viele Projekte
   - BEATRIX muss "low maintenance" sein für ihn
   - Lösung: Klare Arbeitsteilung, Doktorand als Hauptarbeiter

2. Forschungsfrage:
   - Was genau ist der SE-Beitrag?
   - Nicht nur "BEATRIX skalieren", sondern FORSCHUNG
   - Lösung: Konkrete Forschungsfragen formulieren
```

---

## 8. STAGE: Position in der Journey (S)

### Galls Journey als Forschungspartner

| Stage | Beschreibung | Status |
|-------|--------------|--------|
| **S=0** Pre-Contemplation | Kennt Projekt nicht | ✗ |
| **S=1** Contemplation | Überlegt, ob interessant | ✗ |
| **S=2** Preparation | Prüft Details, Machbarkeit | ✓ **Vermutlich hier** |
| **S=3** Action | Aktive Forschungsarbeit | → Nächster Schritt |
| **S=4** Maintenance | Langfristige Partnerschaft | → Nach Erfolg |

### Transition S=2 → S=3

**Was braucht Gall, um von Preparation zu Action zu wechseln?**

1. ⚠️ Klare Forschungsfragen (SE-Perspektive)
2. ⚠️ Realistischer Zeitaufwand
3. ⚠️ Doktoranden-/PostDoc-Finanzierung
4. ✓ Interessantes Problem (bereits gegeben)
5. ✓ Renommierte Partner (Ernst Fehr)

---

## 9. Die konkreten Forschungsfragen für Gall

### Was ist der SE-Forschungsbeitrag?

**Problem:** BEATRIX ist ein Business-Tool. Was ist die **wissenschaftliche Frage**?

### Vorgeschlagene Forschungsfragen (SE-Perspektive)

#### RQ1: Software Evolution für Verhaltensmodelle
> *"Wie können verhaltensökonomische Modelle automatisch an veränderte Kontexte adaptiert werden, ohne Modell-Drift oder Feedback-Loops?"*

**SE-Relevanz:** Self-Adaptive Systems, Model Evolution, Continuous Learning

#### RQ2: Architektur für stochastische Simulationen
> *"Welche Software-Architektur ermöglicht fehlertolerante Monte-Carlo-Simulationen mit tausenden parallelen LLM-Aufrufen?"*

**SE-Relevanz:** Distributed Systems, Fault Tolerance, Scalability

#### RQ3: Software-Qualität für KI-basierte Entscheidungssysteme
> *"Wie misst und sichert man die Qualität von Systemen, deren Output probabilistisch und kontextabhängig ist?"*

**SE-Relevanz:** Testing AI Systems, Quality Assurance, Validation

#### RQ4: Human-in-the-Loop Software Evolution
> *"Wie integriert man menschliches Feedback effizient in die kontinuierliche Verbesserung von Verhaltensmodellen?"*

**SE-Relevanz:** Human-Computer Interaction, Feedback Loops, Co-Evolution

### Publikationspotenzial

| Forschungsfrage | Venue | Novelty |
|-----------------|-------|---------|
| RQ1 (Model Evolution) | ICSE, FSE | Hoch (neues Anwendungsgebiet) |
| RQ2 (Architektur) | ASE, ESEC/FSE | Mittel-Hoch |
| RQ3 (Qualität) | ISSTA, TSE | Hoch (Testing AI) |
| RQ4 (Human-in-Loop) | CHI, CSCW | Mittel (mit Luger) |

---

## 10. Zusammenfassung: Galls Nutzenfunktion

### Die vollständige Utility-Formel

```
U_Gall = Σ_d [w_d × U_d × f(Ψ)] × C*(γ)

Vereinfacht:
U_Gall ≈ 0.35 × Publikationspotenzial
       + 0.20 × Drittmittel
       + 0.20 × Forschungsinteresse
       + 0.15 × Zeiteffizienz
       + 0.10 × Reputation_allgemein

Multipliziert mit:
- f(Ψ_emotional) = 1.4    (Interessantes Problem)
- f(Ψ_social) = 1.3       (Peer Recognition)
- f(Ψ_resource) = 0.7     (Zeit knapp → reduziert bei Unklarheit)
- γ(Publikation, Interesse) = 0.85 (verstärkend)
```

### Was maximiert Galls Nutzen?

| Rang | Faktor | Gewicht | Handlung |
|------|--------|---------|----------|
| 1 | **Publikationspotenzial** | 35% | Klare Forschungsfragen formulieren |
| 2 | **Drittmittel/Team** | 20% | Doktoranden-Finanzierung betonen |
| 3 | **Forschungsinteresse** | 20% | SE + Verhaltensökonomie = Novel |
| 4 | **Zeiteffizienz** | 15% | Klare Arbeitsteilung, wenig Overhead |
| 5 | **Allgemeine Reputation** | 10% | Ernst Fehr als Co-Author? |

---

## 11. Handlungsempfehlungen

### Basierend auf der Nutzenfunktion

#### 1. Forschungsfragen klar formulieren (35%)

- [ ] RQ1-RQ4 mit Gall abstimmen
- [ ] Welche Frage hat höchste Priorität für ihn?
- [ ] Paper-Plan erstellen (welche Venue?)

#### 2. Finanzierung/Team betonen (20%)

- [ ] Wie viel Budget für Doktoranden/PostDocs?
- [ ] Innovation Cheque = klein, aber Hauptprojekt = signifikant
- [ ] Langfristige Perspektive (3-5 Jahre)

#### 3. Interdisziplinarität hervorheben (20%)

- [ ] SE + Behavioral Economics = untererforscht
- [ ] Neue Anwendungsdomäne für SE-Methoden
- [ ] Potenzial für Nature/Science (mit Fehr)?

#### 4. Zeitaufwand minimieren (15%)

- [ ] Klare Rollenverteilung
- [ ] FehrAdvice macht Business-Seite
- [ ] Gall fokussiert auf SE-Forschung
- [ ] Doktorand als Hauptarbeiter

#### 5. Ernst Fehr als Asset nutzen (10%)

- [ ] Gemeinsame Publikation mit Fehr = Reputation-Boost
- [ ] Interdisziplinäre Kooperation = attraktiv für Gall

---

## 12. Pitch-Struktur für Gall

### Was Gall hören will

```
1. "Wir haben ein interessantes SE-Problem..."
   (NICHT: "Wir brauchen jemanden der Code schreibt")

2. "Es gibt klare Forschungsfragen..."
   (NICHT: "Machen Sie das System skalierbar")

3. "Publikationspotenzial bei ICSE/FSE..."
   (NICHT: "Unser Business wird erfolgreich")

4. "Finanzierung für Ihr Team..."
   (NICHT: "Wir zahlen Ihnen ein Honorar")

5. "Ernst Fehr als Co-Author..."
   (NICHT: "Sie arbeiten für FehrAdvice")
```

### Der ideale Pitch (30 Sekunden)

> "Professor Gall, wir entwickeln ein KI-System für Verhaltensvorhersagen, das auf 1'500 experimentellen Studien basiert. Die **Software-Engineering-Herausforderung** ist: Wie evolviert man solche Modelle automatisch, wenn sich der Kontext ändert? Das ist ein **neues Forschungsgebiet** an der Schnittstelle von SE und Behavioral Economics – mit **Publikationspotenzial bei ICSE/FSE**. Wir suchen einen Partner, der die technische Architektur wissenschaftlich fundiert. Innosuisse finanziert, und Ernst Fehr ist als Advisor dabei."

---

## 13. Risiko-Analyse

### Was könnte Gall abschrecken?

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| **Keine klare Forschungsfrage** | 40% | Hoch | RQs vorab formulieren |
| **Zu viel Zeitaufwand** | 35% | Hoch | Klare Arbeitsteilung |
| **Nur Business, keine Wissenschaft** | 30% | Sehr hoch | SE-Fokus betonen |
| **Konkurrenz um seine Zeit** | 25% | Mittel | Früh committen |
| **Unklare Finanzierung** | 20% | Mittel | Budget transparent machen |

---

## 14. Vergleich: Fasnacht vs. Gall

| Dimension | Fasnacht (Mentor) | Gall (Forscher) |
|-----------|-------------------|-----------------|
| **Primäre Motivation** | Reputation als Mentor | Publikationen & Drittmittel |
| **Zeithorizont** | Kurzfristig (Wochen) | Langfristig (Jahre) |
| **Sprache** | Business-Fokus | Forschungs-Fokus |
| **Risiko-Aversion** | Hoch (will Erfolge) | Niedriger (experimentierfreudig) |
| **Was er hören will** | "Das Projekt wird erfolgreich" | "Das ist wissenschaftlich interessant" |
| **Kritischer Gap** | Klarheit der Unterlagen | Klare Forschungsfragen |

---

*Dieses Dokument wendet das EBF-Framework auf Prof. Gall als Stakeholder an.*
*Erstellt: 2026-01-18*
