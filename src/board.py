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
        pygame.draw.rect(self.screen, BLACK, pygame.Rect(WIDTH - 650, 150, 600, 200), 2)
        text_surface = GAME_STATUS_FONT.render("Game Status", True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 640, 160))
        self._screen.blit(text_surface, text_rect)
        text_surface = GAME_STATUS_FONT.render("Match:", True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 640, 200))
        self._screen.blit(text_surface, text_rect)
        text_surface = GAME_STATUS_FONT.render("Current Player:", True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 640, 230))
        self._screen.blit(text_surface, text_rect)
        text_surface = GAME_STATUS_FONT.render("Moves Count:", True, BLACK)
        text_rect = text_surface.get_rect(topleft = (WIDTH - 640, 260))
        self._screen.blit(text_surface, text_rect)

class Pieces:
    def __init__(self, screen):
        self._pieces = {
            # "red": [(0, 12), (1, 11), (1, 13), (2, 10), (2, 12), (2, 14), (3, 9), (3, 11), (3, 13), (3, 15)],
            # "orange": [(16,12),(15, 11), (15, 13), (14, 10), (14, 12), (14, 14), (13, 9), (13, 11), (13, 13), (13, 15)],
            "yellow": [(4,0), (4,2), (4,4), (4,6), (5,1), (5,3), (5,5), (6,2), (6,4), (7,3)],
            "green": [(9,21), (10,20), (10,22), (11,19), (11,21), (11,23), (12,18), (12,20), (12,22), (12,24)],
            "purple": [(4,18), (4,20), (4,22), (4,24), (5,19), (5,21), (5,23), (6,20), (6,22), (7,21)],
            "blue": [(9,3), (10,2), (10,4), (11,1), (11,3), (11,5), (12,0), (12,2), (12,4), (12,6)]
        }
        self._screen = screen
    
    @property
    def pieces(self):
        return self._pieces
    
    @property
    def screen(self):
        return self._screen
        
    @pieces.setter
    def pieces(self, value):
        print(value)
    
    def drawPieces(self):
        for color, positions in self._pieces.items():
            for row, col in positions:
                x, y = getPixelCoordinates(row, col)
                pygame.draw.circle(self._screen, color, (int(x), int(y)), CIRCLE_RADIUS)
                pygame.draw.circle(self._screen, BLACK, (int(x), int(y)), CIRCLE_RADIUS, 2)
                # self.drawCoordinates(f"{row},{col}", (int(x), int(y)))
    
    def drawCoordinates(self, text, position):
        text_surface = CORDINATES_FONT.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=position)
        self._screen.blit(text_surface, text_rect)

class Button:
    def __init__(self, screen, color, font, text, size, pos):
        self._screen = screen
        self._color = color
        self._font = font
        self._text = text
        self._rect = pygame.Rect(pos, size)
        
    @property
    def rect(self):
        return self._rect

    @property
    def text(self):
        return self._text

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
    
    def draw(self):
        pygame.draw.rect(self._screen, self._color, self._rect)
        text_surface = self._font.render(self._text, True, WHITE)
        text_rect = text_surface.get_rect(center=self._rect.center)
        self._screen.blit(text_surface, text_rect)
        
        

    
    
