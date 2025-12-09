.PHONY: install
install:
	pip install -e .[dev]

.PHONY: test
test:
	pytest -q

.PHONY: lint
lint:
	ruff check src
	black --check src
