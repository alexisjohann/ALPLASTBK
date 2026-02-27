# Claude Code Session Lifecycle — Was ist eine "Session"?

> **Dokumentation: Wann und wie werden Datenbanken, Tools und Hooks geladen?**

---

## 🎯 Definition: Was ist eine "Session"?

Eine **Session** im Claude Code Kontext ist eine **isolierte Umgebung**, in der:

1. **Ein neues Conversation mit Claude Code Web gestartet wird**
2. **Der Remote-Container von Anthropic initialisiert wird**
3. **Environment-Variablen gesetzt werden**
4. **Hooks ausgeführt werden**
5. **Tools und Dependencies installiert werden**
6. **Datenbanken geladen werden**

---

## 🏗️ Session-Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  USER öffnet Claude Code Web                                │
│  (https://claude.ai oder ähnlich)                           │
│                                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ANTHROPIC initializes Remote Container                     │
│  - Ubuntu base image                                        │
│  - /home/user/complementarity-context-framework mounted     │
│  - CLAUDE_CODE_REMOTE=true (environment variable)           │
│  - CLAUDE_PROJECT_DIR=/home/user/complementarity-...        │
│                                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: System Setup (Automatic)                          │
│  ✅ Basic OS packages (curl, git, etc.)                     │
│  ✅ Python 3 installed                                      │
│  ✅ Git configured with repository access                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: SessionStart Hook Execution                       │
│  📁 .claude/hooks/session-start.sh                          │
│                                                             │
│  Step 1: Install LaTeX (texlive)                            │
│    ├─ pdflatex                                              │
│    ├─ latexmk                                               │
│    └─ All fonts & science packages                          │
│                                                             │
│  Step 2: Install Build Tools                                │
│    ├─ latexmk (automated LaTeX builds)                      │
│    ├─ pandoc (format conversion)                            │
│    └─ gh (GitHub CLI for PRs)                               │
│                                                             │
│  Step 3: Install Python Dependencies                        │
│    └─ From scripts/llm_monte_carlo/requirements.txt         │
│                                                             │
│  Step 4: Initialize & Load Databases ⭐ NEW!                │
│    └─ Runs: python3 scripts/init-databases.py               │
│       ├─ Load Paper-Sources (1,784 papers)                  │
│       ├─ Load Case Registry (100+ cases)                    │
│       ├─ Load Intervention Registry (50+ projects)          │
│       ├─ Load Model Registry (38+ models)                   │
│       ├─ Load Stakeholder Models (2+ companies)             │
│       └─ Display status + quick tips                        │
│                                                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: Session Ready                                     │
│  ✅ All tools available (LaTeX, pandoc, gh, Python)         │
│  ✅ All 5 databases loaded                                  │
│  ✅ Skills/Commands available (/.../design-model, /case, etc)
│  ✅ Welcome message shown to user                           │
│                                                             │
│  User can now:                                              │
│    • /design-model → Create behavioral models               │
│    • /case → Search case registry                           │
│    • /new-customer → Create customer model                  │
│    • /intervention-manage → Track projects                  │
│    • /apply-models → Run simulations                        │
│    • git operations → Commit/push changes                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Session Lifecycle Details

### **Session Trigger**
A session is created when:

```
✅ User opens Claude Code Web
✅ New conversation thread started
✅ `.claude/` directory exists in repo root
✅ CLAUDE_CODE_REMOTE=true environment variable set
```

### **Session Duration**
A session persists until:

```
⏸️  User closes the conversation
⏸️  Session timeout (typically 60-90 minutes of inactivity)
⏸️  User explicitly ends session
⏸️  Container is destroyed (automatic cleanup)
```

### **Environment at Session Start**

| Variable | Value | Purpose |
|----------|-------|---------|
| `CLAUDE_CODE_REMOTE` | `true` | Indicates remote/web environment |
| `CLAUDE_PROJECT_DIR` | `/home/user/complementarity-context-framework` | Project root for hooks |
| `HOME` | `/home/user` | Home directory |
| `PATH` | Includes `/usr/local/bin`, `/usr/bin` | Executable paths |
| `PYTHONPATH` | Auto-set | Python module discovery |

---

## 🔄 When Does session-start.sh Execute?

```bash
# File: .claude/hooks/session-start.sh
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0  # ← Only runs if CLAUDE_CODE_REMOTE=true
fi
```

**Executes when:**
- ✅ User opens Claude Code Web (Remote/Cloud environment)
- ✅ Container initializes
- ✅ CLAUDE_CODE_REMOTE environment variable is set to "true"

**Does NOT execute when:**
- ❌ Running locally in terminal (CLAUDE_CODE_REMOTE not set)
- ❌ Running in non-remote environment
- ❌ Using Claude Code CLI locally

---

## 📊 Databases Loaded at Session Start

When `python3 scripts/init-databases.py` runs, it:

### **1. Loads All 5 Databases**

| Database | File | Entries | Load Time |
|----------|------|---------|-----------|
| **Paper-Sources** | `data/paper-sources.yaml` | 1,784 papers | ~2-3s |
| **Case Registry** | `data/case-registry.yaml` | 100+ cases | ~0.5-1s |
| **Intervention Registry** | `data/intervention-registry.yaml` | 50+ projects | ~0.5s |
| **Model Registry** | `models/models.registry.yaml` | 38+ models | ~0.5s |
| **Stakeholder Models** | `data/stakeholder-models/stakeholder_models_registry.yaml` | 2+ companies | ~0.2s |

**Total load time:** ~4-5 seconds

### **2. Validates All Databases**

For each database:
```
✓ Check file exists
✓ Parse YAML/JSON
✓ Count entries
✓ Report status (✅ or ⚠️)
```

### **3. Displays Status to User**

```
==================================================
               EBF DATABASE STATUS
==================================================

📚 Paper-Sources                ✅               1,784 entries
📋 Case Registry                ✅                 852 entries
🚀 Intervention Registry        ✅                   4 entries
🧮 Model Registry               ✅                  38 entries
👥 Stakeholder Models           ✅                   2 entries

Total Entries: 2,680

💡 QUICK TIPS:
  /case --domain health              Find similar cases
  /design-model --mode schnell       Design model in 10 min
  /new-customer "Company" 1500      Create customer model
  /intervention-manage new           Track a project
  /sensitivity-analysis Company      What-if analysis

✅ All databases loaded successfully!
```

---

## 🔗 What Happens After Session-Start?

### **Skills/Commands Become Available**

Once session-start completes, users can use slash commands defined in `.claude/commands/`:

```
/design-model         → Nutzt MODEL-REGISTRY + PAPER-SOURCES
/case                 → Durchsucht CASE-REGISTRY
/case-manage          → Verwaltet CASE-REGISTRY
/new-customer         → Erstellt in STAKEHOLDER-MODELS
/apply-models         → Nutzt MODEL-REGISTRY
/intervention         → Durchsucht INTERVENTION-REGISTRY
/intervention-manage  → Verwaltet INTERVENTION-REGISTRY
/generate-paper       → Nutzt PAPER-SOURCES + Appendices
/compile              → Nutzt LaTeX (installiert in session-start)
/convert              → Nutzt pandoc (installiert in session-start)
/check-compliance     → Validiert Kapitel/Appendices
/r-score              → Nutzt scripts/llm_monte_carlo
/sensitivity-analysis → Nutzt STAKEHOLDER-MODELS + MODEL-REGISTRY
/board-presentation   → Nutzt STAKEHOLDER-MODELS
```

### **Pre-Commit Hook Becomes Active**

```
📁 .claude/hooks/pre-commit.sh
├─ Triggers before every git commit
├─ Validates .tex compliance (chapters & appendices)
├─ Blocks commits if score < 85%
└─ Can be overridden with --no-verify (not recommended)
```

---

## 💾 What Gets Cached/Persisted?

### **Persists Across Requests (within Session)**

```
✅ Installed tools (LaTeX, pandoc, gh)
✅ Loaded databases (in-memory cache)
✅ Python packages
✅ File system changes
✅ Git working tree
```

### **Does NOT Persist Across Sessions**

```
❌ Environment variables (except those set by Anthropic)
❌ Temporary files created during session
❌ Any /tmp/ contents
❌ Shell history
```

**Important:** Each NEW session starts fresh with:
- Fresh container
- Fresh installation of tools
- Fresh database loads

---

## 📈 Session Timeline Example

```
T+0:00    User opens Claude Code Web
T+0:01    Container initializes (Anthropic infrastructure)
T+0:02    PHASE 1: OS setup (automatic)
T+0:05    PHASE 2: Hook execution starts
T+0:08    → LaTeX installed (3 seconds)
T+0:10    → Build tools installed (2 seconds)
T+0:12    → Python deps installed (1-2 seconds)
T+0:14    → Databases loaded (4-5 seconds) ⭐
T+0:19    → Status displayed to user
T+0:20    PHASE 3: Session ready
          User can now use /commands

T+...     User works (hours)
T+120:00  Session timeout (after ~2 hours inactivity)
T+120:01  Container destroyed (cleanup)
          ↓
          Next session = New T+0:00
```

---

## 🔍 How to Debug Session Issues

### **If databases don't load:**

```bash
# Test the init script manually
cd /home/user/complementarity-context-framework
python3 scripts/init-databases.py --verbose
```

### **If tools aren't available:**

```bash
# Test LaTeX
pdflatex --version

# Test pandoc
pandoc --version

# Test gh
gh --version
```

### **If session-start hook doesn't run:**

```bash
# Check environment variable
echo $CLAUDE_CODE_REMOTE   # Should be "true" if running remotely

# Check hook file
bash -x .claude/hooks/session-start.sh 2>&1
```

---

## 🎓 Key Insights

### **1. Session = Fresh Start**
Every session starts with:
- Clean container
- Fresh installations
- Full database reloads

### **2. Databases Always Available**
Because `init-databases.py` runs automatically, users:
- Can immediately use `/case`, `/design-model`, etc.
- See full data overview at session start
- Know what's available without asking

### **3. One Session = One Thread**
Multiple conversations = Multiple sessions = Multiple containers

### **4. No Cross-Session State**
Session A's data is isolated from Session B:
```
Session A: User edits /data/case-registry.yaml
Session B: Still sees the old version
           (must git pull to see changes)
```

---

## 📚 Related Files

| File | Purpose |
|------|---------|
| `.claude/hooks/session-start.sh` | Main hook that defines session initialization |
| `scripts/init-databases.py` | Loads & validates all 5 databases |
| `.claude/hooks/pre-commit.sh` | Git hook (runs during session, before commits) |
| `data/paper-sources.schema.yaml` | Schema for Paper-Sources |
| `data/case-registry.schema.yaml` | Schema for Case Registry |
| `data/intervention-registry.schema.yaml` | Schema for Intervention Registry |
| `models/models.schema.yaml` | Schema for Model Registry |
| `data/stakeholder-models/stakeholder-models.schema.yaml` | Schema for Stakeholder Models |
| `.claude/commands/*/` | Available slash commands (loaded from here) |

---

**Version:** 1.0 | **Created:** January 18, 2026 | **Updated:** After Database Schema Standardization
