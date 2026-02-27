# F4 — Übergangsstrategie: Xcite → A1 Youth
## Churn-Minimierungs-Playbook · Bestandskunden-Migration

**Session:** EBF-S-2026-02-20-ORG-001
**Modell:** MOD-TEL-001 v1.2.1
**Version:** 1.0 · 2026-02-20
**Laufzeit:** 6 Monate (M1–M6)
**Kernannahme:** λ=2.1 (Verlustaversion AT-kalibriert), ρ_tech=0.38 (Status-quo-Bias Technologie)

---

## Executive Summary

Die Umbenennung von **A1 Xcite → A1 Youth** ist die empirisch stärkste Hebelmassnahme zur Schliessung des 37pp-Conviction-Gaps (50% Awareness → 13% Usage). Die Simulation (3 Sinus-Milieu-Personas × 4 Namen) ergibt Composite-Score 9.46 für «A1 Youth» (Win-Probability 41%) vs. 3.95 für «Xcite» (Win-P 1%).

**Das zentrale Risiko:** λ=2.1 bedeutet, dass bestehende Xcite-Kund:innen Verluste 2,1× schwerer gewichten als äquivalente Gewinne. Jede Kommunikation, die die Umbenennung als «Änderung» oder «Abschied» rahmt, aktiviert Verlustaversion und erhöht die Churn-Wahrscheinlichkeit.

**Die Lösung:** Konsequentes **Loss-Frame-Reversal** — die Umbenennung wird nie als Abgang von Xcite, sondern immer als Ankunft bei A1 Youth kommuniziert. Xcite ist der Status quo, der die Kund:innen unsichtbar gemacht hat. A1 Youth macht sie sichtbar.

**Erwartetes Nettoergebnis nach 12M:**
- Transitionale Churn-Kosten: −€640k (konservativ, λ=2.1-adjustiert)
- Neue Kund:innen durch verbesserte Category Clarity: +€4.1M
- **Net Uplift: +€3.2–3.5M** bei konstantem ARPU

---

## 1. Behavioral Risk Assessment

### 1.1 Verlustaversion (λ=2.1)

Bestandskund:innen verlieren subjektiv «ihr vertrautes Produkt». Die Wahrnehmungswertung für diesen Verlust ist 2.1× höher als der objektive Wert des neuen Namens.

**Implikation:** Ein 1:1-Ersatz («Xcite wird zu Youth») wird behavioural als Nettoverlust empfunden, selbst wenn der Preis, die Leistung und alle Konditionen identisch bleiben. Ohne aktive Gegensteuerung: geschätzte Baseline-Churn-Erhöhung von +3–5pp im Übergangszeitraum.

**Gegensteuerung:** Die Umbenennung muss als **Upgrade** gerahmt werden, das die Kund:innen bekommen — nicht als Abgang von etwas, das sie verlieren. Der Loss-Frame wird auf Xcite selbst angewendet: «Xcite hat euch bisher unsichtbar gemacht. A1 Youth stellt euch ins Rampenlicht.»

### 1.2 Status-quo-Bias (ρ_tech=0.38)

38% der Xcite-Bestandskund:innen werden bei Status-quo-Stimuli keine aktive Verarbeitungsreaktion zeigen. Sie lesen die Kommunikation, tun aber nichts — und merken erst beim Hard-Cutover, dass sich etwas geändert hat.

**Implikation:** Passive Kommunikation (E-Mail only) reicht nicht. Für diese 38% ist ein **Implementation Intention Prompt** nötig: «Du wirst ab [Datum] automatisch Teil von A1 Youth. Es passiert für dich — du musst nichts tun.»

**Gegensteuerung:** Default-Opt-In-Mechanismus. Kein aktiver Schritt nötig. Die Passivität arbeitet für die Migration, nicht gegen sie.

### 1.3 Churn-Risiko-Multiplikatoren (aus JTBD n=2.134)

| Trigger | Churn-Multiplikator | Massnahme |
|---------|---------------------|-----------|
| Kundenservice-Kontakt notwendig | 1.5× | Self-Service-First + FAQ-Hub zur Umbenennung |
| Erstattungsanfrage wegen Verwirrung | 1.3× | Keine Preisänderung, proaktive Klarstellung |
| Fehler-/Störungsmeldung | 1.4× | Technische Stabilität vor Cutover sicherstellen |
| Tarifwechsel-Unzufriedenheit (26%) | hoch | Reframing: Tarif ändert sich NICHT |

