# python -m core.chessRules
from core.chessBoard import ChessBoard
from core.piece import Piece
from core.specialRules import Special


class Rules:
    def __init__(self):
        self.board = ChessBoard()
        self.special = Special(self)

    def reset_all(self):
        self.board = ChessBoard()

    def generate_move(self, piece: Piece):
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
        step = -1 if piece.color == "white" else 1

        if (0 <= row + step <= 7) and (self.board.board[row + step][col] is None):
            moves.append((row + step, col))

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
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        for r, c in directions:
            dr, dc = row, col
            while True:
                dr += r
                dc += c
                if (0 <= dr <= 7) and (0 <= dc <= 7):
                    if self.board.board[dr][dc] is None:
                        moves.append((dr, dc))
                    else:
                        if piece.color != self.board.board[dr][dc].color:
                            moves.append((dr, dc))
                        break
                else:
                    break
        return moves

    # knight
    def gen_knight_move(self, piece: Piece, row, col):
        moves = []
        direction = [
            (2, 1),  (-2, 1),  (2, -1),  (-2, -1),
            (1, 2),  (-1, 2),  (1, -2),  (-1, -2)
        ]
        for r, c in direction:
            dr, dc = row + r, col + c
            if (0 <= dr <= 7) and (0 <= dc <= 7):
                if self.board.board[dr][dc] is None:
                    moves.append((dr, dc))
                else:
                    if self.board.board[dr][dc].color != piece.color:
                        moves.append((dr, dc))
        return moves

    # bishop
    def gen_bishop_move(self, piece: Piece, row, col):
        moves = []
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for r, c in directions:
            dr, dc = row, col
            while True:
                dr += r
                dc += c
                if (0 <= dr <= 7) and (0 <= dc <= 7):
                    if self.board.board[dr][dc] is None:
                        moves.append((dr, dc))
                    else:
                        if self.board.board[dr][dc].color != piece.color:
                            moves.append((dr, dc))
                        break
                else:
                    break
        return moves

    # queen = rook + bishop
    def gen_queen_move(self, piece: Piece, row, col):
        return self.gen_rook_move(piece, row, col) + self.gen_bishop_move(piece, row, col)

    # king
    def gen_king_move(self, piece: Piece, row, col):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for r, c in directions:
            dr, dc = row + r, col + c
            if (0 <= dr <= 7) and (0 <= dc <= 7):
                if self.board.board[dr][dc] is None:
                    moves.append((dr, dc))
                else:
                    if self.board.board[dr][dc].color != piece.color:
                        moves.append((dr, dc))

        # update castling
        moves += self.gen_castling_moves(piece, row, col)
        return moves

    # update castling

    def gen_castling_moves(self, piece: Piece, row, col):
        moves = []
        if piece.piece_type != "King" or getattr(piece, "has_moved", True):
            return moves

        color = piece.color
        king_row = 7 if color == "white" else 0

        if row != king_row or col != 4:
            return moves

        rook_kingside_col = 7
        path_kingside = [5, 6]

        # kingside castling
        rook_ks = self.board.board[king_row][rook_kingside_col]
        if (isinstance(rook_ks, Piece)
            and rook_ks.piece_type == "Rook"
            and rook_ks.color == color
                and not getattr(rook_ks, "has_moved", True)):

            if all(self.board.board[king_row][c] is None for c in path_kingside):
                if not self.special.is_checking(color):
                    can_castle = True
                    for check_col in path_kingside:
                        if not self.simulate_king_move_and_check(piece, (king_row, check_col)):
                            can_castle = False
                            break

                    if can_castle:
                        moves.append((king_row, 6))

        # queenside castling
        rook_queenside_col = 0
        path_queenside = [1, 2, 3]
        rook_qs = self.board.board[king_row][rook_queenside_col]

        if (isinstance(rook_qs, Piece)
            and rook_qs.piece_type == "Rook"
            and rook_qs.color == color
                and not getattr(rook_qs, "has_moved", True)):

            if all(self.board.board[king_row][c] is None for c in path_queenside):
                if not self.special.is_checking(color):
                    can_castle = True
                    for check_col in [3, 2]:
                        if not self.simulate_king_move_and_check(piece, (king_row, check_col)):
                            can_castle = False
                            break

                    if can_castle:
                        moves.append((king_row, 2))

        return moves

    def simulate_king_move_and_check(self, king_piece, new_pos):
        orig_pos = king_piece.position
        r_new, c_new = new_pos
        captured_piece = self.board.board[r_new][c_new]

        self.board.board[orig_pos[0]][orig_pos[1]] = None
        king_piece.position = (r_new, c_new)
        self.board.board[r_new][c_new] = king_piece

        is_in_check = self.special.is_checking(king_piece.color)

        # undo
        self.board.board[r_new][c_new] = captured_piece
        king_piece.position = orig_pos
        self.board.board[orig_pos[0]][orig_pos[1]] = king_piece

        return (not is_in_check)

    def is_valid(self, piece, new_position):
        valid_moves = self.generate_move(piece)
        return new_position in valid_moves

    def make_move(self, piece: Piece, move_position):
        r, c = piece.position
        dr, dc = move_position

        if piece.piece_type == "King" and abs(dc - c) == 2:
            if dc == 6:
                rook_col_from, rook_col_to = 7, 5
            elif dc == 2:
                rook_col_from, rook_col_to = 0, 3
            rook_piece = self.board.board[r][rook_col_from]
            if rook_piece and rook_piece.piece_type == "Rook":
                self.board.board[r][rook_col_to] = rook_piece
                self.board.board[r][rook_col_from] = None
                rook_piece.position = (r, rook_col_to)
                setattr(rook_piece, "has_moved", True)

        piece.move((dr, dc))
        self.board.board[dr][dc] = piece
        self.board.board[r][c] = None

        setattr(piece, "has_moved", True)

    def check_status(self, color):
        if self.is_insufficient_material():
            return "draw"
        if self.special.is_checkmate(color):
            return "checkmate"
        elif self.special.is_checking(color):
            return "check"
        else:
            return "ongoing"

    def generate_legal_moves(self, piece: Piece):
        color = piece.color
        moves = self.generate_move(piece)

        legal_moves = []
        original_position = piece.position

        for move in moves:
            r_new, c_new = move
            captured_piece = self.board.board[r_new][c_new]

            # temp
            self.make_move(piece, move)

            # not checking -> can castling
            if not self.special.is_checking(color):
                legal_moves.append(move)

            # undo for King
            self.board.board[original_position[0]
                             ][original_position[1]] = piece
            piece.position = original_position
            self.board.board[r_new][c_new] = captured_piece

            # if moving is castling, undo for Rook.
            if piece.piece_type == "King" and abs(c_new - original_position[1]) == 2:

                if c_new == 6:  # kingside
                    self.board.board[original_position[0]
                                     ][7] = self.board.board[original_position[0]][5]

                    if self.board.board[original_position[0]][7] is not None:
                        self.board.board[original_position[0]][7].position = (
                            original_position[0], 7)

                    self.board.board[original_position[0]][5] = None

                elif c_new == 2:  # queenside
                    self.board.board[original_position[0]
                                     ][0] = self.board.board[original_position[0]][3]

                    if self.board.board[original_position[0]][0] is not None:
                        self.board.board[original_position[0]][0].position = (
                            original_position[0], 0)

                    self.board.board[original_position[0]][3] = None

        return legal_moves

    def is_insufficient_material(self):
        """Check for insufficient material draw."""
        pieces = []
        for row in self.board.board:
            for p in row:
                if isinstance(p, Piece) and p.piece_type != "King":
                    pieces.append(p.piece_type)
        # no material
        if not pieces:
            return True
        # single minor piece
        if len(pieces) == 1 and pieces[0] in ("Bishop", "Knight"):
            return True
        # two knights only
        if len(pieces) == 2 and all(pt == "Knight" for pt in pieces):
            return True
        return False