"""Unit tests for the standalone minimax game engine.

Covers board setup, move validity, win/draw detection, and the
alpha-beta minimax AI (immediate wins, blocking, and never losing).
"""
import math
import random


def test_initialize_board_is_3x3_and_empty(game):
    board = game.initialize_board()
    assert len(board) == 3
    assert all(len(row) == 3 for row in board)
    assert all(cell == " " for row in board for cell in row)


def test_initialize_board_returns_fresh_grids(game):
    a = game.initialize_board()
    b = game.initialize_board()
    a[0][0] = "X"
    assert b[0][0] == " "  # no shared references between boards


def test_is_valid_move_on_empty_cell(game, board):
    assert game.is_valid_move(board, 1, 1) is True


def test_is_valid_move_rejects_occupied_cell(game, board):
    game.make_move(board, 1, 1, "X")
    assert game.is_valid_move(board, 1, 1) is False


def test_make_move_places_player_and_returns_true(game, board):
    assert game.make_move(board, 0, 2, "O") is True
    assert board[0][2] == "O"


def test_make_move_on_occupied_cell_leaves_board_unchanged(game, board):
    game.make_move(board, 0, 0, "X")
    assert game.make_move(board, 0, 0, "O") is False
    assert board[0][0] == "X"


def test_check_winner_row(game, board):
    board[2] = ["O", "O", "O"]
    assert game.check_winner(board) == "O"


def test_check_winner_column(game, board):
    for r in range(3):
        board[r][1] = "X"
    assert game.check_winner(board) == "X"


def test_check_winner_diagonals(game, board):
    for i in range(3):
        board[i][i] = "X"
    assert game.check_winner(board) == "X"
    board2 = game.initialize_board()
    for i in range(3):
        board2[i][2 - i] = "O"
    assert game.check_winner(board2) == "O"


def test_check_winner_none_on_fresh_or_draw_board(game, board):
    assert game.check_winner(board) is None
    draw = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "O"],
    ]
    assert game.check_winner(draw) is None


def test_is_draw_false_on_fresh_board(game, board):
    assert game.is_draw(board) is False


def test_is_draw_true_on_full_board(game):
    draw = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "O"],
    ]
    assert game.is_draw(draw) is True


def test_minimax_terminal_scores(game):
    won_x = [["X", "X", "X"], ["O", "O", " "], [" ", " ", " "]]
    won_o = [["O", "O", "O"], ["X", "X", " "], [" ", " ", " "]]
    draw = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "O"]]
    assert game.minimax_with_alpha_beta(won_x, 0, True, -math.inf, math.inf) == 1
    assert game.minimax_with_alpha_beta(won_o, 0, False, -math.inf, math.inf) == -1
    assert game.minimax_with_alpha_beta(draw, 0, True, -math.inf, math.inf) == 0


def test_find_best_move_takes_immediate_win(game, board):
    board[0][0] = "X"
    board[0][1] = "X"
    board[1][0] = "O"
    board[1][1] = "O"
    assert game.find_best_move_with_alpha_beta(board) == (0, 2)


def test_find_best_move_blocks_opponent_win(game, board):
    # O threatens the anti-diagonal at (0, 2); X must block there.
    board[1][1] = "O"
    board[2][0] = "O"
    board[0][0] = "X"
    assert game.find_best_move_with_alpha_beta(board) == (0, 2)


def test_find_best_move_returns_none_on_full_board(game):
    draw = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "O"]]
    assert game.find_best_move_with_alpha_beta(draw) is None


def test_find_best_move_does_not_mutate_board(game, board):
    snapshot = [row[:] for row in board]
    game.find_best_move_with_alpha_beta(board)
    assert board == snapshot


def _best_o_move(game, board):
    """Best reply for O (minimizing player) using the same engine."""
    best_score, best_move = math.inf, None
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "O"
                score = game.minimax_with_alpha_beta(
                    board, 0, True, -math.inf, math.inf
                )
                board[row][col] = " "
                if score < best_score:
                    best_score, best_move = score, (row, col)
    return best_move


def test_ai_never_loses_against_random_opponent(game):
    rng = random.Random(42)
    for _ in range(30):
        board = game.initialize_board()
        turn = "O"
        while game.check_winner(board) is None and not game.is_draw(board):
            if turn == "X":
                move = game.find_best_move_with_alpha_beta(board)
            else:
                empties = [
                    (r, c)
                    for r in range(3)
                    for c in range(3)
                    if board[r][c] == " "
                ]
                move = rng.choice(empties)
            game.make_move(board, move[0], move[1], turn)
            turn = "O" if turn == "X" else "X"
        assert game.check_winner(board) in (None, "X")


def test_optimal_play_ends_in_draw(game):
    board = game.initialize_board()
    turn = "X"
    while game.check_winner(board) is None and not game.is_draw(board):
        if turn == "X":
            move = game.find_best_move_with_alpha_beta(board)
        else:
            move = _best_o_move(game, board)
        game.make_move(board, move[0], move[1], turn)
        turn = "O" if turn == "X" else "X"
    assert game.check_winner(board) is None
    assert game.is_draw(board) is True
