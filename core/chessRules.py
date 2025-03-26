# python -m core.chessRules
from core.chessBoard import ChessBoard
from core.piece import Piece
from core.specialRules import Special


class Rules:
    def __init__(self):
        # chess board object
        self.board = ChessBoard()
        self.special = Special(self)

    def reset_all(self):
        self.board = ChessBoard()

    def generate_move(self, piece: Piece):
        # list of valid steps.
        moves = []
        row, col = piece.position

        if piece.piece_type == "Pawn":
            moves += self.gen_pawn_move(piece, row, col)

        if piece.piece_type == "Rook":
            moves += self.gen_rook_move(piece, row, col)

        if piece.piece_type == "Knight":
            moves += self.gen_knight_move(piece, row, col)

        if piece.piece_type == "Bishop":
            moves += self.gen_bishop_move(piece, row, col)

        if piece.piece_type == "Queen":
            moves += self.gen_queen_move(piece, row, col)

        if piece.piece_type == "King":
            moves += self.gen_king_move(piece, row, col)

        return moves

    # pawn
    def gen_pawn_move(self, piece: Piece, row, col):
        moves = []

        # white up -> -1, black +1
        step = -1 if piece.color == "white" else 1

        # pawn go forward 1 step if empty cell or in (0,7)
        if (0 <= row + step <= 7) and (self.board.board[row + step][col] is None):
            moves.append((row + step, col))

        # pawn can move 2 step when it's in begin position.
            if (row == 1 and piece.color == "black") or (row == 6 and piece.color == "white"):
                if (self.board.board[row + step*2][col] is None) and (self.board.board[row + step][col] is None):
                    moves.append((row + step*2, col))

        for offset in [-1, 1]:
            new_col = col + offset
            new_row = row + step
            if (0 <= new_row <= 7) and (0 <= new_col <= 7):
                new_piece = self.board.board[new_row][new_col]
                if new_piece is not None and new_piece.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    # rook
    def gen_rook_move(self, piece: Piece, row, col):
        moves = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)
                      ]  # up, down, right, left.
        # rook can move all cells in row and col.
        for r, c in directions:
            dr, dc = row, col

            while True:
                dr += r
                dc += c
                if (0 <= dr <= 7) and (0 <= dc <= 7):
                    if self.board.board[dr][dc] is None:
                        moves.append((dr, dc))
                    else:
                        if (piece.color != self.board.board[dr][dc].color):
                            moves.append((dr, dc))
                        break
                else:
                    break

        return moves

    # knight
    def gen_knight_move(self, piece: Piece, row, col):
        moves = []
        direction = [(2, 1), (-2, 1), (2, -1), (-2, -1),
                     (1, 2), (-1, 2), (-1, -2), (1, -2)]
        # knight has 8 directions to move.

        for r, c in direction:
            dr, dc = row, col
            dr += r
            dc += c

            if (0 <= dr <= 7) and (0 <= dc <= 7):
                if (self.board.board[dr][dc] is None):
                    moves.append((dr, dc))
                else:
                    if (self.board.board[dr][dc].color != piece.color):
                        moves.append((dr, dc))
                    else:
                        continue

        return moves

    # bishop
    def gen_bishop_move(self, piece: Piece, row, col):
        moves = []
        # 4 diagonal
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        for r, c in directions:
            dr, dc = row, col
            while True:
                dr += r
                dc += c
                if (0 <= dr <= 7) and (0 <= dc <= 7):
                    if (self.board.board[dr][dc] is None):
                        moves.append((dr, dc))
                    else:
                        if (self.board.board[dr][dc].color != piece.color):
                            moves.append((dr, dc))
                        break
                else:
                    break

        return moves

    # queen move = rook + bishop
    def gen_queen_move(self, piece: Piece, row, col):
        return (self.gen_rook_move(piece, row, col)
                + self.gen_bishop_move(piece, row, col))

    # king
    def gen_king_move(self, piece: Piece, row, col):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for r, c in directions:
            dr, dc = row, col
            dr += r
            dc += c

            if (0 <= dr <= 7) and (0 <= dc <= 7):
                if (self.board.board[dr][dc] is None):
                    moves.append((dr, dc))
                else:
                    if (self.board.board[dr][dc].color != piece.color):
                        moves.append((dr, dc))
                    else:
                        continue

        return moves

    # check valid: move is possible.
    def is_valid(self, piece, new_position):
        valid_moves = self.generate_move(piece)
        # if new_position is not in valid moves, return false.
        return new_position in valid_moves

    # capture function
    def make_move(self, piece: Piece, move_position):
        r, c = piece.position
        dr, dc = move_position

        # go to new position
        piece.move((dr, dc))

        self.board.board[dr][dc] = piece
        self.board.board[r][c] = None

    # checking
    def check_status(self, color):
        if self.special.is_checkmate(color):
            return "checkmate"
        elif self.special.is_checking(color):
            return "check"
        else:
            return "ongoing"
    
    # legal_move after checking
    def generate_legal_moves(self, piece):
        color = piece.color
        moves = self.generate_move(piece)  

        legal_moves = []
        original_position = piece.position

        for move in moves:
            r_new, c_new = move
            captured_piece = self.board.board[r_new][c_new]

            # make_move temp
            self.make_move(piece, move)

            # isn't checking? 
            if not self.special.is_checking(color):
                legal_moves.append(move)

            # undo
            self.board.board[original_position[0]][original_position[1]] = piece
            piece.position = original_position
            self.board.board[r_new][c_new] = captured_piece

        return legal_moves

    
# """
# # testcase:
# if __name__ == '__main__':
#     game = Rules()

#     pawn = game.board.board[1][5]
#     rook = game.board.board[7][7]
#     knight = game.board.board[7][6]
#     bishop = game.board.board[0][5]
#     queen = game.board.board[7][3]
#     king = game.board.board[0][4]

#     # Change all 'king' below becomes any pieces to test.
#     print("Testing moves for:", pawn)

#     moves = game.generate_move(pawn)
#     print("Possible moves:", moves)
#     print("Move (2,0) is valid:", game.is_valid(pawn, (2, 0)))
#     print("Move (4,1) is valid:", game.is_valid(pawn, (4, 1)))
# # """
