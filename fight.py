#!/usr/bin/env python
import pygame
import random
import sys
from core.chessRules import Rules
from agents.random_agent import RandomAgent
from agents.minmax_agent import MinMaxAgent

def run_simulation():
    pygame.init()

    game = Rules()
    #  white agent uses MinmaxAgent, black agent uses RandomAgent
    white_agent = MinMaxAgent('white', game)
    black_agent = RandomAgent('black', game)

    # random first turn
    player_turn = random.choice(['white', 'black'])
    move_counter = 0

    while True:
        move_counter += 1
        print(f"\nMove {move_counter}, turn: {player_turn}")

        if player_turn == 'white':
            agent_move = white_agent.select_move()
            if agent_move is None:
                print("White agent has no moves left! Game over.")
                break
            piece, move = agent_move
            print(f"White moves {piece} to {move}")
            game.make_move(piece, move)
        else:
            agent_move = black_agent.select_move()
            if agent_move is None:
                print("White agent has no moves left! Game over.")
                break
            piece, move = agent_move
            print(f"Black moves {piece} to {move}")
            game.make_move(piece, move)

        # end statement checking
        white_status = game.check_status('white')
        black_status = game.check_status('black')
        if white_status == "checkmate":
            print("Checkmate! White loses.")
            break
        elif black_status == "checkmate":
            print("Checkmate! Black loses.")
            break

        # swap turn
        player_turn = 'black' if player_turn == 'white' else 'white'

    pygame.quit()

if __name__ == "__main__":
    run_simulation()
