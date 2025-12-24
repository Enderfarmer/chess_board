from chess_board import Board
from render import render, clear
from pieces import Pawn
from parser import parse_input, move_piece

clear()
board = Board([[Pawn("white", (0,0)), Pawn("black", (0,1))]])
color_to_move = "white"
error = None
while True:
    # clear()
    render(board)
    if error is not None:
        print("Invalid move: ", error)
        print("Traceback: ", error.__traceback__.__str__())
        error = None
    move = input(f"Enter your move ({color_to_move}): ")
    parsed_move = parse_input(move, color_to_move)
    try:
        move_piece(board, parsed_move)
    except Exception as e:
        error = e
        continue
    color_to_move = "black" if color_to_move == "white" else "white"
    