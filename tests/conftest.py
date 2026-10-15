"""Shared fixture: load the standalone minimax module.

The module file name contains spaces, so it cannot be imported with a
plain ``import`` statement; importlib loads it by path instead.
"""
import importlib.util
import pathlib

import pytest

MODULE_PATH = (
    pathlib.Path(__file__).resolve().parent.parent
    / "Tic-Tac-Toe with Minimax Algorithm.py"
)


@pytest.fixture(scope="session")
def game():
    spec = importlib.util.spec_from_file_location("ttt_minimax", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def board(game):
    return game.initialize_board()
