from chess_board import Board, CheckMateError, StaleMateError
from render import render, clear
from pieces import pos_attacked
from parser import parse_input, move_piece

clear()
board = Board()
color_to_move = "white"
error = None
while True:
    clear()
    render(board)
    if error is not None:
        print("Invalid move: ", error)
        error = None
    move = input(f"Enter your move ({color_to_move}): ")
    parsed_move = parse_input(move, color_to_move)
    
    try:
        if not board.has_legal_move(color_to_move):
            if pos_attacked(board, board.get_king_pos(color_to_move), color_to_move):
                raise CheckMateError()
            else:
                raise StaleMateError()
        move_piece(board, parsed_move)

    except ValueError as e:
        error = e
        continue
    except CheckMateError:
        print(f"The {color_to_move} side has been checkmated. The game is over.")
        break
    except StaleMateError:
        print(f"There is a stalemate on the board. The game resulted in a draw.")
        break
    color_to_move = "black" if color_to_move == "white" else "white"
    