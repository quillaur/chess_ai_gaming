import streamlit as st
import chess
import chess.svg
import base64
from os import walk
import importlib

def render_svg(svg, placeholder=None):
	# From: https://discuss.streamlit.io/t/display-svg/172/5
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64

    if placeholder:
    	placeholder.write(html, unsafe_allow_html=True)
    else:
    	st.write(html, unsafe_allow_html=True)


if __name__ == '__main__':
	# Side panel
	ai_names = ["None"] + [f.replace(".py", "") for root, dirs, files in walk("agents/") for f in files if f.endswith(".py")]
	white_agent = st.sidebar.selectbox("Select the White AI", ai_names)
	black_agent = st.sidebar.selectbox("Select the Black AI", ai_names)

	# Main panel
	st.title(f"{white_agent.upper()} (White) / {black_agent.upper()} (Black)")

	if white_agent != "None" and black_agent != "None":
		white_agent = importlib.import_module(f"agents.{white_agent}")
		black_agent = importlib.import_module(f"agents.{black_agent}")

		play = st.sidebar.button("Play")

		if play:
			board = chess.Board()

			white_turn = True
			st.session_state["svgs"] = []
			st.session_state["status"] = None
			
			with st.spinner("Ais are playing..."):
				c = 0
				placeholder = st.empty()
				svg_holder = st.empty()
				while True:
					if white_turn:
						move  = white_agent.select_move(board, True)
					else:
						move  = black_agent.select_move(board, False)

					white_turn = not white_turn
					board.push(move)
					
					board_svg = chess.svg.board(board)
					st.session_state["svgs"].append(board_svg)

					c += 1
					placeholder.info(f"{c} turned played.")

					render_svg(board_svg, svg_holder)

					if board.outcome():
						if white_turn:
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

					white_turn = not white_turn

				placeholder.empty()
				svg_holder.empty()

		if "status" in st.session_state:
			st.header(st.session_state["status"])

		if "svgs" in st.session_state and st.session_state["svgs"]:
			max_turn_number = len(st.session_state["svgs"])

			turn = st.select_slider("Turn:", options=list(range(max_turn_number)))
			render_svg(st.session_state["svgs"][turn])