import streamlit as st
import chess
import chess.svg



if __name__ == '__main__':
	st.title("My chess APP")

	board = chess.Board()

	svr_board = chess.svg.board(board)

	with open("svg_board.svg", "w") as svg:
		svg.write(svr_board)

	legal_moves = list(board.legal_moves)



	st.write(legal_moves) 