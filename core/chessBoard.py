from piece import Piece


class ChessBoard:
    def __init__(self):

        # init board 8x8
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def setup_board(self):
        # setup pawn in line 1 vs 6
        for i in range(8):
            self.board[1][i] = Piece("Pawn", "black", (1, i))
            self.board[6][i] = Piece("Pawn", "white", (6, i))

        # setup remaining piece
        list_other_piece = ["Rook", "Knight", "Bishop",
                            "Queen", "King", "Bishop", "Kinght", "Rook"]

        for i, each_piece in enumerate(list_other_piece):
            self.board[0][i] = Piece(each_piece, "black", (0, i))
            self.board[7][i] = Piece(each_piece, "white", (7, i))

    # test board
    def print_board(self):
        for row in self.board:
            print(row)


"""# testcase
# a = chessBoard()
# a.setup_board()
# a.print_board()"""
