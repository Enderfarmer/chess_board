from typing import Literal
from graphics.pieces import *
from string import ascii_uppercase, digits

__all__ = [
    "Piece",
    "Empty",
    "Pawn",
    "Knight",
    "Bishop",
    "Rook",
    "Queen",
    "King",
    "Position",
    "Color"
]

Position = tuple[int, int]
Color = Literal["white", "black"]
def pos_protected(board, position: Position, piece_color: Color) -> bool:
    for row in board.mapping:
        for piece in row:
            if piece.color == piece_color:
                if piece.attacks_position(position):
                    return True
    return False
def pos_attacked(board, position: Position, piece_color: Color) -> bool:
    for row in board.mapping:
        for piece in row:
            if piece.color != piece_color:
                if piece.attacks_position(position):
                    return True
    return False

def is_valid_position(position: Position, old_position: Position = None) -> bool:
    return not position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7 or old_position == position

class Piece:
    abbr = ""
    pattern: list[str]
    def __init__(self, color: Color | None, position: Position,  protected: bool = False):
        self.protected = protected
        self.attacked = False
        self.color = color
        self.position = position
        self.board = None
    def __bool__(self):
        return not self.__class__ == Empty
    def update_board(self, board):
        self.board = board
        self.protected = pos_protected(board, self.position, self.color)
        self.attacked = pos_attacked(board, self.position, self.color)
                    
    def move(self, new_position: Position) -> bool:
        if self.is_valid_move(new_position, True):
            old_x, old_y = self.position
            old_board = self.board
            old_piece = self.board[new_position]

            self.board[new_position] = self
            self.board[self.position] = Empty((old_x, old_y))
            self.position = new_position

            self.update_board(self.board)
            if pos_attacked(self.board, self.board.get_king_pos(self.color), self.color):
                self.position = old_x, old_y
                self.board = old_board
                self.board[self.position] = self
                self.board[new_position] = old_piece
                self.update_board(self.board)
                raise ValueError("Leaves king in check")
            return True
        return False
    def __invert__(self):
        return True
    @classmethod
    def is_valid_pos(cls, new_position: Position, ) -> bool:
        if new_position[0] < 0 or new_position[0] > 7 or new_position[1] < 0 or new_position[1] > 7:
            return False

    def is_valid_move(self, new_position: Position, because_of_move: bool) -> bool:
        raise NotImplementedError("This method should be overridden by subclasses")

    def attacks_position(self, position: Position) -> bool:
        return self.is_valid_move(position)

    def __str__(self):
        return f"A {self.color} {self.__class__.__name__} at {ascii_uppercase[self.position[0]]}{digits[self.position[1] + 1]}"
    def __repr__(self):
        return f"A {self.color} {self.__class__.__name__} at {ascii_uppercase[self.position[0]]}{digits[self.position[1] + 1]}"

class Empty(Piece):
    abbr = "."
    pattern = ['________________'] * 9
    def __init__(self, position: Position):
        self.color = None
        self.position = position
    def is_valid_move(self, new_position, because_of_move = None):
        return False
    
    def __str__(self):
        return f"An empty square at {ascii_uppercase[self.position[0]]}{digits[self.position[1] + 1]}"
    def __repr__(self):
        return f"An empty sqare at {ascii_uppercase[self.position[0]]}{digits[self.position[1] + 1]}"

    
class Pawn(Piece):
    abbr = ""
    pattern = PAWN_PATTERN
    def __init__(self, color: Color, position: Position,  protected: bool = False):
        super().__init__(color, position,  protected)
    def is_valid_move(self, new_position, because_of_move = False):
        if not is_valid_position(new_position, self.position): return False
        if self.color == "white":
            move = (self.position[0], self.position[1] + 1)
            first_move = (self.position[0], 3)
            hit_move0 = (self.position[0] - 1, self.position[1] + 1)
            hit_move1 = (self.position[0] + 1,self.position[1] + 1)
            if new_position == hit_move0:
                if self.board[hit_move0].color == "black":
                    return True
            elif new_position == hit_move1:
                if self.board[hit_move1].color == "black":
                    return True
                
            elif new_position == move:
                if not self.board[move]:
                    return True
            elif new_position == first_move and self.position[1] == 1 and not self.board[move] and not self.board[first_move]:
                return True                
        else:
            move = (self.position[0], self.position[1] -1)
            first_move = (self.position[0], 4)
            hit_move0 = (self.position[0] - 1, self.position[1] - 1)
            hit_move1 = (self.position[0] + 1,self.position[1] - 1)
            if new_position == hit_move0:
                if self.board[hit_move0].color == "white":
                    return True
            elif new_position == hit_move1:
                if self.board[hit_move1].color == "white":
                    return True
            elif new_position == move:
                if not self.board[move]:
                    return True
            elif new_position == first_move and self.position[1] == 6:
                if not self.board[move] and not self.board[first_move]:
                    return True
            
        return False

    def move(self, new_position: Position, piece_type_if_promoted: Piece = None) -> bool:
        if super().move(new_position):
            if (self.color == "white" and self.position[1] == 7) or (self.color == "black" and self.position[1] == 0):
                self.promote(piece_type_if_promoted)
            return True
    def promote(self, piece_type: Piece = None):
        self.__class__ = piece_type if piece_type else Queen

