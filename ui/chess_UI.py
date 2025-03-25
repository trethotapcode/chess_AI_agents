# python ui/chess_UI.py
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import pygame
from core.chessBoard import ChessBoard
from core.chessRules import Rules
from agents.random_agent import RandomAgent


pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Chess with Agents - HCMUT')

SQUARE_SIZE = 80
PIECE_SIZE = 70
board = ChessBoard()
game = Rules()
selected_piece = None
player_turn = 'white'
cell_moves = []
black_agent = RandomAgent('black', game)
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


running = True
while running:
    mode_made = False

    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False

            # click mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            realtime_pos = pygame.mouse.get_pos()
            row, col = get_cell_from_mouse(realtime_pos)

            # first click to selected piece
            if selected_piece is None:
                piece = game.board.board[row][col]
                # steps where cell can move
                if piece is not None and piece.color == player_turn:
                    selected_piece = piece
                    cell_moves = game.generate_move(piece)

            # second click: move piece to new_position
            else:
                if (row, col) in cell_moves:
                    game.make_move(selected_piece, (row, col))
                    player_turn = 'black' 
                    mode_made = True
                # un-select if click cells not in move list or after moves.
                selected_piece = None
                cell_moves = []
                
    draw_board(screen)
    draw_pieces(screen, game.board)

    # hightlight cell_moves if selected
    if selected_piece:
        for move in cell_moves:
            r, c = move
            highlight_color = pygame.Color(255, 100, 100, 50)  # red
            pygame.draw.rect(screen, highlight_color, pygame.Rect(
                c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
    pygame.display.flip()
            
    # agent's turn
    if player_turn == 'black':
        pygame.time.delay(500)
        agent_move = black_agent.select_move()
        if agent_move:
            piece, move = agent_move
            game.make_move(piece, move)
        player_turn = 'white'
        valid_moves = []  

        draw_board(screen)
        draw_pieces(screen, game.board)
        pygame.display.flip()


    


pygame.quit()
