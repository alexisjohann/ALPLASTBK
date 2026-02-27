#!/bin/bash
# =============================================================================
# EBF User Prompt Submit Hook
# =============================================================================
# Wird VOR jeder Claude-Antwort ausgeführt
# Prüft ob eine inhaltliche Frage gestellt wurde und erinnert an den Workflow
#
# FUNKTION:
# 1. Klassifiziert die User-Nachricht
# 2. Bei inhaltlicher Frage: Erinnert an /find-model Workflow
# 3. Bei Projekt-Anfrage: Erinnert an /project-setup Workflow
# 4. Gibt Kontext-Hinweise für die 5-Datenbank-Architektur
# 5. NEU: IMMUNE GATEWAY — Automatische Layer-1-Berechnung bei
#    Parameter-Keywords (loest das "Wirt entscheidet"-Paradoxon)
#
# Version: 2.0
# Date: 2026-02-16
# =============================================================================

set -euo pipefail

# Nur wenn USER_PROMPT verfügbar ist
if [ -z "${USER_PROMPT:-}" ]; then
  exit 0
fi

# -----------------------------------------------------------------------------
# Klassifikation der User-Nachricht
# -----------------------------------------------------------------------------

# Lowercase für Pattern-Matching
PROMPT_LOWER=$(echo "$USER_PROMPT" | tr '[:upper:]' '[:lower:]')

# SKIP-Patterns: Technische Befehle, Grüße, kurze Antworten
SKIP_PATTERNS=(
  "^hi$"
  "^hallo$"
  "^hey$"
  "^danke"
  "^ok$"
  "^ja$"
  "^nein$"
  "^git "
  "^/compile"
  "^/convert"
  "^/check"
  "^/new-"
  "^/design-"
  "^/find-model"
  "^/case"
  "^/intervention"
  "^commit"
  "^push"
  "^pull"
  "^merge"
  "^erstelle"
  "^create"
  "^fix"
  "^update"
  "^änder"
  "^change"
  "^delete"
  "^remove"
  "^add "
  "bitte den"
  "bitte die"
  "bitte das"
  "implementier"
  "^k[0-9]"
  "^m[0-9]"
  "^p[0-9]"
  "^a[0-9]"
  "^i[0-9]"
  "^r[0-9]"
  "^s[0-9]"
  "^c[0-9]"
  "^f[0-9]"
  "^alle$"
)

# Prüfe ob SKIP-Pattern matched
for pattern in "${SKIP_PATTERNS[@]}"; do
  if echo "$PROMPT_LOWER" | grep -qE "$pattern"; then
    exit 0  # Kein Workflow-Trigger
  fi
done

# TRIGGER-Patterns: Inhaltliche Fragen
TRIGGER_PATTERNS=(
  "\\?"                          # Fragezeichen
  "^ist "                        # "Ist X...?"
  "^was "                        # "Was ist...?"
  "^wie "                        # "Wie kann...?"
  "^warum "                      # "Warum...?"
  "^welche"                      # "Welche...?"
  "^wann "                       # "Wann...?"
  "^wo "                         # "Wo...?"
  "^wer "                        # "Wer...?"
  "^kann "                       # "Kann man...?"
  "^soll "                       # "Soll ich...?"
  "^würde"                       # "Würde es...?"
  "^könnte"                      # "Könnte...?"
  "näher zu"                     # Distanz-Fragen
  "unterschied"                  # Vergleichsfragen
  "vergleich"                    # Vergleichsfragen
  "analyse"                      # Analyse-Anfragen
  "erklär"                       # Erklärungen
  "möglich"                      # Möglichkeitsfragen
  "stimulier"                    # Verhaltensänderung
  "motivier"                     # Verhaltensänderung
  "bring.*dazu"                  # Verhaltensänderung
  "nudge"                        # Verhaltensänderung
  "intervention"                 # Verhaltensänderung
  "maßnahme"                     # Verhaltensänderung
  "strategie"                    # Strategiefragen
  "empfehl"                      # Empfehlungen
)

