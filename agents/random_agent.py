import random
from core.chessRules import Rules


class RandomAgent:
    def __init__(self, color: str, game: Rules):
        self.color = color
        self.game = game

    def select_move(self):
        moves = []

        # update move in moves_list each of turn
        for row in self.game.board.board:
            # cell maybe contains piece or None.
            for cell in row:
                if cell is not None and cell.color == self.color:
                    valid_moves = self.game.generate_legal_moves(piece=cell)
                    for element in valid_moves:
                        moves.append((cell, element))


        # lost
        if not moves:
            return None

        # random move choice
        selected = random.choice(moves)

        # contains name of piece and new_position.
        return selected
