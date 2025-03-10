import pygame
from settings import *
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game = Game(screen)
    
    running = True
    while running:
        game.draw()
        if game.currentPlayer.isAI:
            game.AIMove()
        else:    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                    game.handleClick(event.pos)

    pygame.quit()

if __name__ == "__main__":
    main()