# PROJECT-Patterns: Projekt-Erstellung erkennen
PROJECT_PATTERNS=(
  "projekt.*eröffnen"            # "Projekt eröffnen"
  "projekt.*anlegen"             # "Projekt anlegen"
  "projekt.*erstellen"           # "Projekt erstellen"
  "projekt.*starten"             # "Projekt starten"
  "neues projekt"                # "neues Projekt"
  "kundenprojekt"                # "Kundenprojekt"
  "beratungsprojekt"             # "Beratungsprojekt"
  "projekt.*aufsetzen"           # "Projekt aufsetzen"
  "wir.*möchten.*projekt"        # "wir möchten ein Projekt"
  "möchten.*eröffnen"            # "möchten ... eröffnen"
  "haben.*ein.*projekt"          # "haben ein Projekt"
  "gibt.*ein.*projekt"           # "gibt ein Projekt"
  "begonnen.*projekt"            # "begonnenes Projekt"
  "laufendes.*projekt"           # "laufendes Projekt"
)

MATCHED=false
for pattern in "${TRIGGER_PATTERNS[@]}"; do
  if echo "$PROMPT_LOWER" | grep -qiE "$pattern"; then
    MATCHED=true
    break
  fi
done

# Projekt-Trigger separat prüfen
PROJECT_MATCHED=false
for pattern in "${PROJECT_PATTERNS[@]}"; do
  if echo "$PROMPT_LOWER" | grep -qiE "$pattern"; then
    PROJECT_MATCHED=true
    break
  fi
done

# -----------------------------------------------------------------------------
# Session Auto-Save (alle 30 Minuten)
# -----------------------------------------------------------------------------
CURRENT_SESSION_FILE="$CLAUDE_PROJECT_DIR/.claude/current-session.yaml"

if [ -f "$CURRENT_SESSION_FILE" ]; then
  # Prüfe ob Python verfügbar
  if command -v python3 &> /dev/null; then
    # Auto-save prüfen und ggf. durchführen
    # --interval 30: Alle 30 Minuten speichern
    # Auto-End um 22:00 Uhr ist im Script integriert
    python3 "$CLAUDE_PROJECT_DIR/scripts/session_manager.py" autosave --interval 30 2>&1 || true
  fi
fi

# -----------------------------------------------------------------------------
# IMMUNE GATEWAY — Autonomous Layer 1 Pre-Computation
# -----------------------------------------------------------------------------
# Solves: "Der Wirt entscheidet, ob der Virus leben darf" (KB-VIR-001)
# The LLM no longer decides whether to call Layer 1.
# Layer 1 runs AUTOMATICALLY when parameter keywords are detected.
# Output is injected into Claude's context BEFORE response generation.
# -----------------------------------------------------------------------------
IMMUNE_GATEWAY="$CLAUDE_PROJECT_DIR/scripts/immune_gateway.py"

if [ -f "$IMMUNE_GATEWAY" ] && command -v python3 &> /dev/null; then
  # Run with timeout (8 seconds max) — fail silently if any error
  GATEWAY_OUTPUT=$(timeout 8s python3 "$IMMUNE_GATEWAY" "$USER_PROMPT" 2>/dev/null) || true
  if [ -n "$GATEWAY_OUTPUT" ]; then
    echo "$GATEWAY_OUTPUT"
  fi
fi

# -----------------------------------------------------------------------------
# PAPER INBOX CHECK — Auto-detect uploaded papers
# -----------------------------------------------------------------------------
# Checks data/paper-texts/inbox/ for new files (excluding README.md, .gitkeep)
# If found, notifies Claude to process them via /integrate-paper workflow
# -----------------------------------------------------------------------------
INBOX_DIR="$CLAUDE_PROJECT_DIR/data/paper-texts/inbox"

if [ -d "$INBOX_DIR" ]; then
  INBOX_FILES=$(find "$INBOX_DIR" -type f ! -name "README.md" ! -name ".gitkeep" 2>/dev/null | head -20)
  if [ -n "$INBOX_FILES" ]; then
    INBOX_COUNT=$(echo "$INBOX_FILES" | wc -l)
    cat << INBOXEOF

