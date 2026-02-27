# F5 — A/B-Test Design & Messaging Copy
## Xcite → A1 Youth · M2-Kommunikationstexte · Alle Segmente

**Session:** EBF-S-2026-02-20-ORG-001
**Modell:** MOD-TEL-001 v1.2.1
**Version:** 1.0 · 2026-02-20
**Grundlage:** F4 Transition Playbook; λ=2.1, ρ_tech=0.38
**Zweck:** Ready-to-deploy Messaging-Varianten für den M2-A/B-Test (n=2.000)

---

## 1. A/B-Test Setup

### Testgruppe & Split

| Gruppe | Segment | n | Variante |
|--------|---------|---|----------|
| G1a | HVV · Hedonisten | 300 | A |
| G1b | HVV · Hedonisten | 300 | B |
| G1c | HVV · Hedonisten | 300 | C |
| G2a | LVV · Adaptiv-Pragmatisch | 200 | A |
| G2b | LVV · Adaptiv-Pragmatisch | 200 | C |
| Control | HVV · gemischt | 300 | keine Kommunikation |
| Backup | LVV · gemischt | 200 | keine Kommunikation |

**Total Testgruppe: 1.800 + 500 Control = 2.300**
Zufällige Ziehung aus CRM-Tag: `xcite_bestand` × `milieu_flag`

### Primär-KPI: Churn-Rate 30 Tage post-Aussendung
**Schwelle:**
- Churn ≤ Baseline → Variante GO für Rollout
- Churn +1–3pp über Baseline → Optimierung nötig
- Churn >+3pp über Baseline → Variante STOP, Creative-Überarbeitung

### Sekundär-KPIs
- SMS/Push Open Rate (Proxy: Link-Click auf FAQ)
- Inbound-Anrufe «Was ändert sich?» (Ziel: <3% der Kontaktierten)
- In-App-Engagement nach Push (Öffnungsrate MeinA1)

### Zeitplan
- **M2 Woche 1:** Test-Aussendung (SMS + Push parallel)
- **M2 Woche 2–4:** 30-Tage-Beobachtungsfenster
- **M2 Woche 5:** Auswertung, Winner-Variante für Rollout M4 festlegen

---

## 2. Die 3 Varianten — Behavioural Fundierung

| Variante | Kern-Mechanismus | Behavioral Basis |
|----------|-----------------|------------------|
| **A — Neutral** | Sachliche Information | Baseline; zeigt, ob pure Information Churn neutral hält |
| **B — Loss-Frame-Reversal** | Xcite = Vergangenheit/Defizit; Youth = Gewinn/Identität | λ=2.1 umkehren: Verlust liegt *vor* der Umbenennung |
| **C — Reassurance + Default** | Alles bleibt; keine Aktion nötig; passiert automatisch | ρ_tech=0.38 nutzen: Passivität arbeitet für Migration |

**Hypothese:** C > B > A für HVV (Bestandsloyale wollen Sicherheit).
B > C > A für LVV (Flexible wollen Upgrade-Narrativ).

---

## 3. Vollständige Messaging-Copy

### Kanal-Spezifikationen

| Kanal | Max. Zeichen | Ton | Ziel |
|-------|-------------|-----|------|
| **SMS** | 160 Zeichen (1 SMS-Einheit) | Persönlich, direkt | Awareness, kein Churn |
| **App-Push Titel** | 45 Zeichen | Neugier-weckend | App öffnen |
| **App-Push Body** | 90 Zeichen | Beruhigend / Benefit | FAQ lesen |
| **E-Mail Betreff** | 50 Zeichen | Handlungsarm, info-orientiert | Öffnen |
| **E-Mail Pre-Header** | 85 Zeichen | Klärt sofort: kein Preis-Wechsel | Churn-Prävention |

---

### VARIANTE A — Neutral

**Behavioral-Ziel:** Basis-Kommunikation ohne Framing. Setzt den Benchmark.

#### SMS (158 Zeichen)
```
Hallo! Dein A1-Tarif bekommt einen neuen Namen: A1 Youth.
Preis, Daten, Nummer – alles bleibt. Du musst nichts tun.
Mehr Infos: a1.at/youth
```

#### App-Push
- **Titel (38 Zeichen):** `Dein Tarif heisst jetzt A1 Youth`
- **Body (82 Zeichen):** `Neuer Name, alles beim Alten. Preis und Leistung bleiben unverändert.`

#### E-Mail
- **Betreff (46 Zeichen):** `Dein A1-Tarif bekommt einen neuen Namen`
- **Pre-Header (84 Zeichen):** `Keine Änderung bei Preis oder Leistung – nur der Name wird besser: A1 Youth ist da.`

