# Google Drive → GitHub Actions Bridge: Setup-Anleitung

## Was macht das?

Ein Google Apps Script ueberwacht einen Google Drive Ordner alle 5 Minuten.
Wenn eine neue Datei erkannt wird:
1. Datei wird automatisch auf "Anyone with the link" geteilt
2. GitHub Actions Workflow wird getriggert
3. Workflow laedt Datei herunter, konvertiert PDF → Text, committed ins Repo
4. PDFs mit "volume/journal" im Namen werden automatisch in einzelne Papers gesplittet

## Automatischer Sync: Repo → Apps Script (via clasp)

Aenderungen an `.gs`-Dateien werden automatisch zu Google Apps Script gepushed.

```
scripts/google-apps-script/*.gs  →  GitHub Action  →  clasp push  →  script.google.com
data/researcher-scraper-config.json  →  (wird von Apps Script zur Laufzeit geladen)
```

### Einmaliges Setup (5 Minuten)

```bash
bash scripts/setup_clasp.sh
```

Das Script:
1. Installiert `clasp` (Googles CLI fuer Apps Script)
2. Oeffnet Browser fuer Google Login
3. Fragt nach der Script ID (aus script.google.com → Projekteinstellungen)
4. Macht einen Test-Push
5. Zeigt an welche GitHub Secrets zu setzen sind

### GitHub Secrets (fuer automatischen Sync)

| Secret | Wert | Woher |
|--------|------|-------|
| `CLASP_TOKEN` | Inhalt von `~/.clasprc.json` | Nach `clasp login` |
| `APPS_SCRIPT_ID` | Script ID | script.google.com → Projekteinstellungen |

### Was wird wie synchronisiert?

| Aenderung | Sync-Methode | Aktion noetig? |
|-----------|-------------|----------------|
| Neuer Forscher | **Keine** — JSON wird zur Laufzeit geladen | Nur JSON editieren + commit |
| .gs Code-Aenderung | GitHub Action → clasp push | Automatisch bei Push auf main |
| Drive Watcher Config | GitHub Action → clasp push | Automatisch bei Push auf main |

```
Google Drive Folder     GitHub Repository
┌──────────────┐        ┌──────────────────┐
│ Neue Datei!  │───────→│ Actions Workflow  │
│ (PDF, etc.)  │  API   │ ↓                │
└──────────────┘        │ Download (gdown)  │
                        │ ↓                │
                        │ PDF → Text       │
                        │ ↓                │
                        │ git commit+push  │
                        └──────────────────┘
```

## Voraussetzungen

- Google Account mit Zugriff auf den Drive-Ordner
- GitHub Fine-Grained PAT mit `actions: write` Berechtigung
- Der Drive-Ordner muss existieren

## Setup (5 Minuten)

### Schritt 1: Google Apps Script erstellen

