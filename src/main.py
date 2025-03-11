import pygame
from settings import *
from game import Game
from engine import Engine
from player import Player
import time
from AI import randomAI
import numpy as np

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    engine = Engine()
    
    player1 = Player(1, COLORS[0], True, randomAI(engine))
    player2 = Player(2, COLORS[1], True, randomAI(engine))

    game = Game(screen, [player1, player2], engine)
    
    running = True
    while running:
        # clock.tick(FPS)
        if not game.end:
            running = game.loop()
    pygame.quit()

def old_testing():
    game = Engine()
    game_loop = True
    start_time = time.time_ns()

    # Start game loop
    while game_loop:
        turn_start_time = time.time_ns()
        print("___________________", game.turn_count, "________________________\nIt is player", game.is_p2_turn + 1,
              "turn.")
        print(game.player_loc.astype(np.int8))  # Shows current board, replace with visuals if you may.
        possible_moves = game.results(game.actions())  # For the current player
        # Update current game state with a randomly chosen move:
        game_loop = not game.update_state(possible_moves[np.random.choice(len(possible_moves))])
        print("--- %s ms ---" % ((time.time_ns() - turn_start_time) // 1_000_000))
    print("End board state:\n", game.player_loc.astype(np.int8), "\nTotal run time: ",
          (time.time_ns() - start_time) // 1_000_000, " ms")


if __name__ == "__main__":
    #old_testing()
    main()