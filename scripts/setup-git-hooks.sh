#!/bin/bash
# Setup Git Hooks für alle Entwickler
# Verwendung: ./scripts/setup-git-hooks.sh

echo "🔧 Installiere Git Hooks..."

# Pre-Push Hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# Pre-Push Hook: Warnt wenn Branch zu weit hinter main ist

BEHIND_THRESHOLD=10

CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "main" ]; then
    exit 0
fi

git fetch origin main --quiet 2>/dev/null
BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")

if [ "$BEHIND" -gt "$BEHIND_THRESHOLD" ]; then
    echo ""
    echo "⚠️  WARNUNG: Branch ist $BEHIND Commits hinter main!"
    echo ""
    echo "   Optionen:"
    echo "   [s] Synchronisieren (automatisch git merge origin/main)"
    echo "   [p] Trotzdem pushen (nicht empfohlen)"
    echo "   [a] Abbrechen"
    echo ""
    read -p "   Wahl [s/p/a]: " -n 1 -r
    echo

    case $REPLY in
        [Ss])
            echo ""
            echo "   🔄 Synchronisiere mit main..."
            git merge origin/main --no-edit
            if [ $? -eq 0 ]; then
                echo "   ✅ Synchronisierung erfolgreich!"
            else
                echo "   ❌ Merge-Konflikt! Bitte manuell lösen."
                exit 1
            fi
            ;;
        [Pp])
            ;;
        *)
            exit 1
            ;;
    esac
fi

exit 0
EOF

chmod +x .git/hooks/pre-push

# Post-Checkout Hook (bei Branch-Wechsel)
cat > .git/hooks/post-checkout << 'EOF'
#!/bin/bash
# Post-Checkout: Zeigt Status nach Branch-Wechsel

# Nur bei Branch-Wechsel (nicht bei File-Checkout)
if [ "$3" != "1" ]; then
    exit 0
fi

BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "?")

if [ "$BEHIND" != "?" ] && [ "$BEHIND" -gt 5 ]; then
    echo ""
    echo "📊 Branch-Status: $BEHIND Commits hinter main"
    echo "   Tipp: git fetch origin main && git merge origin/main"
fi
EOF

chmod +x .git/hooks/post-checkout

echo "✅ Git Hooks installiert!"
echo ""
echo "Installierte Hooks:"
echo "  - pre-push:      Warnt wenn >10 Commits hinter main"
echo "  - post-checkout: Zeigt Status nach Branch-Wechsel"
