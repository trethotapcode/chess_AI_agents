from chessBoard import ChessBoard
from piece import Piece


class Rules:
    def __init__(self):
        # chess board object
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

        return moves

    # def gen_rook_move(self, piece: Piece, row, col):
    #     moves = []
    #     step = [i for i in range(8)]

    #     # rook can move all cells in row and col.

    #     return moves

    # check valid: move is possible.
    def is_valid(self, piece, new_position):
        valid_moves = self.generate_move(piece)

        # if new_position is not in valid moves, return false.
        return new_position in valid_moves


"""
# testcase:
if __name__ == '__main__':
    game = Rules()
    game.board.setup_board()
    pawn = game.board.board[6][0]
    print("Testing moves for:", pawn)

    moves = game.generate_move(pawn)
    print("Possible moves:", moves)
    print("Move (5,0) is valid:", game.is_valid(pawn, (5, 0)))
    print("Move (4,1) is valid:", game.is_valid(pawn, (4, 1)))
"""
