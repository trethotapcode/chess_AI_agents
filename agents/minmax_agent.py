import random
from core.chessRules import Rules
from algorithm.minmax_search import min_max_search


class MinMaxAgent:
    def __init__(self, color: str, game: Rules, level=1):
        self.color = color
        self.game = game
        self.level = level

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
        
        # print(self.level)
        _, moves = min_max_search(self.game, self.color, self.level)
        selected = random.choice(moves)
        return selected
