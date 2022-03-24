import streamlit as st
import chess
import chess.svg
from os import walk
import importlib
import cairosvg


if __name__ == '__main__':
	# Récupérer les IA disponibles.
	# agents = []
	# for root, dirs, files in walk("agents"):
	# 	for file in files:
	# 		if file.endswith(".py"):
	# 			ai_name = file.replace(".py", "")
	# 			agents.append(ai_name)

	agents = ["None"] + [file.replace(".py", "") for root, dirs, files in walk("agents") for file in files if file.endswith(".py")]
	white_name = st.sidebar.selectbox("Select the white AI:", agents)
	black_name = st.sidebar.selectbox("Select the black AI:", agents)

	st.title("AI chess APP")

	if white_name != "None" and black_name != "None":
		st.header(f"{white_name} (white) versus {black_name} (black)")

		if st.sidebar.button("Play"):

			white_agent = importlib.import_module(f"agents.{white_name}")
			black_agent = importlib.import_module(f"agents.{black_name}")

			board = chess.Board()

			board_image = st.empty()

			is_white_turn = True
			while True:
				# Selectionner le coup à jouer
				if is_white_turn:
					move = white_agent.select_move(board, True)
				else:
					move = black_agent.select_move(board, False)

				# Le prochain tour, l'autre IA jouera
				is_white_turn = not is_white_turn

				# Jouer le coup
				board.push(move)

				# Visualiser le coup
				svg_board = chess.svg.board(board)

				my_png = cairosvg.svg2png(bytestring=svg_board.encode('utf-8'), output_width=600, output_height=500)
				board_image.image(my_png)


				if board.outcome():
					break


		# svr_board = chess.svg.board(board)

		# with open("svg_board.svg", "w") as svg:
		# 	svg.write(svr_board)

		# legal_moves = list(board.legal_moves)



		# st.write(legal_moves) 