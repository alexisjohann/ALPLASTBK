.PHONY: zip clean

zip: ## Skill-ZIP für Claude.ai Admin-Upload bauen
	@bash build-skill.sh

clean: ## dist/ Ordner löschen
	@rm -rf dist/
	@echo "✅ dist/ gelöscht"

help: ## Diese Hilfe anzeigen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-10s %s\n", $$1, $$2}'
