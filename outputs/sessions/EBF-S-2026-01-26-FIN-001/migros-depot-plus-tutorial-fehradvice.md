# Migros Bank | Depot Plus
## Interaktives Produkt-Routing Tutorial

---

**Kunde:** Migros Bank AG
**Projekt:** Endkunden-Tutorial Anlageprodukte
**Datum:** 26. Januar 2026
**Version:** 1.0

---

**FehrAdvice & Partners AG**
Klausstrasse 20 | 8008 Zürich
www.fehradvice.com

---

## Executive Summary

Das vorliegende Tutorial führt Migros Bank Endkunden in einem **2-minütigen interaktiven Prozess** zum passenden Anlageprodukt. Die verhaltensökonomisch fundierte Architektur adressiert die drei Kernprodukte der Bank:

| Produkt | Zielgruppe | Erwarteter Anteil |
|---------|------------|-------------------|
| ExO-Depot | Selbstentscheider | ~15% |
| **Depot Plus** | **Orientierungssuchende** | **~65%** |
| PAB | Beziehungssuchende | ~20% |

**Zentrale Design-Prinzipien:**
- Selbstkategorisierung statt Fremdattribution
- Choice Architecture mit 3 Optionen pro Entscheidung
- Trust Priming durch Migros-Markenwerte
- Social Proof durch segmentspezifische Personas

---

## 1. Ausgangslage und Zielsetzung

### 1.1 Herausforderung

Die Migros Bank bietet drei Anlageprodukte mit unterschiedlichen Beratungsintensitäten an. Kunden stehen vor der Herausforderung, das für sie passende Produkt zu identifizieren – eine Entscheidung, die durch folgende verhaltensökonomische Barrieren erschwert wird:

| Barriere | Auswirkung | Häufigkeit |
|----------|------------|------------|
| Choice Overload | Entscheidungsaufschub | 35% der Zielgruppe |
| Loss Aversion | Angst vor Fehlentscheidung | 48% der Zielgruppe |
| Status Quo Bias | Verharren im Sparkonto | 29% der Zielgruppe |

### 1.2 Zielsetzung

Das Tutorial soll:
1. **Selbsterkenntnis fördern** – Kunden identifizieren ihren Anlegertyp
2. **Entscheidungskomplexität reduzieren** – Maximal 3 Optionen pro Schritt
3. **Vertrauen aufbauen** – Migros-Werte (Fairness, Transparenz) aktivieren
4. **Zur Handlung führen** – Klarer, segmentspezifischer Call-to-Action

---

## 2. Verhaltensökonomische Grundlagen

### 2.1 Eingesetzte Mechanismen

Das Tutorial integriert **10 evidenzbasierte Behavioral Mechanisms**:

| # | Mechanismus | Screen | Evidenz |
|---|-------------|--------|---------|
| 1 | Time Anchoring | Welcome | Benartzi & Thaler (2007) |
| 2 | Trust Priming | Welcome | Fehr & Gächter (2000) |
| 3 | Self-Categorization | Frage 1 | Tajfel & Turner (1979) |
| 4 | Choice Architecture | Alle | Thaler & Sunstein (2008) |
| 5 | Autonomy Preservation | Navigation | Deci & Ryan (2000) |
| 6 | Commitment Device | Validierung | Rogers et al. (2015) |
| 7 | Social Proof | Persona | Cialdini (2001) |
| 8 | Anchoring | Preisvergleich | Tversky & Kahneman (1974) |
| 9 | Reframed Loss Aversion | Preisdifferenz | Kahneman & Tversky (1979) |
| 10 | Touchpoint Matching | CTA | Behavioral Targeting |

### 2.2 10C-Framework Mapping

| Tutorial-Element | 10C Dimension | Intervention |
|------------------|---------------|--------------|
| Willkommen | AWARE (AU) | Attention Capture |
| Frage 1 | WHO (AAA) | Self-Categorization |
| Frage 2 | WHAT (C) | Preference Elicitation |
| Validierung | READY (AV) | Commitment Device |
| Persona-Match | WHAT (C.S) | Social Utility |
| Preisvergleich | WHAT (C.F) | Financial Utility |
| CTA | STAGE (AW) | Journey Advancement |

