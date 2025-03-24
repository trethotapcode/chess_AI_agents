import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from core.piece import Piece


class test_piece(unittest.TestCase):
    def test_create(self):
        piece = Piece("Queen", "black", (0, 3))
        self.assertEqual(piece.piece_type, "Queen")
        self.assertEqual(piece.color, "black")
        self.assertEqual(piece.position, (0, 3))

    def test_move(self):
        piece = Piece("Pawn", "white", (6, 0))
        piece.move((5, 0))
        self.assertEqual(piece.position, (5, 0))

    def test_string(self):
        piece = Piece("Knight", "black", (1, 0))
        self.assertEqual(str(piece), 'black Knight at (1, 0)')


if __name__ == '__main__':
    unittest.main()
