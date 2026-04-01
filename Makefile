.PHONY: html clean setup

html:
	@python3 scripts/build-html.py

clean:
	@rm -f claude-code-docs.html
	@echo "✓ Pulito"

setup:
	@pip3 install --break-system-packages markdown -q && echo "✓ Dipendenza 'markdown' installata"
	@git config core.hooksPath .githooks && echo "✓ Git hooks configurati (.githooks/)"
