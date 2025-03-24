from core.chessBoard import ChessBoard
from core.chessRules import Rules


def main():
    game = Rules()
    print('\nInitial Board:')
    game.board.print_board()
    print('\n-------')
    pawn = game.board.board[6][5]
    move_pawn = game.generate_move(pawn)
    print(f"Possible moves for {pawn}: {move_pawn}")

    knight = game.board.board[0][6]
    move_knight = game.generate_move(knight)
    print(f"Possible moves for {knight}: {move_knight}")


if __name__ == '__main__':
    main()