---

### VARIANTE B — Loss-Frame-Reversal

**Behavioral-Ziel:** λ=2.1 umkehren. Der Verlust liegt in der Vergangenheit (Xcite = unsichtbar), der Gain liegt in der Gegenwart (Youth = sichtbar). Kund:innen gewinnen Identität zurück.

#### SMS — HVV (159 Zeichen)
```
Xcite hat dich gut vernetzt. Aber nach aussen war der Name unsichtbar.
Ab jetzt: A1 Youth. Dein Tarif, endlich mit einem Namen der zu dir passt.
a1.at/youth
```

#### SMS — LVV (158 Zeichen)
```
Neu: Dein Tarif heisst A1 Youth. Nicht weil sich etwas ändert –
sondern weil ein Name der nichts sagt, dir nichts bringt.
Jetzt mit Profil: a1.at/youth
```

#### App-Push — HVV
- **Titel (42 Zeichen):** `Xcite war gut. A1 Youth ist dein Name.`
- **Body (88 Zeichen):** `Dein Tarif, jetzt mit einem Namen der wirklich zu dir passt. Preis bleibt. Alles bleibt.`

#### App-Push — LVV
- **Titel (39 Zeichen):** `Upgrade: Dein Tarif heisst A1 Youth`
- **Body (85 Zeichen):** `Gleiche Leistung, stärkeres Profil. A1 Youth gibt dir einen Namen, der etwas aussagt.`

#### E-Mail — HVV
- **Betreff (47 Zeichen):** `Dein Tarif bekommt einen Namen, der zu dir passt`
- **Pre-Header (83 Zeichen):** `Xcite war unsichtbar. A1 Youth macht dich sichtbar – bei gleichem Preis, gleicher Leistung.`

#### E-Mail — LVV
- **Betreff (44 Zeichen):** `A1 Youth: Dein neuer Tarif-Name ist da`
- **Pre-Header (80 Zeichen):** `Gleiche Leistung, stärkeres Profil. Xcite hatte keinen Auftritt – A1 Youth schon.`

---

### VARIANTE C — Reassurance + Default

**Behavioral-Ziel:** ρ_tech=0.38 nutzen. Passivität ist die richtige Antwort. Kein Opt-In, kein aktiver Schritt. «Es passiert für dich.» Maximale Beruhigung, minimale Reibung.

#### SMS — HVV (160 Zeichen)
```
Hey! Dein A1-Tarif wird automatisch zu A1 Youth – du musst nichts tun.
Gleicher Preis, gleiches Angebot, gleiche Nummer. Nur der Name wird besser.
a1.at/youth
```

#### SMS — LVV (157 Zeichen)
```
Info: Dein Tarif heisst ab [Datum] A1 Youth.
Passiert automatisch für dich – kein Klick, kein Formular.
Was sich ändert? Nur der Name. a1.at/youth
```

#### App-Push — HVV
- **Titel (41 Zeichen):** `Du wirst automatisch A1 Youth 👋`
- **Body (90 Zeichen):** `Nichts ändert sich ausser dem Namen. Kein Schritt nötig – es passiert einfach für dich.`

#### App-Push — LVV
- **Titel (38 Zeichen):** `A1 Youth: Dein neuer Name kommt bald`
- **Body (87 Zeichen):** `Automatisch, ohne Formular. Gleiche Leistung. Nur der Name wird klarer. Mehr: a1.at/youth`

#### E-Mail — HVV
- **Betreff (48 Zeichen):** `Nichts zu tun: Dein Tarif wird A1 Youth`
- **Pre-Header (85 Zeichen):** `Du wirst automatisch umgestellt – kein Schritt nötig. Preis, Leistung, Nummer: alles bleibt.`

#### E-Mail — LVV
- **Betreff (44 Zeichen):** `Dein Tarif-Upgrade läuft automatisch ab`
- **Pre-Header (82 Zeichen):** `A1 Youth kommt zu dir – du musst nichts tun. Gleiche Leistung, stärkerer Name.`

---

## 4. Milieu-spezifischer Content-Layer (M5 Rollout)

*Zusatz-Content für Sinus-Milieu-gezielte Digital-/Social-Kampagne im M5-Push. Kein Ersatz für die A/B-Test-Varianten — zusätzlicher Layer auf Social + Display.*

### Hedonisten (Tobias-Profil, ~30% der Basis)

**Behavioral-Risiko:** Magenta-Confusion («dann geh ich halt zu Magenta»). Sprachlich muss A1 Youth eigenständig wirken — keine Überlappung mit «Mobile Young»-Vocabulary.

