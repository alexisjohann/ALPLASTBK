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
#
# Version: 1.1
# Date: 2026-01-29
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
# Workflow-Erinnerung ausgeben (nur bei Match)
# -----------------------------------------------------------------------------

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
# Workflow-Erinnerung ausgeben (nur bei Match)
# -----------------------------------------------------------------------------

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
