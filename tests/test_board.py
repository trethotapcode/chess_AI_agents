# python tests/test_board.py
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from core.piece import Piece
from core.chessBoard import ChessBoard


class TestChessBoard(unittest.TestCase):

    def test_board_initialization(self):
        board = ChessBoard()
        pieces = sum(
            1 for row in board.board for piece in row if piece is not None)
        self.assertEqual(pieces, 32)

    def test_piece_initial_position(self):
        board = ChessBoard()
        self.assertIsInstance(board.board[0][0], Piece)
        self.assertEqual(board.board[0][0].piece_type, 'Rook')
        self.assertEqual(board.board[0][0].color, 'black')

        self.assertIsInstance(board.board[7][4], Piece)
        self.assertEqual(board.board[7][4].piece_type, 'King')
        self.assertEqual(board.board[7][4].color, 'white')

    def test_empty_positions(self):
        board = ChessBoard()
        self.assertIsNone(board.board[3][3])
        self.assertIsNone(board.board[4][4])


if __name__ == '__main__':
    unittest.main()
