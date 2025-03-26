class Special:
    def __init__(self, game):
        self.game = game

    # checking rules
    def is_checking(self, color):
        king_position = None
        board = self.game.board.board
        opponent_color = 'white' if color == 'black' else 'black'

        # find king position
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece is not None and piece.color == color and piece.piece_type == 'King':
                    king_position = (r, c)

        # Is king checking?
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece.color == opponent_color:
                    moves = self.game.generate_move(piece)
                    # moves of one pieces have position of king
                    if king_position in moves:
                        return True
        # king isn't checking
        return False

    # can king is checkmate?
    def is_checkmate(self, color):
        if not self.is_checking(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.game.board.board[row][col]
                if piece and piece.color == color:
                    moves = self.game.generate_move(piece)

                    # save the position of piece to undo.
                    original_position = (row, col)

                    for move in moves:
                        # at move postion, can contains opponent piece, save.
                        opponent_piece = self.game.board.board[move[0]][move[1]]

                        # try move and undo immediately to keep the board state
                        self.game.make_move(piece, move)
                        in_check = self.is_checking(color)

                        # undo
                        self.game.board.board[original_position[0]
                                              ][original_position[1]] = piece
                        piece.position = original_position
                        self.game.board.board[move[0]
                                              ][move[1]] = opponent_piece

                        if in_check == False:
                            return False

        return True
