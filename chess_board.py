from typing import overload
from pieces import *

class Board:
    def __init__(self, mapping=[
    [Rook("white", (0, 0)), Knight("white", (1, 0)), Bishop("white", (2, 0)), Queen("white", (3, 0)), King("white", (4, 0)), Bishop("white", (5, 0)), Knight("white", (6, 0)), Rook("white", (7, 0))],
    [Pawn("white", (0, 1)), Pawn("white", (1, 1)), Pawn("white", (2, 1)), Pawn("white", (3, 1)), Pawn("white", (4, 1)), Pawn("white", (5, 1)), Pawn("white", (6, 1)), Pawn("white", (7, 1))],
    [Empty((0, 2)), Empty((1, 2)), Empty((2, 2)), Empty((3, 2)), Empty((4, 2)), Empty((5, 2)), Empty((6, 2)), Empty((7, 2))],
    [Empty((0, 3)), Empty((1, 3)), Empty((2, 3)), Empty((3, 3)), Empty((4, 3)), Empty((5, 3)), Empty((6, 3)), Empty((7, 3))],
    [Empty((0, 4)), Empty((1, 4)), Empty((2, 4)), Empty((3, 4)), Empty((4, 4)), Empty((5, 4)), Empty((6, 4)), Empty((7, 4))],
    [Empty((0, 5)), Empty((1, 5)), Empty((2, 5)), Empty((3, 5)), Empty((4, 5)), Empty((5, 5)), Empty((6, 5)), Empty((7, 5))],
    [Pawn("black", (0, 6)), Pawn("black", (1, 6)), Pawn("black", (2, 6)), Pawn("black", (3, 6)), Pawn("black", (4, 6)), Pawn("black", (5, 6)), Pawn("black", (6, 6)), Pawn("black", (7, 6))],
    [Rook("black", (0, 7)), Knight("black", (1, 7)), Bishop("black", (2, 7)), Queen("black", (3, 7)), King("black", (4, 7)), Bishop("black", (5, 7)), Knight("black", (6, 7)), Rook("black", (7, 7))]
], white_king_position=(4,0), black_king_position=(4,7)):
        self.mapping = mapping  
        self.white_king_position = white_king_position
        self.black_king_position = black_king_position
        for row in self.mapping:
            for piece in row:
                if isinstance(piece, Piece):
                    piece.board = self  # ONLY set reference

        # AFTER everything exists:
        self.update_all_pieces()
    def update_all_pieces(self):
        for row in self.mapping:
            for piece in row:
                if isinstance(piece, Piece):
                    piece.update_board(self)

    def update_board(self):
        for row in self.mapping:
            for piece in row:
                piece.update_board(self)

    def get_king_pos(self, color: Color) -> Position:
        if color == 'white':
            return self.white_king_position
        else:
            return self.black_king_position
    
    def __getitem__(self, name: tuple[int, int]):
        '''
        board[(x, y)] Shortcut
        
        :param name: Tuple of (x, y)
        :type name: tuple[int, int]
        '''
        return self.mapping[name[1]][ name[0]]
    
    
    
    def __setitem__(self, name: tuple[int,int], value: Piece):
        '''
        board[(x, y)] = value Shortcut
        
        :param name: Position
        :type name: tuple[int, int]
        :param value: Description
        :type value: Piece
        '''
        self.mapping[name[1]][name[0]] = value