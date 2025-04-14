# python -m ui/chess_UI.py
import sys

# run - not ctrl + S 
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

def load_images():
    color_type = ['b', 'w']
    pieces = ['bishop', 'king', 'knight', 'pawn', 'queen', 'rook']
    images_piece = {}

    for color in color_type:
        for piece in pieces:
            path = f"./ui/assets/{color}{piece}.png"
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (PIECE_SIZE, PIECE_SIZE))
                images_piece[f"{color}{piece}"] = img
            except Exception as e:
                print(f"Error loading image {path}: {e}")

    return images_piece

# draw board
def draw_board(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for r in range(8):
        for c in range(8):
            color = colors[(r+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# draw pieces
def draw_pieces(screen, board):
    offset = (SQUARE_SIZE - PIECE_SIZE) // 2
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                key = f"{piece.color[0]}{piece.piece_type.lower()}"
                if key in IMAGES:
                    x_pos = col * SQUARE_SIZE + offset
                    y_pos = row * SQUARE_SIZE + offset
                    screen.blit(IMAGES[key], (x_pos, y_pos))

# click cell
def get_cell_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

# popup for promotion
def promotion_popup(screen, color):
    promotion_choices = [
        ("Queen",  f"./ui/assets/{color[0]}queen.png"),
        ("Rook",   f"./ui/assets/{color[0]}rook.png"),
        ("Bishop", f"./ui/assets/{color[0]}bishop.png"),
        ("Knight", f"./ui/assets/{color[0]}knight.png")
    ]
    list_of_promos = []
    image_size = (90, 90)  

    for piece_name, path in promotion_choices:
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, image_size)
            list_of_promos.append((piece_name, img))
        except Exception as e:
            print(f"img_error {path}: {e}")

    n = len(list_of_promos)
    spacing = 5
    margin = 5
    img_w, img_h = image_size

    total_images_width = n * img_w + (n - 1) * spacing
    box_width = 2 * margin + total_images_width
    box_height = img_h + 2 * margin

    screen_width, screen_height = screen.get_size()
    box_x = (screen_width - box_width) // 2
    box_y = (screen_height - box_height) // 2

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x_draw = box_x + margin
                for piece_name, img in list_of_promos:
                    rect = img.get_rect(topleft=(x_draw, box_y + (box_height - img_h) // 2))
                    if rect.collidepoint(mouse_x, mouse_y):
                        return piece_name
                    x_draw += img_w + spacing

        layer_surface = pygame.Surface((box_width, box_height))
        layer_surface.fill(pygame.Color("lightyellow"))
        screen.blit(layer_surface, (box_x, box_y))

        x_draw = box_x + margin
        for piece_name, img in list_of_promos:
            rect = img.get_rect(topleft=(x_draw, box_y + (box_height - img_h) // 2))
            screen.blit(img, rect)
            x_draw += img.get_width() + spacing

        pygame.display.flip()
        clock.tick(30)



IMAGES = load_images()

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Chess with Agents - HCMUT')
    game = Rules()
    selected_piece = None
    cell_moves = []
    black_agent = RandomAgent('black', game)
    
    user_choice = main_menu(screen, "./ui/assets/background.jpg")
    if not user_choice:
        pygame.quit()
        return
    player_turn = choose_first_player(screen)
    running = True

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
                        # Pawn promotion
                        if selected_piece.piece_type == "Pawn":
                            if (selected_piece.color == "white" and selected_piece.position[0] == 0) or \
                               (selected_piece.color == "black" and selected_piece.position[0] == 7):
                                if selected_piece.color == "white":
                                    new_type = promotion_popup(screen, selected_piece.color)
                                else:
                                    new_type = "Queen"
                                selected_piece.piece_type = new_type
                        player_turn = 'black'
                        move_made = True

                    selected_piece = None
                    cell_moves = []

        # draw board and piece
        draw_board(screen)
        draw_pieces(screen, game.board)

        if selected_piece:
            for move in cell_moves:
                r, c = move
                highlight_color = pygame.Color(255, 100, 100, 50)
                pygame.draw.rect(screen, highlight_color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=5)
                
        draw_notification(screen)
        pygame.display.flip()

        if move_made:
            status_black = game.check_status('black')
            if status_black == "checkmate":
                show_notification("Checkmate! Black loses.", 3000)
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
                show_notification("Checking! Black is in check.", 2000)
                draw_board(screen)
                draw_pieces(screen, game.board)
                draw_notification(screen)
                pygame.display.flip()

        #  agent (black)
        if running and player_turn == 'black':
            pygame.time.delay(500)
            agent_move = black_agent.select_move()
            if agent_move:
                piece, move = agent_move
                game.make_move(piece, move)
                # agent promotion
                if piece.piece_type == "Pawn" and piece.position[0] == 7:
                    piece.piece_type = "Queen"
                    
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

if __name__ == "__main__":
    run_game()
