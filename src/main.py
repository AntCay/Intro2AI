import pygame
from settings import *
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    screen.fill(WHITE)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game = Game(screen)
    
    running = True
    while running:
        clock.tick(FPS)
        game.draw()
        if not game.end:
            if game.currentPlayer.isAI:
                game.AIMove()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            else:    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        game.handleClick(event.pos)

    pygame.quit()

if __name__ == "__main__":
    main()