**Kritische Regel:** Während der Transition-Phase (M3–M6) muss die Youth Internet NPS-Basis stabilisiert werden. Aktuell: −11.5 (Okt 2025, KRITISCH verschlechtert). Ein NPS-Einbruch während der Umbenennung potenziert alle Multiplikatoren.

---

## 2. Bestandskunden-Segmentierung

### 2.1 Schätzung Xcite-Bestandsbasis

Geschätzte 120–150k aktive Xcite-Kund:innen (basierend auf Marktanteil AT Youth 18–26, A1-Position, Penetrationsrate).

### 2.2 Behavioral-Segmente (HVV vs. LVV)

**High Value Voice (HVV) — ~65% der Xcite-Basis**
- Profile: Loyal, schon länger bei A1, kein akuter Wechselimpuls
- Churn-Risiko bei Rename: **MEDIUM** (λ aktivierbar durch schlechte Kommunikation)
- Messaging: Reassurance-First — «Alles bleibt. Der Name wird besser.»
- Kanal: SMS + MeinA1-App Push (persönlich, nicht E-Mail-Masse)

**Low Value Voice (LVV) — ~35% der Xcite-Basis**
- Profile: Flexibilitätsorientiert, wechseln bei Gelegenheit (spusu-Mentalität)
- Churn-Risiko bei Rename: **HIGH** (Rename = Opportunity Window zum Abspringen)
- Messaging: Value-Add-First — «A1 Youth = dein Tarif, jetzt mit stärkerem Profil»
- Kanal: In-App + targeted Social (schnell, peer-sprachlich)

### 2.3 Sinus-Milieu-Verteilung der Xcite-Basis (geschätzt)

| Milieu | Xcite-Anteil (est.) | Churn-Risiko | Priorität |
|--------|---------------------|--------------|-----------|
| Hedonisten (Tobias-Profil) | ~30% | HIGH — Magenta-Confusion wenn schlecht kommuniziert | P1 |
| Adaptiv-Pragmatische Mitte (Sofia-Profil) | ~35% | LOW — funktionale Klarheit wirkt | P3 |
| Kosmopolitische Individualisten (Lukas-Profil) | ~20% | MEDIUM — Identity-Upgrade funktioniert | P2 |
| Andere (Performer, Konservative, Progressiv) | ~15% | MEDIUM | P3 |

**Kritisch für Hedonisten (30% der Basis):** Diese Gruppe reagierte in der Simulation mit «dann geh ich halt zu Magenta» auf A1 Young. Bei A1 Youth war die Reaktion positiver. Das Risiko besteht aber, wenn die Kommunikation «jugendlich» statt «Youth-als-Identität» klingt. Abgrenzung zu Magenta Mobile Young **muss** im Creative explizit sein — nicht durch direkten Vergleich, sondern durch eigenständige Positionierung.

---

## 3. 6-Monats-Migrationsplan

### Phase 1: Preparation (M1–M2) — intern, keine Kundenkommunikation

**M1: Foundation**
- [ ] CRM-Tagging aller Xcite-Bestandskund:innen nach HVV/LVV/Milieu
- [ ] Creative-Briefing «A1 Youth» an Agentur (Loss-Frame-Reversal Kernbotschaft)
- [ ] Interne Schulung Customer Service: FAQ «Was ändert sich für mich?» (Antwort: Nur der Name)
- [ ] Technische Infrastruktur: MeinA1-App-Push-Capability für segmentiertes Messaging
- [ ] NPS-Baseline erfassen (Startpunkt für Pre/Post-Messung)

**M2: Creative & Testing**
- [ ] A/B-Test Messaging-Varianten auf kleiner Bestandsgruppe (n=2.000, HVV/LVV split)
  - Variante A: «Dein Tarif heisst jetzt A1 Youth» (neutral)
  - Variante B: «Xcite war unser Platzhalter. A1 Youth ist dein echter Name.» (Loss-Frame-Reversal)
  - Variante C: «Du wirst automatisch Teil von A1 Youth — nichts ändert sich ausser, dass man dich jetzt findet.» (Reassurance + Default)
- [ ] Metriken: Open Rate, Click-Through auf FAQ, Churn in 30-Tage-Fenster
- [ ] Best Performer → Roll-out Plan für M4

---

### Phase 2: Soft-Launch (M3) — Neuakquisition auf Youth, Dual-Brand sichtbar

