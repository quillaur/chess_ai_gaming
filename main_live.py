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

		play = st.sidebar.button("Play")

		if play:

			white_agent = importlib.import_module(f"agents.{white_name}")
			black_agent = importlib.import_module(f"agents.{black_name}")

			board = chess.Board()

			turn_container = st.empty()
			board_image = st.empty()

			is_white_turn = True
			st.session_state["images"] = []
			count_turn = 0
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

				# Afficher le tour
				turn_container.subheader(f"Turn: {count_turn}")
				count_turn += 1

				# Visualiser le coup
				svg_board = chess.svg.board(board)

				my_png = cairosvg.svg2png(bytestring=svg_board.encode('utf-8'), output_width=600, output_height=500)
				board_image.image(my_png)
				st.session_state["images"].append(my_png)


				if board.outcome():
					if is_white_turn:
						if board.is_checkmate():
							st.session_state["status"] = "White WINS !"
						else:
							st.session_state["status"] = "It's a DRAW !"
					else:
						if board.is_checkmate():
							st.session_state["status"] = "Black WINS !"
						else:
							st.session_state["status"] = "It's a DRAW !"
					break

			turn_container.empty()
			board_image.empty()

		if "status" in st.session_state:
			st.header(st.session_state["status"])

		if "images" in st.session_state and st.session_state["images"]:
			count_turn = len(st.session_state["images"])
			img_index = st.select_slider("Select a turn:", options=list(range(count_turn)))
			st.image(st.session_state["images"][img_index])