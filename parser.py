from pieces import *
from chess_board import Board
from string import ascii_uppercase
from typing import Literal

parsed_dict_keys = Literal["target_piece_type", "initial_position", "target_position", "color_to_move"]
parsed_dict = dict[parsed_dict_keys, str | Color | tuple[int, int]]

def parse_input(input_str:str, color_to_move: Color) -> parsed_dict:
    return_dict: parsed_dict = {"color_to_move": color_to_move}
    target_piece_type: type = None
    if input_str[0] not in ascii_uppercase:
        target_piece_type = Pawn
    else:
        piece_letter = input_str[0]
        piece_type_mapping: dict[str, type] = {
            'R': Rook,
            'N': Knight,
            'B': Bishop,
            'Q': Queen,
            'K': King,
        }
        target_piece_type = piece_type_mapping.get(piece_letter, None)
        if target_piece_type is None:
            raise ValueError(f"Invalid piece letter: {piece_letter}")
        input_str = input_str[1:]  # Remove the piece letter for further parsing
    return_dict["target_piece_type"] = target_piece_type
    input_str = "".join(input_str.split("x"))
    if len(input_str) == 2:
        column_letter = input_str[0]
        row_number = input_str[1]
        column = ord(column_letter.upper()) - ord('A')
        row = int(row_number) - 1
        if not (0 <= column < 8 and 0 <= row < 8):
            raise ValueError(f"Invalid board position: {input_str}")
        return_dict["target_position"] = (column, row)
    elif len(input_str) == 4:
        from_column_letter = input_str[0]
        from_row_number = input_str[1]
        to_column_letter = input_str[2]
        to_row_number = input_str[3]
        from_column = ord(from_column_letter.upper()) - ord('A')
        from_row = int(from_row_number) - 1
        to_column = ord(to_column_letter.upper()) - ord('A')
        to_row = int(to_row_number) - 1
        if not (0 <= from_column < 8 and 0 <= from_row < 8 and 0 <= to_column < 8 and 0 <= to_row < 8):
            raise ValueError(f"Invalid board positions: {input_str}")
        return_dict["initial_position"] = (from_column, from_row)
        return_dict["target_position"] = (to_column, to_row)
    else:
        raise ValueError(f"Invalid input length: {input_str}")
    return return_dict

def move_piece(board: Board, parsed_move: parsed_dict) -> bool:
    target_piece_type: type = parsed_move.get("target_piece_type", None)
    initial_position = parsed_move.get("initial_position", None)
    target_position = parsed_move.get("target_position", None)
    color_to_move = parsed_move.get("color_to_move", None)
    piece: Piece
    if initial_position is not None:
        piece = board.mapping[initial_position[1]][initial_position[0]]
        target_abbr = target_piece_type.abbr
        if not target_abbr == target_piece_type.abbr:
            raise ValueError(f"No {target_piece_type} at position {initial_position}")
        if piece.color != color_to_move:
            raise ValueError(f"The piece on the position {initial_position} is the wrong color")
        if piece.move(target_position):
            board.update_board()
            return True
        else:
            raise ValueError(f"Invalid move for {piece.abbr} from {initial_position} to {target_position}")
    else:
        possible_pieces = []
        for row in board.mapping:
            for pieceiter in row:
                target_abbr = target_piece_type.abbr
                if pieceiter.abbr == target_abbr and pieceiter.color == color_to_move and pieceiter.is_valid_move(target_position):
                    possible_pieces.append(pieceiter)
        if len(possible_pieces) == 1 and possible_pieces[0].color == color_to_move:
            piece = possible_pieces[0]
            piece.move(target_position)
            board.update_all_pieces()
            return True
        elif len(possible_pieces) == 0:
            raise ValueError(f"No valid {target_piece_type} can move to {target_position}")
        else:
            raise ValueError(f"Multiple {target_piece_type} can move to {target_position}, specify initial position")