---

## 3. Tutorial-Architektur

### 3.1 Flow-Übersicht

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   SCREEN 1        SCREEN 2        SCREEN 3        SCREEN 4         │
│   ─────────       ─────────       ─────────       ─────────        │
│   Willkommen  →   Frage 1    →    Frage 2    →   Validierung       │
│   (Trust)         (Identität)     (Vertiefung)   (Commitment)      │
│                                                                     │
│                        │              │                             │
│                   ┌────┴────┐    ┌────┴────┐                       │
│                   ▼    ▼    ▼    ▼    ▼    ▼                       │
│                   A    B    C    a    b    c                       │
│                                                                     │
│                                                                     │
│   SCREEN 5        SCREEN 6        SCREEN 7                         │
│   ─────────       ─────────       ─────────                        │
│   Persona    →    Ergebnis   →    CTA                              │
│   (Social Proof)  (Vergleich)     (Aktion)                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Routing-Logik

| Frage 1 | Frage 2 | Ergebnis |
|---------|---------|----------|
| A: Selbst entscheiden | a: Kein Sicherheitsnetz | **ExO-Depot** |
| A: Selbst entscheiden | b: Mit Sicherheitsnetz | **Depot Plus** |
| B: Mit Rückhalt | a: Bei Bedarf | **Depot Plus** |
| B: Mit Rückhalt | b: Regelmässig | **Depot Plus** (PAB-Hinweis) |
| C: Profis vertrauen | a: Punktuell | **Depot Plus** |
| C: Profis vertrauen | b: Proaktiv | **PAB** |

**Design-Rationale:** Die Routing-Logik ist bewusst so gestaltet, dass **Depot Plus** als Default-Ergebnis für ambivalente Antworten fungiert. Dies entspricht der strategischen Positionierung als "psychologische Brücke" zwischen Autonomie und Sicherheit.

---

## 4. Screen-Spezifikationen

### Screen 1: Willkommen

**Ziel:** Trust Priming, Low-Threshold Entry

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│           WELCHES ANLAGEPRODUKT PASST ZU DIR?                       │
│                                                                     │
│           Finde es heraus – in nur 2 Minuten.                       │
│                                                                     │
│     ┌─────────┐      ┌─────────┐      ┌─────────┐                  │
│     │   🎯    │      │   🤝    │      │   🛡️    │                  │
│     │  ExO    │      │  Depot  │      │   PAB   │                  │
│     │  Depot  │      │  Plus   │      │         │                  │
│     └─────────┘      └─────────┘      └─────────┘                  │
│                                                                     │
│           Keine Tricks, nur Klarheit. Versprochen.                  │
│                                                                     │
│                  ┌──────────────────────┐                          │
│                  │   Jetzt starten →    │                          │
│                  └──────────────────────┘                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Behavioral Elements:**
- "2 Minuten" → Time Anchoring (reduziert wahrgenommenen Aufwand)
- "Keine Tricks" → Trust Priming (aktiviert Migros-Markenwerte)
- Drei Icons → Vorschau ohne Overwhelm

---

### Screen 2: Frage 1 – Entscheidungsstil

**Ziel:** Self-Categorization, Identitätsaktivierung

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ← Zurück                                      Frage 1 von 2        │
│                                                                     │
│        WIE TRIFFST DU ANLAGEENTSCHEIDUNGEN AM LIEBSTEN?             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  🎯  ICH ENTSCHEIDE SELBST                                  │   │
│  │                                                             │   │
│  │  Ich kenne mich aus und will volle Kontrolle.               │   │
│  │  Gebühren für Beratung, die ich nicht brauche? Nein danke.  │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  🤝  ICH ENTSCHEIDE, ABER MIT RÜCKHALT                      │   │
│  │                                                             │   │
│  │  Ab und zu eine zweite Meinung gibt mir Sicherheit.         │   │
│  │  Kontrolle behalten – aber wissen, dass jemand da ist.      │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  🛡️  ICH VERTRAUE LIEBER PROFIS                             │   │
│  │                                                             │   │
│  │  Anlegen ist komplex – ich will jemanden an meiner Seite,   │   │
│  │  der den Überblick behält und mich aktiv informiert.        │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Behavioral Elements:**
- Selbstzuschreibung statt Fremdzuordnung (höhere Akzeptanz)
- Drei Optionen → Choice Architecture (kein Overload)
- Zurück-Button → Autonomie erhalten (kein Lock-in-Gefühl)