**M3: Neu-Akquisition auf «A1 Youth» umstellen**
- [ ] **Day 1:** Alle neuen SIM-Akquisitionen heissen A1 Youth (kein Xcite mehr für Neukund:innen)
- [ ] Webseite, Shop, Vergleichsportale: A1 Youth als Primär-Label
- [ ] Xcite bleibt **parallel sichtbar** mit Redirect-Banner: «Xcite = A1 Youth»
- [ ] **Noch keine aktive Kommunikation** an Bestandskund:innen (Stille Vorbereitungsphase)
- [ ] Werbematerial: A1 Youth branding deployed (Out-of-Home, Digital, Social)

**KPI-Check M3 Ende:**
- Neue Aktivierungen unter «A1 Youth»: Ziel >80% aller Neukund:innen (Zeichen: Category Clarity funktioniert)
- Xcite Bestandskunden Churn: Soll unter Baseline bleiben (keine aktive Kommunikation = kein Auslöser)

---

### Phase 3: Awareness-Push (M4) — Erstkommunikation an Bestandskund:innen

**M4: Proaktive Outreach (HVV zuerst, dann LVV)**

**Woche 1–2: HVV-Segment**
- Kanal: SMS (persönlich, direkter) + MeinA1-App Push
- Botschaft (gewinnender Variant aus M2-A/B-Test, ca. Variante C):
  > «Hey [Name]. Dein A1-Tarif bekommt einen neuen Namen — A1 Youth. Dein Preis, dein Angebot, deine Nummer: alles bleibt. Du musst nichts tun. Ab [Datum] trägt dein Tarif einfach einen Namen, der zu dir passt.»
- FAQ-Link: «Was ändert sich? Nur der Name. Wirklich.»
- **Kein Opt-In/Opt-Out anbieten** (würde Verlustaversion aktivieren — «warum muss ich aktiv werden?»)

**Woche 3–4: LVV-Segment**
- Kanal: In-App Notification + E-Mail
- Botschaft: Value-Add-Frame (für LVV-Mentalität):
  > «A1 Youth ist da — und du bist schon dabei. Dein neuer Name, dein altes Angebot, und jetzt: leichter zu finden, leichter zu empfehlen.»
- Social-Proof-Element: «Schon [X]k Jugendliche unter 26 sind A1 Youth.» (Peer-Norm)

**KPI-Check M4 Ende:**
- Kommunikations-Open-Rate: Ziel >45% (SMS typisch 90%+ open, in-app 25–35%)
- Inbound-Anfragen zu «Was ändert sich»: Soll unter 3% der erreichten Kund:innen
- Churn-Rate in 30 Tagen post-Kommunikation: Soll max. +1pp über Baseline (λ=2.1-Risk-Budget)

---

### Phase 4: Migration Active (M5) — Vertiefung & Nachfass

**M5: Remaining 38% (ρ_tech=0.38 — Status-quo-passive Gruppe)**
- Identifikation: Wer hat Kommunikation aus M4 geöffnet aber keine Interaktion gezeigt?
- Second-Touch: SMS-Reminder — kurz, ohne Druck:
  > «Nur zur Info: Ab [Datum] heisst dein Tarif A1 Youth. Keine Aktion nötig — es passiert automatisch für dich.»
- In-App: Persistent Banner in MeinA1-App («Demnächst: Du wirst A1 Youth»)

**Sinus-Milieu-spezifischer Content-Push (Social/Digital):**
- **Hedonisten-Creative:** Peer-Video-Content, kein Corporate-Ton. «Youth ist die Crew.» Abgrenzung zu Magenta durch Eigenständigkeit, nicht durch Vergleich.
- **Kosmopolit-Creative:** Identity-Forward. «Dein Tarif spricht jetzt deine Sprache.» English-accented visuals OK.
- **Adaptiv-Pragmatisch:** Klarheit/Einfachheit. «Jetzt noch leichter zu finden.»

**KPI-Check M5 Ende:**
- Prozentsatz Bestandskund:innen, die aktiv «A1 Youth» in MeinA1-App sehen (nach Banner): Ziel >90%
- Churn kumuliert M3–M5: Ziel max. +2pp gesamt über Baseline (λ-Budget)

---

### Phase 5: Hard Cutover (M6) — Xcite wird eingestellt

**M6: Vollständige Migration**

