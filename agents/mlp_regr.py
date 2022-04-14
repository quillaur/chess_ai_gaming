from sklearn.neural_network import MLPRegressor
import pandas as pd
import numpy as np
import csv
import os
import chess


def create_mlp():
	# Aller chercher toutes les parties sur lesquelles le MLP doit s'entraîner.
	all_games = []
	for root, dirs, files in os.walk("games"):
		for file in files:
			if file.endswith(".csv"):
				filename = os.path.join(root, file)
				with open(filename, "r") as f:
					rows = list(csv.reader(f))
					all_games.extend(rows)

	# Mettre toutes les parties dans une dataframes
	df = pd.DataFrame(all_games)

	# Initialiser le MLP
	mlp_regr = MLPRegressor()

	# Si j'ai des données, entraîner mon model avec celles-ci.
	if not df.empty:
		x_train = df.iloc[:, :-1]
		y_train = df.iloc[:,-1:]
		mlp_regr.fit(x_train, y_train)

	# Une fois l'entraînement fini
	# sauvegarder le model
	from joblib import dump
	dump(mlp_regr, 'mlp_model.joblib') 

	return mlp_regr


def select_move(board: chess.Board, is_white: bool, mlp: MLPRegressor) -> chess.Move:
	# La liste des coup possible à partir de la position actuelle sur le plateau de jeu (board)
	moves = list(board.legal_moves)

	# On va selectionner le coup avec le meilleur score
	max_score = -99999999
	best_move = None
	
	# Pour chaque coup
	for move in moves:
		# Jouer le coup sur le board
		board.push(move)

		# Demander au MLP comment il évalue cette nouvelle position
		score = mlp_prediction(board, is_white, mlp)
		board.pop()
		
		if score > max_score:
			max_score = score
			best_move = move


	return best_move


def mlp_prediction(board: chess.Board, is_white: bool, mlp: MLPRegressor) -> int:
	# Fonction demandant au MLP de donner un score à cette position.

	# Convertir l'objet board en un format utilisable par le MLP.
	board_convert = convert_board_to_array(board, is_white)

	# Prédire le score de cette position.
	score = mlp.predict(board_convert)

	return score

def convert_board_to_array(board: chess.Board, is_white: bool) -> np.array:
	position = board.fen()
	position = position.split()[0].replace("/", "")

	board_array = []
	for p in position:
		piece_value = get_piece_value(p)
		piece_is_white = p.isupper()

		if (is_white and piece_is_white) or (not is_white and not piece_is_white):
			board_array.append(piece_value)
		elif p.isdigit():
			board_array.extend([0]*int(p))
		else:
			board_array.append(-piece_value)

	board_array = np.array(board_array)

	return np.reshape(board_array, (1, -1))



def get_piece_value(piece: str):
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


# def play_game(mlp: MLPRegressor, is_white: bool):
# 	board


if __name__ == '__main__':
	mlp = create_mlp()
	print("Job done !")

	#for i in range(1):