---

### Screen 3a: Frage 2 – Selbstentscheider-Pfad

**Ziel:** Differenzierung ExO vs. Depot Plus

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ← Zurück                                      Frage 2 von 2        │
│                                                                     │
│        WIE WICHTIG IST DIR EIN SICHERHEITSNETZ?                     │
│                                                                     │
│        Du hast gesagt, du entscheidest gerne selbst. Top!           │
│        Eine letzte Frage:                                           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  💪  NICHT NÖTIG                                            │   │
│  │                                                             │   │
│  │  Ich stehe zu meinen Entscheidungen.                        │   │
│  │  Wenn ich Hilfe brauche, frage ich aktiv.                   │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  🔒  WÄRE GUT ZU WISSEN                                     │   │
│  │                                                             │   │
│  │  Ich entscheide selbst – aber es beruhigt mich,             │   │
│  │  dass jemand da ist, falls ich mal unsicher bin.            │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Screen 3b: Frage 2 – Orientierungssuchende-Pfad

**Ziel:** Bestätigung Depot Plus, Frequenz-Ermittlung

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ← Zurück                                      Frage 2 von 2        │
│                                                                     │
│        WIE OFT MÖCHTEST DU MIT EINEM BERATER SPRECHEN?              │
│                                                                     │
│        Du möchtest selbst entscheiden, aber mit Rückhalt.           │
│        Das verstehen wir gut. Wie intensiv soll der Kontakt sein?   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  📞  BEI BEDARF                                             │   │
│  │                                                             │   │
│  │  Wenn ich Fragen habe oder unsicher bin,                    │   │
│  │  möchte ich jemanden erreichen können.                      │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  📅  REGELMÄSSIG                                            │   │
│  │                                                             │   │
│  │  Ich möchte mindestens einmal pro Jahr                      │   │
│  │  ein Gespräch zur Standortbestimmung.                       │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Screen 3c: Frage 2 – Beziehungssuchende-Pfad

**Ziel:** Differenzierung Depot Plus vs. PAB

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ← Zurück                                      Frage 2 von 2        │
│                                                                     │
│        WIE ENG SOLL DIE BEGLEITUNG SEIN?                            │
│                                                                     │
│        Du vertraust lieber Profis – das ist eine kluge Entscheidung.│
│        Wie aktiv soll dein Berater sein?                            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  🙋  PUNKTUELL                                              │   │
│  │                                                             │   │
│  │  Ich melde mich, wenn ich etwas brauche.                    │   │
│  │  Mein Berater muss nicht von sich aus aktiv werden.         │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  📊  PROAKTIV                                               │   │
│  │                                                             │   │
│  │  Mein Berater soll mich auf dem Laufenden halten            │   │
│  │  und mir Vorschläge machen, bevor ich fragen muss.          │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Screen 4: Validierung

**Ziel:** Commitment Device, Selbstbestätigung

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ← Zurück                                    Nochmal starten ↻      │
│                                                                     │
│                                                                     │
│        DEIN ANLEGERTYP: ORIENTIERUNGSSUCHEND                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  🤝  Das bedeutet:                                          │   │
│  │                                                             │   │
│  │  Du möchtest selbst entscheiden, aber schätzt               │   │
│  │  professionelle Einschätzungen als Rückhalt.                │   │
│  │                                                             │   │
│  │  Kontrolle JA – aber mit Sicherheitsnetz.                   │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│                                                                     │
│        ┌───────────────────┐    ┌───────────────────┐              │
│        │                   │    │                   │              │
│        │  ✓ Ja, das passt! │    │  ← Nochmal von    │              │
│        │                   │    │    vorne          │              │
│        └───────────────────┘    └───────────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Behavioral Elements:**
- Explizite Bestätigung → Commitment Device
- "Nochmal von vorne" → Autonomie (kein Zwang)

