from chess_board import Board
from pieces import Piece
from graphics.numbers import num_graphic_mapping
from graphics.pieces import PAWN_PATTERN
from graphics.letters import letter_graphic_mapping
from subprocess import run

def separator(big_row_index, cols, piece_width, rows):
    beginning_char = "┏"
    ending_char = "┓"
    joiner = "┳"
    class Numbers:
        FIRST = 0
        LAST = rows + 1
    match big_row_index:
        case Numbers.LAST:
            pass
        case Numbers.FIRST:
            beginning_char = "┗"
            ending_char = "┛"
            joiner = "┻"
        case _:
            beginning_char = "┣"
            joiner = "╋"
            ending_char = "┫"
    print(beginning_char + joiner.join(["━" * piece_width for _ in range(cols + 1)]) + ending_char)


def graphics(board: Board) -> str:
    rows = []
    for big_row in range(len(board.mapping), -1, -1):
        big_row_state = []
        for normal_row in range(len(PAWN_PATTERN)):
            row = []
            for column in range(len(board.mapping[0]) + 1):
                if big_row == len(board.mapping):
                    row.append(letter_graphic_mapping[column][normal_row].replace("_", " ").replace("H", "█"))
                else:
                    if column == 0:
                        row.append(num_graphic_mapping[big_row][normal_row].replace("_", " ").replace("H", "█"))
                    else:
                        piece: Piece = board[column-1,big_row]
                        if piece.color == 'black':
                            row.append(piece.pattern[normal_row].replace("H", " ").replace("_", " ").replace("J", "█"))
                        elif piece.color == 'white':
                            row.append(piece.pattern[normal_row].replace("_", " ").replace("H", "█").replace("J", "█"))
                        else:
                            row.append(" " * len(PAWN_PATTERN[0]))
            print("┃" + "┃".join(row) + "┃")
            big_row_state.append("|".join(row)+"\n")
        # print("━" * ((len(board.mapping[0]) + 1)* len(PAWN_PATTERN[0]) + len(PAWN_PATTERN[0]) - 1))
        separator(big_row, len(board.mapping[0]), len(PAWN_PATTERN[0]), len(board.mapping))

        rows.extend(big_row_state)
        rows.append("-" * len(big_row_state[0]))

    return "\n".join(rows)

def render(board: Board):
    graphics(board)
    
def clear():
    run("clear", shell=True)