class Knight(Piece):
    pattern = KNIGHT_PATTERN
    def __init__(self, color: Color, position: Position,  protected: bool = False):
        super().__init__(color, position,  protected)
    abbr = "N"
    def is_valid_move(self, new_position, because_of_move = None):
        if not is_valid_position(new_position, self.position): return False
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
class Bishop(Piece):
    abbr = "B"
    pattern = BISHOP_PATTERN
    def __init__(self, color: Color, position: Position,  protected: bool = False):
        super().__init__(color, position,  protected)
    @classmethod
    def is_valid_bishop_move(cls,old_position, new_position, board):
        if not is_valid_position(new_position, old_position): return False
        dx = abs(new_position[0] - old_position[0])
        dy = abs(new_position[1] - old_position[1])
        if dx == dy:
            step_x = 1 if new_position[0] > old_position[0] else -1
            step_y = 1 if new_position[1] > old_position[1] else -1
            x, y = old_position
            x += step_x
            y += step_y
            while (x, y) != new_position:
                if not not board[x, y]:
                    return False
                x += step_x
                y += step_y
            return True
        return False
    def is_valid_move(self, new_position, because_of_input:bool = None) -> bool:
        if not is_valid_position(new_position, self.position): return False
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])
        if dx == dy:
            step_x = 1 if new_position[0] > self.position[0] else -1
            step_y = 1 if new_position[1] > self.position[1] else -1
            x, y = self.position
            x += step_x
            y += step_y
            while (x, y) != new_position:
                if not not self.board[x,y]:
                    return False
                x += step_x
                y += step_y
            return True
        else:
            return False
class Rook(Piece):
    abbr = "R"
    pattern = ROOK_PATTERN
    def __init__(self, color: Color, position: Position,  protected: bool = False):
        super().__init__(color, position)
    @classmethod
    def is_valid_rook_move(cls,old_position, new_position, board):
        if not is_valid_position(new_position, old_position): return False
        if new_position[0] == old_position[0] or new_position[1] == old_position[1]:
            if new_position[0] == old_position[0]:
                step = 1 if new_position[1] > old_position[1] else -1
                for y in range(old_position[1] + step, new_position[1], step):
                    if not not board[old_position[0], y]:
                        return False
            else:
                step = 1 if new_position[0] > old_position[0] else -1
                for x in range(old_position[0] + step, new_position[0], step):
                    if not not board[x,old_position[1]]:
                        return False
            return True
        return False
    def is_valid_move(self, new_position, because_of_move = None):
        if not is_valid_position(new_position, self.position): return False
        if new_position[0] == self.position[0] or new_position[1] == self.position[1]:
            if new_position[0] == self.position[0]:
                step = 1 if new_position[1] > self.position[1] else -1
                for y in range(self.position[1] + step, new_position[1], step):
                    if not not self.board[self.position[0],y]:
                        return False
            else:
                step = 1 if new_position[0] > self.position[0] else -1
                for x in range(self.position[0] + step, new_position[0], step):
                    if not not self.board[x,self.position[1]]:
                        return False
            return True
        return False
class Queen(Piece):
    abbr = "Q"
    pattern = QUEEN_PATTERN
    def __init__(self, color: Color, position: Position, protected: bool = False):
        super().__init__(color, position,  protected)
    def is_valid_move(self, new_position, because_of_move = None):
        if not is_valid_position(new_position, self.position): return False
        if Rook.is_valid_rook_move(self.position, new_position, self.board) or Bishop.is_valid_bishop_move(self.position, new_position, self.board):
            return True
        return False
class King(Piece):
    abbr = "K"
    pattern = KING_PATTERN
    def __init__(self, color: Color, position: Position, protected: bool = False):
        super().__init__(color, position, protected)
    def is_valid_move(self, new_position, because_of_move = None):
        if not is_valid_position(new_position, self.position): return False
        dx = abs(new_position[0] - self.position[0])
        dy = abs(new_position[1] - self.position[1])
        if dx <= 1 and dy <= 1:
            return not pos_attacked(self.board, new_position, self.color)
        return False
    def attacks_position(self, position: Position) -> bool:
        dx = abs(position[0] - self.position[0])
        dy = abs(position[1] - self.position[1])
        return dx <= 1 and dy <= 1