# Tic-Tac-Toe with Minimax AI — shortcuts
# Usage: make setup && make test && make run
PY ?= python3
VENV ?= .venv

.PHONY: help setup test run play clean

help:
	@echo "Targets:"
	@echo "  setup  - create a virtualenv and install dependencies"
	@echo "  test   - run the pytest suite (19 tests)"
	@echo "  run    - start the Flask web app at http://127.0.0.1:5000"
	@echo "  play   - play the standalone terminal game against the AI"
	@echo "  clean  - remove the virtualenv and caches"

setup:
	$(PY) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

test:
	$(PY) -m pytest -q

run:
	$(PY) app.py

play:
	$(PY) "Tic-Tac-Toe with Minimax Algorithm.py"

clean:
	rm -rf $(VENV) __pycache__ tests/__pycache__ .pytest_cache