┌─────────────────────────────────────────────────────────────────────────────┐
│  📬 PAPER INBOX: ${INBOX_COUNT} neue Datei(en) erkannt                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Dateien in data/paper-texts/inbox/:                                       │
INBOXEOF
    echo "$INBOX_FILES" | while read -r f; do
      BASENAME=$(basename "$f")
      echo "│    → $BASENAME"
    done
    cat << 'INBOXEOF'
│                                                                             │
│  AKTION: Automatisch verarbeiten!                                          │
│  1. Paper identifizieren (Autor, Jahr, DOI)                                │
│  2. BibTeX-Key generieren                                                  │
│  3. Duplikat-Check gegen bcm_master.bib                                    │
│  4. Als PAP-{key}.md in data/paper-texts/ speichern                        │
│  5. YAML + BibTeX erstellen/upgraden                                       │
│  6. Aus inbox/ entfernen                                                   │
│                                                                             │
│  ⚠️  PFLICHT: Vor der eigentlichen User-Anfrage verarbeiten!                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

INBOXEOF
  fi
fi

# -----------------------------------------------------------------------------
# PROJECT-SETUP Trigger (hat Priorität vor EBF Workflow)
# -----------------------------------------------------------------------------
if [ "$PROJECT_MATCHED" = true ]; then
  cat << 'EOF'

┌─────────────────────────────────────────────────────────────────────────────┐
│  📋 PROJEKT-TRIGGER ERKANNT                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  → /project-setup Workflow verwenden!                                       │
│                                                                             │
│  PHASE 1: Lead prüfen/erstellen     → LEAD-XXX                             │
│  PHASE 2: CVA prüfen (PFLICHT!)     → Kundenprofil                         │
│  PHASE 3: Scope definieren          → Ziel, In/Out-Scope, Deliverables     │
│  PHASE 4: Dateien erstellen         → PRJ-XXX + Git commit                 │
│                                                                             │
│  QUICK START:                                                               │
│    /project-setup                        # Interaktiv                       │
│    /project-setup "Kunde" "Projektname"  # Schnellstart                     │
│    /project-setup --from-lead LEAD-047   # Von Lead starten                 │
│                                                                             │
│  OHNE /project-setup FEHLT:                                                 │
│  ✗ Strukturierte Scope-Definition                                          │
│  ✗ CVA-Prüfung (Ψ-Parameter!)                                              │
│  ✗ Einheitliche Superkey-Vergabe                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

EOF
elif [ "$MATCHED" = true ]; then
  cat << 'EOF'

┌─────────────────────────────────────────────────────────────────────────────┐
│  🔴 EBF WORKFLOW TRIGGER                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INHALTLICHE FRAGE ERKANNT → /find-model Workflow anwenden!                │
│                                                                             │
│  SCHRITT 0: Session Init (Domain, Scope, Lieferobjekte)                    │
│  SCHRITT 1: Kontext (Ψ-Dimensionen + 10C)                                  │
│  SCHRITT 2: Modell (Registry-Lookup oder 10C-Build)                        │
│  SCHRITT 3: Parameter (LLMMC + Bayesian)                                   │
│  SCHRITT 4: Antwort (Ergebnis + Sensitivität)                              │
│  SCHRITT 5: Intervention (wenn Verhaltensziel)                             │
│  SCHRITT 6: Abschlussbericht                                               │
│  SCHRITT 7: SPEICHERN (automatisch in alle 5 Datenbanken!)                 │
│                                                                             │
│  DATENBANKEN (Schritt 7 PFLICHT):                                          │
│  → data/model-building-session.yaml                                        │
│  → data/model-registry.yaml                                                │
│  → data/intervention-registry.yaml                                         │
│  → data/output-registry.yaml + outputs/sessions/...                        │
│  → data/parameter-registry.yaml                                            │
│                                                                             │
│  MODUS: User fragen → schnell (10min) / standard (45min) / tief (2h+)     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

EOF
fi