**Day 0 (Cutover-Tag):**
- [ ] «Xcite» als Produktbezeichnung in allen Systemen deaktiviert
- [ ] Alle Bestandskund:innen sehen in MeinA1-App: «Mein Tarif: A1 Youth»
- [ ] Kundenservice: «Xcite» als Stichwort bleibt im System hinterlegt (Kund:innen können noch Monate danach mit «Xcite» anrufen und werden korrekt zugeordnet)
- [ ] Redirect «xcite.a1.at» → «youth.a1.at» bleibt 12 Monate aktiv

**Day 1–7 Hypercare:**
- [ ] Erhöhte Kundenservice-Kapazität (+15% Staffing) für 7 Tage post-Cutover
- [ ] Real-time NPS-Monitoring (Ziel: kein Einbruch unter −15)
- [ ] Churn-Alert: Wenn tägliche Churn-Rate Xcite-Bestandssegment >2× Baseline → Emergency-Kommunikation activieren («Bitte bleib — wir erklären alles»)

---

## 4. Kommunikationsstrategie: Core-Prinzipien

### 4.1 Loss-Frame-Reversal (λ=2.1-Antwort)

**Verboten:**
> ❌ «Xcite wird abgelöst»
> ❌ «Wir stellen Xcite ein»
> ❌ «Xcite gehört der Vergangenheit an»

**Geboten:**
> ✅ «A1 Youth ist da — und du bist von Anfang an dabei»
> ✅ «Dein Tarif bekommt jetzt den Namen, der zu dir passt»
> ✅ «A1 Youth ist das, was Xcite immer sein wollte»

**Mechanismus:** Der Loss-Frame wird auf Xcite selbst gelegt («Xcite hat euch unsichtbar gemacht»), nicht auf die Kund:innen. Damit aktiviert die Umbenennung *positive* Identitäts-Transformation statt Verlust.

### 4.2 Default-Kommunikation (ρ_tech=0.38-Antwort)

Kein Opt-In. Kein aktiver Schritt notwendig. Die Migration passiert automatisch.

Formulierung immer: «Es passiert für dich — du musst nichts tun.»

### 4.3 Konkrete Tonalität nach Milieu

| Milieu | Tonalität | Verboten |
|--------|-----------|----------|
| Hedonisten | Peer-zu-Peer, kurz, energetisch. «Crew», «Belong», «Level up» | Corporate, «Jugend», «Tarif» |
| Kosmopoliten | Cool, eigenständig, multilingual OK. «Global mindset, local network» | Zu österreichisch-bieder |
| Adaptiv-Pragmatisch | Klar, direkt, ehrlich. «Einfacher. Klarer. Dasselbe Angebot.» | Zu viel Hype, unklare Botschaft |

---

## 5. KPI-Framework & Erfolgsmessung

### 5.1 Primär-KPIs (direkt messbar)

| KPI | Baseline (jetzt) | Ziel M6 | Kritische Grenze |
|-----|-----------------|---------|-----------------|
| Category Clarity Score (intern) | Xcite: 2/10 | Youth: 8/10 | <6 = Nacharbeit |
| Churn-Rate Xcite-Bestand (ggü. Baseline) | 0pp | max. +2pp kumulativ | +5pp = Emergency |
| New-Customer-Awareness «A1 Youth» | ~0% (kein Name yet) | >60% unaided | <40% = Creative-Problem |
| MeinA1-App: «A1 Youth»-Tarif-Sichtbarkeit | 0% | >95% der Bestandskund:innen | <80% = tech. Problem |
| Inbound-Anfragen «Was ändert sich?» | — | <3% der Basis | >8% = Kommunikation überarbeiten |

### 5.2 Sekundär-KPIs (strukturell wichtig)

| KPI | Baseline | Ziel M6 |
|-----|---------|---------|
| Youth-Segment Internet NPS | −11.5 (Okt 2025) | ≥−5 (Stabilisierung) |
| Neue Aktivierungen Youth-Segment (MoM) | Baseline M3 | +15% MoM M4–M6 |
| Share of Youth-Acquisitions (15–26) | aktuell unklar | +8pp gegenüber Xcite-Periode |
| Spontan-Awareness «A1 Youth» bei 18–26 AT | ~0% | >25% nach 6 Monaten |

### 5.3 Messzeitpunkte

- **M3 Ende:** First Check — Neue Aktivierungen laufen unter Youth?
- **M4 Woche 2:** Kommunikations-Performance — Open Rate, Inbound-Ratio
- **M5 Ende:** Churn-Kumulierung im Budget? Milieu-Creative wirkt?
- **M6 Woche 1:** Hypercare-KPIs täglich
- **M6 + 4 Wochen:** Post-Transition-NPS-Messung (Vergleich zu Baseline M1)
- **M12:** Revenue-Impact-Messung (Ziel: +€3.2M net realisiert)

