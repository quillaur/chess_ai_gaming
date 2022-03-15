import chess
import time
import random

def evaluate(board: chess.Board, is_white: bool):
	position = board.fen()
	position = position.split()[0].replace("/", "")

	score = 0
	for p in position:
		piece_value = get_piece_value(p)
		piece_is_white = p.isupper()

		if (is_white and piece_is_white) or (not is_white and not piece_is_white):
			score += piece_value
		else:
			score -= piece_value

	return score

def get_piece_value(piece: str):
	value = 0
	piece = piece.lower()

	if piece == "p":
		value = 10
	elif piece == "b":
		value = 30
	elif piece == "k":
		value = 30
	elif piece == "r":
		value = 50
	elif piece == "q":
		value = 90
	elif piece == "k":
		value = 900

	return value

def minimax(board: chess.Board, depth: int, is_maximizing: bool, is_white: bool):
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


def select_move(board: chess.Board, is_white: bool):
	depth: int = 3 
	isMaximizing: bool = True 
	start_time = time.time()
	moves = list(board.legal_moves)
	max_score = -9999
	best_move = random.choice(moves)
	for move in moves:
		board.push(move)
		value = max(max_score, minimax(board, depth-1, not isMaximizing, is_white))
		board.pop()
		
		if value > max_score:
			print("Max score: " , value)
			print("Best move: ", move)
			max_score = value
			best_move = move

	print(f"Took {time.time() - start_time} secondes...")
	return best_move
