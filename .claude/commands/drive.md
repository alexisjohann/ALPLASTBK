# /drive - Google Drive Datei-Integration

Lade Dateien von Google Drive herunter und integriere sie ins Repository. Umgeht die Sandbox-Restriktion via GitHub Actions (der Runner hat uneingeschraenkten Internet-Zugang).

## Verwendung

```
/drive <FILE_ID>
/drive <Google-Drive-URL>
/drive download <FILE_ID> [output_name]
/drive split <FILE_ID> [output_name]
/drive status
/drive pull
```

## Anweisungen

### Schritt 0: File-ID extrahieren

Wenn der User eine Google Drive URL teilt, die File-ID extrahieren:
```
https://drive.google.com/file/d/<FILE_ID>/view?usp=...
                                 ^^^^^^^^
                                 Das ist die FILE_ID
```

### Schritt 1: Modus bestimmen

| Modus | Wann | Was passiert |
|-------|------|-------------|
| `download` | Standard-Modus | Download + PDF-Konvertierung zu Text |
| `split` | Journal-Volume (JEP, AER, etc.) | Download + Konvertierung + Splitting in einzelne Papers |
| `status` | Workflow pruefen | Zeigt Status des letzten GitHub Actions Runs |
| `pull` | Ergebnisse holen | `git pull` um heruntergeladene Dateien zu erhalten |

### Schritt 2: Token laden (PFLICHT!)

```bash
export GH_TOKEN=$(cat .claude/.gh_token | tr -d '[:space:]')
```

### Schritt 3: Workflow triggern

**Option A: Via api.sh (empfohlen)**

```bash
# Einfacher Download mit PDF-Konvertierung
bash scripts/api.sh drive download <FILE_ID> [output_name]

# Download + Split (fuer Journal-Volumes)
bash scripts/api.sh drive split <FILE_ID> [output_name]
```

**Option B: Via Push-Trigger (kein Token noetig)**

```bash
# 1. Trigger-Datei aktualisieren
# data/drive-fetch-trigger.yaml editieren:
#   file_id: '<FILE_ID>'
#   output_name: 'name.pdf'
#   convert_pdf: true
#   split_papers: true/false

# 2. Pushen → Workflow startet automatisch
git add data/drive-fetch-trigger.yaml
git commit -m "trigger: Drive fetch <FILE_ID>"
git push
```

### Schritt 4: Auf Ergebnis warten

```bash
# Status pruefen (ca. 2-5 Minuten)
# GitHub Actions Seite:
echo "https://github.com/FehrAdvice-Partners-AG/complementarity-context-framework/actions/workflows/fetch-google-drive.yml"
```

### Schritt 5: Ergebnis holen

```bash
git pull origin $(git branch --show-current)
ls -la data/drive-downloads/
```

### Schritt 6: Dateien verarbeiten

Nach dem Pull befinden sich die Dateien in `data/drive-downloads/`:
- `*.pdf` — Original-PDF
- `*.txt` — Extrahierter Text (pdftotext)
- `*.md` — Markdown-Version
- `split/` — Einzelne Papers (bei split-Modus)

Fuer Paper-Integration: Dateien aus `data/drive-downloads/` in `data/paper-texts/PAP-*.md` verschieben und `/integrate-paper` Workflow starten.

## Voraussetzungen

- **Google Drive Sharing:** Datei MUSS "Anyone with the link" (Viewer) sein
- **GH_TOKEN:** In `.claude/.gh_token` gespeichert (fuer Option A)
- **GitHub Actions:** Workflow `fetch-google-drive.yml` muss auf dem Branch existieren

## Fehlerbehebung

| Problem | Ursache | Loesung |
|---------|---------|---------|
| 403 bei Download | Datei nicht oeffentlich geteilt | Google Drive → Share → "Anyone with the link" |
| Workflow startet nicht | Token abgelaufen | `export GH_TOKEN=$(cat .claude/.gh_token)` |
| Leere Datei | Google Virus-Scan Seite | `gdown` sollte das handeln — Issue melden |
| Split findet keine Papers | Unbekanntes Journal-Format | Manuell splitten oder Pattern in `fetch_google_drive.py` erweitern |

## Dateien

| Datei | Zweck |
|-------|-------|
| `.github/workflows/fetch-google-drive.yml` | GitHub Actions Workflow |
| `scripts/fetch_google_drive.py` | Download + Split Script |
| `scripts/api.sh` | CLI-Trigger (Kommando `drive`) |
| `data/drive-fetch-trigger.yaml` | Push-Trigger (token-frei) |
| `data/drive-fetch-log.yaml` | Download-Log |
| `data/drive-downloads/` | Heruntergeladene Dateien |

## Architektur

```
Claude Code (Sandbox — Drive blockiert)
         |
    Option A: api.sh drive download <ID>
         |     → curl → GitHub API → workflow_dispatch
         |
    Option B: push data/drive-fetch-trigger.yaml
         |     → git push → push-trigger
         |
         v
GitHub Actions Runner (uneingeschraenkter Internet-Zugang)
         |
    1. gdown → Google Drive Download
    2. pdftotext → Text-Extraktion
    3. fetch_google_drive.py → Paper-Splitting (optional)
    4. git commit + push → Ergebnisse im Repo
         |
         v
Claude Code: git pull → Dateien in data/drive-downloads/
```

## Auto-Watch Modus (Ordner ueberwachen)

Fuer automatische Integration: Ein Google Apps Script ueberwacht einen Drive-Ordner
und triggert den Workflow automatisch bei neuen Dateien.

**Setup:** `scripts/google-apps-script/SETUP.md` (5 Minuten, einmalig)

```
Google Drive Folder        Google Apps Script        GitHub Actions
┌──────────────┐           ┌──────────────┐          ┌──────────────┐
│ Neue Datei!  │──(5min)──→│ checkForNew  │──(API)──→│ Workflow     │
│              │           │ Files()      │          │ Download     │
└──────────────┘           └──────────────┘          │ Convert      │
                                                     │ Commit       │
                                                     └──────────────┘
```

**Was passiert automatisch:**
- Datei wird auf "Anyone with the link" geteilt
- PDFs werden zu Text konvertiert
- Journal-Volumes (Name enthaelt "volume", "jep", etc.) werden gesplittet
- Ergebnisse werden ins Repo committed

**Dateien:**
- `scripts/google-apps-script/drive-watcher.gs` — Apps Script Code
- `scripts/google-apps-script/SETUP.md` — Einrichtungsanleitung
- `data/drive-watch-config.yaml` — Watch-Konfiguration

## Beispiel: JEP Volume herunterladen und splitten

```bash
# 1. Token laden
export GH_TOKEN=$(cat .claude/.gh_token | tr -d '[:space:]')

# 2. Trigger (Split-Modus fuer Journal-Volume)
bash scripts/api.sh drive split 1YlqZ8PRbis5_uyPxBuVLQQ4DQBClVzIg jep_vol40_winter2026.pdf

# 3. Warten (~3-5 Min) dann pullen
git pull

# 4. Ergebnis pruefen
ls data/drive-downloads/
ls data/drive-downloads/split/

# 5. Papers integrieren
# → /integrate-paper fuer jedes Paper
```
