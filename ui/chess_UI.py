# initial setting
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import pygame
from core.chessBoard import ChessBoard

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Chess with Agents - HCMUT')

SQUARE_SIZE = 80
PIECE_SIZE = 70
board = ChessBoard()

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
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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
                screen.blit(piece_image, pygame.Rect(x_pos, y_pos, PIECE_SIZE, PIECE_SIZE))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_board(screen)
    draw_pieces(screen, board)
    pygame.display.flip()

pygame.quit()