---

### Screen 5: Persona-Match

**Ziel:** Social Proof, Similarity Heuristic

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                                                                     │
│        DAS SAGEN ANDERE WIE DU:                                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  👩‍💼  SANDRA, 42, MARKETING-MANAGERIN                        │   │
│  │                                                             │   │
│  │  «Ich wollte nicht alles abgeben, aber auch nicht           │   │
│  │   alleine dastehen. Depot Plus gibt mir genau das –         │   │
│  │   Kontrolle mit Rückendeckung.                              │   │
│  │                                                             │   │
│  │   Wenn ich unsicher bin, ruf ich an. Fertig.»               │   │
│  │                                                             │   │
│  │  ─────────────────────────────────────────────────────────  │   │
│  │                                                             │   │
│  │  ⭐⭐⭐⭐⭐                                                   │   │
│  │                                                             │   │
│  │  87% der Orientierungssuchenden wählen Depot Plus           │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│                                                                     │
│                  ┌────────────────────────────────┐                 │
│                  │  Weiter zu deiner Empfehlung → │                 │
│                  └────────────────────────────────┘                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Persona-Varianten:**

| Ergebnis | Persona | Quote | Social Proof |
|----------|---------|-------|--------------|
| ExO-Depot | Luca, 29, IT-Consultant | "Ich trade gerne selbst..." | 73% wählen ExO |
| Depot Plus | Sandra, 42, Marketing-Managerin | "Kontrolle mit Rückendeckung..." | 87% wählen DP |
| PAB | Jean-Pierre, 56, Arzt | "Meine Zeit ist begrenzt..." | 91% wählen PAB |

---

### Screen 6: Ergebnis + Preisvergleich

**Ziel:** Anchoring, Fairness-Wahrnehmung, Entscheidungsbestätigung

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ← Zurück zum Quiz                      Ergebnis per E-Mail ✉️      │
│                                                                     │
│                                                                     │
│        DEINE EMPFEHLUNG: DEPOT PLUS                                 │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  Produkt              │ Kosten/Jahr* │ Beratung │ Für dich? │   │
│  │  ─────────────────────┼──────────────┼──────────┼───────────│   │
│  │  ExO-Depot            │ ab CHF 90.-  │ Keine    │           │   │
│  │  ─────────────────────┼──────────────┼──────────┼───────────│   │
│  │  ★ DEPOT PLUS ★       │ ab CHF 150.- │ Bei      │    ✓      │   │
│  │                       │              │ Bedarf   │ EMPFOHLEN │   │
│  │  ─────────────────────┼──────────────┼──────────┼───────────│   │
│  │  Pers. Anlageberatung │ ab CHF 300.- │ Laufend  │           │   │
│  │                                                             │   │
│  │  *Beispiel bei CHF 60'000 Depotvolumen                      │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │   │
│  │  ★ DEINE EMPFEHLUNG: DEPOT PLUS                             │   │
│  │                                                             │   │
│  │  ✓ Du entscheidest – mit professionellem Rückhalt           │   │
│  │  ✓ Beratung bei Bedarf, ohne Abo-Zwang                      │   │
│  │  ✓ Persönlicher Ansprechpartner für deine Fragen            │   │
│  │  ✓ Faire, transparente Kosten                               │   │
│  │                                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│                                                                     │
│  💡 Der Unterschied zum ExO-Depot?                                  │
│     Für nur CHF 60.- mehr pro Jahr hast du einen Experten           │
│     an deiner Seite, wann immer du ihn brauchst.                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Behavioral Elements:**
- Vergleichstabelle → Anchoring (mittlere Option attraktiv)
- "Für nur CHF 60.- mehr" → Reframed Loss Aversion
- Checkmarks → Benefit-Framing

---

### Screen 7: Call-to-Action