---

## 6. Risikoanalyse

| Risiko | Eintrittswahrscheinlichkeit | Impact | Gegensteuerung |
|--------|---------------------------|--------|----------------|
| Hedonisten interpretieren «Youth» als Magenta-nah | MEDIUM (30% der Basis) | HIGH | Creative explizit eigenständig; kein «Young»-Vocabulary |
| NPS-Einbruch während Transition | LOW-MEDIUM | SEHR HIGH | Technische Stabilisierung M1–M2; Hypercare M6 |
| LVV-Segment nutzt Rename als Exit-Gelegenheit | HIGH (inherent) | MEDIUM | Value-Add-Messaging; kein Opt-Out anbieten |
| Interne Verwechslung Xcite/Youth in Kundenservice | MEDIUM | MEDIUM | Vollständige Service-Schulung M2; System-Support |
| Wettbewerber (Magenta «Mobile Young») greift Rename-Moment an | LOW-MEDIUM | MEDIUM | Eigene Kampagnenintensität hochhalten M3–M5 |
| 38% passive Kund:innen (ρ_tech) überrascht vom Cutover | HIGH | LOW | Implementation Intention Push M5; Xcite bleibt im System hinterlegt |

---

## 7. Budget-Grössenordnung (Indikativ)

| Posten | Schätzung |
|--------|-----------|
| Creative-Entwicklung A1 Youth (3 Milieu-Varianten) | €80–120k |
| CRM-Kampagnen (SMS + App, 4 Wellen, 150k Kund:innen) | €60–90k |
| Kundenservice-Schulung + Hypercare-Staffing M6 | €30–50k |
| Digital-Kampagne M3–M6 (Neukunden-Akquise) | €200–300k |
| **Gesamt Transition-Investment** | **€370–560k** |
| **Erwarteter Net Uplift (12M)** | **+€3.2–3.5M** |
| **ROI** | **~6:1 bis 9:1** |

---

## 8. Entscheidungsvorlage: Go / No-Go Kriterien

**GO wenn (alle müssen erfüllt sein):**
- [ ] M2-A/B-Test: Winning-Variante zeigt Churn ≤Baseline in 30 Tagen
- [ ] Technische Stabilität: Youth Internet-Infrastruktur NPS besser als −11.5 (aktuell kritisch)
- [ ] Interne Schulung: >95% Customer Service mit A1-Youth-FAQ briefed
- [ ] Creative-Zustimmung: Milieu-spezifische Varianten von Brand Management freigegeben

**NO-GO / Verschiebung wenn:**
- M2-A/B: Churn-Spike >+3pp in Testgruppe → Creative überarbeiten, dann Re-Test
- NPS-Messung M2: Weitere Verschlechterung Youth Internet NPS → erst Service-Problem lösen, dann Rename
- Competitor-Aktion: Magenta launcht «Mobile Youth» (AT) während Preparation → positioning clarification nötig

---

## Anhang: Modell-Referenzen

| Parameter | Wert | Quelle |
|-----------|------|--------|
| λ (Verlustaversion AT) | 2.1 | MOD-TEL-001, BCM2_AT + JTBD n=2.134 |
| ρ_tech (Status-quo-Bias Technologie) | 0.38 | JTBD ConsumerLifetime 2025 |
| γ_FS (Financial-Social Crowding-Out) | −0.35 | Parameter-Registry PAR-COMP-002 |
| γ_SE_kos (Social-Effort Kosmopoliten) | +0.35 | MOD-TEL-001 Milieu-Matrix |
| Xcite Conviction Gap | 37pp | Urban Push Wien + Focus Groups AT |
| Churn-Multiplikator Support-Kontakt | 1.5× | JTBD n=2.134 |
| Youth Internet NPS (Okt 2025) | −11.5 | Urban Push Wien Wave 2 |
| A1 Preference Migrant-Segment | 26% vs. 19% Gesamt | Urban Push Wien |

**Modell-File:** `data/model-registry.yaml` → MOD-TEL-001 (Zeilen 6644–7100)
**Branch:** `claude/check-a1-model-RVR1g`
**Session-Outputs F1–F3:** `outputs/sessions/EBF-S-2026-02-20-ORG-001/`
