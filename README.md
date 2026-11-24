# Tic-Tac-Toe with Minimax AI

Tic-tac-toe game featuring an unbeatable Minimax AI opponent.

## Overview
Two implementations of tic-tac-toe with a Minimax algorithm AI:
1. **Flask web app** — playable in the browser (`app.py`, `templates/`, `static/`)
2. **Standalone Python script** — `Tic-Tac-Toe with Minimax Algorithm.py`

## How to run
Web app:
```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```
Standalone:
```bash
python "Tic-Tac-Toe with Minimax Algorithm.py"
```

## Running tests
The `tests/` suite covers the game engine (board setup, win/draw detection,
move validity) and the alpha-beta minimax AI (immediate wins, blocking, and
verifying optimal play always ends in a draw and the AI never loses to random play):
```bash
pip install -r requirements.txt
pytest
```

## Tests and CI
CI (`.github/workflows/ci.yml`) byte-compiles the sources and runs the
test suite on every push and pull request to `main` (Python 3.11).

## Make shortcuts
The `Makefile` wraps the common commands (`PY` and `VENV` are overridable):
```bash
make setup   # create .venv and install dependencies
make test    # run the pytest suite (19 tests)
make run     # start the Flask web app at http://127.0.0.1:5000
make play    # play the standalone terminal game against the AI
make clean   # remove .venv and caches
```
