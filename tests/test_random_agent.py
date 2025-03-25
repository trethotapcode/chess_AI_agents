# python tests/test_random_agents.py
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from agents.random_agent import RandomAgent
from core.chessRules import Rules


class test_random_agent(unittest.TestCase):
    def test_white_agent(self):
        game = Rules()
        agent = RandomAgent('white', game)
        selected = agent.select_move()
        self.assertIsNotNone(selected, "agent should choose valid move")

        piece, position = selected
        move = game.generate_move(piece)

        self.assertIn(position, move, "selected should be valid")

    def test_black_agent(self):
        game = Rules()
        agent = RandomAgent('black', game)
        selected = agent.select_move()
        self.assertIsNotNone(selected, "agent should choose valid move")

        piece, position = selected
        move = game.generate_move(piece)

        self.assertIn(position, move, "selected should be valid")


if __name__ == '__main__':
    unittest.main()