**Ziel:** Touchpoint-spezifische Conversion

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                                                                     │
│        BEREIT FÜR DEN NÄCHSTEN SCHRITT?                             │
│                                                                     │
│                                                                     │
│                  ┌────────────────────────────────┐                 │
│                  │                                │                 │
│                  │  Beratungstermin vereinbaren → │                 │
│                  │                                │                 │
│                  └────────────────────────────────┘                 │
│                                                                     │
│        ─────────────────────────────────────────────────────        │
│                                                                     │
│        ┌─────────────────┐    ┌─────────────────────────┐          │
│        │ Rückruf         │    │ Erst mal mehr erfahren  │          │
│        │ anfordern       │    │                         │          │
│        └─────────────────┘    └─────────────────────────┘          │
│                                                                     │
│                                                                     │
│        Was passiert beim Beratungstermin?                           │
│        • Wir lernen deine Situation kennen (ca. 30 Min.)            │
│        • Du bekommst eine erste Einschätzung                        │
│        • Keine Verpflichtung – nur Klarheit                         │
│                                                                     │
│                                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                     │
│  ← Zurück zum Vergleich       │       Ergebnis per E-Mail senden    │
│                                                                     │
│  Fragen? Ruf uns an: 0848 845 400                                   │
│  Oder schreib uns: anlegen@migrosbank.ch                            │
│                                                                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                     │
│  🔒 Deine Angaben werden nicht gespeichert.                         │
│     Keine Tricks, nur Klarheit.                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**CTA-Varianten nach Ergebnis:**

| Ergebnis | Primary CTA | Secondary CTAs |
|----------|-------------|----------------|
| ExO-Depot | "Jetzt im E-Banking eröffnen" | Mehr erfahren, Vergleich speichern |
| Depot Plus | "Beratungstermin vereinbaren" | Rückruf, Mehr erfahren |
| PAB | "Persönlichen Berater kennenlernen" | Rückruf, Filiale finden |

---

## 5. Erwartete Ergebnisse

### 5.1 Routing-Verteilung

Basierend auf den verhaltensbasierten Kundensegmenten der Migros Bank:

| Segment | Anteil Kundenbasis | Wahrscheinlichstes Ergebnis |
|---------|-------------------|----------------------------|
| Selbstentscheider | 12% | ExO-Depot (73%) / Depot Plus (27%) |
| Orientierungssuchende | 39% | Depot Plus (87%) |
| Beziehungssuchende | 12% | Depot Plus (45%) / PAB (55%) |
| Schwellenängstliche | 35% | Depot Plus (65%) / ExO (35%) |
| Traditionskunden | 2% | PAB (91%) |

**Aggregierte Erwartung:**

| Produkt | Erwarteter Anteil |
|---------|-------------------|
| ExO-Depot | ~15% |
| **Depot Plus** | **~65%** |
| PAB | ~20% |

### 5.2 KPIs für Erfolgsmessung

| KPI | Zielwert | Messmethode |
|-----|----------|-------------|
| Completion Rate | > 75% | Tutorial abgeschlossen / gestartet |
| CTA Conversion | > 25% | CTA-Klicks / Tutorial abgeschlossen |
| Depot Plus Anteil | 60-70% | Ergebnis-Verteilung |
| Time to Complete | < 3 Min | Durchschnittliche Verweildauer |
| Bounce Rate Screen 2 | < 20% | Abbrüche bei Frage 1 |

---

## 6. Implementierungsempfehlungen

### 6.1 Technische Umsetzung

**Empfohlene Formate:**
- **Web:** Single-Page Application mit Slide-Transitions
- **App:** Native Carousel oder WebView
- **E-Banking:** Integration als Modal oder eigener Bereich

### 6.2 A/B-Test-Kandidaten

| Element | Variante A | Variante B |
|---------|------------|------------|
| Headline | "Welches Produkt passt zu dir?" | "Finde dein Anlageprodukt" |
| Persona | Mit Foto | Nur Icon + Name |
| Preisdarstellung | CHF/Jahr | CHF/Monat |
| CTA-Text | "Beratungstermin vereinbaren" | "Jetzt Termin buchen" |

