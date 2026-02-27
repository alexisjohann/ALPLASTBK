# OKB-002: Google Workspace Handoff

> **Operational Knowledge Base Entry**
> **Zweck:** CI/CD-Referenz für externe Design-Tools (NotebookLM, Slides, Docs)

---

## Übersicht

| Feld | Wert |
|------|------|
| **OKB-ID** | OKB-002 |
| **Name** | Google Workspace Handoff |
| **Ablage** | `data/customers/{kunde}/ci-cd/google-workspace-handoff.yaml` |
| **Template** | `templates/google-workspace-handoff-template.yaml` |

---

## Was ist das?

Eine **einfache YAML-Datei** pro Kunde mit CI/CD-Informationen für externe Tools:

| Enthält | Nicht enthalten |
|---------|-----------------|
| Farben (Hex-Codes) | Projekt-spezifische Inhalte |
| Schriften (Google Fonts) | Layout-Anweisungen |
| Logo-Status | Druckbare Dokumente |
| Orthographie-Regeln | Content-Mapping |
| AI-Prompt für NotebookLM | |

---

## Ablage

```
data/customers/{kunde}/ci-cd/
├── google-workspace-handoff.yaml   ← DIESES FILE
├── corporate-identity.yaml         # Vollständige CI-Doku
├── colors/
├── fonts/
└── logos/
```

---

## Template-Struktur

```yaml
client: "Kundenname"
ci_status: "COMPLETE | PARTIAL | INCOMPLETE"

colors:
  primary: "#024079"
  text_dark: "#1A1A1A"
  chart: ["#024079", "#549EDE"]

fonts:
  headline: "Inter"
  body: "Open Sans"
  google_fonts_import: "Inter:wght@700|Open+Sans:wght@400"

orthography:
  eszett: false        # ss statt ß
  gendering: ":"       # Kund:innen

notebooklm_prompt: |
  Gestalte für {client}:
  Primärfarbe: {primary}
  Schrift: {headline}
```

---

## Verwendung

### Mit NotebookLM

1. Markdown-Deliverable hochladen
2. `google-workspace-handoff.yaml` hochladen
3. Prompt aus YAML kopieren oder:
   ```
   Erstelle Präsentation gemäss YAML-Richtlinien.
   ```

### Mit Google Slides

1. YAML öffnen → Hex-Codes kopieren
2. Farben einrichten: Folie → Hintergrund → Benutzerdefiniert
3. Fonts: Format → Schriftart → Weitere Schriftarten

---

## Beispiel: prio.swiss

```yaml
# data/customers/prio-swiss/ci-cd/google-workspace-handoff.yaml

client: "prio.swiss"
ci_status: "INCOMPLETE"

colors:
  primary: "#0077B6"        # [PLACEHOLDER]
  text_dark: "#1A1A1A"
  chart: ["#0077B6", "#48CAE4", "#00B4D8"]

fonts:
  headline: "Inter"
  body: "Inter"

orthography:
  eszett: false
  gendering: ":"

notebooklm_prompt: |
  Gestalte für prio.swiss (Krankenversicherer):
  - Primär: #0077B6
  - Schrift: Inter
  - Stil: Sachlich, schweizerisch
```

---

## Branchen-Defaults

Falls Kunden-CI fehlt:

| Branche | Primärfarbe | Font |
|---------|-------------|------|
| Gesundheit | #0077B6 (Blau) | Inter |
| Finanz | #1E3A5F (Dunkelblau) | Roboto |
| Energie | #22C55E (Grün) | Lato |
| Öffentlich | #DC2626 (Rot) | Arial |

---

*Erstellt: 2026-02-04 | Version: 1.1*
