from ui.chess_UI import run_game

if __name__ == '__main__':
    run_game()




# # main task 1
# def main():
#     game = Rules()
#     print('\nInitial Board:')
#     game.board.print_board()
#     print('\n-------')
#     pawn = game.board.board[6][5]
#     move_pawn = game.generate_move(pawn)
#     print(f"Possible moves for {pawn}: {move_pawn}")

#     knight = game.board.board[0][6]
#     move_knight = game.generate_move(knight)
#     print(f"Possible moves for {knight}: {move_knight}")

# ------------------------------------------------------------

## main task 2
# from core.chessBoard import ChessBoard
# from core.chessRules import Rules
# from agents.random_agent import RandomAgent

# def main():
#     game = Rules()

#     # create two random agents
#     white_agent = RandomAgent('white', game)
#     black_agent = RandomAgent('black', game)

#     turn = 'white'
#     move_count = 0

#     # play game
#     while True:
#         current_agent = white_agent if turn == 'white' else black_agent
#         selected = current_agent.select_move()

#         if selected == None:
#             print(f"Game over after {move_count} moves! {turn} has no moves left.")
#             break

#         piece, pos = selected
#         game.make_move(piece, pos)
#         print(f"{turn.capitalize()} moved {piece.piece_type} to {pos}")
#         # swap turn
#         turn = 'black' if turn == 'white' else 'white'
#         status = game.check_status(turn)
        
#         if status == "checkmate":
#             print(f"Game over after {move_count} moves! {turn} has no moves left.")
#         elif status == "check":
#             print(f"{turn.capitalize()} is in check!")
#         # endless: after 100 moves
#         move_count += 1
#         if move_count > 1000:
#             print("Game stopped after 100 moves (likely endless)")
#             break

#     game.board.print_board()