**Verboten:** «Young», «Jugend», «jugendlich», Corporate-Ton, Tarif-Sprache
**Geboten:** Peer-Sprache, Energie, Zugehörigkeit, kurz, visuell-dominant

```
Headline:   Youth ist die Crew.
Sub:        A1 Youth — dein Tarif, jetzt mit einem Namen.
CTA:        Jetzt Teil der Crew
Claim:      Wir benennen uns um. Du bleibst dabei.
```

```
Headline:   Dein Netz. Deine Leute. Dein Youth.
Sub:        Gleicher Tarif. Endlich ein Name, der zählt.
CTA:        Zum Youth-Tarif
```

**SMS-Tone (Hedonisten, keine Standard-Variante — rein für Social Retargeting):**
```
Xcite war gestern. A1 Youth bist du.
Dein Tarif, jetzt mit Profil. a1.at/youth
```
*(79 Zeichen)*

---

### Kosmopolitische Individualisten (Lukas-Profil, ~20% der Basis)

**Behavioral-Basis:** γ_SE_kos=+0.35 (stärkster Komp.-Koeffizient). Identitäts-Upgrade aktiviert höchsten Utility-Gain. Sprache: cool, eigenständig, leicht bilingual OK, keine Dialekt-Anker.

**Verboten:** Zu österreichisch-spezifisch, bieder, «Jugend»
**Geboten:** Identity-Forward, global-feeling, eigenständig positioniert

```
Headline:   Your network, your name.
Sub:        A1 Youth. Das war schon immer dein Tarif.
CTA:        A1 Youth entdecken
```

```
Headline:   Xcite? Das war der Platzhalter.
Sub:        A1 Youth ist der Name, den dein Tarif verdient hat.
CTA:        Jetzt A1 Youth
```

**App-Push (Kosmopoliten):**
- **Titel:** `Dein Tarif wächst: A1 Youth ist da`
- **Body:** `Identity upgrade – gleicher Preis, stärkerer Name. Du bist schon dabei.`

---

### Adaptiv-Pragmatische Mitte (Sofia-Profil, ~35% der Basis)

**Behavioral-Basis:** Funktionale Klarheit > Modernity. EINZIGES Milieu, wo Jugend simulationsbedingt gewonnen hat (54% vs. Youth 47%). Dieser Segment-Typ will Klarheit und Ehrlichkeit über Style.

**Verboten:** Hype, leere Versprechen, zu viel Framing, Lifestyle-Sprache
**Geboten:** Direkt, ehrlich, klar, nutzenorientiert

```
Headline:   Einfacher. Klarer. Dasselbe Angebot.
Sub:        A1 Youth ist jetzt der Name deines Tarifs.
            Preis, Daten, Nummer – alles bleibt.
CTA:        Was ändert sich? Nur der Name.
```

```
Headline:   Dein Tarif, jetzt leichter zu finden.
Sub:        A1 Youth ersetzt Xcite – Konditionen unverändert.
            Du musst nichts tun.
CTA:        Alle Infos auf einer Seite
```

**App-Push (Adaptiv-Pragmatisch):**
- **Titel:** `Dein Tarif: Xcite wird A1 Youth`
- **Body:** `Gleiche Konditionen. Einfacherer Name. Kein Handlungsbedarf.`

---

## 5. FAQ-Content: «Was ändert sich?»

*Landingpage a1.at/youth-info — primäre Verlinkung aus allen SMS/Push-Varianten*

### Headline-Vorschlag:
**«A1 Youth ist da. Was bedeutet das für dich?»**

### FAQ-Block (bereit für Landingpage-Integration)

---

**❓ Muss ich etwas tun?**
> Nein. Die Umbenennung passiert automatisch. Du bekommst keine neue SIM, kein neues Formular, nichts zu unterschreiben.

---

**❓ Ändert sich mein Preis?**
> Nein. Dein Preis bleibt exakt gleich.

---

**❓ Ändert sich mein Datenvolumen oder meine Telefonnummer?**
> Nein. Alles bleibt wie es ist. Nur der Name deines Tarifs ändert sich — von Xcite zu A1 Youth.

---

**❓ Warum macht A1 das überhaupt?**
> «Xcite» war ein Name, der nach aussen nicht viel gesagt hat. A1 Youth sagt auf Anhieb: Das ist für dich. Es ist der gleiche Tarif — jetzt mit einem Namen, der zu dir passt.

---

**❓ Was ist mit meinem Vertrag?**
> Dein Vertrag bleibt unverändert. Alle Konditionen gelten weiterhin. Die Umbenennung ist keine Vertragsänderung.

---

