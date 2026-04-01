.PHONY: html clean setup

html:
	@python3 scripts/build-html.py

clean:
	@rm -f claude-code-docs.html
	@echo "✓ Pulito"

setup:
	@which pandoc > /dev/null || (echo "Installa pandoc con: brew install pandoc" && exit 1)
	@git config core.hooksPath .githooks && echo "✓ Git hooks configurati (.githooks/)"