### 6.3 Tracking-Setup

```
Event-Tracking (empfohlen):
├── tutorial_started
├── screen_viewed (screen_number, screen_name)
├── question_answered (question_id, answer_id)
├── result_shown (product_recommendation)
├── cta_clicked (cta_type)
├── tutorial_completed
└── tutorial_abandoned (last_screen)
```

---

## 7. Nächste Schritte

| # | Aktion | Verantwortlich | Termin |
|---|--------|----------------|--------|
| 1 | Review durch Migros Bank Produktteam | Migros Bank | KW 5 |
| 2 | Finalisierung Texte und Visuals | FehrAdvice | KW 6 |
| 3 | Technische Umsetzung (Prototyp) | Migros Bank IT | KW 7-8 |
| 4 | User Testing (n=30) | FehrAdvice | KW 9 |
| 5 | Iteration basierend auf Feedback | Gemeinsam | KW 10 |
| 6 | Go-Live | Migros Bank | KW 12 |

---

## Anhang A: Vollständige Texte

### A.1 Screen 1: Willkommen

**Headline:** Welches Anlageprodukt passt zu dir?

**Subline:** Finde es heraus – in nur 2 Minuten.

**Trust-Line:** Keine Tricks, nur Klarheit. Versprochen.

**CTA:** Jetzt starten →

---

### A.2 Screen 2: Frage 1

**Frage:** Wie triffst du Anlageentscheidungen am liebsten?

**Option A:**
- Label: 🎯 Ich entscheide selbst
- Beschreibung: Ich kenne mich aus und will volle Kontrolle. Gebühren für Beratung, die ich nicht brauche? Nein danke.

**Option B:**
- Label: 🤝 Ich entscheide, aber mit Rückhalt
- Beschreibung: Ab und zu eine zweite Meinung gibt mir Sicherheit. Ich will die Kontrolle behalten – aber wissen, dass jemand da ist, wenn ich Fragen habe.

**Option C:**
- Label: 🛡️ Ich vertraue lieber Profis
- Beschreibung: Anlegen ist komplex – ich will jemanden an meiner Seite, der den Überblick behält und mich aktiv informiert.

---

### A.3 Anlegertyp-Beschreibungen

**Selbstentscheider:**
Du weisst, was du willst, und handelst eigenständig. Kosten und Effizienz sind dir wichtig. Du brauchst keine Beratung – du brauchst gute Tools.

**Orientierungssuchend:**
Du möchtest selbst entscheiden, aber schätzt professionelle Einschätzungen als Rückhalt. Kontrolle JA – aber mit Sicherheitsnetz.

**Beziehungssuchend:**
Du legst Wert auf eine vertrauensvolle Partnerschaft mit deinem Berater. Anlegen ist Teamarbeit – und du willst den besten Partner an deiner Seite.

---

## Anhang B: Persona-Zitate

### B.1 ExO-Depot (Luca, 29)

> «Ich trade gerne selbst und will keine Gebühren für Beratung zahlen, die ich nicht brauche. Das ExO-Depot ist perfekt für mich – günstig, schnell und ich hab die volle Kontrolle.»

### B.2 Depot Plus (Sandra, 42)

> «Ich wollte nicht alles abgeben, aber auch nicht alleine dastehen. Depot Plus gibt mir genau das – Kontrolle mit Rückendeckung. Wenn ich unsicher bin, ruf ich an. Fertig.»

### B.3 PAB (Jean-Pierre, 56)

> «Meine Zeit ist begrenzt, und Anlegen ist nicht mein Fachgebiet. Mit meinem Berater bei der Migros Bank fühle ich mich in guten Händen. Er kennt meine Situation und meldet sich, wenn etwas wichtig ist.»

---

*Erstellt von FehrAdvice & Partners AG*
*Verhaltensökonomische Beratung | Zürich*

**Kontakt:**
FehrAdvice & Partners AG
Klausstrasse 20
8008 Zürich

Tel: +41 44 256 79 00
E-Mail: info@fehradvice.com
Web: www.fehradvice.com
