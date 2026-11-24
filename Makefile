PYTHON ?= python

.DEFAULT_GOAL := help
.PHONY: help install test lint clean

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

install: ## Install runtime and test/lint dependencies
	$(PYTHON) -m pip install -r requirements-dev.txt

test: ## Run the offline test suite (saved HTML fixtures, no network, no Supabase)
	$(PYTHON) -m pytest -q

lint: ## Ruff (default rules)
	$(PYTHON) -m ruff check .

clean: ## Remove caches
	rm -rf .pytest_cache .ruff_cache
	find . -name __pycache__ -type d -not -path './.venv/*' -prune -exec rm -rf {} +
