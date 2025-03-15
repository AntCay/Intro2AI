import pygame

pygame.init()
# Game settings
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]
FPS = 30
BOARD_WIDTH = 25
BOARD_HEIGHT = 17
CELL_SIZE = int(HEIGHT/20)
CIRCLE_RADIUS = CELL_SIZE // 2.5
SLEEP_DURATION = 0
MAX_MOVES = 10000
TITLE = "Chinese Checkers"
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
COLORS = ["red", "orange", "yellow", "green", "purple", "blue"]
BUTTON_MENU_FONT = pygame.font.Font(None, 36)
GAME_STATUS_FONT = pygame.font.Font(None, 30)
CORDINATES_FONT = pygame.font.Font(None, 24)


