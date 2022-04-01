import chess
import random


def evaluate(board: chess.Board, is_white: bool) -> int:
	board_fen = board.fen()
	board_fen = board_fen.split()[0]

	score = 0

	for piece in board_fen:
		is_piece_white = piece.isupper()

		if (is_white and is_piece_white) or (not is_white and not piece_is_white):
			score += piece_value(piece)
		else:
			score -= piece_value(piece)

	return score


def piece_value(piece: str) -> int:
	value = 0
	piece = piece.lower()

	if piece == "p":
		value = 10
	elif piece == "b":
		value = 30
	elif piece == "n":
		value = 30
	elif piece == "r":
		value = 50
	elif piece == "q":
		value = 90
	elif piece == "k":
		value = 900

	return value



def minimax(board: chess.Board, depth: int, is_maximizing: bool, is_white: bool) -> int:
	if(depth == 0):
		return evaluate(board, is_white)
	
	moves = list(board.legal_moves)

	if is_maximizing:
		max_score = -9999
		for move in moves:
			board.push(move)
			max_score = max(max_score, minimax(board, depth-1, not is_maximizing, is_white))
			board.pop()

		return max_score
	else:
		min_score = 9999
		for move in moves:
			board.push(move)
			min_score = min(min_score, minimax(board, depth-1, not is_maximizing, is_white))
			board.pop()
		return min_score


def select_move(board: chess.Board, is_white: bool) -> chess.Move:
	depth: int = 3 
	isMaximizing: bool = True 
	moves = list(board.legal_moves)
	max_score = -9999
	best_move = random.choice(moves)
	for move in moves:
		board.push(move)
		value = max(max_score, minimax(board, depth-1, not isMaximizing, is_white))
		board.pop()
		
		if value > max_score:
			max_score = value
			best_move = move

	return best_move