**❓ Sehe ich A1 Youth jetzt in der MeinA1-App?**
> Ab [Datum] wird dein Tarif in der App als «A1 Youth» angezeigt. Davor siehst du noch «Xcite». Das ist alles.

---

**❓ Kann ich meinen Tarif wechseln, wenn mir der neue Name nicht gefällt?**
> Natürlich kannst du jederzeit zu einem anderen A1-Tarif wechseln — das war schon vorher so und bleibt so. Aber: Preis und Leistung von A1 Youth sind identisch mit Xcite. Nur der Name ist besser.

---

**❓ Was ist mit «A1 Kids» und «A1 Family» — wie passt A1 Youth dazu?**
> A1 Youth ist Teil der A1-Familienstruktur: Kids → Youth → Family. Wir bauen ein klares Portfolio, das zu deiner Lebensphase passt.

---

## 6. Rollout-Matrix: Wer bekommt welche Variante

### M4 Rollout (nach A/B-Test-Auswertung M2)

| Segment | Grösse (est.) | Kanal | Variante | Timing |
|---------|---------------|-------|----------|--------|
| HVV · Hedonisten | ~29k | SMS + App-Push | Winner aus G1-Test | M4 Woche 1 |
| HVV · Kosmopoliten | ~19k | SMS + App-Push | Winner aus G1-Test + Kos-Layer | M4 Woche 1 |
| HVV · Adaptiv-Pragmatisch | ~34k | SMS + App-Push | Winner aus G1-Test | M4 Woche 1–2 |
| HVV · Rest | ~15k | SMS | Variante C (Default-safe) | M4 Woche 2 |
| LVV · alle Milieus | ~52k | App-Push + E-Mail | Winner aus G2-Test | M4 Woche 3–4 |

**Sequenz-Begründung:** HVV zuerst — höheres Churn-Risiko, braucht persönlichere Ansprache. LVV eine Woche später — E-Mail-Kanal ist günstiger, LVV reagiert auf Value-Add.

### M5 Second-Touch (für 38% passive Gruppe)

| Identifikation | Massnahme | Kanal |
|----------------|-----------|-------|
| M4 SMS delivered, kein FAQ-Click, kein Churn | Persistent App-Banner + Short Reminder-SMS | App |
| M4 Push delivered, App nicht geöffnet | In-App Banner bei nächstem App-Start | In-App |

**Reminder-SMS (Passiv-Gruppe, M5, 107 Zeichen):**
```
Kurze Info: Ab [Datum] heisst dein Tarif A1 Youth.
Passiert automatisch. Kein Schritt nötig. a1.at/youth
```

---

## 7. Behavioral Red Lines — Was in keiner Variante erscheinen darf

| ❌ Verbotene Formulierung | Grund |
|--------------------------|-------|
| «Xcite wird abgelöst» / «läuft aus» / «eingestellt» | Aktiviert λ=2.1 Verlustrahmen |
| «Um fortzufahren, bestätige bitte...» | Opt-In = Entscheidungsmoment = Churn-Gelegenheit |
| «Möchtest du wechseln zu A1 Youth?» | Framing als aktiver Wechsel, nicht als Upgrade |
| «Neuer Tarif» | Falsch; es ist der gleiche Tarif mit neuem Namen |
| «Young» im Zusammenhang mit A1 | Magenta-Confusion für Hedonisten |
| «Jugend» / «jugendlich» | Soziale Kosten bei Kosmopoliten + Hedonisten |
| Preis-Vergleich mit Mitbewerbern | Öffnet Preisvergleichs-Mindset, nachteilig |
| Zu viele Optionen / Alternativen nennen | Erhöht Entscheidungsaufwand → inaction bias → Churn-Risiko |

---

## Anhang: Zeichenzählung SMS-Varianten

| Variante | Segment | Zeichen | Status |
|----------|---------|---------|--------|
| A | — | 158 | ✅ 1 SMS |
| B | HVV | 159 | ✅ 1 SMS |
| B | LVV | 158 | ✅ 1 SMS |
| C | HVV | 160 | ✅ 1 SMS |
| C | LVV | 157 | ✅ 1 SMS |
| Hedonisten Social | — | 79 | ✅ kurz |
| Reminder M5 | Passiv | 107 | ✅ 1 SMS |

**Alle Varianten: 1 SMS-Einheit (≤160 Zeichen). Keine Mehrteil-SMS. Kostengünstig.**

---

**Modell-Referenz:** MOD-TEL-001 v1.2.1 · λ=2.1 · ρ_tech=0.38
**Vorherige Files:** F1–F3 (Modell), F4 (Playbook)
**Branch:** `claude/check-a1-model-RVR1g`
