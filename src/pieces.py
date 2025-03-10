from settings import *
from utilities import *
import pygame
import math

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
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=position)
        self._screen.blit(text_surface, text_rect)
