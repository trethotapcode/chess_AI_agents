# python ui/chess_UI.py
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import pygame
from core.chessBoard import ChessBoard
from core.chessRules import Rules
from agents.random_agent import RandomAgent
from ui.notification import show_notification, draw_notification, popup_checkmate, choose_first_player
from ui.main_menu import main_menu



SQUARE_SIZE = 80
PIECE_SIZE = 70

# loading piece images
def load_images():
    color_type = ['b', 'w']
    pieces = ['bishop', 'king', 'knight', 'pawn', 'queen', 'rook']
    images_piece = {}

    for color in color_type:
        for piece in pieces:
            path = f"./ui/assets/{color}{piece}.png"
            images_piece[f"{color}{piece}"] = pygame.transform.scale(
                pygame.image.load(path), (PIECE_SIZE, PIECE_SIZE))

    return images_piece

# draw board
def draw_board(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for r in range(8):
        for c in range(8):
            color = colors[(r+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


IMAGES = load_images()

# draw_pieces
def draw_pieces(screen, board):
    # put piece into the middle by offsets
    offset = (SQUARE_SIZE - PIECE_SIZE) // 2
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                piece_image = IMAGES[f"{piece.color[0]}{piece.piece_type.lower()}"]
                x_pos = col * SQUARE_SIZE + offset
                y_pos = row * SQUARE_SIZE + offset
                screen.blit(piece_image, (x_pos, y_pos))

# click cell
def get_cell_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col



def run_game():

    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Chess with Agents - HCMUT')
    board = ChessBoard()
    game = Rules()
    selected_piece = None
    cell_moves = []
    black_agent = RandomAgent('black', game)
    

    user_choice = main_menu(screen, "./ui/assets/background.jpg")
    if not user_choice:
        # Người dùng chọn EXIT
        pygame.quit()
        return
    player_turn = choose_first_player(screen)
    running = True
    # start game
    while running:
        move_made = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn == 'white':
                realtime_pos = pygame.mouse.get_pos()
                row, col = get_cell_from_mouse(realtime_pos)

                if selected_piece is None:
                    piece = game.board.board[row][col]
                    if piece is not None and piece.color == player_turn:
                        selected_piece = piece
                        cell_moves = game.generate_legal_moves(piece) 
                else:
                    if (row, col) in cell_moves:
                        game.make_move(selected_piece, (row, col))
                        player_turn = 'black'
                        move_made = True

                    selected_piece = None
                    cell_moves = []

        draw_board(screen)
        draw_pieces(screen, game.board)

        if selected_piece:
            for move in cell_moves:
                r, c = move
                highlight_color = pygame.Color(255, 100, 100, 50)  # ví dụ màu đỏ
                pygame.draw.rect(
                    screen, 
                    highlight_color, 
                    pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 
                    width=5
                )
        draw_notification(screen)
        pygame.display.flip()

        if move_made:
            status_white = game.check_status('black')
            if status_white == "checkmate":
                show_notification("Checkmate! Black loses.", 3000)
                # update UI
                draw_board(screen)
                draw_pieces(screen, game.board)
                draw_notification(screen)
                pygame.display.flip()

                user_choice = popup_checkmate(screen, "Replay or exit?")
                if user_choice:
                    game.reset_all()
                    player_turn = 'white'
                    cell_moves = []
                else:
                    running = False

            elif status_white == "check":
                show_notification( "Checking! Black is in check.", 2000)
                # update UI
                draw_board(screen)
                draw_pieces(screen, game.board)
                draw_notification(screen)
                pygame.display.flip()


        if running and player_turn == 'black':
            pygame.time.delay(500)  
            agent_move = black_agent.select_move()
            if agent_move:
                piece, move = agent_move
                game.make_move(piece, move)

                status_black = game.check_status('white')
                if status_black == "checkmate":
                    show_notification("Checkmate! White loses.", 3000)
                    draw_board(screen)
                    draw_pieces(screen, game.board)
                    draw_notification(screen)
                    pygame.display.flip()

                    user_choice = popup_checkmate(screen, "Replay or exit?")
                    if user_choice:
                        game.reset_all()
                        player_turn = 'white'
                        cell_moves = []
                    else:
                        running = False

                elif status_black == "check":
                    show_notification("Checking! White is in check.", 2000)
                    
            else:
                show_notification("Game over! Black has no moves.", 3000)
                draw_notification(screen)
                running = False

            player_turn = 'white'
            cell_moves = []  

            draw_board(screen)
            draw_pieces(screen, game.board)
            draw_notification(screen)
            pygame.display.flip()

    pygame.quit()