1. Oeffne [script.google.com](https://script.google.com)
2. Klicke **Neues Projekt**
3. Benenne es: `EBF Drive Watcher`
4. Loesche den Beispielcode
5. Kopiere den gesamten Inhalt von `drive-watcher.gs` hinein
6. Speichern (Ctrl+S)

### Schritt 2: Script Properties setzen

1. Im Apps Script Editor: **Zahnrad-Icon** (links) → **Projekteinstellungen**
2. Scrolle nach unten zu **Skripteigenschaften**
3. Fuege diese 4 Properties hinzu:

| Property | Wert | Beschreibung |
|----------|------|--------------|
| `GITHUB_TOKEN` | `github_pat_...` | Fine-Grained PAT mit `actions: write` |
| `GITHUB_REPO` | `FehrAdvice-Partners-AG/complementarity-context-framework` | Repository |
| `GITHUB_BRANCH` | `main` | Ziel-Branch |
| `DRIVE_FOLDER_ID` | `1abc...xyz` | Google Drive Folder-ID |

**Folder-ID finden:**
- Oeffne den Google Drive Ordner im Browser
- Die URL sieht so aus: `https://drive.google.com/drive/folders/<FOLDER_ID>`
- Kopiere die `<FOLDER_ID>`

**GitHub Token erstellen:**
- Gehe zu [github.com/settings/tokens](https://github.com/settings/tokens?type=beta)
- **Fine-grained token** → Generate
- Repository: `complementarity-context-framework`
- Permissions: `Actions: Read & Write`
- Kopiere den Token

### Schritt 3: Trigger installieren

1. Im Apps Script Editor: Waehle `setupTrigger` in der Funktionsauswahl (oben)
2. Klicke **Ausfuehren** (Play-Button)
3. Bei der ersten Ausfuehrung: Google fragt nach Berechtigungen → **Erlauben**
4. Im Log (unten) sollte stehen:
   ```
   Trigger installed: checkForNewFiles every 5 minutes
   Config OK. Watching folder: <FOLDER_ID>
   ```

### Schritt 4: Verbindung testen

1. Waehle `testGitHubConnection` → **Ausfuehren**
2. Im Log sollte stehen:
   ```
   Connection OK!
     Repo: FehrAdvice-Partners-AG/complementarity-context-framework
     Private: true
   ```

### Schritt 5: Erste Datei testen

1. Lege eine Test-Datei in den ueberwachten Drive-Ordner
2. Waehle `checkForNewFiles` → **Ausfuehren** (oder warte 5 Minuten)
3. Im Log:
   ```
   New file detected: test.pdf (1abc...xyz)
     Set sharing: Anyone with link (Viewer)
     Triggered GitHub Actions for: test.pdf
   ```
4. Pruefe auf GitHub: Actions → `Fetch Google Drive File` → Run laeuft

## Forscher hinzufuegen (OHNE Google Apps Script!)

Neue Forscher werden ueber eine JSON-Datei im Git-Repo konfiguriert.
Das Apps Script laedt die Config automatisch bei jedem Lauf.

### Datei: `data/researcher-scraper-config.json`

```json
{
  "researchers": [
    {
      "name": "Ernst Fehr",
      "url": "https://www.econ.uzh.ch/en/people/faculty/fehr/publications.html",
      "folder": "Fehr_Ernst",
      "registry_id": "RES-FEHR-E"
    },
    {
      "name": "Neuer Forscher",
      "url": "https://example.com/publications",
      "folder": "Nachname_Vorname",
      "registry_id": "RES-NACHNAME-X"
    }
  ]
}
```

### Workflow: Neuen Forscher hinzufuegen

1. `data/researcher-scraper-config.json` oeffnen
2. Neuen Eintrag im `researchers` Array hinzufuegen:
   - `name`: Anzeigename
   - `url`: Publikationsseite (muss PDF-Links enthalten)
   - `folder`: Drive-Ordnername (Format: `Nachname_Vorname`)
   - `registry_id`: Optional, Verweis auf researcher-registry.yaml
3. Commit + Push auf `main`
4. Fertig — naechster Scraper-Lauf laedt die Config automatisch

**Kein Zugriff auf Google Apps Script noetig!**

### Fallback

Falls GitHub nicht erreichbar ist (z.B. Rate Limit), nutzt das Script
automatisch die lokalen `Researcher_*.gs` Dateien als Fallback.

### Config pruefen

Im Apps Script Editor: `showResearcherConfig` ausfuehren.
Zeigt an welche Forscher aktuell konfiguriert sind und woher die Config kommt.

---

## Verfuegbare Funktionen

| Funktion | Zweck | Ausfuehren |
|----------|-------|-----------|
| `setupTrigger` | Trigger installieren (einmalig) | Manuell |
| `checkForNewFiles` | Neue Dateien pruefen | Automatisch (alle 5 Min) |
| `testGitHubConnection` | GitHub-Verbindung testen | Manuell |
| `listWatchedFolder` | Alle Dateien im Ordner anzeigen | Manuell |
| `showProcessedHistory` | Bereits verarbeitete Dateien | Manuell |
| `resetProcessedHistory` | History zuruecksetzen | Manuell |
| `processFileManually` | Einzelne Datei erneut verarbeiten | Manuell (mit File-ID) |
| `scrapeAllResearchers` | Alle Forscher-Webseiten scrapen | Automatisch (Mo 06:00) |
| `showResearcherConfig` | Aktuelle Forscher-Config anzeigen | Manuell |
| `setupResearcherTrigger` | Woechentlichen Scraper-Trigger setzen | Manuell (einmalig) |

## Automatische Erkennung

Das Script erkennt automatisch:

| Dateiname enthaelt | Aktion |
|--------------------|--------|
| `.pdf` | PDF → Text Konvertierung |
| `vol`, `volume`, `journal`, `jep`, `aer`, `qje` | + Splitting in einzelne Papers |
| Alles andere | Nur Download |

## Fehlerbehebung

| Problem | Loesung |
|---------|---------|
| "Missing config" | Script Properties pruefen (Schritt 2) |
| "GitHub API error 401" | Token abgelaufen → neuen erstellen |
| "GitHub API error 404" | Repo-Name oder Workflow-Name pruefen |
| "GitHub API error 422" | Branch existiert nicht |
| Keine Berechtigungen | Bei erstem Run: Google-Berechtigungen akzeptieren |
| Datei nicht erkannt | `checkForNewFiles` manuell ausfuehren zum Debuggen |
| Duplikate | `showProcessedHistory` pruefen, ggf. `resetProcessedHistory` |

## Kosten

- **Google Apps Script:** Kostenlos (Google Workspace Quota: 90 Min/Tag Script-Laufzeit)
- **GitHub Actions:** Kostenlos fuer private Repos (2000 Min/Monat)
- Jeder Check dauert < 2 Sekunden
- Jeder Download-Workflow dauert 2-5 Minuten

## Sicherheit

- Der GitHub Token wird NICHT im Code gespeichert, sondern in Script Properties
- Script Properties sind verschluesselt und nur fuer den Script-Owner sichtbar
- Der Token braucht nur `actions: write` — kein Zugriff auf Code oder Secrets
- Drive-Dateien werden nur auf "Viewer" geteilt, nicht "Editor"
