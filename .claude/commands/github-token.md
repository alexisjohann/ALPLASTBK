# GitHub Token Management

> Master-Skill für GitHub Personal Access Token (PAT) Erstellung und Verwaltung

---

## Übersicht

GitHub Tokens ermöglichen API-Zugriff auf GitHub von Claude Code aus. Da direkte externe API-Aufrufe im Claude Code Sandbox blockiert sind (403 Forbidden), werden Tokens für GitHub Actions und gh CLI benötigt.

---

## Token-Typen

| Typ | Beschreibung | Empfohlen für |
|-----|--------------|---------------|
| **Fine-grained PAT** | Granulare Berechtigungen, Repository-spezifisch | ✅ Empfohlen |
| **Classic PAT** | Breite Berechtigungen, alle Repos | Legacy-Systeme |
| **GitHub Actions Token** | Auto-generiert bei Workflow-Ausführung | CI/CD Workflows |

---

## Token erstellen (Schritt für Schritt)

### 1. GitHub Developer Settings öffnen

```
https://github.com/settings/tokens?type=beta
```

Oder: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens

### 2. "Generate new token" klicken

### 3. Token konfigurieren

| Feld | Empfohlener Wert |
|------|------------------|
| **Token name** | `claude-code-ebf` |
| **Expiration** | 90 Tage (oder custom) |
| **Resource owner** | `FehrAdvice-Partners-AG` |
| **Repository access** | "Only select repositories" → `complementarity-context-framework` |

### 4. Berechtigungen setzen (Minimum)

| Kategorie | Berechtigung | Level |
|-----------|--------------|-------|
| **Contents** | Read and write | ✅ |
| **Metadata** | Read-only | ✅ |
| **Pull requests** | Read and write | ✅ |
| **Actions** | Read and write | Optional |
| **Workflows** | Read and write | Optional |

### 5. Token generieren und SOFORT kopieren

⚠️ **WICHTIG:** Token wird nur EINMAL angezeigt!

---

## Token verwenden

### Option A: In Claude Code Session (temporär)

```bash
export GH_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
gh auth status  # Verifizieren
```

### Option B: Als Repository Secret (für GitHub Actions)

1. Repository → Settings → Secrets and variables → Actions
2. "New repository secret"
3. Name: `GH_PAT` (nicht `GITHUB_TOKEN` - reserviert!)
4. Value: Token einfügen

### Option C: gh CLI Login

```bash
echo "ghp_xxxxxxxxxxxxxxxxxxxx" | gh auth login --with-token
gh auth status
```

---

## Architektur in Claude Code

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CLAUDE CODE SANDBOX                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  GIT OPERATIONEN (Push/Pull/Clone)                                      │
│  ├── Funktionieren via internem Proxy (127.0.0.1:51277)                │
│  └── Kein Token erforderlich ✅                                         │
│                                                                         │
│  GH CLI (Issues, PRs, API)                                              │
│  ├── Erfordert GH_TOKEN Environment Variable                           │
│  └── Oder: gh auth login --with-token                                  │
│                                                                         │
│  EXTERNE APIs (CrossRef, OpenAlex, etc.)                                │
│  ├── Direkte Aufrufe: 403 Forbidden ❌                                  │
│  └── Via GitHub Actions: Funktioniert ✅                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Token-Verwendung in GitHub Actions Workflows

### Wann welcher Token?

| Token | Verfügbar | Verwendung |
|-------|-----------|------------|
| `secrets.GITHUB_TOKEN` | Automatisch (jeder Workflow) | Standard-Operationen im selben Repo |
| `secrets.GH_PAT` | Manuell konfiguriert | Erweiterte Berechtigungen, Cross-Repo |

### Wann `GITHUB_TOKEN` reicht (Standard)

- ✅ Checkout des aktuellen Repos
- ✅ Commit & Push im selben Repo
- ✅ Lesen von öffentlichen Daten
- ✅ Erstellen von Issues/PRs im selben Repo

### Wann `GH_PAT` erforderlich

- 🔐 Triggern anderer Workflows (`workflow_dispatch`)
- 🔐 Cross-Repository Operationen
- 🔐 Organisation-Level API-Calls
- 🔐 Erhöhte Rate Limits (5000 statt 1000 req/h)

### Workflow-Beispiel mit GH_PAT

```yaml
# .github/workflows/example.yml
jobs:
  example:
    runs-on: ubuntu-latest
    steps:
      # Für erweiterte Berechtigungen: GH_PAT statt GITHUB_TOKEN
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_PAT }}

      # gh CLI verwendet automatisch den GITHUB_TOKEN
      # Für GH_PAT explizit setzen:
      - name: Use gh CLI with PAT
        env:
          GH_TOKEN: ${{ secrets.GH_PAT }}
        run: |
          gh api user
          gh workflow run other-workflow.yml
```

### Externe APIs (CrossRef, OpenAlex, etc.)

**Wichtig:** Externe APIs brauchen KEINEN GitHub Token!

```yaml
# Diese APIs funktionieren ohne Token:
- name: Call CrossRef API
  run: |
    curl "https://api.crossref.org/works/10.1234/example"
    # Funktioniert direkt - kein Token nötig
```

---

## GitHub Actions mit Token triggern

Wenn Token als Secret konfiguriert ist:

```bash
# Workflow manuell triggern
gh workflow run <workflow-name>.yml

# Mit Parametern
gh workflow run doi-lookup.yml -f doi="10.1234/example"

# Status prüfen
gh run list --workflow=<workflow-name>.yml
```

---

## Sicherheitsregeln

| Regel | Beschreibung |
|-------|--------------|
| **Nie committen** | Token NIEMALS in Code oder YAML committen |
| **Expiration** | Immer Ablaufdatum setzen (max 90 Tage) |
| **Minimal permissions** | Nur benötigte Berechtigungen |
| **Rotieren** | Bei Verdacht auf Kompromittierung sofort rotieren |
| **Repository-spezifisch** | Fine-grained PAT nur für benötigte Repos |

---

## Token-Status prüfen

```bash
# gh CLI Status
gh auth status

# Token-Berechtigungen testen
gh api user

# Rate Limit prüfen
gh api rate_limit
```

---

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| `gh: command not found` | `apt-get install gh` (Session-Start Hook sollte das machen) |
| `HTTP 401` | Token abgelaufen oder ungültig → Neuen erstellen |
| `HTTP 403` | Keine Berechtigung für diese Aktion → Token-Berechtigungen prüfen |
| `HTTP 404` | Repository nicht gefunden → Repository access prüfen |

---

## Links

- **Fine-grained Tokens:** https://github.com/settings/tokens?type=beta
- **Classic Tokens:** https://github.com/settings/tokens
- **Developer Settings:** https://github.com/settings/developers
- **Repository Secrets:** https://github.com/FehrAdvice-Partners-AG/complementarity-context-framework/settings/secrets/actions

---

*Skill Version: 1.1 | Erstellt: 2026-01-31 | Aktualisiert: 2026-01-31*

---

## Changelog

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.1 | 2026-01-31 | Token-Verwendung in Workflows dokumentiert (GITHUB_TOKEN vs GH_PAT) |
| 1.0 | 2026-01-31 | Initiale Version mit PAT-Erstellung und Architektur |
