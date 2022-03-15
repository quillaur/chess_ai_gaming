import chess
import random


def select_move(board: chess.Board, is_white: bool):
	moves = list(board.legal_moves)
	return random.choice(moves)