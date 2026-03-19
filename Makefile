.PHONY: docs-serve docs-build

docs-serve:
	mkdocs serve --dev-addr 0.0.0.0:8000

docs-build:
	mkdocs build --clean --strict
