import pygame
from settings import *
from utilities import *

class Board:
    def __init__(self, screen):
        self._board = self.createBoard()
        self._screen = screen
    
    @property
    def board(self):
        return self._board

    @property
    def screen(self):
        return self._screen

    def createBoard(self):
        board = []
        for row in range(0, BOARD_HEIGHT + 1):
            if row < 4:
                for i in range(0, row + 1):
                    col = (24-2*row)/2 + i*2
                    board.append((row, col))
            if row > 12 :
                for i in range(0, BOARD_HEIGHT - row):
                    col = (24-2*(BOARD_HEIGHT - row - 1))/2 + i*2
                    board.append((row, col))
            if row == 4 or row == 12:
                for i in range(0, 13):
                    col = 2*i
                    board.append((row, col))
            if row == 5 or row == 11:
                for i in range(0, 12):
                    col = 1 + 2*i
                    board.append((row, col))
            if row == 6 or row == 10:
                for i in range(0, 11):
                    col = 2 + 2*i
                    board.append((row, col))
            if row == 7 or row == 9:
                for i in range(0, 10):
                    col = 3 + 2*i
                    board.append((row, col))
            if row == 8:
                for i in range(0, 9):
                    col = 4 + 2*i
                    board.append((row, col))
        return board

    def drawBoard(self):
        for row, col in self.board:
            x, y = getPixelCoordinates(row, col)
            pygame.draw.circle(self.screen, GRAY, (int(x), int(y)), CIRCLE_RADIUS)
            pygame.draw.circle(self.screen, BLACK, (int(x), int(y)), CIRCLE_RADIUS, 2)
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(WIDTH - 550, 100, 500, 200), 2)
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render("Game Status", True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 540, 110))
        self._screen.blit(text_surface, text_rect)
        text_surface = font.render("Current Player:", True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 540, 140))
        self._screen.blit(text_surface, text_rect)

    
    
