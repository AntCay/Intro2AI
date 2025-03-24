import pygame
from settings import *
from game import Game
from engine import Engine
from player import Player
from AI import *
import numpy as np
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    engine = Engine()
    
    player1 = Player(1, COLORS[0], True, LookAhead_h2(engine))
    player2 = Player(2, COLORS[1], True, MiniMax_h2(engine))
    
    result_path = "../result/{}_vs_{}.csv".format(player1.name, player2.name)
    
    game = Game(screen, [player1, player2], engine, MAX_MATCHES, result_path)
    running = True
    while running:
        # clock.tick(FPS)
        running = game.loop()
         
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()